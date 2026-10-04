// Serialized sockets + a name lookup for the whole skeleton. Auto-filled by bone name.
using System.Collections.Generic;
using System.Text;
using UnityEngine;

namespace HeroRig
{
    [DisallowMultipleComponent, ExecuteAlways]
    public class HeroAttachPoints : MonoBehaviour
    {
        public Transform hips;
        public Transform socketHead;
        public Transform socketChest;
        public Transform socketShoulderL;
        public Transform socketShoulderR;
        public Transform socketMainHand;
        public Transform socketOffHand;
        public Transform gripMainHand;
        public Transform gripOffHand;
        public Transform socketBack2H;
        public Transform socketBackBow;
        public Transform socketBackShield;
        public Transform socketHipL;
        public Transform socketHipR;
        public Transform socketBelt;

        Dictionary<string, Transform> _bones;
        bool _binding;

        void Reset() => Bind();
        void Awake() { if (!hips) Bind(); }
        void OnValidate() => Bind();

        public void Bind()
        {
            if (_binding) return;
            _binding = true;
            try
            {
                hips = Pick("Hips", hips);
                socketHead = Pick("Socket_Head", socketHead);
                socketChest = Pick("Socket_Chest", socketChest);
                socketShoulderL = Pick("Socket_Shoulder_L", socketShoulderL);
                socketShoulderR = Pick("Socket_Shoulder_R", socketShoulderR);
                socketMainHand = Pick("Socket_MainHand", socketMainHand);
                socketOffHand = Pick("Socket_OffHand", socketOffHand);
                gripMainHand = Pick(HeroWeaponController.GripMainName, gripMainHand);
                gripOffHand = Pick(HeroWeaponController.GripOffName, gripOffHand);
                socketBack2H = Pick("Socket_Back_2H", socketBack2H);
                socketBackBow = Pick("Socket_Back_Bow", socketBackBow);
                socketBackShield = Pick("Socket_Back_Shield", socketBackShield);
                socketHipL = Pick("Socket_Hip_L", socketHipL);
                socketHipR = Pick("Socket_Hip_R", socketHipR);
                socketBelt = Pick("Socket_Belt", socketBelt);
                _bones = null;
            }
            finally { _binding = false; }
        }

        /// Whole skeleton, first transform of each name. Pass ignoreRoot to skip a gear instance being equipped.
        public Transform Bone(string name, Transform ignoreRoot = null)
        {
            if (string.IsNullOrEmpty(name)) return null;
            if (_bones == null) Rebuild(ignoreRoot);
            if (_bones.TryGetValue(name, out var t) && t && (ignoreRoot == null || (t != ignoreRoot && !t.IsChildOf(ignoreRoot))))
                return t;
            Rebuild(ignoreRoot);
            _bones.TryGetValue(name, out t);
            return t;
        }

        public void Rebuild(Transform ignoreRoot = null)
        {
            _bones = new Dictionary<string, Transform>();
            foreach (var t in GetComponentsInChildren<Transform>(true))
            {
                if (!t) continue;
                if (ignoreRoot && (t == ignoreRoot || t.IsChildOf(ignoreRoot))) continue;
                if (t.name.StartsWith("EquipSlot_")) continue;
                if (!_bones.ContainsKey(t.name)) _bones[t.name] = t;
            }
        }

        /// Rigid-attach transforms for the slot.
        /// Skinned slots still list the rigid-fallback anchors (Chest = Socket_Chest, one bone; pairs = one per side).
        /// Legs use LeftLowerLeg + RightLowerLeg (shin). Feet use the feet. Hands use the hands.
        /// MainHand / OffHand return Grip_* when the anchor exists.
        public Transform[] Anchors(HeroGearSlot slot)
        {
            if (!hips) Bind();
            switch (slot)
            {
                case HeroGearSlot.Head: return One(socketHead);
                case HeroGearSlot.Shoulders: return Pair(socketShoulderL, socketShoulderR);
                case HeroGearSlot.Chest: return One(socketChest);
                case HeroGearSlot.Hands: return Pair(Bone("LeftHand"), Bone("RightHand"));
                case HeroGearSlot.Legs: return Pair(Bone("LeftLowerLeg"), Bone("RightLowerLeg"));
                case HeroGearSlot.Feet: return Pair(Bone("LeftFoot"), Bone("RightFoot"));
                case HeroGearSlot.MainHand: return One(GripOrSocket(gripMainHand, socketMainHand, HeroWeaponController.GripMainName));
                case HeroGearSlot.OffHand: return One(GripOrSocket(gripOffHand, socketOffHand, HeroWeaponController.GripOffName));
                default: return new Transform[0];
            }
        }

        public bool Validate(out string missing)
        {
            if (!hips) Bind();
            var miss = new List<string>();
            void Need(string n, Transform t) { if (!t) miss.Add(n); }
            Need("Hips", hips);
            Need("Socket_Head", socketHead);
            Need("Socket_Chest", socketChest);
            Need("Socket_Shoulder_L", socketShoulderL);
            Need("Socket_Shoulder_R", socketShoulderR);
            Need("Socket_MainHand", socketMainHand);
            Need("Socket_OffHand", socketOffHand);
            Need(HeroWeaponController.GripMainName, gripMainHand ? gripMainHand : FindNamed(HeroWeaponController.GripMainName));
            Need(HeroWeaponController.GripOffName, gripOffHand ? gripOffHand : FindNamed(HeroWeaponController.GripOffName));
            Need("Socket_Back_2H", socketBack2H);
            Need("Socket_Back_Bow", socketBackBow);
            Need("Socket_Back_Shield", socketBackShield);
            Need("Socket_Hip_L", socketHipL);
            Need("Socket_Hip_R", socketHipR);
            Need("Socket_Belt", socketBelt);
            foreach (var n in new[] { "LeftHand", "RightHand", "LeftLowerLeg", "RightLowerLeg", "LeftFoot", "RightFoot", "UpperChest", "LeftLowerArm", "RightLowerArm" })
                if (!Bone(n)) miss.Add(n);
            missing = miss.Count == 0 ? "" : string.Join(", ", miss);
            return miss.Count == 0;
        }

        Transform Pick(string name, Transform current)
        {
            var t = FindNamed(name);
            return t ? t : current;
        }

        Transform FindNamed(string name)
        {
            foreach (var t in GetComponentsInChildren<Transform>(true))
            {
                if (t.name != name) continue;
                if (t.name.StartsWith("EquipSlot_")) continue;
                return t;
            }
            return null;
        }

        /// Grip anchor when it exists. Otherwise the raw socket, with one warning (older prefabs).
        Transform GripOrSocket(Transform grip, Transform socket, string gripName)
        {
            if (!grip) grip = FindNamed(gripName);
            if (grip) return grip;
            if (socket) Debug.LogWarning("[HeroRig] " + gripName + " missing; using " + socket.name);
            return socket;
        }

        static Transform[] One(Transform t) => t ? new[] { t } : new Transform[0];
        static Transform[] Pair(Transform a, Transform b)
        {
            if (a && b) return new[] { a, b };
            if (a) return new[] { a };
            if (b) return new[] { b };
            return new Transform[0];
        }

        /// Inspector summary. Not used at runtime.
        public string Describe()
        {
            var sb = new StringBuilder();
            void L(string n, Transform t) => sb.Append(n).Append('=').Append(t ? t.name : "-").Append(" parent=").Append(t && t.parent ? t.parent.name : "-").Append('\n');
            L("hips", hips); L("Socket_Head", socketHead); L("Socket_Chest", socketChest);
            L("Socket_Shoulder_L", socketShoulderL); L("Socket_Shoulder_R", socketShoulderR);
            L("Socket_MainHand", socketMainHand); L("Socket_OffHand", socketOffHand);
            L(HeroWeaponController.GripMainName, gripMainHand); L(HeroWeaponController.GripOffName, gripOffHand);
            L("Socket_Back_2H", socketBack2H); L("Socket_Back_Bow", socketBackBow); L("Socket_Back_Shield", socketBackShield);
            L("Socket_Hip_L", socketHipL); L("Socket_Hip_R", socketHipR); L("Socket_Belt", socketBelt);
            return sb.ToString();
        }
    }
}
