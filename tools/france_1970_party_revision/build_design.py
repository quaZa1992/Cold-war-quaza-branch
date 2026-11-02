# IMPERIA COLD WAR — France party-specific cooperation proposal.
"""Write reviewable proposal data only. Never compile or edit loaded game files."""
from __future__ import annotations
from copy import deepcopy
from decimal import Decimal
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE = ROOT / 'tools/france_1970_runtime/runtime_design.json'

def money(percent):
    return dict(kind='treasury_gdp', percent=-percent, gdp_fraction=float(-Decimal(str(percent))/100), runtime_share_literal=f'{-Decimal(str(percent))/100:.5f}', base='gdp_total', payer='own_country', valuation='at_payment', once=True)
def weekly(percent):
    return dict(kind='weekly_gdp_expense', annual_gdp_percent=percent, gdp_fraction=float(Decimal(str(percent))/100), runtime_share_literal=f'{Decimal(str(percent))/100:.5f}', base='gdp_total', payer='own_country', valuation='weekly_recalculation', divisor=52)
def mod(key,value): return dict(kind='modifier',key=key,value=value)
def research(category,bonus=.5,uses=1): return dict(kind='research',category=category,bonus=bonus,uses=uses,once=True)
def building(state,kind): return dict(kind='building',state=state,building=kind,amount=1,slots=1,slots_before_construction=True,once=True)
def opinion(faction,value): return dict(kind='faction_opinion',faction=faction,value=value,provider='change_'+faction+'_opinion',parameter='temp_opinion',once=True)
def experience(service,amount): return dict(kind='experience',service=service,amount=amount,once=True)
def doctrine(category,reduction=.25): return dict(kind='doctrine',category=category,reduction=reduction,uses=1,once=True)
def unlock(key,title): return dict(kind='unlock_decision',id='COLDWAR_FRA2P_'+key,label=title)


def build():
    raw=BASE.read_bytes()
    baseline=json.loads(raw)
    d=deepcopy(baseline)
    bykey={n['key']:n for n in d['nodes']}
    before={n['key']:deepcopy(n) for n in d['nodes']}
    groups={g['id']:g for g in d['groups']}
    reasons={}
    sources={}
    def rewrite(key,effects,why,description=None):
        n=bykey[key]
        # Preserve every existing starting-problem remedy unless explicitly replaced.
        effects=deepcopy(effects)
        for e in n['effects']:
            if e['kind']=='remove_spirit' and e not in effects: effects.append(deepcopy(e))
        n['effects']=effects
        if description: n['description']=description
        reasons[key]=why
        n['proposal_change']='revised'
    def add(key,group,title,x,y,parents,description,icon):
        n=dict(id='COLDWAR_FRA2_'+key,key=key,group=group,title=title,full_title=title,x=x,y=y,description=description,
               effects=[],prerequisites=parents,exclusions=[],cost=7,days=49,conditions=[groups[group]['trigger']+' = yes'],
               reward_guards=[groups[group]['trigger']+' = yes'],basis='Counterfactual governing programme based on historical institutions',
               lifetime='government',spirit='COLDWAR_FRA2_'+group+'_programme',spirit_name=groups[group]['title']+' Programme',
               icon='COLDWAR_FRA2_focus_'+icon,icon_source=icon,proposal_change='new')
        bykey[key]=n;d['nodes'].append(n);reasons[key]='New substantive continuation of the chosen party policy.'
        return n
    def offer(key,partner,partner_name,title,fra,other,fees,rates,why,description,parents=(),members=()):
        n=bykey[key];g=groups[n['group']]
        conditions=[g['trigger']+' = yes']
        if key=='fn_export': conditions.append('FN identity')
        for tag,idea in members: conditions.append(('has_idea = '+idea) if tag=='FRA' else tag+' = { has_idea = '+idea+' }')
        activation=[tag+' = { has_idea = '+idea+' }' for tag,idea in members]
        for parent in parents:
            po=bykey[parent]['offer']
            for side,tag in [('france','FRA'),('recipient',partner)]:
                idea=po[side]['spirit']
                conditions.append(('has_idea = '+idea) if tag=='FRA' else tag+' = { has_idea = '+idea+' }')
                activation.append(tag+' = { has_idea = '+idea+' }')
        n['conditions']=conditions;n['reward_guards']=deepcopy(conditions)
        n.pop('activation_conditions',None)
        n['lifetime']='treaty'
        n['basis']='Proposed alternate-history agreement, grounded in historical policy and cooperation precedents.'
        n['effects']=[unlock(key+'_response',partner_name+': acceptance or refusal')]
        n['description']=description
        n['offer']={
            'partner':partner,'partner_name':partner_name,'family':'party_'+key,
            'france':dict(spirit='COLDWAR_FRA2P_'+key+'_france',name=title+': France',picture=g['idea_picture'],effects=[money(fees[0]),weekly(rates[0]),*fra],payer='FRA'),
            'recipient':dict(spirit='COLDWAR_FRA2P_'+key+'_'+partner,name=title+': '+partner_name,picture=g['idea_picture'],effects=[money(fees[1]),weekly(rates[1]),*other],payer=partner),
            'activation_conditions':activation,
            'proposal_party':g['id'],'proposal_party_trigger':g['trigger'],
            'acceptance_conditions':['Both countries exist','Bilateral peace','No native embargo or mirrored diplomatic, financial, economic or military sanction in either direction',*activation],
            'acceptance_transaction':'The named recipient decides. Recheck the complete package before either payer is charged.',
            'payment_contract':'Each signatory pays its own current GDP share at acceptance. Annual GDP shares are divided by 52 for weekly funding.',
            'asset_execution':'Validate ownership, full control and native physical capacity. Add the shared slots before each building within the one-time transaction.',
            'signature_lifetime':'Standing state agreement. Signature survives elections; suspend both spirits and weekly funding for invalid bilateral relations or lost active parent/membership. Never replay setup or finite awards.',
            'historical_status':'Proposed alternate-history party programme; historical precedents are recorded separately.'}
        reasons[key]=why;n['proposal_change']='new' if key not in before else 'revised'
    # Concrete domestic choices. Replace existing generic rewards, rather than stack them.
    rewrite('participation',[money(.10),opinion('labour_unions',10),opinion('industrial_conglomerates',-5),mod('civilian_factories_productivity',.03),mod('corporate_tax_income_multiplier_modifier',-.04),unlock('participation_workshops','Fund Participation Workshops')],
            'Profit-sharing earns labour cooperation and a paid technical-training project instead of another military efficiency increment.')
    rewrite('management',[opinion('industrial_conglomerates',10),opinion('labour_unions',-10),mod('civilian_factories_productivity',.04),mod('offices_productivity',.03),mod('corporate_tax_income_multiplier_modifier',.03),research('CAT_electronics',.25)],
            'Professional management favours services and finite electronics expertise; it retains the labour opposition.')
    rewrite('debre',[mod('industrial_capacity_factory',.05),mod('equipment_cost_multiplier_modifier',.06),research('CAT_armor'),experience('army',15)],
            'Industrial sovereignty retains its costly military specialisation and adds actual procurement/training experience.')
    rewrite('sound_franc',[money(.08),mod('offices_productivity',.04),mod('corporate_tax_income_multiplier_modifier',.03),mod('civilian_factories_productivity',-.03)],
            'The disciplined-franc route favours financial services and receipts, with a real demand/output sacrifice.')
    rewrite('credit_expansion',[money(.35),research('CAT_industry'),mod('production_speed_industrial_complex_factor',.08),mod('corporate_tax_income_multiplier_modifier',-.04)],
            'Modernisation credit buys an industrial research window and faster civilian investment at the cost of fiscal concessions.')
    rewrite('regional_councils',[money(.30),building(64,'infrastructure'),mod('political_power_factor',-.03),opinion('farmers',5)],
            'Devolution delivers a funded regional asset and a rural constituency benefit, while weakening central political control.')
    rewrite('mutuals',[money(.25),building(56,'offices'),mod('health_cost_multiplier_modifier',-.04),mod('social_cost_multiplier_modifier',.05),opinion('labour_unions',5)],
            'Mutual insurance adds an actual local-service facility to the insurance reform, with continuing social expenditure.')
    rewrite('left_radicals',[money(.12),opinion('labour_unions',10),research('CAT_industry',.25),mod('offices_productivity',.03),mod('social_cost_multiplier_modifier',.04)],
            'Republican-left policy gains organised labour, civilian expertise and services rather than a generic stability bundle.')
    rewrite('secular_school',[money(.25),research('CAT_electronics'),research('CAT_industry'),mod('education_cost_multiplier_modifier',.08)],
            'Technical schooling grants two distinct finite research awards and preserves its real education budget and starting-spirit remedy.')
    rewrite('public_banks',[money(.50),building(56,'offices'),mod('offices_productivity',.03),mod('bureaucracy_cost_multiplier_modifier',.03),unlock('regional_conversion','Regional Conversion Fund')],
            'Public banks gain a concrete paid industrial lending programme; reduce the old generic service/bureaucracy multipliers.')
    rewrite('social_contract_ps',[money(.20),opinion('labour_unions',15),opinion('industrial_conglomerates',-10),mod('civilian_factories_productivity',.03),mod('social_cost_multiplier_modifier',.06)],
            'A negotiated labour compact changes real faction relationships and civilian productivity, with a payroll/social bill.')
    rewrite('democratic_road',[research('CAT_industry'),opinion('labour_unions',10),mod('foreign_influence_defense_modifier',.04),mod('political_power_factor',-.05)],
            'A pluralist PCF course offers domestic skills and autonomy, rather than only a stability reward.')
    rewrite('party_discipline',[money(.10),research('CAT_industry'),mod('production_factory_efficiency_gain_factor',.04),mod('political_power_factor',.06),mod('stability_factor',-.04)],
            'Cadre coordination provides finite planning expertise and production learning, retaining the legitimacy cost.')
    rewrite('planned_targets',[mod('production_speed_arms_factory_factor',.10),research('CAT_industry'),mod('production_factory_max_efficiency_factor',.05),mod('civilian_factories_productivity',-.03)],
            'Production planning accelerates a specific investment class and line maturity; household production still loses priority.')
    rewrite('decentralised_services',[money(.25),building(58,'offices'),mod('health_cost_multiplier_modifier',-.03),mod('education_cost_multiplier_modifier',.06)],
            'Local services become a funded facility and health-efficiency reform, rather than a generic industrial research coupon.')
    rewrite('civilian_republic',[research('CAT_industry'),mod('offices_productivity',.05),mod('military_factories_productivity',-.03),mod('war_support_factor',-.06)],
            'Civilian conversion shifts the actual economic sector mix; it does not create an unexplained army payroll rebate.')
    rewrite('citizen_defence',[experience('army',20),doctrine('land_doctrine'),mod('supply_consumption_factor',-.03),mod('army_personnel_cost_multiplier_modifier',.04)],
            'Citizen defence funds training, doctrine and logistics, with a continuing personnel bill instead of another core-defence stack.')
    rewrite('efficiency_ecology',[money(.20),research('CAT_energy'),mod('energy_use_modifier_civs',-.04),mod('education_cost_multiplier_modifier',.03)],
            'Conservation combines immediate lower demand with paid technical training and a finite energy research award.')
    rewrite('land_stewardship',[money(.25),building(59,'agriculture_district'),opinion('farmers',10),mod('agricolture_productivity_modifier',.03),mod('social_cost_multiplier_modifier',.04)],
            'Rural stewardship combines a productive asset, farmer support and a narrow agricultural gain, with rural-service costs.')
    rewrite('fn_protection',[money(.65),building(54,'arms_factory'),building(57,'industrial_complex'),research('CAT_industry',.25),mod('civilian_factories_productivity',-.03),mod('foreign_influence_modifier',-.05)],
            'Protection buys a costly domestic industrial base; inefficient input allocation and diplomatic isolation remain real costs.')
    rewrite('fn_defence',[experience('army',25),doctrine('land_doctrine'),mod('max_planning',.05),mod('army_personnel_cost_multiplier_modifier',.08),mod('social_cost_multiplier_modifier',.03)],
            'The armed nation gains an actual training and planning programme instead of stacking another general core-defence buff.')

    # Party-specific offers. These replace the old focus rewards in full.
    eu=(('FRA','EU_member'),('GER','EU_member'))
    offer('pompidou_europe','GER','Federal Republic of Germany','Rhenish Regional Investment',
          [building(57,'infrastructure'),mod('civilian_factories_productivity',.02),mod('corporate_tax_income_multiplier_modifier',-.02)],
          [building(42,'infrastructure'),mod('offices_productivity',.03),mod('corporate_tax_income_multiplier_modifier',-.02)],(.25,.25),(.04,.04),
          'The Hague Opening becomes a reciprocal regional investment proposal, with real assets and co-financing rather than an influence-only reward.',
          'Use the opening after The Hague to finance industrial links and regional services on both sides of the Rhine. Each government retains authority over its own investment.',members=eu)
    offer('atlantic_liberal','USA','United States','Atlantic Electronics Licensing',
          [research('CAT_electronics',.5,2),mod('offices_productivity',.03),mod('foreign_influence_defense_modifier',-.04)],
          [building(811,'offices'),research('CAT_electronics',.25),mod('corporate_tax_income_multiplier_modifier',-.02)],(.30,.20),(.05,.03),
          'Liberal Atlantic policy exchanges licensing access for a real US engineering/marketing foothold; no broad equipment-cost discount.',
          'Negotiate licensing, technical support and export access with American electronics firms. Faster access to expertise comes with dependence on foreign standards and patent terms.')
    offer('europe_liberal','GER','Federal Republic of Germany','European Export Credit Facility',
          [building(56,'offices'),mod('corporate_tax_income_multiplier_modifier',.04),mod('tax_gain_multiplier_modifier',-.02)],
          [building(42,'offices'),mod('corporate_tax_income_multiplier_modifier',.04),mod('tax_gain_multiplier_modifier',-.02)],(.30,.30),(.05,.05),
          'The European option funds a reciprocal credit/insurance facility, distinct from the electronics licensing route.',
          'Underwrite eligible cross-border orders through French and German institutions. Additional business receipts must be weighed against public guarantees and the risk of loss.',members=eu)
    offer('federal_europe','GER','Federal Republic of Germany','Mutual Insurance Cooperation',
          [mod('health_cost_multiplier_modifier',-.03),mod('offices_productivity',.03),mod('education_cost_multiplier_modifier',.03)],
          [mod('health_cost_multiplier_modifier',-.03),mod('offices_productivity',.03),mod('education_cost_multiplier_modifier',.03)],(.20,.20),(.04,.04),
          'Christian-democratic European policy gains a distinct civilian insurance/service programme, not a second industrial treaty.',
          'Exchange insurance administration, professional training and local-care practice between French mutual societies and German partners. Skilled staff and compatible rules require continuing investment.',members=eu)
    offer('atlantic_security','ENG','United Kingdom','Channel Maritime Schools',
          [experience('navy',15),doctrine('naval_doctrine'),research('CAT_naval'),mod('naval_accidents_chance',-.04),mod('navy_personnel_cost_multiplier_modifier',.04)],
          [experience('navy',15),doctrine('naval_doctrine'),research('CAT_naval'),mod('naval_accidents_chance',-.04),mod('navy_personnel_cost_multiplier_modifier',.04)],(.20,.20),(.04,.04),
          'Atlantic security funds actual reciprocal schooling and maritime safety; remove the old unrelated education/army cost rebates.',
          'Pool selected courses in navigation, engineering and maritime safety while preserving national command. The arrangement requires trained instructors and naval personnel on both sides.',members=(('FRA','NATO_member'),('ENG','NATO_member')))
    offer('europe_technology','GER','Federal Republic of Germany','European Computing Consortium',
          [building(56,'offices'),research('CAT_electronics',.5,2),mod('corporate_tax_income_multiplier_modifier',-.03)],
          [building(42,'offices'),research('CAT_electronics',.5,2),mod('corporate_tax_income_multiplier_modifier',-.03)],(.35,.35),(.06,.06),
          'The Radical technology route becomes a CII-Siemens-style programme, with two physical research/service centres and reciprocal obligations.',
          'Support a French-German computing consortium inspired by the European partnerships of the early 1970s. Shared development distributes costs, but product standards and procurement remain contested.')
    offer('europe_restraint','GER','Federal Republic of Germany','European Monetary Cooperation',
          [building(56,'offices'),mod('tax_gain_multiplier_modifier',.04),mod('social_cost_multiplier_modifier',-.03),mod('stability_factor',-.03)],
          [building(42,'offices'),mod('offices_productivity',.04),mod('tax_gain_multiplier_modifier',.02),mod('political_power_factor',-.02)],(.25,.20),(.04,.04),
          'Monetary restraint offers funded bilateral financial coordination and differentiated returns; it does not adopt the euro or waive native currency rules.',
          'Coordinate financial institutions and budget priorities with West Germany. France gains room for monetary discipline at the price of domestic restraint, while Germany commits administrative and political resources.',members=eu)
    offer('sovereign_reflation','ALG','Algeria','Mediterranean Development Credit',
          [research('CAT_industry'),mod('civilian_factories_productivity',.03),mod('corporate_tax_income_multiplier_modifier',-.03)],
          [building(386,'industrial_complex'),mod('civilian_factories_productivity',.04),mod('tax_gain_multiplier_modifier',-.02)],(.50,.30),(.07,.04),
          'Sovereign reflation opens a public-credit-led development alternative with Algeria, instead of an unreciprocated construction modifier.',
          'Finance agreed industrial orders and local production through French public credit and Algerian partners. Development supports demand in both countries, with credit exposure and costly concessions.',parents=('algeria_energy',))
    offer('independent_communism','ITA','Italy','European Cooperative Partnership',
          [building(57,'offices'),research('CAT_industry',.25,2),mod('foreign_influence_defense_modifier',.04),mod('social_cost_multiplier_modifier',.03)],
          [building(265,'offices'),research('CAT_industry',.25,2),mod('civilian_factories_productivity',.03),mod('corporate_tax_income_multiplier_modifier',-.02)],(.25,.25),(.04,.04),
          'The independent PCF course gains its own reciprocal European cooperative programme rather than merely declining Soviet benefits.',
          'Develop cooperative finance, worker participation and municipal expertise with Italian partners. A French communist government can pursue practical European cooperation without yielding its political autonomy.')
    offer('soviet_friendship','SOV','Soviet Union','Franco-Soviet Industrial Partnership',
          [building(62,'industrial_complex'),mod('production_speed_industrial_complex_factor',.06),mod('foreign_influence_defense_modifier',-.03)],
          [building(661,'industrial_complex'),mod('civilian_factories_productivity',.03),mod('corporate_tax_income_multiplier_modifier',-.02)],(.45,.45),(.06,.06),
          'Replace the unilateral land-doctrine reward with a real PCF-originated industrial agreement and separately paid gains for both countries.',
          'Offer French industrial equipment, engineering and production cooperation to the Soviet government. A ratified programme would support French orders and additional Soviet productive capacity. Bilateral restrictions must first be lifted.')
    bykey['soviet_friendship']['icon']='COLDWAR_FRA2_focus_industry_military';bykey['soviet_friendship']['icon_source']='industry_military'
    add('pcf_energy_contract','pcf','Energy Engineering',69,5,[['soviet_friendship']],
        'Extend the industrial partnership into energy engineering, conservation and technical exchange. The programme concentrates scarce specialists on energy and deepens a long-term commercial relationship.','powerplant')
    offer('pcf_energy_contract','SOV','Soviet Union','Franco-Soviet Energy Engineering',
          [research('CAT_energy',.5,2),mod('energy_use_modifier_civs',-.04),mod('foreign_influence_defense_modifier',-.04)],
          [research('CAT_energy',.5,2),mod('energy_gain_multiplier',.06),mod('education_cost_multiplier_modifier',.03)],(.20,.20),(.08,.05),
          'A scarce engineering-budget choice: conservation and generation expertise, not an unsupported guaranteed gas/resource transfer.',
          'Concentrate the industrial partnership on joint energy studies, equipment and efficient use. France lowers industrial demand; Soviet partners improve generation and fund specialist training.',parents=('soviet_friendship',))
    add('pcf_shipping_contract','pcf','Shipping Protocol',73,5,[['soviet_friendship']],
        'Extend cooperation through shipbuilding, repair and commercial maritime administration. Additional orders must share the benefits of port access and compete with other industrial priorities.','french_army_navy')
    offer('pcf_shipping_contract','SOV','Soviet Union','Franco-Soviet Maritime Cooperation',
          [building(64,'dockyard'),research('CAT_naval'),mod('dockyard_productivity',.04),mod('corporate_tax_income_multiplier_modifier',-.03)],
          [building(652,'offices'),research('CAT_naval',.25,2),mod('offices_productivity',.03),mod('tax_gain_multiplier_modifier',-.02)],(.30,.25),(.05,.05),
          'A rival maritime investment package: a real French yard, Soviet commercial administration and reciprocal finite naval engineering knowledge.',
          'Concentrate the industrial partnership on maritime engineering, repair orders and commercial administration. French yards and Soviet commercial services would share funded investment and technical work.',parents=('soviet_friendship',))
    bykey['pcf_energy_contract']['exclusions']=['pcf_shipping_contract'];bykey['pcf_shipping_contract']['exclusions']=['pcf_energy_contract']
    bykey['pcf_energy_contract']['offer']['family']='party_pcf_soviet_specialisation'
    bykey['pcf_shipping_contract']['offer']['family']='party_pcf_soviet_specialisation'
    bykey['communist_settlement']['y']=6
    bykey['communist_settlement']['prerequisites']=[['independent_communism','pcf_energy_contract','pcf_shipping_contract']]
    reasons['communist_settlement']='Consolidation follows the actual selected reciprocal programme instead of bypassing the new specialisation.'
    add('psu_cooperative_exchange','psu','Cooperative Pact',75,2,[['self_management']],
        'Develop a bounded exchange of worker-managed enterprise practice with Yugoslav partners. Commercial accountability and the diversity of local institutions remain essential.','french_union')
    offer('psu_cooperative_exchange','SER','Yugoslavia','Worker-Managed Enterprise Exchange',
          [research('CAT_industry',.5,2),mod('civilian_factories_productivity',.03),mod('corporate_tax_income_multiplier_modifier',-.02)],
          [research('CAT_industry',.5,2),mod('offices_productivity',.03),mod('education_cost_multiplier_modifier',.03)],(.20,.20),(.03,.03),
          'A PSU-specific reciprocal self-management exchange, grounded in French and Yugoslav institutional debates rather than a Soviet-alignment copy.',
          'Exchange enterprise experience and applied industrial expertise with Yugoslav partners. Both countries fund training, while French cooperatives accept commercial discipline and Yugoslav institutions commit skilled staff.')
    add('psu_union_institutes','psu','Union Institutes',83,2,[['union_autonomy']],
        'Build bargaining and technical institutes for independent unions. A domestic network can serve workplaces without relying on a foreign agreement, but requires public funding and employer concessions.','french_union')
    rewrite('psu_union_institutes',[money(.35),building(55,'offices'),research('CAT_industry',.25,2),opinion('labour_unions',10),mod('corporate_tax_income_multiplier_modifier',-.02)],
            'The independent-union route receives an equally useful domestic continuation instead of being a dead end beside the Yugoslav pact.')
    offer('ecological_industry','GER','Federal Republic of Germany','Rhine Clean Production Commission',
          [building(57,'offices'),research('CAT_energy'),mod('energy_use_modifier_civs',-.04),mod('industrial_capacity_factory',-.02)],
          [building(42,'offices'),research('CAT_energy'),mod('energy_use_modifier_civs',-.04),mod('industrial_capacity_factory',-.02)],(.30,.30),(.05,.05),
          'Industrial conversion gains a reciprocal engineering/monitoring institution and lower energy demand; stricter production costs remain visible.',
          'Coordinate industrial conservation and clean-production engineering along the Rhine. Technical offices and shared research support conversion, while stricter operating practice reduces immediate factory output.')
    offer('local_sufficiency','AUS','Austria','Municipal Heat Cooperation',
          [building(62,'infrastructure'),research('CAT_energy'),mod('energy_use_modifier_civs',-.05),mod('industrial_capacity_factory',-.03)],
          [research('CAT_energy',.5,2),mod('energy_gain_multiplier',.03),mod('energy_use_modifier_civs',-.03),mod('corporate_tax_income_multiplier_modifier',-.02)],(.25,.20),(.03,.03),
          'Local sufficiency becomes a distinct municipal heating/technical programme, with a French regional asset and Austrian engineering returns.',
          'Develop municipal heat networks and local energy engineering with Austrian partners. France prioritises regional services over heavy throughput; Austria funds efficient generation and technical exchange.')
    offer('fn_export','ARG','Argentina','Naval Aviation Export Support',
          [research('CAT_aircraft'),opinion('industrial_conglomerates',5),mod('corporate_tax_income_multiplier_modifier',.05),mod('foreign_influence_defense_modifier',-.04)],
          [experience('air',20),research('CAT_aircraft'),mod('air_training_xp_gain_factor',.10),mod('air_accidents_factor',-.05),mod('airforce_personnel_cost_multiplier_modifier',.04)],(.12,.35),(.03,.06),
          'The counterfactual nationalist export route gains a real consenting customer and reciprocal aviation expertise, with market dependence and training costs.',
          'Offer a funded aviation training, engineering and export-support programme to Argentina, drawing on the historical French aircraft relationship. Orders support French firms; Argentina pays for instruction and sustained readiness.')

    # Two explicit new national project decisions: complete numeric effects are inspectable.
    d['decisions'].extend([
        dict(id='COLDWAR_FRA2P_participation_workshops',title='Fund Participation Workshops',days=None,
             conditions=['Gaullist Participation completed',groups['udr']['trigger']+' = yes','Own and fully control Rhone-Alpes (62)','Native office capacity','Once only'],
             effects=[money(.20),building(62,'offices'),research('CAT_industry')]),
        dict(id='COLDWAR_FRA2P_regional_conversion',title='Regional Conversion Fund',days=None,
             conditions=['Public Bank Credit completed',groups['ps']['trigger']+' = yes','Own and fully control Hauts-de-France (54)','Native civilian-factory capacity','Once only'],
             effects=[money(.40),building(54,'industrial_complex'),research('CAT_industry')]),
    ])
    # Implementation requirements are recorded separately from player-facing prose.
    for decision,focus,group,state,btype in [
        ('COLDWAR_FRA2P_participation_workshops','participation','udr',62,'offices'),
        ('COLDWAR_FRA2P_regional_conversion','public_banks','ps',54,'industrial_complex')]:
        dec=next(x for x in d['decisions'] if x['id']==decision)
        dec['runtime_guards']=[
            'COLDWAR_FRA2_is_1970 = yes',
            'NOT = { has_country_flag = '+decision+'_completed }',
            groups[group]['trigger']+' = yes',
            'has_completed_focus = COLDWAR_FRA2_'+focus,
            'check_variable = { gdp_total > 0 }',
            'owns_state = '+str(state),'has_full_control_of_state = '+str(state),
            str(state)+' = { check_variable = { var = building_level@'+btype+' value = 49 compare = less_than_or_equals } }']
    # Full graph remains visible; preserve exact anchors and update local offsets.
    for n in d['nodes']:
        if n['key'] not in before: n['anchor']='COLDWAR_FRA2_'+('advanced_democracy' if n['group']=='pcf' else 'grassroots_left')
        if n.get('anchor'):
            anchor=next(a for a in d['nodes'] if a['id']==n['anchor'])
            n['offset']=[n['x']-anchor['x'],n['y']-anchor['y']]
        else: n['offset']=[n['x'],n['y']]
    # The authorising party matters at proposal/acceptance. Signed state pacts persist;
    # the separately earned domestic party programmes still detach outside office.
    d['project']='IMPERIA COLD WAR'
    d['status']='PROPOSED PARTY REVISION. Not installed in the game.'
    d['revision']='FRA2 party revision 2.0: reciprocal party programmes'
    d['navigation']['initial_focus']='COLDWAR_FRA2_soviet_friendship'
    d['navigation']['initial_government']='pcf'
    d['navigation']['preview_section']='pcf'
    d['proposal_rules']={
        'costs':'Setup fees use the payer\'s own current GDP. Weekly funding is the payer\'s annual GDP share divided by 52.',
        'consent':'Every foreign package originates in its named party focus. The named recipient accepts or refuses.',
        'lifetime':'Domestic party modifiers suspend outside government and restore without replay. Signed state agreements survive elections; both countries\' spirits suspend for war, embargo, sanctions or invalid active parent/membership.',
        'slots':'Each building level adds one shared slot in the same state before construction, within the one-time transaction.',
        'source':'Historical precedents support the policies; the party-government packages and balance values are proposed alternate history.'}
    changes=[]
    for n in d['nodes']:
        if n['key'] in reasons:
            changes.append(dict(key=n['key'],group=n['group'],change_type='revised' if n['key'] in before else 'new',reason=reasons[n['key']],before=before.get(n['key']),after=deepcopy(n)))
    assert len(d['nodes'])==156
    new_offers=[n for n in d['nodes'] if n.get('offer') and n['key'] in reasons]
    assert len(new_offers)==16, len(new_offers)
    assert sum('offer' in n for n in d['nodes'])==35
    HERE.mkdir(parents=True,exist_ok=True)
    frozen=HERE/'BASELINE.json'
    if frozen.exists(): assert frozen.read_bytes()==raw, 'Current installed design differs from the proposal baseline.'
    else: frozen.write_bytes(raw)
    (HERE/'proposal.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report=dict(project='IMPERIA COLD WAR',status='Proposal only',baseline_sha256=hashlib.sha256(raw).hexdigest(),
                focuses_before=152,focuses_after=156,new_party_offers=16,total_offers=35,changed_focuses=len(changes),changes=changes)
    (HERE/'CHANGES.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest=json.loads((ROOT/'tools/france_1970_runtime/manifest.json').read_text(encoding='utf-8'))
    baseline_record=dict(project='IMPERIA COLD WAR',runtime_design_sha256=hashlib.sha256(raw).hexdigest(),
                         loaded_files={r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in manifest['files'] if r.startswith(('common/','history/','interface/','localisation/','events/'))})
    target=HERE/'RUNTIME_BASELINE.json'
    if target.exists(): assert json.loads(target.read_text())==baseline_record, 'Loaded runtime drifted during proposal work.'
    else: target.write_text(json.dumps(baseline_record,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='changes'},indent=2))

if __name__=='__main__': build()
