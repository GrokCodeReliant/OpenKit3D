"""prop-bucket-wood - Tiny, scales with room. Staved bucket with iron hoops, rope-bail handle and water (M3)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Tiny", 800, True
MILESTONE = "M3"


def build(name, p):
    H = p.get("height", 0.32); rb, rt = 0.13, 0.165; wall = 0.018
    b = okit.Builder(name)
    prof = [(0.0, 0.0), (rb, 0.0), (rt, H), (rt - wall, H), (rb - wall, 0.03), (0.0, 0.03)]
    b.lathe(prof, 10, slot="Primary", cap_bottom=False, cap_top=False)
    for t in (0.12, 0.78):
        r = rb + (rt - rb) * t
        b.ring(r - 0.004, r + 0.01, 0.03, 10, (0, 0, t * H), "Metal")
    b.cylinder(rt - wall - 0.012, 0.01, 10, (0, 0, H * 0.72), "Secondary", caps=True)   # water surface
    pts = []                                                                        # arched bail handle over the rim (X-Z plane)
    for i in range(7):
        a = math.pi * i / 6
        pts.append((rt * math.cos(a), 0.0, H + 0.02 + 0.15 * math.sin(a)))
    for p0, p1 in zip(pts[:-1], pts[1:]):
        b.strut(p0, p1, 0.016, "Metal", bevel=0.0)
    for sx in (-1, 1):
        b.box((0.03, 0.03, 0.05), (sx * (rt + 0.005), 0, H - 0.04), "Metal", bevel=0.0)
    obj, _ = b.build()
    return obj
