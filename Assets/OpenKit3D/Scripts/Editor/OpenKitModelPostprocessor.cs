using UnityEditor;
using UnityEngine;

namespace OpenKit.Editor
{
    /// <summary>Enforces the Open Kit import conventions for every model under Assets/OpenKit3D/Models:
    /// metres (scale 1), Bake Axis Conversion (rotation 0, scale 1,1,1), no cameras/lights/animation,
    /// imported (flat) normals, and slot materials remapped to Assets/OpenKit3D/Materials/Slots/*.mat.</summary>
    public class OpenKitModelPostprocessor : AssetPostprocessor
    {
        public const string ModelsRoot = "Assets/OpenKit3D/Models/";
        public const string SlotsRoot = "Assets/OpenKit3D/Materials/Slots/";

        public override uint GetVersion() => 4;

        void OnPreprocessModel()
        {
            if (!assetPath.StartsWith(ModelsRoot)) return;
            var mi = (ModelImporter)assetImporter;
            mi.globalScale = 1f;
            mi.useFileScale = true;
            mi.bakeAxisConversion = true;
            mi.importCameras = false;
            mi.importLights = false;
            mi.importVisibility = false;
            mi.importBlendShapes = false;
            mi.meshCompression = ModelImporterMeshCompression.Off;
            mi.isReadable = false;
            mi.addCollider = false;
            mi.generateSecondaryUV = false;
            mi.importNormals = ModelImporterNormals.Import;   // flat normals come from Blender
            mi.importTangents = ModelImporterTangents.None;
            mi.weldVertices = true;
            mi.optimizeMeshPolygons = true;
            mi.optimizeMeshVertices = true;
            // props are static; monsters (M4) are rigged: Generic rig, clips imported and set to loop (OnPreprocessAnimation)
            if (!assetPath.StartsWith(ModelsRoot + "Monsters/"))
            {
                mi.animationType = ModelImporterAnimationType.None;
                mi.importAnimation = false;
            }
            else
            {
                mi.animationType = ModelImporterAnimationType.Generic;
                mi.avatarSetup = ModelImporterAvatarSetup.CreateFromThisModel;
                mi.importAnimation = true;
                mi.optimizeGameObjects = false;
                mi.skinWeights = ModelImporterSkinWeights.Standard;
                mi.animationCompression = ModelImporterAnimationCompression.Off;
                mi.resampleCurves = true;
            }
            mi.materialImportMode = ModelImporterMaterialImportMode.ImportStandard;
            mi.materialLocation = ModelImporterMaterialLocation.InPrefab;
            mi.materialName = ModelImporterMaterialName.BasedOnMaterialName;
            foreach (var slot in OpenKitConst.SlotNames)
            {
                var mat = AssetDatabase.LoadAssetAtPath<Material>(SlotsRoot + slot + ".mat");
                if (mat) mi.AddRemap(new AssetImporter.SourceAssetIdentifier(typeof(Material), slot), mat);
            }
        }

        void OnPreprocessAnimation()
        {
            if (!assetPath.StartsWith(ModelsRoot + "Monsters/")) return;
            var mi = (ModelImporter)assetImporter;
            var seen = new System.Collections.Generic.HashSet<string>();
            var clips = System.Linq.Enumerable.ToArray(System.Linq.Enumerable.Where(mi.defaultClipAnimations, c =>
            {
                int k = c.takeName.LastIndexOf('|');
                return seen.Add(k >= 0 ? c.takeName.Substring(k + 1) : c.takeName);   // one clip per action name
            }));
            foreach (var c in clips)
            {
                c.loopTime = true;
                c.loopPose = false;
                int bar = c.takeName.LastIndexOf('|');
                c.name = bar >= 0 ? c.takeName.Substring(bar + 1) : c.takeName;   // "rig|idle" -> "idle"
            }
            mi.clipAnimations = clips;
        }

        void OnPostprocessModel(GameObject root)
        {
            if (!assetPath.StartsWith(ModelsRoot)) return;
            var t = root.transform;
            if (t.localRotation != Quaternion.identity || t.localScale != Vector3.one)
                Debug.LogWarning($"[OpenKit] {assetPath}: root transform not identity after import (rot {t.localEulerAngles}, scale {t.localScale}). Check Blender export settings.");
        }
    }
}
