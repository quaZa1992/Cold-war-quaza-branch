"""Domestic regime paths for the reviewable Greece design, never runtime assets."""


def add_paths(section, node, either, exclusive, prefix):
    section('opening', 'GREECE UNDER THE COLONELS', 42, 0)
    node('greece_1970', 'Greece in January 1970', 'opening', (0, 0), pp=25, days=21, icon='junta',
         note='Papadopoulos governs; Zoitakis is regent; Constantine II is in exile. The military regime can endure, open on its own terms, or negotiate an actual civilian transfer.')
    node('state_dossier', 'Open the State Dossier', 'opening', (0, 2), ['greece_1970'], pp=25, days=21, icon='constitution')
    node('officer_loyalties', 'Map the Officer Networks', 'opening', (-6, 4), ['state_dossier'], xp=['army', 10], days=28, icon='army',
         note='Papadopoulos and Ioannidis represent competing circles. Mapping loyalties does not execute a coup or arrest anyone.')
    node('civilian_contacts', 'Reopen Civilian Channels', 'opening', (0, 4), ['state_dossier'], days=28, icon='election',
         note='Sound out domestic opposition and exiles. Contact does not confer office, electoral consent or an automatic democratic mandate.')
    node('economic_stocktake', 'Take Stock of the Expansion', 'opening', (6, 4), ['state_dossier'], pp=25, days=28, icon='industry',
         note='Real industrial, shipping and tourist strengths coexist with regional inequality and patronage. No fabricated starting recession.')

    section('regime', 'THE REGIME QUESTION · THREE FOCUS PATHS', 42, 8,
            'Choose continued military rule, a supervised opening, or an actual civilian handover. These are focus paths. Later negotiated exits have their own focuses, costs and replacement effects.')

    def add(key, title, xy, parents, *, package=None, transition=None, benefits=(), costs=(), lasting=(), **kw):
        n = node(key, title, 'regime', xy, parents, **kw)
        n['tradeoff'] = dict(benefits=list(benefits), costs=list(costs), lasting=list(lasting))
        if package:
            n['regime_package'] = package
        if transition:
            n['transition_package'] = transition
        return n

    packages = {
        'military': dict(key='military_order', title='Entrenched Military Government',
            modifiers={'political_power_factor': .10, 'max_planning': .04, 'research_speed_factor': -.03, 'police_cost_multiplier_modifier': .05},
            removes=[], retains=['rule_by_decree', 'security_state', 'european_censure', 'politicised_officers'],
            flag='military_government_active'),
        'controlled': dict(key='controlled_order', title='A Supervised Civilian Cabinet',
            modifiers={'political_power_factor': .05, 'stability_factor': .02, 'bureaucracy_cost_multiplier_modifier': .03},
            removes=['rule_by_decree', 'security_state'], retains=['european_censure', 'politicised_officers'],
            adds=[dict(key='reserve_powers', title='Military Reserve Powers', modifiers={'stability_factor': -.03, 'political_power_factor': .03}),
                  dict(key='restricted_public_life', title='Restricted Public Life', modifiers={'police_cost_multiplier_modifier': .08, 'stability_factor': -.03}),
                  dict(key='unresolved_victim_claims', title='Unresolved Victim Claims', modifiers={'stability_factor': -.02, 'social_cost_multiplier_modifier': .03})],
            flag='controlled_government_active'),
        'civilian': dict(key='civilian_order', title='A Parliamentary Civilian Mandate',
            modifiers={'stability_factor': .06, 'research_speed_factor': .03},
            removes=['rule_by_decree', 'security_state', 'reserve_powers', 'restricted_public_life', 'crown_in_exile'],
            retains=['european_censure', 'politicised_officers'],
            adds=[dict(key='unresolved_victim_claims', title='Unresolved Victim Claims', modifiers={'stability_factor': -.02, 'social_cost_multiplier_modifier': .03})],
            flag='civilian_government_active'),
    }
    review = dict(key='transition_review', title='Negotiating the Civilian Transfer', duration_days=365,
                  modifiers={'political_power_factor': -.10, 'bureaucracy_cost_multiplier_modifier': .08},
                  note='A funded, time-limited administrative and legal review. Expiry does not itself transfer power or restore rights. One active idea; restarting talks does not stack penalties.')

    add('retain_junta', 'Keep the Junta in Power', (-12, 0), ['officer_loyalties'], days=35, icon='junta',
        benefits=['Unlock a lasting military-government path and either officer compact.'],
        costs=['Retain decree rule, the coercive security apparatus and European censure.'],
        note='A viable alternate-history state, not a countdown to an unavoidable 1974 collapse.')
    add('controlled_opening', 'Open the Regime on Its Own Terms', (0, 0), ['civilian_contacts'], days=35, icon='constitution',
        benefits=['Negotiate selective civilian participation while preserving executive leverage.'],
        costs=['A civilian prime minister alone does not end military reserve powers or censorship.'],
        note='Papadopoulos / Markezinis is the historical reference. An earlier or successful continuation is alternate history, not an automatic 1973 event.')
    add('civilian_transition', 'Hand Power to Civilian Government', (12, 0), ['civilian_contacts'], days=35, icon='election',
        benefits=['Open the route to free elections, accountable institutions and civilian party programmes.'],
        costs=['No military-government command package; negotiations, funded legal work and a real mandate are still required.'],
        note='The player chooses the transition path. No Cyprus war, foreign approval, prescribed election winner or fixed 1974 collapse is required.')
    for a, b in [('retain_junta', 'controlled_opening'), ('retain_junta', 'civilian_transition'), ('controlled_opening', 'civilian_transition')]:
        exclusive(a, b)

    add('military_compact', 'Put the Officer Compact in Writing', (-12, 2), ['retain_junta'], package=packages['military'], icon='junta', days=42,
        benefits=['Political power gain +10%; maximum planning +4% from concentrated decree authority and command preparation.'],
        costs=['Research speed -3%; police cost +5%; all four listed regime legacies remain.'],
        lasting=['National regime slot: replaces every previous regime package; benefits end on civilian handover.'],
        requires='Military junta actually remains in office and the officer compact has been implemented.')
    add('professional_compact', 'Bargain with the Service Commands', (-15, 4), ['military_compact'],
        mods={'army_org_factor': .05, 'political_power_factor': -.02}, slot='officer_compact', icon='army',
        benefits=['Army organisation +2% after the shared military balance scale.'], costs=['Political power gain -2%; service chiefs retain bargaining power.'],
        note='Improves coordination; it does not magically remove the Politicised Officer Corps starting spirit.')
    add('security_compact', 'Entrench the Security Directorate', (-9, 4), ['military_compact'],
        mods={'political_power_factor': .05, 'police_cost_multiplier_modifier': .06, 'stability_factor': -.03}, slot='officer_compact', icon='junta',
        benefits=['Political power gain +5% through executive control.'], costs=['Police cost +6%; stability -3%; arbitrary detention and torture retain their grievance and accountability.'],
        note='This supports an Ioannidis-style internal struggle only if the domestic leadership contest actually succeeds. No extra combat bonus is attached to torture.')
    exclusive('professional_compact', 'security_compact')
    add('service_procurement', 'Fund a Joint-Service Supply Plan', (-15, 6), ['professional_compact'], cost=.8, xp=['army', 15], icon='army',
        benefits=['15 army experience; a funded supply plan.'], costs=['One-time treasury payment: 0.8% of GDP.'])
    add('security_budget', 'Account for the Security Budget', (-9, 6), ['security_compact'], cost=.8, pp=20, icon='money',
        benefits=['20 political power after implementation.'], costs=['One-time treasury payment: 0.8% of GDP; continued recurring police costs.'])
    n = add('lasting_junta', 'A Military Government Built to Last', (-12, 8), ['service_procurement', 'security_budget'], pp=25, icon='junta',
        benefits=['Keep the regime package and access Papadopoulos or an actually victorious rival government.'],
        costs=['Political opposition and external censure remain; neither date nor completion supplies international legitimacy.'])
    either(n, 'service_procurement', 'security_budget')
    add('military_development', 'Direct Credit through the Regime Banks', (-15, 10), ['lasting_junta'],
        mods={'production_factory_max_efficiency_factor': .03, 'bureaucracy_cost_multiplier_modifier': .04}, slot='regime_development', cost=1, icon='industry',
        benefits=['Factory efficiency cap +1.05% after the shared economic balance scale.'],
        costs=['Bureaucracy cost +4%; one-time payment 1% of GDP; the programme ends when this regime ends.'])
    n = add('military_exit', 'Negotiate an Exit for the Colonels', (-9, 12), ['lasting_junta', 'tutelary_charter', 'reverse_opening'], transition=review, cost=.5, icon='constitution',
        benefits=['A later route to civilian institutions despite the initial choice to retain the junta.'],
        costs=['0.5% of GDP; 365-day political power and bureaucracy penalty; relinquish the military regime and its development bonuses on actual handover.'],
        requires='Actual domestic negotiations have established a workable transfer agreement; no foreign seat can be forced to approve it.',
        note='A later exit remains available after durable junta rule, a retained tutelary veto, or an actual hardline reversal of the opening. It does not require the initially excluded military-entry focus. A genuine handover replaces old benefits rather than harvesting both regimes.')
    either(n, 'lasting_junta', 'tutelary_charter', 'reverse_opening')

    add('supervised_cabinet', 'Appoint a Supervised Civilian Cabinet', (0, 2), ['controlled_opening'], package=packages['controlled'], cost=.5, icon='constitution', days=42,
        benefits=['Political power gain +5%; stability +2%; partial reduction of the original decree and policing penalties.'],
        costs=['Bureaucracy cost +3%; 0.5% of GDP; replacement reserve-powers and restricted-public-life spirits remain.'],
        lasting=['European Censure is retained. A civilian cabinet is not a free election or an international rehabilitation.'],
        requires='An actual cabinet agreement and implemented limited reforms; Papadopoulos still controls the regime.')
    add('retain_veto', 'Keep the Military Veto', (-3, 4), ['supervised_cabinet'], icon='junta',
        mods={'political_power_factor': .03, 'stability_factor': -.02}, slot='controlled_constitution',
        benefits=['Political power gain +3%; supervised government remains viable.'], costs=['Stability -2%; no parliamentary-mandate package; restricted political competition remains.'])
    add('renounce_veto', 'Negotiate Away the Military Veto', (3, 4), ['supervised_cabinet'], transition=review, icon='election', cost=.5,
        benefits=['Unlock actual civilian transfer without a compulsory hardline coup.'],
        costs=['0.5% of GDP; 365-day transition review; officer objections require a real domestic settlement.'])
    exclusive('retain_veto', 'renounce_veto')
    add('tutelary_charter', 'Ratify a Tutelary Constitution', (-3, 6), ['retain_veto'], pp=25, icon='constitution',
        benefits=['25 political power; lasting supervised government.'], costs=['The armed forces retain reserve powers; democratic legitimacy and Council of Europe restoration are not granted.'],
        requires='A domestic charter is actually adopted; a controlled vote cannot count as a competitive parliamentary mandate.')
    add('opening_handover', 'Implement the Civilian Handover', (3, 6), ['renounce_veto'], icon='election',
        benefits=['Enter the common constitutional transition path.'], costs=['Actual handover removes military and supervised-government bonuses, including their economic programmes.'],
        requires='The transfer agreement is actually accepted and military executive vetoes are removed.')
    add('opening_tourism', 'Finance the Supervised Tourism Opening', (-3, 8), ['tutelary_charter'], cost=1,
        mods={'production_speed_buildings_factor': .06, 'social_cost_multiplier_modifier': .03}, slot='regime_development', icon='industry',
        benefits=['Construction speed +1.8% after the shared economic balance scale.'], costs=['Social spending cost +3%; one-time 1% of GDP; dependence on external visitors remains.'])
    add('reverse_opening', 'Back the Hardliners against the Opening', (-3, 10), ['tutelary_charter'], package=packages['military'], icon='junta',
        stability=-.04, benefits=['Return to the military command package if the domestic hardline contest actually succeeds.'],
        costs=['One-time stability -4%; restore the full decree and security-state penalties; lose the opening economy and constitution packages.'],
        requires='An actual domestic power struggle has resolved in favour of military hardliners. Ioannidis is not installed by a date.',
        note='The struggle is player-authorised and domestic; no automatic overthrow or Cyprus coup. An unsuccessful bid pays its consequences without a successful-regime reward.')

    add('transition_offer', 'Agree the Terms of a Civilian Transfer', (12, 2), ['civilian_transition'], transition=review, cost=.5, icon='constitution', days=42,
        benefits=['A written domestic transition agreement; free elections become a possible outcome.'],
        costs=['0.5% of GDP; political power gain -10% and bureaucracy cost +8% for 365 days.'],
        requires='A real domestic transfer agreement; a focus proposal alone is not acceptance.')
    add('civilian_preparation', 'Prepare a Civilian Administration', (12, 4), ['transition_offer'], cost=.5, pp=20, icon='constitution',
        benefits=['20 political power and institutional preparation.'], costs=['0.5% of GDP; election results and foreign rehabilitation remain unsettled.'])
    add('legal_parties', 'Restore the Freedom to Organise', (12, 6), ['civilian_preparation'], icon='election',
        benefits=['End the party ban and establish free organisation before an election.'], costs=['The ruler loses the ability to select a compliant winner.'],
        requires='The transfer agreement has been implemented and actual freedom to organise is protected.',
        note='Legal competition does not determine which party wins or prematurely create ND or PASOK.')

    # All three negotiated exits feed the same obligations. Initial exclusivity
    # cannot permanently lock out reform, and a later exit cannot skip its costs.
    n = add('civilian_institutions', 'Return Authority to Civil Institutions', (12, 16), ['legal_parties', 'opening_handover', 'military_exit'], icon='constitution',
        benefits=['Join one shared transition with the same legal and electoral obligations.'],
        costs=['Immediately replace military / controlled packages on actual transfer; prior decree advantages cannot persist.'],
        requires='An actual executive transfer has been implemented; review obligations and protected political competition are active.')
    either(n, 'legal_parties', 'opening_handover', 'military_exit')
    n['clear_regime_on_transfer'] = True
    add('civilian_accountability', 'Launch Independent Junta Investigations', (9, 18), ['civilian_institutions'],
        mods={'stability_factor': .03, 'bureaucracy_cost_multiplier_modifier': .04}, slot='transition_justice', cost=.8, icon='constitution',
        benefits=['Stability +3% from credible, independent investigation safeguards.'], costs=['Bureaucracy cost +4% for continuing casework; 0.8% of GDP; officer resistance must be resolved.'],
        note='Secure evidence and judicial independence before the election. Trials and verdicts can follow later; the historical major trials occurred in 1975. No completed trial is required for voting.')
    add('civilian_retirement', 'Negotiate Retirement and a Limited Amnesty', (15, 18), ['civilian_institutions'],
        mods={'political_power_factor': .03, 'stability_factor': -.02, 'social_cost_multiplier_modifier': .02}, slot='transition_justice', cost=.5, icon='army',
        benefits=['Political power gain +3% from the negotiated officer exit.'], costs=['Stability -2%; social cost +2%; 0.5% of GDP; victim claims and demands for accountability remain.'],
        note='The limited settlement concerns defined nonviolent or lesser participation. Torture and other serious abuses remain individually investigable; evidence, civil claims and compensation rights survive on both paths. Retirement is not innocence.')
    exclusive('civilian_accountability', 'civilian_retirement')
    add('open_courts', 'Protect the Independent Courts', (9, 20), ['civilian_accountability'], icon='constitution', pp=25,
        benefits=['25 political power after the court safeguards are implemented.'], costs=['Accountability programme and victim obligations remain funded; no erasure of casework.'])
    add('retirement_guarantees', 'Enforce the Officer Retirement Agreement', (15, 20), ['civilian_retirement'], icon='army', pp=25,
        benefits=['25 political power after enforceable retirement terms and civilian-command guarantees.'], costs=['No simultaneous prosecution legitimacy reward; serious abuses remain investigable and victim claims survive.'],
        note='Implementation and lengthy casework can continue after the election. Guarantees do not require every retirement or criminal trial to have concluded.')
    n = add('credible_election', 'Hold a Free Parliamentary Election', (12, 22), ['open_courts', 'retirement_guarantees'], icon='election', days=49,
        benefits=['An actual parliamentary mandate unlocks the appropriate governing-party programme.'],
        costs=['The incumbent must accept the implemented vote; no prescribed Karamanlis or Papandreou victory.'],
        requires='Freedom to organise, genuine electoral rules and an implemented vote; actual winner follows party support / agreed multiplayer procedure.')
    either(n, 'open_courts', 'retirement_guarantees')
    add('constitutional_question', 'Ratify the Civilian Constitutional Settlement', (12, 24), ['credible_election'], package=packages['civilian'], icon='constitution', days=49,
        benefits=['Stability +6%; research speed +3%; retire decree rule and the active coercive-state package.'],
        costs=['Lose the junta / supervised political-power, planning and regime-development bonuses; unresolved victim claims remain.'],
        lasting=['European Censure and the Politicised Officer Corps need separate real reforms. Constitutional monarchy remains possible through an actual ratified settlement.'],
        requires='A real civilian executive, implemented civil liberties and a valid constitutional mandate. A referendum result may choose republic or a parliamentary crown.')
    add('civilian_enterprise', 'Rebuild Credit under Independent Courts', (9, 26), ['constitutional_question'],
        mods={'production_factory_max_efficiency_factor': .03, 'bureaucracy_cost_multiplier_modifier': .02}, slot='regime_development', cost=1, icon='industry',
        benefits=['Factory efficiency cap +1.05% after the shared balance scale.'], costs=['Bureaucracy cost +2%; one-time 1% of GDP; competing claims require transparent due process.'])
    add('civilian_reconstruction', 'Put Regional Reconstruction First', (15, 26), ['constitutional_question'],
        mods={'production_speed_buildings_factor': .06, 'social_cost_multiplier_modifier': .04}, slot='regime_development', cost=1, icon='housing',
        benefits=['Construction speed +1.8% after the shared balance scale.'], costs=['Social spending cost +4%; one-time 1% of GDP; fewer resources for direct industrial credit.'])
    exclusive('civilian_enterprise', 'civilian_reconstruction')
    n = add('civilian_settlement', 'A Government Chosen by Its Citizens', (12, 28), ['civilian_enterprise', 'civilian_reconstruction'], icon='election', pp=25,
        benefits=['25 political power after auditing the funded programme; civilian party paths remain available to the actual winner.'],
        costs=['A change of government replaces party programmes; it cannot stack seven governments or restore military perks.'])
    either(n, 'civilian_enterprise', 'civilian_reconstruction')
    return packages


def apply_gates(nodes, prefix):
    """Political roots use factual regime gates, matching MD independent sectors."""
    for n in nodes:
        sec = n['section']
        if sec in ('pap', 'ioa', 'nd', 'centre', 'pasok', 'kke', 'royal'):
            if n['local_y'] == 0:
                n['prerequisite_groups'] = []
            if sec == 'pap':
                flags = ['military_government_active', 'controlled_government_active']
            elif sec == 'ioa':
                flags = ['military_government_active']
            elif sec == 'kke':
                flags = ['civilian_transfer_implemented', 'civilian_government_active', 'socialist_revolution_resolved', 'socialist_executive_government_active']
            elif sec == 'royal':
                flags = ['civilian_transfer_implemented', 'civilian_government_active', 'royal_executive_settlement_implemented']
            else:
                flags = ['civilian_transfer_implemented', 'civilian_government_active']
            n['required_regime_flags'] = flags
            n['requirements'] += ' Actual active regime: ' + ' OR '.join(flags) + '. A party label alone cannot bypass the regime path.'
    by = {n['key']: n for n in nodes}
    by['pap_2']['required_regime_flags'] = ['controlled_government_active']
    by['pap_2']['requirements'] += ' A controlled opening is being negotiated or implemented; a later policy change must replace the current regime package.'
    by['pap_3']['requirements'] += ' Continued military rule or a retained military veto is actually in force.'
    # The opening owns regime-wide justice, veto and handover settlements.
    # Party programmes add their own implementation, never cancel a rival deal.
    for key in ('nd_2', 'nd_4', 'centre_2', 'centre_4'):
        by[key]['requirements'] += ' Independent courts exist; this follow-up does not award the opposing officer-amnesty bargain.'
        by[key]['required_completed_focus'] = ['civilian_accountability']
        by[key]['required_active_idea'] = 'civilian_accountability_programme'
    for key in ('nd_3', 'nd_5', 'centre_3', 'centre_5'):
        by[key]['requirements'] += ' Retain the actual prior justice settlement; negotiations cannot annul completed court judgements.'
        by[key]['required_completed_focus'] = ['civilian_retirement']
        by[key]['required_active_idea'] = 'civilian_retirement_programme'
    for key in ('professional_compact', 'security_compact', 'military_development'):
        by[key]['required_regime_flags'] = ['military_government_active']
    for key in ('retain_veto', 'opening_tourism'):
        by[key]['required_regime_flags'] = ['controlled_government_active']
    for key in ('civilian_accountability', 'civilian_retirement'):
        by[key]['required_regime_flags'] = ['civilian_transfer_implemented', 'civilian_government_active']
    for key in ('civilian_enterprise', 'civilian_reconstruction'):
        by[key]['required_regime_flags'] = ['civilian_government_active']
    for key, flag, title in [('kke_3', 'socialist_executive_government_active', 'A Socialist Executive State'), ('royal_3', 'royal_executive_settlement_implemented', 'A Crown above Parliament')]:
        by[key]['regime_package'] = dict(key='socialist_executive_order' if key=='kke_3' else 'royal_executive_order', title=title,
            modifiers={'political_power_factor': .04, 'stability_factor': -.03}, removes=['civilian_order'], retains=['unresolved_victim_claims', 'european_censure', 'politicised_officers'], flag=flag)
        by[key]['requirements'] += ' Actual constitutional change has replaced parliamentary supremacy; party election alone does not authorise it.'
        by[key]['note'] += ' Replaces the parliamentary regime spirit and its research / stability gains; all existing victim claims survive. This is a change of constitutional order, not an ordinary party change.'
    # The generic shared army branch cannot "professionalise" the services while
    # a completed focus still mandates political security command.
    by['army_6']['requirements'] += ' Actual professional command reform; replace incompatible political-command bonuses and do not erase victims\' claims.'
    # Distinct factual milestones. Proposed Greek flags are set by the domestic
    # transition/election adapter only when the stated outcome actually occurs.
    for key, flag in {
        'military_compact': 'officer_compact_implemented',
        'supervised_cabinet': 'supervised_cabinet_implemented',
        'reverse_opening': 'hardline_power_struggle_won',
        'military_exit': 'negotiated_transfer_agreed',
        'opening_handover': 'executive_transfer_implemented',
        'transition_offer': 'negotiated_transfer_agreed',
        'civilian_institutions': 'executive_transfer_implemented',
        'credible_election': 'free_election_implemented',
        'constitutional_question': 'civilian_constitution_ratified',
        'kke_3': 'socialist_executive_settlement_ratified',
        'royal_3': 'royal_executive_settlement_ratified',
    }.items():
        by[key]['actual_outcome_flag'] = flag
        by[key]['event_contract'] = 'NEW domestic adapter: the preceding path proposes this outcome; record ' + prefix + flag + ' only after the stated domestic agreement or implementation. This focus records/implements that actual result, with no foreign action.'


def effect_lines(n, nodes, prefix):
    """Native primitives for proposed Greek ideas, with explicit replacement."""
    lines = []
    package = n.get('regime_package')
    if package or n.get('clear_regime_on_transfer'):
        lines.append(prefix + 'clear_regime_programmes_effect = yes # NEW wrapper defined in proposed_scripted_effects.txt; native remove_ideas / clr_country_flag only')
        if n.get('clear_regime_on_transfer') or package['key']!='civilian_order':
            lines.append('clr_country_flag = ' + prefix + 'current_electoral_mandate_verified')
        if n.get('clear_regime_on_transfer'):
            lines += ['remove_ideas = ' + prefix + key for key in ('rule_by_decree', 'reserve_powers', 'security_state', 'restricted_public_life')]
            lines.append('add_ideas = ' + prefix + 'unresolved_victim_claims')
            lines.append('set_country_flag = ' + prefix + 'civilian_transfer_implemented')
        if package:
            lines += ['remove_ideas = ' + prefix + key for key in package.get('removes', [])]
            if package['key'] == 'military_order':
                lines += ['remove_ideas = ' + prefix + key for key in ('reserve_powers', 'restricted_public_life')]
                lines += ['add_ideas = ' + prefix + key for key in ('rule_by_decree', 'security_state')]
            lines.append('add_ideas = ' + prefix + package['key'] + ' # NEW Greek regime idea; see regime_package.modifiers')
            lines += ['add_ideas = ' + prefix + extra['key'] for extra in package.get('adds', [])]
            lines.append('set_country_flag = ' + prefix + package['flag'])
    if n.get('transition_package'):
        t = n['transition_package']
        lines.append('remove_ideas = ' + prefix + t['key'])
        lines.append('add_timed_idea = { idea = ' + prefix + t['key'] + ' days = ' + str(t['duration_days']) + ' } # NEW Greek transition idea, one refreshed instance')
    return lines


def proposed_effects(nodes, prefix):
    """Full new wrappers, stored in docs only; never installed in common/."""
    lines = ['# DESIGN ONLY. New Greek wrappers; no runtime installation.', prefix + 'clear_regime_programmes_effect = {']
    for key in ('military_order', 'controlled_order', 'civilian_order', 'socialist_executive_order', 'royal_executive_order'):
        lines.append(' remove_ideas = ' + prefix + key)
    for key in ('military_government_active', 'controlled_government_active', 'civilian_government_active', 'civilian_transfer_implemented', 'socialist_executive_government_active', 'royal_executive_settlement_implemented'):
        lines.append(' clr_country_flag = ' + prefix + key)
    for n in nodes:
        if n['modifiers'] and (n.get('modifier_slot') in ('officer_compact', 'controlled_constitution', 'regime_development') or n['section'] in ('pap', 'ioa', 'nd', 'centre', 'pasok', 'kke', 'royal')):
            lines.append(' remove_ideas = ' + n['id'] + '_programme')
    lines += ['}', '', '# Reconcile the actual current regime/party after a change. Never repeat payments, PP, XP or instant stability rewards.', prefix + 'reconcile_programmes_effect = {']
    for n in nodes:
        if not n['modifiers'] or n.get('duration_days'):
            continue
        # Only these permanent funded policies can be re-enabled. The original
        # _granted flag records the paid investment and is never cleared.
        gate=n['available_code'].splitlines()
        gate=[s for s in gate if s.strip() and not s.lstrip().startswith('#')]
        if n['key']=='energy_ration':
            gate=[s for s in gate if s.strip()!='has_idea = '+prefix+'oil_shock']
            gate.append('OR = { has_idea = '+prefix+'oil_shock has_idea = '+prefix+'oil_shock_rationed }')
        lines += [' if = {', '  limit = {', '   has_country_flag = ' + n['id'] + '_granted']
        lines += ['   ' + s for s in gate]
        lines += ['  }', '  add_ideas = ' + n['id'] + '_programme', ' }', ' else = { remove_ideas = ' + n['id'] + '_programme }']
    lines += ['}', '# Invoke reconciliation after actual leadership / constitutional / policy changes.', '# Timed programmes are excluded: their expiration never recreates them.']
    return '\n'.join(lines) + '\n'

