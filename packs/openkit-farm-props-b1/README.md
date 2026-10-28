# openkit-farm-props-b1
Original procedural farm props, CC0 1.0. All ≤600 tris.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot |
|---|---|---|---|---|
| prop-hay-bale-fp1 | 36 | 0.9 x 0.37 x 0.47 | Primary, Twine | bottom_centre |
| prop-pitchfork-fp1 | 92 | 1.47 x 0.036 x 0.22 | Primary, Metal | bottom_centre |
| prop-wheelbarrow-wood | 220 | 1.455 x 0.565 x 0.575 | Primary, Secondary, Wheel, Metal | bottom_centre |
| prop-feed-trough | 252 | 1.42 x 0.874 x 0.5 | Primary, Secondary, Rack, Feed | bottom_centre |

- prop-feed-trough is a livestock feeder (V-hopper on A-frame legs, hay rack slats, Feed slot). It is NOT the well-water water trough `prop-trough-wood` (flat plank box on skids, Water slot).
- Renames: `prop-hay-bale` → `prop-hay-bale-fp1` (outdoor-props-b1 clash), `prop-pitchfork` → `prop-pitchfork-fp1` (openkit-dnd tipped clash). okm4: no clashes.
- FBX: Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL, path_mode STRIP. Assign by slot from `tex/` (albedo sRGB, normal OpenGL, ao linear).
- Textures: wood_oak/wood_dark/iron byte copies from well-water-b1; mat_straw = byte copy of well-water mat_rope.
- Rebuild: `blender -b -P src/build_farm_props_b1.py -- <packroot>`.
