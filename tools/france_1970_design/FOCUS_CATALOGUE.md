IMPERIA COLD WAR

# France 1970 replacement concept: complete focus catalogue

UNAPPROVED CONCEPT. No replacement focus tree installed.

All amounts are proposed balance. Coordinates use the current native 96 x 130 focus grid. All prerequisites inside a group are OR; separate groups are AND. Programmes are not runtime implementation.

## Republic and Society

Shared institutions. Pompidou remains the historical starting president.

### A State Within Reach

`COLDWAR_FRA2_public_service` | (6, 0) | 35 days | national

Prefects and central ministries possess formidable authority. A practical administrative reform can shorten the distance between citizens and public services.

Requirements: Shared national programme.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": -0.03
  }
]
```

### Executive Safeguards

`COLDWAR_FRA2_executive` | (4, 1) | 49 days | national

Defend the presidential mandate while placing the emergency machinery of the Fifth Republic on a clearer statutory footing.

Requirements: Shared national programme.
Prerequisites: (public_service).
Exclusive: parliament.

```json
[
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_presidency"
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": 0.12
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": -0.02
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### Parliamentary Checks

`COLDWAR_FRA2_parliament` | (8, 1) | 49 days | national

Strengthen scrutiny of ministers and public appointments without returning France to the unstable cabinet arithmetic of the Fourth Republic.

Requirements: Shared national programme.
Prerequisites: (public_service).
Exclusive: executive.

```json
[
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_presidency"
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.05
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": -0.03
  }
]
```

### Social Settlement

`COLDWAR_FRA2_contract` | (4, 2) | 49 days | national

Bring employers and unions into regular national bargaining. Wage assurances must be matched by investment and reliable public financing.

Requirements: Shared national programme.
Prerequisites: (executive OR parliament).
Exclusive: statute.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.1,
    "gdp_fraction": -0.001,
    "runtime_share_literal": "-0.00100",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_grenelle"
  },
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": 10,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "faction_opinion",
    "faction": "industrial_conglomerates",
    "value": -5,
    "provider": "change_industrial_conglomerates_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": 0.03
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.08
  }
]
```

### Statutory Labour Pact

`COLDWAR_FRA2_statute` | (8, 2) | 49 days | national

Legislate minimum protections and clear strike procedures. National standards can secure continuity, but imposed terms risk weakening workplace consent.

Requirements: Shared national programme.
Prerequisites: (executive OR parliament).
Exclusive: contract.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.1,
    "gdp_fraction": -0.001,
    "runtime_share_literal": "-0.00100",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_grenelle"
  },
  {
    "kind": "faction_opinion",
    "faction": "industrial_conglomerates",
    "value": 10,
    "provider": "change_industrial_conglomerates_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": -10,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "police_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Housing and Rights

`COLDWAR_FRA2_housing` | (6, 3) | 49 days | national

Fund serviced housing and the local networks needed to replace precarious accommodation around Paris. The programme supports families already sustaining industrial growth and commits the state to continuing municipal services.

Requirements: Shared national programme.
Prerequisites: (contract OR statute).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 56,
    "building": "infrastructure",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.03
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.05
  }
]
```

### Historical Recognition

`COLDWAR_FRA2_memory` | (4, 4) | 49 days | national

Recognise the distinct experiences of veterans, harkis, repatriates and Algerian families. Public recognition commits the state to support as well as remembrance.

Requirements: Shared national programme.
Prerequisites: (housing).
Exclusive: amnesty.

```json
[
  {
    "kind": "political_power",
    "value": -50
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### Republican Amnesty

`COLDWAR_FRA2_amnesty` | (8, 4) | 49 days | national

Extend the logic of the late-1960s amnesties to close domestic conflicts over Algeria. Reconciliation with former opponents leaves other claims unresolved.

Requirements: Shared national programme.
Prerequisites: (housing).
Exclusive: memory.

```json
[
  {
    "kind": "political_power",
    "value": 60
  },
  {
    "kind": "modifier",
    "key": "war_support_factor",
    "value": 0.03
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": -0.02
  }
]
```

### Civic Settlement

`COLDWAR_FRA2_civic_settlement` | (6, 5) | 35 days | national

Give public institutions a durable basis for integration and remembrance, without requiring citizens to share a single account of the end of empire.

Requirements: Shared national programme.
Prerequisites: (memory OR amnesty).
Exclusive: None.

```json
[
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_postcolonial"
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": -0.02
  }
]
```

## UDR: Gaullist Government

Pompidou and Chaban-Delmas. UDR becomes RPR only through actual dated party identity changes.

### Progress Contract

`COLDWAR_FRA2_progress` | (20, 0) | 35 days | government

Chaban-Delmas proposes to replace entrenched confrontation with negotiated progress in public enterprises. The presidency must decide how far that opening should go.

Requirements: western_conservatism_are_in_power = yes.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.1,
    "gdp_fraction": -0.001,
    "runtime_share_literal": "-0.00100",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### The New Society

`COLDWAR_FRA2_new_society` | (17, 1) | 49 days | government

Back Chaban-Delmas with a funded expansion of technical training and negotiated reform. Unions gain a place in the governing bargain while conservative Gaullists resist the prime minister opening.

Requirements: western_conservatism_are_in_power = yes.
Prerequisites: (progress).
Exclusive: presidential_industry.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.2,
    "gdp_fraction": -0.002,
    "runtime_share_literal": "-0.00200",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_industry",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": 10,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "education_cost_multiplier_modifier",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.04
  }
]
```

### Industrial Presidency

`COLDWAR_FRA2_presidential_industry` | (23, 1) | 49 days | government

Concentrate public investment in export-capable industrial groups and new productive capacity in Normandie. A stronger presidency secures scale and investment discipline while narrowing the social opening sought by organised labour.

Requirements: western_conservatism_are_in_power = yes.
Prerequisites: (progress).
Exclusive: new_society.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.4,
    "gdp_fraction": -0.004,
    "runtime_share_literal": "-0.00400",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 55,
    "building": "industrial_complex",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "production_factory_max_efficiency_factor",
    "value": 0.04
  },
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": -5,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  }
]
```

### Independent ORTF

`COLDWAR_FRA2_ortf` | (17, 2) | 49 days | government

Loosen direct ministerial supervision of the ORTF. A more credible public service limits the executive influence that Gaullist government has long enjoyed.

Requirements: western_conservatism_are_in_power = yes.
Prerequisites: (new_society).
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.02
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.04
  }
]
```

### National Champions

`COLDWAR_FRA2_national_champions` | (23, 2) | 49 days | government

Finance a new production programme in Rhone-Alpes and back national firms with public contracts. The Treasury accepts tax concessions in exchange for industrial scale and a stronger domestic supplier base.

Requirements: western_conservatism_are_in_power = yes.
Prerequisites: (presidential_industry).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.4,
    "gdp_fraction": -0.004,
    "runtime_share_literal": "-0.00400",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 62,
    "building": "industrial_complex",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "civilian_factories_productivity",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "corporate_tax_income_multiplier_modifier",
    "value": -0.04
  }
]
```

### Gaullist Participation

`COLDWAR_FRA2_participation` | (18, 3) | 49 days | government

Extend the profit-sharing instruments established in 1959 and 1967, pairing employee savings with representation. Workers gain a stake in results without replacing management with collective ownership.

Requirements: western_conservatism_are_in_power = yes.
Prerequisites: (ortf OR national_champions).
Exclusive: management.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.1,
    "gdp_fraction": -0.001,
    "runtime_share_literal": "-0.00100",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": 10,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "faction_opinion",
    "faction": "industrial_conglomerates",
    "value": -5,
    "provider": "change_industrial_conglomerates_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "corporate_tax_income_multiplier_modifier",
    "value": -0.04
  }
]
```

### Managerial Autonomy

`COLDWAR_FRA2_management` | (22, 3) | 49 days | government

Give public enterprises room to set investment and employment priorities. Commercial discipline can improve output while weakening political guarantees to workers.

Requirements: western_conservatism_are_in_power = yes.
Prerequisites: (ortf OR national_champions).
Exclusive: participation.

```json
[
  {
    "kind": "faction_opinion",
    "faction": "industrial_conglomerates",
    "value": 10,
    "provider": "change_industrial_conglomerates_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": -10,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "civilian_factories_productivity",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "corporate_tax_income_multiplier_modifier",
    "value": 0.05
  }
]
```

### Strategic Sovereignty

`COLDWAR_FRA2_debre` | (18, 4) | 49 days | government

Support an orthodox defence of national decision-making inside Gaullism. Domestic armament capacity is prioritised over cheaper pooled procurement.

Requirements: western_conservatism_are_in_power = yes.
Prerequisites: (participation).
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "industrial_capacity_factory",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "equipment_cost_multiplier_modifier",
    "value": 0.06
  },
  {
    "kind": "research",
    "category": "CAT_armor",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  }
]
```

### The Hague Opening

`COLDWAR_FRA2_pompidou_europe` | (22, 4) | 49 days | government

Use the opening achieved at The Hague to pursue enlargement and practical European cooperation, while preserving a French voice within it.

Requirements: western_conservatism_are_in_power = yes; has_idea = EU_member.
Prerequisites: (management).
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.03
  }
]
```

### Gaullist Majority

`COLDWAR_FRA2_gaullist_success` | (20, 5) | 35 days | government

Rebuild the governing movement around a social and industrial programme that can outlast its founding president.

Requirements: western_conservatism_are_in_power = yes.
Prerequisites: (debre OR pompidou_europe).
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

## Independent Republicans

Giscard leads a distinct liberal conservative programme. Governing requires native slot 2, not coalition membership.

### Modern Liberal State

`COLDWAR_FRA2_liberal_state` | (36, 0) | 35 days | government

Giscardian reform links administrative competence to private initiative. Support for enterprise requires visible restraints on public privilege.

Requirements: western_liberals_are_in_power = yes.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": -0.05
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.03
  }
]
```

### A Sound Franc

`COLDWAR_FRA2_sound_franc` | (34, 1) | 49 days | government

Defend monetary credibility through tighter public demand and a consistent budget. Investors gain confidence while domestic expansion slows.

Requirements: western_liberals_are_in_power = yes.
Prerequisites: (liberal_state).
Exclusive: credit_expansion.

```json
[
  {
    "kind": "modifier",
    "key": "tax_gain_multiplier_modifier",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "production_speed_buildings_factor",
    "value": -0.04
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.02
  }
]
```

### Modernisation Credit

`COLDWAR_FRA2_credit_expansion` | (38, 1) | 49 days | government

Direct cheaper credit toward modern equipment and housing. Faster construction brings a continuing subsidy bill and a looser claim on fiscal restraint.

Requirements: western_liberals_are_in_power = yes.
Prerequisites: (liberal_state).
Exclusive: sound_franc.

```json
[
  {
    "kind": "modifier",
    "key": "production_speed_buildings_factor",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "civilian_factories_productivity",
    "value": 0.03
  },
  {
    "kind": "modifier",
    "key": "tax_gain_multiplier_modifier",
    "value": -0.05
  }
]
```

### Private Enterprise

`COLDWAR_FRA2_business` | (34, 2) | 49 days | government

Open credit and public contracts to independent businesses and professional services in Rhone-Alpes. A wider enterprise base strengthens office-sector output while tax concessions reduce the immediate fiscal return.

Requirements: western_liberals_are_in_power = yes.
Prerequisites: (sound_franc).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 62,
    "building": "offices",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "offices_productivity",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "corporate_tax_income_multiplier_modifier",
    "value": -0.06
  }
]
```

### Credit Guarantees

`COLDWAR_FRA2_public_credit` | (38, 2) | 49 days | government

Keep public guarantees behind major projects while requiring commercial accounts. The Treasury carries the risk of supporting rapid investment.

Requirements: western_liberals_are_in_power = yes.
Prerequisites: (credit_expansion).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_industry",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "production_factory_max_efficiency_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Equal Citizenship

`COLDWAR_FRA2_civil_liberties` | (36, 3) | 49 days | government

Extend civil rights and remove barriers facing women and younger citizens. A broader public settlement demands new legal and social provision.

Requirements: western_liberals_are_in_power = yes.
Prerequisites: (business OR public_credit).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Atlantic Trade

`COLDWAR_FRA2_atlantic_liberal` | (34, 4) | 49 days | government

Seek a close commercial and technical relationship with the United States. Standardisation can reduce costs while tying French firms more closely to external suppliers.

Requirements: western_liberals_are_in_power = yes.
Prerequisites: (civil_liberties).
Exclusive: europe_liberal.

```json
[
  {
    "kind": "modifier",
    "key": "equipment_cost_multiplier_modifier",
    "value": -0.05
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": -0.04
  }
]
```

### European Market

`COLDWAR_FRA2_europe_liberal` | (38, 4) | 49 days | government

Build a European market large enough for competitive French firms. The benefits of scale require costly adjustment for sheltered producers.

Requirements: western_liberals_are_in_power = yes.
Prerequisites: (civil_liberties).
Exclusive: atlantic_liberal.

```json
[
  {
    "kind": "modifier",
    "key": "civilian_factories_productivity",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "industrial_capacity_factory",
    "value": 0.03
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": -0.03
  }
]
```

## Democratic Centre

CD governs this branch. CDP is a real separate coalition current, represented by an internal cooperation choice until a registry change is approved.

### Social Market

`COLDWAR_FRA2_social_market` | (48, 0) | 35 days | government

Lecanuet and the Christian democrats seek to combine enterprise, social responsibility and parliamentary government.

Requirements: neutrality_neutral_conservatism_are_in_power = yes.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### Regional Councils

`COLDWAR_FRA2_regional_councils` | (46, 1) | 49 days | government

Give regions a mandate and resources of their own. Local investment gains legitimacy while national direction becomes less immediate.

Requirements: neutrality_neutral_conservatism_are_in_power = yes.
Prerequisites: (social_market).
Exclusive: cdp_compromise.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 59,
    "building": "infrastructure",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "production_speed_infrastructure_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.05
  }
]
```

### Duhamel Pact

`COLDWAR_FRA2_cdp_compromise` | (50, 1) | 49 days | government

Follow the CDP precedent of cooperation with the presidential majority, using ministerial influence to secure practical social reforms.

Requirements: neutrality_neutral_conservatism_are_in_power = yes.
Prerequisites: (social_market).
Exclusive: regional_councils.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.15,
    "gdp_fraction": -0.0015,
    "runtime_share_literal": "-0.00150",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_industry",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "education_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Social Insurance

`COLDWAR_FRA2_mutuals` | (48, 2) | 49 days | government

Strengthen the mutual societies and local insurance funds that connect households to health and social provision. Better administration reduces the health-service bill while the state sustains a larger social contribution.

Requirements: neutrality_neutral_conservatism_are_in_power = yes.
Prerequisites: (regional_councils OR cdp_compromise).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.15,
    "gdp_fraction": -0.0015,
    "runtime_share_literal": "-0.00150",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "health_cost_multiplier_modifier",
    "value": -0.04
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.05
  },
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": 5,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  }
]
```

### Federal Europe

`COLDWAR_FRA2_federal_europe` | (46, 3) | 49 days | government

Pursue a stronger community of European institutions. Shared capacity gives France influence through agreement rather than unilateral freedom.

Requirements: neutrality_neutral_conservatism_are_in_power = yes; has_idea = EU_member.
Prerequisites: (mutuals).
Exclusive: atlantic_security.

```json
[
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": 0.1
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.05
  }
]
```

### Atlantic Security

`COLDWAR_FRA2_atlantic_security` | (50, 3) | 49 days | government

Seek allied security cooperation and direct more domestic resources toward public services. France accepts a smaller margin of independent military choice.

Requirements: neutrality_neutral_conservatism_are_in_power = yes.
Prerequisites: (mutuals).
Exclusive: federal_europe.

```json
[
  {
    "kind": "modifier",
    "key": "army_personnel_cost_multiplier_modifier",
    "value": -0.06
  },
  {
    "kind": "modifier",
    "key": "education_cost_multiplier_modifier",
    "value": -0.03
  },
  {
    "kind": "modifier",
    "key": "war_support_factor",
    "value": -0.04
  }
]
```

### Centrist Covenant

`COLDWAR_FRA2_centrist_covenant` | (48, 4) | 35 days | government

Bind regional notables, social organisations and parliamentary reformers to a durable governing agreement.

Requirements: neutrality_neutral_conservatism_are_in_power = yes.
Prerequisites: (federal_europe OR atlantic_security).
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.03
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": 0.03
  }
]
```

## Radical Republicans

The unified Radical Party exists in January 1970. Left-radical separation is a later political choice, not a starting party.

### American Challenge

`COLDWAR_FRA2_american_challenge` | (60, 0) | 35 days | government

Servan-Schreiber argues that France must answer American scale through education, modern management and a larger European market.

Requirements: neutrality_neutral_libertarians_are_in_power = yes.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.1,
    "gdp_fraction": -0.001,
    "runtime_share_literal": "-0.00100",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_electronics",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "education_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Private Enterprise

`COLDWAR_FRA2_radical_enterprise` | (58, 1) | 49 days | government

Give innovative private firms access to credit and public contracts. Faster renewal requires concessions to business income.

Requirements: neutrality_neutral_libertarians_are_in_power = yes.
Prerequisites: (american_challenge).
Exclusive: left_radicals.

```json
[
  {
    "kind": "modifier",
    "key": "country_productivity_growth_modifier",
    "value": 0.07
  },
  {
    "kind": "modifier",
    "key": "corporate_tax_income_multiplier_modifier",
    "value": -0.05
  }
]
```

### Republican Left

`COLDWAR_FRA2_left_radicals` | (62, 1) | 49 days | government

Choose the left-radical precedent of social reform and cooperation with the socialist movement, retaining secular republican priorities.

Requirements: neutrality_neutral_libertarians_are_in_power = yes.
Prerequisites: (american_challenge).
Exclusive: radical_enterprise.

```json
[
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.03
  }
]
```

### The Secular School

`COLDWAR_FRA2_secular_school` | (60, 2) | 49 days | government

Invest in a common public school system and technical routes beyond the grandes ecoles. The promise of equal access requires sustained funding.

Requirements: neutrality_neutral_libertarians_are_in_power = yes.
Prerequisites: (radical_enterprise OR left_radicals).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.2,
    "gdp_fraction": -0.002,
    "runtime_share_literal": "-0.00200",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_industry",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_electronics",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "education_cost_multiplier_modifier",
    "value": 0.06
  }
]
```

### Municipal France

`COLDWAR_FRA2_municipal_france` | (58, 3) | 49 days | government

Back the market towns and cooperative services of Aquitaine with professional services and agricultural processing. Municipal direction brings investment closer to producers while retaining a public administrative cost.

Requirements: neutrality_neutral_libertarians_are_in_power = yes.
Prerequisites: (secular_school).
Exclusive: europe_technology.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.45,
    "gdp_fraction": -0.0045,
    "runtime_share_literal": "-0.00450",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 60,
    "building": "offices",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "building",
    "state": 60,
    "building": "agriculture_district",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### European Ventures

`COLDWAR_FRA2_europe_technology` | (62, 3) | 49 days | government

Pool development programmes across European firms. Joint standards offer scale while reducing the share of contracts kept within France.

Requirements: neutrality_neutral_libertarians_are_in_power = yes.
Prerequisites: (secular_school).
Exclusive: municipal_france.

```json
[
  {
    "kind": "research",
    "category": "CAT_electronics",
    "bonus": 0.75,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "research_speed_factor",
    "value": 0.02
  },
  {
    "kind": "modifier",
    "key": "corporate_tax_income_multiplier_modifier",
    "value": -0.03
  }
]
```

## Socialist Party

PS exists under Alain Savary in 1970. CIR and the 1971 Epinay refoundation belong to its development, not an invented 1970 Mitterrand PS presidency.

### Socialist Renewal

`COLDWAR_FRA2_socialist_refoundation` | (74, 0) | 35 days | government

Rebuild a disoriented socialist movement and negotiate with the republican clubs. A democratic alternative requires agreement on both institutions and ownership.

Requirements: western_social_democrats_are_in_power = yes.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "political_power",
    "value": -40
  },
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": 10,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### Common Programme

`COLDWAR_FRA2_common_programme` | (71, 1) | 49 days | government

Negotiate a governing programme with the Communists and left radicals, placing public ownership and social rights at the centre of the alliance.

Requirements: western_social_democrats_are_in_power = yes.
Prerequisites: (socialist_refoundation).
Exclusive: democratic_left.

```json
[
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "industrial_capacity_factory",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.07
  }
]
```

### Independent Left

`COLDWAR_FRA2_democratic_left` | (77, 1) | 49 days | government

Seek a socialist majority through republican alliances and a clearer distance from the PCF. Greater flexibility comes at the cost of labour unity.

Requirements: western_social_democrats_are_in_power = yes.
Prerequisites: (socialist_refoundation).
Exclusive: common_programme.

```json
[
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "tax_gain_multiplier_modifier",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": -0.03
  }
]
```

### Public Bank Credit

`COLDWAR_FRA2_public_banks` | (71, 2) | 49 days | government

Give public credit institutions the staff and offices needed to direct industrial investment. The state gains a stronger financial-services base while accepting a permanent administrative establishment.

Requirements: western_social_democrats_are_in_power = yes.
Prerequisites: (common_programme).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.5,
    "gdp_fraction": -0.005,
    "runtime_share_literal": "-0.00500",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 56,
    "building": "offices",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "offices_productivity",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.06
  }
]
```

### Collective Bargaining

`COLDWAR_FRA2_social_contract_ps` | (77, 2) | 49 days | government

Put negotiated wage standards and dependable services ahead of a general transfer of ownership.

Requirements: western_social_democrats_are_in_power = yes.
Prerequisites: (democratic_left).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.18,
    "gdp_fraction": -0.0018,
    "runtime_share_literal": "-0.00180",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.08
  }
]
```

### Redistribution

`COLDWAR_FRA2_redistribution` | (72, 3) | 49 days | government

Expand household purchasing power and public employment. Domestic demand strengthens while tax receipts and external competitiveness come under pressure.

Requirements: western_social_democrats_are_in_power = yes.
Prerequisites: (public_banks OR social_contract_ps).
Exclusive: competitiveness_ps.

```json
[
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "production_speed_industrial_complex_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "tax_gain_multiplier_modifier",
    "value": -0.06
  }
]
```

### Investment Compact

`COLDWAR_FRA2_competitiveness_ps` | (76, 3) | 49 days | government

Trade a slower expansion of current benefits for investment, training and a more resilient export sector.

Requirements: western_social_democrats_are_in_power = yes.
Prerequisites: (public_banks OR social_contract_ps).
Exclusive: redistribution.

```json
[
  {
    "kind": "modifier",
    "key": "civilian_factories_productivity",
    "value": 0.07
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "education_cost_multiplier_modifier",
    "value": 0.05
  }
]
```

### The Defferre Reforms

`COLDWAR_FRA2_defferre` | (74, 4) | 49 days | government

Transfer practical authority to elected territorial institutions and finance a first regional services programme in Provence. Local direction gains substance while the central government gives up part of its immediate control.

Requirements: western_social_democrats_are_in_power = yes.
Prerequisites: (redistribution OR competitiveness_ps).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 63,
    "building": "infrastructure",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "production_speed_infrastructure_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.04
  }
]
```

### Monetary Discipline

`COLDWAR_FRA2_europe_restraint` | (72, 5) | 49 days | government

Keep a socialist government within a European monetary framework. Fiscal restraint protects credibility while limiting the pace of domestic reform.

Requirements: western_social_democrats_are_in_power = yes; has_idea = EU_member.
Prerequisites: (defferre).
Exclusive: sovereign_reflation.

```json
[
  {
    "kind": "modifier",
    "key": "tax_gain_multiplier_modifier",
    "value": 0.07
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": -0.03
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": -0.04
  }
]
```

### A Sovereign Reflation

`COLDWAR_FRA2_sovereign_reflation` | (76, 5) | 49 days | government

Retain national control of demand and credit instead of accepting an external monetary constraint. Productive expansion risks fiscal and diplomatic friction.

Requirements: western_social_democrats_are_in_power = yes.
Prerequisites: (defferre).
Exclusive: europe_restraint.

```json
[
  {
    "kind": "modifier",
    "key": "production_speed_buildings_factor",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "tax_gain_multiplier_modifier",
    "value": -0.06
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": -0.04
  }
]
```

## French Communist Party

PCF under Rochet, with Marchais rising. Eurocommunist and orthodox options are real internal tensions, not separate invented mass parties.

### Advanced Democracy

`COLDWAR_FRA2_advanced_democracy` | (90, 0) | 35 days | government

Build on communist municipalities and organised labour to seek national power. Parliamentary advances do not settle the argument over the party and the state.

Requirements: emerging_communist_state_are_in_power = yes.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.02
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Democratic Socialism

`COLDWAR_FRA2_democratic_road` | (87, 1) | 49 days | government

Accept political pluralism and a negotiated socialist transition. Wider legitimacy requires limits on the authority of the party apparatus.

Requirements: emerging_communist_state_are_in_power = yes.
Prerequisites: (advanced_democracy).
Exclusive: party_discipline.

```json
[
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.05
  }
]
```

### Party Discipline

`COLDWAR_FRA2_party_discipline` | (93, 1) | 49 days | government

Prioritise cadre cohesion and central direction. A stronger apparatus can carry a programme through opposition while deepening political mistrust.

Requirements: emerging_communist_state_are_in_power = yes.
Prerequisites: (advanced_democracy).
Exclusive: democratic_road.

```json
[
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": 0.12
  },
  {
    "kind": "modifier",
    "key": "industrial_capacity_factory",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": -0.06
  }
]
```

### Municipal Socialism

`COLDWAR_FRA2_municipal_socialism` | (87, 2) | 49 days | government

Extend the service and housing practices of communist municipalities through a national investment programme.

Requirements: emerging_communist_state_are_in_power = yes.
Prerequisites: (democratic_road).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.35,
    "gdp_fraction": -0.0035,
    "runtime_share_literal": "-0.00350",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 56,
    "building": "infrastructure",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": 10,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.06
  }
]
```

### Public Combines

`COLDWAR_FRA2_public_combine` | (93, 2) | 49 days | government

Coordinate credit and procurement through public industrial groups, funding civilian capacity in Alsace-Lorraine and an armament programme in the north. Concentration supports scale but can slow adaptation and enlarge the planning apparatus.

Requirements: emerging_communist_state_are_in_power = yes.
Prerequisites: (party_discipline).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.8,
    "gdp_fraction": -0.008,
    "runtime_share_literal": "-0.00800",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 57,
    "building": "industrial_complex",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "building",
    "state": 54,
    "building": "arms_factory",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "production_factory_max_efficiency_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": -0.04
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.07
  }
]
```

### Workers on the Board

`COLDWAR_FRA2_workers_control` | (88, 3) | 49 days | government

Give elected workplace representatives binding authority over company planning. Consent can improve implementation while slowing central decisions.

Requirements: emerging_communist_state_are_in_power = yes.
Prerequisites: (municipal_socialism OR public_combine).
Exclusive: planned_targets.

```json
[
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": 15,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "faction_opinion",
    "faction": "industrial_conglomerates",
    "value": -10,
    "provider": "change_industrial_conglomerates_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.04
  }
]
```

### Production Targets

`COLDWAR_FRA2_planned_targets` | (92, 3) | 49 days | government

Direct resources toward a limited set of industrial targets. Higher output must compete with civilian provision and local priorities.

Requirements: emerging_communist_state_are_in_power = yes.
Prerequisites: (municipal_socialism OR public_combine).
Exclusive: workers_control.

```json
[
  {
    "kind": "modifier",
    "key": "industrial_capacity_factory",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "civilian_factories_productivity",
    "value": -0.03
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": -0.03
  }
]
```

### Party Independence

`COLDWAR_FRA2_independent_communism` | (88, 4) | 49 days | government

Affirm a French political course and distance the programme from Soviet direction. Pluralist legitimacy reduces the cohesion of orthodox networks.

Requirements: emerging_communist_state_are_in_power = yes.
Prerequisites: (workers_control).
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": 0.07
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.02
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.04
  }
]
```

### Soviet Partnership

`COLDWAR_FRA2_soviet_friendship` | (92, 4) | 49 days | government

Seek Soviet technical and industrial cooperation while defending the national programme. Access to a partner brings a continuing claim on independent influence.

Requirements: emerging_communist_state_are_in_power = yes; has_idea = COLDWAR_FRA2_soviet_science_france.
Prerequisites: (planned_targets).
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "land_doctrine_cost_factor",
    "value": -0.06
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": -0.05
  }
]
```

### Socialist Settlement

`COLDWAR_FRA2_communist_settlement` | (90, 5) | 35 days | government

Consolidate the institutions of the chosen socialist course, retaining its political and economic commitments.

Requirements: emerging_communist_state_are_in_power = yes.
Prerequisites: (independent_communism OR soviet_friendship).
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.02
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.02
  }
]
```

## Unified Socialist Party

PSU has a distinct anti-authoritarian socialist programme. Autogestion is developed as a policy option, not claimed as its settled January 1970 doctrine.

### Grassroots Left

`COLDWAR_FRA2_grassroots_left` | (106, 0) | 35 days | government

Give local militants, younger workers and university activists a route into national decisions outside the dominant socialist and communist machines.

Requirements: neutrality_neutral_social_are_in_power = yes.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.03
  }
]
```

### Worker Self-Rule

`COLDWAR_FRA2_self_management` | (104, 1) | 49 days | government

Finance a worker-managed industrial pilot in Bourgogne with cooperative credit and technical advice. Experiments in self-management need capital and market access as well as workplace consent.

Requirements: neutrality_neutral_social_are_in_power = yes.
Prerequisites: (grassroots_left).
Exclusive: union_autonomy.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.4,
    "gdp_fraction": -0.004,
    "runtime_share_literal": "-0.00400",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 58,
    "building": "industrial_complex",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.05
  }
]
```

### Independent Unions

`COLDWAR_FRA2_union_autonomy` | (108, 1) | 49 days | government

Protect independent unions and negotiate sector settlements without making workplace councils the owners of production.

Requirements: neutrality_neutral_social_are_in_power = yes.
Prerequisites: (grassroots_left).
Exclusive: self_management.

```json
[
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": 15,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.07
  },
  {
    "kind": "modifier",
    "key": "industrial_capacity_factory",
    "value": 0.03
  }
]
```

### Local Public Services

`COLDWAR_FRA2_decentralised_services` | (106, 2) | 49 days | government

Bring social and educational provision closer to the communities it serves. Local control needs trained personnel and reliable funding.

Requirements: neutrality_neutral_social_are_in_power = yes.
Prerequisites: (self_management OR union_autonomy).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.12,
    "gdp_fraction": -0.0012,
    "runtime_share_literal": "-0.00120",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_industry",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "education_cost_multiplier_modifier",
    "value": 0.06
  }
]
```

### Civilian Social State

`COLDWAR_FRA2_civilian_republic` | (104, 3) | 49 days | government

Reduce the priority of military institutions and redirect attention to social investment. A quieter strategic posture weakens military mobilisation.

Requirements: neutrality_neutral_social_are_in_power = yes.
Prerequisites: (decentralised_services).
Exclusive: citizen_defence.

```json
[
  {
    "kind": "modifier",
    "key": "army_personnel_cost_multiplier_modifier",
    "value": -0.07
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": -0.03
  },
  {
    "kind": "modifier",
    "key": "war_support_factor",
    "value": -0.06
  }
]
```

### Citizen Defence

`COLDWAR_FRA2_citizen_defence` | (108, 3) | 49 days | government

Retain a citizen defence commitment alongside a broad public-service programme, giving local organisations a practical role in national resilience.

Requirements: neutrality_neutral_social_are_in_power = yes.
Prerequisites: (decentralised_services).
Exclusive: civilian_republic.

```json
[
  {
    "kind": "modifier",
    "key": "army_core_defence_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "training_time_army_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

## Political Ecology

A future ecological governing alternative, grounded in Dumont 1974 and later movements. Not a mass governing party in January 1970.

### Environmental Policy

`COLDWAR_FRA2_environment_account` | (118, 0) | 35 days | government

Measure pollution and resource use as public costs. Ecological politics grows from opposition to the social and environmental price of rapid development.

Requirements: neutrality_neutral_green_are_in_power = yes.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "energy_use_modifier_civs",
    "value": -0.04
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Energy Conservation

`COLDWAR_FRA2_efficiency_ecology` | (116, 1) | 49 days | government

Invest in insulation, efficient transport and less wasteful industry. Reducing demand requires capital before it relieves operating costs.

Requirements: neutrality_neutral_green_are_in_power = yes.
Prerequisites: (environment_account).
Exclusive: local_generation.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.22,
    "gdp_fraction": -0.0022,
    "runtime_share_literal": "-0.00220",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "energy_use_modifier_civs",
    "value": -0.1
  },
  {
    "kind": "modifier",
    "key": "production_speed_buildings_factor",
    "value": -0.03
  }
]
```

### Local Power Supply

`COLDWAR_FRA2_local_generation` | (120, 1) | 49 days | government

Fund the engineering programme and regional coordination needed to improve existing hydroelectric and distributed generation. Better use of local resources requires trained operators and a continuing technical administration.

Requirements: neutrality_neutral_green_are_in_power = yes.
Prerequisites: (environment_account).
Exclusive: efficiency_ecology.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_energy",
    "bonus": 0.75,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "energy_gain_multiplier",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "energy_use_modifier_civs",
    "value": -0.03
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.05
  }
]
```

### Rural Stewardship

`COLDWAR_FRA2_land_stewardship` | (118, 2) | 49 days | government

Protect rural services and support farming that uses fewer industrial inputs. Lower dependence on scale must be balanced against yields.

Requirements: neutrality_neutral_green_are_in_power = yes.
Prerequisites: (efficiency_ecology OR local_generation).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.2,
    "gdp_fraction": -0.002,
    "runtime_share_literal": "-0.00200",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 59,
    "building": "agriculture_district",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "faction_opinion",
    "faction": "farmers",
    "value": 10,
    "provider": "change_farmers_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Industrial Conversion

`COLDWAR_FRA2_ecological_industry` | (116, 3) | 49 days | government

Help firms convert rather than simply close. Cleaner production and new skills demand a costly transition away from the fastest possible output growth.

Requirements: neutrality_neutral_green_are_in_power = yes.
Prerequisites: (land_stewardship).
Exclusive: local_sufficiency.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.2,
    "gdp_fraction": -0.002,
    "runtime_share_literal": "-0.00200",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "country_productivity_growth_modifier",
    "value": 0.07
  },
  {
    "kind": "modifier",
    "key": "industrial_capacity_factory",
    "value": -0.03
  }
]
```

### Local Sufficiency

`COLDWAR_FRA2_local_sufficiency` | (120, 3) | 49 days | government

Prioritise local production and short supply chains. Less demand on energy and transport comes with a narrower industrial scale.

Requirements: neutrality_neutral_green_are_in_power = yes.
Prerequisites: (land_stewardship).
Exclusive: ecological_industry.

```json
[
  {
    "kind": "modifier",
    "key": "energy_use_modifier_civs",
    "value": -0.06
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "industrial_capacity_factory",
    "value": -0.04
  }
]
```

## Shopkeepers and the National Right

CID is the actual 1970 slot identity. FN requires its real foundation on 5 October 1972 and an alternate-history accession. Separate receipts prevent CID policies becoming FN rewards automatically.

### Traders' Tax Revolt

`COLDWAR_FRA2_cid_tax` | (128, 0) | 35 days | government

Nicoud and the CID challenge taxation and social charges on independent traders. Relief for small business transfers the cost to public finances.

Requirements: nationalist_right_wing_populists_are_in_power = yes; CID dated identity; before 5 October 1972.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "corporate_tax_income_multiplier_modifier",
    "value": -0.07
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": 0.04
  }
]
```

### Shopkeeper Credit

`COLDWAR_FRA2_cid_cooperatives` | (128, 1) | 49 days | government

Create a protected channel of credit and mutual assistance for independent shops facing concentration in distribution.

Requirements: nationalist_right_wing_populists_are_in_power = yes; CID dated identity; before 5 October 1972.
Prerequisites: (cid_tax).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.2,
    "gdp_fraction": -0.002,
    "runtime_share_literal": "-0.00200",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 60,
    "building": "offices",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "offices_productivity",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Authoritarian State

`COLDWAR_FRA2_fn_state` | (132, 0) | 35 days | government

A marginal nationalist movement seeks governing authority through a major alternate-history shift. Central discipline and exclusion carry serious costs to public trust.

Requirements: nationalist_right_wing_populists_are_in_power = yes; FN identity; founded on or after 5 October 1972.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": 0.1
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": -0.06
  },
  {
    "kind": "modifier",
    "key": "police_cost_multiplier_modifier",
    "value": 0.08
  }
]
```

### Industrial Protection

`COLDWAR_FRA2_fn_protection` | (130, 1) | 49 days | government

Shelter national producers from external competition. Guaranteed markets can support output while weakening productivity renewal.

Requirements: nationalist_right_wing_populists_are_in_power = yes; FN identity.
Prerequisites: (fn_state).
Exclusive: fn_export.

```json
[
  {
    "kind": "modifier",
    "key": "industrial_capacity_factory",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": -0.05
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": -0.05
  }
]
```

### Export Coalition

`COLDWAR_FRA2_fn_export` | (134, 1) | 49 days | government

Build an alliance of export firms and the nationalist state. International sales provide income but make the economy dependent on the markets it claims to resist.

Requirements: nationalist_right_wing_populists_are_in_power = yes; FN identity.
Prerequisites: (fn_state).
Exclusive: fn_protection.

```json
[
  {
    "kind": "modifier",
    "key": "corporate_tax_income_multiplier_modifier",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": -0.04
  },
  {
    "kind": "modifier",
    "key": "stability_factor",
    "value": -0.03
  }
]
```

### The Armed Nation

`COLDWAR_FRA2_fn_defence` | (132, 2) | 49 days | government

Prioritise territorial mobilisation and a national armament base, accepting the cost of sustained preparation and a more militarised public life.

Requirements: nationalist_right_wing_populists_are_in_power = yes; FN identity.
Prerequisites: (fn_protection OR fn_export).
Exclusive: None.

```json
[
  {
    "kind": "modifier",
    "key": "army_core_defence_factor",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "army_personnel_cost_multiplier_modifier",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

## Industry, Regions and Energy

Shared national assets and persistent reforms. No date barrier except technology, survey and real external crisis conditions.

### Sixth Plan

`COLDWAR_FRA2_sixth_plan` | (38, 8) | 35 days | national

Set national investment priorities for the coming decade. Planning must confront the different needs of modern exporters, older industrial districts and underserved regions.

Requirements: Shared national programme.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "country_productivity_growth_modifier",
    "value": 0.03
  }
]
```

### Regional Connections

`COLDWAR_FRA2_regional_links` | (31, 9) | 49 days | national

Connect underserved regions to ports and industrial markets. Transport investment gives smaller centres access to the national economy.

Requirements: Shared national programme.
Prerequisites: (sixth_plan).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 60,
    "building": "infrastructure",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "building",
    "state": 61,
    "building": "infrastructure",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  }
]
```

### Technical Colleges

`COLDWAR_FRA2_technical_colleges` | (36, 9) | 49 days | national

Expand routes into engineering and industrial skills beyond the elite schools, concentrating funding on the practical bottlenecks of modernisation.

Requirements: Shared national programme.
Prerequisites: (sixth_plan).
Exclusive: mass_universities.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.25,
    "gdp_fraction": -0.0025,
    "runtime_share_literal": "-0.00250",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_education"
  },
  {
    "kind": "research",
    "category": "CAT_industry",
    "bonus": 0.5,
    "uses": 2,
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_electronics",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "education_cost_multiplier_modifier",
    "value": 0.05
  }
]
```

### Mass Universities

`COLDWAR_FRA2_mass_universities` | (40, 9) | 49 days | national

Fund the institutions created by the Faure reforms and widen access to advanced study. More open universities require a larger permanent education budget.

Requirements: Shared national programme.
Prerequisites: (sixth_plan).
Exclusive: technical_colleges.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.4,
    "gdp_fraction": -0.004,
    "runtime_share_literal": "-0.00400",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_education"
  },
  {
    "kind": "research",
    "category": "CAT_electronics",
    "bonus": 0.75,
    "uses": 1,
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_nuclear_reactors",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "research_speed_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "education_cost_multiplier_modifier",
    "value": 0.12
  }
]
```

### Industrial Champions

`COLDWAR_FRA2_champion_model` | (31, 10) | 49 days | national

Focus public capital on firms large enough to compete internationally. Faster output is purchased with fiscal exposure and continued regional concentration.

Requirements: Shared national programme.
Prerequisites: (regional_links).
Exclusive: regional_industry.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.6,
    "gdp_fraction": -0.006,
    "runtime_share_literal": "-0.00600",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 55,
    "building": "industrial_complex",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "civilian_factories_productivity",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Regional Industry

`COLDWAR_FRA2_regional_industry` | (35, 10) | 49 days | national

Prepare a modern industrial site in Hauts-de-France and expand port capacity serving the industrial economy of Provence. Regional conversion needs practical connections as well as new factory buildings.

Requirements: Shared national programme.
Prerequisites: (regional_links).
Exclusive: champion_model.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.6,
    "gdp_fraction": -0.006,
    "runtime_share_literal": "-0.00600",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 54,
    "building": "industrial_complex",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "building",
    "state": 63,
    "building": "naval_base",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "province": 11834,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "civilian_factories_productivity",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Industrial Balance

`COLDWAR_FRA2_territorial_balance` | (33, 11) | 35 days | national

Bring the chosen industrial strategy together with regional transport investment, reducing the inherited gap in access to modern production.

Requirements: Shared national programme.
Prerequisites: (champion_model OR regional_industry).
Exclusive: None.

```json
[
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_regions"
  },
  {
    "kind": "modifier",
    "key": "production_speed_infrastructure_factor",
    "value": 0.03
  }
]
```

### Renew Plan Calcul

`COLDWAR_FRA2_plan_calcul` | (38, 10) | 49 days | national

Fund IRIA and the research programme supporting French computing. Public procurement and trained engineers must sustain a domestic capability against established foreign suppliers.

Requirements: Shared national programme.
Prerequisites: (technical_colleges OR mass_universities).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_electronics",
    "bonus": 0.5,
    "uses": 2,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "education_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Computer Industry

`COLDWAR_FRA2_national_computers` | (36, 11) | 49 days | national

Back the domestic computer-systems industry and its Grenoble engineering base with a funded production site. Independent supply requires public orders and continuing fiscal concessions.

Requirements: Shared national programme.
Prerequisites: (plan_calcul).
Exclusive: open_computers.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.35,
    "gdp_fraction": -0.0035,
    "runtime_share_literal": "-0.00350",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 62,
    "building": "industrial_complex",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "research",
    "category": "CAT_electronics",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "corporate_tax_income_multiplier_modifier",
    "value": -0.03
  }
]
```

### Compatible Systems

`COLDWAR_FRA2_open_computers` | (40, 11) | 49 days | national

Adopt international standards and concentrate French engineering on competitive niches. Compatibility accelerates renewal while weakening a fully independent supply chain.

Requirements: Shared national programme.
Prerequisites: (plan_calcul).
Exclusive: national_computers.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.15,
    "gdp_fraction": -0.0015,
    "runtime_share_literal": "-0.00150",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_electronics",
    "bonus": 0.75,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": -0.03
  }
]
```

### Transport Plan

`COLDWAR_FRA2_transport_choice` | (44, 9) | 35 days | national

Choose how to connect a rapidly urbanising country. National rail capacity and dispersed road access compete for the same public investment.

Requirements: Shared national programme.
Prerequisites: (sixth_plan).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.06,
    "gdp_fraction": -0.0006,
    "runtime_share_literal": "-0.00060",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_industry",
    "bonus": 0.25,
    "uses": 1,
    "once": true
  }
]
```

### High-Speed Rail

`COLDWAR_FRA2_tgv` | (42, 10) | 49 days | national

Fund SNCF engineering trials and expand the Lyon terminal and its approaches. Prototype work and a stronger station network prepare the high-speed programme for future commercial service.

Requirements: Shared national programme.
Prerequisites: (transport_choice).
Exclusive: motorways.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.6,
    "gdp_fraction": -0.006,
    "runtime_share_literal": "-0.00600",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 62,
    "building": "infrastructure",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "research",
    "category": "CAT_infrastructure",
    "bonus": 0.75,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "energy_use_modifier_civs",
    "value": -0.03
  }
]
```

### Regional Motorways

`COLDWAR_FRA2_motorways` | (46, 10) | 49 days | national

Expand the road network serving dispersed industry and smaller towns. Flexible access increases the economy reliance on motor fuel.

Requirements: Shared national programme.
Prerequisites: (transport_choice).
Exclusive: tgv.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.6,
    "gdp_fraction": -0.006,
    "runtime_share_literal": "-0.00600",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 60,
    "building": "infrastructure",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "building",
    "state": 59,
    "building": "infrastructure",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "production_speed_infrastructure_factor",
    "value": 0.07
  },
  {
    "kind": "modifier",
    "key": "energy_use_modifier_civs",
    "value": 0.04
  }
]
```

### Energy Review

`COLDWAR_FRA2_energy_review` | (45, 11) | 35 days | national

Review fuel dependence before an external crisis forces the issue. France must choose between capital-intensive generation and a wider portfolio of supply and demand measures.

Requirements: Shared national programme.
Prerequisites: (tgv OR motorways).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.05,
    "gdp_fraction": -0.0005,
    "runtime_share_literal": "-0.00050",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_energy_audit",
    "label": "Energy contingency planning"
  }
]
```

### Nuclear Expansion

`COLDWAR_FRA2_nuclear_scale` | (42, 12) | 49 days | national

Standardise the civil nuclear supply chain around the reactor choice made in 1970 and train the engineering establishment needed for expansion. The programme improves construction and operating performance while the Treasury separately funds each new reactor.

Requirements: Actual civil nuclear technology and reactor construction capacity.
Prerequisites: (energy_review).
Exclusive: diverse_energy.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.75,
    "gdp_fraction": -0.0075,
    "runtime_share_literal": "-0.00750",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_nuclear_reactors",
    "bonus": 0.5,
    "uses": 2,
    "once": true
  },
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_fund_reactor",
    "label": "Fund the first approved reactor project"
  },
  {
    "kind": "modifier",
    "key": "production_speed_nuclear_reactor_factor",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "nuclear_energy_generation_modifier",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Diversified Energy

`COLDWAR_FRA2_diverse_energy` | (48, 12) | 49 days | national

Combine efficient use with a more varied supply portfolio. Smaller commitments reduce concentration risk while leaving a larger role for imported energy.

Requirements: Shared national programme.
Prerequisites: (energy_review).
Exclusive: nuclear_scale.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.6,
    "gdp_fraction": -0.006,
    "runtime_share_literal": "-0.00600",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 55,
    "building": "fossil_powerplant",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "energy_use_modifier_civs",
    "value": -0.05
  },
  {
    "kind": "modifier",
    "key": "civilian_factories_productivity",
    "value": -0.02
  }
]
```

### Cut Oil Dependence

`COLDWAR_FRA2_oil_resilience` | (45, 13) | 35 days | national

Complete the funded energy strategy and replace the inherited assumption of permanently cheap fuel. Actual power stations and fuel contracts remain separate national assets.

Requirements: Chosen civil nuclear strategy: a supplied French reactor operates; or the funded diversified generation and conservation programme is in place.
Prerequisites: (nuclear_scale OR diverse_energy).
Exclusive: None.

```json
[
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_oil"
  }
]
```

### Agricultural Compact

`COLDWAR_FRA2_farm_policy` | (32, 12) | 35 days | national

Choose how to distribute the gains of agricultural modernisation between export-scale farms and the survival of smaller rural communities.

Requirements: Shared national programme.
Prerequisites: (territorial_balance).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.05,
    "gdp_fraction": -0.0005,
    "runtime_share_literal": "-0.00050",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  }
]
```

### Export Agriculture

`COLDWAR_FRA2_export_farms` | (30, 13) | 49 days | national

Back mechanisation and large-scale processing for European and world markets. Scale improves output while sharpening pressure on smaller holdings.

Requirements: Shared national programme.
Prerequisites: (farm_policy).
Exclusive: rural_services.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 60,
    "building": "agriculture_district",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "agricolture_productivity_modifier",
    "value": 0.08
  },
  {
    "kind": "faction_opinion",
    "faction": "farmers",
    "value": -5,
    "provider": "change_farmers_opinion",
    "parameter": "temp_opinion",
    "once": true
  }
]
```

### Rural Services

`COLDWAR_FRA2_rural_services` | (34, 13) | 49 days | national

Support cooperative services and smaller farms, keeping rural communities viable despite a slower concentration of production.

Requirements: Shared national programme.
Prerequisites: (farm_policy).
Exclusive: export_farms.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 59,
    "building": "agriculture_district",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "agricolture_productivity_modifier",
    "value": 0.04
  },
  {
    "kind": "faction_opinion",
    "faction": "farmers",
    "value": 10,
    "provider": "change_farmers_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Telecom Network

`COLDWAR_FRA2_telecoms` | (38, 12) | 49 days | national

Fund PTT and CNET network equipment, switching research and long-distance connections. New exchanges in the Paris and Rhone-Alpes service areas strengthen a telephone network that still falls short of public demand.

Requirements: has_tech = internet_1.
Prerequisites: (national_computers OR open_computers).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.45,
    "gdp_fraction": -0.0045,
    "runtime_share_literal": "-0.00450",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 56,
    "building": "internet_station",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "building",
    "state": 62,
    "building": "internet_station",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "research",
    "category": "CAT_electronics",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  }
]
```

### Industrial Basins

`COLDWAR_FRA2_conversion` | (38, 13) | 49 days | national

Prepare older coal, textile and steel districts for industrial change before closures become a national emergency.

Requirements: Shared national programme.
Prerequisites: (telecoms).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.35,
    "gdp_fraction": -0.0035,
    "runtime_share_literal": "-0.00350",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_industry",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "faction_opinion",
    "faction": "labour_unions",
    "value": 10,
    "provider": "change_labour_unions_opinion",
    "parameter": "temp_opinion",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "production_factory_efficiency_gain_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "social_cost_multiplier_modifier",
    "value": 0.05
  }
]
```

## Independent Defence

Shared armed forces. Real platforms, nuclear stockpiles and technology are never awarded by a ceremonial focus.

### Defence White Paper

`COLDWAR_FRA2_defence_review` | (62, 8) | 35 days | national

Define the relationship between the national deterrent, conventional defence in Europe and commitments overseas.

Requirements: Shared national programme.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.05,
    "gdp_fraction": -0.0005,
    "runtime_share_literal": "-0.00050",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "experience",
    "service": "army",
    "amount": 20,
    "once": true
  }
]
```

### Nuclear Deterrent

`COLDWAR_FRA2_nuclear_priority` | (59, 9) | 49 days | national

Maintain a high priority for the independent deterrent and the engineering base behind it. Conventional procurement must absorb the pressure.

Requirements: Shared national programme.
Prerequisites: (defence_review).
Exclusive: balanced_forces.

```json
[
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_deterrent"
  },
  {
    "kind": "research",
    "category": "CAT_nuclear_reactors",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "war_support_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "equipment_cost_multiplier_modifier",
    "value": 0.08
  }
]
```

### Balanced Forces

`COLDWAR_FRA2_balanced_forces` | (65, 9) | 49 days | national

Retain the deterrent while moderating its priority in the defence programme, directing more effort toward deployable conventional forces.

Requirements: Shared national programme.
Prerequisites: (defence_review).
Exclusive: nuclear_priority.

```json
[
  {
    "kind": "remove_spirit",
    "spirit": "COLDWAR_FRA2_deterrent"
  },
  {
    "kind": "modifier",
    "key": "army_org_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "equipment_cost_multiplier_modifier",
    "value": 0.03
  },
  {
    "kind": "modifier",
    "key": "war_support_factor",
    "value": -0.02
  }
]
```

### Service Reform

`COLDWAR_FRA2_service_review` | (62, 10) | 35 days | national

Choose the role of conscription in a force expected to defend Europe and operate beyond it.

Requirements: Shared national programme.
Prerequisites: (nuclear_priority OR balanced_forces).
Exclusive: None.

```json
[
  {
    "kind": "experience",
    "service": "army",
    "amount": 15,
    "once": true
  }
]
```

### Citizen Army Training

`COLDWAR_FRA2_citizen_army` | (59, 11) | 49 days | national

Invest in reserves and useful training for conscripts. Broad territorial readiness requires a longer and more expensive training establishment.

Requirements: Shared national programme.
Prerequisites: (service_review).
Exclusive: professional_core.

```json
[
  {
    "kind": "doctrine",
    "category": "land_doctrine",
    "reduction": 0.25,
    "uses": 1,
    "once": true
  },
  {
    "kind": "experience",
    "service": "army",
    "amount": 20,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "army_core_defence_factor",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "land_reinforce_rate",
    "value": 0.02
  },
  {
    "kind": "modifier",
    "key": "training_time_army_factor",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "army_personnel_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Professional Forces

`COLDWAR_FRA2_professional_core` | (65, 11) | 49 days | national

Build a smaller high-readiness core for demanding deployments. Experience and preparation come with a higher wage and support bill.

Requirements: Shared national programme.
Prerequisites: (service_review).
Exclusive: citizen_army.

```json
[
  {
    "kind": "doctrine",
    "category": "land_doctrine",
    "reduction": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "experience",
    "service": "army",
    "amount": 25,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "army_org_factor",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "army_personnel_cost_multiplier_modifier",
    "value": 0.1
  }
]
```

### Armour Procurement

`COLDWAR_FRA2_land_procurement` | (55, 10) | 35 days | national

Choose the industrial basis of future land equipment, balancing a national platform against the economies of cooperation.

Requirements: Shared national programme.
Prerequisites: (nuclear_priority OR balanced_forces).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "experience",
    "service": "army",
    "amount": 15,
    "once": true
  }
]
```

### AMX National Design

`COLDWAR_FRA2_national_armour` | (53, 11) | 49 days | national

Fund a continuing national armoured design capability. Domestic production retains expertise but carries a higher procurement cost.

Requirements: Shared national programme.
Prerequisites: (land_procurement).
Exclusive: pooled_armour.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.25,
    "gdp_fraction": -0.0025,
    "runtime_share_literal": "-0.00250",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 55,
    "building": "arms_factory",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "research",
    "category": "CAT_armor",
    "bonus": 0.75,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "equipment_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### Shared Components

`COLDWAR_FRA2_pooled_armour` | (57, 11) | 49 days | national

Pursue common components and externally agreed procurement. Lower unit costs leave French influence dependent on partner consent.

Requirements: Shared national programme.
Prerequisites: (land_procurement).
Exclusive: national_armour.

```json
[
  {
    "kind": "modifier",
    "key": "equipment_cost_multiplier_modifier",
    "value": -0.05
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": -0.04
  }
]
```

### Combat Aircraft Plan

`COLDWAR_FRA2_air_programme` | (69, 10) | 35 days | national

French air power depends on continuing design, testing and production. A domestic priority and cooperative development offer different strengths.

Requirements: Shared national programme.
Prerequisites: (nuclear_priority OR balanced_forces).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "experience",
    "service": "air",
    "amount": 20,
    "once": true
  }
]
```

### Mirage Design Line

`COLDWAR_FRA2_mirage` | (67, 11) | 49 days | national

Sustain the national combat-aircraft design line and its export potential without skipping the technologies required for a new aircraft.

Requirements: Shared national programme.
Prerequisites: (air_programme).
Exclusive: jaguar_doctrine.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.35,
    "gdp_fraction": -0.0035,
    "runtime_share_literal": "-0.00350",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_aircraft",
    "bonus": 0.75,
    "uses": 1,
    "once": true
  },
  {
    "kind": "experience",
    "service": "air",
    "amount": 20,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "air_accidents_factor",
    "value": -0.05
  },
  {
    "kind": "modifier",
    "key": "equipment_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### Jaguar Air Doctrine

`COLDWAR_FRA2_jaguar_doctrine` | (71, 11) | 49 days | national

Develop the training and procurement arrangements needed for cooperative tactical aircraft. Standardisation reduces cost at a price in autonomy.

Requirements: has_idea = COLDWAR_FRA2_jaguar_france.
Prerequisites: (air_programme).
Exclusive: mirage.

```json
[
  {
    "kind": "modifier",
    "key": "air_training_xp_gain_factor",
    "value": 0.08
  },
  {
    "kind": "modifier",
    "key": "air_fuel_consumption_factor",
    "value": -0.05
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": -0.03
  }
]
```

### Naval Commitments

`COLDWAR_FRA2_naval_review` | (62, 12) | 35 days | national

Choose between sustained oceanic presence and concentration on escorts, approaches and sea-lane protection.

Requirements: Shared national programme.
Prerequisites: (citizen_army OR professional_core).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "experience",
    "service": "navy",
    "amount": 20,
    "once": true
  }
]
```

### Ocean-Going Fleet

`COLDWAR_FRA2_ocean_navy` | (59, 13) | 49 days | national

Maintain the dockyards and trained crews needed for an oceanic fleet. Presence overseas requires a larger permanent personnel establishment.

Requirements: Shared national programme.
Prerequisites: (naval_review).
Exclusive: escort_navy.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 64,
    "building": "dockyard",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "industrial_capacity_dockyard",
    "value": 0.06
  },
  {
    "kind": "modifier",
    "key": "navy_personnel_cost_multiplier_modifier",
    "value": 0.08
  }
]
```

### Maritime Escorts

`COLDWAR_FRA2_escort_navy` | (65, 13) | 49 days | national

Prioritise dependable escorts, maintenance and coastal protection. Concentration improves routine performance while narrowing distant commitments.

Requirements: Shared national programme.
Prerequisites: (naval_review).
Exclusive: ocean_navy.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.35,
    "gdp_fraction": -0.0035,
    "runtime_share_literal": "-0.00350",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 63,
    "building": "naval_base",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "province": 11834,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "research",
    "category": "CAT_naval",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "naval_accidents_chance",
    "value": -0.08
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": -0.03
  }
]
```

### Joint Logistics

`COLDWAR_FRA2_logistics` | (55, 12) | 49 days | national

Standardise support between the services so that readiness is sustained after deployment, with a larger permanent maintenance apparatus.

Requirements: Shared national programme.
Prerequisites: (national_armour OR pooled_armour).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.3,
    "gdp_fraction": -0.003,
    "runtime_share_literal": "-0.00300",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 55,
    "building": "naval_base",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "province": 6449,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "supply_consumption_factor",
    "value": -0.05
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.04
  }
]
```

### Flight Schools

`COLDWAR_FRA2_flight_schools` | (69, 12) | 49 days | national

Train instructors and improve flight safety before expanding operational demands on new aircraft.

Requirements: Shared national programme.
Prerequisites: (mirage OR jaguar_doctrine).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.2,
    "gdp_fraction": -0.002,
    "runtime_share_literal": "-0.00200",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "experience",
    "service": "air",
    "amount": 25,
    "once": true
  },
  {
    "kind": "doctrine",
    "category": "air_doctrine",
    "reduction": 0.25,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "air_accidents_factor",
    "value": -0.08
  },
  {
    "kind": "modifier",
    "key": "airforce_personnel_cost_multiplier_modifier",
    "value": 0.05
  }
]
```

## Partnerships by Consent

Distinct French proposal focuses. Named recipients receive Accept and Decline decisions. All terms stay inspectable while locked.

### An Independent Voice

`COLDWAR_FRA2_diplomatic_review` | (104, 8) | 35 days | national

France must choose where independence is best defended through national capacity and where negotiated partnerships offer a stronger result.

Requirements: Shared national programme.
Prerequisites: None.
Exclusive: None.

```json
[
  {
    "kind": "political_power",
    "value": 50
  }
]
```

### Airbus Partnership

`COLDWAR_FRA2_airbus` | (94, 9) | 49 days | treaty

Renew the Franco-German A300 commitment as a joint civil aviation programme. Neither government obtains its partner resources without a new signed agreement.

Requirements: Shared national programme.
Prerequisites: (diplomatic_review).
Exclusive: concorde.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_airbus_response",
    "label": "Federal Republic of Germany: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "GER",
  "family": "civil_aerospace",
  "france": {
    "spirit": "COLDWAR_FRA2_airbus_france",
    "name": "The Airbus Partnership: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.5,
        "gdp_fraction": -0.005,
        "runtime_share_literal": "-0.00500",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "building",
        "state": 61,
        "building": "industrial_complex",
        "amount": 1,
        "slots": 1,
        "slots_before_construction": true,
        "once": true,
        "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
      },
      {
        "kind": "research",
        "category": "CAT_aircraft",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.06,
        "gdp_fraction": 0.0006,
        "runtime_share_literal": "0.00060",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_airbus_GER",
    "name": "The Airbus Partnership: Federal Republic of Germany",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.5,
        "gdp_fraction": -0.005,
        "runtime_share_literal": "-0.00500",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "building",
        "state": 1080,
        "building": "industrial_complex",
        "amount": 1,
        "slots": 1,
        "slots_before_construction": true,
        "once": true,
        "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
      },
      {
        "kind": "research",
        "category": "CAT_aircraft",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.06,
        "gdp_fraction": 0.0006,
        "runtime_share_literal": "0.00060",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "GER"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Federal Republic of Germany",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Concorde

`COLDWAR_FRA2_concorde` | (98, 9) | 49 days | treaty

Deepen the Anglo-French supersonic programme. Prestige and advanced engineering compete with a costly and uncertain commercial future.

Requirements: Shared national programme.
Prerequisites: (diplomatic_review).
Exclusive: airbus.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_concorde_response",
    "label": "United Kingdom: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "ENG",
  "family": "civil_aerospace",
  "france": {
    "spirit": "COLDWAR_FRA2_concorde_france",
    "name": "Concorde and Supersonic Aviation: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.35,
        "gdp_fraction": -0.0035,
        "runtime_share_literal": "-0.00350",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_aircraft",
        "bonus": 0.75,
        "uses": 1,
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_electronics",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "research_speed_factor",
        "value": 0.03
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.1,
        "gdp_fraction": 0.001,
        "runtime_share_literal": "0.00100",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_concorde_ENG",
    "name": "Concorde and Supersonic Aviation: United Kingdom",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.35,
        "gdp_fraction": -0.0035,
        "runtime_share_literal": "-0.00350",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_aircraft",
        "bonus": 0.75,
        "uses": 1,
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_electronics",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "research_speed_factor",
        "value": 0.03
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.1,
        "gdp_fraction": 0.001,
        "runtime_share_literal": "0.00100",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "ENG"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "United Kingdom",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Symphonie Satellite

`COLDWAR_FRA2_symphonie` | (94, 10) | 49 days | treaty

Use the Franco-German satellite project as the basis of a continuing telecommunications partnership.

Requirements: has_tech = internet_1; GER = { has_tech = internet_1 }.
Prerequisites: (airbus OR concorde).
Exclusive: ariane.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_symphonie_response",
    "label": "Federal Republic of Germany: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "GER",
  "family": "space",
  "france": {
    "spirit": "COLDWAR_FRA2_symphonie_france",
    "name": "The Symphonie Satellite Programme: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.2,
        "gdp_fraction": -0.002,
        "runtime_share_literal": "-0.00200",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "building",
        "state": 56,
        "building": "internet_station",
        "amount": 1,
        "slots": 1,
        "slots_before_construction": true,
        "once": true,
        "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
      },
      {
        "kind": "research",
        "category": "CAT_electronics",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_symphonie_GER",
    "name": "The Symphonie Satellite Programme: Federal Republic of Germany",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.2,
        "gdp_fraction": -0.002,
        "runtime_share_literal": "-0.00200",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "building",
        "state": 42,
        "building": "internet_station",
        "amount": 1,
        "slots": 1,
        "slots_before_construction": true,
        "once": true,
        "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
      },
      {
        "kind": "research",
        "category": "CAT_electronics",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "GER"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Federal Republic of Germany",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "has_tech = internet_1",
    "GER = { has_tech = internet_1 }",
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### European Launcher

`COLDWAR_FRA2_ariane` | (98, 10) | 49 days | treaty

Negotiate a French-led European launcher programme with a German partner. Shared engineering does not remove the high cost of independent access to space.

Requirements: Shared national programme.
Prerequisites: (airbus OR concorde).
Exclusive: symphonie.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_ariane_response",
    "label": "Federal Republic of Germany: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "GER",
  "family": "space",
  "france": {
    "spirit": "COLDWAR_FRA2_ariane_france",
    "name": "An Independent European Launcher: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.1,
        "gdp_fraction": -0.001,
        "runtime_share_literal": "-0.00100",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_electronics",
        "bonus": 0.75,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "foreign_influence_modifier",
        "value": 0.04
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.08,
        "gdp_fraction": 0.0008,
        "runtime_share_literal": "0.00080",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_ariane_GER",
    "name": "An Independent European Launcher: Federal Republic of Germany",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.08,
        "gdp_fraction": -0.0008,
        "runtime_share_literal": "-0.00080",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_electronics",
        "bonus": 0.75,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "foreign_influence_modifier",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.06,
        "gdp_fraction": 0.0006,
        "runtime_share_literal": "0.00060",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "GER"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Federal Republic of Germany",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Jaguar Partnership

`COLDWAR_FRA2_jaguar` | (102, 9) | 49 days | treaty

Renew cooperation in tactical aviation around the Jaguar precedent, combining common development with national operational requirements.

Requirements: Shared national programme.
Prerequisites: (diplomatic_review).
Exclusive: atlantic_training.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_jaguar_response",
    "label": "United Kingdom: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "ENG",
  "family": "military_technology",
  "france": {
    "spirit": "COLDWAR_FRA2_jaguar_france",
    "name": "The Jaguar Partnership: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.1,
        "gdp_fraction": -0.001,
        "runtime_share_literal": "-0.00100",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_aircraft",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "air_training_xp_gain_factor",
        "value": 0.04
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_jaguar_ENG",
    "name": "The Jaguar Partnership: United Kingdom",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.08,
        "gdp_fraction": -0.0008,
        "runtime_share_literal": "-0.00080",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_aircraft",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "air_training_xp_gain_factor",
        "value": 0.04
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "ENG"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "United Kingdom",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Atlantic Training

`COLDWAR_FRA2_atlantic_training` | (106, 9) | 49 days | treaty

Negotiate technical training and logistics cooperation while remaining outside NATO integrated command unless France separately chooses to rejoin it.

Requirements: Shared national programme.
Prerequisites: (diplomatic_review).
Exclusive: jaguar.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_atlantic_training_response",
    "label": "United States: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "USA",
  "family": "military_technology",
  "france": {
    "spirit": "COLDWAR_FRA2_atlantic_training_france",
    "name": "Atlantic Training and Logistics: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.08,
        "gdp_fraction": -0.0008,
        "runtime_share_literal": "-0.00080",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "army_org_regain",
        "value": 0.04
      },
      {
        "kind": "modifier",
        "key": "air_training_xp_gain_factor",
        "value": 0.04
      },
      {
        "kind": "modifier",
        "key": "foreign_influence_modifier",
        "value": -0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_atlantic_training_USA",
    "name": "Atlantic Training and Logistics: United States",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.06,
        "gdp_fraction": -0.0006,
        "runtime_share_literal": "-0.00060",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "land_reinforce_rate",
        "value": 0.01
      },
      {
        "kind": "modifier",
        "key": "foreign_influence_modifier",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.02,
        "gdp_fraction": 0.0002,
        "runtime_share_literal": "0.00020",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "USA"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "United States",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Soviet Science Pact

`COLDWAR_FRA2_soviet_science` | (102, 10) | 49 days | treaty

Build on the 1966 cooperation framework and the developing dialogue with Moscow, concentrating on civilian science rather than an imposed military alignment.

Requirements: Shared national programme.
Prerequisites: (jaguar OR atlantic_training).
Exclusive: us_science.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_soviet_science_response",
    "label": "Soviet Union: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "SOV",
  "family": "civil_science",
  "france": {
    "spirit": "COLDWAR_FRA2_soviet_science_france",
    "name": "Franco-Soviet Scientific Cooperation: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.1,
        "gdp_fraction": -0.001,
        "runtime_share_literal": "-0.00100",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_electronics",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "research_speed_factor",
        "value": 0.01
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_soviet_science_SOV",
    "name": "Franco-Soviet Scientific Cooperation: Soviet Union",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.08,
        "gdp_fraction": -0.0008,
        "runtime_share_literal": "-0.00080",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_electronics",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "research_speed_factor",
        "value": 0.01
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "SOV"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Soviet Union",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Atlantic Research

`COLDWAR_FRA2_us_science` | (106, 10) | 49 days | treaty

Seek an alternative civilian research accord with American institutions. Both governments decide whether shared access justifies the funding and external commitments.

Requirements: Shared national programme.
Prerequisites: (jaguar OR atlantic_training).
Exclusive: soviet_science.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_us_science_response",
    "label": "United States: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "USA",
  "family": "civil_science",
  "france": {
    "spirit": "COLDWAR_FRA2_us_science_france",
    "name": "An Atlantic Research Accord: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.1,
        "gdp_fraction": -0.001,
        "runtime_share_literal": "-0.00100",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_electronics",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "production_factory_efficiency_gain_factor",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_us_science_USA",
    "name": "An Atlantic Research Accord: United States",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.08,
        "gdp_fraction": -0.0008,
        "runtime_share_literal": "-0.00080",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_electronics",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "production_factory_efficiency_gain_factor",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "USA"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "United States",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Algerian Energy Pact

`COLDWAR_FRA2_algeria_energy` | (110, 9) | 49 days | treaty

Renegotiate energy and industrial cooperation from the 1965 agreement on the basis of Algerian sovereignty and a mutually agreed development programme.

Requirements: Shared national programme.
Prerequisites: (diplomatic_review).
Exclusive: iran_energy.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_algeria_energy_response",
    "label": "Algeria: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "ALG",
  "family": "mediterranean_energy",
  "france": {
    "spirit": "COLDWAR_FRA2_algeria_energy_france",
    "name": "Algerian Energy and Industrial Cooperation: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.2,
        "gdp_fraction": -0.002,
        "runtime_share_literal": "-0.00200",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "energy_gain_multiplier",
        "value": 0.04
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.08,
        "gdp_fraction": 0.0008,
        "runtime_share_literal": "0.00080",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_algeria_energy_ALG",
    "name": "Algerian Energy and Industrial Cooperation: Algeria",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.1,
        "gdp_fraction": -0.001,
        "runtime_share_literal": "-0.00100",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "civilian_factories_productivity",
        "value": 0.04
      },
      {
        "kind": "modifier",
        "key": "bureaucracy_cost_multiplier_modifier",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "ALG"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Algeria",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Iranian Energy Pact

`COLDWAR_FRA2_iran_energy` | (114, 9) | 49 days | treaty

Negotiate a separate energy and technical agreement with Iran. A larger supply commitment offers an alternative to the deeper educational partnership proposed to Algeria.

Requirements: Shared national programme.
Prerequisites: (diplomatic_review).
Exclusive: algeria_energy.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_iran_energy_response",
    "label": "Iran: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "PER",
  "family": "mediterranean_energy",
  "france": {
    "spirit": "COLDWAR_FRA2_iran_energy_france",
    "name": "A Diversified Iranian Supply: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.2,
        "gdp_fraction": -0.002,
        "runtime_share_literal": "-0.00200",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "energy_gain_multiplier",
        "value": 0.06
      },
      {
        "kind": "modifier",
        "key": "foreign_influence_modifier",
        "value": -0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.07,
        "gdp_fraction": 0.0007,
        "runtime_share_literal": "0.00070",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_iran_energy_PER",
    "name": "A Diversified Iranian Supply: Iran",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.1,
        "gdp_fraction": -0.001,
        "runtime_share_literal": "-0.00100",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "civilian_factories_productivity",
        "value": 0.05
      },
      {
        "kind": "modifier",
        "key": "bureaucracy_cost_multiplier_modifier",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.03,
        "gdp_fraction": 0.0003,
        "runtime_share_literal": "0.00030",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "PER"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Iran",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Algerian Institutes

`COLDWAR_FRA2_algeria_training` | (110, 10) | 49 days | treaty

Extend the Algerian Petroleum Institute assistance precedent into a continuing technical education partnership.

Requirements: Both countries have the actual active Algerian Energy and Industrial Cooperation spirit.
Prerequisites: (algeria_energy).
Exclusive: None.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_algeria_training_response",
    "label": "Algeria: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "ALG",
  "family": "technical_education",
  "france": {
    "spirit": "COLDWAR_FRA2_algeria_training_france",
    "name": "Algerian Technical Institutes: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.15,
        "gdp_fraction": -0.0015,
        "runtime_share_literal": "-0.00150",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "research_speed_factor",
        "value": 0.01
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.06,
        "gdp_fraction": 0.0006,
        "runtime_share_literal": "0.00060",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_algeria_training_ALG",
    "name": "Algerian Technical Institutes: Algeria",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.06,
        "gdp_fraction": -0.0006,
        "runtime_share_literal": "-0.00060",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "production_factory_efficiency_gain_factor",
        "value": 0.04
      },
      {
        "kind": "modifier",
        "key": "education_cost_multiplier_modifier",
        "value": 0.03
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.02,
        "gdp_fraction": 0.0002,
        "runtime_share_literal": "0.00020",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "ALG"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Algeria",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Both countries have the actual active Algerian Energy and Industrial Cooperation spirit",
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration.",
  "activation_conditions": [
    "FRA = { has_idea = COLDWAR_FRA2_algeria_energy_france }",
    "ALG = { has_idea = COLDWAR_FRA2_algeria_energy_ALG }"
  ]
}
```

### Senegal Civil Ties

`COLDWAR_FRA2_senegal_civil` | (114, 10) | 49 days | treaty

Offer a civilian partnership that gives Senegal a negotiated alternative to a relationship centred on French military presence.

Requirements: Shared national programme.
Prerequisites: (diplomatic_review).
Exclusive: senegal_defence.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_senegal_civil_response",
    "label": "Senegal: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "SEN",
  "family": "senegal",
  "france": {
    "spirit": "COLDWAR_FRA2_senegal_civil_france",
    "name": "Civil Partnership with Senegal: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.15,
        "gdp_fraction": -0.0015,
        "runtime_share_literal": "-0.00150",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "foreign_influence_modifier",
        "value": 0.04
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.06,
        "gdp_fraction": 0.0006,
        "runtime_share_literal": "0.00060",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_senegal_civil_SEN",
    "name": "Civil Partnership with Senegal: Senegal",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.04,
        "gdp_fraction": -0.0004,
        "runtime_share_literal": "-0.00040",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "civilian_factories_productivity",
        "value": 0.03
      },
      {
        "kind": "modifier",
        "key": "education_cost_multiplier_modifier",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.02,
        "gdp_fraction": 0.0002,
        "runtime_share_literal": "0.00020",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "SEN"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Senegal",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Senegal Defence

`COLDWAR_FRA2_senegal_defence` | (118, 10) | 49 days | treaty

Renegotiate training and access on the basis of explicit Senegalese consent. The defence precedent creates a security option with continuing costs for both governments.

Requirements: Shared national programme.
Prerequisites: (diplomatic_review).
Exclusive: senegal_civil.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_senegal_defence_response",
    "label": "Senegal: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "SEN",
  "family": "senegal",
  "france": {
    "spirit": "COLDWAR_FRA2_senegal_defence_france",
    "name": "A Renewed Senegalese Defence Accord: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.12,
        "gdp_fraction": -0.0012,
        "runtime_share_literal": "-0.00120",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "foreign_influence_modifier",
        "value": 0.05
      },
      {
        "kind": "modifier",
        "key": "supply_consumption_factor",
        "value": -0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.06,
        "gdp_fraction": 0.0006,
        "runtime_share_literal": "0.00060",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_senegal_defence_SEN",
    "name": "A Renewed Senegalese Defence Accord: Senegal",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.04,
        "gdp_fraction": -0.0004,
        "runtime_share_literal": "-0.00040",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "army_org_factor",
        "value": 0.04
      },
      {
        "kind": "modifier",
        "key": "army_personnel_cost_multiplier_modifier",
        "value": 0.03
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.02,
        "gdp_fraction": 0.0002,
        "runtime_share_literal": "0.00020",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "SEN"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Senegal",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Rhine Industry Pact

`COLDWAR_FRA2_rhine` | (96, 11) | 49 days | treaty

Link conversion and technical training in neighbouring industrial regions, sharing the cost of modernisation rather than assigning foreign construction unilaterally.

Requirements: Shared national programme.
Prerequisites: (symphonie OR ariane).
Exclusive: italy.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_rhine_response",
    "label": "Federal Republic of Germany: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "GER",
  "family": "regional_industry",
  "france": {
    "spirit": "COLDWAR_FRA2_rhine_france",
    "name": "Franco-German Industrial Regions: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.5,
        "gdp_fraction": -0.005,
        "runtime_share_literal": "-0.00500",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "building",
        "state": 57,
        "building": "industrial_complex",
        "amount": 1,
        "slots": 1,
        "slots_before_construction": true,
        "once": true,
        "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
      },
      {
        "kind": "research",
        "category": "CAT_industry",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_rhine_GER",
    "name": "Franco-German Industrial Regions: Federal Republic of Germany",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.5,
        "gdp_fraction": -0.005,
        "runtime_share_literal": "-0.00500",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "building",
        "state": 42,
        "building": "industrial_complex",
        "amount": 1,
        "slots": 1,
        "slots_before_construction": true,
        "once": true,
        "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
      },
      {
        "kind": "research",
        "category": "CAT_industry",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "GER"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Federal Republic of Germany",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### Italian Cooperation

`COLDWAR_FRA2_italy` | (100, 11) | 49 days | treaty

Offer Italy a joint machinery and industrial research programme. Both economies gain from specialisation while accepting a smaller national share of public contracts.

Requirements: Shared national programme.
Prerequisites: (symphonie OR ariane).
Exclusive: rhine.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_italy_response",
    "label": "Italy: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "ITA",
  "family": "regional_industry",
  "france": {
    "spirit": "COLDWAR_FRA2_italy_france",
    "name": "Franco-Italian Industrial Cooperation: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.1,
        "gdp_fraction": -0.001,
        "runtime_share_literal": "-0.00100",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_industry",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "civilian_factories_productivity",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_italy_ITA",
    "name": "Franco-Italian Industrial Cooperation: Italy",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.08,
        "gdp_fraction": -0.0008,
        "runtime_share_literal": "-0.00080",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_industry",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "civilian_factories_productivity",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "ITA"
  },
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Italy",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate.",
  "acceptance_conditions": [
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration."
}
```

### EEC Cooperation

`COLDWAR_FRA2_community_entry` | (104, 11) | 35 days | national

Work through the European Communities to shape enlargement and cooperation. Membership rights and the interests of other RP governments remain part of the existing institutions.

Requirements: has_idea = EU_member.
Prerequisites: (diplomatic_review).
Exclusive: None.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_community_negotiations",
    "label": "Community enlargement and institutional negotiations"
  }
]
```

## Gaullist NATO Strategy

A UDR sub-tree. France remains a NATO treaty member outside integrated military command. The three strategies prioritise different funded capabilities and partnerships, not three fictional accession statuses.

### France and NATO

`COLDWAR_FRA2_nato_review` | (20, 7) | 35 days | government

France remains bound by the Atlantic Treaty after the 1966 command withdrawal. Pompidou can reaffirm national discretion, deepen conditional military cooperation or concentrate on a European contribution to the Alliance. None of these choices transfers authority over the French deterrent.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member.
Prerequisites: (gaullist_success).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.05,
    "gdp_fraction": -0.0005,
    "runtime_share_literal": "-0.00050",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "political_power",
    "value": -35
  },
  {
    "kind": "experience",
    "service": "army",
    "amount": 10,
    "once": true
  },
  {
    "kind": "experience",
    "service": "navy",
    "amount": 10,
    "once": true
  }
]
```

### National Nuclear Veto

`COLDWAR_FRA2_nato_nuclear_veto` | (18, 8) | 35 days | government

Finance an independent assessment and decision system for the force de frappe. National authority strengthens the Gaullist mandate while France bears the full equipment-support burden of its separate capability.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member.
Prerequisites: (nato_review).
Exclusive: nato_nuclear_consult.

```json
[
  {
    "kind": "political_power",
    "value": -40
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "equipment_cost_multiplier_modifier",
    "value": 0.02
  }
]
```

### Nuclear Consultation

`COLDWAR_FRA2_nato_nuclear_consult` | (22, 8) | 35 days | government

Consult allies about deterrence and escalation while reserving the final decision to France. Better understanding of allied doctrine does not entail NPG membership, nuclear sharing or an allied veto over French weapons.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member.
Prerequisites: (nato_review).
Exclusive: nato_nuclear_veto.

```json
[
  {
    "kind": "political_power",
    "value": -40
  },
  {
    "kind": "doctrine",
    "category": "land_doctrine",
    "reduction": 0.25,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": 0.03
  },
  {
    "kind": "modifier",
    "key": "political_power_factor",
    "value": -0.03
  }
]
```

### An Independent Ally

`COLDWAR_FRA2_nato_independent` | (16, 9) | 49 days | government

Keep Atlantic political solidarity while concentrating discretionary defence funds on capabilities controlled and sustained by France. A stronger independent position reduces outside leverage but duplicates part of the equipment-support establishment.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member.
Prerequisites: (nato_nuclear_veto OR nato_nuclear_consult).
Exclusive: nato_pragmatic, nato_european.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.1,
    "gdp_fraction": -0.001,
    "runtime_share_literal": "-0.00100",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_defense_modifier",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "equipment_cost_multiplier_modifier",
    "value": 0.02
  }
]
```

### Selective Cooperation

`COLDWAR_FRA2_nato_pragmatic` | (20, 9) | 49 days | government

Extend liaison, exercises and contingency preparation under national authority. France can improve practical support without assigning forces automatically to allied command, at the cost of a larger coordination staff.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member.
Prerequisites: (nato_nuclear_veto OR nato_nuclear_consult).
Exclusive: nato_independent, nato_european.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "modifier",
    "key": "supply_consumption_factor",
    "value": -0.02
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.02
  }
]
```

### A European Pillar

`COLDWAR_FRA2_nato_european` | (24, 9) | 49 days | government

Concentrate the new programme on European capability and compatible equipment. A larger European voice within the Alliance requires technical preparation and sustained political coordination.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member.
Prerequisites: (nato_nuclear_veto OR nato_nuclear_consult).
Exclusive: nato_independent, nato_pragmatic.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.12,
    "gdp_fraction": -0.0012,
    "runtime_share_literal": "-0.00120",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_electronics",
    "bonus": 0.25,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "foreign_influence_modifier",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### National Land Forces

`COLDWAR_FRA2_nato_land_priority` | (15, 10) | 49 days | government

Fund the French land-equipment base and the training needed for an independent continental contribution. Domestic output expands while sustaining the equipment estate becomes more expensive.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member.
Prerequisites: (nato_independent).
Exclusive: nato_sea_priority.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.5,
    "gdp_fraction": -0.005,
    "runtime_share_literal": "-0.00500",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 54,
    "building": "arms_factory",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "military_factories_productivity",
    "value": 0.04
  },
  {
    "kind": "modifier",
    "key": "equipment_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### National Sea Power

`COLDWAR_FRA2_nato_sea_priority` | (17, 10) | 49 days | government

Give the discretionary programme to national naval construction and support. More shipyard capacity requires a larger naval personnel establishment.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member.
Prerequisites: (nato_independent).
Exclusive: nato_land_priority.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.5,
    "gdp_fraction": -0.005,
    "runtime_share_literal": "-0.00500",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 64,
    "building": "dockyard",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "dockyard_productivity",
    "value": 0.05
  },
  {
    "kind": "modifier",
    "key": "navy_personnel_cost_multiplier_modifier",
    "value": 0.05
  }
]
```

### Armour Design

`COLDWAR_FRA2_nato_land_design` | (15, 11) | 49 days | government

Carry the national land programme through testing and engineering. Independent design expertise must be financed rather than obtained through an automatic technology award.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member.
Prerequisites: (nato_land_priority).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.15,
    "gdp_fraction": -0.0015,
    "runtime_share_literal": "-0.00150",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_armor",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "doctrine",
    "category": "land_doctrine",
    "reduction": 0.25,
    "uses": 1,
    "once": true
  }
]
```

### French Naval Design

`COLDWAR_FRA2_nato_sea_design` | (17, 11) | 49 days | government

Fund design teams and sea trials for a fleet sustained by French institutions. The programme develops knowledge without granting ships or future hull technology.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member.
Prerequisites: (nato_sea_priority).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.15,
    "gdp_fraction": -0.0015,
    "runtime_share_literal": "-0.00150",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "research",
    "category": "CAT_naval",
    "bonus": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "doctrine",
    "category": "naval_doctrine",
    "reduction": 0.25,
    "uses": 1,
    "once": true
  }
]
```

### Rhine Field Exercises

`COLDWAR_FRA2_nato_rhine` | (19, 10) | 49 days | treaty

Offer an additional Franco-German land-exercise programme alongside the existing arrangements for French forces in Germany. Each government retains control of its forces; no new basing rights or automatic wartime commitment are imposed.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member; GER = { has_idea = NATO_member }.
Prerequisites: (nato_pragmatic).
Exclusive: nato_atlantic_fleet.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_nato_rhine_response",
    "label": "Federal Republic of Germany: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "GER",
  "family": "gaullist_operational_cooperation",
  "france": {
    "spirit": "COLDWAR_FRA2_nato_rhine_france",
    "name": "Rhine Field Exercises: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.08,
        "gdp_fraction": -0.0008,
        "runtime_share_literal": "-0.00080",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "army_org_regain",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.03,
        "gdp_fraction": 0.0003,
        "runtime_share_literal": "0.00030",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      },
      {
        "kind": "doctrine",
        "category": "land_doctrine",
        "reduction": 0.25,
        "uses": 1,
        "once": true
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_nato_rhine_GER",
    "name": "Rhine Field Exercises: Federal Republic of Germany",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.08,
        "gdp_fraction": -0.0008,
        "runtime_share_literal": "-0.00080",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "army_org_regain",
        "value": 0.02
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.02,
        "gdp_fraction": 0.0002,
        "runtime_share_literal": "0.00020",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      },
      {
        "kind": "doctrine",
        "category": "land_doctrine",
        "reduction": 0.25,
        "uses": 1,
        "once": true
      }
    ],
    "payer": "GER"
  },
  "activation_conditions": [
    "FRA = { has_idea = NATO_member }",
    "GER = { has_idea = NATO_member }"
  ],
  "activation_note": "Membership requirements supplement the bilateral peace, embargo and four mirrored sanction guards. Current French party is not a condition of an already signed treaty.",
  "acceptance_conditions": [
    "western_conservatism_are_in_power = yes",
    "has_idea = NATO_member",
    "GER = { has_idea = NATO_member }",
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration.",
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Federal Republic of Germany",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate."
}
```

### Atlantic Exercises

`COLDWAR_FRA2_nato_atlantic_fleet` | (21, 10) | 49 days | treaty

Offer Britain a funded programme of sea exercises and fleet-support training. Its authority is bilateral and leaves both governments free to decide whether to commit ships in a crisis.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member; ENG = { has_idea = NATO_member }.
Prerequisites: (nato_pragmatic).
Exclusive: nato_rhine.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_nato_atlantic_fleet_response",
    "label": "United Kingdom: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "ENG",
  "family": "gaullist_operational_cooperation",
  "france": {
    "spirit": "COLDWAR_FRA2_nato_atlantic_fleet_france",
    "name": "Atlantic Naval Exercises: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.08,
        "gdp_fraction": -0.0008,
        "runtime_share_literal": "-0.00080",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "naval_accidents_chance",
        "value": -0.05
      },
      {
        "kind": "experience",
        "service": "navy",
        "amount": 15,
        "once": true
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.03,
        "gdp_fraction": 0.0003,
        "runtime_share_literal": "0.00030",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      },
      {
        "kind": "doctrine",
        "category": "naval_doctrine",
        "reduction": 0.25,
        "uses": 1,
        "once": true
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_nato_atlantic_fleet_ENG",
    "name": "Atlantic Naval Exercises: United Kingdom",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.08,
        "gdp_fraction": -0.0008,
        "runtime_share_literal": "-0.00080",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "modifier",
        "key": "naval_accidents_chance",
        "value": -0.05
      },
      {
        "kind": "experience",
        "service": "navy",
        "amount": 15,
        "once": true
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.02,
        "gdp_fraction": 0.0002,
        "runtime_share_literal": "0.00020",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      },
      {
        "kind": "doctrine",
        "category": "naval_doctrine",
        "reduction": 0.25,
        "uses": 1,
        "once": true
      }
    ],
    "payer": "ENG"
  },
  "activation_conditions": [
    "FRA = { has_idea = NATO_member }",
    "ENG = { has_idea = NATO_member }"
  ],
  "activation_note": "Membership requirements supplement the bilateral peace, embargo and four mirrored sanction guards. Current French party is not a condition of an already signed treaty.",
  "acceptance_conditions": [
    "western_conservatism_are_in_power = yes",
    "has_idea = NATO_member",
    "ENG = { has_idea = NATO_member }",
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration.",
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "United Kingdom",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate."
}
```

### Joint Contingencies

`COLDWAR_FRA2_nato_conditional_plan` | (19, 11) | 49 days | government

Train national staffs to coordinate an agreed contingency while preserving the French decision to commit forces. Reliable planning requires a continuing personnel allocation.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member; has_idea = COLDWAR_FRA2_nato_rhine_france.
Prerequisites: (nato_rhine).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.1,
    "gdp_fraction": -0.001,
    "runtime_share_literal": "-0.00100",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "doctrine",
    "category": "land_doctrine",
    "reduction": 0.25,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "max_planning",
    "value": 0.03
  },
  {
    "kind": "modifier",
    "key": "army_personnel_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### Joint Fleet Support

`COLDWAR_FRA2_nato_fleet_support` | (21, 11) | 49 days | government

Apply the lessons of the agreed naval exercises to French fleet support. More efficient supply comes with a larger trained support establishment.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member; has_idea = COLDWAR_FRA2_nato_atlantic_fleet_france.
Prerequisites: (nato_atlantic_fleet).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.25,
    "gdp_fraction": -0.0025,
    "runtime_share_literal": "-0.00250",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "building",
    "state": 64,
    "building": "naval_base",
    "amount": 1,
    "slots": 1,
    "slots_before_construction": true,
    "once": true,
    "province": 6536,
    "transaction": "Validate state ownership/control, province control if any, native level capacity and slot capacity. Grant the slots first and the building in one guarded transaction with the single GDP debit."
  },
  {
    "kind": "modifier",
    "key": "supply_consumption_factor",
    "value": -0.03
  },
  {
    "kind": "modifier",
    "key": "navy_personnel_cost_multiplier_modifier",
    "value": 0.03
  }
]
```

### Land Standardisation

`COLDWAR_FRA2_nato_europe_land` | (23, 10) | 49 days | treaty

Offer West Germany an additional programme for compatible land equipment and maintenance standards. Both states can reduce their equipment-support bills while financing common technical work; no national force is transferred to a new command.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member; GER = { has_idea = NATO_member }.
Prerequisites: (nato_european).
Exclusive: nato_europe_sea.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_nato_europe_land_response",
    "label": "Federal Republic of Germany: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "GER",
  "family": "gaullist_european_pillar",
  "france": {
    "spirit": "COLDWAR_FRA2_nato_europe_land_france",
    "name": "European Land Standards: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.12,
        "gdp_fraction": -0.0012,
        "runtime_share_literal": "-0.00120",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_armor",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "equipment_cost_multiplier_modifier",
        "value": -0.04
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_nato_europe_land_GER",
    "name": "European Land Standards: Federal Republic of Germany",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.12,
        "gdp_fraction": -0.0012,
        "runtime_share_literal": "-0.00120",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_armor",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "equipment_cost_multiplier_modifier",
        "value": -0.04
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "GER"
  },
  "activation_conditions": [
    "FRA = { has_idea = NATO_member }",
    "GER = { has_idea = NATO_member }"
  ],
  "activation_note": "Membership requirements supplement the bilateral peace, embargo and four mirrored sanction guards. Current French party is not a condition of an already signed treaty.",
  "acceptance_conditions": [
    "western_conservatism_are_in_power = yes",
    "has_idea = NATO_member",
    "GER = { has_idea = NATO_member }",
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration.",
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "Federal Republic of Germany",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate."
}
```

### Naval Industry Pact

`COLDWAR_FRA2_nato_europe_sea` | (25, 10) | 49 days | treaty

Offer Britain a European naval engineering and production partnership. Shared development helps both shipbuilding sectors while requiring a continuing public contribution.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member; ENG = { has_idea = NATO_member }.
Prerequisites: (nato_european).
Exclusive: nato_europe_land.

```json
[
  {
    "kind": "unlock_decision",
    "id": "COLDWAR_FRA2_nato_europe_sea_response",
    "label": "United Kingdom: acceptance or refusal"
  }
]
```

**If they accept**

```json
{
  "partner": "ENG",
  "family": "gaullist_european_pillar",
  "france": {
    "spirit": "COLDWAR_FRA2_nato_europe_sea_france",
    "name": "European Naval Industry: France",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.12,
        "gdp_fraction": -0.0012,
        "runtime_share_literal": "-0.00120",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_naval",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "industrial_capacity_dockyard",
        "value": 0.04
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "FRA"
  },
  "recipient": {
    "spirit": "COLDWAR_FRA2_nato_europe_sea_ENG",
    "name": "European Naval Industry: United Kingdom",
    "effects": [
      {
        "kind": "treasury_gdp",
        "percent": -0.12,
        "gdp_fraction": -0.0012,
        "runtime_share_literal": "-0.00120",
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "at_payment",
        "once": true
      },
      {
        "kind": "research",
        "category": "CAT_naval",
        "bonus": 0.5,
        "uses": 1,
        "once": true
      },
      {
        "kind": "modifier",
        "key": "industrial_capacity_dockyard",
        "value": 0.04
      },
      {
        "kind": "weekly_gdp_expense",
        "annual_gdp_percent": 0.04,
        "gdp_fraction": 0.0004,
        "runtime_share_literal": "0.00040",
        "divisor": 52,
        "base": "gdp_total",
        "payer": "own_country",
        "valuation": "weekly_recalculation"
      }
    ],
    "payer": "ENG"
  },
  "activation_conditions": [
    "FRA = { has_idea = NATO_member }",
    "ENG = { has_idea = NATO_member }"
  ],
  "activation_note": "Membership requirements supplement the bilateral peace, embargo and four mirrored sanction guards. Current French party is not a condition of an already signed treaty.",
  "acceptance_conditions": [
    "western_conservatism_are_in_power = yes",
    "has_idea = NATO_member",
    "ENG = { has_idea = NATO_member }",
    "Named recipient chooses Accept",
    "Both countries exist, are at peace with one another and have no mutual native embargo or any of the four mirrored Imperia sanction classes",
    "The proposal and one-time transaction are still valid",
    "Every promised state/province is owned and fully controlled by its recipient; native building and slot capacity is available"
  ],
  "acceptance_transaction": "Recheck consent, country and programme conditions, own GDP initialisation and all asset feasibility before mutation. Calculate each setup from its own payer current GDP. Charge and grant both sides atomically once; add each state slot before its building and record one-time research, doctrine, experience and faction awards. No Treasury-balance gate, fixed building charge, repeated setup or replay on restoration.",
  "cost_basis": "Each signatory own current gdp_total at acceptance; annual programme share recalculated from each own GDP / 52 weekly. No French GDP reuse for the recipient.",
  "asset_execution": "Acceptance rechecks ownership, control and capacity for each promised asset on both sides before paying either side. One-time assets/slots share the signed transaction receipt; restoration never repeats them.",
  "partner_name": "United Kingdom",
  "payment_contract": "French and recipient setup charges use separate own-country current GDP bases at acceptance; weekly annual-GDP appropriations use each own current GDP / 52. One atomic once-only transaction, no fixed-price building charge or Treasury-balance gate."
}
```

### Shared Maintenance

`COLDWAR_FRA2_nato_common_maintenance` | (23, 11) | 49 days | government

Turn agreed land-equipment standards into training and support routines within the French forces. The partnership provides experience while France funds its own personnel.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member; has_idea = COLDWAR_FRA2_nato_europe_land_france.
Prerequisites: (nato_europe_land).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "doctrine",
    "category": "land_doctrine",
    "reduction": 0.25,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "army_personnel_cost_multiplier_modifier",
    "value": 0.02
  }
]
```

### Joint Naval Staffs

`COLDWAR_FRA2_nato_europe_staff` | (25, 11) | 49 days | government

Develop French naval doctrine through the agreed European industrial programme. Staff exchanges and technical analysis require a permanent administrative effort.

Requirements: western_conservatism_are_in_power = yes; has_idea = NATO_member; has_idea = COLDWAR_FRA2_nato_europe_sea_france.
Prerequisites: (nato_europe_sea).
Exclusive: None.

```json
[
  {
    "kind": "treasury_gdp",
    "percent": -0.08,
    "gdp_fraction": -0.0008,
    "runtime_share_literal": "-0.00080",
    "base": "gdp_total",
    "payer": "own_country",
    "valuation": "at_payment",
    "once": true
  },
  {
    "kind": "doctrine",
    "category": "naval_doctrine",
    "reduction": 0.5,
    "uses": 1,
    "once": true
  },
  {
    "kind": "modifier",
    "key": "bureaucracy_cost_multiplier_modifier",
    "value": 0.02
  }
]
```
