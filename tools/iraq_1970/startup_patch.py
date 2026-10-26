# IMPERIA CW — Cold War: iraq 1970 — startup patch.
"""Bounded IRQ runtime metadata repair; no focus reward replay or file writes.

Historical challenge-card seeding and their native static stages are owned by
runtime_design.py. This module only recovers delivery/programme metadata for an
existing 1970 save after the first real startup/daily country-scope callback.
There is deliberately no invented on_load on-action.
"""
from pathlib import Path
import json

from common import ROOT, P, block, parse, first, values, walk

REPAIR_EFFECT = P + "repair_completed_focus_metadata"
REPAIR_FLAG = P + "runtime_metadata_repaired_v1"
OUTPUT = "common/scripted_effects/COLDWAR_IRQ_1970_startup_patch.txt"


def generate(root: Path = ROOT) -> dict[str, str]:
    root = Path(root)
    from audit_design import load_design
    data = load_design()
    nodes = data["nodes"]
    body = []
    for node in nodes:
        if node.get('audit_retired'):continue
        fid = node["id"]
        # Implemented is the authoritative successful-transaction receipt.
        # package_earned alone is insufficient: a paid policy review can earn an
        # alternate programme without delivering that focus's physical project.
        delivered = [f"set_country_flag = {fid}_package_earned", f"clr_country_flag = {fid}_pending"]
        delivered += [f'set_country_flag = {d["id"]}_unlocked' for d in node["decisions"]]
        body.append(block("if", block("limit", f"has_country_flag = {fid}_implemented") + "\n".join(delivered)))
        body.append(block("else_if", block("limit", f"has_completed_focus = {fid}") + f"set_country_flag = {fid}_pending"))
        if node["budget_gdp_share"]:
            # Preserve a real positive invoice if only its quoting flag was
            # lost. Never invent a historical GDP quote or charge it here.
            body.append(block("if", block("limit", f"has_country_flag = {fid}_pending\nhas_variable = {fid}_invoice\ncheck_variable = {{ {fid}_invoice > 0 }}") + f"set_country_flag = {fid}_quoted"))

    seen = set()
    by_id = {n["id"]: n for n in nodes}
    for node in nodes:
        for other in node["mutually_exclusive"]:
            pair = tuple(sorted((node["id"], other)))
            if pair in seen:
                continue
            seen.add(pair)
            for chosen, alternative in (pair, pair[::-1]):
                selected = P + "policy_" + by_id[chosen]["group"] + "_" + by_id[chosen]["key"]
                opposite = P + "policy_" + by_id[alternative]["group"] + "_" + by_id[alternative]["key"]
                # Never overwrite a later paid programme review. If a modified
                # save completed both excluded focuses, their order is unknown;
                # leave the selection to the existing explicit review menu.
                gate = f"has_country_flag = {chosen}_implemented\nNOT = {{ has_completed_focus = {alternative} }}\nNOT = {{ has_country_flag = {selected} }}\nNOT = {{ has_country_flag = {opposite} }}"
                body.append(block("if", block("limit", gate) + f"set_country_flag = {selected}"))

    body.append(f"set_country_flag = {REPAIR_FLAG}")
    limit = f"COLDWAR_IRQ_campaign_active = yes\nNOT = {{ has_country_flag = {REPAIR_FLAG} }}"
    source = block(REPAIR_EFFECT, block("if", block("limit", limit) + "\n".join(body)))
    return {OUTPUT: source}


def self_test(root: Path = ROOT) -> dict:
    """Execute this small emitted AST; unsupported statements fail closed."""
    root = Path(root)
    rows = parse(generate(root)[OUTPUT])
    body = first(rows, REPAIR_EFFECT)
    forbidden = {"add_dynamic_modifier", "add_ideas", "add_timed_idea", "add_building_construction", "add_resource", "army_experience", "modify_treasury_effect", "modify_debt_effect", "set_variable", "set_temp_variable", "load_focus_tree"}
    assert not any(k in forbidden or k.startswith(P + "apply_") for k, _, _ in walk(rows))
    checks = ["Recovery emits no cash, debt, physical asset, research, literacy or focus-apply operation"]

    class World:
        def __init__(self):
            self.flags = set()
            self.completed = set()
            self.var = {}
            self.campaign = True

        def test(self, seq):
            def cond(k, op, v):
                if k == "NOT":
                    return not self.test(v)
                if k == "COLDWAR_IRQ_campaign_active":
                    return self.campaign == (v == "yes")
                if k == "has_country_flag":
                    return v in self.flags
                if k == "has_completed_focus":
                    return v in self.completed
                if k == "has_variable":
                    return v in self.var
                if k == "check_variable":
                    a, operation, b = v[0]
                    assert operation == ">"
                    return self.var.get(a, 0) > float(b)
                raise AssertionError("Unsupported recovery condition: " + k)
            return all(cond(k, op, v) for k, op, v in seq)

        def run(self, seq):
            taken = False
            for k, _, v in seq:
                if k in ("if", "else_if"):
                    if k == "if":
                        taken = False
                    if not taken and self.test(first(v, "limit", [])):
                        self.run([r for r in v if r[0] != "limit"])
                        taken = True
                elif k == "set_country_flag":
                    self.flags.add(v)
                    taken = False
                elif k == "clr_country_flag":
                    self.flags.discard(v)
                    taken = False
                else:
                    raise AssertionError("Unsupported recovery effect: " + k)

        def call(self):
            self.run(body)

    data = json.loads((root / "tools/iraq_1970/approved_iraq.json").read_text(encoding="utf-8-sig"))
    nodes = data["nodes"]
    source = next(n for n in nodes if n["decisions"])
    fid = source["id"]
    w = World(); w.completed.add(fid); w.flags.update({fid + "_implemented", fid + "_pending"}); w.call()
    assert fid + "_package_earned" in w.flags and fid + "_pending" not in w.flags
    assert all(d["id"] + "_unlocked" in w.flags for d in source["decisions"])
    checks.append("A successful existing receipt restores programme/decision metadata without replaying its transaction")
    before = set(w.flags); w.call(); assert w.flags == before
    checks.append("Repeated recovery is idempotent")
    funded = next(n for n in nodes if n["budget_gdp_share"])
    fid = funded["id"]
    w = World(); w.completed.add(fid); w.var[fid + "_invoice"] = 2.75; w.call()
    assert fid + "_pending" in w.flags and fid + "_quoted" in w.flags
    assert fid + "_implemented" not in w.flags and fid + "_package_earned" not in w.flags
    assert w.var[fid + "_invoice"] == 2.75
    checks.append("Completed but undelivered focus remains pending and preserves its real positive frozen invoice")
    w = World(); w.completed.add(fid); w.call()
    assert fid + "_pending" in w.flags and fid + "_quoted" not in w.flags and not w.var
    checks.append("A missing historical invoice is not fabricated")
    w = World(); w.flags.add(fid + "_package_earned"); w.completed.add(fid); w.call()
    assert fid + "_implemented" not in w.flags
    checks.append("Policy-review package evidence cannot be mistaken for a paid physical delivery")
    choice = next(n for n in nodes if n["mutually_exclusive"])
    fid, alternative = choice["id"], choice["mutually_exclusive"][0]
    other = next(n for n in nodes if n["id"] == alternative)
    selected = P + "policy_" + choice["group"] + "_" + choice["key"]
    opposite = P + "policy_" + other["group"] + "_" + other["key"]
    w = World(); w.completed.add(fid); w.flags.add(fid + "_implemented"); w.call()
    assert selected in w.flags and opposite not in w.flags
    checks.append("A uniquely delivered excluded choice recovers its absent programme selection")
    w = World(); w.completed.add(fid); w.flags.update({fid + "_implemented", opposite}); w.call()
    assert opposite in w.flags and selected not in w.flags
    checks.append("A later explicitly reviewed policy selection is preserved")
    w = World(); w.completed.update({fid, alternative}); w.flags.update({fid + "_implemented", alternative + "_implemented"}); w.call()
    assert selected not in w.flags and opposite not in w.flags
    checks.append("A save with both excluded completions does not invent their chronological selection")
    w = World(); w.campaign = False; w.completed.add(fid); w.flags.add(fid + "_implemented"); before = set(w.flags); w.call()
    assert w.flags == before
    checks.append("Foreign/later-scenario callers cannot write recovery metadata")
    return {"passed": len(checks), "checks": checks, "limitations": "Emitted metadata AST only; native history preview, startup/daily engine callbacks and save loading still require a game check."}


if __name__ == "__main__":
    print(json.dumps(self_test(), indent=2))
