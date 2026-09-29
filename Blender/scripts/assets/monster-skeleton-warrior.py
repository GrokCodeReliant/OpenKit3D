"""monster-skeleton-warrior - Medium, scales with the room. Rigid-part skeleton soldier (M4), human-sized (1.8 m): skull with a hinged
jaw under a rusty helmet, hoop ribcage, vertebrae, thin limb bones, a round shield on the left forearm and a sword in the right hand.
Clips: idle (sway, jaw chatter, head turn, sword arm bob) and walk (stiff march).
Slots: Primary = bone, Secondary = shield wood face + leather belt / strap, Metal = helmet, sword, shield rim + boss, right pauldron,
Accent = shield emblem, Emissive = eye sockets.  (Character faces -Y: its left side is +X.)"""
import math
from mathutils import Vector
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 5000, True
CATEGORY = "Monsters"
MILESTONE = "M4"
EMISSIVE_SCALE = 0.6

J = {  # joints
    "hip": (0, 0.02, 0.92), "waist": (0, 0.02, 1.05), "rib": (0, 0.02, 1.3), "neck": (0, 0.02, 1.5), "skull": (0, 0.0, 1.58),
    "sh_l": (0.2, 0.02, 1.45), "el_l": (0.24, 0.02, 1.18), "wr_l": (0.28, -0.2, 1.12),
    "sh_r": (-0.2, 0.02, 1.45), "el_r": (-0.24, 0.02, 1.18), "wr_r": (-0.26, -0.12, 0.98),
    "hp_l": (0.11, 0.02, 0.9), "kn_l": (0.12, 0.0, 0.5), "an_l": (0.12, 0.02, 0.09),
    "hp_r": (-0.11, 0.02, 0.9), "kn_r": (-0.12, 0.0, 0.5), "an_r": (-0.12, 0.02, 0.09),
}
RIG = [
    {"name": "root", "head": J["hip"], "tail": J["waist"]},
    {"name": "spine", "head": J["waist"], "tail": J["rib"], "parent": "root"},
    {"name": "chest", "head": J["rib"], "tail": J["neck"], "parent": "spine"},
    {"name": "neck", "head": J["neck"], "tail": J["skull"], "parent": "chest"},
    {"name": "head", "head": J["skull"], "tail": (0, 0, 1.84), "parent": "neck"},
    {"name": "jaw", "head": (0, 0.0, 1.62), "tail": (0, -0.12, 1.6), "parent": "head"},
]
for _s in ("l", "r"):
    RIG += [
        {"name": f"upperarm_{_s}", "head": J[f"sh_{_s}"], "tail": J[f"el_{_s}"], "parent": "chest"},
        {"name": f"forearm_{_s}", "head": J[f"el_{_s}"], "tail": J[f"wr_{_s}"], "parent": f"upperarm_{_s}"},
        {"name": f"hand_{_s}", "head": J[f"wr_{_s}"], "tail": tuple(Vector(J[f"wr_{_s}"]) + Vector((0, -0.08, -0.03))), "parent": f"forearm_{_s}"},
        {"name": f"thigh_{_s}", "head": J[f"hp_{_s}"], "tail": J[f"kn_{_s}"], "parent": "root"},
        {"name": f"shin_{_s}", "head": J[f"kn_{_s}"], "tail": J[f"an_{_s}"], "parent": f"thigh_{_s}"},
        {"name": f"foot_{_s}", "head": J[f"an_{_s}"], "tail": tuple(Vector(J[f"an_{_s}"]) + Vector((0, -0.14, -0.06))), "parent": f"shin_{_s}"},
    ]
CLIPS = {
    "idle": {"frames": 64, "channels": [
        ("root", "rz", 1.5, 1, 0), ("chest", "rx", 1.5, 2, 0), ("jaw", "rx", 7, 4, 0), ("head", "ry", 10, 1, 90),
        ("upperarm_r", "rx", 4, 1, 0), ("forearm_r", "rx", 3, 1, 60), ("upperarm_l", "rx", 2, 1, 180)]},
    "walk": {"frames": 32, "channels": [
        ("root", "ly", 0.018, 2, 0), ("spine", "ry", 4, 1, 0), ("head", "rx", 3, 2, 90), ("jaw", "rx", 5, 2, 0),
        ("thigh_l", "rx", 18, 1, 0), ("thigh_r", "rx", 18, 1, 180), ("shin_l", "rx", -10, 1, 60), ("shin_r", "rx", -10, 1, 240),
        ("upperarm_r", "rx", 10, 1, 0), ("upperarm_l", "rx", 4, 1, 180)]},
}


def build(name, p):
    b = okit.Builder(name)
    with b.bone("root"):
        b.box((0.3, 0.16, 0.13), (0, 0.02, 0.86), "Primary", bevel=0.03)                # pelvis
        b.box((0.36, 0.22, 0.07), (0, 0.02, 0.99), "Secondary", bevel=0.01)             # leather belt
        b.box((0.06, 0.03, 0.06), (0, -0.095, 0.995), "Metal", bevel=0.005)             # buckle
        b.prism([(-0.1, 0.0), (0.1, 0.0), (0.06, -0.22), (-0.06, -0.22)], 0.02, (0, -0.1, 0.99), "Secondary", axis='Y')   # tattered tabard flap
    with b.bone("spine"):
        for i in range(4):
            b.box((0.075, 0.07, 0.05), (0, 0.04, 1.06 + i * 0.062), "Primary", bevel=0.012)   # vertebrae
    with b.bone("chest"):
        for i, (r, z) in enumerate([(0.13, 1.28), (0.155, 1.33), (0.165, 1.38), (0.15, 1.43)]):
            b.ring(r - 0.025, r, 0.028, 8, (0, 0.01, z), "Primary")                     # hoop ribs
        b.box((0.05, 0.03, 0.2), (0, -0.155, 1.26), "Primary", bevel=0.01)              # sternum
        b.box((0.07, 0.07, 0.24), (0, 0.15, 1.24), "Primary", bevel=0.01)               # spine behind the ribs
        b.strut((-0.24, 0.02, 1.47), (0.24, 0.02, 1.47), 0.05, "Primary")               # collar bones
        b.strut((0.2, -0.17, 1.47), (-0.16, -0.17, 1.2), 0.04, "Secondary")            # baldric strap (front)
        b.strut((0.2, 0.18, 1.47), (-0.16, 0.18, 1.2), 0.04, "Secondary")              # baldric strap (back)
        b.lathe([(0.1, 0.0), (0.11, 0.05), (0.08, 0.1), (0.0, 0.12)], 8, (-0.22, 0.02, 1.42), "Metal")  # right pauldron
    with b.bone("neck"):
        for i in range(2):
            b.cylinder(0.035, 0.035, 6, (0, 0.02, 1.5 + i * 0.04), "Primary")
    with b.bone("head"):
        b.box((0.19, 0.21, 0.19), (0, -0.005, 1.62), "Primary", bevel=0.04)            # skull
        b.box((0.13, 0.05, 0.06), (0, -0.1, 1.62), "Primary", bevel=0.015)             # cheekbones / upper teeth
        for sx in (-1, 1):
            b.box((0.05, 0.02, 0.04), (sx * 0.048, -0.113, 1.7), "Emissive", bevel=0.0)  # eye sockets
        b.box((0.03, 0.02, 0.03), (0, -0.113, 1.66), "Secondary", bevel=0.0)           # nose hole
        b.lathe([(0.145, 0.0), (0.145, 0.04), (0.125, 0.1), (0.07, 0.15), (0.0, 0.165)], 8, (0, -0.005, 1.74), "Metal")  # helmet dome
        b.ring(0.13, 0.165, 0.025, 8, (0, -0.005, 1.74), "Metal")                       # helmet brim
        b.box((0.03, 0.03, 0.13), (0, -0.17, 1.64), "Metal", bevel=0.005)              # nasal guard
    with b.bone("jaw"):
        b.box((0.15, 0.13, 0.05), (0, -0.05, 1.56), "Primary", bevel=0.015)
    for s, sx in (("l", 1), ("r", -1)):
        with b.bone(f"upperarm_{s}"):
            b.strut(J[f"sh_{s}"], J[f"el_{s}"], 0.05, "Primary", segs=6)
            b.box((0.06, 0.06, 0.05), (J[f"el_{s}"][0], J[f"el_{s}"][1], J[f"el_{s}"][2] - 0.025), "Primary", bevel=0.015)   # elbow
        with b.bone(f"forearm_{s}"):
            b.strut(J[f"el_{s}"], J[f"wr_{s}"], 0.04, "Primary", segs=6)
        with b.bone(f"hand_{s}"):
            w = J[f"wr_{s}"]
            b.box((0.06, 0.08, 0.07), (w[0], w[1] - 0.03, w[2] - 0.04), "Primary", bevel=0.012)
        with b.bone(f"thigh_{s}"):
            b.strut(J[f"hp_{s}"], J[f"kn_{s}"], 0.06, "Primary", segs=6)
            k = J[f"kn_{s}"]
            b.box((0.08, 0.08, 0.07), (k[0], k[1] - 0.01, k[2] - 0.035), "Primary", bevel=0.02)   # knee
        with b.bone(f"shin_{s}"):
            b.strut(J[f"kn_{s}"], J[f"an_{s}"], 0.05, "Primary", segs=6)
        with b.bone(f"foot_{s}"):
            a = J[f"an_{s}"]
            b.box((0.09, 0.22, 0.07), (a[0], a[1] - 0.05, 0.0), "Primary", bevel=0.02)
    # shield on the left forearm (character's left = +X), yawed outward
    n = Vector((math.sin(math.radians(20)), -math.cos(math.radians(20)), 0))
    c = Vector((0.3, -0.18, 1.1))
    with b.bone("forearm_l"):
        rot = (90, 0, 20)
        b.cylinder(0.26, 0.04, 12, tuple(c), "Secondary", rot=rot)                     # wooden face
        b.ring(0.24, 0.275, 0.055, 12, tuple(c - n * 0.005), "Metal", rot=rot)          # iron rim
        b.cylinder(0.075, 0.05, 8, tuple(c + n * 0.035), "Metal", r_top=0.04, rot=rot)  # boss
        b.box((0.36, 0.03, 0.07), tuple(c + n * 0.03 + Vector((0, 0, -0.035))), "Accent", bevel=0.0, rot=(0, 0, 20))   # emblem bar
        b.box((0.07, 0.03, 0.36), tuple(c + n * 0.03 + Vector((0, 0, -0.18))), "Accent", bevel=0.0, rot=(0, 0, 20))    # emblem bar
    # sword in the right hand, leaning forward
    h = Vector(J["wr_r"]) + Vector((0, -0.03, -0.035))
    d = Vector((0, -math.sin(math.radians(35)), math.cos(math.radians(35))))
    with b.bone("hand_r"):
        rot = (35, 0, 0)
        b.box((0.03, 0.03, 0.16), tuple(h - d * 0.08), "Secondary", bevel=0.0, rot=rot)    # leather grip
        b.box((0.045, 0.045, 0.045), tuple(h - d * 0.11), "Metal", bevel=0.01, rot=rot)    # pommel
        b.box((0.2, 0.04, 0.035), tuple(h + d * 0.08), "Metal", bevel=0.008, rot=rot)      # crossguard
        b.box((0.065, 0.016, 0.62), tuple(h + d * 0.11), "Metal", bevel=0.004, rot=rot)    # blade
        b.prism([(-0.0325, 0.0), (0.0325, 0.0), (0.0, 0.09)], 0.016, tuple(h + d * 0.73), "Metal", axis='Y', rot=rot)  # tip
    obj, _ = b.build()
    return obj
