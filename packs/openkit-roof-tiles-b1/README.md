# openkit-roof-tiles-b1 (Open Kit modular roof tiles, batch 1)
Original procedural assets, CC0 1.0. Does not re-author tile-dungeon-*, tile-dojo-*, wall-dress, WPN_* or existing OpenKit3D tiles/walls.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot |
|---|---|---|---|---|
| tile-roof-thatch | 432 | 1.50 x 1.90 x 1.94 | Primary (mat_thatch), Secondary (mat_wood_dark: rafters/battens) | eaves_bottom |
| tile-roof-thatch-ridge | 352 | 1.50 x 0.79 x 0.86 | Primary (mat_thatch), Secondary (mat_wood_dark: liggers/spars) | ridge_apex |
| tile-roof-clay | 1776 | 1.625* x 1.80 x 1.78 | Primary (mat_terracotta: pan & cover), Secondary (mat_wood_dark: deck/rafters) | eaves_bottom |
| tile-roof-clay-ridge | 216 | 1.50 x 0.56 x 0.48 | Primary (mat_terracotta caps), Secondary (mat_terracotta mortar bed) | ridge_apex |

## Grid / snapping
- **Cell:** 1.5 m along the eaves (X) x 1.5 m horizontal run x 1.5 m rise. **Pitch 45 deg**, slope length 2.121 m.
- **eaves_bottom pivot (slopes):** origin is the underside of the eaves line, centred in X. The slope rises toward +Z (Unity, away from the front). Tile along X every 1.5 m. For a full gable roof, put a second slope rotated 180 deg about Y at +3.0 m Z; the two undersides meet at (0, 1.5, 1.5).
- **ridge_apex pivot (ridges):** origin is the apex underside. Place it at slope pivot + (0, 1.5, 1.5). It tiles along X every 1.5 m.
- Snap the eaves pivot to the top of the wall (wall top = y 0 of the roof).
- *Clay: the left pan overhangs by 0.125 m so it laps the neighbouring module (like real pan tiles). The snap step is still 1.5 m.
- Thatch and clay modules have the same footprint, so you can mix families per run.

## Tech
- 1 unit = 1 m, Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL (the kit convention). Unity Scale Factor 1. Max 1776 tris (the budget is 2500 or less).
- **Textures:** `mat_wood_dark_*` is the same as the furniture/tavern/outdoor/clutter/market packs (seed 23). `mat_thatch_*` and `mat_terracotta_*` are new (seed 91). Maps are 512 px albedo (sRGB), normal (OpenGL +Y), and AO (linear).
- The FBX files hold material slots only: image nodes are stripped and path_mode is STRIP. Assign maps by slot (URP Lit, AO in Occlusion).
- Rebuild: `python3 src/make_textures.py tex && python3 src/make_roof_tex.py tex` (then delete the iron/oak maps) `&& blender -b -P src/build_roof_tiles_b1.py -- <packroot>`. The contact sheet is a PIL montage of `renders/`.
