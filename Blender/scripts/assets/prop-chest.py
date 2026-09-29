"""prop-chest - Small, scales with room. Domed lid, metal bands, lock (reused by the M3 mimic)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True


def arc(r, n, cx=0.0, cz=0.0):
    return [(cx + r * math.cos(math.pi * i / n), cz + r * math.sin(math.pi * i / n)) for i in range(n + 1)]


def build(name, p):
    W = p.get("width", 0.9); D = p.get("depth", 0.55); H = p.get("body_height", 0.4)
    b = okit.Builder(name)
    b.box((W, D, H), (0, 0, 0), "Primary")
    r = D / 2
    b.prism(arc(r, 6, 0, 0), W - 0.02, (0, 0, H), "Primary", axis='X')            # domed lid (x-extruded half disc)
    b.box((W + 0.02, D + 0.02, 0.035), (0, 0, H - 0.02), "Secondary", bevel=0.006) # lid seam trim: Secondary colour slot
    for x in (-W / 2 + 0.1, 0, W / 2 - 0.1):
        b.box((0.05, D + 0.02, H), (x, 0, 0), "Metal", bevel=0.005)
        b.prism(arc(r + 0.012, 6), 0.05, (x, 0, H), "Metal", axis='X')
    b.box((0.12, 0.03, 0.14), (0, -D / 2 - 0.012, H - 0.12), "Accent", bevel=0.006)   # lock plate
    b.box((0.03, 0.03, 0.05), (0, -D / 2 - 0.03, H - 0.09), "Metal", bevel=0.004)     # hasp
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.box((0.08, 0.08, 0.03), (sx * (W / 2 - 0.05), sy * (D / 2 - 0.05), -0.0), "Metal", bevel=0.005)
    obj, _ = b.build()
    return obj
