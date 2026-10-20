"""Keep canal revenue, legacy peace implementation and the original shore geography coherent."""
import re
from policy_common import CANAL,ident,has
from script_format import format_script

def register(api):
    # The canal was closed at the 1970 start. Egypt can fund reopening after a ceasefire; the independent
    # Sinai policy programme does not reopen the canal; controlling a shore alone gives no income.
    pay=api.money(.008)
    gate=f'original_tag = EGY IMP_is_1970_scenario = yes controls_state = {CANAL} NOT = {{ has_war_with = ISR }} ISR = {{ NOT = {{ has_country_flag = ISR70_attrition_active }} }}'
    callback=f'''if = {{ limit = {{ has_country_flag = ISR70_policy_egypt_canal_project }}
if = {{ limit = {{ {gate} }} set_global_flag = ISR70_policy_canal_open }}
else = {{ set_temp_variable = {{ treasury_change = ISR70_policy_egypt_canal_paid }} modify_treasury_effect = yes }}
clear_variable = ISR70_policy_egypt_canal_paid clr_country_flag = ISR70_policy_egypt_canal_project }}'''
    event=api.event(1160,'Suez Canal Reopening Works','The reserved canal clearance and reopening programme has reached its completion date. Continued control and ceasefire are required; a failed project returns its original budget.',
        [('Review the completed works.',callback,'',1)],trigger='always = yes',hidden=True)
    api.loc('ISR70_policy_egypt_canal_category','Suez Canal Administration')
    api.loc('ISR70_policy_egypt_reopen_canal','Fund the Reopening of the Suez Canal')
    api.loc('ISR70_policy_egypt_reopen_canal_desc','Reserve 0.8% of annual GDP for a 180-day reopening project. Israeli-Egyptian fighting must have ceased. Completion opens canal traffic; control of the canal shores then determines the normal revenue bonus. Loss of the project conditions refunds the original reservation.')
    api.egypt_decisions=f'''ISR70_policy_egypt_canal_category = {{
ISR70_policy_egypt_reopen_canal = {{ icon = generic_construction cost = 50
visible = {{ original_tag = EGY IMP_is_1970_scenario = yes NOT = {{ has_global_flag = ISR70_policy_canal_open }} }}
available = {{ {gate} NOT = {{ has_country_flag = ISR70_policy_egypt_canal_project }} ISR70_policy_afford_0_0080 = yes }}
complete_effect = {{ set_variable = {{ ISR70_policy_egypt_canal_paid = ISR70_policy_cost_0_0080 }} {pay} set_country_flag = ISR70_policy_egypt_canal_project country_event = {{ id = {event} days = 180 }} }}
days_re_enable = 1 ai_will_do = {{ factor = 1 modifier = {{ factor = 0 is_historical_focus_on = yes date < 1975.6.5 }} }} }} }}'''
    api.tick.append('EGY = { ISR70_policy_refresh_costs = yes }')
    api.tick.append(f'''every_country = {{
if = {{ limit = {{ has_global_flag = ISR70_policy_canal_open NOT = {{ MD_special_countries = yes }} controls_state = 213 controls_state = {CANAL} }}
remove_ideas = partial_control_of_suez add_ideas = full_control_of_suez
}} else_if = {{ limit = {{ has_global_flag = ISR70_policy_canal_open NOT = {{ MD_special_countries = yes }} OR = {{ controls_state = 213 controls_state = {CANAL} }} }}
remove_ideas = full_control_of_suez add_ideas = partial_control_of_suez
}} else = {{ remove_ideas = full_control_of_suez remove_ideas = partial_control_of_suez }} }}''')

def patch(api,write):
    root=api.root
    # Restrict the two legacy canal-grant blocks to later scenarios, and use
    # the original shore state. Preserve all other native hooks.
    path=root/'common/on_actions/02_dod_on_actions.txt';text=path.read_text(encoding='utf-8-sig')
    if '# ISR70 narrow canal adapter' not in text and '# ISR70 canal closure adapter' not in text:
        clean=re.sub(r'"(?:\\.|[^"\\])*"|#[^\n]*',lambda m:' '*len(m[0]),text)
        ranges=[]
        for m in re.finditer(r'\bif\s*=\s*\{',clean):
            start=m.start();end=m.end();depth=1
            while depth:depth+=(clean[end]=='{')-(clean[end]=='}');end+=1
            block=text[start:end]
            if 'add_ideas = full_control_of_suez' in block or 'add_ideas = partial_control_of_suez' in block:
                # Select outer blocks only; nested ROOT/FROM grants are kept.
                ranges.append((start,end,block))
        outer=[r for r in ranges if not any(a<r[0] and b>=r[1] for a,b,_ in ranges)]
        for start,end,block in sorted(outer,reverse=True):
            block=block.replace('controls_state = 214',f'controls_state = {CANAL}').replace('state = 214',f'state = {CANAL}')
            replacement='# ISR70 narrow canal adapter\nif = {\nlimit = { NOT = { IMP_is_1970_scenario = yes } }\n'+block+'\n}'
            text=text[:start]+replacement+text[end:]
    # Undo our superseded split-state references inside owned adapter blocks.
    text=text.replace('controls_state = 1252','controls_state = 214').replace('state = 1252','state = 214')
    text=text.replace('# ISR70 narrow canal adapter','# ISR70 canal closure adapter')
    # Format only our adapter blocks, preserving unrelated native content.
    for marker in reversed(list(re.finditer(r'(?m)^([\t ]*)# ISR70 canal closure adapter\n',text))):
        start=marker.end();opening=text.index('{',start);end=opening+1;depth=1
        while depth:depth+=(text[end]=='{')-(text[end]=='}');end+=1
        formatted='\n'.join(marker[1]+line for line in format_script(text[start:end].strip()).splitlines())
        text=text[:start]+formatted+text[end:]
    write('common/on_actions/02_dod_on_actions.txt',text,normalize=False)
    # Even a stale legacy spirit may not charge closed-canal income between
    # pulse orderings. Both native economic limits have the same explicit gate.
    path=root/'common/scripted_effects/00_money_system.txt';text=path.read_text(encoding='utf-8-sig')
    for spirit in ('full_control_of_suez','partial_control_of_suez'):
        old='limit = { has_idea = '+spirit+' }'
        new='limit = { has_idea = '+spirit+' OR = { NOT = { IMP_is_1970_scenario = yes } has_global_flag = ISR70_policy_canal_open } }'
        text=text.replace(old,new)
    write('common/scripted_effects/00_money_system.txt',text,normalize=False)
