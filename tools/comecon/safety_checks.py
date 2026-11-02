# IMPERIA COLD WAR — COMECON authority and transaction source regressions
import re
from build import ROOT, MARK


def run(check, trees):
    effects = {k:v for k,_,v in trees['common/scripted_effects/ICW_COMECON.txt']}
    triggers = {k:v for k,_,v in trees['common/scripted_triggers/ICW_COMECON.txt']}
    ui = trees['common/scripted_guis/ICW_COMECON.txt'][0][2]
    decisions = trees['common/decisions/ICW_COMECON.txt'][0][2]
    def find(body, key):
        return [v for k,_,v in body if k == key]
    def nested(body):
        for k,o,v in body:
            yield k,o,v
            if isinstance(v,list):yield from nested(v)
    def has(body,key,value=None):
        return any(k==key and (value is None or str(v)==str(value)) for k,o,v in nested(body))
    windows={}
    for kind,op,body in trees['interface/ICW_COMECON.gui'][0][2]:
        names=find(body,'name')
        if names:windows[names[0].strip('"')]=body
    for name,op,body in ui:
        window=find(body,'window_name')[0].strip('"')
        check(window in windows,name+': native window exists')
        available={v.strip('"') for k,o,v in nested(windows[window]) if k=='name' and isinstance(v,str)}
        for lists in find(body,'dynamic_lists'):
            for key,o,value in lists:
                entry=find(value,'entry_container')[0].strip('"')
                check(entry in windows,name+': dynamic entry exists')
                available.update(v.strip('"') for k,o,v in nested(windows[entry]) if k=='name' and isinstance(v,str))
        for kind in ('effects','triggers','properties'):
            for collection in find(body,kind):
                for binding,o,value in collection:
                    target=re.sub(r'_(click_enabled|visible|click)$','',binding) if kind!='properties' else binding
                    check(target in available,name+'.'+binding+': native widget binding exists')
    check(has(triggers['cc_human_member'],'is_ai','no'),'only native human controllers can finance')
    check(has(triggers['cc_secretariat'],'cc_human_member','yes'),'presiding authority requires a human Council member')
    check(not has(triggers['cc_member_country'],'COLDWAR_SOV_is_union_republic','no') and has(triggers['cc_member_country'],'NOT'),'actual Union republics excluded from Council membership')
    check(find(triggers['cc_member_country'],'is_in_array'),'membership requires the bounded Council register')
    check(has(effects['cc_update_authority'],'SOV') and has(effects['cc_update_authority'],'cc_human_member','yes'),'human chair fallback uses actual controllers')
    check(all(has(v,'ai_will_do') and has(find(v,'ai_will_do')[0],'factor','0') for k,o,v in decisions),'all native decisions have zero AI weight')
    for s in range(1,5):
        def eff(name):return effects[f'cc_{s}_{name}']
        footer=windows[f'cc_{s}_ui_controls']
        check(has(find(footer,'size')[0],'width','640') and has(find(footer,'size')[0],'height','35') and has(find(footer,'position')[0],'y','541'),f'file {s}: footer window cannot cover programme or country-list controls')
        check(has(triggers[f'cc_{s}_ai_consent'],'always','no'),f'file {s}: no automatic AI Council vote')
        check(has(triggers[f'cc_{s}_participant'],'cc_human_member','yes'),f'file {s}: AI offers excluded from draft coverage')
        for action in ('increase_share','decrease_share','fund_remainder'):
            body=eff(action)
            check(has(body,'cc_human_member','yes') and has(body,'global.cc_'+str(s)+'_phase','0') and has(body,'cc_view_slot',str(s)),f'file {s}: own contribution action {action} requires human draft and exact file')
            writes=[v for k,o,v in nested(body) if k in ('set_variable','add_to_variable','subtract_from_variable')]
            check(not any('share' in str(v) and 'global.cc_' in str(v) and 'coverage' not in str(v) for v in writes),f'file {s}: {action} never assigns another government a share')
        check(has(eff('open_review'),'cc_'+str(s)+'_can_review','yes') and has(eff('open_review'),'global.cc_'+str(s)+'_payers'),f'file {s}: review captures the actual payers')
        check('global.cc_'+str(s)+'_signatories' in str(triggers[f'cc_{s}_voter']) and not has(eff('ratify'),'clear_array','global.cc_'+str(s)+'_signatories'),f'file {s}: review signatories stay captured throughout execution')
        check(has(triggers[f'cc_{s}_editable'],'global.cc_'+str(s)+'_phase','0'),f'file {s}: terms editable only in Draft')
        check(has(triggers[f'cc_{s}_can_ratify'],'global.cc_'+str(s)+'_phase','1'),f'file {s}: execution requires sealed Council Review')
        for action in ('approve','confirm_local'):
            check(has(eff(action),'cc_'+str(s)+'_seen_terms','yes'),f'file {s}: {action} requires explicit review receipt')
        check(has(eff('prepay'),'global.cc_'+str(s)+'_period_left','0'),f'file {s}: previously prepaid period cannot be billed twice')
        check(has(eff('guard_controllers'),'cc_human_member','yes') and has(eff('guard_controllers'),'global.cc_'+str(s)+'_valid','0'),f'file {s}: loss of human financier stops funded progress')
        check(has(eff('rebuild'),'global.cc_'+str(s)+'_phase','0'),f'file {s}: rebuilding a sealed view cannot recalculate the quote')
        for name,o,body in ui:
            if name.startswith(f'cc_{s}_') or name.startswith(f'cc_overview_{s}') or name.startswith(f'cc_terms_{s}'):
                for fx in find(body,'effects'):
                    for button,op,value in fx:
                        # A file-specific command may change presentation caches, but never another contract.
                        refs=set(re.findall(r'\b(?:global\.)?cc_([1-4])_',str(value)))
                        check(not refs-{str(s)},f'{name}.{button}: cannot route into another file')
        body=str(eff('preview_all'))
        check(f'global.cc_{s}_receivers' in body and 'cc_human_member' in body,f'file {s}: native effects include passive receivers and only human capital costs')
    view=(ROOT/'common/scripted_effects/ICW_COMECON_view.txt').read_text(encoding='utf-8')
    check(not re.search(r'(?:vote_revision|seen_revision|local_revision|treasury_change|cc_\d_share)\s*=',view),'view refreshes cannot vote, acknowledge, offer funds or debit treasury')
    # A displayable programme action must carry its literal file ID, rather than reading the current tab on execution.
    source=(ROOT/'tools/comecon/compact_ui.py').read_text(encoding='utf-8')
    check('dispatch(' not in source,'programme selectors bind commands to their original contract file')
    check(has(effects['cc_refresh_country'],'is_ai','no'),'AI passive recipients have no COMECON weekly fiscal stream')
    check(has(effects['cc_calculate_weekly_expense'],'is_ai','no'),'native fiscal consumer independently excludes AI charges')
