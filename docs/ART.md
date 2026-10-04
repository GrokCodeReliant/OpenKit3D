# Scene art and icons

Beach and forest scenery, dungeon prop art, water and sky materials, and item and slot icons. The scenery and props carry `ThemeAdaptive` like the rest of the kit, so they follow a Theme Room's size (halfling 0.75, human 1.0, giant 2.0) and have three colour slots: Primary, Secondary and Tertiary.

## What's in it

- **Beach:** `cliff-rock-wall` (plus `-corner-out`, `-corner-in`, `-cap`), `ground-sand-ramp`, `prop-rock-small-a/b/c`, `prop-rock-medium-a/b`, `prop-boulder-large-a`, `tidepool-rim-s/m/l`, `cave-mouth-sea`, `wall-cave-rock`, `prop-shipwreck-hull`, `prop-mast-broken`.
- **Forest:** `tree-pine-a/b`, `tree-broadleaf-a/b`, `treeline-segment`, `ground-forest-patch`, `wall-ruin-stone-broken-100/175/250`, `wall-ruin-arch`, `tile-ruin-slab`, `prop-pillar-stub-mossy`.
- **Props:** `prop-chest-iron-banded` (child `Lid`), `prop-door-dungeon` (`Hinge_Leaf`), `prop-lever-wall` (`Handle`), `prop-barrel-banded`, `prop-crate-wood`.
- **Water and sky:** materials `Sea` (transparent), `Pool`, `M_Beach_Water`, `Sand`, `Rock`, `Wood`, `Shelf`, `Rail`, `Portal`, and the sky `BeachSky`. A swatch strip, `water_palette`, has the water colours.
- **Icons:** item icons `icon_armor.l.b01`, `icon_weapon.swd.b01`, `icon_weapon.gsw.b01`, `icon_weapon.bow.b01`, `icon_weapon.shd.b01`, `icon_potion`, `icon_potion.health.small_spare`, `icon_potion.health.large_spare`, `icon_coin` (256 px), and empty-slot silhouettes `slot_Armor`, `slot_MainHand`, `slot_OffHand`, `slot_Potion` (128 px, white).

## Import

Keep the `.meta` files. Models: Scale Factor 1, Convert Units on, Bake Axis Conversion on, Animation Type None, Generate Lightmap UVs off. Icons: Texture Type **Sprite (2D and UI)**, Sprite Mode Single, Alpha Is Transparency on, no mipmaps.

## Settings that matter

- **Scale:** put the pieces under a `ThemeRoom` and set **Room Size** to `Halfling`, `Human` or `Giant`. Space them on a 1.5 m × room scale grid. Change **Base Scale** on `ThemeAdaptive` to resize one piece, not its Transform.
- **Colours:** `ThemeAdaptive` > **User colour slots** > **Primary Color**, **Secondary Color**, **Tertiary Color** (tick **Enabled**). The materials are named for their slot, for example `M_Beach_Rock_Primary`, `_Secondary` and `_Accent` (Accent is the tertiary slot). In a Theme Room with no **Profile**, the pieces keep their natural colours; with a **Profile**, they take the theme's colours.
- **Fade:** the walls and structures already carry `OccluderFade`: the cliff rock wall, its cap and corners, the cave mouth, the cave rock wall, the ruin arch and broken ruin walls, the mossy pillar stub, the dungeon door, the shipwreck hull and the broken mast. The cliff rock and ruin stone materials use the fade shader. Trees aren't marked; add `OccluderFade` to a tree's root if it should fade. Never add it to sand or ground.
- **Colliders:** trees have one around the trunk and none on the canopy.

## Common tasks

**Make a sea**

1. Create **3D Object > Plane**, scale it over the sea area and assign `Sea`.
2. Place it just below the shore, then add `ground-sand-ramp` pieces down to the water.

**Open the chest in an animation**

1. Select `Lid` under `prop-chest-iron-banded`.
2. In the Animation window, key Rotation X at 0, then at −100 a few frames later.

**Show an icon in a UI slot**

1. Add a UI **Image** to your Canvas.
2. Set **Source Image** to `slot_OffHand` for an empty slot, or to `icon_weapon.shd.b01` when the slot is filled.

## Known issues

- The sword icon `icon_weapon.swd.b01` currently shows the greatsword, not the one-hand sword.
