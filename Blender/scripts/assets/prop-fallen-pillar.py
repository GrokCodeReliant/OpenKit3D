"""prop-fallen-pillar - Medium, stone ruin: scales with the room grid (room-adapt rule, 2026-09-28).
Broken stump on its plinth, the fallen shaft section, the toppled capital and rubble."""
import random
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Large", 2500, True  # ~3.7 x 1.5 m footprint
ROOM_SCALE = "grid"   # structural: scales with the room size class and snaps to the room grid (cell = 1.5 m x room scale)


def build(name, p):
    R = 0.28; segs = 12
    b = okit.Builder(name)
    # stump (same profile as prop-pillar-stone base)
    b.box((0.9, 0.9, 0.18), (0, 0, 0), "Secondary", bevel=0.02)
    b.lathe([(0.40, 0.18), (0.40, 0.24), (0.36, 0.28), (0.36, 0.32), (0.32, 0.36), (R + 0.01, 0.40)], segs, slot="Accent")
    b.broken_shaft(R + 0.01, 0.55, segs, jag=0.12, seed=3, loc=(0, 0, 0.40), slot="Primary")
    # fallen shaft section lying along +X
    b.broken_shaft(R, 1.35, segs, jag=0.10, seed=7, jag_bottom=0.08, loc=(0.55, 0.15, R - 0.02), rot=(0, 90, 8), slot="Primary")
    b.ring(R - 0.02, R + 0.03, 0.08, segs, (1.2, 0.2, R - 0.02), "Accent", rot=(0, 90, 8))
    # toppled capital + abacus, tilted on the floor
    b.lathe([(R - 0.02, 0.0), (R + 0.02, 0.06), (0.30, 0.08), (0.38, 0.18), (0.40, 0.22)], segs,
            loc=(-0.95, -0.55, 0.42), slot="Accent", rot=(100, 0, 20))
    b.box((0.9, 0.9, 0.2), (-1.05, -0.2, 0.0), "Secondary", bevel=0.02, rot=(0, 0, 28))
    rnd = random.Random(11)
    for i in range(7):
        s = rnd.uniform(0.1, 0.22)
        b.box((s, s * rnd.uniform(0.7, 1.2), s * 0.7), (rnd.uniform(-0.6, 1.6), rnd.uniform(-0.7, 0.7), 0),
              "Secondary", bevel=0.015, rot=(0, 0, rnd.uniform(0, 90)))
    obj, _ = b.build()
    return obj
