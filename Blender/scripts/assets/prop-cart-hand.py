"""prop-cart-hand - Medium, scales with room. Two-wheeled handcart: plank bed, side boards, spoked wheels, handles, prop leg (M3)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 800, True
MILESTONE = "M3"


def wheel(b, x, R, cz):
    b.ring(R - 0.05, R, 0.05, 12, (x - 0.025, 0, cz), "Primary", rot=(0, 90, 0))   # rim (axis along X)
    b.cylinder(0.06, 0.09, 6, (x - 0.045, 0, cz), "Metal", rot=(0, 90, 0))         # hub
    for k in range(4):                                                              # spokes in the Y-Z plane
        a = math.pi * k / 4
        d = (0, math.cos(a) * (R - 0.04), math.sin(a) * (R - 0.04))
        b.strut((x, -d[1], cz - d[2]), (x, d[1], cz + d[2]), 0.03, "Primary", bevel=0.0)


def build(name, p):
    W = p.get("bed_width", 0.8); L = p.get("bed_length", 1.1); R = 0.34
    b = okit.Builder(name)
    cz = R                                                                           # axle height
    bz = cz + 0.06                                                                   # bed bottom
    b.box((W, L, 0.05), (0, 0, bz), "Primary", bevel=0.0)                            # bed
    for sx in (-1, 1):
        b.box((0.03, L, 0.22), (sx * (W / 2 - 0.015), 0, bz + 0.05), "Primary", bevel=0.0)   # side boards
    for sy in (-1, 1):
        b.box((W - 0.06, 0.03, 0.18), (0, sy * (L / 2 - 0.015), bz + 0.05), "Primary", bevel=0.0)
    for sx in (-1, 1):
        b.box((0.03, 0.035, 0.24), (sx * (W / 2 + 0.005), 0.2, bz + 0.04), "Metal", bevel=0.0)   # corner irons
        b.strut((sx * (W / 2 - 0.08), -L / 2 + 0.1, bz - 0.01), (sx * (W / 2 - 0.08), -L / 2 - 0.6, bz + 0.22), 0.05,
                "Secondary")                                                        # handles toward the front (-Y)
        wheel(b, sx * (W / 2 + 0.07), R, cz)
    b.cylinder(0.025, W + 0.2, 6, (-(W / 2 + 0.1), 0, cz), "Metal", rot=(0, 90, 0))   # axle
    b.strut((0, -L / 2 + 0.05, bz), (0, -L / 2 + 0.05, 0.0), 0.05, "Secondary")      # prop leg
    obj, _ = b.build()
    return obj
