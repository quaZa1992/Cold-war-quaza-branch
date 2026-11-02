# IMPERIA COLD WAR — Cold War: Japan 1970 constitutional focus reward generation.
"""Write reviewable Article Nine rewards to staging; never install them."""
from pathlib import Path

root = Path(__file__).resolve().parent
stage = root / 'staging' / 'constitution'
stage.mkdir(parents=True, exist_ok=True)
from reward_revision import load_overlay

def quote(value):
    return '"' + value.replace('\\', '\\\\').replace('"', '\\"') + '"'

OVERLAY = load_overlay()
article_overrides = OVERLAY.get('article9', {})
terminal_ideas = OVERLAY['terminal_ideas']
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
for key, override in article_overrides.items():
    if key not in records:
        raise ValueError(f'Unknown Article 9 reward override: {key}')
    old_pp, old_cost, old_modifiers, old_days, old_action = records[key]
    records[key] = (override.get('pp', old_pp), override.get('treasury_cost', old_cost),
                    override.get('modifiers', old_modifiers), override.get('days', old_days), old_action)
names = {
    'debate': 'The Constitutional Debate', 'commission': 'Revision Commission',
    'coalition': 'Coalition for Revision', 'campaign': 'Constitutional Campaign',
    'party_talks': 'Inter-Party Constitutional Talks', 'public_hearings': 'Public Constitutional Hearings',
    'draft': 'The Amendment Draft', 'civilian': 'Civilian Safeguards',
    'mission': 'Defence Mission Debate', 'diet': 'The Diet Vote',
}

ideas = ['# IMPERIA COLD WAR — Cold War: Japan constitutional debate modifiers.', 'ideas = {', '\tcountry = {']
effects = ['# IMPERIA COLD WAR — Cold War: Japan constitutional focus rewards.']
loc = ['l_english:', '# IMPERIA COLD WAR — Japan constitutional reward localization.']
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

terminal_lines = ['# IMPERIA COLD WAR — Japan constitutional terminal spirits.', 'ideas = {', '\tcountry = {']
terminal_loc = ['l_english:', '# IMPERIA COLD WAR — Japan constitutional terminal spirit localization.']
for idea, record in terminal_ideas.items():
    terminal_lines += [f'\t\t{idea} = {{', '\t\t\tpicture = JAP_imperial_influence_communist',
                       '\t\t\tallowed_civil_war = { always = yes }', '\t\t\tmodifier = {']
    terminal_lines.extend(f'\t\t\t\t{key} = {value:g}' for key, value in record['modifiers'].items())
    terminal_lines += ['\t\t\t}', '\t\t}']
    terminal_loc += [f' {idea}: {quote(record["name"])}', f' {idea}_desc: {quote(record["description"])}']
terminal_lines += ['\t}', '}']
(stage / 'terminal_ideas.txt').write_text('\n'.join(terminal_lines) + '\n', encoding='utf-8')
(stage / 'terminal_localisation.yml').write_text('\n'.join(terminal_loc) + '\n', encoding='utf-8-sig')
terminal_effects = [
    '# IMPERIA COLD WAR — Japan constitutional referendum terminal effects.',
    'COLDWAR_JAP_1970_article9_abolish = {',
    '\tset_country_flag = COLDWAR_JAP_1970_article9_abolished',
    '\tremove_ideas = COLDWAR_JAP_1970_article9_self_defence',
    '\tadd_ideas = COLDWAR_JAP_1970_revised_defence_constitution',
    '\tif = { limit = { country_exists = USA } USA = { add_opinion_modifier = { target = JAP modifier = COLDWAR_JAP_1970_revision_concern } country_event = { id = coldwar_jap.2 } } }',
    '\tif = { limit = { country_exists = SOV } SOV = { add_opinion_modifier = { target = JAP modifier = COLDWAR_JAP_1970_soviet_revision_concern } country_event = { id = coldwar_jap.3 } } }',
    '}',
    'COLDWAR_JAP_1970_article9_confirm = {',
    '\tset_country_flag = COLDWAR_JAP_1970_article9_confirmed',
    '\tadd_timed_idea = { idea = COLDWAR_JAP_1970_article9_retained_mandate days = 730 }',
    '}',
]
(stage / 'terminal_effects.txt').write_text('\n'.join(terminal_effects) + '\n', encoding='utf-8')
print(f'Staged {len(records)} constitutional focus rewards and {len(terminal_ideas)} terminal spirits; no runtime files were written.')
