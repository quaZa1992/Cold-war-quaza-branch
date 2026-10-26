# IMPERIA CW — Cold War: berlin landmarks — border.
"""Trace the actual shared Berlin province edges with East Berlin on the right."""
from collections import Counter
import numpy as np
from PIL import Image


EAST_RGB = (86, 99, 46)
WEST_RGB = (167, 217, 90)


def shared_edges(path):
    image = np.asarray(Image.open(path).convert('RGB'))
    height, width = image.shape[:2]
    edges = []
    ys, xs = np.where(np.all(image == EAST_RGB, axis=2))
    for y, x in zip(ys, xs):
        z = height - int(y) - 1
        x = int(x)
        for dx, dy, a, b in [
            (-1, 0, (x, z+1), (x, z)),
            (1, 0, (x+1, z), (x+1, z+1)),
            (0, -1, (x+1, z+1), (x, z+1)),
            (0, 1, (x, z), (x+1, z)),
        ]:
            if 0 <= x+dx < width and 0 <= y+dy < height:
                if tuple(image[y+dy, x+dx]) == WEST_RGB:
                    edges.append((a, b))
    return edges


def boundary_path(path):
    edges = shared_edges(path)
    starts = Counter(a for a, b in edges)
    ends = Counter(b for a, b in edges)
    first = list((starts - ends).elements())
    assert len(first) == 1, 'Expected one connected open Berlin sector boundary'
    following = dict(edges)
    assert len(following) == len(edges), 'Branched Berlin sector boundary'
    chain = [first[0]]
    while chain[-1] in following:
        chain.append(following.pop(chain[-1]))
    assert not following and len(chain) == len(edges)+1
    # Keep only actual direction changes; consecutive collinear pixel edges merge.
    result = [chain[0]]
    for a, b, c in zip(chain, chain[1:], chain[2:]):
        u, v = np.subtract(b, a), np.subtract(c, b)
        if u[0]*v[1] != u[1]*v[0] or np.dot(u, v) <= 0:
            result.append(b)
    result.append(chain[-1])
    return np.asarray(result, dtype=float)
