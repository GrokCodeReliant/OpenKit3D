// One shared M_Gear. Per-submesh MaterialPropertyBlocks carry the tier tint.
// An MPB takes these renderers off the SRP Batcher. That is acceptable for the demo.
using UnityEngine;

namespace HeroRig
{
    [DisallowMultipleComponent]
    public class HeroGearLook : MonoBehaviour
    {
        public int primarySubmesh = 0;
        public int secondarySubmesh = 1;
        public int tertiarySubmesh = 2;
        public int darkSubmesh = 3;

        static readonly int BaseColorId = Shader.PropertyToID("_BaseColor");
        static readonly int WearId = Shader.PropertyToID("_Wear");
        static readonly int FinishId = Shader.PropertyToID("_Finish");
        static readonly int EmissiveId = Shader.PropertyToID("_Emissive");
        static readonly int EmissiveColorId = Shader.PropertyToID("_EmissiveColor");
        static readonly int PrismaticId = Shader.PropertyToID("_Prismatic");
        static readonly int SweepId = Shader.PropertyToID("_Sweep");

        public void Apply(HeroGearLookTable table, string baseId, int tier, float q)
        {
            var r = GetComponent<Renderer>();
            if (!r || !table) return;
            var look = table.Resolve(baseId, tier, q);
            int n = r.sharedMaterials != null ? r.sharedMaterials.Length : 0;
            Paint(r, primarySubmesh, n, look.primary, look.finish, look.wear, 0f, Color.black, look.prismatic, false);
            Paint(r, secondarySubmesh, n, look.secondary, look.finish, look.wear, 0f, Color.black, look.prismatic, look.secondarySweep);
            Paint(r, tertiarySubmesh, n, look.tertiary, look.finish, look.wear, look.emissive, look.emissiveColor, look.prismatic, false);
            Paint(r, darkSubmesh, n, look.dark, 0f, 0f, 0f, Color.black, false, false);
        }

        static void Paint(Renderer r, int sub, int count, Color tint, float finish, float wear, float emis, Color emisColor, bool prismatic, bool sweep)
        {
            if (sub < 0 || sub >= count) return;
            var mpb = new MaterialPropertyBlock();
            r.GetPropertyBlock(mpb, sub);
            mpb.SetColor(BaseColorId, tint);
            mpb.SetFloat(WearId, wear);
            mpb.SetFloat(FinishId, finish);
            mpb.SetFloat(EmissiveId, emis);
            mpb.SetColor(EmissiveColorId, emisColor);
            mpb.SetFloat(PrismaticId, prismatic ? 1f : 0f);
            mpb.SetFloat(SweepId, sweep ? 1f : 0f);
            r.SetPropertyBlock(mpb, sub);
        }
    }
}
