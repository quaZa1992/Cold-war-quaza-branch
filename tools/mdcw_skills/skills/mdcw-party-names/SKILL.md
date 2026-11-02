---
name: mdcw-party-names
description: Research and wire historically appropriate January 1970 political party names, descriptions, icons and dated identity changes in IMPERIA COLD WAR's native MD party slots. Use for party localisation and slot alignment, not automatic government redesign.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Party identity and native hooks

Read `AGENTS.md` and [references/party-identity.md](references/party-identity.md). Resolve the requested country and real tag from context. Do not choose a country from upstream issue #3895 or a modern party checklist.

Research the parties and institutions that actually existed on 1 January 1970. Record native names, English names, abbreviations, position, legal status, office and sources. Separate later historical identity changes and approved alternatives. Leave unsupported MD slots generic instead of inventing Salafi, Shia or other country-inappropriate paths.

Read the current ideology definitions, `party_pop_array`, `ruling_party`, exact `*_are_in_power` triggers, political leader arrays and existing party-name hooks. Verify the current slot ordering and case, rather than treating upstream's 24-slot table as immutable. Moving a party requires tracing all slot-index and trigger consumers; a localisation request alone does not authorize that gameplay change.

Write concise factual English descriptions about the party under its actual identity gate. Relevant pre-2000 dates are valid for this scenario. Do not apply upstream's ban on twentieth-century dates, fixed word count or modern 2000-2025 research window. Preserve historically meaningful native proper names without generating unrelated translations.

Wire names and descriptions through actual scripted-localisation selectors, including current Cold War/date overrides. A standalone `TAG.subideology` key is not proof that the politics screen uses it. Add icon-specific keys/hooks only for real registered art; preserve verified generic fallbacks. Keep all identity variants consistent across name, description and icon.

Use existing dated events and party update mechanisms for real renames, mergers or splits. Reuse native exact-party requirements in focuses, keep branches visible, and avoid present-to-future arrow labels. Preserve other bookmarks and do not make historical transitions unconditional on a human player unless authorized by the design.

Verify start identity, flag/date transitions, leader alignment, all hook keys and sprite closure. Describe native politics-screen checks separately from static evidence. Patch relevant generators along with emitted files.

Source and adaptation: [references/source.md](references/source.md).
