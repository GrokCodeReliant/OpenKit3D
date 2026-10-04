// Tier rows for armor.l.b01. value = lerp(tierMin, tierMax, q). Prismatic only at T4 and q >= threshold.
using System;
using System.Collections.Generic;
using UnityEngine;

namespace HeroRig
{
    [Serializable]
    public class HeroGearBaseHue
    {
        public string id = "armor.l.b01";
        public Color primary = new Color(0.478f, 0.322f, 0.204f, 1f);
    }

    [Serializable]
    public class HeroGearTierRow
    {
        public string name;
        public Color tell;
        public float primarySatMul = 1f;
        public float primaryValMul = 1f;
        public float hueToward;
        public Color hueTarget = Color.white;
        public Color secondary;
        public Color tertiary;
        public Color emissiveColor = Color.black;
        public float finishMin, finishMax, wearMin, wearMax, emissiveMin, emissiveMax;
    }

    [Serializable]
    public class HeroGearFitOffset
    {
        public string fit;
        public Vector3 position;
        public Vector3 scaleMultiplier = Vector3.one;
    }

    public struct HeroGearResolvedLook
    {
        public Color primary, secondary, tertiary, dark, tell, emissiveColor;
        public float finish, wear, emissive;
        public bool prismatic, secondarySweep;
    }

    [CreateAssetMenu(fileName = "GearLookTable", menuName = "HeroRig/Gear Look Table")]
    public class HeroGearLookTable : ScriptableObject
    {
        public float prismaticThreshold = 0.95f;
        public Color dark = new Color(0.05f, 0.05f, 0.06f, 1f);
        public List<HeroGearBaseHue> bases = new List<HeroGearBaseHue>();
        public List<HeroGearTierRow> tiers = new List<HeroGearTierRow>();
        public List<HeroGearFitOffset> shldOffsets = new List<HeroGearFitOffset>();

        public static Color Hex(string html)
        {
            ColorUtility.TryParseHtmlString("#" + html, out var c);
            return c;
        }

        public void ResetToSpec()
        {
            prismaticThreshold = 0.95f;
            dark = new Color(0.05f, 0.05f, 0.06f, 1f);
            bases = new List<HeroGearBaseHue>
            {
                new HeroGearBaseHue { id = "armor.l.b01", primary = Hex("7A5234") },
                new HeroGearBaseHue { id = "weapon.swd.b01", primary = Hex("8E9398") },
            };
            // T1 secondary has no hex in the spec. #5C7A48 is the muted green used here.
            tiers = new List<HeroGearTierRow>
            {
                Row("Common", "D8D2C4", 0.65f, 0.85f, 0f, "FFFFFF", "8A7F6E", "6A5646", "000000", 0.05f, 0.15f, 0.95f, 0.70f, 0f, 0f),
                Row("Uncommon", "4FAF4A", 0.85f, 1f, 0f, "FFFFFF", "5C7A48", "7C7C7C", "000000", 0.20f, 0.30f, 0.60f, 0.40f, 0f, 0f),
                Row("Rare", "3B7BDB", 1f, 1f, 0f, "FFFFFF", "3B7BDB", "B8C0C8", "000000", 0.45f, 0.60f, 0.25f, 0.10f, 0f, 0f),
                Row("Epic", "9A4FD6", 1f, 1f, 0.10f, "9A4FD6", "9A4FD6", "D6D8DE", "9A4FD6", 0.65f, 0.75f, 0.08f, 0.02f, 0.25f, 0.50f),
                Row("Legendary", "E8962E", 1f, 1f, 0.15f, "E8962E", "E8962E", "E2B04A", "E8962E", 0.80f, 0.90f, 0.02f, 0.00f, 0.60f, 1.00f),
            };
        }

        static HeroGearTierRow Row(string name, string tell, float sat, float val, float toward, string target,
            string secondary, string tertiary, string emis, float f0, float f1, float w0, float w1, float e0, float e1)
        {
            return new HeroGearTierRow
            {
                name = name,
                tell = Hex(tell),
                primarySatMul = sat,
                primaryValMul = val,
                hueToward = toward,
                hueTarget = Hex(target),
                secondary = Hex(secondary),
                tertiary = Hex(tertiary),
                emissiveColor = Hex(emis),
                finishMin = f0, finishMax = f1,
                wearMin = w0, wearMax = w1,
                emissiveMin = e0, emissiveMax = e1,
            };
        }

        public Color BasePrimary(string baseId)
        {
            if (bases != null)
                for (int i = 0; i < bases.Count; i++)
                    if (bases[i] != null && bases[i].id == baseId) return bases[i].primary;
            return Hex("7A5234");
        }

        public bool IsPrismatic(int tier, float q) => tier >= 4 && q >= prismaticThreshold;

        public HeroGearResolvedLook Resolve(string baseId, int tier, float q)
        {
            if (tiers == null || tiers.Count == 0) ResetToSpec();
            q = Mathf.Clamp01(q);
            tier = Mathf.Clamp(tier, 0, Mathf.Min(4, tiers.Count - 1));
            bool pris = IsPrismatic(tier, q);
            var row = tiers[tier];
            var look = new HeroGearResolvedLook
            {
                primary = PrimaryColor(BasePrimary(baseId), row),
                secondary = BoostSat(row.secondary, q),
                tertiary = row.tertiary,
                dark = dark,
                tell = row.tell,
                emissiveColor = row.emissiveColor,
                finish = Mathf.Lerp(row.finishMin, row.finishMax, q),
                wear = Mathf.Lerp(row.wearMin, row.wearMax, q),
                emissive = Mathf.Lerp(row.emissiveMin, row.emissiveMax, q),
                prismatic = pris,
                secondarySweep = pris,
            };
            if (pris)
            {
                look.finish = 0.95f;
                look.wear = 0f;
                look.emissive = 1f;
                look.emissiveColor = Color.white;
            }
            return look;
        }

        static Color PrimaryColor(Color baseCol, HeroGearTierRow row)
        {
            Color.RGBToHSV(baseCol, out float h, out float s, out float v);
            s = Mathf.Clamp01(s * row.primarySatMul);
            v = Mathf.Clamp01(v * row.primaryValMul);
            if (row.hueToward > 0f)
            {
                Color.RGBToHSV(row.hueTarget, out float ht, out _, out _);
                h = LerpHue(h, ht, row.hueToward);
            }
            var c = Color.HSVToRGB(h, s, v);
            c.a = 1f;
            return c;
        }

        static Color BoostSat(Color c, float q)
        {
            Color.RGBToHSV(c, out float h, out float s, out float v);
            s = Mathf.Clamp01(s + 0.15f * Mathf.Clamp01(q));
            var o = Color.HSVToRGB(h, s, v);
            o.a = 1f;
            return o;
        }

        static float LerpHue(float a, float b, float t)
        {
            float d = Mathf.Repeat(b - a + 0.5f, 1f) - 0.5f;
            return Mathf.Repeat(a + d * t, 1f);
        }
    }
}
