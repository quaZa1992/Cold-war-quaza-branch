# IMPERIA COLD WAR — French bilateral offer compiler
"""Compile France offers with the user-authorized permanent compact lifecycle."""
from pathlib import Path
import json,re,importlib.util
_AST_SPEC=importlib.util.spec_from_file_location("coldwar_offer_script_ast",Path(__file__).resolve().parents[1]/"vietnam_1970/script_ast.py")
_AST=importlib.util.module_from_spec(_AST_SPEC)
_AST_SPEC.loader.exec_module(_AST)
ROOT=Path(__file__).resolve().parents[2]
p=Path(__file__).with_name('approved_design.json')
d=json.loads(p.read_text(encoding='utf-8-sig')); offers=d['offers']; assert len(offers)==24
policy=json.loads(p.with_name('offer_policy.json').read_text(encoding='utf-8'))
assert policy['compact_duration_days'] is None and policy['compact_survives_government_change']
H='# IMPERIA COLD WAR — French bilateral offers\n'
effects=[H]; decisions=[H+'COLDWAR_FRA_offers = {']; events=[H+'add_namespace = COLDWAR_FRA_OFFERS']; ideas=[H+'ideas = { country = {']; loc={'COLDWAR_FRA_offers':'French Bilateral Agreements','COLDWAR_FRA_offers_desc':'France may submit a bilateral agreement for consideration by a sovereign government. Acceptance requires both governments to meet the quoted conditions.','COLDWAR_FRA_offer_accept':'Accept the agreement','COLDWAR_FRA_offer_decline':'Decline the proposal','COLDWAR_FRA_offer_withdraw':'Withdraw from the bilateral compact'}
tags=sorted({p.name[:3] for p in (ROOT/'history/countries').glob('*.txt') if re.match(r'^[A-Z0-9]{3} -',p.name)})
# Category eligibility is derived from complete technology blocks, not category names alone.
cats={c:[] for c in ('CAT_industry','CAT_construction')}
for f in (ROOT/'common/technologies').glob('*.txt'):
 s=re.sub(r'#.*','',f.read_text(encoding='utf-8-sig'))
 for m in re.finditer(r'^\s*([\w]+)\s*=\s*\{',s,re.M):
  dep=1;i=m.end()
  while dep and i<len(s):
   dep+=(s[i]=='{')-(s[i]=='}');i+=1
  b=s[m.end():i-1]
  for c in cats:
   if re.search(r'categories\s*=\s*\{[^}]*\b'+c+r'\b',b) and m.group(1) not in ('technologies',): cats[c].append(m.group(1))
for c in cats: cats[c]=sorted(set(cats[c])); assert cats[c],c

def block(k,b): return '# IMPERIA COLD WAR — French bilateral agreement '+k+'\n'+k+' = {\n'+b+'\n}\n'
def finance(side):
 out=[]
 for e in side['completion_effects']:
  if e['kind']=='treasury' and e['amount']<0: out.append('check_variable = { var = treasury value = '+str(-e['amount'])+' compare = greater_than_or_equals }')
  elif e['kind']=='political_power' and e['amount']<0: out.append('NOT = { has_political_power < '+str(-e['amount'])+' }')
  elif e['kind']=='tech_bonus': out.append('OR = { '+' '.join('NOT = { has_tech = '+t+' }' for t in cats[e['category']])+' }')
 return '\n'.join(out)
def award(side,idea=None):
 out=[]
 for e in side['completion_effects']:
  if e['kind']=='treasury': out.append('set_temp_variable = { treasury_change = '+str(e['amount'])+' } modify_treasury_effect = yes')
  elif e['kind']=='political_power': out.append('add_political_power = '+str(e['amount']))
  elif e['kind']=='tech_bonus': out.append('add_tech_bonus = { name = '+e['name']+' bonus = '+str(e['bonus'])+' uses = '+str(e['uses'])+' category = '+e['category']+' }')
  else: raise ValueError(e)
 if idea:out.append('add_ideas = '+idea)
 return '\n'.join(out)
def snapshots(scope):
 return 'check_variable = { var = ruling_party value = COLDWAR_FRA_quote_party compare = equals } check_variable = { var = COLDWAR_FRA_government_epoch value = COLDWAR_FRA_quote_epoch compare = equals }'
quote='set_variable = { COLDWAR_FRA_quote_party = ruling_party } set_variable = { COLDWAR_FRA_quote_epoch = COLDWAR_FRA_government_epoch }'
cleanup=[]; pending_maint=[]; compact_maint=[]; migrate=[]
relations='exists = yes is_subject = no NOT = { tag = FRA } NOT = { has_war_with = FRA } FRA = { exists = yes is_subject = no IMP_is_1970_scenario = yes } NOT = { OR = { '+' '.join('is_in_array = { array = imp_'+kind+'_sanc_'+direction+' value = FRA }' for kind in policy['terminate_on_bilateral_imperia_sanctions'] for direction in ('on_us','by_us'))+' } }'
relation_trigger='COLDWAR_FRA_offer_partner_relations_valid = { '+relations+' }'
loc['COLDWAR_FRA_offer_relations_tt']='The signatories are sovereign, are at peace with each other and impose no diplomatic, financial, economic or military sanctions on each other.'
loc['COLDWAR_FRA_offer_withdraw_desc']='Terminate the bilateral compact and remove its effects from both signatories.'
for n,o in enumerate(offers,1):
 k=o['focus'];id=o['id']; timed=bool(o['duration_days']); flag=id+'_pending';active=id+'_active';idea=id+'_treaty'; event='COLDWAR_FRA_OFFERS.'+str(n)
 for side in ('france','partner'):
  for effect in o[side]['completion_effects']:
   if effect['kind']=='tech_bonus': loc[effect['name']]=o['title']
 fra='exists = yes IMP_is_1970_scenario = yes is_subject = no COLDWAR_FRA_'+o['group']+'_government = yes has_country_flag = COLDWAR_FRA_'+k+'_earned '+snapshots('FRA')
 partner='COLDWAR_FRA_offer_partner_relations_valid = yes '+snapshots('partner')
 if not timed:
  fra+=' NOT = { has_country_flag = '+id+'_consumed }'
  partner+=' NOT = { has_country_flag = COLDWAR_FRA_research_pair_consumed }'
 else: fra+=' NOT = { has_country_flag = COLDWAR_FRA_compact_active }'
 accept='FRA = { has_country_flag = COLDWAR_FRA_offer_pending } tag = event_target:COLDWAR_FRA_offer_recipient has_country_flag = '+flag+' NOT = { has_country_flag = { flag = '+flag+' days > 89 } } '+partner+' '+finance(o['partner'])+' FRA = { '+fra+' '+finance(o['france'])+' }'
 clear='if = { limit = { has_country_flag = '+flag+' tag = event_target:COLDWAR_FRA_offer_recipient } FRA = { clr_country_flag = COLDWAR_FRA_offer_pending } clear_global_event_target = COLDWAR_FRA_offer_recipient } clr_country_flag = '+flag
 cleanup.append('clr_country_flag = '+flag)
 apply=award(o['partner'],idea if timed else None)+'\nFRA = { '+award(o['france'],idea if timed else None)
 if timed:
  # Establish both sides before adding ideas, so native cancel guards see a valid pair.
  apply='set_country_flag = '+active+' set_country_flag = COLDWAR_FRA_compact_partner save_global_event_target_as = COLDWAR_FRA_compact_partner FRA = { set_country_flag = COLDWAR_FRA_compact_active set_country_flag = COLDWAR_FRA_compact_permanent save_global_event_target_as = COLDWAR_FRA_compact_france '+award(o['france'],idea)+' } '+award(o['partner'],idea)
 else:apply+=' set_country_flag = '+id+'_consumed } set_country_flag = COLDWAR_FRA_research_pair_consumed'
 apply+='\n'+clear
 effects.append(block(id+'_accept','if = { limit = { '+accept+' } '+apply+' }'))
 effects.append(block(id+'_preview','effect_tooltip = { '+award(o['france'],idea if timed else None)+' FROM = { '+award(o['partner'],idea if timed else None)+' } }'))
 # Keep decision completion a pure invitation; the recipient event owns acceptance.
 send='FROM = { '+quote+' set_country_flag = '+flag+' save_global_event_target_as = COLDWAR_FRA_offer_recipient country_event = { id = '+event+' hours = 1 } } '+quote+' set_country_flag = COLDWAR_FRA_offer_pending'
 avail='hidden_trigger = { IMP_is_1970_scenario = yes COLDWAR_FRA_'+o['group']+'_government = yes } is_subject = no NOT = { has_country_flag = COLDWAR_FRA_offer_pending }'
 if timed:avail+=' NOT = { has_country_flag = COLDWAR_FRA_compact_active }'
 else:avail+=' NOT = { has_country_flag = '+id+'_consumed }'
 decisions.append(block(id,'icon = GFX_decision_generic_political_discourse\nallowed = { original_tag = FRA } cost = 0 fire_only_once = no\nvisible = { always = no }\navailable = { '+avail+' }\ntarget_root_trigger = { always = yes } target_non_existing = no targets = { '+' '.join(t for t in tags if t!='FRA')+' }\ntarget_trigger = { FROM = { custom_trigger_tooltip = { tooltip = COLDWAR_FRA_offer_relations_tt COLDWAR_FRA_offer_partner_relations_valid = yes } '+('NOT = { has_country_flag = COLDWAR_FRA_research_pair_consumed }' if not timed else '')+' } }\ncomplete_effect = { custom_effect_tooltip = TT_IF_THEY_ACCEPT '+id+'_preview = yes hidden_effect = { '+send+' } } ai_will_do = { factor = 0 }'))
 event_preview=award(o['partner'],idea if timed else None)+' FRA = { '+award(o['france'],idea if timed else None)+' }'
 events.append(block('country_event','id = '+event+' title = '+id+'_title desc = '+id+'_event_desc picture = GFX_message_signing is_triggered_only = yes\ntrigger = { has_country_flag = '+flag+' }\noption = { name = COLDWAR_FRA_offer_accept trigger = { '+accept+' } effect_tooltip = { '+event_preview+' } hidden_effect = { '+id+'_accept = yes } ai_chance = { factor = 30 } }\noption = { name = COLDWAR_FRA_offer_decline hidden_effect = { '+clear+' } ai_chance = { factor = 70 } }'))
 if timed:
  linked='OR = { AND = { tag = FRA has_country_flag = COLDWAR_FRA_compact_active event_target:COLDWAR_FRA_compact_partner = { exists = yes has_country_flag = '+active+' } } AND = { tag = event_target:COLDWAR_FRA_compact_partner has_country_flag = '+active+' FRA = { exists = yes has_country_flag = COLDWAR_FRA_compact_active } } }'
  ideas.append(block(idea,'picture = generic_diplomatic_treaty allowed = { always = no } removal_cost = -1 cancel = { NOT = { '+linked+' } } modifier = { '+' '.join(m+' = '+str(v) for m,v in o['france']['mods'].items())+' }'))
  loc[idea]=o['title'];loc[idea+'_desc']='An open-ended bilateral programme. It survives changes of government and ends on withdrawal, war between the signatories or sanctions imposed by either signatory on the other.'
  compact_maint.append('if = { limit = { has_country_flag = '+active+' OR = { NOT = { has_idea = '+idea+' } FRA = { NOT = { has_idea = '+idea+' } } } } COLDWAR_FRA_end_compact = yes }')
  migrate.append('if = { limit = { has_country_flag = '+active+' has_idea = '+idea+' FRA = { has_idea = '+idea+' } } remove_ideas = '+idea+' add_ideas = '+idea+' FRA = { remove_ideas = '+idea+' add_ideas = '+idea+' } }')
 loc[id]=o['title'];loc[id+'_desc']='Invite [From.GetName] to conclude '+o['title'].lower()+'. The recipient government decides whether to accept the reciprocal obligations.'
 loc[id+'_title']=o['title'];loc[id+'_event_desc']='France proposes a reciprocal agreement. Both governments must retain their quoted mandate and meet the agreed costs when accepting.'
 pending_maint.append('if = { limit = { has_country_flag = '+flag+' OR = { has_country_flag = { flag = '+flag+' days > 89 } NOT = { '+partner+' } FRA = { NOT = { '+fra+' } } } } '+clear+' }')
# Direct counterpart cleanup: there is no world-country scan, even on withdrawal.
remove='clr_country_flag = COLDWAR_FRA_compact_active clr_country_flag = COLDWAR_FRA_compact_partner clr_country_flag = COLDWAR_FRA_compact_permanent '+' '.join('remove_ideas = '+o['id']+'_treaty clr_country_flag = '+o['id']+'_active' for o in offers if o['duration_days'])
end='FRA = { event_target:COLDWAR_FRA_compact_partner = { '+remove+' } '+remove+' clear_global_event_target = COLDWAR_FRA_compact_partner clear_global_event_target = COLDWAR_FRA_compact_france }'
effects.append(block('COLDWAR_FRA_end_compact',end))
effects.append(block('COLDWAR_FRA_offer_maintenance','if = { limit = { tag = FRA } if = { limit = { has_country_flag = COLDWAR_FRA_compact_active } if = { limit = { NOT = { event_target:COLDWAR_FRA_compact_partner = { COLDWAR_FRA_offer_partner_relations_valid = yes has_country_flag = COLDWAR_FRA_compact_partner } } } COLDWAR_FRA_end_compact = yes } else = { if = { limit = { NOT = { has_country_flag = COLDWAR_FRA_compact_permanent } } event_target:COLDWAR_FRA_compact_partner = { '+' '.join(migrate)+' } set_country_flag = COLDWAR_FRA_compact_permanent } event_target:COLDWAR_FRA_compact_partner = { '+' '.join(compact_maint)+' } } } if = { limit = { has_country_flag = COLDWAR_FRA_offer_pending } if = { limit = { NOT = { event_target:COLDWAR_FRA_offer_recipient = { exists = yes } } } clr_country_flag = COLDWAR_FRA_offer_pending clear_global_event_target = COLDWAR_FRA_offer_recipient } else = { event_target:COLDWAR_FRA_offer_recipient = { '+' '.join(pending_maint)+' } } } }'))
signatory='OR = { AND = { tag = FRA has_country_flag = COLDWAR_FRA_compact_active } AND = { tag = event_target:COLDWAR_FRA_compact_partner has_country_flag = COLDWAR_FRA_compact_partner FRA = { has_country_flag = COLDWAR_FRA_compact_active } } }'
decisions.append(block('COLDWAR_FRA_offer_withdraw','icon = GFX_decision_generic_political_discourse cost = 0 visible = { '+signatory+' } complete_effect = { if = { limit = { '+signatory+' } COLDWAR_FRA_end_compact = yes } } ai_will_do = { factor = 0 }'))
decisions.append('}');ideas.append('} }')
outputs={'common/scripted_effects/COLDWAR_FRA_1970_offers.txt':'\n'.join(effects),'common/scripted_triggers/COLDWAR_FRA_1970_offer_triggers.txt':relation_trigger,'common/decisions/COLDWAR_FRA_1970_offers.txt':'\n'.join(decisions),'events/COLDWAR_FRA_1970_offers.txt':'\n'.join(events),'common/ideas/COLDWAR_FRA_1970_treaties.txt':'\n'.join(ideas),'common/decisions/categories/COLDWAR_FRA_1970_offers.txt':H+'COLDWAR_FRA_offers = { icon = GFX_decision_generic_political_discourse allowed = { always = yes } visible = { OR = { AND = { tag = FRA IMP_is_1970_scenario = yes } has_country_flag = COLDWAR_FRA_compact_partner } } }\n'}
# Audit player-facing references transitively, including research-award names.
required={'COLDWAR_FRA_offers','COLDWAR_FRA_offer_withdraw'}
for offer in offers:
 required.add(offer['id'])
 if offer['duration_days']: required.update((offer['id']+'_treaty',offer['id']+'_treaty_desc'))
for text in outputs.values():
 for key,op,value in _AST.walk(_AST.parse(text)):
  if key in ('custom_effect_tooltip','title','desc','name') and isinstance(value,str) and value.startswith('COLDWAR_FRA_'):
   required.add(value)
assert not (required-set(loc)), 'Unlocalised offer references: '+str(sorted(required-set(loc)))
for path,s in outputs.items():
 assert s.count('{')==s.count('}'),path
 # Preserve every generated block comment while formatting the semantic tree.
 before=_AST.parse(s)
 comments=re.findall(r'(?m)^(# IMPERIA COLD WAR — French bilateral agreement [^\n]+)\n([^\n]+?) = \{',s)
 formatted=_AST.format_code(s)
 rows=[];ci=0
 for line in formatted.splitlines():
  key=line.strip().split(' = ',1)[0]
  if ci<len(comments) and key==comments[ci][1]:
   rows.append(line[:len(line)-len(line.lstrip())]+comments[ci][0]);ci+=1
  rows.append(line)
 assert ci==len(comments),(path,ci,len(comments))
 s=H+'\n'.join(rows)+'\n'
 assert _AST.parse(s)==before,'Formatter changed semantics: '+path
 f=ROOT/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(s,encoding='utf-8')
f=ROOT/'localisation/english/COLDWAR_FRA_1970_offers_l_english.yml';f.parent.mkdir(parents=True,exist_ok=True);f.write_text(H+'l_english:\n'+''.join(' '+k+':0 "'+v.replace('"',"'")+'"\n' for k,v in loc.items()),encoding='utf-8-sig')
print('Compiled',len(offers),'consent offers;',sum(bool(o['duration_days']) for o in offers),'permanent compacts;',len(cats['CAT_industry']),len(cats['CAT_construction']),'category technologies.')
