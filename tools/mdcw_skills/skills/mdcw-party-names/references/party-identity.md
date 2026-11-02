# IMPERIA COLD WAR — Party-source and hook checks

Useful live starting points are `common/ideologies/00_ideologies.txt`, country history, political-leader providers, `common/scripted_triggers`, `common/scripted_localisation` and English politics-view localisation. Discover additional 1970 overrides before editing the modern fallback. A dated Cold War selector may shadow a correctly written modern key.

Record each selected party's 1970 existence, identity, legal position, English/native name, abbreviation, real ideological fit and source. A military institution, royal house or employers' organisation can be appropriate when it is actually the country's institutional actor. Say what it is. Missing real counterparts remain generic rather than being fabricated for slot coverage.

For each party trace slot index, popularity, ruling-party gates, leader block, visible party-name getter, description and icon fallback. A displayed party name must be the current required identity rather than a string combining a later party with an arrow. Moving a slot without its leader and focus/event readers can silently change gameplay.

For later identity changes, keep current and future names behind the actual event/flag/date mechanism used by this project. A real rename or merger differs from a party merely being founded. Reuse existing scheduling and guard against a human alternate path being overwritten by historical automation. Preserve the modern bookmark's independent history and fallback.

Use native MD party localisation and exact `*_are_in_power` triggers in visible requirements. Inspect names, descriptions and icons in the politics view at January 1970 and after relevant identity changes when native UI access is available. Static key/hook closure cannot prove a getter actually renders.
