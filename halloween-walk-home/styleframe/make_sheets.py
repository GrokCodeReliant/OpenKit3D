import html,sys
def load(n):
    t=open(f"parts/{n}.svg").read(); return t.split('viewBox="')[1].split('"')[0], t.split('>',1)[1].rsplit('</svg>',1)[0]
for tag,title in (("batch1_parts","Batch 1"),("batch2_parts","Batch 2: story + challenges"),("batch3_parts","Batch 3: extras galore")):
    names=open(f"../atlas/{tag}.list").read().split("\n"); cols,cw,ch=8,240,260; rows=(len(names)+cols-1)//cols
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{cols*cw}" height="{rows*ch+60}"><rect width="100%" height="100%" fill="#EDE6F5"/><text x="20" y="40" font-family="sans-serif" font-size="28" font-weight="bold" fill="#241A2E">Halloween Walk Home: {title} ({len(names)} parts), CC0</text>']
    for i,n in enumerate(names):
        x,y=(i%cols)*cw,(i//cols)*ch+60; vb,b=load(n)
        o.append(f'<rect x="{x+6}" y="{y+6}" width="{cw-12}" height="{ch-12}" rx="12" fill="#fff" stroke="#C9BEDB"/><svg x="{x+16}" y="{y+14}" width="{cw-32}" height="{ch-64}" viewBox="{vb}">{b}</svg><text x="{x+cw/2}" y="{y+ch-18}" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#241A2E">{html.escape(n)}</text>')
    d=tag.split("_")[0]; import os; os.makedirs(f"../{d}",exist_ok=True)
    open(f"../{d}/contact_sheet.svg","w").write("".join(o)+"</svg>"); print(d,cols*cw,rows*ch+60)
