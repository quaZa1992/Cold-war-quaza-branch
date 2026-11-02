---
name: mdcw-national-trees
description: Design, extend, implement, or review national focus trees for Enes's HOI4 Millennium Dawn Cold War mod, using the project's historical, political, reward, and native MD presentation conventions. Use for national focus content, not research trees or unrelated main-Imperia changes.
metadata:
  project: IMPERIA COLD WAR
---

# IMPERIA COLD WAR: National focus authoring

Build a playable national programme for the January 1970 multiplayer roleplay scenario. Follow current MD mechanics and presentation while preserving approved Imperia and Cold War features. A matching name or tooltip is not proof that a reward works.

Read [project-contract.md](references/project-contract.md) for the user's durable preferences and their scope. Read [source-map.md](references/source-map.md) to locate the code and chat evidence. Reconfirm mutable facts in the target checkout; snapshots are not permanent instructions.

For historical start identity, protected-state transitions, empty reward previews, national-spirit artwork, or an economy changing its income base, read [UAE correction lessons](references/uae-1970-lessons.md). These record demonstrated failures and distinguish reusable rules from UAE-specific values.

## Establish the assignment

- Identify country, scenario, existing tree, source generator, requested phase, and any approved design. Distinguish national focus trees from research trees.
- Preserve historical starting leaders and existing election, succession, economic, diplomatic, and party systems unless the task changes them. Add content through those systems.
- For a new tree, prepare the spatial design and effects first. If the user requests a sketch or explicitly reserves approval, keep it outside the loaded mod until approval arrives. When implementation of a concrete design is authorized, proceed without asking for the same permission again. A layout-only fix does not authorize changing rewards or prerequisites.
- Inspect current work and generator ownership before editing shared files. Assign non-overlapping agent work; do not run a broad generator that can overwrite another chat's changes.

## Learn the actual reference grammar

Use the normal main MD 2000-era national trees as references for values, costs, modifiers, reward bundles, native code and presentation. The reference pool includes Russia, Israel, Germany and Turkey, plus other mechanically comparable countries; select the examples that fit the effect being built. Read [russia-2000-presentation.md](references/russia-2000-presentation.md) for the concrete mistakes learned from Iraq and the verified examples. Compare representative descriptions, English localisation and actual reward code when authoring or substantially rewriting content. For numerical calibration, record the source country/focus, amount, unit, cost, duration and relevant gates. Adapt the scale to the target country and 1970 scenario; these are mechanical references, not political or historical templates. The custom Soviet 1970 tree remains an architecture/gameplay reference.

The lesson is to deliver finished MD-quality content: descriptions explain this country's circumstances, institutions, political intent and meaningful tensions; effects clearly show the actual named outcomes, numbers, costs and trade-offs using native MD presentation. Do not publish raw catalogue instructions (such as "Pay for a factory"), generic filler, placeholder summaries, internal bookkeeping essays, or prose substitutes for executable/numeric effects. Merely deleting technical words, lengthening a description, citing a reference tree, or passing a parser is not an editorial/presentation review. Treat concept-catalogue text as a draft even when its mechanics are approved. Read the emitted descriptions and reward lists together before delivery; for substantial new or rewritten content, have an independent agent compare representative examples against main MD. Preserve approved calculations, guarded transactions and the country-specific design.

Read comparable branches in current main MD `00_generic.txt`, `05_russia.txt`, `05_israel.txt`, `05_germany.txt` and `turkey.txt` as relevant, alongside the target country's native tree. An individual task does not require exhaustively reading every tree. Trace their called effects, ideas, dynamic modifiers and UI rather than copying only focus declarations. Project generators are integration examples, not proof that every local line is correct.

The user also selected Claude's implemented Soviet 1970 tree as a preferred project reference for programme depth, thematic reward bundles, leadership variation and integration. Read [soviet-patterns.md](references/soviet-patterns.md) when designing large programmes, leader paths, decisions or cooperative focuses. Adapt its architecture, not Soviet-only institutions, values or focus count.

Record a small reference profile: source/version, focus cost and duration, entry/branch/join coordinates, icon treatment, party gates, reward shapes and units. Sample comparable political, industrial, military and diplomatic focuses. A superpower's factory grant is not automatically a small country's reward budget.

## Design policy choices, not a chain of small gifts

- Research January 1970 institutions, parties, conflicts, economy and constraints. Cite primary historical sources where possible. Separate historical facts, plausible alternate history and balance proposals.
- Build historical and credible alternative routes for relevant parties, outlooks and leaders. Do not fill every MD slot with an implausible country path. Preserve playable continuation for approved alternatives.
- Use MD's exact party/subparty model. A programme becomes available when that party governs; do not require a redundant 'unlock our already-ruling party' focus. Accession focuses are justified when they really change government through the agreed system. Show an unapproved new party as a provisional design; do not invent a live ideology or party-array slot to make it fit.
- Keep all party branches visible and inspectable, including parties outside government, unless the user explicitly requests hiding. Gate focus availability, real completion and programme activation on the exact ruling party; do not use party-dependent `allow_branch` to conceal content.
- For visible party requirements, reuse the existing native MD exact-party `*_are_in_power` trigger and its registered party-name tooltip. For example, `western_liberals_are_in_power` already checks slot 2 and displays `[liberalism_L] is in Power.` Do not replace it with invented labels such as "Governing political current" or a broad outlook/coalition check. Preserve hidden scenario, dated-identity and receipt guards. Programme names should use the actual registered party name, not a present-to-future party label joined by an arrow.
- Give important programmes meaningful outcomes: appropriate buildings, sector productivity/employment, debt or treasury consequences, programme modifiers, research/doctrine rewards, diplomacy or decisions. Avoid PP/stability filler unrelated to the focus's purpose.
- Make both sides of a historically grounded exclusive choice attractive: the player should want both rewards but have a real reason to choose. Give them different substantial outcomes and, where plausible, a modest disadvantage or credible opportunity cost. Strengthen existing forks before multiplying cosmetic exclusions. Exclude competing constitutional terms, scarce funding priorities or military commitments; keep ordinary complementary development shared. A difficult historical situation and its starting penalties remain real; this preference is not a mandate to make every policy harmless.
- Audit impact across a whole compatible route, including its follow-ups, starting spirits, temporary decisions and government gates. Do not sum incompatible parties or add several versions of the same army reform on top of one another. Replace overlapping rewards explicitly. Prefer meaningful assets, limited-use research/doctrine bonuses, training and enacted institutions to repetitive tiny PP/stability changes or bureaucracy-only penalties. Check whether a positive reward is already lost at an existing cap.
- Give important choices enough distinct follow-through to change the programme. Merge accounting/review filler into the reform it serves; avoid stamping every party with the same focus count, doubled fork and ceremonial finale. These are outcome criteria, not a universal minimum bonus, mandatory malus or prescribed number of forks.
- Include relevant starting problems and ways to improve them. Reforms should change an actual persistent system, not just rename a spirit.
- Avoid arbitrary date barriers. Retain dates where historically or mechanically necessary and explain them; a chapter name alone does not justify locking an entire programme until that year.

## Use one reviewable design

Maintain structured design data where a generator exists. Each focus needs an ID, English name/description, group, coordinates/anchor, prerequisite groups, exclusions, availability, cost, executable effects, associated sprites/ideas/events and its MD reference pattern. Mark one-time, temporary, recurring or party-bound effects explicitly.

Produce a full-tree preview with existing neighbours and normal-scale branch views, using the same resolved coordinates, connectors and labels as the proposed code. A focus inspector should expose conditions and exact proposed rewards. Narrative prose belongs in descriptions; normal completion rewards remain in native tooltips.

Effect fields must contain only concrete native costs, signed modifier changes, research/experience, named spirit changes and decision unlocks. Do not append custom explanatory paragraphs about ownership, consent, expiry or bookkeeping. Put necessary context in descriptions or visible requirements. Keep native numeric formatters and standard MD headings; use `unlock_decision_tooltip` for a decision unlock and non-executing native effect previews for recipient-approved rewards. This applies to every focus, decision, event option and preview in the tree.

For every recipient-approved focus offer, always show the complete prospective outcome directly in the focus Effects under a native "If they accept" heading. Show both countries separately with the exact spirit names and all signed spirit modifiers, one-time and recurring costs, assets, research and other rewards. The numbers must remain inspectable before acceptance, while the focus is locked or excluded, and while treaty, party or sanctions conditions are false. A spirit name, event title, decision unlock or link to later details is not a substitute. Keep the real consent and activation guards in execution; use a non-executing preview so displaying the offer never grants rewards or charges money.

Use `$mdcw-tree-layout` for substantial geometry work and `$mdcw-modifier-audit` for mechanics/reference verification when available. They are installed alongside this skill; the requirements below still apply if either is unavailable.

## Project identity and learned delivery contracts

Every new custom code file starts with the exact `IMPERIA COLD WAR` marker in valid comment syntax; required language headers, shebangs and skill frontmatter keep their required positions, with the marker immediately after. Preserve upstream attribution in shared files, identify only the custom integration, and mark custom blocks as well. Update generator templates and output together. Keep scripts UTF-8 without BOM and localization UTF-8 with BOM. Follow the current repository `AGENTS.md`; do not brand immutable snapshots by changing their hashes.

Read [Cuba implementation lessons](references/cuba-implementation-lessons.md) when implementing recipient-consented offers, permanent bilateral spirits, building/fort grants, or event photographs, and before continuing Cuba. It records the user's exact expectations for full native effect previews, matched recipient responses, peace/sanction suspension, one slot per building level, the actual MD event frame, and evidence boundaries. Cuba's 120-focus ceiling, island route and rejected overseas/medical workforce penalties remain scoped examples.

## Implement and prove the integration

For approved-concept implementation, native succession, government-bound programmes or difficult economic starts, read [vietnam-integration.md](references/vietnam-integration.md). It records the Vietnam implementation lessons without turning its roster, reward counts or dates into requirements for other countries.

1. Edit the canonical generator/design and intended outputs. Match nearby MD blocks and scopes. Use searchable `COLDWAR_<TAG>_...` IDs unless an established country namespace exists; preserve existing IDs/save contracts.
2. Trace each promised effect to its provider and consumer. Check amount, scope, timing, stacking, affordability and displayed units. Helper names alone do not establish behaviour.
3. Preserve prerequisite grouping and gameplay choices while positioning: separate `prerequisite` blocks are AND; multiple `focus` entries inside one block are OR. Do not silently convert visible dependencies into invisible eligibility gates just to simplify lines.
4. Implement appropriate removal, replacement or conditional deactivation on government changes and expiration. Distinguish durable national gains from currently active party/leader programmes; preserve earned programme variables if later reactivation is intended. Resynchronization must not replay factories, cash, annexations or research grants.
5. Register English localisation, sprites/textures, ideas/modifiers/events and transitive dependencies. Reuse appropriate art before creating new art. Do not alter global fonts or other trees to accommodate one branch.
6. Delegate a layout review and independent mechanics/reference review for substantial work, using the user's preferred economical model when available. Review emitted code, not only the catalogue. Keep implementation and final review independent where practical.
7. Run applicable checks and visually inspect the faithful preview. Test in HOI4 when available: new 1970 start, hover/tooltips, representative rewards, party change, save/reload, AI and multiplayer responses as relevant. Report unperformed engine checks plainly.

## Deliver

Explain branches/choices added, important effects/costs, files touched, verification and remaining gaps. Separate designed, implemented, statically checked, visually reviewed and tested in HOI4. Disclose deviations from the approved design. Do not claim perfection or working modifiers merely because parsing passed. Skill invocation does not authorize publication or unrelated system changes.
