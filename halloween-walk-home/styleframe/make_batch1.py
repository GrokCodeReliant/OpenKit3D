import os,glob,html
names=sorted(os.path.basename(p)[:-4] for p in glob.glob("parts/*.svg"))
def load(n):
    t=open(f"parts/{n}.svg").read(); vb=t.split('viewBox="')[1].split('"')[0]; return vb,t.split('>',1)[1].rsplit('</svg>',1)[0]
cols,cw,ch=8,240,260; rows=(len(names)+cols-1)//cols
o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{cols*cw}" height="{rows*ch+60}"><rect width="100%" height="100%" fill="#EDE6F5"/><text x="20" y="40" font-family="sans-serif" font-size="28" font-weight="bold" fill="#241A2E">Halloween Walk Home: Batch 1 parts ({len(names)}), CC0</text>']
for i,n in enumerate(names):
    x,y=(i%cols)*cw,(i//cols)*ch+60; vb,b=load(n)
    o.append(f'<rect x="{x+6}" y="{y+6}" width="{cw-12}" height="{ch-12}" rx="12" fill="#fff" stroke="#C9BEDB"/><svg x="{x+16}" y="{y+14}" width="{cw-32}" height="{ch-64}" viewBox="{vb}">{b}</svg><text x="{x+cw/2}" y="{y+ch-18}" text-anchor="middle" font-family="sans-serif" font-size="15" fill="#241A2E">{html.escape(n)}</text>')
o.append('</svg>'); open("/tmp/_unused_sheet.svg","w").write("".join(o)); print(cols*cw, rows*ch+60)
# composite scene 390x694 (1x) from parts
def put(n,x,y,w,h,par=""):
    vb,b=load(n); return f'<svg x="{x}" y="{y}" width="{w}" height="{h}" viewBox="{vb}" {par}>{b}</svg>'
S=[]
S.append(put("store_front",15,5,360,250))
row=[("tile_driveway"),("tile_sidewalk_straight"),("tile_sidewalk_T"),("tile_sidewalk_straight")]
for i,t in enumerate(row): S.append(put(t,i*100-5,245,104,104))
for i in range(4): S.append(put("tile_crosswalk" if i==1 else "tile_road_lane",i*100-5,345,104,104))
for i,t in enumerate(["tile_mailbox","tile_sidewalk_straight","tile_sidewalk_straight","tile_sidewalk_straight"]): S.append(put(t,i*100-5,445,104,104))
for i,t in enumerate(["tile_hedge","tile_fence","tile_streetlight","tile_tree"]): S.append(put(t,i*100-5,545,104,104))
S.append(put("fx_night_tint",0,0,390,694,'preserveAspectRatio="none"'))
S.append(put("fx_light_pool",130,220,240,140)); S.append(put("fx_light_pool",80,90,240,180)); S.append(put("fx_light_pool",140,500,240,140))
for p,x,y in [("rig_leg",176,300),("rig_leg",188,300)]: S.append(put(p,x,y,18,28))
S.append(f'<g transform="translate(400,0) scale(-1,1)">{put("rig_arm",213,262,24,34)}</g>'+put("rig_arm",203,262,24,34)); S.append(put("rig_torso_f",175,260,40,50)); S.append(put("rig_head_s2",177,226,36,34)); S.append(put("rig_hair_curly",173,222,44,32))
S.append(put("candy_bucket_full",215,286,30,31)); S.append(put("dog",240,300,60,46)); S.append(put("fx_tap_me_pulse",232,282,76,76))
S.append(put("marker_star",80,290,32,30)); S.append(put("marker_gift",300,480,32,32)); S.append(put("jack_carved",30,500,48,50))
open("../batch1/composite_scene.svg","w").write(f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 390 694"><rect width="390" height="694" fill="#7FBF6A"/>{"".join(S)}</svg>')
