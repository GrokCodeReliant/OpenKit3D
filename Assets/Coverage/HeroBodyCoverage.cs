using System.Collections.Generic;
using HeroRig;
using UnityEngine;

namespace OpenKitDungeon
{
    /// <summary>
    /// Swaps the Body renderer's materials onto the coverage shader and sets _HiddenRegions
    /// to the OR of equipped parts' covers. Unequipped â†’ 0. Identity when the mask is 0.
    /// </summary>
    [DisallowMultipleComponent]
    public class HeroBodyCoverage : MonoBehaviour
    {
        public const string HiddenRegions = "_HiddenRegions";
        public const string CoverageInset = "_CoverageInset";
        public const float DefaultInset = 0.8f;
        public const string TemplatePath = "Assets/Coverage/Materials/M_BodyCoverage.mat";
        public const string TablePath = "Assets/Coverage/Data/CoverageTable.asset";

        static readonly Dictionary<int, Mesh> RuntimeCopies = new Dictionary<int, Mesh>();
        static bool warned;

        [SerializeField] Material template;
        [SerializeField] CoverageTable table;

        SkinnedMeshRenderer body;
        Material[] sources;
        Material[] coverage;
        int mask = int.MinValue;

        public int Mask => mask == int.MinValue ? 0 : mask;
        public Material Template => template;
        public CoverageTable Table => table;
        public Material[] SourceMaterials => sources;

        public void Configure(Material coverageTemplate, CoverageTable coverageTable)
        {
            if (coverageTemplate != null) template = coverageTemplate;
            if (coverageTable != null) table = coverageTable;
        }

        public void Reapply()
        {
            ResolveAssets();
            var next = FindBody();
            if (next == null) return;
            if (next != body)
            {
                body = next;
                sources = null;
                coverage = null;
                mask = int.MinValue;
            }
            EnsureMesh(body);
            EnsureMaterials(body);
            SetMask(ComputeMask());
        }

        public void SetMask(int hidden)
        {
            mask = hidden;
            if (coverage == null) return;
            for (int i = 0; i < coverage.Length; i++)
            {
                if (coverage[i] == null || !coverage[i].HasProperty(HiddenRegions)) continue;
                coverage[i].SetFloat(HiddenRegions, hidden);
                coverage[i].SetFloat(CoverageInset, DefaultInset);
            }
            if (body != null && body.sharedMaterials != coverage)
                body.sharedMaterials = coverage;
        }

        public void UseSourceMaterials(bool source)
        {
            if (body == null) return;
            if (source && sources != null) body.sharedMaterials = sources;
            else if (!source && coverage != null) body.sharedMaterials = coverage;
        }

        void ResolveAssets()
        {
            if (template != null && table != null) return;
#if UNITY_EDITOR
            if (template == null)
                template = UnityEditor.AssetDatabase.LoadAssetAtPath<Material>(TemplatePath);
            if (table == null)
                table = UnityEditor.AssetDatabase.LoadAssetAtPath<CoverageTable>(TablePath);
#endif
        }

        SkinnedMeshRenderer FindBody()
        {
            var smrs = GetComponentsInChildren<SkinnedMeshRenderer>(true);
            for (int i = 0; i < smrs.Length; i++)
                if (smrs[i] != null && smrs[i].name == "Body") return smrs[i];
            return null;
        }

        static void EnsureMesh(SkinnedMeshRenderer smr)
        {
            var mesh = smr.sharedMesh;
            if (mesh == null || CoverageBake.HasCoverage(mesh)) return;
            int id = mesh.GetInstanceID();
            if (RuntimeCopies.TryGetValue(id, out var copy) && copy != null)
            {
                smr.sharedMesh = copy;
                return;
            }
            if (!warned)
            {
                warned = true;
                Debug.LogWarning("[Coverage] Body mesh missing TexCoord3; baking a runtime copy of " + mesh.name);
            }
            copy = Instantiate(mesh);
            copy.name = mesh.name + "_Coverage";
            CoverageBake.Write(copy, smr.bones, true);
            RuntimeCopies[id] = copy;
            smr.sharedMesh = copy;
        }

        void EnsureMaterials(SkinnedMeshRenderer smr)
        {
            if (coverage != null && sources != null) return;
            var shader = template != null ? template.shader : Shader.Find("HeroRig/FlatVertexColorCoverage");
            sources = smr.sharedMaterials;
            coverage = new Material[sources.Length];
            for (int i = 0; i < sources.Length; i++)
            {
                // Assigning the coverage shader keeps properties that exist on both shaders.
                Material inst = sources[i] != null ? new Material(sources[i]) : new Material(shader);
                if (shader != null) inst.shader = shader;
                inst.SetFloat(CoverageInset, DefaultInset);
                inst.SetFloat(HiddenRegions, 0f);
                inst.name = (sources[i] != null ? sources[i].name : "Body") + "_Coverage";
                coverage[i] = inst;
            }
            smr.sharedMaterials = coverage;
        }

        int ComputeMask()
        {
            var eq = GetComponent<HeroEquipment>();
            if (eq == null) eq = GetComponentInParent<HeroEquipment>();
            if (eq == null) return 0;
            int union = 0;
            HeroGearSlot[] slots =
            {
                HeroGearSlot.Head, HeroGearSlot.Shoulders, HeroGearSlot.Chest,
                HeroGearSlot.Hands, HeroGearSlot.Legs, HeroGearSlot.Feet
            };
            for (int s = 0; s < slots.Length; s++)
            {
                var slot = eq.Slot(slots[s]);
                if (slot == null || !slot.IsEquipped) continue;
                var current = slot.Current;
                for (int i = 0; i < current.Count; i++)
                    union |= CoversOf(current[i]);
            }
            return union;
        }

        int CoversOf(GameObject go)
        {
            if (go == null) return 0;
            int maskBits = 0;
            var transforms = go.GetComponentsInChildren<Transform>(true);
            for (int i = 0; i < transforms.Length; i++)
            {
                var t = transforms[i];
                if (t == null || t.name.StartsWith("Socket_")) continue;
                var decl = t.GetComponent<HeroCoverageDeclaration>();
                if (decl != null)
                {
                    maskBits |= (int)decl.covers;
                    continue;
                }
                if (table != null && table.TryMatch(t.name, out var row))
                    maskBits |= (int)row;
            }
            return maskBits;
        }
    }
}

