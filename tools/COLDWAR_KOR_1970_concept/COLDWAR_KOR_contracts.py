# IMPERIA CW — Cold War: explicit approval-stage Korean diplomatic contracts.
"""New content contracts, built on existing MD primitives; not installed events."""

def policy(slot,**kwargs):return {'slot':slot,'modifiers':kwargs}

def contract(key,recipient,cost,weekly,benefits,recipient_effects,description,duration=1095):
    return {'id':'COLDWAR_KOR_'+key,'key':key,'recipient':recipient,
      'description':description,'KOR_cost_bn':cost,'KOR_weekly_bn':weekly,
      'KOR_policy':benefits,'recipient_effects':recipient_effects,'duration_days':duration,
      'status':'NEW KOR contract design; existing MD APIs, no existing KOR event claimed',
      'acceptance':'Both countries exist, are independent, at peace with one another; proposer government still eligible; no duplicate/pending signed contract; intended construction state owned and controlled, with capacity if any.',
      'refusal':'No payment, construction or agreement modifier. Record refusal for domestic continuation; renegotiation decision after 180 days.',
      'expiry':'Pending offer expires after 60 days with no charge. Signed limited agreements last stated duration, can be renewed by mutual consent; end immediately on bilateral war or departure of required signatory. Already delivered one-time benefits never replay.',
      'execution':'Charge and grant only inside accepted, revalidated, once-only recipient response; numeric native option effects for each payer/recipient; clear pending flags and send proposer reply.'}

def enrich(data):
    C=[]
    def add(*args,**kw):C.append(contract(*args,**kw))
    add('red_cross_channel','NKO',0,0,[],{},'Exchange humanitarian liaison representatives. No passive stat reward.',0)
    add('family_reunions','NKO',1,0.001,
        [policy('humanitarian',stability_factor=0.025)],
        {'treasury_change':-1,'weekly_expense_bn':0.001,'policy':{'stability_factor':0.025}},
        'Each Korea pays $1bn to establish visits and $0.001bn weekly for three years; each gains +2.5% stability. Separate from existing remittance schemes.')
    add('military_hotline','NKO',0,0.0005,
        [policy('hotline',army_core_defence_factor=0.02,bureaucracy_cost_multiplier_modifier=0.02)],
        {'weekly_expense_bn':0.0005,'policy':{'army_core_defence_factor':0.02,'bureaucracy_cost_multiplier_modifier':0.02}},
        'Both fund $0.0005bn weekly communication links. Core defence +2%, bureaucracy expenses +2%; no offensive coordination.')
    add('nonaggression_compact','NKO',0,0,[],{},
        'Add a native bilateral nonaggression pact after acceptance; no forced military access, faction, disarmament or territory. Existing alliances remain subject to their own treaties.',0)
    add('verified_restraint','NKO',1,0.001,
        [policy('verification',stability_factor=0.03,army_attack_factor=-0.03)],
        {'treasury_change':-1,'weekly_expense_bn':0.001,'policy':{'stability_factor':0.03,'army_attack_factor':-0.03}},
        'Each side pays $1bn plus $0.001bn weekly for reciprocal verification; stability +3%, division attack -3%. Military commitments end on withdrawal or bilateral war.')
    add('working_contacts','NKO',0,0,[],{},'Maintain official working contacts; no free industrial or military effect.',0)
    add('sovereign_confederation','NKO',0,0,[],{},
        'Use the existing NKO confederation-channel model for a sovereign consultative framework. Separate governments, armies, economics and player control; no automatic faction, puppet or annexation.',0)
    add('confederal_secretariat','NKO',1,0.002,
        [policy('secretariat',trade_opinion_factor=0.04,bureaucracy_cost_multiplier_modifier=0.03)],
        {'treasury_change':-1,'weekly_expense_bn':0.002,'policy':{'trade_opinion_factor':0.04,'bureaucracy_cost_multiplier_modifier':0.03}},
        'Both pay $1bn and $0.002bn weekly for a consultative secretariat; trade opinion +4%, bureaucracy expenses +3%. No organizational focus until the actual membership spirit is present.')
    add('parallel_recognition','NKO',0,0,[],{},'Recognize parallel governments through mutual declarations. No free UN membership, diplomatic recognition from third parties or annexation.',0)
    add('limited_trade','NKO',1,0.002,
        [policy('korean_trade',production_factory_max_efficiency_factor=0.025,foreign_influence_defense_modifier=-0.03)],
        {'treasury_change':1,'policy':{'production_factory_max_efficiency_factor':0.025,'foreign_influence_defense_modifier':-0.03},'weekly_income_bn':0.002},
        'KOR funds $1bn access and $0.002bn weekly purchases to NKO; both gain efficiency cap +2.5%, influence defence -3%. Capped abstraction of civilian exchange, no free resources or arms.')
    add('northern_security_compact','NKO',1,0.001,
        [policy('north_security',army_org_factor=0.04,foreign_influence_defense_modifier=-0.08,trade_opinion_factor=-0.04)],
        {'treasury_change':1,'weekly_income_bn':0.001,'policy':{'army_org_factor':0.02,'trade_opinion_factor':-0.02}},
        'Only for an actual RPR government. KOR pays NKO $1bn plus $0.001bn weekly for military liaison; limited readiness, dependence and external-access effects. No automatic allied formations.')
    add('independent_left_dialogue','NKO',0,0,[],{},'Open talks from an independent Southern socialist government; no union or surrender of sovereignty.',0)
    add('technology_licence','One chosen consenting supplier: JAP or USA',1,0.001,
        [policy('licence',production_factory_max_efficiency_factor=0.03,foreign_influence_defense_modifier=-0.03)],
        {'treasury_change':1,'weekly_income_bn':0.001},
        'KOR pays the supplier $1bn plus $0.001bn weekly for industrial know-how. Efficiency cap +3%, influence defence -3%; no technology completion or research-year bypass.')
    add('allied_procurement_contract','USA',2,0.001,
        [policy('procurement_access',equipment_cost_multiplier_modifier=-0.04,foreign_influence_defense_modifier=-0.04)],
        {'treasury_change':2,'weekly_income_bn':0.001},
        'KOR pays $2bn and $0.001bn weekly for access and maintenance; equipment expenses -4%, influence defence -4%. Equipment transfers require separately priced native equipment contracts.')
    add('us_alliance_assurance','USA',1,0.002,
        [policy('assurance',army_core_defence_factor=0.04,army_org_factor=0.02,foreign_influence_defense_modifier=-0.06)],
        {'treasury_change':1,'weekly_income_bn':0.002},
        'KOR funds $1bn plus $0.002bn weekly alliance liaison. Core defence +4%, organization +2%, influence defence -6%. No US unit deployment is ordered by the focus.')
    add('security_partner_contacts','One chosen consenting partner: JAP or USA',1,0,
        [policy('partner',army_org_factor=0.025,bureaucracy_cost_multiplier_modifier=0.025)],
        {'treasury_change':1},'KOR pays $1bn for limited staff cooperation; organization +2.5%, bureaucracy expenses +2.5%.')
    add('japan_technology_finance','JAP',2,0.001,
        [policy('japan_contract',production_factory_max_efficiency_factor=0.04,foreign_influence_defense_modifier=-0.04)],
        {'treasury_change':2,'weekly_income_bn':0.001},
        'KOR pays $2bn plus $0.001bn weekly to Japanese technical partners; efficiency cap +4%, influence defence -4%. Claims are not settled by accepting technical cooperation.')
    add('historical_claims_dialogue','JAP',0,0,[],{},'Open a historical-claims dialogue. No automated reparations, tribunal outcome or financial benefit.',0)
    add('alternative_finance_contacts','One chosen consenting partner: USA or GER',1,0,
        [policy('capital_contacts',interest_rate_multiplier_modifier=-0.25,foreign_influence_defense_modifier=-0.025)],
        {'treasury_change':1},'KOR pays $1bn for financial access; interest-rate adjustment -0.25 points, influence defence -2.5%. No direct debt cancellation.')
    add('nordpolitik_recognition','Separate contracts with SOV and CHI',0,0,
        [policy('recognition',trade_opinion_factor=0.03,bureaucracy_cost_multiplier_modifier=0.02)],
        {'policy':{'trade_opinion_factor':0.03,'bureaucracy_cost_multiplier_modifier':0.02}},
        'Each bilateral contract yields trade opinion +3% and bureaucracy expenses +2% to both sides. SOV and CHI offers use separate signatures and cannot duplicate a partner’s bonus.')
    add('pacific_trade_contacts','JAP',1,0.001,
        [policy('pacific_contract',production_factory_max_efficiency_factor=0.025,foreign_influence_defense_modifier=-0.025)],
        {'treasury_change':1,'weekly_income_bn':0.001},
        'KOR pays $1bn plus $0.001bn weekly for technical export access; efficiency cap +2.5%, influence defence -2.5%.')
    add('revolutionary_recognition','SOV',0,0,
        [policy('revolutionary_recognition',trade_opinion_factor=0.04,foreign_influence_defense_modifier=-0.04)],
        {'policy':{'trade_opinion_factor':0.02}},
        'A revolutionary government requests recognition; no free aid or automatic Soviet alliance.')
    add('neutrality_guarantees','USA, NKO, SOV and CHI; all four must assent',0,0,[],{},
        'A negotiation framework for neutrality. No alliance withdrawal or guarantee changes until all signatories and KOR separately ratify final terms.',0)
    add('vietnam_withdrawal_settlement','SVN and USA; separate replies required',1,0,
        [policy('veterans',stability_factor=0.03,social_cost_multiplier_modifier=0.03)],
        {},'Only if a real ongoing KOR Vietnam deployment/commitment is present. KOR pays $1bn veterans’ settlement; stability +3%, weekly social expenses +3%. The current empty 1970 OOB does not establish a deployment. Otherwise bypass with no payout.')
    data['contracts']=C
    known={x['key'] for x in C}
    # A domestic coalition bargain is not a foreign treaty.
    for n in data['nodes']:
        for a in n['effects']['actions']:
            if a['type']=='offer' and a['value']=='conservative_merger':a['type']='action'
        for a in n['effects']['actions']:
            if a['type']=='offer':assert a['value'] in known,(n['id'],a)
        # Monetary commitments attached to policies are replacement slots.
        for p in n['effects']['policies']:
            p['qualified_slot']=n['group']+':'+p['slot']
            p['weekly_cost_bn']=n['effects']['weekly']
        n['reward_contract']='Domestic policy values are unilateral; separate agreement policies below activate only on accepted signature.'
    # Licence/compact dependent follow-ups remain optional endpoints on refusal;
    # common continuation has a visible resolved-response alternative. No falsely
    # licensed maintenance or joint institution is granted after refusal.
    joins={
      'defence_quality':['licensed_maintenance','changwon_production'],
      'vietnam_legacy':['burden_sharing','diverse_partners'],
      'southern_settlement':['southern_guarantees','joint_planning'],
      'korean_settlement':['confederal_secretariat','limited_trade'],
    }
    for n in data['nodes']:
        if n['key'] in joins:
            n['response_fallback']={
              'type':'visible OR eligibility route','prerequisite_groups':n['prerequisites'],
              'alternative':'A final refusal or expiry of the relevant offer, with the earlier dispatch focus completed.',
              'effect':'Only domestic completion effects; no disputed agreement bonus. Korean settlement instead becomes a unilateral policy review with +25 PP and no joint ratification.'}
        if n['key']=='vietnam_legacy':n['bypass']='No active commitment: bypass, no settlement bonus; continue the foreign tree.'
    # National diplomatic posture is available under every party; leader-specific
    # proposals do not pay a second recognition or alliance reward.
    data['anti_duplication']=[
      'One active signature per contract, recipient pair and term. Offers reached via DRP/RPR/Roh/common tree share the same contract ledger.',
      'Counterpart initiation from NKO resolves the same inter-Korean signature. Simultaneous offers lock to one pending transaction.',
      'A paid focus with an offer stages its displayed budget; where the contract itself carries the same establishment payment it is charged only once on acceptance, not on dispatch as well.',
      'Programme modifiers use owner+qualified policy slot. Completing a later level replaces that slot; it never stacks both levels.',
      'Confederal focus entry AND completion require actual COLDWAR_KOR_confederal_member spirit on both sides; founding offer precedes membership.',
      'Monthly/leadership/load sync recomputes active slot values and weekly costs only. Receipt flags protect all treasury, buildings, experience and PP.',
    ]
    data['actions']={
      'constitutional_process':{'ids':['yushin_institutions','competitive_election_guarantees','parliamentary_republic','presidential_term_limits','controlled_constitution','direct_election_settlement','restore_civil_liberties','civic_pluralism','left_pluralism'],
        'design':'Use native election_allowed/party arrays through the existing politics system, not a parallel cabinet menu. Choices set a persistent national constitutional-settlement flag. Yushin is a new 1970+ decision, never a starting fact; direct election offers no automatic incumbent win.'},
      'succession':{'ids':['managed_succession','open_succession','civilian_transition_agreement','security_transition_terms','conservative_merger'],
        'design':'Open native party/leader nomination and office transitions. No forced assassination, predetermined winner, instant outlook reset or population transfer. Conservative merger requires actual coalition/party agreement; changes eligibility and labels through reconciled party registry.'},
      'rights':{'ids':['intelligence_oversight','independent_union_law','political_prisoner_review','political_case_review','southern_ratification'],
        'design':'Persist legal settlement receipts and replace associated starting/policy spirit slots. Their concrete numerical effects are the focus policies; no hidden free bonus is promised.'},
      'contacts':{'ids':['socialist_international_contacts','nordpolitik_negotiations','inter_korean_channels','joint_ratification'],
        'design':'Reveal the listed repeatable diplomatic offer decisions (180-day failed-offer cooldown). No material reward from merely opening a list.'},
      'energy':{'ids':['energy_project_options','existing_civil_nuclear_projects','existing_energy_purchase_options'],
        'design':'Link to existing Imperia nuclear/power decisions and special projects. Existing safeguards and research conditions remain; weekly project costs use current COLDWAR_nuclear_development_budget. No free reactor, weapon, uranium deposit, raw production or mine.'},
      'workers':{'ids':['existing_guest_worker_contracts'],
        'design':'Link to current overseas-employment/guest-worker agreement flow. The starting idea and shared remittance reader remain the single source of income.'},
    }
    data['refusal_routes']={
      'policy':'Keep native AND/OR semantics explicit. Emit a final-response alternative focus for each fallback join at the same conceptual stage, with reciprocal branch to the accepted follow-up, OR-prerequisite with dispatch. Its review reward is +25 PP only; it does not satisfy treaty membership or treaty-only gates.',
      'approval_note':'The current 194-node graph uses response-condition alternatives in the inspector, not added focus cards. Before implementation choose a visible review focus or native bypass; final emitted geometry must show any added cards. Concept limit leaves 106 spare focuses.',
    }
    return data
