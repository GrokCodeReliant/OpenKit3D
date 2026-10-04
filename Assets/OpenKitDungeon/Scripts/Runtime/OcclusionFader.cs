using System.Collections.Generic;
using UnityEngine;

namespace OpenKitDungeon
{
    /// <summary>
    /// See-through fade for walls, pillars, roofs and cliffs between the camera and the hero.
    /// The fade is a MaterialPropertyBlock on <see cref="Property"/>. Shared materials are not instanced per hit.
    /// </summary>
    [DefaultExecutionOrder(500)]
    public class OcclusionFader : MonoBehaviour
    {
        public const string ShaderName = "OpenKitDungeon/OccludeFadeLit";
        public const string Keyword = "_OCCLUDE_FADE_ON";
        public const string Property = "_OccludeFade";
        public static readonly int PropertyId = Shader.PropertyToID(Property);

        public const float FadeInSeconds = 0.15f;
        public const float FadeOutSeconds = 0.15f;
        public const float FadedValue = 0.32f;

        public Transform hero;
        public LayerMask levelMask;
        public float castRadius = 0.22f;

        static readonly Dictionary<int, Material> Copies = new Dictionary<int, Material>();
        static readonly Dictionary<int, float> Values = new Dictionary<int, float>();
        static MaterialPropertyBlock Block;
        static Shader fadeShader;

        readonly List<Renderer> touching = new List<Renderer>();
        readonly List<Renderer> tracked = new List<Renderer>();
        readonly HashSet<int> touchIds = new HashSet<int>();
        int adoptPasses;
        bool valuesReady;

        public static float FadeOf(Renderer renderer)
        {
            if (renderer == null) return 1f;
            if (Values.TryGetValue(renderer.GetInstanceID(), out float value)) return value;
            var mat = renderer.sharedMaterial;
            if (mat != null && mat.HasProperty(PropertyId)) return mat.GetFloat(PropertyId);
            return 1f;
        }
        // Assign hero and levelMask from the consuming scene or prefab.
        void Start()
        {
            AdoptScene();
        }

        void LateUpdate()
        {
            if (adoptPasses < 12)
            {
                AdoptScene();
                adoptPasses++;
            }
            Collect();
            float dt = Time.deltaTime;
            if (dt <= 0f) return;
            FadeToward(dt);
        }

        static Shader FadeShader()
        {
            if (fadeShader != null) return fadeShader;
            var seed = Resources.Load<Material>("M_OccludeFadeLit");
            if (seed != null && seed.shader != null && seed.shader.name == ShaderName)
                fadeShader = seed.shader;
            if (fadeShader == null)
                fadeShader = Shader.Find(ShaderName);
            return fadeShader;
        }

        void AdoptScene()
        {
            if (FadeShader() == null) return;
            if (!valuesReady)
            {
                Values.Clear();
                valuesReady = true;
            }
            var renderers = Object.FindObjectsByType<Renderer>(FindObjectsInactive.Exclude, FindObjectsSortMode.None);
            for (int i = 0; i < renderers.Length; i++)
            {
                var r = renderers[i];
                if (r == null || !CanFade(r.transform)) continue;
                Adopt(r);
            }
        }

        public static bool HasMarker(Transform t)
        {
            while (t != null)
            {
                if (t.GetComponent<OccluderFade>() != null) return true;
                t = t.parent;
            }
            return false;
        }

        /// <summary>Named character and prop exclusions never fade, even when marked.</summary>
        public static bool NeverFades(Transform t)
        {
            if (t == null) return true;
            if (HasBehaviour(t, "LevelPortal")) return true;
            Transform walk = t;
            while (walk != null)
            {
                string n = walk.name;
                if (Has(n, "lever") || Has(n, "loot")) return true;
                walk = walk.parent;
            }
            return false;
        }

        static bool HasBehaviour(Transform t, string typeName)
        {
            var all = t.GetComponentsInParent<MonoBehaviour>();
            for (int i = 0; i < all.Length; i++)
            {
                if (all[i] != null && all[i].GetType().Name == typeName) return true;
            }
            return false;
        }

        /// <summary>Marked, or the name backup, and not a never-fade actor.</summary>
        public static bool CanFade(Transform t)
        {
            if (t == null || NeverFades(t)) return false;
            return HasMarker(t) || IsStructural(t);
        }

        public static bool CanFade(Collider col)
        {
            if (col == null) return false;
            if (CanFade(col.transform)) return true;
            var renderers = col.GetComponentsInChildren<Renderer>();
            for (int i = 0; i < renderers.Length; i++)
                if (renderers[i] != null && CanFade(renderers[i].transform)) return true;
            return false;
        }

        /// <summary>
        /// Floor, ground, tile, sand, terrain, and an unmarked ceiling. Fadeable pieces, water,
        /// named exclusions do not pull the boom.
        /// </summary>
        public static bool PullsBoom(Collider col)
        {
            if (col == null || col.isTrigger) return false;
            if (NeverFades(col.transform) || CanFade(col)) return false;
            bool floorish = false;
            bool ceiling = false;
            bool water = false;
            Transform t = col.transform;
            while (t != null)
            {
                string n = t.name;
                if (Has(n, "water")) water = true;
                if (Has(n, "floor") || Has(n, "ground") || Has(n, "sand") || Has(n, "tile") || Has(n, "terrain"))
                    floorish = true;
                if (Has(n, "ceiling") || Has(n, "ceil")) ceiling = true;
                t = t.parent;
            }
            if (water) return false;
            if (ceiling && !CanFade(col)) return true;
            return floorish;
        }

        public static bool IsStructural(Transform t)
        {
            while (t != null)
            {
                string n = t.name;
                if (NameMatch(n)) return true;
                t = t.parent;
            }
            return false;
        }

        static bool NameMatch(string n)
        {
            if (string.IsNullOrEmpty(n)) return false;
            if (Has(n, "floor") || Has(n, "ground") || Has(n, "sand") || Has(n, "tile-") || Has(n, "water"))
                return false;
            return Has(n, "wall") || Has(n, "pillar") || Has(n, "roof") || Has(n, "cliff")
                || Has(n, "doorway") || Has(n, "cave-rock") || Has(n, "ruin");
        }

        static bool Has(string n, string part)
        {
            return n.IndexOf(part, System.StringComparison.OrdinalIgnoreCase) >= 0;
        }

        public static void Adopt(Renderer renderer)
        {
            if (renderer == null) return;
            var mats = renderer.sharedMaterials;
            bool changed = false;
            for (int i = 0; i < mats.Length; i++)
            {
                var next = Support(mats[i]);
                if (next != null && next != mats[i])
                {
                    mats[i] = next;
                    changed = true;
                }
            }
            if (!changed) return;
            renderer.sharedMaterials = mats;
        }

        static Material Support(Material src)
        {
            if (src == null) return null;
            var shader = src.shader;
            if (shader != null && shader.name == ShaderName)
            {
                if (!src.IsKeywordEnabled(Keyword)) src.EnableKeyword(Keyword);
                return src;
            }
            int id = src.GetInstanceID();
            if (Copies.TryGetValue(id, out var copy) && copy != null) return copy;
            shader = FadeShader();
            if (shader == null) return src;
            copy = new Material(src)
            {
                name = src.name + "_Occlude",
                hideFlags = HideFlags.DontSave,
                shader = shader
            };
            copy.EnableKeyword(Keyword);
            if (copy.HasProperty(PropertyId)) copy.SetFloat(PropertyId, 1f);
            Copies[id] = copy;
            return copy;
        }

        void Collect()
        {
            touching.Clear();
            touchIds.Clear();
            if (hero == null) return;
            int mask = levelMask.value;
            if (mask == 0)
            {
                int level = LayerMask.NameToLayer("Level");
                if (level >= 0) mask = 1 << level;
            }
            if (mask == 0) return;
            Vector3 chest = hero.position + Vector3.up * 1.15f;
            Vector3 head = hero.position + Vector3.up * 1.65f;
            NoteOverlap(transform.position, mask);
            Cast(chest, mask);
            Cast(head, mask);
        }

        void NoteOverlap(Vector3 at, int mask)
        {
            var cols = Physics.OverlapSphere(at, castRadius, mask, QueryTriggerInteraction.Ignore);
            for (int i = 0; i < cols.Length; i++)
                Note(cols[i]);
        }

        void Cast(Vector3 point, int mask)
        {
            Vector3 from = transform.position;
            Vector3 delta = point - from;
            float dist = delta.magnitude;
            if (dist < 0.05f) return;
            var hits = Physics.SphereCastAll(from, castRadius, delta / dist, dist, mask, QueryTriggerInteraction.Ignore);
            for (int i = 0; i < hits.Length; i++)
            {
                var hit = hits[i];
                if (hit.collider == null) continue;
                // A start-overlap comes back at distance 0 with normal = -direction. That is the
                // wall the camera is inside, and it must fade. Floors are excluded by CanFade.
                Note(hit.collider);
            }
        }

        void Note(Collider col)
        {
            if (col == null || !CanFade(col)) return;
            if (hero != null && (col.transform == hero || col.transform.IsChildOf(hero))) return;
            var renderers = col.GetComponentsInChildren<Renderer>();
            if (renderers == null || renderers.Length == 0)
                renderers = col.GetComponentsInParent<Renderer>();
            for (int r = 0; r < renderers.Length; r++)
            {
                var rend = renderers[r];
                if (rend == null || NeverFades(rend.transform) || !CanFade(rend.transform)) continue;
                Adopt(rend);
                int id = rend.GetInstanceID();
                if (!touchIds.Add(id)) continue;
                touching.Add(rend);
            }
        }

        void FadeToward(float dt)
        {
            for (int i = 0; i < touching.Count; i++)
            {
                var rend = touching[i];
                if (rend == null) continue;
                int id = rend.GetInstanceID();
                float current = Values.TryGetValue(id, out float v) ? v : 1f;
                float next = Mathf.MoveTowards(current, FadedValue, (1f - FadedValue) / FadeInSeconds * dt);
                Values[id] = next;
                Write(rend, next);
                if (!tracked.Contains(rend)) tracked.Add(rend);
            }

            for (int i = tracked.Count - 1; i >= 0; i--)
            {
                var rend = tracked[i];
                if (rend == null)
                {
                    tracked.RemoveAt(i);
                    continue;
                }
                int id = rend.GetInstanceID();
                if (touchIds.Contains(id)) continue;
                float current = Values.TryGetValue(id, out float v) ? v : 1f;
                float next = Mathf.MoveTowards(current, 1f, (1f - FadedValue) / FadeOutSeconds * dt);
                if (next >= 0.999f)
                {
                    Values.Remove(id);
                    Write(rend, 1f);
                    tracked.RemoveAt(i);
                }
                else
                {
                    Values[id] = next;
                    Write(rend, next);
                }
            }
        }

        static void Write(Renderer renderer, float value)
        {
            Block ??= new MaterialPropertyBlock();
            int count = renderer.sharedMaterials != null ? renderer.sharedMaterials.Length : 1;
            if (count < 1) count = 1;
            for (int i = 0; i < count; i++)
            {
                renderer.GetPropertyBlock(Block, i);
                Block.SetFloat(PropertyId, value);
                renderer.SetPropertyBlock(Block, i);
            }
        }
    }
}

