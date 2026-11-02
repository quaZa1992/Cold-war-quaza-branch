# IMPERIA COLD WAR — Strong doctrine trade-offs authorised on 28 October 2026.
"""Current revision over the preserved initial doctrine concept and MD content."""
from decimal import Decimal
from pathlib import Path
import re

REVISION = '20261028_strong_tradeoffs'
MARKER = '# IMPERIA COLD WAR — Strong land doctrine trade-offs.'

# Only activation penalties change. Positive rewards and milestones stay intact.
BASE_OVERRIDES = {
    'mdcw_deliberate_firepower': {'planning_speed': -0.20, 'supply_consumption_factor': 0.12},
    'mdcw_mobile_raiding_warfare': {'out_of_supply_factor': 0.15},
    'mdcw_heliborne_reaction_forces': {'army_fuel_consumption_factor': 0.15, 'L_Air_assault_Bat': {'fort': {'attack': -0.15}}},
    'mdcw_key_zone_defence': {'org_loss_when_moving': 0.15, 'supply_consumption_factor': 0.08},
    'mdcw_guided_anti_armour_integration': {'equipment_cost_multiplier_modifier': 0.08,
        'AT_company': {'soft_attack': -0.15, 'breakthrough': -0.15},
        'Mot_AT_company': {'soft_attack': -0.15, 'breakthrough': -0.15}},
    'mdcw_counterfire_coordination': {'army_intel_to_others': 10, 'supply_consumption_factor': 0.15},
}

DESCRIPTIONS = {
    'mdcw_deliberate_firepower': "Van Fleet's army in Korea in 1951 relied on registered fire and forward ammunition stocks. Deliberate infantry assaults gain fire superiority, but assembling fire plans slows preparation and increases supply demand.",
    'mdcw_mobile_raiding_warfare': 'South African mobile battle groups used rapid concentration and flanking attacks in the 1970s and 1980s. Forward loads support short advances; delayed resupply beyond this reserve brings greater supply penalties and weak fixed defence.',
    'mdcw_heliborne_reaction_forces': 'Rhodesian Fireforce from 1974 linked helicopter-borne blocking groups with reconnaissance and follow-up forces. Light assault groups need considerable fuel and fare poorly in frontal attacks on prepared fortifications.',
    'mdcw_key_zone_defence': "Austria's Raumverteidigung prepared key routes for defence. Forts and river positions support local resistance, but moving these defenders disrupts their organisation. An alternative to Territorial Defence Forces.",
    'mdcw_guided_anti_armour_integration': 'Egyptian defence in 1973 combined infantry with prepared anti-tank positions. Guided weapons improve anti-armour fire, but specialist companies need costly upkeep and sacrifice soft-target fire and offensive breakthrough.',
    'mdcw_counterfire_coordination': 'Observers and early radars supported artillery in Vietnam; more capable networks followed later. Coordinated fire improves the guns, but needs more supply and exposes information through radar and radio emissions.',
}

# File, doctrine, field: (original activation value, revised activation value).
LEGACY = {
 'common/doctrines/subdoctrines/land/land_doctrines_combat.txt': {
    'battalion_combat_teams': {'max_planning_factor': (-0.10, -0.15), 'supply_consumption_factor': (None, 0.08)},
    'decentralized_command': {'max_planning_factor': (-0.05, -0.15), 'planning_decay_rate_factor': (None, 0.20)},
 },
 'common/doctrines/subdoctrines/land/land_doctrines_supporting.txt': {
    'common_technology_army': {'army_intel_to_others': (5, 15)},
 },
 'common/doctrines/subdoctrines/land/mdcw_cold_war_free_subdoctrines.txt': {
    'mdcw_maskirovka': {'initiative_factor': (-0.05, -0.15), 'planning_speed': (None, -0.10)},
    'mdcw_cadre_reserve_system': {'army_org_factor': (-0.03, -0.10), 'experience_loss_factor': (0.05, 0.15)},
    'mdcw_radio_electronic_combat': {'equipment_cost_multiplier_modifier': (0.05, 0.08), 'army_intel_to_others': (None, 10)},
 },
}

LEGACY_TEXT = {
 'localisation/english/MD_doctrines_ncns_l_english.yml': {
    'SUBDOCTRINE_STRUCTURE_BCT_DESC': 'Self-contained battalion teams integrate manoeuvre, fire support and sustainment. Small formations react quickly, but duplicated support elements raise supply demand and leave less capacity for deep battle preparation.',
    'SUBDOCTRINE_STRUCTURE_DECENTRAL_COMMAND_DESC': 'Subordinate commanders act on assigned objectives. Local initiative improves manoeuvre, but dispersed planning limits the preparation and endurance of a single coordinated battle plan and requires longer training.',
    'SUBDOCTRINE_TECHNOLOGY_COMMON_DESC': 'Standardised equipment and communications support a broadly capable army. Common radio procedures remain recognisable to enemy intercept teams even as improved communications security reduces their exposure.',
 },
 'localisation/english/mdcw_cold_war_doctrines_l_english.yml': {
    'SUBDOCTRINE_MDCW_MASKIROVKA_DESC': 'Camouflage, dummy formations and false radio traffic conceal the real attack. Strict secrecy also delays preparation and local decisions. Better radio deception reduces these problems without removing the command burden.',
    'SUBDOCTRINE_MDCW_CADRE_RESERVE_SYSTEM_DESC': 'Cadre formations expand rapidly when reservists arrive. They offer manpower and low standing costs, but limited collective training leaves less cohesive units and greater experience loss even after refresher courses.',
    'SUBDOCTRINE_MDCW_RADIO_ELECTRONIC_COMBAT_DESC': 'Interception, direction finding and jamming disrupt enemy communications. Active emitters can also be detected and located. Signal security limits exposure, while specialist electronic equipment requires costly upkeep.',
 },
}


def merge(target, changes):
    for key, value in changes.items():
        if isinstance(value, dict):
            merge(target.setdefault(key, {}), value)
        else:
            target[key] = value


def apply_revision(items):
    for item in items:
        merge(item['effects'], BASE_OVERRIDES.get(item['id'], {}))
        if item['id'] in DESCRIPTIONS:
            item['description'] = DESCRIPTIONS[item['id']]


def block_span(source, ident):
    start = re.search(r'(?m)^' + re.escape(ident) + r'\s*=\s*\{', source)
    if not start:
        raise ValueError('Missing doctrine: ' + ident)
    token = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]')
    opening = source.index('{', start.start())
    depth = 0
    for match in token.finditer(source, opening):
        if match.group() == '{':
            depth += 1
        elif match.group() == '}':
            depth -= 1
            if depth == 0:
                return start.start(), match.end()
    raise ValueError('Unclosed doctrine: ' + ident)


def patch_legacy(source, ident, changes):
    start, end = block_span(source, ident)
    block = source[start:end]
    split = block.index('\n\trewards = {')
    prefix, tail = block[:split], block[split:]
    if '\t' + MARKER not in prefix:
        prefix = prefix.replace('\n\t# EFFECTS', '\n\t' + MARKER + '\n\t# EFFECTS', 1)
    for field, (before, after) in changes.items():
        pattern = re.compile(r'(?m)^(\t' + re.escape(field) + r'\s*=\s*)(-?\d+(?:\.\d+)?)([^\r\n]*)$')
        match = pattern.search(prefix)
        if match:
            current = Decimal(match[2])
            permitted = {Decimal(str(after))}
            if before is not None:
                permitted.add(Decimal(str(before)))
            if current not in permitted:
                raise ValueError(f'Unexpected current value for {ident}.{field}: {current}')
            prefix = prefix[:match.start(2)] + str(after) + prefix[match.end(2):]
        elif before is None:
            prefix = prefix.rstrip() + '\n\t' + MARKER + '\n\t' + field + ' = ' + str(after) + '\n'
        else:
            raise ValueError('Missing activation field: ' + ident + '.' + field)
    return source[:start] + prefix + tail + source[end:]


def legacy_outputs(root):
    output = {}
    for relative, doctrines in LEGACY.items():
        source = (root / relative).read_text(encoding='utf-8-sig')
        for ident, changes in doctrines.items():
            source = patch_legacy(source, ident, changes)
        if not source.startswith('# IMPERIA COLD WAR —'):
            source = MARKER + '\n# Native MD content retained; only the marked doctrine trade-offs are integrated.\n' + source
        output[relative] = source
    for relative, translations in LEGACY_TEXT.items():
        source = (root / relative).read_text(encoding='utf-8-sig')
        for key, text in translations.items():
            pattern = re.compile(r'(?m)^( ' + re.escape(key) + r':(?:0)? )"(?:\\.|[^"\\])*"$')
            source, count = pattern.subn(lambda match: match[1] + '"' + text + '"', source)
            if count != 1:
                raise ValueError('Expected one English description: ' + key)
        lines = source.splitlines()
        if MARKER not in lines:
            lines.insert(1, MARKER)
        output[relative] = '\n'.join(lines) + '\n'
    return output
