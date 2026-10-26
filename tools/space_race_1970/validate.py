# IMPERIA CW — Cold War: execute the generated native Space Race scripts.
"""Strict static validation and deterministic execution of actual Clausewitz ASTs.

This rejects unsupported statements. It is not an in-game UI or multiplayer test.
Arithmetic is deliberately restricted to three decimal places to expose rounding
deadlocks, zero denominators and unpaid progress in low-cost entry programmes.
"""
import ast
from collections import deque
from copy import deepcopy
from decimal import Decimal, ROUND_DOWN
import json
from pathlib import Path
import re
from dataclasses import dataclass,field
from PIL import Image
from mission_rules import REQUIREMENTS

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/'catalogue.json').read_text(encoding='utf-8'))
MANIFEST=json.loads((HERE/'manifest.json').read_text(encoding='utf-8'))
parser_path=ROOT/'tools/israel_1970/validate_content.py'
tree=ast.parse(parser_path.read_text(encoding='utf-8'))
namespace={'re':re}
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'tokens','parse','values','first','walk'}],type_ignores=[]),str(parser_path),'exec'),namespace)
parse,values,first,walk=(namespace[n] for n in ['parse','values','first','walk'])
D=lambda x:Decimal(str(x))
Q=lambda x:D(x).quantize(D('.001'),rounding=ROUND_DOWN)
CHECKS=0


def check(answer,message):
    global CHECKS
    CHECKS+=1
    assert answer,message


ASTS={}
for file in MANIFEST['outputs']:
    path=ROOT/file
    check(path.exists(),'Missing '+file)
    raw=path.read_bytes()
    if path.suffix in ['.txt','.gui','.gfx']:
        check(not raw.startswith(b'\xef\xbb\xbf'),'Script BOM '+file)
        check(raw.decode('utf-8').startswith('# IMPERIA CW'),'Missing ownership comment '+file)
        try:ASTS[file]=parse(raw.decode('utf-8'))
        except AssertionError as error:raise AssertionError(file+': '+str(error)) from error
    elif path.suffix=='.yml':
        check(raw.startswith(b'\xef\xbb\xbf'),'Localisation BOM '+file)
    elif path.suffix=='.dds':
        im=Image.open(path).convert('RGBA')
        if '/news_' in file or '/report_' in file:
            check(im.getchannel('A').getextrema()==(255,255),'Transparent event image '+file)

EFFECTS={};TRIGGERS={}
for file,body in ASTS.items():
    if '/scripted_effects/' in file: EFFECTS.update({k:v for k,op,v in body})
    if '/scripted_triggers/' in file: TRIGGERS.update({k:v for k,op,v in body})
EVENTS={first(v,'id'):v for file,body in ASTS.items() if file.startswith('events/') for k,op,v in body if k in ['country_event','news_event']}


@dataclass
class Country:
    tag:str
    ai:bool=False
    variables:dict=field(default_factory=lambda:{'treasury':D(10000)})
    flags:set=field(default_factory=set)
    temp:dict=field(default_factory=dict)
    pp:Decimal=D(0)
    manpower:Decimal=D(100000)
    tech_bonuses:list=field(default_factory=list)
    ideas:set=field(default_factory=set)
    dynamic_modifiers:set=field(default_factory=set)


class Machine:
    def __init__(self,tags=('SAU','USA','SOV')):
        self.countries={t:Country(t) for t in tags};self.c=self.countries[tags[0]]
        self.g={'year':D(1970),'month':D(1)};self.gf=set();self.targets={};self.events=[];self.rolls=deque();self.date='1970.1.1'

    def store(self,key,temp=False):
        if key.startswith('global.'):return self.g,key[7:]
        return (self.c.temp if temp else self.c.variables),key

    def get(self,key):
        try:return Q(key)
        except Exception:pass
        if key.startswith('global.'):return self.g.get(key[7:],D(0))
        return self.c.temp.get(key,self.c.variables.get(key,D(0)))

    def put(self,key,value,temp=False):
        store,name=self.store(key,temp);store[name]=Q(value)

    def compare(self,a,op,b):
        return {'=':a==b,'>':a>b,'<':a<b,'equals':a==b,'greater_than_or_equals':a>=b,'less_than_or_equals':a<=b,'not_equals':a!=b}[op]

    def test(self,body):
        answers=[]
        for key,op,v in body:
            if key in TRIGGERS:a=self.test(TRIGGERS[key])
            elif key=='AND':a=self.test(v)
            elif key=='OR':a=any(self.test([node]) for node in v)
            elif key=='NOT':a=not self.test(v)
            elif key=='always':a=v=='yes'
            elif key=='is_ai':a=self.c.ai==(v=='yes')
            elif key=='IMP_is_1970_scenario':a=True
            elif key=='has_country_flag':a=v in self.c.flags
            elif key=='has_idea':a=v in self.c.ideas
            elif key=='has_dynamic_modifier':a=(first(v,'modifier') if isinstance(v,list) else v) in self.c.dynamic_modifiers
            elif key=='has_global_flag':a=v in self.gf
            elif key=='has_event_target':a=v in self.targets
            elif key in ['tag','original_tag']:a=self.c.tag==v
            elif key=='date':a=self.compare(tuple(map(int,self.date.split('.'))),op,tuple(map(int,v.split('.'))))
            elif key=='check_variable':
                if first(v,'var') is not None:name,operator,target=first(v,'var'),first(v,'compare','equals'),first(v,'value')
                else:name,operator,target=v[0]
                a=self.compare(self.get(name),operator,self.get(target))
            else:raise AssertionError('Unsupported trigger '+key)
            answers.append(a)
        return all(answers)

    def call(self,key):self.run(EFFECTS[key])

    def run(self,body):
        taken=False
        for key,op,v in body:
            if key in ['if','else']:
                if key=='if':taken=False
                if not taken and (key=='else' or self.test(first(v,'limit',[]))):
                    self.run([n for n in v if n[0]!='limit']);taken=True
                continue
            taken=False
            if key in EFFECTS:self.call(key)
            elif key=='every_country':
                old=self.c
                for c in self.countries.values():
                    self.c=c
                    if self.test(first(v,'limit',[])):self.run([n for n in v if n[0]!='limit'])
                self.c=old
            elif key.startswith('event_target:'):
                old=self.c;self.c=self.targets[key.split(':',1)[1]];self.run(v);self.c=old
            elif key in ['set_country_flag','clr_country_flag']:
                (self.c.flags.add if key=='set_country_flag' else self.c.flags.discard)(v)
            elif key=='set_global_flag':self.gf.add(v if isinstance(v,str) else first(v,'flag'))
            elif key=='save_global_event_target_as':self.targets[v]=self.c
            elif key=='clear_global_event_target':self.targets.pop(v,None)
            elif key=='modify_treasury_effect':self.put('treasury',self.get('treasury')+self.get('treasury_change'))
            elif key=='international_systems_update':self.g['md_ui_updates']=self.g.get('md_ui_updates',D(0))+1
            elif key=='remove_ideas':self.c.ideas.discard(v)
            elif key=='remove_dynamic_modifier':
                assert isinstance(v,list),'remove_dynamic_modifier requires a modifier block'
                self.c.dynamic_modifiers.discard(first(v,'modifier'))
            elif key in ['country_event','news_event']:
                ident=first(v,'id');assert ident in EVENTS,'Unknown event '+ident
                self.events.append((key,ident,self.c.tag))
            elif key=='add_political_power':self.c.pp+=self.get(v)
            elif key=='add_manpower':self.c.manpower+=self.get(v)
            elif key=='add_tech_bonus':self.c.tech_bonuses.append((first(v,'name'),tuple(values(v,'category')),first(v,'bonus'),first(v,'uses'),tuple(values(v,'technology'))))
            elif key=='set_temp_variable_to_random':
                check(bool(self.rolls),'Unexpected RNG draw; test did not authorise randomness')
                roll=self.rolls.popleft();check(self.get(first(v,'min'))<=roll<self.get(first(v,'max')),'RNG outside documented interval')
                self.put(first(v,'var'),roll,True)
            elif key in ['clamp_variable','clamp_temp_variable']:
                name=first(v,'var');a=max(self.get(first(v,'min')),min(self.get(name),self.get(first(v,'max'))));self.put(name,a,'temp' in key)
            elif key.endswith('_variable'):
                name,_,operand=v[0];value=self.get(operand);old=self.get(name)
                if key.startswith('set_'):a=value
                elif key.startswith('add_'):a=old+value
                elif key.startswith('subtract_'):a=old-value
                elif key.startswith('multiply_'):a=old*value
                elif key.startswith('divide_'):
                    assert value!=0,'Division by zero in '+name
                    a=old/value
                elif key.startswith('modulo_'):a=old%value
                else:raise AssertionError('Unsupported arithmetic '+key)
                self.put(name,a,'temp' in key)
            else:raise AssertionError('Unsupported effect '+key)

    def init(self):
        self.call('cw_sr_seed_world');self.call('cw_sr_initialize');self.call('cw_sr_windows')

    def week(self):
        self.c.temp.clear();self.call('cw_sr_weekly')


def static_checks():
    # Resolve every generated helper/event/sprite/defined-text reference.
    for file,body in ASTS.items():
        for key,op,v in walk(body):
            if key.startswith('cw_sr_') and not isinstance(v,list) and v=='yes':
                check(key in EFFECTS or key in TRIGGERS,'Unresolved helper '+key+' in '+file)
            if key in ['country_event','news_event'] and isinstance(v,list):
                check(first(v,'id') in EVENTS,'Unresolved event')
    sprites={first(v,'name').strip('"'):v for file,body in ASTS.items() if file.endswith('.gfx') for k,op,group in body if k=='spriteTypes' for k2,op2,v in group if k2=='spriteType'}
    for name,body in sprites.items():
        path=ROOT/first(body,'texturefile').strip('"');check(path.exists(),'Missing sprite texture '+name)
    gui=first(ASTS['interface/COLDWAR_space_race.gui'],'guiTypes')
    window=first(gui,'containerWindowType')
    bounds=first(window,'size');panel_width=int(first(bounds,'width'));panel_height=int(first(bounds,'height'))
    elements={first(v,'name').strip('"'):(k,v) for k,op,v in window if k in ['buttonType','instantTextBoxType','iconType']}
    scripted=first(first(ASTS['common/scripted_guis/COLDWAR_space_race_gui.txt'],'scripted_gui'),'cw_sr_main')
    buttons={k for k,(kind,v) in elements.items() if kind=='buttonType'}
    clicks={k.removesuffix('_click') for k,op,v in first(scripted,'effects')}
    check(buttons==clicks,'GUI button/callback mismatch')
    for name,(kind,v) in elements.items():
        position=first(v,'position');x=int(first(position,'x'));y=int(first(position,'y'))
        if kind=='instantTextBoxType':w=int(first(v,'maxWidth'));h=int(first(v,'maxHeight'))
        else:
            sprite=first(v,'spriteType').strip('"');check(sprite in sprites,'Unresolved GUI sprite '+sprite)
            image=Image.open(ROOT/first(sprites[sprite],'texturefile').strip('"'));frames=int(first(sprites[sprite],'noOfFrames','1'));w=image.width//frames;h=image.height
        check(x>=0 and y>=0 and x+w<=panel_width and y+h<=panel_height,'GUI outside panel '+name)
    loc=(ROOT/'localisation/english/COLDWAR_space_race_l_english.yml').read_text(encoding='utf-8-sig')
    pairs=re.findall(r'^ ([\w.]+): "(.*)"$',loc,re.M);localisation=dict(pairs)
    check(len(pairs)==len(localisation),'Duplicate localisation')
    check(not any(word in loc for word in ['NASA archive photograph','Illustrative station imagery','[Source]','NO CAMPAIGN EFFECT','ILLUSTRATIVE BULLETIN']),'Source/debug prose leaked into game text')
    for file,body in ASTS.items():
        for key,op,v in walk(body):
            if key in ['text','buttonText','pdx_tooltip','localization_key','title','desc','custom_effect_tooltip'] and isinstance(v,str):
                value=v.strip('"')
                if value.startswith('cw_sr_'):check(value in localisation,'Missing localisation '+value)
    for ident,body in EVENTS.items():
        for field in ['title','desc']:
            text=localisation[first(body,field)]
            check('[FROM.GetName]' in text or '[ROOT.GetName]' in text,'Country omitted from '+ident+' '+field)
        pic=first(body,'picture');check(pic in sprites,'Missing event sprite '+pic)
        im=Image.open(ROOT/first(sprites[pic],'texturefile').strip('"'))
        check(im.size==((397,153) if ident.startswith('cw_sr_world.') else (217,163)),'Wrong native event image size')


def mechanics():
    for profile in DATA['profiles']:
        tag=profile['id'] if profile['id']!='CUSTOM' else 'SAU'
        m=Machine((tag,));m.init()
        for c in profile['capabilities']:
            check('cw_sr_cap_'+c.replace('-','_') in m.c.flags,tag+' missing inherited '+c)
        check(m.get('cw_sr_prestige')==0,'Free campaign prestige')
    m=Machine();m.c.ai=True;m.init();check('cw_sr_initialized' not in m.c.flags,'AI initialised')
    m.c.ai=False;m.init();m.put('cw_sr_budget',1000)
    m.call('cw_sr_p47_start');check(m.get('cw_sr_active')==1,'Start did not occupy slot')
    initial=m.get('treasury');m.put('cw_sr_budget',0);m.week()
    check(m.get('cw_sr_p47_work')==0 and m.get('treasury')==initial,'Unfunded development advanced')
    m.put('cw_sr_budget',1000)
    for _ in range(84):m.week()
    check(m.get('cw_sr_p47_state')==3,'Entry institution never completes at native precision')
    check(m.get('treasury')<initial,'Development was free')
    check('cw_sr_cap_space_administration' not in m.c.flags,'Capability before acceptance')
    m.rolls.extend([0,0]);m.call('cw_sr_p47_launch')
    check('cw_sr_cap_space_administration' in m.c.flags,'Acceptance did not grant institution')
    check(m.get('cw_sr_p47_state')==5,'Accepted facility not operational')
    for n in [48,49,52]:m.call(f'cw_sr_p{n}_start')
    check(m.get('cw_sr_active')==3,'Three slots unavailable')
    m.call('cw_sr_p71_start');check(m.get('cw_sr_active')==3,'Fourth slot accepted')
    snapshot=deepcopy(m.c.variables);m.c.ai=True;m.week();m.call('cw_sr_daily')
    check(m.c.variables==snapshot,'AI spent money or advanced programmes')
    m.c.ai=False;m.call('cw_sr_p48_pause');check(m.get('cw_sr_active')==2,'Pause did not release slot')
    m.put('cw_sr_p48_work',80);m.call('cw_sr_p48_cancel');check(m.get('cw_sr_p48_work')==60,'Cancellation did not forfeit 25 percent')
    # Every from-scratch programme must finish under all four policies, at native precision.
    for n,p in enumerate(DATA['programmes'],1):
        for policy in range(4):
            t=Machine(('SAU',));t.init();t.put('cw_sr_p'+str(n)+'_state',1);t.put('cw_sr_p'+str(n)+'_policy',policy);t.put('cw_sr_allocation',1000,True)
            for tick in range(math_ceil(p['durationMonths']*52/12*1.4)+8):
                t.call(f'cw_sr_p{n}_week')
                if t.get(f'cw_sr_p{n}_state')==3:break
            check(t.get(f'cw_sr_p{n}_state')==3,f'{p["id"]} policy {policy} development deadlock')
            check(t.get('treasury')<10000,'Uncharged engineering')
    # Delayed mission acceptance, frozen probability, no launch/repeat farming.
    m=Machine(('SAU','USA','SOV'));m.init()
    p=DATA['programmes'][26]
    m.c.flags.update('cw_sr_cap_'+c.replace('-','_') for c in p['capabilityRequirements']);m.put('cw_sr_p27_state',3);m.put('cw_sr_p27_work',100)
    ids={p['id']:i for i,p in enumerate(DATA['programmes'],1)}
    m.c.flags.update('cw_sr_p'+str(ids[group[0]])+'_awarded' for group in REQUIREMENTS[p['id']])
    m.rolls.append(0);before=m.get('treasury');m.call('cw_sr_p27_launch')
    check(m.get('treasury')==before-28 and m.get('cw_sr_p27_state')==4,'Mission appropriation or departure failed')
    check('cw_sr_cap_lunar_landing' not in m.c.flags,'Lunar capability granted on launch')
    frozen=m.get('cw_sr_p27_op');m.put('cw_sr_science',10000);m.call('cw_sr_p27_odds');check(m.get('cw_sr_p27_op')==frozen,'In-flight probability changed')
    days=int(m.get('cw_sr_p27_days'));m.rolls.append(0)
    for _ in range(days):m.call('cw_sr_daily')
    check('cw_sr_cap_lunar_landing' in m.c.flags,'Completed lunar flight did not grant capability')
    check(('country_event','cw_sr_report.8003','SAU') in m.events and ('news_event','cw_sr_world.8003','SAU') in m.events,'Saudi lunar image route missing')
    check('cw_sr_first_first_crewed_lunar_landing' in m.gf,'Apollo historical first not seeded')
    check(m.get('cw_sr_prestige')==p['prestige'],'Historical Moon first awarded twice')
    check(len(m.c.tech_bonuses)==1 and len(m.c.tech_bonuses[0][1])>1 and m.c.tech_bonuses[0][3]=='1','General one-use research reward missing')
    m.call('cw_sr_p27_pause');check('cw_sr_p27_deployed' not in m.c.flags,'Mothball did not suspend operating costs')
    before=m.get('treasury');m.call('cw_sr_p27_upkeep');check(m.get('treasury')==before,'Mothballed programme charged new operations')
    # End-to-end catastrophic launch: real national personnel loss and funded review.
    m.put('cw_sr_p27_state',3);m.rolls.extend([9999,0]);m.call('cw_sr_p27_launch')
    check(m.get('cw_sr_fatalities')==3 and m.c.manpower==99997,'Crew deaths were not recorded')
    check(m.get('cw_sr_p27_im')==12,'Catastrophic review duration')
    m.put('cw_sr_allocation',1000,True)
    for _ in range(54):m.call('cw_sr_p27_week')
    check(m.get('cw_sr_p27_state')==3 and m.get('cw_sr_p27_corrective')==1,'Funded investigation did not complete')
    # Mars firsts: award only on returned mission; share the receipt between countries.
    for tag,event in [('USA','cw_sr_world.9101'),('SOV','cw_sr_world.9102')]:
        t=Machine((tag,'SAU'));t.init();t.date='1988.1.1';t.g.update(year=D(1988),month=D(1))
        p=DATA['programmes'][83];t.c.flags.update('cw_sr_cap_'+c.replace('-','_') for c in p['capabilityRequirements']);t.put('cw_sr_p84_state',3);t.g['cw_sr_window_mars']=D(0)
        t.c.flags.update('cw_sr_p'+str(ids[group[0]])+'_awarded' for group in REQUIREMENTS[p['id']])
        t.rolls.append(0);t.call('cw_sr_p84_launch');check(t.get('cw_sr_p84_state')==4 and 'cw_sr_cap_crewed_mars_return' not in t.c.flags,'Mars return granted at departure')
        t.put('cw_sr_p84_days',1);t.rolls.append(0);t.call('cw_sr_daily')
        check(('news_event',event,tag) in t.events,'First Mars news did not use national image '+tag)
        check(t.get('cw_sr_prestige')==580,'Mars first reward incorrect')
        old=t.get('cw_sr_prestige');bonuses=len(t.c.tech_bonuses)
        for _ in range(50):t.call('cw_sr_p84_success')
        check(t.get('cw_sr_prestige')<=old+D(48) and len(t.c.tech_bonuses)==bonuses,'Repeated flight reward farming')
        t.c=t.countries['SAU'];t.init();t.call('cw_sr_p84_success');check(t.get('cw_sr_prestige')==320,'Second country received the world-first award')
    # Tiny-cost reviews must also terminate without zero denominators.
    for n,p in enumerate(DATA['programmes'],1):
        for kind,months in [('partial',3),('failure',6),('catastrophic',12)]:
            t=Machine(('SAU',));t.init();t.call(f'cw_sr_p{n}_{kind}');t.put('cw_sr_allocation',1000,True)
            for _ in range(math_ceil(months*52/12)+3):t.call(f'cw_sr_p{n}_week')
            check(t.get(f'cw_sr_p{n}_state')==3,p['id']+' review deadlock '+kind)
    # Shared ranking and upkeep reduction; no leader for a tie or an AI score.
    m=Machine();m.init()
    for t,score in [('SAU',10),('USA',20),('SOV',30)]:
        m.c=m.countries[t];m.init();m.put('cw_sr_prestige',score)
    m.call('cw_sr_rank');check(m.targets['cw_sr_rank1'].tag=='SOV','Wrong leader')
    m.c=m.countries['SOV'];m.c.flags.add('cw_sr_p1_deployed');before=m.get('treasury')
    for _ in range(52):m.call('cw_sr_p1_upkeep')
    check(abs(before-m.get('treasury')-D('2.28'))<=D('.002'),'Leader weekly upkeep is not reduced by five percent')
    m.c=m.countries['USA'];m.put('cw_sr_prestige',30);m.call('cw_sr_rank');check(not any('cw_sr_leader' in c.flags for c in m.countries.values()),'Tie conferred leadership')
    m.countries['SOV'].ai=True;m.call('cw_sr_rank');check('cw_sr_leader' in m.countries['USA'].flags,'AI retained leadership')
    m.c=m.countries['USA'];m.put('treasury',0);m.c.flags.add('cw_sr_p1_deployed');m.call('cw_sr_p1_upkeep');check(m.get('cw_sr_p1_arrears')>0,'Unpaid operating debt was discarded')
    for year,month,expected in [(1970,1,10),(1971,5,0),(1973,7,0)]:
        m.g['year']=D(year);m.g['month']=D(month);m.call('cw_sr_windows');check(m.g['cw_sr_window_mars']==expected,'Mars transfer window calendar drift')


def math_ceil(x):return int(-(-x//1))


if __name__=='__main__':
    static_checks();mechanics()
    result={'checks':CHECKS,'programmes':84,'policies_per_programme':4,'investigation_cases':252,'status':'passed','arithmetic':'three-decimal fixed-point stress execution of generated ASTs','in_game_tested':False}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result))
