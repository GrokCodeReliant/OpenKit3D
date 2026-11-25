# Garden Court pieces
Six original low-poly floor props for a cloister garth or small garden court: a stone sundial, a birdbath, a planter, a timber trellis, a cold-frame, and a free-standing lavabo.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `prop-sundial-stone` | 272 | 0.60 × 0.84 × 0.57 | 1 cell | Stone plinth and shaft under a dial plate with incised hour lines and a bronze gnomon. This is deliberate: the plate collider fills the recessed hour lines. |
| `prop-birdbath-stone` | 268 | 0.60 × 0.80 × 0.57 | 1 cell | Stone pedestal with an open shallow bowl and a water disc below the rim. The mouth above the water is a real gap. |
| `prop-planter-stone` | 312 | 0.92 × 0.82 × 0.52 | 1 cell | Rectangular stone trough with soil and a simple shrub. This is deliberate: the trough and soil share one filled box; there is no opening into the trough. |
| `prop-trellis-wood` | 308 | 1.09 × 1.62 × 0.10 | 1 cell | Timber posts and rails with a coarse lattice and iron post caps. The openings in the lattice are real gaps. |
| `prop-cold-frame` | 316 | 1.00 × 0.54 × 0.68 | 1 cell | Low timber box with soil and a sloped lid, slightly open, holding two pale glaze panes. The opening under the raised lid is a real gap. This is deliberate: the trough box is filled. |
| `prop-lavabo-stone` | 312 | 0.64 × 1.02 × 0.61 | 1 cell | Free-standing stone pedestal basin with a small bronze spout and a water disc below the rim. The mouth above the water is a real gap. |

## Conventions
- 1 unit = 1 metre. Grid: 1.5 m cells.
- Pivots: bottom centre on every piece. Each piece fits in one 1.5 m cell. In the raw FBX file frame, the front of each piece faces +Z.
- Flat-shaded closed meshes. Each model uses at most 3 material slots, `Primary`, `Secondary` and `Accent`. FBX files are slots-only (no embedded textures, path_mode STRIP). Optional flat BaseColor PNGs live in `tex/`.
- Static meshes only. Nothing is rigged or animated.

## Colour slots
| Asset | `Primary` | `Secondary` | `Accent` | Suggested `tex/` |
|---|---|---|---|---|
| `prop-sundial-stone` | plinth and shaft, hour lines | dial plate | bronze gnomon | stone, mortar, bronze |
| `prop-birdbath-stone` | plinth and shaft | bowl | water | stone, stone, water |
| `prop-planter-stone` | stone trough | soil | shrub | stone, soil, leaf |
| `prop-trellis-wood` | posts and rails | lattice slats (dark timber) | iron post caps | wood, dark wood, iron |
| `prop-cold-frame` | timber trough and lid frame | soil | glaze panes | wood, soil, glaze |
| `prop-lavabo-stone` | plinth and shaft | basin bowl and spout (bronze) | water | stone, bronze, water |

Texture files: `tex/mat_stone_BaseColor.png`, `tex/mat_mortar_BaseColor.png`, `tex/mat_bronze_BaseColor.png`, `tex/mat_water_BaseColor.png`, `tex/mat_soil_BaseColor.png`, `tex/mat_leaf_BaseColor.png`, `tex/mat_wood_BaseColor.png`, `tex/mat_dark_wood_BaseColor.png`, `tex/mat_iron_BaseColor.png`, `tex/mat_glaze_BaseColor.png`.

## Import
Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Results apply to that version and those settings; other engines, Unity versions or import settings may differ. In the raw FBX file frame, the front of each piece faces +Z.

## Known limits
See `HONEST_LOOK.md`. This is deliberate: the sundial plate box fills the recessed hour lines, the planter trough and the cold-frame trough are filled, and the shrub is a simple faceted bush. Real collider gaps: the birdbath mouth, the lavabo mouth, the openings in the trellis lattice, and the opening under the raised cold-frame lid. Collision notes describe the reference shells, which are not included.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. Recorded in REPORT.md and COLD-FRAME-RETEST.md. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale against the kit's 1.5 m grid. Those standard checks passed on all six props. Grid-snap and occlusion-fade checks were skipped: these are props, not wall or floor modules. Extra checks of the birdbath and lavabo mouths, the trellis lattice, the sundial plate fill, and the planter trough fill passed. The opening under the cold-frame lid failed on the first run and again after a thin-panel split. A later box-collider retest of the cold frame only, recorded in COLD-FRAME-RETEST.md, passed: the opening under the raised lid is clear, and the trough and the lid stay solid. Other garden pieces were not rerun. A character-controller probe in edit mode was run at the birdbath.

Play mode, physics, room-adapt scaling, and an on-screen fade were not run. Theme binding used runtime colour-slot blocks, not baked theme assets from a game project. Ray checks used ray and sphere casts against the shipped collision shells, not a gameplay projectile.

## Contents
- `fbx/`: the six models.
- `tex/`: ten optional slot albedos.
- `CONTACT_SHEET.png`: preview of the six assets plus a grid layout (with a 1.8 m reference pole that is not part of the pack) and a 50 mm perspective view from 13 m.
- `HONEST_LOOK.md`: known visual limits. `MANIFEST.json`: file list and per-asset measures. `SHA256SUMS`: hashes for `sha256sum -c`.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
