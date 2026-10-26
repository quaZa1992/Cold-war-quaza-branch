# IMPERIA CW — Cold War: iraq 1970 — common.
"""Small shared authoring utilities; importing this module never writes files."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT/'tools/vietnam_1970'))
from script_ast import parse,emit,format_code,first,values,walk

P='COLDWAR_IRQ_'
TREE=P+'1970_focus'
def block(key,body):return key+' = {\n'+body+'\n}\n'
def flag(key):return 'has_country_flag = '+key
def invflag(key):return 'NOT = { '+flag(key)+' }'
def check(var,value,compare='greater_than_or_equals'):
    return f'check_variable = {{ var = {var} value = {value} compare = {compare} }}'
def invoice(key,share):
    return block('if',block('limit',invflag(key+'_quoted')+'\ncheck_variable = { gdp_total > 0 }')+f'set_variable = {{ {key}_invoice = gdp_total }}\nmultiply_variable = {{ {key}_invoice = {share:g} }}\nset_country_flag = {key}_quoted')
def pay_var(var):return f'set_temp_variable = {{ treasury_change = {var} }}\nmultiply_temp_variable = {{ treasury_change = -1 }}\nmodify_treasury_effect = yes'
def locline(key,text):
    text=str(text).replace('\\','\\\\').replace('"','\\"').replace('\r','').replace('\n','\\n')
    return f' {key}:0 "{text}"'

PARTIES={
 2:('National Progressive Party','liberalism','Muhammad Hadid'),
 3:('National Democratic Party','socialism','Hussein Jamil'),
 4:('Iraqi Communist Party','communist_state','Aziz Muhammad'),
 6:('Kurdistan Democratic Party','Conservative','Mustafa Barzani'),
 8:('Islamic Dawa Party','Mod_Vilayat_e_Faqih','Muhammad Hadi al-Subayti'),
 9:('Supreme Council for the Islamic Revolution in Iraq','Vilayat_e_Faqih','Muhammad Baqir al-Hakim'),
 12:('Iraqi Islamic Party','Neutral_Muslim_Brotherhood','Numan al-Samarrai'),
 18:('Arab Socialist Union','neutral_Social','Khair al-Din Haseeb'),
 19:('Patriotic Union of Kurdistan','Neutral_Communism','Jalal Talabani'),
 21:("Arab Socialist Ba'ath Party",'Nat_Fascism','Ahmed Hassan al-Bakr'),
 22:('Republican Officers','Nat_Autocracy','Abd al-Rahman Arif'),
 23:('Constitutional Hashemite Movement','Monarchist',"Ra'ad bin Zeid"),
}
GROUP_SLOTS={'baath':[21],'bakr':[21],'saddam':[21],'officers':[22], 'nasserist':[18],
 'communists':[4],'aziz':[4],'civic':[2,3],'monarchy':[23],'kurds':[6], 'puk':[19],
 'dawa':[8],'sciri':[9],'sunni':[12]}

def group_gate(key):
    body='COLDWAR_IRQ_campaign_active = yes'
    if key in GROUP_SLOTS:
        clauses=[f'check_variable = {{ ruling_party = {s} }}' for s in GROUP_SLOTS[key]]
        body+='\n'+(clauses[0] if len(clauses)==1 else block('OR','\n'.join(clauses)))
    if key=='bakr':body+='\nCOLDWAR_IRQ_leader_bakr_in_office = yes'
    if key=='saddam':body+='\nCOLDWAR_IRQ_leader_saddam_in_office = yes'
    if key=='aziz':body+='\nCOLDWAR_IRQ_leader_aziz_muhammad_in_office = yes'
    if key=='puk':body+='\nhas_country_flag = COLDWAR_IRQ_puk_formed'
    if key=='sciri':body+='\nhas_country_flag = COLDWAR_IRQ_sciri_formed'
    return body
