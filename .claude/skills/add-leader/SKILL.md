---
name: add-leader
description: 'Scaffold 1970-era generals, field marshals, and admirals for a country using the MD count formulas and region skill ranges, writing character and recruit_character entries for the Cold War 1970 start. Use when asked to add leaders, generals, or admirals for a TAG, e.g. "/add-leader EGY".'
---

**Syntax:** `/add-leader [TAG]`

Read `.claude/docs/coldwar-1970-context.md` first. Count formulas, skill ranges, and
portrait sizes are in `.claude/docs/content-guidelines.md`.

## 1. Gather country data

- `history/countries/TAG - *.txt`: the `1970.1.1` block only. Ignore the dormant
  `2000.1.1` block. Note major-power status and 1970 alliance membership (NATO, Warsaw
  Pact, other `IMP_1970` alliance templates).
- Force size: 1970 starting OOBs are currently empty placeholders, so do not count
  `division = { }` blocks. Use the planned 1970 order of battle from
  `docs/<country>_1970*/` or `tools/armed_forces_1970/data`. If neither exists, ask for
  the intended force size; never infer zero units.
- Existing characters: `common/characters/TAG.txt` (inherited, mostly 2000-era people)
  and any `common/characters/COLDWAR_TAG_1970_*characters.txt`. Avoid duplicates and do
  not recruit an inherited character at 1970 who was not an officer of that rank then.

## 2. Counts and skills

- Apply the formulas. At least one general. No navy means no admirals.
- One bookmark only (1970). Characters who rise later in the period are added through an
  event or decision that recruits them on a real date, not in the 1970 block.
- Take the skill level from the region range. A historically notable commander of the
  period may exceed it.
- A general at level X gets `(X - 1) * 3 + 4` points across `attack_skill`,
  `defense_skill`, `planning_skill`, `logistics_skill`, and `maneuvering_skill`, each at
  least 1.
- Only real officers who held command around 1970. Verify name spelling, rank and
  service dates from a source you can cite in the report.

## 3. Character file

Put new 1970 characters in `common/characters/COLDWAR_TAG_1970_characters.txt` (create
it if missing; `COLDWAR_GRE_1970_regional_characters.txt` is a working example). Do not
rewrite the inherited `TAG.txt`.

```
characters = {

	COLDWAR_TAG_general_firstname_lastname = {
		name = "Firstname Lastname"
		portraits = {
			army = {
				large = "GFX_portrait_COLDWAR_TAG_firstname_lastname_large"
				small = "GFX_portrait_COLDWAR_TAG_firstname_lastname_small"
			}
		}
		field_marshal = {           # or general = { }
			traits = { trait_name }
			skill = X
			attack_skill = N
			defense_skill = N
			planning_skill = N
			logistics_skill = N
			maneuvering_skill = N
			legacy_id = -1
		}
		advisor = {                 # optional, for high command and branch chiefs
			slot = army_chief       # or high_command, navy_chief, air_chief
			idea_token = COLDWAR_TAG_general_firstname_lastname
			ledger = army           # only for the high_command slot
			allowed = { original_tag = TAG }
			traits = { army_chief_of_defence_1 }
			cost = 100
			ai_will_do = { factor = 1 }
		}
	}

}
```

- The `allowed` block uses `original_tag`, never `tag`.
- The token suffix is `firstname_lastname`, with no initials or titles.
- Verify every trait name exists in this tree (`common/unit_leader/`, `common/country_leader/`).
- Portraits go in `gfx/leaders/TAG/`. List any that do not exist yet in the report;
  use an existing generic period portrait meanwhile and say which.
- Define an air chief even with no air force. Players cannot generate one mid-game.

## 4. Recruit entries

In `history/countries/TAG - *.txt`, inside the `1970.1.1` block's
`date < 1985.1.1` guard:

```
recruit_character = COLDWAR_TAG_general_firstname_lastname
```

## 5. Check

Run the static checker on every touched file (`.claude/docs/validation-pipeline.md`)
and grep that each `recruit_character` id is defined once.

## 6. Report

General, field marshal, and admiral counts with the formula breakdown and where the
force size came from, each character's skill, traits and source, the files changed, the
portraits still needed, and "not tested in game".
