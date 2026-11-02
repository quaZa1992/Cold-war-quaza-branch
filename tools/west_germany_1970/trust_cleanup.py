# IMPERIA COLD WAR — One-time cleanup of retired German alignment and trust scores
"""No recurring hook, country scan or replacement score; preserve other save state."""
P = 'COLDWAR_GER_1970'
MARK = '# IMPERIA COLD WAR — Retired German trust and alignment save cleanup\n'


def files():
    clear_ddr = '\n'.join('clear_variable = '+v for v in (
        'COLDWAR_DDR_moscow_trust', 'COLDWAR_DDR_trust_delta',
        'DDR_state_trust', 'DDR_moscow_trust', 'cwddr_moscow_backing', 'cwddr_dm_backing'))
    effect = f'''{P}_retired_trust_cleanup = {{
 if = {{
  limit = {{ NOT = {{ has_country_flag = {P}_retired_trust_cleaned }} }}
  set_country_flag = {P}_retired_trust_cleaned
  if = {{
   limit = {{ original_tag = GER }}
   clear_variable = cwger_westbindung
   clear_variable = cwger_dm_ideo
   clear_variable = cwgg_g_moscow_raw
   clear_variable = cwgg_g_cwgg_rv_d_moscow
   clr_country_flag = {P}_westbindung_crisis_seen
   if = {{ limit = {{ has_country_flag = {P}_initialized }} {P}_update_modifiers = yes }}
  }}
  if = {{
   limit = {{ original_tag = DDR }}
   {clear_ddr}
   clr_country_flag = COLDWAR_DDR_ambassador_cooldown
   clr_country_flag = COLDWAR_DDR_ambassador_called
   if = {{ limit = {{ has_country_flag = DDR_state_crisis_system_enabled }} DDR_1985_update_state_crisis_values = yes }}
  }}
  force_update_dynamic_modifier = yes
 }}
}}
'''
    hook = f'''on_actions = {{
 on_startup = {{
  effect = {{
   if = {{ limit = {{ country_exists = GER }} GER = {{ {P}_retired_trust_cleanup = yes }} }}
   if = {{ limit = {{ country_exists = DDR }} DDR = {{ {P}_retired_trust_cleanup = yes }} }}
  }}
 }}
}}
'''
    return {
        f'common/scripted_effects/{P}_trust_cleanup.txt': MARK+effect,
        f'common/on_actions/{P}_trust_cleanup.txt': MARK+hook,
    }
