# IMPERIA CW — Cold War: uae 1970 — streamline.
"""COLDWAR direct domestic settlements, replacing redundant invoice dialogues.

The immutable approved catalogue remains untouched. Values below are native MD
balance effects, not historical prices or measured institutional improvements.
"""
P = 'COLDWAR_UAE_'
REMOVED_DECISIONS = frozenset({
    'founders', 'mediate', 'delegation', 'court_settlement', 'cabinet_bargain',
    'withdrawal', 'british_amendment', 'island_offer', 'jeddah', 'gcc',
})


def _relief(node, spirit, component, value, family):
    node['spirit_changes'].append(dict(
        spirit=P+spirit, component=component, operation='reduce_penalty',
        value=value, floor=0, owner_focus=node['id'], family=family,
        evaluation='strongest_in_family_then_sum_credits_from_original_component_clamp_at_zero'))


def apply_revision(data):
    """Apply the user-authorized direct-focus revision to a mutable design copy."""
    by = {n['id'].removeprefix(P): n for n in data['nodes']}
    handover = by['petition_independence']
    handover.update(
        title='Prepare the Handover', narrative_title='Prepare the Handover',
        effect_body='',
        description="Britain has announced its withdrawal by the end of 1971. Local officials must organise records, train civil servants and prepare the departments that will assume the coast's new responsibilities. Staffing this work adds administrative expense; the trained civil service will remain after British protection ends.",
        reward_summary=['Office-sector productivity +5%; bureaucracy spending multiplier +2%.',
                        'Permanently reduce the inherited fragmented-administration bureaucracy penalty by 3 percentage points. The historical withdrawal schedule continues.'],
        ownership='Domestic preparation; earned civil-service relief survives British withdrawal. Ongoing programme contributions retain their existing status conditions.')
    handover['modifiers'].update(offices_productivity=.05, bureaucracy_cost_multiplier_modifier=.02)
    handover.pop('diplomatic_offer', None)
    handover['requirement_contracts'] = []
    _relief(handover, 'fragmented_authority', 'bureaucracy_cost_multiplier_modifier', .03, 'handover_civil_service')

    charter = by['charter']
    charter['description'] = "The rulers can ratify a provisional constitutional framework for common institutions. The settlement must define the responsibilities of the federation and the authority retained by each emirate. Its implementation will follow the division of powers agreed by the rulers."
    charter['reward_summary'].append('Ratify the founding framework; choose emirate guarantees or a stronger federal mandate through the following exclusive focuses.')
    for key, permission in [('dual_veto', 'guarantees_agreed'), ('federal_ministries', 'mandate_agreed')]:
        n = by[key]
        n['available'] = '\n'.join(line for line in n['available'].splitlines()
            if P+permission not in line)

    fund = by['development_fund']
    fund['modifiers']['bureaucracy_cost_multiplier_modifier'] = .03
    _relief(fund, 'unequal_development', 'stability_factor', .03, 'federal_development_transfers')
    fund['description'] = "The smaller emirates need roads, public services and dependable development finance. A common fund can direct projects towards settlements with the greatest needs and strengthen confidence in the union. Planning and supervising those works will require a continuing federal administration."
    fund['reward_summary'] += ['Bureaucracy spending multiplier +3%.',
                              'Reduce the inherited unequal-development stability penalty by 3 percentage points.']

    by['presidential_union']['description'] = "The rulers can delegate clearer executive responsibilities to the presidency while maintaining their constitutional role. A stronger federal executive can carry decisions into effect more consistently, although emirates accustomed to managing their own affairs will resist the concentration of authority."
    compact = by['rulers_compact']
    for key in ('rulers_compact', 'presidential_union'):
        by[key]['available'] += '\nhas_country_flag = '+P+'federation_established\nhidden_trigger = { has_country_flag = '+P+'federation_formed }'
    compact['description'] = "Renewing the federal compact requires an agreed cabinet and a workable division of responsibilities between Abu Dhabi and Dubai. A Dubai-led ministry can strengthen confidence in the federal administration while the presidency remains a separate office."
    compact['reward_summary'] += ['Settle the federal cabinet and its separate premiership.',
                                 'Reduce the inherited fragmented-administration bureaucracy penalty by 3 percentage points through the existing cabinet settlement.']
    republic = by['citizen_republic']
    republic['modifiers']['offices_productivity'] = .05
    republic['description'] = "A republican constitution can place federal authority in elected institutions. Civil guarantees and a professional administration can give the new government a dependable foundation, while the displacement of hereditary authority will unsettle established loyalties."
    republic['reward_summary'].append('Office-sector productivity +5%.')
    diplomacy = by['gulf_diplomacy']
    diplomacy['modifiers'].update(political_power_factor=.05, improve_relations_maintain_cost_factor=-.20)
    diplomacy['description'] = "Independence requires a foreign service able to represent the federation and maintain regular contact with its neighbours. Professional diplomats can sustain those relationships and coordinate external policy, while a permanent ministry adds to the administrative budget."
    diplomacy['reward_summary'] += ['Political Power Gain +5%.', 'Improve Relations maintenance cost -20%.']
    diplomacy['streamlined'] = True
    for key in ('petition_independence', 'charter', 'dual_veto', 'federal_ministries',
                'development_fund', 'presidential_union', 'rulers_compact', 'citizen_republic'):
        by[key]['streamlined'] = True

    removed = {P+'decision_'+key for key in REMOVED_DECISIONS}
    data['decisions'] = [d for d in data['decisions'] if d['id'] not in removed]
    for d in data['decisions']:
        if d['id'] in {P+'decision_reserve_withdraw', P+'decision_british_withdrawal_policy'}:
            d['pp'] = 0
    for n in data['nodes']:
        for field in ('unlocks_decisions', 'decision_unlocks'):
            if field in n:
                n[field] = [x for x in n[field] if x not in removed]
    return data


def focus_leaves(key, preview=False):
    """One-time direct state changes; numerical previews use normal node data.

    Flags are deliberately omitted from preview: Clausewitz does not provide a
    useful numeric tooltip for an internal receipt. The compiler owns wrapping
    actual calls in its existing once-only focus transaction.
    """
    if preview:
        return ''
    return {
        'charter': f'set_country_flag = {P}founders_consented',
        'dual_veto': f'set_country_flag = {P}guarantees_agreed\nclr_country_flag = {P}mandate_agreed',
        'federal_ministries': f'set_country_flag = {P}mandate_agreed\nclr_country_flag = {P}guarantees_agreed',
        'presidential_union': f'set_country_flag = {P}delegated_powers_accepted\nset_country_flag = {P}executive_delegated',
        'rulers_compact': f'{P}accept_cabinet_bargain = yes\nclr_country_flag = {P}constitutional_crisis',
    }.get(key.removeprefix(P), '')
