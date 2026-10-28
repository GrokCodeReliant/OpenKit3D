# openkit-stairs-ladder-b1
Wooden stairs / ladder / ramp set. 1 m units, Blender Z-up (FBX exported -Z fwd, Y up). Slots-only materials: M_Wood_Plank, M_Wood_Dark; textures in tex/ (512 px BaseColor) to assign in engine.

| Asset | Tris | Dims X×Y×Z m | Key measures | Pivot |
|---|---|---|---|---|
| prop-stairs-wood | 168 | 1.0 × 1.478 × 1.25 | rise_m=0.2, run_m=0.25, steps=5, width_m=1.0, total_rise_m=1.0, total_run_m=1.25 | floor level, front edge of first tread, centred on width (0,0,0); stairs climb +Y, up +Z |
| prop-ladder-wood-lean | 108 | 0.51 × 0.04 × 2.4 | height_m=2.4, width_m=0.45, rung_spacing_m=0.3, rungs=7, lean_suggested_deg=15 | bottom_centre between rail feet (0,0,0); rails along +Z, modelled upright; rotate about X ~15deg to lean |
| prop-ramp-plank | 132 | 0.6 × 1.97 × 0.474 | length_m=2.0, width_m=0.6, rise_m=0.4, run_m=1.96, slope_deg=11.5, cleats=6 | floor at low end, centred on width (0,0,0); rises toward +Y |

Modular stair: rise 0.20 / run 0.25 (5 steps = 1.0 m rise, 1.25 m run); width 1.0 m — tiles on a 1 m grid; suggested modular widths 1.0–1.2 m (scale X only). Stack two modules end-to-end with +1.25 Y, +1.0 Z offset for a 2 m storey.
Name note: `prop-ladder-wood` already exists in okm4 base kit → this pack uses `prop-ladder-wood-lean`.
Rebuild: blender -b --factory-startup -P src/build.py
