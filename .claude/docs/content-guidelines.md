# Content Guidelines

Quality checklist for new content in the 1970 Cold War RP fork. Upstream MD's full
guides (content review guide, new general guidelines) are online only; see
`coldwar-1970-context.md`. Where they assume a 2000 start or single-player balance, this
file and `AGENTS.md` win.

## Economic

- Buildings in effects cost money. Use the scripted building effects, which include the
  building slot.
- Trade opinion or a budget law change alone is filler. Pair it with another effect.
- A country tree should meet or exceed the 1970 generic tree's focus count
  (`common/national_focus/mdcw_1970_generic_focus.txt`). Count it before merging.
- Starting factories and GDP match the 1970 economy set by the history block and
  `IMP_1970_gdp_scripted_effects.txt`. Do not change them as part of content work.
- GDP per building and resource comes only from the `@gdp_*` constants in
  `common/scripted_effects/00_money_system.txt`.

## Political

- Parties founded after 1 January 1970 stay hidden until an event or trigger creates
  them.
- Each leader has at least 2 traits, at least 1 with an effect.
- Content is politically neutral and objective.
- Every party has a description and an icon.
- Permanent effects on another nation come from an event or proposal, so the target has
  a choice. Between human-run countries, no annexation, government change, war or
  irreversible loss without an explicit consent path or a documented house rule.
- No free cores. Require 80% compliance or an integration mechanic.
- Aim for 10 to 15 flavor events per country.

## Visual

- Every focus has an icon and `search_filters`.
- Art and wording fit 1970: no later equipment, logos, parties or slang.
- Use tooltips for event outcomes triggered from focuses.
- At most one meme GFX per content set.
- No unlocalised strings. A focus description is not blank and does not repeat the name.
- Starting national spirits have descriptions. A removable one says how.

## AI

- AI is supporting cast. Add game rules for AI customisation and AI logic that prevents
  self-destructive choices, and keep the same rules for AI and humans.
- Events that ask another country to respond give a human time to answer: a deadline in
  game days, a visible default on expiry, and no spam.
- Do not use `add_ai_strategy` in effects.
- Events that target another nation weigh the AI by opinion or influence.
- The AI must be able to use any custom GUI.

## Code

- Log every effect. Give every focus `ai_will_do`.
- No empty `allowed`, `available`, `cancel`, or `bypass` blocks.
- Use `relative_position_id` in focus trees.
- Tags are capitalised in script ids (`SPR_focus_name_here`).
- A focus that spends treasury takes the bankruptcy guard in `search-filters.md`.

## Balance

- No path, idea, or option is weaker than its alternative in every dimension. Each
  choice has a distinct advantage and a distinct drawback.
- Buff or remove a strictly dominated option.
- Currency and alliance transitions never feel like a downgrade.
- Test: if a player could pick the same option every campaign with no trade-off, it is
  not yet a real choice. `cfa_franc_2` against `the_eco` is a pair done well.

## Variety

A tree can be balanced and still formulaic. Compare a new tree against the finished 1970
trees (`COLDWAR_GER_1970_focus.txt`, `COLDWAR_ICE_1970_focus.txt`,
`COLDWAR_SYR_1970_focus.txt`).

- A variable or dynamic-modifier bump is fine as seasoning on a real reward. Flag a
  focus whose whole reward is a log, a tooltip, and `add_to_variable`. More than about
  20% bump-only focuses is too thin.
- No `completion_reward` or `ai_will_do` block repeats verbatim more than about 3 times.
- Every `mutually_exclusive` fork differs in reward kind, not just magnitude.
- At least 4 reward categories across the tree: dynamic modifier, timed idea with
  `swap_ideas`, treasury, building or resource, interest-group opinion, event with a
  choice, bespoke mechanic, decision-category unlock, army or tech unlock.
- At least one bespoke mechanic or idea family the tree alone owns.
- Capstone focuses deliver a new reward kind, not a bigger number.
- Political forks differ mechanically, not only in which popularity ticks up.
  `generic`-named political focus ids are a red flag.
- About one event tie-in per 8 focuses for narrative trees.

## Miscellaneous

- Do not add nations to the bookmarks screen. Leads do that after merge.
- Add the `Changelog.txt` entry before review.
- Drop cosmetic tags that no longer apply.
- A new tag needs an OOB (or the empty 1970 placeholder while forces are deferred), name
  lists, political structure, starting laws, and a starting leader. Name lists:
  `namelist-reference.md`.

## Generals and admirals

- Generals: `ROUND(units / 15) + 1 + IsMajor + IsInFaction + IsNATO`. While 1970
  starting forces are deferred, take `units` from the planned 1970 order of battle
  (design docs or `tools/armed_forces_1970/data`), not the empty OOB, and say so.
  `IsInFaction`/`IsNATO` mean NATO or Warsaw Pact membership in 1970.
- Field marshals: `ROUND(generals / 3)`. Admirals: `ROUND(ships / 15)`.
- Skill level by region: 1-2 civil war factions, 2-3 Africa, 3-4 Middle East and Asia,
  4-5 Eastern Europe and South America, 5-6 Western countries.
- Skill points: `(level - 1) * 3 + 4`.
- Portraits: large 156x210, small 38x51.
- Always include army, navy, and air chiefs, even without an air force.
