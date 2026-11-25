# Chapel Furnishings pieces
Six original low-poly pieces for a chapel interior: two kit-sized wall modules (a piscina niche and an ambry cupboard), a wooden pulpit, a high-backed choir stall, a prie-dieu, and a small credence table.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `wall-chapel-piscina` | 2492 | 1.50 × 3.00 × 0.34 | 1 cell | Kit-sized stone wall with a mid-height basin niche about 0.52 m wide and 0.60 m tall above a visible lip at about 1.0 m, a bowl and an iron drain. This is deliberate: the niche is filled by the solid wall collider. |
| `wall-chapel-ambry` | 2264 | 1.50 × 3.00 × 0.34 | 1 cell | Kit-sized stone wall with a mid-height recessed wooden cupboard, iron hinges and a hasp. This is deliberate: the niche is filled and the door leaf does not swing. |
| `prop-chapel-pulpit-wood` | 468 | 0.76 × 1.66 × 1.28 | 1 cell | Enclosed raised wooden preaching box on four posts, with a short stair, and a sloped book board. The space under the deck between the posts is a real gap. The stair risers are solid. |
| `prop-choir-stall-wood` | 268 | 0.68 × 1.26 × 0.48 | 1 cell | Single high-backed wooden stall with cheek wings and a crest rail. The space under the seat is a real gap. |
| `prop-prie-dieu-wood` | 148 | 0.44 × 0.80 × 0.44 | 1 cell | Low wooden kneeling step, slim uprights, and a sloped book rest at about 0.80 m, with two small iron pins under it. The front and the underside under the rest are real openings. |
| `prop-credence-table-wood` | 292 | 0.68 × 0.99 × 0.36 | 1 cell | Small wooden side table with a lower shelf and two lidded bronze cruets. |

## Conventions
- 1 unit = 1 metre. Grid: 1.5 m cells.
- Pivots: bottom centre on both walls and the four props. Each piece fits in one 1.5 m cell. Facing in the raw FBX (Y-up): the piscina and ambry niches, the stall seat and the prie-dieu kneeling step face −Z; the pulpit's enclosure front faces +Z, with its stair on −Z. Facing after import depends on your importer's axis settings and is not verified here.
- Flat-shaded closed meshes. Each model uses at most 3 material slots, `Primary`, `Secondary` and `Accent`. FBX files are slots-only (no embedded textures, path_mode STRIP). Optional flat BaseColor PNGs live in `tex/`.
- Static meshes only. Nothing is rigged or animated.

## Colour slots
| Asset | `Primary` | `Secondary` | `Accent` | Suggested `tex/` |
|---|---|---|---|---|
| `wall-chapel-piscina` | stone | water | iron | stone, water, iron |
| `wall-chapel-ambry` | stone | wood | iron | stone, wood, iron |
| `prop-chapel-pulpit-wood` | wood | dark wood | iron | wood, dark wood, iron |
| `prop-choir-stall-wood` | wood | dark wood | iron | wood, dark wood, iron |
| `prop-prie-dieu-wood` | wood | dark wood | iron | wood, dark wood, iron |
| `prop-credence-table-wood` | wood | dark wood | bronze | wood, dark wood, bronze |

Texture files: `tex/mat_stone_BaseColor.png`, `tex/mat_water_BaseColor.png`, `tex/mat_iron_BaseColor.png`, `tex/mat_wood_BaseColor.png`, `tex/mat_dark_wood_BaseColor.png`, `tex/mat_bronze_BaseColor.png`.

## Import
Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Results apply to that version and those settings; other engines, Unity versions or import settings may differ. Facing after import is not verified here; see Conventions for the raw-FBX facing.

## Known limits
See `HONEST_LOOK.md`. This is deliberate: the piscina basin niche and the ambry cupboard niche are filled by the solid wall colliders, and the pulpit stair risers are solid. Real collider gaps: the space under the stall seat, the space under the pulpit deck between the posts, the space between the credence legs, and the front and underside of the prie-dieu under the book rest. Collision notes describe the reference shells, which are not included.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. Recorded in REPORT.md and CHAPEL.md. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale and grid snap against the kit's 1.5 m floor. Those standard checks passed on all six pieces. Both wall modules snapped with no gap and passed a logic occlusion-fade check. The piscina and ambry niches are visual only (the wall colliders fill them). Gaps under the credence table and at the front and underside of the prie-dieu passed. The space under the choir-stall seat failed on the first run. A later retest of the stall and credence only, recorded in CHAPEL.md, found the space under the seat open and the seat and plinth solid. Other chapel pieces were not rerun.

Play mode, physics, room-adapt scaling, and an on-screen fade were not run (the fade check was a logic test only). A character-controller contact test was not run. Theme binding used runtime colour-slot blocks, not baked theme assets from a game project. Ray checks used ray and sphere casts against the shipped collision shells, not a gameplay projectile.

## Contents
- `fbx/`: the six models.
- `tex/`: six optional slot albedos.
- `CONTACT_SHEET.png`: preview of the six assets plus a grid layout (with a 1.8 m reference pole that is not part of the pack) and a 50 mm perspective view from 13 m.
- `HONEST_LOOK.md`: known visual limits. `MANIFEST.json`: file list and per-asset measures. `SHA256SUMS`: hashes for `sha256sum -c`.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
