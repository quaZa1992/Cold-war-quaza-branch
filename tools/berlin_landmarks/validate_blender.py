"""Read-only checks of Blender-exported Berlin landmarks and their placement.

Only validation_report_blender.json is written. Source files and game assets are
never repaired or rewritten by this validator.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import sys

import numpy as np
from PIL import Image

from border import EAST_RGB, boundary_path, shared_edges
from pdx import Property, encode, meshes, read


TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[1]
OUT = ROOT / "gfx/models/buildings/landmarks"
TEXTURES = {
    "diff": "mdcw_berlin_landmarks_diffuse.dds",
    "n": "mdcw_berlin_landmarks_normal.dds",
    "spec": "mdcw_berlin_landmarks_specular.dds",
}
MODELS = {
    "landmark_berlin_tv_tower.mesh": "mdcw_berlin_tv_tower",
    "landmark_berlin_tv_tower_destroyed.mesh": "mdcw_berlin_tv_tower",
    "landmark_berlin_wall.mesh": "landmark_berlin_wall",
    "landmark_berlin_wall_destroyed.mesh": "landmark_berlin_wall",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def numeric_properties(node):
    for child in node.children:
        if isinstance(child, Property):
            if child.kind in "fi":
                yield child
        else:
            yield from numeric_properties(child)


def decoded(prop):
    return [v.rstrip(b"\0").decode("utf-8") for v in prop.value]


def check_mesh(path, expected_shape):
    tree = read(path)
    require(encode(tree) == path.read_bytes(), f"{path.name}: binary round trip failed")
    for prop in numeric_properties(tree):
        require(np.isfinite(prop.value).all(), f"{path.name}: nonfinite {prop.name}")
    found = list(meshes(tree))
    require(len(found) == 1, f"{path.name}: expected one joined shape/material, got {len(found)}")
    shape, mesh = found[0]
    require(shape == expected_shape, f"{path.name}: unexpected shape {shape}")
    p = mesh.prop("p").value.reshape(-1, 3)
    tri = mesh.prop("tri").value.reshape(-1, 3)
    n = mesh.prop("n").value.reshape(-1, 3)
    uv = mesh.prop("u0").value.reshape(-1, 2)
    tangent = mesh.prop("ta").value.reshape(-1, 4)
    require(len(p) > 0 and len(tri) > 0, f"{path.name}: empty geometry")
    require(tri.min() >= 0 and tri.max() < len(p), f"{path.name}: triangle index outside vertex array")
    require(len(p) == len(n) == len(uv) == len(tangent), f"{path.name}: vertex attribute counts differ")
    require(np.allclose(np.linalg.norm(n, axis=1), 1, atol=.015), f"{path.name}: nonunit normals")
    require(np.allclose(np.linalg.norm(tangent[:, :3], axis=1), 1, atol=.015), f"{path.name}: nonunit tangents")
    require(np.allclose(np.abs(tangent[:, 3]), 1, atol=.001), f"{path.name}: invalid tangent handedness")
    v = p[tri]
    cross = np.cross(v[:, 1] - v[:, 0], v[:, 2] - v[:, 0])
    cross_length = np.linalg.norm(cross, axis=1)
    require((cross_length > 1e-12).all(), f"{path.name}: degenerate triangles")
    mean_n = n[tri].mean(axis=1)
    alignment = np.einsum("ij,ij->i", cross, mean_n) / cross_length
    require((alignment > 1e-5).all(), f"{path.name}: triangle winding disagrees with vertex normals")
    aabbs = mesh.nodes("aabb")
    require(len(aabbs) == 1, f"{path.name}: missing unique bounds")
    require(np.allclose(aabbs[0].prop("min").value, p.min(axis=0), atol=1e-4), f"{path.name}: incorrect minimum bounds")
    require(np.allclose(aabbs[0].prop("max").value, p.max(axis=0), atol=1e-4), f"{path.name}: incorrect maximum bounds")
    sphere = mesh.prop("boundingsphere").value
    require(sphere.shape == (4,) and sphere[3] > 0, f"{path.name}: invalid bounding sphere")
    require((np.linalg.norm(p - sphere[:3], axis=1) <= sphere[3] + .001).all(), f"{path.name}: bounding sphere does not contain mesh")
    materials = mesh.nodes("material")
    require(len(materials) == 1, f"{path.name}: expected one material")
    material = materials[0]
    require(decoded(material.prop("shader")) == ["PdxMeshAdvanced"], f"{path.name}: unexpected shader")
    for slot, expected in TEXTURES.items():
        require(decoded(material.prop(slot)) == [expected], f"{path.name}: incorrect {slot} atlas")
        texture_path = path.parent / expected
        require(texture_path.is_file(), f"{path.name}: missing texture {expected}")
        with Image.open(texture_path) as image:
            image.verify()
    return p, {
        "shape": shape,
        "vertices": len(p),
        "triangles": len(tri),
        "min": p.min(axis=0).tolist(),
        "max": p.max(axis=0).tolist(),
        "minimum_normal_alignment": float(alignment.min()),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def samples(segments, step=.01):
    result = []
    for a, b in segments:
        count = max(2, int(np.ceil(np.linalg.norm(b - a) / step)) + 1)
        result.append(a + np.linspace(0, 1, count)[:, None] * (b - a))
    return np.concatenate(result)


def distance_to_segments(points, segments):
    distances = []
    for a, b in segments:
        delta = b - a
        t = np.clip((points - a) @ delta / (delta @ delta), 0, 1)
        distances.append(np.linalg.norm(points - a - t[:, None] * delta, axis=1))
    return np.min(distances, axis=0)


def check_path(config):
    path = np.asarray(config["wall_world"], dtype=float)
    require(path.ndim == 2 and path.shape[1] == 2 and 2 <= len(path) <= 5, "Wall path needs two to five control points")
    require(np.isfinite(path).all(), "Wall control points must be finite")
    delta = np.diff(path, axis=0)
    require((np.linalg.norm(delta, axis=1) > 0).all(), "Wall path contains duplicate points")
    raw = boundary_path(ROOT / "map/provinces.bmp")
    require(np.allclose(path[[0, -1]], raw[[0, -1]], atol=1e-6), "Wall path does not retain actual border endpoints")
    # A smooth diagonal follows the centre of the raster staircase. Measure both
    # directions so shortcuts and omitted border sections cannot pass unnoticed.
    actual = np.asarray(shared_edges(ROOT / "map/provinces.bmp"), dtype=float)
    smooth = np.stack((path[:-1], path[1:]), axis=1)
    smooth_error = float(distance_to_segments(samples(smooth), actual).max())
    border_error = float(distance_to_segments(samples(actual), smooth).max())
    require(max(smooth_error, border_error) <= .501, f"Smoothed border deviation exceeds 0.501 map units: {smooth_error}, {border_error}")
    return {
        "control_points": path.tolist(),
        "control_point_count": len(path),
        "shared_unit_edges": len(actual),
        "path_to_border_maximum": smooth_error,
        "border_to_path_maximum": border_error,
        "length": float(np.linalg.norm(delta, axis=1).sum()),
        "sample_step": .01,
    }


def source_hash_records(value, name=""):
    """Accept filename-keyed manifests and explicit source/path/hash records."""
    if isinstance(value, dict):
        paths = [name]
        paths.extend(str(value[k]) for k in ("source", "path", "blend", "source_path") if k in value and isinstance(value[k], str))
        hashes = [value[k] for k in ("sha256", "source_sha256", "source_hash", "blend_sha256") if isinstance(value.get(k), str)]
        for path in paths:
            if path.lower().endswith(".blend"):
                for digest in hashes:
                    yield Path(path).name, digest
        for key, child in value.items():
            if isinstance(child, str) and str(key).lower().endswith(".blend"):
                yield Path(str(key)).name, child
            else:
                yield from source_hash_records(child, str(key))
    elif isinstance(value, list):
        for child in value:
            yield from source_hash_records(child, name)


def check_sources():
    manifest_path = TOOLS / "blender_export.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    require(bool(manifest.get("blender_version")), "Blender export manifest has no Blender version")
    require(bool(manifest.get("exporter")), "Blender export manifest has no exporter identity")
    records = list(source_hash_records(manifest))
    result = {}
    for name in ("tv_tower.blend", "berlin_wall.blend"):
        path = TOOLS / "source" / name
        require(path.is_file(), f"Missing Blender source {name}")
        data = path.read_bytes()
        require(data.startswith(b"BLENDER"), f"{name}: missing uncompressed Blender file header")
        require(len(data) > 12, f"{name}: truncated Blender file")
        digest = hashlib.sha256(data).hexdigest()
        require((name, digest) in records, f"{name}: manifest source SHA256 is missing or stale")
        result[name] = {"bytes": len(data), "header": data[:12].decode("ascii"), "sha256": digest}
    return {"blender_version": manifest["blender_version"], "exporter": manifest["exporter"], "sources": result}


def check_tower_geometry(points, config):
    height = float(config.get("tower_height", config.get("towerheight", 365)))
    center_y = float(config.get("sphere_center", 213.78))
    radius = float(config.get("sphere_radius", 16))
    require(np.isclose(points[:, 1].max(), height, atol=.001), "Tower height differs from the configured model height")
    relative = points - [0, center_y, 0]
    horizontal = np.linalg.norm(relative[:, [0, 2]], axis=1)
    in_globe = (np.abs(relative[:, 1]) <= radius + .001) & (horizontal >= .8 * radius)
    require(in_globe.sum() >= 24, "Tower does not contain a recognisable spherical shell")
    globe_radii = np.linalg.norm(relative[in_globe], axis=1)
    # Window seams and narrow metal trims may sit just above the shell. Require
    # an actual radius-16 sphere while permitting those deliberate details.
    sphere_vertices = globe_radii[np.abs(globe_radii - radius) <= .001]
    require(len(sphere_vertices) >= 24, "Tower sphere vertices do not match the configured centre and radius")
    require(globe_radii.max() <= radius + .35, "Tower globe exceeds its configured spherical envelope")
    require(np.isclose(np.ptp(points[in_globe, 0]), radius * 2, atol=.35), "Tower globe width is incorrect")
    require(np.isclose(np.ptp(points[in_globe, 2]), radius * 2, atol=.35), "Tower globe depth is incorrect")
    return {"height": height, "sphere_center_y": center_y, "sphere_radius": radius, "sphere_vertices_within_0_001": len(sphere_vertices), "maximum_globe_radius": float(globe_radii.max())}


def check_placement(points, config):
    anchor = np.asarray(config["tower_anchor"], dtype=float)
    scale = float(config["tower_scale"])
    require(np.isclose(scale, .014, atol=1e-8), "Tower display scale must be 0.014")
    buildings = (ROOT / "map/buildings.txt").read_text(encoding="utf-8-sig")
    found = re.findall(r"^45;berlin_tv_tower_spawn;([^;]+);([^;]+);([^;]+);", buildings, re.M)
    require(len(found) == 1, "Tower needs exactly one independent map spawn")
    x, y, z = map(float, found[0])
    require(np.allclose([x, z], anchor, atol=1e-6), "Tower map placement differs from configured anchor")
    wall = re.findall(r"^45;landmark_spawn;([^;]+);([^;]+);([^;]+);", buildings, re.M)
    require(len(wall) == 1, "Wall needs exactly one Berlin landmark spawn")
    require(np.allclose([float(wall[0][0]), float(wall[0][2])], config["wall_anchor"], atol=1e-6), "Wall map placement differs from configured anchor")
    provinces = np.asarray(Image.open(ROOT / "map/provinces.bmp").convert("RGB"))
    world = points[:, [0, 2]] * scale + anchor
    world = np.vstack((world, anchor))
    xs = np.floor(world[:, 0]).astype(int)
    ys = np.floor(provinces.shape[0] - world[:, 1]).astype(int)
    require(((xs >= 0) & (xs < provinces.shape[1]) & (ys >= 0) & (ys < provinces.shape[0])).all(), "Tower footprint outside province bitmap")
    require((provinces[ys, xs] == EAST_RGB).all(), "Tower footprint extends outside East Berlin")
    asset = (ROOT / "gfx/entities/mdcw_berlin_landmarks.asset").read_text(encoding="utf-8-sig")
    scales = [float(v) for v in re.findall(r"\bscale\s*=\s*([\d.]+)", asset)]
    require(len(scales) == 2 and np.allclose(scales, scale, atol=1e-8), "Both tower entities must use the configured display scale")
    require(re.search(r'clone\s*=\s*"building_landmark_spawn"\s+name\s*=\s*"building_berlin_tv_tower_spawn"', asset) is not None, "Independent tower spawn alias is missing")
    return {"tower_anchor": [x, z], "tower_ground_height": y, "tower_scale": scale, "tower_display_height": float(points[:, 1].max() * scale), "projected_footprint_inside_east_berlin": True, "wall_anchor": config["wall_anchor"]}


def check_reichstag():
    west = (ROOT / "history/states/1251-West Berlin.txt").read_text(encoding="utf-8-sig")
    require("landmark_berlin_reichstag = {" in west, "Original Reichstag landmark is missing")
    require("reichstag_coldwar" not in west, "Cold War Reichstag history override remains")
    for name in ("common/buildings/mdcw_berlin_landmarks.txt", "gfx/entities/mdcw_berlin_landmarks.asset", "gfx/entities/mdcw_berlin_landmarks.gfx"):
        text = (ROOT / name).read_text(encoding="utf-8-sig")
        require("reichstag_coldwar" not in text and "landmark_reichstag" not in text, f"Reichstag override remains in {name}")
    require(not list(OUT.glob("*reichstag*.mesh")), "Mod still overrides a Reichstag model")
    return "Original Reichstag entity/history retained; no local mesh override"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--game", type=Path, help="Accepted for compatibility; all DDS atlases must be local to the meshes")
    args = parser.parse_args()
    report = {"status": "FAIL", "validator": "validate_blender.py", "models": {}}
    try:
        config = json.loads((TOOLS / "config.json").read_text(encoding="utf-8-sig"))
        report["blender"] = check_sources()
        geometry = {}
        for name, shape in MODELS.items():
            geometry[name], report["models"][name] = check_mesh(OUT / name, shape)
        report["border"] = check_path(config)
        tower = geometry["landmark_berlin_tv_tower.mesh"]
        report["tower_geometry"] = check_tower_geometry(tower, config)
        report["placement"] = check_placement(tower, config)
        report["reichstag"] = check_reichstag()
        report["status"] = "PASS"
    except (ValueError, AssertionError, OSError, KeyError, IndexError, StopIteration) as error:
        report["error"] = str(error) or type(error).__name__
    destination = TOOLS / "validation_report_blender.json"
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{report['status']}: {report.get('error', 'Blender sources, binary meshes, materials, border smoothing, placement and Reichstag rollback verified.')}")
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
