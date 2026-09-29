"""prop-sarcophagus - Medium (environment budget), scales with room. Carved stone tomb on a plinth, long axis Y."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True


def build(name, p):
    b = okit.Builder(name)
    b.box((1.25, 2.45, 0.2), (0, 0, 0), "Secondary", bevel=0.02)
    b.box((1.0, 2.2, 0.72), (0, 0, 0.2), "Primary", bevel=0.02)
    b.box((1.06, 2.26, 0.08), (0, 0, 0.8), "Accent", bevel=0.01)                  # top band
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.box((0.12, 0.12, 0.72), (sx * 0.49, sy * 1.09, 0.2), "Accent", bevel=0.01)  # corner pilasters
        for y in (-0.55, 0.0, 0.55):
            b.box((0.02, 0.4, 0.36), (sx * 0.505, y, 0.36), "Secondary", bevel=0.005)  # side panels
    b.box((1.14, 2.34, 0.12), (0, 0, 0.88), "Secondary", bevel=0.02)             # lid slab
    # lid: gabled ridge (x/z profile extruded along y)
    b.prism([(-0.5, 0), (0.5, 0), (0.18, 0.16), (-0.18, 0.16)], 2.1, (0, 0, 1.0), "Primary", axis='Y')
    b.box((0.2, 0.2, 0.08), (0, -0.8, 1.16), "Metal", bevel=0.01)                 # seal
    obj, _ = b.build()
    return obj
