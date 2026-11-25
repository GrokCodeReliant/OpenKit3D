# Cloister Walk pieces
Six original low-poly pieces for a covered cloister walk: a kit-sized arcade wall, a kit-sized floor tile, a stone bench, a wall-mounted lead rain hopper, a timber alms box, and a long stone trough.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `wall-cloister-arcade` | 2340 | 1.50 × 3.00 × 0.34 | 1 cell | Kit-sized stone wall with slim piers, imposts, and an open pointed two-centred arch with a full-thickness voussoir ring. The archway is a real gap. |
| `tile-cloister-floor` | 376 | 1.50 × 0.12 × 1.50 | 1 cell | Kit-sized floor tile with a mortar bed, a border, a 2-by-2 inner field and a flush iron diamond. This is deliberate: the solid cell collider fills the joints and the inlay. |
| `prop-cloister-bench-stone` | 196 | 1.24 × 0.50 × 0.36 | 1 cell | Backless stone slab on two solid ends, with iron pins on the seat. The space under the slab is a real gap. |
| `prop-cloister-hopper` | 332 | 0.48 × 1.66 × 0.34 | 1 cell | Wall-mounted flared lead rain hopper, with iron brackets to the back plane, a downpipe and a shoe discharging into the walk. This is deliberate: the funnel mouth is a shallow recess and is filled. |
| `prop-alms-box-wood` | 272 | 0.40 × 1.04 × 0.27 | 1 cell | Timber chest on a post and plinth, with an iron strap, a hasp and a coin-slot plate on the lid. This is deliberate: the slot is a shallow recess and is filled. |
| `prop-cloister-trough-stone` | 256 | 1.24 × 0.38 × 0.40 | 1 cell | Long low stone basin with a water disc below the rim and two iron staples on the outer rim. The mouth above the water is a real gap. |

## Conventions
- 1 unit = 1 metre. Grid: 1.5 m cells.
- Pivots: bottom centre on the wall and the four props; floor_top on the floor tile (the walking surface is at z = 0, and the tile extends 0.12 m below). Each piece fits in one 1.5 m cell. In the raw FBX file frame, the front of each piece faces +Z.
- Flat-shaded closed meshes. Each model uses at most 3 material slots, `Primary`, `Secondary` and `Accent`. FBX files are slots-only (no embedded textures, path_mode STRIP). Optional flat BaseColor PNGs live in `tex/`.
- Static meshes only. Nothing is rigged or animated.

## Colour slots
| Asset | `Primary` | `Secondary` | `Accent` | Suggested `tex/` |
|---|---|---|---|---|
| `wall-cloister-arcade` | mortar joints | stone jambs, cap, imposts and voussoirs | iron cap cramps | mortar, stone, iron |
| `tile-cloister-floor` | mortar bed | stone slabs | iron centre diamond | mortar, stone, iron |
| `prop-cloister-bench-stone` | stone ends | stone seat | iron pins | stone, stone, iron |
| `prop-cloister-hopper` | lead hopper body | iron downpipe and shoe | steel brackets and pipe straps | lead, iron, steel |
| `prop-alms-box-wood` | plinth and post | chest, lid and slot recess | iron strap, hasp and slot plate | wood, dark wood, iron |
| `prop-cloister-trough-stone` | stone basin | water | iron rim staples | stone, water, iron |

Texture files: `tex/mat_mortar_BaseColor.png`, `tex/mat_stone_BaseColor.png`, `tex/mat_iron_BaseColor.png`, `tex/mat_lead_BaseColor.png`, `tex/mat_steel_BaseColor.png`, `tex/mat_wood_BaseColor.png`, `tex/mat_dark_wood_BaseColor.png`, `tex/mat_water_BaseColor.png`.

## Import
Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Results apply to that version and those settings; other engines, Unity versions or import settings may differ. In the raw FBX file frame, the front of each piece faces +Z.

## Known limits
See `HONEST_LOOK.md`. This is deliberate: the floor joints and the centre inlay are filled, the hopper funnel mouth is filled, and the alms-box coin slot is a shallow filled recess. Real collider gaps: the arcade opening, the space under the bench slab, the space around the hopper pipe, and the trough mouth above the water. Collision notes describe the reference shells, which are not included.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. Recorded in REPORT.md and CLOISTER.md. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale and grid snap against the kit's 1.5 m floor. Those standard checks passed on all six pieces. The arcade wall snapped between kit stone walls and passed a logic occlusion-fade check. The pointed-arch opening stayed clear (rays, 1 cm and 3 cm probes, and a character-controller walk-through). The floor tile is solid at the walking surface and snaps in a kit floor ring. Gaps under the bench slab and at the trough mouth stayed open. The alms-box coin slot is filled, as authored. The hopper's back plane sits flush on the kit wall face.

Play mode, physics, room-adapt scaling, and an on-screen fade were not run (the fade check was a logic test only). Theme binding used runtime colour-slot blocks, not baked theme assets from a game project. Ray checks used ray and sphere casts against the shipped collision shells, not a gameplay projectile.

## Contents
- `fbx/`: the six models.
- `tex/`: eight optional slot albedos.
- `CONTACT_SHEET.png`: preview of the six assets plus a grid layout (with a 1.8 m reference pole that is not part of the pack) and a 50 mm perspective view from 13 m.
- `HONEST_LOOK.md`: known visual limits. `MANIFEST.json`: file list and per-asset measures. `SHA256SUMS`: hashes for `sha256sum -c`.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
