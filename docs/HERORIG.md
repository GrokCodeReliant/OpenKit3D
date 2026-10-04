# Hero rig, gear and armor

A male and a female low-poly Humanoid hero with named attach points and a body-type blend shape, plus weapons and a light leather armor set made to fit them. Scripts are in the `HeroRig` namespace.

## What's in it

- **Heroes:** `Hero_Male` and `Hero_Female` (models `HeroMale` and `HeroFemale`). Root components: `HeroAttachPoints` (finds the sockets), `HeroEquipment` (equips gear; **Sex** must match the mesh), `HeroBodyType`, `HeroProportions`, `HeroWeaponController` (sets the Animator's weapon layers), `HeroDeformDriver` (corrective `CR_*` shapes at knees, elbows, hips and shoulders), `HeroFootIK` and `HeroShieldIK`.
- **Weapons:** each has `HeroGearItem` (slot, mode, item id) and `HeroGearLook`.

| Prefab | Hand | Carried on |
| --- | --- | --- |
| `WPN_SWD_B01` one-hand sword | `Grip_MainHand` | `Socket_Hip_L` |
| `WPN_GSW_B01` greatsword | `Grip_MainHand` | `Socket_Back_2H` |
| `WPN_BOW_B01` short bow, `WPN_BOW_B01_Arrow` | `Grip_OffHand` | `Socket_Back_Bow` |
| `WPN_SHD_B01` round shield | `Grip_OffHand` | `Socket_Back_Shield` |

- **Armor:** `ARM_L_B01_M` (for `Hero_Male`) and `ARM_L_B01_F` (for `Hero_Female`). Parts: `_HEAD` (rigid, on `Socket_Head`) and `_SHLD`, `_CHST`, `_HAND`, `_LEGS`, `_FEET` (skinned to the hero's bones). Chest and legs hide the base clothing (**Hides Clothing**).
- **Colour and coverage:** material `M_Gear`, colour table `GearLookTable`, and `HeroBodyCoverage` with `M_BodyCoverage` and `CoverageTable`.

## Import

Keep the `.meta` files. Hero: **Humanoid**, **Create From This Model**, Import BlendShapes on. Armor: **Generic**, no avatar, Import BlendShapes on. Weapons: Animation Type **None**. All: Generate Lightmap UVs off. Don't zero the import rotation on a weapon's inner mesh child.

## Weapons the quick way

1. Select the hero and find `HeroWeaponController`.
2. Set **Current** to `OneHand`, `OneHandShield`, `TwoHand` or `Bow`, then press Play. Its **Loadouts** attach the kit weapons and set the Animator.

By hand: drag a weapon onto its grip and set Position and Rotation to 0 and Scale to 1. From code: `hero.GetComponent<HeroEquipment>().Equip(HeroGearSlot.MainHand, prefab);`

## Colours

Gear has three colours you can set, **Primary**, **Secondary** and **Tertiary**, plus a fixed **Dark** trim. `HeroGearLook` shows which material element is which (**Primary Submesh**, **Secondary Submesh**, **Tertiary Submesh**, **Dark Submesh**). These differ per piece. Without colours set, gear shows white.

**By hand:** duplicate `M_Gear` for Primary, Secondary and Tertiary, set each copy's **Base Color**, and put each copy in the matching element of the piece's renderer **Materials** list. Leave the Dark element on `M_Gear`. **Wear**, **Finish** and **Emissive** / **Emissive Color** add scuffs, shine and glow.

**From the table:** in `GearLookTable` (or a new one, **Assets > Create > HeroRig > Gear Look Table**), set a **Primary** per base id under **Bases** (for example `armor.l.b01`). Set **Secondary**, **Tertiary**, finish, wear and glow under **Tiers** (`Common` to `Legendary`). Then equip with `EquipArmor` or `EquipWeapon`, which apply the table colours over the materials.

## Put armor on the hero

1. Create an item: **Assets > Create > HeroRig > Armor Item**. Set **Male Prefab** to `ARM_L_B01_M`, **Female Prefab** to `ARM_L_B01_F` and **Look** to `GearLookTable`.
2. From your script, call:

```csharp
hero.GetComponent<HeroRig.HeroEquipment>().EquipArmor(armorItem, 0, 0.5f); // tier 0-4, quality 0-1
```

It picks the set that matches **Sex**. `UnequipArmor()` removes the armor and leaves the weapons. Main-hand weapons (sword, greatsword) work the same way with **Assets > Create > HeroRig > Weapon Item** and `EquipWeapon`. Equip the bow and shield with `Equip(HeroGearSlot.OffHand, prefab)`.

**Hide skin under armor:** add `HeroBodyCoverage` to the hero, set **Template** to `M_BodyCoverage` and **Table** to `CoverageTable`, and call `Reapply()` after each equip.

## Common tasks

**Make a stocky halfling**

1. On `HeroProportions`, set **Uniform Scale** to 0.75 and **Bulk** to 0.6.
2. On `HeroBodyType`, set **Weight** to 1. Equipped armor follows.

**Carry the greatsword on the back**

1. Drag `WPN_GSW_B01` onto `Socket_Back_2H`.
2. Rotate it until it sits clear of the body.
