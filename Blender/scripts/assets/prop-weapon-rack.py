"""prop-weapon-rack - Medium, scales with room. Standing rack: two uprights, notched cross bars, three spears and two swords (M3)."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 800, True
MILESTONE = "M3"


def build(name, p):
    W = p.get("width", 1.2); H = p.get("height", 1.5)
    b = okit.Builder(name)
    for sx in (-1, 1):
        x = sx * (W / 2 - 0.04)
        b.box((0.07, 0.07, H), (x, 0, 0), "Primary")                               # upright
        b.box((0.08, 0.5, 0.07), (x, 0, 0), "Primary")                             # foot
    b.box((W, 0.06, 0.07), (0, 0.0, 1.05), "Primary")                               # top bar (spears rest)
    b.box((W - 0.1, 0.12, 0.05), (0, 0.0, 0.12), "Primary")                         # base tray for spear butts
    for i, x in enumerate((-0.4, -0.25, -0.1)):                                    # spears leaning back
        top = (x, 0.07, 1.62 + 0.04 * i)
        b.strut((x, -0.03, 0.17), top, 0.028, "Secondary", segs=6)
        b.gem(0.035, 0.16, (top[0], top[1] + 0.0, top[2] - 0.01), "Metal", segs=4)
    for x in (0.18, 0.38):                                                         # swords hanging point-down from the top bar
        z0 = 0.2
        b.prism([(x - 0.03, z0 + 0.08), (x, z0), (x + 0.03, z0 + 0.08), (x + 0.03, 0.95), (x - 0.03, 0.95)], 0.012,
                (0, -0.05, 0), "Metal", axis='Y')                                  # blade
        b.box((0.18, 0.04, 0.03), (x, -0.05, 0.95), "Accent", bevel=0.006)          # cross guard
        b.box((0.032, 0.032, 0.14), (x, -0.05, 0.98), "Secondary", bevel=0.0)      # grip
        b.box((0.05, 0.05, 0.05), (x, -0.05, 1.12), "Accent", bevel=0.008)          # pommel
    b.box((0.36, 0.05, 0.04), (0.28, -0.05, 1.03), "Primary")                        # hook bar for swords
    obj, _ = b.build()
    return obj
