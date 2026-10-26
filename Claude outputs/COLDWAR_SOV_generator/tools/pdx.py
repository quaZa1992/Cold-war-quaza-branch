# IMPERIA CW — Cold War: tools — pdx.
"""Minimal Paradox script parser: tokens -> nested list of (key, op, value, line).
Comments (# ... EOL, outside strings) are stripped but collected with their line numbers."""
import re

TOK = re.compile(r'"(?:[^"\\]|\\.)*"|[{}]|<=|>=|!=|==|[=<>]|[^\s{}=<>"#]+|#[^\n]*|\n')


def tokenize(text):
    toks, comments, line = [], [], 1
    for m in TOK.finditer(text):
        t = m.group(0)
        if t == "\n":
            line += 1
            continue
        if t.startswith("#"):
            comments.append((line, t))
            continue
        if t.startswith('"'):
            line += t.count("\n")
        toks.append((t, line))
    return toks, comments


def parse(text):
    toks, comments = tokenize(text)
    pos = [0]

    def block():
        items = []
        while pos[0] < len(toks):
            t, ln = toks[pos[0]]
            if t == "}":
                pos[0] += 1
                return items
            pos[0] += 1
            if t == "{":           # anonymous block
                items.append((None, None, block(), ln))
                continue
            if pos[0] < len(toks) and toks[pos[0]][0] in ("=", "<", ">", "<=", ">=", "!=", "=="):
                op = toks[pos[0]][0]
                pos[0] += 1
                v, vln = toks[pos[0]]
                pos[0] += 1
                if v == "{":
                    items.append((t, op, block(), ln))
                else:
                    items.append((t, op, v, ln))
            else:
                items.append((t, None, None, ln))   # bare value (list member)
        return items

    return block(), comments


def get(items, key, default=None):
    for k, op, v, ln in items:
        if k == key:
            return v
    return default


def getall(items, key):
    return [v for k, op, v, ln in items if k == key]


def bare(items):
    return [k for k, op, v, ln in items if op is None and k is not None]


def dump(items, ind=0):
    out = []
    for k, op, v, ln in items:
        if isinstance(v, list):
            out.append("\t" * ind + (f"{k} {op} " if k else "") + "{")
            out += dump(v, ind + 1)
            out.append("\t" * ind + "}")
        elif op is None:
            out.append("\t" * ind + str(k))
        else:
            out.append("\t" * ind + f"{k} {op} {v}")
    return out


def focus_records(path):
    text = open(path, encoding="utf-8-sig", errors="replace").read()
    tree, comments = parse(text)
    ft = None
    for k, op, v, ln in tree:
        if k == "focus_tree":
            ft = v
    assert ft is not None
    head = {}
    foci = []
    for k, op, v, ln in ft:
        if k == "focus":
            f = {"line": ln, "id": get(v, "id"), "icon": get(v, "icon")}
            f["x"] = float(get(v, "x", 0))
            f["y"] = float(get(v, "y", 0))
            f["rel"] = get(v, "relative_position_id")
            c = get(v, "cost", "0")
            try:
                f["cost"] = float(c)
            except ValueError:
                f["cost"] = c
            f["pre"] = [[x for x in getall(g, "focus")] for g in getall(v, "prerequisite")]
            f["mx"] = [x for g in getall(v, "mutually_exclusive") for x in getall(g, "focus")]
            sf = get(v, "search_filters")
            f["filters"] = bare(sf) if isinstance(sf, list) else []
            for key in ("allow_branch", "bypass", "available", "ai_will_do", "visible", "cancel_if_invalid",
                        "continue_if_invalid", "available_if_capitulated", "will_lead_to_war_with", "select_effect",
                        "complete_tooltip", "historical_ai", "cancel", "bypass_effect"):
                vv = get(v, key)
                f[key] = vv
            f["offsets"] = getall(v, "offset")
            f["raw"] = v
            foci.append(f)
        elif k == "shortcut":
            head.setdefault("shortcut", []).append({"name": get(v, "name"), "target": get(v, "target"),
                                                   "swf": get(v, "scroll_wheel_factor")})
        else:
            head.setdefault(k, []).append(v)
    return head, foci, comments


def resolve_abs(foci):
    by = {f["id"]: f for f in foci}
    memo = {}

    def A(i, stack=()):
        if i in memo:
            return memo[i]
        f = by[i]
        if f["rel"] and f["rel"] in by and f["rel"] not in stack:
            ax, ay = A(f["rel"], stack + (i,))
            r = (ax + f["x"], ay + f["y"])
        else:
            r = (f["x"], f["y"])
        memo[i] = r
        return r
    for f in foci:
        f["ax"], f["ay"] = A(f["id"])
    return by
