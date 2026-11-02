# IMPERIA COLD WAR — Once-only 1970 prestige baseline and established institutions.
# Scores are balance values, not historical statistics. AI entries are static;
# only human countries may develop, fly, earn rewards or receive leadership buffs.
BASES={'USA':100,'SOV':90,'FRA':15}


def established(p,profiles):
    if not p.get('commissioningOnly'):return []
    return [v['id'] for v in profiles if v['id']!='CUSTOM' and set(p['grants'])<=set(v.get('capabilities',[]))]


def build(c):
    sv,av,cv,block_if,effect=(c[k] for k in ['sv','av','cv','block_if','effect'])
    seed=''
    for tag,score in BASES.items():
        seed+=block_if('tag = '+tag+' NOT = { has_country_flag = cw_sr_prestige_baseline }',sv('cw_sr_historical_prestige',score)+av('cw_sr_prestige',score)+'set_country_flag = cw_sr_prestige_baseline\n')
    institutions=''
    for n,p in enumerate(c['PROGRAMMES'],1):
        tags=established(p,c['DATA']['profiles'])
        if tags:institutions+=block_if(cv(c['var'](n,'state'),'=',0)+f' NOT = {{ has_country_flag = cw_sr_p{n}_awarded }} OR = {{ '+''.join('original_tag = '+tag+' ' for tag in tags)+' }','set_country_flag = cw_sr_institution_'+str(n)+'\n')
    seed='every_country = {\n'+seed+'}\n'
    body=effect('cw_sr_seed_prestige',block_if('IMP_is_1970_scenario = yes NOT = { has_global_flag = cw_sr_prestige_baselines_seeded }',seed+'set_global_flag = cw_sr_prestige_baselines_seeded\n'))
    body+=effect('cw_sr_inherited_institutions',block_if(c['guard']()+' NOT = { has_country_flag = cw_sr_institutions_recorded }',institutions+'set_country_flag = cw_sr_institutions_recorded\n'))
    c['write']('common/scripted_effects/COLDWAR_space_race_history.txt',body)


def ranking(c):
    sv,av,cv,block_if=(c[k] for k in ['sv','av','cv','block_if'])
    ranks='cw_sr_seed_prestige = yes\n'+sv('global.cw_sr_score1',0)+sv('global.cw_sr_score2',0)+sv('global.cw_sr_score3',0)+sv('global.cw_sr_ties',0)
    for j in range(1,4):ranks+=block_if(f'has_event_target = cw_sr_rank{j}',f'clear_global_event_target = cw_sr_rank{j}\n')
    actual='is_ai = no has_country_flag = cw_sr_initialized'
    score=sv('cw_sr_ranking_score',0)+block_if(actual,sv('cw_sr_ranking_score','cw_sr_prestige'),block_if('has_country_flag = cw_sr_prestige_baseline',sv('cw_sr_ranking_score','cw_sr_historical_prestige')))
    ranks+='every_country = { clr_country_flag = cw_sr_ranked clr_country_flag = cw_sr_leader\n'+score+'}\n'
    for j in range(1,4):
        ranks+='every_country = { limit = { '+cv('cw_sr_ranking_score','>',0)+' NOT = { has_country_flag = cw_sr_ranked } }\n'+block_if(cv('cw_sr_ranking_score','>',f'global.cw_sr_score{j}'),sv(f'global.cw_sr_score{j}','cw_sr_ranking_score')+f'save_global_event_target_as = cw_sr_rank{j}\n')+'}\n'
        ranks+=block_if(f'has_event_target = cw_sr_rank{j}',f'event_target:cw_sr_rank{j} = {{ set_country_flag = cw_sr_ranked }}\n')
    ranks+='every_country = { limit = { '+cv('cw_sr_ranking_score','>',0)+' '+cv('cw_sr_ranking_score','=', 'global.cw_sr_score1')+' } '+av('global.cw_sr_ties',1)+'}\n'
    ranks+=block_if(cv('global.cw_sr_ties','=',1),'event_target:cw_sr_rank1 = { '+block_if(actual,'set_country_flag = cw_sr_leader\n')+'}\n')+'cw_sr_touch = yes\n'
    return ranks
