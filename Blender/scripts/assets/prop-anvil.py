"""prop-anvil - Small, scales with room. Smithing anvil (horn toward +X) on a banded wooden block, hammer on the face (M3)."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"


def build(name, p):
    b = okit.Builder(name)
    b.cylinder(0.26, 0.42, 8, (0, 0, 0), "Primary", r_top=0.23, bevel=0.012)      # stump block
    b.ring(0.255, 0.275, 0.05, 8, (0, 0, 0.06), "Metal")
    z = 0.42; D = 0.2
    body = [(-0.2, 0.0), (0.2, 0.0), (0.16, 0.05), (0.08, 0.08), (0.07, 0.17), (0.2, 0.2), (0.2, 0.28),
            (-0.26, 0.28), (-0.26, 0.2), (-0.12, 0.17), (-0.1, 0.08), (-0.16, 0.05)]
    b.prism(body, D, (0, 0, z), "Metal", axis='Y')
    b.cylinder(0.08 / 1.2, 0.26, 6, (0.2, 0, z + 0.2), "Metal", r_top=0.008, rot=(0, 90, 0))   # horn
    b.box((0.03, 0.03, 0.02), (-0.2, 0, z + 0.28), "Secondary", bevel=0.0)        # hardy hole
    # hammer lying on the face
    b.box((0.07, 0.035, 0.035), (-0.08, -0.03, z + 0.28), "Metal", bevel=0.004)
    b.strut((-0.08, -0.03, z + 0.2975), (0.14, -0.1, z + 0.2975), 0.022, "Primary", bevel=0.0)
    obj, _ = b.build()
    return obj
