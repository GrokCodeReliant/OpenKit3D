# Training Yard prop set - procedural low-poly generator (CC0 1.0, public domain).
# Run headless:  blender -b -P build_training_yard.py -- <output_dir>
# Writes fbx/, glb/ (visual meshes), collision/fbx/, collision/glb/ (convex collision shells)
# and collision/colliders.json (the same shells as plain numbers, glTF axes: x right, y up, z toward the front).
# Conventions: 1 unit = 1 m, bottom-centre pivot, flat shading, material slots Primary/Secondary/Accent.
# The geometry and collision helpers are reused from the kit's Farmhouse & Market Equipment build script, which in
# turn reused the Hauling & Lifting build script (both CC0). Only an oval lathe helper and the cross base are new.
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


def build(name, builder, cols, collider_specs, behaviour):
    reset()
    mats = make_mats(cols)
    bm = bmesh.new()
    builder(bm)
    ob = to_object(name, bm, mats)
    raw = [v.co.copy() for v in ob.data.vertices]
    off = Vector((-(min(v.x for v in raw) + max(v.x for v in raw)) / 2, -(min(v.y for v in raw) + max(v.y for v in raw)) / 2, -min(v.z for v in raw)))
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
    COLLIDERS[name] = {"behaviour": behaviour, "shells": defs}



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


# ---------------------------------------------------------------- 1. pell post (heavy practice post on a braced cross foot, fresh hack scars)
PELL_H = 1.80


def pell(bm):
    cross_base(bm, 0.15, 0.16, 0.46, 0.12, 0.12, "Secondary")
    braces(bm, 0.46, 0.12, 0.10, 0.56, 0.06, "Secondary")
    box(bm, -0.10, 0.10, -0.10, 0.10, 0.12, PELL_H - 0.06, "Primary")                                   # post
    lathe(bm, [(0, PELL_H - 0.06), (0.1414, PELL_H - 0.06), (0.075, PELL_H), (0, PELL_H)], 4, "Primary", rot=math.pi / 4)   # chamfered top
    for k, (z, a) in enumerate(((0.92, 18), (1.06, -22), (1.20, 14), (1.34, -16), (1.48, 20))):           # hack scars, front face
        t = math.radians(a)
        obox(bm, (0.01 * (k % 2) - 0.005, -0.104, z), (math.cos(t), 0, math.sin(t)), (0, 1, 0), (-math.sin(t), 0, math.cos(t)), 0.075, 0.006, 0.013, "Accent")
    for z, a in ((1.00, -20), (1.27, 16)):                                                                # hack scars, right face
        t = math.radians(a)
        obox(bm, (0.104, 0.0, z), (0, math.cos(t), math.sin(t)), (1, 0, 0), (0, -math.sin(t), math.cos(t)), 0.075, 0.006, 0.013, "Accent")


build("prop-pell-post-wood", pell, (WOOD, DARK, PALE),
      [("hull", -1, 1, -1, 1, -1, 0.60),                                  # cross foot and braces (with the foot of the post)
       ("box", -0.11, 0.11, -0.11, 0.11, 0.12, PELL_H)],                  # post, cap and scars
      "solid, blocking (braced cross foot; post up to 1.80 m)")

# ---------------------------------------------------------------- 2. quintain (pivot post, swing arm with a shield board and a hanging sandbag)
QZ = 1.62     # post top / pivot cap base


def quintain(bm):
    cross_base(bm, 0.14, 0.16, 0.48, 0.12, 0.12, "Primary")
    braces(bm, 0.48, 0.12, 0.08, 0.58, 0.06, "Primary")
    box(bm, -0.08, 0.08, -0.08, 0.08, 0.12, QZ, "Primary")                                                # post
    cyl(bm, 0, 0, QZ - 0.03, QZ + 0.08, 0.065, 8, "Secondary")                                            # iron pivot cap
    box(bm, -0.66, 0.66, -0.045, 0.045, QZ + 0.08, QZ + 0.18, "Primary")                                  # swing arm
    cyl(bm, 0, 0, QZ + 0.18, QZ + 0.24, 0.025, 6, "Secondary")                                            # pivot pin head
    shield = [(-0.67, QZ), (-0.33, QZ), (-0.33, QZ - 0.22), (-0.40, QZ - 0.36), (-0.50, QZ - 0.45), (-0.60, QZ - 0.36), (-0.67, QZ - 0.22)]
    prism_xz(bm, shield, -0.02, 0.02, "Primary")                                                          # shield board
    for x in (-0.60, -0.40):
        box(bm, x - 0.018, x + 0.018, -0.03, 0.03, QZ - 0.03, QZ + 0.09, "Secondary")                       # hanging straps
    disc_y(bm, -0.50, -0.065, -0.015, QZ - 0.20, 0.055, 8, "Secondary")                                    # shield boss (front)
    beam(bm, (0.52, 0, QZ + 0.09), (0.52, 0, QZ - 0.25), 0.02, "Secondary")                               # chain
    lathe(bm, [(0, QZ - 0.64), (0.10, QZ - 0.62), (0.15, QZ - 0.52), (0.15, QZ - 0.40), (0.10, QZ - 0.30), (0.04, QZ - 0.24), (0, QZ - 0.22)], SEG, "Accent", cx=0.52)   # sandbag


build("prop-quintain-wood", quintain, (WOOD, IRON, BURLAP),
      [("hull", -1, 1, -1, 1, -1, 0.62),                                  # cross foot and braces
       ("box", -0.08, 0.08, -0.08, 0.08, 0.12, QZ - 0.03),                 # post
       ("hull", -0.70, 0.70, -0.1, 0.1, QZ - 0.031, QZ + 0.25),           # pivot cap, swing arm, pin, strap tops, chain top
       ("hull", -0.70, -0.30, -0.1, 0.1, QZ - 0.46, QZ + 0.0),            # shield board, boss, strap feet
       ("hull", 0.35, 0.70, -0.2, 0.2, QZ - 0.65, QZ + 0.0)],             # chain and sandbag
      "post, swing arm, shield board and sandbag; open under the arm on both sides of the post")

# ---------------------------------------------------------------- 3. straw training dummy (bound straw body and head on a post, arm bar)


def dummy(bm):
    cross_base(bm, 0.12, 0.14, 0.40, 0.10, 0.10, "Primary")
    braces(bm, 0.40, 0.10, 0.05, 0.50, 0.05, "Primary")
    box(bm, -0.05, 0.05, -0.05, 0.05, 0.10, 1.42, "Primary")                                              # post
    lathe(bm, [(0, 0.72), (0.14, 0.74), (0.20, 0.86), (0.22, 1.04), (0.20, 1.20), (0.15, 1.30), (0, 1.32)], 8, "Accent")   # straw body
    for z, r in ((0.85, 0.198), (1.03, 0.22), (1.19, 0.20)):                                              # rope bindings
        ring(bm, r - 0.03, r + 0.014, z - 0.014, z + 0.014, 8, "Secondary")
    box(bm, -0.44, 0.44, -0.035, 0.035, 1.12, 1.19, "Primary")                                            # arm bar
    for sx in (-1, 1):
        cyl_x(bm, sx * 0.21 if sx > 0 else -0.42, 0.42 if sx > 0 else -0.21, 0, 1.155, 0.07, 6, "Accent")  # straw arm bundles
        cyl_x(bm, sx * 0.35 if sx > 0 else -0.38, 0.38 if sx > 0 else -0.35, 0, 1.155, 0.078, 6, "Secondary")   # rope ties
    ring(bm, 0.04, 0.072, 1.32, 1.37, 6, "Secondary")                                                     # neck tie
    lathe(bm, [(0, 1.34), (0.08, 1.35), (0.12, 1.42), (0.125, 1.50), (0.10, 1.58), (0.05, 1.63), (0, 1.64)], 8, "Accent")   # sack head
    lathe(bm, [(0, 1.61), (0.035, 1.61), (0, 1.71)], 6, "Accent")                                         # tied top knot


build("prop-training-dummy-straw", dummy, (WOOD, ROPE, STRAW),
      [("hull", -1, 1, -1, 1, -1, 0.52),                                  # cross foot and braces
       ("box", -0.05, 0.05, -0.05, 0.05, 0.10, 0.74),                      # post below the body
       ("hull", -0.24, 0.24, -0.3, 0.3, 0.71, 1.335),                     # body with bindings
       ("box", -0.44, 0.44, -0.08, 0.08, 1.075, 1.235),                    # arm bar with straw arms
       ("hull", -0.13, 0.13, -0.13, 0.13, 1.32, 1.72)],                    # neck tie, head and top knot
      "solid, blocking (cross foot, post, body, arm bar and head)")

# ---------------------------------------------------------------- 4. armour stand (cross foot, post, shoulder bar, cuirass with faulds and belt, pauldrons, helm)
AS_SY = 0.70


def armor_stand(bm):
    cross_base(bm, 0.10, 0.12, 0.34, 0.09, 0.08, "Primary")
    braces(bm, 0.34, 0.08, 0.035, 0.36, 0.04, "Primary")
    box(bm, -0.035, 0.035, -0.035, 0.035, 0.08, 1.50, "Primary")                                         # post
    box(bm, -0.26, 0.26, -0.03, 0.03, 1.34, 1.40, "Primary")                                             # shoulder bar
    lathe_oval(bm, [(0, 0.92), (0.17, 0.92), (0.16, 1.00), (0.20, 1.16), (0.22, 1.26), (0.19, 1.35), (0.10, 1.42), (0, 1.43)], 10, "Secondary", AS_SY)   # cuirass
    lathe_oval(bm, [(0.14, 0.78), (0.20, 0.78), (0.18, 0.935), (0.145, 0.935)], 10, "Secondary", AS_SY, loop=True)   # faulds (skirt lames)
    lathe_oval(bm, [(0.155, 0.905), (0.188, 0.905), (0.188, 0.955), (0.155, 0.955)], 10, "Accent", AS_SY, loop=True)  # leather belt
    box(bm, -0.03, 0.03, -0.142, -0.124, 0.900, 0.960, "Secondary")                                     # buckle
    for sx in (-1, 1):
        lathe(bm, [(0, 1.27), (0.095, 1.27), (0.09, 1.35), (0.055, 1.41), (0, 1.43)], 6, "Secondary", cx=sx * 0.22)   # pauldrons
        box(bm, sx * 0.13 - 0.02, sx * 0.13 + 0.02, -0.14, 0.14, 1.36, 1.385, "Accent")                   # shoulder straps
    lathe(bm, [(0, 1.48), (0.11, 1.48), (0.12, 1.57), (0.10, 1.65), (0.05, 1.70), (0, 1.71)], 8, "Secondary")   # helm
    ring(bm, 0.105, 0.135, 1.474, 1.50, 8, "Secondary")                                                   # helm brim


build("prop-armor-stand-wood", armor_stand, (WOOD, STEEL, LEATHER),
      [("hull", -1, 1, -1, 1, -1, 0.40),                                  # cross foot and braces
       ("box", -0.035, 0.035, -0.035, 0.035, 0.08, 0.79),                  # post below the faulds
       ("hull", -0.35, 0.35, -0.3, 0.3, 0.77, 1.435),                      # cuirass, faulds, belt, pauldrons, shoulder bar
       ("hull", -0.15, 0.15, -0.15, 0.15, 1.42, 1.72)],                    # post top, helm and brim
      "solid, blocking (cross foot, post, armour body and helm)")

with open(os.path.join(OUT, "collision", "colliders.json"), "w") as f:
    json.dump({"axes": "glTF: x right, y up, z toward the prop front; metres; pivot bottom-centre",
               "note": "every shell is closed and convex; box shells also carry center/size",
               "colliders": COLLIDERS}, f, indent=1)
print("built", len(COLLIDERS), "assets ->", OUT)
