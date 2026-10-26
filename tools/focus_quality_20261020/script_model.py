# IMPERIA CW — Cold War: focus quality 20261020 — script model.
"""Strict AST executor for authored transaction arithmetic, not the HOI4 engine.

Native stock/licence/build APIs are modeled explicitly; their rendering and
native implementation still require in-game verification.
"""
import ast
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
import re
from source_edit import ROOT

ns = {'re': re}
parser_file = ROOT / 'tools/israel_1970/validate_content.py'
module = ast.parse(parser_file.read_text(encoding='utf-8'))
functions = [n for n in module.body if isinstance(n, ast.FunctionDef) and n.name in {'tokens', 'parse', 'first', 'values', 'walk'}]
exec(compile(ast.Module(body=functions, type_ignores=[]), str(parser_file), 'exec'), ns)
parse, first, values, walk = (ns[n] for n in ('parse', 'first', 'values', 'walk'))
D = lambda x: Decimal(str(x))


@dataclass
class Country:
    tag: str
    vars: dict = field(default_factory=lambda: {'gdp_total': D(100), 'treasury': D(10), 'debt': D(50)})
    flags: set = field(default_factory=set)
    ideas: dict = field(default_factory=dict)
    licenses: set = field(default_factory=set)
    designs: set = field(default_factory=set)
    techs: set = field(default_factory=set)
    stock: Decimal = D(0)
    xp: Decimal = D(0)
    government: str = 'communism'
    parties: set = field(default_factory=set)
    wars: set = field(default_factory=set)
    dlc: bool = True


@dataclass
class State:
    owner: str
    controller: str
    slots: int = 2
    offices: int = 0
    fossil_powerplant: int = 0
    arms_factory: int = 0


class Model:
    def __init__(self):
        self.countries = {'DDR': Country('DDR'), 'SOV': Country('SOV')}
        self.states = [State('DDR', 'DDR')]
        self.date = '1970.1.1'
        self.functions, self.triggers = {}, {}
        self.events = []
        for stem in ['COLDWAR_DDR_1970_quality', 'COLDWAR_GEN_1970_quality']:
            self.functions.update({k: v for k, _, v in self.read('common/scripted_effects/' + stem + '.txt')})
            self.triggers.update({k: v for k, _, v in self.read('common/scripted_triggers/' + stem + '.txt')})

    def read(self, p):
        return parse((ROOT / p).read_text(encoding='utf-8-sig'))

    def number(self, x, scope):
        if isinstance(x, list):
            value = D(0)
            for key, _, val in x:
                other = self.number(val, scope)
                if key == 'value': value = other
                elif key == 'add': value += other
                elif key == 'subtract': value -= other
                elif key == 'multiply': value *= other
                elif key == 'divide': value /= other
                elif key == 'min': value = min(value, other)
                elif key == 'max': value = max(value, other)
                else: raise AssertionError(('math', key))
            return value
        try: return D(x)
        except Exception:
            if '.' in str(x):
                tag, key = str(x).split('.', 1)
                return self.countries[tag].vars.get(key, D(0))
            return scope.vars.get(str(x), D(0))

    def target(self, tag, scope, root, prev):
        return {'ROOT': root, 'PREV': prev, 'THIS': scope}.get(tag, self.countries.get(tag))

    def compare(self, a, op, b):
        return {'=': a == b, '>': a > b, '<': a < b, '>=': a >= b, '<=': a <= b,
                'greater_than_or_equals': a >= b}[op]

    def condition(self, block, scope, root=None, prev=None):
        root = root or scope
        for key, op, val in block:
            target = self.target(key, scope, root, prev)
            if key == 'OR': ok = any(self.condition([item], scope, root, prev) for item in val)
            elif key == 'AND': ok = self.condition(val, scope, root, prev)
            elif key == 'NOT': ok = not self.condition(val, scope, root, prev)
            elif key == 'always': ok = val == 'yes'
            elif key == 'custom_trigger_tooltip': ok = self.condition([x for x in val if x[0] != 'tooltip'], scope, root, prev)
            elif target is not None: ok = self.condition(val, target, root, scope)
            elif key in self.triggers: ok = self.condition(self.triggers[key], scope, root, prev) == (val == 'yes')
            elif key == 'tag': ok = scope.tag == val
            elif key == 'country_exists': ok = val in self.countries
            elif key == 'has_country_flag': ok = val in scope.flags
            elif key == 'has_idea': ok = val in scope.ideas
            elif key == 'has_tech': ok = val in scope.techs
            elif key == 'has_government': ok = scope.government == val
            elif key == 'has_dlc': ok = scope.dlc
            elif key == 'has_war_with': ok = val in scope.wars
            elif key.endswith('_are_in_power'): ok = key in scope.parties
            elif key == 'date': ok = self.compare(tuple(map(int,self.date.split('.'))), op, tuple(map(int,val.split('.'))))
            elif key == 'has_equipment': ok = self.compare(scope.stock, val[0][1], D(val[0][2]))
            elif key == 'has_license': ok = first(val, 'from') in scope.licenses
            elif key == 'check_variable':
                if first(val, 'var'):
                    ok = self.compare(self.number(first(val,'var'),scope), first(val,'compare'), self.number(first(val,'value'),scope))
                else:
                    name, operator, right = val[0]
                    ok = self.compare(self.number(name,scope),operator,self.number(right,scope))
            elif key == 'any_owned_state':
                ok = any(s.owner == scope.tag and self.condition(val,s,root,scope) for s in self.states)
            elif key == 'is_owned_and_controlled_by':
                owner = self.target(val,scope,root,prev)
                ok = scope.owner == owner.tag and scope.controller == owner.tag
            elif key == 'is_controlled_by': ok = scope.controller == val
            elif key == 'free_building_slots':
                item = next(x for x in val if x[0] == 'size')
                capacity = 20 - scope.fossil_powerplant if first(val,'building') == 'fossil_powerplant' else scope.slots
                ok = self.compare(D(capacity),item[1],D(item[2]))
            elif key == 'has_building':
                item = next(x for x in val if x[0] == 'level')
                ok = self.compare(D(getattr(scope,first(val,'type'))),item[1],D(item[2]))
            else: raise AssertionError(('unsupported trigger', key, val))
            if not ok: return False
        return True

    def run(self, block, scope, root=None, prev=None):
        root = root or scope
        branch = False
        for key, _, val in block:
            target = self.target(key,scope,root,prev)
            if key == 'if':
                branch = self.condition(first(val,'limit',[]),scope,root,prev)
                if branch: self.run([x for x in val if x[0] != 'limit'],scope,root,prev)
            elif key == 'else':
                if not branch: self.run(val,scope,root,prev)
                branch = True
            elif key == 'else_if':
                if not branch and self.condition(first(val,'limit',[]),scope,root,prev):
                    self.run([x for x in val if x[0] != 'limit'],scope,root,prev)
                    branch = True
            elif key in ['custom_effect_tooltip','effect_tooltip','log','force_update_dynamic_modifier']:
                pass
            elif key == 'hidden_effect': self.run(val,scope,root,prev)
            elif target is not None: self.run(val,target,root,scope)
            elif key in self.functions: self.run(self.functions[key],scope,root,prev)
            elif key in ['set_variable','set_temp_variable','add_to_variable']:
                name, _, expression = val[0]
                scope.vars[name] = (scope.vars.get(name,D(0)) if key == 'add_to_variable' else D(0)) + self.number(expression,scope)
            elif key == 'modify_treasury_effect':
                if 'MD_skip_treasury_cost' not in scope.flags:
                    scope.vars['treasury'] += scope.vars['treasury_change']
            elif key == 'modify_debt_effect': scope.vars['debt'] += scope.vars['debt_change']
            elif key == 'set_country_flag': scope.flags.add(first(val,'flag') if isinstance(val,list) else val)
            elif key == 'clr_country_flag': scope.flags.discard(val)
            elif key == 'add_timed_idea': scope.ideas[first(val,'idea')] = int(first(val,'days'))
            elif key == 'army_experience': scope.xp += D(val)
            elif key == 'send_equipment':
                assert first(val,'type') == 'medium_tank_chassis'
                amount=D(first(val,'amount')); assert scope.stock >= amount
                scope.stock -= amount
                self.countries[first(val,'target')].stock += amount
            elif key == 'create_production_license':
                model=first(first(val,'equipment'),'type')
                if model in scope.designs: self.countries[first(val,'target')].licenses.add(scope.tag)
            elif key == 'random_owned_controlled_state':
                eligible=[s for s in self.states if s.owner==scope.tag and s.controller==scope.tag and self.condition(first(val,'limit',[]),s,root,scope)]
                if eligible: self.run([x for x in val if x[0]!='limit'],eligible[0],root,scope)
            elif key == 'add_extra_state_shared_building_slots': scope.slots += int(val)
            elif key == 'add_building_construction':
                kind=first(val,'type'); amount=int(first(val,'level'))
                if kind in ['offices','arms_factory']:
                    assert scope.slots>=amount
                    scope.slots-=amount
                setattr(scope,kind,getattr(scope,kind)+amount)
            elif key == 'country_event': self.events.append((scope.tag,first(val,'id')))
            elif key == 'clamp_variable':
                name=first(val,'var');scope.vars[name]=max(D(first(val,'min')),min(D(first(val,'max')),scope.vars[name]))
            elif key in ['COLDWAR_DDR_change_trust','change_communist_cadres_opinion','change_industrial_conglomerates_opinion','change_the_military_opinion','add_power_balance_value']:
                pass  # Existing native/DDR providers unchanged; transaction tests focus on finance and delivery.
            else: raise AssertionError(('unsupported effect',key,val))

    def call(self, name, tag='DDR'):
        self.run(self.functions[name], self.countries[tag])
