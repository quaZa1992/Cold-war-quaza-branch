# IMPERIA COLD WAR — Reproducible Kissinger focus and regional-system integration.
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

if __package__ in (None,''):
    sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
    __package__='usa_kissinger_implementation'
from .shared import *
from . import deals,regional,content,auxiliary,aid,reconciliation,repression,fiscal,underground,triangular,triangular_china
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes,field

STEM='COLDWAR_USA_kissinger'

def event(eid,title,desc,options,loc,immediate='',picture='GFX_political_deal'):
    key='COLDWAR_USA_KS.'+str(eid);loc[key+'.t']=title;loc[key+'.d']=desc
    body=[f'id = {key}',f'title = {key}.t',f'desc = {key}.d','picture = '+picture,'is_triggered_only = yes']
    if immediate:body.append(b('immediate',immediate))
    for i,(label,gate,reward) in enumerate(options):
        name=key+'.'+str(i);loc[name]=label
        body.append(b('option',[f'name = {name}',b('trigger',gate) if gate else '',reward]))
    return b('country_event',body)

def ui_outputs(loc):
    windows=[];controllers=[];texts=[]
    for h,d in HOSTS.items():
        tag=d['tag'];name=P+'region_'+h+'_window';icon=P+h+'_bar'
        loc[P+h+'_unrest_readout']='Unrest: §Y[?'+tag+'.'+P+'ui_unrest|0]/100§!'
        loc[P+h+'_heading']=d['name']+': Regional Unrest'
        status=P+'GetLegacy_'+h;warning=P+'GetWarning_'+h
        for suffix,value in [('strong','Earlier stabilisation still holds.'),('fading','Earlier stabilisation is gradually fading.'),('none','No lasting period of calm established.'),('warning','Uprising warning: the region requires attention.'),('quiet','Security, investment and negotiations can contain unrest.'),('pressure','Intensified foreign support: [?'+tag+'.'+P+'pressure_weeks|0] weeks remain.'),('settled','A consolidated regional settlement remains in force.'),('reconciling','Regional reconciliation: [?'+tag+'.'+P+'reconciliation_weeks|0]/520 weeks.')]:loc[P+h+'_'+suffix]=value
        loc[P+h+'_trauma']='Legacy of repression: [?'+tag+'.'+P+'trauma_weeks|0] weeks remain.'
        def text(name,x,y,w,h,text):return b('instantTextBoxType',[f'name = "{name}"',f'position = {{ x = {x} y = {y} }}',f'font = "hoi_16mbs"',f'maxWidth = {w}',f'maxHeight = {h}',f'text = "{text}"','format = left'])
        windows.append(b('containerWindowType',[f'name = "{name}"','position = { x = 5 y = 0 }','size = { width = 493 height = 112 }',
          text(P+h+'_title',12,4,469,22,P+h+'_heading'),
          b('iconType',[f'name = "{icon}"','position = { x = 12 y = 34 }',f'spriteType = "GFX_{P}unrest_bar"']),
          text(P+h+'_readout',260,32,221,20,P+h+'_unrest_readout'),text(P+h+'_legacy',12,58,469,20,'['+status+']'),text(P+h+'_warning',12,82,469,20,'['+warning+']')]))
        controllers.append(b(P+'region_'+h+'_gui',['context_type = decision_category',f'window_name = "{name}"',f'dirty = {tag}.{P}ui_dirty',b('properties',b(icon,f'frame = {tag}.{P}ui_unrest'))]))
        texts.append(b('defined_text',[f'name = {status}',b('text',[b('trigger',b(tag,check('ui_legacy','>',1))),f'localization_key = {P}{h}_strong']),b('text',[b('trigger',b(tag,check('ui_legacy','>',0))),f'localization_key = {P}{h}_fading']),b('text','localization_key = '+P+h+'_none')]))
        texts.append(b('defined_text',[f'name = {warning}',b('text',[b('trigger',b(tag,flag('warning'))),f'localization_key = {P}{h}_warning']),b('text',[b('trigger',P+'pressure_'+h+' = yes'),f'localization_key = {P}{h}_pressure']),b('text',[b('trigger',b(tag,check('trauma_weeks','>',0))),f'localization_key = {P}{h}_trauma']),b('text',[b('trigger',b(tag,flag('pacified'))),f'localization_key = {P}{h}_settled']),b('text',[b('trigger',b(tag,check('reconciliation_weeks','>',0))),f'localization_key = {P}{h}_reconciling']),b('text','localization_key = '+P+h+'_quiet')]))
    gfx=b('progressbartype',['name = "GFX_'+P+'unrest_bar"','textureFile1 = "gfx/interface/autonomy/subject_progress_bar_long.dds"','textureFile2 = "gfx/interface/autonomy/subject_progress_bar_long_bg.dds"','size = { x = 240 y = 16 }','effectFile = "gfx/FX/progress.lua"','steps = 100'])
    gfx+='\n'+b('spriteType',['name = "GFX_idea_'+P+'consultations"','texturefile = "gfx/interface/ideas/diplomacy/flexible_foreign_policy2.dds"'])
    gfx+='\n'+b('spriteType',['name = "GFX_idea_'+P+'institutions"','texturefile = "gfx/interface/ideas/politics/political_reform.dds"'])
    for index in range(12):
        texture=f'gfx/interface/goals/COLDWAR_USA_KS/focus_{index}.dds'
        gfx+='\n'+b('spriteType',[f'name = "GFX_goal_{P}{index}"',f'texturefile = "{texture}"'])
        animations=[]
        for rotation in (-90,90):
            animations.append(b('animation',[f'animationmaskfile = "{texture}"',
              'animationtexturefile = "gfx/interface/goals/shine_overlay.dds"',
              f'animationrotation = {rotation}.0','animationlooping = no',
              'animationtime = 0.75','animationdelay = 0','animationblendmode = "add"',
              'animationtype = "scrolling"','animationrotationoffset = { x = 0.0 y = 0.0 }',
              'animationtexturescale = { x = 1.0 y = 1.0 }']))
        gfx+='\n'+b('spriteType',[f'name = "GFX_goal_{P}{index}_shine"',f'texturefile = "{texture}"',
          'effectfile = "gfx/FX/buttonstate.lua"',*animations,'legacy_lazy_load = no'])
    for h in HOSTS:gfx+='\n'+b('spriteType',['name = "GFX_'+P+'aftermath_'+h+'"','texturefile = "gfx/event_pictures/COLDWAR_USA_KS/aftermath_'+h+'.dds"'])
    texts.append(repression.incident_texts(loc))
    return {'interface/'+STEM+'.gui':MARK+b('guiTypes','\n'.join(windows)),
      'interface/'+STEM+'.gfx':MARK+b('spriteTypes',gfx),
      'common/scripted_guis/'+STEM+'.txt':MARK+b('scripted_gui','\n'.join(controllers)),
      'common/scripted_localisation/'+STEM+'.txt':MARK+'\n'.join(texts)}

def country_outputs(loc):
    out={};tags=[]
    for h,d in HOSTS.items():
        if h=='irq':continue
        tag=d['rebel'];name={'per':'Iranian Kurdish Council','tur':'Anatolian Kurdish Council','syr':'Jazira Regional Authority'}[h]
        loc[tag]=name;loc[tag+'_DEF']=name;loc[tag+'_ADJ']={'per':'Iranian Kurdish','tur':'Anatolian Kurdish','syr':'Jaziran'}[h]
        for outlook in ('democratic','communism','fascism','neutrality','nationalist'):
            loc[tag+'_'+outlook]=name;loc[tag+'_'+outlook+'_DEF']=name;loc[tag+'_'+outlook+'_ADJ']=loc[tag+'_ADJ']
        tags.append(tag+' = "countries/'+STEM+'_'+tag+'.txt"')
        color={'per':'102 147 85','tur':'190 160 65','syr':'90 143 164'}[h]
        out['common/countries/'+STEM+'_'+tag+'.txt']=MARK+'graphical_culture = middle_eastern_gfx\ngraphical_culture_2d = middle_eastern_2d\ncolor = { '+color+' }\n'
        history=['capital = '+str(d['states'][0]),'set_oob = "mdcw_1970_empty_land"','set_naval_oob = "mdcw_1970_empty_naval"','set_air_oob = "mdcw_1970_empty_air"',
          'set_variable = { treasury = 0 }','set_variable = { debt = 0 }','set_variable = { int_investments = 0 }',
          'set_popularities = { neutrality = 100 }','set_politics = { ruling_party = neutrality elections_allowed = no }',
          'add_ideas = { us_dollar sunni non_state_actor lacks_international_recognition bureau_03 recession defence_05 edu_02 health_02 social_01 police_01 consumption_economy export_economy volunteer_army volunteer_women minimal_regulations balanced_protections standard_maintenance partially_privatized_healthcare }',
          P+'regional_research = yes','load_focus_tree = mdcw_1970_generic_focus']
        out['history/countries/'+tag+' - '+name+'.txt']=MARK+'\n'.join(history)+'\n'
    out['common/country_tags/'+STEM+'.txt']=MARK+'\n'.join(tags)+'\n'
    return out

def outputs():
    loc=base_loc();fx={};tr={};ideas=[];decisions=[];categories=[]
    fiscal.register(loc,fx)
    deals.build(loc,fx,tr,ideas,decisions)
    regional.build(loc,fx,tr,ideas,decisions,categories)
    auxiliary.build(loc,fx,tr,ideas,decisions)
    reconciliation.build(loc,fx,tr,ideas,decisions)
    repression.build(loc,fx,tr,ideas,decisions)
    aid.build(loc,fx,tr,ideas)
    underground.build(loc,fx,tr,ideas,decisions)
    fragment,specs=content.build(loc,fx,tr,ideas,decisions)
    triangular_china.build(loc,fx,tr,ideas,decisions)
    extension,extra_specs=triangular.build(loc,fx,tr,ideas,decisions)
    fragment+='\n\n'+extension;specs.update(extra_specs)
    # Complete own-country initialization is only entered after a new local
    # identity is born. Existing human players never run these resets.
    fx[P+'regional_research']=auxiliary.regional_research()
    fx[P+'initialize_new_actor']=auxiliary.country_init()
    fx[P+'calculate_streams']='\n'.join([P+'refresh_fiscal = yes',v('weekly_expense',0),v('weekly_income',0),
      guard('IMP_is_1970_scenario = yes',P+'deal_streams = yes\n'+P+'regional_streams = yes\n'+P+'domestic_streams = yes\n'+P+'td_streams = yes\n'+P+'td_strategy_streams = yes\n'+guard('tag = USA\n'+flag('chile_funding')+'\ncountry_exists = CHL',fiscal.stream('expense','us_chile')))])
    events=[]
    for i,(key,d) in enumerate(deals.DEALS.items()):
        if key=='moscow':continue
        ident=P+'deal_'+key
        events.append(event(i+1,d['name'],'Washington proposes a standing arrangement for political consultation and regional cooperation.',[
          ('Accept the proposed terms',ident+'_accept_valid = yes',visible_and_hidden(deals.preview(key),ident+'_accept = yes')),
          ('Decline the proposal',flag('deal_'+key+'_pending'),b('hidden_effect',ident+'_end = yes')),
          ('Review the proposal',None,'ai_chance = { factor = 0 }')],loc))
    events.append(event(2,'American-Soviet Consultations','Our delegations may review the current negotiating paper through the standing treaty channel.',[
      ('Review the negotiating paper','icwt_pending = yes\ncheck_variable = { global.icwt_pending = 7 }','icwt_review_7 = yes'),
      ('Continue consultations',None,'')],loc))
    events.append(event(101,'Regional Mobilisation','Local political networks are preparing an armed mobilisation. A reinforced security operation, regional investment or a negotiated settlement can still contain the crisis.',[('Review regional policy',None,'')],loc))
    events.append(event(102,'Northern Political Talks','Washington proposes discussions with Baghdad and the Kurdish representatives on regional rights.',[('Consider the proposal',None,'')],loc))
    events.extend(repression.events(loc,event))
    # Events and decisions share exactly the same execution guards and fees.
    global_cat=P+'diplomacy';loc[global_cat]='American Statecraft';loc[global_cat+'_desc']='Review proposals, continuing agreements and the implementation of authorised foreign-policy measures.'
    categories.append(b(global_cat,['icon = generic_political_discourse','priority = 165',b('visible','IMP_is_1970_scenario = yes\nOR = { tag = USA tag = IRQ tag = PER tag = TUR tag = SYR tag = CHI tag = SOV tag = UNI tag = KUR tag = PUK tag = KPI tag = KPT tag = KPS tag = CHL }')]))
    groups={global_cat:[]}
    for h in HOSTS:groups[P+'region_'+h]=[]
    for raw in decisions:
        key=nodes(raw)[0].key
        h=next((h for h in HOSTS if key.startswith(P+h+'_') and not key.endswith('_mediation')),None)
        groups[P+'region_'+h if h else global_cat].append(raw)
    weekly='\n'.join([guard('tag = USA\nIMP_is_1970_scenario = yes',P+'migrate_irq = yes\n'+P+'count_campaigns = yes\n'+P+'reconcile_deals = yes\n'+P+'reconcile_aid = yes\n'+P+'misc_reconcile = yes\n'+P+'td_migrate_moscow = yes\n'+P+'td_reconcile = yes\n'+P+'td_reconcile_priorities = yes\n'+P+'td_sov_signal_quote = yes'),P+'regional_weekly = yes'])
    daily='\n'.join(guard('tag = '+d['tag']+'\n'+flag('tracked'),P+'reconcile_domestic = yes\n'+P+'refresh_host = yes') for d in HOSTS.values())
    daily+='\n'+guard('tag = CHL\nIMP_is_1970_scenario = yes','set_variable = { '+P+'investment_quote = gdp_total }\nmultiply_variable = { '+P+'investment_quote = .01 }')
    daily+='\n'+guard('tag = USA\nIMP_is_1970_scenario = yes',P+'refresh_fiscal_usa = yes')
    startup='USA = { '+P+'refresh_fiscal_usa = yes\n'+P+'migrate_irq = yes\n'+P+'count_campaigns = yes\n'+P+'reconcile_deals = yes\n'+P+'td_migrate_moscow = yes\n'+P+'td_reconcile = yes\n'+P+'td_reconcile_priorities = yes }'
    out={
      'common/scripted_effects/'+STEM+'.txt':MARK+'\n\n'.join(b(k,v) for k,v in fx.items())+'\n',
      'common/scripted_triggers/'+STEM+'.txt':MARK+'\n\n'.join(b(k,v) for k,v in tr.items())+'\n',
      'common/ideas/'+STEM+'.txt':MARK+b('ideas',b('country','\n'.join(ideas)))+'\n',
      'common/decisions/'+STEM+'.txt':MARK+'\n\n'.join(b(k,'\n'.join(v)) for k,v in groups.items())+'\n',
      'common/decisions/categories/'+STEM+'.txt':MARK+'\n\n'.join(categories)+'\n',
      'events/'+STEM+'.txt':MARK+'add_namespace = COLDWAR_USA_KS\n'+'\n'.join(events)+'\n',
      'common/on_actions/'+STEM+'.txt':MARK+b('on_actions',[b('on_startup',b('effect',startup)),b('on_weekly',b('effect',weekly)),b('on_daily',b('effect',daily)),b('on_war_relation_added',b('effect','USA = { '+P+'reconcile_deals = yes\n'+P+'reconcile_aid = yes }'))])+'\n',
      'common/opinion_modifiers/'+STEM+'.txt':MARK+b('opinion_modifiers',[b(P+'breach_opinion','value = -75\ndecay = 0'),b(P+'recognition_opinion','value = 50\ndecay = 0'),b(P+'censure_opinion','value = -50\ndecay = 1')])+'\n',
      'tools/usa_kissinger_implementation/focus_fragment.txt':MARK+fragment+'\n',
      'tools/usa_kissinger_implementation/installed_specs.json':json.dumps(dict(project='IMPERIA COLD WAR',approved_sha256=APPROVED_SHA,focuses=specs),indent=2)+'\n'}
    out.update(ui_outputs(loc));out.update(country_outputs(loc))
    out.update(triangular.extra_outputs(loc));out.update(triangular_china.extra_outputs(loc))
    out['localisation/english/'+STEM+'_l_english.yml']=locfile(loc)
    return {path:explicit_decimals(text) if path.endswith(('.txt','.gui','.gfx')) else text for path,text in out.items()}

def patch_tree(text):
    text=re.sub(r'\n# IMPERIA COLD WAR — KISSINGER FOCUSES BEGIN\n.*?\n# IMPERIA COLD WAR — KISSINGER FOCUSES END\n','\n',text,flags=re.S)
    text=re.sub(r'(?m)^'+re.escape(MARK.rstrip())+r'\n','',text)
    root=next(n for n in nodes(text) if n.key=='focus_tree');edits=[]
    for n in root.children():
        if n.key=='focus' and str(field(n.children(),'id','')).startswith(P):edits.append((n.start,n.end,''))
    for start,end,value in sorted(edits,reverse=True):text=text[:start]+value+text[end:]
    text=re.sub(r'(?m)^\s*# IMPERIA COLD WAR — KISSINGER FOCUSES (?:BEGIN|END)\s*\n?','',text)
    root=next(n for n in nodes(text) if n.key=='focus_tree')
    fragment=outputs()['tools/usa_kissinger_implementation/focus_fragment.txt'].removeprefix(MARK)
    addition='\n\n# IMPERIA COLD WAR — KISSINGER FOCUSES BEGIN\n'+fragment+'\n# IMPERIA COLD WAR — KISSINGER FOCUSES END\n'
    text=text[:root.end-1].rstrip()+addition+text[root.end-1:]
    text=re.sub(r'(name\s*=\s*USA_1970_foreign_shortcut\s+target\s*=\s*)(?:USA_1970_F0|COLDWAR_USA_KS_doctrine)',lambda m:m[1]+P+'doctrine',text)
    text=re.sub(r'(scroll_wheel_factor\s*=\s*)\.8\b',lambda m:m[1]+'0.8',text)
    # Keep the historical Kuwait-war entry independent, but route its northern
    # military commitment into the same continuing equipment/budget ledger.
    from .gulf_bridge import patch_legacy_focus
    return patch_legacy_focus(text)

def integrate_money():
    path='common/scripted_effects/00_money_system.txt';text=(ROOT/path).read_text(encoding='utf-8-sig')
    for kind,var in [('income','additional_income_rate'),('expense','additional_expenses_rate')]:
        begin='# IMPERIA COLD WAR — Kissinger weekly '+kind+' BEGIN';end='# IMPERIA COLD WAR — Kissinger weekly '+kind+' END'
        text=re.sub(re.escape(begin)+r'.*?'+re.escape(end)+r'\n?','',text,flags=re.S)
        body=begin+'\n'+P+'calculate_streams = yes\nadd_to_variable = { '+var+' = '+P+'weekly_'+kind+' }\n# IMPERIA COLD WAR — Signed superpower programmes in weekly MD units\nicwt_programme_fiscal = yes\nadd_to_variable = { '+var+' = icwt_weekly_'+kind+' }\n'+end
        if kind=='income':
            anchor='set_variable = { '+var+' = 0 }';assert text.count(anchor)==1,anchor
            pos=text.index(anchor)+len(anchor)
        else:
            # These are signed nominal contracts, like the existing USA deals.
            # Append after the native inflation calculation so the advertised
            # donor expense still matches the recipient's weekly transfer.
            provider=next(n for n in nodes(text) if n.key=='calculate_additional_expense_rate')
            pos=provider.end-1
        text=text[:pos].rstrip()+'\n'+body+'\n'+text[pos:].lstrip('\n')
    if not text.startswith('# IMPERIA COLD WAR'):text=MARK+text
    return [path] if write(path,text) else []

def emit_runtime():
    changed=[]
    for path,text in outputs().items():
        if write(path,text,path.endswith('.yml')):changed.append(path)
    from .assets import emit_assets
    return changed+emit_assets()

def main():
    changed=emit_runtime()
    path='common/national_focus/USA_1970.txt';text=(ROOT/path).read_text(encoding='utf-8-sig')
    if write(path,patch_tree(text)):changed.append(path)
    changed+=integrate_money()
    print(json.dumps(dict(project='IMPERIA COLD WAR',new_focuses=41+len(triangular.NEW),changed=changed),indent=2))

if __name__=='__main__':main()
