# IMPERIA CW — Cold War: Cold War SOV design — d politics.
from sov_dsl import *

# ------------------------------------------------------------------ helpers
POWER_NAMES = {
    0: "The Systems Men Take Charge", 1: "The Solidarists Return", 2: "Power to the Human Rights Committee",
    3: "Power to the Democratic Socialists", 4: "Restore the Party of Lenin", 5: "All Power to the Councils",
    6: "The Iron Line Takes Power", 7: "The Komsomol Vanguard Takes Power", 8: "The Shia Revival Takes Power",
    9: "The Guardians Take Power", 10: "Restore the Emirate", 11: "The Basmachi Rise",
    12: "The Muftis' Government", 13: "The Planners' Government", 14: "Live Not by Lies in Power",
    15: "The Directors Take Over", 16: "The Free Enterprise Cabinet", 17: "The Green Cabinet",
    18: "The Market Socialists Take Power", 19: "A Union of Sovereign Republics", 20: "The Russian Party Takes Power",
    21: "The National Rebirth", 22: "The Marshals Step In", 23: "The Return of the Romanovs"}
POWER_IDS = {i: "power_" + {0: "systems_men", 1: "solidarists", 2: "human_rights", 3: "democratic_socialists", 4: "the_cpsu",
                            5: "councils", 6: "iron_line", 7: "komsomol", 8: "shia_revival", 9: "guardians", 10: "emirate",
                            11: "basmachi", 12: "muftis", 13: "planners", 14: "solzhenitsyn", 15: "directors",
                            16: "free_enterprise", 17: "greens", 18: "market_socialists", 19: "sovereign_republics",
                            20: "russian_party", 21: "national_rebirth", 22: "marshals", 23: "romanovs"}[i] for i in range(24)}


def power_to(i, sec, pre, av_extra="", e_extra=(), c=5, ai="", n=""):
    av = f"Popularität {PARTY[i][0]} ≥ 20 %; Partei regiert noch nicht; nicht im Bürgerkrieg" + (f"; {av_extra}" if av_extra else "")
    F(POWER_IDS[i], POWER_NAMES[i], sec, pre, av=av, c=c, ai=ai,
      e=[rp(i)] + transition() + list(e_extra),
      n=n or "Machtübergabe im eigenen Land (wirkt auf kein anderes Land). Jede Übergabe ist einmal möglich; die KI übergibt höchstens einmal.")


# ================================================================== EMERGING (CPSU home outlook)
F("em_the_party_of_a_new_type", "The Party of a New Type", "em", "dir_the_leading_role", c=5, e=[
    outl(1, 3), dm("ps", {"political_power_factor": 0.02})])
F("em_komsomol_mobilisation", "Komsomol Mobilisation", "em", "dir_the_leading_role", c=5, e=[
    outl(1, 3), stab(1), manpower(10000)])
F("em_the_workers_state", "The Workers' State", "em", "em_the_party_of_a_new_type,em_komsomol_mobilisation", c=5, e=[
    outl(1, 5), fac("labour_unions", 5)])
for i in (4, 5, 6, 7):
    power_to(i, "em", "em_the_workers_state",
             av_extra={4: "", 5: "Politbüro-Balance ≤ −0,2 (Reformer) oder Gewerkschaften ≥ 70",
                       6: "Politbüro-Balance ≥ 0,4 (Orthodoxe)", 7: "Politbüro-Balance ≥ 0,3; KGB-Meinung ≥ 60"}[i])

F("em_the_leading_role_of_the_party", "The Leading Role of the Party", "em", av="`has_government = communism`", c=3, h=1, e=[
    pp(50), idea("socialist_state", "Socialist State", {"communism_drift": 0.02, "mdcw_cw_ideological_defence": 0.05})],
  n="Einstieg in den Regierungsteil – kein Richtungsfokus nötig, auch nach Putsch oder Machtübergabe erreichbar.")
F("em_socialist_emulation", "Socialist Emulation", "em", "em_the_leading_role_of_the_party", c=5, h=1, e=[
    dm("gp", {"production_factory_efficiency_gain_factor": 0.03}), party(4, 2)], n="Sozialistischer Wettbewerb der Brigaden.")
F("em_peoples_control", "People's Control", "em", "em_the_leading_role_of_the_party", c=5, h=1, e=[
    corr(-1), fac("communist_cadres", -5)])
F("em_peace_and_socialism", "Peace and Socialism", "em", "em_socialist_emulation,em_peoples_control", c=5, e=[
    dm("cw", {"mdcw_cw_support_effectiveness": 0.05}), outl(1, 3)], n="Die Prager Zeitschrift der Weltbewegung als Plattform.")

# ================================================================== WESTERN
F("we_the_samizdat_presses", "Tolerate the Samizdat Presses", "we", "dir_convergence", c=5, e=[outl(0, 3), stab(-1)])
F("we_stop_the_jamming", "Stop the Jamming", "we", "dir_convergence", c=5, e=[
    outl(0, 3), dm("cw", {"trade_opinion_factor": 0.05}), dm("ps", {"drift_defence_factor": -0.05})],
  n="1973 wurde das Stören von Voice of America und BBC kurz eingestellt.")
F("we_recognise_the_human_rights_committee", "Recognise the Human Rights Committee", "we", "we_the_samizdat_presses,we_stop_the_jamming", c=5, e=[
    outl(0, 5), bop(-0.05), fac("intelligence_community", -10)])
for i in (0, 1, 2, 3):
    power_to(i, "we", "we_recognise_the_human_rights_committee",
             av_extra="Politbüro-Balance ≤ −0,4 (Reformer) ODER Stabilität < 30 %", e_extra=[coh(-10)],
             n="Ein Regimewechsel weg vom Parteistaat: zusätzlich Zusammenhalt −10. Die KI übergibt nie an den Westen.", ai="0")
F("we_a_democratic_union", "A Democratic Union", "we", av="`has_government = democratic`", c=3, e=[
    pp(50), idea("free_union", "A Free Union", {"democratic_drift": 0.02, "research_speed_factor": 0.03, "stability_factor": -0.03})])
F("we_free_elections", "Free Elections", "we", "we_a_democratic_union", c=5, e=[
    elections(True, "Wahlen erlaubt, Turnus 48 Monate `set_politics`"), stab(-3), coh(-3), party(2, 3)])
F("we_the_market_returns", "The Market Returns", "we", "we_a_democratic_union", c=5, e=[
    set_law("mixed_economy", "Handelsgesetz → Gemischte Wirtschaft"), dm("gp", {"productivity_growth_modifier": 0.05}), stab(-3)])
F("we_join_the_free_world", "Join the Free World", "we", "we_free_elections,we_the_market_returns", c=5, e=[
    cw_join("west", "Cold War: Wechsel in den Westblock, nur wenn `mdcw_cw_can_join_west`"), tension(-3)])

# ================================================================== NON-ALIGNED
F("na_the_yugoslav_model", "The Yugoslav Model", "na", "dir_third_way", c=5, e=[outl(3, 3), op("SER", 15, key="COLDWAR_SOV_third_way")],
  n="Belgrad als Vorbild der Selbstverwaltung.")
F("na_the_technocrats", "The Technocrats", "na", "dir_third_way", c=5, e=[outl(3, 3), dm("gp", {"productivity_growth_modifier": 0.02})])
F("na_the_village_prose", "The Village Prose", "na", "dir_third_way", c=5, e=[outl(3, 2), party(14, 2)],
  n="Rasputin, Below, Schukschin – die Dorfprosa als konservative Gegenkultur.")
F("na_the_third_force", "The Third Force", "na", "na_the_yugoslav_model,na_the_technocrats|na_the_village_prose", c=5, e=[outl(3, 5), bop(-0.05)])
for i in (13, 14, 15, 16, 17, 18, 19):
    power_to(i, "na", "na_the_third_force",
             av_extra={13: "Politbüro-Balance zwischen −0,4 und 0,4",
                       14: "Stabilität < 45 % ODER Politbüro-Balance ≥ 0,4", 15: "Korruptionsstufe ≥ 6", 16: "Politbüro-Balance ≤ −0,5",
                       17: "`COLDWAR_SOV_aral_disaster` gesetzt ODER `COLDWAR_SOV_rbmk` gesetzt", 18: "Politbüro-Balance ≤ −0,3",
                       19: "Zusammenhalt der Union < 45"}[i],
             ai="0" if i == 16 else "", e_extra=[coh(-5)] if i == 19 else [])
F("na_neither_moscow_nor_washington", "Neither Moscow nor Washington", "na", av="`has_government = neutrality`", c=3, e=[
    pp(50), idea("non_aligned_union", "Non-Aligned Union", {"neutrality_drift": 0.02, "foreign_influence_defense_modifier": 0.05})])
F("na_the_third_way_economy", "The Third Way Economy", "na", "na_neither_moscow_nor_washington", c=5, e=[
    dm("gp", {"productivity_growth_modifier": 0.03, "trade_opinion_factor": 0.05})])
F("na_dissolve_the_pact", "Dissolve the Warsaw Pact?", "na", "na_neither_moscow_nor_washington", c=5, ai="0", e=[
    custom("Löst unsere Fraktion auf, Mitglieder werden über Event informiert und entscheiden selbst über neue Bündnisse `dismantle_faction`", ["dismantle_faction"]),
    tension(-3), coh(-5)])
F("na_join_the_movement", "Join the Non-Aligned Movement", "na", "na_the_third_way_economy,na_dissolve_the_pact", c=5, e=[
    cw_join("na", "Cold War: Wechsel zu den Blockfreien"), op("RAJ", 20, key="COLDWAR_SOV_third_way")])

# ================================================================== NATIONALIST
F("nt_molodaya_gvardiya", "Molodaya Gvardiya", "nt", "dir_the_russian_idea", c=5, e=[outl(4, 3), coh(-2)],
  n="Die Zeitschrift der „Russischen Partei“ im Komsomol-Verlag.")
F("nt_the_victory_cult", "The Cult of Victory", "nt", "dir_the_russian_idea", c=5, h=1, e=[outl(4, 2), ws(3), fac("the_military", 5)],
  n="Mamajew-Kurgan, Ewige Flammen, der 9. Mai als Staatsreligion.")
F("nt_vozrozhdenie", "Vozrozhdenie", "nt", "nt_molodaya_gvardiya,nt_the_victory_cult", c=5, e=[outl(4, 5), coh(-3)])
for i in (20, 21, 22, 23):
    power_to(i, "nt", "nt_vozrozhdenie",
             av_extra={20: "Politbüro-Balance ≥ 0,2", 21: "nur Spieler; Stabilität < 30 %", 22: "Armee-Meinung ≥ 75 ODER Stabilität < 25 %",
                       23: "nur Spieler; „Accord with the Patriarchate“ erledigt"}[i],
             ai="0" if i in (21, 23) else "", e_extra=[coh(-8)])
F("nt_russia_first", "Russia First", "nt", av="`has_government = nationalist`", c=3, e=[
    pp(50), idea("russia_first", "Russia First", {"nationalist_drift": 0.02, "war_support_factor": 0.05}), coh(-5)])
F("nt_the_rsfsr_institutions", "Institutions for the RSFSR", "nt", "nt_russia_first", c=5, e=[
    dm("ps", {"political_power_factor": 0.03}), coh(-3)], n="Russland bekommt, was jede andere Republik hat: eigene Partei, Akademie, KGB.")
F("nt_the_army_of_the_nation", "The Army of the Nation", "nt", "nt_russia_first", c=5, e=[dm("af", {"army_morale_factor": 0.05}), ws(3)])
F("nt_the_imperial_question", "The Imperial Question", "nt", "nt_the_rsfsr_institutions,nt_the_army_of_the_nation", c=5, e=[
    txt("Im Event: Union halten (Zusammenhalt +5, Polizeikosten +10 %) oder kleinere russische Union (Republiken dürfen per Angebot austreten)")])

# ================================================================== CPSU (party 4) – common part
P4 = inpower(4)
F("cpsu_the_party_of_lenin", "The Party of Lenin", "cpsu", "power_the_cpsu|em_the_leading_role_of_the_party", av=P4, c=3, h=1, e=[
    pp(50), pm("cpsu", {"political_power_factor": 0.05, "stability_factor": 0.03, "communism_drift": 0.02, "mdcw_cw_ideological_defence": 0.05},
               name="The Party of Lenin")],
  n="Programm-Modifier wie SOV_putin_politic_modifier; entfällt per `remove_trigger`, wenn die KPdSU nicht mehr regiert.")
F("cpsu_the_nomenklatura", "The Nomenklatura", "cpsu", "cpsu_the_party_of_lenin", c=5, h=1, e=[
    fac("communist_cadres", 10), pm("cpsu", {"bureaucracy_cost_multiplier_modifier": 0.03, "political_power_factor": 0.02})])
F("cpsu_the_komsomol", "The Komsomol", "cpsu", "cpsu_the_party_of_lenin", c=5, h=1, e=[
    party(4, 3), pm("cpsu", {"war_support_factor": 0.02}), manpower(10000)])
F("cpsu_the_party_card_exchange", "The Party Card Exchange", "cpsu", "cpsu_the_nomenklatura", c=5, h=1, e=[
    pp(50), stab(2), fac("communist_cadres", -5), corr(-1)], n="1973–1974: Austausch der Parteibücher – eine stille Säuberung.")
F("cpsu_democratic_centralism", "Democratic Centralism", "cpsu", "cpsu_the_komsomol", c=5, h=1, e=[
    pm("cpsu", {"drift_defence_factor": 0.05}), bop(0.05)])
F("cpsu_the_constitution_of_developed_socialism", "Article Six", "cpsu", "cpsu_the_party_card_exchange,cpsu_democratic_centralism", c=5, h=1, e=[
    pm("cpsu", {"stability_factor": 0.02, "political_power_factor": 0.03})], n="„Die führende und lenkende Kraft der sowjetischen Gesellschaft …“")
F("cpsu_the_party_of_the_whole_people", "The Party of the Whole People", "cpsu", "cpsu_the_constitution_of_developed_socialism", c=7, h=1, e=[
    party(4, 5), coh(3), pm("cpsu", {"communism_drift": 0.02})])
