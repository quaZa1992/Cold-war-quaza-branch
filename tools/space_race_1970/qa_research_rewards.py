# IMPERIA CW — Cold War: universal research coverage and first-success award limits.
import json
from pathlib import Path
import validate as V
from research_rewards import scope


def run():
    technologies,categories,uncategorised,_=scope(V.ROOT)
    blocks=[body for effect in V.EFFECTS.values() for key,op,body in V.walk(effect) if key=='add_tech_bonus']
    V.check(bool(blocks),'No native research awards generated')
    for block in blocks:
        tags=set(V.values(block,'category'));explicit=set(V.values(block,'technology'))
        V.check(V.first(block,'uses')=='1','General award has more than one use')
        V.check(set(tags)<=categories and explicit<=set(technologies),'Award targets unknown technology selectors')
        uncovered=[ident for ident,own in technologies.items() if ident not in explicit and not own&tags]
        V.check(not uncovered,'General award excludes technologies: '+','.join(uncovered))
        V.check(V.first(block,'bonus') in ['0.10','0.20'],'Research award magnitude changed')
    m=V.Machine(('SAU',));m.init();m.call('cw_sr_p27_success')
    V.check(len(m.c.tech_bonuses)==1 and m.c.tech_bonuses[0][2]=='0.10','First national lunar success did not award exactly one general 10% bonus')
    before=len(m.c.tech_bonuses)
    for _ in range(20):m.call('cw_sr_p27_success')
    V.check(len(m.c.tech_bonuses)==before,'Repeat missions farm general research awards')
    first=V.Machine(('SAU',));first.init();first.call('cw_sr_p15_success')
    V.check(any(b[2]=='0.20' for b in first.c.tech_bonuses),'Unclaimed world milestone did not award its 20% general bonus')
    before=len(first.c.tech_bonuses)
    for _ in range(20):first.call('cw_sr_p15_success')
    V.check(len(first.c.tech_bonuses)==before,'Repeated milestone awards another research bonus')
    for result in ['partial','failure','catastrophic']:
        t=V.Machine(('SAU',));t.init();t.call('cw_sr_p27_'+result)
        V.check(not t.c.tech_bonuses,'Unsuccessful mission granted full research reward')
    source=(V.ROOT/'localisation/english/COLDWAR_space_race_l_english.yml').read_text(encoding='utf-8-sig')
    V.check('space technology' not in source and 'technology in any field' in source,'Localisation still limits awards to space technology')
    report={'checks':V.CHECKS,'status':'passed','technology_count':len(technologies),'category_count':len(categories),'explicit_uncategorised':len(uncategorised),'native_award_blocks':len(blocks),'uses_per_award':1,'repeat_awards':False,'in_game_tested':False}
    Path(__file__).with_name('research_rewards_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))


if __name__=='__main__':run()
