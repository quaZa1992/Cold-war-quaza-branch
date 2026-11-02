# IMPERIA COLD WAR — Chile compact layout overlay.
"""Apply the approved geometry-only compact layout for the Chile 1970 tree."""
from __future__ import annotations

from copy import deepcopy


def apply_layout(data):
    """Return a deep-copied design with section geometry compacted into 3 bands.

    Focuses retain their section-internal shape and anchor IDs. Only each
    section's absolute x/y origin moves, so prerequisite and exclusion data
    remain untouched.
    """
    result = deepcopy(data)
    groups = {group["id"]: group for group in result["groups"]}
    nodes_by_group = {group_id: [] for group_id in groups}
    for node in result["nodes"]:
        nodes_by_group[node["group"]].append(node)

    # Five columns per band keep the full card bounds compact. Rows are ordered
    # by institutional/political programme; the two tall policy branches sit
    # beside peers in their bands rather than extending a second bank below.
    bands = [
        ["republic", "development", "defence", "pdc", "pn"],
        ["pr", "ps", "pcch", "mapu", "diplomacy"],
        ["dr", "padena", "gremial", "mir", "military"],
    ]
    gap = 2
    band_gap = 2

    # Work from full focus-node bounds, not group labels or assumed widths.
    boxes = {}
    for group_id, nodes in nodes_by_group.items():
        if not nodes:
            raise ValueError(f"empty layout group: {group_id}")
        boxes[group_id] = (
            min(node["x"] for node in nodes),
            max(node["x"] for node in nodes),
            min(node["y"] for node in nodes),
            max(node["y"] for node in nodes),
        )
    if {group_id for band in bands for group_id in band} != set(groups):
        raise ValueError("layout bands must contain every group exactly once")

    band_y = 0
    positions = {}
    for band in bands:
        band_height = max(boxes[group_id][3] - boxes[group_id][2] + 1 for group_id in band)
        cursor_x = 0
        for group_id in band:
            left, right, top, _bottom = boxes[group_id]
            dx = cursor_x - left
            dy = band_y - top
            positions[group_id] = (dx, dy)
            cursor_x += right - left + 1 + gap
        band_y += band_height + band_gap

    # Translate all nodes in a group, preserving their positions and anchors
    # relative to one another. Group metadata follows its anchor focus.
    for node in result["nodes"]:
        dx, dy = positions[node["group"]]
        node["x"] += dx
        node["y"] += dy

    node_by_id = {node["id"]: node for node in result["nodes"]}
    # The compiler emits dx/dy, not the absolute design coordinates. Rebuild
    # those offsets after every node has moved so the emitted tree resolves to
    # the compact absolute positions. Root focuses have no anchor offset.
    for node in result["nodes"]:
        anchor_id = node.get("anchor")
        if anchor_id:
            if anchor_id not in node_by_id:
                raise ValueError(f"missing focus anchor {anchor_id!r} for {node['id']}")
            anchor = node_by_id[anchor_id]
            node["dx"] = node["x"] - anchor["x"]
            node["dy"] = node["y"] - anchor["y"]
        else:
            node["dx"] = node["x"]
            node["dy"] = node["y"]

    for group_id, group in groups.items():
        anchor = node_by_id[group["anchor"]]
        group["x"] = anchor["x"]
        group["y"] = anchor["y"]

    result["meta"]["span"] = [
        min(node["x"] for node in result["nodes"]),
        max(node["x"] for node in result["nodes"]),
        min(node["y"] for node in result["nodes"]),
        max(node["y"] for node in result["nodes"]),
    ]
    # The panel proposal is in native 96x130 pixel coordinates. Keep its
    # horizontal origin and place it below the compact focus-card bounds.
    grid_height = result["meta"]["grid"][1]
    result["meta"]["continuous_panel_proposal"]["y"] = (
        result["meta"]["span"][3] + 2
    ) * grid_height
    result["meta"]["layout_revision"] = "compact_three_band"
    return result
