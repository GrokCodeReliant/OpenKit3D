# Using the Farmhouse & Market Equipment props

## Import
1. Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Other importers may need different settings. The front of each prop is meant to face +Z. The churn and quern look the same from every side. The spit and the steelyard frame are meant to be seen from the front, along their long side; the spit crank and the steelyard counterpoise are on the right (+X), the steelyard pan on the left.
2. Assign your own materials to the slots listed under Colour slots below.
3. `glb/<asset>.glb` holds the same meshes for glTF engines and web viewers.

## Colliders
- `collision/fbx/<asset>-col.fbx` and `collision/glb/<asset>-col.glb`: one closed convex mesh per shell, each with at most 255 triangles, in the same space as the model.
- `collision/colliders.json`: the same shells as numbers, in glTF axes (x right, y up, z toward the front). Box shells also list `center` and `size`. The other shells list their `vertices`. Every shell has `bounds_center` and `bounds_size`. If your engine's front is −z, negate z.
- These are mesh files and numbers only. They are not engine collider components; you set those up yourself.

| Asset | Shells | Behaviour of the shells |
|---|---|---|
| `prop-butter-churn-wood` | 2 (body with hoops, ears and lid; dasher handle) | Solid and blocking up to 0.92 m; a thin box covers the dasher handle up to 1.18 m. |
| `prop-hand-quern-stone` | 3 (stand, stones with flour ring, handle peg) | Solid and blocking. The stand is one filled box 0.64 × 0.36 × 0.64 m, so the space between its legs is blocked. |
| `prop-roasting-spit-wood` | 4 (left stand, right stand, spit rod with prongs, crank) | The space under the rod between the two stands is left open for a fire: in the files, the region 0.82 m wide (x from −0.46 to 0.36), 0.50 m deep and up to 0.67 m high contains no collision. The rod shell is a 0.14 m square bar at 0.75 m. |
| `prop-steelyard-scale-frame` | 5 (two side frames, crossbar, steelyard assembly, pan with chains) | The side frames are filled shapes (sill, post and braces). The steelyard assembly shell hangs from 1.41 m to 1.91 m. The pan shell is one cone-like shape from the pan (0.84 m) up to the hook (1.53 m), so the space between the three chains is blocked. Below the pan, between the posts (0.80 m wide, 0.50 m deep, up to 0.80 m high), and beside the pan on the counterpoise side up to 1.30 m, there is no collision. |

The shells are approximate and none of them is meant to be walked on. How a character touches them, and whether one can reach into the open space under the spit or the steelyard pan, depends on your controller and physics settings. A character-controller contact test was not run. The steelyard assembly shell starts at 1.41 m, below the head height of a standing adult, so a character passing between the posts will bump into it.

The steelyard frame (2.00 m) is the tallest piece. It carries no camera-fade marker, and how it occludes a top-down or isometric camera has not been checked.

## Colour slots
| Asset | `Primary` | `Secondary` | `Accent` |
|---|---|---|---|
| `prop-butter-churn-wood` | staves and ears (brown wood) | hoops (dark iron) | lid, splash cup, dasher (pale wood) |
| `prop-hand-quern-stone` | stand and handle peg (brown wood) | quern stones (grey stone) | grain and spilled flour (off-white) |
| `prop-roasting-spit-wood` | stands, legs, crank grip (brown wood) | spit rod, prongs, crank arm (dark iron) | lashings (pale rope) |
| `prop-steelyard-scale-frame` | posts, sills, braces, crossbar (brown wood) | steelyard, hooks, chains, counterpoise (dark iron) | pan (wicker) |

## Rebuilding
`blender -b -P source/build_farmhouse_market.py -- <output folder>` (made and tested with Blender 5.2) writes every model, collision shell and `collision/colliders.json`.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale and grid snap against the kit's 1.5 m floor. Occlusion fade does not apply: these are props, not wall or roof pieces.

Play mode, physics or ray tests, an on-screen fade, and a character-controller walk or contact test were not run. How a character touches the shells, or reaches into the open space under the spit or the steelyard pan, still depends on your controller and physics settings.
