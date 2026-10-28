# openkit-dungeon-clutter-b1 (Open Kit dungeon clutter, batch 1)
Original procedural assets, CC0 1.0. New dungeon clutter only; does not re-author crypt-f1 pieces (Rubble_Landing, Bone_Pile), OpenKit3D props, outdoor/tavern/furniture/medieval-env packs, prop-candle-niche, prop-weapon-plaque, prop-candle-sconce, WPN_* B01, tile-dojo-*, prop-practice-banner. prop-skull-pile was skipped on purpose.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot |
|---|---|---|---|---|
| prop-rubble-small | 324 | 0.83 x 0.32 x 0.73 | Primary (mat_stone), Secondary (mat_stone) | bottom_centre: ground y=0, centred; low loose pile ~0.75 x 0.6 (not a landing/stair piece) |
| prop-broken-pottery | 460 | 0.78 x 0.21 x 0.79 | Primary (mat_clay), Secondary (mat_wood_dark) | bottom_centre: ground y=0, centred; standing broken base at origin, shards scattered; Secondary = spill stain decal disc (deletable) |
| prop-chain-hanging | 1012 | 0.12 x 0.99 x 0.12 | Primary (mat_iron), Metal (mat_iron) | wall_back: pivot at wall plate centre, wall plane at origin, chain hangs -Y(up) and protrudes toward +Z (Unity) / -Y Blender |
| prop-cage-hanging | 1216 | 0.74 x 1.78 x 0.72 | Primary (mat_iron), Metal (mat_iron), Secondary (mat_wood_dark) | top_hook: pivot at ceiling/wall hook point (y=0), cage hangs below to y=-1.76 |

- 1 unit = 1 m, Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL (same as outdoor/tavern packs). Unity Scale Factor 1.
- **Shared textures:** `mat_wood_dark_*`, `mat_iron_*` byte-identical to furniture/tavern/outdoor (seed 23); `mat_stone_*` = outdoor-props-b1 (seed 57); `mat_clay_*` = tavern-dressing-b1 (seed 41). Keep one set on merge. 512 px albedo (sRGB) / normal (OpenGL +Y) / AO (linear).
- Pottery Secondary = flat spill-stain disc; delete those faces for a clean floor.
- The FBX files contain material slots only (image nodes stripped before export, path_mode STRIP, image paths set to basename). Assign maps by slot in Unity (URP Lit, AO in Occlusion).
- Rebuild: `python3 src/make_textures.py tex && python3 src/make_outdoor_tex.py tex && python3 src/make_clay.py tex` (then delete unused oak/canvas/straw/ember maps) `&& blender -b -P src/build_dungeon_clutter_b1.py -- <packroot>`; contact sheet is a PIL montage of `renders/`.
