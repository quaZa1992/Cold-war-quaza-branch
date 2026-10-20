"""Turkish Cypriot content: community agency, access, economy and settlement."""

def add_community(section,focus,either,exclusive,spirits):
    section('turkish_cypriots','The Turkish Cypriot Community',(86,0),
            'Fazil Kucuk, Rauf Denktas, civilian organisations and the emerging CTP are distinct interlocutors. Address enclaves, restrictions, separate administration and political equality; they are not an obedient faction of the CYP ruling party.')
    def f(key,title,xy,parents=(),**opts):
        node=focus('tc_'+key,title,'turkish_cypriots',xy,['tc_'+p for p in parents],**opts)
        node['community_content']=True
        return node
    def join(node,*parents):return either(node,*['tc_'+p for p in parents])
    def x(a,b):exclusive('tc_'+a,'tc_'+b)

    f('community','A Community in Enclaves',(0,0),
      note='January1970: Turkish Cypriot enclaves and a separate communal administration exist within the internationally recognised Republic. No sovereign NCY at start. Starting spirit: police costs+10%, bureaucracy costs+8%; northern map-state construction-12% and positive growth-15%.')
    f('leadership','Recognise the Communal Interlocutors',(0,1),['community'],cost=.5,
      note='Fazil Kucuk remains the senior communal/vicepresidential figure until1973; Rauf Raif Denktas is the negotiating representative and later successor. Neither becomes CYP president merely by being consulted.')
    f('kucuk','A Channel to Fazil Kucuk',(-4,2),['leadership'],cost=.5,event='tc_leadership_channel',
      note='Direct dialogue with the communal leadership; the counterpart decides whether to cooperate. Turkish Cypriot community-state is tracked separately from national ruling_party.')
    f('denktash','Support the Clerides–Denktas Talks',(4,2),['leadership'],cost=.5,event='tc_negotiating_channel',
      note='Clerides can act for the Makarios government; this does not put Clerides in power. Denktas must obtain a community mandate, not merely accept Ankara\'s instructions.')
    join(f('restrictions','The Restrictions Question',(0,4),pp=25),'kucuk','denktash')
    f('open_trade','Remove Remaining Civilian Trade Controls',(-4,5),['restrictions'],cost=1,tension=-10,
      event='tc_access_protocol',note='Replace access penalties with a lower, defined stage after an implemented agreement. Restrictions were already being eased after1967; avoid portraying January1970 as an unchanged1964 siege.')
    f('pressure','Renew Restrictions as Political Pressure',(4,5),['restrictions'],pp=40,tension=10,
      mods={'police_cost_multiplier_modifier':.08},note='An OPTIONAL renewed coercive policy, not an assertion of an unchanged1964siege in1970. Short-term leverage carries policing expense and hostility; no productivity, tax or manpower reward. Legacy enclave penalties persist.')
    x('open_trade','pressure')
    f('routes','Protected Roads and Supply Routes',(-6,6),['open_trade'],cost=1,tension=-5,event='tc_access_protocol',
      note='Civilian movement and trade access; removal of army defences is a separate negotiation, not a precondition for medicine.')
    f('utilities','Restore Water and Medical Supplies',(-2,6),['open_trade'],cost=1,event='tc_shared_services',
      note='Fund reliable utilities and treatment across communal boundaries. The same project cannot pay twice if the shared constitution branch has already restored it.')
    f('police','Maintain Emergency Police Posts',(2,6),['pressure'],pp=25,tension=5,
      mods={'police_cost_multiplier_modifier':.05},note='A policy of sustained restriction, not an automatic massacre event; armed incidents can worsen the crisis.')
    f('supervised','Permit Supervised Civilian Deliveries',(6,6),['pressure'],cost=.5,tension=-4,event='tc_limited_relief',
      note='Partial relief without freedom of movement. It cannot unlock the economic-normalisation reward on its own.')
    join(f('protocol','A Communal Services Protocol',(0,8),cost=.5,
           note='Choose between joint services or a negotiated decentralised service arrangement. Hardline governments can open talks here, but receive no access relief until they actually implement safeguards.'),
         'routes','utilities','police','supervised')
    f('joint_budgets','Joint Municipal Budgets',(-4,9),['protocol'],cost=1.5,event='tc_joint_services_offer',
      mods={'stability_factor':.04,'bureaucracy_cost_multiplier_modifier':.03},note='Joint funding needs both communities\' acceptance; remove parallel-service friction only as specified by the outcome contract.')
    f('local_services','Locally Managed Communal Services',(4,9),['protocol'],cost=1.5,event='tc_local_services_offer',
      mods={'stability_factor':.03,'bureaucracy_cost_multiplier_modifier':.06},note='Decentralisation gives greater communal control with higher ongoing administrative costs; rights and civilian access remain mandatory.')
    x('joint_budgets','local_services')
    f('cooperative_credit','Credit for Turkish Cypriot Cooperatives',(-6,10),['joint_budgets'],cost=1,
      mods={'interest_rate_multiplier_modifier':-.10},requires='Civilian access protocol implemented; accepted joint-services agreement.',
      note='A modest island-level credit-efficiency effect, not a claim that every Turkish Cypriot supports one economic party.')
    f('mixed_workshops','Reopen Mixed-Community Workshops',(-2,10),['joint_budgets'],cost=1,
      mods={'industrial_capacity_factory':.03},requires='Civilian access protocol implemented; property safeguards.',note='Supports existing repair and processing capacity; no free factory sector.')
    f('business_licences','Recognise Communal Business Licences',(2,10),['local_services'],cost=.5,
      mods={'office_park_income_tax_modifier':.03},requires='Civilian access protocol implemented; accepted local-services agreement.',
      note='Income applies to existing staffed offices only; no invented offshore sector.')
    f('property_records','A Joint Register of Property Claims',(6,10),['local_services'],cost=.5,settlement=5,
      requires='Civilian access protocol implemented; both communities retain access to claims procedures.',note='Documents ownership and displacement claims, not forced alienation or cancellation of rights.')
    join(f('services_mandate','A Mandate for Shared Civilian Life',(0,11),
           requires='At least one implemented access/services outcome; one-way gestures do not count as community assent.'),
         'cooperative_credit','mixed_workshops','business_licences','property_records')
    f('civil_representation','Civil Representation First',(-4,12),['services_mandate'],cost=.5,
      mods={'stability_factor':.03},note='An offer of plural civilian representation. Turkish Cypriots choose their delegates; CYP cannot install a compliant opposition leader.')
    f('security_representation','Security Notables First',(4,12),['services_mandate'],tension=5,
      mods={'foreign_influence_defense_modifier':-.04},note='Negotiate through established security-linked notables; this preserves patron dependence and may marginalise civilian organisations.')
    x('civil_representation','security_representation')
    f('ctp','Talk to Berberoglu and the Emerging CTP',(-6,13),['civil_representation'],cost=.5,event='tc_ctp_dialogue',
      requires='date >=1970.12.27; CTP actually founded; Ahmet Mithat Berberoglu is the historical founding leader.',
      note='The CTP is not present in January1970. Its formation and constituency are Turkish Cypriot political developments; a CYP focus only opens dialogue, not control of the party.')
    f('civic_space','Protect Independent Communal Organisations',(-2,13),['civil_representation'],cost=.5,settlement=5,
      note='Protect lawful organisations, workers and municipal representatives on both sides; do not make rights dependent on supporting the government.')
    f('arms_guarantees','Negotiate Local Arms Guarantees',(2,13),['security_representation'],cost=.5,event='tc_security_protocol',
      note='Supervised reciprocal security measures, including armed organisations associated with TMT and Greek Cypriot militias. No forced automatic disarmament of either community.')
    f('patron_security','Keep Patron-Funded Security',(6,13),['security_representation'],tension=5,
      mods={'foreign_influence_defense_modifier':-.04},note='Rely on existing external patronage; Turkish aid must actually be provided by Turkey. No money is created by this focus.')
    join(f('mandate','A Turkish Cypriot Negotiating Mandate',(0,15),event='tc_community_mandate',
           note='Community assent is an independently resolved outcome. Cyprus cannot set assent just by completing a negotiation focus.'),
         'ctp','civic_space','arms_guarantees','patron_security')
    f('political_equality','Bicommunal Political Equality',(-4,16),['mandate'],cost=1,settlement=10,event='tc_equality_offer',
      note='A federal or power-sharing proposal recognises political equality and safeguards; acceptance requires a real community mandate.')
    f('unitary_bargain','Seek a Unitary Constitutional Bargain',(4,16),['mandate'],cost=1,event='tc_unitary_offer',
      note='Offer protected rights within a more central republic. Rejection is possible and preserves deadlock; majority voting cannot manufacture Turkish Cypriot consent.')
    x('political_equality','unitary_bargain')
    f('federal_framework','Secure Assent to a Federal Framework',(-4,17),['political_equality'],cost=.5,event='tc_federal_assent',
      note='Set the appropriate TC assent flag only after accepted terms. The shared constitutional tree must still ratify and implement the settlement.')
    f('shared_republic','Secure Assent to a Shared Republic',(4,17),['unitary_bargain'],cost=.5,event='tc_republic_assent',
      note='A revised central republic needs explicit Turkish Cypriot acceptance, enforceable safeguards and effective freedom of movement.')
    join(f('constitutional_consent','Consent Is More than a Signature',(0,19),requires='Accepted community mandate plus implemented safeguards; no unresolved reprisals.',
           note='An audit of implementation, not a second stability prize. Ratification in the shared tree requires this outcome.'),'federal_framework','shared_republic')
    f('enosis_consent','Put Enosis before Both Communities',(-6,20),['constitutional_consent'],cost=.5,event='tc_enosis_consultation',
      note='Turkish Cypriots can refuse. No forced population transfer, annexation or community-consent flag is awarded for merely holding a consultation.')
    f('unilateral_resolution','Threaten a Unilateral Resolution',(6,20),['mandate'],pp=35,tension=15,
      mods={'police_cost_multiplier_modifier':.10},note='A coercive alternative to consent. Constitutional deadlock and state access penalties remain; threats can provoke external intervention. Reprisals remain a separate explicit policy with damage and displacement consequences.')
    x('enosis_consent','unilateral_resolution')
    f('postwar_admin','Contact the Turkish Cypriot Administration',(-4,22),['mandate'],cost=.5,event='tc_postwar_contact',
      requires='Actual intervention/partition has occurred; NCY administration or corresponding occupation authority exists.',
      note='Post-crisis contact with a de facto administration does not automatically recognise a sovereign state. No1970 NCY release.')
    f('postwar_dispute','Continue the Sovereignty Dispute',(4,22),['mandate'],pp=25,event='tc_postwar_dispute',
      requires='Actual intervention/partition has occurred.',note='Diplomatic opposition without a free war goal, instant reconquest or mass population transfer.')
    x('postwar_admin','postwar_dispute')
    f('returns','Negotiate Return and Property Claims',(-6,23),['postwar_admin'],cost=1.5,event='tc_return_property_agreement',
      note='Voluntary return, restitution and compensation options need claimant safeguards and counterpart implementation. They do not absolve perpetrators or erase missing-persons cases.')
    f('civilian_access','Demand Civilian Access across the Lines',(-2,23),['postwar_admin'],cost=.5,event='tc_postwar_access',
      note='Aid and family contacts can improve before a final sovereignty settlement. Property claims remain open.')
    f('sovereignty_leverage','Retain Diplomatic and Legal Pressure',(4,23),['postwar_dispute'],cost=.5,
      note='Protect legal claims without manufacturing a victory. This course retains the economic and humanitarian burdens of partition.')
    join(f('beyond_partition','A Settlement beyond Partition',(0,25),cost=1.5,event='tc_postwar_settlement',
           requires='Ceasefire; both-community mandate; applicable foreign acceptance; safeguards and accountability.',
           note='Resolve only the obligations actually implemented. Recognition,1983 independence declaration and voluntary reunification remain separate outcomes.'),
         'returns','civilian_access','sovereignty_leverage')

    # Explicit staged replacement, never repeatedly subtracting the same malus.
    def changes(node,*items):node['spirit_changes']=list(items)
    north='COLDWAR_CYP_1970_restricted_movement_north';south='COLDWAR_CYP_1970_restricted_movement_south';admin='COLDWAR_CYP_1970_tc_parallel_administration'
    bykey={n['key']:n for n in focus.__globals__['nodes']}
    access=[{'id':north,'operation':'replace','modifiers_after':{'state_production_speed_buildings_factor':-.06,'state_productivity_growth_modifier':-.075}},
            {'id':south,'operation':'replace','modifiers_after':{'state_production_speed_buildings_factor':-.025}},
            {'id':admin,'operation':'replace','modifiers_after':{'bureaucracy_cost_multiplier_modifier':.04,'police_cost_multiplier_modifier':.05}}]
    for key in ('tc_open_trade','tc_routes','safe_passage'):
        changes(bykey[key],*access)
    changes(bykey['joint_services'],
            {'id':south,'operation':'remove'},
            {'id':north,'operation':'replace','modifiers_after':{'state_production_speed_buildings_factor':-.03,'state_productivity_growth_modifier':-.04}},
            {'id':admin,'operation':'replace','modifiers_after':{'bureaucracy_cost_multiplier_modifier':.02,'police_cost_multiplier_modifier':.025}})
    bykey['joint_services']['note']='A funded intermediate shared-services stage: south access penalty removed, north construction -3%/positive-growth -4%, national administration friction bureaucracy+2%/police+2.5%. Same highest-relief ledger as the TC branch; earlier/later offers cannot regress or multiply relief. Does not resolve the constitution.'
    for key in ('joint_services','tc_utilities'):
        bykey[key]['cost_project_slot']='COLDWAR_CYP_1970_water_and_medical_access'
        bykey[key]['note']+=' Shared once-funded project slot: if the capital works are already paid, unlock the follow-up without charging the same works again.'
    for key in ('checkpoint_leverage','tc_pressure','tc_police','tc_unilateral_resolution'):
        bykey[key]['sunset_on']='Implemented rights-compliant access/services compact; remove the restriction-policy idea, not the historical record of abuses.'
    for key in ('tc_joint_budgets','tc_local_services'):
        changes(bykey[key],{'id':north,'operation':'remove'},{'id':south,'operation':'remove'},
                {'id':admin,'operation':'remove'})
        bykey[key]['requirements'] += ' Implemented civilian-access safeguards; accepted community service agreement. Replacement is atomic and once-only; do not stack two service programmes.'
    return {'start_spirit':admin,'access_stage':access,'context':'Tied to conflict and administrative fragmentation, not ethnicity as an inherent penalty.'}
