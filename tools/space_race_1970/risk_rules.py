# IMPERIA CW — Cold War: mission-specific safety exposure and recoverable flight incidents.
"""Gameplay shares are conditional on a failed stage, not historical accident rates.

The main departure/objective draws still determine full acceptance. A single
independent, recoverable anomaly can add time and a supplementary appropriation;
it does not add a hidden third failure draw. All exposure is frozen at departure.
"""


def profile(p):
    if p['id']=='space-commission':
        return dict(cat_l=0,cat_o=0,abort=0,anomaly=0,delay=0,cost=0,
                    hazards='Staffing shortages, procurement delays and inadequate scientific coordination.',
                    repair='The commission revised its staffing and procurement arrangements.',
                    loss='The government could not accept the proposed staffing and institutional arrangements.',
                    disaster='The institutional acceptance campaign was suspended.')
    if p.get('commissioningOnly'):
        return dict(cat_l=0, cat_o=2, abort=0, anomaly=0, delay=0, cost=0,
                    hazards='Acceptance-test failures, instrumentation defects and range safety deficiencies.',
                    repair='The acceptance authority identified an instrumentation or safety deficiency.',
                    loss='The acceptance campaign failed its engineering or safety criteria.',
                    disaster='A destructive test accident interrupted the acceptance campaign.')
    deep=p['region'] in {'mars','venus','outer','mercury','se-l1','se-l2'}
    landing=p['missionFamily'] in {'planetary-entry','mars-surface','mars-heavy-landing','mars-return'} or p['id'] in {'lunar-rover','lunar-sample-return'}
    lunar=p['missionFamily']=='crewed-cislunar'
    mars=p['missionFamily']=='crewed-interplanetary'
    cat_o=18 if mars else 12 if lunar or p['missionFamily']=='mars-return' else 10 if landing else 8 if p['crewSize'] else 5
    delay=30 if deep or p['flightMonths']>=12 else 3 if p['crewSize'] else 7
    cost=round(max(.005,p['missionCostB']*.02),5)
    if mars:
        hazards='Radiation exposure, life-support loss, heavy landing, surface ascent and Earth return.'
        repair='A thermal-control fault required redundant equipment and revised flight procedures.'
        loss='Landing, surface ascent or return propulsion failed to qualify the expedition.'
        disaster='An unrecoverable life-support, landing or return-system failure prevented crew recovery.'
    elif lunar:
        hazards='Transfer burns, navigation, docking, life support, landing or ascent, and Earth return.'
        repair='A power-system fault required load shedding and revised flight procedures.'
        loss='Transfer propulsion, rendezvous or return guidance prevented the accepted mission.'
        disaster='An unrecoverable propulsion, pressure-control or return-system failure prevented crew recovery.'
    elif p['crewSize']:
        hazards='Docking impacts, cabin pressure, life support, thermal protection and recovery.'
        repair='A cooling-system fault required backup equipment and revised operations.'
        loss='Docking or onboard-system faults forced an early end to the operating campaign.'
        disaster='An unrecoverable pressure-control or return-system failure prevented crew recovery.'
    elif landing:
        hazards='Cruise communications, entry guidance, landing engines, surface power and sample recovery.'
        repair='A communications fault required antenna recovery and revised operations.'
        loss='Entry, landing, surface operations or sample-recovery hardware failed.'
        disaster='A destructive entry, landing or propulsion failure caused the loss of the spacecraft.'
    elif deep:
        hazards='Long-coast propulsion, navigation, radiation damage, power and communications.'
        repair='An attitude-control fault required a safe-mode recovery and revised operations.'
        loss='Navigation, propulsion or long-range communications failed to support the encounter.'
        disaster='An unrecoverable propulsion or electrical failure caused the loss of the spacecraft.'
    else:
        hazards='Engine or staging failure, deployment, attitude control, electrical power and communications.'
        repair='A deployment or attitude-control fault required recovery commands and revised operations.'
        loss='Payload deployment, guidance or onboard power failed to support the operating campaign.'
        disaster='A destructive propulsion or electrical failure caused the loss of the spacecraft.'
    return dict(cat_l=14,cat_o=cat_o,abort=40,anomaly=10 if deep or p['crewSize'] else 6,
                delay=delay,cost=cost,hazards=hazards,repair=repair,loss=loss,disaster=disaster)


def odds(c,n,p):
    sv,av=(c[k] for k in ['sv','av']);v=lambda s:c['var'](n,s);r=profile(p)
    body=sv(v('risk_cat_l'),r['cat_l'])+sv(v('risk_cat_o'),r['cat_o'])
    # Risk from final stage probabilities. Catastrophic shares are conditional;
    # never present them as an additional independent chance of mission failure.
    body+=sv(v('risk_loss'),100)+f'subtract_from_variable = {{ {v("risk_loss")} = {v("lp")} }}\nmultiply_variable = {{ {v("risk_loss")} = {r["cat_l"]} }}\ndivide_variable = {{ {v("risk_loss")} = 100 }}\n'
    body+=sv('cw_sr_objective_loss',100,True)+f'subtract_from_temp_variable = {{ cw_sr_objective_loss = {v("op")} }}\nmultiply_temp_variable = {{ cw_sr_objective_loss = {v("lp")} }}\nmultiply_temp_variable = {{ cw_sr_objective_loss = {r["cat_o"]} }}\ndivide_temp_variable = {{ cw_sr_objective_loss = 10000 }}\n'+av(v('risk_loss'),'cw_sr_objective_loss')
    body+=sv(v('risk_crew'),0)
    if p['crewSize']:
        body+=sv(v('risk_crew'),v('risk_loss'))
        if p.get('crewAtLaunch') is False:body+=sv(v('risk_crew'),'cw_sr_objective_loss')
    body+=sv(v('risk_anomaly'),0)
    if not p.get('commissioningOnly'):
        body+=sv(v('risk_anomaly'),100)+f'subtract_from_variable = {{ {v("risk_anomaly")} = {v("op")} }}\nmultiply_variable = {{ {v("risk_anomaly")} = 0.5 }}\n'+av(v('risk_anomaly'),r['anomaly'])+c['clamp'](v('risk_anomaly'),2,30)
    return body+sv(v('risk_recorded'),1)


def anomaly(c,n,p):
    sv,av,cv,block_if,effect=(c[k] for k in ['sv','av','cv','block_if','effect']);v=lambda s:c['var'](n,s);r=profile(p)
    if p.get('commissioningOnly'):return ''
    # Service invoices above available cash become ordinary programme arrears.
    # They cannot mint money or silently disappear and prevent the next departure.
    body=sv(v('incident'),1)+av(v('days'),r['delay'])+av(v('delay_days'),r['delay'])+sv('cw_sr_incident_due',r['cost'],True)
    body+=sv('cw_sr_incident_payment','treasury',True)+c['clamp']('cw_sr_incident_payment',0,'cw_sr_incident_due',True)+c['charge']('cw_sr_incident_payment')+av(v('spent'),'cw_sr_incident_payment')
    body+=f'subtract_from_temp_variable = {{ cw_sr_incident_due = cw_sr_incident_payment }}\n'+av(v('arrears'),'cw_sr_incident_due')+c['bulletin'](n,14)+'cw_sr_touch = yes\n'
    return effect(f'cw_sr_p{n}_anomaly',block_if(c['guard']()+' '+cv(v('state'),'=',4)+' '+cv(v('incident'),'=',0),body))


def findings(p,kind):
    r=profile(p)
    if kind=='partial':return 'Electrical or communications degradation limited the accepted results.'
    return r['loss' if kind=='failure' else 'disaster']
