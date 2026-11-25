# Arcane Focus props

Four original low-poly props for a mage's tower, a ritual site or a magic-themed dungeon room.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `prop-rune-obelisk-stone` | 380 | 1.10 × 2.40 × 1.10 | 1 cell | Tapered stone obelisk with a pyramid cap on a two-step base. Each face carries three raised rune inlays. |
| `prop-crystal-focus-pylon` | 388 | 0.95 × 1.62 × 0.96 | 1 cell | Large crystal held upright by three iron claws on an octagonal stone plinth, with smaller crystals growing from the base. |
| `prop-scrying-orb-tripod` | 512 | 0.67 × 1.20 × 0.64 | 1 cell | Glass orb resting in a stone cup on a braced iron tripod. |
| `prop-ritual-dais-stone` | 576 | 2.80 × 0.46 × 2.80 | 2 × 2 cells | Round two-step stone platform with an inlaid rune ring and centre seal, and four marker stones on the lower step. The top is meant to be walked on (a character-controller walk was not run). |

## Conventions
- 1 unit = 1 metre. Pivot at the bottom centre, base resting on the ground.
- Flat shaded, closed meshes, no textures. Each model uses the material slots `Primary`, `Secondary` and `Accent` (3 at most) so you can map them onto your own palette. In the previews, Accent is the blue used for the crystals, orb and runes (a plain colour, not emissive).
- Grid: 1.5 m cells. The dais spans a 2 × 2 block (3.0 m) with its pivot on the shared corner. The others fit inside one cell.
- Formats: FBX and GLB.
- Unity import test passed with one note on the dais (the Open Kit team's engine test, 25 Nov 2026, Unity 6000.4.0f1, scale 1 with Convert Units and Bake Axis Conversion on). Other engines, Unity versions or import settings may give different results. See `USAGE.md` for what was run and what was not.

## Contents
- `fbx/`, `glb/`: the models.
- `collision/`: convex collision shells (`fbx/`, `glb/`) and `colliders.json`, the same shells as plain numbers.
- `renders/`, `CONTACT_SHEET.png`: preview images, including a grid layout and a view of the collision shells.
- `source/build_arcane_focus.py`: the Blender Python script that builds every model and collision shell in this folder.
- `USAGE.md`: import, colliders, walkable surfaces and colour slots.
- `MANIFEST.json`: file list with sizes and SHA-256 hashes.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
