# IMPERIA COLD WAR — Signed international mission work packages.
"""Two concurrent outbound contracts, independent of astronaut assignments.

One operational partner per flight. Work, invoices, countries and reward shares
are frozen before departure; no new random draw or invisible safety multiplier.
"""
from decimal import Decimal, ROUND_DOWN
from technology_integration import tech, rules, provider_name
from research_rewards import award

SHARE = .10
ORDERS = (1, 2)
ROLES = {
    1: ('Scientific instruments', 26, .002,
        'Flight instruments, calibration, environmental testing and delivery to the operator.'),
    2: ('Tracking & communications', 12, .001,
        'Compatible tracking stations, radio links, scheduled coverage and telemetry handover.'),
    3: ('Mission operations', 20, .002,
        'Flight procedures, simulations, command interfaces and a joint operations team.'),
    4: ('Launch services', 26, .004,
        'Launch-vehicle integration, range coordination, interface qualification and launch support.'),
}


def eligible(p):
    return not p.get('commissioningOnly') and p['flightMonths'] > 0 and p['missionCostB'] > 0


def roles(p):
    # A national launch-vehicle qualification cannot be bought from another state.
    if p['id']=='foreign-launch-partnership':return (4,)
    own_launcher = p['id'] in {'upper-stage','heavy-lift','indigenous-small-launcher','diamant-b','black-arrow','lambda-ohsumi','mu-science','dong-fang-hong','slv-3','nuclear-thermal','energia-buran','n1-l3-recovery','reusable-shuttle'}
    return (1,2,3) if own_launcher else (1,2,3,4)


def field(n, suffix):
    return f'cw_sr_p{n}_op_{suffix}'


def order(w, suffix):
    return f'cw_sr_op_w{w}_{suffix}'


def money(p, fraction):
    return float((Decimal(str(p['missionCostB']))*Decimal(str(fraction))).quantize(Decimal('.001'), rounding=ROUND_DOWN))


def adjustment(p, role):
    return money(p,.35)-money(p,.30) if role == 4 else -money(p,.10)


def capability(p, role):
    base='has_country_flag = cw_sr_cap_space_administration '
    if role == 1:
        payload=rules(p)[1]
        return base+'has_country_flag = cw_sr_cap_scientific_instruments has_country_flag = cw_sr_cap_satellite_engineering '+(tech(payload) if payload else '')
    if role == 2:
        deep='deep-space-communications' in p['capabilityRequirements']
        return base+'has_country_flag = cw_sr_cap_ground_tracking '+('has_country_flag = cw_sr_cap_deep_space_communications' if deep else '')
    if role == 3:
        return base+'has_country_flag = cw_sr_cap_ground_tracking has_country_flag = cw_sr_cap_orbital_flight '+('has_country_flag = cw_sr_cap_crewed_flight' if p['crewSize'] else '')
    return base+'has_country_flag = cw_sr_cap_launch_basic has_country_flag = cw_sr_cap_orbital_flight '+('has_country_flag = cw_sr_cap_crewed_flight ' if p['crewSize'] else '')+('has_country_flag = cw_sr_cap_heavy_lift ' if 'heavy-lift' in p['capabilityRequirements'] else '')+tech('OLV',max(1,rules(p)[0]))


def binding(c,n,w):
    cv=c['cv']; f=lambda x:field(n,x)
    return cv(order(w,'host'),'=','PREV.id')+' '+cv(order(w,'programme'),'=',n)+' '+cv(order(w,'serial'),'=',f'PREV.{f("serial")}')+' '+cv(f'PREV.{f("order")}','=',w)


def gate(c,n,p):
    cv=c['cv']; f=lambda x:field(n,x); entries=[]
    for w in ORDERS:
        alternatives=[]
        for r in roles(p):
            cost=money(p,.30 if r==4 else .10)
            alternatives.append('AND = { '+cv(f'PREV.{f("role")}','=',r)+' '+capability(p,r)+' '+cv(order(w,'weeks'),'>=',ROLES[r][1])+' '+cv('treasury','>=',c['num'](cost))+' }')
        entries.append('AND = { '+cv(f('order'),'=',w)+f' var:{f("country")} = {{ exists = yes is_ai = no NOT = {{ has_war_with = PREV }} '+binding(c,n,w)+' '+cv(order(w,'status'),'=',2)+' OR = { '+' '.join(alternatives)+' } } }')
    return 'OR = { '+cv(f('country'),'=',0)+' AND = { '+cv(f('status'),'=',2)+' OR = { '+' '.join(entries)+' } } }'


def funds(c,n,p):
    from crew import slots, field as seat, contribution
    cv=c['cv']; entries=[]
    for mask in range(2**len(slots(p))):
        conditions=' '.join(cv(seat(n,s,'country'),'>' if mask&(1<<i) else '=',0) for i,s in enumerate(slots(p)))
        base=p['missionCostB']-contribution(p)*mask.bit_count()
        entries.append('AND = { '+conditions+' '+cv(field(n,'country'),'=',0)+' '+cv('treasury','>=',c['num'](base))+' }')
        for r in roles(p):
            entries.append('AND = { '+conditions+' '+cv(field(n,'country'),'>',0)+' '+cv(field(n,'role'),'=',r)+' '+cv('treasury','>=',c['num'](base+adjustment(p,r)))+' }')
    return 'OR = { '+' '.join(entries)+' }'


def snapshot(c,n,p):
    sv,cv,block_if=(c[k] for k in ['sv','cv','block_if']);f=lambda x:field(n,x)
    body=sv(f('flight'),f('country'))+sv(f('flight_role'),f('role'))+sv(f('recorded'),1)+sv(f('status'),3)
    for w in ORDERS:
        b=sv(order(w,'status'),3)
        for r in roles(p):
            cost=money(p,.30 if r==4 else .10)
            b+=block_if(cv(f'PREV.{f("role")}','=',r),c['charge'](c['num'](cost)))
        body+=block_if(cv(f('order'),'=',w),f'var:{f("country")} = {{\n'+b+'}\n')
    # The mission bill already contains the supplied work. Transfer its funded
    # share; launcher providers instead receive a procurement invoice.
    for r in roles(p):
        if r==4:
            b=c['charge'](c['num'](money(p,.35)))+f'var:{f("country")} = {{ '+c['charge'](c['num'](-money(p,.35)))+' }\n'
            # Provider's manufacturing share is part of the ordinary mission bill.
            b+=c['charge'](c['num'](-money(p,.30)))
        else:b=c['charge'](c['num'](-money(p,.10)))
        body+=block_if(cv(f('role'),'=',r),b)
    return block_if(cv(f('country'),'>',0),body,sv(f('flight'),0)+sv(f('recorded'),0))


def distribute(c,n,p,science,pp,bonus,name,kind):
    sv,av,cv,block_if=(c[k] for k in ['sv','av','cv','block_if'])
    gain=sv('cw_sr_op_gain','PREV.cw_sr_crew_pool',True)+'multiply_temp_variable = { cw_sr_op_gain = 0.1 }\n'+av('cw_sr_prestige','cw_sr_op_gain')
    if science:gain+=av('cw_sr_science',c['num'](science*SHARE))
    if pp:gain+='add_political_power = '+c['num'](pp*SHARE)+'\n'
    if bonus:gain+=award(c['ROOT'],name,bonus*SHARE)
    escrow=sv('cw_sr_op_gain','PREV.cw_sr_crew_pool',True)+'multiply_temp_variable = { cw_sr_op_gain = 0.1 }\n'+av('cw_sr_op_pending_prestige','cw_sr_op_gain')+av('cw_sr_op_pending_science',c['num'](science*SHARE))+av('cw_sr_op_pending_pp',c['num'](pp*SHARE))+(f'set_country_flag = cw_sr_op_pending_{name}\n' if bonus else '')
    guest=block_if('is_ai = no',gain,escrow)
    # Shares of one first-success pool cannot be claimed again through a second
    # role, a later launch, or an astronaut assignment to the same programme.
    if kind in ['first','partial']:
        receipt=f'cw_sr_guest_p{n}_{kind}'
        cond=f'NOT = {{ has_country_flag = {receipt} }}'
        if kind=='partial':cond+=f' NOT = {{ has_country_flag = cw_sr_guest_p{n}_first }}'
        guest=block_if(cond,guest+f'set_country_flag = {receipt}\n')
    return block_if(cv(field(n,'recorded'),'=',1)+' '+cv(field(n,'flight'),'>',0),f'var:{field(n,"flight")} = {{\n'+guest+'}\n')


def finish(c,n,p,kind):
    sv,cv,block_if=(c[k] for k in ['sv','cv','block_if']);f=lambda x:field(n,x)
    guest=''
    if kind=='success':guest+=f'set_country_flag = cw_sr_op_p{n}_completed\n'
    for w in ORDERS:
        guest+=block_if(binding(c,n,w),f'cw_sr_op_clear{w} = yes\n')
    for r in roles(p):
        guest+=block_if(cv(f'PREV.{f("flight_role")}',"=",r),f'country_event = {{ id = cw_sr_ops.{n*100+r*10+{"success":2,"partial":3,"failure":4,"catastrophic":5,"abort":6}[kind]} }}\n')
    # Ground personnel never incur astronaut casualties. Keep the frozen country
    # and role for reports; release only the matching signed outbound order.
    body=f'var:{f("flight")} = {{\n'+guest+'}\n'+sv(f('country'),0)+sv(f('status'),0)+sv(f('recorded'),0)
    return block_if(cv(f('recorded'),'=',1)+' '+cv(f('flight'),'>',0),body)


def define(name,entries,fallback):
    return 'defined_text = { name = '+name+'\n'+''.join('text = { trigger = { '+cond+' } localization_key = '+key+' }\n' for cond,key in entries)+'text = { localization_key = '+fallback+' }\n}\n'


def build(c):
    sv,av,cv,block_if,effect,loc=(c[k] for k in ['sv','av','cv','block_if','effect','loc'])
    ps=[(n,p) for n,p in enumerate(c['PROGRAMMES'],1) if eligible(p)]
    fx='';triggers='';events='add_namespace = cw_sr_ops\n';defs='';weekly='';daily='';dispatch='';remove_dispatch='';role_dispatch=''
    refresh=sv('cw_sr_op_available',0)+''.join(sv('cw_sr_op_view_'+key,0) for key in ['country','status','weeks','required','weekly_m','role','bill','return','contribution','count','fee'])
    pending=av('cw_sr_prestige','cw_sr_op_pending_prestige')+av('cw_sr_science','cw_sr_op_pending_science')+'add_political_power = cw_sr_op_pending_pp\n'+''.join(sv('cw_sr_op_pending_'+k,0) for k in ['prestige','science','pp'])
    for n,p in ps:
        if p['rewardEffects']['researchPoints']>=4:
            key=f'cw_sr_p{n}_name';pending+=block_if(f'has_country_flag = cw_sr_op_pending_{key}',award(c['ROOT'],key,.01)+f'clr_country_flag = cw_sr_op_pending_{key}\n')
    for m,_ in enumerate(c['DATA']['milestones'],1):
        key=f'cw_sr_milestone_{m}';pending+=block_if(f'has_country_flag = cw_sr_op_pending_{key}',award(c['ROOT'],key,.02)+f'clr_country_flag = cw_sr_op_pending_{key}\n')
    daily+=block_if(c['guard'](),pending)
    for w in ORDERS:
        fx+=effect(f'cw_sr_op_clear{w}',''.join(sv(order(w,key),0) for key in ['host','programme','role','status','weeks','expires','serial','contribution','fee','required','weekly_m']))
        daily+=block_if(cv(order(w,'status'),'=',1),av(order(w,'expires'),-1)+block_if(cv(order(w,'expires'),'<',1),f'cw_sr_op_clear{w} = yes\n'))
        # Once departed the production and flight-support allocation is paid in
        # full. Later political changes cannot reroll a mission already in flight.
        daily+=block_if(cv(order(w,'status'),'=',2)+' var:'+order(w,'host')+' = { OR = { exists = no is_ai = yes has_war_with = PREV } }',f'cw_sr_op_withdraw{w} = yes\n')
        prep=''
        for r,(label,weeks,cost,detail) in ROLES.items():
            prep+=block_if(cv(order(w,'role'),'=',r)+' '+cv(order(w,'weeks'),'<',weeks)+' '+cv('treasury','>=',cost),c['charge'](cost)+av(order(w,'weeks'),1))
        weekly+=block_if(c['guard']()+' '+cv(order(w,'status'),'=',2)+' cw_sr_op_w'+str(w)+'_preflight_binding = yes',prep)
    # IMPERIA COLD WAR — Shared exact preflight bindings for billing and cleanup.
    withdrawals={w:'' for w in ORDERS};preflight_bindings={w:[] for w in ORDERS}
    for n,p in ps:
        f=lambda x:field(n,x);mutable=c['guard']()+' '+cv(c['var'](n,'state'),'!=',4)
        triggers+=effect(f'cw_sr_p{n}_operations_ready',gate(c,n,p))
        if 4 in roles(p):triggers+=effect(provider_name(p),cv(f('country'),'>',0)+' '+cv(f('role'),'=',4)+' '+gate(c,n,p))
        open_order='OR = { '+' '.join(cv(order(w,'status'),'=',0) for w in ORDERS)+' }'
        # A partner cannot receive two shares of the same mission by also taking
        # an astronaut seat; distinct countries may supply the different roles.
        from crew import slots,field as seat
        distinct=' '.join(cv('cw_sr_crew_candidate','!=',seat(n,s,'country')) for s in slots(p))
        candidate='var:cw_sr_crew_candidate = { exists = yes is_ai = no has_country_flag = cw_sr_initialized NOT = { has_war_with = PREV } NOT = { has_country_flag = cw_sr_op_invitation_open } '+open_order+' }'
        role_tests=[]
        for r in roles(p):role_tests.append('AND = { '+('OR = { '+cv(f('role'),'=',0)+' '+cv(f('role'),'=',r)+' }' if r==roles(p)[0] else cv(f('role'),'=',r))+' var:cw_sr_crew_candidate = { '+capability(p,r)+' } }')
        allowed=mutable+' date > '+str(p['minYear']-1)+'.12.31 OR = { '+' '.join(cv(c['var'](n,'state'),'=',s) for s in [1,2,3,5,6])+' } '+cv(f('country'),'=',0)+' '+cv('cw_sr_crew_candidate','>',0)+' '+cv('cw_sr_crew_candidate','!=','THIS.id')+' '+distinct+' '+candidate+' OR = { '+' '.join(role_tests)+' }'
        triggers+=effect(f'cw_sr_p{n}_op_invite_allowed',allowed)
        invite=block_if(cv(f('role'),'=',0),sv(f('role'),roles(p)[0]))+sv(f('country'),'cw_sr_crew_candidate')+sv(f('status'),1)+av(f('serial'),1)+sv(f('order'),0)
        # Lowest free outbound work order, selected deterministically. Do not
        # overwrite either accepted commitments or unresolved invitation windows.
        for w in ORDERS:
            b=sv('PREV.'+f('order'),w)+sv(order(w,'host'),'PREV.id')+sv(order(w,'programme'),n)+sv(order(w,'role'),'PREV.'+f('role'))+sv(order(w,'serial'),'PREV.'+f('serial'))+sv(order(w,'status'),1)+sv(order(w,'weeks'),0)+sv(order(w,'expires'),90)+sv('cw_sr_op_offer_host','PREV.id')+sv('cw_sr_op_offer_programme',n)+sv('cw_sr_op_offer_order',w)+sv('cw_sr_op_offer_serial','PREV.'+f('serial'))+sv('cw_sr_op_offer_role','PREV.'+f('role'))+'set_country_flag = cw_sr_op_invitation_open\n'
            for r,(_,weeks,cost,_) in ROLES.items():
                b+=block_if(cv(order(w,'role'),'=',r),sv('cw_sr_op_offer_weeks',weeks)+sv('cw_sr_op_offer_weekly_m',cost*1000)+sv('cw_sr_op_offer_contribution',money(p,.30 if r==4 else .10))+sv('cw_sr_op_offer_fee',money(p,.35) if r==4 else 0)+sv(order(w,'contribution'),money(p,.30 if r==4 else .10))+sv(order(w,'fee'),money(p,.35) if r==4 else 0)+sv(order(w,'required'),weeks)+sv(order(w,'weekly_m'),cost*1000))
            b+=f'country_event = {{ id = cw_sr_ops.{n*10+1} }}\n'
            invite+=f'var:{f("country")} = {{\n'+block_if(cv('PREV.'+f('order'),'=',0)+' '+cv(order(w,'status'),'=',0),b)+'}\n'
        fx+=effect(f'cw_sr_p{n}_op_invite',block_if(f'cw_sr_p{n}_op_invite_allowed = yes',invite))
        dispatch+=block_if(cv('cw_sr_selected','=',n),f'cw_sr_p{n}_op_invite = yes\n')
        # Role changes cannot invalidate an accepted agreement underneath its owner.
        change=block_if(cv(f('role'),'=',0),sv(f('role'),roles(p)[0]))+av(f('role'),1)+block_if(cv(f('role'),'>',max(roles(p))),sv(f('role'),roles(p)[0]))
        role_dispatch+=block_if(cv('cw_sr_selected','=',n)+' '+cv(f('country'),'=',0)+' '+cv(c['var'](n,'state'),'!=',4),change)
        remove=''
        bindings=[]
        for w in ORDERS:
            b=binding(c,n,w)
            remove+=block_if(cv(f('order'),'=',w),f'var:{f("country")} = {{ '+block_if(b,f'cw_sr_op_clear{w} = yes\n')+' }\n')
            consistent='var:'+f('country')+' = { exists = yes '+b+' '+cv(order(w,'status'),'>',0)+' }'
            bindings.append('AND = { '+cv(f('order'),'=',w)+' '+consistent+' }')
            withdrawals[w]+=block_if(cv(order(w,'programme'),'=',n),f'var:{order(w,"host")} = {{\n'+block_if(cv(c['var'](n,'state'),'!=',4)+' '+cv(f('country'),'=','PREV.id')+' '+cv(f('serial'),'=','PREV.'+order(w,'serial'))+' '+cv(f('order'),'=',w),sv(f('country'),0)+sv(f('status'),0))+'}\n'+f'cw_sr_op_clear{w} = yes\n')
        fx+=effect(f'cw_sr_p{n}_op_remove',block_if(mutable,remove+sv(f('country'),0)+sv(f('status'),0)))
        remove_dispatch+=block_if(cv('cw_sr_selected','=',n),f'cw_sr_p{n}_op_remove = yes\n')
        # IMPERIA COLD WAR — Recover orphaned outbound capacity by exact binding.
        for w in ORDERS:
            # IMPERIA COLD WAR — An invalidated work order cannot keep buying training.
            preflight_host=f'var:{order(w,"host")} = {{ exists = yes is_ai = no NOT = {{ has_war_with = PREV }} '+cv(c['var'](n,'state'),'!=',4)+' '+cv(f('country'),'=','PREV.id')+' '+cv(f('order'),'=',w)+' '+cv(f('serial'),'=','PREV.'+order(w,'serial'))+' '+cv(f('role'),'=','PREV.'+order(w,'role'))+' '+cv(f('status'),'=','PREV.'+order(w,'status'))+' }'
            preflight_bindings[w].append('AND = { '+cv(order(w,'programme'),'=',n)+' '+preflight_host+' }')
            valid_host=f'var:{order(w,"host")} = {{ exists = yes '+cv(f('country'),'=','PREV.id')+' '+cv(f('order'),'=',w)+' '+cv(f('serial'),'=','PREV.'+order(w,'serial'))+' }'
            daily+=block_if(cv(order(w,'programme'),'=',n)+' '+cv(order(w,'status'),'>',0)+' NOT = { '+valid_host+' }',f'cw_sr_op_clear{w} = yes\n')
        daily+=block_if(cv(c['var'](n,'state'),'!=',4)+' '+cv(f('country'),'>',0)+' NOT = { OR = { '+' '.join(bindings)+' } }',sv(f('country'),0)+sv(f('status'),0))
        # Accept rechecks identity, serial, order, country, peace and capability.
        accepts=[];accept_body=''
        for w in ORDERS:
            b=cv('cw_sr_op_offer_order','=',w)+' '+cv(order(w,'status'),'=',1)+' '+cv(order(w,'programme'),'=',n)+' '+cv(order(w,'expires'),'>',0)+' '+cv(order(w,'serial'),'=','cw_sr_op_offer_serial')+' '+cv(order(w,'host'),'=','cw_sr_op_offer_host')
            host=f'var:{order(w,"host")} = {{ exists = yes is_ai = no NOT = {{ has_war_with = PREV }} '+cv(c['var'](n,'state'),'!=',4)+' '+cv(f('country'),'=','PREV.id')+' '+cv(f('order'),'=',w)+' '+cv(f('status'),'=',1)+' '+cv(f('serial'),'=','PREV.'+order(w,'serial'))+' '+cv(f('role'),'=','PREV.'+order(w,'role'))+' }'
            rolecond='OR = { '+' '.join('AND = { '+cv(order(w,'role'),'=',r)+' '+capability(p,r)+' }' for r in roles(p))+' }'
            accepts.append('AND = { '+b+' '+host+' '+rolecond+' }')
            accept_body+=block_if(cv('cw_sr_op_offer_order','=',w),sv(order(w,'status'),2)+f'var:{order(w,"host")} = {{ '+sv(f('status'),2)+' }\n')
        offer=cv('cw_sr_op_offer_programme','=',n)+' has_country_flag = cw_sr_op_invitation_open'
        valid=offer+' OR = { '+' '.join(accepts)+' }'
        fx+=effect(f'cw_sr_op_accept_{n}',block_if(c['guard']()+' '+valid,'clr_country_flag = cw_sr_op_invitation_open\n'+accept_body))
        decline='clr_country_flag = cw_sr_op_invitation_open\n'+''.join(block_if(cv('cw_sr_op_offer_order','=',w)+' '+cv(order(w,'status'),'=',1)+' '+cv(order(w,'serial'),'=','cw_sr_op_offer_serial')+' '+cv(order(w,'programme'),'=',n),f'cw_sr_op_withdraw{w} = yes\n') for w in ORDERS)
        fx+=effect(f'cw_sr_op_decline_{n}',block_if(offer,decline))
        title=loc(f'cw_sr_ops.{n*10+1}.t','[ROOT.GetName]: Joint Mission Work Package')
        desc=loc(f'cw_sr_ops.{n*10+1}.d',f'[?cw_sr_op_offer_host.GetName] invites [ROOT.GetName] to supply [CW_SR_OpOfferRole] for {p["name"]}. The operator retains command and flight-safety authority.\n\nApproval reserves one national work order. Interface qualification must be funded before departure. The flight allocation then funds delivery and support through mission completion. Either government may withdraw before departure; spent qualification funds are retained.\n\nThe offer expires after 90 days. Awards are shared only for results still available to the mission.')
        events+=f'country_event = {{ id = cw_sr_ops.{n*10+1} title = {title} desc = {desc} picture = GFX_cw_sr_report_mission-control is_triggered_only = yes option = {{ name = cw_sr_op_accept trigger = {{ is_ai = no {valid} }} cw_sr_op_accept_{n} = yes custom_effect_tooltip = cw_sr_op_numeric_terms }} option = {{ name = cw_sr_op_decline cw_sr_op_decline_{n} = yes }} }}\n'
        # IMPERIA COLD WAR — Constant role text and native FROM keep concurrent reports independent.
        for r in roles(p):
            for stage,label,phrase in [(2,'Joint Mission Completed','accepted results'),(3,'Joint Mission: Partial Results','limited results'),(4,'Joint Mission Failed','mission failure'),(5,'Joint Mission Accident','a catastrophic accident'),(6,'Joint Launch Aborted','a safe launch abort')]:
                ident=n*100+r*10+stage
                t=loc(f'cw_sr_ops.{ident}.t','[ROOT.GetName]: '+label)
                d=loc(f'cw_sr_ops.{ident}.d',f'[FROM.GetName] reports {phrase} under {p["name"]}. [ROOT.GetName] supplied {ROLES[r][0].lower()}. '+('The agreed share of available awards has been credited.' if stage in [2,3] else 'The joint flight authority has released its report.'))
                events+=f'country_event = {{ id = cw_sr_ops.{ident} title = {t} desc = {d} picture = GFX_cw_sr_report_mission-control is_triggered_only = yes option = {{ name = cw_sr_acknowledge }} }}\n'
        # Stable report descriptions use the frozen flight country and role.
        entries=[]
        for r in roles(p):entries.append((cv(f('flight'),'>',0)+' '+cv(f('flight_role'),'=',r),loc(f'cw_sr_op_news_{n}_{r}',f'[?{f("flight")}.GetName] supplied {ROLES[r][0].lower()} under the joint mission agreement.')))
        defs+=define(f'CW_SR_OpNews_{n}',entries,loc('cw_sr_op_news_empty',''))
        view=sv('cw_sr_op_available',1)+sv('cw_sr_op_view_country',f('country'))+sv('cw_sr_op_view_status',f('status'))+sv('cw_sr_op_view_role',f('role'))+sv('cw_sr_op_view_bill',p['missionCostB'])
        view+=block_if(cv(f('role'),'=',0),sv('cw_sr_op_view_role',roles(p)[0]))
        view+=block_if(cv(c['var'](n,'state'),'=',4),sv('cw_sr_op_view_country',f('flight'))+sv('cw_sr_op_view_role',f('flight_role')))
        for r,(_,weeks,cost,_) in ROLES.items():
            view+=block_if(cv('cw_sr_op_view_role','=',r),sv('cw_sr_op_view_required',weeks)+sv('cw_sr_op_view_weekly_m',cost*1000)+sv('cw_sr_op_view_contribution',money(p,.30 if r==4 else .10))+sv('cw_sr_op_view_fee',money(p,.35) if r==4 else 0))
        for w in ORDERS:view+=block_if(cv(f('country'),'>',0)+' '+cv(f('order'),'=',w),f'var:{f("country")} = {{ '+sv('PREV.cw_sr_op_view_weeks',order(w,'weeks'))+' }\n')
        view+=block_if(cv('cw_sr_op_view_country','>',0),av('cw_sr_crew_host_percent',-10)+sv('cw_sr_op_view_count',1))
        # Crew refresh already populated its net bill; uncrewed missions start
        # at the full appropriation. This view is never used to authorize a bill.
        from crew import eligible as crew_eligible
        if not crew_eligible(p):view+=sv('cw_sr_crew_full_cost',p['missionCostB'])+sv('cw_sr_crew_host_cost',p['missionCostB'])+sv('cw_sr_crew_partner_funding',0)
        for r in roles(p):view+=block_if(cv('cw_sr_op_view_country','>',0)+' '+cv('cw_sr_op_view_role','=',r),av('cw_sr_crew_host_cost',c['num'](adjustment(p,r))))
        refresh+=block_if(cv('cw_sr_selected','=',n),view)
    # IMPERIA COLD WAR — Reclaim stale pending and accepted preflight capacity.
    for w in ORDERS:
        triggers+=effect(f'cw_sr_op_w{w}_preflight_binding','OR = { '+' '.join(preflight_bindings[w])+' }')
        mutable_order='OR = { '+cv(order(w,'status'),'=',1)+' '+cv(order(w,'status'),'=',2)+' }'
        daily+=block_if(c['guard']()+' '+mutable_order+f' NOT = {{ cw_sr_op_w{w}_preflight_binding = yes }}',f'cw_sr_op_withdraw{w} = yes\n')
    for w in ORDERS:
        fx+=effect(f'cw_sr_op_withdraw{w}',block_if('IMP_is_1970_scenario = yes OR = { '+cv(order(w,'status'),'=',1)+' '+cv(order(w,'status'),'=',2)+' }',withdrawals[w]))
    fx+=effect('cw_sr_op_weekly',weekly)+effect('cw_sr_op_daily',daily)+effect('cw_sr_op_invite',dispatch)+effect('cw_sr_op_remove',remove_dispatch)+effect('cw_sr_op_role_next',role_dispatch)
    refresh+=block_if(cv('cw_sr_op_available','=',1),sv('cw_sr_view_mission','cw_sr_crew_host_cost'))
    # Native read-only preview uses a common national reward pool after both
    # astronaut and operational shares, never copies of the full reward.
    for n,p in ps:
        b=sv('cw_sr_op_factor','cw_sr_crew_host_percent')+'divide_variable = { cw_sr_op_factor = 100 }\n'
        # IMPERIA COLD WAR — Operational shares use the same remaining prestige as the real award.
        for key,value in [('prestige','cw_sr_view_first_prestige'),('science',p['rewardEffects']['researchPoints']),('pp',p['rewardEffects']['politicalCapital']),('bonus',10 if p['rewardEffects']['researchPoints']>=4 else 0)]:b+=sv('cw_sr_crew_host_'+key,value)+f'multiply_variable = {{ cw_sr_crew_host_{key} = cw_sr_op_factor }}\n'
        refresh+=block_if(cv('cw_sr_selected','=',n),b)
    refresh+=block_if(cv('cw_sr_op_available','=',1)+' '+cv('cw_sr_op_view_country','>',0)+' '+cv('cw_sr_op_view_role','!=',4),av('cw_sr_crew_partner_funding','cw_sr_op_view_contribution'))
    refresh+=sv('cw_sr_crew_partner_percent',100)+'subtract_from_variable = { cw_sr_crew_partner_percent = cw_sr_crew_host_percent }\n'
    refresh+=sv('cw_sr_crew_share_frame',1)
    for i,percent in enumerate([100,90,80,70,60,50],1):refresh+=block_if(cv('cw_sr_crew_host_percent','=',percent),sv('cw_sr_crew_share_frame',i))
    fx+=effect('cw_sr_op_refresh',refresh)
    for name,v in [('Offer','cw_sr_op_offer_role'),('Report','cw_sr_op_report_role'),('Selected','cw_sr_op_view_role')]:defs+=define('CW_SR_Op'+name+'Role',[(cv(v,'=',r),loc('cw_sr_op_role_'+str(r),role[0])) for r,role in ROLES.items()],loc('cw_sr_op_no_role','No work package'))
    defs+=define('CW_SR_OpStatus',[(cv('cw_sr_op_view_status','=',3),loc('cw_sr_op_flight','§TMission allocation committed§!')),(cv('cw_sr_op_view_status','=',1),loc('cw_sr_op_pending','§HAwaiting government approval§!')),(cv('cw_sr_op_view_status','=',2)+' '+cv('cw_sr_op_view_weeks','>=','cw_sr_op_view_required'),loc('cw_sr_op_ready','§GInterface qualification complete§!')),(cv('cw_sr_op_view_status','=',2),loc('cw_sr_op_work','§HQualification [?cw_sr_op_view_weeks|0]/[?cw_sr_op_view_required|0] weeks§!'))],loc('cw_sr_op_national','National delivery · Full national share'))
    defs+=define('CW_SR_OpCountry',[(cv('cw_sr_op_view_country','>',0),loc('cw_sr_op_country','[?cw_sr_op_view_country.GetName]'))],loc('cw_sr_op_none','No operational partner assigned'))
    for w in ORDERS:
        defs+=define(f'CW_SR_OpWork{w}',[(cv(order(w,'status'),'>',0),loc(f'cw_sr_op_work{w}',f'[?{order(w,"host")}.GetName] · [CW_SR_OpWorkRole{w}]\n[CW_SR_OpWorkProgramme{w}]\n[CW_SR_OpWorkStatus{w}]'))],loc('cw_sr_op_free','Available work order'))
        loc(f'cw_sr_op_workterms_{w}',f'Qualification: [?{order(w,"weeks")}|0]/[?{order(w,"required")}|0] weeks · $[?{order(w,"weekly_m")}|2]m / week\nFlight allocation: $[?{order(w,"contribution")}|3]bn · Invoice: +$[?{order(w,"fee")}|3]bn\nNational award share: 10% of the available mission pool.')
        defs+=define(f'CW_SR_OpWorkTerms{w}',[],f'cw_sr_op_workterms_{w}')
        defs+=define(f'CW_SR_OpWorkRole{w}',[(cv(order(w,'role'),'=',r),loc('cw_sr_op_role_'+str(r),role[0])) for r,role in ROLES.items()],'cw_sr_op_no_role')
        defs+=define(f'CW_SR_OpWorkProgramme{w}',[(cv(order(w,'programme'),'=',n),f'cw_sr_p{n}_name') for n,p in ps],'cw_sr_op_no_role')
        defs+=define(f'CW_SR_OpWorkStatus{w}',[(cv(order(w,'status'),'=',1),'cw_sr_op_pending'),(cv(order(w,'status'),'=',3),'cw_sr_op_flight')],loc(f'cw_sr_op_workstatus{w}',f'Qualification: [?{order(w,"weeks")}|0] paid weeks'))
    defs+=define('CW_SR_OpRequirements',[(cv('cw_sr_selected','=',n),loc('cw_sr_op_requirements_'+str(n),'[CW_SR_OpCapabilities_'+str(n)+']')) for n,p in ps],'cw_sr_op_no_role')
    for n,p in ps:
        labels={1:'Space administration, satellite engineering and scientific instruments'+('; '+rules(p)[1]+' research' if rules(p)[1] else ''),2:'Space administration and ground tracking'+('; deep-space communications' if 'deep-space-communications' in p['capabilityRequirements'] else ''),3:'Space administration, ground tracking and orbital-flight experience'+('; crewed-flight experience' if p['crewSize'] else ''),4:'Space administration, qualified orbital launch operations and the required OLV generation'+('; heavy-lift qualification' if 'heavy-lift' in p['capabilityRequirements'] else '')}
        defs+=define('CW_SR_OpCapabilities_'+str(n),[(cv('cw_sr_op_view_role','=',r),loc(f'cw_sr_op_capabilities_{n}_{r}',labels[r])) for r in roles(p)],'cw_sr_op_no_role')
    defs+=define('CW_SR_CombinedFinance',[(cv('cw_sr_op_view_count','=',1)+' '+cv('cw_sr_op_view_role','=',4),loc('cw_sr_op_procured_line','Launch procurement included in the national bill.'))],loc('cw_sr_op_financing_line','Partner financing: §T$[?cw_sr_crew_partner_funding|3]bn§!'))
    defs+=define('CW_SR_OpFinance',[(cv('cw_sr_op_view_role','=',4),loc('cw_sr_op_procurement','Launch procurement: 35% fee; 30% of flight bill replaced.'))],loc('cw_sr_op_cofunding','Joint delivery: partner finances 10% of the flight bill.'))
    defs+=define('CW_SR_OpFee',[(cv('cw_sr_op_view_role','=',4),loc('cw_sr_op_fee','Launch-service invoice: $[?cw_sr_op_view_fee|3]bn'))],loc('cw_sr_op_no_fee','No procurement invoice for this role.'))
    loc('cw_sr_op_invite_tt','Requires a qualified player country at peace with the operator, a free national work order and no other participation in this mission. Complete partner capabilities are listed below. An existing invitation must be answered before another can be issued.')
    # IMPERIA COLD WAR — First-achievement reports keep the original contributors.
    for m,_ in enumerate(c['DATA']['milestones'],1):
        entries=[(cv(f'cw_sr_first_op_{m}','>',0)+' '+cv(f'cw_sr_first_op_role_{m}','=',r),loc(f'cw_sr_op_first_news_{m}_{r}',f'[?cw_sr_first_op_{m}.GetName] supplied {role[0].lower()} under the joint mission agreement.')) for r,role in ROLES.items()]
        defs+=define(f'CW_SR_OpMilestone_{m}',entries,'cw_sr_op_news_empty')
    defs+=define('CW_SR_LunarOpNews',[(cv('cw_sr_lunar_report_op','>',0)+' '+cv('cw_sr_lunar_report_op_role','=',r),loc(f'cw_sr_op_lunar_news_{r}',f'[?cw_sr_lunar_report_op.GetName] supplied {role[0].lower()} under the joint mission agreement.')) for r,role in ROLES.items()],'cw_sr_op_news_empty')
    loc('cw_sr_op_accept','Approve the joint work package.')
    loc('cw_sr_op_decline','Decline the work package.')
    loc('cw_sr_op_numeric_terms','§HINTERFACE QUALIFICATION§!\nWeekly appropriation: §R-$[?cw_sr_op_offer_weekly_m|2]m§! / week\nPaid qualification: §H[?cw_sr_op_offer_weeks|0] weeks§!\n\n§HDEPARTURE APPROPRIATION§!\nTreasury: §R-$[?cw_sr_op_offer_contribution|3]bn§!\nLaunch-service invoice: §G+$[?cw_sr_op_offer_fee|3]bn§!\n\n§HAVAILABLE MISSION AWARDS§!\nNational share: §H10%§!')
    c['write']('common/scripted_effects/COLDWAR_space_race_cooperation.txt',fx)
    c['write']('common/scripted_triggers/COLDWAR_space_race_cooperation.txt',triggers)
    c['write']('events/COLDWAR_space_race_cooperation.txt',events)
    return defs
