using System;
using System.Collections.Generic;
using UnityEngine;

namespace OpenKit
{
    /// <summary>On every Open Kit prefab (room-adapt rule). Swaps each material slot to the room theme's cached shared material,
    /// scales by the room size class (props and structural pieces alike; structural pieces snap to the room grid, cell = 1.5 m x scale),
    /// and applies the three user colour slots (Primary / Secondary / Tertiary) as per-renderer MaterialPropertyBlocks
    /// on top of the theme defaults, so no materials are duplicated.</summary>
    [ExecuteAlways]
    [DisallowMultipleComponent]
    public class ThemeAdaptive : MonoBehaviour
    {
        [Serializable]
        public class RendererSlots
        {
            public Renderer renderer;
            public ThemeSlot[] slots;
            public Material[] neutral;   // original slot materials, restored when no theme applies
        }

        [Serializable]
        public class ColorOverride
        {
            [Tooltip("Use this colour instead of the theme default")] public bool enabled;
            public Color color = Color.white;
        }

        public SizeClass sizeClass = SizeClass.Small;
        [Tooltip("Scale with the room size class.")]
        public bool scalesWithRoom = true;
        [Tooltip("Structural piece: snaps to the room grid (cell = 1.5 m x room scale)")]
        public bool snapsToRoomGrid;
        [Tooltip("Size-class base scale (1 = authored size)")]
        public Vector3 baseScale = Vector3.one;
        [Tooltip("Optional: force a theme regardless of parent room")]
        public ThemeProfile profileOverride;

        [Header("User colour slots (override the theme defaults)")]
        [Tooltip("Primary material slot")] public ColorOverride primaryColor = new();
        [Tooltip("Secondary material slot")] public ColorOverride secondaryColor = new();
        [Tooltip("Accent + Metal material slots (trim / hardware)")] public ColorOverride tertiaryColor = new();

        [Tooltip("Per-prop cap on the Emissive slot and its light (1 = theme value)")]
        [Range(0.05f, 1f)] public float emissiveScale = 1f;

        [Tooltip("Lights tinted with the Emissive colour (e.g. brazier flame). Range and intensity scale with the room.")]
        public Light[] emissiveLights = new Light[0];
        [SerializeField, HideInInspector] float[] lightBaseRange;
        [SerializeField, HideInInspector] float[] lightBaseIntensity;

        [SerializeField] List<RendererSlots> slotMap = new();

        public ThemeProfile CurrentProfile { get; private set; }
        public float CurrentScale { get; private set; } = 1f;
        public IReadOnlyList<RendererSlots> SlotMap => slotMap;

        static MaterialPropertyBlock s_Block;
        static readonly int BaseColorId = Shader.PropertyToID("_BaseColor");
        static readonly int EmissionColorId = Shader.PropertyToID("_EmissionColor");

        void OnEnable() => Apply();

        void OnTransformParentChanged() => Apply();

        void OnValidate()
        {
#if UNITY_EDITOR
            UnityEditor.EditorApplication.delayCall += () => { if (this) Apply(); };
#endif
        }

        public ColorOverride GetOverride(UserColorSlot s) => s switch
        {
            UserColorSlot.Primary => primaryColor,
            UserColorSlot.Secondary => secondaryColor,
            _ => tertiaryColor,
        };

        /// <summary>Set (or clear with null) a user colour slot and re-apply.</summary>
        public void SetUserColor(UserColorSlot s, Color? c)
        {
            var o = GetOverride(s);
            o.enabled = c.HasValue; if (c.HasValue) o.color = c.Value;
            Apply();
        }

        public ThemeProfile ResolveProfile()
        {
            if (profileOverride) return profileOverride;
            var room = GetComponentInParent<ThemeRoom>(true);
            if (room && room.profile) return room.profile;
            return ThemeRoom.GlobalDefault;
        }

        public float ResolveRoomScale(ThemeProfile p)
        {
            var room = GetComponentInParent<ThemeRoom>(true);
            if (room) return room.InhabitantScale;
            return p ? p.inhabitantScale : 1f;
        }

        /// <summary>Build the renderer -> slot table from material names (done once by the editor build).</summary>
        public void RebuildSlotMap()
        {
            slotMap.Clear();
            foreach (var r in GetComponentsInChildren<Renderer>(true))
            {
                var mats = r.sharedMaterials;
                var e = new RendererSlots { renderer = r, slots = new ThemeSlot[mats.Length], neutral = mats };
                bool any = false;
                for (int i = 0; i < mats.Length; i++)
                {
                    if (mats[i] && OpenKitConst.TryParseSlot(mats[i].name, out var s)) { e.slots[i] = s; any = true; }
                }
                if (any) slotMap.Add(e);
            }
            lightBaseRange = new float[emissiveLights.Length];
            lightBaseIntensity = new float[emissiveLights.Length];
            for (int i = 0; i < emissiveLights.Length; i++)
                if (emissiveLights[i]) { lightBaseRange[i] = emissiveLights[i].range; lightBaseIntensity[i] = emissiveLights[i].intensity; }
        }

        public void Apply()
        {
            if (slotMap == null || slotMap.Count == 0) RebuildSlotMap();
            var p = ResolveProfile();
            CurrentProfile = p;
            float s = scalesWithRoom ? ResolveRoomScale(p) : 1f;
            CurrentScale = s;
            transform.localScale = baseScale * s;
            s_Block ??= new MaterialPropertyBlock();

            foreach (var e in slotMap)
            {
                if (!e.renderer) continue;
                var mats = e.renderer.sharedMaterials;
                bool changed = false;
                for (int i = 0; i < mats.Length && i < e.slots.Length; i++)
                {
                    var m = p ? ThemeMaterialCache.Get(p, e.slots[i]) : (e.neutral != null && i < e.neutral.Length ? e.neutral[i] : null);
                    if (m && mats[i] != m) { mats[i] = m; changed = true; }
                }
                if (changed) e.renderer.sharedMaterials = mats;
                // user colour slots + emissive cap: per-submesh property blocks (theme material stays shared)
                for (int i = 0; i < mats.Length && i < e.slots.Length; i++)
                {
                    s_Block.Clear();
                    int u = OpenKitConst.UserSlotOf(e.slots[i]);
                    if (u >= 0)
                    {
                        var o = GetOverride((UserColorSlot)u);
                        if (o.enabled) s_Block.SetColor(BaseColorId, o.color);
                    }
                    else if (e.slots[i] == ThemeSlot.Emissive && emissiveScale < 0.999f && mats[i] && mats[i].HasProperty(EmissionColorId))
                    {
                        s_Block.SetColor(EmissionColorId, mats[i].GetColor(EmissionColorId) * emissiveScale);
                    }
                    e.renderer.SetPropertyBlock(s_Block, i);   // an empty block clears any earlier override
                }
            }

            if (emissiveLights != null && lightBaseRange != null)
            {
                for (int i = 0; i < emissiveLights.Length && i < lightBaseRange.Length; i++)
                {
                    var l = emissiveLights[i];
                    if (!l) continue;
                    l.range = lightBaseRange[i] * s;
                    float k = p ? Mathf.Max(0.35f, p.emissiveIntensity / 1.5f) : 1f;
                    if (p) l.color = p.GetLook(ThemeSlot.Emissive).color;
                    l.intensity = lightBaseIntensity[i] * k * s * emissiveScale;
                }
            }
        }
    }
}
