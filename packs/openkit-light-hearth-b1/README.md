# openkit-light-hearth-b1 (Open Kit, CC0 1.0)
Light/hearth set, 1 unit = 1 m, slots-only FBX (no embedded textures/paths). Export: Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL (same as outdoor-props-b1). Unity Scale Factor 1.

| Asset | Tris | Size m (x,y-up,z) | Slots -> tex | Pivot |
|---|---|---|---|---|
| prop-torch-wall-iron | 226 | 0.10 x 0.50 x 0.24 | Metal mat_iron, Secondary mat_wood_dark, Emissive mat_ember | wall_back (mount-plate centre on wall plane) |
| prop-brazier-floor | 520 | 0.71 x 0.94 x 0.66 | Metal mat_iron, Emissive mat_ember | bottom_centre |
| prop-campfire-ring-iron | 600 | 1.21 x 0.55 x 1.13 | Primary mat_stone, Metal mat_iron, Secondary mat_wood_dark, Emissive mat_ember | bottom_centre |
| prop-lantern-hang | 262 | 0.17 x 0.45 x 0.43 | Metal mat_iron, Emissive mat_ember | wall_back (hang point = plate centre) |

## Suggested VFX sockets (create an empty/child at these local offsets; up = Unity Y, "out" = distance from wall along the prop's forward)
- prop-torch-wall-iron: `fx_flame` up 0.36, out 0.205 (top of ember tip)
- prop-brazier-floor: `fx_flame` up 0.88, centred (coal bed top)
- prop-campfire-ring-iron: `fx_flame` up 0.22 centred; `fx_smoke` up 0.60 (above grate bar at 0.55)
- prop-lantern-hang: `fx_light` (point light) down 0.26, out 0.34 (glass core centre)
Exact Blender-space values in MANIFEST.json `vfx_sockets_blender_xyz_m`.

## Naming / dedupe
- `prop-torch-wall` exists in okm4 (base/new/beforebl scripts) -> renamed **prop-torch-wall-iron**.
- `prop-campfire-ring` exists in openkit-outdoor-props-b1 -> renamed **prop-campfire-ring-iron** (iron hoop + grate bar + teepee logs; different silhouette from the outdoor stone-only ring).
- `prop-lantern-hang`: free (okm4 has `prop-lantern` only) -> kept that name. `prop-brazier-floor`: free (okm4 has `prop-brazier`) -> kept.
- Not reauthored: prop-candle-niche, prop-candle-sconce, prop-weapon-plaque, prop-torch-sconce/standing/held, WPN_*, tile-dojo-*. Torch/lantern use iron bracket arms, no candle or niche shapes.
- Emissive slot is mat_ember (albedo doubles as emission map). Textures shared byte-identical with outdoor-props-b1.
Rebuild: `blender -b -P src/build_light_hearth_b1.py -- <packroot>`
