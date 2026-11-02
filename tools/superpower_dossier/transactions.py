# IMPERIA COLD WAR — Treaty preflight, exact receipts and reversible ongoing effects
"""Authoritative transaction and provider integrations for configurable treaties."""
from treaties import FIELDS, TREATIES, SANCTIONS, EQUIPMENT, ICBM, MRBM, OPTIONS
import re


def extend(ef,tr,events,loc,defined,root,mark):
    def replace(rows,name,body):
        assert body.count('{')==body.count('}'), (name, 'unbalanced generated transaction')
        rows[:]=[s for s in rows if not s.startswith(name+' = {')]
        rows.append(name+' = {\n'+body+'\n}')
    def effect(n,b):replace(ef,n,b)
    def trigger(n,b):replace(tr,n,b)
    def body(source,name):
        m=re.search(r'\b'+re.escape(name)+r'\s*=\s*\{',source);a=m.end();i=a;d=1
        while d:d+=(source[i]=='{')-(source[i]=='}');i+=1
        return source[a:i-1]
    cw=(root/'common/scripted_effects/mdcw_cold_war_effects.txt').read_text(encoding='utf-8-sig')
    effect('icwt_native_sanction_lifted',body(cw,'mdcw_cw_on_sanction_lifted').replace('ROOT','event_target:icwt_sanction_owner'))
    native=(root/'common/scripted_diplomatic_actions/imp_sanctions_diplomatic_actions.txt').read_text(encoding='utf-8-sig')
    for typ,num in SANCTIONS:
        action={'dip':'diplo','fin':'fin','eco':'eco','mil':'mil'}[typ]
        raw=body(body(native,f'imp_{action}_sanctions_lift'),'complete_effect')
        effect(f'icwt_lift_{typ}_native',raw.replace('ROOT','event_target:icwt_sanction_owner').replace('mdcw_cw_on_sanction_lifted','icwt_native_sanction_lifted'))
        trigger(f'icwt_can_impose_{typ}',f'NOT = {{ check_variable = {{ ROOT.icwt_block_{typ}@THIS > 0 }} }}')
    fee=[];relief=[]
    for typ,num in SANCTIONS:
        cond=f'OR = {{ check_variable = {{ icwt_sanction_mask = {num} }} check_variable = {{ icwt_sanction_mask = 5 }} }} is_in_array = {{ array = imp_{typ}_sanc_by_us value = var:icwt_other }}'
        fee.append(f'if = {{ limit = {{ {cond} }} add_to_temp_variable = {{ icwt_fee = 35 }} }}')
        relief.append(f'if = {{ limit = {{ {cond} }} add_political_power = -35 var:icwt_other = {{ icwt_lift_{typ}_native = yes }} }}')
    effect('icwt_fee','set_temp_variable = { icwt_fee = 0 }\n'+'\n'.join(fee))
    effect('icwt_apply_relief','save_event_target_as = icwt_sanction_owner\n'+'\n'.join(relief))
    effect('icwt_set_other','if = { limit = { tag = USA } set_variable = { icwt_other = SOV.id } } else = { set_variable = { icwt_other = USA.id } }')
    # Modifier lookups are between the investor and actual controller, never a global benefit.
    for kind in ('cost','duration'):
        gate='ROOT' if kind=='cost' else 'PREV'
        target='investments_cost_modifier' if kind=='cost' else 'receiving_investment_duration_temp'
        effect('icwt_investment_'+kind+'_extra',f'''
set_temp_variable = {{ icwt_invest_extra = 0 }}
if = {{ limit = {{ check_variable = {{ icwt_investment@ROOT = 1 }} }} set_temp_variable = {{ icwt_invest_extra = 0.05 }} }}
if = {{ limit = {{ check_variable = {{ icwt_investment@ROOT = 2 }} }} set_temp_variable = {{ icwt_invest_extra = 0.10 }} }}
PREV.PREV = {{
 if = {{ limit = {{ has_country_flag = mutual_investment_treaty_@{gate} }} subtract_from_temp_variable = {{ icwt_invest_extra = 0.05 }} }}
}}
clamp_temp_variable = {{ var = icwt_invest_extra min = 0 max = 0.10 }}
subtract_from_temp_variable = {{ {target} = icwt_invest_extra }}
''')
    for n in range(1,len(TREATIES)+1):
        effect(f'icwt_invite_active_{n}',f'''if = {{ limit = {{ icwt_core = yes has_country_flag = icwt_member_{n} PREV = {{ exists = yes NOT = {{ tag = USA }} NOT = {{ tag = SOV }} NOT = {{ has_country_flag = icwt_member_{n} }} }} check_variable = {{ global.icwt_{n}_members^num < 8 }} OR = {{ check_variable = {{ global.icwt_{n}_invites^num < 6 }} is_in_array = {{ array = global.icwt_{n}_invites value = PREV }} }} }}
if = {{ limit = {{ NOT = {{ is_in_array = {{ array = global.icwt_{n}_invites value = PREV }} }} }} add_to_array = {{ global.icwt_{n}_invites = PREV.id }} }}
PREV = {{ set_variable = {{ icwt_invite_{n} = global.icwt_{n}_revision }} clear_variable = icwt_review_revision clear_variable = icwt_accept_{n} country_event = {{ id = icwt.{100+n} }} }}
icwt_touch = yes }}''')
        # Read-only current fee, including the actual volunteer recall when relevant.
        effect(f'icwt_prepare_cost_{n}',f'''
icwt_set_other = yes
set_variable = {{ icwt_sanction_mask = global.icwt_p_sanctions }} icwt_fee = yes
set_variable = {{ icwt_current_fee = icwt_fee }} set_variable = {{ icwt_current_cp = 0 }}
if = {{ limit = {{ tag = USA }} set_variable = {{ icwt_withdraw_target = global.icwt_p_usa_target }} }} else = {{ set_variable = {{ icwt_withdraw_target = global.icwt_p_sov_target }} }}
if = {{ limit = {{ OR = {{ check_variable = {{ global.icwt_p_regional = 2 }} check_variable = {{ global.icwt_p_regional = 3 }} }} check_variable = {{ icwt_withdraw_target > 0 }} var:icwt_withdraw_target = {{ exists = yes has_volunteers_amount_from = {{ tag = PREV count > 0 }} }} }}
 add_to_variable = {{ icwt_current_fee = 50 }} set_variable = {{ icwt_current_cp = 15 }}
 if = {{ limit = {{ NOT = {{ has_game_rule = {{ rule = allow_recall_intervention_forces option = yes }} }} }} set_variable = {{ global.icwt_preflight = 0 }} }}
}}
''')
        # Core amounts remain the send-time fixed quantities. Re-review cannot silently change them.
        effect(f'icwt_preflight_{n}',f'''
set_variable = {{ global.icwt_preflight = 1 }}
if = {{ limit = {{ check_variable = {{ global.icwt_p_regional > 0 }} OR = {{ NOT = {{ var:global.icwt_p_usa_target = {{ exists = yes NOT = {{ tag = USA }} }} }} NOT = {{ var:global.icwt_p_sov_target = {{ exists = yes NOT = {{ tag = SOV }} }} }} }} }} set_variable = {{ global.icwt_preflight = 0 }} }}
USA = {{ icwt_prepare_cost_{n} = yes if = {{ limit = {{ OR = {{ NOT = {{ icwt_assets_{n} = yes }} NOT = {{ check_variable = {{ icwt_current_fee = icwt_plan_fee_{n} }} }} NOT = {{ check_variable = {{ var = political_power value = icwt_current_fee compare = greater_than_or_equals }} }} NOT = {{ check_variable = {{ var = command_power value = icwt_current_cp compare = greater_than_or_equals }} }} }} }} set_variable = {{ global.icwt_preflight = 0 }} }} }}
SOV = {{ icwt_prepare_cost_{n} = yes if = {{ limit = {{ OR = {{ NOT = {{ icwt_assets_{n} = yes }} NOT = {{ check_variable = {{ icwt_current_fee = icwt_plan_fee_{n} }} }} NOT = {{ check_variable = {{ var = political_power value = icwt_current_fee compare = greater_than_or_equals }} }} NOT = {{ check_variable = {{ var = command_power value = icwt_current_cp compare = greater_than_or_equals }} }} }} }} set_variable = {{ global.icwt_preflight = 0 }} }} }}
''')
        # Amend existing generator bodies rather than duplicating provider logic.
        def existing(name):return next(x for x in ef if x.startswith(name+' = {')).split('\n',1)[1].rsplit('\n}',1)[0]
        send=existing(f'icwt_send_{n}')
        send=send.replace(f'icwt_plan_{n} = yes }}',f'icwt_plan_{n} = yes icwt_prepare_cost_{n} = yes set_variable = {{ icwt_plan_fee_{n} = icwt_current_fee }} set_variable = {{ icwt_plan_cp_{n} = icwt_current_cp }} }}')
        effect(f'icwt_send_{n}',send)
        sign=existing(f'icwt_sign_{n}')
        sign=sign.replace(f'set_variable = {{ global.icwt_{n}_revision = global.icwt_p_revision }}',f'''set_variable = {{ global.icwt_{n}_revision = global.icwt_p_revision }}
clear_array = global.icwt_{n}_invites for_each_loop = {{ array = global.icwt_p_invites value = icwt_invite_copy add_to_array = {{ global.icwt_{n}_invites = icwt_invite_copy }} }}''')
        sign=sign.replace(f'USA = {{ icwt_join_{n} = yes }}', '\n'.join(f'if = {{ limit = {{ check_variable = {{ global.icwt_{n}_duration = {days} }} }} country_event = {{ id = icwt.{600+n} days = {days} }} }}' for days in OPTIONS['duration'] if days>0)+f'\nUSA = {{ icwt_join_{n} = yes }}',1)
        guard_end=sign.index('\nset_variable = { global.icwt_')
        sign=sign[:guard_end]+f'\nicwt_preflight_{n} = yes\nif = {{ limit = {{ check_variable = {{ global.icwt_preflight = 1 }} }}'+sign[guard_end:]
        sign=sign.replace(f'USA = {{ icwt_join_{n} = yes }} SOV = {{ icwt_join_{n} = yes }}',f'''USA = {{ icwt_join_{n} = yes set_variable = {{ icwt_sanction_mask = global.icwt_{n}_sanctions }} icwt_set_other = yes icwt_apply_relief = yes }}
SOV = {{ icwt_join_{n} = yes set_variable = {{ icwt_sanction_mask = global.icwt_{n}_sanctions }} icwt_set_other = yes icwt_apply_relief = yes }}
news_event = {{ id = icwt.{2000+n} }}''')
        sign=re.sub(r'set_variable = \{ global.icwt_news_template = \d+ \} set_variable = \{ global.icwt_news_actor = THIS.id \} news_event = \{ id = icwt.200 \}', '',sign)
        # End nested preflight then original identity guard. Failure leaves every asset/treasury intact.
        sign=sign.rsplit('}',1)[0]+'} else = { icwt_clear_reviews = yes country_event = { id = icwt.500 } }\n}'
        effect(f'icwt_sign_{n}',sign)
        join=existing(f'icwt_join_{n}')
        join=join.replace('clear_variable = icwt_accept_',f'if = {{ limit = {{ NOT = {{ icwt_core = yes }} }} news_event = {{ id = icwt.{2100+n} }} }}\nclear_variable = icwt_accept_',1)
        effect(f'icwt_join_{n}',join)
        effect(f'icwt_accept_invite_{n}',existing(f'icwt_accept_invite_{n}').replace(f'set_variable = {{ global.icwt_news_template = {n} }} set_variable = {{ global.icwt_news_actor = THIS.id }} news_event = {{ id = icwt.201 }}',''))
        effect(f'icwt_leave_{n}',existing(f'icwt_leave_{n}').replace(f'set_variable = {{ global.icwt_news_template = {n} }} set_variable = {{ global.icwt_news_actor = THIS.id }} news_event = {{ id = icwt.202 }}',f'news_event = {{ id = icwt.{2200+n} }}'))
        for kind,base in (('signed',2000),('joined',2100),('left',2200)):
            loc(f'icwt_news_{kind}_{n}',TREATIES[n-1][1]+(': agreement signed' if kind=='signed' else ': [FROM.GetName] '+('joins' if kind=='joined' else 'withdraws')))
            events.append(f'news_event = {{ id = icwt.{base+n} title = icwt_news_{kind}_{n} desc = icwt_news_{kind}_static picture = GFX_icwt_news is_triggered_only = yes major = yes option = {{ name = icwt_news_ack }} }}')
        expire=f'''if = {{ limit = {{ check_variable = {{ global.icwt_{n}_end > 0 }} check_variable = {{ global.icwt_{n}_members^num > 0 }} check_variable = {{ var = global.num_days value = global.icwt_{n}_end compare = greater_than_or_equals }} }}
for_each_scope_loop = {{ array = global.icwt_{n}_members clr_country_flag = icwt_member_{n} remove_ideas = icwt_spirit_{n} }}
clear_array = global.icwt_{n}_members icwt_refresh = yes }}'''
        effect(f'icwt_expire_{n}',expire)
        events.append(f'country_event = {{ id = icwt.{600+n} hidden = yes is_triggered_only = yes immediate = {{ icwt_expire_{n} = yes }} }}')
    events[:]=[e for e in events if not any(e.startswith(f'news_event = {{ id = icwt.{i} ') for i in (200,201,202))]
    events.append('country_event = { id = icwt.501 title = icwt_consult_title desc = icwt_consult_desc picture = GFX_icwt_country is_triggered_only = yes option = { name = icwt_news_ack } }')
    events.append('country_event = { id = icwt.500 title = icwt_changed_title desc = icwt_changed_desc picture = GFX_icwt_country is_triggered_only = yes option = { name = icwt_later } }')
    loc('icwt_changed_title','The proposed concessions have changed')
    loc('icwt_changed_desc','The current stocks, costs or recall conditions no longer match the reviewed paper. No agreement has been concluded. Revise and resubmit the terms.')
    loc('icwt_news_signed_static','The United States and Soviet Union have concluded the agreement. Its signatories have accepted the stated protocols. Further governments may join only following their own consent.')
    loc('icwt_news_joined_static','[FROM.GetName] has joined the agreement following its own approval. Its participation takes effect under the accepted protocols.')
    loc('icwt_news_left_static','[FROM.GetName] has announced its withdrawal. Its continuing treaty effects and obligations have ended. Other signatories retain authority over their own participation.')
    # Investment and trade protocols take their maximum, not the sum of overlapping agreements.
    pair=existing('icwt_pair_recalculate')
    for typ,num in SANCTIONS:
        pair=pair.replace('set_temp_variable = { icwt_pair_trade = 0 }',f'set_temp_variable = {{ icwt_block_{typ} = 0 }}\nset_temp_variable = {{ icwt_pair_trade = 0 }}',1)
        pair+='\nset_variable = { icwt_block_'+typ+'@PREV = icwt_block_'+typ+' }'
        for n in range(1,len(TREATIES)+1):
            needle=f'if = {{ limit = {{ check_variable = {{ global.icwt_{n}_sanctions > 0 }} }} set_temp_variable = {{ icwt_pair_peace = 1 }} }}'
            addition=f'\n if = {{ limit = {{ OR = {{ tag = USA tag = SOV }} PREV = {{ OR = {{ tag = USA tag = SOV }} }} OR = {{ check_variable = {{ global.icwt_{n}_sanctions = {num} }} check_variable = {{ global.icwt_{n}_sanctions = 5 }} }} }} set_temp_variable = {{ icwt_block_{typ} = 1 }} }}'
            pair=pair.replace(needle,needle+addition)
    pair=pair.replace('if = { limit = { NOT = { check_variable = { icwt_trade_applied@PREV', 'if = { limit = { has_country_flag = trade_agreement@PREV } set_temp_variable = { icwt_pair_trade = 0 } }\nif = { limit = { NOT = { check_variable = { icwt_trade_applied@PREV',1)
    effect('icwt_pair_recalculate',pair)
    # Visit only actual treaty partners and the previous partner set needed for cleanup.
    # Eleven instruments with eight members have at most 616 directed active links.
    country=existing('icwt_refresh_country')
    old='for_each_scope_loop = { array = global.icwt_roster limit = { exists = yes NOT = { tag = PREV } } icwt_pair_recalculate = yes }'
    gather='\n'.join(f'''if = {{ limit = {{ has_country_flag = icwt_member_{n} }} for_each_scope_loop = {{ array = global.icwt_{n}_members limit = {{ exists = yes NOT = {{ tag = PREV }} }}
PREV = {{ if = {{ limit = {{ NOT = {{ is_in_array = {{ array = icwt_partners value = PREV }} }} }} add_to_array = {{ icwt_partners = PREV.id }} }} }}
}} }}''' for n in range(1,len(TREATIES)+1))
    country=country.replace(old,gather+'\nfor_each_scope_loop = { array = icwt_partners icwt_pair_recalculate = yes }\nclear_array = icwt_partners\n'+gather)
    effect('icwt_refresh_country',country)
    refresh=existing('icwt_refresh')
    refresh=refresh.replace('array = global.icwt_roster limit = { exists = yes } icwt_refresh_country','array = global.icwt_roster icwt_refresh_country')
    refresh+='\nclear_array = global.icwt_roster\n'+ '\n'.join(f'for_each_scope_loop = {{ array = global.icwt_{n}_members limit = {{ exists = yes NOT = {{ is_in_array = {{ array = global.icwt_roster value = THIS }} }} }} add_to_array = {{ global.icwt_roster = THIS.id }} }}' for n in range(1,len(TREATIES)+1))
    effect('icwt_refresh',refresh)
    weekly=existing('icwt_weekly')
    cleanup=[]
    for n in range(1,len(TREATIES)+1):
        cleanup.append(f'''clear_array = global.icwt_dead
for_each_scope_loop = {{ array = global.icwt_{n}_members
 if = {{ limit = {{ NOT = {{ exists = yes }} }} clr_country_flag = icwt_member_{n} remove_ideas = icwt_spirit_{n}
 add_to_array = {{ global.icwt_dead = THIS.id }} }}
}}
for_each_loop = {{ array = global.icwt_dead value = icwt_dead_id remove_from_array = {{ array = global.icwt_{n}_members value = var:icwt_dead_id }} }}''')
    effect('icwt_weekly','\n'.join(cleanup)+'''\nclear_array = global.icwt_dead
if = { limit = { icwt_pending = yes OR = { NOT = { country_exists = USA } NOT = { country_exists = SOV } } } clear_variable = global.icwt_pending icwt_clear_reviews = yes }
'''+weekly)
    # Read-only native previews for third-party approval, including exact frozen stock counts.
    for n in range(1,len(TREATIES)+1):
        preview=[f'effect_tooltip = {{ add_ideas = icwt_spirit_{n}']
        for prefix,condition in (('global.icwt_p_',f'check_variable = {{ global.icwt_pending = {n} }}'),(f'global.icwt_{n}_',f'NOT = {{ check_variable = {{ global.icwt_pending = {n} }} }}')):
            preview.append('if = { limit = { '+condition+' }')
            preview.append(f'if = {{ limit = {{ icwt_reviewed_{n} = yes check_variable = {{ icwt_review_revision = icwt_invite_{n} }} }} icwt_preview_assets_{n} = yes }} else = {{')
            for equip in EQUIPMENT:
                group=1 if equip in ICBM else 2 if equip in MRBM else 3
                preview.append(f'''if = {{ limit = {{ OR = {{ check_variable = {{ {prefix}scope = {group} }} check_variable = {{ {prefix}scope = 4 }} }} }}
set_temp_variable = {{ icwt_preview_qty = num_equipment@{equip} }} multiply_temp_variable = {{ icwt_preview_qty = {prefix}reduction }} divide_temp_variable = {{ icwt_preview_qty = 100 }} round_temp_variable = icwt_preview_qty multiply_temp_variable = {{ icwt_preview_qty = -1 }} add_equipment_to_stockpile = {{ type = {equip} amount = icwt_preview_qty }} }}''')
            preview.append('}')
            preview.append(f'icwt_preview_limit_{"pending" if prefix=="global.icwt_p_" else "standing"}_{n} = yes')
            for level in (1,2):
                preview.append(f'if = {{ limit = {{ check_variable = {{ {prefix}investment = {level} }} }} custom_effect_tooltip = icwt_investment_{level}_effect }}')
                preview.append(f'if = {{ limit = {{ check_variable = {{ {prefix}trade = {level} }} }}')
                for tag in ('USA','SOV'):preview.append(f'if = {{ limit = {{ NOT = {{ tag = {tag} }} country_exists = {tag} }} add_opinion_modifier = {{ target = {tag} modifier = icwt_trade_{level} }} add_opinion_modifier = {{ target = {tag} modifier = icwt_relations_{level} }} }}')
                preview.append('}')
            preview.append('}')
        preview.append('}')
        effect(f'icwt_preview_join_{n}','\n'.join(preview))
        # Invitations are notification-only; approval is a reviewed, version-checked decision.
        for i,event in enumerate(events):
            if event.startswith(f'country_event = {{ id = icwt.{100+n} '):events[i]=event.replace(f'icwt_review_{n} = yes ai_chance',f'icwt_preview_join_{n} = yes icwt_review_{n} = yes ai_chance')
        reviewed=existing(f'icwt_review_{n}')
        reviewed=reviewed.replace('icwt_touch = yes',f'if = {{ limit = {{ NOT = {{ icwt_core = yes }} }} country_event = {{ id = icwt.{300+n} }} }}\nicwt_touch = yes')
        effect(f'icwt_review_{n}',reviewed)
        events.append(f'''country_event = {{ id = icwt.{300+n} title = icwt_title_{n} desc = icwt_reviewed_invitation_desc picture = GFX_icwt_country is_triggered_only = yes
trigger = {{ icwt_invitation_{n} = yes icwt_reviewed_{n} = yes }}
option = {{ name = icwt_accept_option trigger = {{ check_variable = {{ icwt_review_revision = icwt_invite_{n} }} }} icwt_preview_join_{n} = yes hidden_effect = {{ icwt_accept_invite_{n} = yes }} ai_chance = {{ factor = 0 }} }}
option = {{ name = icwt_decline_option hidden_effect = {{ if = {{ limit = {{ check_variable = {{ icwt_review_revision = icwt_invite_{n} }} }} clear_variable = icwt_invite_{n} clear_variable = icwt_accept_{n} }} }} ai_chance = {{ factor = 100 }} }}
option = {{ name = icwt_later }}
}}''')
    loc('icwt_reviewed_invitation_desc','The complete proposed effects are presented below. Our government may join the agreement or decline the invitation. The core parties can proceed without us.')
    loc('icwt_accept_option','Approve our participation')
    loc('icwt_decline_option','Decline the invitation')
