# IMPERIA CW — Cold War: Egypt 1970 content generator.
# COLDWAR | Static validation of the generated Egypt 1970 files.
import re, os, json, collections, glob
OUT = "out"
T = {p: open(os.path.join(OUT, p), encoding="utf-8-sig").read() for p in
     [os.path.relpath(f, OUT) for f in glob.glob(OUT + "/**/*", recursive=True) if os.path.isfile(f) and not f.endswith(".tga")]}
errs = []


def err(*a):
    errs.append(" ".join(str(x) for x in a))


# 1 braces / quotes
for p, t in T.items():
    if p.endswith(".yml"):
        continue
    body = re.sub(r'"[^"\n]*"', '""', t)
    body = re.sub(r"#.*", "", body)
    d = 0
    for i, ch in enumerate(body):
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
    if t.startswith("﻿"):
        err("BOM in txt", p)

# 2 loc
LOC = {}
yml = open(os.path.join(OUT, "localisation/english/COLDWAR_EGY_1970_l_english.yml"), "rb").read()
assert yml.startswith(b"\xef\xbb\xbf"), "loc without BOM"
for line in yml.decode("utf-8-sig").splitlines()[1:]:
    m = re.match(r'^ ([^\s:]+):0 "(.*)"$', line)
    if m:
        if m.group(1) in LOC:
            err("dup loc", m.group(1))
        LOC[m.group(1)] = m.group(2)
    elif line.strip() and not line.strip().startswith("#"):
        err("bad loc line", line[:80])
MDLOC = set()
for f in glob.glob("/mnt/user-data/uploads/mdcoldwar/localisation/english/**/*.yml", recursive=True):
    for line in open(f, encoding="utf-8-sig", errors="replace"):
        m = re.match(r"^\s+([^\s:#]+):\d*\s", line)
        if m:
            MDLOC.add(m.group(1))
focus = T["common/national_focus/COLDWAR_EGY_1970_focus.txt"]
ids = re.findall(r"^\t\tid = (\w+)", focus, re.M)
assert len(ids) == len(set(ids)) == 812, len(ids)
for i in ids:
    for k in (i, i + "_desc"):
        if k not in LOC:
            err("missing loc", k)
allcode = "\n".join(t for p, t in T.items() if not p.endswith((".yml", ".gfx")))
for k in set(re.findall(r"custom_effect_tooltip = (\w+)", allcode)) | set(re.findall(r"tooltip = (\w+)", allcode)) | set(re.findall(r"localization_key = (\w+)", allcode)):
    if k not in LOC and k not in MDLOC:
        err("missing tooltip loc", k)
for k in set(re.findall(r"(?:title|desc|name) = (COLDWAR_EGY\.\d+\.\w)", allcode)):
    if k not in LOC:
        err("missing event loc", k)

# 3 prerequisites / mx
pre = set(re.findall(r"focus = (COLDWAR_EGY_\w+)", focus))
for p in pre:
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

# 4 scripted effects / triggers referenced
eff = set(open("our_effects.txt").read().split())
trg = set(open("our_triggers.txt").read().split())
defined = set(re.findall(r"^(COLDWAR_EGY_\w+) = \{", T["common/scripted_effects/COLDWAR_EGY_1970_scripted_effects.txt"], re.M))
defined |= set(re.findall(r"^(COLDWAR_EGY_\w+) = \{", T["common/scripted_triggers/COLDWAR_EGY_1970_scripted_triggers.txt"], re.M))
VAN_YES = {"has_civil_war", "has_war", "always", "is_ai", "exists", "is_debug", "elections_allowed", "instant_build", "transfer_troops",
           "limit_to_border", "all_provinces", "major", "is_triggered_only", "fire_only_once", "hidden", "random", "default",
           "reset_on_civilwar", "IMP_is_1970_scenario", "is_historical_focus_on", "retire_country_leader", "ruling_only", "obsolete", "mark_formed_country_formable", "set_improved_trade_agreement", "is_agrarian_economy"}
for name in set(re.findall(r"\b([A-Za-z_][\w]*) = yes\b", allcode)):
    if name in VAN_YES or name in defined or name in eff or name in trg:
        continue
    err("unknown yes-call", name)
for name in set(re.findall(r"\b(COLDWAR_EGY_\w+) = yes", allcode)):
    if name not in defined:
        err("undefined COLDWAR effect/trigger", name)

# 5 ideas and modifiers
mods = set(open("our_mods.txt").read().split())
VANMOD = set()
for line in open("/mnt/user-data/uploads/mdcoldwar/localisation/english/replace/replaced_from_vanilla_modifiers_l_english.yml", encoding="utf-8-sig"):
    m = re.match(r"^\s+MODIFIER_([A-Z0-9_]+):", line)
    if m:
        VANMOD.add(m.group(1).lower())
for f in glob.glob("/mnt/user-data/uploads/mdcoldwar/common/modifier_definitions/*.txt"):
    for m in re.findall(r"^(\w+) = \{", open(f, encoding="utf-8-sig", errors="replace").read(), re.M):
        mods.add(m)
KNOWN_VAN = {"political_power_factor", "stability_factor", "war_support_factor", "research_speed_factor", "trade_opinion_factor",
             "neutrality_drift", "communism_drift", "democratic_drift", "fascism_drift", "nationalist_drift", "production_speed_buildings_factor",
             "industrial_capacity_factory", "consumer_goods_factor", "army_org_factor", "army_morale_factor", "army_attack_factor",
             "army_defence_factor", "breakthrough_factor", "training_time_factor", "conscription", "experience_gain_army", "max_planning_factor",
             "planning_speed", "enemy_army_bonus_air_superiority_factor", "special_forces_cap", "static_anti_air_damage_factor",
             "static_anti_air_hit_chance_factor", "air_training_xp_gain_factor", "monthly_population", "production_factory_efficiency_gain_factor",
             "foreign_influence_modifier", "foreign_influence_defense_modifier", "air_superiority_efficiency",
             "tag", "attack_bonus_against", "defense_bonus_against", "production_speed_air_base_factor"}
used_mods = set()
for blk in re.findall(r"modifier = \{([^{}]*)\}", T["common/ideas/COLDWAR_EGY_1970_ideas.txt"]):
    used_mods |= set(re.findall(r"(\w+) = ", blk))
used_mods |= set(re.findall(r"^\t(\w+) = COLDWAR_EGY_", T["common/dynamic_modifiers/COLDWAR_EGY_1970_dynamic_modifiers.txt"], re.M))
for t in re.findall(r"random = no\n\n((?:\t\t\w+ = [-\d.]+\n)+)", T["common/country_leader/COLDWAR_EGY_1970_traits.txt"]):
    used_mods |= set(re.findall(r"(\w+) = ", t))
for m in used_mods:
    if m not in mods and m not in VANMOD and m not in KNOWN_VAN:
        err("unknown modifier", m)
idea_gfx = set(open("idea_gfx.txt").read().split())
for p in re.findall(r"icon = GFX_idea_([\w-]+)", allcode) + re.findall(r"^\t\t\tpicture = ([\w-]+)", T["common/ideas/COLDWAR_EGY_1970_ideas.txt"], re.M):
    if p not in idea_gfx:
        err("unknown idea gfx", p)
idea_ids = set(re.findall(r"^\t\t(COLDWAR_EGY_\w+) = \{", T["common/ideas/COLDWAR_EGY_1970_ideas.txt"], re.M))
for i in set(re.findall(r"(?:add_ideas|remove_ideas|idea|add_idea|remove_idea|has_idea) = (COLDWAR_EGY_\w+)", allcode)):
    if i not in idea_ids:
        err("unknown idea", i)
for i in idea_ids:
    if i not in LOC:
        err("idea loc", i)

# 6 sprites
goal = {n for n, p in json.load(open("goal_sprites.json"))}
newspr = set(re.findall(r'name = "(GFX_COLDWAR_goal_\w+)"', T["interface/COLDWAR_EGY_1970_goals.gfx"]))
repo = {p.lower() for p in json.load(open("repo_paths.json"))}
for tex in re.findall(r'texturefile = "([^"]+)"', T["interface/COLDWAR_EGY_1970_goals.gfx"]):
    if tex.lower() not in repo:
        err("texture missing", tex)
for ic in re.findall(r"\ticon = (\S+)", focus):
    if ic not in goal and ic not in newspr:
        err("unknown icon", ic)
evpics = set(re.findall(r'name\s*=\s*"?(GFX_\w+)', open("/mnt/user-data/uploads/mdcoldwar/interface/MD_eventpictures.gfx", encoding="utf-8", errors="replace").read()))
for p in set(re.findall(r"picture = (GFX_\w+)", T["events/COLDWAR_EGY_1970_events.txt"])):
    if p not in evpics:
        err("unknown event picture", p)

# 7 events defined vs fired
evdef = set(re.findall(r"\tid = (COLDWAR_EGY\.\d+)", T["events/COLDWAR_EGY_1970_events.txt"])) | set(re.findall(r"^\s*id = (COLDWAR_EGY\.\d+)", T["events/COLDWAR_EGY_1970_events.txt"], re.M))
for e in set(re.findall(r"id = (COLDWAR_EGY\.\d+)", allcode)):
    if e not in evdef:
        err("event not defined", e)
# 8 opinion modifiers
opdef = set(re.findall(r"^\t(COLDWAR_EGY_\w+) = \{", T["common/opinion_modifiers/COLDWAR_EGY_1970_opinion_modifiers.txt"], re.M))
for o in set(re.findall(r"modifier = (COLDWAR_EGY_\w+) \}", allcode)):
    if o not in opdef and not o.endswith(("_modifier", "_programme")):
        err("unknown opinion modifier", o)
# 9 traits
trdef = set(re.findall(r"^\t(COLDWAR_EGY_\w+) = \{", T["common/country_leader/COLDWAR_EGY_1970_traits.txt"], re.M))
for t in set(re.findall(r"(COLDWAR_EGY_(?:field_marshal|air_force_hero|technocrat_in_chief|ailing_rais|consolidated_rule|rais_for_life))", allcode)):
    if t not in trdef:
        err("trait", t)
# 10 marker convention
for p in T:
    base = os.path.basename(p)
    if not (base.startswith("COLDWAR_") or p in ("history/countries/EGY - Egypt.txt", "common/scripted_effects/mdcw_1970_focus_tree_effects.txt")):
        err("file without COLDWAR marker", p)
print(len(errs), "errors")
for e in sorted(set(errs))[:120]:
    print(" ", e)
