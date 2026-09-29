"""prop-brazier - Small, scales with room. Layered, twisted Emissive flame tongues; Unity adds a point light at LIGHT_SOCKET."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
LIGHT_SOCKET = [0.0, 0.0, 1.15]   # metres, Blender Z-up


def build(name, p):
    segs = p.get("segments", 8)
    b = okit.Builder(name)
    bowl = [(0.0, 0.66), (0.12, 0.68), (0.29, 0.80), (0.34, 0.94), (0.30, 0.95), (0.25, 0.86), (0.0, 0.82)]
    b.lathe(bowl, segs, slot="Metal")
    b.ring(0.335, 0.365, 0.035, segs, (0, 0, 0.915), "Accent")
    b.lathe([(0.26, 0.85), (0.17, 0.90), (0.0, 0.92)], segs, slot="Secondary")          # coals
    for i in range(3):
        a = math.radians(90 + 120 * i)
        top = (0.12 * math.cos(a), 0.12 * math.sin(a), 0.72)
        foot = (0.32 * math.cos(a), 0.32 * math.sin(a), 0.0)
        b.strut((foot[0], foot[1], 0.03), top, 0.045, "Primary")          # legs: Primary colour slot
        b.box((0.09, 0.09, 0.03), foot, "Primary", bevel=0.006)
    b.ring(0.19, 0.22, 0.03, 8, (0, 0, 0.30), "Metal")
    # flames: one fat teardrop body + curling side tongues + small licks. Rounded profiles (bulge low, soft taper)
    # read as fire rather than crystals; all Emissive so the theme colours them.
    z0 = 0.845
    body = ((0.0, 0.75), (0.16, 1.0), (0.38, 0.92), (0.62, 0.58), (0.84, 0.24))
    tongue = ((0.0, 0.8), (0.2, 1.0), (0.48, 0.75), (0.76, 0.32))
    lick = ((0.0, 0.9), (0.35, 0.8), (0.7, 0.3))
    b.flame((0, 0, z0), 0.46, 0.15, segs=6, twist=45, lean=(0.03, -0.02), phase=0.2, profile=body)
    for i in range(3):
        a = math.radians(40 + 120 * i)
        b.flame((0.11 * math.cos(a), 0.11 * math.sin(a), z0), 0.30, 0.085, segs=5, twist=-60,
                lean=(0.09 * math.cos(a + 0.7), 0.09 * math.sin(a + 0.7)), phase=a, profile=tongue)
    for i in range(3):
        a = math.radians(100 + 120 * i)
        b.flame((0.19 * math.cos(a), 0.19 * math.sin(a), z0 - 0.01), 0.17, 0.06, segs=4, twist=50,
                lean=(0.06 * math.cos(a), 0.06 * math.sin(a)), phase=a, profile=lick)
    obj, _ = b.build()
    return obj
