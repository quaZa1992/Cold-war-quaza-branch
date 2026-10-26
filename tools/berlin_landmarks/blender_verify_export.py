# IMPERIA CW — Cold War: berlin landmarks — blender verify export.
"""Render the actual exported PDX meshes at their game scale in Blender."""
from pathlib import Path
import sys
import json
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from pdx import read,meshes
config=json.loads((HERE/'config.json').read_text())
out=HERE.parents[1]/'gfx/models/buildings/landmarks'
bpy.ops.wm.open_mainfile(filepath=str(HERE/'source/berlin_wall.blend'))
material=next(mat for mat in bpy.data.materials if 'shader' in mat)
for obj in list(bpy.context.scene.objects):
    if obj.type=='MESH' and any(mat and 'shader' in mat for mat in obj.data.materials):
        bpy.data.objects.remove(obj,do_unlink=True)
for filename,scale,offset in [
    ('landmark_berlin_wall.mesh',1,(0,0,0)),
    ('landmark_berlin_tv_tower.mesh',config['tower_scale'],
     (config['tower_anchor'][0]-config['wall_anchor'][0],config['tower_anchor'][1]-config['wall_anchor'][1],0)),
]:
    shape,source=next(meshes(read(out/filename)))
    p=source.prop('p').value.reshape(-1,3)[:,[0,2,1]]
    n=source.prop('n').value.reshape(-1,3)[:,[0,2,1]]
    t=source.prop('tri').value.reshape(-1,3)[:,[0,2,1]]
    uv=source.prop('u0').value.reshape(-1,2)
    mesh=bpy.data.meshes.new(shape+' verified export')
    mesh.from_pydata(p.tolist(),[],t.tolist());mesh.update()
    mesh.materials.append(material)
    layer=mesh.uv_layers.new(name='UVMap')
    for polygon in mesh.polygons:
        polygon.use_smooth=True
        for i in polygon.loop_indices:
            u,v=uv[mesh.loops[i].vertex_index]
            layer.data[i].uv=(u,1-v)
    mesh.normals_split_custom_set_from_vertices(n.tolist())
    obj=bpy.data.objects.new(shape+' from PDX',mesh)
    bpy.context.collection.objects.link(obj);obj.scale=(scale,)*3;obj.location=offset
scene=bpy.context.scene;camera=scene.camera
camera.location=(12,-17,14)
camera.rotation_euler=(Vector((0,.5,1.7))-camera.location).to_track_quat('-Z','Y').to_euler()
camera.data.ortho_scale=14.7
scene.render.resolution_x=1400;scene.render.resolution_y=1000
scene.cycles.samples=24
scene.render.filepath=str(HERE/'previews/blender_export_verification.png')
bpy.ops.render.render(write_still=True)
print('EXPORTED_MESH_VISUAL_VERIFICATION_RENDERED')
