// One weapon inventory item. Grip-space anchors are full Vector3 points in metres on Unity axes (template v1.3).
using UnityEngine;

namespace HeroRig
{
    [CreateAssetMenu(fileName = "weapon.swd.b01", menuName = "HeroRig/Weapon Item")]
    public class HeroWeaponItem : ScriptableObject
    {
        public string id = "weapon.swd.b01";
        public string displayName = "Sword";
        public int band = 1;
        public string template = "1H";
        public string subSize = "sword";
        public string weightClass = "Medium";
        public Vector3 tipOffset;
        public Vector3 hitBase;
        public Vector3 supportOffset;
        public float hitRadius = 0.06f;
        public string stowSocket = "Socket_Hip_L";
        public Vector3 stowPos;
        public Vector3 stowEuler;
        public GameObject prefab;
        public string lookBaseId = "weapon.swd.b01";
        public HeroGearLookTable look;

        public float attackRange => HeroWeaponTemplates.AttackRange(template, subSize);
    }
}
