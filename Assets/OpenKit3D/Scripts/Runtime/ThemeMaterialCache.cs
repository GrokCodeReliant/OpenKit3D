using System.Collections.Generic;
using UnityEngine;

namespace OpenKit
{
    /// <summary>One shared material per (theme x slot). Keeps the SRP Batcher happy: no MaterialPropertyBlocks,
    /// and a scene with N themes has at most N*5 Open Kit materials.</summary>
    public static class ThemeMaterialCache
    {
        public const string LitShader = "Universal Render Pipeline/Lit";
        static readonly Dictionary<(ThemeProfile, ThemeSlot), Material> s_Runtime = new();

        public static Material Get(ThemeProfile profile, ThemeSlot slot)
        {
            if (!profile) return null;
            var ov = profile.GetOverride(slot);
            if (ov) return ov;
            int i = (int)slot;
            if (profile.bakedMaterials != null && i < profile.bakedMaterials.Length && profile.bakedMaterials[i])
                return profile.bakedMaterials[i];
            if (s_Runtime.TryGetValue((profile, slot), out var m) && m) return m;
            var shader = Shader.Find(LitShader);
            if (!shader) return null;
            m = new Material(shader) { name = $"OK_{profile.themeName}_{slot}", hideFlags = HideFlags.DontSave };
            Apply(m, profile, slot);
            s_Runtime[(profile, slot)] = m;
            return m;
        }

        /// <summary>Write palette values into a material (URP Lit property names).</summary>
        public static void Apply(Material m, ThemeProfile profile, ThemeSlot slot)
        {
            var look = profile.GetLook(slot);
            m.SetColor("_BaseColor", look.color);
            m.SetFloat("_Metallic", look.metallic);
            m.SetFloat("_Smoothness", look.smoothness);
            if (slot == ThemeSlot.Emissive)
            {
                m.EnableKeyword("_EMISSION");
                m.SetColor("_EmissionColor", look.color * Mathf.Max(0f, profile.emissiveIntensity));
                m.globalIlluminationFlags = MaterialGlobalIlluminationFlags.RealtimeEmissive;
            }
            else
            {
                m.DisableKeyword("_EMISSION");
                m.SetColor("_EmissionColor", Color.black);
            }
        }

        /// <summary>Palette edited: push values into the existing shared materials (no reassignment needed).</summary>
        public static void Refresh(ThemeProfile profile)
        {
            if (!profile) return;
            for (int i = 0; i < OpenKitConst.SlotCount; i++)
            {
                var slot = (ThemeSlot)i;
                if (profile.bakedMaterials != null && i < profile.bakedMaterials.Length && profile.bakedMaterials[i])
                    Apply(profile.bakedMaterials[i], profile, slot);
                if (s_Runtime.TryGetValue((profile, slot), out var m) && m) Apply(m, profile, slot);
            }
        }

        public static void Clear()
        {
            foreach (var m in s_Runtime.Values) if (m) Object.DestroyImmediate(m);
            s_Runtime.Clear();
        }
    }
}
