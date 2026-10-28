# openkit-fence-gate-b1
Original procedural fence/gate set, CC0 1.0. 1 unit = 1 m. Blender Z-up authoring; FBX exported Y-up (-Z forward). Slots: Primary / Secondary / Metal (slots-only FBX, no embedded textures; PBR maps in tex/).

## Modular span (snap runs)
- **Span = 1.80 m post centre-to-centre** along X.
- `prop-fence-post`: 0.12 m square, 1.25 m tall. Pivot bottom_centre. Place at x = 0, 1.8, 3.6 …
- `prop-fence-rail`: 3-board panel + back diagonal brace, 1.68 m long (fits between post faces). Pivot bottom_centre (ground level); place at the midpoint between two posts (x = 0.9, 2.7 …). Boards sit at 0.32 / 0.68 / 1.04 m.
- `prop-gate-post`: 0.18 m square, 1.52 m tall, iron pintles on its +X face. Pivot bottom_centre.
- `prop-gate-wood`: 1.00 m wide x 1.225 m tall ledged/Z-braced board leaf. **Pivot = hinge, bottom of the -X edge**; leaf extends +X; rotate about vertical axis to swing. Strap side faces -Y.
- Gate opening: place hinge gate post at x=0, gate leaf pivot at x=+0.10 (post half 0.09 + 0.01 gap), latch-side gate post (rotate 180°) at x=+1.21 centre. Join to a fence run with a fence post 1.8 m beyond either gate post, or butt the panel directly (panel midpoint 0.99 m from gate-post centre).

## Not duplicated
New silhouette vs OpenKit3D picket fence (okm prop-fence-wood: pointed pickets w/ integrated posts). No outdoor-props, market, barrel-chest, doors-windows, WPN_*, wall-dress, tile-dojo-* remakes.
Rebuild: `blender -b -P src/build_fence_gate_b1.py -- <packroot>`
