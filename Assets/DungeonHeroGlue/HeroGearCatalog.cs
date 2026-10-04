using System;
using System.Collections.Generic;
using UnityEngine;

namespace OpenKitDungeon
{
    [Serializable]
    public class HeroGearEntry
    {
        public string variantName;
        public GameObject prefab;
    }

    /// <summary>variantName to display prefab. Leather rows exist with null prefabs until the meshes are imported.</summary>
    public class HeroGearCatalog : ScriptableObject
    {
        public List<HeroGearEntry> entries = new List<HeroGearEntry>();

        public GameObject PrefabFor(string variantName)
        {
            if (entries == null || string.IsNullOrEmpty(variantName)) return null;
            for (int i = 0; i < entries.Count; i++)
                if (entries[i] != null && entries[i].variantName == variantName)
                    return entries[i].prefab;
            return null;
        }

        public static HeroGearCatalog WithLeatherDefaults()
        {
            var cat = CreateInstance<HeroGearCatalog>();
            string[] parts = { "HEAD", "SHLD", "CHST", "HAND", "LEGS", "FEET" };
            string[] sexes = { "M", "F" };
            for (int s = 0; s < sexes.Length; s++)
                for (int p = 0; p < parts.Length; p++)
                    cat.entries.Add(new HeroGearEntry { variantName = "ARM_L_B01_" + sexes[s] + "_" + parts[p] });
            return cat;
        }
    }
}
