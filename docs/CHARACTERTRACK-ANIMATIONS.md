# Character animations

The hero's Animator Controller, its Humanoid clips, hand poses and avatar masks, and extra clips you can add yourself. Humanoid clips play on the kit hero and on any other Humanoid character. The controller, idles, combat set, movement clips, hand poses and masks are in the `HERORIG` folder. The extra sword and shield clips sit in the hero rig's animation library. The other extra clips are in the `CHARACTERTRACK-ANIMATIONS` folder.

## What's in it

- **Controller:** `HeroRig`. The hero prefabs already use it.
- **Idles by weapon:** `Idle_Unarmed`, `Idle_OneHand`, `Idle_OneHandShield`, `Idle_TwoHand`, `Idle_Bow`, `Idle_Staff`.
- **One-hand and shield set:** `OHS_Idle`, `OHS_Walk`, `OHS_Run`, `OHS_Slash`, `OHS_Thrust`, `OHS_BlockEnter`, `OHS_BlockHold`, `OHS_BlockExit`, `OHS_Hit`, `OHS_Death`. `OHS_Hit` and `OHS_Death` are simple placeholders.
- **Movement:** `Walking_A`, `Running_A`, `Melee_2H_Idle`, `Ranged_Bow_Idle`, `Running_HoldingBow`.
- **Extra sword and shield clips (not in the controller):** standalone clips in the hero rig's animation library that you can drop into your own controller.
  - `Sword_Regular_A`, `Sword_Regular_B`, `Sword_Regular_C`: three sword attacks, labelled A, B and C.
  - `Sword_Dash_RM`: a sword dash attack with root motion, so it moves the character.
  - `Shield_Dash_RM`: a shield dash with root motion, so it moves the character.
  - `Shield_OneShot`: a single shield move.
- **Hand poses:** `Hands_Grip_Fist`, `Hands_Bow_Fist`. **Masks:** `UpperBody`, `Hands_Grip`, `Hands_Bow`.
- **Extra clips (not in the controller):** `KK_Spin` (looping spin) and `KK_BowShot` (one bow shot).

## Controller parameters

| Parameter | Type | Use |
| --- | --- | --- |
| `WeaponType` | Int | 0 Unarmed, 1 OneHand, 2 OneHandShield, 3 TwoHand, 4 Bow, 5 Staff |
| `Speed` | Float | 0 idle, 0.4 walk, 1 run |
| `Slash`, `Thrust` | Trigger | Attacks |
| `Block` | Bool | Block enter, hold, exit |
| `Hit`, `Die` | Trigger | Flinch, death |
| `LeftFootPlant`, `RightFootPlant` | Float | Foot plant weights for `HeroFootIK` |

## Layers

| Layer | Starts at | Holds |
| --- | --- | --- |
| `Base Layer` | 1 | `Idle` |
| `UpperBody_Weapon` | 1 (mask `UpperBody`) | One idle per `WeaponType` |
| `OneHandShield_Combat` | 0 | Move blend, `Thrust`, `Slash`, block, `Hit`, `Die` |
| `TwoHand_Combat` | 0 | Move blend, `Slash` |
| `Bow_Combat` | 0 | Move blend, `Slash` |
| `Hands_Grip`, `Hands_Bow` | 0 | Closed fist, bow grip |

Set the `_Combat` layer that matches the weapon to 1 and the others to 0. Without that, walk and run don't show. `HeroWeaponController` does it for you when you set **Current** or call `Equip(WeaponType)`. Set `Hands_Grip` to 1 while a weapon is in the right hand and `Hands_Bow` to 1 while holding the bow.

## Common tasks

**Walk and attack from a script**

1. Get the hero's `Animator`.
2. Each frame: `animator.SetFloat("Speed", 0.4f);` to walk (1 to run, 0 to stand).
3. On attack: `animator.SetTrigger("Slash");`

**Add the spin clip**

1. Open `HeroRig` in the Animator window and select `OneHandShield_Combat`.
2. Drag `KK_Spin` in to make a state. Add a Trigger parameter (for example `Spin`) and a transition into the new state on it, plus a transition back with **Has Exit Time** on.

**Use the clips on your own character**

1. Set your model's **Rig > Animation Type** to **Humanoid** and apply.
2. Make an Animator Controller, drag in the clips, and use the masks on layers that should move only part of the body.

**Root motion clips.** `_RM` means the clip contains root motion, the forward travel of the move. After you add a dash clip to your own controller, for the dash to move the character, tick **Apply Root Motion** on the Animator while it plays. With it off, the body can drift forward from the GameObject and snap back when the clip ends. If your own script moves the character, leave it off and move the character during the dash yourself.

**Monsters** use their own Generic controllers with the states `idle` and `walk`. Set the Bool `walk`.
