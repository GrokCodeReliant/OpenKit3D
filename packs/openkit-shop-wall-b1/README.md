# openkit-shop-wall-b1 (Open Kit shop/tavern wall dressing, batch 1)
These are original procedural assets, released under CC0 1.0. All four are wall-mounted. The pack doesn't re-author prop-candle-niche, prop-weapon-plaque, prop-candle-sconce (Art & Assets wall-dress), prop-rope-coil-bs1 (floor coil), prop-hook-wall or prop-sign-hanging. prop-shield-wall was optional, and I skipped it so its silhouette wouldn't overlap with prop-weapon-plaque.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot |
|---|---|---|---|---|
| prop-herb-bundle | 198 | 0.195 x 0.46 x 0.118 | Primary (mat_herb bunches), Secondary (mat_rope twine), Metal (nail + plate) | wall_back. Mount the nail at about 1.6-2.1 m |
| prop-rope-coil-wall | 204 | 0.38 x 0.49 x 0.14 | Primary (mat_rope, 2 loops + tail), Metal (peg + plate) | wall_back. Mount the peg at about 1.4-1.8 m |
| prop-wanted-poster-blank | 72 | 0.42 x 0.60 x 0.04 | Primary (mat_paper), Secondary (mat_wood_oak board), Metal (4 nails) | wall_back. Mount the bottom at about 1.2 m |
| prop-curtain-short | 200 | 1.00 x 0.63 x 0.10 | Primary (mat_cloth_banner, double-sided), Metal (rod + brackets) | wall_back. Mount the rod at about 1.9-2.2 m |

- wall_back means the origin sits on the wall plane. x is centred, y=0 is the lowest point, and the asset faces +Z (the room). Every asset is within the 210-tri budget.
- 1 unit = 1 m. Export uses Y mirror, axis_forward -Z, axis_up Y, bake_space_transform and FBX_SCALE_ALL, the same as the other openkit packs. Unity imports at Scale Factor 1.
- The FBX files hold material slots only, with no embedded texture paths. In Unity, set up one URP Lit material per texture set (albedo sRGB, normal OpenGL +Y, AO in Occlusion, 512 px).
- The FBX files have no collision meshes. If you need collision, add a box collider in the engine and give it the `-sw1` suffix.
