-- IMPERIA COLD WAR: Project-specific integration; preserve existing author credits.
-- Cold War has one playable bookmark: 1 January 1970.
NDefines.NGame.START_DATE = "1970.1.1.12"

-- IMPERIA COLD WAR 23.11.2026: cap the research time banked by idle research slots (playtest 1: "Days saved" grew every day
-- while a slot stood empty, until Site Planning needed 1 day). Vanilla value, now set explicitly so nothing can raise it.
NDefines.NTechnology.BASE_RESEARCH_POINTS_SAVED = 30.0
