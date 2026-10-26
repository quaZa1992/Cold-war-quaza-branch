# IMPERIA CW — Cold War: independent emitted South Korean runtime checks.
"""Validate loaded/staged scripts; source tests are not an HOI4 engine run."""
from pathlib import Path
from collections import Counter
from copy import deepcopy
import argparse,hashlib,json,re,sys

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];DOC=ROOT/'docs/design/COLDWAR_KOR_1970'
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,first,values,walk
from COLDWAR_KOR_alliance_revision import load_design
P='COLDWAR_KOR_'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--installed',action='store_true');args=ap.parse_args()
    base=ROOT if args.installed else HERE/'runtime_staged'
    d=load_design()
    manifest=json.loads((DOC/'COLDWAR_KOR_runtime_manifest.json').read_text(encoding='utf-8'))
    errors=[];notes=[]
    def ck(ok,msg):
        if not ok:errors.append(msg)
    parsed={};blobs={}
    for rel,digest in manifest['files'].items():
        path=base/rel;ck(path.exists(),'missing output '+rel)
        if not path.exists():continue
        blob=path.read_bytes();blobs[rel]=blob
        ck(hashlib.sha256(blob).hexdigest()==digest,'changed after emission '+rel)
        if rel.endswith('.yml'):
            ck(blob.startswith(b'\xef\xbb\xbf'),'localisation BOM missing '+rel);continue
        ck(not blob.startswith(b'\xef\xbb\xbf'),'script BOM '+rel)
        try:parsed[rel]=parse(blob.decode('utf-8'))
        except Exception as e:errors.append('parse '+rel+': '+str(e))
        ck(not re.search(rb'(?m)^\s*_(bare|list)\s*=',blob),'parser sentinel leaked '+rel)
        if '/COLDWAR_KOR_' in '/'+rel:
            ck(not re.search(rb'\b\d+\.\d{6,}\b',blob),'fixed-point literal precision '+rel)
        elif re.search(rb'\b\d+\.\d{6,}\b',blob):
            notes.append('Existing native long literals outside Korean additions preserved: '+rel)
    treepath='common/national_focus/COLDWAR_KOR_1970_focus.txt'
    tree=first(parsed.get(treepath,[]),'focus_tree',[])
    foci=values(tree,'focus');by={first(n,'id'):n for n in foci};expected={n['id']:n for n in d['nodes']}
    ck(len(by)==len(foci)==len(d['nodes'])<=300,'focus definition count/uniqueness/cap')
    ck(set(by)==set(expected),'approved focus IDs changed')
    ck(len(values(tree,'shortcut'))==8,'shortcut capacity/count')
    ck(first(first(tree,'initial_show_position',[]),'focus')==d['layout']['initial_focus'],'initial camera')
    E={};T={};DM={};IDEA={};sprites={};events={};paths={};decisions={};categories=set();used_categories=set()
    for rel,rows in parsed.items():
        if '/COLDWAR_KOR_' not in '/'+rel:continue
        target=E if '/scripted_effects/' in '/'+rel else T if '/scripted_triggers/' in '/'+rel else DM if '/dynamic_modifiers/' in '/'+rel else None
        if target is not None:
            for k,op,v in rows:
                ck(k not in target,'duplicate definition '+k)
                ck(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*',k) is not None,'invalid top-level identifier '+k)
                target[k]=v;paths[k]=rel
        if '/ideas/' in '/'+rel:
            for k,op,v in first(first(rows,'ideas',[]),'country',[]):
                ck(k not in IDEA,'duplicate idea '+k);IDEA[k]=v;paths[k]=rel
        if rel.startswith('common/decisions/') and '/categories/' not in rel:
            for category,o,body in rows:
                used_categories.add(category)
                for key,o,decision in body:
                    if not isinstance(decision,list):continue
                    ck(key not in decisions,'duplicate decision '+key);decisions[key]=decision
        if rel.startswith('common/decisions/categories/'):
            categories.update(k for k,o,v in rows)
        if rel.endswith('.gfx'):
            for b in values(first(rows,'spriteTypes',[]),'spriteType'):
                name=first(b,'name','').strip('"');sprites[name]=first(b,'texturefile','').strip('"')
        if rel.startswith('events/'):
            declared=set(values(rows,'add_namespace'))
            for b in values(rows,'country_event')+values(rows,'news_event'):
                id=first(b,'id');ck(id not in events,'duplicate event '+str(id));events[id]=b;paths[id]=rel
                ck(bool(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*\.\d+',id or '')),'invalid event ID '+str(id))
                ck(id.split('.')[0] in declared,'undeclared event namespace '+str(id))
                ck(first(b,'is_triggered_only')=='yes' or bool(first(b,'trigger',[])),'unscoped automatic event '+str(id))
    for id,body in DM.items():
        ck(not any(k in ('modifier','allowed','removal_cost') for k,op,v in body),'idea shape in dynamic modifier '+id)
        ck(first(body,'enable') is not None,'dynamic modifier has no live enable '+id)
    ck(not (used_categories-categories),'unregistered decision categories: '+', '.join(sorted(used_categories-categories)))
    loc={}
    for rel,blob in blobs.items():
        if not rel.endswith('.yml'):continue
        lines=blob.decode('utf-8-sig').splitlines();ck(lines[0]=='l_english:','wrong language '+rel)
        for line in lines:
            m=re.match(r'\s+([^\s:#]+):\d+\s+"(.*)"\s*$',line)
            if m:
                ck(m[1] not in loc,'duplicate localisation '+m[1]);loc[m[1]]=m[2]
    def resolve(id,trail=()):
        ck(id not in trail,'cyclic anchor '+id)
        n=by[id];xy=[int(first(n,'x','0')),int(first(n,'y','0'))];anchor=first(n,'relative_position_id')
        if anchor:
            ck(anchor in by,'missing anchor '+anchor)
            if anchor in by:a=resolve(anchor,trail+(id,));xy=[xy[0]+a[0],xy[1]+a[1]]
        return xy
    for id in sorted(decisions):
        ck(id in loc,'missing decision name '+id)
        ck(id+'_desc' in loc,'missing decision description '+id)
    for id in sorted(categories):
        ck(id in loc,'missing decision category name '+id)
        ck(id+'_desc' in loc,'missing decision category description '+id)
    # Native routing checks remain executable, but none may leak through a
    # scripted-trigger expansion into a focus/decision/option tooltip.
    def check_routing_hidden(rows,where,hidden=False):
        for k,o,v in rows:
            technical=k in ('tag','original_tag','IMP_is_1970_scenario') or (k=='has_country_flag' and v==P+'initialized')
            if technical:ck(hidden,'visible initialization/routing check in '+where)
            if isinstance(v,list):check_routing_hidden(v,where,hidden or k=='hidden_trigger')
    for id,body in T.items():check_routing_hidden(body,id)
    for id,body in DM.items():check_routing_hidden(first(body,'enable',[]),id)
    for id,n in expected.items():
        if id not in by:continue
        b=by[id]
        ck(resolve(id)==n['xy'],'geometry changed '+id)
        ck([values(x,'focus') for x in values(b,'prerequisite')]==n['prerequisites'],'prerequisite groups changed '+id)
        ck(set(values(first(b,'mutually_exclusive',[]),'focus'))==set(n['mutually_exclusive']),'exclusions changed '+id)
        ck(abs(float(first(b,'cost'))-n['days']/7)<1e-5,'duration changed '+id)
        ck(first(b,'icon') in sprites,'unregistered focus icon '+id)
        ck(id in loc and id+'_desc' in loc,'focus localisation missing '+id)
        reward=first(b,'completion_reward',[])
        ck(first(reward,'effect_tooltip') is not None and first(reward,'hidden_effect') is not None,'preview/execution not separated '+id)
        helper=P+'complete_'+n['key'];body=E.get(helper,[])
        ck(bool(body),'missing completion '+id)
        guard=first(first(body,'if',[]),'limit',[])
        ck(any(k=='NOT' and ('has_country_flag','=',id+'_paid') in v for k,o,v in guard),'missing once-only guard '+id)
        ck((P+'can_'+n['key'],'=','yes') in guard,'runtime gate missing '+id)
        for p in n['effects']['policies']:
            idea=IDEA.get(id+'_preview',[])
            preview={k:float(v) for k,o,v in first(idea,'modifier',[]) if not isinstance(v,list)}
            ck(preview==p['modifiers'],'visible policy coefficients changed '+id)
            dynamic=DM.get(id+'_programme',[])
            native_vars={k:v for k,o,v in dynamic if k not in ('icon','enable')}
            wanted={k:id+'_'+p['slot']+'_'+k for k in p['modifiers']}
            ck(native_vars==wanted,'modifier variables lack consumer '+id)
            assignments={k:v for k,o,v in walk(body) if o=='=' and not isinstance(v,list)}
            for k,v in p['modifiers'].items():ck(str(v)==assignments.get(wanted[k]) or float(assignments.get(wanted[k],'nan'))==v,'wrong policy assignment '+id+' '+k)
    # Resolve new transitive symbols, options and texture references.
    used_effects=set();used_triggers=set();reference_count=0
    for rel,rows in parsed.items():
        if '/COLDWAR_KOR_' not in '/'+rel:continue
        for k,op,v in walk(rows):
            if k.startswith(P) and v in ('yes','no') if isinstance(v,str) else False:
                reference_count+=1;ck(k in E or k in T,'undefined Korean helper '+k+' in '+rel)
            if k in ('country_event','news_event','state_event') and isinstance(v,list):
                id=first(v,'id')
                if id and id.startswith(P):ck(id in events,'undefined event '+id+' in '+rel)
            if k in ('add_dynamic_modifier','remove_dynamic_modifier','has_dynamic_modifier') and isinstance(v,list):
                id=first(v,'modifier')
                if id and id.startswith(P):ck(id in DM,'undefined dynamic modifier '+id)
            if k=='add_dynamic_modifier' and isinstance(v,str):ck(False,'scalar dynamic modifier addition '+rel)
            if k=='remove_dynamic_modifier' and isinstance(v,str):ck(False,'scalar dynamic modifier removal '+rel)
            if k=='add_timed_idea' and isinstance(v,list):
                id=first(v,'idea')
                if id and id.startswith(P):ck(id in IDEA,'undefined timed idea '+id)
            if k=='add_ideas' and isinstance(v,str) and v.startswith(P):ck(v in IDEA,'undefined idea '+v)
            if k in ('title','desc','name','tooltip','not_tooltip','custom_effect_tooltip') and isinstance(v,str) and v.startswith(P):
                ck(v in loc,'missing English text '+v+' in '+rel)
            if k=='set_politics' and isinstance(v,list):
                ruling=first(v,'ruling_party');ck(ruling is not None and not str(ruling).isdigit(),'invalid engine ideology '+rel)
            if k=='picture' and isinstance(v,str) and v.strip('"').startswith('gfx/'):
                ck((ROOT/v.strip('"')).exists(),'missing portrait '+v)
    for sprite,texture in sprites.items():ck((ROOT/texture).exists(),'missing texture '+texture)
    writes=set();reads=set()
    for rows in parsed.values():
        for k,o,v in walk(rows):
            if k=='set_country_flag':writes.add(v if isinstance(v,str) else first(v,'flag'))
            if k=='has_country_flag' and isinstance(v,str) and v.startswith(P):reads.add(v)
    ck(not (reads-writes),'Korean flags have no provider: '+', '.join(sorted(reads-writes)))
    # Policy traits and weekly accounting must connect to real native readers.
    money=blobs.get('common/scripted_effects/00_money_system.txt',b'').decode('utf-8')
    ck('COLDWAR_KOR_add_weekly_programme_cost = yes' in money and 'COLDWAR_KOR_contract_expenses = yes' in money,'weekly expenses unhooked')
    ck('COLDWAR_KOR_contract_income = yes' in money,'weekly contract income unhooked')
    history=blobs.get('history/countries/KOR - Korea.txt',b'').decode('utf-8')
    ck('load_focus_tree = COLDWAR_KOR_1970_focus' in history,'1970 history tree not installed')
    ck('name = "Park Chung Hee"' in history,'historical starting leader changed')
    ck('COLDWAR_KOR_1970_set_leader = yes' in blobs.get('common/scripted_effects/00_leader_setup_scripted_effects.txt',b'').decode('utf-8'),'native leader routing missing')
    ck('COLDWAR_KOR_sync_politics = yes' in blobs.get('common/scripted_effects/00_MD_politicsview_scripted_effects.txt',b'').decode('utf-8'),'exact-party hook missing')
    # Borrowing must not be blocked by new own-spending cash gates.
    for id,body in T.items():
        ck(not any(k in ('treasury','cash') for k,o,v in walk(body)),'new own-spending treasury gate '+id)
    # Pending referendum/court provider and normal continuation checks.
    ck(P+'calculate_charter_vote' in E,'ballot arithmetic not defined')
    ck(P+'on_native_election_resolved' in E,'election-result provider not defined')
    ck(any(k=='set_country_flag' and v==P+'election_resolution_pending' for b in E.values() for k,o,v in walk(b)),'no pending election setter')
    for n in d['nodes']:
        for a in n['effects']['actions']:
            if a['type']=='action':ck(P+'action_'+a['value'] in E,'missing action implementation '+a['value'])
            if a['type']=='offer':ck(P+'send_'+a['value'] in E,'missing bilateral sender '+a['value'])
    # Independent core execution model tests emitted guards/leaves/consumers.
    model=CoreModel(E,T)
    model.execute(E[P+'complete_chaebol_compact'])
    model.execute(E[P+'complete_export_targets'])
    model.execute(E[P+'calculate_weekly_cost'])
    ck(abs(model.v.get(P+'weekly_cost',0)-.004)<1e-8,'terminal policy expense does not replace prior level')
    paid_snapshot=(model.cash,deepcopy(model.buildings),model.grants)
    model.execute(E[P+'complete_export_targets']);ck(paid_snapshot==(model.cash,model.buildings,model.grants),'completion replay pays again')
    model.party=1;model.execute(E[P+'refresh_programmes']);model.execute(E[P+'calculate_weekly_cost'])
    ck(model.v.get(P+'weekly_cost',0)==0,'departed owner still billed')
    ck(not any('chaebol_compact_programme' in x or 'export_targets_programme' in x for x in model.dm),'departed owner modifier retained')
    model.party=0;model.execute(E[P+'refresh_programmes']);model.execute(E[P+'calculate_weekly_cost'])
    ck(abs(model.v.get(P+'weekly_cost',0)-.004)<1e-8,'returning owner does not resume cost')
    ck(paid_snapshot==(model.cash,model.buildings,model.grants),'returning owner repeats one-time payout')
    model.cash=0;model.execute(E[P+'complete_pohang_foundry'])
    ck(model.cash<0,'native borrowing disallowed from zero cash')
    shot=(model.cash,deepcopy(model.buildings));model.execute(E[P+'complete_pohang_foundry']);ck(shot==(model.cash,model.buildings),'paid construction replay')
    report={'status':'PASS' if not errors else 'FAIL','target':'installed' if args.installed else 'staged','focuses':len(foci),'scripted_effects':len(E),'scripted_triggers':len(T),'dynamic_modifiers':len(DM),'ideas':len(IDEA),'events':len(events),'sprites':len(sprites),'english_keys':len(loc),'new_helper_references':reference_count,'errors':errors,'notes':notes,'scope':'Source AST/graph/reference/API shape and bounded emitted-effect model; not an HOI4 engine, tooltip, multiplayer or save test','approved_design_sha256':manifest['approved_design_sha256']}
    (DOC/'COLDWAR_KOR_runtime_validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))
    if errors:raise SystemExit(1)

class CoreModel:
    """Small fail-closed interpreter for core policy scenarios used above."""
    def __init__(self,e,t):
        self.e=e;self.t=t;self.v={};self.flags={P+'initialized'};self.dm=set();self.party=0;self.leader='Park Chung Hee';self.cash=100.;self.tmp={};self.buildings={};self.grants=0
    def value(self,v):
        try:return float(v)
        except (TypeError,ValueError):return self.tmp.get(v,self.v.get(v,0))
    def trigger(self,rows):
        result=[]
        for k,op,v in rows:
            if k in self.t:r=self.trigger(self.t[k])==(v=='yes')
            elif k in ('AND','hidden_trigger'):r=self.trigger(v)
            elif k=='custom_trigger_tooltip':r=self.trigger([x for x in v if x[0] not in ('tooltip','not_tooltip')])
            elif k=='OR':r=any(self.trigger([x]) for x in v)
            elif k=='NOT':r=not self.trigger(v)
            elif k in ('original_tag','tag'):r=v=='KOR'
            elif k=='IMP_is_1970_scenario':r=v=='yes'
            elif k=='is_subject':r=v=='no'
            elif k=='has_country_flag':r=v in self.flags
            elif k=='has_country_leader':r=first(v,'name').strip('"')==self.leader
            elif k=='has_dynamic_modifier':r=first(v,'modifier') in self.dm
            elif k=='check_variable':
                a,cmp,b=v[0];lhs=self.party if a=='ruling_party' else self.value(a);rhs=self.value(b)
                r={'=':lhs==rhs,'>':lhs>rhs,'<':lhs<rhs,'>=':lhs>=rhs,'<=':lhs<=rhs}[cmp]
            elif k.isdigit():r=self.trigger(v)
            elif k in ('is_owned_by','is_controlled_by'):r=v=='ROOT'
            elif k=='free_building_slots':r=True
            elif k=='has_elections':r=True
            else:raise ValueError('Unmodelled core trigger '+k)
            result.append(r)
            if not r:return False
        return all(result)
    def execute(self,rows):
        previous=False
        for k,op,v in rows:
            if k=='if':
                previous=self.trigger(first(v,'limit',[]))
                if previous:self.execute([r for r in v if r[0]!='limit'])
            elif k=='else':
                if not previous:self.execute(v)
                previous=False
            elif k=='else_if':
                if not previous:
                    previous=self.trigger(first(v,'limit',[]))
                    if previous:self.execute([r for r in v if r[0]!='limit'])
            elif k in self.e:self.execute(self.e[k])
            elif k=='set_variable':
                a,_,b=v[0];self.v[a]=self.value(b)
            elif k=='add_to_variable':
                a,_,b=v[0];self.v[a]=self.v.get(a,0)+self.value(b)
            elif k=='set_temp_variable':
                a,_,b=v[0];self.tmp[a]=self.value(b)
            elif k=='modify_treasury_effect':self.cash+=self.tmp['treasury_change']
            elif k=='set_country_flag':self.flags.add(v if isinstance(v,str) else first(v,'flag'))
            elif k=='clr_country_flag':self.flags.discard(v)
            elif k=='add_dynamic_modifier':self.dm.add(first(v,'modifier'))
            elif k=='remove_dynamic_modifier':self.dm.discard(first(v,'modifier'))
            elif k.isdigit():
                for kind,o,b in v:
                    if kind=='add_building_construction':
                        target=(k,first(b,'type'));self.buildings[target]=self.buildings.get(target,0)+int(first(b,'level'))
                    else:raise ValueError('Unmodelled state effect '+kind)
            elif k in ('hidden_effect',):self.execute(v)
            elif k=='effect_tooltip':continue
            elif k in ('add_political_power','add_stability','add_war_support','army_experience'):self.grants+=1
            elif k in ('force_update_dynamic_modifier','custom_effect_tooltip'):continue
            else:raise ValueError('Unmodelled core effect '+k)

if __name__=='__main__':main()
