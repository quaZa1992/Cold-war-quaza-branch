# IMPERIA COLD WAR — Targeted dossier source, integration and UI validation
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
from integrations import strip as strip_observers
from treaty_integrations import strip as strip_treaties
strip = lambda source: strip_observers(strip_treaties(source))
from runtime import COLS

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/spain_1970_v2'))
spec=importlib.util.spec_from_file_location('icw_audit_parser',ROOT/'tools/multiplayer_quality/audit.py')
parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser)


def main():
    manifest=json.loads((HERE/'generated.json').read_text())
    checks=[]
    def check(condition,label):
        if not condition:raise AssertionError(label)
        checks.append(label)
    asts={}
    for rel in manifest['generated']+manifest['integrations']:
        p=ROOT/rel;raw=p.read_bytes();source=raw.decode('utf-8-sig')
        if p.suffix=='.yml':
            check(raw.startswith(b'\xef\xbb\xbf') and source.startswith('l_english:\n# IMPERIA COLD WAR'),rel+' localisation header and BOM')
            check(not any(c in source for c in ['\u2013','\u2014'] if c!='\u2014') and not any(c in source.split('\n',2)[2] for c in ['\u2013','\u2014']),rel+' English ASCII punctuation')
        else:
            check(not raw.startswith(b'\xef\xbb\xbf') and source.startswith('# IMPERIA COLD WAR'),rel+' marker and UTF-8 without BOM')
            if p.parent.name=='synchronized_dynamic_tokens':
                tokens=[s.strip() for s in source.splitlines() if s.strip() and not s.lstrip().startswith('#')]
                check(all(re.fullmatch(r'\w+',s) for s in tokens) and len(set(tokens))==len(tokens),rel+' stable native token catalogue')
            else:
                asts[rel]=parser.parse(source)
                checks.append(rel+' parsed')
    runtime=(ROOT/'common/scripted_effects/ICW_superpower_dossier.txt').read_text()
    from treaties import EQUIPMENT
    tokens=(ROOT/'common/synchronized_dynamic_tokens/ICW_superpower_treaties.txt').read_text()
    check(set(EQUIPMENT)==set(s for s in tokens.splitlines() if s and not s.startswith('#')),'All treaty equipment query tokens have stable synchronized identifiers')
    forbidden=['modify_treasury_effect','add_ideas','add_equipment_to_stockpile','send_equipment','add_to_variable = { treasury','subtract_from_variable = { treasury','add_political_power','mdcw_cw_add_tension','random_list','random_country','every_state','every_owned_state']
    check(not any(x in runtime for x in forbidden),'Observer/navigation effects cannot execute gameplay transactions or random discovery')
    hooks=(ROOT/'common/on_actions/ICW_superpower_dossier.txt').read_text()
    check('on_daily' not in hooks and hooks.count('on_weekly')==1 and 'global.icsd_weekly_date = global.num_days' in hooks,'One weekly country anchor and native global day guard')
    check('every_owned_state' not in runtime and 'every_country_division' not in runtime and runtime.count('every_country =')==1,'One bounded country discovery pass, no state or unit sweeps')
    check('icsd_mail_kind^num > 23' in runtime,'Each observer correspondence ring bounded to 24')
    check('global.global.' not in runtime and 'global.global.' not in (ROOT/'common/scripted_triggers/ICW_superpower_dossier.txt').read_text(),'Scratch values have exactly one explicit global scope')
    check('for_loop_effect = { start = 0 end = 15' in runtime and 'array = mdcw_cw_out' in runtime,'Only 15 native investment slots and existing assistance links are inspected')
    check('global.icsd_version = 2' in runtime and 'icsd_migrate_legacy' in runtime,'Legacy save migration has an idempotent schema guard')
    native_triggers=(ROOT/'common/scripted_triggers/ICW_superpower_dossier.txt').read_text()
    check('civilian_intel > 0.59999' in native_triggers and 'value > 49.999' in native_triggers,'Native civilian intelligence and recipient network thresholds')
    check('is_local_player' not in runtime+native_triggers and 'is_ai' not in runtime,'Disclosure does not depend on a local client or human observer count')
    from script_ast import walk
    for name,op,body in asts['common/scripted_effects/ICW_superpower_dossier.txt']:
        for key,operator,value in walk(body):
            if key in ('set_variable','add_to_variable','subtract_from_variable','divide_variable','clear_variable','clear_array','set_country_flag','clr_country_flag'):
                target=value[0][0] if isinstance(value,list) else value
                check(bool(re.match(r'(?:global\.)?icsd_',target)),name+' writes only dossier metadata: '+str(target))
    effects=dict((k,v) for k,o,v in asts['common/scripted_effects/ICW_superpower_dossier.txt'])
    for name in ('icsd_build_view','icsd_view_append'):
        source=str(effects[name])
        check(not any(s in source for s in ['network_strength','intel_level_over','every_country','icsd_reconcile']),name+' uses already disclosed cache data only')
    for column in COLS:
        check(f'icsd_mail_{column} index = 0' in runtime and f'icsd_live_{column}' in runtime,column+' participates in bounded journal and live cache')
    check('icsd_selection_found' in runtime and 'clear_variable = icsd_selected_kind' in runtime,'Removed current commitments invalidate selected detail')
    gui=(ROOT/'interface/ICW_superpower_dossier.gui').read_text()
    behavior=(ROOT/'common/scripted_guis/ICW_superpower_dossier.txt').read_text()
    names=set(re.findall(r'name\s*=\s*"([^"]+)"',gui))
    for name in re.findall(r'^\s*((?:icsd|icwt)_[\w]+)\s*=\s*\{',behavior,re.M):
        if name.endswith(('_click','_visible','_click_enabled')):
            suffix='_click_enabled' if name.endswith('_click_enabled') else '_visible' if name.endswith('_visible') else '_click'
            check(name[:-len(suffix)] in names,name+' binds a real GUI element')
    check('selected_country_context' in behavior and 'set_variable = { icsd_response_target = PREV.id }' in behavior,'Country picker uses native country context')
    check('icsd_view_access' in behavior and 'is_ai = no' in (ROOT/'common/scripted_triggers/ICW_superpower_dossier.txt').read_text(),'Only human USA/SOV controls are exposed')
    check('icsd_accept_click' not in behavior and 'icsd_decline_click' not in behavior,'Observer reports cannot answer a native economic offer')
    for rel in manifest['integrations']:
        actual=(ROOT/rel).read_text(encoding='utf-8')
        clean=strip(actual)
        # The current HEAD may already contain this feature's marked insertions.
        # Compare the native source outside those insertions on both sides.
        original=strip(subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT).decode('utf-8-sig').replace('\r\n','\n'))
        check(clean==original,rel+' preserves all original native action code')
        expected=0 if rel.endswith(('imp_sanctions_diplomatic_actions.txt','99_investment_scripted_effects.txt')) else 2 if '00_influence_scripted_effects' in rel else 1 if rel.startswith('events/') else 3
        check(len(re.findall(r'icsd_note_\w+ = yes',actual))==expected,rel+' has only its intended observer callbacks')
    # Geometry of the authored native controls. Inactive overlay variants are intentionally excluded.
    check('width=790 height=794' in gui and 'maxWidth = 508' in gui,'Approved 790x794 dossier proportions and bounded document text')
    check(len(re.findall(r'name = \"icsd_row_\d+\"',gui))==5,'Five native file-index entries per page')
    check('image = ' not in behavior,'No unsupported country image substitution')
    for side,tag in [('usa','USA'),('sov','SOV')]:
        check(f'icsd_paper_{side}_visible = {{ tag = {tag} }}' in behavior and f'icsd_launcher_{side}_visible = {{ tag = {tag} }}' in behavior,tag+' has explicitly gated paper and launcher')
        check(f'name = "icsd_paper_{side}"' in gui and f'spriteType = GFX_icsd_dossier_{side}' in gui,tag+' paper has its own registered static sprite')
    gfx=(ROOT/'interface/ICW_superpower_dossier.gfx').read_text()
    check('gfx/fonts/hoi_16mbs' not in gfx and 'gfx/fonts/hoi_24header' not in gfx,'Dossier uses private regular-weight typewriter and serif fonts')
    check('icsd_tab_active_1_sov' in gui and 'icsd_selected_0_sov' in gui,'Native active-tab and selected-file styling exists')
    from test_treaties import TreatyModel
    model=TreatyModel()
    definitions=dict((k,v) for k,o,v in asts['common/scripted_guis/ICW_superpower_dossier.txt'][0][2])
    for country,expected in [('USA','usa'),('SOV','sov')]:
        for definition,element in [('icsd_main','icsd_paper_'),('icsd_launcher','icsd_launcher_')]:
            rules=dict((k,v) for k,o,v in definitions[definition])['triggers']
            rules=dict((k,v) for k,o,v in rules)
            visible=[side for side in ('usa','sov') if model.test(rules[element+side+'_visible'],(country,country,country))]
            check(visible==[expected],country+' exposes only its own '+element+' image under the emitted native visibility predicates')
        rules=dict((k,v) for k,o,v in dict((k,v) for k,o,v in definitions['icsd_main'])['triggers'])
        model.v[country].update(icsd_tab=2,icwt_screen=3)
        for name in ('icwt_editor_1','icwt_editor_2','icwt_review_edit'):
            check(not model.test(rules[name+'_visible'],(country,country,country)),country+' review hides editing navigation: '+name)
        model.v[country].update(icsd_tab=3,icwt_register=1,icwt_screen=0)
        check(not model.test(rules['icwt_catalog_desc_visible'],(country,country,country)),country+' register cannot overlap catalogue prose')
    for rel,tree in asts.items():
        if not rel.startswith(('common/scripted_effects/ICW_superpower','common/scripted_triggers/ICW_superpower')):continue
        keys=[k for k,o,v in tree]
        check(len(keys)==len(set(keys)),rel+' has unique definitions')
        for k,o,v in walk(tree):
            if k=='for_each_scope_loop':check(not any(n=='limit' for n,o,b in v),rel+' uses documented loop body guards')
    strings=(ROOT/'localisation/english/ICW_superpower_dossier_l_english.yml').read_text(encoding='utf-8-sig')
    getters=set()
    for rel,tree in asts.items():
        if rel.startswith('common/scripted_localisation/ICW_superpower'):
            getters.update(next(b for a,o,b in v if a=='name') for k,o,v in tree if k=='defined_text')
    for getter in set(re.findall(r'\[(icwt_\w+)\]',strings+gui)):
        check(getter in getters,'Dynamic treaty text resolves: '+getter)
    check(all('name = "'+name+'"' not in gui for name in ('icsd_route_sheet','icsd_shade','icsd_modal')),'No intermediary diplomatic-action modal or dimming overlay')
    for name,y in [('icsd_pick',626)]:
        check(re.search(r'name = "'+name+r'"[^\n]*y='+str(y)+r'\b',gui) is not None,name+' fixed footer geometry')
    for name,op,body in asts['common/scripted_guis/ICW_superpower_dossier.txt'][0][2]:
        if name!='icsd_main':continue
        effects=dict((k,v) for k,o,v in body)['effects']
        actions=[(k,v) for k,o,v in effects if re.match(r'icsd_action_\d+(?:_usa|_sov)?_click$',k)]
        check(len(actions)==13,'Every diplomatic response button has a direct native camera route')
        for action,body in actions:
            text_body=str(body)
            check('icsd_locate' in text_body and 'icsd_can_locate' in text_body and 'icsd_route' not in text_body,action+' validates target and closes dossier through native navigation')
    report={'project':'IMPERIA COLD WAR','passed':len(checks),'checks':checks,'scope':'Source/reference/encoding and provider preservation. Not native execution or multiplayer.'}
    (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report if '--full' in sys.argv else {k:v for k,v in report.items() if k!='checks'},indent=2))


if __name__=='__main__':main()
