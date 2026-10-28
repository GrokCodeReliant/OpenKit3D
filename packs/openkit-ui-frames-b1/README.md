# openkit-ui-frames-b1
Parchment/wood fantasy UI chrome for the free Open Kit (13 transparent RGBA PNGs in `ui/`). Complements `openkit-icons-inventory-b1` (item glyphs); no glyphs here.
Sizes: slots 96², buttons 128×64, checkboxes 64², bars 256×32, divider 256×32, tooltip 256×128, panels 512², window 512×384 (transparent centre).
Panels/tooltip/window are 9-slice friendly (suggested border ~24px; window 52px top).
Regenerate: `python3 src/gen_ui_frames.py && python3 src/make_sheet.py`. Preview: `sheet/CONTACT_SHEET.png`.
