# IMPERIA COLD WAR — COMECON private bounded dossier pagination
from build import *

def page_count(source,dest,size,capacity=32):
    return var(dest,1)+' '+' '.join(choose_count(source,n,var(dest,(n-1)//size+1)) for n in range(size+1,capacity+1,size))

def choose_count(source,n,body):
    return f'if = {{ limit = {{ check_variable = {{ {source} > {n-1} }} }} {body} }}'

def slice_array(source,dest,page,size):
    # Scope pointers are copied unchanged. No country, payment or signature is modified.
    return f'''clear_array = {dest}
set_variable = {{ cc_ui_first = {page} }} multiply_variable = {{ cc_ui_first = {size} }}
set_variable = {{ cc_ui_last = cc_ui_first }} add_to_variable = {{ cc_ui_last = {size} }}
set_variable = {{ cc_ui_index = 0 }}
for_each_scope_loop = {{ array = {source} event_target:cc_ui_viewer = {{
if = {{ limit = {{ NOT = {{ check_variable = {{ cc_ui_index < cc_ui_first }} }} check_variable = {{ cc_ui_index < cc_ui_last }} }} add_to_array = {{ {dest} = PREV }} }}
add_to_variable = {{ cc_ui_index = 1 }} }} }}'''

def compile_pagination():
    out=['save_event_target_as = cc_ui_viewer']
    out += [f'if = {{ limit = {{ NOT = {{ has_variable = {key} }} }} set_variable = {{ {key} = 0 }} }}' for key in ('cc_sheet','cc_register_page','cc_delegate_page','cc_recipient_page','cc_ui_choice_page')]
    out += ['clamp_variable = { var = cc_sheet min = 0 max = 3 }',
        'clamp_variable = { var = cc_register_page min = 0 max = 1 }',
        'if = { limit = { check_variable = { cc_sheet = 2 } check_variable = { cc_ui_offer_count < 3 } } set_variable = { cc_sheet = 1 } }',
        'clear_array = cc_ui_all_delegates clear_array = cc_ui_header_flags set_variable = { cc_ui_index = 0 }',
        '''for_each_scope_loop = { array = global.cc_members if = { limit = { cc_member_country = yes } event_target:cc_ui_viewer = {
add_to_array = { cc_ui_all_delegates = PREV } if = { limit = { check_variable = { cc_ui_index < 10 } } add_to_array = { cc_ui_header_flags = PREV } } add_to_variable = { cc_ui_index = 1 } } } }''',
        var('cc_ui_delegate_count','cc_ui_all_delegates^num'),page_count('cc_ui_delegate_count','cc_ui_delegate_pages',4),
        var('cc_ui_delegate_max','cc_ui_delegate_pages'),'subtract_from_variable = { cc_ui_delegate_max = 1 }',
        'clamp_variable = { var = cc_delegate_page min = 0 max = cc_ui_delegate_max }',
        slice_array('cc_ui_all_delegates','cc_ui_delegates','cc_delegate_page',4)]
    for s in range(1,5):
        body=[var('cc_ui_recipient_count',f'global.cc_{s}_view_recipients^num'),
            page_count('cc_ui_recipient_count','cc_ui_recipient_pages',8),var('cc_ui_recipient_max','cc_ui_recipient_pages'),
            'subtract_from_variable = { cc_ui_recipient_max = 1 }',
            'clamp_variable = { var = cc_recipient_page min = 0 max = cc_ui_recipient_max }',
            slice_array(f'global.cc_{s}_view_recipients','cc_ui_recipients','cc_recipient_page',8)]
        out.append(choose('cc_view_slot',s,' '.join(body)))
    out += [var('cc_ui_leaf',1),var('cc_ui_leaves','cc_ui_recipient_pages'),'add_to_variable = { cc_ui_leaves = 2 }',
        'if = { limit = { check_variable = { cc_ui_offer_count > 2 } } add_to_variable = { cc_ui_leaves = 1 } }',
        choose('cc_sheet',1,var('cc_ui_leaf',2)),choose('cc_sheet',2,var('cc_ui_leaf',3)),
        choose('cc_sheet',3,var('cc_ui_leaf','cc_recipient_page')+' add_to_variable = { cc_ui_leaf = 3 } if = { limit = { check_variable = { cc_ui_offer_count > 2 } } add_to_variable = { cc_ui_leaf = 1 } }'),
        'if = { limit = { check_variable = { cc_view_tab > 0 } } set_variable = { cc_ui_leaf = cc_delegate_page } add_to_variable = { cc_ui_leaf = 1 } set_variable = { cc_ui_leaves = cc_ui_delegate_pages } }',
        var('cc_ui_register_number','cc_register_page'),'add_to_variable = { cc_ui_register_number = 1 }',
        var('cc_ui_choice_count','cc_ui_choices^num'),page_count('cc_ui_choice_count','cc_ui_choice_pages',6,64),
        var('cc_ui_choice_max','cc_ui_choice_pages'),'subtract_from_variable = { cc_ui_choice_max = 1 }',
        'clamp_variable = { var = cc_ui_choice_page min = 0 max = cc_ui_choice_max }',
        slice_array('cc_ui_choices','cc_ui_choice_rows','cc_ui_choice_page',6),
        var('cc_ui_choice_number','cc_ui_choice_page'),'add_to_variable = { cc_ui_choice_number = 1 }']
    return block('cc_ui_paginate','\n'.join(out))

def turn_page(delta):
    if delta>0:
        programme='''if = { limit = { check_variable = { cc_sheet = 0 } } set_variable = { cc_sheet = 1 } }
else_if = { limit = { check_variable = { cc_sheet = 1 } } if = { limit = { check_variable = { cc_ui_offer_count > 2 } } set_variable = { cc_sheet = 2 } } else = { set_variable = { cc_sheet = 3 } set_variable = { cc_recipient_page = 0 } } }
else_if = { limit = { check_variable = { cc_sheet = 2 } } set_variable = { cc_sheet = 3 } set_variable = { cc_recipient_page = 0 } }
else = { add_to_variable = { cc_recipient_page = 1 } }'''
        guard='check_variable = { cc_ui_leaf < cc_ui_leaves }'
    else:
        programme='''if = { limit = { check_variable = { cc_sheet = 3 } } if = { limit = { check_variable = { cc_recipient_page > 0 } } subtract_from_variable = { cc_recipient_page = 1 } } else = { if = { limit = { check_variable = { cc_ui_offer_count > 2 } } set_variable = { cc_sheet = 2 } } else = { set_variable = { cc_sheet = 1 } } } }
else = { subtract_from_variable = { cc_sheet = 1 } }'''
        guard='check_variable = { cc_ui_leaf > 1 }'
    return f'if = {{ limit = {{ {guard} }} if = {{ limit = {{ check_variable = {{ cc_view_tab = 0 }} }} {programme} }} else = {{ add_to_variable = {{ cc_delegate_page = {delta} }} }} set_variable = {{ cc_ui_popup = 0 }} cc_ui_refresh = yes cc_touch = yes }}'
