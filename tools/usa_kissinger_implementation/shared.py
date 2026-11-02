# IMPERIA COLD WAR — Canonical Kissinger programme data and native script helpers.
from pathlib import Path
from decimal import Decimal
import hashlib
import json
import re
import textwrap

ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
P='COLDWAR_USA_KS_'
MARK='# IMPERIA COLD WAR — Kissinger statecraft and contested regional politics.\n'
APPROVED=HERE/'approved_design.json'
APPROVED_SHA='54d93f67e7cd0be84ce4cf865d1dbc844b87a2f7be8372cc67c703d1de9f5cf3'
assert hashlib.sha256(APPROVED.read_bytes()).hexdigest()==APPROVED_SHA,'Approved Kissinger design changed'
DESIGN=json.loads(APPROVED.read_text(encoding='utf-8'))
FOCUSES={n['key']:n for n in DESIGN['nodes'] if not n['existing']}
HOSTS={
 'irq':dict(tag='IRQ',name='Iraq',states=[164,633,630,1078],rebel='KUR',base=52,contact='irq_contacts',fund='irq_fund',front='irq_front',rights='irq_autonomy',claim='irq_independence'),
 'per':dict(tag='PER',name='Iran',states=[408],rebel='KPI',base=40,contact='irn_contacts',fund='irn_fund',front='irn_front',rights='irn_rights',claim='irn_claim'),
 'tur':dict(tag='TUR',name='Turkey',states=[162],rebel='KPT',base=40,contact='tur_networks',fund='tur_networks',front='tur_front',rights='tur_rights',claim='tur_claim'),
 'syr':dict(tag='SYR',name='Syria',states=[193],rebel='KPS',base=38,contact='syr_contacts',fund='syr_voice',front='syr_front',rights='syr_rights',claim='syr_claim')}
MODS={
 'Foreign Influence':('foreign_influence_modifier',False),
 'Foreign Influence Defense':('foreign_influence_defense_modifier',False),
 'Decryption':('decryption_factor',False),'Encryption':('encryption_factor',False),
 'Bureaucracy Cost':('bureaucracy_cost_multiplier_modifier',True),
 'Police Cost':('police_cost_multiplier_modifier',True),
 'Army Personnel Cost':('army_personnel_cost_multiplier_modifier',True),
 'Agency Upgrade Time':('agency_upgrade_time',True),'Stability':('stability_factor',False),
 'Army Experience Gain':('experience_gain_army_factor',False),
 'Division Organisation':('army_org_factor',False)}
CAPTIONS={'irq_settlement':'Guarantee Autonomy','irq_independence':'A Separate Kurdistan',
 'irn_contacts':'Zagros Networks','irn_fund':'Mountain Committees','irn_front':'Challenge Tehran',
 'irn_claim':'A Kurdish Claim','tur_networks':'Southeastern Contacts','tur_rights':'Regional Rights Talks',
 'tur_front':'An Armed Alternative','tur_claim':'A Separate State','syr_rights':'Citizenship and Rights',
 'syr_claim':'Northern Authority'}
COORDS={'clients':[73,3],'angola':[73,4],'political':[77,3],'chile':[77,4],'guarantees':[81,2],'shuttle':[81,3]}
# IMPERIA COLD WAR — Preserve the Kurdish fan while accommodating the approved triangle.
COORDS.update({'irq_contacts':[75,5],'irq_transit':[73,6],'irq_anatolia':[77,6],
 'irq_fund':[75,7],'irq_autonomy':[73,8],'irq_front':[77,8],
 'irq_settlement':[73,9],'irq_independence':[77,9],'angola':[73,5]})

def num(v):
    s=format(Decimal(str(v)).normalize(),'f')
    assert '.' not in s or len(s.split('.')[1])<=5,s
    return s

def explicit_decimals(text):
    """Use native-parser-safe numeric spelling in this module's own scripts."""
    return re.sub(r'(?<![\w.])([+-]?)\.(\d+)',lambda m:m[1]+'0.'+m[2],text)

def b(key,body):
    if isinstance(body,(list,tuple)):body='\n'.join(x for x in body if x)
    return f'{key} = {{\n'+textwrap.indent(body.strip(),'\t')+'\n}'

def guard(test,body):return b('if',[b('limit',test),body])
def money(value):return f'set_temp_variable = {{ treasury_change = {num(value)} }}\nmodify_treasury_effect = yes'
def v(key,value):return f'set_variable = {{ {P}{key} = {num(value)} }}'
def add(key,value):return f'add_to_variable = {{ {P}{key} = {num(value)} }}'
def flag(name):return f'has_country_flag = {P}{name}'
def setflag(name):return f'set_country_flag = {P}{name}'
def noflag(name):return f'NOT = {{ {flag(name)} }}'
def check(name,op,value):return f'check_variable = {{ {P}{name} {op} {num(value)} }}'
def at_least(variable,value):return f'check_variable = {{ var = {variable} value = {value} compare = greater_than_or_equals }}'
def requirement(label,conditions):return b('custom_trigger_tooltip',['tooltip = '+P+label,conditions])
def effect_preview(body):return b('effect_tooltip',body)
def visible_and_hidden(preview,execution):return preview+'\n'+b('hidden_effect',execution)
def state_test(tag,states):return 'OR = { '+' '.join(f'{sid} = {{ is_owned_and_controlled_by = {tag} is_fully_controlled_by = {tag} }}' for sid in states)+' }'

def modifier_rows(mods):
    return '\n'.join(f'add_to_variable = {{ {P}preview_{MODS[label][0]} = {num(value)} tooltip = {P}mod_{MODS[label][0]}_tt }}' for label,value in mods.items())

def weekly_row(value):return f'add_to_variable = {{ {P}preview_weekly = {num(value)} tooltip = {P}weekly_tt }}'
def scalar_row(name,value):return f'add_to_variable = {{ {P}preview_{name} = {num(value)} tooltip = {P}{name}_tt }}'

def base_loc():
    loc={P+'if_accept_tt':'If they accept:',P+'weekly_tt':'Weekly programme balance: $RIGHT|+=5$ billion/week',
      P+'organisation_tt':'Regional organisation: $RIGHT|+=0$',P+'unrest_tt':'Regional unrest: $RIGHT|-=0$',
      P+'material_tt':'Committed regional assistance: $RIGHT|+0$ infantry weapons',
      P+'stabilisation_tt':'Lasting stabilisation: $RIGHT|+=0$',P+'slots_tt':'Maximum active regional campaigns: $RIGHT|0$',
      P+'equipment_tt':'At least 1,000 infantry weapons in the stockpile.',
      P+'slot_available_tt':'An available regional campaign slot, or an existing commitment to this region.',
      P+'local_partner_tt':'A cooperating local political network or an accepted agreement with its existing regional government.',
      P+'confrontation_tt':'A strategic confrontation with the regional government.',
      P+'field_forces_tt':'At least two field divisions stationed in the contested region.',
      P+'eligible_region_tt':'The regional government owns and controls the contested territory.',
      P+'recognition_tt':'An independent regional authority controls its own territory and requests recognition.'}
    loc.update({P+'framework_tt':'Baghdad has accepted the framework for northern political talks.',
      P+'tur_contacts_tt':'An active intelligence partnership with Turkey, or established southeastern contacts.',
      P+'syr_crisis_tt':'Syria is at war, or regional unrest exceeds 64.',
      P+'route_tt':'An accepted frontier transit arrangement or an active covert air-supply route.',
      P+'irq_territory_tt':'Iraq owns and fully controls at least two eligible northern states.'})
    for tag in ('KUR','PUK'):
        loc[P+'liaison_'+tag.lower()+'_tt']='Any relevant ['+tag+'.GetNameDef] government has accepted regional political liaison.'
    for label,(key,cost) in MODS.items():loc[P+'mod_'+key+'_tt']=label+': $RIGHT|'+('-=' if cost else '+=')+'%1$'
    return loc

def idea(key,title,description,mods,picture='COLDWAR_USA_KS_consultations',weekly=None):
    # Values are real native modifiers. Preview rows use the same dictionary.
    rows='\n'.join(MODS[k][0]+' = '+num(v) for k,v in mods.items())
    if weekly is not None:rows+='\ncustom_modifier_tooltip = '+P+key+'_weekly_tt'
    return b(P+key,['picture = '+picture,'allowed = { always = no }','allowed_civil_war = { always = no }',b('modifier',rows)])

def fiscal_text(value):
    return 'Programme balance: §'+('R-' if value<0 else 'G+')+'$'+format(abs(Decimal(str(value))),'.5f')+' billion/week§!'

def write(path,text,bom=False):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True)
    data=text.encode('utf-8-sig' if bom else 'utf-8')
    if p.exists() and p.read_bytes()==data:return False
    p.write_bytes(data);return True

def locfile(loc):return 'l_english:\n'+MARK+'\n'.join(' '+k+':0 '+json.dumps(value,ensure_ascii=False) for k,value in loc.items())+'\n'
