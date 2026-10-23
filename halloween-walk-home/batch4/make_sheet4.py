from PIL import Image,ImageDraw
import json
m=json.load(open("batch4_3d.json"))["pieces"]; names=list(m)
A=Image.new("RGBA",(2048,512),(0,0,0,0)); fr={}
S=Image.new("RGB",(2048,620),(237,230,245)); d=ImageDraw.Draw(S)
d.text((20,15),"Halloween Walk Home: Batch 4 3D Open Kit (4 low-poly glTF), CC0",fill=(36,26,46))
for i,n in enumerate(names):
    im=Image.open(f"preview_{n}.png").convert("RGBA"); A.paste(im,(i*512,0)); fr[n]=dict(frame=dict(x=i*512,y=0,w=512,h=512),scale=2,glb=m[n]["file"])
    d.rounded_rectangle((i*512+8,50,i*512+504,600),12,fill="white",outline=(201,190,219)); S.paste(im,(i*512,60),im)
    d.text((i*512+20,570),f'{n}  {m[n]["tris"]} tris  {"x".join(str(v) for v in m[n]["size_m"])} m  slots: {",".join(m[n]["colour_slots"])}',fill=(36,26,46))
A.save("../atlas/batch4_previews@2x.png"); json.dump(dict(frames=fr,meta=dict(image="batch4_previews@2x.png",size=dict(w=2048,h=512),scale=2,license="CC0")),open("../atlas/batch4_previews@2x.json","w"),indent=1)
S.save("contact_sheet.png")
