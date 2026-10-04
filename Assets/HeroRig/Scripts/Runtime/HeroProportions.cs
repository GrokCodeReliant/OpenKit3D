// Retarget-safe proportion controls for the HeroRig humanoid.
// Animation (Humanoid muscles) only drives bone ROTATIONS + hips position, so we change proportions with
// UNIFORM per-bone scales that are compensated on the child bones (no shear, animation untouched):
//   world segment scale  s(bone) = height        for Spine/Chest/UpperChest/Neck
//                                   limbLength    for UpperArm/LowerArm (+ twist children)
//                                   height*limb   for UpperLeg/LowerLeg (+ twist child)
//                                   1             for Hips, Head, Shoulders, Hands, Fingers, Feet, Toes, all Socket_*
//   localScale = s(bone) / s(parent)
// Bulk is a blend shape ("Bulk") baked by the Blender generator. uniformScale scales the root.
// After scaling, the hips are raised/lowered so the lowest foot stays on the ground (legs got longer/shorter).
using System.Collections.Generic;
using UnityEngine;

namespace HeroRig
{
    [ExecuteAlways, DisallowMultipleComponent, DefaultExecutionOrder(900)]
    public class HeroProportions : MonoBehaviour
    {
        [Range(0.5f, 1.6f)] public float uniformScale = 1f;
        [Tooltip("Torso + leg length factor")] [Range(0.85f, 1.15f)] public float height = 1f;
        [Tooltip("Arm + leg length factor")] [Range(0.85f, 1.15f)] public float limbLength = 1f;
        [Tooltip("Girth blend shape 0..1")] [Range(0f, 1f)] public float bulk = 0f;
        public bool keepFeetGrounded = true;
        public Animator animator;

        public enum Preset { Small, Medium, Large }

        readonly Dictionary<Transform, float> _map = new Dictionary<Transform, float>();
        SkinnedMeshRenderer[] _smrs;
        Transform _hips;
        Vector3 _lastBase, _lastWritten;
        bool _hasLast;
        Vector2 _mapKey;

        public void SetPreset(Preset p)
        {
            switch (p)
            {
                case Preset.Small: uniformScale = 0.82f; height = 0.9f; limbLength = 0.92f; bulk = 0.0f; break;
                case Preset.Medium: uniformScale = 1.0f; height = 1.0f; limbLength = 1.0f; bulk = 0.3f; break;
                case Preset.Large: uniformScale = 1.15f; height = 1.08f; limbLength = 1.07f; bulk = 1.0f; break;
            }
        }

        void OnEnable() { if (!animator) animator = GetComponent<Animator>(); _map.Clear(); }
        void OnValidate() { _map.Clear(); }
        void LateUpdate() { Apply(); }

        void BuildMap()
        {
            _map.Clear();
            _hips = animator.GetBoneTransform(HumanBodyBones.Hips);
            float h = height, l = limbLength;
            void M(HumanBodyBones b, float s) { var t = animator.GetBoneTransform(b); if (t) _map[t] = s; }
            M(HumanBodyBones.Hips, 1f);
            M(HumanBodyBones.Spine, h); M(HumanBodyBones.Chest, h); M(HumanBodyBones.UpperChest, h); M(HumanBodyBones.Neck, h);
            M(HumanBodyBones.Head, 1f);
            M(HumanBodyBones.LeftShoulder, 1f); M(HumanBodyBones.RightShoulder, 1f);
            M(HumanBodyBones.LeftUpperArm, l); M(HumanBodyBones.RightUpperArm, l);
            M(HumanBodyBones.LeftLowerArm, l); M(HumanBodyBones.RightLowerArm, l);
            M(HumanBodyBones.LeftHand, 1f); M(HumanBodyBones.RightHand, 1f);
            M(HumanBodyBones.LeftUpperLeg, h * l); M(HumanBodyBones.RightUpperLeg, h * l);
            M(HumanBodyBones.LeftLowerLeg, h * l); M(HumanBodyBones.RightLowerLeg, h * l);
            M(HumanBodyBones.LeftFoot, 1f); M(HumanBodyBones.RightFoot, 1f);
            if (_smrs == null) _smrs = GetComponentsInChildren<SkinnedMeshRenderer>(true);
        }

        public float LegScale => height * limbLength;

        /// Equipped armour adds SkinnedMeshRenderers after the cache was built. Clear it so Bulk is driven on them too.
        public void RefreshRenderers() { _smrs = null; }

        public void Apply()
        {
            if (!animator) animator = GetComponent<Animator>();
            if (!animator || !animator.isHuman) return;
            var key = new Vector2(height, limbLength);
            if (_map.Count == 0 || !_hips || key != _mapKey) { BuildMap(); _mapKey = key; }
            if (_smrs == null) _smrs = GetComponentsInChildren<SkinnedMeshRenderer>(true);
            transform.localScale = Vector3.one * uniformScale;
            Scale(_hips, 1f, 1f);
            foreach (var smr in _smrs)
            {
                if (!smr || !smr.sharedMesh) continue;
                int i = smr.sharedMesh.GetBlendShapeIndex("Bulk");
                if (i >= 0) smr.SetBlendShapeWeight(i, Mathf.Clamp01(bulk) * 100f);
            }
            if (keepFeetGrounded) Ground();
        }

        void Scale(Transform t, float parentS, float selfS)
        {
            t.localScale = Vector3.one * (selfS / parentS);
            if (t.name.StartsWith("Socket_")) return; // don't touch attached weapons
            for (int i = 0; i < t.childCount; i++)
            {
                var c = t.GetChild(i);
                float s;
                if (_map.TryGetValue(c, out var v)) s = v;
                else if (c.name.StartsWith("Socket_")) s = 1f;
                else s = selfS; // twist bones, fingers, toes inherit
                Scale(c, selfS, s);
            }
        }

        void Ground()
        {
            var cur = _hips.localPosition;
            if (_hasLast && cur == _lastWritten) cur = _lastBase; // animator did not run since our last write
            _lastBase = cur;
            _hips.localPosition = cur;
            var lu = animator.GetBoneTransform(HumanBodyBones.LeftUpperLeg);
            var ru = animator.GetBoneTransform(HumanBodyBones.RightUpperLeg);
            var lf = animator.GetBoneTransform(HumanBodyBones.LeftFoot);
            var rf = animator.GetBoneTransform(HumanBodyBones.RightFoot);
            Vector3 up = transform.up;
            float ly = Vector3.Dot(lf.position, up), ry = Vector3.Dot(rf.position, up);
            float e = ly <= ry ? Vector3.Dot(lu.position - lf.position, up) : Vector3.Dot(ru.position - rf.position, up);
            float s = LegScale;
            // the hip->ankle chain is uniformly scaled by s about the hip joint: unscaled extent = e/s
            float delta = e * (1f - 1f / s);
            _hips.position += up * delta;
            _lastWritten = _hips.localPosition;
            _hasLast = true;
        }
    }
}
