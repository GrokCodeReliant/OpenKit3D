# openkit-doors-windows-b1 (CC0 1.0)
Modular doors & windows for Open Kit. 1 unit = 1 m, Unity axes (Y up). FBX are slot-only (no embedded image paths); assign `tex/` maps per MANIFEST `slot_textures`.

| Asset | Tris | Size x,y,z (m) | Pivot |
|---|---|---|---|
| prop-door-wood | 344 | 0.96 x 2.05 x 0.19 (slab 0.05; knobs both faces) | hinge_bottom |
| prop-door-plank | 428 | 1.015 x 2.05 x 0.15 (slab 0.04 + Z-brace) | hinge_bottom |
| prop-window-shutter | 548 | 1.04 x 1.20 x 0.08 | wall_back, bottom-centre |
| prop-window-leaded | 1040 | 1.00 x 1.24 x 0.17 | wall_back, bottom-centre |
| prop-doorframe-trim (optional) | 84 | 1.42 x 2.33 x 0.14 | wall_back, bottom-centre |
| prop-window-sill (optional) | 48 | 1.20 x 0.20 x 0.18 | wall_back, top of sill y=0 |

## Wall openings (cut holes to these)
- **Door hole: 1.0 m wide x 2.1 m tall**, floor at y=0. Doors are 0.95/1.0 x 2.05 → ~2-5 cm clearance; `prop-doorframe-trim` casing wraps exactly this hole.
- **Window hole: 1.0 m wide x 1.2 m tall**, sill at the hole bottom. `prop-window-leaded` fills it exactly; `prop-window-shutter` covers it from outside; `prop-window-sill` sits at its bottom edge.

## Pivots
- **Doors (hinge_bottom):** origin on the hinge edge at the floor. Hinge is the **-X side** of the slab; slab extends along +X. Thickness centred on z=0. Rotate about +Y to open; positive yaw swings the free edge toward **+Z**. Place origin at the left jamb of the hole (x = hole_left), mirror X scale (-1) for a right-hand hinge.
- **Windows/shutters/trim/sill (wall_back):** origin at bottom-centre of the opening, **back face at z=0 flush to the wall's exterior face**, geometry projects toward **-Z** (outside). Put the origin on the wall face at the hole's bottom-centre.
- **Shutter** is a **closed pair** (two 0.5 m louvred leaves, hinge pins at x=±0.51, centre latch). Single mesh — not separately animatable; for opening shutters, use a second instance scaled or split in DCC.
- **Leaded window**: two casement panes with diamond lead cames (both faces) over a double-sided glass plane (`Glass` slot → mat_glass; set transparent/alpha in engine as wanted). Not openable.

Rebuild: `blender -b -P src/build_doors_windows_b1.py -- <packroot>` (+ `python3 src/make_glass.py tex`).
