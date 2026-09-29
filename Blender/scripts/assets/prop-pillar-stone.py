"""prop-pillar-stone - Medium, STRUCTURAL: grid-locked, scales with the room grid (cell = 1.5 m x room scale).
3.0 m tall (2 cells), footprint 0.9 m inside one 1.5 m cell."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True
ROOM_SCALE = "grid"   # structural: scales with the room size class and snaps to the room grid (cell = 1.5 m x room scale)
CATEGORY = "Props"


def build(name, p):
    H = p.get("height", 3.0); segs = p.get("segments", 12); R = p.get("shaft_radius", 0.28)
    b = okit.Builder(name)
    b.box((0.9, 0.9, 0.18), (0, 0, 0), "Secondary", bevel=0.02)                 # plinth
    base = [(0.40, 0.18), (0.40, 0.24), (0.36, 0.28), (0.36, 0.32), (0.32, 0.36), (R + 0.01, 0.40)]
    b.lathe(base, segs, slot="Accent")
    # shaft with slight entasis
    z0, z1 = 0.40, H - 0.42
    n = 6
    prof = []
    for i in range(n + 1):
        t = i / n
        z = z0 + (z1 - z0) * t
        r = R * (1.0 + 0.04 * (1 - (2 * t - 0.35) ** 2)) - 0.03 * t
        prof.append((r, z))
    b.lathe(prof, segs, slot="Primary")
    # a stone band ring part-way up
    b.ring(R - 0.02, R + 0.03, 0.08, segs, (0, 0, 1.2), "Accent")
    cap = [(R - 0.02, z1), (R + 0.02, z1 + 0.06), (0.30, z1 + 0.08), (0.38, z1 + 0.18), (0.40, z1 + 0.22)]
    b.lathe(cap, segs, slot="Accent")
    b.box((0.9, 0.9, 0.20), (0, 0, H - 0.20), "Secondary", bevel=0.02)          # abacus
    obj, _ = b.build()
    return obj
