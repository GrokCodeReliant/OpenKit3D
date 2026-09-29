# M1 time log (2026-09-26, MDT)

Wall clock for the whole session, including setup, all five props, the Unity system, and iterations: **18:05 to 18:22, about 17 min** (agent-driven; no human modelling time).

| Item | Authoring (approx.) | Machine time per build | Tris / budget | Notes |
|---|---|---|---|---|
| Setup (survey PC, create URP project from template) | ~3 min | Unity project create ~1 min | – | Unity 6000.4.0f1 was already installed with a Personal license |
| okit helper lib + build CLI + preview renderer | ~4 min | – | – | 2 fixes: label shadow and framing |
| prop-chair-simple | ~1 min | build 0.1 s, preview 0.2 s | 616 / 800 | |
| prop-table-wood | ~1 min | 0.1 s / 0.2 s | 792 / 800 | near budget; bevels on ~20 boxes |
| prop-barrel | ~1 min | 0.3 s / 0.9 s | 630 / 800 | 12-sided lathe, 4 hoops |
| prop-brazier | ~1.5 min | 0.1 s / 0.2 s | 610 / 800 | 1 fix: legs dipped below the pivot |
| prop-pillar-stone | ~1 min | 0.1 s / 0.2 s | 604 / 2,500 | structural, 3 m |
| Unity scripts (runtime, postprocessor, build, demo, screenshots) | ~5 min | ImportAll ~15 s; All (with 5 renders) ~40 s | – | 2 iterations on FBX axis (see README) |

Per-prop authoring time is approximate: the five prop scripts were written in one pass on top of the shared lib.
**Estimate for M2+:** about 1 to 2 min per simple prop script once the lib is in place, plus review. The real costs will be art-direction passes and organic shapes.

# M2 time log (2026-09-26, MDT)

Wall clock: **18:20 to about 18:40, about 20 min**, covering 12 props, 3 modular pieces, the brazier rework, 3 themes, 2 new scenes, and 3 build/review iterations.
Machine time: the Blender build of all 20 assets with previews takes about 10 s; Unity `All` (import, prefabs, 4 scenes, package, 21 renders) takes about 50 s.

| Asset | Tris / budget | Authoring (approx.) | Fix iterations |
|---|---|---|---|
| prop-brazier (flame rework) | 740 / 800 | ~3 min | 2 (crystal look, then rounded, twisted tongues) |
| prop-crate | 660 / 800 | ~0.5 min | 0 |
| prop-chest | 580 / 800 | ~1 min | 0 |
| prop-torch-wall | 266 / 800 | ~1 min | 0 |
| prop-altar-stone | 572 / 2500 | ~0.5 min | 0 |
| prop-fallen-pillar | 844 / 2500 | ~1 min | 0 |
| prop-throne-simple | 524 / 800 | ~0.5 min | 0 |
| prop-pew-bench | 224 / 800 | ~0.5 min | 0 |
| prop-coffin | 392 / 800 | ~0.5 min | 0 |
| prop-sarcophagus | 672 / 2500 | ~0.5 min | 0 |
| prop-door-stone | 520 / 2500 | ~0.5 min | 1 (hinge pivot check) |
| prop-mushroom | 438 / 800 | ~0.5 min | 1 (822 tris over budget, fixed with unbevelled spots) |
| prop-treasure-pile | 578 / 800 | ~0.5 min | 0 |
| tile-dungeon-stone-floor | 320 / 2500 | ~0.5 min | 1 (top at z=0) |
| wall-dungeon-stone | 1288 / 2500 | ~1 min | 0 |
| wall-dungeon-stone-doorway | 1004 / 2500 | ~0.5 min | 0 |
| Unity: categories, themes, modular + catalog scenes, close-ups | – | ~6 min | 2 (framing) |

# M3 time log (2026-09-28, MDT)

Wall clock: **19:26 to about 19:45, about 20 min** for survey, 22 prop scripts, the validation extension, the Unity validator, the hero scene, the contact-sheet renderer, a from-scratch build, and docs.
Machine time: the Blender build of all 42 assets with previews takes about 15 s. A from-scratch `build.ps1 -Clean` (Blender, then Unity import, prefabs, validation, 5 scenes, package, 21 + 10 renders) takes about 70 s.

| Asset | Tris / budget | Fix iterations |
|---|---|---|
| prop-anvil | 288 / 800 | 0 |
| prop-banner-standing | 264 / 800 | 1 (emblem depth) |
| prop-bed-simple | 528 / 800 | 0 |
| prop-bench-wood | 420 / 800 | 0 |
| prop-bookshelf | 672 / 800 | 1 (992 tris over budget: wider books, unbevelled shelves) |
| prop-bucket-wood | 372 / 800 | 0 |
| prop-candelabra | 382 / 800 | 0 |
| prop-cart-hand | 564 / 800 | 0 |
| prop-cauldron | 472 / 800 | 1 (light socket above the bounds, caught by the new check) |
| prop-door-wood | 588 / 2500 | 1 (Z-brace depth) |
| prop-fence-wood | 348 / 2500 | 0 |
| prop-keg-stand | 560 / 800 | 1 (cradle pierced the keg) |
| prop-ladder-wood | 296 / 800 | 0 |
| prop-lantern | 232 / 800 | 1 (glass hid the glow, so the whole core is Emissive) |
| prop-lectern | 300 / 800 | 1 (slope direction) |
| prop-sack-grain | 412 / 800 | 0 |
| prop-signpost | 222 / 800 | 1 (nail placement) |
| prop-stool-wood | 380 / 800 | 0 |
| prop-stump-axe | 168 / 800 | 0 |
| prop-torch-standing | 518 / 800 | 0 |
| prop-weapon-rack | 648 / 800 | 0 |
| prop-well-stone | 1704 / 2500 | 1 (roof and ridge heights) |
| Validation (Blender + Unity), hero scene, contact sheets | – | 1 (label strip, framing) |

## Next: M4
M4 is done (see the M4 section).

# Room-adapt rule + M3 QA fixes (2026-09-28, MDT, finished about 20:10)
Machine time: Blender build of all 42 assets about 15 s; a from-scratch `build.ps1 -Clean` (now including the room-adapt render checks and 2 new captures) about 72 s, passed.

| Work | Result | Fix iterations |
|---|---|---|
| Audit of all 42 assets (room scale, re-theme, lights, colour slots) | 8 structural pieces did not room-scale; 0/42 had user colour slots; 10 lacked a mesh region for a user slot | – |
| Runtime: `RoomSize`, 3 user colour slots (MaterialPropertyBlocks), `emissiveScale`, grid scaling | installed | 0 |
| Mesh fixes for colour regions (10 assets + well crank axle) | all pass | 0 |
| Blender `validate_roomadapt` + exceptions file | fail test rejected for both rules | 0 |
| Unity `ValidateRoomAdapt` (scale x3, re-theme x2, render diff per user slot) | hidden-Tertiary test rejected; tampered `scalesWithRoom` rejected | 1 (NewScene unloaded the theme profiles) |
| Found by the render check: prop-mushroom's Accent spots buried in the cap | raised onto the cap | 1 |
| Scenes on the scaled room grid (Modular, Hero), Catalog spacing/lighting, hero camera far planes | clean captures | 2 (catalog framing) |
| roomscale.png, colorslots.png | written | 1 (label length, framing) |

# M4 monsters + M3 follow-ups (2026-09-29, MDT)

5 monsters, category Monsters, milestone M4, all `SCALES_WITH_ROOM` True, room-adapt passed with 0 exceptions. Total assets 47 (M1 5, M2 15, M3 22, M4 5). Package: `Builds/OpenKit3D-M4.unitypackage`. Demo scene: `Scenes/Demo/OpenKit3D-M4Monsters.unity`.
Machine time: a from-scratch `build.ps1 -Clean` takes about 87 s (47 assets, 12:39:49-12:41:16 MDT, passed; Blender build of all 47 assets included). `-Clean` also clears `captures\m4`.
Grok Build was used for a first sack/stump draft (not kept; the box versions were used) and for these docs.

| Work | Result | Fix iterations |
|---|---|---|
| Rig helpers + rat | rigid bind at weight 1.0 and smooth `okit.AUTO` skin; rat body + tail skinned (weights blend along the spine/tail), legs/head rigid; 712 / 2500 tris, 12 bones; idle 48 f, walk 24 f | 1 |
| Golem | monster-golem-stone, rigid parts, head raised; 1592 / 5000 tris, 11 bones; idle 72 f, walk 40 f | 1 (head raised) |
| Hound | monster-construct-clockwork-hound, rigid parts; hinged jaw, 3-bone tail, turning wind-up key; 1808 / 5000 tris, 17 bones; idle 48 f, walk 24 f | 0 |
| Mimic | monster-mimic-chest, rigid parts; lid rests 25 deg open, teeth/tongue/eyes, 4 stubby legs; 1196 / 2500 tris, 7 bones; idle 48 f, walk 24 f | 0 |
| Skeleton | monster-skeleton-warrior, rigid parts; shield on left forearm, sword in right hand, helmet; 2076 / 5000 tris, 18 bones; idle 64 f, walk 32 f | 0 |
| Sack | standing sack is a squat, slumped, leaning pear with a gathered neck, tie cord, floppy 4-flap tuft and a Secondary patch; lying sack is a plump pillow with a tied flared end; 412 to 526 tris | 1 |
| Stump-axe | axe head 40% larger and lifted so only the cutting edge bites ~2.5 cm into the cut face; dark split in the cut face; 168 to 196 tris | 2 (axe head enlarged after the first Unity look) |
| Unity rigged import | Generic rig, looping clips, Animator (no root motion) and controller; mesh and rig nodes import at identity | 1 (mesh child imported with 90 deg X rotation -> FBX bake_space_transform on) |
| Readability palette/lights | Hell Primary (0.10,0.08,0.09, smooth 0.7) to (0.25,0.20,0.21, smooth 0.22), Metal (0.22,0.18,0.17) to (0.48,0.42,0.39); Heaven Secondary (0.66,0.76,0.92) to (0.46,0.56,0.78), Primary marble (0.93,0.92,0.88, smooth 0.55) to (0.88,0.86,0.80, smooth 0.45); wall torch 1.6 to 1.25; giant smithy warm front fill (intensity 7) + ember rim (intensity 10), outside ThemeRoom.roomLights | 2 (first pass too weak in the giant smithy) |
| Captures | `captures\m4\`: monster-lineup-roomsizes.png, monster-colorslots.png (Ash/Moss/Frost), monster-clips.png (4 frames per clip), m4-contact-sheet-dungeon.png, m4-contact-sheet-undead.png, catalog-m1-m4.png (47 assets), before-*/after-* pairs (sack-dungeon, sack-heaven, stump-axe, torch-wall-hell, torch-wall-dungeon, smithy, smithy-close, yard, yard-close) | 0 |

Weak spots: clips are procedural sine loops (placeholder quality, no foot locking; walk slides if moved); the rat Tertiary slot is small (inner ears/incisors/claws); lineup labels are small in the halfling room; the hound and rat look narrow in the head-on colour-slot view; skeleton limbs are thin at distance.
