"""Open Kit 3D asset builder.

  blender --background --python build_asset.py -- --asset prop-chair-simple [--preview]
  blender --background --python build_asset.py -- --all --preview

Writes Blender/out/fbx/<name>.fbx, Blender/out/glb/<name>.glb,
Blender/out/previews/<name>.png and Blender/out/manifest.json (read by Unity build).
"""
import sys, os, json, time, argparse, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import okit  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "out")
PARAMS = os.path.join(ROOT, "params")
ASSETS = os.path.join(HERE, "assets")
EXCEPTIONS = okit.load_exceptions(os.path.join(ROOT, "roomadapt_exceptions.json"))
M1 = {"prop-chair-simple", "prop-table-wood", "prop-barrel", "prop-brazier", "prop-pillar-stone"}
# M4: monsters are rigged (RIG + CLIPS in the asset script); build_one validates the rig and exports FBX/GLB with armature + clips


def load_asset_module(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), os.path.join(ASSETS, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_one(name, preview):
    t0 = time.time()
    okit.reset_scene()
    mod = load_asset_module(name)
    params = okit.load_params(PARAMS, name)
    obj = mod.build(name, params)
    pivot = getattr(mod, "PIVOT", "bottom_center")
    sock = getattr(mod, "LIGHT_SOCKET", None)
    off = (0.0, 0.0, 0.0)
    if pivot == "bottom_center" and getattr(mod, "RECENTER", True):
        off = okit.recenter(obj)
        if sock:   # keep the light where it was authored relative to the mesh
            sock = [round(sock[i] + off[i], 4) for i in range(3)]
    rep = okit.validate(obj, mod.BUDGET, pivot)
    rep.update({"sizeClass": mod.SIZE_CLASS, "scalesWithRoom": mod.SCALES_WITH_ROOM,
                "category": getattr(mod, "CATEGORY", "Props"),
                "lightSocket": sock,
                "milestone": getattr(mod, "MILESTONE", "M1" if name in M1 else "M2")})
    okit.validate_extra(obj, rep, rep["category"], rep["sizeClass"], sock, mod.BUDGET)
    rep["roomScale"] = getattr(mod, "ROOM_SCALE", "inhabitant")
    rep["emissiveScale"] = getattr(mod, "EMISSIVE_SCALE", 1.0)
    okit.validate_roomadapt(obj, rep, mod.SCALES_WITH_ROOM, rep["roomScale"], getattr(mod, "EMISSIVE_SCALE", None), EXCEPTIONS)
    rig, clips = getattr(mod, "RIG", None), getattr(mod, "CLIPS", None)
    okit.validate_rig(obj, rep, rig, clips, rep["category"])
    rep["rigged"] = bool(rig)
    if rep["name"] != name:
        rep["problems"].append(f"object name {rep['name']} != script name {name}")
        rep["ok_extra"] = False
    if rig and rep["ok_rig"]:
        fbx, glb = okit.export_rigged(obj, os.path.join(OUT, "fbx"), os.path.join(OUT, "glb"), rig, clips, off)
    else:
        fbx, glb = okit.export(obj, os.path.join(OUT, "fbx"), os.path.join(OUT, "glb"))
    rep["build_seconds"] = round(time.time() - t0, 2)
    if preview:
        t1 = time.time()
        okit.render_preview(obj, os.path.join(OUT, "previews", name + ".png"), rep)
        rep["preview_seconds"] = round(time.time() - t1, 2)
    print("[okit] REPORT " + json.dumps(rep))
    return rep


def main():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser()
    ap.add_argument("--asset", action="append", default=[])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--preview", action="store_true")
    a = ap.parse_args(argv)
    names = sorted(f[:-3] for f in os.listdir(ASSETS) if f.endswith(".py")) if a.all else a.asset
    for d in ("fbx", "glb", "previews"):
        os.makedirs(os.path.join(OUT, d), exist_ok=True)
    man_path = os.path.join(OUT, "manifest.json")
    manifest = json.load(open(man_path)) if os.path.exists(man_path) else {}
    for n in names:
        manifest[n] = build_one(n, a.preview)
    # drop manifest entries whose script no longer exists (stale assets must not reach Unity)
    for n in [n for n in manifest if not os.path.exists(os.path.join(ASSETS, n + ".py"))]:
        del manifest[n]
    with open(man_path, "w") as f:
        json.dump(manifest, f, indent=2)
    # list-shaped copy for Unity's JsonUtility
    ulist = []
    for n in sorted(manifest):
        r = dict(manifest[n]); r["lightSocket"] = r.get("lightSocket") or []
        ulist.append(r)
    with open(os.path.join(OUT, "manifest_unity.json"), "w") as f:
        json.dump({"assets": ulist}, f, indent=2)
    bad = [n for n in names if not (manifest[n]["ok_budget"] and manifest[n]["ok_pivot"] and manifest[n].get("ok_extra", False)
                                 and manifest[n].get("ok_roomadapt", False) and manifest[n].get("ok_rig", True))]
    for n in bad:
        r = manifest[n]
        print(f"[okit] FAIL {n}: budget={r['ok_budget']} ({r['tris']}/{r['budget']}) pivot={r['ok_pivot']} problems={r.get('problems')} roomadapt={r.get('roomadapt_problems')} rig={r.get('rig_problems')}")
    counts = {}
    for n in names:
        counts[manifest[n].get("milestone", "?")] = counts.get(manifest[n].get("milestone", "?"), 0) + 1
    print("[okit] ROOMADAPT exceptions:", {k: sorted(v) for k, v in EXCEPTIONS.items()} or "none")
    print("[okit] DONE", len(names), "assets", counts, "; failing checks:", bad)
    if bad:
        raise SystemExit("[okit] VALIDATION FAILED: " + ", ".join(bad))


main()
