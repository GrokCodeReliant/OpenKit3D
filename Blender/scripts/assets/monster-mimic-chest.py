"""monster-mimic-chest - Medium, scales with the room. Rigid-part mimic (M4): a treasure chest whose lid rests ~25 degrees open on
a back hinge, showing rows of teeth, a dark mouth and a tongue; glowing eyes peer from the lid front; four stubby legs underneath.
Clips: idle (chomping lid, tongue waggle, body bob) and walk (scuttle, body rock).
Slots: Primary = wood planks, Secondary = mouth / dark wood trim / tongue, Metal = iron bands, corner caps and lock plate,
Accent = teeth, Emissive = eyes."""
import math
from mathutils import Matrix, Vector
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True
CATEGORY = "Monsters"
MILESTONE = "M4"
EMISSIVE_SCALE = 0.7

W, D, HB, LEG = 0.9, 0.56, 0.32, 0.09
ZB = LEG + HB                  # top of the body (rim / hinge height)
DOME = 0.18                    # lid height when closed
OPEN = -25.0                   # rest opening (degrees about X at the hinge; negative lifts the front)
HINGE = Vector((0, D / 2, ZB))
LEGS = {"fl": (-1, -1), "fr": (1, -1), "bl": (-1, 1), "br": (1, 1)}

RIG = [
    {"name": "root", "head": (0, 0, LEG + 0.02), "tail": (0, 0, ZB - 0.05)},
    {"name": "lid", "head": tuple(HINGE), "tail": (0, -D / 2, ZB), "parent": "root"},
    {"name": "tongue", "head": (0, 0.06, ZB - 0.02), "tail": (0, -0.2, ZB + 0.02), "parent": "root"},
]
for _k, (_sx, _sy) in LEGS.items():
    RIG.append({"name": f"leg_{_k}", "head": (_sx * (W / 2 - 0.1), _sy * (D / 2 - 0.1), LEG + 0.03),
                "tail": (_sx * (W / 2 - 0.1), _sy * (D / 2 - 0.1), 0.0), "parent": "root"})

CLIPS = {
    "idle": {"frames": 48, "channels": [
        ("lid", "rx", 10, 2, 0), ("tongue", "rz", 16, 2, 90), ("tongue", "rx", 6, 2, 0), ("root", "ly", 0.008, 2, 180)]},
    "walk": {"frames": 24, "channels": [
        ("root", "ly", 0.012, 2, 0), ("root", "rz", 3, 1, 0), ("lid", "rx", 6, 2, 45),
        ("leg_fl", "rx", 25, 1, 0), ("leg_br", "rx", 25, 1, 0), ("leg_fr", "rx", 25, 1, 180), ("leg_bl", "rx", 25, 1, 180)]},
}

R = Matrix.Rotation(math.radians(OPEN), 4, 'X')


def lid_loc(p):
    """Closed-lid point -> rest (open) position."""
    return tuple(HINGE + (R @ (Vector(p) - HINGE)))


def dome(r, h, n=6):
    return [(r * math.cos(math.pi * i / n), h * math.sin(math.pi * i / n)) for i in range(n + 1)]


def build(name, p):
    b = okit.Builder(name)
    rot = (OPEN, 0, 0)
    with b.bone("root"):
        b.box((W, D, HB), (0, 0, LEG), "Primary")                                        # body
        b.box((W - 0.07, D - 0.07, 0.03), (0, 0, ZB - 0.02), "Secondary", bevel=0.0)      # dark mouth floor
        b.box((W + 0.02, D + 0.02, 0.04), (0, 0, LEG), "Secondary", bevel=0.006)          # dark plinth trim
        for x in (-W / 2 + 0.1, 0, W / 2 - 0.1):
            b.box((0.05, D + 0.02, HB - 0.01), (x, 0, LEG), "Metal", bevel=0.005)        # iron bands
        b.box((0.13, 0.03, 0.13), (0, -D / 2 - 0.012, ZB - 0.15), "Metal", bevel=0.006)   # lock plate
        for sx in (-1, 1):
            for sy in (-1, 1):
                b.box((0.07, 0.07, 0.07), (sx * (W / 2 - 0.02), sy * (D / 2 - 0.02), ZB - 0.07), "Metal", bevel=0.006)   # corner caps
        # lower teeth along the front and side rims
        for i in range(7):
            x = -0.33 + i * 0.11
            b.prism([(-0.025, 0.0), (0.025, 0.0), (0.0, 0.07)], 0.02, (x, -D / 2 + 0.05, ZB), "Accent", axis='Y')
        for sx in (-1, 1):
            for j in range(3):
                b.prism([(-0.022, 0.0), (0.022, 0.0), (0.0, 0.055)], 0.02, (sx * (W / 2 - 0.05), -0.13 + j * 0.12, ZB), "Accent", axis='X')
    with b.bone("tongue"):
        b.box((0.16, 0.3, 0.04), (0, -0.07, ZB - 0.01), "Secondary", bevel=0.015, rot=(-6, 0, 0))
        b.box((0.12, 0.08, 0.035), (0, -0.25, ZB + 0.01), "Secondary", bevel=0.012)
    with b.bone("lid"):
        r = D / 2
        b.prism(dome(r, DOME), W - 0.02, lid_loc((0, 0, ZB)), "Primary", axis='X', rot=rot)                 # domed lid
        b.box((W - 0.06, D - 0.06, 0.02), lid_loc((0, 0, ZB - 0.021)), "Secondary", bevel=0.0, rot=rot)     # inner lid (dark)
        for x in (-W / 2 + 0.1, 0, W / 2 - 0.1):
            b.prism(dome(r + 0.012, DOME + 0.012), 0.05, lid_loc((x, 0, ZB)), "Metal", axis='X', rot=rot)   # lid bands
        for i in range(6):
            x = -0.275 + i * 0.11
            b.prism([(-0.025, 0.0), (0.025, 0.0), (0.0, -0.07)], 0.02, lid_loc((x, -D / 2 + 0.05, ZB - 0.02)), "Accent", axis='Y', rot=rot)  # upper fangs
        for sx in (-1, 1):
            b.box((0.07, 0.03, 0.04), lid_loc((sx * 0.15, -D / 2 - 0.004, ZB + 0.05)), "Emissive", bevel=0.0, rot=rot)       # eyes
            b.box((0.1, 0.035, 0.02), lid_loc((sx * 0.15, -D / 2 - 0.004, ZB + 0.095)), "Secondary", bevel=0.0, rot=(OPEN, 0, sx * 12))  # brow
        b.box((0.05, 0.03, 0.06), lid_loc((0, -D / 2 - 0.02, ZB - 0.03)), "Metal", bevel=0.004, rot=rot)                  # hasp
    for k, (sx, sy) in LEGS.items():
        with b.bone(f"leg_{k}"):
            x, y = sx * (W / 2 - 0.1), sy * (D / 2 - 0.1)
            b.cylinder(0.045, LEG + 0.01, 6, (x, y, 0.02), "Secondary", r_top=0.035)
            b.box((0.1, 0.12, 0.03), (x + sx * 0.01, y - 0.02, 0.0), "Primary", bevel=0.008)   # clawed foot
            b.box((0.09, 0.025, 0.025), (x + sx * 0.01, y - 0.085, 0.0), "Accent", bevel=0.0)  # claws
    obj, _ = b.build()
    return obj
