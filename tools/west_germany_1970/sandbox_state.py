# IMPERIA COLD WAR — Actual national policies and retirement of historical outcome proxies
from cw_lib import P

MARK='# IMPERIA COLD WAR — German two-state sandbox\n'


def files():
    # Old negotiations were initiated only by Bonn. Recover the sender without
    # granting the recipient's signature or charging preparation a second time.
    repairs='\n'.join(f'''   if = {{ limit = {{
    check_variable = {{ cwgg_verh = {n} }}
    check_variable = {{ cwgg_vertrag_{n} = 0 }}
   }}
    set_variable = {{ cwgg_tr_sender = 1 }}
    if = {{ limit = {{ check_variable = {{ cwgg_verh_prog > 99 }} }}
     set_variable = {{ cwgg_verh_prog = 100 }}
     set_variable = {{ cwgg_tr_ready = {n} }}
     clr_country_flag = cwgg_tr_brd_dialogue_open
    }}
   }}''' for n in range(1,10))
    # The dossier reads an existing policy, never a date-driven collapse score.
    triggers=f'''{P}_border_open = {{
 country_exists = DDR
 DDR = {{
  has_country_flag = COLDWAR_DDR_initialized
  COLDWAR_DDR_ladder_border_active = no
 }}
}}
{P}_ddr_security_measures = {{
 country_exists = DDR
 DDR = {{ OR = {{
  has_country_flag = cwgg_east_cd_stasi_sweep
  has_idea = COLDWAR_DDR_border_the_iron_border
 }} }}
}}
'''
    effects=f'''{P}_sandbox_migrate = {{
 if = {{
  limit = {{ NOT = {{ has_country_flag = {P}_sandbox_installed }} }}
  set_country_flag = {P}_sandbox_installed
  if = {{ limit = {{ original_tag = GER }}
   clr_global_flag = {P}_honecker_era
   clr_global_flag = {P}_moscow_coup_rolled
   clr_global_flag = {P}_moscow_coup_succeeded
   clr_global_flag = {P}_wall_open
   set_variable = {{ cwgg_brd_order_ready = 0 }}
   set_variable = {{ cwgg_ddr_order_ready = 0 }}
  }}
  if = {{ limit = {{ original_tag = DDR }}
   clear_variable = cwddr_leader
   clear_variable = cwddr_wende_stage
   remove_ideas = {P}_idea_ddr_crackdown
   remove_ideas = {P}_idea_ddr_round_table
  }}
 }}
 # IMPERIA COLD WAR — Repair pre-consent negotiations even if the first migration already ran.
 if = {{ limit = {{ IMP_is_1970_scenario = yes NOT = {{ has_country_flag = {P}_transactions_v2_installed }} }}
  set_country_flag = {P}_transactions_v2_installed
  if = {{ limit = {{ original_tag = GER }}
   if = {{ limit = {{ country_exists = DDR check_variable = {{ cwgg_tr_sender = 0 }} check_variable = {{ cwgg_tr_pending = 0 }} }}
{repairs}
   }}
   if = {{ limit = {{ NOT = {{ has_war_with = DDR }} }} {P}_rv_clear_armistice = yes }}
  }}
  if = {{ limit = {{ original_tag = DDR NOT = {{ has_war_with = GER }} }} clr_country_flag = cwgg_armistice_request }}
 }}
}}
'''
    hook=f'''on_actions = {{
 on_startup = {{ effect = {{
  if = {{ limit = {{ country_exists = GER }} GER = {{ {P}_sandbox_migrate = yes }} }}
  if = {{ limit = {{ country_exists = DDR }} DDR = {{ {P}_sandbox_migrate = yes }} }}
 }} }}
}}
'''
    return {
        f'common/scripted_triggers/{P}_sandbox.txt':MARK+triggers,
        f'common/scripted_effects/{P}_sandbox.txt':MARK+effects,
        f'common/on_actions/{P}_sandbox.txt':MARK+hook,
    }
