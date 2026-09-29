"""prop-lectern - Small, scales with room. Reading stand: stepped base, turned column, slanted desk with an open book (M3)."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"


def build(name, p):
    b = okit.Builder(name)
    b.box((0.5, 0.42, 0.06), (0, 0, 0), "Secondary")                                # base steps
    b.box((0.36, 0.3, 0.05), (0, 0, 0.06), "Secondary")
    b.lathe([(0.07, 0.11), (0.05, 0.2), (0.045, 0.7), (0.06, 0.8), (0.05, 0.9), (0.0, 0.9)], 8, slot="Primary")   # column
    desk = [(-0.2, 0.0), (0.2, 0.0), (0.2, 0.2), (-0.2, 0.05)]                       # wedge (y, z) profile: high at the back (+Y)
    b.prism(desk, 0.55, (0, 0, 0.88), "Primary", axis='X')
    b.box((0.56, 0.03, 0.04), (0, -0.21, 0.92), "Primary", bevel=0.0, rot=(0, 0, 0))    # book ledge
    # open book lying on the slope (rotated to match the desk: rise 0.15 over 0.4 -> ~20.6 deg)
    for sx in (-1, 1):
        b.box((0.2, 0.28, 0.025), (sx * 0.105, 0.0, 1.008), "Accent", bevel=0.004, rot=(20.6, 0, 0))   # pages
        b.box((0.21, 0.29, 0.008), (sx * 0.105, 0.0, 1.0), "Secondary", bevel=0.0, rot=(20.6, 0, 0))  # cover
    obj, _ = b.build()
    return obj
