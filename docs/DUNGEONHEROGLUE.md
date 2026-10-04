# Hero glue

How the kit's gear and armor connect to the hero rig: the attach points, the equipment slots, rigid versus skinned gear, and a small catalog asset that maps part names to prefabs. The scripts are in the `HeroRig` namespace. The catalog is in `OpenKitDungeon`.

## Attach points

`HeroAttachPoints` on the hero root finds these by name. Call `Bind()` after you add or rebuild a hero from code.

| Attach point | Field | Follows |
| --- | --- | --- |
| `Grip_MainHand` (under `Socket_MainHand`) | `gripMainHand` | right hand |
| `Grip_OffHand` (under `Socket_OffHand`) | `gripOffHand` | left hand |
| `Socket_Head` | `socketHead` | head |
| `Socket_Shoulder_L`, `Socket_Shoulder_R` | `socketShoulderL`, `socketShoulderR` | shoulders |
| `Socket_Chest` | `socketChest` | upper chest |
| `Socket_Back_2H`, `Socket_Back_Bow`, `Socket_Back_Shield` | `socketBack2H`, `socketBackBow`, `socketBackShield` | upper chest |
| `Socket_Hip_L`, `Socket_Hip_R`, `Socket_Belt` | `socketHipL`, `socketHipR`, `socketBelt` | hips |

Grip axes: +Y runs along the handle toward the tip, and +Z is the back of the hand (the shield face). A weapon whose origin is the centre of its handle sits in the fist at zero position and rotation.

## Slots and how gear is attached

The hero root has one child per slot, named `EquipSlot_<Slot>`, each with a `HeroEquipSlot`. `HeroEquipment.Equip(slot, prefab)` routes gear to it. Each gear piece's `HeroGearItem` sets **Slot**, **Mode** (`Auto`, `Rigid` or `Skinned`), an optional **Local Position**, **Local Euler** and **Local Scale**, and **Hides Clothing**.

| Slot | Default mode | Where it goes |
| --- | --- | --- |
| `MainHand`, `OffHand` | Rigid | `Grip_MainHand`, `Grip_OffHand` |
| `Head` | Rigid | `Socket_Head` |
| `Shoulders` | Skinned (the kit's leather shoulders) | Re-bound to the hero's bones, like the chest. A piece you set to `Rigid` instead goes on the shoulder sockets: children ending `_L` and `_R` go to the matching side, and a single piece goes on the left with a mirrored copy on the right. |
| `Chest`, `Hands`, `Legs`, `Feet` | Skinned | Re-bound to the hero's bones |

**Rigid** gear is parented to its attach point. Its own root rotation is kept and the `HeroGearItem` offsets are added on top.

**Skinned** gear is re-bound to the hero's skeleton by bone name. The renderer moves under the hero root next to the body, and the piece's own copy of the skeleton is deleted. Body type, bulk and corrective shapes then drive it like the body. If a bone name is missing, the Console logs an error and the nearest parent bone is used.

**A rigid piece in a skinned slot** (for example a simple cube as a test) gets one copy per anchor: chest on `Socket_Chest`, hands on both hands, legs on both lower legs, feet on both feet.

**Whole sets:** `HeroEquipment.EquipItem(root)` splits a set by the part code in each child's name, `_HEAD`, `_SHLD`, `_CHST`, `_HAND`, `_LEGS` or `_FEET`, and equips each part in its slot.

## Using the gear on another rig

- **Rigid gear** (weapons, shield, helmet) works on any character. Parent it to a hand or head bone and adjust the rotation by eye.
- **Skinned armor** only binds to a skeleton with the kit hero's bone names. On other characters, treat each part as a rigid prop or re-skin it in a 3D app.
- **Animations** are Humanoid, so they work on any character set to Humanoid. See [Character animations](CHARACTERTRACK-ANIMATIONS.md).

## Gear catalog

`HeroGearCatalog` is a ScriptableObject with a list of **Entries**, each a **Variant Name** and a **Prefab**. `PrefabFor(name)` returns the prefab for a name. `HeroGearCatalog.WithLeatherDefaults()` creates a catalog with empty rows `ARM_L_B01_M_HEAD` to `ARM_L_B01_F_FEET` for you to fill in.

**Make a catalog asset**

1. In an editor script, call `HeroGearCatalog.WithLeatherDefaults()` and save the result with `AssetDatabase.CreateAsset`.
2. Select the new asset and fill in each row's **Prefab**.
3. In your own script, look up a part with `catalog.PrefabFor("ARM_L_B01_M_CHST")` and pass it to `HeroEquipment.Equip`.

## Common task

**Test a new helmet**

1. Make your helmet model with its origin where it should sit on the head.
2. Add `HeroGearItem` and set **Slot** to `Head` and **Mode** to `Rigid`.
3. Save it as a prefab and call `hero.GetComponent<HeroRig.HeroEquipment>().Equip(HeroRig.HeroGearSlot.Head, helmetPrefab);`
4. If it's off, change **Local Position** and **Local Euler** on the prefab's `HeroGearItem` and equip it again.
