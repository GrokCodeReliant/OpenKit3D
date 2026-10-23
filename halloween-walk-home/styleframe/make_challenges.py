# Composite each challenge screen: background + its interactive pieces (layout mock for Art (UI)/engine).
def load(n):
    t=open(f"parts/{n}.svg").read(); return t.split('viewBox="')[1].split('"')[0].split(), t.split('>',1)[1].rsplit('</svg>',1)[0]
def put(n,cx,cy,s=1.0):
    vb,b=load(n); x,y,w,h=map(float,vb); return f'<svg x="{cx+x*s}" y="{cy+y*s}" width="{w*s}" height="{h*s}" viewBox="{" ".join(vb)}">{b}</svg>'
def bg(n): vb,b=load(n); return b
S={}
S["challenge_clue_board"]=[bg("challenge_clue_board"),put("ui_clue_card_witch_hat",125,245,1.45),put("ui_clue_card_pumpkin",265,255,1.45),put("ui_clue_card_back",135,395,1.45),put("ui_clue_card_house",260,405,1.45),
  put("ui_clue_pin",125,205,1.2),put("ui_clue_pin",265,215,1.2),put("ui_clue_match_check",300,220,1.1),put("ui_clue_card_bat",195,690,1.6),put("fx_tap_me_pulse",195,690,1.25),put("tot_lost_kid_sad",70,690,1.6),put("tot_group_waiting",320,700,1.3)]
dots="".join(put("ui_trace_dot_done" if k<3 else "ui_trace_dot",x,y,1.0) for k,(x,y) in enumerate(((140,358),(155,336),(170,358),(185,380),(155,380))))
S["challenge_carving_trace"]=[bg("challenge_carving_trace"),dots,put("ui_trace_start",112,392,1.3),put("ui_trace_end",205,398,1.3),put("ui_carving_scoop",250,300,1.5),put("ui_carve_chunk",90,560,1.4),put("ui_carve_chunk",300,600,1.2),put("fx_success_sparkle",300,250,1.2)]
S["challenge_paw_prints"]=[bg("challenge_paw_prints"),put("ui_paw_print_found",40,640,1.5),put("ui_paw_print_found",84,580,1.5),put("ui_paw_print_found",128,540,1.5),put("ui_hide_bush",90,200,1.8),put("ui_hide_box",200,480,1.6),put("ui_hide_trash_can",330,520,1.6),put("ui_hide_bush_peek",300,175,2.0),put("fx_tap_me_pulse",300,130,1.5)]
S["challenge_porch_decor"]=[bg("challenge_porch_decor"),put("ui_deco_slot",195,600,1.4),put("ui_deco_slot_valid",320,600,1.4),put("ui_deco_slot",70,600,1.4),put("deco_paper_lantern",320,600,1.2),put("ui_drag_ghost_shadow",150,420,1.2),put("deco_wreath",150,385,1.3),
  put("ui_judge_meter",195,90,1.6),put("ui_contest_ribbon",340,160,1.3)]+[put(n,46+i*62,768,.85) for i,n in enumerate(["deco_bat_garland","deco_paper_lantern","deco_spider_toy","deco_wreath","deco_scarecrow_mini","deco_candy_bowl"])]
S["stop_trick_or_treat_door"]=[f'<rect width="390" height="844" fill="#7FBF6A"/><rect y="560" width="390" height="120" fill="#D9D2C3" stroke="#241A2E" stroke-width="3"/>',put("porch_a" if False else "home_exterior",60,120,1.2) if False else f'<svg x="30" y="180" width="330" height="336" viewBox="0 0 270 275">{bg("home_exterior")}</svg>',
  put("tot_group_waiting",195,600,1.8),put("tot_candy_handout_target",120,520,1.4),put("tot_candy_handout_target",270,520,1.4),put("fx_tap_me_pulse",120,520,.9),put("tot_lost_kid_happy",330,720,1.5),put("tot_reunite_hearts",330,630,1.2),put("fx_night_tint",0,0,1) if False else ""]
S["stop_dog_pet"]=[f'<rect width="390" height="844" fill="#7FBF6A"/><rect y="520" width="390" height="120" fill="#D9D2C3" stroke="#241A2E" stroke-width="3"/>',f'<svg x="30" y="140" width="330" height="336" viewBox="0 0 270 275">{bg("home_exterior")}</svg>',
  put("npc_dog_owner_handover",250,560,2.0),put("dog_bark_2",130,600,1.8),put("fx_pet_heart",120,510,1.4),put("ui_pet_hand_hint",160,560,1.2),put("fx_tap_me_pulse",130,590,1.6),
  put("dog_bark_1",70,760,1.0),put("dog_bark_3",190,760,1.0),put("npc_dog_owner_hold_cake",320,780,1.0)]
import os; os.makedirs("../challenges",exist_ok=True)
for n,parts_ in S.items(): open(f"../challenges/{n}_composite.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="780" height="1688" viewBox="0 0 390 844">{"".join(parts_)}</svg>')
