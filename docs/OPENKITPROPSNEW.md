# Pickups, traps and passage pieces

Small ready-to-use props: pickups that bob and glow, traps, and passage pieces. They all use the theme slot materials and carry `ThemeAdaptive`, so they follow a Theme Room's size and colours.

## What's in it

| Piece | Notes |
| --- | --- |
| `pickup-potion`, `pickup-sword` | Trigger collider, soft point light `Glow`, and `PropBob` |
| `trap-floor-spikes` | Fills one floor cell. Moving child: `Spikes` |
| `trap-swinging-blade` | Hangs from a ceiling bracket. Moving child: `Arm` |
| `hall-arch-stone` | Frames a hallway. Children `PostL` and `PostR` |
| `stairs-stone-short` | Short rise. Children `Ramp` and `Landing` |
| `door-iron-locked` | Single door leaf, pivot on the hinge |

The meshes are stored inside the kit as mesh assets, so there are no model import settings to change.

## Settings that matter

- **Scale:** put the pieces under a `ThemeRoom` and set **Room Size** (`Halfling`, `Human`, `Giant`). Change **Base Scale** on `ThemeAdaptive` to resize one piece.
- **Colours:** `ThemeAdaptive` > **User colour slots** > **Primary Color**, **Secondary Color**, **Tertiary Color**.
- **Bob and spin:** on `PropBob`, **Amplitude** is the bob height in metres and **Spin** is degrees per second. Set both to 0 for a still pickup.
- **Fade:** `hall-arch-stone` and `door-iron-locked` already carry `OccluderFade`, so they fade when they block the camera once `OcclusionFader` is on your camera. Never add it to traps or pickups.

## Common tasks

**Make the potion collectable**

1. Place `pickup-potion`. Its trigger collider is already set.
2. Add your own script with `OnTriggerEnter` that checks for the player and then disables the pickup.

**Animate the spike trap**

1. Select `Spikes` under the placed `trap-floor-spikes`.
2. In the Animation window, key its local Position Y low (hidden), then up (raised) a few frames later, and loop the clip.

**Open the iron door**

1. Select the placed `door-iron-locked`.
2. Animate its Rotation Y. The pivot is on the hinge, so it swings like a real door.

**Frame a hallway**

1. Place `hall-arch-stone` across the hallway opening, on the 1.5 m × room scale grid.
2. Add `stairs-stone-short` where the floor steps up.
