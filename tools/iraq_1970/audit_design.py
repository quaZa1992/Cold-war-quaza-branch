# IMPERIA CW — Cold War: iraq 1970 — audit design.
"""Approved 2026-10-19 audit revision; pure, repeatable design assembly.

The earlier approved catalogue remains an immutable migration baseline. All
current generators consume this assembled revision, not separate stale copies.
Retired focus IDs remain hidden compatibility entries for existing saves.
"""
from pathlib import Path
import json, hashlib
from copy import deepcopy

HERE=Path(__file__).resolve().parent
P='COLDWAR_IRQ_'
REVISION='audit_2026_10_19_v2'
BASELINE='82deef2b498d5e67d2b5dc157eda3ba534c2a8d35de215e7f7de679ffcc24eff'
DESCRIPTIONS={
 P+'oil_nationalize': 'Iraq can bring the IPC installations under national ownership and direct their revenues toward its own development. Operating the fields will be only part of the struggle: a dispute with the old consortium can disrupt buyers and export arrangements while a new settlement is established.',
 P+'saddam_legacy': 'The presidency must turn competing offices and personal loyalties into an administration that can carry out its decisions. A clearer chain of authority will reduce duplicated work and strengthen executive direction, while concessions to the institutions that sustain the regime narrow the state’s revenue base.',
 P+'icp_front_strategy': 'Ministries must answer to an agreed cabinet programme rather than to rival party chains of command. Communist participation in government gives us the opportunity to establish enforceable responsibilities, while preserving the legal guarantees on which cooperation with other parties depends.',
 P+'icp_independent_strategy': 'The party now carries responsibility for the state. Its regional committees need trained administrators and reliable communications, but a governing apparatus must also learn to distinguish the needs of public service from the demands of party discipline.',
 P+'icp_legal_cells': 'Legal party offices can connect Baghdad with workers and local representatives who endured years of repression. Bringing these networks into public life requires offices, accountable organisers and confidence that membership will no longer expose families to arbitrary punishment.',
 P+'icp_underground': 'Years of clandestine organisation left experienced cadres outside normal public administration. Reuniting those networks with the governing party will strengthen its reach, provided security habits do not become a substitute for competent civilian institutions.',
 P+'aziz_negotiated_road': 'Aziz Muhammad must turn a national mandate into a functioning cabinet. Experienced coalition ministers can broaden the government’s expertise, while clearly defined responsibilities prevent competing party organisations from paralysing decisions.',
 P+'aziz_opposition_road': 'Local congresses can give the party leadership a stronger mandate beyond Baghdad. Their delegates expect influence over appointments and policy, obliging the secretariat to reconcile regional demands with the discipline needed to govern.',
 P+'aziz_united_opposition': 'A socialist government cannot treat every disagreement as disloyalty. Parliamentary allies, workplace representatives and provincial delegates need a recognised channel to challenge ministers without dismantling the institutions through which they govern together.',
 P+'aziz_safe_return': 'Exile dispersed Iraqi political experience across neighbouring countries and beyond. Returning organisers can rebuild public institutions and reconnect divided families, but their appointment must rest on an agreed role in the new administration.',
 P+'kdp_common_republic': 'The republic must honour the settlement through which its communities agreed to govern together. Regional services, security arrangements and public revenue should follow that agreement, whether its chosen form is autonomy or a federal constitution.',
 P+'foreign_debt_diplomacy': 'Wartime credit binds Baghdad to neighbouring governments long after the fighting ends. A regional settlement can reduce uncertainty over repayment, but every creditor retains its own interests and must accept the terms offered by Iraq.',
 P+'iran_operational_plan': 'A southern campaign requires more than a map of the frontier. Commanders need a realistic estimate of Iran’s forces, an operational objective and reliable access to fuel, replacement equipment and finance. The choice between a concentrated opening and a prolonged struggle will shape those preparations.',
 P+'iran_tehran_assessment': 'Apparent strength or weakness across the frontier does not reveal how Iran’s armed forces would fight an invasion. Iraqi planners must examine command, mobilisation and supply before treating a favourable report as an opportunity for a southern campaign.',
}

def baseline():
    raw=(HERE/'approved_iraq.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==BASELINE,'Historical audit baseline changed'
    return json.loads(raw.decode('utf-8-sig'))

def _structure(data,retired):
    nodes=data['nodes']; by={n['id']:n for n in nodes}
    def n(key):return by[P+key]
    def parents(key,*groups):n(key)['prerequisites']=[[P+x for x in g] for g in groups]
    def move(key,x,y):n(key)['xy']=[x,y]
    # Administrative entry cards are removed rather than made prerequisites of
    # the opposite mutually-exclusive choice. Other merged deliveries redirect.
    splice={P+x for x in ('industry_survey','defence_accounts','society_literacy_accounts')}
    original=baseline(); old={x['id']:x for x in original['nodes']}
    def redirected(fid):
        seen=set()
        if fid==P+'agri_wasit':return P+'agri_large_irrigation'
        while fid in retired and fid not in splice:
            assert fid not in seen,('Retirement cycle',fid)
            seen.add(fid);fid=retired[fid]
        return fid
    for node in nodes:
        if node['id'] in retired:continue
        result=[]
        for group in node['prerequisites']:
            if any(p in splice for p in group):
                assert len(group)==1,('Entry splice needs explicit grouping',node['id'],group)
                result.extend(deepcopy(old[group[0]]['prerequisites']))
            else:
                opts=list(dict.fromkeys(redirected(p) for p in group))
                opts=[p for p in opts if p!=node['id']]
                if opts:result.append(opts)
        node['prerequisites']=result

    # A constitutional settlement actually completes its three institutions.
    parents('state_compact',['autonomy_guarantees'],['professional_command'],['tax_registry'])
    # Front/monopoly develops through the delivered charter/screening, not a
    # bypass at congress. Its route retains distinct policy decisions thereafter.
    parents('baath_congress',['front_guarantees','party_screening'])
    for node in nodes:
        if node['group']=='baath' and node['id'] not in {P+x for x in ('regional_command','national_front','baath_monopoly','front_guarantees','party_screening')}:
            node['xy'][1]+=1
    parents('baath_future',['enterprise_accounts'],['baath_citizenship'],['party_social_bargain'])
    # Succession is a political decision, not a three-project completion stamp.
    parents('bakr_succession_plan',['bakr_guarantees','bakr_deputy_budget'])
    move('bakr_succession_plan',22,8)
    # Different political branches no longer end in the same optional OR stamp.
    finales={
      'saddam_legacy':[['saddam_local_procurement'],['saddam_bounded_deterrence','saddam_debt_service']],
      'icp_socialist_republic':[['icp_safety_inspection'],['icp_peasant_credit']],
      'aziz_party_renewal':[['aziz_workplace_delegates'],['aziz_safe_return']],
      'civic_mandate':[['civic_security_oversight']],
      'royal_settlement':[['royal_service']],
      'kdp_common_republic':[['kdp_local_policing']],
      'puk_federal_mandate':[['puk_payroll'],['puk_trade_routes']],
      'officer_settlement':[['officer_reintegration'],['officer_continuity']],
      'arab_republic_endures':[['arab_training_network']],
      'dawa_government_review':[['dawa_literacy'],['dawa_medical_network']],
      'sciri_iraqi_mandate':[['sciri_civil_review']],
      'iip_government_mandate':[['iip_public_service'],['iip_medical_welfare']],
      'war_peace_dividend':[['war_reintegration']],
    }
    for key,groups in finales.items():
        assert all(P+x in by for g in groups for x in g),(key,groups)
        parents(key,*groups)
    # Political milestones follow their own institutional subject; foreign
    # offers and civilian reconstruction are no longer stamped with one shape.
    move('arab_republic_endures',44,11)
    n('kdp_common_republic')['active_requires']=['Northern guarantees fulfilled']
    n('saddam_legacy')['modifiers']={'political_power_factor':.08,'bureaucracy_cost_multiplier_modifier':-.03,'tax_gain_multiplier_modifier':-.02}

    # Governing ICP cards now describe cabinet/party institutions. The historical
    # opposition struggle remains available separately before accession.
    for key,title in {
      'icp_front_strategy':'A Coalition Cabinet',
      'icp_independent_strategy':'The Governing Party',
      'icp_legal_cells':'Public Party Offices',
      'icp_underground':'Reunite the Cadres',
      'aziz_negotiated_road':'A Cabinet of Allies',
      'aziz_opposition_road':'The Congress Mandate',
      'aziz_united_opposition':'Parliamentary Allies',
      'aziz_safe_return':'Bring the Exiles Home',
      'kdp_common_republic':'A Common Republic',
      'foreign_debt_diplomacy':'Regional Debt Settlement',
    }.items():n(key)['title']=title
    parents('icp_membership',['icp_legal_cells','icp_underground'])
    for node in nodes:
        if node['group']=='communists' and node['xy'][1]>=4 and node['key'] not in ('icp_legal_cells','icp_underground'):
            node['xy'][1]+=1
    # KDP's budget is an implementation of the constitutional choice.
    parents('kdp_government_accounts',['kdp_autonomy_budget','kdp_federal_budget'])
    for node in nodes:
        if node['group']=='kurds' and node['xy'][1]>=17 and node['key'] not in ('kdp_autonomy_budget','kdp_federal_budget'):
            node['xy'][1]+=1

    # Exact approved oil transform: training plus twelve following cards down
    # one original row, before removing the merged delivery-only entries.
    parents('oil_technical_training',['oil_state_company','oil_concession_delivery'])
    for node in nodes:
        if node['group']=='oil' and (node['key']=='oil_technical_training' or old[node['id']]['xy'][1]>17):node['xy'][1]+=1
    # The two asset deliveries are consolidated into the chosen priority.
    parents('oil_revenue_ledger',['oil_revenue_state','oil_diversification'])
    parents('oil_sovereignty',['oil_field_maintenance'],['oil_baiji'],['oil_contract_review'])

    # Collapse the industry's dead rows after the factory pair is merged.
    for key,x,y in [
      ('industry_heavy',50,15),('industry_light',54,15),('industry_power_grid',52,16),
      ('industry_public_finance',50,17),('industry_credit_finance',54,17),
      ('industry_public_accounts',50,18),('industry_debt_accounts',54,18),
      ('industry_maintenance',52,19),('industry_power',50,20),
      ('industry_machine_tools',52,20),('industry_commercial_services',54,20),
      ('industry_grid_management',50,21),('industry_tax_service',54,21),
    ]:move(key,x,y)
    n('industry_commercial_services')['icon']='generic_office_construct'
    n('industry_grid_management')['icon']='national_grid'
    # Marketing disruption belongs to a new nationalisation, never a later
    # save-upgrade delivery for a nationalisation that happened years earlier.
    n('oil_nationalize')['audit_new_delivery_only']=['add_timed_idea = { idea = COLDWAR_IRQ_ipc_marketing_transition days = 90 }']
    # Different state tasks use their own art; the supplied portrait is retained.
    for key,icon in {'saddam_technocrats':'generic_university','saddam_staff_college':'army_reform',
      'saddam_regional_role':'diplomatic_treaty','saddam_iran_dossier':'intelligence_exchange',
      'saddam_bounded_deterrence':'army_reform'}.items():n(key)['icon']=icon

    # Neutral military assessment no longer assumes an Arabistan demand.
    parents('iran_tehran_assessment',['iran_frontier'])
    move('iran_tehran_assessment',98,16)
    parents('iran_operational_plan',['iran_southern_command'],['iran_tehran_assessment'])
    # The annexation claim remains an explicit requirement of the territorial
    # ultimatum/core route, rather than of every operational preparation.
    for key in ('iran_gulf_credit','iran_supplier_access'):
        for dec in n(key)['decisions']:
            if dec['id'] not in {d['id'] for d in n('iran_operational_plan')['decisions']}:
                n('iran_operational_plan')['decisions'].append(deepcopy(dec))
            for spec in data['decisions']:
                if spec['id']==dec['id']:spec['unlock']=P+'iran_operational_plan'

    # Retired focuses keep their IDs but have no playable branch or transaction.
    for fid,target in retired.items():
        node=by[fid];node['audit_retired']=True;node['audit_replaced_by']=target
        node['modifiers']={};node['building']=None;node['instant']=[];node['army_xp']=0
        node['budget_gdp_share']=0;node['decisions']=[];node['requires']=[]
        node['prerequisites']=[];node['mutually_exclusive']=[]
    # Re-anchor whole sections after removing their administrative root. Legacy
    # entries remain absolute; they never steal a visible branch's anchor.
    for group in data['groups']:
        active=[n for n in nodes if n['group']==group['id'] and not n.get('audit_retired')]
        anchor=group['anchor']
        if anchor in retired:anchor=min(active,key=lambda x:(x['xy'][1],x['xy'][0]))['id']
        group['anchor']=anchor;group['xy']=by[anchor]['xy'][:]
        for node in active:
            node['anchor']=None if node['id']==anchor else anchor
            origin=by[anchor]['xy'] if node['anchor'] else [0,0]
            node['offset']=[node['xy'][0]-origin[0],node['xy'][1]-origin[1]]
    for node in nodes:
        if node.get('audit_retired'):node['anchor']=None;node['offset']=node['xy'][:]

def load_design(include_overhaul=True):
    data=deepcopy(baseline())
    from audit_rewards import apply,RETIRED
    apply(data)
    retired=dict(RETIRED)
    retired.update({P+'iran_gulf_credit':P+'iran_operational_plan',P+'iran_supplier_access':P+'iran_operational_plan'})
    _structure(data,retired)
    from decisions_module import extra_focus_decisions
    extra_focus_decisions(data)
    # Decisions can have several genuine alternative providers after merging a
    # former review card. Completion of the retired card is no longer required.
    for decision in data['decisions']:
        if decision['unlock']=='START':continue
        providers=[n['id'] for n in data['nodes'] if not n.get('audit_retired') and any(d['id']==decision['id'] for d in n['decisions'])]
        if providers:
            decision['audit_providers']=providers
            decision['unlock']=providers[0]
    data['audit_revision']=REVISION;data['retired_focuses']=retired
    data['status']='IMPLEMENTATION AUTHORIZED: full audit approved by user on 2026-10-19'
    if include_overhaul:
        import reward_overhaul
        reward_overhaul.apply(data)
        data['audit_revision']=reward_overhaul.REVISION
    # IMPERIA CW — Cold War: keep original contracts as metadata, publish lean actions.
    if include_overhaul:
        from decision_streamlining import apply_design
        apply_design(data)
    return data
