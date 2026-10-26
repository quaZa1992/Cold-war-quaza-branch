# IMPERIA CW — Cold War: iraq 1970 — audit rewards.
"""Approved 19 October 2026 Iraqi reward revision; pure data transformation.

The immutable approved_iraq.json remains the pre-revision/save-contract source.
``apply`` changes a caller-owned copy, never files or prerequisite geometry.
Root integration consumes RETIRED and the per-node audit_delivery_components;
see AUDIT_REWARDS.md before generating executable upgrade transactions.
"""
from __future__ import annotations

from copy import deepcopy
import re

P = "COLDWAR_IRQ_"
REVISION = "2026_10_19_v1"

def fid(key):
    return P + key

# Retirement targets are stable identifiers, not permission to replay the
# target's rewards or to turn a historical inspection into a delivered factory.
RETIRED = {fid(a): fid(b) for a, b in {
    "defence_accounts": "defence_staff_training",
    "society_literacy_accounts": "society_baseline",
    "industry_survey": "industry_heavy",
    "industry_quality": "industry_maintenance",
    "oil_operators": "oil_baiji",
    "industry_steel": "industry_heavy",
    "industry_consumers": "industry_light",
    "oil_export_terminals": "oil_revenue_state",
    "oil_industrial_fund": "oil_diversification",
    "industry_delivery_review": "industry_tax_service",
    "society_service_compact": "society_baseline",
    "agri_cooperative_credit": "agri_cooperatives",
    "agri_smallholder_credit": "agri_smallholders",
    "agri_wasit": "agri_cooperatives",
}.items()}

# A branch-neutral administrative predecessor cannot be replaced by a new
# mandatory Heavy or Mass-Literacy gate. Structural integration must expand it.
REPLACEMENT_CANDIDATES = {
    fid("industry_survey"): [fid("industry_heavy"), fid("industry_light")],
    fid("society_literacy_accounts"): [fid("society_mass_literacy"), fid("society_teacher_first")],
    fid("defence_accounts"): [fid("defence_professional"), fid("defence_mass")],
}

# Retirement sources attached to each surviving delivery contract.
MERGED_SOURCES = {
    fid("industry_heavy"): [fid("industry_steel")],
    fid("industry_light"): [fid("industry_consumers")],
    fid("oil_revenue_state"): [fid("oil_export_terminals")],
    fid("oil_diversification"): [fid("oil_industrial_fund")],
    fid("industry_maintenance"): [fid("industry_quality")],
    fid("oil_baiji"): [fid("oil_operators")],
    fid("agri_cooperatives"): [fid("agri_cooperative_credit"), fid("agri_wasit")],
    fid("agri_smallholders"): [fid("agri_smallholder_credit")],
}

DESCRIPTIONS = {
    fid("defence_soviet_standard"): "Much of Iraq's military experience has been built around Soviet equipment and instruction. Concentrating stores, maintenance and training on a common standard will reduce the burden of supply, while leaving the army more exposed to decisions made by its principal foreign partner.",
    fid("defence_mixed_supply"): "Iraq can seek capabilities that a single military supplier does not provide. Training specialists to absorb a wider range of aircraft will broaden the army's supporting knowledge, though different systems require more complicated stores and maintenance. Any foreign advisory mission must still be agreed with its government.",
    fid("courts_budget"): "A functioning court needs records, trained clerks and the means to enforce its decisions. Funding those foundations will make commercial obligations and public collection more dependable, while placing a defined responsibility on the civil administration.",
    fid("budget_accounts"): "Ministries cannot administer the same income through competing sets of books. A common public account will make revenue easier to collect and reduce the cost of reconciling overlapping offices, without requiring every province to surrender its daily work to Baghdad.",
    fid("agri_cooperatives"): "The cost of machinery and reliable credit lies beyond many individual cultivators. Cooperative organisation can pool that capacity, supported by agricultural investment in Wasit, but the state must maintain the administration needed to keep shared equipment and finance working.",
    fid("agri_smallholders"): "Rural development also depends on cultivators who can make decisions on their own holdings. Affordable credit and a stronger market for their produce will improve small farms and ease household pressures, while committing the government to support that dispersed network.",
    fid("oil_concession_delivery"): "An agreed concession must bring practical improvements to the industry as well as a signed document. Development around Basra and engineering instruction will give Iraq earlier operating benefits from the partnership, while foreign participation remains part of the settlement.",
    fid("industry_heavy"): "Iraq needs more than imported finished goods if its development plans are to survive a foreign supply crisis. Basic industries around Baghdad will give workshops and military producers a stronger domestic foundation, though directing capital toward heavy plant leaves fewer resources for everyday consumption.",
    fid("industry_light"): "Mosul and the northern provinces need employment as well as goods from the capital. Expanding consumer production will supply domestic markets and strengthen the civilian economy, with public agencies responsible for coordinating land, credit and new workshops.",
    fid("industry_maintenance"): "Machinery bought abroad is only useful while Iraqi workshops can keep it running. Maintenance teams and common inspection standards will reduce stoppages and improve production discipline, even where stricter quality requirements slow the final assembly line.",
    fid("industry_machine_tools"): "Machine tools are the foundation of an industry able to reproduce its own skills. Iraqi technicians must learn to adapt equipment and organise production, rather than depend on a foreign specialist whenever a workshop changes its product.",
    fid("oil_technical_training"): "Control over the oil industry must be matched by the ability to operate it. Training Iraqi engineers will build the technical knowledge needed to maintain installations and develop the country's refining capacity under the ownership settlement we have actually established.",
    fid("oil_baiji"): "Baiji can turn more of Iraq's crude into useful fuel if its refinery is supported by trained operators and reliable maintenance. Combining plant development with practical instruction will strengthen fuel supplies, while adding to the responsibilities of the state oil administration.",
    fid("oil_revenue_state"): "Basra's export installations connect Iraq's oilfields to the revenues on which the state increasingly depends. Expanding that outlet can finance public commitments quickly, but a government built around oil receipts has less incentive to develop a broader tax base.",
    fid("oil_diversification"): "Oil receipts can purchase the foundations of an economy that outlasts an export boom. Directing part of that income into civilian production around Baghdad will support further construction, at the cost of some immediate returns from the oil sector.",
    fid("defence_professional"): "A reliable army begins with trained officers, experienced specialists and formations that can execute orders under pressure. A professional core will cost more to maintain, but it offers a more dependable instrument than paper strength alone.",
    fid("defence_mass"): "A prolonged war cannot be sustained by the standing formations alone. Organising a national reserve will deepen the pool of replacements and improve the army's ability to recover, although bringing a much larger body of men under arms complicates unit cohesion.",
    fid("defence_staff_training"): "Iraqi officers need practice in coordinating whole formations, not merely commanding their own battalions. Staff exercises and doctrine instruction will develop that experience, while more demanding preparation lengthens the training of the forces they lead.",
    fid("defence_air_maintenance"): "An aircraft grounded for want of a trained mechanic contributes nothing to national defence. Our air establishments must develop the technical instruction and practical maintenance skills needed to keep their equipment serviceable and understand the next generation of aircraft.",
    fid("defence_readiness"): "Readiness must be sustained between crises. A regular cycle of exercises will test mobilisation and formation cohesion without confusing a brief demonstration with a permanently prepared army.",
    fid("saddam_guard"): "A presidential guard offers the leadership formations whose readiness and loyalty can be cultivated closely. Privileged training and dependable support are expensive, but they can strengthen the regime's military position when ordinary institutions are under strain.",
    fid("saddam_regular_army"): "Iraq's military strength cannot rest on privileged formations alone. Investing in the regular army's training and replacement system will give its commanders forces that recover more readily and bring new soldiers into service faster, while increasing the permanent payroll.",
    fid("society_mass_literacy"): "Too many Iraqis have been excluded from schooling by poverty, distance and the demands of working life. A broad literacy campaign will take basic instruction to adults now, placing new obligations on teachers and the public services that support them.",
    fid("society_teacher_first"): "A school programme cannot grow indefinitely on a shortage of trained teachers. Building the teaching profession first will support deeper technical learning and more capable institutions, even if the earliest gains in basic literacy arrive more slowly.",
    fid("society_technical_colleges"): "New plants, construction sites and public utilities need Iraqi technicians able to solve practical problems. Technical colleges will connect classroom instruction to those needs, giving development projects a stronger local base while committing the state to sustained educational support.",
    fid("national_front"): "A national front can draw specialists and organised constituencies into public life without pretending that their interests are identical. Giving that cooperation a practical economic purpose will broaden the state’s expertise, while requiring the party to administer real arrangements with its partners.",
    fid("baath_monopoly"): "The party can choose to reserve the commanding positions of the state for its own organisation. Concentrated authority will make it easier to enforce a common political line, at the cost of excluding some of the independent knowledge on which development also depends.",
    fid("state_compact"): "Rules written in Baghdad must become routines that ministries and provincial offices can actually follow. A workable settlement between public authority and administration will make revenue more dependable and reduce the expense of governing through overlapping responsibilities.",
    fid("baath_future"): "The party's claim to lead Iraq must be supported by institutions capable of carrying development beyond a single campaign. Renewing technical instruction within its governing apparatus will strengthen its capacity to turn political decisions into industrial work.",
    fid("bakr_succession_plan"): "The presidency should pass through an agreement that the institutions of the republic can recognise. Al-Bakr must settle the authority of an eligible successor with those whose cooperation will determine whether the transfer endures.",
    fid("icp_socialist_republic"): "A socialist government must make public industry answer to the people whose work sustains it. Giving the industrial programme a durable place in the republic will support production, while binding the state to the social commitments that justify its authority.",
    fid("aziz_party_renewal"): "A party that emerged through clandestine organisation cannot govern indefinitely through habits formed in hiding. Aziz Muhammad must renew its leadership and accounts together, allowing experienced organisers to become an administration that can answer for public money.",
    fid("civic_mandate"): "Civilian government needs a revenue system that survives a change of cabinet. Bringing collection and public accounts under predictable procedures will give elected institutions the means to govern without recreating a patronage office at every political turn.",
    fid("royal_settlement"): "A constitutional crown can only endure if the institutions around it carry the daily work of government. A settled charter will give Iraq a clearer voice abroad, while maintaining the public offices needed to give those commitments substance.",
    fid("kdp_common_republic"): "A common republic must make room for the northern settlement we have chosen. Local policing and recognised responsibilities can reduce the burden of constant military supervision, while creating administrative work that Baghdad and the provinces must sustain together.",
    fid("puk_federal_mandate"): "The PUK's claim to represent a broader northern society must be carried into workplaces and public services. Turning that mandate into practical organisation will improve productive cooperation, while committing the government to social provision beyond its established supporters.",
    fid("dawa_government_review"): "Dawa's networks can carry a message farther than they can run a ministry. The cabinet must give education and professional instruction an institutional footing if a religious mandate is to become a capable administration, with the lasting public obligations that follow.",
    fid("sciri_iraqi_mandate"): "A government cannot leave armed authority divided indefinitely between ministries and the formations that brought it to power. Establishing a common command will improve cohesion, but recognised personnel and their responsibilities must be carried on the public payroll.",
    fid("iip_government_mandate"): "The Iraqi Islamic Party must turn its social and commercial associations into a programme of government. Clearer cooperation with workshops and employers will help production adapt, although the concessions that secure their participation reduce the state's immediate tax return.",
}

BONUS_LOCALISATION = {}

def tech(key, category, bonus, uses=1):
    name = fid(key) + "_research_" + category.removeprefix("CAT_")
    BONUS_LOCALISATION[name] = {
        "CAT_industry": "Iraqi Industrial Instruction",
        "CAT_construction": "Iraqi Construction Engineering",
        "CAT_aircraft": "Iraqi Aircraft Maintenance",
        "CAT_fuel_refining": "Iraqi Oil Engineering",
    }[category]
    return f"add_tech_bonus = {{ name = {name} bonus = {bonus:g} uses = {uses} category = {category} }}"


def _set(n, *, modifiers=None, days=None, share=None, building=..., xp=None, instant=None):
    if modifiers is not None:
        n["modifiers"] = dict(modifiers)
    if days is not None:
        n["days"] = days
        n["cost"] = days / 7
    if share is not None:
        n["budget_gdp_share"] = share
    if building is not ...:
        n["building"] = deepcopy(building)
    if xp is not None:
        n["army_xp"] = xp
    if instant is not None:
        n["instant"] = list(instant)


def _literacy(n):
    for row in n.get("instant", []):
        match = re.fullmatch(r"set_temp_variable\s*=\s*\{\s*LR_change\s*=\s*([0-9.]+)\s*\}", row)
        if match:
            return float(match.group(1))
    return 0


def _components(n, originals):
    """Declare one-time delivery atoms; integration, not previews, guards these.

    legacy_amounts are partial credits, not Boolean 'already done' markers.
    E.g. old Staff Training delivered15XP, so its35XP replacement owes20XP.
    Old Mass Literacy delivered.025, so its.06replacement owes.035.
    """
    sources = [n["id"]] + MERGED_SOURCES.get(n["id"], [])
    rows = []
    def add(kind, suffix, payload, amounts=None):
        row = {"kind": kind, "receipt": fid("audit_reward_") + n["key"] + "_" + suffix,
               "legacy_sources": list(sources), **payload}
        if amounts is not None:
            row["legacy_amounts"] = amounts
        rows.append(row)
    if n.get("building"):
        add("building", "building", {"building": deepcopy(n["building"])},
            {s: originals[s]["building"][2] for s in sources
             if originals[s].get("building") and originals[s]["building"][:2] == n["building"][:2]})
    if n.get("army_xp"):
        add("army_xp", "army_xp", {"amount": n["army_xp"]},
            {s: originals[s]["army_xp"] for s in sources if originals[s].get("army_xp")})
    literacy = _literacy(n)
    if literacy:
        add("literacy", "literacy", {"amount": literacy, "instant": list(n["instant"])},
            {s: _literacy(originals[s]) for s in sources if _literacy(originals[s])})
    else:
        for i, effect in enumerate(n.get("instant", [])):
            # New research and air XP are absent from all old Iraqi packages;
            # exact matching gives a safe native-atom credit for any future use.
            add("instant", "instant_" + str(i), {"instant": [effect]},
                {s: 1 for s in sources if effect in originals[s].get("instant", [])})
    return rows


def apply(data):
    """Mutate caller-owned data once. Keep all graph edits in root integration.

    Returns the same object for composition. The original frozen catalogue is
    never opened or rewritten here. Inputs are expected to be a deepcopy of it.
    """
    if data.get("audit_rewards_revision") == REVISION:
        return data
    nodes = {n["id"]: n for n in data["nodes"]}
    originals = deepcopy(nodes)
    touched = set()
    def change(key, **kwargs):
        n = nodes[fid(key)]
        _set(n, **kwargs)
        touched.add(n["id"])
        return n

    # Six approved policy choices, using the final conservative army values.
    change("industry_heavy", modifiers={"production_factory_max_efficiency_factor": .10, "industrial_capacity_factory": .05, "consumer_goods_factor": .02}, days=49, share=.05, building=[557, "industrial_complex", 1], instant=[tech("industry_heavy", "CAT_industry", .35)])
    change("industry_light", modifiers={"production_speed_buildings_factor": .08, "bureaucracy_cost_multiplier_modifier": .02}, days=49, share=.04, building=[166, "industrial_complex", 1])
    change("defence_professional", modifiers={"army_org_factor": .08, "army_personnel_cost_multiplier_modifier": .06}, days=35, share=.01, xp=25)
    change("defence_mass", modifiers={"conscription_factor": .15, "army_morale_factor": .08, "army_org_factor": -.03}, days=35, share=.01, xp=25)
    change("saddam_guard", modifiers={"army_org_factor": .03, "army_defence_factor": .04, "army_personnel_cost_multiplier_modifier": .10}, days=35, share=.02)
    change("saddam_regular_army", modifiers={"army_morale_factor": .06, "training_time_army_factor": -.08, "army_personnel_cost_multiplier_modifier": .04}, days=35, share=.02)
    change("society_mass_literacy", modifiers={"social_cost_multiplier_modifier": .03}, days=35, share=.025, instant=["set_temp_variable = { LR_change = 0.06 }", "update_literacy_rate = yes"])
    change("society_teacher_first", modifiers={"research_speed_factor": .05, "social_cost_multiplier_modifier": .03}, days=35, share=.025, instant=[tech("society_teacher_first", "CAT_industry", .25)])
    change("oil_revenue_state", modifiers={"oil_export_multiplier_modifier": .18, "tax_gain_multiplier_modifier": -.03}, days=49, share=.035, building=[171, "infrastructure", 1])
    change("oil_diversification", modifiers={"production_speed_buildings_factor": .08, "oil_export_multiplier_modifier": -.03}, days=49, share=.04, building=[557, "industrial_complex", 1])
    change("national_front", modifiers={"production_factory_efficiency_gain_factor": .10, "research_speed_factor": .04, "bureaucracy_cost_multiplier_modifier": .03}, days=35, share=.01)
    change("baath_monopoly", modifiers={"political_power_factor": .15, "drift_defence_factor": .15, "research_speed_factor": -.03}, days=35, share=0)

    # Native limited-use research and experience, rather than generic research.
    change("industry_machine_tools", modifiers={"production_factory_max_efficiency_factor": .03}, instant=[tech("industry_machine_tools", "CAT_industry", .35, 2)])
    change("society_technical_colleges", modifiers={"social_cost_multiplier_modifier": .03}, instant=[tech("society_technical_colleges", "CAT_construction", .50), tech("society_technical_colleges", "CAT_industry", .25)])
    change("defence_air_maintenance", modifiers={"bureaucracy_cost_multiplier_modifier": .02}, instant=[tech("defence_air_maintenance", "CAT_aircraft", .35), "air_experience = 15"])
    doctrine = fid("defence_staff_training_doctrine")
    BONUS_LOCALISATION[doctrine] = "Iraqi General Staff Instruction"
    change("defence_staff_training", modifiers={"training_time_army_factor": .04}, xp=35,
           instant=[f"add_doctrine_cost_reduction = {{ name = {doctrine} category = land_doctrine uses = 1 cost_reduction = 0.25 }}"])
    # The absorbed defence_accounts never adds a second20XP delivery.
    change("defence_readiness", xp=25)

    # Combined production/maintenance and oil engineering milestones.
    change("industry_maintenance", modifiers={"production_factory_efficiency_gain_factor": .08, "production_factory_max_efficiency_factor": .02, "industrial_capacity_factory": -.01, "bureaucracy_cost_multiplier_modifier": .02}, days=35, share=.02)
    change("oil_technical_training", modifiers={"production_factory_efficiency_gain_factor": .02}, instant=[tech("oil_technical_training", "CAT_industry", .35)])
    change("oil_baiji", modifiers={"fuel_gain_factor": .06, "bureaucracy_cost_multiplier_modifier": .02, "production_factory_efficiency_gain_factor": .02})

    # Standardisation saves real supply; diversified technical instruction
    # gives a different capability rather than cosmetic factory efficiency.
    # Equipment/adviser delivery remains a separate actual-consent contract.
    change("defence_soviet_standard", modifiers={"supply_consumption_factor": -.10, "foreign_influence_modifier": -.03}, share=.02)
    change("defence_mixed_supply", modifiers={"supply_consumption_factor": .03}, share=.02,
           instant=[tech("defence_mixed_supply", "CAT_aircraft", .35)])

    # The approved rural-credit priorities absorb their credit administration.
    # Wasit's existing district moves into the cooperative programme once;
    # Dhi Qar remains its separately funded, existing irrigation investment.
    district = deepcopy(originals[fid("agri_wasit")]["building"])
    assert district == [1141, "agriculture_district", 1], district
    change("agri_cooperatives", modifiers={"agricolture_productivity_modifier": .12, "bureaucracy_cost_multiplier_modifier": .03}, days=49, share=.04, building=district)
    change("agri_smallholders", modifiers={"agricolture_productivity_modifier": .08, "consumer_goods_factor": -.02, "social_cost_multiplier_modifier": .02}, days=35, share=.025)
    # Existing acceptance pays Iraq's2%GDP fee to the actual ENG counterpart.
    # Do not charge another2%at focus delivery. Actual accepted terms persist.
    change("oil_concession_delivery", building=[171, "infrastructure", 1],
           instant=[tech("oil_concession_delivery", "CAT_industry", .25)])
    change("courts_budget", modifiers={"tax_gain_multiplier_modifier": .05, "bureaucracy_cost_multiplier_modifier": .02}, days=35, share=.015)
    change("budget_accounts", modifiers={"tax_gain_multiplier_modifier": .04, "bureaucracy_cost_multiplier_modifier": -.03}, share=.005)
    nodes[fid("industry_heavy")]["title"] = "Basic Industries First"
    nodes[fid("industry_light")]["title"] = "Consumer Expansion"

    # Meaningful state institutions; starting-situation relief stays untouched.
    change("state_compact", modifiers={"bureaucracy_cost_multiplier_modifier": -.06, "tax_gain_multiplier_modifier": .04})
    change("baath_future", modifiers={"political_power_factor": .03}, instant=[tech("baath_future", "CAT_industry", .25)])
    change("bakr_succession_plan", modifiers={}, days=21)
    change("icp_socialist_republic", modifiers={"industrial_capacity_factory": .05, "social_cost_multiplier_modifier": .03})
    change("aziz_party_renewal", modifiers={"bureaucracy_cost_multiplier_modifier": -.04, "tax_gain_multiplier_modifier": .03}, days=21)
    change("civic_mandate", modifiers={"tax_gain_multiplier_modifier": .06, "bureaucracy_cost_multiplier_modifier": -.03})
    change("royal_settlement", modifiers={"foreign_influence_modifier": .08, "bureaucracy_cost_multiplier_modifier": .02})
    change("kdp_common_republic", modifiers={"army_personnel_cost_multiplier_modifier": -.05, "bureaucracy_cost_multiplier_modifier": .03})
    change("puk_federal_mandate", modifiers={"production_factory_efficiency_gain_factor": .08, "social_cost_multiplier_modifier": .02})
    change("dawa_government_review", modifiers={"research_speed_factor": .04, "social_cost_multiplier_modifier": .03})
    change("sciri_iraqi_mandate", modifiers={"army_org_factor": .03, "army_personnel_cost_multiplier_modifier": .04})
    change("iip_government_mandate", modifiers={"production_factory_efficiency_gain_factor": .06, "tax_gain_multiplier_modifier": -.02})

    # Move existing inspector/policy-revision unlocks earlier. Copying an unlock
    # is harmless; it must not replay any delivery owned by that decision.
    def transfer(source, targets):
        for target in targets:
            n = nodes[fid(target)]
            ids = {d["id"] for d in n["decisions"]}
            n["decisions"].extend(deepcopy(d) for d in originals[fid(source)]["decisions"] if d["id"] not in ids)
            touched.add(n["id"])
    transfer("industry_survey", ["industry_heavy", "industry_light"])
    transfer("industry_delivery_review", ["industry_heavy", "industry_light"])
    transfer("society_service_compact", ["society_baseline"])
    # This module exports decision data; decisions_module's actual native
    # provider and quote replacement remain a separate owned integration.
    readiness = {"budget_gdp_share": .005, "modifiers": {"army_org_factor": .04, "army_morale_factor": .04, "army_personnel_cost_multiplier_modifier": .04}, "days": 90, "cooldown": 180}
    for collection in [data.get("decisions", [])] + [n["decisions"] for n in data["nodes"]]:
        for decision in collection:
            if decision["id"] == fid("decision_defence_readiness_cycle"):
                decision.update(deepcopy(readiness))
                decision["summary"] = "A ninety-day funded readiness cycle improves formation cohesion and recovery. Sustaining the exercises adds to the army payroll."

    # Data contracts for root's migration and transaction code. Components use
    # historical paid receipts only, never focus completion by itself.
    data["audit_retired_rewards"] = {}
    for source, target in RETIRED.items():
        old = originals[source]
        data["audit_retired_rewards"][source] = {
            "target": target, "replacement_candidates": REPLACEMENT_CANDIDATES.get(source, [target]),
            "legacy_implemented_flag": source + "_implemented",
            "legacy_invoice_variable": source + "_invoice",
            "legacy_quoted_flag": source + "_quoted",
            "legacy_budget_gdp_share": old["budget_gdp_share"],
            "legacy_building": deepcopy(old["building"]), "legacy_instant": list(old["instant"]), "legacy_army_xp": old["army_xp"],
            "legacy_decisions": deepcopy(old["decisions"]),
            "completion_is_not_delivery": True, "refund": False,
        }
    for nid in touched:
        n = nodes[nid]
        sources = [nid] + MERGED_SOURCES.get(nid, [])
        n["audit_delivery_components"] = _components(n, originals)
        n["audit_legacy_cost_credits"] = [
            {"source": s, "implemented_flag": s + "_implemented", "quoted_flag": s + "_quoted", "invoice_variable": s + "_invoice", "original_share": originals[s]["budget_gdp_share"]}
            for s in sources if originals[s]["budget_gdp_share"]
        ]
        n["audit_previous_reward"] = {k: deepcopy(originals[nid][k]) for k in ("modifiers", "building", "army_xp", "instant", "budget_gdp_share")}
        n["audit_revision"] = REVISION
        if nid in DESCRIPTIONS:
            n["description"] = DESCRIPTIONS[nid]
        # Old catalogue effect specimens are not executable authoring sources.
        n.pop("effect_body", None)
        n.pop("effect_code", None)
    data["audit_rewards_revision"] = REVISION
    return data
