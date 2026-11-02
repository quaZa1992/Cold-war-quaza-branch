# IMPERIA COLD WAR — Israel V2 native domestic programme compiler.
"""Compile actual focus transactions; unresolved catalogue fields are fatal.

The reviewed catalogue is input. Execution, native previews and reconciliation
share typed records. No catalogue English sentence is executed as game code.
"""
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/israel_1970'))
from player_rewards import LABELS

MARKER = '# IMPERIA COLD WAR — Israel V2 domestic national programmes.\n'
STATES = {'Tel Aviv': 204, 'Haifa': 205, 'Negev': 206, 'Jerusalem': 1253,
          'West Bank': 208, 'Gaza': 209, 'Sinai': 213, 'Golan': 587}
BUILDINGS = {'Civilian Factory': 'industrial_complex', 'Military Factory': 'arms_factory',
             'Office District': 'offices', 'Agricultural District': 'agriculture_district',
             'Infrastructure': 'infrastructure', 'Civilian Shelter': 'civilian_shelter',
             'Land Fort': 'bunker', 'Land Forts': 'bunker'}
RESEARCH = {'Electronics': 'CAT_electronics', 'Industry': 'CAT_industry',
            'Agriculture': 'CAT_agriculture', 'Armor': 'CAT_armor', 'Aircraft': 'CAT_aircraft',
            'Nuclear Reactors': 'CAT_nuclear_reactors', 'Nuclear Weapons': 'nuclear',
            'Encryption': 'CAT_encryption', 'Decryption': 'CAT_decryption',
            'Infantry Weapons': 'CAT_infantry_weapons', 'Artillery': 'CAT_towed_artillery',
            'Naval Engineering': 'naval_equipment', 'Corvettes': 'CAT_corvettes',
            'Military Electronics': 'CAT_military_electronics', 'Medium Aircraft': 'CAT_medium_aircraft'}
RESEARCH['Nuclear Weapons'] = 'CAT_nuclear_weapons'
MODIFIERS = {v: k for k, v in LABELS.items()}
MODIFIERS.update({'Division Organisation': 'army_org_factor',
                  'Casualty Trickleback': 'casualty_trickleback',
                  'Personal Tax Income': 'population_tax_income_multiplier_modifier',
                  'Corporate Tax Income': 'corporate_tax_income_multiplier_modifier',
                  'Inflation Spending Multiplier': 'inflation_cost_multiplier_modifier',
                  'Controlled Non-Core Territory: Compliance Gain': 'compliance_gain',
                  'Controlled Non-Core Territory: Local Garrison Requirement': 'required_garrison_factor',
                  'Controlled Non-Core Territory: Damage to Garrisons': 'resistance_damage_to_garrison'})
FACTIONS = {'Industrial Conglomerates Opinion': 'industrial_conglomerates',
            'Religious Institutions Opinion': 'the_priesthood', 'Labor Unions Opinion': 'labour_unions',
            'Small and Medium Business Owners Opinion': 'small_medium_business_owners',
            'The Military Opinion': 'the_military'}


def number(value):
    value = Decimal(str(value)).quantize(Decimal('.00001'))
    return format(value, 'f').rstrip('0').rstrip('.') or '0'


def block(name, body):
    return name + ' = {\n' + body + '\n}'


def conditional(condition, body, otherwise=''):
    result = block('if', block('limit', condition) + '\n' + body)
    return result + ('\n' + block('else', otherwise) if otherwise else '')


def amount(value):
    match = re.search(r'[+-]?\d+(?:\.\d+)?', str(value).replace(',', ''))
    if not match:
        raise ValueError(('Missing numeric amount', value))
    return float(match[0])


def gdp_quote(var, fraction):
    return f'set_variable = {{ {var} = gdp_total }}\nmultiply_variable = {{ {var} = {number(fraction)} }}'


def money(var, kind='treasury', sign=1):
    return (f'set_temp_variable = {{ {kind}_change = {var} }}\n' +
            (f'multiply_temp_variable = {{ {kind}_change = -1 }}\n' if sign < 0 else '') +
            f'modify_{kind}_effect = yes')


def build(data, excluded=()):
    core = Core(data, set(excluded))
    return core.build()


class Core:
    def __init__(self, data, excluded):
        self.data, self.excluded = data, excluded
        self.groups = {g['id']: g for g in data['groups']}
        self.nodes = {n['id']: n for n in data['nodes']}
        self.effects, self.triggers, self.dynamic, self.ideas = {}, {}, {}, {}
        self.loc, self.actions, self.records = {}, {}, []
        self.errors = []
        self.quotes, self.initial, self.reconcile, self.timers = [], [], [], []
        self.preview_quotes = []
        self.group_mods = defaultdict(set)

    def modifier_variable(self, group, modifier):
        var = f'ISR2_{group}_{modifier}'
        label = LABELS.get(modifier, next((k for k,v in MODIFIERS.items() if v==modifier), modifier))
        inverse = modifier.endswith('_cost_multiplier_modifier') or modifier in {
            'corruption_cost_factor', 'receiving_investment_cost_modifier',
            'interest_rate_multiplier_modifier', 'mdcw_cw_market_exposure',
            'supply_consumption_factor', 'training_time_army_factor'}
        fmt = '-=%1' if inverse else '+=%1'
        if modifier == 'productivity_growth_modifier':
            fmt = '+=2'
        if modifier == 'interest_rate_multiplier_modifier':
            fmt = '-=2'
        self.loc[var] = label + ': $RIGHT|' + fmt + '$' + (' percentage points' if modifier=='interest_rate_multiplier_modifier' else '')
        self.group_mods[group].add(modifier)
        return var

    def add_modifier(self, n, modifier, value, mods, preview):
        mods[modifier] = mods.get(modifier, 0) + value
        var = self.modifier_variable(n['group'], modifier)
        preview.append(f'add_to_variable = {{ {var} = {number(value)} tooltip = {var} }}')

    def asset(self, n, rows, available, actual, preview):
        """Group state building grants into one atomic, capacity-guarded block."""
        projects = defaultdict(lambda: defaultdict(int))
        consumed = set()
        for index, e in enumerate(rows):
            if ': ' not in e['label']:
                continue
            state, kind = e['label'].rsplit(': ', 1)
            if kind == 'Shared Building Slots':
                consumed.add(index)
                continue
            if kind not in BUILDINGS:
                continue
            consumed.add(index)
            projects[state][BUILDINGS[kind]] += int(amount(e['value']))
        for state_name, buildings in projects.items():
            province = state_name == 'Selected Controlled Sinai Province'
            state = 213 if province else STATES.get(state_name)
            eligible = 'is_owned_by = ISR\nis_controlled_by = ISR\nis_core_of = ISR'
            if province:
                eligible = 'is_controlled_by = ISR\nowner = { exists = yes }'
            for building, levels in buildings.items():
                cap = 7 if building in {'bunker','coastal_bunker'} else self.building_cap(building)
                if building in {'bunker','coastal_bunker'}:
                    eligible += f'\nfree_building_slots = {{ building = {building} size > {levels-1} province = 1155 }}'
                    available.append('controls_province = 1155')
                else:
                    eligible += f'\ncheck_variable = {{ var = building_level@{building} value = {cap-levels} compare = less_than_or_equals }}'
                    if building in {'industrial_complex','arms_factory','offices','agriculture_district'}:
                        eligible += f'\nfree_building_slots = {{ building = {building} size > {levels-1} }}'
            if state is None:
                condition = block('any_owned_state', eligible)
                target = 'random_owned_state'
                inside = block('limit', eligible)
                # Native random state selection uses the deterministic game RNG,
                # synchronized in MP. There is no extra player target menu.
            else:
                condition = block(str(state), eligible)
                target, inside = str(state), ''
            available.append(condition)
            reward = [f'add_extra_state_shared_building_slots = {sum(buildings.values())}']
            for building, levels in buildings.items():
                clause = f'type = {building} level = {levels} instant_build = yes'
                if building in {'bunker','coastal_bunker'}:
                    # Province1155 is the westernmost northern Sinai province,
                    # verified from live state membership and map centroids.
                    reward.append('add_building_construction = { ' + clause + ' province = { id = 1155 } }')
                else:
                    reward.append('add_building_construction = { ' + clause + ' }')
            code = block(target, inside + '\n' + '\n'.join(reward))
            actual.append(code)
            preview.append(code)
        return consumed

    @staticmethod
    def building_cap(building):
        # Read live MD definitions rather than maintaining an invented cap list.
        text = (ROOT/'common/buildings/00_buildings.txt').read_text(encoding='utf-8-sig')
        start = re.search(r'(?m)^\s*' + re.escape(building) + r'\s*=\s*\{', text)
        if not start:
            raise ValueError(('Missing building definition', building))
        depth, end = 1, start.end()
        while depth:
            depth += (text[end] == '{') - (text[end] == '}')
            end += 1
        body = text[start.end():end]
        cap = re.search(r'(?m)^\s*(?:max_level|state_max)\s*=\s*(\d+)', body)
        if not cap:
            raise ValueError(('Missing native building cap', building))
        return int(cap[1])

    def compile_node(self, n):
        fid, key, group = n['id'], n['id'][5:], n['group']
        rows = n['effects']
        available, actual, preview, mods, streams = [], [], [], {}, []
        consumed = self.asset(n, rows, available, actual, preview)
        for i, e in enumerate(rows):
            if i in consumed:
                continue
            label, value, native = e['label'], str(e.get('value', '')), e.get('native_key')
            if native in {'treasury','debt'}:
                quote = f'ISR2_quote_{key}_{i}'
                fraction = e['amount']
                self.quotes.append(gdp_quote(quote, abs(fraction)))
                code = money(quote, native, 1 if fraction > 0 else -1)
                actual.append(code); preview.append(code)
            elif native == 'weekly_budget':
                quote = f'ISR2_weekly_{key}_{i}'
                self.quotes.append(gdp_quote(quote, abs(e['amount'])))
                streams.append(dict(variable=quote, sign=1 if e['amount']>0 else -1,
                                    weeks=e.get('scope') if isinstance(e.get('scope'),int) else None))
                token = quote + '_tt'
                self.loc[token] = label + ': ' + ('§G+' if e['amount']>0 else '§R-') + '[?' + quote + '|5] billion per week§!'
                preview.append('custom_effect_tooltip = ' + token)
            elif native:
                self.add_modifier(n, native, e['amount'], mods, preview)
            elif label == 'Political Power':
                actual.append('add_political_power = ' + number(amount(value)))
                preview.append(actual[-1])
            elif label == 'Stability':
                actual.append('add_stability = ' + number(amount(value)/100))
                preview.append(actual[-1])
            elif label == 'Corruption':
                actual.append('decrease_corruption = yes'); preview.append(actual[-1])
            elif label in FACTIONS:
                code = f'set_temp_variable = {{ temp_opinion = {number(amount(value))} }}\nchange_{FACTIONS[label]}_opinion = yes'
                actual.append(code); preview.append(code)
            elif label in {'Army Experience','Air Experience','Navy Experience'}:
                code = label.split()[0].lower() + '_experience = ' + number(amount(value))
                actual.append(code); preview.append(code)
            elif label == 'Research Bonus':
                match = re.fullmatch(r'(\d+) x (\d+)%: (.+)', value)
                category = RESEARCH.get(match[3]) if match else None
                if not category:
                    self.errors.append((fid, label, value)); continue
                code = ('add_tech_bonus = { name = ' + fid + '_research category = ' + category +
                        f' uses = {match[1]} bonus = {number(int(match[2])/100)} }}')
                self.loc[fid+'_research'] = n['label']
                actual.append(code); preview.append(code)
            elif label == 'Doctrine Cost Reduction':
                code = ('add_doctrine_cost_reduction = { name = ' + fid +
                        '_doctrine cost_reduction = 0.5 uses = 1 category = land_doctrine }')
                self.loc[fid+'_doctrine'] = n['label']
                actual.append(code); preview.append(code)
            elif label == 'Removes National Spirit' and key == 'settled_skills':
                actual.append('remove_ideas = ISR2_start_absorption'); preview.append(actual[-1])
            elif key == 'settled_skills' and label in {'Research Speed','Social Spending Cost'}:
                # These rows describe the actual starting-spirit removal,
                # not a second permanent reward on top of removing its penalty.
                continue
            elif label in MODIFIERS and '%' in value:
                self.add_modifier(n, MODIFIERS[label], amount(value)/100, mods, preview)
            else:
                self.errors.append((fid, label, value))
        self.records.append(dict(id=fid, key=key, group=group, modifiers=mods, streams=streams,
                                 programme=n.get('programme'), focus_cycle=n.get('focus_cycle')))
        self.actions[fid] = dict(available='\n'.join(available), reward='\n'.join(actual), preview='\n'.join(preview))

    def build(self):
        for n in self.data['nodes']:
            if n['id'] not in self.excluded:
                self.compile_node(n)
        self.materialize()
        files = {'common/scripted_effects/ISR2_core_effects.txt': MARKER + '\n\n'.join(block(k,v) for k,v in self.effects.items()),
                 'common/scripted_triggers/ISR2_core_triggers.txt': MARKER + '\n\n'.join(block(k,v) for k,v in self.triggers.items()),
                 'common/dynamic_modifiers/ISR2_core_dynamic_modifiers.txt': MARKER + '\n\n'.join(block(k,v) for k,v in self.dynamic.items()),
                 'common/ideas/ISR2_core_ideas.txt': MARKER + block('ideas', block('country','\n'.join(block(k,v) for k,v in self.ideas.items())))}
        return dict(files=files, actions=self.actions, loc=self.loc, records=self.records,
                    quotes='ISR2_refresh_core_quotes = yes', unresolved=self.errors,
                    daily='ISR2_core_daily = yes', refresh='ISR2_core_refresh = yes', init='ISR2_core_init = yes')

    def materialize(self):
        reconcile = ['set_variable = { ISR2_core_weekly_income = 0 }',
                     'set_variable = { ISR2_core_weekly_expense = 0 }']
        group_any = defaultdict(list)
        for group, mods in self.group_mods.items():
            for mod in sorted(mods):
                reconcile.append(f'set_variable = {{ ISR2_{group}_{mod} = 0 }}')
        rearm=[]
        for record in self.records:
            fid, key, group = record['id'], record['key'], record['group']
            n=self.nodes[fid]
            party=self.groups[group].get('runtime_party_trigger')
            base_guard=['ISR2_is_scenario = yes','check_variable = { gdp_total > 0 }']
            if party:
                base_guard.append(party+' = yes')
            base_guard += [self.actions[fid]['available'], 'NOT = { has_country_flag = ISR2_core_done_'+key+' }']
            visible=[self.actions[fid]['available']]
            if key=='haolam_detention_review':
                occupied='any_controlled_state = { NOT = { is_core_of = ISR } }'
                base_guard.append(occupied)
                visible.append(occupied)
            if key in {'municipal_lists','brotherhood_compact'}:
                token='ISR2_'+key+'_representation_tt'
                self.loc[token]=('Progress and Development' if key=='municipal_lists' else 'Cooperation and Brotherhood')+' is represented in the governing coalition.'
                base_guard.append('custom_trigger_tooltip = { tooltip = '+token+' OR = { check_variable = { ruling_party = 15 } is_in_array = { array = gov_coalition_array value = 15 } } }')
                visible.append(base_guard[-1])
            eligibility='\n'.join(part for part in base_guard if part)
            self.triggers['ISR2_core_can_'+key]=eligibility
            effect=self.actions[fid]['reward']
            # Price support is part of the same guarded transaction. Quotes are
            # pure arithmetic; only commit may debit real escrow balances.
            costrows=[(i,e) for i,e in enumerate(n['effects']) if e.get('native_key')=='treasury' and e.get('amount',0)<0]
            if costrows:
                index,e=costrows[0]
                quote=f'ISR2_quote_{key}_{index}'
                cls=1 if key in {'ulpan_jobs','recognise_qualifications','ort_workshops','housing_connections',
                    'community_clinics','daycare_shifts','scholarships','gahal_rental_sites','gahal_renewal'} else 0
                procurement={'tal_tank':1,'nesher':2}.get(key,0)
                inputs=(f'set_variable = {{ ISR2_project_cost = {quote} }}\n'
                    f'set_variable = {{ ISR2_project_quote = gdp_total }}\n'
                    f'set_variable = {{ ISR2_project_class = {cls} }}\n'
                    f'set_variable = {{ ISR2_project_procurement = {procurement} }}\n')
                original=money(quote,'treasury',-1)
                effect=effect.replace(original,inputs+'ISR2_project_support_commit = yes\n'+money('ISR2_project_net_cost','treasury',-1),1)
                displayvar='ISR2_preview_net_'+key
                self.preview_quotes.append(inputs+'ISR2_project_support_quote = yes\nset_variable = { '+displayvar+' = ISR2_project_net_cost }')
                displayed=money(displayvar,'treasury',-1)
                self.actions[fid]['preview']=self.actions[fid]['preview'].replace(original,displayed,1)
            term=None
            match=re.search(r'(\d+)\s*(weeks|days)',n.get('programme',''))
            if match:
                term=int(match[1])*(7 if match[2]=='weeks' else 1)
            numeric_mod_scopes=[e['scope']*7 for e in n['effects'] if isinstance(e.get('scope'),int) and e.get('native_key') not in {'weekly_budget','treasury','debt'}]
            if numeric_mod_scopes:
                term=max(numeric_mod_scopes)
            # Modifier envelopes use the policy's actual calendar, not the
            # lifetime of a separate construction receipt or public debt.
            active='has_country_flag = ISR2_core_done_'+key
            if term:
                effect+=f'\nset_country_flag = {{ flag = ISR2_core_term_{key} value = 1 days = {term} }}'
                active+='\nhas_country_flag = ISR2_core_term_'+key
            if party:
                active+='\n'+party+' = yes'
            updates=[]
            for modifier,value in record['modifiers'].items():
                var=self.modifier_variable(group,modifier)
                updates.append(f'add_to_variable = {{ {var} = {number(value)} }}')
            if updates:
                reconcile.append(conditional(active,'\n'.join(updates)))
                group_any[group].append(block('AND',active))
            for stream in record['streams']:
                guard='has_country_flag = ISR2_core_done_'+key
                persistent=key in {'property_register','gahal_disposal','labor_indexed_savings'}
                if party and not persistent:
                    guard+='\n'+party+' = yes'
                if stream['weeks']:
                    flag='ISR2_core_stream_'+stream['variable']
                    effect+=f'\nset_country_flag = {{ flag = {flag} value = 1 days = {stream["weeks"]*7} }}'
                    guard+='\nhas_country_flag = '+flag
                total='ISR2_core_weekly_income' if stream['sign']>0 else 'ISR2_core_weekly_expense'
                reconcile.append(conditional(guard,f'add_to_variable = {{ {total} = {stream["variable"]} }}'))
            cycle=record.get('focus_cycle')
            if cycle:
                effect+=f'\nset_country_flag = {{ flag = ISR2_core_cooldown_{key} value = 1 days = {cycle["cooldown_weeks"]*7} }}'
                rearm.append(conditional(f'has_country_flag = ISR2_core_done_{key}\nNOT = {{ has_country_flag = ISR2_core_cooldown_{key} }}',
                    f'uncomplete_national_focus = {{ focus = {fid} uncomplete_children = no refund_political_power = no }}\nclr_country_flag = ISR2_core_done_{key}'))
            effect+='\nset_country_flag = ISR2_core_done_'+key+'\nISR2_core_reconcile = yes\nupdate_money_dirty_variable = yes'
            self.effects['ISR2_core_commit_'+key]=conditional('ISR2_core_can_'+key+' = yes',
                'ISR2_refresh_core_quotes = yes\n'+effect,
                conditional(f'NOT = {{ has_country_flag = ISR2_core_done_{key} }}',
                    f'uncomplete_national_focus = {{ focus = {fid} uncomplete_children = no refund_political_power = no }}'))
            self.actions[fid]['reward']='ISR2_core_commit_'+key+' = yes'
            self.actions[fid]['available']='ISR2_core_can_'+key+' = yes'
            self.actions[fid]['visible_available']='\n'.join(x for x in visible if x)
        for group,modifiers in self.group_mods.items():
            key='ISR2_programme_'+group
            self.loc[key]=self.groups[group]['label']
            self.loc[key+'_desc']=self.groups[group]['subtitle']
            gate='ISR2_is_scenario = yes'
            if self.groups[group].get('runtime_party_trigger'):
                gate+='\n'+self.groups[group]['runtime_party_trigger']+' = yes'
            icon='GFX_idea_generic_political_discourse' if self.groups[group]['kind']=='party' else 'GFX_idea_generic_economy_increase'
            self.dynamic[key]='icon = '+icon+'\n'+block('enable',gate)+'\n'+'\n'.join(
                modifier+' = ISR2_'+group+'_'+modifier for modifier in sorted(modifiers))
            presence=block('OR','\n'.join(group_any[group]))
            reconcile.append(conditional(presence,
                conditional(f'NOT = {{ has_dynamic_modifier = {{ modifier = {key} }} }}',f'add_dynamic_modifier = {{ modifier = {key} }}'),
                conditional(f'has_dynamic_modifier = {{ modifier = {key} }}',f'remove_dynamic_modifier = {{ modifier = {key} }}')))
        self.effects['ISR2_refresh_core_quotes']='\n'.join(self.quotes+self.preview_quotes)
        self.effects['ISR2_core_reconcile']='\n'.join(reconcile)
        self.effects['ISR2_core_daily']='ISR2_refresh_core_quotes = yes\n'+'\n'.join(rearm)+'\nISR2_core_reconcile = yes'
        self.effects['ISR2_core_refresh']='ISR2_refresh_core_quotes = yes\nISR2_core_reconcile = yes'
        # The four authored national starting spirits are separate from the
        # occupation profiles, which the territorial module actually controls.
        starts=[('citizen_army',{'training_time_army_factor':-.10,'personnel_cost_multiplier_modifier':.08}),
                ('histadrut',{'production_speed_industrial_complex_factor':.08,'health_cost_multiplier_modifier':-.05,'receiving_investment_cost_modifier':.08}),
                ('absorption',{'research_speed_factor':-.05,'social_cost_multiplier_modifier':.08}),
                ('import_economy',{'mdcw_cw_market_exposure':.10,'receiving_investment_cost_modifier':-.05})]
        for (suffix,mods),source in zip(starts,self.data['starting'][:4]):
            key='ISR2_start_'+suffix
            self.ideas[key]='picture = generic_economy_increase\nallowed = { always = no }\nallowed_civil_war = { always = yes }\n'+block('modifier','\n'.join(k+' = '+number(v) for k,v in mods.items()))
            self.loc[key]=source['label'];self.loc[key+'_desc']=source['description']
            self.initial.append('add_ideas = '+key)
        self.effects['ISR2_core_init']=conditional('NOT = { has_country_flag = ISR2_core_initialized }',
            '\n'.join(self.initial)+'\nset_country_flag = ISR2_core_initialized')+'\nISR2_core_daily = yes'
