# IMPERIA CW — Cold War: Soviet Union 1970 content generator.
# COLDWAR | The Politburo dossier: a scripted GUI at the top of the decision category "The Politburo of the CPSU"
# (Enes, 19.10.2026). Moscow and every Union republic see the same file: the General Secretary with his portrait and
# office, the Politburo balance, Union cohesion, the next session and congress; the three republican members with portrait,
# flag, title and their vote stamp; the ballot; and Socialist Emulation, a monthly ranking of the republics (growth,
# industry, output per head, plan targets) with its banners and honours (the logic in cw_emulation.py).
# Art: art/politburo_art.py paints the textures (art/dds), art/pb_layout.py holds the shared coordinates.
import os, re, glob
from cw_common import *
import cw_effects as E
import cw_union as U
import cw_events as EV
import cw_emulation as EM                      # Socialist Emulation: the table, banners, honours, favourite, Spartakiad
from cw_sys_effects import KEYS
from art import pb_layout as L

PB = f"{PFX}pb_"
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "art", "dds")
TEX = "gfx/interface/coldwar_politburo"
WINDOW = f"{PFX}politburo_window"
GUI = f"{PFX}politburo_gui"

# ------------------------------------------------------------------ portraits: leader name -> texture
SOV_PORTRAITS = {}      # possible leaders of the Soviet Union
for _k, (_n, _p, _d) in E.GENSEC.items():
    SOV_PORTRAITS[_n] = _p
for _k, (_n, _p, _t) in E.STANDIN.items():
    SOV_PORTRAITS.setdefault(_n, _p)
for _n, (_en, _p) in E.LEADER_EN.items():
    SOV_PORTRAITS.setdefault(_en, _p)
SOV_PORTRAITS.setdefault("Viktor Grishin", "gfx/leaders/mdcw_historical_pool/SOV_viktor_grishin.dds")
SOV_PORTRAITS.setdefault("Boris Yeltsin", "gfx/leaders/mdcw_historical_pool/SOV_boris_yeltsin.dds")   # MDCW_HP_set_sov_yeltsin

SSR_PORTRAITS = {}      # First Secretaries of the Union republics: the 1970 history and Moscow's men (cw_union.SUCC)
SSR_START = {}
for _t in SSR:
    for _f in glob.glob(os.path.join(MOD, f"history/countries/{_t} - *.txt")):
        _txt = open(_f, encoding="utf-8-sig", errors="replace").read()
        _m = re.search(r'1970\.1\.1 = \{.*?create_country_leader = \{ name = "([^"]+)" picture = "([^"]+)"', _txt, re.S)
        if _m:
            SSR_PORTRAITS[_m.group(1)] = _m.group(2)
            SSR_START[_t] = _m.group(1)
for _t, _lst in U.SUCC.items():
    for _n, _p in _lst:
        SSR_PORTRAITS.setdefault(_n, _p)
for _n in ("Petro Shelest", "Volodymyr Shcherbytsky"):
    pass
SSR_PORTRAITS.setdefault("Volodymyr Shcherbytsky", "gfx/leaders/UKR/shcherbytsky.dds")


def sprite_of(name):
    return f"GFX_{PFX}pt_{slug(name)}"


ALL_PORTRAITS = {}
for _d in (SOV_PORTRAITS, SSR_PORTRAITS):
    for _n, _p in _d.items():
        if _p:
            ALL_PORTRAITS[_n] = _p
UNKNOWN = f"GFX_{PB}portrait_unknown"

# titles of the First Secretaries
PARTY_OF = {"UKR": "Ukraine", "BLR": "Byelorussia", "EST": "Estonia", "LAT": "Latvia", "LIT": "Lithuania", "ARM": "Armenia",
            "AZE": "Azerbaijan", "GEO": "Georgia", "KAZ": "Kazakhstan", "KYR": "Kirghizia", "TAJ": "Tajikistan", "TRK": "Turkmenistan",
            "UZB": "Uzbekistan", "MLV": "Moldavia"}

SCRIPTED_LOC = []       # defined_text blocks
EFFECTS = []            # scripted effect lines


def dt(name, entries, fallback):
    """defined_text; entries = [(trigger lines, localization key or sprite)], fallback = key or sprite."""
    L_ = ["defined_text = {", f"name = {name}"]
    for trig, key in entries:
        L_ += ["text = {", "trigger = {"] + list(trig) + ["}", f"localization_key = {key}", "}"]
    L_ += ["text = {", f"localization_key = {fallback}", "}", "}"]
    SCRIPTED_LOC.extend(L_)


def loc(key, text):
    LOC[key] = text
    return key


# ------------------------------------------------------------------ scripted localisation
SEAT = lambda n: f"var:global.{PB}seat_{n}"
SEAT_ON = lambda n: f"check_variable = {{ global.{PB}slot_{n}_on = 1 }}"


def portrait_dt(name, scope, names):
    ent = [([f"{scope} = {{ has_country_leader = {{ name = \"{n}\" ruling_only = yes }} }}"], sprite_of(n)) for n in sorted(names) if names[n]]
    dt(name, ent, UNKNOWN)


portrait_dt(f"{PB}GetGsPortrait", "SOV", SOV_PORTRAITS)
for _s in (1, 2, 3):
    portrait_dt(f"{PB}GetSeat{_s}Portrait", SEAT(_s), SSR_PORTRAITS)
    dt(f"{PB}GetSeat{_s}Title", [([f"{SEAT(_s)} = {{ original_tag = {t} }}"],
                                  loc(f"{PB}title_{t}", f"First Secretary of the\\nCP of {PARTY_OF[t]}")) for t in SSR],
       loc(f"{PB}title_generic", "First Secretary of the\\nrepublican Party"))

dt(f"{PB}GetGsTitle", [(["SOV = { has_government = communism }"], loc(f"{PB}gs_title_cpsu", "General Secretary of the CC CPSU"))],
   loc(f"{PB}gs_title_other", "Leader of the Soviet Union"))
HEIRS = {k: E.GENSEC[k][0] for k in KEYS}
HEIRS.update({"aliyev": "Heydar Aliyev", "grishin": "Viktor Grishin"})
dt(f"{PB}GetHeir", [([f"SOV = {{ has_country_flag = {PFX}heir_{k} }}"], loc(f"{PB}heir_{k}", n)) for k, n in HEIRS.items()],
   loc(f"{PB}heir_none", "none designated"))
dt(f"{PB}GetCohesionTier", [(["SOV = { check_variable = { COLDWAR_SOV_union_cohesion > 74 } }"], loc(f"{PB}coh_unbreakable", "Unbreakable Union")),
                            (["SOV = { check_variable = { COLDWAR_SOV_union_cohesion > 54 } }"], loc(f"{PB}coh_stable", "Stable")),
                            (["SOV = { check_variable = { COLDWAR_SOV_union_cohesion > 34 } }"], loc(f"{PB}coh_strained", "§YStrained§!")),
                            (["SOV = { check_variable = { COLDWAR_SOV_union_cohesion > 14 } }"], loc(f"{PB}coh_crisis", "§RIn Crisis§!"))],
   loc(f"{PB}coh_disintegration", "§RDisintegration§!"))
MONTH = {1: "January", 7: "July"}
_ses = []
for _y in range(1970, 2000):
    _ses.append(([f"check_variable = {{ global.{PFX}session_half = 0 }}", f"date < {_y}.7.2"], loc(f"{PB}ses_{_y}_7", f"1 July {_y}")))
    _ses.append(([f"check_variable = {{ global.{PFX}session_half = 1 }}", f"date < {_y + 1}.1.2"], loc(f"{PB}ses_{_y + 1}_1", f"1 January {_y + 1}")))
dt(f"{PB}GetNextSession", _ses, loc(f"{PB}ses_next", "the next regular session"))
ROMAN = {24: "XXIV", 25: "XXV", 26: "XXVI", 27: "XXVII", 28: "XXVIII"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
_con = [([f"has_global_flag = {PFX}congress_open"], loc(f"{PB}con_open", "[COLDWAR_SOV_GetCongress] - §Yin session§!"))]
for _c, _d in EV.CONGRESSES:
    _yy, _mm, _dd = (int(x) for x in _d.split("."))
    _con.append(([f"date < {_d}"], loc(f"{PB}con_{_c}", f"{ROMAN[_c]} Congress, {_dd} {MONTHS[_mm - 1]} {_yy}")))
dt(f"{PB}GetNextCongress", _con, loc(f"{PB}con_none", "none scheduled"))

# the ballot line
dt(f"{PB}GetBallot",
   [([f"has_global_flag = {PFX}vote_running", f"check_variable = {{ global.{PFX}vote_type = 3 }}"],
     loc(f"{PB}ballot_lead", "§YVote in progress§! on [COLDWAR_SOV_GetVoteSubject]. Moscow casts 3 votes in favour; "
                             "the change fails only if all three republican members vote against.")),
    ([f"has_global_flag = {PFX}vote_running"],
     loc(f"{PB}ballot_run", "§YVote in progress§! on [COLDWAR_SOV_GetVoteSubject]. The seven Moscow members vote with the balance of the Politburo.")),
    ([f"check_variable = {{ global.{PFX}last_type > 0 }}"], loc(f"{PB}ballot_last", "Last decision of the Politburo: [COLDWAR_SOV_GetLastVoteSubject]."))],
   loc(f"{PB}ballot_none", "No question is before the Politburo."))

# Socialist Emulation (the logic lives in cw_emulation.py)
EMU = EM.EMU
ORD = {1: "1st", 2: "2nd", 3: "3rd"}
for _n in range(1, 16):
    loc(f"{PB}ord_{_n}", f"{ORD.get(_n, str(_n) + 'th')} of [?global.COLDWAR_SOV_pb_ssr_count|0]")
for _k in EMU:
    dt(f"{PB}GetRank_{_k}", [([f"has_country_flag = {PB}disqualified"], loc(f"{PB}ord_disq", "§Rdisqualified§!"))] +
       [([f"check_variable = {{ {PB}rank_{_k} = {n} }}"], f"{PB}ord_{n}") for n in range(1, 16)], loc(f"{PB}ord_none", "-"))

# the balance marker: one sprite per position, chosen live from the shadow variable of the balance of power
MARKERS = [f"GFX_{PB}marker_{i:02d}" for i in range(L.BAR_FRAMES)]
_mk = []
for _i in range(L.BAR_FRAMES - 1):
    _hi = -1 + (_i + 0.5) * 2 / (L.BAR_FRAMES - 1)
    _mk.append(([f"SOV = {{ check_variable = {{ {PFX}bop < {round(_hi, 3)} }} }}"], MARKERS[_i]))
dt(f"{PB}GetBopMarker", _mk, MARKERS[-1])

# ------------------------------------------------------------------ effects
EFFECTS += ["# ==== the Politburo dossier (decision category GUI, cw_pbgui.py) =================================",
            "# the three seats keep their place in the dossier: a member who leaves frees his slot, a new member takes the first free one",
            f"{PB}update_seats = {{", "hidden_effect = {",
            f"every_country = {{ limit = {{ has_variable = {PB}slot NOT = {{ has_country_flag = {PFX}seat }} }} clear_variable = {PB}slot }}",
            "set_temp_variable = { pb_o1 = 0 }", "set_temp_variable = { pb_o2 = 0 }", "set_temp_variable = { pb_o3 = 0 }"]
for _s in (1, 2, 3):
    EFFECTS += [f"set_variable = {{ global.{PB}slot_{_s}_on = 0 }}", f"set_variable = {{ global.{PB}seat_{_s} = SOV }}"]
EFFECTS += ["every_country = {", f"limit = {{ has_variable = {PB}slot has_country_flag = {PFX}seat }}"]
for _s in (1, 2, 3):
    EFFECTS += [f"if = {{ limit = {{ check_variable = {{ {PB}slot = {_s} }} }} set_variable = {{ global.{PB}seat_{_s} = THIS }} "
                f"set_variable = {{ global.{PB}slot_{_s}_on = 1 }} set_temp_variable = {{ pb_o{_s} = 1 }} }}"]
EFFECTS += ["}", "every_country = {", f"limit = {{ has_country_flag = {PFX}seat NOT = {{ has_variable = {PB}slot }} }}"]
_chain = []
for _s in (1, 2, 3):
    _chain.append(f"{'if' if _s == 1 else 'else_if'} = {{ limit = {{ check_variable = {{ pb_o{_s} = 0 }} }} set_variable = {{ {PB}slot = {_s} }} "
                  f"set_variable = {{ global.{PB}seat_{_s} = THIS }} set_variable = {{ global.{PB}slot_{_s}_on = 1 }} set_temp_variable = {{ pb_o{_s} = 1 }} }}")
EFFECTS += _chain + ["}", "}", "}", ""]

# ------------------------------------------------------------------ the GUI window
FONT16, FONT22 = "hoi4_typewriter16", "hoi4_typewriter22"
GUI_EL = []
PROPS = {}
TRIGS = {}


def icon(name, sprite, x, y, scale=None, tooltip=None, prop=None, visible=None):
    e = ["iconType = {", f'name = "{PB}{name}"', f'spriteType = "{sprite}"', f"position = {{ x = {x} y = {y} }}"]
    if scale:
        e.append(f"scale = {scale}")
    if tooltip:
        e.append(f'pdx_tooltip = "{tooltip}"')
    e.append("}")
    GUI_EL.extend(e)
    if prop:
        PROPS[PB + name] = prop
    if visible:
        TRIGS[PB + name + "_visible"] = visible


def flag(name, x, y, sprite, image, visible=None, tooltip=None):
    """A country flag: vanilla masked flag sprites, unscaled (GFX_flag_small2 = 41 x 26, GFX_flag_small = 20 x 17 in a 26 x 21 frame)."""
    e = ["buttonType = {", f'name = "{PB}{name}"', f"position = {{ x = {x} y = {y} }}", f'quadTextureSprite = "{sprite}"', 'text = ""']
    if tooltip:
        e.append(f'pdx_tooltip = "{tooltip}"')
    e.append("}")
    GUI_EL.extend(e)
    PROPS[PB + name] = f'image = "{image}"'
    if visible:
        TRIGS[PB + name + "_visible"] = visible


def text(name, key, x, y, w, h, font=FONT16, fmt_="left", visible=None, tooltip=None):
    e = ["instantTextBoxType = {", f'name = "{PB}{name}"', f"position = {{ x = {x} y = {y} }}", f'font = "{font}"',
         f'text = "{key}"', f"maxWidth = {w}", f"maxHeight = {h}", "fixedsize = yes", f"format = {fmt_}"]
    if tooltip:
        e.append(f'pdx_tooltip = "{tooltip}"')
    e.append("}")
    GUI_EL.extend(e)
    if visible:
        TRIGS[PB + name + "_visible"] = visible


icon("dossier", f"GFX_{PB}dossier", 0, 0)
gx, gy = L.GS_PHOTO
icon("gs_portrait", UNKNOWN, gx, gy, scale=L.GS_SCALE, prop=f'image = "[{PB}GetGsPortrait]"',
     tooltip=loc(f"{PB}gs_portrait_tt", "[SOV.GetLeader], [COLDWAR_SOV_pb_GetGsTitle]"))
icon("gs_corners", f"GFX_{PB}photo_corners_large", gx - 4, gy - 4)
R_ = L.ROWS
text("gs_office", loc(f"{PB}gs_office", "[COLDWAR_SOV_pb_GetGsTitle]"), L.VALUE_X, R_["office"] + 3, L.VALUE_W, 18)
text("gs_name", loc(f"{PB}gs_name", "[SOV.GetLeader]"), L.VALUE_X, R_["name"] + 2, L.VALUE_W, 24, font=FONT22)
text("gs_heir", loc(f"{PB}gs_heir", "[COLDWAR_SOV_pb_GetHeir]"), L.VALUE_X, R_["heir"] + 3, L.VALUE_W, 18,
     tooltip=loc(f"{PB}gs_heir_tt", "The designated heir is put to the Politburo first when the General Secretary dies or retires."))
bx, by, bw, bh = L.BAR
icon("bop_marker", MARKERS[L.BAR_FRAMES // 2], bx - L.BAR_PAD, by - 7, prop=f'image = "[{PB}GetBopMarker]"',
     tooltip=loc(f"{PB}bop_tt", "Balance of the Politburo: §Y[?SOV.COLDWAR_SOV_bop|+2]§! (-1 reformers, +1 orthodox)."))
text("gs_balance", loc(f"{PB}gs_balance", "[?SOV.COLDWAR_SOV_bop|+2]"), bx + bw + 8, R_["balance"] + 3, 70, 18)
text("gs_cohesion", loc(f"{PB}gs_cohesion", "[?SOV.COLDWAR_SOV_union_cohesion|0] - [COLDWAR_SOV_pb_GetCohesionTier]"), L.VALUE_X, R_["cohesion"] + 3, L.VALUE_W, 18,
     tooltip=loc(f"{PB}cohesion_tt", "Cohesion of the Union (0-100): above 74 Unbreakable, 55-74 Stable, 35-54 Strained, 15-34 In Crisis, below 15 Disintegration."))
text("gs_session", loc(f"{PB}gs_session", "[COLDWAR_SOV_pb_GetNextSession]"), L.VALUE_X, R_["session"] + 3, L.VALUE_W, 18,
     tooltip=loc(f"{PB}session_tt", "The Politburo meets on 1 January and 1 July. Every republican member may then submit one proposal."))
text("gs_congress", loc(f"{PB}gs_congress", "[COLDWAR_SOV_pb_GetNextCongress]"), L.VALUE_X, R_["congress"] + 3, L.VALUE_W, 18,
     tooltip=loc(f"{PB}congress_tt", "At a Party Congress Moscow fills the three republican seats freely; applications open 90 days before."))

RUNNING = f"has_global_flag = {PFX}vote_running"
for i, x in enumerate(L.SEAT_X, start=1):
    px, py = x + L.SEAT_PHOTO_DX, L.SEAT_Y + L.SEAT_PHOTO_DY
    on = [SEAT_ON(i)]
    icon(f"seat{i}_portrait", UNKNOWN, px, py, scale=L.SEAT_SCALE, prop=f'image = "[{PB}GetSeat{i}Portrait]"', visible=on,
         tooltip=loc(f"{PB}seat{i}_tt", f"§Y[?global.COLDWAR_SOV_pb_seat_{i}.GetLeader]§!, First Secretary of the Central Committee of the Communist Party of "
                                         f"[?global.COLDWAR_SOV_pb_seat_{i}.GetNameDef], holds seat {'I' * i} in the Politburo."))
    icon(f"seat{i}_corners", f"GFX_{PB}photo_corners_small", px - 4, py - 4, visible=on)
    flag(f"seat{i}_flag", x + L.SEAT_FLAG_DX, L.SEAT_Y + L.SEAT_FLAG_DY, "GFX_flag_small2", f"[?global.COLDWAR_SOV_pb_seat_{i}.GetFlag]", visible=on)
    text(f"seat{i}_name", loc(f"{PB}seat{i}_name", f"[?global.COLDWAR_SOV_pb_seat_{i}.GetLeader]"), x, L.SEAT_NAME_Y + 1, L.SEAT_W, 18, visible=on)
    text(f"seat{i}_title", loc(f"{PB}seat{i}_title", f"[{PB}GetSeat{i}Title]"), x, L.SEAT_TITLE_Y, L.SEAT_W, 34, visible=on)
    sx, sy = px + 26, py + 58
    for st, cond in (("pending", f"has_country_flag = {PFX}vote_pending"), ("for", f"has_country_flag = {PFX}voted_yes"),
                     ("against", f"has_country_flag = {PFX}voted_no"), ("abstain", f"has_country_flag = {PFX}voted_abstain")):
        icon(f"seat{i}_stamp_{st}", f"GFX_{PB}stamp_{st}", sx, sy, scale=0.72,
             visible=on + [RUNNING, f"{SEAT(i)} = {{ {cond} }}"] + ([f"{SEAT(i)} = {{ NOT = {{ has_country_flag = {PFX}voted_yes }} "
                                                                    f"NOT = {{ has_country_flag = {PFX}voted_no }} NOT = {{ has_country_flag = {PFX}voted_abstain }} }}"]
                                                                   if st == "pending" else []))
    icon(f"seat{i}_vacant", f"GFX_{PB}stamp_vacant", x + 2, L.SEAT_Y + 30, scale=0.72, visible=[f"check_variable = {{ global.{PB}slot_{i}_on = 0 }}"],
         tooltip=loc(f"{PB}vacant_tt", "This seat is vacant. Moscow fills it at the next Party Congress or by an extraordinary plenum."))

text("ballot", loc(f"{PB}ballot", f"[{PB}GetBallot]"), 82, L.BALLOT_Y + 3, 330, 30)
for st, cond in (("adopted", f"has_global_flag = {PFX}last_passed"), ("rejected", f"NOT = {{ has_global_flag = {PFX}last_passed }}")):
    icon(f"ballot_{st}", f"GFX_{PB}stamp_{st}", 388, L.BALLOT_Y - 14, scale=0.72,
         visible=[f"NOT = {{ {RUNNING} }}", f"check_variable = {{ global.{PFX}last_type > 0 }}", cond])

C_ = L.EMU_COLS
SSR_VIEW = [f"{PFX}is_union_republic = yes"]
HAS_BOARD = [f"check_variable = {{ global.{PB}ssr_count > 0 }}"]
EMU_TT = EM.EMU_TT
for j, (k, (lbl, _e, val, what)) in enumerate(EMU.items()):
    y = L.EMU_ROW_Y + j * L.EMU_ROW_H
    vis = HAS_BOARD + ([f"check_variable = {{ global.{PB}top_plan_val > 0 }}"] if k == "plan" else [])
    # the Transferable Red Banner of the column: bright when the leader holds it, faded when another republic still does
    icon(f"emu_{k}_banner", f"GFX_{PB}banner_held", C_["banner"], y + 1, visible=[EM.leader_holds(k)], tooltip=f"{PB}banner_{k}_tt")
    icon(f"emu_{k}_banner_old", f"GFX_{PB}banner_away", C_["banner"], y + 1, visible=[EM.banner_holder(k), f"NOT = {{ {EM.leader_holds(k)} }}"],
         tooltip=f"{PB}banner_{k}_tt")
    flag(f"emu_{k}_flag", C_["flag"], y - 1, "GFX_flag_small", f"[?global.COLDWAR_SOV_pb_top_{k}.GetFlag]", visible=vis)
    text(f"emu_{k}_leader", loc(f"{PB}emu_{k}_leader", f"[?global.COLDWAR_SOV_pb_top_{k}.GetName]"), C_["leader"], y + 2, 140, 18, visible=vis,
         tooltip=loc(f"{PB}emu_{k}_tt", f"{lbl}: the leading republic by {what}.\\n\\n${EMU_TT}$"))
    text(f"emu_{k}_value", loc(f"{PB}emu_{k}_value", val), C_["value"], y + 2, 80, 18, visible=vis)
    if k == "plan":
        text("emu_plan_none", loc(f"{PB}emu_plan_none", "no target fulfilled yet"), C_["leader"], y + 2, 200, 18,
             visible=HAS_BOARD + [f"check_variable = {{ global.{PB}top_plan_val < 1 }}"])
    text(f"emu_{k}_rank", loc(f"{PB}emu_{k}_rank", f"[{PB}GetRank_{k}]"), C_["rank"], y + 2, 82, 18, visible=SSR_VIEW + HAS_BOARD)
# the honour roll
text("pride", loc(f"{PB}pride", f"[{PB}GetPride]"), L.HONOUR_TEXT_X, L.PRIDE_Y + 1, L.W - L.HONOUR_TEXT_X - 12, 18, tooltip=EMU_TT)
text("lagging", loc(f"{PB}lagging", f"[{PB}GetLagging]"), L.HONOUR_TEXT_X, L.LAG_Y + 1, L.FAV_X - L.HONOUR_TEXT_X - 8, 18, tooltip=EM.LAG_TT)
text("favourite", loc(f"{PB}favourite", f"[{PB}GetFavourite]"), L.FAV_X + 22, L.LAG_Y + 1, L.W - L.FAV_X - 34, 18, tooltip=EM.FAV_GUI_TT)
text("spartakiad", loc(f"{PB}spartakiad", f"[{PB}GetSpartakiad]"), L.HONOUR_TEXT_X, L.SPART_Y + 1, 380, 18, tooltip=EM.SP_TT)


def gui_file():
    L_ = ["guiTypes = {", "containerWindowType = {", f'name = "{WINDOW}"', f"size = {{ width = {L.W} height = {L.H} }}",
          "position = { x = 4 y = 0 }"] + GUI_EL + ["}", "}"]
    return '# IMPERIA CW — Cold War: COLDWAR SOV generator generated content.\n## COLDWAR | The Politburo dossier (decision category GUI). Generated by cw_pbgui.py - edit the generator.\n' + "\n".join(block(L_)) + "\n"


def scripted_gui_file():
    L_ = ["scripted_gui = {", f"{GUI} = {{", "context_type = decision_category", f'window_name = "{WINDOW}"', "properties = {"]
    for el, p in PROPS.items():
        L_.append(f"{el} = {{ {p} }}")
    L_ += ["}", "triggers = {"]
    for k, body in TRIGS.items():
        L_ += [f"{k} = {{"] + list(body) + ["}"]
    L_ += ["}", "}", "}"]
    return HEADER + "\n".join(block(L_)) + "\n"


TEXTURES = {   # sprite -> (texture file in the mod, art/dds source)
    f"GFX_{PB}dossier": "politburo_dossier", f"GFX_{PB}photo_corners_large": "photo_corners_large",
    f"GFX_{PB}photo_corners_small": "photo_corners_small", UNKNOWN: "portrait_unknown",
}
for _k in ("for", "against", "abstain", "pending", "vacant", "adopted", "rejected"):
    TEXTURES[f"GFX_{PB}stamp_{_k}"] = f"stamp_{_k}"
TEXTURES[f"GFX_{PB}banner_held"] = "banner_held"
TEXTURES[f"GFX_{PB}banner_away"] = "banner_away"
for _i, _m in enumerate(MARKERS):
    TEXTURES[_m] = f"marker_{_i:02d}"


def gfx_file():
    L_ = ["spriteTypes = {"]
    for s, stem in TEXTURES.items():
        L_ += ["spriteType = {", f'name = "{s}"', f'texturefile = "{TEX}/{stem}.dds"', "}"]
    for n, p in sorted(ALL_PORTRAITS.items()):
        L_ += ["spriteType = {", f'name = "{sprite_of(n)}"', f'texturefile = "{p}"', "}"]
    L_.append("}")
    return '# IMPERIA CW — Cold War: COLDWAR SOV generator generated content.\n## COLDWAR | Sprites of the Politburo dossier and the leader portraits it shows. Generated by cw_pbgui.py.\n' + "\n".join(block(L_)) + "\n"


def binaries():
    """mod path -> local file of every texture the dossier needs."""
    return {f"{TEX}/{stem}.dds": os.path.join(ART, stem + ".dds") for stem in TEXTURES.values()}


FILES = {
    "interface/COLDWAR_SOV_1970_politburo.gui": gui_file(),
    "interface/COLDWAR_SOV_1970_politburo.gfx": gfx_file(),
    "common/scripted_guis/COLDWAR_SOV_1970_politburo_gui.txt": scripted_gui_file(),
    "common/scripted_localisation/COLDWAR_SOV_1970_politburo_loc.txt": HEADER + "\n".join(block(SCRIPTED_LOC + EM.SCRIPTED_LOC)) + "\n",
}
EFFECTS_TXT = "\n".join(block(EFFECTS + EM.EFFECTS)) + "\n"
