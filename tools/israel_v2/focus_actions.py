# IMPERIA COLD WAR — Israel policy execution through national focuses only.
"""Review data only. Replace every decision menu with concrete focus actions.

The native uncomplete_national_focus effect exists in current MD. Any proposed
renewable action still needs its receipt, expiry and cooldown implementation.
Never reset children or one-time asset receipts when reopening an action.
"""
from copy import deepcopy


def convert(api):
    nodes, groups = api['NODES'], api['GROUPS']
    f, E, asset, paid, cash, debt, research, budget, exclusive = (
        api[k] for k in ('f', 'E', 'asset', 'paid', 'cash', 'debt', 'research', 'budget', 'exclusive'))
    by = {n['id']: n for n in nodes}
    originals = {n['id']: [e['value'] for e in n['effects'] if e['label'] == 'Unlocks Decision']
                 for n in nodes if any(e['label'] == 'Unlocks Decision' for e in n['effects'])}
    for n in nodes:
        n['effects'] = [e for e in n['effects'] if e['label'] != 'Unlocks Decision']
        n['action_origin'] = 'national_focus'

    def heading(rows, title):
        return [dict(e, heading=title) for e in rows]

    def patch(key, **fields):
        n = by['ISR2_' + key]
        n.update(fields)
        return n

    def add(g, key, label, x, y, description, **kwargs):
        f(g, key, label, x, y, description, **kwargs)
        n = nodes[-1]
        n['action_origin'] = 'national_focus'
        by[n['id']] = n
        return n

    def renew(n, weeks, limit=None):
        n['focus_cycle'] = dict(cooldown_weeks=weeks, lifetime_limit=limit,
            provider='uncomplete_national_focus', uncomplete_children=False,
            refund_political_power=False, new_term_costs=True)
        n['mechanics'].append(
            'A new term is chosen by completing this national focus again after its stated term/cooldown. '
            'Only this action is reopened, without refund or child reset. Each term pays its full costs; '
            'persistent asset, debt and programme receipts are never cleared.')

    # Fully specified programmes are enacted directly, with no second click.
    patch('cabinet_ledger', label='Publish the Coalition Budget')
    patch('civil_charter', label='Enact the Civil Registration Statute')
    patch('municipal_tenders', mechanics=[
        'Completion funds one eligible domestic municipal grant with its slot and infrastructure. '
        'The state is the eligible owned and controlled Israeli core with the lowest infrastructure, '
        'breaking ties by state ID. No target menu or occupied-territory core is assumed.'])
    patch('absorption_appeal', mechanics=[
        'Completion establishes the restricted 4%-GDP civilian appropriation. Later housing and training '
        'focus transactions draw it down against actual costs, never beyond the remaining balance. '
        'No unrestricted military cash and no separate spending menu.'])
    for key in ['credit_guarantees', 'workshop_guarantees']:
        n = by['ISR2_' + key]
        n['mechanics'] = [
            'Completion directly starts the listed 52-week funded guarantee programme. '
            'Its full weekly provision and benefit expire together. No individual guarantee menu.']
        renew(n, 52)
    add('capital', 'development_repayment', 'Retire a Development Bond Instalment', 0, 5,
        'Use available treasury funds to retire part of the outstanding development debt. '
        'The reduction is a real payment, rather than a free improvement in the debt calendar.',
        pre=['refinancing'], effects=[cash(-2), debt(-2)], icon='generic_banking_legislation',
        requirements=['Outstanding eligible development debt is at least 2% of quoted annual GDP.'],
        programme='One paid debt instalment', mechanics=[
            'Pays and retires the same quoted principal. Only actual eligible MD debt may be retired. '
            'A bilateral lender receives any payment on its own claim; no duplicate anonymous repayment.'])
    renew(nodes[-1], 26)
    n = by['ISR2_hearing_towns']
    n['effects'].append(E('Industry Repair Speed', '+15% for 52 weeks', 'gain',
                          native_key='industry_repair_factor', amount=.15, scope=52))
    n['programme'] = 'Funded neighbourhood repairs: 52 weeks'
    n['description'] = ('Give the neighbourhood committees a paid repair programme and a public hearing. '
                        'Maintenance teams address the homes and services behind the complaints, while '
                        'the treasury carries the stated appropriation.')
    patch('ambiguity', label='Fund Strategic Research under Ambiguity',
          effects=by['ISR2_ambiguity']['effects'] + [research('Nuclear Weapons')],
          description='Keep strategic research funded without a public declaration of possession. '
          'Laboratories and intelligence protection have a continuing bill; scientific work alone '
          'does not supply uranium, a delivery system or a finished weapon.')

    # Reserve actions themselves occupy focus cards, including early release.
    patch('reserve_register', mechanics=[
        'Exercise and emergency mobilisation are separate national focuses with their complete costs. '
        'Neither is activated automatically by the register.'])
    exercise = add('reserves', 'reserve_exercise', 'Order a Limited Reserve Exercise', -2, 6,
        'Call a limited group of reservists for practical training. Their workshops must manage '
        'a temporary loss of output while the army gains experience.',
        pre=['reserve_register'], cost=.2, effects=[E('Army Experience', '+20', 'gain'),
        E('Civilian Industry Productivity', '-5% for 35 days', 'cost')],
        icon='generic_army_drills', days=7, programme='Limited exercise: 35 days',
        requirements=['No national reserve call-up is active.'], mechanics=[
            'The bounded reserve calendar shortens this exercise to 28 days, without increasing its rewards. '
            'An emergency call-up replaces the exercise penalty, never stacks it.'])
    # Reuse already registered art rather than add an unverified sprite.
    exercise['icon'] = by['ISR2_after_action']['icon']
    renew(exercise, 26)
    callup = add('reserves', 'reserve_callup', 'Issue the National Reserve Call-Up', 2, 6,
        'Mobilise the reserve formations during an actual security emergency. The order improves '
        'military readiness and removes the same people from their civilian workplaces.',
        pre=['reserve_register'], effects=[E('Mobilization Speed', '+25% for at most 70 days', 'gain'),
        E('Division Organisation', '+8% for at most 70 days', 'gain'),
        E('Civilian Industry Productivity', '-12% for at most 70 days', 'cost'),
        E('Office Productivity', '-8% for at most 70 days', 'cost'), budget('Reserve Call-Up Expense', -.04, 10)],
        icon='menorah', days=7, programme='National reserve call-up: at most 70 days',
        requirements=['Israel is at war or has an actual RP-authorised security emergency.'],
        mechanics=['No workforce-size penalty. The bounded calendar replaces the civilian penalty with -8%. '
                   'Release removes readiness, output penalties and weekly expense together. '
                   'The term ends automatically after 70 days or when the security emergency ends.'])
    callup['icon'] = by['ISR2_ready_depots']['icon']
    renew(callup, 10)
    release = add('reserves', 'reserve_release', 'Release the Emergency Reservists', 2, 7,
        'Return the emergency formations to civilian life before the full call-up term runs out. '
        'Factories recover their people while the army gives up its temporary readiness advantage.',
        pre=['reserve_callup'], effects=[E('Removes National Spirit', 'National Reserve Call-Up', 'neutral'),
        E('Mobilization Speed', '-25%', 'cost'), E('Division Organisation', '-8%', 'cost'),
        E('Civilian Industry Productivity', '+12% or +8% with the bounded calendar', 'gain'),
        E('Office Productivity', '+8%', 'gain'), budget('Reserve Call-Up Expense Removed', .04)],
        requirements=['A national reserve call-up is active.'], icon='menorah', days=7,
        programme='Early end of the current call-up')
    release['icon'] = by['ISR2_home_front']['icon']
    renew(release, 10)

    # Direct factory tenders and genuine public-asset sales.
    for key, state, title, x in [('sapir_book', 'Haifa', 'Sapir\'s Haifa Development Tender', 3),
                                  ('sapir_negev', 'Negev', 'Sapir\'s Negev Development Tender', 5)]:
        fields = dict(label=title, effects=paid(.75) + [
            E('Accepted Private Project Capital', '+0.75% of annual GDP', 'neutral')] + asset(state, 'Civilian Factory'),
            requirements=['Alignment is in Power.', 'The project has actual accepted private capital of 0.75% of annual GDP.',
                          'Israel owns and controls ' + state + '.'],
            mechanics=['Completion executes one 1.5%-GDP factory tender: public and actual private halves '
                       'are each 0.75%. No private deposit means no construction or charge. '
                       'The two named focuses are the two distinct original tenders.'],
            programme='One-time paid development tender')
        if key == 'sapir_book':
            patch(key, **fields)
        else:
            n = deepcopy(by['ISR2_sapir_book'])
            n.update(fields, id='ISR2_' + key, xy=[12, 19], pre=[['ISR2_sapir_book']])
            nodes.append(n); by[n['id']] = n
    n = by['ISR2_property_register']
    n.update(label='Auction a Public Commercial Enterprise', effects=paid(.3) + [cash(3),
        budget('Public Enterprise Dividends Lost', -.01)], programme='One completed sale; dividend loss persists',
        mechanics=['The focus itself conducts the first sale. The named commercial asset is sold once. '
                   'Government changes never restore the dividend or the asset receipt.'])
    for key in ['wage_bonds', 'cash_wages']:
        renew(by['ISR2_' + key], 53)
    patch('histadrut_balance', mechanics=[
        'Expired wage settlements can be chosen again through their own wage-bond or cash national focus. '
        'Both competing cards reopen together after the term, with full new costs and no child reset. '
        'This institutional focus never replays any productive asset.'])

    # Separate appropriation alternatives, rather than a concealed policy menu.
    n = by['ISR2_national_bargain']
    n.update(label='Match the Civilian Housing Appropriation', effects=paid(.5) + [
        E('Accepted Private Matched Investment', '+0.5% of annual GDP', 'neutral'),
        E('Civilian Housing and Training Appropriation', '+1% of annual GDP', 'gain')],
        requirements=n['requirements'] + ['Actual matched private investment of 0.5% of annual GDP.'],
        programme='Matched civilian appropriation for two projects',
        mechanics=['Completing this focus directly funds the civilian envelope. Two later housing/training '
                   'focus transactions can each draw 0.5% GDP from it. The public 0.5% and actual private '
                   '0.5% are paid once; no more than 1% total is reimbursed.'])
    alternate = deepcopy(n)
    alternate.update(id='ISR2_gahal_settlement_match', label='Match the Settlement Appropriation',
        xy=[26, 19], description='Reserve the same limited public and private contribution for controlled '
        'territorial development instead of domestic housing. The appropriation reduces later project '
        'payments while every site retains its own security and administrative bill.',
        effects=paid(.5) + [E('Accepted Private Matched Investment', '+0.5% of annual GDP', 'neutral'),
        E('Controlled Settlement Development Appropriation', '+1% of annual GDP', 'gain')],
        programme='Matched settlement appropriation for two projects',
        mechanics=['The two later controlled-development focus transactions can each draw at most '
                   '0.5% GDP from the real 1%-GDP envelope. No host consent or core. '
                   'Insurance contributions and matching appropriations never reimburse the same expense twice.'])
    nodes.append(alternate); by[alternate['id']] = alternate
    exclusive('national_bargain', 'gahal_settlement_match')
    for key in ['gahal_investors', 'gahal_settler_entitlement']:
        if 'ISR2_' + key in by:
            n = by['ISR2_' + key]
            n['pre'] = [[p for p in row] + (['ISR2_gahal_settlement_match'] if 'ISR2_national_bargain' in row else []) for row in n['pre']]

    land = by['ISR2_mafdal_survey']
    land.update(label='Finance a Cooperative in the Negev', description=
        'Direct the land appropriation to a cooperative in the Israeli core economy. '
        'The ministry pays for a working agricultural district instead of adding another occupied site.',
        effects=paid(1) + asset('Negev', 'Agricultural District'),
        requirements=['Mafdal is in Power.', 'Israel owns and controls the Negev.'],
        programme='One-time domestic land appropriation', mechanics=[
            'This national focus directly executes the domestic option. The two territorial options '
            'are separate mutually exclusive focus cards.'])
    for key, state, x in [('mafdal_land_westbank', 'West Bank', 4), ('mafdal_land_gaza', 'Gaza', 6)]:
        n = add('mafdal', key, 'Finance a Cooperative in ' + ('the ' if state == 'West Bank' else '') + state, x, 2,
            'Put the religious-Zionist land appropriation into a controlled territorial cooperative. '
            'The agricultural district produces income while its protection and Palestinian institutional '
            'consequences remain a funded public commitment.', pre=['mizrahi_coops'], cost=1,
            effects=asset(state, 'Agricultural District') + [
                E(state + ': Local Garrison Requirement', '+5%', 'cost'),
                budget('Cooperative Security Expense', -.005)] + heading([
                E('Office Productivity', '-4% at a new pressure tier', 'cost'),
                E('Bureaucracy Cost', '+4% at a new pressure tier', 'cost'),
                E('Stability', '-2% at a new pressure tier', 'cost')], 'Palestine: Affected Core'),
            requirements=['Israel controls ' + state + '.', 'The area has room in the common settlement-tier cap.'],
            icon='jewish_sites_isr', sources=['mafdal_history', 'occupation'],
            programme='Paid site: assets and obligations follow actual control', mechanics=[
                'Executes one additional farm and its slot, without a host veto or territorial transfer. '
                'Counts as one common controlled settlement tier, with Palestinian pressure capped at '
                'two tiers per area. Existing tier attribution prevents duplicate pressure. '
                'The focus grants no infrastructure or fort, so it does not also charge the full Nahal site price.'])
        n['effect_owner'] = 'controlled_site'
        n['settlement_area'] = state
    exclusive('mafdal_survey', 'mafdal_land_westbank', 'mafdal_land_gaza')
    n = by['ISR2_service_bargain']
    n['pre'] = [[p for p in row] + (['ISR2_mafdal_land_westbank', 'ISR2_mafdal_land_gaza'] if 'ISR2_mafdal_survey' in row else []) for row in n['pre']]

    # Each actual region is a focus choice. No regional selector is hidden later.
    patch('occupation_accounts', label='Account for the Military Administration',
        effects=paid(.25) + [E('Controlled Non-Core Territory: Compliance Gain', '+5%', 'gain')],
        programme='Professional military administration',
        description='Audit the four territorial administrations and give their civilian liaison '
        'offices a common standard. Better records ease administration without removing the '
        'resistance, supply or personnel costs already present at the start.')
    controlled_template = deepcopy(by['ISR2_controlled_sites'])
    foreign_template = deepcopy(by['ISR2_foreign_footholds'])
    controlled_ids = [('controlled_sites', 'West Bank', -5), ('gaza_projects', 'Gaza', -2),
                      ('sinai_projects', 'Sinai', 1), ('golan_projects', 'Golan', 4)]
    foreign_ids = [('foreign_footholds', 'West Bank', -5), ('gaza_foothold', 'Gaza', -2),
                   ('sinai_foothold', 'Sinai', 1), ('golan_foothold', 'Golan', 4)]
    for key, state, x in controlled_ids:
        n = by.get('ISR2_' + key)
        if n is None:
            n = deepcopy(controlled_template); n['id'] = 'ISR2_' + key
            nodes.append(n); by[n['id']] = n
        n.update(label='Fund a ' + state + ' Settlement Site', xy=[49+x, 10],
            pre=[['ISR2_occupation_accounts']], requirements=['Israel controls ' + state + '.',
                'The area has fewer than three paid controlled settlement tiers.',
                'An eligible state and province have native building capacity.',
                'No freeze on new settlement projects is active.'],
            effects=heading(paid(1.5) + [E('Police Cost', '+3%', 'cost'),
                E('Personnel Cost', '+2%', 'cost')], 'Israel') + heading(
                asset(state, 'Agricultural District') + asset(state, 'Infrastructure') + asset(state, 'Land Fort') +
                [E('Local Garrison Requirement', '+10%', 'cost')], state),
            programme='Paid site: assets and obligations follow actual control',
            mechanics=['Completion directly buys one paid development tier in ' + state + '. '
                'The three assets receive their three state shared slots first. Actual ownership, '
                'control and province capacity are separate guards. At most three common tiers per area. '
                'Any funded foreign foothold in this area is closed before activating controlled benefits. '
                'Existing buildings, first-purchase receipts and pressure attribution are never replayed.'],
            effect_owner='controlled_site', settlement_area=state, settlement_action='controlled_development')
        if state in ['West Bank', 'Gaza']:
            n['effects'] += heading([E('Office Productivity', '-4% at a new pressure tier', 'cost'),
                E('Bureaucracy Cost', '+4% at a new pressure tier', 'cost'),
                E('Stability', '-2% at a new pressure tier', 'cost')], 'Palestine: Affected Core')
            n['mechanics'].append('Palestinian institutional pressure is automatic if Palestine exists '
                'with the affected core. Shared pressure is capped at two tiers per area, including '
                'party projects and existing footholds. No host or Palestinian approval.')
        n['effects'] += heading([E('Treasury', '-1.0% of annual GDP', 'cost'),
            E('Actual Private Project Capital', '+0.5% of annual GDP', 'neutral')],
            'With Funded Political-Risk Cover: Replaces the 1.5% Public Price')
        n['mechanics'].append('The reduced insured price requires a real 0.5%-GDP private contribution '
            'and an unused place in the funded two-project guarantee book. Otherwise the normal '
            '1.5%-GDP public price applies. Matched funding cannot pay an already reimbursed share.')
        renew(n, 26, 3)
    # The old road card now has its promised actual second-tier transaction.
    n = by['ISR2_west_bank_projects']
    template = deepcopy(by['ISR2_controlled_sites'])
    n.update({k: deepcopy(v) for k, v in template.items() if k not in ['id', 'xy', 'label', 'pre']})
    n.update(label='Extend the West Bank Access-Road Network', xy=[44, 11],
             pre=[['ISR2_controlled_sites']])
    n['mechanics'].append('Shares the same three-tier area counter with the first development card. '
                          'It is not an additional three-site allowance.')
    for key, state, x in foreign_ids:
        n = by.get('ISR2_' + key)
        if n is None:
            n = deepcopy(foreign_template); n['id'] = 'ISR2_' + key
            nodes.append(n); by[n['id']] = n
        effects=[]
        for e in foreign_template['effects']:
            if state not in ['West Bank', 'Gaza'] and 'Palestine' in e.get('heading', ''):
                continue
            item = deepcopy(e)
            item['heading'] = item.get('heading', '').replace('Per Funded Foreign Foothold: ', '').replace('Selected State', state)
            effects.append(item)
        n.update(label='Back a ' + state + ' Foothold beyond Israeli Control', xy=[49+x, 13],
            pre=[['ISR2_occupation_accounts']], effects=effects,
            requirements=['Israel does not control ' + state + '. Its actual controller exists.',
                'Fewer than two foreign foothold areas are currently funded.',
                'This area has no active funded foothold.', 'No freeze on new settlement projects is active.'],
            settlement_area=state, settlement_action='foreign_foothold',
            programme='Funded foreign foothold: consequences follow the actual host',
            mechanics=['Completion directly funds the named area without asking the host or Palestine. '
                'The full listed Israeli benefits and host/state penalties activate together while funded. '
                'No buildings, cores, annexation, host payment or positive host reward. '
                'At most two foreign areas, one foothold per area. Actual control changes replace or '
                'suspend this footprint without duplicate pressure or simultaneous controlled benefits.'])
        renew(n, 26)
    patch('funded_network', pre=[['ISR2_foreign_footholds', 'ISR2_gaza_foothold',
        'ISR2_sinai_foothold', 'ISR2_golan_foothold']], xy=[49, 14])
    for state, x in [('West Bank', -5), ('Gaza', -2), ('Sinai', 1), ('Golan', 4)]:
        slug = state.lower().replace(' ', '_')
        n = add('territories', 'close_' + slug, 'End Foreign Foothold Funding in ' + ('the ' if state=='West Bank' else '') + state,
            x, 8, 'Withdraw the financial support for the foothold beyond Israeli control. '
            'Its funded commercial advantages and mirrored burdens end together with the programme.',
            pre=['occupation_accounts'], effects=[
                E('Removes National Spirit', state + ' Public Settlement Sponsorship', 'neutral')],
            requirements=['A foreign foothold is funded in ' + state + '.', 'Israel does not control ' + state + '.'],
            icon='menorah', days=7, programme='End the funded foreign foothold in this area', mechanics=[
                'Closes only the non-building foreign foothold. Removes exactly its funded Israeli '
                'modifiers/streams, mirrored host/state penalties and attributed Palestinian pressure. '
                'Any separate controlled-site assets, security costs and Palestinian pressure remain '
                'bound to actual productive presence and control. This focus cannot waive those costs. '
                'Re-establishment pays its full setup price again. No territorial withdrawal or peace. '
                'Where a funding freeze is active, only the actual discounted expense is removed.'])
        n['icon'] = controlled_template['icon']
        n['settlement_area'] = state
        n['settlement_action'] = 'end_sponsorship'
        n['effects'] += heading([E('Office Productivity', '-4%, or -6% with the funded network', 'cost'),
            E('Agricultural Productivity', '-3%', 'cost')],
            'If a Foreign Foothold Is Active: Israel')
        n['effects'] += heading([budget('Foreign Foothold Funding Removed', .015),
            E('Funded Network Supplement Removed if Active', '+0.005% of annual GDP per week', 'gain')],
            'Israel: Without the Parliamentary Maintenance Discount')
        n['effects'] += heading([budget('Foreign Foothold Funding Removed', .012),
            E('Funded Network Supplement Removed if Active', '+0.004% of annual GDP per week', 'gain')],
            'Israel: With the 20% Parliamentary Maintenance Discount')
        n['effects'] += heading([E('Agricultural Productivity', '+3%', 'gain'),
            E('Police Cost', '-4%', 'gain'), E('Bureaucracy Cost', '-3%', 'gain')],
            'If a Foreign Foothold Is Active: Actual Host')
        n['effects'] += heading([E('Local Factory Access', '+5 percentage points', 'gain'),
            E('Local Supplies', '+8%', 'gain')], 'If a Foreign Foothold Is Active: ' + state)
        if state in ['West Bank', 'Gaza']:
            n['effects'] += heading([E('Office Productivity', '+4% per removed pressure tier', 'gain'),
                E('Bureaucracy Cost', '-4% per removed pressure tier', 'gain'),
                E('Stability', '+2% per removed pressure tier', 'gain')], 'Palestine: Affected Core')
        renew(n, 26)
    patch('cap_projects', label='Freeze New Settlement Projects',
        requirements=['At least one funded controlled settlement programme or foreign foothold exists.'],
        mechanics=['Completion freezes new settlement-start focuses and reduces existing sponsored-site '
                   'maintenance by 20%. Baseline occupation burdens and accepted insurance liabilities '
                   'remain. The separate appropriation focus can lift the freeze; no peace is imposed.'])
    lift = add('territories', 'lift_freeze', 'Reopen the Settlement Appropriation', 1, 10,
        'Return new settlement expenditure to the cabinet programme. The existing maintenance '
        'discount ends before another site can be funded.', pre=['cap_projects'], cost=.1,
        effects=[E('Settlement Maintenance Discount', '-20% becomes 0%', 'cost')],
        requirements=['A freeze on new settlement projects is active.'], icon='menorah', days=7,
        mechanics=['Lifts the focus availability restriction. The freeze focus can reopen only after '
                   'the current freeze is actually lifted, with no refund or recurring asset reward.'])
    lift['icon'] = controlled_template['icon']
    renew(by['ISR2_cap_projects'], 26)
    renew(lift, 26)

    # Pending offers are sent by focus completion, responses use recipient events.
    for n in nodes:
        if any(e.get('heading', '').startswith('If they accept: ') for e in n['effects']):
            n['offer_origin'] = 'focus_completion'
            n['recipient_response'] = 'country_event_accept_or_refuse'
            n['mechanics'].append('The focus sends the complete offer directly to the named recipient. '
                'The recipient accepts or refuses in a country event. No sender or recipient decision '
                'menu, automatic agreement or benefit on mere offer submission.')
    patch('negotiated_terms', label='Offer Funded Palestinian Service Compensation')
    # The existing political-risk focus now directly establishes its funded book.
    by['ISR2_labor_yanai']['mechanics'].append(
        'Completion reserves and funds the insurance book itself. Eligible territorial-development '
        'focus transactions use its reduced public price only with actual private co-financing.')

    # Specific foreign counterparts are focus choices as well. No target menu.
    api['SOURCES'].extend([
        dict(id='focus_kenya', title='Israeli Embassy in Kenya: bilateral relations',
             url='https://embassies.gov.il/kenya/en/the-embassy/bilateral-relations',
             note='The embassy dates the first Kenyan MASHAV trainees to 1965. The listed mission is a new RP offer.'),
        dict(id='focus_ethiopia', title='JTA, 1960: Israeli-Ethiopian technical cooperation',
             url='https://www.jta.org/archive/israel-ethiopian-ties-to-be-strengthened-joint-enterprises-planned',
             note='Contemporary water, irrigation and technical-training cooperation, not proof of this exact balance package.'),
        dict(id='focus_romania', title='Israeli Film Archive: Romanian commerce minister in Israel, 1969',
             url='https://jfc.org.il/en/news_journal/60675-2/102167-2/',
             note='Contemporary commercial relations support a new civilian workshop offer, not an automatic alliance.'),
        dict(id='focus_equipment', title='JTA, 8 May 1969: Israeli assistance in Africa',
             url='https://www.jta.org/archive/israels-aid-to-african-countries-has-had-mixed-results-washington-post-reports',
             note='Reports training and arms assistance in Uganda and Congo-Kinshasa. The new stock-based invoice is authored RP balance.'),
        dict(id='focus_signals', title='CIA, March 1979: Israeli intelligence relations',
             url='https://nsarchive2.gwu.edu/NSAEBB/NSAEBB407/docs/EBB-PollardDoc1.pdf',
             note='Retrospective primary account of cooperation with Iran and Turkey from 1958. No automatic organisation or operations.'),
    ])

    # Keep a diplomatic channel concrete without dictating a war or border outcome.
    jarring = by['ISR2_jarring_channel']
    jarring.update(label='Offer Egypt a Military Negotiating Channel',
        description='Propose a funded channel for Egyptian and Israeli officers to discuss incidents '
        'and ceasefire terms. Each cabinet retains its own position on territory and security.',
        effects=[], programme='Accepted military negotiating channel: 52 weeks',
        mechanics=['Acceptance funds the named liaison and its listed benefits for 52 weeks. '
                   'It does not end a war, move troops, transfer territory or prescribe a ceasefire. '
                   'Any political settlement remains a separate agreement between the actual governments.'])
    for country in ['Israel', 'Egypt']:
        jarring['effects'] += heading(paid(.15) + [budget('Military Negotiating Channel', -.003, 52),
            E('National Spirit', 'Military Negotiating Channel, 52 weeks', 'gain'),
            E('Police Cost', '-3%', 'gain')], 'If they accept: ' + country)

    irrigation = by['ISR2_irrigation_exports']
    irrigation['effects'] = heading([
        E('Treasury: Buyer Payment', '+$0.00600 billion', 'gain'),
        E('Treasury: Setup', '-$0.00200 billion', 'cost'),
        E('Irrigation Contract Maintenance', '-$0.00002 billion per week for 104 weeks', 'cost',
          native_key='weekly_budget', amount=-.00002, scope=104, unit='billion_dollars_per_week'),
        E('Ethiopia Opinion', '+10', 'gain')], 'If they accept: Israel') + heading([
        E('Treasury', '-$0.00600 billion', 'cost'),
        E('National Spirit', 'Precision Irrigation Contract, 104 weeks', 'gain'),
        E('Agricultural Productivity', '+10%', 'gain'),
        E('Israel Opinion', '+10', 'gain')], 'If they accept: Ethiopia')
    irrigation['mechanics'] = ['Both countries see one fixed $0.00600-billion invoice. '
        'Israel receives that exact payment, pays $0.00200 billion setup and $0.00002 billion '
        'weekly maintenance for 104 weeks. Full-term margin is $0.00192 billion before other '
        'national economic costs. The price and costs are authored balance, not a historical quote '
        'or a percentage of different countries\' GDP. The full +10% agricultural contract lasts '
        '104 weeks only while the paid maintenance and agreement remain active.']

    fixed = [
        ('irrigation_exports', 'Ethiopia', 'ETH', 'Offer Ethiopia a Precision-Irrigation Contract', 'focus_ethiopia'),
        ('mashav', 'Kenya', 'KEN', 'Send a MASHAV Mission to Kenya', 'focus_kenya'),
        ('arms_exports', 'Uganda', 'UGA', 'Offer Uganda an Equipment Contract', 'focus_equipment'),
        ('european_orders', 'Romania', 'ROM', 'Offer Romania a Civilian Workshop Partnership', 'focus_romania'),
        ('liaison_limits', 'Iran', 'PER', 'Offer Iran a Limited Signals Liaison', 'focus_signals'),
        ('washington', 'United States', 'USA', None, None),
        ('eastern_credit', 'Soviet Union', 'SOV', None, None),
        ('negotiated_terms', 'Palestine', 'PAL', None, None),
        ('labor_jordanian_option', 'Jordan', 'JOR', None, None),
        ('gahal_local_autonomy', 'Palestine', 'PAL', None, None),
        ('haolam_joint_services', 'Palestine', 'PAL', None, None),
        ('jarring_channel', 'Egypt', 'EGY', None, None),
    ]

    def target(n, country, tag, title=None, source=None):
        if title:
            n['label'] = title
        n['offer_target'] = dict(country=country, tag=tag)
        n['offer_origin'] = 'focus_completion'
        n['recipient_response'] = 'country_event_accept_or_refuse'
        n['requirements'] = [r for r in n['requirements'] if not r.startswith('The recipient is ')]
        n['requirements'].append('The recipient is ' + country + ', and its government can receive the offer.')
        n['requirements'].extend(['No offer of this programme to ' + country + ' is awaiting a response.',
            'No agreement of this exact programme with ' + country + ' is currently active.'])
        if source:
            n['history']['sources'] = list(dict.fromkeys(n['history']['sources'] + [source]))
            n['history']['status'] = 'Plausible agreement based on contemporary relations'
        for e in n['effects']:
            if e.get('heading') in ['If they accept: Recipient', 'If they accept: Buyer']:
                e['heading'] = 'If they accept: ' + country
            for generic in ['Recipient Opinion', 'Partner Opinion']:
                if e['label'] == generic:
                    e['label'] = (country if e.get('heading') == 'If they accept: Israel' else 'Israel') + ' Opinion'
        n['mechanics'].append('This card names ' + country + ' as the sole recipient. '
            'Completing it sends a real country event with acceptance and refusal. '
            'Its complete prospective effects remain inspectable before either response. '
            'No decision menu or automatic agreement.')
        if any(e.get('heading', '').startswith('If they accept: ') for e in n['effects']):
            weeks = 104 if n['id'] in {'ISR2_irrigation_exports', 'ISR2_european_orders',
                'ISR2_labor_jordanian_option', 'ISR2_gahal_local_autonomy', 'ISR2_eastern_credit'} else 52
            renew(n, weeks)
            n['mechanics'].append('An offer and its accepted contract share one record per programme '
                'and counterpart. Pending offers and active terms block a duplicate. The accepted term '
                'must actually end before renewal; refusal may reopen only the offer after a short '
                'diplomatic cooldown. Agreement replacements remove the old paired programme first.')

    for key, country, tag, title, source in fixed:
        target(by['ISR2_' + key], country, tag, title, source)

    for source, key, country, tag, title, evidence, xy in [
        ('mashav', 'mashav_ethiopia', 'Ethiopia', 'ETH', 'Send a MASHAV Mission to Ethiopia', 'focus_ethiopia', [30, 12]),
        ('arms_exports', 'arms_congo', 'Congo-Kinshasa', 'DRC', 'Offer Congo-Kinshasa an Arms Contract', 'focus_equipment', [24, 13]),
        ('liaison_limits', 'liaison_turkey', 'Turkey', 'TUR', 'Offer Turkey a Limited Signals Liaison', 'focus_signals', [38, 12]),
    ]:
        n = deepcopy(by['ISR2_' + source])
        old_country = n['offer_target']['country']
        n.update(id='ISR2_' + key, xy=xy)
        n.pop('focus_cycle', None)
        for e in n['effects']:
            if e.get('heading') == 'If they accept: ' + old_country:
                e['heading'] = 'If they accept: ' + country
            if e['label'] == old_country + ' Opinion':
                e['label'] = country + ' Opinion'
        n['mechanics'] = [m for m in n['mechanics'] if 'This card names ' not in m
                          and 'Only this action is reopened' not in m]
        n['requirements'] = [r for r in n['requirements'] if not r.startswith(('No offer of this programme', 'No agreement of this exact programme'))]
        nodes.append(n); by[n['id']] = n
        target(n, country, tag, title, evidence)
    # Different MASHAV/technical partners do not duplicate the same Israeli lesson.
    for key in ['mashav', 'mashav_ethiopia']:
        by['ISR2_' + key]['mechanics'].append(
            'The Israeli agricultural research lesson is awarded once per national programme, '
            'not again for a second partner or renewed mission. Recipient benefits are per actual contract.')
    for key in ['arms_exports', 'arms_congo']:
        by['ISR2_' + key]['requirements'].append('No Israeli export production contract is already pending.')
        by['ISR2_' + key]['mechanics'].append('All equipment-offer focuses share one pending Israeli order '
            'and the same per-buyer cooldown. A refusal reopens only this offer after a short diplomatic cooldown, '
            'without granting experience or charging setup fees. No research or experience on resending an offer.')
    # Clear generic target wording that would imply a later player menu.
    for n in nodes:
        if n.get('offer_target'):
            n['mechanics'] = [m.replace('to the named recipient', 'to its fixed recipient') for m in n['mechanics']]
    # All sponsored settlement projects use the same freeze and area counters.
    for key, state in [('labor_valley', 'West Bank'), ('gahal_settler_entitlement', 'West Bank'),
                       ('mafdal_activist_current', 'West Bank'), ('mafdal_land_westbank', 'West Bank'),
                       ('mafdal_land_gaza', 'Gaza'), ('mafdal_regularise_sites', 'West Bank')]:
        n = by['ISR2_' + key]
        n['settlement_area'] = state
        for req in ['No freeze on new settlement projects is active.',
                    'The area has fewer than three paid controlled settlement tiers.']:
            if req not in n['requirements']:
                n['requirements'].append(req)
        n['mechanics'].append('Shares the common area development counter and institutional-pressure '
            'attribution. Freezing new projects does not remove existing productive sites or their '
            'site-bound security and Palestinian consequences.')
    freeze = by['ISR2_mafdal_restrain_sites']
    freeze['mechanics'] = ['While active, this policy supplies a real reason in the common settlement '
        'freeze. Every national and party settlement-start focus checks that same freeze. '
        'Reopening appropriations removes both this policy\'s police/personnel savings and any '
        'parliamentary maintenance discount before a new project can start. Existing sites, '
        'baseline occupation and funded foreign foothold obligations remain.']
    by['ISR2_cap_projects']['freeze_reason'] = 'parliamentary_appropriation'
    freeze['freeze_reason'] = 'mafdal_commitment_policy'
    lift = by['ISR2_lift_freeze']
    lift['pre'] = [['ISR2_cap_projects', 'ISR2_mafdal_restrain_sites']]
    lift['effects'] = paid(.1) + heading([
        E('Settlement Maintenance Discount', '-20% becomes 0%', 'cost')],
        'If the Parliamentary Funding Freeze Is Active') + heading([
        E('Removes National Spirit', 'Refusal of New Unauthorised Commitments', 'neutral'),
        E('Police Cost', '+6%', 'cost'), E('Personnel Cost', '+3%', 'cost')],
        'If the Mafdal Commitment Policy Is Active')
    lift['mechanics'].append('Clears every active settlement-start freeze reason together. '
        'The Mafdal police/personnel savings and generic maintenance discount are removed before '
        'new starts are enabled. They cannot survive reopening under another party.')

    empty = [n['id'] for n in nodes if not n['effects']]
    return dict(project='IMPERIA COLD WAR',revision='2.2-focus-only-20261028',
        original_decision_focuses=len(originals), original_decision_unlocks=sum(map(len, originals.values())),
        converted_actions=originals, decisions=0, pending_empty_effects=empty,
        native_reset_reference='common/scripted_effects/99_ENG_scripted_effects..txt:956',
        evidence='Design only. Native focus reset exists; lifecycle handlers are proposed, not implemented.')
