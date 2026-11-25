# Keep / Gatehouse pieces

Six original low-poly pieces for a dungeon keep or gatehouse: three wall modules, two walkable floor tiles and one floor prop.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `wall-dungeon-portcullis` | 1088 | 1.50 × 3.00 × 0.34 | 1 cell edge | Wall module with a closed iron portcullis in a stone arch: jambs, sill, lintel, cap course, eight pointed verticals and five rails. It does not open. |
| `wall-dungeon-arrow-slit` | 1540 | 1.50 × 3.00 × 0.34 | 1 cell edge | Wall module with a tall splayed loophole that widens toward the front face and narrows to a slim slot at the back, coursed stone, cap course and a small iron sighting lip at the back. |
| `wall-dungeon-window-bars` | 1364 | 1.50 × 3.00 × 0.34 | 1 cell edge | Solid wall module with a small high window: stone sill and lintel, five round bars and two straps. |
| `tile-dungeon-floor-channel` | 624 | 1.50 × 0.12 × 1.50 | 1 cell | Stone floor tile with a front-to-back open gutter, iron lips, end straps and a dark silt surface. The gutter is shallow. |
| `tile-dungeon-floor-pressure-plate` | 560 | 1.50 × 0.12 × 1.50 | 1 cell | Stone floor tile with a closed centre plate, 0.8 mm proud, a joint gap around it, four corner rivets and a faint centre seam. The plate does not move. |
| `prop-cresset-iron` | 800 | 0.44 × 1.54 × 0.43 | 1 cell | Standing iron fire basket: three splayed legs on a ring base, a post, a banded basket with a grate and four coals. |

## Conventions
- 1 unit = 1 metre. Grid: 1.5 m cells.
- Pivots: the walls and the cresset use bottom centre. The two floor tiles use the kit's floor-top pivot: the walking surface is at height 0 and the tile extends 0.12 m below it, the same as the kit's stone floor tile. The pressure plate is 0.8 mm proud of that plane.
- The wall modules have the same size as the kit's stone wall module (1.5 × 3.0 × 0.34 m), so they can sit in a run of those walls. Facing in the raw FBX (Y-up): the arrow-slit's wide splay is on +Z, and the slim slot and iron lip are on −Z. The portcullis and the barred window have no one-sided front. In Build's baked world-coordinate check on 25 Nov 2026 (Unity 6000.4.0f1, Convert Units on, Bake Axis Conversion on), the wide splay was on Unity +Z, the front; other importers or settings may differ.
- Flat-shaded closed meshes. Stone blocks and slabs have chamfered edges like the kit's own stone modules. Each model uses at most 3 material slots, `Primary`, `Secondary` and `Accent`.
- FBX files are slots-only (no embedded textures, path_mode STRIP). Optional flat BaseColor PNGs in `tex/` can be assigned in engine.
- Static meshes only. Nothing is rigged or animated.

## Colour slots
| Asset | `Primary` | `Secondary` | `Accent` | Suggested `tex/` |
|---|---|---|---|---|
| `wall-dungeon-portcullis` | jamb cores (dark mortar) | jamb blocks, sill, lintel and cap (grey stone) | guides, bars and rails (dark iron) | mortar, stone, iron |
| `wall-dungeon-arrow-slit` | mortar cores | masonry and splayed cheeks (grey stone) | iron sighting lip | mortar, stone, iron |
| `wall-dungeon-window-bars` | mortar cores | masonry, sill, lintel and cap (grey stone) | bars and straps (dark iron) | mortar, stone, iron |
| `tile-dungeon-floor-channel` | joint bed and silt (dark mortar) | slabs and channel cheeks (grey stone) | iron lip and end straps | mortar, stone, iron |
| `tile-dungeon-floor-pressure-plate` | joint bed (dark mortar) | slabs and centre plate (grey stone) | rivets and centre seam (dark iron) | mortar, stone, iron |
| `prop-cresset-iron` | legs, feet and post (dark iron) | collar, hoops, straps, lip and grate (steel) | coals (ember) | iron, steel, ember |

Texture files: `tex/mat_mortar_BaseColor.png`, `tex/mat_stone_BaseColor.png`, `tex/mat_iron_BaseColor.png`, `tex/mat_steel_BaseColor.png`, `tex/mat_ember_BaseColor.png`.

## Import
Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Results apply to that version and those settings; other engines, Unity versions or import settings may differ. Facing after import is otherwise not verified here; see Conventions for the raw-FBX facing and for that reported check.

## Known limits
See `HONEST_LOOK.md`. The portcullis is closed and does not open. The pressure plate is only 0.8 mm proud, so it is easy to miss from a typical camera. Collision shells are not part of this pack folder.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. Recorded in REPORT.md and SLIT-R6.md. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale and grid snap against the kit's 1.5 m floor. Those standard checks passed on all six pieces. A logic occlusion-fade check passed on the three wall modules. A pressure-plate depth check passed. Rays against the shipped solid collision panels of the portcullis, slit and window bars passed after a later retest of a revised symmetric collision shell; a first run of that panel-ray check had failed. A later arrow-slit retest, recorded in SLIT-R6.md, passed on slit rays (1 cm and 3 cm clear, 20 cm blocked) and a masonry-leak check on both faces of the slit. Other gatehouse pieces were not rerun in that later slit retest.

Play mode, physics, room-adapt scaling, and an on-screen fade were not run (the fade check was a logic test only). A character-controller contact test was not run. Theme binding used runtime colour-slot blocks, not baked theme assets from a game project. Ray checks used ray and sphere casts against the shipped collision shells, not a gameplay projectile. Visual gaps in the portcullis and window bars are not in the stock collision; with the shipped solid panels, rays are blocked.

## Contents
- `fbx/`: the six models.
- `tex/`: five optional slot albedos.
- `CONTACT_SHEET.png`: preview of the six assets plus a grid layout (with a 1.8 m reference pole that is not part of the pack) and a collision-shell view.
- `HONEST_LOOK.md`: known visual limits. `MANIFEST.json`: file list and per-asset measures. `SHA256SUMS`: hashes for `sha256sum -c`.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
