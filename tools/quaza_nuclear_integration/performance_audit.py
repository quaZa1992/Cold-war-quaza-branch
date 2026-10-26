# IMPERIA CW — Cold War: remove redundant uranium state scans without changing costs.
from pathlib import Path
import hashlib,json,re
from port import ROOT,AUDIT,MARKER,read,write
from adapt import blocks,block

FILES=[
'common/on_actions/COLDWAR_quaza_zzzzzz_imp_uranium_on_actions.txt',
'common/on_actions/COLDWAR_quaza_zzzzzz_imp_nuclear_programme_on_actions.txt',
'common/scripted_effects/COLDWAR_quaza_imp_uranium_effects.txt']

def replace_block(s,name,replacement):
    n=block(s,name);return s[:n['start']]+replacement+s[n['end']:]

def main():
    for rel in FILES:
        p=AUDIT/'performance_before'/rel
        if not p.exists():write(p,read(ROOT/rel))

    rel=FILES[0];s=read(ROOT/rel)
    if re.search(r'\bon_daily\s*=',s):
        n=block(s,'on_daily');s=s[:n['start']]+s[n['end']:]
    s=s.replace('# Run on every load, including saves that already initialized deposits.',
        '# New-game initialization; state slot reservations are saved with the campaign.')
    s=s.replace('on_weekly = {','''# IMPERIA CW — Cold War: saved slot reservations need no daily world scan.
 on_weekly = {''')
    write(ROOT/rel,s)

    rel=FILES[2];s=read(ROOT/rel)
    replacement='''imp_uranium_update_mines = {
 # IMPERIA CW — Cold War: one owned-state pass replaces daily and duplicate weekly scans.
 clr_country_flag = COLDWAR_uranium_has_mining_district
 every_owned_state = {
  imp_uranium_sync_mine_slots = yes
  if = {
   limit = { has_variable = imp_uranium_per_level }
   PREV = { set_country_flag = COLDWAR_uranium_has_mining_district }
   imp_uranium_count_mine_levels = yes
   imp_uranium_sync_mine_output = yes
  }
 }
 # No separate country output sum: nothing in the game reads that former cache.
 if = {
  limit = { is_ai = yes has_country_flag = COLDWAR_uranium_has_mining_district }
  imp_uranium_ai_build_mines = yes
 }
}'''
    s=replace_block(s,'imp_uranium_update_mines',replacement)
    s=s.replace('Fixed set levels also make the operation idempotent on load and daily updates.',
        'Fixed levels make new-game initialization and weekly reconciliation idempotent.')
    write(ROOT/rel,s)

    rel=FILES[1];s=read(ROOT/rel)
    replacement='''on_weekly = {
  effect = {
   # IMPERIA CW — Cold War: only a live or disrupted weapons programme needs an extra recount.
   if = {
    limit = {
     OR = {
      is_special_project_being_researched = sp:sp_nuclear_bomb
      is_special_project_being_researched = sp:sp_nuclear_warhead_program
      has_dynamic_modifier = { modifier = imp_nuclear_programme_disrupted }
     }
    }
    COLDWAR_refresh_enrichment_count = yes
    if = {
     limit = {
      OR = {
       is_special_project_being_researched = sp:sp_nuclear_bomb
       is_special_project_being_researched = sp:sp_nuclear_warhead_program
      }
      check_variable = { undamaged_enrichment_facilities < 3 }
     }
     if = {
      limit = { NOT = { has_dynamic_modifier = { modifier = imp_nuclear_programme_disrupted } } }
      add_dynamic_modifier = { modifier = imp_nuclear_programme_disrupted }
     }
    }
    else_if = {
     limit = { has_dynamic_modifier = { modifier = imp_nuclear_programme_disrupted } }
     remove_dynamic_modifier = { modifier = imp_nuclear_programme_disrupted }
    }
   }
  }
 }'''
    s=replace_block(s,'on_weekly',replacement);write(ROOT/rel,s)

    states=len(list((ROOT/'history/states').glob('*.txt')))
    report={
      'scope':'Additional uranium integration state-iterator visits; excludes native MD calculations and demand-gated AI searches.',
      'state_files':states,
      'before_full_state_passes_per_week':11,
      'before_state_visits_per_week':11*states,
      'after_full_state_passes_per_week':1,
      'after_state_visits_per_week_without_active_weapons_programmes':states,
      'reduction_in_these_state_visits_percent':round(100*(1-1/11),1),
      'conditional_work':'An extra controlled-state recount remains for countries researching nuclear weapons or removing a disruption penalty.',
      'not_a_fps_measurement':True,
      'changes':[{'file':f,'sha256':hashlib.sha256((ROOT/f).read_bytes()).hexdigest()} for f in FILES]
    }
    write(AUDIT/'performance_report.json',json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
