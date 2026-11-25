# Siege Yard pieces
Six original low-poly environment props for a siege yard: a battering ram, a compact ballista, a standing pavise, a wheeled mantlet, a group of stone shot, and a bolt rack.

| Asset | Tris | Size m (width × height × depth) | Footprint | What it is |
|---|---:|---|---|---|
| `prop-battering-ram` | 652 | 2.48 × 0.78 × 0.51 | 2 cells | Log on two trestles, with iron hoops and a capped striking head. Real gaps under the log and between the trestle legs. |
| `prop-ballista` | 868 | 1.37 × 0.86 × 1.43 | 1 cell | Compact scorpion-scale engine with side frames, a front prod, a bowstring across the tips, a rear winch and one bolt. The space between the frames is a real gap. |
| `prop-pavise` | 152 | 0.64 × 1.28 × 0.58 | 1 cell | Tall pointed standing shield with a plain boss, a shoe, battens and a rear leaning prop. This is deliberate: the face is a solid panel. The space under the prop is a real gap. |
| `prop-mantlet` | 612 | 1.40 × 1.01 × 0.25 | 1 cell | Wider, shorter wheeled screen with a 6 cm viewing slit (a real gap), an axle and two wheels. The space under the screen is a real gap. |
| `prop-stone-shot` | 300 | 0.66 × 0.36 × 0.55 | 1 cell | Three stone balls of different sizes sitting on the ground, with small gaps between them. One collider per stone. |
| `prop-ballista-bolt-rack` | 464 | 0.76 × 0.29 × 0.42 | 1 cell | Low timber rack holding four horizontal bolts with iron heads. This is deliberate: one envelope collider covers the set; the openings between the bolts are visual only. |

## Conventions
- 1 unit = 1 metre. Grid: 1.5 m cells.
- Pivots: bottom centre on every piece. The ram occupies two cells along X and stays under the Medium size-class cap of 2.5 m.
- Flat-shaded closed meshes. Each model uses at most 3 material slots, `Primary`, `Secondary` and `Accent`. FBX files are slots-only (no embedded textures, path_mode STRIP). Optional flat BaseColor PNGs live in `tex/`.
- Static meshes only. Nothing is rigged or animated.
- Pivots: bottom centre. In the raw FBX file frame, the front of each piece faces +Z.

## Colour slots
| Asset | `Primary` | `Secondary` | `Accent` | Suggested `tex/` |
|---|---|---|---|---|
| `prop-battering-ram` | log | trestles and hoops (dark timber) | iron cap | wood, dark wood, iron |
| `prop-ballista` | side frames and prod limbs | rails, tiller and bolt shaft (dark timber) | winch, nocks, bowstring and bolt head | wood, dark wood, iron |
| `prop-pavise` | shield board | battens and rear prop (dark timber) | boss and shoe | wood, dark wood, iron |
| `prop-mantlet` | leaves and posts | head, sill and wheel bodies (dark timber) | axle and iron tires | wood, dark wood, iron |
| `prop-stone-shot` | mid stone | large stone | small stone (same stone colour) | mortar, stone, stone |
| `prop-ballista-bolt-rack` | timber rack and legs | bolt shafts (dark timber) | iron heads | wood, dark wood, iron |

Texture files: `tex/mat_wood_BaseColor.png`, `tex/mat_dark_wood_BaseColor.png`, `tex/mat_iron_BaseColor.png`, `tex/mat_stone_BaseColor.png`, `tex/mat_mortar_BaseColor.png`.

## Import
Import `fbx/<asset>.fbx` with scale factor 1. Unity settings used in the engine test of 25 Nov 2026 (Unity 6000.4.0f1): leave "Convert Units" on, and turn on "Bake Axis Conversion" if your version offers it. Results apply to that version and those settings; other engines, Unity versions or import settings may differ. In the raw FBX file frame, the front of each piece faces +Z.

## Known limits
See `HONEST_LOOK.md`. This is deliberate: the pavise face is a solid panel, and the bolt-rack collider uses one envelope around the four bolts. Real collider gaps: under the ram, between trestle legs, between the ballista frames, under the pavise prop, the mantlet slit, under the mantlet, and between the three stones. Collision notes describe the reference shells, which are not included.

## Engine test
These files passed the Open Kit team's Unity engine test on 25 Nov 2026 (Unity 6000.4.0f1). Results apply to that version and those settings; other engines, Unity versions or import settings may differ. Recorded in REPORT.md and SIEGE.md. The test imported each FBX at scale 1 with Convert Units and Bake Axis Conversion on, built a prefab with renderers, the shipped colliders, and colour-slot theme binding, and checked room scale against the kit's 1.5 m grid. Those standard checks passed on all six props. Grid-snap and occlusion-fade checks were skipped: these are props, not wall or floor modules. Extra checks of the gaps under the ram and between its trestles, between the ballista frames, under the pavise prop, through the mantlet slit and under the mantlet, and between the stones, plus the solid pavise face and bolt-rack envelope, all passed as recorded in SIEGE.md. Character-controller probes in edit mode were run on several of those openings.

Play mode, physics, room-adapt scaling, and an on-screen fade were not run. Theme binding used runtime colour-slot blocks, not baked theme assets from a game project. Ray checks used ray and sphere casts against the shipped collision shells, not a gameplay projectile.

## Contents
- `fbx/`: the six models.
- `tex/`: five optional slot albedos.
- `CONTACT_SHEET.png`: preview of the six assets plus a grid layout (with a 1.8 m reference pole that is not part of the pack) and a 50 mm perspective view from 13 m.
- `HONEST_LOOK.md`: known visual limits. `MANIFEST.json`: file list and per-asset measures. `SHA256SUMS`: hashes for `sha256sum -c`.

## License
CC0 1.0 Universal (public domain dedication). See `LICENSE`. Credit is welcome but not required.
