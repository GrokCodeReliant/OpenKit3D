// Deformation driver (runs after the Animator every frame):
//  * shoulder helper bones (Left/RightShoulderHelper, non-Humanoid, child of the Shoulder) follow a fraction of the
//    upper-arm rotation -> deltoid / sleeve volume instead of a rigid pivot;
//  * forearm twist bones (Left/RightLowerArmTwist) take a share of the hand roll -> roll is spread along the forearm;
//  * corrective blend shapes CR_* (authored in Blender as dual-quaternion minus linear-blend skinning at a reference
//    pose) are weighted from the live joint swing: 0 at bind, 1 at the reference pose (clamped to correctiveMax).
// FBX drivers do not survive export, so the drivers live here. Call Apply() manually when sampling the Animator in edit mode.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace HeroRig
{
    [DisallowMultipleComponent, DefaultExecutionOrder(900)]
    public class HeroDeformDriver : MonoBehaviour
    {
        [Serializable]
        public class Corrective
        {
            public string shape;
            public Transform parent, bone, child;
            [Tooltip("bone->child direction at bind, in the parent's local space")] public Vector3 bindDir;
            [Tooltip("reference-pose direction (weight 1), in the parent's local space")] public Vector3 targetDir;
            public float weight;
            [NonSerialized] public int index = -2;
        }

        [Serializable] public class Helper { public Transform helper, follow; public Quaternion helperBind, followBind; }
        [Serializable] public class Twist { public Transform twist, hand; public Quaternion twistBind, handBind; public Vector3 axis; }

        public Animator animator;
        public SkinnedMeshRenderer body;
        [Tooltip("pass 3: other skinned meshes (Clothing, armour) that carry the same CR_* shapes - driven with the same weights")]
        public List<SkinnedMeshRenderer> layers = new List<SkinnedMeshRenderer>();
        [Range(0, 1)] public float shoulderHelperFollow = 0.5f;
        [Range(0, 1)] public float forearmTwistShare = 0.5f;
        [Range(0, 1.5f)] public float correctiveMax = 1.25f;
        public bool driveInPlayMode = true;
        public List<Corrective> correctives = new List<Corrective>();
        public List<Helper> helpers = new List<Helper>();
        public List<Twist> twists = new List<Twist>();

        /// Reference poses (Unity character axes: x right, y up, z forward; sx = -1 left, +1 right).
        /// MUST match corrective_specs() in blender/build_rig.py.
        public static IEnumerable<(string shape, string parent, string bone, string child, Vector3 target)> Specs()
        {
            float c110 = Mathf.Cos(110f * Mathf.Deg2Rad), s110 = Mathf.Sin(110f * Mathf.Deg2Rad);
            foreach (var (side, sx) in new[] { ("Left", -1f), ("Right", 1f) })
            {
                string L = sx < 0 ? "L" : "R";
                yield return ("CR_Knee_" + L, side + "UpperLeg", side + "LowerLeg", side + "Foot", new Vector3(0, -c110, -s110));
                yield return ("CR_Elbow_" + L, side + "UpperArm", side + "LowerArm", side + "Hand", new Vector3(sx * c110, 0, s110));
                yield return ("CR_HipFlex_" + L, "Hips", side + "UpperLeg", side + "LowerLeg", new Vector3(0, 0, 1));
                yield return ("CR_ShoulderDown_" + L, side + "Shoulder", side + "UpperArm", side + "LowerArm", new Vector3(sx * .342f, -.940f, 0));
                yield return ("CR_ShoulderUp_" + L, side + "Shoulder", side + "UpperArm", side + "LowerArm", new Vector3(sx * .5f, .866f, 0));
                yield return ("CR_ShoulderFwd_" + L, side + "Shoulder", side + "UpperArm", side + "LowerArm", new Vector3(sx * .174f, 0, .985f));
            }
        }

        /// Editor/build time: call on an instance in its BIND pose with the root at identity rotation.
        public void Setup()
        {
            if (!animator) animator = GetComponent<Animator>();
            var smrs = GetComponentsInChildren<SkinnedMeshRenderer>(true);
            if (!body) foreach (var r in smrs) if (r.name == "Body") body = r;
            if (!body && smrs.Length > 0) body = smrs[0];
            layers.Clear();
            foreach (var r in smrs) if (r != body) RegisterLayer(r);
            var map = new Dictionary<string, Transform>();
            foreach (var t in GetComponentsInChildren<Transform>(true)) if (!map.ContainsKey(t.name)) map[t.name] = t;
            correctives.Clear(); helpers.Clear(); twists.Clear();
            foreach (var s in Specs())
            {
                if (!map.TryGetValue(s.parent, out var p) || !map.TryGetValue(s.bone, out var b) || !map.TryGetValue(s.child, out var c)) continue;
                correctives.Add(new Corrective
                {
                    shape = s.shape, parent = p, bone = b, child = c,
                    bindDir = p.InverseTransformDirection(c.position - b.position).normalized,
                    targetDir = p.InverseTransformDirection(transform.TransformDirection(s.target)).normalized,
                });
            }
            foreach (var side in new[] { "Left", "Right" })
            {
                if (map.TryGetValue(side + "ShoulderHelper", out var h) && map.TryGetValue(side + "UpperArm", out var u))
                    helpers.Add(new Helper { helper = h, follow = u, helperBind = h.localRotation, followBind = u.localRotation });
                if (map.TryGetValue(side + "LowerArmTwist", out var tw) && map.TryGetValue(side + "Hand", out var hd))
                    twists.Add(new Twist { twist = tw, hand = hd, twistBind = tw.localRotation, handBind = hd.localRotation, axis = hd.localPosition.normalized });
            }
        }

        /// pass 3: drive the corrective shapes on another mesh too (clothing / armour made by transfer_body_shapes)
        public bool RegisterLayer(SkinnedMeshRenderer r)
        {
            if (!r || !r.sharedMesh || layers.Contains(r)) return false;
            foreach (var s in Specs()) if (r.sharedMesh.GetBlendShapeIndex(s.shape) >= 0) { layers.Add(r); return true; }
            return false;
        }

        /// Drop an equipped armour renderer. Safe if it was never registered.
        public bool UnregisterLayer(SkinnedMeshRenderer r)
        {
            if (!r) return false;
            return layers.Remove(r);
        }

        void SetLayers(string shape, float w)
        {
            for (int i = 0; i < layers.Count; i++)
            {
                var r = layers[i]; if (!r || !r.sharedMesh) continue;
                int k = r.sharedMesh.GetBlendShapeIndex(shape);
                if (k >= 0) r.SetBlendShapeWeight(k, w);
            }
        }

        public int ShapeCount
        {
            get { int n = 0; if (body && body.sharedMesh) foreach (var c in correctives) if (body.sharedMesh.GetBlendShapeIndex(c.shape) >= 0) n++; return n; }
        }

        void LateUpdate()
        {
            if (Application.isPlaying && driveInPlayMode) Apply();
        }

        /// weight from the swing of bone->child relative to the parent: angle ratio x direction match
        public static float SwingWeight(Vector3 bind, Vector3 target, Vector3 cur, float max)
        {
            float a = Vector3.Angle(bind, cur), at = Vector3.Angle(bind, target);
            if (at < 1e-3f || a < 1e-3f) return 0f;
            var sc = cur - bind * Vector3.Dot(bind, cur); var st = target - bind * Vector3.Dot(bind, target);
            if (sc.sqrMagnitude < 1e-10f || st.sqrMagnitude < 1e-10f) return 0f;
            float dir = Mathf.Max(0f, Vector3.Dot(sc.normalized, st.normalized));
            return Mathf.Clamp(a / at, 0f, max) * dir;
        }

        /// helpers/twists back to bind, all correctives 0 (A/B comparison: "driver off")
        public void ResetToBind()
        {
            foreach (var h in helpers) if (h.helper) h.helper.localRotation = h.helperBind;
            foreach (var t in twists) if (t.twist) t.twist.localRotation = t.twistBind;
            if (!body || !body.sharedMesh) return;
            foreach (var c in correctives)
            {
                if (c.index == -2) c.index = body.sharedMesh.GetBlendShapeIndex(c.shape);
                if (c.index >= 0) body.SetBlendShapeWeight(c.index, 0f);
                SetLayers(c.shape, 0f);
                c.weight = 0f;
            }
        }

        public void Apply()
        {
            foreach (var h in helpers)
            {
                if (!h.helper || !h.follow) continue;
                var d = h.follow.localRotation * Quaternion.Inverse(h.followBind);
                h.helper.localRotation = Quaternion.Slerp(Quaternion.identity, d, shoulderHelperFollow) * h.helperBind;
            }
            foreach (var t in twists)
            {
                if (!t.twist || !t.hand) continue;
                var dq = t.hand.localRotation * Quaternion.Inverse(t.handBind);
                float proj = Vector3.Dot(new Vector3(dq.x, dq.y, dq.z), t.axis);
                float ang = 2f * Mathf.Atan2(proj, dq.w) * Mathf.Rad2Deg;
                if (ang > 180f) ang -= 360f; else if (ang < -180f) ang += 360f;
                t.twist.localRotation = Quaternion.AngleAxis(forearmTwistShare * ang, t.axis) * t.twistBind;
            }
            if (!body || !body.sharedMesh) return;
            var mesh = body.sharedMesh;
            foreach (var c in correctives)
            {
                if (c.index == -2) c.index = mesh.GetBlendShapeIndex(c.shape);
                if (c.index < 0 || !c.parent || !c.bone || !c.child) continue;
                var cur = c.parent.InverseTransformDirection(c.child.position - c.bone.position).normalized;
                c.weight = SwingWeight(c.bindDir, c.targetDir, cur, correctiveMax);
                body.SetBlendShapeWeight(c.index, c.weight * 100f);
                SetLayers(c.shape, c.weight * 100f);
            }
        }
    }
}
