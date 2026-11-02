# IMPERIA COLD WAR — Strict test interpreter for the prototype and selected native MD paths.
"""This executes script AST, but does not emulate the HOI4 engine or prove MP synchronisation."""
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP
from copy import deepcopy
from integration import build, script, first, PREFIX

D = Decimal
ZERO = D(0)
QUANTUM = D("0.00001")


@dataclass
class Country:
    variables: dict = field(default_factory=dict)
    flags: dict = field(default_factory=dict)
    political_power: Decimal = D(200)
    missions: set = field(default_factory=set)
    ideas: set = field(default_factory=set)
    dynamic_modifiers: set = field(default_factory=set)
    refreshes: int = 0


class Model:
    def __init__(self, quantize=False):
        self.effects, self.constants = build()
        self.triggers = {k: v for k, _, v in script("tools/reserve_currency_example/runtime/common/scripted_triggers/COLDWAR_MON_reserves.txt")}
        self.globals = {PREFIX + "month_serial": D(0), "proj_roi_usd": D("0.1"), "proj_trade_usd": D("0.2")}
        self.temp = {}
        self.day = 0
        self.operations = 0
        self.quantize = quantize

    def rounded(self, value):
        return value.quantize(QUANTUM, rounding=ROUND_HALF_UP) if self.quantize else value

    def value(self, country, expr):
        if isinstance(expr, list):
            out = ZERO
            for key, _, val in expr:
                if key == "value": out = self.value(country, val)
                elif key == "add": out += self.value(country, val)
                elif key == "subtract": out -= self.value(country, val)
                elif key == "multiply": out *= self.value(country, val)
                elif key == "divide": out /= self.value(country, val)
                elif key == "clamp": out = self.clamped(country, out, val)
                else: raise AssertionError(f"Unsupported inline math: {key}")
            return out
        try: return D(expr)
        except Exception: pass
        if expr.startswith("@"): return self.value(country, self.constants[expr])
        if expr.startswith("global."): return self.globals.get(expr[7:], ZERO)
        return self.temp.get(expr, country.variables.get(expr, ZERO))

    def flag(self, country, name):
        expiry = country.flags.get(name, -1)
        return expiry is None or expiry > self.day

    def trigger(self, country, key, value, operator="="):
        self.operations += 1
        if key in ("AND", "limit", "custom_trigger_tooltip"):
            return all(self.trigger(country, k, v, o) for k, o, v in value if k != "tooltip")
        if key == "OR": return any(self.trigger(country, k, v, o) for k, o, v in value)
        if key == "NOT": return not all(self.trigger(country, k, v, o) for k, o, v in value)
        if key == "check_variable":
            if first(value, "var") is not None:
                left, right = first(value, "var"), first(value, "value")
                op = {"equals": "=", "greater_than_or_equals": ">=", "less_than_or_equals": "<="}.get(first(value, "compare"), first(value, "compare"))
            else: left, op, right = value[0]
            a, b = self.value(country, left), self.value(country, right)
            return {"=": a == b, ">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b, "!=": a != b}[op]
        if key == "has_country_flag": return self.flag(country, value)
        if key == "has_variable": return value in country.variables or value in self.temp
        if key == "has_political_power": return country.political_power >= self.value(country, value)
        if key == "political_power":
            a, b = country.political_power, self.value(country, value)
            return {"=": a >= b, ">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[operator]
        if key == "has_active_mission": return value in country.missions
        if key == "has_idea": return value in country.ideas
        if key == "has_dynamic_modifier": return first(value, "modifier") in country.dynamic_modifiers
        if key == "is_debug": return value == "no"
        if key in self.triggers:
            answer = all(self.trigger(country, k, v, o) for k, o, v in self.triggers[key])
            return answer if value == "yes" else not answer
        raise AssertionError(f"Unsupported trigger: {key}")

    def clamped(self, country, current, body):
        minimum, maximum = first(body, "min"), first(body, "max")
        if minimum is not None: current = max(current, self.value(country, minimum))
        if maximum is not None: current = min(current, self.value(country, maximum))
        return current

    def execute(self, country, rows):
        branch = False
        for key, _, value in rows:
            self.operations += 1
            if key in ("if", "else_if", "else"):
                if key == "if": branch = False
                take = not branch and (key == "else" or self.trigger(country, "limit", first(value, "limit", [])))
                if take:
                    branch = True
                    self.execute(country, [(k, o, v) for k, o, v in value if k != "limit"])
                continue
            if key == "hidden_effect": self.execute(country, value)
            elif key == "set_country_flag":
                if isinstance(value, list): country.flags[first(value, "flag")] = self.day + int(self.value(country, first(value, "days")))
                else: country.flags[value] = None
            elif key == "clr_country_flag": country.flags.pop(value, None)
            elif key == "clear_variable": country.variables.pop(value, None)
            elif key == "add_political_power": country.political_power += self.value(country, value)
            elif key in ("clamp_variable", "clamp_temp_variable"):
                name = first(value, "var")
                target = self.temp if "temp" in key else country.variables
                target[name] = self.rounded(self.clamped(country, self.value(country, name), value))
            elif key in {"set_variable", "set_temp_variable", "add_to_variable", "add_to_temp_variable", "subtract_from_variable", "subtract_from_temp_variable", "multiply_variable", "multiply_temp_variable", "divide_variable", "divide_temp_variable"}:
                name, _, arg = value[0]
                target = self.globals if name.startswith("global.") else (self.temp if "temp" in key else country.variables)
                a, b = self.value(country, name), self.value(country, arg)
                if key.startswith("set_"): out = b
                elif key.startswith("add_"): out = a + b
                elif key.startswith("subtract_"): out = a - b
                elif key.startswith("multiply_"): out = a * b
                else: out = a / b
                target[name[7:] if name.startswith("global.") else name] = self.rounded(out)
            elif key == "ingame_update_setup":
                # The complete native economy/state/UI pipeline is outside this test interpreter.
                country.refreshes += 1
                self.execute(country, self.effects["calculate_debt_fx_factor"])
            elif key == "calculate_interest_rate": self.execute(country, self.effects["calculate_debt_fx_factor"])
            elif key == "remove_dynamic_modifier": country.dynamic_modifiers.discard(first(value, "modifier"))
            elif key in ("custom_effect_tooltip", "log", "update_money_dirty_variable"): pass
            elif key in self.effects: self.execute(country, self.effects[key])
            else: raise AssertionError(f"Unsupported effect: {key}")

    def run(self, country, effect, temp=None):
        self.temp = {k: D(str(v)) for k, v in (temp or {}).items()}
        self.execute(country, self.effects[effect])
        self.temp = {}

    def save(self, countries):
        # Temp variables deliberately omitted, as in the runtime contract.
        return deepcopy((self.globals, self.day, countries))

    def load(self, snapshot):
        self.globals, self.day, countries = deepcopy(snapshot)
        self.temp = {}
        return countries
