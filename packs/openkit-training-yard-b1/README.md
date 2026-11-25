# Training Yard props

Four original low-poly pieces of martial practice equipment for a castle yard, barracks, guild hall, militia camp or tournament ground.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `prop-pell-post-wood` | 220 | 0.92 × 1.80 × 0.92 | 1 cell | Heavy square practice post with a chamfered top, set in a braced timber cross foot. Pale hack scars on the front and right faces show where blades have struck. |
| `prop-quintain-wood` | 376 | 1.34 × 1.86 × 0.96 | 1 cell | Pivot-post quintain: a post on a braced cross foot with an iron pivot cap carrying a long swing arm. A shield board with a boss hangs from straps at the left end and a sandbag hangs from a chain at the right. |
| `prop-training-dummy-straw` | 624 | 0.88 × 1.71 × 0.80 | 1 cell | Straw-stuffed practice figure: a bound straw body and sack head on a post, with a cross arm bar wrapped in straw, standing on a braced cross foot. No hat or clothes. |
| `prop-armor-stand-wood` | 648 | 0.68 × 1.71 × 0.68 | 1 cell | Armour stand: a post and shoulder bar on a braced cross foot, dressed with a cuirass, skirt lames, a leather belt with buckle, shoulder straps, two pauldrons and a rounded helm. |

## Conventions
- 1 unit = 1 metre. The pivot is at the bottom centre, with the base resting on the ground.
- Flat-shaded closed meshes, no textures. Each model uses at most 3 material slots, `Primary`, `Secondary` and `Accent`, so you can map them onto your own palette. What each slot stands for differs per model; see `USAGE.md`.
- Grid: 1.5 m cells. Each prop fits inside one cell.
- Static meshes only. Nothing is rigged or animated; the quintain arm does not swing.
- Formats: FBX and GLB.
- Unity import test passed (the Open Kit team's engine test, 25 Nov 2026, Unity 6000.4.0f1, scale 1 with Convert Units and Bake Axis Conversion on). Other engines, Unity versions or import settings may give different results. See `USAGE.md` for what was run and what was not.

## Contents
- `fbx/`, `glb/`: the models.
- `collision/`: convex collision shells (`fbx/`, `glb/`) and `colliders.json`, which holds the same shells as plain numbers.
- `renders/`, `CONTACT_SHEET.png`: preview images, including a grid layout with a plain 1.8 m reference pole (not part of the pack) and a view of the collision shells.
- `source/build_training_yard.py`: the Blender Python script that builds every model and collision shell in this folder.
- `USAGE.md`: import, colliders and colour slots.
- `MANIFEST.json`: file list with sizes and SHA-256 hashes.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
