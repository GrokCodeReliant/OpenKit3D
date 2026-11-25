# Using the Gaol Cell pieces

## Import
1. Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Other importers may need different settings. The front of each piece faces +Z.
2. Assign your own materials to the slots listed under Colour slots below.
3. `glb/<asset>.glb` holds the same meshes for glTF engines and web viewers.

## Placing
- Floor tiles: place on the 1.5 m grid like the kit's stone floor tile. The walking surface is at height 0; nothing on the tile rises above it.
- Wall: place on a cell edge like the kit's stone wall module. Its width, height and thickness match that module, and its block courses and cap course line up with it.
- Stocks: stand on any floor cell. They fit inside one cell, leaving 0.05 m at each end of the long side.

## Colliders
- `collision/fbx/<asset>-col.fbx` and `collision/glb/<asset>-col.glb`: one closed convex mesh per shell, each with at most 255 triangles, in the same space as the model.
- `collision/colliders.json`: the same shells as numbers, in glTF axes (x right, y up, z toward the front). Box shells also list `center` and `size`. The other shells list their `vertices`. Every shell has `bounds_center` and `bounds_size`.
- These are mesh files and numbers only. They are not engine collider components; you set those up yourself.

| Asset | Shells | Behaviour of the shells |
|---|---|---|
| `tile-dungeon-floor-grate` | 1 box | Solid ground for the whole cell, top at the walking surface. The sump under the grate is filled, so nothing falls into it. |
| `tile-dungeon-floor-trapdoor` | 1 box | Solid ground for the whole cell, top at the walking surface. The hatch is closed and is walked over like the rest of the floor. |
| `wall-dungeon-cell-bars` | 6 (two jambs, sill, lintel, cap course, bar panel) | Solid and blocking. The bars are covered by one thin solid panel 0.07 m deep, so characters cannot pass between them. Whether rays, arrows or spells pass through the gaps is up to your own setup. |
| `prop-stocks-wood` | 4 (feet, main frame, two brace pairs) | Solid and blocking. The leg holes are closed by the collision. |

## Camera fade
`wall-dungeon-cell-bars` is a wall piece and its name contains `wall`, so a camera fader that matches structural pieces by name (wall, pillar, roof) picks it up the same way as the kit's other wall modules. It uses the same three slot materials as those walls, with no special material of its own. The floor tiles are named `tile-...` and carry `floor`, so a fader that skips floors leaves them alone. The stocks are a prop and are not meant to fade. The cell-bars wall passed that fade logic test in the Unity test of 2026-11-25; an on-screen fade in play mode was not run.

## Colour slots
| Asset | `Primary` | `Secondary` | `Accent` |
|---|---|---|---|
| `tile-dungeon-floor-grate` | joint bed and sump floor (dark mortar) | slabs (grey stone) | frame and grate bars (dark iron) |
| `tile-dungeon-floor-trapdoor` | hatch planks (brown wood) | slabs and bed (grey stone) | curb, straps, hinges and ring (dark iron) |
| `wall-dungeon-cell-bars` | jamb cores (dark mortar) | jamb blocks, sill, lintel and cap course (grey stone) | bars and cross straps (dark iron) |
| `prop-stocks-wood` | feet, sill, uprights, braces and cap rail (brown wood) | yoke boards (dark wood) | cap bands, hasp, padlock and hinge strap (dark iron) |

## Rebuilding
`blender -b -P source/build_gaol_cells.py -- <output folder>` (made and tested with Blender 5.2) writes every model, collision shell and `collision/colliders.json`.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale and grid snap against the kit's 1.5 m floor and wall. One note: the room-scale check flagged the two floor tiles for extending 0.12 m below the floor. On review that is the kit's floor-top pivot (walking surface at height 0), the same as the kit's stone floor. The cell-bars wall passed a camera-fade logic test: the fade value was applied and read back. No on-screen fade was drawn.

Play mode, physics or ray tests, room-adapt scaling, an on-screen fade, and a character-controller walk or contact test were not run.
