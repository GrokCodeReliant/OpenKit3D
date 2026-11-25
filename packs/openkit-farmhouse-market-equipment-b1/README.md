# Farmhouse & Market Equipment props

Four original low-poly pieces of food-preparation and market equipment for farmhouses, kitchens, camps, village markets or a castle larder.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `prop-butter-churn-wood` | 432 | 0.42 × 1.18 × 0.40 | 1 cell | Tall staved dash churn that narrows toward the top, with three iron hoops, two long staves as lifting ears, a pale wooden lid with a splash cup and a dasher handle with a cross grip. |
| `prop-hand-quern-stone` | 340 | 0.64 × 0.79 × 0.64 | 1 cell | Rotary hand quern on a low four-legged stand: a bed stone and a runner stone with a central eye holding grain, an upright wooden handle peg, and a ring of spilled flour. |
| `prop-roasting-spit-wood` | 268 | 1.26 × 0.87 × 0.49 | 1 cell | Open-fire roasting spit: two forked stands on splayed legs, lashed with rope, carrying an iron spit rod with two meat prongs and a crank. The space under the rod is open; no fire is included. |
| `prop-steelyard-scale-frame` | 412 | 1.16 × 2.00 × 0.60 | 1 cell | Market weighing frame: two braced posts on foot sills and a crossbar, from which hangs an iron steelyard with notches, a pear-shaped counterpoise and a wicker pan on three chains. |

## Conventions
- 1 unit = 1 metre. The pivot is at the bottom centre, with the base resting on the ground.
- Flat-shaded closed meshes, no textures. Each model uses at most 3 material slots, `Primary`, `Secondary` and `Accent`, so you can map them onto your own palette. What each slot stands for differs per model; see `USAGE.md`.
- Grid: 1.5 m cells. Each prop fits inside one cell.
- Static meshes only. Nothing is rigged or animated; the dasher, runner stone, crank and steelyard do not move.
- Formats: FBX and GLB.
- Unity import test passed (the Open Kit team's engine test, 25 Nov 2026, Unity 6000.4.0f1, scale 1 with Convert Units and Bake Axis Conversion on). Other engines, Unity versions or import settings may give different results. See `USAGE.md` for what was run and what was not.

## Contents
- `fbx/`, `glb/`: the models.
- `collision/`: convex collision shells (`fbx/`, `glb/`) and `colliders.json`, which holds the same shells as plain numbers.
- `renders/`, `CONTACT_SHEET.png`: preview images, including a grid layout with a plain 1.8 m reference pole (not part of the pack) and a view of the collision shells.
- `source/build_farmhouse_market.py`: the Blender Python script that builds every model and collision shell in this folder.
- `USAGE.md`: import, colliders and colour slots.
- `MANIFEST.json`: file list with sizes and SHA-256 hashes.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
