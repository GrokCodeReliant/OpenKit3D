# Regenerates art/OPEN_KIT_INVENTORY.md: one row per file incl. itself, with size and sha256.
import os,glob,hashlib
from collections import Counter
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),".."))
INV="OPEN_KIT_INVENTORY.md"
INTERNAL={"ART_PACK.VEIL.md","SELF_CRITIQUE.md","ASSET_LIST.md"}  # internal-only, not shipped (Veil condition)
def kind(p):
    if "/parts/" in p: return "SVG master"
    if p.startswith("atlas/") and p.endswith(".png"): return "atlas PNG @2x"
    if p.startswith("atlas/"): return "atlas data"
    if p.endswith(".glb"): return "3D glTF"
    if "batch4/preview_" in p: return "3D preview PNG"
    if p.startswith("backgrounds/"): return "background"
    if p.startswith("challenges/"): return "challenge composite (mock)"
    if "previews/" in p: return "sprite preview PNG"
    if "contact_sheet" in p: return "contact sheet"
    if p.startswith("styleframe/styleframe") or "composite_scene" in p: return "style frame / mock"
    if p.endswith(".css"): return "palette"
    return {"py":"source script","sh":"source script","md":"doc","json":"data"}.get(p.rsplit(".",1)[-1],"file")
def tool(p):
    if p.endswith(".glb") or "batch4/preview_" in p: return "Blender (batch4/make_3d.py)"
    if p.endswith((".py",".sh",".css",".md")): return "hand-written by the studio crew"
    if p.endswith(".svg"): return "our Python/SVG scripts"
    if p.endswith(".png"):
        if p.startswith("batch4/") or "batch4_previews" in p: return "Blender render + Python (Pillow) layout"
        if "_360" in p: return "headless Chrome render + Pillow downscale"
        return "headless Chrome render of our SVG"
    return "our Python scripts"
files=sorted(set(p for p in glob.glob("**/*",recursive=True) if os.path.isfile(p) and "__pycache__" not in p and p not in INTERNAL)|{INV})
rows=[]
for i,p in enumerate(files,1):
    if p==INV: size,h="(this file)","n/a (self)"
    else: size=os.path.getsize(p); h=hashlib.sha256(open(p,"rb").read()).hexdigest()
    rows.append(f"| {i} | `{p}` | {kind(p)} | {size} | `{h}` | original, made by the studio crew | CC0 | {tool(p)} |")
c=Counter(kind(p) for p in files)
out=["# Open Kit inventory: 'Halloween / Cozy Spooky 2D' (+ 3D pieces)","",
"For Intake. Every file below is **original, made by the studio crew** (no downloads, no third-party art or fonts, no trademarks, no real people, no religious symbols), licensed **CC0 1.0**.",
f"{len(files)} files, including this inventory. Paths are relative to `halloween-walk/art/`. Hash = SHA-256. Contact sheets use the viewer's system sans-serif only for review labels; no font is embedded in any sprite.","Internal-only files, not shipped and not listed: `ART_PACK.VEIL.md`, `SELF_CRITIQUE.md`, `ASSET_LIST.md`.","",
"| # | file | type | bytes | sha256 | source | license | tool |","|---|---|---|---|---|---|---|---|"]+rows
out+=["","## Totals by type"]+[f"- {k}: {v}" for k,v in sorted(c.items())]
out+=["","## Notes for Intake","- Signs and banners are blank panels; any text is drawn in code by the game, not baked into the art.",
"- The palette lives in `styleframe/palette.css` inside the pack; the builds read nothing outside `art/`.",
"- 3D: metres, ≤3 colour slots per mesh, ≤1500 tris, collider child per piece (see `batch4/batch4_3d.json`).",
"- Rebuild: `python3 styleframe/build.py && python3 styleframe/make_batch1.py && python3 styleframe/make_sheets.py && python3 styleframe/make_challenges.py && styleframe/render_all.sh && python3 styleframe/make_inventory.py`; 3D: `blender -b --python batch4/make_3d.py`."]
open(INV,"w").write("\n".join(out)+"\n"); print(len(files),dict(c))
