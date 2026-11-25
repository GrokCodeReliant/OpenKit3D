# Wayside Shrine props

Four original low-poly props for roadsides, village squares and small chapels.

| Asset | Tris | Size m (width × height × depth) | What it is |
|---|---:|---|---|
| `prop-wayside-shrine-stone` | 280 | 1.28 × 2.08 × 0.88 | Stone niche shrine with a pitched gable roof, sill, stele and two votive cups. Wall and roof are separate nodes so they can fade when they block the camera. |
| `prop-offering-bowl-stone` | 724 | 0.66 × 0.77 × 0.66 | Wide, shallow open offering dish (7 cm deep) on a turned stand, with a few offerings and coins. |
| `prop-holy-water-font` | 352 | 0.74 × 1.05 × 0.74 | Octagonal font with a deep open basin (28 cm), banded rim and stepped base. |
| `prop-votive-candle-rack` | 640 | 0.94 × 1.14 × 0.50 | Three stepped candle shelves with trays and 15 unlit wax candles of different heights, on a braced stand with feet. |

## Conventions
- 1 unit = 1 metre. Pivot at the bottom centre, base resting on the ground.
- Flat shaded, closed meshes, no textures. Material slots are named `Primary`, `Secondary` and `Accent` (3 at most per asset) so you can map them onto your own palette.
- Each prop fits inside one 1.5 m grid cell. These are free-standing props, not modular wall pieces.
- Formats: FBX and GLB.

## Contents
- `fbx/`, `glb/`: the models.
- `collision/`: box collision hulls (`fbx/`, `glb/`) and `colliders.json`, the same boxes as plain numbers.
- `renders/`, `CONTACT_SHEET.png`: preview images.
- `source/build_wayside_shrine.py`: the Blender Python script that builds every model and collider in this folder.
- `USAGE.md`: import, colliders, camera fade setup and colour slots.
- `MANIFEST.json`: file list with sizes and SHA-256 hashes.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
