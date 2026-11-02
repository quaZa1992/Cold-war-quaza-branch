# IMPERIA COLD WAR — Native diplomatic recognition and UN membership.
# IMPERIA COLD WAR — East Berlin perspective without national trust meters
"""DDR-facing presentation for the shared Inner-German Relations minigame.

The host generator supplies the existing GUI DSL and scripted-localisation helper.
Shared rivalry state is owned by GER; this module only reads it and emits UI actions.
"""

from cw_lib import L
import rivalry as rv
import entry_ui

LEVER_ACTIONS = [
    ("nva_alert_up", "Raise NVA Alert"),
    ("nva_alert_down", "Lower NVA Alert"),
    ("raise_exchange", "Raise Exchange"),
    ("transit_checks", "Transit Checks"),
    ("tighten_border", "Strengthen Border"),
    ("hva_offensive", "HVA in Bonn"),
    ("recognition_drive", "Recognition Drive"),
    ("goodwill", "Offer Goodwill"),
    ("ask_credit", "Request Credit"),
    ("close_transit", "Close Access Routes"),
]

DOMESTIC_ACTIONS = [
    ("intershop", "Intershops"),
    ("koko", "KoKo"),
    ("border_regime", "Border Regime"),
    ("stasi_sweep", "State Security"),
    ("consumer_imports", "Consumer Imports"),
    ("reform_course", "Press Reform"),
]

ANSWER_ROWS = [
    (1, "yield", "Back Down"),
    (2, "stall", "Stall"),
    (3, "escalate", "Escalate"),
    (4, "moscow", "Call on Moscow"),
    (5, "counter", "Make a Counter-Offer"),
]


def _register_action_labels(actions):
    for key, label in actions:
        L(f"cwgg_east_action_{key}", label)


def window(Window, DT):
    """Return the DDR-perspective window using the host's Window and DT DSL."""
    tabs = [f"cwgg_east_tab_{i}" for i in range(1, 6)]
    w = Window(
        "cwgg_east", "cwgg_east_open", "cwgg_east_tab", tabs,
        "cwgg_east_title", "cwgg_east_subtitle", "GFX_cwgg_emblem_ddr",
        "cwgg_east_right_label", "cwgg_east_right_value",
        dict(x=entry_ui.RELATIONS_X, y=entry_ui.BUTTON_Y, sprite="GFX_cwgg_launcher_relations"),
        skin="ddr", emblem2="GFX_cwgg_emblem_brd",
    )

    L("cwgg_east_title", "Inner-German Relations")
    L("cwgg_east_subtitle", "German Democratic Republic · [Root.GetLeader]")
    L("cwgg_east_right_label", "Escalation ladder")
    L("cwgg_east_right_value", "[EGR_StageColored]")
    L("cwgg_east_right_value_tt", "§Y[EGR_StageName]§!\nShared climate and crisis intensity determine the current stage.")
    L("cwgg_east_topbar_value", "[?GER.cwgg_stufe|0]")
    L("cwgg_east_topbar_tt", "§YInner-German Relations§!\nClimate: §Y[?GER.cwgg_klima|0]§! | East Berlin initiative: §Y[?GER.cwgg_init_ddr|0]§!/6\nClick to open the window.")
    L('cwgg_east_relations_tt','§YInner-German Relations§!\nOpen the file on relations with the Federal Republic: the political situation, crises, readiness and agreements.')
    L('cwgg_east_security_tt','§YDomestic Affairs§!\nOpen the Council of Ministers file on currency pressures, public order and domestic policy.')
    L("cwgg_east_emblem2_tt", "§YThe Federal Republic§!\nBonn's government and its levers in the shared rivalry.")
    L("cwgg_east_tab_1", "Situation")
    L("cwgg_east_tab_2", "Crisis")
    L("cwgg_east_tab_3", "Levers")
    L("cwgg_east_tab_4", "Treaties")
    L("cwgg_east_tab_5", "Domestic")

    # Initiative and refresh data are presentation-only; all authoritative rivalry data stays on GER.
    w.text("init", "cwgg_east_init", 370, 66, 330, fmt_="right", tip="cwgg_east_init_tt")
    L("cwgg_east_init", "Initiative [?GER.cwgg_init_ddr|0]/6")
    L("cwgg_east_init_tt", "§YInitiative§! pays for East Berlin's shared-rivalry actions. Current stock: §Y[?GER.cwgg_init_ddr|0]§!/6.")

    # Situation: shared ladder/readiness/border snapshots plus selected GDR meters.
    tab = 1
    w.section("s_climate", 138, "cwgg_east_h_climate", tab)
    L("cwgg_east_h_climate", "CLIMATE BETWEEN THE TWO GERMAN STATES")
    w.text("climate", "cwgg_east_climate", 36, 172, 700, font="hoi_18mbs", tab=tab, tip="cwgg_east_climate_tt")
    L("cwgg_east_climate", "Climate §Y[?GER.cwgg_klima|0]§!  ·  pressure §R[?GER.cwgg_druck|0]§!  ·  stage [EGR_StageName]")
    L("cwgg_east_climate_tt", "The political climate ranges from -100 confrontation to +100 interdependence. Escalation pressure raises the risk of a crisis.")
    w.icon("climate_track", "GFX_cwgg_climate_track", 110, 206, tab=tab, tip="cwgg_east_climate_tt")
    w.icon("climate_marker", "GFX_cwgg_marker", 104, 200, tab=tab, xprop="cwgg_g_east_marker")
    w.refresh.append("set_variable = { cwgg_g_east_marker = GER.cwgg_klima }\nadd_to_variable = { cwgg_g_east_marker = 100 }\nmultiply_variable = { cwgg_g_east_marker = 2.8 }\nadd_to_variable = { cwgg_g_east_marker = 104 }\nround_variable = cwgg_g_east_marker")
    w.text("climate_min", "cwgg_east_climate_min", 36, 207, 70, fmt_="right", tab=tab)
    w.text("climate_max", "cwgg_east_climate_max", 676, 207, 80, tab=tab)
    L("cwgg_east_climate_min", "§R-100§!")
    L("cwgg_east_climate_max", "§G+100§!")

    w.section("s_readiness", 244, "cwgg_east_h_readiness", tab)
    L("cwgg_east_h_readiness", "READINESS AND BORDER POSTURE")
    w.text("readiness", "cwgg_east_readiness", 36, 278, 700, tab=tab)
    L("cwgg_east_readiness", "NVA alert §Y[?GER.cwgg_mob_ddr|0]§!/3  ·  Bundeswehr alert §Y[?GER.cwgg_mob_brd|0]§!/3  ·  East German border divisions §Y[?GER.cwgg_aufm_ddr_div|0]§!  ·  West German border divisions §Y[?GER.cwgg_aufm_brd_div|0]§!")
    w.bar("pressure", 220, 310, "GER.cwgg_druck", 0, 100, "red", tab=tab, tip="cwgg_east_climate_tt")
    w.text("pressure_label", "cwgg_east_pressure_label", 36, 307, 170, tab=tab)
    w.text("pressure_value", "cwgg_east_pressure_value", 530, 307, 60, tab=tab)
    L("cwgg_east_pressure_label", "Escalation pressure")
    L("cwgg_east_pressure_value", "§R[?GER.cwgg_druck|0]§!")
    w.text("meters", "cwgg_east_meters", 36, 342, 710, h=58, tab=tab, tip="cwgg_east_meters_tt")
    L("cwgg_east_meters", "Hard-currency shortage §Y[?cwddr_hard_currency|0]§!  ·  dependence on Bonn §Y[?cwddr_west_dependency|0]§!  ·  recognising states §Y[?Granted_Recognition|0]§!\nSED control §Y[?cwddr_sed_control|0]§!  ·  civic opposition §Y[?cwddr_opposition|0]§!")
    L("cwgg_east_meters_tt", "Hard-currency shortage measures financial pressure: lower values mean relief. Recognising states are counted from diplomatic recognition. Dependence, government control and civic opposition reflect the pressures facing the republic.")
    w.text('counterpart_absent','cwgg_east_counterpart_absent',36,630,700,h=40,tab=1,vis='NOT = { country_exists = GER }')
    L('cwgg_east_counterpart_absent','The Federal Republic is not available for bilateral negotiations. Domestic affairs remain accessible.')
    w.section("s_report", 408, "cwgg_east_h_report", tab)
    L("cwgg_east_h_report", "SITUATION REPORT")
    for i in range(1, 6):
        w.text(f"log_{i}", f"cwgg_east_log_{i}", 36, 442 + (i - 1) * 22, 700, tab=tab,
               vis=f"GER = {{ check_variable = {{ cwgg_log_{i} > 0 }} }}")
        L(f"cwgg_east_log_{i}", f"§Y[?GER.cwgg_log_y_{i}|0]§!  [EGR_Log{i}]")
        entries=[(f'GER = {{ check_variable = {{ cwgg_log_{i} = {code} }} }}',f'cwgg_log_{code}') for code,text in sorted(rv.LOGS.values())]
        entries += [(f'GER = {{ check_variable = {{ cwgg_log_{i} = {900+a[0]} }} }}',f'cwgg_log_{900+a[0]}') for a in rv.ANSWERS]
        DT(f'EGR_Log{i}',entries,'cwgg_east_no_log')
    L('cwgg_east_no_log','No entry.')
    w.text('report_initial','cwgg_east_report_initial',36,442,700,h=80,tab=tab,vis='GER = { check_variable = { cwgg_log_1 = 0 } }')
    L('cwgg_east_report_initial','Relations with Bonn rest on access to Berlin, international recognition and trade across the border. The government must balance its need for hard currency against dependence on the Federal Republic and the political risks of wider contacts.')
    w.text("situation_footer", "cwgg_east_situation_footer", 36, 568, 700, h=56, tab=tab)
    L("cwgg_east_situation_footer", "Initiative and readiness shape the bilateral balance. Border strength follows the latest joint assessment. Treaties and the political climate are reviewed monthly, including while this file is closed.")
    DT("EGR_StageName", [(f"GER = {{ check_variable = {{ cwgg_stufe = {i} }} }}", f"cwgg_east_stage_{i}") for i in range(7)], "cwgg_east_stage_0")
    DT("EGR_StageColored", [(f"GER = {{ check_variable = {{ cwgg_stufe = {i} }} }}", f"cwgg_east_stage_col_{i}") for i in range(7)], "cwgg_east_stage_col_0")
    stage_names = ["Modus Vivendi", "Cool Coexistence", "Tensions", "Crisis", "Confrontation", "War Danger", "War"]
    colors = ["G", "G", "Y", "Y", "R", "R", "R"]
    for i, name in enumerate(stage_names):
        L(f"cwgg_east_stage_{i}", name)
        L(f"cwgg_east_stage_col_{i}", f"§{colors[i]}{name}§!")

    # Crisis: only show the DDR's pending answer and the previous resolved Bonn course.
    tab = 2
    crisis_live = "GER = { check_variable = { cwgg_krise_typ > 0 } }"
    crisis_none = "GER = { check_variable = { cwgg_krise_typ = 0 } }"
    w.section("c_head", 138, "cwgg_east_h_crisis", tab)
    L("cwgg_east_h_crisis", "CRISIS COURSE")
    w.text("crisis_name", "cwgg_east_crisis_name", 36, 174, 700, font="hoi_18mbs", tab=tab, vis=crisis_live)
    L("cwgg_east_crisis_name", "[EGR_CrisisName]")
    DT("EGR_CrisisName", [(f"GER = {{ check_variable = {{ cwgg_krise_typ = {i} }} }}", f"cwgg_east_crisis_{i}") for i in range(1, 11)], "cwgg_east_crisis_none")
    for i, crisis in enumerate(["Transit Crisis", "Border Incident", "Spy Affair", "Embassy Refugees", "Recognition Crisis", "Missile Crisis", "Manoeuvre Crisis", "Dissident Crisis", "Elbe Border Dispute", "Uprising in the GDR"], 1):
        L(f"cwgg_east_crisis_{i}", crisis.upper())
    L("cwgg_east_crisis_none", "NO CRISIS UNDER WAY")
    w.text("crisis_none", "cwgg_east_crisis_empty", 36, 182, 700, h=56, tab=tab, vis=crisis_none)
    # IMPERIA COLD WAR — Align East Berlin's status and month counter with Bonn's two-month round clock.
    L("cwgg_east_crisis_empty", "There is no active crisis. Submit your government's instructions when a dispute begins. Each two-month round waits for both governments' instructions; silence makes no concession.")
    w.text("crisis_status", "cwgg_east_crisis_status", 36, 208, 700, tab=tab, vis=crisis_live)
    L("cwgg_east_crisis_status", "Intensity §Y[?GER.cwgg_krise_int|0]§!/100  ·  round §Y[?GER.cwgg_krise_runde|0]§!/§Y[?GER.cwgg_krise_max|0]§!  ·  month §Y[?GER.cwgg_krise_monat|0]§!/2")
    w.bar("crisis_intensity", 220, 236, "GER.cwgg_krise_int", 0, 100, "gold", tab=tab, vis=crisis_live)
    w.text("pending", "cwgg_east_pending", 36, 258, 700, tab=tab, vis=crisis_live)
    L("cwgg_east_pending", "Our answer: §Y[EGR_PendingAnswer]§! · Bonn: [EGR_BonnReady] · East Berlin: [EGR_EastReady]")
    for name,var in (('Bonn','cwgg_brd_order_ready'),('East','cwgg_ddr_order_ready')):
        DT('EGR_'+name+'Ready',[(f'GER = {{ check_variable = {{ {var} > 0 }} }}','cwgg_east_order_submitted')],'cwgg_east_order_waiting')
    L('cwgg_east_order_submitted','§Gsubmitted§!')
    L('cwgg_east_order_waiting','§Ywaiting§!')
    DT("EGR_PendingAnswer", [(f"GER = {{ check_variable = {{ cwgg_ddr_wahl = {a[0]} }} }}", f"cwgg_answer_{a[1]}") for a in ANSWER_ROWS], "cwgg_east_no_pending")
    L("cwgg_east_no_pending", "no answer chosen")
    w.text("last_round", "cwgg_east_last_round", 36, 284, 700, h=34, tab=tab,
           vis="GER = { check_variable = { cwgg_krise_runde > 0 } }")
    L("cwgg_east_last_round", "Last resolved round: Bonn chose §Y[EGR_LastBonn]§!; we chose §Y[EGR_LastAnswer]§!. Intensity changed by §Y[?GER.cwgg_last_dint|0]§!.")
    DT("EGR_LastBonn", [(f"GER = {{ check_variable = {{ cwgg_last_h = {s[0]} }} }}", f"cwgg_stance_{s[1]}") for s in [
        (1, "wait", "Wait"), (2, "deescalate", "De-escalate"), (3, "firm", "Stand Firm"),
        (4, "pressure", "Counter-Pressure"), (5, "allies", "Call in the Allies"), (6, "secret", "Secret Channel"), (7, "mobilise", "Prepare Mobilisation")]], "cwgg_east_no_bonn_course")
    DT("EGR_LastAnswer", [(f"GER = {{ check_variable = {{ cwgg_last_a = {a[0]} }} }}", f"cwgg_answer_{a[1]}") for a in ANSWER_ROWS], "cwgg_east_no_pending")
    L("cwgg_east_no_bonn_course", "not recorded")
    w.section("c_answers", 326, "cwgg_east_h_answers", tab, right="cwgg_east_choice_note")
    L("cwgg_east_h_answers", "OUR COURSE FOR THE NEXT ROUND")
    L("cwgg_east_choice_note", "Bonn's current choice remains undisclosed")
    for i, key, label in ANSWER_ROWS:
        y = 364 + (i - 1) * 43
        L(f"cwgg_east_answer_label_{i}", label)
        cost = "Free at resolution" if i <= 2 else "Costs 1 initiative when the round resolves"
        eligibility = ""
        if i == 4:
            eligibility = " Requires the Soviet Union to exist. This does not commit Moscow to intervene."
        L(f"cwgg_east_answer_{i}_tt", f"§Y{label}§!\n{cost}. Choosing an answer starts a 30-day lock on the shared crisis instruction. The Federal Republic's current course remains confidential.{eligibility}")
        w.button(f"answer_{i}", "GFX_mdcw_cw_button_160", 36, y, f"cwgg_east_answer_label_{i}",
                 f"COLDWAR_GER_1970_east_act_answer_{i} = yes", tab=tab, vis=crisis_live,
                 enabled=f"COLDWAR_GER_1970_east_can_answer_{i} = yes", tip=f"cwgg_east_answer_{i}_tt")
        w.text(f"answer_terms_{i}", f"cwgg_east_answer_terms_{i}", 210, y + 3, 530, h=36, tab=tab, vis=crisis_live)
        L(f"cwgg_east_answer_terms_{i}", [
            "Free at resolution · 30-day shared instruction lock",
            "Free at resolution · 30-day shared instruction lock",
            "1 initiative at resolution · 30-day shared instruction lock",
            "1 initiative at resolution · Soviet Union must exist",
            "1 initiative at resolution · 30-day shared instruction lock",
        ][i - 1])

    # Shared levers and GDR-facing decision actions.
    tab = 3
    w.section("l_head", 138, "cwgg_east_h_levers", tab)
    L("cwgg_east_h_levers", "EAST BERLIN'S LEVERS")
    w.text("lever_intro", "cwgg_east_lever_intro", 36, 171, 700, h=36, tab=tab)
    L("cwgg_east_lever_intro", "These measures alter bilateral relations and the GDR's position. Initiative and political power costs appear with each option.")
    _register_action_labels(LEVER_ACTIONS)
    for i, (key, label) in enumerate(LEVER_ACTIONS):
        y = 211 + i * 46
        w.button(f"lever_{key}", "GFX_mdcw_cw_button_160", 36, y, f"cwgg_east_action_{key}",
                 f"COLDWAR_GER_1970_east_act_{key} = yes", tab=tab,
                 enabled=f"COLDWAR_GER_1970_east_can_{key} = yes", tip=f"cwgg_east_action_{key}_tt")
        w.text(f"lever_terms_{key}", f"cwgg_east_action_{key}_terms", 210, y + 3, 530, h=36, tab=tab)

    # IMPERIA COLD WAR — Both German governments can propose agreements and review signatures.
    tab = 4
    w.section("t_head", 138, "cwgg_east_h_treaties", tab, right="cwgg_east_treaty_nogo")
    L("cwgg_east_h_treaties", "DIPLOMATIC FRAMEWORK")
    L("cwgg_east_treaty_nogo", "Unity uses separate consent events")
    w.text("t_intro", "cwgg_east_treaty_intro", 36, 168, 700, h=24, tab=tab)
    L("cwgg_east_treaty_intro", "Either government may propose talks. Agreements require both governments' signatures.")
    for treaty in rv.TREATIES:
        n, treaty_key, name, desc = treaty[:4]
        y = 198 + (n - 1) * 46
        w.icon(f"t_{n}_bg", "GFX_cwgg_panel_740", 20, y, tab=tab)
        w.icon(f"t_{n}_status_icon", "GFX_cwgg_treaty", 30, y + 9, tab=tab, frame=f"cwgg_g_east_t_{n}", tip=f"cwgg_treaty_{n}_desc")
        w.text(f"t_{n}_name", f"cwgg_treaty_{n}", 58, y + 3, 565, font="hoi_16mbs", tab=tab, tip=f"cwgg_treaty_{n}_desc")
        w.text(f"t_{n}_status", f"cwgg_east_treaty_{n}_status", 58, y + 24, 415, tab=tab)
        w.bar(f"east_t_{n}", 486, y + 32, "GER.cwgg_verh_prog", 0, 100, "gold", small=True, tab=tab,
              vis=f"GER = {{ check_variable = {{ cwgg_verh = {n} }} }}")
        w.button(f't_{n}_propose','GFX_mdcw_cw_button_96',648,y+7,'cwgg_east_treaty_propose',
                 f'COLDWAR_GER_1970_east_act_treaty_{n} = yes',tab=tab,
                 enabled=f'COLDWAR_GER_1970_east_can_treaty_{n} = yes',tip='cwgg_east_treaty_propose_tt')
        w.refresh.append(f"if = {{ limit = {{ GER = {{ check_variable = {{ cwgg_vertrag_{n} = 1 }} }} }} set_variable = {{ cwgg_g_east_t_{n} = 4 }} }}\n"
                         f"else_if = {{ limit = {{ GER = {{ check_variable = {{ cwgg_vertrag_{n} = 2 }} }} }} set_variable = {{ cwgg_g_east_t_{n} = 5 }} }}\n"
                         f"else_if = {{ limit = {{ GER = {{ check_variable = {{ cwgg_verh = {n} }} }} }} set_variable = {{ cwgg_g_east_t_{n} = 3 }} }}\n"
                         f"else = {{ set_variable = {{ cwgg_g_east_t_{n} = 1 }} }}")
        # IMPERIA COLD WAR — Joint applications do not imply successful UN admission.
        DT(f"EGR_Treaty_{n}", [(f"GER = {{ check_variable = {{ cwgg_vertrag_{n} = 1 }} }}", "COLDWAR_Germany_un_applications_status" if n == 4 else "cwgg_east_treaty_in_force"),
                               (f"GER = {{ check_variable = {{ cwgg_vertrag_{n} = 2 }} }}", "cwgg_east_treaty_suspended"),
                               (f"GER = {{ OR = {{ check_variable = {{ cwgg_tr_pending = {n} }} check_variable = {{ cwgg_tr_ready = {n} }} }} }}", "cwgg_east_treaty_signature"),
                               (f"GER = {{ check_variable = {{ cwgg_verh = {n} }} }}", "cwgg_east_treaty_negotiating")], "cwgg_east_treaty_pending")
        L(f"cwgg_east_treaty_{n}_status", f"[EGR_Treaty_{n}]")
    L("cwgg_east_treaty_in_force", "§GIn force§!")
    L("cwgg_east_treaty_suspended", "§RSuspended§!")
    L("cwgg_east_treaty_negotiating", "§YNegotiating§!")
    L("cwgg_east_treaty_pending", "Not concluded")
    L('cwgg_east_treaty_signature','§YAwaiting signature§!')
    L('cwgg_east_treaty_propose','Propose')
    L('cwgg_east_treaty_propose_tt','Open negotiations: §Y25 political power§! and §Y2 initiative§!. Existing treaties, climate and diplomatic conditions apply. Each government retains its right to refuse.')
    w.text("t_progress", "cwgg_east_treaty_progress", 36, 620, 540, tab=tab,
           vis="GER = { check_variable = { cwgg_verh > 0 } }")
    L("cwgg_east_treaty_progress", "Current talks: [EGR_TreatyProgress]  ·  §Y[?GER.cwgg_verh_prog|0]%§!")
    DT("EGR_TreatyProgress", [(f"GER = {{ check_variable = {{ cwgg_verh = {t[0]} }} }}", f"cwgg_treaty_{t[0]}") for t in rv.TREATIES], "cwgg_east_treaty_pending")
    w.button('t_review','GFX_mdcw_cw_button_160',590,616,'cwgg_east_treaty_review',
             'COLDWAR_GER_1970_east_review_treaty = yes',tab=tab,
             enabled='COLDWAR_GER_1970_east_can_review_treaty = yes',tip='cwgg_east_treaty_review_tt')
    L('cwgg_east_treaty_review','Review Proposal')
    L('cwgg_east_treaty_review_tt','Review or defer the current agreement. Reviewing costs no political power. The agreement takes effect only after both governments sign.')
    w.text("unity_terms", "cwgg_east_unity_terms", 36, 646, 510, h=36, tab=tab, tip="cwgg_east_unity_review_tt")
    L("cwgg_east_unity_terms", "Propose talks: §Y100 PP§! + §Y3 initiative§!  ·  Current chapter: §Y30-day position cooldown§!")
    w.button("unity_review", "GFX_mdcw_cw_button_160", 560, 650, "cwgg_east_unity_review",
             "COLDWAR_GER_1970_east_act_unity_review = yes", tab=tab,
             enabled="COLDWAR_GER_1970_east_can_unity_review = yes", tip="cwgg_east_unity_review_tt")
    L("cwgg_east_unity_review", "Unity Agenda")
    L("cwgg_east_unity_review_tt", "§YPropose unity talks§!: costs 100 political power and 3 initiative. Requires 36 consecutive months of détente, climate at least 70, Modus Vivendi with no active crisis, the Basic Treaty, Permanent Representations and Traffic, Post and Travel Agreements, plus either the Cultural Agreement or the SED leader's State Visit and Bonn's European Peace Order focus. Once talks are under way, reopen East Berlin's position on the current chapter; the position decision has a 30-day cooldown. Chapter consent and ratification are handled through their scheduled events.")

    # Domestic course options.
    tab = 5
    w.section("d_head", 138, "cwgg_east_h_domestic", tab)
    L("cwgg_east_h_domestic", "ECONOMY, SECURITY AND SOCIAL POLICY")
    w.text("d_intro", "cwgg_east_domestic_intro", 36, 171, 700, h=36, tab=tab)
    L("cwgg_east_domestic_intro", "Choose an institutional response to the GDR's currency needs, population pressure and Soviet alignment.")
    _register_action_labels(DOMESTIC_ACTIONS)
    for i, (key, label) in enumerate(DOMESTIC_ACTIONS):
        y = 224 + i * 61
        w.button(f"domestic_{key}", "GFX_mdcw_cw_button_160", 36, y, f"cwgg_east_action_{key}",
                 f"COLDWAR_GER_1970_east_act_{key} = yes", tab=tab,
                 enabled=f"COLDWAR_GER_1970_east_can_{key} = yes", tip=f"cwgg_east_action_{key}_tt")
        w.text(f"domestic_terms_{key}", f"cwgg_east_action_{key}_terms", 210, y + 3, 530, h=42, tab=tab)

    return w
