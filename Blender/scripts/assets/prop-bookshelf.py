"""prop-bookshelf - Medium, scales with room. Tall open shelf with rows of books (Accent / Secondary / Metal spines) (M3)."""
import random
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 800, True
MILESTONE = "M3"


def build(name, p):
    W = p.get("width", 1.0); D = p.get("depth", 0.34); H = p.get("height", 1.8); t = 0.04
    b = okit.Builder(name)
    for sx in (-1, 1):
        b.box((t, D, H), (sx * (W / 2 - t / 2), 0, 0), "Primary")                  # sides
    b.box((W - 2 * t, 0.02, H - 0.02), (0, D / 2 - 0.01, 0), "Primary", bevel=0.0) # back panel
    b.box((W + 0.04, D + 0.03, 0.05), (0, -0.005, H - 0.0), "Primary")             # crown
    shelves = [0.06, 0.48, 0.92, 1.36]
    for z in shelves:
        b.box((W - 2 * t, D - 0.02, t), (0, -0.01, z - t), "Primary", bevel=0.0)
    rnd = random.Random(11)
    slots = ["Accent", "Secondary", "Accent", "Metal", "Secondary"]
    for si, z in enumerate(shelves):
        x = -W / 2 + t + 0.03
        k = 0
        limit = W / 2 - t - (0.25 if si == 1 else 0.03)
        while x < limit - 0.05:
            bw = rnd.uniform(0.06, 0.1); bh = rnd.uniform(0.24, 0.34); bd = rnd.uniform(0.2, 0.25)
            b.box((bw, bd, bh), (x + bw / 2, -0.03, z), slots[(k + si) % len(slots)], bevel=0.0)
            x += bw + 0.004; k += 1
        if si == 1:                                                                # one book leaning, one lying flat
            b.box((0.05, 0.22, 0.3), (limit - 0.02, -0.03, z), "Accent", bevel=0.0, rot=(0, -22, 0))
            b.box((0.2, 0.24, 0.05), (limit + 0.14, -0.03, z), "Secondary", bevel=0.0)
    obj, _ = b.build()
    return obj
