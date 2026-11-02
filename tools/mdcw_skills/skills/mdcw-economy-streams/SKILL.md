---
name: mdcw-economy-streams
description: Integrate or audit recurring income, expenses, programme funding, and associated tooltips in the IMPERIA COLD WAR MD economy. Use for money-system streams and budget transactions, rather than general historical currency research.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Weekly fiscal streams

Read `AGENTS.md` and [references/fiscal-contract.md](references/fiscal-contract.md). Resolve the requested amount, source unit, payer, recipient, activation and suspension conditions from the request and current code before asking for missing information.

Trace `calculate_additional_income_rate`, `calculate_additional_expense_rate`, their callers, money-tooltip ideas, relevant modifiers and treasury application in the loaded `00_money_system.txt`. Confirm variable names, signs and cadence at the consumer. A similarly named custom modifier is insufficient evidence that money changes.

Keep setup payments separate from recurring weekly flows. Convert annual or monthly source budgets explicitly using the convention actually used by the project. Store at most five fractional digits in scripted budget literals, record rounding, and verify that small payments do not round to zero. Do not rebalance approved amounts while repairing integration.

Initialize each stream's contribution to zero before conditional accumulation. Confirm repeated recalculation is idempotent, deactivation clears stale values, same-country wrappers are not duplicated, and each stream enters the final total exactly once. Preserve fiscal refresh order so calculated revenue reaches the treasury in the intended period.

Use current native monetary effects and numeric formatters. Tooltip activation must match runtime activation; granting a display idea alone must not create an uncharged programme. Show actual signed costs and rewards, including both countries' prospective terms for recipient-approved content. Previewing must never transfer money or set receipts.

Patch the owning generator and emitted files together. Preserve the native money file's UTF-8 without BOM, upstream notices and marked custom blocks. Test inactive, active, suspended, restored, repeated and deficit cases, plus the relevant weekly boundary. Identify source/model tests separately from native economy observations and live MP tests.

Source and adaptation: [references/source.md](references/source.md).
