# IMPERIA COLD WAR — Native diplomatic recognition and UN membership.
# IMPERIA COLD WAR — DDR controls and permanent political dossier access
"""GER owns the simulation; DDR owns its payments, UI state and native politics."""
from pathlib import Path
import sys
from cw_lib import player_text, P, LOC, L, fmt

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'spain_1970_v2'))
from script_ast import parse, first, emit

E=P+'_east'
R=P+'_rv'
MARK='# IMPERIA COLD WAR — Shared German dossier, East Berlin perspective\n'
DOMESTIC={'intershop','koko','border_regime','stasi_sweep','consumer_imports','reform_course'}
OFFENSIVE={'raise_exchange','transit_checks','tighten_border','hva_offensive','close_transit'}
KEYS=('nva_alert_up','nva_alert_down','raise_exchange','transit_checks','tighten_border',
      'hva_offensive','recognition_drive','goodwill','ask_credit','close_transit',
      'intershop','koko','border_regime','stasi_sweep','consumer_imports','reform_course','propose_unity','unity_position')
TERMS={
 'nva_alert_up':'0 PP / 30 days\nNVA alert +1 / Pressure +5 / Stability -1%',
 'nva_alert_down':'0 PP / 30 days\nNVA alert -1 / Climate +2',
 'raise_exchange':'25 PP / 2 initiative / 365 days\nShortage -3 / Exit pressure +1 / Climate -6',
 'transit_checks':'25 PP / 2 initiative / 180 days\nBerlin access -5 / Pressure +12 / Climate -5',
 'tighten_border':'25 PP / 2 initiative / 365 days\nBorder lever +1 / Exit pressure -3 / Pressure +8',
 'hva_offensive':'25 PP / 2 initiative / 180 days\nPenetration +5 / Federal counter-intelligence remains active',
 'recognition_drive':'200 PP / 365 days\nRecognition requests to UN member states',
 'goodwill':'25 PP / 2 initiative / 180 days\nClimate +6 / Border and exchange levers -1',
 'ask_credit':'25 PP / 720 days\nRequest only; Bonn decides on the credit',
 'close_transit':'50 PP / 3 initiative / 730 days\nStarts a Transit Crisis',
 'intershop':'40 PP / 365 days\nShortage -4 / Media reach +2 / Opposition +1',
 'koko':'50 PP / 540 days\nShortage -6 / Dependence on Bonn +3',
 'border_regime':'50 PP / 365 days\nExit pressure -5 / SED control +3',
 'stasi_sweep':'50 PP / 365 days\nOpposition -5 / SED control +2 / Media reach +1',
 'consumer_imports':'30 PP / 365 days\nExit pressure -3 / Shortage +5 / Stability +2%',
 'reform_course':'75 PP / Once\nExit pressure -6 / SED control -6 / Opposition +3',
 'propose_unity':'100 PP / 3 initiative\nBonn must accept before chapter talks begin',
 'unity_position':'0 PP / 30 days\nReview the DDR position on the current chapter',
}


def block(name,body):return name+' = {\n'+body+'\n}\n'
def iff(gate,body):return block('if','limit = { '+gate+' }\n'+body)


def catalogue():
    import decisions
    out={}
    for category in (decisions.WP,decisions.DR):
        for raw in decisions.DECISIONS[category]:
            did,op,node=parse(raw)[0]
            key=did.removeprefix(P+'_dec_ddr_')
            if key not in KEYS:continue
            out[key]=dict(id=did,body=node,cost=int(first(node,'cost','0')),
                          cooldown=int(first(node,'days_re_enable','0')),
                          once=first(node,'fire_only_once')=='yes')
    if set(out)!=set(KEYS):raise ValueError('Missing DDR action source '+str(set(KEYS)-set(out)))
    return out


def clean(rows):
    # The DDR view consumes the border snapshot. Refreshing another view must
    # never request an additional division scan or execute a monthly tick.
    return [(k,o,clean(v) if isinstance(v,list) else v) for k,o,v in rows if k not in (R+'_gui_refresh',R+'_set_stage_modifiers')]


def triggers():
    access='original_tag = DDR tag = DDR IMP_is_1970_scenario = yes'
    active=f'''original_tag = DDR
tag = DDR
IMP_is_1970_scenario = yes
country_exists = GER
country_exists = DDR
has_country_flag = {P}_ddr_initialized
GER = {{ has_country_flag = cwgg_initialized has_country_flag = {P}_initialized }}
NOT = {{ has_global_flag = {P}_unity_achieved }}
'''
    out=block(E+'_access',access)+block(E+'_domestic_active',access+'\nhas_country_flag = '+P+'_ddr_initialized')+block(E+'_active',active)
    for key,row in catalogue().items():
        node=row['body']
        entry=E+('_domestic_active' if key in DOMESTIC else '_active')
        required='\n'.join((entry+' = yes',emit(first(node,'visible',[])),emit(first(node,'available',[]))))
        if key=='propose_unity':
            # Original admission helper includes the price; native decisions
            # have already paid when the transactional body rechecks eligibility.
            required=f'{E}_active = yes\nGER = {{ {P}_uni_ready = yes check_variable = {{ cwgg_init_ddr > 2 }} }}'
        if key in ('border_regime','stasi_sweep','tighten_border','hva_offensive','reform_course'):
            required+='\nCOLDWAR_DDR_sed_governs = yes'
        if row['cooldown']:required+=f'\nNOT = {{ has_country_flag = cwgg_east_cd_{key} }}'
        if row['once']:required+=f'\nNOT = {{ has_country_flag = cwgg_east_done_{key} }}'
        # IMPERIA COLD WAR — Both German governments share the same 60-day offensive-order limit.
        if key in OFFENSIVE:
            required+='\ncustom_trigger_tooltip = { tooltip = COLDWAR_GER_1970_balance_offensive_ready NOT = { has_country_flag = cwgg_balance_offensive_cd } }'
        out+=block(E+'_req_'+key,required)
        out+=block(E+'_can_'+key,E+'_req_'+key+' = yes\nNOT = { has_political_power < '+str(row['cost'])+' }')
    for a in range(1,6):
        gate=f'{E}_active = yes\nNOT = {{ has_country_flag = cwgg_east_answer_cd }}\nGER = {{ check_variable = {{ cwgg_krise_typ > 0 }} check_variable = {{ cwgg_countdown = 0 }} }}'
        if a>2:gate+='\nGER = { check_variable = { cwgg_init_ddr > 0 } }'
        if a==4:gate+='\ncountry_exists = SOV'
        out+=block(E+'_can_answer_'+str(a),gate)
    out+=block(E+'_can_crisis_menu',f'{E}_active = yes\nNOT = {{ has_country_flag = cwgg_east_answer_cd }}\nGER = {{ check_variable = {{ cwgg_krise_typ > 0 }} check_variable = {{ cwgg_countdown = 0 }} }}')
    out+=block(E+'_can_unity_review',f'''{E}_active = yes
NOT = {{ has_country_flag = cwgg_east_unity_dialog }}
OR = {{
 {E}_can_propose_unity = yes
 AND = {{ {E}_can_unity_position = yes GER = {{ check_variable = {{ cwgg_u_cur > 0 }} check_variable = {{ cwgg_u_cur < 6 }} }} }}
}}''')
    return MARK+out


def effects(w):
    out=''
    for key,row in catalogue().items():
        body=clean(first(row['body'],'complete_effect'))
        code=emit(body)
        if key in OFFENSIVE:code+='\nset_country_flag = { flag = cwgg_balance_offensive_cd days = 60 }'
        if row['cooldown']:code+=f'\nset_country_flag = {{ flag = cwgg_east_cd_{key} days = {row["cooldown"]} }}'
        if row['once']:code+=f'\nset_country_flag = cwgg_east_done_{key}'
        code+=f'\nif = {{ limit = {{ country_exists = GER }} GER = {{ {R}_update_stage = yes }} }}\n{R}_sync_views = yes'
        out+=block(E+'_do_'+key,code)
        out+=block(E+'_act_'+key,iff(E+'_can_'+key+' = yes',f'add_political_power = -{row["cost"]}\n{E}_do_{key} = yes'))
        # A native decision already deducted its displayed PP price. Both paths
        # now share the same body and cooldown; a stale native order is refunded.
        native=iff(E+'_req_'+key+' = yes',E+'_do_'+key+' = yes')
        native+='else = { add_political_power = '+str(row['cost'])+' }\n'
        out+=block(E+'_native_'+key,native)
    for a in range(1,6):
        out+=block(E+'_act_answer_'+str(a),iff(E+'_can_answer_'+str(a)+' = yes',f'set_country_flag = {{ flag = cwgg_east_answer_cd days = 30 }}\nGER = {{ set_variable = {{ cwgg_ddr_wahl = {a} }} set_variable = {{ cwgg_ddr_order_ready = 1 }} {R}_sync_views = yes }}'))
    out+=block(E+'_act_crisis_menu',iff(E+'_can_crisis_menu = yes','country_event = { id = COLDWAR_GGR.200 }'))
    # Review opens the existing country-owned event; it never accepts a chapter
    # or ratification for the player. Repeated prompts are bounded for two days.
    review=f'set_country_flag = {{ flag = cwgg_east_unity_dialog days = 2 }}\n'
    review+=iff(E+'_can_propose_unity = yes',E+'_act_propose_unity = yes')
    review+='else = { '+E+'_act_unity_position = yes }\n'
    out+=block(E+'_act_unity_review',iff(E+'_can_unity_review = yes',review))
    # Presentation: no world scan, random roll, payment or simulation mutation.
    # IMPERIA COLD WAR — Domestic access survives a missing bilateral counterpart.
    empty='set_variable = { cwgg_g_east_marker = 104 }\n'
    empty+='\n'.join('set_variable = { '+bar['var']+' = -'+str(bar['w'])+' }' for bar in w.bars)
    empty+='\n'+'\n'.join('set_variable = { cwgg_g_east_t_'+str(i)+' = 1 }' for i in range(1,10))
    presentation=iff('country_exists = GER','\n'.join(w.refresh))+'else = {\n'+empty+'\n}\n'
    refresh=iff(E+'_access = yes\nis_ai = no',iff('has_country_flag = cwgg_east_open',presentation)+f'\n{E}_gui_touch = yes')
    refresh+=iff(E+'_access = no\nhas_country_flag = cwgg_east_open',f'clr_country_flag = cwgg_east_open\n{E}_gui_touch = yes')
    out+=block(E+'_gui_touch','add_to_variable = { cwgg_east_gui_dirty = 1 }')
    out+=block(E+'_gui_refresh',refresh)
    out+=block(E+'_open',iff(E+'_access = yes\nis_ai = no',f'if = {{ limit = {{ NOT = {{ has_country_flag = {P}_ddr_initialized }} }} {P}_initialize_ddr = yes }}\nset_country_flag = cwgg_east_open\nif = {{ limit = {{ OR = {{ check_variable = {{ cwgg_east_tab < 1 }} check_variable = {{ cwgg_east_tab > 5 }} }} }} set_variable = {{ cwgg_east_tab = 1 }} }}\n{E}_gui_refresh = yes'))
    for name,tab in (('relations',1),('domestic',5)):
        out+=block(E+'_open_'+name,iff(E+'_access = yes\nis_ai = no',f'set_variable = {{ cwgg_east_tab = {tab} }}\n{E}_open = yes'))
    out+=block(R+'_sync_views',iff('country_exists = GER',f'''GER = {{
 if = {{ limit = {{ is_ai = no }}
  if = {{ limit = {{ has_country_flag = cwgg_open }} {R}_gui_presentation = yes }}
  {R}_gui_touch = yes
 }}
}}''')+iff('country_exists = DDR',f'DDR = {{ {E}_gui_refresh = yes }}'))
    return MARK+out


def adapt_decisions(text):
    rows=parse(text);sources=catalogue()
    for cid,o,nodes in rows:
        for did,o,node in nodes:
            key=did.removeprefix(P+'_dec_ddr_')
            if key=='crisis_course':
                node[:]=[(k,op,v) for k,op,v in node if k not in ('available','complete_effect')]
                node.append(('available','=',parse(E+'_can_crisis_menu = yes')))
                node.append(('complete_effect','=',parse(E+'_act_crisis_menu = yes')))
                continue
            if key not in sources:continue
            original=first(node,'available',[])
            node[:]=[(k,op,v) for k,op,v in node if k not in ('available','complete_effect')]
            node.append(('available','=',parse(E+'_can_'+key+' = yes')))
            node.append(('complete_effect','=',parse(E+'_native_'+key+' = yes')))
    return MARK+emit(rows)+'\n'


def localise():
    for key,row in catalogue().items():
        did=row['id']
        details=LOC[did+'_desc']
        numeric=[]
        def visit(nodes):
            for k,o,v in nodes:
                if k=='custom_effect_tooltip' and v in LOC:numeric.append(LOC[v])
                if isinstance(v,list):visit(v)
        visit(first(row['body'],'complete_effect'))
        text=details+'\n\n'+TERMS[key]+'\n'+'\n'.join(dict.fromkeys(numeric))
        if key=='hva_offensive':text+='\nExisting federal counter-intelligence can expose or disrupt these networks.'
        if key=='reform_course':text+='\nWestern media reach +3.'
        if key in ('border_regime','stasi_sweep','tighten_border','hva_offensive','reform_course'):text+='\nRequires an SED government.'
        if row['cooldown']:text+=f'\nCooldown: {row["cooldown"]} days, shared with the corresponding decision.'
        if row['once']:text+='\nMay be enacted once.'
        L('cwgg_east_action_'+key+'_terms',TERMS[key])
        L('cwgg_east_action_'+key+'_tt',text)


def files():
    import gui
    import ddr_rivalry_ui
    import entry_ui
    localise()
    start=len(gui.SCRIPTED_LOC)
    w=ddr_rivalry_ui.window(gui.Window,gui.DT)
    loc_blocks=gui.SCRIPTED_LOC[start:];del gui.SCRIPTED_LOC[start:]
    loc='l_english:\n'+MARK+''.join(' '+k+':0 "'+player_text(v).replace('"','\\"').replace('\n','\\n')+'"\n' for k,v in sorted(LOC.items()) if k.startswith('cwgg_east_'))
    view='original_tag = DDR '+E+'_access = yes'
    # The small daily callback invalidates only an open human DDR view. It reads
    # current country values; the sole monthly GER simulation remains untouched.
    daily=block('on_actions',block('on_daily',block('effect',iff('original_tag = DDR is_ai = no has_country_flag = cwgg_east_open',E+'_gui_refresh = yes'))))
    decision=block('COLDWAR_DDR_1970_relations_category',block('COLDWAR_DDR_1970_open_relations',f'''icon = GFX_decision_negotiate_icon
cost = 0
visible = {{ {E}_access = yes }}
complete_effect = {{ {E}_open = yes }}
ai_will_do = {{ factor = 0 }}'''))
    L('cwgg_east_open_decision','Open the Inner-German Relations File')
    loc+=' COLDWAR_DDR_1970_relations_category:0 "Inner-German Relations"\n COLDWAR_DDR_1970_open_relations:0 "Open the Inner-German Relations File"\n COLDWAR_DDR_1970_open_relations_desc:0 "Review relations with Bonn and set the government\'s course."\n'
    return {
      'common/scripted_effects/COLDWAR_DDR_1970_relations.txt':effects(w),
      'common/scripted_triggers/COLDWAR_DDR_1970_relations.txt':triggers(),
      'interface/COLDWAR_DDR_1970_relations.gui':MARK+'guiTypes = {\n'+'\n'.join(w.gui()[1:]+entry_ui.ddr_gui())+'\n}\n',
      'interface/COLDWAR_DDR_1970_relations.gfx':MARK+'spriteTypes = { corneredTileSpriteType = { name = "GFX_cwgg_akte_bg_ddr" size = { x = 780 y = 700 } texturefile = "gfx/interface/cwger_1970/cwgg_akte_bg_ddr.dds" tilingCenter = yes effectFile = "gfx/FX/buttonstate_nodowneffect.lua" } }\n',
      'common/scripted_guis/COLDWAR_DDR_1970_relations.txt':MARK+'scripted_gui = {\n'+'\n'.join(w.scripted_gui(view)[1:]+entry_ui.ddr_scripted_gui())+'\n}\n',
      'common/scripted_localisation/COLDWAR_DDR_1970_relations.txt':MARK+'\n'.join(loc_blocks)+'\n',
      'common/on_actions/COLDWAR_DDR_1970_relations.txt':MARK+daily,
      'common/decisions/COLDWAR_DDR_1970_relations.txt':MARK+decision,
      'common/decisions/categories/COLDWAR_DDR_1970_relations.txt':MARK+block('COLDWAR_DDR_1970_relations_category','icon = GFX_decision_category_coms_cat\npriority = 211\nallowed = { original_tag = DDR }\nvisible = { '+E+'_access = yes is_ai = no }'),
      'localisation/english/COLDWAR_DDR_1970_relations_l_english.yml':loc,
    }


def write_art(root):
    import akte_sprites as art
    import gui_sprites
    old=dict(art.FONTS)
    try:
        if Path('C:/Windows/Fonts/cour.ttf').exists():
            art.FONTS.update(mono='C:/Windows/Fonts/cour.ttf',monob='C:/Windows/Fonts/courbd.ttf',sansb='C:/Windows/Fonts/arialbd.ttf',serifb='C:/Windows/Fonts/georgiab.ttf')
        rel='gfx/interface/cwger_1970/cwgg_akte_bg_ddr.dds'
        image=art.folder_bg('ddr')
        gui_sprites.write_dds(str(Path(root)/rel),image)
        return rel
    finally:art.FONTS.clear();art.FONTS.update(old)
