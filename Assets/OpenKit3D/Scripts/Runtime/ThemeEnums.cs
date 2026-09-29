namespace OpenKit
{
    /// <summary>The five material slots every Open Kit mesh may use (names survive FBX export).</summary>
    public enum ThemeSlot { Primary = 0, Secondary = 1, Accent = 2, Metal = 3, Emissive = 4 }

    /// <summary>The three user-settable colour slots (inspector). Theme supplies the defaults, a user override wins.
    /// Mapping: Primary &lt;- Primary, Secondary &lt;- Secondary, Tertiary &lt;- Accent + Metal. Emissive stays theme-driven.</summary>
    public enum UserColorSlot { Primary = 0, Secondary = 1, Tertiary = 2 }

    /// <summary>D&amp;D-style footprint classes on the 1.5 m (5 ft) grid.</summary>
    public enum SizeClass { Tiny, Small, Medium, Large, Huge }

    /// <summary>Room size class. FromTheme uses the ThemeProfile's inhabitantScale.</summary>
    public enum RoomSize { FromTheme, Halfling, Human, Giant }

    public static class OpenKitConst
    {
        public const float GridCell = 1.5f;
        public const int SlotCount = 5;
        public const int UserSlotCount = 3;
        public static readonly string[] SlotNames = { "Primary", "Secondary", "Accent", "Metal", "Emissive" };
        public static readonly string[] UserSlotNames = { "Primary", "Secondary", "Tertiary" };

        /// <summary>Approved inhabitant scales: halfling 0.75, human 1.0, giant 2.0.</summary>
        public static float ScaleOf(RoomSize size, float themeScale) => size switch
        {
            RoomSize.Halfling => 0.75f,
            RoomSize.Human => 1.0f,
            RoomSize.Giant => 2.0f,
            _ => themeScale,
        };

        /// <summary>User colour slot for a material slot, or -1 (Emissive: outside the user slots).</summary>
        public static int UserSlotOf(ThemeSlot s) => s switch
        {
            ThemeSlot.Primary => 0,
            ThemeSlot.Secondary => 1,
            ThemeSlot.Accent => 2,
            ThemeSlot.Metal => 2,
            _ => -1,
        };

        /// <summary>Resolve a slot from a material name ("Primary", "Primary (Instance)", "OK_Hell_Primary").</summary>
        public static bool TryParseSlot(string materialName, out ThemeSlot slot)
        {
            slot = ThemeSlot.Primary;
            if (string.IsNullOrEmpty(materialName)) return false;
            string n = materialName.Replace(" (Instance)", "");
            for (int i = 0; i < SlotCount; i++)
            {
                string s = SlotNames[i];
                if (n == s || n.EndsWith("_" + s) || n.StartsWith(s + ".") || n.StartsWith(s + " "))
                { slot = (ThemeSlot)i; return true; }
            }
            return false;
        }
    }
}
