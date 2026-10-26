# IMPERIA CW — Cold War: Guest Worker Administration
"""Count authored script work for repeatable MP-style workloads.

These are native-script AST operation/iteration counts, not HOI4 timings,
network measurements, FPS estimates, or a substitute for an MP session.
"""
from collections import Counter
import argparse
import json
from pathlib import Path
import validate as V
import validate_diaspora as T
from test_ministry import Machine


class Profile(Machine):
    def __init__(self,*args):
        super().__init__(*args)
        self.calls=Counter();self.origin_entries=0
    def call(self,name,parameters=None,trigger=False):
        self.calls[name]+=1
        return super().call(name,parameters,trigger)
    def array_values(self,name):
        result=super().array_values(name)
        if name=='gw_origins':self.origin_entries+=len(result)
        return result


def origins(m,count=40):
    for i in range(count):
        for key,value in [('origins',i+2),('stock',25),('registered',0),('housed',0),('protected',0),('outreach',0)]:
            m.execute([('add_to_array','=',[('gw_'+key,'=',str(value))])])
    m.root.variables.update(gw_selected_origin=V.D(20),mdcw_gw_guest_workers_k=V.D(count*25))


def measure():
    data=T.load();repeat=25;players=40;result={}
    lookups=[];refresh=[]
    for _ in range(players):
        m=Profile(*data);origins(m)
        m.root.temporary['gw_lookup_origin']=V.D(20)
        for _ in range(repeat):m.call('mdcw_gw_find_origin')
        lookups.append(m.origin_entries)
        m=Profile(*data);origins(m);m.call('mdcw_gw_refresh_dashboard')
        refresh.append(m.calls['mdcw_gw_select_origin'])
    result['origin_lookup']={'countries':players,'origins_per_country':40,'lookups_per_country':repeat,
                             'origin_array_entries_read':sum(lookups)}
    result['community_refresh']={'countries':players,'refreshes_per_country':1,'selection_calls':sum(refresh)}
    scans=0;visits=0
    for _ in range(players):
        m=Profile(*data)
        for n in range(2,100):
            c=V.Country('COUNTRY_'+str(n));c.ideas.add('mdcw_ni_overseas_employment_programme');m.countries[c.tag]=c
        for _ in range(20):m.call('mdcw_gw_ministry_list_partners')
        scans+=m.country_scans;visits+=m.country_scans*len(m.countries)
    result['recruitment_tab_reopening']={'players':players,'world_countries':100,'opens_per_player_same_day':20,
                                        'global_country_scans':scans,'country_candidates_visited':visits}
    calls=0
    for _ in range(100):
        m=Profile(*data);m.root.ideas.clear()
        for _ in range(30):m.call('mdcw_gw_update_cost_receipt')
        calls+=m.calls['mdcw_gw_ministry_counters']
    result['inactive_budget_refresh']={'countries_without_programme_or_residents':100,'budget_refreshes_each':30,
                                       'ministry_display_preparations':calls}
    return {'project':'IMPERIA CW — Cold War','scope':'Synthetic MP-style AST workload; operation counts, not engine timings',
            'workloads':result}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--phase',choices=('before','after'),required=True)
    args=parser.parse_args();result=measure()
    out=V.ROOT/'docs/guest_workers_ministry'/('performance_'+args.phase+'.json')
    out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
