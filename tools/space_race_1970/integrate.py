# IMPERIA CW — Cold War: retire the Antarctic subsystem and reuse its ledger slot.
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
MARK='# IMPERIA CW — Cold War: Space Race replaces Antarctica.'


def span(source,name,start=0):
    match=re.search(r'(?m)^\s*'+re.escape(name)+r'\s*=\s*\{',source[start:])
    assert match,'Missing block '+name
    begin=start+match.start();brace=source.index('{',start+match.start());depth=1;quoted=False;comment=False;i=brace+1
    while depth:
        ch=source[i]
        if ch=='\n':comment=False
        elif not quoted and ch=='#':comment=True
        elif not comment and ch=='"' and source[i-1]!='\\':quoted=not quoted
        elif not quoted and not comment:
            if ch=='{':depth+=1
            elif ch=='}':depth-=1
        i+=1
    return begin,i,brace


def save(relative,source):
    path=ROOT/relative
    if path.read_text(encoding='utf-8-sig')==source:return
    temporary=path.with_suffix(path.suffix+'.cw_sr_tmp')
    temporary.write_text(source,encoding='utf-8',newline='\n')
    temporary.replace(path)


def apply():
    changed=[]
    relative='common/scripted_guis/00_missiles_scripted_guis.txt';source=(ROOT/relative).read_text(encoding='utf-8-sig')
    begin,end,brace=span(source,'antarctica_gui_ledger_button_click')
    replacement='\n\t\t\t'+MARK+'\n\t\t\tantarctica_gui_ledger_button_click = {\n\t\t\t\tif = { limit = { is_ai = no IMP_is_1970_scenario = yes }\n\t\t\t\t\tcw_sr_open_from_ledger = yes\n\t\t\t\t}\n\t\t\t}'
    # Replace the complete callback, including its old variable writes and refresh calls.
    if 'cw_sr_open_from_ledger = yes' not in source[begin:end]:source=source[:begin]+replacement+source[end:]
    for callback in ['missiles_button_click','space_gui_ledger_button_click','ct_gui_ledger_button_click','pmc_gui_ledger_button_click','un_gui_ledger_button_click','cyber_gui_ledger_button_click']:
        begin,end,brace=span(source,callback)
        if 'clr_country_flag = cw_sr_open' not in source[begin:end]:source=source[:brace+1]+'\n\t\t\t\t'+MARK+'\n\t\t\t\tclr_country_flag = cw_sr_open\n'+source[brace+1:]
        begin,end,brace=span(source,callback)
        block=source[begin:end]
        if 'cw_sr_touch = yes' not in block:source=source[:begin]+block.replace('clr_country_flag = cw_sr_open','clr_country_flag = cw_sr_open\n\t\t\t\tcw_sr_touch = yes',1)+source[end:]
    begin,end,brace=span(source,'MD_missiles_gui');main=source[begin:end]
    if 'antarctica_gui_ledger_button_click_enabled' not in main:
        b,e,o=span(main,'triggers');main=main[:o+1]+'\n\t\t\t'+MARK+'\n\t\t\tantarctica_gui_ledger_button_click_enabled = { is_ai = no IMP_is_1970_scenario = yes }\n'+main[o+1:];source=source[:begin]+main+source[end:]
    for name in re.findall(r'(?m)^\t([\w]+antarctica[\w]*|MD_antarctica[\w]*)\s*=\s*\{',source):
        begin,end,brace=span(source,name)
        block=source[begin:end]
        if 'visible = {' not in block:continue
        b,e,o=span(block,'visible')
        if 'always = no' not in block[b:e]:
            block=block[:b]+'\n\t\t'+MARK+'\n\t\tvisible = { always = no }'+block[e:]
            source=source[:begin]+block+source[end:]
    save(relative,source);changed.append(relative)
    relative='interface/MD_countrymissilesview.gui';source=(ROOT/relative).read_text(encoding='utf-8-sig')
    # Audit and patch the entire adjacent button/icon pair without moving the other ledgers.
    m=re.search(r'buttonType\s*=\s*\{\s*name = "antarctica_gui_ledger_button".*?\n\s*\}',source,re.S);assert m
    pair=m[0].replace('"ANTARCTICA_GUI_LEDGER_TT"','"cw_sr_ledger_tt"').replace('"ANTARCTICA_GUI_LEDGER_TT_DELAYED"','"cw_sr_ledger_delayed"')
    if MARK not in source[max(0,m.start()-100):m.start()]:pair=MARK+'\n\t\t\t'+pair
    source=source[:m.start()]+pair+source[m.end():]
    m=re.search(r'iconType\s*=\s*\{\s*name ="icon_antarctica_gui_ledger".*?\n\s*\}',source,re.S);assert m
    pair=m[0].replace('GFX_ledger_icon_small_antarctica','GFX_cw_sr_ledger_orbit')
    if MARK not in source[max(0,m.start()-100):m.start()]:pair=MARK+'\n\t\t\t'+pair
    source=source[:m.start()]+pair+source[m.end():];save(relative,source);changed.append(relative)
    relative='common/on_actions/MD_antarctica_on_actions.txt';path=ROOT/relative;source=path.read_text(encoding='utf-8-sig')
    archive=ROOT/'tools/space_race_1970/legacy_antarctica_on_actions.txt'
    if MARK not in source:
        archive.write_text(MARK+'\n# Archived reference; this file is not loaded by HOI4.\n'+source,encoding='utf-8',newline='\n')
        save(relative,MARK+'\n# Legacy startup, daily, weekly, monthly and AI station processing are retired.\n# Original module retained under tools/space_race_1970 for reference.\non_actions = { }\n')
    changed.append(relative)
    relative='common/decisions/categories/00_antarctica_categories.txt';source=(ROOT/relative).read_text(encoding='utf-8-sig')
    source=source.replace('allowed = { always = yes }',MARK+'\n\tallowed = { always = no }')
    save(relative,source);changed.append(relative)
    relative='common/scripted_localisation/01_international_scripted_localisation.txt';source=(ROOT/relative).read_text(encoding='utf-8-sig')
    source=source.replace('localization_key = IS_title_antarctica',MARK+'\n\t\tlocalization_key = cw_sr_ledger_name')
    save(relative,source);changed.append(relative)
    return changed


if __name__=='__main__':
    print('\n'.join(apply()))
