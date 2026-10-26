# IMPERIA CW — Cold War: Guest Worker Administration
"""On-demand foreign-community reading and a snapshot-safe outreach dialog."""
def runtime():
    text='''
# IMPERIA CW — Cold War: read only the four displayed hosts, on explicit UI interaction.
mdcw_gw_ministry_host_page = {
 clamp_variable = { var = gw_ui_host_page min = 0 }
 set_variable = { gw_ui_host_offset = gw_ui_host_page } multiply_variable = { gw_ui_host_offset = 4 }
 if = { limit = { NOT = { check_variable = { gw_ui_host_offset < gw_hosts^num } } }
  set_variable = { gw_ui_host_page = 0 } set_variable = { gw_ui_host_offset = 0 }
 }
 set_variable = { gw_ui_host_next = gw_ui_host_offset } add_to_variable = { gw_ui_host_next = 4 }
 set_variable = { gw_ui_host_page_display = gw_ui_host_page } add_to_variable = { gw_ui_host_page_display = 1 }
'''
    for row in range(1,5):
        text+=f'''
 set_variable = {{ gw_host{row}_origin = -1 }} set_variable = {{ gw_host{row}_k = 0 }}
 set_temp_variable = {{ gw_ui_host_i = gw_ui_host_offset }} add_to_temp_variable = {{ gw_ui_host_i = {row-1} }}
 if = {{ limit = {{ check_variable = {{ gw_ui_host_i < gw_hosts^num }} }}
  set_variable = {{ gw_host{row}_origin = gw_hosts^gw_ui_host_i }}
  var:gw_host{row}_origin = {{
   if = {{ limit = {{ exists = yes }}
    set_temp_variable = {{ gw_lookup_origin = ROOT.id }} mdcw_gw_find_origin = yes
    if = {{ limit = {{ check_variable = {{ gw_index > -1 }} }}
     ROOT = {{ set_variable = {{ gw_host{row}_k = PREV.gw_stock^PREV.gw_index }} }}
    }}
   }}
  }}
 }}
 set_variable = {{ gw_host{row}_people = gw_host{row}_k }}
 clamp_variable = {{ var = gw_host{row}_people min = 0 max = 2000 }} multiply_variable = {{ gw_host{row}_people = 1000 }}
 set_variable = {{ gw_host{row}_m = gw_host{row}_k }} divide_variable = {{ gw_host{row}_m = 1000 }}
'''
    text+='''
 if = { limit = { NOT = { has_variable = gw_ui_host } } set_variable = { gw_ui_host = -1 } }
 mdcw_gw_ministry_host_selection = yes
 if = { limit = { NOT = { check_variable = { gw_ui_host_stock_k > 0 } } check_variable = { gw_host1_k > 0 } }
  set_variable = { gw_ui_host = gw_host1_origin } mdcw_gw_ministry_host_selection = yes
 }
 add_to_variable = { gw_ui_dirty = 1 }
}
mdcw_gw_ministry_host_selection = {
 set_variable = { gw_ui_host_stock_k = 0 }
 set_variable = { gw_ui_host_registered_k = 0 }
 set_variable = { gw_ui_host_housed_k = 0 }
 set_variable = { gw_ui_host_protected_k = 0 }
 set_variable = { gw_ui_return_rate = 0 }
 set_variable = { gw_ui_return_last = 0 }
 set_variable = { gw_ui_return_expected = 0 }
 if = { limit = { has_variable = gw_ui_host check_variable = { gw_ui_host > -1 } }
  var:gw_ui_host = {
   if = { limit = { exists = yes }
    set_temp_variable = { gw_lookup_origin = ROOT.id } mdcw_gw_find_origin = yes
    if = { limit = { check_variable = { gw_index > -1 } }
     set_temp_variable = { gw_mi = gw_index }
     set_temp_variable = { gw_mo = ROOT.id }
     mdcw_dp_return_rate = yes
     ROOT = {
      set_variable = { gw_ui_host_stock_k = PREV.gw_stock^PREV.gw_index }
      set_variable = { gw_ui_host_registered_k = PREV.gw_registered^PREV.gw_index }
      set_variable = { gw_ui_host_housed_k = PREV.gw_housed^PREV.gw_index }
      set_variable = { gw_ui_host_protected_k = PREV.gw_protected^PREV.gw_index }
      set_variable = { gw_ui_return_rate = PREV.gw_rate }
      set_variable = { gw_ui_return_last = PREV.gw_return_last^PREV.gw_index }
      set_variable = { gw_ui_return_expected = PREV.gw_return_basis^PREV.gw_index }
      multiply_variable = { gw_ui_return_expected = gw_ui_return_rate }
      divide_variable = { gw_ui_return_expected = 100 }
     }
    }
   }
  }
 }
 set_variable = { gw_ui_host_people = gw_ui_host_stock_k }
 clamp_variable = { var = gw_ui_host_people min = 0 max = 2000 } multiply_variable = { gw_ui_host_people = 1000 }
 set_variable = { gw_ui_host_m = gw_ui_host_stock_k } divide_variable = { gw_ui_host_m = 1000 }
'''
    for field in ('registered','housed','protected'):
        text+=f'''
 set_variable = {{ gw_ui_{field}_ratio = 0 }}
 if = {{ limit = {{ check_variable = {{ gw_ui_host_stock_k > 0 }} }}
  set_variable = {{ gw_ui_{field}_ratio = gw_ui_host_{field}_k }}
  divide_variable = {{ gw_ui_{field}_ratio = gw_ui_host_stock_k }}
 }}
 set_variable = {{ gw_ui_{field}_frame = gw_ui_{field}_ratio }} multiply_variable = {{ gw_ui_{field}_frame = 10 }}
 round_variable = gw_ui_{field}_frame add_to_variable = {{ gw_ui_{field}_frame = 1 }}
'''
    text+='''
 add_to_variable = { gw_ui_dirty = 1 }
}

# IMPERIA CW — Cold War: outreach uses the same native prices and eligibility as the existing decision.
mdcw_gw_ministry_confirm_outreach = {
 if = { limit = {
  has_country_flag = gw_dialog_valid has_country_flag = gw_dialog_window
  NOT = { check_variable = { political_power < 75 } } NOT = { check_variable = { treasury < 0.5 } }
  var:gw_dialog_host = { mdcw_gw_outreach_target_valid = yes }
 }
  add_political_power = -75 subtract_from_variable = { treasury = 0.5 }
  var:gw_dialog_host = {
   set_temp_variable = { gw_lookup_origin = ROOT.id } mdcw_gw_find_origin = yes
   set_variable = { gw_outreach^gw_index = 1 }
   add_to_variable = { gw_ui_dirty = 1 }
   country_event = { id = mdcw_diaspora.80 days = 180 }
  }
  ingame_update_setup = yes
 }
 clr_country_flag = gw_dialog_valid clr_country_flag = gw_dialog_window
}
'''
    return text
