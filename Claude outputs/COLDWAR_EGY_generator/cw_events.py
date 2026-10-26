# IMPERIA CW — Cold War: Egypt 1970 content generator.
# COLDWAR | Events and offer events of the Egypt 1970 focus tree (English texts).
# Offers follow the multiplayer rule: the focus only sends the offer; the other
# country (player or AI) decides, and every effect happens in its answer.

PIC = {
    "egy": "GFX_egy_flagg", "uar": "GFX_united_arab_republic", "uar_news": "GFX_news_united_arab_republic",
    "arab_conf": "GFX_news_arab_conference", "camp_david": "GFX_camp_david_eve", "mb": "GFX_politics_muslim_brotherhood",
    "islamic_rally": "GFX_generic_islamic_rally", "riot": "GFX_news_arab_riot_police", "copt": "GFX_christian_event",
    "suez_oil": "GFX_defense_line_suez", "soviet": "GFX_soviet_union_flag", "usa": "GFX_israel_usa",
    "grain": "GFX_grain_deal", "bank": "GFX_banking_crisis", "army": "GFX_syrian_arab_army", "saudi": "GFX_saudi_taif",
    "libya": "GFX_libya_muammar_gaddafi", "factory": "GFX_generic_factory", "oil": "GFX_generic_oil_field",
    "military": "GFX_Military_Reform", "nile": "GFX_defense_line_nile", "farm": "GFX_aleppo_spring_farmers",
    "coup": "GFX_army_coup_event", "hospital": "GFX_hospital", "crowd": "GFX_generic_labor_crowd",
}

# ---------------------------------------------------------------- plain events
# key: (id, picture, title, desc, options[(text, code, ai_factor)], extra)
EVENTS = {}


def ev(key, n, pic, title, desc, options, **extra):
    EVENTS[key] = dict(n=n, pic=PIC.get(pic, pic), title=title, desc=desc, options=options, **extra)


ev("intro", 1, "egy", "A Nation at War of Attrition",
   "January 1970. Along the Suez Canal Egyptian and Israeli guns trade fire every day, and Israeli jets strike deep into the Nile Valley. "
   "Three years after the Naksa, President Gamal Abdel Nasser still commands the loyalty of the Arab street, yet his health is failing. "
   "Soviet advisers fill the ministries and the missile sites, the Canal lies closed and silent, and the Arab Socialist Union speaks of victory "
   "while the economy groans under the weight of the front. Whoever governs Egypt in the coming decade must decide what kind of country it will be.",
   [("What has been taken by force can only be regained by force.", "", 1)])

ev("succession", 2, "egy", "Who Follows the Rais?",
   "Behind the closed doors of the Arab Socialist Union the question no one dares ask aloud is being asked everywhere: who will follow Nasser? "
   "Vice President Anwar as-Sadat is considered a harmless placeholder. Ali Sabri commands the party apparatus and the confidence of Moscow. "
   "War Minister Mohamed Fawzi speaks for the officers, while Zakaria Mohieddin's technocrats wait in the wings. The answer will shape the Egypt of the seventies.",
   [("The Revolution will choose its heir.", "", 1)])

ev("sabri_trial", 3, "coup", "The Trial of the Centres of Power",
   "In May 1971 the President moved first. Ali Sabri, Sharawi Gomaa, Sami Sharaf and Mohamed Fawzi resigned in a body, hoping to bring the government down; "
   "instead they were arrested within hours. The tapes of the security service were burned in public, and the trial of the 'centres of power' "
   "has become a spectacle of a new order that promises the rule of law.",
   [("The Corrective Revolution has triumphed.", "add_political_power = 25", 1)])

ev("bread_intifada", 4, "riot", "The Bread Intifada",
   "The announcement that subsidies on bread, sugar and cooking oil would be cut has brought hundreds of thousands into the streets of Cairo and Alexandria. "
   "Police stations burn, the Central Security Forces are overwhelmed, and the army stands ready at the edge of the capital. "
   "The government must decide whether to restore the subsidies or to see the reform through.",
   [("Restore the subsidies.",
     "add_stability = 0.05\n"
     "custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_EGY_economy_modifier }\n"
     "add_to_variable = { COLDWAR_EGY_economy_social_cost_multiplier_modifier = COLDWAR_EGY_subsidy_restore tooltip = @TT:social_cost_multiplier_modifier@ }\n"
     "clear_variable = COLDWAR_EGY_subsidy_restore", 3),
    ("The reform stands.",
     "add_timed_idea = { idea = COLDWAR_EGY_bread_riots days = 180 }\nclear_variable = COLDWAR_EGY_subsidy_restore", 1)])

ev("rayan", 5, "bank", "The Rayan Scandal",
   "For years the Islamic investment companies promised returns no bank could match, and millions of small savers entrusted them with their remittances. "
   "Now the largest of them can no longer pay. Depositors besiege its offices, and the government must decide whether it can still regulate the sector in time.",
   [("Let them collapse.",
     "set_temp_variable = { COLDWAR_EGY_gdp_share = 0.005 }\nCOLDWAR_EGY_pay_gdp_share = yes\nadd_stability = -0.03", 1),
    ("Regulate them at once.", "add_political_power = -50", 2)])

ev("coptic_unrest", 6, "copt", "Unrest among the Copts",
   "The new legal order has alarmed Egypt's Coptic Christians. Pope Shenouda has cancelled the Easter celebrations in protest, "
   "churches in Upper Egypt report attacks, and Coptic notables ask the government for guarantees. The ulema watch the response closely.",
   [("Guarantee the protection of the Copts.",
     "set_temp_variable = { coptic_opinion_change = 10 }\nmodify_coptic_opinion_effect = yes\n"
     "set_temp_variable = { temp_opinion = -5 }\nCOLDWAR_EGY_change_the_ulema_opinion_exact = yes", 1),
    ("The law will be applied without exception.",
     "add_stability = -0.03\nset_temp_variable = { temp_opinion = 5 }\nCOLDWAR_EGY_change_the_ulema_opinion_exact = yes", 1)])

ev("csf_mutiny", 7, "riot", "Mutiny of the Central Security Forces",
   "Rumours that their term of service would be extended by a year have driven thousands of poorly paid Central Security conscripts into revolt. "
   "Hotels near the pyramids burn and the army has to be called in to restore order. Cheap order has proven expensive.",
   [("Send in the army.", "add_stability = -0.05\nset_temp_variable = { temp_opinion = 5 }\nCOLDWAR_EGY_change_the_military_opinion_exact = yes", 1)],
   triggered=dict(trigger="has_country_flag = COLDWAR_EGY_cheap_order\ndate > 1986.2.1", mtth=60))

ev("league_suspension", 8, "arab_conf", "Suspended from the Arab League",
   "Meeting in Baghdad, the Arab League has answered our separate peace with Israel: Egypt's membership is suspended, the League's headquarters will leave Cairo, "
   "and one Arab capital after another recalls its ambassador. Peace has been won, but the Arab world now treats us as a stranger.",
   [("History will judge who was right.", "", 1)])

ev("nasser_health", 9, "hospital", "The Rais's Heart",
   "The Soviet cardiologists have bought the President time, but not health. After another exhausting round of summits Nasser collapses at home, "
   "and his doctors can only advise rest he will never take.",
   [("He will recover.", "", 1)],
   triggered=dict(trigger="has_country_flag = COLDWAR_EGY_nasser_ailing", mtth=365),
   immediate="random_list = {\n75 = { add_stability = -0.01 }\n25 = { COLDWAR_EGY_nasser_dies = yes }\n}")

ev("eastern_flank", 10, "army", "The Eastern Flank",
   "Cairo has asked its partners of the Arab Joint Defense Command to keep the eastern front active, so that Israel cannot concentrate its strength on the Canal. "
   "Our headquarters report that the call has been heard.",
   [("Every front is our front.", "", 1)])

ev("lease", 11, "soviet", "Rent for the Eskadra",
   "The Soviet Mediterranean squadron has paid the annual rent for its facilities in Alexandria and Mersa Matruh.",
   [("Welcome income.", "", 1)], hidden=True)

ev("uar_news", 12, "uar_news", "The United Arab Republic Is Back",
   "From Cairo comes the proclamation that the United Arab Republic has been restored. Egypt and its partners will share one flag, one army and one foreign policy. "
   "Whether the new union will outlast its predecessor of 1958 remains to be seen.",
   [("A new chapter for the Arab world.", "", 1)], news=True)

# ---------------------------------------------------------------- offers
# targets: tags; accept/decline code runs in the target country's scope (FROM = Egypt)
OFFERS = {}


def offer(focus, n, pic, targets, title, desc, accept, accept_code, decline="We must decline.", decline_code="",
          ai_base=50, ai_mods="", limit="", **extra):
    OFFERS[focus] = dict(n=n, pic=PIC.get(pic, pic), targets=targets, title=title, desc=desc, accept=accept,
                         accept_code=accept_code, decline=decline, decline_code=decline_code, ai_base=ai_base,
                         ai_mods=ai_mods, limit=limit, **extra)


OPINION_AI = ("modifier = { factor = 0 has_war_with = FROM }\n"
              "modifier = { factor = 2 has_opinion = { target = FROM value > 50 } }\n"
              "modifier = { factor = 0.25 has_opinion = { target = FROM value < 0 } }")
TRADE = ("set_temp_variable = { receiver_nation = THIS.id }\nset_temp_variable = { sender_nation = FROM.id }\nset_improved_trade_agreement = yes")


def mutual(op=25, mod="COLDWAR_EGY_partnership"):
    return f"add_opinion_modifier = {{ target = FROM modifier = {mod} }}\nreverse_add_opinion_modifier = {{ target = FROM modifier = {mod} }}"


def gdp_to_egypt(share):
    """Egypt receives `share` of its own GDP; the payer pays the same sum."""
    return ("FROM = { set_temp_variable = { COLDWAR_EGY_gdp_share = " + share + " } COLDWAR_EGY_receive_gdp_share = yes }\n"
            "set_temp_variable = { treasury_change = FROM.COLDWAR_EGY_last_transfer }\nmultiply_temp_variable = { treasury_change = -1 }\nmodify_treasury_effect = yes")


offer("em_comecon_partnership", 101, "soviet", ["SOV"], "Egypt Seeks a Cooperation Agreement",
      "Cairo proposes a long-term agreement on trade, credits and technical cooperation with the socialist community. Egyptian cotton would flow north, Soviet machinery south.",
      "Sign the agreement.", TRADE + "\n" + mutual(), ai_base=70, ai_mods=OPINION_AI)
offer("we_the_usaid_mission", 102, "usa", ["USA"], "Egypt Requests American Aid",
      "The Egyptian government asks for a USAID mission to Cairo: grain, infrastructure loans and advisers for its reforms. It would be the first such programme since 1967.",
      "Open the mission.",
      "FROM = { add_timed_idea = { idea = COLDWAR_EGY_american_aid days = 1095 } }\n"
      "set_temp_variable = { percent_change = 10 }\nset_temp_variable = { tag_index = THIS.id }\nset_temp_variable = { influence_target = FROM.id }\nchange_influence_percentage = yes",
      ai_base=60, ai_mods=OPINION_AI)
offer("we_americas_partner", 103, "usa", ["USA"], "Egypt Proposes a Strategic Partnership",
      "Cairo asks Washington to recognise Egypt as a strategic partner of the United States, with training programmes and preferential access to American arms.",
      "Egypt is our partner.", "FROM = { add_ideas = COLDWAR_EGY_us_strategic_partner }\n" + mutual(), ai_base=60, ai_mods=OPINION_AI)
offer("ndp_americas_shield", 104, "usa", ["USA"], "Egypt Proposes a Strategic Partnership",
      "Cairo asks Washington to recognise Egypt as a strategic partner of the United States, with training programmes and preferential access to American arms.",
      "Egypt is our partner.", "FROM = { add_ideas = COLDWAR_EGY_us_strategic_partner }\n" + mutual(), ai_base=60, ai_mods=OPINION_AI)
offer("asu_petrodollars_to_cairo", 105, "saudi", ["SAU", "KUW", "UAE"], "Deposits for the Central Bank of Egypt",
      "Cairo asks the oil states to place part of their reserves with the Central Bank of Egypt, to steady the pound and finance reconstruction.",
      "Deposit the funds.", gdp_to_egypt("0.005") + "\n" + mutual(), ai_base=40, ai_mods=OPINION_AI)
offer("mb_islamic_banking", 106, "saudi", ["SAU"], "Seed Capital for Islamic Banking",
      "The new Egyptian government asks for seed capital to found banks that operate without interest, in accordance with the sharia.",
      "Provide the capital.", gdp_to_egypt("0.01") + "\n" + mutual(), ai_base=60, ai_mods=OPINION_AI)
offer("mb_gulf_brothers_capital", 107, "saudi", ["SAU", "KUW", "QAT"], "Investment in Egypt",
      "Cairo invites Gulf investors to finance Egyptian housing, banking and industry, promising them a privileged place in the new economy.",
      "Invest in Egypt.", "FROM = { add_timed_idea = { idea = COLDWAR_EGY_gulf_capital days = 1095 } }\n" + mutual(), ai_base=50, ai_mods=OPINION_AI)
offer("tag_the_belgrade_credit", 108, "factory", ["SER"], "An Industrial Credit for Egypt",
      "Egypt asks its old partner of the Non-Aligned Movement for an industrial credit, to be repaid in cotton and textiles.",
      "Grant the credit.",
      gdp_to_egypt("0.01") + "\nFROM = { set_temp_variable = { debt_change = FROM.COLDWAR_EGY_last_transfer } multiply_temp_variable = { debt_change = 0.5 } modify_debt_effect = yes }\n" + mutual(),
      ai_base=60, ai_mods=OPINION_AI)
offer("fn_nile_basin_water_talks", 109, "nile", ["SUD", "ETH"], "Talks on the Nile Waters",
      "Cairo proposes an agreement on the use of the Nile waters, with joint monitoring and shared projects instead of rivalry over every drop.",
      "Sign the water agreement.", mutual() + "\nadd_timed_idea = { idea = COLDWAR_EGY_nile_water_agreement days = 1825 }\nFROM = { add_timed_idea = { idea = COLDWAR_EGY_nile_water_agreement days = 1825 } }",
      ai_base=60, ai_mods=OPINION_AI)
offer("cp_the_treaty_stronger_than_friendship", 110, "soviet", ["SOV"], "A Treaty Stronger than Friendship",
      "Cairo proposes to deepen the Treaty of Friendship: more advisers, more air-defence systems and a common front against imperialism in the Middle East.",
      "Deepen the treaty.", mutual() + "\nFROM = { add_tech_bonus = { name = COLDWAR_EGY_soviet_sam_bonus bonus = 0.5 uses = 1 category = CAT_surface_to_air_missiles } }",
      ai_base=70, ai_mods=OPINION_AI)
offer("cp_facilities_for_the_eskadra", 111, "soviet", ["SOV"], "Facilities for the Fifth Eskadra",
      "Egypt offers the Soviet Mediterranean squadron permanent facilities in Alexandria and Mersa Matruh, against an annual rent.",
      "Accept the facilities.",
      "FROM = { give_military_access = ROOT set_country_flag = COLDWAR_EGY_eskadra_lease country_event = { id = COLDWAR_EGY.11 days = 365 } }\n" + mutual(),
      ai_base=70, ai_mods=OPINION_AI)
offer("ecp_comecon_membership", 112, "soviet", ["SOV"], "Egypt Applies to the Comecon",
      "The People's Republic of Egypt applies for membership of the Council for Mutual Economic Assistance and offers to integrate its plan with the socialist division of labour.",
      "Welcome Egypt to the Comecon.", "FROM = { add_ideas = COLDWAR_EGY_comecon_member }\n" + mutual(), ai_base=70, ai_mods=OPINION_AI)
offer("ndp_the_food_security_programme", 113, "grain", ["USA"], "American Wheat for Egypt",
      "Cairo asks for long-term deliveries of American wheat under the PL-480 programme to keep bread cheap in Egypt's cities.",
      "Ship the wheat.", "FROM = { add_timed_idea = { idea = COLDWAR_EGY_american_wheat days = 1095 } }\n" + mutual(), ai_base=60, ai_mods=OPINION_AI)
offer("ndp_the_jerusalem_initiative", 114, "camp_david", ["ISR"], "The President of Egypt in Jerusalem",
      "In a move no one thought possible, the President of Egypt has come to Jerusalem and offered a full peace treaty: recognition and normal relations, "
      "in exchange for the return of the Sinai in stages.",
      "Sign the peace treaty.",
      "COLDWAR_EGY_return_sinai = yes\nFROM = { set_country_flag = COLDWAR_EGY_peace_with_israel COLDWAR_EGY_peace_with_israel_consequences = yes }\n" + mutual(mod="COLDWAR_EGY_peace_treaty"),
      decline="We cannot accept these terms.", ai_base=40,
      ai_mods="modifier = { factor = 2 has_country_flag = COLDWAR_EGY_us_mediation }",
      extra_options=[("Negotiate further.", "FROM = { add_political_power = 25 }", 30)])
offer("lib_the_eec_association", 115, "egy", ["FRA", "GER", "ITA"], "An Association Agreement with Egypt",
      "Cairo proposes an association agreement: lower tariffs for Egyptian cotton and textiles, and a market of forty million for European industry.",
      "Sign the agreement.", TRADE + "\n" + mutual(), ai_base=60, ai_mods=OPINION_AI)
offer("azh_the_riyadh_axis", 116, "saudi", ["SAU"], "An Alliance of the Scholars",
      "The scholars of al-Azhar propose a lasting alliance with the Kingdom: shared missions, shared universities and Saudi support for the Islamic order in Egypt.",
      "Support our Egyptian brothers.", gdp_to_egypt("0.015") + "\n" + mutual(mod="COLDWAR_EGY_alliance_of_scholars"), ai_base=70, ai_mods=OPINION_AI)
offer("mon_the_crown_development_fund", 117, "saudi", ["SAU", "KUW", "JOR"], "The Crown Development Fund",
      "The restored King of Egypt asks his fellow monarchs to support a development fund that will prove the crown can deliver what the republic could not.",
      "Contribute to the fund.", gdp_to_egypt("0.005") + "\n" + mutual(), ai_base=60, ai_mods=OPINION_AI)
offer("mon_the_shahs_friendship", 118, "oil", ["PER"], "An Alliance of Crowns",
      "Cairo recalls the old ties between the houses of Muhammad Ali and Pahlavi and proposes a union of crowns, backed by an oil credit.",
      "Embrace the alliance.", gdp_to_egypt("0.005") + "\n" + mutual(mod="COLDWAR_EGY_alliance_of_crowns"), ai_base=60, ai_mods=OPINION_AI)
offer("fn_nile_partnership", 119, "nile", ["SUD"], "A Joint Nile Authority",
      "Egypt proposes a joint authority for the Nile valley: shared irrigation planning, shared data and open trade along the river.",
      "Found the authority.",
      TRADE + "\nadd_timed_idea = { idea = COLDWAR_EGY_joint_nile_authority days = 1825 }\nFROM = { add_timed_idea = { idea = COLDWAR_EGY_joint_nile_authority days = 1825 } }",
      ai_base=60, ai_mods=OPINION_AI)
offer("accept_the_ceasefire", 120, "suez_oil", ["ISR"], "Egypt Accepts the Ceasefire",
      "Cairo has accepted the American ceasefire proposal for the Suez front. The guns along the Canal would fall silent; the Sinai would remain under our control until a treaty is signed.",
      "Accept the ceasefire.", "COLDWAR_EGY_ceasefire_status_quo = yes\nFROM = { COLDWAR_EGY_ceasefire_accepted = yes }",
      decline="The war continues.", decline_code="FROM = { add_war_support = 0.05 }", ai_base=60)
offer("coordinate_the_oil_weapon", 121, "oil", ["SAU", "LBA", "IRQ", "KUW"], "Egypt Asks for the Oil Weapon",
      "Cairo asks the Arab oil producers to use their oil as a weapon: an embargo on the states that support Israel. The decision remains entirely ours.",
      "We will consider it.", "add_opinion_modifier = { target = FROM modifier = COLDWAR_EGY_arab_solidarity }\ncustom_effect_tooltip = COLDWAR_EGY_oil_weapon_request_tt",
      decline="Oil and politics do not mix.", ai_base=60)
offer("kilometre_101", 122, "suez_oil", ["ISR"], "Talks at Kilometre 101",
      "In a tent at Kilometre 101 on the Cairo-Suez road, Egyptian and Israeli officers have begun to talk directly for the first time. Cairo proposes a disengagement of forces.",
      "Agree to disengage.", "COLDWAR_EGY_ceasefire_status_quo = yes\nFROM = { set_country_flag = COLDWAR_EGY_disengagement }\nFROM = { USA = { add_opinion_modifier = { target = PREV modifier = COLDWAR_EGY_peace_effort } } }",
      ai_base=50, ai_mods="modifier = { factor = 2 FROM = { has_country_flag = COLDWAR_EGY_us_mediation } }")
offer("the_sinai_agreement", 123, "suez_oil", ["ISR"], "The Sinai Agreement",
      "Cairo proposes a second agreement: the return of the Sinai in exchange for demilitarised zones, early-warning stations and free passage through the Canal.",
      "Return the Sinai.", "COLDWAR_EGY_return_sinai = yes\nFROM = { set_country_flag = COLDWAR_EGY_sinai_returned }\n" + mutual(mod="COLDWAR_EGY_peace_treaty"),
      ai_base=35, ai_mods="modifier = { factor = 2 FROM = { has_country_flag = COLDWAR_EGY_us_mediation } }")
offer("mediate_black_september", 124, "arab_conf", ["JOR", "PAL"], "The Cairo Agreement",
      "President Nasser has summoned King Hussein and Yasser Arafat to Cairo to end the fighting in Jordan. Both sides are asked to sign an agreement that ends the bloodshed.",
      "Sign the Cairo Agreement.",
      "FROM = { set_country_flag = COLDWAR_EGY_cairo_agreement_@ROOT }\nadd_opinion_modifier = { target = FROM modifier = COLDWAR_EGY_partnership }\nCOLDWAR_EGY_check_cairo_agreement = yes",
      ai_base=70)
offer("the_khartoum_subsidies", 125, "arab_conf", ["SAU", "KUW", "LBA"], "Aid for the Front-line States",
      "As agreed in Khartoum, Egypt asks for the annual aid owed to the states that carry the burden of the war against Israel.",
      "Pay the subsidy.", gdp_to_egypt("0.005") + "\nadd_opinion_modifier = { target = FROM modifier = COLDWAR_EGY_arab_solidarity }", ai_base=70, ai_mods=OPINION_AI)
offer("federation_of_arab_republics", 126, "uar", ["LBA", "SYR", "SUD"], "The Federation of Arab Republics",
      "Cairo proposes a federation of the progressive Arab republics: a common presidency council, coordinated foreign policy and an open market, under Egyptian leadership.",
      "Join the Federation.", "add_ideas = COLDWAR_EGY_far_member\nFROM = { if = { limit = { NOT = { has_idea = COLDWAR_EGY_far_member } } add_ideas = COLDWAR_EGY_far_member } }\n" + mutual(),
      ai_base=50, ai_mods=OPINION_AI)
offer("full_union_with_libya", 127, "libya", ["LBA"], "A Full Union with Egypt",
      "Libya once proposed a complete union of the two states. Cairo now answers: one state, one army, one president. If we accept, Libya will become part of Egypt.",
      "Unite with Egypt.", "FROM = { annex_country = { target = PREV transfer_troops = yes } }",
      decline="Libya stays Libyan.", ai_base=15, ai_mods="modifier = { factor = 0 is_ai = no }")
offer("unity_of_the_nile_valley", 128, "nile", ["SUD"], "An Economic Union of the Nile Valley",
      "Egypt proposes an economic union of the Nile valley: open borders for goods, coordinated agriculture and a shared development fund.",
      "Join the economic union.",
      TRADE + "\nadd_timed_idea = { idea = COLDWAR_EGY_nile_valley_union days = 1825 }\nFROM = { add_timed_idea = { idea = COLDWAR_EGY_nile_valley_union days = 1825 } }",
      ai_base=50, ai_mods=OPINION_AI)
offer("arab_industrialisation_organisation", 129, "factory", ["SAU", "UAE", "QAT"], "The Arab Organisation for Industrialisation",
      "Cairo invites the Gulf states to co-finance an Arab arms industry in Egypt. Every partner that joins halves Egypt's remaining share of the cost.",
      "Co-finance the AOI.", "FROM = { COLDWAR_EGY_aoi_cofinance = yes }\n" + mutual(), ai_base=50, ai_mods=OPINION_AI)
offer("operation_kavkaz", 130, "soviet", ["SOV"], "Operation Kavkaz",
      "Egypt asks for Soviet crews for its missile sites and Soviet pilots for its MiGs, to stop the Israeli deep-penetration raids.",
      "Send the crews.",
      "FROM = { add_ideas = COLDWAR_EGY_operation_kavkaz }\nset_temp_variable = { percent_change = 10 }\nset_temp_variable = { tag_index = THIS.id }\nset_temp_variable = { influence_target = FROM.id }\nchange_influence_percentage = yes",
      ai_base=60, ai_mods=OPINION_AI)
offer("treaty_of_friendship", 131, "soviet", ["SOV"], "A Treaty of Friendship and Cooperation",
      "Cairo proposes a fifteen-year Treaty of Friendship and Cooperation between Egypt and the Soviet Union.",
      "Sign the treaty.", mutual(), ai_base=70, ai_mods=OPINION_AI)
offer("the_gulf_investment_wave", 132, "saudi", ["SAU", "KUW", "UAE"], "An Investment Agreement with Egypt",
      "The Infitah has opened Egypt to foreign capital. Cairo offers Gulf investors protection, tax breaks and a share in the new Egypt.",
      "Sign the agreement.", "FROM = { add_timed_idea = { idea = COLDWAR_EGY_gulf_investment days = 1825 } }\n" + mutual(), ai_base=50, ai_mods=OPINION_AI)
offer("the_sumed_pipeline", 133, "oil", ["SAU", "KUW", "UAE"], "The SUMED Pipeline",
      "Egypt is building a pipeline from Suez to the Mediterranean that will carry Gulf crude around the closed Canal. Cairo asks for co-financing.",
      "Co-finance the pipeline.", gdp_to_egypt("0.005") + "\n" + mutual(), ai_base=50, ai_mods=OPINION_AI)
offer("arm_the_arab_military_pact", 134, "army", ["FACTION"], "A Joint Arab High Command",
      "The Egyptian high command proposes to its allies a joint command structure, common exercises and coordinated war plans.",
      "Join the joint command.", "add_ideas = COLDWAR_EGY_joint_arab_command\nFROM = { if = { limit = { NOT = { has_idea = COLDWAR_EGY_joint_arab_command } } add_ideas = COLDWAR_EGY_joint_arab_command } }",
      ai_base=60, ai_mods=OPINION_AI)

offer("oct_the_october_coalition", 135, "army", ["SYR", "JOR", "IRQ", "ALG", "LBA", "MOR"], "The October Coalition",
      "Cairo has sent a secret envoy: Egypt is preparing to cross the Canal and asks us to join a coordinated war against Israel. "
      "A second front would split the Israeli army; squadrons, brigades and money from every Arab capital would decide the outcome. "
      "If we agree we will be given our own war aims and a place in the joint plan.",
      "We will fight beside Egypt.",
      "add_ideas = COLDWAR_EGY_october_coalition\n"
      "if = { limit = { tag = SYR } create_wargoal = { type = take_state_focus target = ISR generator = { 587 } } }\n"
      "else_if = { limit = { tag = JOR } create_wargoal = { type = take_state_focus target = ISR generator = { 208 207 } } }\n"
      "else = { create_wargoal = { type = topple_government target = ISR } }\n"
      "FROM = { if = { limit = { NOT = { has_idea = COLDWAR_EGY_october_coalition } } add_ideas = COLDWAR_EGY_october_coalition } }\n"
      "add_opinion_modifier = { target = FROM modifier = COLDWAR_EGY_arab_solidarity }\nreverse_add_opinion_modifier = { target = FROM modifier = COLDWAR_EGY_arab_solidarity }",
      decline="This is not our war.", ai_base=55,
      ai_mods="modifier = { factor = 0 has_war_with = FROM }\nmodifier = { factor = 0 NOT = { country_exists = ISR } }\n"
              "modifier = { factor = 1.5 tag = SYR }\nmodifier = { factor = 0.5 tag = JOR }\nmodifier = { factor = 0.25 has_opinion = { target = FROM value < 0 } }")
