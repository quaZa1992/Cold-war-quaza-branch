# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Foreign policy expansion of the West Germany 1970 tree (multiplayer roleplay).

Diplomatic focuses do not simply hand out bonuses: many of them send a proposal to the partner
country. The government there decides for itself (accept / refuse, each with its own
consequences); an AI government decides by its opinion of Bonn. Bonn only gets the result when
the partner agrees. Every proposal is three events in COLDWAR_GDIP: the offer (partner), the
acceptance and the refusal (Bonn).
"""
from cw_lib import *
from events_lib import E, O
from tree import F, core, infl, opinion, state_build, unlock, climate_base
from rivalry import kl, lever

DIP = "COLDWAR_GDIP"
_N = [0]
ERA2 = f"OR = {{ date > 1981.12.31 has_country_flag = {P}_era2 }}"
WALL = f"has_global_flag = {P}_wall_open"
UNITY = f"has_global_flag = {P}_unity_achieved"
OPEN_OR_UNITY = f"OR = {{ {WALL} {UNITY} date > 1990.12.31 }}"
SPD = "check_variable = { ruling_party = 3 }"
UNION = "check_variable = { ruling_party = 1 }"
DARK = f"has_country_flag = {P}_dark_regime"
NOT_DARK = f"NOT = {{ has_country_flag = {P}_dark_regime }}"


def ai_accept(base, tag="GER"):
    return (f"base = {base} modifier = {{ factor = 0.2 has_opinion = {{ target = {tag} value < -25 }} }} "
            f"modifier = {{ factor = 1.5 has_opinion = {{ target = {tag} value > 40 }} }} "
            f"modifier = {{ factor = 0 {tag} = {{ has_country_flag = {P}_dark_regime }} }}")


def ai_refuse(base, tag="GER"):
    return (f"base = {base} modifier = {{ factor = 2 has_opinion = {{ target = {tag} value < -25 }} }} "
            f"modifier = {{ factor = 0.5 has_opinion = {{ target = {tag} value > 40 }} }}")


def offer(key, tag, title, pitch, ger_eff, partner_eff="", accept="We accept.", refuse="We decline.",
          ai=70, pic="GFX_treaty", refuse_eff="", ger_refused=""):
    """Send a proposal to <tag>. Returns the focus reward snippet."""
    _N[0] += 1
    n = _N[0] * 10
    ask, yes, no = f"{DIP}.{n}", f"{DIP}.{n + 1}", f"{DIP}.{n + 2}"
    E(ask, title, "The ambassador of the Federal Republic has asked for an urgent appointment and delivers a proposal from Bonn. " + pitch +
      "\n\nThe cabinet must weigh what the Germans offer against what saying yes would mean - at home, with our neighbours and with our allies.", pic,
      [O(accept, J(partner_eff, f"add_opinion_modifier = {{ target = GER modifier = small_increase }}",
                    f"GER = {{ country_event = {{ id = {yes} days = 1 }} }}"), ai=ai_accept(ai)),
       O(refuse, J(refuse_eff, f"GER = {{ country_event = {{ id = {no} days = 1 }} }}"), ai=ai_refuse(100 - ai))],
      scope="ANY", trig=f"original_tag = {tag}")
    E(yes, f"{title}: Agreed", f"The answer arrives by diplomatic cable, sooner than the Foreign Office expected: [From.GetName] has accepted. '{title}' is no longer a proposal but policy - and the ministries in Bonn now have to make it work.", pic,
      [O("A good day for German diplomacy.", J(ger_eff, f"set_country_flag = cwdip_{key}"))])
    E(no, f"{title}: Refused", f"The ambassador's report is courteous and unambiguous: [From.GetName] will not accept '{title}'. In the Foreign Office the desk officers file the draft away - for another occasion, another approach, or another government.", pic,
      [O("Then not - for now.", J(ger_refused, "add_political_power = 15",
                                   f"set_country_flag = {{ flag = cwdip_{key}_refused days = 365 value = 1 }}"))])
    head = f"cwdip_tt_{key}"
    L(head, f"Our ambassador presents the proposal in §Y[{tag}.GetName]§!. Its cabinet weighs it on its own terms - and may well say no. §GIf it accepts§!, we gain:")
    return J(f"custom_effect_tooltip = {head}", f"effect_tooltip = {{ {ger_eff} }}",
             f"if = {{ limit = {{ country_exists = {tag} }} {tag} = {{ country_event = {{ id = {ask} days = 1 }} }} }}")


def multi_offer(key, tags, title, pitch, ger_eff_each, partner_eff="", **kw):
    """The same proposal to several partners; each acceptance pays out separately."""
    return J(*[offer(f"{key}_{t.lower()}", t, title, pitch, ger_eff_each(t), partner_eff, **kw) for t in tags])


def news_all(title, text, pic):
    """A news line for every other human player (roleplay: everybody sees what Bonn does)."""
    _N[0] += 1
    evid = f"{DIP}.{_N[0] * 10}"
    E(evid, title, text, pic, [O("Noted.")], scope="ANY", trig="NOT = { original_tag = GER }")
    return f"every_other_country = {{ limit = {{ is_ai = no }} country_event = {{ id = {evid} days = 1 }} }}"


FP = "FOCUS_FILTER_POLITICAL"

# =========================================================================== WESTERN INTEGRATION
# --- the Atlantic relationship
F("atlantic_declaration", "g7_bonn", -1, 1, cost=3, avail="date > 1974.1.1", icon="usa", name="The Atlantic Declaration",
  desc="Ottawa, June 1974: after the 'Year of Europe' quarrel, NATO's governments write down what binds them. Bonn wants the Americans to promise to stay - and Washington wants Bonn to promise to pay.",
  reward=J(offer("ottawa", "USA", "The Atlantic Declaration",
                 "Bonn proposes a joint declaration on the future of the Alliance: American troops stay in Europe, the Europeans carry more of the burden, and both sides consult before they act.",
                 J(core("west", ideo=0.05, opinion=0.05), opinion("USA", "medium_increase"), ws(0.02)),
                 partner_eff=J("add_political_power = 25", "add_stability = 0.01"),
                 accept="We sign. The Alliance stands.", refuse="Washington does not need a declaration.")))
F("neutron_quarrel", "atlantic_declaration", -1, 1, cost=2, mutex=["follow_washington"], avail="date > 1977.6.1", icon="nuclear",
  name="The Neutron Bomb Quarrel",
  desc="Schmidt agreed to station the 'enhanced radiation weapon' at great cost to his party - and then Carter cancelled it without asking. Bonn decides it will no longer simply follow.",
  reward=J(core("bonn", stab=0.01), core("west", europe=0.02), opinion("USA", "small_decrease"), opinion("FRA", "small_increase"),
           v("cwger_peace_movement", -3), tt(f"{P}_tt_neutron", "Bonn speaks for itself inside the Alliance: §Ymore European, less automatic§!.")))
F("follow_washington", "atlantic_declaration", 1, 1, cost=2, mutex=["neutron_quarrel"], avail="date > 1977.6.1", icon="usa",
  name="Loyal to Washington",
  desc="Whatever the White House decides, Bonn will not be the ally that makes trouble: a West German security depends on American guarantees, not on French speeches.",
  reward=J(opinion("USA", "medium_increase"), core("west", ideo=0.05), v("cwger_westbindung", 5), v("cwger_peace_movement", 4)))
F("host_nation_support", "follow_washington", 0, 1, cost=3, pre=[["neutron_quarrel", "follow_washington"]], avail="date > 1981.6.1", icon="usa",
  name="Host Nation Support",
  desc="The 1982 Wartime Host Nation Support Agreement: 90,000 West German reservists to move, supply and guard American reinforcements arriving in a crisis.",
  reward=offer("hns", "USA", "Host Nation Support",
               "Bonn offers a wartime host nation support agreement: German reservists will receive, move and protect American reinforcements. In return Washington pledges to send ten divisions within ten days of a crisis.",
               J(core("armee", core=0.05, plan=0.05), lever("allianz", 1), "add_manpower = -15000"),
               partner_eff=J("add_political_power = 30"),
               accept="Ten divisions in ten days. Agreed.", refuse="We will not tie our hands.", pic="GFX_news_german_army"))
F("sdi_research", "host_nation_support", -1, 1, cost=3, mutex=["take_gorbachev_at_word"], avail="date > 1985.3.1", icon="space", filt="FOCUS_FILTER_RESEARCH",
  name="Partners in SDI Research",
  desc="Reagan's Strategic Defense Initiative wants European laboratories. The Union sees contracts for German high technology; the SPD sees a new arms race in space.",
  reward=offer("sdi", "USA", "SDI Research Memorandum",
               "Bonn proposes a memorandum of understanding: West German firms and institutes take part in the research for the Strategic Defense Initiative.",
               J(tech("CAT_electronics", 0.5, 2), tech("CAT_computing", 0.5, 1), core("west", research=0.03), opinion("SOV", "medium_decrease"),
                 v("cwger_peace_movement", 6), tension(1)),
               partner_eff=J("add_political_power = 20"), accept="Welcome aboard.", refuse="This research stays American.", pic="GFX_missiles_on_road"))
F("take_gorbachev_at_word", "host_nation_support", 1, 1, cost=3, mutex=["sdi_research"], avail="date > 1986.6.1", icon="truce",
  name="Take Gorbachev at His Word",
  desc="Davos, February 1987: Genscher tells the West to 'take Gorbachev at his word'. Washington hears 'Genscherism'; Moscow hears an open door.",
  reward=J(tension(-3), kl(4), opinion("SOV", "medium_increase"), opinion("USA", "small_decrease"), core("welt", support=0.05),
           climate_base(2), v("cwger_peace_movement", -4)))
F("inf_treaty", "take_gorbachev_at_word", 0, 1, cost=3, pre=[["sdi_research", "take_gorbachev_at_word"]], avail="date > 1987.6.1", icon="truce",
  name="The Pershing Ia Question",
  desc="The superpowers agree on the double zero option - but 72 old West German Pershing Ia missiles with American warheads stand in the way. Kohl gives them up.",
  reward=J(tension(-4), opinion("SOV", "medium_increase"), opinion("USA", "medium_increase"), v("cwger_peace_movement", -8),
           core("armee", plan=-0.03), kl(4)))
# --- Europe
F("regional_fund", "political_cooperation", 0, 1, cost=3, avail="date > 1974.6.1", icon="europe", name="The Regional Fund",
  desc="The Paris summit of 1974 creates a European fund for poor regions. Bonn pays the most - and buys Rome's and Dublin's goodwill for decades.",
  reward=J(money_gdp(-0.002), infl("ITA", 2), infl("IRE", 3), opinion("ITA", "medium_increase"), opinion("IRE", "medium_increase"),
           core("west", europe=0.02), europe(2)))
F("ep_direct_elections", "regional_fund", 0, 1, cost=2, avail="date > 1978.6.1", icon="europe", name="Electing Europe",
  desc="June 1979: for the first time Europeans elect their parliament directly. Bonn campaigns for a parliament with real powers.",
  reward=J(core("west", europe=0.03, opinion=0.03), europe(3), core("bonn", drift=0.02)))
F("genscher_colombo", "ep_direct_elections", 0, 1, cost=3, avail="date > 1981.6.1", icon="western_europe", name="The Genscher-Colombo Plan",
  desc="November 1981: the German and Italian foreign ministers propose a 'European Act' - common foreign policy, security and culture, decided by majority.",
  reward=offer("genscher_colombo", "ITA", "The Genscher-Colombo Plan",
               "Bonn invites Rome to put a joint proposal for a European Act before the Community: a common foreign policy, security cooperation and majority voting.",
               J(core("west", europe=0.03), infl("ITA", 3), europe(3), core("west", opinion=0.03)),
               partner_eff="add_political_power = 25", accept="Rome signs as co-author.", refuse="Rome prefers to wait for Paris.", pic="GFX_european_parliament"))
F("southern_enlargement", "genscher_colombo", -1, 1, cost=3, avail="date > 1979.6.1", icon="europe", name="Southern Enlargement",
  desc="Greece in 1981, Spain and Portugal in 1986: young democracies that the Federal Republic's party foundations helped to build now join the Community.",
  reward=J(infl("GRE", 3), infl("SPR", 3), infl("POR", 3), opinion("SPR", "medium_increase"), opinion("POR", "medium_increase"), opinion("GRE", "small_increase"),
           money_gdp(-0.002), core("west", trade=0.05)))
F("british_rebate", "genscher_colombo", 1, 1, cost=2, avail="date > 1983.6.1", icon="trade_europe", name="Fontainebleau",
  desc="'I want my money back': Thatcher blocks the Community budget until she gets a rebate. Bonn, the paymaster, decides how much peace is worth.",
  reward=J(money_gdp(-0.001), opinion("ENG", "medium_increase"), opinion("FRA", "small_increase"), core("west", europe=0.02)))
F("weimar_triangle", "southern_enlargement", 1, 1, cost=3, pre=[["southern_enlargement", "british_rebate"]], avail=OPEN_OR_UNITY, icon="poland",
  name="The Weimar Triangle",
  desc="August 1991, Weimar: the foreign ministers of Germany, France and Poland meet for the first time as a group. Germany's eastern neighbour is to be anchored in the West as Germany once was.",
  reward=J(multi_offer("weimar", ["POL", "FRA"], "The Weimar Triangle",
                       "Bonn proposes a standing trilateral forum of the German, French and Polish foreign ministers: Poland's road to the West, prepared together.",
                       lambda t: J(infl(t, 3), opinion(t, "medium_increase")), partner_eff="add_political_power = 20",
                       accept="We will come to Weimar.", refuse="Not in this form.", pic="GFX_politics_talks"),
           core("west", opinion=0.03)))
F("eastern_enlargement", "weimar_triangle", 0, 1, cost=5, avail=f"{OPEN_OR_UNITY} date > 1993.6.1", icon="europe", name="Eastern Enlargement",
  desc="Copenhagen, 1993: the Community promises membership to the new democracies of Central Europe. For Germany, the edge of the West moves from the Elbe to the Bug.",
  reward=J(infl("POL", 4), infl("CZE", 4), infl("HUN", 4), infl("SLV", 3), money_gdp(-0.003), core("west", trade=0.05, europe=0.03), europe(3)))
F("franco_german_youth", "elysee_revival", 0, 2, cost=2, pre=[["elysee_revival"]], icon="france", name="The Youth Office",
  desc="Since 1963 the Franco-German Youth Office has sent millions of pupils across the Rhine. Bonn doubles its budget.",
  reward=J(opinion("FRA", "medium_increase", mutual=True), core("west", opinion=0.03), core("bonn", drift=0.01)))

# =========================================================================== OSTPOLITIK BEYOND THE GDR
F("eastern_relations", "warsaw_treaty", 1, 1, cost=3, avail="date > 1973.6.1", icon="diplomacy", name="Relations with the East",
  desc="After Moscow, Warsaw and Prague, the rest of the Warsaw Pact: diplomatic relations with Budapest and Sofia in December 1973 end the last traces of the Hallstein Doctrine.",
  reward=J(multi_offer("eastrel", ["HUN", "BUL"], "Diplomatic Relations with Bonn",
                       "The Federal Republic proposes full diplomatic relations: embassies, trade agreements and cultural exchange.",
                       lambda t: J(infl(t, 3), opinion(t, "medium_increase")), partner_eff="add_political_power = 15",
                       accept="We establish relations.", refuse="Not without Moscow's blessing.", pic="GFX_handshake_black"),
           dv("cwddr_recognition", 3), core("welt", support=0.03)))
F("romanian_germans", "eastern_relations", -1, 1, cost=3, avail="date > 1977.6.1", icon="refugees", name="The Ransom of the Romanian Germans",
  desc="Bucharest sells its ethnic Germans: so many marks for every Transylvanian Saxon and Banat Swabian allowed to leave. Bonn pays, quietly.",
  reward=offer("romania", "ROM", "Emigration for Credits",
               "Bonn offers hard currency and credits in return for permission for ethnic Germans to emigrate - several thousand a year, without publicity.",
               J("add_manpower = 8000", core("bonn", stab=0.01), party("cdu", 0.002), money_gdp(-0.001)),
               partner_eff=money_gdp(0.002), accept="The price is acceptable.", refuse="Romania's citizens are not for sale.", pic="GFX_German_migrant"))
F("polish_emigration", "eastern_relations", 1, 1, cost=3, avail="date > 1975.6.1", icon="poland", name="Credits for Emigration",
  desc="Helsinki, August 1975: Schmidt and Gierek agree on a billion marks in credits and pension payments - and exit permits for 125,000 ethnic Germans.",
  reward=offer("poland_credit", "POL", "Credits for Emigration",
               "Bonn offers a billion marks in low-interest credits and a pension settlement. In return 125,000 ethnic Germans may leave for the Federal Republic over four years.",
               J("add_manpower = 15000", infl("POL", 3), core("bonn", stab=0.01), money_gdp(-0.002), party("cdu", 0.002)),
               partner_eff=J(money_gdp(0.003), "add_stability = 0.01"), accept="Warsaw accepts the credit.", refuse="Warsaw will not trade people.", pic="GFX_German_migrant"))
F("yugoslav_partnership", "eastern_relations", 0, 2, cost=3, pre=[["romanian_germans", "polish_emigration"]], icon="diplomacy", name="Tito's Germans",
  desc="Half a million Yugoslav guest workers live in the Federal Republic. Belgrade wants credits instead of reparations; Bonn wants Belgrade to stop sheltering terrorists.",
  reward=offer("yugoslavia", "SER", "A Partnership with Belgrade",
               "Bonn offers long-term capital aid and a social insurance agreement for Yugoslav workers. In return Belgrade cooperates against terrorists who use the country as a refuge.",
               J(infl("SER", 4), v("cwger_raf_milieu", -2), core("wehrhaft", detect=0.03), core("welt", market=0.02)),
               partner_eff=money_gdp(0.002), accept="Yugoslavia accepts.", refuse="Non-alignment means no conditions.", pic="GFX_handshake_black"))
F("solidarity_support", "yugoslav_partnership", -1, 1, cost=2, mutex=["quiet_diplomacy_poland"], avail="date > 1980.8.1", icon="speech",
  name="Parcels for Poland",
  desc="Martial law in Poland. Millions of West Germans send food parcels; the government sends money to the church - and asks itself whether it should also speak out for Solidarność.",
  reward=J(opinion("POL", "medium_decrease"), opinion("USA", "small_increase"), dv("cwddr_opposition", 2), core("west", ideo=0.03), kl(-3), core("bonn", stab=0.01)))
F("quiet_diplomacy_poland", "yugoslav_partnership", 1, 1, cost=2, mutex=["solidarity_support"], avail="date > 1980.8.1", icon="negotiations",
  name="Quiet Diplomacy",
  desc="Schmidt is at Honecker's side at the Werbellinsee on the day martial law is declared - and stays for the talks. Détente must not become a casualty of Warsaw.",
  reward=J(kl(4), opinion("SOV", "small_increase"), opinion("USA", "small_decrease"), climate_base(1), v("cwger_peace_movement", -2)))
F("soviet_germans", "solidarity_support", 1, 1, cost=3, pre=[["solidarity_support", "quiet_diplomacy_poland"]], avail="date > 1986.12.1", icon="refugees",
  name="The Soviet Germans",
  desc="Two million ethnic Germans live in Kazakhstan and Siberia. Under Gorbachev the gates open - if Bonn asks.",
  reward=offer("sovgermans", "SOV", "Exit Permits for Soviet Germans",
               "Bonn asks Moscow to allow ethnic Germans to emigrate freely and offers economic cooperation and help with consumer goods in return.",
               J("add_manpower = 20000", core("bonn", stab=0.01), party("cdu", 0.003), money_gdp(-0.001)),
               partner_eff=J(money_gdp(0.002), "add_political_power = 20"), accept="Let them go.", refuse="They are Soviet citizens.", pic="GFX_German_migrant"))
F("bonn_declaration_1989", "soviet_germans", 0, 1, cost=3, avail="date > 1988.10.1", icon="soviet", name="The Bonn Declaration",
  desc="June 1989: Gorbachev in Bonn, crowds cheering 'Gorbi!'. The joint declaration recognises the right of every people to choose its own political system.",
  reward=offer("bonn_decl", "SOV", "The Bonn Declaration",
               "Bonn invites the Soviet leader for a state visit and proposes a joint declaration: the right of all peoples and states to determine their own fate, freely.",
               J(tension(-4), kl(6), opinion("SOV", "large_increase"), v("cwger_unity", 6), core("welt", support=0.05)),
               partner_eff=J("add_political_power = 40", "add_stability = 0.02"), accept="We come to Bonn.", refuse="The time is not right.", pic="GFX_politics_talks", ai=60))
F("hungarian_border", "bonn_declaration_1989", 0, 1, cost=3, avail="date > 1989.4.1", icon="borders", name="The Hungarian Door",
  desc="Hungary is cutting its border fence with Austria. Thousands of East Germans camp in Budapest. Bonn can help Budapest decide - with a credit of 500 million marks.",
  reward=offer("hungary_border", "HUN", "The Hungarian Door",
               "Bonn offers a credit of 500 million marks and asks Budapest to let the East German refugees in Hungary leave for the West.",
               J(dv("cwddr_exit_pressure", 12), dv("cwddr_sed_control", -5), infl("HUN", 5), v("cwger_unity", 5)),
               partner_eff=J(money_gdp(0.003), "add_stability = 0.01"), accept="We open the border.", refuse="We will not anger East Berlin.", pic="GFX_German_migrant", ai=55))

# =========================================================================== CIVILIAN POWER: THE WIDER WORLD
# --- Asia
F("recognise_china", "development_ministry", -1, 2, cost=3, pre=[["development_ministry"]], avail="date > 1972.3.1", icon="diplomacy", name="Relations with Beijing",
  desc="October 1972: Walter Scheel flies to Beijing. Mao wants a strong Federal Republic as a counterweight to Moscow; Bonn wants a market of 800 million.",
  reward=offer("china", "CHI", "Diplomatic Relations with Bonn",
               "The Federal Republic proposes diplomatic relations and a trade agreement. Beijing sees a counterweight to Moscow in Europe.",
               J(infl("CHI", 4), core("welt", market=0.05), opinion("SOV", "small_decrease"), opinion("TAI", "medium_decrease")),
               partner_eff="add_political_power = 25", accept="China welcomes the Federal Republic.", refuse="Bonn is too close to Washington.", pic="GFX_handshake_black"))
F("japan_partnership", "recognise_china", -1, 1, cost=2, icon="trade_europe", name="Two Export Champions",
  desc="Tokyo and Bonn: two defeated powers that became the world's export champions. They agree to talk about trade before Washington talks to them about it.",
  reward=offer("japan", "JAP", "A German-Japanese Consultation",
               "Bonn proposes regular government consultations with Tokyo on trade, currency and technology.",
               J(core("welt", market=0.05), infl("JAP", 2), tech("CAT_computing", 0.25, 1)),
               partner_eff="add_political_power = 20", accept="Agreed.", refuse="Our trade policy is our own.", pic="GFX_stock_market"))
F("cap_anamur", "recognise_china", 1, 1, cost=2, avail="date > 1979.1.1", icon="refugees", name="Cap Anamur",
  desc="1979: a freighter chartered by German citizens fishes Vietnamese boat people out of the South China Sea. The government decides to give them a home.",
  reward=J(core("bonn", stab=0.01), core("welt", support=0.05), core("west", opinion=0.03), opinion("VIE", "small_decrease"), party("greens", 0.001)))
F("india_partnership", "japan_partnership", 1, 1, cost=3, pre=[["japan_partnership", "cap_anamur"]], icon="trade_europe", name="Partnership with India",
  desc="The world's largest democracy is also the largest recipient of West German aid: steelworks at Rourkela, the IIT Madras, credits for the Green Revolution.",
  reward=offer("india", "RAJ", "A Development Partnership",
               "Bonn offers a long-term development partnership: capital aid, technical universities and industrial cooperation.",
               J(infl("RAJ", 4), core("welt", cap=1, eff=0.03)), partner_eff=money_gdp(0.002),
               accept="India accepts.", refuse="We prefer Soviet terms.", pic="GFX_decision_generic_factory"))
# --- the Middle East
F("euro_arab_dialogue", "middle_east_balance", 0, 2, cost=3, pre=[["middle_east_balance"]], avail="date > 1974.1.1", icon="oil", name="The Euro-Arab Dialogue",
  desc="After the oil embargo, the Community opens a dialogue with the Arab League: oil for technology, security of supply for a hearing on Palestine.",
  reward=J(infl("EGY", 2), infl("SAU", 2), infl("ALG", 2), core("energie", fossil=-0.02), opinion("ISR", "small_decrease")))
F("venice_declaration", "euro_arab_dialogue", -1, 1, cost=2, mutex=["israel_first"], avail="date > 1980.1.1", icon="diplomacy", name="The Venice Declaration",
  desc="June 1980: the Nine recognise the Palestinians' right to self-determination and call for the PLO to be associated with peace talks.",
  reward=J(infl("JOR", 3), infl("EGY", 2), opinion("ISR", "medium_decrease"), opinion("USA", "small_decrease"), core("welt", support=0.05)))
F("israel_first", "euro_arab_dialogue", 1, 1, cost=2, mutex=["venice_declaration"], avail="date > 1980.1.1", icon="diplomacy", name="Special Responsibility",
  desc="Bonn's relationship with Israel is not like any other. The Federal Republic refuses to sign anything that Jerusalem sees as a threat.",
  reward=J(opinion("ISR", "large_increase"), infl("ISR", 3), opinion("SAU", "small_decrease"), core("west", opinion=0.03)))
F("saudi_tanks", "venice_declaration", 0, 1, cost=3, pre=[["venice_declaration", "israel_first"]], avail="date > 1981.1.1", icon="leopard",
  name="Leopards for Riyadh?",
  desc="Saudi Arabia wants 300 Leopard 2 tanks. The money is enormous, the guidelines forbid exports into areas of tension, and Begin calls Schmidt a man who served Hitler.",
  reward=offer("saudi_tanks", "SAU", "The Leopard Deal",
               "Bonn offers to sell Leopard 2 main battle tanks and the training that comes with them.",
               J(money_gdp(0.004), infl("SAU", 5), opinion("ISR", "large_decrease"), corruption(True, 40), v("cwger_rechtsstaat", -2)),
               partner_eff=J("add_war_support = 0.02", "army_experience = 10"),
               accept="Riyadh buys.", refuse="We buy American.", pic="GFX_GER_Panzer_strasse", ai=80))
# --- Africa and Latin America
F("lome_convention", "africa_development", 0, 1, cost=3, avail="date > 1974.10.1", icon="trade_europe", name="The Lomé Convention",
  desc="February 1975: the Community opens its markets to 46 African, Caribbean and Pacific states and stabilises their export earnings.",
  reward=J(infl("SEN", 2), infl("KEN", 2), infl("NIG", 3), infl("TNZ", 2), core("welt", cap=1), money_gdp(-0.001)))
F("namibia_contact_group", "lome_convention", -1, 1, cost=2, avail="date > 1977.3.1", icon="un", name="The Contact Group",
  desc="Five Western members of the Security Council - including the Federal Republic - try to negotiate Namibia's independence from South Africa. Twenty thousand German-speakers live there.",
  reward=J(core("welt", support=0.05), opinion("SAF", "small_decrease"), infl("NAM", 3), opinion("AGL", "small_increase")))
F("apartheid_sanctions", "namibia_contact_group", -1, 1, cost=2, mutex=["pretoria_trade"], avail="date > 1984.6.1", icon="embargo", name="Sanctions against Apartheid",
  desc="Bonn joins the Community's sanctions: no new investment, no iron and steel, no krugerrands.",
  reward=J("if = { limit = { country_exists = SAF } SAF = { " + f"{P}_sanction_prev_economic = yes" + " } }", opinion("SAF", "large_decrease"),
           core("welt", support=0.05), party("greens", -0.002), faction("bdi", -4)))
F("pretoria_trade", "namibia_contact_group", 1, 1, cost=2, mutex=["apartheid_sanctions"], avail="date > 1984.6.1", icon="trade_europe", name="Change through Trade",
  desc="Daimler, Siemens and Hoechst want to stay: sanctions hurt black workers first, they say. Strauß visits Pretoria.",
  reward=J(opinion("SAF", "medium_increase"), core("welt", market=0.03, support=-0.05), faction("bdi", 5), party("greens", 0.002), v("cwger_peace_movement", 2)))
F("chile_exiles", "brazil_nuclear_deal", 0, 1, cost=2, avail="date > 1973.9.11", icon="refugees", name="Refuge from Santiago",
  desc="After Pinochet's coup, the West German embassy in Santiago fills with people fleeing the junta. Bonn decides how many it will take - and whether to keep selling to the generals.",
  reward=J(opinion("CHL", "medium_decrease"), core("welt", support=0.05), core("bonn", drift=0.02), party("spd", 0.002)))
F("latin_democracy", "chile_exiles", 0, 1, cost=3, avail="date > 1982.6.1", icon="socdem", name="Democracy in Latin America",
  desc="The party foundations are present wherever generals hand back power: Buenos Aires in 1983, Brasília in 1985, Santiago in 1990.",
  reward=J(infl("ARG", 3), infl("BRA", 2), infl("CHL", 2), core("welt", support=0.05)))
# --- arms control and the United Nations
F("npt_ratification", "cultural_diplomacy", 3, 1, cost=2, avail="date > 1974.1.1", icon="nuclear", name="Ratify the Non-Proliferation Treaty",
  desc="Signed in 1969, ratified in 1975: the Federal Republic renounces nuclear weapons of its own for good - and gets guaranteed access to civilian nuclear technology.",
  reward=J(f"set_country_flag = {P}_npt_ratified", "set_country_flag = GER_no_nuclear", tension(-2), opinion("SOV", "medium_increase"), opinion("USA", "small_increase"), core("welt", support=0.05),
           tt(f"{P}_tt_npt", "§RThe 'national option' for nuclear weapons is closed for good.§!")))
F("un_entry", "npt_ratification", 0, 1, cost=2, avail=f"has_country_flag = {P}_un_member", icon="un", name="Germany at the United Nations",
  desc="18 September 1973: the black, red and gold flag is raised on the East River - next to the GDR's. Bonn now has a voice in the General Assembly, and a delegation to staff.",
  reward=J(core("welt", support=0.05, cap=1), opinion("FRA", "small_increase"), opinion("ENG", "small_increase")))
F("csce_followup", "un_entry", 0, 1, cost=3, pre=[["un_entry", "npt_ratification"]], avail="date > 1977.6.1", icon="diplomacy", name="Belgrade, Madrid, Vienna",
  desc="The CSCE follow-up conferences: where the West reads out the names of prisoners and the East counts the tank divisions. Bonn's diplomats are always the last to leave the room.",
  reward=J(tension(-2), kl(2), dv("cwddr_opposition", 2), core("welt", support=0.03), core("west", opinion=0.03)))
F("rambouillet", "csce_followup", 0, 1, cost=2, avail="date > 1975.10.1", icon="usa", name="The Summit at Rambouillet",
  desc="November 1975: Giscard invites the leaders of the six largest Western economies to a château - the birth of the world economic summits.",
  reward=offer("rambouillet", "FRA", "A Summit of the Big Economies",
               "Bonn and Paris propose an informal summit of the leading Western economies to coordinate currencies, energy and trade after the oil shock.",
               J(core("welt", market=0.05), core("modell", fac=0.01), opinion("FRA", "medium_increase")),
               partner_eff="add_political_power = 25", accept="Paris will host.", refuse="Paris has its own plans.", pic="GFX_politics_talks"))
