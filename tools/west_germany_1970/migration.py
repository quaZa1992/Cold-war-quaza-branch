# IMPERIA CW — Cold War: Real state-population movement for German resettlers.
"""Bounded monthly transfers; no guest-worker stock or delayed refugee POP grant."""
from cw_lib import P
from events_lib import EXTRA_EFFECTS


def transfer(people):
    return f'{P}_transfer_uebersiedler_{people} = yes'


def effect(people):
    return f"""
# IMPERIA CW — Cold War: Validate both states before withdrawing any resident.
{P}_transfer_uebersiedler_{people} = {{
 set_temp_variable = {{ cwger_ue_arrived = 0 }}
 if = {{ limit = {{
  DDR = {{ exists = yes any_owned_state = {{ is_controlled_by = DDR state_population > {people} }} }}
  any_owned_state = {{ is_controlled_by = GER }}
 }}
  DDR = {{
   set_variable = {{ cwger_ue_reserve_before = manpower }}
   random_owned_state = {{ limit = {{ is_controlled_by = DDR state_population > {people} }} save_event_target_as = cwger_ue_origin }}
  }}
  random_owned_state = {{ limit = {{ is_controlled_by = GER }} save_event_target_as = cwger_ue_destination }}
  event_target:cwger_ue_origin = {{ add_manpower = -{people} }}
  DDR = {{
   set_temp_variable = {{ cwger_ue_reserve_gain = manpower }}
   subtract_from_temp_variable = {{ cwger_ue_reserve_gain = cwger_ue_reserve_before }}
   if = {{ limit = {{ check_variable = {{ cwger_ue_reserve_gain > 0 }} }}
    multiply_temp_variable = {{ cwger_ue_reserve_gain = -1 }}
    add_manpower = cwger_ue_reserve_gain
   }}
  }}
  event_target:cwger_ue_destination = {{ add_manpower = {people} }}
  add_to_variable = {{ cwger_uebersiedler_k = {people / 1000:g} }}
  set_temp_variable = {{ cwger_ue_arrived = {people} }}
  DDR = {{ ingame_update_setup = yes }}
  ingame_update_setup = yes
 }}
}}
"""


for _people in (600, 1500, 3000, 6000, 15000, 20000, 30000):
    EXTRA_EFFECTS.append(effect(_people))
