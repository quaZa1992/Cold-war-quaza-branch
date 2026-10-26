# IMPERIA CW — Cold War: mutually authorized Korean-American exercises.
"""Invitation -> US assent -> Korean authorization -> paid training -> outcome."""
P = "COLDWAR_KOR_usfk_exercise_"
NS = "COLDWAR_KOR_usfk_exercise"
HEADER = "# IMPERIA CW — Cold War: Korean-American combined exercises.\n"
SPECS = {
    "field": {"kind": 1, "cost": 2, "us_cost": 1, "weekly": 0.004, "xp": 40, "us_xp": 15,
        "burden": {"equipment_cost_multiplier_modifier": .03, "personnel_cost_multiplier_modifier": .03, "trade_opinion_factor": -.03},
        "reward": {"army_org_factor": .05, "army_morale_factor": .04, "supply_consumption_factor": .06},
        "us_reward": {"army_org_factor": .015, "supply_consumption_factor": .03}},
    "staff": {"kind": 2, "cost": 1, "us_cost": 1, "weekly": .002, "xp": 20, "us_xp": 10,
        "burden": {"bureaucracy_cost_multiplier_modifier": .02},
        "reward": {"planning_speed": .08, "max_planning_factor": .05, "bureaucracy_cost_multiplier_modifier": .03},
        "us_reward": {"planning_speed": .04, "bureaucracy_cost_multiplier_modifier": .02}},
}
def b(name, body): return name + " = {\n" + body + "\n}\n"
def f(name): return P + name
def block(name, body): return b(f(name), body)
def cost(amount): return f"set_temp_variable = {{ treasury_change = -{amount} }} modify_treasury_effect = yes"
def idea(kind, role): return "COLDWAR_KOR_usfk_" + kind + "_" + role
def kind_test(s): return f'KOR = {{ check_variable = {{ {f("kind")} = {s["kind"]} }} }}'

def preview(kind):
    s = SPECS[kind]
    return ("custom_effect_tooltip = " + f("launch_terms_tt") + "\n" +
        b("effect_tooltip", b("KOR", cost(s["cost"]) + f' add_timed_idea = {{ idea = {idea(kind,"burden")} days = 30 }}') +
            b("USA", cost(s["us_cost"]) + f' add_timed_idea = {{ idea = {idea(kind,"burden")} days = 30 }}')) +
        "custom_effect_tooltip = " + f(kind + "_weekly_tt") + "\ncustom_effect_tooltip = " + f("completion_terms_tt") + "\n" +
        b("effect_tooltip", b("KOR", f'army_experience = {s["xp"]} add_timed_idea = {{ idea = {idea(kind,"kor_reward")} days = 180 }}') +
            b("USA", f'army_experience = {s["us_xp"]} add_timed_idea = {{ idea = {idea(kind,"usa_reward")} days = 180 }}')))

def build(data):
    loc = {}; triggers = []; effects = []; events = ["add_namespace = " + NS]; decisions = []; ideas = []
    pair = 'COLDWAR_KOR_usfk_cooperation_live = yes KOR = { NOT = { has_war_with = NKO } } USA = { NOT = { has_war_with = NKO } }'
    triggers += [
        block("pair_active", pair),
        block("field_forces", 'KOR = { has_army_size = { size > 0 } } USA = { has_army_size = { size > 0 } }'),
        block("training_feasible", f'{f("pair_active")} = yes OR = {{ KOR = {{ check_variable = {{ {f("kind")} = 2 }} }} {f("field_forces")} = yes }}'),
        block("can_invite", f'tag = KOR has_country_flag = COLDWAR_KOR_combined_exercises_paid {f("pair_active")} = yes NOT = {{ has_country_flag = {f("pending")} }} NOT = {{ has_country_flag = {f("running")} }} NOT = {{ has_country_flag = {f("cooldown")} }}'),
        block("offer_current", f'{f("pair_active")} = yes KOR = {{ has_country_flag = {f("pending")} has_country_flag = {f("offer_open")} check_variable = {{ var = {f("sender_party")} value = ruling_party compare = equals }} check_variable = {{ var = {f("sender_office_epoch")} value = COLDWAR_KOR_office_epoch compare = equals }} }} USA = {{ has_country_flag = {f("pending")} has_country_flag = {f("offer_open")} }}'),
        block("can_accept", f'tag = USA {f("offer_current")} = yes NOT = {{ has_country_flag = {f("assent")} }}'),
        block("can_conduct", f'tag = KOR {f("offer_current")} = yes {f("training_feasible")} = yes USA = {{ has_country_flag = {f("assent")} }} NOT = {{ has_country_flag = {f("running")} }}'),
        block("training_live", f'{f("training_feasible")} = yes KOR = {{ has_country_flag = {f("running")} has_country_flag = {f("training_open")} }} USA = {{ has_country_flag = {f("running")} has_country_flag = {f("training_open")} }}')
    ]
    clear = " ".join(f"clr_country_flag = {f(x)}" for x in ("pending", "offer_open", "assent"))
    effects += [block("clear_offer", b("KOR", clear) + b("USA", clear))]
    for kind, s in SPECS.items():
        body = f'if = {{ limit = {{ {f("can_invite")} = yes }} set_variable = {{ {f("kind")} = {s["kind"]} }} set_variable = {{ {f("sender_party")} = ruling_party }} set_variable = {{ {f("sender_office_epoch")} = COLDWAR_KOR_office_epoch }} {f("clear_offer")} = yes '
        body += b("KOR", f'set_country_flag = {f("pending")} set_country_flag = {{ flag = {f("offer_open")} days = 30 }}')
        body += b("USA", f'set_country_flag = {f("pending")} set_country_flag = {{ flag = {f("offer_open")} days = 30 }} country_event = {{ id = {NS}.1 }}')
        effects += [block("invite_" + kind, body + " }")]
    effects += [
        block("accept", f'if = {{ limit = {{ {f("can_accept")} = yes }} set_country_flag = {{ flag = {f("assent")} days = 30 }} set_country_flag = {{ flag = {f("offer_open")} days = 30 }} KOR = {{ set_country_flag = {{ flag = {f("offer_open")} days = 30 }} country_event = {{ id = {NS}.2 }} }} }}'),
        block("decline", f'if = {{ limit = {{ {f("can_accept")} = yes }} {f("clear_offer")} = yes KOR = {{ set_country_flag = {{ flag = {f("cooldown")} days = 90 }} country_event = {{ id = {NS}.5 }} }} }}'),
        block("cancel", f'if = {{ limit = {{ tag = KOR has_country_flag = {f("pending")} }} {f("clear_offer")} = yes set_country_flag = {{ flag = {f("cooldown")} days = 30 }} USA = {{ country_event = {{ id = {NS}.6 }} }} }}'),
        block("release_access", f'if = {{ limit = {{ KOR = {{ has_country_flag = {f("temporary_access")} }} }} USA = {{ diplomatic_relation = {{ country = KOR relation = military_access active = no }} }} KOR = {{ clr_country_flag = {f("temporary_access")} }} }}')
    ]
    body = f'if = {{ limit = {{ {f("can_conduct")} = yes }} if = {{ limit = {{ NOT = {{ USA = {{ has_military_access_to = KOR }} }} }} give_military_access = USA set_country_flag = {f("temporary_access")} }} '
    for kind, s in SPECS.items():
        body += b("if", b("limit", kind_test(s)) +
            b("KOR", cost(s["cost"]) + f' add_timed_idea = {{ idea = {idea(kind,"burden")} days = 30 }}') +
            b("USA", cost(s["us_cost"]) + f' add_timed_idea = {{ idea = {idea(kind,"burden")} days = 30 }}'))
    body += f'{f("clear_offer")} = yes set_country_flag = {{ flag = {f("cooldown")} days = 180 }} '
    for tag in ("KOR", "USA"):
        body += b(tag, f'set_country_flag = {f("running")} set_country_flag = {{ flag = {f("training_open")} days = 30 }}')
    effects += [block("conduct", body + " }")]
    close_training = " ".join(f"clr_country_flag = {f(x)}" for x in ("running", "training_open"))
    cleanup = " ".join(f"remove_ideas = {idea(k, role)}" for k in SPECS for role in ("burden", "kor_reward", "usa_reward"))
    running = f'OR = {{ KOR = {{ has_country_flag = {f("running")} }} USA = {{ has_country_flag = {f("running")} }} }}'
    body = f'if = {{ limit = {{ {running} }} ' + b("KOR", close_training + f' country_event = {{ id = {NS}.9 }}') + b("USA", close_training + f' country_event = {{ id = {NS}.9 }}') + " } "
    effects += [block("abort", body + b("KOR", cleanup) + b("USA", cleanup) + f'{f("release_access")} = yes')]
    body = f'if = {{ limit = {{ {f("training_feasible")} = yes KOR = {{ has_country_flag = {f("running")} NOT = {{ has_country_flag = {f("training_open")} }} }} USA = {{ has_country_flag = {f("running")} }} }} '
    for kind, s in SPECS.items():
        eid = 3 if kind == "field" else 4
        body += b("if", b("limit", kind_test(s)) +
            b("KOR", f'army_experience = {s["xp"]} add_timed_idea = {{ idea = {idea(kind,"kor_reward")} days = 180 }} country_event = {{ id = {NS}.{eid} }}') +
            b("USA", f'army_experience = {s["us_xp"]} add_timed_idea = {{ idea = {idea(kind,"usa_reward")} days = 180 }} country_event = {{ id = {NS}.{eid} }}'))
    for tag in ("KOR", "USA"):
        body += b(tag, close_training + " " + " ".join(f'remove_ideas = {idea(k,"burden")}' for k in SPECS))
    effects += [block("complete", body + f'{f("release_access")} = yes }}')]
    reward_active = "OR = { " + " ".join(b(tag, "OR = { " + " ".join(f"has_idea = {idea(k, role)}" for k in SPECS for role in ("kor_reward", "usa_reward")) + " }") for tag in ("KOR", "USA")) + " }"
    body = f'if = {{ limit = {{ OR = {{ NOT = {{ {f("pair_active")} = yes }} AND = {{ {running} NOT = {{ {f("training_feasible")} = yes }} }} }} OR = {{ {running} {reward_active} }} }} {f("abort")} = yes }} '
    body += f'if = {{ limit = {{ KOR = {{ has_country_flag = {f("pending")} }} NOT = {{ {f("offer_current")} = yes }} }} {f("clear_offer")} = yes KOR = {{ set_country_flag = {{ flag = {f("cooldown")} days = 30 }} country_event = {{ id = {NS}.10 }} }} }} {f("complete")} = yes'
    effects += [block("daily", body)]
    body = ""
    for kind, s in SPECS.items():
        body += b("if", b("limit", f'{f("training_live")} = yes {kind_test(s)} OR = {{ tag = KOR tag = USA }}') + f'add_to_variable = {{ additional_expenses_rate = {s["weekly"]} }}')
    effects += [block("expenses", body), b("COLDWAR_KOR_action_open_usfk_exercises", f'if = {{ limit = {{ {f("can_invite")} = yes }} country_event = {{ id = {NS}.7 }} }}')]
    for kind, s in SPECS.items():
        for role, mods in (("burden", s["burden"]), ("kor_reward", s["reward"]), ("usa_reward", s["us_reward"])):
            key = idea(kind, role)
            loc[key] = ("Field Exercise Commitments" if kind == "field" else "Command-Post Commitments") if role == "burden" else ("Combined Field Readiness" if kind == "field" else "Combined Command Planning")
            loc[key + "_desc"] = "The armed forces are carrying the agreed training commitments." if role == "burden" else "The armed forces apply the lessons of completed Korean-American training."
            ideas.append(b(key, "picture = COLDWAR_KOR_spirit_training allowed = { always = yes } removal_cost = -1 " + b("modifier", " ".join(f"{k} = {v}" for k, v in mods.items()))))
    def option(eid, slug, label, trigger="", display="", effect=""):
        key = f"{NS}.{eid}.option_{slug}"; loc[key] = label
        return b("option", "name = " + key + "\n" + (b("trigger", trigger) if trigger else "") + display + (b("hidden_effect", effect) if effect else ""))
    def event(eid, title, description, options):
        key = f"{NS}.{eid}"; loc[key + ".t"] = title; loc[key + ".d"] = description
        events.append(b("country_event", f"id = {key} is_triggered_only = yes title = {key}.t desc = {key}.d " + "".join(options)))
    opts = [option(1, kind, "Approve the Field Programme" if kind == "field" else "Approve the Command-Post Programme", f'{f("can_accept")} = yes {kind_test(s)}', preview(kind), f'{f("accept")} = yes') for kind, s in SPECS.items()]
    opts += [option(1, "decline", "Decline the Proposal", f'{f("can_accept")} = yes', effect=f'{f("decline")} = yes'), option(1, "close", "Close the Lapsed Proposal", f'NOT = {{ {f("can_accept")} = yes }}')]
    event(1, "A Korean-American Exercise Proposal", "Seoul proposes combined training to test plans, communications and reinforcement readiness. Washington must decide whether to participate; the programme will proceed only after final authorization from the Korean government.", opts)
    opts = [option(2, kind, "Authorize the Field Exercise" if kind == "field" else "Authorize the Command-Post Exercise", f'{f("can_conduct")} = yes {kind_test(s)}', preview(kind), f'{f("conduct")} = yes') for kind, s in SPECS.items()]
    opts += [option(2, "cancel", "Cancel the Proposed Programme", f'has_country_flag = {f("pending")}', effect=f'{f("cancel")} = yes'), option(2, "close", "Close the Lapsed Proposal", f'NOT = {{ has_country_flag = {f("pending")} }}')]
    event(2, "Washington Approves the Programme", "The United States has accepted the proposed training. Seoul must now authorize the exercise and the agreed commitments of both governments.", opts)
    for kind, s in SPECS.items():
        eid = 3 if kind == "field" else 4
        shown = b("effect_tooltip", b("if", b("limit", "tag = KOR") + f'army_experience = {s["xp"]} add_timed_idea = {{ idea = {idea(kind,"kor_reward")} days = 180 }}') + b("if", b("limit", "tag = USA") + f'army_experience = {s["us_xp"]} add_timed_idea = {{ idea = {idea(kind,"usa_reward")} days = 180 }}'))
        event(eid, "Combined Field Exercise Concluded" if kind == "field" else "Command-Post Exercise Concluded", "The agreed programme has concluded. The participating staffs have recorded their findings and will apply the lessons to operational planning and readiness.", [option(eid, "record", "Record the Training Results", display=shown)])
    for eid, title, desc in (
        (5, "Washington Declines the Exercise", "The American government has declined the proposed programme. The staffs will have to reconsider the conditions for another invitation."),
        (6, "Seoul Cancels the Exercise", "The Korean government has decided not to authorize the proposed programme. The training commitments will not take effect."),
        (9, "Combined Training Interrupted", "Changed security conditions have interrupted the programme. The participating forces must return their attention to current operational responsibilities."),
        (10, "Exercise Proposal Lapsed", "The proposed programme has not secured the required authorization within its response period. The staffs have closed this round of planning.")):
        event(eid, title, desc, [option(eid, "acknowledge", "Acknowledge the Decision")])
    choices = [option(7, kind, "Plan a Combined Field Exercise" if kind == "field" else "Plan a Command-Post Exercise", f'{f("can_invite")} = yes', preview(kind), f'{f("invite_" + kind)} = yes') for kind in SPECS]
    choices.append(option(7, "later", "Defer the Programme"))
    event(7, "The Combined Training Programme", "The two military establishments can prepare either a field exercise or a command-post programme. Seoul’s choice will be sent to Washington before either government commits resources.", choices)
    loc[f("launch_terms_tt")] = "§YUpon Korean authorization — 30 days of training:§!"
    loc[f("completion_terms_tt")] = "§YOn successful completion:§!"
    loc[f("field_weekly_tt")] = "Training upkeep: §R$4 million/week§! for each government."
    loc[f("staff_weekly_tt")] = "Training upkeep: §R$2 million/week§! for each government."
    loc["COLDWAR_KOR_action_open_usfk_exercises_tt"] = "Opens the choice of field or command-post exercises. Washington must approve the programme before Seoul authorizes its launch."
    category = f("category"); loc[category] = "Korean-American Exercises"
    loc[category + "_desc"] = "Combined training tests the alliance’s plans against the demands of reinforcement, command and logistics. Every programme requires an agreed schedule and the commitment of both governments."
    for kind in SPECS:
        key = f("invite_" + kind + "_decision")
        decisions.append(b(key, f'icon = GFX_decision_relation cost = 0 visible = {{ tag = KOR has_country_flag = COLDWAR_KOR_combined_exercises_paid }} available = {{ {f("can_invite")} = yes }} complete_effect = {{ {f("invite_" + kind)} = yes }} ai_will_do = {{ factor = 0 }}'))
        loc[key] = "Propose Combined Field Exercises" if kind == "field" else "Propose Command-Post Exercises"
        loc[key + "_desc"] = ("A field programme would test combat readiness and reinforcement arrangements under demanding conditions. Its benefits depend on coordination with the United States and the resources required to sustain the agreed schedule." if kind == "field" else "A command-post programme would test communications and operational planning without the same field commitment. Both staffs must contribute personnel and resources while reconciling their national chains of command.")
    return {
        "common/scripted_triggers/COLDWAR_KOR_1970_usfk_exercises.txt": HEADER + "".join(triggers),
        "common/scripted_effects/COLDWAR_KOR_1970_usfk_exercises.txt": HEADER + "".join(effects),
        "common/ideas/COLDWAR_KOR_1970_usfk_exercises.txt": HEADER + b("ideas", b("country", "".join(ideas))),
        "events/COLDWAR_KOR_1970_usfk_exercises.txt": HEADER + "\n".join(events),
        "common/decisions/COLDWAR_KOR_1970_usfk_exercises.txt": HEADER + b(category, "".join(decisions)),
        "common/decisions/categories/COLDWAR_KOR_1970_usfk_exercises.txt": HEADER + b(category, "icon = GFX_decision_category_generic_foreign_policy visible = { tag = KOR IMP_is_1970_scenario = yes }"),
    }, loc
