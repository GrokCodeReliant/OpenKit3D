# openkit-forge-props-b1

Open Kit forge/smithy props. 4 props, slots-only FBX, 1 unit = 1 m, Y-up, bottom_centre pivot.

| asset | tris | size m (x,y,z) | slots | notes |
|---|---|---|---|---|
| prop-anvil-fg1 | 108 | [0.81, 0.892, 0.5] | Iron, Wood | iron anvil on 0.5 m wood stump, working face ~0.87 m, horn +X |
| prop-forge-hearth | 108 | [1.45, 2.9, 1.06] | Stone, Brick, Ember | 1.4 x 1.0 m stone base, ember bed y=0.84, open brick mouth 1.0 w x 0.6 h, hood+chimney to 2.9 m |
| prop-bellows | 116 | [1.14, 0.35, 0.4] | Wood, Leather, Iron | floor bellows 1.25 m incl handle (-X) and iron nozzle (+X), 0.4 m wide, 0.35 m tall |
| prop-quench-barrel | 184 | [0.85, 0.54, 0.85] | Wood, IronDark, Water, Steam | short open quench tub 0.86 m dia x 0.5 m, 2 dark iron bands, water at 0.42 m, steam stub cone |

- `prop-anvil-fg1`: renamed from `prop-anvil` (existing in okm4 / openkit v0.3).
- `prop-forge-hearth`: open stone/brick forge mouth with hood + chimney; distinct from light-hearth brazier / campfire-ring-iron.
- `prop-quench-barrel`: short open quench tub w/ dark iron bands + steam stub; distinct from prop-barrel-wood / prop-water-barrel.

## FX attach (prop-forge-hearth, Unity local)
- `FX_ForgeMouth` (0, 0.95, 0.05): fire/ember glow over `Ember` slot, mouth faces local -Z... verify facing in engine.
- `FX_ChimneySmoke` (0, 2.9, -0.15).
- quench steam: (0.12, 0.6, -0.05) on prop-quench-barrel.

