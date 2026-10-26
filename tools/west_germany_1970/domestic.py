# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Domestic policy expansion of the West Germany 1970 tree (multiplayer roleplay).

* constitutional amendments need two thirds of the Bundestag as elected (cwger_seats_gov against
  cwger_two_thirds, both from the last election); without them the player decides whether to pay
  the opposition's price or let the amendment fail - no hidden dice
* historical and alternative-historical choices sit side by side (direct democracy, a directly elected
  president, new Länder, first-past-the-post, a lower threshold, the abortion law, private television,
  the census, the party donations affair, schools, citizenship)
* events in COLDWAR_GDOM carry the decisions; a few decisions in Bonn Politics follow from the focuses
"""
from cw_lib import *
from events_lib import E, O, EXTRA_EFFECTS
from tree import F, core, unlock, state_build, state_mod, opinion, STATE_MODS
import decisions as dec

EVD_ = "COLDWAR_GDOM"
SPD = "check_variable = { ruling_party = 3 }"
UNION = "check_variable = { ruling_party = 1 }"
FDP_GOV = "is_in_array = { gov_coalition_array = 2 }"
from roster import requirement
GREEN_GOV = 'AND = { ' + requirement('greens') + ' OR = { check_variable = { ruling_party = 17 } is_in_array = { gov_coalition_array = 17 } } }'
ERA2 = f"OR = {{ date > 1981.12.31 has_country_flag = {P}_era2 }}"
SH, NDS, NRW, RLP, HES, BW, BAY, SAAR, HH = 37, 38, 39, 40, 41, 42, 43, 967, 1080

L(f"{P}_tt_two_thirds", "The government holds §Ytwo thirds§! of the Bundestag seats won at the last election")
TWO_THIRDS = f"custom_trigger_tooltip = {{ tooltip = {P}_tt_two_thirds check_variable = {{ cwger_seats_gov > cwger_two_thirds }} }}"
NO_TWO_THIRDS = f"NOT = {{ check_variable = {{ cwger_seats_gov > cwger_two_thirds }} }}"
OPPOSITION_UP = (f"if = {{ limit = {{ {SPD} }} {party('cdu', 0.01)} }} else_if = {{ limit = {{ {UNION} }} {party('spd', 0.01)} }}")

STATE_MODS.update({
    "nordstaat": ("Nordstaat", {"state_production_speed_buildings_factor": 0.1, "local_building_slots": 1}),
    "merged_land": ("Merged Land", {"state_productivity_growth_modifier": 0.03}),
})

_n = [0]


def amendment(key, title, desc, passed, failed="", pic="GFX_german_parliament_bundestag"):
    """A constitutional amendment as an event; returns the effect that fires it."""
    _n[0] += 1
    evid = f"{EVD_}.{_n[0]}"
    E(evid, title, desc + "\n\nAn amendment to the Basic Law needs two thirds of the Bundestag and of the Bundesrat.", pic,
      [O("We have the two thirds. Pass it.", J(passed, f"set_country_flag = {P}_amend_{key}"), trig=TWO_THIRDS),
       O("Pay the opposition's price for its votes.", J("add_political_power = -75", OPPOSITION_UP, passed, f"set_country_flag = {P}_amend_{key}"),
         trig=f"{NO_TWO_THIRDS} has_political_power > 74",
         tt="The opposition votes with us - and takes the credit (§Y75§! political power, the largest opposition party §R+1%§!)."),
       O("Without two thirds it cannot pass. Let it fall.", J(failed, f"set_country_flag = {P}_amend_{key}_failed"))],
      imm=f"{P}_dom_tick = yes")
    return f"country_event = {{ id = {evid} days = 7 }}"


def ev(title, desc, opts, pic="GFX_german_parliament", days=5):
    _n[0] += 1
    evid = f"{EVD_}.{_n[0]}"
    E(evid, title, desc, pic, opts)
    return f"country_event = {{ id = {evid} days = {days} }}", evid


EXTRA_EFFECTS.append(f"""
# Monthly, GER scope: the two-thirds line of the Bundestag as elected.
{P}_dom_tick = {{
	set_variable = {{ cwger_two_thirds = cwger_seats_total }}
	multiply_variable = {{ cwger_two_thirds = 0.6666 }}
	# vote shares of possible coalitions at the last election
	set_variable = {{ cwger_rg_share = cwger_parliament_shares^3 }}
	if = {{ limit = {{ {requirement("greens")} }} add_to_variable = {{ cwger_rg_share = cwger_parliament_shares^17 }} }}
	set_variable = {{ cwger_cf_share = cwger_parliament_shares^1 }}
	add_to_variable = {{ cwger_cf_share = cwger_parliament_shares^2 }}
	set_variable = {{ cwger_sl_share = cwger_parliament_shares^3 }}
	add_to_variable = {{ cwger_sl_share = cwger_parliament_shares^2 }}
}}
""")

# =========================================================================== REFORMING THE REPUBLIC
F("constitutional_reform", "chancellery", 10, 1, cost=2, icon="constitution", name="The Enquete Commission",
  desc="1970: the Bundestag sets up a commission to review the whole Basic Law after twenty years. Its report will gather dust for six years - unless a government wants to use it.",
  reward=J(core("bonn", drift=0.02), pp(25), tt(f"{P}_tt_enquete", "Amendments to the Basic Law need §Ytwo thirds§! of the Bundestag as elected. Without them we must pay the opposition's price - or let them fall.")))
_ref_ok = J(core("bonn", stab=0.03, drift=-0.05), v("cwger_rechtsstaat", 4), party("greens", 0.002),
            unlock(f"{P}_referendum_unlocked", "the decision §YPut the Question to the People§!"))
F("direct_democracy", "constitutional_reform", -1, 1, cost=3, icon="election", name="Dare More Direct Democracy",
  desc="Referendums are part of every Land constitution, but the Basic Law knows them only for redrawing borders. The memory of Weimar's plebiscites has kept them out - should it still?",
  reward=amendment("referendum", "Referendums in the Basic Law",
                   "The government asks the Bundestag to add national referendums and citizens' initiatives to the Basic Law. The Union warns of demagogues, the Greens cheer, the constitutional lawyers quote Weimar.",
                   _ref_ok, J(core("bonn", stab=-0.01), party("greens", 0.002))))
F("elected_president", "direct_democracy", 0, 1, cost=3, icon="republic", mutex=[], name="A President Elected by the People",
  desc="Since 1949 the Federal Convention has chosen the head of state. A directly elected president would have a mandate of his own - exactly what the fathers of the Basic Law feared after Hindenburg.",
  avail=f"has_country_flag = {P}_amend_referendum",
  reward=amendment("president", "Direct Election of the Federal President",
                   "The Bundestag debates a direct election of the Federal President by the people. Critics fear a 'substitute emperor'; supporters a closer bond between citizens and the state.",
                   J(core("bonn", stab=0.04, pp=0.03, drift=-0.05), pp(50), f"set_country_flag = {P}_elected_president",
                     tt(f"{P}_tt_elected_president", "A popularly elected president is a counterweight in a constitutional crisis: §Gthe Bundestag is more likely to stop an emergency government§!.")),
                   core("bonn", stab=-0.01)))
F("laender_reform", "constitutional_reform", 1, 1, cost=3, icon="borders", name="Redrawing the Länder",
  desc="The Ernst Commission (1973) proposes five or six strong Länder instead of eleven unequal ones: a Nordstaat around Hamburg, the Saar inside Rhineland-Palatinate. Article 29 even commands it - and every Land government is against it.",
  reward=ev("The Länder Reform",
            "The Ernst Commission's report lies on the table. Every option needs referendums in the Länder concerned - and the Bundesrat, where the Länder sit, must agree to its own abolition.",
            [O("The Nordstaat: Hamburg, Schleswig-Holstein and Lower Saxony together.",
               J(state_mod(SH, "nordstaat"), state_mod(NDS, "nordstaat"), state_mod(HH, "nordstaat"), core("bonn", bureau=-0.05), stab(-0.03),
                 pp(-50), f"set_country_flag = {P}_nordstaat"), ai=20),
             O("Only the small ones: the Saarland joins Rhineland-Palatinate.",
               J(state_mod(SAAR, "merged_land"), state_mod(RLP, "merged_land"), core("bonn", bureau=-0.02), stab(-0.01)), ai=40),
             O("The Länder have spoken. Leave the map as it is.", J(pp(25), v("cwger_csu_autonomy", 3)), ai=40)],
            pic="GFX_german_parliament_bundestag")[0])
F("emergency_laws_review", "laender_reform", 0, 1, cost=3, icon="civil_rights", mutex=[], name="Disarm the Emergency Laws",
  desc="The emergency constitution of 1968 brought hundreds of thousands onto the streets. A liberal majority could tie it tighter: no decrees without the Constitutional Court, no Joint Committee without the Bundesrat.",
  avail=f"NOT = {{ has_country_flag = {P}_dark_crisis }} OR = {{ {SPD} {FDP_GOV} {GREEN_GOV} }}",
  reward=amendment("emergency", "Tying the Emergency Constitution",
                   "The coalition proposes to bind every use of the emergency laws to the Federal Constitutional Court and the Bundesrat.",
                   J(v("cwger_rechtsstaat", 6), v("cwger_dark", -20), f"set_country_flag = {P}_emergency_laws_tied", v("cwger_security", -3),
                     tt(f"{P}_tt_emergency_tied", "§GAn emergency government becomes much harder: the Bundestag is more likely to stop it.§!")),
                   v("cwger_rechtsstaat", -1)))
# --- the electoral law (a simple law, but it decides who sits in the Bundestag)
F("first_past_the_post", "constitutional_reform", 3, 1, cost=3, mutex=["three_percent"], icon="election", name="First Past the Post",
  desc="The Grand Coalition promised it in 1966: British-style constituencies, and the FDP would vanish. Whoever governs with a majority of their own could finish the job - and end coalition politics for good.",
  avail=f"OR = {{ {UNION} {SPD} }} NOT = {{ {FDP_GOV} }}", ai=2,
  reward=ev("The Majority Vote",
            "The bill for a first-past-the-post system is before the Bundestag. The FDP calls it 'political murder', the small parties take to the streets, and the constitutional lawyers argue whether the Basic Law allows it at all.",
            [O("Pass it. Two parties are enough for Germany.",
               J("set_variable = { election_threshold = 0.15 }", party("fdp", -0.03), party("greens", -0.01), party("npd", -0.01),
                 core("bonn", stab=0.02, drift=0.05), v("cwger_rechtsstaat", -3), protest(4), f"set_country_flag = {P}_majority_vote",
                 tt(f"{P}_tt_fptp", "From the next election, parties need §Y15%§! to enter the Bundestag (approximating single-member constituencies).")), ai=50),
             O("Withdraw it. The price is too high.", J(pp(-25), party("fdp", 0.003)), ai=50)])[0])
F("three_percent", "constitutional_reform", 5, 1, cost=2, mutex=["first_past_the_post"], icon="greens", name="Three Percent Is Enough",
  desc="The five-percent hurdle keeps Weimar's splinter parties out - and new movements too. Lower it, and the Bundestag becomes more colourful. Some colours are welcome, others not.",
  avail=f"OR = {{ {FDP_GOV} {GREEN_GOV} date > 1979.1.1 }}", ai=2,
  reward=J("set_variable = { election_threshold = 0.03 }", party("greens", 0.004), party("npd", 0.003), party("dkp", 0.002), core("bonn", drift=-0.03),
           v("cwger_rechtsstaat", 2), tt(f"{P}_tt_3pct", "From the next election, parties need only §Y3%§! to enter the Bundestag.")))

# =========================================================================== A CHANGING SOCIETY
F("changing_society", "chancellery", 14, 1, cost=2, icon="speech", name="A Changing Society",
  desc="Long hair in the Bundestag, communes in Kreuzberg, women who want a career and not permission from their husbands. The republic of Adenauer is becoming the republic of 1968 - and not everyone likes it.",
  reward=J(core("bonn", drift=0.02), party("spd", 0.002), v("cwger_raf_milieu", -1)))
_k218, _k218_id = ev("Karlsruhe on Paragraph 218",
                     "February 1975: the Federal Constitutional Court strikes down the period solution. The state has a duty to protect unborn life, the judges rule - two of them dissent sharply.",
                     [O("We accept the ruling. An indications solution it is.",
                        J(f"set_country_flag = {P}_218_indications", party("cdu", 0.003), stab(0.01), v("cwger_rechtsstaat", 2)), ai=70),
                      O("Amend the Basic Law to overrule the court.",
                        J(amendment("abortion", "Overruling Karlsruhe",
                                    "The coalition wants to write the period solution into the Basic Law itself. The churches call for resistance.",
                                    J(f"set_country_flag = {P}_218_period", party("spd", 0.004), party("cdu", -0.004), protest(6)),
                                    J(f"set_country_flag = {P}_218_indications", stab(-0.01)))), ai=30)],
                     pic="GFX_german_parliament_bundestag", days=180)
F("paragraph_218", "changing_society", -2, 1, cost=3, icon="civil_rights", name="Paragraph 218",
  desc="'My belly belongs to me': in 1971, 374 women declare in Stern that they have had abortions. The criminal law of 1871 is now the most hotly debated paragraph in the country.",
  avail=f"date > 1971.6.1 OR = {{ {SPD} {FDP_GOV} {UNION} }}",
  reward=ev("The Abortion Law",
            "The Bundestag must choose between a period solution (no punishment in the first twelve weeks) and an indications solution (only for medical, ethical or social reasons). The churches, the women's movement and the Union all mobilise.",
            [O("The period solution.", J(party("spd", 0.004), party("fdp", 0.002), party("cdu", -0.003), protest(4), _k218), trig=f"OR = {{ {SPD} {FDP_GOV} {GREEN_GOV} }}", ai=60,
               tt="Bavaria and the Union will go to the §YConstitutional Court§!."),
             O("The indications solution.", J(f"set_country_flag = {P}_218_indications", party("cdu", 0.003), party("spd", -0.002), stab(0.01)), ai=40),
             O("Keep the old law.", J(party("cdu", 0.004), party("spd", -0.004), protest(6), v("cwger_raf_milieu", 2)), trig=UNION, ai=20)],
            pic="GFX_Demo_Generic")[0])
F("equal_rights", "paragraph_218", 0, 1, cost=2, icon="unions", name="Equal Pay, Equal Work",
  desc="The 1980 law on equal treatment at work, written because Brussels demanded it: the first time a German statute says that women and men must be paid the same.",
  avail="date > 1977.1.1",
  reward=J("add_manpower = 10000", core("modell", prod=0.01), faction("dgb", 4), party("spd", 0.002), party("greens", 0.001)))
F("comprehensive_schools", "changing_society", 0, 1, cost=3, mutex=["tripartite_schools"], icon="education", name="The Comprehensive School",
  desc="One school for all children until sixteen, instead of sorting them at ten into Gymnasium, Realschule and Hauptschule. Hesse and North Rhine-Westphalia try it; parents' associations collect millions of signatures against it.",
  reward=J(core("west", research=0.02), core("modell", prod=0.01), party("spd", 0.003), party("cdu", -0.002), protest(3), state_build(HES, "offices"), state_build(NRW, "offices")))
F("tripartite_schools", "changing_society", 2, 1, cost=3, mutex=["comprehensive_schools"], icon="education", name="Achievement Must Pay Off",
  desc="The three-tier school is Germany's pride: the Gymnasium for the few, the dual apprenticeship for the many. Bavaria and Baden-Württemberg show it works.",
  reward=J(core("modell", prod=0.02), core("bonn", stab=0.01), party("cdu", 0.003), faction("mittelstand", 4), state_build(BAY, "offices")))
F("university_framework", "comprehensive_schools", 1, 1, cost=3, pre=[["comprehensive_schools", "tripartite_schools"]], icon="research", name="The Universities Framework Act",
  desc="1976: one federal law for all universities - group universities with student votes, or professors in charge again, as the Constitutional Court demands.",
  avail="date > 1975.6.1",
  reward=J(core("west", research=0.03), v("cwger_raf_milieu", -2), tech("CAT_computing", 0.25, 1), state_build(BW, "offices")))
F("census", "university_framework", 0, 1, cost=2, icon="cryptography", name="The Census",
  desc="1983: every household is to answer the state's questions. A grassroots movement calls for a boycott - 'Only sheep let themselves be counted' - and the Constitutional Court is asked to stop it.",
  avail="date > 1982.6.1",
  reward=ev("The Census Boycott",
            "December 1983: the Constitutional Court halts the census and invents a new basic right, 'informational self-determination'. The government must decide how to count its citizens - and how much to know about them.",
            [O("A new census law with strict data protection.", J(v("cwger_rechtsstaat", 6), v("cwger_security", -2), core("wehrhaft", detect=-0.02), party("greens", -0.002),
                                                                  f"set_country_flag = {P}_data_self_determination"), ai=60),
             O("Count them anyway - with fines for boycotters.", J(v("cwger_security", 4), v("cwger_rechtsstaat", -5), protest(8), party("greens", 0.004), core("wehrhaft", detect=0.03)), ai=40)],
            pic="GFX_politics_protest")[0])
F("private_television", "changing_society", 4, 1, cost=3, mutex=["public_broadcasting"], icon="television", name="Cable and Satellite",
  desc="1984: the cable pilot project in Ludwigshafen launches the first private channel. The Union wants an end to 'red radio'; the SPD fears Berlusconi's Italy.",
  avail="date > 1982.1.1",
  reward=J(core("modell", cg=-0.01, prod=0.01), faction("bdi", 6), party("cdu", 0.003), core("bonn", drift=-0.02), state_build(RLP, "offices")))
F("public_broadcasting", "changing_society", 6, 1, cost=3, mutex=["private_television"], icon="television", name="Public Service Broadcasting",
  desc="ARD and ZDF remain the only channels: independent of the state, financed by fees, controlled by councils in which churches, unions and parties sit.",
  avail="date > 1982.1.1",
  reward=J(core("bonn", drift=0.03, stab=0.01), party("spd", 0.002), faction("dgb", 3), v("cwger_rechtsstaat", 2)))
F("citizenship_reform", "private_television", 1, 1, cost=3, pre=[["private_television", "public_broadcasting"]], mutex=[], icon="migration", name="Citizens by Birth",
  desc="Millions of children of guest workers were born in Germany and are not German. Citizenship by birthplace - and perhaps a second passport - would change that.",
  avail=f"OR = {{ date > 1990.1.1 has_completed_focus = {P}_guest_worker_policy }}",
  reward=ev("Two Passports?",
            "The government's citizenship reform reaches the Bundestag. In Hesse the Union collects signatures 'against dual citizenship' - and wins an election with them.",
            [O("Citizenship by birth and dual citizenship.", J("add_manpower = 30000", core("modell", fac=0.01), party("greens", 0.003), party("cdu", 0.004), party("rep", 0.003),
                                                               protest(4), stab(-0.02)), ai=30),
             O("Citizenship by birth - but choose one passport at 23.", J("add_manpower = 20000", core("bonn", stab=0.01), party("fdp", 0.002)), ai=50),
             O("Withdraw the bill.", J(party("cdu", 0.002), party("greens", -0.002), v("cwger_terror_right", -2)), ai=20)],
            pic="GFX_German_migrant")[0])
# --- the donations affair (event-gated, its own block)
F("flick_affair", "chancellery", 16, 12, cost=2, pre=[], icon="dangerous_deal", name="The Flick Affair",
  desc="The tax inspectors have found the Flick group's ledger: 'cultivating the political landscape', and next to it the names of almost every party treasurer in Bonn - and of two economics ministers.",
  avail=f"date > 1981.10.1 check_variable = {{ cwger_scandal > 15 }}",
  reward=ev("Cultivating the Political Landscape",
            "Prosecutors want to charge Otto Graf Lambsdorff and Hans Friderichs with corruption. The parties' leaders have prepared a quiet way out: an amnesty for all illegal party donations of the past.",
            [O("Pass the amnesty law.", J(v("cwger_scandal", 15), v("cwger_rechtsstaat", -6), party("fdp", -0.006), party("greens", 0.004), protest(6),
                                         f"set_country_flag = {P}_donations_amnesty"), ai=30,
               tt="The FDP's own deputies might revolt - and the public will not forget."),
             O("Let the prosecutors do their work.", J(v("cwger_scandal", -10), v("cwger_rechtsstaat", 5), party("fdp", -0.003), pp(-50), v("cwger_fdp_course", -5)), ai=70)],
            pic="GFX_investigation_schreiber_kiep")[0])
F("party_finance_law", "flick_affair", 0, 1, cost=3, icon="parliament", name="The Party Finance Law",
  desc="Donations above a limit must be published; parties get state money in proportion to their votes. The Greens get rich overnight.",
  reward=J(v("cwger_scandal", -10), corruption(False), party("greens", 0.002), core("bonn", stab=0.01)))

# =========================================================================== MODELL DEUTSCHLAND: WORK
F("job_creation", "housing_programme", 0, 1, cost=3, icon="unions", name="Job Creation Measures",
  desc="Two million unemployed: the Federal Labour Office pays local authorities to hire them for a year - to plant trees, renovate schools, sort archives.",
  avail="date > 1975.1.1",
  reward=J(money_gdp(-0.002), core("bonn", stab=0.02), core("modell", social=0.02), faction("dgb", 5), party("spd", 0.002)))
F("early_retirement", "job_creation", 0, 1, cost=3, mutex=["working_longer"], icon="strike", name="Early Retirement",
  desc="1984: workers can retire at 58 if their employer hires a young unemployed person instead. The unions call it solidarity between generations.",
  avail="date > 1983.1.1",
  reward=J(core("modell", social=0.03, prod=-0.01), core("bonn", stab=0.02), "add_manpower = -10000", faction("dgb", 6)))
F("working_longer", "job_creation", 2, 1, cost=3, mutex=["early_retirement"], icon="market", name="The Pension Reform of 1992",
  desc="Fewer children, longer lives: the pension age is to rise and pensions to follow net wages, not gross ones. The first reform that the opposition helps to write.",
  avail="date > 1988.1.1",
  reward=J(core("modell", social=-0.04), money_gdp(0.002), faction("dgb", -4), faction("bdi", 4), stab(-0.01)))

# =========================================================================== DECISIONS
dec.D(dec.PO, "referendum", "Put the Question to the People",
      "A national referendum on a question the Bundestag cannot settle. If the government wins, it has a mandate no opposition can question; if it loses, it has a problem.",
      "GFX_decision_elections_button", visible=f"has_country_flag = {P}_referendum_unlocked",
      available="NOT = { has_country_flag = elections_in_progress }", cost=75, re_enable=1095,
      effect=J(f"random_list = {{ 50 = {{ modifier = {{ add = 15 has_stability > 0.6 }} modifier = {{ add = -15 has_stability < 0.4 }} "
               f"country_event = {{ id = {EVD_}.90 days = 30 }} }} 50 = {{ country_event = {{ id = {EVD_}.91 days = 30 }} }} }}",
               tt(f"{P}_tt_referendum", "The vote takes a month. Higher stability makes a 'yes' more likely.")), ai=2)
E(f"{EVD_}.90", "The People Say Yes",
  "The government's proposal wins the referendum. The opposition accepts the result - it has little choice.",
  "GFX_election_day", [O("The people have spoken.", J(pp(100), stab(0.03), core("bonn", drift=0.02)))])
E(f"{EVD_}.91", "The People Say No",
  "The referendum is lost. Commentators ask whether a chancellor who loses a vote on his own question can still govern.",
  "GFX_election_day", [O("We accept the verdict.", J(pp(-50), stab(-0.03), f"if = {{ limit = {{ {SPD} }} {party('spd', -0.006)} }} else = {{ {party('cdu', -0.006)} }}"))])
dec.D(dec.PO, "federal_reform_commission", "Federal Reform Commission",
      "A joint commission of Bundestag and Bundesrat untangles who pays for what: fewer joint tasks, fewer vetoes.",
      "GFX_decision_negotiate_icon", visible=f"has_completed_focus = {P}_constitutional_reform",
      available="date > 1985.1.1", cost=60, re_enable=1460,
      effect=J(core("bonn", bureau=-0.03), v("cwger_bundesrat_union", -3), pp(30)), ai=8)
