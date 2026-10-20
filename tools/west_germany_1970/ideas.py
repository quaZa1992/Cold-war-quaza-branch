"""National spirits of the Federal Republic 1970-2000 (and two for the GDR)."""
from cw_lib import P, L

# key: (name, desc, picture (GFX_idea_<picture>), modifier dict)
IDEAS = {
    # --- starting spirits
    "bonn_republic": ("Bonn Is Not Weimar",
                      "Constructive votes of no confidence, a 5% hurdle, a Constitutional Court and militant democracy: the Basic Law was written against the failures of 1933.",
                      "democracy", {"stability_factor": 0.08, "drift_defence_factor": 0.2}),
    "fading_miracle": ("The Fading Miracle",
                       "Growth is slowing, the labour market is empty and the unions want a share of twenty years of prosperity.",
                       "economic_boom", {"production_speed_buildings_factor": 0.05, "consumer_goods_factor": 0.03}),
    "frontline_state": ("Frontline State",
                        "Twenty Soviet divisions stand behind the inner-German border. The Fulda Gap is the most planned battlefield on earth.",
                        "fortification", {"army_core_defence_factor": 0.1, "war_support_factor": 0.05, "conscription": 0.005}),
    "nuclear_sharing": ("Nuclear Participation",
                        "No German bomb - but German aircraft, German missiles and a seat in NATO's Nuclear Planning Group.",
                        "NATO_member", {"mdcw_cw_ideological_defence": 0.05}),
    "hallstein_legacy": ("The Hallstein Doctrine's Shadow",
                         "For fifteen years Bonn broke relations with anyone who recognised the GDR. The doctrine is dying, but the reflex remains.",
                         "anti_soviet_pact", {"trade_opinion_factor": -0.1, "political_power_factor": -0.03}),
    "extraparliamentary_opposition": ("The Children of 1968",
                                      "The extra-parliamentary opposition has split: into the SPD, into the citizens' initiatives, into the K-groups - and into the underground.",
                                      "political_violence", {"stability_factor": -0.04, "research_speed_factor": 0.02}),
    "strong_dmark": ("The Deutschmark",
                     "The only national symbol West Germans trust without reservation.",
                     "deutsche_mark", {"interest_rate_multiplier_modifier": -0.1, "currency_strength_modifier": 0.05}),
    "guest_workers": ("Guest Workers",
                      "Italians, Spaniards, Greeks, Yugoslavs and Turks build the cars - and are expected to leave one day.",
                      "migration_regulation_light", {"total_workforce_modifier": 0.03}),
    # --- politics
    "student_aid": ("BAföG", "Federal grants open universities to working-class children.", "research_minstry",
                    {"research_speed_factor": 0.03, "education_cost_multiplier_modifier": 0.05}),
    "codetermination": ("Co-determination", "Employees sit on the supervisory boards of large companies.", "labour_unions",
                        {"stability_factor": 0.03, "production_factory_efficiency_gain_factor": 0.03}),
    "kohl_system": ("The Kohl System", "Patience, loyalty and the telephone.", "political_power_bonus",
                    {"political_power_factor": 0.08, "stability_factor": 0.02}),
    "red_green_project": ("The Red-Green Project", "A government of the generation of 1968.", "social_democracy",
                          {"stability_factor": 0.02, "research_speed_factor": 0.02, "production_speed_buildings_factor": -0.02}),
    "strauss_government": ("Chancellor Strauß", "Polarising, brilliant, unpredictable.", "army_strengthened",
                           {"political_power_factor": 0.05, "stability_factor": -0.04, "war_support_factor": 0.05}),
    # --- economy
    "bundesbank_credibility": ("Bundesbank Credibility", "Frankfurt fights inflation whatever Bonn wants.", "stable_growth",
                               {"interest_rate_multiplier_modifier": -0.1, "inflation_cost_multiplier_modifier": -0.1}),
    "floating_dmark": ("A Floating Deutschmark", "The D-Mark rises against the dollar: cheaper oil, dearer exports.", "deutsche_mark",
                       {"currency_strength_modifier": 0.05, "production_speed_buildings_factor": -0.02}),
    "ems": ("European Monetary System", "European currencies tied to a grid anchored on the D-Mark.", "european_union_member",
            {"globalism_equilibrium": 5, "trade_opinion_factor": 0.05}),
    "export_champion": ("Export World Champion", "Made in Germany sells everywhere.", "export_economy",
                        {"industrial_capacity_factory": 0.05, "tax_gain_multiplier_modifier": 0.03}),
    "working_time_385": ("38.5-Hour Week", "Shorter hours, flexible plants.", "worker_reforms",
                         {"stability_factor": 0.02, "production_factory_max_efficiency_factor": -0.02}),
    "single_market": ("Single European Market", "Goods, capital, services and people without borders.", "european_union_member",
                      {"globalism_equilibrium": 8, "production_factory_max_efficiency_factor": 0.03}),
    "treuhand": ("The Treuhand", "Privatise, restructure, close.", "industrial_concern",
                 {"production_speed_buildings_factor": 0.05, "stability_factor": -0.04}),
    "soli": ("Solidarity Surcharge", "A supplement on income tax for the East.", "inflation_spirit",
             {"tax_gain_multiplier_modifier": 0.05, "stability_factor": -0.02}),
    "euro_founder": ("Founder of the Euro", "A currency built in the image of the D-Mark.", "euro",
                     {"globalism_equilibrium": 10, "interest_rate_multiplier_modifier": -0.1, "trade_opinion_factor": 0.1}),
    "dmark_bloc": ("The D-Mark Bloc", "A hard-currency zone around Frankfurt.", "euro",
                   {"interest_rate_multiplier_modifier": -0.15, "globalism_equilibrium": 4}),
    "integration_policy": ("Country of Immigration", "The guest workers stay - and so do their children.", "migration_regulation_medium",
                           {"total_workforce_modifier": 0.03, "stability_factor": -0.01}),
    "dual_system": ("Dual Vocational Training", "Apprenticeships in firm and school.", "worker_reforms",
                    {"production_factory_efficiency_gain_factor": 0.05}),
    # --- energy
    "kohlepfennig": ("The Coal Penny", "Every electricity bill pays for German coal.", "coal",
                     {"stability_factor": 0.01, "production_speed_buildings_factor": -0.02, "fossil_pp_energy_generation_modifier": 0.05}),
    "nuclear_buildout": ("Nuclear Build-Out", "Fifty reactors are planned.", "nuclear_energy",
                         {"nuclear_energy_generation_modifier": 0.1, "stability_factor": -0.02}),
    "soviet_gas": ("Siberian Gas", "Pipes for gas, gas for decades.", "oil_profits",
                   {"fossil_pp_energy_generation_modifier": 0.05, "mdcw_cw_ideological_defence": -0.03}),
    "flue_gas_law": ("Flue Gas Desulphurisation", "Filters for every coal power plant.", "eco_factories",
                     {"stability_factor": 0.02, "production_speed_buildings_factor": -0.01}),
    "eco_tax": ("Ecological Tax Reform", "Tax energy, relieve labour.", "eco_factories",
                {"tax_gain_multiplier_modifier": 0.03, "energy_use_multiplier": -0.05}),
    # --- security
    "radicals_decree": ("The Radicals Decree", "Loyalty checks for every public servant.", "spy_intel",
                        {"political_power_factor": -0.02, "police_cost_multiplier_modifier": 0.05}),
    "security_state": ("Security State", "The state has given itself extraordinary powers.", "political_violence",
                       {"stability_factor": -0.05, "police_cost_multiplier_modifier": 0.2, "terror_threat_detection_modifier": 0.25}),
    "deutscher_herbst": ("German Autumn", "Kidnappings, hijackings, a crisis staff that governs.", "political_violence",
                         {"stability_factor": -0.05, "political_power_factor": -0.05}),
    # --- Bundeswehr
    "army_structure_4": ("Army Structure 4", "Thirty-six heavy brigades.", "army_tank_good",
                         {"army_org_factor": 0.05, "experience_gain_army": 0.05}),
    "army_structure_5": ("Army Structure 5", "370,000 soldiers.", "army_war_college",
                         {"army_personnel_cost_multiplier_modifier": -0.1, "conscription": -0.003}),
    "officer_education": ("Academic Officers", "Educated officers for a democratic army.", "army_good_officer",
                          {"experience_gain_army": 0.05, "max_planning": 0.05}),
    "territorial_army": ("Territorial Army", "Reservists to hold the rear.", "fortification2",
                         {"army_core_defence_factor": 0.05}),
    # --- West and East
    "open_borders": ("Schengen", "No more controls at the inner European borders.", "migration_open_borders",
                     {"globalism_equilibrium": 4, "trade_opinion_factor": 0.05}),
    "un_member": ("Member of the United Nations", "Two German states at the UN.", "european_union_member",
                  {"political_power_factor": 0.03}),
    "cultural_diplomacy": ("Cultural Foreign Policy", "Goethe-Institut, Deutsche Welle, DAAD.", "propaganda",
                           {"foreign_influence_defense_modifier": 0.05, "trade_opinion_factor": 0.05}),
    "bmz": ("Development Ministry", "Development aid as foreign policy.", "trade",
            {"mdcw_cw_assistance_capacity": 1, "mdcw_cw_assistance_effectiveness": 0.1}),
    "north_south": ("North-South Dialogue", "The Brandt Commission's legacy.", "trade",
                    {"political_power_factor": 0.02, "mdcw_cw_assistance_effectiveness": 0.1}),
    "development_partner": ("Development Partnerships", "Wells, roads and schools.", "trade",
                            {"mdcw_cw_assistance_capacity": 1}),
    "unsc_member": ("Security Council Seat", "Two years at the table.", "european_union_member",
                    {"political_power_factor": 0.05}),
    "inner_unity": ("Inner Unity", "One state, two societies.", "democracy",
                    {"stability_factor": 0.03, "production_speed_buildings_factor": 0.02}),
    "aufbau_ost": ("Aufbau Ost", "A trillion marks for the new Länder.", "economy_housing",
                   {"tax_gain_multiplier_modifier": -0.06, "stability_factor": -0.03, "production_speed_buildings_factor": 0.05}),
    "two_plus_four": ("Two Plus Four", "Full sovereignty - and limits on the army.", "NATO_member",
                      {"political_power_factor": 0.05, "army_personnel_cost_multiplier_modifier": 0.05}),
    "new_constitution": ("A Constitution for All Germans", "The Basic Law is replaced by a constitution adopted by the whole people.", "democracy",
                         {"stability_factor": 0.06, "political_power_factor": -0.03}),
    "neutral_germany": ("Neutral Germany", "Unity bought with neutrality between the blocs.", "anti_soviet_pact",
                        {"mdcw_cw_ideological_defence": -0.05, "trade_opinion_factor": 0.1, "war_support_factor": -0.1}),
    "german_confederation": ("German Confederation", "Two states, one nation, common institutions.", "democracy",
                             {"political_power_factor": -0.03, "trade_opinion_factor": 0.05}),
    "second_cold_war": ("The Second Cold War", "The Wall stands again.", "fortification3",
                        {"war_support_factor": 0.1, "consumer_goods_factor": 0.03}),
    "car_free_sundays": ("Car-Free Sundays", "Empty motorways, a speed limit and a nation on bicycles.", "Stabilized_Food_Supply",
                         {"fossil_fuel_consumption": -0.1, "stability_factor": -0.02}),
    "stagflation": ("Stagflation", "Prices rise while the jobs disappear.", "inflation2",
                    {"production_speed_buildings_factor": -0.05, "stability_factor": -0.03}),
    "peace_movement_idea": ("The Peace Movement", "Hundreds of thousands in the Hofgarten.", "democratic_socialism",
                            {"war_support_factor": -0.08, "stability_factor": -0.02}),
    "asylum_crisis": ("The Asylum Debate", "438,000 applications in one year.", "migration_regulation_hard",
                      {"stability_factor": -0.04, "total_workforce_modifier": 0.02}),
}

SOV_IDEAS = {}
DDR_IDEAS = {
    "ddr_crackdown": ("The Chinese Solution", "The regime has fired on its own people.", "political_violence",
                      {"stability_factor": -0.08, "political_power_factor": -0.05, "police_cost_multiplier_modifier": 0.2}),
    "ddr_round_table": ("The Round Table", "Party, churches and civic movements negotiate the future.", "democracy",
                        {"stability_factor": -0.03, "political_power_factor": -0.05}),
    "ddr_abgrenzung": ("Abgrenzung", "Demarcation: the GDR seals itself off from the West, ideologically and physically.", "anti_soviet_pact",
                       {"stability_factor": 0.03, "consumer_goods_factor": 0.02}),
}


def ideas_file():
    out = ["## Generated by tools/west_germany_1970/compile.py. Edit the generator, not this file.\n", "ideas = {", "\tcountry = {"]
    for table, tag in ((IDEAS, "GER"), (DDR_IDEAS, "DDR"), (SOV_IDEAS, "SOV")):
        for k, (name, desc, pic, mods) in table.items():
            iid = f"{P}_idea_{k}"
            L(iid, name)
            L(iid + "_desc", desc)
            out.append(f"\t\t{iid} = {{")
            out.append(f"\t\t\tpicture = {pic}")
            out.append(f"\t\t\tallowed = {{ original_tag = {tag} }}")
            out.append("\t\t\tallowed_civil_war = { always = yes }")
            out.append("\t\t\tremoval_cost = -1")
            out.append("\t\t\tmodifier = {")
            for mk, mv in mods.items():
                out.append(f"\t\t\t\t{mk} = {mv}")
            out.append("\t\t\t}")
            out.append("\t\t}")
    out.append("\t}")
    out.append("}")
    return "\n".join(out) + "\n"
