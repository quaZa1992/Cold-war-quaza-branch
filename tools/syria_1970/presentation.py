# IMPERIA CW — Cold War: Syria 1970 content imported from quaZa.
"""Player-facing eligibility for Syrian programmes; execution retains raw gates."""
import re

FLAG_TEXT = {
    'dual_command_resolved': 'The party and officer corps have accepted a command settlement.',
    'corrective_transition': 'The Corrective Movement has secured a negotiated transfer of authority.',
    'succession_crisis_resolved': 'The presidential succession crisis has been settled.',
    'enterprise_audits_completed': 'Three public-enterprise contracts have been audited.',
    'irrigation_trials_completed': 'Three funded irrigation and drainage trials have been completed.',
    'reservoir_resettlement_completed': 'Reservoir communities have received the agreed resettlement support.',
    'citizenship_review_completed': 'Citizenship appeals have been reviewed and their decisions implemented.',
    'political_bureau_formed': 'The Communist Political Bureau has been organized.',
    'faisal_faction_formed': "Yusuf Faisal's Communist faction has been organized.",
    'saadeddin_leadership_established': "Adnan Saadeddin's leadership organization has been established.",
    'safwan_leadership_established': "Safwan al-Qudsi's leadership organization has been established.",
    'limited_war_route': 'The government has chosen preparations for a limited Golan campaign.',
    'operations_funded': 'The Golan operations budget has been funded and remains valid.',
    'campaign_review_completed': 'The cabinet has completed its review of the campaign.',
    'darwish_coalition_active': 'Abd al-Hamid Darwish participates in the current representation agreement.',
    'badr_coalition_active': 'Salah Badr al-Din participates in the current representation agreement.',
}


def availability(node, group, loc):
    source = node['available']
    technical = 'original_tag = SYR IMP_is_1970_scenario = yes'
    parts = ['hidden_trigger = { '+technical+' }']
    gate = re.sub(r'IMP_is_1970_scenario\s*=\s*yes', '', group['gate']).strip()
    if gate and gate in source:
        key = 'COLDWAR_SYR_eligibility_'+group['id']
        name = group['label'].split(' — ')[0]
        if group['id'] in ('opening', 'baath'):
            text = "The Arab Socialist Ba'ath Party leads the government."
        elif group['id'] == 'parliament':
            text = 'Constitutional conservatives, civic liberals or independent socialists lead the government.'
        elif group['id'] == 'limited_war':
            text = FLAG_TEXT['limited_war_route']
        elif group['kind'] == 'leader':
            text = name+' directs the governing programme.'
        elif group['kind'] == 'coalition':
            text = name+' participates in an accepted cabinet representation agreement.'
        elif group.get('slot') is not None:
            text = '§Y$COLDWAR_SYR_party_'+str(group['slot'])+'$§! leads the government.'
        else:
            text = name+' leads the government.'
        loc(key, text)
        parts.append('custom_trigger_tooltip = { tooltip = '+key+' '+gate+' }')
        source = source.replace(gate, '', 1)
    source = re.sub(r'IMP_is_1970_scenario\s*=\s*yes', '', source)

    def flag(match):
        ident = match[1]
        short = ident.removeprefix('COLDWAR_SYR_')
        key = ident+'_eligibility_tt'
        assert short in FLAG_TEXT, ('Missing player-facing condition', ident, node['id'])
        loc(key, FLAG_TEXT[short])
        return 'custom_trigger_tooltip = { tooltip = '+key+' has_country_flag = '+ident+' }'

    source = re.sub(r'has_country_flag\s*=\s*(COLDWAR_SYR_\w+)', flag, source)
    assert not re.search(r'check_variable\s*=\s*\{\s*treasury\b', source), node['id']
    parts.append(source.strip())
    return '\n'.join(part for part in parts if part)
