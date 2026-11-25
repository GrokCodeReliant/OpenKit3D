# Using the Training Yard props

## Import
1. Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Other importers may need different settings. The front of each prop is meant to face +Z. The pell's hack scars are on the front and right (+X) faces. The quintain is meant to be seen from the front, along its arm: the shield board (boss facing front) is on the left (−X) and the sandbag on the right (+X). The dummy and the armour stand face front; their arms and pauldrons run along X.
2. Assign your own materials to the slots listed under Colour slots below.
3. `glb/<asset>.glb` holds the same meshes for glTF engines and web viewers.

## Colliders
- `collision/fbx/<asset>-col.fbx` and `collision/glb/<asset>-col.glb`: one closed convex mesh per shell, each with at most 255 triangles, in the same space as the model.
- `collision/colliders.json`: the same shells as numbers, in glTF axes (x right, y up, z toward the front). Box shells also list `center` and `size`. The other shells list their `vertices`. Every shell has `bounds_center` and `bounds_size`. If your engine's front is −z, negate z.
- These are mesh files and numbers only. They are not engine collider components; you set those up yourself.

| Asset | Shells | Behaviour of the shells |
|---|---|---|
| `prop-pell-post-wood` | 2 (cross foot with braces; post) | Solid and blocking. The foot shell is one filled shape 0.92 × 0.58 × 0.92 m, so the space between the braces is blocked. The post shell is a 0.22 m square box up to 1.80 m. |
| `prop-quintain-wood` | 5 (cross foot with braces; post; pivot cap with swing arm; shield board; chain with sandbag) | The foot shell is filled up to 0.60 m. The arm shell runs from 1.59 m to 1.86 m. The space under the arm on both sides of the post is left open: in the files, x from 0.36 to 0.64 m (under the sandbag, z up to 0.90 m) and x from −0.64 to −0.36 m (under the shield, up to 1.08 m), 0.40 m deep, from 0.35 m upward, contain no collision. The braced foot still blocks the lowest part near the post. |
| `prop-training-dummy-straw` | 5 (cross foot with braces; post; body with bindings; arm bar with straw arms; head) | Solid and blocking. |
| `prop-armor-stand-wood` | 4 (cross foot with braces; post; armour body with pauldrons and shoulder bar; helm) | Solid and blocking. The armour shell is one filled shape from 0.78 m to 1.43 m. |

The shells are approximate and none of them is meant to be walked on. How a character or weapon touches them depends on your controller and physics settings. A character-controller contact test was not run. The quintain arm (1.59–1.86 m) and its shield board (from 1.17 m) and sandbag (from 0.98 m) are at head and chest height of a standing adult, so a character walking under the arm beside the post will bump into them.

All four pieces are 1.7–1.9 m tall. None carries a camera-fade marker, and how they occlude a top-down or isometric camera has not been checked.

## Colour slots
| Asset | `Primary` | `Secondary` | `Accent` |
|---|---|---|---|
| `prop-pell-post-wood` | post and chamfered top (brown wood) | cross foot and braces (dark timber) | hack scars (pale fresh wood) |
| `prop-quintain-wood` | foot, braces, post, swing arm, shield board (brown wood) | pivot cap, pin, straps, chain, shield boss (dark iron) | sandbag (burlap) |
| `prop-training-dummy-straw` | foot, braces, post, arm bar (brown wood) | body bindings, arm ties, neck tie (rope) | body, head, top knot, straw arms (straw) |
| `prop-armor-stand-wood` | foot, braces, post, shoulder bar (brown wood) | cuirass, skirt lames, buckle, pauldrons, helm and brim (steel) | belt and shoulder straps (leather) |

## Rebuilding
`blender -b -P source/build_training_yard.py -- <output folder>` (made and tested with Blender 5.2) writes every model, collision shell and `collision/colliders.json`. A rebuild gives byte-identical GLB files and `colliders.json`; the FBX files differ only in the creation time stamp the exporter writes into the header.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale and grid snap against the kit's 1.5 m floor. Occlusion fade does not apply: these are props, not wall or roof pieces.

Play mode, physics or ray tests, an on-screen fade, and a character-controller walk or contact test were not run. How a character or weapon touches the shells still depends on your controller and physics settings.
