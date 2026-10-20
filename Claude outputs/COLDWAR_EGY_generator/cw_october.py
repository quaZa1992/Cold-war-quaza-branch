# COLDWAR | Mini tree "The Road to October" (added 14 Oct 2026 on request).
# Opens when Egypt is at peace with Israel while Israel still holds the Sinai (after the ceasefire).
# Preparation (missiles, air force, deception) -> coalition offers -> war council with the wargoal.
SECTION = dict(key="oct", title="The Road to October", group="Krieg", color="#8c3b2f",
               desc="Mini tree: at peace with Israel while the Sinai is occupied. Prepare and plan the next war.")

GATE = "country_exists = ISR\nNOT = { has_war_with = ISR }\n213 = { NOT = { is_controlled_by = ROOT } }"

FOCI = [
    dict(id="EGY_1970_oct_no_war_no_peace", name="No War, No Peace", sec="oct", pre=[], mx=[], cost=5, hist=1,
         av_raw=GATE, icon="gfx/interface/goals/coldwar/Six_Days_War_Arab.dds",
         eff=["PP +50 `add_political_power`", "Kriegsunterstützung +5 % `add_war_support`",
              "Militär +5 `EGY_1970_change_the_military_exact` → `change_the_military_opinion`"],
         desc="The guns along the Canal are silent, but the Sinai is still occupied and the Bar-Lev Line grows stronger every month. "
              "Neither war nor peace has returned a single kilometre of Egyptian soil. Cairo concludes that only a limited war can break the deadlock "
              "and force the superpowers to take Egypt seriously again."),
    dict(id="EGY_1970_oct_the_sam_umbrella", name="The SAM Umbrella", sec="oct", pre=[["EGY_1970_oct_no_war_no_peace"]], mx=[], cost=7, hist=1,
         icon="gfx/interface/goals/00_army/s125pechora.dds",
         eff=["Forschungsbonus CAT_surface_to_air_missiles +50 % ×2 `add_tech_bonus`", "Forschungsbonus CAT_missiles +50 % ×1 `add_tech_bonus`",
              "Streitkräfte: feindl. Luftüberlegenheit −10 % `enemy_army_bonus_air_superiority_factor` `EGY_1970_armed_forces_modifier`",
              "Kosten 0.5 % BIP `EGY_1970_pay_gdp_share`"],
         desc="Our pilots cannot yet beat the Israeli air force in the sky, so our missiles will deny it the sky. A dense belt of SA-2, SA-3 and mobile SA-6 "
              "batteries along the Canal will cover the crossing points and let the army advance under a roof of missiles."),
    dict(id="EGY_1970_oct_rebuild_the_squadrons", name="Rebuild the Squadrons", sec="oct", pre=[["EGY_1970_oct_no_war_no_peace"]], mx=[], cost=7, hist=1,
         icon="gfx/interface/goals/coldwar/Egyptian_airforce.dds",
         eff=["Idee „Air Force Rearmament“: Fabrikoutput +5 % `industrial_capacity_factory`, Luft-Ausbildungs-XP +10 % `air_training_xp_gain_factor` (1095 Tage `add_timed_idea`)",
              "Forschungsbonus CAT_aircraft +50 % ×2 `add_tech_bonus`", "Kosten 0.5 % BIP `EGY_1970_pay_gdp_share`"],
         desc="In 1967 the air force was destroyed on the ground in a single morning. Never again: hardened shelters, dispersed airfields, new MiG and Sukhoi "
              "squadrons and pilots trained for low-level strikes will give the next war an Egyptian air arm that survives the first hour."),
    dict(id="EGY_1970_oct_saggers_and_rpgs", name="Saggers and RPGs", sec="oct", pre=[["EGY_1970_oct_the_sam_umbrella"]], mx=[], cost=5, hist=1,
         icon="gfx/interface/goals/coldwar/ImprovedATGMs.dds",
         eff=["Forschungsbonus CAT_anti_tank +50 % ×2 `add_tech_bonus`", "Forschungsbonus CAT_ballistic_missiles +50 % ×1 `add_tech_bonus`",
              "Streitkräfte: Verteidigung +3 % `army_defence_factor` `EGY_1970_armed_forces_modifier`"],
         desc="Israeli armour counter-attacks will come within hours of a crossing. The infantry that crosses first will carry its own defence: "
              "Sagger missiles and RPGs in every platoon, and long-range Scuds to deter strikes deep into Egypt."),
    dict(id="EGY_1970_oct_the_deception_plan", name="Tahrir 41: The Deception Plan", sec="oct", pre=[["EGY_1970_oct_no_war_no_peace"]], mx=[], cost=7, hist=1,
         icon="gfx/interface/goals/00_security/Generic_Intelligence_Gathering.dds",
         eff=["Streitkräfte: max. Planung +10 %, Planungsgeschwindigkeit +10 % `EGY_1970_armed_forces_modifier`"],
         desc="Exercises on the Canal will become routine, reservists will be called up and sent home again, and rumours of poor Soviet maintenance will be allowed "
              "to spread. When the real attack comes, Israeli intelligence must believe it is just another exercise."),
    dict(id="EGY_1970_oct_the_october_coalition", name="The October Coalition", sec="oct", pre=[["EGY_1970_oct_no_war_no_peace"]], mx=[], cost=7, hist=1,
         icon="gfx/interface/goals/coldwar/strenthen_ties_with_syria.tga",
         eff=["Angebot an SYR, JOR, IRQ, ALG, LBA, MOR (Event, Spieler/KI entscheidet; keine Vorab-Belohnung): Kriegskoalition – bei Annahme Kriegsziel gegen ISR und Idee „October Coalition“"],
         desc="Egypt will not fight alone. Damascus must open a second front on the Golan, and the Arab capitals are asked to send squadrons, brigades and money. "
              "Every partner that agrees receives its own war aims and joins the coordinated plan."),
    dict(id="EGY_1970_oct_the_war_council", name="The War Council of October", sec="oct",
         pre=[["EGY_1970_oct_the_sam_umbrella"], ["EGY_1970_oct_rebuild_the_squadrons"], ["EGY_1970_oct_the_deception_plan"]], mx=[], cost=10, hist=1,
         icon="gfx/interface/goals/coldwar/OctoberWar.dds",
         eff=["RAW:create_wargoal = { type = take_state_focus target = ISR generator = { 213 } }",
              "Idee „The Badr Plan“: Kriegsunterstützung +10 % (365 Tage `add_timed_idea`)",
              "RAW:custom_effect_tooltip = COLDWAR_EGY_badr_plan_attack_tt",
              "Kriegsunterstützung +10 % `add_war_support`"],
         desc="The President, the war minister and the chief of staff meet behind closed doors and fix the day and the hour. The objective is limited but clear: "
              "cross the Canal, storm the Bar-Lev Line and hold the east bank under the missile umbrella until the world is forced to negotiate."),
]
LOC = {"COLDWAR_EGY_badr_plan_attack_tt": "While §YThe Badr Plan§! lasts our divisions gain §G+15%§! attack and §G+5%§! defence against §YIsrael§!."}
# targeted modifiers per idea (tag, key, value)
TARGETED = {"COLDWAR_EGY_the_badr_plan": [("ISR", "attack_bonus_against", 0.15), ("ISR", "defense_bonus_against", 0.05)],
            "COLDWAR_EGY_october_coalition": [("ISR", "attack_bonus_against", 0.10)]}
