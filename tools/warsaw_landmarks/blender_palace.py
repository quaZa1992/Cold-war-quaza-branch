# IMPERIA CW — Cold War: warsaw landmarks — blender palace.
"""Native Blender PKiN: period massing, ornamental silhouette, panel facades."""
from pathlib import Path
import hashlib
import json
import math
import sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/berlin_landmarks'))
import blender_landmarks as shared
from pdx import read,meshes
CFG=json.loads((HERE/'config.json').read_text())
OUT=ROOT/'gfx/models/buildings/landmarks'
PREFIX='mdcw_warsaw_palace'
shared.OUT=OUT


def material():
    mat=shared.material();mat.name='PKiN aged sandstone ceramic and bronze'
    for node in mat.node_tree.nodes:
        if node.type=='TEX_IMAGE' and node.image:
            for kind in ['diffuse','normal','specular']:
                if kind in node.image.name:
                    node.image=bpy.data.images.load(str(OUT/f'{PREFIX}_{kind}.dds'),check_existing=True)
                    node.image.alpha_mode='CHANNEL_PACKED'
                    node.image.colorspace_settings.name='sRGB' if kind=='diffuse' else 'Non-Color'
    return mat


def block(name,center,size,mat,tile=0,facade=None,panel_width=65,roof=None):
    cx,cy,cz=center;dx,dy,dz=[v/2 for v in size]
    vertices=[];faces=[];uvs=[]
    def face(points,t):
        n=len(vertices);vertices.extend(points);faces.append(tuple(range(n,n+len(points))))
        uvs.append([shared.uv_tile(t,u,v) for u,v in [(0,1),(1,1),(1,0),(0,0)]])
    # Undersides are buried in the ground or other masses and are not exported.
    face([(cx-dx,cy-dy,cz+dz),(cx+dx,cy-dy,cz+dz),(cx+dx,cy+dy,cz+dz),(cx-dx,cy+dy,cz+dz)],roof if roof is not None else (3 if facade is not None else tile))
    for axis,length,fixed,sign in [(1,size[1],cx+dx,1),(1,size[1],cx-dx,-1),(0,size[0],cy+dy,-1),(0,size[0],cy-dy,1)]:
        count=max(1,math.ceil(length/panel_width)) if facade is not None else 1
        start=cy-dy if axis==1 else cx-dx
        for col in range(count):
            a=start+length*col/count;b=start+length*(col+1)/count;z0=cz-dz;z1=cz+dz
            q=[(fixed,a,z0),(fixed,b,z0),(fixed,b,z1),(fixed,a,z1)] if axis==1 else [(a,fixed,z0),(b,fixed,z0),(b,fixed,z1),(a,fixed,z1)]
            if sign<0:q=[q[1],q[0],q[3],q[2]]
            face(q,facade if facade is not None else tile)
    return shared.mesh_object(name,vertices,faces,uvs,mat)


def cornice(name,center,width,depth,mat):
    x,y,z=center
    block(name+' shadow course',(x,y,z-.7),(width-.6,depth-.6,.7),mat,11,roof=3)
    # Perimeter coping leaves the dark recessed roof visible inside the parapet.
    for side in [-1,1]:
        block(name+' coping Y',(x,y+side*(depth-.9)/2,z),(width,.9,.8),mat,4)
        block(name+' coping X',(x+side*(width-.9)/2,y,z),(.9,depth-1.8,.8),mat,4)


def pyramid(name,base,size,height,mat,tile=3,top=.12):
    x,y,z=base;w,d=size
    p=[(x-w/2,y-d/2,z),(x+w/2,y-d/2,z),(x+w/2,y+d/2,z),(x-w/2,y+d/2,z),
       (x-top/2,y-top/2,z+height),(x+top/2,y-top/2,z+height),(x+top/2,y+top/2,z+height),(x-top/2,y+top/2,z+height)]
    f=[(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)]
    uv=[[shared.uv_tile(tile,u,v) for u,v in [(0,1),(1,1),(1,0),(0,0)]] for _ in f]
    return shared.mesh_object(name,p,f,uv,mat)


def attic(name,center,width,depth,mat,height=3.2,pinnacles=2.5):
    x,y,z=center
    # A continuous relief band replaces the rows of detached castle-like beads.
    block(name+' Renaissance frieze',(x,y,z+height/2),(width,depth,height),mat,facade=14,roof=3)
    cornice(name+' upper moulding',(x,y,z+height),width+.8,depth+.8,mat)
    for a in [-1,1]:
        for b in [-1,1]:
            cx=x+a*(width/2-.8);cy=y+b*(depth/2-.8)
            block(name+' corner pedestal',(cx,cy,z+height+.65),(2.5,2.5,1.3),mat,4)
            pyramid(name+' slender finial',(cx,cy,z+height+1.3),(1.8,1.8),pinnacles,mat,4)
    # Sparse intermediate curved/gabled ornaments, only on the outer silhouette.
    if width>40:
        for v in [-width*.25,0,width*.25]:
            for b in [-1,1]:
                pyramid(name+' gable',(x+v,y+b*(depth/2-.5),z+height+.4),(2.1,1.2),1.7,mat,4)


def piers(name,center,width,depth,height,mat,count=6,thickness=1.45):
    x,y,z=center
    for a in [-1,1]:
        for i in range(1,count-1):
            t=-.5+i/(count-1)
            block(name+' vertical stone pier X',(x+a*(width/2+.15),y+t*depth,z),(thickness,thickness,height),mat,4)
            block(name+' vertical stone pier Y',(x+t*width,y+a*(depth/2+.15),z),(thickness,thickness,height),mat,4)
    for a in [-1,1]:
        for b in [-1,1]:
            block(name+' corner stone pier',(x+a*width/2,y+b*depth/2,z),(thickness+.3,thickness+.3,height),mat,4)


def portico(name,x,y,z,width,depth,height,mat,facing='east'):
    # Monumental square columns and deep, shaded lintel; no tiny window geometry.
    if facing=='east':
        block(name+' entrance recess',(x+.1,y,z+height/2),(1,width,height),mat,facade=13)
        cornice(name+' entablature',(x+depth/2,y,z+height+1.4),depth+2,width+3,mat)
        for i in range(6):
            yy=y-width*.44+width*.88*i/5
            block(name+' column',(x+depth,yy,z+height/2),(2.0,2.0,height),mat,4)
            block(name+' capital',(x+depth,yy,z+height-.1),(2.7,2.7,.9),mat,4)
        for i in range(3):
            step_top=z-.725+i*.3
            step_height=step_top if i==0 else .35
            block(name+' step',(x+depth/2+1,y,step_top-step_height/2),(depth+6-i,width+5-i,step_height),mat,8)
    else:
        block(name+' entrance recess',(x,y-.5,z+height/2),(width,1,height),mat,facade=13)
        cornice(name+' entablature',(x,y-depth/2,z+height+1.4),width+3,depth+2,mat)
        for i in range(6):
            xx=x-width*.44+width*.88*i/5
            block(name+' column',(xx,y-depth,(z+height)/2),(2,2,z+height),mat,4)
            block(name+' capital',(xx,y-depth,z+height-.1),(2.7,2.7,.9),mat,4)


def congress_hall(mat):
    profile=[(0,39.5),(3,40),(4,40),(4.2,38.8),(20.5,38.8),(21,39.8),(24,39.8),(25,38.5),(28,38.5)]
    obj=shared.lathe('03 west Congress Hall drum',profile,mat,[8,4,4,10,4,14,4,0],32,False)
    # Eight facade panels around the drum give 48 tall bays on 32 simple sides.
    uv=obj.data.uv_layers.active.data
    for polygon in obj.data.polygons:
        band=polygon.index//32;j=polygon.index%32
        if band==3:
            coords=[shared.uv_tile(10,u,v) for u,v in [((j%4)/4,1),((j%4+1)/4,1),((j%4+1)/4,0),((j%4)/4,0)]]
            for loop,coord in zip(polygon.loop_indices,coords):uv[loop].uv=coord
    roof=shared.lathe('03 Congress Hall shallow copper dome',[(28,38.7),(30,37.8),(33,33.2),(35.6,25),(37,13),(37.5,.4)],mat,3,32,True)
    for part in [o for o in bpy.context.scene.objects if o.name.startswith('03 ')]:part.location.x=-70


def build(mat):
    # No enclosing ground slab: the existing foundations meet the map terrain.
    for x in [-57,57]:
        for y in [-87,87]:
            block(f'02 rusticated wing base {x} {y}',(x,y,4.375),(51,70,8.75),mat,facade=13)
            block(f'02 pavilion facade {x} {y}',(x,y,17.7),(51,70,18),mat,facade=9)
            cornice('02 wing string course',(x,y,9),51.5,70.5,mat)
            attic('02 pavilion attic',(x,y,27),51,70,mat,2.5,1.8)
            # A few low roof housings break the otherwise perfectly empty roofs.
            block('02 recessed roof housing',(x-8,y,30.2),(16,25,1.8),mat,11,roof=3)
    for x in [-62,62]:
        block('02 long low connecting range',(x,0,12.25),(30,104,24.5),mat,facade=9)
        cornice('02 connector coping',(x,0,25),31,104,mat)
    for y in [-104.5,104.5]:
        block('02 low cross range',(0,y,12.25),(63,35,24.5),mat,facade=9)
        cornice('02 cross range coping',(0,y,25),63,36,mat)
    congress_hall(mat)
    block('04 central entrance plinth',(0,0,18.25),(86,86,36.5),mat,facade=13)
    cornice('04 podium cornice',(0,0,37),88,88,mat)
    # Four intermediate shoulders, each capped by a substantial carved attic.
    for x in [-33,33]:
        for y in [-33,33]:
            block('05 shoulder',(x,y,52),(25,25,31),mat,facade=2)
            piers('05 shoulder',(x,y,52),25,25,31,mat,6,1.05)
            attic('05 shoulder attic',(x,y,67.5),26,26,mat,3.0,3.2)
    block('06 main shaft',(0,0,75.5),(47,47,77),mat,facade=1)
    piers('06 main shaft',(0,0,76),47,47,75,mat,8,1.45)
    # The 114 m observation gallery hugs the shaft; no oversized canopy plates.
    cornice('07 observation ledge',(0,0,114),51,51,mat)
    block('07 recessed high gallery',(0,0,118.2),(46,46,7.5),mat,facade=10)
    piers('07 gallery',(0,0,118.2),47,47,7.5,mat,7,1.1)
    attic('07 principal Renaissance crown',(0,0,122),49,49,mat,4.0,4.0)
    # Narrower upper stages and a blank period field where the later clock sits.
    block('08 upper tower',(0,0,140.5),(31,31,29),mat,facade=15)
    piers('08 upper tower',(0,0,140.5),31,31,29,mat,6,.95)
    attic('08 upper attic',(0,0,155),34,34,mat,2.3,2.1)
    block('09 clockless crown',(0,0,166.5),(22,22,19),mat,facade=12)
    for x in [-10.5,10.5]:
        for y in [-10.5,10.5]:block('09 crown corner pilaster',(x,y,166.5),(1.6,1.6,19),mat,4)
    cornice('09 terminal roof cornice',(0,0,176.4),24,24,mat)
    pyramid('10 steep dark pavilion roof',(0,0,176.8),(22,22),8.8,mat,3,top=4.0)
    shared.lathe('10 restrained bronze bulb',[(185.6,2),(186.3,2.7),(187.1,2.3),(187.68,1.45)],mat,5,16,True)
    shared.lathe('11 original continuous needle',[(187.68,1.45),(194,1.25),(202,1.0),(212,.72),(221,.43),(228,.18),(230.68,.035)],mat,6,12,True)
    portico('12 east main entrance',43,0,2.7,38,12,22,mat)
    for y in [-87,87]:portico('12 east pavilion entrance',82.5,y,2.2,32,8,14,mat)
    for x in [-57,57]:portico('12 south pavilion entrance',x,-122,2.2,30,5,14,mat,'south')
    return [obj for obj in bpy.context.scene.objects if obj.type=='MESH']


def main():
    bpy.context.preferences.filepaths.save_version=0
    shared.clear_scene();mat=material();objects=build(mat);bie=shared.exporter()
    for suffix in ['', '_destroyed']:shared.export_objects(objects,'landmark_warsaw_palace'+suffix+'.mesh','mdcw_warsaw_palace',bie)
    shared.camera_and_light((0,0,95),(440,-620,345),345,1400)
    scene=bpy.context.scene;scene.render.resolution_x=1400;scene.render.resolution_y=1250
    scene.view_settings.exposure=-.35
    for image in bpy.data.images:
        if image.source=='FILE' and image.filepath:
            try:image.pack()
            except RuntimeError:pass
    source=HERE/'source/warsaw_palace.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source))
    scene.render.filepath=str(HERE/'previews/palace_blender.png');bpy.ops.render.render(write_still=True)
    # Rear view verifies the round Congress Hall rather than hiding it in the hero shot.
    camera=scene.camera;camera.location=(-470,-590,340)
    camera.rotation_euler=(Vector((0,0,95))-camera.location).to_track_quat('-Z','Y').to_euler()
    scene.render.filepath=str(HERE/'previews/palace_west.png');bpy.ops.render.render(write_still=True)
    camera.location=(440,-620,345);camera.rotation_euler=(Vector((0,0,95))-camera.location).to_track_quat('-Z','Y').to_euler()
    bpy.data.objects['Presentation ground (not exported)'].hide_render=True
    scene.render.film_transparent=True;scene.render.resolution_x=384;scene.render.resolution_y=384;scene.cycles.samples=16
    scene.render.filepath=str(HERE/'previews/palace_icon.png');bpy.ops.render.render(write_still=True)
    mesh=next(meshes(read(OUT/'landmark_warsaw_palace.mesh')))[1]
    before={'triangles':16144,'vertices':33545}
    report={'blender_version':bpy.app.version_string,'exporter':'io_pdx_mesh 0.91','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'source':str(source.relative_to(HERE)),'height':CFG['original_height'],'scale':CFG['scale'],'display_height':CFG['original_height']*CFG['scale'],
            'mesh_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('landmark_warsaw_palace*.mesh')},
            'performance':{'vertices':len(mesh.prop('p').value)//3,'triangles':len(mesh.prop('tri').value)//3,'material_count':1,
                           'previous_triangles':before['triangles'],'previous_vertices':before['vertices'],'atlas_size':1024,'atlas_mip_levels':11}}
    (HERE/'blender_export.json').write_text(json.dumps(report,indent=2)+'\n')
    print('WARSAW_PALACE_BLENDER_COMPLETE',report['performance'])


if __name__=='__main__':main()
