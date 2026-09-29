"""prop-treasure-pile - Small, scales with room. Coin mound (Metal), scattered coins, gems (Accent), goblet."""
import math, random
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True

PROF = [(0.55, 0.0), (0.46, 0.1), (0.32, 0.22), (0.14, 0.31), (0.0, 0.33)]


def h_at(r):
    for (r0, z0), (r1, z1) in zip(PROF[:-1], PROF[1:]):
        if r1 <= r <= r0:
            return z0 + (z1 - z0) * (r0 - r) / (r0 - r1)
    return 0.0


def build(name, p):
    b = okit.Builder(name)
    b.lathe(PROF, 10, slot="Metal", phase=0.2)
    rnd = random.Random(5)
    for i in range(9):                                              # coins on/around the mound
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(0.15, 0.62)
        z = h_at(r)
        b.cylinder(0.045, 0.012, 6, (r * math.cos(a), r * math.sin(a), max(0.0, z - 0.004)), "Metal",
                   rot=(rnd.uniform(-25, 25), rnd.uniform(-25, 25), 0))
    for i in range(6):                                              # gems
        a = rnd.uniform(0, 2 * math.pi); r = rnd.uniform(0.05, 0.45)
        b.gem(0.05, 0.1, (r * math.cos(a), r * math.sin(a), max(0.0, h_at(r) - 0.03)), "Accent",
              rot=(rnd.uniform(-20, 20), rnd.uniform(-20, 20), 0))
    # goblet lying on the side and a standing one
    gob = [(0.0, 0.0), (0.06, 0.0), (0.06, 0.012), (0.012, 0.03), (0.012, 0.1), (0.05, 0.13), (0.06, 0.2), (0.05, 0.2), (0.0, 0.16)]
    b.lathe(gob, 8, loc=(0.18, -0.35, h_at(0.4) - 0.02), slot="Metal")
    b.lathe(gob, 8, loc=(-0.45, 0.25, 0.06), slot="Metal", rot=(0, 95, 30))
    # colour-slot coverage: a broken plank (Primary) and a coin pouch (Secondary) at the edge of the pile
    b.box((0.5, 0.1, 0.03), (0.2, 0.52, 0.0), "Primary", rot=(0, 0, -25))
    b.lathe([(0.0, 0.0), (0.08, 0.0), (0.1, 0.06), (0.07, 0.13), (0.03, 0.15), (0.045, 0.19), (0.0, 0.19)], 7,
            loc=(-0.52, -0.2, 0.0), slot="Secondary")
    obj, _ = b.build()
    return obj
