using System;

namespace OpenKitDungeon
{
    /// <summary>
    /// Body regions. Bit = 1 &lt;&lt; id. Same names as gear part codes.
    /// HEAD=0, SHLD=1, CHST=2, HAND=3, LEGS=4, FEET=5.
    /// </summary>
    [Flags]
    public enum BodyRegionMask
    {
        None = 0,
        HEAD = 1 << 0,
        SHLD = 1 << 1,
        CHST = 1 << 2,
        HAND = 1 << 3,
        LEGS = 1 << 4,
        FEET = 1 << 5
    }
}
