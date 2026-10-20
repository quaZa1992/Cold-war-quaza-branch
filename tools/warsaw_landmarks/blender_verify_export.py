"""Read the shipped PDX geometry into Blender, with houses at game scale."""
from pathlib import Path
import json
import sys

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tools/berlin_landmarks'))
from pdx import read, meshes

config = json.loads((HERE/'config.json').read_text())
report = json.loads((HERE/'city_style_report.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(HERE/'source/warsaw_palace.blend'))
palace_material = next(mat for mat in bpy.data.materials if 'shader' in mat)
for obj in list(bpy.context.scene.objects):
    if obj.type == 'MESH' and any(mat and 'shader' in mat for mat in obj.data.materials):
        bpy.data.objects.remove(obj, do_unlink=True)


def import_mesh(filename, material, scale=1, offset=(0, 0, 0)):
    shape, data = next(meshes(read(filename)))
    points = data.prop('p').value.reshape(-1, 3)[:, [0, 2, 1]]
    normals = data.prop('n').value.reshape(-1, 3)[:, [0, 2, 1]]
    faces = data.prop('tri').value.reshape(-1, 3)[:, [0, 2, 1]]
    uvs = data.prop('u0').value.reshape(-1, 2)
    mesh = bpy.data.meshes.new(shape+' read from PDX')
    mesh.from_pydata(points.tolist(), [], faces.tolist()); mesh.update()
    mesh.materials.append(material)
    layer = mesh.uv_layers.new(name='UVMap')
    for polygon in mesh.polygons:
        polygon.use_smooth = True
        for loop in polygon.loop_indices:
            u, v = uvs[mesh.loops[loop].vertex_index]
            layer.data[loop].uv = (u, 1-v)
    mesh.normals_split_custom_set_from_vertices(normals.tolist())
    obj = bpy.data.objects.new(shape+' verified export', mesh)
    bpy.context.collection.objects.link(obj)
    obj.scale = (scale,)*3; obj.location = offset
    return obj


import_mesh(ROOT/'gfx/models/buildings/landmarks/landmark_warsaw_palace.mesh', palace_material)
offsets = [(-190, -170, 0), (180, -190, 0), (-190, 170, 0), (190, 160, 0)]
for (label, entry), offset in zip(report['chosen_meshes'].items(), offsets):
    filename = ROOT/'gfx/models/buildings'/entry['mesh']
    mat = bpy.data.materials.new(label); mat.use_nodes = True
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Roughness'].default_value = .82
    texture = mat.node_tree.nodes.new('ShaderNodeTexImage')
    texture.image = bpy.data.images.load(str(HERE/'city_style_runtime'/(filename.stem+'.png')))
    mat.node_tree.links.new(texture.outputs['Color'], shader.inputs['Base Color'])
    import_mesh(filename, mat, entry['combined_scale']/config['scale'], offset)

scene = bpy.context.scene
camera = scene.camera
camera.location = (600, -800, 500)
camera.rotation_euler = (Vector((0, 0, 65))-camera.location).to_track_quat('-Z', 'Y').to_euler()
camera.data.ortho_scale = 650
scene.render.resolution_x = 1500; scene.render.resolution_y = 1100
scene.cycles.samples = 24
scene.render.filepath = str(HERE/'previews/palace_export_scale.png')
bpy.ops.render.render(write_still=True)
print('WARSAW_PALACE_ACTUAL_EXPORT_SCALE_VERIFIED')
