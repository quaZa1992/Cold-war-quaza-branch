"""COLDWAR_UAE approval concept. Writes design/preview files only; never loaded game files."""
from pathlib import Path
import json, sys, re, base64, io, hashlib
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
VIZ=Path('C:/Users/Enes/.codex/visualizations/2026/10/19/01a153f9-9c59-71b2-8460-d28a5d918d07')
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
sys.path.insert(0,str(ROOT/'tools/iraq_1970_concept'))
from native_font import GLYPHS,KERNINGS,ATLAS,raster,width

nodes=[]; groups=[]; decisions=[]
def ID(s): return 'COLDWAR_UAE_'+s
labels={
'political_power_factor':('Political power gain','percent'),
'stability_factor':('Stability','percent'),
'production_speed_buildings_factor':('Construction speed','percent'),
'production_speed_infrastructure_factor':('Infrastructure construction speed','percent'),
'production_speed_offices_factor':('Office construction speed','percent'),
'production_speed_naval_base_factor':('Naval base construction speed','percent'),
'production_speed_industrial_complex_factor':('Civilian factory construction speed','percent'),
'production_speed_arms_factory_factor':('Military factory construction speed','percent'),
'research_speed_factor':('Research speed','percent'),
'civilian_factories_productivity':('Civilian sector productivity','percent'),
'offices_productivity':('Office sector productivity','percent'),
'oil_export_multiplier_modifier':('Oil export revenue multiplier','percent'),
'education_cost_multiplier_modifier':('Education spending multiplier','percent'),
'bureaucracy_cost_multiplier_modifier':('Bureaucracy spending multiplier','percent'),
'army_personnel_cost_multiplier_modifier':('Military personnel spending multiplier','percent'),
'equipment_cost_multiplier_modifier':('Military equipment spending multiplier','percent'),
'health_cost_multiplier_modifier':('Health spending multiplier','percent'),
'energy_use_multiplier':('Energy consumption','percent'),
'fossil_pp_energy_generation_modifier':('Fossil power generation','percent'),
'energy_gain_multiplier':('Energy generation','percent'),
'country_productivity_growth_modifier':('Productivity growth multiplier','percent'),
'productivity_growth_modifier':('Productivity growth input','flat'),
'total_workforce_modifier':('Available workforce','percent'),
'buildings_worker_requirement_modifier':('Building workforce requirements','percent'),
'conscription_factor':('Recruitable population multiplier','percent'),
'interest_rate_multiplier_modifier':('Annual interest rate','pp'),
'return_on_investment_modifier':('Annual native investment return','fraction_pp'),
'imp_sanction_resistance':('Imperia sanction resistance','percent'),
'imp_oil_price_resistance':('Imperia consumer oil price resistance','percent'),
'imp_investment_in_extra':('Additional concurrent inward investments','integer'),
'army_org_factor':('Army organisation','percent'),
'training_time_factor':('Training time','percent'),
'supply_consumption_factor':('Supply consumption','percent'),
'industrial_capacity_factory':('Military factory output','percent'),
}
def fmt(k,v):
    label,unit=labels[k]
    val=(f'{v*100:+g}%' if unit=='percent' else f'{v:+g} percentage points' if unit=='pp' else f'{v*100:+g} percentage points' if unit=='fraction_pp' else f'{v:+g}')
    return f'{label}: {val}'

def group(key,label,origin,outlook='shared',gate='always = yes',status='Historical institutions / proposed policy balance'):
    groups.append(dict(id=key,label=label,origin=origin,outlook=outlook,gate=gate,status=status,
        ownership='Earned policy contributions are active only under the exact qualifying government; physical projects and one-time grants remain national.' if outlook!='shared' else 'Permanent national gains; institutional burdens are replaced through the stated reform. Temporary costs expire.'))

def add(key,title,group_key,xy,description,mods=None,pre=(),ex=(),days=35,cost=0,leaves='',rewards=(),gate='',status='',changes=(),temporary=0):
    g=next(g for g in groups if g['id']==group_key); mods=mods or {}
    available=g['gate']+ ('\n'+gate if gate else '')
    summary=list(rewards)+[fmt(k,v) for k,v in mods.items()]
    if cost: summary.append(f'Treasury: −${cost:g} billion (preparation / programme setup; queued buildings still require normal construction).')
    if changes: summary+=list(changes)
    if temporary: summary.append(f'The listed modifier contribution lasts {temporary} days; it does not renew on a government change.')
    body=[]
    if cost: body += [f'set_temp_variable = {{ treasury_change = -{cost:g} }}','modify_treasury_effect = yes']
    if leaves:body.append(leaves)
    if mods:
        body+=['# PROPOSED COLDWAR_UAE dynamic-modifier integration; these variable deltas require a registered consumer.']
        body += [f'add_to_variable = {{ COLDWAR_UAE_{key}_{k} = {v:g} }}' for k,v in mods.items()]
        body.append('COLDWAR_UAE_refresh_programmes = yes # NEW helper, not an existing MD API')
    if changes:body.append('# PROPOSED institutional replacement: '+ ' | '.join(changes))
    if cost: available+=f'\ncheck_variable = {{ treasury > {cost:g} }}'
    node=dict(id=ID(key),title=title,narrative_title=title,group=group_key,xy=[g['origin'][0]+xy[0],g['origin'][1]+xy[1]],
        days=days,cost=days/7,treasury_cost_billion=cost,prerequisites=[[ID(x) for x in row] for row in pre],mutually_exclusive=[ID(x) for x in ex],
        icon=ICON[group_key],description=description,reward_summary=summary,modifiers=mods,available=available,
        active_condition=g['gate']+ ('\n'+gate if gate else ''),requirement_contracts=[],
        historical_status=status or g['status'],effect_body='\n'.join(body),ownership=g['ownership'],starting_changes=list(changes),temporary_days=temporary)
    if cost:node['requirement_contracts'].append(dict(meaning='Affordability and current government are rechecked at completion. No negative treasury, automatic borrowing or lost payment if a project cannot be queued.',proposed_code='COLDWAR_UAE_complete_funded_focus = yes # proposed guarded transaction'))
    if 'add_building_construction' in leaves:node['requirement_contracts'].append(dict(meaning='Only the named owned and controlled UAE state, available building levels/slots and native project eligibility. Queue once; construction, workers and electricity remain required.',proposed_code='COLDWAR_UAE_validate_and_queue_project = yes # proposed guard; leaf below is native'))
    nodes.append(node);return key

ICON={'union':'union_negotiations','monarchy':'monarchism_constitution','constitutional':'Election_graphics','arab':'align_to_arab_league','left':'centralization','islah':'sunni_government','oil':'oil_production2','commerce':'liberalization','society':'focus_generic_education','defence':'navy2','diplomacy':'treaty2','british':'align_to_britain'}
def queue(state,kind):return f'{state} = {{ add_extra_state_shared_building_slots = 1\n add_building_construction = {{ type = {kind} level = 1 }} }} # queued, NOT instant'
def prod(points,state=None):return ((f'{state} = {{ ' if state else '')+f'set_temp_variable = {{ temp_productivity_change = {points} }}\n'+('state_flat_productivity_change_effect = yes }' if state else 'flat_productivity_change_effect = yes'))

group('union','Federation & British withdrawal',[0,0])
group('monarchy','The ruling-house bargain',[10,0],'nationalist','nationalist_monarchists_are_in_power = yes')
group('constitutional','Constitutional government · ALT',[20,0],'western','OR = { western_liberals_are_in_power = yes western_conservatism_are_in_power = yes }','Alternative government; constitutional questions have historical roots')
group('arab','Arab nationalist republic · ALT',[30,0],'emerging','OR = { emerging_autocracy_are_in_power = yes nationalist_military_junta_are_in_power = yes }','Alternative government; local Arab nationalism is historical, a republican takeover is not')
group('left','The social republic · ALT',[0,9],'emerging','OR = { emerging_communist_state_are_in_power = yes neutrality_neutral_social_are_in_power = yes }','Speculative alternative; no verified mass UAE communist party in January 1970')
group('islah','Sunni social reform · ALT',[10,9],'nonaligned','neutrality_neutral_muslim_brotherhood_are_in_power = yes\nhas_country_flag = COLDWAR_UAE_islah_organised','Islah association from 1974; its becoming a governing party is alternative history')
group('oil','Oil, sovereignty & savings',[20,9])
group('commerce','Dubai & the trading coast',[30,9])
group('society','Citizens, skills & public services',[0,18])
group('defence','A small state’s defence',[10,18])
group('diplomacy','A place in the Gulf',[20,18])
group('british','British protection & independence',[-8,0],gate='is_subject_of = ENG',status='Historical special treaty protection; continuation after1971 is an agreed alternative')

add('treaty_coast','The Protected Coast','british',(5,0),'The seven rulers govern their own sheikhdoms, while Britain conducts their external relations and carries defence responsibilities. A common liaison office can make this divided arrangement work more effectively.',{'bureaucracy_cost_multiplier_modifier':-.05},days=21,cost=.01,rewards=['Coordinate the existing protected-state administration; native MD subject rules continue to apply.'])
add('renew_protection','Renew the Protection','british',(3,1),'Some rulers would prefer continued British protection to facing stronger neighbours alone. London must decide whether it will revise its announced withdrawal policy and accept a renewed compact.',pre=[['treaty_coast']],ex=['petition_independence'],rewards=['Send Britain a proposal to continue special treaty protection. UK can accept, refuse or propose independent friendship.','The proposal grants no British money, troops or agreement by itself.'],days=35)
add('petition_independence','Prepare the Handover','british',(7,1),'Britain has already announced its withdrawal by the end of 1971. The rulers must prepare to assume responsibility for their external affairs and defence, while deciding which forms of British cooperation should continue after protection ends.',pre=[['treaty_coast']],ex=['renew_protection'],rewards=['Open negotiations for an earlier release and practical handover terms. The historical withdrawal is already scheduled at game start.','Neither this focus nor a new British approval is required for the normal historical release.'],days=35)
add('protected_administration','Shared Administration','british',(3,2),'With a renewed agreement in place, the rulers can extend common administrative and commercial institutions under British protection. This is internal cooperation, not a sovereign proclamation.',{'offices_productivity':.08,'bureaucracy_cost_multiplier_modifier':-.05},pre=[['renew_protection','petition_independence']],cost=.02,gate='has_country_flag = COLDWAR_UAE_protection_accepted',rewards=['Available after an accepted protection compact, including a later agreement reached after initial handover talks.'])
add('orderly_handover','An Orderly Handover','british',(7,2),'Once the country is independent, handover arrangements can organise stores, training and local responsibilities. Sovereignty has already changed through the existing withdrawal schedule or an accepted earlier release.',{'equipment_cost_multiplier_modifier':-.08},pre=[['renew_protection','petition_independence']],days=21,rewards=['Army experience: +15. Handover arrangements grant no new starting units.'],leaves='army_experience = 15',temporary=365)
add('british_training','British Training Teams','british',(2,3),'Training teams and common equipment standards can strengthen the small local forces. Maintaining the relationship still requires a professional establishment and expenditure.',{'training_time_factor':-.15,'equipment_cost_multiplier_modifier':-.05,'army_personnel_cost_multiplier_modifier':.08},pre=[['protected_administration']],ex=['british_commercial'],cost=.02,rewards=['Army experience: +15, once.'],leaves='army_experience = 15')
add('british_commercial','Commercial Partnership','british',(4,3),'Predictable British-linked commercial arrangements can draw firms and expertise to the coast. The rulers must maintain oversight and accept the continuing limits of protection.',{'offices_productivity':.12,'imp_investment_in_extra':1,'bureaucracy_cost_multiplier_modifier':.05},pre=[['protected_administration']],ex=['british_training'],cost=.03)
add('british_friendship','A Friendship Treaty','british',(7,3),'An independent federation can retain consultation, advisers and commercial links with Britain through a new agreement. Friendship does not recreate the old protected relationship or promise an unconditional defence guarantee.',{'research_speed_factor':.03,'offices_productivity':.06,'education_cost_multiplier_modifier':.05},pre=[['orderly_handover']],rewards=['Offer Britain an independent friendship and technical cooperation treaty. Listed programme contributions activate only after UK acceptance.','No subject relation, automatic faction, basing rights or military guarantee is granted.'])
add('enduring_protection','An Enduring Compact','british',(3,4),'A continuing protection arrangement needs funding, reliable local institutions and an understood division of responsibility. It can offer stability and credit while leaving external sovereignty constrained.',{'interest_rate_multiplier_modifier':-.50,'country_productivity_growth_modifier':.05,'political_power_factor':-.05},pre=[['british_training','british_commercial']],days=49,rewards=['Unlock a one-off British co-financing offer: UK may choose to pay$0.25bn to the UAE. Refusal pays nothing.','Maintain a collective Council or agreed protected administration; no automatic federal presidency on the historical character-expiry date.'])

# Ten federation focuses. One OR continuation preserves the consent-based nine-state alternative.
add('council','A Coast in Transition','union',(5,0),'The rulers possess courts, customs houses and forces of their own. The Council can coordinate development, but Britain’s announced departure makes an agreed political settlement urgent.',{'political_power_factor':.10,'bureaucracy_cost_multiplier_modifier':.05},days=21,rewards=['Unlock the Federation Negotiations and Political Organisation decisions.'])
add('development_fund','The Development Fund','union',(5,1),'Roads and clinics can give the smaller sheikhdoms a stake in cooperation before anyone settles the constitution.',{'production_speed_infrastructure_factor':.10},pre=[['council']],cost=.01,rewards=['Dubai state: +10 productivity points.'],leaves=prod(10,179))
add('seven_emirates','A Trucial Federation','union',(3,2),'An agreement among the Trucial rulers offers a more manageable union, while Bahrain and Qatar pursue their own futures.',{'stability_factor':.04},pre=[['development_fund']],ex=['nine_states'],rewards=['Negotiation scope: seven Trucial emirates; no annexation or free territory.','Founding settlement: reduce Fragmented Authority bureaucracy penalty by 5 percentage points.'])
add('nine_states','Keep Nine at the Table','union',(7,2),'Bahrain and Qatar remain possible partners. Representation, the capital and their rulers’ sovereignty must be settled through agreement.',{'bureaucracy_cost_multiplier_modifier':.05},pre=[['development_fund']],ex=['seven_emirates'],rewards=['Unlock separate Bahrain and Qatar offers. Acceptance by each player is required.','An accepted broad settlement adds +1 inward investment capacity; no acceptance means a seven-emirate fallback.'],status='Plausible diplomatic alternative; talks remained active during 1970')
add('charter','The Provisional Charter','union',(5,3),'The draft must make common government possible without pretending that the rulers have already surrendered their powers.',{'political_power_factor':.05},pre=[['seven_emirates','nine_states']],days=49,rewards=['Unlock the federal formation settlement and the two constitutional bargains below.','A separate northern-emirate consent ledger represents the emirates inside the existing two-state map.'])
add('dual_veto','The Dual Veto','union',(3,4),'Requiring Abu Dhabi and Dubai to agree protects the founding bargain. It also makes a common policy harder to impose.',{'stability_factor':.06,'bureaucracy_cost_multiplier_modifier':.08},pre=[['charter']],ex=['federal_ministries'],rewards=['Fragmented Authority: army organisation penalty reduced from −10% to −5%.','Unequal Development: construction penalty reduced from −12% to −6%.'])
add('federal_ministries','Common Ministries','union',(7,4),'A stronger federal budget promises more effective government. Smaller courts and Dubai’s merchants will expect guarantees in exchange.',{'political_power_factor':.10,'stability_factor':-.04},pre=[['charter']],ex=['dual_veto'],rewards=['Fragmented Authority: bureaucracy penalty reduced from +20% to +5%.','Unequal Development: construction penalty reduced from −12% to −6%.','Requires an accepted rulers’ compact; rejection leaves the proposal open, without a forced civil war.'])
add('sovereign_union','British Withdrawal','union',(5,5),'With the special treaty relationship ended and the coast independent, the consenting rulers can proclaim a sovereign federation. British release and federal formation are distinct decisions.',pre=[['dual_veto','federal_ministries']],days=21,gate='is_subject = no\nhas_country_flag = COLDWAR_UAE_founders_consented',rewards=['Requires actual independence from every overlord. A pending or refused UK request is insufficient.','Proclaim the sovereign federation; replace the interim Council with the agreed leadership, historically Zayed as President.','Establish UAE identity and the federation flag. British Treaty Dependence already deactivates on leaving British protection.'],status='Historical release1 December1971; sovereign UAE formation2 December1971')
add('rak_accession','The Seventh Emirate','union',(3,6),'Ras Al Khaimah’s security concerns and island claims require a place in the settlement, rather than an invisible territorial reward.',{'stability_factor':.03},pre=[['sovereign_union']],cost=.01,rewards=['Resolve Ras Al Khaimah accession through the emirate consent ledger.','Reduce Unequal Development stability penalty from −6% to −3%.'],status='Historical accession 10 February 1972')
add('federal_council','A National Council','union',(7,6),'An appointed consultative council gives the emirates a federal forum. Turning it into a sovereign elected legislature would be a further political choice.',{'bureaucracy_cost_multiplier_modifier':.03,'political_power_factor':.05},pre=[['sovereign_union']],rewards=['Unlock constitutional conventions through the existing party and outlook system.','Historical FNC remains consultative; this focus does not install parliamentary democracy.'])

# Eight-focus political diamonds. Substantive first focuses are already gated by the governing party.
add('majlis','The Rulers’ Majlis','monarchy',(5,0),'The dynasty can turn personal access to the rulers into a durable federal bargain. Listening to local notables takes time and resources.',{'stability_factor':.05,'bureaucracy_cost_multiplier_modifier':.04},days=21)
add('zayed_compact','Zayed’s Solidarity','monarchy',(3,1),'Abu Dhabi can spread oil-financed development beyond its own borders and make union valuable to the poorer emirates.',{'production_speed_infrastructure_factor':.15,'bureaucracy_cost_multiplier_modifier':.06},pre=[['majlis']],ex=['rashid_compact'],cost=.02,rewards=['Reduce the remaining Unequal Development construction penalty by 6 percentage points, to a floor of 0.'])
add('rashid_compact','Rashid’s Enterprise','monarchy',(7,1),'Dubai’s commercial institutions need room to operate. A bargain with its merchants attracts business while narrowing federal discretion.',{'offices_productivity':.12,'political_power_factor':-.05},pre=[['majlis']],ex=['zayed_compact'],cost=.02)
add('rulers_compact','Renew the Compact','monarchy',(5,2),'The union survives when transfers and autonomy are negotiated together. Neither leading emirate can govern the coast as a private estate.',{'stability_factor':.04},pre=[['zayed_compact','rashid_compact']],rewards=['Unlock 1976–79 constitutional mediation; an accepted settlement removes the remaining Unequal Development stability penalty.'])
add('gradual_union','An Agreed Union','monarchy',(3,3),'Joint procurement and shared institutions can expand without abolishing the ruling houses. Consensus remains a real constraint.',{'army_org_factor':.05,'bureaucracy_cost_multiplier_modifier':.05},pre=[['rulers_compact']],ex=['presidential_union'])
add('presidential_union','Executive Authority','monarchy',(7,3),'A more forceful presidency can press ministries to act. Emirate opposition must be managed through a negotiated delegation or a declared constitutional confrontation.',{'political_power_factor':.15,'stability_factor':-.06},pre=[['rulers_compact']],ex=['gradual_union'],rewards=['Unlock the Delegation of Powers offer; no automatic abolition of other monarchies.'])
add('civil_list','A Federal Civil List','monarchy',(5,4),'Clear obligations between court and ministry make the ruler’s promise more credible, at the price of maintaining a permanent federal apparatus.',{'country_productivity_growth_modifier':.05,'bureaucracy_cost_multiplier_modifier':.03},pre=[['gradual_union','presidential_union']],cost=.01)
add('succession_compact','Continuity by Consent','monarchy',(5,5),'A succession understood by the rulers protects the federation from becoming a contest over the whole state whenever one court changes hands.',{'stability_factor':.05},pre=[['civil_list']],days=49,rewards=['Unlock an agreed succession protocol using the existing leader system.','Political programme progress survives succession; office-specific benefits require the designated office.'])

add('constitutional_forum','An Open Federal Forum','constitutional',(5,0),'A governing constitutional coalition can begin opening the institutions that the founding charter left under the rulers’ supervision.',{'research_speed_factor':.03,'bureaucracy_cost_multiplier_modifier':.05},rewards=['Alternative government already rules; no additional party-unlock focus.'])
add('constitutional_crown','A Crown under Law','constitutional',(3,1),'Keep the ruling houses as constitutional partners while a responsible cabinet controls ordinary administration.',{'stability_factor':.08,'political_power_factor':-.05},pre=[['constitutional_forum']],ex=['citizen_republic'])
add('citizen_republic','A Citizen Republic','constitutional',(7,1),'An elected presidency could remove hereditary control of the executive. Founding courts would demand a serious settlement of authority and assets.',{'political_power_factor':.12,'stability_factor':-.06},pre=[['constitutional_forum']],ex=['constitutional_crown'],rewards=['Unlock a negotiated constitutional transition; no automatic seizure of emirate property.'])
add('public_accounts','Public Accounts','constitutional',(5,2),'Published federal accounts allow deputies and merchants to judge how the new government uses public money.',{'bureaucracy_cost_multiplier_modifier':-.07,'interest_rate_multiplier_modifier':-.25},pre=[['constitutional_crown','citizen_republic']],cost=.01)
add('citizen_ballot','Citizens’ Franchise','constitutional',(3,3),'A national electorate drawn from citizens can build a defensible constitutional bargain while leaving most expatriate residents outside it.',{'stability_factor':.06,'total_workforce_modifier':-.03},pre=[['public_accounts']],ex=['municipal_compact'])
add('municipal_compact','A Municipal Compact','constitutional',(7,3),'Advisory municipal representation for long-term residents can improve the trading cities without granting an instant national franchise.',{'offices_productivity':.10,'bureaucracy_cost_multiplier_modifier':.06},pre=[['public_accounts']],ex=['citizen_ballot'],rewards=['Unlock a staged residency and municipal participation law; citizenship remains a separate decision.'])
add('independent_courts','Independent Courts','constitutional',(5,4),'Commercial and administrative courts need trained judges and enforceable jurisdiction if constitutional promises are to change everyday government.',{'offices_productivity':.05,'bureaucracy_cost_multiplier_modifier':.04},pre=[['citizen_ballot','municipal_compact']],cost=.02)
add('responsible_cabinet','A Responsible Cabinet','constitutional',(5,5),'Parliamentary oversight can outlive the first reforming cabinet if ministries accept regular scrutiny and an orderly transfer of office.',{'country_productivity_growth_modifier':.08,'political_power_factor':-.04},pre=[['independent_courts']],days=49)

add('arab_awakening','The Arab Awakening','arab',(5,0),'Arab nationalist ideas reached the coast through teachers, broadcasting and regional politics. A republican government would have to build institutions beyond those networks.',{'political_power_factor':.08,'bureaucracy_cost_multiplier_modifier':.05},rewards=['No historical Baath party or republican majority is asserted. Saqr’s restoration episode is a separate crisis, not this government’s automatic origin.'])
add('civilian_arabism','A Civic Arabism','arab',(3,1),'Teachers and civil administrators can define the republic through Arab public education and shared institutions rather than permanent military supervision.',{'research_speed_factor':.06,'education_cost_multiplier_modifier':.08},pre=[['arab_awakening']],ex=['officers_republic'],gate='emerging_autocracy_are_in_power = yes')
add('officers_republic','The Officers’ Council','arab',(7,1),'A national command can provide discipline in a fragile republic. Its privileges impose a continuing cost and limit civilian authority.',{'army_org_factor':.10,'army_personnel_cost_multiplier_modifier':.12},pre=[['arab_awakening']],ex=['civilian_arabism'],gate='nationalist_military_junta_are_in_power = yes')
add('republican_service','A National Service','arab',(5,2),'A professional civil service can replace competing court offices without assuming that trained officials appear with a change of flag.',{'bureaucracy_cost_multiplier_modifier':-.05},pre=[['civilian_arabism','officers_republic']],cost=.02,rewards=['All controlled states: +10 productivity points.'],leaves=prod(10))
add('arab_solidarity','Arab Solidarity','arab',(3,3),'A regional development compact offers teachers, training and a stronger Arab voice. Partners must agree to the obligations and retain their sovereignty.',{'imp_sanction_resistance':.10,'offices_productivity':-.04},pre=[['republican_service']],ex=['sovereign_republic'],rewards=['Unlock an opt-in Arab technical cooperation offer; no automatic faction or annexation.'])
add('sovereign_republic','Our Own Republic','arab',(7,3),'Commercial independence can keep the republic from becoming a client of a larger Arab state, but it leaves defence more dependent on local resources.',{'offices_productivity':.10,'equipment_cost_multiplier_modifier':.06},pre=[['republican_service']],ex=['arab_solidarity'])
add('public_industry','A Public Industry','arab',(5,4),'A modest state industrial programme can create an alternative to oil rents. Buildings still need workers, power and a normal construction programme.',{'production_speed_industrial_complex_factor':.10,'energy_use_multiplier':.05},pre=[['arab_solidarity','sovereign_republic']],cost=.03,rewards=['Queue 1 civilian factory in Abu Dhabi; +1 shared building slot.'],leaves=queue(180,'industrial_complex'))
add('republican_charter','A Republican Charter','arab',(5,5),'A settled division between cabinet, command and local government gives the republic a chance to survive its founders.',{'stability_factor':.07,'bureaucracy_cost_multiplier_modifier':.04},pre=[['public_industry']],days=49)

add('social_compact','A Social Compact','left',(5,0),'A left-led government must reconcile national sovereignty with an economy sustained by oil, merchants and a large expatriate workforce.',{'total_workforce_modifier':.04,'bureaucracy_cost_multiplier_modifier':.05},rewards=['Alternative governing movement; this does not invent a historical UAE communist party.'])
add('social_ownership','Public Ownership','left',(3,1),'A communist cabinet can direct key enterprises toward a national plan, accepting the loss of private commercial initiative.',{'civilian_factories_productivity':.15,'offices_productivity':-.08},pre=[['social_compact']],ex=['social_market'],gate='emerging_communist_state_are_in_power = yes')
add('social_market','A Social Market','left',(7,1),'A non-aligned social government can leave the trading economy open while purchasing public services from its revenue.',{'offices_productivity':.12,'health_cost_multiplier_modifier':.08},pre=[['social_compact']],ex=['social_ownership'],gate='neutrality_neutral_social_are_in_power = yes')
add('labour_code','A Labour Code','left',(5,2),'Enforceable contracts and inspections can improve migrant workers’ bargaining position. Enforcement creates costs for employers and the state.',{'total_workforce_modifier':.05,'bureaucracy_cost_multiplier_modifier':.06},pre=[['social_ownership','social_market']],cost=.01)
add('universal_services','Universal Services','left',(3,3),'Residence-based access to basic services supports a stable workforce while greatly expanding the obligation of the small public administration.',{'total_workforce_modifier':.06,'health_cost_multiplier_modifier':.12},pre=[['labour_code']],ex=['citizen_dividend'])
add('citizen_dividend','A Citizens’ Dividend','left',(7,3),'Concentrating social entitlements on citizens builds a national constituency for reform, but leaves unequal access to public services.',{'stability_factor':.08,'total_workforce_modifier':-.03},pre=[['labour_code']],ex=['universal_services'],cost=.02)
add('technical_cadres','Technical Cadres','left',(5,4),'Scholarships and technical institutes can supply planners and engineers without treating foreign advisers as a permanent substitute for local expertise.',{'research_speed_factor':.06,'education_cost_multiplier_modifier':.08},pre=[['universal_services','citizen_dividend']],cost=.02,rewards=['Reduce Scarce Specialists research penalty by 5 percentage points.'])
add('social_charter','The Social Charter','left',(5,5),'A durable social settlement needs rules for funding, residency and public control that can survive more than one cabinet.',{'country_productivity_growth_modifier':.08,'bureaucracy_cost_multiplier_modifier':.03},pre=[['technical_cadres']],days=49)

# Six-focus Islah programme. Association history and government access are separate.
add('social_associations','Associations of Reform','islah',(5,0),'An Islah-led alternative grows from Sunni educational and charitable associations. Their historical existence does not imply an elected national mandate.',{'stability_factor':.05,'education_cost_multiplier_modifier':.05},rewards=['Government programme requires the association to have organised: historical context 1974, or a separately agreed early legalisation.'])
add('charitable_network','A Charitable Network','islah',(3,1),'Local charities can extend assistance through trusted institutions, while unequal provision makes federal oversight harder.',{'health_cost_multiplier_modifier':-.08,'bureaucracy_cost_multiplier_modifier':.05},pre=[['social_associations']],ex=['public_welfare'])
add('public_welfare','Public Welfare','islah',(7,1),'A common welfare administration gives reformers a national instrument but requires a larger and more expensive public service.',{'total_workforce_modifier':.05,'health_cost_multiplier_modifier':.10},pre=[['social_associations']],ex=['charitable_network'])
add('reform_education','Faith and Education','islah',(5,2),'Religious education and professional training need not be enemies. The governing movement must decide where independent institutions retain authority.',{'country_productivity_growth_modifier':.06,'education_cost_multiplier_modifier':.06},pre=[['charitable_network','public_welfare']],cost=.01)
add('consultative_reform','Consultative Reform','islah',(3,3),'A consultative civic pact preserves room for merchants and other associations, reducing the reform movement’s freedom to govern alone.',{'offices_productivity':.08,'political_power_factor':-.05},pre=[['reform_education']],ex=['clerical_supervision'])
add('clerical_supervision','Clerical Supervision','islah',(7,3),'A stronger religious council can unify social policy while deterring some outside business and political cooperation.',{'stability_factor':.08,'offices_productivity':-.06},pre=[['reform_education']],ex=['consultative_reform'])

add('concession_review','Review the Concessions','oil',(5,0),'Oil has made Abu Dhabi’s development possible, but contractual terms, technical expertise and ownership remain matters of negotiation.',{'oil_export_multiplier_modifier':.05},cost=.01,rewards=['Unlock concession talks; foreign equity transfers require an accepted contract.'])
add('oil_accounts','Develop the Fields','oil',(5,1),'Existing oil reserves need producing wells, gathering lines and trained crews before they can support the emirates’ ambitions. The first major capital programme expands Abu Dhabi’s modest operating capacity.',pre=[['concession_review']],cost=.75,days=70,rewards=['Abu Dhabi: +8 base oil; nominal UAE capacity 4 → 12.','This pays for operating extraction capacity, not the discovery of eight barrels or a percentage export bonus.'],leaves='180 = { add_resource = { type = oil amount = 8 } }')
add('state_participation','State Participation','oil',(3,2),'Larger public participation can capture more of the export margin while placing technical and financial risks on the producing emirate.',{'oil_export_multiplier_modifier':.15,'bureaucracy_cost_multiplier_modifier':.06},pre=[['oil_accounts']],ex=['partner_expertise'],cost=.04,rewards=['Unlock a negotiated participation contract; full benefit requires acceptance or a separately costed buyout.'])
add('partner_expertise','Retain the Partners','oil',(7,2),'Longer-term technical partnerships support more efficient operations, at the price of preserving the partners’ share of oil income.',{'country_productivity_growth_modifier':.08,'oil_export_multiplier_modifier':-.04},pre=[['oil_accounts']],ex=['state_participation'],cost=.02,rewards=['Abu Dhabi: +15 productivity points.'],leaves=prod(15,180))
add('onshore_expansion','Expand Onshore Output','oil',(3,3),'A second onshore programme extends producing fields and their pipelines. Its cost competes directly with schools, ports and the public budget, while the resulting receipts remain exposed to world oil prices.',pre=[['state_participation','partner_expertise']],cost=2.50,days=70,rewards=['Abu Dhabi: +10 base oil.','Available after either the state-equity or technical-services settlement; compatible with the offshore programme.'],leaves='180 = { add_resource = { type = oil amount = 10 } }')
add('offshore_expansion','Develop Offshore Oil','oil',(7,3),'Offshore production requires platforms, subsea connections and marine support. Abu Dhabi and Dubai can both expand, but the programme commits a much larger sum than the first onshore wells.',pre=[['state_participation','partner_expertise']],cost=5,days=105,rewards=['Abu Dhabi: +12 base oil; Dubai: +3 base oil.','Compatible with onshore expansion. Reserves and contract ownership are distinct from operating capacity.'],leaves='180 = { add_resource = { type = oil amount = 12 } }\n179 = { add_resource = { type = oil amount = 3 } }')
add('offshore_second_phase','Offshore Phase Two','oil',(9,4),'The next offshore phase expands the producing system rather than providing another cheap discovery. It ties up substantial capital and relies on the marine infrastructure established by the first programme.',pre=[['offshore_expansion']],cost=8,days=140,rewards=['Abu Dhabi: +7 base oil; Dubai: +3 base oil.','All four paid phases together restore nominal capacity to Abu Dhabi40 + Dubai7 =47, before native extraction modifiers or later depletion.'],leaves='180 = { add_resource = { type = oil amount = 7 } }\n179 = { add_resource = { type = oil amount = 3 } }')
add('oil_institutions','An Oil Administration','oil',(5,4),'Professional administration can make the producing emirates’ oil arrangements more predictable while maintaining their separate ownership.',{'bureaucracy_cost_multiplier_modifier':.03},pre=[['onshore_expansion','offshore_expansion']],rewards=['Unlock participation, development-transfer and export restraint decisions through the native oil system.'])
add('adia_savings','Save the Windfall','oil',(3,5),'An Abu Dhabi investment institution can turn exceptional oil receipts into a financial reserve and a professionally managed portfolio. These assets belong to Abu Dhabi unless a separate federal agreement is made.',{'interest_rate_multiplier_modifier':-.50,'return_on_investment_modifier':.005,'production_speed_buildings_factor':-.04},pre=[['oil_institutions']],ex=['domestic_windfall'],cost=.04,rewards=['Unlock funded reserve deposits and withdrawals, with principal recorded once.','The +0.5 percentage-point annual return applies only to separately funded native investments, subject to the native ROI cap. The cash-only reserve ledger earns no income.'],status='Historical institutional model: ADIA, 1976; this is not a federal wealth fund')
add('domestic_windfall','Spend on Development','oil',(7,5),'Using the windfall at home can accelerate physical development, while leaving fewer reserves for a downturn.',{'production_speed_buildings_factor':.12,'energy_use_multiplier':.08},pre=[['oil_institutions']],ex=['adia_savings'],cost=.04,rewards=['Unlock staged domestic development projects.'])
add('oil_shock_plan','Prepare for a Downturn','oil',(5,6),'Public plans must remain affordable when the oil market turns. Reserves can support the budget; diversified earnings can reduce its dependence on exports.',{'bureaucracy_cost_multiplier_modifier':-.04},pre=[['adia_savings','domestic_windfall']],rewards=['Unlock the 1986 oil downturn response. Oil-export revenue still follows native prices.','Reduce Narrow Revenue Base civilian productivity penalty by 5 percentage points; never substitute consumer oil-price resistance for export protection.'])

add('trading_coast','The Trading Coast','commerce',(5,0),'Dubai’s merchants built links across the Gulf before its oil exports began. Ports, courts and transport can give these networks a wider reach.',{'offices_productivity':.06},cost=.01)
add('port_planning','A Port Programme','commerce',(5,1),'Port Rashid and Jebel Ali answer different stages of Dubai’s growth. Capacity must be developed with real labour and infrastructure.',{'production_speed_naval_base_factor':.15,'bureaucracy_cost_multiplier_modifier':.03},pre=[['trading_coast']],cost=.02,rewards=['Unlock staged port and logistics projects. Abu Dhabi’s inherited level-10 port is not given an impossible extra level.'])
add('free_zone','A Free Zone','commerce',(3,2),'A separate commercial zone can attract foreign firms with predictable rules while surrendering part of the local tax take.',{'imp_investment_in_extra':1,'offices_productivity':.10,'bureaucracy_cost_multiplier_modifier':.05},pre=[['port_planning']],ex=['national_merchants'],cost=.03,status='Jafza institutional model, 1985; earlier completion is an explicit accelerated alternative')
add('national_merchants','Back Local Merchants','commerce',(7,2),'Credit and contracts reserved for established local businesses can deepen national ownership, while limiting the scale of foreign participation.',{'offices_productivity':.15,'country_productivity_growth_modifier':-.03},pre=[['port_planning']],ex=['free_zone'],cost=.03)
add('logistics_corridor','A Logistics Corridor','commerce',(3,3),'Efficient customs and reliable connections matter as much as quays. The free zone needs a functioning transport economy around it.',{'production_speed_infrastructure_factor':.10,'energy_use_multiplier':.04},pre=[['free_zone']],cost=.02,rewards=['Queue 1 office in Dubai; +1 shared building slot.'],leaves=queue(179,'offices'))
add('merchant_credit','Merchant Credit','commerce',(7,3),'A more disciplined local credit system can finance trade while requiring the public authorities to scrutinise business risk.',{'interest_rate_multiplier_modifier':-.25,'bureaucracy_cost_multiplier_modifier':.04},pre=[['national_merchants']],cost=.02,rewards=['Dubai: +15 productivity points.'],leaves=prod(15,179))
add('commercial_courts','Commercial Courts','commerce',(5,4),'Reliable contracts can link Dubai’s ambitions to a wider federation while preserving the emirates’ distinct commercial jurisdictions.',{'offices_productivity':.05,'bureaucracy_cost_multiplier_modifier':.03},pre=[['logistics_corridor','merchant_credit']],cost=.01,rewards=['Reduce Narrow Revenue Base office productivity penalty from −10% to −5%.'])
add('aviation_hub','An Aviation Hub','commerce',(3,5),'An airline can connect trade and visitors to the coast, but aircraft leases, trained crews and operating costs make it a serious commercial undertaking.',{'offices_productivity':.10,'energy_use_multiplier':.06},pre=[['commercial_courts']],ex=['industrial_port'],cost=.03,rewards=['Unlock a funded civil airline venture; no combat aircraft or free airbase.'],status='Emirates institutional model, 1985; this is a civil transport programme')
add('industrial_port','An Industrial Port','commerce',(7,5),'Repair yards and light industry can add production to the trade economy, with larger demands on electricity and workers.',{'production_speed_industrial_complex_factor':.12,'energy_use_multiplier':.08},pre=[['commercial_courts']],ex=['aviation_hub'],cost=.03,rewards=['Queue 1 civilian factory in Dubai; +1 shared building slot.'],leaves=queue(179,'industrial_complex'))
add('beyond_oil','Earnings beyond Oil','commerce',(5,6),'A broader base of service and industrial income leaves the country better placed to absorb an oil slump. It does not stop the world price from falling.',{'offices_productivity':.05},pre=[['aviation_hub','industrial_port']],days=49,rewards=['Remove the remaining Narrow Revenue Base office productivity penalty.','Reduce Narrow Revenue Base civilian productivity penalty by 5 percentage points, to a floor of 0.','Unlock the optional 1990s tourism and logistics continuation; no Burj Al Arab or 2005 aircraft in the Cold War rewards.'])

add('schools_clinics','Schools and Clinics','society',(5,0),'The coast needs teachers, nurses and technicians as urgently as it needs buildings. New public services carry continuing obligations.',{'education_cost_multiplier_modifier':.05,'health_cost_multiplier_modifier':.05},cost=.01,rewards=['All controlled states: +10 productivity points.'],leaves=prod(10))
add('national_training','Train Citizens','society',(3,1),'Training nationals takes time but can reduce dependence on imported expertise and support a locally staffed administration.',{'research_speed_factor':.05,'education_cost_multiplier_modifier':.08},pre=[['schools_clinics']],ex=['foreign_specialists'],cost=.02,rewards=['Reduce Scarce Specialists research penalty from −10% to −5%.'])
add('foreign_specialists','Invite Specialists','society',(7,1),'International recruitment can relieve immediate shortages while increasing housing demand and the reliance on a mobile expatriate population.',{'total_workforce_modifier':.10,'bureaucracy_cost_multiplier_modifier':.06},pre=[['schools_clinics']],ex=['national_training'],cost=.02,rewards=['Reduce Scarce Specialists workforce penalty from −8% to −3%.'])
add('water_network','Water for the Towns','society',(5,2),'Desalination and distribution can make expanding coastal towns liveable, at a cost in power and skilled maintenance.',{'energy_use_multiplier':.06,'production_speed_infrastructure_factor':.10},pre=[['national_training','foreign_specialists']],cost=.03,rewards=['Replace Water and Power Constraints: energy penalty +15% → +5%; civilian productivity penalty −5% → 0.','Desalination has no invented building type: use native energy/infrastructure projects.'])
add('citizen_housing','Homes for Citizens','society',(3,3),'Public housing for citizens can strengthen support for the federation while leaving the trading cities’ migrant housing problem to employers and local authorities.',{'stability_factor':.07,'bureaucracy_cost_multiplier_modifier':.05},pre=[['water_network']],ex=['worker_towns'],cost=.02)
add('worker_towns','Housing the Workforce','society',(7,3),'Planned workforce accommodation can support a more stable labour supply but requires permanent inspection and public services.',{'total_workforce_modifier':.06,'health_cost_multiplier_modifier':.07},pre=[['water_network']],ex=['citizen_housing'],cost=.02)
add('technical_institutes','Technical Institutes','society',(5,4),'Universities and technical institutes can supply the skills a growing federation needs. Laboratories and teachers must be maintained after the opening ceremony.',{'productivity_growth_modifier':.20,'education_cost_multiplier_modifier':.08},pre=[['citizen_housing','worker_towns']],cost=.02,rewards=['Remove the remaining Scarce Specialists research penalty.','National Training route: also remove the −8% specialist workforce penalty; Invite Specialists route: remaining −3% becomes 0.'])
add('efficient_services','Services That Endure','society',(5,5),'Professional management can help public services keep pace with rapid growth. The goal is a functioning state, rather than an unlimited oil-financed payroll.',{'buildings_worker_requirement_modifier':-.08,'bureaucracy_cost_multiplier_modifier':.03},pre=[['technical_institutes']],days=49,cost=.02)

add('security_handover','The Security Handover','defence',(5,0),'The end of British protection leaves a small population and distinct emirate forces facing powerful neighbours. Coordination matters before prestige purchases.',{'training_time_factor':-.05,'army_personnel_cost_multiplier_modifier':.05},rewards=['Unlock training and procurement negotiations; starting units and equipment remain outside this concept.'])
add('force_register','One Force Register','defence',(5,1),'A common register of personnel, stores and contracts is the first step toward a force that the federation can actually sustain.',{'equipment_cost_multiplier_modifier':-.05,'bureaucracy_cost_multiplier_modifier':.04},pre=[['security_handover']],cost=.01)
add('union_command','A Union Command','defence',(3,2),'A shared chain of command can improve readiness, at the price of a larger standing federal organisation.',{'army_org_factor':.10,'army_personnel_cost_multiplier_modifier':.10},pre=[['force_register']],ex=['emirate_commands'],gate='has_country_flag = COLDWAR_UAE_federation_established',rewards=['Remove Fragmented Authority army organisation penalty.'],status='Historical legal union 6 May 1976; full integration remains a programme')
add('emirate_commands','Coordinated Commands','defence',(7,2),'The emirates can retain local commands while standardising procedures. This protects autonomy but preserves duplication in personnel and administration.',{'training_time_factor':-.10,'bureaucracy_cost_multiplier_modifier':.08},pre=[['force_register']],ex=['union_command'],rewards=['Fragmented Authority army organisation penalty reduced to −3%, rather than removed.'])
add('shared_logistics','Shared Logistics','defence',(3,3),'Compatible depots, transport and communications allow a unified command to operate without importing a large foreign army.',{'supply_consumption_factor':-.08,'equipment_cost_multiplier_modifier':.04},pre=[['union_command']],cost=.02)
add('common_standards','Common Standards','defence',(7,3),'Standard equipment and training can make autonomous forces cooperate, even while their commanders remain answerable to different rulers.',{'equipment_cost_multiplier_modifier':-.08,'army_personnel_cost_multiplier_modifier':.04},pre=[['emirate_commands']],cost=.02)
add('defence_staff','A Defence Staff','defence',(5,4),'A permanent staff can translate the federation’s limited resources into realistic operational plans.',{'army_org_factor':.05,'bureaucracy_cost_multiplier_modifier':.03},pre=[['shared_logistics','common_standards']],rewards=['Army experience: +15.'],leaves='army_experience = 15')
add('air_coastal_shield','An Air-Coastal Shield','defence',(3,5),'Surveillance, air defence and maritime training address the coast’s vulnerabilities with a small professional force. Imported systems bring costs and external dependence.',{'army_org_factor':.05,'equipment_cost_multiplier_modifier':.10},pre=[['defence_staff']],ex=['land_deterrent'],cost=.02,rewards=['Unlock recipient-approved training and era-appropriate procurement offers.','Air experience: +10; Navy experience: +10. No free F-16 Block 60.'],leaves='air_experience = 10\nnavy_experience = 10')
add('land_deterrent','A Mobile Deterrent','defence',(7,5),'A compact mobile land force can protect key routes and facilities, while consuming a larger share of the federation’s scarce personnel.',{'army_org_factor':.10,'army_personnel_cost_multiplier_modifier':.12},pre=[['defence_staff']],ex=['air_coastal_shield'],cost=.02,rewards=['Army experience: +20.','Unlock a funded maintenance workshop project; no automatic armoured divisions.'],leaves='army_experience = 20')
add('sustainable_force','A Sustainable Force','defence',(5,6),'Maintenance, training and a realistic establishment matter more than a paper arsenal. The federation must be able to operate what it buys.',{'equipment_cost_multiplier_modifier':-.06},pre=[['air_coastal_shield','land_deterrent']],days=49,cost=.02,rewards=['Unlock periodic training decisions with explicit costs and cooldowns; no repeated focus grants.'])

add('gulf_diplomacy','Gulf Diplomacy','diplomacy',(5,0),'A small state needs recognised borders and working relationships as much as it needs arms. Disputes and trade can exist in the same relationship.',{'bureaucracy_cost_multiplier_modifier':.03},days=21,rewards=['Unlock British withdrawal, Saudi border, islands and regional cooperation offers.','An offer never compels another human player to accept.'])
add('gulf_contacts','Open the Channels','diplomacy',(5,1),'Missions and bilateral contacts allow the federation to work with Britain, Arab neighbours, Iran and both Cold War blocs without automatically joining any of them.',{'offices_productivity':.03},pre=[['gulf_diplomacy']],cost=.01,rewards=['Unlock diplomatic missions and technical exchanges; no ideology conversion.'])
add('western_security','Western Security Links','diplomacy',(3,2),'British and Western advisers can help sustain a professional force while maintaining an expensive reliance on imported equipment.',{'training_time_factor':-.08,'equipment_cost_multiplier_modifier':.08},pre=[['gulf_contacts']],ex=['armed_nonalignment'],rewards=['Unlock opt-in British / US training contracts. Separate base rights require an explicit agreement.'])
add('armed_nonalignment','Armed Non-Alignment','diplomacy',(7,2),'Buying and trading across blocs can reduce dependence on any single patron, at the price of a more complicated support system.',{'imp_sanction_resistance':.10,'equipment_cost_multiplier_modifier':.10},pre=[['gulf_contacts']],ex=['western_security'],rewards=['Unlock opt-in multi-supplier contracts; compatibility and export approval remain required.'])
add('security_contracts','Training Agreements','diplomacy',(3,3),'Training relationships are useful when they supply real skills and clear obligations, rather than an assumed foreign guarantee.',pre=[['western_security']],rewards=['Accepted partner contract: +15 Army experience and −5% training time for 730 days; UAE pays 2% of offer-date GDP.','Rejected offer: no payment, no benefit; try another eligible partner after 180 days.'])
add('technical_exchange','Across the Blocs','diplomacy',(7,3),'Technical exchanges can support development while leaving the federation free to pursue its own diplomacy.',pre=[['armed_nonalignment']],rewards=['Accepted exchange: all controlled states +10 productivity; UAE pays 2% of offer-date GDP; partner chooses acceptance.','Foreign benefits never fire from this focus alone.'])
add('gulf_cooperation','Gulf Cooperation','diplomacy',(5,4),'Common standards and consultation can make the Gulf more secure and prosperous. The GCC is more than a unilateral anti-Iran military bloc.',{'offices_productivity':.04,'bureaucracy_cost_multiplier_modifier':.04},pre=[['security_contracts','technical_exchange']],gate='has_country_flag = COLDWAR_UAE_federation_established',rewards=['Unlock a multilateral GCC proposal through the existing regional framework; each participant consents.','Historical charter: 25 May 1981. An earlier charter is an agreed alternative; no automatic faction.'])
add('islands_arbitration','Seek an Island Accord','diplomacy',(3,5),'Abu Musa’s arrangement and the Tunbs dispute cannot be settled by the same formula. A negotiated accord may preserve trade while limiting immediate ambitions.',{'offices_productivity':.07,'political_power_factor':-.04},pre=[['gulf_cooperation']],ex=['islands_claim'],rewards=['Unlock an Iran offer: arbitration, access and trade commitments negotiated separately.','No automatic surrender of claims, Iranian payment, non-aggression pact or territorial transfer.'])
add('islands_claim','Maintain the Claims','diplomacy',(7,5),'The federation can keep the islands at the centre of its diplomacy while accepting tension with a much stronger neighbour.',{'army_org_factor':.04,'offices_productivity':-.04},pre=[['gulf_cooperation']],ex=['islands_arbitration'],rewards=['Unlock diplomatic pressure and monitored maritime incidents; no free conquest goal.','Any military escalation remains an explicit player choice with normal war rules.'])
add('gulf_crisis','The Gulf Crisis','diplomacy',(5,6),'An Iraqi invasion of Kuwait would force the federation to weigh coalition support against the risks of exposure. Without that crisis, civil protection remains useful.',{'imp_sanction_resistance':.05,'bureaucracy_cost_multiplier_modifier':.03},pre=[['islands_arbitration','islands_claim']],days=49,rewards=['Unlock coalition support only if Kuwait is invaded; separate funding, transit and military participation options.','Otherwise unlock civil contingency planning. No fixed 1990 war is forced.'])

# Independent revision after source, history and layout review.
bykey={n['id'].removeprefix('COLDWAR_UAE_'):n for n in nodes}
bykey['dual_veto']['title']='Emirate Guarantees'
bykey['dual_veto']['description']='All viable federal charters need common ministries and recognise the leading emirates. Prioritising entrenched emirate guarantees follows the historical bargain, while keeping federal coordination expensive.'
bykey['federal_ministries']['title']='A Stronger Mandate'
bykey['federal_ministries']['description']='Ministries already belong in the charter. A stronger federal mandate asks the rulers to delegate more authority than in the historical bargain, in exchange for clear limits and shared development.'
bykey['state_participation']['title']='Buy a Larger Share'
bykey['state_participation']['description']='The producing emirate can seek a larger equity share while retaining foreign technical partners, as historical participation arrangements did. The choice is how much ownership risk to assume, not whether foreigners may remain.'
bykey['partner_expertise']['title']='Service Guarantees'
bykey['partner_expertise']['description']='Prioritising technical-service guarantees and management expertise preserves more of the partners’ commercial margin. It does not rule out state participation in the concession.'
bykey['citizen_ballot']['title']='Citizen Preference'
bykey['citizen_ballot']['description']='Citizen elections can coexist with municipal consultation. This policy instead reserves a larger share of jobs and residency opportunities for citizens, strengthening their political stake while reducing access to migrant labour.'
bykey['municipal_compact']['title']='A Resident Compact'
bykey['municipal_compact']['description']='Citizen elections remain possible. This alternative prioritises long-term residency and advisory municipal participation for expatriates, sustaining the trading economy while expanding the work of local administration.'

# Keep the island dispute independently reachable in 1971, before a GCC charter.
for k,x in [('islands_arbitration',11),('islands_claim',13)]:
    bykey[k]['xy']=[20+x,20]
    bykey[k]['prerequisites']=[[ID('gulf_contacts')]]
bykey['gulf_crisis']['xy']=[29,23]
bykey['gulf_crisis']['prerequisites']=[[ID('gulf_cooperation')],[ID('islands_arbitration'),ID('islands_claim')]]
# Tighten simple native policy diamonds to two-grid spacing; delivery forks keep room.
for g in ['monarchy','constitutional','left','islah']:
    origin=next(x['origin'][0] for x in groups if x['id']==g)
    for n in nodes:
        if n['group']==g and n['xy'][0] in [origin+3,origin+7]:n['xy'][0]=origin+(4 if n['xy'][0]==origin+3 else 6)

add('dirham','A Common Currency','union',(5,7),'Abu Dhabi uses the Bahraini dinar while the other emirates use the Qatar–Dubai riyal. A currency board and common dirham can simplify federal accounts and trade without creating oil wealth by decree.',{'offices_productivity':.04,'interest_rate_multiplier_modifier':-.25,'bureaucracy_cost_multiplier_modifier':.03},pre=[['rak_accession'],['federal_council']],cost=.02,days=49,rewards=['Create a proposed COLDWAR_UAE domestic Dirham identity and Currency Board, following the project’s domestic-currency extension pattern. No reserve-currency issuer or exchange-rate bonus.'],status='Historical Currency Board and dirham, 1973; earlier completion is an agreed institutional alternative')

# Explicit, structured spirit replacement contract. These are proposed operations,
# not claimed existing APIs. A compiler must consume them only after approval.
remedies={
'seven_emirates':[('fragmented_authority','bureaucracy_cost_multiplier_modifier','reduce',.05,0)],
'dual_veto':[('fragmented_authority','army_org_factor','set',-.05,0),('unequal_development','production_speed_buildings_factor','set',-.06,0)],
'federal_ministries':[('fragmented_authority','bureaucracy_cost_multiplier_modifier','set',.05,0),('unequal_development','production_speed_buildings_factor','set',-.06,0)],
'rak_accession':[('unequal_development','stability_factor','set',-.03,0)],
'zayed_compact':[('unequal_development','production_speed_buildings_factor','reduce_penalty',.06,0)],
'national_training':[('scarce_specialists','research_speed_factor','set',-.05,0)],
'foreign_specialists':[('scarce_specialists','total_workforce_modifier','set',-.03,0)],
'technical_cadres':[('scarce_specialists','research_speed_factor','reduce_penalty',.05,0)],
'technical_institutes':[('scarce_specialists','research_speed_factor','set',0,0),('scarce_specialists','total_workforce_modifier','set',0,0)],
'water_network':[('water_power','energy_use_multiplier','set',.05,0),('water_power','civilian_factories_productivity','set',0,0)],
'commercial_courts':[('narrow_revenues','offices_productivity','set',-.05,0)],
'beyond_oil':[('narrow_revenues','offices_productivity','set',0,0),('narrow_revenues','civilian_factories_productivity','reduce_penalty',.05,0)],
'oil_shock_plan':[('narrow_revenues','civilian_factories_productivity','reduce_penalty',.05,0)],
'union_command':[('fragmented_authority','army_org_factor','set',0,0)],
'emirate_commands':[('fragmented_authority','army_org_factor','set',-.03,0)],
}
for n in nodes:
    key=n['id'].removeprefix('COLDWAR_UAE_')
    n['spirit_changes']=[dict(spirit=ID(s),component=k,operation=op,value=v,floor=f) for s,k,op,v,f in remedies.get(key,[])]
    n['starting_changes']=n['spirit_changes']
    if n['spirit_changes']:n['effect_body']+='\n# PROPOSED persistent starting-spirit operations:\n'+json.dumps(n['spirit_changes'],indent=2)
    n['conditional_contributions']=[]
    if key=='state_participation':
        n['active_condition']='has_country_flag = COLDWAR_UAE_oil_participation_accepted'
        n['conditional_contributions']=[dict(condition=n['active_condition'],modifiers=n['modifiers'])]
        n['reward_summary']=[s.replace('Oil export revenue multiplier: +15%','After accepted equity contract — Oil export revenue multiplier: +15%').replace('Bureaucracy spending multiplier: +6%','After accepted equity contract — Bureaucracy spending multiplier: +6%') for s in n['reward_summary']]
        n['effect_body']+='\n# The contributions above are stored as earned, but their dynamic modifier is ENABLED ONLY by COLDWAR_UAE_oil_participation_accepted.'
    if key=='nine_states':
        n['conditional_contributions']=[dict(condition='has_country_flag = COLDWAR_UAE_broad_charter_accepted',modifiers={'imp_investment_in_extra':1})]
        n['effect_body']+='\n# PROPOSED accepted broad-charter dynamic modifier: imp_investment_in_extra = 1; never on offer alone.'
    if key in ['charter','federal_ministries','dual_veto']:
        n['requirement_contracts'].append(dict(meaning='Charter terms are resolved by the Founders’ Settlement decision. The institutional bargain is binding only when all represented founding rulers consent.',proposed_code='has_country_flag = COLDWAR_UAE_founders_consented # set by an accepted Founders Settlement'))
    if key in ['federal_ministries','dual_veto']:
        n['available']+='\nhas_country_flag = COLDWAR_UAE_founders_consented'
        n['available']+='\nhas_country_flag = COLDWAR_UAE_'+('mandate_agreed' if key=='federal_ministries' else 'guarantees_agreed')
    if key in ['security_contracts','technical_exchange']:
        n['effect_body']='unlock_decision_tooltip = '+ID('decision_training_offer' if key=='security_contracts' else 'decision_exchange_offer')+' # NEW decision defined in this concept'
    n['narrative_title']=n['title']

# Component remedies are evaluated from immutable starting values, never applied
# by reading-and-writing the current spirit. Additive credits may combine across
# programmes; alternative stages in one family contribute only the strongest.
for n in nodes:
    for r in n['spirit_changes']:
        k=n['id'].removeprefix('COLDWAR_UAE_')
        r['owner_focus']=n['id']
        r['family']='army_integration' if r['component']=='army_org_factor' else 'administration_integration' if k in ['seven_emirates','federal_ministries'] and r['component']=='bureaucracy_cost_multiplier_modifier' else k
        r['evaluation']='strongest_in_family_then_sum_credits_from_original_component_clamp_at_zero'
    if n['spirit_changes']:
        a=n['effect_body'].index('# PROPOSED persistent starting-spirit operations:')
        n['effect_body']=n['effect_body'][:a]+'# PROPOSED persistent starting-spirit operations (recomputed from original values; order independent):\n'+json.dumps(n['spirit_changes'],indent=2)

# Art choices refined from the inspected native icon set.
for n in nodes:
    if n['id']==ID('water_network'): n['icon']='desalination_plants'
    if n['id']==ID('aviation_hub'):n['icon']='build_airport'
    if n['id'] in [ID('schools_clinics'),ID('universal_services')]:n['icon']='generic_healthcare'
    if n['id'] in [ID('technical_institutes'),ID('technical_cadres')]:n['icon']='scientific_exchange'
    if n['id']==ID('armed_nonalignment'):n['icon']='neutrality'
art_by_focus={
'council':'government_beu','development_fund':'construction_engineering','charter':'monarchism_constitution','dual_veto':'monarchism_constitution','federal_ministries':'centralization','sovereign_union':'global_community','rak_accession':'treaty2','federal_council':'self_management','dirham':'money',
'majlis':'government_beu','zayed_compact':'construction_engineering','rashid_compact':'liberalization','rulers_compact':'treaty2','gradual_union':'union_negotiations','presidential_union':'centralization','civil_list':'money','succession_compact':'monarchism_constitution',
'constitutional_forum':'self_management','constitutional_crown':'monarchism_constitution','citizen_republic':'government_beu','public_accounts':'money','citizen_ballot':'Election_graphics','municipal_compact':'global_community','independent_courts':'focus_generic_court','responsible_cabinet':'self_management',
'arab_awakening':'align_to_arab_league','civilian_arabism':'focus_generic_education','officers_republic':'general_staff','republican_service':'government_beu','arab_solidarity':'global_community','sovereign_republic':'neutrality','public_industry':'construction_engineering','republican_charter':'self_management',
'social_compact':'union_negotiations','social_ownership':'centralization','social_market':'decentralized_economy','labour_code':'union_negotiations','universal_services':'generic_healthcare','citizen_dividend':'money','social_charter':'government_beu',
'charitable_network':'generic_healthcare','public_welfare':'government_beu','reform_education':'focus_generic_education','consultative_reform':'self_management',
'concession_review':'oil_companies','oil_accounts':'resource_extraction','state_participation':'oil_companies','partner_expertise':'scientific_exchange','onshore_expansion':'oil_production2','offshore_expansion':'focus_generic_offshore_oil_rig','offshore_second_phase':'oil_red','oil_institutions':'government_beu','adia_savings':'gold_standard','domestic_windfall':'construction_engineering','oil_shock_plan':'money',
'trading_coast':'naval_industry','port_planning':'naval_dockyard','free_zone':'liberalization','national_merchants':'decentralized_economy','logistics_corridor':'naval_industry','merchant_credit':'money','commercial_courts':'focus_generic_court','industrial_port':'construction_engineering','beyond_oil':'global_community',
'national_training':'focus_generic_education','foreign_specialists':'scientific_exchange','citizen_housing':'construction_engineering','worker_towns':'generic_housing','efficient_services':'government_beu',
'security_handover':'military_mission','force_register':'general_staff','union_command':'general_staff','emirate_commands':'recruitment','shared_logistics':'construction_engineering','common_standards':'military_mission','defence_staff':'general_staff','air_coastal_shield':'navy2','land_deterrent':'military_mission','sustainable_force':'general_staff',
'gulf_diplomacy':'global_community','gulf_contacts':'treaty2','western_security':'military_mission','security_contracts':'military_mission','technical_exchange':'scientific_exchange','gulf_cooperation':'gcc','islands_arbitration':'treaty2','islands_claim':'navy2','gulf_crisis':'general_staff',
}
for n in nodes:
    key=n['id'].removeprefix('COLDWAR_UAE_')
    if key in art_by_focus:n['icon']=art_by_focus[key]

# Low-oil start and expensive native extraction programmes; design data only.
oil_start={
    'label':'Limited Operating Oil Capacity',
    'existing_base':{'179':7,'180':40},'proposed_base':{'179':1,'180':3},
    'total_existing':47,'total_proposed':4,'reduction_percent':round((1-4/47)*100,2),
    'source_contract':'Validate the audited raw Dubai7 / AbuDhabi40 snapshot before applying the one-off reductions. No monthly resource reset.',
    'setup_order':'New1970 campaign only: apply low-oil deltas BEFORE the existing1970 GDP calibration freezes its accounting offset. Retain the authored0.686bn GDP snapshot, fewer actual export units and less oil export cash. Never recalibrate after investment.',
    'one_time_flag':ID('low_oil_start_applied'),
    'proposed_effect_body':'# NEW1970 setup integration, BEFORE frozen GDP calibration; expected raw resources verified at compile time.\nif = {\n limit = {\n  original_tag = UAE\n  IMP_is_1970_scenario = yes\n  date < 1971.1.1\n  NOT = { has_country_flag = IMP_1970_gdp_profile_applied }\n  NOT = { has_country_flag = COLDWAR_UAE_low_oil_start_applied }\n  179 = { is_owned_by = ROOT is_controlled_by = ROOT }\n  180 = { is_owned_by = ROOT is_controlled_by = ROOT }\n }\n 179 = { add_resource = { type = oil amount = -6 } }\n 180 = { add_resource = { type = oil amount = -37 } }\n set_country_flag = COLDWAR_UAE_low_oil_start_applied\n ingame_update_setup = yes\n}',
    'scope':'Base units represent operating capacity, not geological reserves or a historical barrels/day estimate. Technology, infrastructure, native prices and depletion remain active.'
}
oil_phases=[
    dict(focus=ID('oil_accounts'),phase=1,treasury_billion=.75,days=70,resources={'180':8},cumulative_base=12),
    dict(focus=ID('onshore_expansion'),phase=2,treasury_billion=2.5,days=70,resources={'180':10},cumulative_base=22),
    dict(focus=ID('offshore_expansion'),phase=3,treasury_billion=5,days=105,resources={'180':12,'179':3},cumulative_base=37),
    dict(focus=ID('offshore_second_phase'),phase=4,treasury_billion=8,days=140,resources={'180':7,'179':3},cumulative_base=47),
]
for phase in oil_phases:
    n=next(n for n in nodes if n['id']==phase['focus']);flag=n['id']+'_paid'
    scope_guards=[f'{s} = {{ is_owned_by = ROOT is_controlled_by = ROOT }}' for s in phase['resources']]
    funds=f'check_variable = {{ var = treasury value = {phase["treasury_billion"]:g} compare = greater_than_or_equals }}'
    guards=[funds,f'NOT = {{ has_country_flag = {flag} }}']+scope_guards
    n['available']='always = yes\n'+'\n'.join(guards)
    n['one_time_delivery_flag']=flag
    n['resource_changes']=[dict(state=int(s),resource='oil',base_amount=amount) for s,amount in phase['resources'].items()]
    n['reward_summary']=[s for s in n['reward_summary'] if not s.startswith('Treasury:')]+[
        f'Treasury: −${phase["treasury_billion"]:g} billion in full field-development capital expenditure; paid once.',
        'No automatic borrowing. Existing native loans or negotiated player financing may fund the investment.',
        'World prices and actual export demand determine receipts; neither exports nor payback are guaranteed.']
    n['requirement_contracts']=[dict(meaning='Recheck sufficient treasury, ownership/control of every recipient state and the unpaid flag immediately before atomic payment and resource delivery. If any check fails, neither cash nor oil moves. No replay on government change or reload.',proposed_code='\n'.join(guards))]
    native=n['effect_body']
    n['effect_body']='# Proposed atomic wrapper; treasury/resource/update leaves are existing MD APIs.\nif = {\n limit = {\n  '+'\n  '.join(guards)+'\n }\n '+native.replace('\n','\n ')+'\n set_country_flag = '+flag+'\n ingame_update_setup = yes\n}'
    n['historical_status']='Proposed1970–1990 roleplay investment balance using native base oil; fees and units are not historical estimates.'
next(g for g in groups if g['id']=='oil')['ownership']='Paid extraction capacity remains national across governments; native depletion can reduce later base oil. No programme refresh repeats payment or a resource grant.'

# British protection is a status, not an outlook or a permanent party unlock.
british_nodes={n['id'].removeprefix('COLDWAR_UAE_'):n for n in nodes if n['group']=='british'}
for key,n in british_nodes.items():
    independent=key in ['orderly_handover','british_friendship']
    n['diplomatic_state_gate']='independent' if independent else 'protection_agreed' if key in ['protected_administration','british_training','british_commercial','enduring_protection'] else 'british_subject'
    n['available']=('is_subject = no' if independent else 'is_subject_of = ENG')
    if n['diplomatic_state_gate']=='protection_agreed':n['available']+='\nhas_country_flag = COLDWAR_UAE_protection_accepted'
    if n['treasury_cost_billion']:n['available']+=f'\ncheck_variable = {{ treasury > {n["treasury_cost_billion"]:g} }}'
    n['active_condition']=n['available'].split('\ncheck_variable')[0]
    if key=='british_friendship':n['active_condition']+='\nhas_country_flag = COLDWAR_UAE_friendship_accepted'
    n['ownership']='One-time domestic gains remain earned. British protection programme contributions require both British subject status and an accepted compact. They suspend on release or a new overlord. Independent friendship needs its own accepted treaty. No regrant on reload.'
    n['icon']={'treaty_coast':'align_to_britain','renew_protection':'align_to_britain','petition_independence':'treaty3','protected_administration':'government_beu','orderly_handover':'accept_treaty','british_training':'military_mission','british_commercial':'liberalization','british_friendship':'treaty2','enduring_protection':'align_to_britain3'}[key]
    n['requirement_contracts'].append(dict(meaning='Native Puppet State already transfers50% of civilian/military factory capacity and restricts independent war declarations. Treaty spirits explain these terms; they do not add a second copy of these penalties.',proposed_code='is_subject_of = ENG # exact status; independent route instead uses is_subject = no'))
next(n for n in nodes if n['id']==ID('sovereign_union'))['diplomatic_state_gate']='independent'
next(g for g in groups if g['id']=='british')['ownership']='Existing domestic liaison requires British subject status. Renewed protection programmes additionally require an accepted compact; independent friendship requires its own accepted treaty. Preserve earned progress and one-time grants; suspend only the ongoing contributions when their status condition ends.'
british_nodes['treaty_coast']['ownership']='Existing-relation domestic liaison: requires British subject status, without needing a newly accepted extension. This ongoing contribution suspends when the relationship ends.'
british_nodes['treaty_coast']['bypass']='is_subject = no'
british_nodes['treaty_coast']['bypass_contract']='After actual independence, bypass this non-exclusive starting liaison focus without charging its fee or granting its rewards. Do not auto-complete or bypass either exclusive policy choice.'
british_nodes['petition_independence']['available']='OR = { is_subject_of = ENG is_subject = no }'
british_nodes['petition_independence']['active_condition']=british_nodes['petition_independence']['available']
british_nodes['petition_independence']['diplomatic_state_gate']='british_or_independent'
british_nodes['petition_independence']['ownership']='Domestic handover preparation may be taken before or after independence. Only an actual British subject sends an early-release proposal. After release it opens the existing handover follow-up without a new UK veto or automatic grant.'

release_leaf='''# UK-scoped delivery of the starting historical schedule OR a mutually accepted replacement.
if = {
 limit = {
  country_exists = UAE
  UAE = { is_subject_of = ENG has_country_flag = COLDWAR_UAE_withdrawal_schedule_active }
  COLDWAR_UAE_release_schedule_is_current_and_due = yes # NEW origin/nonce/date guard; no focus or fresh approval gate
 }
 end_puppet = UAE
 UAE = {
  set_country_flag = COLDWAR_UAE_withdrawal_agreed
  clr_country_flag = COLDWAR_UAE_protection_accepted
  clr_country_flag = COLDWAR_UAE_withdrawal_schedule_active
  set_country_flag = COLDWAR_UAE_release_contract_fulfilled
  COLDWAR_UAE_sync_treaty_spirits = yes # NEW: mirror fulfilled date, stop subject-only benefits
  ingame_update_setup = yes
 }
}'''
british_treaties={
    'record_contract':'Both countries START on 1 January 1970 with British Withdrawal Announced spirits and the same existing withdrawal schedule. Its origin is the British policy announced in 1968, not a newly signed independence request. Mirror one current schedule/compact ID, origin, nonce, terms and dates. Later bilateral agreements replace that record only on mutual acceptance; an unsigned offer creates no new signed-agreement spirit.',
    'timer_contract':'Store a relative due date with the verified native global.date convention and GetDateStringNoHourLong display. A360-day term uses the native investment pattern: copy global.date, add8.64. Historical1December1971 uses a literal date trigger and an explicit English date, avoiding an invented numeric date conversion. Timed-idea expiry alone never frees the country.',
    'delivery_contract':'The normal historical withdrawal is scheduled from the 1970 start and needs NO focus, UAE petition or new UK acceptance. Use 1 December 1971 as the explicitly labelled historical scenario execution date; the 1968 announcement specified the end of 1971, not that precise signed date. A daily/load observer and scheduled wake-up execute the current starting schedule or accepted replacement once. Recheck both countries, origin/nonce/date and actual British subject status. An unanswered or refused offer never pauses the baseline. If already free, close without replay; another overlord or annexation invalidates stale British delivery.',
    'changes_contract':'An EARLIER release, negotiated handover terms or continued protection needs both countries’ agreement. A mutually accepted renewed compact can replace the starting withdrawal schedule only BEFORE its due date. Recheck the current nonce, both countries, actual British subject status and the unfulfilled schedule at acceptance; a late popup cannot postpone a deadline that is already due. Process the due release first. A pending, refused or expired renewal changes nothing. Handover-only cooperation preserves the existing date unless an explicit date amendment is accepted. UK cannot unilaterally postpone the baseline; government changes and focus completion do not reset it. Refusals permit renewed talks after180 days; only one current offer at a time.',
    'continuity_contract':'While still protected, and while independent but not yet federated, retain an appropriate collective Council/interim administration. Do not let the existing1971.12.2 character expiry create a federal presidency or end the treaty. Respect individual ruler succession; do not freeze a named ruler or blindly cycle the native leader pool.',
    'release_effect':release_leaf,
    'variants':[
        dict(id='starting',label='British Withdrawal Announced',status='Starting state on 1 January 1970; withdrawal was announced on 16 January 1968',date_label='Announced withdrawal deadline',date='By the end of 1971',independence='Historical scenario execution: 1 December 1971, automatically unless both countries agree to replace the schedule',uk_spirit=ID('ENG_withdrawal_announced'),uae_spirit=ID('treaty_dependence'),icon='treaty3',uae_terms=['Start with this spirit and the existing withdrawal schedule; no independence petition is needed.','Until release, Britain retains the external-affairs and defence responsibilities represented by native subject rules.','Prepare local institutions. An earlier release or continued protection requires a new mutual agreement; refusing those proposals does not cancel the historical withdrawal.'],uk_terms=['Start with this spirit recording the withdrawal policy already announced in 1968: leave the Gulf by the end of 1971.','The historical scenario delivers release on 1 December 1971 without a new vote. That precise execution date is a scenario convention based on the later historical termination, not a date already signed in January 1970.','Continue existing responsibilities until release. Retaining protection requires UAE consent to a replacement compact.']),
        dict(id='scheduled',label='Agreed British Withdrawal',status='Signed; UAE remains a British subject until the agreed date',date_label='Contractual independence',date='1 December1971',independence='1 December1971 — automatic delivery of the already accepted settlement',uk_spirit=ID('ENG_withdrawal_treaty'),uae_spirit=ID('withdrawal_treaty'),icon='treaty3',uae_terms=['Accept the agreed handover timetable and prepare local institutions.','Remain under British protection until the release date; no independence purchase fee.','Actual independence opens British Withdrawal; federal founding still needs the rulers’ charter.'],uk_terms=['End the special treaty/subject relationship on1December1971. No new approval is required when the date arrives.','Coordinate the agreed handover. Any paid aid, equipment transfer or continuing base access needs separate explicit terms.']),
        dict(id='protection',label='Renewed Protection Compact',status='Signed alternative: continued British protection',date_label='Review date',date='360 days after acceptance; example27December1970 if signed1January1970',independence='No fixed independence date; review does not automatically free the country',uk_spirit=ID('ENG_protection_compact'),uae_spirit=ID('protection_compact'),icon='align_to_britain3',uae_terms=['Retain the agreed limits on external sovereignty and the existing native subject obligations.','Fund the selected local training/commercial programme; no repeated50% factory penalty is added.','A fixed independence date can be negotiated only by a mutually accepted amendment.'],uk_terms=['Accept continued special treaty protection rather than enforce the historical withdrawal policy.','Provide the agreed advisory/security cooperation. Cash, equipment or basing commitments require explicit accepted amounts.','Review the compact after360 days; review expiry alone changes no sovereignty.']),
        dict(id='fulfilled',label='Independence Agreement Fulfilled',status='Completed; UAE is independent',date_label='Independence delivered',date='1 December1971 in this historical example',independence='Completed — the country is already free',uk_spirit=ID('ENG_withdrawal_fulfilled'),uae_spirit=ID('withdrawal_fulfilled'),icon='accept_treaty',uae_terms=['The agreed release has taken effect. Federal formation is a separate local decision.','Keep a30-day completed-agreement notice; no continuing protection bonus or second release.'],uk_terms=['The special treaty relationship has ended.','Keep the same30-day completion record; new friendship or access arrangements require a new accepted agreement.']),
        dict(id='friendship',label='UK–UAE Friendship Treaty',status='Signed cooperation between independent states',date_label='Independence status',date='UAE is already independent; no future independence date is required',independence='Already independent',uk_spirit=ID('ENG_friendship_treaty'),uae_spirit=ID('friendship_treaty'),icon='treaty2',uae_terms=['Maintain agreed consultation and technical cooperation. Active UAE programme: research+3%, office productivity+6%, education spending+5%.','This treaty creates no subject relation, automatic faction, base rights or unconditional military guarantee.'],uk_terms=['Provide the accepted consultation and technical-cooperation access.','No automatic treasury debit, unit deployment or military guarantee; any paid offer receives its own numeric option.']),
    ]
}
for key,kind,event in [('renew_protection','protection',2),('petition_independence','early_handover',1),('british_friendship','friendship',3)]:
    n=british_nodes[key]
    n['diplomatic_offer']=dict(kind=kind,recipient='ENG',event=f'COLDWAR_UAE_BRITISH.{event}',initial_delivery='Only a CHANGE to the starting withdrawal plan needs mutual consent. The historical schedule already exists; pending or refused talks do not delay it.')
    n['effect_body']+=f'\nCOLDWAR_UAE_send_{kind}_offer = yes # NEW guarded nonce-aware dispatcher to ENG event COLDWAR_UAE_BRITISH.{event}'
    if kind=='early_handover':
        n['effect_body']='if = {\n limit = { is_subject_of = ENG }\n '+n['effect_body'].strip()+'\n}\n# Already independent: domestic preparation only; no offer, fee, cash or equipment grant.'
        n['diplomatic_offer']['dispatch_condition']='is_subject_of = ENG; after independence skip dispatch and retain domestic handover progression'
    n['requirement_contracts'].append(dict(meaning='UK and UAE explicitly agree to a changed plan. Only accepted terms replace the matching national spirits, schedule nonce and due/review date. Until then the historical release remains in force; the UK cannot veto it by rejecting or ignoring a proposal.',proposed_code=release_leaf if kind=='early_handover' else '# Proposed replacement agreement: mirror country-specific spirits, origin, nonce and accepted terms only on mutual acceptance.'))
british_nodes['petition_independence']['reward_summary']=['The historical withdrawal is already scheduled at the 1970 start: normal release on 1 December 1971 needs neither this focus nor a new UK approval.','While still a British subject, unlock negotiations for an earlier release and practical handover terms; both countries must accept changes to the existing plan.','After independence, this remains available as domestic preparation for An Orderly Handover; no new UK approval or release offer.','A refused or unanswered proposal leaves the original schedule running. The focus itself grants no cash, equipment or immediate sovereignty.']
british_nodes['renew_protection']['reward_summary'].append('Only mutual acceptance replaces the starting withdrawal schedule with Renewed Protection Compact spirits. Pending or refused proposals leave historical release in force. The accepted alternative has a review date and no fixed independence date.')
british_treaties['starting_state']=dict(active_on='1970.1.1',origin='British withdrawal policy announced 1968.1.16',announced_deadline='By the end of 1971',historical_execution_date='1971.12.1',requires_focus=False,requires_new_uk_acceptance=False,starts_with_both_spirits=True,initialisation_contract='Initialise once inside the existing NEW 1970 scenario setup when UAE is an ENG subject. Create the canonical starting-policy record and mirror the role-specific spirits to ENG and UAE before play. Mark treaty state initialised. Save/load and government changes only resynchronise that existing record; never recreate the baseline after a valid renewal, amendment or completed release.',bootstrap_effect='''# UAE scope, inside the existing new-1970-scenario bootstrap only.
if = {
 limit = {
  is_subject_of = ENG
  NOT = { has_country_flag = COLDWAR_UAE_treaty_state_initialised }
 }
 set_country_flag = COLDWAR_UAE_treaty_state_initialised
 set_country_flag = COLDWAR_UAE_withdrawal_schedule_active
 COLDWAR_UAE_register_starting_withdrawal = yes # NEW: origin=1968 policy, current nonce, due=1971.12.1
 COLDWAR_UAE_sync_treaty_spirits = yes # NEW: starting role-specific spirits in BOTH countries
}''')
british_treaties['date_options']=[
    dict(id='immediate',label='Immediate independence',acceptance='Release on acceptance, record the actual date in both countries, then show a30-day fulfilled-agreement notice.'),
    dict(id='historical',label='Keep the historical withdrawal schedule',availability='Already active at the 1970 start; no new offer or acceptance required.',maturity_trigger='NOT = { date < 1971.12.1 }',display='1 December 1971 (historical scenario execution)'),
    dict(id='negotiated_term',label='A360-day transition',date_code='set_variable = { COLDWAR_UAE_contract_due = global.date }\nadd_to_variable = { COLDWAR_UAE_contract_due = 8.64 }',display='[?COLDWAR_UAE_contract_due.GetDateStringNoHourLong]'),
]
british_treaties['spirit_implementation']='Install the British Withdrawal Announced role-specific spirits in BOTH countries at the 1970 start, reusing UAE treaty_dependence rather than stacking a second subject penalty. Preserve its single −10% political power contribution while UAE remains an ENG subject, including an accepted protection compact: relabel the existing carrier or transfer that contribution exactly once, never drop or duplicate it. Mirror record origin, nonce, execution date and status. Distinguish the announced end-1971 deadline from the historical scenario execution on 1 December. Later signed agreements replace the starting spirits together only on mutual acceptance. Active effects read actual subject/free status and accepted programme flags. An unsigned offer adds no new signed-agreement spirit and cannot erase or pause the starting schedule.'
for variant in british_treaties['variants']:
    for field in ['date','status','independence']:
        variant[field]=variant[field].replace('December1971','December 1971').replace('December1970','December 1970').replace('January1970','January 1970').replace('of1971','of 1971')
    for field in ['uae_terms','uk_terms']:
        variant[field]=[s.replace('December1971','December 1971').replace('the1968','the 1968').replace('after360','after 360') for s in variant[field]]

def decision(key,label,g,unlock,pp,days,summary,code=''):
    decisions.append(dict(id=ID('decision_'+key),label=label,group=g,unlock=ID(unlock) if unlock else None,pp=pp,days=days,summary=summary,effect_code=code))
decision('withdrawal','Reopen the Status Talks','british','treaty_coast',35,60,'After either policy focus, and180 days after a refused or expired proposal, reopen talks on earlier release or continued protection. Changes need both countries’ consent. Normal historical withdrawal requires no decision and continues during talks. A later petition after an accepted loyalty compact can negotiate a new release without resetting exclusive focuses.')
decision('bahrain','Offer Bahrain a Charter','union','nine_states',25,60,'Bahrain chooses: join the negotiated representation settlement, remain an associated partner, or refuse. UAE setup offer costs 2% of offer-date GDP only on acceptance. No unilateral annexation.')
decision('qatar','Offer Qatar a Charter','union','nine_states',25,60,'Qatar receives its own sovereignty and representation offer. Terms and any integration level require its player’s consent. A refused offer permits the seven-emirate fallback.')
decision('convention','Convene a Constitutional Convention','union','federal_council',50,90,'Use native outlook, subparty organisation and governing-party change. No instant 100% party switch. Proposed constitutional, nationalist and social rosters are alternate-history institutions, with historical availability explained.')
decision('mediate','Mediate the Federal Dispute','monarchy','rulers_compact',35,90,'Once per constitutional crisis: offer 3% of start-date GDP as development transfers. Accepted rulers’ compact removes the remaining Unequal Development stability penalty; rejection spends no transfer money.')
decision('delegation','Request Delegated Powers','monarchy','presidential_union',50,120,'Offer a stronger federal executive with explicit emirate guarantees. Acceptance activates the constitutional change; refusal leaves existing autonomy. Coercion requires a separate declared crisis, not a surprise civil war.')
decision('court_settlement','Settle Crown and Property','constitutional','citizen_republic',50,120,'An agreed settlement costs 5% of start-date GDP and ends the −6% republican transition contribution. It does not seize a player’s property or grant duplicate treasury rewards.')
decision('residency','A Staged Residency Law','constitutional','municipal_compact',35,90,'Pay 2% of start-date GDP. Gain +3% workforce for 730 days and +3% bureaucracy spending for the same duration. Once per 730 days; no automatic citizenship.')
decision('arab_exchange','Offer Arab Technical Cooperation','arab','arab_solidarity',25,90,'Recipient-approved exchange: UAE pays 2% of offer-date GDP; both parties receive +10 productivity points in controlled states, once per partner in 730 days. Partner does not pay without choosing the offer.')
decision('industry_project','Prepare the Public Industrial Site','arab','public_industry',25,60,'Pay 2% of start-date GDP to gain +10% civilian factory construction speed for 365 days. A queued factory still requires native labour, electricity and construction output. No instant factory.')
decision('labour_inspection','Inspect Labour Contracts','left','labour_code',25,90,'Treasury cost 1% of start-date GDP; +5% workforce and +3% bureaucracy spending for 365 days. Cooldown 730 days; enforceable contract theme, no free manpower.')
decision('scholarships','Fund Technical Scholarships','left','technical_cadres',25,90,'Treasury cost 2% of start-date GDP; +10 productivity points to each controlled state on completion. Cooldown 730 days; one grant per paid course.')
decision('association_law','Recognise Educational Associations','islah',None,35,90,'Historical institutional context 1974. Early legalisation is a distinct alternate choice through the existing political system, not a mass party at the 1970 start. +3% research and +5% education cost for 365 days; costs 1% GDP.')
decision('charity_oversight','Register Charitable Accounts','islah','charitable_network',25,60,'Treasury cost 1% of start-date GDP; reduce the programme’s bureaucracy burden by 3 percentage points once. Re-registration cannot stack the reward.')
decision('participation','Negotiate Oil Participation','oil','state_participation',35,120,'Foreign partner chooses an equity participation deal. Proposed buy-in: 10% of offer-date UAE GDP; final executed cost is shown numerically. Acceptance activates the conditional +15% export revenue contribution. A refusal does not charge or activate it.')
decision('reserve_deposit','Deposit an Oil Reserve','oil','adia_savings',15,30,'Transfer exactly 5% of start-date GDP from treasury to a tracked Abu Dhabi reserve principal, once per 365 days. No income is generated by a bookkeeping variable. Native investment returns need a separately funded native investment.')
decision('reserve_withdraw','Release the Reserve Principal','oil','adia_savings',15,30,'Return the chosen recorded principal to treasury, up to the reserve balance. Withdrawn principal is removed from the ledger in the same transaction; no repeatable money creation.')
decision('oil_restraint','Debate Export Restraint','oil','oil_institutions',35,90,'Use the active Cold War OPEC decisions and existing restraint flag. Native restraint already deducts 10 percentage points from the export multiplier. Do not add a second price model or duplicate the penalty.')
decision('oil_downturn','Respond to an Oil Downturn','oil','oil_shock_plan',35,90,'During a native oil-price slump choose reserve withdrawal or a 365-day spending pause. Pause: bureaucracy costs −10%, construction speed −8%; it neither fixes world prices nor guarantees export income.')
decision('port_project','Prepare a Port Expansion','commerce','port_planning',25,60,'Pay 2% of start-date GDP for +15% naval base construction speed for 365 days. A new port level is queued only in a verified coastal province with free capacity; existing level-10 Abu Dhabi is ineligible.')
decision('airline','Finance a Civil Airline','commerce','aviation_hub',35,120,'Lease/operations fund: 5% of offer-date GDP; +8% office productivity and +6% energy consumption for 730 days. Repeated operating contracts replace rather than stack. No military aircraft grant.')
decision('industrial_power','Audit Industrial Power Demand','commerce','industrial_port',25,60,'Pay 1% of start-date GDP for −5% energy consumption for 365 days. Construction remains queued and can be delayed by real labour or power shortages.')
decision('housing','Fund a Housing Phase','society','citizen_housing',25,120,'Pay 3% of start-date GDP; +3% stability and +3% bureaucracy spending for 730 days. Cooldown 730 days; repeated phases replace rather than stack the active contribution.')
decision('housing_workers','Inspect Worker Housing','society','worker_towns',25,90,'Pay 2% of start-date GDP; +4% workforce and +4% health spending for 365 days. Cooldown 730 days. Migrant workers do not automatically enter the citizen recruitment pool.')
decision('vocational','A Vocational Intake','society','technical_institutes',25,120,'Pay 2% of start-date GDP; all controlled states +10 productivity points once at completion. Cooldown 730 days; an interrupted unpaid course grants nothing.')
decision('training','A Joint Training Cycle','defence','sustainable_force',25,90,'Pay 2% of start-date GDP; +15 Army experience and −5% training time for 365 days. Cooldown 730 days, no new units and no stacking duplicate active cycles.')
decision('procurement','Request a Procurement Offer','defence','air_coastal_shield',25,60,'Seller chooses whether to offer era-appropriate equipment using existing licensed/market contracts. Money and quantities must be numerical in the event option. No one-sided sale or modern equipment unlock.')
decision('maintenance','A Mobile Maintenance Course','defence','land_deterrent',25,90,'Pay 2% of start-date GDP; +10 Army experience, equipment costs −5% for 365 days. Cooldown 730 days; the modifier replaces any existing identical course.')
decision('island_offer','Offer an Islands Settlement','diplomacy','islands_arbitration',35,90,'Separate Abu Musa access arrangements from the Tunbs sovereignty dispute. Iran may accept arbitration, make a counter-offer or refuse. No direct state transfer: these islands are not separate existing UAE states on this map.')
decision('jeddah','Negotiate the Saudi Border','diplomacy','gulf_diplomacy',35,90,'Recipient-approved border accord inspired by the 1974 settlement. No guessed map-resource transfer; economic terms are frozen numerically when offered. Rejection leaves the dispute unresolved.')
decision('gcc','Propose a Gulf Charter','diplomacy','gulf_cooperation',50,120,'Each eligible Gulf player accepts membership separately. Administrative entry cost: 2% of own offer-date GDP, paid by each accepting participant. Use the existing GCC framework; no automatic military faction.')
decision('kuwait','Respond to an Invasion of Kuwait','diplomacy','gulf_crisis',35,60,'Only if an invasion exists: offer 3% GDP financial support, negotiated transit, or opt-in deployment. Kuwait/coalition recipients receive the funded offer. Neutral civil protection costs 1% GDP and gives +3% stability for 365 days.')
decision('founders','The Founders’ Settlement','union','charter',35,60,'Choose the proposed charter priority, negotiate ruler guarantees, then accept the settlement. Acceptance sets COLDWAR_UAE_founders_consented and the chosen charter term flag; only the matching institutional focus is available. A refused stronger mandate can be renegotiated as emirate guarantees. Broader Bahrain/Qatar agreement separately sets COLDWAR_UAE_broad_charter_accepted. No annexation or forced consent.')
decision('sharjah','The Sharjah Crisis','monarchy','majlis',25,30,'Triggered only by a restoration/coup attempt, with the historical crisis context January1972. Choose negotiated surrender (2% start-date GDP, +3% stability for365 days) or federal security intervention (+10 Army experience, +5% military personnel costs for365 days). Local ruler settlement is explicit; neither option installs an invented Baath government. One resolved crisis, one reward.')
decision('cabinet_bargain','The Federal Cabinet Bargain','monarchy','rulers_compact',35,90,'A 1976–79 constitutional dispute may be settled by a federal cabinet led by an agreed Dubai nominee, historically Rashid in1979, with recognition of emirate authority. −3 percentage points of the Fragmented Authority bureaucracy penalty once, floor0; +3% bureaucracy spending while the negotiated cabinet is active. President and prime minister remain distinct offices.')
decision('training_offer','Offer a Training Agreement','diplomacy','security_contracts',25,90,'Selected eligible partner receives the offer. Accept: UAE pays exactly2% of offer-date GDP, gains15 Army experience and −5% training time for730 days. Partner grants access to instructors without an imposed treasury debit. Reject: no charge or benefit. Cooldown730 days; replacement, no stacking.')
decision('exchange_offer','Offer a Technical Exchange','diplomacy','technical_exchange',25,90,'Selected eligible partner receives the offer. Accept: UAE pays exactly2% of offer-date GDP, gains10 productivity points per controlled state once; partner chooses whether to provide experts and has no automatic payment. Reject: nothing charged or granted. Cooldown730 days per partner.')
for d in decisions:
    if d['id']==ID('decision_association_law'):
        d['available']='original_tag = UAE; association not yet organised; available independently of current governing party via civil-association law; historical context1974 or explicit early-recognition alternative'
        d['sets_flags']=[ID('islah_organised')]
        d['summary']+=' On legal recognition set COLDWAR_UAE_islah_organised once; this does NOT put the movement in government.'
    if d['id']==ID('decision_founders'):
        d['sets_flags']=[ID('founders_consented')]
        d['choice_flags']={'stronger_mandate':ID('mandate_agreed'),'emirate_guarantees':ID('guarantees_agreed')}
        d['mutually_exclusive_choice_flags']=True
    if d['id']==ID('decision_participation'):d['sets_flags']=[ID('oil_participation_accepted')]
    if d['id']==ID('decision_kuwait'):d['unlock']=ID('gulf_diplomacy')
    if d['id']==ID('decision_withdrawal'):
        d['available']='is_subject_of = ENG; completed one of renew_protection/petition_independence; no pending offer;180-day retry cooldown'
        d['unlock_any']=[ID('renew_protection'),ID('petition_independence')]
decision('british_cofinance','Request British Co-Financing','british','enduring_protection',25,60,'Offer one agreed development grant. UK acceptance: UK treasury−$0.25bn, UAE treasury+$0.25bn, once per country programme. UK must have the money and UAE must still be its subject under the compact. Refusal/expiry moves no money; paid flag prevents repeat grants even after government changes.',code='''# UK-scoped accepted option; the current-offer trigger is NEW nonce-aware integration.
if = {
 limit = {
  original_tag = ENG
  country_exists = UAE
  check_variable = { var = treasury value = 0.25 compare = greater_than_or_equals }
  UAE = {
   is_subject_of = ENG
   has_country_flag = COLDWAR_UAE_protection_accepted
   has_completed_focus = COLDWAR_UAE_enduring_protection
   NOT = { has_country_flag = COLDWAR_UAE_british_development_grant_paid }
  }
  COLDWAR_UAE_british_offer_is_current = yes # NEW requestID/nonce guard
 }
 set_temp_variable = { treasury_change = -0.25 }
 modify_treasury_effect = yes
 UAE = {
  set_temp_variable = { treasury_change = 0.25 }
  modify_treasury_effect = yes
  set_country_flag = COLDWAR_UAE_british_development_grant_paid
 }
}''')
decision('british_amendment','Amend the Withdrawal Terms','british','treaty_coast',35,60,'Available for the starting withdrawal schedule or an accepted replacement compact: propose a different date or change the protection/cooperation terms. Both countries must explicitly accept the same amendment. The current schedule remains in force until a valid replacement is accepted before its deadline; UK cannot silently postpone it. Replace both mirrored spirits and nonce together. Normal historical withdrawal requires no use of this decision.')
decision('british_withdrawal_policy','The British Withdrawal Policy','british',None,0,0,'The withdrawal schedule and paired spirits already exist on 1 January 1970. No UK approval decision is needed for the normal historical release. UK may offer earlier release, handover cooperation or renewed protection; changing the baseline requires UAE consent. A pending or refused offer never pauses the scheduled release.')

def british_prose(s):
    s=re.sub(r'(?<=[A-Za-z])(?=[0-9$])',' ',s)
    s=re.sub(r'(?<=[0-9])(?=[A-Z][a-z])',' ',s)
    return re.sub(r'(?<=[A-Za-z])(?=[+−])',' ',s)
for n in british_nodes.values():
    for field in ['description','historical_status']:n[field]=british_prose(n[field])
    n['reward_summary']=[british_prose(s) for s in n['reward_summary']]
for d in decisions:
    if d['group']=='british':d['summary']=british_prose(d['summary'])
for variant in british_treaties['variants']:
    for field in ['date','status','independence']:variant[field]=british_prose(variant[field])
    for field in ['uae_terms','uk_terms']:variant[field]=[british_prose(s) for s in variant[field]]
next(v for v in british_treaties['variants'] if v['id']=='starting')['uae_spirit']=ID('treaty_dependence')

spirits=[
dict(id=ID('treaty_dependence'),label='British Withdrawal Announced',description='In January 1968 Britain announced that its forces would leave the Gulf by the end of 1971. The Trucial rulers must prepare for the end of British protection. Until that withdrawal, Britain retains its external-affairs and defence responsibilities.',modifiers={'political_power_factor':-.10},active_condition='is_subject_of = ENG',native_consequences={'Starting withdrawal schedule':'Present from 1 January 1970 in both countries. Announced deadline: by the end of 1971. Historical scenario execution: 1 December 1971, without a new petition, focus or UK vote.','Existing British subject relation':'Native subject restrictions remain until actual release; no duplicate factory-transfer penalty.','Changing the plan':'An earlier release or continued protection needs mutual consent. Unsigned or refused talks leave the original schedule running.'},treatment='Reuse the existing treaty_dependence ID and −10% political power contribution. Replace its visible terms after an accepted compact; deactivate on actual release. Sovereign federal formation remains a separate focus.'),
dict(id=ID('fragmented_authority'),label='Fragmented Authority',description='Separate courts, administrations and forces make common action expensive and difficult.',modifiers={'bureaucracy_cost_multiplier_modifier':.20,'army_org_factor':-.10},treatment='Constitutional bargains reduce administration costs; Union Command or Coordinated Commands treats the military penalty. No permanent extra penalty after full removal.'),
dict(id=ID('unequal_development'),label='Unequal Development',description='Abu Dhabi has oil; Dubai has commerce; the northern emirates have much less fiscal room.',modifiers={'production_speed_buildings_factor':-.12,'stability_factor':-.06},treatment='Charter bargain, accession, solidarity and crisis mediation remove explicit parts. These are national reforms and survive a change of government.'),
dict(id=ID('scarce_specialists'),label='Scarce Specialists',description='Oil revenue cannot instantly supply teachers, technicians, doctors or administrators.',modifiers={'research_speed_factor':-.10,'total_workforce_modifier':-.08},treatment='Training or specialist recruitment provides an initial remedy; Technical Institutes completes the structural remedy.'),
dict(id=ID('water_power'),label='Water and Power Constraints',description='Coastal expansion depends on costly water distribution, desalination and reliable generation.',modifiers={'energy_use_multiplier':.15,'civilian_factories_productivity':-.05},treatment='Water for the Towns removes the productivity penalty and reduces the energy penalty to +5%; its own +6% operating contribution is still explicit.'),
dict(id=ID('narrow_revenues'),label='A Narrow Revenue Base',description='The emirates possess valuable reserves, but only a small operating oil industry. Producing wells and offshore systems need costly investment; the broader productive and service economy remains thin.',modifiers={'civilian_factories_productivity':-.10,'offices_productivity':-.10},native_consequences={'Starting base oil':'4 total: Abu Dhabi3 + Dubai1 instead of inherited47, a proposed91.49% reduction in mapped operating capacity.','Oil development':'Four once-paid focuses add8 /10 /15 /10 base oil for0.75 /2.50 /5.00 /8.00 billion. Nominal capacity after all four is47 before extraction modifiers or depletion.','Oil receipts':'Native prices and actual exports determine receipts; no duplicate percentage income debuff is added.'},treatment='Paid expansion supplies operating oil. Oil downturn preparation and Earnings beyond Oil remove the two civilian penalty steps. Commercial Courts and Earnings beyond Oil remove the office penalty steps.'),
dict(id=ID('expatriate_workforce'),label='An Expatriate Workforce',description='Imported workers expand the labour force without giving the rulers an equivalent citizen military reserve.',modifiers={'total_workforce_modifier':.10,'conscription_factor':-.20},treatment='A structural trade-off. Residency and education do not silently convert migrants into recruitable citizens; no mass citizenship decision is assumed.'),
]
rules={
'approval':'CONCEPT ONLY. No loaded focus, history, character, idea, decision, on-action, GFX or localisation file is changed. All new proposed IDs begin COLDWAR_UAE_.',
'politics':'Use the existing outlook and exact subparty system. Available checks gate meaningful programmes immediately when their governing party is in office. Fixed branches remain visible and locked, following MD Russia; no redundant outlook unlock focus.',
'lifecycle':'Persist earned progress separately from active government programmes. Recalculate enabled dynamic modifiers after government change, succession, load and a periodic fallback. When the qualifying party returns, restore only earned ongoing contributions; never rerun buildings, productivity grants, cash or diplomacy.',
'exact_parties':'The two internal paths in the Arab and Left clusters have exact-party conditions as well as their shared cluster gate. Moving between those parties suspends their branch-specific programme while common earned institutional gains remain. The presidency is not assumed from the ruling-party slot alone.',
'stacking':'Numbers in focus details are contributions, not whole-spirit replacements. One earned contribution per focus, counted once. Political positive stability contributions have a combined +15 percentage-point cap per currently active programme, all negatives remain. Economic and military contributions otherwise add as shown; mutually exclusive alternatives never stack.',
'national_reforms':'Starting-spirit remedies are permanent and order independent. Recompute each component from its immutable original value plus once-earned remedy credits, strongest credit within a shared stage family, then clamp at zero. A target stage is converted to its relief against the original component, never written onto the current value. Charter and Zayed construction relief combine; army integration stages use the strongest relief, not a sum. Never replay one-time rewards or turn deletion of a penalty into an extra positive modifier. Accepted crisis settlements add their own once-earned credits; rejection adds none.',
'conditional_deals':'State Participation +15% oil export revenue activates only after its contract is accepted. Nine-state +1 investment capacity activates only with an accepted broad federation settlement. The focus unlocks an offer, not acceptance. Training Agreements and Across the Blocs grant only their contract decisions, never the listed contract rewards immediately.',
'money':'Cash values are MD billions. Costed focuses require funds at completion. Decisions freeze their GDP-based price at offer/start, show the concrete numeric debit, recheck acceptance and feasibility, and execute atomically once. No implicit debt or free money on rejection.',
'projects':'All promised factories, offices and fossil plants are QUEUED with ordinary native construction, staffing and energy requirements; the small cash fee funds preparation only. State179=Dubai, state180=Abu Dhabi. Port levels require verified coastal provinces and capacity; no level11 Abu Dhabi port.',
'diplomacy':'Foreign players retain consent over treaties, equity contracts, GCC membership, bases, federation integration and transfers. Individual northern emirates are a political ledger inside the existing two UAE states. Bahrain/Qatar integration and non-state islands need explicit negotiated representation, not guessed map changes.',
'time':'Most focuses take21/35 days; major settlements49 days, matching Russia. Real event context remains: withdrawal1971, Islah1974, military union1976, GCC1981, oil slump1986. Earlier institutional models are labelled alternatives; no blanket year locks or forced historical wars. A Kuwait-invasion response is available from early Gulf Diplomacy whenever the invasion exists, independent of the later Gulf Crisis focus or the islands choices.',
'calibration':'Balance is proposed, not engine tested. StartGDP target0.686bn;1%=0.00686bn. Check actual new-game output before implementing. The starting OOB and equipment work remains deferred. No F-16 Block60 Cold War grant.',
'oil_programme':'Start with4 raw oil units: AbuDhabi3/Dubai1 instead of47. First development costs0.75bn for+8; onshore2.50bn for+10; offshore5.00bn for+15; second offshore8.00bn for+10. Total16.25bn for+43 base oil. Each phase requires actual funding, ownership/control and an unpaid project flag. The main onshore and offshore expansions are compatible and follow either ownership/services settlement.',
'oil_economy':'Apply reduced raw resources BEFORE the existing1970 GDP snapshot calibration, then freeze the native accounting offset once. This preserves the authored0.686bn initialGDP target without restoring oil units or oil export cash. Later oil phases grow endogenousGDP. Native demand, extraction, world prices and six-month depletion continue; nominal47 after all grants is not an output guarantee or periodic refill.',
'british_flow':'Start BOTH countries with British Withdrawal Announced spirits and the pre-existing schedule. The historical release executes on 1 December 1971 without a focus or new UK approval. The 1968 announced deadline was the end of 1971; the precise date is a labelled historical scenario convention. Initial focus choice: seek a mutually accepted protection extension or prepare the already-planned handover and negotiate optional earlier release/terms. Only accepted replacements change the baseline. Sovereign British Withdrawal still requires actual is_subject = no plus founder consent.',
'british_lifecycle':'Protection programmes need British subject status and an accepted compact, and suspend on release or a new overlord. Friendship requires a separate accepted independent-state treaty. A refusal permits a180-day retry or a new protection proposal; initial focus exclusions remain intact. Preserve the Council/interim administration until real formation rather than letting a character-expiry date create a federal president.',
'british_maturity':'A once-only new-1970 bootstrap creates the starting schedule and mirrored spirits. Daily/load observers and a scheduled callback execute the CURRENT starting-policy schedule or mutually accepted replacement once when due, without a new UK veto or focus gate. Pending/refused offers do not pause it. Keep origin, nonce and date in both countries; never restore the baseline over an accepted renewal on load. Timed-spirit expiry alone does not free UAE. No automatic payment, army, faction or war is bundled into release.',
}
data=dict(country='UAE / Trucial States',scenario='1970.1.1',version='Concept4 — Withdrawal scheduled at the 1970 start',groups=groups,nodes=nodes,decisions=decisions,starting_spirits=spirits,programme_rules=rules,modifier_labels=labels,starting_resources=oil_start,oil_development=oil_phases,british_treaties=british_treaties,
    references=['HISTORY_RESEARCH.md','MD_REFERENCE_LAYOUT.md','MECHANICS_AUDIT.md','OIL_REVISION_AUDIT.md','BRITISH_PATH_HISTORY.md','BRITISH_PATH_MECHANICS.md','STARTING_WITHDRAWAL_CORRECTION_HISTORY.md','STARTING_WITHDRAWAL_CORRECTION_MECHANICS.md'],preview_limits='Faithful proposed grid, native icon pixels, titlebars and font. Browser connector routing, state shading and shine are approximations. Treaty-status selection previews conditions and sample agreement dates; it does not send offers or simulate the full world. This is not an HOI4 screenshot or implemented tree.')

def validate():
    by={n['id']:n for n in nodes}; errors=[]
    for n in nodes:
        if width(n['title'])>143:errors.append(f'Title wider than native field: {n["title"]} ({width(n["title"])})')
        for row in n['prerequisites']:
            for p in row:
                if p not in by:errors.append('Missing predecessor '+p)
                elif by[p]['xy'][1]>=n['xy'][1]:errors.append('Non-downward predecessor '+n['id'])
        for other in n['mutually_exclusive']:
            if n['id'] not in by[other]['mutually_exclusive']:errors.append('Asymmetric exclusion '+n['id'])
        for k in n['modifiers']:
            if k not in labels:errors.append('Unknown modifier '+k)
    for i,n in enumerate(nodes):
        for q in nodes[i+1:]:
            if n['xy'][1]==q['xy'][1] and abs(n['xy'][0]-q['xy'][0])<2:errors.append('Overlapping row '+n['id']+' '+q['id'])
    originals={s['id']:s['modifiers'] for s in spirits}
    def component(completed,spirit,key):
        base=originals[ID(spirit)][key]; credits={}
        for focus in completed:
            for r in next(n for n in nodes if n['id']==ID(focus))['spirit_changes']:
                if r['spirit']!=ID(spirit) or r['component'] not in [key,'all']:continue
                if r['operation']=='remove':relief=abs(base)
                elif r['operation']=='set':relief=abs(base-r['value'])
                else:relief=r['value']
                credits[r['family']]=max(credits.get(r['family'],0),relief)
        return round(max(0,base-sum(credits.values())) if base>0 else min(0,base+sum(credits.values())),8)
    remedy_cases=[
        (['zayed_compact','dual_veto'],'unequal_development','production_speed_buildings_factor',0),
        (['dual_veto','zayed_compact'],'unequal_development','production_speed_buildings_factor',0),
        (['emirate_commands','dual_veto'],'fragmented_authority','army_org_factor',-.03),
        (['dual_veto','emirate_commands'],'fragmented_authority','army_org_factor',-.03),
        (['seven_emirates','federal_ministries'],'fragmented_authority','bureaucracy_cost_multiplier_modifier',.05),
        (['oil_shock_plan','beyond_oil'],'narrow_revenues','civilian_factories_productivity',0),
    ]
    for completed,s,k,expected in remedy_cases:
        actual=component(completed,s,k)
        if actual!=expected:errors.append(f'Remedy mismatch {completed}: {actual}!={expected}')
    capacity={int(k):v for k,v in oil_start['proposed_base'].items()}
    paid_flags=[]
    for phase in oil_phases:
        n=by[phase['focus']];paid_flags.append(n['one_time_delivery_flag'])
        if n['treasury_cost_billion']!=phase['treasury_billion']:errors.append('Oil invoice mismatch '+n['id'])
        for s,amount in phase['resources'].items():capacity[int(s)]+=amount
        if sum(capacity.values())!=phase['cumulative_base']:errors.append('Oil phase arithmetic '+n['id'])
        if n['days']!=phase['days']:errors.append('Oil duration mismatch '+n['id'])
        if n['mutually_exclusive']:errors.append('Oil investment must be compatible '+n['id'])
        for s in phase['resources']:
            if f'{s} = {{ is_owned_by = ROOT is_controlled_by = ROOT }}' not in n['effect_body']:errors.append('Missing state control guard '+n['id'])
        if 'ingame_update_setup = yes' not in n['effect_body']:errors.append('Missing oil economic refresh '+n['id'])
    if capacity!={179:7,180:40} or sum(p['treasury_billion'] for p in oil_phases)!=16.25:errors.append('Oil programme totals')
    if len(set(paid_flags))!=4:errors.append('Oil programme shares payment flag')
    if sum(oil_start['proposed_base'].values())!=4:errors.append('Incorrect low oil start')
    for guard in ['IMP_is_1970_scenario = yes','NOT = { has_country_flag = IMP_1970_gdp_profile_applied }','NOT = { has_country_flag = COLDWAR_UAE_low_oil_start_applied }','179 = { is_owned_by = ROOT is_controlled_by = ROOT }','180 = { is_owned_by = ROOT is_controlled_by = ROOT }']:
        if guard not in oil_start['proposed_effect_body']:errors.append('Missing new-game oil setup guard '+guard)
    if by[ID('onshore_expansion')]['prerequisites']!=by[ID('offshore_expansion')]['prerequisites']:errors.append('Oil paths do not share ownership alternatives')
    baseline=HERE/'OIL_PRESERVATION_BASELINE.json'
    if baseline.exists():
        previous=json.loads(baseline.read_text(encoding='utf-8'))
        current={n['id']:hashlib.sha256(json.dumps({k:n[k] for k in previous['fields']},sort_keys=True).encode()).hexdigest() for n in nodes if n['group'] not in ['oil','british'] and n['id']!=ID('sovereign_union')}
        expected={k:v for k,v in previous['non_oil_nodes'].items() if k!=ID('sovereign_union')}
        if current!=expected:errors.append('Non-oil semantics changed beyond the authorised federation gate')
    british_baseline=HERE/'BRITISH_PRESERVATION_BASELINE.json'
    if british_baseline.exists():
        previous=json.loads(british_baseline.read_text(encoding='utf-8'))
        current={n['id']:hashlib.sha256(json.dumps({k:n[k] for k in previous['fields']},sort_keys=True).encode()).hexdigest() for n in nodes if n['group']!='british' and n['id']!=ID('sovereign_union')}
        if current!=previous['nodes']:errors.append('British revision changed an unrelated existing focus')
    main=by[ID('sovereign_union')]
    if 'is_subject = no' not in main['available'] or 'end_puppet' in main['effect_body']:errors.append('Sovereign formation must require independence and must not release a subject')
    if any('end_puppet' in british_nodes[k]['effect_body'] for k in ['renew_protection','petition_independence']):errors.append('Request focus cannot release a subject')
    if 'end_puppet = UAE' not in british_treaties['release_effect']:errors.append('Missing verified UK-scoped release leaf')
    start=british_treaties['starting_state']
    if start['requires_focus'] or start['requires_new_uk_acceptance'] or not start['starts_with_both_spirits']:errors.append('Historical withdrawal must already exist for both countries without a focus or fresh acceptance')
    if start['historical_execution_date']!='1971.12.1':errors.append('Unexpected historical withdrawal execution date')
    if british_nodes['petition_independence']['title']!='Prepare the Handover' or british_nodes['petition_independence']['diplomatic_offer']['kind']!='early_handover':errors.append('Initial handover focus still requests baseline independence')
    if next(v for v in british_treaties['variants'] if v['id']=='starting')['uae_spirit']!=ID('treaty_dependence'):errors.append('Starting withdrawal duplicates the existing subject spirit')
    for variant in british_treaties['variants']:
        if not all(variant[k] for k in ['uk_spirit','uae_spirit','date','uk_terms','uae_terms']):errors.append('Incomplete bilateral treaty '+variant['id'])
    assert len(by)==len(nodes)
    (HERE/'STRUCTURE_VALIDATION.json').write_text(json.dumps(dict(errors=errors,focuses=len(nodes),decisions=len(decisions),exclusive_pairs=sum(len(n['mutually_exclusive']) for n in nodes)//2,starting_spirits=len(spirits),max_title_width=max(width(n['title']) for n in nodes),remedy_order_cases=len(remedy_cases),oil_phases=4,start_base_oil=4,fully_funded_nominal_base_oil=47,oil_total_cost_billion=16.25,unrelated_existing_focuses_preserved=97,authorised_existing_focus_changes=[ID('sovereign_union')],bilateral_treaty_variants=len(british_treaties['variants'])),indent=2))
    if errors:raise ValueError('\n'.join(errors))

def native_assets():
    reg={}
    for p in (ROOT/'interface').glob('*.gfx'):
        t=p.read_text(encoding='utf-8-sig',errors='replace')
        for m in re.finditer(r'\b(?:spriteType|SpriteType)\s*=\s*\{\s*name\s*=\s*"([^"]+)"\s+texture[Ff]ile\s*=\s*"([^"]+)"',t):reg[m[1]]=(m[2].replace('\\','/'),str(p.relative_to(ROOT)),t[:m.start()].count('\n')+1)
    def uri(im):
        b=io.BytesIO();im.save(b,format='WEBP',lossless=True);return 'data:image/webp;base64,'+base64.b64encode(b.getvalue()).decode()
    assets={'icons':{}};images={};sources={}
    for icon in sorted(set(n['icon'] for n in nodes)):
        rel,definition,line=reg[icon];p=ROOT/rel
        if not p.exists():p=GAME/rel
        im=Image.open(p).convert('RGBA');images[icon]=im;assets['icons'][icon]=uri(im)
        sources[icon]=dict(texture=str(p),definition=definition,line=line,dimensions=list(im.size),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
    assets['font_atlas']=uri(Image.open(ATLAS).convert('RGBA'))
    assets['font_glyphs']={k:[v['x'],v['y'],v['width'],v['height'],v['xoffset'],v['yoffset'],v['xadvance']] for k,v in GLYPHS.items()}
    assets['font_kernings']={str(a)+','+str(b):v for (a,b),v in KERNINGS.items()}
    for key,name in [('available','focus_can_start_bg'),('unavailable','focus_unavailable_bg'),('completed','focus_completed_bg')]:assets[key]=uri(Image.open(GAME/f'gfx/interface/focusview/titlebar/{name}.dds').convert('RGBA'))
    (HERE/'ART_PROVENANCE.json').write_text(json.dumps(sources,indent=2))
    return assets,images

def render():
    assets,images=native_assets()
    fragment=(ROOT/'tools/iraq_1970_concept/tree_fragment.html').read_text(encoding='utf-8')
    fragment=fragment.replace('coldwar-iraq-concept','coldwar-uae-concept').replace('irq-','uae-').replace('Iraq national focus concept','UAE national focus concept').replace('IRAQ · 1 JANUARY 1970','TRUCIAL STATES · 1 JANUARY 1970').replace('Iraq1970','UAE1970').replace('COLDWAR_IRQ','COLDWAR_UAE').replace('The Complete Iraqi Programme','The Complete Emirati Programme').replace('Two horizontal tiers','Three compact tiers')
    fragment=fragment.replace("let current='iran_war',picked='COLDWAR_UAE_iran_arabistan_claim'","let current='british',picked='COLDWAR_UAE_treaty_coast'")
    start=fragment.index('<select id="uae-government"');end=fragment.index('</select>',start)
    fragment=fragment[:start]+'''<select id="uae-government" aria-label="Preview current government"><option value="monarchy">1970 · Council / ruling houses</option><option value="constitutional">Constitutional cabinet · ALT</option><option value="arab_civil">Arab civilian government · ALT</option><option value="arab_officers">Officers’ government · ALT</option><option value="left_communist">Communist cabinet · ALT</option><option value="left_social">Non-aligned social cabinet · ALT</option><option value="islah">Islah cabinet · ALT</option><option value="all">All branches · design view</option>'''+fragment[end:]
    status_control='''<label>Treaty status <select id="uae-treaty-status" aria-label="Preview treaty and independence status"><option value="subject">1970 · Withdrawal announced</option><option value="transition">Signed handover · 1 Dec 1971</option><option value="loyal">Renewed protection agreed</option><option value="free">Independent · release completed</option><option value="friendship">Independent · friendship agreed</option><option value="other">Subject of another country</option></select></label>'''
    fragment=fragment.replace('<div class="uae-camera">',status_control+'<div class="uae-camera">')
    a=fragment.index(' const activeGroups=');b=fragment.index(' function paintGovernment()',a)
    fragment=fragment[:a]+''' const treatyStatus=root.querySelector('#uae-treaty-status');
 const activeGroups={monarchy:['monarchy'],constitutional:['constitutional'],arab_civil:['arab'],arab_officers:['arab'],left_communist:['left'],left_social:['left'],islah:['islah']};
 function available(n){const state=treatyStatus.value,independent=['free','friendship'].includes(state);if(n.diplomatic_state_gate==='independent'&&!independent)return false;if(n.diplomatic_state_gate==='british_subject'&&!['subject','transition','loyal'].includes(state))return false;if(n.diplomatic_state_gate==='british_or_independent'&&state==='other')return false;if(n.diplomatic_state_gate==='protection_agreed'&&state!=='loyal')return false;if(government.value==='all')return true;const g=groups.get(n.group);if(g.outlook==='shared')return true;if(!(activeGroups[government.value]||[]).includes(n.group))return false;
 const party={COLDWAR_UAE_civilian_arabism:'arab_civil',COLDWAR_UAE_officers_republic:'arab_officers',COLDWAR_UAE_social_ownership:'left_communist',COLDWAR_UAE_social_market:'left_social'};return !party[n.id]||party[n.id]===government.value;}
'''+fragment[b:]
    fragment=fragment.replace('<button type="button" id="uae-rules">','<button type="button" id="uae-treaties">UK–UAE Treaty Spirits</button><button type="button" id="uae-rules">')
    fragment=fragment.replace("else if(b.id==='uae-rules')rules();","else if(b.id==='uae-treaties')showTreaties();else if(b.id==='uae-rules')rules();")
    fragment=fragment.replace('government:government.value,view:mode','government:government.value,treatyStatus:treatyStatus.value,view:mode').replace('government:government.value,mode,camera:','government:government.value,treatyStatus:treatyStatus.value,mode,camera:')
    fragment=fragment.replace("government.value=s.government||'saddam';paintGovernment();","government.value=s.government||'saddam';treatyStatus.value=s.treatyStatus||'subject';paintGovernment();")
    fragment=fragment.replace("else if(s.mode==='rules')rules();","else if(s.mode==='rules')rules();else if(s.mode==='treaties')showTreaties();")
    extension=(HERE/'british_view.js').read_text(encoding='utf-8')
    fragment=fragment.replace('})();\n</script>',extension+'\n})();\n</script>')
    fragment+='''<style>
#coldwar-uae-concept .uae-treaty-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:24px}
#coldwar-uae-concept .uae-treaty-heading{display:flex;align-items:center;gap:12px}
#coldwar-uae-concept .uae-treaty-heading img{width:80px;height:80px;object-fit:contain}
#coldwar-uae-concept .uae-treaty-heading h4{margin:0;color:var(--uae-gold)}
#coldwar-uae-concept .uae-treaty-card dt{color:var(--uae-muted);margin-top:12px}
#coldwar-uae-concept .uae-treaty-card dd{margin:3px 0 8px}
#coldwar-uae-concept .uae-treaty-date{color:var(--uae-gold)}
</style>'''
    fragment=fragment.replace("government.value='saddam'","government.value='monarchy'").replace("||'saddam'","||'monarchy'")
    fragment=fragment.replace('min(total positive policy contributions, +15%) + all negative policy contributions. Starting situation penalties remain separate.','min(total positive political-programme contributions, +15 percentage points) + all negative contributions. Starting penalties and permanent national reforms remain separate.')
    fragment=fragment.replace('camera.z<.65','camera.z<.30')
    fragment=fragment.replace('meta.textContent=`${g.label} · ${list.length} focuses ·','meta.textContent=`${g.label} · ${list.length} focuses${current===\'oil\'?\' · Start:4 base oil · Full expansion:$16.25bn\':\'\'} ·')
    fragment=fragment.replace("${n.modifiers.stability_factor>0?", "${n.modifiers.stability_factor>0&&groups.get(n.group).outlook!=='shared'?")
    fragment=fragment.replace('Runs once, after current eligibility, the frozen GDP invoice and native building-capacity checks pass. Unfunded completion becomes pending. New COLDWAR_UAE helpers and condition providers are proposed integration, not existing MD APIs.','Proposed effect body. Verified MD leaf APIs require the described eligibility, affordability and building-capacity guards. COLDWAR_UAE helpers, flags, spirit stage changes and diplomacy wrappers are NEW design work. Modifier contributions need registered dynamic modifiers before they can work. A queued building is not a completed building.')
    fragment=fragment.replace("${v>0?'+':''}${(v*100).toFixed(0)}%","${v>0?'+':''}${(v*100).toFixed(0)}%")
    # Add explicit unlock conditions and structural remedy text outside technical details.
    fragment=fragment.replace('<h4>Proposed effects and costs</h4>','<p>Government / context: ${esc(n.available.replace(/\\n/g," · "))}</p>${n.bypass?`<p>Bypass: ${esc(n.bypass)}. ${esc(n.bypass_contract)}</p>`:""}<h4>Proposed effects and costs</h4>')
    fragment=fragment.replace("<p>Native source-verified: modifier keys, money/literacy effects, construction and political refresh patterns. Proposed: historical roster extensions, leadership bridges, project/contract decisions and all numeric balance. Native focus typography uses the inherited UbuntuBold16 bitmap atlas. Browser approximations remain connector routing, glows and availability. The programme selector changes the camera, never focus coordinates.</p>","<p>MD 2.0.2 reference: native 96 × 130 grid, actual focus icons, titlebars and Ubuntu Bold 16 atlas. Connector routing, shine and availability are browser approximations. Government view demonstrates party gates, not full prerequisite or world-state eligibility. All programme balance and COLDWAR_UAE integration are proposed. No loaded game files changed.</p>")
    # Viewer starts at native scale; inspection remains separate from eligibility.
    shown={**data,'assets':assets}
    fragment=fragment.replace('<!-- DESIGN_DATA -->','<script type="application/json" id="uae-data">'+json.dumps(shown,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+'</script>')
    assert len(fragment.encode())<1_000_000
    (VIZ/'uae-1970-focus-concept.html').write_text(fragment,encoding='utf-8')
    wrapper='<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>COLDWAR UAE concept</title><style>html{background:#152026;color:#eee;font:14px/1.4 Arial,sans-serif}body{margin:0;padding:12px}main{max-width:1400px;margin:auto}</style><main>'+fragment+'</main></html>'
    (HERE/'PREVIEW.html').write_text(wrapper,encoding='utf-8')
    # Full normal-scale proof sheets; same coordinates, icons, atlas and dependency groups.
    bar=Image.open(GAME/'gfx/interface/focusview/titlebar/focus_unavailable_bg.dds').convert('RGBA')
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',16);by={n['id']:n for n in nodes}
    for g in groups:
        ns=[n for n in nodes if n['group']==g['id']];minx=min(n['xy'][0] for n in ns)*96-30;miny=min(n['xy'][1] for n in ns)*130-110
        maxx=max(n['xy'][0] for n in ns)*96+205;maxy=max(n['xy'][1] for n in ns)*130+140
        im=Image.new('RGBA',(maxx-minx,maxy-miny),'#22343c');d=ImageDraw.Draw(im)
        for n in ns:
            x=n['xy'][0]*96-minx;y=n['xy'][1]*130-miny
            for row in n['prerequisites']:
                for parent in row:
                    p=by[parent];px=p['xy'][0]*96-minx;py=p['xy'][1]*130-miny;mid=(py+90+y-26)//2
                    d.line([(px+80,py+90),(px+80,mid),(x+80,mid),(x+80,y-26)],fill='#9aabad',width=2)
            for other in n['mutually_exclusive']:
                if other<n['id']:continue
                q=by[other];qx=q['xy'][0]*96-minx;a=min(x,qx)+139;b=max(x,qx)+27
                for xx in range(a,b,9):d.line([(xx,y+20),(min(xx+4,b),y+20)],fill='#d9a287',width=2)
                d.text(((a+b)//2-4,y-3),'×',font=font,fill='#d9a287')
        for n in ns:
            x=n['xy'][0]*96-minx;y=n['xy'][1]*130-miny;icon=images[n['icon']]
            im.alpha_composite(icon,(int(x+87.5-icon.width/2),int(y+20-icon.height/2)))
            im.alpha_composite(bar,(x+5,y+40));im.alpha_composite(raster(n['title']),(x+15,y+58))
        d.text((18,12),g['label']+' · CONCEPT',font=font,fill='#e3cf90')
        d.text((18,38),'Native art and grid · '+str(len(ns))+' focuses',font=font,fill='#c4cdcb')
        im.convert('RGB').save(HERE/f'BRANCH_{g["id"]}.png')
    print(json.dumps(dict(focuses=len(nodes),decisions=len(decisions),bytes=len(fragment.encode()),fragment=str(VIZ/'uae-1970-focus-concept.html'))))

if __name__=='__main__':
    validate()
    (HERE/'COLDWAR_UAE_1970_CONCEPT.json').write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding='utf-8')
    render()
