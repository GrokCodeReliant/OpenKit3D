# openkit-kitchen-props-b1
Original procedural medieval kitchen props, CC0 1.0. All ≤210 tris.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot |
|---|---|---|---|---|
| prop-pot-hanging-kp1 | 152 | 0.272 x 0.6 x 0.548 | Primary, Bail, Bracket | wall_back |
| prop-cutting-board | 72 | 0.5 x 0.043 x 0.24 | Primary, Handle, Knife | bottom_centre |
| prop-jar-crock | 199 | 0.262 x 0.34 x 0.266 | Primary, Lid, Band | bottom_centre |
| prop-ladle-hook | 110 | 0.1 x 0.41 x 0.066 | Primary, Ladle | wall_back |

- Rename: `prop-pot-hanging` → `prop-pot-hanging-kp1` (distinct from camp `prop-cookpot-hang`, okm `prop-cauldron`). Others clash-free in art/, okm4, openkit-dnd (dnd has only 2D `prop-ladle`).
- Pivots: bottom_centre for board/crock; wall_back (back face on wall plane y=0) for pot crane and ladle hook.
- FBX: axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL, path_mode STRIP. Assign tex by slot from `tex/` (albedo sRGB, normal OpenGL, ao linear).
- Textures: byte copies from openkit-stable-props-b1 (iron, oak, dark wood) and openkit-tavern-dressing-b1 (clay), all CC0.
