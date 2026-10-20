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

EFFECTS_TXT = S.build() + "\n" + "\n".join(block(["# ==== offers: the focus only sends the proposal; the partner decides ===================="] + OF.offer_effects())) + "\n"
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
    hdr = "## COLDWAR | Soviet Union 1970 focus icons from gfx/interface/goals (mostly the coldwar folder), registered for the COLDWAR Soviet tree.\n"
    return hdr + "\n".join(a) + "\n", hdr + "\n".join(b) + "\n"


GFX, GFX_SHINE = gfx_files()

# ---------------------------------------------------------------- patches of existing mod files
HIST_SRC = os.path.join(MOD, "history/countries/SOV - Russia.txt")
hist = open(HIST_SRC, encoding="utf-8-sig").read()
assert "\t\tload_focus_tree = mdcw_1970_generic_focus\n" in hist
hist = hist.replace("\t\tload_focus_tree = mdcw_1970_generic_focus\n",
                    "\t\tload_focus_tree = COLDWAR_SOV_1970_focus # COLDWAR | Soviet Union 1970 tree\n", 1)
old_leader = 'create_country_leader = { name = "Leonid Brezhnev" picture = "gfx/Leaders/SOV/SOV_Coldwar_Brezhnev.dds" expire = "1982.11.10" ideology = communist_state }\n'
assert old_leader in hist
hist = hist.replace(old_leader,
                    'create_country_leader = { name = "Leonid Brezhnev" picture = "gfx/Leaders/SOV/SOV_Coldwar_Brezhnev.dds" ideology = communist_state } '
                    '# COLDWAR | no expire: the death event of the tree decides\n', 1)
hist = hist.replace("\t\tset_country_flag = SOV_1985_soviet_republic_autonomies_enabled\n",
                    "\t\tset_country_flag = SOV_1985_soviet_republic_autonomies_enabled\n", 1)
anchor = "\t\t# Warsaw Pact: original faction, membership and research setup.\n"
assert anchor in hist
hist = hist.replace(anchor, "\t\tCOLDWAR_SOV_initialize_1970 = yes # COLDWAR | laws, factions, start spirits, Politburo balance, Union cohesion\n\n" + anchor, 1)
FB_SRC = os.path.join(MOD, "common/scripted_effects/mdcw_1970_focus_tree_effects.txt")
fb = open(FB_SRC, encoding="utf-8-sig").read()
if "COLDWAR_SOV_1970_focus" not in fb:
    anchor = "\t\t\t\t\toriginal_tag = EGY # COLDWAR"
    i = fb.index(anchor)
    j = fb.index("\n", i)
    fb = fb[:j + 1] + "\t\t\t\t\tAND = { original_tag = SOV IMP_is_1970_scenario = yes } # COLDWAR | COLDWAR_SOV_1970_focus\n" + fb[j + 1:]
CWD_SRC = os.path.join(MOD, "common/decisions/mdcw_cold_war_decisions.txt")
cwd = open(CWD_SRC, encoding="utf-8-sig").read()
old = '\t\t\tlog = "[GetDateText]: [Root.GetName]: Decision mdcw_cw_dec_comecon"\n'
assert old in cwd
if "COLDWAR_SOV_comprehensive_programme" not in cwd:
    cwd = cwd.replace(old, old + "\t\t\tif = { limit = { has_country_flag = COLDWAR_SOV_comprehensive_programme } add_political_power = 25 } "
                                 "# COLDWAR | Soviet focus The Comprehensive Programme\n", 1)

# ---------------------------------------------------------------- localisation
MD_LOC_KEYS = set()
for _f in glob.glob(os.path.join(MOD, "localisation/english/**/*.yml"), recursive=True):
    if "COLDWAR_SOV" in _f:
        continue
    for _l in open(_f, encoding="utf-8-sig", errors="replace"):
        _m = re.match(r"^\s+([^\s:#]+):\d*\s", _l)
        if _m:
            MD_LOC_KEYS.add(_m.group(1))


def loc_file():
    dup = [k for k in LOC if k in MD_LOC_KEYS]
    if dup:
        print("skipped existing loc keys:", dup)
    out = ["l_english:", " # COLDWAR | Soviet Union 1970 (focus tree, Politburo of the Republics, ideas, events, decisions). Generated - edit the generator."]
    for k, v in LOC.items():
        if k in MD_LOC_KEYS:
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
    "history/countries/SOV - Russia.txt": hist,
    "common/scripted_effects/mdcw_1970_focus_tree_effects.txt": fb,
    "common/decisions/mdcw_cold_war_decisions.txt": cwd,
}
if __name__ == "__main__":
    for p, t in FILES.items():
        write(p, t)
    write("localisation/english/COLDWAR_SOV_1970_l_english.yml", loc_file(), bom=True)
    print("written", len(FILES) + 1, "files;", len(FO.FOCI) if hasattr(FO, "FOCI") else "", "foci;", len(R.ideas), "ideas;", len(FO.NEW_SPRITES), "new sprites;",
          len(EV.EVENTS) + len(R.offers), "events;", sum(len(v) for v in D.DECS.values()), "decisions;", len(LOC), "loc keys; unhandled", len(R.unhandled))
