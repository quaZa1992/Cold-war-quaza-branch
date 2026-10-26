# IMPERIA CW — Cold War: design — dsl.
"""COLDWAR generic 1970 tree - party path design DSL (data only, no game code).

Every party file defines PARTIES (list) and optionally TRUNK (dict).
Effects are tuples built with the helpers below. Positions, prerequisites,
mutual exclusions and costs come from the fixed template in build.py.
"""

# ---------------------------------------------------------------- vocab
# key: (German label, kind, typical size = 1 point, good sign)
#   kind 'pct' -> shown as %, 'abs' -> shown as plain number
KEYS = {
    # politics
    'stability_factor': ('Stabilität', 'pct', 0.02, +1),
    'political_power_factor': ('PP-Gewinn', 'pct', 0.05, +1),
    'war_support_factor': ('Kriegsunterstützung', 'pct', 0.03, +1),
    'drift_defence_factor': ('Driftabwehr', 'pct', 0.10, +1),
    'foreign_influence_defense_modifier': ('Abwehr fremden Einflusses', 'pct', 0.05, +1),
    'foreign_influence_modifier': ('Einfluss im Ausland', 'pct', 0.05, +1),
    'mdcw_cw_ideological_defence': ('Ideologische Abwehr (CW)', 'pct', 0.10, +1),
    'bureaucracy_cost_multiplier_modifier': ('Bürokratiekosten', 'pct', 0.05, -1),
    'police_cost_multiplier_modifier': ('Polizeikosten', 'pct', 0.05, -1),
    'corruption_cost_factor': ('Korruptionskosten', 'pct', 0.10, -1),
    'internal_factions_cost_factor': ('Kosten Fraktionsaktionen', 'pct', 0.10, -1),
    'party_popularity_stability_factor': ('Stabilität aus Parteipopularität', 'pct', 0.05, +1),
    'democratic_drift': ('Western-Drift', 'abs', 0.03, +1),
    'communism_drift': ('Emerging-Drift', 'abs', 0.03, +1),
    'fascism_drift': ('Salafist-Drift', 'abs', 0.03, +1),
    'neutrality_drift': ('Non-Aligned-Drift', 'abs', 0.03, +1),
    'nationalist_drift': ('Nationalist-Drift', 'abs', 0.03, +1),
    'intel_network_gain_factor': ('Agentennetz-Aufbau', 'pct', 0.10, +1),
    'intelligence_agency_defense': ('Spionageabwehr', 'pct', 0.10, +1),
    'encryption_factor': ('Verschlüsselung', 'pct', 0.10, +1),
    'decryption_factor': ('Entschlüsselung', 'pct', 0.10, +1),
    'required_garrison_factor': ('Benötigte Garnison', 'pct', 0.10, -1),
    # economy
    'research_speed_factor': ('Forschung', 'pct', 0.02, +1),
    'production_speed_buildings_factor': ('Bautempo', 'pct', 0.03, +1),
    'production_speed_industrial_complex_factor': ('Bautempo zivile Fabriken', 'pct', 0.05, +1),
    'production_speed_arms_factory_factor': ('Bautempo Rüstungsfabriken', 'pct', 0.05, +1),
    'production_speed_infrastructure_factor': ('Bautempo Infrastruktur', 'pct', 0.08, +1),
    'production_speed_agriculture_district_factor': ('Bautempo Agrarbezirke', 'pct', 0.08, +1),
    'production_speed_offices_factor': ('Bautempo Büros', 'pct', 0.08, +1),
    'industrial_capacity_factory': ('Fabrikleistung', 'pct', 0.03, +1),
    'industrial_capacity_dockyard': ('Werftleistung', 'pct', 0.05, +1),
    'production_factory_max_efficiency_factor': ('Max. Fabrikeffizienz', 'pct', 0.03, +1),
    'production_factory_efficiency_gain_factor': ('Effizienzwachstum', 'pct', 0.05, +1),
    'consumer_goods_factor': ('Konsumgüter', 'pct', 0.02, -1),
    'productivity_growth_modifier': ('Produktivitätswachstum', 'pct', 0.05, +1),
    'tax_gain_multiplier_modifier': ('Steuereinnahmen', 'pct', 0.03, +1),
    'population_tax_income_multiplier_modifier': ('Einkommensteuer', 'pct', 0.04, +1),
    'corporate_tax_income_multiplier_modifier': ('Körperschaftsteuer', 'pct', 0.04, +1),
    'office_park_income_tax_modifier': ('Büroeinnahmen', 'pct', 0.05, +1),
    'agriculture_tax_modifier': ('Agrarsteuer', 'pct', 0.05, +1),
    'agricolture_productivity_modifier': ('Agrarproduktivität', 'pct', 0.04, +1),
    'military_industry_tax_modifier': ('Steuer Rüstungsindustrie', 'pct', 0.05, +1),
    'return_on_investment_modifier': ('Investitionsrendite', 'pct', 0.005, +1),
    'receiving_investment_cost_modifier': ('Kosten empfangener Investitionen', 'pct', 0.05, -1),
    'interest_rate_multiplier_modifier': ('Zinssatz', 'abs', 0.5, -1),
    'social_cost_multiplier_modifier': ('Sozialkosten', 'pct', 0.05, -1),
    'health_cost_multiplier_modifier': ('Gesundheitskosten', 'pct', 0.05, -1),
    'education_cost_multiplier_modifier': ('Bildungskosten', 'pct', 0.05, -1),
    'buildings_worker_requirement_modifier': ('Arbeiterbedarf Gebäude', 'pct', 0.05, -1),
    'trade_opinion_factor': ('Handelsmeinung', 'pct', 0.05, +1),
    'resource_export_multiplier_modifier': ('Rohstoffexporte', 'pct', 0.05, +1),
    'monthly_population': ('Bevölkerungswachstum', 'pct', 0.05, +1),
    'literacy_rate_education_modifier': ('Alphabetisierung (Bildungseffekt)', 'pct', 0.03, +1),
    'energy_gain_multiplier': ('Energieerzeugung', 'pct', 0.05, +1),
    'globalism_equilibrium': ('Globalismus-Gleichgewicht', 'abs', 5, 0),
    'imp_sanction_resistance': ('Sanktionsresistenz', 'pct', 0.05, +1),
    'imp_oil_price_resistance': ('Ölpreisresistenz', 'pct', 0.10, +1),
    'mdcw_cw_market_exposure': ('Weltmarkt-Exposition (CW)', 'pct', 0.05, -1),
    'mdcw_cw_support_effectiveness': ('Wirkung unserer Unterstützungskampagnen (CW)', 'pct', 0.10, +1),
    'mdcw_cw_assistance_limit': ('Empfangsgrenze Hilfsprogramme (CW)', 'pct', 0.15, +1),
    'mdcw_cw_assistance_capacity': ('Kapazität eigener Hilfsprogramme (CW)', 'abs', 1, +1),
    'mdcw_cw_military_programme_cost': ('Kosten unserer Militärprogramme (CW)', 'pct', 0.10, -1),
    # military
    'conscription_factor': ('Rekrutierbare Bevölkerung', 'pct', 0.02, +1),
    'army_personnel_cost_multiplier_modifier': ('Personalkosten Heer', 'pct', 0.05, -1),
    'personnel_cost_multiplier_modifier': ('Personalkosten Militär', 'pct', 0.05, -1),
    'training_time_army_factor': ('Ausbildungszeit Heer', 'pct', 0.05, -1),
    'experience_gain_army_factor': ('Heeres-XP-Gewinn', 'pct', 0.10, +1),
    'experience_gain_air_factor': ('Luft-XP-Gewinn', 'pct', 0.10, +1),
    'experience_gain_navy_factor': ('Marine-XP-Gewinn', 'pct', 0.10, +1),
    'army_org_factor': ('Organisation Heer', 'pct', 0.03, +1),
    'army_morale_factor': ('Moral Heer', 'pct', 0.05, +1),
    'army_attack_factor': ('Angriff Heer', 'pct', 0.03, +1),
    'army_defence_factor': ('Verteidigung Heer', 'pct', 0.03, +1),
    'army_core_defence_factor': ('Verteidigung auf Kerngebiet', 'pct', 0.05, +1),
    'army_core_attack_factor': ('Angriff auf Kerngebiet', 'pct', 0.05, +1),
    'command_power_gain': ('Kommandomacht', 'abs', 0.10, +1),
    'military_factories_productivity': ('Produktivität Rüstungsfabriken', 'pct', 0.05, +1),
    'equipment_conversion_speed': ('Umrüstgeschwindigkeit', 'pct', 0.10, +1),
    'special_forces_cap': ('Spezialkräfte-Obergrenze', 'pct', 0.10, +1),
    'justify_war_goal_time': ('Kriegszielrechtfertigung', 'pct', 0.10, -1),
    'defensive_war_stability_factor': ('Stabilität im Verteidigungskrieg', 'pct', 0.10, +1),
    'weekly_manpower': ('Wöchentliche Mannstärke', 'abs', 300, +1),
    'production_speed_bunker_factor': ('Bautempo Bunker', 'pct', 0.10, +1),
}

FACTIONS = {
    'chaebols': 'Chaebols', 'communist_cadres': 'Kommunistische Kader', 'defense_industry': 'Rüstungsindustrie',
    'farmers': 'Bauern', 'foreign_jihadis': 'Ausländische Dschihadisten', 'fossil_fuel_industry': 'Fossile Brennstoffindustrie',
    'industrial_conglomerates': 'Konglomerate', 'intelligence_community': 'Geheimdienst',
    'international_bankers': 'Internationale Banker', 'iranian_quds_force': 'Quds-Truppe', 'labour_unions': 'Gewerkschaften',
    'landowners': 'Grundbesitzer', 'maritime_industry': 'Schifffahrtsindustrie', 'oligarchs': 'Oligarchen',
    'saudi_royal_family': 'Saudisches Königshaus', 'small_medium_business_owners': 'Mittelstand', 'the_clergy': 'Klerus',
    'the_donju': 'Donju', 'the_military': 'Militär', 'the_priesthood': 'Priesterschaft', 'the_ulema': 'Ulema',
    'the_wahabi_ulema': 'Wahhabitische Ulema', 'wall_street': 'Wall Street', 'all': 'Alle Fraktionen',
}

# paid MD building helpers (price is inside the helper): helper -> (label, number of buildings)
BUILD = {
    'one_random_industrial_complex': ('1 zivile Fabrik', 1), 'two_random_industrial_complex': ('2 zivile Fabriken', 2),
    'three_random_industrial_complex': ('3 zivile Fabriken', 3),
    'one_random_arms_factory': ('1 Rüstungsfabrik', 1), 'two_random_arms_factory': ('2 Rüstungsfabriken', 2),
    'three_random_arms_factory': ('3 Rüstungsfabriken', 3),
    'one_random_dockyard': ('1 Werft', 1), 'two_random_dockyards': ('2 Werften', 2),
    'one_office_construction': ('1 Bürokomplex', 1), 'two_office_construction': ('2 Bürokomplexe', 2),
    'three_office_construction': ('3 Bürokomplexe', 3),
    'one_random_infrastructure': ('1 Infrastruktur', 1), 'two_random_infrastructure': ('2 Infrastruktur', 2),
    'three_random_infrastructure': ('3 Infrastruktur', 3),
    'one_random_agriculture_district': ('1 Agrarbezirk', 1), 'two_random_agriculture_district': ('2 Agrarbezirke', 2),
    'one_random_energy_infrastructure': ('1 Energieinfrastruktur', 1),
    'one_random_industrial_infrastructure': ('1 Industrieinfrastruktur', 1),
    'one_random_fossil_fuel_powerplant': ('1 Fossilkraftwerk', 1), 'two_random_fossil_fuel_powerplant': ('2 Fossilkraftwerke', 2),
    'one_random_renewable_energy_infra': ('1 Erneuerbare-Anlage', 1), 'two_random_renewable_energy_infra': ('2 Erneuerbare-Anlagen', 2),
    'one_random_nuclear_reactor': ('1 Kernreaktor', 1),
    'one_random_synthetic_refinery': ('1 Synthetische Raffinerie', 1),
    'one_air_base': ('1 Luftwaffenbasis', 1), 'two_air_base': ('2 Luftwaffenbasen', 2),
    'one_anti_air': ('1 Flak', 1), 'two_anti_air': ('2 Flak', 2),
    'one_radar_station': ('1 Radarstation', 1), 'two_radar_station': ('2 Radarstationen', 2),
    'one_fuel_reserve': ('1 Treibstofflager', 1),
    'one_random_land_facility': ('1 Landforschungsanlage', 1), 'one_random_air_facility': ('1 Luftforschungsanlage', 1),
    'one_random_naval_facility': ('1 Marineforschungsanlage', 1), 'one_random_nuclear_facility': ('1 Nuklearforschungsanlage', 1),
}

# MD budget / law helpers (running costs or law steps)
LAWS = {
    'increase_military_spending': 'Verteidigungsbudget eine Stufe höher', 'decrease_military_spending': 'Verteidigungsbudget eine Stufe niedriger',
    'increase_policing_budget': 'Polizeibudget eine Stufe höher', 'decrease_policing_budget': 'Polizeibudget eine Stufe niedriger',
    'increase_social_spending': 'Sozialbudget eine Stufe höher', 'decrease_social_spending': 'Sozialbudget eine Stufe niedriger',
    'increase_healthcare_budget': 'Gesundheitsbudget eine Stufe höher', 'decrease_healthcare_budget': 'Gesundheitsbudget eine Stufe niedriger',
    'increase_education_budget': 'Bildungsbudget eine Stufe höher', 'decrease_education_budget': 'Bildungsbudget eine Stufe niedriger',
    'increase_centralization': 'Zentralisierung eine Stufe höher', 'decrease_centralization': 'Zentralisierung eine Stufe niedriger',
    'increase_migration_law': 'Migrationsgesetz strenger (MD: Richtung closed_borders)', 'decrease_migration_law': 'Migrationsgesetz offener (MD: Richtung open_borders)',
    'increase_exports': 'Exportquote höher', 'decrease_exports': 'Exportquote niedriger',
}

CATS = ['CAT_small_arms', 'CAT_utility_vehicles', 'CAT_surface_to_air_missiles', 'CAT_anti_air', 'CAT_aircraft',
        'CAT_towed_artillery', 'CAT_self_propelled_artillery', 'CAT_night_vision', 'CAT_naval_anti_ship_missiles',
        'CAT_manpads', 'CAT_infantry_fighting_vehicles', 'CAT_helicopters', 'CAT_heavy_aircraft', 'CAT_corvettes',
        'CAT_attack_helicopters', 'CAT_armored_fighting_vehicles', 'CAT_armor', 'CAT_transport_helicopters',
        'CAT_surface_ships', 'CAT_special_forces_equipment', 'CAT_satellites', 'CAT_nuclear_reactors', 'CAT_nuclear',
        'CAT_medium_aircraft', 'CAT_main_battle_tanks', 'CAT_light_anti_tank', 'CAT_light_aircraft', 'CAT_anti_tank',
        'CAT_air_to_ground_weapons', 'CAT_encryption', 'CAT_decryption', 'CAT_computing', 'CAT_agriculture',
        'CAT_submarines', 'CAT_destroyers']

# existing MD ideas usable as rewards: name -> (label, approx points)
MD_IDEAS = {
    'political_power_bonus': ('MD-Idee Political Power Bonus (PP +10 %)', 2),
    'generic_centralization': ('MD-Idee Centralization (PP +15 %, Steuern +5 %, Bürokratie +25 %)', 2),
    'generic_decentralization': ('MD-Idee Decentralization (Bautempo +10 %, Bürokratie −25 %)', 3),
    'militarism': ('MD-Idee Militarism (Rekrutierung +10 %, Umrüstung −30 %, Effizienzwachstum −10 %)', 3),
    'peaceful_emergence': ('MD-Idee Peaceful Emergence (Effizienzwachstum +10 %, Fabrikbau +10 %)', 4),
    'defensive_constructions2': ('MD-Idee Defensive Constructions (Bunkerbau +10 %)', 1),
    'idea_focus_generic_national_heritage': ('MD-Idee National Heritage (Stabilität wöchentl., Rekrutierung +10 %)', 3),
    'idea_focus_generic_counter_terrorism': ('MD-Idee Counter-Terrorism (Aufklärung, Driftabwehr +10 %)', 2),
    'idea_focus_unemployment_program': ('MD-Idee Unemployment Program (Sozial-/Gesundheitskosten −5 %)', 2),
    'idea_focus_social_spending_expansions': ('MD-Idee Social Spending Expansions (Sozialkosten −10 %)', 2),
    'idea_focus_generic_public_service_investment': ('MD-Idee Public Service Investment (Bau +10 %, Steuern +10 %)', 4),
    'idea_focus_expanded_secret_services': ('MD-Idee Expanded Secret Services', 2),
    'agricultural_investments': ('MD-Idee Agricultural Investments', 2),
    'economic_autonomy': ('MD-Idee Economic Autonomy (Kapazität +10 %, lokale Rohstoffe +10 %)', 3),
    'developmentalism': ('MD-Idee Developmentalism (Bautempo +10 %)', 3),
    'combined_defense_industries_idea': ('MD-Idee Combined Defence Industries', 3),
    'military_industry_project': ('MD-Idee Military Industry Project', 2),
    'railway_construction_effort': ('MD-Idee Railway Construction Effort (Schienenbau +35 %)', 1),
    'hydroelectric_energy_production_idea': ('MD-Idee Hydroelectric Energy Production', 2),
    'neutrality_idea': ('MD-Idee Neutrality (Abwehr fremden Einflusses +30 %)', 3),
    'revanchism': ('MD-Idee Revanchism (Angriff +10 %)', 3),
    'light_infantry_special_forces_idea': ('MD-Idee Light Infantry Special Forces', 2),
    'establishing_a_paratrooper_corps_idea': ('MD-Idee Paratrooper Corps', 2),
}

OUTLOOKS = {'W': 'Western', 'E': 'Emerging', 'S': 'Salafist', 'N': 'Non-Aligned', 'R': 'Nationalist'}


# ---------------------------------------------------------------- effects
def prog(key, v):            return ('prog', key, v)            # party programme line (only while the party rules)
def idea(iid, mods, name, bound=False):                          # new permanent national spirit GEN_1970_<iid>
    return ('idea', iid, mods, name, bound)                      # bound=True: removed when the party loses power
def timed(iid, days, mods, name): return ('timed', iid, days, mods, name)
def swap(old, new, mods, name, bound=False):                     # ladder: replaces idea <old> (defined earlier) with <new>
    return ('swap', old, new, mods, name, bound)
def mdidea(name):            return ('mdidea', name)
def mdtimed(name, days):     return ('mdtimed', name, days)
def pp(v):                   return ('pp', v)
def stab(v):                 return ('stab', v)
def ws(v):                   return ('ws', v)
def fac(f, v):               return ('fac', f, v)
def pop(v):                  return ('pop', v)                  # ruling party (+ its outlook)
def outlook(o, v):           return ('outlook', o, v)           # another outlook W/E/S/N/R (+ = they grow)
def build(helper):           return ('build', helper)
def money(share):            return ('money', share)            # share of GDP, + gain, - cost
def debt(share):             return ('debt', share)             # + more debt (share of GDP)
def tech(cats, bonus, uses): return ('tech', tuple(cats) if isinstance(cats, (list, tuple)) else (cats,), bonus, uses)
def xp(kind, v):             return ('xp', kind, v)             # army / air / navy
def law(helper):             return ('law', helper)
def corruption(n):           return ('corruption', n)           # -1 = one level less, +1 = one level more
def corruption_chance():     return ('corruption_chance',)
def tension(v):              return ('tension', v)              # global Cold War tension (0-100)
def literacy(v):             return ('literacy', v)             # one-off literacy rate change (0.05 = +5 %)
def growth(n=1):             return ('growth', n)               # MD economic cycle one step up (n<0 down)
def flag(name, text):        return ('flag', name, text)
def note(text):              return ('note', text)


def F(fid, name, fx, why, old=False):
    return dict(id=fid, name=name, fx=list(fx), why=why, old=old)
