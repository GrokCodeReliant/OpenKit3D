"""prop-barrel - Small, scales with room."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True


def build(name, p):
    H = p.get("height", 0.90); r_end = p.get("r_end", 0.25); r_mid = p.get("r_mid", 0.31)
    segs = p.get("segments", 12)
    b = okit.Builder(name)

    def r_at(z):  # parabolic bulge
        t = z / H * 2 - 1
        return r_end + (r_mid - r_end) * (1 - t * t)

    zs = [0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9]
    zs = [z * H / 0.9 for z in zs]
    lip = 0.035
    prof = [(r_at(z), z) for z in zs] + [(r_end - lip, H), (r_end - lip, H - 0.04)]
    b.lathe(prof, segs, slot="Primary", cap_top=False)
    b.cylinder(r_end - lip + 0.001, 0.01, segs, (0, 0, H - 0.045), "Secondary")  # lid
    for z in p.get("hoops", [0.07, 0.27, 0.59, 0.79]):
        z = z * H / 0.9; h = 0.045
        r = max(r_at(z), r_at(z + h))
        b.ring(r - 0.01, r + 0.012, h, segs, (0, 0, z), "Metal")
    obj, _ = b.build()
    return obj
