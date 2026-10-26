---
name: additional-income
description: 'Wire a country-specific income or expense stream into the MD money system for the Cold War 1970 fork: calculation block, hidden tooltip idea, English loc key, and granting effect. Use when asked to add an income or expense stream, e.g. "/additional-income ICE fishing_licences income".'
---

Arguments: $ARGUMENTS, as `TAG stream_name [income|expense]`. Ask for anything missing.
Also ask what activates the stream (focus, decision, idea, flag, agreement), whether it
is GDP-scaled or flat, its display name, and which focus, decision, or event grants it.

Read `.claude/docs/coldwar-1970-context.md` first. The money system is inherited from
MD 2.0.2; confirm each hook below exists here before using it. For working examples,
grep `calculate_additional_income_rate` in `common/scripted_effects/`.

A stream needs four pieces. The variable name must match across all of them. Name it
`COLDWAR_TAG_stream_name` for new 1970 work.

## 1. Calculation

In `common/scripted_effects/00_money_system.txt`, inside
`calculate_additional_income_rate` or `calculate_additional_expense_rate`. This shared
file is the only hook, so keep the insertion minimal:

```
if = {
    limit = { original_tag = TAG }
    if = {
        limit = { has_completed_focus = COLDWAR_TAG_focus_name }
        set_variable = { COLDWAR_TAG_stream_name_income = gdp_total }
        multiply_variable = { COLDWAR_TAG_stream_name_income = 0.003 }
        add_to_variable = { additional_income_rate = COLDWAR_TAG_stream_name_income }
    }
}
```

- Income adds to `additional_income_rate`. Expense uses a `_expense` variable and adds
  to `additional_expenses_rate`.
- Each country has one `original_tag` wrapper per effect. If one exists, nest the new
  inner `if` in it. Never add a second wrapper.
- The value is GDP-scaled as above, or flat: `set_variable = { COLDWAR_TAG_x_income = 0.500 }`.
  Size it against the country's 1970 GDP, not the 2000 economy.
- A stream paid by one country to another (aid, rent, licences) needs both sides: income
  on the receiver, expense on the payer, ended together. Between human countries it
  must come from an accepted agreement with an end or cancel path (`hoi4-rp-diplomacy`
  in `.agents/skills/`).

## 2. Hidden idea

In the country's 1970 ideas file (`common/ideas/COLDWAR_TAG_*.txt`, or create one), in
its `hidden_ideas` block:

```
hidden_ideas = {
    COLDWAR_TAG_stream_name_money = {
        allowed_civil_war = { always = yes }
        modifier = {
            custom_modifier_tooltip = additional_income_COLDWAR_TAG_stream_name_TT
        }
    }
}
```

Use `additional_expense_COLDWAR_TAG_stream_name_TT` for an expense. Do not add
`allowed = { always = no }` or an empty `on_add`.

## 3. Localisation

In the country's `localisation/english/COLDWAR_TAG_<area>_l_english.yml` (UTF-8 BOM),
not in the inherited `MD_money_l_english.yml`:

```
 additional_income_COLDWAR_TAG_stream_name_TT: "$$[?COLDWAR_TAG_stream_name_income|+3] from §YDisplay Name§!\n"
 additional_expense_COLDWAR_TAG_stream_name_TT: "$$[?COLDWAR_TAG_stream_name_expense|-3] from §YDisplay Name§!\n"
```

`|+3` formats income and `|-3` formats an expense. Keep the trailing `\n`.

## 4. Grant the idea

In the effect that unlocks the stream:

```
add_ideas = COLDWAR_TAG_stream_name_money
```

Add `remove_ideas = COLDWAR_TAG_stream_name_money` wherever the stream should stop, and
reset the variable there too.

## Report

Summarize what was added, run the static checker on the touched files, and remind the
user to check in game that the tooltip appears, the value updates, and (for a two-sided
stream) both clients show matching amounts.
