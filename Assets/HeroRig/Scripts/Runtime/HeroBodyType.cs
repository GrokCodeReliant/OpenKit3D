// Body types: exactly two per sex, as ONE blend shape on the same mesh + skeleton
//   male:   Lean / Athletic (base mesh)  <->  Strong / Muscled  (blend shape "BodyType_Strong")
//   female: Petite (base mesh)           <->  Busty / fuller    (blend shape "BodyType_Busty")
// The weight is applied to every SkinnedMeshRenderer under the hero that carries the shape (Body, Clothing and any
// armour built with build_rig.transfer_body_shapes), so clothing follows the body without clipping.
// Overall height stays on HeroProportions; correctives (HeroDeformDriver) add on top of the body type.
using UnityEngine;

namespace HeroRig
{
    [ExecuteAlways, DisallowMultipleComponent]
    public class HeroBodyType : MonoBehaviour
    {
        public const string ShapePrefix = "BodyType_";
        public enum Preset { Base = 0, Full = 1 }

        [Tooltip("0 = base body (male Lean / female Petite), 1 = full alternate body (male Strong / female Busty)")]
        [Range(0, 1)] public float weight;

        float _applied = -1f;
        int _smrCount = -1;

        /// "Lean"/"Petite" for the base, "Strong"/"Busty" for the blend shape (read from the mesh)
        public string AlternateName { get { var s = FindShape(out _, out _); return s != null ? s.Substring(ShapePrefix.Length) : "-"; } }
        public string BaseName => AlternateName == "Strong" ? "Lean" : AlternateName == "Busty" ? "Petite" : "Base";

        public void Set(Preset p) { weight = p == Preset.Full ? 1f : 0f; Apply(); }
        public void Set(float w) { weight = Mathf.Clamp01(w); Apply(); }

        string FindShape(out SkinnedMeshRenderer smr, out int index)
        {
            foreach (var r in GetComponentsInChildren<SkinnedMeshRenderer>(true))
            {
                var m = r.sharedMesh; if (!m) continue;
                for (int i = 0; i < m.blendShapeCount; i++)
                {
                    var n = m.GetBlendShapeName(i);
                    if (n.StartsWith(ShapePrefix)) { smr = r; index = i; return n; }
                }
            }
            smr = null; index = -1; return null;
        }

        /// sets the body-type blend shape on every skinned mesh that has it; returns how many meshes were driven
        public int Apply()
        {
            string shape = FindShape(out _, out _);
            int n = 0;
            var smrs = GetComponentsInChildren<SkinnedMeshRenderer>(true);
            if (shape != null)
                foreach (var r in smrs)
                {
                    if (!r.sharedMesh) continue;
                    int i = r.sharedMesh.GetBlendShapeIndex(shape);
                    if (i >= 0) { r.SetBlendShapeWeight(i, Mathf.Clamp01(weight) * 100f); n++; }
                }
            _applied = weight; _smrCount = smrs.Length;
            return n;
        }

        void OnEnable() => Apply();
        void OnValidate() => Apply();
        void LateUpdate()
        {
            // re-apply when the weight changes or armour / clothing meshes are added at runtime
            if (!Mathf.Approximately(_applied, weight) || (Time.frameCount % 30 == 0 && GetComponentsInChildren<SkinnedMeshRenderer>(true).Length != _smrCount)) Apply();
        }

        [ContextMenu("Body type: base")] void CtxBase() => Set(Preset.Base);
        [ContextMenu("Body type: full alternate")] void CtxFull() => Set(Preset.Full);
    }
}
