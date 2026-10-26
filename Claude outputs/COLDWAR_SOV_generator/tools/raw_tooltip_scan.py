# IMPERIA CW — Cold War: tools — raw tooltip scan.
# COLDWAR | Finds internal names that the game would print raw in tooltips (flags, variables) in player-visible blocks
# of the generated output. Run from the generator folder after cw_build.py: python3 tools/raw_tooltip_scan.py
import os, re, sys, glob, collections, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx   # tools/pdx.py: minimal Paradox script parser

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out")


def load(pattern):
    res = {}
    for f in glob.glob(os.path.join(OUT, pattern)):
        items, _ = pdx.parse(open(f, encoding="utf-8-sig").read())
        res[f] = items
    return res


SE, ST = {}, {}
for f, items in load("common/scripted_effects/COLDWAR_*.txt").items():
    for k, op, v, ln in items:
        if isinstance(v, list):
            SE[k] = v
for f, items in load("common/scripted_triggers/COLDWAR_*.txt").items():
    for k, op, v, ln in items:
        if isinstance(v, list):
            ST[k] = v

FLAG_T = {"has_country_flag", "has_global_flag", "has_state_flag"}
VAR_T = {"check_variable", "has_variable"}
VAR_E = {"set_variable", "add_to_variable", "subtract_from_variable", "multiply_variable", "divide_variable", "clamp_variable", "round_variable"}
FLAG_E = {"set_country_flag", "clr_country_flag", "set_global_flag", "clr_global_flag"}
HITS = collections.defaultdict(set)   # (kind, name) -> set(context)


def name_of(v):
    if isinstance(v, list):
        for k, op, vv, ln in v:
            if k in ("flag", "var") and isinstance(vv, str):
                return vv
            if k and k not in ("value", "days", "min", "max", "tooltip") and k.startswith(("COLDWAR", "global.COLDWAR")):
                return k
        # check_variable = { X > Y }
        for k, op, vv, ln in v:
            if k and not isinstance(vv, list):
                return k
        return None
    return v


def has_tooltip(v):
    return isinstance(v, list) and any(k == "tooltip" for k, *_ in v)


def walk_trigger(items, ctx, seen=()):
    for k, op, v, ln in items:
        if k in ("custom_trigger_tooltip", "hidden_trigger"):
            continue
        if k in FLAG_T:
            HITS[("flag", name_of(v))].add(ctx)
        elif k in VAR_T:
            n = name_of(v)
            if n:
                HITS[("var", n)].add(ctx)
        elif k in ST and v == "yes" and k not in seen:
            walk_trigger(ST[k], ctx + f" > {k}", seen + (k,))
        elif isinstance(v, list):
            walk_trigger(v, ctx, seen)


def walk_effect(items, ctx, seen=()):
    for k, op, v, ln in items:
        if k in ("hidden_effect", "limit", "custom_effect_tooltip", "random_list") and k != "random_list":
            continue
        if k in FLAG_E:
            HITS[("eflag", name_of(v))].add(ctx)
        elif k in VAR_E:
            n = name_of(v)
            if n and not has_tooltip(v):
                HITS[("evar", n)].add(ctx)
        elif k in SE and v == "yes" and k not in seen:
            walk_effect(SE[k], ctx + f" > {k}", seen + (k,))
        elif isinstance(v, list):
            walk_effect(v, ctx, seen)


# foci
for f, items in load("common/national_focus/COLDWAR_*.txt").items():
    blocks = []
    for k, op, v, ln in items:
        if k == "focus_tree":
            blocks += [(kk, vv) for kk, oo, vv, ll in v if kk in ("focus", "shared_focus", "joint_focus") and isinstance(vv, list)]
        elif k in ("joint_focus", "shared_focus") and isinstance(v, list):
            blocks.append((k, v))
    for kind, b in blocks:
        fid = pdx.get(b, "id")
        for k, op, v, ln in b:
            if k in ("available", "bypass"):
                walk_trigger(v, f"focus {fid} {k}")
            elif k and k.startswith("completion_reward"):
                walk_effect(v, f"focus {fid} reward")
# decisions and missions
for f, items in load("common/decisions/COLDWAR_*.txt").items():
    for cat, op, decs, ln in items:
        for d, op2, b, ln2 in decs:
            if not isinstance(b, list):
                continue
            for k, op, v, ln in b:
                if k == "available":
                    walk_trigger(v, f"decision {d} available")
                elif k in ("complete_effect", "remove_effect", "timeout_effect"):
                    walk_effect(v, f"decision {d} {k}")
# events: option effects (not hidden events)
for f, items in load("events/COLDWAR_*.txt").items():
    for k, op, v, ln in items:
        if k not in ("country_event", "news_event") or pdx.get(v, "hidden") == "yes":
            continue
        eid = pdx.get(v, "id")
        for kk, oo, vv, ll in v:
            if kk == "option":
                walk_effect([x for x in vv if x[0] not in ("name", "trigger", "ai_chance")], f"event {eid} option")

kinds = collections.Counter(k for k, n in HITS)
REPORT = {f"{k}:{n}": sorted(c)[:3] + ([f"... {len(c)} contexts"] if len(c) > 3 else [])
          for (k, n), c in sorted(HITS.items(), key=lambda x: (x[0][0], str(x[0][1])))}

# which names have no localisation (ours or MD's)?
MDLOC = set()
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from cw_common import MOD
for f in glob.glob(os.path.join(MOD, "localisation/english/**/*.yml"), recursive=True):
    if "COLDWAR_SOV" in f or "COLDWAR_UNI" in f:
        continue
    for l in open(f, encoding="utf-8-sig", errors="replace"):
        m = re.match(r"^\s+([^\s:#]+):\d*\s", l)
        if m:
            MDLOC.add(m.group(1))
OURLOC = set()
for f in glob.glob(os.path.join(OUT, "localisation/english/*.yml")):
    for l in open(f, encoding="utf-8-sig"):
        m = re.match(r"^\s+([^\s:#]+):\d*\s", l)
        if m:
            OURLOC.add(m.group(1))
MISSING = sorted({(k, n.replace("global.", "")) for (k, n) in HITS if n and n.replace("global.", "") not in MDLOC | OURLOC})
if __name__ == "__main__":
    print(kinds)
    print("missing loc:", len(MISSING), collections.Counter(k for k, n in MISSING))
    for k, n in MISSING:
        if k in ("flag", "var") or not n.startswith("COLDWAR"):
            print(" ", k, n)
