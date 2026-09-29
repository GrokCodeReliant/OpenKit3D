"""prop-banner-standing - Small, scales with room. Free-standing banner: tripod feet, pole with finial, crossbar,
swallow-tailed cloth with a metal emblem (M3)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"


def build(name, p):
    H = p.get("height", 2.2)
    b = okit.Builder(name)
    for i in range(3):                                                               # tripod feet
        a = math.radians(90 + 120 * i)
        b.strut((0.3 * math.cos(a), 0.3 * math.sin(a), 0.0), (0, 0, 0.45), 0.04, "Primary")
    b.cylinder(0.025, H, 6, (0, 0, 0), "Primary")                                    # pole
    b.gem(0.05, 0.14, (0, 0, H), "Metal", segs=4)                                    # finial
    top = H - 0.12
    b.cylinder(0.018, 0.8, 6, (-0.4, 0, top), "Primary", rot=(0, 90, 0))              # crossbar
    for sx in (-1, 1):
        b.gem(0.028, 0.06, (sx * 0.4, 0, top), "Metal", segs=4, rot=(0, sx * 90, 0))
    w = 0.34; bz = top - 1.1                                                         # cloth hangs in front of the pole
    cloth = [(-w, top - 0.02), (w, top - 0.02), (w, bz), (0.0, bz + 0.2), (-w, bz)]
    b.prism(cloth, 0.02, (0, -0.04, 0), "Accent", axis='Y')
    b.prism([(-w, top - 0.02), (w, top - 0.02), (w, top - 0.12), (-w, top - 0.12)], 0.028, (0, -0.04, 0), "Secondary", axis='Y')  # hem
    b.gem(0.11, 0.07, (0, -0.05, top - 0.55), "Metal", segs=4, rot=(90, 0, 0))       # emblem (diamond boss, pointing out)
    obj, _ = b.build()
    return obj
