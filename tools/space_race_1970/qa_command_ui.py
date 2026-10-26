# IMPERIA CW — Cold War: exercise the replacement ledger and native command-room controls.
import hashlib
import json
import re
from pathlib import Path
import validate as V

ROOT=V.ROOT


def run():
    gui=V.first(V.first(V.ASTS['common/scripted_guis/COLDWAR_space_race_gui.txt'],'scripted_gui'),'cw_sr_main')
    callbacks=dict((k,v) for k,op,v in V.first(gui,'effects'))
    enabled=dict((k,v) for k,op,v in V.first(gui,'triggers') if k.endswith('_click_enabled'))
    window=V.first(V.first(V.ASTS['interface/COLDWAR_space_race.gui'],'guiTypes'),'containerWindowType')
    surface=next(v for k,op,v in window if k=='iconType' and V.first(v,'name')=='"cw_sr_input_surface"')
    V.check(V.first(surface,'alwaysTransparent')=='no' and V.first(window,'click_to_front')=='yes','Floating window passes empty-space input through to the game')
    def click(m,name):
        if name+'_click_enabled' in enabled:
            V.check(m.test(enabled[name+'_click_enabled']),'Disabled control clicked by test '+name)
        m.run(callbacks[name+'_click'])
    # Verify the complete legacy donor pair, all adjacent ledger positions and every old GUI.
    shared=V.parse((ROOT/'common/scripted_guis/00_missiles_scripted_guis.txt').read_text(encoding='utf-8'))
    old=V.first(V.first(shared,'scripted_gui'),'MD_missiles_gui')
    open_callback=V.first(V.first(old,'effects'),'antarctica_gui_ledger_button_click')
    V.check(any(k=='cw_sr_open_from_ledger' for k,op,v in V.walk(open_callback)),'Old ledger does not open Space Race')
    for name,op,body in V.first(shared,'scripted_gui'):
        if 'antarctica' in name:
            V.check(V.first(V.first(body,'visible',[]),'always')=='no','Legacy Antarctic GUI still reachable: '+name)
    ui=V.first(V.parse((ROOT/'interface/MD_countrymissilesview.gui').read_text(encoding='utf-8')),'guiTypes')
    parent=next(v for k,op,v in ui if k=='containerWindowType' and V.first(v,'name')=='"MD_countrymissilesview"')
    ledger=next(v for k,op,v in parent if k=='containerWindowType' and V.first(v,'name')=='"missiles_gui_ledger_menu"')
    pairs={V.first(v,'name').strip('"'):v for k,op,v in ledger if k in ['buttonType','iconType']}
    for i,name in enumerate(['space','ct','pmc','un','cyber','antarctica']):
        widget=pairs[name+'_gui_ledger_button'];pos=V.first(widget,'position')
        V.check(int(V.first(pos,'x'))==i*84,'Adjacent ledger moved: '+name)
    V.check(V.first(pairs['antarctica_gui_ledger_button'],'pdx_tooltip')=='"cw_sr_ledger_tt"','Antarctic tooltip retained')
    icon=pairs['icon_antarctica_gui_ledger']
    V.check(V.first(icon,'spriteType')=='"GFX_cw_sr_ledger_orbit"','Old Antarctic icon retained')
    V.check(V.first(V.first(icon,'position'),'x')=='452','Replacement icon moved outside donor slot')
    hooks=V.parse((ROOT/'common/on_actions/MD_antarctica_on_actions.txt').read_text(encoding='utf-8'))
    V.check(V.first(hooks,'on_actions')==[],'Antarctic startup or tick hooks still active')
    category=V.parse((ROOT/'common/decisions/categories/00_antarctica_categories.txt').read_text(encoding='utf-8'))
    V.check(V.first(V.first(category[0][2],'allowed'),'always')=='no','Antarctic decision remains available')
    # Existing saves lose Antarctic costs and modifiers; annual allocation is converted once.
    m=V.Machine(('SAU','USA'));m.c.flags.update(['antarctica_has_active_station','auto_resupply_antarctica_station']);m.c.dynamic_modifiers.add('antarctica_laboratory_dynamic_modifier');m.c.ideas.add('at_member');m.put('antarctica_station_total_upkeep_multiplier',20)
    m.call('cw_sr_retire_antarctica')
    V.check('antarctica_has_active_station' not in m.c.flags and not m.c.dynamic_modifiers and 'at_member' not in m.c.ideas,'Legacy benefits survived retirement')
    V.check(m.get('antarctica_station_total_upkeep_multiplier')==0,'Legacy running cost survived retirement')
    m.c.dynamic_modifiers.add('antarctica_laboratory_dynamic_modifier');m.call('cw_sr_retire_antarctica')
    V.check(not m.c.dynamic_modifiers,'Already-retired save kept its laboratory modifier')
    m.c.flags.add('cw_sr_initialized');m.put('cw_sr_budget',52);m.call('cw_sr_migrate_weekly');m.call('cw_sr_migrate_weekly')
    V.check(m.get('cw_sr_budget')==1,'Annual budget was not converted exactly once')
    m=V.Machine(('SOV','USA'));m.init();m.c.flags.add('open_MD_countrymissilesview');m.put('var_open_MD_antarctica_gui',2);m.run(open_callback)
    V.check('cw_sr_open' in m.c.flags and 'open_MD_countrymissilesview' not in m.c.flags,'Replacement did not switch windows')
    V.check(m.get('var_open_MD_antarctica_gui')==0 and m.g.get('md_ui_updates',0)>0,'Legacy selector or dirty cache was retained')
    # Every tab is a real routed view; catalogue pages cover all 84 programmes exactly once.
    for tab in range(1,8):click(m,'cw_sr_tab_'+str(tab));V.check(m.get('cw_sr_tab')==tab,'Tab not routed')
    click(m,'cw_sr_tab_3');seen=[]
    for page in range(7):
        if page:click(m,'cw_sr_list_next')
        seen.extend(int(m.get('cw_sr_slot_'+str(i))) for i in range(12) if m.get('cw_sr_slot_'+str(i))>0)
    V.check(seen==list(range(1,85)),'Catalogue skips, duplicates or misorders a programme')
    V.check(not m.test(enabled['cw_sr_list_next_click_enabled']),'Catalogue permits an empty eighth page')
    click(m,'cw_sr_tab_3');click(m,'cw_sr_filter_region')
    V.check(m.get('cw_sr_list_count')==19,'Ground filter count is wrong')
    packed=[m.get('cw_sr_slot_'+str(i)) for i in range(12)]
    V.check(all(packed),'Filtered catalogue has gaps')
    click(m,'cw_sr_filter_kind')
    V.check(m.get('cw_sr_list_count')==sum(p['region']=='ground' and p['kind']=='historical' for p in V.DATA['programmes']),'Historical-status filter is wrong')
    click(m,'cw_sr_tab_2');click(m,'cw_sr_brief_programmes')
    expected=[i for i,p in enumerate(V.DATA['programmes'],1) if p.get('entryProgramme') or 'SOV' in p.get('owners',[]) or 'SOV' in p.get('initialProgress',{})]
    V.check(m.get('cw_sr_list_count')==len(expected),'National programme filter is wrong')
    click(m,'cw_sr_filter_national');V.check(m.get('cw_sr_list_count')==84,'National filter did not clear')
    click(m,'cw_sr_filter_ready')
    expected=sum(m.test(V.parse(f'cw_sr_p{n}_start_allowed = yes')) or m.test(V.parse(f'cw_sr_p{n}_launch_allowed = yes')) for n in range(1,85))
    V.check(m.get('cw_sr_list_count')==expected and expected>0,'Ready filter includes locked programmes or hides available programmes')
    click(m,'cw_sr_filter_ready');V.check(m.get('cw_sr_list_count')==84,'Ready filter did not restore catalogue')
    click(m,'cw_sr_slot_0_wide');V.check(m.get('cw_sr_tab')==1 and m.get('cw_sr_selected')>0,'Catalogue selection did not open its mission card')
    before=m.get('treasury');chance=m.get('cw_sr_view_full');click(m,'cw_sr_policy_cycle')
    V.check('cw_sr_policy_open' in m.c.flags,'Policy choices did not open')
    click(m,'cw_sr_policy_option_1')
    V.check(m.get('treasury')==before and m.get('cw_sr_view_full')==chance,'Policy selection charged or qualified engineering in advance')
    V.check(m.get('cw_sr_view_policy')==1 and 'cw_sr_policy_open' not in m.c.flags,'Policy was not selected or popup remained open')
    for size in [11,12,13,14,15,16,17,19,21,23,24,28,29]:
        source=(ROOT/f'gfx/fonts/COLDWAR_space_race/cw_sr_ui_{size}.fnt').read_text(encoding='utf-8')
        for control in [0,8,10,13,29,31,65279]:
            glyph=next(line for line in source.splitlines() if line.startswith(f'char id={control} '))
            V.check('width=0 height=0' in glyph and 'xadvance=0 ' in glyph,'Control character renders a visible box')
    from illustrations import category
    V.check(set(map(category,V.DATA['programmes']))=={'ground','rocket','satellite','station','probe','crew','lander'},'Programme artwork classes are incomplete')
    click(m,'cw_sr_requirements');V.check('cw_sr_requirements_open' in m.c.flags,'Requirements did not expand')
    V.check(m.get('cw_sr_details_mode')==0,'Requirements button does not open mission eligibility')
    click(m,'cw_sr_requirements_close');V.check('cw_sr_requirements_open' not in m.c.flags,'Requirements did not close')
    click(m,'cw_sr_active_effects');V.check('cw_sr_requirements_open' in m.c.flags and m.get('cw_sr_details_mode')==1,'Active effects header button does not open national modifiers')
    click(m,'cw_sr_readiness_mode');V.check(m.get('cw_sr_details_mode')==0,'Readiness overlay tab does not switch')
    click(m,'cw_sr_requirements_close')
    m.put('cw_sr_p10_state',1);m.put('cw_sr_p13_state',4);click(m,'cw_sr_tab_4')
    V.check(m.get('cw_sr_list_count')==1 and m.get('cw_sr_slot_0')==10,'Funding view does not show active engineering')
    click(m,'cw_sr_tab_5');V.check(m.get('cw_sr_list_count')==1 and m.get('cw_sr_slot_0')==13,'Manifest does not show the flight')
    # Re-reading a genuine bulletin cannot roll another mission or grant rewards.
    m=V.Machine(('SAU',));m.init();m.c.flags.add('cw_sr_open');m.call('cw_sr_p27_success');m.put('cw_sr_selected',27);click(m,'cw_sr_tab_7')
    V.check(m.get('cw_sr_view_picture')==6,'Saudi lunar bulletin chose the wrong image')
    before=(m.get('treasury'),m.get('cw_sr_prestige'),m.get('cw_sr_science'),m.c.pp,len(m.c.tech_bonuses),len(m.rolls))
    click(m,'cw_sr_news_read')
    after=(m.get('treasury'),m.get('cw_sr_prestige'),m.get('cw_sr_science'),m.c.pp,len(m.c.tech_bonuses),len(m.rolls))
    V.check(before==after,'Re-reading a bulletin changed money, rewards or mission randomness')
    V.check(m.events[-1][1]=='cw_sr_report.8003','Saudi bulletin replay used the wrong event')
    m.c.ai=True;before=dict(m.c.variables);m.run(open_callback);m.run(callbacks['cw_sr_primary_click'])
    V.check(m.c.variables==before,'AI accessed Space Race through the old ledger or new controls')
    # Weekly runtime hooks and five-place literal cap are repository requirements.
    hooks=V.first(V.ASTS['common/on_actions/COLDWAR_space_race_on_actions.txt'],'on_actions')
    V.check(V.first(hooks,'on_weekly') is not None and V.first(hooks,'on_monthly') is None,'Recurring finance still uses monthly ticks')
    for file,body in V.ASTS.items():
        source=(ROOT/file).read_text(encoding='utf-8')
        V.check(not re.search(r'(?<![\w.])[-+]?\d+\.\d{6,}(?![\w.])',source),'Overlong numeric literal: '+file)
    result={'checks':V.CHECKS,'status':'passed','legacy_antarctica':'startup/ticks/AI, windows and decision retired; modifiers/costs cleaned','ledger':'complete donor button/icon pair and adjacent slot positions checked','tabs':7,'catalogue_programmes':84,'finance':'weekly; one-time existing-save budget conversion','bulletin_replay':'no finance, reward or RNG mutation','in_game_tested':False}
    (Path(__file__).with_name('command_ui_validation.json')).write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8');print(json.dumps(result))


if __name__=='__main__':run()
