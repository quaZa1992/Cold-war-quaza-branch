# COLDWAR | Shared helpers for the Egypt 1970 focus tree compiler.
# Marker convention: every new ID, flag, variable, idea, event, loc key and
# file carries "COLDWAR" (analogous to Imperia's "IMP"): COLDWAR_EGY_<name>.
import re

PFX = "COLDWAR_EGY_"
TREE_ID = "COLDWAR_EGY_1970_focus"
NS = "COLDWAR_EGY"  # event namespace


def cid(x):
    """Design id EGY_1970_xxx -> COLDWAR_EGY_xxx."""
    return x.replace("EGY_1970_", PFX)


def slug(s):
    s = s.lower().replace("'", "").replace("’", "")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def num(s):
    """'+0,25' / '−10' / '+1.5' -> float"""
    s = s.replace("−", "-").replace("–", "-").replace(",", ".").replace(" ", "")
    return float(s)


def fmt(v):
    """Clausewitz number formatting."""
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s


# German design label -> (modifier key, mode)  mode: pct (value/100) | flat
LABEL = {
    "Sozialkosten": ("social_cost_multiplier_modifier", "pct"),
    "PP-Faktor": ("political_power_factor", "pct"),
    "PP": ("political_power_factor", "pct"),
    "Forschung": ("research_speed_factor", "pct"),
    "Agrarsteuer": ("agriculture_tax_modifier", "pct"),
    "Agrarproduktivität": ("agricolture_productivity_modifier", "pct"),
    "Produktivitätswachstum": ("productivity_growth_modifier", "pct"),
    "Büroeinkommen": ("office_park_income_tax_modifier", "pct"),
    "Stabilität": ("stability_factor", "pct"),
    "Empfangs-Investitionskosten": ("receiving_investment_cost_modifier", "pct"),
    "Empfangs-Investitionsdauer": ("receiving_investment_duration_modifier", "pct"),
    "ROI": ("return_on_investment_modifier", "flat"),
    "Zinsen": ("interest_rate_multiplier_modifier", "pct"),
    "Ausbildungszeit": ("training_time_factor", "pct"),
    "Ausbildung": ("training_time_factor", "pct"),
    "Baugeschw.": ("production_speed_buildings_factor", "pct"),
    "Baugeschwindigkeit": ("production_speed_buildings_factor", "pct"),
    "Ressourcenexport": ("resource_export_multiplier_modifier", "pct"),
    "Organisation": ("army_org_factor", "pct"),
    "Inflationskosten": ("inflation_cost_multiplier_modifier", "pct"),
    "Einflussabwehr": ("foreign_influence_defense_modifier", "pct"),
    "Bürokratiekosten": ("bureaucracy_cost_multiplier_modifier", "pct"),
    "Verteidigung": ("army_defence_factor", "pct"),
    "Zivilindustrie-Steuer": ("civilian_industry_tax_modifier", "pct"),
    "Polizeikosten": ("police_cost_multiplier_modifier", "pct"),
    "Fabrik-Effizienzzuwachs": ("production_factory_efficiency_gain_factor", "pct"),
    "Effizienzzuwachs": ("production_factory_efficiency_gain_factor", "pct"),
    "Arbeitskräfte": ("total_workforce_modifier", "pct"),
    "Angriff": ("army_attack_factor", "pct"),
    "Steuereinnahmen": ("tax_gain_multiplier_modifier", "pct"),
    "ideol. Abwehr": ("mdcw_cw_ideological_defence", "pct"),
    "ideologische Abwehr": ("mdcw_cw_ideological_defence", "pct"),
    "Handelsmeinung": ("trade_opinion_factor", "pct"),
    "Militärindustrie-Steuer": ("military_industry_tax_modifier", "pct"),
    "Erfahrung": ("experience_gain_army", "pct"),
    "Moral": ("army_morale_factor", "pct"),
    "Konsumgüter": ("consumer_goods_factor", "pct"),
    "Gesundheitskosten": ("health_cost_multiplier_modifier", "pct"),
    "Ölexport": ("oil_export_multiplier_modifier", "pct"),
    "Durchbruch": ("breakthrough_factor", "pct"),
    "max. Planung": ("max_planning_factor", "pct"),
    "Planungsgeschwindigkeit": ("planning_speed", "pct"),
    "Planungsgeschw.": ("planning_speed", "pct"),
    "Globalism": ("globalism_equilibrium", "flat"),
    "Globalism-Gleichgewicht": ("globalism_equilibrium", "flat"),
    "Kaufpreise auf dem Waffenmarkt": ("international_market_purchase_modifier", "pct"),
    "Kaufpreise": ("international_market_purchase_modifier", "pct"),
    "Ausrüstungskauf bei USA": ("international_market_purchase_modifier", "pct"),
    "Bevölkerungssteuer": ("population_tax_income_multiplier_modifier", "pct"),
    "Unternehmenssteuer": ("corporate_tax_income_multiplier_modifier", "pct"),
    "Fabrikoutput": ("industrial_capacity_factory", "pct"),
    "feindl. Luftüberlegenheit": ("enemy_army_bonus_air_superiority_factor", "pct"),
    "feindl. Luftüberlegenheitsbonus": ("enemy_army_bonus_air_superiority_factor", "pct"),
    "Personalkosten Armee": ("army_personnel_cost_multiplier_modifier", "pct"),
    "Sanktionsresistenz": ("imp_sanction_resistance", "pct"),
    "Spezialkräfte-Limit": ("special_forces_cap", "pct"),
    "Kampagnen-Effektivität": ("mdcw_cw_support_effectiveness", "pct"),
    "Rekrutierung": ("conscription", "pct"),
    "Rekrutierbare Bevölkerung": ("conscription", "pct"),
    "Flak-Schaden": ("static_anti_air_damage_factor", "pct"),
    "Trefferchance": ("static_anti_air_hit_chance_factor", "pct"),
    "Luft-Ausbildungs-XP": ("air_training_xp_gain_factor", "pct"),
    "Hilfsprogramme": ("mdcw_cw_assistance_effectiveness", "pct"),
    "Empfangsgrenzen": ("mdcw_cw_assistance_limit", "pct"),
    "Bevölkerungswachstum": ("monthly_population", "pct"),
    "Kriegsunterstützung": ("war_support_factor", "pct"),
    "Auslandseinfluss": ("foreign_influence_modifier", "pct"),
    "Ulema-Mindestmeinung": ("if_the_ulema_minimum_opinion", "flat"),
    "Militär-Mindestmeinung": ("if_the_military_minimum_opinion", "flat"),
    "Gewerkschafts-Mindestmeinung": ("if_labour_unions_minimum_opinion", "flat"),
    "Mukhabarat-Mindestmeinung": ("if_intelligence_community_minimum_opinion", "flat"),
    "Energieverbrauch Bevölkerung": ("pop_energy_use_multiplier", "pct"),
    "Terror-Erkennung": ("terror_threat_detection_modifier", "pct"),
    "Non-Aligned-Kampagnenkosten": ("nonaligned_outlook_campaign_cost_modifier", "pct"),
    "Emerging-Kampagnenkosten": ("emerging_outlook_campaign_cost_modifier", "pct"),
}
DRIFTS = {"communism_drift", "nationalist_drift", "fascism_drift", "neutrality_drift", "democratic_drift"}
FLAT_KEYS = {"globalism_equilibrium", "return_on_investment_modifier"} | DRIFTS | {
    k for k, (m, mode) in LABEL.items() if mode == "flat"}


def parse_mods(text):
    """'PP-Faktor +5 %, Stabilität −3 % `x`, `communism_drift` +0.02' -> list[(key, value)]"""
    text = re.sub(r"\((?:[^()]*`[^()]*)\)", "", text)  # parentheticals with code refs
    out = []
    for part in re.split(r",\s+|;\s*", text):
        part = part.strip()
        if not part:
            continue
        tok = re.findall(r"`([^`]+)`", part)
        p = re.sub(r"`[^`]+`", "", part).strip()
        m = re.match(r"^(.*?)\s*([+−\-–]\s*[\d.,]+)\s*(%?)$", p)
        if not m:
            # forms like "`communism_drift` +0.03"
            m2 = re.match(r"^([+−\-–][\d.,]+)\s*(%?)$", p)
            if m2 and tok:
                key = tok[0]
                v = num(m2.group(1))
                if m2.group(2) == "%" and key not in FLAT_KEYS:
                    v /= 100
                out.append((key, v))
                continue
            raise ValueError(f"cannot parse modifier part: {part!r} in {text!r}")
        label, val, pct = m.group(1).strip(), num(m.group(2)), m.group(3)
        if label in LABEL:
            key, mode = LABEL[label]
        elif tok and tok[0] not in ("add_ideas", "add_timed_idea"):
            key, mode = tok[0], ("flat" if tok[0] in FLAT_KEYS else "pct")
        else:
            raise ValueError(f"unknown label {label!r} in {text!r}")
        if tok and tok[0] not in ("add_ideas", "add_timed_idea") and tok[0] != key and not tok[0].startswith("EGY_1970"):
            key = tok[0] if not tok[0].startswith("if_") or key.startswith("if_") else key
            mode = "flat" if key in FLAT_KEYS else mode
        if mode == "pct" and pct == "%":
            val = val / 100
        elif mode == "pct" and pct != "%":
            pass  # e.g. drift written without %
        if key == "return_on_investment_modifier":
            val = val / 10  # design 'ROI +0,25' -> MD scale 0.025
        out.append((key, val))
    return out
