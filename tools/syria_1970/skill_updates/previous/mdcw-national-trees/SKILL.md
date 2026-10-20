---
name: mdcw-national-trees
description: Design, extend, implement, or review national focus trees for the HOI4 Millennium Dawn Cold War mod, using the project's historical, political, reward, and native MD presentation conventions. Use for national focus content, not research trees or unrelated main-Imperia changes.
---

# MD Cold War national trees

Build a playable national programme for the January 1970 multiplayer roleplay scenario. Follow current MD mechanics and presentation while preserving approved Imperia and Cold War features. A matching name or tooltip is not proof that a reward works.

Read [project-contract.md](references/project-contract.md) for the user's durable preferences and their scope. Read [source-map.md](references/source-map.md) to locate the code and chat evidence. Reconfirm mutable facts in the target checkout; snapshots are not permanent instructions.

## Establish the assignment

- Identify country, scenario, existing tree, source generator, requested phase, and any approved design. Distinguish national focus trees from research trees.
- Preserve historical starting leaders and existing election, succession, economic, diplomatic, and party systems unless the task changes them. Add content through those systems.
- For a new tree, prepare the spatial design and effects first. If the user requests a sketch or explicitly reserves approval, keep it outside the loaded mod until approval arrives. When implementation of a concrete design is authorized, proceed without asking for the same permission again. A layout-only fix does not authorize changing rewards or prerequisites.
- Inspect current work and generator ownership before editing shared files. Assign non-overlapping agent work; do not run a broad generator that can overwrite another chat's changes.

## Learn the actual reference grammar

Read representative branches in current main MD `00_generic.txt` and `05_russia.txt`, plus the country's native tree and applicable Germany party branches. Trace their called effects, ideas, dynamic modifiers and UI rather than copying only focus declarations. Project generators are integration examples, not proof that every local line is correct.

The user also selected Claude's implemented Soviet 1970 tree as a preferred project reference for programme depth, thematic reward bundles, leadership variation and integration. Read [soviet-patterns.md](references/soviet-patterns.md) when designing large programmes, leader paths, decisions or cooperative focuses. Adapt its architecture, not Soviet-only institutions, values or focus count.

Record a small reference profile: source/version, focus cost and duration, entry/branch/join coordinates, icon treatment, party gates, reward shapes and units. Sample comparable political, industrial, military and diplomatic focuses. A superpower's factory grant is not automatically a small country's reward budget.

## Design policy choices, not a chain of small gifts

- Research January 1970 institutions, parties, conflicts, economy and constraints. Cite primary historical sources where possible. Separate historical facts, plausible alternate history and balance proposals.
- Build historical and credible alternative routes for relevant parties, outlooks and leaders. Do not fill every MD slot with an implausible country path. Preserve playable continuation for approved alternatives.
- Use MD's exact party/subparty model. A programme becomes available when that party governs; do not require a redundant 'unlock our already-ruling party' focus. Accession focuses are justified when they really change government through the agreed system. Show an unapproved new party as a provisional design; do not invent a live ideology or party-array slot to make it fit.
- Give important programmes meaningful outcomes: appropriate buildings, sector productivity/employment, debt or treasury consequences, programme modifiers, research/doctrine rewards, diplomacy or decisions. Avoid PP/stability filler unrelated to the focus's purpose.
- Make choices distinct, with credible benefits, costs, risks and opportunity costs. Do not force a malus onto every focus or offer one universally superior policy behind cosmetic alternatives.
- Include relevant starting problems and ways to improve them. Reforms should change an actual persistent system, not just rename a spirit.
- Avoid arbitrary date barriers. Retain dates where historically or mechanically necessary and explain them; a chapter name alone does not justify locking an entire programme until that year.

## Use one reviewable design

Maintain structured design data where a generator exists. Each focus needs an ID, English name/description, group, coordinates/anchor, prerequisite groups, exclusions, availability, cost, executable effects, associated sprites/ideas/events and its MD reference pattern. Mark one-time, temporary, recurring or party-bound effects explicitly.

Produce a full-tree preview with existing neighbours and normal-scale branch views, using the same resolved coordinates, connectors and labels as the proposed code. A focus inspector should expose conditions and exact proposed rewards. Narrative prose belongs in descriptions; normal completion rewards remain in native tooltips.

Use `$mdcw-tree-layout` for substantial geometry work and `$mdcw-modifier-audit` for mechanics/reference verification when available. They are installed alongside this skill; the requirements below still apply if either is unavailable.

## Implement and prove the integration

1. Edit the canonical generator/design and intended outputs. Match nearby MD blocks and scopes. Use searchable `COLDWAR_<TAG>_...` IDs unless an established country namespace exists; preserve existing IDs/save contracts.
2. Trace each promised effect to its provider and consumer. Check amount, scope, timing, stacking, affordability and displayed units. Helper names alone do not establish behaviour.
3. Preserve prerequisite grouping and gameplay choices while positioning: separate `prerequisite` blocks are AND; multiple `focus` entries inside one block are OR. Do not silently convert visible dependencies into invisible eligibility gates just to simplify lines.
4. Implement appropriate removal, replacement or conditional deactivation on government changes and expiration. Distinguish durable national gains from currently active party/leader programmes; preserve earned programme variables if later reactivation is intended. Resynchronization must not replay factories, cash, annexations or research grants.
5. Register English localisation, sprites/textures, ideas/modifiers/events and transitive dependencies. Reuse appropriate art before creating new art. Do not alter global fonts or other trees to accommodate one branch.
6. Delegate a layout review and independent mechanics/reference review for substantial work, using the user's preferred economical model when available. Review emitted code, not only the catalogue. Keep implementation and final review independent where practical.
7. Run applicable checks and visually inspect the faithful preview. Test in HOI4 when available: new 1970 start, hover/tooltips, representative rewards, party change, save/reload, AI and multiplayer responses as relevant. Report unperformed engine checks plainly.

## Deliver

Explain branches/choices added, important effects/costs, files touched, verification and remaining gaps. Separate designed, implemented, statically checked, visually reviewed and tested in HOI4. Disclose deviations from the approved design. Do not claim perfection or working modifiers merely because parsing passed. Skill invocation does not authorize publication or unrelated system changes.
