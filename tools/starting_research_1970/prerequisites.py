# IMPERIA COLD WAR — Complete historical starting technology predecessors.
"""Close active native paths and hard dependencies without combining XOR branches."""
from functools import lru_cache
from itertools import product
from pathlib import Path
from catalog import parse, first, bare

ROOT=Path(__file__).resolve().parents[2]
GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
DLCS=('No Step Back','By Blood Alone','Gotterdammerung')


def gate(rows,dlcs):
    values=[]
    for key,op,value in rows:
        if key=='has_dlc':result=value.strip('"') in dlcs
        elif key in ('NOT','AND','OR'):
            children=[gate([row],dlcs) for row in value]
            result=(any(children) if key=='OR' else all(children))
            if key=='NOT':result=not result
        else:result=True
        values.append(result)
    return all(values)


@lru_cache(None)
def folder_gates():
    result={}
    for base in (GAME,ROOT):
        for path in sorted((base/'common/technology_tags').glob('*.txt')):
            for container,op,rows in parse(path.read_text(encoding='utf-8-sig')):
                if container=='technology_folders':
                    result.update({name:first(block,'available',[]) for name,op,block in rows if isinstance(block,list)})
    return result


def active(record,dlcs):
    return gate(record.get('allow_branch',[]),dlcs) and (not record.get('folders') or any(gate(folder_gates().get(folder,[]),dlcs) for folder in record['folders']))


def incoming(techs):
    result={key:set() for key in techs}
    for parent,row in techs.items():
        for child in row.get('paths',[]):
            if child in result:result[child].add(parent)
    return result


def configurations():
    for bits in product((False,True),repeat=3):
        yield {name for name,enabled in zip(DLCS,bits) if enabled},{'common','nsb' if bits[0] else 'legacy','bba' if bits[1] else 'non_bba','got' if bits[2] else 'non_got'}


def required(child,known,dlcs,techs,parents):
    hard=set(techs[child].get('dependencies',[]))
    visible={p for p in parents[child] if active(techs[p],dlcs)}
    # Native XOR weapon specialisations are alternatives, not cumulative tiers.
    ordinary={p for p in visible if not techs[p].get('xor')}
    result=hard|ordinary
    alternatives=visible-ordinary
    if not ordinary and alternatives and not alternatives&known:
        choices=[p for p in alternatives if not(set(techs[p].get('xor',[]))&known)]
        assert choices,('No compatible prerequisite branch',child,sorted(alternatives))
        result.add(min(choices,key=lambda p:(techs[p]['year'] or 0,p)))
    return result


def complete(groups,techs,route):
    groups={name:set(ids) for name,ids in groups.items()}
    parents=incoming(techs)
    while True:
        additions=set()
        for dlcs,enabled in configurations():
            known=set().union(*(groups[group] for group in enabled))
            for child in known:
                additions.update(required(child,known,dlcs,techs,parents)-known)
        if not additions:break
        previous=set().union(*groups.values())
        for parent in sorted(additions):
            assert parent in techs,parent
            assert techs[parent]['year'] is None or techs[parent]['year']<=1969,('Future prerequisite',parent)
            routed=route(parent)
            assert any(parent in ids for ids in routed.values()),('Unroutable prerequisite',parent)
            for name,ids in routed.items():groups[name].update(ids)
        assert set().union(*groups.values())!=previous,('Unresolvable prerequisite routing',sorted(additions))
    for dlcs,enabled in configurations():
        known=set().union(*(groups[group] for group in enabled))
        assert all(not(set(techs[key].get('xor',[]))&known) for key in known),('Conflicting prerequisite branches',sorted(dlcs))
    return {name:sorted(ids) for name,ids in groups.items()}
