using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.Universal;
using UnityEngine.SceneManagement;

namespace OpenKit.Editor
{
    /// <summary>Batchmode entry points.
    ///   Unity.exe -batchmode -projectPath . -executeMethod OpenKit.Editor.Build.ImportAll -quit
    ///   Unity.exe -batchmode -projectPath . -executeMethod OpenKit.Editor.Build.RenderScreenshots -quit
    ///   Unity.exe -batchmode -projectPath . -executeMethod OpenKit.Editor.Build.All -quit
    /// </summary>
    public static class Build
    {
        const string Root = "Assets/OpenKit3D";
        const string ModelsProps = Root + "/Models/Props";
        const string PrefabsProps = Root + "/Prefabs/Props";
        const string SlotsDir = Root + "/Materials/Slots";
        const string ThemesDir = Root + "/Themes";
        const string DemoDir = Root + "/Scenes/Demo";
        const string DemoScene = DemoDir + "/OpenKit3D-Demo.unity";
        const string LineupScene = DemoDir + "/OpenKit3D-Lineup.unity";
        const string ModularScene = DemoDir + "/OpenKit3D-Modular.unity";
        const string CatalogScene = DemoDir + "/OpenKit3D-Catalog.unity";
        const string HeroScene = DemoDir + "/OpenKit3D-M3Hero.unity";
        const string Milestone = "M4";
        static readonly string[] Categories = { "Props", "Tiles", "Walls", "Monsters" };

        static string Cat(ManifestEntry a) => string.IsNullOrEmpty(a.category) ? "Props" : a.category;
        static string ModelPath(ManifestEntry a) => $"{Root}/Models/{Cat(a)}/{a.name}.fbx";
        static string PrefabPath(ManifestEntry a) => $"{Root}/Prefabs/{Cat(a)}/{a.name}.prefab";

        static string ProjectRoot => Directory.GetParent(Application.dataPath).FullName;
        static string BlenderOut => Path.Combine(ProjectRoot, "Blender", "out");

        [Serializable] class ManifestEntry { public string name; public int tris; public int budget; public string sizeClass; public bool scalesWithRoom; public string category; public float[] lightSocket; public float[] dims_m; public string pivot; public string milestone; public string roomScale; public float emissiveScale; public string[] user_slots; public bool rigged; public int bones; public string[] clips; }
        [Serializable] class Manifest { public ManifestEntry[] assets; }

        // ------------------------------------------------------------------ entry points
        [MenuItem("Open Kit 3D/Build: Import All (prefabs + demo + package)")]
        public static void ImportAll() => Run(() => { DoImportAll(); });

        [MenuItem("Open Kit 3D/Build: Render Screenshots")]
        public static void RenderScreenshots() => Run(DoScreenshots);

        public static void All() => Run(() => { DoImportAll(); DoScreenshots(); });

        [MenuItem("Open Kit 3D/Build: Validate")]
        public static void Validate() => Run(() => ValidateAssets(LoadManifest()));

        [MenuItem("Open Kit 3D/Build: M3 Captures (contact sheets + hero shots)")]
        public static void CaptureM3() => Run(() => DoM3Captures(LoadManifest()));

        [MenuItem("Open Kit 3D/Build: M4 Captures (monsters + before/after)")]
        public static void CaptureM4() => Run(() => DoM4Captures(LoadManifest()));

        /// <summary>Before/after shots only; the tag comes from the OKIT_CAPTURE_TAG environment variable (default "after").</summary>
        public static void CaptureM4Compare() => Run(() => DoM4Compare(Environment.GetEnvironmentVariable("OKIT_CAPTURE_TAG") is string t && t.Length > 0 ? t : "after"));

        static void Run(Action a)
        {
            try { a(); Debug.Log("[OpenKit] BUILD OK"); }
            catch (Exception e)
            {
                Debug.LogError("[OpenKit] BUILD FAILED: " + e);
                if (Application.isBatchMode) EditorApplication.Exit(1);
            }
        }

        static void DoImportAll()
        {
            var sw = System.Diagnostics.Stopwatch.StartNew();
            foreach (var d in new[] { ModelsProps, PrefabsProps, SlotsDir, ThemesDir, DemoDir, Root + "/Models/Tiles", Root + "/Models/Walls", Root + "/Models/Monsters", Root + "/Prefabs/Tiles", Root + "/Prefabs/Walls", Root + "/Prefabs/Monsters" })
                Directory.CreateDirectory(Path.Combine(ProjectRoot, d));
            AssetDatabase.Refresh();

            var slotMats = EnsureSlotMaterials();
            var manifest = LoadManifest();
            CopyModels(manifest);
            VerifyRemaps(manifest, slotMats);
            var themes = EnsureThemes();
            var prefabs = BuildPrefabs(manifest);
            ValidateAssets(manifest);
            BuildDemoScene(themes, prefabs);
            BuildLineupScene(themes, prefabs);
            BuildModularScene(themes, prefabs);
            BuildCatalogScene(themes, prefabs, manifest);
            BuildHeroScene(themes, prefabs);
            BuildMonsterScene(themes, prefabs);
            EditorBuildSettings.scenes = new[] { DemoScene, LineupScene, ModularScene, CatalogScene, HeroScene, MonsterScene }.Select(x => new EditorBuildSettingsScene(x, true)).ToArray();
            ExportPackage();
            Debug.Log($"[OpenKit] ImportAll finished in {sw.Elapsed.TotalSeconds:F1}s");
        }

        // ------------------------------------------------------------------ materials
        static Dictionary<string, Material> EnsureSlotMaterials()
        {
            var shader = Shader.Find(ThemeMaterialCache.LitShader) ?? throw new Exception("URP Lit shader not found - is URP the active pipeline?");
            var neutral = ScriptableObject.CreateInstance<ThemeProfile>();
            neutral.themeName = "Neutral"; neutral.emissiveIntensity = 1.5f;
            var dict = new Dictionary<string, Material>();
            for (int i = 0; i < OpenKitConst.SlotCount; i++)
            {
                string n = OpenKitConst.SlotNames[i];
                string p = $"{SlotsDir}/{n}.mat";
                var m = AssetDatabase.LoadAssetAtPath<Material>(p);
                if (!m) { m = new Material(shader) { name = n }; AssetDatabase.CreateAsset(m, p); }
                ThemeMaterialCache.Apply(m, neutral, (ThemeSlot)i);
                EditorUtility.SetDirty(m);
                dict[n] = m;
            }
            UnityEngine.Object.DestroyImmediate(neutral);
            AssetDatabase.SaveAssets();
            return dict;
        }

        static Manifest LoadManifest()
        {
            string p = Path.Combine(BlenderOut, "manifest_unity.json");
            if (!File.Exists(p)) throw new FileNotFoundException("Run the Blender build first", p);
            var m = JsonUtility.FromJson<Manifest>(File.ReadAllText(p));
            Debug.Log($"[OpenKit] manifest: {string.Join(", ", m.assets.Select(a => a.name + " (" + a.tris + " tris)"))}");
            return m;
        }

        static void CopyModels(Manifest m)
        {
            foreach (var a in m.assets)
            {
                string src = Path.Combine(BlenderOut, "fbx", a.name + ".fbx");
                string dst = Path.Combine(ProjectRoot, ModelPath(a));
                File.Copy(src, dst, true);
            }
            AssetDatabase.Refresh(ImportAssetOptions.ForceSynchronousImport);
            foreach (var a in m.assets)
                AssetDatabase.ImportAsset(ModelPath(a), ImportAssetOptions.ForceUpdate | ImportAssetOptions.ForceSynchronousImport);
        }

        static bool s_DoorExtendsPlusX = true;

        static void VerifyRemaps(Manifest m, Dictionary<string, Material> slotMats)
        {
            foreach (var a in m.assets)
            {
                string p = ModelPath(a);
                var go = AssetDatabase.LoadAssetAtPath<GameObject>(p);
                var mats = go.GetComponentsInChildren<Renderer>().SelectMany(r => r.sharedMaterials).ToArray();
                bool ok = mats.All(x => x && slotMats.ContainsValue(x));
                if (!ok)
                {
                    var mi = (ModelImporter)AssetImporter.GetAtPath(p);
                    foreach (var kv in slotMats) mi.AddRemap(new AssetImporter.SourceAssetIdentifier(typeof(Material), kv.Key), kv.Value);
                    mi.SaveAndReimport();
                    go = AssetDatabase.LoadAssetAtPath<GameObject>(p);
                    mats = go.GetComponentsInChildren<Renderer>().SelectMany(r => r.sharedMaterials).ToArray();
                }
                var vmesh = MeshOf(go);
                int tris = 0; if (vmesh) for (int si = 0; si < vmesh.subMeshCount; si++) tris += (int)vmesh.GetIndexCount(si) / 3;
                Debug.Log($"[OpenKit] {a.name}: rot={go.transform.localEulerAngles} scale={go.transform.localScale} bounds={(vmesh ? vmesh.bounds.ToString() : "none")} tris={tris} rigged={a.rigged} mats=[{string.Join(",", mats.Select(x => x ? x.name : "null"))}]");
            }
            // orientation check: chair backrest must be at -Z so the front faces +Z
            var chair = AssetDatabase.LoadAssetAtPath<GameObject>($"{ModelsProps}/prop-chair-simple.fbx");
            if (chair)
            {
                var mesh = chair.GetComponentInChildren<MeshFilter>().sharedMesh;
                // backrest top rail = the highest part of the chair: compare bounds centre of the top slice via the collider-free approach
                float z = 0;
                try
                {
                    var tmp = UnityEngine.Object.Instantiate(mesh);
                    var verts = tmp.vertices; UnityEngine.Object.DestroyImmediate(tmp);
                    var top = verts.Where(v => v.y > 0.85f).ToArray();
                    z = top.Length > 0 ? top.Average(v => v.z) : 0;
                }
                catch (Exception e) { Debug.LogWarning("[OpenKit] orientation check skipped: " + e.Message); }
                var door = m.assets.FirstOrDefault(x => x.name == "prop-door-stone");
                if (door != null)
                {
                    var dgo = AssetDatabase.LoadAssetAtPath<GameObject>(ModelPath(door));
                    var db = dgo.GetComponentInChildren<MeshFilter>().sharedMesh.bounds;
                    s_DoorExtendsPlusX = db.center.x > 0;
                    Debug.Log($"[OpenKit] ORIENTATION door bounds {db} -> leaf extends {(s_DoorExtendsPlusX ? "+X" : "-X")} from the hinge");
                }
                Debug.Log($"[OpenKit] ORIENTATION chair backrest avg z = {z:F3} -> front faces {(z < 0 ? "+Z (OK)" : "-Z (WRONG)")}");
            }
        }

        // ------------------------------------------------------------------ themes
        static ThemeProfile.SlotLook L(float r, float g, float b, float metal = 0, float smooth = 0.2f)
            => new ThemeProfile.SlotLook { color = new Color(r, g, b), metallic = metal, smoothness = smooth };

        static List<ThemeProfile> EnsureThemes()
        {
            var list = new List<ThemeProfile>
            {
                MakeTheme("Dungeon", 0.75f, 1.6f, new Color(1f, 0.78f, 0.55f), new[] {
                    L(0.42f, 0.27f, 0.15f, 0, 0.15f),   // Primary: worn oak
                    L(0.36f, 0.37f, 0.33f, 0, 0.10f),   // Secondary: mossy stone
                    L(0.60f, 0.47f, 0.22f, 0, 0.35f),   // Accent: brass / straw
                    L(0.33f, 0.31f, 0.30f, 1, 0.45f),   // Metal: iron
                    L(1.00f, 0.55f, 0.16f, 0, 0.5f) }), // Emissive: torch fire
                MakeTheme("Heaven", 1.0f, 1.4f, new Color(0.85f, 0.92f, 1f), new[] {
                    L(0.88f, 0.86f, 0.80f, 0, 0.45f),   // Primary: white marble (M4: a touch warmer / less glare)
                    L(0.46f, 0.56f, 0.78f, 0, 0.30f),   // Secondary: sky stone (M4: deeper, for yard contrast against the marble)
                    L(1.00f, 0.82f, 0.38f, 0, 0.5f),    // Accent: gilt
                    L(0.95f, 0.78f, 0.36f, 1, 0.75f),   // Metal: gold
                    L(0.75f, 0.92f, 1.00f, 0, 0.5f) }), // Emissive: holy light
                MakeTheme("Hell", 2.0f, 2.2f, new Color(1f, 0.45f, 0.3f), new[] {
                    L(0.25f, 0.20f, 0.21f, 0, 0.22f),   // Primary: obsidian (M4: lighter + much rougher - silhouettes read, no mortar glints)
                    L(0.35f, 0.09f, 0.07f, 0, 0.15f),   // Secondary: blood basalt
                    L(0.85f, 0.30f, 0.08f, 0, 0.4f),    // Accent: ember
                    L(0.48f, 0.42f, 0.39f, 1, 0.35f),   // Metal: blackened iron (M4: lighter so iron props read on obsidian)
                    L(1.00f, 0.32f, 0.05f, 0, 0.5f) }), // Emissive: lava
                // M2 themes. Scales stay inside the approved set (halfling 0.75 / human 1.0 / giant 2.0):
                //   Crypt 1.0 - human-built tombs, human-size dead;  Jungle 0.75 - small folk (goblins, kobolds, grippli, faerie);
                //   Undead 2.0 - bone-giant ossuary / giant undead lords.
                MakeTheme("Crypt", 1.0f, 1.4f, new Color(0.75f, 0.82f, 1f), new[] {
                    L(0.55f, 0.55f, 0.58f, 0, 0.25f),   // Primary: cold granite
                    L(0.27f, 0.28f, 0.31f, 0, 0.15f),   // Secondary: slate
                    L(0.47f, 0.40f, 0.24f, 0, 0.35f),   // Accent: tarnished bronze
                    L(0.42f, 0.42f, 0.44f, 1, 0.4f),    // Metal: dull iron
                    L(1.00f, 0.84f, 0.55f, 0, 0.5f) }), // Emissive: candle
                MakeTheme("Jungle", 0.75f, 1.8f, new Color(0.8f, 1f, 0.75f), new[] {
                    L(0.36f, 0.28f, 0.14f, 0, 0.15f),   // Primary: dark hardwood
                    L(0.30f, 0.42f, 0.22f, 0, 0.12f),   // Secondary: mossy stone
                    L(0.86f, 0.32f, 0.14f, 0, 0.35f),   // Accent: flower red
                    L(0.33f, 0.55f, 0.45f, 0.8f, 0.45f),// Metal: verdigris bronze
                    L(0.30f, 1.00f, 0.72f, 0, 0.5f) }), // Emissive: bioluminescence
                MakeTheme("Undead", 2.0f, 2.0f, new Color(0.7f, 1f, 0.72f), new[] {
                    L(0.82f, 0.78f, 0.66f, 0, 0.3f),    // Primary: bone
                    L(0.25f, 0.22f, 0.28f, 0, 0.12f),   // Secondary: grave stone
                    L(0.42f, 0.52f, 0.26f, 0, 0.25f),   // Accent: rot green
                    L(0.42f, 0.29f, 0.20f, 0.7f, 0.3f), // Metal: rusted iron
                    L(0.45f, 1.00f, 0.35f, 0, 0.5f) }), // Emissive: necrotic glow
            };
            AssetDatabase.SaveAssets();
            return list;
        }

        static ThemeProfile MakeTheme(string name, float scale, float emissive, Color lightTint, ThemeProfile.SlotLook[] pal)
        {
            string p = $"{ThemesDir}/{name}.asset";
            var t = AssetDatabase.LoadAssetAtPath<ThemeProfile>(p);
            if (!t) { t = ScriptableObject.CreateInstance<ThemeProfile>(); AssetDatabase.CreateAsset(t, p); }
            t.themeName = name; t.inhabitantScale = scale; t.emissiveIntensity = emissive; t.palette = pal; t.lightTint = lightTint;
            // bake one persistent material per slot as sub-assets of the theme (saved scenes keep real references)
            var subs = AssetDatabase.LoadAllAssetsAtPath(p).OfType<Material>().ToList();
            var shader = Shader.Find(ThemeMaterialCache.LitShader);
            t.bakedMaterials = new Material[OpenKitConst.SlotCount];
            for (int i = 0; i < OpenKitConst.SlotCount; i++)
            {
                string mn = $"OK_{name}_{OpenKitConst.SlotNames[i]}";
                var m = subs.FirstOrDefault(x => x.name == mn);
                if (!m) { m = new Material(shader) { name = mn }; AssetDatabase.AddObjectToAsset(m, t); }
                ThemeMaterialCache.Apply(m, t, (ThemeSlot)i);
                EditorUtility.SetDirty(m);
                t.bakedMaterials[i] = m;
            }
            EditorUtility.SetDirty(t);
            return t;
        }

        // ------------------------------------------------------------------ prefabs
        static Dictionary<string, GameObject> BuildPrefabs(Manifest m)
        {
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var result = new Dictionary<string, GameObject>();
            foreach (var a in m.assets)
            {
                var model = AssetDatabase.LoadAssetAtPath<GameObject>(ModelPath(a));
                var inst = (GameObject)PrefabUtility.InstantiatePrefab(model);
                inst.name = a.name;
                inst.transform.SetPositionAndRotation(Vector3.zero, Quaternion.identity);
                // collider fitted to the render bounds
                var b = new Bounds(Vector3.zero, Vector3.zero); bool first = true;
                foreach (var r in inst.GetComponentsInChildren<Renderer>()) { if (first) { b = r.bounds; first = false; } else b.Encapsulate(r.bounds); }
                var bc = inst.AddComponent<BoxCollider>(); bc.center = b.center; bc.size = b.size;
                var lights = new List<Light>();
                if (a.lightSocket != null && a.lightSocket.Length == 3)
                {
                    var lg = new GameObject("FlameLight");
                    lg.transform.SetParent(inst.transform, false);
                    // Blender (x, y, z) -> Unity (-x, z, -y) given the 180-degree FBX spin (front -Y -> +Z); verified by the door/chair orientation logs
                    lg.transform.localPosition = new Vector3(-a.lightSocket[0], a.lightSocket[2], -a.lightSocket[1]);
                    var l = lg.AddComponent<Light>();
                    bool big = a.name.Contains("brazier") || a.name == "prop-torch-standing";
                    l.type = LightType.Point; l.range = big ? 5f : 3.5f; l.intensity = big ? 2.5f : 1.25f; l.shadows = big ? LightShadows.Soft : LightShadows.None;   // M4: wall torches 1.6 -> 1.25 (less hot-spot on nearby mortar)
                    l.color = Color.white;
                    lights.Add(l);
                }
                var ta = inst.AddComponent<ThemeAdaptive>();
                ta.sizeClass = (SizeClass)Enum.Parse(typeof(SizeClass), a.sizeClass);
                ta.scalesWithRoom = a.scalesWithRoom;
                ta.emissiveLights = lights.ToArray();
                ta.snapsToRoomGrid = a.roomScale == "grid";
                ta.emissiveScale = a.emissiveScale > 0f ? Mathf.Clamp(a.emissiveScale, 0.05f, 1f) : 1f;
                ta.RebuildSlotMap();
                if (a.rigged)
                {
                    var anim = inst.GetComponent<Animator>() ?? inst.AddComponent<Animator>();
                    anim.applyRootMotion = false;
                    anim.cullingMode = AnimatorCullingMode.CullUpdateTransforms;
                    anim.runtimeAnimatorController = EnsureController(a);
                }
                if (a.roomScale == "grid") GameObjectUtility.SetStaticEditorFlags(inst, StaticEditorFlags.BatchingStatic | StaticEditorFlags.OccluderStatic | StaticEditorFlags.OccludeeStatic);
                string path = PrefabPath(a);
                var prefab = PrefabUtility.SaveAsPrefabAsset(inst, path);
                UnityEngine.Object.DestroyImmediate(inst);
                result[a.name] = prefab;
                Debug.Log($"[OpenKit] prefab {path} sizeClass={ta.sizeClass} scalesWithRoom={ta.scalesWithRoom} grid={ta.snapsToRoomGrid} emissiveScale={ta.emissiveScale} collider={b.size}");
            }
            AssetDatabase.SaveAssets();
            return result;
        }

        // ------------------------------------------------------------------ demo scene
        struct RoomDef { public string label; public int cells; }

        static void SetupEnvironment(string profileName)
        {
            RenderSettings.skybox = null;
            RenderSettings.ambientMode = AmbientMode.Trilight;
            RenderSettings.ambientSkyColor = new Color(0.32f, 0.34f, 0.40f);
            RenderSettings.ambientEquatorColor = new Color(0.20f, 0.20f, 0.22f);
            RenderSettings.ambientGroundColor = new Color(0.10f, 0.09f, 0.09f);
            var sun = new GameObject("Sun").AddComponent<Light>();
            sun.type = LightType.Directional; sun.intensity = 0.9f; sun.shadows = LightShadows.Soft;
            sun.color = new Color(1f, 0.97f, 0.92f);
            sun.transform.rotation = Quaternion.Euler(52f, -35f, 0f);

            string vp = $"{DemoDir}/{profileName}.asset";
            var prof = AssetDatabase.LoadAssetAtPath<VolumeProfile>(vp);
            if (!prof)
            {
                prof = ScriptableObject.CreateInstance<VolumeProfile>();
                AssetDatabase.CreateAsset(prof, vp);
                var bloom = prof.Add<Bloom>(true); bloom.intensity.Override(0.9f); bloom.threshold.Override(1.0f); bloom.scatter.Override(0.6f);
                var tm = prof.Add<Tonemapping>(true); tm.mode.Override(TonemappingMode.Neutral);
                foreach (var c in prof.components) AssetDatabase.AddObjectToAsset(c, prof);
                AssetDatabase.SaveAssets();
            }
            var vol = new GameObject("PostFX").AddComponent<Volume>();
            vol.isGlobal = true; vol.sharedProfile = prof;
        }

        static Camera MakeCamera(string name, Vector3 pos, Vector3 look, float fov, bool main)
        {
            var go = new GameObject(name);
            var cam = go.AddComponent<Camera>();
            go.transform.position = pos; go.transform.LookAt(look);
            cam.fieldOfView = fov; cam.nearClipPlane = 0.1f; cam.farClipPlane = 300f;
            cam.clearFlags = CameraClearFlags.SolidColor; cam.backgroundColor = new Color(0.05f, 0.05f, 0.07f);
            var data = cam.GetUniversalAdditionalCameraData();
            data.renderPostProcessing = true;
            data.antialiasing = AntialiasingMode.SubpixelMorphologicalAntiAliasing;
            if (main) { go.tag = "MainCamera"; go.AddComponent<AudioListener>(); }
            else cam.enabled = false;
            return cam;
        }

        static GameObject Cube(string name, Transform parent, Vector3 pos, Vector3 size, Material mat, bool collider = true)
        {
            var c = GameObject.CreatePrimitive(PrimitiveType.Cube);
            c.name = name; c.transform.SetParent(parent, false);
            c.transform.localPosition = pos; c.transform.localScale = size;
            c.GetComponent<Renderer>().sharedMaterial = mat;
            if (!collider) UnityEngine.Object.DestroyImmediate(c.GetComponent<Collider>());
            return c;
        }

        static GameObject Place(GameObject prefab, Transform parent, Vector3 localPos, float yRot)
        {
            var g = (GameObject)PrefabUtility.InstantiatePrefab(prefab, parent);
            g.transform.localPosition = localPos;
            g.transform.localRotation = Quaternion.Euler(0, yRot, 0);
            return g;
        }

        static Material InhabitantMat()
        {
            string p = $"{DemoDir}/InhabitantRef.mat";
            var m = AssetDatabase.LoadAssetAtPath<Material>(p);
            if (!m) { m = new Material(Shader.Find(ThemeMaterialCache.LitShader)) { name = "InhabitantRef" }; AssetDatabase.CreateAsset(m, p); }
            m.SetColor("_BaseColor", new Color(0.35f, 0.75f, 0.85f)); m.SetFloat("_Smoothness", 0.3f);
            EditorUtility.SetDirty(m);
            return m;
        }

        static void BuildDemoScene(List<ThemeProfile> themes, Dictionary<string, GameObject> P)
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            var slotPrimary = AssetDatabase.LoadAssetAtPath<Material>($"{SlotsDir}/Primary.mat");
            var slotSecondary = AssetDatabase.LoadAssetAtPath<Material>($"{SlotsDir}/Secondary.mat");
            var inhabitant = InhabitantMat();
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");

            var defs = new[] {
                new RoomDef { label = "Halfling den  -  Dungeon  -  inhabitant 0.75x", cells = 4 },
                new RoomDef { label = "Human hall  -  Heaven  -  inhabitant 1.0x", cells = 5 },
                new RoomDef { label = "Giant's cave  -  Hell  -  inhabitant 2.0x", cells = 7 },
            };
            float cell = OpenKitConst.GridCell, gap = 3f, x = 0f;
            var rooms = new List<(ThemeRoom room, float size)>();
            for (int i = 0; i < 3; i++)
            {
                var t = themes[i]; float s = t.inhabitantScale; int n = defs[i].cells; float L = n * cell, h = L / 2f;
                x += (i == 0 ? 0 : gap) + h;
                var root = new GameObject($"Room_{t.themeName}");
                root.transform.position = new Vector3(x, 0, 0);
                x += h;

                // floor: one tile per 1.5 m cell over a grout slab (structural: recolour only)
                var floor = new GameObject("Floor"); floor.transform.SetParent(root.transform, false);
                Cube("Grout", floor.transform, new Vector3(0, -0.08f, 0), new Vector3(L, 0.1f, L), slotSecondary);
                for (int cx = 0; cx < n; cx++)
                    for (int cz = 0; cz < n; cz++)
                        Cube($"Tile_{cx}_{cz}", floor.transform, new Vector3(-h + cell * (cx + 0.5f), -0.05f, -h + cell * (cz + 0.5f)), new Vector3(cell - 0.04f, 0.1f, cell - 0.04f), slotPrimary, false);
                var fa = floor.AddComponent<ThemeAdaptive>(); fa.scalesWithRoom = false; fa.sizeClass = SizeClass.Huge; fa.RebuildSlotMap();

                var walls = new GameObject("Walls"); walls.transform.SetParent(root.transform, false);
                float wh = Mathf.Max(4.5f, 3f * s + 0.5f);   // pillars now scale with the room
                Cube("Wall_Back", walls.transform, new Vector3(-0.15f, wh / 2, h + 0.15f), new Vector3(L + 0.3f, wh, 0.3f), slotSecondary);
                Cube("Wall_Left", walls.transform, new Vector3(-h - 0.15f, wh / 2, 0), new Vector3(0.3f, wh, L), slotSecondary);
                var wa = walls.AddComponent<ThemeAdaptive>(); wa.scalesWithRoom = false; wa.sizeClass = SizeClass.Huge; wa.RebuildSlotMap();

                // the SAME prefabs in every room; layout offsets scale with the inhabitants
                var props = new GameObject("Props"); props.transform.SetParent(root.transform, false);
                Place(P["prop-table-wood"], props.transform, new Vector3(-0.2f * s, 0, 0), 0);
                Place(P["prop-chair-simple"], props.transform, new Vector3(-0.45f * s, 0, -0.62f * s), 0);
                Place(P["prop-chair-simple"], props.transform, new Vector3(0.05f * s, 0, 0.62f * s), 180);
                Place(P["prop-chair-simple"], props.transform, new Vector3(0.75f * s, 0, -0.05f * s), -90);
                Place(P["prop-barrel"], props.transform, new Vector3(-h + 0.45f * s, 0, -0.35f * s), 0);
                Place(P["prop-barrel"], props.transform, new Vector3(-h + 0.45f * s, 0, 0.35f * s), 30);
                Place(P["prop-brazier"], props.transform, new Vector3(1.6f * s, 0, 1.2f * s), 0);
                // structural: grid-locked cell centres, never scaled
                Place(P["prop-pillar-stone"], props.transform, new Vector3(-h + cell * 0.5f, 0, h - cell * 0.5f), 0);
                Place(P["prop-pillar-stone"], props.transform, new Vector3(h - cell * 0.5f, 0, h - cell * 0.5f), 0);

                // inhabitant reference (1.8 m human x scale) - scene-only, not themed
                var inh = GameObject.CreatePrimitive(PrimitiveType.Capsule);
                inh.name = $"InhabitantRef_{1.8f * s:F2}m"; inh.transform.SetParent(root.transform, false);
                inh.transform.localScale = new Vector3(0.36f * s, 0.9f * s, 0.36f * s);
                inh.transform.localPosition = new Vector3(-1.55f * s, 0.9f * s, -1.35f * s);
                inh.GetComponent<Renderer>().sharedMaterial = inhabitant;

                // room fill light tinted by the theme
                var fill = new GameObject("RoomFill").AddComponent<Light>();
                fill.transform.SetParent(root.transform, false);
                fill.transform.localPosition = new Vector3(0.5f, 3.8f, -h * 0.4f);
                fill.type = LightType.Point; fill.range = L * 1.4f; fill.intensity = 2.2f; fill.shadows = LightShadows.None;

                // label on the back wall
                var lab = new GameObject("Label"); lab.transform.SetParent(root.transform, false);
                lab.transform.localPosition = new Vector3(0, wh - 0.35f, h - 0.02f);
                var tm = lab.AddComponent<TextMesh>();
                tm.text = defs[i].label; tm.font = font; tm.fontSize = 64; tm.characterSize = 0.035f * (L / 6f);
                tm.anchor = TextAnchor.MiddleCenter; tm.color = new Color(1, 1, 1, 0.9f);
                lab.GetComponent<MeshRenderer>().sharedMaterial = font.material;

                var room = root.AddComponent<ThemeRoom>();
                room.profile = t; room.roomLights = new[] { fill };
                room.Apply();
                rooms.Add((room, L));

                // per-room camera (front-right 3/4 view)
                var c = root.transform.position;
                MakeCamera($"Cam_{t.themeName}", c + new Vector3(0.5f * L, 0.5f * L + 0.8f, -0.9f * L), c + new Vector3(-0.08f * L, 0.35f * s + 0.25f, 0.0f), 44f, false);
            }
            float span = x;
            MakeCamera("Cam_Overview", new Vector3(span * 0.5f, span * 0.55f, -span * 0.95f), new Vector3(span * 0.5f, 0.2f, 0.8f), 36f, true);

            EditorSceneManager.SaveScene(scene, DemoScene);
            Debug.Log("[OpenKit] saved " + DemoScene);
        }

        static void BuildLineupScene(List<ThemeProfile> themes, Dictionary<string, GameObject> P)
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            var gm = AssetDatabase.LoadAssetAtPath<Material>($"{DemoDir}/LineupGround.mat");
            if (!gm) { gm = new Material(Shader.Find(ThemeMaterialCache.LitShader)) { name = "LineupGround" }; AssetDatabase.CreateAsset(gm, $"{DemoDir}/LineupGround.mat"); }
            gm.SetColor("_BaseColor", new Color(0.16f, 0.16f, 0.18f)); gm.SetFloat("_Smoothness", 0.1f); EditorUtility.SetDirty(gm);
            Cube("Ground", null, new Vector3(0, -0.05f, 4f), new Vector3(60f, 0.1f, 40f), gm);
            string[] order = { "prop-chair-simple", "prop-table-wood", "prop-barrel", "prop-brazier" };
            float[] rowZ = { 0f, 3.4f, 8.0f };
            for (int i = 0; i < 3; i++)
            {
                var t = themes[i]; float s = t.inhabitantScale;
                var row = new GameObject($"Row_{t.themeName}"); row.transform.position = new Vector3(0, 0, rowZ[i]);
                float step = 2.0f * s, x0 = -4.2f;
                for (int k = 0; k < order.Length; k++)
                    Place(P[order[k]], row.transform, new Vector3(x0 + k * step, 0, 0), order[k] == "prop-chair-simple" ? -30 : 0);
                // structural pillar: same 3 m in every row (never scales)
                Place(P["prop-pillar-stone"], row.transform, new Vector3(-7.2f - 1.4f * i, 0, 0), 0);
                var room = row.AddComponent<ThemeRoom>(); room.profile = t; room.Apply();
            }
            MakeCamera("Cam_Lineup", new Vector3(-0.5f, 8.5f, -12.5f), new Vector3(-0.5f, 1.0f, 4.2f), 42f, true);
            EditorSceneManager.SaveScene(scene, LineupScene);
            Debug.Log("[OpenKit] saved " + LineupScene);
        }

        // ------------------------------------------------------------------ M2: modular rooms (tile + wall pieces)
        struct Item { public string name; public float x, z, rot; public bool abs; public Item(string n, float x, float z, float rot = 0, bool abs = false) { name = n; this.x = x; this.z = z; this.rot = rot; this.abs = abs; } }

        static void AddRoomExtras(GameObject root, ThemeProfile t, float L, float wallH, string label, Material inhabitant, Font font, Light[] extraLights, out Light fill)
        {
            float s = t.inhabitantScale, h = L / 2f;
            var inh = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            inh.name = $"InhabitantRef_{1.8f * s:F2}m"; inh.transform.SetParent(root.transform, false);
            inh.transform.localScale = new Vector3(0.36f * s, 0.9f * s, 0.36f * s);
            inh.transform.localPosition = new Vector3(-h + 1.1f * s + 0.6f, 0.9f * s, -h + 1.0f * s + 0.4f);
            inh.GetComponent<Renderer>().sharedMaterial = inhabitant;
            fill = new GameObject("RoomFill").AddComponent<Light>();
            fill.transform.SetParent(root.transform, false);
            fill.transform.localPosition = new Vector3(0.5f, Mathf.Max(3.8f, wallH * 0.9f), -h * 0.4f);
            fill.type = LightType.Point; fill.range = L * 1.4f; fill.intensity = 2.0f; fill.shadows = LightShadows.None;
            var lab = new GameObject("Label"); lab.transform.SetParent(root.transform, false);
            lab.transform.localPosition = new Vector3(0, wallH - 0.45f, h - 0.2f);
            var tm = lab.AddComponent<TextMesh>();
            tm.text = label; tm.font = font; tm.fontSize = 64; tm.characterSize = 0.035f * (L / 6f);
            tm.anchor = TextAnchor.MiddleCenter; tm.color = new Color(1, 1, 1, 0.9f);
            lab.GetComponent<MeshRenderer>().sharedMaterial = font.material;
        }

        static void BuildModularScene(List<ThemeProfile> themes, Dictionary<string, GameObject> P)
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            var inhabitant = InhabitantMat();
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            ThemeProfile T(string n) => themes.First(x => x.themeName == n);
            var defs = new (ThemeProfile t, int cells, string label, Item[] items)[]
            {
                (T("Crypt"), 5, "Crypt  -  modular tiles + walls  -  inhabitant 1.0x", new[] {
                    new Item("prop-altar-stone", 0, 2.4f, 180), new Item("prop-sarcophagus", 0, 0.1f, 0),
                    new Item("prop-coffin", 2.5f, 0.9f, 8), new Item("prop-coffin", 2.5f, -1.4f, -6),
                    new Item("prop-pew-bench", -0.4f, -2.2f, 0), new Item("prop-pew-bench", -0.4f, -3.1f, 0),
                    new Item("prop-treasure-pile", -2.3f, 2.3f, 0), new Item("prop-chest", 2.4f, 2.6f, 200) }),
                (T("Jungle"), 5, "Jungle ruin  -  modular  -  inhabitant 0.75x", new[] {
                    new Item("prop-throne-simple", 0, 2.6f, 180), new Item("prop-fallen-pillar", 0.9f, -1.3f, 25, true),
                    new Item("prop-mushroom", -2.6f, 2.6f, 0), new Item("prop-mushroom", 2.8f, 0.4f, 60), new Item("prop-mushroom", -1.0f, -2.9f, 140),
                    new Item("prop-crate", 2.7f, 2.6f, 12), new Item("prop-crate", 2.7f, 1.7f, -8), new Item("prop-chest", -2.2f, 1.2f, 90),
                    new Item("prop-treasure-pile", 1.3f, 2.4f, 0), new Item("prop-brazier", -0.9f, 0.6f, 0) }),
                (T("Undead"), 5, "Undead ossuary  -  walls scale with the room  -  inhabitant 2.0x", new[] {
                    new Item("prop-throne-simple", 0, 2.8f, 180), new Item("prop-treasure-pile", -2.3f, 2.6f, 0), new Item("prop-treasure-pile", 2.3f, 2.6f, 40),
                    new Item("prop-coffin", -2.4f, -0.6f, 0), new Item("prop-coffin", -2.4f, -2.1f, 0),
                    new Item("prop-sarcophagus", 2.1f, -1.3f, 0), new Item("prop-brazier", 0, 0.4f, 0), new Item("prop-chest", 1.3f, 2.1f, 170) }),
            };
            float cell = OpenKitConst.GridCell, gap = 4f, x = 0f;
            foreach (var d in defs)
            {
                var t = d.t; float s = t.inhabitantScale; float cellR = cell * s; int n = d.cells; float L = n * cellR, h = L / 2f;   // room grid scales with the size class
                int tiers = 1; float wallH = 3f * s;   // walls scale with the room (no more stacking for giants)
                x += (x == 0 ? 0 : gap) + h;
                var root = new GameObject($"ModularRoom_{t.themeName}");
                root.transform.position = new Vector3(x, 0, 0);
                x += h;
                var structure = new GameObject("Structure"); structure.transform.SetParent(root.transform, false);
                for (int cx = 0; cx < n; cx++)
                    for (int cz = 0; cz < n; cz++)
                        Place(P["tile-dungeon-stone-floor"], structure.transform, new Vector3(-h + cellR * (cx + 0.5f), 0, -h + cellR * (cz + 0.5f)), 0);
                int doorCell = n / 2;
                for (int tier = 0; tier < tiers; tier++)
                {
                    float y = tier * 3f;
                    for (int c = 0; c < n; c++)
                    {
                        float u = -h + cellR * (c + 0.5f);
                        Place(P["wall-dungeon-stone"], structure.transform, new Vector3(u, y, h), 180);
                        bool door = tier == 0 && c == doorCell;
                        Place(P[door ? "wall-dungeon-stone-doorway" : "wall-dungeon-stone"], structure.transform, new Vector3(-h, y, u), 90);
                    }
                }
                foreach (var c in new[] { new Vector2(-h, h), new Vector2(h, h), new Vector2(-h, -h) })
                    for (int tier = 0; tier < tiers; tier++)
                        Place(P["prop-pillar-stone"], structure.transform, new Vector3(c.x, tier * 3f, c.y), 0);
                // door in the doorway: hinge on the jamb, swung ~65 degrees into the room
                float dz = -h + cellR * (doorCell + 0.5f);
                float hingeLocal = (s_DoorExtendsPlusX ? -0.56f : 0.56f) * s;   // doorway-local x of the hinge jamb (door + doorway scale together)
                // doorway rotated 90: local +X -> world -Z
                var doorGo = Place(P["prop-door-stone"], structure.transform, new Vector3(-h, 0, dz - hingeLocal), 90 - 65 * (s_DoorExtendsPlusX ? 1 : -1));
                // torches on the back wall's inner face
                float mountY = 1.6f * s;
                foreach (float tx in new[] { -cellR, cellR })
                    Place(P["prop-torch-wall"], root.transform, new Vector3(tx, mountY, h - 0.17f * s), 180);
                var props = new GameObject("Props"); props.transform.SetParent(root.transform, false);
                foreach (var it in d.items)
                {
                    if (!P.ContainsKey(it.name)) continue;
                    var pos = it.abs ? new Vector3(it.x, 0, it.z) : new Vector3(it.x * s, 0, it.z * s);
                    Place(P[it.name], props.transform, pos, it.rot);
                }
                AddRoomExtras(root, t, L, wallH, d.label, inhabitant, font, null, out var fill);
                var room = root.AddComponent<ThemeRoom>(); room.profile = t; room.roomLights = new[] { fill }; room.Apply();
                var cpos = root.transform.position;
                MakeCamera($"Cam_{t.themeName}", cpos + new Vector3(0.5f * L, 0.5f * L + 0.8f + (tiers - 1) * 2f, -0.9f * L), cpos + new Vector3(-0.08f * L, 0.35f * s + 0.25f, 0.0f), 44f, false);
            }
            float span = x;
            MakeCamera("Cam_Overview", new Vector3(span * 0.5f, span * 0.55f, -span * 0.95f), new Vector3(span * 0.5f, 0.6f, 0.8f), 36f, true);
            EditorSceneManager.SaveScene(scene, ModularScene);
            Debug.Log("[OpenKit] saved " + ModularScene);
        }

        // ------------------------------------------------------------------ M2: catalog (every asset; re-themed per screenshot)
        const float CatDX = 4.8f, CatDZ = 4.5f;   // M3 QA: doors hid neighbours and labels overlapped at 3.7 x 3.4

        static void BuildCatalogScene(List<ThemeProfile> themes, Dictionary<string, GameObject> P, Manifest m)
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            // M3 QA: the catalog ran hot - tone the key light and ambient down
            var catSun = GameObject.Find("Sun").GetComponent<Light>(); catSun.intensity = 0.7f;
            RenderSettings.ambientSkyColor *= 0.85f; RenderSettings.ambientEquatorColor *= 0.85f;
            var gm = AssetDatabase.LoadAssetAtPath<Material>($"{DemoDir}/LineupGround.mat");
            Cube("Ground", null, new Vector3(0, -0.2f, 0), new Vector3(160f, 0.1f, 160f), gm);
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            var root = new GameObject("Catalog");
            var items = new GameObject("Items"); items.transform.SetParent(root.transform, false);
            var labels = new GameObject("Labels"); labels.transform.SetParent(root.transform, false);
            var names = m.assets.Select(a => a.name).OrderBy(n => n.StartsWith("prop-") ? 0 : 1).ThenBy(n => n).ToList();
            int CatCols = names.Count > 25 ? 7 : 5;
            int rows = (names.Count + CatCols - 1) / CatCols;
            float camK = Mathf.Max(1f, Mathf.Max(CatCols / 5f, rows / 4f)) * (CatDX / 3.7f) * 0.86f;   // M2 framing was tuned for 5 x 4 at 3.7 m
            for (int i = 0; i < names.Count; i++)
            {
                int c = i % CatCols, r = i / CatCols;
                var pos = new Vector3((c - (CatCols - 1) / 2f) * CatDX, 0, ((rows - 1) / 2f - r) * CatDZ);
                var g = Place(P[names[i]], items.transform, pos, 155);
                if (names[i] == "prop-torch-wall") g.transform.localPosition = pos + new Vector3(0, 1.2f, 0);
                if (names[i] == "prop-door-stone" || names[i] == "prop-door-wood") g.transform.localPosition = pos - Quaternion.Euler(0, 155, 0) * new Vector3(s_DoorExtendsPlusX ? 0.55f : -0.55f, 0, 0);   // centre the leaf on its cell
                var lab = new GameObject("Label_" + names[i]); lab.transform.SetParent(labels.transform, false);
                lab.transform.localPosition = pos + new Vector3(0, 0.02f, -1.9f);
                lab.transform.localRotation = Quaternion.Euler(60, 0, 0);
                var tm = lab.AddComponent<TextMesh>(); tm.text = names[i]; tm.font = font; tm.fontSize = 64; tm.characterSize = 0.05f;
                tm.anchor = TextAnchor.MiddleCenter; tm.color = new Color(0.9f, 0.9f, 0.9f);
                lab.GetComponent<MeshRenderer>().sharedMaterial = font.material;
            }
            var room = root.AddComponent<ThemeRoom>(); room.profile = themes.First(t => t.themeName == "Heaven"); room.Apply();
            MakeCamera("Cam_Catalog", new Vector3(0, 14f, -14.5f) * camK, new Vector3(0, 0f, -1.3f * camK), 42f, true);
            EditorSceneManager.SaveScene(scene, CatalogScene);
            Debug.Log("[OpenKit] saved " + CatalogScene + $" ({names.Count} assets)");
        }

        static void RenderCatalogPerTheme(string outDir)
        {
            EditorSceneManager.OpenScene(CatalogScene, OpenSceneMode.Single);
            var room = GameObject.Find("Catalog").GetComponent<ThemeRoom>();
            var items = room.transform.Find("Items"); var labels = room.transform.Find("Labels");
            var cam = GameObject.Find("Cam_Catalog").GetComponent<Camera>();
            var basePos = new Dictionary<Transform, Vector3>();
            foreach (Transform t in items) basePos[t] = t.localPosition;
            foreach (Transform t in labels) basePos[t] = t.localPosition;
            var camBase = cam.transform.position; var camFwd = cam.transform.rotation;
            foreach (var guid in AssetDatabase.FindAssets("t:ThemeProfile", new[] { ThemesDir }))
            {
                var prof = AssetDatabase.LoadAssetAtPath<ThemeProfile>(AssetDatabase.GUIDToAssetPath(guid));
                float s = prof.inhabitantScale, k = Mathf.Max(1f, s);   // spacing never shrinks below 1 so structural pieces don't collide
                room.profile = prof;
                foreach (var kv in basePos) { var bp = kv.Value; kv.Key.localPosition = new Vector3(bp.x * k, bp.y * (kv.Key.parent == items ? s : 1f), bp.z * k); }
                foreach (Transform t in labels) t.localScale = Vector3.one * k;
                room.Apply();
                cam.transform.SetPositionAndRotation(camBase * k, camFwd);
                RenderCamera(cam, Path.Combine(outDir, $"catalog-{prof.themeName.ToLowerInvariant()}.png"), 1600, 900);
                // flame close-up: brazier + wall torch
                var br = items.Cast<Transform>().FirstOrDefault(t => t.name == "prop-brazier");
                if (br)
                {
                    var closeGo = new GameObject("Cam_FlameClose");
                    var cc = closeGo.AddComponent<Camera>();
                    cc.CopyFrom(cam); cc.fieldOfView = 30f;
                    var target = br.position + Vector3.up * (1.0f * s);
                    closeGo.transform.position = target + new Vector3(0.9f, 0.9f, -2.3f) * s;
                    closeGo.transform.LookAt(target);
                    cc.GetUniversalAdditionalCameraData().renderPostProcessing = true;
                    RenderCamera(cc, Path.Combine(outDir, $"flame-{prof.themeName.ToLowerInvariant()}.png"), 1000, 800);
                    UnityEngine.Object.DestroyImmediate(closeGo);
                }
            }
        }

        // ------------------------------------------------------------------ M3: validation (naming, scale, tris, materials, pivots, prefabs, lights)
        static readonly System.Text.RegularExpressions.Regex NameRe = new(@"^(prop|tile|wall|monster)-[a-z0-9]+(-[a-z0-9]+)*$");
        static readonly Dictionary<string, string> PrefixCategory = new() { { "prop", "Props" }, { "tile", "Tiles" }, { "wall", "Walls" }, { "monster", "Monsters" } };

        static void ValidateAssets(Manifest m)
        {
            var errors = new List<string>();
            var slotMats = OpenKitConst.SlotNames.Select(n => AssetDatabase.LoadAssetAtPath<Material>($"{SlotsDir}/{n}.mat")).ToList();
            var seen = new HashSet<string>();
            int checkedCount = 0;
            foreach (var a in m.assets)
            {
                void E(string msg) => errors.Add($"{a.name}: {msg}");
                if (!seen.Add(a.name)) E("duplicate manifest entry");
                // naming + category
                if (!NameRe.IsMatch(a.name)) E("name is not <prefix>-lower-kebab-case");
                string cat = Cat(a);
                if (!Categories.Contains(cat)) E($"unknown category '{cat}'");
                string pre = a.name.Split('-')[0];
                if (!PrefixCategory.TryGetValue(pre, out var want) || want != cat) E($"prefix '{pre}-' does not belong in category '{cat}'");
                if (!Enum.TryParse<SizeClass>(a.sizeClass, out _)) E($"unknown sizeClass '{a.sizeClass}'");
                // model: root transform, tris, materials, bounds/pivot
                var go = AssetDatabase.LoadAssetAtPath<GameObject>(ModelPath(a));
                if (!go) { E($"model missing at {ModelPath(a)}"); continue; }
                if (go.name != a.name) E($"model asset name '{go.name}' != manifest name");
                var t = go.transform;
                if (Quaternion.Angle(t.localRotation, Quaternion.identity) > 0.01f || (t.localScale - Vector3.one).sqrMagnitude > 1e-8f)
                    E($"root transform not identity (rot {t.localEulerAngles}, scale {t.localScale})");
                // static props: one MeshFilter; rigged monsters: one SkinnedMeshRenderer
                var srcs = go.GetComponentsInChildren<MeshFilter>().Select(x => (tr: x.transform, mesh: x.sharedMesh, rend: (Renderer)x.GetComponent<Renderer>()))
                    .Concat(go.GetComponentsInChildren<SkinnedMeshRenderer>().Select(x => (tr: x.transform, mesh: x.sharedMesh, rend: (Renderer)x))).ToList();
                if (srcs.Count != 1) E($"{srcs.Count} meshes (expected 1)");
                if (srcs.Count == 0) continue;
                var src = srcs[0];
                if (src.tr != t && (Quaternion.Angle(src.tr.localRotation, Quaternion.identity) > 0.01f || (src.tr.localScale - Vector3.one).sqrMagnitude > 1e-8f || src.tr.localPosition.sqrMagnitude > 1e-8f))
                    E($"mesh child transform not identity (pos {src.tr.localPosition}, rot {src.tr.localEulerAngles}, scale {src.tr.localScale})");
                if (a.rigged != (src.rend is SkinnedMeshRenderer)) E($"rigged={a.rigged} but the model has a {src.rend.GetType().Name}");
                var mesh = src.mesh;
                int tris = 0; for (int si = 0; si < mesh.subMeshCount; si++) tris += (int)mesh.GetIndexCount(si) / 3;
                if (tris != a.tris) E($"tris {tris} in Unity != {a.tris} from Blender");
                if (tris > a.budget) E($"tris {tris} over budget {a.budget}");
                var rend = src.rend;
                var mats = rend ? rend.sharedMaterials : new Material[0];
                if (mats.Length != mesh.subMeshCount) E($"{mats.Length} materials for {mesh.subMeshCount} submeshes");
                if (mats.Any(x => !x)) E("missing (null) material");
                if (mats.Any(x => x && !slotMats.Contains(x))) E($"non-slot materials [{string.Join(",", mats.Where(x => x && !slotMats.Contains(x)).Select(x => x.name))}]");
                var b = mesh.bounds; const float eps = 1e-3f;
                // Blender (x, y, z) -> Unity (-x, z, -y): dims_m = [x, y, z] -> Unity size (x, z, y)
                if (a.dims_m != null && a.dims_m.Length == 3)
                {
                    var want3 = new Vector3(a.dims_m[0], a.dims_m[2], a.dims_m[1]);
                    if ((b.size - want3).magnitude > 0.01f) E($"size {b.size} != Blender dims {want3} (unit scale problem?)");
                }
                string piv = string.IsNullOrEmpty(a.pivot) ? "bottom_center" : a.pivot;
                bool pivOk = piv switch
                {
                    "hinge" => b.max.x <= 0.05f && b.max.x >= -eps && b.min.x < -0.3f && Mathf.Abs(b.min.y) < eps && Mathf.Abs(b.center.z) < 0.05f,
                    "wall_back" => Mathf.Abs(b.min.z) < eps && Mathf.Abs(b.min.y) < eps && Mathf.Abs(b.center.x) < 0.02f,
                    "floor_top" => Mathf.Abs(b.max.y) < eps && Mathf.Abs(b.center.x) < 0.02f && Mathf.Abs(b.center.z) < 0.02f,
                    "bottom_center" => Mathf.Abs(b.min.y) < eps && Mathf.Abs(b.center.x) < 0.02f && Mathf.Abs(b.center.z) < 0.02f,
                    _ => false,
                };
                if (!pivOk) E($"pivot '{piv}' check failed, bounds {b.min}..{b.max}");
                // prefab: exists, same name, collider, ThemeAdaptive settings, light iff socket
                var pf = AssetDatabase.LoadAssetAtPath<GameObject>(PrefabPath(a));
                if (!pf) { E($"prefab missing at {PrefabPath(a)}"); continue; }
                if (pf.name != a.name) E($"prefab name '{pf.name}' != manifest name");
                var bc = pf.GetComponent<BoxCollider>();
                if (!bc || bc.size.x < 0.01f || bc.size.y < 0.01f || bc.size.z < 0.01f) E("prefab has no usable BoxCollider");
                var ta = pf.GetComponent<ThemeAdaptive>();
                if (!ta) E("prefab has no ThemeAdaptive");
                else if (ta.scalesWithRoom != a.scalesWithRoom) E("ThemeAdaptive.scalesWithRoom != manifest");
                bool wantsLight = a.lightSocket != null && a.lightSocket.Length == 3;
                int lights = pf.GetComponentsInChildren<Light>(true).Length;
                if (wantsLight != (lights > 0)) E($"light socket {(wantsLight ? "set" : "unset")} but prefab has {lights} lights");
                if (wantsLight && !mats.Any(x => x && x.name == "Emissive")) E("light-emitting prop without an Emissive slot");
                if (cat == "Monsters" || a.rigged) ValidateMonster(a, go, pf, E);
                checkedCount++;
            }
            // stale / orphan models or prefabs that would ship in the package without a Blender source
            foreach (var cat in Categories)
                foreach (var kind in new[] { ("Models", "*.fbx"), ("Prefabs", "*.prefab") })
                {
                    string dir = Path.Combine(ProjectRoot, Root, kind.Item1, cat);
                    if (!Directory.Exists(dir)) continue;
                    foreach (var f in Directory.GetFiles(dir, kind.Item2))
                    {
                        string n = Path.GetFileNameWithoutExtension(f);
                        var entry = m.assets.FirstOrDefault(x => x.name == n);
                        if (entry == null) errors.Add($"{kind.Item1}/{cat}/{Path.GetFileName(f)}: orphan (not in the Blender manifest)");
                        else if (Cat(entry) != cat) errors.Add($"{kind.Item1}/{cat}/{Path.GetFileName(f)}: in the wrong category folder (manifest says {Cat(entry)})");
                    }
                }
            ValidateRoomAdapt(m, errors);
            var byMs = m.assets.GroupBy(a => string.IsNullOrEmpty(a.milestone) ? "?" : a.milestone).OrderBy(g => g.Key).Select(g => $"{g.Key}={g.Count()}");
            if (errors.Count > 0)
            {
                foreach (var e in errors) Debug.LogError("[OpenKit] VALIDATE FAIL " + e);
                throw new Exception($"validation failed: {errors.Count} problem(s)");
            }
            Debug.Log($"[OpenKit] VALIDATE OK {checkedCount} assets ({string.Join(", ", byMs)}): naming, category, root transform/scale, tris vs Blender and budget, slot materials, pivots, prefabs/colliders, light sockets, monster rigs/clips/animators, no orphans, room-adapt (room scale x3, re-theme, 3 working colour slots)");
        }

        // ------------------------------------------------------------------ room-adapt rule: room scale, re-theme, 3 working user colour slots
        [Serializable] class RoomAdaptException { public string asset; public string rule; public string reason; }
        [Serializable] class RoomAdaptExceptions { public RoomAdaptException[] exceptions; }
        static string ExceptionsPath => Path.Combine(ProjectRoot, "Blender", "roomadapt_exceptions.json");

        static List<RoomAdaptException> LoadRoomAdaptExceptions(List<string> errors)
        {
            if (!File.Exists(ExceptionsPath)) { errors.Add($"room-adapt exceptions file missing: {ExceptionsPath}"); return new List<RoomAdaptException>(); }
            var f = JsonUtility.FromJson<RoomAdaptExceptions>(File.ReadAllText(ExceptionsPath));
            var list = (f?.exceptions ?? new RoomAdaptException[0]).ToList();
            foreach (var x in list)
            {
                if (string.IsNullOrWhiteSpace(x.asset)) errors.Add("room-adapt exception without an asset name");
                if (x.rule != "room_scale" && x.rule != "color_slots") errors.Add($"room-adapt exception for {x.asset}: unknown rule '{x.rule}' (room_scale | color_slots)");
                if (string.IsNullOrWhiteSpace(x.reason)) errors.Add($"room-adapt exception for {x.asset}/{x.rule}: a reason is required");
            }
            return list;
        }

        static readonly Color[] ProbeColors = { new(1f, 0f, 1f), new(0f, 1f, 1f), new(1f, 1f, 0f), new(0f, 1f, 0f), new(1f, 0.3f, 0f) };

        static Color32[] RenderPixels(Camera cam, RenderTexture rt, Texture2D tex)
        {
            cam.targetTexture = rt; cam.aspect = 1f;
            cam.Render(); cam.Render();
            var prev = RenderTexture.active; RenderTexture.active = rt;
            tex.ReadPixels(new Rect(0, 0, rt.width, rt.height), 0, 0); tex.Apply();
            RenderTexture.active = prev; cam.targetTexture = null;
            return tex.GetPixels32();
        }

        static int DiffPixels(Color32[] a, Color32[] b)
        {
            int n = 0;
            for (int i = 0; i < a.Length; i++)
            {
                int d = Mathf.Max(Mathf.Abs(a[i].r - b[i].r), Mathf.Max(Mathf.Abs(a[i].g - b[i].g), Mathf.Abs(a[i].b - b[i].b)));
                if (d > 24) n++;
            }
            return n;
        }

        /// <summary>Every asset must room-scale (halfling / human / giant), re-theme at runtime and expose 3 WORKING user colour slots
        /// (a slot works when overriding it changes rendered pixels). Entries in Blender/roomadapt_exceptions.json (with a reason) are skipped.</summary>
        static void ValidateRoomAdapt(Manifest m, List<string> errors)
        {
            var exc = LoadRoomAdaptExceptions(errors);
            bool Excepted(string asset, string rule) => exc.Any(x => x.asset == asset && x.rule == rule);
            foreach (var x in exc) Debug.Log($"[OpenKit] ROOMADAPT exception {x.asset} / {x.rule}: {x.reason}");
            // new scene FIRST: NewScene(Single) unloads unreferenced assets, which would leave dead ThemeProfile handles behind
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var profiles = AssetDatabase.FindAssets("t:ThemeProfile", new[] { ThemesDir }).Select(g => AssetDatabase.LoadAssetAtPath<ThemeProfile>(AssetDatabase.GUIDToAssetPath(g))).OrderBy(p => p.themeName).ToList();
            if (profiles.Count < 2) { errors.Add("room-adapt: need at least 2 theme profiles to test re-theming"); return; }
            var human = profiles.FirstOrDefault(p => p.themeName == "Heaven") ?? profiles[0];
            var other = profiles.First(p => p != human);
            RenderSettings.skybox = null; RenderSettings.ambientMode = AmbientMode.Flat; RenderSettings.ambientLight = new Color(0.45f, 0.45f, 0.45f);
            var sun = new GameObject("ProbeSun").AddComponent<Light>(); sun.type = LightType.Directional; sun.intensity = 1.1f; sun.shadows = LightShadows.None;
            sun.transform.rotation = Quaternion.Euler(45f, -30f, 0f);
            var camGo = new GameObject("ProbeCam"); var cam = camGo.AddComponent<Camera>();
            cam.clearFlags = CameraClearFlags.SolidColor; cam.backgroundColor = Color.black; cam.fieldOfView = 30f; cam.enabled = false;
            var camData = cam.GetUniversalAdditionalCameraData(); camData.renderPostProcessing = false; camData.antialiasing = AntialiasingMode.None;
            const int px = 128;
            var rt = new RenderTexture(px, px, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB); rt.Create();
            var tex = new Texture2D(px, px, TextureFormat.RGB24, false);
            var views = new[] { new Vector3(0.35f, 0.55f, -1f), new Vector3(-0.4f, 0.6f, 1f), new Vector3(0.05f, 1f, -0.15f) };
            var roomGo = new GameObject("ProbeRoom"); var room = roomGo.AddComponent<ThemeRoom>(); room.profile = human;
            int scaleOk = 0, themeOk = 0, colorOk = 0;
            var block = new MaterialPropertyBlock();
            var baseColorId = Shader.PropertyToID("_BaseColor");
            try
            {
                foreach (var a in m.assets)
                {
                    void E(string msg) => errors.Add($"{a.name}: ROOMADAPT {msg}");
                    var pf = AssetDatabase.LoadAssetAtPath<GameObject>(PrefabPath(a));
                    if (!pf) continue;   // reported by ValidateAssets
                    var pta = pf.GetComponent<ThemeAdaptive>();
                    if (!pta) { E("no ThemeAdaptive: cannot room-scale or re-theme"); continue; }
                    bool scaleExc = Excepted(a.name, "room_scale"), colorExc = Excepted(a.name, "color_slots");
                    if (!pta.scalesWithRoom && !scaleExc) E("scalesWithRoom is off (room_scale needs an exception entry with a reason)");
                    if (pta.SlotMap == null || pta.SlotMap.Count == 0) { E("empty slot map: cannot re-theme"); continue; }
                    var pfLights = pf.GetComponentsInChildren<Light>(true).Select(l => l.range).ToArray();
                    var inst = (GameObject)PrefabUtility.InstantiatePrefab(pf, roomGo.transform);
                    var ta = inst.GetComponent<ThemeAdaptive>();
                    var rends = inst.GetComponentsInChildren<Renderer>(true);
                    foreach (var r in rends) if (!ta.SlotMap.Any(e => e.renderer == r)) E($"renderer '{r.name}' is not in the slot map (would not re-theme)");
                    Bounds WB() { var bb = rends[0].bounds; foreach (var r in rends) bb.Encapsulate(r.bounds); return bb; }
                    // --- room scale: Halfling 0.75 / Human 1.0 / Giant 2.0
                    room.profile = human;
                    room.roomSize = RoomSize.Human; room.Apply();
                    var refSize = WB().size;
                    bool sOk = pta.scalesWithRoom || scaleExc;
                    foreach (var size in new[] { RoomSize.Halfling, RoomSize.Human, RoomSize.Giant })
                    {
                        room.roomSize = size; room.Apply();
                        float s = pta.scalesWithRoom ? OpenKitConst.ScaleOf(size, 1f) : 1f;
                        if ((inst.transform.localScale - pta.baseScale * s).magnitude > 1e-3f) { E($"{size}: localScale {inst.transform.localScale} != {s}"); sOk = false; }
                        if ((WB().size - refSize * s).magnitude > 0.01f * Mathf.Max(1f, refSize.magnitude * s)) { E($"{size}: renderer bounds {WB().size} did not scale to {refSize * s}"); sOk = false; }
                        var ls = inst.GetComponentsInChildren<Light>(true);
                        for (int i = 0; i < ls.Length && i < pfLights.Length; i++)
                            if (Mathf.Abs(ls[i].range - pfLights[i] * s) > 1e-3f) { E($"{size}: light range {ls[i].range} != {pfLights[i]} x {s}"); sOk = false; }
                    }
                    if (sOk) scaleOk++;
                    // --- re-theme: every submesh takes the theme's shared material; two themes must differ
                    room.roomSize = RoomSize.Human;
                    bool tOk = true;
                    foreach (var prof in new[] { other, human })
                    {
                        room.profile = prof; room.Apply();
                        foreach (var e in ta.SlotMap)
                        {
                            var mats = e.renderer.sharedMaterials;
                            for (int i = 0; i < mats.Length; i++)
                                if (i >= e.slots.Length || mats[i] != ThemeMaterialCache.Get(prof, e.slots[i])) { E($"{prof.themeName}: submesh {i} not re-themed ({(mats[i] ? mats[i].name : "null")}, expected {(i < e.slots.Length && ThemeMaterialCache.Get(prof, e.slots[i]) ? ThemeMaterialCache.Get(prof, e.slots[i]).name : "null")}, resolved profile {(ta.CurrentProfile ? ta.CurrentProfile.themeName : "none")}, room {(ta.GetComponentInParent<ThemeRoom>(true) ? "yes" : "no")})"); tOk = false; }
                        }
                    }
                    if (tOk) themeOk++;
                    // --- 3 working user colour slots (Primary / Secondary / Tertiary = Accent + Metal)
                    if (!colorExc)
                    {
                        bool cOk = true;
                        var b = WB();
                        float radius = Mathf.Max(b.extents.magnitude, 0.15f), dist = radius / Mathf.Sin(15f * Mathf.Deg2Rad) * 1.1f;
                        cam.nearClipPlane = Mathf.Max(0.01f, dist - radius * 2f); cam.farClipPlane = dist + radius * 2f;
                        var baseline = new List<Color32[]>();
                        foreach (var v in views) { cam.transform.position = b.center + v.normalized * dist; cam.transform.LookAt(b.center); baseline.Add(RenderPixels(cam, rt, tex)); }
                        for (int u = 0; u < OpenKitConst.UserSlotCount; u++)
                        {
                            var us = (UserColorSlot)u;
                            var subs = ta.SlotMap.SelectMany(e => Enumerable.Range(0, e.slots.Length).Where(i => OpenKitConst.UserSlotOf(e.slots[i]) == u).Select(i => (e.renderer, i))).ToList();
                            if (subs.Count == 0) { E($"user colour slot {OpenKitConst.UserSlotNames[u]} maps to no material region"); cOk = false; continue; }
                            // probe colour: the palette entry furthest from the theme default of that region
                            var def = subs[0].renderer.sharedMaterials[subs[0].i].GetColor(baseColorId);
                            var probe = ProbeColors.OrderByDescending(c => Mathf.Abs(c.r - def.r) + Mathf.Abs(c.g - def.g) + Mathf.Abs(c.b - def.b)).First();
                            ta.SetUserColor(us, probe);
                            bool mpb = subs.All(sb => { sb.renderer.GetPropertyBlock(block, sb.i); return block.GetColor(baseColorId) == probe; });
                            if (!mpb) { E($"user colour slot {OpenKitConst.UserSlotNames[u]}: property block not applied"); cOk = false; }
                            int changed = 0;
                            for (int vi = 0; vi < views.Length; vi++) { cam.transform.position = b.center + views[vi].normalized * dist; cam.transform.LookAt(b.center); changed += DiffPixels(baseline[vi], RenderPixels(cam, rt, tex)); }
                            ta.SetUserColor(us, null);
                            if (changed < 6) { E($"user colour slot {OpenKitConst.UserSlotNames[u]} changes {changed} visible pixels (needs a visible region; hidden or zero-area geometry does not count)"); cOk = false; }
                            else Debug.Log($"[OpenKit] ROOMADAPT {a.name} {OpenKitConst.UserSlotNames[u]}: {subs.Count} submesh(es), {changed} px changed");
                        }
                        // clearing the overrides must restore the theme look
                        bool cleared = ta.SlotMap.All(e => Enumerable.Range(0, e.slots.Length).All(i => { e.renderer.GetPropertyBlock(block, i); return OpenKitConst.UserSlotOf(e.slots[i]) < 0 || block.isEmpty; }));
                        if (!cleared) { E("clearing the user colour slots left a property block behind"); cOk = false; }
                        if (cOk) colorOk++;
                    }
                    UnityEngine.Object.DestroyImmediate(inst);
                }
            }
            finally
            {
                rt.Release(); UnityEngine.Object.DestroyImmediate(rt); UnityEngine.Object.DestroyImmediate(tex);
            }
            int ce = exc.Count(x => x.rule == "color_slots");
            Debug.Log($"[OpenKit] ROOMADAPT room-scale OK {scaleOk}/{m.assets.Length}, re-theme OK {themeOk}/{m.assets.Length}, 3 working colour slots OK {colorOk}/{m.assets.Length - ce}, exceptions {exc.Count}{(exc.Count == 0 ? " (none)" : "")}");
        }

        // ------------------------------------------------------------------ room-adapt captures: roomscale.png + colorslots.png
        static TextMesh WorldLabel(Transform parent, string text, Vector3 pos, float size, Color col, Font font, Quaternion rot)
        {
            var g = new GameObject("Label"); g.transform.SetParent(parent, false);
            g.transform.localPosition = pos; g.transform.localRotation = rot;
            var tm = g.AddComponent<TextMesh>(); tm.text = text; tm.font = font; tm.fontSize = 64; tm.characterSize = size;
            tm.anchor = TextAnchor.MiddleCenter; tm.alignment = TextAlignment.Center; tm.color = col;
            g.GetComponent<MeshRenderer>().sharedMaterial = font.material;
            return tm;
        }

        static Material RefMat(string name, Color c)
        {
            string p = $"{DemoDir}/{name}.mat";
            var m = AssetDatabase.LoadAssetAtPath<Material>(p);
            if (!m) { m = new Material(Shader.Find(ThemeMaterialCache.LitShader)) { name = name }; AssetDatabase.CreateAsset(m, p); }
            m.SetColor("_BaseColor", c); m.SetFloat("_Smoothness", 0.25f); EditorUtility.SetDirty(m);
            return m;
        }

        static GameObject Capsule(string name, Transform parent, Vector3 footPos, float height, Material mat)
        {
            var c = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            UnityEngine.Object.DestroyImmediate(c.GetComponent<Collider>());
            c.name = name; c.transform.SetParent(parent, false);
            c.transform.localScale = new Vector3(height * 0.25f, height * 0.5f, height * 0.25f);
            c.transform.localPosition = footPos + Vector3.up * height * 0.5f;
            c.GetComponent<Renderer>().sharedMaterial = mat;
            return c;
        }

        static readonly (RoomSize size, string label)[] RoomSizes = { (RoomSize.Halfling, "Halfling room  0.75x"), (RoomSize.Human, "Human room  1.0x"), (RoomSize.Giant, "Giant room  2.0x") };

        static void CaptureRoomScale(Dictionary<string, GameObject> P, string file)
        {
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            GameObject.Find("Sun").GetComponent<Light>().transform.rotation = Quaternion.Euler(48f, -20f, 0f);
            var gm = AssetDatabase.LoadAssetAtPath<Material>($"{DemoDir}/LineupGround.mat");
            Cube("Ground", null, new Vector3(0, -0.45f, 0), new Vector3(200f, 0.1f, 200f), gm);
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            var prof = AssetDatabase.LoadAssetAtPath<ThemeProfile>($"{ThemesDir}/Dungeon.asset") ?? throw new Exception("theme missing: Dungeon");
            var inhabitant = InhabitantMat(); var humanRef = RefMat("HumanRef", new Color(0.72f, 0.72f, 0.72f));
            float cell = OpenKitConst.GridCell, gap = 2.2f, x = 0f; int n = 3;
            var faceCam = Quaternion.Euler(20f, 0, 0);
            foreach (var (size, label) in RoomSizes)
            {
                float s = OpenKitConst.ScaleOf(size, 1f), cr = cell * s, L = n * cr, h = L / 2f;
                x += (x == 0 ? 0 : gap) + h;
                var root = new GameObject($"Room_{size}"); root.transform.position = new Vector3(x, 0, 0);
                x += h;
                var st = new GameObject("Structure"); st.transform.SetParent(root.transform, false);
                for (int cx = 0; cx < n; cx++) for (int cz = 0; cz < n; cz++)
                    Place(P["tile-dungeon-stone-floor"], st.transform, new Vector3(-h + cr * (cx + 0.5f), 0, -h + cr * (cz + 0.5f)), 0);
                for (int c = 0; c < n; c++)
                    Place(P[c == 1 ? "wall-dungeon-stone-doorway" : "wall-dungeon-stone"], st.transform, new Vector3(-h + cr * (c + 0.5f), 0, h), 180);
                // wooden door in the back doorway (doorway local +X -> world -X at 180), swung 60 degrees into the room
                float hingeX = (s_DoorExtendsPlusX ? -0.56f : 0.56f) * s;
                Place(P["prop-door-wood"], st.transform, new Vector3(-hingeX, 0, h - 0.17f * s), 180 - 60 * (s_DoorExtendsPlusX ? 1 : -1));
                var props = new GameObject("Props"); props.transform.SetParent(root.transform, false);
                foreach (var (nm, px, pz, rot) in new[] { ("prop-bed-simple", -1.25f, 1.05f, 90f), ("prop-bench-wood", 0.95f, -0.35f, 90f), ("prop-stool-wood", -0.2f, -0.9f, 15f),
                                                           ("prop-bookshelf", 1.55f, 1.85f, 180f), ("prop-lantern", -1.7f, -1.5f, 0f) })
                    Place(P[nm], props.transform, new Vector3(px * s, 0, pz * s), rot);
                var refs = new GameObject("References"); refs.transform.SetParent(root.transform, false);
                Capsule("Inhabitant_1.8xS", refs.transform, new Vector3(0.55f * s, 0, -1.6f * s), 1.8f * s, inhabitant);
                Capsule("Human_1.8m", refs.transform, new Vector3(h + 0.55f, 0, -h + 0.4f), 1.8f, humanRef);
                WorldLabel(root.transform, label, new Vector3(0, 0.05f, -h - 0.9f), 0.05f, Color.white, font, Quaternion.Euler(70f, 0, 0));
                var room = root.AddComponent<ThemeRoom>(); room.profile = prof; room.roomSize = size; room.Apply();
            }
            float span = x;
            WorldLabel(null, "grey capsule = human reference 1.8 m (same in every room)     cyan capsule = room inhabitant 1.8 m x room scale     Dungeon theme, same prefabs",
                new Vector3(span * 0.5f, 0.05f, -7.0f), 0.045f, new Color(0.85f, 0.85f, 0.85f), font, Quaternion.Euler(70f, 0, 0));
            var cam = MakeCamera("Cam_RoomScale", new Vector3(span * 0.5f, 11.5f, -20f), new Vector3(span * 0.5f, 1.2f, 0.6f), 42f, true);
            RenderCamera(cam, file, 2400, 1100);
        }

        static void CaptureColorSlots(Dictionary<string, GameObject> P, string file)
        {
            var combos = new (string name, Color p, Color s, Color t)[]
            {
                ("Royal",  new Color(0.36f, 0.14f, 0.46f), new Color(0.95f, 0.91f, 0.78f), new Color(0.92f, 0.72f, 0.18f)),
                ("Forest", new Color(0.22f, 0.36f, 0.16f), new Color(0.74f, 0.66f, 0.50f), new Color(0.12f, 0.50f, 0.42f)),
                ("Ocean",  new Color(0.12f, 0.22f, 0.42f), new Color(0.84f, 0.90f, 0.96f), new Color(0.90f, 0.34f, 0.24f)),
            };
            string Hex(Color c) => "#" + ColorUtility.ToHtmlStringRGB(c);
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            var gm = AssetDatabase.LoadAssetAtPath<Material>($"{DemoDir}/LineupGround.mat");
            Cube("Ground", null, new Vector3(0, -0.05f, 0), new Vector3(200f, 0.1f, 200f), gm);
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            var prof = AssetDatabase.LoadAssetAtPath<ThemeProfile>($"{ThemesDir}/Dungeon.asset") ?? throw new Exception("theme missing: Dungeon");
            var roomGo = new GameObject("SlotRoom"); var room = roomGo.AddComponent<ThemeRoom>(); room.profile = prof;
            var bed = Place(P["prop-bed-simple"], roomGo.transform, new Vector3(0.2f, 0, 0.3f), 150f);
            var ta = bed.GetComponent<ThemeAdaptive>();
            Capsule("Human_1.8m", null, new Vector3(-1.9f, 0, -0.2f), 1.8f, RefMat("HumanRef", new Color(0.72f, 0.72f, 0.72f)));
            const float fov = 34f; const int tw = 720, th = 540;
            var cam = MakeCamera("Cam_Slots", new Vector3(3.0f, 4.2f, -6.7f), new Vector3(-0.35f, 0.7f, 0.35f), fov, true);
            float ld = 0.3f, halfH = Mathf.Tan(fov * 0.5f * Mathf.Deg2Rad) * ld;
            var lab = new GameObject("Label"); lab.transform.SetParent(cam.transform, false); lab.transform.localPosition = new Vector3(0, -halfH * 0.84f, ld);
            var tm = lab.AddComponent<TextMesh>(); tm.font = font; tm.fontSize = 64; tm.characterSize = 0.0036f * ld;
            tm.anchor = TextAnchor.MiddleCenter; tm.alignment = TextAlignment.Center; tm.color = new Color(0.95f, 0.95f, 0.95f);
            lab.GetComponent<MeshRenderer>().sharedMaterial = font.material;
            var strip = GameObject.CreatePrimitive(PrimitiveType.Quad); UnityEngine.Object.DestroyImmediate(strip.GetComponent<Collider>());
            strip.transform.SetParent(cam.transform, false); strip.transform.localPosition = new Vector3(0, -halfH * 0.86f, ld + 0.002f);
            strip.transform.localScale = new Vector3(2.2f * halfH * tw / th, halfH * 0.3f, 1f);
            var stripMat = new Material(Shader.Find("Universal Render Pipeline/Unlit")) { hideFlags = HideFlags.DontSave }; stripMat.SetColor("_BaseColor", new Color(0.035f, 0.035f, 0.05f));
            var sr = strip.GetComponent<MeshRenderer>(); sr.sharedMaterial = stripMat; sr.shadowCastingMode = ShadowCastingMode.Off;
            var sheet = new Texture2D(3 * tw, 3 * th, TextureFormat.RGB24, false);
            var rt = new RenderTexture(tw, th, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB) { antiAliasing = 4 }; rt.Create();
            var tile = new Texture2D(tw, th, TextureFormat.RGB24, false);
            for (int r = 0; r < 3; r++)
                for (int c = 0; c < 3; c++)
                {
                    var co = combos[r]; var (size, label) = RoomSizes[c];
                    room.roomSize = size;
                    ta.primaryColor.enabled = ta.secondaryColor.enabled = ta.tertiaryColor.enabled = true;
                    ta.primaryColor.color = co.p; ta.secondaryColor.color = co.s; ta.tertiaryColor.color = co.t;
                    room.Apply();
                    tm.text = $"prop-bed-simple  -  {label}  -  {co.name}  (grey = human 1.8 m)\nPrimary {Hex(co.p)}   Secondary {Hex(co.s)}   Tertiary {Hex(co.t)}";
                    cam.targetTexture = rt; cam.aspect = (float)tw / th;
                    for (int k = 0; k < 3; k++) cam.Render();
                    var prev = RenderTexture.active; RenderTexture.active = rt;
                    tile.ReadPixels(new Rect(0, 0, tw, th), 0, 0); tile.Apply(); RenderTexture.active = prev; cam.targetTexture = null;
                    sheet.SetPixels32(c * tw, (2 - r) * th, tw, th, tile.GetPixels32());
                }
            var line = new Color32(40, 42, 52, 255);
            for (int c = 1; c < 3; c++) for (int y = 0; y < sheet.height; y++) { sheet.SetPixel(c * tw, y, line); sheet.SetPixel(c * tw - 1, y, line); }
            for (int r = 1; r < 3; r++) for (int xx = 0; xx < sheet.width; xx++) { sheet.SetPixel(xx, r * th, line); sheet.SetPixel(xx, r * th - 1, line); }
            sheet.Apply();
            File.WriteAllBytes(file, sheet.EncodeToPNG());
            UnityEngine.Object.DestroyImmediate(sheet); UnityEngine.Object.DestroyImmediate(tile); rt.Release(); UnityEngine.Object.DestroyImmediate(rt); UnityEngine.Object.DestroyImmediate(stripMat);
            Debug.Log($"[OpenKit] colour-slot grid {file}");
        }

        // ------------------------------------------------------------------ M3: hero vignettes (inn, smithy, yard) built from the M3 props
        struct Hero { public string name; public float x, z, rot, y, tilt; public Hero(string n, float x, float z, float rot = 0, float y = 0, float tilt = 0) { name = n; this.x = x; this.z = z; this.rot = rot; this.y = y; this.tilt = tilt; } }

        static void BuildHeroScene(List<ThemeProfile> themes, Dictionary<string, GameObject> P)
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            var inhabitant = InhabitantMat();
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            ThemeProfile T(string n) => themes.First(x => x.themeName == n);
            var defs = new (ThemeProfile t, int cells, bool walls, string label, Hero[] items)[]
            {
                (T("Dungeon"), 7, true, "Inn  -  M3 props  -  Dungeon  -  inhabitant 0.75x", new[] {
                    new Hero("prop-table-wood", 0.5f, 0.3f, 0), new Hero("prop-bench-wood", 0.5f, -0.45f, 0), new Hero("prop-bench-wood", 0.5f, 1.05f, 180),
                    new Hero("prop-stool-wood", -0.75f, 0.3f, 0), new Hero("prop-stool-wood", 1.75f, 0.2f, 20),
                    new Hero("prop-lantern", 0.8f, 0.35f, 30, 0.76f), new Hero("prop-bookshelf", -2.0f, 4.8f, 180), new Hero("prop-keg-stand", 1.6f, 4.65f, 180),
                    new Hero("prop-bed-simple", -4.05f, 2.6f, 90), new Hero("prop-lectern", 3.4f, 2.4f, -120), new Hero("prop-candelabra", -1.9f, 1.4f, 0),
                    new Hero("prop-candelabra", 3.7f, 0.6f, 0), new Hero("prop-sack-grain", 3.7f, 4.3f, 200), new Hero("prop-bucket-wood", 2.8f, 4.7f, 0) }),
                (T("Hell"), 5, true, "Giant's smithy  -  M3 props  -  Hell  -  inhabitant 2.0x", new[] {
                    new Hero("prop-anvil", 0.3f, 0.4f, 160), new Hero("prop-stump-axe", -1.2f, -0.6f, 30), new Hero("prop-weapon-rack", -0.8f, 3.3f, 180),
                    new Hero("prop-cauldron", 1.6f, 2.2f, 0), new Hero("prop-torch-standing", -3.0f, 3.2f, 0), new Hero("prop-torch-standing", 3.0f, 3.2f, 0),
                    new Hero("prop-bucket-wood", 0.9f, -0.1f, 0), new Hero("prop-ladder-wood", 2.3f, 2.9f, 0, 0, 15), new Hero("prop-crate", -2.3f, 0.7f, 15),
                    new Hero("prop-barrel", 2.3f, 0.1f, 0), new Hero("prop-sack-grain", -2.1f, -1.5f, 60) }),
                (T("Heaven"), 5, false, "Village yard  -  M3 props  -  Heaven  -  inhabitant 1.0x", new[] {
                    new Hero("prop-well-stone", 0.3f, 1.0f, 180), new Hero("prop-cart-hand", 2.3f, -0.8f, -140), new Hero("prop-signpost", -2.8f, -2.4f, 30),
                    new Hero("prop-banner-standing", -2.9f, 3.0f, 150), new Hero("prop-banner-standing", 2.9f, 3.0f, 210), new Hero("prop-sack-grain", 1.9f, 1.8f, 20),
                    new Hero("prop-bucket-wood", 1.25f, 0.1f, 0), new Hero("prop-barrel", 3.1f, 2.9f, 0), new Hero("prop-bench-wood", -1.4f, -0.6f, 40),
                    new Hero("prop-lantern", -0.7f, -1.2f, 20) }),
            };
            float cell = OpenKitConst.GridCell, gap = 18f, x = 0f;   // wide gaps: each area camera must not catch the next room
            foreach (var d in defs)
            {
                var t = d.t; float s = t.inhabitantScale; float cellR = cell * s; int n = d.cells; float L = n * cellR, h = L / 2f;   // room grid scales with the size class
                int tiers = 1; float wallH = d.walls ? 3f * s : 1.2f;   // walls scale with the room
                x += (x == 0 ? 0 : gap) + h;
                var root = new GameObject($"HeroRoom_{t.themeName}");
                root.transform.position = new Vector3(x, 0, 0);
                x += h;
                var structure = new GameObject("Structure"); structure.transform.SetParent(root.transform, false);
                for (int cx = 0; cx < n; cx++)
                    for (int cz = 0; cz < n; cz++)
                        Place(P["tile-dungeon-stone-floor"], structure.transform, new Vector3(-h + cellR * (cx + 0.5f), 0, -h + cellR * (cz + 0.5f)), 0);
                int doorCell = n / 2;
                if (d.walls)
                {
                    for (int tier = 0; tier < tiers; tier++)
                        for (int c = 0; c < n; c++)
                        {
                            float u = -h + cellR * (c + 0.5f), y = tier * 3f;
                            Place(P["wall-dungeon-stone"], structure.transform, new Vector3(u, y, h), 180);
                            Place(P[tier == 0 && c == doorCell ? "wall-dungeon-stone-doorway" : "wall-dungeon-stone"], structure.transform, new Vector3(-h, y, u), 90);
                        }
                    foreach (var c in new[] { new Vector2(-h, h), new Vector2(h, h), new Vector2(-h, -h) })
                        for (int tier = 0; tier < tiers; tier++)
                            Place(P["prop-pillar-stone"], structure.transform, new Vector3(c.x, tier * 3f, c.y), 0);
                    float dz = -h + cellR * (doorCell + 0.5f);
                    float hingeLocal = (s_DoorExtendsPlusX ? -0.56f : 0.56f) * s;   // door + doorway scale with the room
                    Place(P["prop-door-wood"], structure.transform, new Vector3(-h, 0, dz - hingeLocal), 90 - 70 * (s_DoorExtendsPlusX ? 1 : -1));
                }
                else
                {
                    // open yard: structural fence sections on the back and left cell edges (one room-grid cell each)
                    for (int c = 0; c < n; c++)
                    {
                        float u = -h + cellR * (c + 0.5f);
                        Place(P["prop-fence-wood"], structure.transform, new Vector3(u, 0, h), 180);
                        if (c != doorCell) Place(P["prop-fence-wood"], structure.transform, new Vector3(-h, 0, u), 90);
                    }
                }
                var props = new GameObject("Props"); props.transform.SetParent(root.transform, false);
                foreach (var it in d.items)
                {
                    if (!P.ContainsKey(it.name)) throw new Exception("hero scene: missing prefab " + it.name);
                    var g = Place(P[it.name], props.transform, new Vector3(it.x * s, it.y * s, it.z * s), it.rot);
                    if (it.tilt != 0) g.transform.localRotation = Quaternion.Euler(it.tilt, it.rot, 0);
                }
                AddRoomExtras(root, t, L, Mathf.Max(wallH, 3f), d.label, inhabitant, font, null, out var fill);
                var room = root.AddComponent<ThemeRoom>(); room.profile = t; room.roomLights = new[] { fill }; room.Apply();
                if (t.themeName == "Hell")
                {
                    // M4 readability: the smithy's dark props lost their silhouettes against the obsidian walls. A warm front fill and an
                    // ember rim light from the back corner (outside roomLights, so ThemeRoom does not re-tint them).
                    var sfill = new GameObject("SmithyFill").AddComponent<Light>(); sfill.transform.SetParent(root.transform, false);
                    sfill.transform.localPosition = new Vector3(0.3f * L, 0.45f * L, -0.35f * L);
                    sfill.type = LightType.Point; sfill.range = 1.6f * L; sfill.intensity = 7f; sfill.color = new Color(1f, 0.86f, 0.72f); sfill.shadows = LightShadows.None;
                    var rim = new GameObject("SmithyRim").AddComponent<Light>(); rim.transform.SetParent(root.transform, false);
                    rim.transform.localPosition = new Vector3(-0.25f * L, 0.5f * L, 0.38f * L);
                    rim.type = LightType.Point; rim.range = 1.6f * L; rim.intensity = 10f; rim.color = new Color(1f, 0.58f, 0.36f); rim.shadows = LightShadows.None;
                }
                var cpos = root.transform.position;
                // far plane just past this room's far corner, so an area camera never shows the neighbouring rooms (M3 QA)
                MakeCamera($"Cam_{t.themeName}", cpos + new Vector3(0.5f * L, 0.5f * L + 0.8f + (tiers - 1) * 2f, -0.9f * L), cpos + new Vector3(-0.08f * L, 0.35f * s + 0.25f, 0.0f), 44f, false).farClipPlane = 2.0f * L + 2f;
                MakeCamera($"Cam_{t.themeName}Close", cpos + new Vector3(0.3f * L, 0.24f * L + 0.4f, -0.5f * L), cpos + new Vector3(0.02f * L, 0.45f * s, 0.12f * L), 40f, false).farClipPlane = 1.6f * L + 2f;
            }
            float span = x;
            MakeCamera("Cam_Overview", new Vector3(span * 0.5f, span * 0.5f, -span * 0.9f), new Vector3(span * 0.5f, 0.6f, 0.8f), 36f, true);
            EditorSceneManager.SaveScene(scene, HeroScene);
            Debug.Log("[OpenKit] saved " + HeroScene);
        }

        // ------------------------------------------------------------------ M3: captures (contact sheets with name labels + hero shots) -> captures/m3
        static void DoM3Captures(Manifest m)
        {
            string outDir = Path.Combine(ProjectRoot, "captures", "m3"); Directory.CreateDirectory(outDir);
            ShaderUtil.allowAsyncCompilation = false;
            var P = new Dictionary<string, GameObject>();
            foreach (var a in m.assets) P[a.name] = AssetDatabase.LoadAssetAtPath<GameObject>(PrefabPath(a)) ?? throw new Exception("prefab missing: " + a.name);
            int MsOrder(string ms) => ms == "M1" ? 0 : ms == "M2" ? 1 : ms == "M3" ? 2 : 3;
            var m3 = m.assets.Where(a => a.milestone == "M3").OrderBy(a => a.name).ToList();
            var all = m.assets.Where(a => a.milestone != "M4").OrderBy(a => MsOrder(a.milestone)).ThenBy(a => a.name.StartsWith("prop-") ? 0 : 1).ThenBy(a => a.name).ToList();
            if (m3.Count == 0) throw new Exception("no M3 assets in the manifest");
            ContactSheet(m3, P, "Dungeon", Path.Combine(outDir, "m3-contact-sheet-dungeon.png"), 6, 480, 400, false);
            ContactSheet(m3, P, "Heaven", Path.Combine(outDir, "m3-contact-sheet-heaven.png"), 6, 480, 400, false);
            ContactSheet(all, P, "Dungeon", Path.Combine(outDir, "catalog-m1-m2-m3.png"), 7, 400, 340, true);
            CaptureRoomScale(P, Path.Combine(outDir, "roomscale.png"));
            CaptureColorSlots(P, Path.Combine(outDir, "colorslots.png"));
            EditorSceneManager.OpenScene(HeroScene, OpenSceneMode.Single);
            foreach (var r in UnityEngine.Object.FindObjectsByType<ThemeRoom>(FindObjectsInactive.Include, FindObjectsSortMode.None)) r.Apply();
            foreach (var cam in UnityEngine.Object.FindObjectsByType<Camera>(FindObjectsInactive.Include, FindObjectsSortMode.None))
                RenderCamera(cam, Path.Combine(outDir, $"hero-{cam.name.Replace("Cam_", "").ToLowerInvariant()}.png"), 1600, 900);
            Debug.Log($"[OpenKit] M3 captures written to {outDir}");
        }

        /// <summary>One framed render per asset (label: name, tris, milestone) composited into a grid PNG.</summary>
        static void ContactSheet(List<ManifestEntry> list, Dictionary<string, GameObject> P, string themeName, string file, int cols, int tw, int th, bool showMilestone)
        {
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            var gm = AssetDatabase.LoadAssetAtPath<Material>($"{DemoDir}/LineupGround.mat");
            Cube("Ground", null, new Vector3(0, -0.05f, 0), new Vector3(60f, 0.1f, 60f), gm);
            var prof = AssetDatabase.LoadAssetAtPath<ThemeProfile>($"{ThemesDir}/{themeName}.asset") ?? throw new Exception("theme missing: " + themeName);
            var room = new GameObject("SheetRoom").AddComponent<ThemeRoom>(); room.profile = prof;
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            const float fov = 30f;
            var cam = MakeCamera("Cam_Sheet", new Vector3(0, 2, -4), Vector3.zero, fov, true);
            cam.nearClipPlane = 0.05f;
            // label rides on the camera, 0.3 m in front, near the bottom edge
            float ld = 0.3f, halfH = Mathf.Tan(fov * 0.5f * Mathf.Deg2Rad) * ld;
            var lab = new GameObject("Label"); lab.transform.SetParent(cam.transform, false);
            lab.transform.localPosition = new Vector3(0, -halfH * 0.8f, ld);
            var tm = lab.AddComponent<TextMesh>(); tm.font = font; tm.fontSize = 64; tm.characterSize = 0.0048f * ld * (showMilestone ? 0.95f : 1f);
            tm.anchor = TextAnchor.MiddleCenter; tm.alignment = TextAlignment.Center; tm.color = new Color(0.95f, 0.95f, 0.95f);
            lab.GetComponent<MeshRenderer>().sharedMaterial = font.material;
            // dark unlit strip behind the label so it stays readable over bright emissive props
            var strip = GameObject.CreatePrimitive(PrimitiveType.Quad);
            UnityEngine.Object.DestroyImmediate(strip.GetComponent<Collider>());
            strip.name = "LabelStrip"; strip.transform.SetParent(cam.transform, false);
            strip.transform.localPosition = new Vector3(0, -halfH * 0.83f, ld + 0.002f);
            strip.transform.localScale = new Vector3(2.2f * halfH * tw / th, halfH * 0.34f, 1f);
            var stripMat = new Material(Shader.Find("Universal Render Pipeline/Unlit")) { hideFlags = HideFlags.DontSave };
            stripMat.SetColor("_BaseColor", new Color(0.035f, 0.035f, 0.05f));
            var sr = strip.GetComponent<MeshRenderer>(); sr.sharedMaterial = stripMat; sr.shadowCastingMode = ShadowCastingMode.Off; sr.receiveShadows = false;
            int rows = (list.Count + cols - 1) / cols;
            var sheet = new Texture2D(cols * tw, rows * th, TextureFormat.RGB24, false);
            var bg = Enumerable.Repeat(new Color32(13, 13, 18, 255), sheet.width * sheet.height).ToArray();
            sheet.SetPixels32(bg);
            var rt = new RenderTexture(tw, th, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB) { antiAliasing = 4 };
            rt.Create();
            var tile = new Texture2D(tw, th, TextureFormat.RGB24, false);
            var dir = new Vector3(0f, 0.62f, -1f).normalized;   // sun comes from -Z, so view from -Z; props turned 155 deg to face the camera
            for (int i = 0; i < list.Count; i++)
            {
                var a = list[i];
                var go = Place(P[a.name], room.transform, Vector3.zero, 155f);
                room.Apply();
                Bounds B() { var rs = go.GetComponentsInChildren<Renderer>(); var bb = rs[0].bounds; foreach (var r in rs) bb.Encapsulate(r.bounds); return bb; }
                var b = B();
                if (b.min.y < -1e-4f) { go.transform.position += Vector3.up * -b.min.y; b = B(); }   // floor tiles sit on the ground for the photo
                float radius = Mathf.Max(b.extents.magnitude, 0.2f);
                float dist = radius / Mathf.Sin(fov * 0.5f * Mathf.Deg2Rad) * 1.2f;
                var target = b.center - Vector3.up * radius * 0.26f;   // keep the prop clear of the label strip
                cam.transform.position = target + dir * dist; cam.transform.LookAt(target);
                cam.farClipPlane = dist + 60f;
                tm.text = showMilestone ? $"{a.name}\n{a.milestone}  -  {a.tris} tris" : $"{a.name}\n{a.tris} tris";
                cam.targetTexture = rt; cam.aspect = (float)tw / th;
                for (int k = 0; k < 3; k++) cam.Render();
                var prev = RenderTexture.active; RenderTexture.active = rt;
                tile.ReadPixels(new Rect(0, 0, tw, th), 0, 0); tile.Apply();
                RenderTexture.active = prev; cam.targetTexture = null;
                int c = i % cols, r = i / cols;
                sheet.SetPixels32(c * tw, (rows - 1 - r) * th, tw, th, tile.GetPixels32());
                UnityEngine.Object.DestroyImmediate(go);
            }
            // 2 px grid lines between tiles
            var line = new Color32(40, 42, 52, 255);
            for (int c = 1; c < cols; c++) for (int y = 0; y < sheet.height; y++) { sheet.SetPixel(c * tw, y, line); sheet.SetPixel(c * tw - 1, y, line); }
            for (int r = 1; r < rows; r++) for (int xx = 0; xx < sheet.width; xx++) { sheet.SetPixel(xx, r * th, line); sheet.SetPixel(xx, r * th - 1, line); }
            sheet.Apply();
            File.WriteAllBytes(file, sheet.EncodeToPNG());
            UnityEngine.Object.DestroyImmediate(sheet); UnityEngine.Object.DestroyImmediate(tile); rt.Release(); UnityEngine.Object.DestroyImmediate(rt);
            UnityEngine.Object.DestroyImmediate(stripMat);
            Debug.Log($"[OpenKit] contact sheet {file} ({list.Count} assets, {themeName})");
        }

        // ------------------------------------------------------------------ M4: monsters (rigged), monster scene, M4 captures
        static Mesh MeshOf(GameObject go)
        {
            var mf = go.GetComponentInChildren<MeshFilter>(true);
            if (mf && mf.sharedMesh) return mf.sharedMesh;
            var smr = go.GetComponentInChildren<SkinnedMeshRenderer>(true);
            return smr ? smr.sharedMesh : null;
        }

        static List<AnimationClip> ModelClips(ManifestEntry a) =>
            AssetDatabase.LoadAllAssetsAtPath(ModelPath(a)).OfType<AnimationClip>().Where(c => !c.name.StartsWith("__preview__")).OrderBy(c => c.name == "idle" ? 0 : 1).ThenBy(c => c.name).ToList();

        /// <summary>Animator controller per rigged monster: default state "idle", optional "walk" behind a bool parameter "walk".</summary>
        static RuntimeAnimatorController EnsureController(ManifestEntry a)
        {
            string cp = $"{Root}/Prefabs/{Cat(a)}/{a.name}.controller";
            AssetDatabase.DeleteAsset(cp);
            var ctrl = UnityEditor.Animations.AnimatorController.CreateAnimatorControllerAtPath(cp);
            var sm = ctrl.layers[0].stateMachine;
            var clips = ModelClips(a);
            if (clips.Count == 0) throw new Exception($"{a.name}: rigged but the FBX has no animation clips");
            var states = new Dictionary<string, UnityEditor.Animations.AnimatorState>();
            foreach (var c in clips)
            {
                var st = sm.AddState(c.name); st.motion = c; states[c.name] = st;
                if (c.name == "idle") sm.defaultState = st;
            }
            if (states.TryGetValue("idle", out var idle) && states.TryGetValue("walk", out var walk))
            {
                ctrl.AddParameter("walk", AnimatorControllerParameterType.Bool);
                var t1 = idle.AddTransition(walk); t1.hasExitTime = false; t1.duration = 0.15f; t1.AddCondition(UnityEditor.Animations.AnimatorConditionMode.If, 0, "walk");
                var t2 = walk.AddTransition(idle); t2.hasExitTime = false; t2.duration = 0.15f; t2.AddCondition(UnityEditor.Animations.AnimatorConditionMode.IfNot, 0, "walk");
            }
            AssetDatabase.SaveAssets();
            return ctrl;
        }

        static void ValidateMonster(ManifestEntry a, GameObject model, GameObject pf, Action<string> E)
        {
            if (!a.rigged) { E("monster is not rigged"); return; }
            var smrs = model.GetComponentsInChildren<SkinnedMeshRenderer>(true);
            if (smrs.Length != 1) { E($"{smrs.Length} SkinnedMeshRenderers in the model (expected 1)"); return; }
            var smr = smrs[0];
            if (smr.bones.Length != a.bones) E($"{smr.bones.Length} bones in Unity != {a.bones} from Blender");
            if (smr.bones.Any(b => !b)) E("missing bone transforms");
            var bpv = smr.sharedMesh.GetBonesPerVertex();
            if (bpv.Length != smr.sharedMesh.vertexCount || bpv.Any(n => n == 0)) E("vertices without bone weights");
            var clips = ModelClips(a);
            foreach (var want in a.clips ?? new string[0])
            {
                var c = clips.FirstOrDefault(x => x.name == want);
                if (!c) { E($"clip '{want}' missing in Unity (clips: {string.Join(",", clips.Select(x => x.name))})"); continue; }
                if (c.length < 0.2f) E($"clip '{want}' too short ({c.length:F2}s)");
                if (!c.isLooping) E($"clip '{want}' does not loop");
            }
            var anim = pf.GetComponent<Animator>();
            if (!anim || !anim.runtimeAnimatorController) E("prefab has no Animator with a controller");
            else
            {
                if (anim.applyRootMotion) E("Animator applies root motion (would fight room scaling / placement)");
                var names = anim.runtimeAnimatorController.animationClips.Select(c => c.name).ToList();
                if (!names.Contains("idle")) E("controller has no idle clip");
            }
            // clips must animate bones only, never the root (the root carries the room scale)
            foreach (var c in clips)
                foreach (var bnd in AnimationUtility.GetCurveBindings(c))
                    if (string.IsNullOrEmpty(bnd.path)) E($"clip '{c.name}' animates the root ({bnd.propertyName})");
        }

        const string MonsterScene = DemoDir + "/OpenKit3D-M4Monsters.unity";
        static readonly string[] MonsterOrder = { "monster-golem-stone", "monster-construct-clockwork-hound", "monster-mimic-chest", "monster-skeleton-warrior", "monster-giant-rat" };

        static List<string> MonsterNames(Dictionary<string, GameObject> P)
        {
            var list = MonsterOrder.Where(P.ContainsKey).ToList();
            list.AddRange(P.Keys.Where(k => k.StartsWith("monster-") && !list.Contains(k)).OrderBy(k => k));
            return list;
        }

        /// <summary>Monster lineup: the same monster prefabs in a halfling, a human and a giant room (Dungeon theme), with the fixed 1.8 m human reference.</summary>
        static void BuildMonsterScene(List<ThemeProfile> themes, Dictionary<string, GameObject> P)
        {
            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            var gm = AssetDatabase.LoadAssetAtPath<Material>($"{DemoDir}/LineupGround.mat");
            Cube("Ground", null, new Vector3(0, -0.45f, 0), new Vector3(300f, 0.1f, 300f), gm);
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            var prof = themes.First(t => t.themeName == "Dungeon");
            var inhabitant = InhabitantMat(); var humanRef = RefMat("HumanRef", new Color(0.72f, 0.72f, 0.72f));
            var names = MonsterNames(P);
            if (names.Count == 0) throw new Exception("monster scene: no monster prefabs");
            float cell = OpenKitConst.GridCell, gap = 2.5f, x = 0f; int nx = 6, nz = 3;
            foreach (var (size, label) in RoomSizes)
            {
                float s = OpenKitConst.ScaleOf(size, 1f), cr = cell * s, Lx = nx * cr, Lz = nz * cr, hx = Lx / 2f, hz = Lz / 2f;
                x += (x == 0 ? 0 : gap) + hx;
                var root = new GameObject($"MonsterRoom_{size}"); root.transform.position = new Vector3(x, 0, 0);
                x += hx;
                var st = new GameObject("Structure"); st.transform.SetParent(root.transform, false);
                for (int cx = 0; cx < nx; cx++) for (int cz = 0; cz < nz; cz++)
                    Place(P["tile-dungeon-stone-floor"], st.transform, new Vector3(-hx + cr * (cx + 0.5f), 0, -hz + cr * (cz + 0.5f)), 0);
                for (int c = 0; c < nx; c++)
                    Place(P["wall-dungeon-stone"], st.transform, new Vector3(-hx + cr * (c + 0.5f), 0, hz), 180);
                var mons = new GameObject("Monsters"); mons.transform.SetParent(root.transform, false);
                // monsters in a row, spaced by their footprint (in room units), facing the camera (+Z front -> rotate 180 to face -Z)
                var widths = names.Select(n => { var b = MeshOf(P[n]).bounds; return Mathf.Max(b.size.x, 0.5f); }).ToList();
                float total = widths.Sum() + 0.45f * (names.Count - 1), u = -total / 2f;
                for (int i = 0; i < names.Count; i++)
                {
                    var g = Place(P[names[i]], mons.transform, new Vector3((u + widths[i] / 2f) * s, 0, 0.1f * s), 200f);
                    u += widths[i] + 0.45f;
                    if (size == RoomSize.Human)
                        WorldLabel(root.transform, names[i].Replace("monster-", ""), new Vector3(g.transform.localPosition.x, 0.03f, -hz + 0.35f), 0.03f, Color.white, font, Quaternion.Euler(70f, 0, 0));
                }
                var refs = new GameObject("References"); refs.transform.SetParent(root.transform, false);
                Capsule("Inhabitant_1.8xS", refs.transform, new Vector3(-hx + 0.5f * s, 0, -hz + 0.9f * s), 1.8f * s, inhabitant);
                Capsule("Human_1.8m", refs.transform, new Vector3(hx + 0.6f, 0, -hz + 0.4f), 1.8f, humanRef);
                WorldLabel(root.transform, label, new Vector3(0, 0.05f, -hz - 0.8f), 0.05f, Color.white, font, Quaternion.Euler(70f, 0, 0));
                var room = root.AddComponent<ThemeRoom>(); room.profile = prof; room.roomSize = size; room.Apply();
            }
            float span = x;
            WorldLabel(null, "M4 monsters (rigged; press Play for the idle clips)     grey capsule = human reference 1.8 m     cyan = room inhabitant 1.8 m x room scale     Dungeon theme",
                new Vector3(span * 0.5f, 0.05f, -8.0f), 0.045f, new Color(0.85f, 0.85f, 0.85f), font, Quaternion.Euler(70f, 0, 0));
            MakeCamera("Cam_MonsterLineup", new Vector3(span * 0.5f, 13.5f, -24f), new Vector3(span * 0.5f, 1.6f, 1.0f), 40f, true);
            EditorSceneManager.SaveScene(scene, MonsterScene);
            Debug.Log("[OpenKit] saved " + MonsterScene + $" ({names.Count} monsters x 3 room sizes)");
        }

        static readonly (string name, Color p, Color s, Color t)[] MonsterCombos =
        {
            ("Ash",     new Color(0.30f, 0.30f, 0.33f), new Color(0.62f, 0.20f, 0.16f), new Color(0.95f, 0.78f, 0.25f)),
            ("Moss",    new Color(0.30f, 0.42f, 0.22f), new Color(0.55f, 0.45f, 0.30f), new Color(0.75f, 0.82f, 0.86f)),
            ("Frost",   new Color(0.72f, 0.82f, 0.92f), new Color(0.20f, 0.30f, 0.52f), new Color(0.85f, 0.35f, 0.62f)),
        };

        /// <summary>Monster colour-slot grid: one row per monster, one column per custom colour combo (human room, Dungeon theme).</summary>
        static void CaptureMonsterColorSlots(Dictionary<string, GameObject> P, string file)
        {
            string Hex(Color c) => "#" + ColorUtility.ToHtmlStringRGB(c);
            var names = MonsterNames(P);
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            var gm = AssetDatabase.LoadAssetAtPath<Material>($"{DemoDir}/LineupGround.mat");
            Cube("Ground", null, new Vector3(0, -0.05f, 0), new Vector3(200f, 0.1f, 200f), gm);
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            var prof = AssetDatabase.LoadAssetAtPath<ThemeProfile>($"{ThemesDir}/Dungeon.asset") ?? throw new Exception("theme missing: Dungeon");
            var roomGo = new GameObject("SlotRoom"); var room = roomGo.AddComponent<ThemeRoom>(); room.profile = prof; room.roomSize = RoomSize.Human;
            const float fov = 30f; const int tw = 560, th = 460;
            var cam = MakeCamera("Cam_Slots", new Vector3(0, 2, -4), Vector3.zero, fov, true); cam.nearClipPlane = 0.05f;
            float ld = 0.3f, halfH = Mathf.Tan(fov * 0.5f * Mathf.Deg2Rad) * ld;
            var lab = new GameObject("Label"); lab.transform.SetParent(cam.transform, false); lab.transform.localPosition = new Vector3(0, -halfH * 0.83f, ld);
            var tm = lab.AddComponent<TextMesh>(); tm.font = font; tm.fontSize = 64; tm.characterSize = 0.0036f * ld;
            tm.anchor = TextAnchor.MiddleCenter; tm.alignment = TextAlignment.Center; tm.color = new Color(0.95f, 0.95f, 0.95f);
            lab.GetComponent<MeshRenderer>().sharedMaterial = font.material;
            var strip = GameObject.CreatePrimitive(PrimitiveType.Quad); UnityEngine.Object.DestroyImmediate(strip.GetComponent<Collider>());
            strip.transform.SetParent(cam.transform, false); strip.transform.localPosition = new Vector3(0, -halfH * 0.85f, ld + 0.002f);
            strip.transform.localScale = new Vector3(2.2f * halfH * tw / th, halfH * 0.32f, 1f);
            var stripMat = new Material(Shader.Find("Universal Render Pipeline/Unlit")) { hideFlags = HideFlags.DontSave }; stripMat.SetColor("_BaseColor", new Color(0.035f, 0.035f, 0.05f));
            var sr = strip.GetComponent<MeshRenderer>(); sr.sharedMaterial = stripMat; sr.shadowCastingMode = ShadowCastingMode.Off;
            int cols = MonsterCombos.Length + 1, rows = names.Count;
            var sheet = new Texture2D(cols * tw, rows * th, TextureFormat.RGB24, false);
            var rt = new RenderTexture(tw, th, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB) { antiAliasing = 4 }; rt.Create();
            var tile = new Texture2D(tw, th, TextureFormat.RGB24, false);
            var dir = new Vector3(0.25f, 0.5f, -1f).normalized;
            for (int r = 0; r < rows; r++)
            {
                var go = Place(P[names[r]], roomGo.transform, Vector3.zero, 160f);
                var ta = go.GetComponent<ThemeAdaptive>();
                room.Apply();
                var rends = go.GetComponentsInChildren<Renderer>(); var b = rends[0].bounds; foreach (var rr in rends) b.Encapsulate(rr.bounds);
                float radius = Mathf.Max(b.extents.magnitude, 0.2f), dist = radius / Mathf.Sin(fov * 0.5f * Mathf.Deg2Rad) * 1.15f;
                var target = b.center - Vector3.up * radius * 0.22f;
                cam.transform.position = target + dir * dist; cam.transform.LookAt(target); cam.farClipPlane = dist + 60f;
                for (int c = 0; c < cols; c++)
                {
                    if (c == 0) { ta.primaryColor.enabled = ta.secondaryColor.enabled = ta.tertiaryColor.enabled = false; tm.text = $"{names[r]}\ntheme default (Dungeon)"; }
                    else
                    {
                        var co = MonsterCombos[c - 1];
                        ta.primaryColor.enabled = ta.secondaryColor.enabled = ta.tertiaryColor.enabled = true;
                        ta.primaryColor.color = co.p; ta.secondaryColor.color = co.s; ta.tertiaryColor.color = co.t;
                        tm.text = $"{names[r]}  -  {co.name}\nP {Hex(co.p)}  S {Hex(co.s)}  T {Hex(co.t)}";
                    }
                    ta.Apply();
                    cam.targetTexture = rt; cam.aspect = (float)tw / th;
                    for (int k = 0; k < 3; k++) cam.Render();
                    var prev = RenderTexture.active; RenderTexture.active = rt;
                    tile.ReadPixels(new Rect(0, 0, tw, th), 0, 0); tile.Apply(); RenderTexture.active = prev; cam.targetTexture = null;
                    sheet.SetPixels32(c * tw, (rows - 1 - r) * th, tw, th, tile.GetPixels32());
                }
                UnityEngine.Object.DestroyImmediate(go);
            }
            GridLines(sheet, cols, rows, tw, th);
            File.WriteAllBytes(file, sheet.EncodeToPNG());
            UnityEngine.Object.DestroyImmediate(sheet); UnityEngine.Object.DestroyImmediate(tile); rt.Release(); UnityEngine.Object.DestroyImmediate(rt); UnityEngine.Object.DestroyImmediate(stripMat);
            Debug.Log($"[OpenKit] monster colour-slot grid {file}");
        }

        static void GridLines(Texture2D sheet, int cols, int rows, int tw, int th)
        {
            var line = new Color32(40, 42, 52, 255);
            for (int c = 1; c < cols; c++) for (int y = 0; y < sheet.height; y++) { sheet.SetPixel(c * tw, y, line); sheet.SetPixel(c * tw - 1, y, line); }
            for (int r = 1; r < rows; r++) for (int xx = 0; xx < sheet.width; xx++) { sheet.SetPixel(xx, r * th, line); sheet.SetPixel(xx, r * th - 1, line); }
            sheet.Apply();
        }

        /// <summary>Animation evidence: every monster's clips sampled at 4 points in time (edit-mode AnimationClip.SampleAnimation).</summary>
        static void CaptureMonsterClips(Manifest m, Dictionary<string, GameObject> P, string file)
        {
            var rows = new List<(ManifestEntry a, AnimationClip c)>();
            foreach (var n in MonsterNames(P))
            {
                var a = m.assets.First(x => x.name == n);
                foreach (var c in ModelClips(a)) rows.Add((a, c));
            }
            if (rows.Count == 0) return;
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            var gm = AssetDatabase.LoadAssetAtPath<Material>($"{DemoDir}/LineupGround.mat");
            Cube("Ground", null, new Vector3(0, -0.05f, 0), new Vector3(200f, 0.1f, 200f), gm);
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            var prof = AssetDatabase.LoadAssetAtPath<ThemeProfile>($"{ThemesDir}/Heaven.asset");
            var roomGo = new GameObject("ClipRoom"); var room = roomGo.AddComponent<ThemeRoom>(); room.profile = prof; room.roomSize = RoomSize.Human;
            const float fov = 30f; const int tw = 360, th = 300, cols = 4;
            var cam = MakeCamera("Cam_Clips", new Vector3(0, 2, -4), Vector3.zero, fov, true); cam.nearClipPlane = 0.05f;
            float ld = 0.3f, halfH = Mathf.Tan(fov * 0.5f * Mathf.Deg2Rad) * ld;
            var lab = new GameObject("Label"); lab.transform.SetParent(cam.transform, false); lab.transform.localPosition = new Vector3(0, -halfH * 0.86f, ld);
            var tm = lab.AddComponent<TextMesh>(); tm.font = font; tm.fontSize = 64; tm.characterSize = 0.0036f * ld;
            tm.anchor = TextAnchor.MiddleCenter; tm.alignment = TextAlignment.Center; tm.color = new Color(0.95f, 0.95f, 0.95f);
            lab.GetComponent<MeshRenderer>().sharedMaterial = font.material;
            var sheet = new Texture2D(cols * tw, rows.Count * th, TextureFormat.RGB24, false);
            var rt = new RenderTexture(tw, th, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB) { antiAliasing = 4 }; rt.Create();
            var tile = new Texture2D(tw, th, TextureFormat.RGB24, false);
            var dir = new Vector3(0.9f, 0.45f, -0.6f).normalized;   // side-ish view so leg swings and jaw/tail motion read
            for (int r = 0; r < rows.Count; r++)
            {
                var (a, clip) = rows[r];
                var go = Place(P[a.name], roomGo.transform, Vector3.zero, 180f);
                room.Apply();
                var rends = go.GetComponentsInChildren<Renderer>(); var b = rends[0].bounds; foreach (var rr in rends) b.Encapsulate(rr.bounds);
                float radius = Mathf.Max(b.extents.magnitude, 0.2f), dist = radius / Mathf.Sin(fov * 0.5f * Mathf.Deg2Rad) * 1.25f;
                var target = b.center;
                cam.transform.position = target + dir * dist; cam.transform.LookAt(target); cam.farClipPlane = dist + 60f;
                for (int c = 0; c < cols; c++)
                {
                    float t = clip.length * c / cols;
                    clip.SampleAnimation(go, t);
                    tm.text = $"{a.name.Replace("monster-", "")}  {clip.name}  t={t:F2}s";
                    cam.targetTexture = rt; cam.aspect = (float)tw / th;
                    for (int k = 0; k < 3; k++) cam.Render();
                    var prev = RenderTexture.active; RenderTexture.active = rt;
                    tile.ReadPixels(new Rect(0, 0, tw, th), 0, 0); tile.Apply(); RenderTexture.active = prev; cam.targetTexture = null;
                    sheet.SetPixels32(c * tw, (rows.Count - 1 - r) * th, tw, th, tile.GetPixels32());
                }
                UnityEngine.Object.DestroyImmediate(go);
            }
            GridLines(sheet, cols, rows.Count, tw, th);
            File.WriteAllBytes(file, sheet.EncodeToPNG());
            UnityEngine.Object.DestroyImmediate(sheet); UnityEngine.Object.DestroyImmediate(tile); rt.Release(); UnityEngine.Object.DestroyImmediate(rt);
            Debug.Log($"[OpenKit] monster clip frames {file}");
        }

        /// <summary>Before/after shots for the M4 fixes (sack silhouette + readability). tag = "before" | "after".</summary>
        static void DoM4Compare(string tag)
        {
            string outDir = Path.Combine(ProjectRoot, "captures", "m4"); Directory.CreateDirectory(outDir);
            ShaderUtil.allowAsyncCompilation = false;
            var P = new Dictionary<string, GameObject>();
            foreach (var cat in Categories)
                foreach (var guid in AssetDatabase.FindAssets("t:Prefab", new[] { $"{Root}/Prefabs/{cat}" }))
                {
                    var g = AssetDatabase.LoadAssetAtPath<GameObject>(AssetDatabase.GUIDToAssetPath(guid));
                    if (g) P[g.name] = g;
                }
            ManifestEntry fake(string n) { var me = MeshOf(P[n]); int tr = 0; if (me) for (int i = 0; i < me.subMeshCount; i++) tr += (int)(me.GetIndexCount(i) / 3); return new ManifestEntry { name = n, tris = tr, category = "Props" }; }
            ContactSheet(new List<ManifestEntry> { fake("prop-sack-grain") }, P, "Dungeon", Path.Combine(outDir, $"{tag}-sack-dungeon.png"), 1, 900, 700, false);
            ContactSheet(new List<ManifestEntry> { fake("prop-sack-grain") }, P, "Heaven", Path.Combine(outDir, $"{tag}-sack-heaven.png"), 1, 900, 700, false);
            ContactSheet(new List<ManifestEntry> { fake("prop-stump-axe") }, P, "Dungeon", Path.Combine(outDir, $"{tag}-stump-axe.png"), 1, 900, 700, false);
            TorchWallShot(P, "Hell", Path.Combine(outDir, $"{tag}-torch-wall-hell.png"));
            TorchWallShot(P, "Dungeon", Path.Combine(outDir, $"{tag}-torch-wall-dungeon.png"));
            EditorSceneManager.OpenScene(HeroScene, OpenSceneMode.Single);
            foreach (var r in UnityEngine.Object.FindObjectsByType<ThemeRoom>(FindObjectsInactive.Include, FindObjectsSortMode.None)) r.Apply();
            foreach (var (camName, fn) in new[] { ("Cam_Hell", "smithy"), ("Cam_HellClose", "smithy-close"), ("Cam_Heaven", "yard"), ("Cam_HeavenClose", "yard-close") })
            {
                var cam = GameObject.Find(camName)?.GetComponent<Camera>();
                if (cam) RenderCamera(cam, Path.Combine(outDir, $"{tag}-{fn}.png"), 1600, 900);
            }
            Debug.Log($"[OpenKit] M4 {tag} shots written to {outDir}");
        }

        /// <summary>A short run of wall with two wall torches, lit mostly by the torches (mortar-glow check).</summary>
        static void TorchWallShot(Dictionary<string, GameObject> P, string themeName, string file)
        {
            EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            SetupEnvironment("DemoPostFX");
            GameObject.Find("Sun").GetComponent<Light>().intensity = 0.25f;
            RenderSettings.ambientSkyColor *= 0.6f; RenderSettings.ambientEquatorColor *= 0.6f;
            var prof = AssetDatabase.LoadAssetAtPath<ThemeProfile>($"{ThemesDir}/{themeName}.asset");
            var root = new GameObject("TorchWall");
            for (int i = -2; i <= 2; i++)
            {
                Place(P["wall-dungeon-stone"], root.transform, new Vector3(i * 1.5f, 0, 0), 0);
                Place(P["tile-dungeon-stone-floor"], root.transform, new Vector3(i * 1.5f, 0, 0.75f + 0.17f), 0);
                Place(P["tile-dungeon-stone-floor"], root.transform, new Vector3(i * 1.5f, 0, 2.25f + 0.17f), 0);
            }
            foreach (float tx in new[] { -1.5f, 1.5f }) Place(P["prop-torch-wall"], root.transform, new Vector3(tx, 1.6f, 0.17f), 0);
            var room = root.AddComponent<ThemeRoom>(); room.profile = prof; room.roomSize = RoomSize.Human; room.Apply();
            var cam = MakeCamera("Cam_TorchWall", new Vector3(1.2f, 1.9f, 4.6f), new Vector3(0, 1.45f, 0), 45f, true);
            RenderCamera(cam, file, 1600, 900);
        }

        static void DoM4Captures(Manifest m)
        {
            string outDir = Path.Combine(ProjectRoot, "captures", "m4"); Directory.CreateDirectory(outDir);
            ShaderUtil.allowAsyncCompilation = false;
            var P = new Dictionary<string, GameObject>();
            foreach (var a in m.assets) P[a.name] = AssetDatabase.LoadAssetAtPath<GameObject>(PrefabPath(a)) ?? throw new Exception("prefab missing: " + a.name);
            var mons = m.assets.Where(a => a.category == "Monsters").OrderBy(a => Array.IndexOf(MonsterOrder, a.name) is int k && k >= 0 ? k : 99).ToList();
            if (mons.Count == 0) throw new Exception("no monsters in the manifest");
            ContactSheet(mons, P, "Dungeon", Path.Combine(outDir, "m4-contact-sheet-dungeon.png"), mons.Count, 480, 440, false);
            ContactSheet(mons, P, "Undead", Path.Combine(outDir, "m4-contact-sheet-undead.png"), mons.Count, 480, 440, false);
            EditorSceneManager.OpenScene(MonsterScene, OpenSceneMode.Single);
            foreach (var r in UnityEngine.Object.FindObjectsByType<ThemeRoom>(FindObjectsInactive.Include, FindObjectsSortMode.None)) r.Apply();
            RenderCamera(GameObject.Find("Cam_MonsterLineup").GetComponent<Camera>(), Path.Combine(outDir, "monster-lineup-roomsizes.png"), 2400, 1100);
            CaptureMonsterColorSlots(P, Path.Combine(outDir, "monster-colorslots.png"));
            CaptureMonsterClips(m, P, Path.Combine(outDir, "monster-clips.png"));
            int MsOrder(string ms) => ms == "M1" ? 0 : ms == "M2" ? 1 : ms == "M3" ? 2 : ms == "M4" ? 3 : 4;
            var all = m.assets.OrderBy(a => MsOrder(a.milestone)).ThenBy(a => a.name.StartsWith("prop-") ? 0 : 1).ThenBy(a => a.name).ToList();
            ContactSheet(all, P, "Dungeon", Path.Combine(outDir, "catalog-m1-m4.png"), 8, 380, 330, true);
            DoM4Compare("after");
            Debug.Log($"[OpenKit] M4 captures written to {outDir}");
        }

        // ------------------------------------------------------------------ package
        static void ExportPackage()
        {
            AssetDatabase.SaveAssets();
            string dir = Path.Combine(ProjectRoot, "Builds"); Directory.CreateDirectory(dir);
            string pkg = Path.Combine(dir, $"OpenKit3D-{Milestone}.unitypackage");
            AssetDatabase.ExportPackage(new[] { Root }, pkg, ExportPackageOptions.Recurse);
            Debug.Log($"[OpenKit] exported {pkg} ({new FileInfo(pkg).Length / 1024} KB)");
        }

        // ------------------------------------------------------------------ screenshots
        static void DoScreenshots()
        {
            string outDir = Path.Combine(ProjectRoot, "Screenshots"); Directory.CreateDirectory(outDir);
            ShaderUtil.allowAsyncCompilation = false;
            foreach (var (scenePath, prefix) in new[] { (DemoScene, "demo"), (LineupScene, "lineup"), (ModularScene, "modular") })
            {
                EditorSceneManager.OpenScene(scenePath, OpenSceneMode.Single);
                foreach (var r in UnityEngine.Object.FindObjectsByType<ThemeRoom>(FindObjectsInactive.Include, FindObjectsSortMode.None)) r.Apply();
                foreach (var cam in UnityEngine.Object.FindObjectsByType<Camera>(FindObjectsInactive.Include, FindObjectsSortMode.None))
                {
                    string name = cam.name.Replace("Cam_", "").ToLowerInvariant();
                    string file = Path.Combine(outDir, prefix == "lineup" ? "lineup-themes.png" : $"{prefix}-{name}.png");
                    RenderCamera(cam, file, 1600, 900);
                }
            }
            RenderCatalogPerTheme(outDir);
            DoM3Captures(LoadManifest());
            DoM4Captures(LoadManifest());
        }

        static void RenderCamera(Camera cam, string file, int w, int h)
        {
            var rt = new RenderTexture(w, h, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB) { antiAliasing = 4 };
            rt.Create();
            bool wasEnabled = cam.enabled;
            cam.enabled = true;
            cam.targetTexture = rt;
            cam.aspect = (float)w / h;
            for (int i = 0; i < 3; i++) cam.Render();   // warm-up frames (shadows, shader variants)
            var prev = RenderTexture.active;
            RenderTexture.active = rt;
            var tex = new Texture2D(w, h, TextureFormat.RGB24, false);
            tex.ReadPixels(new Rect(0, 0, w, h), 0, 0); tex.Apply();
            RenderTexture.active = prev;
            File.WriteAllBytes(file, tex.EncodeToPNG());
            cam.targetTexture = null; cam.enabled = wasEnabled;
            UnityEngine.Object.DestroyImmediate(tex); rt.Release(); UnityEngine.Object.DestroyImmediate(rt);
            Debug.Log($"[OpenKit] screenshot {file}");
        }
    }
}
