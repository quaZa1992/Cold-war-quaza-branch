# IMPERIA COLD WAR — Palestinian settlement-pressure regression checks.
"""Bounded tests of actual emitted AST through validate_presence.World.

No generators run. Unknown executed operations/variables still fail. Preview
arithmetic is evaluated only on throwaway copies; its wrapper is independently
checked for providers and runtime mutations. This does not emulate native HOI4.
"""
from pathlib import Path
import copy
import hashlib
import json

import validate_presence as native_model
from validate_presence import World, child, scalar, walk, snapshot
from script_format import read

ROOT=Path(__file__).resolve().parents[2]
DATA=native_model.DATA
EFFECTS=native_model.EFFECTS
DYNAMIC=native_model.DYNAMIC
TRIGGERS=native_model.TRIGGERS
RESPONSES=native_model.RESPONSES
EVENTS=native_model.EVENTS
META=DATA['palestinian_pressure']
HELPER=EFFECTS[META['reconcile_effect']]
ROWS={p['state']:p for p in META['states']}
CONTRACTS={p['state']:p for p in DATA['settlement_presence']['contracts']}
EXPECTED={'stability_factor':-.02,'political_power_factor':-.025,'offices_productivity':-.04,
          'bureaucracy_cost_multiplier_modifier':.04,'social_cost_multiplier_modifier':.03}
SOURCES=native_model.SOURCES+['common/decisions/ISR70_policy_decisions.txt',
                             'tools/israel_1970/palestinian_pressure.py']
CHECKS=[];ERRORS=[]


def check(ok,label):
    CHECKS.append(label)
    if not ok:ERRORS.append(label)


def level(w,state):
    return w.countries['ISR']['vars'][ROWS[state]['level_variable']]


def reconcile(w):w.execute(HELPER)


def verify_values(w,state,expected,label):
    record=ROWS[state];pal=w.countries['PAL']
    check(level(w,state)==expected,label+': computed territorial level')
    check(pal['vars'][record['applied_variable']]==expected,label+': PAL applied-level receipt')
    for key,amount in EXPECTED.items():
        variable=record['modifier_variables'][key]
        actual=pal['vars'].get(variable,0)
        check(abs(actual-amount*expected)<1e-9,label+': exact '+key)
    check(w.enabled('PAL',record['modifier'])==(expected>0),label+': live modifier enable')


def delivered(state,receipt):
    w=World();w.countries['ISR']['flags'].add(receipt);reconcile(w);return w


def foreign(state,host='PAL',fund=True):
    c=CONTRACTS[state];w=World();w.states[state]['owner']=host;w.states[state]['controller']=host
    if fund:w.execute(EFFECTS[c['offer']])
    return w


def pressure_displays(block,state,direct=False):
    def displayed_terms(block):
        # The generic decision compiler can place a pure effect_tooltip inside
        # another effect_tooltip beside hidden execution. Select its innermost
        # visible payload, without confusing hidden transaction code with rows.
        for k,o,v in block:
            if k in ('effect_tooltip','hidden_effect'):continue
            yield k,o,v
            if isinstance(v,list):yield from displayed_terms(v)
    candidates=[]
    for key,op,value in block if direct else walk(block):
        if key=='effect_tooltip' and isinstance(value,list):
            names=[name for command,o,payload in displayed_terms(value) if command=='add_to_variable'
                   for name,_,v in payload if name.startswith(f'ISR70_display_pal_row_{state}_')]
            if names:candidates.append(value)
            elif direct:candidates.extend(pressure_displays(value,state,direct=True))
    return candidates


def verify_display(display,state,current,planned,label,pal_exists=True,context='ISR',selected=None):
    forbidden={'modify_treasury_effect','modify_debt_effect','add_ideas','add_dynamic_modifier',
               'remove_dynamic_modifier','set_country_flag','clr_country_flag','add_building_construction',
               'add_extra_state_shared_building_slots','transfer_state','set_state_controller','add_manpower'}
    terms=list(walk(display))
    check(not any(k in forbidden or k in EFFECTS for k,o,v in terms),label+': no runtime providers or grants')
    w=World();w.countries['PAL']['exists']=pal_exists;w.countries['ISR']['focuses'].clear()
    if selected is not None:w.countries['ISR']['flags'].add('ISR70_policy_target_'+str(selected))
    if current is not None:w.countries['ISR']['vars'][ROWS[state]['level_variable']]=current
    original=snapshot(w);w.execute([('effect_tooltip','=',display)],[context])
    check(snapshot(w)==original,label+': native display wrapper has no model runtime mutations')
    # Execute only the display arithmetic on a disposable world to observe all
    # actual native formatter values, without treating them as real effects.
    preview=copy.deepcopy(w)
    # The foreign display also has existing state-scoped dummy rows. Empty
    # state variable stores support those native rows without defaulting any
    # unknown read to zero; World.number remains strict.
    for state_object in preview.states.values():state_object.setdefault('vars',{})
    preview.execute(display,[context])
    for key,amount in EXPECTED.items():
        target=f'ISR70_display_pal_row_{state}_{key}'
        found=[country['vars'][target] for country in preview.countries.values() if target in country['vars']]
        check(len(found)==1 and abs(found[0]-amount*planned)<1e-9,label+': visible '+key)


def main():
    check(set(ROWS)=={208,209} and META['max_total_level']==4,'Only West Bank and Gaza, capped at four combined levels')
    check(META['per_level_modifiers']==EXPECTED,'Exact five approved per-level modifiers')
    for state,record in ROWS.items():
        registered=DYNAMIC[record['modifier']]
        check({key:scalar(registered,key) for key in EXPECTED}==record['modifier_variables'],
              str(state)+': native dynamic definition consumes the five real PAL variables')
        check(not any('workforce' in key or 'population' in key for key,op,v in walk(registered)),
              str(state)+': no population or workforce penalty')
        baseline=World();before_balances=baseline.balances();reconcile(baseline)
        verify_values(baseline,state,0,str(state)+' no delivered sites')
        check(baseline.balances()==before_balances,str(state)+': pressure reconciliation never transfers treasury')
        reserved=World();receipt=record['basic_receipts'][0]
        reserved.countries['ISR']['flags'].add(receipt.removesuffix('_done')+'_active')
        reserved.countries['ISR']['vars'][receipt.removesuffix('_done')+'_paid']=1.5
        reconcile(reserved);verify_values(reserved,state,0,str(state)+' reserved but undelivered project')
        for receipt in record['basic_receipts']:
            verify_values(delivered(state,receipt),state,1,receipt)
        for receipt in record['extensive_receipts']:
            verify_values(delivered(state,receipt),state,2,receipt)
        w=delivered(state,record['extensive_receipts'][0])
        for receipt in record['basic_receipts']:w.countries['ISR']['flags'].add(receipt)
        reconcile(w);verify_values(w,state,2,str(state)+' extensive network plus new small farm')
        pal=copy.deepcopy(w.countries['PAL']);reconcile(w)
        check(w.countries['PAL']==pal,str(state)+': unchanged daily reconciliation neither multiplies costs nor dirties PAL again')
        w.countries['ISR']['flags'].add('ISR70_policy_target_'+str(state))
        w.countries['ISR']['flags'].add('ISR70_policy_fund_settlement_compensation_done')
        reconcile(w);verify_values(w,state,1,str(state)+' funded compensation reduces extensive tier')
        w=delivered(state,record['extensive_receipts'][0]);w.countries['ISR']['flags'].add('ISR70_policy_fund_settlement_compensation_done')
        reconcile(w);verify_values(w,state,2,str(state)+' compensation without matching project target')
        w.countries['ISR']['flags'].add('ISR70_policy_target_'+str(state));w.countries['ISR']['flags'].discard('ISR70_policy_fund_settlement_compensation_done')
        w.countries['ISR']['flags'].add('ISR70_policy_binding_settlement_ceiling')
        reconcile(w);verify_values(w,state,2,str(state)+' unfunded ceiling does not substitute for compensation')

        for loss in ('control','claim','pal_absent','israel_absent'):
            w=delivered(state,record['extensive_receipts'][0])
            if loss=='control':w.states[state]['controller']='PAL'
            if loss=='claim':w.states[state]['owner']='USA';w.states[state]['cores'].discard('PAL')
            if loss=='pal_absent':w.countries['PAL']['exists']=False
            if loss=='israel_absent':w.countries['ISR']['exists']=False
            check(not w.enabled('PAL',record['modifier']),str(state)+': '+loss+' immediately disables effects')
            reconcile(w);check(level(w,state)==0,str(state)+': '+loss+' computes zero pressure')
            w.states[state]['controller']='ISR';w.states[state]['owner']='PAL';w.states[state]['cores'].add('PAL')
            w.countries['PAL']['exists']=True;w.countries['ISR']['exists']=True
            reconcile(w);verify_values(w,state,2,str(state)+' '+loss+' restoration')
        for retained_claim in ('owner','core'):
            w=delivered(state,record['basic_receipts'][0])
            if retained_claim=='owner':w.states[state]['cores'].discard('PAL')
            else:w.states[state]['owner']='USA'
            reconcile(w);verify_values(w,state,1,str(state)+' Palestinian '+retained_claim+' alone retains the claim')

        c=CONTRACTS[state]
        w=foreign(state,fund=False);w.countries['ISR']['flags'].add(c['pending']);reconcile(w)
        verify_values(w,state,0,str(state)+' legacy pending flag without funding')
        for partial in (c['active'],c['paid']):
            w=World();w.countries['ISR']['flags'].add(partial);reconcile(w)
            verify_values(w,state,0,str(state)+' only one funded-presence receipt: '+partial)
        check(set(record['funded_presence_receipts'])=={c['active'],c['paid']},str(state)+': metadata requires both active and paid receipts')
        w=foreign(state,fund=False);w.countries['ISR']['vars']['treasury']=0;w.execute(EFFECTS[c['offer']]);reconcile(w)
        verify_values(w,state,0,str(state)+' unfunded unilateral establishment')
        w=foreign(state)
        verify_values(w,state,1,str(state)+' funded unilateral establishment reconciles immediately')
        w.states[state]['controller']='ISR';w.execute(EFFECTS['ISR70_policy_reconcile_presence'])
        verify_values(w,state,1,str(state)+' funded foothold retains Palestinian pressure under Israeli control')
        check(not w.enabled('ISR',c['israel_modifier']),str(state)+': taking military control suspends foreign commercial benefits separately')
        w.countries['ISR']['flags'].add(record['extensive_receipts'][0]);reconcile(w)
        verify_values(w,state,2,str(state)+' extensive physical development upgrades a funded foothold')
        w=foreign(state);w.execute(EFFECTS[c['cancel']]);reconcile(w)
        verify_values(w,state,0,str(state)+' ending Israeli funding without physical sites ends pressure')
        w=foreign(state);w.states[state]['controller']='USA';w.execute(EFFECTS['ISR70_policy_reconcile_presence'])
        verify_values(w,state,1,str(state)+' controller change does not erase funded Palestinian land pressure')
        w=foreign(state,host='USA',fund=False);w.countries['PAL']['exists']=False;w.execute(EFFECTS[c['offer']]);reconcile(w)
        check(level(w,state)==0 and not w.enabled('PAL',record['modifier']),str(state)+': unilateral third-country foothold never penalises absent Palestine')

        # The actual Israeli focus and re-establishment decision show all terms
        # before eligibility and execution, without any recipient response.
        focus=EFFECTS['ISR70_policy_complete_'+c['focus'].removeprefix('ISR70_')]
        decisions=child(read((ROOT/'common/decisions/ISR70_policy_decisions.txt').read_text(encoding='utf-8')),'ISR70_policy_category')
        renew=child(child(decisions,f'ISR70_policy_decision_renew_presence_{state}'),'complete_effect')
        for location,block in [('locked unilateral focus',focus),('Israeli re-establishment decision',renew)]:
            previews=pressure_displays(block,state,direct=True)
            check(bool(previews),str(state)+': '+location+' has unconditional numeric Palestinian terms')
            for preview in previews:
                verify_display(preview,state,None,1,str(state)+' '+location+' absent PAL',False)
                verify_display(preview,state,2,1,str(state)+' '+location+' prospective foreign tier remains one')

    # Both extensive routes together are the maximum. These are modifier deltas,
    # not immediate stability/population edits or an arbitrary daily penalty.
    w=World()
    for record in ROWS.values():w.countries['ISR']['flags'].update(record['extensive_receipts'])
    reconcile(w)
    check(sum(level(w,s) for s in ROWS)==4,'Compatible extensive West Bank plus Gaza totals exactly four levels')
    for key,amount in EXPECTED.items():
        total=sum(w.countries['PAL']['vars'][record['modifier_variables'][key]] for record in ROWS.values())
        check(abs(total-4*amount)<1e-9,'Maximum compatible total is exact for '+key)
    w=World();w.countries['ISR']['flags'].update(('ISR70_policy_project_controlled_sinai_done','ISR70_policy_project_controlled_golan_done'))
    for state in (213,587):
        c=CONTRACTS[state];host='EGY' if state==213 else 'SYR';w.states[state]['controller']=host
        w.execute(EFFECTS[c['offer']])
    reconcile(w)
    check(all(level(w,s)==0 for s in ROWS),'Sinai and Golan sites or unilateral footholds alone create no Palestinian pressure')

    for project in DATA['policy_expansion']['projects']:
        if project['states'] not in ([208],[209]):continue
        state=project['states'][0];previews=pressure_displays(read(project['preview_code']),state)
        if project['key'].startswith(('designated_sites','settlement_services','settlement_ceiling',
                'settlement_package','entrench_network','settlement_extension','controlled_')):
            check(bool(previews),project['key']+': promised project preview contains Palestinian modifier rows')
        if not previews:continue
        tier=2 if project['key'].startswith(('settlement_package','entrench_network','settlement_extension')) else 1
        for preview in previews:
            verify_display(preview,state,None,tier,project['key']+' prospective tier')
            verify_display(preview,state,2,2,project['key']+' retains stronger existing tier')

    for state,record in ROWS.items():
        for title,source in [('compensation focus',EFFECTS['ISR70_policy_complete_settlement_compensation']),
                             ('acceptance event',child(EVENTS['ISR70P.403'],'option'))]:
            previews=pressure_displays(source,state,direct=True)
            check(bool(previews),str(state)+': '+title+' displays funded reduced Palestinian burden')
            for preview in previews:verify_display(preview,state,2,1,str(state)+' '+title+' fixed compensated tier',
                context='PAL' if title=='acceptance event' else 'ISR',selected=state)
        decisions=child(read((ROOT/'common/decisions/ISR70_policy_decisions.txt').read_text(encoding='utf-8')),'ISR70_policy_category')
        funded=child(decisions,'ISR70_policy_decision_fund_settlement_compensation')
        check(funded is not None,'Funded compensation decision is present')
        if funded:
            previews=pressure_displays(child(funded,'complete_effect'),state,direct=True)
            check(bool(previews),str(state)+': paid compensation decision displays reduced Palestinian burden')
            for preview in previews:verify_display(preview,state,2,1,str(state)+' compensation funding fixed tier',selected=state)


if __name__=='__main__':
    try:main()
    except Exception as exc:ERRORS.append(type(exc).__name__+': '+str(exc))
    report=dict(project='IMPERIA COLD WAR',status='FAIL' if ERRORS else 'PASS',checks=len(CHECKS),errors=ERRORS,
        passed=[c for c in CHECKS if c not in ERRORS],source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES},
        method='Actual emitted AST evaluated through strict multi-country validate_presence.World; isolated prospective arithmetic and native-variable wiring checks.',
        limitations=['No native HOI4 execution, save, multiplayer or UI tooltip verification.',
            'Native scopes, dynamic enable and money providers use the explicitly bounded adapters of validate_presence.World.',
            'Prospective effect_tooltip payload arithmetic is inspected on disposable fixtures; the real wrapper is verified inert in the model.'],runtime_test=False)
    (ROOT/'docs/israel_1970_design/palestinian_pressure_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('passed','source_sha256')},indent=2));raise SystemExit(bool(ERRORS))
