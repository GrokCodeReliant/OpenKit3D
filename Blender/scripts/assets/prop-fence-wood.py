"""prop-fence-wood - Medium, structural (scales with the room grid). One 1.5 m fence section along X: two posts, two rails,
pointed pickets. Snaps to grid cell edges; posts sit at the section ends so sections chain (M3)."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True
ROOM_SCALE = "grid"   # structural: scales with the room size class and snaps to the room grid (cell = 1.5 m x room scale)
MILESTONE = "M3"


def build(name, p):
    L = okit.GRID; H = p.get("height", 1.0); post = 0.1
    b = okit.Builder(name)
    for sx in (-1, 1):                                                            # end posts (centred on the section ends -> overlap when chained)
        x = sx * (L / 2 - post / 2)
        b.box((post, post, H + 0.1), (x, 0, 0), "Secondary")
        b.cylinder(0.065, 0.06, 4, (x, 0, H + 0.1), "Secondary", r_top=0.0, phase=0.785398)   # pyramid cap
    for z in (0.25, H - 0.25):                                                    # rails (behind the pickets, +Y)
        b.box((L - 2 * post, 0.04, 0.08), (0, 0.035, z), "Primary")
    n = 7; gap = (L - 2 * post) / n
    for i in range(n):                                                            # pickets with pointed tops
        x = -L / 2 + post + gap * (i + 0.5)
        pw = gap * 0.72; ph = H - 0.08 + (0.04 if i % 2 else 0.0)
        b.prism([(x - pw / 2, 0.0), (x + pw / 2, 0.0), (x + pw / 2, ph), (x, ph + 0.09), (x - pw / 2, ph)], 0.03,
                (0, -0.0, 0), "Primary", axis='Y')
    for z in (0.25, H - 0.25):                                                    # nail heads
        for i in (0, n - 1):
            x = -L / 2 + post + gap * (i + 0.5)
            b.box((0.02, 0.01, 0.02), (x, -0.02, z + 0.03), "Metal", bevel=0.0)
    obj, _ = b.build()
    return obj
