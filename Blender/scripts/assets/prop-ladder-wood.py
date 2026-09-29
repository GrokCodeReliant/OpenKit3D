"""prop-ladder-wood - Small, scales with room. 2.4 m wooden ladder, authored upright (lean it on a wall in the scene) (M3)."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"


def build(name, p):
    H = p.get("height", 2.4); W = p.get("width", 0.46); n = p.get("rungs", 8)
    b = okit.Builder(name)
    for sx in (-1, 1):
        b.box((0.06, 0.08, H), (sx * W / 2, 0, 0), "Primary")                        # rails
    step = H / (n + 1)
    for i in range(n):
        z = step * (i + 1)
        b.cylinder(0.02, W, 6, (-W / 2, 0, z), "Secondary", rot=(0, 90, 0))          # rungs
    for sx in (-1, 1):
        for z in (step, H - step):
            b.box((0.07, 0.09, 0.03), (sx * W / 2, 0, z - 0.015), "Metal", bevel=0.0)   # iron bands at the end rungs
    obj, _ = b.build()
    return obj
