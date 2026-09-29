"""wall-dungeon-stone - modular wall, STRUCTURAL (scales with the room grid). 1.5 m long (one cell edge) x 3.0 m tall x 0.3 m.
Pivot bottom-centre, centred on the cell edge; front faces -Y (Unity +Z). Blocks = Secondary, mortar core = Primary,
cap course = Accent. Running bond with half blocks at the ends so neighbours line up."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True
ROOM_SCALE = "grid"   # structural: scales with the room size class and snaps to the room grid (cell = 1.5 m x room scale)
CATEGORY = "Walls"

L, H, T = 1.5, 3.0, 0.3
ROW_H = 0.375
GAP = 0.018


def courses():
    """yield (z, [(x0, x1), ...]) per course; alternate full and half-offset bonds."""
    n = int(round((H - 0.12) / ROW_H))
    rh = (H - 0.12) / n
    for i in range(n):
        if i % 2 == 0:
            cuts = [-0.75, -0.25, 0.25, 0.75]
        else:
            cuts = [-0.75, -0.5, 0.0, 0.5, 0.75]
        yield i * rh, rh, list(zip(cuts[:-1], cuts[1:]))


def build_wall(name, opening=None):
    """opening = (half_width, height) centred at x=0, or None."""
    b = okit.Builder(name)
    if opening:
        ow, oh = opening
        jw = (L / 2 - ow)
        for sx in (-1, 1):
            b.box((jw, T - 0.06, oh), (sx * (ow + jw / 2), 0, 0), "Primary", bevel=0.0)
        b.box((L, T - 0.06, H - oh), (0, 0, oh), "Primary", bevel=0.0)
    else:
        b.box((L, T - 0.06, H), (0, 0, 0), "Primary", bevel=0.0)
    for z, rh, spans in courses():
        for (x0, x1) in spans:
            parts = [(x0, x1)]
            if opening and z < opening[1] - 1e-6:
                ow = opening[0]
                parts = [(a, min(c, -ow)) for (a, c) in parts if a < -ow] + [(max(a, ow), c) for (a, c) in parts if c > ow]
            for (a, c) in parts:
                w = c - a
                if w < 0.06:
                    continue
                g0 = GAP / 2 if a > -L / 2 + 1e-6 else 0.0
                g1 = GAP / 2 if c < L / 2 - 1e-6 else 0.0
                top = min(z + rh, opening[1]) if (opening and z < opening[1] and z + rh > opening[1] and -opening[0] < (a + c) / 2 < opening[0]) else z + rh
                b.box((w - g0 - g1 - 0.002, T, top - z - GAP), ((a + g0 + c - g1) / 2, 0, z + GAP / 2), "Secondary", bevel=0.02)
    b.box((L, T + 0.04, 0.12), (0, 0, H - 0.12), "Accent", bevel=0.015)       # cap course
    if opening:
        ow, oh = opening
        b.box((2 * ow + 0.3, T + 0.04, 0.3), (0, 0, oh), "Accent", bevel=0.02)  # lintel
        for sx in (-1, 1):
            b.box((0.12, T + 0.03, oh), (sx * (ow + 0.06), 0, 0), "Accent", bevel=0.015)   # jamb stones
    obj, _ = b.build()
    return obj


def build(name, p):
    return build_wall(name)
