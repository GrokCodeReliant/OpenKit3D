"""prop-cauldron - Small, scales with room. Iron pot on three stubby legs, rim, side lugs, glowing brew (Emissive + light) (M3)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"
LIGHT_SOCKET = [0.0, 0.0, 0.58]
EMISSIVE_SCALE = 0.4    # per-prop cap: the brew blew out to white in bright themes


def build(name, p):
    b = okit.Builder(name)
    z0 = 0.1
    pot = [(0.0, z0), (0.16, z0 + 0.01), (0.28, z0 + 0.1), (0.33, z0 + 0.25), (0.31, z0 + 0.4), (0.26, z0 + 0.48),
           (0.235, z0 + 0.48), (0.25, z0 + 0.42), (0.0, z0 + 0.42)]
    b.lathe(pot, 10, slot="Metal")
    b.ring(0.255, 0.3, 0.045, 10, (0, 0, z0 + 0.46), "Metal")                     # thick rim
    b.cylinder(0.25, 0.02, 10, (0, 0, z0 + 0.4), "Emissive")                      # brew surface
    for (x, y, r) in ((0.08, -0.05, 0.05), (-0.1, 0.06, 0.035), (0.02, 0.12, 0.028)):   # bubbles
        b.lathe([(0.0, 0.0), (r, r * 0.6), (r * 0.7, r * 1.3), (0.0, r * 1.5)], 5, loc=(x, y, z0 + 0.41), slot="Emissive")
    for i in range(3):                                                            # legs
        a = math.radians(90 + 120 * i)
        b.cylinder(0.04, 0.16, 6, (0.2 * math.cos(a), 0.2 * math.sin(a), 0.0), "Metal", r_top=0.05)
    for i in range(3):                                                            # firewood under the pot: Primary slot
        a = math.radians(30 + 120 * i)
        b.cylinder(0.03, 0.34, 5, (-0.17 * math.cos(a), -0.17 * math.sin(a), 0.03), "Primary", rot=(0, 90, math.degrees(a)), phase=0.0)
    b.ring(0.3, 0.38, 0.05, 8, (0, 0, 0), "Secondary")                            # hearth stones: Secondary slot
    for sx in (-1, 1):                                                            # side lugs (hanging rings)
        b.ring(0.035, 0.055, 0.025, 6, (sx * 0.34, 0, z0 + 0.34), "Metal", rot=(90, 0, 0))
    obj, _ = b.build()
    return obj
