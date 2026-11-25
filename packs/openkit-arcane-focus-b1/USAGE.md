# Usage

## Import
1. Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Other importers may need different settings. The front of each prop is meant to face +Z.
2. Map the `Primary`, `Secondary` and `Accent` slots to your own materials. No textures are needed. For a glow, give `Accent` an emissive material.
3. `glb/<asset>.glb` holds the same meshes for glTF engines and web viewers.

## Colliders
Every collider is a closed, convex shell. Each is small enough for a convex mesh collider (at most 255 triangles). They are given twice:
- `collision/fbx/<asset>-col.fbx` and `collision/glb/<asset>-col.glb`: one mesh per shell, same pivot as the model. Import them next to the model and use them as collision only, for example a convex Mesh Collider per shell with no renderer.
- `collision/colliders.json`: the same shells as numbers (glTF axes: x right, y up, z toward the front). Box shells also list `center` and `size`. The other shells list their `vertices`, and every shell has `bounds_center` and `bounds_size`. If your engine's front is −z, negate z.

| Asset | Shells | Behaviour |
|---|---:|---|
| `prop-rune-obelisk-stone` | 4 (two base steps, shaft, cap) | Solid and blocking. |
| `prop-crystal-focus-pylon` | 3 (base with small crystals, plinth, claws with main crystal) | Solid and blocking. The gaps between the claws are filled. |
| `prop-scrying-orb-tripod` | 1 (convex hull of the whole stand) | Solid and blocking. The open space between the tripod legs is filled, so nothing can walk or roll under it. |
| `prop-ritual-dais-stone` | 6 (lower step, upper step, four marker stones) | Intended as a walkable static surface. Measured in the files: the upper-step collider top is flat at 0.20 m and each of the two steps is 0.10 m high. Whether a character can step up depends on your controller's step-height and slope settings. A character-controller walk was not run. The four marker stones block. |

The shells are approximate. The raised rune inlays on the obelisk stand about 2 cm proud of its collider. The 5 mm rune ring and seal on the dais sit just above the walkable collider top.

## Colour slots
| Slot | Obelisk, dais | Pylon, orb stand |
|---|---|---|
| Primary | Stone | Stone |
| Secondary | Dark stone | Iron |
| Accent | Rune inlays | Crystal, orb |

## Rebuild
`blender -b -P source/build_arcane_focus.py -- <output folder>` (made and tested with Blender 5.2) writes every model, collision shell and `collision/colliders.json`.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale and grid snap against the kit's 1.5 m floor.
One note: the room-scale check flagged `prop-ritual-dais-stone`, because it compared the dais's declared 2 × 2-cell, 2.80 m footprint with a single 1.5 m floor cell. On review this was a test-rule mistake. The dais imported, sat flat on the floor (base at height 0) and passed the import, prefab, collider, snap and theme checks.

Play mode, physics or ray tests, an on-screen fade, and a character-controller walk or contact test were not run. Whether a character can step onto the dais still depends on your controller's step-height and slope settings.
