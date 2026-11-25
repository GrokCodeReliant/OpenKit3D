# Hauling & Lifting prop set - procedural low-poly generator (CC0 1.0, public domain).
# Run headless:  blender -b -P build_hauling_lifting.py -- <output_dir>
# Writes fbx/, glb/ (visual meshes), collision/fbx/, collision/glb/ (convex collision shells)
# and collision/colliders.json (the same shells as plain numbers, glTF axes: x right, y up, z toward the front).
# Conventions: 1 unit = 1 m, bottom-centre pivot, flat shading, material slots Primary/Secondary/Accent.
import bpy, bmesh, math, sys, os, json
from mathutils import Vector, Matrix

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
for d in ("fbx", "glb", "collision/fbx", "collision/glb"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

SLOTS = ("Primary", "Secondary", "Accent")
WOOD = (0.42, 0.28, 0.16, 1)
IRON = (0.22, 0.22, 0.24, 1)
ROPE = (0.70, 0.60, 0.42, 1)


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
            b.inputs["Roughness"].default_value = 0.5 if name == "Secondary" else 0.85
            b.inputs["Metallic"].default_value = 0.6 if name == "Secondary" else 0.0
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


OCT = math.pi / 8

# ---------------------------------------------------------------- 1. two-man windlass (horizontal rope drum, ratchet, two cranks)
CRANK_X = 0.52


def windlass(bm):
    for sx in (-1, 1):
        x = 0.42 * sx
        box(bm, x - 0.05, x + 0.05, -0.40, 0.40, 0.0, 0.09, "Primary")              # side sill
        beam(bm, (x, -0.30, 0.06), (x, -0.03, 0.80), 0.09, "Primary")               # A-frame legs
        beam(bm, (x, 0.30, 0.06), (x, 0.03, 0.80), 0.09, "Primary")
        box(bm, x - 0.06, x + 0.06, -0.08, 0.08, 0.72, 0.88, "Secondary")           # iron bearing block
        # crank: arm (down on +x, up on -x so the two men push in turn) and a wooden grip
        z1 = 0.81 - sx * 0.30
        beam(bm, (sx * CRANK_X, 0, 0.81), (sx * CRANK_X, 0, z1), 0.04, "Secondary")
        cyl_x(bm, min(sx * CRANK_X, sx * 0.62), max(sx * CRANK_X, sx * 0.62), 0, z1, 0.025, 6, "Primary")
    for y in (-0.30, 0.30):
        box(bm, -0.47, 0.47, y - 0.045, y + 0.045, 0.0, 0.08, "Primary")           # cross sills
    cyl_x(bm, -0.54, 0.54, 0, 0.81, 0.03, 6, "Secondary")                            # iron axle
    cyl_x(bm, -0.34, 0.34, 0, 0.81, 0.13, 10, "Primary")                             # drum
    for x0 in (-0.36, 0.32):
        cyl_x(bm, x0, x0 + 0.04, 0, 0.81, 0.18, 10, "Primary")                        # drum flanges
    cyl_x(bm, -0.30, 0.30, 0, 0.81, 0.155, 10, "Accent")                             # rope turns
    ratchet_x(bm, -0.40, -0.37, 0, 0.81, 0.17, 0.13, 10, "Secondary")                # ratchet wheel
    beam(bm, (-0.385, 0.06, 1.02), (-0.385, 0.03, 0.955), 0.03, "Secondary")         # pawl
    beam(bm, (0.08, -0.13, 0.75), (0.08, -0.33, 0.07), 0.035, "Accent")             # rope lead to the load
    box(bm, 0.03, 0.13, -0.40, -0.30, 0.0, 0.07, "Secondary")                        # iron load ring / shackle


build("prop-windlass-wood", windlass, (WOOD, IRON, ROPE),
      [("box", -0.47, 0.47, -0.40, 0.40, 0.0, 1.03),
       ("hull", 0.47, 1.0, -1, 1, -1, 2), ("hull", -1.0, -0.47, -1, 1, -1, 2)],
      "solid, blocking (frame, drum and cranks)")

# ---------------------------------------------------------------- 2. capstan (vertical drum, whelps, four push bars)
BAR_R = 0.70


def capstan(bm):
    lathe(bm, [(0, 0.0), (0.46, 0.0), (0.46, 0.08), (0.42, 0.10), (0, 0.10)], 8, "Primary", rot=OCT)          # base
    lathe(bm, [(0, 0.10), (0.30, 0.10), (0.25, 0.30), (0.23, 0.50), (0.27, 0.70), (0.30, 0.74), (0, 0.74)], 8, "Primary", rot=OCT)
    for z0 in (0.10, 0.69):
        lathe(bm, [(0.285, z0), (0.315, z0), (0.315, z0 + 0.05), (0.285, z0 + 0.05)], 8, "Secondary", rot=OCT, loop=True)
    lathe(bm, [(0, 0.74), (0.34, 0.74), (0.34, 0.90), (0.30, 0.93), (0, 0.93)], 8, "Primary", rot=OCT)        # drumhead
    lathe(bm, [(0, 0.93), (0.13, 0.93), (0.13, 0.96), (0, 0.98)], 8, "Secondary", rot=OCT)                     # iron cap
    for k in range(8):                                                                                          # whelps
        d = Vector((math.cos(k * math.pi / 4), math.sin(k * math.pi / 4), 0))
        beam(bm, d * 0.265 + Vector((0, 0, 0.16)), d * 0.245 + Vector((0, 0, 0.66)), 0.05, "Primary")
    for k in range(4):                                                                                          # push bars
        d = Vector((math.cos(k * math.pi / 2), math.sin(k * math.pi / 2), 0))
        beam(bm, d * 0.15 + Vector((0, 0, 0.83)), d * BAR_R + Vector((0, 0, 0.83)), 0.06, "Primary")
    lathe(bm, [(0.215, 0.36), (0.262, 0.36), (0.262, 0.46), (0.215, 0.46)], 10, "Accent", loop=True)          # rope turns
    beam(bm, (0, -0.24, 0.40), (0, -0.66, 0.04), 0.05, "Accent")                                               # rope lead


build("prop-capstan-wood", capstan, (WOOD, IRON, ROPE),
      [("lathe", [(0, 0.0), (0.46, 0.0), (0.46, 0.10), (0, 0.10)], 8, OCT, 0, 0),
       ("lathe", [(0, 0.10), (0.33, 0.10), (0.33, 0.74), (0, 0.74)], 8, OCT, 0, 0),
       ("lathe", [(0, 0.74), (0.34, 0.74), (0.34, 0.98), (0, 0.98)], 8, OCT, 0, 0),
       ("box", -BAR_R, BAR_R, -0.03, 0.03, 0.80, 0.86), ("box", -0.03, 0.03, -BAR_R, BAR_R, 0.80, 0.86),
       ("pts", beam_pts((0, -0.24, 0.40), (0, -0.66, 0.04), 0.06))],
      "solid, blocking (drum, base and push bars)")

# ---------------------------------------------------------------- 3. jib crane (post, counterweighted arm, sheave, hook, post winch)
def jib(bm):
    box(bm, -0.56, 0.56, -0.07, 0.07, 0.0, 0.14, "Primary")                    # cross-foot sills
    box(bm, -0.07, 0.07, -0.56, 0.56, 0.0, 0.14, "Primary")
    box(bm, -0.09, 0.09, -0.09, 0.09, 0.14, 2.78, "Primary")                   # post
    box(bm, -0.11, 0.11, -0.11, 0.11, 2.78, 2.84, "Secondary")                 # post cap
    for k in range(4):                                                         # foot braces
        d = Vector((math.cos(k * math.pi / 2), math.sin(k * math.pi / 2), 0))
        beam(bm, d * 0.48 + Vector((0, 0, 0.16)), d * 0.09 + Vector((0, 0, 0.78)), 0.07, "Primary")
    box(bm, -0.12, 0.12, -0.12, 0.12, 2.40, 2.50, "Secondary")                 # iron slewing collar
    box(bm, -0.07, 0.07, -0.66, 0.66, 2.50, 2.64, "Primary")                   # jib arm
    beam(bm, (0, -0.09, 1.95), (0, -0.50, 2.50), 0.07, "Primary")              # knee braces
    beam(bm, (0, 0.09, 1.95), (0, 0.50, 2.50), 0.07, "Primary")
    box(bm, -0.15, 0.15, 0.46, 0.70, 2.20, 2.50, "Secondary")                  # counterweight
    cyl_x(bm, -0.03, 0.03, -0.58, 2.44, 0.075, 10, "Secondary")                # sheave
    box(bm, -0.045, -0.03, -0.62, -0.54, 2.40, 2.50, "Secondary")              # sheave cheeks
    box(bm, 0.03, 0.045, -0.62, -0.54, 2.40, 2.50, "Secondary")
    beam(bm, (0, -0.655, 2.44), (0, -0.655, 1.62), 0.025, "Accent")            # rope fall
    box(bm, -0.06, 0.06, -0.70, -0.61, 1.50, 1.62, "Secondary")                # hook block
    beam(bm, (0, -0.655, 1.50), (0, -0.655, 1.37), 0.03, "Secondary")          # hook
    beam(bm, (0, -0.67, 1.37), (0, -0.625, 1.37), 0.03, "Secondary")
    beam(bm, (0, -0.625, 1.355), (0, -0.625, 1.43), 0.03, "Secondary")
    beam(bm, (0, -0.505, 2.44), (0, -0.11, 2.30), 0.025, "Accent")             # rope back to the post
    beam(bm, (0, -0.11, 2.30), (0, -0.11, 1.10), 0.025, "Accent")              # rope down the post
    for x0 in (-0.15, 0.12):                                                   # winch cheeks on the post
        box(bm, x0, x0 + 0.03, -0.24, -0.09, 0.94, 1.10, "Secondary")
    cyl_x(bm, -0.15, 0.22, -0.17, 1.02, 0.025, 6, "Secondary")                 # winch axle
    cyl_x(bm, -0.11, 0.11, -0.17, 1.02, 0.07, 8, "Accent")                     # rope turns on the winch
    beam(bm, (0.22, -0.17, 1.02), (0.22, -0.17, 0.82), 0.035, "Secondary")     # winch crank
    cyl_x(bm, 0.22, 0.32, -0.17, 0.82, 0.02, 6, "Primary")


build("prop-jib-crane-wood", jib, (WOOD, IRON, ROPE),
      [("box", -0.56, 0.56, -0.07, 0.07, 0.0, 0.14), ("box", -0.07, 0.07, -0.56, 0.56, 0.0, 0.14),
       ("hull", -1, 1, -1, 1, 0.14, 0.86),                    # foot braces (space between them filled)
       ("box", -0.09, 0.09, -0.125, 0.09, 0.14, 2.40),        # post, incl. the rope running down its front
       ("hull", -1, 1, -0.30, 0.0, 0.78, 1.13),               # post winch
       ("hull", -1, 1, -1, 1, 1.90, 2.85),                    # arm, braces, counterweight, sheave
       ("box", -0.06, 0.06, -0.70, -0.61, 1.34, 2.44)],       # rope fall, hook block and hook
      "solid, blocking (base, post, winch, hook; the arm assembly sits above 1.9 m)")

# ---------------------------------------------------------------- 4. four-leg shaft hoist frame (open centre over a hatch or shaft)
FOOT, APEX_R, LEG_Z0, LEG_Z1 = 0.60, 0.07, 0.03, 2.45
SPREAD_Z, CLEAT_Z = 0.45, 1.40


def leg_at(sx, sy, z):
    t = (z - LEG_Z0) / (LEG_Z1 - LEG_Z0)
    r = FOOT + (APEX_R - FOOT) * t
    return Vector((sx * r, sy * r, z))


LEGS = [(sx, sy) for sx in (-1, 1) for sy in (-1, 1)]
HAUL = ((0.08, 0.0, 2.20), tuple(leg_at(1, 1, CLEAT_Z) - Vector((0.04, 0.04, 0))))


def hoist(bm):
    for sx, sy in LEGS:
        beam(bm, leg_at(sx, sy, LEG_Z0), leg_at(sx, sy, LEG_Z1), 0.10, "Primary")
        fx, fy = sx * FOOT, sy * FOOT
        box(bm, fx - 0.09, fx + 0.09, fy - 0.09, fy + 0.09, 0.0, 0.06, "Secondary")   # iron foot shoes
    for (ax, ay), (bx, by) in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))):
        beam(bm, leg_at(ax, ay, SPREAD_Z), leg_at(bx, by, SPREAD_Z), 0.06, "Primary")   # spreader bars
    box(bm, -0.14, 0.14, -0.14, 0.14, 2.40, 2.56, "Secondary")                       # iron head
    beam(bm, (0, 0, 2.40), (0, 0, 2.30), 0.03, "Secondary")                          # shackle
    box(bm, -0.08, 0.08, -0.06, 0.06, 2.06, 2.30, "Secondary")                       # upper block
    for x in (-0.045, 0.045):
        beam(bm, (x, 0, 2.06), (x, 0, 1.64), 0.03, "Accent")                         # two rope falls
    box(bm, -0.08, 0.08, -0.06, 0.06, 1.50, 1.64, "Secondary")                       # lower block
    beam(bm, (0, 0, 1.50), (0, 0, 1.40), 0.04, "Secondary")                          # hook
    beam(bm, (-0.02, 0, 1.40), (0.09, 0, 1.40), 0.04, "Secondary")
    beam(bm, (0.09, 0, 1.38), (0.09, 0, 1.47), 0.04, "Secondary")
    beam(bm, HAUL[0], HAUL[1], 0.022, "Accent")                                      # hauling line to the cleat
    c = leg_at(1, 1, CLEAT_Z)
    box(bm, c.x - 0.07, c.x + 0.07, c.y - 0.07, c.y + 0.07, CLEAT_Z - 0.05, CLEAT_Z + 0.05, "Secondary")   # cleat


def hoist_cols():
    out = []
    for sx, sy in LEGS:
        p = beam_pts(leg_at(sx, sy, LEG_Z0), leg_at(sx, sy, LEG_Z1), 0.10)
        fx, fy = sx * FOOT, sy * FOOT
        p += box_pts(fx - 0.09, fx + 0.09, fy - 0.09, fy + 0.09, 0.0, 0.06)
        if (sx, sy) == (1, 1):
            c = leg_at(1, 1, CLEAT_Z)
            p += box_pts(c.x - 0.07, c.x + 0.07, c.y - 0.07, c.y + 0.07, CLEAT_Z - 0.05, CLEAT_Z + 0.05)
        out.append(("pts", p))
    for (ax, ay), (bx, by) in (((-1, -1), (1, -1)), ((1, -1), (1, 1)), ((1, 1), (-1, 1)), ((-1, 1), (-1, -1))):
        out.append(("pts", beam_pts(leg_at(ax, ay, SPREAD_Z), leg_at(bx, by, SPREAD_Z), 0.06)))
    out.append(("hull", -0.15, 0.15, -0.15, 0.15, 1.36, 2.60))       # head, blocks, falls and hook
    out.append(("pts", beam_pts(HAUL[0], HAUL[1], 0.03)))
    return out


build("prop-shaft-hoist-frame-wood", hoist, (WOOD, IRON, ROPE), hoist_cols(),
      "legs, spreader bars, cleat and the hanging tackle block; the centre below the hook is left open (for a hatch or shaft placed under it)")

with open(os.path.join(OUT, "collision", "colliders.json"), "w") as f:
    json.dump({"axes": "glTF: x right, y up, z toward the prop front; metres; pivot bottom-centre",
               "note": "every shell is closed and convex; box shells also carry center/size",
               "colliders": COLLIDERS}, f, indent=1)
print("built", len(COLLIDERS), "assets ->", OUT)
