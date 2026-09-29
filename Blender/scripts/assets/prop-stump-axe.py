"""prop-stump-axe - Small, scales with room. Chopping stump with roots, an axe bitten into the top and split logs (M3; M4: axe head lifted out of the stump)."""
import math
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"


def build(name, p):
    b = okit.Builder(name)
    b.broken_shaft(0.26, 0.5, segs=9, jag=0.015, seed=4, slot="Primary", r_top=0.24)   # stump (bark)
    b.cylinder(0.225, 0.012, 9, (0, 0, 0.5), "Accent")                                # cut face (light wood)
    for i in range(4):                                                               # roots
        a = math.radians(20 + 90 * i)
        b.prism([(0.0, 0.0), (0.18, 0.0), (0.0, 0.18)], 0.1, (0.2 * math.cos(a), 0.2 * math.sin(a), 0), "Primary",
                axis='Y', rot=(0, 0, math.degrees(a)))
    # axe (M4 rework): the handle rises at 20 degrees toward +X; the head hangs off it with only the cutting edge bitten ~2-4 cm
    # into the cut face, so the whole blade (broad faces toward -Y/+Y) reads clearly above the stump.
    S = 0.512                                                                          # top of the cut face
    ang = math.radians(20)
    u = (math.cos(ang), math.sin(ang)); n = (-math.sin(ang), math.cos(ang))
    E = (0.21 * n[0], S - 0.025 + 0.21 * n[1])

    def P(a, c):
        return (E[0] + a * u[0] + c * n[0], E[1] + a * u[1] + c * n[1])
    y0 = -0.02
    blade = [P(-0.04, 0.035), P(0.04, 0.035), P(0.05, -0.07), P(0.13, -0.21), P(-0.13, -0.21), P(-0.05, -0.07)]   # M4: 40% larger head
    b.prism(blade, 0.035, (0, y0, 0), "Metal", axis='Y')                                # head + blade
    b.prism([P(-0.035, 0.035), P(0.035, 0.035), P(0.03, 0.09), P(-0.03, 0.09)], 0.05, (0, y0, 0), "Metal", axis='Y')   # poll
    h0, h1 = P(-0.05, 0.02), P(0.56, 0.02)
    b.strut((h0[0], y0, h0[1]), (h1[0], y0, h1[1]), 0.035, "Secondary", segs=6)       # handle through the eye
    em = P(0.0, -0.21)
    b.box((0.22, 0.05, 0.004), (em[0], y0, S - 0.001), "Secondary", bevel=0.0, rot=(0, math.degrees(ang) * 0.3, 0))  # dark split in the cut face
    for (x, y, r) in ((-0.42, -0.1, 0.07), (-0.38, 0.12, 0.06)):                       # split logs on the ground
        b.cylinder(r, 0.36, 5, (x, y - 0.18, r), "Primary", rot=(-90, 0, 0), phase=0.0)
    obj, _ = b.build()
    return obj
