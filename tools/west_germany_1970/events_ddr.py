# IMPERIA COLD WAR — Native diplomatic recognition and UN membership.
# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
# IMPERIA COLD WAR — Retire Western integration and Moscow backing point mechanics.
"""East German events, the inner-German crisis chain and the dynamic road to unity."""
from cw_lib import *
from events_lib import E, O, fire, ger, ddr, EXTRA_EFFECTS
from migration import transfer
import balance_patch
from rivalry import kl, lever


def gv(var, n):
    """GER variable change from DDR scope."""
    return ger(v(var, n))


# IMPERIA COLD WAR — Retire the GER-owned crackdown roll; DDR political outcomes stay player-controlled.

# IMPERIA COLD WAR — Legacy Two Plus Four fast-track retired; COLDWAR_GGU owns negotiations and ratification.

EXTRA_EFFECTS.append(f"""
# IMPERIA COLD WAR — Sandbox DDR event scheduling leaves succession and crisis outcomes to East Berlin.
# Monthly, GER scope: economic and cultural developments; political choices remain with DDR.
{P}_ddr_events_tick = {{
	if = {{
		limit = {{ country_exists = DDR DDR = {{ has_country_flag = {P}_ddr_initialized is_ai = yes has_government = communism }} NOT = {{ has_global_flag = {P}_unity_achieved }} }}
		if = {{
			limit = {{ date > 1976.9.1 NOT = {{ has_global_flag = {P}_biermann_done }} DDR = {{ check_variable = {{ cwddr_opposition > 9 }} }} }}
			random_list = {{ 94 = {{ }} 6 = {{ set_global_flag = {P}_biermann_done DDR = {{ country_event = {{ id = {EVD}.6 days = 1 }} }} }} }}
		}}
		if = {{
			limit = {{ date > 1978.1.1 NOT = {{ has_global_flag = {P}_min_exchange_done }} DDR = {{ check_variable = {{ cwddr_hard_currency > 45 }} }} }}
			set_global_flag = {P}_min_exchange_done
			DDR = {{ country_event = {{ id = {EVD}.5 days = 2 }} }}
		}}
	}}
}}
""")

# ====================================================================== GDR, 1970s
# IMPERIA COLD WAR — Retired Honecker event ID remains inert for saves that had already queued it.
E(f"{EVD}.1", "", "", "", [O("Continue.")], scope="DDR", hidden=True)

# IMPERIA COLD WAR — Show prospective consequences in the native effect preview.
SWING_PREVIEW_ROWS, CREDIT_PREVIEW_ROWS = balance_patch.acceptance_previews(kl, lever)
SWING_PREVIEW = "effect_tooltip = {\n" + SWING_PREVIEW_ROWS + "\n}"
CREDIT_PREVIEW = "effect_tooltip = {\n" + CREDIT_PREVIEW_ROWS + "\n}"

E(f"{EVD}.2", "Bonn Offers a Larger Swing",
  "The Federal Republic proposes to raise the interest-free overdraft in inner-German trade. More Western goods, fewer questions - and a little more dependence on the class enemy.",
  "GFX_political_deal",
  [O("Accept the credit.", J(SWING_PREVIEW, f"{P}_balance_accept_swing = yes"),
     ai="base = 70 modifier = { factor = 2 check_variable = { cwddr_hard_currency > 50 } }",
     trig=f"{P}_balance_can_accept_swing = yes"),
   O("We do not need Bonn's charity.", f"{P}_balance_refuse_swing = yes", ai=30,
     trig=f"{P}_balance_can_respond_swing = yes"),
   O("Return to the situation map.", "", ai=0)],
  scope="DDR")

E(f"{EVD}.3", "The Billion-Mark Credit",
  "Franz Josef Strauß himself has arranged a bank loan of one billion marks, guaranteed by the federal government. Schalck-Golodkowski brings the conditions: the self-firing devices on the border are to go, and the minimum exchange for children is to be dropped.",
  "GFX_political_deal",
  [O("Take the money, dismantle the SM-70.", J(CREDIT_PREVIEW, f"{P}_balance_accept_credit = yes"),
     ai=80,
     trig=f"{P}_balance_can_accept_credit = yes"),
   O("No conditions on our border.", f"{P}_balance_refuse_credit = yes", ai=20,
     trig=f"{P}_balance_can_respond_credit = yes"),
   O("Return to the situation map.", "", ai=0)],
  scope="DDR")

E(f"{EVD}.4", "Prisoners for Hard Currency",
  "The lawyer Wolfgang Vogel brings a new list from Bonn. Every political prisoner released to the West brings tens of thousands of D-Marks - in goods delivered through the churches.",
  "GFX_politics_negotiations",
  [O("Sell them.", J(dv_self("cwddr_hard_currency", -4), dv_self("cwddr_opposition", -2), dv_self("cwddr_west_dependency", 2), ger(v("cwger_ostpolitik", 2, show=False))), ai=85),
   O("Not this year.", J(dv_self("cwddr_sed_control", 1), ger("add_political_power = 25")), ai=15)],
  scope="DDR")

E(f"{EVD}.5", "Raise the Minimum Exchange?",
  "Every visitor from the West must exchange a fixed sum of D-Marks at a rate of one to one. Raising it would bring in hard currency - and keep pensioners from Hanover away from their relatives in Halle.",
  "GFX_euro",
  [O("Double it to 25 marks.", J(dv_self("cwddr_hard_currency", -5), dv_self("cwddr_west_media", -3), dv_self("cwddr_sed_control", 2), ger(v("cwger_ostpolitik", -5))), ai=70),
   O("Leave it as it is.", J(dv_self("cwddr_hard_currency", 2), ger(v("cwger_ostpolitik", 2))), ai=30)],
  scope="DDR")

E(f"{EVD}.6", "Biermann in Cologne",
  "The singer Wolf Biermann has been allowed to perform in Cologne - and the concert was broadcast by the WDR to the whole GDR. The Politburo considers withdrawing his citizenship.",
  "GFX_Good_bye_lenin",
  [O("Expatriate him.", J(dv_self("cwddr_opposition", 4), dv_self("cwddr_west_media", 3), dv_self("cwddr_sed_control", 2)), ai=80),
   O("Let him come home and sing.", J(dv_self("cwddr_opposition", 6), dv_self("cwddr_sed_control", -4)), ai=20)],
  scope="DDR")

E(f"{EVD}.8", "The General Secretary on the Rhine",
  "Erich Honecker is received in Bonn with military honours, the GDR flag and the GDR anthem. He visits his birthplace in the Saarland. Kohl's speech at the dinner speaks of unity and freedom - and is broadcast live in the East.",
  "GFX_handshake_black",
  [O("Promise travel relief in return.", J(dv_self("cwddr_exit_pressure", -3), dv_self("cwddr_west_media", 2), dv_self("cwddr_hard_currency", -2)), ai=60),
   O("Recognition. Nothing else.", J(dv_self("cwddr_sed_control", 3), ger(v("cwger_ostpolitik", -3))), ai=40)],
  scope="DDR")

E(f"{EVD}.10", "'Willy Brandt ans Fenster!'",
  "When the West German chancellor arrives at the Erfurter Hof hotel, thousands break through the police lines and call for him to show himself at the window. The Stasi brings in trucks of loyal cadres for the next day.",
  "GFX_politics_protest",
  [O("Hold the crowds back.", J(dv_self("cwddr_sed_control", 2), dv_self("cwddr_opposition", 1)), ai=70),
   O("Let them cheer. It changes nothing.", J(dv_self("cwddr_exit_pressure", 3), dv_self("cwddr_west_media", 2)), ai=30)],
  scope="DDR")

E(f"{EVD}.11", "The Basic Treaty",
  "Two German states, good-neighbourly relations, permanent missions. The GDR wins the recognition it has wanted for twenty years - and opens its border a crack for journalists, visitors and the telephone.",
  "GFX_treaty",
  [O("Sign - and demarcate.", J(f"add_ideas = {P}_idea_ddr_abgrenzung", dv_self("cwddr_sed_control", 4), dv_self("cwddr_west_dependency", 3)), ai=70),
   O("Sign and open a little.", J(dv_self("cwddr_west_media", 4), dv_self("cwddr_exit_pressure", 2), dv_self("cwddr_west_dependency", 5), "add_stability = 0.02"), ai=30)],
  scope="DDR")

# IMPERIA COLD WAR — Retired GER-owned collapse chain; old queued IDs resolve without political effects.
for retired_id in (30, 31, 32, 33, 34, 36, 37, 38, 39):
    E(f"{EVD}.{retired_id}", "", "", "", [O("Continue.")], scope="DDR", hidden=True)

# IMPERIA COLD WAR — East Berlin chooses whether Bonn's unity proposal opens a treaty community.
E(f"{EVD}.35", "Bonn's Plan for Unity",
  "The federal government has published a plan: free elections in the GDR, then 'confederative structures', then a federation. Nobody in East Berlin was consulted.",
  "GFX_politics_talks",
  [O("Ask Bonn to open the existing treaty review.", J(dv_self("cwddr_sed_control", 2),
     ger(f"set_country_flag = {P}_confederation_request country_event = {{ id = {EVG}.35 days = 1 }}"),
     tt(f"{P}_tt_confed_ddr", "This asks Bonn to consider opening the existing Treaty Community negotiation. The request does not bind either state.")), ai=60),
   O("Reject Bonn's timetable.", J(dv_self("cwddr_sed_control", 3), ger(v("cwger_unity", -5))), ai=40)],
  scope="DDR")

# IMPERIA COLD WAR — Bonn must consent before the existing Treaty 9 negotiation can begin.
E(f"{EVG}.35", "East Berlin Requests Treaty Community Talks",
  "East Berlin has asked Bonn to open the existing Treaty Community negotiation. The request does not establish a confederation; both governments retain their existing treaty choices and ratification process.",
  "GFX_politics_talks",
  [O("Open Treaty 9 negotiations.", J(f"COLDWAR_GER_1970_rv_start_treaty_9 = yes", f"clr_country_flag = {P}_confederation_request"),
     trig="COLDWAR_GER_1970_rv_can_treaty_9 = yes", ai=0,
     tt=tt(f"{P}_tt_confed_open", "Costs §Y25§! political power. Opens the existing Treaty 9 negotiation; no confederation takes effect without the bilateral ratification process.")),
   O("Leave the proposal under review.", f"clr_country_flag = {P}_confederation_request", ai=0)],
  trig=f"has_country_flag = {P}_confederation_request")

# ====================================================================== Bonn's side
# IMPERIA CW — Cold War: reception costs follow a completed population transfer.
EXODUS_SUCCESS = J(money_gdp(-0.001), v("cwger_unity", 5), dv("cwddr_exit_pressure", 5))
E(f"{EVG}.130", "The Exodus",
  "East Germans are leaving through every crack in the Iron Curtain: through Hungary, through the embassy in Prague, through the permanent mission in East Berlin. Reception camps in Gießen and Marienfelde overflow.\n\nGDR crisis index: §Y[?DDR.cwddr_crisis|0]§!",
  "GFX_German_migrant",
  [O("Take them all in. They are Germans.", J(transfer(20000), f"if = {{ limit = {{ check_variable = {{ cwger_ue_arrived > 0 }} }} {EXODUS_SUCCESS} }}"), ai=60),
   O("Quiet diplomacy. Do not destabilise the East.", J(v("cwger_ostpolitik", 3), v("cwger_unity", -2), dv("cwddr_exit_pressure", -3)), ai=40)])

E(f"{EVG}.131", "Massacre in Leipzig",
  "The pictures smuggled out are blurred but unmistakable: armoured vehicles, water cannon, men with truncheons in front of the opera house. The GDR has chosen the Chinese solution.",
  "GFX_gdratwarsov",
  [O("Sanctions against the regime.", J("if = { limit = { country_exists = DDR } DDR = { ROOT = { " + P + "_sanction_prev_economic = yes } } }", tension(4), v("cwger_ostpolitik", -10),
     dv("cwddr_hard_currency", 8), f"add_ideas = {P}_idea_second_cold_war"), ai=50),
   O("Keep the channels open - for the prisoners' sake.", J(v("cwger_ostpolitik", -4), stab(-0.03), party("greens", 0.003)), ai=50)])

# IMPERIA COLD WAR — Retire the old Wall-to-annexation route; preserve IDs for queued saves.
for retired_id in (133, 134, 135, 137, 140, 141, 142, 143, 145):
    E(f"{EVG}.{retired_id}", "", "", "", [O("Continue.")], hidden=True)

E(f"{EVG}.150", "Germany Is United",
  "At midnight the flag of the Federal Republic rises in front of the Reichstag. Germany, divided since 1945, is a single state again - and the largest country in Western Europe.",
  "GFX_germany_flag", [O("A new Germany in Europe.")], scope="ANY")
