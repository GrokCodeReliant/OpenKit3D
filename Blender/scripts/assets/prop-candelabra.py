"""prop-candelabra - Small, scales with room. Floor-standing iron candelabrum: centre + 2 arms, wax candles, Emissive flames + light (M3)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"
LIGHT_SOCKET = [0.0, 0.0, 1.55]


def build(name, p):
    H = p.get("height", 1.35)
    b = okit.Builder(name)
    base = [(0.0, 0.0), (0.24, 0.0), (0.24, 0.03), (0.13, 0.08), (0.06, 0.14), (0.04, 0.2), (0.0, 0.2)]
    b.lathe(base, 8, slot="Secondary")                                          # base: Secondary colour slot
    b.cylinder(0.022, H - 0.2, 6, (0, 0, 0.2), "Primary")                        # stem: Primary colour slot
    b.lathe([(0.0, 0.0), (0.05, 0.03), (0.04, 0.07), (0.0, 0.08)], 6, loc=(0, 0, 0.72), slot="Accent")   # knop
    tips = [(0.0, 0.0, H + 0.02)]
    for i in range(2):                                                            # two side arms + centre
        a = math.radians(0 + 180 * i)
        c, s = math.cos(a), math.sin(a)
        p0 = (0.0, 0.0, H - 0.18)
        p1 = (0.16 * c, 0.16 * s, H - 0.16)
        p2 = (0.24 * c, 0.24 * s, H - 0.08)
        b.strut(p0, p1, 0.022, "Metal", bevel=0.0)
        b.strut(p1, p2, 0.022, "Metal", bevel=0.0)
        tips.append((p2[0], p2[1], H - 0.08))
    for (x, y, z) in tips:
        b.cylinder(0.035, 0.03, 6, (x, y, z - 0.01), "Metal", r_top=0.05)         # drip pan
        ch = 0.2 if z > H else 0.16
        b.cylinder(0.024, ch, 6, (x, y, z + 0.02), "Accent")                     # candle
        b.flame((x, y, z + 0.02 + ch), 0.1, 0.02, segs=4, twist=60, lean=(0.005, -0.004), phase=x * 7)
    obj, _ = b.build()
    return obj
