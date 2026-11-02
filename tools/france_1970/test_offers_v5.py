# IMPERIA COLD WAR — Executable emitted-source tests for France v5 agreements.
"""A bounded Clausewitz AST model; no claim of native HOI4 execution."""
from pathlib import Path
from decimal import Decimal
from collections import defaultdict
import json, importlib.util, copy, re
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
spec=importlib.util.spec_from_file_location('v5_test_ast',HERE.parent/'vietnam_1970/script_ast.py');A=importlib.util.module_from_spec(spec);spec.loader.exec_module(A)
D=json.loads((HERE/'approved_design_v5.json').read_text(encoding='utf-8-sig'))
OLD=json.loads((HERE/'approved_design.json').read_text(encoding='utf-8-sig'))
def read(path):return A.parse((ROOT/path).read_text(encoding='utf-8-sig'))
def first(rows,key,default=None):return next((v for k,op,v in rows if k==key),default)
def table(rows):return {k:v for k,op,v in rows}
E=table(read('common/scripted_effects/COLDWAR_FRA_1970_v5_offers.txt'));E.update(table(read('common/scripted_effects/COLDWAR_FRA_1970_offers.txt')))
T=table(read('common/scripted_triggers/COLDWAR_FRA_1970_v5_offers.txt'));T.update(table(read('common/scripted_triggers/COLDWAR_FRA_1970_offer_triggers.txt')))
I=table(first(first(read('common/ideas/COLDWAR_FRA_1970_v5_offers.txt'),'ideas'),'country'));I.update(table(first(first(read('common/ideas/COLDWAR_FRA_1970_treaties.txt'),'ideas'),'country')))
DEC=table(first(read('common/decisions/COLDWAR_FRA_1970_v5_offers.txt'),'COLDWAR_FRA_v5_agreements'))
N={n['id']:n for n in D['nodes']};checks=0
CORE=table(read('common/scripted_effects/COLDWAR_FRA_1970_effects.txt'))
E.update({k:v for k,v in CORE.items() if k.startswith('COLDWAR_FRA_apply_v5_')})

def check(ok,message):
 global checks
 checks+=1
 assert ok,message

class Country:
 def __init__(self,tag):
  self.tag=tag;self.exists=True;self.subject=False;self.flags={};self.vars=defaultdict(Decimal);self.ideas=set();self.timed=set();self.arrays=defaultdict(set);self.wars=set();self.completed=set();self.gov='gaullist';self.pp=Decimal(1000);self.vars['treasury']=Decimal(1000)
class World:
 def __init__(self,bba=False):
  self.countries={t:Country(t) for t in {'FRA','USA',*[o['partner'] for o in D['offers']]}};self.targets={};self.temp={};self.day=0;self.bba=bba;self.skip_dead_effects=True
 def scope(self,s):return self.countries.get(self.targets.get(s.split(':',1)[1])) if s.startswith('event_target:') else self.countries.get(s)
 def val(self,c,v):
  try:return Decimal(str(v))
  except Exception:return c.vars[v]
 def compare(self,a,op,b):return {'=':a==b,'<':a<b,'>':a>b,'>=':a>=b,'<=':a<=b,'equals':a==b,'greater_than_or_equals':a>=b}[op]
 def cond(self,c,rows,any_=False):
  rs=[]
  for k,op,v in rows:
   if k in ('AND','hidden_trigger','custom_trigger_tooltip'):r=self.cond(c,v)
   elif k=='OR':r=self.cond(c,v,True)
   elif k=='NOT':r=not self.cond(c,v)
   elif k.endswith('_government') and k.startswith('COLDWAR_FRA_'):r=c.gov==k[len('COLDWAR_FRA_'):-len('_government')]
   elif k in T:r=self.cond(c,T[k])==(v=='yes')
   elif k in self.countries or k.startswith('event_target:'):
    target=self.scope(k);r=target is not None and self.cond(target,v)
   elif k in ('tag','original_tag'):
    target=self.scope(v);r=c.tag==(target.tag if target else v)
   elif k=='exists':r=c.exists==(v=='yes')
   elif k=='is_subject':r=c.subject==(v=='yes')
   elif k=='always':r=v=='yes'
   elif k=='IMP_is_1970_scenario':r=v=='yes'
   elif k=='has_dlc':r=(v.strip('"')=='By Blood Alone' and self.bba)
   elif k=='has_war_with':r=v in c.wars or c.tag in self.countries[v].wars
   elif k=='has_idea':r=v in c.ideas
   elif k=='has_completed_focus':r=v in c.completed
   elif k=='has_country_flag':
    if isinstance(v,list):
     name=first(v,'flag');age=next((o,Decimal(x)) for key,o,x in v if key=='days');r=name in c.flags and self.compare(Decimal(self.day-c.flags[name]),age[0],age[1])
    else:r=v in c.flags
   elif k=='check_variable':
    if first(v,'var'):r=self.compare(self.val(c,first(v,'var')),first(v,'compare','equals'),self.val(c,first(v,'value')))
    else:
     name,operation,value=v[0];r=self.compare(self.val(c,name),operation,self.val(c,value))
   elif k=='has_political_power':r=self.compare(c.pp,op,Decimal(v))
   elif k=='has_event_target':r=self.scope('event_target:'+v) is not None
   elif k=='is_in_array':r=first(v,'value') in c.arrays[first(v,'array')]
   elif k in ('tooltip','localization_key'):continue
   else:raise AssertionError('Unsupported condition '+str((k,op,v)))
   rs.append(r)
  return any(rs) if any_ else all(rs)
 def effect(self,c,rows):
  previous=None
  for k,op,v in rows:
   if k=='if':
    previous=self.cond(c,first(v,'limit',[]))
    if previous:self.effect(c,[r for r in v if r[0]!='limit'])
   elif k=='else':
    if previous is False:self.effect(c,v)
    previous=None
   elif k in ('hidden_effect',):self.effect(c,v)
   elif k in ('effect_tooltip','custom_effect_tooltip','log'):continue
   elif k=='COLDWAR_FRA_refresh_programmes':
    self.call('FRA','COLDWAR_FRA_offer_maintenance');self.call('FRA','COLDWAR_FRA_v5_offer_maintenance')
   elif k in E:self.effect(c,E[k])
   elif k in self.countries or k.startswith('event_target:'):
    target=self.scope(k)
    if target is not None and (target.exists or not self.skip_dead_effects):self.effect(target,v)
   elif k=='set_country_flag':c.flags[v]=self.day
   elif k=='clr_country_flag':c.flags.pop(v,None)
   elif k=='set_variable':
    name,operation,value=v[0];c.vars[name]=self.val(c,value)
   elif k=='set_temp_variable':
    name,operation,value=v[0];self.temp[name]=self.val(c,value)
   elif k=='modify_treasury_effect':
    if 'MD_skip_treasury_cost' not in c.flags:c.vars['treasury']+=self.temp['treasury_change']
   elif k=='add_political_power':c.pp+=Decimal(v)
   elif k=='add_ideas':
    # Native cancel guard is exercised immediately, not only after both grants finish.
    if v not in I or not self.cond(c,first(I[v],'cancel',[])):c.ideas.add(v)
   elif k=='remove_ideas':c.ideas.discard(v);c.timed.discard(v)
   elif k=='save_global_event_target_as':self.targets[v]=c.tag
   elif k=='clear_global_event_target':self.targets.pop(v,None)
   else:raise AssertionError('Unsupported effect '+str((k,op,v)))
 def call(self,tag,key):self.effect(self.countries[tag],E[key])
 def condition(self,tag,key):return self.cond(self.countries[tag],T[key])
 def seed(self,o):
  f=self.countries['FRA'];f.gov=o['group'];f.vars['ruling_party']=Decimal(next(g for g in D['groups'] if g['id']==o['group'])['slots'][0]);f.completed.add(o['id'])
  for group in N[o['id']]['parents']:
   for k in group:f.flags['COLDWAR_FRA_'+k+'_earned']=self.day
 def send(self,o):self.seed(o);self.call('FRA',o['id']+'_send')
 def accept(self,o):self.call(o['partner'],o['id']+'_accept')
 def maintain(self):self.call('FRA','COLDWAR_FRA_v5_offer_maintenance')
 def balances(self):return {t:(c.pp,c.vars['treasury']) for t,c in self.countries.items()}
 def snapshot(self):return copy.deepcopy({t:(c.pp,dict(c.vars),dict(c.flags),set(c.ideas)) for t,c in self.countries.items()})
 def active(self,o):return all(o['id']+'_'+s+'_spirit' in str(self.countries[tag].ideas) for tag,s in [('FRA','france'),(o['partner'],'partner')])
 def decision(self,tag,name):self.effect(self.countries[tag],first(DEC[name],'complete_effect',[]))

def native_actions(w,c,rows,temp=None):
 # Read prospective and actual effect ASTs independently; ignore bookkeeping, retain scope/amount.
 temp={} if temp is None else temp;out=[];previous=None
 for k,op,v in rows:
  if k=='if':
   previous=w.cond(c,first(v,'limit',[]))
   if previous:out+=native_actions(w,c,[r for r in v if r[0]!='limit'],temp)
  elif k=='else':
   if previous is False:out+=native_actions(w,c,v,temp)
   previous=None
  elif k=='effect_tooltip' or k=='hidden_effect':out+=native_actions(w,c,v,temp)
  elif k in E:out+=native_actions(w,c,E[k],temp)
  elif k in w.countries:out+=native_actions(w,w.countries[k],v,temp)
  elif k=='set_temp_variable':
   name,operation,value=v[0];temp[name]=w.val(c,value)
  elif k=='modify_treasury_effect':out.append((c.tag,'treasury',str(temp['treasury_change'])))
  elif k=='add_political_power':out.append((c.tag,'political_power',str(Decimal(v))))
  elif k=='add_ideas':out.append((c.tag,'idea',v))
 return out

for o in D['offers']:
 O=o['id'];P=o['partner'];fam=o['family'];av='COLDWAR_FRA_v5_'+fam+'_active'
 for bba in (False,True):
  w=World(bba);w.seed(o);before=w.balances();check(w.condition('FRA',O+'_can_send'),'Cannot send '+O);w.call('FRA',O+'_send');check(w.balances()==before,'Sending charged acceptance/focus PP '+O)
  actual=sorted(native_actions(w,w.countries[P],E[O+'_accept']))
  check(sorted(native_actions(w,w.countries['FRA'],E[O+'_focus_preview']))==actual,'Focus native preview differs from real transaction '+O)
  check(sorted(native_actions(w,w.countries[P],E[O+'_recipient_preview']))==actual,'Recipient native preview differs from real transaction '+O)
  w.accept(o)
  check(w.active(o),'Missing bilateral native idea '+O+' '+str(bba));check(all(w.countries[t].vars[av]>0 for t in ('FRA',P)),'Family not reserved '+O)
  for tag,side in [('FRA','france'),(P,'partner_terms')]:
   check(w.countries[tag].pp==before[tag][0]+Decimal(o[side]['political_power']),'PP amount '+O)
   check(w.countries[tag].vars['treasury']==before[tag][1]+Decimal(o[side]['treasury_millions'])/1000,'Treasury conversion '+O)
   ids=[i for i in w.countries[tag].ideas if i.startswith(O+'_')];check(len(ids)==1,'Stacked DLC variants '+O)
   idea=I[ids[0]];mods={k:Decimal(v) for k,op,v in first(idea,'modifier')};check(mods=={k:Decimal(str(v)) for k,v in o[side]['mods'].items()},'Modifier mismatch '+O)
   actual={k:Decimal(first(v,'build_cost_ic')) for k,op,v in first(idea,'equipment_bonus',[])};expected=defaultdict(Decimal)
   for alias,amount in o[side]['equipment'].items():
    targets=D['equipment_families'][alias]['targets'];classes=targets.get('all',targets.get('By Blood Alone' if bba else 'without By Blood Alone'))
    for cls in classes:expected[cls]+=Decimal(str(amount))
   check(actual==dict(expected),'Equipment class/value mismatch '+O)
  paid=w.balances();w.accept(o);w.call('FRA',O+'_send');w.maintain();check(w.balances()==paid,'Repeated acceptance/send/maintenance charged '+O)
  w.day=5000;w.countries['FRA'].gov='other';w.countries['FRA'].vars['COLDWAR_FRA_government_epoch']+=1;w.countries[P].vars['ruling_party']=99;w.countries[P].vars['COLDWAR_FRA_government_epoch']+=1;w.maintain();check(w.active(o),'Government or time ended permanent contract '+O)
 for who in ('FRA',P):
  for fund in ('pp','treasury'):
   w=World();w.send(o);side='france' if who=='FRA' else 'partner_terms';amount=-Decimal(o[side]['political_power']) if fund=='pp' else -Decimal(o[side]['treasury_millions'])/1000
   if fund=='pp':w.countries[who].pp=amount-Decimal('.00001')
   else:w.countries[who].vars['treasury']=amount-Decimal('.00001')
   before=w.balances();w.accept(o);check(w.balances()==before and not w.active(o),'Atomic funds check '+O+' '+who+' '+fund)
   if fund=='pp':w.countries[who].pp=amount
   else:w.countries[who].vars['treasury']=amount
   w.accept(o);check(w.active(o),'Exact affordability boundary rejected '+O)
 for reason in ('sender_epoch','sender_slot','missing_focus','missing_parent','expired','subject','deleted'):
  w=World();w.send(o)
  if reason=='sender_epoch':w.countries['FRA'].vars['COLDWAR_FRA_government_epoch']+=1
  if reason=='recipient_epoch':w.countries[P].vars['COLDWAR_FRA_government_epoch']+=1
  if reason=='sender_slot':w.countries['FRA'].vars['ruling_party']+=1
  if reason=='recipient_slot':w.countries[P].vars['ruling_party']+=1
  if reason=='missing_focus':w.countries['FRA'].completed.clear()
  if reason=='missing_parent':w.countries['FRA'].flags={k:v for k,v in w.countries['FRA'].flags.items() if not k.endswith('_earned')}
  if reason=='expired':w.day=90
  if reason=='subject':w.countries[P].subject=True
  if reason=='deleted':w.countries[P].exists=False
  before=w.balances();w.accept(o);w.maintain();check(w.balances()==before and not w.active(o),'Invalid pending accepted '+O+' '+reason);check(not w.countries['FRA'].vars['COLDWAR_FRA_v5_'+fam+'_pending'],'Invalid pending stuck '+O+' '+reason)
 for kind in ('dip','fin','eco','mil'):
  for direction in ('on_us','by_us'):
   array='imp_'+kind+'_sanc_'+direction
   w=World();w.send(o);w.countries[P].arrays[array].add('FRA');before=w.balances();w.accept(o);check(w.balances()==before and not w.active(o),'Sanctioned acceptance '+O+array)
   w=World();w.send(o);w.accept(o);paid=w.balances();w.countries[P].arrays[array].add('FRA');w.maintain();check(not w.active(o),'Sanction failed bilateral removal '+O+array);w.countries[P].arrays[array].clear();w.maintain();check(not w.active(o) and w.balances()==paid,'Sanction lifting regranted/charged '+O)
 for change in ('recipient_epoch','recipient_slot'):
  w=World();w.send(o)
  if change=='recipient_epoch':w.countries[P].vars['COLDWAR_FRA_government_epoch']+=1
  else:w.countries[P].vars['ruling_party']+=1
  w.maintain();w.accept(o);check(w.active(o),'Recipient government improperly vetoed its new consent '+O+change)
 w=World();w.seed(o);w.countries['FRA'].completed.clear();w.countries['FRA'].pp=0
 check(w.condition('FRA',O+'_can_send'),'Initial focus cannot dispatch after root PP debit/before focus receipt '+O)
 w.call('FRA',O+'_send');check(w.countries['FRA'].vars['COLDWAR_FRA_v5_'+fam+'_pending']>0,'Initial dispatch requires completed own focus '+O)
 for reason in ('war','reverse_war','subject','subject_france','deleted','missing_idea','missing_france_idea'):
  w=World();w.send(o);w.accept(o);paid=w.balances()
  if reason=='war':w.countries[P].wars.add('FRA')
  if reason=='reverse_war':w.countries['FRA'].wars.add(P)
  if reason=='subject_france':w.countries['FRA'].subject=True
  if reason=='missing_france_idea':w.countries['FRA'].ideas.clear()
  if reason=='subject':w.countries[P].subject=True
  if reason=='deleted':w.countries[P].exists=False
  if reason=='missing_idea':w.countries[P].ideas.clear()
  w.maintain();check(not w.countries['FRA'].vars[av] and not w.active(o),'Active cleanup '+O+reason);check(w.balances()==paid,'Cleanup refunded/charged '+O)
  if reason=='deleted':
   w.countries[P].exists=True;w.day=500;w.seed(o);check(w.condition('FRA',O+'_can_send'),'Restored recipient stale slots block reissue '+O)
 for tag in ('FRA',P):
  w=World();w.send(o);w.accept(o);paid=w.balances();w.decision(tag,O+'_withdraw_decision');check(not w.active(o) and w.balances()==paid,'Withdrawal '+O+tag)
 for action,tag in [('decline',P),('cancel','FRA')]:
  w=World();w.send(o);before=w.balances();w.decision(tag,O+'_'+action+'_decision');check(w.balances()==before and not w.countries['FRA'].vars['COLDWAR_FRA_v5_'+fam+'_pending'],'Pending choice charged or stuck '+O);w.day=179;check(not w.condition('FRA',O+'_can_send'),'Cooldown early '+O);w.day=180;check(w.condition('FRA',O+'_can_send'),'Cooldown not released '+O);w.decision('FRA',O+'_reissue_decision');w.accept(o);check(w.active(o),'Fixed reissue failed '+O)
 # Pure prospective blocks never execute any real grant/debit or bookkeeping.
 w=World();w.seed(o);before=w.snapshot();w.call('FRA',O+'_focus_preview');w.call(P,O+'_recipient_preview');check(w.snapshot()==before,'Preview executed '+O)
 for preview in (E[O+'_focus_preview'],E[O+'_recipient_preview']):check(not any(k in ('has_country_flag','check_variable',O+'_can_accept') for k,op,v in A.walk(preview)),'Prospective preview suppressed by live gate '+O)
 # Ordinary decisions actually belong to recipient, sender or the two fixed signatories.
 check(first(first(DEC[O+'_accept_decision'],'allowed'),'original_tag')==P,'Recipient does not own accept '+O)
 check(not any(k in ('target_trigger','targets','country_event') for k,op,v in A.walk(DEC[O+'_accept_decision'])),'Target-picker/event slipped into acceptance '+O)

# Family lock excludes all other offers of that family but never blocks the other five.
for chosen in D['offers']:
 w=World();w.send(chosen);w.accept(chosen)
 for other in D['offers']:
  w.seed(other);check(w.condition('FRA',other['id']+'_can_send')==(other['family']!=chosen['family']),'Family isolation '+chosen['id']+' '+other['id'])
w=World()
for fam in D['agreement_rules']['families']:
 o=next(o for o in D['offers'] if o['family']==fam);w.send(o);w.accept(o)
check(sum(bool(w.countries['FRA'].vars['COLDWAR_FRA_v5_'+f+'_active']) for f in D['agreement_rules']['families'])==6,'Six simultaneous family agreements unavailable')
paid=w.balances();w.maintain();check(w.balances()==paid,'Six-family maintenance charged')

# Execute each actually emitted core apply helper in the real completion ordering.
for o in D['offers']:
 w=World();w.seed(o);f=w.countries['FRA'];f.completed.clear();f.pp=Decimal(25)
 helper='COLDWAR_FRA_apply_'+o['key'];check(helper in E,'Missing integrated core apply helper '+o['id'])
 w.call('FRA',helper)
 check(f.pp==0,'Core initial focus PP charged incorrectly '+o['id'])
 check(o['id']+'_earned' in f.flags and f.vars['COLDWAR_FRA_v5_'+o['family']+'_pending']>0,'Completion-order refresh erased initial quote '+o['id'])
 check(not w.condition(o['partner'],o['id']+'_can_accept'),'Acceptance precedes actual focus completion '+o['id'])
 f.completed.add(o['id']);f.pp=Decimal(20);w.accept(o);check(w.active(o),'Integrated completed focus invitation cannot be accepted '+o['id'])
 paid=w.balances();w.call('FRA',helper);check(w.balances()==paid,'Completed core focus helper replayed PP charge '+o['id'])

# Two independent same-government quotes preserve their separate state, while a family cannot double-quote.
a=next(o for o in D['offers'] if any(x['group']==o['group'] and x['family']!=o['family'] for x in D['offers']))
b=next(o for o in D['offers'] if o['group']==a['group'] and o['family']!=a['family'])
w=World();w.send(a);w.send(b);w.maintain();check(w.condition(a['partner'],a['id']+'_pending_valid') and w.condition(b['partner'],b['id']+'_pending_valid'),'A second family overwrote the first quote');w.accept(a);w.accept(b);check(w.active(a) and w.active(b),'Separate same-government quotes cannot both be accepted')
for a in D['offers']:
 b=next((o for o in D['offers'] if o['family']==a['family'] and o['id']!=a['id']),None)
 if b:
  w=World();w.send(a);w.seed(b);before=w.snapshot();w.call('FRA',b['id']+'_send');check(w.snapshot()==before,'Second pending family quote overwrote first '+a['id'])
# A restored former counterparty cannot withdraw another partner's new agreement.
a=next(o for o in D['offers'] if any(x['family']==o['family'] and x['partner']!=o['partner'] for x in D['offers']))
b=next(o for o in D['offers'] if o['family']==a['family'] and o['partner']!=a['partner'])
w=World();w.send(a);w.accept(a);w.decision(a['partner'],a['id']+'_withdraw_decision');w.day=200;w.send(b);w.accept(b);paid=w.balances();w.countries[a['partner']].flags[a['id']+'_active']=0;w.countries[a['partner']].vars['COLDWAR_FRA_v5_'+a['family']+'_active']=1;w.decision(a['partner'],a['id']+'_withdraw_decision');check(w.active(b) and w.balances()==paid,'Stale former recipient withdrew current pair')

# Accepted legacy ideas and pending legacy quotes reserve exactly their mapped family.
from build_offers_v5 import LEGACY
for old in [o for o in OLD['offers'] if o['duration_days']]:
 fam=LEGACY[old['focus']];candidate=next(o for o in D['offers'] if o['family']==fam);w=World();w.seed(candidate);f=w.countries['FRA'];p=w.countries[candidate['partner']];idea=old['id']+'_treaty'
 f.ideas.add(idea);p.ideas.add(idea);f.flags['COLDWAR_FRA_compact_active']=0;p.flags['COLDWAR_FRA_compact_partner']=0;p.flags[old['id']+'_active']=0;w.targets['COLDWAR_FRA_compact_partner']=p.tag;w.targets['COLDWAR_FRA_compact_france']='FRA';f.flags['COLDWAR_FRA_compact_permanent']=0
 check(not w.condition('FRA',candidate['id']+'_can_send'),'Legacy accepted family not reserved '+old['id'])
 other=next(o for o in D['offers'] if o['family']!=fam);w.seed(other);check(w.condition('FRA',other['id']+'_can_send'),'Legacy compact incorrectly blocks all V5 families '+old['id']);w.seed(candidate)
 before=w.balances();w.call('FRA','COLDWAR_FRA_offer_maintenance');w.maintain();check(idea in f.ideas and idea in p.ideas and before==w.balances(),'Legacy acceptance lost/recharged '+old['id'])
 # Simulate a pre-permanent saved idea: existing legacy migration still works, without V5 rewriting it.
 f.flags.pop('COLDWAR_FRA_compact_permanent');f.timed.add(idea);p.timed.add(idea);w.call('FRA','COLDWAR_FRA_offer_maintenance');check(idea in f.ideas and idea in p.ideas and not f.timed and not p.timed and before==w.balances(),'Legacy migration regression '+old['id'])
 w=World();w.seed(candidate);w.targets['COLDWAR_FRA_offer_recipient']=candidate['partner'];w.countries[candidate['partner']].flags[old['id']+'_pending']=0;check(not w.condition('FRA',candidate['id']+'_can_send'),'Legacy pending family not reserved '+old['id'])
# No worldwide loops, irreversible research/design awards, temporal spirits or event dispatch.
rows=[r for k,v in E.items() if k.startswith('COLDWAR_FRA_v5_') for r in v]
check(not any(k in ('every_country','every_other_country','for_each_scope_loop','for_each_loop','add_timed_idea','add_tech_bonus','add_equipment_bonus','country_event') for k,op,v in A.walk(rows)),'Unbounded scan or finite award in V5')
olddec=table(first(read('common/decisions/COLDWAR_FRA_1970_offers.txt'),'COLDWAR_FRA_offers'))
for old in OLD['offers']:check(first(first(olddec[old['id']],'visible'),'always')=='no','Old target-picker still visible '+old['id'])
for path in ['common/scripted_effects','common/scripted_triggers','common/ideas','common/decisions','common/decisions/categories']:
 f=ROOT/path/'COLDWAR_FRA_1970_v5_offers.txt';raw=f.read_bytes();check(not raw.startswith(b'\xef\xbb\xbf') and raw.decode('utf-8').startswith('# IMPERIA COLD WAR —'),'Script BOM/marker '+str(f))
loc=(ROOT/'localisation/english/COLDWAR_FRA_1970_v5_offers_l_english.yml').read_bytes();check(loc.startswith(b'\xef\xbb\xbf'),'Localisation BOM missing')
print('PASS:',checks,'v5 emitted-source lifecycle, atomic funds, dual DLC, family, legacy migration and preview assertions. Engine tested: false.')
