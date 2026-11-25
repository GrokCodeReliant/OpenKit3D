# Arcane Focus prop set - procedural low-poly generator (CC0 1.0, public domain).
# Run headless:  blender -b -P build_arcane_focus.py -- <output_dir>
# Writes fbx/, glb/ (visual meshes), collision/fbx/, collision/glb/ (convex collision shells)
# and collision/colliders.json (the same shells as plain numbers, glTF axes: x right, y up, z toward the front).
# Conventions: 1 unit = 1 m, bottom-centre pivot, flat shading, material slots Primary/Secondary/Accent.
import bpy, bmesh, math, sys, os, json
from mathutils import Vector, Matrix

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
for d in ("fbx", "glb", "collision/fbx", "collision/glb"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

SLOTS = ("Primary", "Secondary", "Accent")
STONE = (0.47, 0.47, 0.50, 1)
DARK = (0.27, 0.27, 0.30, 1)
IRON = (0.20, 0.20, 0.22, 1)
WOOD = (0.33, 0.22, 0.14, 1)
CRYSTAL = (0.33, 0.52, 0.86, 1)
RUNE = (0.30, 0.62, 0.80, 1)


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
            b.inputs["Roughness"].default_value = 0.85 if name != "Accent" else 0.5
            b.inputs["Metallic"].default_value = 0.6 if name == "Accent" else 0.0
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


def pebble(bm, c, r, slot, squash=0.7):
    g = bmesh.ops.create_uvsphere(bm, u_segments=6, v_segments=4, radius=r)
    for v in g["verts"]:
        v.co = Vector((c[0] + v.co.x, c[1] + v.co.y, c[2] + v.co.z * squash))
    for f in {f for v in g["verts"] for f in v.link_faces}:
        f.material_index = S[slot]


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


def crystal(bm, base, h, r, seg, slot, tilt=0.0, heading=0.0, spin=0.0):
    """Faceted crystal (prism with pointed tip) leaning by tilt toward heading."""
    prof = [(0, 0.0), (r * 0.8, h * 0.08), (r, h * 0.22), (r * 0.9, h * 0.78), (0, h)]
    g0 = len(bm.verts)
    tmp = bmesh.new()
    lathe(tmp, prof, seg, slot, rot=spin)
    M = Matrix.Translation(Vector(base)) @ Matrix.Rotation(heading, 4, "Z") @ Matrix.Rotation(tilt, 4, "Y")
    tmp.transform(M)
    me = bpy.data.meshes.new("_tmp")
    tmp.to_mesh(me); tmp.free()
    bm.from_mesh(me)
    bpy.data.meshes.remove(me)


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


COLLIDERS = {}


def collider_shell(bm, spec, all_verts):
    kind = spec[0]
    if kind == "box":
        box(bm, *spec[1:], "Primary")
    elif kind == "lathe":
        _, prof, seg, rot, cx, cy = spec
        lathe(bm, prof, seg, "Primary", cx, cy, rot)
    elif kind == "hull":   # convex hull of the visual vertices, optionally limited to a height band
        z0, z1 = (spec[1], spec[2]) if len(spec) > 1 else (-1e9, 1e9)
        vs = [bm.verts.new(p) for p in all_verts if z0 - 1e-6 <= p.z <= z1 + 1e-6]
        bmesh.ops.convex_hull(bm, input=vs, use_existing_faces=False)
        loose = [v for v in bm.verts if not v.link_faces]
        bmesh.ops.delete(bm, geom=loose, context="VERTS")


def build(name, builder, cols, collider_specs, walkable=None):
    reset()
    mats = make_mats(cols)
    bm = bmesh.new()
    builder(bm)
    ob = to_object(name, bm, mats)
    vs = [v.co for v in ob.data.vertices]
    off = Vector((-(min(v.x for v in vs) + max(v.x for v in vs)) / 2, -(min(v.y for v in vs) + max(v.y for v in vs)) / 2, -min(v.z for v in vs)))
    for v in ob.data.vertices:
        v.co += off
    ob.data.update()
    box_uv([ob])
    all_verts = [v.co.copy() for v in ob.data.vertices]
    export((os.path.join(OUT, "fbx", name), os.path.join(OUT, "glb", name)), [ob])
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    cobs, defs = [], []
    for i, spec in enumerate(collider_specs):
        bm = bmesh.new()
        collider_shell(bm, spec, all_verts if spec[0] == "hull" else None)
        if spec[0] != "hull":
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
        d = {"node": me.name, "shape": spec[0] if spec[0] != "lathe" else "prism",
             "convex": True, "bounds_center": [round((a + b) / 2, 4) for a, b in zip(mn, mx)],
             "bounds_size": [round(b - a, 4) for a, b in zip(mn, mx)]}
        if spec[0] == "box":
            d["type"] = "box"; d["center"] = d["bounds_center"]; d["size"] = d["bounds_size"]
        else:
            d["type"] = "convex_mesh"; d["vertices"] = P
        defs.append(d)
    export((os.path.join(OUT, "collision", "fbx", f"{name}-col"), os.path.join(OUT, "collision", "glb", f"{name}-col")), cobs)
    COLLIDERS[name] = {"shells": defs}
    if walkable:
        COLLIDERS[name]["walkable_top_y"] = walkable


R2 = math.sqrt(2)

# ---------------------------------------------------------------- 1. rune obelisk (tapered stone needle, rune inlays)
def hw(z):  # shaft half-width at height z
    return 0.30 - 0.11 * (z - 0.30) / 1.75


GLYPHS = [  # strokes in face coordinates (u across, v up), metres, relative to glyph centre
    [((0, -0.09), (0, 0.09)), ((0, 0.02), (0.06, 0.08))],
    [((-0.05, -0.08), (0.05, 0.08)), ((0.05, -0.08), (-0.05, 0.08))],
    [((0, -0.09), (0, 0.09)), ((0, 0.09), (0.06, 0.03)), ((0, 0.0), (0.06, -0.06))],
    [((-0.05, 0.08), (0, -0.08)), ((0, -0.08), (0.05, 0.08))],
]


def obelisk(bm):
    box(bm, -0.55, 0.55, -0.55, 0.55, 0.0, 0.14, "Secondary")
    box(bm, -0.43, 0.43, -0.43, 0.43, 0.14, 0.30, "Primary")
    lathe(bm, [(0, 0.30), (0.30 * R2, 0.30), (hw(2.05) * R2, 2.05), (0, 2.05)], 4, "Primary", rot=math.pi / 4)
    lathe(bm, [(0, 2.05), (0.215 * R2, 2.05), (0.215 * R2, 2.10), (0, 2.40)], 4, "Secondary", rot=math.pi / 4)
    tilt = math.atan2(0.11, 1.75)
    k = 0
    for face in range(4):
        ang = face * math.pi / 2
        out = Vector((math.sin(ang), -math.cos(ang), 0))       # face 0 = front (-y)
        uax = Vector((math.cos(ang), math.sin(ang), 0))
        vax = (Vector((0, 0, 1)) - out * math.tan(tilt)).normalized()
        nrm = uax.cross(vax).normalized() * -1 if uax.cross(vax).dot(out) < 0 else uax.cross(vax).normalized()
        for zc in (0.85, 1.25, 1.65):
            g = GLYPHS[k % len(GLYPHS)]; k += 1
            base = out * (hw(zc) + 0.008) + Vector((0, 0, zc))
            for (u0, v0), (u1, v1) in g:
                p0 = base + uax * u0 + vax * v0
                p1 = base + uax * u1 + vax * v1
                a = p1 - p0
                obox(bm, (p0 + p1) / 2, a, nrm.cross(a), nrm, a.length / 2 + 0.012, 0.012, 0.010, "Accent")


build("prop-rune-obelisk-stone", obelisk, (STONE, DARK, RUNE),
      [("box", -0.55, 0.55, -0.55, 0.55, 0.0, 0.14), ("box", -0.43, 0.43, -0.43, 0.43, 0.14, 0.30),
       ("lathe", [(0, 0.30), (0.30 * R2, 0.30), (hw(2.05) * R2, 2.05), (0, 2.05)], 4, math.pi / 4, 0, 0),
       ("lathe", [(0, 2.05), (0.215 * R2, 2.05), (0.215 * R2, 2.10), (0, 2.40)], 4, math.pi / 4, 0, 0)])

# ---------------------------------------------------------------- 2. crystal focus pylon (crystal held by iron claws)
OCT = math.pi / 8


def pylon(bm):
    lathe(bm, [(0, 0.0), (0.50, 0.0), (0.50, 0.10), (0.44, 0.13), (0.0, 0.13)], 8, "Primary", rot=OCT)
    lathe(bm, [(0, 0.13), (0.27, 0.13), (0.21, 0.60), (0.24, 0.64), (0.0, 0.64)], 8, "Primary", rot=OCT)
    lathe(bm, [(0.235, 0.56), (0.265, 0.56), (0.265, 0.60), (0.235, 0.60)], 8, "Secondary", rot=OCT, loop=True)
    for i in range(3):   # iron claws: rise out, then hook in toward the crystal
        a = math.pi / 2 + i * 2 * math.pi / 3
        d = Vector((math.cos(a), math.sin(a), 0))
        p0 = d * 0.17 + Vector((0, 0, 0.60)); p1 = d * 0.26 + Vector((0, 0, 0.98)); p2 = d * 0.15 + Vector((0, 0, 1.18))
        beam(bm, p0, p1, 0.04, "Secondary"); beam(bm, p1, p2, 0.035, "Secondary")
    crystal(bm, (0, 0, 0.52), 1.10, 0.15, 6, "Accent", spin=0.3)
    for (x, y, h, r, t, hd) in ((0.33, 0.12, 0.34, 0.06, 0.45, 0.35), (-0.30, 0.20, 0.26, 0.05, 0.5, 2.6),
                                (-0.08, -0.36, 0.30, 0.055, 0.42, -1.7), (0.22, -0.30, 0.18, 0.04, 0.6, -0.9)):
        crystal(bm, (x, y, 0.10), h, r, 5, "Accent", tilt=t, heading=hd)


build("prop-crystal-focus-pylon", pylon, (STONE, IRON, CRYSTAL),
      [("hull", 0.0, 0.45), ("hull", 0.13, 0.64), ("hull", 0.56, 2.0)])

# ---------------------------------------------------------------- 3. scrying orb on an iron tripod
def tripod(bm):
    tops = []
    for i in range(3):
        a = math.pi / 2 + i * 2 * math.pi / 3
        d = Vector((math.cos(a), math.sin(a), 0))
        foot = d * 0.34 + Vector((0, 0, 0.0)); top = d * 0.13 + Vector((0, 0, 0.86))
        beam(bm, foot + Vector((0, 0, 0.04)), top, 0.035, "Secondary")
        box(bm, foot.x - 0.04, foot.x + 0.04, foot.y - 0.04, foot.y + 0.04, 0.0, 0.05, "Secondary")   # foot pad
        tops.append(top)
    lathe(bm, [(0.235, 0.36), (0.26, 0.36), (0.26, 0.39), (0.235, 0.39)], 12, "Secondary", loop=True)  # brace ring
    lathe(bm, [(0, 0.82), (0.09, 0.82), (0.16, 0.89), (0.18, 0.95), (0.155, 0.95), (0.12, 0.905), (0, 0.885)],
          12, "Primary")                                                                              # stone cup
    g = bmesh.ops.create_uvsphere(bm, u_segments=14, v_segments=9, radius=0.165)
    for v in g["verts"]:
        v.co += Vector((0, 0, 1.03))
    for f in {f for v in g["verts"] for f in v.link_faces}:
        f.material_index = S["Accent"]


build("prop-scrying-orb-tripod", tripod, (STONE, IRON, CRYSTAL), [("hull",)])

# ---------------------------------------------------------------- 4. ritual dais (walkable two-step platform, 2x2 cells)
def dais(bm):
    lathe(bm, [(0, 0.0), (1.40, 0.0), (1.40, 0.08), (1.37, 0.10), (0, 0.10)], 16, "Primary")
    lathe(bm, [(0, 0.10), (1.10, 0.10), (1.10, 0.18), (1.07, 0.20), (0, 0.20)], 16, "Secondary")
    lathe(bm, [(0.78, 0.198), (0.86, 0.198), (0.86, 0.205), (0.78, 0.205)], 24, "Accent", loop=True)   # rune ring inlay
    lathe(bm, [(0, 0.198), (0.20, 0.198), (0.20, 0.205), (0, 0.205)], 8, "Accent")                      # centre seal
    for i in range(8):   # radial rune ticks between ring and edge
        a = i * math.pi / 4 + math.pi / 8
        d = Vector((math.cos(a), math.sin(a), 0)); t = Vector((-d.y, d.x, 0))
        obox(bm, d * 0.95 + Vector((0, 0, 0.2015)), d, t, (0, 0, 1), 0.06, 0.012, 0.0035, "Accent")
    for i in range(4):   # marker stones on the lower step
        a = math.pi / 4 + i * math.pi / 2
        c = Vector((math.cos(a), math.sin(a), 0)) * 1.25
        lathe(bm, [(0, 0.10), (0.11, 0.10), (0.085, 0.40), (0, 0.46)], 4, "Primary", c.x, c.y, rot=a)


build("prop-ritual-dais-stone", dais, (STONE, DARK, RUNE),
      [("lathe", [(0, 0.0), (1.40, 0.0), (1.40, 0.10), (0, 0.10)], 16, 0.0, 0, 0),
       ("lathe", [(0, 0.10), (1.10, 0.10), (1.10, 0.20), (0, 0.20)], 16, 0.0, 0, 0)]
      + [("lathe", [(0, 0.10), (0.11, 0.10), (0.085, 0.40), (0, 0.46)], 4, math.pi / 4 + i * math.pi / 2,
          1.25 * math.cos(math.pi / 4 + i * math.pi / 2), 1.25 * math.sin(math.pi / 4 + i * math.pi / 2)) for i in range(4)],
      walkable=0.20)

with open(os.path.join(OUT, "collision", "colliders.json"), "w") as f:
    json.dump({"axes": "glTF: x right, y up, z toward the prop front; metres; pivot bottom-centre",
               "note": "every shell is closed and convex; box shells also carry center/size",
               "colliders": COLLIDERS}, f, indent=1)
print("built", len(COLLIDERS), "assets ->", OUT)
