# IMPERIA CW — Cold War: source-level validation of the installed DPRK programme.
"""Exercise emitted scripts and native helper interfaces; this is not the HOI4 engine."""
from pathlib import Path
from copy import deepcopy
import sys,json,re,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk
D=json.loads((ROOT/'tools/north_korea_1970/current_design.json').read_text(encoding='utf-8'))
FILES=[*ROOT.glob('common/**/COLDWAR_NKO_1970*.txt'),*ROOT.glob('events/COLDWAR_NKO_1970*.txt'),*ROOT.glob('interface/COLDWAR_NKO_1970*.gfx')]
E={};T={};DM={}
for folder,target in [('scripted_effects',E),('scripted_triggers',T),('dynamic_modifiers',DM)]:
    for path in (ROOT/'common'/folder).glob('COLDWAR_NKO_1970*.txt'):
        for k,_,v in parse(path.read_text(encoding='utf-8')):
            assert k not in target,('duplicate definition',k)
            target[k]=v

class Model:
    def __init__(self):
        self.c={tag:dict(flags={},v={'gdp_total':100.,'treasury':0.,'debt':0.,'ruling_party':4},tmp={},dm=set(),completed=set(),arrays={},leader='Kim Il Sung',tree='COLDWAR_NKO_1970_focus',subject=False) for tag in D['country_names']}
        self.s={int(k):dict(owner='NKO',controller='NKO',slots=0,build={},coast=int(k)!=1201) for k in D['state_names']}
        self.globalflags=set();self.wars=set();self.day=0;self.date=(1986,1,1);self.events=[];self.goals=[];self.kills=[]
        self.c['NKO']['flags']['COLDWAR_NKO_initialized']=None
    def scope(self,name,ctx):return {'ROOT':ctx[2],'THIS':ctx[0],'PREV':ctx[1],'FROM':ctx[3]}.get(name,name)
    def value(self,x,ctx):
        try:return float(x)
        except (ValueError,TypeError):pass
        if '.' in x:
            prefix,name=x.split('.',1)
            tag=self.scope(prefix,ctx)
            if tag in self.c:
                if name=='id':return tag
                return self.c[tag]['tmp'].get(name,self.c[tag]['v'].get(name,0))
        c=self.c[ctx[0]];return c['tmp'].get(x,c['v'].get(x,0))
    def trigger(self,rows,ctx):
        results=[]
        for k,op,v in rows:
            c=self.c.get(ctx[0]);state=self.s.get(int(ctx[0])) if ctx[0].isdigit() else None
            if k in T:result=self.trigger(T[k],ctx)==(v=='yes')
            elif k in self.c or k in ('NKO','SOV','CHI','KOR','DDR','BUL','ROM','EGY','JAP','ROOT','PREV','THIS','FROM'):
                tag=self.scope(k,ctx);result=tag in self.c and self.trigger(v,(tag,ctx[0],ctx[2],ctx[3]))
            elif k.isdigit():result=int(k) in self.s and self.trigger(v,(k,ctx[0],ctx[2],ctx[3]))
            elif k in ('AND','hidden_trigger'):result=self.trigger(v,ctx)
            elif k=='OR':result=any(self.trigger([row],ctx) for row in v)
            elif k=='NOT':result=not self.trigger(v,ctx)
            elif k=='custom_trigger_tooltip':result=self.trigger([r for r in v if r[0] not in ('tooltip','not_tooltip')],ctx)
            elif k in ('tag','original_tag'):result=ctx[0]==v
            elif k in ('IMP_is_1970_scenario','COLDWAR_nuc_economy_allows'):result=v=='yes'
            elif k=='country_exists':result=v in self.c
            elif k=='exists':result=(ctx[0] in self.c)==(v=='yes')
            elif k=='always':result=v=='yes'
            elif k=='is_subject':result=c['subject']==(v=='yes')
            elif k=='has_war_with':result=frozenset((ctx[0],self.scope(v,ctx))) in self.wars
            elif k=='has_country_flag':result=v in c['flags'] and (c['flags'][v] is None or c['flags'][v]>self.day)
            elif k=='has_global_flag':result=v in self.globalflags
            elif k=='has_dynamic_modifier':result=first(v,'modifier') in c['dm']
            elif k=='has_country_leader':result=c['leader']==first(v,'name').strip('"')
            elif k=='has_focus_tree':result=c['tree']==v
            elif k=='has_completed_focus':result=v in c['completed']
            elif k=='has_variable':result=v in c['v']
            elif k=='check_variable':
                a,comparison,b=v[0];left=self.value(a,ctx);right=self.value(b,ctx)
                result={'=':left==right,'>':left>right,'<':left<right,'>=':left>=right,'<=':left<=right}[comparison]
            elif k=='is_in_array':
                array=first(v,'array',first(v,v[0][0]));value=first(v,'value')
                if value is None:array=v[0][0];value=v[0][2]
                result=self.scope(value,ctx) in c['arrays'].get(array,set())
            elif k=='date':
                d=tuple(map(int,v.split('.')));result={'=':self.date==d,'>':self.date>d,'<':self.date<d}[op]
            elif k=='is_owned_by':result=state['owner']==v
            elif k=='is_controlled_by':result=state['controller']==v
            elif k=='is_coastal':result=state['coast']==(v=='yes')
            elif state is not None:
                level=state['build'].get(k,0);result=level<float(v) if op=='<' else level==float(v)
            else:raise AssertionError(('Unsupported source trigger',k,op,v))
            results.append(result)
        return all(results)
    def run(self,rows,ctx):
        branch=False
        for k,op,v in rows:
            c=self.c.get(ctx[0]);state=self.s.get(int(ctx[0])) if ctx[0].isdigit() else None
            if k=='effect_tooltip':continue
            if k in E:self.run(E[k],ctx)
            elif k in self.c or k in ('ROOT','PREV','THIS','FROM'):
                self.run(v,(self.scope(k,ctx),ctx[0],ctx[2],ctx[3]))
            elif k.isdigit():self.run(v,(k,ctx[0],ctx[2],ctx[3]))
            elif k=='if':
                branch=self.trigger(first(v,'limit',[]),ctx)
                if branch:self.run([r for r in v if r[0]!='limit'],ctx)
            elif k=='else_if':
                if not branch:
                    branch=self.trigger(first(v,'limit',[]),ctx)
                    if branch:self.run([r for r in v if r[0]!='limit'],ctx)
            elif k=='else':
                if not branch:self.run(v,ctx)
            elif k=='hidden_effect':self.run(v,ctx)
            elif k in ('custom_effect_tooltip','newline','log'):continue
            elif k=='set_country_flag':c['flags'][first(v,'flag') if isinstance(v,list) else v]=self.day+int(first(v,'days')) if isinstance(v,list) and first(v,'days') else None
            elif k=='clr_country_flag':c['flags'].pop(v,None)
            elif k=='set_global_flag':self.globalflags.add(v)
            elif k=='clr_global_flag':self.globalflags.discard(v)
            elif k in ('set_variable','set_temp_variable','add_to_variable','subtract_from_variable','multiply_temp_variable','divide_temp_variable','multiply_variable','divide_variable','add_to_temp_variable'):
                name,_,amount=v[0];target=c['tmp'] if ('temp_variable' in k or k=='set_temp_variable') else c['v'];amount=self.value(amount,ctx)
                if k.startswith('set_'):target[name]=amount
                elif k.startswith('add_'):target[name]=target.get(name,0)+amount
                elif k.startswith('subtract_'):target[name]=target.get(name,0)-amount
                elif k.startswith('multiply_'):target[name]=target.get(name,0)*amount
                else:target[name]=target.get(name,0)/amount
            elif k in ('clear_variable','clear_temp_variable'):(c['tmp'] if k=='clear_temp_variable' else c['v']).pop(v,None)
            elif k=='modify_treasury_effect':c['v']['treasury']+=c['tmp']['treasury_change']
            elif k=='modify_debt_effect':c['v']['debt']=max(0,c['v']['debt']+c['tmp']['debt_change'])
            elif k=='add_dynamic_modifier':
                mid=first(v,'modifier');assert mid in DM,mid
                if self.trigger(first(DM[mid],'enable',[]),ctx):c['dm'].add(mid)
            elif k=='remove_dynamic_modifier':c['dm'].discard(first(v,'modifier'))
            elif k=='add_extra_state_shared_building_slots':state['slots']+=int(v)
            elif k=='add_building_construction':
                kind=first(v,'type');state['build'][kind]=state['build'].get(kind,0)+int(first(v,'level'))
            elif k=='load_focus_tree':c['tree']=v
            elif k in ('country_event','news_event'):self.events.append((ctx[0],k,first(v,'id') if isinstance(v,list) else v))
            elif k=='create_wargoal':self.goals.append((ctx[0],first(v,'target'),first(v,'type')))
            elif k=='kill_country_leader':self.kills.append((ctx[0],c['leader']));c['leader']=None
            elif k=='create_country_leader':c['leader']=first(v,'name').strip('"')
            elif k=='add_tech_bonus':c.setdefault('research',[]).append(tuple(v))
            elif k=='change_permanent_investment_target':
                self.c[c['tmp']['target_nation']]['arrays'].setdefault('permanent_investment_targets',set()).add(c['tmp']['adding_nation'])
            else:raise AssertionError(('Unsupported source effect',k,op,v))
    def call(self,name,tag='NKO'):self.run(E[name],(tag,tag,tag,'NKO'))
    def state(self):return deepcopy((self.c,self.s,self.globalflags,self.goals,self.kills))

def structural():
    for p in FILES:
        raw=p.read_bytes();assert not raw.startswith(b'\xef\xbb\xbf'),p
        rows=parse(raw.decode('utf-8'))
        assert not any(k in ('_bare','_list') for k,_,_ in walk(rows)),('invalid emitted bare token',p)
        for k,_,v in walk(rows):
            assert k!='clear_temp_variable',('engine-rejected temporary cleanup',p)
            if k.startswith('COLDWAR_NKO_') and isinstance(v,str) and v in ('yes','no'):assert k in E or k in T,('missing helper',p,k)
            if isinstance(v,str) and re.fullmatch(r'-?\d+\.\d{6,}',v):raise AssertionError(('unsafe fixed-point literal',p,k,v))
    loc={}
    for p in (ROOT/'localisation/english').glob('COLDWAR_NKO_1970*.yml'):
        raw=p.read_bytes();assert raw.startswith(b'\xef\xbb\xbf') and not raw.startswith(b'\xef\xbb\xbf\xef\xbb\xbf'),p
        assert '\ufffd' not in raw.decode('utf-8-sig'),('replacement character in localization',p)
        for key,value in re.findall(r'^\s+([^ #:\s]+):\d*\s+"(.*)"',raw.decode('utf-8-sig'),re.M):
            assert key not in loc,('duplicate localization',key);loc[key]=value
    tree=first(parse((ROOT/'common/national_focus/COLDWAR_NKO_1970_focus.txt').read_text(encoding='utf-8')),'focus_tree')
    nodes={first(v,'id'):v for k,_,v in tree if k=='focus'};assert len(nodes)==360 and len(nodes)==len(D['nodes'])
    coords={}
    def xy(nid):
        if nid in coords:return coords[nid]
        node=nodes[nid];x,y=int(first(node,'x')),int(first(node,'y'));anchor=first(node,'relative_position_id')
        if anchor:a,b=xy(anchor);x+=a;y+=b
        coords[nid]=(x,y);return x,y
    for n in D['nodes']:
        node=nodes[n['id']];assert xy(n['id'])==(n['x'],n['y'])
        assert [values(pg,'focus') for pg in values(node,'prerequisite')]==n['prerequisites']
        assert set(values(first(node,'mutually_exclusive',[]),'focus'))==set(n['mutex'])
        assert first(node,'icon')==n['icon'] and float(first(node,'cost'))==n['cost']
        assert n['id'] in loc and n['id']+'_desc' in loc
        if n['modifiers']:
            got={k:float(v) for k,_,v in DM[n['id']+'_programme'] if k not in ('icon','enable')}
            assert got==n['modifiers'],n['id']
    # An exclusion must be reciprocal, and every AND/OR prerequisite graph must
    # have a consistent completion certificate without selecting both rivals.
    prerequisites={nid:values(node,'prerequisite') for nid,node in nodes.items()}
    parents={nid:[values(pg,'focus') for pg in groups] for nid,groups in prerequisites.items()}
    rivals={nid:set(values(first(node,'mutually_exclusive',[]),'focus')) for nid,node in nodes.items()}
    visiting=set();visited=set()
    def visit(nid):
        assert nid in nodes,('missing predecessor',nid)
        assert nid not in visiting,('prerequisite cycle',nid)
        if nid in visited:return
        visiting.add(nid)
        for pg in parents[nid]:
            assert pg,('empty prerequisite group',nid)
            for parent in pg:visit(parent)
        visiting.remove(nid);visited.add(nid)
    def certificate(todo,chosen):
        if not todo:return chosen
        pg,*rest=todo
        if chosen.intersection(pg):return certificate(rest,chosen)
        for nid in pg:
            if rivals[nid].intersection(chosen):continue
            result=certificate(parents[nid]+rest,chosen|{nid})
            if result is not None:return result
        return None
    for nid in nodes:
        visit(nid)
        assert nid not in rivals[nid],('self exclusion',nid)
        for rival in rivals[nid]:assert rival in nodes and nid in rivals[rival],('asymmetric exclusion',nid,rival)
        assert certificate([[nid]],set()) is not None,('unreachable exclusion/dependency combination',nid)
    items=list(coords.items())
    for i,(nid,(x,y)) in enumerate(items):
        for other,(ox,oy) in items[i+1:]:
            assert abs(x-ox)*96>=165 or abs(y-oy)*130>=128,('overlapping focus cards',nid,other)
    approved=json.loads((ROOT/'docs/COLDWAR_NKO_1970_concept/v2/COLDWAR_NKO_v2_design.json').read_text(encoding='utf-8'))
    current={n['id']:n for n in D['nodes']}
    for old in approved['nodes']:
        new=current[old['id']]
        for field in ('x','dx','dy','anchor','cost','prerequisites','mutex','modifiers','slot','icon'):
            assert new[field]==old[field],('unrequested original graph change',old['id'],field)
        roots={g['id']:g['y'] for g in D['groups']};oldroots={g['id']:g['y'] for g in approved['groups']}
        assert new['y']==old['y']+roots[old['group']]-oldroots[old['group']]
        assert abs(new['cost_gdp_share']-old['cost_gdp_share']*1.25)<.000006
    fnt=Path(r'C:/Program Files (x86)/Steam/steamapps/common/Hearts of Iron IV/gfx/fonts/hoi_16mbs.fnt').read_text(encoding='utf-8')
    advances={int(cid):int(advance) for cid,advance in re.findall(r'char id=(\d+).*?xadvance=(-?\d+)',fnt)}
    for n in D['nodes']:
        assert all(ord(c) in advances for c in n['title']),('unsupported title glyph',n['id'])
        assert sum(advances[ord(c)] for c in n['title'])<=147,('title too wide',n['id'],n['title'])
    assert not any('Expenditure:' in text for text in loc.values()),'Duplicate GDP expenditure prose'
    for key,text in loc.items():
        if key.endswith('_building_tt'):assert text.count('§G')==2,(key,text)
        if key.startswith('COLDWAR_NKO_foreign_offer_') and key.endswith('_terms'):
            assert len(text)<250 and '% of' not in text and 'effects:' not in text,('verbose proposal prose',key)
    for p in FILES:
        for k,_,v in walk(parse(p.read_text(encoding='utf-8'))):
            if k in ('custom_effect_tooltip','tooltip') and isinstance(v,str) and v.startswith('COLDWAR_NKO_'):assert v in loc,(p,v)
            if k in ('add_dynamic_modifier','remove_dynamic_modifier'):
                mid=first(v,'modifier');assert mid in DM,(p,mid)
        def preview_calls(rows,inside=False):
            for k,_,v in rows:
                if isinstance(v,list):preview_calls(v,inside or k=='effect_tooltip')
                elif k.startswith(('COLDWAR_NKO_foreign_preview_','COLDWAR_NKO_foreign_terms_')) and v=='yes':
                    assert inside,('display-only helper called at runtime',p,k)
        preview_calls(parse(p.read_text(encoding='utf-8')))
    # Event IDs, decision labels and proposal feedback are checked independently
    # of their generators, including uniqueness and all queued event references.
    event_ids=set()
    for p in (ROOT/'events').glob('COLDWAR_NKO_1970*.txt'):
        for kind,_,body in parse(p.read_text(encoding='utf-8')):
            if kind not in ('country_event','news_event'):continue
            eid=first(body,'id');assert eid not in event_ids,('duplicate event',eid);event_ids.add(eid)
            for k,_,v in walk(body):
                if k in ('title','desc','text','name') and isinstance(v,str) and v.startswith('COLDWAR_NKO_'):assert v in loc,(eid,k,v)
    assert sum(x.startswith('COLDWAR_NKO_foreign.') for x in event_ids)==4*sum(1+len(a['upgrades']) for a in D['agreements'])
    for p in FILES:
        for k,_,v in walk(parse(p.read_text(encoding='utf-8'))):
            if k in ('country_event','news_event') and isinstance(v,list):assert first(v,'id') in event_ids,(p,first(v,'id'))
    sprites=set()
    for p in (ROOT/'interface').glob('*.gfx'):
        sprites.update(re.findall(r'\bname\s*=\s*"([^"\r\n]+)"',p.read_text(encoding='utf-8-sig')))
    for p in (ROOT/'common/decisions').glob('COLDWAR_NKO_1970*.txt'):
        for category,_,body in parse(p.read_text(encoding='utf-8')):
            assert category in loc,category
            for did,_,decision in body:
                assert did in loc and did+'_desc' in loc,('unlocalized decision',did)
                assert first(decision,'icon') in sprites,('unregistered decision icon',did,first(decision,'icon'))
    for p in (ROOT/'interface').glob('COLDWAR_NKO_1970*.gfx'):
        for k,_,v in walk(parse(p.read_text(encoding='utf-8'))):
            if k=='texturefile':assert (ROOT/v.strip('"')).exists(),('missing texture',v)
    # Native MD entry points must retain exactly one country adapter.
    shared={
      '00_money_system.txt':'COLDWAR_NKO_foreign_add_weekly_expenses = yes',
      '00_MD_politicsview_scripted_effects.txt':'COLDWAR_NKO_refresh_programmes = yes',
      'IMP_sanctions_effects.txt':'COLDWAR_NKO_foreign_refresh = yes',
      'mdcw_1970_focus_tree_effects.txt':'# COLDWAR NKO authored tree',
    }
    for filename,anchor in shared.items():
        p=ROOT/'common/scripted_effects'/filename;raw=p.read_bytes()
        assert not raw.startswith(b'\xef\xbb\xbf'),p
        assert raw.decode('utf-8').count(anchor)==1,('missing or duplicate integration',filename)
    xp=(ROOT/'localisation/english/MD_dm_modifiers_l_english.yml').read_bytes()
    assert xp.startswith(b'\xef\xbb\xbf') and not xp.startswith(b'\xef\xbb\xbf\xef\xbb\xbf')
    assert 'experience_gain_army_tt: "$MODIFIER_XP_GAIN_ARMY$: $RIGHT|+=2$"' in xp.decode('utf-8-sig')
    return len(loc)

def transactions():
    cases=0
    for a in D['agreements']:
        key=a['key'];partner=a['partner'];m=Model()
        m.c['NKO']['v']['treasury']=-5.;m.c[partner]['v']['treasury']=-10.
        m.call('COLDWAR_NKO_offer_'+key+'_base')
        pending=a['receipts']['pending'];assert pending in m.c[partner]['flags']
        assert m.c['NKO']['v']['treasury']==-5.
        m.call('COLDWAR_NKO_foreign_accept_'+key+'_base',partner)
        assert a['receipts']['accepted'] in m.c[partner]['flags'],key
        assert abs(m.c['NKO']['v']['treasury']-(-5-100*a['nko']['setup_gdp_share']))<1e-8,key
        assert abs(m.c[partner]['v']['treasury']-(-10-100*a['recipient']['setup_gdp_share']))<1e-8,key
        before=m.state();m.call('COLDWAR_NKO_foreign_accept_'+key+'_base',partner);assert m.state()==before
        m.c['NKO']['v']['additional_expenses_rate']=0;m.call('COLDWAR_NKO_foreign_add_weekly_expenses')
        assert abs(m.c['NKO']['v']['additional_expenses_rate']-100*a['nko']['annual_commitment_gdp_share']/52)<1e-8
        cases+=4
        base=deepcopy(m)
        for direction in ('NKO',partner):
            for cls in ('dip','fin','eco','mil'):
                m=deepcopy(base);other=partner if direction=='NKO' else 'NKO';m.c[direction]['arrays']['imp_'+cls+'_sanc_by_us']={other}
                m.call('COLDWAR_NKO_foreign_refresh')
                assert not any(key+'_base_' in x for tag in ('NKO',partner) for x in m.c[tag]['dm'])
                m.c['NKO']['v']['additional_expenses_rate']=0;m.call('COLDWAR_NKO_foreign_add_weekly_expenses');assert m.c['NKO']['v']['additional_expenses_rate']==0
                m.c[direction]['arrays'].clear();beforemoney=[m.c[t]['v']['treasury'] for t in ('NKO',partner)];m.call('COLDWAR_NKO_foreign_refresh')
                assert [m.c[t]['v']['treasury'] for t in ('NKO',partner)]==beforemoney
                assert any(key+'_base_' in x for x in m.c['NKO']['dm']);cases+=1
        m=deepcopy(base);m.wars.add(frozenset(('NKO',partner)));m.call('COLDWAR_NKO_foreign_refresh')
        assert not any(key+'_base_' in x for x in m.c['NKO']['dm']);m.wars.clear();m.call('COLDWAR_NKO_foreign_refresh');assert any(key+'_base_' in x for x in m.c['NKO']['dm']);cases+=1
        for u in a['upgrades']:
            m=deepcopy(base);m.c['NKO']['flags']['COLDWAR_NKO_safeguards_valid']=None
            m.call('COLDWAR_NKO_offer_'+u['key']);m.call('COLDWAR_NKO_foreign_accept_'+key+'_'+u['key'],partner)
            assert u['receipt'] in m.c['NKO']['flags'];assert any(key+'_'+u['key']+'_' in x for x in m.c['NKO']['dm'])
            assert not any(key+'_base_' in x for x in m.c['NKO']['dm'])
            before=m.state();m.call('COLDWAR_NKO_foreign_accept_'+key+'_'+u['key'],partner);assert m.state()==before;cases+=1
        m=Model();m.call('COLDWAR_NKO_offer_'+key+'_base');beforemoney=[m.c[t]['v']['treasury'] for t in ('NKO',partner)]
        m.call('COLDWAR_NKO_foreign_decline_'+key+'_base',partner);assert pending not in m.c['NKO']['flags'] and pending not in m.c[partner]['flags']
        assert [m.c[t]['v']['treasury'] for t in ('NKO',partner)]==beforemoney;m.call('COLDWAR_NKO_foreign_send_'+key+'_base');assert pending not in m.c[partner]['flags']
        m.day=180;m.call('COLDWAR_NKO_foreign_send_'+key+'_base');assert pending in m.c[partner]['flags'];cases+=1
        m=Model();m.call('COLDWAR_NKO_offer_'+key+'_base');m.day=91;m.call('COLDWAR_NKO_foreign_refresh')
        assert 'COLDWAR_NKO_foreign_resubmit_'+key+'_base' in m.c['NKO']['flags'];m.call('COLDWAR_NKO_foreign_send_'+key+'_base');assert pending not in m.c[partner]['flags']
        m.day=180;m.call('COLDWAR_NKO_foreign_send_'+key+'_base');assert m.c[partner]['flags'][pending]==270;cases+=1
    return cases

def domestic_and_succession():
    m=Model();m.call('COLDWAR_NKO_refresh_programmes');assert sum('start' in x or any(s['id']==x for s in D['starting_spirits']) for x in m.c['NKO']['dm'])==6
    m.c['NKO']['completed'].add('COLDWAR_NKO_fifth_congress');m.call('COLDWAR_NKO_complete_monolithic');assert 'COLDWAR_NKO_monolithic_programme' in m.c['NKO']['dm']
    m.c['NKO']['v']['ruling_party']=5;m.call('COLDWAR_NKO_refresh_programmes');assert 'COLDWAR_NKO_monolithic_programme' not in m.c['NKO']['dm'] and 'COLDWAR_NKO_monolithic_start' not in m.c['NKO']['dm']
    before=deepcopy((m.s,m.c['NKO']['v']));m.c['NKO']['v']['ruling_party']=4;m.call('COLDWAR_NKO_refresh_programmes');assert 'COLDWAR_NKO_monolithic_programme' in m.c['NKO']['dm'];assert m.s==before[0]
    principal=100*next(e['principal_gdp_share'] for n in D['nodes'] for e in n['extra'] if e['kind']=='debt')
    m=Model();m.call('COLDWAR_NKO_open_machinery_credit');assert m.c['NKO']['v']['treasury']==0 and m.c['NKO']['v']['debt']==principal
    m.c['NKO']['v']['gdp_total']=200;m.c['NKO']['flags']['COLDWAR_NKO_machinery_review_pending']=None;m.call('COLDWAR_NKO_settle_machinery_account');assert m.c['NKO']['v']['treasury']==-principal and m.c['NKO']['v']['debt']==0
    before=m.state();m.call('COLDWAR_NKO_settle_machinery_account');assert m.state()==before
    for party,leader,expected in [(4,'Kim Il Sung',True),(5,'Another Leader',False),(4,'Another Leader',False)]:
        m=Model();m.date=(1994,7,8);m.c['NKO']['v']['ruling_party']=party;m.c['NKO']['leader']=leader;m.call('COLDWAR_NKO_world_succession_daily','SOV')
        assert (m.c['NKO']['leader']=='Kim Jong-il')==expected;assert len(m.events)==1
        before=m.state();m.call('COLDWAR_NKO_world_succession_daily','CHI');assert m.state()==before and len(m.events)==1
    m=Model();m.date=(1994,7,8);del m.c['NKO'];m.call('COLDWAR_NKO_world_succession_daily','SOV');assert len(m.events)==1
    return 10

def additional_lifecycles():
    cases=0
    for a in D['agreements']:
        key=a['key'];partner=a['partner'];send='COLDWAR_NKO_offer_'+key+'_base';accept='COLDWAR_NKO_foreign_accept_'+key+'_base'
        # An offer is a saved quote, not an acceptance-time price. Each endpoint
        # pays its own quoted GDP share and current GDP drives recurring fees.
        m=Model();m.c['NKO']['v']['gdp_total']=140;m.c[partner]['v']['gdp_total']=310;m.call(send)
        m.c['NKO']['v']['gdp_total']=240;m.c[partner]['v']['gdp_total']=510;m.call(accept,partner)
        assert abs(m.c['NKO']['v']['treasury']+140*a['nko']['setup_gdp_share'])<1e-8
        assert abs(m.c[partner]['v']['treasury']+310*a['recipient']['setup_gdp_share'])<1e-8
        for tag,side in [('NKO','nko'),(partner,'recipient')]:
            m.c[tag]['v']['additional_expenses_rate']=0;m.call('COLDWAR_NKO_foreign_add_weekly_expenses',tag)
            assert abs(m.c[tag]['v']['additional_expenses_rate']-m.c[tag]['v']['gdp_total']*a[side]['annual_commitment_gdp_share']/52)<1e-8
        cases+=1
        m=Model();m.call(send);before=m.state();m.call(accept,'CHI' if partner!='CHI' else 'SOV');assert m.state()==before;cases+=1
        # An intervening war cancels an outstanding offer without a transfer.
        m=Model();m.call(send);m.wars.add(frozenset(('NKO',partner)));m.call(accept,partner)
        assert a['receipts']['accepted'] not in m.c['NKO']['flags']
        assert m.c['NKO']['v']['treasury']==m.c[partner]['v']['treasury']==0
        m.call('COLDWAR_NKO_foreign_refresh');m.call('COLDWAR_NKO_foreign_refresh')
        assert a['receipts']['pending'] not in m.c['NKO']['flags'] and a['receipts']['pending'] not in m.c[partner]['flags']
        closed=[e for e in m.events if e[0]=='NKO'];m.call('COLDWAR_NKO_foreign_refresh');assert [e for e in m.events if e[0]=='NKO']==closed;cases+=1
        # Refresh after loading a save repairs a missing endpoint spirit without
        # replaying its payment, factory, slots or acceptance notification.
        m=Model();m.call(send);m.call(accept,partner);m.c[partner]['dm'].clear()
        money=[m.c[t]['v']['treasury'] for t in ('NKO',partner)];states=deepcopy(m.s);events=deepcopy(m.events)
        m.call('COLDWAR_NKO_foreign_refresh');m.call('COLDWAR_NKO_foreign_refresh')
        assert [m.c[t]['v']['treasury'] for t in ('NKO',partner)]==money and m.s==states and m.events==events
        assert 'COLDWAR_NKO_1970_foreign_'+key+'_base_partner' in m.c[partner]['dm'];cases+=1
    # Every authored construction grant is paired in the same actual state and
    # cannot repeat. Invalid primary sites must choose the documented fallback.
    for n in D['nodes']:
        for b in [e for e in n['extra'] if e['kind']=='building']:
            m=Model();m.date=(1995,1,1);m.c['NKO']['v']['ruling_party']=n['slot'] if n['slot'] is not None else 4
            for pg in n['prerequisites']:m.c['NKO']['completed'].update(pg)
            m.call('COLDWAR_NKO_complete_'+n['key'])
            added=[s for s in m.s.values() if s['slots']]
            assert len(added)==1 and added[0]['slots']==b['slots'] and added[0]['build'][b['type']]==b['levels'],n['key']
            before=m.state();m.call('COLDWAR_NKO_complete_'+n['key']);assert m.state()==before;cases+=1
            if len(b['state_ids'])>1:
                m=Model();m.date=(1995,1,1);m.c['NKO']['v']['ruling_party']=n['slot'] if n['slot'] is not None else 4
                for pg in n['prerequisites']:m.c['NKO']['completed'].update(pg)
                m.s[b['state_ids'][0]]['controller']='KOR';m.call('COLDWAR_NKO_complete_'+n['key'])
                assert m.s[b['state_ids'][0]]['slots']==0 and sum(s['slots'] for s in m.s.values())==b['slots'],n['key'];cases+=1
    m=Model();m.s[602]['build']['industrial_complex']=50;m.call('COLDWAR_NKO_offer_soviet_industry_base');m.call('COLDWAR_NKO_foreign_accept_soviet_industry_base','SOV')
    assert m.s[602]['slots']==0 and m.s[1200]['slots']==1 and m.s[1200]['build']['industrial_complex']==1;cases+=1
    m=Model();m.s[602]['build']['industrial_complex']=50;m.s[1200]['build']['industrial_complex']=50;m.call('COLDWAR_NKO_offer_soviet_industry_base');before=m.state();m.call('COLDWAR_NKO_foreign_accept_soviet_industry_base','SOV');assert m.state()==before;cases+=1
    m=Model();m.call('COLDWAR_NKO_offer_soviet_industry_base');m.call('COLDWAR_NKO_foreign_accept_soviet_industry_base','SOV');m.wars.add(frozenset(('NKO','SOV')));m.call('COLDWAR_NKO_foreign_refresh')
    assert 'COLDWAR_NKO_patron_disruption' in m.c['NKO']['dm'];m.call('COLDWAR_NKO_mitigate_patron_disruption')
    sov=next(a for a in D['agreements'] if a['key']=='soviet_industry');mitigation=next(i['mitigation_cost_gdp_share'] for i in D['incidents'] if i['id']=='COLDWAR_NKO_patron_disruption')
    assert abs(m.c['NKO']['v']['treasury']+100*(sov['nko']['setup_gdp_share']+mitigation))<1e-8
    before=m.state();m.call('COLDWAR_NKO_mitigate_patron_disruption');m.call('COLDWAR_NKO_foreign_refresh');assert m.state()==before;cases+=1
    m=Model();m.call('COLDWAR_NKO_offer_civil_atomic_base');m.call('COLDWAR_NKO_foreign_accept_civil_atomic_base','SOV');m.c['NKO']['flags']['COLDWAR_NKO_safeguards_valid']=None
    m.c['NKO']['flags']['COLDWAR_NKO_safeguards_earned']=None;m.call('COLDWAR_NKO_refresh_programmes');m.call('COLDWAR_NKO_offer_npt_offer');m.call('COLDWAR_NKO_foreign_accept_civil_atomic_npt_offer','SOV');money=[m.c[t]['v']['treasury'] for t in ('NKO','SOV')]
    m.call('COLDWAR_NKO_withdraw_safeguards')
    assert 'COLDWAR_NKO_safeguards_programme' not in m.c['NKO']['dm']
    assert all('COLDWAR_NKO_1970_foreign_civil_atomic_npt_offer_'+side not in m.c[tag]['dm'] for tag,side in [('NKO','nko'),('SOV','partner')])
    assert all('COLDWAR_NKO_1970_foreign_civil_atomic_base_'+side in m.c[tag]['dm'] for tag,side in [('NKO','nko'),('SOV','partner')])
    assert [m.c[t]['v']['treasury'] for t in ('NKO','SOV')]==money;cases+=1
    # Due-date event fires once; settling or aggregate debt-zero reconciliation
    # clears the external-credit risk and any temporary arrears penalty.
    m=Model();m.call('COLDWAR_NKO_open_machinery_credit');m.day=731;m.call('COLDWAR_NKO_daily');assert len(m.events)==1
    m.call('COLDWAR_NKO_daily');assert len(m.events)==1;m.call('COLDWAR_NKO_suspend_machinery_repayments');m.c['NKO']['v']['debt']=0;m.call('COLDWAR_NKO_daily')
    assert not any(x in m.c['NKO']['dm'] for x in ('COLDWAR_NKO_credit_default','COLDWAR_NKO_credit_rescheduled','COLDWAR_NKO_machinery_credit_risk'));cases+=1
    # Each political programme retains its earned receipt across loss and return
    # of office; reinstatement must never repeat purchases or construction.
    for group in D['groups']:
        if group['slot'] is None:continue
        n=next(n for n in D['nodes'] if n['group']==group['id'] and n['modifiers'])
        m=Model()
        if n.get('leader_bound'):m.c['NKO']['leader']='Kim Jong-il'
        m.c['NKO']['flags'][n['id']+'_earned']=None;m.c['NKO']['v']['ruling_party']=group['slot'];m.call('COLDWAR_NKO_refresh_programmes');mid=n['id']+'_programme';assert mid in m.c['NKO']['dm']
        m.c['NKO']['v']['ruling_party']=99;m.call('COLDWAR_NKO_refresh_programmes');assert mid not in m.c['NKO']['dm']
        money=m.c['NKO']['v']['treasury'];states=deepcopy(m.s);m.c['NKO']['v']['ruling_party']=group['slot'];m.call('COLDWAR_NKO_refresh_programmes');assert mid in m.c['NKO']['dm'] and m.c['NKO']['v']['treasury']==money and m.s==states;cases+=1
    for date in [(1994,7,7),(1994,7,9)]:
        m=Model();m.date=date;m.call('COLDWAR_NKO_world_succession_daily','SOV');assert not m.events and m.c['NKO']['leader']=='Kim Il Sung';cases+=1
    return cases

def screenshot_regressions():
    cases=0
    for a in D['agreements']:
        for stage in ['base']+[u['key'] for u in a['upgrades']]:
            key=a['key'];partner=a['partner'];m=Model()
            if stage!='base':
                for tag in ('NKO',partner):m.c[tag]['flags'][a['receipts']['accepted']]=None
                m.c['NKO']['flags']['COLDWAR_NKO_safeguards_valid']=None
            send='COLDWAR_NKO_foreign_send_'+key+'_'+stage;pending=a['receipts']['pending'] if stage=='base' else 'COLDWAR_NKO_foreign_'+key+'_'+stage+'_pending'
            m.call(send);assert m.c['NKO']['flags']['COLDWAR_NKO_foreign_cooldown_'+key+'_'+stage]==180
            m.call('COLDWAR_NKO_foreign_decline_'+key+'_'+stage,partner)
            for day in (1,179):
                m.day=day;before=deepcopy((m.c['NKO']['v'],m.c[partner]['v'],m.events));m.call(send)
                assert pending not in m.c[partner]['flags'] and before==(m.c['NKO']['v'],m.c[partner]['v'],m.events)
            m.day=180;m.call(send);assert m.c[partner]['flags'][pending]==270
            assert m.c['NKO']['flags']['COLDWAR_NKO_foreign_cooldown_'+key+'_'+stage]==360;cases+=1
            # Preview calculations must match payment timing: current GDP for
            # a new proposal, saved quotes for its recipient acceptance.
            share_nko=a['nko']['setup_gdp_share'] if stage=='base' else next(u['setup_nko_gdp_share'] for u in a['upgrades'] if u['key']==stage)
            share_partner=a['recipient']['setup_gdp_share'] if stage=='base' else next(u['setup_recipient_gdp_share'] for u in a['upgrades'] if u['key']==stage)
            m.c['NKO']['v']['gdp_total']=200;m.c[partner]['v']['gdp_total']=350
            proposal=deepcopy(m);proposal.call('COLDWAR_NKO_foreign_preview_'+key+'_'+stage)
            acceptance=deepcopy(m);acceptance.call('COLDWAR_NKO_foreign_terms_'+key+'_'+stage)
            for tag,side,share in [('NKO','nko',share_nko),(partner,'recipient',share_partner)]:
                assert abs(proposal.c[tag]['v']['treasury']+m.c[tag]['v']['gdp_total']*share)<1e-8
                assert abs(acceptance.c[tag]['v']['treasury']+100*share)<1e-8
                expected=m.c[tag]['v']['gdp_total']*a[side]['annual_commitment_gdp_share']/52
                assert abs(acceptance.c[tag]['tmp']['COLDWAR_NKO_foreign_weekly_preview']-expected)<1e-8
            cases+=1
    # Each new leader programme rejects the wrong incumbent and wrong party,
    # then pays exactly once with its own negative balance preserved.
    for n in [n for n in D['nodes'] if n['group']=='jongil' and n['key'] not in ('jongil_authority','jongil_cadres','jongil_cabinet','jongil_settlement')]:
        m=Model();m.c['NKO']['v']['treasury']=-2
        for pg in n['prerequisites']:m.c['NKO']['completed'].update(pg)
        complete='COLDWAR_NKO_complete_'+n['key'];before=m.state();m.call(complete);assert m.state()==before
        m.c['NKO']['leader']='Kim Jong-il';m.c['NKO']['v']['ruling_party']=5;before=m.state();m.call(complete);assert m.state()==before
        m.c['NKO']['v']['ruling_party']=4;m.call(complete);assert abs(m.c['NKO']['v']['treasury']+2+100*n['cost_gdp_share'])<1e-8
        assert n['id']+'_programme' in m.c['NKO']['dm'];before=m.state();m.call(complete);assert m.state()==before
        for opposite in n['mutex']:
            before=m.state();m.call('COLDWAR_NKO_complete_'+opposite.removeprefix('COLDWAR_NKO_'));assert m.state()==before
        m.c['NKO']['leader']='Another Leader';m.call('COLDWAR_NKO_refresh_programmes');assert n['id']+'_programme' not in m.c['NKO']['dm'];cases+=1
    # All four complete combinations remain playable through both joins.
    for food in [('jongil_distribution','jongil_priority_inputs'),('jongil_local_markets','jongil_barter_channels')]:
        for priority in ('jongil_kpa_priority','jongil_civilian_recovery'):
            m=Model();m.c['NKO']['leader']='Kim Jong-il'
            for key in ('jongil_authority','jongil_cadres','jongil_settlement','jongil_supply_commission',*food,'jongil_industrial_repair',priority,'jongil_recovery_accounts'):
                m.call('COLDWAR_NKO_complete_'+key);assert 'COLDWAR_NKO_'+key+'_earned' in m.c['NKO']['flags'],key
                m.c['NKO']['completed'].add('COLDWAR_NKO_'+key)
            cases+=1
    # Screenshot regression: every displayed presidency condition is fulfilled
    # in 1970, so a historical date must not silently block the start/reward.
    for party,leader,prerequisite,expected in [
      (4,'Kim Il Sung',True,True),(5,'Kim Il Sung',True,False),
      (4,'Another Leader',True,False),(4,'Kim Il Sung',False,False)]:
        m=Model();m.date=(1970,1,1);m.c['NKO']['v']['ruling_party']=party;m.c['NKO']['leader']=leader
        if prerequisite:m.c['NKO']['completed'].add('COLDWAR_NKO_loyalty')
        assert m.trigger(T['COLDWAR_NKO_can_presidency'],('NKO','NKO','NKO','NKO'))==expected
        m.call('COLDWAR_NKO_complete_presidency')
        assert ('COLDWAR_NKO_presidency_earned' in m.c['NKO']['flags'])==expected
        assert ('COLDWAR_NKO_presidency_programme' in m.c['NKO']['dm'])==expected
        before=m.state();m.call('COLDWAR_NKO_complete_presidency');assert m.state()==before
        cases+=1
    return cases

def expansion_lifecycles():
    # Exercise every new executor, including party departure, actual membership
    # spirits, recipient consent and suspension of dependent domestic benefits.
    cases=0
    additions=D['nodes'][-D['amendments']['national_expansion_focuses']:]
    assert len(additions)==162
    agreements={a['key']:a for a in D['agreements']}
    def fixture(n):
        m=Model();m.date=(1995,1,1)
        m.c['NKO']['v']['ruling_party']=n['slot'] if n['slot'] is not None else 4
        if n.get('leader_bound'):m.c['NKO']['leader']='Kim Jong-il'
        for pg in n['prerequisites']:m.c['NKO']['completed'].add(pg[0])
        guards=n.get('eligibility_notes',[])+n.get('policy_enable_guards',[])+n.get('availability_guards',[])
        for guard in guards:
            for flag in re.findall(r'has_country_flag\s*=\s*(COLDWAR_NKO_\w+)',guard):m.c['NKO']['flags'][flag]=None
        for key in n.get('required_agreements',[]):
            a=agreements[key];m.call('COLDWAR_NKO_offer_'+key+'_base')
            m.call('COLDWAR_NKO_foreign_accept_'+key+'_base',a['partner'])
            assert m.trigger(T['COLDWAR_NKO_has_agreement_'+key],('NKO','NKO','NKO','NKO')),n['id']
        m.c['NKO']['v']['treasury']=-5.
        return m
    def resources(m):
        return deepcopy(([(tag,c['v']['treasury'],c.get('research',[])) for tag,c in m.c.items()],m.s,m.events))
    for n in additions:
        key=n['key'];complete='COLDWAR_NKO_complete_'+key;can='COLDWAR_NKO_can_'+key
        receipt=n['id']+'_earned';mid=n['id']+'_programme';m=fixture(n)
        assert m.trigger(T[can],('NKO','NKO','NKO','NKO')),('expansion fixture cannot start',key)
        wrong=deepcopy(m);before=wrong.state();events=deepcopy(wrong.events);wrong.call(complete,'SOV')
        assert wrong.state()==before and wrong.events==events,('wrong country reward',key);cases+=1
        if n['cost_gdp_share'] or any(e['kind']=='agreement' for e in n['extra']):
            zero=deepcopy(m);zero.c['NKO']['v']['gdp_total']=0;before=zero.state();zero.call(complete)
            assert zero.state()==before,('invalid GDP reward',key);cases+=1
        if n['slot'] is not None:
            wrong=deepcopy(m);wrong.c['NKO']['v']['ruling_party']=99;before=wrong.state();wrong.call(complete)
            assert wrong.state()==before,('wrong party reward',key);cases+=1
        for akey in n.get('required_agreements',[]):
            absent=deepcopy(m)
            absent.c['NKO']['dm']={spirit for spirit in absent.c['NKO']['dm'] if not spirit.startswith('COLDWAR_NKO_1970_foreign_'+akey+'_')}
            assert not absent.trigger(T[can],('NKO','NKO','NKO','NKO')),('receipt without membership allowed',key,akey)
            before=absent.state();absent.call(complete);assert absent.state()==before
            absent.call('COLDWAR_NKO_foreign_refresh');assert absent.trigger(T[can],('NKO','NKO','NKO','NKO'));cases+=1
        m.call(complete)
        assert receipt in m.c['NKO']['flags'],('missing expansion reward',key)
        assert abs(m.c['NKO']['v']['treasury']+5+100*n['cost_gdp_share'])<1e-8,('expansion GDP price',key)
        if n['modifiers']:assert mid in m.c['NKO']['dm'],('missing expansion spirit',key)
        before=m.state();events=deepcopy(m.events);m.call(complete)
        assert m.state()==before and m.events==events,('replayed expansion reward',key);cases+=1
        if n['slot'] is not None and n['modifiers']:
            snapshot=resources(m);m.c['NKO']['v']['ruling_party']=99;m.call('COLDWAR_NKO_refresh_programmes')
            assert mid not in m.c['NKO']['dm'],('departed party retains expansion spirit',key)
            m.c['NKO']['v']['ruling_party']=n['slot'];m.call('COLDWAR_NKO_refresh_programmes')
            assert mid in m.c['NKO']['dm'] and resources(m)==snapshot,('party return replays reward',key);cases+=1
        for akey in n.get('required_agreements',[]):
            if not n['modifiers']:continue
            partner=agreements[akey]['partner']
            for kind in ('war','sanction'):
                suspended=deepcopy(m);snapshot=resources(suspended)
                if kind=='war':suspended.wars.add(frozenset(('NKO',partner)))
                else:suspended.c[partner]['arrays']['imp_eco_sanc_by_us']={'NKO'}
                suspended.call('COLDWAR_NKO_foreign_refresh')
                assert mid not in suspended.c['NKO']['dm'],('dependent benefit survives suspension',key,akey,kind)
                if kind=='war':suspended.wars.clear()
                else:suspended.c[partner]['arrays'].clear()
                suspended.call('COLDWAR_NKO_foreign_refresh')
                assert mid in suspended.c['NKO']['dm'] and resources(suspended)==snapshot,('resumption replays reward',key,akey,kind);cases+=1
        if 'has_country_flag = COLDWAR_NKO_safeguards_valid' in n.get('policy_enable_guards',[]):
            snapshot=resources(m);m.c['NKO']['flags'].pop('COLDWAR_NKO_safeguards_valid');m.call('COLDWAR_NKO_refresh_programmes')
            assert mid not in m.c['NKO']['dm'],('safeguards withdrawal keeps benefit',key)
            m.c['NKO']['flags']['COLDWAR_NKO_safeguards_valid']=None;m.call('COLDWAR_NKO_refresh_programmes')
            assert mid in m.c['NKO']['dm'] and resources(m)==snapshot;cases+=1
        for e in n['extra']:
            if e['kind']!='agreement':continue
            a=agreements[e['agreement']];partner=a['partner'];pending=a['receipts']['pending']
            assert n['cost_gdp_share']==0 and pending in m.c[partner]['flags'],('proposal charged before consent',key)
            beforemoney={tag:m.c[tag]['v']['treasury'] for tag in ('NKO',partner)}
            m.call('COLDWAR_NKO_foreign_accept_'+a['key']+'_base',partner)
            for tag,side in [('NKO','nko'),(partner,'recipient')]:
                assert abs(m.c[tag]['v']['treasury']-beforemoney[tag]+100*a[side]['setup_gdp_share'])<1e-8,('accepted proposal price',key,tag)
            snapshot=resources(m);m.call('COLDWAR_NKO_foreign_accept_'+a['key']+'_base',partner)
            assert resources(m)==snapshot,('new agreement acceptance replay',key);cases+=1
    return cases

if __name__=='__main__':
    rebuild=None
    if '--check-rebuild' in sys.argv:
        manifest=ROOT/'tools/north_korea_1970/emission_manifest.json'
        before=json.loads(manifest.read_text(encoding='utf-8'))
        expected={rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in before['root_outputs']}
        assert expected==before['output_sha256'],'Manifest does not match installed content'
        subprocess.run([sys.executable,str(ROOT/'tools/north_korea_1970/compile.py')],cwd=ROOT,check=True,capture_output=True,text=True)
        after=json.loads(manifest.read_text(encoding='utf-8'))
        assert before==after,'Rebuild changed installed output'
        assert expected=={rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in after['root_outputs']}
        rebuild='byte-identical'
    keys=structural();count=transactions()+domestic_and_succession()+additional_lifecycles()+screenshot_regressions()+expansion_lifecycles()
    report={'focuses':len(D['nodes']),'script_files':len(FILES),'localized_keys':keys,'source_transaction_cases':count,'structural':'pass','encoding':'pass','engine_tested':False}
    if rebuild:report['rebuild']=rebuild
    (ROOT/'docs/COLDWAR_NKO_1970_concept/implementation_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))
