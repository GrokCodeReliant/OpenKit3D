"""monster-construct-clockwork-hound - Medium, scales with the room. Rigid-part clockwork hound (M4): brass plates on a dark iron
frame, flank gears, a wind-up key on the back, hinged jaw, two-segment legs and a segmented tail. Clips: idle (breathing, head tilt,
jaw clack, tail wag, key turning) and walk (trot, diagonal legs in phase).
Slots: Primary = brass plates, Secondary = dark iron frame / joints, Metal = gears, pistons, rivets, key, Accent = copper trim,
Emissive = eyes."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 5000, True
CATEGORY = "Monsters"
MILESTONE = "M4"
EMISSIVE_SCALE = 0.7

LEGS = {"fl": (-0.17, -0.27, "chest"), "fr": (0.17, -0.27, "chest"), "bl": (-0.17, 0.27, "root"), "br": (0.17, 0.27, "root")}
RIG = [
    {"name": "root", "head": (0, 0.1, 0.5), "tail": (0, 0.1, 0.62)},
    {"name": "chest", "head": (0, 0.1, 0.58), "tail": (0, -0.36, 0.6), "parent": "root"},
    {"name": "neck", "head": (0, -0.36, 0.62), "tail": (0, -0.47, 0.76), "parent": "chest"},
    {"name": "head", "head": (0, -0.47, 0.78), "tail": (0, -0.76, 0.8), "parent": "neck"},
    {"name": "jaw", "head": (0, -0.5, 0.72), "tail": (0, -0.76, 0.7), "parent": "head"},
    {"name": "tail1", "head": (0, 0.38, 0.66), "tail": (0, 0.5, 0.73), "parent": "root"},
    {"name": "tail2", "head": (0, 0.5, 0.73), "tail": (0, 0.61, 0.8), "parent": "tail1"},
    {"name": "tail3", "head": (0, 0.61, 0.8), "tail": (0, 0.71, 0.87), "parent": "tail2"},
    {"name": "key", "head": (0, 0.02, 0.74), "tail": (0, 0.02, 0.92), "parent": "chest"},
]
for _k, (_x, _y, _p) in LEGS.items():
    RIG.append({"name": f"upper_{_k}", "head": (_x, _y, 0.5), "tail": (_x, _y - 0.02, 0.27), "parent": _p})
    RIG.append({"name": f"lower_{_k}", "head": (_x, _y - 0.02, 0.27), "tail": (_x, _y, 0.03), "parent": f"upper_{_k}"})

CLIPS = {
    "idle": {"frames": 48, "channels": [
        ("chest", "rx", 1.5, 2, 0), ("root", "ly", 0.006, 2, 90), ("head", "ry", 8, 1, 0), ("head", "rx", 4, 1, 90),
        ("jaw", "rx", 6, 2, 0), ("tail1", "rz", 10, 2, 0), ("tail2", "rz", 14, 2, 40), ("tail3", "rz", 18, 2, 80),
        ("key", "ry", 60, 1, 0)]},
    "walk": {"frames": 24, "channels": [
        ("root", "ly", 0.015, 2, 0), ("chest", "rz", 3, 1, 0), ("neck", "rx", 4, 2, 60),
        ("upper_fl", "rx", 24, 1, 0), ("upper_br", "rx", 24, 1, 0), ("upper_fr", "rx", 24, 1, 180), ("upper_bl", "rx", 24, 1, 180),
        ("lower_fl", "rx", -14, 1, 60), ("lower_br", "rx", -14, 1, 60), ("lower_fr", "rx", -14, 1, 240), ("lower_bl", "rx", -14, 1, 240),
        ("tail1", "rz", 8, 1, 90), ("tail2", "rz", 12, 1, 130), ("tail3", "rz", 16, 1, 170), ("key", "ry", 90, 1, 0)]},
}


def build(name, p):
    b = okit.Builder(name)
    with b.bone("root"):
        b.box((0.4, 0.34, 0.24), (0, 0.24, 0.46), "Secondary", bevel=0.03)             # hip frame
        b.box((0.44, 0.3, 0.1), (0, 0.24, 0.68), "Primary", bevel=0.02)                # rump plate
        for sx in (-1, 1):
            b.cylinder(0.07, 0.05, 8, (sx * 0.22, 0.27, 0.5), "Metal", rot=(0, sx * 90, 0))    # hip hub
    with b.bone("chest"):
        b.box((0.36, 0.5, 0.28), (0, -0.12, 0.42), "Secondary", bevel=0.03)            # iron ribcage frame
        b.box((0.46, 0.56, 0.14), (0, -0.14, 0.68), "Primary", bevel=0.03)             # brass back plate
        for sx in (-1, 1):
            b.box((0.05, 0.42, 0.22), (sx * 0.215, -0.13, 0.46), "Primary", bevel=0.015)     # brass flank plate
            b.cylinder(0.11, 0.035, 10, (sx * 0.24, -0.08, 0.57), "Metal", rot=(0, sx * 90, 0))  # flank gear
            b.cylinder(0.04, 0.05, 6, (sx * 0.26, -0.08, 0.57), "Accent", rot=(0, sx * 90, 0))   # copper gear hub
            b.cylinder(0.065, 0.05, 8, (sx * 0.22, -0.27, 0.5), "Metal", rot=(0, sx * 90, 0))    # shoulder hub
            b.strut((sx * 0.21, 0.18, 0.5), (sx * 0.21, -0.3, 0.44), 0.035, "Metal", segs=6)     # flank piston rod
        b.box((0.3, 0.1, 0.06), (0, 0.02, 0.8), "Accent", bevel=0.01)                  # copper key collar
        b.box((0.3, 0.12, 0.22), (0, -0.38, 0.44), "Primary", bevel=0.02)              # brass breastplate
    with b.bone("key"):
        b.cylinder(0.022, 0.12, 6, (0, 0.02, 0.8), "Metal")                             # key shaft
        b.box((0.2, 0.03, 0.1), (0, 0.02, 0.9), "Metal", bevel=0.01)                   # key bow
    with b.bone("neck"):
        b.strut((0, -0.34, 0.6), (0, -0.48, 0.78), 0.14, "Secondary")
        b.ring(0.07, 0.09, 0.04, 8, (0, -0.42, 0.68), "Accent", rot=(-50, 0, 0))
    with b.bone("head"):
        b.box((0.26, 0.24, 0.16), (0, -0.54, 0.74), "Primary", bevel=0.02)             # skull
        b.box((0.16, 0.22, 0.1), (0, -0.72, 0.75), "Primary", bevel=0.02)              # upper muzzle
        b.box((0.1, 0.04, 0.035), (0, -0.84, 0.8), "Secondary", bevel=0.005)           # nose grille
        for sx in (-1, 1):
            b.box((0.05, 0.02, 0.035), (sx * 0.075, -0.665, 0.83), "Emissive", bevel=0.0)          # eye
            b.prism([(-0.04, 0.0), (0.04, 0.0), (0.01, 0.13)], 0.03, (sx * 0.1, -0.5, 0.9), "Secondary", axis='X', rot=(0, sx * -12, 0))  # ear
            b.box((0.03, 0.03, 0.03), (sx * 0.135, -0.54, 0.8), "Metal", bevel=0.0)                # rivet
    with b.bone("jaw"):
        b.box((0.14, 0.26, 0.05), (0, -0.66, 0.68), "Secondary", bevel=0.01)           # lower jaw
        for sx in (-1, 1):
            b.prism([(-0.012, 0.0), (0.012, 0.0), (0.0, 0.035)], 0.012, (sx * 0.05, -0.77, 0.73), "Metal", axis='X')   # fang
    for i, (a, c) in enumerate([((0, 0.36, 0.65), (0, 0.5, 0.73)), ((0, 0.5, 0.73), (0, 0.61, 0.8)), ((0, 0.61, 0.8), (0, 0.72, 0.88))]):
        with b.bone(f"tail{i + 1}"):
            b.strut(a, c, 0.06 - 0.012 * i, "Secondary" if i < 2 else "Primary", segs=6)
            b.ring(0.03 - 0.005 * i, 0.045 - 0.006 * i, 0.03, 6, c, "Metal", rot=(-50, 0, 0))
    for k, (x, y, _p) in LEGS.items():
        with b.bone(f"upper_{k}"):
            b.box((0.1, 0.12, 0.24), (x * 1.06, y, 0.27), "Primary", bevel=0.015)      # brass thigh plate
        with b.bone(f"lower_{k}"):
            b.cylinder(0.045, 0.06, 6, (x * 1.06 - 0.03, y - 0.02, 0.25), "Metal", rot=(0, 90, 0))   # knee hub
            b.strut((x * 1.06, y - 0.02, 0.27), (x * 1.06, y, 0.05), 0.05, "Secondary", segs=6)
            b.box((0.1, 0.14, 0.05), (x * 1.06, y - 0.03, 0.0), "Secondary", bevel=0.01)   # paw
            b.box((0.08, 0.03, 0.03), (x * 1.06, y - 0.1, 0.0), "Metal", bevel=0.0)        # claw plate
    obj, _ = b.build()
    return obj
