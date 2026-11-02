---
name: mdcw-localisation
description: Write or review English IMPERIA COLD WAR localisation, dynamic text, numeric effect wording and accurate removal conditions for starting national spirits. Use for localisation and player-facing prose, including spirit-removal descriptions, rather than changing mechanics.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — English localisation and spirit conditions

Read `AGENTS.md` and [references/text-and-spirits.md](references/text-and-spirits.md). Resolve existing localisation ownership and generators. Preserve the project's separate country/mechanic files; do not consolidate everything into modern MD's `MD_focus_TAG` convention just to follow upstream.

Write concise English suitable for Cold War multiplayer RP. Names and descriptions explain the actual political and institutional situation. New text uses no en or em dashes. Keep implementation jargon, debug explanations, receipt bookkeeping and code workflows out of player prose.

Effects show real native rewards, costs, signed modifier changes, named spirits and unlocks. Descriptions provide necessary context. Use native numeric formatting and standard headings; never replace effect previews with explanatory custom paragraphs. Recipient-approved focuses must expose both countries' complete numeric prospective terms even while locked, unsigned or suspended, without executing them.

Preserve dynamic tokens byte-for-byte during prose-only editing: colour pairs, icons, literal `\n`, getters, variable formatters and scripted requirements. Verify exact getter spelling and scope in installed documentation. A syntactically valid token may still render blank.

For starting-spirit removal text, trace all actual additions, tiers, swaps, improvements, cancellations, weekly updates and removal paths from the real 1970 start. Explain only verified player-accessible changes in the description. Exclude permanent and hidden systems that have no such removal. Do not promise expiry for standing Cuban bilateral agreements or confuse suspension with termination. Repairing a description does not authorize changing its mechanic.

Save localisation as UTF-8 with BOM, `l_english:` first, then the exact project marker, then correctly indented keys. Preserve upstream credits, existing keys and other languages. Verify duplicate keys, references, punctuation, costs/units and actual runtime correspondence. Inspect native hovers or politics views where available, and state when rendering remains unverified.

Source and adaptation: [references/source.md](references/source.md).
