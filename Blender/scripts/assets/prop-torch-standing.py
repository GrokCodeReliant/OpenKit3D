"""prop-torch-standing - Small, scales with room. Free-standing torch post: stone footing, wooden pole, iron cage with flames + light (M3)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"
LIGHT_SOCKET = [0.0, 0.0, 1.78]


def build(name, p):
    H = p.get("height", 1.55)
    b = okit.Builder(name)
    b.cylinder(0.24, 0.14, 8, (0, 0, 0), "Secondary", r_top=0.2, bevel=0.012)     # stone footing
    b.cylinder(0.05, H - 0.14, 6, (0, 0, 0.14), "Primary", r_top=0.04)            # pole
    b.ring(0.05, 0.065, 0.05, 6, (0, 0, 0.5), "Metal")                            # iron collars
    b.ring(0.042, 0.058, 0.05, 6, (0, 0, H - 0.08), "Metal")
    cz = H - 0.03
    b.cylinder(0.05, 0.03, 6, (0, 0, cz), "Metal", r_top=0.1)                     # cage floor
    for i in range(6):                                                            # cage bars
        a = math.radians(60 * i + 30)
        b.strut((0.09 * math.cos(a), 0.09 * math.sin(a), cz + 0.02), (0.14 * math.cos(a), 0.14 * math.sin(a), cz + 0.22),
                0.018, "Metal", bevel=0.0)
    b.ring(0.13, 0.15, 0.025, 6, (0, 0, cz + 0.2), "Metal")
    b.lathe([(0.1, cz + 0.03), (0.07, cz + 0.1), (0.0, cz + 0.12)], 6, slot="Secondary")   # pitch-soaked rags
    body = ((0.0, 0.75), (0.16, 1.0), (0.38, 0.92), (0.62, 0.58), (0.84, 0.24))
    b.flame((0, 0, cz + 0.08), 0.36, 0.1, segs=6, twist=50, lean=(0.02, -0.02), phase=0.3, profile=body)
    for i in range(3):
        a = math.radians(30 + 120 * i)
        b.flame((0.06 * math.cos(a), 0.06 * math.sin(a), cz + 0.08), 0.22, 0.05, segs=4, twist=-70,
                lean=(0.05 * math.cos(a + 0.6), 0.05 * math.sin(a + 0.6)), phase=a)
    obj, _ = b.build()
    return obj
