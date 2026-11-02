# IMPERIA COLD WAR — Economic organisation parser and regression checks
import copy
import hashlib
import json
import re
from pathlib import Path
from PIL import Image
from catalogue import ROOT, TIERS, REFORMS, STARTS, MARKER

OUT=ROOT/'docs/design/economic_organisation'
COUNT=0
def check(ok,message):
    global COUNT
    COUNT+=1
    assert ok,message

def parse(source):
    ts=[m[0] for m in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]|>=|<=|!=|=|<|>|[^\s{}<>=!#"]+',source) if not m[0].startswith('#')]
    assert not any(t in ('>=','<=','!=') for t in ts),'Unsupported compound comparison'
    pos=0
    def block(nested=False):
        nonlocal pos
        result=[]
        while pos<len(ts):
            key=ts[pos];pos+=1
            if key=='}':
                assert nested,'Unexpected close'
                return result
            if key=='{':result.append(('_list','=',block(True)));continue
            if pos<len(ts) and ts[pos] in ('=','>','<'):
                op=ts[pos];pos+=1;value=ts[pos];pos+=1
                if value=='{':value=block(True)
                assert value!='}','Missing value'
                result.append((key,op,value))
            else:result.append(('_bare','=',key))
        assert not nested,'Unclosed block'
        return result
    return block()

def vals(body,key):return [v for k,o,v in body if k==key]
def first(body,key,default=None):return next(iter(vals(body,key)),default)
def walk(body):
    for k,o,v in body:
        yield k,o,v
        if isinstance(v,list):yield from walk(v)

MANIFEST=json.loads((OUT/'implementation_manifest.json').read_text())
ASTS={rel:parse((ROOT/rel).read_text(encoding='utf-8-sig')) for rel in MANIFEST['generated'] if not rel.endswith('.yml')}
EFFECTS=dict((k,v) for k,o,v in ASTS['common/scripted_effects/ICW_economic_organisation.txt'])
TRIGGERS=dict((k,v) for k,o,v in ASTS['common/scripted_triggers/ICW_economic_organisation.txt'])
IDEAS=dict((k,v) for k,o,v in first(first(ASTS['common/ideas/ICW_economic_organisation.txt'],'ideas'),'country'))
SHARED=parse((ROOT/'common/scripted_effects/99_investment_scripted_effects.txt').read_text(encoding='utf-8'))
EFFECTS.update({k:v for k,o,v in SHARED if k in ('get_building_construction_values','calculate_project_duration')})
EFFECTS.update({k:v for k,o,v in parse((ROOT/'common/scripted_effects/00_budget_effects.txt').read_text(encoding='utf-8')) if k=='modify_treasury_effect'})
CONTEXT={}

class Country:
    """Strict evaluator of the emitted country transactions, with external readers stubbed explicitly."""
    def __init__(self,tag='ZZZ',date='1970.1.1'):
        self.tag=tag;self.date=date;self.variables={'political_power':1000,'globalism_value':80};self.flags=set();self.ideas={'unrelated_national_spirit'};self.refreshes=0
    @property
    def context(self):
        if self not in CONTEXT:CONTEXT[self]={'world':{self.tag:self},'root':self,'prev':None,'parent':None,'exists':True,'targets':{},'events':[],'id':len(CONTEXT)+1}
        return CONTEXT[self]
    def scope(self,name):
        if name=='THIS':return self
        if name=='ROOT':return self.context['root']
        if name=='PREV':return self.context['prev']
        if name=='overlord':return self.context['world'].get(self.context['parent'])
        if name.startswith('event_target:'):return self.context['world'].get(self.context['root'].context['targets'].get(name.split(':',1)[1]))
        return None
    def scoped(self,target,body,testing=False):
        if target is None:return False if testing else None
        context=target.context;old=(context['root'],context['prev']);context['root']=self.context['root'];context['prev']=self
        try:return target.test(body) if testing else target.run(body)
        finally:context['root'],context['prev']=old
    def storage(self,name):
        if '.' in name and name.split('.',1)[0] in ('THIS','ROOT','PREV'):
            prefix,name=name.split('.',1);return self.scope(prefix),name
        return self,self.variable_name(name)
    def number(self,value):
        if isinstance(value,list):
            result=0
            for k,o,v in value:
                if k=='value':result=self.number(v)
                elif k=='add':result+=self.number(v)
                elif k=='multiply':result*=self.number(v)
                elif k=='subtract':result-=self.number(v)
                elif k=='round':result=round(result)
                elif k=='clamp':result=min(self.number(first(v,'max')),max(self.number(first(v,'min')),result))
                else:raise AssertionError('Unknown inline operator '+k)
            return result
        try:return float(value)
        except ValueError:
            if value.endswith('.id') and self.scope(value[:-3]):return self.scope(value[:-3]).context['id']
            if '.' in value and value.split('.',1)[0] in ('THIS','ROOT','PREV'):
                prefix,field=value.split('.',1);owner=self.scope(prefix);return owner.number(field) if owner else 0
            if value=='modifier@globalism_equilibrium':return 50+sum(float(first(first(IDEAS.get(i,[]),'modifier',[]),'globalism_equilibrium',0)) for i in self.ideas)
            return self.variables.get(self.variable_name(value),0)
    def variable_name(self,name):
        if '^' in name:
            base,index=name.split('^',1)
            try:int(index)
            except ValueError:index=str(int(self.number(index)))
            return base+'^'+index
        return name
    def test(self,body):
        answers=[]
        for k,o,v in body:
            if k in ('AND','hidden_trigger','custom_trigger_tooltip'):a=self.test([item for item in v if item[0]!='tooltip'])
            elif k=='OR':a=any(self.test([item]) for item in v)
            elif k=='NOT':a=not self.test(v)
            elif k=='always':a=v=='yes'
            elif k=='has_country_flag':a=v in self.flags
            elif k=='has_idea':a=v in self.ideas
            elif k=='exists':a=self.context['exists']==(v=='yes')
            elif k=='is_ai':a=(v=='no')
            elif k=='is_subject':a=bool(self.context['parent'])==(v=='yes')
            elif k=='is_subject_of':a=self.scope(v) is not None and self.context['parent']==self.scope(v).tag
            elif k=='overlord' or k.startswith('event_target:'):a=self.scoped(self.scope(k),v,True)
            elif k=='original_tag':a=self.tag==v
            elif k=='date':
                left=tuple(map(int,self.date.split('.')));right=tuple(map(int,v.split('.')));a=left<right if o=='<' else left>right if o=='>' else left==right
            elif k=='has_political_power':a=self.compare(self.number('political_power'),o,self.number(v))
            elif k=='check_variable':
                name,op,value=v[0];a=self.compare(self.number(name),op,self.number(value))
            elif k=='has_dynamic_modifier':a=False
            elif k=='IMP_is_1970_scenario':a=False
            elif k in TRIGGERS:a=self.test(TRIGGERS[k])==(v=='yes')
            else:raise AssertionError('Unknown trigger '+k)
            answers.append(a)
        return all(answers)
    @staticmethod
    def compare(a,o,b):return a<b if o=='<' else a>b if o=='>' else abs(a-b)<.00001
    def run(self,body):
        branch=False
        for k,o,v in body:
            if k in ('if','else_if','else'):
                if k=='if':branch=False
                take=not branch and (k=='else' or self.test(first(v,'limit',[])))
                if take:self.run([item for item in v if item[0]!='limit']);branch=True
            elif k=='hidden_effect':self.run(v)
            elif k in ('effect_tooltip','custom_effect_tooltip'):pass
            elif k=='set_country_flag':self.flags.add(v)
            elif k=='clr_country_flag':self.flags.discard(v)
            elif k=='clear_variable':self.variables.pop(v,None)
            elif k=='save_event_target_as':self.context['root'].context['targets'][v]=self.tag
            elif k=='country_event':self.context['events'].append({'recipient':self.tag,'id':first(v,'id'),'days':int(first(v,'days',0)),'targets':dict(self.context['root'].context['targets'])})
            elif k=='overlord' or k.startswith('event_target:'):self.scoped(self.scope(k),v)
            elif k in ('set_variable','add_to_variable','subtract_from_variable','set_temp_variable','add_to_temp_variable','subtract_from_temp_variable','multiply_temp_variable','divide_temp_variable'):
                name,op,value=v[0]
                if name=='var':name=value;value=first(v,'value')
                amount=self.number(value);owner,name=self.storage(name)
                if k.startswith('set_'):owner.variables[name]=amount
                elif k.startswith('multiply_'):owner.variables[name]=owner.number(name)*amount
                elif k.startswith('divide_'):owner.variables[name]=owner.number(name)/amount
                else:owner.variables[name]=owner.number(name)+(amount if k.startswith('add_') else -amount)
            elif k in ('clamp_variable','clamp_temp_variable'):
                name=first(v,'var');self.variables[name]=min(self.number(first(v,'max','1000000000')),max(self.number(first(v,'min','-1000000000')),self.number(name)))
            elif k=='add_political_power':self.variables['political_power']+=self.number(v)
            elif k=='add_ideas':self.ideas.add(v)
            elif k=='remove_ideas':
                for _,_,i in v:self.ideas.discard(i)
            elif k=='ingame_update_setup':self.refreshes+=1
            elif k=='update_money_dirty_variable':pass  # Native UI invalidation only.
            elif k in EFFECTS:self.run(EFFECTS[k])
            else:raise AssertionError('Unknown effect '+k)
    def call(self,name):self.run(EFFECTS[name])

def main():
    for rel in MANIFEST['generated']:
        raw=(ROOT/rel).read_bytes()
        check(raw.startswith(b'\xef\xbb\xbf')==rel.endswith('.yml'),'Incorrect BOM '+rel)
        check(hashlib.sha256(raw).hexdigest()==MANIFEST['files_sha256'][rel],'Manifest drift '+rel)
        check(MARKER in raw.decode('utf-8-sig'),'Marker missing '+rel)
        check(not re.search(r'\d+\.\d{6,}',raw.decode('utf-8-sig')),'Fixed point precision '+rel)
    alltext='\n'.join((ROOT/r).read_text(encoding='utf-8-sig') for r in MANIFEST['generated'])
    check(not re.search(r'\b(?:set_power_balance|remove_power_balance|add_power_balance_value|add_building_construction|add_extra_state_shared_building_slots|set_politics)\s*=',alltext),'Unexpected native BoP, building or political side effect')
    # User-approved prototype is the independent acceptance contract for restored values.
    contract=json.loads((OUT/'original_compact_effects.json').read_text(encoding='utf-8'))
    original={stage['slug']:stage['expected_modifiers'] for stage in contract['stages']}
    before=json.loads((OUT/'pre_restoration_balance.json').read_text(encoding='utf-8'))
    for slug,expected in original.items():
        mods=first(IDEAS['icw_econ_'+slug],'modifier')
        for key,value in expected.items():check(abs(float(first(mods,key,'999'))-value)<.00001,'Original compact value lost: '+slug+'/'+key)
    for slug,name,lo,hi,mods in before['tiers']:
        current=first(IDEAS['icw_econ_'+slug],'modifier')
        for key,value in mods.items():
            expected=original[slug].get(key,value)
            check(abs(float(first(current,key,'999'))-expected)<.00001,'Later enhancement lost during restoration: '+slug+'/'+key)
    # IMPERIA COLD WAR — English localisation coverage
    localisation=(ROOT/'localisation/english/ICW_economic_organisation_l_english.yml').read_text(encoding='utf-8-sig')
    keys=re.findall(r'^ (\w+):',localisation,re.M)
    localised=dict(re.findall(r'^ (\w+): "(.*)"$',localisation,re.M))
    check(len(keys)==len(set(keys)),'Duplicate English key')
    check(not any('–' in line or '—' in line for line in localisation.splitlines() if not line.startswith('#')),'Player-facing dash punctuation')
    guis=first(ASTS['common/scripted_guis/ICW_economic_organisation.txt'],'scripted_gui')
    reform_gui=first(guis,'icw_econ_reforms');gui_effects=dict((k,v) for k,o,v in first(reform_gui,'effects'))
    check(all(not vals(body,'dirty') for k,o,body in guis),'Stale political-power or Globalisation eligibility cache')
    decisions=first(ASTS['common/decisions/ICW_economic_organisation.txt'],'icw_econ_category')
    # IMPERIA COLD WAR — Native decision presentation regression checks
    # Native custom costs require normal, blocked and hover localisation entries.
    for slug,name,delta,cost,description in REFORMS:
        decision=first(decisions,'icw_econ_decision_'+slug)
        base=first(decision,'custom_cost_text')
        check(all(localised.get(base+suffix) for suffix in ('','_blocked','_tooltip')),'Incomplete native cost localisation '+slug)
        check(f'£pol_power §R{cost}§!'==localised[base+'_blocked'],'Blocked political-power cost '+slug)
        check(all(ref in localised for ref in re.findall(r'\$(\w+)\$',localised['icw_econ_decision_'+slug+'_desc'])),'Unresolved reform description '+slug)
    md_sprites=dict(re.findall(r'name\s*=\s*"([^"]+)"\s+texturefile\s*=\s*"([^"]+)"',(ROOT/'interface/MD_decisions.gfx').read_text(encoding='utf-8')))
    category=first(ASTS['common/decisions/categories/ICW_economic_organisation.txt'],'icw_econ_category')
    for name,body,max_size in [('category',category,(52,40))]+[(k,v,(34,34)) for k,o,v in decisions]:
        sprite=first(body,'icon')
        check(sprite in md_sprites,'Unregistered native economic decision icon '+name)
        with Image.open(ROOT/md_sprites[sprite]) as icon:
            icon.load()
            check(icon.width<=max_size[0] and icon.height<=max_size[1],'Native decision icon exceeds its slot '+name)
    for i,(slug,name,delta,cost,description) in enumerate(REFORMS,1):
        c=Country();c.call('icw_econ_initialize');before=c.number('political_power')
        c.run(gui_effects['icw_econ_select_'+slug+'_click'])
        check(c.number('political_power')==before and c.number('icw_econ_position')==0 and not c.test([('has_country_flag','=','icw_econ_reform_active')]),'Row selection enacted reform '+slug)
        check(c.number('icw_econ_selected_reform')==i and [c.number('icw_econ_button_'+str(j)) for j in range(1,6)]==[2 if j==i else 1 for j in range(1,6)],'Reform selection highlight '+slug)
        c.run(gui_effects['icw_econ_enact_click'])
        d=Country();d.call('icw_econ_initialize');d.run(first(first(decisions,'icw_econ_decision_'+slug),'complete_effect'))
        substantive=lambda variables:{k:v for k,v in variables.items() if k!='icw_econ_gui_dirty'}
        check(substantive(c.variables)==substantive(d.variables) and c.flags==d.flags and c.ideas==d.ideas,'Decision / GUI transaction mismatch '+slug)
    for tag,pos in [(tag,pos) for pos,tags in STARTS.items() for tag in tags]+[('CHI',-80),('ZZZ',0)]:
        c=Country(tag);c.call('icw_econ_initialize');check(c.number('icw_econ_position')==pos,'Initial profile '+tag)
        state=copy.deepcopy(c.__dict__);c.call('icw_econ_initialize');check(c.__dict__==state,'Initialization replay '+tag)
    c=Country('CHI','1980.1.1');c.call('icw_econ_initialize');check(c.number('icw_econ_position')==-35,'Chinese reform profile')
    c=Country('SOV','2000.1.1');c.call('icw_econ_initialize');check(c.number('icw_econ_position')==0,'Later scenario fallback')
    c=Country();c.call('icw_econ_initialize');c.variables.update(icw_econ_position=25,icw_econ_needle_x=402,icw_econ_days_remaining=45,icw_econ_cooldown_days=135);c.flags.add('icw_econ_reform_active');c.call('icw_econ_initialize')
    check(c.number('icw_econ_needle_x')==round(125*2.7+59) and c.number('icw_econ_position')==25 and c.number('icw_econ_days_remaining')==45 and c.number('icw_econ_cooldown_days')==135 and 'icw_econ_reform_active' in c.flags,'Saved marker migration changed reform state')
    for pos,idx in [(-200,1),(-100,1),(-70.001,1),(-70,2),(-40.001,2),(-40,3),(-15,4),(14.999,4),(15,5),(40,6),(70,7),(100,7),(200,7)]:
        c=Country();c.variables['icw_econ_position']=pos;c.call('icw_econ_refresh_tier')
        check(c.number('icw_econ_tier')==idx,'Tier boundary '+str(pos))
        check(len(c.ideas.intersection(IDEAS))==1 and 'unrelated_national_spirit' in c.ideas,'Exclusive policy and unrelated spirit')
        check(59<=c.number('icw_econ_needle_x')<=599,'Needle clamp')
    for slug,name,delta,cost,description in REFORMS:
        c=Country();c.call('icw_econ_initialize');before=copy.deepcopy(c.__dict__)
        c.run([('effect_tooltip','=',[('icw_econ_preview_'+slug,'=','yes')])]);check(c.__dict__==before,'Tooltip mutation '+slug)
        c.call('icw_econ_start_'+slug)
        check(c.number('political_power')==1000-cost and c.number('icw_econ_position')==0,'Start cost and delayed position '+slug)
        snapshot=copy.deepcopy(c.__dict__)
        for _ in range(3):
            for other,*_ in REFORMS:c.call('icw_econ_start_'+other)
        check(c.__dict__==snapshot,'Repeated or concurrent reform '+slug)
        for _ in range(89):c.call('icw_econ_daily')
        check(c.number('icw_econ_position')==0 and c.number('icw_econ_days_remaining')==1,'Day 89 '+slug)
        # Serialize the native-persisted state mid-reform, then resume through the same script.
        resumed=Country();resumed.__dict__=copy.deepcopy(c.__dict__);resumed.call('icw_econ_initialize');resumed.call('icw_econ_daily');resumed.call('icw_econ_complete_reform')
        check(resumed.number('icw_econ_position')==delta and resumed.number('political_power')==1000-cost and resumed.refreshes==1,'Completion replay '+slug)
        check(resumed.number('icw_econ_cooldown_days')==90 and not resumed.test(TRIGGERS['icw_econ_ready']),'Post completion cooldown '+slug)
        for _ in range(90):resumed.call('icw_econ_daily')
        check(resumed.test(TRIGGERS['icw_econ_ready']),'Day 180 '+slug)
        for pp,pos,g in [(cost-1,0,80),(1000,-100 if delta<0 else 100,80),(1000,70-delta,79.999)] if delta>0 else [(cost-1,0,80),(1000,-100,80)]:
            c=Country();c.call('icw_econ_initialize');c.variables.update(political_power=pp,icw_econ_position=pos,globalism_value=g);before=copy.deepcopy(c.__dict__);c.call('icw_econ_start_'+slug);check(c.__dict__==before,'Invalid reform mutation '+slug)
        if delta>0:
            c=Country();c.call('icw_econ_initialize');c.variables.update(icw_econ_position=70-delta,globalism_value=80);check(c.test(TRIGGERS['icw_econ_can_'+slug]),'80 globalisation threshold '+slug)
    # Audit the complete host container and every neighbouring window, including percentage-sized workforce.
    host=parse((ROOT/'interface/MD_countryeconomyview.gui').read_text())
    economy=next(v for k,o,v in walk(host) if k=='containerWindowType' and first(v,'name')=='"economyview_container"' and first(first(v,'size',[]),'height')=='1058')
    children={first(v,'name').strip('"'):v for v in vals(economy,'containerWindowType')}
    for move in json.loads((OUT/'economy_layout_moves.json').read_text())['moves']:
        check(int(first(first(children[move['name']],'position'),'y'))==move['after_y'],'Host neighbour not moved '+move['name'])
    check(first(first(economy,'size'),'height')=='1058','Host scroll content size')
    anchors={first(v,'name').strip('"') for k,o,v in walk(host) if k=='containerWindowType' and first(v,'name')}
    for k,o,body in guis:check(first(body,'parent_window_name') in anchors,'Missing named GUI anchor '+k)
    for path in (ROOT/'gfx/interface/ICW_economic_organisation').glob('*.dds'):
        image=Image.open(path);image.load();check(image.width>0 and image.height>0,'Unreadable texture '+path.name)
    events={first(body,'id'):body for k,o,body in ASTS['events/ICW_economic_organisation.txt'] if k=='country_event'}
    def subject_world():
        countries={tag:Country(tag) for tag in ['SUB','PAR','ALT','OTHER']};queued=[]
        for c in countries.values():c.context.update(world=countries,events=queued);c.call('icw_econ_initialize')
        countries['SUB'].context['parent']='PAR';countries['OTHER'].context['parent']='PAR'
        return countries,queued
    def respond(countries,queued,choice=0,event_index=-1):
        event=queued[event_index];recipient=countries[event['recipient']];recipient.context['targets']=event['targets'].copy()
        body=events[event['id']]
        if not recipient.test(first(body,'trigger')):return False
        option=vals(body,'option')[choice]
        if not recipient.test(first(option,'trigger',[])):return False
        recipient.run([item for item in option if item[0] not in ('name','trigger','ai_chance')]);return True
    for i,(slug,name,delta,cost,description) in enumerate(REFORMS,1):
        countries,queued=subject_world();s=countries['SUB'];s.call('icw_econ_start_'+slug)
        check(len(queued)==1 and queued[0]['days']==1 and queued[0]['recipient']=='PAR' and queued[0]['targets']['icw_econ_applicant']=='SUB','One-day approval route '+slug)
        check(s.number('political_power')==1000 and s.number('icw_econ_position')==0 and s.number('icw_econ_cooldown_days')==0 and 'icw_econ_reform_active' not in s.flags,'Request caused cost or reform '+slug)
        for other,*_ in REFORMS:s.call('icw_econ_start_'+other);s.call('icw_econ_apply_'+other)
        check(len(queued)==1 and s.number('political_power')==1000,'Pending request bypass '+slug)
        check(respond(countries,queued) and s.number('political_power')==1000-cost and s.number('icw_econ_days_remaining')==90 and 'icw_econ_reform_active' in s.flags,'Approval payment/start '+slug)
        check('icw_econ_overlord_authorised' not in s.flags and 'icw_econ_approval_pending' not in s.flags,'Authorisation leaked '+slug)
        check(not respond(countries,queued) and s.number('political_power')==1000-cost,'Repeated approval '+slug)
        s.call('icw_econ_complete_reform');check(s.number('icw_econ_position')==delta,'Approved direction '+slug)
        countries,queued=subject_world();s=countries['SUB'];s.call('icw_econ_start_'+slug)
        check(respond(countries,queued,1) and s.number('political_power')==1000 and s.number('icw_econ_position')==0 and 'icw_econ_approval_pending' not in s.flags and s.number('icw_econ_cooldown_days')==0,'Decline not free/no-op '+slug)
        for mutation in ['parent','independence','position','funds']:
            countries,queued=subject_world();s=countries['SUB'];s.call('icw_econ_start_'+slug)
            if mutation=='parent':s.context['parent']='ALT'
            elif mutation=='independence':s.context['parent']=None
            elif mutation=='position':s.variables['icw_econ_position']=1
            else:s.variables['political_power']=cost-1
            check(not respond(countries,queued),'Stale/ineligible approval '+slug+'/'+mutation)
            s.call('icw_econ_daily')
            if mutation!='funds':check('icw_econ_approval_pending' not in s.flags,'Invalid request not cleared '+slug+'/'+mutation)
            else:check(respond(countries,queued,1),'Unfunded request cannot be declined '+slug)
    countries,queued=subject_world();countries['SUB'].call('icw_econ_start_ownership');countries['OTHER'].call('icw_econ_start_autonomy')
    check(respond(countries,queued,event_index=0) and respond(countries,queued,event_index=1),'Concurrent subjects sharing overlord')
    check(countries['SUB'].number('icw_econ_pending_position')==-10 and countries['OTHER'].number('icw_econ_pending_position')==5,'Applicant scopes mixed up')
    windows=vals(first(ASTS['interface/ICW_economic_organisation.gui'],'guiTypes'),'containerWindowType')
    for window in windows:
        needle=next(body for kind,o,body in window if kind=='iconType' and first(body,'name','').endswith('_needle"'))
        check(first(needle,'scale')=='1.5','Position marker scale')
    for slug,name,delta,cost,desc in REFORMS:
        arrow=next(body for kind,o,body in windows[1] if kind=='iconType' and first(body,'name')=='"icw_econ_direction_'+slug+'"')
        check(first(arrow,'spriteType')=='GFX_icw_econ_arrow_'+('left' if delta<0 else 'right'),'Direction arrow '+slug)
    # Exercise the actual shared reader, including the existing zero-speed fallback.
    def duration(receiving,investor=0,local=1):
        c=Country();c.variables.update({'global.build_const_cost_array^1':47500,'project_type':1,'project':-1,'project_build_amount^-1':1,'local_state_modifier':local,'receiving_investment_duration_temp':receiving,'modifier@investment_duration_modifier':investor})
        c.call('calculate_project_duration');return c.number('project_construction_duration^-2')
    baseline=duration(0)
    check(duration(.2)>baseline>duration(-.2)>0,'Actual duration reader signs')
    check(duration(.1,.1)==duration(.2),'Recipient and investor duration stacking')
    check(duration(-100)==duration(-.9) and duration(100)==duration(9),'Bounded duration factor')
    check(duration(.2,local=-10)==duration(-.2,local=-10)==1,'Existing nonpositive construction-speed fallback')
    report={'project':'IMPERIA COLD WAR','success':True,'checks':COUNT,'scope':'Emitted script parser, transaction state model, boundaries, profiles, guard failures, preview non-mutation, native custom-cost localisation, decision icon registration and fit, encoding, host layout and texture decoding. State persistence model is not an actual game save/reload.'}
    (OUT/'validation_report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
