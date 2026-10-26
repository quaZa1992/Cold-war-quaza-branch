# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""The dark path: the Bonn Republic collapses into an authoritarian nationalist regime.

Multiplayer roleplay rules:
  * only a human West German government can walk this path (every focus has is_ai = no, AI weight 0)
  * it is very hard: several years of deliberate erosion (Erosion of the Republic >= 60), a far-right
    result of at least 15% in the LAST Bundestag election, low stability, a broken rule of law and a
    strong security apparatus - and then three points where it can fail: the Constitutional Court, the
    Bundestag and the Bundeswehr's generals
  * everything is public: other human players get news events and can react at each stage
  * reactions: NATO members can suspend Bonn from the Alliance, impose sanctions and - human
    governments of the three Western Allies only - invoke their reserved rights (war goal); the Soviet
    Union can put its forces in Germany on alert, guarantee its allies, impose sanctions and - human
    only - invoke the UN Charter's enemy-state clauses (war goal). AI governments react hard, but never
    start a war on their own.
  * a way back: the Basic Law can be restored
The regime is fictional: it is led by a "National Directorate", not by a historical person.
"""
from cw_lib import *
from events_lib import E, O, gov, EXTRA_EFFECTS
from tree import F, core, unlock, state_build, opinion, climate_base
from rivalry import kl
from foreign import news_all

EVK = "COLDWAR_GDARK"
HUMAN = "is_ai = no"
NO_FAIL = f"NOT = {{ has_country_flag = {P}_dark_failed }}"
DARK = f"has_country_flag = {P}_dark_regime"
ALLIES = ("USA", "ENG", "FRA")
AI0 = "modifier = { factor = 0 is_ai = yes }"


def ctt(key, text, cond):
    L(key, text)
    return f"custom_trigger_tooltip = {{ tooltip = {key} {cond} }}"


def erosion(n):
    return v("cwger_dark", n)


# ------------------------------------------------------------------ availability (with readable tooltips)
AV_ENTRY = J(HUMAN, NO_FAIL, f"NOT = {{ has_completed_focus = {P}_liberal_state }}", "date > 1970.6.1",
             ctt(f"{P}_tt_av_dark_entry", "The far right (NPD, DVU, Republikaner) polls above §Y6%§! together, or the right-wing terror threat is above §Y30§!",
                 "OR = { check_variable = { cwger_far_right_pop > 0.06 } check_variable = { cwger_terror_right > 30 } }"))
AV_GATE = J(HUMAN, NO_FAIL,
            ctt(f"{P}_tt_av_dark_erosion", "Erosion of the Republic is at least §Y60§!", "check_variable = { cwger_dark > 59 }"),
            ctt(f"{P}_tt_av_dark_vote", "The far right won at least §Y15%§! together in the §Ylast Bundestag election§!",
                "check_variable = { cwger_far_right_elect > 0.1499 }"),
            "has_stability < 0.30",
            ctt(f"{P}_tt_av_dark_rs", "Rule-of-law credibility is below §Y35§!", "check_variable = { cwger_rechtsstaat < 35 }"),
            ctt(f"{P}_tt_av_dark_sec", "The security state is above §Y65§!", "check_variable = { cwger_security > 65 }"))

# ------------------------------------------------------------------ focuses (Chancellery pillar, own block)
F("national_right", "chancellery", -10, 16, cost=3, pre=[], avail=AV_ENTRY, ai=0, ai_mod=AI0, icon="ban_npd",
  name="Courting the National Right",
  desc="There are votes to the right of the Union - and a government that needs them. A chancellor who speaks of 'foreign infiltration' and 'red terror' finds an audience that Bonn has kept out of politics since 1949.",
  reward=J(erosion(15), party("npd", 0.02), party("rep", 0.005), v("cwger_rechtsstaat", -4), stab(-0.02), protest(4), faction("mittelstand", 3),
           tt(f"{P}_tt_dark_warn", "§RThis is the first step on a path that can end the Bonn Republic. Other governments will notice.§!")))
F("order_above_all", "national_right", 0, 1, cost=3, ai=0, ai_mod=AI0, avail=J(HUMAN, NO_FAIL), icon="policeman",
  name="Order Above Everything",
  desc="Terrorists, demonstrators, 'parasites': the government promises order and the police get whatever they ask for. The Basic Law's critics are no longer only on the left.",
  reward=J(erosion(15), v("cwger_security", 8), v("cwger_rechtsstaat", -6), party("npd", 0.015), party("rep", 0.01), faction("dgb", -6), faction("mittelstand", 4),
           news_all("Worrying Signals from Bonn", "The West German government is courting the far right and talks of 'order above everything'. Diplomats in Bonn report that the Federal Republic's democratic consensus is fraying.", "GFX_npd_flag")))
F("street_and_ballot", "order_above_all", 0, 1, cost=3, ai=0, ai_mod=AI0, avail=J(HUMAN, NO_FAIL), icon="ban_npd",
  name="The Street and the Ballot Box",
  desc="Torchlight marches in provincial towns, a 'national' newspaper on every kiosk, veterans' associations in the front row. The far right no longer hides - and the other side takes to the streets as well.",
  reward=J(erosion(15), v("cwger_terror_right", 8), party("npd", 0.02), party("dvu", 0.01), stab(-0.03), protest(6),
           f"country_event = {{ id = {EVK}.5 days = 10 }}"))
F("crisis_of_the_republic", "street_and_ballot", 0, 1, cost=5, ai=0, ai_mod=AI0, avail=AV_GATE, icon="parliament",
  name="The Crisis of the Republic",
  desc="Bonn is not Weimar, the textbooks said. The government now argues that the Basic Law has made the state defenceless - and that only an emergency can save it. The Constitutional Court in Karlsruhe is watching.",
  reward=J(erosion(10), f"set_country_flag = {P}_dark_crisis", f"country_event = {{ id = {EVK}.1 days = 3 }}",
           tt(f"{P}_tt_dark_court", "§YThe Federal Constitutional Court will act.§! Whether the government obeys it is our decision.")))
F("emergency_decree", "crisis_of_the_republic", 0, 1, cost=5, ai=0, ai_mod=AI0, avail=J(HUMAN, NO_FAIL, f"has_country_flag = {P}_dark_defied"), icon="constitution",
  name="Rule by Emergency Decree",
  desc="The emergency laws of 1968 were written for war. The government declares that the war has come from within: decrees instead of laws, the Joint Committee instead of the Bundestag.",
  reward=J(erosion(10), v("cwger_rechtsstaat", -15), v("cwger_security", 10), protest(10),
           f"country_event = {{ id = {EVK}.3 days = 5 }}",
           tt(f"{P}_tt_dark_vote", "§YThe Bundestag can still stop us§! with a constructive vote of no confidence - and then the generals must choose.")))
F("national_directorate", "emergency_decree", 0, 1, cost=7, ai=0, ai_mod=AI0, avail=J(HUMAN, NO_FAIL, f"has_country_flag = {P}_dark_army"), icon="chancellor",
  name="The National Directorate",
  desc="The Bundestag is adjourned 'until order is restored'. A National Directorate takes over the powers of the chancellor and the federal president. The Federal Republic's flag still flies - over a different state.",
  reward=J(f"{P}_dark_seize = yes",
           tt(f"{P}_tt_dark_seize", "§RThe Bonn Republic ends.§! The government passes to a National Directorate (NPD), elections are suspended.\n"
                                    "§RNATO members§! decide whether to suspend us, impose sanctions or - the three Western Allies - invoke their reserved rights.\n"
                                    "§RThe Soviet Union§! decides whether to alert its forces, impose sanctions or invoke the UN Charter's enemy-state clauses.")))
F("purge_institutions", "national_directorate", -1, 1, cost=3, ai=0, ai_mod=AI0, avail=DARK, icon="secret_police",
  name="Purge the Institutions",
  desc="Judges, editors, professors, officers: lists are drawn up. Those who sign the loyalty declaration stay. The others leave - for prison or for the West.",
  reward=J(v("cwger_rechtsstaat", -100), v("cwger_security", 20), pp(100), stab(0.04), protest(8), faction("dgb", -20),
           core("west", research=-0.05), core("bonn", drift=0.1)))
F("national_rearmament", "national_directorate", 1, 1, cost=5, ai=0, ai_mod=AI0, avail=DARK, icon="army_reform", filt="FOCUS_FILTER_MANPOWER",
  name="National Rearmament",
  desc="No more NATO quotas: the Directorate wants an army of its own size, its own command and its own purpose.",
  reward=J(core("armee", consc=0.1, org=0.03), ws(0.1), "add_manpower = 100000", tension(5),
           f"random_owned_controlled_state = {{ limit = {{ free_building_slots = {{ building = arms_factory size > 1 include_locked = yes }} }} add_building_construction = {{ type = arms_factory level = 2 instant_build = yes }} }}",
           f"if = {{ limit = {{ country_exists = SOV }} SOV = {{ country_event = {{ id = {EVK}.31 days = 2 }} }} }}"))
F("renounce_treaties", "purge_institutions", 1, 1, cost=3, ai=0, ai_mod=AI0, avail=DARK, pre=[["purge_institutions"], ["national_rearmament"]], icon="treaty",
  name="Renounce the Eastern Treaties",
  desc="Moscow, Warsaw, Prague, the Basic Treaty: 'treaties of renunciation', signed by a republic that no longer exists. The Directorate declares them void.",
  reward=J(kl(-40), climate_base(-20), tension(8), opinion("SOV", "large_decrease"), opinion("POL", "large_decrease"), opinion("CZE", "large_decrease"),
           f"set_country_flag = {P}_treaties_renounced",
           f"if = {{ limit = {{ country_exists = POL }} POL = {{ country_event = {{ id = {EVK}.45 days = 2 }} }} }}",
           f"if = {{ limit = {{ country_exists = SOV }} SOV = {{ country_event = {{ id = {EVK}.31 days = 2 }} }} }}"))
F("old_borders", "renounce_treaties", 0, 1, cost=5, ai=0, ai_mod=AI0, avail=J(DARK, "country_exists = DDR"), icon="tank_wall", wargoal="DDR",
  name="The Old Borders",
  desc="The Directorate claims the 'Soviet Zone' as German territory under occupation. A war goal against East Berlin - and a challenge to every army of the Warsaw Pact.",
  reward=J("create_wargoal = { type = annex_everything target = DDR }", tension(20), ws(0.05),
           f"if = {{ limit = {{ country_exists = SOV }} SOV = {{ country_event = {{ id = {EVK}.32 days = 1 }} }} }}",
           f"if = {{ limit = {{ country_exists = DDR }} DDR = {{ country_event = {{ id = {EVK}.40 days = 1 }} }} }}",
           tt(f"{P}_tt_dark_borders", "§RA war goal against the GDR.§! The Soviet Union and the Warsaw Pact will decide how to answer.")))
F("restore_basic_law", "national_directorate", 0, 3, cost=3, pre=[["national_directorate"]], ai=0, ai_mod=AI0,
  avail=J(DARK, ctt(f"{P}_tt_av_dark_end", "Stability below §Y20%§!, or the resistance has grown strong (§Y60§!+), or we are at war",
                    "OR = { has_stability < 0.20 check_variable = { cwger_resistance > 59 } has_war = yes }")),
  icon="constitution", name="Restore the Basic Law",
  desc="The Directorate has failed - or has understood that it will. The Bundestag is recalled, the decrees are lifted, free elections are announced. Whether the world believes it is another question.",
  reward=J(f"{P}_dark_restore = yes",
           tt(f"{P}_tt_dark_restore", "The Bonn Republic returns: the Union forms a caretaker government, elections are restored, the Directorate's spirit is removed. NATO members decide whether to lift their measures.")))

# ------------------------------------------------------------------ events: the three tests
E(f"{EVK}.1", "Karlsruhe Moves",
  "The Federal Constitutional Court has opened proceedings under Article 21 of the Basic Law to ban the NPD as unconstitutional, and has issued an injunction against the government's emergency plans. The president of the court says the Basic Law 'does not provide for its own abolition'.",
  "GFX_german_parliament_bundestag",
  [O("We respect the court. This ends here.", J(f"set_country_flag = {P}_dark_failed", erosion(-40), party("npd", -0.03), v("cwger_rechtsstaat", 10), stab(0.03)),
     tt="§GThe path ends for good.§! The republic has defended itself."),
   O("The court has no army. We ignore it.", J(f"set_country_flag = {P}_dark_defied", v("cwger_rechtsstaat", -15), erosion(10), protest(10),
                                                news_all("Bonn Defies Its Constitutional Court", "The West German government has declared that it will not comply with an injunction of the Federal Constitutional Court. Lawyers speak of a constitutional crisis; the Allies' embassies speak of nothing else.", "GFX_german_parliament")),
     tt="§RA constitutional crisis.§! Every other government will hear of it.")])
E(f"{EVK}.3", "The Vote in the Bundestag",
  "The opposition and the government's own dissidents table a constructive vote of no confidence. If they find a majority for another chancellor, the emergency is over before it began.",
  "GFX_bundestag",
  [O("Count the votes.", J(
      f"random_list = {{ 40 = {{ modifier = {{ add = 25 check_variable = {{ cwger_margin < 0 }} }} modifier = {{ add = 15 check_variable = {{ cwger_margin < -20 }} }} modifier = {{ add = 20 has_country_flag = {P}_emergency_laws_tied }} modifier = {{ add = 15 has_country_flag = {P}_elected_president }} "
      f"modifier = {{ factor = 0.6 check_variable = {{ cwger_security > 80 }} }} country_event = {{ id = {EVK}.6 days = 1 }} }} "
      f"60 = {{ country_event = {{ id = {EVK}.4 days = 3 }} }} }}"),
     tt="§Y40%§! (more without a government majority, if the emergency laws were tied to the court or with a popularly elected president) that the Bundestag replaces the chancellor - the path ends. Otherwise the generals must choose.")])
E(f"{EVK}.4", "The Generals' Answer",
  "The chief of staff of the Bundeswehr is asked whether the armed forces will carry out the government's orders. The officers swore an oath to the Basic Law, not to a government; the Innere Führung taught them to refuse unlawful orders.",
  "GFX_news_german_army",
  [O("Await their answer.", J(
      f"random_list = {{ 50 = {{ modifier = {{ add = 15 has_completed_focus = {P}_civilian_service }} modifier = {{ add = 10 has_completed_focus = {P}_bundeswehr_universities }} "
      f"modifier = {{ add = 10 has_idea = NATO_member }} modifier = {{ factor = 0.7 check_variable = {{ cwger_security > 80 }} }} modifier = {{ factor = 0.8 has_war_support > 0.6 }} "
      f"country_event = {{ id = {EVK}.7 days = 1 }} }} "
      f"50 = {{ set_country_flag = {P}_dark_army country_event = {{ id = {EVK}.8 days = 1 }} }} }}"),
     tt="§Y50%§! that the generals refuse (more with the Innere Führung reforms and NATO integration) - then the path ends.")])
E(f"{EVK}.5", "The Other Germany Takes to the Streets",
  "Trade unions, churches, students and the Greens call a day of protest against the 'march to the right'. Hundreds of thousands fill the Bonn Hofgarten.",
  "GFX_peace_demonstration_berlin",
  [O("Let them march.", J(erosion(-5), stab(0.01), v("cwger_resistance", 5))),
   O("Ban the march as a threat to public order.", J(erosion(5), v("cwger_rechtsstaat", -5), v("cwger_resistance", 10), protest(6)))])
E(f"{EVK}.6", "A New Chancellor",
  "The constructive vote of no confidence succeeds. The Bundestag elects a new chancellor, who lifts the emergency decrees in his first act. The republic has defended itself - narrowly.",
  "GFX_german_parliament_bundestag",
  [O("The Basic Law holds.", J(f"set_country_flag = {P}_dark_failed", erosion(-50), v("cwger_rechtsstaat", 15), party("npd", -0.04), stab(0.05),
                              gov(1, [2]), f"{P}_refresh_leader = yes",
                              news_all("The Federal Republic Holds", "A constructive vote of no confidence has ended the West German government's attempt to rule by decree. The new chancellor promises to restore every constitutional right.", "GFX_bundestag")))])
E(f"{EVK}.7", "The Generals Refuse",
  "The inspector general announces on television that the Bundeswehr 'stands on the ground of the Basic Law' and will not act against the Bundestag. The government's authority collapses within hours.",
  "GFX_news_german_army",
  [O("It is over.", J(f"set_country_flag = {P}_dark_failed", erosion(-50), v("cwger_rechtsstaat", 10), stab(-0.05), party("npd", -0.05),
                     gov(1, [2]), f"{P}_refresh_leader = yes",
                     news_all("The Bundeswehr Stands by the Constitution", "West Germany's armed forces have refused to support the government's emergency rule. A caretaker government has taken over in Bonn.", "GFX_news_german_army")))])
E(f"{EVK}.8", "The Army Stands Aside",
  "The generals declare the armed forces 'neutral in a political dispute'. Nobody will stop the government - and everybody understands what that means.",
  "GFX_GER_Panzer_strasse",
  [O("The way is open.", J(erosion(10), tt(f"{P}_tt_dark_open", "§YThe National Directorate§! can now be proclaimed.")))])

# ------------------------------------------------------------------ the seizure and the way back
EXTRA_EFFECTS.append(f"""
{P}_dark_seize = {{
	set_country_flag = {P}_dark_regime
	set_global_flag = cwger_dark_germany
	clr_global_flag = cwger_dark_germany_ended
	set_variable = {{ cwger_resistance = 10 }}
	if = {{ limit = {{ has_idea = {P}_idea_bonn_republic }} remove_ideas = {P}_idea_bonn_republic }}
	add_ideas = {P}_idea_dark_regime
	{gov(21, (), elections=False)}
	{P}_refresh_leader = yes
	add_stability = -0.05
	if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} set_temp_variable = {{ mdcw_cw_tension_delta = 15 }} mdcw_cw_add_tension = yes }}
	add_to_variable = {{ cwgg_klima = -30 }}
	clamp_variable = {{ var = cwgg_klima min = -100 max = 100 }}
	every_other_country = {{
		limit = {{ has_idea = NATO_member }}
		country_event = {{ id = {EVK}.20 days = 1 }}
	}}
	if = {{ limit = {{ country_exists = SOV }} SOV = {{ country_event = {{ id = {EVK}.30 days = 1 }} }} }}
	if = {{ limit = {{ country_exists = DDR }} DDR = {{ country_event = {{ id = {EVK}.40 days = 1 }} }} }}
	every_other_country = {{
		limit = {{ is_ai = no NOT = {{ has_idea = NATO_member }} NOT = {{ original_tag = SOV }} NOT = {{ original_tag = DDR }} }}
		country_event = {{ id = {EVK}.10 days = 1 }}
	}}
}}

{P}_dark_restore = {{
	clr_country_flag = {P}_dark_regime
	set_country_flag = {P}_dark_failed
	clr_global_flag = cwger_dark_germany
	set_global_flag = cwger_dark_germany_ended
	if = {{ limit = {{ has_idea = {P}_idea_dark_regime }} remove_ideas = {P}_idea_dark_regime }}
	add_ideas = {P}_idea_bonn_republic
	{gov(1, (2,), elections=True)}
	{P}_refresh_leader = yes
	set_variable = {{ cwger_dark = 0 }}
	add_to_variable = {{ cwger_rechtsstaat = 30 }}
	clamp_variable = {{ var = cwger_rechtsstaat min = 0 max = 100 }}
	if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} set_temp_variable = {{ mdcw_cw_tension_delta = -10 }} mdcw_cw_add_tension = yes }}
	every_other_country = {{
		limit = {{ OR = {{ has_idea = NATO_member is_ai = no }} }}
		country_event = {{ id = {EVK}.25 days = 2 }}
	}}
}}

# Monthly, GER scope: far-right vote shares, the slow recovery of the republic, the resistance.
{P}_dark_tick = {{
	set_variable = {{ cwger_far_right_pop = 0 }}
	add_to_variable = {{ cwger_far_right_pop = party_pop_array^21 }}
	set_variable = {{ cwger_far_right_elect = 0 }}
	add_to_variable = {{ cwger_far_right_elect = cwger_parliament_shares^21 }}
	if = {{ limit = {{ NOT = {{ has_country_flag = {P}_dark_regime }} }}
		# democratic institutions recover by themselves unless someone keeps pushing
		add_to_variable = {{ cwger_dark = -0.5 }}
		if = {{ limit = {{ check_variable = {{ cwger_rechtsstaat > 60 }} }} add_to_variable = {{ cwger_dark = -0.5 }} }}
		clamp_variable = {{ var = cwger_dark min = 0 max = 100 }}
	}}
	else = {{
		add_to_variable = {{ cwger_resistance = 0.5 }}
		if = {{ limit = {{ has_stability < 0.35 }} add_to_variable = {{ cwger_resistance = 1 }} }}
		if = {{ limit = {{ check_variable = {{ cwger_security > 80 }} }} add_to_variable = {{ cwger_resistance = -0.5 }} }}
		clamp_variable = {{ var = cwger_resistance min = 0 max = 100 }}
		if = {{ limit = {{ NOT = {{ has_country_flag = cwger_resistance_cd }} }}
			random_list = {{ 92 = {{ }} 8 = {{ modifier = {{ add = 6 check_variable = {{ cwger_resistance > 40 }} }} set_country_flag = {{ flag = cwger_resistance_cd days = 180 value = 1 }} country_event = {{ id = {EVK}.60 days = 1 }} }} }}
		}}
	}}
}}
""")

# ------------------------------------------------------------------ reactions
REF = "[From.GetName]"
E(f"{EVK}.10", "Dictatorship in Bonn",
  "The West German government has suspended the Bundestag and handed power to a 'National Directorate'. In the heart of Europe, between NATO and the Warsaw Pact, a democracy has ended.",
  "GFX_npd_flag",
  [O("We condemn it.", "add_opinion_modifier = { target = GER modifier = large_decrease }"),
   O("This is Germany's own affair.", "")],
  scope="ANY")

NATO_TRIG = "has_idea = NATO_member"
E(f"{EVK}.20", "The Alliance and the Directorate",
  "Bonn's new rulers still sit in NATO's councils, still command twelve divisions assigned to the Alliance, still hold the codes of the nuclear sharing arrangements. Every member government must decide what the Alliance owes a dictatorship.",
  "GFX_decision_nato",
  [O("Suspend Bonn from the Alliance.",
     J("add_opinion_modifier = { target = GER modifier = large_decrease }",
       "GER = { if = { limit = { has_idea = NATO_member } NATO_leave = yes } }"),
     ai="base = 40 modifier = { factor = 2 is_faction_leader = yes } modifier = { factor = 2 original_tag = USA }",
     tt="If Bonn is still a member, it §Rleaves NATO§! (one member's decision is enough)."),
   O("Economic sanctions.",
     J("add_opinion_modifier = { target = GER modifier = large_decrease }", f"GER = {{ {P}_sanction_prev_economic = yes }}"),
     ai="base = 45"),
   O("Invoke the Allied reserved rights - prepare to intervene.",
     J("create_wargoal = { type = topple_government target = GER }", "add_war_support = 0.05",
       "add_opinion_modifier = { target = GER modifier = large_decrease }",
       f"if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} set_temp_variable = {{ mdcw_cw_tension_delta = 5 }} mdcw_cw_add_tension = yes }}"),
     ai=0, trig=f"is_ai = no OR = {{ {' '.join(f'original_tag = {t}' for t in ALLIES)} }}",
     tt="The Western Allies never gave up their rights for Germany as a whole and Berlin. §RCreates a war goal to restore the Basic Law.§! The Allies would be marching into the country they once liberated - and rebuilt."),
   O("Condemn it, but keep the channels open.", "add_opinion_modifier = { target = GER modifier = medium_decrease }", ai="base = 15")],
  scope="ANY", trig=f"{NATO_TRIG} NOT = {{ original_tag = GER }}")
E(f"{EVK}.25", "The Republic Returns",
  "Bonn has lifted the emergency decrees, recalled the Bundestag and announced free elections. The question is whether the world will take the Germans back - again.",
  "GFX_bundestag",
  [O("Welcome back. Lift our measures.", J("add_opinion_modifier = { target = GER modifier = medium_increase }",
                                          f"GER = {{ {P}_lift_eco_sanction_on_prev = yes }}"), ai="base = 60"),
   O("Trust will have to be earned.", "", ai="base = 40")],
  scope="ANY")

SOV_T = "original_tag = SOV"
E(f"{EVK}.30", "Revanchism in Power",
  "Twenty-five years after the Great Patriotic War, nationalists rule in Bonn. The marshals want to know whether the Group of Soviet Forces in Germany is to be placed on alert. The Foreign Ministry reminds the Politburo that the UN Charter still names Germany an 'enemy state'.",
  "GFX_gdratwarsov",
  [O("Invoke the enemy-state clauses of the UN Charter.",
     J("create_wargoal = { type = topple_government target = GER }", f"add_ideas = {P}_idea_gsfg_alert", "add_war_support = 0.1",
       f"if = {{ limit = {{ has_global_flag = mdcw_cw_initialized }} set_temp_variable = {{ mdcw_cw_tension_delta = 10 }} mdcw_cw_add_tension = yes }}"),
     ai=0, trig="is_ai = no",
     tt="Articles 53 and 107 allow action against a former enemy state that resumes an aggressive policy. §RCreates a war goal against the Federal Republic.§! The road to the Rhine has been planned since 1945; now it would be driven."),
   O("Alert the Group of Soviet Forces and guarantee our allies.",
     J(f"if = {{ limit = {{ NOT = {{ has_idea = {P}_idea_gsfg_alert }} }} add_ideas = {P}_idea_gsfg_alert }}", "add_war_support = 0.05",
       "if = { limit = { country_exists = DDR NOT = { has_war_with = DDR } } give_guarantee = DDR }",
       "if = { limit = { country_exists = POL NOT = { has_war_with = POL } } give_guarantee = POL }",
       "add_opinion_modifier = { target = GER modifier = large_decrease }"),
     ai="base = 70"),
   O("Sanctions and a note of protest.",
     J(f"GER = {{ {P}_sanction_prev_economic = yes }}", "add_opinion_modifier = { target = GER modifier = large_decrease }"), ai="base = 30")],
  scope="ANY", trig=SOV_T)
E(f"{EVK}.31", "The Directorate Arms",
  "Bonn is rearming outside every Alliance quota and has torn up the treaties of the 1970s. The General Staff asks for permission to prepare for every eventuality.",
  "GFX_missiles_on_road",
  [O("Prepare for every eventuality.",
     J("create_wargoal = { type = topple_government target = GER }", "add_war_support = 0.05"),
     ai=0, trig="is_ai = no", tt="§RCreates a war goal against the Federal Republic.§! The plans in the General Staff's safe stop being exercises."),
   O("Reinforce the Western Group of Forces.",
     J(f"if = {{ limit = {{ NOT = {{ has_idea = {P}_idea_gsfg_alert }} }} add_ideas = {P}_idea_gsfg_alert }}", "add_war_support = 0.05",
       "if = { limit = { country_exists = DDR NOT = { has_war_with = DDR } } give_guarantee = DDR }"), ai="base = 80"),
   O("Watch and wait.", "", ai="base = 20")],
  scope="ANY", trig=SOV_T)
E(f"{EVK}.32", "Bonn Claims the GDR",
  "The National Directorate claims the territory of the German Democratic Republic and has issued a war goal against East Berlin. Every treaty since 1945 is at stake.",
  "GFX_gdratwarsov",
  [O("Any attack on the GDR is an attack on the Soviet Union.",
     J("if = { limit = { country_exists = DDR NOT = { has_war_with = DDR } } give_guarantee = DDR }",
       "if = { limit = { country_exists = POL NOT = { has_war_with = POL } } give_guarantee = POL }",
       f"if = {{ limit = {{ NOT = {{ has_idea = {P}_idea_gsfg_alert }} }} add_ideas = {P}_idea_gsfg_alert }}", "add_war_support = 0.1"),
     ai="base = 90"),
   O("Strike before the Directorate does.",
     J("create_wargoal = { type = topple_government target = GER }", "add_war_support = 0.1"),
     ai=0, trig="is_ai = no", tt="§RCreates a war goal against the Federal Republic.§! A pre-emptive war on German soil - the nightmare of every planner since 1949.")],
  scope="ANY", trig=SOV_T)
E(f"{EVK}.40", "Fascism on Our Border",
  "The GDR has always called the Federal Republic a revanchist state. Now Bonn's own government seems determined to prove it. The National People's Army is put on alert; the Politburo asks Moscow for guarantees.",
  "GFX_gdrfromexitsov",
  [O("The anti-fascist protective wall was right.", J("add_stability = 0.05", "add_war_support = 0.1", "add_political_power = 50")),
   O("Appeal to the United Nations.", J("add_political_power = 25", "add_opinion_modifier = { target = GER modifier = large_decrease }"))],
  scope="ANY", trig="original_tag = DDR")
E(f"{EVK}.45", "Bonn Tears Up the Warsaw Treaty",
  "The National Directorate has declared the Warsaw Treaty of 1970 void - including the recognition of the Oder-Neisse line. Every Polish family that was moved west in 1945 understands what that means.",
  "GFX_politics_protest",
  [O("Ask Moscow for protection.", J("add_war_support = 0.1", "if = { limit = { country_exists = SOV } add_opinion_modifier = { target = SOV modifier = medium_increase } }")),
   O("Mobilise and appeal to the West.", J("add_war_support = 0.15", "add_stability = 0.02"))],
  scope="ANY", trig="original_tag = POL")
E(f"{EVK}.60", "The Resistance",
  "Leaflets at the universities, a strike at the Ruhr pits, a broadcast from a hidden transmitter: 'The Basic Law lives.' The Directorate's police know the names of some of them.",
  "GFX_german_riot",
  [O("Arrest them.", J(v("cwger_security", 5), v("cwger_resistance", 8), stab(-0.02), protest(5))),
   O("Make concessions.", J(v("cwger_resistance", -5), stab(0.02), pp(-50)))])

# ------------------------------------------------------------------ spirits
DARK_IDEAS = {
    "dark_regime": ("The National Directorate",
                    "Elections suspended, the Bundestag adjourned, the press licensed. A state that was built against 1933 has fallen to the same temptation.",
                    "political_violence",
                    {"political_power_factor": 0.15, "war_support_factor": 0.1, "stability_factor": -0.1, "research_speed_factor": -0.1,
                     "trade_opinion_factor": -0.5, "conscription_factor": 0.1, "drift_defence_factor": 0.5}),
}
SOV_IDEAS = {
    "gsfg_alert": ("Forces in Germany on Alert",
                   "The twenty divisions of the Group of Soviet Forces in Germany leave their barracks for their deployment areas.",
                   "army_strengthened", {"mobilization_speed": 0.25, "war_support_factor": 0.05, "army_org_factor": 0.05}),
}


import ideas as _ideas
_ideas.IDEAS.update(DARK_IDEAS)
_ideas.SOV_IDEAS.update(SOV_IDEAS)
