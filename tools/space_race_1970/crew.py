# IMPERIA COLD WAR — Consensual international astronaut delegations.
"""Country seats, conserved awards and signed, funded flight assignments.

Each guest occupies one seat. Two guest countries maximum; the commander and
all other seats remain national. Country variables retain native country scopes.
"""
from research_rewards import award
# IMPERIA COLD WAR — Conserve the same pool across crew and work packages.
import cooperation
from decimal import Decimal, ROUND_DOWN

SHARE = .20
CONTRIBUTION = .15
TRAINING_WEEKS = 26
TRAINING_WEEKLY = .002


def eligible(p):
    return bool(p['crewSize']) and not p.get('commissioningOnly') and p['id']!='interkosmos-cosmonaut'


def slots(p):
    return range(1, min(2, p['crewSize']-1)+1) if eligible(p) else []


def field(n, s, suffix):
    return f'cw_sr_p{n}_guest{s}_{suffix}'


def contribution(p):
    """Whole millions ensure contribution and net-treasury guards agree."""
    return float((Decimal(str(p['missionCostB']))*Decimal('.15')).quantize(Decimal('.001'),rounding=ROUND_DOWN))


def funds(c,n,p):
    cv=c['cv'];terms=[]
    for mask in range(2**len(slots(p))):
        count=mask.bit_count();condition=''
        for i,s in enumerate(slots(p)):
            condition+=cv(field(n,s,'country'),'>' if mask&(1<<i) else '=',0)+' '
        terms.append('AND = { '+condition+cv('treasury','>=',c['num'](p['missionCostB']-contribution(p)*count))+' }')
    return 'OR = { '+' '.join(terms)+' }'


def gate(c, n, p):
    cv = c['cv']
    result = ''
    for s in slots(p):
        f = lambda x: field(n,s,x)
        # PREV is the host in the native country-variable scope.
        result += ('OR = { '+cv(f('country'),'=',0)+' AND = { '+cv(f('status'),'=',2)+
                   f' var:{f("country")} = {{ exists = yes is_ai = no NOT = {{ has_war_with = PREV }} '+
                   cv('cw_sr_crew_host','=','PREV.id')+' '+cv('cw_sr_crew_programme','=',n)+' '+
                   cv('cw_sr_crew_slot','=',s)+' '+cv('cw_sr_crew_serial','=',f'PREV.{f("serial")}')+' '+cv('cw_sr_crew_weeks','>=',TRAINING_WEEKS)+' '+
                   cv('treasury','>=',c['num'](contribution(p)))+' } } }\n')
    return result


# IMPERIA COLD WAR — Exact live preflight crew assignment on both governments.
def preflight(c,n,seat):
    cv=c['cv'];f=lambda x:field(n,seat,x)
    states='OR = { '+' '.join(cv(c['var'](n,'state'),'=',value) for value in [1,2,3,5,6])+' }'
    host='exists = yes is_ai = no NOT = { has_war_with = PREV } '+states+' '+cv(f('country'),'=','PREV.id')+' '+cv(f('status'),'=','PREV.cw_sr_crew_status')+' '+cv(f('serial'),'=','PREV.cw_sr_crew_serial')
    return cv('cw_sr_crew_programme','=',n)+' '+cv('cw_sr_crew_slot','=',seat)+' var:cw_sr_crew_host = { '+host+' }'


def snapshot(c,n,p):
    sv,block_if,cv,av=(c[k] for k in ['sv','block_if','cv','av'])
    body=sv(f'cw_sr_p{n}_crew_recorded',1)
    for s in slots(p):
        f=lambda x:field(n,s,x)
        payment=c['num'](contribution(p))
        body+=sv(f('flight'),f('country'))
        body+=block_if(cv(f('country'),'>',0),sv(f('status'),3)+f'var:{f("country")} = {{\n'+sv('cw_sr_crew_status',3)+c['charge'](payment)+'}\n'+c['charge']('-'+payment))
    return body


# IMPERIA COLD WAR — International operational cooperation.
def distribute(c,n,p,prestige,science=0,pp=0,bonus=0,name='',kind='first'):
    """Split the original pool. Never issue copies of the host's full award."""
    sv,av,cv,block_if=(c[k] for k in ['sv','av','cv','block_if'])
    body=sv('cw_sr_crew_pool',prestige,True)+sv('cw_sr_crew_host_share',1,True)
    for s in slots(p):
        body+=block_if(cv(f'cw_sr_p{n}_crew_recorded','=',1)+' '+cv(field(n,s,'flight'),'>',0),av('cw_sr_crew_host_share',-SHARE,True))
    if cooperation.eligible(p):body+=block_if(cv(cooperation.field(n,'recorded'),'=',1)+' '+cv(cooperation.field(n,'flight'),'>',0),av('cw_sr_crew_host_share',-.10,True))
    def numeric(mult):
        b=sv('cw_sr_crew_gain','PREV.cw_sr_crew_pool' if mult==SHARE else 'cw_sr_crew_pool',True)
        b+=f'multiply_temp_variable = {{ cw_sr_crew_gain = {mult if mult==SHARE else "cw_sr_crew_host_share"} }}\n'+av('cw_sr_prestige','cw_sr_crew_gain')
        if science:b+=av('cw_sr_science',c['num'](science*mult)) if mult==SHARE else sv('cw_sr_crew_gain',science,True)+'multiply_temp_variable = { cw_sr_crew_gain = cw_sr_crew_host_share }\n'+av('cw_sr_science','cw_sr_crew_gain')
        if pp:b+=f'add_political_power = {c["num"](pp*SHARE)}\n' if mult==SHARE else sv('cw_sr_crew_gain',pp,True)+'multiply_temp_variable = { cw_sr_crew_gain = cw_sr_crew_host_share }\nadd_political_power = cw_sr_crew_gain\n'
        return b
    body+=numeric(1)
    if bonus:
        shares=sorted({round(1-SHARE*count-.10*op,2) for count in range(len(slots(p))+1) for op in ([0,1] if cooperation.eligible(p) else [0])})
        for share in shares:
            body+=block_if(cv('cw_sr_crew_host_share','=',c['num'](share)),award(c['ROOT'],name,bonus*share))
    for s in slots(p):
        f=lambda x:field(n,s,x)
        guest=numeric(SHARE)
        if bonus:guest+=award(c['ROOT'],name,bonus*SHARE)
        # Guests formerly controlled by players retain signed flight entitlements;
        # awards wait in escrow until their country is human-controlled again.
        guest=block_if('is_ai = no',guest,sv('cw_sr_crew_escrow_prestige','PREV.cw_sr_crew_pool',True)+f'multiply_temp_variable = {{ cw_sr_crew_escrow_prestige = {SHARE} }}\n'+av('cw_sr_crew_pending_prestige','cw_sr_crew_escrow_prestige')+av('cw_sr_crew_pending_science',c['num'](science*SHARE))+av('cw_sr_crew_pending_pp',c['num'](pp*SHARE))+(f'set_country_flag = cw_sr_crew_pending_{name}\n' if bonus else ''))
        if kind in ['first','partial']:
            receipt=f'cw_sr_guest_p{n}_'+kind
            condition=f'NOT = {{ has_country_flag = {receipt} }}'
            if kind=='partial':condition+=f' NOT = {{ has_country_flag = cw_sr_guest_p{n}_first }}'
            guest=block_if(condition,guest+f'set_country_flag = {receipt}\n')
        body+=block_if(cv(f'cw_sr_p{n}_crew_recorded','=',1)+' '+cv(f('flight'),'>',0),f'var:{f("flight")} = {{\n'+guest+'}\n')
    if cooperation.eligible(p):body+=cooperation.distribute(c,n,p,science,pp,bonus,name,kind)
    return body


def finish(c,n,p,kind):
    sv,av,cv,block_if=(c[k] for k in ['sv','av','cv','block_if'])
    body=''
    for s in slots(p):
        f=lambda x:field(n,s,x)
        guest=f'set_country_flag = cw_sr_guest_p{n}_trained\n'+sv(f'cw_sr_guest_p{n}_last_fatalities',0)+f'country_event = {{ id = cw_sr_crew.{n*10+{ "success":2,"partial":3,"failure":4,"catastrophic":5,"abort":6}[kind]} }}\n'
        if kind=='catastrophic':
            deaths=f'clr_country_flag = cw_sr_guest_p{n}_trained\n'+av('cw_sr_fatalities',1)+av(f'cw_sr_guest_p{n}_fatalities',1)+sv(f'cw_sr_guest_p{n}_last_fatalities',1)+'add_manpower = -1\nadd_political_power = -4\n'
            guest+=block_if(cv(f'PREV.cw_sr_p{n}_phase','=',1) if p.get('crewAtLaunch') is False else 'always = yes',deaths)
        if kind=='success':guest+=f'set_country_flag = cw_sr_guest_p{n}_completed\n'
        # IMPERIA COLD WAR — A restored old operator cannot erase a newer delegation.
        active_binding=cv('cw_sr_crew_host','=','PREV.id')+' '+cv('cw_sr_crew_programme','=',n)+' '+cv('cw_sr_crew_slot','=',s)+' '+cv('cw_sr_crew_serial','=',f'PREV.{f("serial")}')+' '+cv('cw_sr_crew_status','=',3)
        guest+=block_if(active_binding,sv('cw_sr_crew_status',0)+sv('cw_sr_crew_host',0)+sv('cw_sr_crew_programme',0)+sv('cw_sr_crew_slot',0)+sv('cw_sr_crew_weeks',0))
        body+=block_if(cv(f('flight'),'>',0),f'var:{f("flight")} = {{\n'+guest+'}\n')
        # Keep the roster for reports. A surviving qualified delegation retains
        # its basic course; another assignment requires a six-week refresher.
        body+=sv(f('country'),0)+sv(f('status'),0)
    return block_if(cv(f'cw_sr_p{n}_crew_recorded','=',1),body+sv(f'cw_sr_p{n}_crew_recorded',0))


def deaths(c,n,p):
    sv,av,cv,block_if=(c[k] for k in ['sv','av','cv','block_if'])
    body=sv('cw_sr_crew_national',p.get('nationalCrewSize',p['crewSize']),True)
    for s in slots(p):body+=block_if(cv(f'cw_sr_p{n}_crew_recorded','=',1)+' '+cv(field(n,s,'flight'),'>',0),av('cw_sr_crew_national',-1,True))
    # Existing Interkosmos guest programme includes a contracted foreign pilot.
    body+=c['clamp']('cw_sr_crew_national',0,p['crewSize'],True)
    body+=av('cw_sr_fatalities','cw_sr_crew_national')+av(f'cw_sr_p{n}_fatalities',p['crewSize'])
    body+='multiply_temp_variable = { cw_sr_crew_national = -1 }\nadd_manpower = cw_sr_crew_national\nmultiply_temp_variable = { cw_sr_crew_national = 4 }\nadd_political_power = cw_sr_crew_national\n'
    return body


# IMPERIA COLD WAR — International operational cooperation.
def build(c):
    sv,av,cv,block_if,effect,var,loc=(c[k] for k in ['sv','av','cv','block_if','effect','var','loc'])
    programmes=[(n,p) for n,p in enumerate(c['PROGRAMMES'],1) if eligible(p)]
    fx='';triggers='';defs='';events='add_namespace = cw_sr_crew\n';refresh=sv('cw_sr_crew_available',0)
    def define(name,entries,fallback):
        return 'defined_text = { name = '+name+'\n'+''.join('text = { trigger = { '+cond+' } localization_key = '+key+' }\n' for cond,key in entries)+'text = { localization_key = '+fallback+' } }\n'
    # IMPERIA COLD WAR — Deterministic human partner discovery and empty states.
    # PREV is the viewing government throughout the native every_country scope.
    # No random selection, initialization, offers or rewards occur in this scan.
    scan=sv('cw_sr_partner_count',0)+sv('cw_sr_crew_found',0,True)+sv('cw_sr_crew_first',0,True)+sv('cw_sr_crew_next',0,True)
    scan+='every_country = { limit = { exists = yes is_ai = no NOT = { tag = PREV } NOT = { has_war_with = PREV } }\n'
    scan+=av('PREV.cw_sr_partner_count',1)
    scan+=block_if(cv('PREV.cw_sr_crew_first','=',0),sv('PREV.cw_sr_crew_first','THIS.id',True))
    scan+=block_if(cv('PREV.cw_sr_crew_found','=',1)+' '+cv('PREV.cw_sr_crew_next','=',0),sv('PREV.cw_sr_crew_next','THIS.id',True))
    scan+=block_if(cv('THIS.id','=','PREV.cw_sr_crew_candidate'),sv('PREV.cw_sr_crew_found',1,True))+'}\n'
    scan+=block_if(cv('cw_sr_crew_next','=',0),sv('cw_sr_crew_next','cw_sr_crew_first',True))
    scan+=sv('cw_sr_partner_checked_day','global.num_days')+'set_country_flag = cw_sr_partner_catalogue_cached\n'
    fx+=effect('cw_sr_partner_scan',block_if(c['guard'](),scan))
    fx+=effect('cw_sr_crew_candidate_next',block_if(c['guard'](),'cw_sr_partner_scan = yes\n'+sv('cw_sr_crew_candidate','cw_sr_crew_next')))
    due='OR = { NOT = { has_country_flag = cw_sr_partner_catalogue_cached } '+cv('cw_sr_partner_checked_day','!=','global.num_days')+' }'
    visible='has_country_flag = cw_sr_open OR = { '+cv('cw_sr_tab','=',9)+' '+cv('cw_sr_tab','=',10)+' }'
    fx+=effect('cw_sr_partner_refresh',block_if(c['guard']()+' '+visible+' '+due,'cw_sr_partner_scan = yes\n'+block_if(cv('cw_sr_crew_found','=',0),sv('cw_sr_crew_candidate','cw_sr_crew_first'))))
    # IMPERIA COLD WAR — Stop orphaned or politically invalid training before charging.
    preflight_guard='OR = { '+' '.join('AND = { '+preflight(c,n,seat)+' }' for n,p in programmes for seat in slots(p))+' }'
    triggers+=effect('cw_sr_crew_preflight_binding',preflight_guard)
    weekly=block_if(c['guard']()+' '+cv('cw_sr_crew_status','=',2)+' '+cv('cw_sr_crew_weeks','<',TRAINING_WEEKS)+' '+cv('treasury','>=',TRAINING_WEEKLY)+' cw_sr_crew_preflight_binding = yes',c['charge'](TRAINING_WEEKLY)+av('cw_sr_crew_weeks',1))
    fx+=effect('cw_sr_crew_training_weekly',weekly)
    cleanup=''
    for key in ['host','programme','slot','status','weeks','expires']:cleanup+=sv('cw_sr_crew_'+key,0)
    fx+=effect('cw_sr_crew_clear_assignment',cleanup)
    pending=av('cw_sr_prestige','cw_sr_crew_pending_prestige')+av('cw_sr_science','cw_sr_crew_pending_science')+'add_political_power = cw_sr_crew_pending_pp\n'+''.join(sv('cw_sr_crew_pending_'+k,0) for k in ['prestige','science','pp'])
    for n,p in programmes:
        if p['rewardEffects']['researchPoints']>=4:
            key=f'cw_sr_p{n}_name';pending+=block_if(f'has_country_flag = cw_sr_crew_pending_{key}',award(c['ROOT'],key,.02)+f'clr_country_flag = cw_sr_crew_pending_{key}\nset_country_flag = cw_sr_guest_p{n}_first\n')
    for m,ms in enumerate(c['DATA']['milestones'],1):
        key=f'cw_sr_milestone_{m}';pending+=block_if(f'has_country_flag = cw_sr_crew_pending_{key}',award(c['ROOT'],key,.04)+f'clr_country_flag = cw_sr_crew_pending_{key}\n')
    daily=block_if(c['guard'](),pending)+block_if(cv('cw_sr_crew_status','=',1),av('cw_sr_crew_expires',-1)+block_if(cv('cw_sr_crew_expires','<',1),'cw_sr_crew_clear_assignment = yes\n'))
    # IMPERIA COLD WAR — Recover preflight seats after host loss, war or a stale serial.
    invalid='OR = { '+cv('cw_sr_crew_status','=',1)+' '+cv('cw_sr_crew_status','=',2)+' } NOT = { cw_sr_crew_preflight_binding = yes }'
    daily+=block_if(c['guard']()+' '+invalid,'cw_sr_crew_withdraw = yes\n')
    # IMPERIA COLD WAR — Annexation releases administrative reservations without inventing a flight outcome.
    daily+=block_if(c['guard']()+' '+cv('cw_sr_crew_status','=',3)+' NOT = { var:cw_sr_crew_host = { exists = yes } }','cw_sr_crew_clear_assignment = yes\n')
    invite_action='';remove_action='';withdraw=''
    for n,p in programmes:
        refresh+=block_if(cv('cw_sr_selected','=',n),sv('cw_sr_crew_available',1)+sv('cw_sr_crew_total',p['crewSize'])+sv('cw_sr_crew_host_percent',100)+sv('cw_sr_crew_host_bonus',10 if p['rewardEffects']['researchPoints']>=4 else 0)+sv('cw_sr_crew_host_prestige',p['prestige'])+sv('cw_sr_crew_host_science',p['rewardEffects']['researchPoints'])+sv('cw_sr_crew_host_pp',p['rewardEffects']['politicalCapital'])+sv('cw_sr_crew_full_cost',p['missionCostB'])+sv('cw_sr_crew_host_cost',p['missionCostB'])+sv('cw_sr_crew_invited',0)+sv('cw_sr_crew_awarded',0)+block_if(f'has_country_flag = cw_sr_p{n}_awarded',sv('cw_sr_crew_awarded',1)))
        triggers+=effect(f'cw_sr_p{n}_crew_ready',gate(c,n,p))
        for s in slots(p):
            f=lambda x:field(n,s,x)
            mutable=c['guard']()+' NOT = { '+cv(var(n,'state'),'=',4)+' }'
            selected=cv('cw_sr_selected','=',n)+' '+cv('cw_sr_crew_edit_slot','=',s)
            other=field(n,3-s,'country')
            valid=(cv('cw_sr_crew_candidate','>',0)+' '+cv('cw_sr_crew_candidate','!=','THIS.id')+' '+cv('cw_sr_crew_candidate','!=',other)+' '+cv('cw_sr_crew_candidate','!=',cooperation.field(n,'country'))+
                   ' var:cw_sr_crew_candidate = { exists = yes is_ai = no has_country_flag = cw_sr_initialized NOT = { has_war_with = PREV } NOT = { has_country_flag = cw_sr_crew_invitation_open } '+cv('cw_sr_crew_status','=',0)+' }')
            condition=mutable+f' date > {p["minYear"]-1}.12.31 '+ 'OR = { '+' '.join(cv(var(n,'state'),'=',state) for state in [1,2,3,5,6])+' } '+cv(f('country'),'=',0)+' '+valid
            triggers+=effect(f'cw_sr_p{n}_crew_invite{s}_allowed',condition)
            invite=sv(f('country'),'cw_sr_crew_candidate')+sv(f('status'),1)+av(f('serial'),1)
            invite+=f'var:{f("country")} = {{\nset_country_flag = cw_sr_crew_invitation_open\n'+sv('cw_sr_crew_host','PREV.id')+sv('cw_sr_crew_offer_operator','PREV.id')+sv('cw_sr_crew_offer_contribution',c['num'](contribution(p)))+sv('cw_sr_crew_training_weekly_m',2)+sv('cw_sr_crew_programme',n)+sv('cw_sr_crew_slot',s)+sv('cw_sr_crew_status',1)+sv('cw_sr_crew_weeks',0)+block_if(f'has_country_flag = cw_sr_guest_p{n}_trained',sv('cw_sr_crew_weeks',20))+sv('cw_sr_crew_expires',90)+sv('cw_sr_crew_serial',f'PREV.{f("serial")}')+f'country_event = {{ id = cw_sr_crew.{n*10+1} }}\n}}\n'
            fx+=effect(f'cw_sr_p{n}_crew_invite{s}',block_if(f'cw_sr_p{n}_crew_invite{s}_allowed = yes',invite))
            invite_action+=block_if(selected,f'cw_sr_p{n}_crew_invite{s} = yes\n')
            binding=cv('cw_sr_crew_host','=','PREV.id')+' '+cv('cw_sr_crew_programme','=',n)+' '+cv('cw_sr_crew_slot','=',s)+' '+cv('cw_sr_crew_serial','=',f'PREV.{f("serial")}')
            retain=block_if(cv('cw_sr_crew_weeks','>=',26),f'set_country_flag = cw_sr_guest_p{n}_trained\n')
            remove=block_if(cv(f('country'),'>',0),f'var:{f("country")} = {{\n'+block_if(binding,retain+'cw_sr_crew_clear_assignment = yes\n')+'}\n')+sv(f('country'),0)+sv(f('status'),0)
            fx+=effect(f'cw_sr_p{n}_crew_remove{s}',block_if(mutable,remove))
            remove_action+=block_if(selected,f'cw_sr_p{n}_crew_remove{s} = yes\n')
            # Expired/refused/disbanded assignments cannot reserve a seat forever.
            consistent=f'var:{f("country")} = {{ exists = yes '+binding+' '+cv('cw_sr_crew_status','>',0)+' }'
            daily+=block_if(cv(var(n,'state'),'!=',4)+' '+cv(f('country'),'>',0)+' NOT = { '+consistent+' }',sv(f('country'),0)+sv(f('status'),0))
            flight=cv(var(n,'state'),'=',4)
            chosen=field(n,s,'flight')
            copy=sv(f'cw_sr_crew_view_guest{s}',f('country'))+block_if(flight,sv(f'cw_sr_crew_view_guest{s}',chosen))
            copy+=sv(f'cw_sr_crew_view_status{s}',f('status'))+sv(f'cw_sr_crew_view_weeks{s}',0)+block_if(cv(f('country'),'>',0),f'var:{f("country")} = {{\n'+sv(f'PREV.cw_sr_crew_view_weeks{s}','cw_sr_crew_weeks')+'}\n')
            copy+=block_if(cv(f'cw_sr_crew_view_guest{s}','>',0),av('cw_sr_crew_host_percent',-20)+av('cw_sr_crew_invited',1)+av('cw_sr_crew_host_cost',c['num'](-contribution(p))))
            refresh+=block_if(cv('cw_sr_selected','=',n),copy)
            withdraw+=block_if(cv('cw_sr_crew_programme','=',n)+' '+cv('cw_sr_crew_slot','=',s),retain+f'var:cw_sr_crew_host = {{\n'+block_if(cv(var(n,'state'),'!=',4)+' '+cv(f('country'),'=','PREV.id')+' '+cv(f('serial'),'=','PREV.cw_sr_crew_serial'),sv(f('country'),0)+sv(f('status'),0))+'}\ncw_sr_crew_clear_assignment = yes\n')
        # Invitation validity includes the exact host, seat and offer serial.
        offer=cv('cw_sr_crew_status','=',1)+' '+cv('cw_sr_crew_programme','=',n)+' '+cv('cw_sr_crew_expires','>',0)
        host_valid=[];accepted=''
        for s in slots(p):
            f=lambda x:field(n,s,x)
            bind=cv('cw_sr_crew_slot','=',s)+f' var:cw_sr_crew_host = {{ exists = yes is_ai = no NOT = {{ has_war_with = PREV }} '+cv(var(n,'state'),'!=',4)+' '+cv(f('country'),'=','PREV.id')+' '+cv(f('status'),'=',1)+' '+cv(f('serial'),'=','PREV.cw_sr_crew_serial')+' }'
            host_valid.append('AND = { '+bind+' }')
            accepted+=block_if(cv('cw_sr_crew_slot','=',s),f'var:cw_sr_crew_host = {{ '+sv(f('status'),2)+' }\n')
        accept=offer+' OR = { '+' '.join(host_valid)+' }'
        fx+=effect(f'cw_sr_crew_accept_{n}',block_if(c['guard']()+' '+accept,'clr_country_flag = cw_sr_crew_invitation_open\n'+sv('cw_sr_crew_status',2)+accepted))
        # An AI takeover can only dismiss an outstanding offer; it cannot accept
        # a mission. Administrative cleanup must not strand its invitation slot.
        fx+=effect(f'cw_sr_crew_decline_{n}',block_if('IMP_is_1970_scenario = yes','clr_country_flag = cw_sr_crew_invitation_open\n'+block_if(offer,block_if('is_ai = no','cw_sr_crew_withdraw = yes\n','cw_sr_crew_clear_assignment = yes\n'))))
        title=loc(f'cw_sr_crew.{n*10+1}.t','[ROOT.GetName]: Joint Spaceflight Invitation')
        desc=loc(f'cw_sr_crew.{n*10+1}.d',f'[?cw_sr_crew_offer_operator.GetName] invites [ROOT.GetName] to supply one research astronaut for {p["name"]}. The commander remains with the mission operator.\n\nAccepted programme and world-first awards are shared. Previously claimed awards remain unavailable; repeat flights carry limited prestige. The delegation requires funded joint training and a departure contribution.\n\nThe offer expires after 90 days. Either government may withdraw before departure. Training payments remain committed; previously qualified delegations need refresher training.')
        events+=f'country_event = {{ id = cw_sr_crew.{n*10+1} title = {title} desc = {desc} picture = GFX_cw_sr_report_mission-control is_triggered_only = yes\noption = {{ name = cw_sr_crew_accept trigger = {{ is_ai = no {accept} }} cw_sr_crew_accept_{n} = yes custom_effect_tooltip = cw_sr_crew_agreement_terms }}\noption = {{ name = cw_sr_crew_decline cw_sr_crew_decline_{n} = yes }}\n}}\n'
        for stage,title,phrase in [(2,'Joint Crew Returns','has completed the flight campaign with'),(3,'Joint Flight: Limited Results','has recovered limited results with'),(4,'Joint Mission Fails','has failed to complete the mission with'),(5,'Joint Crew Accident','has suffered a catastrophic accident with'),(6,'Joint Launch Aborted','has safely aborted departure with')]:
            t=loc(f'cw_sr_crew.{n*10+stage}.t',f'[ROOT.GetName]: {title}')
            d=loc(f'cw_sr_crew.{n*10+stage}.d',f'[FROM.GetName] {phrase} a research astronaut delegation from [ROOT.GetName] under {p["name"]}. '+('The agreed national share has been credited for accepted results.' if stage in [2,3] else 'The joint flight authority has released its report.'))
            if stage==5:loc(f'cw_sr_crew.{n*10+stage}.d',c['LOC'][d]+f'\n\nCrew fatalities reported for [ROOT.GetName]: [?cw_sr_guest_p{n}_last_fatalities|0].')
            events+=f'country_event = {{ id = cw_sr_crew.{n*10+stage} title = {t} desc = {d} picture = GFX_cw_sr_report_mission-control is_triggered_only = yes option = {{ name = cw_sr_acknowledge }} }}\n'
    fx+=effect('cw_sr_crew_daily',daily)
    fx+=effect('cw_sr_crew_invite',invite_action)+effect('cw_sr_crew_remove',remove_action)
    fx+=effect('cw_sr_crew_withdraw',block_if(c['guard']()+' OR = { '+cv('cw_sr_crew_status','=',1)+' '+cv('cw_sr_crew_status','=',2)+' }',withdraw))
    # Reset every selected view before copying; small crews never inherit slot 2.
    reset=sv('cw_sr_crew_host_percent',100)+''.join(sv(f'cw_sr_crew_view_{field}{s}',0) for s in [1,2] for field in ['guest','status','weeks'])
    # IMPERIA COLD WAR — Show the unclaimed prestige pool after partial results.
    refresh+=sv('cw_sr_crew_host_prestige','cw_sr_view_first_prestige')
    refresh+=sv('cw_sr_crew_host_factor','cw_sr_crew_host_percent')+'divide_variable = { cw_sr_crew_host_factor = 100 }\n'
    for key in ['prestige','science','pp','bonus']:refresh+=f'multiply_variable = {{ cw_sr_crew_host_{key} = cw_sr_crew_host_factor }}\n'
    refresh+=sv('cw_sr_crew_host_seats','cw_sr_crew_total')+'subtract_from_variable = { cw_sr_crew_host_seats = cw_sr_crew_invited }\n'
    refresh+=block_if(cv('cw_sr_crew_available','=',1),sv('cw_sr_view_mission','cw_sr_crew_host_cost'))
    # IMPERIA COLD WAR — Read-only nationality and contribution presentation.
    refresh+=sv('cw_sr_crew_partner_funding','cw_sr_crew_full_cost')+'subtract_from_variable = { cw_sr_crew_partner_funding = cw_sr_crew_host_cost }\n'
    refresh+=sv('cw_sr_crew_partner_percent',100)+'subtract_from_variable = { cw_sr_crew_partner_percent = cw_sr_crew_host_percent }\n'
    refresh+=sv('cw_sr_crew_share_frame',1)+block_if(cv('cw_sr_crew_host_percent','=',80),sv('cw_sr_crew_share_frame',2))+block_if(cv('cw_sr_crew_host_percent','=',60),sv('cw_sr_crew_share_frame',3))
    for seat in [1,2]:
        refresh+=sv(f'cw_sr_crew_flag_guest{seat}','THIS.id')+block_if(cv(f'cw_sr_crew_view_guest{seat}','>',0),sv(f'cw_sr_crew_flag_guest{seat}',f'cw_sr_crew_view_guest{seat}'))
        refresh+=sv(f'cw_sr_crew_badge{seat}',1)+block_if(cv(f'cw_sr_crew_view_status{seat}','=',1),sv(f'cw_sr_crew_badge{seat}',2))+block_if(cv(f'cw_sr_crew_view_status{seat}','=',2),sv(f'cw_sr_crew_badge{seat}',3)+block_if(cv(f'cw_sr_crew_view_weeks{seat}','>=',26),sv(f'cw_sr_crew_badge{seat}',4)))+block_if(cv(f'cw_sr_crew_view_status{seat}','=',3),sv(f'cw_sr_crew_badge{seat}',5))
    for rank in [1,2,3]:
        refresh+=sv(f'cw_sr_flag_rank{rank}',0)+block_if(f'has_event_target = cw_sr_rank{rank}',f'event_target:cw_sr_rank{rank} = {{ '+sv(f'PREV.cw_sr_flag_rank{rank}','THIS.id')+' }\n')
    # IMPERIA COLD WAR — At most one automatic partner scan per visible game day.
    fx+=effect('cw_sr_crew_refresh','cw_sr_partner_refresh = yes\n'+reset+refresh)
    loc('cw_sr_crew_agreement_terms','§HJOINT TRAINING§!\nWeekly appropriation: §R-$[?cw_sr_crew_training_weekly_m|2]m§! / week\nInitial course: §H26 weeks§!\nQualified refresher: §H6 weeks§!\n\n§HDEPARTURE APPROPRIATION§!\nTreasury: §R-$[?cw_sr_crew_offer_contribution|3]bn§!\n\n§HACCEPTED MISSION AWARDS§!\nNational share: §H20%§!')
    loc('cw_sr_crew_accept','Approve the research astronaut delegation.')
    loc('cw_sr_crew_decline','Decline the invitation.')
    defs+=define('CW_SR_CrewCandidate',[(cv('cw_sr_crew_candidate','>',0),loc('cw_sr_crew_candidate_name','[?cw_sr_crew_candidate.GetName]'))],loc('cw_sr_crew_no_candidate','No other player country'))
    # IMPERIA COLD WAR — A paused hotjoin can also refresh the player list manually.
    defs+=define('CW_SR_PartnerCycle',[(cv('cw_sr_partner_count','>',0),loc('cw_sr_partner_cycle','Next country  >'))],loc('cw_sr_partner_rescan','Refresh players  >'))
    loc('cw_sr_partner_selector_tt','Other player-controlled countries at peace with us can be selected. Click to cycle countries or refresh the list. In singleplayer there may be no eligible partner. Invitations require government approval and the qualifications shown below.')
    for s in [1,2]:
        defs+=define(f'CW_SR_CrewGuest{s}',[(cv(f'cw_sr_crew_view_guest{s}','>',0),loc(f'cw_sr_crew_guest_name{s}',f'[?cw_sr_crew_view_guest{s}.GetName]'))],loc('cw_sr_crew_national_seat','National astronaut'))
        defs+=define(f'CW_SR_CrewStatus{s}',[(cv(f'cw_sr_crew_view_status{s}','=',3),loc('cw_sr_crew_in_flight','§TMission in flight§!')),(cv(f'cw_sr_crew_view_status{s}','=',1),loc('cw_sr_crew_awaiting','§HInvitation awaiting reply§!')),(cv(f'cw_sr_crew_view_status{s}','=',2)+' '+cv(f'cw_sr_crew_view_weeks{s}','>=',26),loc('cw_sr_crew_trained','§GJoint training completed§!')),(cv(f'cw_sr_crew_view_status{s}','=',2),loc(f'cw_sr_crew_training{s}',f'§HJoint training: [?cw_sr_crew_view_weeks{s}|0]/26 weeks§!'))],loc('cw_sr_crew_empty','Available for a national or guest astronaut'))
    defs+=define('CW_SR_CrewResearchReward',[(cv('cw_sr_crew_host_bonus','>',0),loc('cw_sr_crew_research_reward','General research bonus  §G[?cw_sr_crew_host_bonus|0]%§! for 1 technology'))],loc('cw_sr_crew_no_research_reward','General research bonus  -'))
    defs+=define('CW_SR_CrewAwardState',[(cv('cw_sr_crew_awarded','=',1),loc('cw_sr_crew_used_award','Programme award already claimed. Only capped repeat prestige and an unclaimed world first remain.'))],loc('cw_sr_crew_new_award','First accepted programme: rewards split by the agreed crew shares.'))
    # News resolves in the host's country scope, independent of the selected UI.
    for n,p in programmes:
        fields=[field(n,s,'flight') for s in slots(p)]
        entries=[]
        if len(fields)>1:entries.append((cv(fields[0],'>',0)+' '+cv(fields[1],'>',0),loc(f'cw_sr_crew_news_{n}_two',f'The expedition includes research astronauts from [?{fields[0]}.GetName] and [?{fields[1]}.GetName].')))
        for i,f in enumerate(fields):entries.append((cv(f,'>',0),loc(f'cw_sr_crew_news_{n}_{i}',f'The expedition includes a research astronaut from [?{f}.GetName].')))
        defs+=define(f'CW_SR_CrewNews_{n}',entries,loc('cw_sr_crew_news_national','The expedition is staffed by the national astronaut corps.'))
    def frozen_news(name,prefix):
        first,second=prefix+'1',prefix+'2'
        entries=[(cv(first,'>',0)+' '+cv(second,'>',0),loc(prefix+'_two',f'The expedition includes research astronauts from [?{first}.GetName] and [?{second}.GetName].'))]
        for f in [first,second]:entries.append((cv(f,'>',0),loc(f+'_one',f'The expedition includes a research astronaut from [?{f}.GetName].')))
        return define(name,entries,loc('cw_sr_crew_news_empty',''))
    for m,milestone in enumerate(c['DATA']['milestones'],1):defs+=frozen_news(f'CW_SR_CrewMilestone_{m}',f'cw_sr_first_crew_{m}_')
    defs+=frozen_news('CW_SR_LunarCrewNews','cw_sr_lunar_report_crew_')
    c['write']('common/scripted_effects/COLDWAR_space_race_crew.txt',fx)
    c['write']('common/scripted_triggers/COLDWAR_space_race_crew.txt',triggers)
    c['write']('events/COLDWAR_space_race_crew.txt',events)
    return defs


# IMPERIA COLD WAR — Delegate native visual composition to the crew manifest.
def controls(c,a):
    from crew_ui import controls as manifest_controls
    manifest_controls(c,a)
