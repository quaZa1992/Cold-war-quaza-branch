# IMPERIA COLD WAR — Deterministic dossier observations and native intelligence disclosure
"""Emit passive caches. No effect in this module executes a gameplay transaction."""
import re
PAGE = 5

COLS = ('actor', 'target', 'kind', 'state', 'amount', 'date', 'place', 'type', 'size', 'left', 'detail', 'key')
KINDS = {1:'Lend-lease', 2:'Volunteer deployment', 3:'Military attache', 4:'Imperia sanctions',
         5:'Improved trade agreement', 6:'Trade correspondence', 7:'Money transfer',
         8:'Foreign investment', 9:'Assistance programme', 10:'Public political support',
         11:'Political interference', 12:'Economic aid', 13:'Financial subsidy'}
PROGRAMMES = ('Construction Assistance', 'Technical Mission', 'Industrial Equipment Programme',
              'Productivity Mission', 'Consumer Supply Credits', 'Military Training Mission',
              'Arms Production Assistance', 'Administrative Assistance')
BUILDINGS = ('industrial_complex','arms_factory','dockyard','infrastructure','offices','anti_air_building',
             'radar_station','air_base','fuel_silo','internet_station','renewable_energy_infra',
             'fossil_powerplant','nuclear_reactor','agriculture_district','uranium_mine')


def sets(prefix, source, columns=COLS, temp=False):
    op = 'set_temp_variable' if temp else 'set_variable'
    return '\n'.join(f'{op} = {{ {prefix}{c} = {source}{c} }}' for c in columns)


def build(write, block, mark):
    def synchronized_scratch(source):
        # A fixed, synchronous metadata packet survives scope switches explicitly.
        # No event, timer or GUI selection may consume this scratch packet later.
        source=re.sub(r'(?<![\w.])icsd_t_(\w+)',r'global.icsd_t_\1',source)
        for old,new in [('set_temp_variable','set_variable'),('add_to_temp_variable','add_to_variable'),('subtract_from_temp_variable','subtract_from_variable')]:
            source=re.sub(r'\b'+old+r'(\s*=\s*\{\s*global\.icsd_t_)',new+r'\1',source)
        return source
    triggers = '''
icsd_country = { IMP_is_1970_scenario = yes OR = { tag = USA tag = SOV } }
icsd_view_access = { icsd_country = yes is_ai = no }
icsd_has_selection = { check_variable = { icsd_selected_kind > 0 } check_variable = { icsd_selected_target > 0 } }
icsd_can_locate = { icsd_country = yes check_variable = { icsd_response_target > 0 } var:icsd_response_target = { exists = yes capital_scope = { is_owned_by = PREV } } }
# THIS observer. Source identities are captured before entering either observer.
# Native synchronized country intelligence, never local-player or GUI state.
icsd_event_access = {
 OR = {
  check_variable = { icsd_t_actor = THIS.id }
  check_variable = { icsd_t_target = THIS.id }
  intel_level_over = { target = var:icsd_t_actor civilian_intel > 0.59999 }
  network_strength = { target = var:icsd_t_target value > 49.999 }
 }
}
icsd_cached_access = {
 OR = {
  check_variable = { icsd_t_actor = THIS.id }
  check_variable = { icsd_t_target = THIS.id }
  AND = { check_variable = { icsd_t_actor = USA.id } check_variable = { icsd_civ_usa = 1 } }
  AND = { check_variable = { icsd_t_actor = SOV.id } check_variable = { icsd_civ_sov = 1 } }
  var:icsd_t_target = { PREV = { check_variable = { icsd_network@PREV = 1 } } }
 }
}
'''
    write('common/scripted_triggers/ICW_superpower_dossier.txt',mark+synchronized_scratch(triggers))
    e=[mark]
    def effect(name, body):e.append(block(name,body))
    effect('icsd_touch','add_to_variable = { icsd_dirty = 1 }')
    effect('icsd_reset_observation','\n'.join(f'set_temp_variable = {{ icsd_t_{c} = 0 }}' for c in COLS)+'\nset_temp_variable = { icsd_t_date = global.date }')
    effect('icsd_clear_observation','\n'.join(f'clear_variable = global.icsd_t_{c}' for c in COLS))
    effect('icsd_clear_live','\n'.join(f'clear_array = icsd_live_{c}' for c in COLS))
    effect('icsd_append_live','''
if = { limit = { icsd_country = yes }
 set_temp_variable = { icsd_t_detail = 1 }
 if = { limit = { OR = { check_variable = { icsd_t_kind = 8 } check_variable = { icsd_t_kind = 9 } check_variable = { icsd_t_kind = 13 } } NOT = { icsd_cached_access = yes } }
  set_temp_variable = { icsd_t_detail = 0 }
 }
 # Unknown subsidies leave no row or count. Public investment/assistance retain a redacted cover.
 if = { limit = { OR = { NOT = { check_variable = { icsd_t_kind = 13 } } check_variable = { icsd_t_detail = 1 } } }
'''+ '\n'.join(f'add_to_array = {{ icsd_live_{c} = icsd_t_{c} }}' for c in COLS if c not in ('amount','place','size','left','type'))+'''
  if = { limit = { check_variable = { icsd_t_detail = 1 } }
'''+ '\n'.join(f'add_to_array = {{ icsd_live_{c} = icsd_t_{c} }}' for c in ('amount','place','size','left','type'))+'''
  } else = {
'''+ '\n'.join(f'add_to_array = {{ icsd_live_{c} = 0 }}' for c in ('amount','place','size','left'))+'''
   # The assistance category is public; the investment site and building are withheld.
   if = { limit = { check_variable = { icsd_t_kind = 9 } } add_to_array = { icsd_live_type = icsd_t_type } }
   else = { add_to_array = { icsd_live_type = 0 } }
  }
 }
}
''')
    effect('icsd_publish_live','\n'.join(f'if = {{ limit = {{ country_exists = {tag} }} {tag} = {{ icsd_append_live = yes }} }}' for tag in ('USA','SOV'))+'\nicsd_clear_observation = yes')
    effect('icsd_append_mail','''
if = { limit = { icsd_country = yes }
 if = { limit = { check_variable = { icsd_mail_kind^num > 23 } }
'''+ '\n'.join(f'remove_from_array = {{ array = icsd_mail_{c} index = 0 }}' for c in COLS)+'''
 }
'''+ '\n'.join(f'add_to_array = {{ icsd_mail_{c} = icsd_t_{c} }}' for c in COLS)+'''
 icsd_touch = yes
}
''')
    effect('icsd_publish_mail','''
if = { limit = { IMP_is_1970_scenario = yes OR = { check_variable = { icsd_t_actor = USA.id } check_variable = { icsd_t_actor = SOV.id } check_variable = { icsd_t_target = USA.id } check_variable = { icsd_t_target = SOV.id } } }
 add_to_variable = { global.icsd_sequence = 1 }
 set_temp_variable = { icsd_t_key = global.icsd_sequence }
 set_temp_variable = { icsd_t_detail = 1 }
'''+ '\n'.join(f'''if = {{ limit = {{ country_exists = {tag} }} {tag} = {{
 if = {{ limit = {{ OR = {{
  check_variable = {{ icsd_t_actor = THIS.id }} check_variable = {{ icsd_t_target = THIS.id }}
  AND = {{ OR = {{ check_variable = {{ icsd_t_state = 2 }} check_variable = {{ icsd_t_state = 5 }} }} icsd_event_access = yes }}
 }} }} icsd_append_mail = yes
  if = {{ limit = {{ has_country_flag = icsd_open }} icsd_build_view = yes }}
 }}
}} }}''' for tag in ('USA','SOV'))+'''
}
icsd_clear_observation = yes
''')
    for kind,name in ((6,'trade'),(7,'money')):
        for state,verb in ((1,'sent'),(2,'accepted'),(3,'declined')):
            effect(f'icsd_note_{name}_{verb}',f'''icsd_reset_observation = yes
set_temp_variable = {{ icsd_t_actor = ROOT.id }}
set_temp_variable = {{ icsd_t_target = THIS.id }}
set_temp_variable = {{ icsd_t_kind = {kind} }}
set_temp_variable = {{ icsd_t_state = {state} }}
set_temp_variable = {{ icsd_t_amount = {'ROOT.gift_size' if kind==7 else '0'} }}
icsd_publish_mail = yes''')
    effect('icsd_note_politics','''
# Called after the native manipulation completed: THIS target, ROOT sponsor.
# USA/SOV use the ordinary single-party branch; do not attribute other countries' special branches.
if = { limit = { OR = { ROOT = { tag = USA } ROOT = { tag = SOV } } }
 icsd_reset_observation = yes
 set_temp_variable = { icsd_t_actor = ROOT.id }
 set_temp_variable = { icsd_t_target = THIS.id }
 set_temp_variable = { icsd_t_type = ROOT.ruling_party }
 set_temp_variable = { icsd_t_kind = 11 }
 set_temp_variable = { icsd_t_state = 5 }
 icsd_publish_mail = yes
}
''')
    effect('icsd_note_economic_aid','''
# Called after the existing flat-amount aid transfer: THIS sender, named target recipient.
icsd_reset_observation = yes
set_temp_variable = { icsd_t_actor = THIS.id }
set_temp_variable = { icsd_t_target = event_target:influence_recipient.id }
set_temp_variable = { icsd_t_amount = global.mp_aid_amount }
set_temp_variable = { icsd_t_kind = 12 }
set_temp_variable = { icsd_t_state = 5 }
icsd_publish_mail = yes
''')
    effect('icsd_note_gdp_aid','''
# Existing GDP-based aid, after recipient credit. FROM donor, THIS recipient.
icsd_reset_observation = yes
set_temp_variable = { icsd_t_actor = FROM.id }
set_temp_variable = { icsd_t_target = THIS.id }
set_temp_variable = { icsd_t_amount = temp_amount_gift_sum }
set_temp_variable = { icsd_t_kind = 12 }
set_temp_variable = { icsd_t_state = 5 }
icsd_publish_mail = yes
''')
    # Startup/save migration cannot retrospectively reveal old foreign financial history.
    effect('icsd_migrate_legacy','''
if = { limit = { icsd_country = yes }
 for_each_loop = { array = global.icsd_mail_kind index = icsd_legacy_i value = icsd_legacy_kind
  icsd_reset_observation = yes
'''+ '\n'.join(f'set_temp_variable = {{ icsd_t_{c} = global.icsd_mail_{c}^icsd_legacy_i }}' for c in ('actor','target','kind','state','amount','date'))+'''
  if = { limit = { OR = { check_variable = { icsd_t_actor = THIS.id } check_variable = { icsd_t_target = THIS.id } } }
   add_to_variable = { global.icsd_sequence = 1 }
   set_temp_variable = { icsd_t_key = global.icsd_sequence }
   set_temp_variable = { icsd_t_detail = 1 }
   icsd_append_mail = yes
  }
 }
}
''')
    effect('icsd_initialize','''
if = { limit = { IMP_is_1970_scenario = yes NOT = { check_variable = { global.icsd_version = 2 } } }
 set_variable = { global.icsd_version = 2 }
 set_global_flag = icsd_initialized
 if = { limit = { country_exists = USA } USA = { clear_variable = icsd_selected_kind icsd_migrate_legacy = yes } }
 if = { limit = { country_exists = SOV } SOV = { clear_variable = icsd_selected_kind icsd_migrate_legacy = yes } }
'''+ '\n'.join(f'clear_array = global.icsd_mail_{c}' for c in ('actor','target','kind','state','amount','date'))+'''
 clear_array = global.icsd_report_actor
 clear_array = global.icsd_report_target
 clear_array = global.icsd_report_kind
 set_variable = { global.icsd_weekly_date = global.num_days }
 icsd_reconcile = yes
}
''')
    effect('icsd_prepare_observer','''
icsd_clear_live = yes
set_variable = { icsd_civ_usa = 0 }
set_variable = { icsd_civ_sov = 0 }
if = { limit = { country_exists = USA intel_level_over = { target = USA civilian_intel > 0.59999 } } set_variable = { icsd_civ_usa = 1 } }
if = { limit = { country_exists = SOV intel_level_over = { target = SOV civilian_intel > 0.59999 } } set_variable = { icsd_civ_sov = 1 } }
''')
    scanning=[]
    for obs in ('USA','SOV'):
        scanning.append(f'''if = {{ limit = {{ country_exists = {obs} }} {obs} = {{
 set_variable = {{ icsd_network@PREV = 0 }}
 if = {{ limit = {{ NOT = {{ tag = PREV }} network_strength = {{ target = PREV value > 49.999 }} }} set_variable = {{ icsd_network@PREV = 1 }} }}
}} }}''')
    for actor in ('USA','SOV'):
        sanctions='OR = { '+' '.join(f'is_in_array = {{ array = {actor}.imp_{k}_sanc_by_us value = THIS }}' for k in ('dip','fin','eco','mil'))+' }'
        checks=((1,f'{actor} = {{ is_lend_leasing = PREV }}'),(2,f'has_volunteers_amount_from = {{ tag = {actor} count > 0 }}'),
                (3,f'has_attache_from = {actor}'),(4,sanctions),(5,f'has_country_flag = trade_agreement@{actor}'))
        scanning.append(f'if = {{ limit = {{ country_exists = {actor} NOT = {{ tag = {actor} }} }}')
        for kind,trigger in checks:
            scanning.append(f'''if = {{ limit = {{ {trigger} }} icsd_reset_observation = yes
 set_temp_variable = {{ icsd_t_actor = {actor}.id }} set_temp_variable = {{ icsd_t_target = THIS.id }}
 set_temp_variable = {{ icsd_t_kind = {kind} }} icsd_publish_live = yes }}''')
        scanning.append(f'''if = {{ limit = {{ check_variable = {{ {actor}.active_subsidies@THIS > 0 }} }}
 icsd_reset_observation = yes set_temp_variable = {{ icsd_t_actor = {actor}.id }} set_temp_variable = {{ icsd_t_target = THIS.id }}
 set_temp_variable = {{ icsd_t_kind = 13 }} set_temp_variable = {{ icsd_t_amount = {actor}.active_subsidies@THIS }}
 icsd_publish_live = yes }}''')
        scanning.append('}')
    effect('icsd_scan_investments','''
# Exactly the native 15 project slots, no state search. THIS is USA or SOV.
for_loop_effect = { start = 0 end = 15 value = icsd_slot
 if = { limit = { check_variable = { project_array^icsd_slot < 0 } check_variable = { project_build_amount^icsd_slot > 0 } check_variable = { project_target_country^icsd_slot > 0 } }
  if = { limit = { var:project_target_country^icsd_slot = { exists = yes } }
   icsd_reset_observation = yes
   set_temp_variable = { icsd_t_actor = THIS.id }
   set_temp_variable = { icsd_t_target = project_target_country^icsd_slot }
   set_temp_variable = { icsd_t_kind = 8 }
   set_temp_variable = { icsd_t_place = project_array^icsd_slot }
   set_temp_variable = { icsd_t_type = project_building_type^icsd_slot }
   set_temp_variable = { icsd_t_size = project_build_amount^icsd_slot }
   set_temp_variable = { icsd_t_amount = project_monetary_cost^icsd_slot }
   set_temp_variable = { icsd_t_key = icsd_slot } add_to_temp_variable = { icsd_t_key = 1 }
   icsd_publish_live = yes
  }
 }
}
''')
    assistance=['''# Existing outgoing links only. THIS recipient, PREV sponsor inside the loop.
for_each_scope_loop = { array = mdcw_cw_out
 if = { limit = { exists = yes }''']
    for p in range(1,9):
        assistance.append(f'''if = {{ limit = {{ check_variable = {{ PREV.mdcw_cw_p{p}_size@THIS > 0 }} check_variable = {{ PREV.mdcw_cw_p{p}_end@THIS > global.num_days }} }}
 icsd_reset_observation = yes
 set_temp_variable = {{ icsd_t_actor = PREV.id }} set_temp_variable = {{ icsd_t_target = THIS.id }}
 set_temp_variable = {{ icsd_t_kind = 9 }} set_temp_variable = {{ icsd_t_type = {p} }} set_temp_variable = {{ icsd_t_key = {p} }}
 set_temp_variable = {{ icsd_t_size = PREV.mdcw_cw_p{p}_size@THIS }}
 set_temp_variable = {{ icsd_t_left = PREV.mdcw_cw_p{p}_end@THIS }} subtract_from_temp_variable = {{ icsd_t_left = global.num_days }}
 if = {{ limit = {{ check_variable = {{ PREV.mdcw_cw_p{p}_state@THIS = 2 }} }} set_temp_variable = {{ icsd_t_state = 4 }} }}
 icsd_publish_live = yes
}}''')
    assistance.append('''if = { limit = { check_variable = { PREV.mdcw_cw_pps_party@THIS > 0 } check_variable = { PREV.mdcw_cw_pps_end@THIS > global.num_days } }
 icsd_reset_observation = yes
 set_temp_variable = { icsd_t_actor = PREV.id } set_temp_variable = { icsd_t_target = THIS.id }
 set_temp_variable = { icsd_t_kind = 10 }
 set_temp_variable = { icsd_t_type = PREV.mdcw_cw_pps_party@THIS } subtract_from_temp_variable = { icsd_t_type = 1 }
 set_temp_variable = { icsd_t_left = PREV.mdcw_cw_pps_end@THIS } subtract_from_temp_variable = { icsd_t_left = global.num_days }
 icsd_publish_live = yes
}
} }''')
    effect('icsd_scan_assistance','\n'.join(assistance))
    effect('icsd_reconcile','''
if = { limit = { IMP_is_1970_scenario = yes }
 if = { limit = { country_exists = USA } USA = { icsd_prepare_observer = yes } }
 if = { limit = { country_exists = SOV } SOV = { icsd_prepare_observer = yes } }
 every_country = { limit = { exists = yes }
'''+ '\n'.join(scanning)+'''
 }
'''+ '\n'.join(f'if = {{ limit = {{ country_exists = {tag} }} {tag} = {{ icsd_scan_investments = yes icsd_scan_assistance = yes }} }}' for tag in ('USA','SOV'))+'''
 set_variable = { global.icsd_review_date = global.date }
 add_to_variable = { global.icsd_revision = 1 }
'''+ '\n'.join(f'if = {{ limit = {{ country_exists = {tag} }} {tag} = {{ if = {{ limit = {{ has_country_flag = icsd_open }} icsd_build_view = yes }} }} }}' for tag in ('USA','SOV'))+'''
}
''')
    identity=' '.join(f'check_variable = {{ icsd_selected_{c} = icsd_item_{c} }}' for c in ('actor','target','kind','key'))
    effect('icsd_view_append',f'''if = {{ limit = {{ {identity} }} set_variable = {{ icsd_selection_found = 1 }}
'''+sets('icsd_selected_','icsd_item_')+'''
}
if = { limit = { check_variable = { var = icsd_view_count value = icsd_offset compare = greater_than_or_equals } check_variable = { icsd_row_count < 5 } }
'''+ '\n'.join(f'if = {{ limit = {{ check_variable = {{ icsd_row_count = {i} }} }}\n'+sets(f'icsd_r{i}_','icsd_item_')+'\n}' for i in range(PAGE))+'''
 add_to_variable = { icsd_row_count = 1 }
}
add_to_variable = { icsd_view_count = 1 }
''')
    effect('icsd_build_view','''
if = { limit = { icsd_country = yes }
 if = { limit = { OR = { check_variable = { icsd_tab < 1 } check_variable = { icsd_tab > 3 } } } set_variable = { icsd_tab = 1 } }
 if = { limit = { check_variable = { icsd_offset < 0 } } set_variable = { icsd_offset = 0 } }
 set_variable = { icsd_view_count = 0 } set_variable = { icsd_row_count = 0 } set_variable = { icsd_selection_found = 0 }
'''+ '\n'.join(f'clear_variable = icsd_r{i}_{c}' for i in range(PAGE) for c in COLS)+'''
 if = { limit = { check_variable = { icsd_history = 1 } }
  set_variable = { icsd_cursor = icsd_mail_kind^num }
  while_loop_effect = { limit = { check_variable = { icsd_cursor > 0 } }
   subtract_from_variable = { icsd_cursor = 1 }
'''+ '\n'.join(f'set_variable = {{ icsd_item_{c} = icsd_mail_{c}^icsd_cursor }}' for c in COLS)+'''
   if = { limit = { OR = { AND = { check_variable = { icsd_tab = 1 } OR = { AND = { tag = USA check_variable = { icsd_item_actor = SOV.id } } AND = { tag = SOV check_variable = { icsd_item_actor = USA.id } } } } AND = { check_variable = { icsd_tab = 3 } OR = { check_variable = { icsd_item_actor = THIS.id } check_variable = { icsd_item_target = THIS.id } } } } } icsd_view_append = yes }
  }
 } else = {
  for_each_loop = { array = icsd_live_kind index = icsd_index value = icsd_value
'''+ '\n'.join(f'set_variable = {{ icsd_item_{c} = icsd_live_{c}^icsd_index }}' for c in COLS)+'''
   if = { limit = { OR = { AND = { check_variable = { icsd_tab = 1 } OR = { AND = { tag = USA check_variable = { icsd_item_actor = SOV.id } } AND = { tag = SOV check_variable = { icsd_item_actor = USA.id } } } } AND = { check_variable = { icsd_tab = 3 } OR = { check_variable = { icsd_item_actor = THIS.id } check_variable = { icsd_item_target = THIS.id } } } } } icsd_view_append = yes }
  }
 }
 if = { limit = { check_variable = { icsd_offset > 0 } check_variable = { icsd_row_count = 0 } } set_variable = { icsd_offset = 0 } icsd_build_view = yes }
 if = { limit = { check_variable = { icsd_selection_found = 0 } }
'''+ '\n'.join(f'clear_variable = icsd_selected_{c}' for c in COLS)+'''
  clear_variable = icsd_route clear_variable = icsd_response_target
 }
 set_variable = { icsd_page = icsd_offset } divide_variable = { icsd_page = 5 } add_to_variable = { icsd_page = 1 }
 set_variable = { icsd_next_offset = icsd_offset } add_to_variable = { icsd_next_offset = 5 }
 set_variable = { icsd_r0_number = icsd_offset } add_to_variable = { icsd_r0_number = 1 }
 set_variable = { icsd_r1_number = icsd_offset } add_to_variable = { icsd_r1_number = 2 }
 set_variable = { icsd_r2_number = icsd_offset } add_to_variable = { icsd_r2_number = 3 }
 set_variable = { icsd_r3_number = icsd_offset } add_to_variable = { icsd_r3_number = 4 }
 set_variable = { icsd_r4_number = icsd_offset } add_to_variable = { icsd_r4_number = 5 }
 icsd_touch = yes
}
''')
    effect('icsd_response_context','''
clear_variable = icsd_context_opponent
if = { limit = { check_variable = { icsd_tab = 1 } check_variable = { icsd_selected_target > 0 } }
for_each_loop = { array = icsd_live_kind index = icsd_context_i value = icsd_context_kind
if = { limit = { check_variable = { icsd_context_opponent = 0 } check_variable = { icsd_live_actor^icsd_context_i = THIS.id } OR = { check_variable = { icsd_context_kind = 1 } check_variable = { icsd_context_kind = 2 } check_variable = { icsd_context_kind = 3 } } }
set_temp_variable = { icsd_context_candidate = icsd_live_target^icsd_context_i }
if = { limit = { var:icsd_context_candidate = { exists = yes has_war_with = var:PREV.icsd_selected_target } }
set_variable = { icsd_context_opponent = icsd_context_candidate } set_variable = { icsd_response_target = icsd_context_candidate }
}
}
}
}
''')
    for i in range(PAGE):
        effect(f'icsd_select_{i}',f'''if = {{ limit = {{ icsd_country = yes check_variable = {{ icsd_r{i}_kind > 0 }} }}
'''+sets('icsd_selected_',f'icsd_r{i}_')+'''
 clear_variable = icsd_route clear_variable = icsd_response_target
 # Selection is display metadata. No native executor consumes it.
 if = { limit = { check_variable = { icsd_selected_actor = THIS.id } } set_variable = { icsd_response_target = icsd_selected_target } }
 else_if = { limit = { check_variable = { icsd_selected_target = THIS.id } } set_variable = { icsd_response_target = icsd_selected_actor } }
 else { set_variable = { icsd_response_target = icsd_selected_target } }
 icsd_response_context = yes
 icsd_touch = yes
}'''.replace('else {','else = {'))
    effect('icsd_open','''if = { limit = { icsd_country = yes } icsd_initialize = yes set_country_flag = icsd_open clr_country_flag = icsd_picking clear_variable = icsd_route clear_variable = icsd_actions_page icsd_build_view = yes if = { limit = { NOT = { icsd_has_selection = yes } check_variable = { icsd_row_count > 0 } } icsd_select_0 = yes } icwt_display = yes }''')
    effect('icsd_locate','''if = { limit = { icsd_can_locate = yes } var:icsd_response_target = { capital_scope = { goto_state = THIS } } clr_country_flag = icsd_open icsd_touch = yes }''')
    write('common/scripted_effects/ICW_superpower_dossier.txt',synchronized_scratch(''.join(e)))
    write('common/on_actions/ICW_superpower_dossier.txt',mark+'''on_actions = {
on_startup = { effect = { if = { limit = { country_exists = USA } USA = { icsd_initialize = yes } } else_if = { limit = { country_exists = SOV } SOV = { icsd_initialize = yes } } } }
on_weekly = { effect = {
 if = { limit = { icsd_country = yes OR = { tag = USA AND = { NOT = { country_exists = USA } tag = SOV } } }
  icsd_initialize = yes
  if = { limit = { NOT = { check_variable = { global.icsd_weekly_date = global.num_days } } } set_variable = { global.icsd_weekly_date = global.num_days } icsd_reconcile = yes icwt_weekly = yes }
 }
} }
}
''')
    write('common/decisions/categories/ICW_superpower_dossier.txt',mark+'''icsd_category = { icon = GFX_decision_category_generic_political_actions allowed = { always = yes } visible = { OR = { icsd_view_access = yes icwt_invitation_1 = yes has_country_flag = icwt_member_1 icwt_invitation_2 = yes has_country_flag = icwt_member_2 icwt_invitation_3 = yes has_country_flag = icwt_member_3 icwt_invitation_4 = yes has_country_flag = icwt_member_4 icwt_invitation_5 = yes has_country_flag = icwt_member_5 icwt_invitation_6 = yes has_country_flag = icwt_member_6 icwt_invitation_7 = yes has_country_flag = icwt_member_7 icwt_invitation_8 = yes has_country_flag = icwt_member_8 icwt_invitation_9 = yes has_country_flag = icwt_member_9 icwt_invitation_10 = yes has_country_flag = icwt_member_10 icwt_invitation_11 = yes has_country_flag = icwt_member_11 } } }
''')
    write('common/decisions/ICW_superpower_dossier.txt',mark+'''icsd_category = { icsd_open_decision = { icon = icsd_file visible = { icsd_view_access = yes } available = { icsd_view_access = yes } cost = 0 days_re_enable = 0 complete_effect = { hidden_effect = { icsd_open = yes } } ai_will_do = { factor = 0 } } }
''')
