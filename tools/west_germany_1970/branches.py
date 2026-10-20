"""Deeper branches for the short paths of the West Germany 1970 tree (multiplayer roleplay).

Lafontaine, the grand coalition, the CSU as a fourth party, Chancellor Barzel, the Greens, Späth, the
party donations affairs, nuclear participation, forward defence, Strauß and Schmidt's minority government.
Same rules as before: coalitions follow the LAST election (cwger_*_share from party_pop_elect_array),
alternative-historical choices sit beside the historical ones, partner countries decide for themselves
(offers), drastic steps are for human governments only and other human players hear about them.
Events in COLDWAR_GBR.
"""
from cw_lib import *
from events_lib import E, O, gov
from tree import F, core, unlock, state_build, state_mod, opinion, infl, climate_base, STATE_MODS
from rivalry import kl, lever
from foreign import offer, news_all

EVB = "COLDWAR_GBR"
SPD = "check_variable = { ruling_party = 3 }"
UNION = "check_variable = { ruling_party = 1 }"
FDP_GOV = "is_in_array = { gov_coalition_array = 16 }"
GREEN_GOV = "OR = { check_variable = { ruling_party = 17 } is_in_array = { gov_coalition_array = 17 } }"
ERA2 = f"OR = {{ date > 1981.12.31 has_country_flag = {P}_era2 }}"
UNITY = f"has_global_flag = {P}_unity_achieved"
HUMAN = "is_ai = no"
AI0 = "modifier = { factor = 0 is_ai = yes }"
SH, NDS, NRW, RLP, HES, BW, BAY, SAAR, HH = 37, 38, 39, 40, 41, 42, 43, 967, 1080
THURINGIA, SAXONY = 545, 44

STATE_MODS.update({
    "neckar_valley": ("Silicon Valley on the Neckar", {"state_productivity_growth_modifier": 0.06, "local_building_slots": 1}),
    "jena_revival": ("Jena Reborn", {"state_productivity_growth_modifier": 0.05, "state_production_speed_buildings_factor": 0.1}),
    "fulda_gap": ("Fulda Gap Barrier Plans", {"local_building_slots": 1}),
    "wackersdorf": ("Wackersdorf", {"state_production_speed_buildings_factor": -0.05}),
})

L(f"{P}_tt_rg_majority", "SPD and Greens won more than half of the vote at the last election")
L(f"{P}_tt_cf_majority", "CDU/CSU and FDP won more than half of the vote at the last election")
L(f"{P}_tt_sl_majority", "SPD and FDP won more than half of the vote at the last election")
RG_MAJ = f"custom_trigger_tooltip = {{ tooltip = {P}_tt_rg_majority check_variable = {{ cwger_rg_share > 0.5 }} }}"
CF_MAJ = f"custom_trigger_tooltip = {{ tooltip = {P}_tt_cf_majority check_variable = {{ cwger_cf_share > 0.5 }} }}"
SL_MAJ = f"custom_trigger_tooltip = {{ tooltip = {P}_tt_sl_majority check_variable = {{ cwger_sl_share > 0.5 }} }}"

_n = [0]


def ev(title, desc, opts, pic="GFX_german_parliament", days=5, imm=""):
    _n[0] += 1
    evid = f"{EVB}.{_n[0]}"
    E(evid, title, desc, pic, opts, imm=imm)
    return f"country_event = {{ id = {evid} days = {days} }}"


# =========================================================================== LAFONTAINE
F("mannheim_congress", "chancellery", 6, 12, cost=2, pre=[], icon="spd2", name="The Mannheim Party Congress",
  desc="The SPD has lost four federal elections in a row and drifts somewhere around thirty per cent, its chairman respected and unloved. Mannheim was meant to be a routine party congress. Then the Saarland's premier steps up to the lectern: 'There are still causes we can be enthusiastic about.' The delegates rise - and the party has to decide who leads it into the next election.",
  avail=f"NOT = {{ {SPD} }} date > 1990.1.1",
  bypass=f"OR = {{ check_variable = {{ cwger_spd_leader = 5 }} check_variable = {{ cwger_spd_leader = 8 }} }}",
  reward=ev("Mannheim",
            "Twenty minutes of standing ovation. Oskar Lafontaine had not announced a candidacy; now the delegates demand one. Rudolf Scharping, the chairman, sits on the podium and knows that a vote tomorrow would be a vote of no confidence. In the corridors the Lower Saxony delegation counts heads for its own man - Gerhard Schröder, who wants the chancellorship more than the party.",
            [O("Lafontaine takes the party.", J("set_variable = { cwger_spd_leader = 5 }", party("spd", 0.01), faction("dgb", 5), faction("bdi", -4)), ai=60),
             O("Scharping holds on - the left is told to wait.", J(party("spd", -0.004), v("cwger_fdp_course", 3)), ai=40)],
            pic="GFX_election_day"))
F("ecological_restructuring", "lafontaine_cautious_unity", -1, 1, cost=3, icon="green_projects", name="Ecological Restructuring",
  desc="'Fortschritt 90': the SPD's programme of ecological modernisation - energy taxes, environmental technology, a new industrial policy for a country that has run out of space for smokestacks.",
  reward=J(core("energie", renew=0.08, fossil=-0.03), core("modell", tax=0.01), state_build(SAAR, "renewable_energy_infra"), party("greens", -0.003), faction("bdi", -3)))
F("shorter_week", "lafontaine_cautious_unity", 1, 1, cost=3, icon="unions", name="Share the Work",
  desc="Four million unemployed and an economy that produces more with fewer people: the 35-hour week, overtime limits and part-time rights as a programme for full employment.",
  reward=J(faction("dgb", 10), faction("bdi", -8), core("modell", prod=-0.01, social=0.02), core("bonn", stab=0.02), "add_manpower = 15000"))
F("red_green_pact", "ecological_restructuring", 1, 1, cost=3, pre=[["ecological_restructuring", "shorter_week"]], icon="greens", name="A Red-Green Pact",
  desc="Lafontaine offers the Greens what Brandt never offered: a coalition of equals. The Realos are tempted; the Fundis want the end of NATO in the coalition agreement.",
  avail=f"NOT = {{ {GREEN_GOV} }}",
  reward=ev("Coalition with the Greens",
            "SPD and Greens sit down to negotiate a federal government. Whether they can form one depends on the last election - and on what each side is willing to give up.",
            [O("Form a red-green government.", J(gov(3, [17]), f"{P}_refresh_leader = yes", party("greens", 0.003), core("energie", renew=0.05)), trig=RG_MAJ, ai=70),
             O("Without a majority: a pact for the next election.", J(party("spd", 0.004), party("greens", 0.004), party("fdp", -0.003)), ai=30)],
            pic="GFX_joschka_fischer_event"))
F("wealth_tax", "red_green_pact", -1, 1, cost=3, mutex=["bundesbank_truce"], icon="market", name="Tax the Rich",
  desc="A wealth tax, a higher top rate and an end to the capital gains loopholes: the money for the East and for the jobs programme is to come from those who have it.",
  reward=J("set_temp_variable = { pop_change = 2 }", "modify_population_tax_rate_effect = yes", money_gdp(0.004), faction("bdi", -10), faction("dgb", 6),
           v("cwger_bundesbank", 8), party("fdp", 0.003)))
F("bundesbank_truce", "red_green_pact", 1, 1, cost=2, mutex=["wealth_tax"], icon="euro", name="A Truce with Frankfurt",
  desc="The finance minister makes his peace with the Bundesbank: no more public demands for lower interest rates, no more 'Lafontaine, the most dangerous man in Europe' on the front page of The Sun.",
  reward=J(v("cwger_bundesbank", -12), core("modell", tax=0.01), faction("bdi", 4), party("spd", -0.002)))
F("european_employment_pact", "wealth_tax", 1, 1, cost=3, pre=[["wealth_tax", "bundesbank_truce"]], icon="europe", name="A European Employment Pact",
  desc="Keynes on a continental scale: coordinated wages, public investment and lower interest rates across the Community - if Paris joins in.",
  reward=offer("employment_pact", "FRA", "A European Employment Pact",
               "Bonn proposes a European employment pact: coordinated public investment, wage policy and pressure on the central banks for lower interest rates.",
               J(core("modell", fac=0.02, social=0.02), core("west", europe=0.03), faction("dgb", 6), v("cwger_bundesbank", 6)),
               partner_eff="add_stability = 0.02", accept="Paris signs up.", refuse="Paris prefers its own plans.", pic="GFX_european_parliament"))

# =========================================================================== THE GRAND COALITION
F("two_thirds_reforms", "grand_coalition", -1, 1, cost=3, icon="constitution", name="The Power of Two Thirds",
  desc="Together the two big parties hold the two-thirds majority that every constitutional amendment needs. What they agree on, nobody can stop.",
  reward=J(core("bonn", pp=0.05), pp(50), tt(f"{P}_tt_gc_2_3", "While the grand coalition governs, amendments to the Basic Law are within reach without paying the opposition's price.")))
F("finance_reform", "two_thirds_reforms", -1, 1, cost=3, icon="market", name="Reforming the Federal Finances",
  desc="Joint tasks, a fiscal equalisation that the rich Länder hate and the poor ones need: the grand coalition untangles who pays for what.",
  reward=J(core("bonn", bureau=-0.05), v("cwger_bundesrat_union", -3), money_gdp(0.002), v("cwger_csu_autonomy", 3)))
F("concerted_action_revived", "two_thirds_reforms", 1, 1, cost=2, icon="unions", name="Concerted Action Revived",
  desc="Schiller's round table returns: the unions, the employers, the Bundesbank and both coalition partners agree on wages, prices and investment.",
  reward=J(faction("dgb", 6), faction("bdi", 6), v("cwger_bundesbank", -5), core("modell", prod=0.01), core("bonn", stab=0.02)))
F("small_parties_rise", "finance_reform", 1, 1, cost=2, pre=[["finance_reform", "concerted_action_revived"]], icon="election", name="The Opposition Outside Parliament",
  desc="With both big parties in government, opposition happens elsewhere: in the streets, in the small parties, at the edges.",
  reward=ev("The Edges Grow",
            "Polls show the small parties rising: the FDP as the only liberal opposition, the Greens or the far left among students, the NPD among the disappointed. The coalition must decide how to answer.",
            [O("Answer with reforms the voters can see.", J(core("bonn", stab=0.02), money_gdp(-0.002), party("fdp", 0.003)), ai=50),
             O("Answer with a tougher line on extremists.", J(party("npd", -0.003), v("cwger_security", 3), v("cwger_rechtsstaat", -2)), ai=30),
             O("Ignore them - they will fade.", J(party("npd", 0.004), party("greens", 0.003), protest(3)), ai=20)],
            pic="GFX_politics_protest"))
F("renew_grand_coalition", "small_parties_rise", -1, 1, cost=3, mutex=["end_grand_coalition"], icon="parliament", name="Renew the Grand Coalition",
  desc="Another four years together. The country is governed calmly - and the parties begin to look alike.",
  reward=J(core("bonn", stab=0.04, drift=0.03), party("cdu", -0.003), party("spd", -0.003), party("fdp", 0.003), party("greens", 0.003)))
F("end_grand_coalition", "small_parties_rise", 1, 1, cost=3, mutex=["renew_grand_coalition"], icon="confidence", name="Each to Its Own Camp",
  desc="Enough of the marriage of convenience. The chancellor's party looks for a smaller partner - if the last election allows one.",
  reward=ev("The End of the Grand Coalition",
            "The coalition committee meets for the last time. The chancellor's party can try a smaller coalition - but only if the numbers from the last election are there.",
            [O("A Christian-liberal coalition.", J(gov(1, [16]), f"{P}_refresh_leader = yes", party("cdu", 0.003)), trig=f"{UNION} {CF_MAJ}", ai=50),
             O("A social-liberal coalition.", J(gov(3, [16]), f"{P}_refresh_leader = yes", party("spd", 0.003)), trig=f"{SPD} {SL_MAJ}", ai=50),
             O("No majority without them. Call an election.", "country_event = { id = COLDWAR_GER.23 days = 1 }", ai=20)],
            pic="GFX_german_parliament_bundestag"))

# =========================================================================== THE CSU AS A FOURTH PARTY
F("csu_land_parties", "cdu_centre_course", -1, 1, cost=3, icon="cdu", name="The CSU in Every Land",
  desc="'Freundeskreise' become Land associations: the CSU stands in Hesse, Lower Saxony, Baden-Württemberg - wherever the CDU is too soft for Strauß.",
  reward=J(v("cwger_csu_autonomy", 10), party("cdu", 0.004), party("rep", -0.004), party("npd", -0.003), core("bonn", stab=-0.02)))
F("cdu_in_bavaria", "cdu_centre_course", 1, 1, cost=3, icon="cdu", name="The CDU in Bavaria",
  desc="If the CSU marches north, the CDU marches south: a Bavarian Land association, candidates in every constituency between Hof and Lindau.",
  reward=J(v("cwger_csu_autonomy", -5), party("cdu", -0.002), core("bonn", drift=0.02), stab(-0.01)))
F("sister_war", "csu_land_parties", 1, 1, cost=2, pre=[["csu_land_parties", "cdu_in_bavaria"]], icon="confidence", name="The War of the Sisters",
  desc="Two Christian parties competing for the same voters: the left smiles, the FDP rejoices, and the Union's joint parliamentary group is about to break up.",
  reward=ev("Kreuth, Again",
            "The two Union parties face each other at the conference table in Wildbad Kreuth. They can make peace on new terms - or go their separate ways for good.",
            [O("A non-aggression pact: separate parties, one parliamentary group.", J(v("cwger_csu_autonomy", 5), party("cdu", 0.004), core("bonn", stab=0.02)), ai=60),
             O("Separate groups, separate campaigns.", J(v("cwger_csu_autonomy", 15), party("cdu", -0.004), party("rep", -0.004), party("fdp", 0.003), protest(2)), ai=30),
             O("The CSU returns to Bavaria.", J(v("cwger_csu_autonomy", -15), core("bonn", stab=0.03)), ai=10)],
            pic="GFX_flag_cdu"))
F("strauss_of_the_right", "sister_war", 0, 1, cost=3, icon="cdu", name="A Home on the Right",
  desc="'There must be no democratically legitimate party to the right of the CSU' - Strauß's maxim, applied nationwide.",
  reward=J(party("rep", -0.006), party("npd", -0.004), v("cwger_terror_right", -3), core("west", ideo=0.03), v("cwger_dark", -10)))

# =========================================================================== CHANCELLOR BARZEL
F("barzel_eastern_treaties", "barzel_social_market", -1, 1, cost=3, icon="treaty", name="The Treaties with Reservations",
  desc="Barzel will not tear up Brandt's treaties - but he will sign them only with a resolution that keeps the German question open.",
  reward=J(f"set_country_flag = {P}_treaties_with_reservations", lever("recht", 1), kl(-3), opinion("SOV", "small_decrease"), party("cdu", 0.003)))
F("barzel_property", "barzel_social_market", 1, 1, cost=3, icon="market", name="Property for Workers",
  desc="Every employee a small capitalist: savings premiums, shares in the company, the 'investment wage' the Union's labour wing has wanted since the 1950s.",
  reward=J(faction("dgb", 4), faction("bdi", 2), core("modell", cg=-0.01, social=0.01), core("bonn", stab=0.02), money_gdp(-0.001)))
F("barzel_majority", "barzel_eastern_treaties", 1, 1, cost=2, pre=[["barzel_eastern_treaties", "barzel_property"]], icon="confidence", name="The Fight for the Majority",
  desc="Barzel governs with a handful of defectors from the SPD and FDP. Every vote could be the last.",
  reward=ev("Two Votes",
            "Two deputies are rumoured to be wavering - and the Stasi's money has found its way to Bonn before. The chancellor must decide how to secure his majority.",
            [O("Call an election and win a mandate of our own.", "country_event = { id = COLDWAR_GER.23 days = 1 }", ai=40),
             O("Win over the FDP: a Christian-liberal coalition.", J(gov(1, [16]), f"{P}_refresh_leader = yes", v("cwger_fdp_course", 8)), trig=CF_MAJ, ai=50),
             O("Govern on, vote by vote.", J(core("bonn", pp=-0.03), v("cwger_scandal", 5)), ai=10)],
            pic="GFX_german_parliament_bundestag"))
F("barzel_europe", "barzel_majority", 0, 1, cost=3, icon="europe", name="Barzel's Europe",
  desc="A political union of Western Europe as the frame in which the German question can one day be answered: Barzel's alternative to Brandt's Ostpolitik.",
  reward=J(core("west", europe=0.03, opinion=0.03), infl("FRA", 2), infl("ITA", 2), europe(3)))

# =========================================================================== THE GREENS
F("first_green_minister", "red_green_hesse", -1, 1, cost=2, icon="greens", name="Sneakers in the Ministry",
  desc="December 1985: Joschka Fischer takes the oath as Hesse's environment minister in white trainers. The Greens have arrived in power - and must now govern.",
  reward=ev("The First Green Minister",
            "Fischer's first months in Wiesbaden: the Hanau nuclear fuel plants, the chemical industry, a coalition partner that wants jobs. The party base watches every compromise.",
            [O("Govern pragmatically.", J(party("greens", 0.003), core("energie", renew=0.03), faction("bdi", 2)), ai=60),
             O("Close Hanau - whatever the cost.", J(core("energie", nuclear=-0.05), v("cwger_anti_nuclear", -6), faction("bdi", -5), stab(-0.01)), ai=40)],
            pic="GFX_joschka_fischer_event"))
F("rotation_principle", "fundis", 0, 1, cost=2, icon="greens", name="The Rotation Principle",
  desc="No professional politicians: every Green deputy gives up the seat after two years. Grassroots democracy - and a parliamentary group that never learns the job.",
  reward=J(party("greens", 0.002), core("bonn", drift=-0.02), v("cwger_peace_movement", 3)))
F("green_unilateralism", "rotation_principle", 0, 1, cost=3, icon="pacifists", name="Swords into Ploughshares",
  desc="The Greens demand unilateral disarmament, the withdrawal of all nuclear weapons and an end to the blocs. Their Bundestag group tables the motions every month.",
  reward=J(v("cwger_peace_movement", 10), party("greens", 0.004), opinion("USA", "small_decrease"), kl(3), core("armee", plan=-0.03)))
F("greens_merge", "greens_parliament", 0, 2, cost=3, pre=[["realos", "fundis"]], icon="greens", name="Alliance 90/The Greens",
  desc="1993: the West German Greens merge with the East German civil rights movement Alliance 90. The party of 1968 meets the people of 1989.",
  avail=UNITY,
  reward=J(party("greens", 0.006), core("bonn", drift=0.02), party("pds", -0.002)))
F("bielefeld_congress", "greens_merge", 0, 1, cost=3, icon="kosovo", name="Bielefeld, 1999",
  desc="A paint bomb hits the foreign minister's ear. The party of peace must decide whether a Green government may send the Luftwaffe to war against Serbia.",
  avail=f"{GREEN_GOV} date > 1998.6.1",
  reward=ev("The Bielefeld Party Congress",
            "Delegates shout 'warmonger'. Fischer, his ear bleeding, speaks of Auschwitz and Srebrenica. The vote decides whether the coalition survives.",
            [O("The party follows its foreign minister.", J(party("greens", -0.004), core("armee", xp=0.02), opinion("USA", "medium_increase"), v("cwger_peace_movement", 4)), ai=70),
             O("The party says no - the coalition breaks.", J(party("greens", 0.002), v("cwger_peace_movement", -6), "country_event = { id = COLDWAR_GER.23 days = 30 }"), ai=30)],
            pic="GFX_joschka_fischer_event"))

# =========================================================================== SPÄTH
F("neckar_valley", "spaeth_slow_unity", -1, 1, cost=3, icon="research", name="Silicon Valley on the Neckar",
  desc="Research institutes, technology parks, venture capital from the Landesbank: Baden-Württemberg as Germany's answer to California.",
  reward=J(state_mod(BW, "neckar_valley"), state_build(BW, "offices"), tech("CAT_computing", 0.5, 1), core("modell", prod=0.02)))
F("laender_partnership", "spaeth_slow_unity", 1, 1, cost=2, icon="unified", name="Partners in the East",
  desc="Baden-Württemberg adopts Saxony: civil servants, judges and engineers on loan, a partnership treaty between the Länder.",
  avail=f"OR = {{ {UNITY} has_global_flag = {P}_wall_open }}",
  reward=J(v("cwger_east_burden", -5), f"if = {{ limit = {{ {SAXONY} = {{ is_owned_by = ROOT }} }} {state_build(SAXONY, 'offices')} }}", core("bonn", stab=0.01)))
F("jena_revival", "neckar_valley", 1, 1, cost=3, pre=[["neckar_valley", "laender_partnership"]], icon="research", name="Jenoptik",
  desc="Späth goes east himself: he turns the remains of Carl Zeiss Jena into a technology company that survives the Treuhand.",
  avail=UNITY,
  reward=J(f"if = {{ limit = {{ {THURINGIA} = {{ is_owned_by = ROOT }} }} {state_mod(THURINGIA, 'jena_revival')} {state_build(THURINGIA, 'industrial_complex')} }}",
           v("cwger_east_burden", -6), core("modell", prod=0.01)))
F("spaeth_chancellor", "jena_revival", 0, 1, cost=3, icon="cdu", name="The Bremen Putsch",
  desc="September 1989: the CDU's reformers want Späth instead of Kohl. Historically, they lost the nerve at the Bremen party congress. Here they need not.",
  avail=f"{UNION} NOT = {{ check_variable = {{ cwger_cdu_leader = 5 }} }}",
  reward=ev("Bremen",
            "The delegates wait for the challenger to declare. Kohl has counted the votes; the reformers have counted the polls.",
            [O("Späth challenges - and wins.", J("set_variable = { cwger_cdu_leader = 5 }", f"{P}_refresh_leader = yes", party("cdu", 0.006), stab(-0.02)), ai=40),
             O("The challenge collapses. Kohl remains.", J(party("cdu", -0.002), core("bonn", pp=0.02)), ai=60)],
            pic="GFX_flag_cdu"))

# =========================================================================== THE DONATIONS AFFAIRS
F("donations_committee", "party_finance_law", -1, 1, cost=2, icon="cryptography", name="The Committee of Inquiry",
  desc="The Bundestag's committee summons party treasurers, accountants and two former ministers. The Greens ask the questions; everyone else hopes for short memories.",
  reward=J(v("cwger_scandal", -5), v("cwger_rechtsstaat", 3), party("greens", 0.002), pp(-25)))
F("black_accounts", "donations_committee", 1, 1, cost=3, icon="dangerous_deal", name="Black Accounts",
  desc="Cash in suitcases, accounts in Liechtenstein, 'Jewish legacies' that never existed. A former chancellor refuses to name the donors - his 'word of honour'.",
  avail="date > 1990.1.1",
  reward=ev("The Word of Honour",
            "The prosecutors, the press and the party's own young leaders demand the names. The old chancellor says he gave his word.",
            [O("The party breaks with its past.", J(v("cwger_scandal", -15), v("cwger_rechtsstaat", 5), party("cdu", -0.006), core("bonn", stab=-0.01)), ai=60),
             O("Close ranks behind the old man.", J(v("cwger_scandal", 15), v("cwger_rechtsstaat", -5), party("cdu", -0.004), corruption(True, 60)), ai=40)],
            pic="GFX_investigation_schreiber_kiep"))
F("transparency_act", "party_finance_law", 1, 1, cost=3, icon="parliament", name="The Transparency Act",
  desc="Every donation above 10,000 marks published within a month, cash donations banned, criminal penalties for false accounts.",
  reward=J(v("cwger_scandal", -10), corruption(False), core("bonn", stab=0.02), party("fdp", 0.002)))

# =========================================================================== NUCLEAR PARTICIPATION
F("npg_seat", "nuclear_sharing_role", -1, 1, cost=2, icon="nato", name="A Seat in the Nuclear Planning Group",
  desc="Bonn has no bomb, but a voice: in NATO's Nuclear Planning Group German ministers discuss target lists on German soil.",
  reward=J(core("armee", plan=0.05), core("west", ideo=0.02), opinion("USA", "small_increase")))
F("dual_key", "npg_seat", 0, 1, cost=3, icon="nuclear", name="Two Keys",
  desc="The Pershing Ia missiles are German; the warheads are American. One key each - and a debate over who turns his first.",
  reward=J(core("armee", plan=0.05), ws(0.02), v("cwger_peace_movement", 4), opinion("SOV", "small_decrease")))
F("chemical_free_zone", "npg_seat", 2, 1, cost=3, mutex=["national_option"], icon="truce", name="A Zone Free of Chemical Weapons",
  desc="1985: the SPD and the SED draft a treaty for a Central Europe free of chemical weapons - an opposition party negotiating with a foreign government. Here, a government makes it its policy.",
  avail="country_exists = DDR date > 1980.1.1",
  reward=offer("cw_zone", "DDR", "A Zone Free of Chemical Weapons",
               "Bonn proposes a treaty between the two German states: no chemical weapons on German soil, verified by mutual inspections.",
               J(tension(-3), kl(6), climate_base(2), v("cwger_peace_movement", -5), opinion("USA", "small_decrease")),
               partner_eff="add_stability = 0.02", accept="The GDR signs.", refuse="Moscow decides such questions.", pic="GFX_politics_talks"))
def sp_progress(project, ratio):
    """MD special projects: advance a project that is not yet finished."""
    return f"if = {{ limit = {{ NOT = {{ is_special_project_completed = sp:{project} }} }} sp:{project} = {{ add_project_progress_ratio = {ratio} }} }}"


L(f"{P}_tt_enrich_nuclear", "Builds an §Yenrichment facility§! (needs nuclear technology - otherwise the nuclear energy project advances instead).")
F("gronau_enrichment", "national_option", 0, 1, cost=3, ai=0, ai_mod=AI0, avail=HUMAN, icon="nuclear_science", name="Centrifuges at Gronau",
  desc="The enrichment plant in Gronau is civilian - officially. A few cascades more, a few inspectors less, and the Federal Republic would be months from weapons-grade uranium.",
  reward=J(f"custom_effect_tooltip = {P}_tt_enrich_nuclear",
           "if = { limit = { has_tech = nuclear_technology } hidden_effect = { set_temp_variable = { skip_payment = 1 } one_random_enrichment_facility = yes set_temp_variable = { skip_payment = 0 } } }",
           f"else = {{ {sp_progress('sp_nuclear_energy', 0.3)} }}",
           "set_temp_variable = { skip_payment = 1 }", "one_random_nuclear_facility = yes", "set_temp_variable = { skip_payment = 0 }",
           money_gdp(-0.002), v("cwger_westbindung", -5), opinion("USA", "medium_decrease"), opinion("FRA", "small_decrease"),
           tension(3), news_all("Questions about Gronau", "Western intelligence services report that West Germany's uranium enrichment at Gronau is expanding beyond civilian needs.", "GFX_nuclear_power_plant")))
F("german_bomb", "gronau_enrichment", 0, 1, cost=7, ai=0, ai_mod=AI0, avail=f"{HUMAN} NOT = {{ has_country_flag = {P}_npt_ratified }}", icon="nuclear", name="A German Bomb Programme",
  desc="The taboo of 1945 breaks. Engineers from Karlsruhe and Jülich, a test site that does not yet exist, and a question every government from Washington to Moscow will ask: what is a German bomb for?",
  reward=J("clr_country_flag = GER_no_nuclear", f"set_country_flag = {P}_bomb_programme",
           tt(f"{P}_tt_bomb_lift", "The Federal Republic no longer renounces nuclear weapons: the §Ynuclear weapon special projects§! become available."),
           sp_progress("sp_nuclear_energy", 0.25), sp_progress("sp_nuclear_bomb", 0.3), sp_progress("sp_nuclear_warhead_program", 0.1),
           "set_temp_variable = { skip_payment = 1 }", "one_random_air_facility = yes", "set_temp_variable = { skip_payment = 0 }",
           "add_tech_bonus = { name = " + P + "_bomb_bonus bonus = 0.5 uses = 2 category = CAT_nuclear_weapons }",
           money_gdp(-0.006), v("cwger_westbindung", -15), protest(10), v("cwger_peace_movement", 15), tension(5),
           opinion("USA", "medium_decrease"), opinion("SOV", "medium_decrease"), opinion("FRA", "medium_decrease"),
           news_all("A German Bomb Programme", "Leaks from Bonn suggest that the Federal Republic has begun a nuclear weapons programme. Washington, Moscow, London and Paris demand explanations.", "GFX_nuclear_power_plant"),
           tt(f"{P}_tt_german_bomb", "§RWhen the nuclear bomb project is completed§!, Washington, Moscow, London and Paris will have to decide how to answer a German finger on the trigger - with sanctions, with isolation, or with the threat to disarm the Federal Republic by force.")))
L(f"{P}_bomb_bonus", "German bomb programme")
EXTRA_BOMB = f"""
# Monthly, GER scope: the world reacts when the German bomb project is finished.
{P}_bomb_watch = {{
	if = {{ limit = {{ has_country_flag = {P}_bomb_programme NOT = {{ has_global_flag = {P}_german_bomb }} is_special_project_completed = sp:sp_nuclear_bomb }}
		set_global_flag = {P}_german_bomb
		add_to_variable = {{ cwger_westbindung = -10 }}
		clamp_variable = {{ var = cwger_westbindung min = 0 max = 100 }}
		if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} set_temp_variable = {{ mdcw_cw_tension_delta = 10 }} mdcw_cw_add_tension = yes }}
		every_other_country = {{ limit = {{ OR = {{ original_tag = USA original_tag = SOV original_tag = FRA original_tag = ENG }} }} country_event = {{ id = {EVB}.90 days = 1 }} }}
		{news_all("Germany Has the Bomb", "The Federal Republic of Germany has completed its first nuclear weapon. Twenty-five years of non-proliferation diplomacy lie in ruins.", "GFX_nuclear_power_plant")}
	}}
}}
"""
from events_lib import EXTRA_EFFECTS as _EE
_EE.append(EXTRA_BOMB)
E(f"{EVB}.90", "Germany Has the Bomb",
  "Bonn has built a nuclear weapon. Every agreement since 1954 - the renunciation of ABC weapons, the Non-Proliferation Treaty, the Four Powers' rights - is being tested. The government must decide how to answer.",
  "GFX_nuclear_power_plant",
  [O("Sanctions until the programme is dismantled.", J("add_opinion_modifier = { target = GER modifier = large_decrease }", f"GER = {{ {P}_sanction_prev_economic = yes }}"), ai="base = 70"),
   O("Prepare to disarm Germany by force.", J("create_wargoal = { type = topple_government target = GER }", "add_war_support = 0.1",
                                              "add_opinion_modifier = { target = GER modifier = large_decrease }"),
     ai="base = 0", trig="is_ai = no", tt="§RCreates a war goal against the Federal Republic.§! Whoever chooses this is prepared to fight a nuclear power in the heart of Europe."),
   O("Accept it - quietly.", "add_opinion_modifier = { target = GER modifier = medium_decrease }", ai="base = 30")],
  scope="ANY")

# =========================================================================== FORWARD DEFENCE
F("fulda_barrier", "forward_defence", -1, 1, cost=3, icon="tank_wall", name="Barrier Plans for the Fulda Gap",
  desc="Prepared demolition shafts in every bridge and road near the border, barrier materials in depots, plans to flood the valleys - and never, officially, a fortification.",
  reward=J(state_mod(HES, "fulda_gap"), state_mod(BAY, "fulda_gap"), core("armee", core=0.05), kl(-2),
           core("armee", plan=0.03)))
F("reforger", "forward_defence", 1, 1, cost=3, icon="usa", name="REFORGER",
  desc="Return of Forces to Germany: every autumn tens of thousands of American soldiers fly in, collect their tanks from depots and practise the defence of the border.",
  reward=offer("reforger", "USA", "A Larger REFORGER Exercise",
               "Bonn proposes to make the annual REFORGER exercise larger and closer to the inner-German border, with German divisions under American corps command.",
               J("army_experience = 15", core("armee", xp=0.02, plan=0.03), kl(-4), tension(1)),
               partner_eff="army_experience = 10", accept="The Army is coming.", refuse="The budget does not allow it.", pic="GFX_news_german_army"))
F("wintex", "prepare_defence_case", 0, 1, cost=3, icon="home_stretch", name="WINTEX",
  desc="Every two years the government, the Joint Committee and NATO rehearse the state of defence in bunkers under the Ahr valley - including the release of nuclear weapons.",
  reward=J(core("armee", plan=0.05, org=0.02), core("bonn", stab=-0.01), v("cwger_peace_movement", 3)))
F("civil_defence", "wintex", -1, 1, cost=3, mutex=["peace_dividend_defence"], icon="reserve", name="Civil Defence",
  desc="Shelters under schools and underground stations, sirens on every roof, iodine tablets in every town hall. The peace movement calls it preparing for the unthinkable.",
  reward=J(money_gdp(-0.002), core("armee", core=0.05), ws(0.03), v("cwger_peace_movement", 5)))
F("peace_dividend_defence", "wintex", 1, 1, cost=2, mutex=["civil_defence"], icon="pacifists", name="Defensive Defence",
  desc="'Structural inability to attack': fewer tanks, more anti-tank infantry and barriers - an army the other side cannot read as a threat.",
  avail="date > 1980.1.1",
  reward=J(core("armee", core=0.05, equip=-0.05), kl(5), climate_base(2), v("cwger_peace_movement", -6), opinion("SOV", "small_increase")))

# =========================================================================== STRAUSS
F("strauss_moscow_flight", "strauss_east_credit", 0, 1, cost=3, icon="soviet", name="Strauß Flies to Moscow",
  desc="December 1987: the Bavarian premier pilots his own Cessna through a snowstorm to Moscow. The anti-communist of the 1950s meets Gorbachev - and is impressed.",
  avail="country_exists = SOV date > 1985.1.1",
  reward=offer("strauss_moscow", "SOV", "A Visit from Strauß",
               "The Bavarian premier and former defence minister asks for a meeting with the General Secretary: trade, Bavarian industry, and a message from the Western conservatives.",
               J(opinion("SOV", "medium_increase"), kl(3), core("welt", market=0.02), v("cwger_csu_autonomy", 3)),
               partner_eff="add_political_power = 25", accept="Let him land.", refuse="Not this man.", pic="GFX_politics_talks"))
F("wackersdorf", "strauss_aerospace", 0, 1, cost=3, icon="nuclear_plant", name="Wackersdorf",
  desc="A reprocessing plant for plutonium in the Upper Palatinate - Strauß's prestige project, and the scene of the fiercest battles the anti-nuclear movement ever fought.",
  avail="date > 1981.1.1",
  reward=ev("The Battle of Wackersdorf",
            "Tens of thousands camp in the forest around the construction site; police use CS gas from helicopters. Austria protests, and the energy companies begin to doubt.",
            [O("Build it - Bavaria does not give way.", J(state_mod(BAY, "wackersdorf"), core("energie", nuclear=0.05), v("cwger_anti_nuclear", 10), protest(10), v("cwger_rechtsstaat", -3)), ai=50),
             O("Abandon it - reprocess in France instead.", J(core("energie", nuclear=-0.02), v("cwger_anti_nuclear", -8), opinion("FRA", "small_increase"), v("cwger_csu_autonomy", -3)), ai=50)],
            pic="GFX_nuclear_power_plant"))

# =========================================================================== SCHMIDT'S MINORITY GOVERNMENT
F("schmidt_alone", "schmidt_snap_election", 0, 1, cost=2, icon="spd", name="Governing Without a Majority",
  desc="The FDP has left; the chancellor governs with the SPD alone, from vote to vote, until the Bundestag either backs him or replaces him.",
  reward=ev("Seventeen Days",
            "The opposition prepares a constructive vote of no confidence; the chancellor prepares an answer. Whoever moves first sets the terms.",
            [O("Ask for a vote of confidence and lose it on purpose.", "country_event = { id = COLDWAR_GER.23 days = 1 }", ai=50),
             O("Seek a tolerance pact with the Greens.", J(party("greens", 0.003), core("energie", renew=0.03), v("cwger_peace_movement", -3), stab(-0.01)),
               trig=f"check_variable = {{ party_pop_elect_array^17 > 0.0499 }}", ai=30),
             O("Govern on and dare them.", J(core("bonn", pp=0.03), stab(-0.02)), ai=20)],
            pic="GFX_german_parliament_bundestag"))
F("schmidt_legacy", "schmidt_alone", 0, 1, cost=3, icon="speech", name="The Statesman's Farewell",
  desc="Whatever happens in the Bundestag, the chancellor uses his last months for what he does best: the economy of the world, the security of Europe, a speech that both sides quote for years.",
  reward=J(core("welt", support=0.05), core("west", opinion=0.03), party("spd", 0.004), opinion("USA", "small_increase"), opinion("FRA", "small_increase")))


# =========================================================================== THE NEW CENTRE (after Mannheim)
import tree as _tree
_lk = _tree.BY_KEY["lafontaine_keynes"]
_lk.update(rel="mannheim_congress", dx=0, dy=1, ax=_tree.BY_KEY["mannheim_congress"]["ax"], ay=_tree.BY_KEY["mannheim_congress"]["ay"] + 1,
           pre=[["mannheim_congress"]], mutex=["candidate_from_hanover"])
NDS_T = NDS
F("candidate_from_hanover", "mannheim_congress", 3, 1, cost=3, icon="confidence", name="The Candidate from Hanover",
  desc="Gerhard Schröder once shook the railings of the chancellery in Bonn after a night out and shouted 'I want in there!'. Twenty years later he governs Lower Saxony with an absolute majority, sits on the supervisory board of Volkswagen and polls ten points ahead of his own party. The SPD does not love him. It may need him.",
  avail=f"NOT = {{ {SPD} }} date > 1990.1.1 NOT = {{ check_variable = {{ cwger_spd_leader = 5 }} }}",
  bypass="check_variable = { cwger_spd_leader = 8 }",
  reward=ev("The Troika",
            "Chairman, parliamentary leader and the premier of Lower Saxony pose for the photographers in Bonn, arms linked, smiles fixed. Behind the smiles one question: who will the party put on the posters? The Lower Saxony state election is two months away, and Schröder has announced that a single per cent lost will end his ambitions.",
            [O("Schröder is the candidate.", J("set_variable = { cwger_spd_leader = 8 }", party("spd", 0.008), party("cdu", -0.003), faction("bdi", 4), faction("dgb", -2)), ai=60),
             O("The chairman insists on his right.", J(party("spd", -0.004), core("bonn", stab=0.01)), ai=40)],
            pic="GFX_election_day"))
F("neue_mitte", "candidate_from_hanover", 0, 1, cost=3, icon="spd", name="Die Neue Mitte",
  desc="'We will not do everything differently, but we will do many things better.' The New Centre is less a programme than a promise: modern, pragmatic, friendly to business and to the unions, impatient with the old quarrels of the left. The party grumbles. The voters in the suburbs listen for the first time in sixteen years.",
  avail=f"{SPD} check_variable = {{ cwger_spd_leader = 8 }}",
  reward=J(core("modell", prod=0.02, tax=0.01), party("spd", 0.005), party("cdu", -0.004), faction("bdi", 6), faction("dgb", -3)))
F("alliance_for_jobs", "neue_mitte", -1, 1, cost=3, icon="unions", name="The Alliance for Jobs",
  desc="Unions, employers and the government around one table in the chancellery, as in the days of Concerted Action: wage restraint in exchange for training places, early retirement in exchange for new hiring. Everybody comes. Whether anybody gives is another matter.",
  reward=ev("The Alliance for Jobs",
            "The third round in the chancellery. IG Metall wants early retirement at sixty and refuses to talk about wage guidelines; the employers' federation wants exactly that and refuses to promise a single job in return. The chancellor has invited the press for seven o'clock.",
            [O("A pact: moderate wages, more apprenticeships.", J(faction("dgb", 4), faction("bdi", 4), core("modell", prod=0.01), stab(0.02)), ai=60),
             O("The talks collapse - and everybody blames the government.", J(faction("dgb", -4), faction("bdi", -2), core("bonn", stab=-0.01), party("spd", -0.003)), ai=40)],
            pic="GFX_politics_talks"))
F("comrade_of_the_bosses", "neue_mitte", 1, 1, cost=3, icon="export", name="Comrade of the Bosses",
  desc="The chancellor rescues a bankrupt construction giant on live television, phones car executives by their first names and smokes Cohibas for the cameras. The tabloids call him 'the comrade of the bosses'. In Wolfsburg and Stuttgart, nobody minds.",
  reward=J(state_build(NDS_T, "industrial_complex"), core("modell", fac=0.02), faction("bdi", 8), faction("dgb", -5), money_gdp(-0.002), party("pds", 0.002)))
F("third_way_paper", "alliance_for_jobs", 1, 1, cost=3, pre=[["alliance_for_jobs", "comrade_of_the_bosses"]], icon="western_europe", name="Europe: The Third Way",
  desc="A joint paper with London: flexible labour markets, lower taxes for companies, a state that activates rather than provides. In Downing Street it is a manifesto for a new European social democracy. In the SPD's local branches it reads like a declaration of war.",
  reward=J(offer("third_way", "ENG", "Europe: The Third Way",
                 "The German chancellor proposes a joint declaration with the British prime minister on the future of European social democracy: modern government, flexible markets, fewer subsidies and an 'enabling state'.",
                 J(core("west", europe=0.02, opinion=0.03), core("modell", prod=0.01), opinion("ENG", "medium_increase")),
                 partner_eff="add_political_power = 25", accept="Sign it together.", refuse="London keeps its own counsel.", pic="GFX_european_parliament"),
           ev("The Chairman Resigns",
              "A Thursday evening in March: the finance minister and party chairman resigns from every office he holds, without a word to the press, and switches off his telephone. Bonn learns about it from the news agencies. The left of the party has lost its champion - and is looking for someone to blame.",
              [O("The chancellor takes the party as well.", J(party("spd", -0.003), faction("bdi", 3), core("bonn", pp=0.02)), ai=70),
               O("Bring him back - at any price.", J(faction("dgb", 4), core("bonn", stab=-0.02), v("cwger_bundesbank", 4)), ai=30)],
              pic="GFX_german_parliament", days=30)))
F("agenda_renewal", "third_way_paper", -1, 1, cost=4, mutex=["rhineland_renewed"], icon="modernisation", name="An Agenda for Renewal",
  desc="Unemployment benefit cut to one year, the trades opened, the job centres reformed from top to bottom: the hardest cuts to the welfare state the Federal Republic has ever seen - made by a Social Democrat. The economy will thank him in ten years. His party may not wait that long.",
  reward=J(core("modell", prod=0.03, social=-0.03), faction("dgb", -10), faction("bdi", 8), party("spd", -0.008), party("pds", 0.006), protest(8)))
F("rhineland_renewed", "third_way_paper", 1, 1, cost=3, mutex=["agenda_renewal"], icon="socdem", name="The Rhineland Model Renewed",
  desc="No shock therapy: the chancellor keeps the social partnership and buys time with public money - investment in rail and schools, a training levy, early retirement paid for by the pension funds. The Federal Republic stays comfortable. It also stays slow.",
  reward=J(faction("dgb", 8), core("modell", social=0.02), stab(0.02), money_gdp(-0.004), party("spd", 0.003)))
F("chancellor_of_the_centre", "agenda_renewal", 1, 1, cost=3, pre=[["agenda_renewal", "rhineland_renewed"]], icon="chancellor", name="A Chancellor of the Centre",
  desc="He has broken with his party's dogmas, made peace with the bosses and kept the unions talking. The Social Democrats have learned to govern from the middle - at the cost of their soul, say the old comrades; at last, say the voters.",
  reward=J(core("bonn", stab=0.03, pp=0.03), party("spd", 0.004), core("west", opinion=0.02)))
