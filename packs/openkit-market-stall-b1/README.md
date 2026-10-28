# openkit-market-stall-b1 (Open Kit market/shop stall props, batch 1)
Original procedural assets, CC0 1.0. Does not re-author prop-cart-hand, prop-crate (closed), prop-barrel, prop-table-*, prop-counter-tavern, outdoor/tavern/furniture/medieval-env/clutter packs, prop-candle-niche, prop-weapon-plaque, prop-candle-sconce, WPN_* B01, tile-dojo-*, prop-practice-banner.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot |
|---|---|---|---|---|
| prop-market-stall | 300 | 2.06 x 2.42 x 1.14 | Primary (mat_wood_dark), Secondary (mat_wood_oak), Trim (mat_wood_oak, blank sign) | bottom_centre; counter top y=0.9, front faces -Z |
| prop-awning-cloth | 460 | 2.16 x 0.56 x 1.37 | Primary (mat_canvas), Secondary (mat_straw, ties) | stall_space: separate piece; place at the stall's origin/rotation and it sits on the posts |
| prop-crate-open | 276 | 0.64 x 0.36 x 0.45 | Primary (mat_wood_oak), Secondary (mat_wood_dark) | bottom_centre; open top, slatted |
| prop-basket-wicker | 992 | 0.44 x 0.41 x 0.44 | Primary (mat_straw), Secondary (mat_straw) | bottom_centre |
| prop-produce-pile | 396 | 0.57 x 0.25 x 0.60 | Primary (mat_produce), Secondary (mat_canvas) | bottom_centre; fruit mound on cloth |

- 1 unit = 1 m, Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL (same as outdoor/tavern/clutter). Unity Scale Factor 1.
- **Shared textures:** `mat_wood_oak_*`/`mat_wood_dark_*` match furniture/tavern/outdoor/clutter (seed 23). `mat_canvas_*`/`mat_straw_*` match outdoor-props-b1 (seed 57). `mat_produce_*` is new (seed 73). Keep one set when you merge. 512 px albedo (sRGB) / normal (OpenGL +Y) / AO (linear).
- The FBX files hold material slots only: image nodes are stripped, path_mode is STRIP, and paths are basenames. Assign maps by slot in Unity (URP Lit, AO in Occlusion).
- Rebuild: `python3 src/make_textures.py tex && python3 src/make_outdoor_tex.py tex && python3 src/make_produce.py tex` (then delete the iron/stone/ember maps) `&& blender -b -P src/build_market_stall_b1.py -- <packroot>`. The contact sheet is a PIL montage of `renders/`.
