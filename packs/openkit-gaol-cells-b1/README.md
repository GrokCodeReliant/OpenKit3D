# Gaol Cell pieces

Four original low-poly pieces for dungeon cells, guard rooms and lock-ups: two walkable floor tiles, one wall module and one prop.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `tile-dungeon-floor-grate` | 552 | 1.50 × 0.12 × 1.50 | 1 cell | Stone floor tile with an iron drain grate over a shallow sump in the middle. Six flat bars and two cross bars sit in an iron frame, a few millimetres below the slabs. |
| `tile-dungeon-floor-trapdoor` | 656 | 1.50 × 0.12 × 1.50 | 1 cell | Stone floor tile with a closed plank hatch in an iron curb: five planks, two iron straps, two hinge knuckles at the back and a flat pull ring at the front. The hatch does not open. |
| `wall-dungeon-cell-bars` | 1100 | 1.50 × 3.00 × 0.34 | 1 cell edge | Wall module for a cell front: coursed stone jambs, a stone sill and lintel under a full-width cap course, nine round iron bars and two flat cross straps. There is no door in it. |
| `prop-stocks-wood` | 380 | 1.40 × 1.06 × 0.60 | 1 cell | Foot stocks: a sill on two feet, two braced uprights with iron cap bands, a two-board yoke with two leg holes, a cap rail, an iron hasp with a padlock and a strap hinge. |

## Conventions
- 1 unit = 1 metre. Grid: 1.5 m cells.
- Pivots: the wall and the stocks use bottom centre. The two floor tiles use the kit's floor-top pivot: the walking surface is at height 0 and the tile extends 0.12 m below it, the same as the kit's stone floor tile.
- The wall module has the same size as the kit's stone wall module (1.5 × 3.0 × 0.34 m), so it can sit in a run of those walls. Its front faces +Z.
- Flat-shaded closed meshes, no textures. Stone blocks, slabs and the big timbers have chamfered edges like the kit's own stone modules. Each model uses at most 3 material slots, `Primary`, `Secondary` and `Accent`; see `USAGE.md` for what each stands for.
- Static meshes only. Nothing is rigged or animated.
- Formats: FBX and GLB.
- Unity import test passed with one note on the floor tiles (the Open Kit team's engine test, 25 Nov 2026, Unity 6000.4.0f1, scale 1 with Convert Units and Bake Axis Conversion on). Other engines, Unity versions or import settings may give different results. See `USAGE.md` for what was run and what was not.

## Contents
- `fbx/`, `glb/`: the models.
- `collision/`: convex collision shells (`fbx/`, `glb/`) and `colliders.json`, which holds the same shells as plain numbers.
- `renders/`, `CONTACT_SHEET.png`: preview images, including a grid layout with a plain 1.8 m reference pole (not part of the pack) and a view of the collision shells.
- `source/build_gaol_cells.py`: the Blender Python script that builds every model and collision shell in this folder.
- `USAGE.md`: import, colliders, camera fade and colour slots.
- `SOURCE_LOG.md`: where each model comes from. `HONEST_LOOK.md`: known visual limits. `VALIDATION.json`: the file-level check results, including the Unity test of 2026-11-25.
- `MANIFEST.json`: file list with sizes and SHA-256 hashes. `SHA256SUMS.txt`: the same hashes for `sha256sum -c`.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
