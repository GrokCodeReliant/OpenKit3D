"""wall-dungeon-stone-doorway - modular wall with a 1.2 x 2.4 m opening for prop-door-stone. STRUCTURAL.
Same footprint and bond as wall-dungeon-stone."""
import os, sys, importlib.util
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 2500, True
ROOM_SCALE = "grid"   # structural: scales with the room size class and snaps to the room grid (cell = 1.5 m x room scale)
CATEGORY = "Walls"

_spec = importlib.util.spec_from_file_location("wall_base", os.path.join(os.path.dirname(os.path.abspath(__file__)), "wall-dungeon-stone.py"))
_wall = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_wall)


def build(name, p):
    return _wall.build_wall(name, opening=(0.6, 2.4))
