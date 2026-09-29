using System;
using UnityEngine;

namespace OpenKit
{
    /// <summary>One theme (Dungeon, Heaven, Hell, ...): a palette per slot, optional material overrides,
    /// and the inhabitant scale used by props with scalesWithRoom (halfling 0.75, human 1.0, giant 2.0).</summary>
    [CreateAssetMenu(menuName = "Open Kit 3D/Theme Profile", fileName = "Theme")]
    public class ThemeProfile : ScriptableObject
    {
        [Serializable]
        public struct SlotLook
        {
            public Color color;
            [Range(0, 1)] public float metallic;
            [Range(0, 1)] public float smoothness;
        }

        [Serializable]
        public struct SlotOverride
        {
            public ThemeSlot slot;
            public Material material;
        }

        public string themeName = "Theme";

        [Header("Palette (index = ThemeSlot)")]
        public SlotLook[] palette = DefaultPalette();
        [Min(0)] public float emissiveIntensity = 2f;

        [Tooltip("Optional: replace a slot with an authored material (e.g. Primary -> obsidian in Hell).")]
        public SlotOverride[] materialOverrides = Array.Empty<SlotOverride>();

        [Header("Scale")]
        [Tooltip("Design values: halfling 0.75, human 1.0, giant 2.0")]
        [Min(0.05f)] public float inhabitantScale = 1f;

        [Header("Room hints (optional)")]
        public Color lightTint = Color.white;

        [Tooltip("Persistent theme x slot materials (sub-assets written by the editor build). If empty, runtime materials are created and cached.")]
        [HideInInspector] public Material[] bakedMaterials = new Material[OpenKitConst.SlotCount];

        public SlotLook GetLook(ThemeSlot s)
        {
            int i = (int)s;
            return (palette != null && i < palette.Length) ? palette[i] : new SlotLook { color = Color.grey, smoothness = 0.3f };
        }

        public Material GetOverride(ThemeSlot s)
        {
            if (materialOverrides == null) return null;
            foreach (var o in materialOverrides) if (o.slot == s && o.material) return o.material;
            return null;
        }

        public static SlotLook[] DefaultPalette() => new[]
        {
            new SlotLook { color = new Color(0.60f, 0.60f, 0.60f), smoothness = 0.2f },
            new SlotLook { color = new Color(0.42f, 0.42f, 0.42f), smoothness = 0.15f },
            new SlotLook { color = new Color(0.80f, 0.80f, 0.80f), smoothness = 0.4f },
            new SlotLook { color = new Color(0.30f, 0.30f, 0.30f), metallic = 1f, smoothness = 0.6f },
            new SlotLook { color = new Color(0.92f, 0.92f, 0.92f), smoothness = 0.5f },
        };

        void OnValidate()
        {
            if (palette == null || palette.Length != OpenKitConst.SlotCount)
            {
                var p = DefaultPalette();
                if (palette != null) for (int i = 0; i < Mathf.Min(palette.Length, p.Length); i++) p[i] = palette[i];
                palette = p;
            }
            ThemeMaterialCache.Refresh(this);
            ThemeRoom.RefreshAll();
        }
    }
}
