# IMPERIA COLD WAR — Reversible native PMC access integration.
"""Apply bounded guards while preserving native costs, templates and cleanup paths."""
from pathlib import Path
import hashlib
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/colonial_affairs'))
from test_runtime import parse, first

MARK = '# IMPERIA COLD WAR — PMC start-date access and Game Controller override.'
ACTIVE = 'ICW_pmc_system_active = yes'
TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|#[^\r\n]*|[{}=]|[^\s{}=#]+')
MANIFEST = Path(__file__).with_name('changes.json')
changes = []


def block(text, path):
    tokens = [m for m in TOKEN.finditer(text) if not m.group().startswith('#')]
    lo, hi = 0, len(tokens)
    for name in path:
        depth = 0
        hits = []
        for i in range(lo, hi - 2):
            s = tokens[i].group()
            if depth == 0 and s == name and tokens[i+1].group() == '=' and tokens[i+2].group() == '{':
                hits.append(i)
            depth += (s == '{') - (s == '}')
        assert len(hits) == 1, (path, name, len(hits))
        start = hits[0]
        opening = start + 2
        depth = 1
        closing = opening + 1
        while depth:
            s = tokens[closing].group()
            depth += (s == '{') - (s == '}')
            closing += 1
        lo, hi = opening + 1, closing - 1
    return tokens[start].start(), tokens[opening].end(), tokens[hi].start()


def change(text, path, kind, value='', tail=''):
    start, opening, closing = block(text, path)
    nl = '\r\n' if '\r\n' in text else '\n'
    value = value.replace('\n', nl)
    indent = re.match(r'[\t ]*', text[text.rfind('\n', 0, start)+1:start]).group()
    inner = indent + '\t'
    body = text[opening:closing]
    if kind == 'prefix':
        new = nl + inner + MARK + nl + inner + value + body
    elif kind == 'wrap':
        body = body.rstrip('\t ')
        new = nl + inner + MARK + nl + inner + 'if = {' + nl + inner + '\tlimit = { ' + value + ' }' + body
        new += inner + '}' + nl
        if tail:
            new += inner + tail.replace('\n', nl + inner) + nl
        new += indent
    else:
        raise AssertionError(kind)
    changes.append({'path': current, 'block': list(path), 'before': text[opening:closing], 'after': new})
    return text[:opening] + new + text[closing:]


def source(rel):
    global current
    current = rel
    return (ROOT/rel).read_bytes().decode('utf-8')


def write(rel, text):
    nl = '\r\n' if '\r\n' in text else '\n'
    header = MARK + nl
    assert not text.startswith(MARK), rel
    changes.append({'path': rel, 'header': header})
    data = (header + text).encode('utf-8')
    staging = (ROOT/rel).with_suffix('.ICW_pmc.tmp')
    staging.write_bytes(data)
    staging.replace(ROOT/rel)


def main():
    if MANIFEST.exists():
        record = json.loads(MANIFEST.read_text(encoding='utf-8'))
        validate_reverse(record, restore='--rebuild' in sys.argv)
        if '--rebuild' not in sys.argv:
            print('PMC integration is already applied; native-source reversal verified.')
            return
        MANIFEST.unlink()
    original = {}
    for rel in ('common/scripted_guis/00_missiles_scripted_guis.txt',
                'common/scripted_triggers/01_international_triggers.txt',
                'common/scripted_effects/02_pmc_scripted_effects.txt',
                'common/decisions/01_pmc_decisions.txt',
                'common/decisions/categories/02_pmc_decision_categories.txt',
                'events/PMC.txt'):
        original[rel] = hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()

    rel = 'common/scripted_guis/00_missiles_scripted_guis.txt'
    text = source(rel)
    text = change(text, ('scripted_gui','MD_missiles_gui','triggers'), 'prefix',
                  'pmc_gui_ledger_button_visible = { '+ACTIVE+' }\n'+
                  '\t\t\tpmc_gui_ledger_button_click_enabled = { '+ACTIVE+' }\n'+
                  '\t\t\ticon_pmc_gui_ledger_visible = { '+ACTIVE+' }')
    text = change(text, ('scripted_gui','MD_missiles_gui','effects','pmc_gui_ledger_button_click'), 'wrap', ACTIVE)
    for name in ('MD_PMC_system_gui','international_pmc_units_dynamic_lists','international_pmc_companies_dynamic_lists'):
        text = change(text, ('scripted_gui',name,'visible'), 'prefix', ACTIVE)
    for name, control in (('international_pmc_units_dynamic_lists','name_of_pmc_units_button'),
                          ('international_pmc_companies_dynamic_lists','name_of_pmc_companies_button')):
        text = change(text, ('scripted_gui',name,'triggers',control+'_click_enabled'), 'prefix', ACTIVE)
        text = change(text, ('scripted_gui',name,'effects',control+'_click'), 'wrap', ACTIVE)
    write(rel, text)

    rel = 'common/scripted_triggers/01_international_triggers.txt'
    text = change(source(rel), ('pmc_can_recruit',), 'prefix', ACTIVE)
    write(rel, text)

    rel = 'common/scripted_effects/02_pmc_scripted_effects.txt'
    text = source(rel)
    names = [k for k,o,v in parse(text) if k.startswith('spawn_')]
    for name in names:
        text = change(text, (name,), 'wrap', ACTIVE)
    write(rel, text)

    rel = 'common/decisions/01_pmc_decisions.txt'
    text = source(rel)
    categories = parse(text)
    recruits = []
    local = []
    for category,o,entries in categories:
        for name,o,body in entries:
            path = (category,name)
            if name.startswith('get_'):
                flag = first(first(body,'complete_effect'),'clr_country_flag')
                assert flag
                recruits.append((name,flag))
                text = change(text, path+('available',), 'prefix', ACTIVE)
                text = change(text, path, 'prefix',
                              'cancel_trigger = { ICW_pmc_system_active = no }\n\t\t'+
                              'cancel_effect = { clr_country_flag = '+flag+' }')
                text = change(text, path+('timeout_effect',), 'wrap', ACTIVE, 'clr_country_flag = '+flag)
            elif name.endswith('_create') or category == 'pmc_global_management' or (category == 'pmc_local_management' and not name.startswith('disband_')):
                if first(body,'visible') is not None:
                    text = change(text, path+('visible',), 'prefix', ACTIVE)
                if first(body,'available') is not None:
                    text = change(text, path+('available',), 'prefix', ACTIVE)
                else:
                    text = change(text, path, 'prefix', 'available = { '+ACTIVE+' }')
                for key in ('complete_effect','remove_effect'):
                    if first(body,key) is not None:
                        tail = ''
                        if name.startswith('recruit_') and key == 'remove_effect':
                            index = len(local)
                            tail = ('else = { ICW_pmc_refund_pending_local_'+str(index)+' = yes }\n'+
                                    'if = { limit = { '+ACTIVE+' } clr_country_flag = ICW_pmc_local_pending_'+str(index)+' }')
                        text = change(text, path+(key,), 'wrap', ACTIVE, tail)
                if name.startswith('recruit_'):
                    index = len(local)
                    effect = first(body,'complete_effect')
                    flag = first(first(first(effect,'if'),'limit'),'has_country_flag')
                    counted = first(first(effect,'if'),'add_to_variable')[0][0].removeprefix('ROOT.')
                    assert flag and counted.startswith('pmc_local_'), (name, flag, counted)
                    local.append((name,flag,counted,index))
                    text = change(text, path+('complete_effect',), 'prefix',
                                  'if = { limit = { '+ACTIVE+' } clr_country_flag = ICW_pmc_local_refunded_'+str(index)+
                                  ' set_country_flag = ICW_pmc_local_pending_'+str(index)+' }')
                    text = change(text, path, 'prefix',
                                  'cancel_trigger = { ICW_pmc_system_active = no }\n\t\t'+
                                  'cancel_effect = { ICW_pmc_refund_pending_local_'+str(index)+' = yes }')
    assert len(recruits) == 35 and len(local) == 7
    write(rel, text)

    rel = 'common/decisions/categories/02_pmc_decision_categories.txt'
    text = change(source(rel), ('pmc_global_management',), 'prefix', 'visible = { '+ACTIVE+' }')
    write(rel, text)

    rel = 'events/PMC.txt'
    text = source(rel)
    # Only the formation news is blocked. Receipts for already signed contracts remain valid.
    text = change(text, ('news_event','trigger'), 'prefix', ACTIVE)
    write(rel, text)

    emit_effects(recruits, local)
    record = {'project':'IMPERIA COLD WAR','native_sha256_before':original,'changes':changes,
              'major_recruitment_missions':[name for name,flag in recruits],
              'local_recruitment_decisions':[name for name,flag,count,index in local],
              'spawn_effects_guarded':len(names)}
    MANIFEST.write_text(json.dumps(record,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    validate_reverse(record)
    print('PMC guards applied. Exact native-source reversal verified.')


def emit_effects(recruits, local):
    lines = [MARK, 'ICW_pmc_cancel_pending_recruitment = {']
    for name,flag in recruits:
        lines.append('\tif = { limit = { has_decision = '+name+' } remove_mission = '+name+' }')
    for name,flag,count,index in local:
        lines.extend(['\tif = {','\t\tlimit = { has_decision = '+name+' }',
                      '\t\tICW_pmc_refund_pending_local_'+str(index)+' = yes',
                      '\t\tremove_decision = '+name,'\t}'])
    for flag in sorted({flag for name,flag in recruits}):
        lines.append('\tclr_country_flag = '+flag)
    lines.extend(['\tclear_variable = var_open_MD_PMC_gui','}', '',
                  MARK, 'ICW_pmc_gc_open = {','\tif = {',
                  '\t\tlimit = { ICW_pmc_gc_controller = yes ICW_pmc_system_active = no }',
                  '\t\tclr_global_flag = ICW_pmc_closed','\t\tset_global_flag = ICW_pmc_opened',
                  '\t\tinternational_systems_force_update = yes','\t}', '}', '',
                  MARK, 'ICW_pmc_gc_close = {','\tif = {',
                  '\t\tlimit = { ICW_pmc_gc_controller = yes ICW_pmc_system_active = yes }',
                  '\t\tset_global_flag = ICW_pmc_closed','\t\tclr_global_flag = ICW_pmc_opened',
                  '\t\tevery_country = { ICW_pmc_cancel_pending_recruitment = yes }',
                  '\t\tinternational_systems_force_update = yes','\t}', '}'])
    for name,flag,count,index in local:
        index = str(index)
        lines.extend(['',MARK,'ICW_pmc_refund_pending_local_'+index+' = {','\tif = {',
                      '\t\tlimit = { NOT = { has_country_flag = ICW_pmc_local_refunded_'+index+' } check_variable = { '+count+' > 0 } OR = { has_country_flag = ICW_pmc_local_pending_'+index+' has_decision = '+name+' } }',
                      '\t\tset_country_flag = ICW_pmc_local_refunded_'+index,
                      '\t\tclr_country_flag = ICW_pmc_local_pending_'+index,
                      '\t\tset_temp_variable = { treasury_change = global.mercs_cost^'+index+' }',
                      '\t\tmultiply_temp_variable = { treasury_change = 0.8 }',
                      '\t\tmodify_treasury_effect = yes',
                      '\t\tset_temp_variable = { temp_expense = global.mercs_weekly_cost^'+index+' }',
                      '\t\tmultiply_temp_variable = { temp_expense = 0.8 }',
                      '\t\tsubtract_from_variable = { pmc_expenses = temp_expense }',
                      '\t\tsubtract_from_variable = { pmc_bought = 1 }',
                      '\t\tsubtract_from_variable = { merc_deployed = global.merc_deploy_cost^'+index+' }',
                      '\t\tsubtract_from_variable = { '+count+' = 1 }',
                      '\t\tif = { limit = { check_variable = { '+count+' < 1 } } clr_country_flag = '+flag+' }',
                      '\t}', '}'])
    target = ROOT/'common/scripted_effects/ICW_pmc_access.txt'
    target.write_text('\n'.join(lines)+'\n',encoding='utf-8')


def validate_reverse(record, restore=False):
    originals = {}
    for rel, expected in record['native_sha256_before'].items():
        text = (ROOT/rel).read_bytes().decode('utf-8')
        for edit in reversed(record['changes']):
            if edit['path'] != rel:
                continue
            if 'header' in edit:
                assert text.startswith(edit['header'])
                text = text[len(edit['header']):]
            else:
                _, opening, closing = block(text, edit['block'])
                assert text[opening:closing] == edit['after'], (rel, edit['block'])
                text = text[:opening] + edit['before'] + text[closing:]
        assert hashlib.sha256(text.encode('utf-8')).hexdigest() == expected, rel
        originals[rel] = text.encode('utf-8')
    if restore:
        for rel, data in originals.items():
            staging = (ROOT/rel).with_suffix('.ICW_pmc.tmp')
            staging.write_bytes(data)
            staging.replace(ROOT/rel)


if __name__ == '__main__':
    main()
