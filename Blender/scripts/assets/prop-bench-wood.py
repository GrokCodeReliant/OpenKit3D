"""prop-bench-wood - Small, scales with room. Backless tavern bench: two-plank seat on splayed legs (M3)."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"


def build(name, p):
    W = p.get("width", 1.30); D = p.get("depth", 0.32); H = p.get("height", 0.45); T = 0.05
    b = okit.Builder(name)
    for sy in (-1, 1):                                                             # two seat planks
        b.box((W, D / 2 - 0.005, T), (0, sy * D / 4, H - T), "Primary")
    for sx in (-1, 1):                                                             # splayed leg pairs + foot rail
        x = sx * (W / 2 - 0.16)
        for sy in (-1, 1):
            b.strut((x + sx * 0.05, sy * (D / 2 - 0.02), 0.0), (x, sy * (D / 2 - 0.07), H - T), 0.055, "Secondary")
        b.box((0.05, D - 0.06, 0.05), (x + sx * 0.02, 0, 0.12), "Secondary")
    b.box((W - 0.36, 0.05, 0.06), (0, 0, H - T - 0.06), "Secondary")              # long under-rail
    for sx in (-1, 1):                                                             # iron nail plates
        b.box((0.07, D - 0.04, 0.008), (sx * (W / 2 - 0.16), 0, H), "Metal", bevel=0.0)
    obj, _ = b.build()
    return obj
