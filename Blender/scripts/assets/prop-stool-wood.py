"""prop-stool-wood - Tiny, scales with room. Three-legged round stool with stretchers (M3)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Tiny", 800, True
MILESTONE = "M3"


def build(name, p):
    R = p.get("seat_radius", 0.19); H = p.get("height", 0.48)
    b = okit.Builder(name)
    b.cylinder(R, 0.045, 10, (0, 0, H - 0.045), "Primary", bevel=0.008)            # seat
    feet, tops = [], []
    for i in range(3):
        a = math.radians(90 + 120 * i)
        foot = (0.21 * math.cos(a), 0.21 * math.sin(a), 0.0)
        top = (0.11 * math.cos(a), 0.11 * math.sin(a), H - 0.045)
        b.strut(foot, top, 0.045, "Secondary")
        feet.append(foot); tops.append(top)
    z = 0.17
    mid = [(f[0] + (t[0] - f[0]) * z / (H - 0.045), f[1] + (t[1] - f[1]) * z / (H - 0.045), z) for f, t in zip(feet, tops)]
    for i in range(3):                                                             # ring of stretchers
        b.strut(mid[i], mid[(i + 1) % 3], 0.03, "Accent")       # stretchers: Tertiary colour slot
    obj, _ = b.build()
    return obj
