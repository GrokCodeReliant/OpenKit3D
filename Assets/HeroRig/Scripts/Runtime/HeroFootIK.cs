using UnityEngine;

namespace HeroRig
{
    /// <summary>
    /// Foot planting on the Animator IK pass. Combat clips drive LeftFootPlant / RightFootPlant.
    /// The lock starts at the animated foot, then the target stays within 6 cm vertical and 12 cm
    /// horizontal of that foot, inside the leg's reach, and no more bent than the clip's knee + 10Â°.
    /// Weight eases in from 0. A LateUpdate pass (after HeroProportions) compares the IK pose with
    /// the same-frame FK pose in proportioned space and restores FK if the leg collapses.
    /// Hip-to-ankle is UpperLeg to Foot. Knee bend is the angle at the knee, 0 = straight.
    /// </summary>
    [RequireComponent(typeof(Animator)), DisallowMultipleComponent, DefaultExecutionOrder(1100)]
    public class HeroFootIK : MonoBehaviour
    {
        public Animator animator;
        public string layerName = "OneHandShield_Combat";
        public string leftPlantParam = "LeftFootPlant", rightPlantParam = "RightFootPlant";
        [Range(0, 1)] public float maxWeight = 1f;
        [Tooltip("fade in/out time of the IK weight (s)")] public float blendTime = 0.12f;
        [Tooltip("release a locked foot when it gets this far (horizontally) from the hips")] public float releaseDistance = 0.55f;
        [Tooltip("max vertical correction from the animated foot (m)")] public float maxVertical = 0.06f;
        [Tooltip("max horizontal correction from the animated foot (m)")] public float maxHorizontal = 0.12f;
        public LayerMask groundMask = ~0;
        public float rayUp = 0.5f, rayDown = 1.0f;
        [Tooltip("legacy lock: groundY + ankle height above the root, no reach clamp, no safety restore. Capture only. Shipped prefabs leave this off.")]
        public bool legacy;

        public int LockCount { get; private set; }
        public float LeftWeight => _l != null ? _l.w : 0f;
        public float RightWeight => _r != null ? _r.w : 0f;
        public float MinReachRatio { get; private set; } = 1f;
        public float MaxFkBend { get; private set; }
        public float MaxIkBend { get; private set; }
        public float MaxKneeExcess { get; private set; }
        public float PeakWeight { get; private set; }
        public float WatchedSeconds { get; private set; }

        class Foot
        {
            public AvatarIKGoal goal;
            public HumanBodyBones upper, lower, bone;
            public int param;
            public bool locked;
            public Vector3 pos;
            public float w;
            public bool fkValid;
            public Quaternion fkUpper, fkLower, fkFoot;
        }

        Foot _l, _r;
        int _layer = -2, _frame = -1;
        bool _hasParams, _watching;
        float _watchStart = -1f;

        public void BeginWatch()
        {
            _watching = true;
            _watchStart = -1f;
            WatchedSeconds = 0f;
            MinReachRatio = 1f;
            MaxFkBend = 0f;
            MaxIkBend = 0f;
            MaxKneeExcess = 0f;
            PeakWeight = 0f;
        }

        void OnEnable() { _l = null; _layer = -2; }

        void Init()
        {
            if (!animator) animator = GetComponent<Animator>();
            _l = new Foot
            {
                goal = AvatarIKGoal.LeftFoot, upper = HumanBodyBones.LeftUpperLeg,
                lower = HumanBodyBones.LeftLowerLeg, bone = HumanBodyBones.LeftFoot,
                param = Animator.StringToHash(leftPlantParam)
            };
            _r = new Foot
            {
                goal = AvatarIKGoal.RightFoot, upper = HumanBodyBones.RightUpperLeg,
                lower = HumanBodyBones.RightLowerLeg, bone = HumanBodyBones.RightFoot,
                param = Animator.StringToHash(rightPlantParam)
            };
            _hasParams = false;
            if (animator && animator.runtimeAnimatorController)
            {
                int found = 0;
                foreach (var p in animator.parameters)
                    if (p.type == AnimatorControllerParameterType.Float && (p.name == leftPlantParam || p.name == rightPlantParam)) found++;
                _hasParams = found == 2;
            }
            _layer = animator && !string.IsNullOrEmpty(layerName) ? animator.GetLayerIndex(layerName) : -1;
        }

        void OnAnimatorIK(int layerIndex)
        {
            if (!Application.isPlaying) return;
            if (_l == null || _layer == -2) Init();
            if (!animator || !animator.isHuman || !_hasParams) return;
            if (_layer >= 0 && layerIndex != _layer) return;
            bool advance = _frame != Time.frameCount;
            _frame = Time.frameCount;
            if (advance) { Capture(_l); Capture(_r); }
            Solve(_l, advance);
            Solve(_r, advance);
        }

        void Capture(Foot f)
        {
            var up = animator.GetBoneTransform(f.upper);
            var lo = animator.GetBoneTransform(f.lower);
            var ft = animator.GetBoneTransform(f.bone);
            f.fkValid = up && lo && ft;
            if (!f.fkValid) return;
            f.fkUpper = up.localRotation;
            f.fkLower = lo.localRotation;
            f.fkFoot = ft.localRotation;
        }

        void Solve(Foot f, bool advance)
        {
            if (legacy) { SolveLegacy(f, advance); return; }
            var ft = animator.GetBoneTransform(f.bone);
            if (!ft) return;
            if (advance)
            {
                float plant = animator.GetFloat(f.param);
                if (!f.locked && plant > 0.5f && f.w < 0.01f)
                {
                    f.pos = ft.position;
                    if (Ground(ft.position, out float gy))
                        f.pos.y = Mathf.Clamp(gy + 0.012f, ft.position.y - maxVertical, ft.position.y + maxVertical);
                    f.locked = true;
                    LockCount++;
                }
                else if (f.locked && plant < 0.5f) f.locked = false;
                if (f.locked)
                {
                    var up = animator.GetBoneTransform(f.upper);
                    var lo = animator.GetBoneTransform(f.lower);
                    var hips = animator.GetBoneTransform(HumanBodyBones.Hips);
                    Vector3 hip = up ? up.position : (hips ? hips.position : transform.position);
                    Vector3 drift = f.pos - ft.position; drift.y = 0f;
                    Vector3 fromHip = f.pos - (hips ? hips.position : transform.position); fromHip.y = 0f;
                    float limit = releaseDistance * Mathf.Max(0.5f, animator.humanScale);
                    if (drift.magnitude > maxHorizontal || fromHip.magnitude > limit) f.locked = false;
                    else if (up && lo)
                    {
                        float a = Vector3.Distance(hip, lo.position);
                        float b = Vector3.Distance(lo.position, ft.position);
                        float dFk = Vector3.Distance(hip, ft.position);
                        float knee = Vector3.Angle(lo.position - hip, ft.position - lo.position);
                        if (Ground(ft.position, out float gy))
                            f.pos.y = gy + 0.012f;
                        f.pos = ClampTarget(f.pos, ft.position, hip, a, b, dFk, knee);
                    }
                }
                float step = Mathf.Min(Time.deltaTime, 1f / 30f) / Mathf.Max(1e-3f, blendTime);
                f.w = Mathf.MoveTowards(f.w, f.locked ? maxWeight : 0f, step);
                if (f.w > PeakWeight) PeakWeight = f.w;
            }
            animator.SetIKPositionWeight(f.goal, f.w);
            animator.SetIKRotationWeight(f.goal, 0f);
            if (f.w > 0f) animator.SetIKPosition(f.goal, f.pos);
        }

        Vector3 ClampTarget(Vector3 plant, Vector3 fkFoot, Vector3 hip, float a, float b, float dFk, float kneeFk)
        {
            Vector3 delta = plant - fkFoot;
            Vector3 horiz = delta; horiz.y = 0f;
            if (horiz.magnitude > maxHorizontal) horiz *= maxHorizontal / Mathf.Max(1e-5f, horiz.magnitude);
            float dy = Mathf.Clamp(delta.y, -maxVertical, maxVertical);
            Vector3 boxed = fkFoot + horiz + Vector3.up * dy;
            float bendLimit = Mathf.Clamp(kneeFk + 10f, 0f, 170f);
            float cMinKnee = Mathf.Sqrt(Mathf.Max(0f, a * a + b * b + 2f * a * b * Mathf.Cos(bendLimit * Mathf.Deg2Rad)));
            float cMin = Mathf.Max(cMinKnee, 0.85f * dFk);
            float cMax = 0.98f * (a + b);
            if (cMin > cMax) cMin = cMax;
            Vector3 best = fkFoot;
            for (int i = 8; i >= 0; i--)
            {
                Vector3 cand = Vector3.Lerp(fkFoot, boxed, i / 8f);
                float dist = Vector3.Distance(hip, cand);
                if (dist + 1e-4f >= cMin && dist <= cMax + 1e-4f) { best = cand; break; }
            }
            return best;
        }

        /// Legacy foot solver. Locks the world foot and rebases Y to groundY + (ankleY - rootY). No reach clamp.
        void SolveLegacy(Foot f, bool advance)
        {
            var t = animator.GetBoneTransform(f.bone);
            if (!t) return;
            if (advance)
            {
                float plant = animator.GetFloat(f.param);
                if (!f.locked && plant > 0.5f && f.w < 0.01f)
                {
                    f.pos = t.position;
                    float above = f.pos.y - transform.position.y;
                    if (Ground(f.pos, out float groundY)) f.pos.y = groundY + above;
                    f.locked = true;
                    LockCount++;
                }
                else if (f.locked && plant < 0.5f) f.locked = false;
                if (f.locked)
                {
                    var hips = animator.GetBoneTransform(HumanBodyBones.Hips);
                    var d = f.pos - (hips ? hips.position : transform.position);
                    d.y = 0f;
                    if (d.magnitude > 0.55f * Mathf.Max(0.5f, animator.humanScale)) f.locked = false;
                }
                f.w = Mathf.MoveTowards(f.w, f.locked ? maxWeight : 0f, Time.deltaTime / Mathf.Max(1e-3f, 0.08f));
                if (f.w > PeakWeight) PeakWeight = f.w;
            }
            animator.SetIKPositionWeight(f.goal, f.w);
            animator.SetIKRotationWeight(f.goal, 0f);
            if (f.w > 0f) animator.SetIKPosition(f.goal, f.pos);
        }

        void LateUpdate()
        {
            if (!Application.isPlaying || _l == null || !animator || !animator.isHuman) return;
            Evaluate(_l);
            Evaluate(_r);
            if (_watching && LockCount > 0)
            {
                if (_watchStart < 0f) _watchStart = Time.time;
                WatchedSeconds = Time.time - _watchStart;
            }
        }

        void Evaluate(Foot f)
        {
            if (!f.fkValid || f.w < 0.01f) return;
            var up = animator.GetBoneTransform(f.upper);
            var lo = animator.GetBoneTransform(f.lower);
            var ft = animator.GetBoneTransform(f.bone);
            if (!up || !lo || !ft) return;
            Quaternion ikU = up.localRotation, ikL = lo.localRotation, ikF = ft.localRotation;
            up.localRotation = f.fkUpper; lo.localRotation = f.fkLower; ft.localRotation = f.fkFoot;
            float fkDist = Vector3.Distance(up.position, ft.position);
            float fkBend = Vector3.Angle(lo.position - up.position, ft.position - lo.position);
            up.localRotation = ikU; lo.localRotation = ikL; ft.localRotation = ikF;
            float ikDist = Vector3.Distance(up.position, ft.position);
            float ikBend = Vector3.Angle(lo.position - up.position, ft.position - lo.position);
            float ratio = fkDist > 1e-4f ? ikDist / fkDist : 1f;
            bool bad = ratio < 0.85f || ikBend > fkBend + 10f;
            if (_watching && LockCount > 0)
            {
                if (ratio < MinReachRatio) MinReachRatio = ratio;
                if (fkBend > MaxFkBend) MaxFkBend = fkBend;
                if (ikBend > MaxIkBend) MaxIkBend = ikBend;
                float excess = ikBend - fkBend;
                if (excess > MaxKneeExcess) MaxKneeExcess = excess;
            }
            if (legacy) return;
            if (!bad) return;
            up.localRotation = f.fkUpper;
            lo.localRotation = f.fkLower;
            ft.localRotation = f.fkFoot;
            f.w = 0f;
            f.locked = false;
            animator.SetIKPositionWeight(f.goal, 0f);
        }

        bool Ground(Vector3 p, out float y)
        {
            y = 0f;
            var hits = Physics.RaycastAll(p + Vector3.up * rayUp, Vector3.down, rayUp + rayDown, groundMask, QueryTriggerInteraction.Ignore);
            float best = float.MaxValue; bool ok = false;
            foreach (var h in hits)
            {
                if (!h.transform) continue;
                if (h.transform == transform || h.transform.IsChildOf(transform)) continue;
                if (h.distance < best) { best = h.distance; y = h.point.y; ok = true; }
            }
            return ok;
        }
    }
}
