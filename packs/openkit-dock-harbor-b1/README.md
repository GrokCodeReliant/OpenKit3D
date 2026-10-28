# openkit-dock-harbor-b1
Dock and harbor props for Open Kit. License: CC0 1.0. Units: 1 m. Y-up in FBX. The FBX files have material slots only (no embedded or linked textures). Every asset is 210 triangles or fewer.

| Asset | Tris | Dims XYZ (m) | Materials | Pivot |
|---|---|---|---|---|
| prop-mooring-bollard | 108 | 0.42 x 0.44 x 0.54 | M_Iron, M_Wood_Dark | bottom_centre, under the base plate |
| prop-rope-coil-dock | 206 | 0.55 x 0.52 x 0.07 | M_Rope | bottom_centre, at the coil centre on the deck |
| prop-gangplank | 132 | 0.60 x 2.40 x 0.08 | M_Wood_Plank, M_Wood_Dark | bottom_centre. Length runs along Y. Tilt about X. |
| prop-lobster-pot | 168 | 0.60 x 0.45 x 0.26 | M_Wood_Plank, M_Wood_Dark | bottom_centre, under the base boards |

The optional textures in tex/ are T_Wood_Plank, T_Wood_Dark, T_Rope and T_Iron (BaseColor, 512 px). Assign them in the engine.
Renames: rope coil uses -dock to avoid bs1/wall/dnd; the plank stack (already in bridge-scaffold) was replaced by prop-gangplank.
