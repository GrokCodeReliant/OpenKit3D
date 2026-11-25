# Keep Stable pieces
Ten original low-poly pieces for a keep or yard stable: three kit-sized wall modules (a stall front, a split door and a hay hatch), a kit-sized packed-earth floor tile, a free-standing manger, a saddle rack, a bridle peg rail, a watering tub, a tack bench, and a blanket rail.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `wall-stable-stall` | 2084 | 1.50 × 3.00 × 0.34 | 1 cell | Kit-sized stone wall with a timber breast about 1.16 m high, a slatted manger pocket on the room face, and an open bay above the breast. The upper bay is a real gap. This is deliberate: the manger pocket is filled by the solid breast collider. |
| `wall-stable-door` | 1476 | 1.50 × 3.00 × 0.34 | 1 cell | Kit-sized stone wall with a split stable door: a closed lower timber leaf with iron hinges and a latch, and an open upper leaf. The upper opening is a real gap. The lower leaf does not swing. |
| `wall-stable-hay-hatch` | 1556 | 1.50 × 3.00 × 0.34 | 1 cell | Kit-sized stone wall with a high square hay hatch that does not reach the floor, a timber lining, and a shutter parked to the side. The hatch opening is a real through-gap. |
| `tile-stable-floor` | 384 | 1.50 × 0.12 × 1.50 | 1 cell | Kit-sized packed-earth floor tile with a stone border, one straight gutter with a small square iron catch. This is deliberate: the solid cell collider fills the joints and the gutter. |
| `prop-manger-wood` | 528 | 1.10 × 0.92 × 0.48 | 1 cell | Free-standing V-shaped slatted timber hay manger on two posts, with a little hay and iron pins on the posts. The mouth above the slats is a real gap. |
| `prop-saddle-rack-wood` | 364 | 0.74 × 1.22 × 0.46 | 1 cell | Standing two-post timber rack with a top rail and a sloped rest bar. The rack is empty. |
| `prop-bridle-peg-rail` | 524 | 1.14 × 1.40 × 0.24 | 1 cell | Free-standing timber rail on two posts, with five pegs facing the room. The pegs are empty. |
| `prop-watering-tub-wood` | 376 | 0.74 × 0.34 × 0.74 | 1 cell | Low round timber drinking tub with iron hoops and a water disc below the rim. This is deliberate: the mouth is filled by the solid collider. |
| `prop-tack-bench-wood` | 416 | 1.00 × 0.78 × 0.36 | 1 cell | Short timber bench with a lower tray, four legs, and a low back rail. The space between the seat and the tray is a real gap. |
| `prop-blanket-rail-wood` | 352 | 1.22 × 1.34 × 0.12 | 1 cell | Two timber posts with a high bar and a lower bar, and iron ferrules on the posts. The rails are empty. |

## Conventions
- 1 unit = 1 metre. Grid: 1.5 m cells.
- Pivots: bottom centre on the three walls and the six props; floor_top on the floor tile (the walking surface is at z = 0, and the tile extends 0.12 m below). Each piece fits in one 1.5 m cell. Facing in the raw FBX (Y-up): the stall opening and manger pocket, the split door, and the hay hatch face −Z, the room side. The manger mouth, the saddle rest, the pegs, the tub mouth, the bench front and the blanket rail also face −Z. The floor tile has no one-sided front. In the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1), the room side measured at Unity +Z. Results apply to that version and those settings; other engines, Unity versions or import settings may differ. (The glTF/GLB exports, which use +Z for the room side, are not included in this pack.)
- Flat-shaded closed meshes. Each model uses at most 3 material slots, `Primary`, `Secondary` and `Accent`. FBX files are slots-only (no embedded textures, path_mode STRIP). Optional flat BaseColor PNGs live in `tex/`.
- Static meshes only. Nothing is rigged or animated.

## Colour slots
| Asset | `Primary` | `Secondary` | `Accent` | Suggested `tex/` |
|---|---|---|---|---|
| `wall-stable-stall` | stone | timber breast, manger slats | iron tying ring and pins | stone, wood, iron |
| `wall-stable-door` | stone | lower leaf and transom | iron hinges and latch | stone, wood, iron |
| `wall-stable-hay-hatch` | stone | hatch lining and parked shutter | iron hinges and stay | stone, wood, iron |
| `tile-stable-floor` | packed earth | stone border | iron grate | earth, stone, iron |
| `prop-manger-wood` | timber frame and slats | hay | iron post pins | wood, straw, iron |
| `prop-saddle-rack-wood` | posts and top rail | sloped rest | iron pins | wood, dark wood, iron |
| `prop-bridle-peg-rail` | posts and beam | pegs | iron post bands | wood, dark wood, iron |
| `prop-watering-tub-wood` | timber staves | water | iron hoops | wood, water, iron |
| `prop-tack-bench-wood` | legs and back rail | seat and tray | iron seat pins | wood, dark wood, iron |
| `prop-blanket-rail-wood` | posts | the two bars | iron ferrules | wood, dark wood, iron |

Texture files: `tex/mat_earth_BaseColor.png`, `tex/mat_stone_BaseColor.png`, `tex/mat_iron_BaseColor.png`, `tex/mat_wood_BaseColor.png`, `tex/mat_dark_wood_BaseColor.png`, `tex/mat_straw_BaseColor.png`, `tex/mat_water_BaseColor.png`.

## Import
Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Other importers may need different settings. See Conventions for facing in both the raw FBX and Unity frames.

## Known limits
See `HONEST_LOOK.md`. This is deliberate: the stall manger pocket is filled by the solid breast collider, the floor joints and the gutter are filled, and the tub mouth is filled by the solid collider. Real collider gaps: the stall's upper bay, the door's upper-leaf opening, the hay hatch, the mouth above the manger slats, the space between the tack-bench seat and the tray, and the space between the blanket-rail bars. Collision notes describe the reference shells, which are not included.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, colliders from the reference collision shells (not included in this pack), and colour-slot theme binding, and checked room scale on all ten pieces and grid snap on the three walls and the floor tile against the kit's 1.5 m floor and wall. Those checks passed. A logic occlusion-fade check passed on the three wall modules. In baked Unity world coordinates the room side measured at Unity +Z. Rays and 1 cm, 3 cm and 20 cm probes through the stall bay, the upper door opening and the hay hatch passed on both faces. One note: the raw opening check flagged points on the stall and door at one probe-grid row just under the lintel, inside the authored openings. On review that was a test-rule mistake, not a hole in the masonry. The floor tile was solid under all 25 probes, including at the catch. The manger mouth, the filled tub mouth, and the gaps under the tack-bench seat and between the blanket-rail bars behaved as authored. A CharacterController walk stayed on the floor and was stopped by the stall breast, the lower door leaf, and the wall below the hay hatch.

Play mode and an on-screen fade were not run (the fade check was a logic test only). A general physics test was not run. Room-adapt scaling was not run. Theme binding used runtime colour-slot blocks, not baked theme assets from a game project. Ray checks used ray and sphere casts against those reference collision shells, not a gameplay projectile.

## Contents
- `fbx/`: the ten models.
- `tex/`: seven optional slot albedos.
- `CONTACT_SHEET.png`: preview of the ten assets plus a grid layout (with a 1.8 m reference pole that is not part of the pack) and a 50 mm perspective view from 13 m.
- `HONEST_LOOK.md`: known visual limits. `MANIFEST.json`: file list and per-asset measures. `SHA256SUMS`: hashes for `sha256sum -c`.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
