// Equips placeholder weapons to the skeleton sockets and drives the Animator "WeaponType" int parameter.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace HeroRig
{
    public enum WeaponType { Unarmed = 0, OneHand = 1, OneHandShield = 2, TwoHand = 3, Bow = 4, Staff = 5 }

    [Serializable]
    public class WeaponLoadout
    {
        public WeaponType type;
        public GameObject mainHand;   // -> Socket_MainHand
        public GameObject offHand;    // -> Socket_OffHand
        [Tooltip("Grip fit offset in HAND space (m): x = toward the fingers, y = back of hand, z = thumb side")]
        public Vector3 mainGripOffset, offGripOffset;
    }

    [Serializable]
    public class SocketBinding
    {
        public string name;
        public Transform socket;
        [Tooltip("Inverse(socket bind rotation) * root rotation, captured in the bind (T) pose")]
        public Quaternion bindCorrection = Quaternion.identity;
    }

    [DisallowMultipleComponent]
    [DefaultExecutionOrder(120)]
    public class HeroWeaponController : MonoBehaviour
    {
        public const string MainHandSocket = "Socket_MainHand";
        public const string OffHandSocket = "Socket_OffHand";
        public static readonly int WeaponTypeParam = Animator.StringToHash("WeaponType");

        public Animator animator;
        public WeaponType current = WeaponType.Unarmed;
        public List<WeaponLoadout> loadouts = new List<WeaponLoadout>();
        public List<SocketBinding> sockets = new List<SocketBinding>();
        [Tooltip("+1 if the weapon asset's local +Z is its back-of-hand side (set by the build from the shield mesh)")]
        public float dorsalSign = 1f;
        [Header("Demo")] public bool cycleInPlayMode = false;
        public float cycleSeconds = 2f;

        [SerializeField] GameObject _main, _off;
        float _t;
        bool _suppressMain, _suppressOff;

        public GameObject DemoMain => _main;
        public GameObject DemoOff => _off;

        /// Gear on MainHand / OffHand hides the built-in demo weapon without destroying it. Unequip passes false.
        public void SetDemoSuppressed(bool mainHand, bool suppressed)
        {
            if (mainHand) _suppressMain = suppressed; else _suppressOff = suppressed;
            ApplyDemoVisibility();
        }

        void ApplyDemoVisibility()
        {
            if (_main) _main.SetActive(!_suppressMain);
            if (_off) _off.SetActive(!_suppressOff);
        }

        void Start() { if (Application.isPlaying) Equip(current); }

        void Update()
        {
            if (!Application.isPlaying || !cycleInPlayMode) return;
            _t += Time.deltaTime;
            if (_t >= cycleSeconds) { _t = 0f; Cycle(); }
        }

        /// Call while the model is in its bind (T) pose. Records every Socket_* transform.
        public void CaptureBindPose()
        {
            sockets.Clear();
            foreach (var t in GetComponentsInChildren<Transform>(true))
                if (t.name.StartsWith("Socket_"))
                    sockets.Add(new SocketBinding { name = t.name, socket = t, bindCorrection = Quaternion.Inverse(t.rotation) * transform.rotation });
        }

        public SocketBinding GetSocket(string socketName) => sockets.Find(s => s.name == socketName);

        public const string GripMainName = "Grip_MainHand";
        public const string GripOffName = "Grip_OffHand";

        /// Weapon asset frame: +Y = along the grip (toward blade tip), dorsalSign*Z = back of hand.
        /// In the bind pose (palms down) the grip axis points character-forward and the back of the hand points up.
        public Quaternion GripRotation() => Quaternion.LookRotation(Vector3.up * dorsalSign, Vector3.forward);

        /// Hand-space grip offset with x mirrored for the off hand (right fingers +X, left fingers -X).
        public static Vector3 MirroredGrip(string socketName, Vector3 gripOffset)
        {
            float side = socketName == OffHandSocket ? -1f : 1f;
            return new Vector3(side * gripOffset.x, gripOffset.y, gripOffset.z);
        }

        /// Socket-local Grip_* frame: rotation = bindCorrection * GripRotation, position = bindCorrection * hand-space offset.
        public static void ApplyGripFrame(Transform grip, Quaternion bindCorrection, Quaternion gripRotation, Vector3 handSpaceOffset)
        {
            grip.localRotation = bindCorrection * gripRotation;
            grip.localPosition = bindCorrection * handSpaceOffset;
            grip.localScale = Vector3.one;
        }

        /// Direct child Grip_MainHand / Grip_OffHand, or null when this socket has no grip anchor.
        public static Transform GripUnder(Transform socket, string socketName)
        {
            if (!socket) return null;
            string n = socketName == MainHandSocket ? GripMainName : socketName == OffHandSocket ? GripOffName : null;
            return string.IsNullOrEmpty(n) ? null : socket.Find(n);
        }

        public void Equip(WeaponType type)
        {
            Unequip();
            current = type;
            var l = loadouts.Find(x => x.type == type);
            if (l != null)
            {
                if (l.mainHand && !BowAlreadyHeld(l.mainHand)) _main = Attach(l.mainHand, MainHandSocket, l.mainGripOffset);
                if (l.offHand && !BowAlreadyHeld(l.offHand)) _off = Attach(l.offHand, OffHandSocket, l.offGripOffset);
            }
            ApplyDemoVisibility();
            ApplyAnimator();
        }

        /// Sets WeaponType and enables the per-weapon full-body layer "<WeaponType>_Combat" (if the controller has one).
        /// Hands_Grip (fingers-only override) is weight 1 while a weapon is in the main hand, else 0.
        public void ApplyAnimator()
        {
            if (!animator || !animator.runtimeAnimatorController) return;
            animator.SetInteger(WeaponTypeParam, (int)current);
            foreach (WeaponType wt in Enum.GetValues(typeof(WeaponType)))
            {
                int li = animator.GetLayerIndex(wt + "_Combat");
                if (li > 0) animator.SetLayerWeight(li, wt == current ? 1f : 0f);
            }
            int grip = animator.GetLayerIndex("Hands_Grip");
            if (grip > 0) animator.SetLayerWeight(grip, MainHandWeapon() ? 1f : 0f);
        }

        /// Demo loadout with a main-hand prefab, or a HeroEquipment main-hand slot that is occupied.
        public bool MainHandWeapon()
        {
            if (current != WeaponType.Unarmed)
            {
                var l = loadouts.Find(x => x.type == current);
                if (l != null && l.mainHand) return true;
            }
            var eq = GetComponent<HeroEquipment>();
            var slot = eq ? eq.Slot(HeroGearSlot.MainHand) : null;
            return slot != null && slot.IsEquipped;
        }

        public void Cycle() => Equip((WeaponType)(((int)current + 1) % 6));

        /// <summary>
        /// DressHeld already put WPN_BOW_B01 on the rig. Start after a sex rebuild would Attach a second copy.
        /// Swords and shields still attach. A destroyed demo bow is ignored.
        /// </summary>
        bool BowAlreadyHeld(GameObject prefab)
        {
            if (prefab == null || prefab.name != "WPN_BOW_B01") return false;
            var all = GetComponentsInChildren<Transform>(true);
            for (int i = 0; i < all.Length; i++)
            {
                var t = all[i];
                if (t == null || t.name != "WPN_BOW_B01") continue;
                if (_main != null && t.gameObject == _main) continue;
                if (_off != null && t.gameObject == _off) continue;
                return true;
            }
            return false;
        }

        public GameObject Attach(GameObject prefab, string socketName) => Attach(prefab, socketName, Vector3.zero);

        public GameObject Attach(GameObject prefab, string socketName, Vector3 gripOffset)
        {
            var sb = GetSocket(socketName);
            if (sb == null || !sb.socket) { Debug.LogWarning("[HeroRig] missing socket " + socketName); return null; }
            var grip = GripUnder(sb.socket, socketName);
            var parent = grip ? grip : sb.socket;
            var go = Instantiate(prefab, parent, false);
            go.name = prefab.name;
            var rootPos = prefab.transform.localPosition;
            var rootRot = prefab.transform.localRotation;
            var rootScale = prefab.transform.localScale;
            if (grip)
            {
                // Grip_* already is C*G at the sword/shield offset. Other loadouts only add the difference,
                // so the world pose stays socket-space = C * G * assetRoot + loadoutOffset.
                var loadout = sb.bindCorrection * MirroredGrip(socketName, gripOffset);
                var delta = loadout - grip.localPosition;
                go.transform.localRotation = rootRot;
                go.transform.localPosition = rootPos + Quaternion.Inverse(grip.localRotation) * delta;
                go.transform.localScale = rootScale;
            }
            else
            {
                // keep the asset's own root transform (FBX axis conversion may live there): socket-space = C * G * assetRoot
                var q = sb.bindCorrection * GripRotation();
                go.transform.localPosition = q * rootPos;
                go.transform.localRotation = q * rootRot;
                go.transform.localScale = rootScale;
                // hand-space offset -> socket space (bind: right fingers +X, left fingers -X, back of hand +Y, thumb +Z)
                go.transform.localPosition += sb.bindCorrection * MirroredGrip(socketName, gripOffset);
            }
            return go;
        }

        public void Unequip()
        {
            foreach (var g in new[] { _main, _off })
            {
                if (!g) continue;
                if (Application.isPlaying) Destroy(g); else DestroyImmediate(g);
            }
            _main = _off = null;
        }

        /// <summary>One collider, once per armed swing. Point is on the swept segment.</summary>
        public event Action<HeroWeaponController, Collider, Vector3> BladeHit;

        Transform _hitGrip;
        Vector3 _hitBase;
        Vector3 _tipOffset;
        float _hitRadius = 0.06f;
        bool _hitArmed;
        bool _hitHasPrev;
        Vector3 _hitPrevA;
        Vector3 _hitPrevB;
        readonly HashSet<int> _hitOnce = new HashSet<int>();

        public bool HitWindowOpen => _hitArmed;
        public Vector3 LastBladeTip { get; private set; }
        public Vector3 LastBladeBase { get; private set; }

        /// <summary>Grip-space points, same axes as HeroWeaponItem.tipOffset / hitBase. Clears the per-swing set.</summary>
        public void ArmHit(Transform grip, Vector3 hitBase, Vector3 tipOffset, float hitRadius)
        {
            _hitGrip = grip;
            _hitBase = hitBase;
            _tipOffset = tipOffset;
            _hitRadius = hitRadius > 0f ? hitRadius : 0.06f;
            _hitArmed = grip != null;
            _hitHasPrev = false;
            _hitOnce.Clear();
        }

        public void CloseHit()
        {
            _hitArmed = false;
            _hitHasPrev = false;
            LastBladeTip = Vector3.zero;
            LastBladeBase = Vector3.zero;
        }

        void LateUpdate()
        {
            if (_hitArmed) SweepBlade();
        }

        void SweepBlade()
        {
            if (_hitGrip == null) return;
            Vector3 a = _hitGrip.TransformPoint(_hitBase);
            Vector3 b = _hitGrip.TransformPoint(_tipOffset);
            float travel = _hitHasPrev
                ? Vector3.Distance(_hitPrevA, a) + Vector3.Distance(_hitPrevB, b)
                : 0f;
            float stepLen = Mathf.Max(0.02f, _hitRadius);
            int steps = _hitHasPrev ? Mathf.Clamp(Mathf.CeilToInt(travel / stepLen), 1, 32) : 1;
            for (int s = 1; s <= steps; s++)
            {
                float u = s / (float)steps;
                Vector3 sa = _hitHasPrev ? Vector3.Lerp(_hitPrevA, a, u) : a;
                Vector3 sb = _hitHasPrev ? Vector3.Lerp(_hitPrevB, b, u) : b;
                var cols = Physics.OverlapCapsule(sa, sb, _hitRadius, Physics.AllLayers, QueryTriggerInteraction.Collide);
                for (int i = 0; i < cols.Length; i++)
                {
                    var col = cols[i];
                    if (col == null) continue;
                    if (col.transform.IsChildOf(transform.root)) continue;
                    int id = col.transform.root.GetInstanceID();
                    if (!_hitOnce.Add(id)) continue;
                    Vector3 point = ClosestOnSegment(sa, sb, col.bounds.center);
                    BladeHit?.Invoke(this, col, point);
                }
            }
            _hitPrevA = a;
            _hitPrevB = b;
            _hitHasPrev = true;
            LastBladeBase = a;
            LastBladeTip = b;
        }

        static Vector3 ClosestOnSegment(Vector3 a, Vector3 b, Vector3 p)
        {
            Vector3 ab = b - a;
            float d = ab.sqrMagnitude;
            if (d < 1e-8f) return a;
            float t = Mathf.Clamp01(Vector3.Dot(p - a, ab) / d);
            return a + ab * t;
        }
    }
}
