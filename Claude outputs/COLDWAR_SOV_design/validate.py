# IMPERIA CW — Cold War: Cold War SOV design — validate.
import sys, json, re
sys.path.insert(0, '/home/claude/sov')
import build_all
from sov_dsl import *
idx = json.load(open('/home/claude/gentools/generic_1970_focus_tree/idx_mdcw.json'))
E, T, I, MD, CATS = set(idx['effects']), set(idx['triggers']), set(idx['ideas']), set(idx['moddefs']), set(idx['cats'])
MK = set(json.load(open('/home/claude/sov/modkeys.json')).keys())
VAN_EFF = set("""add_political_power add_stability add_war_support add_ideas add_timed_idea swap_ideas remove_ideas add_power_balance_value
add_tech_bonus army_experience navy_experience air_experience add_mastery add_command_power add_manpower add_opinion_modifier add_resource
add_extra_state_shared_building_slots add_building_construction set_cosmetic_tag create_country_leader add_country_leader_trait set_politics
dismantle_faction create_wargoal add_dynamic_modifier unlock_decision_tooltip country_event random_owned_controlled_state set_country_flag
add_project_progress_ratio""".split())
SP = {"sp_space_program", "sp_aircraft_project", "sp_helicopter_project", "sp_naval_vessel_project", "sp_microchip_production", "sp_composite_production"}
errs, warns = [], []
ids = [f['id'] for f in FOCI]
dup = {x for x in ids if ids.count(x) > 1}
if dup: errs.append(f"duplicate ids {dup}")
S_ = {s['key'] for s in SECTIONS}
idset = set(ids)
byid = {f['id']: f for f in FOCI}
for f in FOCI:
    if f['sec'] not in S_: errs.append(f"{f['id']}: unknown section {f['sec']}")
    for g in f['pre']:
        for p in g:
            if p not in idset: errs.append(f"{f['id']}: prereq {p} missing")
    for m in f['mx']:
        if m not in idset: errs.append(f"{f['id']}: mx {m} missing")
        elif f['id'] not in byid[m]['mx']: errs.append(f"{f['id']}: mx {m} not symmetric")
    for e in f['eff']:
        k = e['k']
        mods = e.get('mods') or {}
        for mk in mods:
            if mk not in MK and mk not in MD: errs.append(f"{f['id']}: modifier {mk} unknown")
        if k == 'tech':
            for c in e['cats']:
                if c not in CATS: errs.append(f"{f['id']}: tech cat {c} unknown")
        if k == 'build' and e['helper'] not in E: errs.append(f"{f['id']}: helper {e['helper']} unknown")
        if k == 'law' and e['helper'] not in E: errs.append(f"{f['id']}: law helper {e['helper']} unknown")
        if k == 'setlaw' and e['idea'] not in I: errs.append(f"{f['id']}: law idea {e['idea']} unknown")
        if k == 'fac':
            if e['f'] not in I: errs.append(f"{f['id']}: faction idea {e['f']} unknown")
            if f"change_{e['f']}_opinion" not in E: errs.append(f"{f['id']}: faction helper change_{e['f']}_opinion unknown")
        if k == 'corr' and e['helper'] not in E: errs.append(f"{f['id']}: {e['helper']}")
        if k == 'tax' and e['helper'] not in E: errs.append(f"{f['id']}: {e['helper']}")
        if k == 'sp' and e['project'] not in SP: errs.append(f"{f['id']}: special project {e['project']}")
        if k == 'custom':
            for t in e['tokens']:
                if t not in E and t not in I and t not in VAN_EFF: errs.append(f"{f['id']}: custom token {t} unknown")
        if k == 'idea':
            for mk in IDEAS[e['id']]['mods']:
                if mk not in MK and mk not in MD: errs.append(f"{f['id']}: idea modifier {mk} unknown")
# MD effects relied on by kinds
for need in ["change_relative_party_popularity", "modify_treasury_effect", "modify_debt_effect", "change_influence_percentage",
             "change_domestic_influence_percentage", "change_ruling_party_effect", "mdcw_cw_add_tension", "mdcw_cw_change_alignment",
             "add_space_program_progress", "flat_productivity_change_effect", "increase_corruption", "decrease_corruption",
             "initialize_internal_faction_dynamic_modifiers", "recalculate_party", "update_party_name"]:
    if need not in E: errs.append(f"MD helper missing: {need}")
for i, t in TRIG.items():
    if f"{t}_are_in_power" not in T: errs.append(f"trigger {t}_are_in_power missing")
# reachability: every focus must have a path to a root (no cycles)
def depth(fid, seen=()):
    if fid in seen: errs.append(f"cycle at {fid}"); return 0
    f = byid[fid]
    if not f['pre']: return 0
    return 1 + max(min(depth(p, seen + (fid,)) for p in g) for g in f['pre'])
for fid in ids: depth(fid)
print("foci", len(FOCI), "ideas", len(IDEAS), "offers", len(OFFERS), "events", len(EVENTS), "decisions", len(DECISIONS), "progs", len(PROGS), "traits", len(TRAITS), "opinions", len(OPINIONS))
print("ERRORS", len(errs)); print("\n".join(errs[:80]))
import d_concept as C
errs2=[]
for iid, d in IDEAS.items():
    for mk in d['mods']:
        if mk not in MK and mk not in MD: errs2.append(f"idea {iid}: modifier {mk} unknown")
for law, _ in C.START_LAWS:
    if law not in I: errs2.append(f"start law {law} unknown")
for f_, _, _ in C.START_FACTIONS:
    if f_ not in I: errs2.append(f"start faction {f_} unknown")
name2id = {d['name']: i for i, d in IDEAS.items()}
for f in FOCI:
    for e in f['eff']:
        if e['k'] == 'idea' and e.get('swap') and e['swap'] not in name2id: errs2.append(f"{f['id']}: swap source '{e['swap']}' unknown")
print("ERRORS2", len(errs2)); print("\n".join(errs2))
# stats
neg = 0
def is_neg(e):
    k = e['k']
    if k in ('stab','ws') and e['v'] < 0: return True
    if k == 'pp' and e['v'] < 0: return True
    if k == 'fac' and e['v'] < 0: return True
    if k in ('gdp',): return True
    if k == 'coh' and e['v'] < 0: return True
    if k in ('dyn','prog') and any((v < 0) != (mk in ('bureaucracy_cost_multiplier_modifier','police_cost_multiplier_modifier','corruption_cost_factor','consumer_goods_factor','army_personnel_cost_multiplier_modifier','equipment_cost_multiplier_modifier','social_cost_multiplier_modifier','health_cost_multiplier_modifier','education_cost_multiplier_modifier','interest_rate_multiplier_modifier','training_time_factor','receiving_investment_cost_modifier','supply_consumption_factor','foreign_subversive_activites','mdcw_cw_military_programme_cost','air_accidents_factor','agriculture_workers_modifier','enemy_justify_war_goal_time','military_spending_cost_factor')) and v!=0 for mk, v in e['mods'].items()): return True
    if k == 'idea':
        d = IDEAS[e['id']]['mods']
        if any((v < 0) != (mk in ('bureaucracy_cost_multiplier_modifier','police_cost_multiplier_modifier','corruption_cost_factor','consumer_goods_factor','army_personnel_cost_multiplier_modifier','equipment_cost_multiplier_modifier','social_cost_multiplier_modifier','training_time_factor','enemy_justify_war_goal_time','military_spending_cost_factor')) and v!=0 for mk, v in d.items()): return True
    return False
choice = sum(1 for f in FOCI if f['mx'])
neg = sum(1 for f in FOCI if any(is_neg(e) for e in f['eff']))
hist = sum(1 for f in FOCI if f['hist'])
print(f"foci with any cost/downside: {neg} ({neg*100//len(FOCI)} %), with exclusive choice: {choice}, historical: {hist}")
