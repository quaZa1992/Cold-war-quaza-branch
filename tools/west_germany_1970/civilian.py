# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""The Civilian Power pillar, deepened (multiplayer roleplay).

Culture abroad, human rights, the global economy and the environment, the United Nations, Asia,
Africa, Latin America and sport. Same rules as the rest of the tree: partner countries decide for
themselves through offers (COLDWAR_GDIP), alternative-historical choices sit beside the historical
ones, the big moments are public news for every other government. Events in COLDWAR_GCIV.
"""
from cw_lib import *
from events_lib import E, O
from tree import F, core, infl, opinion, state_build, state_mod, STATE_MODS
from rivalry import kl
from foreign import offer, multi_offer, news_all

EVC = "COLDWAR_GCIV"
UNITY = f"has_global_flag = {P}_unity_achieved"
WALL = f"has_global_flag = {P}_wall_open"
OPEN_OR_UNITY = f"OR = {{ {WALL} {UNITY} date > 1990.12.31 }}"
SPD = "check_variable = { ruling_party = 3 }"
UNION = "check_variable = { ruling_party = 1 }"
from roster import requirement
GREEN_GOV = 'AND = { ' + requirement('greens') + ' OR = { check_variable = { ruling_party = 17 } is_in_array = { gov_coalition_array = 17 } } }'
NOT_DARK = f"NOT = {{ has_country_flag = {P}_dark_regime }}"
NRW = 39

STATE_MODS.update({
    "un_city": ("UN City Bonn", {"state_productivity_growth_modifier": 0.03, "local_building_slots": 1}),
})

_n = [0]


def ev(title, desc, opts, pic="GFX_politics_talks", days=3):
    _n[0] += 1
    evid = f"{EVC}.{_n[0]}"
    E(evid, title, desc, pic, opts)
    return f"country_event = {{ id = {evid} days = {days} }}"


# =========================================================================== CULTURE ABROAD
F("goethe_worldwide", "cultural_diplomacy", 13, 1, cost=2, icon="education", name="A Goethe-Institut in Every Capital",
  desc="One hundred and thirty institutes, from Lagos to La Paz, teach German, show Fassbinder and invite local writers to read. They are paid for by the Foreign Office and answer to nobody in it - a freedom that diplomats curse whenever an institute hosts the wrong dissident on the wrong evening.",
  reward=J(core("welt", support=0.05), core("west", opinion=0.02), money_gdp(-0.001)))
F("deutsche_welle", "goethe_worldwide", -1, 1, cost=2, icon="television", name="The Voice from Cologne",
  desc="Deutsche Welle broadcasts in thirty-four languages on short wave, and in the East its German service is jammed less than RIAS or Radio Free Europe. Its editors insist on one thing: the news must be true, including the news Bonn would rather not hear.",
  reward=J(core("wehrhaft", influence=0.05), core("west", ideo=0.03), dv("cwddr_opposition", 2), tension(1)))
F("two_way_street", "goethe_worldwide", 1, 1, cost=2, icon="diplomacy", name="Culture as a Two-Way Street",
  desc="Hildegard Hamm-Brücher's guidelines turn cultural policy on its head: no more exporting Beethoven and the German idea, but exchange - partners invited to Germany, foreign artists in German theatres, a dialogue rather than a lecture.",
  reward=J(core("welt", eff=0.05), core("bonn", drift=0.02), party("fdp", 0.002)))
F("solzhenitsyn_guest", "deutsche_welle", -1, 1, cost=2, avail="date > 1974.2.1", icon="pacifists", name="A Guest in the Eifel",
  desc="February 1974: the Soviet Union expels Alexander Solzhenitsyn. The plane from Moscow lands in Frankfurt, and the first house that opens its door to him belongs to Heinrich Böll, in a village in the Eifel. The Kremlin is watching how Bonn receives its most famous exile.",
  reward=ev("Solzhenitsyn in Germany",
            "Photographers have climbed the garden wall in Langenbroich. The Soviet embassy lets it be known that an official reception would be 'an unfriendly act'; the opposition demands one. The author himself wants only a desk and silence - and a word from the chancellor.",
            [O("The chancellor receives him publicly.", J(core("west", ideo=0.05), opinion("SOV", "medium_decrease"), kl(-2), party("cdu", 0.002)), ai=40),
             O("A private welcome - nothing for the cameras.", J(core("welt", support=0.03), opinion("SOV", "small_decrease")), ai=60)],
            pic="GFX_der_Spiegel"))
F("textbook_commission", "two_way_street", 1, 1, cost=2, avail="date > 1972.1.1 country_exists = POL", icon="poland", name="The Textbook Commission",
  desc="German and Polish historians sit down to read each other's schoolbooks - the war, the expulsions, the Oder and the Neisse - and to agree on what children on both sides should learn. In Bavaria the expellees' associations call it a betrayal before the first page is written.",
  reward=offer("textbooks", "POL", "A Joint Textbook Commission",
               "Bonn proposes a joint commission of historians to revise the history textbooks of both countries and remove the hatred of the last century from the classroom.",
               J(opinion("POL", "medium_increase"), infl("POL", 2), kl(1), v("cwger_ostpolitik", 3)),
               partner_eff="add_stability = 0.01", accept="Our historians will come.", refuse="History is ours to teach.", pic="GFX_politics_talks", ai=60))
F("arte_channel", "deutsche_welle", 1, 1, cost=3, pre=[["deutsche_welle", "two_way_street"]], avail="date > 1988.1.1", icon="france", name="A Channel for Europe",
  desc="Kohl and Mitterrand agree on a television channel that belongs to neither nation: films without dubbing, documentaries at prime time, an evening programme for perhaps two per cent of the audience - and the conviction that two per cent of two nations is a beginning.",
  reward=offer("arte", "FRA", "A Franco-German Television Channel",
               "Bonn proposes a joint cultural television channel, run from Strasbourg and paid for by both countries, broadcasting the same programme in two languages.",
               J(core("west", europe=0.03, opinion=0.02), opinion("FRA", "medium_increase"), core("welt", support=0.03)),
               partner_eff="add_political_power = 20", accept="Strasbourg it is.", refuse="French culture needs no partner.", pic="GFX_european_parliament", ai=70))
F("image_of_germany", "arte_channel", -1, 1, cost=2, mutex=["critical_mirror"], icon="west_germany", name="The Image of Germany",
  desc="The Federal Press Office wants a Germany that sells: Mercedes and Mozart, Lufthansa and the Rhine, a reliable, prosperous, slightly boring democracy. Exhibitions, glossy brochures, a travelling show of German design. The Goethe-Institutes are asked to stay on message.",
  reward=J(core("welt", market=0.04), core("modell", fac=0.01), faction("bdi", 3), core("bonn", drift=-0.01)))
F("critical_mirror", "arte_channel", 1, 1, cost=2, mutex=["image_of_germany"], icon="speech", name="A Critical Mirror",
  desc="Grass reads in Calcutta, Wenders shows his films in Tokyo, Wallraff's reportages are translated into Turkish. The government sends abroad the artists who attack it at home - on the theory that a democracy which exports its critics is more convincing than one which exports its brochures.",
  reward=J(core("welt", support=0.06, eff=0.03), core("west", ideo=0.03), party("greens", 0.001), party("cdu", -0.001)))
F("goethe_in_the_east", "image_of_germany", 1, 1, cost=3, pre=[["image_of_germany", "critical_mirror"]], avail=OPEN_OR_UNITY, icon="eastern_europe", name="Goethe Goes East",
  desc="The Wall has fallen and suddenly everyone east of the Oder wants to learn German: Goethe-Institutes open in Moscow, Kiev, Riga and Almaty, teachers are flown to Prague and Budapest, and the German language becomes, for a few years, the lingua franca of a continent in transition.",
  reward=J(infl("POL", 3), infl("CZE", 3), infl("HUN", 3), infl("SOV", 2), core("welt", support=0.04), money_gdp(-0.002)))
F("humboldt_fellows", "goethe_in_the_east", 0, 1, cost=2, icon="research", name="Scholarships for the World",
  desc="DAAD and the Humboldt Foundation bring a hundred thousand students and scholars a year to German universities. Many go home as ministers, judges and professors - and keep a soft spot for Heidelberg, Göttingen or Tübingen for the rest of their lives.",
  reward=J(core("west", research=0.03), core("welt", support=0.03, eff=0.03), money_gdp(-0.001)))

# =========================================================================== HUMAN RIGHTS
F("human_rights_policy", "csce_followup", 2, 1, cost=2, avail="date > 1977.1.1", icon="civil_rights", name="Human Rights as Foreign Policy",
  desc="Since Helsinki, human rights are no longer an internal affair of the East. Bonn has signed Basket Three and now has to decide what it is worth: a weapon against Moscow, a lever for East German families, or a principle that applies to friends as much as to enemies.",
  reward=J(core("welt", support=0.04), core("west", ideo=0.02), dv("cwddr_opposition", 2)))
F("speak_for_dissidents", "human_rights_policy", -1, 1, cost=2, mutex=["quiet_diplomacy"], icon="speech", name="Name the Prisoners",
  desc="At every conference the German delegation reads out names: Sakharov, Orlov, Havel, Bahro. It is loud, it is public, and it makes the other side's diplomats walk out - but for the prisoners, a name known in the West is sometimes the only protection they have.",
  reward=J(core("west", ideo=0.05), dv("cwddr_opposition", 4), opinion("SOV", "small_decrease"), kl(-3), party("cdu", 0.002)))
F("quiet_diplomacy", "human_rights_policy", 1, 1, cost=2, mutex=["speak_for_dissidents"], icon="secret_meeting", name="Quiet Diplomacy",
  desc="The Foreign Office prefers the back channel: a word to the Soviet ambassador over dinner, an exit visa quietly granted, a credit quietly extended. No headlines, no walkouts - and every year a few hundred people who are allowed to leave.",
  reward=J(kl(3), core("ost", stab=0.02), opinion("SOV", "small_increase"), core("west", ideo=-0.01)))
F("charter_77", "speak_for_dissidents", 1, 1, cost=2, pre=[["speak_for_dissidents", "quiet_diplomacy"]], avail="date > 1977.1.6 country_exists = CZE", icon="civil_rights", name="The Signatories of Charter 77",
  desc="Two hundred and forty Czechoslovak citizens have signed a document asking their own government to obey its own laws. They are fired, interrogated, their children barred from university. Prague warns that any foreign support is interference in its internal affairs.",
  reward=ev("Charter 77",
            "Václav Havel is in custody again. The embassy in Prague reports that a public statement from Bonn would make his release more likely - or less; the diplomats disagree. A group of Bundestag members wants to travel to Prague and visit the signatories in person.",
            [O("A public statement and a parliamentary delegation.", J(dv("cwddr_opposition", 3), opinion("CZE", "medium_decrease"), core("west", ideo=0.03), tension(1)), ai=40),
             O("Visas and scholarships for the persecuted, without fanfare.", J(core("welt", support=0.03), opinion("CZE", "small_decrease"), "add_manpower = 2000"), ai=60)],
            pic="GFX_politics_protest"))
F("volga_germans", "charter_77", 0, 1, cost=3, avail="date > 1975.1.1 country_exists = SOV", icon="migration", name="Exit for the Soviet Germans",
  desc="Two million Germans live in the Soviet Union - descendants of the settlers Catherine the Great invited to the Volga, deported to Kazakhstan by Stalin in 1941. Most of them want only one thing: to leave. Moscow lets out a few thousand a year, and Bonn wonders what the rest would cost.",
  reward=offer("soviet_germans", "SOV", "Exit Visas for the Soviet Germans",
               "The Federal Republic asks the Soviet government to let ethnic Germans who wish to emigrate leave for West Germany - and indicates that trade credits would be easier to grant in a better climate.",
               J("add_manpower = 40000", party("cdu", 0.002), core("welt", support=0.02), money_gdp(-0.002)),
               partner_eff=J(money_gdp(0.002), "add_political_power = 15"), accept="Let them go - for a price.", refuse="Soviet citizens stay Soviet citizens.", pic="GFX_German_migrant", ai=45))

# =========================================================================== THE WORLD ECONOMY AND THE ENVIRONMENT
F("hermes_cover", "rambouillet", -1, 1, cost=2, icon="export", name="Hermes Cover",
  desc="A Hamburg insurer underwrites the risk on behalf of the Federal Government: if the buyer in Baghdad, Lagos or Moscow does not pay, Bonn does. Hermes guarantees make German exporters the most fearless in the world - and the taxpayer the silent partner of every contract.",
  reward=J(core("welt", market=0.05), core("modell", fac=0.01), faction("bdi", 4), debt_gdp(0.001)))
F("tied_aid", "hermes_cover", -1, 1, cost=2, mutex=["untied_aid"], icon="trade_europe", name="Aid that Buys German",
  desc="Development credits, but with a condition: the turbines come from Siemens, the trucks from Daimler, the consultants from Frankfurt. The Ministry of Economics is delighted; the Development Ministry calls it an export subsidy with a humanitarian label.",
  reward=J(core("welt", market=0.04, eff=-0.03), faction("bdi", 5), core("modell", fac=0.01)))
F("untied_aid", "hermes_cover", 1, 1, cost=2, mutex=["tied_aid"], icon="green_projects", name="Aid without Strings",
  desc="Bonn follows the OECD's advice and unties most of its development aid: partners may buy wherever it is cheapest, and the projects are judged by what they achieve, not by how many German machines they ship. Industry complains, the recipients notice.",
  reward=J(core("welt", eff=0.06, cap=1), faction("bdi", -3), party("greens", -0.001)))
F("cologne_debt", "tied_aid", 1, 1, cost=3, pre=[["tied_aid", "untied_aid"]], avail="date > 1996.1.1", icon="euro", name="The Cologne Debt Initiative",
  desc="Under the cathedral, the leaders of the eight biggest economies agree to cancel up to seventy billion dollars of debt owed by the poorest countries in the world - while a human chain of thirty thousand people from the Jubilee campaign links arms around the summit.",
  reward=J(core("welt", support=0.08, eff=0.04), money_gdp(-0.003), opinion("ETH", "medium_increase"), opinion("TNZ", "medium_increase"), opinion("NIG", "small_increase"),
           news_all("The Cologne Debt Initiative", "At the summit in Cologne, Germany leads the leading industrial nations in cancelling the debts of the world's poorest countries.", "GFX_politics_talks")))
F("earth_summit", "rambouillet", 1, 1, cost=2, avail="date > 1991.6.1", icon="green_projects", name="The Earth Summit",
  desc="Rio de Janeiro, June 1992: a hundred and seventy governments discuss the climate, the forests and the species. The German delegation arrives with the reputation of a country that taught the world the word 'Waldsterben' - and with a chancellor who promises a quarter less carbon dioxide by 2005.",
  reward=J(core("energie", renew=0.04), core("welt", support=0.05), infl("BRA", 2), party("greens", -0.002), faction("bdi", -2)))
F("berlin_mandate", "earth_summit", 0, 1, cost=3, avail="date > 1994.6.1", icon="green_projects", name="The Berlin Mandate",
  desc="The first conference of the parties to the climate convention meets in Berlin in the spring of 1995. The young environment minister in the chair negotiates through the night until the delegates agree to negotiate binding targets - the road that will lead to Kyoto.",
  reward=ev("The Climate Conference in Berlin",
            "Four in the morning in the Congress Centre. The oil states want no targets at all, the island states want them now, Washington wants them later. The chair has one draft left and two ways to end the night.",
            [O("Binding targets - Germany leads by example.", J(core("energie", renew=0.05, fossil=-0.03), core("welt", support=0.05), faction("bdi", -4), party("greens", -0.002)), ai=60),
             O("A mandate to negotiate, nothing more.", J(core("welt", support=0.02), faction("bdi", 2)), ai=40)],
            pic="GFX_politics_negotiations"))
F("un_city_bonn", "berlin_mandate", 0, 1, cost=3, avail=f"{UNITY} date > 1993.1.1", icon="un", name="Bonn, City of the United Nations",
  desc="The government is moving to Berlin, and the federal city on the Rhine fears it will become a provincial town with too many empty ministries. The answer: the climate secretariat, the UN Volunteers and a dozen other agencies move into the old parliamentary quarter.",
  reward=J(state_mod(NRW, "un_city"), core("welt", support=0.04, cap=1), core("bonn", stab=0.01)))

# =========================================================================== THE MIDDLE EAST
F("rabta_affair", "saudi_tanks", 0, 1, cost=2, avail="date > 1988.6.1", icon="dangerous_deal", name="The Rabta Affair",
  desc="American satellites photograph a factory in the Libyan desert. Washington says it makes poison gas, and that German companies built it. Bonn denies everything - until the customs investigators find the invoices of a firm in Lahr.",
  reward=ev("Poison Gas from Lahr",
            "The New York Times calls it 'Auschwitz in the sand'. The chancellor's office has the files on its desk: more than fifty German firms have supplied Libya and Iraq with plants that can produce chemical weapons. The export laws allowed almost all of it.",
            [O("Tighten the export laws - prison for the guilty.", J(v("cwger_rechtsstaat", 3), core("west", opinion=0.03), opinion("USA", "small_increase"), opinion("ISR", "medium_increase"), faction("bdi", -5), core("welt", market=-0.02)), ai=70),
             O("Blame a few black sheep and move on.", J(opinion("USA", "medium_decrease"), opinion("ISR", "medium_decrease"), faction("bdi", 3), v("cwger_rechtsstaat", -3)), ai=30)],
            pic="GFX_investigation_schreiber_kiep"))

# =========================================================================== ASIA
F("tiananmen_sanctions", "india_partnership", -1, 1, cost=2, mutex=["tiananmen_business"], avail="date > 1989.6.4 country_exists = CHI", icon="embargo", name="After Tiananmen: Sanctions",
  desc="Tanks on the Square of Heavenly Peace, students shot on the Avenue of Eternal Peace. The Community freezes arms sales and ministerial contacts with Beijing. For Bonn, which has courted China since 1972, the question is how long a freeze can last.",
  reward=J(opinion("CHI", "large_decrease"), core("west", ideo=0.04, opinion=0.02), core("welt", support=0.03, market=-0.03), faction("bdi", -3)))
F("tiananmen_business", "india_partnership", 1, 1, cost=2, mutex=["tiananmen_sanctions"], avail="date > 1989.6.4 country_exists = CHI", icon="trade_europe", name="After Tiananmen: Business",
  desc="A year after the massacre the first German minister is back in Beijing; Volkswagen is building in Shanghai, Siemens wants the high-speed line. Change through trade, says the government. The human rights groups call it a licence to shoot.",
  reward=J(infl("CHI", 4), core("welt", market=0.05, support=-0.03), faction("bdi", 5), opinion("CHI", "medium_increase")))
F("asean_partners", "cap_anamur", 1, 2, cost=2, avail="date > 1980.3.1", icon="trade_europe", name="Partners in Southeast Asia",
  desc="Five nations between Burma and the Philippines have formed a community to stand together against the Vietnamese advance and for their own prosperity. In 1980 the European Community signs a cooperation agreement with them - and German engineers follow the diplomats.",
  reward=J(infl("SIN", 2), infl("MAY", 2), infl("SIA", 2), infl("PHI", 2), infl("IND", 2), core("welt", market=0.04)))
F("jakarta_fleet", "asean_partners", 0, 1, cost=3, avail=f"{UNITY} country_exists = IND", icon="frigates", name="A Fleet for Jakarta",
  desc="The navy of the GDR is lying at anchor in Peenemünde, waiting for the scrapyard. Jakarta's technology minister - an aircraft engineer trained in Aachen - wants all of it: thirty-nine corvettes, landing ships and minesweepers, refitted in German yards.",
  reward=offer("jakarta_fleet", "IND", "The Former Volksmarine",
               "The Federal Republic offers to sell thirty-nine former East German warships to Indonesia, refitted in German shipyards and delivered with training crews.",
               J(money_gdp(0.002), infl("IND", 4), state_build(37, "dockyard"), corruption(True, 30), party("greens", 0.001)),
               partner_eff=J("add_political_power = 20", "navy_experience = 10"), accept="We buy the fleet.", refuse="We will not buy someone else's rust.", pic="GFX_politics_talks", ai=70))

# =========================================================================== AFRICA AND LATIN AMERICA
F("ethiopia_famine", "lome_convention", 1, 1, cost=2, avail="date > 1984.6.1", icon="refugees", name="Bread for Ethiopia",
  desc="Pictures from the camps at Korem fill the evening news: a famine in the north of Ethiopia, made worse by a civil war and a Marxist regime that resettles whole villages at gunpoint. Germans donate more than ever before. The government has to decide how to deliver - and to whom.",
  reward=ev("The Famine in Ethiopia",
            "The Derg in Addis Ababa demands that all aid go through its own ministries. The relief organisations warn that grain handed to the government will end up with the army. The Luftwaffe has Transall transport aircraft ready in Hanover.",
            [O("A Luftwaffe airlift directly to the camps.", J(core("welt", support=0.05, cap=1), core("armee", xp=0.02), opinion("ETH", "small_increase"), money_gdp(-0.001)), ai=60),
             O("Through the churches and the Red Cross only.", J(core("welt", eff=0.05), opinion("ETH", "small_decrease"), party("greens", -0.001)), ai=40)],
            pic="GFX_German_migrant"))
F("namibia_independence", "apartheid_sanctions", 1, 1, cost=2, pre=[["apartheid_sanctions", "pretoria_trade"]], avail="date > 1988.12.1", icon="un", name="Independence for Namibia",
  desc="After seventy years of South African rule and twenty-three years of war, Namibia goes to the polls under UN supervision. The former German colony owes Bonn little and remembers a great deal - the war against the Herero and Nama has never been officially called by its name.",
  reward=ev("Namibia Votes",
            "SWAPO has won the election. Windhoek's new government invites the Federal Republic to the independence celebrations and asks, politely, what Germany intends to say about the years between 1904 and 1908.",
            [O("Special aid - and a word of regret.", J(infl("NAM", 5), core("welt", support=0.05), money_gdp(-0.001), opinion("NAM", "medium_increase")), ai=60),
             O("Aid, yes. The past is for historians.", J(infl("NAM", 2), opinion("NAM", "small_decrease")), ai=40)],
            pic="GFX_handshake_black"))
F("central_america", "latin_democracy", 0, 1, cost=2, avail="date > 1983.1.1", icon="negotiations", name="Peace in Central America",
  desc="El Salvador's death squads, Nicaragua's Sandinistas, the Contras in Honduras: Washington sees a Soviet beachhead, the Contadora states see a regional war. German volunteers pick coffee in Nicaragua; the CDU's foundation trains Christian democrats in San Salvador.",
  reward=ev("Central America",
            "The Contadora group - Mexico, Venezuela, Colombia and Panama - asks the Europeans to back its peace plan. Washington asks its allies not to legitimise the Sandinistas. Both requests arrive on the same day.",
            [O("Back Contadora - peace before ideology.", J(infl("MEX", 3), infl("NIC", 2), opinion("USA", "small_decrease"), core("welt", support=0.05), party("spd", 0.001)), ai=50),
             O("Stand with Washington.", J(opinion("USA", "medium_increase"), opinion("NIC", "medium_decrease"), core("west", opinion=0.02)), ai=50)],
            pic="GFX_politics_negotiations"))

# =========================================================================== THE UNITED NATIONS
F("permanent_seat", "un_security_council", -1, 1, cost=3, mutex=["european_seat"], avail=f"date > 1990.10.3", icon="un", name="A German Seat",
  desc="The third-largest contributor to the UN budget has no permanent seat at the table where the decisions are made. Bonn asks quietly at first, then openly: if the Security Council is reformed, the Federal Republic wants in - and the five who hold a veto must agree.",
  reward=multi_offer("perm_seat", ["USA", "ENG", "FRA", "SOV", "CHI"], "A Permanent Seat for Germany",
                     "The German government asks for our support for a reform of the Security Council that would give the Federal Republic a permanent seat.",
                     lambda t: J(core("welt", support=0.03), opinion(t, "small_increase")),
                     partner_eff="", accept="We will support Germany.", refuse="The Council is not for reform.", pic="GFX_politics_talks", ai=35))
F("european_seat", "un_security_council", 1, 1, cost=3, mutex=["permanent_seat"], avail=f"date > 1990.10.3", icon="europe", name="A European Seat",
  desc="Not a German seat, but a European one: the foreign minister proposes that the Community speak with one voice in the Security Council, one day with one chair. Paris and London, who already have chairs of their own, listen politely.",
  reward=offer("euro_seat", "FRA", "A European Seat at the United Nations",
               "Bonn proposes that the European Community should in the long run be represented in the Security Council by a single, shared permanent seat.",
               J(core("west", europe=0.05), core("welt", support=0.04), opinion("FRA", "small_increase")),
               partner_eff="", accept="A vision worth discussing.", refuse="France's seat is France's.", pic="GFX_european_parliament", ai=25))

# =========================================================================== SPORT
F("inner_german_sport", "world_cup_1974", -1, 1, cost=2, icon="east_germany", name="Sport across the Border",
  desc="Since Sparwasser's goal in Hamburg the two German states play each other - but rarely, and under protocols negotiated like arms treaties. Bonn proposes a sports agreement: a hundred meetings a year, youth teams, even a friendly in Leipzig.",
  reward=J(kl(3), core("ost", stab=0.02), dv("cwddr_opposition", 1), v("cwger_ostpolitik", 2)))
F("tennis_nation", "olympic_boycott", -1, 1, cost=1, avail="date > 1985.7.1", icon="television", name="Boris and Steffi",
  desc="A seventeen-year-old from Leimen wins Wimbledon with a dive across the grass; a girl from Brühl beats Martina Navratilova. Within a summer, tennis courts are sold out in every suburb and the whole country watches matches that start at two in the afternoon.",
  reward=J(stab(0.02), core("bonn", stab=0.01), core("welt", support=0.02)))
F("berlin_2000", "world_cup_1990", -1, 1, cost=2, avail=f"date > 1990.10.3 {UNITY}", icon="berlin", name="Berlin 2000",
  desc="The divided city is whole again, and Berlin wants the Olympic Games of the year 2000 to prove it. The bid has a budget, a stadium built in 1936 and a resistance movement of its own: 'NOlympia' sets fire to department stores and sends threatening letters to IOC members.",
  reward=ev("The IOC Decides",
            "Monte Carlo, September 1993. Sydney, Beijing, Manchester, Istanbul and Berlin wait for the envelope. The bid committee has been too generous with gifts and too careless with dossiers on the IOC members' private lives; the newspapers have found out.",
            [O("Hope for the best.", "random_list = { 15 = { " + J(core("welt", support=0.05, market=0.03), stab(0.03), state_build(45, "offices"),
                                                                news_all("Olympic Games for Berlin", "The International Olympic Committee has awarded the Games of the year 2000 to Berlin - the first Olympics in a united Germany since 1936.", "GFX_event_olympics")) +
              " } 85 = { " + J(stab(-0.01), core("bonn", pp=-0.02)) + " } }")],
            pic="GFX_event_olympics"))
