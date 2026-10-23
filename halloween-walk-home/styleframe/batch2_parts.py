# Batch 2: story + challenges. exec'd in build.py globals.
ST=lambda c,f=1:shade(c,f)
# costumes (rig overlays: torso + hat slot pieces)
def torso(c,extra=""): return f'<g {O()}><path d="M-14 -46 h28 l3 40 h-34z" fill="{c}"/></g>{extra}'
part("costume_sheet_torso",f'<path d="M-18 -4 q-2 -46 18 -46 q20 0 18 46 l-6 -5 l-6 6 l-6 -6 l-6 6 l-6 -6z" fill="{P["cream"]}" {O()}/>',"-22 -54 44 56")
part("costume_pumpkin_torso",f'<ellipse cx="0" cy="-26" rx="22" ry="20" fill="{P["pumpkin"]}" {O()}/><path d="M-8 -44 q-5 18 0 36 M8 -44 q5 18 0 36" fill="none" {O(2)}/>',"-26 -50 52 48")
part("costume_cat_torso",torso("#3A3F5C",f'<path d="M14 -10 q16 -2 12 -22" fill="none" {O(4)}/>'),"-20 -50 50 50")
part("costume_cat_ears",f'<path d="M-12 -70 l2 -14 l8 9z M12 -70 l-2 -14 l-8 9z" fill="#3A3F5C" {O(2)}/>',"-16 -88 32 22")
part("costume_robot_torso",f'<rect x="-15" y="-46" width="30" height="40" rx="4" fill="#A9B4C8" {O()}/><circle cx="-5" cy="-30" r="3" fill="{P["berry"]}"/><circle cx="5" cy="-30" r="3" fill="{P["teal"]}"/><rect x="-7" y="-20" width="14" height="5" fill="{P["candle"]}" {O(1.5)}/>',"-19 -50 38 48")
part("costume_robot_antenna",f'<path d="M0 -72 v-12" {O(2)}/><circle cx="0" cy="-86" r="4" fill="{P["berry"]}" {O(2)}/>',"-6 -92 12 22")
part("costume_bee_torso",torso(P["candle"],f'<path d="M-15 -34 h30 M-16 -22 h32" stroke="{P["ink"]}" stroke-width="5"/><ellipse cx="-18" cy="-40" rx="9" ry="6" fill="#DDF3F1" {O(2)}/><ellipse cx="18" cy="-40" rx="9" ry="6" fill="#DDF3F1" {O(2)}/>'),"-30 -50 60 50")
part("costume_bee_antennae",f'<path d="M-5 -72 q-4 -10 -8 -12 M5 -72 q4 -10 8 -12" fill="none" {O(2)}/><circle cx="-13" cy="-85" r="3" fill="{P["ink"]}"/><circle cx="13" cy="-85" r="3" fill="{P["ink"]}"/>',"-18 -90 36 20")
# jack variants, spooks
part("jack_carved_unlit",f'<g {O()}><path d="M-2 -26 q2 -8 6 -10" fill="none" stroke="#5E8C3A" stroke-width="5"/><ellipse cx="0" cy="0" rx="28" ry="24" fill="{P["pumpkin"]}"/><path d="M-10 -22 q-6 22 0 46 M10 -22 q6 22 0 46" fill="none" stroke-width="2"/></g><g fill="#6B4A3A" {O(2)}><ellipse cx="-10" cy="-7" rx="5" ry="6"/><ellipse cx="10" cy="-7" rx="5" ry="6"/><path d="M-14 6 q14 14 28 0z"/></g><circle cx="-8" cy="-9" r="1.6" fill="#FFFFFF"/><circle cx="12" cy="-9" r="1.6" fill="#FFFFFF"/><circle cx="-20" cy="4" r="3.5" fill="{P["berry"]}" opacity=".5"/><circle cx="20" cy="4" r="3.5" fill="{P["berry"]}" opacity=".5"/>',"-32 -40 64 66")
part("zombie_bg_2",parts["zombie_bg"].replace("#B49AC8","#9CC0D8").replace('<path d="M-9 -42 L0 -66 L9 -42z" fill="#E7A4B4"/><circle cx="0" cy="-67" r="4" fill="#F0DDA0"/>','<path d="M-14 -42 q14 -14 28 0z" fill="#C9A0D6"/>'),"-30 -75 70 115")
part("ghost_little_2",parts["ghost_sheet"].replace('<ellipse cx="0" cy="4" rx="4" ry="3"','<path d="M-5 2 q5 6 10 0" fill="none" stroke="'+P["ink"]+'" stroke-width="2.5"/><ellipse cx="0" cy="40" rx="0" ry="0"'),"-22 -32 44 54")
part("dog_sit",f'<g {O()}><path d="M-14 18 q-8 -30 10 -34 q18 4 14 34z" fill="{P["dog"]}"/><path d="M8 18 q14 0 16 -10" fill="none"/><circle cx="-4" cy="-20" r="14" fill="{P["dog"]}"/><path d="M-16 -28 q-8 6 -4 16 q6 -2 6 -12z M8 -28 q8 6 4 16 q-6 -2 -6 -12z" fill="#E8DCCB"/></g><circle cx="-9" cy="-22" r="2.2" fill="{P["ink"]}"/><circle cx="2" cy="-22" r="2.2" fill="{P["ink"]}"/><circle cx="-3" cy="-14" r="3" fill="{P["ink"]}"/><path d="M-6 -8 q3 6 6 0" fill="{P["berry"]}" {O(1.5)}/>',"-30 -40 60 62")
kit=lambda pose:f'<g {O(2.5)}>'+(f'<ellipse cx="0" cy="0" rx="14" ry="8" fill="{P["pumpkin"]}"/><path d="M-10 6 v6 M-4 7 v6 M5 7 v6 M11 6 v6" />' if pose=="walk" else f'<path d="M-9 10 q-4 -18 9 -18 q13 0 9 18z" fill="{P["pumpkin"]}"/>')+f'<path d="M12 -2 q10 -4 8 -14" fill="none"/><circle cx="-13" cy="-8" r="9" fill="{P["pumpkin"]}"/><path d="M-20 -14 l1 -8 l5 5z M-8 -14 l1 -8 l-6 4z" fill="{P["pumpkin"]}"/></g><circle cx="-16" cy="-9" r="1.6" fill="{P["ink"]}"/><circle cx="-10" cy="-9" r="1.6" fill="{P["ink"]}"/>'
part("kitten_walk",kit("walk"),"-26 -26 50 42"); part("kitten_sit",kit("sit"),"-26 -26 50 42")
part("ghost_kid_full",f'<ellipse cx="0" cy="4" rx="34" ry="40" fill="{P["teal"]}" opacity=".35"/><path d="M-18 36 q-2 -60 18 -60 q20 0 18 60 l-6 -5 l-6 6 l-6 -6 l-6 6 l-6 -6z" fill="{P["cream"]}" {O()}/><ellipse cx="-6" cy="-6" rx="3" ry="4" fill="{P["ink"]}"/><ellipse cx="6" cy="-6" rx="3" ry="4" fill="{P["ink"]}"/><path d="M-12 40 v6 M12 40 v6" {O(4)}/>',"-36 -38 72 88")
part("ghost_kid_grin",f'<path d="M-24 -20 q24 -30 48 0 q-6 -6 -12 -2 q-6 -6 -12 0 q-6 -6 -12 0 q-6 -4 -12 2z" fill="{P["cream"]}" {O()}/><circle cx="0" cy="0" r="16" fill="{P["skin"]}" {O()}/><circle cx="-6" cy="-2" r="2.2" fill="{P["ink"]}"/><circle cx="6" cy="-2" r="2.2" fill="{P["ink"]}"/><path d="M-8 5 q8 10 16 0z" fill="#FFFFFF" {O(2)}/><path d="M-12 16 h24 l4 30 h-32z" fill="{P["cream"]}" {O()}/>',"-28 -40 56 90")
part("witch_silhouette",f'<g fill="{P["purple"]}"><path d="M-70 10 L60 -4 l4 4 L-70 14z"/><path d="M50 -6 l22 -10 l-4 8 l10 2 l-12 4z"/><path d="M-14 4 q-4 -18 6 -24 l-6 -18 l14 16 q10 4 6 24z"/><circle cx="2" cy="-22" r="6"/><path d="M-14 -26 l18 -2 l-6 -16z"/></g>',"-74 -46 150 64")
part("moon_full",f'<circle r="80" fill="{P["teal"]}" opacity=".25"/><circle r="62" fill="#C9F3EC" {O()}/><circle cx="-20" cy="-14" r="9" fill="#A6E6DC"/><circle cx="18" cy="22" r="12" fill="#A6E6DC"/>',"-82 -82 164 164")
def car(c): return (f'<g {O()}><ellipse cx="0" cy="34" rx="70" ry="8" fill="{P["ink"]}" opacity=".18" stroke="none"/><path d="M-66 24 v-22 q0 -8 10 -10 l20 -4 l14 -20 h44 l16 20 l20 4 q8 2 8 10 v22z" fill="{c}"/>'
  f'<path d="M-16 -10 l10 -14 h16 v14z M16 -10 v-14 h12 l10 14z" fill="#CFEFF0"/><circle cx="-40" cy="26" r="12" fill="#3A3F5C"/><circle cx="40" cy="26" r="12" fill="#3A3F5C"/><circle cx="-40" cy="26" r="4" fill="{P["cream"]}"/><circle cx="40" cy="26" r="4" fill="{P["cream"]}"/>'
  f'<circle cx="64" cy="6" r="5" fill="{P["candle"]}"/><path d="M56 16 q4 4 8 0" fill="none" stroke-width="2"/></g>')
part("car_cartoon_teal",car(P["teal"]),"-74 -40 148 84"); part("car_cartoon_berry",car(P["berry"]),"-74 -40 148 84")
for st,c,icon in [("walk","#7FE08A",f'<circle cx="0" cy="-12" r="4" fill="#7FE08A"/><path d="M0 -8 v10 l-5 8 M0 2 l5 8 M-5 -4 l5 -2 l5 4" fill="none" stroke="#7FE08A" stroke-width="3" stroke-linecap="round"/>'),("wait",P["pumpkin"],f'<rect x="-8" y="-6" width="16" height="16" rx="5" fill="{P["pumpkin"]}"/>'+"".join(f'<rect x="{x}" y="-16" width="3.5" height="12" rx="1.7" fill="{P["pumpkin"]}"/>' for x in (-8,-3.5,1,5.5))+f'<rect x="-14" y="-2" width="8" height="4" rx="2" fill="{P["pumpkin"]}" transform="rotate(-30 -8 0)"/>')]:
    part(f"walk_signal_{st}",f'<rect x="-3" y="18" width="6" height="40" fill="{P["plight"]}" {O(2)}/><rect x="-18" y="-24" width="36" height="44" rx="8" fill="#3A3F5C" {O()}/>{icon}',"-22 -28 44 90")
part("fx_curse_flicker","".join(f'<path d="M{x} {y} l4 -10 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4z" fill="{c}" {O(2)}/>' for x,y,c in ((-20,-10,P["plight"]),(14,6,P["teal"]),(-4,22,P["candle"]))),"-36 -26 66 64")
part("fx_bee_puff","".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{P["cream"]}" opacity=".9" {O(2)}/>' for x,y,r in ((-12,4,12),(8,-4,14),(10,12,9)))+f'<ellipse cx="22" cy="-16" rx="7" ry="5" fill="{P["candle"]}" {O(2)}/><path d="M20 -20 v8 M24 -20 v8" stroke="{P["ink"]}" stroke-width="2"/>',"-28 -26 60 50")
part("fx_ghost_poof","".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{P["teal"]}" opacity="{o}"/>' for x,y,r,o in ((0,0,30,.25),(-14,-6,14,.5),(12,-10,12,.5),(4,12,13,.5)))+"".join(f'<path d="M{x} {y} l3 -7 l3 7 l7 3 l-7 3 l-3 7 l-3 -7 l-7 -3z" fill="{P["candle"]}"/>' for x,y in ((-26,-22),(22,18),(20,-26)))+f'<path d="M-6 0 q6 6 12 0" fill="none" {O(2.5)}/><circle cx="-6" cy="-6" r="2" fill="{P["ink"]}"/><circle cx="6" cy="-6" r="2" fill="{P["ink"]}"/>',"-36 -36 72 72")
# home interior dark/lit
def interior(lit):
    wall="#E9D7C0" if lit else "#6E5E86"; floor="#C9A27A" if lit else "#4D4166"
    return (f'<rect width="390" height="844" fill="{wall}"/><rect y="560" width="390" height="284" fill="{floor}"/>'
      f'<g {O()}><rect x="40" y="200" width="120" height="150" rx="6" fill="{"#BFE7E4" if lit else "#2E2448"}"/><path d="M100 200 v150 M40 275 h120"/>'
      f'<rect x="210" y="400" width="140" height="170" fill="{P["wood"] if lit else "#5C4A6E"}"/><rect x="60" y="470" width="120" height="16" fill="{P["wood"] if lit else "#5C4A6E"}"/><path d="M70 486 v84 M170 486 v84"/>'
      f'<rect x="180" y="150" width="10" height="40" fill="{P["cream"]}"/><circle cx="185" cy="200" r="14" fill="{P["candle"] if lit else "#8C7FA6"}"/></g>')
part("home_interior_dark",interior(False),"0 0 390 844"); part("home_interior_lit",interior(True),"0 0 390 844")
# party guests (rig torso recolours) + dog owner NPC
for n,c in (("party_guest_torso_1",P["berry"]),("party_guest_torso_2",P["teal"]),("party_guest_torso_3",P["candle"]),("party_guest_torso_4",P["plight"])): part(n,torso(c),"-20 -50 40 50")
part("npc_dog_owner_torso",torso("#C77B9E",f'<path d="M-2 -46 v40 M2 -46 v40" {O(2)}/><circle cx="-6" cy="-34" r="2" fill="{P["cream"]}"/><circle cx="-6" cy="-22" r="2" fill="{P["cream"]}"/>'),"-20 -50 40 50")
part("npc_dog_owner_hair",f'<path d="M-15 -58 q-2 -22 15 -22 q17 0 15 22 q-4 -10 -15 -10 q-11 0 -15 10z" fill="#D9D4CF" {O()}/><circle cx="-6" cy="-58" r="5" fill="none" {O(1.5)}/><circle cx="6" cy="-58" r="5" fill="none" {O(1.5)}/>',"-20 -84 40 32")
# challenge screens (390x844 backdrops) + porch decorations
def screen(bg,inner): return f'<rect width="390" height="844" fill="{bg}"/>'+inner
part("challenge_clue_board",screen(P["purple"],f'<g {O()}><rect x="30" y="160" width="330" height="420" rx="18" fill="{P["wood"]}"/><rect x="50" y="180" width="290" height="380" rx="10" fill="#E8C89A"/></g>'+"".join(f'<rect x="{x}" y="{y}" width="110" height="90" rx="6" fill="{P["cream"]}" {O(2)} transform="rotate({r} {x+55} {y+45})"/><circle cx="{x+55}" cy="{y+4}" r="6" fill="{P["berry"]}" {O(2)}/>' for x,y,r in ((70,200,-4),(210,210,5),(80,350,3),(205,360,-6)))+f'<path d="M125 290 L265 300 L135 440 L260 450" fill="none" stroke="{P["berry"]}" stroke-width="3" stroke-dasharray="8 6"/>'))
part("challenge_carving_trace",screen(P["purple"],f'<g transform="translate(195,420) scale(5)">{parts["jack_plain"]}</g><g fill="none" stroke="{P["cream"]}" stroke-width="5" stroke-dasharray="10 8" stroke-linecap="round"><path d="M125 380 l30 -45 l30 45z M205 380 l30 -45 l30 45z M120 440 q75 70 150 0"/></g><circle cx="125" cy="380" r="10" fill="{P["candle"]}" {O()}/>'))
paw=lambda x,y,r,o=1:f'<g transform="translate({x},{y}) rotate({r}) scale(1.25)" fill="#3A2A4A" opacity="{o}"><ellipse cx="0" cy="4" rx="7" ry="6"/><circle cx="-7" cy="-5" r="3"/><circle cx="0" cy="-8" r="3"/><circle cx="7" cy="-5" r="3"/></g>'
part("challenge_paw_prints",screen(P["grass"],f'<rect x="0" y="300" width="390" height="120" fill="{P["walk"]}" {O()}/>'+"".join(paw(40+i*44,640-i*60+(i%2)*20,-30+i*8) for i in range(8))))
part("challenge_porch_decor",screen(P["purple"],f'<g transform="translate(195,700) scale(1.35)">{porch(P["house2"],P["plight"])}</g><rect x="0" y="720" width="390" height="124" fill="{P["pmid"]}"/>'+"".join(f'<rect x="{18+i*62}" y="740" width="56" height="56" rx="12" fill="{P["cellbg"]}" stroke="{P["cellbd"]}" stroke-width="2"/>' for i in range(6))))
DEC=dict(deco_bat_garland=f'<path d="M-30 -6 q30 18 60 0" fill="none" {O(2)}/>'+"".join(f'<g transform="translate({x},{y}) scale(.35)">{parts["bat"]}</g>' for x,y in ((-18,0),(0,6),(18,0))),
 deco_paper_lantern=f'<path d="M0 -24 v6" {O(2)}/><ellipse cx="0" cy="0" rx="16" ry="18" fill="{P["pumpkin"]}" {O()}/><path d="M-16 0 h32 M-12 -10 h24 M-12 10 h24" {O(2)}/>',
 deco_spider_toy=f'<path d="M0 -26 v14" {O(1.5)}/><g {O(2.5)} fill="none"><path d="M-6 -4 l-12 -6 M-6 0 l-14 2 M-6 4 l-12 8 M6 -4 l12 -6 M6 0 l14 2 M6 4 l12 8"/></g><circle cx="0" cy="0" r="9" fill="{P["plight"]}" {O()}/><circle cx="-3" cy="-2" r="2.5" fill="{P["cream"]}"/><circle cx="3" cy="-2" r="2.5" fill="{P["cream"]}"/>',
 deco_wreath=f'<circle r="18" fill="none" stroke="{P["ink"]}" stroke-width="12"/><circle r="18" fill="none" stroke="{P["pumpkin"]}" stroke-width="7"/><path d="M-6 16 l6 8 l6 -8z" fill="{P["plight"]}" {O(2)}/>',
 deco_scarecrow_mini=f'<path d="M0 -6 v30 M-16 2 h32" {O(4)}/><circle cx="0" cy="-12" r="9" fill="#E8C07A" {O()}/><path d="M-14 -18 h28 l-8 -10 h-12z" fill="{P["wood"]}" {O(2)}/>',
 deco_candy_bowl=f'<path d="M-20 -2 q0 22 20 22 q20 0 20 -22z" fill="{P["teal"]}" {O()}/>'+"".join(f'<circle cx="{x}" cy="-5" r="5" fill="{c}" {O(1.5)}/>' for x,c in ((-10,P["berry"]),(0,P["candle"]),(10,P["pumpkin"]))))
for n,b in DEC.items(): part(n,b,"-30 -30 60 60")

# ---- challenge interactive pieces (M1 priority)
CI={}
# clue board
for i,(c,ic) in enumerate(((P["teal"],"witch_hat"),(P["berry"],"pumpkin"),(P["candle"],"bat"),(P["plight"],"house"))):
    icon=dict(witch_hat=f'<path d="M-14 10 h28 L4 -14 l-10 6z" fill="{P["plight"]}" {O(2)}/>',pumpkin=f'<ellipse cy="4" rx="13" ry="10" fill="{P["pumpkin"]}" {O(2)}/><path d="M0 -6 v-5" {O(2)}/>',bat=f'<g transform="translate(0,4) scale(.6)">{parts["bat"]}</g>',house=f'<path d="M-12 12 V-2 L0 -12 L12 -2 V12z" fill="{P["plight"]}" {O(2)}/>')[ic]
    CI[f"ui_clue_card_{ic}"]=(f'<rect x="-36" y="-30" width="72" height="60" rx="6" fill="{P["cream"]}" {O()}/><rect x="-36" y="-30" width="72" height="10" fill="{c}" {O(2)}/>{icon}',"-40 -34 80 68")
CI["ui_clue_card_back"]=(f'<rect x="-36" y="-30" width="72" height="60" rx="6" fill="{P["pmid"]}" {O()}/><path d="M-8 -6 q0 -10 8 -10 q8 0 8 8 q0 6 -8 8 v6" fill="none" stroke="{P["candle"]}" stroke-width="5" stroke-linecap="round"/><circle cx="0" cy="16" r="3" fill="{P["candle"]}"/>',"-40 -34 80 68")
CI["ui_clue_pin"]=(f'<circle cy="-4" r="8" fill="{P["berry"]}" {O()}/><path d="M0 4 v8" {O(2)}/><circle cx="-3" cy="-7" r="2" fill="#FFFFFF"/>',"-12 -16 24 30")
CI["ui_clue_string_end"]=(f'<circle r="5" fill="{P["berry"]}" {O(2)}/>',"-8 -8 16 16")
CI["ui_clue_match_check"]=(f'<circle r="18" fill="#7FE08A" {O()}/><path d="M-8 0 l6 6 l10 -12" fill="none" {O(4)}/>',"-22 -22 44 44")
# carving trace
CI["ui_trace_dot"]=(f'<circle r="12" fill="{P["cream"]}" {O(3)}/>',"-16 -16 32 32")
CI["ui_trace_dot_done"]=(f'<circle r="12" fill="{P["candle"]}" {O(3)}/>',"-16 -16 32 32")
CI["ui_trace_start"]=(f'<circle r="14" fill="#7FE08A" {O()}/><path d="M-4 -7 l10 7 l-10 7z" fill="{P["cream"]}" {O(2)}/>',"-18 -18 36 36")
CI["ui_trace_end"]=(f'<circle r="14" fill="{P["candle"]}" {O()}/>'+parts["marker_star"].replace('<path d=','<path transform="scale(.45)" d=',1),"-18 -18 36 36")
CI["ui_carving_scoop"]=(f'<g transform="rotate(-35)"><rect x="-5" y="0" width="10" height="34" rx="4" fill="{P["teal"]}" {O()}/><ellipse cx="0" cy="-8" rx="9" ry="12" fill="#C9D3E0" {O()}/></g>',"-24 -28 48 60")
CI["ui_carve_chunk"]=(f'<path d="M-8 -6 l10 -4 l8 8 l-6 10 l-10 -2z" fill="{P["pumpkin"]}" {O(2)}/>',"-12 -14 24 28")
CI["fx_success_sparkle"]=("".join(f'<path d="M{x} {y} l4 -10 l4 10 l10 4 l-10 4 l-4 10 l-4 -10 l-10 -4z" fill="{c}" {O(2)}/>' for x,y,c in ((-24,-14,P["candle"]),(16,-20,P["teal"]),(4,14,P["berry"]),(-30,18,P["candle"]))),"-44 -34 80 68")
# lost pet
CI["ui_paw_print"]=(paw(0,0,0),"-12 -14 24 24")
CI["ui_paw_print_found"]=(f'<circle r="14" fill="{P["candle"]}" opacity=".6"/>'+paw(0,0,0),"-16 -16 32 32")
CI["ui_hide_bush"]=(f'<g {O()}><circle cx="-16" cy="4" r="16" fill="{P["grass2"]}"/><circle cx="14" cy="4" r="16" fill="{P["grass2"]}"/><circle cx="0" cy="-8" r="18" fill="{P["grass2"]}"/></g>',"-36 -30 72 54")
CI["ui_hide_bush_peek"]=(f'<g transform="translate(0,-14)"><g {O()}><path d="M-17 -30 l3 -16 l11 10z M17 -30 l-3 -16 l-11 10z" fill="{P["pumpkin"]}"/><circle cx="0" cy="-26" r="15" fill="{P["pumpkin"]}"/></g><path d="M-14 -33 l1.5 -8 l5 5z M14 -33 l-1.5 -8 l-5 5z" fill="{P["cream"]}"/><circle cx="-6" cy="-28" r="3" fill="{P["ink"]}"/><circle cx="6" cy="-28" r="3" fill="{P["ink"]}"/><circle cx="-5" cy="-29" r="1" fill="#FFFFFF"/><circle cx="7" cy="-29" r="1" fill="#FFFFFF"/><path d="M-3 -21 l3 2 l3 -2" fill="none" {O(2)}/></g>'+CI["ui_hide_bush"][0],"-36 -64 72 88")
CI["ui_hide_box"]=(f'<path d="M-22 -6 h44 v26 h-44z" fill="{P["wood"]}" {O()}/><path d="M-22 -6 l-6 -10 h44 l12 10z" fill="#E0A870" {O()}/>',"-32 -20 64 44")
CI["ui_hide_trash_can"]=(f'<path d="M-16 -10 h32 l-3 32 h-26z" fill="#A9B4C8" {O()}/><rect x="-19" y="-16" width="38" height="7" rx="3" fill="#8C97AE" {O()}/>',"-23 -20 46 46")
# porch decorating
CI["ui_deco_slot"]=(f'<circle r="20" fill="{P["cream"]}" opacity=".25" stroke="{P["cream"]}" stroke-width="3" stroke-dasharray="6 5"/><path d="M-6 0 h12 M0 -6 v12" stroke="{P["cream"]}" stroke-width="3" stroke-linecap="round"/>',"-24 -24 48 48")
CI["ui_deco_slot_valid"]=(f'<circle r="20" fill="{P["teal"]}" opacity=".35" stroke="{P["tdark"]}" stroke-width="4"/>',"-24 -24 48 48")
CI["ui_drag_ghost_shadow"]=(f'<ellipse rx="22" ry="7" fill="{P["ink"]}" opacity=".3"/>',"-24 -9 48 18")
CI["ui_contest_ribbon"]=(f'<path d="M-8 6 l-8 26 l8 -5 l6 7 l2 -28z M8 6 l8 26 l-8 -5 l-6 7 l-2 -28z" fill="{P["berry"]}" {O(2)}/><circle r="16" fill="{P["candle"]}" {O()}/><circle r="9" fill="{P["pumpkin"]}" {O(2)}/>',"-20 -20 40 58")
CI["ui_judge_meter"]=(f'<rect x="-60" y="-10" width="120" height="20" rx="10" fill="{P["pmid"]}" {O()}/><rect x="-56" y="-6" width="70" height="12" rx="6" fill="{P["candle"]}"/>'+"".join(f'<path transform="translate({x},-24) scale(.6)" d="M0 -20 L6 -6 L20 -6 L9 3 L13 18 L0 9 L-13 18 L-9 3 L-20 -6 L-6 -6z" fill="{P["candle"]}" {O(6)}/>' for x in (-40,0,40)),"-66 -40 132 54")
for n,(bdy,vb) in CI.items(): part(n,bdy,vb)

# ---- trick-or-treaters challenge (lost kid finds group): minimal extras
def kid(c,hat=""): return (f'<g {O()}><rect x="-8" y="8" width="16" height="14" rx="4" fill="#3A3F5C"/><path d="M-11 -10 h22 l2 20 h-26z" fill="{c}"/><circle cy="-20" r="11" fill="{P["skin"]}"/></g><circle cx="-4" cy="-21" r="1.8" fill="{P["ink"]}"/><circle cx="4" cy="-21" r="1.8" fill="{P["ink"]}"/>{hat}')
smile='<path d="M-4 -15 q4 4 8 0" fill="none" stroke="#1A0F2B" stroke-width="2" stroke-linecap="round"/>'.replace("#1A0F2B",P["ink"])
sad=f'<path d="M-4 -13 q4 -4 8 0" fill="none" {O(2)}/><path d="M7 -18 q2 4 0 6" fill="none" stroke="{P["teal"]}" stroke-width="2.5"/>'
HAT=dict(witch=f'<path d="M-14 -27 h28 L4 -50 l-10 6z" fill="{P["plight"]}" {O(2)}/>',pumpkin=f'<path d="M-11 -28 q11 -12 22 0z" fill="{P["pumpkin"]}" {O(2)}/>',bat=f'<g transform="translate(0,-33) scale(.5)">{parts["bat"]}</g>')
part("tot_lost_kid_sad",kid(P["teal"],HAT["witch"])+sad,"-18 -54 36 80")
part("tot_lost_kid_happy",kid(P["teal"],HAT["witch"])+smile+f'<path d="M-11 -6 l-8 -12 M11 -6 l8 -12" {O(4)}/>',"-22 -54 44 80")
part("tot_group_waiting",f'<g transform="translate(-26,0)">{kid(P["berry"],HAT["pumpkin"])}{smile}</g><g transform="translate(0,-2)">{kid(P["candle"],HAT["bat"])}{smile}</g><g transform="translate(26,0)">{kid(P["pumpkin"],"")}{smile}</g>',"-44 -50 88 76")
part("tot_candy_handout_target",f'<circle r="22" fill="{P["candle"]}" opacity=".35" stroke="{P["candle"]}" stroke-width="3"/><g transform="scale(.8)">{parts["x_candy_wrapped_1"] if "x_candy_wrapped_1" in parts else ""}<path d="M-18 -6 l8 6 l-8 6z M18 -6 l-8 6 l8 6z" fill="{P["berry"]}" {O(2)}/><ellipse rx="11" ry="8" fill="{P["berry"]}" {O()}/></g>',"-26 -26 52 52")
part("tot_reunite_hearts","".join(f'<path transform="translate({x},{y}) scale({s})" d="M0 6 q-12 -8 -8 -14 q4 -6 8 0 q4 -6 8 0 q4 6 -8 14z" fill="{P["berry"]}" {O(2)}/>' for x,y,s in ((-14,0,1.2),(10,-10,1),(16,10,.8))),"-30 -24 58 44")
# ---- dog tap-to-pet stop (M1)
def dogf(tail,mouth):
    return (f'<g {O()}><ellipse cx="0" cy="0" rx="26" ry="15" fill="{P["dog"]}"/><path d="M-20 8 v12 M-8 10 v12 M10 10 v12 M20 8 v12"/>'
      f'<path d="M24 -6 q{8+tail} -14 {tail} -24" fill="none" stroke-width="4"/><circle cx="-28" cy="-12" r="14" fill="{P["dog"]}"/>'
      f'<path d="M-38 -22 q-8 6 -4 16 q6 -2 6 -12z" fill="#E8DCCB"/></g><circle cx="-31" cy="-15" r="2.2" fill="{P["ink"]}"/><circle cx="-42" cy="-6" r="3" fill="{P["ink"]}"/>'
      +(f'<path d="M-40 0 q6 10 12 0z" fill="{P["berry"]}" {O(2)}/>' if mouth else f'<path d="M-36 2 q2 6 6 2" fill="{P["berry"]}" {O(1.5)}/>')
      +(f'<path d="M-58 -12 q-6 9 0 18 M-66 -17 q-9 14 0 28" fill="none" {O(3)}/>' if mouth else ""))
for i,(t,mo) in enumerate(((-6,False),(14,True),(-14,True))): part(f"dog_bark_{i+1}",dogf(t,mo),"-74 -42 114 72")
def owner(arms):
    a=(f'<path d="M-13 -40 q-6 14 -2 22 M13 -40 q6 14 2 22" fill="none" stroke="#C77B9E" stroke-width="7" stroke-linecap="round"/>' if arms=="hold" else f'<path d="M-13 -40 q-6 12 -16 16 M13 -40 q-8 16 -22 18" fill="none" stroke="#C77B9E" stroke-width="7" stroke-linecap="round"/>')
    cy=-20 if arms=="hold" else -22; cx=0 if arms=="hold" else -26
    cake_=f'<g transform="translate({cx-27},{cy-24})">{cake(54,45)}</g>'
    return (f'<g {O()}><rect x="-10" y="-8" width="9" height="22" rx="4" fill="#3A3F5C"/><rect x="1" y="-8" width="9" height="22" rx="4" fill="#3A3F5C"/></g><g transform="translate(0,-2)">{parts["npc_dog_owner_torso"]}</g>'
      f'<circle cx="0" cy="-60" r="13" fill="{P["skin"]}" {O()}/>{parts["npc_dog_owner_hair"]}<circle cx="-5" cy="-60" r="1.8" fill="{P["ink"]}"/><circle cx="5" cy="-60" r="1.8" fill="{P["ink"]}"/><path d="M-4 -53 q4 4 8 0" fill="none" {O(2)}/>{cake_}{a}')
part("npc_dog_owner_hold_cake",owner("hold"),"-36 -86 72 104")
part("npc_dog_owner_handover",owner("give"),"-40 -86 80 104")
part("fx_pet_heart",f'<path d="M0 14 q-22 -14 -14 -26 q7 -9 14 0 q7 -9 14 0 q8 12 -14 26z" fill="{P["berry"]}" {O()}/><circle cx="-6" cy="-6" r="3" fill="#FFFFFF" opacity=".8"/>'+"".join(f'<path d="M{x} {y} l2.5 -6 l2.5 6 l6 2.5 l-6 2.5 l-2.5 6 l-2.5 -6 l-6 -2.5z" fill="{P["candle"]}" {O(1.5)}/>' for x,y in ((-26,-18),(22,-20),(24,10))),"-36 -32 72 52")
part("ui_pet_hand_hint",f'<g transform="rotate(-20)"><rect x="-10" y="-4" width="20" height="22" rx="8" fill="{P["skin"]}" {O()}/>'+"".join(f'<rect x="{x}" y="-18" width="5" height="16" rx="2.5" fill="{P["skin"]}" {O(2)}/>' for x in (-10,-4,2,8))+'</g>',"-22 -26 44 50")

