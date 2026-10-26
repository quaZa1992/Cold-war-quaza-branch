# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Static validation of the generated GDR 1970 files. Run after dg_build.py: python3 validate_ddr.py
import re, os, json, collections, glob
from dg_common import OUT, MOD, EGY, HERE, MD_TT, MD_TT_WRONG, SHARED_TT_FILE

IDX = json.load(open(next(p for p in (os.path.join(HERE, "ref", "idx_mdcw.json"), os.path.join(MOD, "tools/generic_1970_focus_tree/idx_mdcw.json"),
                                      "/home/claude/ddr/ref/idx_mdcw.json") if os.path.exists(p))))
T = {os.path.relpath(f, OUT): open(f, encoding="utf-8-sig").read() for f in glob.glob(OUT + "/**/*", recursive=True) if os.path.isfile(f)}
errs, warns = [], []


def err(*a):
    errs.append(" ".join(str(x) for x in a))


def warn(*a):
    warns.append(" ".join(str(x) for x in a))


OWN = {p: t for p, t in T.items() if "COLDWAR_DDR" in p}
X = "COLDWAR_DDR_"
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
for yml in ("COLDWAR_DDR_1970_l_english.yml", "COLDWAR_DDR_1970_parties_l_english.yml"):
    raw = open(os.path.join(OUT, "localisation/english", yml), "rb").read()
    if not raw.startswith(b"\xef\xbb\xbf"):
        err("loc without BOM", yml)
    for line in raw.decode("utf-8-sig").splitlines()[1:]:
        if re.match(r'^ [^\s:]+:0 "', line):
            err("loc with :0 (MD writes KEY: \"Text\")", line[:60])
        m = re.match(r'^ ([^\s:]+): "(.*)"$', line)
        if m:
            if m.group(1) in LOC:
                err("dup loc", m.group(1))
            LOC[m.group(1)] = m.group(2)
        elif line.strip() and not line.strip().startswith("#"):
            err("bad loc line", line[:80])
MDLOC = set()
for f in glob.glob(os.path.join(MOD, "localisation/english/**/*.yml"), recursive=True):
    if "COLDWAR_DDR" in os.path.basename(f):
        continue
    for line in open(f, encoding="utf-8-sig", errors="replace"):
        m = re.match(r"^\s+([^\s:#]+):\d*\s", line)
        if m:
            MDLOC.add(m.group(1))
for f in glob.glob("/mnt/user-data/uploads/2777392649/localisation/english/**/*.yml", recursive=True):   # staged MD files (sandbox)
    for line in open(f, encoding="utf-8-sig", errors="replace"):
        m = re.match(r"^\s+([^\s:#]+):\d*\s", line)
        if m:
            MDLOC.add(m.group(1))
SHARED = {}
for line in open(os.path.join(OUT, SHARED_TT_FILE), encoding="utf-8-sig").read().splitlines()[1:]:
    m = re.match(r'^ ([^\s:]+): "(.*)"$', line)
    if m:
        SHARED[m.group(1)] = m.group(2)
ALLLOC = set(LOC) | MDLOC | set(SHARED) | MD_TT | {"modifies_dynamic_modifier_tt"}
focus = F("common/national_focus/COLDWAR_DDR_1970_focus.txt")
ids = re.findall(r"^\t\tid = (\w+)", focus, re.M)
if not (len(ids) == len(set(ids)) == 821):
    err("focus count", len(ids), len(set(ids)))
for i in ids:
    for k in (i, i + "_desc"):
        if k not in LOC:
            err("missing loc", k)
for k in set(re.findall(r"custom_effect_tooltip = (\w+)", code)) | set(re.findall(r"\btooltip = (\w+)", code)) | \
        set(re.findall(r"localization_key = (\w+)", code)) | set(re.findall(r"name = (COLDWAR_DDR_\w+_tree_shortcut)", code)) - {"modifies_dynamic_modifier_tt"}:
    if k not in ALLLOC:
        err("missing tooltip loc", k)
for k in set(re.findall(r"add_tech_bonus = \{ name = (\w+)", code)):
    if k not in ALLLOC:
        err("missing tech bonus loc", k)
for k in set(re.findall(r"(?:title|desc|name) = (COLDWAR_DDR\.\d+\.\w)", code)):
    if k not in LOC:
        err("missing event loc", k)
sloc = set(re.findall(r"name = (COLDWAR_DDR_Get\w+)", F("common/scripted_localisation/COLDWAR_DDR_1970_scripted_localisation.txt")))
for k, v in LOC.items():
    for m in re.findall(r"\[(?:\w+\.)?(COLDWAR_DDR_\w+)\]", v):
        if m not in sloc:
            err("unknown scripted loc", m)
    if v.count("[") != v.count("]"):
        err("bracket mismatch in loc", k, v[:60])
    if v.count("§") % 2:
        warn("odd colour codes", k, v[:70])
    if "$" in v and not re.search(r"\$RIGHT\|[^$]+\$|\$[A-Z_]+\$", v):
        warn("dollar in loc", k, v[:60])

# 3 focus structure
for p in set(re.findall(r"focus = (COLDWAR_DDR_\w+)", focus)) | set(re.findall(r"has_completed_focus = (COLDWAR_DDR_\w+)", code)):
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
# absolute positions: no two foci on one cell
import dg_load as DL
cells = collections.Counter(DL.POS.values())
for c, n in cells.items():
    if n > 1:
        err("two foci on one cell", c)
if re.search(r"\bdate\s*[<>]", "\n".join(re.findall(r"available = \{(.*?)\n\t\t\}", focus, re.S))):
    err("date condition in a focus 'available' (house rule)")

# 4 scripted effects / triggers
eff, trg = set(IDX["effects"]), set(IDX["triggers"])
eff |= {"MDCW_HP_sync_native_counter"}   # newer than the index
defined = set(re.findall(r"^(COLDWAR_DDR_\w+) = \{", F("common/scripted_effects/COLDWAR_DDR_1970_scripted_effects.txt"), re.M))
dtrig = set(re.findall(r"^(COLDWAR_DDR_\w+) = \{", F("common/scripted_triggers/COLDWAR_DDR_1970_scripted_triggers.txt"), re.M))
VAN_YES = {"has_civil_war", "has_war", "always", "is_ai", "exists", "is_debug", "elections_allowed", "instant_build", "limit_to_border", "all_provinces",
           "major", "is_triggered_only", "fire_only_once", "hidden", "random", "default", "reset_on_civilwar", "is_historical_focus_on",
           "retire_country_leader", "ruling_only", "dismantle_faction", "force_update_dynamic_modifier", "visible_when_empty", "trade",
           "target_non_existing", "is_subject", "has_capitulated", "is_good", "selectable_mission", "mark_focus_tree_layout_dirty",
           "is_coastal", "transfer_troops", "leave_faction", "is_in_faction", "is_puppet", "is_major"}
for name in set(re.findall(r"\b([A-Za-z_]\w*) = (?:yes|no)\b", code)):
    if name in VAN_YES or name in defined or name in dtrig or name in eff or name in trg:
        continue
    err("unknown yes-call", name)
for name in set(re.findall(r"\b(COLDWAR_DDR_\w+) = yes", code)):
    if name not in defined and name not in dtrig:
        err("undefined COLDWAR effect/trigger", name)
YESCALLS = collections.Counter(re.findall(r"\b(\w+) = yes", code + open(os.path.join(OUT, "history/countries/DDR - East Germany.txt") if os.path.exists(os.path.join(OUT, "history/countries/DDR - East Germany.txt")) else os.path.join(MOD, "history/countries/DDR - East Germany.txt"), encoding="utf-8-sig").read()))
for name in defined:
    if not YESCALLS[name]:
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
             "corruption_cost_factor", "military_spending_cost_factor", "production_speed_nuclear_reactor_factor", "industrial_capacity_dockyard",
             "local_resources_factor", "air_accidents_factor", "air_cas_efficiency", "air_training_xp_gain_factor", "army_intel_factor", "civilian_intel_factor",
             "conversion_cost_civ_to_mil_factor", "decryption_factor", "encryption_factor", "defensive_war_stability_factor", "enemy_operative_capture_chance_factor",
             "fuel_gain_factor", "industry_repair_factor", "intel_network_gain_factor", "license_production_speed", "line_change_production_efficiency_factor",
             "mobilization_speed", "naval_coordination", "operative_slot", "party_popularity_stability_factor", "root_out_resistance_effectiveness_factor",
             "special_forces_attack_factor", "civilian_factories_productivity", "military_factories_productivity", "dockyard_productivity",
             # building and idea-category modifiers the engine creates (MD buildings agriculture_district / energy_infrastructure, category economic_cycles)
             "production_speed_agriculture_district_factor", "production_speed_energy_infrastructure_factor", "economic_cycles_cost_factor"}
used = set()
for p in ("common/ideas/COLDWAR_DDR_1970_ideas.txt", "common/bop/COLDWAR_DDR_1970_inner_german_course.txt"):
    for blk in re.findall(r"modifier = \{([^{}]*)\}", F(p)):
        used |= set(re.findall(r"(\w+) = ", blk))
dyn = F("common/dynamic_modifiers/COLDWAR_DDR_1970_dynamic_modifiers.txt")
used |= set(re.findall(r"^\t(\w+) = (?:COLDWAR_DDR_|-?[\d.])", dyn, re.M))
for t in re.findall(r"random = no\n\n((?:\t\t\w+ = [-\d.]+\n)+)", F("common/country_leader/COLDWAR_DDR_1970_traits.txt")):
    used |= set(re.findall(r"(\w+) = ", t))
for m in sorted(used - {"icon"}):
    if m not in mods and m not in KNOWN_VAN:
        err("unknown modifier", m)
    elif m not in KNOWN_VAN and not ({m, "MODIFIER_" + m.upper(), "MODIFIER_" + m} & ALLLOC):
        warn("modifier without loc in the staged files", m)
idea_gfx = set(open(os.path.join(EGY, "idea_gfx.txt")).read().split())
for p in re.findall(r"icon = GFX_idea_([\w-]+)", code) + re.findall(r"^\t\t\tpicture = ([\w-]+)", F("common/ideas/COLDWAR_DDR_1970_ideas.txt"), re.M):
    if p not in idea_gfx:
        err("unknown idea gfx", p)
own_ideas = set(re.findall(r"^\t\t(COLDWAR_DDR_\w+) = \{", F("common/ideas/COLDWAR_DDR_1970_ideas.txt"), re.M))
md_ideas = set(IDX["ideas"]) | {"mdcw_cw_self_reliance", "mdcw_cw_soviet_advisers", "mdcw_cw_show_of_strength", "mdcw_cw_diplomatic_realignment"}
for i in set(re.findall(r"(?:add_ideas|remove_ideas|\bidea|add_idea|remove_idea|has_idea) = (\w+)", code)):
    if i not in own_ideas and i not in md_ideas:
        err("unknown idea", i)
for blk in re.findall(r"add_ideas = \{([^}]*)\}", code):
    for i in blk.split():
        if i not in own_ideas and i not in md_ideas:
            err("unknown idea in block", i)
WORDS_NO_IDEAS = collections.Counter(re.findall(r"\w+", code.replace(F("common/ideas/COLDWAR_DDR_1970_ideas.txt"), "")))
for i in own_ideas:
    if i not in LOC:
        err("idea loc", i)
    if not WORDS_NO_IDEAS[i]:
        warn("idea never used", i)
dyndef = set(re.findall(r"^(COLDWAR_DDR_\w+) = \{", dyn, re.M))
for d in set(re.findall(r"\b(?:modifier|MODIFIER) = (COLDWAR_DDR_\w+_(?:modifier|programme))\b", code)) | set(re.findall(r"modifier = (COLDWAR_DDR_trust_\w+)", code)):
    if d not in dyndef:
        err("unknown dynamic modifier", d)
for d in dyndef:
    if d not in LOC:
        err("dyn loc", d)
ASSIGNED = set(re.findall(r"\b(\w+) = ", code.replace(dyn, "")))
for var in set(re.findall(r"^\t\w+ = (COLDWAR_DDR_\w+)$", dyn, re.M)):
    if var not in ASSIGNED:
        warn("dyn var never changed", var)

# 6 sprites and pictures
spr = set(IDX["sprites"])
for f in glob.glob(os.path.join(MOD, "interface/*.gfx")):
    if "COLDWAR_DDR" in os.path.basename(f):
        continue
    spr |= set(re.findall(r'name\s*=\s*"?(GFX_\w+)', open(f, encoding="utf-8", errors="replace").read()))
goal = {n for n, p in json.load(open(os.path.join(EGY, "goal_sprites.json")))}
gfx = F("interface/COLDWAR_DDR_1970_goals.gfx")
newspr = set(re.findall(r'name = "(COLDWAR_DDR_goal_\w+)"', gfx))
repo = {p.lower() for p in json.load(open(os.path.join(EGY, "repo_paths.json")))}
for tex in re.findall(r'texturefile = "([^"]+)"', gfx) + re.findall(r'textureFile = "([^"]+)"', F("interface/COLDWAR_DDR_1970_focus_filters.gfx")):
    if tex.lower() not in repo:
        err("texture missing", tex)
for ic in re.findall(r"\ticon = (\S+)", focus):
    if ic not in goal and ic not in newspr:
        err("unknown focus icon", ic)
# our new sprite names may already exist from the Soviet tree: same name must mean the same texture
sov_gfx = os.path.join(MOD, "interface/COLDWAR_SOV_1970_goals.gfx")
dupe = [n for n in newspr if n in spr]
if dupe:
    warn("new sprite names also defined elsewhere (check same texture)", len(dupe), dupe[:5])
evs = F("events/COLDWAR_DDR_1970_events.txt")
for p in set(re.findall(r"picture = (GFX_\w+)", evs)):
    if p not in spr:
        err("unknown event picture", p)
for p in ("common/decisions/COLDWAR_DDR_1970_decisions.txt", "common/decisions/categories/COLDWAR_DDR_1970_decision_categories.txt",
          "common/bop/COLDWAR_DDR_1970_inner_german_course.txt"):
    for ic in set(re.findall(r"icon = (GFX_\w+)", F(p))):
        if ic not in spr:
            err("unknown icon", p, ic)

# 7 events
evdef = set(re.findall(r"^\s*id = (COLDWAR_DDR\.\d+)", evs, re.M))
for e in set(re.findall(r"id = (COLDWAR_DDR\.\d+)", code)):
    if e not in evdef:
        err("event not defined", e)
for e in evdef:
    blk = evs[evs.index(f"id = {e}\n"):][:3000]
    if "mean_time_to_happen" in blk.split("option = {")[0]:
        continue
    if not re.search(rf"id = {re.escape(e)} ", code):
        warn("event never fired", e)
for m in re.finditer(r"(?:country_event|news_event) = \{\n\tid = (\S+)(.*?)\n\}", evs, re.S):
    if m.group(2).count("option = {") > 26:
        err("too many options", m.group(1))

# 8 opinion modifiers, traits, tech categories
opdef = set(re.findall(r"^\t(COLDWAR_DDR_\w+) = \{", F("common/opinion_modifiers/COLDWAR_DDR_1970_opinion_modifiers.txt"), re.M))
for o in set(re.findall(r"modifier = (COLDWAR_DDR_\w+) \}", code)):
    if o not in opdef and not re.search(r"_(modifier|programme)$|^COLDWAR_DDR_trust_", o):
        err("unknown opinion modifier", o)
trdef = set(re.findall(r"^\t(COLDWAR_DDR_\w+) = \{", F("common/country_leader/COLDWAR_DDR_1970_traits.txt"), re.M))
for blk in re.findall(r"\btraits = \{([^}]*)\}", code.replace(F("common/country_leader/COLDWAR_DDR_1970_traits.txt"), "")):
    for t in blk.split():
        if t.startswith("COLDWAR_DDR_") and t not in trdef:
            err("unknown trait", t)
        if not t.startswith("COLDWAR_DDR_") and not re.match(r"^(western|emerging|salafist|neutrality|nationalist)_\w+$", t):
            err("unknown leader trait", t)
for t in re.findall(r"add_country_leader_trait = (\w+)", code):
    if t not in trdef:
        err("unknown trait", t)
cats = set(IDX["cats"])
for c in re.findall(r"category = (CAT_\w+)", code):
    if c not in cats:
        err("unknown tech category", c)

# 9 flags and variables: every flag that is checked is also set
setf = set(re.findall(r"set_(?:country|global)_flag = (?:\{ flag = )?(COLDWAR_DDR_\w+)", code))
for fl in set(re.findall(r"has_(?:country|global)_flag = (COLDWAR_DDR_\w+)", code)):
    if fl not in setf:
        err("flag checked but never set", fl)
READF = set(re.findall(r"has_(?:country|global)_flag = (\w+)", code))
for fl in setf:
    if fl not in READF and not fl.endswith("_unlocked"):
        warn("flag set but never read", fl)
for v in set(re.findall(r"check_variable = \{ (?:global\.)?(COLDWAR_DDR_\w+)", code)):
    if not re.search(rf"(?:set_variable|add_to_variable|set_temp_variable|add_to_temp_variable|multiply_temp_variable)(?: = \{{)? (?:var = )?(?:global\.)?{v}\b", code):
        err("variable checked but never set", v)
for fl in set(re.findall(r"(COLDWAR_DDR_\w+_unlocked)", code)):
    if fl not in READF:
        warn("unlock flag never read", fl)

# 10 decisions
decs = F("common/decisions/COLDWAR_DDR_1970_decisions.txt")
catdef = set(re.findall(r"^(COLDWAR_DDR_\w+) = \{", F("common/decisions/categories/COLDWAR_DDR_1970_decision_categories.txt"), re.M))
for c in re.findall(r"^(COLDWAR_DDR_\w+) = \{", decs, re.M):
    if c not in catdef:
        err("decision category not defined", c)
for d in re.findall(r"^\t(COLDWAR_DDR_\w+) = \{", decs, re.M):
    for k in (d, d + "_desc"):
        if k not in LOC:
            err("decision loc", k)
for c in catdef:
    if c not in LOC:
        err("category loc", c)
bop = F("common/bop/COLDWAR_DDR_1970_inner_german_course.txt")
for c in re.findall(r"decision_category = (\w+)", bop):
    if c not in catdef:
        err("bop decision category", c)

# 11 marker convention and patches
for p in T:
    base = os.path.basename(p)
    if not (base.startswith("COLDWAR_") or p in ("history/countries/DDR - East Germany.txt", "common/scripted_effects/mdcw_1970_focus_tree_effects.txt",
                                                  "common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt",
                                                  "common/scripted_localisation/mdcw_historical_parties.txt")):
        err("file without COLDWAR marker", p)
PATCHED = ("history/countries/DDR - East Germany.txt", "common/scripted_effects/mdcw_1970_focus_tree_effects.txt",
           "common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt", "common/scripted_localisation/mdcw_historical_parties.txt")
F_P = lambda p: T[p] if p in T else open(os.path.join(MOD, p), encoding="utf-8-sig").read()   # unchanged patched files are not written
for p in PATCHED:
    orig = open(os.path.join(MOD, p), encoding="utf-8-sig").read()
    new = F_P(p)
    ns, os_ = set(new.splitlines()), set(orig.splitlines())
    removed = [l for l in orig.splitlines() if l not in ns]
    added = [l for l in new.splitlines() if l not in os_]
    if any("COLDWAR" not in l for l in added):
        err("patch adds a line without marker", p, [l for l in added if "COLDWAR" not in l][:2])
    if p != "history/countries/DDR - East Germany.txt" and removed and not all("COLDWAR_DDR" in l or "GDR 1970" in l for l in removed):
        err("patch removes lines", p, removed[:3])
    print("patch", p, "+", len(added), "-", len(removed))
hist = F_P("history/countries/DDR - East Germany.txt")
for need in ("load_focus_tree = COLDWAR_DDR_1970_focus", "COLDWAR_DDR_initialize_1970 = yes"):
    if hist.count(need) != 1:
        err("history patch", need)
if "expire" in hist.split("COLDWAR HISTORICAL1970 NATIVE IDENTITY END")[0]:
    err("Ulbricht still expires in the history")
pv = F_P("common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt")
if pv.count("COLDWAR | GDR 1970") != 2 * 19:
    err("party name lines in the politics view", pv.count("COLDWAR | GDR 1970"))

# 12 MD style like Russia 2000 (05_russia.txt)
RUS = open(next(p for p in (os.path.join(MOD, "common/national_focus/05_russia.txt"), "/mnt/user-data/uploads/2777392649/common/national_focus/05_russia.txt")
                if os.path.exists(p)), encoding="utf-8-sig", errors="replace").read()
blocks = [m.group(0) for m in re.finditer(r"^\tfocus = \{\n.*?^\t\}$", focus, re.M | re.S)]
if len(blocks) != len(ids):
    err("focus blocks", len(blocks), len(ids))
ORDER_KEYS = ["id", "icon", "x", "y", "relative_position_id", "cost", "allow_branch", "prerequisite", "mutually_exclusive", "will_lead_to_war_with",
              "search_filters", "available", "bypass", "cancel", "completion_reward", "ai_will_do"]
style = collections.Counter()
for b in blocks:
    fid = re.search(r"^\t\tid = (\w+)", b, re.M).group(1)
    keys = re.findall(r"^\t\t(\w+) = ", b, re.M)
    idx = [ORDER_KEYS.index(k) for k in keys if k in ORDER_KEYS]
    if idx != sorted(idx):
        err("MD field order", fid, keys)
    if "search_filters" not in keys:
        err("no search_filters", fid)
    icon = re.search(r"^\t\ticon = (\S+)", b, re.M).group(1)
    if icon.startswith("GFX_"):
        err("icon with GFX_ prefix (MD: bare sprite name)", fid, icon)
    rew = re.search(r"^\t\tcompletion_reward = \{\n(.*?)^\t\t\}", b, re.M | re.S)
    if not rew:
        err("no completion_reward", fid)
        continue
    rl = [l.strip() for l in rew.group(1).splitlines() if l.strip()]
    if not rl or rl[0] != f'log = "[GetDateText]: [Root.GetName]: Focus {fid}"':
        err("completion_reward does not start with the MD log line", fid)
    heads = sum(1 for l in rl if l.startswith("custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt"))
    nls = sum(1 for l in rl if l == "newline = yes")
    if heads > 1 and nls < heads - 1:
        err("modifier groups without newline", fid)
    if rl and rl[-1] == "newline = yes":
        warn("newline at the end of a reward", fid)
    ai = re.search(r"ai_will_do = \{(.*?)\n\t\t\}|ai_will_do = \{ base = \d+ \}", b, re.S)
    if not ai or "base =" not in ai.group(0):
        err("ai_will_do without base", fid)
    if ai and re.search(r"^\t\t\tmodifier = \{$", ai.group(0), re.M):
        err("ai_will_do modifier not on one line (MD)", fid)
    for t in re.findall(r"^\t\t\t(\w{3}) = \{ country_event", rew.group(1), re.M):
        if "TT_IF_THEY_ACCEPT" not in rew.group(1):
            err("event to another country without TT_IF_THEY_ACCEPT", fid, t)
    style["foci"] += 1
    style["newline"] += nls
CW_HIDDEN = re.compile(r"hidden_effect = \{ force_update_dynamic_modifier = yes if = \{ limit = \{ has_country_flag = mdcw_cw_initialized \} mdcw_cw_")
for l in focus.splitlines():
    if "force_update_dynamic_modifier" in l and not CW_HIDDEN.search(l):
        err("force_update_dynamic_modifier in a focus outside the Cold War refresh", l.strip()[:90])
for l in code.splitlines():
    s_ = l.strip()
    if re.search(r"\b(?:add_power_balance_value|swap_ideas|add_tech_bonus) = \{ ", s_) and s_.endswith("}"):
        err("MD style: one-line add_power_balance_value/swap_ideas/add_tech_bonus (MD writes them multi-line)", s_[:90])
    if re.search(r"mutually_exclusive = \{ focus = \w+ focus = ", s_):
        err("MD style: several foci in one mutually_exclusive (MD: one per line)", s_[:90])
for pat, what in (
                  (r"is_historical_focus_on", "is_historical_focus_on directly in a focus (MD: scripted AI triggers)"),
                  (r"_opinion_exact", "own faction wrapper (MD: change_<faction>_opinion directly)"),
                  (r"COLDWAR_DDR_(?:pay|receive)_gdp_share|change_debt_gdp_share", "own money helper (MD: treasury_change + modify_treasury_effect)"),
                  (r"hidden_effect = \{[^\n]*add_dynamic_modifier", "hidden add_dynamic_modifier in a focus"),
                  (r"COLDWAR_DDR_mod_\w+_tt", "own per-tree modifier tooltip (MD <modifier>_tt or the shared file)"),
                  ):
    if re.search(pat, focus):
        err("MD style:", what)
for k in set(re.findall(r"add_to_variable = \{ \S+ = \S+ tooltip = (\w+) \}", code)):
    base = k[:-3]
    if k.startswith("COLDWAR_"):
        if k not in SHARED:
            err("own tooltip not in the shared tooltip file", k)
        if base.replace("COLDWAR_", "", 1) + "_tt" in MD_TT and base.replace("COLDWAR_", "", 1) not in MD_TT_WRONG:
            err("own tooltip although MD has one", k)
    elif k not in MD_TT:
        err("tooltip key neither MD nor shared", k)
if re.search(r"^\t\t\tallowed = ", F("common/ideas/COLDWAR_DDR_1970_ideas.txt"), re.M):
    err("MD style: ideas with allowed (Russian.txt has none)")
for p, t in T.items():
    if p.endswith(".yml") and re.search(r"^ [^\s:]+:0 ", t, re.M):
        err("MD style: loc with :0", p)
for name, pat in (("newline = yes", r"newline = yes"), ("treasury_change", r"treasury_change"), ("TT_IF_THEY_ACCEPT", r"TT_IF_THEY_ACCEPT"),
                  ("log line", r'log = "\[GetDateText\]: \[Root.GetName\]: Focus'), ("modifies_dynamic_modifier_tt", r"modifies_dynamic_modifier_tt"),
                  ("ai one-line modifier", r"modifier = \{ factor = [\d.]+ \w+ = yes \}")):
    print(f"  style {name:28s} ours {len(re.findall(pat, focus)):5d}  MD Russia {len(re.findall(pat, RUS)):5d}")

# layout: what belongs together stands together (Enes, 19.10.2026) - every party root directly under its "Power to" focus,
# every First Secretary's root directly under his candidacy; every icon only once
POSA = dict(DL.POS)
SECOF = {f["id"]: f["sec"] for f in DL.FOCI}
for f in DL.FOCI:
    if f["id"].startswith(X + "power_"):
        sec = f["id"][len(X + "power_"):]
        roots = [g for g in DL.FOCI if g["sec"] == sec and not any(SECOF.get(p) == sec for gg in g["pre"] for p in gg)]
        for r in roots:
            if r["pre"]:
                err("prerequisite line into a party tree", r["id"])
            if POSA[r["id"]][0] != POSA[f["id"]][0] or POSA[r["id"]][1] - POSA[f["id"]][1] != 1:
                err("party tree not directly under its power focus", sec, POSA[f["id"]], POSA[r["id"]])
for k in DL.LEADER_KEYS:
    roots = [g for g in DL.FOCI if g["sec"] == k and not any(SECOF.get(p) == k for gg in g["pre"] for p in gg)]
    cand = X + "cc_" + k
    for r in roots:
        if cand in POSA and POSA[r["id"]][0] != POSA[cand][0]:
            err("First Secretary tree not directly under his candidacy", k)
icons = collections.Counter(re.findall(r"^\t\ticon = (\S+)", focus, re.M))
for ic, n in icons.items():
    if n > 1:
        err("icon used more than once", ic, n)
gfxtex = dict(re.findall(r'name = "(COLDWAR_DDR_goal_\w+)"\n\t\ttexturefile = "([^"]+)"', gfx))
texuse = collections.Counter(gfxtex.get(ic, json.dumps(ic)).lower() for ic in icons)
goalmap = {n: p.lower() for n, p in json.load(open(os.path.join(EGY, "goal_sprites.json")))}
texuse = collections.Counter((gfxtex.get(ic) or goalmap.get(ic) or ic).lower() for ic in re.findall(r"^\t\ticon = (\S+)", focus, re.M))
for t, n in texuse.items():
    if n > 1:
        err("icon texture used more than once", t, n)

# 13 Cold War / Imperia hooks
CWIDEAS = set()
for m in re.finditer(r"^\t\t(COLDWAR_DDR_\w+) = \{(.*?)^\t\t\}", F("common/ideas/COLDWAR_DDR_1970_ideas.txt"), re.M | re.S):
    if "mdcw_cw_" in m.group(2):
        CWIDEAS.add(m.group(1))
for b in blocks:
    fid = re.search(r"^\t\tid = (\w+)", b, re.M).group(1)
    if re.search(r"add_to_variable = \{ COLDWAR_DDR_\w*mdcw_cw_\w+ =", b) or any(re.search(rf"(?:add_ideas|add_idea|idea) = {i}\b", b) for i in CWIDEAS):
        if "mdcw_cw_recalculate_country = yes" not in b:
            err("Cold War modifier changed without mdcw_cw_recalculate_country", fid)
    if re.search(r"(?:globalism_equilibrium|mdcw_cw_market_exposure) =", b) and "mdcw_cw_update_world_market" not in b:
        err("globalism/market exposure changed without mdcw_cw_update_world_market", fid)
for m in re.finditer(r"mdcw_cw_change_alignment = yes(.{0,200})", code, re.S):
    if "mdcw_cw_t_free = 0" not in m.group(1):
        err("mdcw_cw_change_alignment without resetting mdcw_cw_t_free")
for pat in (r"(?:set|add_to)_variable = \{ global\.mdcw_cw_tension", r"mdcw_cw_start_opec_vote", r"mdcw_cw_(?:start|end)_oil_embargo",
            r"global\.mdcw_cw_oil_level =", r"imp_spike_oil_price", r"imp_oil_price_demand_", r"imp_oil_prices_ask_", r"mdcw_cw_start_program_\d",
            r"mdcw_cw_start_pps", r"\bglobalism_value\b", r"\bEU_member\b", r"given_bonds@", r"active_subsidies@", r"IMP_1970_apply_starting_gdp_profile",
            r"imp_eco_\w+_dynamic_modifier"):
    if re.search(pat, code):
        err("forbidden Cold War/Imperia hook", pat)
for r in re.findall(r"add_resource = \{[^}]*type = (\w+)", code):
    if r not in ("oil", "aluminium", "rubber", "tungsten", "steel", "chromium"):
        err("add_resource with an undefined resource (crash)", r)

print(len(errs), "errors,", len(warns), "warnings")
for e in sorted(set(errs))[:150]:
    print("  E", e)
for w in sorted(set(warns))[:120]:
    print("  W", w)
