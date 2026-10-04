// attackRange is one constant per sub-size (weapon template v1.2 section 1.9), not a per-item number.
using System;

namespace HeroRig
{
    public static class HeroWeaponTemplates
    {
        public static float AttackRange(string template, string subSize)
        {
            string key = (template ?? "") + "." + (subSize ?? "");
            switch (key)
            {
                case "1H.dagger":
                case "OFFHAND.dagger":
                    return 1.0f;
                case "1H.sword":
                case "1H.axe":
                case "1H.mace":
                case "OFFHAND.sword":
                case "OFFHAND.axe":
                    return 1.5f;
                case "2H.greatsword":
                case "2H.greataxe":
                case "2H.maul":
                case "2H.staff":
                case "1H.spear-short":
                    return 2.0f;
                case "2H.spear":
                    return 2.6f;
                case "BOW.short":
                case "BOW.long":
                    return 15f;
                default:
                    return 0f;
            }
        }
    }
}
