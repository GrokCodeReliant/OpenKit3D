using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Rendering;

#if UNITY_EDITOR
using UnityEditor;
#endif

/// <summary>
/// Writes body-region scores into the Body mesh.
/// UV3 (mesh channel 2, TEXCOORD2) = (HEAD, SHLD, CHST, HAND).
/// UV4 (mesh channel 3, TEXCOORD3) = (LEGS, FEET, 0, 0).
/// Does not write vertex colours or UV2 (gear WearMask, channel 1).
/// </summary>
public static class CoverageBake
{
    public const int Uv3Channel = 2;
    public const int Uv4Channel = 3;
    const int HipsSplit = 6;
    const float SplitHalf = 0.03f;

    public static readonly string[] HeroFbx =
    {
        "Assets/HeroRig/Models/Characters/HeroMale.fbx",
        "Assets/HeroRig/Models/Characters/HeroFemale.fbx"
    };

    public static bool HasCoverage(Mesh mesh)
    {
        return mesh != null && mesh.HasVertexAttribute(VertexAttribute.TexCoord3);
    }

    public static void Write(Mesh mesh, Transform[] bones, bool upload)
    {
        if (mesh == null || bones == null || bones.Length == 0) return;
        int vc = mesh.vertexCount;
        if (vc == 0) return;

        var region = new int[bones.Length];
        int hips = -1, leftUpper = -1, rightUpper = -1;
        var unmapped = new List<string>();
        for (int i = 0; i < bones.Length; i++)
        {
            region[i] = ClassifyChain(bones[i]);
            string n = bones[i] != null ? bones[i].name : "";
            if (n == "Hips") hips = i;
            else if (n == "LeftUpperLeg") leftUpper = i;
            else if (n == "RightUpperLeg") rightUpper = i;
            if (region[i] < 0 && !string.IsNullOrEmpty(n) && !unmapped.Contains(n))
                unmapped.Add(n);
        }
        if (unmapped.Count > 0)
            Debug.LogWarning("[Coverage] unmapped bones (weight dropped before normalise): " + string.Join(", ", unmapped));

        float splitY = 0f;
        int splitN = 0;
        if (leftUpper >= 0) { splitY += BindHeight(mesh, leftUpper); splitN++; }
        if (rightUpper >= 0) { splitY += BindHeight(mesh, rightUpper); splitN++; }
        if (splitN > 0) splitY /= splitN;
        else if (hips >= 0) splitY = BindHeight(mesh, hips);

        var verts = mesh.vertices;
        var uv3 = new Vector4[vc];
        var uv4 = new Vector4[vc];
        var scores = new float[6];

        var bpv = mesh.GetBonesPerVertex();
        var all = mesh.GetAllBoneWeights();
        bool modern = bpv.IsCreated && bpv.Length == vc && all.IsCreated;
        BoneWeight[] legacy = null;
        if (!modern)
        {
#pragma warning disable CS0618
            legacy = mesh.boneWeights;
#pragma warning restore CS0618
        }

        int offset = 0;
        for (int v = 0; v < vc; v++)
        {
            for (int s = 0; s < 6; s++) scores[s] = 0f;
            if (modern)
            {
                int n = bpv[v];
                for (int k = 0; k < n; k++)
                {
                    var bw = all[offset + k];
                    Add(scores, region, bw.boneIndex, bw.weight, verts[v].y, splitY);
                }
                offset += n;
            }
            else if (legacy != null && v < legacy.Length)
            {
                var bw = legacy[v];
                Add(scores, region, bw.boneIndex0, bw.weight0, verts[v].y, splitY);
                Add(scores, region, bw.boneIndex1, bw.weight1, verts[v].y, splitY);
                Add(scores, region, bw.boneIndex2, bw.weight2, verts[v].y, splitY);
                Add(scores, region, bw.boneIndex3, bw.weight3, verts[v].y, splitY);
            }

            float sum = scores[0] + scores[1] + scores[2] + scores[3] + scores[4] + scores[5];
            if (sum > 1e-8f)
            {
                float inv = 1f / sum;
                for (int s = 0; s < 6; s++) scores[s] *= inv;
            }
            uv3[v] = new Vector4(scores[0], scores[1], scores[2], scores[3]);
            uv4[v] = new Vector4(scores[4], scores[5], 0f, 0f);
        }

        mesh.SetUVs(Uv3Channel, new List<Vector4>(uv3));
        mesh.SetUVs(Uv4Channel, new List<Vector4>(uv4));
        if (upload) mesh.UploadMeshData(false);
    }

    static void Add(float[] scores, int[] region, int bone, float weight, float vertexY, float splitY)
    {
        if (weight <= 1e-6f || bone < 0 || bone >= region.Length) return;
        int r = region[bone];
        if (r == HipsSplit)
        {
            float t = SmoothStep(splitY - SplitHalf, splitY + SplitHalf, vertexY);
            scores[2] += weight * t;
            scores[4] += weight * (1f - t);
            return;
        }
        if (r >= 0 && r < 6) scores[r] += weight;
    }

    public static float SmoothStep(float edge0, float edge1, float x)
    {
        float t = Mathf.Clamp01((x - edge0) / (edge1 - edge0));
        return t * t * (3f - 2f * t);
    }

    static float BindHeight(Mesh mesh, int boneIndex)
    {
        if (mesh.bindposes != null && boneIndex >= 0 && boneIndex < mesh.bindposes.Length)
            return mesh.bindposes[boneIndex].inverse.MultiplyPoint3x4(Vector3.zero).y;
        return 0f;
    }

    static int ClassifyChain(Transform bone)
    {
        var t = bone;
        int guard = 0;
        while (t != null && guard++ < 64)
        {
            int r = ClassifyName(t.name);
            if (r != -1) return r;
            t = t.parent;
        }
        return -1;
    }

    /// <summary>Hips returns <see cref="HipsSplit"/>. Unknown returns -1. Does not walk parents.</summary>
    public static int ClassifyName(string name)
    {
        if (string.IsNullOrEmpty(name)) return -1;
        if (name == "Hips") return HipsSplit;
        if (Has(name, "Toes") || Has(name, "Foot")) return 5;
        if (Has(name, "Thumb") || Has(name, "Index") || Has(name, "Middle") || Has(name, "Ring")
            || Has(name, "Little") || Has(name, "LowerArm") || Has(name, "Hand"))
            return 3;
        if (Has(name, "Shoulder") || Has(name, "UpperArm")) return 1;
        if (Has(name, "Head") || Has(name, "Neck") || Has(name, "Jaw") || Has(name, "Eye") || Has(name, "Face"))
            return 0;
        if (Has(name, "Spine") || Has(name, "Chest")) return 2;
        if (Has(name, "UpperLeg") || Has(name, "LowerLeg")) return 4;
        return -1;
    }

    static bool Has(string name, string token)
    {
        return name.IndexOf(token, System.StringComparison.Ordinal) >= 0;
    }

#if UNITY_EDITOR
    [MenuItem("Open Kit Dungeon/Reimport Hero Coverage")]
    public static void ReimportHeroes()
    {
        try
        {
            for (int i = 0; i < HeroFbx.Length; i++)
            {
                if (AssetDatabase.LoadAssetAtPath<GameObject>(HeroFbx[i]) == null &&
                    !System.IO.File.Exists(HeroFbx[i]))
                {
                    Debug.LogError("[Coverage] missing " + HeroFbx[i]);
                    if (Application.isBatchMode) EditorApplication.Exit(1);
                    return;
                }
                AssetDatabase.ImportAsset(HeroFbx[i], ImportAssetOptions.ForceUpdate);
            }
            AssetDatabase.SaveAssets();
            Debug.Log("[OKD] coverage reimport ok");
            if (Application.isBatchMode) EditorApplication.Exit(0);
        }
        catch (System.Exception e)
        {
            Debug.LogError("[Coverage] reimport failed: " + e);
            if (Application.isBatchMode) EditorApplication.Exit(1);
            else throw;
        }
    }
#endif
}

