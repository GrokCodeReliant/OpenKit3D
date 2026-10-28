# openkit-tavern-dressing-b1 (Open Kit shop/tavern dressing, batch 1)
These are original procedural assets, released under CC0 1.0. The pack adds new small dressing props only. It does not re-author prop-keg-stand, prop-signpost, prop-banner-*, prop-table-*, prop-stool-*, prop-shelf-wall, prop-counter-tavern, prop-coffer-wood, barrel, crate, chest, bookshelf, candle-niche or weapon-plaque.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot |
|---|---|---|---|---|
| prop-tankard-wood | 324 | 0.16 x 0.15 x 0.12 | Primary (oak body), Secondary (dark handle), Metal (2 hoops) | bottom_centre, handle on +X |
| prop-jug-clay | 344 | 0.21 x 0.32 x 0.20 | Primary (mat_clay body and handle), Secondary (dark wood stopper) | bottom_centre, handle on +X |
| prop-sign-hanging | 180 | 0.08 x 0.60 x 0.72 | Primary (oak board), Secondary (dark frame), Metal (bracket, strut, links) | wall_back: plate on the wall plane, x centred, y=0 at the board bottom, arm sticks out +Z, board faces ±X. Mount the board bottom at about 2.0-2.4 m |
| prop-bowl-wood | 196 | 0.18 x 0.07 x 0.18 | Primary (oak) | bottom_centre |
| prop-plate-wood | 160 | 0.24 x 0.02 x 0.24 | Primary (oak trencher) | bottom_centre |
| prop-hook-wall | 224 | 0.80 x 0.12 x 0.10 | Primary (oak pegs), Secondary (dark rail), Metal (hooks, nails) | wall_back: rail back on the wall plane, x centred, y=0 at the rail bottom, faces +Z. Mount at about 1.4-1.7 m |

- Scale and export follow the same pattern as openkit-medieval-env-b1 and furniture-extras-b1: 1 unit = 1 m, Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL. Unity imports at Scale Factor 1.
- **Shared texture seed:** `tex/mat_wood_oak_*`, `tex/mat_wood_dark_*` and `tex/mat_iron_*` are byte-identical copies of the openkit-furniture-extras-b1 PNGs (same `make_textures.py`, seed 23). If both packs are imported, keep one set. `mat_clay_*` is new and comes from `src/make_clay.py` (seed 41).
- Each texture set has `_albedo` (sRGB), `_normal` (OpenGL +Y) and `_ao` (linear) at 512 px.
- The FBX files contain material slots only (no embedded texture paths). Assign albedo/normal/AO by slot in Unity using one URP Lit material per set, with AO in Occlusion.
- To rebuild: `python3 src/make_textures.py tex && python3 src/make_clay.py tex && blender -b -P src/build_tavern_dressing_b1.py -- <packroot>`. After that, the contact sheet is a PIL montage of `renders/`.
