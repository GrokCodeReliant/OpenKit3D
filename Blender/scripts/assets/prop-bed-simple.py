"""prop-bed-simple - Medium, scales with room. Single wooden bed: posts, head/foot boards, mattress, pillow, blanket (M3)."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 800, True
MILESTONE = "M3"


def build(name, p):
    W = p.get("width", 1.0); L = p.get("length", 2.0)
    b = okit.Builder(name)
    post = 0.08
    hx, hy = W / 2 - post / 2, L / 2 - post / 2
    for sy, ph in ((1, 1.0), (-1, 0.7)):                                           # head (+Y back) posts taller than foot posts
        for sx in (-1, 1):
            b.box((post, post, ph), (sx * hx, sy * hy, 0), "Primary")
    b.box((W - 2 * post, 0.05, 0.55), (0, hy, 0.30), "Primary")                    # headboard
    b.box((W - 2 * post, 0.05, 0.28), (0, -hy, 0.30), "Primary")                   # footboard
    for sx in (-1, 1):
        b.box((0.05, L - 2 * post, 0.14), (sx * hx, 0, 0.22), "Primary")           # side rails
    b.box((W - 0.14, L - 0.18, 0.16), (0, 0, 0.30), "Secondary", bevel=0.03)       # mattress
    b.box((W - 0.34, 0.34, 0.1), (0, hy - 0.25, 0.46), "Secondary", bevel=0.035)   # pillow
    b.box((W - 0.10, L * 0.58, 0.05), (0, -L * 0.17, 0.44), "Accent", bevel=0.02)  # blanket
    b.box((W - 0.10, 0.12, 0.06), (0, -L * 0.17 + L * 0.29 - 0.06, 0.45), "Accent", bevel=0.02)   # blanket fold
    obj, _ = b.build()
    return obj
