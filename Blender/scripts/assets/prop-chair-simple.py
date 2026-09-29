"""prop-chair-simple - Small, scales with room. Human-scale (1.0) dimensions."""
import okit
SIZE_CLASS, BUDGET, SCALES_WITH_ROOM = "Small", 800, True


def build(name, p):
    W = p.get("width", 0.44); D = p.get("depth", 0.42)
    seat_h = p.get("seat_height", 0.46); back_h = p.get("back_height", 0.94)
    leg = p.get("leg", 0.045); seat_t = p.get("seat_thickness", 0.04)
    b = okit.Builder(name)
    x = W / 2 - leg / 2; y = D / 2 - leg / 2
    # front legs (front = -Y) stop under the seat; back legs run up into the backrest
    for sx in (-1, 1):
        b.box((leg, leg, seat_h - seat_t), (sx * x, -y, 0), "Primary")
        b.box((leg, leg, back_h), (sx * x, y, 0), "Primary")
    # seat
    b.box((W, D, seat_t), (0, 0, seat_h - seat_t), "Secondary")
    # stretchers
    st = leg * 0.6
    for sx in (-1, 1):
        b.box((st, D - leg, st), (sx * x, 0, 0.14), "Primary")
    b.box((W - leg, st, st), (0, -y, 0.2), "Primary")
    b.box((W - leg, st, st), (0, y, 0.2), "Primary")
    # backrest: top rail (Accent) + two vertical slats
    b.box((W - leg * 0.5, leg * 0.8, 0.09), (0, y, back_h - 0.1), "Accent")
    b.box((W - leg, leg * 0.6, 0.05), (0, y, seat_h + 0.12), "Primary")
    for sx in (-0.33, 0.0, 0.33):
        b.box((0.05, leg * 0.5, back_h - 0.1 - (seat_h + 0.17)), (sx * (W - leg) / 2, y, seat_h + 0.17), "Primary")
    obj, _ = b.build()
    return obj
