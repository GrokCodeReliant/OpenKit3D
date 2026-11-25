# Hauling & Lifting props

Four original low-poly hand-powered lifting and hauling machines for docks, mines, quarries, castle works or a dungeon shaft.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `prop-windlass-wood` | 460 | 1.24 × 1.13 × 0.80 | 1 cell | Two-man windlass. A rope drum on an iron axle between two A-frames, with a ratchet and pawl, a crank at each end and a rope leading off to an iron load ring. |
| `prop-capstan-wood` | 572 | 1.40 × 0.98 × 1.40 | 1 cell | Octagonal capstan: a waisted drum with eight whelps, a drumhead with four push bars, and rope turns with a lead running to the ground. |
| `prop-jib-crane-wood` | 404 | 1.12 × 2.84 × 1.40 | 1 cell | Post crane on cross-foot sills with braces. The arm has a counterweight at the back and a sheave at the front. A rope runs from a small post winch over the sheave down to a hook block. |
| `prop-shaft-hoist-frame-wood` | 276 | 1.38 × 2.56 × 1.38 | 1 cell | Four-leg hoist frame with spreader bars and an iron head, a two-block rope tackle with a hook, and a hauling line tied off on one leg. The centre is open, so it can stand over a hatch or shaft. |

## Conventions
- 1 unit = 1 metre. The pivot is at the bottom centre, with the base resting on the ground.
- Flat-shaded closed meshes, no textures. Each model uses the material slots `Primary` (wood), `Secondary` (iron) and `Accent` (rope), 3 at most, so you can map them onto your own palette.
- Grid: 1.5 m cells. Each prop fits inside one cell.
- Static meshes only. Nothing is rigged or animated, and cranks, drums and hooks do not move.
- Formats: FBX and GLB.
- Unity import test passed (the Open Kit team's engine test, 25 Nov 2026, Unity 6000.4.0f1, scale 1 with Convert Units and Bake Axis Conversion on). Other engines, Unity versions or import settings may give different results. See `USAGE.md` for what was run and what was not.

## Contents
- `fbx/`, `glb/`: the models.
- `collision/`: convex collision shells (`fbx/`, `glb/`) and `colliders.json`, which holds the same shells as plain numbers.
- `renders/`, `CONTACT_SHEET.png`: preview images, including a grid layout with a plain 1.8 m reference pole (not part of the pack) and a view of the collision shells.
- `source/build_hauling_lifting.py`: the Blender Python script that builds every model and collision shell in this folder.
- `USAGE.md`: import, colliders and colour slots.
- `MANIFEST.json`: file list with sizes and SHA-256 hashes.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
