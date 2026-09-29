"""prop-signpost - Small, scales with room. Crossroads post with three arrow boards and a cap (M3)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"


def arrow(b, z, length, yaw, flip=False):
    L = length; h = 0.16
    pts = [(0.04, -h / 2), (L - 0.12, -h / 2), (L, 0.0), (L - 0.12, h / 2), (0.04, h / 2)]
    if flip:
        pts = [(-u, v) for (u, v) in pts]
    b.prism([(u, v + z) for (u, v) in pts], 0.03, (0, 0, 0), "Primary", axis='Y', rot=(0, 0, yaw))
    nx = (L - 0.2) * (-1 if flip else 1); a = math.radians(yaw)
    b.box((0.03, 0.036, 0.03), (nx * math.cos(a), nx * math.sin(a), z - 0.015), "Metal", bevel=0.0, rot=(0, 0, yaw))   # nail


def build(name, p):
    H = p.get("height", 2.0)
    b = okit.Builder(name)
    b.box((0.1, 0.1, H), (0, 0, 0), "Secondary")                                    # post
    b.cylinder(0.08, 0.08, 4, (0, 0, H), "Secondary", r_top=0.0, phase=0.785398)    # cap
    b.box((0.3, 0.06, 0.06), (0, 0, 0.0), "Secondary")                              # foot braces
    b.box((0.06, 0.3, 0.06), (0, 0, 0.0), "Secondary")
    arrow(b, H - 0.2, 0.7, 0)
    arrow(b, H - 0.45, 0.6, 35, flip=True)
    arrow(b, H - 0.7, 0.55, -60)
    obj, _ = b.build()
    return obj
