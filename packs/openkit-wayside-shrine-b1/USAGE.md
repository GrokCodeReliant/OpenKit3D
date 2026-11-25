# Usage

## Import
1. Import `fbx/<asset>.fbx` with scale factor 1. Recommended for Unity, leave "Convert Units" on and turn on "Bake Axis Conversion" if your version offers it. The front of each prop faces +Z.
2. Map the `Primary`, `Secondary` and `Accent` slots to your own materials. No textures are needed.
3. `glb/<asset>.glb` holds the same meshes for glTF engines and web viewers.

## Colliders
Each prop has box colliders that wrap its body. They are given twice:
- `collision/fbx/<asset>-col.fbx` and `collision/glb/<asset>-col.glb`: one closed box mesh per collider, same pivot as the model. Import them next to the model and use them as collision only (for example, a Mesh Collider per box, with no renderer).
- `collision/colliders.json`: the same boxes as `center` and `size` in metres (glTF axes: x right, y up, z toward the front). Every box is centred on x = 0, so a left/right axis flip on import does not move it. If your engine's front is −z, negate the z of `center`. Only the shrine plinth has a non-zero z (−0.02).

| Asset | Boxes | Suggested use |
|---|---:|---|
| `prop-wayside-shrine-stone` | 3 (plinth, walls, roof) | Blocking |
| `prop-holy-water-font` | 3 (base, shaft, basin) | Blocking |
| `prop-votive-candle-rack` | 1 (stand and shelves) | Blocking or none |
| `prop-offering-bowl-stone` | 2 (stand, dish) | Optional |

The boxes are solid blocks around each prop's main volumes. They fill the open spaces too: the shrine niche, the font basin, the dish bowl and the space under the rack shelves are all solid collision. Nothing is walkable or enterable, and items or physics objects will not settle inside the basin or dish. The shrine's roof box is a full block from the wall tops to the ridge, so it also fills the air above the sloped eaves. A few small details sit just outside the boxes: candle tips above the rack's top rail, and the thin collar ring at the bottom of the font's shaft.

## Camera fade (shrine)
`prop-wayside-shrine-stone` is split into three child nodes:
- `prop-wayside-shrine-stone-wall`: back wall, side walls, front pilasters, lintel and gable.
- `prop-wayside-shrine-stone-roof`: the pitched roof and ridge cap.
- `prop-wayside-shrine-stone-base`: plinth, sill, stele and cups.

If your camera fades or dithers geometry between itself and the player, mark the `-wall` and `-roof` nodes as occluders and leave `-base` solid. Each node is its own renderer, so the fade can be applied per renderer without touching the collider. Use a fade-capable material on those two nodes, or let your fade system swap it at runtime. The other three props are small enough that they normally stay solid.

## Colour slots
| Slot | Shrine, dish, font | Candle rack |
|---|---|---|
| Primary | Stone | Wax |
| Secondary | Dark stone or slate | Wood |
| Accent | Iron or bronze trim, coins | Iron trays and rail |

## Rebuild
`blender -b -P source/build_wayside_shrine.py -- <output folder>` (made and tested with Blender 5.2) writes every model, collision mesh and `colliders.json`.
