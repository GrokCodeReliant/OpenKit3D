"""prop-well-stone - Medium, scales with room. Round stone well with a coping ring, two posts, gabled roof, winch and bucket (M3)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True
MILESTONE = "M3"


def build(name, p):
    R = p.get("radius", 0.62); segs = 12
    b = okit.Builder(name)
    b.lathe([(R - 0.16, 0.0), (R, 0.0), (R, 0.62), (R - 0.16, 0.62)], segs, slot="Secondary", closed=True)   # wall
    for k in range(segs):                                                            # staggered block courses (relief)
        for row, z in enumerate((0.08, 0.34)):
            a = 2 * math.pi * (k + 0.5 * row) / segs
            b.box((0.24, 0.05, 0.2), (R * math.cos(a), R * math.sin(a), z), "Secondary", bevel=0.01,
                  rot=(0, 0, math.degrees(a) + 90))
    b.ring(R - 0.2, R + 0.05, 0.08, segs, (0, 0, 0.62), "Accent")                  # coping
    b.cylinder(R - 0.17, 0.01, segs, (0, 0, 0.3), "Metal")                         # water surface (Metal = wet sheen)
    for sx in (-1, 1):                                                               # posts
        b.box((0.1, 0.1, 1.45), (sx * (R - 0.08), 0, 0.62), "Primary")
    zr = 2.07                                                                        # gabled roof over the posts
    for sy in (-1, 1):
        b.box((2 * R + 0.3, 0.55, 0.04), (0, sy * 0.22, zr - 0.06), "Primary", rot=(sy * -32, 0, 0))
    b.box((2 * R + 0.34, 0.08, 0.08), (0, 0, zr), "Primary")                  # ridge beam
    b.cylinder(0.05, 2 * R - 0.06, 8, (-(R - 0.03), 0, 1.72), "Primary", rot=(0, 90, 0))   # winch drum
    b.cylinder(0.022, 0.2, 6, (R - 0.12, 0, 1.72), "Metal", rot=(0, 90, 0))              # axle through the post
    b.strut((R + 0.07, 0, 1.72), (R + 0.07, 0, 1.52), 0.03, "Metal", bevel=0.0)       # crank arm on the axle end
    b.strut((R + 0.07, 0, 1.52), (R + 0.19, 0, 1.52), 0.03, "Metal", bevel=0.0)       # handle
    b.cylinder(0.01, 0.62, 4, (0, 0, 1.1), "Accent")                                # rope
    b.lathe([(0.0, 0.0), (0.1, 0.0), (0.12, 0.16), (0.105, 0.16), (0.085, 0.02), (0.0, 0.02)], 8,
            loc=(0, 0, 0.94), slot="Primary", cap_bottom=False, cap_top=False)       # bucket
    b.ring(0.11, 0.125, 0.025, 8, (0, 0, 1.06), "Metal")
    obj, _ = b.build()
    return obj
