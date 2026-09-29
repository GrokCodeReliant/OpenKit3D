"""monster-golem-stone - Large, scales with the room. Rigid-part stone golem (M4): every block is bound to one bone (no skin blending),
so it animates like a jointed statue. Idle: slow breathing heave, head turn, arm sway. Walk: heavy stomp.
Slots: Primary = dressed stone blocks, Secondary = dark joint stone, Accent = moss / carved rune bands, Metal = iron wrist and
ankle bands, Emissive = eyes + chest rune."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Large", 5000, True
CATEGORY = "Monsters"
MILESTONE = "M4"
EMISSIVE_SCALE = 0.7

RIG = [
    {"name": "root", "head": (0, 0, 1.05), "tail": (0, 0, 1.3)},
    {"name": "torso", "head": (0, 0, 1.3), "tail": (0, 0, 2.1), "parent": "root"},
    {"name": "head", "head": (0, -0.18, 2.36), "tail": (0, -0.18, 2.76), "parent": "torso"},
    {"name": "arm_l", "head": (-0.98, 0, 2.05), "tail": (-0.98, 0, 1.45), "parent": "torso"},
    {"name": "fore_l", "head": (-0.98, 0, 1.45), "tail": (-0.98, 0, 0.5), "parent": "arm_l"},
    {"name": "arm_r", "head": (0.98, 0, 2.05), "tail": (0.98, 0, 1.45), "parent": "torso"},
    {"name": "fore_r", "head": (0.98, 0, 1.45), "tail": (0.98, 0, 0.5), "parent": "arm_r"},
    {"name": "leg_l", "head": (-0.36, 0, 1.05), "tail": (-0.36, 0, 0.55), "parent": "root"},
    {"name": "shin_l", "head": (-0.36, 0, 0.55), "tail": (-0.36, 0, 0.05), "parent": "leg_l"},
    {"name": "leg_r", "head": (0.36, 0, 1.05), "tail": (0.36, 0, 0.55), "parent": "root"},
    {"name": "shin_r", "head": (0.36, 0, 0.55), "tail": (0.36, 0, 0.05), "parent": "leg_r"},
]
CLIPS = {
    "idle": {"frames": 72, "channels": [
        ("torso", "ly", 0.025, 1, 0), ("torso", "rx", 1.5, 1, 90), ("head", "ry", 12, 1, 0), ("head", "rx", 3, 2, 45),
        ("arm_l", "rx", 4, 1, 0), ("arm_r", "rx", 4, 1, 180), ("fore_l", "rx", -3, 1, 30), ("fore_r", "rx", -3, 1, 210)]},
    "walk": {"frames": 40, "channels": [
        ("root", "ly", 0.03, 2, 90), ("torso", "ry", 5, 1, 0),
        ("leg_l", "rx", 20, 1, 0), ("leg_r", "rx", 20, 1, 180), ("shin_l", "rx", -12, 1, 60), ("shin_r", "rx", -12, 1, 240),
        ("arm_l", "rx", 14, 1, 180), ("arm_r", "rx", 14, 1, 0)]},
}


def build(name, p):
    b = okit.Builder(name)
    with b.bone("root"):
        b.box((0.95, 0.6, 0.34), (0, 0.02, 1.02), "Secondary")                          # pelvis
        b.box((0.6, 0.5, 0.2), (0, 0.02, 1.3), "Secondary", bevel=0.03)                # waist joint
    with b.bone("torso"):
        b.box((1.45, 0.85, 0.72), (0, 0.04, 1.42), "Primary", bevel=0.05)              # chest block
        b.box((1.25, 0.75, 0.3), (0, 0.06, 2.1), "Primary", bevel=0.05)                # upper chest / shoulder shelf
        for sx in (-1, 1):
            b.broken_shaft(0.3, 0.4, segs=7, jag=0.06, seed=3 + sx, loc=(sx * 0.82, 0.02, 1.9), slot="Primary", r_top=0.24)   # shoulder boulders
            b.box((0.3, 0.12, 0.2), (sx * 0.45, 0.47, 1.62), "Accent", bevel=0.02)     # moss on the back
        b.box((1.0, 0.08, 0.12), (0, -0.39, 1.95), "Accent", bevel=0.02)               # carved rune band
        b.box((0.26, 0.06, 0.26), (0, -0.40, 1.6), "Emissive", bevel=0.0)              # chest rune core
        b.box((0.4, 0.06, 0.4), (0, -0.37, 1.53), "Secondary", bevel=0.02)             # rune socket
    with b.bone("head"):
        b.box((0.46, 0.44, 0.38), (0, -0.2, 2.38), "Primary", bevel=0.04)
        b.box((0.52, 0.2, 0.1), (0, -0.28, 2.66), "Secondary", bevel=0.02)              # brow ridge
        for sx in (-1, 1):
            b.box((0.1, 0.04, 0.06), (sx * 0.11, -0.43, 2.54), "Emissive", bevel=0.0)  # eyes
        b.box((0.2, 0.05, 0.08), (0, -0.43, 2.42), "Accent", bevel=0.0)                # carved mouth rune
    for sx, side in ((-1, "l"), (1, "r")):
        with b.bone(f"arm_{side}"):
            b.box((0.42, 0.42, 0.62), (sx * 0.98, 0, 1.42), "Primary", bevel=0.04)     # upper arm
        with b.bone(f"fore_{side}"):
            b.box((0.3, 0.3, 0.14), (sx * 0.98, 0, 1.33), "Secondary", bevel=0.02)     # elbow joint
            b.box((0.46, 0.46, 0.5), (sx * 0.98, -0.02, 0.86), "Primary", bevel=0.04)  # forearm
            b.ring(0.235, 0.27, 0.1, 8, (sx * 0.98, -0.02, 0.8), "Metal")              # iron wrist band
            b.box((0.58, 0.56, 0.44), (sx * 0.98, -0.05, 0.42), "Primary", bevel=0.05) # fist
            b.box((0.5, 0.1, 0.1), (sx * 0.98, -0.34, 0.6), "Secondary", bevel=0.02)   # knuckle ridge
        with b.bone(f"leg_{side}"):
            b.box((0.44, 0.44, 0.5), (sx * 0.36, 0, 0.58), "Primary", bevel=0.04)      # thigh
        with b.bone(f"shin_{side}"):
            b.box((0.4, 0.4, 0.42), (sx * 0.36, 0, 0.16), "Primary", bevel=0.04)       # shin
            b.ring(0.21, 0.25, 0.08, 8, (sx * 0.36, 0, 0.26), "Metal")                 # ankle band
            b.box((0.5, 0.66, 0.18), (sx * 0.36, -0.08, 0.0), "Secondary", bevel=0.04) # foot
            b.box((0.16, 0.12, 0.1), (sx * 0.36 + sx * 0.12, -0.36, 0.14), "Accent", bevel=0.01)   # moss on the toe
    obj, _ = b.build()
    return obj
