"""Run inside Blender. Author, save, export and render Berlin map landmarks."""
from pathlib import Path
import hashlib
import importlib
import json
import logging
import math
import sys
import types

import bpy
import bmesh
from mathutils import Vector

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
CFG = json.loads((HERE/'config.json').read_text())
OUT = ROOT/'gfx/models/buildings/landmarks'
SOURCE = HERE/'source'
PREVIEW = HERE/'previews'
SOURCE.mkdir(exist_ok=True)
PREVIEW.mkdir(exist_ok=True)


def exporter():
    """Use the installed exporter without registering UI or writing preferences."""
    addon = Path(CFG['exporter'])
    package = types.ModuleType('io_pdx_mesh')
    package.__path__ = [str(addon)]
    package.IO_PDX_LOG = logging.getLogger('io_pdx')
    sys.modules[package.__name__] = package
    sub = types.ModuleType('io_pdx_mesh.pdx_blender')
    sub.__path__ = [str(addon/'pdx_blender')]
    sys.modules[sub.__name__] = sub
    return importlib.import_module('io_pdx_mesh.pdx_blender.blender_import_export')


def uv_tile(tile, u, v):
    row, col = divmod(tile, 4)
    return ((col*128+4+120*u)/512, 1-(row*128+4+120*v)/512)


def material():
    mat = bpy.data.materials.new('Berlin concrete, steel and glazing')
    mat.use_nodes = True
    mat.use_backface_culling = True
    mat['shader'] = 'PdxMeshAdvanced'
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes.get('Principled BSDF')
    def texture(suffix, data=False):
        node = nodes.new('ShaderNodeTexImage')
        node.image = bpy.data.images.load(str(OUT/f'mdcw_berlin_landmarks_{suffix}.dds'), check_existing=True)
        node.image.alpha_mode = 'CHANNEL_PACKED'
        node.image.colorspace_settings.name = 'Non-Color' if data else 'sRGB'
        node.label = suffix
        return node
    diffuse, spec, normal = texture('diffuse'), texture('specular',True), texture('normal',True)
    links.new(diffuse.outputs['Color'], bsdf.inputs['Base Color'])
    links.new(spec.outputs['Alpha'], bsdf.inputs['Roughness'])
    channels = nodes.new('ShaderNodeSeparateColor')
    links.new(spec.outputs['Color'], channels.inputs['Color'])
    links.new(channels.outputs['Green'], bsdf.inputs['Specular IOR Level'])
    links.new(channels.outputs['Blue'], bsdf.inputs['Metallic'])
    nc = nodes.new('ShaderNodeSeparateColor')
    links.new(normal.outputs['Color'],nc.inputs['Color'])
    rgb = nodes.new('ShaderNodeCombineColor')
    rgb.inputs['Blue'].default_value = 1
    links.new(nc.outputs['Green'],rgb.inputs['Red'])
    links.new(normal.outputs['Alpha'],rgb.inputs['Green'])
    nm = nodes.new('ShaderNodeNormalMap')
    links.new(rgb.outputs['Color'],nm.inputs['Color'])
    links.new(nm.outputs['Normal'],bsdf.inputs['Normal'])
    return mat


def mesh_object(name, vertices, faces, face_uvs, mat, smooth=False):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    mesh.materials.append(mat)
    uv = mesh.uv_layers.new(name='UVMap')
    for polygon, coords in zip(mesh.polygons, face_uvs):
        polygon.use_smooth = smooth
        for loop, coord in zip(polygon.loop_indices,coords):
            uv.data[loop].uv = coord
    return obj


def lathe(name, profile, mat, tiles=0, sides=96, smooth=True, windows=False, sphere_uv=False):
    vertices=[];faces=[];uvs=[]
    for height,radius in profile:
        vertices.extend((radius*math.cos(j*2*math.pi/sides),radius*math.sin(j*2*math.pi/sides),height) for j in range(sides))
    for i in range(len(profile)-1):
        tile=tiles[i] if isinstance(tiles,list) else tiles
        for j in range(sides):
            k=(j+1)%sides
            faces.append((i*sides+j,i*sides+k,(i+1)*sides+k,(i+1)*sides+j))
            # Eight atlas repeats around each window row = 64 fine window panes.
            u0=(j%12)/12 if tile==2 and windows else j/sides
            u1=((j%12)+1)/12 if tile==2 and windows else (j+1)/sides
            v0,v1=1,0
            if sphere_uv and tile==1:
                v0=(profile[i][0]-CFG['sphere_center']+16)/32
                v1=(profile[i+1][0]-CFG['sphere_center']+16)/32
            uvs.append([uv_tile(tile,u0,v0),uv_tile(tile,u1,v0),uv_tile(tile,u1,v1),uv_tile(tile,u0,v1)])
    # Triangulated end caps have hard normals; separate from the smooth side rings.
    obj=mesh_object(name,vertices,faces,uvs,mat,smooth)
    for index, normal in [(0,-1),(len(profile)-1,1)]:
        height,radius=profile[index]
        verts=[(0,0,height)]+[(radius*math.cos(j*2*math.pi/sides),radius*math.sin(j*2*math.pi/sides),height) for j in range(sides)]
        capfaces=[]
        for j in range(sides):
            tri=(0,j+1,(j+1)%sides+1)
            capfaces.append(tri if normal>0 else tuple(reversed(tri)))
        tile=tiles[0 if index==0 else -1] if isinstance(tiles,list) else tiles
        mesh_object(name+('_lower_cap' if index==0 else '_upper_cap'),verts,capfaces,
                    [[uv_tile(tile,.5,.5)]*3 for _ in capfaces],mat)
    return obj


def cylinder_between(name, a, b, radius, mat, tile=5, sides=8):
    a,b=Vector(a),Vector(b)
    length=(b-a).length
    obj=lathe(name,[(0,radius),(length,radius)],mat,tile,sides,True)
    # Move the side AND the two matching cap objects into place.
    for part in [obj]+[bpy.data.objects.get(name+s) for s in ['_lower_cap','_upper_cap']]:
        part.location=a
        part.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
    return obj


def make_tower(mat):
    # Engineering elevation: smooth hyperboloid foot, linear concrete taper to
    # 190 m, then a 9 m cylindrical shaft to the 248.7 m catching platform.
    profile=[(-.5,16),(0,16),(1,15.2),(3,13.7),(6,12.0),(10,10.5),
             (15,9.35),(23,8.75),(60,7.81),(100,6.79),(140,5.77),(190,4.5),(248.7,4.5)]
    lathe('01 concrete shaft and curved foot',profile,mat,0,96,True)
    center,radius=CFG['sphere_center'],CFG['sphere_radius']
    heights=sorted(set([center-15.95,center+15.95]+[center+radius*math.sin(math.radians(a)) for a in range(-80,81,5)]+
                       [202.0,205.2,206.2,209.4]))
    sphere=[(h,math.sqrt(radius**2-(h-center)**2)) for h in heights]
    tiles=[2 if (202.0<=h<205.2 or 206.2<=h<209.4) else 1 for h in heights[:-1]]
    lathe('02 silver sphere and two window bands',sphere,mat,tiles,96,True,True,True)
    # Restrained horizontal trims frame the glazing, without checkerboard panels.
    for i,h in enumerate([202.0,205.2,206.2,209.4]):
        r=math.sqrt(radius**2-(h-center)**2)+.08
        lathe(f'03 window trim {i+1}',[(h-.10,r),(h+.10,r)],mat,1,96,True)
    # One principal platform, not a stack of large discs.
    lathe('04 ice catching platform',[(248.7,8.0),(249.7,8.0)],mat,1,64,True)
    for i in range(24):
        angle=2*math.pi*i/24
        a=(7.7*math.cos(angle),7.7*math.sin(angle),249.7)
        b=(a[0],a[1],250.8)
        cylinder_between(f'05 deck railing post {i:02}',a,b,.055,mat,5,4)
    lathe('05 deck upper handrail',[(250.72,7.75),(250.85,7.75)],mat,5,64,True)
    # Original 115 m transmitter: ~4 m base diameter, tapering to the 1.8 m tip.
    bands=[250.0]+list(range(258,346,8))+[345.0,353.0,361.0,365.0]
    bands=sorted(set(bands))
    for i,(a,b) in enumerate(zip(bands,bands[1:])):
        def r(h):return 2.0-(min(h,345)-250)/95*1.1
        lathe(f'06 red white antenna band {i:02}',[(a,r(a)),(b,r(b))],mat,3 if i%2==0 else 4,40,True)
    # Small maintenance collars are subordinate to the main platform and sphere.
    for i,(h,r) in enumerate([(262,2.6),(285,2.05)]):
        lathe(f'07 small maintenance collar {i}',[(h,r),(h+.35,r)],mat,5,40,True)
    # Fine antenna equipment above the sphere, without another broad platform.
    for i in range(8):
        angle=2*math.pi*i/8
        x,y=4.85*math.cos(angle),4.85*math.sin(angle)
        cylinder_between(f'07 receiving aerial {i:02}',(x,y,233.0),(x,y,239.2),.12,mat,5,6)
        cylinder_between(f'07 receiving mount {i:02}',(4.3*math.cos(angle),4.3*math.sin(angle),235.0),(x,y,235.0),.08,mat,5,6)
    return [obj for obj in bpy.context.scene.objects if obj.type=='MESH']


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for collection in list(bpy.data.collections):
        if collection.name!='Collection' and not collection.objects:
            bpy.data.collections.remove(collection)


def export_objects(objects, filename, shape, bie):
    bpy.ops.object.select_all(action='DESELECT')
    copies=[]
    for obj in objects:
        duplicate=obj.copy();duplicate.data=obj.data.copy()
        bpy.context.collection.objects.link(duplicate)
        duplicate.select_set(True);copies.append(duplicate)
        bpy.context.view_layer.objects.active=duplicate
        for modifier in list(duplicate.modifiers):
            bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.context.view_layer.objects.active=copies[0]
    bpy.ops.object.join()
    joined=bpy.context.view_layer.objects.active
    joined.name=shape;joined.data.name=shape
    # Join can leave duplicate material slots. Consolidate to the one atlas.
    atlas=joined.data.materials[0]
    joined.data.materials.clear();joined.data.materials.append(atlas)
    for polygon in joined.data.polygons:polygon.material_index=0
    bpy.ops.object.transform_apply(location=True,rotation=True,scale=True)
    triangulate=joined.modifiers.new('Native triangulation before PDX tangents','TRIANGULATE')
    bpy.ops.object.modifier_apply(modifier=triangulate.name)
    if shape=='landmark_berlin_wall':
        edit=bmesh.new();edit.from_mesh(joined.data)
        bmesh.ops.remove_doubles(edit,verts=list(edit.verts),dist=1e-6)
        bmesh.ops.dissolve_degenerate(edit,edges=list(edit.edges),dist=1e-7)
        collapsed=[face for face in edit.faces if face.calc_area()<1e-12]
        if collapsed:bmesh.ops.delete(edit,geom=collapsed,context='FACES_ONLY')
        bmesh.ops.recalc_face_normals(edit,faces=list(edit.faces))
        edit.to_mesh(joined.data);edit.free();joined.data.update()
        triangulate=joined.modifiers.new('Triangulate cleaned concrete joins','TRIANGULATE')
        bpy.ops.object.modifier_apply(modifier=triangulate.name)
    # Bevel strips can inherit collapsed UV triangles. Give those tiny faces a
    # planar projection within their existing atlas cell before Blender computes
    # tangents, rather than exporting zero tangent vectors.
    uv_layer=joined.data.uv_layers.active.data
    for polygon in joined.data.polygons:
        loops=list(polygon.loop_indices)
        coords=[uv_layer[i].uv.copy() for i in loops]
        a,b=coords[1]-coords[0],coords[2]-coords[0]
        if abs(a.x*b.y-a.y*b.x)<1e-12:
            axes=[axis for axis in range(3) if axis!=max(range(3),key=lambda axis:abs(polygon.normal[axis]))]
            points=[joined.data.vertices[joined.data.loops[i].vertex_index].co for i in loops]
            low=[min(point[axis] for point in points) for axis in axes]
            extent=[max(point[axis] for point in points)-value for axis,value in zip(axes,low)]
            center=sum(coords,Vector((0,0)))/3
            cell=[min(3,max(0,int(center[axis]*4))) for axis in range(2)]
            for index,point in zip(loops,points):
                uv_layer[index].uv=tuple((cell[j]+.05+.90*(point[axis]-low[j])/max(extent[j],1e-12))/4 for j,axis in enumerate(axes))
    joined.data.update()
    joined.data.calc_tangents(uvmap=joined.data.uv_layers.active.name)
    for polygon in joined.data.polygons:
        if any(joined.data.loops[i].tangent.length<.9 for i in polygon.loop_indices):
            polygon.use_smooth=False
    joined.data.free_tangents()
    joined.data.update()
    bie.export_meshfile(str(OUT/filename),exp_mesh=True,exp_skel=False,exp_locs=False,
                       exp_selected=True,split_verts=False,sort_verts='~',plain_txt=False)
    data=joined.data
    bpy.data.objects.remove(joined,do_unlink=True)
    bpy.data.meshes.remove(data)


def camera_and_light(target, camera_position, ortho, floor_size):
    scene=bpy.context.scene
    scene.render.engine='CYCLES';scene.cycles.samples=24
    scene.cycles.use_denoising=True
    scene.render.threads_mode='FIXED';scene.render.threads=8
    scene.render.resolution_x=900;scene.render.resolution_y=1100;scene.render.resolution_percentage=100
    scene.view_settings.view_transform='AgX'
    scene.world.color=(.6,.6,.6)
    world=scene.world;world.use_nodes=True
    world.node_tree.nodes['Background'].inputs['Color'].default_value=(.56,.61,.67,1)
    world.node_tree.nodes['Background'].inputs['Strength'].default_value=.6
    data=bpy.data.cameras.new('Presentation camera');camera=bpy.data.objects.new('Presentation camera',data)
    scene.collection.objects.link(camera);camera.location=camera_position
    camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
    data.type='ORTHO';data.ortho_scale=ortho;data.clip_end=5000
    scene.camera=camera
    for name,position,energy,size in [
        ('Large softbox',Vector(target)+Vector((-ortho, -ortho, ortho)),ortho**2*70,ortho*.7),
        ('Silver rim',Vector(target)+Vector((ortho*.7,ortho*.3,ortho*.5)),ortho**2*45,ortho*.6),
    ]:
        ld=bpy.data.lights.new(name,'AREA');ld.energy=energy;ld.shape='DISK';ld.size=size
        light=bpy.data.objects.new(name,ld);scene.collection.objects.link(light);light.location=position
        light.rotation_euler=(Vector(target)-light.location).to_track_quat('-Z','Y').to_euler()
    bpy.ops.mesh.primitive_plane_add(size=floor_size,location=(0,0,-.55 if ortho>100 else -.12))
    plane=bpy.context.object;plane.name='Presentation ground (not exported)'
    ground=bpy.data.materials.new('Neutral presentation ground');ground.diffuse_color=(.19,.21,.22,1)
    ground.use_nodes=True;ground.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.19,.21,.22,1)
    plane.data.materials.append(ground)
    return camera


def save_source(filename):
    # Keep textures with the editable project and disable autosave backup files.
    bpy.context.preferences.filepaths.save_version=0
    for image in bpy.data.images:
        if image.source=='FILE' and image.filepath:
            try:image.pack()
            except RuntimeError:pass
    bpy.ops.wm.save_as_mainfile(filepath=str(SOURCE/filename))


def main():
    logging.basicConfig(level=logging.WARNING)
    bie=exporter()
    clear_scene();mat=material()
    tower=make_tower(mat)
    export_objects(tower,'landmark_berlin_tv_tower.mesh','mdcw_berlin_tv_tower',bie)
    # Damage disabled for this landmark; a valid identical fallback is retained.
    export_objects(tower,'landmark_berlin_tv_tower_destroyed.mesh','mdcw_berlin_tv_tower',bie)
    camera=camera_and_light((0,0,180),(460,-650,245),410,1400)
    save_source('tv_tower.blend')
    bpy.context.scene.render.filepath=str(PREVIEW/'blender_tower.png')
    bpy.ops.render.render(write_still=True)
    # Inspect the actual sphere, observation glazing and antenna platform close up.
    camera.location=(125,-170,245);camera.rotation_euler=(Vector((0,0,231))-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.ortho_scale=88
    bpy.context.scene.render.filepath=str(PREVIEW/'blender_tower_detail.png')
    bpy.ops.render.render(write_still=True)

    clear_scene();mat=material()
    from blender_wall import build_wall
    wall=build_wall(mat,CFG)
    export_objects(wall,'landmark_berlin_wall.mesh','landmark_berlin_wall',bie)
    export_objects(wall,'landmark_berlin_wall_destroyed.mesh','landmark_berlin_wall',bie)
    camera_and_light((-.9,.1,.18),(11,-18,17),10.8,80)
    save_source('berlin_wall.blend')
    bpy.context.scene.render.resolution_x=1400;bpy.context.scene.render.resolution_y=950
    bpy.context.scene.render.filepath=str(PREVIEW/'blender_wall.png')
    bpy.ops.render.render(write_still=True)
    # Render an additional composition at the actual entity scale and positions.
    with bpy.data.libraries.load(str(SOURCE/'tv_tower.blend'),link=False) as (available,loaded):
        loaded.objects=[name for name in available.objects if name[:2].isdigit()]
    delta=Vector((CFG['tower_anchor'][0]-CFG['wall_anchor'][0],
                  CFG['tower_anchor'][1]-CFG['wall_anchor'][1],0))
    for obj in loaded.objects:
        if obj is not None and obj.type=='MESH':
            bpy.context.collection.objects.link(obj)
            obj.location=obj.location*CFG['tower_scale']+delta
            obj.scale*=CFG['tower_scale']
    camera=bpy.context.scene.camera
    camera.location=(12,-17,14)
    camera.rotation_euler=(Vector((0,.5,1.7))-camera.location).to_track_quat('-Z','Y').to_euler()
    camera.data.ortho_scale=14.7
    bpy.context.scene.render.resolution_y=1000
    bpy.context.scene.render.filepath=str(PREVIEW/'blender_map_scale.png')
    bpy.ops.render.render(write_still=True)
    sources=[]
    for path in [SOURCE/'tv_tower.blend',SOURCE/'berlin_wall.blend']:
        sources.append({'path':str(path.relative_to(HERE)), 'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    manifest={'blender_version':bpy.app.version_string,'exporter':'io_pdx_mesh 0.91 (installed native Blender exporter)',
              'sources':sources,'tower_scale':CFG['tower_scale'],'display_height':CFG['tower_height']*CFG['tower_scale'],
              'exported_files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.glob('landmark_berlin_*.mesh')},
              'validation_scope':'Blender authoring, native PDX export and render; no in-game screenshot'}
    (HERE/'blender_export.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('BLENDER_BERLIN_COMPLETE',json.dumps(manifest))


if __name__=='__main__':
    main()
