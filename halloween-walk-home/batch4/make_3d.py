# Batch 4: low-poly 3D Open Kit pieces. Original work, CC0. Units: metres. <=3 colour slots per mesh, tri cap 1500, simple collider.
import bpy,bmesh,math,json,os
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__)); TRI_CAP=1500
def hexc(h): h=h.lstrip('#'); return tuple((int(h[i:i+2],16)/255)**2.2 for i in (0,2,4))+(1,)
PAL=dict(pumpkin="#F28C28",stem="#5E8C3A",candle="#FFD36B",ink="#241A2E",purple="#3B2557",stone="#B9B4C8",grass="#7FBF6A",wood="#C98B55",straw="#E8C07A",cloth="#5FC9C3")
def mat(n):
    m=bpy.data.materials.get(n) or bpy.data.materials.new(n); m.use_nodes=True
    b=m.node_tree.nodes["Principled BSDF"]; b.inputs["Base Color"].default_value=hexc(PAL[n]); b.inputs["Roughness"].default_value=.8
    if n=="candle": b.inputs["Emission Color"].default_value=hexc(PAL[n]); b.inputs["Emission Strength"].default_value=2
    m.diffuse_color=hexc(PAL[n]); return m
def reset(): bpy.ops.wm.read_factory_settings(use_empty=True)
def setmat(o,m):
    o.data.materials.clear(); o.data.materials.append(m)
def join(objs,name):
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active=objs[0]; bpy.ops.object.join(); o=bpy.context.object; o.name=name; o.data.name=name
    bpy.ops.object.transform_apply(location=False,rotation=True,scale=True); return o
def collider(o,kind):
    d=o.dimensions; c=sum((o.matrix_world@Vector(v) for v in o.bound_box),Vector())/8
    if kind=="box": bpy.ops.mesh.primitive_cube_add(location=c); col=bpy.context.object; col.scale=(d.x/2,d.y/2,d.z/2)
    else: bpy.ops.mesh.primitive_cylinder_add(vertices=8,radius=max(d.x,d.y)/2,depth=d.z,location=c); col=bpy.context.object
    bpy.ops.object.transform_apply(scale=True); col.name=o.name+"_collider"; col["collider"]=kind; col.display_type='WIRE'; col.hide_render=True; col.parent=o; return col
def tris(o): return sum(len(p.vertices)-2 for p in o.data.polygons)
def shade_flat(o):
    for p in o.data.polygons: p.use_smooth=False
def sphere(r,seg,ring,loc,scale=(1,1,1),m=None):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=ring,radius=r,location=loc); o=bpy.context.object; o.scale=scale; setmat(o,m); return o
def cyl(r,d,v,loc,rot=(0,0,0),m=None,r2=None):
    if r2 is None: bpy.ops.mesh.primitive_cylinder_add(vertices=v,radius=r,depth=d,location=loc,rotation=rot)
    else: bpy.ops.mesh.primitive_cone_add(vertices=v,radius1=r,radius2=r2,depth=d,location=loc,rotation=rot)
    o=bpy.context.object; setmat(o,m); return o
def cube(sz,loc,m,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot); o=bpy.context.object; o.scale=(sz[0]/2,sz[1]/2,sz[2]/2); setmat(o,m); return o
def pumpkin():
    P,S,C=mat("pumpkin"),mat("stem"),mat("candle")
    body=sphere(.2,24,12,(0,0,.17),(1,1,.82),P)
    # ribs: push alternate vertical rings inward
    for v in body.data.vertices:
        a=math.atan2(v.co.y,v.co.x); k=1-.06*(0.5+0.5*math.cos(a*8)); v.co.x*=k; v.co.y*=k
    # cut the face out of the shell: solidify into a 2 cm shell, boolean-subtract cutters, glowing core inside
    bpy.context.view_layer.objects.active=body; m=body.modifiers.new("shell","SOLIDIFY"); m.thickness=.02; bpy.ops.object.modifier_apply(modifier="shell")
    cutters=[cyl(.045,.2,3,(x,-.17,.22),(math.pi/2,math.pi/2,0),C) for x in (-.07,.07)]
    bpy.ops.mesh.primitive_cube_add(location=(0,-.17,.12)); mo=bpy.context.object; mo.scale=(.08,.1,.022); bpy.ops.object.transform_apply(scale=True); cutters.append(mo)
    for c in cutters:
        bm=body.modifiers.new("cut","BOOLEAN"); bm.operation='DIFFERENCE'; bm.object=c; bm.solver='EXACT'; bm.material_mode='INDEX'
        bpy.context.view_layer.objects.active=body; bpy.ops.object.modifier_apply(modifier=bm.name); bpy.data.objects.remove(c)
    core=sphere(.15,10,6,(0,0,.17),(1,1,.8),C)
    stem=cyl(.025,.08,6,(0,0,.33),(0.15,0,0),S,.018)
    return join([body,stem,core],"hw3d_pumpkin"),"cyl"
def lantern():
    I,C,Pp=mat("ink"),mat("candle"),mat("purple")
    base=cube((.18,.18,.03),(0,0,.015),I); top=cyl(.13,.06,4,(0,0,.32),(0,0,math.pi/4),I,.03)
    glass=cube((.14,.14,.24),(0,0,.16),C)
    posts=[cube((.02,.02,.26),(x,y,.16),I) for x in (-.075,.075) for y in (-.075,.075)]
    ring=cyl(.03,.008,8,(0,0,.38),(math.pi/2,0,0),Pp); bpy.ops.object.modifier_add(type='SOLIDIFY')
    return join([base,top,glass,ring]+posts,"hw3d_lantern"),"box"
def gravestone():
    St,G,I=mat("stone"),mat("grass"),mat("ink")
    slab=cube((.4,.1,.45),(0,0,.25),St); cap=cyl(.2,.1,10,(0,0,.475),(math.pi/2,0,0),St)
    for v in cap.data.vertices: pass
    mound=sphere(.32,10,4,(0,.05,0),(1,.6,.25),G)
    eyes=[cube((.04,.02,.05),(x,-.055,.36),I) for x in (-.07,.07)]
    smile=cube((.12,.02,.025),(0,-.055,.28),I)
    return join([slab,cap,mound,smile]+eyes,"hw3d_gravestone"),"box"
def scarecrow():
    W,Sw,Cl=mat("wood"),mat("straw"),mat("cloth")
    post=cube((.07,.07,1.6),(0,0,.8),W); arm=cube((1.0,.06,.06),(0,0,1.25),W)
    head=sphere(.15,10,6,(0,0,1.55),(1,1,1.05),Sw)
    hat_b=cyl(.24,.03,10,(0,0,1.68),m=W); hat_t=cyl(.12,.18,10,(0,0,1.78),m=W,r2=.08)
    shirt=cube((.42,.2,.45),(0,0,1.12),Cl); sleeves=cube((.8,.14,.14),(0,0,1.25),Cl)
    straw=[cyl(.04,.12,4,(x,0,1.25),(0,math.pi/2,0),Sw,.0) for x in (-.47,.47)]+[cyl(.06,.14,5,(0,0,.86),(math.pi,0,0),Sw,.0)]
    return join([post,arm,head,hat_b,hat_t,shirt,sleeves]+straw,"hw3d_scarecrow"),"box"
meta={}
for fn in (pumpkin,lantern,gravestone,scarecrow):
    reset(); o,ck=fn()
    for m in o.modifiers: bpy.ops.object.modifier_apply(modifier=m.name)
    shade_flat(o); bpy.context.view_layer.objects.active=o; bpy.ops.object.material_slot_remove_unused()
    # put origin at base centre, base on z=0
    bpy.context.scene.cursor.location=(0,0,0); bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    zmin=min((o.matrix_world@Vector(v)).z for v in o.bound_box); o.location.z-=zmin; bpy.ops.object.transform_apply(location=True)
    col=collider(o,ck); t=tris(o); slots=len(o.data.materials)
    assert t<=TRI_CAP and slots<=3,(o.name,t,slots)
    bpy.ops.object.select_all(action='DESELECT'); o.select_set(True); col.select_set(True)
    bpy.ops.export_scene.gltf(filepath=f"{OUT}/{o.name}.glb",export_format='GLB',use_selection=True,export_extras=True,export_apply=True)
    # preview render (workbench, flat colour)
    sc=bpy.context.scene; sc.render.engine='BLENDER_WORKBENCH'; sc.display.shading.light='STUDIO'; sc.display.shading.color_type='MATERIAL'
    sc.display.shading.show_object_outline=True; sc.display.shading.object_outline_color=hexc(PAL["ink"])[:3]
    sc.render.resolution_x=sc.render.resolution_y=512; sc.render.film_transparent=True; col.hide_set(True)
    h=o.dimensions.z; r=max(o.dimensions)*1.9
    bpy.ops.object.camera_add(location=(r*.55,-r*.85,h*.5+r*.55)); cam=bpy.context.object; sc.camera=cam
    d=Vector((0,0,h*.45))-cam.location; cam.rotation_euler=d.to_track_quat('-Z','Y').to_euler(); cam.data.type='ORTHO'; cam.data.ortho_scale=max(o.dimensions)*1.5
    sc.render.filepath=f"{OUT}/preview_{o.name}.png"; bpy.ops.render.render(write_still=True)
    meta[o.name]=dict(file=f"{o.name}.glb",tris=t,colour_slots=[m.name for m in o.data.materials],size_m=[round(v,3) for v in o.dimensions],collider=ck,origin="base centre, +Z up (glTF +Y up)")
json.dump(dict(pieces=meta,units="metres",tri_cap=TRI_CAP,max_colour_slots=3,license="CC0, all original"),open(f"{OUT}/batch4_3d.json","w"),indent=1)
print("DONE",json.dumps(meta))
