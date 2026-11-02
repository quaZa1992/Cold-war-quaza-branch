# IMPERIA COLD WAR — Brazil party-formation material previews and decision access.
from common import *

# Existing native organization effects grant 0.01 relative party and outlook
# support. These display helpers never register organizations or appoint leaders.
FORMS={
    'pds':(1,'democratic','party_pds_registered','party_1_2'),
    'pmdb':(2,'democratic','party_pmdb_registered','party_2_2'),
    'historic_ptb':(3,'democratic','party_historic_ptb_restored','party_3_1'),
    'ptb_late':(3,'democratic','party_ptb_late_registered','party_3_2'),
    'pdt':(3,'democratic','party_pdt_registered','party_3_3'),
    'pt':(3,'democratic','party_pt_registered','party_3_4'),
    'pfl':(1,'democratic','party_pfl_registered','party_1_3'),
    'psdb':(2,'democratic','party_psdb_registered','party_2_3'),
    'pcb':(4,'communism','party_pcb_legalized',None),
    'pcdob':(19,'neutrality','party_pcdob_legalized',None),
    'prn':(20,'nationalist','party_prn_registered','party_20_2'),
}
CP=P+'1970_'

def new_organisation(org,body):
    return iff(block('custom_trigger_tooltip','tooltip = '+CP+'not_organised_'+org+'_tt',neg('has_country_flag = '+CP+FORMS[org][2])),body)

def polish_politics(pack):
    effects=[];loc=pack['loc'];files=pack['files']
    path='common/decisions/COLDWAR_BRA_1970_politics.txt';decisions=files[path]
    for org,(slot,outlook,receipt,name_key) in FORMS.items():
        name='$'+CP+name_key+'$' if name_key else ('The Brazilian Communist Party' if org=='pcb' else 'The Communist Party of Brazil')
        loc[CP+'not_organised_'+org+'_tt']=name+' has not yet been organised.'
        loc[CP+'not_organised_'+org+'_tt_NOT']=name+' has already been organised.'
        material=['set_temp_variable = { party_index = '+str(slot)+' }','set_temp_variable = { party_popularity_increase = 0.01 }','custom_effect_tooltip = TT_ADD_RELATIVE_PARTY_POPULARITY',block('add_popularity','ideology = '+outlook,'popularity = 0.01')]
        if org not in ('pcb','pcdob'):material.append('unlock_decision_tooltip = '+CP+'congress_'+org)
        effects.append(block(CP+'preview_register_'+org,new_organisation(org,'\n'.join(material))))
        old=CP+'form_'+org+' = yes';assert decisions.count(old)==1,org
        decisions=decisions.replace(old,block('effect_tooltip',CP+'preview_register_'+org+' = yes')+'\n'+block('hidden_effect',old),1)
    for ix in (0,1):
        access=[]
        for org in ('pds','pmdb','historic_ptb','ptb_late','pdt','pt')+(('pcb','pcdob') if ix==0 else ()):
            access.append(new_organisation(org,'unlock_decision_tooltip = '+CP+'register_'+org))
        if ix==1:
            access.append(iff('date > 1984.12.31',*[new_organisation(org,'unlock_decision_tooltip = '+CP+'register_'+org) for org in ('pcb','pcdob')]))
        effects.append(block(CP+'preview_party_reform_'+str(ix),*access))
    files[path]=decisions
    path='common/scripted_effects/COLDWAR_BRA_1970_politics.txt';files[path]=files[path].rstrip()+'\n\n'+'\n\n'.join(effects)+'\n'
    return pack
