"""prop-table-wood - Medium, scales with room."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Medium", 800, True


def build(name, p):
    W = p.get("width", 1.40); D = p.get("depth", 0.80); H = p.get("height", 0.76)
    top_t = p.get("top_thickness", 0.06); leg = p.get("leg", 0.08); inset = p.get("leg_inset", 0.08)
    b = okit.Builder(name)
    # top made of three planks (reads as wood, flat colour only)
    planks = 3; pw = D / planks
    for i in range(planks):
        y = -D / 2 + pw * (i + 0.5)
        b.box((W, pw - 0.006, top_t), (0, y, H - top_t), "Primary")
    x = W / 2 - inset - leg / 2; y = D / 2 - inset - leg / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.box((leg, leg, H - top_t), (sx * x, sy * y, 0), "Secondary")
    ap_h = 0.09; ap_t = 0.025
    b.box((2 * x, ap_t, ap_h), (0, -y, H - top_t - ap_h), "Secondary")
    b.box((2 * x, ap_t, ap_h), (0, y, H - top_t - ap_h), "Secondary")
    for sx in (-1, 1):
        b.box((ap_t, 2 * y, ap_h), (sx * x, 0, H - top_t - ap_h), "Secondary")
    # low H-stretcher
    b.box((2 * x, 0.04, 0.04), (0, 0, 0.14), "Secondary")
    for sx in (-1, 1):
        b.box((0.04, 2 * y, 0.04), (sx * x, 0, 0.14), "Secondary")
    # metal corner brackets under the top
    for sx in (-1, 1):
        for sy in (-1, 1):
            b.box((0.1, 0.1, 0.012), (sx * (W / 2 - 0.05), sy * (D / 2 - 0.05), H - top_t - 0.012), "Metal", bevel=0.003)
    obj, _ = b.build()
    return obj
