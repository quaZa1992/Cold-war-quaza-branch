# IMPERIA CW — Cold War: Generic 1970 national focus content generator.
"""COLDWAR | design effects (design/dsl.py tuples) -> completion_reward lines in MD Russia 2000 form."""
import re
from gen_common import P, num, OUTLOOK_RANGE, OUTLOOK_LABEL, BUILD_PRICE_PER_BN

# ---------------------------------------------------------------- tooltips
# own tooltip only where MD has none (or colours it wrong); label, MD format ($RIGHT|<fmt>$)
COLDWAR_TT = {
    'mdcw_cw_ideological_defence': ('Ideological Defence', '+=%1'),
    'mdcw_cw_support_effectiveness': ('Our Public Support Campaigns Abroad', '+=%1'),
    'mdcw_cw_assistance_limit': ('Limits of Received Assistance Programmes', '+=%1'),
    'mdcw_cw_assistance_capacity': ('Assistance Capacity', '+=0'),
    'mdcw_cw_military_programme_cost': ('Cost of Our Military Programmes', '-=%1'),
    'mdcw_cw_market_exposure': ('Exposure to World Market Swings', '-=%1'),
    'imp_sanction_resistance': ('Sanction Resistance', '+=%1'),
    'imp_oil_price_resistance': ('Oil Price Resistance', '+=%1'),
    'globalism_equilibrium': ('Globalism Equilibrium', 'Y=0'),
    'internal_factions_cost_factor': ('Internal Faction Action Cost', '-=%1'),
    'party_popularity_stability_factor': ('Stability from Party Popularity', '+=%1'),
    'production_factory_efficiency_gain_factor': ('Production Efficiency Growth', '+=%1'),
    'literacy_rate_education_modifier': ('Literacy Growth from Education', '+=%1'),
    'experience_gain_army_factor': ('Army Experience Gain', '+=%1'),
    'experience_gain_air_factor': ('Air Experience Gain', '+=%1'),
    'experience_gain_navy_factor': ('Navy Experience Gain', '+=%1'),
    'command_power_gain': ('Daily Command Power Gain', '+=2'),
    'defensive_war_stability_factor': ('Stability in Defensive Wars', '+=%1'),
    'weekly_manpower': ('Weekly Manpower', '+=0'),
    # MD colours these wrong (green for a cost)
    'consumer_goods_factor': ('Consumer Goods Factories', '-=%1'),
    # MD's trees use <modifier>_tt for these, but no MD file defines them (same labels as the GDR generator)
    'army_attack_factor': ('Division Attack', '+=%1'),
    'army_org_factor': ('Division Organisation', '+=%1'),
    'democratic_drift': ('Western Drift', '+=%1'),
    'monthly_population': ('Monthly Population', '+=%1'),
    'production_factory_max_efficiency_factor': ('Maximum Production Efficiency', '+=%1'),
    'production_speed_infrastructure_factor': ('Infrastructure Construction Speed', '+=%1'),
    'research_speed_factor': ('Research Speed', '+=%1'),
}
CW_KEYS = {'mdcw_cw_ideological_defence', 'mdcw_cw_support_effectiveness', 'mdcw_cw_assistance_limit',
           'mdcw_cw_assistance_capacity', 'mdcw_cw_military_programme_cost', 'mdcw_cw_market_exposure',
           'imp_sanction_resistance', 'imp_oil_price_resistance', 'globalism_equilibrium'}
MARKET_KEYS = {'globalism_equilibrium', 'mdcw_cw_market_exposure'}

# MD building helpers -> fixed MD price (bn) read from 00_scripted_effects.txt (filled by gen_build)
BUILD_COST = {}

# design law helper -> conditions under which the MD helper pays political power instead of changing the law
LAW_GUARD = {
    'increase_military_spending': [
        'NOT = { has_idea = defence_09 }',
        'OR = {', '\thas_war = yes', '\tnationalist_fascist_are_in_power = yes', '\tsalafist_caliphate_are_in_power = yes',
        '\tNOT = {', '\t\thas_idea = defence_05', '\t\thas_idea = defence_06', '\t\thas_idea = defence_07',
        '\t\thas_idea = defence_08', '\t}', '}'],
    'decrease_military_spending': ['NOT = {', '\thas_idea = defence_00', '\thas_idea = defence_01', '}'],
    'increase_policing_budget': ['NOT = { has_idea = police_05 }'],
    'decrease_policing_budget': ['NOT = { has_idea = police_01 }'],
    'increase_social_spending': ['OR = {'] + [f'\thas_idea = social_0{i}' for i in range(1, 6)] + ['}'],
    'decrease_social_spending': ['OR = {'] + [f'\thas_idea = social_0{i}' for i in range(2, 7)] + ['}'],
    'increase_healthcare_budget': ['OR = {'] + [f'\thas_idea = health_0{i}' for i in range(1, 6)] + ['}'],
    'decrease_healthcare_budget': ['OR = {'] + [f'\thas_idea = health_0{i}' for i in range(2, 7)] + ['}'],
    'increase_education_budget': ['OR = {'] + [f'\thas_idea = edu_0{i}' for i in range(1, 5)] + ['}'],
    'decrease_education_budget': ['OR = {'] + [f'\thas_idea = edu_0{i}' for i in range(2, 6)] + ['}'],
    'increase_centralization': None,     # no political power fallback in MD
    'decrease_centralization': None,
    'increase_exports': ['NOT = { has_idea = globalized_trade_economy }'],
    'decrease_exports': ['NOT = { has_idea = md_closed_economy }'],
}
# increase_migration_law pays PP only in its final else (closed_borders or no migration law at all)
LAW_GUARD['increase_migration_law'] = ['OR = {', '\thas_idea = open_borders', '\thas_idea = slightly_regulated_immigration',
                                       '\thas_idea = regulated_immigration', '\thas_idea = heavily_regulated_immigration', '}']
LAW_GUARD['decrease_migration_law'] = ['OR = {', '\thas_idea = slightly_regulated_immigration', '\thas_idea = regulated_immigration',
                                       '\thas_idea = heavily_regulated_immigration', '\thas_idea = closed_borders', '}']


class Ctx:
    """per-run registries"""
    def __init__(self, md_tt_keys, party_meta, trunk_t2):
        self.md_tt = md_tt_keys          # MD <modifier>_tt keys that exist
        self.meta = party_meta           # party key -> META dict (idx, trigger, party)
        self.trunk_t2 = trunk_t2         # outlook -> id of T2
        self.coldwar_tt = {}             # key -> (label, fmt) used
        self.loc = {}                    # extra loc keys -> text
        self.ideas = {}                  # idea id -> dict
        self.md_ideas_used = {}          # MD idea -> [focus ids]
        self.notes_dropped = []          # design notes without game code
        self.idea_owner = {}

    def tt(self, key):
        if key in COLDWAR_TT:
            self.coldwar_tt[key] = COLDWAR_TT[key]
            return f'COLDWAR_{key}_tt'
        t = f'{key}_tt'
        if t in self.md_tt:
            return t
        raise KeyError(f'no tooltip for modifier {key} (add it to COLDWAR_TT)')


def pct_text(v):
    return f'{abs(v) * 100:g}%'


def outlook_tt(ctx, o, v):
    sign = 'p' if v > 0 else 'm'
    key = f'{P}outlook_{o}_{sign}{int(round(abs(v) * 100))}_tt'
    lab = OUTLOOK_LABEL[o]
    ctx.loc.setdefault(key, f'§Y{lab}§! outlook: the governing party (or, if it belongs to another outlook, the most popular '
                            f'{lab} party) {"§Ggains" if v > 0 else "§Rloses"} {int(round(abs(v) * 100))}%§! popularity.')
    return key


def tension_tt(ctx, v):
    key = f'{P}tension_{"p" if v > 0 else "m"}{abs(v)}_tt'
    ctx.loc.setdefault(key, f'Cold War Tension: {"§R+" if v > 0 else "§G-"}{abs(v)}§!')
    return key


def compile_focus(ctx, node, programme, var_prefix):
    """node: design node; programme: dynamic modifier name of the party (None for trunk foci).
    Returns list of lines (relative indentation with \\t) for completion_reward (without the log line)."""
    fx = node['fx']
    fid = P + node['id']
    party = node['party']
    out = []
    groups = {k: [] for k in ('pol', 'prog', 'idea', 'party', 'law', 'build', 'money', 'tech', 'xp', 'fac', 'misc')}
    cw = False
    cw_prog = False
    market = False

    # ---- one-off politics
    for e in fx:
        t = e[0]
        if t == 'pp':
            groups['pol'].append(f'add_political_power = {e[1]}')
        elif t == 'stab':
            groups['pol'].append(f'add_stability = {num(e[1])}')
        elif t == 'ws':
            groups['pol'].append(f'add_war_support = {num(e[1])}')

    # ---- programme (party dynamic modifier)
    prog = [e for e in fx if e[0] == 'prog']
    if prog:
        if not programme:
            raise ValueError(f'{fid}: programme line outside a party tree')
        if node['slot'] == 'E':
            groups['prog'].append(f'custom_effect_tooltip = {{ localization_key = adds_dynamic_modifier_tt MODIFIER = {programme} }}')
        else:
            groups['prog'].append(f'custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {programme} }}')
        for e in prog:
            groups['prog'].append(f'add_to_variable = {{ {var_prefix}{e[1]} = {num(e[2])} tooltip = {ctx.tt(e[1])} }}')
            if e[1] in CW_KEYS:
                cw = True
                cw_prog = True       # a dynamic modifier variable changed: refresh before the Cold War recalculation
            if e[1] in MARKET_KEYS:
                market = True
        if node['slot'] == 'E':
            groups['prog'].append(f'add_dynamic_modifier = {{ modifier = {programme} }}')
    elif node['slot'] == 'E' and programme:
        raise ValueError(f'{fid}: party entry without programme lines')

    # ---- national spirits
    for e in fx:
        t = e[0]
        if t in ('idea', 'timed'):
            iid = P + e[1]
            mods = e[2] if t == 'idea' else e[3]
            name = e[3] if t == 'idea' else e[4]
            bound = e[4] if t == 'idea' else False
            if iid in ctx.ideas:
                raise ValueError(f'idea {iid} defined twice')
            ctx.ideas[iid] = dict(id=iid, mods=mods, name=name, bound=bound, party=party, focus=fid,
                                  days=(e[2] if t == 'timed' else None))
            if any(k in CW_KEYS for k in mods):
                cw = True
            if any(k in MARKET_KEYS for k in mods):
                market = True
            if t == 'idea':
                groups['idea'].append(f'add_ideas = {iid}')
                if bound:
                    key = f'{P}{party}_bound_idea_tt'
                    ctx.loc.setdefault(key, f'This national spirit is removed when the §Y{ctx.meta[party]["party"]}§! party loses power.')
                    groups['idea'].append(f'custom_effect_tooltip = {key}')
            else:
                groups['idea'].append(f'add_timed_idea = {{ idea = {iid} days = {e[2]} }}')
        elif t == 'mdidea':
            ctx.md_ideas_used.setdefault(e[1], []).append(fid)
            groups['idea'].append(('MDIDEA', e[1]))
        elif t == 'mdtimed':
            ctx.md_ideas_used.setdefault(e[1], []).append(fid)
            groups['idea'].append(('MDTIMED', e[1], e[2]))

    # ---- party popularity and outlooks
    for e in fx:
        t = e[0]
        if t == 'pop':
            m = ctx.meta[party]
            groups['party'] += [f'set_temp_variable = {{ party_index = {m["idx"]} }}',
                                f'set_temp_variable = {{ party_popularity_increase = {num(e[1])} }}',
                                f'set_temp_variable = {{ temp_outlook_increase = {num(e[1])} }}',
                                'change_relative_party_popularity = yes']
        elif t == 'outlook':
            o, v = e[1], e[2]
            lo, hi = OUTLOOK_RANGE[o]
            groups['party'] += [f'custom_effect_tooltip = {outlook_tt(ctx, o, v)}', 'hidden_effect = {',
                                f'\tset_temp_variable = {{ {P}outlook_start = {lo} }}',
                                f'\tset_temp_variable = {{ {P}outlook_end = {hi} }}',
                                f'\tset_temp_variable = {{ {P}outlook_change = {num(v)} }}',
                                f'\t{P}change_outlook_popularity = yes', '}']

    # ---- laws
    for e in fx:
        if e[0] == 'law':
            g = LAW_GUARD[e[1]]
            if g is None:
                groups['law'].append(f'{e[1]} = yes')
            else:
                groups['law'] += ['if = {', '\tlimit = {'] + ['\t\t' + l for l in g] + ['\t}', f'\t{e[1]} = yes', '}']

    # ---- buildings (paid as a share of GDP instead of MD's fixed price) and money: one treasury line per focus
    builds = [e[1] for e in fx if e[0] == 'build']
    treasury = sum(e[1] for e in fx if e[0] == 'money')
    if 'two_office_construction' in builds:
        from gen_quality import OFFICE_PROJECTS, prefix
        expected_share, _ = OFFICE_PROJECTS[fid]
        actual_share = round(BUILD_COST['two_office_construction'] * BUILD_PRICE_PER_BN - treasury, 3)
        assert actual_share == expected_share, (fid, actual_share, expected_share)
        groups['build'].append(f'{prefix(fid)}_open = yes')
        builds = [helper for helper in builds if helper != 'two_office_construction']
        treasury = 0
        office_project = True
    else:
        office_project = False
    if builds:
        groups['build'].append('set_temp_variable = { skip_payment = 1 }')
        for h in builds:
            groups['build'].append(f'{h} = yes')
            treasury -= BUILD_COST[h] * BUILD_PRICE_PER_BN
        groups['build'].append('set_temp_variable = { skip_payment = 0 }')
    if builds or (not office_project and any(e[0] == 'money' for e in fx)):
        treasury = round(treasury, 3)
        if treasury != 0:
            groups['money'] += [f'set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = {num(treasury)} }} }}',
                                'modify_treasury_effect = yes']
    for e in fx:
        if e[0] == 'debt':
            groups['money'] += [f'set_temp_variable = {{ debt_change = {{ value = gdp_total multiply = {num(e[1])} }} }}',
                                'modify_debt_effect = yes']

    # ---- research
    n_tech = sum(1 for e in fx if e[0] == 'tech')
    k = 0
    for e in fx:
        if e[0] == 'tech':
            k += 1
            groups['tech'] += ['add_tech_bonus = {', f'\tname = {fid}', f'\tbonus = {num(e[2])}', f'\tuses = {e[3]}'] + \
                              [f'\tcategory = {c}' for c in e[1]] + ['}']

    # ---- experience
    for e in fx:
        if e[0] == 'xp':
            groups['xp'].append(f'{e[1]}_experience = {e[2]}')

    # ---- internal factions (same value -> one temp variable, MD style)
    facs = [e for e in fx if e[0] == 'fac']
    last = None
    for e in facs:
        if e[1] == 'all':
            groups['fac'] += [f'set_temp_variable = {{ temp_all_opinion = {e[2]} }}', 'change_all_internal_faction_opinion = yes']
            last = None
            continue
        groups['fac'].append(f'set_temp_variable = {{ temp_opinion = {e[2]} }}')
        groups['fac'].append(f'change_{e[1]}_opinion = yes')

    # ---- misc
    for e in fx:
        t = e[0]
        if t == 'corruption':
            if e[1] > 0:
                groups['misc'].append('increase_corruption = yes')      # MD: no fallback at level 10
            else:
                groups['misc'] += ['if = {', '\tlimit = { NOT = { has_idea = corruption_level_01 } }', '\tdecrease_corruption = yes', '}']
            if abs(e[1]) != 1:
                raise ValueError(f'{fid}: corruption steps other than 1')
        elif t == 'corruption_chance':
            groups['misc'] += [f'custom_effect_tooltip = {P}corruption_chance_tt', 'hidden_effect = {',
                               '\trandom = { chance = 50 increase_corruption = yes }', '}']
            ctx.loc.setdefault(f'{P}corruption_chance_tt', 'There is a §R50%§! chance that §Rcorruption increases§! by one level.')
        elif t == 'growth':
            if e[1] != 1:
                raise ValueError(f'{fid}: growth other than one step')
            groups['misc'] += ['if = {', '\tlimit = { NOT = { has_idea = economic_boom } }', '\tincrease_economic_growth = yes', '}']
        elif t == 'literacy':
            groups['misc'] += ['if = {', '\tlimit = { has_variable = literacy_rate }', f'\tset_temp_variable = {{ LR_change = {num(e[1])} }}',
                               '\tupdate_literacy_rate = yes', '}']
        elif t == 'tension':
            v = int(e[1])
            groups['misc'] += [f'custom_effect_tooltip = {tension_tt(ctx, v)}', 'hidden_effect = {',
                               '\tif = {', '\t\tlimit = { has_variable = global.mdcw_cw_tension }',
                               f'\t\tset_temp_variable = {{ mdcw_cw_tension_delta = {v} }}', '\t\tmdcw_cw_add_tension = yes', '\t}', '}']
        elif t == 'flag':
            key = f'{P}{e[1][len(P):] if e[1].startswith(P) else e[1]}_tt'
            ctx.loc.setdefault(key, e[2] + '.')
            groups['misc'] += [f'custom_effect_tooltip = {key}', f'set_country_flag = {e[1]}']
        elif t == 'note':
            if node['role'] == 'government' and '+50 political power' in e[1]:
                t2 = ctx.trunk_t2[node['o']]
                groups['pol'] += ['if = {', f'\tlimit = {{ has_completed_focus = {P}{t2} }}', '\tadd_political_power = 50', '}']
            else:
                ctx.notes_dropped.append((fid, e[1]))

    # ---- assemble in MD order, newline between tooltip groups
    order = ['pol', 'prog', 'idea', 'party', 'law', 'build', 'money', 'tech', 'xp', 'fac', 'misc']
    chunks = [(g, groups[g]) for g in order if groups[g]]
    for i, (g, lines) in enumerate(chunks):
        out += lines
        if g == 'prog' and i < len(chunks) - 1:
            out.append('newline = yes')
    if cw:
        inner = ['\tif = {', '\t\tlimit = { has_country_flag = mdcw_cw_initialized }']
        if cw_prog:
            inner.append('\t\tforce_update_dynamic_modifier = yes')      # allowed deviation: only right before the recalculation
        inner.append('\t\tmdcw_cw_recalculate_country = yes')
        if market:
            inner.append('\t\tmdcw_cw_update_world_market = yes')
        out += ['hidden_effect = {'] + inner + ['\t}', '}']
    return out


def resolve_md_ideas(lines, guarded):
    """MD ideas: guard with NOT has_idea where another branch of the tree can give the same idea"""
    res = []
    for l in lines:
        if isinstance(l, tuple):
            if l[0] == 'MDIDEA':
                if l[1] in guarded:
                    res += ['if = {', f'\tlimit = {{ NOT = {{ has_idea = {l[1]} }} }}', f'\tadd_ideas = {l[1]}', '}']
                else:
                    res.append(f'add_ideas = {l[1]}')
            else:
                if l[1] in guarded:
                    res += ['if = {', f'\tlimit = {{ NOT = {{ has_idea = {l[1]} }} }}', f'\tadd_timed_idea = {{ idea = {l[1]} days = {l[2]} }}', '}']
                else:
                    res.append(f'add_timed_idea = {{ idea = {l[1]} days = {l[2]} }}')
        else:
            res.append(l)
    return res
