# Gaol Cell set - procedural low-poly generator (CC0 1.0, public domain).
# Run headless:  blender -b -P build_gaol_cells.py -- <output_dir>
# Writes fbx/, glb/ (visual meshes), collision/fbx/, collision/glb/ (convex collision shells)
# and collision/colliders.json (the same shells as plain numbers, glTF axes: x right, y up, z toward the front).
# Conventions: 1 unit = 1 m, flat shading, material slots Primary/Secondary/Accent, 1.5 m grid cell.
# Pivots: props and walls bottom-centre; floor tiles floor_top (walking surface at z = 0, tile extends 0.12 m below),
# matching the kit's existing dungeon wall (1.5 x 3.0 x 0.3 m) and stone floor tile (1.5 x 1.5 m).
# The geometry and collision helpers are reused unchanged from the kit's Training Yard build script (CC0).
import bpy, bmesh, math, sys, os, json
from mathutils import Vector, Matrix

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
for d in ("fbx", "glb", "collision/fbx", "collision/glb"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

SLOTS = ("Primary", "Secondary", "Accent")
WOOD = (0.42, 0.28, 0.16, 1)
DARK = (0.28, 0.19, 0.11, 1)     # dark weathered timber
IRON = (0.22, 0.22, 0.24, 1)
STEEL = (0.52, 0.54, 0.57, 1)
ROPE = (0.70, 0.60, 0.42, 1)
PALE = (0.74, 0.62, 0.44, 1)     # pale scrubbed / freshly hacked wood
STRAW = (0.80, 0.68, 0.36, 1)
BURLAP = (0.62, 0.50, 0.32, 1)
LEATHER = (0.45, 0.25, 0.14, 1)
METALS = (IRON, STEEL)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def make_mats(cols):
    mats = []
    for name, c in zip(SLOTS, cols):
        m = bpy.data.materials.new(name)
        if not m.node_tree:
            m.use_nodes = True
        b = m.node_tree.nodes.get("Principled BSDF")
        if b:
            b.inputs["Base Color"].default_value = c
            metal = c in METALS
            b.inputs["Roughness"].default_value = 0.5 if metal else 0.85
            b.inputs["Metallic"].default_value = 0.6 if metal else 0.0
        m.diffuse_color = c
        mats.append(m)
    return mats


S = {n: i for i, n in enumerate(SLOTS)}

# ---------------------------------------------------------------- geometry helpers (Blender: x right, -y front, z up)

def _faces(bm, vs, idx, slot):
    for f in idx:
        face = bm.faces.new([vs[i] for i in f])
        face.material_index = S[slot]


def box(bm, x0, x1, y0, y1, z0, z1, slot):
    c = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    vs = [bm.verts.new(p) for p in c]
    _faces(bm, vs, [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)], slot)


def prism_xz(bm, poly, y0, y1, slot):
    """Extrude an (x, z) polygon along y."""
    n = len(poly)
    a = [bm.verts.new((x, y0, z)) for x, z in poly]
    b = [bm.verts.new((x, y1, z)) for x, z in poly]
    for i in range(n):
        j = (i + 1) % n
        f = bm.faces.new([a[i], a[j], b[j], b[i]]); f.material_index = S[slot]
    f = bm.faces.new(a); f.material_index = S[slot]
    f = bm.faces.new(b[::-1]); f.material_index = S[slot]


def prism_yz(bm, poly, x0, x1, slot):
    """Extrude a (y, z) polygon along x."""
    n = len(poly)
    a = [bm.verts.new((x0, y, z)) for y, z in poly]
    b = [bm.verts.new((x1, y, z)) for y, z in poly]
    for i in range(n):
        j = (i + 1) % n
        f = bm.faces.new([a[i], a[j], b[j], b[i]]); f.material_index = S[slot]
    f = bm.faces.new(a); f.material_index = S[slot]
    f = bm.faces.new(b[::-1]); f.material_index = S[slot]


def lathe(bm, prof, seg, slot, cx=0.0, cy=0.0, rot=0.0, loop=False):
    """Revolve an (r, z) profile about a vertical axis. r == 0 ends become poles.
    loop=True closes the profile back to its start (ring / annulus shapes)."""
    rings = []
    for r, z in prof:
        if r <= 1e-9:
            rings.append([bm.verts.new((cx, cy, z))])
        else:
            rings.append([bm.verts.new((cx + r * math.cos(rot + 2 * math.pi * i / seg),
                                        cy + r * math.sin(rot + 2 * math.pi * i / seg), z)) for i in range(seg)])
    pairs = list(zip(rings, rings[1:]))
    if loop:
        pairs.append((rings[-1], rings[0]))
    for a, b in pairs:
        for i in range(seg):
            j = (i + 1) % seg
            if len(a) == 1:
                q = [a[0], b[j], b[i]]
            elif len(b) == 1:
                q = [a[i], a[j], b[0]]
            else:
                q = [a[i], a[j], b[j], b[i]]
            f = bm.faces.new(q); f.material_index = S[slot]


def cyl(bm, cx, cy, z0, z1, r, seg, slot, rot=0.0):
    lathe(bm, [(0, z0), (r, z0), (r, z1), (0, z1)], seg, slot, cx, cy, rot)


def disc_y(bm, cx, y0, y1, cz, r, seg, slot):
    """Short cylinder whose axis runs along y."""
    a = [bm.verts.new((cx + r * math.cos(2 * math.pi * i / seg), y0, cz + r * math.sin(2 * math.pi * i / seg))) for i in range(seg)]
    b = [bm.verts.new((v.co.x, y1, v.co.z)) for v in a]
    for i in range(seg):
        j = (i + 1) % seg
        f = bm.faces.new([a[i], a[j], b[j], b[i]]); f.material_index = S[slot]
    f = bm.faces.new(a); f.material_index = S[slot]
    f = bm.faces.new(b[::-1]); f.material_index = S[slot]


def obox(bm, c, u, v, n, hu, hv, hn, slot):
    """Oriented box: centre c, unit axes u, v, n with half sizes."""
    c, u, v, n = Vector(c), Vector(u).normalized(), Vector(v).normalized(), Vector(n).normalized()
    pts = [c + su * hu * u + sv * hv * v + sn * hn * n for sn in (-1, 1) for sv in (-1, 1) for su in (-1, 1)]
    vs = [bm.verts.new(p) for p in pts]
    _faces(bm, vs, [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)], slot)


def beam(bm, p0, p1, w, slot, up=(0, 0, 1)):
    """Square bar of width w from p0 to p1."""
    p0, p1 = Vector(p0), Vector(p1)
    a = (p1 - p0)
    side = a.cross(Vector(up))
    if side.length < 1e-6:
        side = a.cross(Vector((1, 0, 0)))
    n = side.cross(a)
    obox(bm, (p0 + p1) / 2, side, n, a, w / 2, w / 2, a.length / 2, slot)


def to_object(name, bm, mats):
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.triangulate(bm, faces=bm.faces, quad_method="BEAUTY", ngon_method="BEAUTY")
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    used = sorted({p.material_index for p in me.polygons})
    remap = {g: i for i, g in enumerate(used)}
    for g in used:
        me.materials.append(mats[g])
    for p in me.polygons:
        p.material_index = remap[p.material_index]
        p.use_smooth = False
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    return ob


def box_uv(obs):
    for ob in obs:
        bpy.ops.object.select_all(action="DESELECT")
        bpy.context.view_layer.objects.active = ob
        ob.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.uv.cube_project(cube_size=1.0)
        bpy.ops.object.mode_set(mode="OBJECT")


def export(paths, sel):
    bpy.ops.object.select_all(action="DESELECT")
    for o in sel:
        o.select_set(True)
    bpy.context.view_layer.objects.active = sel[0]
    bpy.ops.export_scene.fbx(
        filepath=paths[0] + ".fbx", use_selection=True, object_types={"EMPTY", "MESH"},
        apply_unit_scale=True, apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y",
        bake_space_transform=True, path_mode="STRIP", embed_textures=False, bake_anim=False,
        mesh_smooth_type="FACE", use_mesh_modifiers=True, add_leaf_bones=False)
    bpy.ops.export_scene.gltf(
        filepath=paths[1] + ".glb", export_format="GLB", use_selection=True, export_apply=True,
        export_animations=False, export_extras=False)



def circle(cy, cz, r, seg, rot=0.0):
    return [(cy + r * math.cos(rot + 2 * math.pi * i / seg), cz + r * math.sin(rot + 2 * math.pi * i / seg)) for i in range(seg)]


def cyl_x(bm, x0, x1, cy, cz, r, seg, slot, rot=0.0):
    """Cylinder whose axis runs along x."""
    prism_yz(bm, circle(cy, cz, r, seg, rot), x0, x1, slot)


def ratchet_x(bm, x0, x1, cy, cz, r_out, r_in, teeth, slot):
    """Ratchet wheel (saw-tooth outline) with its axis along x."""
    poly = []
    for i in range(teeth):
        a0 = 2 * math.pi * i / teeth
        poly.append((cy + r_in * math.cos(a0), cz + r_in * math.sin(a0)))
        a1 = a0 + 2 * math.pi / teeth * 0.85
        poly.append((cy + r_out * math.cos(a1), cz + r_out * math.sin(a1)))
    prism_yz(bm, poly, x0, x1, slot)


# ---------------------------------------------------------------- collision shells
# Every shell is closed and convex:
#   ("box", x0, x1, y0, y1, z0, z1)              axis-aligned box
#   ("lathe", profile, seg, rot, cx, cy)         revolved convex profile
#   ("hull", x0, x1, y0, y1, z0, z1)             convex hull of the visual vertices inside that box
#   ("pts", [points])                            convex hull of explicit points

def box_pts(x0, x1, y0, y1, z0, z1):
    return [Vector((x, y, z)) for x in (x0, x1) for y in (y0, y1) for z in (z0, z1)]


def beam_pts(p0, p1, w, up=(0, 0, 1)):
    p0, p1 = Vector(p0), Vector(p1)
    a = p1 - p0
    side = a.cross(Vector(up))
    if side.length < 1e-6:
        side = a.cross(Vector((1, 0, 0)))
    n = side.cross(a)
    side.normalize(); n.normalize()
    return [p + su * w / 2 * side + sn * w / 2 * n for p in (p0, p1) for su in (-1, 1) for sn in (-1, 1)]


def _hull(bm, pts):
    vs = [bm.verts.new(p) for p in pts]
    bmesh.ops.convex_hull(bm, input=vs, use_existing_faces=False)
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context="VERTS")


def collider_shell(bm, spec, verts):
    kind = spec[0]
    if kind == "box":
        box(bm, *spec[1:], "Primary")
    elif kind == "lathe":
        _, prof, seg, rot, cx, cy = spec
        lathe(bm, prof, seg, "Primary", cx, cy, rot)
    elif kind == "hull":
        x0, x1, y0, y1, z0, z1 = spec[1:]
        e = 1e-6
        _hull(bm, [p for p in verts if x0 - e <= p.x <= x1 + e and y0 - e <= p.y <= y1 + e and z0 - e <= p.z <= z1 + e])
    elif kind == "pts":
        _hull(bm, spec[1])


COLLIDERS = {}


def build(name, builder, cols, collider_specs, behaviour, pivot="bottom_center"):
    reset()
    mats = make_mats(cols)
    bm = bmesh.new()
    builder(bm)
    ob = to_object(name, bm, mats)
    raw = [v.co.copy() for v in ob.data.vertices]
    oz = -max(v.z for v in raw) if pivot == "floor_top" else -min(v.z for v in raw)
    off = Vector((-(min(v.x for v in raw) + max(v.x for v in raw)) / 2, -(min(v.y for v in raw) + max(v.y for v in raw)) / 2, oz))
    for v in ob.data.vertices:
        v.co += off
    ob.data.update()
    box_uv([ob])
    export((os.path.join(OUT, "fbx", name), os.path.join(OUT, "glb", name)), [ob])
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    cobs, defs = [], []
    for i, spec in enumerate(collider_specs):
        bm = bmesh.new()
        collider_shell(bm, spec, raw)
        bmesh.ops.translate(bm, vec=off, verts=bm.verts)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bmesh.ops.triangulate(bm, faces=bm.faces)
        me = bpy.data.meshes.new(f"{name}-col-{i:02d}")
        bm.to_mesh(me); bm.free()
        o = bpy.data.objects.new(me.name, me)
        bpy.context.scene.collection.objects.link(o)
        cobs.append(o)
        P = [(round(v.co.x, 4), round(v.co.z, 4), round(-v.co.y, 4)) for v in me.vertices]   # glTF axes
        mn = [min(p[k] for p in P) for k in range(3)]; mx = [max(p[k] for p in P) for k in range(3)]
        d = {"node": me.name, "convex": True, "bounds_center": [round((a + b) / 2, 4) for a, b in zip(mn, mx)],
             "bounds_size": [round(b - a, 4) for a, b in zip(mn, mx)]}
        if spec[0] == "box":
            d["type"] = "box"; d["center"] = d["bounds_center"]; d["size"] = d["bounds_size"]
        else:
            d["type"] = "convex_mesh"; d["vertices"] = P
        defs.append(d)
    export((os.path.join(OUT, "collision", "fbx", f"{name}-col"), os.path.join(OUT, "collision", "glb", f"{name}-col")), cobs)
    COLLIDERS[name] = {"behaviour": behaviour, "pivot": pivot, "shells": defs}



SEG = 10


def ring(bm, r_in, r_out, z0, z1, seg, slot, cx=0.0, cy=0.0, rot=0.0):
    """Closed flat band (annulus) about a vertical axis."""
    lathe(bm, [(r_in, z0), (r_out, z0), (r_out, z1), (r_in, z1)], seg, slot, cx, cy, rot, loop=True)


SEG = 10


def lathe_oval(bm, prof, seg, slot, sy, cx=0.0, cy=0.0, loop=False):
    """Lathe with its y radius scaled by sy (flattened front-to-back, e.g. a cuirass)."""
    before = set(bm.verts)
    lathe(bm, prof, seg, slot, cx, cy, 0.0, loop)
    for v in set(bm.verts) - before:
        v.co.y = cy + (v.co.y - cy) * sy


def cross_base(bm, blk, blk_h, arm, w, h, slot):
    """Timber foot: a centre block with four arms butted against its sides (no coplanar overlaps)."""
    box(bm, -blk, blk, -blk, blk, 0.0, blk_h, slot)
    box(bm, blk, arm, -w / 2, w / 2, 0.0, h, slot); box(bm, -arm, -blk, -w / 2, w / 2, 0.0, h, slot)
    box(bm, -w / 2, w / 2, blk, arm, 0.0, h, slot); box(bm, -w / 2, w / 2, -arm, -blk, 0.0, h, slot)


def braces(bm, arm, h, half_post, z_top, w, slot):
    for sx, sy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        beam(bm, (sx * (arm - 0.07), sy * (arm - 0.07), h - 0.01), (sx * half_post, sy * half_post, z_top), w, slot,
             up=(0, 1, 0) if sx else (1, 0, 0))


def bbox(bm, x0, x1, y0, y1, z0, z1, slot, bev=0.015):
    """Box with chamfered edges (one bevel segment), like the kit's own bevelled stone blocks and slabs."""
    t = bmesh.new()
    c = [(x, y, z) for z in (z0, z1) for y in (y0, y1) for x in (x0, x1)]
    vs = [t.verts.new(p) for p in c]
    for f in [(0, 2, 3, 1), (4, 5, 7, 6), (0, 1, 5, 4), (2, 6, 7, 3), (0, 4, 6, 2), (1, 3, 7, 5)]:
        t.faces.new([vs[i] for i in f])
    bev = min(bev, 0.45 * min(x1 - x0, y1 - y0, z1 - z0))
    bmesh.ops.bevel(t, geom=list(t.edges) + list(t.verts), offset=bev, offset_type="OFFSET", segments=1, profile=0.5, affect="EDGES", clamp_overlap=True)
    m = {}
    for v in t.verts:
        m[v] = bm.verts.new(v.co)
    for f in t.faces:
        nf = bm.faces.new([m[v] for v in f.verts]); nf.material_index = S[slot]
    t.free()


STONE = (0.47, 0.46, 0.44, 1)
MORTAR = (0.25, 0.24, 0.23, 1)
C = 1.5                     # grid cell
G = 0.012                   # half joint gap between slabs


def slab(bm, x0, x1, y0, y1, drop=0.0):
    bbox(bm, x0 + G, x1 - G, y0 + G, y1 - G, -0.08, -drop, "Secondary", 0.015)


def slab_frame(bm, o, drops):
    """Stone slabs round a square opening of half-size o (all joints inside the cell, so neighbours tile)."""
    h = C / 2
    slab(bm, -h, -0.20, -h, -o, drops[0]); slab(bm, -0.20, 0.35, -h, -o, drops[1]); slab(bm, 0.35, h, -h, -o, 0.0)       # front strip
    slab(bm, -h, 0.10, o, h, drops[2]); slab(bm, 0.10, h, o, h, drops[3])                                          # back strip
    slab(bm, -h, -o, -o, 0.05, drops[4]); slab(bm, -h, -o, 0.05, o, 0.0)                                           # left strip
    slab(bm, o, h, -o, -0.15, drops[5]); slab(bm, o, h, -0.15, o, 0.002)                                           # right strip


# ---------------------------------------------------------------- 1. floor drain grate (walkable stone tile with an iron grate over a shallow sump)
GR_O = 0.36

def floor_grate(bm):
    box(bm, -C / 2, C / 2, -C / 2, C / 2, -0.12, -0.045, "Primary")          # joint bed / sump floor, top -0.045
    slab_frame(bm, GR_O, (0.0, 0.004, 0.006, 0.0, 0.003, 0.0))
    o, w = GR_O - G, 0.035                                                  # iron frame inside the slab opening
    box(bm, -o, o, -o, -o + w, -0.040, -0.003, "Accent"); box(bm, -o, o, o - w, o, -0.040, -0.003, "Accent")
    box(bm, -o + 0.002, -o + w, -o + w - 0.006, o - w + 0.006, -0.038, -0.005, "Accent"); box(bm, o - w, o - 0.002, -o + w - 0.006, o - w + 0.006, -0.038, -0.005, "Accent")
    n = 6
    for k in range(n):                                                      # flat bars, run front to back
        x = -o + w + (k + 0.5) * (2 * (o - w)) / n
        box(bm, x - 0.012, x + 0.012, -o + w - 0.01, o - w + 0.01, -0.036, -0.006, "Accent")
    for y in (-0.11, 0.11):                                                 # two cross bars, slightly lower
        box(bm, -o + w - 0.01, o - w + 0.01, y - 0.014, y + 0.014, -0.042, -0.014, "Accent")


build("tile-dungeon-floor-grate", floor_grate, (MORTAR, STONE, IRON),
      [("box", -C / 2, C / 2, -C / 2, C / 2, -0.12, 0.0)],
      "solid, walkable: one box for the whole cell, top at the walking surface (z = 0); the sump under the grate is filled",
      pivot="floor_top")


# ---------------------------------------------------------------- 2. floor trapdoor (walkable stone tile with a closed plank hatch)
TD_O = 0.47

def floor_trapdoor(bm):
    box(bm, -C / 2, C / 2, -C / 2, C / 2, -0.12, -0.05, "Secondary")        # stone bed under slabs and hatch
    slab_frame(bm, TD_O, (0.003, 0.0, 0.0, 0.005, 0.0, 0.004))
    o, w = TD_O - G, 0.03                                                   # iron curb round the hatch
    box(bm, -o, o, -o, -o + w, -0.045, -0.002, "Accent"); box(bm, -o, o, o - w, o, -0.045, -0.002, "Accent")
    box(bm, -o + 0.002, -o + w, -o + w - 0.006, o - w + 0.006, -0.043, -0.004, "Accent"); box(bm, o - w, o - 0.002, -o + w - 0.006, o - w + 0.006, -0.043, -0.004, "Accent")
    i, n, gap = o - w - 0.004, 5, 0.008                                     # five planks, running front to back
    pw = (2 * i - (n - 1) * gap) / n
    for k in range(n):
        x0 = -i + k * (pw + gap)
        box(bm, x0, x0 + pw, -i, i, -0.047, -0.006 - 0.002 * (k % 2), "Primary")
    for y in (-0.24, 0.24):                                                 # two iron straps across the planks
        box(bm, -i + 0.02, i - 0.02, y - 0.03, y + 0.03, -0.012, -0.001, "Accent")
    for x in (-0.25, 0.25):                                                 # hinge knuckles at the back
        cyl_x(bm, x - 0.06, x + 0.06, i - 0.005, -0.024, 0.018, 6, "Accent")
    ring(bm, 0.036, 0.052, -0.010, -0.003, 8, "Accent", cx=0.0, cy=-0.30)     # pull ring lying flat at the front
    box(bm, -0.014, 0.014, -0.268, -0.246, -0.014, -0.0005, "Accent")          # ring staple


build("tile-dungeon-floor-trapdoor", floor_trapdoor, (WOOD, STONE, IRON),
      [("box", -C / 2, C / 2, -C / 2, C / 2, -0.12, 0.0)],
      "solid, walkable: one box for the whole cell, top at the walking surface (z = 0); the hatch is closed and does not open",
      pivot="floor_top")


# ---------------------------------------------------------------- 3. cell-bar wall (1.5 m wall-module with stone jambs, sill, lintel and iron bars)
WL, WH, WT = 1.5, 3.0, 0.34                                              # same module size as the kit stone wall
JW = 0.20                                                                   # jamb width
BARS = 9

def cell_bars_wall(bm):
    """Courses, gaps and cap match the kit stone wall: 8 block courses of 0.36 m (0.3 m thick) and a 0.12 m cap course 0.34 m thick."""
    h, T, rh, CAP = WL / 2, 0.30, 0.36, 0.12
    for sx in (-1, 1):                                                      # jamb cores (mortar) + coursed stone blocks
        xa, xb = sorted((sx * h, sx * (h - JW)))
        box(bm, xa + 0.02, xb - 0.02, -T / 2 + 0.03, T / 2 - 0.03, 0.004, WH - CAP - 0.004, "Primary")
        for k in range(8):
            z0 = k * rh + (0.009 if k else 0.0); z1 = (k + 1) * rh - 0.009
            bbox(bm, xa + (0.0 if sx < 0 else 0.009), xb - (0.0 if sx > 0 else 0.009), -T / 2, T / 2, z0, z1, "Secondary", 0.02)
    bbox(bm, -h, h, -WT / 2, WT / 2, WH - CAP, WH, "Secondary", 0.015)       # cap course, full width (kit wall: same size)
    ix = h - JW
    bbox(bm, -ix - 0.03, ix + 0.03, -0.13, 0.13, 0.002, 0.20, "Secondary", 0.015)   # sill (runs into the jamb cores)
    bbox(bm, -ix - 0.03, ix + 0.03, -0.145, 0.145, 2.52, WH - CAP - 0.006, "Secondary", 0.015)   # lintel under the cap
    sp = 2 * ix / (BARS + 1)
    for k in range(BARS):                                                   # round iron bars set into sill and lintel
        x = -ix + (k + 1) * sp
        cyl(bm, x, 0.0, 0.12, 2.60, 0.022, 6, "Accent", rot=math.pi / 6)
    for z in (0.95, 1.95):                                                  # flat cross straps, ends buried in the jambs
        box(bm, -ix - 0.05, ix + 0.05, -0.034, 0.034, z - 0.03, z + 0.03, "Accent")


build("wall-dungeon-cell-bars", cell_bars_wall, (MORTAR, STONE, IRON),
      [("hull", -0.76, -0.54, -0.2, 0.2, -0.1, 2.877),                      # left jamb
       ("hull", 0.54, 0.76, -0.2, 0.2, -0.1, 2.877),                        # right jamb
       ("box", -0.55, 0.55, -0.13, 0.13, 0.0, 0.20),                        # sill
       ("box", -0.55, 0.55, -0.145, 0.145, 2.52, 2.874),                    # lintel
       ("box", -0.75, 0.75, -0.17, 0.17, 2.88, 3.0),                        # cap course
       ("box", -0.55, 0.55, -0.035, 0.035, 0.20, 2.52)],                    # bars treated as one thin solid panel
      "solid, blocking: jambs, sill, lintel, cap course, and the bars as one thin solid panel (characters cannot pass; whether rays or projectiles pass the gaps is up to your setup)")


# ---------------------------------------------------------------- 4. foot stocks (sill on two feet, two uprights, notched boards, iron hasp)
NOTCH_X, NOTCH_Z, NOTCH_R = 0.20, 0.52, 0.07

def notched(x0, x1, z0, z1, top, seg=6):
    """(x, z) outline of a board with two half-round leg notches on its top (top=True) or bottom edge."""
    if top:
        pts = [(x0, z0), (x1, z0), (x1, z1)]
        for cx in (NOTCH_X, -NOTCH_X):
            pts += [(cx + NOTCH_R * math.cos(-math.pi * i / seg), z1 + NOTCH_R * math.sin(-math.pi * i / seg)) for i in range(seg + 1)]
        pts.append((x0, z1))
    else:
        pts = [(x1, z1), (x0, z1), (x0, z0)]
        for cx in (-NOTCH_X, NOTCH_X):
            pts += [(cx - NOTCH_R * math.cos(-math.pi * i / seg), z0 - NOTCH_R * math.sin(-math.pi * i / seg)) for i in range(seg + 1)]
        pts.append((x1, z0))
    return pts


def stocks(bm):
    for sx in (-1, 1):
        box(bm, sx * 0.49 if sx > 0 else -0.65, 0.65 if sx > 0 else -0.49, -0.30, 0.30, 0.0, 0.10, "Primary")   # feet
        box(bm, sx * 0.52 if sx > 0 else -0.62, 0.62 if sx > 0 else -0.52, -0.05, 0.05, 0.04, 0.99, "Primary")  # uprights
        beam(bm, (sx * 0.57, -0.27, 0.085), (sx * 0.57, -0.045, 0.40), 0.05, "Primary", up=(1, 0, 0))        # front braces
        beam(bm, (sx * 0.57, 0.27, 0.085), (sx * 0.57, 0.045, 0.40), 0.05, "Primary", up=(1, 0, 0))          # back braces
        box(bm, sx * 0.515 if sx > 0 else -0.625, 0.625 if sx > 0 else -0.515, -0.055, 0.055, 0.93, 0.955, "Accent")  # iron cap bands
    bbox(bm, -0.70, 0.70, -0.08, 0.08, 0.06, 0.18, "Primary", 0.012)        # sill
    prism_xz(bm, notched(-0.56, 0.56, 0.30, NOTCH_Z, True), -0.04, 0.04, "Secondary")          # lower board
    prism_xz(bm, notched(-0.56, 0.56, NOTCH_Z + 0.006, 0.72, False), -0.04, 0.04, "Secondary")  # upper board (6 mm gap)
    bbox(bm, -0.68, 0.68, -0.06, 0.06, 0.985, 1.06, "Primary", 0.012)       # cap rail
    box(bm, -0.035, 0.035, -0.052, -0.036, 0.44, 0.66, "Accent")            # hasp across the join
    box(bm, -0.03, 0.03, -0.085, -0.050, 0.47, 0.53, "Accent")              # padlock body
    box(bm, 0.40, 0.52, -0.050, -0.036, 0.62, 0.66, "Accent")               # strap hinge on the upper board


build("prop-stocks-wood", stocks, (WOOD, DARK, IRON),
      [("hull", -1, 1, -1, 1, -0.01, 0.101),                               # feet
       ("hull", -1, 1, -0.1, 0.1, 0.039, 1.07),                            # sill, uprights, boards, cap rail, iron
       ("pts", beam_pts((-0.57, -0.27, 0.085), (-0.57, -0.045, 0.40), 0.05, (1, 0, 0)) + beam_pts((-0.57, 0.27, 0.085), (-0.57, 0.045, 0.40), 0.05, (1, 0, 0))),
       ("pts", beam_pts((0.57, -0.27, 0.085), (0.57, -0.045, 0.40), 0.05, (1, 0, 0)) + beam_pts((0.57, 0.27, 0.085), (0.57, 0.045, 0.40), 0.05, (1, 0, 0)))],
      "solid, blocking (feet, sill, uprights, boards and cap rail); the leg notches are closed by the collision")

with open(os.path.join(OUT, "collision", "colliders.json"), "w") as f:
    json.dump({"axes": "glTF: x right, y up, z toward the prop front; metres; pivot bottom-centre (tiles: floor_top, walking surface at y = 0)",
               "note": "every shell is closed and convex; box shells also carry center/size",
               "colliders": COLLIDERS}, f, indent=1)
print("built", len(COLLIDERS), "assets ->", OUT)
