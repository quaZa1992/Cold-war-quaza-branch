"""Design-only Cyprus dossier. Does not write any HOI4 runtime directory."""
from pathlib import Path
import json
import re
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREFIX = 'COLDWAR_CYP_1970_'
nodes = []
sections = []
spirits = []

def ident(value):
    return PREFIX + value

def section(key, title, anchor, description):
    sections.append(dict(id=key, title=title, anchor=list(anchor), description=description))

def focus(key, title, sec, xy, parents=(), *, mods=None, cost=0, pp=0, stability=0,
          tension=0, settlement=0, days=35, note='', requires='', removes=(),
          event='', party=None, scope='country', duration=None, research=None):
    anchor = next(s['anchor'] for s in sections if s['id'] == sec)
    node = dict(id=ident(key), key=key, title=title, section=sec,
                x=anchor[0]+xy[0], y=anchor[1]+xy[1], local_x=xy[0], local_y=xy[1],
                prerequisite_groups=[[ident(p)] for p in parents], excludes=[],
                days=days, focus_cost=days/10, modifiers=mods or {},
                treasury_cost_gdp_percent=cost, political_power=pp,
                stability=stability, tension=tension, settlement=settlement,
                note=note, requirements=requires, removes=[ident(r) for r in removes],
                event_contract=event, party=party, party_indices=[] if party is None else [party], scope=scope,
                duration_days=duration, research=research,
                status='Design proposal; source syntax audited; not runtime tested')
    nodes.append(node)
    return node

def either(node, *parents):
    node['prerequisite_groups'] = [[ident(p) for p in parents]]
    return node

def exclusive(a,b):
    aa=next(n for n in nodes if n['key']==a)
    bb=next(n for n in nodes if n['key']==b)
    aa['excludes'].append(bb['id']); bb['excludes'].append(aa['id'])

def spirit(key,title,mods,scope='country',note=''):
    spirits.append(dict(id=ident(key),title=title,modifiers=mods,scope=scope,note=note))

# Values are balance proposals, not historical measurements.
spirit('constitutional_breakdown','A Constitution in Abeyance',
       {'stability_factor':-.10,'political_power_factor':-.12},note='Institutional breakdown since1963; not an intrinsic ethnic penalty. Negotiation and an implemented constitutional agreement can resolve it.')
spirit('divided_command','A Divided Chain of Command',
       {'army_org_factor':-.05,'max_planning':-.05},note='National Guard, police, armed organisations and foreign officers have competing loyalties.')
spirit('narrow_economy','A Narrow Island Economy',
       {'production_speed_buildings_factor':-.05},note='Small domestic market and import dependence; avoid pretending that Cyprus was economically stagnant.')
spirit('guarantor_pressure','Independence under Guarantee',
       {'foreign_influence_defense_modifier':-.10},note='Greece, Turkey and Britain constrain freedom of action; legal guarantee is not a universal defence pact.')
spirit('makarios_authority','The Archbishop-President',
       {'political_power_factor':.08,'stability_factor':.03},note='Leader-bound; removed on Makarios leaving office, dying or being overthrown. Conservative outlook is the existing game mapping, not a claim that he was Atlanticist.')
spirit('restricted_movement_south','Fragmented Markets and Unsettled Access',
       {'state_production_speed_buildings_factor':-.05},scope='state 145',note='Legacy displacement, disrupted local economic links and uneven reciprocal access, not a blanket1964-style blockade in1970. Enclaves existed across the island. Together with the national narrow-economy penalty: -10% construction before other effects.')
spirit('restricted_movement_north','Enclave Economies and Uneven Normalisation',
       {'state_production_speed_buildings_factor':-.12,'state_productivity_growth_modifier':-.15},scope='state 146',note='Coarse proxy for separate economic development, displacement and fragmented institutions, affecting all residents of the map state. Travel had substantially normalised by1969. Combined construction -17%; positive growth15% slower, not15% GDP loss. No pre-existing NCY.')
spirit('tc_parallel_administration','Turkish Cypriot Enclaves and Separate Administration',
       {'bureaucracy_cost_multiplier_modifier':.08,'police_cost_multiplier_modifier':.10},
       note='Separate communal institutions, displaced communities, uneven reciprocal access and duplicated services impose administrative/security costs. A1969 UN report records largely restored Turkish Cypriot movement outside military areas; this is not an unchanged1964 siege. Agreed services and remaining-access normalisation reduce the penalties.')
spirit('displacement_emergency','Displacement and Missing Persons',
       {'stability_factor':-.08,'social_cost_multiplier_modifier':.15},note='Contingent on violence/war; NOT a January 1970 starting spirit. Separate from existing global refugee pressure to prevent duplicate costs.')
spirit('shattered_communities','Shattered Communities',
       {'state_production_speed_buildings_factor':-.15,'state_productivity_growth_modifier':-.15},scope='affected state',note='Contingent destruction, flight and loss of trust; reconstruction can reduce this, coercion cannot simply erase it.')

section('constitution','The Republic and the Cyprus Question',(6,0),
        'Negotiation, security and constitutional outcomes. Both communities have political agency; foreign players can accept or reject proposals.')
focus('republic_at_ten','The Republic at Ten','constitution',(0,0),pp=50,
      note='Makarios governs an internationally recognised republic with a damaged bicommunal constitution. Initialise tension 55 and settlement progress 10 once.')
focus('intercommunal_talks','Keep the Intercommunal Talks Alive','constitution',(-4,1),['republic_at_ten'],tension=-5,settlement=10,cost=.5,
      note='Clerides and Denktash are negotiating counterparts. Talks began before this start date.')
focus('command_review','Review the Security Apparatus','constitution',(4,1),['republic_at_ten'],pp=25,
      note='Review competing command structures; no free battalions while starting OOB work remains deferred.')
focus('safe_passage','Consolidate Safe Civilian Passage','constitution',(-6,2),['intercommunal_talks'],cost=1,tension=-10,settlement=10,
      note='Open supervised civilian routes; halve the two starting state construction penalties after an agreed local protocol.',event='local_protocol')
focus('checkpoint_leverage','Retain Checkpoints as Leverage','constitution',(-2,2),['intercommunal_talks'],mods={'police_cost_multiplier_modifier':.05},pp=40,tension=10,
      note='Administrative leverage gives immediate political room, but movement restrictions and enclave penalties remain. Does not reward targeting civilians.')
exclusive('safe_passage','checkpoint_leverage')
focus('joint_services','Restore Shared Municipal Services','constitution',(-6,3),['safe_passage'],cost=1,settlement=10,
      mods={'bureaucracy_cost_multiplier_modifier':.05},note='Fund water and health access; remove the state145 starting penalty, reduce state146 construction penalty to -3%.')
focus('civil_rights_commission','A Bicommunal Rights Commission','constitution',(-2,4),['intercommunal_talks'],cost=.5,settlement=10,days=50,
      mods={'stability_factor':.02},note='Record abuses and safeguard access to courts; not a magic reconciliation event.')
focus('civilian_command','A Civilian Chain of Command','constitution',(2,2),['command_review'],cost=1,pp=-25,
      note='Begin removing divided-command penalties; temporary officer resistance: political_power_factor -0.05 for 180 days.',mods={'political_power_factor':-.05},duration=180)
focus('foreign_officers','Retain Mainland Officers','constitution',(6,2),['command_review'],mods={'army_org_factor':.03,'foreign_influence_defense_modifier':-.05},
      tension=5,note='Retain expertise and external dependence; remove only half the divided-command penalty. Greek officer presence does not make every Greek officer a coup participant.')
exclusive('civilian_command','foreign_officers')
focus('police_oversight','An Accountable Police Force','constitution',(2,3),['civilian_command'],cost=.5,mods={'police_cost_multiplier_modifier':-.05},
      removes=['divided_command'],note='Complete chain-of-command reform; constitutional reform remains separate.')
focus('emergency_powers','Emergency Security Powers','constitution',(6,3),['foreign_officers'],pp=40,tension=10,
      mods={'political_power_factor':.05,'police_cost_multiplier_modifier':.10},note='Government control improves, but outside influence and civilian tension remain. Powers lapse after civilian restoration.',duration=365)
focus('bicomm_constitution','Negotiate Bicommunal Safeguards','constitution',(-4,5),['civil_rights_commission'],cost=1,settlement=15,days=60,
      requires='Settlement progress >= 40; tension <= 45; no active collective-reprisals policy.',event='constitutional_offer',
      note='Requires a Turkish Cypriot negotiating acceptance; a CYP focus alone cannot decide the other community\'s rights.')
focus('unitary_constitution','Press for a Unitary Constitution','constitution',(0,5),['civil_rights_commission'],pp=50,tension=15,days=60,
      mods={'bureaucracy_cost_multiplier_modifier':-.05},event='unitary_offer',note='Majority-rule argument without automatic dissolution of the Turkish Cypriot administration. Rejection preserves deadlock and raises diplomatic pressure.')
exclusive('bicomm_constitution','unitary_constitution')
focus('federal_compromise','A Federal Compromise','constitution',(-6,6),['bicomm_constitution'],cost=1.5,days=60,
      mods={'stability_factor':.05,'bureaucracy_cost_multiplier_modifier':.08},event='federal_ratification',
      requires='Both-community ratification; settlement progress >= 60; no war; rights guarantees.',note='Explicit alternative before 1974; not claimed as the universally accepted January 1970 settlement. Replace constitutional breakdown; legitimate decentralisation carries administrative cost.')
focus('shared_republic','Restore the Shared Republic','constitution',(-2,6),['bicomm_constitution'],cost=1.5,days=60,
      mods={'stability_factor':.04,'political_power_factor':.03},event='shared_republic_ratification',
      requires='Both-community ratification; settlement progress >= 70; no war.',note='A revised 1960-style bicommunal republic: tighter veto rules and central services, slower negotiations; replace constitutional breakdown only after acceptance.')
exclusive('federal_compromise','shared_republic')
focus('constitutional_settlement','An Agreed Constitutional Settlement','constitution',(-4,7),days=50,settlement=10,
      removes=['constitutional_breakdown','restricted_movement_south','restricted_movement_north'],
      requires='Accepted settlement flag; CYP controls both states or an agreed federation has the necessary institutions.',
      note='The earlier administrative and state relief is replaced, not stacked. No annexation of state812.')
either(nodes[-1],'federal_compromise','shared_republic')
focus('ban_armed_factions','Disarm the Political Militias','constitution',(4,5),['command_review'],cost=1,pp=-25,tension=-5,days=50,
      event='militia_disarmament',note='Targets armed organisations on both sides through negotiated/local implementation; Greek mainland resistance can raise coup pressure.')
focus('tolerate_armed_factions','Tolerate Loyal Armed Networks','constitution',(8,5),['command_review'],pp=50,tension=10,
      mods={'army_org_factor':-.03,'political_power_factor':.03},note='Regime mobilisation with a lasting fragmented-command cost; can unlock a hardline coup route after its formation date.')
exclusive('ban_armed_factions','tolerate_armed_factions')
focus('reject_reprisals','Forbid Collective Reprisals','constitution',(2,7),['ban_armed_factions'],cost=.5,tension=-10,
      mods={'stability_factor':.02},note='Judicial orders and civilian protection; can be taken by any ruling party willing to obey them.')
focus('collective_reprisals','Authorise Collective Reprisals','constitution',(6,7),['tolerate_armed_factions'],pp=25,stability=-.05,tension=20,days=35,
      mods={'police_cost_multiplier_modifier':.15},event='reprisal_consequences',
      note='Explicitly depicts intimidation, unlawful detention, expulsions and killings as abuses. Adds displacement/missing-persons and affected-state damage; blocks negotiated-settlement capstones until accountability and restitution. No GDP, research, core or manpower reward.')
exclusive('reject_reprisals','collective_reprisals')
focus('crisis_conference','Convene an Emergency Conference','constitution',(2,9),days=35,cost=.5,tension=-10,event='crisis_conference',
      requires='Crisis active or tension >= 65; CYP exists.',note='Greece, Turkey, Britain and local community negotiators receive offers; any player can refuse. Available after either security course.')
either(nodes[-1],'reject_reprisals','collective_reprisals','unitary_constitution')
focus('independence_mandate','Renew the Mandate for Independence','constitution',(-2,9),['constitutional_settlement'],mods={'foreign_influence_defense_modifier':.05},days=60,
      note='Keep an independent republic. Mutually exclusive with an implemented Enosis agreement, not with merely debating one.')

section('economy','An Island Economy',(26,0),
        'Choose the structure of development: tourism or productive diversification; credit openness or domestic control. No giant free industrial base.')
focus('development_survey','Survey the Island Economy','economy',(0,0),cost=.5,pp=25)
focus('development_budget','A Funded Development Budget','economy',(0,1),['development_survey'],cost=1,mods={'bureaucracy_cost_multiplier_modifier':-.03})
focus('tourism_priority','Make Tourism the Growth Engine','economy',(-4,2),['development_budget'],cost=1.5,
      mods={'office_park_income_tax_modifier':.05,'mdcw_cw_market_exposure':.05},note='More service income, greater exposure to external demand and a crisis. No anachronistic offshore gas windfall.')
focus('productive_diversification','Diversify beyond Tourism','economy',(4,2),['development_budget'],cost=2,
      mods={'production_speed_industrial_complex_factor':.05,'production_speed_offices_factor':-.03},note='Slower service expansion in exchange for agricultural processing and light industry.')
exclusive('tourism_priority','productive_diversification')
focus('coastal_hotels','Support Coastal Hotels','economy',(-6,3),['tourism_priority'],cost=1,
      mods={'office_park_income_tax_modifier':.03},requires='No active invasion; at least one controlled coastal state.',note='A modest services modifier, not an entire free office sector.')
focus('small_business','Local Guesthouses and Suppliers','economy',(-2,3),['tourism_priority'],cost=.5,mods={'stability_factor':.02},
      note='Distribute tourism income locally. Compatible with the coastal-hotel project.')
focus('irrigation','Rural Water and Irrigation','economy',(2,3),['productive_diversification'],cost=1,research='CAT_agriculture',
      note='One 25% research bonus; no ahead-of-time reduction; the technology must exist in the local 1970 research set.')
focus('light_workshops','Food Processing and Workshops','economy',(6,3),['productive_diversification'],cost=1.5,
      mods={'industrial_capacity_factory':.03},note='Boost existing output modestly; does not create a factory if the country has none.')
focus('transport_plan','Roads between Towns and Ports','economy',(0,5),cost=1.5,
      mods={'production_speed_infrastructure_factor':.08},note='Construction bonus for funded work; not a railway project on an island whose railway closed in 1951.')
either(nodes[-1],'coastal_hotels','small_business','irrigation','light_workshops')
focus('famagusta_port','The Port of Famagusta','economy',(-4,6),['transport_plan'],cost=2,days=60,
      requires='CYP owns AND controls state146; province7193 naval base below cap; no war.',
      note='One queued naval_base level in province7193 (instant_build = no), owner rechecked on completion; native construction/upkeep still applies.')
focus('limassol_port','Develop Limassol Alternatives','economy',(0,6),['transport_plan'],cost=1.5,days=60,
      mods={'production_speed_naval_base_factor':.10},note='State145 contains Nicosia only in this coarse map. Use a national port-construction modifier; do not pretend province11984 is a verified Limassol port location.')
focus('vocational_schools','Technical and Vocational Schools','economy',(4,6),['transport_plan'],cost=1,
      mods={'research_speed_factor':.02,'education_cost_multiplier_modifier':.03},note='No university institution before its historical foundation; no additional research slot.')
focus('credit_question','The Credit Question','economy',(0,8),['transport_plan'],pp=25)
focus('foreign_capital','Invite Foreign Capital','economy',(-4,9),['credit_question'],cost=.5,
      mods={'receiving_investment_cost_modifier':-.08,'foreign_influence_defense_modifier':-.05},note='Investment efficiency is not a transfer of free cash; donors retain their own accept/refuse choice.')
focus('cooperative_credit','Strengthen Cooperative Credit','economy',(4,9),['credit_question'],cost=1,
      mods={'interest_rate_multiplier_modifier':-.15,'bureaucracy_cost_multiplier_modifier':.03},note='Interest effect is -0.15 percentage POINTS, not -15%. Cooperatives are a credible historical institution.')
exclusive('foreign_capital','cooperative_credit')
focus('transparent_accounts','Publish Public Accounts','economy',(-4,10),['foreign_capital'],cost=.5,mods={'bureaucracy_cost_multiplier_modifier':-.03})
focus('village_banks','Village Cooperative Banks','economy',(4,10),['cooperative_credit'],cost=.5,mods={'stability_factor':.02})
focus('energy_security','Electricity and Imported Fuel','economy',(0,12),cost=1.5,mods={'fuel_gain_factor':.03},
      note='Fuel-use planning and secure purchases; no free oil fields, nuclear plant or modern gas extraction.')
either(nodes[-1],'transparent_accounts','village_banks')
focus('industrial_estate','A Modest Industrial Estate','economy',(-4,13),['energy_security'],cost=3,days=60,
      mods={'production_speed_industrial_complex_factor':.05},note='Permit a construction programme; a whole factory must be paid/built through the existing economy, not granted for 3% GDP.')
focus('services_network','A Services and Shipping Network','economy',(4,13),['energy_security'],cost=2,days=60,
      mods={'office_park_income_tax_modifier':.03},note='Institutional port and services network; no free office building or automatic international tax-haven status.')
exclusive('industrial_estate','services_network')
focus('balanced_development','A Viable Island Economy','economy',(0,15),days=60,removes=['narrow_economy'],
      note='Remove the narrow-economy construction penalty after sustained development. Does not erase war damage or alter Imperia GDP/productivity by raw writes.')
either(nodes[-1],'industrial_estate','services_network')

section('military','Defending a Small Republic',(46,0),
        'A credible defensive force, external supply choices and civilian authority. Cyprus cannot win a symmetrical arms race with Turkey.')
focus('guard_review','Review the National Guard','military',(0,0),pp=25)
focus('force_structure','A Force the Island Can Sustain','military',(0,1),['guard_review'],cost=.5,pp=25)
focus('territorial_defence','Territorial Defence','military',(-4,2),['force_structure'],cost=1,
      mods={'army_defence_factor':.05,'army_attack_factor':-.03},note='Dispersed defensive preparation, limited offensive capacity.')
focus('mobile_reserve','A Small Mobile Reserve','military',(4,2),['force_structure'],cost=1.5,
      mods={'army_org_factor':.03,'supply_consumption_factor':.03},note='A more responsive reserve with a modest logistics burden; no gift tank divisions.')
exclusive('territorial_defence','mobile_reserve')
focus('village_defence','Defensive Positions and Signals','military',(-6,3),['territorial_defence'],cost=.5,mods={'dig_in_speed_factor':.08})
focus('reserve_medical','Reserve Medical Services','military',(-2,3),['territorial_defence'],cost=.5,mods={'army_org_factor':.02})
focus('transport_pool','A Shared Transport Pool','military',(2,3),['mobile_reserve'],cost=.5,research='CAT_utility_vehicles')
focus('small_arms','Standardise Small Arms','military',(6,3),['mobile_reserve'],cost=.5,research='CAT_small_arms')
focus('training_standards','Common Training Standards','military',(0,5),cost=1,mods={'training_time_army_factor':-.05})
either(nodes[-1],'village_defence','reserve_medical','transport_pool','small_arms')
focus('greek_mission','Request a Greek Training Mission','military',(-4,6),['training_standards'],event='greek_training_offer',
      mods={'army_org_factor':.03,'foreign_influence_defense_modifier':-.05},note='Benefits activate only if GRE accepts; tied to bilateral relations, not a free license or automatic alliance.')
focus('independent_procurement','Diversify Military Procurement','military',(4,6),['training_standards'],cost=1,research='CAT_towed_artillery',
      note='One 25% artillery research bonus; Soviet/Czechoslovak contacts possible without changing outlook or receiving a free production license.')
exclusive('greek_mission','independent_procurement')
focus('air_defence','Ground-Based Air Defence','military',(-4,8),days=50,cost=1,research='CAT_anti_air',
      note='No free fighter wing; imported weapons use existing purchases and depend on seller approval.')
either(nodes[-1],'greek_mission','independent_procurement')
focus('air_ambulance','Air Observation and Evacuation','military',(0,8),days=50,cost=.5,mods={'army_org_factor':.01},
      note='Liaison and casualty evacuation; no modern attack helicopter technology unlock.')
either(nodes[-1],'greek_mission','independent_procurement')
focus('coast_watch','Coast Watch and Harbour Patrols','military',(4,8),days=50,cost=.5,mods={'naval_detection':.05},
      note='Coastal observation, not a blue-water navy. Modifier must be confirmed by the audit before implementation.')
either(nodes[-1],'greek_mission','independent_procurement')
focus('civil_defence','Civil Defence without Militarising Society','military',(-4,10),['air_defence'],cost=1,mods={'stability_factor':.02},
      note='Evacuation planning and medical stocks; deliberately uses an idea because Imperia shelter buildings cost $0.008bn per level EACH WEEK.')
focus('military_preparedness','A Higher State of Readiness','military',(4,10),['coast_watch'],cost=1,
      mods={'mobilization_speed':.05,'war_support_factor':.03,'production_speed_buildings_factor':-.03},note='Military readiness diverts civilian capacity.')
exclusive('civil_defence','military_preparedness')
focus('defence_doctrine','A Defensive Doctrine for Cyprus','military',(0,12),cost=1,days=60,mods={'army_defence_factor':.03},
      note='No generic land-doctrine effect carried over without checking the MD 2.0 doctrine system.')
either(nodes[-1],'civil_defence','military_preparedness')
focus('constitutional_guard','A Guard of the Republic','military',(0,14),['defence_doctrine'],days=60,
      requires='Civilian command reform complete; no active coup regime.',mods={'army_org_factor':.02},
      note='A professional constitutional force. Does not cancel active communal violence or territorial war.')

section('diplomacy','Between the Guarantors and the Blocs',(66,0),
        'Non-alignment, patron dependence and the Sovereign Base Areas. Offers are bilateral; another player\'s acceptance is never assumed.')
focus('foreign_policy','An Independent Voice Abroad','diplomacy',(0,0),pp=25)
focus('nonaligned_contacts','Renew Non-Aligned Contacts','diplomacy',(-4,1),['foreign_policy'],cost=.5,mods={'foreign_influence_defense_modifier':.03},
      note='Contacts with Egypt, Yugoslavia and India; no automatic faction or military guarantee.')
focus('guarantor_dialogue','Consult the Three Guarantors','diplomacy',(4,1),['foreign_policy'],cost=.5,pp=25)
focus('western_association','Seek Western Economic Association','diplomacy',(-6,3),['nonaligned_contacts'],cost=.5,
      mods={'receiving_investment_cost_modifier':-.05,'mdcw_cw_market_exposure':.03},event='western_association_offer',
      note='Trade talks in a pre-EU era; no EU membership, Schengen, euro or instant NATO accession.')
focus('soviet_trade','Trade with the Socialist States','diplomacy',(-2,3),['nonaligned_contacts'],cost=.5,
      mods={'production_speed_industrial_complex_factor':.03,'foreign_influence_defense_modifier':-.03},event='eastern_trade_offer')
exclusive('western_association','soviet_trade')
focus('british_bases','The Sovereign Base Areas','diplomacy',(4,3),['guarantor_dialogue'],pp=25,
      note='State812 remains ENG. Negotiating access is separate from sovereign transfer.')
focus('base_cooperation','Negotiate Practical Base Cooperation','diplomacy',(2,4),['british_bases'],cost=.5,event='base_cooperation_offer',
      mods={'foreign_influence_defense_modifier':-.03},note='If accepted: joint emergency access and a funded local works agreement. Any payment is a real ENG treasury transfer, never manufactured income.')
focus('base_sovereignty','Campaign for Full Sovereignty','diplomacy',(6,4),['british_bases'],pp=40,event='base_sovereignty_offer',
      note='British refusal remains possible; no automatic annexation or war goal. Slow diplomatic road to negotiated transfer.')
exclusive('base_cooperation','base_sovereignty')
focus('athens_relationship','Define the Relationship with Athens','diplomacy',(-4,6),['guarantor_dialogue'],pp=25)
focus('independent_athens','Cooperate as an Independent Republic','diplomacy',(-6,7),['athens_relationship'],mods={'foreign_influence_defense_modifier':.03},
      note='Reject automatic political subordination while keeping cultural and commercial ties.')
focus('enosis_debate','Open the Enosis Question','diplomacy',(-2,7),['athens_relationship'],tension=10,event='enosis_debate',
      requires='A legal party mandate or coup outcome; no accepted permanent-independence settlement.',note='Debating union is not annexation. Community objections, Turkey and Britain are represented in the subsequent conference.')
exclusive('independent_athens','enosis_debate')
focus('ankara_channel','Keep a Channel to Ankara','diplomacy',(4,6),['guarantor_dialogue'],cost=.5,tension=-5,event='ankara_channel_offer',
      note='Talk directly and through Turkish Cypriot negotiators; Turkey is not interchangeable with the Turkish Cypriot community.')
focus('guarantee_review','A Conference on the Guarantees','diplomacy',(0,9),['ankara_channel'],cost=1,days=60,event='guarantee_conference',
      note='Revised guarantees need local assent and foreign acceptances. Unilateral withdrawal only changes CYP policy; it does not remove external claims.')
focus('enosis_agreement','Negotiate an Enosis Agreement','diplomacy',(-4,10),['enosis_debate'],days=60,cost=1,event='enosis_ratification',
      requires='GRE accepts; both communities assent through the negotiated constitutional procedure; guarantee/base arrangements agreed; no occupation.',
      note='Exceptional peaceful alternative. Final transfer ends independent CYP play: explicit irreversible outcome notice, recheck consent on resolution. Never transfer ENG bases implicitly.')
focus('un_security_council','Bring the Crisis to the United Nations','diplomacy',(4,10),['guarantee_review'],cost=.5,event='un_appeal',
      requires='Crisis, coup threat or invasion; no surrender of sovereign authority.',note='Diplomatic support and mediation, not an automatic foreign army.')

section('aftermath','Crisis, Partition and Recovery',(26,20),
        'Conditional historical crisis branch. The 1974 coup/invasion can happen, be averted or diverge; no inevitable date-triggered partition.')
focus('crisis_response','The Republic in Crisis','aftermath',(0,0),days=10,
      requires='Coup attempt, communal escalation or foreign intervention active.',note='Branch remains visible but locked before a real crisis. Set a once-only crisis instance flag.')
focus('civilian_protection','Protect Civilians and Aid Routes','aftermath',(-4,1),['crisis_response'],cost=1,tension=-5,
      note='Civilian protection reaches Greek and Turkish Cypriots; reduce damage escalation, not an instant end to war.')
focus('emergency_repression','Rule through Emergency Repression','aftermath',(4,1),['crisis_response'],pp=50,stability=-.03,tension=10,
      mods={'political_power_factor':.05,'police_cost_multiplier_modifier':.15},duration=180,
      note='Temporary regime control with repression, abuses and deepening division; no permanent stability reward.')
exclusive('civilian_protection','emergency_repression')
focus('ceasefire_lines','Negotiate Ceasefire Lines','aftermath',(-4,3),['civilian_protection'],cost=.5,event='ceasefire_offer',
      note='Controller/occupation follows actual war outcome. State146 is indivisible in this map; document this abstraction explicitly.')
focus('continue_resistance','Continue Military Resistance','aftermath',(4,3),['emergency_repression'],cost=1,mods={'army_defence_factor':.03},duration=180,
      note='State war damage persists; at war only. This is a military choice, not permission to attack civilians.')
exclusive('ceasefire_lines','continue_resistance')
focus('emergency_relief','Emergency Relief for the Displaced','aftermath',(0,5),cost=1.5,
      mods={'imp_refugee_integration_rate':.05},note='Existing integration modifier affects registered refugees only. Internal displacement uses a separate documented burden; do not inject fictional overseas refugee populations.')
either(nodes[-1],'ceasefire_lines','continue_resistance')
focus('return_and_restitution','Return and Property Restitution','aftermath',(-4,6),['emergency_relief'],cost=2,settlement=10,
      note='Reduces affected-state damage by half after protected return access. Original claims remain documented; housing grants do not extinguish them.')
focus('temporary_housing','Build Temporary Housing and Livelihoods','aftermath',(4,6),['emergency_relief'],cost=1,
      mods={'social_cost_multiplier_modifier':-.05},note='Offsets part of the new displacement-emergency spirit; does not provide extra manpower or erase the right to return.')
exclusive('return_and_restitution','temporary_housing')
focus('missing_persons','Investigate the Missing','aftermath',(0,8),cost=.5,settlement=5,
      note='Early investigations and family support can occur before 1981; a formal bicommunal CMP is date-gated to 1981 unless explicitly alternate-history.',event='missing_persons_cooperation')
either(nodes[-1],'return_and_restitution','temporary_housing')
focus('accountability','Investigate Crimes and Restore Civilian Rule','aftermath',(-4,9),['missing_persons'],cost=1,pp=-50,tension=-10,
      note='Remove repression programme; reopen settlement eligibility after accountability and restitution. Requires legal/institutional steps, not a 35-day moral reset.',days=60)
focus('frozen_partition','Administer a Frozen Conflict','aftermath',(4,9),['missing_persons'],cost=1,
      mods={'stability_factor':.02,'foreign_influence_defense_modifier':-.05},note='Remove only immediate emergency, keep displacement/property claims and affected-state penalties. NCY autonomy/recognition depends on actual negotiated/war result.')
exclusive('accountability','frozen_partition')
focus('reconstruction','Rebuild Civilian Livelihoods','aftermath',(0,11),cost=2,days=60,
      note='Remove half remaining construction damage; remove displacement-emergency only after aid/housing and an agreed durable solution. No magical repair of foreign-held states.')
either(nodes[-1],'accountability','frozen_partition')

# Six important political forces; minor ideologies retain shared country content.
from cyprus_routes import add_routes
parties = add_routes(section, focus, either, exclusive)
from cyprus_community import add_community
community_design = add_community(section, focus, either, exclusive, spirits)
from cyprus_crisis import add_crisis
crisis_design = add_crisis(section, focus, either, exclusive, spirit)
# Reflow orthogonal connectors around unrelated focus tiles. Positions are
# section-local; the preview uses the MD-style focus pitch and jogs at the
# midpoint of each prerequisite edge.
def reposition(key,x,y):
    node=next(n for n in nodes if n['key']==key)
    anchor=next(s['anchor'] for s in sections if s['id']==node['section'])
    node.update(local_x=x,local_y=y,x=anchor[0]+x,y=anchor[1]+y)
reposition('foreign_officers',10,2)
reposition('emergency_powers',10,4)
reposition('british_bases',6,3)
reposition('athens_relationship',-4,5)
reposition('ankara_channel',0,4)
reposition('soviet_trade',-2,2)
reposition('base_sovereignty',10,4)
reposition('crisis_conference',0,9)
reposition('limassol_port',0,7)
reposition('credit_question',0,9)
reposition('foreign_capital',-4,10)
reposition('cooperative_credit',4,10)
reposition('transparent_accounts',-4,11)
reposition('village_banks',4,11)
reposition('air_ambulance',0,9)
either(next(n for n in nodes if n['key']=='credit_question'),'famagusta_port','limassol_port','vocational_schools')
unilateral_resolution=next(n for n in nodes if n['key']=='tc_unilateral_resolution')
unilateral_resolution['prerequisite_groups']=[]
unilateral_resolution['requirements']='The Turkish Cypriot community has rejected negotiated constitutional terms, and the CYP government chooses unilateral pressure. Require the recorded rejection outcome; do not infer rejection from the CYP party in government.'
for key in ('tc_postwar_admin','tc_postwar_dispute'):
    node=next(n for n in nodes if n['key']==key)
    node['prerequisite_groups']=[]
    node['note']+=' Independent conditional post-partition entry: a government need not have obtained a pre-war community mandate to address an actual post-war administration.'

# Separate military posture from the treatment of civilians. A lawful government
# can resist invasion, and an abusive government must still be able to seek peace.
for name in ('ceasefire_lines','continue_resistance'):
    either(next(n for n in nodes if n['key']==name),'civilian_protection','emergency_repression')
next(n for n in nodes if n['key']=='continue_resistance')['requirements']='CYP is at war or an armed foreign intervention is active.'
next(n for n in nodes if n['key']=='temporary_housing')['note'] += ' This choice postpones, rather than forbids, restitution; the later accountability focus also contains a funded property-claims stage.'
next(n for n in nodes if n['key']=='accountability')['note'] += ' If temporary housing was chosen, add a 1% GDP property-restitution stage before settlement eligibility returns.'
next(n for n in nodes if n['key']=='mobile_reserve')['modifiers']['army_org_factor']=.02
next(n for n in nodes if n['key']=='greek_mission')['modifiers']['army_org_factor']=.02
next(n for n in nodes if n['key']=='industrial_estate')['modifiers']['production_speed_industrial_complex_factor']=.02
exclusive('independence_mandate','enosis_agreement')
for s in spirits:
    s['activation']='crisis_only' if s['id'] in (ident('displacement_emergency'),ident('shattered_communities')) else 'start'
next(n for n in nodes if n['key']=='constitutional_settlement')['requirements'] += ' No unresolved collective reprisals; accountability and restitution required if abuses occurred.'
next(n for n in nodes if n['key']=='crisis_conference')['note'] += ' Mediation remains available during abuses; only a final settlement is blocked until accountability and restitution.'
# Central handoff nodes keep OR prerequisites legible without crossing wires.
focus('training_framework','Ratify the Training Framework','military',(0,7),days=10,
      note='Domestic procurement proceeds immediately; Greek mission benefits require Greek acceptance. No duplicated conditional benefits.')
either(nodes[-1],'greek_mission','independent_procurement')
for name in ('air_defence','air_ambulance','coast_watch'):
    next(n for n in nodes if n['key']==name)['prerequisite_groups']=[[ident('training_framework')]]
focus('crisis_council','Convene the Emergency Council','aftermath',(0,2),days=10,
      note='Military posture is independent of civilian-protection policy. Either initial response can lead to a ceasefire or continued defence.')
either(nodes[-1],'civilian_protection','emergency_repression')
for name in ('ceasefire_lines','continue_resistance'):
    next(n for n in nodes if n['key']==name)['prerequisite_groups']=[[ident('crisis_council')]]
# Credit a political reform milestone once globally, rather than repeatedly on
# every change of government. Shared negotiated progress is separate.
for n in nodes:
    n['settlement_credit_target']=0
    if n['party'] is not None and n['settlement']>0:
        n['settlement_credit_target']=n['settlement']
        n['settlement']=0
        n['note'] += ' Reform credit is a shared milestone ceiling, not additive: only the increase above the highest previously credited party milestone applies (maximum10 across all major-party routes).'

sources=[
 {'id':'MD_GENERIC','path':'E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/00_generic.txt','use':'Layout, focus fields, costs, mutual exclusion and economic helper idioms.'},
 {'id':'MD_RUSSIA','path':'E:/SteamLibrary/steamapps/workshop/content/394360/2777392649/common/national_focus/05_russia.txt','use':'Separate political islands, shortcuts, leader paths and mixed political/economic rewards.'},
 {'id':'LOCAL_GENERIC','path':'common/national_focus/mdcw_1970_generic_focus.txt','use':'Compatible 1970 party gates, categories and rewards.'},
 {'id':'PARTY_GATES','path':'common/scripted_triggers/01_political_triggers.txt:1','use':'Exact 0-23 ruling_party index mapping.'},
 {'id':'PROGRAMMES','path':'common/dynamic_modifiers/mdcw_1970_generic_party_programmes.txt:1','use':'Active-party-only dynamic programmes; no party-switch stacking.'},
 {'id':'IMPERIA_UPKEEP','path':'common/scripted_effects/mdcw_imperia_infrastructure_effects.txt:29','use':'Real weekly upkeep; avoid casually granting costly infrastructure.'},
 {'id':'IMPERIA_REFUGEES','path':'common/scripted_effects/imp_refugees_effects.txt:252','use':'Registered refugee cost and integration system; not a safe generic setter for internal displacement.'},
 {'id':'CYP_HISTORY','path':'history/countries/CYP - Cyprus.txt:4','use':'Makarios and the current 1970 scenario profile.'},
 {'id':'IPU_1970','url':'https://data.ipu.org/election-summary/PDF/CYPRUS_1970_E.PDF','use':'Historical 1970 parties, electoral institutions and unfilled Turkish-community parliamentary seats.'},
 {'id':'FRUS_1970','url':'https://history.state.gov/historicaldocuments/frus1969-76v29/d355','use':'Contemporary assessment of Makarios, Clerides and the March 1970 crisis.'},
 {'id':'FRUS_CONTINGENCIES','url':'https://history.state.gov/historicaldocuments/frus1969-76v30/d75','use':'Distinct crisis possibilities: talks, communal conflict, coup, mainland intervention and partition. Source is a contemporary US assessment, not neutral proof of every allegation.'},
 {'id':'NAM','url':'https://www.nam.ac.uk/explore/cyprus','use':'1960 independence, British bases, 1963-64 violence, 1974 Greek-junta-backed coup and Turkish invasion.'},
 {'id':'CMP','url':'https://www.cmp-cyprus.org/origins/','use':'A formal bicommunal Committee on Missing Persons dates from 1981; earlier investigations must have another name.'},
 {'id':'UNHCR','url':'https://www.unhcr.org/publications/report-united-nations-high-commissioner-refugees-4','use':'Relief for displaced Greek and Turkish Cypriots following 1974.'},
 {'id':'AKEL','url':'https://akel.org.cy/the-memory-of-ezekias-papaioannou-was-honored/?lang=en','use':'Historical AKEL leadership; partisan commemorative source, not sole evidence for its political programme.'},
 {'id':'IPU_1976','url':'https://data.ipu.org/election-summary/PDF/CYPRUS_1976_E.PDF','use':'The later party landscape is distinct from1970; new centre/right formations and Kyprianou in1976.'},
 {'id':'CY_PARLIAMENT','url':'https://www.parliament.cy/easyconsole.cfm/id/142','use':'Official constitutional/electoral chronology, including delayed1970 elections and the next poll in1976.'},
 {'id':'UNFICYP_ACCESS','url':'https://unficyp.unmissions.org/en/supervision-cease-fire','use':'Official account of civilian movement, economic restrictions, enclave defences and reciprocal normalisation efforts. Sources support historical context; the proposed spirit values are balance design.'},
 {'id':'CTP_FOUNDER','url':'https://cumhuriyetciturkpartisi.org/4-nisan-2020-ctpnin-kurucu-genel-baskani-ahmet-mithat-berberoglu-aniliyor/','use':'Party biography dates CTP formation to27December1970 and identifies founding leader Ahmet Mithat Berberoglu. Used for identity/date, not as neutral evidence of all party claims.'},
 {'id':'TURKISH_ARCHIVE_1974','url':'https://www5.tbmm.gov.tr/tutanaklar/TUTANAK/GZC/d13/c013/b003/gcz130130030019.pdf','use':'Original TBMM secret sitting20July1974, printedp19: Ecevit announces the operation and its stated purposes. Evidence of the contemporary Turkish position, not independent validation of every justification.'},
 {'id':'UN_1969_NORMALISATION','url':'https://digitallibrary.un.org/record/504435','use':'S/9521,3December1969, para54: uneven normalisation and access. Historian used indexed French text; direct scans returned403. See WAR_HISTORY.md for precise source-access limits.'},
 {'id':'FRUS_1970_UNDERGROUND','url':'https://history.state.gov/historicaldocuments/frus1969-76v29/d353','use':'Contemporary18March1970 assessment of the helicopter attack, NationalFront, Georkadjis and uncertainty over responsibility; do not attribute it anachronistically to EOKAB.'},
]

def reward_code(n):
    lines=[]
    if n.get('execution_mode')=='event_milestone':
        lines += ['# FAST CRISIS MILESTONE: actor event owns this payload, guarded once per crisis instance.',
                  '# The event records the focus with complete_national_focus after applying the outcome.',
                  '# Focus completion must not repay, redispatch or reapply the payload.']
    if n['treasury_cost_gdp_percent']:
        if n.get('cost_project_slot'):
            lines.append('# Pay only if the shared project slot has not been funded: '+n['cost_project_slot'])
        lines += ['# COUNTRY scope. Project administration/grant cost; NOT payment for a whole factory.',
                  'set_temp_variable = { treasury_change = gdp_total }',
                  f'multiply_temp_variable = {{ treasury_change = {-n["treasury_cost_gdp_percent"]/100:g} }}',
                  'modify_treasury_effect = yes']
    if n['event_contract'] and n['event_contract'] not in ('reprisal_consequences','enosis_debate','turkish_crisis_response'):
        lines.append('# OUTCOME PAYLOAD below: run once in the accepted/result event, NOT in the focus reward on sending the offer.')
    if n['political_power']: lines.append(f'add_political_power = {n["political_power"]}')
    if n['stability']: lines.append(f'add_stability = {n["stability"]:g}')
    for variable in ('tension','settlement'):
        if n[variable]:
            key=ident('communal_tension' if variable=='tension' else 'settlement_progress')
            lines += [f'add_to_variable = {{ {key} = {n[variable]:g} }}',
                      f'clamp_variable = {{ var = {key} min = 0 max = 100 }}']
    if n.get('coup_pressure_delta'):
        lines += [f'add_to_variable = {{ {ident("coup_pressure")} = {n["coup_pressure_delta"]:g} }}',
                  f'clamp_variable = {{ var = {ident("coup_pressure")} min = 0 max = 100 }}']
    if n['settlement_credit_target']:
        credit=ident('party_reform_credit'); target=n['settlement_credit_target']
        progress=ident('settlement_progress')
        lines += ['# Shared highest-milestone ledger prevents party-switch reform shopping.',
                  'if = {', f'\tlimit = {{ check_variable = {{ {credit} < {target} }} }}',
                  f'\tset_temp_variable = {{ COLDWAR_CYP_1970_credit_delta = {target} }}',
                  f'\tsubtract_from_temp_variable = {{ COLDWAR_CYP_1970_credit_delta = {credit} }}',
                  f'\tadd_to_variable = {{ {progress} = COLDWAR_CYP_1970_credit_delta }}',
                  f'\tset_variable = {{ {credit} = {target} }}',
                  f'\tclamp_variable = {{ var = {progress} min = 0 max = 100 }}','}']
    if n['research']:
        lines += ['add_tech_bonus = {',f'\tname = {n["id"]}_research_bonus',
                  '\tbonus = 0.25','\tuses = 1',f'\tcategory = {n["research"]}','}']
    if n['modifiers']:
        if n['event_contract']:
            lines.append('# Apply these benefits ONLY in the acceptance/outcome event; not on sending the offer.')
        elif n['party'] is not None:
            for k,v in n['modifiers'].items():
                lines.append(f'add_to_variable = {{ {ident("p"+str(n["party"])+"_"+k)} = {v:g} }}')
            lines += [f'add_dynamic_modifier = {{ modifier = {ident("p"+str(n["party"])+"_programme")} }}',
                      'force_update_dynamic_modifier = yes']
        else:
            if n['duration_days']:
                lines.append(f'add_timed_idea = {{ idea = {n["id"]}_idea days = {n["duration_days"]} }}')
            else: lines.append(f'add_ideas = {n["id"]}_idea')
        lines.append('# Proposed modifier definition; new COLDWAR idea/programme, real modifier keys:')
        for k,v in n['modifiers'].items(): lines.append(f'#\t{k} = {v:g}')
    if n['removes']:
        lines.append('# Conditional removal/replacement only after the outcome contract succeeds:')
        for key in n['removes']: lines.append('#\t'+key)
    if n['event_contract']:
        lines.append(f'# NEW event contract, not an existing scripted effect: {n["event_contract"]}')
    for change in n.get('spirit_changes',[]):
        lines.append('# Staged outcome '+change['operation']+': '+change['id'])
        for key,value in change.get('modifiers_after',{}).items():lines.append(f'#\t{key} = {value:g}')
    if n.get('sunset_on'):lines.append('# Restriction policy expires on: '+n['sunset_on'])
    if not lines: lines.append('# Unlock the next focus / register the mandate once; no invented passive reward.')
    return '\n'.join(lines)

def readable_prose(value):
    value=re.sub(r'(?<=[A-Za-z])(?=\d)|(?<=\d)(?=[A-Z])',' ',value)
    return value.replace('NationalFront','National Front').replace('EOKAB','EOKA B')

for s in spirits:
    s['note']=readable_prose(s['note'])
for n in nodes:
    for field in ('title','note','requirements'):
        n[field]=readable_prose(n[field])
    n['reward_code']=reward_code(n)
    party_gate=''
    if n['party'] is not None:
        indices=n['party_indices']
        party_gate='has_variable = ruling_party\n'
        if len(indices)>1:party_gate+='OR = { '+' '.join(f'check_variable = {{ ruling_party = {index} }}' for index in indices)+' }\n'
        else:party_gate+=f'check_variable = {{ ruling_party = {n["party"]} }}\n'
    n['available_code']=(f'original_tag = CYP\nIMP_is_1970_scenario = yes\n'+party_gate
        + ('# Additional outcome/formation conditions described in requirements must also be implemented.\n' if n['requirements'] else ''))
    if n['key'] in ('bicomm_constitution','federal_compromise','shared_republic','constitutional_settlement'):
        n['available_code'] += f'NOT = {{ has_country_flag = {ident("unresolved_reprisals")} }}\n'
    if n['key'] in ('federal_compromise','shared_republic','constitutional_settlement'):
        n['available_code'] += f'has_country_flag = {ident("tc_community_assent")}\n'
    if n['key']=='tc_ctp':
        n['available_code'] += f'date > 1970.12.26\nhas_country_flag = {ident("ctp_formed")}\n'
    if n['key'] in ('tc_postwar_admin','tc_postwar_dispute'):
        n['available_code'] += f'has_country_flag = {ident("actual_partition")}\n'
    if n['key']=='tc_unilateral_resolution':
        n['available_code'] += f'has_country_flag = {ident("tc_terms_rejected")}\nNOT = {{ has_country_flag = {ident("final_settlement_implemented")} }}\n'
    if n['key']=='war_guarantors':
        n['available_code'] += f'OR = {{ has_country_flag = {ident("coup_regime_active")} has_country_flag = {ident("unilateral_enosis")} has_country_flag = {ident("grave_renewed_communal_violence")} }}\n'
    if n['key']=='war_july_ceasefire':
        n['available_code'] += f'has_country_flag = {ident("first_intervention_phase")}\n'
    if n['key']=='war_august':
        n['available_code'] += f'has_country_flag = {ident("geneva_failed")}\nNOT = {{ has_country_flag = {ident("final_settlement_implemented")} }}\n'
    if n['key']=='constitutional_guard':
        n['available_code'] += f'has_completed_focus = {ident("police_oversight")}\nNOT = {{ has_country_flag = {ident("coup_regime_active")} }}\n'
    if n['key']=='enosis_agreement':
        n['available_code'] += f'has_country_flag = {ident("enosis_all_consents")}\nNOT = {{ has_country_flag = {ident("independence_settled")} }}\n'
    if n['key']=='independence_mandate':
        n['available_code'] += f'NOT = {{ has_country_flag = {ident("enosis_implemented")} }}\n'

contracts={
 'local_protocol':'A CYP offer begins a local/community negotiation; acceptance halves named initial movement penalties. Refusal leaves them. Never treat TUR assent as a substitute for Turkish Cypriot assent.',
 'constitutional_offer':'Evaluate settlement progress, tension, both communities and their political representatives. Accepted offers unlock ratification, rejected offers preserve the current institutional penalties. One active conference instance only.',
 'unitary_offer':'Community representatives can refuse. No unilateral removal of constitutional breakdown. Failure adds 5 tension, not an automatic Turkish declaration of war.',
 'federal_ratification':'A dated or counterfactual federal compact requires consent from both communities; replace the old starting spirit with the agreed administrative programme. No transfer of state812.',
 'shared_republic_ratification':'A revised 1960-style central republic requires stronger settlement progress and both-community ratification; one settlement result flag, mutually exclusive with federation.',
 'militia_disarmament':'Supervised disarmament is negotiated across armed groups, not a blanket ethnic purge. Greek/other patrons may accept withdrawal or add coup pressure. No arbitrary free manpower.',
 'reprisal_consequences':'Abstract intimidation, killing, detention and forced displacement without operational detail. The focus applies tension+20 ONCE; the event adds displaced/missing-persons burden, affected-state destruction and the settlement block, without another tension debit. No population, GDP, core or military reward. Record perpetrating faction; apply the same harm rules to armed actors in either community.',
 'crisis_conference':'Offers to GRE/TUR/ENG plus local representatives. AI weighs actual regime, tension, claims and guarantees; human players decide. Refusal cannot force another player\'s action.',
 'turkish_crisis_response':'When a junta-backed coup succeeds, TUR chooses diplomatic ultimatum, bounded intervention or broader invasion; GRE chooses support/withdrawal/escalation; ENG chooses mediation/base defence; no forced player choices.',
 'ceasefire_offer':'All belligerents must accept a ceasefire; war control is retained until a settlement. NCY administration can emerge conditionally after intervention; recognition is a later separate question, with the 1983 declaration not misdated to 1974.',
 'enosis_debate':'Open a diplomatic/political dispute without annexation. A hardline majority mandate does not imply Turkish Cypriot consent. Peaceful Enosis needs a separate ratification chain; unilateral Enosis increases crisis risk.',
 'enosis_ratification':'Recheck GRE/CYP and both-community assent, guarantees, war state and ownership on resolution. State145/146 transfer only under agreed terms. Warn that independent CYP play ends; state812 stays ENG without separate British assent. Block permanent-independence capstone reciprocally.',
 'base_cooperation_offer':'ENG can accept/refuse; only accepted projects enable modifiers. A proposed subsidy must debit the donor and credit CYP with the same amount, checked against funds. Cooperation is not sovereignty transfer.',
 'base_sovereignty_offer':'Negotiated transfer of state812 requires explicit ENG acceptance and local settlement safeguards. British refusal gives no free annexation or automatic casus belli.',
 'guarantee_conference':'Greece, Turkey and Britain each retain a response; local community consent matters separately. Revise only the guarantees to which the parties actually agree.',
 'missing_persons_cooperation':'A civilian investigation/family-support initiative can begin early. The historical bicommunal CMP is 1981-gated, or deliberately marked early alternate institution; cooperation does not erase crimes.',
 'generic_bilateral_offer':'Used by Greek training, Western/Eastern trade, technical agreements, patronage and crown offers. On focus completion send an offer; apply conditional benefits only after acceptance. No recurring free money, no automatic faction, license or guarantee. Timeout90 days returns no benefits; one accepted agreement per policy slot.',
}
for name in sorted({n['event_contract'] for n in nodes if n['event_contract']}):
    if name not in contracts: contracts[name]=contracts['generic_bilateral_offer']
for name in [x for x in contracts if x.startswith('tc_')]:
    contracts[name]='Turkish Cypriot counterpart contract: '+contracts['generic_bilateral_offer']+' A local community mandate is independent of CYP ruling_party and Ankara. Küçük/Denktas or elected community representatives may refuse; Cyprus may not select an obedient delegate. No NCY release at the1970 start.'
for name in ('tc_access_protocol','local_protocol'):
    contracts[name]='On implemented protected civilian access, replace initial movement/friction penalties with the single agreed access stage: state145 construction -2.5%, state146 construction -6% and positive growth -7.5%, country bureaucracy +4% and police +5%. Use a shared highest-relief stage ledger; never halve repeatedly, double-count the same project or reapply a worse stage later. Refusal leaves starting penalties.'
for name in ('tc_joint_services_offer','tc_local_services_offer'):
    contracts[name]='An accepted and implemented access/services compact removes BOTH initial state-access modifiers and the national enclave-administration spirit. Replace with ONE agreed programme: joint services stability +4%, bureaucracy +3%; local services stability +3%, bureaucracy +6%. In a hardline government this agreement must explicitly reopen civilian access. No duplicate budgets, conflicting stages or automatic removal of constitutional deadlock/war damage.'
contracts['tc_community_mandate']='The independently represented Turkish Cypriot community resolves its own negotiating mandate. Mere completion of a CYP focus cannot set assent; historical actors may reject proposed constitutional terms. Do not equate Turkish government acceptance with Turkish Cypriot assent.'
contracts['tc_community_mandate']+=' An actual rejected communal proposal records the NEW tc_terms_rejected flag for the current negotiation instance; it is not a universal ethnic-hostility flag. Reset before a new proposal, clear after an accepted/implemented compact, and reject stale replies. This rejected-outcome flag can unlock the independent unilateral-pressure focus; no free coercive reward is generated by merely sending an offer.'
for name in ('tc_federal_assent','tc_republic_assent'):
    contracts[name]='On independently accepted terms and implemented access/security safeguards, set COLDWAR_CYP_1970_tc_community_assent once with the agreed constitutional model and clear the current tc_terms_rejected marker. A rejected offer sets no assent flag and cannot unlock final shared constitutional ratification; instead it records the actual rejection for this negotiation instance. Final settlement also requires Greek Cypriot approval and applicable guarantees.'
contracts['tc_ctp_dialogue']='CTP formation only from27December1970, led by Ahmet Mithat Berberoglu. The CTP decides whether to join negotiations; Cyprus cannot create a government-controlled Turkish Cypriot party or assume its leadership speaks for every Turkish Cypriot.'
for name in ('social_development_loan','eastern_equipment_credit','mainland_emergency_loan','nonaligned_credit_offer'):
    contracts[name]='A real loan must debit a consenting lender, credit CYP through modify_treasury_effect and create equal debt through modify_debt_effect, with credit/repayment terms and amount checked at resolution. Listed efficiency/dependence modifiers apply only after acceptance; no free cash or debt-free loan. Domestic-funded alternatives create no fictitious loan.'
for name in [x for x in contracts if x.startswith('war_')]:
    contracts[name]='Research-led crisis outcome, defined in WAR_HISTORY.md and WAR_MECHANICS.md. Resolve once per crisis instance with actual actor choices, dated/conditional milestones and separate coup/communal tracks. Historical AI is conditional, not a compulsory war timer. Reactive responses use the crisis event clock, then record the milestone focus once with complete_national_focus; costs/effects have one guarded owner. New event implementation is required; this is not an existing MD helper.'
contracts['war_coup_resolution']='A prepared Greek-junta-backed plot may succeed, fail or meet effective constitutional resistance. Historical timing15July1974 only if the sponsor, unresolved command dispute and armed network survive. Successful coup can install Sampson and enable the combined21/22 route. Neither arbitrary presidential murder nor war/partition is automatic.'
contracts['war_turkish_intervention_choice']='Turkey independently chooses continued diplomacy, ultimatum or actual military intervention after defined grounds. Use existing create_wargoal/declare_war_on only in a deliberate sovereign decision, after military readiness. All current1970 OOBs are deliberately deferred; do not hide that with modern unit spawns.'
contracts['war_july_ceasefire']='Chosen current-map version: abstract the limited July20 foothold and July22 ceasefire/conference phase without starting a fake engine war or transferring all state146. Show the abstraction explicitly. If actual engine combat is used in a later map/OOB version, it requires a tested ownership-preserving ceasefire adapter: generic MD CPD ceasefire transfers territory and its whitepeace adds720-day truce, both wrong here. A flag alone never stops engine fighting.'
contracts['war_geneva_negotiation']='FirstGeneva arrangements30July and secondconference8–14August are distinct phases. Terms and requested guarantees go to their real counterpart players. Accepted and implemented terms stop escalation; refusal/deadline failure allows a new Turkish decision, not a mandatory war.'
contracts['war_second_phase_combat']='Second offensive14–16August is conditional on failed settlement and an actual renewed-combat decision. The chosen current-map design explicitly abstracts the July phase; a later real engine offensive requires initialized historical forces and actual readiness. Territory follows battles or accepted settlement terms. No automatic transfer/NCY release or fixed future sovereignty.'

meta=dict(title='Cold War Cyprus — January 1970 Focus Tree Design',prefix=PREFIX,
          stage='DESIGN ONLY — no runtime files changed',language='English',
          counts=dict(focuses=len(nodes),party_routes=len(parties),mutually_exclusive_pairs=sum(len(n['excludes']) for n in nodes)//2),
          source_md='User-supplied installed MD snapshot; no claim of online version currency.',
          starting_variables={ident('communal_tension'):55,ident('settlement_progress'):10,ident('party_reform_credit'):0,ident('coup_pressure'):45},
          variable_note='NEW bounded scenario variables, not existing MD features. Values are tuning proposals, not historical statistics.',
          focus_timing='cost is days/10; 35/50/60 days. MD generic reference often uses cost8.6. Cyprus pacing remains to be playtested.',
          progression='Shared sector roots are parallel from start; party routes require the specific governing subparty, formation and date conditions. Completed one-time focuses never reset on elections.',
          layout='Shared roots x6/26/46/66; Turkish Cypriot community root x86; six political/economic roots x114/136/158/180/202/224. The research-led road-to-war root sits x6,y14; recovery x26,y20. All sections share one MD coordinate space.',
          caps='Small-country balance targets: combined shared + ONE active political/economic programme research <=10%, organisation <=18%, generic+specific construction <=25%, office tax income <=35%. These are authored reward ceilings, not GDP increases. No free research slots or whole industrial sectors; strong modifiers remain constrained by actual capacity/workforce and political tradeoffs.',
          economy='Costs use GDP-scaled modify_treasury_effect. Costs below are project grants/administration, not an assertion that 3%GDP purchases a factory. Construction queues and upkeep remain payable. Require funds on start AND completion; apply atomic debit/reward, or cancel with no reward. No double charging internal helpers.',
          history='States145+146 are CYP in1970; state812 is ENG. The two-province MD map cannot represent the distribution of pre-1974 enclaves. Do not use resistance/compliance as a fake communal mechanic in core territory.',
          party_lifecycle='Exact governing subparty gate, never just outlook. Six major routes: indices1,2,3,4,20 and combined21/22. Minor parties retain the shared national economy/military/diplomacy/community content. Persistent reveal preserves history; only the current government\'s political AND economic programme is enabled, avoiding election stacking. Shared funded projects and historical consequences persist. A global highest-milestone ledger caps all party reform credit at10; do not reset on elections.',
          crisis='Historical mode favours the conditional1970-74 chain; successful talks/reform can avert it. EOKAB from1971, Grivas death1974, DIKO/DISY from1976, Makarios death1977 and CMP1981 need dated or explicitly alternate outcomes. Full chronology/portraits need implementation verification.',
          cumulative_status='Numeric design audited statically against local keys. No engine run or multiplayer balance claim.')
data=dict(meta=meta,sections=sections,parties=parties,starting_spirits=spirits,community_design=community_design,crisis_design=crisis_design,
          focuses=nodes,event_contracts=contracts,sources=sources)

def validate():
    ids={n['id'] for n in nodes}
    assert len(ids)==len(nodes)
    assert sorted(p['index'] for p in parties)==[1,2,3,4,20,22]
    occupied={}
    for n in nodes:
        assert n['id'].startswith(PREFIX)
        cell=(n['x'],n['y'])
        assert cell not in occupied,(cell,n['id'],occupied.get(cell))
        occupied[cell]=n['id']
        for group in n['prerequisite_groups']:
            assert group
            for p in group:
                assert p in ids and p!=n['id']
                assert next(k['y'] for k in nodes if k['id']==p)<n['y']
        for e in n['excludes']:
            assert e in ids and n['id'] in next(k['excludes'] for k in nodes if k['id']==e)
        assert n['reward_code'] and n['days']>0
        if n['party'] is not None: assert f'ruling_party = {n["party"]}' in n['available_code']
    return dict(focuses=len(nodes),unique_ids=True,unique_coordinates=True,
                acyclic_prerequisites=True,reciprocal_exclusions=True,
                important_party_routes=len(parties),party_focuses=sum(n['party'] is not None for n in nodes),
                turkish_cypriot_focuses=sum(n['section']=='turkish_cypriots' for n in nodes),
                road_to_war_focuses=sum(n['section']=='road_to_war' for n in nodes),
                starting_spirits=sum(s['activation']=='start' for s in spirits),event_contracts=len(contracts))

def write_dossier():
    lines=['# Cold War Cyprus: January 1970 design','',
           '**Design only.** All game-facing names and descriptions are English. No focus, idea, state history or event has been installed. All new identifiers use `COLDWAR_CYP_1970_`.', '',
           f'{len(nodes)} proposed focuses; six important political routes with24 focuses each, including14 bespoke economic focuses per route; {meta["counts"]["mutually_exclusive_pairs"]} reciprocal exclusive pairs. Dedicated39-focus Turkish Cypriot section plus a research-led road-to-war section. A playthrough completes a fraction of the full tree.', '',
           '## How the1974 war can emerge','',
           'Read WAR_HISTORY.md for the sourced chronology and Turkish archival evidence, and WAR_MECHANICS.md for actual reusable MD APIs and limitations. The design separates the1963legacy, uneven normalisation by1970, the armedNationalFront,1971EOKAB, Greekmilitary influence, a conditional1974coup, Turkishintervention, Julyceasefire, Geneva and a possibleAugustoffensive. Active movement restrictions are an optional renewed policy, not a false assertion that every1964restriction persisted in1970. A hostile ethnic population is not the war trigger.', '',
           '## Historical starting point','',
           'Makarios III is president. Local history maps him to conservatism/index1, while his diplomacy remains non-aligned. The current country profile is a generic world template, not a researched Cypriot party distribution; replace it with sourced setup during implementation. Do not equate parliamentary seats with presidential popularity or outlook support.', '',
           'The legacy of the 1963–64 constitutional breakdown, displacement, separate administrations and armed enclaves is present. Movement had substantially normalised by1969; remaining uneven reciprocal access must be distinguished from optional renewed restrictions. Both state145 and state146 belong to CYP in1970; state812 is British. A pre-existing sovereign Northern Cyprus would be an error. The later coup, Turkish invasion, civilian killings, expulsions, missing persons and partition must be conditional events with clear responsibility. Violence by armed actors from either community has the same lasting harm rules.', '',
           'Historical facts and proposed ideological mappings are distinguished below. The conservative game slot does not prove Makarios was pro-Western; a historical party assigned to an engine category does not inherit every regime associated with that category.', '',
           '## Starting spirits and conditional crisis burdens','',
           '| Proposed spirit | Scope | Exact proposed modifiers | Interpretation |','|---|---|---|---|']
    for s in spirits:
        lines.append(f'| {s["title"]} | {s["scope"]} | '+', '.join(f'`{k} = {v:g}`' for k,v in s['modifiers'].items())+f' | {s["note"]} |')
    lines += ['', '## Military phase and crisis timing','',crisis_design['selected_phase_model'],'',crisis_design['reaction_clock'],'',crisis_design['payload_rule'],'', '## Design contracts and lifecycle','']
    for field in ('variable_note','progression','layout','caps','economy','party_lifecycle','crisis','cumulative_status'):
        lines += [f'**{field.replace("_"," ").capitalize()}:** {meta[field]}','']
    lines += ['## Outlooks, parties and leaders','',
              'Six relevant routes replace the earlier24 miniature party trees: Makarios, Clerides/Eniaion, EDEK, AKEL, the Progressive Front and the combined armed-Enosis/coup milieu. Each now contains ten political and14 bespoke economic focuses with four internal choice pairs. Party indices21/22 share the hardline coup route; all other minors retain shared national content. Turkish Cypriot political agency is a separate community counterpart, not an invented Islamist party or a sovereign NCY at the start.', '',
              '| Index | Outlook / subideology | Programme | Leader / status | Formation |','|---|---|---|---|---|']
    for p in parties:
        lines.append(f'| {p["index"]} | {p["outlook"]} / `{p["ideology"]}` | {p["title"]} | {p["leader"]} {p["status"]}. | {p["formation"]} |')
    lines += ['', '## Focus register','',
              'Coordinates are resolved absolute positions for review. Implementation uses an absolute section root and local offsets via `relative_position_id`. Each row is a separate focus; comma-separated prerequisites within brackets mean OR, separate brackets mean AND. Modifier values are signed engine values, not an informal balance rating. Effects are proposed; the underlying modifier names and helper syntax are verified against the repository.', '']
    for s in sections:
        lines += [f'### {s["title"]}', '',s['description'],'',
                  '| Focus / ID suffix | Position; days | Prerequisites / excludes | Effects and costs | Requirements and consequence |',
                  '|---|---|---|---|---|']
        for n in [n for n in nodes if n['section']==s['id']]:
            effects=[f'{k}={v:+g}' for k,v in n['modifiers'].items()]
            if n['treasury_cost_gdp_percent']: effects.append(f'cost {n["treasury_cost_gdp_percent"]:g}% GDP')
            for k in ('political_power','stability','tension','settlement'):
                if n[k]: effects.append(f'{k} {n[k]:+g}')
            if n['settlement_credit_target']: effects.append(f'global party-reform credit ceiling {n["settlement_credit_target"]}/10; only uncredited difference applies')
            if n.get('coup_pressure_delta'):effects.append(f'coup pressure {n["coup_pressure_delta"]:+g}')
            for change in n.get('spirit_changes',[]):
                effects.append(change['operation']+' '+change['id']+' '+str(change.get('modifiers_after',{})))
            if n['research']: effects.append(f'1x25% {n["research"]} research; no ahead-of-time reduction')
            if n['duration_days']: effects.append(f'modifier duration {n["duration_days"]} days')
            if n['removes']: effects.append('conditional replacement: '+', '.join(n['removes']))
            pre=' AND '.join('['+' OR '.join(x.replace(PREFIX,'') for x in g)+']' for g in n['prerequisite_groups']) or 'Root'
            if n['excludes']: pre+='; X '+', '.join(x.replace(PREFIX,'') for x in n['excludes'])
            effects='; '.join(effects) or 'Unlock / event progression'
            extra=n['requirements']+' '+n['note']
            if n['event_contract']: extra+=' Contract: '+n['event_contract']+'.'
            lines.append(f'| {n["title"]}<br>`{n["key"]}` | ({n["x"]},{n["y"]}); {n["days"]}d | {pre} | {effects} | {extra} |')
    lines += ['', '## Event contracts: must exist before runtime implementation','']
    for k,v in contracts.items(): lines += [f'- **{k}:** {v}']
    lines += ['', '## Implementation order and acceptance checks','',
      '1. Resolve the historical party setup and era-safe leader/succession roster. The current `CYP_political_leaders` helper contains later leaders and must never run unguarded in1970. Date-gate or replace it for this tree; use existing portraits only after checking identity and date.',
      '2. Define the new COLDWAR variables, spirits, active-party dynamic programmes, English localisation and event contracts under the same prefix. Variables start once, are clamped0..100 and are not historical measurements.',
      '3. Add the tree selector and protect it in the1970 fallback loader, following the existing authored-tree exclusions. Never reset progress when a party changes. Give every section an MD-style shortcut; opening focus is The Republic at Ten.',
      '4. Gate the existing modern CYP decision category: offshore gas/EU accession and modern financing must not leak into1970. Keep user-requested policy choices in the focus tree; the crisis can resolve through events. Do not quietly add a second decision minigame.',
      '5. Apply shared policies once, one programme per exclusive policy slot; active-party modifiers only while that party governs. Cross-sector national outcomes (independence/implemented Enosis/federation) must have reciprocal exclusions/flags, not just visual in-section exclusions.',
      '6. On offers, display the offer, prospective benefits and failure result. Apply conditional modifiers in the acceptance event, not on sending the offer. Bind state effects to valid current owner/controller; clean up treaty effects when a treaty ends.',
      '7. Use GDP-relative administration/grant costs and existing native financial recalculation. Building caps, workforce, power and recurring upkeep are required checks. Native construction queue remains payable. No extra research slots, nuclear capability or future equipment.',
      '8. Static checks: all IDs/localisation/icons exist; prerequisites resolve; exclusions reciprocal; no overlap; six major routes and combined21/22 gate are reachable in their intended scenarios; enumerate compatible policy combinations for revised caps. Verify the39-focus Turkish Cypriot section cannot manufacture counterpart consent.',
      '9. In-game tests: historical start, each important ruler plus a minor-party government, election away/back, interrupted focus, funds, donor refusal, loss of state146, prevented/successful coup, TUR human refusal, actual partition, staged access/services relief, aid and restitution, save/reload and multiplayer. Static source matches do not replace these tests.', '',
      '## Sources and audits','',
      'The installed MD path is treated as the user-provided reference snapshot; its online version status was not verified. Exact coding examples and balance traps are documented in `EFFECTS_REVIEW.md`; coordinate observations and proposed geometry in `LAYOUT_REVIEW.md`. Historical sources support the starting context and major chronology; bespoke bonuses, alternate parties and policy forks are design proposals, not sourced historical platforms.', '']
    for source in sources:
        lines.append(f'- **{source["id"]}:** '+ (f'[{source["use"]}]({source["url"]})' if 'url' in source else f'`{source["path"]}` — {source["use"]}'))
    (HERE/'DESIGN.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

if __name__=='__main__':
    result=validate()
    HERE.mkdir(parents=True,exist_ok=True)
    (HERE/'coldwar_cyprus_1970_design.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    write_dossier()
    (HERE/'VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    # build_md_view.py renders both current preview aliases from this data.
    print(json.dumps(result))


