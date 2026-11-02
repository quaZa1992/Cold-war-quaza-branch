IMPERIA COLD WAR

# France: native cost-row presentation

User instruction, 30 October 2026: "sowas finde ich unschön. mach das wie MD es macht". The screenshot showed consecutive custom tooltip fragments concatenated into a paragraph after the native treasury cost, followed immediately by the next reward.

The bilateral generator now keeps MD's native `modify_treasury_effect` setup row. It removes the duplicate "Setup expenditure" explanation and replaces the raw weekly decimal and annual-GDP division formula with a single numeric Additional Expenses row. Every row explicitly ends in a localisation line break, keeping the following spirit or building effect separate.

## Native reference and unit adaptation

Current source donor: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`.

- `common/decisions/Cartel Decisions.txt`, `anti_cartel_propaganda_decision`: computes the expense quote in a temporary variable and displays `additional_expense_rate_percent_tt` before its hidden runtime effects.
- `localisation/english/MD_money_l_english.yml`, `additional_expense_rate_percent_tt`: uses the Additional Expenses heading and a red native numeric monetary formatter, `|R3`.
- `localisation/english/MD_tooltips_l_english.yml`, `modify_treasury_effect_tt`: the existing national flag, country adjective and signed Treasury row. This shared native text is unchanged.

France's small programme quotes are shown in millions per week with `|R2`, rather than billions with five decimal places. This is a display-only conversion by 1,000. A precision of 0.01 million equals 0.00001 billion, preserving the previous displayed monetary precision. The expense-increase wording, colour treatment and numeric formatter follow MD; the explicit weekly unit and million denomination fit this programme's amounts.

Both participants of the original 35 agreements retain separate prospective setup costs, recurring costs, signed spirit modifiers, buildings, slots and finite rewards. Their payer GDP shares, division by 52, charges and receipts are unchanged. The later authorized foreign-policy extension brings the same presentation contract to all 67 agreements, including matched fee/aid streams. Quotes remain inside native `effect_tooltip`, so showing them cannot charge money or award assets.

`COST_DISPLAY_BASELINE.json` records the pre-repair hashes of every non-preview diplomacy provider. The original repair preserved all 144. After the authorized foreign-policy extension, `check_cost_display.py` still checks 141 unchanged original providers and explicitly permits the three extended aggregate/lifecycle providers. It checks all 134 country cost rows, their GDP calculations and display conversion, line breaks and 201 non-executing call sites. `COST_DISPLAY_CHECKS.json` records the current result. This source check does not establish live tooltip rendering.
