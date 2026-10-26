# IMPERIA CW — Cold War: cyprus 1970 — north.
"""Historical Turkish Cypriot roster, latent until NCY actually exists.

No release, border transfer, intervention, OOB creation or recognition is owned
here. Country formation and international choices remain with the future adapter.
"""
import json
from politics import IDEOLOGIES

N='COLDWAR_NCY_1970_'

POLITICIANS=[
 ('kucuk','Fazıl Küçük','1970.1.1','1984.1.15','civic','Communal leader and vice-president before Denktaş\'s 1973 accession.'),
 ('denktas','Rauf Denktaş','1970.1.1','2000.1.1','diplomat','Communal representative; head of the Turkish Cypriot administration from 28 February 1973. The presidency is distinct from the UBP premiership.'),
 ('berberoglu','Ahmet Mithat Berberoğlu','1970.12.27','2000.1.1','civic','CTP founder and first chair, 1970–1976.'),
 ('ozgur','Özker Özgür','1975.1.1','2000.1.1','civic','Founding assembly member in 1975 and CTP chair from 1976 to 1996.'),
 ('durduran','Alpay Durduran','1975.1.1','2000.1.1','civic','Founding assembly member and founding TKP chair, 1976–1983.'),
 ('bozkurt','İsmail Bozkurt','1970.1.1','2000.1.1','diplomat','Turkish Cypriot parliamentarian and later TKP chair, 1983–1987.'),
 ('akinci','Mustafa Akıncı','1976.1.1','2000.1.1','civic','Nicosia municipal politician from 1976 and TKP chair from 1987. This is not the later TDP or presidential office.'),
 ('konuk','Nejat Konuk','1975.1.1','2000.1.1','administrator','Early head of government and UBP chair; subsequently associated with the Democratic People\'s Party. He is not substituted for the president.'),
 ('orek','Osman Örek','1970.1.1','1999.3.24','administrator','Former Republic of Cyprus defence minister, senior Turkish Cypriot administrator and 1978 prime minister.'),
 ('cagatay','Mustafa Çağatay','1970.7.5','1989.4.3','administrator','Turkish Cypriot parliamentarian from July 1970 and later head of government, 1978–1983.'),
 ('eroglu','Derviş Eroğlu','1976.1.1','2000.1.1','administrator','UBP parliamentarian from 1976, later party chair and prime minister. His Cold War cabinet role is distinct from his later presidency.'),
]

# First-of-month boundaries are explicit availability approximations for the
# secondary-source TMT handover months; they are not claimed appointment days.
TMT=[('kazandag','Rüştü Kazandağ','1970.1.1','1970.8.1'),
     ('eyupoglu','Süleyman Eyüpoğlu','1970.8.1','1972.7.1'),
     ('eryilmaz','Arif Eryılmaz','1972.7.1','1974.9.1'),
     ('basar','Çetin Başar','1974.9.1','1976.8.1')]


def generate_north(c):
    block,cond=c.block,c.cond
    def flag(k):return 'has_country_flag = '+N+k
    def setflag(k):return 'set_country_flag = '+N+k
    effects={};chars=[];roster=[]
    assets=json.loads((c.HERE/'north/assets.json').read_text(encoding='utf-8'))['assets']
    def pic(key):return assets[key]['portrait']
    def identifier(key):return N+key
    context='original_tag = NCY\nexists = yes\nIMP_is_1970_scenario = yes'
    def register(key,body):effects[identifier(key)]=body
    def make_advisor(key,name,start,end,trait,note,military=False,skill=2):
        c.loc(identifier(key),name);c.loc(identifier(key)+'_desc',note)
        body='name = '+identifier(key)+'\n'+block('portraits',block('army' if military else 'civilian',
            'large = "'+pic(key)+'"\nsmall = "'+assets[key]['small']+'"'))
        if military:
            body+='\n'+block('corps_commander',f'skill = {skill}\nattack_skill = 2\ndefense_skill = 3\nplanning_skill = 3\nlogistics_skill = 2')
        allowed=context+'\ndate > '+previous_day(start)+'\ndate < '+end
        if key in {x[0] for x in TMT}:allowed+='\ndate < 1976.8.1'
        if not military:allowed+='\nNOT = { has_country_leader = { name = "'+name+'" ruling_only = yes } }'
        body+='\n'+block('advisor','slot = '+('army_chief' if military else 'political_advisor')+'\nidea_token = '+identifier(key)+
            '\ntraits = { '+trait+' }\ncost = '+('100' if military else '75')+'\n'+
            block('allowed','original_tag = NCY\nIMP_is_1970_scenario = yes')+'\n'+block('available',allowed)+'\nai_will_do = { factor = 1 }')
        chars.append(block(identifier(key),body))
        roster.append({'id':identifier(key),'key':key,'name':name,'available_from':start,'until':end,
            'kind':'commander' if military else 'politician','portrait':pic(key),'small':assets[key]['small'],
            'portrait_status':assets[key]['status'],'note':note})
    for key,name,start,end,trait,note in POLITICIANS:
        make_advisor(key,name,start,end,identifier(trait),note)
    for key,name,start,end in TMT:
        make_advisor(key,name,start,end,'army_chief_organizational_1',
            'TMT Bayraktar: a Turkish officer commanding local Turkish Cypriot forces. Approximate availability follows a reported handover month; it is not an appointment-day claim. Not a GKK post or an invasion-corps command.',True)
    gkk=json.loads((c.HERE/'north/references/gkk_metadata.json').read_text(encoding='utf-8'))
    for p in sorted(gkk,key=lambda x:x['key']):
        year=int(p['key'].split('_')[-1]);end=year+2
        start='1976.8.1' if year==1976 else str(year)+'.1.1'
        make_advisor(p['key'],p['display_name'],start,'2000.1.1','army_chief_organizational_1',
            'Historical GKK commander, '+str(year)+'–'+str(end)+'. Available from the documented year; later recruitment does not claim a January appointment. The GKK was established on 1 August 1976. Strategic skills are balance values.',True,3 if year==1978 else 2)
    c.write('common/characters/COLDWAR_NCY_1970_characters.txt',c.HEADER+block('characters','\n\n'.join(chars))+'\n')
    traits={'civic':('Civic Organizer','political_power_factor = 0.03'),
            'diplomat':('Communal Negotiator','foreign_influence_defense_modifier = 0.03'),
            'administrator':('Experienced Administrator','bureaucracy_cost_multiplier_modifier = -0.03')}
    for key,(name,mods) in traits.items():c.loc(identifier(key),name)
    c.write('common/country_leader/COLDWAR_NCY_1970_traits.txt',c.HEADER+block('leader_traits','\n'.join(block(identifier(k),'random = no\n'+v[1]) for k,v in traits.items()))+'\n')
    # The named political roster is available as advisors. MD's country leader
    # dispatch is separate, matching the existing native political system.
    def create(key,ideology):
        name=next(x['name'] for x in roster if x['key']==key)
        return 'create_country_leader = { name = "'+name+'" picture = "'+pic(key)+'" expire = "2000.1.1" ideology = '+ideology+' }'
    default={
        1:cond('date < 1973.2.28',create('kucuk','conservatism'),create('denktas','conservatism')),
        3:cond('date < 1970.12.27','create_country_leader = { name = "Democratic Opposition Council" picture = "'+pic('generic')+'" ideology = socialism }',
            cond('date < 1976.10.31',create('berberoglu','socialism'),create('ozgur','socialism'))),
        18:cond('date < 1976.3.18','create_country_leader = { name = "Social-Democratic Independents" picture = "'+pic('generic')+'" ideology = neutral_Social }',
            cond('date < 1983.11.6',create('durduran','neutral_Social'),cond('date < 1987.1.1',create('bozkurt','neutral_Social'),create('akinci','neutral_Social')))),
    }
    epoch=cond('check_variable = { ruling_party = 1 }',cond('date < 1973.2.28',
        'set_variable = { '+N+'current_epoch = 1 }','set_variable = { '+N+'current_epoch = 2 }'))
    epoch+='\n'+cond('check_variable = { ruling_party = 3 }',cond('date < 1970.12.27',
        'set_variable = { '+N+'current_epoch = 1 }',cond('date < 1976.10.31',
        'set_variable = { '+N+'current_epoch = 2 }','set_variable = { '+N+'current_epoch = 3 }')))
    epoch+='\n'+cond('check_variable = { ruling_party = 18 }',cond('date < 1976.3.18',
        'set_variable = { '+N+'current_epoch = 1 }',cond('date < 1983.11.6',
        'set_variable = { '+N+'current_epoch = 2 }',cond('date < 1987.1.1',
        'set_variable = { '+N+'current_epoch = 3 }','set_variable = { '+N+'current_epoch = 4 }'))))
    register('update_leadership_epoch','set_variable = { '+N+'current_epoch = 0 }\n'+epoch)
    leader=['update_set_politics = yes',identifier('update_leadership_epoch')+' = yes']
    for idx,ideo in enumerate(IDEOLOGIES):
        payload=default.get(idx,'create_country_leader = { name = "Turkish Cypriot National Administration" picture = "'+pic('generic')+'" expire = "2000.1.1" ideology = '+ideo+' }')
        leader.append(block('if' if idx==0 else 'else_if','limit = { check_variable = { ruling_party = '+str(idx)+' } }\n'+payload))
    leader += ['set_variable = { '+N+'leader_party = ruling_party }',
               'set_variable = { '+N+'leader_epoch = '+N+'current_epoch }',setflag('leader_roster_v1')]
    register('set_leader',cond(context,'\n'.join(leader)))
    recruit=[]
    for p in roster:
        ready='date > '+previous_day(p['available_from'])+'\ndate < '+p['until']+'\nNOT = { '+flag('recruited_'+p['key'])+' }'
        # Retain an already recruited person's military career for human roleplay;
        # the game does not retrospectively force a cabinet or army appointment.
        if p['key'] in {x[0] for x in TMT}:ready+='\ndate < 1976.8.1'
        recruit.append(cond(ready,'recruit_character = '+p['id']+'\n'+setflag('recruited_'+p['key'])))
    register('refresh_roster',cond(context,'\n'.join(recruit)))
    setup=[setflag('initialized'),setflag('human_seat_reserved'),
        # A direct preview slot does not mean that the full MD politics preset was seeded.
        cond('OR = { NOT = { has_variable = ruling_party } NOT = { has_country_flag = IMP_1970_historical_politics } }','IMP_1970_profile_democratic_conservative = yes'),
        'retire_character = NCY_sezai_ozturk','retire_character = NCY_secme_akin',
        identifier('refresh_roster')+' = yes',identifier('set_leader')+' = yes']
    # Retirement is conditional so an unrecruited modern character is not acted on.
    setup=[cond('has_character = '+line.split(' = ')[1],line) if line.startswith('retire_character') else line for line in setup]
    register('initialize',cond(context+'\nNOT = { '+flag('initialized')+' }','\n'.join(setup)))
    register('daily_tick',identifier('initialize')+' = yes\n'+identifier('refresh_roster')+' = yes\n'+identifier('update_leadership_epoch')+' = yes\n'+
        cond('OR = { NOT = { '+flag('leader_roster_v1')+' } NOT = { check_variable = { '+N+'leader_party = ruling_party } } }',identifier('set_leader')+' = yes'))
    # Calendar turnover offers a human action; it never forces an election,
    # replaces a human's incumbent or changes the ruling political slot.
    ready=context+'\nis_ai = no\nNOT = { check_variable = { '+N+'leader_epoch = '+N+'current_epoch } }'
    register('select_contemporary_leadership',cond(ready,identifier('set_leader')+' = yes'))
    category=identifier('political_dossier');decision=identifier('leadership_review')
    c.loc(category,'Turkish Cypriot Administration')
    c.loc(category+'_desc','Manage the local leadership without changing party popularity or forcing a constitutional settlement.')
    c.loc(decision,'Convene a Leadership Review')
    c.loc(decision+'_desc','A new historical leadership generation is available for the current political current. Adopt its contemporary representative, or retain the incumbent for roleplay. This does not change the governing party, call an election or grant any reward.')
    c.write('common/decisions/categories/COLDWAR_NCY_1970_categories.txt',c.HEADER+block(category,
        'icon = GFX_decision_category_generic_foreign_policy\nallowed = { original_tag = NCY IMP_is_1970_scenario = yes }\n'+block('visible',context+'\nis_ai = no'))+'\n')
    c.write('common/decisions/COLDWAR_NCY_1970_decisions.txt',c.HEADER+block(category,block(decision,
        block('allowed','original_tag = NCY IMP_is_1970_scenario = yes')+'\n'+block('visible',ready)+'\n'+
        block('available',ready)+'\ncost = 0\nfire_only_once = no\n'+block('complete_effect',identifier('select_contemporary_leadership')+' = yes')+'\nai_will_do = { factor = 0 }'))+'\n')
    c.write('common/scripted_effects/COLDWAR_NCY_1970_effects.txt',c.HEADER+'\n\n'.join(block(k,v) for k,v in effects.items())+'\n')
    daily=cond(context,identifier('daily_tick')+' = yes')
    startup=block('NCY',cond('exists = yes\nIMP_is_1970_scenario = yes',identifier('daily_tick')+' = yes'))
    c.write('common/on_actions/COLDWAR_NCY_1970_on_actions.txt',c.HEADER+block('on_actions',
        block('on_startup',block('effect',startup))+'\n'+block('on_daily',block('effect',daily)))+'\n')
    c.write('tools/cyprus_1970/north/roster.json',json.dumps(roster,indent=2,ensure_ascii=False)+'\n')
    return {'people':len(roster),'scripted_effects':len(effects),'decisions':1,
            'auto_formation':False,'restored_portraits':23,'official_GKK_photo_references':8,
            'existing_portraits':0,'placeholder_portraits':0}


def previous_day(value):
    from datetime import date,timedelta
    y,m,d=map(int,value.split('.'));v=date(y,m,d)-timedelta(days=1)
    return f'{v.year}.{v.month}.{v.day}'
