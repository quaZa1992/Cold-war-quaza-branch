# COLDWAR | Soviet Union 1970 focus tree - design DSL (Imperia MD Cold War)
# Every effect is a dict: t = German design text, k = kind, plus machine parameters.
# Tokens (`k`/params) are validated against the mod index in validate.py.

PFX = "COLDWAR_SOV_"

PARTY = {
    0: ("Systems Directorate", "Western Autocracy", "Dzhermen Gvishiani"),
    1: ("People's Labour Union (NTS)", "Conservatism", "Vladimir Poremsky"),
    2: ("Committee for Human Rights", "Liberalism", "Andrei Sakharov"),
    3: ("Union of Democratic Socialists", "Socialism", "Roy Medvedev"),
    4: ("Communist Party of the Soviet Union", "Communist State", "Leonid Brezhnev"),
    5: ("Free Councils of Labour", "Anarchist Communism", "Pyotr Siuda"),
    6: ("Neo-Stalinist Platform", "Emerging Conservative", "Sergei Trapeznikov"),
    7: ("Komsomol Vanguard", "Emerging Autocracy", "Alexander Shelepin"),
    8: ("Transcaucasian Islamic Revival", "Moderate Vilayat-e Faqih", "Shia Revival Council"),
    9: ("Guardians of the Faith", "Vilayat-e Faqih", "Council of Guardians"),
    10: ("Bukharan Restoration", "Salafist Kingdom", "Bukharan Regency Council"),
    11: ("Basmachi Revival", "Caliphate", "Ferghana Mujahideen Council"),
    12: ("Muslim Spiritual Reformists", "Muslim Brotherhood", "Ziyauddin Babakhanov"),
    13: ("Gosplan Technocracy", "Neutral Autocracy", "Nikolai Baibakov"),
    14: ("Live Not by Lies", "Neutral Conservatism", "Aleksandr Solzhenitsyn"),
    15: ("The Red Directors", "Oligarchism", "Nikolai Shchelokov"),
    16: ("Free Enterprise League", "Neutral Libertarian", "Nikolai Shmelyov"),
    17: ("Friends of Baikal", "Neutral Green", "Grigory Galazy"),
    18: ("Socialist Market Commonwealth", "Neutral Social", "Alexander Yakovlev"),
    19: ("Union of Sovereign Republics", "Neutral Communism", "Pyotr Shelest"),
    20: ("The Russian Party", "Nationalist Populism", "Dmitry Polyansky"),
    21: ("Committee of National Rebirth", "Nationalist Fascism", "Committee of National Rebirth"),
    22: ("Council of Marshals", "Military Junta", "Andrei Grechko"),
    23: ("House of Romanov", "Monarchism", "Grand Duke Vladimir Kirillovich"),
}
TRIG = {0: "western_autocrats", 1: "western_conservatism", 2: "western_liberals", 3: "western_social_democrats",
        4: "emerging_communist_state", 5: "emerging_anarchist_communism", 6: "emerging_reactionaries",
        7: "emerging_autocracy", 8: "emerging_moderate_shiite", 9: "emerging_hardline_shiite",
        10: "salafist_kingdom", 11: "salafist_caliphate", 12: "neutrality_neutral_muslim_brotherhood",
        13: "neutrality_neutral_autocracy", 14: "neutrality_neutral_conservatism", 15: "neutrality_neutral_oligarch",
        16: "neutrality_neutral_libertarians", 17: "neutrality_neutral_green", 18: "neutrality_neutral_social",
        19: "neutrality_neutral_communism", 20: "nationalist_right_wing_populists", 21: "nationalist_fascist",
        22: "nationalist_military_junta", 23: "nationalist_monarchists"}
SUBIDEO = {0: "Western_Autocracy", 1: "conservatism", 2: "liberalism", 3: "socialism", 4: "communist_state",
           5: "anarchist_communism", 6: "Conservative", 7: "Autocracy", 8: "Mod_Vilayat_e_Faqih", 9: "Vilayat_e_Faqih",
           10: "Kingdom", 11: "Caliphate", 12: "Neutral_Muslim_Brotherhood", 13: "Neutral_Autocracy",
           14: "Neutral_conservatism", 15: "oligarchism", 16: "Neutral_Libertarian", 17: "Neutral_green",
           18: "neutral_Social", 19: "Neutral_Communism", 20: "Nat_Populism", 21: "Nat_Fascism", 22: "Nat_Autocracy",
           23: "Monarchist"}
OUTLOOK = {0: ("Western", "democratic"), 1: ("Emerging", "communism"), 2: ("Salafist", "fascism"),
           3: ("Non-Aligned", "neutrality"), 4: ("Nationalist", "nationalist")}
OUTLOOK_OF = {i: (0 if i < 4 else 1 if i < 10 else 2 if i < 12 else 3 if i < 20 else 4) for i in range(24)}

FAC = {"communist_cadres": "Nomenklatura", "the_military": "Armee & Generalstab", "intelligence_community": "KGB",
       "defense_industry": "Rüstungskomplex (VPK)", "industrial_conglomerates": "Branchenministerien",
       "farmers": "Kolchosbauern", "labour_unions": "Gewerkschaften (VTsSPS)", "the_clergy": "Moskauer Patriarchat",
       "oligarchs": "Schattenwirtschaft", "fossil_fuel_industry": "Öl- und Gasministerien",
       "the_ulema": "Muslimische Geistliche Verwaltungen", "small_medium_business_owners": "Kooperativen & Kleinbetriebe",
       "maritime_industry": "Schiffbau", "landowners": "Agrarbarone"}

# dynamic modifier groups (country scope, MD Russia pattern: variables + add_to_variable)
DYN = {"ps": ("party_state", "Der Parteistaat"), "gp": ("gosplan", "Gosplan – Planwirtschaft"),
       "af": ("armed_forces", "Streitkräfte der UdSSR"), "un": ("union", "Union der Republiken"),
       "cw": ("commonwealth", "Sozialistische Gemeinschaft")}

# German labels for modifier keys (only for the design text)
MODL = {
    "political_power_factor": "PP-Gewinn", "stability_factor": "Stabilität", "war_support_factor": "Kriegsunterstützung",
    "bureaucracy_cost_multiplier_modifier": "Bürokratiekosten", "police_cost_multiplier_modifier": "Polizeikosten",
    "drift_defence_factor": "Ideologische Driftabwehr", "mdcw_cw_ideological_defence": "Ideologische Abwehr (Cold War)",
    "foreign_influence_defense_modifier": "Abwehr fremden Einflusses", "foreign_influence_modifier": "Auslandseinfluss",
    "corruption_cost_factor": "Korruptionskosten", "research_speed_factor": "Forschung",
    "production_speed_buildings_factor": "Baugeschwindigkeit", "production_factory_efficiency_gain_factor": "Effizienzzuwachs",
    "production_factory_max_efficiency_factor": "Max. Fabrikeffizienz", "productivity_growth_modifier": "Produktivitätswachstum",
    "consumer_goods_factor": "Konsumgüter", "civilian_industry_tax_modifier": "Steuer Zivilindustrie",
    "military_industry_tax_modifier": "Steuer Rüstungsindustrie", "tax_gain_multiplier_modifier": "Steuereinnahmen",
    "agricolture_productivity_modifier": "Agrarproduktivität", "agriculture_tax_modifier": "Agrarsteuer",
    "agriculture_workers_modifier": "Arbeitskräftebedarf Landwirtschaft", "industrial_capacity_factory": "Fabrikleistung (zivil)",
    "industrial_capacity_dockyard": "Werftleistung", "oil_export_multiplier_modifier": "Öl-Exporterlöse",
    "resource_export_multiplier_modifier": "Rohstoff-Exporterlöse", "energy_gain_multiplier": "Energieerzeugung",
    "social_cost_multiplier_modifier": "Sozialkosten", "health_cost_multiplier_modifier": "Gesundheitskosten",
    "education_cost_multiplier_modifier": "Bildungskosten", "interest_rate_multiplier_modifier": "Zinsen",
    "trade_opinion_factor": "Handelsmeinung", "globalism_equilibrium": "Globalism-Gleichgewicht",
    "army_attack_factor": "Angriff (Heer)", "army_defence_factor": "Verteidigung (Heer)", "army_org_factor": "Organisation (Heer)",
    "army_morale_factor": "Moral (Heer)", "training_time_factor": "Ausbildungszeit", "experience_gain_army": "Heereserfahrung/Tag",
    "planning_speed": "Planungsgeschwindigkeit", "max_planning_factor": "Max. Planung",
    "army_personnel_cost_multiplier_modifier": "Personalkosten Heer", "personnel_cost_multiplier_modifier": "Personalkosten",
    "equipment_cost_multiplier_modifier": "Ausrüstungskosten", "conscription_factor": "Rekrutierbare Bevölkerung",
    "breakthrough_factor": "Durchbruch", "navy_max_range_factor": "Reichweite Marine", "navy_org_factor": "Organisation Marine",
    "naval_speed_factor": "Geschwindigkeit Marine", "air_defence_factor": "Verteidigung Luft",
    "special_forces_cap": "Spezialkräfte-Limit", "army_core_defence_factor": "Verteidigung auf Kerngebiet",
    "subjects_autonomy_gain": "Autonomiezuwachs der Republiken", "compliance_gain": "Compliance-Zuwachs",
    "recruitable_population_factor": "Rekrutierbare Bevölkerung (Faktor)", "nationalist_drift": "Nationalistische Drift",
    "communism_drift": "Kommunistische Drift", "democratic_drift": "Demokratische Drift", "neutrality_drift": "Blockfreie Drift",
    "fascism_drift": "Salafistische Drift", "opinion_gain_monthly_same_ideology_factor": "Meinungsgewinn gleiche Ideologie",
    "send_volunteer_size": "Freiwilligen-Kontingent", "mdcw_cw_support_effectiveness": "Unterstützungskampagnen (Cold War)",
    "mdcw_cw_assistance_capacity": "Hilfsprogramm-Kapazität (Cold War)", "mdcw_cw_assistance_effectiveness": "Hilfsprogramm-Wirkung (Cold War)",
    "mdcw_cw_military_programme_cost": "Kosten Militärprogramme (Cold War)", "imp_sanction_resistance": "Sanktionsresistenz (Imperia)",
    "intel_network_gain_factor": "Geheimdienstnetz-Zuwachs", "encryption_factor": "Verschlüsselung", "decryption_factor": "Entschlüsselung",
    "foreign_subversive_activites": "Fremde Subversion", "root_out_resistance_effectiveness_factor": "Widerstandsbekämpfung",
    "production_speed_industrial_complex_factor": "Bau Zivilfabriken", "production_speed_arms_factory_factor": "Bau Rüstungsfabriken",
    "production_speed_infrastructure_factor": "Bau Infrastruktur", "production_speed_nuclear_reactor_factor": "Bau Kernreaktoren",
    "production_speed_dockyard_factor": "Bau Werften", "production_speed_offices_factor": "Bau Büros",
    "production_speed_rail_way_factor": "Bau Eisenbahn", "production_speed_air_base_factor": "Bau Luftwaffenbasen",
    "nuclear_energy_generation_modifier": "Kernenergie-Erzeugung", "fossil_pp_energy_generation_modifier": "Erzeugung fossiler Kraftwerke",
    "military_factories_productivity": "Produktivität Rüstungsfabriken", "civilian_factories_productivity": "Produktivität Zivilfabriken",
    "offices_productivity": "Produktivität Büros", "experience_gain_navy": "Marineerfahrung/Tag", "experience_gain_air": "Lufterfahrung/Tag",
    "air_training_xp_gain_factor": "Lufttraining-Erfahrung", "air_accidents_factor": "Flugunfälle",
    "navy_submarine_attack_factor": "U-Boot-Angriff", "naval_damage_factor": "Marine-Schaden", "naval_defense_factor": "Marine-Verteidigung",
    "air_superiority_efficiency": "Luftüberlegenheit-Effizienz", "army_armor_attack_factor": "Panzerangriff",
    "special_forces_attack_factor": "Spezialkräfte-Angriff", "paradrop_organization_factor": "Luftlande-Organisation",
    "terrain_penalty_reduction": "Geländemalus-Reduktion", "acclimatization_cold_climate_gain_factor": "Kälte-Akklimatisierung",
    "supply_consumption_factor": "Versorgungsverbrauch", "mobilization_speed": "Mobilmachungsgeschwindigkeit",
    "monthly_population": "Bevölkerungswachstum", "population_tax_income_multiplier_modifier": "Einkommensteuer-Einnahmen",
    "corporate_tax_income_multiplier_modifier": "Körperschaftsteuer-Einnahmen", "office_park_income_tax_modifier": "Büro-Einnahmen",
    "return_on_investment_modifier": "Investitionsrendite", "receiving_investment_cost_modifier": "Kosten für Investoren bei uns",
    "investment_cost_modifier": "Kosten Auslandsinvestitionen", "total_workforce_modifier": "Arbeitskräfte",
    "expected_welfare_modifier": "Erwartete Sozialausgaben", "nationalist_acceptance": "Nationalist-Akzeptanz",
    "command_power_gain": "Kommandomacht", "air_volunteer_cap": "Luftwaffen-Freiwillige", "justify_war_goal_time": "Kriegsgrund-Zeit",
    "enemy_justify_war_goal_time": "Kriegsgrund-Zeit gegen uns", "party_popularity_stability_factor": "Stabilität aus Parteipopularität",
    "economic_cycles_cost_factor": "Kosten Konjunkturgesetze", "communism_acceptance": "Kommunismus-Akzeptanz",
    "faction_trade_opinion_factor": "Handelsmeinung im Bündnis", "research_sharing_per_country_bonus_factor": "Forschungsteilung",
    "army_infantry_attack_factor": "Infanterieangriff", "mechanized_attack_factor": "Mechanisiert-Angriff",
    "air_mission_xp_gain_factor": "Luftmissions-Erfahrung", "rocket_attack_factor": "Raketenartillerie-Angriff",
    "static_anti_air_damage_factor": "Flak-Schaden (stationär)", "static_anti_air_hit_chance_factor": "Flak-Trefferchance",
    "intelligence_agency_defense": "Spionageabwehr", "operative_slot": "Agenten-Slots", "civilian_intel_factor": "Zivile Aufklärung",
    "army_intel_factor": "Heeresaufklärung", "navy_intel_factor": "Marineaufklärung", "air_volunteer_cap_": "",
    "resistance_growth": "Widerstandswachstum", "required_garrison_factor": "Besatzungsbedarf",
    "production_speed_renewable_energy_infra_factor": "Bau Erneuerbare", "renewable_energy_gain_multiplier": "Erneuerbare Energie",
    "local_resources_factor": "Ressourcenausbeute", "state_resources_factor": "Staatsressourcen",
    "migration_rate_value_factor": "Migration", "health_budget_cost_factor": "Gesundheitsbudget-Kosten",
    "social_budget_cost_factor": "Sozialbudget-Kosten", "military_spending_cost_factor": "Kosten Verteidigungshaushalt",
    "education_budget_cost_factor": "Bildungsbudget-Kosten", "crime_fighting_cost_factor": "Polizeibudget-Kosten",
    "interest_rate_multiplier_modifier_": "", "experience_gain_army_factor": "Heereserfahrung (Faktor)",
    "navy_capital_ship_attack_factor": "Angriff Großkampfschiffe", "naval_coordination": "Marine-Koordination",
    "amphibious_invasion": "Landungsoperationen", "naval_invasion_prep_speed": "Landungsvorbereitung",
    "positioning": "Positionierung", "army_speed_factor": "Heeresgeschwindigkeit", "initiative_factor": "Initiative",
    "special_forces_training_time_factor": "Ausbildung Spezialkräfte", "max_command_power": "Max. Kommandomacht",
    "army_morale_factor_": "", "attrition": "Abnutzung", "army_fuel_consumption_factor": "Treibstoffverbrauch Heer",
    "air_attack_factor": "Luftangriff", "air_agility_factor": "Wendigkeit Luft", "air_range_factor": "Reichweite Luft",
    "air_cas_efficiency": "CAS-Effizienz", "air_intercept_efficiency": "Abfang-Effizienz",
    "enemy_army_bonus_air_superiority_factor": "Feindlicher Luftüberlegenheitsbonus",
    "line_change_production_efficiency_factor": "Effizienzerhalt bei Linienwechsel", "industry_repair_factor": "Reparaturgeschwindigkeit",
    "conversion_cost_civ_to_mil_factor": "Umbaukosten zivil→militär", "license_production_speed": "Lizenzproduktion",
    "global_building_slots_factor": "Bauplätze", "fuel_gain_factor": "Treibstoffgewinn",
    "energy_use_multiplier": "Energieverbrauch", "neutrality_acceptance": "Blockfreie Akzeptanz",
    "democratic_acceptance": "Demokratische Akzeptanz", "fascism_acceptance": "Salafist-Akzeptanz",
    "propaganda_campaign_cost_modifier": "Kosten Propagandakampagnen", "improve_relations_maintain_cost_factor": "Kosten Beziehungen pflegen",
    "nuclear_fuel_consumption_modifier": "Kernbrennstoffverbrauch", "gdp_from_resource_sector_modifier": "BIP aus Rohstoffsektor",
    "resource_sector_workers_modifier": "Arbeitskräfte Rohstoffsektor", "international_market_income_modifier": "Erlöse Waffenmarkt",
    "international_market_purchase_modifier": "Kaufpreise Waffenmarkt", "weekly_manpower": "Mannstärke/Woche",
    "army_leader_start_level": "Startlevel Generäle", "experience_gain_navy_factor": "Marineerfahrung (Faktor)",
    "navy_anti_air_attack_factor": "Marine-Flugabwehr", "naval_mine_hit_chance": "Minentreffer", "naval_accidents_chance": "Marineunfälle",
    "air_superiority_bonus_in_combat": "Luftüberlegenheit im Kampf", "radar": "",
}


def _pct(v):
    s = f"{v*100:+.1f}".rstrip("0").rstrip(".") if abs(v) < 1 or isinstance(v, float) else f"{v:+d}"
    return s


def fmt_mod(k, v):
    """German line for one modifier value."""
    lab = MODL.get(k) or k
    flat = {"experience_gain_army", "experience_gain_navy", "experience_gain_air", "planning_speed", "monthly_population",
            "subjects_autonomy_gain", "compliance_gain", "communism_drift", "democratic_drift", "nationalist_drift",
            "neutrality_drift", "fascism_drift", "special_forces_cap", "operative_slot", "command_power_gain",
            "air_volunteer_cap", "max_command_power", "send_volunteer_size", "globalism_equilibrium",
            "mdcw_cw_assistance_capacity", "weekly_manpower", "army_leader_start_level", "radar",
            "communism_acceptance", "nationalist_acceptance", "democratic_acceptance", "neutrality_acceptance",
            "fascism_acceptance", "positioning"}
    if k in flat:
        return f"{lab} {v:+g}"
    return f"{lab} {v*100:+.0f} %" if abs(v * 100 - round(v * 100)) < 1e-9 else f"{lab} {v*100:+.1f} %"


def mods_text(mods):
    return ", ".join(fmt_mod(k, v) for k, v in mods.items())


# --------------------------------------------------------------------------- effects
def pp(n):
    return dict(k="pp", v=n, t=f"PP {n:+d} `add_political_power`")


def stab(p):
    return dict(k="stab", v=p / 100, t=f"Stabilität {p:+d} % `add_stability`")


def ws(p):
    return dict(k="ws", v=p / 100, t=f"Kriegsunterstützung {p:+d} % `add_war_support`")


def fac(f, n):
    return dict(k="fac", f=f, v=n, t=f"{FAC[f]} {n:+d} `COLDWAR_SOV_change_{f}_opinion_exact` → `change_{f}_opinion`")


def party(i, p, o=None):
    o = p if o is None else o
    return dict(k="party", i=i, v=p / 100, o=o / 100,
                t=f"{PARTY[i][0]} {p:+g} % Popularität (Outlook {o:+g} %) `change_relative_party_popularity`")


def outl(oid, p):
    return dict(k="outlook", o=oid, v=p / 100,
                t=f"Outlook {OUTLOOK[oid][0]} {p:+g} % `COLDWAR_SOV_change_outlook_popularity`")


def dm(group, mods, note=""):
    g, lab = DYN[group]
    return dict(k="dyn", g=g, mods=mods,
                t=f"{lab}: {mods_text(mods)}{(' – ' + note) if note else ''} `COLDWAR_SOV_{g}_modifier`")


IDEAS = {}


def idea(iid, name, mods, days=None, extra="", swap=None, remove=None):
    full = PFX + iid
    IDEAS.setdefault(full, dict(name=name, mods=mods, days=days))
    how = f"{days} Tage `add_timed_idea`" if days else ("`swap_ideas`" if swap else "`add_ideas`")
    pre = ""
    if swap:
        pre = f"ersetzt „{swap}“: "
    return dict(k="idea", id=full, days=days, swap=swap, remove=remove,
                t=f"{pre}Idee „{name}“: {mods_text(mods)}{(', ' + extra) if extra else ''} ({how})")


def rmidea(iid, name):
    full = iid if iid.startswith(PFX) or "_" in iid and not iid.islower() else PFX + iid
    if not iid.startswith(PFX):
        full = PFX + iid
    return dict(k="rmidea", id=full, t=f"Entfernt „{name}“ `remove_ideas`")


def rmidea_raw(iid, name):
    return dict(k="rmidea", id=iid, t=f"Entfernt „{name}“ `remove_ideas`")


def bop(v):
    side = "Reformer" if v < 0 else "Orthodoxe"
    return dict(k="bop", v=v, t=f"Politbüro-Balance {v:+.2f} Richtung {side} `add_power_balance_value`")


def coh(v):
    return dict(k="coh", v=v, t=f"Zusammenhalt der Union {v:+d} `COLDWAR_SOV_change_union_cohesion`")


def gdp(pct):
    return dict(k="gdp", v=pct / 100, t=f"Kosten {pct:g} % BIP `COLDWAR_SOV_pay_gdp_share`")


def gdp_gain(pct):
    return dict(k="gdp_gain", v=pct / 100, t=f"Einnahme +{pct:g} % BIP `COLDWAR_SOV_receive_gdp_share`")


def debt(pct):
    return dict(k="debt", v=pct / 100,
                t=f"Kredit: Treasury +{pct:g} % BIP, Schulden +{pct:g} % BIP `COLDWAR_SOV_receive_gdp_share` `modify_debt_effect`")


BUILD_HELPERS = {
    "civ": ("Zivilfabrik", "one_random_industrial_complex"), "civ2": ("Zivilfabriken", "two_random_industrial_complex"),
    "civ3": ("Zivilfabriken", "three_random_industrial_complex"),
    "mil": ("Rüstungsfabrik", "one_random_arms_factory"), "mil2": ("Rüstungsfabriken", "two_random_arms_factory"),
    "mil3": ("Rüstungsfabriken", "three_random_arms_factory"),
    "off": ("Büro", "one_office_construction"), "off2": ("Büros", "two_office_construction"),
    "inf": ("Infrastruktur", "one_random_infrastructure"), "inf2": ("Infrastruktur", "two_random_infrastructure"),
    "inf3": ("Infrastruktur", "three_random_infrastructure"),
    "nuc": ("Kernreaktor", "one_random_nuclear_reactor"), "agr": ("Agrarbezirk", "one_random_agriculture_district"),
    "agr2": ("Agrarbezirke", "two_random_agriculture_district"), "dock": ("Werft", "one_random_dockyard"),
    "air": ("Luftwaffenbasis", "one_air_base"), "air2": ("Luftwaffenbasen", "two_air_base"),
    "ref": ("Synthetik-Raffinerie", "one_random_synthetic_refinery"), "chip": ("Mikrochipwerk", "one_random_microchip_plant"),
    "ren": ("Erneuerbare-Energie-Anlage", "one_random_renewable_energy_infra"),
    "energy": ("Energieinfrastruktur", "one_random_energy_infrastructure"),
    "indinf": ("Industrieinfrastruktur", "one_random_industrial_infrastructure"),
    "landfac": ("Heeres-Versuchsanstalt", "one_random_land_facility"), "airfac": ("Luftfahrt-Versuchsanstalt", "one_random_air_facility"),
    "navfac": ("Marine-Versuchsanstalt", "one_random_naval_facility"), "nucfac": ("Kernforschungsanlage", "one_random_nuclear_facility"),
    "aa": ("Flugabwehrstellung", "one_anti_air"), "fuel": ("Treibstofflager", "one_fuel_reserve"),
}


def build(kind, cost_pct=None):
    lab, helper = BUILD_HELPERS[kind]
    c = f", Kosten {cost_pct:g} % BIP statt MD-Pauschale (`skip_payment`)" if cost_pct is not None else ""
    return dict(k="build", helper=helper, cost=None if cost_pct is None else cost_pct / 100,
                t=f"Gebäude: {lab} `{helper}`{c}")


def tech(cat, n=1, b=50):
    cats = cat if isinstance(cat, (list, tuple)) else [cat]
    return dict(k="tech", cats=list(cats), n=n, b=b / 100,
                t=f"Forschungsbonus {', '.join(cats)} +{b} % ×{n} `add_tech_bonus`")


def xp(kind, n):
    lab = {"army": "Heereserfahrung", "navy": "Marineerfahrung", "air": "Lufterfahrung"}[kind]
    return dict(k="xp", kind=kind, v=n, t=f"{lab} +{n} `{kind}_experience`")


def mastery(folder, n):
    return dict(k="mastery", folder=folder, v=n, t=f"Doktrin-Mastery {folder} +{n} `add_mastery`")


def sp(project, ratio):
    return dict(k="sp", project=project, v=ratio / 100,
                t=f"Spezialprojekt `sp:{project}` +{ratio} % Fortschritt `add_project_progress_ratio`")


def space():
    return dict(k="space", t="Raumfahrtprogramm-Fortschritt `add_space_program_progress`")


def cp(n):
    return dict(k="cp", v=n, t=f"Kommandomacht +{n} `add_command_power`")


def manpower(n):
    return dict(k="manpower", v=n, t=f"Mannstärke +{n:,} `add_manpower`".replace(",", "."))


def infl(tags, p):
    tags = tags if isinstance(tags, (list, tuple)) else [tags]
    return dict(k="infl", tags=list(tags), v=p,
                t=f"Einfluss {p:+g} % in {', '.join(tags)} `change_influence_percentage`")


def dinfl(p):
    return dict(k="dinfl", v=p, t=f"Einflussabwehr: heimischer Einfluss {p:+g} % `change_domestic_influence_percentage`")


OPINIONS = {}


def op(tag, n, key=None, trade=False):
    key = key or f"{PFX}{tag.lower()}_{'plus' if n > 0 else 'minus'}_{abs(n)}"
    OPINIONS[key] = (n, trade)
    return dict(k="op", tag=tag, v=n, key=key, t=f"Meinung {tag} {n:+d} `add_opinion_modifier`")


OFFERS = {}


def offer(key, tags, text):
    tags = tags if isinstance(tags, (list, tuple)) else [tags]
    OFFERS[PFX + "offer_" + key] = dict(tags=tags, text=text)
    return dict(k="offer", key=PFX + "offer_" + key, tags=list(tags),
                t=f"Angebot an {', '.join(tags)} (Event; Spieler oder KI entscheidet, keine Vorab-Belohnung): {text} `{PFX}offer_{key}`")


EVENTS = {}


def ev(key, text):
    EVENTS[PFX + key] = text
    return dict(k="event", key=PFX + key, t=f"Event: {text}")


FLAGS = set()


def flag(name, text=None):
    FLAGS.add(PFX + name)
    return dict(k="flag", f=PFX + name, t=text or f"Flag `{PFX}{name}`")


DECISIONS = {}


def dec(key, text):
    DECISIONS[PFX + key] = text
    return dict(k="decision", key=PFX + key, t=f"Schaltet Entscheidung frei: {text} `unlock_decision_tooltip`")


def law(helper, text):
    return dict(k="law", helper=helper, t=f"{text} `{helper}`")


def set_law(idea_id, text):
    return dict(k="setlaw", idea=idea_id, t=f"{text} `add_ideas` ({idea_id})")


def tension(v):
    return dict(k="tension", v=v, t=f"Cold-War-Spannung {v:+g} `mdcw_cw_add_tension`")


def cw_join(al, text):
    return dict(k="cwjoin", al=al, t=f"{text} (PP-frei, Fokus ist die Wahl) `mdcw_cw_change_alignment`")


def rp(i, leader=None, note=""):
    ldr = leader or PARTY[i][2]
    return dict(k="rp", i=i, leader=ldr,
                t=f"Regierungspartei → {PARTY[i][0]} ({PARTY[i][1]}) `change_ruling_party_effect`, Staatschef {ldr} `create_country_leader`{(' – ' + note) if note else ''}")


TRAITS = {}


def leader(name, ideo_idx, trait=None, trait_name=None, note=""):
    if trait:
        TRAITS[PFX + trait] = trait_name or trait
    tr = f", Trait „{trait_name}“ `{PFX}{trait}`" if trait else ""
    return dict(k="leader", name=name, i=ideo_idx, trait=(PFX + trait) if trait else None,
                t=f"Neuer Staatschef: {name} `create_country_leader`{tr}{(' – ' + note) if note else ''}")


def trait(t, name):
    TRAITS[PFX + t] = name
    return dict(k="trait", trait=PFX + t, t=f"Staatschef erhält Trait „{name}“ `add_country_leader_trait`")


def elections(on, text=None):
    return dict(k="elections", on=on, t=text or ("Wahlen erlaubt `set_politics`" if on else "Wahlen gesperrt `set_politics`"))


def corr(n):
    h = "decrease_corruption" if n < 0 else "increase_corruption"
    return dict(k="corr", helper=h, v=n, t=f"Korruption {'−' if n < 0 else '+'}{abs(n)} Stufe `{h}`")


def tax(kind, n):
    helper = {"corp": "modify_corporate_tax_rate_effect", "pop": "modify_population_tax_rate_effect"}[kind]
    var = {"corp": "corp_change", "pop": "pop_change"}[kind]
    lab = {"corp": "Körperschaftsteuer", "pop": "Einkommensteuer"}[kind]
    return dict(k="tax", helper=helper, var=var, v=n, t=f"{lab} {n:+d} Pkt. (`{var}`) `{helper}`")


def prod(n):
    return dict(k="prod", v=n, t=f"Produktivität +{n} % (einmalig) `flat_productivity_change_effect`")


def res(resource, amount, where):
    return dict(k="res", r=resource, v=amount, where=where,
                t=f"Ressource: +{amount} {resource} in {where} `add_resource`")


def slot(n=1, where="zufälligem Staat"):
    return dict(k="slot", v=n, t=f"+{n} Bauplatz in {where} `add_extra_state_shared_building_slots`")


def cosmetic(tag, text):
    return dict(k="cosmetic", tag=PFX + tag, t=f"Kosmetischer Name/Flagge: {text} `set_cosmetic_tag`")


def wargoal_none(text):
    return dict(k="note", t=text)


def txt(text):
    return dict(k="note", t=text)


def custom(text, tokens=()):
    return dict(k="custom", tokens=list(tokens), t=text)


# --------------------------------------------------------------------------- foci
FOCI = []
SECTIONS = []


def S(key, title, group, color, desc, party_idx=None):
    SECTIONS.append(dict(key=key, title=title, group=group, color=color, desc=desc, party=party_idx))


def F(fid, name, sec, pre="", mx="", av="", c=5, e=(), n="", h=0, by="", ai=""):
    FOCI.append(dict(id=PFX + fid, name=name, sec=sec,
                     pre=[[PFX + x.strip() for x in grp.split("|")] for grp in pre.split(",") if grp.strip()],
                     mx=[PFX + x.strip() for x in mx.split(",") if x.strip()],
                     av=av, cost=c, eff=list(e), note=n, hist=h, bypass=by, ai=ai))


def power_av(i):
    return f"Popularität {PARTY[i][0]} ≥ 20 %; Stabilität ≥ 35 %; nicht im Krieg mit einer Großmacht"


def inpower(i):
    return f"`{TRIG[i]}_are_in_power`"


PROGS = {}


def pm(key, mods, name=None):
    """Party / leader programme (dynamic modifier with variables, removed when the party/leader loses power)."""
    if name:
        PROGS.setdefault(PFX + key + "_programme", name)
    nm = PROGS.get(PFX + key + "_programme", key)
    return dict(k="prog", g=key, mods=mods, t=f"Programm „{nm}“: {mods_text(mods)} `{PFX}{key}_programme`")


def transition(days=180, extra_coh=0):
    e = [idea("transition_of_power", "Transition of Power", {"stability_factor": -0.10, "political_power_factor": -0.15}, days=days)]
    if extra_coh:
        e.append(coh(extra_coh))
    return e


GENSEC = {}


def gensec(key, name, traits=(), note=""):
    GENSEC[key] = name
    for t in traits:
        TRAITS[PFX + t[0]] = t[1]
    tr = ", ".join(f"„{t[1]}“ `{PFX}{t[0]}`" for t in traits)
    return dict(k="gensec", key=key, name=name, traits=[PFX + t[0] for t in traits],
                t=f"Neuer Generalsekretär: {name}; der Vorgänger geht in den Ruhestand, sein Flag und Programm fallen weg "
                  f"(Flag `{PFX}gensec_{key}`) `{PFX}install_gensec`" + (f"; Traits {tr}" if tr else "") + (f" – {note}" if note else ""))


def heir(key, name, note=""):
    FLAGS.add(f"{PFX}heir_{key}")
    return dict(k="heir", key=key, t=f"Erbe festgelegt: {name} übernimmt beim Tod oder Rücktritt (Flag `{PFX}heir_{key}`, Event setzt den Politbüro-Fokus um)"
                + (f" – {note}" if note else ""))
