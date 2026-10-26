# IMPERIA CW — Cold War: iraq 1970 — politics.
"""Country-owned 1970 leadership, using MD's ruling_party and native dispatcher."""
from common import ROOT,P,PARTIES,block,locline,group_gate
import importlib.util,json

GENERIC='gfx/leaders/EGY/Portrait_Arabia_Generic_1.dds'
PORTRAITS={
 'Ahmed Hassan al-Bakr':'gfx/Leaders/IRQ/IRQ_Coldwar_Ahmed_Hassan_al_Bakr.dds',
 'Saddam Hussein':'gfx/Leaders/IRQ/IRQ_COLDWAR_YOUNGER_SADDAM.dds',
 'Tariq Aziz':'gfx/leaders/mdcw_historical_pool/IRQ_tariq_aziz.dds',
 'Masoud Barzani':'gfx/Leaders/KUR/KUR_Coldwar_Young_Barzani_Massoud.dds',
 'Jalal Talabani':'gfx/Leaders/PUK/jalal_talabani.dds',
 "Ra'ad bin Zeid":'gfx/leaders/IRQ/raad_bin_zaid.dds',
}

def party_presentation(loc,root):
    """Read the shared curated presentation without running its installer.

    Historical politics owns these names/icons. Reuse its pure methods for
    our twelve keys, so an Iraqi regeneration cannot undo its reviewed names.
    Leader selection, party indices and all non-Iraqi keys stay untouched.
    """
    source=root/'tools/historical_politics_1970'
    spec=importlib.util.spec_from_file_location('coldwar_irq_shared_party_presentation',source/'party_presentation.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    world=json.loads((source/'data/world.json').read_text(encoding='utf-8-sig'))
    country=next(c for c in world['countries'] if c['tag']=='IRQ')
    reference=json.loads((source/'party_md_reference.json').read_text(encoding='utf-8'))
    icons={ideology:reference['families'][ideology]['icon'] for _,ideology,_ in PARTIES.values()}
    manifest=json.loads((source/'party_icon_manifest.json').read_text(encoding='utf-8-sig'))
    shared=module.PartyPresentation({'IRQ':country},manifest,icons)
    names=shared.names['IRQ']
    for slot,(name,ideology,_) in PARTIES.items():
        key=P+'party_'+str(slot)
        display=names.get('bespoke_names',{}).get(key) or names.get('party_names',{}).get(name,name)
        candidates=[row for row in country['parties'] if row['index']==slot and row['name']==name]
        icon=shared.icon('IRQ',ideology,candidates[0]) if candidates else (shared.native_icon('IRQ',display) or icons[ideology])
        loc[key]=icon+' '+display
        loc[key+'_icon']=icon
        loc[key+'_desc']=shared.description(slot,loc[key+'_desc']).replace('\\n','\n')

def generate(root=ROOT):
    loc={};effects=[]
    def L(k,v):loc[k]=v
    def effect(k,v):effects.append(block(k,v))
    def leader(name,ideology,expire=None):
        picture=PORTRAITS.get(name,GENERIC)
        body=f'name = "{name}"\npicture = "{picture}"\nideology = {ideology}\ntraits = {{ }}'
        if expire:body+='\nexpire = "'+expire+'"'
        return block('create_country_leader',body)
    record='''if = { limit = { has_country_leader = { name = "Ahmed Hassan al-Bakr" ruling_only = yes } } set_variable = { COLDWAR_IRQ_baath_incumbent = 0 } }
if = { limit = { has_country_leader = { name = "Saddam Hussein" ruling_only = yes } } set_variable = { COLDWAR_IRQ_baath_incumbent = 1 } }
if = { limit = { has_country_leader = { name = "Tariq Aziz" ruling_only = yes } } set_variable = { COLDWAR_IRQ_baath_incumbent = 2 } }
if = { limit = { has_country_leader = { name = "Mustafa Barzani" ruling_only = yes } } set_variable = { COLDWAR_IRQ_kdp_incumbent = 0 } }
if = { limit = { has_country_leader = { name = "Idris Barzani" ruling_only = yes } } set_variable = { COLDWAR_IRQ_kdp_incumbent = 1 } }
if = { limit = { has_country_leader = { name = "Masoud Barzani" ruling_only = yes } } set_variable = { COLDWAR_IRQ_kdp_incumbent = 2 } }'''
    effect(P+'record_incumbent',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes')+record))
    body='''COLDWAR_IRQ_reconcile_historical_roster = yes
COLDWAR_IRQ_record_incumbent = yes
update_set_politics = yes
if = {
 limit = { check_variable = { ruling_party = 21 } }
 if = { limit = { has_variable = COLDWAR_IRQ_install_baath } set_variable = { COLDWAR_IRQ_baath_incumbent = COLDWAR_IRQ_install_baath } clear_variable = COLDWAR_IRQ_install_baath }
 else_if = { limit = { check_variable = { MDCW_HP_native_retirement = 1 } NOT = { has_country_flag = do_not_retire } }
  set_country_flag = COLDWAR_IRQ_baath_alternate_succession
  add_to_variable = { COLDWAR_IRQ_baath_incumbent = 1 }
  if = { limit = { check_variable = { COLDWAR_IRQ_baath_incumbent > 2 } } set_variable = { COLDWAR_IRQ_baath_incumbent = 1 } }
 }
 if = { limit = { NOT = { has_variable = COLDWAR_IRQ_baath_incumbent } }
  if = { limit = { date > 1979.7.15 } set_variable = { COLDWAR_IRQ_baath_incumbent = 1 } }
  else = { set_variable = { COLDWAR_IRQ_baath_incumbent = 0 } }
 }
 if = { limit = { check_variable = { COLDWAR_IRQ_baath_incumbent = 0 } OR = { date > 1982.10.3 AND = { date > 1979.7.15 NOT = { has_country_flag = COLDWAR_IRQ_bakr_retained } NOT = { has_country_flag = COLDWAR_IRQ_baath_alternate_succession } } } } set_variable = { COLDWAR_IRQ_baath_incumbent = 1 } }
 kill_country_leader = yes
'''
    body+=block('if',block('limit','check_variable = { COLDWAR_IRQ_baath_incumbent = 0 }')+leader('Ahmed Hassan al-Bakr','Nat_Fascism','1982.10.4'))
    body+=block('else_if',block('limit','check_variable = { COLDWAR_IRQ_baath_incumbent = 2 }')+leader('Tariq Aziz','Nat_Fascism'))
    body+=block('else',leader('Saddam Hussein','Nat_Fascism'))+'}\n'
    body+='''else_if = {
 limit = { check_variable = { ruling_party = 6 } }
 if = { limit = { has_variable = COLDWAR_IRQ_install_kdp } set_variable = { COLDWAR_IRQ_kdp_incumbent = COLDWAR_IRQ_install_kdp } clear_variable = COLDWAR_IRQ_install_kdp }
 if = { limit = { NOT = { has_variable = COLDWAR_IRQ_kdp_incumbent } }
  if = { limit = { date > 1979.2.28 } set_variable = { COLDWAR_IRQ_kdp_incumbent = 2 } }
  else = { set_variable = { COLDWAR_IRQ_kdp_incumbent = 0 } }
 }
 if = { limit = { date > 1979.2.28 check_variable = { COLDWAR_IRQ_kdp_incumbent = 0 } } set_variable = { COLDWAR_IRQ_kdp_incumbent = 2 } }
 if = { limit = { date > 1987.1.30 check_variable = { COLDWAR_IRQ_kdp_incumbent = 1 } } set_variable = { COLDWAR_IRQ_kdp_incumbent = 2 } }
 kill_country_leader = yes
'''
    body+=block('if',block('limit','check_variable = { COLDWAR_IRQ_kdp_incumbent = 0 }')+leader('Mustafa Barzani','Conservative','1979.3.1'))
    body+=block('else_if',block('limit','check_variable = { COLDWAR_IRQ_kdp_incumbent = 1 }')+leader('Idris Barzani','Conservative','1987.1.31'))
    body+=block('else',leader('Masoud Barzani','Conservative'))+'}\n'
    for slot,(_,ideology,name) in PARTIES.items():
        if slot in [21,6]:continue
        creation=leader(name,ideology)
        if slot==8:
            creation=block('if',block('limit','NOT = { has_country_flag = COLDWAR_IRQ_subayti_dead }')+creation)+block('else',leader('Ibrahim al-Jaafari',ideology))
        if slot in (9,19):
            formed='COLDWAR_IRQ_'+('sciri' if slot==9 else 'puk')+'_formed'
            collective="Shi'a Opposition Council" if slot==9 else 'Kurdish Leftist Delegates'
            creation=block('if',block('limit','has_country_flag = '+formed)+creation)+block('else',leader(collective,ideology))
        body+=block('else_if',block('limit',f'check_variable = {{ ruling_party = {slot} }}')+'kill_country_leader = yes\n'+creation)
    # Less prominent families remain usable through MD politics without pulling
    # their modern Iraqi candidate lists into the 1970 campaign.
    families=['Western_Autocracy','conservatism','liberalism','socialism','communist_state','anarchist_communism','Conservative','Autocracy','Mod_Vilayat_e_Faqih','Vilayat_e_Faqih','Kingdom','Caliphate','Neutral_Muslim_Brotherhood','Neutral_Autocracy','Neutral_conservatism','oligarchism','Neutral_Libertarian','Neutral_green','neutral_Social','Neutral_Communism','Nat_Populism','Nat_Fascism','Nat_Autocracy','Monarchist']
    for slot,family in enumerate(families):
        if slot in PARTIES:continue
        body+=block('else_if',block('limit',f'check_variable = {{ ruling_party = {slot} }}')+'kill_country_leader = yes\n'+leader('Iraqi National Administration',family))
    body+='COLDWAR_IRQ_apply_decision_leader_choices = yes\nset_correct_ideology_trait = yes\nCOLDWAR_IRQ_reconcile_programmes = yes\nupdate_dirty_politicsview_expanded = yes'
    effect(P+'set_leader',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes')+body))
    daily='''COLDWAR_IRQ_reconcile_historical_roster = yes
COLDWAR_IRQ_record_incumbent = yes
if = { limit = { date > 1975.5.31 NOT = { has_country_flag = COLDWAR_IRQ_puk_formed } }
 set_country_flag = COLDWAR_IRQ_puk_formed
 if = { limit = { check_variable = { ruling_party = 19 } } COLDWAR_IRQ_set_leader = yes }
}
if = { limit = { date > 1982.10.31 NOT = { has_country_flag = COLDWAR_IRQ_sciri_formed } }
 set_country_flag = COLDWAR_IRQ_sciri_formed
 if = { limit = { check_variable = { ruling_party = 9 } } COLDWAR_IRQ_set_leader = yes }
}
if = {
 limit = { check_variable = { ruling_party = 21 } check_variable = { COLDWAR_IRQ_baath_incumbent = 0 }
  OR = { date > 1982.10.3 AND = { date > 1979.7.15 NOT = { has_country_flag = COLDWAR_IRQ_bakr_retained } NOT = { has_country_flag = COLDWAR_IRQ_baath_alternate_succession } } } }
 set_variable = { COLDWAR_IRQ_install_baath = 1 }
 COLDWAR_IRQ_set_leader = yes
}
if = { limit = { check_variable = { ruling_party = 6 } OR = { AND = { date > 1979.2.28 check_variable = { COLDWAR_IRQ_kdp_incumbent = 0 } } AND = { date > 1987.1.30 check_variable = { COLDWAR_IRQ_kdp_incumbent = 1 } } } }
 set_variable = { COLDWAR_IRQ_install_kdp = 2 }
 COLDWAR_IRQ_set_leader = yes
}
if = { limit = { OR = {
 AND = { has_country_flag = COLDWAR_IRQ_rikabi_dead has_country_leader = { name = "Fuad al-Rikabi" ruling_only = yes } }
 AND = { has_country_flag = COLDWAR_IRQ_dukhayl_dead has_country_leader = { name = "Abd al-Sahib Dukhayl" ruling_only = yes } }
 AND = { has_country_flag = COLDWAR_IRQ_subayti_dead has_country_leader = { name = "Muhammad Hadi al-Subayti" ruling_only = yes } }
} } COLDWAR_IRQ_set_leader = yes }
'''
    effect(P+'political_tick',block('if',block('limit','COLDWAR_IRQ_campaign_active = yes')+daily))
    # Names are inserted into the native MDCW_HP family consumers by compile.py.
    for slot,(name,ideology,_) in PARTIES.items():
        L(P+'party_'+str(slot),name)
        L(P+'party_'+str(slot)+'_desc','An Iraqi political organization represented through the existing '+ideology+' party family. Its national programme requires actual control of government.')
        icon_family='Communist_State' if ideology=='communist_state' else ideology
        L(P+'party_'+str(slot)+'_icon','£generic_'+icon_family+'_small')
    party_presentation(loc,root)
    return {'common/scripted_effects/COLDWAR_IRQ_1970_politics.txt':'\n'.join(effects),
            'localisation/english/COLDWAR_IRQ_1970_politics_l_english.yml':'l_english:\n# IMPERIA CW — Cold War: iraq 1970 English localisation.\n'+'\n'.join(locline(k,v) for k,v in loc.items())+'\n'}
