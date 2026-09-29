"""prop-mushroom - Tiny, scales with room. Cluster of three toadstools; glowing gills (Emissive) for faerie/jungle."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Tiny", 800, True


def toadstool(b, x, y, h, r, lean=(0, 0)):
    b.cylinder(r * 0.28, h, 7, (x, y, 0), "Secondary", r_top=r * 0.2, rot=(lean[0], lean[1], 0))
    cx = x + h * math.sin(math.radians(lean[1])); cy = y - h * math.sin(math.radians(lean[0]))
    cz = h * math.cos(math.radians(max(abs(lean[0]), abs(lean[1]))))
    b.cylinder(r * 0.2, r * 0.12, 8, (cx, cy, cz - r * 0.12), "Emissive", r_top=r * 0.96)          # gills
    b.lathe([(r, cz), (r * 0.88, cz + r * 0.32), (r * 0.52, cz + r * 0.58), (0.0, cz + r * 0.66)], 8,
            slot="Primary", loc=(cx, cy, 0))
    for k in range(4):                                                                             # spots (sit ON the cap: the room-adapt render check found them buried at 0.3 r)
        a = math.radians(90 * k + 30)
        b.box((r * 0.18, r * 0.18, r * 0.12), (cx + r * 0.62 * math.cos(a), cy + r * 0.62 * math.sin(a), cz + r * 0.53),
              "Accent", bevel=0.0, rot=(0, 0, 45))


def build(name, p):
    b = okit.Builder(name)
    toadstool(b, 0.0, 0.0, 0.32, 0.2)
    toadstool(b, 0.2, -0.12, 0.2, 0.13, lean=(-10, 12))
    toadstool(b, -0.16, -0.1, 0.13, 0.09, lean=(-8, -14))
    obj, _ = b.build()
    return obj
