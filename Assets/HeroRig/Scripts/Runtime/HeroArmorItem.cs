// One inventory item for both sexes and all four fits. The display prefab follows HeroEquipment.sex.
using UnityEngine;

namespace HeroRig
{
    [CreateAssetMenu(fileName = "armor.l.b01", menuName = "HeroRig/Armor Item")]
    public class HeroArmorItem : ScriptableObject
    {
        public string id = "armor.l.b01";
        public string displayName = "Light Armor";
        public string weightCode = "L";
        public int band = 1;
        public GameObject malePrefab;
        public GameObject femalePrefab;
        public string lookBaseId = "armor.l.b01";
        public HeroGearLookTable look;
    }
}
