"""prop-throne-simple - Medium, scales with room. On a one-step dais."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 800, True


def build(name, p):
    b = okit.Builder(name)
    b.box((1.2, 1.05, 0.15), (0, 0.05, 0), "Secondary", bevel=0.02)                 # dais
    b.box((0.72, 0.62, 0.36), (0, 0, 0.15), "Primary", bevel=0.02)                   # seat block
    b.box((0.6, 0.5, 0.07), (0, -0.03, 0.51), "Accent", bevel=0.02)                  # cushion
    b.box((0.72, 0.14, 1.25), (0, 0.24, 0.51), "Primary", bevel=0.02)                # back
    b.box((0.5, 0.03, 0.8), (0, 0.16, 0.66), "Accent", bevel=0.01)                   # back panel
    b.prism([(-0.36, 0), (0.36, 0), (0, 0.28)], 0.14, (0, 0.24, 1.76), "Accent", axis='Y')   # pointed crest
    for sx in (-1, 1):
        b.box((0.1, 0.6, 0.3), (sx * 0.41, -0.01, 0.51), "Primary", bevel=0.015)    # armrests
        b.box((0.12, 0.12, 0.34), (sx * 0.41, -0.29, 0.15), "Primary", bevel=0.015)  # front posts
        b.lathe([(0.0, 0.0), (0.05, 0.02), (0.06, 0.07), (0.03, 0.12), (0.0, 0.14)], 6,
                loc=(sx * 0.3, 0.24, 1.76), slot="Metal")                           # finials
        b.lathe([(0.0, 0.0), (0.045, 0.02), (0.05, 0.06), (0.0, 0.1)], 6, loc=(sx * 0.41, -0.29, 0.81), slot="Metal")
    obj, _ = b.build()
    return obj
