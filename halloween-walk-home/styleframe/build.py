# Halloween Walk Home style frames - all original, CC0. Palette from palette.css.
import os,re
_T=dict(re.findall(r'--hw-([\w-]+):\s*([^;]+);',open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"palette.css")).read()))
def tok(k): return _T[k].strip()
P=dict(pumpkin=tok("pumpkin"),pdark=tok("pumpkin-dark"),purple=tok("purple"),pmid=tok("purple-mid"),plight=tok("purple-light"),teal=tok("teal"),
 tdark=tok("teal-dark"),candle=tok("candle"),cream=tok("cream"),ink=tok("ink"),berry=tok("berry"),night=tok("night"),cellbg=tok("cell-bg"),cellbd=tok("cell-border"),
 grass="#7FBF6A",grass2="#6AAE5A",walk="#D9D2C3",road="#8A8796",house1="#E9B98A",house2="#9FC4E8",wood="#C98B55",
 skin="#E8B48A",hair="#6B3E26",uniform="#3FA37A",dog="#FBF8F2")
S=3  # outline at 1x; frame drawn at 1x*2.769 (1080/390) so scale stroke
O=lambda w=S: f'stroke="{P["ink"]}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
parts={}
def part(name,body,vb="0 0 390 844"):
    parts[name]=body
    open(f"parts/{name}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{body}</svg>')
    return body
# --- rig parts (worker F), local origin at hips, 1x px
part("rig_head_f",f'<g {O()}><path d="M-15 -66 q-6 -22 15 -24 q21 2 15 24z" fill="{P["hair"]}"/><circle cx="0" cy="-60" r="13" fill="{P["skin"]}"/><path d="M-13 -64 q2 -12 13 -12 q11 0 13 12 q-8 -6 -13 -2 q-6 -4 -13 2z" fill="{P["hair"]}"/><circle cx="14" cy="-56" r="6" fill="{P["hair"]}"/></g><circle cx="-4" cy="-59" r="2" fill="{P["ink"]}"/><circle cx="5" cy="-59" r="2" fill="{P["ink"]}"/><path d="M-4 -53 q4 4 8 0" fill="none" {O(2)}/>',"-30 -95 60 50")
part("rig_torso_uniform",f'<g {O()}><path d="M-13 -46 h26 l3 40 h-32z" fill="{P["uniform"]}"/><rect x="2" y="-38" width="9" height="6" rx="1.5" fill="{P["cream"]}" stroke-width="2"/></g><path d="M-6 -46 l6 8 l6 -8" fill="none" {O(2)}/>',"-20 -50 40 50")
_armp="M0 0 q-5 9 -3 13 q3 5 9 9"
part("rig_arm",f'<g transform="rotate(14)"><path d="{_armp}" fill="none" stroke="{P["ink"]}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/><path d="{_armp}" fill="none" stroke="{P["uniform"]}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="6" cy="22" r="4" fill="{P["skin"]}" {O(2)}/></g>',"-12 -4 24 34")
part("rig_leg",f'<rect x="-5" y="0" width="10" height="20" rx="4" fill="#3A3F5C" {O()}/><path d="M-6 18 h13 q3 6 -2 6 h-11z" fill="{P["ink"]}"/>',"-8 -2 18 28")
part("rig_hat_party",f'<path d="M-9 0 L0 -24 L9 0z" fill="{P["berry"]}" {O()}/><circle cx="0" cy="-26" r="4" fill="{P["candle"]}" {O(2)}/><path d="M-5 -8 h10" {O(2)}/>',"-12 -32 24 34")
def worker(x,y,s,step=1):
    a=parts
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="22" rx="20" ry="6" fill="{P["ink"]}" opacity=".25"/>'
      f'<g transform="translate(-6,-8) rotate({-18*step})">{a["rig_leg"]}</g><g transform="translate(6,-8) rotate({18*step})">{a["rig_leg"]}</g>'
      f'<g transform="translate(-15,-44) rotate({25*step})">{a["rig_arm"]}</g>{a["rig_torso_uniform"]}<g transform="translate(15,-44) rotate({-25*step})">{a["rig_arm"]}</g>{a["rig_head_f"]}</g>')
part("dog",f'<g {O()}><ellipse cx="0" cy="0" rx="26" ry="15" fill="{P["dog"]}"/><path d="M-20 8 v12 M-8 10 v12 M10 10 v12 M20 8 v12"/><path d="M24 -6 q14 -16 6 -24" fill="none"/><circle cx="-28" cy="-12" r="14" fill="{P["dog"]}"/><path d="M-38 -22 q-8 6 -4 16 q6 -2 6 -12z" fill="#E8DCCB"/><path d="M-40 -6 q-4 3 0 6 h6" fill="{P["dog"]}"/></g><circle cx="-31" cy="-14" r="2.2" fill="{P["ink"]}"/><circle cx="-42" cy="-5" r="3" fill="{P["ink"]}"/><path d="M-36 2 q2 6 6 2" fill="{P["berry"]}" {O(1.5)}/><path d="M-22 -2 q4 4 10 2" fill="none" stroke="{P["berry"]}" stroke-width="3"/>',"-50 -40 90 70")
part("jack_carved",f'<g {O()}><path d="M-2 -26 q2 -8 6 -10" fill="none" stroke-width="5"/><path d="M-2 -26 q2 -8 6 -10" fill="none" stroke="#5E8C3A" stroke-width="2"/><ellipse cx="0" cy="0" rx="28" ry="24" fill="{P["pumpkin"]}"/><path d="M-10 -22 q-6 22 0 46 M10 -22 q6 22 0 46" fill="none" stroke-width="2"/></g><g fill="{P["candle"]}" {O(2)}><path d="M-17 -6 l6 -9 l6 9z"/><path d="M5 -6 l6 -9 l6 9z"/><path d="M-19 -18 q8 -6 14 0 M5 -18 q8 -6 14 0" fill="none" stroke-width="3"/><path d="M-18 4 q18 18 36 0 q-18 6 -36 0z"/><path d="M-11 7 l4 11 l4 -10z M3 8 l4 10 l4 -11z" fill="#FFFFFF"/></g>',"-32 -40 64 66")
part("jack_plain",f'<g {O()}><path d="M0 -20 q1 -8 5 -10" fill="none" stroke="#5E8C3A" stroke-width="5"/><ellipse cx="0" cy="0" rx="24" ry="20" fill="{P["pumpkin"]}"/><path d="M-8 -18 q-5 18 0 38 M8 -18 q5 18 0 38" fill="none" stroke-width="2"/></g>',"-28 -34 56 56")
part("zombie_bg",f'<g opacity=".72"><ellipse cx="0" cy="34" rx="18" ry="5" fill="{P["ink"]}" opacity=".2"/><rect x="-11" y="10" width="9" height="22" rx="4" fill="#7F86A0"/><rect x="2" y="10" width="9" height="22" rx="4" fill="#7F86A0"/><path d="M-14 -16 h28 l2 30 h-32z" fill="#B49AC8"/><path d="M12 -12 q18 0 22 6" stroke="#A9C9A0" stroke-width="8" stroke-linecap="round" fill="none"/><path d="M-12 -12 q16 -4 24 4" stroke="#A9C9A0" stroke-width="8" stroke-linecap="round" fill="none"/><circle cx="0" cy="-30" r="15" fill="#A9C9A0"/><circle cx="-5" cy="-32" r="3" fill="#4D4766"/><circle cx="6" cy="-31" r="4" fill="#4D4766"/><path d="M-6 -22 q6 5 12 0" stroke="#4D4766" stroke-width="2.5" fill="none" stroke-linecap="round"/><path d="M-9 -42 L0 -66 L9 -42z" fill="#E7A4B4"/><circle cx="0" cy="-67" r="4" fill="#F0DDA0"/></g>',"-30 -75 70 115")
part("ghost_sheet",f'<path d="M-18 18 q-2 -46 18 -46 q20 0 18 46 l-6 -5 l-6 6 l-6 -6 l-6 6 l-6 -6z" fill="{P["cream"]}" {O()}/><ellipse cx="-6" cy="-6" rx="3" ry="4" fill="{P["ink"]}"/><ellipse cx="6" cy="-6" rx="3" ry="4" fill="{P["ink"]}"/><ellipse cx="0" cy="4" rx="4" ry="3" fill="{P["ink"]}"/><circle cx="-12" cy="2" r="3" fill="{P["berry"]}" opacity=".5"/><circle cx="12" cy="2" r="3" fill="{P["berry"]}" opacity=".5"/>',"-22 -32 44 54")
part("ghost_kid_peek",f'<ellipse cx="0" cy="0" rx="40" ry="44" fill="{P["teal"]}" opacity=".22"/><ellipse cx="0" cy="0" rx="31" ry="35" fill="{P["teal"]}" opacity=".45"/><path d="M-16 30 q-2 -50 16 -50 q18 0 16 50z" fill="{P["cream"]}" {O()}/><path d="M-16 22 q-14 -2 -10 -12" fill="{P["skin"]}" {O(2)}/><ellipse cx="-5" cy="-4" rx="3" ry="4" fill="{P["ink"]}"/><ellipse cx="6" cy="-4" rx="3" ry="4" fill="{P["ink"]}"/>',"-34 -36 68 72")
part("witch_moon",f'<circle cx="0" cy="0" r="80" fill="{P["teal"]}" opacity=".25"/><circle cx="0" cy="0" r="62" fill="#C9F3EC" {O()}/><circle cx="-20" cy="-14" r="9" fill="#A6E6DC"/><circle cx="18" cy="22" r="12" fill="#A6E6DC"/><g fill="{P["purple"]}"><path d="M-70 10 L60 -4 l4 4 L-70 14z"/><path d="M50 -6 l22 -10 l-4 8 l10 2 l-12 4z"/><path d="M-14 4 q-4 -18 6 -24 l-6 -18 l14 16 q10 4 6 24z"/><circle cx="2" cy="-22" r="6"/><path d="M-14 -26 l18 -2 l-6 -16z"/><path d="M-6 6 q-8 8 -18 6 l2 -4z"/></g>',"-82 -82 164 164")
part("streetlight",f'<g {O()}><rect x="-4" y="-120" width="8" height="120" fill="{P["plight"]}"/><path d="M0 -118 q0 -14 22 -14" fill="none" stroke-width="5"/><path d="M14 -136 h20 l4 10 h-28z" fill="{P["pmid"]}"/><ellipse cx="0" cy="0" rx="12" ry="5" fill="{P["pmid"]}"/></g><ellipse cx="24" cy="-124" rx="10" ry="4" fill="{P["candle"]}"/>',"-20 -145 70 155")
def shade(c,f):
    c=c.lstrip("#"); return "#"+"".join(f"{max(0,min(255,int(int(c[k:k+2],16)*f))):02X}" for k in (0,2,4))
def porch(color,roof):  # 3/4 top-down: big roof planes seen from above, short foreshortened front wall
    return (f'<g {O()}><ellipse cx="0" cy="4" rx="128" ry="12" fill="{P["ink"]}" opacity=".18" stroke="none"/>'
      f'<path d="M110 -112 L132 -146 V-26 L110 0z" fill="{shade(color,.7)}"/>'
      f'<path d="M-118 -232 H118 L126 -150 H-126z" fill="{shade(roof,1.18)}"/><path d="M-126 -150 H126 L118 -112 H-118z" fill="{roof}"/><path d="M-118 -232 H118" stroke-width="4"/>'
      f'<path d="M-90 -205 h50 M30 -200 h60 M-60 -178 h40 M40 -175 h50" stroke="{shade(roof,.8)}" stroke-width="3"/>'
      f'<rect x="-110" y="-112" width="220" height="112" fill="{color}"/><rect x="-110" y="-112" width="220" height="12" fill="{shade(color,.82)}" stroke="none"/>'
      f'<rect x="-24" y="-74" width="48" height="74" rx="6" fill="{P["wood"]}"/><circle cx="14" cy="-36" r="4" fill="{P["candle"]}"/>'
      f'<rect x="-90" y="-88" width="44" height="34" rx="4" fill="{P["candle"]}"/><rect x="46" y="-88" width="44" height="34" rx="4" fill="{P["candle"]}"/>'
      f'<path d="M-68 -88 v34 M68 -88 v34 M-90 -71 h44 M46 -71 h44" stroke-width="2"/><path d="M-62 0 h124 l8 22 h-140z" fill="#CDBBA2"/><path d="M-50 22 h100 l6 16 h-112z" fill="#E0D2BC"/></g>')
part("porch_a",porch(P["house1"],"#C2603F"),"-135 -235 270 275")
part("porch_b",porch(P["house2"],P["plight"]),"-135 -235 270 275")
part("bat",f'<path d="M0 0 q-10 -12 -30 -6 q8 6 6 12 q8 -4 12 2 q6 -6 12 -2 q6 -6 12 2 q4 -6 12 -2 q-2 -6 6 -12 q-20 -6 -30 6z" fill="{P["pmid"]}" {O(2)}/><circle cx="-3" cy="2" r="1.5" fill="{P["candle"]}"/><circle cx="3" cy="2" r="1.5" fill="{P["candle"]}"/>',"-34 -14 68 28")

W,H=390,694  # 1x canvas (scaled 2.769 to 1080x1920)
def street():
    g=[f'<rect width="{W}" height="{H}" fill="{P["grass"]}"/>']
    g.append(f'<rect x="0" y="0" width="{W}" height="150" fill="{P["pmid"]}"/>')  # sky band (top of 3/4 view)
    g.append(f'<g transform="translate(295,78) scale(.78)">{parts["witch_moon"]}</g>')
    for i,(x,y) in enumerate([(60,40),(150,60),(210,25)]): g.append(f'<g transform="translate({x},{y}) scale(.7)">{parts["bat"]}</g>' if i<2 else f'<circle cx="{x}" cy="{y}" r="2" fill="{P["cream"]}"/>')
    g.append(f'<rect x="0" y="140" width="{W}" height="20" fill="{P["grass2"]}"/>')
    g.append(f'<g transform="translate(95,260) scale(.62)">{parts["porch_a"]}</g><g transform="translate(290,260) scale(.62)">{parts["porch_b"]}</g>')
    # sidewalk
    g.append(f'<rect x="-5" y="290" width="{W+10}" height="64" fill="{P["walk"]}" {O()}/>')
    for x in range(0,W,48): g.append(f'<path d="M{x} 293 v58" stroke="#B9B1A2" stroke-width="2"/>')
    g.append(f'<rect x="72" y="260" width="46" height="32" fill="{P["walk"]}" {O()}/><rect x="267" y="260" width="46" height="32" fill="{P["walk"]}" {O()}/>')
    # road + crosswalk
    g.append(f'<rect x="-5" y="430" width="{W+10}" height="140" fill="{P["road"]}" {O()}/>')
    for x in range(10,W,60): g.append(f'<rect x="{x}" y="497" width="30" height="6" rx="3" fill="{P["candle"]}"/>')
    g.append(f'<rect x="150" y="354" width="90" height="78" fill="{P["walk"]}" {O()}/>')
    for y in range(440,566,22): g.append(f'<rect x="152" y="{y}" width="86" height="12" rx="2" fill="{P["cream"]}" {O(2)}/>')
    g.append(f'<rect x="-5" y="570" width="{W+10}" height="64" fill="{P["walk"]}" {O()}/>')
    g.append(f'<g transform="translate(330,392) scale(.85)">{parts["zombie_bg"]}</g>')
    g.append(f'<g transform="translate(30,395) scale(.95)">{parts["ghost_kid_peek"]}</g>')
    g.append(f'<g transform="translate(60,300) scale(.8)">{parts["jack_carved"]}</g><g transform="translate(330,300) scale(.8)">{parts["jack_plain"]}</g>')
    g.append(f'<g transform="translate(110,600) scale(1.1)">{parts["ghost_sheet"]}</g>')
    g.append(f'<g transform="translate(130,356)">{parts["streetlight"]}</g>')
    g.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{P["night"]}" opacity=".42"/>')  # night tint
    g.append(f'<defs><radialGradient id="pool"><stop offset="0" stop-color="{P["candle"]}" stop-opacity=".55"/><stop offset="1" stop-color="{P["candle"]}" stop-opacity="0"/></radialGradient></defs>')
    g.append(f'<ellipse cx="160" cy="370" rx="120" ry="70" fill="url(#pool)" style="mix-blend-mode:screen"/>')
    g.append(f'<ellipse cx="60" cy="300" rx="50" ry="38" fill="url(#pool)"/><ellipse cx="110" cy="600" rx="60" ry="40" fill="url(#pool)" opacity=".6"/>')
    g.append(f'<g transform="translate(155,318) scale(.6)">{parts["streetlight"].split("</g>")[0]}</g>' if False else "")
    g.append(worker(195,345,1.2))
    g.append(f'<g transform="translate(268,352) scale(.85)">{parts["dog"]}</g>')
    return "".join(g)
def svgdoc(body,w,h): return f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice">{body}</svg>'
open("styleframe_street.svg","w").write(svgdoc(street(),W,H))
# ---- bag UI mock; cell 48 at 1x, 4px inset
CELL=int(tok("cell")[:-2]); C=int(tok("cell-pitch")[:-2]); INS=int(tok("item-inset")[:-2])
def cellsvg(ox,oy,cols=4,rows=4):
    return "".join(f'<rect x="{ox+c*C}" y="{oy+r*C}" width="{CELL}" height="{CELL}" rx="8" fill="{P["cellbg"]}" stroke="{P["cellbd"]}" stroke-width="2"/>' for r in range(rows) for c in range(cols))
def it(name,ox,oy,c,r,w,h,body):
    x,y=ox+c*C+INS,oy+r*C+INS; ww,hh=w*C-(C-CELL)-2*INS,h*C-(C-CELL)-2*INS
    part("item_"+name,body(ww,hh),f"-4 -4 {ww+8} {hh+8}")
    return f'<g transform="translate({x},{y})">{body(ww,hh)}</g>'
cake=lambda w,h:f'<g {O()}><rect x="4" y="{h*.35}" width="{w-8}" height="{h*.6}" rx="8" fill="{P["cream"]}"/><path d="M14 {h*.48} q{(w-28)/8} 10 {(w-28)/4} 0 t{(w-28)/4} 0 t{(w-28)/4} 0 t{(w-28)/4} 0" fill="none" stroke="{P["berry"]}" stroke-width="5"/><circle cx="{w/2}" cy="{h*.25}" r="8" fill="{P["berry"]}"/></g>'
candles=lambda w,h:"".join(f'<g {O()}><rect x="{x}" y="{h*.3}" width="9" height="{h*.65}" rx="3" fill="{col}"/><path d="M{x+4.5} {h*.08} q6 8 0 {h*.18} q-6 -10 0 -{h*.18}" fill="{P["candle"]}" stroke-width="2"/></g>' for x,col in [(w*.15,P["teal"]),(w*.55,P["berry"])])
balloons=lambda w,h:f'<g {O()}><path d="M{w*.35} {h*.55} L{w*.5} {h}" fill="none" stroke-width="2"/><path d="M{w*.68} {h*.5} L{w*.5} {h}" fill="none" stroke-width="2"/><ellipse cx="{w*.33}" cy="{h*.32}" rx="{w*.2}" ry="{h*.26}" fill="{P["berry"]}"/><ellipse cx="{w*.68}" cy="{h*.3}" rx="{w*.2}" ry="{h*.26}" fill="{P["teal"]}"/></g>'
gift=lambda w,h:f'<g {O()}><rect x="4" y="{h*.3}" width="{w-8}" height="{h*.66}" rx="4" fill="{P["teal"]}"/><rect x="{w/2-5}" y="{h*.3}" width="10" height="{h*.66}" fill="{P["berry"]}"/><path d="M{w/2} {h*.3} q-14 -18 -16 -4 q2 6 16 4 q14 2 16 -4 q-2 -14 -16 4z" fill="{P["berry"]}"/></g>'
card=lambda w,h:f'<g {O()}><rect x="3" y="6" width="{w-6}" height="{h-12}" rx="4" fill="{P["candle"]}"/><path d="M{w/2} {h*.66} q-12 -10 -8 -16 q4 -5 8 1 q4 -6 8 -1 q4 6 -8 16z" fill="{P["berry"]}" stroke-width="2"/></g>'
def bread(w,h):  # 2x1 loaf: tall domed crown, 3 diagonal score marks, flat base
    return (f'<g {O()}><path d="M4 {h-3} V{h*.62} C4 {h*.05} {w*.18} 1 {w/2} 1 C{w*.82} 1 {w-4} {h*.05} {w-4} {h*.62} V{h-3}z" fill="#E3A35C"/>'
      f'<path d="M4 {h*.7} H{w-4}" stroke="{P["pdark"]}" stroke-width="2.5"/>'
      f'<path d="M{w*.26} {h*.42} l{w*.1} -{h*.24} M{w*.45} {h*.42} l{w*.1} -{h*.26} M{w*.64} {h*.42} l{w*.1} -{h*.24}" fill="none" stroke="#FFE3B0" stroke-width="4"/></g>')
hats=lambda w,h:"".join(f'<g {O()}><path d="M{x-12} {y} L{x} {y-h*.38} L{x+12} {y}z" fill="{col}"/><circle cx="{x}" cy="{y-h*.38-3}" r="4" fill="{P["candle"]}" stroke-width="2"/></g>' for x,y,col in [(w/2,h*.48,P["berry"]),(w/2,h*.96,P["teal"])])
batteries=lambda w,h:"".join(f'<g {O()}><rect x="{x}" y="8" width="12" height="{h-12}" rx="3" fill="{P["teal"]}"/><rect x="{x+3}" y="3" width="6" height="5" fill="{P["cream"]}" stroke-width="2"/></g>' for x in (w*.18,w*.55))
def hatsL(w,h):  # L of 3: (0,0),(0,1),(1,1)
    c=C; hs=[(c/2-4,c-14,P["berry"]),(c/2-4,2*c-14,P["teal"]),(c*1.5-4,2*c-14,P["candle"])]
    return f'<path d="M0 0 H{c-8} V{c-4} H{2*c-8} V{2*c-8} H0z" fill="{P["cream"]}" opacity=".18"/>'+"".join(f'<g {O()}><path d="M{x-13} {y} L{x} {y-c+20} L{x+13} {y}z" fill="{col}"/><circle cx="{x}" cy="{y-c+17}" r="4" fill="{P["pumpkin"]}" stroke-width="2"/></g>' for x,y,col in hs)
streamersH=lambda w,h:f'<g {O(5)} fill="none">'+"".join(f'<path d="M6 {y} q{w*.12} -12 {w*.25} 0 t{w*.25} 0 t{w*.25} 0 t{w*.2} 0" stroke="{col}"/>' for y,col in [(h*.3,P["berry"]),(h*.65,P["teal"])])+'</g>'
squish=lambda w,h:f'<rect x="-2" y="-2" width="{w+4}" height="{h+4}" rx="10" fill="{P["berry"]}" opacity=".28" stroke="{P["berry"]}" stroke-width="4" stroke-dasharray="8 6"/>'
part("fx_squish_warning_cell",squish(CELL,CELL),"-6 -6 60 60")
part("fx_tap_me_pulse",f'<circle cx="0" cy="0" r="34" fill="none" stroke="{P["candle"]}" stroke-width="6" opacity=".9"/><circle cx="0" cy="0" r="42" fill="none" stroke="{P["candle"]}" stroke-width="3" opacity=".45"/>',"-48 -48 96 96")
part("marker_star",f'<path d="M0 -20 L6 -6 L20 -6 L9 3 L13 18 L0 9 L-13 18 L-9 3 L-20 -6 L-6 -6z" fill="{P["candle"]}" {O()}/>',"-24 -24 48 46")
part("marker_gift",f'<g {O()}><rect x="-16" y="-8" width="32" height="24" rx="4" fill="{P["teal"]}"/><rect x="-4" y="-8" width="8" height="24" fill="{P["berry"]}"/><path d="M0 -8 q-12 -14 -14 -3 q2 5 14 3 q12 2 14 -3 q-2 -11 -14 3z" fill="{P["berry"]}"/></g>',"-22 -24 44 44")
GW=3*C-(C-CELL); GH=4*C-(C-CELL)
B=[f'<rect width="{W}" height="{H}" fill="{P["purple"]}"/>']
L=(W-2*GW-40)//2; R=L+GW+40; T=150; TR=T; TL=T
for ox in (L,R): B.append(f'<rect x="{ox-10}" y="{T-10}" width="{GW+20}" height="{GH+20}" rx="22" fill="{P["pmid"]}" stroke="{P["ink"]}" stroke-width="4"/>'+cellsvg(ox,T,3,4))
B.append(it("cake_2x2",L,T,0,0,2,2,cake)); B.append(f'<g transform="translate({L},{T})">{squish(2*C-4,2*C-4)}</g>')
B.append(it("candles_1x1",L,T,2,0,1,1,candles)); B.append(it("card_1x1",L,T,2,1,1,1,card)); B.append(it("streamers_1x3",L,T,0,2,3,1,streamersH))
B.append(it("gift_2x2",R,T,0,0,2,2,gift)); B.append(it("balloons_1x2",R,T,2,0,1,2,balloons)); B.append(it("bread_2x1",R,T,1,2,2,1,bread))
B.append(f'<g transform="translate({R+INS},{T+2*C+INS})">{hatsL(0,0)}</g>'); part("item_party_hats_L3",hatsL(0,0),f"-4 -4 {2*C} {2*C}")
GW=GH;TR=T
B.append(f'<rect x="{L-10}" y="{T+GH+40}" width="{W-2*L+20}" height="110" rx="22" fill="{P["cream"]}" stroke="{P["ink"]}" stroke-width="4"/>')
for i in range(7): B.append(f'<circle cx="{W/2+(i-3)*44}" cy="{T+GH+95}" r="16" fill="{[P["candle"],P["pumpkin"],P["plight"]][i%3]}" {O()}/>')
open("styleframe_bag_ui.svg","w").write(svgdoc("".join(B),W,H))

for n,f in [("reward_gift",gift),("reward_card",card)]: part(n,f(48,48),"-4 -4 56 56")
streamers=lambda w,h:f'<g {O(5)} fill="none"><path d="M4 8 q10 10 0 20 q-10 10 0 20" stroke="{P["berry"]}"/><path d="M24 8 q10 10 0 20 q-10 10 0 20" stroke="{P["teal"]}"/><path d="M44 8 q-10 10 0 20" stroke="{P["candle"]}"/></g>'
part("reward_streamers",streamers(48,48),"-4 -4 56 56")
exec(open("batch1_parts.py").read())
import json
FULL={n for n in parts}  # placeholder, recomputed per call
def is_bg(n):
    vb=open(f"parts/{n}.svg").read().split('viewBox="')[1].split('"')[0].split(); return float(vb[2])>=380 and float(vb[3])>=800
BGS=[]
def atlas(tag,names):
    MAX=2048; names=sorted(names); bgs=[n for n in names if is_bg(n)]; BGS.extend(bgs); names=[n for n in names if n not in bgs]
    pages=[[]]; x=y=rowh=0; info={}
    for n in names:
        vb=[float(v) for v in open(f"parts/{n}.svg").read().split('viewBox="')[1].split('"')[0].split()]
        w,h=int(vb[2]*2+.999)+2,int(vb[3]*2+.999)+2; assert w<=MAX and h<=MAX,n
        if x+w>MAX: x=0;y+=rowh;rowh=0
        if y+h>MAX: pages.append([]); x=y=rowh=0
        pages[-1].append((n,x,y,w,h,vb)); x+=w; rowh=max(rowh,h)
    for old in __import__("glob").glob(f"../atlas/{tag}*"): os.remove(old)
    for pi,pg in enumerate(pages):
        ptag=tag if len(pages)==1 else tag.replace("_parts",f"{'abcdefgh'[pi]}_parts")
        AH=max(y+h for n,x,y,w,h,vb in pg); fr={}; items=[]
        for n,x,y,w,h,vb in pg:
            fr[n]=dict(frame=dict(x=x,y=y,w=w,h=h),sourceSize=dict(w=w,h=h),scale=2,svg=f"styleframe/parts/{n}.svg")
            items.append(f'<svg x="{x+1}" y="{y+1}" width="{w-2}" height="{h-2}" viewBox="{" ".join(map(str,vb))}">{parts[n]}</svg>')
        open(f"../atlas/{ptag}@2x.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{MAX}" height="{AH}">{"".join(items)}</svg>')
        json.dump(dict(frames=fr,meta=dict(image=f"{ptag}@2x.png",size=dict(w=MAX,h=AH),scale=2,license="CC0, all original")),open(f"../atlas/{ptag}@2x.json","w"),indent=1)
        print("atlas",ptag,MAX,AH,len(fr))
    open(f"../atlas/{tag}.list","w").write("\n".join(sorted(names+bgs)))
B1=set(parts); atlas("batch1_parts",B1)
for _bk in (2,3):
    before=set(parts); exec(open(f"batch{_bk}_parts.py").read()); atlas(f"batch{_bk}_parts",set(parts)-before)

os.makedirs("../backgrounds",exist_ok=True)
for n in BGS:
    vb=open(f"parts/{n}.svg").read().split('viewBox="')[1].split('"')[0]
    open(f"../backgrounds/{n}.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="780" height="1688" viewBox="{vb}" preserveAspectRatio="none">{parts[n]}</svg>')
print("backgrounds",len(BGS),BGS)
