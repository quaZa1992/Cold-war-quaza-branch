# IMPERIA COLD WAR — COMECON human-only decisions and passive site selection
from build import *

def compile_decisions():
    loc('cc_decisions','Council for Mutual Economic Assistance')
    loc('cc_decisions_desc','Joint investment and technical co-operation. Contributions are offered by the financing governments. The secretariat submits a completed draft for Council review before signature. Passive recipients need no separate delegation signature.')
    write('common/decisions/categories/ICW_COMECON.txt',MARK+' human agreement decisions\ncc_decisions = { icon = GFX_cc_emblem allowed = { always = yes } visible = { is_ai = no OR = { cc_access = yes has_country_flag = cc_invited } } }')
    out=[MARK+' no autonomous AI choices','cc_decisions = {']
    loc('cc_invite','Invite [FROM.GetName] to COMECON');loc('cc_invite_desc','Offer the government full Council membership. Admission requires its acceptance.')
    out.append('cc_invite = { icon = GFX_cc_emblem target_array = global.countries target_root_trigger = { cc_secretariat = yes check_variable = { global.cc_members^num < 32 } } target_trigger = { FROM = { is_ai = no exists = yes NOT = { cc_member_country = yes } NOT = { COLDWAR_SOV_is_union_republic = yes } NOT = { has_country_flag = cc_invited } } } complete_effect = { if = { limit = { cc_secretariat = yes FROM = { is_ai = no exists = yes NOT = { cc_member_country = yes } NOT = { COLDWAR_SOV_is_union_republic = yes } } } FROM = { set_country_flag = cc_invited } cc_touch = yes } } ai_will_do = { factor = 0 } }')
    for action,label in [('accept','Accept COMECON Membership'),('refuse','Decline COMECON Membership')]:
        loc('cc_membership_'+action,label);loc('cc_membership_'+action+'_desc','Membership permits participation in separately financed agreements. It does not commit national funds automatically.')
        grant='add_ideas = cc_member if = { limit = { NOT = { is_in_array = { array = global.cc_members value = THIS } } } add_to_array = { global.cc_members = THIS } } if = { limit = { NOT = { is_in_array = { array = global.cc_hosts value = THIS } } } add_to_array = { global.cc_hosts = THIS } } capital_scope = { '+' '.join(f'set_variable = {{ PREV.cc_{s}_site1 = THIS.id }}' for s in range(1,5))+' }' if action=='accept' else ''
        out.append(f'cc_membership_{action} = {{ icon = GFX_cc_emblem visible = {{ is_ai = no has_country_flag = cc_invited NOT = {{ cc_member_country = yes }} }} complete_effect = {{ if = {{ limit = {{ is_ai = no has_country_flag = cc_invited NOT = {{ cc_member_country = yes }} NOT = {{ COLDWAR_SOV_is_union_republic = yes }} check_variable = {{ global.cc_members^num < 32 }} }} {grant} clr_country_flag = cc_invited cc_update_authority = yes cc_touch = yes }} }} ai_will_do = {{ factor = 0 }} }}')
    loc('cc_annex','Ratify Military-Technical Co-operation Annex');loc('cc_annex_desc','Authorise participation in agreed industrial programmes affecting military production. This does not establish a military alliance.')
    out.append('cc_annex = { icon = GFX_decision_generic_factory visible = { cc_human_member = yes NOT = { has_country_flag = cc_military_annex } } complete_effect = { if = { limit = { cc_human_member = yes } set_country_flag = cc_military_annex cc_touch = yes } } ai_will_do = { factor = 0 } }')
    for s in range(1,5):
        for action,label in [('approve','Approve Agreement'),('decline','Decline Agreement'),('local_confirm','Confirm Local Programme Implementation')]:
            loc(f'cc_{s}_{action}',f'File {s}: '+label);loc(f'cc_{s}_{action}_desc','Review the current sealed terms before signing. Financing, national sites and programme services form one agreement.')
            fn=f'cc_{s}_confirm_local' if action=='local_confirm' else f'cc_{s}_{action}'
            voter=f'cc_{s}_receiving_country = yes NOT = {{ cc_{s}_voter = yes }}' if action=='local_confirm' else f'cc_{s}_voter = yes'
            out.append(f'cc_{s}_{action} = {{ icon = GFX_cc_emblem visible = {{ is_ai = no {voter} check_variable = {{ global.cc_{s}_phase > 0 }} check_variable = {{ global.cc_{s}_phase < 4 }} }} available = {{ cc_{s}_seen_terms = yes }} complete_effect = {{ cc_{s}_preview_all = yes hidden_effect = {{ {fn} = yes }} }} ai_will_do = {{ factor = 0 }} }}')
        for site in range(1,4):
            cases=[]
            for i,(p,o) in enumerate(OFFERS,1):
                for t in range(3):
                    for host in (True,False):
                        if offer_effects(p,o,t,host)[2]>=site:
                            role=cv('THIS.id','=',f'global.cc_{s}_host');role=role if host else 'NOT = { '+role+' }'
                            cases.append(f'AND = {{ {cv(f"global.cc_{s}_offer","=",i)} {cv(f"global.cc_{s}_tier","=",t+1)} {role} }}')
            needed='always = yes' if site==1 else 'OR = { '+' '.join(cases)+' }'
            key=f'cc_{s}_site' if site==1 else f'cc_{s}_site_{site}'
            loc(key,f'File {s}, Site {site}: Select [FROM.GetName]');loc(key+'_desc','Select a national implementation site before the draft is sealed for Council review.')
            out.append(f'''{key} = {{ icon = GFX_decision_generic_factory state_target = yes on_map_mode = map_and_decisions_view
target_root_trigger = {{ is_ai = no cc_{s}_receiving_country = yes check_variable = {{ cc_view_slot = {s} }} check_variable = {{ global.cc_{s}_phase = 0 }} {needed} }}
target_trigger = {{ FROM = {{ is_owned_by = ROOT is_controlled_by = ROOT }} }}
complete_effect = {{ if = {{ limit = {{ is_ai = no cc_{s}_receiving_country = yes check_variable = {{ global.cc_{s}_phase = 0 }} {needed} FROM = {{ is_owned_by = ROOT is_controlled_by = ROOT }} }} set_variable = {{ cc_{s}_site{site} = FROM.id }} cc_{s}_revise = yes }} }} ai_will_do = {{ factor = 0 }} }}''')
            key=f'cc_{s}_passive_site_{site}';loc(key,f'File {s}, Passive Site {site}: Select [FROM.GetName]');loc(key+'_desc','Select an agreed site in a passive recipient country. Ownership, control, sector and capacity are checked before ratification and delivery.')
            out.append(f'''{key} = {{ icon = GFX_decision_generic_factory state_target = yes on_map_mode = map_and_decisions_view
target_root_trigger = {{ cc_{s}_editable = yes check_variable = {{ cc_view_slot = {s} }} }}
target_trigger = {{ FROM = {{ owner = {{ is_ai = yes cc_{s}_receiving_country = yes {needed} }} }} }}
complete_effect = {{ if = {{ limit = {{ cc_{s}_editable = yes FROM = {{ owner = {{ is_ai = yes cc_{s}_receiving_country = yes {needed} }} }} }} FROM = {{ owner = {{ set_variable = {{ cc_{s}_site{site} = PREV.id }} }} }} cc_{s}_revise = yes }} }} ai_will_do = {{ factor = 0 }} }}''')
    out.append('}');write('common/decisions/ICW_COMECON.txt','\n'.join(out))
