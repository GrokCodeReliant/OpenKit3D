using UnityEngine;

namespace OpenKitDungeon
{
    /// <summary>
    /// Optional per-part covers. When present on a part, it replaces the CoverageTable row for that object.
    /// </summary>
    public class HeroCoverageDeclaration : MonoBehaviour
    {
        public BodyRegionMask covers;
    }
}
