"""Open Kit 3D - shared bpy helper library (M1; M3 adds validate_extra).

Conventions (see PLAN.md):
  * 1 unit = 1 m, pivot at bottom-center, transforms applied.
  * Front of every asset faces Blender -Y (Unity +Z after FBX export + Bake Axis Conversion).
  * At most five material slots: Primary, Secondary, Accent, Metal, Emissive (neutral grey).
  * Flat-shaded low-poly, no textures, no UV work needed.
"""
import bpy
import bmesh
import math
import os
import json
import time
from mathutils import Matrix, Vector

SLOTS = ["Primary", "Secondary", "Accent", "Metal", "Emissive"]
BEVEL = 0.012          # house bevel width (m) - fixed for style consistency
GRID = 1.5             # 1 grid cell = 1.5 m (5 ft)

# neutral grey values per slot (viewport + base colour), metallic, roughness
_SLOT_LOOK = {
    "Primary":   ((0.60, 0.60, 0.60), 0.0, 0.80),
    "Secondary": ((0.42, 0.42, 0.42), 0.0, 0.85),
    "Accent":    ((0.80, 0.80, 0.80), 0.0, 0.60),
    "Metal":     ((0.30, 0.30, 0.30), 1.0, 0.40),
    "Emissive":  ((0.92, 0.92, 0.92), 0.0, 0.50),
}

# ----------------------------------------------------------------- scene / materials

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.unit_settings.system = 'METRIC'
    s.unit_settings.scale_length = 1.0


def slot_material(slot):
    assert slot in SLOTS, slot
    mat = bpy.data.materials.get(slot)
    if mat:
        return mat
    mat = bpy.data.materials.new(slot)
    col, metal, rough = _SLOT_LOOK[slot]
    mat.diffuse_color = (*col, 1.0)
    mat.metallic = metal
    mat.roughness = rough
    try:
        mat.use_nodes = True   # no-op / deprecated in Blender 5.x
    except Exception:
        pass
    nt = mat.node_tree
    if nt is not None:
        bsdf = next((n for n in nt.nodes if n.type == 'BSDF_PRINCIPLED'), None)
        if bsdf is None:
            bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
            out = next((n for n in nt.nodes if n.type == 'OUTPUT_MATERIAL'), None) or nt.nodes.new('ShaderNodeOutputMaterial')
            nt.links.new(bsdf.outputs[0], out.inputs[0])
        bsdf.inputs['Base Color'].default_value = (*col, 1.0)
        bsdf.inputs['Metallic'].default_value = metal
        bsdf.inputs['Roughness'].default_value = rough
        if slot == "Emissive":
            for key in ("Emission Color", "Emission"):
                if key in bsdf.inputs:
                    bsdf.inputs[key].default_value = (*col, 1.0)
                    break
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = 2.0
    return mat


# ----------------------------------------------------------------- mesh builder

class Builder:
    """Accumulates parts (each with one slot) into one bmesh, then makes one object."""

    def __init__(self, name):
        self.name = name
        self.bm = bmesh.new()
        # M4 rigging: parts built inside `with b.bone("name"):` are weighted 1.0 to that bone (rigid parts);
        # parts built inside `with b.bone(AUTO):` get weights from the skin(co) callback passed to build() (smooth skinning).
        self.bone_names = []
        self._bone = None
        self._dl = None

    from contextlib import contextmanager as _cm

    @_cm
    def bone(self, name):
        """Context manager: every part added inside is bound to bone `name` (weight 1.0)."""
        if name not in self.bone_names:
            self.bone_names.append(name)
        prev, self._bone = self._bone, name
        try:
            yield self
        finally:
            self._bone = prev

    # -- internal: finish a part bmesh and merge it
    def _merge(self, pbm, slot, matrix=None, recalc=True):
        idx = SLOTS.index(slot)
        if matrix is not None:
            bmesh.ops.transform(pbm, matrix=matrix, verts=pbm.verts)
        if recalc:
            bmesh.ops.recalc_face_normals(pbm, faces=pbm.faces)
        for f in pbm.faces:
            f.material_index = idx
            f.smooth = False
        tmp = bpy.data.meshes.new("_tmp")
        pbm.to_mesh(tmp)
        pbm.free()
        n0 = len(self.bm.verts)
        self.bm.from_mesh(tmp)
        bpy.data.meshes.remove(tmp)
        if self._bone is not None:
            if self._dl is None:
                self._dl = self.bm.verts.layers.deform.verify()
            gi = self.bone_names.index(self._bone)
            self.bm.verts.ensure_lookup_table()
            for v in self.bm.verts[n0:]:
                v[self._dl][gi] = 1.0

    @staticmethod
    def _bevel(pbm, width, segments=1):
        if width and width > 0:
            bmesh.ops.bevel(pbm, geom=list(pbm.verts) + list(pbm.edges), offset=width,
                            offset_type='OFFSET', segments=segments, profile=0.5,
                            affect='EDGES', clamp_overlap=True)

    # -- primitives ------------------------------------------------------
    def box(self, size, loc=(0, 0, 0), slot="Primary", bevel=BEVEL, rot=(0, 0, 0), bottom=True):
        """Axis box. size=(x,y,z). loc = bottom-center (bottom=True) or center."""
        pbm = bmesh.new()
        bmesh.ops.create_cube(pbm, size=1.0)
        bmesh.ops.scale(pbm, vec=Vector(size), verts=pbm.verts)
        if bottom:
            bmesh.ops.translate(pbm, vec=Vector((0, 0, size[2] / 2)), verts=pbm.verts)
        self._bevel(pbm, min(bevel, min(size) * 0.3) if bevel else 0)
        m = Matrix.Translation(Vector(loc)) @ _euler(rot)
        self._merge(pbm, slot, m)

    def cylinder(self, r, h, segs=8, loc=(0, 0, 0), slot="Primary", r_top=None, caps=True,
                 bevel=0.0, rot=(0, 0, 0), phase=None):
        """Cylinder / cone standing on loc (bottom-center)."""
        pbm = bmesh.new()
        bmesh.ops.create_cone(pbm, cap_ends=caps, cap_tris=False, segments=segs,
                              radius1=r, radius2=(r if r_top is None else r_top), depth=h)
        bmesh.ops.translate(pbm, vec=Vector((0, 0, h / 2)), verts=pbm.verts)
        if phase is None:
            phase = math.pi / segs  # put a flat face toward -Y (front)
        bmesh.ops.rotate(pbm, cent=Vector(), matrix=Matrix.Rotation(phase, 3, 'Z'), verts=pbm.verts)
        if bevel:
            self._bevel(pbm, bevel)
        m = Matrix.Translation(Vector(loc)) @ _euler(rot)
        self._merge(pbm, slot, m)

    def lathe(self, profile, segs=8, loc=(0, 0, 0), slot="Primary", closed=False,
              cap_bottom=True, cap_top=True, rot=(0, 0, 0), phase=None):
        """Revolve a (radius, z) profile around Z. r==0 points become poles."""
        pbm = bmesh.new()
        if phase is None:
            phase = math.pi / segs
        rings = []
        for (r, z) in profile:
            if r <= 1e-6:
                rings.append([pbm.verts.new((0, 0, z))])
            else:
                rings.append([pbm.verts.new((r * math.cos(phase + 2 * math.pi * i / segs),
                                             r * math.sin(phase + 2 * math.pi * i / segs), z))
                              for i in range(segs)])
        pairs = list(zip(rings[:-1], rings[1:]))
        if closed:
            pairs.append((rings[-1], rings[0]))
        for a, b in pairs:
            for i in range(segs):
                j = (i + 1) % segs
                if len(a) == 1 and len(b) == 1:
                    continue
                if len(a) == 1:
                    pbm.faces.new((a[0], b[i], b[j]))
                elif len(b) == 1:
                    pbm.faces.new((a[i], a[j], b[0]))
                else:
                    pbm.faces.new((a[i], a[j], b[j], b[i]))
        if not closed:
            if cap_bottom and len(rings[0]) > 1:
                pbm.faces.new(list(reversed(rings[0])))
            if cap_top and len(rings[-1]) > 1:
                pbm.faces.new(rings[-1])
        m = Matrix.Translation(Vector(loc)) @ _euler(rot)
        self._merge(pbm, slot, m)

    def ring(self, r_in, r_out, h, segs=8, loc=(0, 0, 0), slot="Metal", rot=(0, 0, 0), phase=None):
        """Flat band / hoop (closed rectangular profile)."""
        prof = [(r_in, 0), (r_out, 0), (r_out, h), (r_in, h)]
        self.lathe(prof, segs, loc, slot, closed=True, rot=rot, phase=phase)

    def strut(self, p0, p1, t=0.04, slot="Primary", bevel=BEVEL, segs=None):
        """Square (segs=None) or n-gon (segs=n) bar from point p0 to p1."""
        p0, p1 = Vector(p0), Vector(p1)
        d = p1 - p0
        L = d.length
        q = Vector((0, 0, 1)).rotation_difference(d.normalized())
        m = Matrix.Translation(p0) @ q.to_matrix().to_4x4()
        pbm = bmesh.new()
        if segs:
            bmesh.ops.create_cone(pbm, cap_ends=True, cap_tris=False, segments=segs,
                                  radius1=t / 2, radius2=t / 2, depth=L)
        else:
            bmesh.ops.create_cube(pbm, size=1.0)
            bmesh.ops.scale(pbm, vec=Vector((t, t, L)), verts=pbm.verts)
        bmesh.ops.translate(pbm, vec=Vector((0, 0, L / 2)), verts=pbm.verts)
        if bevel and not segs:
            self._bevel(pbm, min(bevel, t * 0.3))
        self._merge(pbm, slot, m)

    def prism(self, points, depth, loc=(0, 0, 0), slot="Primary", axis='Z', rot=(0, 0, 0)):
        """Extrude a 2D polygon. axis='Z': points=(x,y), z 0..depth.
        axis='X': points=(y,z), x -depth/2..depth/2.  axis='Y': points=(x,z), y -depth/2..depth/2."""
        pbm = bmesh.new()
        def v3(u, v, w):
            if axis == 'Z':
                return (u, v, w)
            if axis == 'X':
                return (w - depth / 2, u, v)
            return (u, w - depth / 2, v)
        a = [pbm.verts.new(v3(u, v, 0)) for (u, v) in points]
        b_ = [pbm.verts.new(v3(u, v, depth)) for (u, v) in points]
        n = len(points)
        pbm.faces.new(list(reversed(a)))
        pbm.faces.new(b_)
        for i in range(n):
            j = (i + 1) % n
            pbm.faces.new((a[i], a[j], b_[j], b_[i]))
        m = Matrix.Translation(Vector(loc)) @ _euler(rot)
        self._merge(pbm, slot, m)

    def flame(self, base, height, radius, segs=4, twist=70, lean=(0, 0), slot="Emissive", phase=0.0,
              profile=((0.0, 0.8), (0.2, 1.0), (0.48, 0.75), (0.76, 0.32))):
        """Low-poly flame tongue: stacked, twisted, tapering rings bending along `lean`, ending in a tip."""
        pbm = bmesh.new()
        rings = []
        for (t, rf) in profile:
            ang = phase + math.radians(twist) * t
            ox, oy = lean[0] * t * t, lean[1] * t * t
            r = radius * rf
            rings.append([pbm.verts.new((ox + r * math.cos(ang + 2 * math.pi * i / segs),
                                         oy + r * math.sin(ang + 2 * math.pi * i / segs), height * t))
                          for i in range(segs)])
        tip = pbm.verts.new((lean[0], lean[1], height))
        pbm.faces.new(list(reversed(rings[0])))
        for a, b in zip(rings[:-1], rings[1:]):
            for i in range(segs):
                j = (i + 1) % segs
                pbm.faces.new((a[i], a[j], b[j], b[i]))
        for i in range(segs):
            pbm.faces.new((rings[-1][i], rings[-1][(i + 1) % segs], tip))
        self._merge(pbm, slot, Matrix.Translation(Vector(base)))

    def broken_shaft(self, r, h, segs=12, jag=0.08, seed=1, loc=(0, 0, 0), slot="Primary", rot=(0, 0, 0),
                     jag_bottom=0.0, r_top=None):
        """Column piece with a jagged (broken) top and optionally bottom."""
        import random
        rnd = random.Random(seed)
        rt = r if r_top is None else r_top
        pbm = bmesh.new()
        ph = math.pi / segs
        bot = [pbm.verts.new((r * math.cos(ph + 2 * math.pi * i / segs), r * math.sin(ph + 2 * math.pi * i / segs),
                              rnd.uniform(-jag_bottom, jag_bottom) + jag_bottom)) for i in range(segs)]
        top = [pbm.verts.new((rt * math.cos(ph + 2 * math.pi * i / segs), rt * math.sin(ph + 2 * math.pi * i / segs),
                              h + rnd.uniform(-jag, jag))) for i in range(segs)]
        ct = pbm.verts.new((0, 0, h - jag * 0.5))
        cb = pbm.verts.new((0, 0, jag_bottom * (1.4 if jag_bottom else 0)))
        for i in range(segs):
            j = (i + 1) % segs
            pbm.faces.new((bot[i], bot[j], top[j], top[i]))
            pbm.faces.new((top[i], top[j], ct))
            pbm.faces.new((bot[j], bot[i], cb))
        m = Matrix.Translation(Vector(loc)) @ _euler(rot)
        self._merge(pbm, slot, m)

    def gem(self, r, h, loc=(0, 0, 0), slot="Accent", segs=4, rot=(0, 0, 0)):
        self.lathe([(0.0, 0.0), (r, h * 0.45), (r * 0.6, h * 0.8), (0.0, h)], segs, loc, slot, rot=rot)

    # -- finish ----------------------------------------------------------
    def build(self, skin=None):
        """Create the object. Returns (obj, tri_count).
        skin: optional callable(co: Vector) -> {bone_name: weight} used for parts built inside `with b.bone(AUTO):`."""
        bm = self.bm
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-5)
        if self._dl is not None and AUTO in self.bone_names:
            ai = self.bone_names.index(AUTO)
            if skin is None:
                raise ValueError("parts use bone AUTO but build() got no skin callback")
            for v in bm.verts:
                dv = v[self._dl]
                if ai in dv:
                    ws = {k: w for k, w in skin(v.co.copy()).items() if w > 1e-4}
                    tot = sum(ws.values())
                    if tot <= 0:
                        raise ValueError(f"skin() returned no weight at {tuple(v.co)}")
                    del dv[ai]
                    for k, w in ws.items():
                        if k not in self.bone_names:
                            self.bone_names.append(k)
                        dv[self.bone_names.index(k)] = w / tot
        bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method='BEAUTY', ngon_method='EAR_CLIP')
        used = sorted({f.material_index for f in bm.faces})
        remap = {old: new for new, old in enumerate(used)}
        for f in bm.faces:
            f.material_index = remap[f.material_index]
        me = bpy.data.meshes.new(self.name)
        bm.to_mesh(me)
        bm.free()
        for old in used:
            me.materials.append(slot_material(SLOTS[old]))
        for p in me.polygons:
            p.use_smooth = False
        obj = bpy.data.objects.new(self.name, me)
        bpy.context.scene.collection.objects.link(obj)
        if self._dl is not None:
            for n in self.bone_names:
                obj.vertex_groups.new(name=n)
            if AUTO in obj.vertex_groups:
                obj.vertex_groups.remove(obj.vertex_groups[AUTO])
        return obj, tri_count(obj)


AUTO = "__auto__"


def _euler(rot):
    from mathutils import Euler
    return Euler(tuple(math.radians(a) for a in rot), 'XYZ').to_matrix().to_4x4()


def tri_count(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)


def dims(obj):
    xs = [v.co.x for v in obj.data.vertices]; ys = [v.co.y for v in obj.data.vertices]; zs = [v.co.z for v in obj.data.vertices]
    return (max(xs) - min(xs), max(ys) - min(ys), max(zs) - min(zs)), (min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))


def recenter(obj):
    """Shift mesh so bbox centre xy = 0 and min z = 0 (bottom-centre pivot)."""
    (dx, dy, dz), mn, mx = dims(obj)
    off = Vector((-(mn[0] + mx[0]) / 2, -(mn[1] + mx[1]) / 2, -mn[2]))
    obj.data.transform(Matrix.Translation(off))
    return tuple(off)   # M3: callers shift light sockets by the same offset


PIVOTS = {
    "bottom_center": "bottom-centre (default)",
    "hinge": "door hinge: hinge axis at x = 0, door extends toward +X, min z = 0, slab centred in depth",
    "wall_back": "wall mount: back face at y = 0 (front toward -Y), min z = 0, centred in x",
    "floor_top": "floor tile: top surface at z = 0, centred in xy",
}


def validate(obj, budget, pivot="bottom_center"):
    """Pivot check + budget. Returns dict report."""
    (dx, dy, dz), mn, mx = dims(obj)
    cx, cy = (mn[0] + mx[0]) / 2, (mn[1] + mx[1]) / 2
    rep = {
        "name": obj.name, "tris": tri_count(obj), "budget": budget, "pivot": pivot,
        "dims_m": [round(dx, 3), round(dy, 3), round(dz, 3)],
        "min_z": round(mn[2], 4), "center_xy": [round(cx, 4), round(cy, 4)],
        "slots": [m.name for m in obj.data.materials],
    }
    rep["ok_budget"] = rep["tris"] <= budget
    e = 1e-3
    if pivot == "hinge":
        ok = -0.05 <= mn[0] <= e and mx[0] > 0.3 and abs(mn[2]) < e and abs(cy) < 0.05  # hinge axis at x=0 (knuckles may straddle it)
    elif pivot == "wall_back":
        ok = abs(mx[1]) < e and abs(mn[2]) < e and abs(cx) < 0.02
    elif pivot == "floor_top":
        ok = abs(mx[2]) < e and abs(cx) < 0.02 and abs(cy) < 0.02
    else:
        ok = abs(mn[2]) < e and abs(cx) < 0.02 and abs(cy) < 0.02
    rep["ok_pivot"] = ok
    return rep


# ----------------------------------------------------------------- M3: extended validation
import re as _re

NAME_RE = _re.compile(r"^(prop|tile|wall|monster)-[a-z0-9]+(-[a-z0-9]+)*$")
CATEGORY_FOR_PREFIX = {"prop": "Props", "tile": "Tiles", "wall": "Walls", "monster": "Monsters"}
CATEGORIES = set(CATEGORY_FOR_PREFIX.values())
SIZE_CLASSES = ("Tiny", "Small", "Medium", "Large", "Huge")
# max footprint (largest of x/y, metres) per size class: Tiny <= 0.5 cell (+ slack), Small/Medium ~1 cell
# (long furniture like coffins and pews allowed), Large 2x2, Huge 3x3.  Heights stay within 2 wall tiers.
MAX_FOOTPRINT = {"Tiny": 0.8, "Small": 1.3, "Medium": 2.5, "Large": 3.9, "Huge": 5.0}
MAX_HEIGHT = 6.0
BUDGET_TIERS = (800, 2500, 5000)


def validate_extra(obj, rep, category, size_class, light_socket, budget):
    """Naming, category, scale/transform, missing materials, degenerate faces, size-class footprint, light sockets.
    Adds ok_* keys and a list of human-readable problems to rep."""
    probs = []
    name = obj.name
    # naming: kit prefix + lowercase kebab-case, prefix must match the category folder
    if not NAME_RE.match(name):
        probs.append(f"name '{name}' is not <prefix>-lower-kebab-case")
    pre = name.split("-", 1)[0]
    if category not in CATEGORIES:
        probs.append(f"unknown category '{category}' (known: {sorted(CATEGORIES)})")
    elif CATEGORY_FOR_PREFIX.get(pre) != category:
        probs.append(f"prefix '{pre}-' does not match category '{category}'")
    if size_class not in SIZE_CLASSES:
        probs.append(f"unknown sizeClass '{size_class}'")
    if budget not in BUDGET_TIERS:
        probs.append(f"budget {budget} is not a house tier {BUDGET_TIERS}")
    # scale / transforms: object must be identity (all geometry lives in the mesh)
    if any(abs(v - 1) > 1e-6 for v in obj.scale) or any(abs(v) > 1e-6 for v in obj.rotation_euler) \
            or any(abs(v) > 1e-6 for v in obj.location):
        probs.append("object transform is not identity")
    (dx, dy, dz), mn, mx = dims(obj)
    foot = max(dx, dy)
    if dz < 0.05 or foot < 0.05:
        probs.append(f"degenerate size {dx:.3f}x{dy:.3f}x{dz:.3f}")
    if size_class in MAX_FOOTPRINT and foot > MAX_FOOTPRINT[size_class] + 1e-3:
        probs.append(f"footprint {foot:.2f} m too big for sizeClass {size_class} (max {MAX_FOOTPRINT[size_class]})")
    if dz > MAX_HEIGHT:
        probs.append(f"height {dz:.2f} m > {MAX_HEIGHT}")
    # materials: 1..5 slots, all named house slots, no empty slot, no face pointing past the slot list
    mats = list(obj.data.materials)
    if not mats or len(mats) > len(SLOTS):
        probs.append(f"{len(mats)} material slots (need 1..{len(SLOTS)})")
    if any(m is None for m in mats):
        probs.append("empty material slot")
    bad = [m.name for m in mats if m is not None and m.name not in SLOTS]
    if bad:
        probs.append(f"non-house materials {bad}")
    n = len(mats)
    if any(p.material_index >= n for p in obj.data.polygons):
        probs.append("faces reference a missing material slot")
    unused = sorted(set(range(n)) - {p.material_index for p in obj.data.polygons})
    if unused:
        probs.append(f"unused material slots {[mats[i].name for i in unused]}")
    # flat shading + degenerate faces
    if any(p.use_smooth for p in obj.data.polygons):
        probs.append("smooth-shaded faces (house style is flat)")
    tiny = sum(1 for p in obj.data.polygons if p.area < 1e-8)
    if tiny:
        probs.append(f"{tiny} zero-area faces")
    # lights (M3 category: light-emitting props): socket inside the bounds and an Emissive slot to tint it
    if light_socket:
        e = 0.05
        inside = all(mn[i] - e <= light_socket[i] <= mx[i] + e for i in range(3))
        if not inside:
            probs.append(f"light socket {light_socket} outside bounds {mn}..{mx}")
        if "Emissive" not in rep["slots"]:
            probs.append("light socket but no Emissive slot")
    rep["ok_naming"] = not any(p.startswith(("name", "prefix", "unknown category")) for p in probs)
    rep["problems"] = probs
    rep["ok_extra"] = not probs
    return rep


# ----------------------------------------------------------------- room-adapt rule (2026-09-28): room scale + 3 user colour slots
# User colour slots (inspector overrides on ThemeAdaptive; theme supplies the defaults, a user override wins):
#   Primary   <- Primary material slot
#   Secondary <- Secondary material slot
#   Tertiary  <- Accent + Metal material slots (trim / hardware)
#   (Emissive stays outside the user slots: it is theme-driven and tints the prop's light)
USER_SLOT_OF = {"Primary": "Primary", "Secondary": "Secondary", "Accent": "Tertiary", "Metal": "Tertiary", "Emissive": None}
USER_SLOTS = ("Primary", "Secondary", "Tertiary")
ROOM_SCALE_MODES = ("inhabitant", "grid")


def load_exceptions(path):
    """Explicit, reasoned exceptions to the room-adapt rule. File: Blender/roomadapt_exceptions.json"""
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        data = json.load(f)
    out = {}
    for e in data.get("exceptions", []):
        if not e.get("reason"):
            raise ValueError(f"roomadapt exception for {e.get('asset')} has no reason")
        out.setdefault(e["asset"], set()).add(e["rule"])
    return out


def validate_roomadapt(obj, rep, scales_with_room, room_scale, emissive_scale, exceptions):
    """Every asset must room-scale (all size classes) and expose 3 working user colour slots."""
    probs = []
    exc = exceptions.get(obj.name, set())
    if not scales_with_room and "room_scale" not in exc:
        probs.append("does not scale with the room size class (SCALES_WITH_ROOM = False, no exception)")
    if room_scale not in ROOM_SCALE_MODES:
        probs.append(f"ROOM_SCALE '{room_scale}' not in {ROOM_SCALE_MODES}")
    mats = [m.name for m in obj.data.materials if m is not None]
    unknown = [m for m in mats if m not in USER_SLOT_OF]
    if unknown:
        probs.append(f"materials {unknown} have no theme / user-slot mapping")
    used = {USER_SLOT_OF.get(mats[p.material_index]) for p in obj.data.polygons if p.material_index < len(mats)}
    missing = [u for u in USER_SLOTS if u not in used]
    rep["user_slots"] = [u for u in USER_SLOTS if u in used]
    if missing and "color_slots" not in exc:
        probs.append(f"no mesh region for user colour slot(s) {missing} (Primary<-Primary, Secondary<-Secondary, Tertiary<-Accent/Metal)")
    # scale-safe: uniform scaling happens about the pivot, so the pivot contract must hold exactly
    (dx, dy, dz), mn, mx = dims(obj)
    if rep.get("pivot") == "floor_top":
        if abs(mx[2]) > 1e-3:
            probs.append("floor_top pivot: walking surface not at z = 0 (would sink/float when scaled)")
    elif abs(mn[2]) > 1e-3:
        probs.append("pivot not on the ground plane (min z != 0), would float/sink when scaled")
    if room_scale == "grid" and rep.get("category") in ("Tiles", "Walls") and abs(dx - GRID) > 2e-3:
        probs.append(f"grid piece is {dx:.3f} m wide, must be one {GRID} m cell so it tiles on the scaled room grid")
    if emissive_scale is not None and not (0.0 < emissive_scale <= 1.0):
        probs.append(f"EMISSIVE_SCALE {emissive_scale} outside (0, 1]")
    rep["roomadapt_problems"] = probs
    rep["ok_roomadapt"] = not probs
    return rep


# ----------------------------------------------------------------- export

def export(obj, fbx_dir, glb_dir):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    fbx = os.path.join(fbx_dir, obj.name + ".fbx")
    glb = os.path.join(glb_dir, obj.name + ".glb")
    # Blender->FBX->Unity maps Blender +Y to Unity +Z. Our assets face Blender -Y (standard front view),
    # so spin the mesh 180 deg about Z for the FBX only; Unity then sees the front on +Z with rotation 0.
    # (glTF already maps Blender -Y to +Z, the glTF front, so the GLB is exported unrotated.)
    flip = Matrix.Rotation(math.pi, 4, 'Z')
    obj.data.transform(flip)
    try:
        _export_fbx(fbx)
    finally:
        obj.data.transform(flip)
    bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', use_selection=True,
                              export_apply=True, export_yup=True, export_materials='EXPORT')
    return fbx, glb


def _export_fbx(fbx):
    bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={'MESH'},
                             apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL',
                             axis_forward='-Z', axis_up='Y', bake_space_transform=True,
                             mesh_smooth_type='FACE', use_mesh_modifiers=True,
                             add_leaf_bones=False, bake_anim=False, path_mode='STRIP',
                             use_custom_props=False)


# ----------------------------------------------------------------- preview / turntable sheet

def render_preview(obj, path, report=None, views=(-35, 55, 145, 235), res_x=1280):
    """4-view turntable sheet (front-3/4 then +90 deg steps about the pivot) on a 1.5 m grid floor."""
    scene = bpy.context.scene
    (dx, dy, dz), mn, mx = dims(obj)
    foot = max(dx, dy, GRID * 0.6)
    spacing = max(foot * 1.35, GRID * 1.1)
    n = len(views)
    copies = []
    for i, ang in enumerate(views):
        o = obj if i == 0 else bpy.data.objects.new(f"{obj.name}_v{i}", obj.data)
        if i:
            scene.collection.objects.link(o)
        o.location = ((i - (n - 1) / 2) * spacing, 0, 0)
        o.rotation_euler = (0, 0, math.radians(ang))
        copies.append(o)
        # 1.5 m grid cell outline under each view
        _cell_outline(o.location, f"cell_{i}")
    # floor
    fme = bpy.data.meshes.new("floor"); fbm = bmesh.new()
    bmesh.ops.create_grid(fbm, x_segments=1, y_segments=1, size=spacing * n)
    fbm.to_mesh(fme); fbm.free()
    fl = bpy.data.objects.new("floor", fme); scene.collection.objects.link(fl)
    fmat = bpy.data.materials.new("floor"); fmat.diffuse_color = (0.16, 0.17, 0.19, 1); fme.materials.append(fmat)
    fl.location.z = -0.002
    # camera: ortho, front (-Y), 30 deg elevation
    cam_d = bpy.data.cameras.new("cam"); cam_d.type = 'ORTHO'
    cam = bpy.data.objects.new("cam", cam_d); scene.collection.objects.link(cam)
    elev = math.radians(32)
    width = spacing * n
    aspect = 16 / 7
    height_needed = (dz * math.cos(elev) + foot * math.sin(elev)) * 1.6
    cam_d.ortho_scale = max(width * 1.02, height_needed * aspect)
    target = Vector((0, 0, dz * 0.5 + 0.08 * (dz * math.cos(elev) + foot * math.sin(elev))))
    dirv = Vector((0, -math.cos(elev), math.sin(elev)))
    cam.location = target + dirv * 30
    cam.rotation_euler = (math.pi / 2 - elev, 0, 0)
    cam_d.clip_end = 200
    cam_d.clip_start = 0.1
    scene.camera = cam
    # label
    label = obj.name
    if report:
        label += f"   {report['tris']} tris   {report['dims_m'][0]}x{report['dims_m'][1]}x{report['dims_m'][2]} m   slots: {', '.join(report['slots'])}"
    cu = bpy.data.curves.new("label", 'FONT'); cu.body = label
    cu.size = cam_d.ortho_scale * 0.022
    t = bpy.data.objects.new("label", cu); scene.collection.objects.link(t)
    try:
        t.visible_shadow = False
    except Exception:
        pass
    t.rotation_euler = cam.rotation_euler
    # place label at top-left of frame (in camera plane)
    right = Vector((1, 0, 0)); up = Vector((0, math.sin(elev), math.cos(elev)))
    half_w = cam_d.ortho_scale / 2; half_h = half_w / aspect
    t.location = target + dirv * 29 - right * (half_w * 0.97) + up * (half_h * 0.86)
    lm = bpy.data.materials.new("label"); lm.diffuse_color = (0.95, 0.95, 0.95, 1); cu.materials.append(lm)
    # render settings
    scene.render.resolution_x = res_x
    scene.render.resolution_y = int(res_x / aspect)
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.filepath = path
    ok = False
    try:
        scene.render.engine = 'BLENDER_WORKBENCH'
        sh = scene.display.shading
        sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'
        sh.show_cavity = True; sh.cavity_type = 'WORLD'
        sh.show_shadows = True
        sh.show_object_outline = True
        scene.display.render_aa = '8'
        bpy.ops.render.render(write_still=True)
        ok = os.path.exists(path)
    except Exception as e:
        print("[okit] workbench render failed:", e)
    if not ok:
        scene.render.engine = 'CYCLES'
        scene.cycles.device = 'CPU'; scene.cycles.samples = 32
        bpy.ops.render.render(write_still=True)
    # cleanup extra copies so export state is untouched
    obj.location = (0, 0, 0); obj.rotation_euler = (0, 0, 0)
    return path


def _cell_outline(center, name):
    scene = bpy.context.scene
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    h = GRID / 2; w = 0.015
    for (sx, sy, lx, ly) in [(0, h, GRID, w), (0, -h, GRID, w), (h, 0, w, GRID), (-h, 0, w, GRID)]:
        r = bmesh.ops.create_cube(bm, size=1.0)
        bmesh.ops.scale(bm, vec=Vector((lx, ly, 0.002)), verts=r['verts'])
        bmesh.ops.translate(bm, vec=Vector((sx, sy, 0)), verts=r['verts'])
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); scene.collection.objects.link(o)
    o.location = center
    m = bpy.data.materials.get("cell") or bpy.data.materials.new("cell")
    m.diffuse_color = (0.35, 0.55, 0.85, 1); me.materials.append(m)
    return o


def load_params(params_dir, name):
    p = os.path.join(params_dir, name + ".json")
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return {}



# ----------------------------------------------------------------- M4: rigs (rigid-part monsters + skinned rat) and procedural clips
# An asset script that is rigged defines
#   RIG = [ {"name": "body", "head": (x, y, z), "tail": (x, y, z), "parent": None}, ... ]   authored in the asset's own space
#         (optional "align": (x, y, z) = the bone's local +Z; default: front (-Y) for near-vertical bones, up (+Z) otherwise)
#   CLIPS = {"idle": {"frames": 48, "channels": [(bone, channel, amplitude, cycles, phase_deg), ...]}, "walk": {...}}
#         channel: "rx" / "ry" / "rz" (degrees about the bone's local X / Y / Z) or "lx" / "ly" / "lz" (metres, bone-local location).
#         Bone-local axes with the default align:  local Y = along the bone (head -> tail);
#           near-vertical bone (pointing up or down): local Z = the asset front (-Y), local X = +/- world X
#             -> rx = pitch (lean forward/back), ry = yaw (turn left/right), rz = roll (tilt sideways), ly = up/down along the bone;
#           other bones: local Z = world up -> rx = pitch (nod), rz = yaw (swing sideways), ry = twist.
#         Each channel is amplitude * sin(2 pi * cycles * t / frames + phase), so every clip loops seamlessly (cycles must be whole numbers).
# Every vertex must be weighted (use `with b.bone(...)` for every part), and every weighted group must be a RIG bone.
RIG_NAME = "rig"
FPS = 24


def _bone_align(head, tail, align):
    if align is not None:
        return Vector(align)
    d = (Vector(tail) - Vector(head)).normalized()
    return Vector((0, -1, 0)) if abs(d.z) > 0.7 else Vector((0, 0, 1))


def make_rig(obj, rig, offset=(0, 0, 0), spin=None):
    """Create armature `rig` for obj (armature modifier, mesh stays unparented at the origin).
    offset: the recentre offset applied to the mesh; spin: optional 4x4 matrix applied to bones (export flip)."""
    off = Vector(offset)
    M = spin or Matrix.Identity(4)
    arm = bpy.data.armatures.new(RIG_NAME)
    ao = bpy.data.objects.new(RIG_NAME, arm)
    bpy.context.scene.collection.objects.link(ao)
    bpy.context.view_layer.objects.active = ao
    for o in bpy.context.view_layer.objects:
        o.select_set(o == ao)
    bpy.ops.object.mode_set(mode='EDIT')
    ebs = {}
    for b in rig:
        eb = arm.edit_bones.new(b["name"])
        h = M @ (Vector(b["head"]) + off); t = M @ (Vector(b["tail"]) + off)
        eb.head, eb.tail = h, t
        al = M.to_3x3() @ _bone_align(b["head"], b["tail"], b.get("align"))
        eb.align_roll(al)
        eb.use_deform = True
        ebs[b["name"]] = eb
    for b in rig:
        if b.get("parent"):
            ebs[b["name"]].parent = ebs[b["parent"]]
            ebs[b["name"]].use_connect = False
    bpy.ops.object.mode_set(mode='OBJECT')
    mod = obj.modifiers.new("Armature", 'ARMATURE')
    mod.object = ao
    return ao


def make_clips(ao, clips):
    """Key the procedural CLIPS as one Action per clip (all rotation_mode XYZ). Returns the action names."""
    import math as _m
    names = []
    ao.animation_data_create()
    for pb in ao.pose.bones:
        pb.rotation_mode = 'XYZ'
    for cname, spec in clips.items():
        frames = int(spec.get("frames", 48))
        act = bpy.data.actions.new(cname)
        act.use_fake_user = True
        ao.animation_data.action = act
        chans = spec["channels"]
        step = max(1, frames // 16)
        for f in list(range(0, frames, step)) + [frames]:
            for pb in ao.pose.bones:
                pb.rotation_euler = (0, 0, 0); pb.location = (0, 0, 0)
            for (bone, ch, amp, cyc, ph) in chans:
                pb = ao.pose.bones[bone]
                v = amp * _m.sin(2 * _m.pi * cyc * f / frames + _m.radians(ph))
                axis = "xyz".index(ch[1])
                if ch[0] == "r":
                    e = list(pb.rotation_euler); e[axis] += _m.radians(v); pb.rotation_euler = e
                else:
                    l = list(pb.location); l[axis] += v; pb.location = l
            for pb in ao.pose.bones:
                pb.keyframe_insert("rotation_euler", frame=f)
                pb.keyframe_insert("location", frame=f)
        names.append(cname)
    ao.animation_data.action = bpy.data.actions.get("idle") or bpy.data.actions.get(names[0])
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = max(int(c.get("frames", 48)) for c in clips.values())
    bpy.context.scene.render.fps = FPS
    return names


def validate_rig(obj, rep, rig, clips, category):
    """Monsters must be rigged with an idle clip; every vertex weighted to real bones; clips loop (whole cycles)."""
    probs = []
    if category == "Monsters" and not rig:
        probs.append("monster without RIG (monsters are rigid-part or skinned rigs)")
    if rig:
        names = [b["name"] for b in rig]
        if len(set(names)) != len(names):
            probs.append("duplicate bone names")
        if len(names) > 40:
            probs.append(f"{len(names)} bones (max 40)")
        for b in rig:
            if b.get("parent") and b["parent"] not in names:
                probs.append(f"bone {b['name']} parent {b['parent']} missing")
            if (Vector(b["tail"]) - Vector(b["head"])).length < 0.01:
                probs.append(f"bone {b['name']} has zero length")
        groups = {g.index: g.name for g in obj.vertex_groups}
        stray = sorted({n for n in groups.values() if n not in names})
        if stray:
            probs.append(f"vertex groups without a bone: {stray}")
        unweighted = 0
        for v in obj.data.vertices:
            tot = sum(g.weight for g in v.groups if groups.get(g.group) in names)
            if abs(tot - 1.0) > 1e-3:
                unweighted += 1
        if unweighted:
            probs.append(f"{unweighted} vertices not fully weighted (weights must sum to 1)")
        if not clips or "idle" not in clips:
            probs.append("no 'idle' clip")
        for cn, c in (clips or {}).items():
            for ch in c.get("channels", []):
                bone, chan, amp, cyc, ph = ch
                if bone not in names:
                    probs.append(f"clip {cn}: unknown bone {bone}")
                if chan not in ("rx", "ry", "rz", "lx", "ly", "lz"):
                    probs.append(f"clip {cn}: bad channel {chan}")
                if abs(cyc - round(cyc)) > 1e-6 or cyc == 0:
                    probs.append(f"clip {cn}: {bone} {chan} cycles {cyc} is not a whole number (clip would not loop)")
        rep["bones"] = len(names)
        rep["clips"] = sorted((clips or {}).keys())
    rep["rig_problems"] = probs
    rep["ok_rig"] = not probs
    return rep


def export_rigged(obj, fbx_dir, glb_dir, rig, clips, offset):
    """FBX with armature + skin + one take per clip; GLB = the same rig and clips (glTF front = -Y already, unrotated)."""
    fbx = os.path.join(fbx_dir, obj.name + ".fbx")
    glb = os.path.join(glb_dir, obj.name + ".glb")
    flip = Matrix.Rotation(math.pi, 4, 'Z')
    # FBX: spin mesh AND bones 180 deg about Z (same reason as export()), rig built in the spun space
    obj.data.transform(flip)
    ao = make_rig(obj, rig, offset, spin=flip)
    try:
        make_clips(ao, clips)
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True); ao.select_set(True)
        bpy.context.view_layer.objects.active = ao
        bpy.ops.export_scene.fbx(filepath=fbx, use_selection=True, object_types={'MESH', 'ARMATURE'},
                                 apply_unit_scale=True, apply_scale_options='FBX_SCALE_ALL',
                                 axis_forward='-Z', axis_up='Y', bake_space_transform=True,   # identity mesh + rig nodes in Unity (as for the props)
                                 mesh_smooth_type='FACE', use_mesh_modifiers=False, use_armature_deform_only=True,
                                 add_leaf_bones=False, primary_bone_axis='Y', secondary_bone_axis='X',
                                 bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False,
                                 bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True,
                                 bake_anim_step=1.0, bake_anim_simplify_factor=0.0,
                                 path_mode='STRIP', use_custom_props=False)
    finally:
        _drop_rig(obj, ao)
        obj.data.transform(flip)
    # GLB: unrotated
    ao = make_rig(obj, rig, offset)
    try:
        make_clips(ao, clips)
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True); ao.select_set(True)
        bpy.context.view_layer.objects.active = ao
        bpy.ops.export_scene.gltf(filepath=glb, export_format='GLB', use_selection=True, export_apply=False,
                                  export_yup=True, export_materials='EXPORT', export_animations=True, export_skins=True)
    finally:
        _drop_rig(obj, ao)
    return fbx, glb


def _drop_rig(obj, ao):
    for m in list(obj.modifiers):
        if m.type == 'ARMATURE':
            obj.modifiers.remove(m)
    arm = ao.data
    bpy.data.objects.remove(ao)
    bpy.data.armatures.remove(arm)
    for a in list(bpy.data.actions):
        bpy.data.actions.remove(a)
