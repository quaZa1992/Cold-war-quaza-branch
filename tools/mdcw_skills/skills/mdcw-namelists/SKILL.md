---
name: mdcw-namelists
description: Add or repair division, ship, design and air-wing name lists for IMPERIA COLD WAR countries and their 1970 OOBs. Use for unit naming and list wiring, not equipment balance or military commanders.
metadata:
  project: IMPERIA COLD WAR
license: CC-BY-SA-4.0
---
# IMPERIA COLD WAR — Unit and formation names

Read `AGENTS.md`. Resolve the native tag, 1970 identity, loaded OOB, owned coast, service branches and existing name-list providers. Append or repair within the established structure; do not replace a populated list merely because a template uses another filename.

Research period-appropriate formation and ship names. Use actual service traditions and distinguish historically fielded formations from plausible generated names. Do not import later ship classes, renamed services, postcolonial identities or squadrons into the starting OOB without evidence.

New player-facing categories, explanatory text and generic localisation are English. Proper unit and ship names may retain a verified historical name; if the requested naming-language policy is unclear and material, resolve it before producing an entire new-language naming set. Do not create translations of game descriptions under this skill.

Inspect live schemas under `common/units/names_divisions`, `names_ships`, `names`, the country OOB and relevant English keys. Use current equipment archetypes and existing generic patterns rather than copying a modern MD hull catalogue. Landlocked countries do not require a ship-name file.

Wire `division_names_group` and ordered starting names only for the actual relevant templates and units. Preserve OOB equipment, deployment and balance. Check group references, ordered-key behavior, duplicates, class/archetype names, fallback keys and carrier variants against the current engine and MD examples.

Keep project markers, original credits and UTF-8 without BOM in script files; use BOM only for localisation. Record the sources and which names are provisional. Report covered groups and unresolved references, separating static closure from in-game automatic naming behavior. Do not create a navy or change templates simply to fill every upstream group.

Source and adaptation: [references/source.md](references/source.md).
