# IMPERIA CW — Cold War: Soviet Union 1970 content generator.
# COLDWAR | Static validation of the generated Soviet Union 1970 files. Run after cw_build.py: python3 validate_sov.py
import re, os, json, collections, glob, sys
from cw_common import OUT, MOD, EGY

IDX = json.load(open(next(p for p in (os.path.join(MOD, "tools/generic_1970_focus_tree/idx_mdcw.json"),
                                      "/home/claude/gentools/generic_1970_focus_tree/idx_mdcw.json") if os.path.exists(p))))
T = {os.path.relpath(f, OUT): open(f, encoding="utf-8-sig").read() for f in glob.glob(OUT + "/**/*", recursive=True)
     if os.path.isfile(f) and not f.endswith((".dds", ".png", ".tga"))}
errs, warns = [], []


def err(*a):
    errs.append(" ".join(str(x) for x in a))


def warn(*a):
    warns.append(" ".join(str(x) for x in a))


OWN = {p: t for p, t in T.items() if "COLDWAR_SOV" in p or "COLDWAR_UNI" in p}
X = r"COLDWAR_(?:SOV|UNI)_"   # our two prefixes: the Soviet tree and the Union plan (cw_union.py)
code = "\n".join(t for p, t in OWN.items() if not p.endswith((".yml", ".gfx")))
F = lambda name: T[name]

# 1 braces, quotes, line endings
for p, t in T.items():
    if p.endswith(".yml"):
        continue
    body = re.sub(r'"[^"\n]*"', '""', t)
    body = re.sub(r"#.*", "", body)
    d = 0
    for ch in body:
        d += ch == "{"
        d -= ch == "}"
        if d < 0:
            err("negative depth", p)
            break
    if d:
        err("unbalanced", p, d)
    if t.count('"') % 2:
        err("odd quotes", p)
    if "\r" in t:
        err("CRLF", p)

# 2 localisation
LOC = {}
for yml in ("COLDWAR_SOV_1970_l_english.yml", "COLDWAR_UNI_1970_l_english.yml"):
  raw = open(os.path.join(OUT, "localisation/english", yml), "rb").read()
  if not raw.startswith(b"\xef\xbb\xbf"):
    err("loc without BOM", yml)
  for line in raw.decode("utf-8-sig").splitlines()[1:]:
    m = re.match(r'^ ([^\s:]+):0 "(.*)"$', line)
    if m:
        if m.group(1) in LOC:
            err("dup loc", m.group(1))
        LOC[m.group(1)] = m.group(2)
        if m.group(1).startswith("COLDWAR_UNI") != yml.startswith("COLDWAR_UNI"):
            err("loc key in the wrong file", yml, m.group(1))
    elif line.strip() and not line.strip().startswith("#"):
        err("bad loc line", line[:80])
    if re.search(r"[äöüÄÖÜß„“]", line):
        err("German characters in loc", line[:90])
MDLOC = set()
for f in glob.glob(os.path.join(MOD, "localisation/english/**/*.yml"), recursive=True):
    if "COLDWAR_SOV" in os.path.basename(f) or "COLDWAR_UNI" in os.path.basename(f):   # an older deployed copy of our own file must not hide missing keys
        continue
    for line in open(f, encoding="utf-8-sig", errors="replace"):
        m = re.match(r"^\s+([^\s:#]+):\d*\s", line)
        if m:
            MDLOC.add(m.group(1))
ALLLOC = set(LOC) | MDLOC | {"modifies_dynamic_modifier_tt"}   # vanilla key, used by MD code
focus = F("common/national_focus/COLDWAR_SOV_1970_focus.txt")
ids = re.findall(r"^\t\tid = (\w+)", focus, re.M)
if not (len(ids) == len(set(ids)) == 836):
    err("focus count", len(ids), len(set(ids)))
for i in ids:
    for k in (i, i + "_desc"):
        if k not in LOC:
            err("missing loc", k)
for k in set(re.findall(r"custom_effect_tooltip = (\w+)", code)) | set(re.findall(r"\btooltip = (\w+)", code)) | \
        set(re.findall(r"localization_key = (\w+)", code)) | set(re.findall(r"name = (COLDWAR_SOV_shortcut_\w+)", code)) - {"modifies_dynamic_modifier_tt"}:
    if k not in ALLLOC and not k.startswith("GFX_"):   # a defined_text may return a sprite name (the Politburo dossier portraits)
        err("missing tooltip loc", k)
for k in set(re.findall(r"add_tech_bonus = \{ name = (\w+)", code)):   # the research screen names the bonus by this key
    if k not in ALLLOC:
        err("missing tech bonus loc", k)
for k in set(re.findall(r"(?:title|desc|name) = (COLDWAR_(?:SOV|UNI)\.\d+\.\w)", code)):
    if k not in LOC:
        err("missing event loc", k)
# scripted localisation used in loc strings
sloc = set(re.findall(r"name = (COLDWAR_(?:SOV|UNI)_\w+)", "\n".join(t for p_, t in T.items() if p_.startswith("common/scripted_localisation/COLDWAR_"))))
for v in LOC.values():
    for m in re.findall(r"\[(?:\w+\.)?(COLDWAR_(?:SOV|UNI)_\w+)\]", v):
        if m not in sloc:
            err("unknown scripted loc", m)
    if v.count("[") != v.count("]"):
        err("bracket mismatch in loc", v[:60])
    if v.count("§") % 2:
        warn("odd colour codes", v[:70])

# 3 focus structure
for p in set(re.findall(r"focus = (COLDWAR_SOV_\w+)", focus)) | set(re.findall(r"has_completed_focus = (COLDWAR_SOV_\w+)", code)):
    if p not in ids:
        err("unknown focus ref", p)
mx = collections.defaultdict(set)
for m in re.finditer(r"\t\tid = (\w+)(.*?)\n\t}", focus, re.S):
    for mm in re.findall(r"mutually_exclusive = \{([^}]*)\}", m.group(2)):
        mx[m.group(1)] |= set(re.findall(r"focus = (\w+)", mm))
for a, bs in mx.items():
    for b in bs:
        if a not in mx.get(b, ()):
            err("mx asym", a, b)
for m in re.finditer(r"relative_position_id = (\w+)", focus):
    if m.group(1) not in ids:
        err("bad relative id", m.group(1))

# 4 scripted effects / triggers
eff, trg = set(IDX["effects"]), set(IDX["triggers"])
defined = set(re.findall(r"^(COLDWAR_(?:SOV|UNI)_\w+) = \{", F("common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt")
                         + F("common/scripted_effects/COLDWAR_UNI_1970_scripted_effects.txt"), re.M))
dtrig = set(re.findall(r"^(COLDWAR_(?:SOV|UNI)_\w+) = \{", F("common/scripted_triggers/COLDWAR_SOV_1970_scripted_triggers.txt")
                       + F("common/scripted_triggers/COLDWAR_UNI_1970_scripted_triggers.txt"), re.M))
# effects of other mod tools that the generator calls as hooks (e.g. the historical-politics successor tool, MDCW_HP_*)
ext_defined = set()
for f in glob.glob(os.path.join(MOD, "common/scripted_effects/mdcw_historical_*.txt")):
    ext_defined |= set(re.findall(r"^(MDCW_HP_\w+) = \{", open(f, encoding="utf-8-sig", errors="replace").read(), re.M))
VAN_YES = {"has_civil_war", "has_war", "always", "is_ai", "exists", "is_debug", "elections_allowed", "instant_build", "limit_to_border", "all_provinces",
           "major", "is_triggered_only", "fire_only_once", "hidden", "random", "default", "reset_on_civilwar", "is_historical_focus_on",
           "retire_country_leader", "ruling_only", "dismantle_faction", "force_update_dynamic_modifier", "visible_when_empty", "trade",
           "target_non_existing", "is_subject", "has_capitulated", "is_good", "selectable_mission", "mark_focus_tree_layout_dirty",
           "is_coastal", "fixedsize"}
for name in set(re.findall(r"\b([A-Za-z_]\w*) = (?:yes|no)\b", code)):
    if name in VAN_YES or name in defined or name in ext_defined or name in dtrig or name in eff or name in trg:
        continue
    err("unknown yes-call", name)
for name in set(re.findall(r"\b(COLDWAR_(?:SOV|UNI)_\w+) = yes", code)):
    if name not in defined and name not in dtrig:
        err("undefined COLDWAR effect/trigger", name)
for name in defined:
    if not re.search(rf"\b{name} = yes", code):
        warn("effect never used", name)

# 5 ideas, modifiers, dynamic modifiers
mods = set(open(os.path.join(EGY, "our_mods.txt")).read().split()) | set(IDX["moddefs"])
for line in open(os.path.join(MOD, "localisation/english/replace/replaced_from_vanilla_modifiers_l_english.yml"), encoding="utf-8-sig"):
    m = re.match(r"^\s+MODIFIER_([A-Z0-9_]+):", line)
    if m:
        mods.add(m.group(1).lower())
KNOWN_VAN = {"political_power_factor", "stability_factor", "war_support_factor", "research_speed_factor", "trade_opinion_factor", "neutrality_drift",
             "communism_drift", "democratic_drift", "fascism_drift", "nationalist_drift", "production_speed_buildings_factor", "industrial_capacity_factory",
             "consumer_goods_factor", "army_org_factor", "army_morale_factor", "army_attack_factor", "army_defence_factor", "breakthrough_factor",
             "training_time_factor", "conscription", "conscription_factor", "experience_gain_army", "max_planning_factor", "planning_speed",
             "special_forces_cap", "static_anti_air_damage_factor", "monthly_population", "production_factory_efficiency_gain_factor",
             "production_factory_max_efficiency_factor", "foreign_influence_modifier", "foreign_influence_defense_modifier", "air_superiority_efficiency",
             "drift_defence_factor", "navy_max_range_factor", "naval_damage_factor", "navy_org_factor", "army_core_defence_factor", "supply_consumption_factor",
             "production_speed_arms_factory_factor", "production_speed_industrial_complex_factor", "production_speed_infrastructure_factor",
             "production_speed_rail_way_factor", "opinion_gain_monthly_same_ideology_factor", "research_sharing_per_country_bonus_factor",
             "enemy_justify_war_goal_time", "subjects_autonomy_gain", "army_speed_factor", "air_defence_factor", "intelligence_agency_defense",
             "foreign_subversive_activites", "industrial_factory_donation_bonus", "equipment_cost_multiplier_modifier",
             # used by MD's own ideas and dynamic modifiers (engine modifiers)
             "corruption_cost_factor", "military_spending_cost_factor", "production_speed_nuclear_reactor_factor", "industrial_capacity_dockyard"}
used = set()
for p in ("common/ideas/COLDWAR_SOV_1970_ideas.txt", "common/ideas/COLDWAR_UNI_1970_ideas.txt", "common/bop/COLDWAR_SOV_1970_politburo.txt"):
    for blk in re.findall(r"modifier = \{([^{}]*)\}", F(p)):
        used |= set(re.findall(r"(\w+) = ", blk))
dyn = F("common/dynamic_modifiers/COLDWAR_SOV_1970_dynamic_modifiers.txt") + F("common/dynamic_modifiers/COLDWAR_UNI_1970_dynamic_modifiers.txt")
used |= set(re.findall(r"^\t(\w+) = (?:COLDWAR_(?:SOV|UNI)_|-?[\d.])", dyn, re.M))
for t in re.findall(r"random = no\n\n((?:\t\t\w+ = [-\d.]+\n)+)", F("common/country_leader/COLDWAR_SOV_1970_traits.txt") + F("common/country_leader/COLDWAR_UNI_1970_traits.txt")):
    used |= set(re.findall(r"(\w+) = ", t))
# HOI4 creates <idea category>_cost_factor for every idea category (MD uses e.g. social_budget_cost_factor)
for f in glob.glob(os.path.join(MOD, "common/ideas/*.txt")):
    for cat in re.findall(r"^\t(\w+) = \{", open(f, encoding="utf-8-sig", errors="replace").read(), re.M):
        mods.add(cat + "_cost_factor")
for m in used - {"icon"}:
    if m not in mods and m not in KNOWN_VAN:
        err("unknown modifier", m)
    # the tooltip needs a text: vanilla/MD MODIFIER_ key, MD's bare key (custom and idea-category modifiers) or ours,
    # otherwise the game prints the raw key (e.g. imp_national_ideas_3_cost_factor)
    elif m not in KNOWN_VAN and not ({m, "MODIFIER_" + m.upper(), "MODIFIER_" + m} & ALLLOC):
        err("modifier without loc", m)
idea_gfx = set(open(os.path.join(EGY, "idea_gfx.txt")).read().split())
for p in re.findall(r"icon = GFX_idea_([\w-]+)", code) + re.findall(r"^\t\t\tpicture = ([\w-]+)", F("common/ideas/COLDWAR_SOV_1970_ideas.txt") + F("common/ideas/COLDWAR_UNI_1970_ideas.txt"), re.M):
    if p not in idea_gfx:
        err("unknown idea gfx", p)
own_ideas = set(re.findall(r"^\t\t(COLDWAR_(?:SOV|UNI)_\w+) = \{", F("common/ideas/COLDWAR_SOV_1970_ideas.txt") + F("common/ideas/COLDWAR_UNI_1970_ideas.txt"), re.M))
md_ideas = set(IDX["ideas"]) | set(re.findall(r"^\t\t(COLDWAR_EGY_\w+) = \{", open(os.path.join(MOD, "common/ideas/COLDWAR_EGY_1970_ideas.txt"), encoding="utf-8-sig").read(), re.M)) \
    if os.path.exists(os.path.join(MOD, "common/ideas/COLDWAR_EGY_1970_ideas.txt")) else set(IDX["ideas"])
for i in set(re.findall(r"(?:add_ideas|remove_ideas|\bidea|add_idea|remove_idea|has_idea) = (\w+)", code)):
    if i not in own_ideas and i not in md_ideas and not i.startswith("COLDWAR_EGY_"):
        err("unknown idea", i)
for blk in re.findall(r"add_ideas = \{([^}]*)\}", code):
    for i in blk.split():
        if i not in own_ideas and i not in md_ideas:
            err("unknown idea in block", i)
for i in own_ideas:
    if i not in LOC:
        err("idea loc", i)
dyndef = set(re.findall(r"^(COLDWAR_(?:SOV|UNI)_\w+) = \{", dyn, re.M))
for d in set(re.findall(r"\b(?:modifier|MODIFIER) = (COLDWAR_SOV_\w+_(?:modifier|programme))\b", code)) | set(re.findall(r"modifier = (COLDWAR_SOV_cohesion_\w+)", code)) \
        | set(re.findall(r"dynamic_modifier = \{ modifier = (COLDWAR_UNI_\w+) \}", code)):
    if d not in dyndef:
        if d not in set(re.findall(r"^\t(COLDWAR_SOV_\w+) = \{", F("common/opinion_modifiers/COLDWAR_SOV_1970_opinion_modifiers.txt"), re.M)):
            err("unknown dynamic modifier", d)
for d in dyndef:
    if d not in LOC:
        err("dyn loc", d)
# variables behind every dynamic modifier line are set somewhere
for var in set(re.findall(r"^\t\w+ = (COLDWAR_(?:SOV|UNI)_\w+)$", dyn, re.M)):
    if not re.search(rf"\b{var} = ", code.replace(dyn, "")):
        warn("dyn var never changed", var)

# 6 sprites and pictures
spr = set(IDX["sprites"])
KNOWN_TEX = {l.strip().lower() for l in open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools", "device_known_textures.txt"))
             if l.strip() and not l.startswith("#")}
for f in glob.glob(os.path.join(MOD, "interface/*.gfx")):
    if "COLDWAR_SOV" in os.path.basename(f) or "COLDWAR_UNI" in os.path.basename(f):   # a deployed copy of our own sprites
        continue
    spr |= set(re.findall(r'name\s*=\s*"?(GFX_\w+)', open(f, encoding="utf-8", errors="replace").read()))
for p_, t_ in T.items():   # our own generated sprite files (event pictures) count before they are copied into the mod
    if p_.endswith(".gfx") and "goals" not in p_:
        spr |= set(re.findall(r'name\s*=\s*"?(GFX_\w+)', t_))
for p_, t_ in T.items():   # and their textures must exist in the mod
    if p_.endswith(".gfx") and "goals" not in p_:
        for tex in re.findall(r'texturefile = "([^"]+)"', t_):
            if (not os.path.exists(os.path.join(MOD, tex)) and not os.path.exists(os.path.join(OUT, tex)) and tex.lower() not in KNOWN_TEX
                    and tex.lower() not in {x.lower() for x in json.load(open(os.path.join(EGY, "repo_paths.json")))}):
                err("texture missing", tex)
goal = {n for n, p in json.load(open(os.path.join(EGY, "goal_sprites.json")))}
gfx = F("interface/COLDWAR_SOV_1970_goals.gfx")
newspr = set(re.findall(r'name = "(GFX_COLDWAR_goal_\w+)"', gfx))
repo = {p.lower() for p in json.load(open(os.path.join(EGY, "repo_paths.json")))}
for tex in re.findall(r'texturefile = "([^"]+)"', gfx):
    if tex.lower() not in repo:
        err("texture missing", tex)
for ic in re.findall(r"\ticon = (\S+)", focus):
    if ic not in goal and ic not in newspr:
        err("unknown focus icon", ic)
dupe = [n for n in newspr if n in spr]
if dupe:
    err("new sprite names clash with existing sprites", dupe[:5])
evs = F("events/COLDWAR_SOV_1970_events.txt") + F("events/COLDWAR_UNI_1970_events.txt")
for p in set(re.findall(r"picture = (GFX_\w+)", evs)):
    if p not in spr:
        err("unknown event picture", p)
for p in ("common/decisions/COLDWAR_SOV_1970_decisions.txt", "common/decisions/categories/COLDWAR_SOV_1970_decision_categories.txt",
          "common/bop/COLDWAR_SOV_1970_politburo.txt", "common/decisions/COLDWAR_UNI_1970_decisions.txt",
          "common/decisions/categories/COLDWAR_UNI_1970_decision_categories.txt"):
    for ic in set(re.findall(r"icon = (GFX_\w+)", F(p))):
        if ic not in spr:
            err("unknown icon", p, ic)

# 7 events
evdef = set(re.findall(r"^\s*id = (COLDWAR_(?:SOV|UNI)\.\d+)", evs, re.M))
for e in set(re.findall(r"id = (COLDWAR_(?:SOV|UNI)\.\d+)", code)):
    if e not in evdef:
        err("event not defined", e)
for e in evdef:
    if not re.search(rf"id = {re.escape(e)} ", code.replace(evs, "")) and not re.search(rf"id = {re.escape(e)}\b(?! *\n\t*title)", evs):
        n = e.split(".")[1]
        blk = evs[evs.index(f"id = {e}\n"):][:2000]
        if "mean_time_to_happen" not in blk:
            warn("event never fired", e)
for m in re.finditer(r"(?:country_event|news_event) = \{\n\tid = (\S+)(.*?)\n\}", evs, re.S):
    if m.group(2).count("option = {") > 26:
        err("too many options", m.group(1))

# 8 opinion modifiers, traits, tech categories
opdef = set(re.findall(r"^\t(COLDWAR_SOV_\w+) = \{", F("common/opinion_modifiers/COLDWAR_SOV_1970_opinion_modifiers.txt"), re.M))
for o in set(re.findall(r"modifier = (COLDWAR_SOV_\w+) \}", code)):
    if o not in opdef and not re.search(r"_(modifier|programme)$|^COLDWAR_SOV_cohesion_", o):
        err("unknown opinion modifier", o)
trdef = set(re.findall(r"^\t(COLDWAR_(?:SOV|UNI)_\w+) = \{", F("common/country_leader/COLDWAR_SOV_1970_traits.txt") + F("common/country_leader/COLDWAR_UNI_1970_traits.txt"), re.M))
for blk in re.findall(r"traits = \{([^}]*)\}", code):
    for t in blk.split():
        if t.startswith(("COLDWAR_SOV_", "COLDWAR_UNI_")) and t not in trdef:
            err("unknown trait", t)
for t in re.findall(r"add_country_leader_trait = (\w+)", code):
    if t not in trdef:
        err("unknown trait", t)
cats = set(IDX["cats"])
for c in re.findall(r"category = (CAT_\w+)", code):
    if c not in cats:
        err("unknown tech category", c)

# 9 flags and variables: every flag that is checked is also set
setf = set(re.findall(r"set_(?:country|global)_flag = (?:\{ flag = )?(COLDWAR_(?:SOV|UNI)_\w+)", code))
for fl in set(re.findall(r"has_(?:country|global)_flag = (COLDWAR_(?:SOV|UNI)_\w+)", code)):
    if fl.endswith("_in_progress") and re.search(rf"flag = {fl} days", code):
        continue
    if fl not in setf:
        err("flag checked but never set", fl)
for v in set(re.findall(r"check_variable = \{ (?:global\.)?(COLDWAR_(?:SOV|UNI)_\w+)", code)):
    if not re.search(rf"(?:set_variable|add_to_variable|set_temp_variable|add_to_temp_variable|multiply_temp_variable|set_temp_variable_to_random)(?: = \{{)? (?:var = )?(?:global\.)?{v}\b", code) \
            and not re.search(rf"array = (?:global\.)?{v}\b", code):
        err("variable checked but never set", v)

# 10 decisions
decs = F("common/decisions/COLDWAR_SOV_1970_decisions.txt") + F("common/decisions/COLDWAR_UNI_1970_decisions.txt")
catdef = set(re.findall(r"^(COLDWAR_(?:SOV|UNI)_\w+) = \{", F("common/decisions/categories/COLDWAR_SOV_1970_decision_categories.txt")
                        + F("common/decisions/categories/COLDWAR_UNI_1970_decision_categories.txt"), re.M))
for c in re.findall(r"^(COLDWAR_(?:SOV|UNI)_\w+) = \{", decs, re.M):
    if c not in catdef:
        err("decision category not defined", c)
for d in re.findall(r"^\t(COLDWAR_(?:SOV|UNI)_\w+) = \{", decs, re.M):
    for k in (d, d + "_desc"):
        if k not in LOC:
            err("decision loc", k)
for c in catdef:
    if c not in LOC:
        err("category loc", c)

# 11 marker convention
for p in T:
    base = os.path.basename(p)
    if not (base.startswith("COLDWAR_") or p in ("history/countries/SOV - Russia.txt", "common/scripted_effects/mdcw_1970_focus_tree_effects.txt",
                                                  "common/decisions/mdcw_cold_war_decisions.txt", "common/national_focus/mdcw_1970_generic_focus.txt")):
        err("file without COLDWAR marker", p)

# 12 the Union plan (cw_union.py): joint tree, attachment, missions, layout
joint = F("common/national_focus/COLDWAR_UNI_1970_union_joint.txt")
jblocks = re.findall(r"^joint_focus = \{\n(.*?)\n\}", joint, re.M | re.S)
jids = [re.search(r"^\tid = (\w+)", b, re.M).group(1) for b in jblocks]
if len(jids) != len(set(jids)) or not jids:
    err("joint focus ids", jids)
if "COLDWAR_UNI_the_union_plan" not in jids:
    err("joint root missing")
for fn in ("common/national_focus/COLDWAR_SOV_1970_focus.txt", "common/national_focus/mdcw_1970_generic_focus.txt"):
    if len(re.findall(r"^\tshared_focus = COLDWAR_UNI_the_union_plan\b", F(fn), re.M)) != 1:
        err("joint root not attached exactly once", fn)
if re.search(r"^\s*(?:shared_focus|mutually_exclusive) = \{", joint, re.M):
    err("the Union branch is joint only and has no exclusions")
for b, i in zip(jblocks, jids):
    if "joint_trigger = { COLDWAR_UNI_is_member = yes }" not in b:
        err("joint focus without membership trigger", i)
    if f"flag = {i}_in_progress days" not in b or f"has_global_flag = {i}_in_progress" not in b:
        err("joint focus without AI de-duplication", i)
    for part in re.findall(r"^\t(completion_reward(?:_joint_member)?) = \{\n(.*?)\n\t\}", b, re.M | re.S):
        body = part[1]
        if re.search(r"= -\d|= -0|cohesion_delta = -|\bglobal\.|set_global_flag|\b(?:SOV|UKR|BLR|EST|LAT|LIT|ARM|AZE|GEO|KAZ|KYR|TAJ|TRK|UZB|MLV) = \{", body):
            err("joint member reward must be positive and local", i, part[0])
    for r in re.findall(r"(?:relative_position_id|focus) = (\w+)", b):
        if r not in jids:
            err("joint focus reference", i, r)
    ic = re.search(r"^\ticon = (\S+)", b, re.M).group(1)
    if ic not in goal and ic not in newspr:
        err("unknown joint focus icon", i, ic)
    for k in (i, i + "_desc"):
        if k not in LOC:
            err("missing loc", k)
missions = set(re.findall(r"^\t(COLDWAR_UNI_\w+) = \{\n\t\ticon = \S+\n\t\tallowed = \{[^}]*\}\n\t\tactivation", F("common/decisions/COLDWAR_UNI_1970_decisions.txt"), re.M))
for m in set(re.findall(r"(?:activate_mission|remove_mission|has_active_mission) = (COLDWAR_UNI_\w+)", code)):
    if m not in missions:
        err("unknown mission", m)
for m in missions:
    if not re.search(rf"activate_mission = {m}\b", code):
        err("mission never activated", m)
import cw_focus as _FO
x0, y0, x1, y1 = _FO.UNION_BOX
for fid, (x, y) in _FO.POS.items():
    if x0 <= x <= x1 and y0 <= y <= y1:
        err("Soviet focus inside the Union box", fid, x, y)
cx, cy = _FO.CFP
if not (cx + 6 < x0 or cx > x1 or cy + 5 < y0 or cy > y1):
    err("continuous focus panel over the Union box", _FO.CFP)

# 13 no internal name in a tooltip (Enes, 18.10.2026): every flag and variable in a visible condition or effect has a text
sys_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools")
import sys
sys.path.insert(0, sys_path)
import raw_tooltip_scan as RTS
for kind, name in RTS.MISSING:
    err("raw name in a tooltip (no localisation)", kind, name, RTS.REPORT.get(f"{kind}:{name}", [""])[0])
for name in set(re.findall(r"(?:has|set|clr)_(?:country|global)_flag = (?:\{ flag = )?(COLDWAR_(?:SOV|UNI)_\w+)", code)):
    if name not in ALLLOC:
        err("flag without localisation", name)

# 14 the Politburo dossier (cw_pbgui.py): the GUI, its scripted GUI and its sprites fit together
GUI_T = T.get("interface/COLDWAR_SOV_1970_politburo.gui", "")
SG_T = T.get("common/scripted_guis/COLDWAR_SOV_1970_politburo_gui.txt", "")
GFX_T = T.get("interface/COLDWAR_SOV_1970_politburo.gfx", "")
if not (GUI_T and SG_T and GFX_T):
    err("politburo dossier files missing")
else:
    els = set(re.findall(r'name = "(COLDWAR_SOV_pb_\w+)"', GUI_T))
    for el in re.findall(r"^\t\t\t(COLDWAR_SOV_pb_\w+) = \{", SG_T, re.M):
        if re.sub(r"_visible$", "", el) not in els:
            err("dossier: scripted GUI element not in the .gui", el)
    own_spr = set(re.findall(r'name = "(GFX_\w+)"', GFX_T))
    for sp in set(re.findall(r'spriteType = "(GFX_\w+)"', GUI_T)):
        if sp not in own_spr and sp not in spr:
            err("dossier: unknown sprite", sp)
    for sp in set(re.findall(r"localization_key = (GFX_\w+)", "\n".join(t for p_, t in T.items() if "scripted_localisation" in p_))):
        if sp not in own_spr:
            err("dossier: scripted loc returns an unknown sprite", sp)
    for k in re.findall(r'text = "(\w+)"', GUI_T):
        if k not in LOC:
            err("dossier: text key without localisation", k)
    for k in re.findall(r'pdx_tooltip = "(\w+)"', GUI_T):
        if k not in LOC:
            err("dossier: tooltip key without localisation", k)
    if 'window_name = "COLDWAR_SOV_politburo_window"' not in SG_T or 'name = "COLDWAR_SOV_politburo_window"' not in GUI_T:
        err("dossier: window name")
    if "scripted_gui = COLDWAR_SOV_politburo_gui" not in T["common/decisions/categories/COLDWAR_SOV_1970_decision_categories.txt"]:
        err("dossier: the category does not carry the scripted GUI")
    for tex in re.findall(r'texturefile = "(gfx/interface/coldwar_politburo/[^"]+)"', GFX_T):
        if not os.path.exists(os.path.join(OUT, tex)):
            err("dossier: texture not shipped", tex)
    try:
        from PIL import Image
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from art import pb_layout as PBL
        if Image.open(os.path.join(OUT, "gfx/interface/coldwar_politburo/politburo_dossier.dds")).size != (PBL.W, PBL.H):
            err("dossier: background size differs from art/pb_layout.py (re-run art/politburo_art.py)")
    except ImportError:
        warn("dossier: PIL not available, background size not checked")

print(len(errs), "errors,", len(warns), "warnings")
for e in sorted(set(errs))[:150]:
    print("  E", e)
for w in sorted(set(warns))[:80]:
    print("  W", w)
