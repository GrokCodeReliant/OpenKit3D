# openkit-cart-crate-b1
Original procedural cart/crate/sack set, CC0 1.0.

| Asset | Tris | Size m (x, y-up, z) | Slots | Pivot | Notes |
|---|---|---|---|---|---|
| prop-cart-wood | 372 | 1.02 x 0.608 x 1.658 | Primary, Secondary, Metal | bottom_centre (axle): y=0 at wheel ground contact, origin directly under axle centre; rest-leg also touches y=0 at z=-0.6 (handle side) | 2-wheel hand cart, empty bed, iron tyres, rest leg; distinct from okm4 prop-cart-hand |
| prop-crate-wood-open | 276 | 0.769 x 0.605 x 0.62 | Primary, Secondary, Metal | bottom_centre: floor y=0, centred on crate body (loose lid leans on +X side) | open framed crate + loose lid leaning on +X; distinct from market prop-crate-open (low slatted 0.64x0.36x0.45) |
| prop-crate-wood-closed | 228 | 0.625 x 0.605 x 0.625 | Primary, Secondary, Metal | bottom_centre: floor y=0, centred | closed framed crate with diagonal braces + iron corner caps; distinct name from v03b prop-crate-wood |
| prop-sack-tied-cc1 | 224 | 0.472 x 0.78 x 0.506 | Primary, Secondary | bottom_centre: floor y=0, centred on base (top leans +X) | tall leaning sack (0.78 m, top leans +X), rope-tied neck; different silhouette from barrel-chest prop-sack-tied (squat 0.65 m pile) |

- Cart pivot: origin on the ground (y=0) directly under the axle centre, at the wheel contact line. The wheel radius is 0.30 m and the axle height is y=0.30. The rest leg touches the ground about 0.6 m toward the handles.
- FBX: Y mirror, axis_forward -Z, axis_up Y, bake_space_transform, FBX_SCALE_ALL. Unity Scale Factor 1.
- The FBX files hold material slots only. Assign the materials by slot using `tex/` (albedo sRGB, normal OpenGL, ao linear).
- Rebuild: `blender -b -P src/build_cart_crate_b1.py -- <packroot>`.
