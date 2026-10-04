# Open Kit 3D v0.3

Free low-poly 3D assets for Unity (URP): a modular dungeon kit, beach and forest scenery, props, monsters, and a male and female hero rig with weapons, armor and Humanoid animations. Everything is released under CC0 1.0. See [LICENSES.md](LICENSES.md) and [CREDITS.md](CREDITS.md).

## The three rules of the kit

1. **Rooms scale to three sizes:** halfling, human and giant.
2. **Every piece has exactly three colours you can set:** primary, secondary and tertiary.
3. **Walls and roofs fade see-through** when they come between the camera and the hero.

## What's inside

| Folder | Contents | Guide |
| --- | --- | --- |
| `ART` | Beach and forest scenery, dungeon prop art, water and sky materials, item and slot icons | [Scene art and icons](docs/ART.md) |
| `OPENKIT3D` | Modular dungeon tiles, walls, props and monsters, theme profiles, slot materials, and the room scale and colour scripts | [Modular dungeon kit](docs/OPENKIT3D.md) |
| `OPENKITPROPSNEW` | Pickups, traps, an arch, short stairs and a locked iron door | [Pickups, traps and passage pieces](docs/OPENKITPROPSNEW.md) |
| `HERORIG` | Male and female hero, attach points, body types, weapons, leather armor, gear materials and colour table, rig scripts, and the hero Animator Controller with its clips and masks | [Hero rig, gear and armor](docs/HERORIG.md) |
| `DUNGEONHEROGLUE` | A gear catalog asset that maps part names to prefabs | [Hero glue](docs/DUNGEONHEROGLUE.md) |
| `CHARACTERTRACK-ANIMATIONS` | Extra Humanoid clips for the hero | [Character animations](docs/CHARACTERTRACK-ANIMATIONS.md) |

A few supporting folders ship alongside these: body coverage for the hero, shared level materials, extra item icons, and the wall fade (camera component, marker and shader) with extra themes and the slash effect. The guides cover them with the family that uses them.

## Coming in v0.3.1

These pieces are planned for v0.3.1.

- `ground-sand-patch`
- `prop-boulder-large-b`
- `tile-sand`
- `fx-surf-strip`
- `path-dirt-strip`
- `path-dirt-strip-bend`
- `prop-bush-a`
- `prop-bush-b`
- `prop-fern-a`
- `prop-fern-b`
- `prop-log-fallen`
- `prop-portal-exit`
- `prop-torch-sconce`
- `prop-trap-spikes-plate`
- `pickup-coin-stack`
- `pickup-key`

## Getting started

Read [docs/HOW_TO_USE.md](docs/HOW_TO_USE.md). It covers importing, room scale, the three colour slots, the wall and roof fade, putting gear on the hero, body types and the animations, all by hand in the Unity Editor.

## Requirements

- Unity 6 with the Universal Render Pipeline.
- Keep each `.meta` file next to its asset when you copy folders. The import settings are stored there.

## Not included

Gameplay systems and raw third-party animation packs aren't included.

## Note

Built by an AI crew running on Grok.
