// Facade on the hero prefab root. HeroBodyType and HeroProportions stay on the prefab;
// this drives them and the per-slot HeroEquipSlot children.
using System.Collections.Generic;
using UnityEngine;

namespace HeroRig
{
    [DisallowMultipleComponent]
    public class HeroEquipment : MonoBehaviour
    {
        public HeroSex sex = HeroSex.Male;

        /// ML / MS from male HeroBodyType.weight < 0.5 / >= 0.5. FP / FB the same way for female.
        public HeroFit CurrentFit
        {
            get
            {
                var bt = GetComponent<HeroBodyType>();
                float w = bt ? bt.weight : 0f;
                bool full = w >= 0.5f;
                if (sex == HeroSex.Female) return full ? HeroFit.FB : HeroFit.FP;
                return full ? HeroFit.MS : HeroFit.ML;
            }
        }

        HeroEquipSlot[] _slots;
        bool _clothingCaptured;
        bool _clothingEnabled = true;
        GameObject _armorRoot;
        HeroArmorItem _armor;
        int _armorTier;
        float _armorQ;

        public HeroEquipSlot Slot(HeroGearSlot slot)
        {
            if (_slots == null || _slots.Length == 0) _slots = GetComponentsInChildren<HeroEquipSlot>(true);
            for (int i = 0; i < _slots.Length; i++)
                if (_slots[i] && _slots[i].slot == slot) return _slots[i];
            _slots = GetComponentsInChildren<HeroEquipSlot>(true);
            for (int i = 0; i < _slots.Length; i++)
                if (_slots[i] && _slots[i].slot == slot) return _slots[i];
            return null;
        }

        public GameObject Equip(HeroGearSlot slot, GameObject prefabOrInstance)
        {
            var s = Slot(slot);
            if (!s) { Debug.LogError("[HeroRig] no EquipSlot_" + slot); return null; }
            var inst = s.Equip(prefabOrInstance);
            if (slot == HeroGearSlot.MainHand) RefreshGripLayer();
            return inst;
        }

        public void Unequip(HeroGearSlot slot)
        {
            Slot(slot)?.Unequip();
            if (slot == HeroGearSlot.MainHand) RefreshGripLayer();
        }

        void RefreshGripLayer()
        {
            var wc = GetComponent<HeroWeaponController>();
            if (wc) wc.ApplyAnimator();
        }

        public void UnequipAll()
        {
            foreach (HeroGearSlot s in System.Enum.GetValues(typeof(HeroGearSlot)))
                Unequip(s);
        }

        /// One armour inventory item. Children are split by part-code token
        /// (_HEAD _SHLD _CHST _HAND _LEGS _FEET, e.g. ARM_L_B01_M_CHST or TEST_M_SHLD_L).
        /// Several children for one slot (SHLD_L + SHLD_R) are equipped together.
        public void EquipItem(GameObject displayRoot)
        {
            if (!displayRoot) return;
            var groups = new Dictionary<HeroGearSlot, List<Transform>>();
            var pending = new List<Transform>();
            for (int i = 0; i < displayRoot.transform.childCount; i++)
                pending.Add(displayRoot.transform.GetChild(i));
            foreach (var c in pending)
            {
                if (!HeroGearCodes.TryParsePart(c.name, out var slot)) continue;
                if (!groups.TryGetValue(slot, out var list))
                    groups[slot] = list = new List<Transform>();
                list.Add(c);
            }
            foreach (var kv in groups)
            {
                if (kv.Value.Count == 1)
                {
                    Equip(kv.Key, kv.Value[0].gameObject);
                    continue;
                }
                var holder = new GameObject(displayRoot.name + "_" + kv.Key);
                for (int i = 0; i < kv.Value.Count; i++)
                    kv.Value[i].SetParent(holder.transform, false);
                Equip(kv.Key, holder);
            }
        }

        /// Sex picks the display prefab. EquipItem routes the six parts. The look is one table row.
        /// Fit follows HeroBodyType (skinned shapes) and CurrentFit (stored SHLD offsets; not applied when SHLD is skinned).
        public GameObject EquipArmor(HeroArmorItem item, int tier, float q)
        {
            if (!item)
            {
                Debug.LogError("[HeroRig] EquipArmor null item");
                return null;
            }
            UnequipArmor();
            var prefab = sex == HeroSex.Female ? item.femalePrefab : item.malePrefab;
            if (!prefab)
            {
                Debug.LogError("[HeroRig] EquipArmor missing prefab for " + sex);
                return null;
            }
            var inst = Instantiate(prefab);
            inst.name = prefab.name;
            _armorRoot = inst;
            _armor = item;
            _armorTier = tier;
            _armorQ = q;
            EquipItem(inst);
            if (inst) { inst.transform.SetParent(transform, false); inst.SetActive(false); }
            ApplyArmorLook();
            var sh = Slot(HeroGearSlot.Shoulders);
            if (sh && sh.IsEquipped) sh.ReapplyFit();
            return inst;
        }

        HeroWeaponItem _weapon;
        int _weaponTier;
        float _weaponQ;

        /// Main-hand weapon. Sex uses the one prefab. Look is applied on that item's submeshes only.
        public GameObject EquipWeapon(HeroWeaponItem item, int tier, float q)
        {
            if (!item)
            {
                Debug.LogError("[HeroRig] EquipWeapon null item");
                return null;
            }
            if (!item.prefab)
            {
                Debug.LogError("[HeroRig] EquipWeapon missing prefab for " + item.id);
                return null;
            }
            _weapon = item;
            _weaponTier = tier;
            _weaponQ = q;
            var inst = Equip(HeroGearSlot.MainHand, item.prefab);
            ApplyWeaponLook();
            return inst;
        }

        public void ApplyWeaponLook()
        {
            if (_weapon == null || _weapon.look == null) return;
            foreach (var look in GetComponentsInChildren<HeroGearLook>(true))
            {
                var gi = look.GetComponent<HeroGearItem>();
                if (!gi || gi.itemId != _weapon.lookBaseId) continue;
                look.Apply(_weapon.look, _weapon.lookBaseId, _weaponTier, _weaponQ);
            }
        }

        public void UnequipArmor()
        {
            Unequip(HeroGearSlot.Head);
            Unequip(HeroGearSlot.Shoulders);
            Unequip(HeroGearSlot.Chest);
            Unequip(HeroGearSlot.Hands);
            Unequip(HeroGearSlot.Legs);
            Unequip(HeroGearSlot.Feet);
            if (_armorRoot)
            {
                if (Application.isPlaying) Destroy(_armorRoot);
                else DestroyImmediate(_armorRoot);
            }
            _armorRoot = null;
            _armor = null;
        }

        public void ApplyArmorLook()
        {
            if (_armor == null || _armor.look == null) return;
            foreach (var look in GetComponentsInChildren<HeroGearLook>(true))
            {
                var gi = look.GetComponent<HeroGearItem>();
                if (gi && !string.IsNullOrEmpty(gi.itemId) && gi.itemId != _armor.lookBaseId) continue;
                look.Apply(_armor.look, _armor.lookBaseId, _armorTier, _armorQ);
            }
        }

        public void SetBodyType(float weight)
        {
            var bt = GetComponent<HeroBodyType>();
            if (bt) bt.Set(weight);
            var sh = Slot(HeroGearSlot.Shoulders);
            if (sh && sh.IsEquipped) sh.ReapplyFit();
        }

        public void SetHeight(float height)
        {
            var p = GetComponent<HeroProportions>();
            if (!p) return;
            p.height = height;
            p.Apply();
        }

        public void SetScale(float uniformScale)
        {
            var p = GetComponent<HeroProportions>();
            if (!p) return;
            p.uniformScale = uniformScale;
            p.Apply();
        }

        public void RefreshClothing()
        {
            bool hide = false;
            var slots = GetComponentsInChildren<HeroEquipSlot>(true);
            for (int i = 0; i < slots.Length; i++)
                if (slots[i] && slots[i].HidesClothing) { hide = true; break; }
            foreach (var r in GetComponentsInChildren<SkinnedMeshRenderer>(true))
            {
                if (r.name != "Clothing") continue;
                if (!_clothingCaptured) { _clothingEnabled = r.enabled; _clothingCaptured = true; }
                r.enabled = hide ? false : _clothingEnabled;
            }
        }
    }
}
