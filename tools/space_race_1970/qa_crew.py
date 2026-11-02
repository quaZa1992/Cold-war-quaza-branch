# IMPERIA COLD WAR — International crew consent, funding and award invariants.
# COLDWAR 2025-cut: test fixtures use tier 6, the highest remaining OLV/GNSS/COMSAT/SPYSAT research.
from copy import deepcopy
import json
from pathlib import Path
import validate as V
from crew import eligible,slots,field,TRAINING_WEEKS,contribution
from mission_rules import REQUIREMENTS


def setup(n=27):
    m=V.Machine(('SOV','DDR','POL','USA','FRA'));m.countries['FRA'].ai=True
    for country in m.countries.values():m.c=country;m.init()
    m.c=m.countries['SOV'];p=V.DATA['programmes'][n-1]
    m.date='1995.12.1';m.g.update(year=V.D(1995),month=V.D(12),cw_sr_window_mars=V.D(0),cw_sr_window_venus=V.D(0))
    m.c.flags.update('cw_sr_cap_'+k.replace('-','_') for k in p['capabilityRequirements'])
    ids={p['id']:i for i,p in enumerate(V.DATA['programmes'],1)}
    for group in REQUIREMENTS.get(p['id'],[]):m.c.flags.add('cw_sr_p'+str(ids[group[0]])+'_awarded')
    m.c.technologies.update(['OLV6','GNSS6','COMSAT6','SPYSAT6'])
    m.put(f'cw_sr_p{n}_state',3);m.put(f'cw_sr_p{n}_work',100);m.put(f'cw_sr_p{n}_months',p['durationMonths']);m.put('cw_sr_selected',n)
    return m,p


def invite(m,n,s,tag,train=True):
    m.c=m.countries['SOV'];m.put('cw_sr_crew_candidate',m.country_ids[tag]);m.call(f'cw_sr_p{n}_crew_invite{s}')
    m.c=m.countries[tag];V.check(m.get('cw_sr_crew_status')==1,'Invitation not delivered')
    m.call(f'cw_sr_crew_accept_{n}');V.check(m.get('cw_sr_crew_status')==2,'Valid invitation could not be accepted')
    if train:
        initial=m.get('treasury')
        for _ in range(TRAINING_WEEKS):m.call('cw_sr_crew_training_weekly')
        V.check(initial-m.get('treasury')==V.D('.052'),'Joint training did not cost 26 x $2m')
    m.c=m.countries['SOV']


def economic(m):
    return [(c.tag,deepcopy(c.variables),c.pp,c.manpower,deepcopy(c.flags),deepcopy(c.tech_bonuses)) for c in m.countries.values()]


def run():
    # The pure-national route retains its old launch and award behaviour.
    for n,p in enumerate(V.DATA['programmes'],1):
        if not eligible(p):continue
        t,_=setup(n)
        if 'fixedWindowStartMonth' in p:t.date='1984.12.1'
        V.check(t.test(V.TRIGGERS[f'cw_sr_p{n}_crew_ready']),'National crew incorrectly blocked '+p['id'])
        V.check(t.test(V.TRIGGERS[f'cw_sr_p{n}_launch_allowed']),'Valid national launch broken '+p['id'])
        V.check(len(slots(p))<p['crewSize'],'Guest crew replaces the national commander')
    m,p=setup()
    m.call('cw_sr_crew_candidate_next');V.check(m.get('cw_sr_crew_candidate')==m.country_ids['DDR'],'First partner selection is not the first other human country')
    m.call('cw_sr_crew_candidate_next');V.check(m.get('cw_sr_crew_candidate')==m.country_ids['POL'],'Country selector did not advance')
    m.countries['USA'].ai=True;m.call('cw_sr_crew_candidate_next');V.check(m.get('cw_sr_crew_candidate')==m.country_ids['DDR'],'Country selector included AI or failed to wrap')
    # Self-invitation, AI invitations and countries at war are rejected.
    for tag in ['SOV','USA']:
        m.put('cw_sr_crew_candidate',m.country_ids[tag]);m.call('cw_sr_p27_crew_invite1');V.check(m.get(field(27,1,'country'))==0,'Invalid partner accepted '+tag)
    m.wars.add(frozenset(('SOV','POL')));m.put('cw_sr_crew_candidate',m.country_ids['POL']);m.call('cw_sr_p27_crew_invite1');V.check(m.get(field(27,1,'country'))==0,'Enemy astronaut accepted');m.wars.clear()
    # Acceptance is necessary, and paid training cannot be bypassed with a click.
    m.put('cw_sr_crew_candidate',m.country_ids['DDR']);m.call('cw_sr_p27_crew_invite1')
    V.check(not m.test(V.TRIGGERS['cw_sr_p27_launch_allowed']),'Pending consent did not block departure')
    m.c=m.countries['DDR'];m.call('cw_sr_crew_accept_27');m.put('treasury',0);m.call('cw_sr_crew_training_weekly')
    V.check(m.get('cw_sr_crew_weeks')==0 and m.get('treasury')==0,'Unfunded training advanced')
    m.put('treasury',100)
    for _ in range(25):m.call('cw_sr_crew_training_weekly')
    m.c=m.countries['SOV'];V.check(not m.test(V.TRIGGERS['cw_sr_p27_launch_allowed']),'Incomplete joint training permitted departure')
    m.c=m.countries['DDR'];m.call('cw_sr_crew_training_weekly');m.c=m.countries['SOV']
    invite(m,27,2,'POL');V.check(m.test(V.TRIGGERS['cw_sr_p27_launch_allowed']),'Qualified joint crew cannot launch')
    # A fresh invitation cannot silently replace an accepted guest.
    before=economic(m);m.put('cw_sr_crew_candidate',m.country_ids['USA']);m.call('cw_sr_p27_crew_invite1')
    V.check(m.get(field(27,1,'country'))==m.country_ids['DDR'],'Accepted seat overwritten')
    # Contributions are charged once, only on a real guarded departure.
    shares={c.tag:c.variables['treasury'] for c in m.countries.values()};m.put('treasury',V.D(p['missionCostB'])-2*V.D(contribution(p)))
    V.check(m.test(V.TRIGGERS['cw_sr_p27_launch_allowed']),'Net appropriation check still requires the gross bill')
    m.rolls.append(0);m.call('cw_sr_p27_launch')
    V.check(abs(m.get('treasury'))<=V.D('.002'),'Host departure bill was not reduced to 70%')
    for tag in ['DDR','POL']:
        V.check(shares[tag]-m.countries[tag].variables['treasury']==V.D(contribution(p)),'Guest contribution wrong')
    snapshot=economic(m);m.call('cw_sr_p27_launch');m.call('cw_sr_p27_crew_remove1');m.call('cw_sr_p27_crew_invite1')
    V.check(economic(m)==snapshot,'In-flight crew could be changed or launch charged again')
    # Refresh and view navigation cannot train, pay, or change any campaign award.
    def assets():return [(c.variables['treasury'],c.variables.get('cw_sr_prestige',0),c.pp,c.manpower,deepcopy(c.tech_bonuses)) for c in m.countries.values()]
    stable=assets()
    for _ in range(3):m.call('cw_sr_refresh')
    V.check(assets()==stable,'Read-only crew view changed campaign assets')
    # First-success pool is precisely 60/20/20, including a single-use all-tech bonus.
    base={c.tag:(c.variables.get('cw_sr_prestige',V.D(0)),c.variables.get('cw_sr_science',V.D(0)),c.pp,len(c.tech_bonuses),{k for k in c.flags if k.startswith('cw_sr_cap_')}) for c in m.countries.values()}
    m.call('cw_sr_p27_success')
    for tag,fraction,bonus in [('SOV','.6','0.06'),('DDR','.2','0.02'),('POL','.2','0.02')]:
        c=m.countries[tag];old=base[tag];factor=V.D(fraction)
        V.check(c.variables['cw_sr_prestige']-old[0]==V.D(p['prestige'])*factor,'Prestige share wrong '+tag)
        V.check(c.variables['cw_sr_science']-old[1]==V.D(p['rewardEffects']['researchPoints'])*factor,'Science share wrong '+tag)
        V.check(c.pp-old[2]==V.D(p['rewardEffects']['politicalCapital'])*factor,'Political reward share wrong '+tag)
        V.check(len(c.tech_bonuses)==old[3]+1 and c.tech_bonuses[-1][2]==bonus,'Research bonus was duplicated instead of divided '+tag)
        V.check(c.variables.get('cw_sr_crew_status',0)==0,'Completed mission kept a foreign crew reservation '+tag)
    V.check({k for k in m.countries['DDR'].flags if k.startswith('cw_sr_cap_')}==base['DDR'][4],'Guest inherited host spacecraft/launch capability')
    V.check(not any(k=='cw_sr_p27_awarded' for k in m.countries['DDR'].flags),'Guest flight created domestic lunar qualification')
    old=[len(c.tech_bonuses) for c in m.countries.values()]
    for _ in range(10):m.call('cw_sr_p27_success')
    V.check([len(c.tech_bonuses) for c in m.countries.values()]==old,'Repeat mission created research rewards')
    # An AI takeover after launch cannot collect player-only research/economic awards.
    t,p=setup();invite(t,27,1,'DDR');t.rolls.append(0);t.call('cw_sr_p27_launch');guest=t.countries['DDR'];guest.ai=True
    t.call('cw_sr_p27_success');V.check(not guest.tech_bonuses and not guest.variables.get('cw_sr_prestige',0),'AI collected a player award')
    guest.ai=False;t.c=guest;t.call('cw_sr_crew_daily');V.check(len(guest.tech_bonuses)==1 and guest.variables['cw_sr_prestige']==V.D(p['prestige'])*V.D('.2'),'Returning player did not receive exactly the signed entitlement')
    old=deepcopy(guest.tech_bonuses);t.call('cw_sr_crew_daily');V.check(guest.tech_bonuses==old,'Escrow paid twice')
    # Every failure path releases seats; fatalities follow nationality and phase.
    for kind in ['abort','partial','failure','catastrophic']:
        t,p=setup();invite(t,27,1,'DDR');invite(t,27,2,'POL');t.rolls.append(0);t.call('cw_sr_p27_launch');t.call('cw_sr_p27_'+kind)
        V.check(all(c.variables.get('cw_sr_crew_status',0)==0 for c in t.countries.values()),kind+' leaked a reservation')
        V.check(not any(c.tech_bonuses for c in t.countries.values()),kind+' granted full research rewards')
        if kind=='catastrophic':
            for tag in ['SOV','DDR','POL']:
                V.check(t.countries[tag].variables['cw_sr_fatalities']==1,'Fatality attributed to wrong nationality '+tag)
                V.check(t.countries[tag].manpower==99999,'Manpower loss attributed to wrong nationality '+tag)
        else:V.check(all(c.manpower==100000 for c in t.countries.values()),kind+' caused spurious crew deaths')
    # A host cannot spend a guest's money after withdrawal, expiry, or stale consent.
    for action in ['withdraw','expiry','serial']:
        t,p=setup();invite(t,27,1,'DDR',False);t.c=t.countries['DDR']
        if action=='withdraw':t.call('cw_sr_crew_withdraw')
        if action=='expiry':t.put('cw_sr_crew_status',1);t.put('cw_sr_crew_expires',1);t.call('cw_sr_crew_daily')
        if action=='serial':
            t.put('cw_sr_crew_status',1);t.put('cw_sr_crew_serial',0);t.call('cw_sr_crew_accept_27')
            V.check(t.get('cw_sr_crew_status')==1,'Old invitation accepted a replacement offer')
        t.c=t.countries['SOV'];t.call('cw_sr_crew_daily')
        if action!='serial':V.check(t.get(field(27,1,'country'))==0,'Stale seat not reclaimed after '+action)
    # Completed training survives a safe abort; fatal losses require a new course.
    t,p=setup();invite(t,27,1,'DDR');t.rolls.append(0);t.call('cw_sr_p27_launch');t.call('cw_sr_p27_abort');t.put('cw_sr_p27_state',3)
    invite(t,27,1,'DDR',False);t.c=t.countries['DDR'];V.check(t.get('cw_sr_crew_weeks')==20,'Safe abort erased the astronaut course')
    initial=t.get('treasury')
    for _ in range(6):t.call('cw_sr_crew_training_weekly')
    V.check(t.get('cw_sr_crew_weeks')==26 and initial-t.get('treasury')==V.D('.012'),'Refresher did not require six funded weeks')
    t,p=setup(15);invite(t,15,1,'DDR');t.rolls.extend([9999,0]);t.call('cw_sr_p15_launch')
    V.check(all(c.manpower==100000 for c in t.countries.values()),'Uncrewed station launch killed its future station crew')
    t,p=setup();invite(t,27,1,'DDR');t.call('cw_sr_p27_cancel')
    V.check(t.countries['DDR'].variables['cw_sr_crew_status']==0 and t.get(field(27,1,'country'))==0,'Cancelled programme retained a signed guest')
    t,p=setup();t.put('cw_sr_crew_candidate',t.country_ids['DDR']);t.call('cw_sr_p27_crew_invite1');t.call('cw_sr_p27_crew_remove1');t.call('cw_sr_p27_crew_invite1')
    V.check(t.get(field(27,1,'country'))==0,'Unresolved old popup was replaced by a new invitation')
    t.c=t.countries['DDR'];t.call('cw_sr_crew_decline_27');t.c=t.countries['SOV'];t.call('cw_sr_p27_crew_invite1')
    V.check(t.get(field(27,1,'country'))==t.country_ids['DDR'],'Dismissing an old popup did not free the invitation channel')
    t,p=setup();t.put('cw_sr_crew_candidate',t.country_ids['DDR']);t.call('cw_sr_p27_crew_invite1');t.c=t.countries['DDR'];t.c.ai=True;t.call('cw_sr_crew_accept_27')
    V.check(t.get('cw_sr_crew_status')==1,'AI accepted an outstanding crew invitation')
    t.call('cw_sr_crew_decline_27');V.check(t.get('cw_sr_crew_status')==0 and 'cw_sr_crew_invitation_open' not in t.c.flags,'AI dismissal stranded an invitation popup')
    # An unclaimed world first conserves the whole expedition's additional pool.
    t,p=setup(15);invite(t,15,1,'DDR');invite(t,15,2,'POL');t.rolls.append(0);t.call('cw_sr_p15_launch')
    initial=sum(c.variables.get('cw_sr_prestige',0) for c in t.countries.values());t.call('cw_sr_p15_success')
    milestone=next(x for x in V.DATA['milestones'] if x['capability'] in p['grants'])
    V.check(sum(c.variables.get('cw_sr_prestige',0) for c in t.countries.values())-initial==V.D(p['prestige']+milestone['prestige']),'World-first rewards were multiplied or lost')
    V.check(sorted(b[2] for b in t.countries['SOV'].tech_bonuses)==['0.12'],'Host kept full world-first research award')
    report={'project':'IMPERIA COLD WAR','status':'passed','checks':V.CHECKS,'crew_programmes':sum(eligible(p) for p in V.DATA['programmes']),'maximum_guest_countries':2,'share_per_guest':.2,'training_paid_weeks':26,'native_country_scopes':True,'in_game_tested':False}
    Path(__file__).with_name('crew_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':run()
