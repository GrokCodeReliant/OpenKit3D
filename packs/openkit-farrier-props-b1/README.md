# openkit-farrier-props-b1
Original procedural farrier / horseshoeing props, CC0 1.0. All ≤210 tris (all ≤140).

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot |
|---|---|---|---|---|
| prop-hoof-stand | 136 | 0.332 x 0.582 x 0.37 | Primary, Secondary, Post, Metal | bottom_centre |
| prop-shoeing-hammer-fr1 | 84 | 0.301 x 0.034 x 0.125 | Primary, Metal, Wedge | bottom_centre |
| prop-hoof-knife | 116 | 0.228 x 0.026 x 0.05 | Primary, Metal, Ferrule | bottom_centre |
| prop-blank-horseshoe | 92 | 0.135 x 0.012 x 0.101 | Metal | bottom_centre |

- Pivots: all bottom_centre (floor y=0, bbox-centred XZ). Hammer, knife and blank lie flat on the floor.
- Rename: `prop-shoeing-hammer` → `prop-shoeing-hammer-fr1` (keeps clear of smithy `prop-hammer-st1`). Others: no clashes across studio/art/openkit-*/fbx.
- FBX: Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL, path_mode STRIP, no images. Assign by slot from `tex/` (albedo sRGB, normal OpenGL, ao linear).
- Textures: byte copies of mat_iron / mat_wood_oak / mat_wood_dark from openkit-stable-props-b1 (CC0).
