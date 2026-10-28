# openkit-outdoor-props-b1 (Open Kit outdoor/yard props, batch 1)
Original procedural assets, CC0 1.0. New outdoor props only; does not re-author prop-fence-wood, prop-gate-wood (dropped this batch), prop-cart-hand, prop-well-stone, prop-bucket-wood, prop-ladder-wood, prop-sack-grain, prop-stump-axe, prop-anvil, prop-mushroom, candle-niche, weapon-plaque, WPN_* B01, tile-dojo-wood-*, prop-practice-banner.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot |
|---|---|---|---|---|
| prop-wheelbarrow | 264 | 1.43 x 0.68 x 0.70 | Primary (mat_wood_oak), Secondary (mat_wood_dark), Metal (mat_iron) | bottom_centre: ground y=0, centred; wheel toward +X, handles -X |
| prop-hay-bale | 140 | 0.90 x 0.39 x 0.47 | Primary (mat_straw), Secondary (mat_canvas) | bottom_centre: ground y=0, centred; long axis X |
| prop-campfire-ring | 436 | 1.07 x 0.23 x 1.01 | Primary (mat_stone), Secondary (mat_wood_dark), Emissive (mat_ember) | bottom_centre: ground y=0, centred; Emissive slot = coals (drop logs/coals by deleting slot faces if a cold ring is needed) |
| prop-tent-lean-to | 230 | 2.60 x 1.33 x 1.80 | Primary (mat_canvas), Secondary (mat_wood_dark), Tertiary (mat_straw) | bottom_centre: ground y=0, centred; ridge along X, open front +X, closed back -X, guy ropes/pegs to +X |

- 1 unit = 1 m, Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL (same as tavern-dressing-b1). Unity Scale Factor 1.
- **Shared texture seed:** `mat_wood_oak_*`, `mat_wood_dark_*`, `mat_iron_*` are byte-identical to openkit-furniture-extras-b1 / tavern-dressing-b1 (seed 23); keep one set on merge. `mat_canvas_*`, `mat_stone_*`, `mat_straw_*`, `mat_ember_*` are new (`src/make_outdoor_tex.py`, seed 57). 512 px albedo (sRGB) / normal (OpenGL +Y) / AO (linear).
- **Campfire Emissive slot:** use `mat_ember_albedo` as both Base Map and Emission Map (emission colour ~ (1, 0.35, 0.08), intensity to taste). Stone ring only = hide/delete Secondary+Emissive faces.
- Tent Tertiary (guy ropes) uses `mat_straw` as a rope-fibre stand-in.
- The FBX files contain material slots only (image nodes stripped before export, path_mode STRIP, image paths set to basename). Assign maps by slot in Unity (URP Lit, AO in Occlusion).
- Rebuild: `python3 src/make_textures.py tex && python3 src/make_outdoor_tex.py tex && blender -b -P src/build_outdoor_props_b1.py -- <packroot>`; contact sheet is a PIL montage of `renders/`.
