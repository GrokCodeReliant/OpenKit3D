# Open Kit 3D: how to use it by hand

This guide is for people using Unity without AI tools or generators. It covers importing the kit, sizing rooms, recolouring pieces, making walls and roofs fade, dressing the hero and playing the animations.

## The three rules of the kit

1. **Rooms scale to three sizes: halfling, human and giant.** Set one value on the room and every kit piece inside it resizes. See [Room scale](#room-scale-halfling-human-giant).
2. **Every piece has exactly three colours you can set: primary, secondary and tertiary.** See [The three colour slots](#the-three-colour-slots).
3. **Walls and roofs fade see-through when they come between the camera and the hero.** Floors never fade. See [Walls and roofs fade](#walls-and-roofs-fade).

## Requirements

- Unity 6 with the Universal Render Pipeline (URP). The materials use URP shaders and show pink in the Built-in pipeline.
- 1 unit = 1 metre. The room grid is 1.5 m per cell at human size.
- Models are low-poly and flat-shaded. Colour comes from materials, not textures.

## Quick start

1. Create a project from Unity's **Universal 3D** template, or open a URP project you already have.
2. Copy the kit's folders into your project's `Assets` folder. Keep every `.meta` file next to its asset: the import settings are stored there.
3. Wait for the import to finish, then check the Console for errors.
4. Create an empty GameObject named `Room`, add the **Theme Room** component and set **Room Size** to `Human`.
5. From the modular dungeon kit, drag `tile-dungeon-stone-floor`, `wall-dungeon-stone` and a few props under `Room`.
6. Set **Profile** on the Theme Room to a theme, for example `Dungeon`. Everything under the room takes that theme's colours.
7. Drag `Hero_Male` or `Hero_Female` into the scene.

## Family index

| Family | Folder | What's in it |
| --- | --- | --- |
| [Scene art and icons](ART.md) | `ART` | Beach and forest scenery, dungeon prop art, water and sky materials, item and slot icons |
| [Modular dungeon kit](OPENKIT3D.md) | `OPENKIT3D` | Floor tile, walls, doorway, furniture and props, monsters, theme profiles, the room scale and colour scripts. The guide also covers the wall fade, extra themes and slash effect, which ship in a supporting folder. |
| [Pickups, traps and passage pieces](OPENKITPROPSNEW.md) | `OPENKITPROPSNEW` | Potion and sword pickups, spike and blade traps, arch, short stairs, locked iron door |
| [Hero rig, gear and armor](HERORIG.md) | `HERORIG` | Male and female hero, attach points, body types, weapons, leather armor, colour table. The guide also covers body coverage, which ships in a supporting folder. |
| [Hero glue](DUNGEONHEROGLUE.md) | `DUNGEONHEROGLUE` | How the gear and armor connect to the hero rig: attach points, slots, rigid and skinned gear, and a gear catalog asset |
| [Character animations](CHARACTERTRACK-ANIMATIONS.md) | `CHARACTERTRACK-ANIMATIONS` | The hero Animator Controller, Humanoid clips, hand poses, masks and extra clips |

The scale and colour scripts (`ThemeRoom`, `ThemeAdaptive`, `ThemeProfile`) are in the modular dungeon kit. Most families need it.

Pieces that are still being finished are listed in [Coming in v0.3.1](../README.md#coming-in-v031).

## Importing

- **Use the prefabs, not the raw models.** The prefabs carry the colliders, materials and components.
- **Unity package:** if you have a `.unitypackage`, choose **Assets > Import Package > Custom Package**, leave every box ticked and click **Import**.
- **Loose folders:** copy them with their `.meta` files. If a `.meta` file is lost, set the model by hand from this table (Inspector, **Model** and **Rig** tabs):

| Models | Scale Factor | Bake Axis Conversion | Rig > Animation Type | Import BlendShapes | Read/Write |
| --- | --- | --- | --- | --- | --- |
| Tiles, walls, props, beach, forest | 1, Convert Units on | on | None | off | on for beach and forest, otherwise off |
| Monsters | 1, Convert Units on | on | Generic, Avatar **Create From This Model** | off | off |
| Hero (`HeroMale`, `HeroFemale`) | 1, Convert Units on | on | **Humanoid**, Avatar **Create From This Model** | **on** | on |
| Armor (`ARM_L_B01_M`, `ARM_L_B01_F`) | 1, Convert Units on | on | Generic, no avatar | **on** | on |
| Weapons (`WPN_*`) | 1, Convert Units on | on | None | on | on |

Leave **Generate Lightmap UVs** off on every model. The armor and weapons keep a wear mask in UV2, and lightmap UVs would overwrite it.

Shaders used: `Universal Render Pipeline/Lit` (most pieces), `Universal Render Pipeline/Unlit` (slash effect), `HeroRig/FlatVertexColor` (hero, gear and armor), `HeroRig/FlatVertexColorCoverage` (hero body while armor is on), `OpenKitDungeon/OccludeFadeLit` (pieces that fade) and `Skybox/Procedural` (`BeachSky`).

## Room scale (halfling, human, giant)

| Room Size | Scale | Grid cell |
| --- | --- | --- |
| `Halfling` | 0.75 | 1.125 m |
| `Human` | 1 | 1.5 m |
| `Giant` | 2 | 3 m |

**Every kit piece has a settable size and three colour slots.** The modular dungeon kit, the beach, forest and dungeon prop art, the pickups, traps and passage pieces, and the monsters do it with a Theme Adaptive component:

1. Put the pieces under a GameObject that has `ThemeRoom`.
2. Set **Room Size** to `Halfling`, `Human` or `Giant`. `FromTheme` uses the theme profile's **Inhabitant Scale** instead.
3. Place tiles, walls and doors on a grid of 1.5 m × the room scale.

Don't type a scale into these pieces' Transforms: `ThemeAdaptive` overwrites it with **Base Scale** × room scale. To resize one piece, change its **Base Scale**. To keep one piece from following the room, untick **Scales With Room**.

**Hero and gear** do it with `HeroProportions` and `HeroGearLook`. See [Hero rig, gear and armor](HERORIG.md).

**The hero:** set **Uniform Scale** on `HeroProportions` to 0.75 or 1. The slider stops at 1.6, so for a giant put the hero under an empty parent scaled (2, 2, 2) and leave Uniform Scale at 1. `HeroProportions` writes the hero root's scale, so don't scale the root itself.

Giant scale on the hero is untested.

## The three colour slots

You can set three colours: **Primary**, **Secondary** and **Tertiary**. Glow (emissive) follows the theme and isn't a user colour.

**Dungeon kit, scene art, pickups, traps, passage pieces and monsters** set their colours on **Theme Adaptive**. Each material is named for its slot, ending in `Primary`, `Secondary`, `Accent`, `Metal` or `Emissive`. Tertiary tints `Accent` and `Metal` together (trim and hardware).

1. Select the piece and find **Theme Adaptive**.
2. Under **User colour slots**, open **Primary Color**, **Secondary Color** or **Tertiary Color**.
3. Tick **Enabled** and pick a **Color**. Untick it to go back to the theme colour.

The colour goes into a material property block, so other pieces don't change. To recolour a whole room, change the `ThemeRoom` **Profile**, or make a new one with **Assets > Create > Open Kit 3D > Theme Profile**. From code: `GetComponent<OpenKit.ThemeAdaptive>().SetUserColor(OpenKit.UserColorSlot.Primary, Color.red);` Pass `null` to clear it.

In a Theme Room with no **Profile**, a piece keeps its own materials, so beach and forest art keep their natural colours. With a **Profile**, the piece takes the theme's colours. The user colour slots override either.

**Gear and armor.** One shared material with Primary, Secondary and Tertiary parts, plus a fixed Dark trim. See [Hero rig, gear and armor](HERORIG.md#colours).

**Hero body.** Skin, hair and clothing have their own materials (`M_Skin`, `M_Hair`, `M_Tunic`, `M_Trousers`, `M_Trim`, `M_Belt`, `M_Wraps`, `M_Lip`, `M_Eye` and `_Female` versions). Change **Base Color** on a duplicate to tint one hero.

## Walls and roofs fade

The rule: anything that can block the view of the hero, meaning walls, pillars, roofs, cliffs, cave rock, ruins, arches and doors, fades to a see-through dither while it's between the camera and the hero, then fades back. Floors, ground, sand, tiles and water never fade, and neither does the hero.

Three parts do the work:

- **`OcclusionFader`**, the fade driver. It goes on the camera. Each frame it casts from the camera to the hero's chest and head and fades every marked piece in the way, over 0.15 s each way.
- **`OccluderFade`**, an empty marker. Put it on a piece's parent and every renderer under it can fade. The kit's walls and structures already carry it: the dungeon stone wall and doorway, the stone pillar, the dungeon door, the stone hall arch, the locked iron door, the cliff rock wall with its cap and corners, the cave mouth, the cave rock wall, the ruin arch and broken ruin walls, the mossy pillar stub, the shipwreck hull and the broken mast.
- **The fade shader**, `OpenKitDungeon/OccludeFadeLit`. It dithers a piece out using the keyword `_OCCLUDE_FADE_ON` and the value `_OccludeFade` (1 is solid). The driver sets the value on each renderer, so shared materials aren't changed.

**Set up the camera**

1. Select your camera and click **Add Component > Occlusion Fader**.
2. Drag the hero's root object into **Hero**.
3. Set **Level Mask** to the layers your walls and structures are on. The kit prefabs are on the `Default` layer. If you leave **Level Mask** at `Nothing`, the driver uses a layer named `Level` if one exists.
4. Leave **Cast Radius** at 0.22 m. It's the width of the cast from the camera to the hero.
5. Press Play and walk the hero behind a wall.

**Mark your own pieces**

1. Select the parent object of the wall, roof or other blocking piece.
2. Click **Add Component** and choose **Occluder Fade**.
3. Give the piece a collider on a layer in **Level Mask**. The driver finds pieces by their colliders.
4. For trees, mark the trunk and canopy, never the ground under them.

Pieces whose object name contains `wall`, `pillar`, `roof`, `cliff`, `doorway`, `cave-rock` or `ruin` also fade without the marker. Names containing `floor`, `ground`, `sand`, `tile-` or `water` never fade, and nor do names containing `lever` or `loot`.

**Materials**

- Any URP Lit material works. When a piece first fades, the driver makes a fading copy of its material on the fade shader and keeps the base colour, base map, metallic and smoothness.
- To set it up ahead of time, switch the material's **Shader** to `OpenKitDungeon/OccludeFadeLit`. The beach cliff rock and forest ruin materials already use it.
- Keep the `M_OccludeFadeLit` material where it ships, in a `Resources` folder. The driver loads it to find the fade shader in builds.

## Attaching gear to the hero

The hero has named attach points, which the `HeroAttachPoints` component finds:

| Attach point | Follows | Use |
| --- | --- | --- |
| `Grip_MainHand` (under `Socket_MainHand`) | right hand | Sword, greatsword |
| `Grip_OffHand` (under `Socket_OffHand`) | left hand | Shield, bow |
| `Socket_Head` | head | Helmet or cap |
| `Socket_Shoulder_L`, `Socket_Shoulder_R` | shoulders | Shoulder props you set to `Rigid`. The kit's shoulder armor is skinned and doesn't use them. |
| `Socket_Chest` | upper chest | Rigid chest piece |
| `Socket_Back_2H`, `Socket_Back_Bow`, `Socket_Back_Shield` | upper chest | Weapons carried on the back |
| `Socket_Hip_L`, `Socket_Hip_R`, `Socket_Belt` | hips | Hip weapon, pouch, quiver |

**Rigid gear by hand** (weapons, shield):

1. Expand the hero in the Hierarchy and find the attach point, for example `Grip_MainHand`.
2. Drag the weapon prefab onto it.
3. Set the weapon's Position and Rotation to (0, 0, 0) and Scale to (1, 1, 1). Don't change any rotation on the weapon's inner mesh child.

**Armor** is skinned to the skeleton, so it needs the `HeroEquipment` component and a few lines of code. See [Hero rig, gear and armor](HERORIG.md#put-armor-on-the-hero) and [Hero glue](DUNGEONHEROGLUE.md). The calls are `Equip(HeroGearSlot, prefab)`, `EquipItem(armorRoot)`, `EquipArmor(item, tier, q)`, `Unequip(slot)`, `UnequipArmor()` and `UnequipAll()`. Slots: `Head`, `Shoulders`, `Chest`, `Hands`, `Legs`, `Feet`, `MainHand`, `OffHand`.

## Swapping body types

| Hero | Weight 0 | Weight 1 | Blend shape |
| --- | --- | --- | --- |
| Male | Lean | Strong | `BodyType_Strong` |
| Female | Petite | Curvy (the blend shape named Busty) | `BodyType_Busty` |

1. Select the hero root.
2. On **Hero Body Type**, drag **Weight** between 0 and 1. Or right-click the component and choose **Body type: base** or **Body type: full alternate**.
3. Equipped armor carries the same blend shape and follows.

From code, call `HeroEquipment.SetBodyType(weight)`. `HeroProportions` adds **Height**, **Limb Length** and **Bulk**.

## Using the animations

The hero clips are **Humanoid**, so they play on the kit hero and on any other Humanoid character. The monster clips are **Generic** and only play on their own models.

1. The hero prefabs already have the `HeroRig` controller and their own **Avatar** on the **Animator**. On another Humanoid character, set **Controller** to `HeroRig` and keep that character's own avatar.
2. Drive `WeaponType` (Int), `Speed` (Float: 0 idle, 0.4 walk, 1 run), `Slash` and `Thrust` (Triggers), `Block` (Bool), and `Hit` and `Die` (Triggers).
3. Set the combat layer that matches the weapon to weight 1, or let `HeroWeaponController` do it.

The full guide is in [Character animations](CHARACTERTRACK-ANIMATIONS.md).

## License and credits

Quoted from [LICENSES.md](../LICENSES.md). Thanks are in [CREDITS.md](../CREDITS.md).

> All of Open Kit 3D v0.3 is dedicated to the public domain under CC0 1.0: https://creativecommons.org/publicdomain/zero/1.0/. You can use, change and share it for any purpose, including commercial use. No credit is required.
>
> Files derived from these packs were CC0 at the source:
>
> - KayKit Character Animations by Kay Lousberg, CC0 1.0. Source: https://kaylousberg.itch.io/kaykit-character-animations
> - Quaternius Universal Animation Library 2 (UAL2), CC0 1.0. Source: https://quaternius.itch.io/universal-animation-library-2
>
> This release contains no third-party material other than the CC0 sources listed above.
