# Open Kit Phase 2: Theme-Adaptive 3D Kit for Unity (Proposal)

**Goal:** an original, royalty-free, low-poly 3D companion to the 2D Open Kit (1,001 PNGs: 431 `prop-`, 271 `token-`, 156 `tile-`, 143 `monster-`). Each asset is built once at a standard size in neutral colors, and a Unity script scales and recolors it to the room's theme. No purchases and no Polyfork, which was inspiration only.

## 1. Modeling approach

| Option | Cost / license | Verdict |
|---|---|---|
| **Blender + Python (`bpy`), procedural, run headless** | Free. Blender is GPL, but everything you make with it, including scripts and exported files, is yours ([Blender license](https://www.blender.org/about/license/), [FAQ](https://www.blender.org/support/faq/)) | **Primary** |
| Hand-modeling in Blender | Free | For one-off hero pieces only |
| Meshy (AI text/image to 3D) | Free plan output is **CC BY 4.0, so credit is required**. Paid plans start at $20/mo ([pricing](https://www.meshy.ai/en/pricing), [terms](https://www.meshy.ai/terms-of-use)). Needs an account. | ⚠ Flag: attribution, signup, and a paid upsell. Don't use. |
| Microsoft TRELLIS / TRELLIS.2 (local) | Code and models are MIT, but the mesh/GLB extraction and texture-baking steps use separately licensed parts that the maintainers say are not for commercial use ([issue #41](https://github.com/microsoft/TRELLIS/issues/41), [TRELLIS.2](https://github.com/microsoft/TRELLIS.2)). Needs a big GPU. | Not recommended |
| Tencent Hunyuan3D 2.x (local) | The license excludes the EU, UK, and South Korea, and that includes outputs ([license](https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE)) | ✗ Can't be sold worldwide |

**Pick: procedural Blender Python.** We own 100% of the output and it's reproducible (parameters in, mesh out). Shared primitives (bevelled boxes, cylinders, lathe profiles) keep the style consistent. It also suits Grok Build, which can write one script per asset and run `blender --background --python build_asset.py -- --asset prop-chair-simple` on the PC. AI meshes come out messy and hard to recolor by slot.

**Style:** flat-shaded low-poly, no textures, color only from material slots. Triangle budgets (our own targets, tune after M1): small props ≤800, large/environment ≤2,500, monsters ≤5,000.

## 2. Theme-adaptive system (Unity 6, URP)

**Material slots.** Every mesh uses at most five named materials: `Primary`, `Secondary`, `Accent`, `Metal`, `Emissive`. They are neutral grey in Blender and the names survive the FBX export.

**`ThemeProfile` (ScriptableObject)**, one per theme (Hell, Heaven, Crypt, Jungle, Dungeon, Undead…): a `palette` (a color per slot plus emissive intensity), optional per-slot `materialOverrides` (e.g. `Primary` becomes obsidian in Hell), and `inhabitantScale` (design values: halfling 0.75, human 1.0, giant 2.0).

**`ThemeRoom` (MonoBehaviour)** sits on a room root and holds a `ThemeProfile`.

**`ThemeAdaptive` (MonoBehaviour, `[ExecuteAlways]`)** goes on every asset prefab:
1. In `OnEnable`/`OnValidate`, it finds `GetComponentInParent<ThemeRoom>()` (or a global default).
2. **Color:** it swaps each slot to a cached shared material for that theme × slot (`ThemeMaterialCache`), so a scene has only a handful of materials and URP's SRP Batcher keeps working. Unity documents that `MaterialPropertyBlock` breaks SRP Batcher compatibility ([docs](https://docs.unity3d.com/ScriptReference/MaterialPropertyBlock.html), [SRP Batcher](https://docs.unity3d.com/Manual/SRPBatcher-Materials.html)). Use MPB only for rare per-instance tints. Unity 6's Renderer Shader User Value is a batch-friendly option for later ([RSUV](https://docs.unity3d.com/Manual/renderer-shader-user-value.html)).
3. **Scale:** `localScale = sizeClassBase × room.inhabitantScale` when `scalesWithRoom` is true.

**Size classes** (enum, match D&D-style footprints on a 1.5 m / 5 ft grid):

| Class | Footprint | Examples |
|---|---|---|
| Tiny | ≤0.5 cell | mushroom, candle |
| Small | 1 cell, short | crate, chair, giant rat |
| Medium | 1 cell | table, chest, human-size monster |
| Large | 2×2 | throne dais, golem |
| Huge | 3×3 | dragon, gate |

**Props vs monsters:**
- **Props** (furniture, doors, pews) usually have `scalesWithRoom = true`, so a chair shrinks in a halfling den and grows in a giant's cave.
- ~~**Structural pieces** (walls, floor tiles, pillars) never scale. They stay grid-locked and only recolor.~~ **Room-adapt rule (2026-09-28):** structural pieces scale with the room size class too and snap to the room grid (cell = 1.5 m × scale), so a giant's doorway is giant-sized.
- ~~**Monsters** never scale with the room. Their size comes from their own size class, and they recolor only through optional variant palettes (e.g. a "hell" construct).~~ **Room-adapt rule:** every asset, monsters included, must room-scale, re-theme at runtime and expose 3 working user colour slots (Primary, Secondary, Tertiary = Accent + Metal). Only a reasoned entry in `Blender/roomadapt_exceptions.json` can exempt an asset; both validators fail the build otherwise.

## 3. Export and import pipeline

- **Format:** **FBX is the primary format.** Unity imports it natively and it carries rigs and animation well. **GLB is secondary**, for other engines, web, and previews; Unity imports it through the free glTFast package ([glTFast](https://docs.unity3d.com/Packages/com.unity.cloud.gltfast@6.17/manual/installation.html)).
- **Conventions:**
  - 1 unit = 1 m, pivot at bottom-center (doors at the hinge), front faces Unity +Z, transforms applied.
  - Blender FBX settings: *Apply Scalings: FBX All*, forward −Y and up Z (the Blender side), then *Bake Axis Conversion* in Unity. That gives scale 1,1,1 and rotation 0 ([Blender FBX manual](https://docs.blender.org/manual/en/3.4/addons/import_export/scene_fbx.html), [walkthrough](https://polynook.com/learn/lesson/how-to-export-models-from-blender-to-unity)). An import `AssetPostprocessor` enforces this automatically.
- **Naming** matches the 2D kit exactly: `prop-chair-simple.fbx`, `monster-golem-stone.fbx`, `tile-dungeon-stone-floor.fbx`. Each prefab has the same name as its file. One proposed new prefix, `wall-`, covers modular walls (needs approval).
- **Project layout** (repo root, `OpenKit3D\`):
  ```
  Blender/        scripts/ (lib + one .py per asset), params/*.json, out/fbx, out/glb
  Assets/OpenKit3D/
    Models/{Props,Tiles,Walls,Monsters}/   Prefabs/{...}
    Materials/Slots/   Themes/*.asset   Scripts/{Runtime,Editor}/   Scenes/Demo/
  ```
- **Automation (run by Grok Build):** `Unity.exe -batchmode -projectPath … -executeMethod OpenKit.Editor.Build.ImportAll -quit` imports the FBX files, builds prefabs with `ThemeAdaptive` and colliders, and exports a `.unitypackage` via `AssetDatabase.ExportPackage`.
- **Licensing:** we author everything ourselves in Blender, so we own it outright. Ship under the same royalty-free license as the 2D kit. ~~If it goes on the Asset Store later, that store's EULA applies to sales there, and Unity takes a share of sales (check current terms).~~
  **Open Kit 3D is free forever under CC0 1.0 (see `LICENSE`). Paid work lives only in separate products, never in this project.**

## 4. First batch (22 items, taken from existing 2D names)

| # | Name | Class | Notes |
|---|---|---|---|
| 1 | prop-chair-simple | Small | new name |
| 2 | prop-table-wood | Medium | |
| 3 | prop-barrel | Small | |
| 4 | prop-crate | Small | |
| 5 | prop-chest | Small | reused by the mimic |
| 6 | prop-brazier | Small | Emissive slot |
| 7 | prop-torch-wall | Tiny | Emissive |
| 8 | prop-altar-stone | Medium | works as a hell or celestial altar |
| 9 | prop-pillar-stone | Medium | structural, no scaling |
| 10 | prop-fallen-pillar | Medium | |
| 11 | prop-throne-simple | Medium | |
| 12 | prop-pew-bench | Medium | |
| 13 | prop-coffin | Medium | |
| 14 | prop-sarcophagus | Medium | |
| 15 | prop-door-stone | Medium | hinge pivot |
| 16 | prop-mushroom | Tiny | jungle / faerie |
| 17 | prop-treasure-pile | Small | |
| 18 | tile-dungeon-stone-floor + wall-dungeon-stone | n/a | modular 1.5 m |
| 19 | monster-giant-rat | Small | simple skinned |
| 20 | monster-golem-stone | Large | rigid parts, no skinning |
| 21 | monster-construct-clockwork-hound | Medium | rigid parts |
| 22 | monster-mimic-chest | Medium | hinged-lid animation |

Most of these monsters animate with **rigid parts** (hinges and pivots), not skinning, which puts off the hard rigging work.

## 5. Milestones

- **M0, setup (needs approval):** confirm Blender is installed on the PC (free), pick the Unity 6 version and URP, create the project.
- **M1, proof:** a `bpy` helper library, 5 props (chair, table, barrel, brazier, pillar), the three scripts, and 3 themes. **Demo scene:** the same chair and table in a halfling den (0.75×, Dungeon), a human hall (1×, Heaven), and a giant's cave (2×, Hell). Deliver screenshots and a `.unitypackage`.
- **M2:** the rest of the batch, plus the floor/wall modules and 3 more themes (Crypt, Jungle, Undead).
- ~~**M3:** the rigid-part monsters with simple idle animations, plus a skinned test on the giant rat.~~ **M3 (done 2026-09-28):** was run as prop batch 2 instead: 22 new props, extended validation, hero scene, captures (see README).
- ~~**M4:** docs and packaging; decide on Asset Store readiness.~~
- ~~**M4 (planned, not started, do not build yet):** the monsters: the 4 rigid-part monsters (section 4 names three: monster-golem-stone, monster-construct-clockwork-hound, monster-mimic-chest; the fourth is still to be chosen) with simple idle animations, the skinned monster-giant-rat test, and the M3 follow-ups below.~~ **M4 (done 2026-09-29):** 5 monsters with idle and walk clips (rigid golem, clockwork hound, mimic, skeleton warrior, and the skinned giant rat), all room-adapt with 0 exceptions, plus the follow-ups below. Package `Builds/OpenKit3D-M4.unitypackage`, 47 assets (M1 5, M2 15, M3 22, M4 5). See README.
  - ~~**4th rigid monster: a skeleton warrior** (`monster-skeleton-warrior`), alongside monster-golem-stone, monster-construct-clockwork-hound and monster-mimic-chest.~~ **Done (2026-09-29):** Medium, rigid parts, shield on the left forearm, sword in the right hand, helmet; 2,076 / 5,000 tris, 18 bones; idle 64 f, walk 32 f.
  - ~~**All monsters must follow the room-adapt rule**: room-scale (halfling / human / giant), re-theme at runtime, and expose 3 working user colour slots (checked by both validators, including the Unity render check).~~ **Done (2026-09-29):** all 5 have `SCALES_WITH_ROOM` True, Primary / Secondary / Tertiary (Accent + Metal) user slots, and Emissive eyes/core (`EMISSIVE_SCALE` 0.6-0.7). Passed with 0 exceptions (skinned render check included: rat Tertiary 55 px, threshold 6; all 47 OK).
  - ~~**Sack rework**: a better prop-sack-grain silhouette.~~ **Done (2026-09-29):** standing sack is a squat, slumped, leaning pear with a gathered neck, tie cord, floppy 4-flap tuft and a Secondary patch; lying sack is a plump pillow with a tied flared end. 412 to 526 tris.
  - ~~**Readability pass from the M3 QA look**: the axe blade is buried in the stump (prop-stump-axe), silhouettes are dark in the giant smithy, contrast is low in the village yard, and wall mortar glows near the torches.~~ **Done (2026-09-29):** stump axe head 40% larger and lifted so only the cutting edge bites ~2.5 cm into the cut face, dark split in the cut face (168 to 196 tris). Hell Primary obsidian (0.10,0.08,0.09, smooth 0.7) to (0.25,0.20,0.21, smooth 0.22) and Metal (0.22,0.18,0.17) to (0.48,0.42,0.39) (mortar glints near the torches removed, dark silhouettes lifted). Giant smithy warm front fill (intensity 7) and ember rim light (intensity 10), outside `ThemeRoom.roomLights`. Wall torch light intensity 1.6 to 1.25. Heaven Secondary sky stone (0.66,0.76,0.92) to (0.46,0.56,0.78) and Primary marble (0.93,0.92,0.88, smooth 0.55) to (0.88,0.86,0.80, smooth 0.45) for yard contrast.
  - ~~Cap on the prop-lantern glow~~ **Done (room-adapt pass):** per-prop `EMISSIVE_SCALE` caps emissive and light intensity (lantern 0.45, cauldron 0.4).
- **Later:** docs and packaging. There is no Asset Store release: Open Kit 3D stays free under CC0.

**Owner approval needed:** Blender install on the PC (free); Unity version and render pipeline; the 1.5 m grid and scale values; the `wall-` prefix; the batch list; the license text; whether any AI mesh tools are allowed (recommended: no); Grok Build running scripts on the PC.

## 6. Risks and open questions

- **Rigging and animation:** skinned monsters are the biggest time sink. Mixamo is free but needs an Adobe account, only auto-rigs humanoids, and **forbids redistributing its raw animation files**, which is a problem for an asset kit ([Mixamo FAQ](https://helpx.adobe.com/si/creative-cloud/faq/mixamo-faq.html), [licensing thread](https://community.adobe.com/questions-696/mixamo-faq-licensing-royalties-ownership-eula-and-tos-589400); verify before relying on it). ⚠ Avoid it. Prefer rigid-part animation made in Blender or Unity, or our own simple rigs.
- **Style consistency:** shared helper library, fixed bevel size, palette-only rule, and a turntable render per asset for review.
- **Procedural limits:** organic shapes (plants, dragons, beasts) are harder to build from code. These may need hand-sculpting, or they wait for a later phase.
- **Time budget:** unknown until M1. Use M1's hours per asset to estimate the rest before committing to M2.
- **Unity licensing:** Unity Personal is free only up to Unity's revenue threshold (check current terms).
