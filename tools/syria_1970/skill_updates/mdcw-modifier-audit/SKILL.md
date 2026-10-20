---
name: mdcw-modifier-audit
description: Audit modifier and effect mechanics in Millennium Dawn Cold War focus trees, including MD API support, calculation, visibility, stacking, cleanup, references, and 1970-scenario reachability. Use for focused-tree mechanic reviews; exclude general tree drafting and layout work.
---

# MD Cold War focus-tree mechanic audit

Use this skill to review whether a focus-tree reward has the intended, traceable effect in the current Millennium Dawn Cold War codebase. The audit is evidence-led: distinguish what source files prove from what requires an in-game test. Do not invent modifier keys, formulas, units, stacking rules, balance targets, or engine guarantees. Do not implement changes or add mechanics unless the user explicitly asks for implementation.

Start by locating the active MD Cold War repository and the installed MD source version. Treat the code anchors in the references as search starting points, not frozen truth; confirm their current contents and line numbers before relying on them. For a normal review:

An explicitly supplied fixture or review copy takes precedence over the live mod as the target. Missing external providers or consumers in an incomplete input are unresolved, not confirmed defects, unless the supplied provider universe is known to be complete. Do not broaden a bounded audit without need.

1. Trace each relevant focus from `available` and its prerequisite graph through `completion_reward`, referenced scripted effects/triggers, event options, ideas or dynamic modifiers, and their cleanup paths.
2. For every modifier or effect, establish its native MD form and scope. Trace a modifier into the actual system that reads or applies it; a matching word in a file, an icon, or an effect tooltip alone does not prove behavior.
3. Compare visible tooltips with executed effects. Verify values, units, duration, repeated grants, simultaneous sources, and intended removal, replacement or conditional deactivation on government/office changes. Separate permanent national gains from active leadership programmes.
4. Follow references transitively: event IDs and options, ideas, scripted effects and triggers, focus sprites and texture files, English localization keys, equipment types/design bonuses, research categories, and doctrine-cost categories.
5. Check that the route is reachable in the 1970 scenario from its real start setup, accounting for tree loading, starting government/party, date and country gates, event decisions, grouped prerequisites, exclusions and later-year formations. Multiple prerequisite blocks are AND; multiple focus fields inside a single block are OR.
6. Report concrete findings with source paths and current line anchors, the source evidence, the likely player-visible consequence, and any remaining runtime uncertainty. Separate confirmed defects from questions that need a live game check.

Read [references/modifier-effect-audit.md](references/modifier-effect-audit.md) when verifying modifier keys, formulas, units, tooltips, stacking, dynamic ideas, equipment, research, or doctrine effects. Read [references/focus-graph-and-scenario.md](references/focus-graph-and-scenario.md) when auditing transitive references, party-change cleanup, or 1970-scenario reachability.

For generated trees, trace the reviewed focuses and their applicable overrides through staged output into loaded files. Keep coverage within the requested scope unless findings justify expanding it. The references contain Soviet patterns for dynamic rewards, programme ownership, recipient-controlled agreements and joint-focus scopes, not a certificate that the entire Soviet tree passed a game test.

For unavailable or unaffordable focuses, audit the displayed reward independently of the guarded payout. In-game screenshots and parser errors take precedence over an earlier static PASS. See the presentation and parser checks in [references/modifier-effect-audit.md](references/modifier-effect-audit.md).

Static parsers, source searches, and local validators can establish source consistency and graph properties; they do not prove that HOI4 loads the tree, renders the exact tooltip, evaluates every scope as intended, or preserves behavior in a save. State those limits plainly. Do not convert audit work into a balance redesign or broad code cleanup.
