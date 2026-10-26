# IMPERIA CW — Cold War: Guest Worker Administration
"""Validate guest-worker integration and execute its real script arithmetic.

Run from any directory with Python 3.12+. No game files are changed. The small
interpreter intentionally rejects unsupported operations: it is a regression
check for the authored scripts, not an alternative implementation of HOI4.
"""
from __future__ import annotations

import ast
from copy import deepcopy
from dataclasses import dataclass, field
from decimal import Decimal
import json
from pathlib import Path
import re
import struct
import sys

ROOT = Path(__file__).resolve().parents[2]
PARSER_PATH = ROOT / "tools/israel_1970/validate_content.py"
# Extract only the established parser's functions. Importing its module would
# execute another country's validation and require its unrelated dependencies.
parser_module = ast.parse(PARSER_PATH.read_text(encoding="utf-8"))
parser_functions = [n for n in parser_module.body
                    if isinstance(n, ast.FunctionDef)
                    and n.name in {"tokens", "parse", "values", "first", "walk"}]
parser_namespace = {"re": re}
exec(compile(ast.Module(body=parser_functions, type_ignores=[]),
             str(PARSER_PATH), "exec"), parser_namespace)
parse, values, first, walk = (parser_namespace[n]
                             for n in ("parse", "values", "first", "walk"))

ISSUES: list[str] = []
CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        ISSUES.append(message)


def read_script(relative):
    path = ROOT / relative
    check(path.is_file(), "Missing script: " + relative)
    if not path.is_file():
        return []
    try:
        return parse(path.read_text(encoding="utf-8-sig"))
    except AssertionError as error:
        ISSUES.append(relative + ": " + str(error))
        return []


D = lambda value: Decimal(str(value))


@dataclass
class State:
    population: Decimal = D(1_000_000)
    owner: str = "A"
    controller: str = "A"


@dataclass
class Country:
    tag: str
    variables: dict = field(default_factory=lambda: {"treasury": D(100), "population_total": D(10), "gdp_per_capita": D(2)})
    temporary: dict = field(default_factory=dict)
    flags: dict = field(default_factory=dict)
    flag_started: dict = field(default_factory=dict)
    ideas: set = field(default_factory=set)
    political_power: Decimal = D(1000)
    peace: bool = True
    # IMPERIA CW — Cold War: Native human/AI distinction for hard programme guards.
    is_ai: bool = False
    exists: bool = True
    states: list = field(default_factory=list)
    refreshes: int = 0
    dynamic_modifiers: set = field(default_factory=set)
    dynamic_refreshes: int = 0
    military_manpower: Decimal = D(250000)
    stability: Decimal = D("0.8")
    timed_ideas: dict = field(default_factory=dict)


class ScriptMachine:
    """Execute the subset used by the actual guest-worker effect/trigger ASTs."""

    def __init__(self, effects, triggers, events=None):
        self.effects = effects
        self.triggers = triggers
        self.countries = {tag: Country(tag) for tag in ("A", "B")}
        for tag, country in self.countries.items():
            country.states = [State(owner=tag, controller=tag)]
            country.ideas = {"mdcw_ni_overseas_employment_programme",
                             "mdcw_ni_guest_worker_recruitment_programme"}
        self.countries["A"].variables["gdp_per_capita"] = D(5)
        self.current = self.root = self.countries["A"]
        self.origin = self.countries["B"]
        self.previous = self.current
        self.previous_history = []
        self.targets = {}
        self.events = events or {}
        self.queue = []
        self.open_events = []
        self.delivered = []
        self.now = D(0)
        # Tests may inject observed engine side effects. This is not a model of
        # HOI4's conscription/recruitable-population recalculation internals.
        self.state_population_hook = None

    def substitute(self, text):
        if not isinstance(text, str):
            return text
        assert "$" not in text, "Runtime macro placeholders are not supported by the native helper protocol"
        return text.strip('"')

    def scope(self, name):
        name = self.substitute(name)
        if name.startswith("event_target:"):
            return self.targets.get(name.split(":", 1)[1])
        if name.startswith("var:"):
            number = self.get(name.split(":", 1)[1])
            return next((country for index, country in enumerate(self.countries.values(), 1)
                         if number == index), None)
        if name.startswith("PREV.") and all(part == "PREV" for part in name.split(".")):
            depth = len(name.split(".")) - 1
            return self.previous_history[-depth] if len(self.previous_history) >= depth else None
        if name in {"owner", "OWNER", "controller", "CONTROLLER"} and isinstance(self.current, State):
            tag = self.current.owner if name.lower() == "owner" else self.current.controller
            return self.countries.get(tag)
        return {"ROOT": self.root, "FROM": self.origin,
                "PREV": self.previous, "THIS": self.current,
                **self.countries}.get(name)

    def resolve_variable(self, name):
        name = self.substitute(name)
        if "." in name:
            parts = name.split(".")
            for boundary in range(len(parts) - 1, 0, -1):
                target = self.scope(".".join(parts[:boundary]))
                if target is not None:
                    return target, self.array_key(".".join(parts[boundary:]))
            raise AssertionError("Unknown variable scope: " + name)
        return self.current, self.array_key(name)

    def array_key(self, name):
        if "^" in name:
            base, index = name.rsplit("^", 1)
            if index != "num":
                name = base + "^" + str(int(self.get(index)))
        return name

    def get(self, name):
        name = self.substitute(name)
        try:
            return D(name)
        except Exception:
            pass
        country_scope = self.scope(name)
        if isinstance(country_scope, Country):
            return D(list(self.countries).index(country_scope.tag) + 1)
        country, key = self.resolve_variable(name)
        if isinstance(country, State):
            if key == "state_population":
                return country.population
            if key == "state_population_k":
                return country.population / 1000
            raise AssertionError("Unsupported state variable: " + key)
        if key in {"political_power", "has_political_power"}:
            return country.political_power
        if key in {"manpower", "manpower_k"}:
            return country.military_manpower / (1000 if key.endswith("_k") else 1)
        if key == "id":
            return D(list(self.countries).index(country.tag) + 1)
        # IMPERIA CW — Cold War: Native exported stability, in fractions of one.
        if key == 'stability': return country.stability
        if key.startswith("modifier@"):
            modifier = key.split("@", 1)[1]
            if modifier == "health_cost_multiplier_modifier":
                return country.variables.get("mdcw_gw_health_cost", D(0))
            if modifier == "bureaucracy_cost_multiplier_modifier":
                return country.variables.get("mdcw_gw_bureaucracy_cost", D(0)) + sum(
                    D(".05") for idea in ("mdcw_ni_guest_worker_recruitment_programme", "mdcw_ni_overseas_employment_programme") if idea in country.ideas)
            return D(0)
        return country.temporary.get(key, country.variables.get(key, D(0)))

    def expression(self, expression):
        if not isinstance(expression, list):
            return self.get(expression)
        result = D(0)
        for key, _, value in expression:
            if key == "value": result = self.expression(value)
            elif key == "add": result += self.expression(value)
            elif key == "subtract": result -= self.expression(value)
            elif key == "multiply": result *= self.expression(value)
            elif key == "divide":
                denominator = self.expression(value)
                assert denominator != 0, "Script divides by zero"
                result /= denominator
            elif key == "clamp": result = self.clamp(result, value)
            else: raise AssertionError("Unsupported expression: " + key)
        return result

    def clamp(self, number, body):
        if first(body, "min") is not None:
            number = max(number, self.expression(first(body, "min")))
        if first(body, "max") is not None:
            number = min(number, self.expression(first(body, "max")))
        return number

    def in_scope(self, scope, callback):
        assert scope is not None, "Missing event target or scope"
        old_current, old_previous = self.current, self.previous
        self.previous_history.append(old_previous)
        self.current, self.previous = scope, old_current
        try: return callback()
        finally:
            self.current, self.previous = old_current, old_previous
            self.previous_history.pop()

    def call(self, name, parameters=None, trigger=False):
        assert parameters is None, "Scripted helpers must use native no-argument '= yes' calls: " + name
        body = (self.triggers if trigger else self.effects)[name]
        return self.test(body) if trigger else self.execute(body)

    # IMPERIA CW — Cold War: Native scoped country flags, as used by MD investments.
    def flag_name(self, name):
        if '@' not in name:return name
        prefix,scope=name.rsplit('@',1)
        target=self.scope(scope)
        assert isinstance(target,Country),'Invalid scoped flag country: '+name
        return prefix+'@'+target.tag

    def compare(self, left, op, right):
        return {"=": left == right, ">": left > right,
                "<": left < right, "equals": left == right,
                "not_equals": left != right, "greater_than": left > right,
                "less_than": left < right, "greater_than_or_equals": left >= right,
                "less_than_or_equals": left <= right}[op]

    def test(self, body):
        results = []
        for key, op, value in body:
            key = self.substitute(key)
            if key in {"tooltip", "not_tooltip"}: continue
            if key in {"AND", "limit", "custom_trigger_tooltip", "hidden_trigger"}:
                answer = self.test(value)
            elif key == "OR": answer = any(self.test([node]) for node in value)
            elif key == "NOT": answer = not self.test(value)
            elif key == "always": answer = value == "yes"
            elif key == "exists":
                target = self.current if value in {"yes", "no"} else self.scope(value)
                answer = bool(target and target.exists)
                if value == "no": answer = not answer
            elif key == "has_war": answer = self.current.peace == (value == "no")
            elif key == "is_ai": answer = self.current.is_ai == (value == "yes")
            elif key == "tag": answer = self.current is self.scope(value)
            elif key == "state":
                assert isinstance(self.current, State), "State identity trigger evaluated outside native state scope"
                answer = self.current is self.scope(value)
            elif key == "has_idea": answer = value in self.current.ideas
            elif key == "is_in_array":
                name, _, item = value[0]
                answer = self.expression(item) in self.array_values(name)
            elif key == "any_of":
                name = first(value, "array")
                conditions = [node for node in value if node[0] not in {"array", "index", "value"}]
                answer = False
                for i, item in enumerate(self.array_values(name)):
                    self.current.temporary[first(value, "index", "index")] = D(i)
                    self.current.temporary[first(value, "value", "value")] = item
                    if self.test(conditions):
                        answer = True
                        break
            elif key in {"set_temp_variable", "divide_temp_variable", "multiply_temp_variable", "add_to_temp_variable", "subtract_from_temp_variable"}:
                self.execute([(key, op, value)])
                answer = True
            elif key == "has_dynamic_modifier":
                modifier = value if isinstance(value, str) else first(value, "modifier")
                answer = modifier in self.current.dynamic_modifiers
            elif key == "has_variable":
                answer = value in self.current.variables or value in self.current.temporary
            elif key == "has_country_flag":
                flag = self.flag_name(value if isinstance(value, str) else first(value, "flag"))
                answer = flag in self.current.flags
                if isinstance(value, list):
                    for test_key, comparison, target in value:
                        if test_key == "days":
                            answer = answer and self.compare(
                                self.now - self.current.flag_started.get(flag, D(0)),
                                comparison, self.expression(target))
                        elif test_key != "flag":
                            raise AssertionError("Unsupported flag comparison: " + test_key)
            elif key == "is_controlled_by": answer = self.current.controller == self.scope(value).tag
            elif key == "is_owned_by": answer = self.current.owner == self.scope(value).tag
            elif key in {"any_owned_state", "any_controlled_state"}:
                states = self.current.states
                if key == "any_owned_state": states = [s for s in states if s.owner == self.current.tag]
                else: states = [s for s in states if s.controller == self.current.tag]
                answer = any(self.in_scope(s, lambda: self.test(value)) for s in states)
            elif key == "check_variable":
                if first(value, "var") is not None:
                    answer = self.compare(self.get(first(value, "var")),
                                          first(value, "compare", "equals"),
                                          self.expression(first(value, "value")))
                else:
                    name, comparison, target = value[0]
                    answer = self.compare(self.get(name), comparison, self.expression(target))
            elif key in self.triggers: answer = self.call(key, value if isinstance(value, list) else None, True)
            elif key.startswith(("var:", "event_target:")) or self.scope(key) is not None:
                target_scope = self.scope(key)
                answer = target_scope is not None and self.in_scope(target_scope, lambda: self.test(value))
            elif key == "has_political_power": answer = self.compare(self.current.political_power, op, self.expression(value))
            elif key == "state_population": answer = self.compare(self.current.population, op, self.expression(value))
            else: raise AssertionError("Unsupported trigger: " + key)
            results.append(answer)
        return all(results)

    def ai_weight(self, body):
        """Evaluate native base/factor/modifier weights without running effects."""
        weight = D(1)
        for key, _, value in body:
            if key == "base": weight = self.expression(value)
            elif key == "factor": weight *= self.expression(value)
            elif key == "add": weight += self.expression(value)
            elif key == "modifier":
                conditions = [node for node in value if node[0] not in {"factor", "add"}]
                if self.test(conditions):
                    for modifier, _, operand in value:
                        if modifier == "factor": weight *= self.expression(operand)
                        elif modifier == "add": weight += self.expression(operand)
            else: raise AssertionError("Unsupported AI weight: " + key)
        assert weight >= 0, "AI weight becomes negative"
        return weight

    def execute(self, body):
        branch_taken = False
        for key, _, value in body:
            key = self.substitute(key)
            if key == "if": branch_taken = False
            if key in {"if", "else_if", "else"}:
                if key == "if" or not branch_taken:
                    matches = key == "else" or self.test(first(value, "limit", []))
                    if matches:
                        self.execute([n for n in value if n[0] != "limit"])
                        branch_taken = True
                continue
            branch_taken = False
            if key in {"hidden_effect", "effect"}: self.execute(value)
            elif key in {"custom_effect_tooltip", "effect_tooltip", "log", "newline"}: pass
            elif key in {"set_variable", "set_temp_variable", "add_to_variable", "add_to_temp_variable",
                         "subtract_from_variable", "subtract_from_temp_variable", "multiply_variable",
                         "multiply_temp_variable", "divide_variable", "divide_temp_variable"}:
                if first(value, "var") is not None:
                    name, operand = first(value, "var"), first(value, "value")
                else: name, _, operand = value[0]
                scope, name = self.resolve_variable(name)
                store = scope.temporary if "temp" in key else scope.variables
                operand = self.expression(operand)
                current = store.get(name, D(0))
                if key.startswith("set_"): number = operand
                elif key.startswith("add_"): number = current + operand
                elif key.startswith("subtract_"): number = current - operand
                elif key.startswith("multiply_"): number = current * operand
                else:
                    assert operand != 0, "Script divides by zero"
                    number = current / operand
                store[name] = number
            elif key in {"clamp_variable", "clamp_temp_variable"}:
                scope, name = self.resolve_variable(first(value, "var"))
                store = scope.temporary if "temp" in key else scope.variables
                store[name] = self.clamp(store.get(name, D(0)), value)
            elif key in {"clear_variable", "clear_temp_variable"}:
                scope, name = self.resolve_variable(value)
                (scope.temporary if "temp" in key else scope.variables).pop(name, None)
            elif key in {"round_variable", "round_temp_variable"}:
                scope, name = self.resolve_variable(value)
                store = scope.temporary if "temp" in key else scope.variables
                store[name] = store.get(name, D(0)).quantize(D(1))
            elif key == "set_country_flag":
                flag = self.flag_name(value if isinstance(value, str) else first(value, "flag"))
                self.current.flags[flag] = D(0) if isinstance(value, str) else self.expression(first(value, "days", "0"))
                self.current.flag_started[flag] = self.now
            elif key == "clr_country_flag":
                flag=self.flag_name(value)
                self.current.flags.pop(flag, None)
                self.current.flag_started.pop(flag, None)
            elif key in {"save_event_target_as", "save_global_event_target_as"}:
                self.targets[value] = self.current
            elif key in {"random_owned_state", "random_controlled_state", "every_owned_state"}:
                country = self.current
                states = [s for s in country.states if s.owner == country.tag]
                eligible = [s for s in states if self.in_scope(s, lambda: self.test(first(value, "limit", [])))]
                if key.startswith("random"): eligible = eligible[:1]
                for state in eligible:
                    self.in_scope(state, lambda: self.execute([n for n in value if n[0] != "limit"]))
            elif key == "add_manpower":
                # Native effect localization distinguishes STATE Local Population
                # from COUNTRY Manpower. Keep both resources separate; do not
                # silently turn a country manpower operation into population.
                if isinstance(self.current, State):
                    delta = self.expression(value)
                    self.current.population += delta
                    if self.state_population_hook:
                        self.state_population_hook(self, self.current, delta)
                elif isinstance(self.current, Country): self.current.military_manpower += self.expression(value)
                else: raise AssertionError("Manpower effect has no native state/country scope")
            elif key == "add_political_power": self.current.political_power += self.expression(value)
            elif key == "add_stability": self.current.stability += self.expression(value)
            elif key == "add_ideas": self.current.ideas.add(value)
            elif key == "remove_ideas":
                self.current.ideas.discard(value)
                self.current.timed_ideas.pop(value, None)
            elif key == "add_timed_idea":
                idea = first(value, "idea")
                self.current.ideas.add(idea)
                self.current.timed_ideas[idea] = self.expression(first(value, "days"))
            elif key in {"add_opinion_modifier"}: pass
            elif key == "add_to_array":
                name, _, operand = value[0]
                scope, name = self.resolve_variable(name)
                length = int(scope.variables.get(name + "^num", D(0)))
                scope.variables[name + "^" + str(length)] = self.expression(operand)
                scope.variables[name + "^num"] = D(length + 1)
            elif key == "clear_array":
                scope, name = self.resolve_variable(value)
                for stored in list(scope.variables):
                    if stored.startswith(name + "^"): del scope.variables[stored]
            elif key == "remove_from_array":
                name, _, operand = value[0]
                remaining = [v for v in self.array_values(name) if v != self.expression(operand)]
                self.execute([("clear_array", "=", name)])
                for item in remaining: self.execute([("add_to_array", "=", [(name, "=", str(item))])])
            elif key == "for_each_loop":
                name = first(value, "array")
                children = [n for n in value if n[0] not in {"array", "index", "value", "break"}]
                for i, item in enumerate(self.array_values(name)):
                    self.current.temporary[first(value, "index", "i")] = D(i)
                    self.current.temporary[first(value, "value", "v")] = item
                    self.execute(children)
            # IMPERIA CW — Cold War: Native, guarded bounded transfer chunks.
            elif key == 'while_loop_effect':
                children=[n for n in value if n[0]!='limit'];iterations=0
                while self.test(first(value,'limit',[])):
                    self.execute(children);iterations+=1
                    assert iterations<10000,'Non-terminating native loop'
            elif key == "random_scope_in_array":
                candidates = [self.scope_from_id(v) for v in self.array_values(first(value, "array"))]
                selected = next((scope for scope in candidates if scope is not None and self.in_scope(scope, lambda: self.test(first(value, "limit", [])))), None)
                if selected:
                    self.in_scope(selected, lambda: self.execute([n for n in value if n[0] not in {"array", "limit"}]))
            elif key == "random_list":
                # Deterministic no-incident branch. Dedicated event tests execute
                # both outcomes directly; this model does not test engine RNG.
                self.execute([n for n in value[0][2] if n[0] != "modifier"])
            elif key == "country_event":
                identifier = first(value, "id") if isinstance(value, list) else value
                delay = (self.expression(first(value, "days", "0"))
                         + self.expression(first(value, "hours", "0")) / 24)
                self.queue.append((self.now + delay, identifier, self.current,
                                   self.root, dict(self.targets)))
            elif key == "modify_treasury_effect":
                self.current.variables["treasury"] += self.get("treasury_change")
            elif key == "ingame_update_setup":
                # Model only the native refresh boundary used by this feature:
                # update_state_variables refreshes controlled POP in 100K units,
                # then the real guest-worker hook runs before budget reads.
                self.current.refreshes += 1
                self.current.variables["population_total"] = sum((
                    state.population for country in self.countries.values() for state in country.states
                    if state.controller == self.current.tag), D(0)) / 100000
                if "mdcw_gw_update_resident_costs" in self.effects:
                    self.call("mdcw_gw_update_resident_costs")
            elif key == "add_dynamic_modifier":
                modifier = value if isinstance(value, str) else first(value, "modifier")
                assert isinstance(modifier, str) and modifier, "Missing dynamic modifier name"
                assert not isinstance(value, list) or first(value, "days") is None, "Timed dynamic modifiers are outside this model"
                self.current.dynamic_modifiers.add(modifier)
            elif key == "remove_dynamic_modifier":
                modifier = value if isinstance(value, str) else first(value, "modifier")
                self.current.dynamic_modifiers.discard(modifier)
            elif key == "force_update_dynamic_modifier": self.current.dynamic_refreshes += 1
            elif key == "update_money_dirty_variable": pass
            elif key in self.effects: self.call(key, value if isinstance(value, list) else None)
            elif key.startswith(("var:", "event_target:")) or self.scope(key) is not None:
                target_scope = self.scope(key)
                if target_scope is not None:
                    self.in_scope(target_scope, lambda: self.execute(value))
            else: raise AssertionError("Unsupported effect: " + key)

    def advance_days(self, days):
        """Deliver scheduled events; visible options require an explicit choice.

        Intentionally leaving visible offers unanswered also exercises watchdogs
        if a popup is never resolved. Native timeout defaults are checked on AST.
        """
        end = self.now + D(days)
        while self.queue and min(item[0] for item in self.queue) <= end:
            self.queue.sort(key=lambda item: item[0])
            event = self.queue.pop(0)
            self.elapse(event[0] - self.now)
            self.deliver(event)
        self.elapse(end - self.now)

    def elapse(self, days):
        self.now += days
        for country in self.countries.values():
            for idea, duration in list(country.timed_ideas.items()):
                if duration <= days:
                    country.timed_ideas.pop(idea)
                    country.ideas.discard(idea)
                else:
                    country.timed_ideas[idea] -= days
            for flag, duration in list(country.flags.items()):
                if duration > 0:
                    if duration <= days:
                        country.flags.pop(flag, None)
                        country.flag_started.pop(flag, None)
                    else:
                        country.flags[flag] -= days

    def scope_from_id(self, number):
        return next((country for i, country in enumerate(self.countries.values(), 1) if number == i), None)

    def array_values(self, name):
        scope, base = self.resolve_variable(name)
        return [scope.variables.get(base + "^" + str(i), D(0))
                for i in range(int(scope.variables.get(base + "^num", D(0))))]

    def event_context(self, event, callback):
        _, _, recipient, source, targets = event
        old = self.current, self.root, self.origin, self.previous, self.targets, self.previous_history
        self.current = self.root = self.previous = recipient
        self.previous_history = []
        self.origin, self.targets = source, dict(targets)
        try: return callback()
        finally:
            self.current, self.root, self.origin, self.previous, self.targets, self.previous_history = old

    def deliver(self, event):
        _, identifier, recipient, _, _ = event
        assert identifier in self.events, "Undefined queued event: " + identifier
        body = self.events[identifier]
        if not recipient.exists:
            return
        def delivery():
            if not self.test(first(body, "trigger", [])):
                return
            self.delivered.append(identifier)
            self.execute(first(body, "immediate", []))
            if first(body, "hidden") != "yes" and values(body, "option"):
                self.open_events.append(event)
        self.event_context(event, delivery)

    def choose(self, event, option_index):
        body = self.events[event[1]]
        options = values(body, "option")
        if isinstance(option_index, str):
            name = option_index if option_index.startswith("mdcw_guest_workers.") else "mdcw_guest_workers." + option_index
            matches = [option for option in options if first(option, "name") == name]
            assert len(matches) == 1, "Requested event option is missing or duplicated: " + name
            option = matches[0]
        else:
            option = options[option_index]
        def response():
            assert self.test(first(option, "trigger", [])), "Chosen event option is unavailable"
            self.execute([node for node in option if node[0] not in
                          {"name", "ai_chance", "trigger", "highlight"}])
        self.event_context(event, response)
        if event in self.open_events:
            self.open_events.remove(event)
        self.advance_days(0)


def prepare_tier_fixture(machine, population):
    """Keep country totals unchanged while giving the 100K tier two real states."""
    if population == 100000:
        for country in machine.countries.values():
            if len(country.states) == 1:
                first_state = country.states[0]
                first_state.population /= 2
                country.states.append(State(first_state.population, first_state.owner, first_state.controller))
    return machine


def update_fixture_states(country, **changes):
    for state in country.states:
        for field_name, value in changes.items():
            setattr(state, field_name, value)


def main():
    effect_ast = read_script("common/scripted_effects/mdcw_guest_workers_effects.txt")
    extended_effect_ast = effect_ast[:]
    for path in sorted((ROOT / "common/scripted_effects").glob("mdcw_diaspora*txt")):
        extended_effect_ast += read_script(path.relative_to(ROOT).as_posix())
    trigger_ast = read_script("common/scripted_triggers/mdcw_guest_workers_triggers.txt")
    ai_trigger_ast = read_script("common/scripted_triggers/mdcw_guest_workers_ai_triggers.txt")
    trigger_ast += ai_trigger_ast
    trigger_ast += read_script("common/scripted_triggers/mdcw_diaspora_triggers.txt")
    trigger_ast += read_script("common/scripted_triggers/mdcw_diaspora_policy_triggers.txt")
    decision_ast = read_script("common/decisions/mdcw_guest_workers_decisions.txt")
    category_ast = read_script("common/decisions/categories/mdcw_guest_workers_categories.txt")
    idea_ast = read_script("common/ideas/mdcw_guest_workers_ideas.txt")
    event_ast = read_script("events/mdcw_guest_workers_events.txt")
    scripted_loc_ast = read_script("common/scripted_localisation/mdcw_guest_workers_scripted_localisation.txt")
    art_ast = read_script("interface/mdcw_guest_workers.gfx")
    dynamic_ast = read_script("common/dynamic_modifiers/mdcw_guest_workers_dynamic_modifiers.txt")
    events = {first(body, "id"): body for key, _, body in event_ast if key == "country_event"}
    original_events = dict(events)
    events.update({first(body, "id"): body for key, _, body in read_script("events/mdcw_diaspora_events.txt") if key == "country_event"})
    events.update({first(body, "id"): body for key, _, body in read_script("events/mdcw_diaspora_policy_events.txt") if key == "country_event"})
    effects = {k: v for k, _, v in extended_effect_ast}
    triggers = {k: v for k, _, v in trigger_ast}
    validate_native_helper_calls(extended_effect_ast, trigger_ast,
                                 [decision_ast, category_ast, idea_ast, event_ast, scripted_loc_ast, art_ast, dynamic_ast])
    locpath = ROOT / "localisation/english/mdcw_guest_workers_l_english.yml"
    check(locpath.is_file(), "Missing English localisation")
    raw = locpath.read_bytes() if locpath.is_file() else b""
    check(raw.startswith(b"\xef\xbb\xbf"), "English localisation requires UTF-8 BOM")
    source = raw.decode("utf-8-sig").replace("\r\n", "\n")
    check(source.startswith("l_english:\n"), "English localisation header missing")
    locpairs = re.findall(r'^ (\S+):\d+ (".*")$', source, re.M)
    loc = {}
    for key, quoted in locpairs:
        try: loc[key] = json.loads(quoted)
        except ValueError: check(False, "Invalid localisation quotation: " + key)
    check(len(loc) == len(locpairs), "Duplicate English localisation keys")
    for path in sorted((ROOT / "localisation/english").glob("mdcw_diaspora*english.yml")):
        for key, quoted in re.findall(r'^ (\S+):\d+ (".*")$', path.read_text(encoding="utf-8-sig"), re.M):
            check(key not in loc, "Duplicate diaspora localisation key: " + key)
            loc[key] = json.loads(quoted)
    check(not any("[event_target:mdcw_gw_" in value for value in loc.values()),
          "A saved guest-worker target still uses colon localisation rejected by the native engine")
    check(not list((ROOT / "localisation/german").glob("mdcw_guest_workers*")),
          "Guest-worker localisation should be English only")
    for nodes in (effect_ast, trigger_ast, decision_ast, category_ast, idea_ast, event_ast, dynamic_ast):
        for key, _, value in walk(nodes):
            is_call = value == "yes" or (isinstance(value, list) and first(value, "value") is None)
            if key.startswith("mdcw_gw_") and is_call and key != "mdcw_gw_immigration_backlash":
                if key not in {k for k, _, _ in nodes}:
                    check(key in effects or key in triggers or key.startswith("mdcw_gw_recruit_"),
                          "Undefined guest-worker helper: " + key)
            if key in {"tooltip", "not_tooltip", "custom_effect_tooltip", "title", "desc", "name"} and isinstance(value, str) and value.startswith(("mdcw_gw_", "mdcw_guest_workers.")):
                check(value in loc, "Missing tooltip: " + value)
    validate_assets_and_structure(effect_ast, trigger_ast, decision_ast, category_ast, idea_ast,
                                  loc, scripted_loc_ast, art_ast, dynamic_ast)
    if effects and triggers and decision_ast:
        run_mechanics(effects, triggers, decision_ast, events)
    validate_events_and_tooltips(effect_ast, trigger_ast, original_events, loc)
    validate_offer_presentation(extended_effect_ast, trigger_ast, original_events, loc, art_ast, scripted_loc_ast)
    validate_offer_ai(effect_ast, trigger_ast, ai_trigger_ast, original_events)
    try:
        validate_resident_mechanics(effects, triggers, events, idea_ast, dynamic_ast, loc)
    except (AssertionError, KeyError, TypeError, AttributeError) as error:
        check(False, f"Resident stock/cost executable check: {error}")
    check_budget_and_tick()
    if ISSUES:
        print("FAIL: guest-worker validation")
        for issue in ISSUES: print(" - " + issue)
        return 1
    print(f"PASS: guest-worker static integration and mechanics ({CHECKS} checks)")
    return 0


def run_mechanics(effects, triggers, decision_ast, events):
    decisions = {key: body for _, _, category in decision_ast for key, _, body in category}
    exercise_native_scope_semantics(effects, triggers, events)
    for population, cost, payment, pp_reward, remittance in (
            (25000, 75, 10, 25, 150), (50000, 125, 15, 50, 250),
            (100000, 200, 25, 100, 400)):
        identifier = f"mdcw_gw_recruit_{population}"
        check(identifier in decisions, "Missing recruitment tier: " + identifier)
        if identifier not in decisions: continue
        decision = decisions[identifier]
        check(first(decision, "cost") == str(cost), "Wrong PP cost: " + identifier)
        check(first(decision, "target_root_trigger") is not None and first(decision, "target_trigger") is not None,
              "Missing native targeted decision triggers: " + identifier)
        try:
            exercise_tier(effects, triggers, decision, population, cost, payment, pp_reward, remittance, events)
            exercise_export_reserve_gain(effects, triggers, decision, population, cost, events)
        except (AssertionError, KeyError, TypeError, AttributeError) as error:
            check(False, f"{identifier} executable script check: {error}")
    if all(f"mdcw_gw_recruit_{population}" in decisions for population in (25000, 50000, 100000)):
        try:
            exercise_success_cooldowns(effects, triggers, events, decisions)
            exercise_early_retry_watchdogs(effects, triggers, events, decisions)
            exercise_stale_offer_window(effects, triggers, events, decisions)
        except (AssertionError, KeyError, TypeError, AttributeError) as error:
            check(False, f"Cross-tier receiver cooldown executable script check: {error}")
        try:
            exercise_repeated_arrivals(effects, triggers, events, decisions)
            exercise_large_source_guards(effects, triggers, events, decisions["mdcw_gw_recruit_100000"])
            exercise_stale_population_cache(effects, triggers, events, decisions)
            exercise_income_eligibility(effects, triggers, events, decisions)
        except (AssertionError, KeyError, TypeError, AttributeError) as error:
            check(False, f"Repeated arrival/receipt executable script check: {error}")


def reachable_triggers(triggers, names):
    """Return the real helper dependency closure, preserving its parsed AST."""
    pending, visited, result = list(names), set(), []
    while pending:
        name = pending.pop()
        if name in visited or name not in triggers:
            continue
        visited.add(name)
        body = triggers[name]
        result.append((name, "=", body))
        pending.extend(key for key, _, _ in walk(body) if key in triggers)
    return result


def tier_helpers(base):
    return {f"{base}_{population}" for population in (25000, 50000, 100000)}


def state_population_operations(nodes, path=(), role="ROOT", selected=None):
    result = []
    for key, _, value in nodes:
        if key == "add_manpower": result.append((path, value, role, selected))
        if isinstance(value, list):
            nested_role = key if key in {"ROOT", "FROM"} else role
            selector = first(first(value, "limit", []), "state") if key == "random_owned_state" else selected
            if key in {"event_target:mdcw_gw_origin_state", "event_target:mdcw_gw_origin_state_2",
                       "event_target:mdcw_gw_destination_state"}:
                selector = key
            result.extend(state_population_operations(value, path + (key,), nested_role, selector))
    return result


def validate_native_helper_calls(effect_ast, trigger_ast, other_asts):
    """Reject script forms which parse offline but failed in the actual engine."""
    helpers = {key for key, _, _ in effect_ast + trigger_ast}
    specialized = {"mdcw_gw_apply_immigration", "mdcw_gw_add_emigration",
                   "mdcw_gw_has_sending_state", "mdcw_gw_agreement_available",
                   "mdcw_gw_request_available", "mdcw_gw_request_agreement",
                   "mdcw_gw_complete_agreement", "mdcw_gw_ai_offer_viable"}
    for base in specialized:
        check(base not in helpers and tier_helpers(base) <= helpers,
              "A runtime-parameterized helper has not been replaced with three native variants: " + base)
    definition_bodies = [body for _, _, body in effect_ast + trigger_ast]
    for nodes in definition_bodies + other_asts:
        for key, _, value in walk(nodes):
            check("$" not in key and (not isinstance(value, str) or "$" not in value),
                  "A guest-worker runtime $PARAM$ placeholder remains in loaded gameplay scripts")
            if key in helpers:
                check(value == "yes", "A scripted helper passes unsupported block arguments: " + key)
            if key in {"set_variable", "set_temp_variable"} and isinstance(value, list):
                check(not any(isinstance(operand, list) for _, _, operand in value),
                      "A variable assignment uses an inline arithmetic block rejected by the native engine")


def validate_assets_and_structure(effect_ast, trigger_ast, decision_ast, category_ast, idea_ast,
                                  loc, scripted_loc, art_ast, dynamic_ast):
    sprite_names = set()
    for path in (ROOT / "interface").rglob("*.gfx"):
        sprite_names.update(re.findall(r'\bname\s*=\s*"([^"\n]+)"',
                                      path.read_text(encoding="utf-8-sig", errors="replace")))
    for nodes in (decision_ast, category_ast, idea_ast, dynamic_ast):
        for key, _, value in walk(nodes):
            if key == "icon" and isinstance(value, str):
                check(value in sprite_names, "Unknown decision/category icon: " + value)
            if key == "picture" and isinstance(value, str):
                check(value in sprite_names or "GFX_idea_" + value in sprite_names,
                      "Unknown idea artwork: " + value)
            if key == "custom_modifier_tooltip" and isinstance(value, str):
                check(value in loc, "Missing modifier tooltip: " + value)
    idea_groups = first(idea_ast, "ideas", [])
    ideas = {k: v for _, _, group in idea_groups for k, _, v in group
             if k.startswith("mdcw_ni_")}
    check(len(ideas) == 2, "Expected one sending and one receiving national idea")
    for key in ideas:
        check(key in loc and key + "_desc" in loc, "Missing idea name/description: " + key)
    validate_guestworker_art(ideas, art_ast)
    category_names = {k for k, _, _ in category_ast}
    for category, _, decisions in decision_ast:
        check(category in category_names, "Decision category is undefined: " + category)
        check(category in loc and category + "_desc" in loc, "Missing decision category localisation")
        for key, _, decision in decisions:
            check(key in loc and key + "_desc" in loc, "Missing decision localisation: " + key)
            check(first(decision, "targets") is None and first(decision, "target_array") is None,
                  "Recruitment must use native target generation, not a static country list")
    recruitment_groups = [(category, [key for key, _, _ in decisions])
                          for category, _, decisions in decision_ast]
    check(len(recruitment_groups) == 3 and all(len(keys) == 1 for _, keys in recruitment_groups),
          "The three recruitment sizes must each have their own decision category")
    check({key for _, keys in recruitment_groups for key in keys} == {
              "mdcw_gw_recruit_25000", "mdcw_gw_recruit_50000", "mdcw_gw_recruit_100000"},
          "Separate size categories lose or duplicate a recruitment tier")
    check(len({name for name, _ in recruitment_groups}) == 3,
          "Recruitment size categories share an ID and collapse in the native UI")
    expected_groups = {"mdcw_guest_workers_small": ["mdcw_gw_recruit_25000"],
                       "mdcw_guest_workers_medium": ["mdcw_gw_recruit_50000"],
                       "mdcw_guest_workers_large": ["mdcw_gw_recruit_100000"]}
    check(dict(recruitment_groups) == expected_groups,
          "Small/medium/large categories contain the wrong recruitment sizes")
    overview = first(category_ast, "mdcw_guest_workers_decisions", [])
    check(bool(overview) and first(overview, "visible_when_empty") == "yes",
          "The informational remittance overview disappears when its category has no decisions")
    check("mdcw_guest_workers_decisions" not in {name for name, _ in recruitment_groups},
          "Recruitment entries remain mixed into the remittance overview")
    for category, _, _ in category_ast:
        check(category in loc and category + "_desc" in loc,
              "Missing category name or description: " + category)
    visibility = ScriptMachine({k: v for k, _, v in effect_ast},
                               {k: v for k, _, v in trigger_ast})
    # IMPERIA CW — Cold War: approved Ministry UI replaces the three legacy lists.
    ministry = first(first(read_script("common/scripted_guis/mdcw_diaspora_gui.txt"), "scripted_gui", []), "mdcw_gw_dashboard", [])
    ministry_clicks = dict((k,v) for k,_,v in first(ministry,"effects",[]))
    for category in expected_groups:
        definition = first(category_ast, category, [])
        check(first(definition, "visible_when_empty") == "yes", "Legacy category ID was removed")
        check(not visibility.test(first(definition, "visible", [])),
              "Legacy size list duplicates the approved Recruitment tab: " + category)
    for size in (25000, 50000, 100000):
        check("gw_recruit_"+str(size)+"_click" in ministry_clicks,
              "Ministry Recruitment tab loses a contract size: "+str(size))

    # Ensure that the only physical POP changes occur in the two state targets
    # which the actual owned-and-controlled selection saved earlier.
    all_manpower_sites = state_population_operations(effect_ast)
    reserve_sites = [site for site in all_manpower_sites
                     if site[0][0] == "mdcw_gw_remove_export_reserve_gain"]
    check(len(reserve_sites) == 1
          and reserve_sites[0][1:] == ("mdcw_gw_source_reserve_delta", "FROM", None),
          "The bounded reserve correction must only remove military manpower from the sender country")
    population_sites = [site for site in all_manpower_sites if site not in reserve_sites]
    check(len(population_sites) == 7, "Expected two small/medium and three large native state POP operations")
    check(all(path[-1] == "random_owned_state" and selected for path, _, _, selected in population_sites),
          "A population operation bypasses its exact native STATE selector or changes country manpower")
    for population in (25000, 50000, 100000):
        completion = dict((k, v) for k, _, v in effect_ast)[f"mdcw_gw_complete_agreement_{population}"]
        check(sum(key == "mdcw_gw_remove_export_reserve_gain" for key, _, _ in walk(completion)) == 1,
              f"Tier {population} does not apply exactly one exporter reserve correction")
        sites = [(role, selected, value) for path, value, role, selected in population_sites
                 if path[0] == f"mdcw_gw_complete_agreement_{population}"]
        expected = [("FROM", "event_target:mdcw_gw_origin_state", str(-min(population, 50000))),
                    ("ROOT", "event_target:mdcw_gw_destination_state", str(population))]
        if population == 100000:
            expected.append(("FROM", "event_target:mdcw_gw_origin_state_2", "-50000"))
        check(sorted(sites, key=repr) == sorted(expected, key=repr),
              f"Tier {population} does not use the required exact native state population deltas")
    # Economic and diplomatic AI preferences must not become human request
    # prerequisites. Audit the actual availability dependency closure only.
    trigger_map = {key: body for key, _, body in trigger_ast}
    business_ast = reachable_triggers(trigger_map, tier_helpers("mdcw_gw_agreement_available")
                                      | tier_helpers("mdcw_gw_request_available"))
    all_trigger_keys = {k for k, _, _ in walk(business_ast)}
    forbidden = {"has_opinion", "gdp_total", "total_unemployed",
                 "total_unemployed_k", "average_worker_fulfillment", "is_neighbor_of"}
    check(not all_trigger_keys.intersection(forbidden), "Unexpected recruitment relation/economy/job gate")
    for _, _, value in walk(business_ast):
        if isinstance(value, str):
            check(value not in {"open_borders", "closed_borders"}, "Unexpected border-law gate")
    effects = {k: v for k, _, v in effect_ast}
    for name in ("mdcw_gw_weekly_update", "mdcw_gw_add_remittance_income"):
        keys = [key for key, _, _ in walk(effects.get(name, []))]
        check(not any(key in {"every_country", "every_other_country", "every_owned_state",
                              "every_controlled_state", "for_each_scope_loop", "ingame_update_setup",
                              "add_manpower", "modify_treasury_effect"} for key in keys),
              "Weekly guest-worker path scans countries/POP, refreshes economy or directly pays treasury: " + name)
        check(not any(key in {"treasury", "debt"} for key in keys),
              "Weekly guest-worker path directly mutates treasury/debt: " + name)
    income_body = effects.get("mdcw_gw_add_remittance_income", [])
    for key, _, value in walk(income_body):
        if key in {"set_variable", "add_to_variable", "multiply_variable", "subtract_from_variable"}:
            variable = first(value, "var") or (value[0][0] if value else "")
            check(variable in {"mdcw_gw_weekly_income", "additional_income_rate"},
                  "Budget aggregation writes a persistent gameplay variable: " + str(variable))
    check(any(first(body, "name") == "mdcw_gw_remittance_income"
              for key, _, body in scripted_loc if key == "defined_text"),
          "Missing guest-worker Additional Income scripted localisation")
    money_loc = (ROOT / "localisation/english/MD_money_l_english.yml").read_text(encoding="utf-8-sig")
    income_line = re.search(r'^ AdditionalIncome\S*:\d* .*$', money_loc, re.M)
    check("[mdcw_gw_remittance_income]" in money_loc,
          "Guest-worker income is absent from the native money tooltip")
    for _, _, value in walk(scripted_loc):
        if isinstance(value, str) and value.startswith("mdcw_gw_") and value.endswith("_tt"):
            check(value in loc, "Missing remittance status localisation: " + value)


def validate_guestworker_art(ideas, art_ast):
    sprites = {str(first(body, "name", "")).strip('"'): str(first(body, "texturefile", "")).strip('"')
               for body in values(first(art_ast, "spriteTypes", []), "spriteType")}
    for idea, body in ideas.items():
        picture = first(body, "picture", "")
        name = "GFX_idea_" + picture
        check(name in sprites, "Guest-worker idea does not resolve to its custom sprite: " + idea)
        texture = sprites.get(name)
        if not isinstance(texture, str):
            continue
        path = ROOT / texture
        check(path.resolve().is_relative_to((ROOT / "gfx").resolve()) and path.is_file(),
              "Guest-worker sprite points to a missing or non-gfx texture: " + name)
        if not path.is_file():
            continue
        data = path.read_bytes()
        valid_dds = len(data) >= 128 and data[:4] == b"DDS " and struct.unpack_from("<I", data, 4)[0] == 124
        check(valid_dds, "Guest-worker DDS has an invalid magic/header: " + path.name)
        if not valid_dds:
            continue
        height, width = struct.unpack_from("<II", data, 12)
        check((width, height) == (64, 64), "Guest-worker DDS must use native 64x64 idea dimensions: " + path.name)
        flags, bits = struct.unpack_from("<I", data, 80)[0], struct.unpack_from("<I", data, 88)[0]
        compressed = bool(flags & 0x4) and data[84:88] == b"DXT5"
        rgba = bool(flags & 0x40) and bool(flags & 0x1) and bits == 32
        check(compressed or rgba, "Guest-worker DDS must use alpha-capable DXT5 or uncompressed32-bit RGBA: " + path.name)
        if rgba:
            masks = struct.unpack_from("<IIII", data, 92)
            check(all(mask.bit_count() == 8 for mask in masks)
                  and all(not (left & right) for index, left in enumerate(masks) for right in masks[index + 1:])
                  and (masks[0] | masks[1] | masks[2] | masks[3]) == 0xFFFFFFFF,
                  "Guest-worker RGBA channel masks overlap or omit alpha/color bits: " + path.name)
            pitch = (struct.unpack_from("<I", data, 20)[0]
                     if struct.unpack_from("<I", data, 8)[0] & 0x8 else width * 4)
            expected_bytes = 128 + max(width * 4, pitch) * height
        else:
            expected_bytes = 128 + ((width + 3) // 4) * ((height + 3) // 4) * 16
        check(len(data) >= expected_bytes, "Guest-worker DDS pixel payload is truncated: " + path.name)
        preview = path.with_suffix(".png")
        check(preview.is_file(), "Guest-worker DDS is missing its matching PNG preview: " + path.name)
        if not preview.is_file():
            continue
        png = preview.read_bytes()
        valid_png = (len(png) >= 33 and png[:8] == b"\x89PNG\r\n\x1a\n" and png[12:16] == b"IHDR"
                     and struct.unpack_from(">I", png, 8)[0] == 13)
        check(valid_png, "Guest-worker PNG has an invalid magic/IHDR: " + preview.name)
        if valid_png:
            check(struct.unpack_from(">II", png, 16) == (width, height),
                  "Guest-worker PNG dimensions do not match the DDS texture: " + preview.name)


def validate_events_and_tooltips(effect_ast, trigger_ast, events, loc):
    required = {f"mdcw_guest_workers.{number}" for number in
                (1, 2, 3, 11, 12, 13, 20, 30, 31, 32, 90, 91, 92)}
    check(set(events) == required, "Consent event definitions are incomplete or duplicated")
    for key, _, value in walk(effect_ast + [node for body in events.values() for node in body]):
        if key == "country_event" and isinstance(value, list):
            check(first(value, "id") in events, "Undefined country event: " + str(first(value, "id")))
    for tier in (1, 2, 3):
        identifier = f"mdcw_guest_workers.{tier}"
        if identifier not in events: continue
        body = events[identifier]
        options = values(body, "option")
        check(first(body, "timeout_days") == "17", "Offer timeout must follow the day-17 refund watchdog")
        check(len(options) == 2 and first(options[0], "name") == "mdcw_guest_workers.accept"
              and first(options[1], "name") == "mdcw_guest_workers.refuse",
              "Acceptance must be first, refusal second")
        for option in options:
            hidden = first(option, "hidden_effect", [])
            check(bool(hidden) and hidden[0] == ("mdcw_gw_close_offer_window", "=", "yes"),
                  "An offer option does not clear its sender UI lock before invoking its callback")
        check(first(body, "is_triggered_only") == "yes", "Offer may fire without a pending request")
        request = next((value for key, _, value in effect_ast
                        if key == f"mdcw_gw_request_agreement_{(25000, 50000, 100000)[tier - 1]}"), [])
        queued = [value for key, _, value in walk(request)
                  if key == "country_event" and isinstance(value, list)]
        offer_delay = next((D(first(value, "days", 0)) for value in queued
                            if first(value, "id") == identifier), None)
        watchdog_delays = [D(first(value, "days", 0)) for value in queued
                           if first(value, "id") in {"mdcw_guest_workers.90", "mdcw_guest_workers.91"}]
        check(offer_delay is not None and len(watchdog_delays) == 2
              and all(delay < offer_delay + D(first(body, "timeout_days", 0)) for delay in watchdog_delays),
              "An accept-first timeout can fire before pending requests are safely refunded")
        for field in ("title", "desc"):
            check(first(body, field) in loc, "Offer text is missing: " + identifier)
    trigger_map = {key: value for key, _, value in trigger_ast}
    for population in (25000, 50000, 100000):
        business_name = f"mdcw_gw_agreement_available_{population}"
        business = trigger_map.get(business_name, [])
        request = trigger_map.get(f"mdcw_gw_request_available_{population}", [])
        check(bool(values(business, "hidden_trigger")),
              "Technical programme/existence guards leak into visible requirements")
        visible = values(business, "custom_trigger_tooltip") + values(request, "custom_trigger_tooltip")
        check(len(visible) == 5, "Expected five clean visible request conditions per tier")
        for condition in visible:
            positive, negative = first(condition, "tooltip"), first(condition, "not_tooltip")
            check(positive in loc and negative in loc, "A visible condition lacks explicit positive/negative English text")
            if positive in loc and negative in loc:
                check(not re.search(r"\bmdcw_gw_(?:partner|request_pending|offer_pending|pending_tier)\b",
                                    loc[positive] + loc[negative]), "Internal request data leaks into a prerequisite")
        check(set(key for key, _, _ in business) <= {"hidden_trigger", "custom_trigger_tooltip"},
              "A raw business prerequisite bypasses the clean tooltip wrapper")
        check(set(key for key, _, _ in request) <= {business_name, "custom_trigger_tooltip"},
              "A raw pending prerequisite bypasses the clean tooltip wrapper")


def validate_offer_presentation(effect_ast, trigger_ast, events, loc, art_ast, scripted_loc):
    effects = {key: body for key, _, body in effect_ast}
    triggers = {key: body for key, _, body in trigger_ast}
    for tier, population, payment, pp, bonus in ((1, 25000, 10, 25, 150),
                                                (2, 50000, 15, 50, 250),
                                                (3, 100000, 25, 100, 400)):
        event = events[f"mdcw_guest_workers.{tier}"]
        description = loc.get(first(event, "desc"), "")
        lines = [line for line in description.splitlines() if line.strip()]
        check(len(lines) == (3 if population == 100000 else 2) and len(description.split()) <= 40
              and "[FROM.GetName]" in lines[0],
              "Offer must stay brief: requester introduction followed by the exact transfer route(s)")
        route_text = re.sub(r"§.", "", description)
        first_route = ("[mdcw_gw_origin_state.GetName] to [mdcw_gw_destination_state.GetName]: "
                       + f"{min(population, 50000):,} residents")
        check(first_route in route_text,
              "Offer does not name the exact source→destination route and full population amount")
        if population == 100000:
            check("[mdcw_gw_origin_state_2.GetName] to [mdcw_gw_destination_state.GetName]: 50,000 residents"
                  in route_text and route_text.count("50,000 residents") == 2,
                  "Large offer does not show two explicit50,000-person source→destination routes")
        check("event_target:mdcw_gw_" not in description,
              "Offer state localisation uses colon promotions rejected by the native engine")
        options = {first(option, "name"): option for option in values(event, "option")}
        accept = options["mdcw_guest_workers.accept"]
        check(all(first(option, "default_option") is None for option in options.values()),
              "An unverified native default-option field was added")
        check(set(key for key, _, _ in accept) <= {"name", "ai_chance", "effect_tooltip", "hidden_effect"},
              "Accept option performs rewards outside its preview and single hidden callback")
        previews = values(accept, "effect_tooltip")
        check(len(previews) == 1, "Accept option must have one native reward-preview block")
        if len(previews) != 1:
            continue
        wrapped_preview = previews[0]
        active_preview = first(wrapped_preview, "if", [])
        active_condition = first(active_preview, "limit", [])
        preview = [node for node in active_preview if node[0] != "limit"]
        # IMPERIA CW — Cold War: Inspect the shared preview's actual arithmetic,
        # retaining the ban on persistent writes rather than whitelisting a call.
        preview = [child for node in preview for child in
                   (effects[node[0]] if node[0]=='mdcw_dp_preview_export_income' else [node])]
        expired_preview = first(wrapped_preview, "else", [])
        check([key for key, _, _ in wrapped_preview] == ["if", "else"]
              and active_condition == [("mdcw_gw_offer_pair_pending", "=", "yes")]
              and expired_preview == [("custom_effect_tooltip", "=", "mdcw_gw_offer_expired_tt")]
              and "mdcw_gw_offer_expired_tt" in loc,
              "An expired offer must replace every native gain with its cancellation explanation")
        allowed_preview = {"set_temp_variable", "clamp_temp_variable", "add_to_temp_variable",
                           "subtract_from_temp_variable", "multiply_temp_variable", "divide_temp_variable",
                           "modify_treasury_effect", "add_political_power", "custom_effect_tooltip",
                           "event_target:mdcw_gw_origin_state", "event_target:mdcw_gw_origin_state_2",
                           "ROOT", "FROM"}
        check(set(key for key, _, _ in preview) <= allowed_preview,
              "Reward preview contains persistent gameplay writes or callbacks")
        check(first(preview, "modify_treasury_effect") == "yes"
              and first(preview, "add_political_power") == str(pp),
              "Native treasury/PP preview is absent or uses the wrong tier values")
        tooltip = f"mdcw_gw_accept_offer_{population}_tt"
        check(first(preview, "custom_effect_tooltip") == tooltip and tooltip in loc,
              "Accept preview uses the wrong tier's population/remittance tooltip")
        text = loc.get(tooltip, "")
        check("mdcw_gw_offer_remittance_m" in text and "60" in text,
              "Accept reward lines omit current remittance increase or receiving cooldown")
        preview_operations = state_population_operations(preview)
        expected_operations = [("ROOT", "event_target:mdcw_gw_origin_state", str(-min(population, 50000))),
                               ("FROM", "event_target:mdcw_gw_destination_state", str(population))]
        if population == 100000:
            expected_operations.append(("ROOT", "event_target:mdcw_gw_origin_state_2", "-50000"))
        check(sorted((role, target, value) for _, value, role, target in preview_operations)
              == sorted(expected_operations)
              and all(path[-1] == target for path, _, _, target in preview_operations),
              "Native Local Population preview uses a wrong state, delta or country manpower scope")
        amount_k = D(population) / 1000
        cases = ((D(0), D(0), D(bonus)), (-amount_k, D(0), D(0)),
                 (-amount_k / 2, D(0), D(bonus) / 2), (amount_k, D(500), D(bonus)),
                 (D(0), D(2990), D(10)), (D(0), D(3000), D(0)),
                 (-amount_k * 2, D(0), D(0)))
        try:
            for net, pool, expected_increase in cases:
                machine = prepare_tier_fixture(ScriptMachine(effects, triggers, events), population)
                machine.root.variables.update(mdcw_gw_net_emigration_k=net, mdcw_gw_remittance_pool_m=pool)
                machine.root.flags["mdcw_gw_offer_pending"] = D(0)
                machine.origin.flags["mdcw_gw_request_pending"] = D(0)
                machine.root.variables.update(mdcw_gw_partner=D(2), mdcw_gw_pending_tier=D(tier))
                machine.origin.variables.update(mdcw_gw_partner=D(1), mdcw_gw_pending_tier=D(tier))
                machine.targets.update(mdcw_gw_origin_state=machine.root.states[0],
                                       mdcw_gw_destination_state=machine.origin.states[0])
                if population == 100000:
                    machine.targets["mdcw_gw_origin_state_2"] = machine.root.states[1]
                before = persistent_snapshot(machine)
                # Choosing an option must never execute its effect_tooltip.
                machine.execute([("effect_tooltip", "=", wrapped_preview)])
                check(persistent_snapshot(machine) == before,
                      "Reward preview executes a payment, PP reward, POP move or persistent write")
                # Evaluate display arithmetic in an isolated snapshot, checking
                # independently known edge cases against the actual emission helper.
                display = deepcopy(machine)
                check(display.test(active_condition), "Valid sender preview fails its pending-pair condition")
                display.execute(wrapped_preview)
                check(sum(state.population for state in display.root.states) == 1_000_000 - population
                      and sum(state.population for state in display.origin.states) == 1_000_000 + population
                      and all(country.military_manpower == 250000 for country in display.countries.values()),
                      "Sandboxed native preview does not represent real state population separately from military manpower")
                check(display.root.variables["treasury"] == D(100 + payment)
                      and display.root.political_power == D(1000 + pp),
                      "Displayed native treasury/PP rewards do not match the approved tier")
                shown = display.root.temporary.get("mdcw_gw_offer_remittance_m")
                check(shown == expected_increase,
                      "Displayed remittance increase ignores net-import offsets or the pool cap")
                actual = deepcopy(machine)
                actual.call(f"mdcw_gw_add_emigration_{population}")
                check(shown == actual.root.variables["mdcw_gw_remittance_pool_m"] - pool,
                      "Displayed remittance amount differs from the actual helper's financial result")
                check(display.root.variables["mdcw_gw_net_emigration_k"] == net
                      and display.root.variables["mdcw_gw_remittance_pool_m"] == pool,
                      "Preview calculation modifies persistent migration/remittance ledgers")
                expired = deepcopy(machine)
                expired.root.flags.pop("mdcw_gw_offer_pending")
                expired.origin.flags.pop("mdcw_gw_request_pending")
                before_expired = persistent_snapshot(expired)
                before_temporary = deepcopy([country.temporary for country in expired.countries.values()])
                check(not expired.test(active_condition), "Expired offer still selects its native reward preview")
                expired.execute(wrapped_preview)
                check(persistent_snapshot(expired) == before_expired
                      and [country.temporary for country in expired.countries.values()] == before_temporary,
                      "Expired preview still displays/evaluates POP, treasury, PP or remittance rewards")
        except (AssertionError, KeyError, TypeError, AttributeError) as error:
            check(False, f"Tier {population} reward preview executable check: {error}")
    validate_arrival_picture(events, art_ast)
    check(first(events["mdcw_guest_workers.30"], "timeout_days") == "13"
          and D(first(events["mdcw_guest_workers.30"], "timeout_days", 0)) < 60,
          "Arrival receipt must explicitly close before the next60-day recruitment window can overwrite its data")
    success_text = loc.get(first(events["mdcw_guest_workers.30"], "desc"), "")
    check("[mdcw_gw_sender.GetName]" in success_text
          and "[mdcw_gw_arrival_source_details]" in success_text
          and len([line for line in success_text.splitlines() if line.strip()]) == 2
          and len(success_text.split()) <= 20,
          "Success notification must stay brief with the sender and scripted transfer route(s)")
    source_details = next((body for key, _, body in scripted_loc
                           if key == "defined_text" and first(body, "name") == "mdcw_gw_arrival_source_details"), [])
    check(bool(source_details), "Missing native scripted-localisation source receipt")
    for count, arrival, expected in ((0, 0, "mdcw_gw_arrival_one_source_tt"),
                                    (1, 25, "mdcw_gw_arrival_one_source_tt"),
                                    (1, 50, "mdcw_gw_arrival_one_source_50000_tt"),
                                    (2, 100, "mdcw_gw_arrival_two_sources_tt"),
                                    (2, 50, "mdcw_gw_arrival_two_sources_tt")):
        context = ScriptMachine(effects, triggers, events)
        context.root.variables["mdcw_gw_last_source_count"] = D(count)
        context.root.variables["mdcw_gw_last_arrival_k"] = D(arrival)
        chosen = next((first(text, "localization_key") for text in values(source_details, "text")
                       if context.test(first(text, "trigger", []))), None)
        check(chosen == expected and chosen in loc, "Scripted source receipt chooses the wrong25K/50K/two-source route")
        text = loc.get(chosen, "")
        amount = "50,000" if count == 2 or arrival == 50 else "25,000"
        first_route = ("[mdcw_gw_origin_state.GetName] to [mdcw_gw_destination_state.GetName]: "
                       + amount + " residents")
        check(first_route in re.sub(r"§.", "", text),
              "Source receipt omits its exact source→destination route or full population amount")
        if count == 2:
            check("[mdcw_gw_origin_state_2.GetName] to [mdcw_gw_destination_state.GetName]: 50,000 residents"
                  in re.sub(r"§.", "", text) and text.count("50,000 residents") == 2,
                  "Two-state receipt does not display both50,000-person source→destination routes")
        check(not any(name in success_text + text for name in
                      ("mdcw_gw_departure_before_k", "mdcw_gw_departure_after_k", "mdcw_gw_last_arrival_k",
                       "mdcw_gw_arrival_before_k", "mdcw_gw_arrival_after_k", "mdcw_gw_guest_workers_k"))
              and len(text.splitlines()) == (2 if count == 2 else 1),
              "Transfer description replaces the simple route with diagnostic/stock prose")
    check("event_target:mdcw_gw_" not in success_text,
          "Success notification uses colon promotions rejected by the native engine")
    result_options = values(events["mdcw_guest_workers.30"], "option")
    check(len(result_options) == 1 and "mdcw_gw_resident_status_tt" in values(result_options[0], "custom_effect_tooltip")
          and set(key for key, _, _ in result_options[0]) <= {"name", "custom_effect_tooltip", "effect_tooltip"},
          "Arrival acknowledgement is missing its cost status or performs gameplay effects")
    receipt_preview = first(result_options[0], "effect_tooltip", []) if result_options else []
    receipt_operations = state_population_operations(receipt_preview)
    check(all(str(value) in {"-25000", "-50000", "25000", "50000", "100000"}
              and path[-1] == target for path, value, _, target in receipt_operations)
          and len(receipt_operations) == 7
          and not any(key in {"set_temp_variable", "multiply_temp_variable", "subtract_from_temp_variable"}
                      for key, _, _ in walk(receipt_preview)),
          "Native receipt must display literal population effects without unevaluated temporary arithmetic")
    check("0.01%" in loc.get("mdcw_ni_overseas_employment_programme_desc", "")
          and not any("0.5% weekly decay" in value for value in loc.values()),
          "English remittance description does not match the slower 0.01% weekly decay")


def validate_arrival_picture(events, art_ast):
    name = "GFX_mdcw_guest_workers_arrival"
    for number in (1, 2, 3):
        check(first(events[f"mdcw_guest_workers.{number}"], "picture") == name,
              "A guest-worker offer does not use the custom arrival picture")
    registrations = [body for body in values(first(art_ast, "spriteTypes", []), "spriteType")
                     if str(first(body, "name", "")).strip('"') == name]
    check(len(registrations) == 1, "Custom arrival picture sprite is missing or registered more than once")
    if len(registrations) != 1:
        return
    texture = str(first(registrations[0], "texturefile", "")).strip('"')
    path = ROOT / texture
    check(path.resolve().is_relative_to((ROOT / "gfx").resolve()) and path.is_file(),
          "Custom arrival sprite points to a missing or non-gfx texture")
    if not path.is_file():
        return
    data = path.read_bytes()
    valid = len(data) >= 128 and data[:4] == b"DDS " and struct.unpack_from("<I", data, 4)[0] == 124
    check(valid, "Arrival picture DDS has an invalid magic/header")
    if valid:
        height, width = struct.unpack_from("<II", data, 12)
        check((width, height) == (217, 163), "Arrival picture does not use the native 217x163 framed dimensions")
        flags, bits = struct.unpack_from("<I", data, 80)[0], struct.unpack_from("<I", data, 88)[0]
        check(flags & 0x40 and flags & 0x1 and bits == 32,
              "Arrival picture must retain its uncompressed 32-bit RGBA pixels")
        check(len(data) >= 128 + width * height * 4, "Arrival picture DDS pixel payload is truncated")
        preview = path.with_suffix(".png")
        if preview.is_file():
            png = preview.read_bytes()
            check(len(png) >= 24 and png[:8] == b"\x89PNG\r\n\x1a\n"
                  and png[12:16] == b"IHDR" and struct.unpack_from(">II", png, 16) == (width, height),
                  "Arrival picture PNG preview header/dimensions do not match the native DDS")


def validate_offer_ai(effect_ast, trigger_ast, ai_trigger_ast, events):
    effects = {key: body for key, _, body in effect_ast}
    triggers = {key: body for key, _, body in trigger_ast}
    ai_names = {key for key, _, _ in ai_trigger_ast}
    check(ai_names == tier_helpers("mdcw_gw_ai_offer_viable") | {"mdcw_gw_ai_financial_pressure", "mdcw_gw_ai_sender_eligible"},
          "AI evaluation helpers are missing or unexpectedly expanded")
    # IMPERIA CW — Cold War: Acquisition may consider labour supply; offer replies remain financial only.
    ai_names.discard("mdcw_gw_ai_sender_eligible")
    business = reachable_triggers(triggers, tier_helpers("mdcw_gw_request_available"))
    check(not {key for key, _, _ in walk(business)} & ai_names,
          "AI preferences have leaked into player request eligibility")
    check(not {key for key, _, _ in walk(effect_ast)} & ai_names,
          "AI offer evaluation has been added to gameplay effects or recurring updates")
    def inspect_ai_context(nodes, inside_weight=False):
        for key, _, value in nodes:
            if key in ai_names:
                check(inside_weight, "AI preferences affect event visibility or callbacks outside ai_chance")
            if isinstance(value, list):
                inspect_ai_context(value, inside_weight or key == "ai_chance")
    for body in events.values():
        inspect_ai_context(body)
    scans_or_mutations = {"any_country", "any_other_country", "every_country", "every_other_country",
                          "random_country", "any_state", "every_state", "random_state",
                          "any_owned_state", "any_controlled_state", "every_owned_state",
                          "every_controlled_state", "random_owned_state", "random_controlled_state",
                          "for_each_scope_loop", "for_each_loop", "while_loop", "state_population",
                          "set_variable", "add_to_variable",
                          "ingame_update_setup", "country_event", "add_manpower"}
    for tier in (1, 2, 3):
        event = events.get(f"mdcw_guest_workers.{tier}", [])
        check(first(event, "immediate") is None,
              "Offer arrival performs new calculations or effects outside AI weights")
        options = values(event, "option")
        for option in options:
            check(first(option, "trigger") is None,
                  "AI evaluation disables a human accept/refuse button")
            weight = first(option, "ai_chance", [])
            check(bool(weight), "Offer option has no explicit AI weight")
            helper_names = {key for key, _, _ in walk(weight) if key in triggers}
            closure = weight + reachable_triggers(triggers, helper_names)
            check(not {key for key, _, _ in walk(closure)} & scans_or_mutations,
                  "AI evaluation scans population/countries or changes gameplay state")
            forbidden_preferences = {"population_total_m", "workforce_total_display", "workforce_total",
                                     "total_unemployed_percentage_display", "total_unemployed_k",
                                     "average_worker_fulfillment", "mdcw_gw_net_emigration_k"}
            referenced = {key for key, _, _ in walk(closure)}
            referenced.update(value for _, _, value in walk(closure) if isinstance(value, str))
            check(not referenced & forbidden_preferences,
                  "AI acceptance considers sender population, migration balance or labour needs")
        if len(options) != 2:
            continue
        try:
            exercise_offer_ai(effects, triggers, events, tier)
        except (AssertionError, KeyError, TypeError, AttributeError) as error:
            check(False, f"Offer {tier} AI executable check: {error}")
    for path in (ROOT / "common/on_actions").rglob("*.txt"):
        source = path.read_text(encoding="utf-8-sig", errors="replace")
        check(not any(re.search(r"\b" + re.escape(name) + r"\b", source) for name in ai_names),
              "AI offer evaluation was added to an on-action: " + path.name)
    # Only the monetary return should change willingness. With fees below 10%
    # of GDP, all sizes share the same baseline despite different POP amounts.
    neutral_sizes = [offer_ai_scores(make_ai_machine(effects, triggers, events, population_m=5), tier)[2]
                     for tier in (1, 2, 3)]
    check(neutral_sizes == [D("0.55")] * 3,
          "Recruitment size changes AI acceptance without a monetary reason")
    for gdp, expected_order in ((80, "large"), (120, "medium")):
        machine = make_ai_machine(effects, triggers, events, population_m=5)
        machine.root.variables["gdp_total"] = D(gdp)
        small, medium, large = [offer_ai_scores(machine, tier)[2] for tier in (1, 2, 3)]
        check((small == medium < large) if expected_order == "large" else (small < medium == large),
              "A more significant upfront payment does not improve AI acceptance")
    neutral = make_ai_machine(effects, triggers, events, population_m=10)
    favorable = make_ai_machine(effects, triggers, events, population_m=100)
    favorable.root.variables.update(budget_balance_ratio=D("-0.20"), gdp_total=D(30))
    cautious = make_ai_machine(effects, triggers, events, population_m=2)
    cautious.root.variables.update(mdcw_gw_remittance_pool_m=D(3000))
    neutral_p = offer_ai_scores(neutral, 2)[2]
    favorable_p = offer_ai_scores(favorable, 1)[2]
    cautious_p = offer_ai_scores(cautious, 3)[2]
    check(neutral_p == D("0.55"), "Neutral 10M-country / 50K offer does not yield 55% acceptance")
    check(favorable_p == D("96.25") / D("141.25"),
          "Financial-need and significant-payment scenario has incorrect combined AI weights")
    check(cautious_p == D("46.75") / D("91.75"),
          "Limited further remittance-return scenario has incorrect combined AI weights")
    check(cautious_p < neutral_p < favorable_p,
          "Monetary return does not change AI willingness in the expected direction")


def make_ai_machine(effects, triggers, events, population_m):
    # Offer scope: ROOT sends and FROM receives. MD's caches use millions,
    # billions and fractions; no actual population or economy scan is required.
    machine = ScriptMachine(effects, triggers, events)
    machine.root.variables["gdp_per_capita"] = D(2)
    machine.origin.variables["gdp_per_capita"] = D(5)
    machine.root.variables.update(population_total_m=D(population_m), workforce_total_display=D(6),
                                  total_unemployed_percentage_display=D("0.05"),
                                  average_worker_fulfillment=D(1), budget_balance_ratio=D(0),
                                  debt_ratio=D("0.5"), gdp_total=D(1000),
                                  mdcw_gw_remittance_pool_m=D(0), mdcw_gw_net_emigration_k=D(0))
    return machine


def offer_ai_scores(machine, tier):
    options = values(machine.events[f"mdcw_guest_workers.{tier}"], "option")
    by_name = {first(option, "name"): option for option in options}
    refused = machine.ai_weight(first(by_name["mdcw_guest_workers.refuse"], "ai_chance", []))
    accepted = machine.ai_weight(first(by_name["mdcw_guest_workers.accept"], "ai_chance", []))
    assert refused + accepted > 0, "Both offer choices have zero AI weight"
    return accepted, refused, accepted / (accepted + refused)


def exercise_offer_ai(effects, triggers, events, tier):
    population, payment = {1: (25000, 10), 2: (50000, 15), 3: (100000, 25)}[tier]
    def make(): return make_ai_machine(effects, triggers, events, population_m=10)
    def expect(label, changes, factor, absent=()):
        machine = make()
        machine.root.variables.update({key: D(value) for key, value in changes.items()})
        for key in absent:
            machine.root.variables.pop(key, None)
        before = persistent_snapshot(machine)
        accepted, refused, probability = offer_ai_scores(machine, tier)
        check(accepted == D(55) * D(factor) and refused == 45,
              f"Offer {tier}: {label} has wrong AI weights")
        check(persistent_snapshot(machine) == before and not machine.queue,
              f"Offer {tier}: AI evaluation changes caches, POP, cash, flags or event queue")
        return probability

    expect("neutral baseline", {}, 1)
    epsilon = D("0.000001")
    # Sender size and labour needs are deliberately irrelevant. Exercise the
    # former population cutoffs too, so removed policies cannot return silently.
    population_values = {D(0), D(".01"), D(1), D(2), D(10), D(100), D(1000)}
    for divisor in (20000, 10000, 5000, 1000):
        cutoff = D(population) / divisor
        population_values.update({cutoff - epsilon, cutoff, cutoff + epsilon})
    for value in sorted(population_values):
        expect("population size is irrelevant: " + str(value), {"population_total_m": value}, 1)
    expect("missing population size is irrelevant", {}, 1, absent=("population_total_m",))
    for variable, samples in {
            "workforce_total_display": (0, ".01", 1, 1000),
            "total_unemployed_percentage_display": (0, ".099999", ".10", ".100001", ".50"),
            "average_worker_fulfillment": (0, ".5", ".899999", ".90", ".900001", 1),
            "total_unemployed_k": (0, 1, 10000)}.items():
        for value in samples:
            expect(f"labour data is irrelevant: {variable}={value}", {variable: value}, 1)
        expect("missing labour data is irrelevant: " + variable, {}, 1, absent=(variable,))
    expect("combined shortage and joblessness remain irrelevant",
           {"population_total_m": ".01", "workforce_total_display": 1,
            "average_worker_fulfillment": ".1", "total_unemployed_percentage_display": ".50"}, 1)
    expect("exact deficit boundary", {"budget_balance_ratio": "-.10"}, 1)
    expect("deficit pressure", {"budget_balance_ratio": "-.100001"}, "1.25")
    expect("exact debt boundary", {"debt_ratio": 1}, 1)
    expect("debt pressure", {"debt_ratio": "1.000001"}, "1.25")
    expect("combined deficit/debt counted once",
           {"budget_balance_ratio": "-.2", "debt_ratio": 2}, "1.25")
    expect("missing financial caches", {}, 1, absent=("budget_balance_ratio", "debt_ratio"))
    for gdp, factor in ((D(payment) * 4 - epsilon, "1.4"), (D(payment) * 4, "1.4"),
                        (D(payment) * 4 + epsilon, "1.2"), (D(payment) * 10, "1.2"),
                        (D(payment) * 10 + epsilon, 1), (D(0), 1), (D(-1), 1)):
        expect(f"payment/GDP boundary {gdp}", {"gdp_total": gdp}, factor)
    expect("missing GDP does not manufacture payment significance", {}, 1, absent=("gdp_total",))
    expect("below remittance cap threshold", {"mdcw_gw_remittance_pool_m": "1079.999999"}, 1)
    expect("exact remittance cap threshold", {"mdcw_gw_remittance_pool_m": 2700}, ".85")
    expect("full remittance pool", {"mdcw_gw_remittance_pool_m": 3000}, ".85")
    for balance in (-D(population) / 1000 + epsilon, -D(population) / 1000,
                    -D(population) / 1000 - epsilon, D(-10000), D(0), D(10000)):
        expect("migration balance is irrelevant: " + str(balance), {"mdcw_gw_net_emigration_k": balance}, 1)
    invalidations = {
        "sender absent": lambda m: setattr(m.root, "exists", False),
        "receiver absent": lambda m: setattr(m.origin, "exists", False),
        "sender programme missing": lambda m: m.root.ideas.remove("mdcw_ni_overseas_employment_programme"),
        "receiver programme missing": lambda m: m.origin.ideas.remove("mdcw_ni_guest_worker_recruitment_programme"),
        "insufficient GDP/c gap": lambda m: m.origin.variables.update(gdp_per_capita=D("2.4999")),
        "missing sender GDP/c": lambda m: m.root.variables.pop("gdp_per_capita", None),
        "receiver cooldown": lambda m: m.origin.flags.update(mdcw_gw_receiving_cooldown=D(60)),
        "receiver cannot pay": lambda m: m.origin.variables.update(treasury=D(payment) - epsilon),
    }
    for label, invalidate in invalidations.items():
        machine = make()
        invalidate(machine)
        accepted, refused, probability = offer_ai_scores(machine, tier)
        check(accepted == probability == 0 and refused == 45,
              f"Offer {tier}: invalid {label} retains a nonzero AI acceptance weight")
        options = values(events[f"mdcw_guest_workers.{tier}"], "option")
        check(all(machine.test(first(option, "trigger", [])) for option in options),
              f"Offer {tier}: {label} disables a player's accept/refuse option")
    machine = make()
    machine.origin.variables["treasury"] = D(payment)
    check(offer_ai_scores(machine, tier)[0] == 55,
          "AI rejects an otherwise valid offer when the receiver has exactly enough cash")
    machine.root.flags.update(mdcw_gw_sending_cooldown=D(60), mdcw_gw_receiving_cooldown=D(60))
    check(offer_ai_scores(machine, tier)[0] == 55,
          "Sender AI incorrectly refuses because of a legacy sending flag or its own receiving cooldown")
    machine.root.states.clear()
    machine.origin.states.clear()
    check(offer_ai_scores(machine, tier)[0] == 55,
          "AI weights scan actual state population instead of leaving validation to the existing callback")


def resident_snapshot(machine):
    fields = ("mdcw_gw_guest_workers_k", "mdcw_gw_health_cost", "mdcw_gw_social_cost", "mdcw_gw_bureaucracy_cost")
    return deepcopy([(country.tag, tuple(country.variables.get(key, D(0)) for key in fields),
                      country.dynamic_modifiers, country.dynamic_refreshes)
                     for country in machine.countries.values()])


def arrival_receipt_snapshot(machine):
    fields = ("mdcw_gw_last_arrival_k", "mdcw_gw_arrival_before_k", "mdcw_gw_arrival_after_k",
              "mdcw_gw_departure_before_k", "mdcw_gw_departure_after_k",
              "mdcw_gw_departure_2_before_k", "mdcw_gw_departure_2_after_k",
              "mdcw_gw_last_departure_k", "mdcw_gw_last_source_count",
              "mdcw_gw_source_manpower_before_k", "mdcw_gw_source_manpower_after_k",
              "mdcw_gw_source_reserve_before", "mdcw_gw_source_reserve_removed")
    return deepcopy([(country.tag, tuple(country.variables.get(key) for key in fields))
                     for country in machine.countries.values()])


def exercise_native_scope_semantics(effects, triggers, events):
    """Lock the model to vanilla's distinct Country Manpower/State Population API.

    This tests direct script-resource operations. Conscription/mobilization
    reactions remain engine behavior; the feature logs native manpower_k before
    and after real source operations so they can be observed without guessing.
    """
    machine = ScriptMachine(effects, triggers, events)
    country, state = machine.root, machine.root.states[0]
    machine.execute([("add_manpower", "=", "321")])
    check(country.military_manpower == 250321 and state.population == 1_000_000,
          "Model incorrectly treats native COUNTRY manpower as civilian population")
    machine.in_scope(state, lambda: machine.execute([("add_manpower", "=", "17")]))
    check(country.military_manpower == 250321 and state.population == 1_000_017,
          "Model incorrectly treats native STATE population as a country manpower grant")
    check(machine.get("manpower_k") == D("250.321"),
          "Native manpower_k diagnostics do not read the separate country reserve")


def exercise_export_reserve_gain(effects, triggers, decision, population, cost, events):
    """Replay the logged Portugal +9,219 reserve artifact, without guessing its cause."""
    source_count = 2 if population == 100000 else 1
    scenarios = [(9746, [0] * source_count),
                 (9746, [9219] + [0] * (source_count - 1)),
                 (39989, [2] + [0] * (source_count - 1)),
                 (9746, [-400] + [0] * (source_count - 1)),
                 (0, [9219] + [0] * (source_count - 1))]
    if source_count == 2:
        scenarios += [(9746, [0, 9219]), (9746, [4000, 5219]),
                      (9746, [-400, 200]), (9746, [400, -200])]
    for initial, adjustments in scenarios:
        machine = prepare_tier_fixture(ScriptMachine(effects, triggers, events), population)
        sender, receiver = machine.origin, machine.root
        sender.military_manpower = D(initial)
        # Stale receipt values must never be used for a new agreement.
        receiver.variables.update(mdcw_gw_source_reserve_before=D(123456),
                                  mdcw_gw_source_reserve_removed=D(99999))
        remaining = list(adjustments)
        def observed_side_effect(model, state, delta):
            if state.owner == sender.tag and delta < 0:
                sender.military_manpower += D(remaining.pop(0))
        machine.state_population_hook = observed_side_effect
        before_pop = [[s.population for s in c.states] for c in (receiver, sender)]
        machine.root.political_power -= cost
        machine.execute(first(decision, "complete_effect", []))
        machine.advance_days(1)
        tier = {25000: 1, 50000: 2, 100000: 3}[population]
        offer = next(item for item in machine.open_events if item[1] == f"mdcw_guest_workers.{tier}")
        machine.choose(offer, "accept")
        expected = D(initial + min(sum(adjustments), 0))
        label = f"Tier {population}, reserve {initial}, injected withdrawal effects {adjustments}"
        check(not remaining, label + ": did not execute every source withdrawal")
        check(sender.military_manpower == expected,
              label + ": exporter gains military reserves or a real reserve reduction is refunded")
        check(receiver.military_manpower == 250000,
              label + ": exporter correction touched the recipient's military reserve")
        check(receiver.states[0].population == before_pop[0][0] + population
              and all(state.population == before - min(population, 50000)
                      for state, before in zip(sender.states, before_pop[1])),
              label + ": reserve correction changed the agreed physical state population transfer")
        check(receiver.variables.get("mdcw_gw_source_reserve_removed") == max(sum(adjustments), 0)
              and receiver.variables.get("mdcw_gw_source_manpower_after_k") == expected / 1000,
              label + ": correction receipt is stale or does not match the final exporter reserve")


def exercise_large_source_guards(effects, triggers, events, decision):
    def make(): return prepare_tier_fixture(ScriptMachine(effects, triggers, events), 100000)
    def request(machine):
        machine.root.political_power -= 200
        machine.execute(first(decision, "complete_effect", []))
    def resources(machine):
        return deepcopy(([(country.tag, country.variables["treasury"], country.military_manpower,
                           [state.population for state in country.states]) for country in machine.countries.values()],
                         resident_snapshot(machine), arrival_receipt_snapshot(machine)))
    for populations in ((2_000_000,), (50001, 50000), (50000, 50001), (50000, 50000), (25000, 1_000_000)):
        machine = make()
        machine.origin.states = [State(population=D(value), owner="B", controller="B") for value in populations]
        check(not machine.test(first(decision, "available", [])),
              "Large request allows fewer than two distinct source states above50K population")
        before = persistent_snapshot(machine)
        request(machine)
        check(persistent_snapshot(machine) == before and not machine.queue,
              "Invalid two-source request charges PP or creates a partial/pending transfer")
    # A valid alternative third state must not replace source2 after the offer.
    for invalidation in ("ownership", "control", "population", "same_state", "missing_target"):
        machine = make()
        machine.origin.states.append(State(owner="B", controller="B"))
        request(machine)
        if invalidation in {"same_state", "missing_target"}:
            replacement = []
            for queued in machine.queue:
                if queued[1] == "mdcw_guest_workers.3":
                    targets = dict(queued[4])
                    if invalidation == "same_state": targets["mdcw_gw_origin_state_2"] = targets["mdcw_gw_origin_state"]
                    else: targets.pop("mdcw_gw_origin_state_2", None)
                    queued = (*queued[:4], targets)
                replacement.append(queued)
            machine.queue = replacement
        machine.advance_days(1)
        offered = next(item for item in machine.open_events if item[1] == "mdcw_guest_workers.3")
        second = offered[4].get("mdcw_gw_origin_state_2")
        if invalidation == "ownership": second.owner = "A"
        elif invalidation == "control": second.controller = "A"
        elif invalidation == "population": second.population = D(50000)
        check(machine.call("mdcw_gw_agreement_available_100000", trigger=True),
              "Large source-invalidation fixture lacks two other eligible states")
        before = resources(machine)
        machine.choose(offered, "accept")
        check(resources(machine) == before and machine.root.political_power == 1000
              and machine.origin.political_power == 1000,
              "Invalid source2 causes a partial/rerolled transfer or fails to refund the full request")
        check("mdcw_guest_workers.30" not in machine.delivered
              and "mdcw_guest_workers.32" in machine.delivered
              and not any(country.flags.keys() & {"mdcw_gw_request_pending", "mdcw_gw_offer_pending",
                                                  "mdcw_gw_sending_cooldown", "mdcw_gw_receiving_cooldown"}
                          for country in machine.countries.values()),
              "Invalid or legacy one-source large request leaves locks/cooldowns or reports success")


def validate_resident_mechanics(effects, triggers, events, idea_ast, dynamic_ast, loc):
    stock, modifier = "mdcw_gw_guest_workers_k", "mdcw_gw_resident_costs"
    definition = first(dynamic_ast, modifier, [])
    bindings = {"health_cost_multiplier_modifier": "mdcw_gw_health_cost",
                "consumer_goods_factor": "gw_project_consumer",
                "bureaucracy_cost_multiplier_modifier": "mdcw_gw_bureaucracy_cost"}
    check(bool(definition) and all(first(definition, key) == value for key, value in bindings.items()),
          "Retained stock is not bound to the three native spending-cost multipliers")
    for key in (modifier, modifier + "_desc", "mdcw_gw_resident_count_tt", "mdcw_gw_resident_status_tt"):
        check(key in loc, "Missing retained-resident spirit/status localisation: " + key)
    check(stock in loc.get("mdcw_gw_resident_count_tt", "")
          and "thousand" in loc.get("mdcw_gw_resident_count_tt", ""),
          "Resident count does not display its safe thousands ledger")
    all_nodes = [node for name, body in effects.items() for node in walk(body)]
    references = {key for key, _, _ in all_nodes}
    references.update(value for _, _, value in all_nodes if isinstance(value, str))
    check("mdcw_gw_guest_workers" not in references,
          "An unsafe raw-person resident variable was introduced alongside the thousands ledger")
    cost_keys = {key for key, _, _ in walk(effects["mdcw_gw_update_resident_costs"])}
    check(not cost_keys & {"every_country", "any_country", "every_owned_state", "any_owned_state",
                           "every_controlled_state", "random_owned_state", "ingame_update_setup"},
          "Resident cost refresh adds scans or recursively refreshes the economy")
    def make(): return ScriptMachine(effects, triggers, events)
    def costs(country): return tuple(country.variables.get(key, D(0)) for key in ("mdcw_gw_health_cost", "mdcw_gw_social_cost", "mdcw_gw_bureaucracy_cost"))
    def expected_costs(amount, population):
        health = D(amount) * D(".10") / D(population)
        bureau = D(amount) * D(".20") / D(population)
        return health, D(0), bureau
    def match(left, right): return all(abs(a - b) < D("1e-18") for a, b in zip(left, right))
    for amount, population in ((25, 10), (50, 100), (100, 100), (100, 200), (2500, 1000)):
        machine = make()
        machine.root.variables.update({stock: D(amount), "population_total": D(population)})
        machine.call("mdcw_gw_update_resident_costs")
        check(match(costs(machine.root), expected_costs(amount, population))
              and modifier in machine.root.dynamic_modifiers,
              "Resident healthcare/social/bureaucracy costs do not scale by actual population share")
        before = resident_snapshot(machine)
        machine.call("mdcw_gw_update_resident_costs")
        check(resident_snapshot(machine) == before,
              "An unchanged resident refresh stacks modifiers or forces redundant updates")
        machine.root.ideas.clear()
        machine.call("mdcw_gw_update_resident_costs")
        check(resident_snapshot(machine) == before and machine.test(first(definition, "enable", [])),
              "Closing a programme removes retained stock or its ongoing spending costs")
    # A large stock remains represented as thousands instead of overflowing a
    # raw-person variable. Population growth changes costs without deleting stock.
    growth = make()
    growth.root.states[0].population = D(10_000_000)
    growth.root.variables.update({stock: D(100), "population_total": D(1)})
    growth.execute([("ingame_update_setup", "=", "yes")])
    check(growth.root.variables["population_total"] == 100
          and match(costs(growth.root), (D(".10"), D(0), D(".20"))),
          "Resident cost refresh reads a stale denominator before native population refresh")
    growth.root.states[0].population = D(20_000_000)
    growth.execute([("ingame_update_setup", "=", "yes")])
    check(growth.root.variables[stock] == 100
          and match(costs(growth.root), (D(".05"), D(0), D(".10"))),
          "Population growth does not lower cost shares while preserving retained stock")
    for population in (None, D(0), D(-1)):
        missing = make()
        missing.root.variables[stock] = D(25)
        if population is None: missing.root.variables.pop("population_total", None)
        else: missing.root.variables["population_total"] = population
        missing.call("mdcw_gw_update_resident_costs")
        check(missing.root.variables[stock] == 25 and costs(missing.root) == (0, 0, 0)
              and modifier in missing.root.dynamic_modifiers
              and missing.test(first(definition, "enable", [])),
              "Missing/zero population divides by zero, erases stock or hides its retained-count spirit")
    empty = make()
    empty.root.variables[stock] = D(-25)
    empty.root.dynamic_modifiers.add(modifier)
    empty.call("mdcw_gw_update_resident_costs")
    check(empty.root.variables[stock] == 0 and costs(empty.root) == (0, 0, 0)
          and modifier not in empty.root.dynamic_modifiers,
          "Resident stock can go negative or leave stale costs after its zero cleanup")
    for net, expected in ((-50, 50), (50, 0), (0, 0)):
        legacy = make()
        legacy.root.variables["mdcw_gw_net_emigration_k"] = D(net)
        legacy.call("mdcw_gw_initialize_resident_stock")
        check(legacy.root.variables[stock] == expected, "Legacy retained stock is seeded with the wrong sign/units")
        legacy.root.variables["mdcw_gw_net_emigration_k"] = D(-1000)
        legacy.call("mdcw_gw_initialize_resident_stock")
        check(legacy.root.variables[stock] == expected, "Legacy stock migration is repeated after the ledger changes")
    cumulative = make()
    previous = D(0)
    for population in (25000, 50000, 100000):
        amount = D(population) / 1000
        cumulative.call(f"mdcw_gw_apply_immigration_{population}")
        cumulative.root.states[0].population += population
        cumulative.execute([("ingame_update_setup", "=", "yes")])
        check(cumulative.root.variables[stock] == previous + amount
              and costs(cumulative.root)[0] > previous * D(".10") / ((D(1000) + previous) / 100),
              "Additional arrivals do not increase retained stock and spending costs")
        previous += amount
        legacy = make()
        legacy.root.variables["mdcw_gw_net_emigration_k"] = D(-50)
        legacy.call(f"mdcw_gw_apply_immigration_{population}")
        check(legacy.root.variables[stock] == D(50) + amount,
              "First new import counts the legacy migration seed or arriving population twice")
        for cached_population in (D(100), D(".1"), D(0), None):
            exported = make()
            exported.root.variables[stock] = D(100)
            if cached_population is None: exported.root.variables.pop("population_total", None)
            else: exported.root.variables["population_total"] = cached_population
            exported.call(f"mdcw_gw_add_emigration_{population}")
            check(exported.root.variables[stock] == 100
                  and exported.root.variables.get("mdcw_gw_pending_export_pop") == amount / 100,
                  "Export helper consumes a stale population cache instead of deferring stock removal")
            exported.root.states[0].population -= population
            exported.execute([("ingame_update_setup", "=", "yes")])
            retained = D(100)
            check(abs(exported.root.variables[stock] - retained) < D("1e-18")
                  and "mdcw_gw_pending_export_pop" not in exported.root.variables,
                  "Deferred own export does not use fresh population plus the actual departure exactly once")
    for population in (None, D(0), D(-1)):
        missing = make()
        missing.root.variables.update({stock: D(100), "mdcw_gw_pending_export_pop": D(".5")})
        if population is None: missing.root.variables.pop("population_total", None)
        else: missing.root.variables["population_total"] = population
        missing.call("mdcw_gw_update_resident_costs")
        check(missing.root.variables[stock] == 100
              and "mdcw_gw_pending_export_pop" not in missing.root.variables,
              "Missing/nonpositive fresh population erases stock or leaves an export marker for a later double reduction")
    groups = first(idea_ast, "ideas", [])
    receiving = next(body for _, _, group in groups for key, _, body in group
                     if key == "mdcw_ni_guest_worker_recruitment_programme")
    before = resident_snapshot(growth)
    growth.root.ideas.discard("mdcw_ni_guest_worker_recruitment_programme")
    growth.execute(first(receiving, "on_remove", []))
    check(resident_snapshot(growth) == before,
          "Actual programme removal clears resident stock, costs or its dynamic modifier")
    programme_definitions = {key: body for _, _, group in groups for key, _, body in group
                             if key in {"mdcw_ni_overseas_employment_programme", "mdcw_ni_guest_worker_recruitment_programme"}}
    exercise_programme_lifecycle(effects, triggers, events, programme_definitions)


def exercise_income_eligibility(effects, triggers, events, decisions):
    """All sizes: 25% boundary, uncached old saves, wartime and acceptance recheck."""
    for tier, population, cost in ((1, 25000, 75), (2, 50000, 125), (3, 100000, 200)):
        decision = decisions[f"mdcw_gw_recruit_{population}"]
        for income, eligible in (("2.4999", False), ("2.5", True), ("2.5001", True),
                                 ("2", False), ("1", False), ("0", False)):
            machine = prepare_tier_fixture(ScriptMachine(effects, triggers, events), population)
            machine.root.variables["gdp_per_capita"] = D(income)
            check(machine.test(first(decision, "available", [])) == eligible,
                  f"Tier {population}: wrong 25% GDP/c boundary at {income}")
        for cached in (None, D(0), D(-1)):
            machine = prepare_tier_fixture(ScriptMachine(effects, triggers, events), population)
            if cached is not None: machine.origin.variables["gw_native_available_k"] = cached
            machine.root.variables["gdp_per_capita"] = D("2.5")
            machine.root.peace = machine.origin.peace = False
            check(machine.test(first(decision, "available", [])),
                  "War or a missing/stale native-population cache still blocks recruitment")
            before = sum(s.population for s in machine.root.states)
            machine.root.political_power -= cost
            machine.execute(first(decision, "complete_effect", []))
            machine.advance_days(1)
            offer = next(e for e in machine.open_events if e[1] == f"mdcw_guest_workers.{tier}")
            machine.choose(offer, "accept")
            check(sum(s.population for s in machine.root.states) == before + population,
                  "An eligible wartime/old-save agreement does not complete its real population transfer")
        ai = make_ai_machine(effects, triggers, events, population_m=10)
        ai.root.peace = ai.origin.peace = False
        for income, eligible in (("2.4999", False), ("2.5", True), ("2.5001", True)):
            ai.origin.variables["gdp_per_capita"] = D(income)
            check((offer_ai_scores(ai, tier)[0] > 0) == eligible,
                  "Sender AI uses a different GDP/c threshold or still refuses because of war")


def exercise_stale_population_cache(effects, triggers, events, decisions):
    """Real acceptance must derive source retention from actual predeparture POP."""
    stock, marker = "mdcw_gw_guest_workers_k", "mdcw_gw_pending_export_pop"
    for tier, population, cost, payment in ((1, 25000, 75, 10), (2, 50000, 125, 15),
                                           (3, 100000, 200, 25)):
        for cached_population in (D(10), D(1000), D(0), D(-1), None):
            machine = prepare_tier_fixture(ScriptMachine(effects, triggers, events), population)
            source = machine.origin
            for state in source.states: state.population = D(10_000_000) / len(source.states)
            source.variables[stock] = D(100)
            if cached_population is None: source.variables.pop("population_total", None)
            else: source.variables["population_total"] = cached_population
            decision = decisions[f"mdcw_gw_recruit_{population}"]
            machine.root.political_power -= cost
            machine.execute(first(decision, "complete_effect", []))
            machine.advance_days(1)
            offer = next(item for item in machine.open_events if item[1] == f"mdcw_guest_workers.{tier}")
            machine.choose(offer, "accept")
            expected = D(100)
            check(abs(source.variables[stock] - expected) < D("1e-18")
                  and marker not in source.variables
                  and source.variables["population_total"] == D(10_000_000 - population) / 100000,
                  f"Tier {population}: stale source cache {cached_population} corrupts retained residents")
            check(all(abs(source.variables.get(key, D(0)) - expected_cost) < D("1e-18")
                      for key, expected_cost in (("mdcw_gw_health_cost", D(100)*D(".10") / (D(10_000_000-population)/100000)),
                                                 ("mdcw_gw_social_cost", D(0)),
                                                 ("mdcw_gw_bureaucracy_cost", D(100)*D(".20") / (D(10_000_000-population)/100000)))),
                  "Deferred source removal does not precede fresh resident-cost calculation")
            check(source.refreshes == machine.root.refreshes == 1
                  and source.variables["treasury"] == 100 + payment
                  and machine.root.variables["treasury"] == 100 - payment
                  and machine.root.variables[stock] == D(population) / 1000
                  and sum(state.population for country in machine.countries.values()
                          for state in country.states) == 11_000_000,
                  "Fixing stale retention adds economy scans/refreshes or changes POP/cash/recipient stock")
            before = resident_snapshot(machine)
            machine.in_scope(source, lambda: machine.execute([("ingame_update_setup", "=", "yes")]))
            check(resident_snapshot(machine) == before and marker not in source.variables,
                  "A later fresh population update consumes the same export marker twice")


def exercise_programme_lifecycle(effects, triggers, events, programmes):
    """Receiver removal is governed by retained population; sender keeps its old commitment."""
    receiver_id = "mdcw_ni_guest_worker_recruitment_programme"
    sender_id = "mdcw_ni_overseas_employment_programme"
    for retained in (D(0), D(100)):
        machine = ScriptMachine(effects, triggers, events)
        machine.root.political_power = D(10000)
        machine.root.variables["mdcw_gw_guest_workers_k"] = retained
        for identifier, definition in programmes.items():
            machine.root.ideas.discard(identifier)
            machine.root.ideas.add(identifier)
            machine.execute(first(definition, "on_add", []))
            check(machine.test(first(definition, "allowed_to_remove", [])) == (identifier == receiver_id and retained == 0),
                  "Receiver can escape positive-stock costs or an empty programme cannot close")
        machine.advance_days(1440)
        check(machine.test(first(programmes[sender_id], "allowed_to_remove", [])),
              "Sender commitment never expires")
        check(machine.test(first(programmes[receiver_id], "allowed_to_remove", [])) == (retained == 0),
              "Four years unlocks receiver removal while residents remain")
        # This fixture tests the removal gate; real zero-stock repatriation is
        # executed independently in the diaspora transaction tests.
        machine.root.variables["mdcw_gw_guest_workers_k"] = D(0)
        machine.root.variables["gw_unrecorded_k"] = D(0)
        machine.call("mdcw_gw_update_resident_costs")
        check(machine.test(first(programmes[receiver_id], "allowed_to_remove", [])),
              "Returning the final residents does not unlock receiver closure")
        for identifier, definition in programmes.items():
            machine.root.ideas.discard(identifier)
            machine.execute(first(definition, "on_remove", []))
        check("mdcw_gw_resident_costs" not in machine.root.dynamic_modifiers,
              "Zero-stock closure leaves a resident-cost modifier")


def exercise_repeated_arrivals(effects, triggers, events, decisions):
    machine = prepare_tier_fixture(ScriptMachine(effects, triggers, events), 100000)
    cumulative = D(0)
    for tier, population, pp_cost in ((1, 25000, 75), (2, 50000, 125), (3, 100000, 200)):
        before = machine.root.states[0].population
        machine.root.political_power -= pp_cost
        machine.execute(first(decisions[f"mdcw_gw_recruit_{population}"], "complete_effect", []))
        machine.advance_days(1)
        offer = next(item for item in machine.open_events if item[1] == f"mdcw_guest_workers.{tier}")
        destination = offer[4]["mdcw_gw_destination_state"]
        origin = offer[4]["mdcw_gw_origin_state"]
        origin_before = origin.population
        machine.choose(offer, "accept")
        cumulative += population
        machine.advance_days(D(1) / 24)
        notice = [item for item in machine.open_events if item[1] == "mdcw_guest_workers.30"][-1]
        check(destination is machine.root.states[0] and destination.population == before + population
              and origin.population == origin_before - min(population, 50000)
              and machine.root.variables["mdcw_gw_guest_workers_k"] == cumulative / 1000,
              "Repeated contracts do not physically arrive at the stated destination or accumulate retained stock once")
        check(machine.root.variables["mdcw_gw_arrival_before_k"] == before / 1000
              and machine.root.variables["mdcw_gw_arrival_after_k"] == destination.population / 1000
              and machine.root.variables["mdcw_gw_last_arrival_k"] == D(population) / 1000,
              "Arrival receipt is not sampled from the actual destination before/after its population change")
        display = deepcopy(machine)
        displayed_notice = [item for item in display.open_events if item[1] == "mdcw_guest_workers.30"][-1]
        shown_destination = displayed_notice[4]["mdcw_gw_destination_state"]
        shown_origin = displayed_notice[4]["mdcw_gw_origin_state"]
        shown_second = displayed_notice[4].get("mdcw_gw_origin_state_2") if population == 100000 else None
        display_before = shown_destination.population
        origin_display_before = shown_origin.population
        second_display_before = shown_second.population if shown_second else None
        total_display_before = sum(state.population for country in display.countries.values() for state in country.states)
        preview = first(values(events["mdcw_guest_workers.30"], "option")[0], "effect_tooltip", [])
        display.event_context(displayed_notice, lambda: display.execute(preview))
        check(shown_destination.population - display_before == D(population)
              and shown_origin.population - origin_display_before == -min(population, 50000)
              and (shown_second is None or shown_second.population - second_display_before == -50000)
              and sum(state.population for country in display.countries.values() for state in country.states)
                  == total_display_before
              and all(country.military_manpower == 250000 for country in display.countries.values()),
              "Recipient native effect preview does not show the exact source loss(es) and equal destination gain")
        snapshot = persistent_snapshot(machine)
        machine.choose(notice, 0)
        check(persistent_snapshot(machine) == snapshot,
              "Acknowledging the arrival status duplicates a transfer, receipt or spending-cost change")
        machine.advance_days(60)
    check(sum(state.population for state in machine.root.states) == 1_175_000
          and sum(state.population for state in machine.origin.states) == 825_000
          and machine.root.variables["mdcw_gw_guest_workers_k"] == 175
          and machine.root.variables["treasury"] == 50 and machine.origin.variables["treasury"] == 150,
          "All three completed tiers fail final destination POP/stock/cash conservation")
    machine.root.political_power -= 75
    machine.execute(first(decisions["mdcw_gw_recruit_25000"], "complete_effect", []))
    machine.advance_days(1)
    single = next(item for item in machine.open_events if item[1] == "mdcw_guest_workers.1")
    machine.choose(single, "accept")
    check(machine.root.variables["mdcw_gw_last_source_count"] == 1
          and machine.root.variables["mdcw_gw_departure_2_before_k"] == 0
          and machine.root.variables["mdcw_gw_departure_2_after_k"] == 0,
          "A single-source agreement after a two-source agreement retains stale second-source receipts")


def exercise_tier(effects, triggers, decision, population, cost, payment, pp_reward, remittance, events):
    body = first(decision, "complete_effect", [])
    tier = {25000: 1, 50000: 2, 100000: 3}[population]
    offer_id = f"mdcw_guest_workers.{tier}"
    per_origin = 50000 if population == 100000 else population
    initial_state_pop = D(500000 if population == 100000 else 1_000_000)
    def make(): return prepare_tier_fixture(ScriptMachine(effects, triggers, events), population)
    def request(machine):
        machine.root.political_power -= cost
        machine.execute(body)
    def offer(machine):
        machine.advance_days(1)
        found = [item for item in machine.open_events if item[1] == offer_id]
        assert len(found) == 1, "Next-day sender offer is missing or duplicated"
        check(found[0][2] is machine.origin and found[0][3] is machine.root,
              "Offer swaps the sending/receiving countries")
        check(any(found[0][4].get("mdcw_gw_origin_state") is state for state in machine.origin.states)
              and any(found[0][4].get("mdcw_gw_destination_state") is state for state in machine.root.states),
              "Next-day offer loses its preselected source/destination state targets")
        return found[0]
    def accept(machine):
        machine.choose(offer(machine), "accept")
    def pending_cleared(machine):
        return all(not c.flags.keys() & {"mdcw_gw_request_pending", "mdcw_gw_offer_pending"}
                   and not c.variables.keys() & {"mdcw_gw_partner", "mdcw_gw_pending_tier", "mdcw_gw_pending_pp"}
                   for c in machine.countries.values())
    def financial_population(machine):
        return [(c.tag, c.variables["treasury"], c.political_power,
                 [s.population for s in c.states]) for c in machine.countries.values()]

    machine = make()
    receiver, sender = machine.root, machine.origin
    check(machine.test(first(decision, "available", [])), "A valid request is unavailable")
    request(machine)
    check(receiver.states[0].population == sender.states[0].population == initial_state_pop,
          "Request transfers population before sender approval")
    check(receiver.variables["treasury"] == sender.variables["treasury"] == 100,
          "Request spends/reserves cash before sender approval")
    check(sender.political_power == 1000 and receiver.political_power == D(1000 - cost),
          "Request grants sender PP or charges receiver PP incorrectly")
    check(not any(c.variables.get("mdcw_gw_remittance_pool_m", 0) for c in machine.countries.values()),
          "Request creates remittances before sender approval")
    check(receiver.refreshes == sender.refreshes == 0, "Request unnecessarily refreshes both economies")
    check(not any(c.flags.keys() & {"mdcw_gw_sending_cooldown", "mdcw_gw_receiving_cooldown"}
                  for c in machine.countries.values()), "Request starts a success cooldown before approval")
    check(len(machine.queue) == 3, "Request should queue one offer and two one-shot watchdogs")
    chosen_offer = offer(machine)
    check(machine.now == 1, "Offer does not arrive on the next day")
    machine.choose(chosen_offer, "accept")
    check(receiver.states[0].population == initial_state_pop + population, "Receiver POP differs from approved agreement")
    check(sender.states[0].population == initial_state_pop - per_origin, "Sender POP differs from approved agreement")
    if population == 100000:
        check(chosen_offer[4].get("mdcw_gw_origin_state_2") is sender.states[1]
              and chosen_offer[4]["mdcw_gw_origin_state_2"] is not chosen_offer[4]["mdcw_gw_origin_state"]
              and sender.states[1].population == initial_state_pop - 50000,
              "Large agreement does not remove exactly50K from each of two distinct source states")
    check(all(country.military_manpower == 250000 for country in machine.countries.values()),
          "A population transfer directly changes a country's military manpower reserve")
    check(receiver.variables.get("mdcw_gw_source_manpower_before_k") == 250
          and receiver.variables.get("mdcw_gw_source_manpower_after_k") == 250,
          "Source military-manpower diagnostic is not sampled separately from state population")
    check(receiver.variables.get("mdcw_gw_last_source_count") == (2 if population == 100000 else 1)
          and receiver.variables.get("mdcw_gw_last_departure_k") == D(population) / 1000
          and receiver.variables.get("mdcw_gw_departure_before_k") == initial_state_pop / 1000
          and receiver.variables.get("mdcw_gw_departure_after_k") == (initial_state_pop - per_origin) / 1000,
          "Source receipt does not match the observed departure and correct number of source states")
    check(receiver.variables.get("mdcw_gw_departure_2_before_k") == (initial_state_pop / 1000 if population == 100000 else 0)
          and receiver.variables.get("mdcw_gw_departure_2_after_k") == ((initial_state_pop - 50000) / 1000 if population == 100000 else 0),
          "Second-source receipt is missing, wrong or left stale for a single-source agreement")
    check(sum(s.population for c in machine.countries.values() for s in c.states) == 2_000_000,
          "Approved agreement creates or destroys POP")
    check(receiver.variables["treasury"] == D(100 - payment)
          and sender.variables["treasury"] == D(100 + payment), "Approved payment is not equal and opposite")
    check(sender.political_power == D(1000 + pp_reward)
          and receiver.political_power == D(1000 - cost), "Approval duplicates PP cost/reward")
    check("mdcw_gw_sending_cooldown" not in sender.flags, "Success incorrectly gives the sender a cooldown")
    check(receiver.flags.get("mdcw_gw_receiving_cooldown") == D(60),
          "Receiver success cooldown is not country-wide for 60 days")
    check(receiver.refreshes == sender.refreshes == 1, "Approved agreement must refresh each economy once")
    check(receiver.variables.get("mdcw_gw_guest_workers_k") == D(population) / 1000
          and sender.variables.get("mdcw_gw_guest_workers_k") == 0,
          "Successful import does not add the retained stock exactly once in thousands")
    check(receiver.variables.get("mdcw_gw_arrival_before_k") == initial_state_pop / 1000
          and receiver.variables.get("mdcw_gw_arrival_after_k") == (initial_state_pop + population) / 1000
          and receiver.variables.get("mdcw_gw_last_arrival_k") == D(population) / 1000,
          "Successful receipt does not prove the observed population arrival in its actual destination")
    expected_health = (D(population) / 1000) * D(".10") / receiver.variables["population_total"]
    check(abs(receiver.variables.get("mdcw_gw_health_cost", D(0)) - expected_health) < D("1e-18")
          and receiver.variables.get("mdcw_gw_social_cost") == 0
          and abs(receiver.variables.get("mdcw_gw_bureaucracy_cost", D(0)) - expected_health * 2) < D("1e-18")
          and "mdcw_gw_resident_costs" in receiver.dynamic_modifiers,
          "Approved import does not refresh retained-resident costs against the new population")
    stocked = make()
    stocked.root.variables["mdcw_gw_guest_workers_k"] = D(50)
    stocked.origin.variables["mdcw_gw_guest_workers_k"] = D(100)
    stocked.call("mdcw_gw_update_resident_costs")
    stocked.in_scope(stocked.origin, lambda: stocked.call("mdcw_gw_update_resident_costs"))
    request(stocked)
    accept(stocked)
    expected_source_stock = D(100)
    check(abs(stocked.origin.variables["mdcw_gw_guest_workers_k"] - expected_source_stock) < D("1e-18")
          and stocked.root.variables["mdcw_gw_guest_workers_k"] == D(50) + D(population) / 1000,
          "Actual bilateral transfer uses a post-transfer source denominator or double-counts recipient stock")
    check(abs(stocked.origin.variables["mdcw_gw_health_cost"] - D(100) * D(".10") / (D(1000000-population) / 100000)) < D("1e-18"),
          "Domestic exports do not preserve the existing diaspora and refresh its population share")
    for outcome in ("refuse", "invalid", "expire"):
        unchanged = make()
        unchanged.root.variables["mdcw_gw_guest_workers_k"] = D(50)
        unchanged.origin.variables["mdcw_gw_guest_workers_k"] = D(100)
        unchanged.root.variables.update(mdcw_gw_last_arrival_k=D(13), mdcw_gw_arrival_before_k=D(987),
                                         mdcw_gw_arrival_after_k=D(1000))
        unchanged.call("mdcw_gw_update_resident_costs")
        unchanged.in_scope(unchanged.origin, lambda: unchanged.call("mdcw_gw_update_resident_costs"))
        before_residents = resident_snapshot(unchanged)
        before_receipt = arrival_receipt_snapshot(unchanged)
        request(unchanged)
        if outcome == "expire":
            unchanged.advance_days(17)
        else:
            waiting = offer(unchanged)
            if outcome == "invalid":
                unchanged.root.variables["treasury"] = D(payment) - D(".001")
            unchanged.choose(waiting, "refuse" if outcome == "refuse" else "accept")
        check(resident_snapshot(unchanged) == before_residents,
              "Refusal/invalidation/expiry changes retained stock, spending costs or modifier refreshes")
        check(arrival_receipt_snapshot(unchanged) == before_receipt,
              "Refusal/invalidation/expiry overwrites the last successful arrival receipt")
    check(sender.variables.get("mdcw_gw_net_emigration_k") == D(population) / 1000
          and receiver.variables.get("mdcw_gw_net_emigration_k") == -D(population) / 1000,
          "Approved migration ledger has wrong sign or units")
    check(sender.variables.get("mdcw_gw_remittance_pool_m") == D(remittance)
          and receiver.variables.get("mdcw_gw_remittance_pool_m", 0) == 0,
          "Approved agreement credits the wrong remittance pool")
    check(pending_cleared(machine), "Success leaves stale pending locks or partner IDs")
    check("mdcw_gw_offer_window_open" not in sender.flags,
          "Manual acceptance leaves its sender UI window locked")
    check("mdcw_guest_workers.30" not in machine.delivered,
          "Arrival receipt fires immediately instead of one hour after acceptance")
    before_notice = financial_population(machine)
    snapshot_receipt = arrival_receipt_snapshot(machine)
    machine.advance_days(D(1) / 24)
    check(financial_population(machine) == before_notice and arrival_receipt_snapshot(machine) == snapshot_receipt,
          "Receipt delivery duplicates the transfer, payment or recorded state measurements")
    check("mdcw_guest_workers.30" in machine.delivered, "One-hour success notification is missing")
    success_notice = next(item for item in machine.open_events if item[1] == "mdcw_guest_workers.30")
    check(success_notice[4].get("mdcw_gw_receiver") is receiver
          and success_notice[4].get("mdcw_gw_sender") is sender,
          "Success notification loses country names after pending variables are cleared")
    check(success_notice[4].get("mdcw_gw_origin_state") is sender.states[0]
          and success_notice[4].get("mdcw_gw_destination_state") is receiver.states[0],
          "Success notification does not preserve the exact states whose population moved")
    if population == 100000:
        check(success_notice[4].get("mdcw_gw_origin_state_2") is sender.states[1],
              "Success notification loses the second actual departure state")
    before = persistent_snapshot(machine)
    machine.choose(chosen_offer, "accept")
    check(persistent_snapshot(machine) == before, "Duplicate acceptance transfers or refunds twice")

    refused = make()
    original = financial_population(refused)
    request(refused)
    refused_offer = offer(refused)
    refused.choose(refused_offer, "refuse")
    check(financial_population(refused) == original and pending_cleared(refused),
          "Refusal loses PP, changes cash/POP, or leaves pending locks")
    check("mdcw_gw_offer_window_open" not in refused.origin.flags,
          "Manual refusal leaves its sender UI window locked")
    check("mdcw_guest_workers.31" in refused.delivered, "Refusal notification is missing")
    check(not any(c.flags.keys() & {"mdcw_gw_sending_cooldown", "mdcw_gw_receiving_cooldown"}
                  for c in refused.countries.values()), "Refusal starts a success cooldown")
    check(refused.test(first(decision, "available", [])), "Refusal does not permit a fresh request")
    refusal_notice = next(item for item in refused.open_events if item[1] == "mdcw_guest_workers.31")
    check(refusal_notice[4].get("mdcw_gw_receiver") is refused.root
          and refusal_notice[4].get("mdcw_gw_sender") is refused.origin,
          "Refusal notification loses country names after pending variables are cleared")
    before = persistent_snapshot(refused)
    refused.choose(refused_offer, "refuse")
    check(persistent_snapshot(refused) == before, "Duplicate refusal refunds PP twice")

    failures = {
        "insufficient cash": lambda m: m.root.variables.update(treasury=D(payment) - D("0.001")),
        "receiver cooldown": lambda m: m.root.flags.update(mdcw_gw_receiving_cooldown=D(60)),
        "insufficient GDP/c gap": lambda m: m.root.variables.update(gdp_per_capita=D("2.4999")),
        "missing sender GDP/c": lambda m: m.origin.variables.pop("gdp_per_capita", None),
        "missing sender programme": lambda m: m.origin.ideas.remove("mdcw_ni_overseas_employment_programme"),
        "missing receiver programme": lambda m: m.root.ideas.remove("mdcw_ni_guest_worker_recruitment_programme"),
        "source POP exactly transfer": lambda m: update_fixture_states(m.origin, population=D(per_origin)),
        "source POP too small": lambda m: update_fixture_states(m.origin, population=D(per_origin - 1)),
        "source not controlled": lambda m: update_fixture_states(m.origin, controller="A"),
        "source not owned": lambda m: update_fixture_states(m.origin, owner="A"),
        "destination not controlled": lambda m: update_fixture_states(m.root, controller="B"),
        "destination not owned": lambda m: update_fixture_states(m.root, owner="B"),
        "no sending state": lambda m: m.origin.states.clear(),
        "no receiving state": lambda m: m.root.states.clear(),
        "sender absent": lambda m: setattr(m.origin, "exists", False),
        "receiver absent": lambda m: setattr(m.root, "exists", False),
        "same country": lambda m: setattr(m, "origin", m.root),
    }
    for label, invalidate in failures.items():
        failed = make()
        invalidate(failed)
        check(not failed.test(first(decision, "available", [])), label + " does not block request")
        before = persistent_snapshot(failed)
        request(failed)
        check(persistent_snapshot(failed) == before, label + " request is not an atomic PP refund")
        check(not failed.queue, label + " request still queues offers/watchdogs")

    # A previously valid offer can become invalid before approval. Business
    # checks must be repeated when the callback actually executes.
    for label, invalidate in failures.items():
        if label in {"sender absent", "receiver absent", "same country"}: continue
        failed = make()
        request(failed)
        waiting = offer(failed)
        invalidate(failed)
        before = financial_population(failed)
        before_receipt = arrival_receipt_snapshot(failed)
        failed.choose(waiting, "accept")
        expected = deepcopy(before)
        expected[0] = (expected[0][0], expected[0][1], D(1000), expected[0][3])
        check(financial_population(failed) == expected and pending_cleared(failed),
              label + " at approval mutates POP/cash or fails to refund and clear")
        check(arrival_receipt_snapshot(failed) == before_receipt,
              label + " at approval overwrites the previous arrival receipt")
        check("mdcw_guest_workers.32" in failed.delivered, label + " lacks invalidation notification")

    boundary = make()
    boundary.root.variables["treasury"] = D(payment)
    update_fixture_states(boundary.origin, population=D(per_origin + 1))
    check(boundary.test(first(decision, "available", [])), "Exact cash / one remaining source POP is blocked")
    request(boundary)
    accept(boundary)
    check(boundary.root.variables["treasury"] == 0 and all(state.population == 1 for state in boundary.origin.states),
          "Boundary approval overspends cash or source POP")
    skip = make()
    skip.root.flags["MD_skip_treasury_cost"] = skip.origin.flags["MD_skip_treasury_cost"] = D(0)
    request(skip)
    accept(skip)
    check(skip.root.variables["treasury"] == D(100 - payment)
          and skip.origin.variables["treasury"] == D(100 + payment), "History skip flag creates an unfunded payment")
    selected = make()
    selected.root.states.insert(0, State(owner="A", controller="B"))
    selected.origin.states.insert(0, State(population=D(per_origin), owner="B", controller="B"))
    request(selected)
    accept(selected)
    check(selected.root.states[0].population == 1_000_000
          and selected.root.states[1].population == initial_state_pop + population, "Approval changes an uncontrolled state")
    check(selected.origin.states[0].population == per_origin
          and selected.origin.states[1].population == initial_state_pop - per_origin, "Approval chooses an insufficient source state")
    selected.advance_days(D(1) / 24)
    selected_notice = next(item for item in selected.open_events if item[1] == "mdcw_guest_workers.30")
    check(selected_notice[4].get("mdcw_gw_origin_state") is selected.origin.states[1]
          and selected_notice[4].get("mdcw_gw_destination_state") is selected.root.states[1],
          "Reported states differ from the selected eligible states when other owned states are skipped")
    if population == 100000:
        check(selected_notice[4].get("mdcw_gw_origin_state_2") is selected.origin.states[2]
              and selected.origin.states[2].population == initial_state_pop - 50000,
              "The second source rerolls to an insufficient/duplicate state or loses the wrong population")
    invalid_targets = ["mdcw_gw_origin_state", "mdcw_gw_destination_state"]
    if population == 100000: invalid_targets.append("mdcw_gw_origin_state_2")
    for invalid_state in invalid_targets:
        reroll = make()
        reroll.root.states.append(State(owner="A", controller="A"))
        reroll.origin.states.append(State(owner="B", controller="B"))
        request(reroll)
        waiting = offer(reroll)
        chosen = waiting[4][invalid_state]
        chosen.controller = "B" if invalid_state == "mdcw_gw_destination_state" else "A"
        check(reroll.call(f"mdcw_gw_agreement_available_{population}", trigger=True),
              "No-reroll fixture lacks a different eligible state")
        before = financial_population(reroll)
        resident_before = resident_snapshot(reroll)
        receipt_before = arrival_receipt_snapshot(reroll)
        reroll.choose(waiting, "accept")
        expected = deepcopy(before)
        expected[0] = (expected[0][0], expected[0][1], D(1000), expected[0][3])
        check(financial_population(reroll) == expected and resident_snapshot(reroll) == resident_before
              and arrival_receipt_snapshot(reroll) == receipt_before and pending_cleared(reroll),
              "Acceptance rerolls an invalid preselected state instead of refunding without POP/stock/cost changes")
        check("mdcw_guest_workers.30" not in reroll.delivered
              and "mdcw_guest_workers.32" in reroll.delivered,
              "A failed exact-state revalidation reports a successful move")

    # Wait out success restrictions explicitly before a real reverse agreement.
    machine.advance_days(60)
    machine.root, machine.origin = sender, receiver
    machine.current = machine.previous = machine.root
    check(not machine.test(first(decision, "available", [])), "GDP/c gap permits a lower-income reverse import")
    machine.root.variables["gdp_per_capita"] = D(5)
    machine.origin.variables["gdp_per_capita"] = D(2)
    check(machine.test(first(decision, "available", [])), "Valid reverse request is unavailable")
    request(machine)
    accept(machine)
    check(all(sum(state.population for state in c.states) == 1_000_000 and c.variables["treasury"] == 100
              and c.variables["mdcw_gw_net_emigration_k"] == 0
              and c.variables["mdcw_gw_remittance_pool_m"] == 0 for c in machine.countries.values()),
          "Approved physical round trip creates POP/cash/remittances")

    expired = make()
    original = financial_population(expired)
    request(expired)
    expired.advance_days(17)
    check(financial_population(expired) == original and pending_cleared(expired),
          "Unanswered request watchdogs do not refund PP and release both countries")
    check(not any(c.flags.keys() & {"mdcw_gw_sending_cooldown", "mdcw_gw_receiving_cooldown"}
                  for c in expired.countries.values()), "Expired request starts a success cooldown")
    check(not expired.test(first(decision, "available", [])),
          "A timed-out request can reuse its sender before the old popup resolves")
    before = persistent_snapshot(expired, exclude_flags={"mdcw_gw_offer_window_open"})
    stale = [item for item in expired.open_events if item[1] == offer_id][0]
    # Native timeout chooses the first option. It happens on day 18, after the
    # day-17 watchdog has refunded and cleared this still-open popup's request.
    expired.advance_days(1)
    expired.choose(stale, 0)
    check(persistent_snapshot(expired, exclude_flags={"mdcw_gw_offer_window_open"}) == before,
          "Accept-first native timeout after expiry can still transfer/refund")
    check("mdcw_gw_offer_window_open" not in expired.origin.flags
          and expired.test(first(decision, "available", [])),
          "Old popup resolution does not release its sender for a fresh request")
    # The sender watchdog must recover independently if the receiver's timer
    # never arrives, restoring callback ROOT/FROM before refund and cleanup.
    fallback = make()
    original = financial_population(fallback)
    request(fallback)
    fallback.queue = [item for item in fallback.queue if item[1] != "mdcw_guest_workers.90"]
    fallback.advance_days(17)
    check("mdcw_guest_workers.92" in fallback.delivered
          and financial_population(fallback) == original and pending_cleared(fallback),
          "Sender watchdog cannot independently restore receiver scope and refund once")
    # A watchdog from an old resolved agreement must not expire a new one.
    young = make()
    request(young)
    young.choose(offer(young), "refuse")
    young.advance_days(14)  # Day 15, before old day-17 watchdogs.
    request(young)
    before = financial_population(young)
    young.advance_days(2)
    check(financial_population(young) == before
          and "mdcw_gw_request_pending" in young.countries["A"].flags,
          "An old watchdog expires/refunds a younger request")
    young.advance_days(15)
    check(pending_cleared(young) and young.countries["A"].political_power == 1000,
          "New request's own watchdog never cleans up after old watchdog is ignored")
    for missing in ("A", "B"):
        orphan = make()
        request(orphan)
        orphan.countries[missing].exists = False
        orphan.advance_days(17)
        survivor = orphan.countries["B" if missing == "A" else "A"]
        check(not survivor.flags.keys() & {"mdcw_gw_request_pending", "mdcw_gw_offer_pending"},
              "Country disappearance leaves the surviving partner locked")
        if missing == "B":
            check(survivor.political_power == 1000, "Missing sender costs receiver PP permanently")
    exercise_concurrency(effects, triggers, events, decision, cost, population)
    exercise_remittances(effects, triggers, population // 1000, remittance)


def exercise_success_cooldowns(effects, triggers, events, decisions):
    """A successful request locks all sizes and partners for exactly 60 days."""
    for population, cost, tier in ((25000, 75, 1), (50000, 125, 2), (100000, 200, 3)):
        machine = ScriptMachine(effects, triggers, events)
        extra = Country("C")
        extra.states = [State(owner="C", controller="C")]
        extra.ideas = set(machine.root.ideas)
        machine.countries["C"] = extra
        prepare_tier_fixture(machine, 100000)
        original_sender = machine.origin
        machine.root.political_power -= cost
        machine.execute(first(decisions[f"mdcw_gw_recruit_{population}"], "complete_effect", []))
        machine.advance_days(1)
        offer = next(item for item in machine.open_events if item[1] == f"mdcw_guest_workers.{tier}")
        machine.choose(offer, "accept")
        machine.origin = extra
        for next_population in (25000, 50000, 100000):
            check(not machine.test(first(decisions[f"mdcw_gw_recruit_{next_population}"], "available", [])),
                  "Receiver can bypass success cooldown by changing recruitment size or donor")
        # Pending bookkeeping cleanup must never remove the receiver's timer.
        machine.call("mdcw_gw_clear_pending")
        machine.in_scope(original_sender, lambda: machine.call("mdcw_gw_clear_pending"))
        check(machine.root.flags.get("mdcw_gw_receiving_cooldown") == 60
              and "mdcw_gw_sending_cooldown" not in original_sender.flags,
              "Pending cleanup removes the receiver cooldown or success locks the sender")
        # Another receiver can immediately conclude any tier with the same sender.
        # Flags left in an older save, and the sender's own import cooldown, must
        # not block exports either. Exercise actual accepted callbacks, not just UI.
        for next_population, next_cost, next_tier in ((25000, 75, 1), (50000, 125, 2), (100000, 200, 3)):
            for legacy in (False, True):
                probe = deepcopy(machine)
                probe.root = probe.current = probe.countries["C"]
                probe.origin = probe.countries["B"]
                probe.root.variables["gdp_per_capita"] = D(5)
                if legacy:
                    probe.origin.flags.update(mdcw_gw_sending_cooldown=D(60),
                                              mdcw_gw_receiving_cooldown=D(60))
                decision = decisions[f"mdcw_gw_recruit_{next_population}"]
                check(probe.test(first(decision, "available", [])),
                      "A sender cannot immediately export to another recipient (including legacy flags)")
                sender_pop = sum(s.population for s in probe.origin.states)
                receiver_pop = sum(s.population for s in probe.root.states)
                probe.root.political_power -= next_cost
                probe.execute(first(decision, "complete_effect", []))
                probe.advance_days(1)
                second_offer = next(item for item in probe.open_events
                                    if item[1] == f"mdcw_guest_workers.{next_tier}")
                probe.choose(second_offer, "accept")
                check(sum(s.population for s in probe.origin.states) == sender_pop - next_population
                      and sum(s.population for s in probe.root.states) == receiver_pop + next_population
                      and probe.root.flags.get("mdcw_gw_receiving_cooldown") == 60
                      and probe.countries["A"].flags.get("mdcw_gw_receiving_cooldown") == 59,
                      "A second recipient's agreement fails, or changes the original recipient's cooldown")
        machine.advance_days(59)
        check(machine.root.flags.get("mdcw_gw_receiving_cooldown") == 1
              and "mdcw_gw_sending_cooldown" not in original_sender.flags,
              "The receiver cooldown expires early or the sender gets a cooldown")
        for next_population in (25000, 50000, 100000):
            decision = decisions[f"mdcw_gw_recruit_{next_population}"]
            check(not machine.test(first(decision, "available", [])),
                  "A different donor bypasses receiver cooldown on day 59")
            machine.origin = original_sender
            check(not machine.test(first(decision, "available", [])),
                  "The original pair bypasses receiver cooldown on day 59")
            machine.origin = extra
        machine.advance_days(1)
        check("mdcw_gw_receiving_cooldown" not in machine.root.flags
              and "mdcw_gw_sending_cooldown" not in original_sender.flags,
              "A success cooldown persists after the full 60 days")
        for next_population in (25000, 50000, 100000):
            decision = decisions[f"mdcw_gw_recruit_{next_population}"]
            check(machine.test(first(decision, "available", [])),
                  "A different donor remains blocked when receiver cooldown ends on day 60")
            machine.origin = original_sender
            check(machine.test(first(decision, "available", [])),
                  "The original pair remains blocked after the receiving cooldown ends")
            machine.origin = extra


def exercise_early_retry_watchdogs(effects, triggers, events, decisions):
    """Old timers must not expire a day-1 retry while it is only16 days old."""
    pending = {"mdcw_gw_request_pending", "mdcw_gw_offer_pending"}
    success = {"mdcw_gw_receiving_cooldown", "mdcw_gw_sending_cooldown"}
    for tier, population, cost in ((1, 25000, 75), (2, 50000, 125), (3, 100000, 200)):
        for sender_only in (False, True):
            machine = prepare_tier_fixture(ScriptMachine(effects, triggers, events), population)
            decision = decisions[f"mdcw_gw_recruit_{population}"]
            def request():
                machine.root.political_power -= cost
                machine.execute(first(decision, "complete_effect", []))
                if sender_only:
                    machine.queue = [item for item in machine.queue if item[1] != "mdcw_guest_workers.90"]
            def resources():
                return deepcopy([(country.tag, country.variables, country.political_power,
                                  country.ideas, [(state.population, state.owner, state.controller)
                                                  for state in country.states], country.military_manpower,
                                  country.dynamic_modifiers, country.refreshes, country.dynamic_refreshes)
                                 for country in machine.countries.values()])
            request()
            machine.advance_days(1)
            original_offer = next(item for item in machine.open_events
                                  if item[1] == f"mdcw_guest_workers.{tier}")
            machine.choose(original_offer, "refuse")
            check(machine.root.political_power == 1000
                  and machine.test(first(decision, "available", [])),
                  "Day-1 refusal fails to refund/unlock an immediate retry")
            request()
            charged = resources()
            machine.advance_days(15)  # Day16; the retry is15 days old.
            check(resources() == charged and machine.root.political_power == D(1000 - cost)
                  and "mdcw_gw_request_pending" in machine.root.flags,
                  "Immediate retry changes resources before either old watchdog is due")
            machine.advance_days(1)  # Old timers: day17; fresh request age16.
            check(resources() == charged and machine.root.political_power == D(1000 - cost)
                  and "mdcw_gw_request_pending" in machine.root.flags
                  and "mdcw_gw_offer_pending" in machine.origin.flags
                  and "mdcw_guest_workers.92" not in machine.delivered,
                  f"Tier {population}: old {'sender' if sender_only else 'receiver'} watchdog expires a16-day-old retry")
            machine.advance_days(1)  # Fresh timers: day18; fresh request age17.
            check(machine.root.political_power == 1000
                  and all(not country.flags.keys() & (pending | success)
                          for country in machine.countries.values())
                  and all(not country.variables.keys() & {"mdcw_gw_partner", "mdcw_gw_pending_tier", "mdcw_gw_pending_pp"}
                          for country in machine.countries.values())
                  and machine.delivered.count("mdcw_guest_workers.32") == 1
                  and (not sender_only or machine.delivered.count("mdcw_guest_workers.92") == 1),
                  "Retry's own17-day watchdog fails to refund once and clear both roles")
            before = resources()
            machine.advance_days(3)
            check(resources() == before and machine.root.political_power == 1000,
                  "Overlapping old/new watchdogs refund the retried request more than once")


def exercise_stale_offer_window(effects, triggers, events, decisions):
    """An expired popup must never approve a later request for the same tier."""
    ui = "mdcw_gw_offer_window_open"
    costs = {25000: 75, 50000: 125, 100000: 200}
    check(ui not in {value for key, _, value in walk(effects["mdcw_gw_clear_pending"])
                     if key == "clr_country_flag"},
          "Pending cleanup clears an offer window which can still auto-select accept")
    for tier, population in enumerate(costs, 1):
        machine = ScriptMachine(effects, triggers, events)
        extra = Country("C")
        extra.states = [State(owner="C", controller="C")]
        extra.ideas = set(machine.root.ideas)
        machine.countries["C"] = extra
        prepare_tier_fixture(machine, 100000)
        def pair(receiver, sender):
            machine.current = machine.root = machine.previous = machine.countries[receiver]
            machine.origin = machine.countries[sender]
        def request(size):
            machine.root.political_power -= costs[size]
            machine.execute(first(decisions[f"mdcw_gw_recruit_{size}"], "complete_effect", []))
        request(population)
        check(machine.countries["B"].flags.get(ui) == 19,
              "Request does not give its sender the 19-day popup lifecycle failsafe")
        machine.advance_days(17)
        stale = next(item for item in machine.open_events if item[1] == f"mdcw_guest_workers.{tier}")
        check(machine.countries["A"].political_power == 1000
              and machine.countries["B"].flags.get(ui) == 2,
              "Watchdog does not refund while preserving the still-open popup's sender lock")
        # At day 17 the old agreement is gone, but its popup still exists until
        # day 18. Block reuse of that sender in either role and for every tier.
        for receiver, sender in (("A", "B"), ("C", "B"), ("B", "A"), ("B", "C")):
            pair(receiver, sender)
            for size in costs:
                decision = decisions[f"mdcw_gw_recruit_{size}"]
                check(not machine.test(first(decision, "available", [])),
                      "An unresolved old popup permits country reuse in another role, tier or partner")
                before = persistent_snapshot(machine)
                queued = len(machine.queue)
                request(size)
                check(persistent_snapshot(machine) == before and len(machine.queue) == queued,
                      "A stale same-pair/tier request overwrites state instead of atomically refunding")
        # The refunded receiver may use another source. The old source's popup
        # must not approve, clear or refund this newer agreement when it expires.
        pair("A", "C")
        for size in costs:
            check(machine.test(first(decisions[f"mdcw_gw_recruit_{size}"], "available", [])),
                  "An old sender's UI lock unnecessarily blocks the receiver's other partners")
        request(population)
        machine.advance_days(1)
        before = persistent_snapshot(machine, exclude_flags={ui})
        machine.choose(stale, 0)  # Native day-18 timeout chooses the old top accept.
        check(persistent_snapshot(machine, exclude_flags={ui}) == before,
              "Old accept-first popup approves/refunds/clears a newer agreement")
        check(ui not in machine.countries["B"].flags
              and ui in machine.countries["C"].flags
              and "mdcw_gw_request_pending" in machine.countries["A"].flags,
              "Old popup cleanup releases the wrong sender or damages the newer pending agreement")
        fresh = next(item for item in machine.open_events
                     if item[1] == f"mdcw_guest_workers.{tier}" and item[2] is machine.countries["C"])
        machine.choose(fresh, "accept")
        check(sum(state.population for state in machine.countries["B"].states) == 1_000_000
              and machine.countries["B"].variables["treasury"] == 100
              and machine.countries["B"].political_power == 1000,
              "The expired sender participates in the replacement agreement")
        check(sum(state.population for state in machine.countries["A"].states) == D(1_000_000 + population)
              and sum(state.population for state in machine.countries["C"].states) == D(1_000_000 - population)
              and machine.countries["A"].political_power == D(1000 - costs[population]),
              "Replacement agreement is not approved exactly once after the old timeout is ignored")
        # If the popup never resolves at all, the UI-only lock must eventually
        # expire; it must not turn a refusal into a 60-day success restriction.
        failsafe = ScriptMachine(effects, triggers, events)
        prepare_tier_fixture(failsafe, 100000)
        failsafe.root.political_power -= costs[population]
        failsafe.execute(first(decisions[f"mdcw_gw_recruit_{population}"], "complete_effect", []))
        failsafe.advance_days(19)
        check(ui not in failsafe.origin.flags
              and failsafe.root.political_power == 1000
              and failsafe.test(first(decisions[f"mdcw_gw_recruit_{population}"], "available", [])),
              "The popup lifecycle lock fails to release after its 19-day fallback")


def exercise_concurrency(effects, triggers, events, decision, cost, population):
    machine = ScriptMachine(effects, triggers, events)
    extra = Country("C")
    extra.states = [State(owner="C", controller="C")]
    extra.ideas = set(machine.root.ideas)
    machine.countries["C"] = extra
    prepare_tier_fixture(machine, 100000)
    machine.root.political_power -= cost
    machine.execute(first(decision, "complete_effect", []))
    before = persistent_snapshot(machine)
    for receiver, sender in (("C", "B"), ("A", "C"), ("B", "C"), ("C", "A")):
        machine.current = machine.root = machine.previous = machine.countries[receiver]
        machine.origin = machine.countries[sender]
        check(not machine.test(first(decision, "available", [])), "Pending-country concurrency gate is missing")
        machine.root.political_power -= cost
        machine.execute(first(decision, "complete_effect", []))
        check(persistent_snapshot(machine) == before, "Rejected concurrent request overwrites another request")


# IMPERIA CW — Cold War: UI repaint notifications are not economic or contract mutations.
# Keep every other persistent variable in replay/expiry comparisons; the Ministry
# regression suite separately checks that real UI transitions increment this key.
def persistent_snapshot(machine, exclude_flags=()):
    return deepcopy([(c.tag, {key: value for key, value in c.variables.items() if key != 'gw_ui_dirty'},
                      {key: value for key, value in c.flags.items() if key not in exclude_flags},
                      c.ideas, c.political_power,
                      [(s.population, s.owner, s.controller) for s in c.states], c.refreshes,
                      (c.dynamic_modifiers, c.dynamic_refreshes, c.military_manpower))
                     for c in machine.countries.values()])


def exercise_remittances(effects, triggers, population_k, remittance):
    net, pool = "mdcw_gw_net_emigration_k", "mdcw_gw_remittance_pool_m"
    def make(balance=0, income=0):
        machine = ScriptMachine(effects, triggers)
        machine.current.variables.update({net: D(balance), pool: D(income)})
        return machine
    def export(machine):
        machine.call(f"mdcw_gw_add_emigration_{population_k * 1000}")
    def receive(machine, times=1):
        for _ in range(times):
            machine.call(f"mdcw_gw_apply_immigration_{population_k * 1000}")

    machine = make()
    for _ in range(5):
        export(machine)
        check(machine.current.variables[pool] == D(remittance), "Round-trip export accumulates extra remittances")
        receive(machine)
        check(machine.current.variables[net] == machine.current.variables[pool] == 0,
              "Round trip retains a remittance pool without net emigration")
    machine = make(-population_k, 0)
    export(machine)
    check(machine.current.variables[net] == machine.current.variables[pool] == 0,
          "Re-exporting imported population creates remittances")
    machine = make(-population_k * 2, 0)
    export(machine)
    check(machine.current.variables[net] < 0 and machine.current.variables[pool] == 0,
          "A net importer earns a partial-export remittance")
    machine = make(-D(population_k) / 2, 0)
    export(machine)
    check(machine.current.variables[pool] == D(remittance) / 2,
          "Crossing zero credits gross exports instead of newly positive net exports")
    machine = make(population_k * 2, remittance * 2)
    receive(machine)
    check(machine.current.variables[pool] == D(remittance), "Imports do not scale an existing pool proportionally")
    receive(machine, times=2)
    check(machine.current.variables[net] < 0 and machine.current.variables[pool] == 0,
          "Imports crossing zero leave stale remittance income")
    machine = make(1000, 2999)
    export(machine)
    check(machine.current.variables[pool] == 3000, "Pool is not capped at 3 billion/week")
    machine.call("mdcw_gw_weekly_update")
    check(machine.current.variables[pool] == D("2999.7"), "Cap pool does not decay by 0.01% weekly")
    machine = make(population_k, remittance)
    machine.call("mdcw_gw_weekly_update")
    check(machine.current.variables[pool] == D(remittance) * D("0.9999"), "Weekly decay differs from 0.9999")
    for _ in range(51): machine.call("mdcw_gw_weekly_update")
    expected = D(remittance) * D("0.9999") ** 52
    check(abs(machine.current.variables[pool] - expected) < D("0.001"), "52-week decay compounds incorrectly")
    for _ in range(1040 - 52): machine.call("mdcw_gw_weekly_update")
    expected = D(remittance) * D("0.9999") ** 1040
    check(abs(machine.current.variables[pool] - expected) < D("0.001"),
          "Twenty-year remittance decay does not preserve the intended slower compounding")
    # Economy refresh can happen repeatedly between weekly settlements. A pure
    # aggregation hook must never change pool, POP or treasury during refresh.
    before = persistent_snapshot(machine)
    expected_income = machine.current.variables[pool] / 1000
    for _ in range(3):
        machine.current.variables["additional_income_rate"] = D(7)
        machine.call("mdcw_gw_add_remittance_income")
        check(machine.current.variables["additional_income_rate"] == D(7) + expected_income,
              "Budget hook has wrong million-to-billion conversion or duplicates income")
    before_core = [(tag, {k: v for k, v in variables.items()
                         if k not in {"additional_income_rate", "mdcw_gw_weekly_income", "gw_dp_bonus_m", "gw_dp_total_income_m"}},
                    flags, ideas, pp, states, refreshes, dynamic)
                   for tag, variables, flags, ideas, pp, states, refreshes, dynamic in before]
    after_core = [(tag, {k: v for k, v in variables.items()
                        if k not in {"additional_income_rate", "mdcw_gw_weekly_income", "gw_dp_bonus_m", "gw_dp_total_income_m"}},
                   flags, ideas, pp, states, refreshes, dynamic)
                  for tag, variables, flags, ideas, pp, states, refreshes, dynamic in persistent_snapshot(machine)]
    check(after_core == before_core, "Budget refresh changes pool, cash or population")
    for balance in (0, -population_k):
        machine = make(balance, remittance)
        machine.call("mdcw_gw_add_remittance_income")
        check(machine.current.variables.get("additional_income_rate", D(0)) == 0,
              "Nonpositive net exporter receives weekly income")
        machine.call("mdcw_gw_weekly_update")
        check(machine.current.variables[pool] == 0, "Weekly cleanup retains pool after net emigration ends")
    machine = make(population_k, remittance)
    machine.current.ideas.clear()
    machine.call("mdcw_gw_add_remittance_income")
    check(machine.current.variables.get("additional_income_rate") == D(remittance) / 1000,
          "Closing the programme deletes already earned remittances")


def check_budget_and_tick():
    money = read_script("common/scripted_effects/00_money_system.txt")
    setup = first(money, "ingame_update_setup", [])
    setup_names = [key for key, _, _ in setup]
    consumers = ("calculate_int_investments_rate", "expense_modifier_calculations",
                 "update_bureaucracy_rate", "update_health_rate", "update_social_rate")
    check(setup_names.count("mdcw_gw_update_resident_costs") == 1
          and "update_state_variables" in setup_names
          and all(name in setup_names for name in consumers)
          and setup_names.index("update_state_variables") < setup_names.index("mdcw_gw_update_resident_costs")
          and all(setup_names.index("mdcw_gw_update_resident_costs") < setup_names.index(name) for name in consumers),
          "Resident costs must refresh once after fresh population and before native budget consumers")
    money_references = {key for key, _, _ in walk(money)}
    money_references.update(value for _, _, value in walk(money) if isinstance(value, str))
    for name in ("health_cost_multiplier_modifier", "social_cost_multiplier_modifier", "bureaucracy_cost_multiplier_modifier"):
        check("modifier@" + name in money_references,
              "Resident cost modifier is not consumed by the native money formulas: " + name)
    income = first(money, "calculate_additional_income_rate", [])
    calls = [i for i, (k, _, v) in enumerate(income) if k == "mdcw_gw_add_remittance_income"]
    check(len(calls) == 1, "Remittance income must enter the native budget exactly once")
    if calls:
        reset = next((i for i, (k, _, v) in enumerate(income)
                      if k == "set_variable" and first(v, "additional_income_rate") == "0"), -1)
        check(reset >= 0 and calls[0] > reset, "Remittance hook must follow income reset")
    actions = read_script("common/on_actions/MD_on_actions.txt")
    paths = []
    weekly_body = None
    def find_calls(block, path=()):
        nonlocal weekly_body
        for index, (key, _, value) in enumerate(block):
            if key == "mdcw_gw_weekly_update":
                paths.append(path + (index,))
                weekly_body = block
            if isinstance(value, list): find_calls(value, path + (key,))
    find_calls(actions)
    check(len(paths) == 1, "Guest-worker decay must run exactly once in existing weekly on-actions")
    if paths: check(any("weekly" in str(part) for part in paths[0]), "Decay is outside weekly on-action")
    if weekly_body:
        names = [key for key, _, _ in weekly_body]
        check(names.index("mdcw_gw_weekly_update") < names.index("update_tension_premium")
              < names.index("ingame_update_setup"), "Weekly decay runs after the MD budget refresh")
    check(not (ROOT / "common/on_actions/mdcw_guest_workers_on_actions.txt").exists(),
          "Separate guest-worker tick duplicates the native weekly integration")


if __name__ == "__main__":
    sys.exit(main())
