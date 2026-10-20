"""Citizen policy and development-finance effects for the Israel 1970 expansion."""


def build(api):
    """Register citizen and finance focus rewards with the policy compiler."""
    # The civic entry sets up a real choice. Local autonomy remains an optional
    # administrative programme and may be combined with either rights route.
    api.focus(
        "citizen_review",
        "add_political_power = -35\nset_country_flag = ISR70_policy_citizen_programme",
        description="Set the cabinet programme for Arab citizens of Israel. Equal access and preferential discrimination are exclusive; municipal self-government remains a separate, compatible choice.",
        summary="Opens the two exclusive access routes and optional municipal autonomy.",
    )

    api.project(
        "equal_services", 205,
        [{"type": "infrastructure", "levels": 1}], .006, 180,
        mods={"stability_factor": .02, "social_cost_multiplier_modifier": .03},
    )
    api.focus("equal_services", "", description="Fund municipal services and transport links in state 205. The stability and continuing service costs begin when the project is completed.")

    api.idea("equal_employment_idea", "Open Public Employment", "Public hiring and vocational access are opened more broadly.",
             {"offices_worker_requirement_modifier": -.02})
    api.focus("equal_employment", api.money(.003) + "\nadd_ideas = ISR70_policy_equal_employment_idea",
        available="has_country_flag = ISR70_policy_project_equal_services_done",
        description="Spend 0.3% of GDP once on training and hiring procedures. Office worker requirement falls by 2%.")

    api.project(
        "equal_access", 205,
        [{"type": "industrial_complex", "levels": 1}], .012, 270,
        mods={"industrial_capacity_factory": .03,
              "receiving_investment_cost_modifier": -.05,
              "bureaucracy_cost_multiplier_modifier": .02},
        political_cost=50,
        available="has_country_flag = ISR70_policy_project_equal_services_done",
    )
    api.focus("equal_access", "", description="Spend 50 political power and reserve 1.2% of GDP for a one-factory credit and enterprise programme in Haifa (state 205). Reform effects begin after delivery.")

    api.idea("municipal_autonomy_idea", "Municipal Self-Government", "Planning, procurement and municipal duties are devolved, with fragmented oversight.",
             {"bureaucracy_cost_multiplier_modifier": -.10, "corruption_cost_factor": .03})
    api.focus("municipal_self", """add_political_power = -50
add_ideas = ISR70_policy_municipal_autonomy_idea""",
        description="Spend 50 political power to devolve municipal responsibilities. Bureaucracy costs fall 10%; corruption costs rise 3%.")

    api.project(
        "municipal_pacts", [205, 206],
        [{"state": 205, "type": "infrastructure", "levels": 1},
         {"state": 206, "type": "infrastructure", "levels": 1}],
        .01, 180, mods={"social_cost_multiplier_modifier": .02},
        available="has_idea = ISR70_policy_municipal_autonomy_idea",
    )
    api.focus("municipal_pacts", "", description="Opens one joint 1.0% GDP grant programme for states 205 and 206. Both projects must remain deliverable; the shared social cost applies after completion.")

    local_fund = api.state_modifier(
        "municipal_representation", "Municipal Development Funds",
        "Local infrastructure planning and procurement are funded in states 205 and 206.",
        {"state_production_speed_infrastructure_factor": .15},
        enable="is_owned_by = ISR\nis_controlled_by = ISR",
    )
    api.idea("municipal_representation_idea", "Municipal Development Funds", "Internal investment costs fall through pooled municipal development funds.",
             {"internal_investments_money_cost_modifier": -.10})
    api.focus("municipal_representation", api.money(.002) + f"""
205 = {{ add_dynamic_modifier = {{ modifier = {local_fund} }} }}
206 = {{ add_dynamic_modifier = {{ modifier = {local_fund} }} }}
add_ideas = ISR70_policy_municipal_representation_idea""",
        available="has_country_flag = ISR70_policy_project_municipal_pacts_done",
        description="Spend 0.2% of GDP to establish the funds. Infrastructure construction is 15% faster in states 205 and 206 while Israel owns and controls them; internal investment costs fall 10%.")

    api.project(
        "preferential_allocations", 206,
        [{"type": "shared_slots", "levels": 2},
         {"type": "infrastructure", "levels": 1}], .005, 180,
        mods={"stability_factor": -.02}, political_cost=0,
    )
    api.focus("preferential_allocations", "", description="Reserve 0.5% of GDP to open two building slots and deliver one infrastructure level in state 206. Stability falls by 2 percentage points on completion.")

    api.project(
        "restricted_employment", 206,
        [{"type": "industrial_complex", "levels": 1}], .012, 270,
        mods={"corruption_cost_factor": .03},
        after="set_temp_variable = { temp_opinion = 10 }\nchange_industrial_conglomerates_opinion = yes",
        available="has_country_flag = ISR70_policy_project_preferential_allocations_done",
    )
    api.focus("restricted_employment", "",
        available="has_country_flag = ISR70_policy_project_preferential_allocations_done",
        description="Reserve 1.2% of GDP for a factory in state 206. Preferential procurement raises corruption costs by 3%; industrial conglomerates gain 10 opinion if active after delivery.")

    api.idea("separate_development_idea", "Separate Municipal Funding Rules", "Public services are restricted for disadvantaged municipalities, reducing expenditure while increasing political and administrative costs.",
             {"social_cost_multiplier_modifier": -.05, "stability_factor": -.02, "corruption_cost_factor": .02})
    api.focus("separate_development", "add_ideas = ISR70_policy_separate_development_idea",
        available="has_country_flag = ISR70_policy_project_restricted_employment_done",
        description="Choose discriminatory funding rules: social costs fall 5%, stability falls 2 percentage points, and corruption costs rise 2%.")

    # Development-finance common route and three mutually exclusive financing
    # models are shaped by the focus graph; these effects retain the approved
    # office and finance values exactly.
    api.focus("finance_links", "set_country_flag = ISR70_policy_finance_programme",
              description="Open the domestic, bank-led and international development-finance programmes.")

    api.idea("clerical_training_idea", "Trained Clerical Workforce", "Accounting and administrative training improves the labour efficiency of office buildings.",
             {"offices_worker_requirement_modifier": -.03})
    api.focus("clerical_training", api.money(.004) + "\nadd_ideas = ISR70_policy_clerical_training_idea",
        description="Spend 0.4% of GDP on accounting and office training. Office worker requirement falls 3%.")

    api.idea("clearing_network_idea", "Mechanized Clearing Network", "Mechanized bookkeeping and common clearing reduce labour required per office level.",
             {"offices_worker_requirement_modifier": -.03})
    api.focus("clearing_network", api.money(.006) + "\nadd_ideas = ISR70_policy_clearing_network_idea",
        description="Spend 0.6% of GDP on mechanized clearing and bookkeeping. Office worker requirement falls a further 3% (6% across this finance route).")

    loan = """set_temp_variable = { treasury_change = gdp_total }
multiply_temp_variable = { treasury_change = 0.01 }
modify_treasury_effect = yes
set_temp_variable = { debt_change = gdp_total }
multiply_temp_variable = { debt_change = 0.01 }
modify_debt_effect = yes"""
    bond_decision = api.decision(
        "development_bond_draw", "Draw the Development Bond Facility",
        "Draw up to 1% of current GDP into the treasury. Public debt rises by exactly the same amount and remains subject to normal interest and repayment.",
        "development_bonds", "NOT = { has_active_mission = bankruptcy_incoming_collapse }",
        loan,
    )
    api.focus("development_bonds", "unlock_decision_tooltip = " + bond_decision,
              description="Unlock a one-time decision to borrow 1% of GDP. The amount borrowed is added equally to treasury liquidity and public debt; bankruptcy blocks the draw.")

    api.idea("audited_funds_idea", "Audited Development Funds", "Project procurement is subject to stronger audit and reporting requirements.",
             {"corruption_cost_factor": -.03})
    api.focus("audited_funds", """add_political_power = -50
add_ideas = ISR70_policy_audited_funds_idea""",
        description="Spend 50 political power on project oversight. Corruption costs fall 3%.")

    api.project("development_offices", 206,
                [{"type": "offices", "levels": 1}], .012, 240,
                mods={"offices_worker_requirement_modifier": -.02})
    api.focus("development_offices", "", description="Reserve 1.2% of GDP for an office level in state 206. On delivery, office worker requirement falls a further 2%, making the route total 8%.")

    api.idea("bank_consortium_idea", "Domestic Banking Consortium", "A coordinated domestic banking consortium improves office-sector productivity while increasing concentration-related costs.",
             {"offices_productivity": .03, "corruption_cost_factor": .03})
    api.focus("bank_consortium", "add_ideas = ISR70_policy_bank_consortium_idea",
              description="Office productivity rises 3%; concentration and privileged access raise corruption costs 3%.")

    api.idea("shared_services_idea", "Shared Back Offices", "Shared accounting and administration lower the workforce required per office level.",
             {"offices_worker_requirement_modifier": -.04})
    api.focus("shared_services", api.money(.005) + "\nadd_ideas = ISR70_policy_shared_services_idea",
        description="Spend 0.5% of GDP to standardize shared accounting and administration. Office worker requirement falls a further 4%, for 10% across this route.")

    api.project("industrial_credit", 204,
                [{"type": "offices", "levels": 1}], .012, 240,
                mods={"production_speed_offices_factor": .05,
                      "corruption_cost_factor": .02})
    api.focus("industrial_credit", "", description="Reserve 1.2% of GDP for an office level in Tel Aviv (204). Office construction speed rises 5%; corruption costs rise a further 2% on delivery.")

    export_idea = api.idea("export_credit_accepted", "Accepted Export Credit Line", "External lenders have accepted a civilian export-credit arrangement.",
                           {"receiving_investment_cost_modifier": -.05})
    acceptance = api.event(
        300, "Export Credit Proposal", "The United States is asked to support a civilian export-credit line. It may accept or decline.",
        [
            ("Accept the civilian export-credit line.",
             f"ISR = {{ clr_country_flag = ISR70_policy_export_credit_pending\nset_country_flag = ISR70_policy_export_credit_accepted\nadd_ideas = {export_idea} }}",
             "NOT = { has_war_with = ISR }", 3),
            ("Decline the civilian export-credit line.",
             "ISR = { clr_country_flag = ISR70_policy_export_credit_pending\nset_country_flag = ISR70_policy_export_credit_declined }", "", 1),
        ],
        trigger="original_tag = USA\nIMP_is_1970_scenario = yes\nISR = { ISR70_is_scenario = yes has_country_flag = ISR70_policy_export_credit_pending }",
    )
    request_credit = f"""clr_country_flag = ISR70_policy_export_credit_declined
set_country_flag = ISR70_policy_export_credit_pending
USA = {{ country_event = {{ id = {acceptance} days = 1 }} }}"""
    request_decision = api.decision(
        "export_credit_request", "Request an Export Credit Line",
        "Request a civilian export-credit line from the United States. A refusal leaves the request available again after the stated interval.",
        "export_credit",
        "USA = { exists = yes }\nNOT = { has_war_with = USA }\nhas_country_flag = ISR70_us_agreement\nNOT = { has_country_flag = ISR70_policy_export_credit_accepted }\nNOT = { has_country_flag = ISR70_policy_export_credit_pending }",
        request_credit, cost=50, repeatable=True, cooldown=360,
    )
    api.focus("export_credit", "unlock_decision_tooltip = " + request_decision,
        available="USA = { exists = yes }\nNOT = { has_war_with = USA }\nhas_country_flag = ISR70_us_agreement\nNOT = { has_country_flag = ISR70_policy_export_credit_accepted }",
        description="Unlock a repeatable request costing 50 political power. The United States may accept or decline; a declined request can be renewed after 360 days. An existing military agreement does not block civilian credit.")

    api.idea("equipment_finance_idea", "Financed Office Equipment", "Imported office equipment raises office productivity, with greater exposure to the international market.",
             {"offices_productivity": .05, "mdcw_cw_market_exposure": .05})
    api.focus("equipment_finance", api.money(.006) + "\nadd_ideas = ISR70_policy_equipment_finance_idea",
        available="has_country_flag = ISR70_policy_export_credit_accepted",
        description="Spend 0.6% of GDP on imported office equipment. Office productivity rises 5%; Cold War market exposure rises 5%.")

    api.project("export_services", 205,
                [{"type": "offices", "levels": 1}], .012, 240,
                mods={"production_speed_offices_factor": .10,
                      "mdcw_cw_market_exposure": .05},
                available="has_country_flag = ISR70_policy_export_credit_accepted")
    api.focus("export_services", "", description="Requires an accepted export-credit line. Reserve 1.2% of GDP for an office level in Haifa (205); office construction speed rises 10% and market exposure rises a further 5% on delivery.")
