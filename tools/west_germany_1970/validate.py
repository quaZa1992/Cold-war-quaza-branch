"""Static checks for the generated West Germany 1970 files.

    python3 validate.py <build_root> <mod_root_for_reference>

Checks braces, ids, cross references, localisation, sprites, modifiers, focus layout.
Exit code 1 on errors; warnings are printed but do not fail.
"""
import glob
import os
import re
import sys

from cw_lib import P, check_braces

VANILLA_MODIFIERS = {"mobilization_speed", "monthly_population", 
    "army_core_defence_factor", "army_org_factor", "conscription", "consumer_goods_factor", "drift_defence_factor",
    "experience_gain_army", "industrial_capacity_factory", "max_planning", "political_power_factor",
    "production_factory_efficiency_gain_factor", "production_factory_max_efficiency_factor",
    "production_speed_buildings_factor", "research_speed_factor", "stability_factor", "trade_opinion_factor",
    "war_support_factor", "foreign_influence_defense_modifier", "conscription_factor", "opinion_gain_monthly_factor",
    "local_building_slots", "state_production_speed_buildings_factor",
}
TECH_CATS = {"CAT_computing", "CAT_electronics", "CAT_main_battle_tanks", "CAT_tank_engines", "CAT_artillery",
             "CAT_infantry_fighting_vehicles", "CAT_medium_aircraft", "CAT_air_engines", "CAT_wing_designs",
             "CAT_submarines", "CAT_submarine_engines", "CAT_frigates", "CAT_naval_anti_ship_missiles",
             "CAT_surface_to_air_missiles", "CAT_command_and_control_equipment", "CAT_microchips",
             "CAT_information_technology", "CAT_production_lines", "CAT_infrastructure", "CAT_orbital_launch_vehicles",
             "CAT_intermediate_range_ballistic_missiles", "CAT_nuclear_weapons", "CAT_nuclear", "CAT_nuclear_reactors"}
BUILDINGS = {"industrial_complex", "arms_factory", "infrastructure", "dockyard", "offices", "fossil_powerplant",
             "nuclear_reactor", "renewable_energy_infra", "air_base", "naval_base", "anti_air_building", "radar_station"}
VANILLA_TEXTURES = {"gfx/interface/goals/shine_overlay.dds"}
EXTERNAL_EVENTS = {"MD4_election_campaign.0"}
KNOWN_VARS = {"gdp_total", "labour_unions_opinion", "industrial_conglomerates_opinion", "small_medium_business_owners_opinion",
              "ruling_party", "inflation_rate_var", "global.mdcw_cw_arms", "global.mdcw_cw_tension"}

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def strip_comments(t):
    return re.sub(r"#[^\n]*", "", t)


def read(path):
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def main(build, ref):
    REF["root"] = ref
    files = {os.path.relpath(p, build): read(p) for p in glob.glob(os.path.join(build, "**", "*.*"), recursive=True)
             if p.endswith((".txt", ".gfx", ".yml", ".gui")) and "CREDITS" not in p and P in os.path.basename(p)}
    script = {k: strip_comments(v) for k, v in files.items() if not k.endswith(".yml")}
    allscript = "\n".join(script.values())
    for k, v in script.items():
        try:
            check_braces(v, k)
        except ValueError as e:
            err(str(e))

    # ---------------------------------------------------------- localisation
    loc_text = files[f"localisation/english/{P}_l_english.yml"]
    if not loc_text.startswith("l_english:"):
        err("localisation header")
    loc = dict(re.findall(r'^ ([^:\s]+):0 "(.*)"$', loc_text, re.M))

    def need_loc(key, where):
        if key not in loc:
            err(f"missing localisation {key} ({where})")

    # ---------------------------------------------------------- events
    ev_text = script[f"events/{P}_events.txt"]
    ev_defined = set(re.findall(r"^\tid = (\S+)", ev_text, re.M))
    for ns in set(re.findall(r"^add_namespace = (\S+)", ev_text, re.M)):
        pass
    for ref_id in set(re.findall(r"country_event = \{ id = (\S+)", allscript)) | set(re.findall(r"country_event = (\S+\.\d+)\b", allscript)):
        if ref_id not in ev_defined and ref_id not in EXTERNAL_EVENTS:
            err(f"event {ref_id} referenced but not defined")
    unreferenced = {e for e in ev_defined if not re.search(r"id = " + re.escape(e) + r"\b(?! *\n\t(hidden|title))", allscript.replace(f"\tid = {e}\n", ""))}
    for e in sorted(unreferenced):
        warn(f"event {e} is never fired")
    for key in re.findall(r"(?:title|desc|name|text) = (COLDWAR_(?:GER|DDR)\.\S+)", ev_text):
        need_loc(key, "event")
    for pic in set(re.findall(r"picture = (GFX_\S+)", ev_text)):
        if not exists_sprite(pic, "events"):
            err(f"event picture {pic} not found")

    # ---------------------------------------------------------- ideas
    idea_text = script[f"common/ideas/{P}_ideas.txt"]
    ideas_defined = set(re.findall(r"^\t\t(COLDWAR_GER_1970_idea_\S+) = \{", idea_text, re.M))
    for i in ideas_defined:
        need_loc(i, "idea")
        need_loc(i + "_desc", "idea")
    for pic in re.findall(r"picture = (\S+)", idea_text):
        if not exists_sprite("GFX_idea_" + pic, "ideas"):
            err(f"idea picture {pic} not found")
    for ref_i in set(re.findall(r"(COLDWAR_GER_1970_idea_[a-z0-9_]+)", allscript)):
        if ref_i not in ideas_defined:
            err(f"idea {ref_i} referenced but not defined")
    for i in ideas_defined:
        if allscript.count(i) < 2:
            warn(f"idea {i} is never added")
    custom = set()
    for p in glob.glob(os.path.join(ref, "common/modifier_definitions/*.txt")):
        custom |= set(re.findall(r"^(\w+) = \{", strip_comments(read(p)), re.M))
    mod_whitelist = VANILLA_MODIFIERS | custom
    for block in re.findall(r"modifier = \{([^{}]*)\}", idea_text):
        for m in re.findall(r"(\w+) =", block):
            if m not in mod_whitelist:
                err(f"unknown idea modifier {m}")
    dm = script[f"common/dynamic_modifiers/{P}_dynamic_modifiers.txt"]
    for m in re.findall(r"^\t(\w+) = (?:cw\w+|-?[\d.]+)$", dm, re.M):
        if m not in mod_whitelist:
            err(f"unknown dynamic modifier {m}")
    for m in set(re.findall(r"^\t+(\w+) = -?[\d.]+$", script[f"common/bop/{P}_bop.txt"], re.M)) - {"initial_value", "min", "max"}:
        if m not in mod_whitelist:
            err(f"unknown bop modifier {m}")

    # ---------------------------------------------------------- focus tree
    ft = script[f"common/national_focus/{P}_focus.txt"]
    blocks = re.findall(r"\tfocus = \{\n(.*?)\n\t\}", ft, re.S)
    focus, raw = {}, {}
    for b in blocks:
        fid = re.search(r"id = (\S+)", b).group(1)
        if fid in focus:
            err(f"duplicate focus {fid}")
        x = int(re.search(r"\bx = (-?\d+)", b).group(1))
        y = int(re.search(r"\by = (-?\d+)", b).group(1))
        rel = re.search(r"relative_position_id = (\S+)", b)
        pre = re.findall(r"prerequisite = \{([^}]*)\}", b)
        mut = re.findall(r"mutually_exclusive = \{([^}]*)\}", b)
        icon = re.search(r"icon = (\S+)", b).group(1)
        cost = float(re.search(r"cost = ([\d.]+)", b).group(1))
        raw[fid] = (x, y, rel.group(1) if rel else None)
        focus[fid] = dict(pre=[re.findall(r"focus = (\S+)", p) for p in pre], cost=cost,
                          mut=sum((re.findall(r"focus = (\S+)", m) for m in mut), []), icon=icon, block=b)

    def absolute(fid, depth=0):
        x, y, rel = raw[fid]
        if rel is None:
            return x, y
        if rel not in raw or depth > 50:
            err(f"{fid}: relative position {rel} unknown")
            return x, y
        rx, ry = absolute(rel, depth + 1)
        return rx + x, ry + y
    for fid in focus:
        focus[fid]["x"], focus[fid]["y"] = absolute(fid)
    costs = [f["cost"] for f in focus.values()]
    if costs and sum(costs) / len(costs) > 8:
        warn(f"average focus cost {sum(costs) / len(costs):.1f} is high")
    for fid, f in focus.items():
        body = re.search(r"completion_reward = \{(.*)\}", f["block"], re.S)
        txt = body.group(1) if body else ""
        meaningful = re.search(r"custom_effect_tooltip|add_ideas|swap_ideas|add_building_construction|add_dynamic_modifier|build_railway|country_event|"
                               r"change_influence|add_opinion_modifier|change_\w+_opinion|add_tech_bonus|set_country_flag|treasury|power_balance", txt)
        if not meaningful:
            warn(f"focus {fid} has no system effect")
    gfx = script[f"interface/{P}_goals.gfx"] + script[f"interface/{P}_goals_shine.gfx"]
    sprites = set(re.findall(r'name = "(\S+)"', gfx))
    pos = {}
    for fid, f in focus.items():
        need_loc(fid, "focus")
        need_loc(fid + "_desc", "focus")
        if f["icon"] not in sprites or f["icon"] + "_shine" not in sprites:
            err(f"focus icon {f['icon']} missing sprite")
        if (f["x"], f["y"]) in pos:
            err(f"focus overlap {fid} and {pos[(f['x'], f['y'])]} at {f['x']},{f['y']}")
        pos[(f["x"], f["y"])] = fid
        for group in f["pre"]:
            for p in group:
                if p not in focus:
                    err(f"{fid}: prerequisite {p} missing")
                elif focus[p]["y"] >= f["y"]:
                    warn(f"{fid}: prerequisite {p} is not above it")
        for m in f["mut"]:
            if m not in focus:
                err(f"{fid}: mutex {m} missing")
            elif fid not in focus[m]["mut"]:
                err(f"{fid}: mutex with {m} is not symmetric")
    for tex in re.findall(r'texturefile = "(\S+)"', gfx):
        if not exists_texture(tex):
            err(f"texture {tex} missing")
    sov_focus = read(os.path.join(ref, "common/national_focus/COLDWAR_SOV_1970_focus.txt")) if os.path.exists(os.path.join(ref, "common/national_focus/COLDWAR_SOV_1970_focus.txt")) else ""
    for ref_f in set(re.findall(r"has_completed_focus = (\S+)", allscript)):
        if ref_f.startswith(P):
            if ref_f not in focus:
                err(f"has_completed_focus {ref_f} unknown")
        elif ref_f.startswith("COLDWAR_SOV") and f"id = {ref_f}" not in sov_focus:
            err(f"Soviet focus {ref_f} not found")

    # ---------------------------------------------------------- decisions
    dec = script[f"common/decisions/{P}_decisions.txt"]
    cats = script[f"common/decisions/categories/{P}_categories.txt"]
    cat_ids = set(re.findall(r"^(\S+) = \{", cats, re.M))
    for c in cat_ids:
        need_loc(c, "category")
        if f"\n{c} = {{" not in "\n" + dec:
            warn(f"category {c} has no decisions")
    for d in re.findall(r"^\t(COLDWAR_GER_1970_dec_\S+) = \{", dec, re.M):
        need_loc(d, "decision")
        need_loc(d + "_desc", "decision")
    for icon in set(re.findall(r"icon = (GFX_\S+)", dec + cats)):
        if not exists_sprite(icon, "decisions"):
            err(f"decision icon {icon} missing")
    if f"decision_category = {P}_deutschlandpolitik_category" in script[f"common/bop/{P}_bop.txt"] and f"{P}_deutschlandpolitik_category" not in cat_ids:
        err("BoP decision category missing")


    # ---------------------------------------------------------- raw conditions the game cannot localise
    def strip_ctt(t):
        out, i = [], 0
        while True:
            j = t.find("custom_trigger_tooltip = {", i)
            if j < 0:
                out.append(t[i:]); break
            out.append(t[i:j]); d = 0
            for k in range(j, len(t)):
                if t[k] == "{": d += 1
                elif t[k] == "}":
                    d -= 1
                    if d == 0: break
            i = k + 1
        return "".join(out)
    for where, txt in (("focus", ft), ("decision", dec)):
        for av in re.findall(r"\n\t+available = \{ (.*) \}\n", txt):
            raw = re.findall(r"(has_country_flag|has_global_flag|check_variable|is_in_array) = ", strip_ctt(av))
            if raw:
                err(f"{where} availability shows raw {raw[0]}: {av[:120]}")
    for block in re.findall(r"completion_reward = \{(.*?)\n\t\t\}", ft, re.S):
        if re.search(r"(?<!hidden_effect = \{ )\b(set_variable|add_to_variable|subtract_from_variable) = ", block.replace("\n", " ")):
            pass

    # ---------------------------------------------------------- tooltips and loc in script
    for key in set(re.findall(r"custom_effect_tooltip = (\S+)", allscript)):
        if key.startswith(("COLDWAR", "COLDWAR_GER_1970")):
            need_loc(key, "tooltip")
    for key in set(re.findall(r"(?:left_side|right_side|id) = (COLDWAR_GER_1970_bop_\S+)", allscript)):
        need_loc(key, "bop")
    for key in set(re.findall(r"name = (COLDWAR_GER_1970_shortcut_\S+)", ft)):
        need_loc(key, "shortcut")
    for key in set(re.findall(r"tech_bonus = \{ name = (\S+)", allscript)):
        need_loc(key, "tech bonus")

    # ---------------------------------------------------------- techs, buildings, opinion modifiers
    for c in set(re.findall(r"category = (CAT_\w+)", allscript)):
        if c not in TECH_CATS:
            err(f"unknown tech category {c}")
    for b in set(re.findall(r"type = (\w+) level", allscript)) | set(re.findall(r"building = (\w+) size", allscript)):
        if b not in BUILDINGS:
            err(f"unknown building {b}")
    opinions = set()
    for p in glob.glob(os.path.join(ref, "common/opinion_modifiers/*.txt")):
        opinions |= set(re.findall(r"^\s*(\w+) = \{", read(p), re.M))
    for o in set(re.findall(r"add_opinion_modifier = \{ target = \S+ modifier = (\w+)", allscript)) | set(re.findall(r"remove_opinion_modifier = \{ target = \S+ modifier = (\w+)", allscript)):
        if o not in opinions:
            err(f"opinion modifier {o} unknown")

    # ---------------------------------------------------------- variables shown in loc
    set_vars = set(re.findall(r"(?:set_variable|add_to_variable|subtract_from_variable) = \{ (\w+) =", allscript))
    for k, text in loc.items():
        for var in re.findall(r"\[\?(?:(?:DDR|GER|ROOT|FROM)\.)?([\w.]+)\|", text):
            if var not in set_vars and var not in KNOWN_VARS and "global." + var not in KNOWN_VARS:
                err(f"loc {k} shows variable {var} that is never set")

    # ---------------------------------------------------------- flags
    checked = set(re.findall(r"has_(?:country|global)_flag = (COLDWAR_GER_1970_\w+)", allscript))
    set_f = set(re.findall(r"set_(?:country|global)_flag = (?:\{ flag = )?(COLDWAR_GER_1970_\w+)", allscript))
    for f_ in sorted(checked - set_f):
        warn(f"flag {f_} is checked but never set")

    windows_checks(build, files, script, allscript, loc, need_loc, ev_defined)

    # ---------------------------------------------------------- report
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"{len(focus)} focuses, {len(ev_defined)} events, {len(ideas_defined)} ideas, {len(loc)} loc keys; "
          f"{len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


VANILLA_GUI_SPRITES = {"GFX_closebutton"}
LOC_FUNCS = {"Root.GetLeader", "DDR.GetLeader", "GER.GetLeader", "Root.GetName", "GetDateText", "This.GetName", "ROOT.GetName",
             "Root.GetNameDef", "From.GetName", "FROM.GetName"}


def windows_checks(build, files, script, allscript, loc, need_loc, ev_defined):
    """Checks for the windows (rivalry, security): GUI elements, sprites, scripted GUI hooks,
    scripted localisation, effect and trigger references, variables."""
    gui = "\n".join(v for k, v in script.items() if k.endswith(".gui"))
    gfx = "\n".join(v for k, v in script.items() if k.endswith(".gfx"))
    sg = "\n".join(v for k, v in script.items() if k.startswith("common/scripted_guis/"))
    sl = "\n".join(v for k, v in script.items() if k.startswith("common/scripted_localisation/"))
    if not gui:
        return
    elements = set(re.findall(r'name = "(\w+)"', gui))
    # sprites used in the gui
    ours = dict(re.findall(r'name = "(GFX_\w+)"\s+(?:size = \{[^}]*\}\s+)?texturefile = "([^"]+)"', gfx))
    frames = dict((n, int(f)) for n, _t, f in re.findall(r'name = "(GFX_\w+)"\s+texturefile = "([^"]+)"\s+noOfFrames = (\d+)', gfx))
    mod_cw = read(os.path.join(REF["root"], "interface/mdcw_cold_war.gfx")) if os.path.exists(os.path.join(REF["root"], "interface/mdcw_cold_war.gfx")) else ""
    mod_sprites = set(re.findall(r'name = "(GFX_\w+)"', mod_cw))
    for spr in set(re.findall(r'(?:spriteType|quadTextureSprite) = "(GFX_\w+)"', gui)):
        if spr not in ours and spr not in mod_sprites and spr not in VANILLA_GUI_SPRITES and not exists_sprite(spr, "events"):
            err(f"gui sprite {spr} not defined")
    for name, tex in re.findall(r'name = "(GFX_\w+)"\s+texturefile = "([^"]+)"', gfx):
        if name.startswith("GFX_cwgg") and not os.path.exists(os.path.join(build, tex)):
            err(f"texture {tex} for {name} not written")
    # loc keys in the gui
    for key in set(re.findall(r'(?:text|pdx_tooltip) = "(\w+)"', gui)):
        need_loc(key, "gui")
    # scripted gui hooks must point at elements
    for win in re.findall(r'window_name = "(\w+)"', sg):
        if win not in elements:
            err(f"scripted gui window {win} missing in .gui")
    for hook in set(re.findall(r"^\t\t\t(\w+?)(?:_visible|_click_enabled|_click) = \{", sg, re.M)):
        if hook not in elements:
            err(f"scripted gui hook for unknown element {hook}")
    for el, body in re.findall(r"^\t\t\t(\w+) = \{ ((?:frame|x|y|image) = [^}]*)\}", sg, re.M):
        if el not in elements:
            err(f"property for unknown element {el}")
        if "frame =" in body:
            m = re.search(r'name = "' + el + r'"\s+spriteType = "(GFX_\w+)"', gui)
            if m and m.group(1) not in frames:
                err(f"element {el} uses frames but {m.group(1)} has no noOfFrames")
    # scripted localisation
    defined = set(re.findall(r"^\tname = (\w+)", sl, re.M))
    for key in set(re.findall(r"localization_key = (\w+)", sl)):
        need_loc(key, "scripted loc")
    for k, text in loc.items():
        for ref_ in re.findall(r"\[([A-Za-z][\w.]*)\]", text):
            if ref_ in LOC_FUNCS or "." in ref_ and ref_.split(".")[-1].startswith("Get"):
                continue
            if ref_ not in defined:
                err(f"loc {k} uses [{ref_}] which is not defined")
        for ref_ in re.findall(r"\$(\w+)\$", text):
            need_loc(ref_, f"$ in {k}")
    # effects and triggers with our prefix must exist
    eff_defs = set(re.findall(r"^(\w+) = \{", "\n".join(v for kk, v in script.items() if kk.startswith("common/scripted_effects/")), re.M))
    trg_defs = set(re.findall(r"^(\w+) = \{", "\n".join(v for kk, v in script.items() if kk.startswith("common/scripted_triggers/")), re.M))
    mod_eff = set(open(os.path.join(LIST_DIR, "def_eff.txt")).read().split()) if os.path.exists(os.path.join(LIST_DIR, "def_eff.txt")) else set()
    mod_trg = set(open(os.path.join(LIST_DIR, "def_trg.txt")).read().split()) if os.path.exists(os.path.join(LIST_DIR, "def_trg.txt")) else set()
    for name in set(re.findall(r"\b(COLDWAR_GER_1970_\w+) = yes", allscript)):
        if name not in eff_defs and name not in trg_defs:
            err(f"{name} = yes but no such effect or trigger")
    for name in set(re.findall(r"\b(mdcw_cw_\w+|NATO_\w+|IMP_\w+|change_\w+_opinion|modify_\w+_effect|europeanism_change|increase_corruption|decrease_corruption) = yes", allscript)):
        if mod_eff and name not in mod_eff and name not in mod_trg:
            err(f"mod effect {name} not found in the mod")
    # GGR events need localisation
    for key in re.findall(r"(?:title|desc|name|text) = (COLDWAR_GGR\.\S+)", script[f"events/{P}_events.txt"]):
        need_loc(key, "event")
    # cwgg variables: read but never written
    written = set(re.findall(r"(?:set_variable|add_to_variable|subtract_from_variable|multiply_variable|divide_variable) = \{ (cwgg_\w+) =", allscript))
    written |= set(re.findall(r"(?:set_temp_variable|add_to_temp_variable) = \{ (cwgg_\w+) =", allscript))
    for var in set(re.findall(r"check_variable = \{ (cwgg_\w+) [<>=]", allscript)) | set(re.findall(r"\b(?:x|y|frame) = (cwgg_\w+)", sg)):
        if var not in written:
            err(f"variable {var} is read but never set")
    for k, text in loc.items():
        for var in re.findall(r"\[\?(cwgg_\w+)\|", text):
            if var not in written:
                err(f"loc {k} shows {var} that is never set")
    # flags read but never set (cwgg_)
    checked = set(re.findall(r"has_(?:country|global)_flag = (cwgg_\w+)", allscript))
    set_f = set(re.findall(r"set_(?:country|global)_flag = (?:\{ flag = )?(cwgg_\w+)", allscript))
    for f_ in sorted(checked - set_f):
        warn(f"flag {f_} is checked but never set")


SPRITES = {}
LIST_DIR = os.environ.get("CWGER_SPRITE_LISTS", "/tmp/claude-0")
REF = {"root": None}


def _load_sprites():
    for k in ("events", "ideas", "decisions", "goals", "_textures"):
        SPRITES[k] = set()
    for k, f in (("events", "events_list.txt"), ("ideas", "ideas_list.txt"), ("decisions", "dec_list.txt"), ("goals", "goals_list.txt")):
        p = os.path.join(LIST_DIR, f)
        if os.path.exists(p):
            for line in open(p):
                parts = line.split()
                if parts:
                    SPRITES[k].add(parts[0])
                    if len(parts) > 1:
                        SPRITES["_textures"].add(parts[1])
    # sprites declared anywhere in the reference mod's interface folder
    if REF["root"]:
        for p in glob.glob(os.path.join(REF["root"], "interface", "*.gfx")):
            t = read(p)
            for name, tex in re.findall(r'name\s*=\s*"?(\w+)"?\s+texturefile\s*=\s*"([^"]+)"', t, re.I):
                for k in ("events", "ideas", "decisions", "goals"):
                    SPRITES[k].add(name)
                SPRITES["_textures"].add(tex)
    SPRITES["_any"] = bool(sum(len(s) for s in SPRITES.values()))


def exists_sprite(name, kind):
    if not SPRITES:
        _load_sprites()
    if not SPRITES["_any"]:
        return True  # nothing to check against
    return name in SPRITES[kind]


def exists_texture(tex):
    if not SPRITES:
        _load_sprites()
    if not SPRITES["_any"]:
        return True
    return tex in SPRITES["_textures"] or tex in VANILLA_TEXTURES


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
