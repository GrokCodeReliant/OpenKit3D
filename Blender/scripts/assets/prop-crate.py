"""prop-crate - Small, scales with room. 0.7 m slatted crate with braces."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True


def build(name, p):
    S = p.get("size", 0.7); t = p.get("frame", 0.07)
    b = okit.Builder(name)
    h = S / 2
    b.box((S - 0.04, S - 0.04, S - 0.04), (0, 0, 0.02), "Secondary")               # boards
    for sx in (-1, 1):                                                             # 4 vertical posts
        for sy in (-1, 1):
            b.box((t, t, S), (sx * (h - t / 2), sy * (h - t / 2), 0), "Primary")
    for z in (0, S - t):                                                           # top/bottom rails
        for sy in (-1, 1):
            b.box((S - 2 * t, t, t), (0, sy * (h - t / 2), z), "Primary")
        for sx in (-1, 1):
            b.box((t, S - 2 * t, t), (sx * (h - t / 2), 0, z), "Primary")
    for sy in (-1, 1):                                                             # diagonal braces front/back
        y = sy * (h - 0.005)
        b.strut((-h + t, y, t), (h - t, y, S - t), 0.06, "Accent")   # braces: Tertiary colour slot
    obj, _ = b.build()
    return obj
