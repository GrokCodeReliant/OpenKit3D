# openkit-butcher-props-b1 (CC0)
Medieval-fantasy butcher shop props for Open Kit: prop-cleaver-bt1, prop-butcher-block, prop-meat-hook-rail, prop-hanging-ham. All <=210 tris (max 132), 1 m units, slots-only FBX; optional BaseColor PNGs in tex/. PG, no gore.

## Pivots
- prop-cleaver-bt1: bottom_centre (0,0,0) on floor; heavy 0.20x0.11x0.01 m rectangular cleaver blade laid flat, blade toward +X, wood handle toward -X
- prop-butcher-block: bottom_centre (0,0,0) on floor; 0.64 m dia x 0.70 m tall end-grain stump block with slightly dished worn top
- prop-meat-hook-rail: wall_back (0,0,0) = centre of back face against wall (XZ plane), protrudes toward -Y; 0.62 m oak board, iron rail with 3 empty S-hooks
- prop-hanging-ham: top_centre (0,0,0) at top of hook eye; hangs down -Z; stylized cured ham (teardrop, shank up) 0.26 m wide, bound with twine on an iron hook

Renames: prop-cleaver -> prop-cleaver-bt1 (collision with openkit-dnd / CATALOG 2D prop-cleaver).
Rebuild: blender -b -P src/build.py
