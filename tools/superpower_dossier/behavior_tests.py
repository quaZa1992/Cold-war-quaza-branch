# IMPERIA COLD WAR — Execute emitted dossier AST against bounded observer fixtures
"""Source behaviour model, not the native engine or a multiplayer simulation."""
import copy
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools/spain_1970_v2'))
spec=importlib.util.spec_from_file_location('audit',ROOT/'tools/multiplayer_quality/audit.py')
parser=importlib.util.module_from_spec(spec);spec.loader.exec_module(parser)
from runtime import COLS


class Model:
    def __init__(self):
        self.tags={'USA':1,'SOV':2,'EGY':3,'ISR':4,'CHI':5}
        self.v={k:{} for k in ('global',*self.tags)}
        self.a={k:{} for k in self.v};self.flags={k:set() for k in self.v}
        self.intel={};self.network={};self.queries=0;self.date=100;self.temp={}
        self.camera=[]
        self.effects={k:b for k,o,b in parser.parse((ROOT/'common/scripted_effects/ICW_superpower_dossier.txt').read_text())}
        self.triggers={k:b for k,o,b in parser.parse((ROOT/'common/scripted_triggers/ICW_superpower_dossier.txt').read_text())}
        for k in self.tags:self.v[k]['treasury']=1000

    def owner(self,key,ctx):
        if key.startswith(('global.','USA.','SOV.','EGY.','ISR.','CHI.','ROOT.','PREV.','THIS.')):
            prefix,key=key.split('.',1)
            return ({'ROOT':ctx[2],'PREV':ctx[1],'THIS':ctx[0]}.get(prefix,prefix)),key
        return ctx[0],key

    def index(self,key,ctx):
        for token,value in [('THIS',ctx[0]),('PREV',ctx[1]),('ROOT',ctx[2])]:
            key=key.replace('@'+token,'@'+str(value))
        return key

    def value(self,key,ctx):
        if isinstance(key,(int,float)):return key
        if key in ('date','global.date'):return self.date
        try:return float(key)
        except ValueError:pass
        if key.endswith('.id'):
            tag=key[:-3];tag={'THIS':ctx[0],'PREV':ctx[1],'ROOT':ctx[2]}.get(tag,tag)
            return self.tags.get(tag,0)
        owner,key=self.owner(key,ctx);key=self.index(key,ctx)
        if '^' in key:
            array,index=key.split('^',1);items=self.a[owner].get(array,[])
            if index=='num':return len(items)
            i=int(self.value(index,ctx));return items[i] if 0<=i<len(items) else 0
        return self.v[owner].get(key,self.temp.get(key,0))

    def country(self,key,ctx):
        if key.startswith('var:'):
            ident=self.value(key[4:],ctx)
            return next((k for k,v in self.tags.items() if v==ident),None)
        return {'THIS':ctx[0],'PREV':ctx[1],'ROOT':ctx[2]}.get(key,key)

    def compare(self,a,b,op):
        return {'=':a==b,'>':a>b,'<':a<b,'greater_than_or_equals':a>=b,'less_than_or_equals':a<=b}[op]

    def test(self,rows,ctx):
        return all(self.predicate(k,o,b,ctx) for k,o,b in rows)

    def predicate(self,k,o,b,ctx):
        if k in ('AND','limit'):return self.test(b,ctx)
        if k=='OR':return any(self.predicate(*r,ctx) for r in b)
        if k=='NOT':return not self.test(b,ctx)
        if k in self.triggers:return self.test(self.triggers[k],ctx)
        if k=='IMP_is_1970_scenario':return True
        if k=='check_variable':
            if b[0][0]=='var':
                fields=dict((k,v) for k,o,v in b)
                return self.compare(self.value(fields['var'],ctx),self.value(fields['value'],ctx),fields['compare'])
            a,op,v=b[0];return self.compare(self.value(a,ctx),self.value(v,ctx),op)
        if k in ('exists','always'):return b=='yes'
        if k=='capital_scope':return self.test(b,('capital:'+str(ctx[0]),ctx[0],ctx[2]))
        if k=='is_owned_by':return ctx[0]=='capital:'+str(self.country(b,ctx))
        if k=='is_ai':return b=='no'
        if k=='tag':return ctx[0]==self.country(b,ctx)
        if k=='country_exists':return b in self.tags
        if k in ('has_country_flag','has_global_flag'):
            return b in self.flags['global' if k=='has_global_flag' else ctx[0]]
        if k=='has_variable':return self.value(b,ctx)!=0
        if k in ('intel_level_over','network_strength'):
            self.queries+=1;fields=dict((k,v) for k,o,v in b)
            target=self.country(fields['target'],ctx)
            threshold=next((v for n,o,v in b if n!='target'),0)
            table=self.intel if k=='intel_level_over' else self.network
            return table.get((ctx[0],target),0)>float(threshold)
        if k.startswith('var:') or k in ('USA','SOV','EGY','ISR','CHI','ROOT','PREV'):
            tag=self.country(k,ctx)
            return bool(tag) and self.test(b,(tag,ctx[0],ctx[2]))
        if k in ('is_lend_leasing','has_volunteers_amount_from','has_attache_from','has_country_flag','is_in_array'):return False
        raise AssertionError(('Unsupported predicate',k,b))

    def call(self,name,tag='USA',root=None):self.run(self.effects[name],(tag,tag,root or tag))

    def run(self,rows,ctx):
        previous=None
        for k,o,b in rows:
            if k in ('if','else_if','else'):
                if k=='if':previous=False
                take=not previous and (k=='else' or self.test(next(v for n,o,v in b if n=='limit'),ctx))
                if take:self.run([r for r in b if r[0]!='limit'],ctx);previous=True
                continue
            if k in self.effects:self.run(self.effects[k],ctx);continue
            if k in ('set_variable','add_to_variable','subtract_from_variable','divide_variable','set_temp_variable','add_to_temp_variable','subtract_from_temp_variable'):
                key,op,value=b[0];owner,key=self.owner(key,ctx);key=self.index(key,ctx);val=self.value(value,ctx)
                table=self.temp if '_temp_' in k else self.v[owner]
                if k.startswith('add'):val=table.get(key,0)+val
                elif k.startswith('subtract'):val=table.get(key,0)-val
                elif k.startswith('divide'):val=table.get(key,0)/val
                table[key]=val;continue
            if k in ('clear_variable','clear_array'):
                owner,key=self.owner(b,ctx);key=self.index(key,ctx)
                (self.v if k=='clear_variable' else self.a)[owner].pop(key,None);continue
            if k=='add_to_array':
                key,o,val=b[0];owner,key=self.owner(key,ctx)
                self.a[owner].setdefault(key,[]).append(self.value(val,ctx));continue
            if k=='remove_from_array':
                fields=dict((k,v) for k,o,v in b);owner,key=self.owner(fields['array'],ctx)
                self.a[owner][key].pop(int(self.value(fields['index'],ctx)));continue
            if k in ('set_country_flag','clr_country_flag','set_global_flag'):
                flags=self.flags['global' if k=='set_global_flag' else ctx[0]]
                if k=='clr_country_flag':flags.discard(b)
                else:flags.add(b)
                continue
            if k in ('for_each_loop','for_each_scope_loop'):
                fields=dict((k,v) for k,o,v in b if k in ('array','index','value'));owner,key=self.owner(fields['array'],ctx)
                for i,val in enumerate(list(self.a[owner].get(key,[]))):
                    self.temp[fields.get('index','i')]=i;self.temp[fields.get('value','v')]=val
                    if k=='for_each_scope_loop':
                        tag=next((k for k,v in self.tags.items() if v==val),None)
                        self.run([r for r in b if r[0] not in fields],(tag,ctx[0],ctx[2]))
                    else:self.run([r for r in b if r[0] not in fields],ctx)
                continue
            if k=='for_loop_effect':
                fields=dict((k,v) for k,o,v in b if not isinstance(v,list))
                for i in range(int(fields.get('start',0)),int(fields['end'])):
                    self.temp[fields.get('value','v')]=i;self.run([r for r in b if r[0] not in fields],ctx)
                continue
            if k=='while_loop_effect':
                limit=next(v for n,o,v in b if n=='limit');count=0
                while self.test(limit,ctx):
                    count+=1;assert count<1000,'Unbounded emitted loop'
                    self.run([r for r in b if r[0]!='limit'],ctx)
                continue
            if k=='every_country':
                for tag in self.tags:
                    scope=(tag,ctx[0],ctx[2]);limit=next(v for n,o,v in b if n=='limit')
                    if self.test(limit,scope):self.run([r for r in b if r[0]!='limit'],scope)
                continue
            if k=='capital_scope':self.run(b,('capital:'+str(ctx[0]),ctx[0],ctx[2]));continue
            if k=='goto_state':self.camera.append(ctx[0]);continue
            if k in self.tags or k.startswith('var:'):
                tag=self.country(k,ctx)
                if tag:self.run(b,(tag,ctx[0],ctx[2]))
                continue
            raise AssertionError(('Unsupported effect',k,b))

    def packet(self,**values):
        self.call('icsd_reset_observation')
        for k,v in values.items():self.v['global']['icsd_t_'+k]=v


def main():
    checks=[]
    def check(value,label):
        assert value,label
        checks.append(label)
    from test_treaties import TreatyModel
    m=TreatyModel()
    def rows(tag,kind='mail'):return m.a[tag].get('icsd_'+kind+'_kind',[])
    def payment(state=2):
        m.packet(actor=1,target=3,kind=7,state=state,amount=0.5)
        m.call('icsd_publish_mail')
    payment(1);payment(2)
    check(rows('USA')==[7,7] and not rows('SOV'),'Own proposals/payments visible; undiscovered rival payment absent')
    m.network['SOV','EGY']=50
    m.call('icsd_build_view','SOV')
    check(not rows('SOV'),'Later network does not reconstruct old payments')
    payment()
    check(rows('SOV')==[7] and m.a['SOV']['icsd_mail_amount']==[0.5],'Fresh payment discovered using the native target-network predicate')
    check(not any(k.startswith('icsd_t_') for k in m.v['global']),'Synchronous packet cleared after both observers')
    m.network.clear();m.intel['SOV','USA']=0.6;payment()
    check(len(rows('SOV'))==2,'Civilian intelligence independently discovers new payment')
    m.intel.clear();m.call('icsd_build_view','SOV')
    check(len(rows('SOV'))==2,'Previously discovered correspondence survives lost access')
    m.flags['USA'].add('icsd_open');m.flags['SOV'].add('icsd_open')
    for _ in range(35):payment()
    check(all(len(m.a['USA']['icsd_mail_'+c])==24 for c in COLS),'All journal columns evict together at 24')
    check(len(rows('SOV'))==2,'Hidden new payments do not alter rival journal or visible count')
    m.v['USA'].update(icsd_tab=3,icsd_history=1,icwt_register=0);m.call('icsd_build_view')
    check(m.v['USA']['icsd_view_count']==24 and m.v['USA']['icsd_row_count']==5,'Five-row dossier pagination consumes only observer-visible records')
    m.call('icsd_select_0');oldkey=m.v['USA']['icsd_selected_key']
    payment();m.call('icsd_build_view')
    check(m.v['USA']['icsd_selected_key']==oldkey,'Journal insertion keeps selection tied to its stable event key')
    for _ in range(24):payment()
    m.call('icsd_build_view')
    check(m.v['USA'].get('icsd_selected_kind',0)==0,'Evicted selected record clears all detail fields')
    for tag in ('USA','SOV'):m.call('icsd_clear_live',tag)
    def investment():
        m.packet(actor=1,target=3,kind=8,place=-447,type=1,size=2,amount=12,key=1)
        m.call('icsd_publish_live')
    investment()
    check(m.a['USA']['icsd_live_amount']==[12] and m.a['SOV']['icsd_live_amount']==[0],'Foreign investment cost is redacted for the rival only')
    check(all(m.a['SOV']['icsd_live_'+c]==[0] for c in ('place','type','size','left')),'Masked investment data is absent from the observer cache')
    m.packet(actor=1,target=3,kind=13,amount=0.2);m.call('icsd_publish_live')
    check(rows('SOV','live')==[8],'Unknown subsidy leaves no row/count')
    m.packet(actor=1,target=3,kind=10,type=4,left=200);m.call('icsd_publish_live')
    check(m.a['SOV']['icsd_live_type']==[0,4],'Public political support retains the exact native party slot without an intel gate')
    m.v['SOV']['icsd_network@EGY']=1;investment()
    check(m.a['SOV']['icsd_live_amount'][-1]==12,'Cached recipient network unlocks ongoing project details')
    m.v['SOV']['icsd_tab']=1;before=m.queries;m.call('icsd_build_view','SOV');m.call('icsd_select_0','SOV')
    check(m.queries==before,'Opening/paging/selecting performs no intelligence query or world discovery')
    m.v['SOV']['icsd_offset']=6000;m.call('icsd_build_view','SOV')
    check(m.v['SOV']['icsd_offset']==0,'Out-of-range page recovers')
    m.call('icsd_clear_live','SOV');m.call('icsd_build_view','SOV')
    check(m.v['SOV'].get('icsd_selected_kind',0)==0,'Ended investment clears selected detail')
    m.call('icsd_build_view','CHI')
    check('icsd_tab' not in m.v['CHI'],'Third country cannot build a dossier')
    check(all(m.v[tag]['treasury']==1000 for tag in m.tags),'Every observation/navigation path leaves every treasury unchanged')
    saved=copy.deepcopy((m.v,m.a,m.flags));m.v,m.a,m.flags=copy.deepcopy(saved)
    m.v['USA'].update(icsd_tab=3,icsd_history=1,icwt_register=0);m.call('icsd_build_view')
    check(len(rows('USA'))==24,'Saved observer records rebuild without replaying any payment')
    gui=parser.parse((ROOT/'common/scripted_guis/ICW_superpower_dossier.txt').read_text())[0][2]
    main_gui=next(b for k,o,b in gui if k=='icsd_main')
    controls=next(b for k,o,b in main_gui if k=='effects')
    actions={k:b for k,o,b in controls if k.startswith('icsd_action_') and k.endswith('_click')}
    m.effects.update(actions)
    for action in actions:
        m.v['USA']['icsd_selected_kind']=8;m.v['USA']['icsd_selected_target']=3;m.v['USA']['icsd_response_target']=3
        m.flags['USA'].add('icsd_open');before=len(m.camera);m.call(action)
        check('icsd_open' not in m.flags['USA'] and len(m.camera)==before+1 and m.camera[-1]=='capital:EGY',action+' closes file and goes directly to the selected recipient')
    m.v['USA']['icsd_response_target']=999;m.flags['USA'].add('icsd_open');before=len(m.camera);m.call(next(iter(actions)))
    check('icsd_open' in m.flags['USA'] and len(m.camera)==before,'Missing recipient cannot route to a stale country')
    check(all(m.v[tag]['treasury']==1000 for tag in m.tags),'All direct response clicks preserve all treasury balances')
    report={'project':'IMPERIA COLD WAR','passed':len(checks),'checks':checks,'scope':'Actual emitted script AST in a bounded semantic model. Not native execution, elapsed timings or multiplayer.'}
    (HERE/'behavior-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
