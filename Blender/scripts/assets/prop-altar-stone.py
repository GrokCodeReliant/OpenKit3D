"""prop-altar-stone - Medium (environment budget), scales with room. Works as hell or celestial altar via theme."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True


def build(name, p):
    b = okit.Builder(name)
    b.box((1.8, 1.1, 0.15), (0, 0, 0), "Secondary", bevel=0.02)
    b.box((1.5, 0.8, 0.78), (0, 0, 0.15), "Primary", bevel=0.02)
    b.box((1.7, 1.0, 0.12), (0, 0, 0.93), "Secondary", bevel=0.02)
    b.box((0.7, 0.03, 0.42), (0, -0.405, 0.33), "Accent", bevel=0.008)            # front inlay
    b.box((0.2, 0.035, 0.2), (0, -0.42, 0.44), "Metal", bevel=0.006)              # sigil boss
    for sx in (-1, 1):
        b.box((0.12, 0.84, 0.78), (sx * 0.69, 0, 0.15), "Accent", bevel=0.01)       # corner pilasters
    # offering bowl + candles
    b.lathe([(0.0, 1.05), (0.1, 1.06), (0.17, 1.13), (0.19, 1.17), (0.15, 1.17), (0.0, 1.12)], 8, slot="Metal")
    for (x, y) in [(-0.68, 0.3), (0.68, 0.3), (-0.68, -0.3), (0.68, -0.3)]:
        b.cylinder(0.035, 0.16, 6, (x, y, 1.05), "Accent")
        b.flame((x, y, 1.21), 0.1, 0.022, twist=90, segs=4)
    obj, _ = b.build()
    return obj
