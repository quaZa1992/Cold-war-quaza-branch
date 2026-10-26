# IMPERIA CW — Cold War: bucharest landmarks — blender scinteii.
"""Native Blender authoring of the 1970 Casa Scinteii printing complex."""
from pathlib import Path
import hashlib,json,math,sys
import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/berlin_landmarks'))
sys.path.insert(0,str(ROOT/'tools/warsaw_landmarks'))
import blender_landmarks as shared
import blender_palace as detail
from pdx import read,meshes
CFG=json.loads((HERE/'config.json').read_text())
OUT=ROOT/'gfx/models/buildings/landmarks';shared.OUT=OUT
PREFIX='mdcw_bucharest_scinteii'


def material():
    mat=shared.material();mat.name='Casa Scinteii cream stone bronze and slate'
    for node in mat.node_tree.nodes:
        if node.type=='TEX_IMAGE' and node.image:
            for kind in ['diffuse','normal','specular']:
                if kind in node.image.name:
                    node.image=bpy.data.images.load(str(OUT/f'{PREFIX}_{kind}.dds'),check_existing=True)
                    node.image.alpha_mode='CHANNEL_PACKED';node.image.colorspace_settings.name='sRGB' if kind=='diffuse' else 'Non-Color'
    return mat


def box(name,center,size,mat,tile=0,facade=None,side=None):
    obj=detail.block(name,center,size,mat,tile,facade=facade,panel_width=120 if facade==1 else 65)
    if side is not None:
        layer=obj.data.uv_layers.active.data
        for poly in obj.data.polygons:
            if abs(poly.normal.x)>.5:
                for loop,(u,v) in zip(poly.loop_indices,[(0,1),(1,1),(1,0),(0,0)]):layer[loop].uv=shared.uv_tile(side,u,v)
    return obj


def footing(name,x0,x1,y0,y1,mat):
    box(name+' buried wall footings',((x0+x1)/2,(y0+y1)/2,-4),(x1-x0,y1-y0,8),mat,0)


def arcade(name,center,width,bottom,height,depth,bays,normal,mat,segments=4,open_back=False):
    # Genuine arch openings. Small facade/window ornament stays in the atlas.
    nx,ny=normal;ux,uy=-ny,nx;cx,cy=center
    bay=width/bays;radius=bay*.33;spring=height-radius-1.05
    verts=[];faces=[];uvs=[]
    def p(u,d,z):return (cx+ux*u-nx*d,cy+uy*u-ny*d,bottom+z)
    def face(points,tile=0):
        n=len(verts);verts.extend(points);faces.append(tuple(range(n,n+4)))
        uvs.append([shared.uv_tile(tile,u,v) for u,v in [(0,1),(1,1),(1,0),(0,0)]])
    for i in range(bays+1):
        u=-width/2+i*bay
        pier_width=(bay-2*radius) if 0<i<bays else (bay-2*radius)/2
        if i==0:u+=pier_width/2
        elif i==bays:u-=pier_width/2
        a,b=u-pier_width/2,u+pier_width/2
        # The pier tops are covered by the upper wall. Interior backs are hidden
        # by the recessed wall, except in the genuinely open roof lanterns.
        face([p(a,0,0),p(b,0,0),p(b,0,height),p(a,0,height)])
        face([p(a,depth,0),p(a,0,0),p(a,0,height),p(a,depth,height)])
        face([p(b,0,0),p(b,depth,0),p(b,depth,height),p(b,0,height)])
        if open_back:face([p(b,depth,0),p(a,depth,0),p(a,depth,height),p(b,depth,height)])
    for i in range(bays):
        middle=-width/2+(i+.5)*bay
        arc=[(middle+radius*math.cos(math.pi-j*math.pi/segments),spring+radius*math.sin(math.pi-j*math.pi/segments)) for j in range(segments+1)]
        for (a,za),(b,zb) in zip(arc,arc[1:]):
            face([p(a,0,za),p(b,0,zb),p(b,0,height),p(a,0,height)])
            face([p(a,0,za),p(a,depth,za),p(b,depth,zb),p(b,0,zb)],4)
            if open_back:face([p(b,depth,zb),p(a,depth,za),p(a,depth,height),p(b,depth,height)])
        left=middle-radius;right=middle+radius
        face([p(left,depth,0),p(left,0,0),p(left,0,spring),p(left,depth,spring)],4)
        face([p(right,0,0),p(right,depth,0),p(right,depth,spring),p(right,0,spring)],4)
    return shared.mesh_object(name+' arch vaults',verts,faces,uvs,mat)


def coping(name,x,y,z,width,depth,mat):
    # One rectangular ring, rather than five intersecting closed boxes.
    outer=[(x-width/2,y-depth/2),(x+width/2,y-depth/2),(x+width/2,y+depth/2),(x-width/2,y+depth/2)]
    inner=[(x-width/2+.85,y-depth/2+.85),(x+width/2-.85,y-depth/2+.85),(x+width/2-.85,y+depth/2-.85),(x-width/2+.85,y+depth/2-.85)]
    vertices=[(a,b,h) for h,ring in [(z-.6,outer),(z+.4,outer),(z+.4,inner),(z-.15,inner)] for a,b in ring]
    faces=[]
    for i in range(4):
        j=(i+1)%4;faces.extend([(i,j,4+j,4+i),(4+i,4+j,8+j,8+i),(8+i,8+j,12+j,12+i)])
    uvs=[[shared.uv_tile(4,u,v) for u,v in [(0,1),(1,1),(1,0),(0,0)]] for _ in faces]
    return shared.mesh_object(name,vertices,faces,uvs,mat)


def wing(name,x0,x1,y0,y1,mat,arches=()):
    x0,x1=max(-139.5,x0),min(139.5,x1)
    y0,y1=max(-139.5,y0),min(119.5,y1)
    cx,cy=(x0+x1)/2,(y0+y1)/2;w,d=x1-x0,y1-y0
    footing(name,x0,x1,y0,y1,mat)
    if arches:
        box(name+' arcade interior',(cx,cy,3.5),(max(2,w-5),max(2,d-5),7),mat,10)
        for side,normal,c,width in [('S',(0,-1),(cx,y0),w),('N',(0,1),(cx,y1),w),('E',(1,0),(x1,cy),d),('W',(-1,0),(x0,cy),d)]:
            if side in arches:arcade(name+' '+side,c,width,0,7,2.5,max(1,round(width/5.8)),normal,mat)
            else:
                size=(width,.3,7) if side in ['S','N'] else (.3,width,7)
                box(name+' closed lower wall',(c[0],c[1],3.5),size,mat,13 if width>30 else 0)
    else:box(name+' lower masonry',(cx,cy,3.5),(w,d,7),mat,13)
    box(name+' four storey facade',(cx,cy,15),(w,d,16),mat,facade=9)
    coping(name+' cornice',cx,cy,23.5,w+.6,d+.6,mat)
    # Recessed factory skylight/ventilator, restrained enough for the map camera.
    if w*d>1800:box(name+' roof monitor',(cx,cy,24),(w*.35,d*.34,1.1),mat,0)


def lantern(name,x,y,mat):
    # Project slightly beyond the connecting range, avoiding coplanar facades.
    box(name+' pavilion',(x,y,12.5),(19.6,19.6,25),mat,facade=11)
    footing(name,x-9.8,x+9.8,y-9.8,y+9.8,mat)
    coping(name+' pavilion roof',x,y,25.5,20,20,mat)
    box(name+' ornamented drum',(x,y,27.2),(14.2,14.2,3.0),mat,facade=14)
    coping(name+' lantern sill',x,y,29,14.8,14.8,mat)
    for normal,c in [((0,-1),(x,y-6.1)),((0,1),(x,y+6.1)),((1,0),(x+6.1,y)),((-1,0),(x-6.1,y))]:
        arcade(name+' open belvedere',c,12.2,29,10.5,1.5,1,normal,mat,6,True)
    coping(name+' open lantern roof',x,y,40.0,14.2,14.2,mat)
    box(name+' little roof attic',(x,y,40.9),(11.7,11.7,1.0),mat,facade=14)
    box(name+' pinnacle base',(x,y,42),(2.2,2.2,1.4),mat,4)
    detail.pyramid(name+' short obelisk',(x,y,42.7),(1.5,1.5),3.1,mat,4,top=.3)


def star(name,center,radius,mat,tile=6):
    x,y,z=center
    ring=[(x+math.cos(math.pi/2+i*math.pi/5)*(radius if i%2==0 else radius*.43),y,z+math.sin(math.pi/2+i*math.pi/5)*(radius if i%2==0 else radius*.43)) for i in range(10)]
    vertices=[center]+ring;faces=[(0,i+1,(i+1)%10+1) for i in range(10)]
    uvs=[[shared.uv_tile(tile,.5,.5),shared.uv_tile(tile,0,0),shared.uv_tile(tile,1,0)] for _ in faces]
    return shared.mesh_object(name,vertices,faces,uvs,mat)


def bronze_head(name,position,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=10,ring_count=6,radius=1,location=position)
    obj=bpy.context.object;obj.name=name;obj.scale=(.42,.4,.52);obj.data.materials.append(mat)
    for poly in obj.data.polygons:poly.use_smooth=True
    for coord in obj.data.uv_layers.active.data:coord.uv=shared.uv_tile(6,coord.uv.x,coord.uv.y)


def lenin_monument(mat):
    # Small period statue on its own pedestal, not an enclosing ground slab.
    x,y=0,-129
    box('12 Lenin pedestal foundation',(x,y,-3.8),(8,7.2,8.4),mat,0)
    box('12 Lenin plinth step',(x,y,.65),(7.1,6.3,.5),mat,8)
    box('12 Lenin stone pedestal',(x,y,4.45),(4.0,3.5,7.1),mat,0)
    box('12 Lenin pedestal coping',(x,y,8.2),(4.5,4.0,.4),mat,8)
    detail.pyramid('12 bronze long coat',(x,y,9.7),(1.55,1.1),2.65,mat,6,top=1.1)
    for side in [-1,1]:box('12 bronze boots',(x+side*.33,y-.12,8.95),(.47,.72,1.2),mat,6)
    box('12 bronze shoulders',(x,y,12.0),(1.5,.9,.6),mat,6)
    shared.cylinder_between('12 bronze left sleeve',(x-.68,y,11.95),(x-.8,y-.05,10.0),.22,mat,6,8)
    shared.cylinder_between('12 bronze right sleeve',(x+.68,y,11.95),(x+.83,y-.3,10.65),.22,mat,6,8)
    bronze_head('12 bronze Lenin head',(x,y,12.85),mat)
    detail.pyramid('12 short bronze beard',(x,y-.36,12.46),(.34,.28),.32,mat,6,top=.1)


def build(mat):
    # Survey-guided aligned plan: side U wings open west/east; three rear courts.
    for side in [-1,1]:
        x0,x1=(-72,-56) if side<0 else (56,72)
        wing('02 side spine',x0,x1,-140,-26,mat,('W',) if side<0 else ('E',))
        for yy in [-132,-34]:
            a,b=(-140,-72) if side<0 else (72,140)
            wing('02 outward U arm',a,b,yy-8,yy+8,mat,('S',))
            lantern('03 outer pavilion lantern',side*130,-130 if yy==-132 else yy,mat)
    wing('04 inner left bridge',-56,-43,-102,-71,mat)
    wing('04 inner right bridge',46,56,-102,-71,mat)
    wing('04 two-court dividing wing',-8,8,-71,-34,mat)
    wing('04 two-court rear crosspiece',-56,56,-34,-18,mat)
    # Slimmer rear factory: narrower roofs and a shorter, less bulky perimeter.
    wing('05 rear printing west range',-62,-40,-18,92,mat)
    wing('05 rear printing east range',40,62,-18,92,mat)
    wing('05 rear printing north range',-40,40,74,92,mat)
    # Main front office body, with narrow shoulder pylons and 13 rhythmic bays.
    x,y=1.5,-86.5
    footing('06 main office',-43,46,-102,-71,mat)
    box('06 main office arcade interior',(x,y,3.8),(84,26,7.6),mat,10)
    arcade('06 main entrance arcade',(x,-102),89,0,7.6,3.0,13,(0,-1),mat,6)
    box('06 thirteen-storey office facade',(x,y,29.3),(89,31,43.4),mat,facade=1,side=15)
    coping('06 office main roof',x,y,51.6,90,32,mat)
    for xx in [-38.5,41.5]:
        box('07 shoulder pylon',(xx,y,27.8),(12,34,55.6),mat,facade=2,side=15)
        footing('07 shoulder pylon',xx-6,xx+6,y-17,y+17,mat)
        coping('07 pylon cornice',xx,y,55.9,12.8,34.8,mat)
        box('07 pylon small upper openings',(xx,y,54.5),(10.6,33.4,3.2),mat,facade=14)
    # The short open upper pavilion is smaller than the broad office body below.
    box('08 upper pavilion drum',(x,y,53.4),(30,24,3.4),mat,facade=14)
    coping('08 upper pavilion sill',x,y,55.5,31,25,mat)
    box('08 red marble relief backing',(x,y,61.6),(25,19,11.2),mat,facade=12)
    for normal,c,width,bays in [((0,-1),(x,y-12),30,6),((0,1),(x,y+12),30,6),((1,0),(x+15,y),24,4),((-1,0),(x-15,y),24,4)]:
        arcade('08 upper colonnaded pavilion',c,width,55.7,12.0,1.7,bays,normal,mat,5)
    coping('08 ornamental crown',x,y,68.3,32,26,mat)
    box('08 pierced crown frieze',(x,y,69.4),(29.5,23.5,1.4),mat,facade=14)
    for v in [-12,-8,-4,0,4,8,12]:
        for side in [-1,1]:
            box('08 crown small finial',(x+v,y+side*11.7,70.6),(.65,.65,1.0),mat,4)
    # Documented 91.6 m stone arrow and 12.4 m broadcasting antenna.
    detail.pyramid('09 lower masonry arrow',(x,y,70.2),(10,10),5.5,mat,5,top=6.2)
    box('09 slender masonry shaft',(x,y,81.0),(6.2,6.2,10.6),mat,facade=5)
    coping('09 arrow small collar',x,y,86.3,6.8,6.8,mat)
    detail.pyramid('09 terminal masonry arrow',(x,y,86.3),(3.2,3.2),5.3,mat,4,top=.75)
    star('10 period star',(x,y-.6,90.5),1.25,mat)
    shared.lathe('10 television antenna',[(91.6,.38),(94,.32),(98,.23),(101.8,.12),(104,.035)],mat,6,12,True)
    for obj in bpy.context.scene.objects:
        if obj.name.startswith('10 television antenna'):obj.location=(x,y,0)
    lenin_monument(mat)
    return [obj for obj in bpy.context.scene.objects if obj.type=='MESH']


def frame_camera(camera,objects):
    """Fit the actual architecture, keeping every pavilion inside the preview."""
    scene=bpy.context.scene;bpy.context.view_layer.update()
    points=[obj.matrix_world @ vertex.co for obj in objects for vertex in obj.data.vertices
            if (obj.matrix_world @ vertex.co).z>=0]
    def bounds():
        uv=[world_to_camera_view(scene,camera,point) for point in points]
        return min(p.x for p in uv),max(p.x for p in uv),min(p.y for p in uv),max(p.y for p in uv)
    a,b,c,d=bounds()
    camera.data.ortho_scale*=max((b-a)/.92,(d-c)/.86)
    bpy.context.view_layer.update();a,b,c,d=bounds()
    rotation=camera.rotation_euler.to_quaternion()
    aspect=scene.render.resolution_x/scene.render.resolution_y
    camera.location+=(rotation @ Vector((1,0,0)))*((a+b)/2-.5)*camera.data.ortho_scale
    camera.location+=(rotation @ Vector((0,1,0)))*((c+d)/2-.5)*camera.data.ortho_scale/aspect
    bpy.context.view_layer.update()


def main():
    bpy.context.preferences.filepaths.save_version=0
    shared.clear_scene();mat=material();objects=build(mat);bie=shared.exporter()
    for suffix in ['', '_destroyed']:shared.export_objects(objects,'landmark_bucharest_scinteii'+suffix+'.mesh','mdcw_bucharest_scinteii',bie)
    camera=shared.camera_and_light((0,-8,32),(390,-540,300),390,1600)
    scene=bpy.context.scene;scene.render.resolution_x=1600;scene.render.resolution_y=1150;scene.view_settings.exposure=-.30
    frame_camera(camera,objects)
    hero_location=camera.location.copy();hero_rotation=camera.rotation_euler.copy();hero_scale=camera.data.ortho_scale
    for img in bpy.data.images:
        if img.source=='FILE' and img.filepath:
            try:img.pack()
            except RuntimeError:pass
    source=HERE/'source/casa_scinteii.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source))
    scene.render.filepath=str(HERE/'previews/casa_scinteii.png');bpy.ops.render.render(write_still=True)
    camera.location=(350,500,320);camera.rotation_euler=(Vector((0,5,30))-camera.location).to_track_quat('-Z','Y').to_euler()
    frame_camera(camera,objects)
    scene.render.filepath=str(HERE/'previews/casa_scinteii_rear.png');bpy.ops.render.render(write_still=True)
    camera.location=hero_location;camera.rotation_euler=hero_rotation;camera.data.ortho_scale=hero_scale
    bpy.data.objects['Presentation ground (not exported)'].hide_render=True
    scene.render.film_transparent=True;scene.render.resolution_x=384;scene.render.resolution_y=384;scene.cycles.samples=16
    frame_camera(camera,objects)
    scene.render.filepath=str(HERE/'previews/casa_scinteii_icon.png');bpy.ops.render.render(write_still=True)
    mesh=next(meshes(read(OUT/'landmark_bucharest_scinteii.mesh')))[1]
    report={'blender_version':bpy.app.version_string,'exporter':'io_pdx_mesh 0.91','source':str(source.relative_to(HERE)),
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'height':104,'scale':CFG['scale'],'display_height':104*CFG['scale'],
            'mesh_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('landmark_bucharest_scinteii*.mesh')},
            'performance':{'vertices':len(mesh.prop('p').value)//3,'triangles':len(mesh.prop('tri').value)//3,'materials':1,'atlas_size':1024,'mip_levels':11}}
    (HERE/'blender_export.json').write_text(json.dumps(report,indent=2)+'\n')
    print('CASA_SCINTEII_BLENDER_COMPLETE',report['performance'])


if __name__=='__main__':main()
