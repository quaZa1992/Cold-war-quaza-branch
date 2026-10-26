# IMPERIA CW — Cold War: Soviet Union 1970 content generator.
# COLDWAR | Writes every mod file of the Soviet Union 1970 tree. Run: python3 cw_build.py
import os, re, glob, shutil
from cw_common import *

shutil.rmtree(OUT, ignore_errors=True)

import cw_focus as FO
FOCUS_TXT = FO.focus_file()                    # first: fills the registry (ideas, offers, plenum results)
import cw_effects as E
from cw_effects import R
import cw_offers as OF
import cw_sys_effects as S
import cw_events as EV
import cw_decisions as D
import cw_misc as M
import cw_union as U                           # the Union plan (missions, judgement, joint Union tree); before the gfx (it registers focus icons)
import cw_pbgui as PG                          # the Politburo dossier (decision category GUI); before the events and ideas files (news 38, Pride of the Union)

EFFECTS_TXT = (S.build() + "\n" + "\n".join(block(["# ==== offers: the focus only sends the proposal; the partner decides ===================="] + OF.offer_effects()))
               + "\n\n" + PG.EFFECTS_TXT)
TRIGGERS_TXT = S.triggers()
EVENTS_TXT = M.events_file()
DEC_CAT_TXT = D.categories_file()
DEC_TXT = D.decisions_file()
IDEAS_TXT = M.ideas_file()
DYN_TXT = M.dyn_file()
BOP_TXT = M.bop_file()
OPINION_TXT = M.opinion_file()
TRAITS_TXT = M.traits_file()
SLOC_TXT = M.scripted_loc_file()

# ---------------------------------------------------------------- gfx (focus icons that have no sprite yet)
def gfx_files():
    a, b = ["spriteTypes = {"], ["spriteTypes = {"]
    for name, path in sorted(FO.NEW_SPRITES.items()):
        a += ["\tspriteType = {", f'\t\tname = "{name}"', f'\t\ttexturefile = "{path}"', "\t}"]
        b += ["\tspriteType = {", f'\t\tname = "{name}_shine"', f'\t\ttexturefile = "{path}"', '\t\teffectFile = "gfx/FX/buttonstate.lua"']
        for rot in ("-90.0", "90.0"):
            b += ["\t\tanimation = {", f'\t\t\tanimationmaskfile = "{path}"', '\t\t\tanimationtexturefile = "gfx/interface/goals/shine_overlay.dds"',
                  f"\t\t\tanimationrotation = {rot}", "\t\t\tanimationlooping = no", "\t\t\tanimationtime = 0.75", "\t\t\tanimationdelay = 0",
                  '\t\t\tanimationblendmode = "add"', '\t\t\tanimationtype = "scrolling"', "\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }",
                  "\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }", "\t\t}"]
        b += ["\t\tlegacy_lazy_load = no", "\t}"]
    a.append("}")
    b.append("}")
    hdr = '# IMPERIA CW — Cold War: COLDWAR SOV generator generated content.\n## COLDWAR | Soviet Union 1970 focus icons from gfx/interface/goals (mostly the coldwar folder), registered for the COLDWAR Soviet tree.\n'
    return hdr + "\n".join(a) + "\n", hdr + "\n".join(b) + "\n"


GFX, GFX_SHINE = gfx_files()

# ---------------------------------------------------------------- event pictures of our own (MD event frame: 217 x 163, photo 180 x 150)
EVENT_PICTURES = {
    "GFX_report_event_COLDWAR_SOV_politburo_table": "gfx/event_pictures/coldwar_1970/COLDWAR_SOV_politburo_table.dds",
    "GFX_COLDWAR_SOV_politburo_session": "gfx/event_pictures/coldwar_1970/COLDWAR_SOV_politburo_session.dds",
}
EVENT_GFX = ('# IMPERIA CW — Cold War: COLDWAR SOV generator generated content.\n## COLDWAR | Soviet Union 1970 event pictures (MD frame format). Generated - edit the generator.\nspriteTypes = {\n'
             + "".join(f'\tspriteType = {{\n\t\tname = "{n}"\n\t\ttexturefile = "{p}"\n\t}}\n' for n, p in sorted(EVENT_PICTURES.items())) + "}\n")

# ---------------------------------------------------------------- patches of existing mod files
HIST_SRC = os.path.join(MOD, "history/countries/SOV - Russia.txt")
hist = open(HIST_SRC, encoding="utf-8-sig").read()
# every patch is idempotent: the build works on the original MD file and on an already patched mod file
TREE_LINE = "\t\tload_focus_tree = COLDWAR_SOV_1970_focus # COLDWAR | Soviet Union 1970 tree\n"
if TREE_LINE not in hist:
    assert "\t\tload_focus_tree = mdcw_1970_generic_focus\n" in hist
    hist = hist.replace("\t\tload_focus_tree = mdcw_1970_generic_focus\n", TREE_LINE, 1)
old_leader = 'create_country_leader = { name = "Leonid Brezhnev" picture = "gfx/Leaders/SOV/SOV_Coldwar_Brezhnev.dds" expire = "1982.11.10" ideology = communist_state }\n'
new_leader = ('create_country_leader = { name = "Leonid Brezhnev" picture = "gfx/Leaders/SOV/SOV_Coldwar_Brezhnev.dds" ideology = communist_state } '
              '# COLDWAR | no expire: the death event of the tree decides\n')
if new_leader not in hist and old_leader in hist:
    hist = hist.replace(old_leader, new_leader, 1)
# since 19.10.2026 another session's "HISTORICAL1970 NATIVE IDENTITY" block creates Brezhnev itself, without expire: nothing to patch then
assert new_leader in hist or ('name = "Leonid Brezhnev"' in hist and 'expire = "1982.11.10"' not in hist), "Brezhnev must not expire (the death event decides)"
INIT_LINE = "\t\tCOLDWAR_SOV_initialize_1970 = yes # COLDWAR | laws, factions, start spirits, Politburo balance, Union cohesion\n"
anchor = "\t\t# Warsaw Pact: original faction, membership and research setup.\n"
if INIT_LINE not in hist:
    assert anchor in hist
    hist = hist.replace(anchor, INIT_LINE + "\n" + anchor, 1)
# the KGB at the start (17.10.2026): created before the init, which then sets the KGB faction opinion to its start value
KGB_BLOCK = '\t\t# IMPERIA CW — Cold War: COLDWAR SOV generator generated content.\n\t\t# COLDWAR | The Soviet Union starts 1970 with the KGB (Committee for State Security, chaired by Andropov since 1967).\n\t\t# Created before COLDWAR_SOV_initialize_1970 so the KGB faction opinion is still set to its start value there.\n\t\tif = {\n\t\t\tlimit = { has_dlc = "La Resistance" }\n\t\t\tcreate_intelligence_agency = {\n\t\t\t\tname = "Committee for State Security (KGB)"\n\t\t\t\ticon = GFX_intelligence_agency_logo_kgb_soviet_agency\n\t\t\t}\n\t\t\tset_country_flag = MD_skip_treasury_cost\n\t\t\tupgrade_intelligence_agency = upgrade_form_department # 8th Chief Directorate (ciphers and government communications)\n\t\t\tupgrade_intelligence_agency = upgrade_crypto_strength\n\t\t\tupgrade_intelligence_agency = upgrade_passive_defense # Second Chief Directorate (counter-intelligence)\n\t\t\tupgrade_intelligence_agency = upgrade_passive_defense\n\t\t\tupgrade_intelligence_agency = upgrade_invisible_ink # First Chief Directorate (foreign intelligence)\n\t\t\tupgrade_intelligence_agency = upgrade_invisible_ink\n\t\t\tupgrade_intelligence_agency = upgrade_training_centers # Higher School of the KGB\n\t\t\tupgrade_intelligence_agency = upgrade_diplo_training # legal residencies under embassy cover\n\t\t\tclr_country_flag = MD_skip_treasury_cost\n\t\t}\n\n'
if 'name = "Committee for State Security (KGB)"' not in hist:
    hist = hist.replace(INIT_LINE, KGB_BLOCK + INIT_LINE, 1)
FB_SRC = os.path.join(MOD, "common/scripted_effects/mdcw_1970_focus_tree_effects.txt")
fb = open(FB_SRC, encoding="utf-8-sig").read()
if "COLDWAR_SOV_1970_focus" not in fb:
    anchor = "\t\t\t\t\toriginal_tag = EGY # COLDWAR"
    i = fb.index(anchor)
    j = fb.index("\n", i)
    fb = fb[:j + 1] + "\t\t\t\t\tAND = { original_tag = SOV IMP_is_1970_scenario = yes } # COLDWAR | COLDWAR_SOV_1970_focus\n" + fb[j + 1:]
# the joint Union tree hangs into the generic 1970 tree too (the 14 Union republics use it; allow_branch hides it from everybody else).
# The line must never ship without common/national_focus/COLDWAR_UNI_1970_union_joint.txt: a missing shared focus crashes the game.
GEN_SRC = os.path.join(MOD, "common/national_focus/mdcw_1970_generic_focus.txt")
gen = open(GEN_SRC, encoding="utf-8-sig").read()
GEN_LINE = ("\tshared_focus = COLDWAR_UNI_the_union_plan # COLDWAR | the joint Union tree (Soviet generator, cw_union.py); "
            "shown to the Soviet Union and the 14 Union republics only\n")
if GEN_LINE not in gen:
    assert "shared_focus = COLDWAR_UNI_the_union_plan" not in gen
    anchor = "\tinitial_show_position = { focus = GEN_1970_reform_the_government }\n"
    assert anchor in gen
    gen = gen.replace(anchor, anchor + GEN_LINE, 1)
# the Comecon refund is paid by COLDWAR_SOV_monthly_comecon_refund; the generated Cold War decision file stays untouched
CWD_SRC = os.path.join(MOD, "common/decisions/mdcw_cold_war_decisions.txt")
cwd = open(CWD_SRC, encoding="utf-8-sig").read()
assert "COLDWAR_SOV" not in cwd

# ---------------------------------------------------------------- localisation
MD_LOC_KEYS = set()
for _f in glob.glob(os.path.join(MOD, "localisation/english/**/*.yml"), recursive=True):
    if "COLDWAR_SOV" in _f or "COLDWAR_UNI" in _f:
        continue
    for _l in open(_f, encoding="utf-8-sig", errors="replace"):
        _m = re.match(r"^\s+([^\s:#]+):\d*\s", _l)
        if _m:
            MD_LOC_KEYS.add(_m.group(1))


import cw_layout as _CL
for _k, _v in _CL.NEW_LOC.items():
    LOC.setdefault(_k, _v)


def is_uni(k):
    return k.startswith("COLDWAR_UNI")


def loc_file(uni=False):
    dup = [k for k in LOC if k in MD_LOC_KEYS]
    if dup and not uni:
        print("skipped existing loc keys:", dup)
    title = ("The Union Plan 1970 (missions of the Union republics, Moscow's judgement, the joint Union tree)" if uni else
             "Soviet Union 1970 (focus tree, Politburo of the Republics, ideas, events, decisions)")
    out = ['l_english:\n# IMPERIA CW — Cold War: COLDWAR SOV generator English localisation.', f" # COLDWAR | {title}. Generated - edit the generator."]
    for k, v in LOC.items():
        if k in MD_LOC_KEYS or is_uni(k) != uni:
            continue
        v = str(v).replace("\n", "\\n").replace('"', "'")
        out.append(f' {k}:0 "{v}"')
    return "\n".join(out) + "\n"


FILES = {
    "common/national_focus/COLDWAR_SOV_1970_focus.txt": FOCUS_TXT,
    "common/ideas/COLDWAR_SOV_1970_ideas.txt": IDEAS_TXT,
    "common/dynamic_modifiers/COLDWAR_SOV_1970_dynamic_modifiers.txt": DYN_TXT,
    "common/bop/COLDWAR_SOV_1970_politburo.txt": BOP_TXT,
    "common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt": EFFECTS_TXT,
    "common/scripted_triggers/COLDWAR_SOV_1970_scripted_triggers.txt": TRIGGERS_TXT,
    "common/scripted_localisation/COLDWAR_SOV_1970_scripted_localisation.txt": SLOC_TXT,
    "common/decisions/categories/COLDWAR_SOV_1970_decision_categories.txt": DEC_CAT_TXT,
    "common/decisions/COLDWAR_SOV_1970_decisions.txt": DEC_TXT,
    "common/opinion_modifiers/COLDWAR_SOV_1970_opinion_modifiers.txt": OPINION_TXT,
    "common/country_leader/COLDWAR_SOV_1970_traits.txt": TRAITS_TXT,
    "common/on_actions/COLDWAR_SOV_1970_on_actions.txt": M.ON_ACTIONS,
    "events/COLDWAR_SOV_1970_events.txt": EVENTS_TXT,
    "interface/COLDWAR_SOV_1970_goals.gfx": GFX,
    "interface/COLDWAR_SOV_1970_goals_shine.gfx": GFX_SHINE,
    "interface/COLDWAR_SOV_1970_event_pictures.gfx": EVENT_GFX,
    "history/countries/SOV - Russia.txt": hist,
    "common/scripted_effects/mdcw_1970_focus_tree_effects.txt": fb,
    "common/decisions/mdcw_cold_war_decisions.txt": cwd,   # restores the original (an earlier build had patched it)
    "common/national_focus/mdcw_1970_generic_focus.txt": gen,
}
FILES.update(U.FILES)
FILES.update(PG.FILES)
BINARIES = PG.binaries()                       # textures of the Politburo dossier (painted by art/politburo_art.py)
BINARIES["gfx/event_pictures/coldwar_1970/COLDWAR_SOV_politburo_session.dds"] = os.path.join(
    HERE, "art", "dds", "COLDWAR_SOV_politburo_session.dds")

# ---------------------------------------------------------------- tooltips (Enes, 18.10.2026: no raw names anywhere)
# 1. Variable bookkeeping is never shown: every flat set/add/subtract/multiply/divide/clamp_variable without its own tooltip
#    runs inside hidden_effect (same behaviour, no tooltip line). Only our generated script files, never the patched MD files.
VAR_OP = re.compile(r"\b(?:set_variable|add_to_variable|subtract_from_variable|multiply_variable|divide_variable|clamp_variable) = \{ [^{}\n]* \}")


def hide_var_ops(text):
    return VAR_OP.sub(lambda m: m.group(0) if "tooltip" in m.group(0) else "hidden_effect = { " + m.group(0) + " }", text)


for _p in list(FILES):
    if os.path.basename(_p).startswith("COLDWAR_") and _p.endswith(".txt") and _p.split("/")[1] in (
            "national_focus", "decisions", "scripted_effects", "on_actions", "bop") or _p.startswith("events/COLDWAR_"):
        FILES[_p] = hide_var_ops(FILES[_p])
# 2. every COLDWAR flag and variable gets a readable localisation key (cw_names): nothing can show up raw
import cw_names as NM
NM.add_name_loc([t for _p, t in FILES.items() if _p.endswith(".txt")])
if __name__ == "__main__":
    for p, t in FILES.items():
        write(p, t)
    for p, src in BINARIES.items():
        os.makedirs(os.path.dirname(os.path.join(OUT, p)), exist_ok=True)
        shutil.copyfile(src, os.path.join(OUT, p))
    write("localisation/english/COLDWAR_SOV_1970_l_english.yml", loc_file(), bom=True)
    write("localisation/english/COLDWAR_UNI_1970_l_english.yml", loc_file(uni=True), bom=True)
    print("union plan:", len(U.JF), "joint foci,", len(U.UMISSIONS) + 1, "missions,", len(U.UDECS[U.CAT]), "decisions,", len(U.UEV), "events,",
          len(U.UIDEAS), "ideas,", sum(1 for k in LOC if is_uni(k)), "loc keys")
    print("written", len(FILES) + 2, "files;", len(FO.FOCI) if hasattr(FO, "FOCI") else "", "foci;", len(R.ideas), "ideas;", len(FO.NEW_SPRITES), "new sprites;",
          len(EV.EVENTS) + len(R.offers), "events;", sum(len(v) for v in D.DECS.values()), "decisions;", len(LOC), "loc keys; unhandled", len(R.unhandled))
