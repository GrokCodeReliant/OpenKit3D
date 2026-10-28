# openkit-dyer-props-b1

4 medieval cloth-dyer workshop props. 1 m units, Z-up in Blender / Y-up FBX, slots-only materials.

| asset | tris | dims m | mats | pivot |
|---|---|---|---|---|
| prop-dye-vat-small | 172 | [0.54, 0.55, 0.26] | M_Wood_Dark, M_Indigo, M_Iron | bottom_centre (0,0,0) on floor; 0.55 m dia low open staved tub, no handles, 2 iron hoops, deep-indigo dye surface at 0.21 m |
| prop-yarn-skein-rack | 108 | [1.02, 0.4, 1.295] | M_Wood_Oak, M_Indigo, M_Madder, M_Weld | bottom_centre (0,0,0) on floor; 1.0 m freestanding drying frame on 2 foot skids, pole along X at 1.27 m, 4 dyed skeins (indigo/madder/weld) hanging; flat in Y so can sit against a wall |
| prop-madder-root-bundle | 120 | [0.551, 0.148, 0.113] | M_Madder_Root, M_Twine | bottom_centre (0,0,0) on floor/bench; 0.55 m bundle of 5 tapering madder roots lying along X, 2 twine ties |
| prop-stirring-paddle-dy1 | 56 | [0.12, 0.036, 1.405] | M_Wood_Oak, M_Indigo | bottom_centre (0,0,0) at blade tip; 1.4 m upright dyer's paddle, flat solid 0.11 m blade in XZ, indigo stain band, T-grip at top; rotate ~15 deg about X to lean |

Rebuild: `blender -b --factory-startup -P src/build.py`
