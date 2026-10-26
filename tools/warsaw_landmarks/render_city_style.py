# IMPERIA CW — Cold War: warsaw landmarks — render city style.
"""Render actual low/midrise game meshes selected for the Warsaw city style."""
from pathlib import Path
import json
import sys

import bpy
from mathutils import Vector

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'tools/berlin_landmarks'))
from pdx import read, meshes

report = json.loads((HERE/'city_style_report.json').read_text())
runtime = HERE/'city_style_runtime'
preview = HERE/'previews'
preview.mkdir(exist_ok=True)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for index, (label, entry) in enumerate(report['chosen_meshes'].items()):
    filename = ROOT/'gfx/models/buildings'/entry['mesh']
    shape, source = next(meshes(read(filename)))  # only the highest-detail LOD
    p = source.prop('p').value.reshape(-1, 3)[:, [0, 2, 1]]*entry['combined_scale']
    t = source.prop('tri').value.reshape(-1, 3)[:, [0, 2, 1]]
    uv = source.prop('u0').value.reshape(-1, 2)
    mesh = bpy.data.meshes.new(shape)
    mesh.from_pydata(p.tolist(), [], t.tolist())
    mesh.update()
    layer = mesh.uv_layers.new(name='UVMap')
    for polygon in mesh.polygons:
        for loop in polygon.loop_indices:
            u, v = uv[mesh.loops[loop].vertex_index]
            layer.data[loop].uv = (u, 1-v)
    material = bpy.data.materials.new(label)
    material.use_nodes = True
    shader = material.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Roughness'].default_value = .82
    image = material.node_tree.nodes.new('ShaderNodeTexImage')
    image.image = bpy.data.images.load(str(runtime/(filename.stem+'.png')))
    material.node_tree.links.new(image.outputs['Color'], shader.inputs['Base Color'])
    mesh.materials.append(material)
    obj = bpy.data.objects.new(label, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location.x = (index-1.5)*1.7
    bpy.ops.object.text_add(location=(obj.location.x-.5, -.91, .006))
    text = bpy.context.object
    text.data.body = ['LOW HOUSES', 'OLD TOWN', 'COURTYARD BLOCK', 'APARTMENTS'][index]
    text.data.size = .105
    text.data.extrude = 0
    ink = bpy.data.materials.get('Label ink') or bpy.data.materials.new('Label ink')
    ink.diffuse_color = (.06, .07, .08, 1)
    text.data.materials.append(ink)

bpy.ops.mesh.primitive_plane_add(size=200)
ground = bpy.context.object
ground.location.z = -.015
material = bpy.data.materials.new('Matte ground')
material.diffuse_color = (.55, .57, .55, 1)
ground.data.materials.append(material)
bpy.ops.object.light_add(type='AREA', location=(0, -4, 6))
light = bpy.context.object
light.data.energy = 500
light.data.shape = 'DISK'
light.data.size = 6
bpy.ops.object.camera_add(location=(3.4, -7.5, 5.2))
camera = bpy.context.object
camera.rotation_euler = (Vector((0, 0, .10))-camera.location).to_track_quat('-Z', 'Y').to_euler()
camera.data.type = 'ORTHO'
camera.data.ortho_scale = 8.8
scene = bpy.context.scene
scene.camera = camera
scene.render.engine = 'BLENDER_EEVEE_NEXT'
scene.world.color = (.45, .45, .45)
scene.render.resolution_x = 1600
scene.render.resolution_y = 640
scene.render.resolution_percentage = 100
scene.view_settings.view_transform = 'Standard'
scene.render.filepath = str(preview/'city_style.png')
bpy.ops.render.render(write_still=True)
print('WARSAW_CITY_STYLE_ACTUAL_MESH_RENDERED')
