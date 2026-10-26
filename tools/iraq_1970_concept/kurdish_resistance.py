# IMPERIA CW — Cold War: iraq 1970 concept — kurdish resistance.
"""COLDWAR: proposed core-state insurgency; catalogue only, no runtime writes."""

def extend(nodes, decisions, rules, sources, prefix):
    bykey = {n['id'].removeprefix(prefix): n for n in nodes}
    bykey['contacts']['reward_summary'] += [
        'No Kurdish country is required for political contacts: an underground movement can be represented by crisis events and state records. Without a playable Kurdish actor, local responses are scripted; Baghdad does not choose whether its opponents accept US aid.'
    ]
    bykey['arm_front']['available'] = (
        'No limited-war policy for this crisis; organized local opposition and real unresolved northern grievances exist. '
        'If a Kurdish country exists, use its accepted aid contract. If none exists, the paid underground route is available in eligible Iraqi-controlled northern states.'
    )
    bykey['arm_front']['reward_summary'] += [
        'WITHOUT A KURDISH COUNTRY: unlock Fund the Kurdish Underground. Spend the same initial $0.25bn programme invoice and commit the same 1,000 actual infantry_weapons_1 items to one tracked clandestine cache. No payment or send_equipment targets an absent country.',
        'Begin in at most two organized, eligible northern states: enable genuine resistance against IRQ while retaining Iraqi cores; raise resistance to at least 60% once per state per crisis, never reduce a higher current value. Renewed funded support adds +25 percentage points to the native resistance TARGET for 90 days; this does not set the final target to 80%.',
        'At most one paid reinforcement pulse per 30 days adds +10 resistance points, up to 80% from this scripted pulse. A funded Iraqi security operation prevents that automatic pulse. Normal resistance, garrisons and Iraqi decisions continue to change the value.',
        'High resistance alone is not an instant liberation button. Sustained northern crisis plus the actual US intervention/military opening can start a visible 45-day uprising warning. Iraq can pay for countermeasures, negotiate, or risk a bounded Kurdish rising.'
    ]
    bykey['arm_front']['effect_body'] = (
        'Native core-state support exists: force_enable_resistance = { occupier = IRQ }; '
        'start_resistance = KUR or PUK only for that tag\'s actual core. '
        'set_resistance = 60 is a guarded one-time minimum; add_resistance_target = { id = 19709101 amount = 25 occupier = IRQ days = 90 } adds 25 points, not a hard cap. '
        'The native primitives are verified; ownership checks, local organization, invoices, cache accounting, pulse cooldowns, the scoped uprising and native-revolt coordination remain new COLDWAR integration.'
    )
    # Existing country aid and the clandestine variant are alternatives using one
    # initial-delivery marker and a shared support budget, never duplicate packages.
    for d in decisions:
        if d['id'] == prefix+'arms_offer':
            d['summary'] += ' This existing-country offer and Fund the Kurdish Underground share one initial-package consumed marker; forming a country does not unlock a second grant.'
        if d['id'] == prefix+'renew_arms':
            d['summary'] += ' Existing-country and underground support use one programme budget. At country emergence convert the remaining term and funding once; do not run both bills or both reward packages.'

    def add(key, label, unlock, summary, pp=0, days=0, actor='USA'):
        decisions.append(dict(id=('COLDWAR_IRQ_northern_'+key if actor=='IRAQ' else prefix+key),
            label=actor+' · '+label, unlock=(None if actor=='IRAQ' else prefix+unlock), group='gulf', pp=pp, days=days,
            unlock_label=('Live northern insurgency in Iraq; independent of US focus completion' if actor=='IRAQ' else None),
            actor=actor, summary=summary))
    add('underground','Fund the Kurdish Underground','arm_front',
        'Alternative use of the existing initial package: pay $0.25bn and debit 1,000 eligible actual infantry_weapons_1 items into one recorded cache. Requires no Kurdish country, real local organization/grievance, a feasible paid route and IRQ ownership/control. Begin in at most two states among 164/633/630/1078. Force-enable resistance against IRQ, bind to an appropriate local KUR/PUK core tag and seed a one-time 60% minimum. Halabja 1078 requires an actually formed PUK movement for that binding; never invent a 1970 PUK or silently add KUR cores. Preserve all cores; no country, units or territory are created at this step. Existing native resistance must be reconciled rather than overwritten.',25)
    add('sustain_underground','Sustain the Clandestine Network','arm_front',
        'Renewable 90-day contract, $0.05bn/week, prorated over actual active days. This is spent US operational funding, not a treasury gift to absent KUR or to Iraq. One native target contribution of +25 points per affected state, identified by 19709101; renewal replaces/extends that contribution, never stacks it. Optional expansion to another eligible northern state costs $0.10bn and takes 30 days of continuing funding; the initial seed can never replay in an already touched state. Reinforcement pulses: at most +10 current resistance points per 30 days, never pushing the value above 80 by that pulse; skip the pulse during an active paid Iraqi security operation. Persist seed markers and pulse cooldowns through renewal, withdrawal and government change. Native resistance growth can still exceed 80: 80 is NOT an engine cap.',0,90)
    add('security','Emergency Security Appropriation','arm_front',
        'IRAQI RESPONSE: visible when a relevant northern insurgency is active, regardless of whether USA has completed or revealed its focus. One-time preparation invoice: 2% of frozen Iraqi annual GDP. Active 90-day package: +35% army personnel cost modifier and +20% equipment upkeep modifier, additional to other valid MD war costs. A viable actual garrison/force commitment is required. After 30 funded days, reduce resistance by 15 points in each affected IRQ-owned/controlled campaign state; apply a separate -20-point resistance-target contribution for the remaining term. Block the scripted US reinforcement pulse while this operation is funded. These are extra expenses, not free garrison strength or immunity. Shares a 90-day operation cooldown with the larger operation.',0,90,'IRAQ')
    add('major_operation','Expand Northern Operations','arm_front',
        'IRAQI RESPONSE: choose instead of Emergency Security Appropriation at the start of a new 90-day operation cycle. Invoice: 4% of frozen annual GDP. One 90-day spending package: +60% army personnel cost modifier and +35% equipment upkeep modifier. A viable actual garrison/force commitment is required. After 30 funded days, reduce current resistance by 25 points in affected campaign states and apply -35 target points for the remaining term. This REPLACES the smaller package, never adds both; the shared cooldown prevents mid-cycle switching or replaying reductions. Normal garrison requirements/losses and real state-control checks remain. An operation does not guarantee a political settlement; new aid and continuing grievances can revive resistance.',0,90,'IRAQ')
    add('talks','Reopen Kurdish Negotiations','contacts',
        'IRAQI RESPONSE: may be attempted from the beginning of the northern crisis, not gated by US focus completion. Talks do not automatically succeed. An accepted, implemented regional settlement reduces current campaign resistance by 30 points, ends the associated uprising warning, and blocks renewed US exploitation of that resolved grievance. Reconstruction invoice: 2% of frozen annual GDP on acceptance. Real local budget/security powers and the cost of reduced central control are specified in the agreement; no free pacification button.',50,30,'IRAQ')
    add('withdraw_security','End the Northern Operation','arm_front',
        'IRAQI RESPONSE: end the current exceptional military-spending package and its target reduction. Preparation expenditure is sunk and the 90-day operation cooldown remains, preventing instant restart rewards. Resistance and grievances do not reset; the US network may resume pressure. A government change neither replays the resistance reduction nor erases remaining contracted bills automatically.',0,0,'IRAQ')
    add('warning','The Northern Uprising Warning','arm_front',
        'NEW SHARED CRISIS MISSION: two eligible northern states at >=80% resistance for 30 consecutive days, a supplied/organized movement, unresolved grievances and an actual US-Iraqi war or recent Iraqi military defeat open a 45-day public warning to Baghdad. No US date lock, no uprising merely because the focus exists. Falling below the two-state condition pauses the warning; 15 consecutive days below it reset the warning. A functioning accepted settlement cancels it. With no Kurdish country, local readiness is handled by scripted political actors, not an Iraqi veto. If the warning expires while all live conditions hold, a coordinated rising can establish bounded local strongholds and a Kurdish actor. Native generic resistance_90 must be integrated so it cannot fire a second, differently scoped civil war.')
    add('uprising_aftermath','Support the Northern Rising','arm_front',
        'At a genuine rising, consume the recorded clandestine cache once. Existing-country aid replaces the underground contract for its remaining term. Create only the authorized northern strongholds and finite locally organized forces; no all-core release, Kirkuk gift, foreign-core transfer or unlimited fully equipped army. If KUR/PUK already exists, support that actual actor rather than creating a duplicate. Baghdad can fight, negotiate or accept a settlement. US relief, protection and self-rule branches then respond to the actual outcome.')

    rules.update({
        'core_resistance':'Confirmed native exception: force_enable_resistance works even on an occupier core, followed by start_resistance. In a USA event use occupier = IRQ, never ROOT (= USA). start_resistance = KUR/PUK binds to an actual core country; the occupied field alone is a filter, not a tag setter. No removal of IRQ cores is necessary.',
        'pressure':'Balance proposal: one-time 60% seed in up to two organized states; +25 points of temporary resistance target and bounded monthly +10-point reinforcement pulses up to 80 from those pulses. No daily floor reset that erases Iraqi reductions. Target contributions are additive; 80 is not a native resistance cap.',
        'security_spending':'IRAQ chooses one 90-day programme: preparation 2% annual GDP with +35% army personnel/+20% equipment upkeep, or preparation 4% GDP with +60%/+35%. Larger replaces smaller. Equipment cost is the native country-wide upkeep modifier for deployed/stockpiled equipment, not procurement prices or a north-only army bill. Ordinary garrisons and other war costs still apply. All figures require balance/runtime testing.',
        'local_penalties':'Native MD already imposes major local effects at 75% resistance: controller supply and movement -50%, attrition modifier +0.30 and disabled strategic redeployment. These are existing threshold effects, not an additional invented national penalty. Actual garrison assignment/occupation-law UI on forced core resistance must be tested; funding alone never creates full garrison strength.',
        'uprising_safety':'Native MD resistance_90 can create a country, transfer all controller-held states with the same occupied_country_tag, generate fully equipped units and declare war. A dedicated COLDWAR northern outcome must coordinate with this existing hook, isolate the authorized geography, pay/consume cached aid once and prevent duplicate revolts. This is REQUIRED NEW integration, not a proven safe consequence of setting resistance to 90 or 100.',
        'cleanup':'Remove/replace only our identified resistance-target contribution on expiry or withdrawal. Retain local resistance after aid ends; it decays through native conditions/counterplay. Record whether this crisis enabled core resistance. Clear the forced override or cancel resistance only when the campaign is resolved and no other active native protest/occupation owner needs it. Do not permanently suppress resistance from another system.',
        'cache':'The initial 1,000-item cache is backed by one matching US stockpile debit; the same initial-package marker is shared with direct country aid. A valid Kurdish actor that emerges by uprising receives the remaining undelivered balance once. Peaceful emergence needs an accepted lawful handover agreement for that same remaining cache, never a new grant. A resolved/defeated movement without a valid handover writes off and clears the remaining cache with no refund or later replay. Mere US funding withdrawal stops support but does not magically recreate/destroy already committed arms; the recorded cache remains bounded until delivery, seizure/writeoff or settlement.',
        'no_country':'An underground movement needs no country to receive political support or create state resistance. Money spent on it leaves the USA treasury; no money/equipment country effect targets an absent tag. A committed equipment cache is backed by one actual stockpile debit and delivered once after a valid Kurdish actor emerges. Baghdad can counter the insurgency before any Kurdish country exists; its responses depend on the live crisis rather than US focus completion.',
    })
    sources += [dict(label='FRUS: US Kurdish assistance begun July 1972, confirmed June 1974',url='https://history.state.gov/historicaldocuments/frus1969-76v27/d254')]
    return dict(
        phase='CONCEPT ONLY; no loaded files',
        states=[dict(id=164,resistance_core_tag='KUR'),dict(id=633,resistance_core_tag='KUR'),dict(id=630,resistance_core_tag='KUR'),dict(id=1078,resistance_core_tag='PUK',requires_actual_puk_formation=True)],
        excluded_automatic_transfer=[165], seed=60, target_contribution=25, term_days=90,
        reinforcement=dict(days=30,points=10,scripted_pulse_ceiling=80,skip_if_paid_iraqi_operation=True),
        warning=dict(minimum_states=2,minimum_resistance=80,qualifying_days=30,warning_days=45,reset_after_below_condition_days=15),
        security=dict(gdp_share=.02,army_personnel_cost_multiplier_modifier=.35,equipment_cost_multiplier_modifier=.20,resistance_reduction=15,target_reduction=20,delivery_after_days=30,days=90),
        major_operation=dict(gdp_share=.04,army_personnel_cost_multiplier_modifier=.60,equipment_cost_multiplier_modifier=.35,resistance_reduction=25,target_reduction=35,delivery_after_days=30,days=90),
        native_90_coordination='Required new integration and runtime test; no native per-state hard cap claimed',
    )
