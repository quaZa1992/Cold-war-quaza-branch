# IMPERIA CW — Cold War: berlin landmarks — blender wall.
"""Editable Berlin wall made with native Blender meshes.

Called by the landmark Blender build. Coordinates are map X, map north, height;
the five-point route replaces the province bitmap's one-pixel stair steps.
"""

import math

import bmesh
import bpy
from mathutils import Vector


DEFAULT_ROUTE = [
    (3011.0, 1574.0),
    (3011.5, 1572.0),
    (3011.5, 1569.0),
    (3014.0, 1566.5),
    (3014.0, 1566.0),
]


def _atlas_uv(tile, u, v):
    row, column = divmod(tile, 4)
    return ((column * 128 + 4 + 120 * u) / 512,
            1 - (row * 128 + 4 + 120 * v) / 512)


class _NativeMesh:
    """Collect disconnected native primitives into an editable named part."""

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.tiles = []
        self.smooth = []

    def face(self, points, tile=9, smooth=False):
        first = len(self.vertices)
        self.vertices.extend(tuple(point) for point in points)
        self.faces.append(tuple(range(first, first + len(points))))
        self.tiles.append(tile)
        self.smooth.append(smooth)

    def box(self, center, size, tile=9, direction=(1, 0)):
        center = Vector(center)
        along = Vector((direction[0], direction[1], 0)).normalized()
        across = Vector((-along.y, along.x, 0))
        vertical = Vector((0, 0, 1))
        half = [value * .5 for value in size]
        points = [center + along * (a * half[0])
                  + across * (b * half[1]) + vertical * (c * half[2])
                  for a, b, c in [(-1, -1, -1), (1, -1, -1),
                                  (1, 1, -1), (-1, 1, -1),
                                  (-1, -1, 1), (1, -1, 1),
                                  (1, 1, 1), (-1, 1, 1)]]
        for indices in [(0, 3, 2, 1), (4, 5, 6, 7),
                        (0, 1, 5, 4), (1, 2, 6, 5),
                        (2, 3, 7, 6), (3, 0, 4, 7)]:
            self.face([points[index] for index in indices], tile)

    def tube(self, start, end, radius, tile=5, sides=8):
        start, end = Vector(start), Vector(end)
        axis = (end - start).normalized()
        reference = Vector((0, 0, 1))
        if abs(axis.dot(reference)) > .95:
            reference = Vector((1, 0, 0))
        u = axis.cross(reference).normalized()
        v = axis.cross(u).normalized()
        ring = [radius * (u * math.cos(2 * math.pi * i / sides)
                          + v * math.sin(2 * math.pi * i / sides))
                for i in range(sides)]
        for i in range(sides):
            j = (i + 1) % sides
            self.face([start + ring[i], start + ring[j],
                       end + ring[j], end + ring[i]], tile, smooth=True)
        self.face([start + point for point in reversed(ring)], tile)
        self.face([end + point for point in ring], tile)

    def object(self, name, material, bevel=0):
        mesh = bpy.data.meshes.new(name + "_Mesh")
        mesh.from_pydata(self.vertices, [], self.faces)
        mesh.materials.append(material)
        mesh.update()
        uv = mesh.uv_layers.new(name="UVMap")
        for polygon, tile, smooth in zip(mesh.polygons, self.tiles, self.smooth):
            polygon.use_smooth = smooth
            count = len(polygon.loop_indices)
            corners = [(0, 1), (1, 1), (1, 0), (0, 0)]
            for index, loop_index in enumerate(polygon.loop_indices):
                if count <= 4:
                    u, v = corners[index]
                else:
                    angle = 2 * math.pi * index / count
                    u, v = .5 + .5 * math.cos(angle), .5 + .5 * math.sin(angle)
                uv.data[loop_index].uv = _atlas_uv(tile, u, v)
        # Recalculate with Blender itself, preserving the authored UV layers.
        edit_mesh = bmesh.new()
        edit_mesh.from_mesh(mesh)
        bmesh.ops.remove_doubles(edit_mesh, verts=list(edit_mesh.verts), dist=1e-7)
        bmesh.ops.recalc_face_normals(edit_mesh, faces=edit_mesh.faces)
        edit_mesh.to_mesh(mesh)
        edit_mesh.free()
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.collection.objects.link(obj)
        if bevel:
            modifier = obj.modifiers.new("Kleine_Betonkanten", 'BEVEL')
            modifier.width = bevel
            modifier.segments = 2
            modifier.use_clamp_overlap = True
            # Ground-facing bottom bevels create long sliver triangles hidden
            # below terrain. Bevel the exposed upper concrete edges only.
            group = obj.vertex_groups.new(name='Exposed_concrete_edges')
            indices = [vertex.index for vertex in mesh.vertices if vertex.co.z > .001]
            if indices:
                group.add(indices, 1.0, 'REPLACE')
                modifier.limit_method = 'VGROUP'
                modifier.vertex_group = group.name
        return obj


def build_wall(material, config):
    """Return native mesh parts; the caller evaluates modifiers for export.

    ``wall_world`` is the simplified five-point X/north route and ``wall_anchor``
    is its game locator. Positive offsets point into East Berlin.
    """
    world = config.get("wall_world", DEFAULT_ROUTE)
    anchor = Vector(config.get("wall_anchor", (3013.5, 1569.5)))
    if len(world) != 5:
        raise ValueError("The wall must use the simplified five-point border route")
    points = [Vector(point) - anchor for point in world]
    directions = [(b - a).normalized() for a, b in zip(points, points[1:])]
    normals = [Vector((-direction.y, direction.x)) for direction in directions]
    lengths = [(b - a).length for a, b in zip(points, points[1:])]
    miters = [normals[0]]
    for previous, following in zip(normals, normals[1:]):
        bisector = (previous + following).normalized()
        miters.append(bisector / bisector.dot(following))
    miters.append(normals[-1])
    cumulative = [0.0]
    for length in lengths:
        cumulative.append(cumulative[-1] + length)
    total_length = cumulative[-1]
    objects = []

    def xyz(point, height):
        return (point.x, point.y, height)

    def add(name, data, bevel=0):
        obj = data.object(name, material, bevel)
        obj["mdcw_landmark"] = "berlin_wall"
        objects.append(obj)
        return obj

    def at(distance, offset=0):
        distance = max(0.0, min(float(distance), total_length))
        index = next((i for i in range(len(lengths))
                      if distance <= cumulative[i + 1]), len(lengths) - 1)
        t = (distance - cumulative[index]) / lengths[index]
        point = points[index].lerp(points[index + 1], t)
        miter = miters[index].lerp(miters[index + 1], t)
        return point + miter * offset, directions[index], normals[index]

    def ribbon(name, lo, hi, bottom, top, tile, bevel=0):
        data = _NativeMesh()
        low = [point + miter * lo for point, miter in zip(points, miters)]
        high = [point + miter * hi for point, miter in zip(points, miters)]
        for i in range(len(points) - 1):
            a, b, c, d = low[i], low[i + 1], high[i + 1], high[i]
            data.face([xyz(a, top), xyz(b, top), xyz(c, top), xyz(d, top)], tile)
            data.face([xyz(d, bottom), xyz(c, bottom),
                       xyz(b, bottom), xyz(a, bottom)], tile)
            data.face([xyz(a, bottom), xyz(b, bottom), xyz(b, top), xyz(a, top)], tile)
            data.face([xyz(d, bottom), xyz(d, top), xyz(c, top), xyz(c, bottom)], tile)
        data.face([xyz(low[0], bottom), xyz(low[0], top),
                   xyz(high[0], top), xyz(high[0], bottom)], tile)
        data.face([xyz(low[-1], bottom), xyz(high[-1], bottom),
                   xyz(high[-1], top), xyz(low[-1], top)], tile)
        return add(name, data, bevel)

    def crown(name, offset, height, radius):
        data = _NativeMesh()
        sides = 10
        rings = []
        for point, miter in zip(points, miters):
            ring = []
            for i in range(sides):
                angle = 2 * math.pi * i / sides
                q = point + miter * (offset + radius * math.cos(angle))
                ring.append(xyz(q, height + radius * math.sin(angle)))
            rings.append(ring)
        for first, second in zip(rings, rings[1:]):
            for i in range(sides):
                j = (i + 1) % sides
                data.face([first[i], second[i], second[j], first[j]], 9, smooth=True)
        data.face(list(reversed(rings[0])), 9)
        data.face(rings[-1], 9)
        return add(name, data)

    # Every lengthwise part uses the same continuous mitered route.
    ribbon("Mauer_Grenzstreifen", .005, .50, -.09, .012, 6)
    ribbon("Mauer_Kontrollstreifen", .105, .215, .012, .015, 6)
    ribbon("Mauer_Patrouillenweg", .23, .35, .012, .016, 7)
    ribbon("Mauer_Westseite", .0025, .0575, -.09, .56, 9)
    ribbon("Mauer_Hinterland", .4425, .4775, -.09, .44, 9)
    crown("Mauer_Krone_West", .03, .56, .0275)
    crown("Mauer_Krone_Ost", .46, .44, .0175)

    # Same concrete material and very shallow geometry keep panel joints subtle.
    joints = _NativeMesh()
    distance = .23
    while distance < total_length - .1:
        point, direction, normal = at(distance, .0020)
        joints.box(xyz(point, .275), (.003, .002, .535), 9, direction)
        distance += .23
    add("Mauer_Betonplatten_Stossfugen", joints)

    # Separate editable light objects, with a compact combined mesh per light.
    distance = .40
    light_index = 1
    while distance < total_length - .15:
        point, direction, normal = at(distance, .385)
        head = point - normal * .075
        light = _NativeMesh()
        light.tube(xyz(point, .015), xyz(point, .71), .007, 5, 8)
        light.tube(xyz(point, .71), xyz(head, .735), .006, 5, 8)
        light.box(xyz(head, .732), (.052, .032, .022), 5, direction)
        light.box(xyz(head, .719), (.041, .024, .004), 4, direction)
        add("Mauer_Leuchte_%02d" % light_index, light)
        light_index += 1
        distance += .72

    # The low signal fence reads as context rather than another heavy wall.
    fence = _NativeMesh()
    distance = .15
    while distance < total_length - .1:
        point, direction, normal = at(distance, .409)
        fence.tube(xyz(point, .015), xyz(point, .30), .004, 5, 6)
        distance += .30
    for height in (.105, .195, .285):
        for i in range(len(points) - 1):
            start = points[i] + miters[i] * .409
            end = points[i + 1] + miters[i + 1] * .409
            fence.tube(xyz(start, height), xyz(end, height), .0022, 5, 6)
    add("Mauer_Signalzaun", fence)

    for index, distance in enumerate((total_length * .23, total_length * .73), 1):
        point, direction, normal = at(distance, .365)
        tower = _NativeMesh()
        tower.box(xyz(point, .37), (.09, .09, .74), 9, direction)
        tower.box(xyz(point, .75), (.18, .18, .05), 9, direction)
        tower.box(xyz(point, .84), (.171, .171, .13), 2, direction)
        tower.box(xyz(point, .91), (.18, .18, .025), 9, direction)
        tower.box(xyz(point, .937), (.205, .205, .03), 5, direction)
        # Fine corner uprights divide the observation cabin's four window faces.
        across = Vector((-direction.y, direction.x))
        for side in (-1, 1):
            for end in (-1, 1):
                corner = point + direction * (side * .082) + across * (end * .082)
                tower.box(xyz(corner, .84), (.014, .014, .14), 9, direction)
        add("Mauer_Wachturm_%02d" % index, tower, .002)

    objects[0]["route_world"] = [value for point in world for value in point]
    objects[0]["route_deviation_map_units"] = .5
    return objects
