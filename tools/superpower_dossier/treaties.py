# IMPERIA COLD WAR — Versioned configurable superpower treaties, native concessions and membership
"""Generate bounded treaty records. UI review is separate from authoritative execution."""
from pathlib import Path
import re

TREATIES = (
 ('salt1','SALT I','Strategic restraint','Negotiate a freeze or reduction of nuclear-capable missile reserves, with separately agreed commercial provisions.',1),
 ('abm','ABM Treaty','Defence talks','Establish a standing strategic-defence consultation accord. Any additional material obligations are specified in its protocols.',1),
 ('salt2','SALT II','Strategic restraint','Negotiate strategic restraint and an agreed reduction of the selected missile stockpiles.',1),
 ('inf','INF Treaty','Missile elimination','Negotiate the elimination or reduction of explicitly selected stored missile types. Deployed systems and unlisted types remain separate obligations.',1),
 ('start','START I','Strategic reductions','Reduce the selected nuclear-capable missile reserves and agree a continuing ceiling on the remaining stocks.',1),
 ('reykjavik','Reykjavik Framework','Deep reductions','Negotiate deep missile-reserve reductions and continuing ceilings, alongside explicit reciprocal concessions.',1),
 ('risk','Nuclear Risk Reduction','Consultation','Create a standing consultation channel and specify any reciprocal restraint and economic measures.',1),
 ('trade','Commercial Accord','Trade normalization','Promote trade among the consenting signatories and negotiate explicitly named sanctions relief.',2),
 ('investment','Investment Cooperation','Mutual investment','Reduce the cost and construction time of investments between consenting signatories.',2),
 ('regional','Regional Stand-down','Support withdrawal','Withdraw the named own military missions and deployments. Supported governments retain control of their own war.',3),
 ('sanctions','Sanctions and Restraint','Reciprocal concessions','Exchange named sanctions relief for specified military and economic concessions.',3),
 ('custom','Custom Agreement','Own negotiating paper','Choose the missile, commercial, financial and regional commitments to propose. Both governments review the complete paper before either signs.',3),
)
# Actual loaded native equipment models. These are reserves, not deployed delivery systems.
ICBM = tuple(f'nuclear_missile_equipment_{i}' for i in range(1,7))
MRBM = tuple(f'{p}_{i}' for p in ('ballistic_missile_equipment','nuclear_ballistic_missile_equipment') for i in range(1,4))
CRUISE = tuple(f'guided_missile_equipment_{i}' for i in range(1,4))
LEGACY_EQUIPMENT = ICBM + MRBM + CRUISE
# Preserve every original plan index for pending/saved instruments; append verified models.
EQUIPMENT = LEGACY_EQUIPMENT + tuple(e for e in tuple(f'ballistic_missile_equipment_{i}' for i in range(4,7))+tuple(f'nuclear_ballistic_missile_equipment_{i}' for i in range(4,6))+tuple(f'guided_missile_equipment_{i}' for i in range(4,7)) if e not in LEGACY_EQUIPMENT)
FIELDS = ('scope','reduction','restraint','sanctions','trade','investment','duration','regional','usa_target','sov_target','programme','reserve_limit','missile_version')
OPTIONS = {'scope':(0,1,2,3,4,5,6),'reduction':(0,10,25,50,100),'restraint':(0,10,25,50),
           'sanctions':(0,1,2,3,4,5),'trade':(0,1,2),'investment':(0,1,2),
           'duration':(0,180,365,730,1825,5475),'regional':(0,1,2,3),'programme':(0,1,2,3,4),
           'reserve_limit':(0,1),'missile_version':(0,1)}
SANCTIONS = (('dip',1),('fin',2),('eco',3),('mil',4))


def defaults(n):
    return dict(scope=1 if n in (1,3,5,6) else 6 if n==4 else 0,
                reduction=25 if n==5 else 50 if n==6 else 100 if n==4 else 0,
                restraint=0,sanctions=5 if n==11 else 0,
                trade=2 if n==8 else 0,investment=1 if n==9 else 0,
                duration=1825 if n in (1,3) else 5475 if n==5 else 0,regional=3 if n==10 else 0,usa_target=0,sov_target=0,programme=0,
                reserve_limit=1 if n in (1,3,4,5,6) else 0,missile_version=1)


def build(write,loc,defined,mark,root,here):
    tr=[mark];ef=[mark];sl=[mark];events=[mark,'add_namespace = icwt']
    def trigger(name,body):tr.append(f'{name} = {{\n{body}\n}}')
    def effect(name,body):ef.append(f'{name} = {{\n{body}\n}}')
    def text(name,rows,fallback='icsd_empty'):sl.append(defined(name,rows,fallback))
    trigger('icwt_core','IMP_is_1970_scenario = yes OR = { tag = USA tag = SOV }')
    trigger('icwt_actor','IMP_is_1970_scenario = yes exists = yes')
    trigger('icwt_pending','check_variable = { global.icwt_pending > 0 }')
    trigger('icwt_edit_valid','\n'.join('OR = { '+' '.join(f'check_variable = {{ icwt_edit_{f} = {v} }}' for v in values)+' }' for f,values in OPTIONS.items())+'''
OR = { check_variable = { icwt_edit_scope > 0 } check_variable = { icwt_edit_reduction = 0 } }
OR = { check_variable = { icwt_edit_regional = 0 }
 AND = { check_variable = { icwt_edit_usa_target > 0 } check_variable = { icwt_edit_sov_target > 0 }
  var:icwt_edit_usa_target = { exists = yes NOT = { tag = USA } }
  var:icwt_edit_sov_target = { exists = yes NOT = { tag = SOV } }
 }
}
''')
    effect('icwt_touch','icsd_touch = yes')
    effect('icwt_touch_core','if = { limit = { country_exists = USA } USA = { icwt_display = yes } } if = { limit = { country_exists = SOV } SOV = { icwt_display = yes } }')
    effect('icwt_clear_reviews','''
if = { limit = { country_exists = USA } USA = { clear_variable = icwt_review_revision clear_variable = icwt_review_template } }
if = { limit = { country_exists = SOV } SOV = { clear_variable = icwt_review_revision clear_variable = icwt_review_template } }
''')
    # Only this synchronous pair helper uses PREV: caller country, THIS other country.
    effect('icwt_pair_recalculate','''
set_temp_variable = { icwt_pair_trade = 0 } set_temp_variable = { icwt_pair_invest = 0 } set_temp_variable = { icwt_pair_peace = 0 }
'''+ '\n'.join(f'''if = {{ limit = {{ has_country_flag = icwt_member_{n} PREV = {{ has_country_flag = icwt_member_{n} }} NOT = {{ has_war_with = PREV }} }}
 if = {{ limit = {{ check_variable = {{ global.icwt_{n}_trade > icwt_pair_trade }} }} set_temp_variable = {{ icwt_pair_trade = global.icwt_{n}_trade }} }}
 if = {{ limit = {{ check_variable = {{ global.icwt_{n}_investment > icwt_pair_invest }} }} set_temp_variable = {{ icwt_pair_invest = global.icwt_{n}_investment }} }}
 if = {{ limit = {{ check_variable = {{ global.icwt_{n}_sanctions > 0 }} }} set_temp_variable = {{ icwt_pair_peace = 1 }} }}
}}''' for n in range(1,len(TREATIES)+1))+'''
if = { limit = { NOT = { check_variable = { icwt_trade_applied@PREV = icwt_pair_trade } } }
 remove_opinion_modifier = { target = PREV modifier = icwt_trade_1 } remove_opinion_modifier = { target = PREV modifier = icwt_trade_2 }
 remove_opinion_modifier = { target = PREV modifier = icwt_relations_1 } remove_opinion_modifier = { target = PREV modifier = icwt_relations_2 }
 if = { limit = { check_variable = { icwt_pair_trade = 1 } } add_opinion_modifier = { target = PREV modifier = icwt_trade_1 } add_opinion_modifier = { target = PREV modifier = icwt_relations_1 } }
 if = { limit = { check_variable = { icwt_pair_trade = 2 } } add_opinion_modifier = { target = PREV modifier = icwt_trade_2 } add_opinion_modifier = { target = PREV modifier = icwt_relations_2 } }
 set_variable = { icwt_trade_applied@PREV = icwt_pair_trade }
}
set_variable = { icwt_investment@PREV = icwt_pair_invest }
set_variable = { icwt_moratorium@PREV = icwt_pair_peace }
''')
    effect('icwt_refresh_country','''
set_temp_variable = { icwt_restraint = 0 }
'''+ '\n'.join(f'if = {{ limit = {{ has_country_flag = icwt_member_{n} check_variable = {{ global.icwt_{n}_restraint > icwt_restraint }} }} set_temp_variable = {{ icwt_restraint = global.icwt_{n}_restraint }} }}' for n in range(1,len(TREATIES)+1))+'''
if = { limit = { NOT = { check_variable = { icwt_restraint = 10 } } has_idea = icwt_restraint_10 } remove_ideas = icwt_restraint_10 }
if = { limit = { NOT = { check_variable = { icwt_restraint = 25 } } has_idea = icwt_restraint_25 } remove_ideas = icwt_restraint_25 }
if = { limit = { NOT = { check_variable = { icwt_restraint = 50 } } has_idea = icwt_restraint_50 } remove_ideas = icwt_restraint_50 }
if = { limit = { check_variable = { icwt_restraint = 10 } NOT = { has_idea = icwt_restraint_10 } } add_ideas = icwt_restraint_10 }
if = { limit = { check_variable = { icwt_restraint = 25 } NOT = { has_idea = icwt_restraint_25 } } add_ideas = icwt_restraint_25 }
if = { limit = { check_variable = { icwt_restraint = 50 } NOT = { has_idea = icwt_restraint_50 } } add_ideas = icwt_restraint_50 }
for_each_scope_loop = { array = global.icwt_roster limit = { exists = yes NOT = { tag = PREV } } icwt_pair_recalculate = yes }
icsd_touch = yes
''')
    # A bounded ever-participant roster, not a per-frame or world scan. Max 8 per 11 records.
    effect('icwt_refresh','''
for_each_scope_loop = { array = global.icwt_roster limit = { exists = yes } icwt_refresh_country = yes }
set_temp_variable = { icwt_relief = 0 }
'''+ '\n'.join(f'''if = {{ limit = {{ country_exists = USA country_exists = SOV USA = {{ has_country_flag = icwt_member_{n} NOT = {{ has_war_with = SOV }} }} SOV = {{ has_country_flag = icwt_member_{n} }} }} add_to_temp_variable = {{ icwt_relief = 1 }} }}''' for n in range(1,len(TREATIES)+1))+'''
clamp_temp_variable = { var = icwt_relief min = 0 max = 5 }
set_temp_variable = { mdcw_cw_tension_delta = global.icwt_relief }
subtract_from_temp_variable = { mdcw_cw_tension_delta = icwt_relief }
if = { limit = { NOT = { check_variable = { mdcw_cw_tension_delta = 0 } } has_global_flag = mdcw_cw_initialized } mdcw_cw_add_tension = yes }
set_variable = { global.icwt_relief = icwt_relief }
icwt_touch_core = yes
''')
    # Budgeted sanction relief calls the exact native lift body. Preserve ROOT = sanctioning country.
    native=(root/'common/scripted_diplomatic_actions/imp_sanctions_diplomatic_actions.txt').read_text(encoding='utf-8-sig')
    def body_at(source,name,field):
        start=re.search(r'\b'+re.escape(name)+r'\s*=\s*\{',source).end();depth=1;end=start
        while depth:depth+=(source[end]=='{')-(source[end]=='}');end+=1
        s=source[start:end-1];start=re.search(r'\b'+field+r'\s*=\s*\{',s).end();depth=1;end=start
        while depth:depth+=(s[end]=='{')-(s[end]=='}');end+=1
        return s[start:end-1]
    for typ,num in SANCTIONS:
        name={'dip':'diplo','fin':'fin','eco':'eco','mil':'mil'}[typ]
        effect(f'icwt_lift_{typ}_native',body_at(native,f'imp_{name}_sanctions_lift','complete_effect'))
    # Scope of this helper is the signer, target entered using an explicit country variable.
    for n in range(1,len(TREATIES)+1):
        choices=[];apply=[]
        for typ,num in SANCTIONS:
            cond=f'OR = {{ check_variable = {{ global.icwt_{n}_sanctions = {num} }} check_variable = {{ global.icwt_{n}_sanctions = 5 }} }} is_in_array = {{ array = imp_{typ}_sanc_by_us value = var:icwt_other }}'
            choices.append(f'if = {{ limit = {{ {cond} }} add_to_temp_variable = {{ icwt_fee = 35 }} }}')
            # Native ROOT must be the actual sanction owner, not the GUI's original root.
            # A scripted effect call does not change ROOT: use direct mirror operations and the current CW hook in explicit scope instead.
            apply.append(f'''if = {{ limit = {{ {cond} }}
 add_political_power = -35
 remove_from_array = {{ array = imp_{typ}_sanc_by_us value = var:icwt_other }}
 var:icwt_other = {{ remove_from_array = {{ array = imp_{typ}_sanc_on_us value = PREV }} remove_opinion_modifier = {{ target = PREV modifier = opinion_{typ}_sanctioned_us }} }}
}}''')
        effect(f'icwt_fee_{n}','set_temp_variable = { icwt_fee = 0 }\n'+'\n'.join(choices))
        effect(f'icwt_relief_{n}','\n'.join(apply))
    trigger('icwt_can_impose_sanctions','NOT = { check_variable = { ROOT.icwt_moratorium@THIS > 0 } }')
    for f,values in OPTIONS.items():
        entries=[]
        for i,v in enumerate(values):
            nxt=values[(i+1)%len(values)]
            entries.append(f'else_if = {{ limit = {{ check_variable = {{ icwt_edit_{f} = {v} }} }} set_variable = {{ icwt_edit_{f} = {nxt} }} }}')
        amendment_guard=' NOT = { check_variable = { icwt_edit_addendum = 1 } }' if f!='programme' else ''
        effect(f'icwt_cycle_{f}','if = { limit = { icwt_core = yes NOT = { icwt_pending = yes }'+amendment_guard+' }\n'+''.join(entries).replace('else_if','if',1)+'\nclear_variable = icwt_review_revision icwt_touch = yes }')
    for n,(slug,title,caption,desc,cat) in enumerate(TREATIES,1):
        loc(f'icwt_title_{n}',title);loc(f'icwt_caption_{n}',caption);loc(f'icwt_desc_{n}',desc)
        loc(f'icwt_spirit_{n}',title+' Treaty' if 'Treaty' not in title else title)
        loc(f'icwt_spirit_{n}_desc','Our government is a signatory to this agreement. Its selected protocols define our continuing obligations and relations with fellow signatories. Participation may be ended through the treaty register.')
        effect(f'icwt_select_{n}',f'set_variable = {{ icwt_template = {n} }} set_variable = {{ icwt_screen = 0 }} clear_variable = icwt_review_revision icwt_touch = yes')
        preset=defaults(n)
        effect(f'icwt_edit_{n}',f'''if = {{ limit = {{ icwt_core = yes NOT = {{ icwt_pending = yes }} check_variable = {{ global.icwt_{n}_members^num < 1 }} }}
set_variable = {{ icwt_template = {n} }} set_variable = {{ icwt_screen = 1 }} clear_variable = icwt_review_revision clear_array = icwt_edit_invites
'''+ '\n'.join(f'set_variable = {{ icwt_edit_{f} = {v} }}' for f,v in preset.items())+'\nicwt_touch = yes }')
        # Stock plan is frozen at review/send. Concrete exact model counts are visible in native tooltips.
        plan=[];valid=[];scrap=[];preview=[]
        for i,equip in enumerate(EQUIPMENT):
            group=1 if equip in ICBM else 2 if equip in MRBM else 3
            plan.append(f'''set_variable = {{ icwt_plan_{n}_{i} = 0 }}
if = {{ limit = {{ OR = {{ check_variable = {{ icwt_calc_scope = {group} }} check_variable = {{ icwt_calc_scope = 4 }} }} }}
 set_variable = {{ icwt_plan_{n}_{i} = num_equipment@{equip} }} multiply_variable = {{ icwt_plan_{n}_{i} = icwt_calc_fraction }} round_variable = icwt_plan_{n}_{i}
}}''')
            valid.append(f'check_variable = {{ var = num_equipment@{equip} value = icwt_plan_{n}_{i} compare = greater_than_or_equals }}')
            scrap.append(f'''if = {{ limit = {{ check_variable = {{ icwt_plan_{n}_{i} > 0 }} }}
 set_temp_variable = {{ icwt_remove = icwt_plan_{n}_{i} }} multiply_temp_variable = {{ icwt_remove = -1 }}
 add_equipment_to_stockpile = {{ type = {equip} amount = icwt_remove }}
}}''')
            preview.append(f'''if = {{ limit = {{ check_variable = {{ icwt_plan_{n}_{i} > 0 }} }} set_temp_variable = {{ icwt_remove = icwt_plan_{n}_{i} }} multiply_temp_variable = {{ icwt_remove = -1 }} add_equipment_to_stockpile = {{ type = {equip} amount = icwt_remove }} }}''')
        effect(f'icwt_plan_{n}','\n'.join(plan))
        trigger(f'icwt_assets_{n}','\n'.join(valid))
        effect(f'icwt_scrap_{n}','\n'.join(scrap))
        effect(f'icwt_preview_assets_{n}','effect_tooltip = {\n'+'\n'.join(preview)+'\n}')
        trigger(f'icwt_member_{n}',f'has_country_flag = icwt_member_{n}')
        trigger(f'icwt_invitation_{n}',f'''icwt_actor = yes NOT = {{ has_country_flag = icwt_member_{n} }} check_variable = {{ icwt_invite_{n} > 0 }}
OR = {{ AND = {{ check_variable = {{ global.icwt_pending = {n} }} check_variable = {{ icwt_invite_{n} = global.icwt_p_revision }} }} AND = {{ check_variable = {{ global.icwt_{n}_members^num > 0 }} check_variable = {{ icwt_invite_{n} = global.icwt_{n}_revision }} }} }}''')
        trigger(f'icwt_reviewed_{n}',f'check_variable = {{ icwt_review_template = {n} }} check_variable = {{ icwt_review_revision > 0 }} OR = {{ icwt_core = yes icwt_assets_{n} = yes }}')
        effect(f'icwt_send_{n}',f'''if = {{ limit = {{ icwt_core = yes icwt_edit_valid = yes NOT = {{ icwt_pending = yes }} check_variable = {{ global.icwt_{n}_members^num < 1 }} }}
add_to_variable = {{ global.icwt_sequence = 1 }} set_variable = {{ global.icwt_pending = {n} }} set_variable = {{ global.icwt_p_revision = global.icwt_sequence }} set_variable = {{ global.icwt_p_author = THIS.id }}
'''+ '\n'.join(f'set_variable = {{ global.icwt_p_{f} = icwt_edit_{f} }}' for f in FIELDS)+'''
clear_array = global.icwt_p_invites
for_each_scope_loop = { array = icwt_edit_invites limit = { exists = yes }
 add_to_array = { global.icwt_p_invites = THIS.id }
'''+f''' set_variable = {{ icwt_invite_{n} = global.icwt_p_revision }} clear_variable = icwt_accept_{n}
 country_event = {{ id = icwt.{100+n} }}
}}
icwt_clear_reviews = yes
USA = {{ set_variable = {{ icwt_calc_scope = global.icwt_p_scope }} set_variable = {{ icwt_calc_fraction = global.icwt_p_reduction }} divide_variable = {{ icwt_calc_fraction = 100 }} icwt_plan_{n} = yes }}
SOV = {{ set_variable = {{ icwt_calc_scope = global.icwt_p_scope }} set_variable = {{ icwt_calc_fraction = global.icwt_p_reduction }} divide_variable = {{ icwt_calc_fraction = 100 }} icwt_plan_{n} = yes }}
if = {{ limit = {{ tag = USA }} SOV = {{ country_event = {{ id = icwt.{n} }} }} }} else = {{ USA = {{ country_event = {{ id = icwt.{n} }} }} }}
set_variable = {{ icwt_screen = 3 }} icwt_touch_core = yes
}}''')
        effect(f'icwt_review_{n}',f'''if = {{ limit = {{ OR = {{ AND = {{ icwt_core = yes check_variable = {{ global.icwt_pending = {n} }} }} icwt_invitation_{n} = yes }} }}
set_variable = {{ icwt_template = {n} }} set_variable = {{ icwt_screen = 3 }}
if = {{ limit = {{ check_variable = {{ global.icwt_pending = {n} }} }}
 set_variable = {{ icwt_review_revision = global.icwt_p_revision }}
 set_variable = {{ icwt_calc_scope = global.icwt_p_scope }} set_variable = {{ icwt_calc_fraction = global.icwt_p_reduction }}
}} else = {{ set_variable = {{ icwt_review_revision = global.icwt_{n}_revision }} set_variable = {{ icwt_calc_scope = global.icwt_{n}_scope }} set_variable = {{ icwt_calc_fraction = global.icwt_{n}_reduction }} }}
divide_variable = {{ icwt_calc_fraction = 100 }}
if = {{ limit = {{ NOT = {{ icwt_core = yes }} }} icwt_plan_{n} = yes }}
set_variable = {{ icwt_review_template = {n} }}
if = {{ limit = {{ icwt_core = yes }} set_variable = {{ icsd_tab = 2 }} set_country_flag = icsd_open }}
icwt_touch = yes
}}''')
        # A new member's one-time asset transaction is keyed to this exact concluded revision.
        effect(f'icwt_join_{n}',f'''if = {{ limit = {{ NOT = {{ has_country_flag = icwt_member_{n} }} icwt_assets_{n} = yes NOT = {{ check_variable = {{ icwt_receipt_{n} = global.icwt_{n}_revision }} }} }}
set_variable = {{ icwt_receipt_{n} = global.icwt_{n}_revision }} set_country_flag = icwt_member_{n} add_to_array = {{ global.icwt_{n}_members = THIS.id }}
if = {{ limit = {{ NOT = {{ is_in_array = {{ array = global.icwt_roster value = THIS }} }} }} add_to_array = {{ global.icwt_roster = THIS.id }} }}
add_ideas = icwt_spirit_{n} icwt_scrap_{n} = yes
if = {{ limit = {{ tag = USA }} set_variable = {{ icwt_withdraw_target = global.icwt_{n}_usa_target }} }}
else_if = {{ limit = {{ tag = SOV }} set_variable = {{ icwt_withdraw_target = global.icwt_{n}_sov_target }} }} else = {{ clear_variable = icwt_withdraw_target }}
if = {{ limit = {{ check_variable = {{ icwt_withdraw_target > 0 }} var:icwt_withdraw_target = {{ exists = yes }} }}
 if = {{ limit = {{ OR = {{ check_variable = {{ global.icwt_{n}_regional = 1 }} check_variable = {{ global.icwt_{n}_regional = 3 }} }} }} recall_attache = var:icwt_withdraw_target }}
 if = {{ limit = {{ OR = {{ check_variable = {{ global.icwt_{n}_regional = 2 }} check_variable = {{ global.icwt_{n}_regional = 3 }} }} has_game_rule = {{ rule = allow_recall_intervention_forces option = yes }} has_political_power > 49 command_power > 14 var:icwt_withdraw_target = {{ has_volunteers_amount_from = {{ tag = PREV count > 0 }} }} }}
  add_political_power = -50 add_command_power = -15 recall_volunteers_from = var:icwt_withdraw_target
 }}
}}
clear_variable = icwt_accept_{n} clear_variable = icwt_invite_{n} icwt_touch = yes
}}''')
        effect(f'icwt_sign_{n}',f'''if = {{ limit = {{ icwt_core = yes check_variable = {{ global.icwt_pending = {n} }} icwt_reviewed_{n} = yes check_variable = {{ icwt_review_revision = global.icwt_p_revision }} NOT = {{ check_variable = {{ global.icwt_p_author = THIS.id }} }}
country_exists = USA country_exists = SOV USA = {{ NOT = {{ has_war_with = SOV }} }} check_variable = {{ global.icwt_{n}_members^num < 1 }} }}
set_variable = {{ global.icwt_{n}_revision = global.icwt_p_revision }}
'''+ '\n'.join(f'set_variable = {{ global.icwt_{n}_{f} = global.icwt_p_{f} }}' for f in FIELDS)+f'''
set_variable = {{ global.icwt_{n}_end = 0 }}
if = {{ limit = {{ check_variable = {{ global.icwt_{n}_duration > 0 }} }} set_variable = {{ global.icwt_{n}_end = global.num_days }} add_to_variable = {{ global.icwt_{n}_end = global.icwt_{n}_duration }} }}
USA = {{ icwt_join_{n} = yes }} SOV = {{ icwt_join_{n} = yes }}
for_each_scope_loop = {{ array = global.icwt_p_invites limit = {{ exists = yes check_variable = {{ icwt_accept_{n} = global.icwt_{n}_revision }} icwt_assets_{n} = yes }} icwt_join_{n} = yes }}
clear_variable = global.icwt_pending icwt_clear_reviews = yes
set_variable = {{ global.icwt_news_template = {n} }} set_variable = {{ global.icwt_news_actor = THIS.id }} news_event = {{ id = icwt.200 }}
icwt_refresh = yes set_variable = {{ icsd_tab = 3 }} set_variable = {{ icwt_register = 1 }} set_variable = {{ icwt_template = {n} }} icwt_touch_core = yes
}}''')
        effect(f'icwt_accept_invite_{n}',f'''if = {{ limit = {{ icwt_invitation_{n} = yes icwt_reviewed_{n} = yes check_variable = {{ icwt_review_revision = icwt_invite_{n} }} }}
if = {{ limit = {{ check_variable = {{ global.icwt_pending = {n} }} }} set_variable = {{ icwt_accept_{n} = icwt_review_revision }} }}
else = {{ icwt_join_{n} = yes set_variable = {{ global.icwt_news_template = {n} }} set_variable = {{ global.icwt_news_actor = THIS.id }} news_event = {{ id = icwt.201 }} icwt_refresh = yes }}
}}''')
        effect(f'icwt_leave_{n}',f'''if = {{ limit = {{ has_country_flag = icwt_member_{n} }}
clr_country_flag = icwt_member_{n} remove_ideas = icwt_spirit_{n} remove_from_array = {{ array = global.icwt_{n}_members value = THIS }}
set_variable = {{ global.icwt_news_template = {n} }} set_variable = {{ global.icwt_news_actor = THIS.id }} news_event = {{ id = icwt.202 }}
icwt_refresh = yes
}}''')
        # Native events only notify/review. A stale event cannot sign an updated instrument.
        for eid,invited in ((n,False),(100+n,True)):
            guard=f'icwt_invitation_{n} = yes' if invited else f'icwt_core = yes check_variable = {{ global.icwt_pending = {n} }}'
            events.append(f'''country_event = {{ id = icwt.{eid} title = icwt_title_{n} desc = icwt_invitation_desc picture = GFX_icwt_country is_triggered_only = yes trigger = {{ {guard} }}
option = {{ name = icwt_review_option icwt_review_{n} = yes ai_chance = {{ factor = 0 }} }}
option = {{ name = icwt_later ai_chance = {{ factor = 100 }} }}
}}''')
    effect('icwt_cancel_pending','if = { limit = { icwt_core = yes icwt_pending = yes } clear_variable = global.icwt_pending icwt_clear_reviews = yes icwt_touch_core = yes }')
    effect('icwt_weekly','\n'.join(f'''if = {{ limit = {{ check_variable = {{ global.icwt_{n}_end > 0 }} check_variable = {{ global.icwt_{n}_members^num > 0 }} check_variable = {{ var = global.num_days value = global.icwt_{n}_end compare = greater_than_or_equals }} }}
for_each_scope_loop = {{ array = global.icwt_{n}_members limit = {{ exists = yes }} clr_country_flag = icwt_member_{n} remove_ideas = icwt_spirit_{n} }} clear_array = global.icwt_{n}_members
}}''' for n in range(1,len(TREATIES)+1))+'\nicwt_refresh = yes')
    for id_,titlekey,desckey in ((200,'icwt_news_signed','icwt_news_signed_desc'),(201,'icwt_news_joined','icwt_news_joined_desc'),(202,'icwt_news_left','icwt_news_left_desc')):
        events.append(f'news_event = {{ id = icwt.{id_} title = {titlekey} desc = {desckey} picture = GFX_icwt_news is_triggered_only = yes major = yes option = {{ name = icwt_news_ack }} }}')
    text('icwt_selected_title',[(f'check_variable = {{ icwt_template = {n} }}',f'icwt_title_{n}') for n in range(1,len(TREATIES)+1)])
    text('icwt_selected_desc',[(f'check_variable = {{ icwt_template = {n} }}',f'icwt_desc_{n}') for n in range(1,len(TREATIES)+1)])
    text('icwt_news_title',[(f'check_variable = {{ global.icwt_news_template = {n} }}',f'icwt_title_{n}') for n in range(1,len(TREATIES)+1)])
    loc('icwt_invitation_desc','A negotiating paper has been delivered to our government. Review its current terms before deciding whether to join.')
    for key,value in {'review_option':'Review the negotiating paper','later':'Consider the paper later','news_signed':'[icwt_news_title]: agreement signed',
        'news_joined':'[?global.icwt_news_actor.GetName] joins [icwt_news_title]','news_left':'[?global.icwt_news_actor.GetName] leaves [icwt_news_title]',
        'news_signed_desc':'Washington and Moscow have concluded a new agreement. The signatories have accepted its stated protocols and retain responsibility for their own commitments.',
        'news_joined_desc':'[?global.icwt_news_actor.GetName] has joined the agreement following its own approval. Its participation takes effect under the accepted protocols.',
        'news_left_desc':'[?global.icwt_news_actor.GetName] has announced its withdrawal. Its continuing treaty effects and obligations have ended. Other signatories retain authority over their own participation.',
        'news_ack':'The world takes note.'}.items():loc('icwt_'+key,value)
    from transactions import extend
    extend(ef,tr,events,loc,defined,root,mark)
    from programmes import extend as programme_clauses
    programme_ideas = programme_clauses(ef,tr,events,loc,mark)
    from missile_protocols import extend as missile_protocols
    missile_decisions = missile_protocols(ef,tr,events,loc,mark,root)
    write('common/scripted_triggers/ICW_superpower_treaties.txt','\n'.join(tr)+'\n')
    write('common/scripted_effects/ICW_superpower_treaties.txt','\n'.join(ef)+'\n')
    write('common/scripted_localisation/ICW_superpower_treaties.txt','\n'.join(sl)+'\n')
    write('events/ICW_superpower_treaties.txt','\n'.join(events)+'\n')
    ideas=[mark,'ideas = { country = {']
    for n in range(1,len(TREATIES)+1):ideas.append(f'icwt_spirit_{n} = {{ picture = international_treaty2 allowed = {{ always = no }} allowed_civil_war = {{ always = no }} removal_cost = -1 modifier = {{ }} }}')
    ideas.extend(programme_ideas)
    for value in (10,25,50):
        ideas.append(f'icwt_restraint_{value} = {{ picture = international_treaty2 allowed = {{ always = no }} allowed_civil_war = {{ always = no }} removal_cost = -1 modifier = {{ }} }}')
        loc(f'icwt_restraint_{value}','Superseded Strategic Clause');loc(f'icwt_restraint_{value}_desc','Missile obligations are determined by the reserve and reduction terms reviewed by the signatories.')
    write('common/ideas/ICW_superpower_treaties.txt','\n'.join(ideas)+'\n} }\n')
    write('common/synchronized_dynamic_tokens/ICW_superpower_treaties.txt',mark+'\n'.join(EQUIPMENT)+'\n')
    write('common/opinion_modifiers/ICW_superpower_treaties.txt',mark+'opinion_modifiers = {\nicwt_trade_1 = { trade = yes value = 50 }\nicwt_trade_2 = { trade = yes value = 100 }\nicwt_relations_1 = { value = 10 }\nicwt_relations_2 = { value = 25 }\n}\n')
    for key,value in {'icwt_trade_1':'Commercial cooperation','icwt_trade_2':'Commercial normalization','icwt_relations_1':'Commercial understanding','icwt_relations_2':'Commercial accord'}.items():loc(key,value)
    decisions=[mark,'icsd_category = {']
    decisions.extend(missile_decisions)
    for n in range(1,len(TREATIES)+1):
        for action,test,eff in [('review',f'icwt_invitation_{n} = yes',f'icwt_review_{n} = yes'),('join',f'icwt_invitation_{n} = yes icwt_reviewed_{n} = yes',f'icwt_accept_invite_{n} = yes'),('leave',f'has_country_flag = icwt_member_{n}',f'icwt_leave_{n} = yes')]:
            key=f'icwt_{action}_decision_{n}';loc(key,{'review':'Review ','join':'Join ','leave':'Withdraw from '}[action]+TREATIES[n-1][1]);loc(key+'_desc',TREATIES[n-1][3])
            decisions.append(f'{key} = {{ icon = icsd_file visible = {{ {test} }} available = {{ {test} }} cost = 0 complete_effect = {{ {f'icwt_preview_join_{n} = yes' if action in ('review','join') else ''} hidden_effect = {{ {eff} }} }} ai_will_do = {{ factor = 0 }} }}')
    write('common/decisions/ICW_superpower_treaties.txt','\n'.join(decisions)+'\n}\n')
    return TREATIES
