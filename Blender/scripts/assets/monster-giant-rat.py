"""monster-giant-rat - Small, scales with the room. The skinned test monster (M4): a hunched giant rat with a smooth-skinned body and tail
(weights blend along the spine and tail bones) and rigid legs and head parts. Clips: idle (breathing, sniffing, tail sway) and walk.
Slots: Primary = fur, Secondary = skin (tail, feet, snout), Accent = inner ears + teeth + claws, Emissive = eyes."""
import math
import okit
from okit import AUTO
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 2500, True
CATEGORY = "Monsters"
MILESTONE = "M4"
EMISSIVE_SCALE = 0.6

BODY_Z = 0.22
RIG = [
    {"name": "root", "head": (0, 0.05, BODY_Z), "tail": (0, 0.05, BODY_Z + 0.12)},
    {"name": "spine", "head": (0, 0.26, BODY_Z), "tail": (0, -0.02, BODY_Z + 0.02), "parent": "root"},
    {"name": "chest", "head": (0, -0.02, BODY_Z + 0.02), "tail": (0, -0.27, BODY_Z + 0.03), "parent": "spine"},
    {"name": "head", "head": (0, -0.27, BODY_Z + 0.03), "tail": (0, -0.5, BODY_Z), "parent": "chest"},
    {"name": "tail1", "head": (0, 0.3, 0.2), "tail": (0.0, 0.43, 0.16), "parent": "root"},
    {"name": "tail2", "head": (0.0, 0.43, 0.16), "tail": (0.05, 0.56, 0.11), "parent": "tail1"},
    {"name": "tail3", "head": (0.05, 0.56, 0.11), "tail": (0.14, 0.66, 0.07), "parent": "tail2"},
    {"name": "tail4", "head": (0.14, 0.66, 0.07), "tail": (0.27, 0.72, 0.04), "parent": "tail3"},
    {"name": "leg_fl", "head": (-0.1, -0.19, 0.17), "tail": (-0.11, -0.23, 0.02), "parent": "chest"},
    {"name": "leg_fr", "head": (0.1, -0.19, 0.17), "tail": (0.11, -0.23, 0.02), "parent": "chest"},
    {"name": "leg_bl", "head": (-0.12, 0.17, 0.17), "tail": (-0.13, 0.2, 0.02), "parent": "spine"},
    {"name": "leg_br", "head": (0.12, 0.17, 0.17), "tail": (0.13, 0.2, 0.02), "parent": "spine"},
]
CLIPS = {
    "idle": {"frames": 48, "channels": [
        ("root", "ly", 0.006, 2, 0), ("chest", "rx", 2.5, 2, 30),
        ("head", "rx", 7, 2, 0), ("head", "rz", 10, 1, 90),
        ("tail1", "rz", 8, 1, 0), ("tail2", "rz", 12, 1, 40), ("tail3", "rz", 16, 1, 80), ("tail4", "rz", 20, 1, 120)]},
    "walk": {"frames": 24, "channels": [
        ("root", "ly", 0.012, 2, 0), ("spine", "rz", 4, 1, 0), ("head", "rx", 4, 2, 60),
        ("leg_fl", "rx", 28, 1, 0), ("leg_br", "rx", 28, 1, 0), ("leg_fr", "rx", 28, 1, 180), ("leg_bl", "rx", 28, 1, 180),
        ("tail1", "rz", 10, 1, 90), ("tail2", "rz", 14, 1, 130), ("tail3", "rz", 18, 1, 170), ("tail4", "rz", 22, 1, 210)]},
}

# smooth skin: piecewise-linear blend between neighbouring bones along the body / tail axis (y)
SPINE_KEYS = [(-0.40, "head"), (-0.2, "chest"), (0.0, "spine"), (0.26, "spine"), (0.36, "tail1"), (0.5, "tail2"), (0.62, "tail3"), (0.72, "tail4")]


def skin(co):
    y = co.y
    if y <= SPINE_KEYS[0][0]:
        return {SPINE_KEYS[0][1]: 1.0}
    for (y0, b0), (y1, b1) in zip(SPINE_KEYS[:-1], SPINE_KEYS[1:]):
        if y <= y1:
            t = (y - y0) / (y1 - y0)
            w = {}
            w[b0] = w.get(b0, 0) + 1 - t
            w[b1] = w.get(b1, 0) + t
            return w
    return {SPINE_KEYS[-1][1]: 1.0}


def build(name, p):
    b = okit.Builder(name)
    with b.bone(AUTO):
        # body: lathe along -Y (rear at y = +0.3, nose at y = -0.47), hunched (slightly higher at the shoulders)
        prof = [(0.0, 0.0), (0.1, 0.02), (0.155, 0.1), (0.175, 0.24), (0.165, 0.38), (0.135, 0.5), (0.1, 0.6), (0.065, 0.69), (0.0, 0.77)]
        b.lathe(prof, 8, loc=(0, 0.3, BODY_Z), slot="Primary", rot=(90, 0, 0))
        # tail: tapering segments (Secondary = bare skin)
        pts = [(0, 0.28, 0.2), (0.0, 0.43, 0.16), (0.05, 0.56, 0.11), (0.14, 0.66, 0.07), (0.27, 0.72, 0.04)]
        for i, (a, c) in enumerate(zip(pts[:-1], pts[1:])):
            b.strut(a, c, 0.05 - 0.009 * i, "Secondary", segs=5)
    with b.bone("head"):
        b.cylinder(0.035, 0.05, 6, (0, -0.47, BODY_Z - 0.02), "Secondary", rot=(90, 0, 0))                     # snout tip / nose
        for sx in (-1, 1):
            b.cylinder(0.05, 0.02, 6, (sx * 0.075, -0.27, BODY_Z + 0.1), "Secondary", r_top=0.04, rot=(-15, sx * 25, 0))   # ear
            b.cylinder(0.042, 0.014, 6, (sx * 0.078, -0.281, BODY_Z + 0.106), "Accent", r_top=0.032, rot=(-15, sx * 25, 0))  # inner ear
            b.box((0.03, 0.02, 0.022), (sx * 0.05, -0.39, BODY_Z + 0.05), "Emissive", bevel=0.0)                 # eye
        b.box((0.05, 0.016, 0.055), (0, -0.466, BODY_Z - 0.1), "Accent", bevel=0.0)                              # incisors
    for leg, (x, y, z0, bone) in {"fl": (-0.1, -0.19, 0.17, "leg_fl"), "fr": (0.1, -0.19, 0.17, "leg_fr"),
                                  "bl": (-0.12, 0.17, 0.17, "leg_bl"), "br": (0.12, 0.17, 0.17, "leg_br")}.items():
        with b.bone(bone):
            fx = x * 1.1
            b.strut((x, y, z0), (fx, y - 0.04 if leg[0] == "f" else y + 0.03, 0.03), 0.06 if leg[0] == "b" else 0.05, "Primary", segs=6)
            fy = (y - 0.04) if leg[0] == "f" else (y + 0.03)
            b.box((0.07, 0.1, 0.03), (fx, fy - 0.02, 0.0), "Secondary", bevel=0.006)                              # paw
            for k in (-1, 0, 1):
                b.box((0.012, 0.03, 0.012), (fx + k * 0.022, fy - 0.08, 0.0), "Accent", bevel=0.0)             # claws
    obj, _ = b.build(skin=skin)
    return obj
