"""prop-lantern - Tiny, scales with room. Hand lantern: base, four posts, glowing core (Emissive + light), cap and ring handle (M3)."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Tiny", 800, True
MILESTONE = "M3"
LIGHT_SOCKET = [0.0, 0.0, 0.17]
EMISSIVE_SCALE = 0.45   # per-prop cap on emissive + light (the whole glass core glows)


def build(name, p):
    b = okit.Builder(name)
    b.box((0.18, 0.18, 0.035), (0, 0, 0), "Primary", bevel=0.006)                 # base: Primary colour slot
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.box((0.02, 0.02, 0.2), (sx * 0.075, sy * 0.075, 0.035), "Secondary", bevel=0.0)   # posts: Secondary slot
    b.box((0.135, 0.135, 0.2), (0, 0, 0.035), "Emissive", bevel=0.0)             # lit glass panes (whole core glows)
    b.box((0.19, 0.19, 0.025), (0, 0, 0.235), "Metal", bevel=0.005)               # top plate
    b.cylinder(0.09, 0.07, 6, (0, 0, 0.26), "Metal", r_top=0.03)                  # cap
    b.ring(0.035, 0.05, 0.015, 8, (0, 0.0075, 0.35), "Metal", rot=(90, 0, 0))    # handle ring
    obj, _ = b.build()
    return obj
