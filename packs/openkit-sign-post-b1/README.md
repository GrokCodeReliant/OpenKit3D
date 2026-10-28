# openkit-sign-post-b1

Open Kit sign/post set. 4 props, slots-only FBX (material slots, no textures), 1 unit = 1 m, Y-up, bottom_centre pivot (bbox centre in X/Z, base at y=0).

| asset | tris | size m (x,y,z) | slots | notes |
|---|---|---|---|---|
| prop-signpost-wood | 48 | [0.708, 1.86, 0.168] | Wood, WoodDark | post 1.86 m tall (0.10 m sq); blank board 0.70 x 0.30 x 0.04 m, top at ~1.60 m, offset one side |
| prop-waymarker-stone | 112 | [0.74, 1.322, 0.613] | Stone | 5 stacked stones + upright capstone, ~0.76 m wide, ~1.2 m tall |
| prop-banner-hang-pole | 76 | [0.94, 2.55, 0.5] | Wood, Cloth, Iron | free-standing pole 2.55 m, 0.5 m sq foot; L-arm 0.7 m; cloth 0.60 x 1.12 m (swallowtail), single-sheet double-faced. Distinct from wall-mounted prop-banner-hanging (env-b1). |
| prop-notice-board | 144 | [2.3, 1.908, 0.402] | Wood, WoodDark, Paper | 3 posts 1.8 m, board 2.0 x 0.9 m (centre 1.15 m), roof cap 2.3 m wide, 5 blank notices |

Note: prop-signpost-wood pivot is at the post foot (post axis at x=0,z=0, base y=0), not bbox centre; the board extends to +X (~0.62 m). Other props use bbox-centre XZ.
prop-banner-hang-pole is free-standing (foot block + pole + L-arm + cloth) and is not the wall-mounted `prop-banner-hanging` from env-b1.

Rebuild: `blender -b -P src/build_sign_post_b1.py -- <packroot>`; renders: `src/render.py`.
