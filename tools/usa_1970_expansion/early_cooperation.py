# IMPERIA COLD WAR — Early US cooperation and allied readiness revision.
"""User-requested legacy reward revision, independent of the approved snapshot.

Only this module's outputs are written. The existing agreement emitter is loaded
as a private, read-only API instance; its code and output files are not changed.
"""
from __future__ import annotations

import ast
from collections import OrderedDict
from decimal import Decimal
import importlib.util
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
OUT=HERE/'early_cooperation'
P='COLDWAR_USA_early'
STEM='COLDWAR_USA_1970_early_cooperation'
MARKER='# IMPERIA COLD WAR — Early US cooperation and allied readiness.\n'
ALLY_COST=Decimal('0.005')
ALLY_USA_ID=P+'_allied_readiness_usa'
ALLY_PARTNER_ID=P+'_allied_readiness_partner'
ROOTS={
 'USA_1970_F7': ('israel','Israeli Security Aid','A standing security-assistance programme gives both governments a practical relationship in training and defence supply. Industrial expansion remains a separate agreement requiring renewed Israeli consent.'),
 'USA_1970_E9': ('trade','North American Trade','Canada and Mexico each receive an independent proposal for industrial and commercial cooperation. Each government can accept or decline its own terms. Later supplier and border-industry investment remains a separate negotiation.'),
 'USA_1970_NIX_F3': ('alliances','Reassure the Alliances','Washington offers an allied-readiness programme to countries holding recognised NATO membership or major non-NATO ally status. Each government decides independently. American coordination remains one national institution, with additional weekly funding for every participating partner.'),
}


def parser():
 ns={'re':re}
 file=ROOT/'tools/israel_1970/validate_content.py'
 tree=ast.parse(file.read_text(encoding='utf-8'))
 definitions=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'tokens','parse','first','values','walk'}]
 exec(compile(ast.Module(body=definitions,type_ignores=[]),str(file),'exec'),ns)
 return ns


def render(tree):
 rows=[]
 for key,op,value in tree:
  if key=='_bare':rows.append(str(value))
  elif isinstance(value,list):rows.append(f'{key} {op} {{\n'+render(value)+'\n}')
  else:rows.append(f'{key} {op} {value}')
 return '\n'.join(rows)


def load_api():
 spec=importlib.util.spec_from_file_location('usa_early_agreement_api',HERE/'agreements.py')
 api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
 api.P=P;api.STEM=STEM;api.NAMESPACE=P;api.HERE=OUT
 api.BUILDINGS={};api.PARENTS={}
 api.PICTURES={'israel':'department_of_defense','canada':'trade','mexico':'trade'}
 api.FOCUS_ICONS={'israel':'align_to_israel','canada':'diplomacy','mexico':'diplomacy'}
 return api


def base_nodes(api):
 data=[
  ('israel','ISR','Security Assistance Partnership','American Security Assistance',
   ['Weekly programme expense: -$0.01 billion','Army experience gain: +5%','Production efficiency retention: +3%','Equipment cost: +1%'],
   ['Division organisation: +4%','Organisation regain: +4%','Equipment cost: -2%','Personnel cost: +2%'],ROOTS['USA_1970_F7'][2]),
  ('canada','CAN','Canadian Industrial Cooperation','Continental Trade Cooperation',
   ['Weekly programme expense: -$0.005 billion','Factory output: +2%','Production efficiency retention: +3%','Tax collection efficiency: -1%'],
   ['Factory output: +3%','Production efficiency growth: +3%','Tax collection efficiency: -1%'],ROOTS['USA_1970_E9'][2]),
  ('mexico','MEX','Mexican Industrial Cooperation','Border Trade Cooperation',
   ['Weekly programme expense: -$0.005 billion','Factory output: +2%','Production efficiency growth: +3%','Tax collection efficiency: -1%'],
   ['Factory output: +3%','Production efficiency growth: +3%','Education cost: +2%'],ROOTS['USA_1970_E9'][2]),
 ]
 result=[]
 for i,(s,t,us_name,partner_name,us_rows,partner_rows,desc) in enumerate(data):
  terms={'USA':dict(spirit=us_name,effects=us_rows),t:dict(spirit=partner_name,effects=partner_rows)}
  result.append(dict(id=P+'_contract_'+s,suffix=s,index=i,name=ROOTS['USA_1970_F7'][1] if s=='israel' else 'North American Trade: '+('Canada' if t=='CAN' else 'Mexico'),description=desc,
   partners=[t],duration=0,offer=terms,terms={tag:api.parse_terms(s,tag,rows) for tag,rows in terms.items()}))
 return result


def eligibility(api):
 sanctions=' '.join(f'is_in_array = {{ array = imp_{kind}_sanc_{direction}_us value = USA }}' for kind in ('dip','fin','eco','mil') for direction in ('on','by'))
 reverse=' '.join(f'is_in_array = {{ array = imp_{kind}_sanc_{direction}_us value = PREV }}' for kind in ('dip','fin','eco','mil') for direction in ('on','by'))
 return {
  P+'_alliance_relations_clear': '\n'.join(['exists = yes','NOT = { tag = USA }','country_exists = USA','IMP_is_1970_scenario = yes',
   'NOT = { has_war_with = USA }','NOT = { is_embargoing = USA }',f'NOT = {{ OR = {{ {sanctions} }} }}',
   'USA = { NOT = { has_war_with = PREV } NOT = { is_embargoing = PREV } NOT = { OR = { '+reverse+' } } }']),
  P+'_alliance_member': 'country_exists = USA\nUSA = { has_idea = NATO_member }\nOR = { has_idea = NATO_member has_idea = Major_Non_NATO_Ally }',
  P+'_alliance_can_offer': f'{P}_alliance_relations_clear = yes\n{P}_alliance_member = yes\nUSA = {{ has_country_flag = {P}_alliances_authorised }}\nNOT = {{ has_country_flag = {P}_alliance_signed }}\nNOT = {{ has_country_flag = {P}_alliance_pending }}\nNOT = {{ has_country_flag = {P}_alliance_cooldown }}\nNOT = {{ has_country_flag = {P}_alliance_sender_blocked }}',
  P+'_alliance_accept_valid': f'{P}_alliance_relations_clear = yes\n{P}_alliance_member = yes\nhas_country_flag = {P}_alliance_pending\nhas_country_flag = {P}_alliance_sponsor_authorised\nNOT = {{ has_country_flag = {P}_alliance_signed }}\nNOT = {{ has_country_flag = {P}_alliance_sender_blocked }}\nUSA = {{ has_country_flag = {P}_alliances_authorised }}',
  P+'_alliance_active': f'{P}_alliance_relations_clear = yes\n{P}_alliance_member = yes\nhas_country_flag = {P}_alliance_signed\nhas_idea = {ALLY_PARTNER_ID}\nUSA = {{ has_country_flag = {P}_alliances_authorised has_idea = {ALLY_USA_ID} is_in_array = {{ array = {P}_alliance_accepted value = PREV }} }}',
 }


def alliance_preview(api,individual=False):
 def mod(key,value):return f'add_to_variable = {{ {P}_preview_{key} = {value} tooltip = {P}_mod_{key}_tt }}'
 us='\n'.join([f'add_ideas = {ALLY_USA_ID}',mod('army_org_factor','0.02'),mod('experience_gain_army_factor','0.05'),mod('personnel_cost_multiplier_modifier','0.02'),f'add_doctrine_cost_reduction = {{ name = {P}_allied_usa_doctrine cost_reduction = 0.5 uses = 1 category = land_doctrine }}'])
 partner='\n'.join([f'add_ideas = {ALLY_PARTNER_ID}',mod('army_org_factor','0.03'),mod('supply_consumption_factor','-0.03'),mod('personnel_cost_multiplier_modifier','0.02'),f'add_doctrine_cost_reduction = {{ name = {P}_allied_partner_doctrine cost_reduction = 0.5 uses = 1 category = land_doctrine }}'])
 cost=f'add_to_variable = {{ {P}_preview_weekly = -{api.number(ALLY_COST)} tooltip = {P}_weekly_expense_tt }}'
 if individual:
  # Complete prospective institutional terms always remain inspectable. The
  # single shared USA idea cannot stack, and doctrine grants have real receipts.
  us=us.rsplit('\n',1)[0]+f'\nif = {{ limit = {{ NOT = {{ has_country_flag = {P}_alliance_usa_grant_received }} }} {us.rsplit(chr(10),1)[1]} }}'
  partner=partner.rsplit('\n',1)[0]+f'\nif = {{ limit = {{ NOT = {{ has_country_flag = {P}_alliance_grant_received }} }} {partner.rsplit(chr(10),1)[1]} }}'
  return api.block('effect_tooltip',[f'custom_effect_tooltip = {P}_if_accept_tt',api.scoped('USA',us+'\n'+cost),partner])
 # The recipient template is unconditional. It remains inspectable even when
 # no country currently holds the required membership or relations are blocked.
 # Bare native effects beneath a recipient heading do not name an unrelated tag.
 return api.block('effect_tooltip',[f'custom_effect_tooltip = {P}_if_accept_tt',api.scoped('USA',us),
  f'custom_effect_tooltip = {P}_each_partner_tt',partner,f'custom_effect_tooltip = {P}_each_partner_cost_tt',api.scoped('USA',cost)])


def emit_alliance(api):
 b=api.block
 flags=lambda name,days:f'set_country_flag = {{ flag = {P}_{name} value = 1 days = {days} }}'
 fx=OrderedDict()
 fx[P+'_alliance_preview']=alliance_preview(api)
 fx[P+'_alliance_recipient_preview']=alliance_preview(api,True)
 fx[P+'_alliance_send_to_recipient']=b('if',[f'limit = {{ {P}_alliance_can_offer = yes }}',flags('alliance_pending',90),f'set_country_flag = {P}_alliance_sponsor_authorised',f'set_country_flag = {P}_alliance_ever_offered',
  f'USA = {{ if = {{ limit = {{ NOT = {{ is_in_array = {{ array = {P}_alliance_offered value = PREV }} }} }} add_to_array = {{ array = {P}_alliance_offered value = PREV }} }} }}',f'country_event = {{ id = {P}.900 }}'])
 fx[P+'_alliance_record_candidate']=b('if',[f'limit = {{ exists = yes NOT = {{ tag = USA }} country_exists = USA OR = {{ has_idea = NATO_member has_idea = Major_Non_NATO_Ally }} USA = {{ has_country_flag = {P}_alliances_authorised }} }}',
  f'USA = {{ if = {{ limit = {{ NOT = {{ is_in_array = {{ array = {P}_alliance_offered value = PREV }} }} }} add_to_array = {{ array = {P}_alliance_offered value = PREV }} }} }}',
  P+'_alliance_send_to_recipient = yes'])
 fx[P+'_alliance_dispatch']=b('if',[f'limit = {{ tag = USA IMP_is_1970_scenario = yes has_country_flag = {P}_alliances_authorised }}',b('every_country',[f'limit = {{ NOT = {{ tag = USA }} OR = {{ has_idea = NATO_member has_idea = Major_Non_NATO_Ally }} }}',P+'_alliance_record_candidate = yes'])])
 fx[P+'_membership_changed']=f'if = {{ limit = {{ country_exists = USA }} USA = {{ {P}_reconcile_all = yes }} }}\n'+b('if',[f'limit = {{ tag = USA IMP_is_1970_scenario = yes has_country_flag = {P}_alliances_authorised has_idea = NATO_member }}',P+'_alliance_dispatch = yes'])+'\n'+b('else_if',[f'limit = {{ NOT = {{ tag = USA }} OR = {{ has_idea = NATO_member has_idea = Major_Non_NATO_Ally }} }}',P+'_alliance_record_candidate = yes'])
 fx[P+'_alliance_accept']=b('if',[f'limit = {{ {P}_alliance_accept_valid = yes }}',f'set_country_flag = {P}_alliance_signed',f'clr_country_flag = {P}_alliance_pending',
  f'if = {{ limit = {{ NOT = {{ has_country_flag = {P}_alliance_grant_received }} }} add_doctrine_cost_reduction = {{ name = {P}_allied_partner_doctrine cost_reduction = 0.5 uses = 1 category = land_doctrine }} set_country_flag = {P}_alliance_grant_received }}',
  f'USA = {{ if = {{ limit = {{ NOT = {{ is_in_array = {{ array = {P}_alliance_accepted value = PREV }} }} }} add_to_array = {{ array = {P}_alliance_accepted value = PREV }} }} if = {{ limit = {{ NOT = {{ has_country_flag = {P}_alliance_usa_grant_received }} }} add_doctrine_cost_reduction = {{ name = {P}_allied_usa_doctrine cost_reduction = 0.5 uses = 1 category = land_doctrine }} set_country_flag = {P}_alliance_usa_grant_received }} {P}_reconcile_all = yes }}'])
 fx[P+'_alliance_decline']=b('if',[f'limit = {{ NOT = {{ tag = USA }} has_country_flag = {P}_alliance_pending }}',f'clr_country_flag = {P}_alliance_pending',flags('alliance_cooldown',90)])
 fx[P+'_alliance_end']=b('if',[f'limit = {{ NOT = {{ tag = USA }} has_country_flag = {P}_alliance_signed }}',f'clr_country_flag = {P}_alliance_signed',f'clr_country_flag = {P}_alliance_pending',f'remove_ideas = {ALLY_PARTNER_ID}',flags('alliance_cooldown',90),
  f'if = {{ limit = {{ ROOT = {{ tag = USA }} }} set_country_flag = {P}_alliance_sender_blocked clr_country_flag = {P}_alliance_sponsor_authorised }}',
  f'if = {{ limit = {{ country_exists = USA }} USA = {{ remove_from_array = {{ array = {P}_alliance_accepted value = PREV }} {P}_reconcile_all = yes }} }}'])
 # Only offered/accepted scopes are revisited. New members enter through the
 # native membership hook; there is no daily every_country scan.
 live=f'has_country_flag = {P}_alliance_signed {P}_alliance_relations_clear = yes {P}_alliance_member = yes USA = {{ has_country_flag = {P}_alliances_authorised }}'
 ally_reconcile=b('for_each_scope_loop',[f'array = {P}_alliance_accepted',b('if',[f'limit = {{ {live} }}',f'if = {{ limit = {{ NOT = {{ has_idea = {ALLY_PARTNER_ID} }} }} add_ideas = {ALLY_PARTNER_ID} }}',f'USA = {{ add_to_variable = {{ {P}_alliance_active_count = 1 }} add_to_variable = {{ {P}_alliance_weekly_expense = {api.number(ALLY_COST)} }} }}'])+'\n'+b('else',[f'remove_ideas = {ALLY_PARTNER_ID}'])])
 initial_retries=[]
 for s in ('israel','canada','mexico'):
  initial_retries.append(b('if',[f'limit = {{ has_country_flag = {api.flag(s,"authorised")} NOT = {{ has_country_flag = {api.flag(s,"ever_offered")} }} {P}_can_offer_{s} = yes }}',P+'_send_'+s+' = yes']))
 queued=b('for_each_scope_loop',[f'array = {P}_alliance_offered',b('if',[f'limit = {{ NOT = {{ has_country_flag = {P}_alliance_ever_offered }} {P}_alliance_can_offer = yes }}',P+'_alliance_send_to_recipient = yes'])])
 fx[P+'_reconcile_all']=b('if',['limit = { tag = USA IMP_is_1970_scenario = yes }',P+'_base_reconcile_all = yes',*initial_retries,queued,f'set_variable = {{ {P}_alliance_active_count = 0 }}',f'set_variable = {{ {P}_alliance_weekly_expense = 0 }}',ally_reconcile,
  b('if',[f'limit = {{ check_variable = {{ {P}_alliance_active_count > 0 }} }}',f'if = {{ limit = {{ NOT = {{ has_idea = {ALLY_USA_ID} }} }} add_ideas = {ALLY_USA_ID} }}'])+'\n'+b('else',[f'remove_ideas = {ALLY_USA_ID}'])])
 fx[P+'_calculate_weekly_streams']='\n'.join([P+'_base_calculate_weekly_streams = yes',f'set_variable = {{ {P}_alliance_weekly_expense = 0 }}',b('if',['limit = { tag = USA IMP_is_1970_scenario = yes }',b('for_each_scope_loop',[f'array = {P}_alliance_accepted',b('if',[f'limit = {{ {P}_alliance_active = yes }}',f'USA = {{ add_to_variable = {{ {P}_weekly_expense = {api.number(ALLY_COST)} }} add_to_variable = {{ {P}_alliance_weekly_expense = {api.number(ALLY_COST)} }} }}'])])])])
 return fx


def root_helpers(api,nodes):
 b=api.block;fx={}
 for fid,(name,_,_) in ROOTS.items():
  chosen=[n for n in nodes if n['suffix']==name or name=='trade' and n['suffix'] in ('canada','mexico')]
  preview=P+'_alliance_preview = yes' if name=='alliances' else '\n'.join(P+'_preview_'+n['suffix']+' = yes' for n in chosen)
  fx[P+'_preview_root_'+name]=preview
  if name=='alliances':authorise=[f'set_country_flag = {P}_alliances_authorised',P+'_alliance_dispatch = yes']
  else:
   authorise=[f'set_country_flag = {P}_root_{name}_authorised']
   for n in chosen:
    s=n['suffix'];authorise += [f'set_country_flag = {api.flag(s,"unlocked")}',f'set_country_flag = {api.flag(s,"authorised")}',f'{P}_send_{s} = yes']
  fx[P+'_authorise_root_'+name]=b('if',['limit = { tag = USA IMP_is_1970_scenario = yes }']+authorise)
  gate='tag = USA IMP_is_1970_scenario = yes'+(' has_country_flag = USA_1970_nixon_presidency has_idea = NATO_member' if name=='alliances' else '')
  fx[P+'_complete_root_'+name]=preview+'\n'+b('hidden_effect',[b('if',[f'limit = {{ {gate} }}',P+'_authorise_root_'+name+' = yes'])])
 migrations=[]
 for fid,(name,_,_) in ROOTS.items():
  auth=P+'_alliances_authorised' if name=='alliances' else P+'_root_'+name+'_authorised'
  migrations.append(b('if',[f'limit = {{ has_completed_focus = {fid} NOT = {{ has_country_flag = {auth} }} }}',P+'_authorise_root_'+name+' = yes']))
 fx[P+'_initialize']=b('if',['limit = { tag = USA IMP_is_1970_scenario = yes }',
  b('if',[f'limit = {{ NOT = {{ has_country_flag = {P}_initialized }} }}',f'set_country_flag = {P}_initialized']+migrations),P+'_reconcile_all = yes'])
 return fx


def alliance_ideas(api):
 b=api.block
 return b(ALLY_USA_ID,['picture = NATO_member','allowed = { always = no }','allowed_civil_war = { always = no }','cancel = { NOT = { tag = USA } }','modifier = { army_org_factor = 0.02 experience_gain_army_factor = 0.05 personnel_cost_multiplier_modifier = 0.02 custom_modifier_tooltip = '+P+'_alliance_weekly_tt }'])+'\n'+b(ALLY_PARTNER_ID,['picture = NATO_member','allowed = { always = no }','allowed_civil_war = { always = no }','cancel = { OR = { tag = USA NOT = { country_exists = USA } } }','modifier = { army_org_factor = 0.03 supply_consumption_factor = -0.03 personnel_cost_multiplier_modifier = 0.02 }'])


def alliance_event(api):
 b=api.block
 return b('country_event',[f'id = {P}.900',f'title = {P}_alliance_title',f'desc = {P}_alliance_desc','picture = GFX_political_deal','is_triggered_only = yes',f'trigger = {{ NOT = {{ tag = USA }} has_country_flag = {P}_alliance_pending }}',
  b('option',[f'name = {P}_accept',f'trigger = {{ {P}_alliance_accept_valid = yes }}',P+'_alliance_recipient_preview = yes',f'hidden_effect = {{ {P}_alliance_accept = yes }}','ai_chance = { base = 70 }']),
  b('option',[f'name = {P}_decline',f'hidden_effect = {{ {P}_alliance_decline = yes }}','ai_chance = { base = 30 }']),
  b('option',[f'name = {P}_review','ai_chance = { base = 0 }'])])


def alliance_decisions(api):
 b=api.block
 def decision(name,visible,available,effect,ai=0):return b(P+'_'+name,['icon = generic_diplomacy','cost = 0','days_remove = 1',b('visible',[visible]),b('available',[available]),b('complete_effect',[effect]),f'ai_will_do = {{ base = {ai} }}'])
 pending=f'NOT = {{ tag = USA }} has_country_flag = {P}_alliance_pending'
 out=[decision('alliance_accept',pending,P+'_alliance_accept_valid = yes',P+'_alliance_recipient_preview = yes\nhidden_effect = { '+P+'_alliance_accept = yes }',4),
  decision('alliance_decline',pending,pending,P+'_alliance_decline = yes',1),
  decision('alliance_reopen',f'NOT = {{ tag = USA }} has_country_flag = {P}_alliance_ever_offered NOT = {{ has_country_flag = {P}_alliance_signed }} NOT = {{ has_country_flag = {P}_alliance_pending }}',P+'_alliance_can_offer = yes',P+'_alliance_send_to_recipient = yes'),
  decision('alliance_end',f'NOT = {{ tag = USA }} has_country_flag = {P}_alliance_signed',f'has_country_flag = {P}_alliance_signed',P+'_alliance_end = yes')]
 out.append(b(P+'_alliance_end_partner',['icon = generic_diplomacy',f'target_array = {P}_alliance_accepted','target_root_trigger = { tag = USA }',f'target_trigger = {{ FROM = {{ has_country_flag = {P}_alliance_signed }} }}','cost = 0','days_remove = 1',f'complete_effect = {{ FROM = {{ {P}_alliance_end = yes }} }}','ai_will_do = { base = 0 }']))
 return '\n'.join(out)


def make_specs(api,nodes):
 focuses={}
 for fid,(name,title,desc) in ROOTS.items():
  available='hidden_trigger = { tag = USA IMP_is_1970_scenario = yes }'
  if name=='alliances':available+='\nhas_idea = NATO_member\ncustom_trigger_tooltip = { tooltip = '+P+'_nixon_in_office_tt has_country_flag = USA_1970_nixon_presidency }'
  else:
   selected=[n for n in nodes if n['suffix']==name or name=='trade' and n['suffix'] in ('canada','mexico')]
   clauses=' '.join(P+'_can_offer_'+n['suffix']+' = yes' for n in selected)
   available+=f'\ncustom_trigger_tooltip = {{ tooltip = {P}_{name}_counterparts_tt OR = {{ {clauses} }} }}'
  focuses[fid]=dict(id=fid,name=title,description=desc,available=available,replace_legacy_available=True,completion_reward=P+'_complete_root_'+name+' = yes',completion_preview=P+'_preview_root_'+name+' = yes',icon='blr_nato_cooperation' if name=='alliances' else 'align_to_israel' if name=='israel' else 'diplomacy',replace_legacy_completion=True)
 followups={}
 for suffix,fid,root,tag in [('israel','USA_X_israel','USA_1970_F7','ISR'),('canada','USA_X_canada','USA_1970_E9','CAN'),('mexico','USA_X_mexico','USA_1970_E9','MEX')]:
  followups[fid]=dict(prerequisites=[[root]],runtime_guard=P+'_active_'+suffix+' = yes',public_guard=f'has_idea = {api.idea(suffix,"USA")}\n{tag} = {{ has_idea = {api.idea(suffix,tag)} }}',parent_ideas={'USA':api.idea(suffix,'USA'),tag:api.idea(suffix,tag)})
 return dict(project='IMPERIA COLD WAR',revision='User-requested legacy reward upgrade',focuses=focuses,followups=followups,
  hooks=dict(initialize=P+'_initialize',reconcile=P+'_reconcile_all',streams=P+'_calculate_weekly_streams',income_variable=P+'_weekly_income',expense_variable=P+'_weekly_expense',alliance_only_expense_variable=P+'_alliance_weekly_expense',membership_changed=P+'_membership_changed',membership_hook_scope='Country after native NATO/MNNA admission or removal; USA readmission performs a one-off dispatch'),
  legacy_replaced=list(ROOTS),new_focus_count=0,base_contracts=3,alliance_partner_pool='Any existing country holding NATO_member or Major_Non_NATO_Ally; no static tag whitelist',alliance_cost_per_partner=str(ALLY_COST),alliance_usa_spirit=ALLY_USA_ID,
  migration='Completed old roots authorise actual offers without setup fees or automatic spirits. Parent must retire their old legacy execution/retry bundles and remove old recurring helper deltas once, preserving historical payments.',
  implementation_notes=['No sender offer selector. Offers originate in their distinct roots; recipient decisions can reopen authorised terms.','No new status, faction, military access, territorial transfer, equipment or building is granted.','Advanced existing agreements retain their own accepted terms and costs; attach the published parent guards in offer availability, acceptance and ongoing readiness.'])


def build():
 api=load_api();ns=parser();parse,first=ns['parse'],ns['first'];nodes=base_nodes(api)
 # Replace only the three common API definition names. Their internal callers
 # continue to call the new combined authoritative hooks below.
 base_fx=api.emit_effects(nodes).replace(P+'_reconcile_all = {',P+'_base_reconcile_all = {',1).replace(P+'_calculate_weekly_streams = {',P+'_base_calculate_weekly_streams = {',1).replace(P+'_initialize = {',P+'_base_initialize = {',1)
 effects=base_fx+'\n'+'\n\n'.join(api.block(k,[v]) for k,v in {**emit_alliance(api),**root_helpers(api,nodes)}.items())+'\n'
 triggers=api.emit_triggers(nodes)+'\n'+'\n\n'.join(api.block(k,[v]) for k,v in eligibility(api).items())+'\n'
 idea_tree=parse(api.emit_ideas(nodes));country=first(first(idea_tree,'ideas'),'country');country.extend(first(parse(api.block('country',[alliance_ideas(api)])),'country'))
 ideas=MARKER+render(idea_tree)+'\n'
 events=api.emit_events(nodes)+'\n'+alliance_event(api)+'\n'
 category,decisions=api.emit_decisions(nodes)
 # Fixed ISR/CAN/MEX terms use native recipient controls. There is deliberately
 # no USA sender offer-selection or renewal menu in this revision.
 visible_flags=' '.join('has_country_flag = '+P+'_'+f for f in ('root_israel_authorised','root_trade_authorised','alliances_authorised','alliance_ever_offered','israel_ever_offered','canada_ever_offered','mexico_ever_offered'))
 category=MARKER+api.block(STEM,['icon = generic_diplomacy','priority = 206','allowed = { always = yes }','visible = { IMP_is_1970_scenario = yes OR = { '+visible_flags+' } }'])+'\n'
 decision_tree=parse(decisions);entries=first(decision_tree,STEM)
 entries[:]=[entry for entry in entries if not entry[0].startswith(P+'_renew_')]
 entries.extend(parse(alliance_decisions(api)))
 decisions=MARKER+render(decision_tree)+'\n'
 text=api.emit_localisation(nodes)
 # Private contract IDs are helper records, not new focuses. Existing focus
 # localisation stays with the parent's authoritative legacy provider.
 for n in nodes:text=re.sub(r'(?m)^ '+re.escape(n['id'])+r'(?:_desc)?:0 .*\n','',text)
 text=text.replace('$RIGHT|+=2$ billion/week','$RIGHT|+=3$ billion/week')
 extra={
  ALLY_USA_ID:'Allied Readiness Coordination',ALLY_USA_ID+'_desc':ROOTS['USA_1970_NIX_F3'][2]+' The coordination programme remains a single institution regardless of the number of partners.',
  ALLY_PARTNER_ID:'American Readiness Partnership',ALLY_PARTNER_ID+'_desc':'Common training and support arrangements improve readiness while increasing personnel commitments. The partnership remains active while both countries retain the required alliance status and unrestricted bilateral relations.',
  P+'_alliance_title':'Allied Readiness Programme',P+'_alliance_desc':ROOTS['USA_1970_NIX_F3'][2]+' Washington funds a separate weekly contribution for each ratified partnership. The proposal remains open for 90 days.',
  P+'_alliance_accept':'Ratify the Allied Readiness Programme',P+'_alliance_accept_desc':ROOTS['USA_1970_NIX_F3'][2],
  P+'_alliance_decline':'Decline the Allied Readiness Programme',P+'_alliance_decline_desc':'The government will pursue its own readiness priorities. Neither country receives the proposed programme.',
  P+'_alliance_reopen':'Reopen Allied Readiness Talks',P+'_alliance_reopen_desc':'The government can reconsider the same American proposal after the consultation interval.',
  P+'_alliance_end':'End the American Readiness Partnership',P+'_alliance_end_desc':'Terminate the bilateral readiness arrangement and its future financial commitments.',
  P+'_alliance_end_partner':'End Readiness Cooperation with [From.GetNameDef]',P+'_alliance_end_partner_desc':'Terminate the selected bilateral readiness arrangement. Other accepted partnerships continue.',
  P+'_allied_usa_doctrine':'Allied Readiness Coordination',P+'_allied_partner_doctrine':'American Readiness Partnership',
  P+'_israel_counterparts_tt':'Israel exists and bilateral relations permit a new security-assistance proposal.',
  P+'_trade_counterparts_tt':'At least one North American trading partner is available for bilateral consultations.',
  P+'_nixon_in_office_tt':'Richard Nixon is President.',
  P+'_each_partner_tt':'Each participating partner:',P+'_each_partner_cost_tt':'United States, per accepted partner:',
  P+'_alliance_weekly_tt':'Weekly allied programme expense: §R-$[?'+P+'_alliance_weekly_expense|3] billion/week§!',
 }
 text+=''.join(' '+k+':0 '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in extra.items())
 files={f'common/scripted_effects/{STEM}.txt':effects,f'common/scripted_triggers/{STEM}.txt':triggers,f'common/ideas/{STEM}.txt':ideas,f'events/{STEM}.txt':events,f'common/decisions/categories/{STEM}.txt':category,f'common/decisions/{STEM}.txt':decisions,f'localisation/english/{STEM}_l_english.yml':text}
 specs=make_specs(api,nodes)
 report=validate(files,specs,api,nodes,ns)
 for path,content in files.items():
  target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content,encoding='utf-8-sig' if path.endswith('.yml') else 'utf-8',newline='\n')
 OUT.mkdir(parents=True,exist_ok=True)
 (OUT/'focus_specs.json').write_text(json.dumps(specs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
 (OUT/'RESEARCH.md').write_text(research_record(),encoding='utf-8')
 print(json.dumps(report))
 return report


def validate(files,specs,api,nodes,ns):
 parsed={p:ns['parse'](s) for p,s in files.items() if p.endswith('.txt')}
 defined={k for tree in parsed.values() for k,_,_ in tree}
 for path,tree in parsed.items():
  for k,_,v in ns['walk'](tree):
   if k.startswith(P+'_') and v=='yes':assert k in defined,(path,k)
   if k=='set_country_flag' and isinstance(v,list):assert ns['first'](v,'value')=='1',(path,v)
   assert k not in {'has_building'},(path,k)
 for p,s in files.items():
  assert s.startswith('l_english:\n# IMPERIA COLD WAR') if p.endswith('.yml') else s.startswith('# IMPERIA COLD WAR')
  assert not s.startswith('\ufeff')
  if p.endswith('.yml'):
   pairs=re.findall(r'^ ([^ :]+):0 (.+)$',s,re.M);assert len(pairs)==len(dict(pairs))
   assert all('\u2013' not in json.loads(v) and '\u2014' not in json.loads(v) for k,v in pairs)
 assert len(specs['focuses'])==3 and all(s['replace_legacy_completion'] for s in specs['focuses'].values())
 effects=dict((k,v) for k,_,v in parsed[f'common/scripted_effects/{STEM}.txt'])
 for name in (P+'_alliance_preview',P+'_alliance_recipient_preview'):
  assert [k for k,_,v in effects[name]]==['effect_tooltip']
 reconcile=effects[P+'_reconcile_all'];assert not any(k=='every_country' for k,_,v in ns['walk'](reconcile))
 ledger=effects[P+'_calculate_weekly_streams'];assert not any(k in {'every_country','modify_treasury_effect','set_country_flag','country_event','add_ideas'} for k,_,v in ns['walk'](ledger))
 return dict(project='IMPERIA COLD WAR',status='Source checks passed; native and multiplayer tests pending',legacy_roots=3,fixed_contracts=3,dynamic_partner_pool='Actual NATO or MNNA members without tag whitelist',weekly_per_allied_partner=str(ALLY_COST),shared_usa_idea_copies=1,checks=['Strict script parsing','Custom effect/trigger closure','Explicit timed flag values','No unsupported has_building','Unconditional nonexecuting prospective previews','No recurring world scan','Pure fixed weekly stream calculator','English localisation and project markers'])


def research_record():
 return '''IMPERIA COLD WAR

# Early US cooperation: historical and mechanical basis

The user requested this reward revision after reviewing the implemented legacy focus tooltips. It changes the three existing roots, rather than editing the immutable 24 October 2026 proposal. No historical budget is claimed to equal the authored game-balance amounts.

- Nixon's 17 March 1970 aide-memoire ties Israeli military security, maintenance of the regional balance and negotiated diplomacy: https://history.state.gov/historicaldocuments/frus1969-76v23/d103 . The 19 August 1970 review calls for a costed defensive package and consultation, explicitly short of joint planning: https://history.state.gov/historicaldocuments/frus1969-76v23/d153 . This supports a funded security-assistance institution with training/supply benefits, not automatic war entry or territorial concessions.
- NATO's 3 December 1970 Alliance Defence for the Seventies statement calls for shared burdens, sustained North American forces, stronger European readiness and funded communications/protection measures: https://www.nato.int/cps/en/natohq/official_texts_26792.htm?selectedLocale=en . The programme adapts that cooperation to recipient-approved RP. It does not grant NATO/MNNA status or claim the modern legal MNNA designation already existed in 1970. Eligibility reads the existing MD national spirits NATO_member and Major_Non_NATO_Ally.
- Canada-US Automotive Products Agreement, signed in 1965: https://www.treaty-accord.gc.ca/details.aspx?id=100604 . Mexico's Ministry of Economy dates border industrialisation policy to 20 May 1965: https://www.economia-snci.gob.mx/sic_php/pages/importa/abc_maquiladora.php . These are different bilateral industrial relationships, not an invented 1970 NAFTA. Canadian and Mexican recipients decide independently.

Mechanical references were inspected in the installed original MD USA tree. USA_focus_gold_star_program (cost8.6) combines daily army experience+0.03, leader XP+8%, attack+3%, defence+2%, personnel cost+4% and education cost+7%. The original UK state visit grants PP gain+5%, influence measures and export return+5%, but lacks the requested paired standing-consent lifecycle. The new static USA alliance spirit gives organisation+2%, army experience gain+5%, personnel cost+2%, with an additional0.005billion/week for each actually active accepted partner. The USA doctrine coupon is granted once, not once per member. Partner readiness gives organisation+3%, supply consumption-3%, personnel cost+2% and one50%land-doctrine coupon. These are balance choices, not transplanted historical statistics.

F7 costs0.01billion/week while the accepted Israeli parent programme is active. E9 costs0.005billion/week per accepted Canadian or Mexican parent partnership. Root setup fees and assets are zero. Existing USA_X_israel, USA_X_canada and USA_X_mexico remain distinct industrial/research follow-ups with their own acceptance and published costs; they require the actual active early parent pair. No root pays their fees or grants their assets in advance.

Native hooks use one focus-time world dispatch and stored offered/accepted country arrays. Daily reconciliation and fiscal calculation do not scan the world. The parent must call the membership_changed hook after native NATO/MNNA admission, allowing later Spain or alternate RP members to receive a real offer. The exact native providers are common/ideas/Factions.txt:NATO_member and common/ideas/united_states.txt:Major_Non_NATO_Ally; the admission effects are common/scripted_effects/01_NATO_effects.txt.

Existing native GFX_political_deal is reused without editing image/frame/alpha pixels. Its217x163RGBA donor and adjacent native event options were inspected in the preceding agreement work. Original image author and individual licence are unknown. Existing trade, defence and NATO idea textures are referenced; project integration does not establish ownership. No new binary game asset is emitted.
'''


if __name__=='__main__':
 build()
