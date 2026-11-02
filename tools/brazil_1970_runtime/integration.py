# IMPERIA COLD WAR — Brazil 1970 bounded native integration.
import sys,re
from common import *
sys.path.insert(0,str(ROOT/'tools'))
from focus_prerequisite_ui import nodes

def header(t,feature='national programmes'):
    h='# IMPERIA COLD WAR — Brazil 1970 '+feature+' integration.\n'
    return t if t.startswith(h) else h+t
def append_effect(text,name,body):
    n=next(n for n in nodes(text) if n.key==name)
    return text[:n.end-1]+body+text[n.end-1:]
def build_integrations(loc):
    out={}
    rel='history/countries/BRA - Brazil.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    marker='# IMPERIA COLD WAR — Brazil authored 1970 tree BEGIN'
    if marker not in text:
        old='load_focus_tree = mdcw_1970_generic_focus';assert text.count(old)==1
        text=text.replace(old,marker+'\n\t\tload_focus_tree = '+TREE+'\n\t\tCOLDWAR_BRA_initialize = yes\n\t\t# IMPERIA COLD WAR — Brazil authored 1970 tree END',1)
    out[rel]=header(text)

    rel='common/scripted_effects/mdcw_1970_focus_tree_effects.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    marker='# IMPERIA COLD WAR — Brazil fallback routing BEGIN'
    if marker not in text:
        n=next(n for n in nodes(text) if n.key=='mdcw_load_1970_fallback_tree')
        opening=text.index('{',n.start)+1
        addition='\n\t'+marker+'\n\t'+iff(P+'campaign = yes\nNOT = { has_focus_tree = '+TREE+' }','load_focus_tree = '+TREE,P+'initialize = yes').replace('\n','\n\t')+'\n\t# IMPERIA COLD WAR — Brazil fallback routing END\n'
        text=text[:opening]+addition+text[opening:]
        target='AND = { tag = FRA IMP_is_1970_scenario = yes } # COLDWAR_FRA2 authored tree';assert text.count(target)==1
        text=text.replace(target,'AND = { tag = BRA IMP_is_1970_scenario = yes } # IMPERIA COLD WAR — Brazil authored tree\n\t\t\t\t\t'+target,1)
    out[rel]=header(text)

    rel='common/scripted_effects/00_money_system.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    for effect,call in [('calculate_additional_expense_rate','COLDWAR_BRA_add_weekly_expenses'),('calculate_additional_income_rate','COLDWAR_BRA_add_weekly_income')]:
        if call+' = yes' not in text:
            text=append_effect(text,effect,'\n\t# IMPERIA COLD WAR — Brazil weekly programme stream BEGIN\n\t'+call+' = yes\n\t# IMPERIA COLD WAR — Brazil weekly programme stream END\n')
        assert text.count(call+' = yes')==1
    out[rel]=header(text,'weekly finance')

    rel='common/scripted_localisation/mdcw_historical_parties.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    for slot,name in [(1,'conservatism'),(2,'liberalism'),(3,'socialism'),(20,'Nat_Populism')]:
        for suffix in ('','_desc','_icon'):
            provider='MDCW_HP_'+name+suffix;mark='# IMPERIA COLD WAR — BRA registry '+provider
            wrapper=P+'registry_'+str(slot)+(suffix or '_name');loc[wrapper]='[COLDWAR_BRA_1970_party_slot_'+str(slot)+suffix+']'
            if mark not in text:
                found=[]
                for n in nodes(text):
                    if n.key=='defined_text' and re.search(r'\bname\s*=\s*'+re.escape(provider)+r'\b',text[n.start:n.end]):found.append(n)
                assert len(found)==1,(provider,len(found));n=found[0]
                name_line=re.search(r'\bname\s*=\s*'+re.escape(provider)+r'\b',text[n.start:n.end]);pos=n.start+name_line.end()
                addition='\n\t'+mark+'\n\t'+block('text',block('trigger','original_tag = BRA','IMP_is_1970_scenario = yes'),'localization_key = '+wrapper).replace('\n','\n\t')+'\n'
                text=text[:pos]+addition+text[pos:]
    out[rel]=header(text,'party registry')

    # Own a separate else-if before the generic dispatcher, outside Chile's generator markers.
    rel='common/scripted_effects/00_leader_setup_scripted_effects.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    mark='# IMPERIA COLD WAR — Brazil early leader route BEGIN'
    endmark='# IMPERIA COLD WAR — Brazil early leader route END'
    if mark in text:
        begin=text.index(mark);end=text.index(endmark,begin)+len(endmark)
        old_route=text[begin:end]
        if old_route.splitlines()[1].startswith('if ='):
            text=text[:begin]+text[end:]
            text=text.replace('else_if = { limit = { COLDWAR_CHL_is_scenario = yes } COLDWAR_CHL_route_leader = yes }','if = { limit = { COLDWAR_CHL_is_scenario = yes } COLDWAR_CHL_route_leader = yes }',1)
    if mark not in text:
        parent=next(n for n in nodes(text) if n.key=='set_leader')
        fallback=[n for n in parent.children() if n.key=='else' and 'kill_country_leader = yes' in text[n.start:n.end]]
        assert len(fallback)==1
        pos=fallback[0].start
        route=mark+'\nelse_if = { limit = { COLDWAR_BRA_1970_party_leader_route_supported = yes } COLDWAR_BRA_1970_install_party_leader = yes }\n'+endmark+'\n\t'
        text=text[:pos]+route+text[pos:]
    out[rel]=header(text,'historical leader')

    rel='common/scripted_effects/00_MD_politicsview_scripted_effects.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    mark='# IMPERIA COLD WAR — Brazil actual party change BEGIN'
    if mark not in text:
        body='\n\t'+mark+'\n\t'+iff(P+'campaign = yes',P+'open_organisation_stages = yes',P+'reconcile_politics = yes',iff(P+'1970_party_leader_route_supported = yes',P+'1970_install_party_leader = yes'),P+'sync_programmes = yes').replace('\n','\n\t')+'\n\t# IMPERIA COLD WAR — Brazil actual party change END\n'
        text=append_effect(text,'change_ruling_party_effect',body)
    out[rel]=header(text,'native party change')

    rel='localisation/english/MD_money_l_english.yml';text=(ROOT/rel).read_text(encoding='utf-8-sig')
    assert text.startswith('l_english:')
    for key,token in [('ADDITIONAL_INCOME_REVENUES_TOOLTIP','[COLDWAR_BRA_weekly_income_display]'),('ADDITIONAL_EXPENSES_TOOLTIP','[COLDWAR_BRA_weekly_expense_display]')]:
        lines=text.splitlines();matches=[i for i,s in enumerate(lines) if re.match(r'^\s*'+key+r':',s)];assert len(matches)==1
        i=matches[0]
        if token not in lines[i]:pos=lines[i].rfind('"');lines[i]=lines[i][:pos]+token+lines[i][pos:]
        text='\n'.join(lines)+'\n'
    mark='# IMPERIA COLD WAR — Brazil programme budget display integration.'
    if mark not in text[:180]:text=text.replace('l_english:\n','l_english:\n'+mark+'\n',1)
    out[rel]=text
    return out

def build_on_actions():
    bra_daily=[P+'initialize = yes',P+'open_organisation_stages = yes',P+'reconcile_politics = yes',P+'reconcile_focus_receipts = yes',P+'sync_programmes = yes',P+'sync_agreements = yes']
    monthly=[P+'political_pressure_pulse = yes',P+'1970_monthly_politics_reconcile = yes',iff(flag('1970_party_reform_open')+'\n'+once('event_sent_party_split'),P+'fire_party_split = yes')]
    # Formation helpers expose actual dated parties without changing a governing slot.
    monthly+=[P+'1970_mark_prn_leader_available = yes']
    monthly += [iff(P+'1970_party_leader_route_supported = yes',P+'1970_install_party_leader = yes')]
    startup=block('on_startup',block('effect',country('BRA',P+'initialize = yes')))
    daily=block('on_daily',block('effect',iff(P+'campaign = yes',*bra_daily),P+'cleanup_orphaned_agreements = yes'))
    month=block('on_monthly',block('effect',iff(P+'campaign = yes',*monthly)))
    change=[block(name,block('effect',iff(P+'campaign = yes',P+'reconcile_politics = yes',P+'sync_programmes = yes'))) for name in ('on_government_change','on_ruling_party_change')]
    return output('common/on_actions/COLDWAR_BRA_1970_on_actions.txt',block('on_actions',startup,daily,month,*change))
