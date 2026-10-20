"""Small lossless reader/writer for the PDX binary asset tree used by HOI4."""
from dataclasses import dataclass, field
from pathlib import Path
import struct
import numpy as np


@dataclass
class Property:
    name: str
    kind: str
    value: object


@dataclass
class Node:
    name: str
    children: list = field(default_factory=list)

    def nodes(self, name):
        return [c for c in self.children if isinstance(c, Node) and c.name == name]

    def prop(self, name):
        return next(c for c in self.children if isinstance(c, Property) and c.name == name)


def read(path):
    data = Path(path).read_bytes()
    assert data[:4] == b"@@b@"
    root = Node("")
    stack = [root]
    at = 4
    while at < len(data):
        if data[at] == 91:
            depth = 0
            while data[at] == 91:
                depth += 1
                at += 1
            end = data.index(0, at)
            node = Node(data[at:end].decode())
            stack = stack[:depth]
            stack[-1].children.append(node)
            stack.append(node)
            at = end + 1
        else:
            assert data[at] == 33, (at, data[at:at+40])
            size = data[at + 1]
            name = data[at+2:at+2+size].decode()
            at += size + 2
            kind = chr(data[at])
            count = struct.unpack_from("<I", data, at+1)[0]
            at += 5
            if kind in "fi":
                value = np.frombuffer(data, dtype="<f4" if kind == "f" else "<i4", count=count, offset=at).copy()
                at += count * 4
            elif kind == "s":
                value = []
                for _ in range(count):
                    length = struct.unpack_from("<I", data, at)[0]
                    at += 4
                    value.append(data[at:at+length])
                    at += length
            else:
                raise ValueError((kind, at))
            stack[-1].children.append(Property(name, kind, value))
    return root


def encode(root):
    out = bytearray(b"@@b@")
    def visit(node, depth):
        if depth:
            out.extend(b"[" * depth + node.name.encode() + b"\0")
        for item in node.children:
            if isinstance(item, Node):
                visit(item, depth+1)
            else:
                name = item.name.encode()
                out.extend(b"!" + bytes([len(name)]) + name + item.kind.encode())
                out.extend(struct.pack("<I", len(item.value)))
                if item.kind == "s":
                    for value in item.value:
                        out.extend(struct.pack("<I", len(value)) + value)
                else:
                    out.extend(np.asarray(item.value, dtype="<f4" if item.kind == "f" else "<i4").tobytes())
    visit(root, 0)
    return bytes(out)


def write(path, root):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_bytes(encode(root))
    temporary.replace(path)


def meshes(root):
    for obj in root.nodes("object"):
        for shape in obj.children:
            if isinstance(shape, Node):
                for mesh in shape.nodes("mesh"):
                    yield shape.name, mesh


def bounds(mesh):
    p = mesh.prop("p").value.reshape(-1, 3)
    low, high = p.min(axis=0), p.max(axis=0)
    center = (low+high)/2
    sphere = np.r_[center, np.linalg.norm(p-center, axis=1).max()]
    try:
        mesh.prop("boundingsphere").value = sphere
    except StopIteration:
        pass
    aabb = mesh.nodes("aabb")[0]
    aabb.prop("min").value = low
    aabb.prop("max").value = high
