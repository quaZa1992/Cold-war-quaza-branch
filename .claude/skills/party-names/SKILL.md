---
name: party-names
description: 'Fill or rework a country''s 1970 political party localisation in the MD politics view for the Cold War fork: the 24 subideology name, icon, and description keys as COLDWAR_<TAG>_party_* keys plus IMP_is_1970_scenario hooks placed before the inherited 2000-era ones. Use when asked for party names, subideology localisation, or "political parties for TAG", e.g. "/party-names GRE".'
---

Fill a country's 1970 parties across the 24 subideology slots: loc keys, descriptions,
and the hooks that make them render at the 1970 start, without breaking the inherited
modern labels.

Requested arguments: $ARGUMENTS (one or more TAGs).

Read `.claude/docs/party-loc-reference.md` (slot table, key format, icons, hooks, the
"This fork: 1970 party names" section) and `.claude/docs/coldwar-1970-context.md` first.
`docs/iceland_1970/PARTY_INTEGRATION.md` is the worked example.

At most 5 TAGs per PR. Split larger requests into separate branches and say so up front.

## Defaults

Settled. Do not ask about them.

- No TAG given: ask which country; there is no tracking issue for party batches in this
  fork.
- Branch: `git fetch origin`, then `git switch -c <tag-lower>-1970-parties origin/main`.
- Research, then re-verify: one research agent per tag, then a fresh agent re-verifies
  every party, slot fit, and gate date against sources. Only then present the mapping.
- Style: shape from the upstream `ENG` block (header, `\n\n`, two paragraphs), register
  from `HOL`, both in `MD_politics_view_parties_l_english.yml`. Present tense **as of
  the party's own gate** (1 January 1970 for the starting set). What the party stands
  for, how it governs or campaigns, its Cold War foreign-policy posture (bloc alignment,
  non-alignment, decolonisation), and where its leverage lies. No leader parades,
  chronologies, or founding narratives. 90 to 120 words per `_desc` including the header.
- Identity only: each `_desc` describes the party under its own gate. Never say what it
  later becomes.
- Dates: none before 1970 except a founding year when it explains the party's legal
  status (for example a party banned since 1967). Post-1970 events may carry a year,
  never a day. No election results, percentages, seat counts, or speculation.
- Banned, exiled and underground parties of 1970 (juntas, one-party states, colonial
  administrations) may fill their slot; the description says they are banned or in
  exile.
- Gating: the starting set needs no flag. A later identity change (rename, merger,
  legalisation, ban, split) is gated on a country flag set by an event, a focus or a
  decision, never on a bare date in the hook.
- Icons: a generic sprite means no `_icon` key and no `_icon` hook. Period party logos
  only; never reuse a modern logo for the 1970 party.
- Slot 23: the monarchist party while out of power, and the royal house when
  `check_variable = { ruling_party = 23 }`.
- The slot that rules on 1 January 1970 must match the country's `IMP_1970` starting
  ruling party (`IMP_1970_has_historical_ruling_party`, `IMP_1970_<TAG>_STARTING_PARTY`).
  If it does not, stop and report rather than moving the government.
- PR title: "Add 1970 party localisation for TAG[, TAG]".
- Changelog: one line under Localization (or Content),
  ` - Added historical 1970 party names for: TAG, TAG`. Append the tag to it.

## Steps

1. Inventory what exists:

   ```bash
   grep -n "^ TAG\." localisation/english/MD_politics_view_parties_l_english.yml
   grep -rn "COLDWAR_TAG_party_" localisation/english/
   grep -n "original_tag = TAG" common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt
   grep -n "IMP_1970_TAG_STARTING_PARTY\|original_tag = TAG" common/scripted_localisation/IMP_1970_party_name_scripted_localisation.txt localisation/english/IMP_1970_*_l_english.yml
   grep -n 'name = "GFX_TAG_' interface/*.gfx
   grep -n "party_pop_array\|IMP_1970_profile" "history/countries/TAG - "*.txt
   ```

   Report which slots already have a 1970 key, which only have inherited 2000-era keys,
   the starting ruling party, and which hooks exist.

2. Research the country's real parties around 1970 (and those that appear in the 1970s)
   and map them to slots: native name and transliteration, abbreviation, ideology, legal
   status in 1970, and two or three concrete facts. Use verifiable sources only:
   Wikipedia and its references, parliament or electoral archives, academic party
   histories, reputable news archives. Drop any claim you cannot verify, and leave a
   slot generic when there is no real counterpart. Plan a flag-gated variant for each
   identity change in the 1970s. Then have a fresh agent re-verify the list.

3. Confirm the slot mapping, the slots left generic, and the gated variants before
   writing.

4. Check sprites: tag sprite or generic for each party. Verify each `£name` resolves in
   `interface/`.

5. Write the keys `COLDWAR_TAG_party_<subideology>`, `_desc` and (with a tag sprite)
   `_icon` in `localisation/english/COLDWAR_TAG_party_l_english.yml` (UTF-8 with BOM,
   leading space, ordered by `^N`). Do not edit the inherited `TAG.<subideology>` keys.

6. Wire the hooks in `00_MD_politicsview_scripted_localisation.txt`: for each filled
   slot, insert one clause in `<slot>_L` and `<slot>_L_desc` (and `<slot>_L_icon` only
   where a tag sprite exists), **immediately before** the existing TAG clause in that
   block:

   ```
   text = { trigger = { original_tag = TAG IMP_is_1970_scenario = yes } localization_key = COLDWAR_TAG_party_conservatism }
   ```

   For a gated variant, the flag clause goes first:

   ```
   text = { trigger = { original_tag = TAG IMP_is_1970_scenario = yes has_country_flag = COLDWAR_TAG_<party>_<change> } localization_key = COLDWAR_TAG_party_conservatism_<change> }
   ```

   The flag is set by a focus, decision or event the players can reach. A dated AI
   fallback event (`is_triggered_only`, `fire_only_once`, `original_tag` trigger, no
   picture, one option that sets the flag and runs `update_party_name = yes`) needs a
   `trigger_year_<YYYY>_events` block, which this fork only has for 2001 to 2030; add the
   1970s block in a namespaced effects file and say so in the PR. Its English title and
   description go in the country's `COLDWAR_TAG_*_l_english.yml`.

7. Verify: recheck style against ENG and HOL; grep the new block for anachronisms (any
   year after the gate, modern names); run the static checker on every touched file;
   work the reference doc's checklist; confirm the branch touches at most 5 TAGs. In
   game (not runnable by the agent): open the politics view on 1 January 1970, then fire
   each new event and check the name, description, and icon swap, and confirm a modern
   label never shows at 1970.
