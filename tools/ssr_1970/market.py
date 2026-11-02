# IMPERIA COLD WAR — Universal SSR market programme generator.
"""Generate only the market-owned files from the immutable approved snapshot."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import shared
import art

P = "COLDWAR_SSR_market_"
STATE_SELECTION_FLAGS = {tag: f"{P}selected_{tag}" for tag in shared.TAGS}


def _start_effects(market):
    blocks = []
    settlement_keys = sorted({k for d in market['decisions'] for k in d['modifiers']})
    for i, (course, item) in enumerate(market['courses'].items(), 1):
        init = "\n".join(f"\t\tset_variable = {{ {P}settlements_{k} = 0 }}" for k in settlement_keys)
        blocks.append(f'''COLDWAR_SSR_start_market_{course} = {{
\tif = {{ limit = {{ NOT = {{ has_country_flag = {P}course_started }} }}
\t\tset_country_flag = {P}course_started
\t\tset_country_flag = {P}{course}_started
\t\tset_country_flag = {{ flag = {P}{course}_deadline value = 1 days = {item['window']['days']} }}
\t\tset_variable = {{ {P}course = {i} }}
\t\tset_variable = {{ {P}original_burden = {shared.number(item['burden']['modifiers']['consumer_goods_factor'])} }}
\t\tset_variable = {{ {P}burden_remaining = {shared.number(item['burden']['modifiers']['consumer_goods_factor'])} }}
\t\tset_variable = {{ {P}relief_preview = {{ value = {shared.number(item['burden']['modifiers']['consumer_goods_factor'])} divide = -6 }} }}
\t\t{P}set_course_values_{course} = yes
\t\tset_country_flag = {P}burden_dirty
{init}
\t\tCOLDWAR_SSR_market_reconcile = yes
\t}}
}}''')
    return blocks


def _authority_triggers():
    models = shared.models()
    party_triggers = shared.data()['party_triggers']
    triggers = []
    for kind in ('market', 'public'):
        options = []
        for model in models.values():
            for node in model['nodes']:
                if node.get(f'{kind}_charter'):
                    slot = node['gate'].replace('slot', '')
                    party = party_triggers[slot]
                    options.append(f"AND = {{ {party} = yes has_country_flag = {node['receipt']} }}")
        triggers.append(f"COLDWAR_SSR_market_has_{kind}_authority = {{\n\tOR = {{\n\t\t" + "\n\t\t".join(options) + "\n\t}\n}")
    return "\n\n".join(triggers) + "\n"


def _finish_effects(market):
    blocks = []
    selected_state_guard = "OR = { " + " ".join(
        f"AND = {{ ROOT = {{ tag = {tag} }} has_state_flag = {flag} }}"
        for tag, flag in STATE_SELECTION_FLAGS.items()
    ) + " }"
    selected_state_eligible = f"any_state = {{ is_owned_and_controlled_by = ROOT is_core_of = ROOT check_variable = {{ building_level@industrial_complex > 1 }} {selected_state_guard} }}"
    for d in market['decisions']:
        sector, method = d['sector'], d['method']
        receipt = f"{P}lot_{sector}_settled"
        authority = ("COLDWAR_SSR_market_has_market_authority = yes" if method in ('auction', 'workers') else
                     "COLDWAR_SSR_market_has_public_authority = yes" if method == 'public' else "always = yes")
        valid_state = selected_state_eligible if method == 'liquidate' else "always = yes"
        close_state = []
        cleanup_state = []
        if method == 'liquidate':
            for tag, flag in STATE_SELECTION_FLAGS.items():
                close_state.append(f"if = {{ limit = {{ tag = {tag} }} every_state = {{ limit = {{ has_state_flag = {flag} is_owned_and_controlled_by = ROOT is_core_of = ROOT check_variable = {{ building_level@industrial_complex > 1 }} }} remove_building = {{ type = industrial_complex level = 1 }} clr_state_flag = {flag} }} }}")
                cleanup_state.append(f"if = {{ limit = {{ tag = {tag} }} every_state = {{ clr_state_flag = {flag} }} }}")
        mods = "\n".join(f"\t\t\tadd_to_variable = {{ {P}settlements_{k} = {shared.number(v)} }}" for k, v in d['modifiers'].items())
        fee, proceeds = shared.number(d['gdp_cost']), shared.number(d['gdp_income'])
        proceeds_effect = ""
        if d['gdp_income'] > 0:
            proceeds_effect = f"\t\tset_temp_variable = {{ treasury_change = {P}transaction_proceeds }}\n\t\tmodify_treasury_effect = yes"
        blocks.append(f'''{P}complete_{sector}_{method} = {{
\tset_temp_variable = {{ {P}transaction_cost = {{ value = gdp_total multiply = {fee} }} }}
\tset_temp_variable = {{ {P}transaction_proceeds = {{ value = gdp_total multiply = {proceeds} }} }}
\tif = {{
\t\tlimit = {{ COLDWAR_SSR_is_independent = yes has_country_flag = {P}pending_{sector}_{method} NOT = {{ has_country_flag = {receipt} }} {authority} {valid_state} check_variable = {{ treasury > {P}transaction_cost }} }}
\t\tset_temp_variable = {{ treasury_change = {P}transaction_cost }}
\t\tmultiply_temp_variable = {{ treasury_change = -1 }}
\t\tmodify_treasury_effect = yes
{proceeds_effect}
\t\t{"\n\t\t".join(close_state)}
\t\tset_country_flag = {receipt}
\t\tset_country_flag = {P}decision_{sector}_{method}_settled
\t\tset_country_flag = {{ flag = {P}lot_cooldown value = 1 days = 30 }}
\t\tset_variable = {{ {P}lot_count = {{ value = {P}lot_count add = 1 }} }}
{mods}
\t\tset_temp_variable = {{ {P}relief = {{ value = {P}original_burden divide = 6 }} }}
\t\tsubtract_from_variable = {{ {P}burden_remaining = {P}relief }}
\t\tif = {{ limit = {{ check_variable = {{ {P}burden_remaining < 0.00001 }} }} clear_variable = {P}burden_remaining }}
\t\tset_country_flag = {P}has_settlement
\t\tset_country_flag = {P}burden_dirty
\t\tset_country_flag = {P}settlements_dirty
\t}}
\tclr_country_flag = {P}pending_{sector}_{method}
\tclr_country_flag = {P}pending_transaction
\tclr_country_flag = {P}pending_timer
{"\n\t".join(cleanup_state)}
\tCOLDWAR_SSR_market_reconcile = yes
}}''')
    resolver = []
    for d in market['decisions']:
        s, m = d['sector'], d['method']
        resolver.append(f"if = {{ limit = {{ has_country_flag = {P}pending_{s}_{m} NOT = {{ has_country_flag = {P}pending_timer }} }} {P}complete_{s}_{m} = yes }}")
    blocks.append(f"{P}resolve_pending = {{\n\tif = {{ limit = {{ has_country_flag = {P}pending_transaction NOT = {{ has_country_flag = {P}pending_timer }} }}\n\t\t" + "\n\t\t".join(resolver) + "\n\t}\n}")
    return blocks


def _effects(data):
    market = data['market']
    lines = _start_effects(market)
    lines.extend(_course_value_effects(market))
    lines.extend(_finish_effects(market))
    lines.append(_reconcile_effect(market))
    lines.extend(_preview_effects(market))
    lines.append(_refresh_budget_effect(market))
    clears = "\n\t".join(f"clr_country_flag = {P}pending_{d['sector']}_{d['method']}" for d in market['decisions'])
    state_clears = "\n\t".join(f"if = {{ limit = {{ tag = {tag} }} every_state = {{ clr_state_flag = {flag} }} }}" for tag, flag in STATE_SELECTION_FLAGS.items())
    lines.append(f'''COLDWAR_SSR_market_cancel_pending = {{
\tclr_country_flag = {P}pending_transaction
\tclr_country_flag = {P}pending_timer
\t{clears}
\t{state_clears}
}}''')
    return "\n\n".join(lines) + "\n"


def _preview_effects(market):
    effects = []
    for course, item in market['courses'].items():
        effects.append(f'''COLDWAR_SSR_preview_market_{course} = {{
\teffect_tooltip = {{
\t\tadd_timed_idea = {{ idea = COLDWAR_SSR_market_preview_{course}_window days = {item['window']['days']} }}
\t\tadd_timed_idea = {{ idea = COLDWAR_SSR_market_preview_{course}_fiscal days = {item['fiscal']['days']} }}
\t\tadd_ideas = COLDWAR_SSR_market_preview_{course}_burden
\t}}
}}''')
    return effects


def _refresh_budget_effect(market):
    entries = []
    for d in market['decisions']:
        entries.append(f"\tset_variable = {{ {P}fee_{d['sector']}_{d['method']} = {{ value = gdp_total multiply = {shared.number(d['gdp_cost'])} }} }}")
    for course, item in market['courses'].items():
        weekly = item['weekly_gdp_cost']
        if weekly:
            entries.append(f"\tif = {{ limit = {{ has_country_flag = {P}{course}_started check_variable = {{ {P}burden_remaining > 0 }} }} set_variable = {{ COLDWAR_SSR_market_weekly_expense = {{ value = gdp_total multiply = {shared.number(weekly)} }} }} }}")
    return "\n".join([
        "COLDWAR_SSR_market_refresh_budget = {",
        "\tset_variable = { COLDWAR_SSR_market_weekly_expense = 0 }",
        f"\tif = {{ limit = {{ COLDWAR_SSR_is_independent = yes has_country_flag = {P}course_started }}\n" + "\n".join(entries) + "\n\t}",
        "}",
    ])


def _course_value_effects(market):
    result = []
    all_window = sorted({k for c in market['courses'].values() for k in c['window']['modifiers']})
    all_fiscal = sorted({k for c in market['courses'].values() for k in c['fiscal']['modifiers']})
    for course, item in market['courses'].items():
        assignments = [f"\tset_variable = {{ {P}window_{k} = {shared.number(v)} }}" for k, v in item['window']['modifiers'].items()]
        assignments += [f"\tset_variable = {{ {P}fiscal_{k} = {shared.number(v)} }}" for k, v in item['fiscal']['modifiers'].items()]
        clears = [f"\tclear_variable = {P}window_{k}" for k in all_window]
        clears += [f"\tclear_variable = {P}fiscal_{k}" for k in all_fiscal]
        result.append(f"{P}set_course_values_{course} = {{\n" + "\n".join(clears + assignments) + "\n}")
    return result


def _reconcile_effect(market):
    courses = market['courses']
    active_flags = "OR = { " + " ".join(f"has_country_flag = {P}{course}_deadline" for course in courses) + " }"
    active_condition = f"COLDWAR_SSR_is_independent = yes has_country_flag = {P}course_started {active_flags}"
    course_values = "\n\t\t".join(f"if = {{ limit = {{ has_country_flag = {P}{course}_deadline }} {P}set_course_values_{course} = yes }}" for course in courses)
    clear_vars = []
    for kind in ('window', 'fiscal'):
        keys = sorted({key for course in courses.values() for key in course[kind]['modifiers']})
        clear_vars.extend(f"clear_variable = {P}{kind}_{key}" for key in keys)
    clear_course_values = "\n\t\t".join(clear_vars)
    window_refresh = f"{active_condition} OR = {{ NOT = {{ has_country_flag = {P}window_applied }} NOT = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_window_dynamic_modifier }} }} NOT = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_fiscal_dynamic_modifier }} }} }}"
    window_cleanup = f"NOT = {{ {active_condition} }} OR = {{ has_country_flag = {P}window_applied has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_window_dynamic_modifier }} has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_fiscal_dynamic_modifier }} }}"
    burden_refresh = f"check_variable = {{ {P}burden_remaining > 0 }} OR = {{ NOT = {{ has_country_flag = {P}burden_applied }} has_country_flag = {P}burden_dirty NOT = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_burden_dynamic_modifier }} }} }}"
    settlements_refresh = f"has_country_flag = {P}has_settlement OR = {{ NOT = {{ has_country_flag = {P}settlements_applied }} has_country_flag = {P}settlements_dirty NOT = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_settlements_dynamic_modifier }} }} }}"
    settlements_cleanup = f"NOT = {{ has_country_flag = {P}has_settlement }} OR = {{ has_country_flag = {P}settlements_applied has_country_flag = {P}settlements_dirty has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_settlements_dynamic_modifier }} }}"
    return f'''COLDWAR_SSR_market_reconcile = {{
\t{P}resolve_pending = yes
\tif = {{ limit = {{ {window_refresh} }}
\t\tif = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_window_dynamic_modifier }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_window_dynamic_modifier }} }}
\t\tif = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_fiscal_dynamic_modifier }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_fiscal_dynamic_modifier }} }}
\t\t{course_values}
\t\tadd_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_window_dynamic_modifier }}
\t\tadd_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_fiscal_dynamic_modifier }}
\t\tset_country_flag = {P}window_applied
\t}}
\tif = {{ limit = {{ {window_cleanup} }}
\t\tif = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_window_dynamic_modifier }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_window_dynamic_modifier }} }}
\t\tif = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_fiscal_dynamic_modifier }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_fiscal_dynamic_modifier }} }}
\t\tclr_country_flag = {P}window_applied
\t\t{clear_course_values}
\t}}
\tif = {{ limit = {{ {burden_refresh} }}
\t\tif = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_burden_dynamic_modifier }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_burden_dynamic_modifier }} }}
\t\tadd_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_burden_dynamic_modifier }}
\t\tset_country_flag = {P}burden_applied
\t\tclr_country_flag = {P}burden_dirty
\t}}
\tif = {{ limit = {{ NOT = {{ check_variable = {{ {P}burden_remaining > 0 }} }} OR = {{ has_country_flag = {P}burden_applied has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_burden_dynamic_modifier }} }} }}
\t\tif = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_burden_dynamic_modifier }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_burden_dynamic_modifier }} }}
\t\tclr_country_flag = {P}burden_applied
\t\tclr_country_flag = {P}burden_dirty
\t}}
\tif = {{ limit = {{ {settlements_refresh} }}
\t\tif = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_settlements_dynamic_modifier }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_settlements_dynamic_modifier }} }}
\t\tadd_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_settlements_dynamic_modifier }}
\t\tset_country_flag = {P}settlements_applied
\t\tclr_country_flag = {P}settlements_dirty
\t}}
\tif = {{ limit = {{ {settlements_cleanup} }}
\t\tif = {{ limit = {{ has_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_settlements_dynamic_modifier }} }} remove_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_settlements_dynamic_modifier }} }}
\t\tclr_country_flag = {P}settlements_applied
\t\tclr_country_flag = {P}settlements_dirty
\t}}
}}'''


def _ideas(data):
    market = data['market']
    all_settlement = sorted({k for d in market['decisions'] for k in d['modifiers']})
    blocks = []
    for name, mapping in (
        ('window', sorted({k for c in market['courses'].values() for k in c['window']['modifiers']})),
        ('fiscal', sorted({k for c in market['courses'].values() for k in c['fiscal']['modifiers']})),
        ('burden', ['consumer_goods_factor']),
        ('settlements', all_settlement),
    ):
        lines = [f"COLDWAR_SSR_market_{name}_dynamic_modifier = {{", '\ticon = '+art.icon_for_idea(f"COLDWAR_SSR_market_{name}_dynamic_modifier")]
        for key in mapping:
            var = f"{P}burden_remaining" if name == 'burden' else f"{P}{name}_{key}"
            lines.append(f"\t{key} = {var}")
        lines.append("}")
        blocks.append("\n".join(lines))
    blocks.append(f'''COLDWAR_SSR_market_relief_preview_dynamic_modifier = {{
\ticon = {art.icon_for_idea('COLDWAR_SSR_market_relief_preview_dynamic_modifier')}
\tconsumer_goods_factor = {P}relief_preview
}}''')
    return "\n\n".join(blocks) + "\n"


def _preview_ideas(data):
    blocks = ["ideas = {", "\tcountry = {"]
    for course, item in data['market']['courses'].items():
        for suffix, section in (('window', 'window'), ('fiscal', 'fiscal')):
            mods = item[section]['modifiers']
            idea_id = f"COLDWAR_SSR_market_preview_{course}_{suffix}"
            lines = [f"\t\t{idea_id} = {{", "\t\t\tpicture = "+art.picture_for_idea(idea_id),
                     "\t\t\tallowed = { always = no }", "\t\t\tallowed_civil_war = { always = yes }",
                     "\t\t\tmodifier = {"]
            lines.extend(f"\t\t\t\t{k} = {shared.number(v)}" for k, v in mods.items())
            lines += ["\t\t\t}", "\t\t}"]
            blocks.append("\n".join(lines))
        idea_id = f"COLDWAR_SSR_market_preview_{course}_burden"
        lines = [f"\t\t{idea_id} = {{", "\t\t\tpicture = "+art.picture_for_idea(idea_id),
                 "\t\t\tallowed = { always = no }", "\t\t\tallowed_civil_war = { always = yes }",
                 "\t\t\tmodifier = {"]
        lines.extend(f"\t\t\t\t{k} = {shared.number(v)}" for k, v in item['burden']['modifiers'].items())
        lines += ["\t\t\t}", "\t\t}"]
        blocks.append("\n".join(lines))
    for method, item in data['market']['methods'].items():
        idea_id = f"COLDWAR_SSR_market_method_preview_{method}"
        lines = [f"\t\t{idea_id} = {{", "\t\t\tpicture = "+art.picture_for_idea(idea_id),
                 "\t\t\tallowed = { always = no }", "\t\t\tallowed_civil_war = { always = yes }",
                 "\t\t\tmodifier = {"]
        lines.extend(f"\t\t\t\t{k} = {shared.number(v)}" for k, v in item['modifiers'].items())
        lines += ["\t\t\t}", "\t\t}"]
        blocks.append("\n".join(lines))
    blocks.append("\t}")
    blocks.append("}")
    return "\n".join(blocks) + "\n"


def _decisions(market):
    lines = ["COLDWAR_SSR_market_category = {"]
    for d in market['decisions']:
        s, m = d['sector'], d['method']
        did = f"{P}{d['id'].removeprefix('COLDWAR_SSR_')}"
        auth = ("COLDWAR_SSR_market_has_market_authority = yes" if m in ('auction', 'workers') else
                "COLDWAR_SSR_market_has_public_authority = yes" if m == 'public' else "always = yes")
        visible = f"COLDWAR_SSR_is_independent = yes has_country_flag = {P}course_started NOT = {{ has_country_flag = {P}lot_{s}_settled }} NOT = {{ has_country_flag = {P}lot_cooldown }} NOT = {{ has_country_flag = {P}pending_transaction }} {auth}"
        affordable = f"check_variable = {{ treasury > {P}fee_{s}_{m} }}"
        block = [f"\t{did} = {{", "\t\ticon = generic_industry", f"\t\tvisible = {{ {visible} }}", f"\t\tavailable = {{ {visible} {affordable} }}"]
        if m == 'liquidate':
            block += ["\t\tstate_target = yes", "\t\ton_map_mode = map_only", f"\t\ttarget_trigger = {{ FROM = {{ is_owned_and_controlled_by = ROOT is_core_of = ROOT check_variable = {{ building_level@industrial_complex > 1 }} }} }}"]
            start = "\n\t\t\t".join(f"if = {{ limit = {{ tag = {tag} }} FROM = {{ set_state_flag = {flag} }} }}" for tag, flag in STATE_SELECTION_FLAGS.items())
        else:
            start = ""
        if start:
            start += "\n\t\t\t"
        start += f"set_country_flag = {P}pending_{s}_{m}\n\t\t\tset_country_flag = {{ flag = {P}pending_timer value = 1 days = {d['days']} }}\n\t\t\tset_country_flag = {P}pending_transaction"
        preview = [
            f"set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{shared.number(d['gdp_cost'])} }} }}",
            "modify_treasury_effect = yes",
        ]
        if d['gdp_income'] > 0:
            preview += [f"set_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = {shared.number(d['gdp_income'])} }} }}", "modify_treasury_effect = yes"]
        preview += [f"add_ideas = COLDWAR_SSR_market_method_preview_{m}", f"add_dynamic_modifier = {{ modifier = COLDWAR_SSR_market_relief_preview_dynamic_modifier }}"]
        preview_block = "\n\t\t\t".join(preview)
        tooltips = f"effect_tooltip = {{\n\t\t\t{preview_block}\n\t\t}}"
        if m == 'liquidate':
            tooltips += "\n\t\t\tFROM = { effect_tooltip = { remove_building = { type = industrial_complex level = 1 } } }"
        block += [f"\t\tcomplete_effect = {{\n\t\t\t{tooltips}\n\t\t\t{start}\n\t\t}}", "\t\tai_will_do = { base = 0 }", "\t}"]
        lines += block
    lines += [f"\tCOLDWAR_SSR_market_cancel_pending = {{", "\t\ticon = generic_industry", f"\t\tvisible = {{ has_country_flag = {P}pending_transaction }}", f"\t\tcomplete_effect = {{ COLDWAR_SSR_market_cancel_pending = yes }}", "\t\tai_will_do = { base = 0 }", "\t}", "}"]
    return "\n".join(lines) + "\n"


def _decision_category():
    return """COLDWAR_SSR_market_category = {
\tallowed = { COLDWAR_SSR_is_independent = yes }
\ticon = GFX_decision_category_generic_democracy
\tpriority = 97
\tvisible_when_empty = yes
}
"""


def _loc(data):
    loc = {"COLDWAR_SSR_market_category": "Sovereign Economic Transition", "COLDWAR_SSR_market_category_desc": "Choose how to settle six industrial lots after beginning a sovereign reform course.", "COLDWAR_SSR_market_cancel_pending": "Cancel Pending Settlement", "COLDWAR_SSR_market_cancel_pending_desc": "Cancel the current settlement before execution. No fee or proceeds are paid."}
    for d in data['market']['decisions']:
        did = f"{P}{d['id'].removeprefix('COLDWAR_SSR_')}"
        loc[did] = d['title']
        loc[did + '_desc'] = d['description']
        fee = shared.number(d['gdp_cost'] * 100)
        income = shared.number(d['gdp_income'] * 100)
    for method, item in data['market']['methods'].items():
        loc[f"COLDWAR_SSR_market_method_preview_{method}"] = item['title']
        loc[f"COLDWAR_SSR_market_method_preview_{method}_desc"] = item['description']
    loc["COLDWAR_SSR_market_relief_preview_dynamic_modifier"] = "One-Sixth Restructuring Relief"
    for course, item in data['market']['courses'].items():
        loc[f"COLDWAR_SSR_market_preview_{course}_window"] = f"{item['window']['name']}"
        loc[f"COLDWAR_SSR_market_preview_{course}_fiscal"] = f"{item['fiscal']['name']}"
        loc[f"COLDWAR_SSR_market_preview_{course}_burden"] = "Industrial Restructuring"
        loc[f"COLDWAR_SSR_market_preview_{course}_window_desc"] = item['description']
        loc[f"COLDWAR_SSR_market_preview_{course}_fiscal_desc"] = item['description']
        loc[f"COLDWAR_SSR_market_preview_{course}_burden_desc"] = "The restructuring burden persists until the six national industrial lots are settled."
    loc.update({
        "COLDWAR_SSR_market_window_dynamic_modifier": "Economic Transition Programme",
        "COLDWAR_SSR_market_fiscal_dynamic_modifier": "Transition Fiscal Measures",
        "COLDWAR_SSR_market_burden_dynamic_modifier": "Industrial Restructuring",
        "COLDWAR_SSR_market_settlements_dynamic_modifier": "Industrial Settlements",
    })
    return shared.loc_text(loc)


def generate():
    data = shared.data()
    outputs = [
        shared.write("common/scripted_effects/COLDWAR_SSR_market.txt", _effects(data)),
        shared.write("common/scripted_triggers/COLDWAR_SSR_market.txt", _authority_triggers()),
        shared.write("common/dynamic_modifiers/COLDWAR_SSR_market.txt", _ideas(data)),
        shared.write("common/ideas/COLDWAR_SSR_market_preview.txt", _preview_ideas(data)),
        shared.write("common/decisions/COLDWAR_SSR_market.txt", _decisions(data['market'])),
        shared.write("common/decisions/categories/COLDWAR_SSR_market.txt", _decision_category()),
        shared.write("localisation/english/COLDWAR_SSR_market_l_english.yml", _loc(data), localisation=True),
    ]
    # `shared.MARKER` may have been decoded from a legacy Windows code page.
    # Keep these owned outputs compliant even if shared.py awaits its own repair.
    expected_marker = "# IMPERIA COLD WAR \u2014 Universal SSR focus programme."
    for relative in outputs:
        path = shared.ROOT / relative
        is_loc = relative.endswith(".yml")
        raw = path.read_bytes()
        body = raw.decode("utf-8-sig" if is_loc else "utf-8")
        body = body.replace(shared.MARKER, expected_marker, 1)
        path.write_bytes(("\ufeff" if is_loc else "").encode("utf-8") + body.encode("utf-8"))
    return outputs


if __name__ == "__main__":
    print("\n".join(generate()))
