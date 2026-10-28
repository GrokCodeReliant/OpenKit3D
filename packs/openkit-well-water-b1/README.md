# openkit-well-water-b1
Original procedural well/water set, CC0 1.0. Water surfaces use their own `Water` slot (mat_water).

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot | Notes |
|---|---|---|---|---|---|
| prop-well-stone-wb1 | 796 | 1.77 x 2.219 x 1.52 | Primary(stone), Secondary(oak), Axle, Metal, Rope, Water | bottom_centre | stone curb with outer D 1.50 m, **inner shaft D 1.00 m**, and rim h 0.78 m (plus coping to 0.83). Water plane is at y=0.35 m. Two posts, a winch axle with a rope coil and a hanging rope, an iron crank on +X, and a gable roof stub (top 2.22 m) |
| prop-bucket-wood-wb1 | 308 | 0.365 x 0.468 x 0.34 | Primary, Metal, Water | bottom_centre | tapered staves, top D 0.34 / base D 0.27, body h 0.32, 2 hoops, raised bail handle, water at y=0.26 |
| prop-trough-wood | 168 | 1.60 x 0.51 x 0.61 | Primary, Metal, Water | bottom_centre | **outer length 1.60 m**, inner length 1.48 m x inner width 0.43 m. 0.06 m planks on 2 skids, 2 iron straps, water plane at y=0.40. Long axis X |
| prop-water-barrel | 832 | 0.594 x 1.27 x 0.693 | Primary, Secondary(stand), Metal, Water | bottom_centre | tall open rain cask on a 0.42 m plank stand. Front (+Z) iron spigot, 3 hoops, water plane near the top. Distinct from prop-barrel-wood/-open (those have no stand, no spigot, and a lid or grain fill) |

- Renames: okm4 already has `prop-well-stone` and `prop-bucket-wood` (base/Blender scripts), so this pack ships them as `prop-well-stone-wb1` and `prop-bucket-wood-wb1`. `prop-trough-wood` and `prop-water-barrel` have no clash.
- FBX: Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL. Unity Scale Factor 1. Materials are slots only with no texture refs. Assign by slot from `tex/` (albedo sRGB, normal OpenGL, ao linear).
- Textures: wood_oak/wood_dark/iron are byte copies from barrel-chest-b1, and stone is a byte copy from outdoor-props-b1. water and rope are new (src/make_water_tex.py).
- Rebuild: `blender -b -P src/build_well_water_b1.py -- <packroot>`.
