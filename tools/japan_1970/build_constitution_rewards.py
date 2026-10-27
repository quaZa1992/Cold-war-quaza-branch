# IMPERIA CW — Cold War: Japan 1970 constitutional focus reward generation.
"""Write reviewable Article Nine rewards to staging; never install them."""
from pathlib import Path

root = Path(__file__).resolve().parent
stage = root / 'staging' / 'constitution'
stage.mkdir(parents=True, exist_ok=True)
prefix = 'COLDWAR_JAP_1970_article9_'
records = {
    'debate': (-50, 0, {'stability_factor': -.03}, 730, 'init'),
    'commission': (-50, 0, {'bureaucracy_cost_multiplier_modifier': .02}, 730, 'support_10'),
    'coalition': (0, 2, {'political_power_factor': -.05}, 730, 'support_20'),
    'campaign': (30, 0, {'stability_factor': -.04}, 730, 'support_15'),
    'party_talks': (0, 0, {'stability_factor': .02, 'bureaucracy_cost_multiplier_modifier': .03}, 730, 'support_10'),
    'public_hearings': (0, 1, {'stability_factor': .02}, 730, 'support_10'),
    'draft': (0, 1, {'bureaucracy_cost_multiplier_modifier': .02}, 730, 'support_8'),
    'civilian': (0, 0, {'bureaucracy_cost_multiplier_modifier': .03, 'stability_factor': .02}, 730, 'support_8'),
    'mission': (0, 0, {'experience_gain_army_factor': .05, 'stability_factor': -.03}, 730, 'support_10'),
    'diet': (-75, 0, {'stability_factor': -.03}, 365, None),
    'referendum': (-75, 2, {}, None, 'referendum_open'),
    'abolish': (0, 0, {}, None, 'abolish'),
    'confirm': (0, 0, {}, None, 'confirm'),
}
names = {
    'debate': 'The Constitutional Debate', 'commission': 'Revision Commission',
    'coalition': 'Coalition for Revision', 'campaign': 'Constitutional Campaign',
    'party_talks': 'Inter-Party Constitutional Talks', 'public_hearings': 'Public Constitutional Hearings',
    'draft': 'The Amendment Draft', 'civilian': 'Civilian Safeguards',
    'mission': 'Defence Mission Debate', 'diet': 'The Diet Vote',
}

ideas = ['# IMPERIA CW — Cold War: Japan constitutional debate modifiers.', 'ideas = {', '\tcountry = {']
effects = ['# IMPERIA CW — Cold War: Japan constitutional focus rewards.']
loc = ['l_english:']
for key, (pp, cost, modifiers, days, action) in records.items():
    idea = prefix + key + '_climate'
    if modifiers:
        ideas.extend([f'\t\t{idea} = {{', '\t\t\tpicture = JAP_imperial_influence_communist',
                      '\t\t\tallowed_civil_war = { always = yes }', '\t\t\tmodifier = {'])
        ideas.extend(f'\t\t\t\t{k} = {v:g}' for k, v in modifiers.items())
        ideas.extend(['\t\t\t}', '\t\t}'])
        loc.append(f' {idea}: "{names[key]}"')
    helper = prefix + 'reward_' + key
    flag = helper + '_done'
    conditions = [f'NOT = {{ has_country_flag = {flag} }}', 'original_tag = JAP', 'IMP_is_1970_scenario = yes']
    if key in ('debate', 'commission', 'abolish', 'confirm'):
        conditions.append('has_idea = COLDWAR_JAP_1970_article9_self_defence')
    if key == 'diet':
        conditions.append('check_variable = { var = COLDWAR_JAP_1970_article9_support value = 67 compare = greater_than_or_equals }')
    if key == 'referendum':
        conditions.append('has_country_flag = COLDWAR_JAP_1970_article9_diet_approved')
    if key in ('abolish', 'confirm'):
        conditions.append('has_country_flag = COLDWAR_JAP_1970_article9_referendum_open')
    if key == 'abolish':
        conditions.append('has_stability > 0.54999')
    lines = []
    if pp:
        lines.append(f'add_political_power = {pp}')
    if cost:
        lines.extend((f'set_temp_variable = {{ treasury_change = -{cost} }}', 'modify_treasury_effect = yes'))
    if modifiers:
        lines.append(f'add_timed_idea = {{ idea = {idea} days = {days} }}')
    if action:
        lines.append(f'{prefix}{action} = yes')
    if key == 'diet':
        lines.append('set_country_flag = COLDWAR_JAP_1970_article9_diet_approved')
    if key in ('abolish', 'confirm'):
        lines.append('clr_country_flag = COLDWAR_JAP_1970_article9_referendum_open')
        lines.append('clr_country_flag = COLDWAR_JAP_1970_article9_debate_open')
    effects.extend([f'{helper} = {{', '\tif = {', f'\t\tlimit = {{ {" ".join(conditions)} }}'])
    effects.extend('\t\t' + line for line in lines)
    effects.extend([f'\t\tset_country_flag = {flag}', '\t}', '}'])
ideas.extend(['\t}', '}'])
(stage / 'ideas.txt').write_text('\n'.join(ideas) + '\n', encoding='utf-8')
(stage / 'effects.txt').write_text('\n'.join(effects) + '\n', encoding='utf-8')
(stage / 'localisation.yml').write_text('\n'.join(loc) + '\n', encoding='utf-8-sig')
print(f'Staged {len(records)} constitutional rewards; focus availability and display require integration.')
