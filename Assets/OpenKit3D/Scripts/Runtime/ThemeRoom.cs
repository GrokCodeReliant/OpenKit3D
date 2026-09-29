using System.Collections.Generic;
using UnityEngine;

namespace OpenKit
{
    /// <summary>Put on a room root. Every ThemeAdaptive below it recolours to this profile and scales to the room size class.</summary>
    [ExecuteAlways]
    [DisallowMultipleComponent]
    public class ThemeRoom : MonoBehaviour
    {
        public ThemeProfile profile;
        [Tooltip("Room size class: halfling den 0.75, human hall 1.0, giant's cave 2.0. FromTheme = the profile's inhabitantScale.")]
        public RoomSize roomSize = RoomSize.FromTheme;
        [Tooltip("Optional room lights tinted by profile.lightTint")]
        public Light[] roomLights = new Light[0];

        /// <summary>Fallback profile for adaptive assets that are not under any ThemeRoom (null = leave neutral).</summary>
        public static ThemeProfile GlobalDefault;

        static readonly List<ThemeRoom> s_Rooms = new();

        /// <summary>Scale applied to room-scaling assets in this room.</summary>
        public float InhabitantScale => OpenKitConst.ScaleOf(roomSize, profile ? profile.inhabitantScale : 1f);

        /// <summary>The room's grid cell: structural pieces (tiles, walls, doors, fences, pillars) snap to this.</summary>
        public float GridCell => OpenKitConst.GridCell * InhabitantScale;

        void OnEnable() { if (!s_Rooms.Contains(this)) s_Rooms.Add(this); Apply(); }
        void OnDisable() { s_Rooms.Remove(this); }

        void OnValidate()
        {
#if UNITY_EDITOR
            UnityEditor.EditorApplication.delayCall += () => { if (this) Apply(); };
#else
            Apply();
#endif
        }

        public void Apply()
        {
            if (profile && roomLights != null)
                foreach (var l in roomLights) if (l) l.color = profile.lightTint;
            foreach (var a in GetComponentsInChildren<ThemeAdaptive>(true)) a.Apply();
        }

        public static void RefreshAll()
        {
            foreach (var r in s_Rooms) if (r) r.Apply();
        }
    }
}
