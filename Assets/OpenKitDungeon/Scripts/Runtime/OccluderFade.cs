using UnityEngine;

namespace OpenKitDungeon
{
    /// <summary>
    /// Marker for a piece that should fade when it sits between the camera and the hero.
    /// Put it on the parent. Every renderer under it can fade, except never-fade exclusions
    /// (Health, the hero, loot, chests, levers, the exit portal). Art places these; gameplay does not.
    /// </summary>
    public class OccluderFade : MonoBehaviour
    {
    }
}
