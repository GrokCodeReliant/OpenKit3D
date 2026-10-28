# openkit-stable-props-b1
Original procedural stable props, CC0 1.0. All ≤210 tris.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot |
|---|---|---|---|---|
| prop-hay-bale-sp1 | 72 | 1.0 x 0.41 x 0.51 | Primary, Twine | bottom_centre |
| prop-feed-trough-sp1 | 120 | 1.2 x 0.4 x 0.5 | Primary, Secondary, Metal, Feed | bottom_centre |
| prop-hitching-post | 156 | 1.96 x 1.02 x 0.16 | Primary, Secondary, Metal | bottom_centre |
| prop-horseshoe-wall | 112 | 0.3 x 0.36 x 0.059 | Primary, Metal, Nails | wall_back |

- Renames: `prop-hay-bale` → `prop-hay-bale-sp1` (outdoor-props-b1, openkit-dnd, farm-props `-fp1`), `prop-feed-trough` → `prop-feed-trough-sp1` (farm-props-b1). `prop-hitching-post`, `prop-horseshoe-wall`: no clashes in art/, release/, okm4, openkit-dnd.
- Pivots: bottom_centre (floor y=0, centred) for bale/trough/post; wall_back (back face on wall plane, centred) for horseshoe.
- FBX: Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL, path_mode STRIP. Assign by slot from `tex/` (albedo sRGB, normal OpenGL, ao linear).
- Textures: byte copies from openkit-farm-props-b1 (CC0).
