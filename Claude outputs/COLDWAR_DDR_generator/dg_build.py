# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Writes every mod file of the German Democratic Republic 1970 tree. Run: python3 dg_build.py
import os, re, glob, shutil
from dg_common import *

shutil.rmtree(OUT, ignore_errors=True)

import dg_focus as FO
FOCUS_TXT = FO.focus_file()                    # first: fills the registry (ideas, offers, flags, events)
import dg_effects as E
from dg_effects import R
import dg_offers as OF
import dg_decisions as D
import dg_sys as S
import dg_misc as M
import dg_avail as A
from dg_load import PARTY, SUBIDEO

EFFECTS_TXT = S.build() + "\n" + "\n".join(block(D.plan_effects())) + "\n"
TRIGGERS_TXT = S.triggers()
DEC_CAT_TXT = D.categories_file()
DEC_TXT = D.decisions_file()
EVENTS_TXT = M.events_file()
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
    hdr = '# IMPERIA CW — Cold War: COLDWAR DDR generator generated content.\n## COLDWAR | German Democratic Republic 1970: focus icons from gfx/interface/goals (mostly coldwar, DDR, germany) registered for the COLDWAR GDR tree.\n'
    return hdr + "\n".join(a) + "\n", hdr + "\n".join(b) + "\n"


GFX, GFX_SHINE = gfx_files()

# Native MD country-event photo box; the archived binary is exported by
# tools/event_art/export_ddr_intro.py without changing the global event GUI.
EVENT_GFX = ('# IMPERIA CW — Cold War: COLDWAR DDR generator generated content.\n## COLDWAR | DDR1970 country-event pictures.\nspriteTypes = {\n\tspriteType = {\n\t\tname = "GFX_COLDWAR_DDR_intro"\n\t\ttexturefile = "gfx/event_pictures/coldwar_1970/COLDWAR_DDR_intro.dds"\n\t}\n}\n')

# ---------------------------------------------------------------- party names (MD politics view and the MDCW historical party registry)
PARTY_DESC = {
    0: "The hard-currency empire of Alexander Schalck-Golodkowski: Commercial Coordination, founded in 1966 under the wing of the MfS, would run the republic like a firm that sells to the West.",
    1: "The Christian Democratic Union in the GDR, a bloc party of the National Front since 1949 - Christians who accept socialism, and some who only wait.",
    2: "The Liberal Democratic Party of Germany, the bloc party of craftsmen, shopkeepers and the old middle class. Manfred Gerlach's liberals remember 1945.",
    3: "The social democrats forced into the SED in 1946 never quite disappeared - in the factories, in the families and on the West's radio.",
    4: "The Socialist Unity Party of Germany, the leading party of the working class and of the state since 1949.",
    5: "Robert Havemann's heretics: communists who want socialism with free speech, free elections and no Wall.",
    6: "The hardliners of the old KPD tradition around Alfred Neumann, for whom every reform is already one too many.",
    7: "Erich Mielke's Ministry for State Security sees itself as the shield and sword of the party - and sometimes as the party itself.",
    13: "The technocrats of the State Planning Commission under Gerhard Schürer, who know how bad the figures really are.",
    14: "The Federation of Protestant Churches under Bishop Albrecht Schönherr: 'not against, not beside, but in socialism'.",
    15: "The general directors of the great Kombinate, who run the economy and would like to run the state.",
    16: "The master craftsmen and the last private and semi-state firms - nationalised in 1972, but not forgotten.",
    17: "Environmentalists around Reimar Gilsenbach who count the dead forests of the Ore Mountains and the sulphur over Bitterfeld.",
    18: "The Democratic Farmers' Party of Germany, the bloc party of the cooperative farmers.",
    19: "Wolfgang Harich's platform for a democratic, neutral, reunited socialist Germany between the blocs.",
    20: "The National Democratic Party of Germany, founded in 1948 for former soldiers and Nazi party members, now the bloc party of the national question.",
    21: "A national-revolutionary underground that dreams of a Germany neither Eastern nor Western.",
    22: "The generals of the National People's Army in Strausberg, who see themselves as the last guarantors of order.",
    23: "Monarchists around Louis Ferdinand, Prince of Prussia, head of the House of Hohenzollern - a dream of Prussia restored.",
}
PARTY_LOC = {}
for i, p in sorted(PARTY.items()):
    PARTY_LOC[f"{PFX}1970_party_{i}"] = p["name"]
    PARTY_LOC[f"{PFX}1970_party_{i}_desc"] = PARTY_DESC[i] + f"\\n\\nLeader: {E.LEADER_DISPLAY.get(p['leader'], p['leader'])}"
MARK = "# COLDWAR | GDR 1970"
TRIG_LINE = "original_tag = DDR IMP_is_1970_scenario = yes"


def party_line(i, desc=False):
    return f"\ttext = {{ trigger = {{ {TRIG_LINE} }} localization_key = {PFX}1970_party_{i}{'_desc' if desc else ''} }} {MARK}\n"


def patch_defined_texts(src, names_for, after_name):
    """insert our line as the first text of every defined_text named in names_for (idempotent)"""
    have = sorted(l.strip() for l in src.splitlines() if MARK in l)
    if have and have == sorted(l.strip() for l in names_for.values()):
        return src                     # our lines are all there already: leave the team's file as it is
    if MARK in src:
        src = "".join(l for l in src.splitlines(keepends=True) if MARK not in l)   # rebuild from the original
    out, i = src, 0
    for name, line in names_for.items():
        if after_name:
            pat = re.compile(r"^(\s*name = " + re.escape(name) + r"\s*\n)", re.M)
            m = pat.search(out)
            assert m, name
            out = out[:m.end()] + line + out[m.end():]
        else:
            # the text entries may stand before the name: insert right after the opening of the block that holds the name
            m = re.search(r"^\s*name = " + re.escape(name) + r"\s*$", out, re.M)
            assert m, name
            start = out.rfind("defined_text = {", 0, m.start())
            j = out.index("\n", start) + 1
            out = out[:j] + line + out[j:]
    return out


PV_SRC = os.path.join(MOD, "common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt")
pv = open(PV_SRC, encoding="utf-8-sig").read()
names = {}
for i in PARTY:
    names[f"{SUBIDEO[i]}_L"] = party_line(i)
    names[f"{SUBIDEO[i]}_L_desc"] = party_line(i, True)
pv = patch_defined_texts(pv, names, after_name=False)
HP_SRC = os.path.join(MOD, "common/scripted_localisation/mdcw_historical_parties.txt")
hp = open(HP_SRC, encoding="utf-8-sig").read()
names = {}
for i in PARTY:
    names[f"MDCW_HP_{SUBIDEO[i]}"] = party_line(i)
    names[f"MDCW_HP_{SUBIDEO[i]}_desc"] = party_line(i, True)
hp = patch_defined_texts(hp, names, after_name=True)

# ---------------------------------------------------------------- history and the fallback tree
HIST_SRC = os.path.join(MOD, "history/countries/DDR - East Germany.txt")
hist = open(HIST_SRC, encoding="utf-8-sig").read()
HIST_ORIG = hist
TREE_LINE = "\t\tload_focus_tree = COLDWAR_DDR_1970_focus # COLDWAR | German Democratic Republic 1970 tree\n"
INIT_LINE = "\t\tCOLDWAR_DDR_initialize_1970 = yes # COLDWAR | laws, factions, start spirits, parties, Moscow's Trust, the Inner-German course\n"
if TREE_LINE not in hist:
    assert "\t\tload_focus_tree = mdcw_1970_generic_focus\n" in hist
    hist = hist.replace("\t\tload_focus_tree = mdcw_1970_generic_focus\n", TREE_LINE, 1)
# Ulbricht: the team's 1970 identity block creates him without expire (the Central Committee and the death event decide);
# a leftover comment line of the old leader patch is removed
hist = "".join(l for l in hist.splitlines(keepends=True) if l.strip() != "# COLDWAR | no expire: the Central Committee and the death event of the tree decide")
assert 'name = "Walter Ulbricht"' in hist and "expire" not in hist.split("COLDWAR HISTORICAL1970 NATIVE IDENTITY END")[0], "Ulbricht must be created without expire"
if INIT_LINE not in hist:
    anchor = "\t\tadd_ideas = mdcw_ni_guest_worker_recruitment_programme\n"
    assert anchor in hist
    hist = hist.replace(anchor, anchor + "\n" + INIT_LINE, 1)
FB_SRC = os.path.join(MOD, "common/scripted_effects/mdcw_1970_focus_tree_effects.txt")
fb = open(FB_SRC, encoding="utf-8-sig").read()
if "COLDWAR_DDR_1970_focus" not in fb:
    anchor = "\t\t\t\t\tAND = { original_tag = SOV IMP_is_1970_scenario = yes } # COLDWAR | COLDWAR_SOV_1970_focus\n"
    assert anchor in fb
    fb = fb.replace(anchor, anchor + "\t\t\t\t\tAND = { original_tag = DDR IMP_is_1970_scenario = yes } # COLDWAR | COLDWAR_DDR_1970_focus\n", 1)

# ---------------------------------------------------------------- localisation
MD_LOC_KEYS = md_loc_keys()


def loc_file(entries, title):
    out = ['l_english:\n# IMPERIA CW — Cold War: COLDWAR DDR generator English localisation.', f" # COLDWAR | {title}. Generated - edit the generator (Claude outputs/COLDWAR_DDR_generator)."]
    for k, v in entries.items():
        v = str(v).replace("\n", "\\n").replace('"', "'").replace("Erich's Krönung", "Erichs Krönung")
        out.append(f' {k}: "{v}"')
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- search filters (MD: FOCUS_FILTER_RUSSIA_* = loc + GFX_FOCUS_FILTER_* sprite)
for fk, (fname, _) in FO.FILTERS.items():
    LOC[fk] = fname
FILTER_GFX = (HEADER.replace("##", "#") + "spriteTypes = {\n" +
              "".join(f'\tspriteType = {{\n\t\tname = "GFX_{fk}"\n\t\ttextureFile = "{tex}"\n\t}}\n' for fk, (_, tex) in FO.FILTERS.items()) + "}\n")


# ---------------------------------------------------------------- shared modifier tooltips of all COLDWAR trees (merged, idempotent)
def shared_tooltips():
    path = os.path.join(MOD, SHARED_TT_FILE)
    have = collections.OrderedDict()
    if os.path.exists(path):
        for line in open(path, encoding="utf-8-sig"):
            m = re.match(r'^\s+([A-Za-z0-9_.]+):\d*\s+"(.*)"\s*$', line)
            if m:
                have[m.group(1)] = m.group(2)
    for k, v in SHARED_TT.items():
        have.setdefault(k, v)
    out = ['l_english:\n# IMPERIA CW — Cold War: COLDWAR DDR generator English localisation.', " # COLDWAR | Modifier tooltips of the COLDWAR focus trees for keys without an MD tooltip (or with a wrong MD colour).",
           " # MD format: <Label>: $RIGHT|+=%1$ (green when it rises) / -=%1 (green when it falls). Shared by all trees: reuse keys, add missing ones."]
    for k in sorted(have):
        out.append(f' {k}: "{have[k]}"')
    return "\n".join(out) + "\n"


def ordered_loc(entries):
    """MD order (MD_focus_SOV_l_english.yml): tree name, shortcuts, filters, then every focus with its description, then the rest"""
    keys = list(entries)
    first = [TREE_ID] + [k for k in keys if k.endswith("_tree_shortcut")] + [k for k in keys if k.startswith("FOCUS_FILTER_")]
    foci = []
    for f in FO.FOCI:
        foci += [f["id"], f["id"] + "_desc"]
    head = [k for k in first + foci if k in entries]
    hs = set(head)
    return collections.OrderedDict((k, entries[k]) for k in head + [k for k in keys if k not in hs])


FILES = {
    "common/national_focus/COLDWAR_DDR_1970_focus.txt": FOCUS_TXT,
    "common/ideas/COLDWAR_DDR_1970_ideas.txt": IDEAS_TXT,
    "common/dynamic_modifiers/COLDWAR_DDR_1970_dynamic_modifiers.txt": DYN_TXT,
    "common/bop/COLDWAR_DDR_1970_inner_german_course.txt": BOP_TXT,
    "common/scripted_effects/COLDWAR_DDR_1970_scripted_effects.txt": EFFECTS_TXT,
    "common/scripted_triggers/COLDWAR_DDR_1970_scripted_triggers.txt": TRIGGERS_TXT,
    "common/scripted_localisation/COLDWAR_DDR_1970_scripted_localisation.txt": SLOC_TXT,
    "common/decisions/categories/COLDWAR_DDR_1970_decision_categories.txt": DEC_CAT_TXT,
    "common/decisions/COLDWAR_DDR_1970_decisions.txt": DEC_TXT,
    "common/opinion_modifiers/COLDWAR_DDR_1970_opinion_modifiers.txt": OPINION_TXT,
    "common/country_leader/COLDWAR_DDR_1970_traits.txt": TRAITS_TXT,
    "common/on_actions/COLDWAR_DDR_1970_on_actions.txt": M.ON_ACTIONS,
    "events/COLDWAR_DDR_1970_events.txt": EVENTS_TXT,
    "interface/COLDWAR_DDR_1970_goals.gfx": GFX,
    "interface/COLDWAR_DDR_1970_goals_shine.gfx": GFX_SHINE,
    "interface/COLDWAR_DDR_1970_focus_filters.gfx": FILTER_GFX,
    "interface/COLDWAR_DDR_1970_event_pictures.gfx": EVENT_GFX,
    "history/countries/DDR - East Germany.txt": hist,
    "common/scripted_effects/mdcw_1970_focus_tree_effects.txt": fb,
    "common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt": pv,
    "common/scripted_localisation/mdcw_historical_parties.txt": hp,
}
# Script files are UTF-8 without BOM. Only localisation below uses a BOM.
from dg_quality import runtime_files
FILES.update(runtime_files())

if __name__ == "__main__":
    PATCHED = {"history/countries/DDR - East Germany.txt", "common/scripted_effects/mdcw_1970_focus_tree_effects.txt",
               "common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt", "common/scripted_localisation/mdcw_historical_parties.txt"}
    for p, t in FILES.items():
        if p in PATCHED and open(os.path.join(MOD, p), encoding="utf-8-sig").read() == t:
            print("unchanged (not written):", p)
            continue
        write(p, t, bom=p.endswith('.yml'))
    event_art = "gfx/event_pictures/coldwar_1970/COLDWAR_DDR_intro.dds"
    os.makedirs(os.path.dirname(os.path.join(OUT, event_art)), exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "art", "dds", "COLDWAR_DDR_intro.dds"), os.path.join(OUT, event_art))
    dup = [k for k in LOC if k in MD_LOC_KEYS]
    main = collections.OrderedDict((k, v) for k, v in LOC.items() if k not in MD_LOC_KEYS)
    write("localisation/english/COLDWAR_DDR_1970_l_english.yml",
          loc_file(ordered_loc(main), "German Democratic Republic 1970 (focus tree, ideas, events, decisions, offers)"), bom=True)
    write(SHARED_TT_FILE, shared_tooltips(), bom=True)
    write("localisation/english/COLDWAR_DDR_1970_parties_l_english.yml", loc_file(PARTY_LOC, "German Democratic Republic 1970: party names"), bom=True)
    print("skipped existing loc keys:", dup)
    print("written", len(FILES) + 2, "files;", len(FO.FOCI) if hasattr(FO, "FOCI") else "", "foci;", len(R.ideas), "ideas;", len(FO.NEW_SPRITES), "new sprites;",
          len(M.EV.EVENTS) + len(R.offers), "events;", sum(len(v) for v in D.DECS.values()), "decisions;", len(LOC), "loc keys;",
          "dropped date clauses", len(A.DROPPED), "unknown", len(A.UNKNOWN))
