# IMPERIA CW — Cold War: read-only runtime audit with reproducible report/hash refresh.
import hashlib,json,re
from port import ROOT,AUDIT,read,write
from adapt import block,blocks
from test_integration import Model,pdx

def part(text,name):
    n=block(text,name)
    return text[n['open']:n['close']]

def count(text,name):
    def walk(nodes):
        for n in nodes:
            yield n
            yield from walk(n['children'])
    return sum(n['name']==name for n in walk(blocks(text)))

def main():
    manifest=json.loads(read(AUDIT/'manifest.json'))
    existing={r['file'] for r in manifest['runtime_files']}
    additions=['common/scripted_effects/COLDWAR_nuclear_development_budget.txt',
               'localisation/english/replace/replaced_from_special_projects_l_english.yml',
               'interface/COLDWAR_nuclear_project_icons.gfx']
    additions.extend(p.relative_to(AUDIT/'coverage_before').as_posix() for p in (AUDIT/'coverage_before').rglob('*') if p.is_file() and p.relative_to(AUDIT/'coverage_before').parts[0] in ['common','interface','events','localisation','history','gfx'])
    additions.extend(p.relative_to(AUDIT/'geology_before').as_posix() for p in (AUDIT/'geology_before').rglob('*') if p.is_file() and p.relative_to(AUDIT/'geology_before').parts[0] in ['common','interface','events','localisation','history','gfx'])
    for rel in additions:
        if rel not in existing:
            before=AUDIT/'performance_before'/rel
            if not before.exists():before=AUDIT/'coverage_before'/rel
            if not before.exists():before=AUDIT/'geology_before'/rel
            manifest['runtime_files'].append({'file':rel,'before_sha256':hashlib.sha256(before.read_bytes()).hexdigest() if before.exists() else None,'source_sha256':None})
            existing.add(rel)
    for entry in manifest['runtime_files']:
        entry['sha256']=hashlib.sha256((ROOT/entry['file']).read_bytes()).hexdigest()
    manifest['runtime_files'].sort(key=lambda r:r['file'])
    write(AUDIT/'manifest.json',json.dumps(manifest,indent=2))

    effects='common/scripted_effects/COLDWAR_quaza_imp_uranium_effects.txt'
    hooks='common/on_actions/COLDWAR_quaza_zzzzzz_imp_uranium_on_actions.txt'
    nuclear='common/on_actions/COLDWAR_quaza_zzzzzz_imp_nuclear_programme_on_actions.txt'
    old_hooks=read(AUDIT/'performance_before'/hooks)
    old_mines=part(read(AUDIT/'performance_before'/effects),'imp_uranium_update_mines')
    new_mines=part(read(ROOT/effects),'imp_uranium_update_mines')
    old_daily=count(part(old_hooks,'on_daily'),'every_owned_state')*7
    old_weekly=count(old_mines,'every_owned_state')+count(old_mines,'every_collection')
    old_nuclear=1 # The saved weekly hook unconditionally called its controlled-state recount.
    old_weekly_hook=part(read(AUDIT/'performance_before'/nuclear),'on_weekly')
    assert part(old_weekly_hook,'effect').lstrip().startswith('# IMPERIA CW')
    assert part(old_weekly_hook,'effect').find('COLDWAR_refresh_enrichment_count')<part(old_weekly_hook,'effect').find('if =')
    new_weekly=count(new_mines,'every_owned_state')
    old_passes=old_daily+old_weekly+old_nuclear
    state_files=len(list((ROOT/'history/states').glob('*.txt')))
    report={
      'method':'Structural iterator count from saved before/runtime scripts, not elapsed-time profiling.',
      'scope':'Additional uranium integration state scans, excluding native MD building/energy accounting and demand-gated AI searches.',
      'state_files':state_files,
      'before_equivalent_full_state_passes_per_week':old_passes,
      'before_breakdown':{'daily_slot_scans':old_daily,'weekly_mine_and_unused_cache_scans':old_weekly,'unconditional_enrichment_recount':old_nuclear},
      'after_unconditional_full_state_passes_per_week':new_weekly,
      'map_size_upper_bound_before':old_passes*state_files,
      'map_size_upper_bound_after_without_active_or_disrupted_weapons_programmes':new_weekly*state_files,
      'reduction_in_unconditional_iterator_passes_percent':round(100*(1-new_weekly/old_passes),1),
      'conditional_work':'Controlled-state recount only for active/disrupted weapons programmes. AI mine search requires a deposit country, economic eligibility and a 90-day construction cooldown. Nuclear AI policy/construction runs monthly.',
      'timing':'Mine reconciliation weekly, uranium market price once globally per month, research budgets in the existing economic refresh; no additional daily or hourly finance loops.',
      'caveat':'Map-size counts are upper bounds, not measured visits; ownership/control can exclude states. This is not a total game-load or FPS improvement percentage.',
      'files':[{'file':rel,'sha256':hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()} for rel in [effects,hooks,nuclear]]
    }
    write(AUDIT/'performance_report.json',json.dumps(report,indent=2))

    buildings=read(ROOT/'common/buildings/00_buildings.txt')
    mine=pdx.parse(part(buildings,'uranium_mine'))[0]
    enrichment=pdx.parse(part(buildings,'enrichment_facility'))[0]
    uranium=read(ROOT/effects)
    money=read(ROOT/'common/scripted_effects/00_money_system.txt')
    energy=read(ROOT/'common/scripted_effects/!_energy_effects.txt')
    investment=read(ROOT/'common/scripted_effects/99_investment_scripted_effects.txt')
    projects={}
    for rel,names in {
      'common/special_projects/projects/nuclear_projects.txt':['sp_nuclear_energy','sp_thorium_nuclear_fuel','sp_nuclear_bomb','sp_nuclear_warhead_program'],
      'common/special_projects/projects/naval_projects.txt':['sp_medium_naval_nuclear_engines','sp_nuclear_torpedoes']}.items():
        source=read(ROOT/rel)
        for name in names:
            resource=pdx.parse(part(part(part(source,name),'resource_cost'),'resources'))[0]
            projects[name]={'file':rel,'resources':{k:int(v) for k,op,v,line in resource}}
    base_rates={}
    for name in ['sp:sp_nuclear_bomb','sp:sp_nuclear_warhead_program']:
        m=Model();m.vars.update(gdp_per_capita=36,inflation_multiplier=1);m.projects={name}
        m.call('COLDWAR_calculate_nuclear_development_budget')
        base_rates[name]={'base_weekly_billion':m.vars['COLDWAR_nuclear_development_weekly_base'],'weekly_at_gdpc_36k_inflation_1':m.vars['COLDWAR_nuclear_development_weekly_cost']}
    costs={
      'unit':'MD monetary values in billions; IC for native construction costs; resource units are native production/research requirements.',
      'starting_production':f'Zero raw uranium production in every state; {len(json.loads(read(AUDIT/"coldwar_balance.json"))["deposits"])} surveyed districts enable paid mine development.',
      'mine':{
        'construction_ic':int(pdx.get(mine,'base_cost')),
        'extra_ic_per_existing_level':int(pdx.get(mine,'per_level_extra_cost')),
        'international_investment_billion_per_level':float(re.search(r'global.build_cost_array\^15\s*=\s*([\d.]+)',investment)[1]),
        'base_weekly_infrastructure_billion_per_level':float(re.search(r'multiply\s*=\s*([\d.]+)',part(money,'uranium_mine_infra_expense'))[1]),
        'upkeep_adjustment':'Infrastructure cost modifier, common_money_modifier (GDP/c and inflation) and native population-size scaling.',
        'base_power_gw':float(re.search(r'multiply\s*=\s*([\d.]+)',part(energy,'energy_use_uranium_mine_total_display_var'))[1]),
        'working_output':'3–12 raw units/level by deposit; damaged levels produce no additional uranium.'},
      'enrichment':{'construction_ic':int(pdx.get(enrichment,'base_cost')),
        'uranium_required_per_facility':int(re.search(r'@imp_uranium_per_enrichment_facility\s*=\s*(\d+)',uranium)[1]),
        'shortage_output':'Proportional, with zero new fuel output when uranium supply is zero.',
        'separate_new_cash_upkeep':False,
        'cash_note':'No additional standalone enrichment-facility operating fee was introduced; existing native reactor upkeep remains in infrastructure spending.'},
      'special_project_resources':projects,
      'weapons_research_budgets':{'rates':base_rates,
        'weekly_formula':'weekly_base × clamp(GDP/c_in_thousands / 36, 0.4, 1.2) × inflation_multiplier',
        'active_condition':'Actual special project being researched; both add if active together; no arsenal-size exemption.',
        'lifecycle':'Calculated on native economic refresh; completion/cancellation resets the rate, disruption does not waive costs.',
        'accounting_path':['COLDWAR_calculate_nuclear_development_budget','update_military_rate -> defence_gain','update_display -> display_expense -> treasury_rate','MD_on_actions on_weekly -> treasury'],
        'display':['Defence Spending breakdown','Atomic bomb and warhead project descriptions'],
        'refresh_safety':'Rate calculation overwrites its result and never directly modifies treasury.'},
      'raid_policy':'50/50 raids block AI in both available and launchable.'
    }
    write(AUDIT/'cost_audit.json',json.dumps(costs,indent=2,ensure_ascii=False))
    engine=read(ROOT/'tools/quaza_nuclear_integration/runtime/logs/error.log')
    names={PathLike(entry['file']) for entry in manifest['runtime_files']}
    diagnostic=[line for line in engine.splitlines() if any(name in line for name in names) and 'Missing icon shine' not in line]
    write(AUDIT/'engine_modified_files_errors.json',json.dumps({'runtime_files':len(names),'diagnostics':diagnostic,
          'scope':'Filename scan of the last saved engine log only; the interrupted run predates the latest geology and project-card changes. This is not native verification of the current build.'},indent=2))
    assert not diagnostic,diagnostic[:10]
    print(json.dumps({'runtime_files':len(manifest['runtime_files']),'cost_report':'cost_audit.json','performance_report':'performance_report.json','modified_file_engine_diagnostics':len(diagnostic)}))

def PathLike(rel):
    return rel.replace('\\','/').split('/')[-1]

if __name__=='__main__':main()
