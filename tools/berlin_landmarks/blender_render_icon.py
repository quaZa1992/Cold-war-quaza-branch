"""Render the saved Blender source as a transparent inventory symbol."""
from pathlib import Path
import bpy
root=Path(__file__).resolve().parent
scene=bpy.context.scene
for obj in scene.objects:
    if obj.name.startswith('Presentation ground'):obj.hide_render=True
scene.render.film_transparent=True
scene.render.resolution_x=256;scene.render.resolution_y=512
scene.render.resolution_percentage=100
scene.cycles.samples=16
scene.render.filepath=str(root/'previews/blender_tower_icon.png')
bpy.ops.render.render(write_still=True)
