# IMPERIA CW — Cold War: jerusalem landmarks — blender western wall.
"""Western Wall prayer facade, native Blender, period context circa 1970."""
from pathlib import Path
import hashlib,json,math,random,sys
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/berlin_landmarks'))
sys.path.insert(0,str(ROOT/'tools/warsaw_landmarks'))
sys.path.insert(0,str(ROOT/'tools/bucharest_landmarks'))
import blender_landmarks as shared
import blender_palace as detail
from blender_scinteii import frame_camera
from pdx import read,meshes
CFG=json.loads((HERE/'config.json').read_text())
OUT=ROOT/'gfx/models/buildings/landmarks';shared.OUT=OUT
PREFIX='mdcw_jerusalem_western_wall'


def material():
    mat=shared.material();mat.name='Western Wall weathered Jerusalem limestone'
    for node in mat.node_tree.nodes:
        if node.type=='TEX_IMAGE' and node.image:
            for kind in ['diffuse','normal','specular']:
                if kind in node.image.name:
                    node.image=bpy.data.images.load(str(OUT/f'{PREFIX}_{kind}.dds'),check_existing=True)
                    node.image.alpha_mode='CHANNEL_PACKED'
                    node.image.colorspace_settings.name='sRGB' if kind=='diffuse' else 'Non-Color'
    # Game specular alpha is glossiness. Invert only this landmark's preview
    # graph so Blender roughness matches the shipped matte limestone material.
    nodes,links=mat.node_tree.nodes,mat.node_tree.links
    specular=next(node for node in nodes if node.type=='TEX_IMAGE' and node.label=='specular')
    inverse=nodes.new('ShaderNodeMath');inverse.operation='SUBTRACT'
    inverse.label='Native glossiness to Blender roughness';inverse.inputs[0].default_value=1
    links.new(specular.outputs['Alpha'],inverse.inputs[1])
    links.new(inverse.outputs[0],nodes.get('Principled BSDF').inputs['Roughness'])
    return mat


def box(name,center,size,mat,tile=0):
    return detail.block(name,center,size,mat,tile)


def stone(name,ya,yb,za,zb,mat,tile,boss,rng):
    # The back is supplied once by the continuous structural wall. Ten triangles
    # give each visible ashlar a drafted edge and a shallow projecting boss.
    outer=[(.05,ya,za),(.05,ya,zb),(.05,yb,zb),(.05,yb,za)]
    margin_y=min(.16,(yb-ya)*.08);margin_z=min(.14,(zb-za)*.12)
    face_x=-boss
    inner=[(face_x,ya+margin_y,za+margin_z),(face_x,ya+margin_y,zb-margin_z),
           (face_x,yb-margin_y,zb-margin_z),(face_x,yb-margin_y,za+margin_z)]
    verts=outer+inner
    faces=[(i,(i+1)%4,(i+1)%4+4,i+4) for i in range(4)]+[(4,5,6,7)]
    uvs=[]
    for face in faces:
        uvs.append([shared.uv_tile(tile,(verts[k][1]-ya)/(yb-ya),(verts[k][2]-za)/(zb-za)) for k in face])
    return shared.mesh_object(name,verts,faces,uvs,mat)


def panel(name,x,ya,yb,za,zb,mat,tile):
    p=[(x,ya,za),(x,ya,zb),(x,yb,zb),(x,yb,za)]
    uv=[[shared.uv_tile(tile,u,v) for u,v in [(0,0),(0,1),(1,1),(1,0)]]]
    return shared.mesh_object(name,p,[(0,1,2,3)],uv,mat)


def plant(name,y,z,radius,mat,rng):
    # Opaque twelve-vertex clumps: no alpha overdraw, wind bones or extra material.
    for j in range(2):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=radius*(.8 if j else 1),location=(-.30-j*.13,y+j*.18,z-j*.14))
        obj=bpy.context.object;obj.name=name+f' {j}'
        obj.scale=(.55,1,.72);obj.data.materials.append(mat)
        for old in list(obj.data.uv_layers):obj.data.uv_layers.remove(old)
        layer=obj.data.uv_layers.new(name='UVMap')
        for poly in obj.data.polygons:
            for idx,(u,v) in zip(poly.loop_indices,[(0,0),(1,0),(.5,1)]):layer.data[idx].uv=shared.uv_tile(10,u,v)


def north_entry(mat):
    # Narrow pointed doorway in a thick rough-stone wall, visible in Carmi1969.
    for a,b in [(20.5,23),(26,28.5)]:
        box('04 pointed entrance side pier',(-7.35,(a+b)/2,2.9),(1.3,b-a,4.2),mat,5)
    curve=[(23,3),(23.4,3.7),(23.9,4.4),(24.5,4.9),(25.1,4.4),(25.6,3.7),(26,3)]
    verts=[];faces=[];uvs=[]
    for (a,za),(b,zb) in zip(curve,curve[1:]):
        for p in [[(-8,a,za),(-8,a,5),(-8,b,5),(-8,b,zb)],
                  [(-8,a,za),(-8,b,zb),(-6.7,b,zb),(-6.7,a,za)]]:
            n=len(verts);verts.extend(p);faces.append((n,n+1,n+2,n+3))
            uvs.append([shared.uv_tile(5,u,v) for u,v in [(0,0),(0,1),(1,1),(1,0)]])
    shared.mesh_object('04 pointed arch masonry and deep reveal',verts,faces,uvs,mat)
    # The small upper window also has an arched head, with no extra materials.
    yz=[(24.05,16),(24.05,17.05),(24.18,17.38),(24.5,17.6),(24.82,17.38),(24.95,17.05),(24.95,16)]
    verts=[(-8.026,y,z) for y,z in yz]
    shared.mesh_object('04 little arched upper window',verts,[tuple(range(len(verts)))],
                       [[shared.uv_tile(7,(y-24.05)/.9,(z-16)/1.6) for y,z in yz]],mat)


def build(mat):
    rng=random.Random(1970)
    # Source X west/east, Y south/north. Original prayer face approximately57x19m.
    box('01 continuous retaining wall',(2,0,3.5),(4,57,31),mat,5)
    # Above core top19; lower part down to-12 is buried terrain protection.
    heights=[1.25,1.40,1.30,1.45,1.20,1.35,1.15,.90,.85,.90,.95]
    z=0
    for row,h in enumerate(heights):
        lengths=[];y=-28.5
        # The running bond is deliberately irregular; mortar gaps stay narrow.
        while y<28.5-.01:
            w=min(rng.uniform(2.8,5.4) if row<7 else rng.uniform(1.9,3.5),28.5-y)
            if 0<28.5-y-w<.8:w=28.5-y
            lengths.append((y,y+w));y+=w
        for col,(a,b) in enumerate(lengths):
            stone(f'02 drafted ashlar {row:02d}-{col:02d}',a+.025,b-.025,z+.018,z+h-.018,mat,rng.randrange(4),rng.uniform(.06,.15) if row<7 else .045,rng)
        z+=h
    # Small upper restoration stones occupy17 courses, packed in one atlas tile.
    for i in range(4):panel(f'03 small upper stones panel {i}',-.012,-28.5+i*14.25,-28.5+(i+1)*14.25,z,19,mat,4)
    # Flat top, no decorative battlements or invented parapet.
    # Northern rough-stone abutment, small vaulted entrance and grilled windows.
    box('04 north covered bay upper body',(-2,24.5,13.5),(12,8,17),mat,5)
    box('04 north covered bay buried rear',(.75,24.5,-3.5),(6.5,8,17),mat,5)
    for y in [20.8,28.2]:
        box('04 north bay solid return wall',(-4.6,y,-3.5),(4.2,.6,17),mat,5)
    box('04 north bay dark vaulted interior',(-5.8,24.5,2.5),(.4,6,5),mat,7)
    north_entry(mat)
    for y in [22.6,26.25]:
        panel('04 grilled north window',-8.025,y-.48,y+.48,8,10,mat,11)
        for e in [-1,1]:box('04 window limestone jamb',(-8.09,y+e*.56,9),(.16,.15,2.25),mat,1)
        box('04 window lintel',(-8.09,y,10.14),(.16,1.25,.20),mat,1)
    # Low stone/earth southern access bank, period silhouette, no modern bridge.
    p=[(4.04,-28.45,-12),(8,-28.45,-12),(8,-21,-12),(4.04,-21,-12),
       (4.04,-28.45,8),(8,-28.45,8),(8,-21,.8),(4.04,-21,.8)]
    f=[(0,1,5,4),(1,2,6,5),(2,3,7,6),(4,5,6,7)]
    uv=[[shared.uv_tile(12,u,v) for u,v in [(0,0),(1,0),(1,1),(0,1)]] for _ in f]
    shared.mesh_object('06 southern stone and earth access',p,f,uv,mat)
    for i,(y,h,r) in enumerate([(-24,7.9,.50),(-19,9.0,.33),(-15,6.8,.39),(-10,9.15,.63),(-6,10.9,.45),(-2,8.0,.35),(3,8.0,.32),(7,6.7,.50),(11,9.15,.62),(15,11.7,.37),(18,8.0,.38),(-22,11.1,.27)]):
        plant(f'07 caper growing from joint {i}',y,h,r,mat,rng)
    # Simple removable timber prayer partition documented in the period photos.
    for i in range(9):
        x=-3-i*2.5;floor=.8+.22*x
        box('08 timber screen post',(x,-5,floor+.62),(.13,.13,1.24),mat,9)
    for i in range(8):
        x=-4.25-i*2.5;floor=.8+.22*x
        for zoff in [.28,.95]:box('08 timber screen rail',(x,-5,floor+zoff),(2.5,.10,.10),mat,9)
        for j in range(3):
            xx=x-.8+j*.8;zz=.8+.22*xx
            box('08 timber screen lattice',(xx,-5,zz+.61),(.07,.07,.60),mat,9)
    return [obj for obj in bpy.context.scene.objects if obj.type=='MESH']


def main():
    for folder in ['source','previews','runtime']:(HERE/folder).mkdir(exist_ok=True)
    bpy.context.preferences.filepaths.save_version=0
    shared.clear_scene();mat=material();objects=build(mat);bie=shared.exporter()
    for suffix in ['', '_destroyed']:
        shared.export_objects(objects,'landmark_jerusalem_western_wall'+suffix+'.mesh','landmark_jerusalem_western_wall',bie)
    camera=shared.camera_and_light((-10,0,7),(-96,-85,68),92,500)
    scene=bpy.context.scene;scene.render.resolution_x=1400;scene.render.resolution_y=1000
    scene.view_settings.exposure=-.45
    # Matching presentation terrain hides the same buried wall footings as game.
    ground=bpy.data.objects['Presentation ground (not exported)']
    ground.location.z=.65;ground.rotation_euler.y=-math.atan(.22)
    frame_camera(camera,objects)
    hero_location=camera.location.copy();hero_rotation=camera.rotation_euler.copy();hero_scale=camera.data.ortho_scale
    for img in bpy.data.images:
        if img.source=='FILE' and img.filepath:
            try:img.pack()
            except RuntimeError:pass
    source=HERE/'source/western_wall.blend';bpy.ops.wm.save_as_mainfile(filepath=str(source))
    scene.render.filepath=str(HERE/'previews/western_wall.png');bpy.ops.render.render(write_still=True)
    camera.location=(-85,-18,30);camera.rotation_euler=(Vector((0,-2,9))-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.ortho_scale=70
    scene.render.filepath=str(HERE/'previews/western_wall_detail.png');bpy.ops.render.render(write_still=True)
    camera.location=hero_location;camera.rotation_euler=hero_rotation;camera.data.ortho_scale=hero_scale
    ground.hide_render=True;scene.render.film_transparent=True
    # Icon excludes buried footings by using a non-exported holdout terrain.
    holdout=bpy.data.materials.new('UI only holdout terrain');holdout.use_nodes=True
    nodes=holdout.node_tree.nodes;nodes.clear();shader=nodes.new('ShaderNodeHoldout');output=nodes.new('ShaderNodeOutputMaterial')
    holdout.node_tree.links.new(shader.outputs[0],output.inputs['Surface'])
    ground.data.materials.clear();ground.data.materials.append(holdout);ground.hide_render=False
    scene.render.resolution_x=384;scene.render.resolution_y=384;scene.cycles.samples=16
    frame_camera(camera,objects)
    scene.render.filepath=str(HERE/'previews/western_wall_icon.png');bpy.ops.render.render(write_still=True)
    mesh=next(meshes(read(OUT/'landmark_jerusalem_western_wall.mesh')))[1]
    report={'blender_version':bpy.app.version_string,'exporter':'io_pdx_mesh 0.91','source':str(source.relative_to(HERE)),
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'height':22,'scale':CFG['scale'],'display_height':22*CFG['scale'],
            'mesh_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('landmark_jerusalem_western_wall*.mesh')},
            'performance':{'vertices':len(mesh.prop('p').value)//3,'triangles':len(mesh.prop('tri').value)//3,'materials':1,'atlas_size':1024,'mip_levels':11}}
    (HERE/'blender_export.json').write_text(json.dumps(report,indent=2)+'\n')
    print('WESTERN_WALL_BLENDER_COMPLETE',report['performance'])


if __name__=='__main__':main()
