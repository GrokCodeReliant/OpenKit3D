using System;
using UnityEngine;

namespace OpenKitDungeon
{
    [Serializable]
    public class CoverageEntry
    {
        [Tooltip("Part-name glob. * is any run of characters. Example: ARM_L_B01_*_CHST")]
        public string pattern;
        public BodyRegionMask covers;
    }

    [CreateAssetMenu(fileName = "CoverageTable", menuName = "Open Kit Dungeon/Coverage Table")]
    public class CoverageTable : ScriptableObject
    {
        public CoverageEntry[] entries = new CoverageEntry[0];

        public bool TryMatch(string partName, out BodyRegionMask covers)
        {
            covers = BodyRegionMask.None;
            if (string.IsNullOrEmpty(partName) || entries == null) return false;
            bool any = false;
            for (int i = 0; i < entries.Length; i++)
            {
                var e = entries[i];
                if (e == null || string.IsNullOrEmpty(e.pattern)) continue;
                if (!Glob(e.pattern, partName)) continue;
                covers |= e.covers;
                any = true;
            }
            return any;
        }

        public static bool Glob(string pattern, string text)
        {
            if (pattern == null || text == null) return false;
            int pi = 0, ti = 0, starP = -1, starT = -1;
            while (ti < text.Length)
            {
                if (pi < pattern.Length && pattern[pi] == text[ti])
                {
                    pi++;
                    ti++;
                }
                else if (pi < pattern.Length && pattern[pi] == '*')
                {
                    starP = pi;
                    pi++;
                    starT = ti;
                }
                else if (starP >= 0)
                {
                    pi = starP + 1;
                    starT++;
                    ti = starT;
                }
                else return false;
            }
            while (pi < pattern.Length && pattern[pi] == '*') pi++;
            return pi == pattern.Length;
        }
    }
}
