# openkit-charcoal-burner-props-b1 (CC0)
Charcoal-burner / collier workshop props for Open Kit: prop-charcoal-rake, prop-kiln-vent-cover, prop-charcoal-sack-open, prop-measuring-scoop-cb1. All <=210 tris, 1 m units, slots-only FBX; optional BaseColor PNGs in tex/.

## Pivots
- prop-charcoal-rake: bottom_centre-ish (0,0,0) lying flat at handle midpoint; 1.6 m ash handle along X, 0.36 m iron 5-tine head at +X tines down; rotate about Y to lean against a kiln
- prop-kiln-vent-cover: bottom_centre (0,0,0) on kiln/ground; 0.44 m square plank damper with battens, centre lift handle and two turf clods weighing it down
- prop-charcoal-sack-open: bottom_centre (0,0,0) on ground; 0.42 m dia soot-stained hessian sack, mouth rolled open, black charcoal heap and lumps inside, two spilled lumps at +X
- prop-measuring-scoop-cb1: bottom_centre (0,0,0) on ground/sack; 0.2x0.16 m open-front box scoop (quarter-peck measure) with iron lip and bands, handle +X from back wall

Rebuild: blender -b -P src/build.py
