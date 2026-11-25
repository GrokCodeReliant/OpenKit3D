# Farmhouse & Market Equipment prop set - procedural low-poly generator (CC0 1.0, public domain).
# Run headless:  blender -b -P build_farmhouse_market.py -- <output_dir>
# Writes fbx/, glb/ (visual meshes), collision/fbx/, collision/glb/ (convex collision shells)
# and collision/colliders.json (the same shells as plain numbers, glTF axes: x right, y up, z toward the front).
# Conventions: 1 unit = 1 m, bottom-centre pivot, flat shading, material slots Primary/Secondary/Accent.
# The geometry and collision helpers are reused from the kit's Hauling & Lifting build script (also CC0).
import bpy, bmesh, math, sys, os, json
from mathutils import Vector, Matrix

OUT = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
for d in ("fbx", "glb", "collision/fbx", "collision/glb"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

SLOTS = ("Primary", "Secondary", "Accent")
WOOD = (0.42, 0.28, 0.16, 1)
IRON = (0.22, 0.22, 0.24, 1)
ROPE = (0.70, 0.60, 0.42, 1)
PALE = (0.74, 0.62, 0.44, 1)     # pale scrubbed wood
STONE = (0.55, 0.54, 0.50, 1)
FLOUR = (0.90, 0.87, 0.80, 1)
WICKER = (0.66, 0.52, 0.30, 1)


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
            metal = name == "Secondary" and c == IRON
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


# ---------------------------------------------------------------- 1. butter churn (tall staved dash churn, iron hoops, lid, dasher)
CH_R0, CH_R1, CH_H = 0.20, 0.16, 0.78


def churn_r(z):
    return CH_R0 + (CH_R1 - CH_R0) * (z - 0.02) / (CH_H - 0.02)


def churn(bm):
    lathe(bm, [(0, 0.0), (CH_R0, 0.0), (CH_R0, 0.02), (CH_R1, CH_H), (0, CH_H)], SEG, "Primary")       # staved body
    for z0 in (0.07, 0.38, 0.66):                                                                   # iron hoops
        r = churn_r(z0 + 0.02)
        ring(bm, r - 0.015, r + 0.012, z0, z0 + 0.04, SEG, "Secondary")
    for sx in (-1, 1):                                                                              # two long staves as lifting ears
        box(bm, sx * 0.175 - 0.025, sx * 0.175 + 0.025, -0.035, 0.035, 0.60, 0.92, "Primary")
    lathe(bm, [(0, CH_H), (0.172, CH_H), (0.172, CH_H + 0.03), (0, CH_H + 0.03)], SEG, "Accent")     # lid
    lathe(bm, [(0, CH_H + 0.03), (0.05, CH_H + 0.03), (0.04, CH_H + 0.07), (0, CH_H + 0.07)], 8, "Accent")   # splash cup
    cyl(bm, 0, 0, 0.30, 1.18, 0.018, 6, "Accent")                                                   # dasher handle
    box(bm, -0.06, 0.06, -0.012, 0.012, 1.150, 1.175, "Accent")                                     # cross grip


build("prop-butter-churn-wood", churn, (WOOD, IRON, PALE),
      [("hull", -1, 1, -1, 1, -1, 0.95),                       # body, hoops, ears, lid and cup
       ("box", -0.06, 0.06, -0.02, 0.02, 0.80, 1.18)],         # dasher handle (overlaps the body shell below the lid top)
      "solid, blocking (body, hoops, ears and lid; separate thin shell for the dasher handle)")

# ---------------------------------------------------------------- 2. rotary hand quern on a low stand (two stones, handle, spilled flour)
Q_TOP = 0.36


def quern(bm):
    box(bm, -0.32, 0.32, -0.32, 0.32, Q_TOP - 0.06, Q_TOP, "Primary")                              # stand top
    for sx in (-1, 1):
        for sy in (-1, 1):
            box(bm, sx * 0.26 - 0.035, sx * 0.26 + 0.035, sy * 0.26 - 0.035, sy * 0.26 + 0.035, 0.0, Q_TOP - 0.06, "Primary")   # legs
    for sy in (-1, 1):
        box(bm, -0.225, 0.225, sy * 0.26 - 0.02, sy * 0.26 + 0.02, 0.07, 0.12, "Primary")           # stretchers
    lathe(bm, [(0, Q_TOP), (0.23, Q_TOP), (0.23, Q_TOP + 0.10), (0, Q_TOP + 0.11)], 12, "Secondary")   # lower (bed) stone
    lathe(bm, [(0.045, Q_TOP + 0.11), (0.22, Q_TOP + 0.10), (0.22, Q_TOP + 0.185), (0.045, Q_TOP + 0.205)], 12, "Secondary", loop=True)   # upper stone with eye
    lathe(bm, [(0, Q_TOP + 0.15), (0.05, Q_TOP + 0.15), (0, Q_TOP + 0.19)], 8, "Accent")            # grain in the eye
    lathe(bm, [(0.205, Q_TOP + 0.004), (0.29, Q_TOP), (0.232, Q_TOP + 0.035)], 12, "Accent", loop=True)     # spilled flour ring (underside tilted off the stone base)
    cyl(bm, 0.165, 0, Q_TOP + 0.17, Q_TOP + 0.43, 0.022, 6, "Primary")                              # handle peg


build("prop-hand-quern-stone", quern, (WOOD, STONE, FLOUR),
      [("box", -0.32, 0.32, -0.32, 0.32, 0.0, Q_TOP),          # stand (space between the legs filled)
       ("hull", -0.30, 0.30, -0.30, 0.30, Q_TOP - 1e-4, Q_TOP + 0.21),   # stones, flour ring and grain
       ("box", 0.143, 0.187, -0.022, 0.022, Q_TOP + 0.21, Q_TOP + 0.43)],   # handle peg
      "solid, blocking (stand filled as one box; stones and handle above it)")

# ---------------------------------------------------------------- 3. roasting spit (two lashed forked stands, iron spit with crank and prongs)
SP_X, SP_Z = 0.50, 0.74


def spit_stand(bm, x):
    for sy in (-1, 1):
        beam(bm, (x, sy * 0.22, 0.0), (x, sy * 0.03, 0.56), 0.05, "Primary")                       # splayed legs
    beam(bm, (x, 0, 0.30), (x, 0, 0.70), 0.06, "Primary")                                           # upright
    for sy in (-1, 1):
        beam(bm, (x, sy * 0.022, 0.68), (x, sy * 0.08, 0.86), 0.035, "Primary")                    # fork tines (kept apart: no shared faces)
    box(bm, x - 0.04, x + 0.04, -0.05, 0.05, 0.50, 0.58, "Accent")                                  # rope lashing (legs)
    box(bm, x - 0.035, x + 0.035, -0.045, 0.045, 0.64, 0.69, "Accent")                              # rope lashing (fork)


def spit(bm):
    for sx in (-1, 1):
        spit_stand(bm, sx * SP_X)
    cyl_x(bm, -0.58, 0.60, 0, SP_Z, 0.014, 6, "Secondary")                                          # iron spit rod
    beam(bm, (0.60, 0, SP_Z + 0.01), (0.60, 0, SP_Z - 0.16), 0.025, "Secondary")                   # crank arm
    cyl_x(bm, 0.60, 0.68, 0, SP_Z - 0.15, 0.02, 6, "Primary")                                       # crank grip
    for x in (-0.20, 0.20):                                                                         # meat prongs
        box(bm, x - 0.012, x + 0.012, -0.012, 0.012, SP_Z - 0.07, SP_Z + 0.07, "Secondary")
        box(bm, x - 0.009, x + 0.009, -0.07, 0.07, SP_Z - 0.018, SP_Z + 0.018, "Secondary")   # sized off the rod and upright tine faces


build("prop-roasting-spit-wood", spit, (WOOD, IRON, ROPE),
      [("hull", -1, -0.35, -1, 1, -1, 2),                      # left stand (A-legs, upright, fork, lashings)
       ("hull", 0.35, 0.56, -1, 1, -1, 2),                     # right stand
       ("box", -0.58, 0.60, -0.07, 0.07, SP_Z - 0.07, SP_Z + 0.07),   # spit rod and prongs
       ("hull", 0.565, 1, -1, 1, -1, 2)],                      # crank arm and grip
      "stands, spit rod and crank; the space under the rod between the stands is left open (place your own fire there)")

# ---------------------------------------------------------------- 4. steelyard weighing frame (two-post frame, crossbar, steelyard, counterpoise, hanging pan)
ST_X, BAR_Z, BEAM_Z, PAN_X = 0.50, 1.90, 1.66, -0.14


def steelyard(bm):
    for sx in (-1, 1):
        x = sx * ST_X
        box(bm, x - 0.05, x + 0.05, -0.30, 0.30, 0.0, 0.10, "Primary")                             # foot sill
        box(bm, x - 0.045, x + 0.045, -0.045, 0.045, 0.10, BAR_Z, "Primary")                         # post
        for sy in (-1, 1):
            beam(bm, (x, sy * 0.25, 0.08), (x, sy * 0.035, 0.52), 0.05, "Primary")                  # foot braces
    box(bm, -0.58, 0.58, -0.05, 0.05, BAR_Z, BAR_Z + 0.10, "Primary")                                # crossbar
    beam(bm, (0, 0, BAR_Z + 0.005), (0, 0, BEAM_Z + 0.02), 0.025, "Secondary")                       # hanger
    box(bm, -0.22, 0.52, -0.015, 0.015, BEAM_Z - 0.015, BEAM_Z + 0.015, "Secondary")                 # steelyard beam
    for k in range(1, 7):                                                                           # notch marks on the long arm
        box(bm, 0.05 * k + 0.07, 0.05 * k + 0.08, -0.018, 0.018, BEAM_Z + 0.010, BEAM_Z + 0.022, "Secondary")
    beam(bm, (0.36, 0, BEAM_Z - 0.005), (0.36, 0, BEAM_Z - 0.10), 0.015, "Secondary")                 # counterpoise hook
    lathe(bm, [(0, BEAM_Z - 0.10), (0.03, BEAM_Z - 0.11), (0.055, BEAM_Z - 0.18), (0.045, BEAM_Z - 0.24), (0, BEAM_Z - 0.25)], 8, "Secondary", cx=0.36)   # pear weight
    beam(bm, (PAN_X, 0, BEAM_Z - 0.005), (PAN_X, 0, BEAM_Z - 0.16), 0.02, "Secondary")               # load hook
    for k in range(3):                                                                              # three chains to the pan rim
        a = 2 * math.pi * k / 3 + math.pi / 2
        beam(bm, (PAN_X, 0, BEAM_Z - 0.15), (PAN_X + 0.19 * math.cos(a), 0.19 * math.sin(a), 0.97), 0.012, "Secondary")
    lathe(bm, [(0, 0.84), (0.15, 0.84), (0.21, 0.90), (0.22, 0.97), (0.19, 0.97), (0.18, 0.91), (0, 0.89)], 10, "Accent", cx=PAN_X)   # wicker pan


build("prop-steelyard-scale-frame", steelyard, (WOOD, IRON, WICKER),
      [("hull", -1, -0.44, -1, 1, -1, BAR_Z), ("hull", 0.44, 1, -1, 1, -1, BAR_Z),    # two side frames (sill, post, braces)
       ("box", -0.58, 0.58, -0.05, 0.05, BAR_Z, BAR_Z + 0.10),                           # crossbar
       ("hull", -0.25, 0.55, -1, 1, BEAM_Z - 0.26, BAR_Z + 0.01),                               # hanger, steelyard, counterpoise, hooks, chain tops
       ("hull", -0.45, 0.17, -1, 1, 0.83, BEAM_Z - 0.14)],                               # chains and pan (open space between the chains filled)
      "side frames, crossbar, steelyard and hanging pan; open between the posts below the pan and beside it")

with open(os.path.join(OUT, "collision", "colliders.json"), "w") as f:
    json.dump({"axes": "glTF: x right, y up, z toward the prop front; metres; pivot bottom-centre",
               "note": "every shell is closed and convex; box shells also carry center/size",
               "colliders": COLLIDERS}, f, indent=1)
print("built", len(COLLIDERS), "assets ->", OUT)
