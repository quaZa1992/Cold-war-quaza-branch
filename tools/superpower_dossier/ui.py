# IMPERIA COLD WAR — Financial dossier presentation and disclosure requirements
from runtime import KINDS, PROGRAMMES, BUILDINGS

PARTIES = ('Western_Autocracy','conservatism','liberalism','socialism','communist_state','anarchist_communism',
           'Conservative','Autocracy','Mod_Vilayat_e_Faqih','Vilayat_e_Faqih','Kingdom','Caliphate',
           'Neutral_Muslim_Brotherhood','Neutral_Autocracy','Neutral_conservatism','oligarchism',
           'Neutral_Libertarian','Neutral_green','neutral_Social','Neutral_Communism','Nat_Populism',
           'Nat_Fascism','Nat_Autocracy','Monarchist')


def extend(data, loc, defined):
    data.update({
        'icsd_tab_2':'Correspondence',
        'icsd_detail_facts':'Provider: [?icsd_selected_actor.GetName]\nRecipient: [?icsd_selected_target.GetName]\nRecord: [icsd_selected_kind_L]\nStatus: [icsd_selected_state_L]',
        'icsd_extra_investment':'Region: [?icsd_selected_place.GetName]\nConstruction: [icsd_building] | Remaining levels: [?icsd_selected_size|0]\nRecorded project cost: $[?icsd_selected_amount|2] billion',
        'icsd_extra_assistance':'Programme: [icsd_programme]\nScale: [?icsd_selected_size|0] | Remaining term: [?icsd_selected_left|0] days',
        'icsd_extra_party':'Supported party: [icsd_party]\nRemaining term: [?icsd_selected_left|0] days',
        'icsd_extra_politics':'Supported party: [icsd_party]\nA political influence action has been recorded.',
        'icsd_extra_money':'Recorded amount: $[?icsd_selected_amount|2] billion\n[icsd_description]',
        'icsd_extra_subsidy':'Weekly funding: $[?icsd_selected_amount|3] billion',
        'icsd_extra_redacted':'Details: REDACTED\nRequires 60% civilian intelligence on [?icsd_selected_actor.GetName]\nor 50% network strength in [?icsd_selected_target.GetName].',
        'icsd_extra_assistance_redacted':'Programme: [icsd_programme] | Scale and term: REDACTED\nRequires 60% civilian intelligence on [?icsd_selected_actor.GetName]\nor 50% network strength in [?icsd_selected_target.GetName].',
        'icsd_more':'More actions','icsd_basic':'Basic actions','icsd_sources':'Sources',
        'icsd_sources_tt':'Own and received records are fully available. Public commitments identify their partners. Financial details require 60% civilian intelligence on the provider or 50% network strength in the recipient. Agency economic upgrades improve civilian intelligence. Networks must be established through existing operative missions.\n\nCurrent commitments are reviewed weekly. Foreign payments and political interference are recorded only when sufficient intelligence exists at the time. Later intelligence does not reveal earlier undiscovered payments. Previously discovered correspondence remains in the file. No records does not establish that no activity occurred.',
        'icsd_invest':'Foreign investment','icsd_assist':'Assistance programme','icsd_party_action':'Public political support',
        'icsd_politics':'Influence politics','icsd_aid':'Economic aid','icsd_subsidy':'Financial subsidies',
        'icsd_route_7':'Select a foreign state > Foreign Investment\nChoose the building and number of levels. The recipient answers the existing investment offer. Normal treasury and construction limits apply.',
        'icsd_route_8':'Diplomacy > Assistance Programme\nChoose the existing programme and scale. The recipient accepts or refuses. Review current programmes in the Cold War country view.',
        'icsd_route_9':'Cold War country view > Public Political Support\nChoose the actual party in the recipient country. Existing programme costs, access conditions and recipient controls apply.',
        'icsd_route_10':'Country view > Influence > Manipulate Politics\nUses the existing political-power cost and influence effects. The native target-party rules apply.',
        'icsd_route_11':'Country view > Influence > Economic Aid\nChoose the existing aid amount. The normal aid procedure controls payment and recipient response.',
        'icsd_route_12':'Diplomacy > Grant Subsidies\nChoose weekly funding from your treasury. The recipient answers the normal offer. Cancel through the existing subsidy controls.',
        'icsd_desc_8':'An active foreign construction investment is recorded.',
        'icsd_desc_9':'An existing government assistance programme links these countries.',
        'icsd_desc_10':'An openly sponsored political campaign is recorded.',
        'icsd_desc_11':'A completed political influence action is recorded.',
        'icsd_desc_12':'An economic aid payment is recorded.',
        'icsd_desc_13':'An existing weekly financial subsidy is recorded.',
        'icsd_desc_6':'Trade correspondence between the two governments.',
        'icsd_desc_7':'Financial correspondence between the two governments.',
        'icsd_state_4':'Suspended','icsd_state_5':'Action recorded',
        'icsd_footer':'USA AND USSR ONLY | REVIEWED WEEKLY',
    })
    for i,name in KINDS.items():data[f'icsd_kind_{i}']=name
    for i,name in enumerate(PROGRAMMES,1):data[f'icsd_programme_{i}']=f'$mdcw_cw_prog_name_{i}$'
    for i,name in enumerate(BUILDINGS,1):data[f'icsd_building_{i}']='$'+name+'$'
    for i,name in enumerate(PARTIES):data[f'icsd_party_{i}']='[?icsd_selected_target.'+name+'_L]'
    for k,v in data.items():loc(k,v)
    scripts=[]
    for label,prefix,values in [('programme','icsd_programme_',range(1,9)),('building','icsd_building_',range(1,16)),('party','icsd_party_',range(24))]:
        scripts.append(defined('icsd_'+label,[(f'check_variable = {{ icsd_selected_type = {i} }}',prefix+str(i)) for i in values]))
    scripts.append(defined('icsd_more_label',[('check_variable = { icsd_actions_page = 2 }','icsd_basic')],'icsd_more'))
    scripts.append(defined('icsd_extra',[
        ('check_variable = { icsd_selected_kind = 9 } check_variable = { icsd_selected_detail = 0 }','icsd_extra_assistance_redacted'),
        ('check_variable = { icsd_selected_kind = 8 } check_variable = { icsd_selected_detail = 0 }','icsd_extra_redacted'),
        ('check_variable = { icsd_selected_kind = 8 }','icsd_extra_investment'),
        ('check_variable = { icsd_selected_kind = 9 }','icsd_extra_assistance'),
        ('check_variable = { icsd_selected_kind = 10 }','icsd_extra_party'),
        ('check_variable = { icsd_selected_kind = 11 }','icsd_extra_politics'),
        ('OR = { check_variable = { icsd_selected_kind = 7 } check_variable = { icsd_selected_kind = 12 } }','icsd_extra_money'),
        ('check_variable = { icsd_selected_kind = 13 }','icsd_extra_subsidy'),
    ]+[(f'check_variable = {{ icsd_selected_kind = {i} }}',f'icsd_known_{i}') for i in range(1,6)],'icsd_extra_default'))
    loc('icsd_extra_default','[icsd_description]')
    return scripts
