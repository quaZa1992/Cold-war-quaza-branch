# IMPERIA CW — Cold War: Soviet Union 1970 content generator.
# COLDWAR | Readable names for the flags and variables of the Soviet Union and the Union Plan (Enes, 18.10.2026:
# "bitte localisation überall gefixed haben"). HOI4 prints a flag or variable in a tooltip by its localisation key if one
# exists, otherwise by its raw name ("Not: COLDWAR_SOV_gensec_ust"). Two layers:
#  1. cw_avail and the decision/mission code wrap visible conditions in custom_trigger_tooltip with a full sentence (TT helpers here);
#  2. add_name_loc() gives every COLDWAR flag and variable that appears anywhere in the generated code a localisation key, so nothing
#     can ever show up raw (effects of scripted effects, conditions inside scripted triggers, the debug view).
import re
from cw_common import *
import cw_effects as E

OPWORD = {"≥": "at least", "≤": "at most", ">": "above", "<": "below"}
FACTION_EN = {"communist_cadres": "the Nomenklatura (Communist Cadres)", "labour_unions": "the Trade Unions",
              "intelligence_community": "the KGB (Intelligence Community)", "the_military": "the Army",
              "defense_industry": "the Defence Industry", "industrial_conglomerates": "the Branch Ministries (Industrial Conglomerates)",
              "fossil_fuel_industry": "the Fossil Fuel Industry", "the_clergy": "the Clergy", "oligarchs": "the Oligarchs"}
GOV_EN = {"communism": "Emerging", "democratic": "Western", "neutrality": "Non-Aligned", "nationalist": "Nationalist", "fascism": "Fascist"}


def gs(k):
    return E.GENSEC[k][0] if k in E.GENSEC else {"aliyev": "Heydar Aliyev", "grishin": "Viktor Grishin"}.get(k, k)


def keypart(s):
    """a value as a loc-key fragment: -0.3 -> m0p3"""
    return str(s).replace("-", "m").replace("−", "m").replace(".", "p").replace(",", "p").replace("+", "")


def ctt(key, text, body):
    """custom_trigger_tooltip on one line with its own loc key"""
    k = f"{PFX}tt_{key}"
    LOC[k] = text
    return f"custom_trigger_tooltip = {{ tooltip = {k} {body} }}"


# ---------------------------------------------------------------- flags
FLAG_TEXT = {
    # Soviet system
    "accused": "Accused in a kompromat dossier", "ai_proposal_cooldown": "Has recently made a proposal (AI)",
    "applications_open": "Applications for the Politburo are open", "applied": "Has applied for a seat in the Politburo",
    "aral_disaster": "The Aral Sea is dying", "bam_open": "The Baikal-Amur Mainline is open to traffic",
    "berlin_agreement": "The Berlin Agreement has been signed", "bid_100": "Applied with a gift of 100 political power",
    "bid_25": "Applied with a gift of 25 political power", "bid_50": "Applied with a gift of 50 political power",
    "bre_retiring": "Brezhnev is about to retire", "cadre_protection": "Its cadres are protected from investigation",
    "comecon_refunded": "The Comecon programme refund has been paid", "comprehensive_programme": "The Comprehensive Programme of Comecon is adopted",
    "congress_open": "A Party Congress is in session", "current_proposer": "Its proposal is before the Politburo",
    "discipline_campaign": "Andropov's discipline campaign is running", "disintegration_cooldown": "The Union's crisis has struck recently",
    "extra_session": "An extra session of the Politburo has been called", "federal_union": "A Federal Union: republican votes count double on Union questions",
    "federation_council": "The Federation Council has replaced the republican seats", "free_appointment": "A seat may be filled without a plenum",
    "free_dismissal": "A republican member may be purged without a plenum", "garrison_host": "Hosts a Soviet garrison",
    "grain_bought": "Grain has been bought abroad this year", "grain_importer": "The Soviet Union imports grain",
    "harvest_cooldown": "A harvest has recently failed", "in_vote": "Votes in the running Politburo vote",
    "initialized": "The Soviet Union of 1970 is set up", "iron_discipline": "Romanov's iron discipline",
    "kompromat_pending": "Moscow is examining a kompromat dossier", "kompromat_proven": "The accusations were confirmed",
    "kremlin_doctors": "The Kremlin doctors keep Brezhnev alive", "last_abstain": "Abstained in the last vote",
    "last_no": "Voted against in the last vote", "last_passed": "The last vote passed", "last_proposer": "Made the last proposal",
    "last_seat": "Changed its seat most recently", "last_yes": "Voted in favour in the last vote",
    "local_barons": "Brezhnev trusts the local barons", "market_reform": "The Kosygin reform has been deepened",
    "ninth_plan": "The Ninth Five-Year Plan has been adopted", "ogas": "OGAS: cybernetic planning",
    "patron_cooldown": "Has made a proposal through its patron this year", "pipelines_to_europe_signed": "The pipelines to Europe are agreed",
    "plan_priority_chosen": "The priority of the Five-Year Plan is set", "politburo_system": "The Politburo of the Republics is active",
    "poor_harvest": "The harvest has failed this year", "power_transferred": "Power has passed to another party",
    "pripiski": "Has falsified its plan report (pripiski)", "proposal_locked": "An earlier proposal is still open",
    "proposal_made": "Has made a proposal in this session", "proposal_rejected": "Moscow has rejected its proposal",
    "rbmk": "The RBMK reactors are being built", "rotate_cadres": "The cadres are being rotated",
    "seat": "Has a seat in the Politburo", "seat_changed_this_congress": "A seat has changed hands at this congress",
    "slavic_core_signed": "The Slavic core treaty is signed", "soyuz_pipeline_signed": "The Soyuz pipeline is agreed",
    "treaty_signer": "The treaty signer", "vote_passed": "The vote has passed", "vote_pending": "Has not voted yet",
    "vote_running": "A Politburo vote is running", "voted_abstain": "Has abstained", "voted_no": "Has voted against",
    "voted_yes": "Has voted in favour",
    # the Union Plan
    "banner_holder": "Holds the Transferable Red Banner", "cadre_target": "Moscow wants to replace its First Secretary",
    "cheap_directives": "Gosplan Directives: directives cost 15 political power", "counter_unlocked": "The Counter-Plan is available",
    "d_ai_done": "The directive is fulfilled (AI)", "d_delivered": "The special consignment has been delivered",
    "d_komsomol": "The Komsomol brigades have been sent", "d_reported": "Has reported the directive fulfilled",
    "dir_pending": "A directive is being drafted", "directive_active": "A directive of Moscow is running",
    "emulation": "Socialist Emulation is adopted", "exposed": "Its false plan report has been exposed",
    "fail_directive": "Has failed Moscow's directive", "fail_exposed": "Its false plan report was exposed",
    "fail_target": "Has failed its annual plan target", "last_cadre": "The last cadre question concerned it",
    "last_fail": "Failed its annual target last year", "last_ok": "Fulfilled its annual target last year",
    "last_shortfall": "Plan Shortfall last year", "last_won": "The Union plan was fulfilled last year",
    "left_union": "Has left the Union plan", "moscows_man": "Its First Secretary is Moscow's Man",
    "pardon_cd": "Has pardoned a republic this year", "party_control": "The Party Control Commission is set up",
    "peoples_control": "The People's Control audits the plan reports", "rearm_15": "The plan year still allows a later deadline",
    "rearm_30": "The plan year still allows a later deadline (30 days)", "rearm_45": "The plan year still allows a later deadline (45 days)",
    "reported_false": "Has reported a fulfilment it did not achieve", "requisitioned": "Its capacity is requisitioned",
    "reserves": "Keeps reserves in hand", "storming_unlocked": "Storm the Plan is available", "system": "The Union plan is running",
    "t_ai_done": "The annual target is fulfilled (AI)", "t_delivered": "Has delivered to the Union fund",
    "t_rearmed": "The tolkachi have already moved the deadline", "t_reported": "Has reported the annual target fulfilled",
    "t_stormed": "Has stormed the plan", "t_tolkachi": "The tolkachi have been sent", "target_active": "An annual plan target is running",
    "target_failed": "Has failed its annual plan target", "target_fulfilled": "Has fulfilled its annual plan target",
    "tolkachi_unlocked": "Send the Tolkachi is available", "tree_started": "The Union Plan is adopted",
    "year_running": "A plan year is running", "year_won": "This year's Union plan is fulfilled",
}
CAT_EN = {"politburo_category": "The Politburo", "five_year_plan_category": "Five-Year Plans", "union_category": "The Union of Republics",
          "grain_import_decisions": "Grain Imports"}


def flag_text(flag):
    short_ = re.sub(r"^COLDWAR_(?:SOV|UNI)_", "", flag)
    if short_ in FLAG_TEXT:
        return FLAG_TEXT[short_]
    m = re.match(r"^(gensec|candidate|heir|dead|plenum_failed)_(\w+)$", short_)
    if m:
        who = gs(m.group(2))
        return {"gensec": f"{who} is General Secretary", "candidate": f"{who} is a candidate for General Secretary",
                "heir": f"{who} is the designated heir", "dead": f"{who} has died",
                "plenum_failed": f"The Plenum has recently rejected {who}"}[m.group(1)]
    m = re.match(r"^direction_under_(\w+)$", short_)
    if m:
        return f"A direction has been chosen under the {GOV_EN.get(m.group(1), m.group(1))} government"
    m = re.match(r"^(\w+)_unlocked$", short_)
    if m and m.group(1) in CAT_EN:
        return f"Decisions unlocked: §Y{CAT_EN[m.group(1)]}§!"
    m = re.match(r"^(\w+)_in_progress$", short_)
    if m:
        return f"{LOC.get(PFX[:-4] + 'UNI_' + m.group(1)) or m.group(1).replace('_', ' ').title()} is being researched"
    m = re.match(r"^directives_(\d+)$", short_)
    if m:
        return f"The directives of the {['Ninth', 'Tenth', 'Eleventh', 'Twelfth'][int(m.group(1)) - 9]} Plan are adopted"
    return short_.replace("_", " ").capitalize()


# ---------------------------------------------------------------- variables
VAR_TEXT = {
    "union_cohesion": "Union Cohesion", "bop": "Politburo Balance (reformers -1, orthodox +1)", "plan": "Five-Year Plan",
    "seat_count": "Republican Seats Taken", "session_half": "Politburo Session Calendar", "congress": "Party Congress",
    "vote_type": "Type of the Running Vote", "vote_lean": "Lean of the Moscow Members", "vote_subject": "Subject of the Vote",
    "vote_union": "Union Question", "vote_yes": "Votes in Favour", "vote_no": "Votes Against", "vote_total": "Votes Cast",
    "vote_moscow": "Moscow Votes in Favour", "vote_rep_yes": "Republican Votes in Favour", "vote_rep_total": "Republican Votes", "vote_rep_cast": "Republican Votes Cast",
    "vote_succession": "Succession Vote", "vote_proposer": "Proposer", "last_type": "Type of the Last Vote", "last_subject": "Subject of the Last Vote",
    "last_succession": "Last Vote Was a Succession", "last_proposer": "Last Proposer", "res_queue": "Resolutions Waiting for a Vote",
    "accused_id": "Accused Republic", "accuser_id": "Accusing Republic", "bid": "Bid for a Seat", "disgrace_left": "Congresses in Disgrace",
    "prop_type": "Type of Proposal", "prop_building": "Proposed Building", "prop_benef": "Beneficiary of the Proposal",
    "pripiski_plan": "Plan of the Last False Report", "russification_count": "Russian Language Campaigns",
    "republic_burden": "Union Projects Weighing on the Budget", "last_transfer": "Last Transfer", "berlin_signatures": "Signatures (Berlin)",
    "helsinki_signatures": "Signatures (Helsinki)", "keep_alignment": "Kept Bloc Alignment",
    # the Union Plan
    "fulfilled": "Republics That Fulfilled the Plan", "needed": "Republics Needed", "members": "Republics in the Union Plan",
    "prio": "Moscow's Plan Priority", "prio_key": "Moscow's Priority Mission", "year": "Plan Year", "year_plan": "Five-Year Plan of the Plan Year",
    "last_year": "Last Plan Year", "last_fulfilled": "Fulfilled Last Year", "last_needed": "Needed Last Year", "last_members": "Republics Last Year",
    "sf_pts": "Shortfall Points", "sf_total": "Shortfall Points of the Union", "sf_void": "Shortfall Points Already Settled",
    "sf_pct": "Shortfall (Construction and Political Power, %)", "cg_pct": "Shortfall (Consumer Goods Tax, %)",
    "sf_build": "Shortfall: Construction Speed", "sf_pp": "Shortfall: Political Power Gain", "sf_cg": "Shortfall: Consumer Goods Tax",
    "dl_pts": "Delivery Points", "dl_total": "Delivery Points of the Union", "dl_build": "Deliveries: Construction Speed",
    "dl_pp": "Deliveries: Political Power Gain", "req_n": "Requisitioned Civilian Factories", "req_sum": "Requisitioned Civilian Factories (Union)",
    "req_cfu": "Freed Civilian Factories", "replaced": "First Secretaries Replaced by Moscow", "cadre_target": "Target of the Cadre Question",
    "dir_count": "Directives in This Plan", "dir_plan": "Plan of the Last Directive", "fp_plan": "Plan of the Fulfilled Targets",
    "fulfilled_plan": "Annual Targets Fulfilled in This Plan", "u_days": "Days of the Union Mission",
    "t_key": "Annual Target", "t_tier": "Reward Tier of the Annual Target", "t_days": "Days for the Annual Target",
    "t_b1": "Annual Target: Starting Value", "t_b2": "Annual Target: Starting Value (Nuclear)", "t_b3": "Annual Target: Starting Value (Renewable)",
    "t_infra": "Annual Target: Infrastructure at the Start", "d_key": "Directive", "d_tier": "Reward Tier of the Directive",
    "d_days": "Days for the Directive", "d_b1": "Directive: Starting Value", "d_b2": "Directive: Starting Value (Nuclear)",
    "d_b3": "Directive: Starting Value (Renewable)", "d_infra": "Directive: Infrastructure at the Start",
}
for _n in (9, 10, 11, 12):
    VAR_TEXT[f"good_years_{_n}"] = f"Fulfilled Years of the {['Ninth', 'Tenth', 'Eleventh', 'Twelfth'][_n - 9]} Plan"


def var_text(var):
    short_ = re.sub(r"^(?:global\.)?COLDWAR_(?:SOV|UNI)_", "", var)
    if short_ in VAR_TEXT:
        return VAR_TEXT[short_]
    # dynamic modifier lines: <group>_<modifier>, <key>_programme_<modifier>
    for mod in sorted(MOD_EN, key=len, reverse=True):
        if short_.endswith("_" + mod):
            group = short_[: -len(mod) - 1]
            gname = LOC.get(f"{PFX}{group}_modifier") or LOC.get(f"{PFX}{group}") or group.replace("_", " ").title()
            return f"{MOD_EN[mod]} ({gname})"
    return short_.replace("_", " ").title()


# ---------------------------------------------------------------- loc for every name in the generated code
FLAG_RE = re.compile(r"(?:has|set|clr)_(?:country|global|state)_flag = (?:\{ flag = )?(COLDWAR_(?:SOV|UNI)_\w+)")
VAR_RE = re.compile(r"(?:check_variable = \{|set_variable = \{|add_to_variable = \{|subtract_from_variable = \{|multiply_variable = \{|"
                    r"divide_variable = \{|clamp_variable = \{ var =|round_variable =|has_variable =|var:)\s*(?:global\.)?(COLDWAR_(?:SOV|UNI)_\w+)")
TEMP_RE = re.compile(r"(?:set_temp_variable|add_to_temp_variable|multiply_temp_variable|subtract_from_temp_variable|set_temp_variable_to_random|"
                     r"clamp_temp_variable|round_temp_variable|divide_temp_variable) = \{?\s*(?:var = )?(COLDWAR_(?:SOV|UNI)_\w+)")
ADDED = {}


def add_name_loc(texts):
    """texts: the generated script files (not the localisation). Adds a loc key for every COLDWAR flag and variable without one."""
    code = "\n".join(texts)
    temps = set(TEMP_RE.findall(code))
    flags = set(FLAG_RE.findall(code))
    vars_ = set(VAR_RE.findall(code)) - temps
    for f in sorted(flags):
        if f not in LOC:
            LOC[f] = ADDED[f] = flag_text(f)
    for v in sorted(vars_):
        if v not in LOC:
            LOC[v] = ADDED[v] = var_text(v)
    return ADDED
