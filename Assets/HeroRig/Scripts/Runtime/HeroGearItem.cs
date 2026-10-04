// Optional component on a gear prefab or one display part (gear display parts can use this).
using System;
using System.Collections.Generic;
using UnityEngine;

namespace HeroRig
{
    [Serializable]
    public class HeroFitOffset
    {
        public HeroFit fit;
        public Vector3 position;
        [Tooltip("Multiplies HeroGearItem.localScale. Zero is treated as (1,1,1).")]
        public Vector3 scaleMultiplier = Vector3.one;
    }

    [DisallowMultipleComponent]
    public class HeroGearItem : MonoBehaviour
    {
        public HeroGearSlot slot;
        public HeroGearMode mode = HeroGearMode.Auto;
        public Vector3 localPosition;
        public Vector3 localEuler;
        public Vector3 localScale = Vector3.one;
        [Tooltip("While equipped, disable the hero Clothing renderer. Defaults on for Chest and Legs.")]
        public bool hidesClothing;
        [Tooltip("Shoulder (SHLD) per-fit placement. HeroEquipment.CurrentFit picks the entry.")]
        public List<HeroFitOffset> fitOffsets = new List<HeroFitOffset>();
        public string itemId;

        [SerializeField] HeroGearSlot _slotForDefault;
        [SerializeField] bool _defaultSynced;

        public HeroFitOffset FitFor(HeroFit fit)
        {
            if (fitOffsets == null) return null;
            for (int i = 0; i < fitOffsets.Count; i++)
                if (fitOffsets[i] != null && fitOffsets[i].fit == fit) return fitOffsets[i];
            return null;
        }

        void Reset()
        {
            localScale = Vector3.one;
            hidesClothing = slot == HeroGearSlot.Chest || slot == HeroGearSlot.Legs;
            _slotForDefault = slot;
            _defaultSynced = true;
        }

        void OnValidate()
        {
            if (localScale == Vector3.zero) localScale = Vector3.one;
            if (!_defaultSynced || _slotForDefault != slot)
            {
                bool oldDefault = _slotForDefault == HeroGearSlot.Chest || _slotForDefault == HeroGearSlot.Legs;
                if (!_defaultSynced || hidesClothing == oldDefault)
                    hidesClothing = slot == HeroGearSlot.Chest || slot == HeroGearSlot.Legs;
                _slotForDefault = slot;
                _defaultSynced = true;
            }
        }
    }
}
