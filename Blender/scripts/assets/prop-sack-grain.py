"""prop-sack-grain - Small, scales with room. One standing tied sack, one lying sack, a little spilled grain (M3).
M4 silhouette rework: the standing sack is a squat, slumped pear (wide heavy base, no vase shoulder) that leans a little, with a
gathered neck, a tie cord and a floppy four-flap tuft; the lying sack is a plump pillow with a tied, flared end. Patch = Secondary."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"

SACK = [(0.0, 0.0), (0.2, 0.0), (0.27, 0.05), (0.29, 0.15), (0.275, 0.27), (0.23, 0.37), (0.15, 0.44), (0.085, 0.48),
        (0.07, 0.5)]
SX, SY = -0.14, 0.06
LEAN = (4, -7, 0)


def _lean(p):
    """Point in the sack's upright frame -> leaned world position (rotation about the sack base)."""
    from mathutils import Vector
    return tuple(Vector((SX, SY, 0)) + okit._euler(LEAN).to_3x3() @ Vector(p))


def build(name, p):
    b = okit.Builder(name)
    b.lathe(SACK, 10, slot="Primary", loc=(SX, SY, 0), rot=LEAN, phase=0.2)
    b.ring(0.06, 0.085, 0.035, 8, _lean((0, 0, 0.475)), "Accent", rot=LEAN)          # tie cord
    b.cylinder(0.065, 0.06, 8, _lean((0, 0, 0.5)), "Primary", r_top=0.1, rot=LEAN)     # gathered neck, flaring out
    for i in range(4):                                                                # floppy tuft flaps
        a = 30 + 90 * i
        b.prism([(-0.05, 0.0), (0.05, 0.0), (0.02, 0.09), (-0.03, 0.08)], 0.02, _lean((0.05 * math.cos(math.radians(a)),
                0.05 * math.sin(math.radians(a)), 0.55)), "Primary", axis='X', rot=(LEAN[0] + 35 * (1 if i % 2 else -1), LEAN[1], a))
    b.box((0.14, 0.02, 0.13), _lean((0.05, -0.275, 0.12)), "Secondary", bevel=0.0, rot=(LEAN[0] - 8, LEAN[1], 12))   # patch
    # lying sack: plump pillow with a tied, flared end pointing toward -X/-Y
    b.box((0.5, 0.36, 0.22), (0.22, -0.3, 0.0), "Primary", bevel=0.09, rot=(0, 0, 20))
    ex, ey = 0.22 - 0.25 * math.cos(math.radians(20)), -0.3 - 0.25 * math.sin(math.radians(20))
    b.cylinder(0.06, 0.07, 8, (ex + 0.02, ey + 0.007, 0.11), "Primary", r_top=0.045, rot=(0, -90, 20))
    b.ring(0.04, 0.06, 0.03, 8, (ex - 0.03, ey - 0.011, 0.11), "Accent", rot=(0, -90, 20))
    b.cylinder(0.045, 0.05, 8, (ex - 0.05, ey - 0.018, 0.11), "Primary", r_top=0.085, rot=(0, -90, 20))
    for (x, y, r) in ((0.5, -0.55, 0.13), (0.34, -0.66, 0.08)):                      # spilled grain heaps
        b.lathe([(r, 0.0), (r * 0.55, r * 0.35), (0.0, r * 0.45)], 7, loc=(x, y, 0), slot="Secondary")   # grain: Secondary slot
    obj, _ = b.build()
    return obj
