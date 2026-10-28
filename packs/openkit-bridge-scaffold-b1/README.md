# openkit-bridge-scaffold-b1
Bridge / scaffold set. 1 m units, Blender Z-up (FBX -Z fwd, Y up). Slots-only materials: M_Wood_Plank, M_Wood_Dark, M_Rope; 512 px BaseColor in tex/ to assign in engine.

| Asset | Tris | Dims X×Y×Z m | Pivot |
|---|---|---|---|
| prop-bridge-wood-plank | 192 | 1.0 × 2.0 × 0.905 | bottom_centre (0,0,0) at centre of span on stringer underside; span runs along Y from -1.0 to +1.0; snap modules at +2.0 m Y |
| prop-scaffold-frame | 252 | 1.6 × 1.08 × 2.04 | bottom_centre (0,0,0) between the four post feet; stack vertically at +2.04 m Z, tile at 1.5 m X / 1.0 m Y |
| prop-plank-stack | 168 | 1.02 × 2.095 × 0.278 | bottom_centre (0,0,0) under bearer blocks |
| prop-rope-coil-bs1 | 584 | 0.51 × 0.51 × 0.229 | bottom_centre (0,0,0) on floor at coil axis |

**Modular snap:** bridge span = 2.0 m along Y (pivot at span centre, ends at ±1.0 m); chain segments at +2.0 m Y. Deck width 1.0 m, deck top z=0.19 m. Scaffold 1.5×1.0 m footprint, stacks at +2.04 m Z.
Name note: `prop-rope-coil` already exists in openkit-dnd/passed → this pack uses `prop-rope-coil-bs1` (a mesh prop, separate from mat_rope textures).
