# Using the Hauling & Lifting props

## Import
1. Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Other importers may need different settings. The front of each prop is meant to face +Z. On the windlass, capstan and jib crane, the front is the side the rope or hook faces.
2. Assign your own materials to the slots `Primary` (wood), `Secondary` (iron) and `Accent` (rope).
3. `glb/<asset>.glb` holds the same meshes for glTF engines and web viewers.

## Colliders
- `collision/fbx/<asset>-col.fbx` and `collision/glb/<asset>-col.glb`: one closed convex mesh per shell, each with at most 255 triangles, in the same space as the model.
- `collision/colliders.json`: the same shells as numbers, in glTF axes (x right, y up, z toward the front). Box shells also list `center` and `size`. The other shells list their `vertices`. Every shell has `bounds_center` and `bounds_size`. If your engine's front is −z, negate z.

| Asset | Shells | Behaviour of the shells |
|---|---|---|
| `prop-windlass-wood` | 3 (frame block, one per crank) | Solid and blocking. The open space inside the A-frames is filled by one box. |
| `prop-capstan-wood` | 6 (base, drum, drumhead, two bar boxes, rope lead) | Solid and blocking, including the four push bars at 0.83 m. |
| `prop-jib-crane-wood` | 7 (two sills, braced base, post, post winch, arm assembly, hook column) | Solid and blocking. The braced base is one filled shape. The arm assembly shell starts at about 1.93 m. Below it, the space between the post and the hook column is open. |
| `prop-shaft-hoist-frame-wood` | 10 (four legs, four spreader bars, tackle and hook, hauling line) | Legs, spreaders at 0.45 m, the cleat and the hanging tackle block. The centre under the hook is left without collision: in the files, a 0.40 m × 0.40 m column from the ground up to 1.36 m is clear. The clear square narrows from about 0.96 m wide at 0.1 m height to 0.44 m at 1.36 m, because the legs lean in. |

The shells are approximate and none of them is meant to be walked on. Whether a character can step over the hoist frame's 0.45 m spreader bars, or how it touches any shell, depends on your controller and physics settings. A character-controller contact test was not run.

The jib crane (2.84 m) and the hoist frame (2.56 m) are tall. They carry no camera-fade marker, and how they occlude a top-down or isometric camera has not been checked.

## Colour slots
| Slot | Used for | Preview colour |
|---|---|---|
| `Primary` | timber: frames, drums, post, arm, legs, grips | warm brown |
| `Secondary` | iron: axles, bearings, ratchet, bands, blocks, hooks, shoes | dark grey |
| `Accent` | rope | pale hemp |

## Rebuilding
`blender -b -P source/build_hauling_lifting.py -- <output folder>` (made and tested with Blender 5.2) writes every model, collision shell and `collision/colliders.json`.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale and grid snap against the kit's 1.5 m floor. Occlusion fade does not apply: these are props, not wall or roof pieces.

Play mode, physics or ray tests, an on-screen fade, and a character-controller walk or contact test were not run. How a character touches the shells, or steps over the hoist frame's spreader bars, still depends on your controller and physics settings.
