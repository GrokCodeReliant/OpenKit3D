# Crypt / Undercroft pieces

Six original low-poly pieces for a dungeon crypt or undercroft: one wall module, one walkable floor tile and four floor props. This is not another keep / gatehouse set.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `wall-dungeon-fountain` | 1528 | 1.50 × 3.00 × 0.34 | 1 cell edge | Kit-sized stone wall module with a recessed spout and basin (the bowl is cut into the 0.34 m thickness, not a projecting fountain). Dark water sits in the bowl. The basin is filled by the collider. |
| `prop-cistern-stone` | 372 | 1.16 × 1.00 × 1.16 | 1 cell | Open masonry water tank with a short plinth, two iron bands and a dark water plane 0.30 m below the rim. Not a well: no winch, no raised parapet, no bucket rope. The mouth is a real opening. |
| `prop-urn-stone` | 460 | 0.36 × 0.90 × 0.36 | 1 cell | Closed lidded stone burial urn on a square plinth, with an iron lid band and a small finial. It does not open; no remains are modelled. |
| `prop-ossuary-cist` | 324 | 0.90 × 0.48 × 0.55 | 1 cell | Closed stone ossuary chest on four short feet, with a slightly oversized lid and three iron straps. No bones or opening. The space between the legs is a real gap. |
| `tile-dungeon-floor-memorial` | 628 | 1.50 × 0.12 × 1.50 | 1 cell | Walkable 1.5 m floor tile. A 2.2 cm recessed field, an incised border and a bronze rosette sit below the walking surface (the rosette top is 8 mm below z = 0) so the carving stays readable from a 13 m camera without breaking the floor-top pivot. |
| `prop-sluice-gate` | 352 | 1.06 × 1.14 × 0.32 | 1 cell | Small timber-framed drainage sluice on a stone sill, with a raised iron plate and a clear opening under it. Not a keep portcullis: no arch, no pointed bars, about 1.1 m tall. |

## Conventions
- 1 unit = 1 metre. Grid: 1.5 m cells.
- Pivots: the wall and the four props use bottom centre. The memorial tile uses the kit's floor-top pivot: the walking surface is at height 0 and the tile extends 0.12 m below it. The carving is recessed below that plane.
- The fountain wall has the same size as the kit's stone wall module (1.5 × 3.0 × 0.34 m). Facing in the raw FBX (Y-up): the basin faces −Z. The basin is a recess in that thickness, not a projection. In the engine test of 25 Nov 2026 (Unity 6000.4.0f1, Convert Units on, Bake Axis Conversion on), the basin was on Unity +Z; other importers or settings may differ.
- Flat-shaded closed meshes. Each model uses at most 3 material slots, `Primary`, `Secondary` and `Accent`.
- FBX files are slots-only (no embedded textures, path_mode STRIP). Optional flat BaseColor PNGs in `tex/` can be assigned in engine.
- Static meshes only. Nothing is rigged or animated.

## Colour slots
| Asset | `Primary` | `Secondary` | `Accent` | Suggested `tex/` |
|---|---|---|---|---|
| `wall-dungeon-fountain` | mortar cores | masonry, basin and spout | water in the bowl | mortar, stone, water |
| `prop-cistern-stone` | plinth and iron bands | tank wall | water in the mouth | mortar, stone, water |
| `prop-urn-stone` | square plinth | urn body and lid | lid band and finial | mortar, stone, iron |
| `prop-ossuary-cist` | feet | body and lid | straps and handles | mortar, stone, iron |
| `tile-dungeon-floor-memorial` | mortar bed, recessed field and border | surrounding slabs | bronze rosette | mortar, stone, bronze |
| `prop-sluice-gate` | timber stiles and lintel | stone sill | iron plate and guides | wood, stone, iron |

Texture files: `tex/mat_mortar_BaseColor.png`, `tex/mat_stone_BaseColor.png`, `tex/mat_iron_BaseColor.png`, `tex/mat_wood_BaseColor.png`, `tex/mat_water_BaseColor.png`, `tex/mat_bronze_BaseColor.png`.

## Import
Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Results apply to that version and those settings; other engines, Unity versions or import settings may differ. Facing after import is otherwise not verified here; see Conventions for the raw-FBX facing and for that reported check.

## Known limits
See `HONEST_LOOK.md`. The fountain basin and the memorial carving are visual recesses filled by collision (solid panels on purpose). The cistern mouth and the opening under the sluice plate are real gaps, as are the spaces between the cist's legs. Collision shells are not part of this pack folder.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. Recorded in REPORT.md and CRYPT-ROSETTE.md. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale and grid snap against the kit's 1.5 m floor. Those standard checks passed on all six pieces. A logic occlusion-fade check passed on the fountain wall. Openings at the sluice and the cistern mouth were checked. A character-controller probe in edit mode was run on the cist. A later retest of the memorial floor tile only, recorded in CRYPT-ROSETTE.md, found that the tile sits at the kit floor-top (the walking surface at height 0, the tile 0.12 m below), that its collider is solid at the walking surface over the 8 mm carving, and that feet will appear to sink by that amount, which is expected. Other crypt pieces were not rerun in that launch.

Play mode, physics, room-adapt scaling, and an on-screen fade were not run (the fade check was a logic test only). Theme binding used runtime colour-slot blocks, not baked theme assets from a game project. Ray checks used ray and sphere casts against the shipped collision shells, not a gameplay projectile.

## Contents
- `fbx/`: the six models.
- `tex/`: six optional slot albedos.
- `CONTACT_SHEET.png`: preview of the six assets plus a grid layout (with a 1.8 m reference pole that is not part of the pack) and a 50 mm perspective view from 13 m.
- `HONEST_LOOK.md`: known visual limits. `MANIFEST.json`: file list and per-asset measures. `SHA256SUMS`: hashes for `sha256sum -c`.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
