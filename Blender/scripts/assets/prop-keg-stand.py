"""prop-keg-stand - Small, scales with room. Keg lying on an X-frame cradle with a brass tap (M3)."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True
MILESTONE = "M3"


def build(name, p):
    L = p.get("keg_length", 0.62); re, rm = 0.2, 0.25
    b = okit.Builder(name)
    cz = 0.52                                                                      # keg axis height
    def r_at(t):
        return re + (rm - re) * (1 - (2 * t - 1) ** 2)
    ts = [0, 0.2, 0.5, 0.8, 1.0]
    prof = [(r_at(t), t * L) for t in ts]
    b.lathe(prof, 10, slot="Primary", loc=(-L / 2, 0, cz), rot=(0, 90, 0))        # keg along X (front face = end cap)
    for t in (0.1, 0.9):
        b.ring(r_at(t) - 0.01, r_at(t) + 0.012, 0.04, 10, (-L / 2 + t * L - 0.02, 0, cz), "Metal", rot=(0, 90, 0))
    # tap on the +X end cap
    b.cylinder(0.025, 0.09, 6, (L / 2, 0, cz - 0.08), "Accent", rot=(0, 90, 0))
    b.cylinder(0.016, 0.07, 6, (L / 2 + 0.07, 0, cz - 0.13), "Accent")
    # X-frame cradles
    for x in (-L / 2 + 0.12, L / 2 - 0.12):
        for s in (-1, 1):
            b.strut((x, s * 0.24, 0.0), (x, -s * 0.17, 0.37), 0.05, "Secondary")
    for s in (-1, 1):
        b.box((L - 0.1, 0.05, 0.05), (0, s * 0.2, 0.12), "Secondary")               # floor rails
    obj, _ = b.build()
    return obj
