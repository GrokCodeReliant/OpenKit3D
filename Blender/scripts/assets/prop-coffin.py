"""prop-coffin - Medium, scales with room. Classic six-sided coffin, head toward +Y (back), lid cross."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 800, True


def build(name, p):
    b = okit.Builder(name)
    shape = [(-0.22, 1.0), (-0.33, 0.55), (-0.2, -1.0), (0.2, -1.0), (0.33, 0.55), (0.22, 1.0)]
    b.prism(list(reversed(shape)), 0.40, (0, 0, 0), "Primary")
    lid = [(x * 1.07, y * 1.02) for (x, y) in shape]
    b.prism(list(reversed(lid)), 0.07, (0, 0, 0.40), "Secondary")
    b.box((0.08, 1.1, 0.025), (0, 0.05, 0.47), "Accent", bevel=0.006)             # cross upright
    b.box((0.4, 0.08, 0.025), (0, 0.4, 0.47), "Accent", bevel=0.006)              # cross bar
    for y in (-0.6, 0.0, 0.5):                                                    # handles
        for sx in (-1, 1):
            w = 0.2 + 0.13 * (0.55 - abs(y - 0.55)) / 1.55
            x = sx * (0.2 + (0.13 * (y + 1.0) / 1.55 if y < 0.55 else 0.13))
            b.box((0.04, 0.14, 0.03), (x + sx * 0.02, y, 0.22), "Metal", bevel=0.004)
    obj, _ = b.build()
    return obj
