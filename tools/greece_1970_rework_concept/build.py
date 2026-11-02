# IMPERIA COLD WAR — Greece approval concept compiler. Does not emit loaded runtime.
from pathlib import Path
import json,base64,io,hashlib,itertools,re
from collections import Counter
from PIL import Image
from design import build,ROOT
from contracts import STARTING,offers,SOURCES,COUNTRIES

OUT=ROOT/'docs/greece_1970_rework_20261029'
VIS=Path('C:/Users/Enes/.codex/visualizations/2026/10/27/01a17ef0-dd9d-7a11-b0e5-985305e237a1/greece-1970-rework.html')
LABELS={
'political_power_factor':'Political power gain','stability_factor':'Stability','research_speed_factor':'Research speed',
'army_org_factor':'Army organization','navy_org_factor':'Naval organization','training_time_factor':'Training time','planning_speed':'Planning speed','max_planning_factor':'Maximum planning',
'foreign_influence_modifier':'Foreign influence','foreign_influence_defense_modifier':'Foreign influence defence',
'industrial_capacity_factory':'Factory output','industrial_capacity_dockyard':'Dockyard output','dockyard_productivity':'Dockyard productivity',
'production_speed_buildings_factor':'Construction speed','production_speed_industrial_complex_factor':'Civilian factory construction','production_speed_arms_factory_factor':'Military factory construction','production_speed_dockyard_factor':'Dockyard construction',
'production_factory_max_efficiency_factor':'Production efficiency cap','production_factory_efficiency_gain_factor':'Production efficiency growth',
'agricolture_productivity_modifier':'Agricultural productivity','office_park_income_tax_modifier':'Office income tax yield',
'bureaucracy_cost_multiplier_modifier':'Bureaucracy budget cost','education_cost_multiplier_modifier':'Education budget cost','health_cost_multiplier_modifier':'Health budget cost',
'naval_speed_factor':'Naval speed','naval_invasion_prep_speed':'Naval invasion preparation speed','amphibious_invasion':'Amphibious invasion attack',
'special_forces_cap':'Special forces capacity','special_forces_training_time_factor':'Special forces training time','naval_equipment_upgrade_xp_cost':'Naval equipment upgrade XP cost',
'democratic_drift':'Daily Pro-Western support','neutrality_drift':'Daily Non-Aligned support','war_support_factor':'War support','trade_opinion_factor':'Trade opinion','consumer_goods_factor':'Tax cost',
}
STATES={139:'Thessaly',140:'Southern Macedonia',141:'Central Greece',142:'Peloponnese',143:'Aegean Islands',144:'Crete',145:'Nicosia and southern Cyprus',146:'Famagusta and northern Cyprus',132:'Eastern Serbia'}
BUILDINGS={'industrial_complex':'Civilian factory','arms_factory':'Military factory','offices':'Office park','infrastructure':'Infrastructure','dockyard':'Dockyard','radar_station':'Radar station'}
TECH={'CAT_industry':'Industry','CAT_infantry':'Infantry','CAT_aircraft':'Aircraft','CAT_light_aircraft':'Light aircraft','CAT_air_to_ground_weapons':'Air-to-ground weapons','CAT_naval':'Naval technology','CAT_electronics':'Electronics','land_doctrine':'Land doctrine'}
EQUIPMENT={'infantry_weapons_type':'Infantry weapons','L_AT_Equipment':'Light anti-tank weapons','AA_Equipment':'Anti-air weapons','cnc_equipment_type':'Command and control equipment'}

def numeric(key,value):
 return f'{value:+g}' if key.endswith('_drift') else f'{value*100:+g}%'
def values(v):return [LABELS.get(k,k)+': '+numeric(k,n)for k,n in v.items()]
def effects(e):
 t=e['type']
 if t in ('modifier','temporary'):return [e['spirit']+(f" ({e['days']} days)"if t=='temporary'else'')]+values(e['values'])
 if t=='remove_spirit':return ['Remove '+e['name']]+values({k:-v for s in DATA['starting_spirits']if s['name']==e['name']for k,v in s['values'].items()})
 if t=='building':return [f"{STATES[e['state']]}: State shared building slots +{e['shared_slots']}",f"{STATES[e['state']]}: {BUILDINGS[e['building']]} +{e['levels']}"]
 if t=='research':return [f"{e['uses']} x {e['bonus']*100:g}% research bonus: {TECH[e['category']]}"]
 if t=='doctrine':return [f"{e['uses']} x {e['bonus']*100:g}% doctrine cost reduction: {TECH[e['category']]}"]
 if t=='experience':return [f"{e['service'].title()} experience +{e['value']}"]
 if t=='manpower':return [f"Military manpower {e['amount']:+,}"]
 if t=='equipment':return [f"{e['label']} {e['amount']:+,}"]
 if t=='units':return [f"Cyprus: +{e['count']} divisions, {e['template']}",f"Per division: {e['manpower_each']:,} manpower; {e['combat_width']} combat width; 6 light infantry battalions",'Full manpower and equipment on arrival']+[f"Per division: {EQUIPMENT[key]} +{n:,}"for key,n in e['equipment_each'].items()]
 if t=='native_action':return [e['text']]
 if t=='existing_actor':return e['effects']
 if t=='offer':return ['If they accept: '+DATA['offers'][e['key']]['name']]
 if t=='conditional_transaction':return [e['label'],f"Weekly expense: +{e['weekly_gdp_percent']:g}% Greek GDP"]+[s for inner in e['effects']for s in effects(inner)]
 if t=='political_power':return [f"Political power {e['amount']:+g}"]
 if t=='opinion':return [f"Opinion of {COUNTRIES[e['target']]} {e['amount']:+g} ({e['days']} days)"]
 if t=='wargoal':return [f"Greece: gain {e['label']} war goal against Cyprus"+(''if e['goal_type']=='annex_everything'else': '+STATES[145])+(f" ({e['expiry_days']} days)"if e['expiry_days']else'')]
 if t=='annexation':return ['Annex Cyprus']+[STATES[s]+': ownership to Greece'for s in e['states']]+['Transfer existing Cyprus-owned forces to Greece']
 if t=='country_cession':return ['Cyprus is annexed by Greece']+[STATES[s]+': ownership to Greece'for s in e['states']]+['Cypriot forces and public accounts transfer to Greece']
 if t=='ledger_succession':return ['Treasury: add current signed Cypriot treasury','National debt: add current Cypriot debt','International investments: transfer current Cypriot assets and liabilities']
 if t=='union_integration':
  result=[]
  for v in e['variants'].values():
   result += [v['label'],f"Political power -{e['pp_cost']}",f"Treasury: -{v['setup_gdp_percent']:g}% Greek GDP",'Remove '+v['remove']]+values({k:-n for k,n in v['remove_values'].items()})+[f"Weekly expense: -{v['stop_weekly_gdp_percent']:g}% Greek GDP"]+['Greek core: '+STATES[s]for s in v['states']]
  return result+[e['settlement_spirit']]+values(e['values'])+[f"Weekly expense: +{e['weekly_after_gdp_percent']:g}% Greek GDP"]
 raise ValueError(t)

def prepare():
 global DATA
 DATA=build();DATA.update(starting_spirits=STARTING,offers=offers(),sources=SOURCES,countries=COUNTRIES,modifier_labels=LABELS,state_names=STATES,building_names=BUILDINGS,technology_names=TECH,equipment_labels=EQUIPMENT)
 old=json.loads((ROOT/'tools/cyprus_1970_rework/approved_design.json').read_text('utf8'))
 DATA['crisis_intervention']=old['intervention'];DATA['crisis_intervention']['status']='Existing CYP_R2 terms retained. Source cross-check recorded in MECHANICS_REFERENCE.md.'
 DATA['crisis_decisions']=old['crisis_decisions']
 DATA['enosis']={'project':'IMPERIA COLD WAR','status':'Approval concept, not loaded','routes':['enosis_full','enosis_south'],'integration':next(e for f in DATA['focuses']if f['key']=='cypriot_settlement'for e in f['effects']),'consolidated_focuses':{'enduring_order':['civil_ministries','security_budget'],'provinces':['universities'],'workers_voice':['social_contract']}}
 DATA['historical_start']={'date':'January 1970','government':'Prime Minister Georgios Papadopoulos; Regent Georgios Zoitakis; King Constantine II in exile.','parties':'Domestic parties are banned. ERE, Centre Union, EDA and KKE represent historical constituencies. PAK is an exile resistance movement. ND and PASOK are founded in 1974, not lawful parties in January 1970. KKE Interior constituencies appear inside the broad-left alternative, not an invented MD party slot.','institutions':'Greece remains a NATO member and a kingdom. EEC association is restricted, not membership. Withdrawal from the Council of Europe was notified in December 1969; legal membership ends in December 1970.','economy':'Strong shipping, tourism and growth coexist with regional inequality, emigration and shortages of technical expertise. No custom workforce-size penalties.','later':'The Ioannidis takeover, the July 1974 Cyprus coup, democratization, European accession and the 1983 health-system precedent inform reachable alternatives rather than scripted inevitabilities.'}
 DATA['implementation_contract']={
 'approval':'Design only. Current Greek runtime tree and all loaded files are retained until approval.',
 'party_programmes':'Keep all branches visible. Exact existing native party-in-power triggers gate availability and execution. Rebuild each party-owned dynamic modifier from earned receipts only while that party governs; named leader subprogrammes require that leader as well. Disable their weekly streams on departure; restore on return. Never replay buildings, slots, research, XP, setup fees or one-time starting-spirit remedies. State constitutional settlements and signed bilateral agreements retain their separate state conditions.',
 'refresh':'Existing party/leader change callbacks plus one GRE monthly reconciliation. Fixed CYP/GRE crisis participants and explicit offer partners only. No new daily or weekly script observer, no every_country loops or global monthly offer searches. Budget streams use existing MD weekly accounting, with literals of at most five decimal places.',
 'party_identity':'Use actual native party-name localisation keys. Slot 1 uses the dated ERE/ND identity; slot 3 the dated PAK/PASOK identity. Correct the native 1970 slot23 display to Royalists because the kingdom still exists; reserve restoration language for an actual subsequent abolition. Preserve existing slot alignment, including slot7 State Emergency Hardliners. Do not activate banned parties automatically.',
 'civilian_transfer':'Negotiate a Civilian Handover proposes a one-time domestic event with actual Kanellopoulos conservative or Mavros Centre Union caretaker cabinets, preserving the existing native party/leader dispatcher. A cabinet already under civilian rule is not overwritten. This is a hypothetical negotiated alternative, not a claim of a real January 1970 deal. Actual civilian authority ends Emergency Rule. The following amnesty and election focuses restore competition; PAK/PASOK and KKE may later govern through the native party system. The Crown remains constitutionally unsettled until the explicit settlement fork. Papadopoulos and Ioannidis internal choices also route to real government/leader snapshots rather than cosmetic names.',
 'offer_lifecycle':'A Greek national focus proposes each unique contract. Named RP recipients receive accept/refuse decisions with full prospective numeric effects for all participants. The pending offer expires after 90 days, cleaned by monthly/event callbacks. An unpaid declined or expired offer may be resent once by a single Greek event option with no home-country decision menu; one active offer per contract. Every required recipient must agree to identical terms. Payment, ownership, capacity, existence, independence where required, party proposer and relation guards recheck at acceptance. No unilateral rewards. Setup and one-time assets commit atomically only once all approvals and all guards succeed. Permanent standing spirits suspend and restore together without repeating charges or assets.',
 'community':'Snapshot only the current native global.EU_member, excluding GRE, for one proposal round. Use exact count N for Greek expense N x 0.001% Greek GDP per week and each member income 0.001%. Six is only the January 1970 preview. Membership or passed-law changes invalidate pending terms. Accession replaces association spirits and charges. Before consent, a native preview helper enumerates every applicable effect of current EU_passed_votes as well as all seven base EU_member modifiers, research and money. At concept snapshot no specific passed laws are assumed. Add EU_member through its native on_add only after admission. No EU_join helper or custom membership roster.',
 'community_setup_correction':'After the erroneous inherited Greek EU_member is removed through its native on_remove, synchronize native member/law/tech-sharing cleanup and explicitly clear the artificial EU_former_member and EU_rejoin_cooldown flags. Greece was never a former member. Prevent the history/generator from restoring the error. Begin with Restricted European Association. Do not touch other actual members.',
 'buildings':'Every building level first adds one shared slot in the same state inside the same asset receipt. Actual target ownership, control, native building cap and available state capacity are separate guards. Failure never charges setup money or creates orphan slots. A recipient asset uses that recipient ownership, not Greek ownership.',
 'cyprus_preparation':'The extra +10 staff penetration uses a unique timed receipt and clamp 0..100. It expires after 180 days or on network withdrawal/crisis cancellation; remove the contribution once and clear the receipt. Existing withdrawal remains -20, plus -10 when preparation is active. A resolved coup consumes the contribution receipt. No double subtraction after resolution. Remove Forward Operational Planning when cancelled.',
 'cyprus_resolution':'Reuse the existing deterministic 14-day warning: captured defence is 40 plus Cypriot preparedness, and Greek penetration must strictly exceed it. A tie defends. No random roll or periodic roll. Operational Initiative is once only after real coup success with the coup government still in power, peaceful GRE-CYP relations and no sanctions/embargo. Completion rechecks these guards. Its weekly charge stops on loss of eligibility or the 180-day expiry.',
 'settlement':'The four governments are Cyprus plus the three guarantors, not four guarantors. Require separate Greek Cypriot and Turkish Cypriot assent receipts from the Cypriot communal programme. All six state pairs are checked in both sanction directions. Suspend and restore all four settlement spirits collectively. Close the existing security-crisis receipt on successful settlement.',
 'nato':'Retain installed CYP_R2 war and NATO APIs and all nine existing Greek shared-focus IDs, relocating their anchors after approval. Direct Greek entry removes prior GRE/TUR NATO memberships before joining the actual CYP-TUR war. Return each prior member only after both GRE-TUR and CYP-TUR peace. This is the requested alternative-history full Alliance exit; historical Greece withdrew only from integrated military command in 1974. New Aegean Expeditionary Command is a once-only 180-day direct-entry reward: +10% army and navy organization, +25% planning, +15% maximum planning, +20% amphibious attack, +30% invasion preparation, -10% office income and +0.005% Greek GDP weekly expense. Require actual successful entry on Cyprus side. End that package on related Greek-Turkish peace or 180 days; never end NATO separation merely because the reward expires. No automatic divisions, aircraft or ships are created. Real volunteer formations still require the actual native deployment action and Cypriot approval. Same-faction deployment compatibility remains a live-engine check.',
 'new_helpers':'COLDWAR_GRE_R2_politics events, programme refresh, recipient offers, dynamic law preview, staff receipt cleanup and post-coup reward helpers are proposed new work. Their names in this concept do not imply installed definitions.',
 'entry_transaction':'Wrap the existing escalation helper in a single guarded completion transaction. Verify independence, war sides, funds and native entry eligibility before snapshots and debit. After add_to_war, require actual GRE-TUR war, CYP-TUR war, no GRE-CYP war and the entry receipt before issuing the separate expeditionary package receipt and weekly active receipt. The previous helper entry flag alone does not prove success. If native entry fails, grant no package or stream, refund exactly the captured 100 PP and 0.5% Greek-GDP debit and undo only this attempt NATO changes through native helpers with the saved prior memberships. Clear the failed attempt separation receipts before rollback, not an unrelated active crisis. No permanent faction loss after a failed war join. Do not replay a completed successful entry.',
 'reinforcements':'New independent 7-day Reinforce the National Guard focus offers two CYP-owned 18-width light infantry divisions. Six L_Inf_Bat each, exactly1200 manpower and1200 infantry weapons,120 light anti-tank,120 anti-air and120 CNC equipment per division. Greece loses the complete two-division reserve, Cyprus receives fully formed units immediately on consent. Available before Turkish intervention; no dependency or exclusion with Volunteers or Fight Beside Cyprus. This is a one-time paid unit transfer, not a starting OOB, free reserve, standing spirit or change of belligerent status. Use explicit Greek stockpile debit plus unit generation; do not also transfer a second equipment package. The new transaction data and REINFORCEMENT_REFERENCE.md define the native engine conservation fixture. No extra monthly observer. Independent Cypriot consent and controlled landing area are required. Historical precedent is the exceptional1964-67 deployment, not an automatic Treaty of Guarantee entitlement.',
 'replacement':'After approval: archive old Greek content outside the mod on E:, update its original generator and emitted tree, remove stale custom focus/idea/event references, integrate the approved data and preserve the existing Cyprus shared-focus identities. No deletion or installation performed by this concept build.'}
 from fiscal import apply_prices
 apply_prices(DATA)
 profile=json.loads((OUT/'MD_REFERENCE_PROFILE.json').read_text('utf8'));icons={i['theme']:i for i in profile['icon_candidates'] if i['candidate_sprite']}
 mapping={
 'republic':'constitution republic parliamentary_king parliament_first constitutional_right liberal_mandate',
 'cabinet':'handover papadopoulos civil_ministries professional_service provinces conservative_mandate',
 'mediation':'gre_consult guarantee_settlement aegean_talks liberal_compromise service_council kanellopoulos',
 'ballot':'election constitutional_crown constantine dynastic_settlement cypriot_settlement',
 'checkpoints':'entrench tribunals security_directorate loyal_command security_budget enduring_order',
 'rights':'amnesty civil_war_families left_front social_contract',
 'plan':'development orthodox_plan military_technocrats national_change public_credit',
 'technical':'technical universities research_institutes army_school skills_return',
 'movement':'visitor_credit island_links shipping sea_control aegean_command sea_denial',
 'workshops':'industrial_credit army_industry shipyards domestic_marine_supply',
 'industrial_standards':'industrial_standards productive_credit negotiated_development',
 'land_improvement':'rural_water farm_cooperatives',
 'commercial_credit':'commercial_farming',
 'officers':'joint_staff officer_compact gre_officers gre_network gre_coup staff_network operational_initiative gre_response gre_escalate air_command close_support',
 'mobile':'territorial_army professional_cadres gre_volunteers aegean_deterrence reinforce_guard',
 'infantry':'american_standard interceptors',
 'association':'association accession european_credit french_option western_bargain eastern_terms',
 'liaison':'gre_treaty gre_withdraw external_room british_guarantee services_reconciled',
 'passage':'yugoslav_corridor',
 'enterprise':'bulgarian_trade enterprise',
 'audit':'tax_compliance managed_opening',
 'clinics':'national_health',
 'democratic_socialism':'workers_voice left_mandate',
 'endure':'island_trade independent_diplomacy radar karamanlis enosis_full',
 'scrutiny':'royal_mandate royal_veto enosis_compromise',
 }
 themed={k:t for t,keys in mapping.items()for k in keys.split()}
 for f in DATA['focuses']:
  t=themed.get(f['key'],'cabinet');f['icon_theme']=t;f['icon_sprite']=icons[t]['candidate_sprite']
  f['effect_lines']=[s for e in f['effects']for s in effects(e)]
  f['relative_anchor']=next(n['id']for n in DATA['focuses']if n['group']==f['group'])
 for s in DATA['starting_spirits']:
  s['focuses']=[key for key in s['focuses']if key!='dynastic_settlement']
  s['effect_lines']=values(s['values']);s['source']= 'economy' if s['name']in('Uneven Development','Emigration and Technical Gaps','Maritime and Tourism Expansion')else'eec'if s['name']=='Restricted European Association'else'guarantee'if s['name']=='1960 Treaty of Guarantee'else'history'
  if s['name']=='Emigration and Technical Gaps':
   s['description']='Emigration brings remittances but makes technical capacity at home harder to maintain. Education and returning expertise are essential to a broader domestic productive base.'
   s['remedy']='Complete Technical Skills at Home or Free and Capable Universities.'
  if s['name']=='1960 Treaty of Guarantee':
   s['description']='The 1960 settlement recognizes the independent Republic of Cyprus and the guarantee roles of Greece, Turkey and the United Kingdom. Consultation and the obligations of the settlement give each government a stake in Cypriot security.'
   s['remedy']='Retained as the treaty basis of the guarantor paths. No automatic annexation, partition or sovereign control.'
  if s['name']=='Restricted European Association':s['description']='Association continues in limited treaty form, while further political integration and new Community financing are restricted. Greece is associated with the Community, without being a member.'
  if s['name']=='Suppressed Political Life':s['remedy']='Complete Amnesty and Open Courts, or enact the Social Contract under an actual civilian mandate.'
  if s['name']=='Civil War Inheritance':s['remedy']='An accepted parliamentary constitutional settlement or Rehabilitate the Excluded.'
 DATA['icon_manifest']=[dict(i,source='Existing local MD/IMPERIA asset. Original individual author and licence unknown; preserve IMPERIA_COLD_WAR_NOTICE.md and upstream attribution.',modifications='Preview-only resize to fit native icon area. Original game asset unchanged.')for t,i in icons.items()if t in {f['icon_theme']for f in DATA['focuses']}]
 images={}
 for t in {f['icon_theme']for f in DATA['focuses']}:
  im=Image.open(ROOT/icons[t]['texture']).convert('RGBA');im.thumbnail((96,80));buf=io.BytesIO();im.save(buf,format='PNG',optimize=True);images[t]='data:image/png;base64,'+base64.b64encode(buf.getvalue()).decode()
 DATA['images']=images
 return DATA

def audit(d):
 fs=d['focuses'];by={f['key']:f for f in fs};ids=[f['id']for f in fs]
 assert len(fs)==len(by)==len(set(ids))==100
 assert Counter(f['group']for f in fs)=={g['key']:g['count']for g in d['groups']}
 overlaps=[]
 for a,b in itertools.combinations(fs,2):
  if abs(a['x']-b['x'])*96<165 and abs(a['y']-b['y'])*130<128:overlaps.append([a['key'],b['key']])
 assert not overlaps,overlaps
 for f in fs:
  for group in f['prerequisites']:
   for p in group:assert p in by and by[p]['y']<f['y'],(f['key'],p)
  for p in f['exclusive']:assert f['key']in by[p]['exclusive'],(f['key'],p)
  for e in f['effects']:
   if 'values'in e:assert set(e['values'])<=set(LABELS),(f['key'],e)
   if e['type']=='building':assert e['levels']==e['shared_slots']and e['state']in STATES
   if e['type']in('research','doctrine'):assert e['category']in TECH
   if e['type']=='conditional_transaction':
    assert e['once']and e['post_conditions']and e['receipt']and e['active_receipt']
    for inner in e['effects']:assert set(inner.get('values',{}))<=set(LABELS)
  assert f['completion_recheck']
 # All branches are structurally reachable with their OR alternatives; no unchosen exclusive is forced by another prerequisite.
 for focus in fs:
  def search(todo,taken):
   if not todo:return True
   key,*rest=todo
   if key in taken:return search(rest,taken)
   if any(x in taken for x in by[key]['exclusive']):return False
   taken=taken|{key};groups=by[key]['prerequisites']
   return any(search(list(choices)+rest,taken)for choices in itertools.product(*groups))if groups else search(rest,taken)
  assert search([focus['key']],set()),focus['key']
 assert len(d['offers'])==15 and len(d['starting_spirits'])==9
 for s in d['starting_spirits']:assert all(key in by for key in s['focuses'])
 transfer=d['offers']['reinforcements'];units=transfer['sides']['CYP']['effects'][0]
 assert transfer['transaction']['manpower']==units['count']*units['manpower_each']==2400
 assert transfer['transaction']['equipment']=={k:n*units['count']for k,n in units['equipment_each'].items()}
 for o in d['offers'].values():
  for s in o['sides'].values():
   assert set(s['values'])<=set(LABELS)
   for e in s['effects']:
    if e['type']=='building':assert e['levels']==e['shared_slots']
 assert len(d['offers']['cyprus_settlement']['relationship_matrix'])==6
 assert d['offers']['association']['sides']['GRE']['weekly_formula']['per_recipient_gdp_percent']==.004
 from fiscal import native_fraction
 for f in fs:
  if f['weekly_gdp_percent']:native_fraction(f['weekly_gdp_percent'])
  b=f.get('budget_binding',{})
  if b.get('maximum_days'):assert b['spirit']and b['active_instance_receipt']and b['maximum_days']==180
 for o in d['offers'].values():
  for s in o['sides'].values():
   for field in ('weekly_gdp_percent','income_gdp_percent'):
    if s.get(field):native_fraction(s[field])
 for key in ('association','accession'):
  per=d['offers'][key]['sides']['GRE']['weekly_formula']['per_recipient_gdp_percent']
  assert per==d['offers'][key]['sides']['each_recipient']['income_gdp_percent']
 for key,payer,recipient in [('usa','USA','GRE'),('france','GRE','FRA'),('britain','GRE','ENG'),('germany','GRE','GER'),('soviet','GRE','SOV'),('cyprus_trade','GRE','CYP')]:
  sides=d['offers'][key]['sides'];assert sides[payer]['weekly_gdp_percent']==sides[recipient]['income_gdp_percent']
  assert sides[payer]['basis']==sides[recipient]['basis']=='GRE'
 for key,states in [('enosis_full',[145,146]),('enosis_south',[145])]:
  a=next(e for e in d['offers'][key]['sides']['GRE']['effects']if e['type']=='annexation')
  assert a['states']==states and a['transfer_troops']and not a['immediate_cores']and 812 in a['exclude_states']
  assert all(s in (145,146)for s in a['states'])
  guards=d['offers'][key]['transaction']['execution_guards']
  assert guards['CYP_ruling_party_slot']==20 and guards['CYP_exact_party_trigger']=='nationalist_right_wing_populists_are_in_power'
  types=[e['type']for e in d['offers'][key]['sides']['GRE']['effects']]
  assert types.index('ledger_succession')<types.index('annexation')
  refusal=d['offers'][key]['refusal'];goal=refusal['effects'][0]
  assert refusal['declining_country']=='CYP'and refusal['beneficiary']=='GRE'
  assert refusal['guards']['explicit_response']=='refuse'and refusal['guards']['current_pending_instance']
  assert goal['target']=='CYP'and goal['country']=='GRE'
  assert goal['goal_type']==('annex_everything'if key=='enosis_full'else'take_state_focus')
  assert refusal['turkish_entry']['restoration_peace_pairs']==[['GRE','CYP'],['GRE','TUR']]
 assert d['offers']['enosis_full']['refusal']['shared_once_receipt']==d['offers']['enosis_south']['refusal']['shared_once_receipt']
 assert by['enosis_full']['exclusive']==['enosis_compromise']
 return {'project':'IMPERIA COLD WAR','status':'Static concept checks passed. Not engine validation.','focus_count':100,'group_count':len(d['groups']),'standing_agreements':12,'one_time_reinforcement_package':1,'territorial_offers':2,'offers_total':15,'starting_spirits':9,'full_item_bounds_px':[165,128],'pitch_px':[96,130],'overlap_pairs':overlaps,'all_graph_references_valid':True,'exclusions_reciprocal':True,'all_focus_prerequisites_satisfiable':True,'reinforcement_resource_totals_match':True,'enosis_has_no_initial_cores_or_British_base_transfer':True,'supported_reward_keys_reviewed':True,'reused_CYP_R2_focus_IDs':sum(bool(f.get('existing_actor'))for f in fs),'grid_bounds':[min(f['x']for f in fs),max(f['x']for f in fs),min(f['y']for f in fs),max(f['y']for f in fs)],'boundary':'Orthogonal connector preview is approximate; native font, annex/ledger/troop bookkeeping, create_unit stockpile behavior and loading require engine checks after approval.'}

def document(d):
 lines=['IMPERIA COLD WAR','','# Greece 1970 replacement concept','','Status: approval proposal only. No loaded runtime files changed. 100 focuses, 11 sections, 12 standing agreements, 1 military transfer, 2 territorial offers and 9 starting spirits.','','## Historical premise','']
 lines+=list(d['historical_start'].values())
 lines+=['','All modifier amounts and package prices below are proposed game balance, not historical economic estimates. Benefits use verified native keys; recorded historical precedents justify institutions and tradeoffs. Later policies are reachable alternatives, not an automatic timeline.','','## Starting national spirits','']
 for s in d['starting_spirits']:
  lines+=['### '+s['name'],'',s['description'],'']+['- '+x for x in s['effect_lines']]+['','Remedy: '+s['remedy'],'']
 lines+=['## Exact focus structure and prospective effects','','Coordinates are resolved HOI4 grid positions; pitch 96 x 130 px. Each prerequisite group is OR internally; groups combine with AND. Mutual exclusions are reciprocal. Every party branch remains visible. Modifier entries are signed deltas to the named programme, not replacement totals. Money below is percentage of Greek GDP unless explicitly another basis. Recurring amounts are per week.','']
 for g in d['groups']:
  lines+=['### '+g['title']+f" ({g['count']})",'']
  for f in [x for x in d['focuses']if x['group']==g['key']]:
   lines += [f"#### {f['title']}",'',f"`{f['id']}`. Position ({f['x']}, {f['y']}). {f['days']} days.",f"Predecessors: {' AND '.join('('+ ' OR '.join(v)+')' for v in f['prerequisites'])or'None'}. Excludes: {', '.join(f['exclusive'])or'None'}."]
   if f['party_trigger']:lines+=[f"Party requirement: {f['required_party']} via `{f['party_trigger']} = yes`. Dated native party names apply."]
   if f['leader']:lines+=['Leader requirement: '+f['leader']+'.']
   if f['requirements']:lines+=['Requirements: '+f['requirements']]
   lines+=['',f['description'],'']
   if f['setup_gdp_percent']:lines+=[f"- Treasury: -{f['setup_gdp_percent']:g}% Greek GDP once"]
   if f['weekly_gdp_percent']:lines+=[f"- Weekly expense: +{f['weekly_gdp_percent']:g}% Greek GDP"]
   lines+=['- '+v for v in f['effect_lines']]
   if f.get('cleanup'):lines+=['','Lifecycle: '+f['cleanup']]
   if f.get('completion_guard'):lines+=['','Completion guard: '+f['completion_guard']]
   if f.get('weekly_lifetime'):lines+=['','Lifetime: '+f['weekly_lifetime']]
   lines+=['',f"Historical basis: [{SOURCES[f['source']]['title']}]({SOURCES[f['source']]['url']}).",'']
 lines+=['## Complete recipient-approved packages','','All packages below are proposed, not historical contract transcripts. Show all prospective terms in the originating focus and recipient decisions before acceptance, including while locked. Recipient decisions are the only new decision surface. Standing spirits have no fixed expiry.','']
 for key,o in d['offers'].items():
  lines+=['### '+o['name'],'',o['requirements'],'',o['acceptance'],'']
  for tag,s in o['sides'].items():
   lines += ['**'+COUNTRIES.get(tag,'Each actual Community member')+'**: '+(s['spirit']or s.get('label','')),'']
   basis='own GDP'if s['basis']=='own'else'Greek GDP'
   if s['setup_gdp_percent']:lines+=[f"- Treasury: -{s['setup_gdp_percent']:g}% of {basis} once"]
   if s.get('weekly_gdp_percent'):lines+=[f"- Weekly expense: +{s['weekly_gdp_percent']:g}% of {basis}"]
   if s.get('weekly_formula'):
    formula=s['weekly_formula'];lines+=[f"- Weekly expense: +{formula['per_recipient_gdp_percent']:g}% of Greek GDP per actual member; +{formula['preview_gdp_percent']:g}% for six members in the January 1970 preview."]
   if s['income_gdp_percent']:lines+=[f"- Weekly income: +{s['income_gdp_percent']:g}% of {basis}"]
   lines+=['- '+v for v in values(s['values'])]
   lines+=['- '+v for e in s['effects']for v in effects(e)]
   lines+=['']
  if o.get('native_membership_values'):lines+=['**Additional native EU_member base effects for Greece**','']+['- '+v for v in values(o['native_membership_values'])]+['',o['native_law_preview'],'',o['replaces'],'']
  if o.get('transaction'):lines+=['**Transaction**','']+[f"- {k}: {v}"for k,v in o['transaction'].items()]+['']
  if o.get('pending_state'):lines+=['**Pending and resumed ratification**','']+[f"- {k}: {v}"for k,v in o['pending_state'].items()]+['']
  if o.get('turkish_window'):lines+=['**Turkish reaction window**','']+[f"- {k}: {v}"for k,v in o['turkish_window'].items()]+['']
  if o.get('refusal'):lines+=['**If Cyprus refuses**','']+['- '+s for e in o['refusal']['effects']for s in effects(e)]+['']+[f"- {k}: {v}"for k,v in o['refusal'].items()if k!='effects']+['']
  lines+=[o['validity'],'',f"Historical precedent: [{SOURCES[o['basis']]['title']}]({SOURCES[o['basis']]['url']}).",'']
 lines+=['## Implementation and performance contract','']
 for k,v in d['implementation_contract'].items():lines+=['**'+k.replace('_',' ').capitalize()+'**: '+v,'']
 lines+=['## Fiscal revision','','Budget changes are proposed game balance. Native rates and stream gates still require implementation and engine testing. One-time crisis-helper overrides replace old fees rather than add another charge.','',d['fiscal_revision']['policy'],'']
 for f in d['focuses']:
  if f.get('budget_binding'):lines+=['- '+f['title']+': '+json.dumps(f['budget_binding'],ensure_ascii=False)]
 lines+=['','- Direct-entry expeditionary stream: '+json.dumps(d['fiscal_revision']['expeditionary_stream'],ensure_ascii=False),'','- Native Turkish stream guard: '+d['fiscal_revision']['native_turkish_stream'],'']
 lines+=['## Approval boundary','','Static graph, data, native API and geometry review establish a reviewable proposal. They do not establish in-game loading, native tooltips, volunteer compatibility or multiplayer execution. Those checks follow approved implementation. See RESEARCH_HISTORY.md, HISTORY_REVIEW.md, MD_REFERENCE_LAYOUT.md, COORDINATE_REVIEW.json and MECHANICS_REVIEW.md for independent evidence.']
 (OUT/'CONCEPT.md').write_text('\n'.join(lines)+'\n',encoding='utf8')

def main():
 d=prepare();report=audit(d)
 from fiscal import report as fiscal_report
 (OUT/'FISCAL_REVISION_CHECKS.json').write_text(json.dumps(fiscal_report(d),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 (OUT/'concept.json').write_text(json.dumps({k:v for k,v in d.items()if k!='images'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
 (OUT/'CONCEPT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
 document(d)
 # The complete data and literal template are the sole preview sources.
 template=(Path(__file__).parent/'preview.html').read_text('utf8')
 payload=json.dumps(d,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
 fragment=template.replace('/*__CONCEPT_DATA__*/',payload)
 assert len(fragment.encode('utf8'))<1000000
 VIS.write_text(fragment,encoding='utf8')
 print(json.dumps(dict(report,preview_bytes=len(fragment.encode('utf8'))),indent=2))

if __name__=='__main__':main()
