"""prop-torch-wall - Tiny, scales with room. Wall-mounted: pivot = back plate bottom-centre (back at y=0,
torch sticks out toward the front). Mount it on a wall face; Unity adds a light at LIGHT_SOCKET."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Tiny", 800, True
PIVOT = "wall_back"
LIGHT_SOCKET = [0.0, -0.36, 0.62]


def build(name, p):
    b = okit.Builder(name)
    b.box((0.14, 0.03, 0.24), (0, -0.015, 0), "Metal", bevel=0.005)                # wall plate
    b.strut((0, -0.03, 0.07), (0, -0.21, 0.10), 0.03, "Metal")                     # arm
    b.ring(0.035, 0.05, 0.04, 6, (0, -0.22, 0.08), "Metal")                        # cup ring
    tilt = -15
    b.cylinder(0.024, 0.40, 6, (0, -0.22, 0.02), "Primary", r_top=0.034, rot=(tilt, 0, 0))   # stick
    t = math.radians(tilt)
    top = (0, -0.22 + 0.40 * math.sin(t), 0.02 + 0.40 * math.cos(t))
    b.cylinder(0.046, 0.09, 6, (top[0], top[1] + 0.02, top[2] - 0.08), "Secondary", r_top=0.05, rot=(tilt, 0, 0))  # pitch wrap
    fz = top[2] + 0.0
    b.flame((top[0], top[1], fz), 0.26, 0.055, twist=100, lean=(0.0, -0.03))
    b.flame((top[0] + 0.03, top[1] - 0.01, fz - 0.01), 0.16, 0.035, twist=-80, lean=(0.04, -0.02), phase=1.0)
    b.flame((top[0] - 0.03, top[1] + 0.01, fz - 0.01), 0.18, 0.035, twist=90, lean=(-0.04, -0.03), phase=2.0)
    obj, _ = b.build()
    return obj
