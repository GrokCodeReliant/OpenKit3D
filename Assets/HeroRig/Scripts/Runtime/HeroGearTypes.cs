// Gear slots. Part codes on a display FBX child name: _HEAD _SHLD _CHST _HAND _LEGS _FEET.
using System;

namespace HeroRig
{
    public enum HeroSex { Male, Female }

    /// Male lean / male strong / female petite / female busty. Chosen from sex + HeroBodyType.weight (0.5 threshold).
    public enum HeroFit { ML, MS, FP, FB }

    public enum HeroGearSlot { Head, Shoulders, Chest, Hands, Legs, Feet, MainHand, OffHand }

    /// How a slot attaches. Head, Shoulders, MainHand, OffHand are rigid sockets.
    /// Chest, Hands, Legs, Feet are skinned to the body skeleton (rigid mesh is a fallback, one copy per anchor).
    public enum HeroAttachMode { Rigid, Skinned }

    /// HeroGearItem override. Auto = Skinned when the object has a SkinnedMeshRenderer, otherwise Rigid.
    public enum HeroGearMode { Auto, Rigid, Skinned }

    public static class HeroGearCodes
    {
        public static bool TryParsePart(string name, out HeroGearSlot slot)
        {
            slot = default;
            if (string.IsNullOrEmpty(name)) return false;
            // Socket_Head contains the _HEAD token. It is a bone, not a helmet mesh.
            if (name.StartsWith("Socket_", StringComparison.OrdinalIgnoreCase)) return false;
            string u = name.ToUpperInvariant();
            // Longer tokens first. A code matches only as an _CODE token (end or another _).
            (string code, HeroGearSlot s)[] table =
            {
                ("SHLD", HeroGearSlot.Shoulders),
                ("HEAD", HeroGearSlot.Head),
                ("CHST", HeroGearSlot.Chest),
                ("LEGS", HeroGearSlot.Legs),
                ("FEET", HeroGearSlot.Feet),
                ("HAND", HeroGearSlot.Hands),
            };
            foreach (var (code, s) in table)
            {
                int i = 0;
                string token = "_" + code;
                while ((i = u.IndexOf(token, i, StringComparison.Ordinal)) >= 0)
                {
                    int end = i + token.Length;
                    if (end == u.Length || u[end] == '_') { slot = s; return true; }
                    i = end;
                }
            }
            return false;
        }
    }
}
