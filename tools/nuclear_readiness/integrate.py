# IMPERIA CW — Cold War: narrow integration into native MD consumers.
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MARK = '# IMPERIA CW — Cold War: nuclear readiness and crisis diplomacy.'

def edit(rel, transform, loc=False):
    path = ROOT / rel
    old = path.read_text(encoding='utf-8-sig')
    backup = HERE / 'baseline' / rel
    if not backup.exists():
        backup.parent.mkdir(parents=True, exist_ok=True)
        backup.write_text(old, encoding='utf-8-sig' if loc else 'utf-8', newline='\n')
    new = transform(old)
    path.write_text(new, encoding='utf-8-sig' if loc else 'utf-8', newline='\n')
    print(('Changed ' if old != new else 'Unchanged ') + rel)

def block_end(s, start):
    depth = 0
    for m in re.finditer(r'#[^\n]*|"(?:\\.|[^"\\])*"|[{}]', s[start:]):
        if m[0] == '{':depth += 1
        elif m[0] == '}':
            depth -= 1
            if depth == 0:return start+m.end()
    raise ValueError('Unclosed block')

def raids(s):
    if 'COLDWAR_nr_record_raid' in s:
        for loss,kind in [('0.05','tactical'),('0.15','state'),('0.4','strategic')]:
            s=s.replace('COLDWAR_nr_record_raid = { LOSS = '+loss+' }','COLDWAR_nr_record_raid_'+kind+' = yes')
        return escalation_raids(s)
    for name,guard,loss in [
        ('tactical_nuclear_strike','tactical',0.05),
        ('state_nuclear_strike','state',0.15),
        ('strategic_nuclear_strike','strategic',0.4),
    ]:
        start = re.search(r'\b'+name+r'\s*=\s*{', s).start()
        end = block_end(s,s.index('{',start))
        body = s[start:end]
        for field in ['available','launchable']:
            m = re.search(r'\b'+field+r'\s*=\s*{',body)
            condition_end=block_end(body,body.index('{',m.start()))
            first_ai=re.search(r'\bis_ai\s*=\s*no',body[m.end():condition_end])
            point=m.end()+first_ai.end()
            add='\n\t\t\t'+MARK+'\n\t\t\tCOLDWAR_nr_'+guard+'_ready = yes'
            if field == 'launchable':
                add+='\n\t\t\t'+('is_able_to_use_nuclear_strikes_tac' if guard=='tactical' else 'is_able_to_use_nuclear_strikes')+' = yes'
                if guard != 'strategic':add+='\n\t\t\tis_able_to_launch_a_nuclear_strike = yes'
                else:add+='\n\t\t\tif = { limit = { has_idea = nuclear_power_def } surrender_progress > 0.5 }'
            body=body[:point]+add+body[point:]
        body=re.sub(r'\bvictim_effects\s*=\s*{',lambda m:m[0]+'\n\t\t\t\t\t'+MARK+'\n\t\t\t\t\tCOLDWAR_nr_record_raid_'+guard+' = yes',body)
        s=s[:start]+body+s[end:]
    return escalation_raids(s)

# IMPERIA CW — Cold War: retain native targeting and outcomes while adding release authority.
def escalation_raids(s):
    for name,kind in [('tactical_nuclear_strike','tactical'),('state_nuclear_strike','state'),('strategic_nuclear_strike','strategic')]:
        start=re.search(r'\b'+name+r'\s*=\s*{',s).start()
        end=block_end(s,s.index('{',start))
        body=s[start:end]
        for field in ['available','launchable']:
            match=re.search(r'\b'+field+r'\s*=\s*{',body)
            stop=block_end(body,body.index('{',match.start()))
            phase=body[match.start():stop]
            if field=='available':
                guard='COLDWAR_nr_can_prepare_'+('tactical' if kind=='tactical' else 'nuclear')+'_operation = yes'
                if guard not in phase:
                    anchor='COLDWAR_nr_'+kind+'_ready = yes'
                    assert phase.count(anchor)==1
                    phase=phase.replace(anchor,anchor+'\n\t\t\t'+MARK+'\n\t\t\t'+guard,1)
                if kind!='tactical':
                    phase=re.sub(r'(?m)^\s*has_war_with\s*=\s*ROOT\s*$', '',phase)
            else:
                phase=re.sub(r'(?m)^(\s*)has_war_with\s*=\s*FROM\s*$',
                             lambda m:m[1]+MARK+'\n'+m[1]+'COLDWAR_nr_can_launch_nuclear_operation = yes',phase)
                assert phase.count('COLDWAR_nr_can_launch_nuclear_operation = yes')==1
            body=body[:match.start()]+phase+body[stop:]
        if 'COLDWAR_nr_resolve_peacetime_operation' not in body:
            body,count=re.subn(r'\bactor_effects\s*=\s*{',
                              lambda m:m[0]+'\n\t\t\t\t\t'+MARK+'\n\t\t\t\t\tCOLDWAR_nr_resolve_peacetime_operation = yes',body)
            assert count==4,(name,count)
        assert body.count('COLDWAR_nr_resolve_peacetime_operation = yes')==4
        s=s[:start]+body+s[end:]
    return s

def economy(s):
    if 'COLDWAR_nr_calculate_budget' in s:return s
    s=s.replace('\tCOLDWAR_calculate_nuclear_development_budget = yes', '\t'+MARK+'\n\tCOLDWAR_nr_calculate_budget = yes\n\tCOLDWAR_calculate_nuclear_development_budget = yes',1)
    s=s.replace('add = COLDWAR_nuclear_development_weekly_cost clamp', 'add = COLDWAR_nuclear_development_weekly_cost add = COLDWAR_nr_weekly_cost clamp',1)
    return s

def damage(s):
    if 'COLDWAR_nr_civilian_protection' in s:return s
    # One call in each state callback, before casualties are multiplied by population.
    return s.replace('set_temp_variable = { temp_state_pop = state_population_k }',MARK+'\n\t\tCOLDWAR_nr_civilian_protection = yes\n\t\tset_temp_variable = { temp_state_pop = state_population_k }')

def doctrine(s):
    if 'COLDWAR_nr_retaliation_allowed' in s:return s
    return s.replace('has_country_flag = has_been_nuked',MARK+'\n\t\t\t\tCOLDWAR_nr_retaliation_allowed = yes')

def legacy(s):
    if 'COLDWAR_nr_enabled' in s:return s
    start=s.index('SOV_USA_nuke_ai = {')
    m=re.search(r'visible\s*=\s*{',s[start:])
    point=start+m.end()
    return s[:point]+'\n\t\t'+MARK+'\n\t\tNOT = { COLDWAR_nr_enabled = yes }'+s[point:]

def money_loc(s):
    if 'COLDWAR_nr_forces_weekly' in s:return s
    key=' DEFENCE_SPENDING_TOOLTIP: '
    lines=s.splitlines()
    for i,line in enumerate(lines):
        if line.startswith(key):
            lines.insert(i,MARK)
            lines[i+1]=line[:-1]+'\\n$[?COLDWAR_nr_forces_weekly|-3] is spent as §YStrategic Forces Readiness§!\\n$[?COLDWAR_nr_civil_weekly|-3] is spent as §YCivil Defence Mobilisation§!"'
            break
    return '\n'.join(lines)+'\n'

if __name__ == '__main__':
    edit('common/raids/nuclear_raids.txt',raids)
    edit('common/scripted_effects/00_money_system.txt',economy)
    edit('common/scripted_effects/mdcw_imperia_nuclear_effects.txt',damage)
    edit('common/scripted_triggers/01_raids_triggers.txt',doctrine)
    edit('common/decisions/categories/99_SOV_decision_categories.txt',legacy)
    edit('localisation/english/MD_money_l_english.yml',money_loc,True)
