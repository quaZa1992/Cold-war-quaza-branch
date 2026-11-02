# IMPERIA COLD WAR — SSR concept lifecycle and native API contracts.
"""Reviewable proposed rules. These are not installed scripted effects."""
import content as c

PARTY_TRIGGERS={0:'western_autocrats_are_in_power',1:'western_conservatism_are_in_power',
 2:'western_liberals_are_in_power',3:'western_social_democrats_are_in_power',
 4:'emerging_communist_state_are_in_power',12:'neutrality_neutral_muslim_brotherhood_are_in_power',
 14:'neutrality_neutral_conservatism_are_in_power',18:'neutrality_neutral_social_are_in_power',
 20:'nationalist_right_wing_populists_are_in_power',21:'nationalist_fascist_are_in_power'}

# Three repairs each. An initial penalty is reduced to 2/3, 1/3 and 0.
# Stage modifiers are rounded to five fractional digits; the final stage removes
# the spirit, so accumulated rounding cannot leave a permanent remainder.
REPAIR={
 'payment_register':('broken_supply',1),'supplier_contracts':('broken_supply',2),'industrial_conversion':('broken_supply',3),
 'revenue_service':('state_accounts',1),'registered_accounts':('state_accounts',2),
 'budget_protection':('state_accounts',3),'budget_consolidation':('state_accounts',3),
 'defence_authority':('command_gap',1),'maintenance_command':('command_gap',2),'defence_settlement':('command_gap',3),
}
PREP={
 'diversify_orders':('broken_supply',0.25),'regional_diversify':('broken_supply',0.25),
 'civil_registers':('state_accounts',0.25),'defence_records':('command_gap',0.25),
}
SPECIALISATION=dict(name='Unconverted Union Orders',modifiers=c.M(tax=-4,eff=-5))
CASES={
 'abrupt':dict(title='Abrupt separation',separation=1,prepared=False),
 'prepared':dict(title='Prepared separation',separation=1,prepared=True),
 'negotiated':dict(title='Prepared and negotiated separation',separation=0.6,prepared=True),
}
SEVERITY={
 'UKR':(1.1,1,1),'BLR':(1.1,1,1),'MLV':(1,1.1,1),
 'EST':(0.9,0.9,1),'LAT':(1,0.9,1),'LIT':(1,0.9,1),
 'GEO':(1.05,1.1,1),'ARM':(1.1,1.05,1),'AZE':(0.95,1,1),
 'KAZ':(1,1,1),'UZB':(1,1.2,1),'TRK':(0.95,1.15,1),
 'KYR':(1,1.25,1),'TAJ':(1,1.3,1),
}

CONTRACT=dict(
 status='Proposed implementation contract, not an existing SSR API',
 ssr='IMP_is_1970_scenario and COLDWAR_SOV_is_union_republic and a recorded scenario SSR identity or a subsequently accepted SSR admission. A whitelisted puppet by itself is insufficient.',
 sovereign='Existing state exists, is not a subject of any country, and has a recorded actual SSR independence or Union dissolution transition. A successful unilateral secession can create that record as well as a negotiated release; continuing Soviet approval is not a requirement for independent domestic content. Occupation or a different overlord does not count as independence.',
 transition='Apply once on that real status transition. Do not release countries, change government, create borders or transfer units from focus completion. Re-entry to the USSR suspends the aftermath; a second exit resumes the stored recovery state without repeated rewards.',
 programme='Sector rewards modify one named dynamic programme for that sector. One primary Union specialisation may be selected from nine mutually exclusive roles. All shared SSR content requires recognised SSR status without a communist-party or Soviet-outlook gate. Ordinary Union-dependent programmes suspend on independence. The chosen specialisation instead becomes a national legacy: 20 percent of beneficial modifiers and scoped equipment bonuses, 75 percent of adverse modifiers, and half the weekly GDP maintenance share. Construction, research bonuses and earned experience remain national assets. Each independent party has one stored programme requiring actual sovereignty and the exact current slot; departure suspends that programme and return never repeats one-time rewards.',
 durable='Construction, earned experience, limited research bonuses and completed civil registers are national gains. Removal or replacement of an inherited problem is a persistent reform receipt, separate from a party programme. Existing infrastructure and state institutions survive a government change.',
 starting='The Union Technical Network ends with genuine SSR status or suspended Union links. Plan shortages and patronage persist unless actually reformed. The original or reformed Social Guarantees persist after independence until a separately designed welfare reform changes them. Regional constraints persist in original or managed form.',
 recovery='Each of supply, state accounts and defence administration has three distinct repairs. Count unique completed repair receipts, independently of completion order. One leaves two thirds of the initial penalty, two leave one third, three remove it. State accounts can be repaired across different chapters in either order; a later focus never restores an earlier penalty. Both exclusive budget courses provide the same third distinct receipt. Actual completed preparations reduce only their specified initial liability. Negotiated separation reduces the remaining liability to 60 percent only if a real accepted settlement keeps deliveries, payments and administration operating. Continued war or interrupted terms invalidate that mitigation until restored; elapsed time alone repairs nothing.',
 exposure='Union Supply Contracts gives the stated SSR reward and adds Unconverted Union Orders on independence. Export Conversion or Domestic Suppliers removes that separate penalty. Diversify Orders is mutually exclusive and reduces the starting supply liability instead. These ordinary contracts are distinct from the nine mutually exclusive primary specialisations.',
 bilateral='Each concrete foreign-policy focus dispatches one offer to one eligible named RP recipient, selected through its completion event. The recipient receives Accept and Refuse decisions with the complete two-country effects. Setup costs occur only on acceptance, once. Refusal charges neither country and opens a 180-day renegotiation decision for the same terms. Each originating republic has one active or pending partner per contract type. A shared recipient programme and its weekly operating budget apply once per contract type while any valid pair remains active; accepting additional republics does not multiply its national modifiers. The actual marginal preview must reflect any already active recipient programme. Acceptance rechecks status, geography, prerequisites and restrictions.',
 standing='Signatures have no expiry. Both states must exist, remain at peace with each other, impose no native embargo and none of the four mirrored Imperia diplomatic, financial, economic or military sanctions in either direction. Failure suspends that pair\'s entitlements, spirits and dedicated weekly expenses. A shared recipient programme remains only if another valid signed pair independently supports it, and never multiplies its national modifiers. Restoration resumes the actual active programmes without fees or one-time rewards. Either signatory may terminate. Recognition of one actual Soviet successor is recorded by the dissolution settlement, not inferred from an arbitrary tag.',
 geography='Border commissions require an actual land neighbour. Water commissions require a shared real basin. Energy transit requires an actual supplier-route relationship. Technical and training treaties require the partner capability recorded in the agreement. These focuses remain inspectable when ineligible. A focus with no live eligible counterpart stays unavailable and cannot block unrelated regional diplomacy.',
 no_duplicate='No duplicate subject subsidy, ministry system, COMECON treaty membership, automatic army, free uranium deposit or automatic conflict. SSRs retain existing COMECON access. The 1985 autonomy penalties are not assumed to exist in the 1970 start.',
    equipment='Equipment production costs use native idea equipment_bonus entries with build_cost_ic and instant = yes. The six weapon-related specialisations also retain their original military output, efficiency-cap or dockyard modifiers where present. Explicit equipment targets cover the intended class; no unstated parent-to-duplicate inheritance is assumed. Completed components accumulate once in the active programme and are replaced by their separately scaled legacy on independence. Distinct archetypes remain distinct named rows, never repeated under the same target. Existing MD native names are used in every preview. Designer and non-designer application and existing-variant refresh require an in-game check.',
)

def initial(tag,case='abrupt'):
    out=[];mode=CASES[case]
    for i,base in enumerate(c.TRANSITION):
        prep=sum(v[1] for v in PREP.values() if v[0]==base['id']) if mode['prepared'] else 0
        factor=SEVERITY[tag][i]*(1-prep)*mode['separation']
        out.append({**base,'modifiers':{k:round(v*factor,5) for k,v in base['modifiers'].items()}})
    return out

def prepare_node(n,tag):
    hidden=['IMP_is_1970_scenario']
    visible=[]
    if n['phase']=='ssr':hidden.append(CONTRACT['ssr']);visible.append('Recognised Soviet Union republic status')
    elif n['phase'] in {'independent','party'}:hidden.append(CONTRACT['sovereign']);visible.append('An independent republic')
    if n.get('gate')=='union_member':visible.append('Current Union Plan membership');hidden.append('COLDWAR_UNI_is_member')
    elif (n.get('gate') or '').startswith('slot'):
        slot=int(n['gate'][4:]);hidden.append(PARTY_TRIGGERS[slot])
        name=next(p['name'] for p in c.party_profile(tag)['parties'] if p['slot']==slot)
        visible.append(name+' is in power')
    if (n.get('action') or '').startswith('offer:'):
        visible += ['Eligible named RP partner','Peace and no bilateral embargo or sanctions']
    if n.get('building'):visible += ['Eligible owned and controlled core state with native construction capacity']
    if n.get('geography')=='naval_coast':visible += ['An owned and controlled coast with a legal naval project site']
    if n.get('needs_existing_resources'):visible += ['Existing controlled fossil fuel or non-uranium mineral production']
    if n.get('party_transfer'):
        t=n['party_transfer'];t['from_name']=next(p['name'] for p in c.party_profile(tag)['parties'] if p['slot']==t['from_slot'])
        t['to_name']=next(p['name'] for p in c.party_profile(tag)['parties'] if p['slot']==t['to_slot'])
    n['requirements']=visible;n['runtime_contract']=hidden
    if n['key'] in REPAIR:n['repair']=dict(zip(('spirit','stage'),REPAIR[n['key']]))
    if n['key'] in PREP:n['preparation']=dict(zip(('spirit','reduction'),PREP[n['key']]))
    if n['key']=='deepen_specialisation':n['exposure']=SPECIALISATION
    if n['key'] in {'export_conversion','domestic_chains'}:n['remove_exposure']=SPECIALISATION['name']
    inherited={s['name']:s['modifiers'] for s in c.STARTING}
    inherited['Revised Plan Targets']=c.M(cap=-5,eff=-5)
    if n['key']=='industrial_conversion':
        n['conditional_removals']=[dict(name=name,delta={k:-v for k,v in inherited[name].items()}) for name in ['Plan Targets and Shortages','Revised Plan Targets']]
    if n['key'] in {'court_review','executive_service'}:
        name='Republican Patronage Networks'
        n['conditional_removals']=[dict(name=name,delta={k:-v for k,v in inherited[name].items()})]
    if n['key']=='transition_settlement':
        regional=c.party_profile(tag)['regional']
        n['regional_aftercare']=dict(old=regional['name'],new='Managed '+regional['name'],
            modifiers={k:round(v/2,5) for k,v in regional['modifiers'].items()},
            delta={k:round(-v/2,5) for k,v in regional['modifiers'].items()})

def repair_delta(n,tag,case='abrupt'):
    if not n.get('repair'):return None
    t=n['repair'];s=next(v for v in initial(tag,case) if v['id']==t['spirit']);stage=t['stage']
    before={k:round(v*(4-stage)/3,5) for k,v in s['modifiers'].items()}
    after={k:round(v*(3-stage)/3,5) for k,v in s['modifiers'].items()}
    return dict(name=s['name'],stage=stage,before=before,after=after,
                delta={k:round(after[k]-before[k],5) for k in after})
