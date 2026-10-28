# openkit-barrel-chest-b1
Original procedural barrel/chest/sack set, CC0 1.0. No crates are included, and this pack does not re-author prop-coffer-wood.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot | Notes |
|---|---|---|---|---|---|
| prop-barrel-wood | 802 | 0.675 x 0.95 x 0.675 | Primary, Secondary, Metal | bottom_centre | closed, lid with cleats + bung, 4 iron hoops |
| prop-barrel-open | 1034 | 0.675 x 0.95 x 0.675 | Primary, Metal, Fill | bottom_centre | open top, ~25% grain fill (Fill slot surface at y=0.30 m inside, floor at 0.08 m) |
| prop-chest-wood | 228 | 0.86 x 0.61 x 0.577 | Primary, Secondary, Metal | bottom_centre | closed; low hipped trapezoid lid + corner brackets + strap hinges + runners (coffer is small 0.53 m domed half-round lid) |
| prop-sack-tied | 268 | 0.605 x 0.647 x 0.474 | Primary, Secondary | bottom_centre | soft pile footprint 0.61 x 0.47 m (oval), h 0.65 |

- Pivot: bottom_centre (floor contact at y=0). Front (hasp) faces +Z.
- FBX: Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL. Unity Scale Factor 1.
- The FBX files hold material slots only, with no texture references. Assign the materials by slot using `tex/` (albedo sRGB, normal OpenGL, ao linear).
- Rebuild: `blender -b -P src/build_barrel_chest_b1.py -- <packroot>`. The textures come from src/make_textures.py and src/make_outdoor_tex.py.
