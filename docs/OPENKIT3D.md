# Modular dungeon kit

Floor tile, walls, furniture and props, monsters and theme profiles, plus the scripts that handle room scale and colours, and the wall fade. Every piece carries a `ThemeAdaptive` component.

## What's in it

- **Structure:** `tile-dungeon-stone-floor`, `wall-dungeon-stone`, `wall-dungeon-stone-doorway`.
- **Props:** `prop-altar-stone`, `prop-anvil`, `prop-banner-standing`, `prop-barrel`, `prop-bed-simple`, `prop-bench-wood`, `prop-bookshelf`, `prop-brazier`, `prop-bucket-wood`, `prop-candelabra`, `prop-cart-hand`, `prop-cauldron`, `prop-chair-simple`, `prop-chest`, `prop-coffin`, `prop-crate`, `prop-door-stone`, `prop-door-wood`, `prop-fallen-pillar`, `prop-fence-wood`, `prop-keg-stand`, `prop-ladder-wood`, `prop-lantern`, `prop-lectern`, `prop-mushroom`, `prop-pew-bench`, `prop-pillar-stone`, `prop-sack-grain`, `prop-sarcophagus`, `prop-signpost`, `prop-stool-wood`, `prop-stump-axe`, `prop-table-wood`, `prop-throne-simple`, `prop-torch-standing`, `prop-torch-wall`, `prop-treasure-pile`, `prop-weapon-rack`, `prop-well-stone`.
- **Monsters:** `monster-skeleton-warrior`, `monster-giant-rat`, `monster-construct-clockwork-hound`, `monster-golem-stone`, `monster-mimic-chest`. Each has its own Animator Controller.
- **Themes** (`ThemeProfile` assets): `Crypt`, `Dungeon`, `Heaven`, `Hell`, `Jungle`, `Undead`, `Vault`, `Smithy`, `DungeonRat`.
- **Slot materials:** `Primary`, `Secondary`, `Accent`, `Metal`, `Emissive` (URP Lit).
- **Scripts:** `ThemeRoom`, `ThemeAdaptive`, `ThemeProfile` (namespace `OpenKit`), plus the `OccluderFade` marker, the `OcclusionFader` camera component and the `OpenKitDungeon/OccludeFadeLit` shader.
- **Effect:** the `SlashArc` mesh and the additive `Slash` material, for a weapon swipe.

## Import

Keep the `.meta` files. The models are already set up (Scale Factor 1, Bake Axis Conversion on, slot materials remapped). Monsters import as **Generic** with **Create From This Model**, and their `idle` and `walk` clips loop.

## Settings that matter

- **Room Size** on `ThemeRoom`: `Halfling` (0.75), `Human` (1), `Giant` (2) or `FromTheme`. Every piece under the room scales. To resize one piece, change its **Base Scale**, not its Transform.
- **Colours:** **Profile** on `ThemeRoom` sets the room palette. **User colour slots** on a piece's `ThemeAdaptive` override **Primary Color**, **Secondary Color** or **Tertiary Color** (tick **Enabled**). **Emissive Scale** dims that piece's glow.
- **Grid:** place tiles, walls and doors on a 1.5 m × room scale grid. **Snaps To Room Grid** only marks a piece as structural and doesn't move it, so set the Scene view grid snap to that size instead.
- **Fade:** `wall-dungeon-stone`, `wall-dungeon-stone-doorway` and `prop-pillar-stone` carry `OccluderFade` already. Add `OcclusionFader` to your camera to make them fade. See `HOW_TO_USE.md`, "Walls and roofs fade".
- **Monsters:** set the Bool `walk` on the monster's Animator to switch between `idle` and `walk`.

## Common tasks

**Build a giant's hall**

1. Create an empty GameObject named `Hall` and add `ThemeRoom`.
2. Set **Profile** to `Vault` and **Room Size** to `Giant`.
3. Place `tile-dungeon-stone-floor` pieces 3 m apart, then `wall-dungeon-stone` along the edges.

**Make your own theme**

1. Choose **Assets > Create > Open Kit 3D > Theme Profile**.
2. Set the **Palette** (a colour, metallic and smoothness per slot), **Emissive Intensity**, **Inhabitant Scale** and **Light Tint**.
3. Drag the new profile into a `ThemeRoom` **Profile**.

**Show a sword swipe**

1. Under the weapon, create a GameObject with a **Mesh Filter** (`SlashArc`) and a **Mesh Renderer** (`Slash`).
2. Turn it on for a few frames during the swing.
