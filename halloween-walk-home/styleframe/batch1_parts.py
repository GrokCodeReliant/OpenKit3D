# Batch 1 parts. exec'd inside build.py (shares P, O, part, C, CELL, INS, parts).
def isz(cw,ch): return cw*C-(C-CELL)-2*INS, ch*C-(C-CELL)-2*INS
def item(name,cw,ch,f):
    w,h=isz(cw,ch); part(f"item_{name}",f(w,h),f"-4 -4 {w+8} {h+8}")
g=lambda inner,w=S:f'<g {O(w)}>{inner}</g>'
# --- groceries / tools (polyomino-fit, no text)
item("flashlight",1,2,lambda w,h:g(f'<rect x="{w*.3}" y="{h*.3}" width="{w*.4}" height="{h*.66}" rx="5" fill="{P["plight"]}"/><path d="M{w*.15} 4 h{w*.7} l-{w*.12} {h*.28} h-{w*.46}z" fill="{P["pumpkin"]}"/><ellipse cx="{w/2}" cy="6" rx="{w*.3}" ry="4" fill="{P["candle"]}"/><rect x="{w*.42}" y="{h*.5}" width="{w*.16}" height="10" rx="3" fill="{P["cream"]}" stroke-width="2"/>'))
item("batteries",1,1,lambda w,h:"".join(g(f'<rect x="{x}" y="10" width="13" height="{h-14}" rx="2" fill="#3A3F5C"/><rect x="{x}" y="10" width="13" height="10" fill="{P["candle"]}" stroke-width="2"/><rect x="{x+4}" y="4" width="5" height="6" fill="{P["cream"]}" stroke-width="2"/>') for x in (w*.18,w*.55)))
item("umbrella",1,3,lambda w,h:g(f'<path d="M{w/2} {h*.2} V{h-12} q0 8 -8 8 q-6 0 -6 -6" fill="none" stroke-width="6"/><path d="M4 {h*.3} q{w/2-4} -{h*.32} {w-8} 0 q-{w*.15} -8 -{w*.29} 0 q-{w*.14} -8 -{w*.28} 0 q-{w*.14} -8 -{w*.29} 0z" fill="{P["berry"]}"/>'))
item("dog_treats",1,1,lambda w,h:f'<g transform="translate({w*.12},{h*.12}) scale(.76)">'+g(f'<path d="M{w*.22} {h*.5} a8 8 0 1 1 8 -9 h{w*.4} a8 8 0 1 1 8 9 a8 8 0 1 1 -8 9 h-{w*.4} a8 8 0 1 1 -8 -9z" fill="#E9C07A"/>')+"</g>")
item("leash",2,1,lambda w,h:g(f'<path d="M10 {h/2} q{w*.25} -{h*.4} {w*.5} 0 t{w*.4} 0" fill="none" stroke="{P["berry"]}" stroke-width="8"/><circle cx="12" cy="{h/2}" r="9" fill="none" stroke-width="4"/><rect x="{w-20}" y="{h/2-6}" width="14" height="12" rx="3" fill="{P["candle"]}"/>'))
item("carving_kit",2,1,lambda w,h:g(f'<rect x="4" y="{h*.25}" width="{w-8}" height="{h*.65}" rx="6" fill="{P["pumpkin"]}"/><path d="M{w*.2} {h*.45} h{w*.25} M{w*.55} {h*.45} h{w*.25}" stroke-width="4"/><path d="M{w*.35} {h*.25} q{w*.15} -{h*.25} {w*.3} 0" fill="none"/>'))
item("glue",1,1,lambda w,h:g(f'<path d="M{w*.35} {h*.3} h{w*.3} v{h*.62} h-{w*.3}z" fill="#FFFFFF"/><path d="M{w*.42} {h*.3} L{w/2} 3 L{w*.58} {h*.3}z" fill="{P["berry"]}"/><path d="M{w*.35} {h*.55} h{w*.3}" stroke="{P["berry"]}" stroke-width="4"/>'))
item("tape",1,1,lambda w,h:g(f'<circle cx="{w/2}" cy="{h/2}" r="{w*.4}" fill="{P["candle"]}"/><circle cx="{w/2}" cy="{h/2}" r="{w*.17}" fill="{P["cellbg"]}"/><path d="M{w*.88} {h/2} h-{w*.0} v{h*.4} l-6 -5 l-6 5 v-{h*.4}" fill="{P["candle"]}" stroke-width="2"/>'))
item("bug_spray",1,2,lambda w,h:g(f'<rect x="{w*.22}" y="{h*.25}" width="{w*.56}" height="{h*.7}" rx="6" fill="{P["tdark"]}"/><rect x="{w*.35}" y="{h*.1}" width="{w*.3}" height="{h*.15}" fill="{P["cream"]}"/><circle cx="{w/2}" cy="{h*.6}" r="7" fill="{P["candle"]}" stroke-width="2"/>'))
item("bread",2,1,bread)
item("ice_cream",1,1,lambda w,h:g(f'<path d="M{w*.25} {h*.45} L{w/2} {h-3} L{w*.75} {h*.45}z" fill="{P["candle"]}"/><circle cx="{w/2}" cy="{h*.35}" r="{w*.28}" fill="{P["berry"]}"/><circle cx="{w*.42}" cy="{h*.26}" r="3" fill="{P["cream"]}" stroke="none"/>'))
item("frozen_peas",1,1,lambda w,h:g(f'<rect x="5" y="5" width="{w-10}" height="{h-10}" rx="6" fill="{P["teal"]}"/>'+"".join(f'<circle cx="{x}" cy="{h*.55}" r="5" fill="#7FBF6A" stroke-width="2"/>' for x in (w*.3,w*.5,w*.7))))
item("pumpkin",2,2,lambda w,h:parts["jack_plain"].replace('<g ',f'<g transform="translate({w/2},{h*.55}) scale({w/58})" ',1)+'</g>' if False else f'<g transform="translate({w/2},{h*.56}) scale({w/58})">{parts["jack_plain"]}</g>')
item("milk",1,2,lambda w,h:g(f'<path d="M{w*.2} {h*.3} L{w/2} {h*.12} L{w*.8} {h*.3} V{h-4} H{w*.2}z" fill="{P["cream"]}"/><rect x="{w*.4}" y="4" width="{w*.2}" height="{h*.1}" fill="{P["teal"]}"/><rect x="{w*.2}" y="{h*.5}" width="{w*.6}" height="{h*.2}" fill="{P["teal"]}" stroke-width="2"/>'))
item("apples",1,1,lambda w,h:"".join(g(f'<circle cx="{x}" cy="{h*.6}" r="{w*.24}" fill="{c}"/><path d="M{x} {h*.38} q2 -8 6 -9" fill="none" stroke-width="2"/>') for x,c in ((w*.32,P["berry"]),(w*.68,"#9BD06A"))))
# checklist (cake/candles/card/balloons/gift/hats/streamers) already exist as bag sprites; add missing named ones at locked size
item("cake",2,2,cake); item("candles",1,1,candles); item("card",1,1,card); item("balloons",1,2,balloons); item("gift",2,2,gift); item("streamers",3,1,streamersH)
part("item_party_hats",hatsL(0,0),f"-4 -4 {2*C} {2*C}")
for n in ["cake_2x2","candles_1x1","card_1x1","balloons_1x2","gift_2x2","streamers_1x3","party_hats_L3","batteries_1x1","bread_2x1"]:
    parts.pop("item_"+n,None); 
    import os as _o
    if _o.path.exists(f"parts/item_{n}.svg"): _o.remove(f"parts/item_{n}.svg")
# --- candy bucket
part("candy_bucket_empty",g(f'<path d="M-24 -10 q0 34 24 34 q24 0 24 -34z" fill="{P["pumpkin"]}"/><path d="M-26 -12 h52" stroke-width="4"/><path d="M-22 -12 q22 -36 44 0" fill="none" stroke-width="4"/><path d="M-12 0 l4 -6 l4 6z M4 0 l4 -6 l4 6z M-10 8 q10 8 20 0" fill="{P["ink"]}" stroke-width="2"/>'),"-30 -34 60 62")
part("candy_bucket_full",parts["candy_bucket_empty"]+"".join(f'<circle cx="{x}" cy="-14" r="6" fill="{c}" {O(2)}/>' for x,c in ((-12,P["berry"]),(0,P["teal"]),(12,P["candle"]))),"-30 -34 60 62")
# --- sign panels (blank; text in code)
for n,w,h,c in [("sign_corner_market",200,48,P["teal"]),("sign_sold_out",180,40,P["berry"]),("sign_birthday_banner",260,56,P["candle"])]:
    body=g(f'<rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="{c}"/><rect x="8" y="8" width="{w-16}" height="{h-16}" rx="8" fill="{P["cream"]}" stroke-width="2"/>')
    if "banner" in n: body=g(f'<path d="M-14 6 L0 {h/2} L-14 {h-6} H0z M{w+14} 6 L{w} {h/2} L{w+14} {h-6} H{w}z" fill="{P["berry"]}"/>')+body
    part(n,body,f"-18 -4 {w+36} {h+8}")
# --- rig: skins x hairs, M/F torsos
SK=dict(s1="#F4CDA8",s2="#C98D5E",s3="#7A4A2E"); HC=dict(bun="#6B3E26",short="#2A1F1A",curly="#C46A2B")
for k,c in SK.items(): part(f"rig_head_{k}",f'<circle cx="0" cy="-60" r="13" fill="{c}" {O()}/><circle cx="-4" cy="-59" r="2" fill="{P["ink"]}"/><circle cx="5" cy="-59" r="2" fill="{P["ink"]}"/><path d="M-4 -53 q4 4 8 0" fill="none" {O(2)}/>',"-18 -78 36 34")
hair=dict(bun=lambda c:f'<path d="M-13 -64 q2 -12 13 -12 q11 0 13 12 q-8 -6 -13 -2 q-6 -4 -13 2z" fill="{c}" {O()}/><circle cx="14" cy="-56" r="6" fill="{c}" {O()}/>',
 short=lambda c:f'<path d="M-14 -60 q0 -18 14 -18 q14 0 14 18 q-6 -8 -14 -8 q-8 0 -14 8z" fill="{c}" {O()}/>',
 curly=lambda c:"".join(f'<circle cx="{x}" cy="{y}" r="6" fill="{c}" {O(2)}/>' for x,y in ((-11,-66),(-4,-72),(5,-72),(12,-66))))
for k,f in hair.items(): part(f"rig_hair_{k}",f(HC[k]),"-22 -82 44 32")
part("rig_torso_f",parts["rig_torso_uniform"],"-20 -50 40 50")
part("rig_torso_m",f'<g {O()}><path d="M-15 -46 h30 l1 40 h-32z" fill="{P["uniform"]}"/><rect x="3" y="-38" width="9" height="6" rx="1.5" fill="{P["cream"]}" stroke-width="2"/></g><path d="M-6 -46 l6 6 l6 -6" fill="none" {O(2)}/>',"-20 -50 40 50")
part("rig_name_tag_blank",f'<rect x="0" y="0" width="18" height="12" rx="3" fill="{P["cream"]}" {O(2)}/>',"-3 -3 24 18")
part("rig_hat_slot",f'<circle r="3" fill="{P["teal"]}"/>',"-4 -4 8 8")  # anchor marker; party hat is rig_hat_party
# --- street tiles (2x2 cells = 100 px, 1x)
T=2*C-(C-CELL)
def tile(n,inner,cw=2,ch=2): part(f"tile_{n}",inner,f"-2 -2 {cw*C-(C-CELL)+4} {ch*C-(C-CELL)+4}")
walk=lambda x,y,w,h:f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{P["walk"]}" {O()}/>'
tile("sidewalk_straight",f'<rect width="{T}" height="{T}" fill="{P["grass"]}"/>'+walk(0,T*.3,T,T*.4)+f'<path d="M{T/2} {T*.3} v{T*.4}" stroke="#B9B1A2" stroke-width="2"/>')
tile("sidewalk_corner",f'<rect width="{T}" height="{T}" fill="{P["grass"]}"/><path d="M0 {T*.3} H{T*.7} V{T} H{T*.3} V{T*.7} H0z" fill="{P["walk"]}" {O()}/>')
tile("sidewalk_T",f'<rect width="{T}" height="{T}" fill="{P["grass"]}"/>'+walk(0,T*.3,T,T*.4)+f'<rect x="{T*.3}" y="{T*.7}" width="{T*.4}" height="{T*.3}" fill="{P["walk"]}"/><path d="M{T*.3} {T*.7} V{T} M{T*.7} {T*.7} V{T}" {O()}/>')
tile("crosswalk",f'<rect width="{T}" height="{T}" fill="{P["road"]}"/>'+"".join(f'<rect x="{T*.15}" y="{y}" width="{T*.7}" height="10" rx="2" fill="{P["cream"]}" {O(2)}/>' for y in range(6,T-6,20)))
tile("road_lane",f'<rect width="{T}" height="{T}" fill="{P["road"]}"/><rect x="{T*.1}" y="{T/2-3}" width="{T*.35}" height="6" rx="3" fill="{P["candle"]}"/><rect x="{T*.6}" y="{T/2-3}" width="{T*.35}" height="6" rx="3" fill="{P["candle"]}"/>')
tile("driveway",f'<rect width="{T}" height="{T}" fill="{P["grass"]}"/><rect x="{T*.2}" y="0" width="{T*.6}" height="{T}" fill="#C9BFAE" {O()}/><path d="M{T*.2} {T*.33} h{T*.6} M{T*.2} {T*.66} h{T*.6}" stroke="#A89E8C" stroke-width="2"/><path d="M{T*.4} {T*.1} l6 10 l-4 8" fill="none" stroke="#A89E8C" stroke-width="2"/><circle cx="{T*.62}" cy="{T*.8}" r="3" fill="#A89E8C"/>')
tile("lawn",f'<rect width="{T}" height="{T}" fill="{P["grass"]}"/>'+"".join(f'<path d="M{x} {y} l3 -7 l3 7" fill="none" stroke="{P["grass2"]}" stroke-width="2"/>' for x,y in ((20,30),(60,70),(70,24),(30,80))))
tile("hedge",f'<rect width="{T}" height="{T}" fill="{P["grass"]}"/><rect x="2" y="{T*.25}" width="{T-4}" height="{T*.5}" rx="22" fill="{P["grass2"]}" {O()}/>')
tile("fence",f'<rect width="{T}" height="{T}" fill="{P["grass"]}"/>'+"".join(f'<path d="M{x} {T*.75} V{T*.3} l7 -8 l7 8 V{T*.75}z" fill="{P["cream"]}" {O(2)}/>' for x in range(4,T-10,19))+f'<path d="M0 {T*.45} H{T} M0 {T*.65} H{T}" {O(2)}/>')
for k,(c,r) in dict(A=(P["house1"],"#C2603F"),B=(P["house2"],P["plight"]),C=("#F2D27A",P["tdark"])).items(): tile(f"porch_{k}",f'<g transform="translate(100,190) scale(.72)">{porch(c,r)}</g>',4,4)
tile("streetlight",f'<rect width="{T}" height="{T}" fill="{P["grass"]}"/><g transform="translate({T*.35},{T-6}) scale(.62)">{parts["streetlight"]}</g>')
tile("mailbox",f'<rect width="{T}" height="{T}" fill="{P["grass"]}"/>'+g(f'<rect x="{T/2-3}" y="{T*.45}" width="6" height="{T*.45}" fill="{P["wood"]}"/><path d="M{T*.25} {T*.5} V{T*.3} q0 -14 {T*.25} -14 q{T*.25} 0 {T*.25} 14 V{T*.5}z" fill="{P["teal"]}"/><path d="M{T*.72} {T*.25} v-14 h12 v8 h-12" fill="{P["berry"]}" stroke-width="2"/>'))
tile("tree",f'<rect width="{T}" height="{T}" fill="{P["grass"]}"/>'+g(f'<rect x="{T/2-6}" y="{T*.55}" width="12" height="{T*.4}" fill="{P["wood"]}"/><circle cx="{T/2}" cy="{T*.38}" r="{T*.34}" fill="#E08A3C"/><circle cx="{T*.35}" cy="{T*.3}" r="{T*.08}" fill="{P["candle"]}" stroke="none"/>'))
# --- store front / interior / home exterior
part("store_front",g(f'<ellipse cx="200" cy="244" rx="215" ry="12" fill="{P["ink"]}" opacity=".18" stroke="none"/><path d="M-6 -30 H406 L412 60 H-12z" fill="#B7AFC4"/><rect x="40" y="-14" width="60" height="30" rx="6" fill="#9A93A8"/><rect x="300" y="-10" width="40" height="40" rx="20" fill="#9A93A8"/><rect x="0" y="60" width="400" height="180" fill="#F6C98A"/><rect x="0" y="60" width="400" height="10" fill="#D9A96A" stroke="none"/><path d="M-12 60 h424 l-12 28 '+"".join("q-12.5 12 -25 0 " for _ in range(16))+f'z" fill="{P["berry"]}"/><rect x="150" y="120" width="100" height="120" fill="#FFE9A8"/><path d="M200 120 v120"/><rect x="20" y="112" width="110" height="80" rx="4" fill="#FFE9A8"/><rect x="270" y="112" width="110" height="80" rx="4" fill="#FFE9A8"/><path d="M140 240 h120 l10 20 h-140z" fill="#CDBBA2"/>')+f'<g transform="translate(100,58)">{parts["sign_corner_market"]}</g>',"-16 -34 432 300")
part("store_interior",g(f'<rect width="390" height="844" fill="#EFE6D6"/><rect y="600" width="390" height="244" fill="#D9CBB2"/>'+"".join(f'<rect x="30" y="{y}" width="330" height="14" fill="{P["wood"]}"/>' for y in (240,360,480))+f'<rect x="30" y="200" width="330" height="300" fill="none"/>'+"".join(f'<rect x="{x}" y="{y-34}" width="22" height="34" rx="4" fill="{c}" stroke-width="2"/>' for y in (360,480) for x,c in zip(range(46,340,40),[P["teal"],P["pumpkin"],P["berry"],P["candle"]]*3)))+f'<g transform="translate(110,150)">{parts["sign_sold_out"]}</g>',"0 0 390 844")
part("home_exterior",f'<g transform="translate(135,235)">{porch("#F7C6A3",P["berry"])}</g><g transform="translate(215,255) scale(.5)">{parts["jack_carved"]}</g>',"0 0 270 275")
part("fx_night_tint",f'<rect width="390" height="844" fill="{P["night"]}" opacity=".42"/>',"0 0 390 844")
part("fx_light_pool",f'<defs><radialGradient id="lp"><stop offset="0" stop-color="{P["candle"]}" stop-opacity=".6"/><stop offset="1" stop-color="{P["candle"]}" stop-opacity="0"/></radialGradient></defs><ellipse cx="0" cy="0" rx="120" ry="70" fill="url(#lp)"/>',"-120 -70 240 140")
for n in ["porch_a","porch_b"]:
    parts.pop(n,None); _o.remove(f"parts/{n}.svg")
