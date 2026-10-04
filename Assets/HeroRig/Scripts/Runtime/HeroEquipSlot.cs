// One component per slot, on a child of the hero root named EquipSlot_<Slot>.
//
// RIGID (Head, Shoulders, MainHand, OffHand): parent to the anchor, worldPositionStays false.
// The instance's own root (prefab/FBX root, captured before parenting) is kept and HeroGearItem
// is composed on top: localRotation = Euler(item) * rootRotation,
// localPosition = itemPosition + Euler(item) * rootPosition, localScale = item scale
// (the root scale when there is no item, or when the item scale is zero).
// MainHand/OffHand anchors are Grip_* (weapon frame). Identity roots (head, shoulders, cubes) are unchanged.
// Shoulders: direct-or-nested children whose names end _L / _R go to Socket_Shoulder_L / _R.
// If the item has no such children, the item goes on L and a copy on R. The copy mirrors local
// position and rotation (scale.x = -1 is never used â€” flat shading / backface culling). SHLD fit
// offsets come from HeroGearItem.fitOffsets for HeroEquipment.CurrentFit.
//
// SKINNED (Chest, Hands, Legs, Feet): every SkinnedMeshRenderer is remapped by bone NAME onto this
// hero, rootBone = Hips, sharedMesh and bindposes kept. The renderer is reparented under the hero
// root (next to Body). The item's duplicate armature is destroyed. Missing bone name: error log,
// then the nearest source-skeleton parent that exists on the hero. Then HeroDeformDriver.RegisterLayer,
// HeroBodyType.Apply, HeroProportions.RefreshRenderers.
//
// RIGID FALLBACK on a skinned slot (a cube, or any item with no SkinnedMeshRenderer / mode Rigid):
// parent one copy per anchor, same local offset, no negative scale.
//   Chest -> Socket_Chest (one)
//   Hands -> LeftHand + RightHand
//   Legs  -> LeftLowerLeg + RightLowerLeg
//   Feet  -> LeftFoot + RightFoot
//
// MainHand / OffHand hide HeroWeaponController's demo weapon on that socket and restore it on Unequip.
using System.Collections.Generic;
using UnityEngine;

namespace HeroRig
{
    [DisallowMultipleComponent]
    public class HeroEquipSlot : MonoBehaviour
    {
        public HeroGearSlot slot;
        public HeroAttachMode mode = HeroAttachMode.Rigid;
        public Transform[] anchors = new Transform[0];
        public List<GameObject> current = new List<GameObject>();

        public IReadOnlyList<GameObject> Current => current;
        public bool IsEquipped => current.Exists(g => g);
        public bool HidesClothing => IsEquipped && _hidesClothing;
        /// Bones that were missing on the hero during the last skinned equip, "Source->Fallback".
        public string lastBoneFallback;

        [SerializeField] bool _hidesClothing;

        struct FitSnap
        {
            public HeroFit fit;
            public Vector3 position;
            public Vector3 scaleMultiplier;
        }

        class Placement
        {
            public GameObject go;
            public bool mirror;
            public Vector3 pos, euler, scale, rootPos;
            public Quaternion rootRot;
            public FitSnap[] fits;
        }

        readonly List<Placement> _placed = new List<Placement>();
        HeroAttachPoints _points;
        HeroEquipment _equipment;

        HeroAttachPoints Points => _points ? _points : (_points = GetComponentInParent<HeroAttachPoints>(true));
        HeroEquipment Equipment => _equipment ? _equipment : (_equipment = GetComponentInParent<HeroEquipment>(true));

        void OnValidate()
        {
            var p = Points;
            if (!p) return;
            var next = p.Anchors(slot);
            if (next != null && next.Length > 0 && System.Array.TrueForAll(next, a => a))
                anchors = next;
        }

        public void RefreshAnchors()
        {
            var p = Points;
            if (!p) return;
            anchors = p.Anchors(slot);
        }

        public GameObject Equip(GameObject prefabOrInstance)
        {
            Unequip();
            if (!prefabOrInstance) return null;
            EnsureAnchors();
            var instance = Spawn(prefabOrInstance);
            if (!instance) return null;
            instance.name = prefabOrInstance.name;

            bool skinned = WantsSkinned(instance);
            _hidesClothing = ResolveHides(instance);
            GameObject primary;
            if (skinned) primary = EquipSkinned(instance);
            else if (slot == HeroGearSlot.Shoulders) primary = EquipShoulders(instance);
            else primary = EquipRigidAnchors(instance);

            if (slot == HeroGearSlot.MainHand || slot == HeroGearSlot.OffHand)
                Demo(true);
            var eq = Equipment;
            if (eq) eq.RefreshClothing();
            return primary;
        }

        public void Unequip()
        {
            var hero = HeroRoot;
            var dd = hero ? hero.GetComponent<HeroDeformDriver>() : null;
            for (int i = 0; i < current.Count; i++)
            {
                var g = current[i];
                if (!g) continue;
                if (dd)
                    foreach (var smr in g.GetComponentsInChildren<SkinnedMeshRenderer>(true))
                        dd.UnregisterLayer(smr);
                DestroyObj(g);
            }
            current.Clear();
            _placed.Clear();
            _hidesClothing = false;
            lastBoneFallback = "";
            if (slot == HeroGearSlot.MainHand || slot == HeroGearSlot.OffHand)
                Demo(false);
            var eq = Equipment;
            if (eq) eq.RefreshClothing();
            if (hero)
            {
                var prop = hero.GetComponent<HeroProportions>();
                if (prop) prop.RefreshRenderers();
            }
        }

        /// Re-apply SHLD (and any rigid) fit offsets after HeroEquipment.SetBodyType changes CurrentFit.
        public void ReapplyFit()
        {
            var fit = Equipment ? Equipment.CurrentFit : HeroFit.ML;
            for (int i = 0; i < _placed.Count; i++)
            {
                var p = _placed[i];
                if (!p.go) continue;
                ApplyLocal(p.go.transform, p.pos, p.euler, p.scale, p.rootPos, p.rootRot, p.fits, p.mirror, fit);
            }
        }

        void EnsureAnchors()
        {
            if (anchors == null || anchors.Length == 0 || System.Array.Exists(anchors, a => !a))
                RefreshAnchors();
        }

        Transform HeroRoot
        {
            get
            {
                var eq = Equipment;
                if (eq) return eq.transform;
                var p = Points;
                return p ? p.transform : transform.parent;
            }
        }

        static bool IsAsset(GameObject go) => go && !go.scene.IsValid();

        static GameObject Spawn(GameObject src)
        {
            if (!src) return null;
            if (!IsAsset(src)) return src;
            var go = Object.Instantiate(src);
            go.name = src.name;
            return go;
        }

        bool WantsSkinned(GameObject instance)
        {
            var item = ItemOf(instance);
            bool has = instance.GetComponentInChildren<SkinnedMeshRenderer>(true);
            // Item mode wins. Shoulders stay a rigid slot, but a skinned SHLD (leather pads) must follow the arm.
            if (item && item.mode == HeroGearMode.Rigid) return false;
            if (item && item.mode == HeroGearMode.Skinned) return has;
            if (mode != HeroAttachMode.Skinned) return false;
            return has;
        }

        static HeroGearItem ItemOf(GameObject go) =>
            go ? (go.GetComponent<HeroGearItem>() ?? go.GetComponentInChildren<HeroGearItem>(true)) : null;

        bool ResolveHides(GameObject instance)
        {
            var item = ItemOf(instance);
            if (item) return item.hidesClothing;
            return slot == HeroGearSlot.Chest || slot == HeroGearSlot.Legs;
        }

        void Demo(bool suppress)
        {
            var wc = HeroRoot ? HeroRoot.GetComponent<HeroWeaponController>() : null;
            if (!wc) return;
            if (slot == HeroGearSlot.MainHand) wc.SetDemoSuppressed(true, suppress);
            else if (slot == HeroGearSlot.OffHand) wc.SetDemoSuppressed(false, suppress);
        }

        GameObject EquipRigidAnchors(GameObject instance)
        {
            if (anchors == null || anchors.Length == 0)
            {
                Debug.LogError("[HeroRig] equip " + slot + ": no anchor");
                DestroyObj(instance);
                return null;
            }
            ReadOffset(instance, instance, out var pos, out var euler, out var scale, out var rootPos, out var rootRot, out var fits);
            GameObject primary = null;
            for (int i = 0; i < anchors.Length; i++)
            {
                if (!anchors[i]) continue;
                var go = primary == null ? instance : Object.Instantiate(instance);
                if (primary != null) go.name = instance.name;
                Place(go, anchors[i], pos, euler, scale, rootPos, rootRot, fits, false);
                current.Add(go);
                if (!primary) primary = go;
            }
            return primary;
        }

        GameObject EquipShoulders(GameObject instance)
        {
            var left = AnchorNamed("Socket_Shoulder_L", 0);
            var right = AnchorNamed("Socket_Shoulder_R", 1);
            if (!left || !right)
            {
                Debug.LogError("[HeroRig] equip Shoulders: Socket_Shoulder_L/R missing");
                DestroyObj(instance);
                return null;
            }
            var pieces = SidePieces(instance);
            if (pieces.Count > 0)
            {
                foreach (var c in pieces)
                {
                    bool rightSide = c.name.EndsWith("_R");
                    ReadOffset(c.gameObject, instance, out var sp, out var se, out var ss, out var sRoot, out var sRot, out var sFits);
                    Place(c.gameObject, rightSide ? right : left, sp, se, ss, sRoot, sRot, sFits, false);
                    current.Add(c.gameObject);
                }
                if (instance && instance.transform.childCount == 0 && !instance.GetComponent<Renderer>() && !current.Contains(instance))
                    DestroyObj(instance);
                return current.Count > 0 ? current[0] : null;
            }
            ReadOffset(instance, instance, out var p, out var e, out var s, out var rootPos, out var rootRot, out var f);
            Place(instance, left, p, e, s, rootPos, rootRot, f, false);
            current.Add(instance);
            var copy = Object.Instantiate(instance, right, false);
            copy.name = instance.name + "_R";
            // Instantiate kept the already-applied local transform. Re-apply from the unmirrored base, then mirror.
            Place(copy, right, p, e, s, rootPos, rootRot, f, true);
            current.Add(copy);
            return instance;
        }

        Transform AnchorNamed(string boneName, int index)
        {
            if (anchors != null)
                for (int i = 0; i < anchors.Length; i++)
                    if (anchors[i] && anchors[i].name == boneName) return anchors[i];
            if (anchors != null && index < anchors.Length && anchors[index]) return anchors[index];
            var pts = Points;
            return pts ? pts.Bone(boneName) : null;
        }

        static List<Transform> SidePieces(GameObject root)
        {
            var list = new List<Transform>();
            foreach (var t in root.GetComponentsInChildren<Transform>(true))
            {
                if (t == root.transform) continue;
                if (t.name.EndsWith("_L") || t.name.EndsWith("_R")) list.Add(t);
            }
            for (int i = list.Count - 1; i >= 0; i--)
            {
                bool nested = false;
                for (int j = 0; j < list.Count; j++)
                    if (i != j && list[i].IsChildOf(list[j])) { nested = true; break; }
                if (nested) list.RemoveAt(i);
            }
            return list;
        }

        GameObject EquipSkinned(GameObject instance)
        {
            var hero = HeroRoot;
            var pts = Points;
            if (!hero || !pts)
            {
                Debug.LogError("[HeroRig] equip " + slot + ": hero or attach points missing");
                DestroyObj(instance);
                return null;
            }
            var smrs = instance.GetComponentsInChildren<SkinnedMeshRenderer>(true);
            if (smrs.Length == 0) return EquipRigidAnchors(instance);
            var hips = pts.hips ? pts.hips : pts.Bone("Hips", instance.transform);
            var body = FindBody(hero);
            var kept = new HashSet<GameObject>();
            var notes = new List<string>();
            GameObject primary = null;
            foreach (var smr in smrs)
            {
                var src = smr.bones;
                var dst = new Transform[src != null ? src.Length : 0];
                for (int i = 0; i < dst.Length; i++)
                {
                    var sb = src[i];
                    string boneName = sb ? sb.name : "";
                    var heroBone = pts.Bone(boneName, instance.transform);
                    if (!heroBone && sb)
                    {
                        var p = sb.parent;
                        while (p && p != instance.transform)
                        {
                            heroBone = pts.Bone(p.name, instance.transform);
                            if (heroBone)
                            {
                                Debug.LogError("[HeroRig] gear bone '" + boneName + "' missing on hero; using parent '" + p.name + "'");
                                notes.Add(boneName + "->" + p.name);
                                break;
                            }
                            p = p.parent;
                        }
                    }
                    if (!heroBone)
                    {
                        Debug.LogError("[HeroRig] gear bone '" + boneName + "' missing on hero; using Hips");
                        notes.Add(boneName + "->Hips");
                        heroBone = hips;
                    }
                    dst[i] = heroBone;
                }
                smr.bones = dst;
                smr.rootBone = hips;
                smr.updateWhenOffscreen = false;
                if (body)
                {
                    var b = body.localBounds;
                    b.Expand(0.05f);
                    smr.localBounds = b;
                }
                smr.transform.SetParent(hero, false);
                if (body)
                {
                    smr.transform.localPosition = body.transform.localPosition;
                    smr.transform.localRotation = body.transform.localRotation;
                    smr.transform.localScale = body.transform.localScale;
                }
                kept.Add(smr.gameObject);
                current.Add(smr.gameObject);
                if (!primary) primary = smr.gameObject;
                var dd = hero.GetComponent<HeroDeformDriver>();
                if (dd) dd.RegisterLayer(smr);
            }
            lastBoneFallback = string.Join("; ", notes);
            DestroyArmature(instance, kept);
            var bt = hero.GetComponent<HeroBodyType>();
            if (bt) bt.Apply();
            var prop = hero.GetComponent<HeroProportions>();
            if (prop) prop.RefreshRenderers();
            return primary;
        }

        static SkinnedMeshRenderer FindBody(Transform hero)
        {
            SkinnedMeshRenderer first = null;
            foreach (var r in hero.GetComponentsInChildren<SkinnedMeshRenderer>(true))
            {
                if (r.name == "Body") return r;
                if (!first) first = r;
            }
            return first;
        }

        static void DestroyArmature(GameObject root, HashSet<GameObject> kept)
        {
            if (!root) return;
            if (kept.Contains(root))
            {
                for (int i = root.transform.childCount - 1; i >= 0; i--)
                {
                    var c = root.transform.GetChild(i).gameObject;
                    bool hold = kept.Contains(c);
                    if (!hold)
                        foreach (var k in kept)
                            if (k && k.transform.IsChildOf(c.transform)) { hold = true; break; }
                    if (!hold) DestroyObj(c);
                }
                return;
            }
            DestroyObj(root);
        }

        void ReadOffset(GameObject piece, GameObject root, out Vector3 pos, out Vector3 euler, out Vector3 scale, out Vector3 rootPos, out Quaternion rootRot, out FitSnap[] fits)
        {
            // Captured before parenting. This is the prefab/FBX root on a fresh instance.
            rootPos = piece.transform.localPosition;
            rootRot = piece.transform.localRotation;
            var rootScale = piece.transform.localScale;
            if (rootScale == Vector3.zero) rootScale = Vector3.one;
            var item = piece.GetComponent<HeroGearItem>() ?? (root ? root.GetComponent<HeroGearItem>() : null) ?? ItemOf(piece);
            if (item)
            {
                pos = item.localPosition;
                euler = item.localEuler;
                scale = item.localScale == Vector3.zero ? rootScale : item.localScale;
                fits = Snap(item);
            }
            else
            {
                pos = Vector3.zero;
                euler = Vector3.zero;
                scale = rootScale;
                fits = null;
            }
        }

        static FitSnap[] Snap(HeroGearItem item)
        {
            if (item.fitOffsets == null || item.fitOffsets.Count == 0) return null;
            var a = new FitSnap[item.fitOffsets.Count];
            for (int i = 0; i < a.Length; i++)
            {
                var f = item.fitOffsets[i];
                if (f == null) continue;
                a[i] = new FitSnap { fit = f.fit, position = f.position, scaleMultiplier = f.scaleMultiplier };
            }
            return a;
        }

        void Place(GameObject go, Transform anchor, Vector3 pos, Vector3 euler, Vector3 scale, Vector3 rootPos, Quaternion rootRot, FitSnap[] fits, bool mirror)
        {
            go.transform.SetParent(anchor, false);
            var fit = Equipment ? Equipment.CurrentFit : HeroFit.ML;
            ApplyLocal(go.transform, pos, euler, scale, rootPos, rootRot, fits, mirror, fit);
            _placed.Add(new Placement { go = go, mirror = mirror, pos = pos, euler = euler, scale = scale, rootPos = rootPos, rootRot = rootRot, fits = fits });
        }

        static void ApplyLocal(Transform t, Vector3 pos, Vector3 euler, Vector3 scale, Vector3 rootPos, Quaternion rootRot, FitSnap[] fits, bool mirror, HeroFit fit)
        {
            if (fits != null)
            {
                for (int i = 0; i < fits.Length; i++)
                {
                    if (fits[i].scaleMultiplier == Vector3.zero && fits[i].position == Vector3.zero && !FitsMatch(fits[i], fit)) continue;
                    if (fits[i].fit != fit) continue;
                    pos += fits[i].position;
                    var m = fits[i].scaleMultiplier;
                    if (m == Vector3.zero) m = Vector3.one;
                    scale = Vector3.Scale(scale, m);
                    break;
                }
            }
            scale = new Vector3(Mathf.Abs(scale.x), Mathf.Abs(scale.y), Mathf.Abs(scale.z));
            if (scale == Vector3.zero) scale = Vector3.one;
            var itemRot = Quaternion.Euler(euler);
            t.localRotation = itemRot * rootRot;
            t.localPosition = pos + itemRot * rootPos;
            t.localScale = scale;
            if (mirror) MirrorLocal(t);
        }

        static bool FitsMatch(FitSnap s, HeroFit fit) => s.fit == fit;

        /// Mirror across the socket's YZ plane. Scale stays positive.
        public static void MirrorLocal(Transform t)
        {
            var p = t.localPosition;
            p.x = -p.x;
            t.localPosition = p;
            var q = t.localRotation;
            t.localRotation = new Quaternion(q.x, -q.y, -q.z, q.w);
            var s = t.localScale;
            t.localScale = new Vector3(Mathf.Abs(s.x), Mathf.Abs(s.y), Mathf.Abs(s.z));
        }

        static void DestroyObj(GameObject go)
        {
            if (!go) return;
            if (Application.isPlaying) Object.Destroy(go);
            else Object.DestroyImmediate(go);
        }
    }
}
