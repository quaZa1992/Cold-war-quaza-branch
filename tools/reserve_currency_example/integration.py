# IMPERIA COLD WAR — In-memory integration example; never writes native game files.
"""Build reviewable hooks from the CURRENT native MD providers, without activating them."""
from copy import deepcopy
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "tools/spain_1970_v2"))
from script_ast import parse, first, walk, emit

PREFIX = "COLDWAR_MON_"
UTILITIES = "common/scripted_effects/00_economic_system_utilities.txt"
BUDGET = "common/scripted_effects/00_budget_effects.txt"
MONEY = "common/scripted_effects/00_money_system.txt"
CURRENCY = "common/scripted_effects/00_currency_effects.txt"
DEBT_PROVIDERS = ("automated_debt_taker", "take_manual_debt_effect", "repay_manual_debt_effect", "ai_repay_debt")
PROVIDERS = {
    UTILITIES: (*DEBT_PROVIDERS, "increment_global_reserve_currency"),
    BUDGET: ("modify_treasury_effect", "modify_debt_effect"),
    MONEY: ("restructure_debt_after_financial_collapse", "calculate_debt_fx_factor", "calculate_additional_expense_rate"),
    CURRENCY: ("refresh_currency_inflation_effects", "calculate_reserve_roi_bonus"),
}


def script(path):
    return parse((ROOT / path).read_text(encoding="utf-8-sig"))


def call(name):
    return (PREFIX + name, "=", "yes")


def native_effects():
    effects, constants = {}, {}
    for path, names in PROVIDERS.items():
        tree = script(path)
        constants.update({k: v for k, _, v in tree if k.startswith("@")})
        for name in names:
            body = first(tree, name)
            if not isinstance(body, list):
                raise ValueError(f"Native provider missing: {path}: {name}")
            effects[name] = deepcopy(body)
    return effects, constants


def instrument_mutations(body):
    """Keep the native acceptance branch; commit BEFORE any native economy refresh."""
    result = []
    for key, op, value in body:
        changed = isinstance(value, list) and key in {
            "set_variable", "add_to_variable", "subtract_from_variable"
        } and any(k == "debt" for k, _, _ in value)
        if changed:
            result.extend([call("before_debt_change"), (key, op, deepcopy(value)), call("after_debt_change")])
        else:
            result.append((key, op, instrument_mutations(value) if isinstance(value, list) else value))
    return result


def route_active(custom, original):
    return [
        ("if", "=", [("limit", "=", [("has_country_flag", "=", PREFIX + "initialized")]), call(custom)]),
        ("else", "=", deepcopy(original)),
    ]


def budget_hook():
    return [("if", "=", [
        ("limit", "=", [("has_country_flag", "=", PREFIX + "initialized")]),
        call("calculate_transition_cost"),
        ("add_to_variable", "=", [("additional_expenses_rate", "=", PREFIX + "weekly_transition_cost")]),
    ])]


def month_serial_hook():
    return ("add_to_variable", "=", [("global." + PREFIX + "month_serial", "=", "1")])


def monthly_preview():
    """Insert in the current MD callback in memory; no second on_monthly or new world scan."""
    body = deepcopy(first(first(first(script("common/on_actions/MD_on_actions.txt"), "on_actions"), "on_monthly"), "effect"))
    globals_found, locals_found = 0, 0
    for i, (key, op, val) in enumerate(body):
        if key == "if" and first(val, "limit") == [("NOT", "=", [("has_global_flag", "=", "on_monthly_done")])]:
            val.insert(1, month_serial_hook())
            globals_found += 1
        if key == "calculate_currency_strength":
            body.insert(i + 1, call("monthly_once"))
            locals_found += 1
    assert (globals_found, locals_found) == (1, 1), "Native monthly anchor changed; review required"
    return body


def build():
    effects, constants = native_effects()
    for name in (*DEBT_PROVIDERS, "restructure_debt_after_financial_collapse"):
        effects[name] = instrument_mutations(effects[name])
    # Native ADD + CLAMP constitute one transaction. Never observe its negative intermediate.
    body = effects["modify_debt_effect"]
    clamp_index = next(i for i, (k, _, _) in enumerate(body) if k == "clamp_variable")
    effects["modify_debt_effect"] = [call("before_debt_change")] + body[:clamp_index + 1] + [call("after_debt_change")] + body[clamp_index + 1:]
    effects["calculate_debt_fx_factor"] = route_active("calculate_debt_fx", effects["calculate_debt_fx_factor"])
    effects["calculate_reserve_roi_bonus"] = route_active("refresh_derived", effects["calculate_reserve_roi_bonus"])
    effects["increment_global_reserve_currency"] = route_active("add_reserve_weight", effects["increment_global_reserve_currency"])
    body = effects["calculate_additional_expense_rate"]
    assert body[0] == ("set_variable", "=", [("additional_expenses_rate", "=", "0")])
    effects["calculate_additional_expense_rate"] = body[:1] + budget_hook() + body[1:]
    effects.update({k: v for k, _, v in script("tools/reserve_currency_example/runtime/common/scripted_effects/COLDWAR_MON_reserves.txt")})
    return effects, constants


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    effects, _ = build()
    # stdout only: this is a review example, not a live-file patch generator.
    print("# IMPERIA COLD WAR — Inactive integration preview, derived from current MD providers.")
    print(emit([(name, "=", effects[name]) for name in (
        "take_manual_debt_effect", "modify_debt_effect", "calculate_debt_fx_factor"
    )]))
