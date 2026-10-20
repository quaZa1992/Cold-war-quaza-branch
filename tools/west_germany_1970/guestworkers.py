"""Guest workers and deportations (multiplayer roleplay).

1. Recruitment agreements: Bonn offers recruitment agreements to the sending countries (COLDWAR_GDIP
   offers). The sending country decides for itself. If it accepts:
   - the Federal Republic gets more population growth and a larger workforce (dynamic modifier
     {P}_dm_guest_workers, fed by cwger_gw_pop / cwger_gw_work);
   - the sending country gets remittances every month (a share of its own GDP, paid in GER's monthly
     tick), a small negative population growth, a smaller workforce (less unemployment) and a little
     stability (dynamic modifier {P}_dm_gw_sender, fed by cwgw_pop / cwgw_work / cwgw_stab / cwgw_remit).
2. The National Directorate's deportation decree uses the IMP refugee mechanic: the country flag
   mass_deportation_campaigns makes imp_refugee_cost_calc push 4 % of the costly refugees back into the
   international pool every month; the decree also sends half of them at once. The guest workers can be
   expelled as well - then the sending countries lose their remittances and get their people back.
Events in COLDWAR_GGW.
"""
from cw_lib import *
from events_lib import E, O, EXTRA_EFFECTS
from tree import F, core, opinion
from foreign import offer, multi_offer, news_all

EVW = "COLDWAR_GGW"
DM_GER = f"{P}_dm_guest_workers"
DM_SND = f"{P}_dm_gw_sender"
STOP = f"has_country_flag = {P}_recruitment_stop"
OPEN = f"NOT = {{ {STOP} }}"
NOT_DARK = f"NOT = {{ has_country_flag = {P}_dark_regime }}"

_n = [0]


def ev(title, desc, opts, pic="GFX_German_migrant", days=3):
    _n[0] += 1
    evid = f"{EVW}.{_n[0]}"
    E(evid, title, desc, pic, opts)
    return f"country_event = {{ id = {evid} days = {days} }}"


def pct(x):
    return f"{'+' if x > 0 else '-'}{round(abs(x) * 100, 1)}%"


def ger_gw(pop, work, manpower=0):
    """GER scope: guest workers arrive."""
    key = f"{P}_tt_gw_{str(pop).replace('.', '_').replace('-', 'm')}_{str(work).replace('.', '_').replace('-', 'm')}"
    L(key, f"Guest workers: monthly population growth §G{pct(pop)}§!, workforce §G{pct(work)}§!")
    s = (f"custom_effect_tooltip = {key}\nhidden_effect = {{ add_to_variable = {{ cwger_gw_pop = {pop} }} add_to_variable = {{ cwger_gw_work = {work} }} "
         f"if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {DM_GER} }} }} }} add_dynamic_modifier = {{ modifier = {DM_GER} }} }} "
         f"force_update_dynamic_modifier = yes }}")
    if manpower:
        s += f"\nadd_manpower = {manpower}"
    return s


def sender(pop, work, remit, stab=0.01):
    """Partner scope: the sending country's side of a recruitment agreement."""
    key = f"{P}_tt_gws_" + "_".join(str(x).replace('.', '_').replace('-', 'm') for x in (pop, work, remit, stab))
    L(key, f"Remittances from the workers in Germany: §G{round(remit * 1200, 1)}% of our GDP per year§!, paid monthly\n"
           f"Monthly population growth §R{pct(pop)}§!, workforce {pct(work)} (§Gless unemployment§!), stability §G{pct(stab)}§!")
    return (f"custom_effect_tooltip = {key}\nhidden_effect = {{ set_country_flag = cwgw_sender "
            f"add_to_variable = {{ cwgw_pop = {pop} }} add_to_variable = {{ cwgw_work = {work} }} add_to_variable = {{ cwgw_stab = {stab} }} "
            f"add_to_variable = {{ cwgw_remit = {remit} }} "
            f"if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {DM_SND} }} }} }} add_dynamic_modifier = {{ modifier = {DM_SND} }} }} "
            f"force_update_dynamic_modifier = yes }}")


def dynamic_modifiers():
    L(DM_GER, "Guest Workers")
    L(DM_SND, "Workers in Germany")
    return f"""
{DM_GER} = {{
	icon = GFX_idea_german_advisors
	enable = {{ always = yes }}
	monthly_population = cwger_gw_pop
	total_workforce_modifier = cwger_gw_work
}}

{DM_SND} = {{
	icon = GFX_idea_german_advisors
	enable = {{ always = yes }}
	monthly_population = cwgw_pop
	total_workforce_modifier = cwgw_work
	stability_factor = cwgw_stab
}}
"""


# Monthly, GER scope: remittances flow home.
EXTRA_EFFECTS.append(f"""
{P}_gw_tick = {{
	every_country = {{
		limit = {{ has_country_flag = cwgw_sender check_variable = {{ cwgw_remit > 0 }} }}
		set_temp_variable = {{ treasury_change = gdp_total }}
		multiply_temp_variable = {{ treasury_change = cwgw_remit }}
		modify_treasury_effect = yes
	}}
}}
""")


# =========================================================================== RECRUITMENT
F("gw_recruitment", "social_market", 9, 1, cost=2, icon="guest_workers", name="Recruiting Abroad",
  desc="The economic miracle has run out of Germans. Since 1955 the Federal Labour Office has run 'German Commissions' in Verona, Madrid, Athens and Istanbul: doctors examine the applicants' teeth and lungs, officials check their papers, and special trains carry them north to Munich main station. Industry wants more of them every year. The question is from where - and on whose terms.",
  avail=OPEN,
  reward=J(ger_gw(0.005, 0.005), faction("bdi", 3), core("modell", fac=0.01)))
F("gw_turkey", "gw_recruitment", -2, 1, cost=3, icon="migration", name="The Istanbul Office",
  desc="The recruitment agreement with Turkey was signed in 1961 almost as an afterthought, to please a NATO ally. Ten years later the German Commission in Istanbul is the busiest of them all: young men from Anatolia queue for days for a medical examination and a one-way ticket to Cologne or Duisburg. Ankara wants the jobs and the hard currency. Bonn wants the hands.",
  avail=f"{OPEN} country_exists = TUR",
  reward=offer("gw_turkey", "TUR", "A Larger Recruitment Agreement",
               "Bonn proposes to expand the recruitment agreement: more places, more German Commissions in Anatolia, and the right for workers to bring their savings home without restrictions. The remittances would become one of our largest sources of foreign currency.",
               ger_gw(0.03, 0.02, 30000),
               partner_eff=sender(-0.03, -0.015, 0.0015), accept="Send them north.", refuse="Turkey's sons stay at home.", pic="GFX_German_migrant", ai=85))
F("gw_yugoslavia", "gw_recruitment", 0, 1, cost=3, icon="migration", name="Workers from Tito's Yugoslavia",
  desc="The only socialist country that lets its citizens work in the West: since 1968 Belgrade has sent hundreds of thousands to Stuttgart, Munich and Frankfurt. Tito calls it temporary employment abroad; his planners call it the safety valve for an unemployment that officially does not exist. The remittances keep the dinar alive.",
  avail=f"{OPEN} country_exists = SER",
  reward=offer("gw_yugoslavia", "SER", "Workers for the Federal Republic",
               "The Federal Republic proposes to expand the agreement on the employment of Yugoslav workers in Germany: more contracts, social insurance for their families at home and free transfer of their wages.",
               ger_gw(0.02, 0.015, 20000),
               partner_eff=sender(-0.03, -0.02, 0.0015), accept="Agreed - they will come back richer.", refuse="Socialism needs its workers at home.", pic="GFX_German_migrant", ai=80))
F("gw_southern_europe", "gw_recruitment", 2, 1, cost=3, icon="migration", name="Spain, Portugal, Greece",
  desc="From Andalusia, the Minho and Macedonia they come to Wolfsburg, Rüsselsheim and the Swabian machine shops, sending home the money that builds new houses in villages that have only ever known emigration. All three countries are dictatorships for now. All three need the jobs more than they would like to admit.",
  avail=OPEN,
  reward=multi_offer("gw_south", ["SPR", "POR", "GRE"], "Recruitment Agreement with Bonn",
                     "The West German government proposes to renew and enlarge the recruitment agreement for workers in its industry, with free transfer of wages and social insurance for the families who stay behind.",
                     lambda t: ger_gw(0.01, 0.008, 10000),
                     partner_eff=sender(-0.02, -0.01, 0.001), accept="Our workers will go.", refuse="Not on these terms.", pic="GFX_German_migrant", ai=80))
F("gw_maghreb", "gw_turkey", 0, 1, cost=2, icon="migration", name="Morocco and Tunisia",
  desc="The agreements with Rabat and Tunis are the smallest of all: miners for the Ruhr, labourers for the building sites, contracts limited to two years and no right to bring families. The two kingdoms - one a monarchy, one a republic of a single man - want more places. Bonn is not sure it wants to give them.",
  avail=OPEN,
  reward=multi_offer("gw_maghreb", ["MOR", "TUN"], "Workers for the Ruhr",
                     "Bonn offers to enlarge the recruitment agreement: more places for workers in German mines and industry, longer contracts and free transfer of wages.",
                     lambda t: ger_gw(0.005, 0.005, 5000),
                     partner_eff=sender(-0.01, -0.005, 0.001), accept="Agreed.", refuse="Not on these terms.", pic="GFX_German_migrant", ai=80))
F("gw_korea", "gw_southern_europe", 0, 1, cost=2, icon="migration", name="Miners and Nurses from Korea",
  desc="The strangest of the agreements: since 1963 young South Koreans have come to work underground in the Ruhr pits, and since 1966 Korean nurses have staffed German hospitals. Seoul uses their wages to finance its industrialisation and asks for more places. The hospitals, short of staff, would gladly agree.",
  avail=f"{OPEN} country_exists = KOR",
  reward=offer("gw_korea", "KOR", "Miners and Nurses for Germany",
               "Bonn proposes to enlarge the programme for Korean miners and nurses in the Federal Republic, with vocational training and credits for Korean industry in return.",
               J(ger_gw(0.003, 0.004, 3000), core("modell", social=-0.005)),
               partner_eff=J(sender(-0.005, -0.005, 0.0005), "add_political_power = 15"), accept="Our nurses will go.", refuse="We need them here.", pic="GFX_German_migrant", ai=85))
F("gw_family_reunification", "gw_yugoslavia", 0, 2, cost=3, pre=[["gw_turkey", "gw_yugoslavia", "gw_southern_europe"]], icon="refugees", name="Wives and Children",
  desc="The guests were supposed to go home after a year or two. They stayed, and now their wives and children are following them: whole streets in Kreuzberg, Duisburg-Marxloh and Cologne-Mülheim where Turkish, Greek and Serbo-Croat are spoken in the shops. The schools are not ready. The cities ask Bonn who is going to pay.",
  reward=ev("Family Reunification",
            "The Bundesrat has asked for a decision. The cities want money for schools, language courses and housing; the interior ministers of the Union-led Länder want age limits for children who may join their parents. Employers point out that a worker with his family at home works better than one who is homesick.",
            [O("Let the families come - and pay for the schools.", J(ger_gw(0.02, 0.005), core("modell", social=0.01), money_gdp(-0.002), stab(0.01), party("cdu", -0.002)), ai=60),
             O("Age limits and waiting periods.", J(ger_gw(0.005, 0.002), party("cdu", 0.002), core("bonn", drift=-0.01)), ai=40)],
            pic="GFX_German_migrant"))
F("gw_recruitment_stop", "gw_family_reunification", -1, 1, cost=2, mutex=["gw_open_doors"], icon="borders", name="The Recruitment Stop",
  desc="November 1973: the oil embargo has begun, short-time work is spreading and the labour minister stops all further recruitment from outside the Community overnight. Nobody new may come. But the millions who are already here now face a choice: go home and never come back - or stay for good. Most of them stay.",
  avail="date > 1973.1.1",
  reward=J(f"set_country_flag = {P}_recruitment_stop", stab(0.02), faction("dgb", 4), faction("bdi", -3), party("npd", -0.002),
           tt(f"{P}_tt_gw_stop", "No further recruitment agreements. The guest workers who are already here stay - and keep sending money home.")))
F("gw_open_doors", "gw_family_reunification", 1, 1, cost=3, mutex=["gw_recruitment_stop"], icon="guest_workers", name="Keep the Doors Open",
  desc="The oil shock will pass, argues the employers' federation, and the demographers are already warning of a country with too few children. Bonn refuses to stop recruiting: the German Commissions stay open, the contracts are made permanent, and the Federal Republic admits - quietly - that it has become a country of immigration.",
  avail=OPEN,
  reward=J(ger_gw(0.01, 0.015, 20000), faction("bdi", 6), faction("dgb", -3), party("npd", 0.003), protest(3), core("modell", fac=0.01)))
F("gw_guests_to_citizens", "gw_recruitment_stop", 1, 1, cost=3, pre=[["gw_recruitment_stop", "gw_open_doors"]], icon="unified", name="From Guests to Citizens",
  desc="Twenty years after the first special train arrived at Munich, the children of the guest workers speak German better than their parents' language and support Schalke or Bayern. A commissioner for foreigners, language courses for adults, the right to vote in local elections: the Republic begins to treat those who stayed as what they have become - its own people.",
  avail=NOT_DARK,
  reward=J(ger_gw(0.01, 0.005), stab(0.02), core("bonn", drift=0.02), party("greens", 0.001), party("rep", -0.002), money_gdp(-0.001),
           opinion("TUR", "medium_increase"), opinion("SER", "small_increase")))


# =========================================================================== THE DEPORTATION DECREE (dark path)
DARK = f"has_country_flag = {P}_dark_regime"
EXPEL = J(
    "set_variable = { cwger_gw_pop = -0.02 }", "set_variable = { cwger_gw_work = -0.03 }",
    f"if = {{ limit = {{ NOT = {{ has_dynamic_modifier = {{ modifier = {DM_GER} }} }} }} add_dynamic_modifier = {{ modifier = {DM_GER} }} }}",
    "force_update_dynamic_modifier = yes",
    core("modell", fac=-0.03), protest(10), faction("bdi", -15),
    f"set_country_flag = {P}_guest_workers_expelled",
    "every_country = { limit = { has_country_flag = cwgw_sender } "
    "set_variable = { cwgw_remit = 0 } set_variable = { cwgw_pop = 0.01 } set_variable = { cwgw_work = 0.015 } set_variable = { cwgw_stab = -0.02 } "
    "force_update_dynamic_modifier = yes add_opinion_modifier = { target = GER modifier = large_decrease } }",
    tt(f"{P}_tt_gw_expel", "§RThe guest workers and their families are expelled.§! The sending countries lose their remittances and get back hundreds of thousands of people without work. Industry loses its workforce."),
    news_all("Germany Expels Its Guest Workers", "The National Directorate in Bonn has ordered the expulsion of the foreign workers and their families. Trains and buses are leaving for Istanbul, Belgrade and Athens.", "GFX_German_migrant"))
F("deportation_decree", "purge_institutions", -1, 1, cost=3, ai=0, ai_mod="modifier = { factor = 0 is_ai = yes }", avail=DARK, icon="police_siren", name="The Deportation Decree",
  desc="'Germany for the Germans': the Directorate's interior ministry orders the deportation of every refugee whose asylum has not been granted, and has the camps cleared by the Federal Border Guard. Lists of foreign workers are being compiled in the labour offices as well. The churches ring their bells in protest; the UN High Commissioner for Refugees flies to Bonn and is not received.",
  reward=J("set_country_flag = mass_deportation_campaigns",
           "set_temp_variable = { cwger_dep_t = imp_costly_refugees_k }", "multiply_temp_variable = { cwger_dep_t = 0.5 }",
           "subtract_from_variable = { imp_costly_refugees_k = cwger_dep_t }", "add_to_variable = { global.imp_monthly_refugees_global_k = cwger_dep_t }",
           tt(f"{P}_tt_deport", "§RHalf of the refugees still in Germany (about §Y[?imp_costly_refugees_k|0]k§! people) are deported at once; every month afterwards, another 4% are sent back into the international refugee pool.§!"),
           v("cwger_rechtsstaat", -10), protest(6), stab(-0.02), opinion("TUR", "medium_decrease"), core("welt", support=-0.1),
           ev("The Guest Workers",
              "The refugee camps are being emptied. Now the Directorate's hardliners present the next list: four million foreigners, most of them guest workers and their families, who have lived here for years. Industry warns that the assembly lines in Wolfsburg and Cologne will stop. The ambassadors of Turkey, Yugoslavia and Greece have asked for an appointment.",
              [O("The refugees only. The factories need the workers.", J(faction("bdi", 3), v("cwger_dark", -2)), ai=70),
               O("The guest workers go as well.", J(EXPEL, v("cwger_dark", 5)), ai=30)],
              pic="GFX_German_migrant"),
           news_all("Mass Deportations from Germany", "The National Directorate has ordered the deportation of the refugees living in the Federal Republic. Camps are being cleared by the Federal Border Guard.", "GFX_German_migrant")))
