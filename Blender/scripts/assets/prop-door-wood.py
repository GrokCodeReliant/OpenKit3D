"""prop-door-wood - Medium, structural: scales with the room grid (fits wall-dungeon-stone-doorway's 1.2 x 2.4 m opening, like prop-door-stone).
Plank door with a Z-brace, iron straps and ring pull. PIVOT = hinge: hinge edge at x = 0, door extends toward +X (M3)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True
ROOM_SCALE = "grid"   # structural: scales with the room size class and snaps to the room grid (cell = 1.5 m x room scale)
PIVOT = "hinge"
MILESTONE = "M3"


def build(name, p):
    W = p.get("width", 1.12); H = p.get("height", 2.34); T = p.get("thickness", 0.07)
    b = okit.Builder(name)
    n = 5; pw = W / n
    for i in range(n):                                                            # vertical planks (slightly uneven tops)
        b.box((pw - 0.006, T, H - (0.02 if i % 2 else 0.0)), (pw * (i + 0.5), 0, 0), "Primary", bevel=0.01)
    by = T / 2 + 0.015                                                            # Z-brace on the back (+Y) face
    for z in (0.3, H - 0.4):
        b.box((W - 0.12, 0.03, 0.12), (W / 2, by, z), "Secondary", bevel=0.008)
    dx, dz = W - 0.24, H - 0.82
    b.box((0.1, 0.03, math.hypot(dx, dz)), (0.12, by, 0.42), "Secondary", bevel=0.008, rot=(0, math.degrees(math.atan2(dx, dz)), 0))
    fy = -(T / 2 + 0.008)                                                         # iron straps on the front (-Y) face
    for z in (0.35, H - 0.45):
        b.box((W * 0.7, 0.016, 0.06), (W * 0.35, fy, z), "Metal", bevel=0.004)
        b.cylinder(0.03, 0.2, 6, (0.0, 0.0, z - 0.07), "Metal")                  # hinge knuckles
    b.box((0.1, 0.02, 0.14), (W - 0.16, fy, 1.03), "Metal", bevel=0.005)          # pull plate
    b.ring(0.05, 0.065, 0.016, 8, (W - 0.16, fy - 0.008, 1.02), "Metal", rot=(90, 0, 0))   # ring pull
    obj, _ = b.build()
    return obj
