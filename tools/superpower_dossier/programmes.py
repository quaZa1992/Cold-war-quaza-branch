# IMPERIA COLD WAR — Consented scientific, commercial and regional treaty programmes
"""Programme clauses are part of the signed paper, never inferred from focus completion."""
from decimal import Decimal
from treaties import TREATIES

PROGRAMMES = {
    1: dict(slot=9, label='Scientific cooperation', title='American-Soviet Scientific Cooperation',
            protocol='investment', setup='.0003', weekly='.00002',
            usa={'research_speed_factor':'.03','bureaucracy_cost_multiplier_modifier':'.01'},
            sov={'research_speed_factor':'.03','bureaucracy_cost_multiplier_modifier':'.01'}),
    2: dict(slot=8, label='Civilian supply', title='Soviet Export Programme', partner='American Civilian Supply Agreement',
            protocol='trade', setup='.001', weekly='.00002',
            usa={'foreign_influence_modifier':'.03','bureaucracy_cost_multiplier_modifier':'.01'},
            sov={'consumer_goods_factor':'-.03','stability_factor':'.02','bureaucracy_cost_multiplier_modifier':'.01'}),
    3: dict(slot=1, label='Strategic consultations', title='Strategic Consultations Programme',
            protocol='reserve_limit', setup='.0005', weekly='.00002',
            usa={'stability_factor':'.02','foreign_influence_defense_modifier':'.05','bureaucracy_cost_multiplier_modifier':'.01'},
            sov={'stability_factor':'.02','foreign_influence_defense_modifier':'.05','bureaucracy_cost_multiplier_modifier':'.01'}),
    4: dict(slot=10, label='Regional cooperation', title='Negotiated Regional Understanding', partner='American Economic Cooperation Programme',
            protocol='regional', setup='.0005', weekly='.00005', transfer=True,
            usa={'foreign_influence_modifier':'.05'},
            sov={'production_speed_buildings_factor':'.05','research_speed_factor':'.02','bureaucracy_cost_multiplier_modifier':'.01'}),
}
MODIFIERS = {
    'research_speed_factor':('Research Speed',False),
    'bureaucracy_cost_multiplier_modifier':('Bureaucracy Cost',True),
    'foreign_influence_modifier':('Foreign Influence',False),
    'consumer_goods_factor':('Consumer Goods Factor',True),
    'stability_factor':('Stability',False),
    'foreign_influence_defense_modifier':('Foreign Influence Defense',False),
    'production_speed_buildings_factor':('Construction Speed',False),
}

def number(value):
    text=format(Decimal(str(value)).normalize(),'f')
    assert '.' not in text or len(text.split('.')[1])<=5
    return text

def calculate(variable,percent,basis='gdp_total',temporary=False):
    kind='temp_variable' if temporary else 'variable'
    return f'set_{kind} = {{ {variable} = {basis} }}\nmultiply_{kind} = {{ {variable} = {number(percent)} }}\ndivide_{kind} = {{ {variable} = 100 }}'

def programme_terms(pid,removing=False):
    """Native non-transactional rows; caller owns effect_tooltip."""
    p=PROGRAMMES[pid];rows=[]
    for tag,side in (('USA','usa'),('SOV','sov')):
        rows.append(f'{tag} = {{ '+('remove_ideas' if removing else 'add_ideas')+f' = icwt_programme_{pid}_{side}')
        for key,value in p[side].items():
            rows.append(f'add_to_variable = {{ icwt_preview_{key} = {number(-Decimal(value) if removing else value)} tooltip = icwt_mod_{key}_tt }}')
        if not removing and not (p.get('transfer') and tag=='SOV'):
            setup=-Decimal(p['setup'])
            places=max(0,-setup.normalize().as_tuple().exponent)
            rows.append(f'add_to_variable = {{ icwt_preview_setup = {number(setup)} tooltip = icwt_gdp_setup_{places}_tt }}')
            rows.append(calculate('treasury_change',setup,temporary=True)+'\nmodify_treasury_effect = yes')
        amount=Decimal(p['weekly'])*(1 if p.get('transfer') and tag=='SOV' else -1)*(-1 if removing else 1)
        donor=p.get('transfer') and tag=='SOV';basis='USA.gdp_total' if donor else 'gdp_total'
        rows.append(f'add_to_variable = {{ icwt_preview_weekly_pct = {number(amount)} tooltip = icwt_gdp_weekly_usa_tt }}' if donor else f'add_to_variable = {{ icwt_preview_weekly_pct = {number(amount)} tooltip = icwt_gdp_weekly_tt }}')
        rows.append(calculate('icwt_preview_weekly_amount',amount,basis,True))
        rows.append('add_to_variable = { icwt_preview_weekly = icwt_preview_weekly_amount tooltip = icwt_weekly_balance_tt }\n}')
    return '\n'.join(rows)

def extend(ef,tr,events,loc,mark):
    def get(rows,name):return next(x for x in rows if x.startswith(name+' = {')).split('\n',1)[1].rsplit('\n}',1)[0]
    def put(rows,name,body):
        assert body.count('{')==body.count('}'),name
        rows[:]=[x for x in rows if not x.startswith(name+' = {')]
        rows.append(name+' = {\n'+body+'\n}')
    def effect(name,body):put(ef,name,body)
    def trigger(name,body):put(tr,name,body)
    sanctions=' '.join(f'is_in_array = {{ array = imp_{kind}_sanc_{direction}_us value = SOV }}' for kind in ('dip','fin','eco','mil') for direction in ('on','by'))
    reverse=' '.join(f'is_in_array = {{ array = imp_{kind}_sanc_{direction}_us value = USA }}' for kind in ('dip','fin','eco','mil') for direction in ('on','by'))
    trigger('icwt_programme_relations',f'''country_exists = USA country_exists = SOV
USA = {{ NOT = {{ has_war_with = SOV }} NOT = {{ is_embargoing = SOV }} NOT = {{ OR = {{ {sanctions} }} }} }}
SOV = {{ NOT = {{ has_war_with = USA }} NOT = {{ is_embargoing = USA }} NOT = {{ OR = {{ {reverse} }} }} }}''')
    observed=['OR = { check_variable = { global.icwt_10_regional = 1 } check_variable = { global.icwt_10_regional = 2 } check_variable = { global.icwt_10_regional = 3 } }']
    for side,tag in (('usa','USA'),('sov','SOV')):
        target=f'global.icwt_10_{side}_target'
        observed.append(f'''check_variable = {{ {target} > 0 }}
var:{target} = {{
 exists = yes NOT = {{ tag = {tag} }}
 OR = {{ check_variable = {{ global.icwt_10_regional = 2 }} NOT = {{ has_attache_from = {tag} }} }}
 OR = {{ check_variable = {{ global.icwt_10_regional = 1 }} NOT = {{ has_volunteers_amount_from = {{ tag = {tag} count > 0 }} }} }}
}}''')
    trigger('icwt_programme_regional_observed','\n'.join(observed))
    edit=['OR = { check_variable = { icwt_edit_programme = 0 }'];pending=['OR = { check_variable = { global.icwt_p_programme = 0 }']
    for pid,p in PROGRAMMES.items():
        n=p['slot'];protocol=p['protocol']
        edit.append(f'AND = {{ check_variable = {{ icwt_edit_programme = {pid} }} check_variable = {{ icwt_template = {n} }} check_variable = {{ icwt_edit_{protocol} > 0 }} USA = {{ has_country_flag = icwt_programme_{pid}_unlocked }} }}')
        pending.append(f'AND = {{ check_variable = {{ global.icwt_p_programme = {pid} }} check_variable = {{ global.icwt_pending = {n} }} check_variable = {{ global.icwt_p_{protocol} > 0 }} USA = {{ has_country_flag = icwt_programme_{pid}_unlocked }} }}')
        trigger(f'icwt_programme_{pid}_active',f'''check_variable = {{ global.icwt_{n}_programme = {pid} }} check_variable = {{ global.icwt_{n}_{protocol} > 0 }}
check_variable = {{ global.icwt_{n}_revision > 0 }}
OR = {{ check_variable = {{ global.icwt_{n}_end = 0 }} check_variable = {{ global.num_days < global.icwt_{n}_end }} }}
USA = {{ has_country_flag = icwt_member_{n} check_variable = {{ icwt_programme_{pid}_receipt = global.icwt_{n}_revision }} }}
SOV = {{ has_country_flag = icwt_member_{n} check_variable = {{ icwt_programme_{pid}_receipt = global.icwt_{n}_revision }} }}
icwt_programme_relations = yes'''+ ('\nicwt_programme_regional_observed = yes' if pid==4 else ''))
        effect(f'icwt_programme_terms_{pid}',programme_terms(pid))
        effect(f'icwt_programme_preview_{pid}','effect_tooltip = {\n'+programme_terms(pid)+'\n}')
    trigger('icwt_programme_edit_valid','\n'.join(edit+['}']))
    trigger('icwt_programme_pending_valid','\n'.join(pending+['}']))
    trigger('icwt_edit_valid',get(tr,'icwt_edit_valid')+'\nicwt_programme_edit_valid = yes')
    # Draft selection toggles only the programme applicable to this instrument.
    toggle='if = { limit = { icwt_core = yes NOT = { icwt_pending = yes } }\nif = { limit = { check_variable = { icwt_edit_programme > 0 } } clear_variable = icwt_edit_programme }'
    for pid,p in PROGRAMMES.items():
        toggle+=f'\nelse_if = {{ limit = {{ check_variable = {{ icwt_template = {p["slot"]} }} USA = {{ has_country_flag = icwt_programme_{pid}_unlocked }} }} set_variable = {{ icwt_edit_programme = {pid} }} }}'
    effect('icwt_cycle_programme',toggle+'\nclear_variable = icwt_review_revision icwt_touch = yes }')
    # Setup amount is a share of current GDP at conclusion, not a frozen nominal invoice.
    quote=['set_variable = { icwt_programme_setup = 0 }']
    for pid,p in PROGRAMMES.items():
        quote.append(f'if = {{ limit = {{ check_variable = {{ global.icwt_p_programme = {pid} }}'+(' tag = USA' if p.get('transfer') else '')+' }\n'+calculate('icwt_programme_setup',p['setup'])+'\n}')
    effect('icwt_programme_quote_setup','\n'.join(quote))
    trigger('icwt_programme_setup_affordable','''OR = {
 AND = { tag = SOV check_variable = { global.icwt_p_programme = 4 } }
 AND = { check_variable = { gdp_total > 0 } check_variable = { var = treasury value = icwt_programme_setup compare = greater_than_or_equals } }
}''')
    pay=[]
    for pid,p in PROGRAMMES.items():
        pay.append(f'''if = {{ limit = {{ check_variable = {{ global.icwt_p_programme = {pid} }} NOT = {{ check_variable = {{ icwt_programme_{pid}_receipt = global.icwt_{p['slot']}_revision }} }} }}
set_variable = {{ icwt_programme_{pid}_receipt = global.icwt_{p['slot']}_revision }}
if = {{ limit = {{ check_variable = {{ icwt_programme_setup > 0 }} }} set_temp_variable = {{ treasury_change = icwt_programme_setup }} multiply_temp_variable = {{ treasury_change = -1 }} modify_treasury_effect = yes }}
}}''')
    effect('icwt_programme_pay_setup','\n'.join(pay))
    for n in range(1,len(TREATIES)+1):
        preflight=get(ef,f'icwt_preflight_{n}')+'''
if = { limit = { check_variable = { global.icwt_p_programme > 0 } }
 if = { limit = { OR = { NOT = { icwt_programme_pending_valid = yes } NOT = { icwt_programme_relations = yes } } } set_variable = { global.icwt_preflight = 0 } }
 USA = { icwt_programme_quote_setup = yes if = { limit = { NOT = { icwt_programme_setup_affordable = yes } } set_variable = { global.icwt_preflight = 0 } } }
 SOV = { icwt_programme_quote_setup = yes if = { limit = { NOT = { icwt_programme_setup_affordable = yes } } set_variable = { global.icwt_preflight = 0 } } }
}'''
        effect(f'icwt_preflight_{n}',preflight)
        sign=get(ef,f'icwt_sign_{n}')
        for tag in ('USA','SOV'):
            sign=sign.replace(f'{tag} = {{ icwt_join_{n} = yes',f'{tag} = {{ icwt_programme_pay_setup = yes icwt_join_{n} = yes',1)
        effect(f'icwt_sign_{n}',sign)
    refresh=[]
    for pid,p in PROGRAMMES.items():
        ensure=' '.join(f'if = {{ limit = {{ country_exists = {tag} }} {tag} = {{ if = {{ limit = {{ NOT = {{ has_idea = icwt_programme_{pid}_{side} }} }} add_ideas = icwt_programme_{pid}_{side} }} }} }}' for tag,side in (('USA','usa'),('SOV','sov')))
        remove=' '.join(f'{tag} = {{ remove_ideas = icwt_programme_{pid}_{side} }}' for tag,side in (('USA','usa'),('SOV','sov')))
        if pid==4:
            remove='USA = { if = { limit = { NOT = { COLDWAR_USA_KS_td_regional_active = yes } } remove_ideas = icwt_programme_4_usa } } SOV = { remove_ideas = icwt_programme_4_sov }'
        refresh.append(f'if = {{ limit = {{ icwt_programme_{pid}_active = yes }} {ensure} }} else = {{ {remove} }}')
    refresh.append('if = { limit = { country_exists = USA USA = { COLDWAR_USA_KS_td_regional_active = yes } } USA = { if = { limit = { NOT = { has_idea = icwt_programme_4_usa } } add_ideas = icwt_programme_4_usa } } }')
    effect('icwt_programmes_refresh','\n'.join(refresh))
    effect('icwt_refresh',get(ef,'icwt_refresh')+'\nicwt_programmes_refresh = yes')
    fiscal=['set_variable = { icwt_weekly_expense = 0 } set_variable = { icwt_weekly_income = 0 }',*(f'set_variable = {{ icwt_weekly_programme_{pid} = 0 }}' for pid in PROGRAMMES),'if = { limit = { OR = { tag = USA tag = SOV } } icwt_programmes_refresh = yes }']
    for pid,p in PROGRAMMES.items():
        for tag in ('USA','SOV'):
            kind='income' if p.get('transfer') and tag=='SOV' else 'expense'
            basis='USA.gdp_total' if p.get('transfer') and tag=='SOV' else 'gdp_total'
            fiscal.append(f'if = {{ limit = {{ tag = {tag} icwt_programme_{pid}_active = yes }}\n'+calculate(f'icwt_weekly_programme_{pid}',p['weekly'],basis)+'\nadd_to_variable = { icwt_weekly_'+kind+f' = icwt_weekly_programme_{pid}'+' }\n}')
    fiscal.append('if = { limit = { tag = USA COLDWAR_USA_KS_td_regional_active = yes }\n'+calculate('icwt_weekly_programme_4',PROGRAMMES[4]['weekly'])+'\n}')
    effect('icwt_programme_fiscal','\n'.join(fiscal))
    # Preview the existing reversible treaty relief, never another executable focus reward.
    for n in range(1,len(TREATIES)+1):
        effect(f'icwt_tension_terms_{n}',f'''if = {{ limit = {{
has_global_flag = mdcw_cw_initialized check_variable = {{ global.icwt_relief < 5 }} check_variable = {{ global.mdcw_cw_tension > 0 }}
check_variable = {{ global.icwt_{n}_members^num < 1 }}
NOT = {{ AND = {{ USA = {{ has_country_flag = icwt_member_{n} }} SOV = {{ has_country_flag = icwt_member_{n} }} }} }}
NOT = {{ AND = {{ check_variable = {{ global.icwt_pending = {n} }} check_variable = {{ global.icwt_p_addendum = 1 }} }} }}
}}
set_temp_variable = {{ icwt_preview_tension_delta = global.mdcw_cw_tension }}
clamp_temp_variable = {{ var = icwt_preview_tension_delta min = 0 max = 1 }} multiply_temp_variable = {{ icwt_preview_tension_delta = -1 }}
add_to_variable = {{ icwt_preview_tension = icwt_preview_tension_delta tooltip = icwt_tension_tt }}
}}''')
    # Open the relevant existing paper without signing, resetting or replacing it.
    for n in (7,9,8,1,10):
        pid=next((pid for pid,p in PROGRAMMES.items() if p['slot']==n),0)
        opening=['if = { limit = { tag = USA IMP_is_1970_scenario = yes }']
        if pid:opening.append(f'set_country_flag = icwt_programme_{pid}_unlocked')
        opening.append('icsd_open = yes\nif = { limit = { icwt_pending = yes }')
        opening += [f'if = {{ limit = {{ check_variable = {{ global.icwt_pending = {k} }} }} icwt_review_{k} = yes }}' for k in range(1,len(TREATIES)+1)]
        opening.append(f'}} else_if = {{ limit = {{ check_variable = {{ global.icwt_{n}_members^num > 0 }} }} set_variable = {{ icsd_tab = 3 }} set_variable = {{ icwt_register = 1 }} set_variable = {{ icwt_template = {n} }} }} else = {{ set_variable = {{ icsd_tab = 2 }} icwt_edit_{n} = yes')
        if pid:opening.append(f'set_variable = {{ icwt_edit_programme = {pid} }}')
        opening.append('}\nicwt_display = yes icwt_touch = yes\n}')
        effect(f'icwt_initiative_{n}','\n'.join(opening))
        preview=['effect_tooltip = { custom_effect_tooltip = icwt_if_accept_tt']
        preview.append(f'if = {{ limit = {{ NOT = {{ AND = {{ USA = {{ has_country_flag = icwt_member_{n} }} SOV = {{ has_country_flag = icwt_member_{n} }} }} }} }}')
        for tag in ('USA','SOV'):
            other='SOV' if tag=='USA' else 'USA'
            preview.append(f'{tag} = {{ add_ideas = icwt_spirit_{n}')
            if n==9:preview.append('custom_effect_tooltip = icwt_investment_1_effect')
            if n==8:preview.append(f'add_opinion_modifier = {{ target = {other} modifier = icwt_trade_2 }} add_opinion_modifier = {{ target = {other} modifier = icwt_relations_2 }}')
            if n==1:preview.append('icwt_preview_opening_limit_1 = yes')
            if n==10:
                preview.append('custom_effect_tooltip = icwt_regional_concession_tt')
                preview.append('custom_effect_tooltip = icwt_deployed_volunteer_cost_tt')
            preview.append('}')
        preview.append('}')
        if pid:preview.append(programme_terms(pid))
        preview.append(f'icwt_tension_terms_{n} = yes')
        preview.append('}')
        effect(f'icwt_focus_preview_{n}','\n'.join(preview))
    selected='\n'.join(f'if = {{ limit = {{ check_variable = {{ ROOT.icwt_show_programme = {pid} }} }} icwt_programme_terms_{pid} = yes }}' for pid in PROGRAMMES)
    for pid,p in PROGRAMMES.items():
        effect(f'icwt_programme_remove_terms_{pid}',programme_terms(pid,True))
        selected+=f'\nif = {{ limit = {{ check_variable = {{ ROOT.icwt_show_addendum = 1 }} check_variable = {{ ROOT.icwt_show_programme = 0 }} check_variable = {{ ROOT.icwt_template = {p["slot"]} }} check_variable = {{ global.icwt_{p["slot"]}_programme = {pid} }} }} icwt_programme_remove_terms_{pid} = yes }}'
    effect('icwt_programme_terms_selected',selected)
    pending_preview='\n'.join(f'if = {{ limit = {{ check_variable = {{ global.icwt_p_programme = {pid} }} }} icwt_programme_terms_{pid} = yes }}' for pid in PROGRAMMES)
    for pid,p in PROGRAMMES.items():
        pending_preview+=f'\nif = {{ limit = {{ check_variable = {{ global.icwt_p_addendum = 1 }} check_variable = {{ global.icwt_p_programme = 0 }} check_variable = {{ global.icwt_pending = {p["slot"]} }} check_variable = {{ global.icwt_{p["slot"]}_programme = {pid} }} }} icwt_programme_remove_terms_{pid} = yes }}'
    effect('icwt_programme_preview_pending','effect_tooltip = {\n'+pending_preview+'\n}')
    # The notification's review option also shows its exact bilateral programme terms.
    for n in range(1,len(TREATIES)+1):
        for i,event in enumerate(events):
            if event.startswith(f'country_event = {{ id = icwt.{n} '):events[i]=event.replace('desc = icwt_invitation_desc','desc = icwt_pending_paper_desc').replace(f'icwt_review_{n} = yes ai_chance',f'icwt_programme_preview_pending = yes icwt_review_{n} = yes ai_chance')
    descriptions={
      1:'American and Soviet research institutions maintain civilian exchanges and joint scientific work. The delegations fund these commitments through their investment agreement.',
      2:'American exporters and Soviet purchasing agencies maintain a civilian supply programme under their commercial accord. The arrangement sustains economic access while each government funds its own commitments.',
      3:'The American and Soviet delegations maintain strategic consultations alongside the agreed production restraint. Diplomatic cooperation supports domestic confidence while verification and administration require continuing resources.',
      4:'Washington supports civilian economic cooperation in return for the accepted withdrawal of the two governments\' own military missions from their named recipients. Local governments retain responsibility for their own conflicts.',
    }
    for pid,p in PROGRAMMES.items():
        for side in ('usa','sov'):
            key=f'icwt_programme_{pid}_{side}';loc(key,p.get('partner',p['title']) if side=='sov' else p['title'])
            incoming=p.get('transfer') and side=='sov';basis='US GDP' if incoming else 'current GDP';sign='+' if incoming else '-';colour='G' if incoming else 'R'
            balance=f'Weekly programme balance: §{colour}{sign}{number(p["weekly"])}%§! of {basis} per week (§{colour}{sign}$[?icwt_weekly_programme_{pid}|5] billion/week§!).'
            if pid==4 and side=='usa':balance='Per active regional agreement: §R-0.00005%§! of current GDP per week (§R-$[?icwt_weekly_programme_4|5] billion/week§!).'
            continuation='Benefits and funding require continuing joint participation, the agreed protocol, peace and normal bilateral economic relations.'
            if pid==4:continuation+=' Cooperation and funding pause if either government returns a covered military mission to its named recipient. They resume after its withdrawal.'
            loc(key+'_desc',descriptions[pid]+'\n\n'+balance+'\n\n'+continuation)
    for key,(label,negative) in MODIFIERS.items():loc('icwt_mod_'+key+'_tt',label+': $RIGHT|'+('-' if negative else '+')+'=%$')
    for places in range(6):loc('icwt_gdp_setup_'+str(places)+'_tt','Treasury: $RIGHT|+='+str(places)+'$% of current GDP')
    loc('icwt_gdp_weekly_tt','Weekly programme balance: $RIGHT|+=5$% of current GDP per week')
    loc('icwt_gdp_weekly_usa_tt','Weekly programme balance: $RIGHT|+=5$% of US GDP per week')
    loc('icwt_weekly_balance_tt','Weekly programme balance: $RIGHT|+=5$ billion/week')
    loc('icwt_tension_tt','Cold War Tension: $RIGHT|-=0$ points')
    loc('icwt_if_accept_tt','If they accept:')
    loc('icwt_regional_concession_tt','Recall own military attache and volunteers from the named mission recipient.')
    loc('icwt_deployed_volunteer_cost_tt','If volunteers are deployed: Political Power §R-50§!; Command Power §R-15§!.')
    ideas=[]
    for pid,p in PROGRAMMES.items():
        for side in ('usa','sov'):
            mods=' '.join(key+' = '+number(value) for key,value in p[side].items())
            ideas.append(f'icwt_programme_{pid}_{side} = {{ picture = international_treaty2 allowed = {{ always = no }} allowed_civil_war = {{ always = no }} removal_cost = -1 modifier = {{ {mods} }} }}')
    from programme_addenda import extend as addenda
    addenda(ef,tr,events,loc)
    return ideas
