# Wayside Shrine prop set - procedural low-poly generator (CC0 1.0, public domain).
# Run headless:  blender -b -P build_wayside_shrine.py -- <output_dir>
# Writes fbx/, glb/ (visual meshes) and collision/fbx/, collision/glb/ (box collision hulls)
# plus colliders.json (box collider definitions in glTF axes: x right, y up, z toward the front).
# Conventions: 1 unit = 1 m, bottom-centre pivot, flat shading, material slots Primary/Secondary/Accent.
import bpy, bmesh, math, sys, os, json
from mathutils import Vector

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
for d in ("fbx", "glb", "collision/fbx", "collision/glb"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

SLOTS = ("Primary", "Secondary", "Accent")
STONE = (0.50, 0.49, 0.46, 1)
DARK = (0.30, 0.28, 0.27, 1)
WOOD = (0.36, 0.23, 0.13, 1)
IRON = (0.20, 0.20, 0.22, 1)
BRONZE = (0.45, 0.33, 0.16, 1)
WAX = (0.86, 0.82, 0.70, 1)


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


def bottom_centre(obs):
    vs = [v.co for ob in obs for v in ob.data.vertices]
    mn = Vector((min(v.x for v in vs), min(v.y for v in vs), min(v.z for v in vs)))
    mx = Vector((max(v.x for v in vs), max(v.y for v in vs), max(v.z for v in vs)))
    off = Vector((-(mn.x + mx.x) / 2, -(mn.y + mx.y) / 2, -mn.z))
    for ob in obs:
        for v in ob.data.vertices:
            v.co += off
        ob.data.update()
    return off


def export(path_noext, sel):
    bpy.ops.object.select_all(action="DESELECT")
    for o in sel:
        o.select_set(True)
    bpy.context.view_layer.objects.active = sel[0]
    bpy.ops.export_scene.fbx(
        filepath=path_noext[0] + ".fbx", use_selection=True, object_types={"EMPTY", "MESH"},
        apply_unit_scale=True, apply_scale_options="FBX_SCALE_ALL", axis_forward="-Z", axis_up="Y",
        bake_space_transform=True, path_mode="STRIP", embed_textures=False, bake_anim=False,
        mesh_smooth_type="FACE", use_mesh_modifiers=True, add_leaf_bones=False)
    bpy.ops.export_scene.gltf(
        filepath=path_noext[1] + ".glb", export_format="GLB", use_selection=True, export_apply=True,
        export_animations=False, export_extras=False)


COLLIDERS = {}


def build(name, parts, cols, collider_boxes):
    """parts: list of (node_suffix or None, builder(bm)). collider_boxes: Blender-space (x0,x1,y0,y1,z0,z1)."""
    reset()
    mats = make_mats(cols)
    obs = []
    for suffix, fn in parts:
        bm = bmesh.new()
        fn(bm)
        obs.append(to_object(name if suffix is None else f"{name}-{suffix}", bm, mats))
    off = bottom_centre(obs)
    box_uv(obs)
    sel = list(obs)
    if len(obs) > 1:
        root = bpy.data.objects.new(name, None)
        bpy.context.scene.collection.objects.link(root)
        for ob in obs:
            ob.parent = root
        sel = [root] + obs
    export((os.path.join(OUT, "fbx", name), os.path.join(OUT, "glb", name)), sel)
    # collision hulls: one closed box shell per collider, same pivot offset
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    cobs, defs = [], []
    for i, (x0, x1, y0, y1, z0, z1) in enumerate(collider_boxes):
        x0, x1, y0, y1, z0, z1 = x0 + off.x, x1 + off.x, y0 + off.y, y1 + off.y, z0 + off.z, z1 + off.z
        bm = bmesh.new()
        box(bm, x0, x1, y0, y1, z0, z1, "Primary")
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bmesh.ops.triangulate(bm, faces=bm.faces)
        me = bpy.data.meshes.new(f"{name}-col-{i:02d}")
        bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new(me.name, me)
        bpy.context.scene.collection.objects.link(ob)
        cobs.append(ob)
        # glTF axes: x = x, y = z (up), z = -y (front)
        defs.append({"type": "box",
                     "center": [round((x0 + x1) / 2, 4), round((z0 + z1) / 2, 4), round(-(y0 + y1) / 2, 4)],
                     "size": [round(x1 - x0, 4), round(z1 - z0, 4), round(y1 - y0, 4)]})
    export((os.path.join(OUT, "collision", "fbx", f"{name}-col"), os.path.join(OUT, "collision", "glb", f"{name}-col")), cobs)
    COLLIDERS[name] = defs


# ---------------------------------------------------------------- 1. wayside shrine (gable roof, open niche)
ZR, EAVE_X, ZE, TV = 2.04, 0.64, 1.66, 0.08   # ridge height, eave half-width, eave height, roof thickness (vertical)
SLOPE = (ZR - ZE) / EAVE_X


def under(x):
    return ZR - TV - SLOPE * abs(x)


def shrine_base(bm):
    box(bm, -0.60, 0.60, -0.40, 0.40, 0.00, 0.16, "Primary")            # plinth
    box(bm, -0.54, 0.54, -0.37, 0.33, 0.16, 0.24, "Secondary")          # step
    box(bm, -0.38, 0.38, -0.30, 0.18, 0.24, 0.34, "Secondary")          # niche sill
    box(bm, -0.15, 0.15, 0.02, 0.18, 0.34, 0.46, "Secondary")           # stele foot
    prism_xz(bm, [(-0.10, 0.46), (0.10, 0.46), (0.10, 0.95), (0.0, 1.05), (-0.10, 0.95)], 0.05, 0.14, "Primary")  # stele
    disc_y(bm, 0.0, 0.02, 0.05, 0.82, 0.065, 8, "Accent")                # plain disc emblem
    for x in (-0.24, 0.24):                                              # votive cups on the sill
        lathe(bm, [(0, 0.34), (0.035, 0.34), (0.045, 0.40), (0.03, 0.40), (0.0, 0.37)], 6, "Accent", x, -0.17)


def shrine_wall(bm):
    box(bm, -0.50, 0.50, 0.18, 0.30, 0.24, 1.60, "Primary")             # back wall
    for s in (-1, 1):
        box(bm, *sorted((s * 0.38, s * 0.50)), -0.30, 0.18, 0.24, 1.60, "Primary")  # side walls
        box(bm, *sorted((s * 0.36, s * 0.53)), -0.34, -0.26, 0.24, 1.60, "Primary")  # front pilasters
    box(bm, -0.38, 0.38, -0.32, -0.22, 1.44, 1.60, "Secondary")         # lintel
    # gable infill up to the roof underside (front and back faces flush with the walls)
    prism_xz(bm, [(-0.50, 1.60), (0.50, 1.60), (0.50, under(0.50)), (0.0, under(0.0)), (-0.50, under(0.50))],
             -0.30, 0.30, "Primary")


def shrine_roof(bm):
    # one closed chevron slab: two half-width slopes meeting on the ridge line x = 0
    prism_xz(bm, [(-EAVE_X, ZE - TV), (0.0, ZR - TV), (EAVE_X, ZE - TV), (EAVE_X, ZE), (0.0, ZR), (-EAVE_X, ZE)],
             -0.44, 0.40, "Secondary")
    prism_xz(bm, [(-0.07, ZR - 0.03), (0.07, ZR - 0.03), (0.0, ZR + 0.04)], -0.46, 0.42, "Accent")   # ridge cap


build("prop-wayside-shrine-stone",
      [("base", shrine_base), ("wall", shrine_wall), ("roof", shrine_roof)],
      (STONE, DARK, IRON),
      [(-0.60, 0.60, -0.40, 0.40, 0.00, 0.24),
       (-0.53, 0.53, -0.34, 0.30, 0.24, 1.60),
       (-0.64, 0.64, -0.44, 0.40, 1.60, 2.08)])

# ---------------------------------------------------------------- 2. offering dish (wide, shallow, open)
def offering(bm):
    lathe(bm, [(0, 0.0), (0.19, 0.0), (0.19, 0.05), (0.13, 0.10), (0.07, 0.14), (0.055, 0.40), (0.085, 0.44),
               (0.055, 0.48), (0.05, 0.60), (0.11, 0.66), (0.0, 0.66)], 12, "Secondary")          # stand
    lathe(bm, [(0.084, 0.425), (0.095, 0.425), (0.095, 0.455), (0.084, 0.455)], 12, "Accent", loop=True)  # knop band
    lathe(bm, [(0, 0.64), (0.10, 0.64), (0.24, 0.68), (0.31, 0.735), (0.33, 0.745), (0.33, 0.77),
               (0.295, 0.77), (0.22, 0.725), (0.10, 0.705), (0.0, 0.70)], 16, "Primary")            # dish
    for x, y in ((-0.06, 0.04), (0.05, 0.07), (0.07, -0.05)):
        pebble(bm, (x, y, 0.725), 0.04, "Secondary")                                            # offerings
    for x, y in ((-0.10, -0.08), (0.13, 0.02)):
        cyl(bm, x, y, 0.705 + 0.012 * x, 0.716 + 0.012 * x, 0.022, 6, "Accent")                # coins


build("prop-offering-bowl-stone", [(None, offering)], (STONE, DARK, BRONZE),
      [(-0.19, 0.19, -0.19, 0.19, 0.0, 0.64), (-0.33, 0.33, -0.33, 0.33, 0.64, 0.77)])

# ---------------------------------------------------------------- 3. holy water font (deep octagonal basin)
OCT = math.pi / 8


def font(bm):
    lathe(bm, [(0, 0.0), (0.40, 0.0), (0.40, 0.10), (0.0, 0.10)], 8, "Primary", rot=OCT)      # base step
    lathe(bm, [(0, 0.10), (0.31, 0.10), (0.31, 0.18), (0.0, 0.18)], 8, "Secondary", rot=OCT)   # second step
    lathe(bm, [(0, 0.18), (0.15, 0.18), (0.15, 0.62), (0.0, 0.62)], 8, "Primary", rot=OCT)     # shaft
    lathe(bm, [(0.145, 0.20), (0.18, 0.20), (0.18, 0.25), (0.145, 0.25)], 8, "Accent", rot=OCT, loop=True)
    lathe(bm, [(0, 0.58), (0.17, 0.58), (0.26, 0.65), (0.34, 0.78), (0.37, 0.98), (0.37, 1.05),
               (0.30, 1.05), (0.29, 0.98), (0.25, 0.83), (0.0, 0.77)], 8, "Primary", rot=OCT)   # basin, 0.28 m deep
    lathe(bm, [(0.35, 0.87), (0.385, 0.87), (0.385, 0.93), (0.35, 0.93)], 8, "Accent", rot=OCT, loop=True)  # iron band


build("prop-holy-water-font", [(None, font)], (STONE, DARK, IRON),
      [(-0.37, 0.37, -0.37, 0.37, 0.0, 0.18), (-0.15, 0.15, -0.15, 0.15, 0.18, 0.58),
       (-0.37, 0.37, -0.37, 0.37, 0.58, 1.05)])

# ---------------------------------------------------------------- 4. votive candle rack (three stepped tiers)
TIERS = [(-0.24, -0.08, 0.74), (-0.08, 0.08, 0.86), (0.08, 0.24, 0.98)]   # y0, y1, shelf top


def rack(bm):
    side = [(-0.24, 0.06), (-0.24, 0.74), (-0.08, 0.74), (-0.08, 0.86), (0.08, 0.86), (0.08, 0.98),
            (0.24, 0.98), (0.24, 0.06), (0.14, 0.06), (0.10, 0.18), (-0.10, 0.18), (-0.14, 0.06)]
    for s in (-1, 1):
        prism_yz(bm, side, *sorted((s * 0.41, s * 0.45)), "Secondary")                       # stepped side board
        for y in (-0.24, 0.24):                                                               # feet
            box(bm, *sorted((s * 0.39, s * 0.47)), y - 0.04 if y > 0 else y, y if y > 0 else y + 0.04, 0.0, 0.06, "Secondary")
    for y0, y1, zt in TIERS:
        box(bm, -0.41, 0.41, y0, y1, zt - 0.04, zt, "Secondary")                               # shelf plank
        box(bm, -0.40, 0.40, y0 + 0.01, y1 - 0.01, zt, zt + 0.025, "Accent")                   # sand tray
        box(bm, -0.41, 0.41, y0, y0 + 0.02, zt - 0.16, zt - 0.04, "Secondary")                 # riser / apron
    box(bm, -0.41, 0.41, -0.20, 0.20, 0.22, 0.25, "Secondary")                                 # low shelf brace
    box(bm, -0.41, 0.41, 0.22, 0.24, 0.30, 0.98, "Secondary")                                  # back panel
    box(bm, -0.45, 0.45, 0.20, 0.26, 0.98, 1.02, "Accent")                                     # top rail
    # wax candles: varied heights and widths, unlit
    rnd = [0.62, 0.15, 0.88, 0.41, 0.73, 0.27, 0.95, 0.05, 0.55, 0.34, 0.81, 0.19, 0.67, 0.48, 0.09]
    k = 0
    for t, (y0, y1, zt) in enumerate(TIERS):
        for i, x in enumerate((-0.30, -0.15, 0.0, 0.15, 0.30)):
            u = rnd[k]; k += 1
            h = 0.035 + 0.12 * u
            r = 0.018 + 0.012 * rnd[(k * 7) % 15]
            yy = (y0 + y1) / 2 + (0.025 if (i + t) % 2 else -0.02)
            cyl(bm, x + 0.03 * (u - 0.5), yy, zt + 0.025, zt + 0.025 + h, r, 6, "Primary", rot=u)


build("prop-votive-candle-rack", [(None, rack)], (WAX, WOOD, IRON),
      [(-0.47, 0.47, -0.24, 0.26, 0.0, 1.02)])

with open(os.path.join(OUT, "colliders.json"), "w") as f:
    json.dump({"axes": "glTF: x right, y up, z toward the prop front; metres; pivot bottom-centre",
               "colliders": COLLIDERS}, f, indent=2)
print("built", len(COLLIDERS), "assets ->", OUT)
