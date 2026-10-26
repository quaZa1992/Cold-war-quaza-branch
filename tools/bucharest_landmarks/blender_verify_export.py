# IMPERIA CW — Cold War: bucharest landmarks — blender verify export.
"""Render the shipped native PDX file after reading its UVs/normals back."""
from pathlib import Path
import sys
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/berlin_landmarks'))
from pdx import read,meshes

bpy.ops.wm.open_mainfile(filepath=str(HERE/'source/casa_scinteii.blend'))
material=next(mat for mat in bpy.data.materials if 'shader' in mat)
for obj in list(bpy.context.scene.objects):
    if obj.type=='MESH' and any(mat and 'shader' in mat for mat in obj.data.materials):
        bpy.data.objects.remove(obj,do_unlink=True)
shape,data=next(meshes(read(ROOT/'gfx/models/buildings/landmarks/landmark_bucharest_scinteii.mesh')))
points=data.prop('p').value.reshape(-1,3)[:,[0,2,1]]
normals=data.prop('n').value.reshape(-1,3)[:,[0,2,1]]
faces=data.prop('tri').value.reshape(-1,3)[:,[0,2,1]]
uvs=data.prop('u0').value.reshape(-1,2)
mesh=bpy.data.meshes.new(shape+' actual native export')
mesh.from_pydata(points.tolist(),[],faces.tolist());mesh.update();mesh.materials.append(material)
layer=mesh.uv_layers.new(name='UVMap')
for polygon in mesh.polygons:
    polygon.use_smooth=True
    for loop in polygon.loop_indices:
        u,v=uvs[mesh.loops[loop].vertex_index];layer.data[loop].uv=(u,1-v)
mesh.normals_split_custom_set_from_vertices(normals.tolist())
obj=bpy.data.objects.new(shape+' read back from PDX',mesh)
bpy.context.collection.objects.link(obj)
scene=bpy.context.scene
scene.render.filepath=str(HERE/'previews/casa_scinteii_export.png')
bpy.ops.render.render(write_still=True)
print('CASA_SCINTEII_ACTUAL_EXPORT_VERIFIED')
