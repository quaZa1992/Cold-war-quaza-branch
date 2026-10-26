# IMPERIA CW — Cold War: German Democratic Republic 1970 content generator.
# COLDWAR | Events of the GDR 1970 tree: the 16 focus events of the design, the system events (deaths, succession,
# Moscow's Trust, the Inner-German course, the Kremlin's say, accession, the garrison) and the historical events.
# Namespace COLDWAR_DDR. Offers (100-199) are in dg_offers.py; 900/901 are the answers to our offers.
import json
from dg_common import *
import dg_effects as E
from dg_load import LEADER_NAME, BYID

PICS = json.load(open(os.path.join(HERE, "gfxsel", "gfx_pick.json"), encoding="utf-8"))["events"]
EVENTS = []          # dicts: n, key, title, desc, pic, kind, options [(text, code, ai, trigger)], trigger, mtth, once, ttrigger, immediate
EV = {}              # key -> number
DDR_T = ["original_tag = DDR", f"has_country_flag = {PFX}initialized"]


def ev(n, key, title, desc, pic, options, **kw):
    assert n not in [e["n"] for e in EVENTS], n
    p = PICS.get(pic) or PICS.get(f"{PFX}{pic}") or pic
    EVENTS.append(dict(n=n, key=key, title=title, desc=desc, pic=p, options=options, **kw))
    EV[key] = n


def J(*parts):
    out = []
    for p in parts:
        out += p if isinstance(p, list) else [p]
    return out


def o(text, *code, ai=50, trigger=None):
    return (text, J(*code), ai, trigger or [])


def T(key, text):
    LOC[f"{PFX}{key}_tt"] = text
    return f"custom_effect_tooltip = {PFX}{key}_tt"


def eid(key):
    return f"{NS}.{EV[key]}"


SED = "emerging_communist_state_are_in_power = yes"
SOV_HUMAN = "country_exists = SOV SOV = { is_ai = no NOT = { tag = ROOT } }"

# ================================================================ the focus events of the design
ev(1, f"{PFX}intro", "The Republic at Twenty",
   "Twenty years after its founding, the German Democratic Republic enters the 1970s under Walter Ulbricht and the Socialist Unity Party. "
   "The Berlin Wall has stemmed the flight to the West, but consumer shortages and the strain of economic reform continue to test public confidence.\n\n"
   "Willy Brandt's government in Bonn is seeking closer relations with its eastern neighbours. East Berlin hopes to secure international recognition "
   "while defending its claim to be a separate German state. The coming negotiations will test Ulbricht's leadership and the republic's place within the socialist bloc.",
   "intro", [o("A new decade begins.")])
ev(2, f"{PFX}erfurt_summit", "The Erfurt Summit",
   "19 March 1970. Willy Brandt arrives by train in Erfurt to meet Willi Stoph. Thousands break through the police lines in front of the Erfurter Hof "
   "and call 'Willy Brandt to the window!'. The Chancellor raises his hands to calm them. The Politburo watches the pictures in silence.",
   "COLDWAR_DDR_erfurt_summit",
   [o("Let the cameras roll: the world sees two German states.", E.course(0.05), "add_stability = -0.02", ai=30),
    o("Clear the square and send in the cheering cadres.", E.course(-0.05), E.trust(2), E.faction("intelligence_community", 5), ai=70)])
ev(3, f"{PFX}kassel_meeting", "The Kassel Meeting",
   "21 May 1970. In Kassel protesters tear down the flag of the republic, Brandt offers twenty points and Stoph insists on recognition under international law. "
   "Both sides agree on a 'pause for reflection'. Moscow and Bonn will continue without East Berlin.",
   "COLDWAR_DDR_kassel_meeting",
   [o("Recognition first - there is nothing else to discuss.", E.course(-0.05), E.trust(2), ai=70),
    o("Keep the channel to Bonn open.", E.course(0.05), E.trust(-2), ai=30)])
ev(4, f"{PFX}ulbricht_resigns", "Ulbricht Resigns",
   "3 May 1971. 'For reasons of age' Walter Ulbricht asks the Central Committee to relieve him of his duties as First Secretary. "
   "The plenum elects Erich Honecker unanimously; the old man becomes Chairman of the Party - an honorary title without power.",
   "ulbricht_resigns",
   [o("Long live Comrade Honecker.", f"{PFX}install_first_sec_hon = yes")],
   ttrigger=[f"has_country_flag = {PFX}first_sec_ulb", f"NOT = {{ has_country_flag = {PFX}ulb_stays }}", SED,
             f"check_variable = {{ {PFX}moscow_trust > 39 }}"])
ev(5, f"{PFX}ulb_the_old_man_stays", "The Old Man Stays",
   "Ambassador Abrasimov delivers a letter from Brezhnev: Moscow is 'concerned' about the First Secretary's lectures on economics and his private German policy. "
   "In the Politburo the thirteen signatories of the letter look at the floor.",
   "COLDWAR_DDR_ulb_the_old_man_stays",
   [o("The signatories recant at the next plenum.", "add_stability = 0.02", ai=60),
    o("Dismiss the ringleaders.", "add_political_power = 50", E.faction("communist_cadres", -5), E.trust(-5), ai=40)])
ev(6, f"{PFX}ulb_heart_attack", "A Heart Attack",
   "Spring 1973. Walter Ulbricht suffers a heart attack. The Kremlin doctors flown in from Moscow save him, but the old man must rest at Lake Döllnsee "
   "for months. The Politburo runs the republic without him.",
   "COLDWAR_DDR_ulb_heart_attack",
   [o("He will be back.", "add_political_power = -25", "add_stability = -0.02")],
   trigger=DDR_T + [f"has_country_flag = {PFX}ulb_kremlin_doctors", f"{PFX}alive_ulb = yes", "date > 1973.3.1"], mtth=30, once=True)
ev(7, f"{PFX}kessler_succession", "The Generals' Candidate",
   "Army General Heinz Hoffmann is dead. As he wished, the Military Council proposes Generaloberst Heinz Keßler as First Secretary. "
   "The Central Committee hesitates: a general at the head of the party has never happened in the socialist camp.",
   "COLDWAR_DDR_kessler_succession",
   [o("The Central Committee elects Keßler.", f"{PFX}install_kessler = yes", E.faction("the_military", 10), E.faction("communist_cadres", -10), ai=50),
    o("The Central Committee refuses.", f"set_country_flag = {PFX}kessler_refused",
      T("kessler_refused", "The Military Council of the NVA may now claim power: §YThe Generals Step In§! no longer needs the NVA Command's opinion."),
      E.faction("the_military", -10), f"{PFX}succession = yes", ai=50)])
ev(8, f"{PFX}guillaume_affair", "The Guillaume Affair",
   "April 1974. In Bonn the police arrest Günter Guillaume, a personal aide of the Chancellor - and an officer of the Main Directorate for Reconnaissance. "
   "Two weeks later Willy Brandt resigns. In Normannenstraße nobody celebrates in public.",
   "COLDWAR_DDR_guillaume_affair",
   [o("A painful success.")], kind="news")
ev(9, f"{PFX}x_world_festival", "The X World Festival",
   "Nine days in summer: 25,000 foreign guests and eight million visitors fill East Berlin. Young people from Chile, Vietnam and the West discuss on Alexanderplatz "
   "until morning, and for once the police look away.",
   "COLDWAR_DDR_x_world_festival",
   [o("Let the world see an open, young republic.", "add_stability = 0.03", E.course(0.05), E.party_pop(4, 0.02, 0.02), ai=60),
    o("Keep a close eye on the guests.", "add_stability = 0.01", E.faction("intelligence_community", 5), ai=40)])
ev(10, f"{PFX}the_doping_files", "The Doping Files",
   "Files of State Plan Research Topic 14.25 have reached Western journalists: the medals of the republic were won with anabolic steroids, given to athletes "
   "as young as thirteen. The diplomats in tracksuits come home disgraced.",
   "COLDWAR_DDR_the_doping_files",
   [o("A Western smear campaign.", f"if = {{ limit = {{ has_idea = {PFX}soc_diplomats_in_tracksuits }} remove_ideas = {PFX}soc_diplomats_in_tracksuits }}",
      "add_stability = -0.05")],
   trigger=DDR_T + [f"has_country_flag = {PFX}doping_scandal_risk", f"has_idea = {PFX}soc_diplomats_in_tracksuits",
                    f"OR = {{ check_variable = {{ {PFX}course > 0.59 }} NOT = {{ has_government = communism }} }}"], mtth=60, once=True)
ev(11, f"{PFX}helsinki_exit_applications", "The Exit Applications",
   "Since the Final Act of Helsinki thousands of citizens have filed applications to leave the republic, quoting Basket Three. "
   "Most lose their jobs; some are bought free by Bonn. The MfS opens a file on every applicant.",
   "COLDWAR_DDR_helsinki_exit_applications",
   [o("Process the applications quietly.", "add_stability = -0.02", E.course(0.05), ai=40),
    o("A file on every applicant.", "add_stability = 0.01", E.faction("intelligence_community", 5), E.course(-0.05), E.trust(2), ai=60)])
ev(12, f"{PFX}bucharest_formula", "The Bucharest Formula",
   "From now on Comecon prices follow a moving average of world prices. Soviet crude gets dearer every year, and the republic pays in machines and ships "
   "it would rather sell for hard currency.",
   "COLDWAR_DDR_bucharest_formula",
   [o("Pay with machines and ships.", E.country_dyn("planned_economy", {"civilian_industry_tax_modifier": -0.02}), E.trust(3), ai=60),
    o("Sell more crude products to the West.", E.pay(0.005), E.trust(-2), ai=40)])
ev(13, f"{PFX}polish_crisis", "The Polish Crisis",
   "Solidarity counts ten million members; the Polish United Workers' Party has lost the workers. The Politburo fears the Polish disease more than the "
   "West German television.",
   "COLDWAR_DDR_polish_crisis",
   [o("Stand by the Polish comrades.", E.trust(3), E.faction("communist_cadres", 5), ai=70),
    o("Watch and wait.", "add_stability = 0.01", ai=30)])
ev(14, f"{PFX}euromissiles", "The Euromissile Crisis",
   "The Bundestag has approved the Pershing II, the Soviet delegation has left Geneva, and Moscow announces new missiles for the GDR. "
   "Erich Honecker speaks of 'damage limitation' and a 'coalition of reason'.",
   "COLDWAR_DDR_euromissiles",
   [o("Welcome the counter-deployment.", E.trust(5), E.tension(1), "add_stability = -0.02", ai=60),
    o("A coalition of reason with Bonn.", E.course(0.05), E.trust(-3), ai=40)])
ev(15, f"{PFX}ldk_warsaw_pact_manoeuvres", "Manoeuvres on the Border",
   "Soviet, Polish and Czechoslovak divisions exercise along our borders. The commanders speak of a routine exercise; everyone in Berlin remembers Prague 1968.",
   "COLDWAR_DDR_ldk_warsaw_pact_manoeuvres",
   [o("Concede: the reforms will be slowed.", E.trust(10), "add_stability = -0.05", ai=60),
    o("Stand firm.", "add_war_support = 0.05", E.tension(3),
      f"if = {{ limit = {{ check_variable = {{ {PFX}moscow_trust < 20 }} }} {PFX}open_fraternal_assistance = yes }}", ai=40)])
ev(16, f"{PFX}ssp_the_world_condemns", "The World Condemns",
   "Western capitals recall their ambassadors, the Non-Aligned protest in New York. The Ministry calls it an internal matter of a sovereign state.",
   "COLDWAR_DDR_ssp_the_world_condemns",
   [o("Let them protest.", E.course(-0.10))],
   immediate=[f"every_country = {{ limit = {{ OR = {{ tag = GER tag = USA tag = ENG tag = FRA tag = SWE tag = RAJ tag = SER }} NOT = {{ tag = ROOT }} }} "
              f"country_event = {{ id = {NS}.17 days = 2 }} }}"])
ev(17, f"{PFX}world_condemns_reaction", "Terror in East Berlin",
   "The government of [FROM.GetNameDef] has unleashed its state security against its own people. Our ambassador asks for instructions.",
   "COLDWAR_DDR_ssp_the_world_condemns",
   [o("Recall our ambassador.", f"add_opinion_modifier = {{ target = FROM modifier = {PFX}terror_condemned }}",
      f"FROM = {{ add_opinion_modifier = {{ target = ROOT modifier = {PFX}ambassador_recalled }} }}", ai=60),
    o("A statement is enough.", ai=40)])

# ================================================================ historical events (date triggered)
ev(20, f"{PFX}moscow_treaty", "The Moscow Treaty",
   "12 August 1970. In the Kremlin Brandt and Kosygin sign a treaty renouncing force and recognising the borders of Europe, the inner-German border included. "
   "East Berlin was informed - not asked.",
   "moscow_treaty",
   [o("Moscow knows best.", E.trust(3), E.course(0.05), ai=60),
    o("Protest - in private.", E.trust(-3), E.course(-0.05), E.faction("communist_cadres", 5), ai=40)],
   trigger=DDR_T + ["date > 1970.8.11", "is_subject_of = SOV"], mtth=1, once=True)
ev(21, f"{PFX}biermann_affair", "The Biermann Affair",
   "16 November 1976. After a concert in Cologne the singer Wolf Biermann is told he may not return. A dozen writers and actors sign a protest letter; "
   "West German television broadcasts the whole concert.",
   "biermann_affair",
   [o("Expatriated - and good riddance.", "add_stability = -0.02", E.course(-0.05), E.faction("intelligence_community", 5), ai=70),
    o("Let him come home.", E.course(0.05), E.trust(-3), E.faction("communist_cadres", -5), "add_stability = 0.01", ai=30)],
   trigger=DDR_T + ["date > 1976.11.15", "has_government = communism"], mtth=1, once=True)
ev(22, f"{PFX}coffee_crisis", "The Coffee Crisis",
   "1977. Frost in Brazil and the world market prices explode: the republic spends three hundred million hard-currency marks on coffee a year. "
   "The Politburo considers a blend with chicory and rye - the people already call it 'Erichs Krönung'.",
   "coffee_crisis",
   [o("Introduce the blend.", "add_stability = -0.03", ai=40),
    o("Buy coffee from Vietnam and Ethiopia.", E.pay(0.005), "add_stability = -0.01", ai=60)],
   trigger=DDR_T + ["date > 1977.6.1"], mtth=1, once=True)
ev(23, f"{PFX}oil_cut", "The Oil Cut",
   "Autumn 1981. Moscow informs East Berlin that oil deliveries will be cut by two million tonnes a year. Brezhnev writes of 'the most difficult decision'. "
   "The refineries at Schwedt and Leuna must find something else to burn.",
   "oil_cut",
   [o("Coal instead of oil.", f"if = {{ limit = {{ {PFX}ladder_lignite_active = yes }} {PFX}ladder_lignite_clear = yes add_ideas = {PFX}energy_coal_instead_of_oil }}",
      "add_stability = -0.02", ai=60),
    o("Buy the missing oil on the world market.", E.pay(0.01), E.trust(-2), ai=40)],
   trigger=DDR_T + ["date > 1981.10.1", "is_subject_of = SOV"], mtth=1, once=True, immediate=[f"set_country_flag = {PFX}oil_cut"])
ev(24, f"{PFX}man_in_space", "Our Man in Space",
   "26 August 1978. Sigmund Jähn, a lieutenant colonel of the air force from the Vogtland, lifts off from Baikonur on Soyuz 31: the first German in space "
   "is a citizen of the republic.",
   "man_in_space",
   [o("The first German in space!", "add_stability = 0.03", E.party_pop(4, 0.02, 0.02), E.trust(3))])

# ================================================================ Moscow's Trust and the Inner-German course
ev(30, f"{PFX}bonns_embrace", "Bonn's Embrace",
   "Credits, visits, town twinnings, a hotline between the chancelleries: the two German states have never been closer. In Moscow they read the reports "
   "of the embassy with growing alarm.",
   "bonns_embrace",
   [o("The embrace is good for us.", E.trust(-5), "add_stability = 0.02", ai=40),
    o("Step back from Bonn.", E.course(-0.15), E.trust(3), ai=60)])
ev(31, f"{PFX}ambassador_calls", "The Ambassador Calls",
   "The Soviet ambassador asks for an appointment - tonight. He brings a letter from the General Secretary and a list of 'questions of concern'. "
   "In Wünsdorf the Group of Soviet Forces has cancelled all leave.",
   "ambassador_calls",
   [o("Submit to Moscow.", E.trust(15), E.course(-0.10), "add_political_power = -50", ai=80),
    o("Defy the ambassador.", "add_war_support = 0.05", f"{PFX}open_fraternal_assistance = yes", ai=20)],
   immediate=[f"set_country_flag = {PFX}ambassador_called"])
ev(32, f"{PFX}fraternal_concern", "Fraternal Concern",
   "Moscow has rejected our request. A Soviet delegation arrives without notice and speaks of the 'common responsibility of the fraternal parties'. "
   "The Group of Soviet Forces holds an alert exercise.",
   "fraternal_concern",
   [o("Reassure Moscow.", E.trust(5), E.course(-0.05), ai=70),
    o("Hold our course.", "add_war_support = 0.03",
      f"if = {{ limit = {{ check_variable = {{ {PFX}moscow_trust < 20 }} }} {PFX}open_fraternal_assistance = yes }}", ai=30)])
ev(33, f"{PFX}fraternal_assistance", "Fraternal Assistance",
   "The Soviet Union demands that the republic return to the path of socialism - at once. Soviet divisions are moving out of their garrisons; "
   "the ultimatum expires at dawn.",
   "fraternal_assistance",
   [o("Bow to Moscow.", f"{PFX}bow_to_moscow = yes", f"FROM = {{ country_event = {{ id = {NS}.34 days = 1 }} }}", ai=80),
    o("Resist.", f"{PFX}resist_fraternal_assistance = yes", ai=20)])
ev(34, f"{PFX}fraternal_assistance_answer", "East Berlin Bows",
   "[FROM.GetNameDefCap] has accepted our ultimatum. The comrades in East Berlin return to the path of socialism.",
   "fraternal_assistance", [o("We will see.")])

# ================================================================ First Secretaries: deaths, succession, the Kremlin
DEATH = {"ulb": ("Walter Ulbricht", "death_ulbricht",
                 "Walter Ulbricht, founder of the republic, has died at the government guest house at Lake Döllnsee. The state funeral is held in Berlin; "
                 "the Politburo stands in the front row, and in the second the men who wrote the letter to Brezhnev.",
                 [f"OR = {{ AND = {{ date > 1973.7.31 NOT = {{ has_country_flag = {PFX}ulb_kremlin_doctors }} }} date > 1976.7.31 }}"]),
         "lam": ("Werner Lamberz", "death_lamberz",
                 "Werner Lamberz, the youngest member of the Politburo, has died in a helicopter crash in the Libyan desert after a meeting with Colonel Gaddafi. "
                 "Many in the party had seen him as the next First Secretary.",
                 ["date > 1978.3.5", f"NOT = {{ has_country_flag = {PFX}lamberz_stays_in_berlin }}"]),
         "hof": ("Heinz Hoffmann", "death_hoffmann",
                 "Army General Heinz Hoffmann, Minister of National Defence for a quarter of a century, has died. The NVA lowers its flags; "
                 "the Grand Tattoo plays for him in Strausberg.", ["date > 1985.12.1"])}
for n, (k, (name, pic, desc, cond)) in enumerate(DEATH.items(), start=40):
    ev(n, f"{PFX}death_{k}", f"Death of {name}", desc, pic,
       [o("The republic mourns.", f"{PFX}leader_dies_{k} = yes")],
       trigger=DDR_T + [f"NOT = {{ has_country_flag = {PFX}dead_{k} }}"] + cond, mtth=1, once=True)

# the Central Committee chooses a successor (no designated heir): every living candidate the party would accept
SUCC = ["hon", "sto", "mit", "hag", "kre", "kro", "mod", "lam", "hof", "ulb"]
SUCC_AI = {"hon": "base = 40", "sto": "base = 20", "mit": "base = 8", "hag": "base = 8", "kre": "base = 10", "kro": "base = 6", "mod": "base = 2",
           "lam": "base = 10", "hof": "base = 4", "ulb": "base = 1"}
ev(43, f"{PFX}succession_plenum", "The Central Committee Elects",
   "The office of First Secretary is vacant and no heir has been named. In the great hall at Werderscher Markt the Central Committee meets behind closed doors; "
   "the Politburo has prepared the candidates.",
   "succession_plenum",
   [(f"Elect {LEADER_NAME[k]}.", [f"{PFX}install_first_sec_{k} = yes"], SUCC_AI[k],
     [f"{PFX}alive_{k} = yes", f"NOT = {{ has_country_flag = {PFX}first_sec_{k} }}"]) for k in SUCC])
ev(44, f"{PFX}heir_elected", "The Heir Takes Over",
   "The old First Secretary keeps his word: the Central Committee is convened and elects the designated heir without a dissenting vote.",
   "cc_elects", [o("A new First Secretary.", f"{PFX}succession = yes")],
   ttrigger=[f"has_country_flag = {PFX}ulb_retiring", f"has_country_flag = {PFX}first_sec_ulb", SED])
ev(45, f"{PFX}new_first_secretary", "A New First Secretary",
   "The Central Committee of the Socialist Unity Party of Germany has elected §Y[ROOT.GetLeader]§! First Secretary. Neues Deutschland prints the "
   "biography on page one and the congratulations of the fraternal parties on pages two to six.",
   "cc_elects", [o("Long live the Party.")], kind="news")
# the Kremlin's say (human Soviet Union only)
ev(46, f"{PFX}kremlin_consulted", "East Berlin Asks",
   "The Central Committee in East Berlin intends to elect §Y[COLDWAR_DDR_GetCandidate]§! as First Secretary of the SED "
   "and asks for the opinion of the Soviet comrades before the vote.",
   "kremlin_consulted",
   [o("We have no objections.", "DDR = { COLDWAR_DDR_cc_approved = yes }", ai=90),
    o("Veto the candidate.", "DDR = { COLDWAR_DDR_cc_vetoed = yes }", ai=10)])
ev(47, f"{PFX}kremlin_veto", "Moscow Says No",
   "The Soviet ambassador has delivered the answer of the Kremlin: the candidate is 'not acceptable to the fraternal parties'. The plenum is postponed.",
   "kremlin_consulted", [o("We must bow to Moscow - for now.", "add_stability = -0.03")])
for n, (k, what) in enumerate([("first_sec", "has a new First Secretary, §Y[DDR.GetLeader]§!"),
                               ("western_credit", "has signed a credit agreement with a West German bank consortium"),
                               ("basic_treaty", "has signed a Basic Treaty with the Federal Republic")], start=48):
    ev(n, f"{PFX}kremlin_notice_{k}", "News from East Berlin",
       f"Our embassy reports: [DDR.GetNameDefCap] {what}. The General Secretary may let East Berlin know what Moscow thinks of it.",
       "kremlin_notice",
       [o("Endorse the step.", f"DDR = {{ {PFX}kremlin_endorses = yes }}", ai=60),
        o("Object to it.", f"DDR = {{ {PFX}kremlin_objects = yes }}", ai=40)])
ev(51, f"{PFX}kremlin_endorsed", "Moscow Approves",
   "The Soviet leadership has let us know that it approves of our latest step. Moscow's Trust rises.", "kremlin_notice", [o("Good.")])
ev(53, f"{PFX}kremlin_objected", "Moscow Objects",
   "The Soviet leadership has let us know that it does not approve of our latest step. Moscow's Trust falls.", "kremlin_notice", [o("We will remember.")])
ev(52, f"{PFX}soviet_endorses", "Moscow Courts a Rival",
   "The Soviet ambassador has been seen at the dacha of Werner Krolikowski. Moscow lets it be known that it would welcome 'a change of generations' in East Berlin.",
   "kremlin_notice", [o("The Central Committee takes note.")],
   immediate=[f"set_country_flag = {{ flag = {PFX}soviet_endorses_change days = 365 }}"])

# ================================================================ treaties: accession, release, the garrison
ACC_OK = ["is_subject = no", "country_exists = GER", "NOT = { has_war_with = GER }", "NOT = { has_government = communism }",
          f"has_country_flag = {PFX}accession_pending"]
ev(60, f"{PFX}accession_complete", "The Transition Year Ends",
   "The transition year is over. If nothing stands in the way, the flag of the republic is lowered at midnight in front of the Reichstag "
   "and the five restored states join the Federal Republic.",
   "accession",
   [("Unity in freedom.", [f"{PFX}complete_accession = yes"], 100, ACC_OK),
    ("The accession has failed.", [f"clr_country_flag = {PFX}accession_pending", "add_stability = -0.05"], 100, ["NOT = { AND = { " + " ".join(ACC_OK) + " } }"])])
ev(64, f"{PFX}two_plus_four", "Two Plus Four",
   "Bonn has agreed that the German Democratic Republic may join the Federal Republic. East Berlin asks the Soviet Union to release the republic "
   "from its treaty ties and the Warsaw Pact. The Group of Soviet Forces would be settled in a separate treaty.",
   "accession",
   [o("Let Germany unite.", "end_puppet = DDR", E.tension(-2), f"DDR = {{ {PFX}begin_transition = yes }}",
      ai="base = 10\nmodifier = { factor = 6 NOT = { has_government = communism } }\nmodifier = { factor = 3 has_country_flag = COLDWAR_SOV_gensec_gor }"),
    o("Never.", f"DDR = {{ add_stability = -0.03 {' '.join(E.trust(-10))} country_event = {{ id = {NS}.65 days = 1 }} }}", ai=90)])
ev(65, f"{PFX}accession_blocked", "Moscow Says No to Unity",
   "The Soviet Union has refused to release the republic. Bonn's yes is worth nothing while the Group of Soviet Forces stands in Wünsdorf.",
   "accession", [o("Unity must wait.")])
ev(61, f"{PFX}garrison_leaves", "The Soldiers Go Home",
   "The last trains of the Group of Soviet Forces leave Wünsdorf. Generals and soldiers have packed for three decades; the barracks stand empty.",
   "garrison_leaves", [o("Do svidaniya.", f"if = {{ limit = {{ has_idea = {PFX}the_soviet_garrison }} remove_ideas = {PFX}the_soviet_garrison }}",
                         f"clr_country_flag = {PFX}garrison_withdrawing")])
ev(62, f"{PFX}released_from_the_pact", "Out of the Warsaw Pact",
   "Moscow has agreed: the republic leaves the Warsaw Pact and its treaty ties. The Group of Soviet Forces will withdraw within two years.",
   "COLDWAR_DDR_offer_release_west", [o("A new chapter.", f"{PFX}leave_warsaw_pact = yes", f"{PFX}start_garrison_withdrawal_730 = yes")])

ev(63, f"{PFX}arms_for_oil_payment", "Payment for the Weapons",
   "Another tranche for the weapons and trucks arrives in hard currency.", "offer_answer",
   [o("Book it.")], hidden=True, immediate=E.receive(0.003))

# 900/901: the answers to our offers (the effects happen in the partner's answer - it decides)
ev(900, f"{PFX}offer_accepted", "Our Proposal Is Accepted",
   "[FROM.GetNameDefCap] has accepted our proposal. The agreed terms take effect.", "offer_answer", [o("Excellent.")])
ev(901, f"{PFX}offer_declined", "Our Proposal Is Declined",
   "[FROM.GetNameDefCap] has declined our proposal.", "offer_answer", [o("Regrettable.")])


# ---------------------------------------------------------------- how a focus fires an event
DELAY = {f"{PFX}ulbricht_resigns": 30, f"{PFX}ldk_warsaw_pact_manoeuvres": 30}


def fire(key, f):
    """code lines of a focus effect 'event'"""
    if key == f"{PFX}kessler_succession":
        return [T("kessler_succession", "At Hoffmann's death the Central Committee is asked to elect §YHeinz Keßler§! as First Secretary. "
                                         "If it refuses, the Military Council of the NVA may claim power.")]
    if key == f"{PFX}ulb_heart_attack":
        return [T("ulb_heart_attack", "In spring 1973 a heart attack will force the old man to rest for months (event).")]
    if key == f"{PFX}the_doping_files":
        return [f"set_country_flag = {PFX}doping_scandal_risk",
                T("doping_risk", "If the Inner-German course reaches §Y0.6§! or a non-Emerging party governs, §RThe Doping Files§! become public: "
                                 "\"Diplomats in Tracksuits\" is lost and stability falls by §R5%§!.")]
    n = EV[key]
    kind = next(e.get("kind") for e in EVENTS if e["n"] == n)
    if kind == "news":
        return [f"news_event = {{ id = {NS}.{n} hours = 6 }}"]
    if key in DELAY:
        LOC[f"{PFX}ev_{n}_delay_tt"] = f"In §Y{DELAY[key]} days§!: event §Y{next(e['title'] for e in EVENTS if e['n'] == n)}§!."
        return [f"custom_effect_tooltip = {PFX}ev_{n}_delay_tt", f"hidden_effect = {{ country_event = {{ id = {NS}.{n} days = {DELAY[key]} }} }}"]
    return [f"country_event = {{ id = {NS}.{n} days = 1 }}"]
