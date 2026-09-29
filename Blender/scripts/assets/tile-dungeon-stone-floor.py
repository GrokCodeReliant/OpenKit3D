"""tile-dungeon-stone-floor - one 1.5 x 1.5 m grid cell, STRUCTURAL (scales with the room grid).
PIVOT = floor_top: the walking surface is at z = 0 and the tile extends 0.12 m below it, so props at y = 0 stand on it.
Slabs = Secondary (stone), one accent slab = Accent (Tertiary slot), joint bed = Primary (visible in the joints)."""
import random
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True
ROOM_SCALE = "grid"   # structural: scales with the room size class and snaps to the room grid (cell = 1.5 m x room scale)
PIVOT = "floor_top"
CATEGORY = "Tiles"


def build(name, p):
    C = okit.GRID; gap = 0.02
    b = okit.Builder(name)
    b.box((C, C, 0.08), (0, 0, -0.12), "Primary", bevel=0.0)                   # joint bed, top at -0.04
    rnd = random.Random(21)
    # irregular 3-row slab layout that tiles seamlessly (all joints inside the cell)
    rows = [[0.55, 0.95], [0.9, 0.6], [0.4, 0.65, 0.45]]
    heights = [0.5, 0.55, 0.45]
    y = -C / 2
    for row, rh in zip(rows, heights):
        x = -C / 2
        for w in row:
            drop = rnd.uniform(0.0, 0.012) if (x > -C / 2 or y > -C / 2) else 0.0
            slot = "Accent" if w == 0.4 else "Secondary"                           # one accent slab: Tertiary colour slot
            b.box((w - gap, rh - gap, 0.08 - drop), (x + w / 2, y + rh / 2, -0.08), slot, bevel=0.018)
            x += w
        y += rh
    obj, _ = b.build()
    return obj
