"""prop-pew-bench - Medium, scales with room. 1.8 m church pew; front (knees) faces -Y."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 800, True


def build(name, p):
    W = p.get("width", 1.8)
    b = okit.Builder(name)
    b.box((W - 0.1, 0.42, 0.05), (0, 0.0, 0.42), "Primary")                        # seat
    b.box((W - 0.1, 0.04, 0.5), (0, 0.23, 0.5), "Primary", rot=(-8, 0, 0))        # back
    b.box((W - 0.1, 0.06, 0.08), (0, 0.25, 0.98), "Accent", rot=(-8, 0, 0))       # top rail
    b.box((W - 0.1, 0.05, 0.05), (0, 0.1, 0.12), "Primary")                        # stretcher
    # end panels (side profile in x/z plane extruded along x): foot, seat, armrest scroll, back
    prof = [(-0.26, 0.0), (0.3, 0.0), (0.3, 1.05), (0.2, 1.08), (0.18, 0.62), (-0.2, 0.62), (-0.26, 0.55)]
    for sx in (-1, 1):
        # prism axis 'X' uses (y, z) points and extrudes along x
        b.prism(prof, 0.06, (sx * (W / 2 - 0.03), 0, 0), "Secondary", axis='X')
    obj, _ = b.build()
    return obj
