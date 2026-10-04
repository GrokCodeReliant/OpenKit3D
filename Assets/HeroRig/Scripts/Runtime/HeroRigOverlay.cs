// Game-view visible bone + socket overlay (real geometry, renders on top via HeroRig/Overlay shader).
using System.Collections.Generic;
using UnityEngine;

namespace HeroRig
{
    [ExecuteAlways, DefaultExecutionOrder(1000)]
    public class HeroRigOverlay : MonoBehaviour
    {
        public Transform rigRoot;
        public bool showBones = true, showSockets = true, showLabels = true;
        public Color boneColor = new Color(1f, 0.85f, 0.1f, 1f);
        public Color twistColor = new Color(1f, 0.45f, 0.1f, 1f);
        public Color fingerColor = new Color(0.6f, 1f, 0.4f, 1f);
        public Color socketColor = new Color(0.1f, 0.9f, 1f, 1f);
        public float boneWidth = 0.012f, jointSize = 0.022f, socketSize = 0.05f, labelSize = 0.05f;
        public Material overlayMaterial;
        public Font labelFont;
        public Transform labelFacing;

        struct Line { public LineRenderer lr; public Transform a, b; public Vector3 axis; public float len; }
        struct Pt { public Transform go, target; }
        struct Lbl { public Transform go, target; public bool right; }
        readonly List<Line> _lines = new List<Line>();
        readonly List<Pt> _pts = new List<Pt>();
        readonly List<Lbl> _lbls = new List<Lbl>();
        Transform _root;
        static readonly string[] FingerNames = { "Thumb", "Index", "Middle", "Ring", "Little" };

        static bool IsSocket(Transform t) => t.name.StartsWith("Socket_");
        static bool IsFinger(Transform t) { foreach (var f in FingerNames) if (t.name.Contains(f)) return true; return false; }

        void OnEnable() { if (!_root) Rebuild(); }
        void OnDisable() { Clear(); }
        void LateUpdate() { Refresh(); }

        Material Mat()
        {
            if (!overlayMaterial) overlayMaterial = new Material(Shader.Find("HeroRig/Overlay")) { hideFlags = HideFlags.DontSave };
            return overlayMaterial;
        }

        Material Tinted(Color c)
        {
            var m = new Material(Mat()) { hideFlags = HideFlags.DontSave };
            m.SetColor("_Color", c);
            return m;
        }

        void Clear()
        {
            _lines.Clear(); _pts.Clear(); _lbls.Clear();
            var old = transform.Find("RigOverlay");
            while (old)
            {
                if (Application.isPlaying) { old.name = "RigOverlay_dead"; Destroy(old.gameObject); }
                else DestroyImmediate(old.gameObject);
                old = transform.Find("RigOverlay");
            }
            _root = null;
        }

        public void Rebuild()
        {
            Clear();
            if (!rigRoot) return;
            var go = new GameObject("RigOverlay") { hideFlags = HideFlags.DontSave };
            _root = go.transform; _root.SetParent(transform, false);
            var matBone = Tinted(boneColor); var matTwist = Tinted(twistColor); var matFinger = Tinted(fingerColor); var matSock = Tinted(socketColor);
            var matX = Tinted(Color.red); var matY = Tinted(Color.green); var matZ = Tinted(Color.blue);
            foreach (var t in rigRoot.GetComponentsInChildren<Transform>(true))
            {
                if (IsSocket(t))
                {
                    if (!showSockets) continue;
                    AddPoint(t, PrimitiveType.Cube, socketSize, matSock);
                    AddLine(t.parent, t, matSock, boneWidth * 0.6f);
                    AddAxis(t, Vector3.right, matX); AddAxis(t, Vector3.up, matY); AddAxis(t, Vector3.forward, matZ);
                    if (showLabels) AddLabel(t);
                    continue;
                }
                if (IsSocket(t.parent) || !showBones) continue;
                bool finger = IsFinger(t);
                var mat = t.name.Contains("Twist") ? matTwist : finger ? matFinger : matBone;
                AddPoint(t, PrimitiveType.Sphere, finger ? jointSize * 0.5f : jointSize, mat);
                if (t != rigRoot && t.parent) AddLine(t.parent, t, mat, finger ? boneWidth * 0.6f : boneWidth);
            }
            Refresh();
        }

        void AddPoint(Transform target, PrimitiveType type, float size, Material m)
        {
            var p = GameObject.CreatePrimitive(type);
            p.hideFlags = HideFlags.DontSave;
            var col = p.GetComponent<Collider>(); if (col) { if (Application.isPlaying) Destroy(col); else DestroyImmediate(col); }
            p.GetComponent<Renderer>().sharedMaterial = m;
            p.GetComponent<Renderer>().shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
            p.transform.SetParent(_root, false);
            p.transform.localScale = Vector3.one * size;
            _pts.Add(new Pt { go = p.transform, target = target });
        }

        LineRenderer NewLine(Material m, float w)
        {
            var g = new GameObject("line") { hideFlags = HideFlags.DontSave };
            g.transform.SetParent(_root, false);
            var lr = g.AddComponent<LineRenderer>();
            lr.useWorldSpace = true; lr.positionCount = 2; lr.startWidth = lr.endWidth = w;
            lr.sharedMaterial = m; lr.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off; lr.receiveShadows = false;
            lr.numCapVertices = 2;
            return lr;
        }

        void AddLine(Transform a, Transform b, Material m, float w) => _lines.Add(new Line { lr = NewLine(m, w), a = a, b = b });
        void AddAxis(Transform s, Vector3 axis, Material m) => _lines.Add(new Line { lr = NewLine(m, boneWidth * 0.5f), a = s, b = null, axis = axis, len = socketSize * 1.6f });

        void AddLabel(Transform t)
        {
            var g = new GameObject("label_" + t.name) { hideFlags = HideFlags.DontSave };
            g.transform.SetParent(_root, false);
            var tm = g.AddComponent<TextMesh>();
            if (!labelFont) labelFont = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            tm.font = labelFont; tm.text = t.name.Substring("Socket_".Length); tm.fontSize = 64;
            tm.characterSize = labelSize * 10f / 64f; tm.color = socketColor;
            var m = new Material(Mat()) { hideFlags = HideFlags.DontSave, mainTexture = labelFont.material.mainTexture };
            m.SetColor("_Color", Color.white);
            g.GetComponent<MeshRenderer>().sharedMaterial = m;
            _lbls.Add(new Lbl { go = g.transform, target = t });
        }

        public void Refresh()
        {
            if (!_root) return;
            float inv = 1f / Mathf.Max(1e-4f, transform.lossyScale.x);
            foreach (var p in _pts) if (p.target) { p.go.position = p.target.position; p.go.rotation = p.target.rotation; }
            foreach (var l in _lines)
            {
                if (!l.a) continue;
                l.lr.SetPosition(0, l.a.position);
                l.lr.SetPosition(1, l.b ? l.b.position : l.a.position + l.a.TransformDirection(l.axis).normalized * l.len);
            }
            Quaternion face = labelFacing ? Quaternion.identity : Quaternion.identity;
            foreach (var lb in _lbls)
            {
                if (!lb.target) continue;
                Vector3 camRight = labelFacing ? labelFacing.right : Vector3.right;
                Vector3 local = rigRoot ? rigRoot.InverseTransformPoint(lb.target.position) : Vector3.zero;
                bool right = Vector3.Dot(lb.target.position - (rigRoot ? rigRoot.position : transform.position), camRight) >= 0f;
                var tm = lb.go.GetComponent<TextMesh>();
                tm.anchor = right ? TextAnchor.MiddleLeft : TextAnchor.MiddleRight;
                lb.go.position = lb.target.position + camRight * (right ? 1f : -1f) * socketSize * 0.9f;
                lb.go.rotation = labelFacing ? Quaternion.LookRotation(lb.go.position - labelFacing.position, labelFacing.up) : Quaternion.identity;
            }
        }
    }
}
