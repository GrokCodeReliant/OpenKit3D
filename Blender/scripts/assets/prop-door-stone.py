"""prop-door-stone - Medium, structural: scales with the room grid (fits wall-dungeon-stone-doorway's 1.2 x 2.4 m opening).
PIVOT = hinge: the hinge edge is at x = 0 and the door extends toward +X; rotate about Y to open."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True
ROOM_SCALE = "grid"   # structural: scales with the room size class and snaps to the room grid (cell = 1.5 m x room scale)
PIVOT = "hinge"


def build(name, p):
    W = p.get("width", 1.12); H = p.get("height", 2.34); T = p.get("thickness", 0.12)
    b = okit.Builder(name)
    b.box((W, T, H), (W / 2, 0, 0), "Primary", bevel=0.02)
    for side in (-1, 1):
        y = side * (T / 2 + 0.008)
        for z in (0.2, 1.25):
            b.box((W - 0.3, 0.02, 0.85), (W / 2, y, z), "Secondary", bevel=0.008)   # raised panels
    for z in (0.35, 1.15, 1.95):
        b.box((W - 0.06, 0.02, 0.07), (W / 2 + 0.01, -(T / 2 + 0.02), z), "Metal", bevel=0.005)   # straps
        b.cylinder(0.035, 0.22, 6, (0.0, 0.0, z - 0.07), "Metal")                                  # hinge knuckles
    b.ring(0.07, 0.09, 0.02, 8, (W - 0.18, -(T / 2 + 0.035), 1.1), "Metal", rot=(90, 0, 0))       # ring pull
    b.box((0.08, 0.03, 0.08), (W - 0.18, -(T / 2 + 0.015), 1.16), "Accent", bevel=0.006)
    obj, _ = b.build()
    return obj
