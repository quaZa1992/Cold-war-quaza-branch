# Write templates

Every artefact of a country AI path pass, verbatim. Copy from here — **do not open another country's
focus tree to learn a shape**.

Substitute `DEN` / `Denmark` / the path names. Tabs for indentation. The shapes come from
upstream MD; in this fork they go into the 1970 files named below each heading, and
every id for new 1970 work keeps the `COLDWAR_TAG_` namespace except the rule's own
`TAG_*_FOCUS_PATH` flags.

## 1. Game rule — `common/game_rules/COLDWAR_DEN_1970_rules.txt`

The shared `00_game_rules.txt` carries the modern MD rules for the 2000 trees. A 1970
rule gets its own namespaced file and the id `COLDWAR_DEN_1970_ai_behavior`.

```
COLDWAR_DEN_1970_ai_behavior = {
	name = "COLDWAR_DEN_1970_AI_BEHAVIOR"
	group = "RULE_GROUP_AI_BEHAVIOR"
	option = {
		name = HISTORICAL
		text = "RULE_OPTION_DEN_HISTORICAL"
		desc = "RULE_OPTION_DEN_HISTORICAL_DESC"
	}
	option = {
		name = EUROPEAN_UNION
		text = "RULE_OPTION_DEN_EUROPEAN_UNION"
		desc = "RULE_OPTION_DEN_EUROPEAN_UNION_DESC"
	}
	option = {
		name = RANDOM_PATH
		text = "RULE_OPTION_MD_RANDOM_PATH"
		desc = "RULE_OPTION_MD_RANDOM_PATH_DESC"
	}
	default = {
		name = NO_PATH
		text = "RULE_OPTION_MD_NO_PATH"
		desc = "RULE_OPTION_MD_NO_PATH_DESC"
	}
}
```

`NO_PATH` is the `default = { }` block and stays last — a fresh game leaves the AI unscripted unless
the player picks a path. `HISTORICAL` is a plain `option` and comes first, with one `option` per
alt-history path between it and `RANDOM_PATH`. No `DEFAULT`. Option names are unprefixed
(`EUROPEAN_UNION`, not `DEN_EUROPEAN_UNION`) and never contain "random". (The example paths are
upstream's; a 1970 Denmark would offer 1970s choices.) A country sub-rule goes in the same file
directly after the main rule, with no `icon`.

## 2. Localisation — `localisation/english/COLDWAR_DEN_<area>_l_english.yml`

Put the rule's keys in the country's namespaced 1970 loc file (UTF-8 BOM), not in the inherited
`MD_game_rules_l_english.yml`. The shared `RULE_OPTION_MD_RANDOM_PATH` / `RULE_OPTION_MD_NO_PATH`
keys already exist there and are reused.

The historical option's displayed text is literally `"Historical"`. Its `_desc` carries the
country-specific history. Never an evocative title, never `"Default"`, `"Historic"` or
`"Historical AI"` — those are pre-standard spellings still in the file.

```
 COLDWAR_DEN_1970_AI_BEHAVIOR: "@DEN Denmark"
 RULE_OPTION_DEN_HISTORICAL: "Historical"
 RULE_OPTION_DEN_HISTORICAL_DESC: "..."
 RULE_OPTION_DEN_EUROPEAN_UNION: "Into the Union"
 RULE_OPTION_DEN_EUROPEAN_UNION_DESC: "..."
```

Header key `@TAG <short country name>` — `@EST Estonia`, not `@EST Republic of Estonia`. Grep all of
`localisation/english/` (including `replace/`) before adding a key, so it is defined once.

Every `_desc` is **exactly two sentences**, present tense about the country, no hard dates, `§8…§!`
on party and movement names. First sentence: what the country does. Second: what that means for the
world or its neighbours. Written from a 1970 viewpoint. Upstream reference blocks: `TUR` and `BHR` in
`MD_game_rules_l_english.yml`.

`RANDOM_PATH` / `NO_PATH` reuse the shared keys that already exist near the top of the file —
`RULE_OPTION_MD_RANDOM_PATH`, `RULE_OPTION_MD_NO_PATH` and their `_DESC`s. Never write per-country
copies.

## 3. Flag wiring — `common/on_actions/999_game_rules_on_actions.txt`

```
				if = {
					limit = {
						has_game_rule = {
							rule = COLDWAR_DEN_1970_ai_behavior
							option = RANDOM_PATH
						}
					}
					random_list = {
						30 = { set_global_flag = DEN_HISTORICAL_FOCUS_PATH }
						15 = { set_global_flag = DEN_EUROPEAN_UNION_FOCUS_PATH }
						15 = { set_global_flag = DEN_EUROSCEPTIC_FOCUS_PATH }
						10 = { set_global_flag = DEN_NATIONALIST_FOCUS_PATH }
					}
				}
				if = {
					limit = {
						has_game_rule = {
							rule = COLDWAR_DEN_1970_ai_behavior
							option = HISTORICAL
						}
					}
					set_global_flag = DEN_HISTORICAL_FOCUS_PATH
				}
```

One `if` per named option. `RANDOM_PATH` draws from a `random_list` that **includes the historical
bucket** and excludes `NO_PATH`; no bucket may be empty. `NO_PATH` gets no branch at all — it sets
nothing. Flags are global (`set_global_flag`), never country flags.

Optional AI sentiment grant, if the country has one — `if`/`else_if`, no bookkeeping flag:

```
				if = {
					limit = {
						is_ai = yes
						has_global_flag = DEN_SOCIALIST_FOCUS_PATH
					}
					add_timed_idea = { idea = DEN_ai_communist_sentiment days = 1095 }
				}
				else_if = {
					limit = {
						is_ai = yes
						OR = {
							has_global_flag = DEN_MONARCHIST_FOCUS_PATH
							has_global_flag = DEN_NATIONALIST_FOCUS_PATH
						}
					}
					add_timed_idea = { idea = DEN_ai_nationalist_sentiment days = 1095 }
				}
```

Everything downstream gates on `has_global_flag`, **never** `has_game_rule` — including events and
strategy plans, or a `RANDOM_PATH` roll enables the flags but not the plan. Grep every direct
`has_game_rule` reader for your tag (focus tree, events, decisions, strategy plans) and convert each one.

## 4. Scripted triggers — `common/scripted_triggers/COLDWAR_DEN_1970_triggers.txt`

Every ownership group gets an **owner** trigger and a **not** trigger. AI-internal, so no loc key and
no `custom_trigger_tooltip`.

The **historical** group is special and must use this owner trigger — the flag alone is not enough,
because under `NO_PATH` with historical AI on no flag is set and the historical spine would be
zeroed along with everything else:

```
DEN_ai_historical_path = {
	OR = {
		is_historical_focus_on = yes
		has_global_flag = DEN_HISTORICAL_FOCUS_PATH
	}
}

DEN_ai_not_historical_path = {
	OR = {
		has_global_flag = DEN_EUROPEAN_UNION_FOCUS_PATH
		has_global_flag = DEN_EUROSCEPTIC_FOCUS_PATH
		has_global_flag = DEN_SOCIALIST_FOCUS_PATH
		has_global_flag = DEN_NATIONALIST_FOCUS_PATH
	}
}
```

An **alt path** group owns its flag directly, and its not trigger carries the historical killswitch:

```
DEN_ai_not_socialist_path = {
	NOT = { has_global_flag = DEN_SOCIALIST_FOCUS_PATH }
	OR = {
		is_historical_focus_on = yes
		DEN_ai_rival_of_socialist_path = yes
	}
}
```

**Alias** — only when several flags own one spine. Substitute it for the flag on both lines
(`NOT = { DEN_ai_western_path = yes }` in the not trigger):

```
DEN_ai_western_path = {
	OR = {
		has_global_flag = DEN_HISTORICAL_FOCUS_PATH
		has_global_flag = DEN_EUROPEAN_UNION_FOCUS_PATH
	}
}
```

**Rival** — the paths that are not this one. Only worth defining when a not trigger would otherwise
repeat a long flag list, or when several groups share the same rival set:

```
DEN_ai_rival_of_socialist_path = {
	OR = {
		DEN_ai_western_path = yes
		has_global_flag = DEN_EUROSCEPTIC_FOCUS_PATH
		has_global_flag = DEN_NATIONALIST_FOCUS_PATH
	}
}
```

Triggers may call each other, so the set stays small. Keep the depth shallow — three levels is
plenty.

**The `is_historical_focus_on` arm is only safe inside `ai_will_do`.** Under an explicit alt rule with
historical AI on, the plain owner trigger above is _also_ true — harmless there only because the
mandated pair (§5) puts `factor = 0 DEN_ai_not_historical_path = yes` **last**, and that not trigger
is a pure alt-flag OR, so the killswitch wins. Two places break that guarantee:

- An **alias** spanning historical and an alt path. Its not trigger opens with
  `NOT = { DEN_ai_western_path = yes }`, so the alias being true suppresses its own killswitch and the
  historical spine outbids the rule the player picked.
- Any reader **outside** `ai_will_do` — a decision or category `visible`, a strategy-plan `enable`, a
  walker event `trigger`. There is no second modifier to correct it.

Either case needs the alt-flag guard (`99_FRA_scripted_triggers.txt` and
`99_GEO_scripted_triggers.txt` are references):

```
DEN_ai_alt_path = {
	OR = {
		has_global_flag = DEN_EUROPEAN_UNION_FOCUS_PATH
		has_global_flag = DEN_EUROSCEPTIC_FOCUS_PATH
		has_global_flag = DEN_SOCIALIST_FOCUS_PATH
		has_global_flag = DEN_NATIONALIST_FOCUS_PATH
	}
}

DEN_ai_historical_path = {
	OR = {
		has_global_flag = DEN_HISTORICAL_FOCUS_PATH
		AND = {
			is_historical_focus_on = yes
			NOT = { DEN_ai_alt_path = yes }
		}
	}
}
```

Name the helper `TAG_ai_alt_path` for the non-historical flags and `TAG_ai_any_path` when it must
include historical too. A single reader outside `ai_will_do` may instead pair the plain trigger with
its not trigger: `DEN_ai_historical_path = yes` + `DEN_ai_not_historical_path = no` (§8).

Check both failures by hand: a focus alive under an alt rule only because historical is on, and a
decision gate that is dead under `NO_PATH` or visible during an alt path.

**Precondition.** The collapsed shape is behaviour-identical to the old three-modifier form only
while at most one `TAG_*_FOCUS_PATH` flag is ever set and each not trigger excludes its own group's
flags. Check both by grepping every `set_global_flag = DEN_*_FOCUS_PATH` before writing the triggers.

## 5. Focus weights — `common/national_focus/COLDWAR_DEN_1970_focus.txt`

The only shape — one boost, one killswitch. Historical group:

```
		ai_will_do = {
			base = 1
			modifier = { factor = 25 DEN_ai_historical_path = yes }
			modifier = { factor = 0 DEN_ai_not_historical_path = yes }
		}
```

Alt path group (owner is the flag, or an alias where a spine is shared):

```
		ai_will_do = {
			base = 1
			modifier = { factor = 25 has_global_flag = DEN_SOCIALIST_FOCUS_PATH }
			modifier = { factor = 0 DEN_ai_not_socialist_path = yes }
		}
```

Path modifiers are always **multiplicative** (`factor`), never `add` — an `add` loses to any
multiplicative historical modifier, which is the default state. Situational `add` nudges unrelated
to paths are fine and stay.

The two path modifiers go **last in the block**, after every other modifier. Order matters:
modifiers apply in sequence, so an `add` after a `factor = 0` resurrects a focus the killswitch was
meant to kill. Everything else in the block (bankruptcy, `can_staff`, `ai_is_threatened`, crisis
weighting) keeps its place and form — never fold a guard into a path trigger.

Upstream writes these with `apply_ai_path_weights.py`, which is not in this repository. Write them by
hand: first author a mapping table (focus id → ownership group, boost) in the PR notes, then apply it
block by block, removing any older path modifiers in the same block. If the tree is generated by a
`tools/<country>_1970/` builder, apply the mapping in the builder's source and rebuild. Re-grep every
mapped id afterwards to confirm exactly one boost and one killswitch, last in the block.

Leave the economy, army, airforce and equipment trunk path-neutral — only re-own focuses that
actually belong to a path.

## 6. AI-only popularity ramp — decisions

Needed when the chosen path's party cannot reach power on its own. Category in
`common/decisions/categories/COLDWAR_DEN_1970_categories.txt`:

```
DEN_ai_path_category = {
	allowed = {
		is_ai = yes
		original_tag = DEN
	}

	icon = GFX_decisions_category_political
	priority = 100

	visible = {
		OR = {
			has_global_flag = DEN_MONARCHIST_FOCUS_PATH
			has_global_flag = DEN_NATIONALIST_FOCUS_PATH
		}
	}
}
```

The icon must be a **category** sprite (52x40, `GFX_decisions_category_*`), not a decision one.

Raw flags are right only while every path in the `visible` is an **alt** path, as above. A ramp that
also has to run for the **historical** party gates on the alt-guarded `DEN_ai_historical_path` (§4)
instead — raw `DEN_HISTORICAL_FOCUS_PATH` is dead under `NO_PATH` with historical AI, which is the one
state the trigger exists to cover, and a bare unguarded trigger runs the historical ramp on top of the
alt ramp the player picked.

A ramp pair per path, in `common/decisions/COLDWAR_DEN_1970_decisions.txt`:

```
	DEN_rally_the_monarchists = {

		icon = generic_decision

		cost = 25

		days_re_enable = 30

		visible = { has_global_flag = DEN_MONARCHIST_FOCUS_PATH }

		available = {
			has_civil_war = no
			check_variable = { party_pop_array^23 < 0.55 }
		}

		complete_effect = {
			log = "[GetDateText]: [Root.GetName]: Decision DEN_rally_the_monarchists"
			set_temp_variable = { party_index = 23 }
			set_temp_variable = { party_popularity_increase = 0.04 }
			set_temp_variable = { temp_outlook_increase = 0.04 }
			change_relative_party_popularity = yes
		}

		ai_will_do = { base = 100 }
	}

	DEN_monarchists_take_the_country = {

		icon = generic_decision

		cost = 150

		days_re_enable = 180

		visible = { has_global_flag = DEN_MONARCHIST_FOCUS_PATH }

		available = {
			has_civil_war = no
			nationalist_monarchists_are_in_power = no
			check_variable = { party_pop_array^23 > 0.5 }
		}

		complete_effect = {
			log = "[GetDateText]: [Root.GetName]: Decision DEN_monarchists_take_the_country"
			set_temp_variable = { rul_party_temp = 23 }
			change_ruling_party_effect = yes
		}

		ai_will_do = { base = 100 }
	}
```

The category is `is_ai = yes`, so **no localisation keys at all** — not for the category, not for a
decision name or desc — and bare `check_variable` in `available` with no
`custom_trigger_tooltip`.

Read `change_relative_party_popularity` before picking numbers: passing `temp_outlook_increase`
skips the sibling-redistribution loop, so it is required when the target group starts at zero and
wrong when the target sits inside a group next to the incumbent.

## 7. AI strategy — war weighting

**Write none.** An AI path PR adds no war block to `common/ai_strategy/`: no per-target readiness
gate (`TAG_avoid_unready_war_with_X`, `TAG_prepare_war_with_X`), no `declare_war` / `conquer`
hold-and-release tiers, no `avoid_starting_wars`, no losing-war brake. War-goal declaration is
already covered by the general suite in `MD_war_declaration_ai.txt` (mod-wide restraint without
`allowed`, plus the named rivalry pairings) and the engine's own wargoal handling. Review rejects
every per-TAG variant. Existing per-TAG war blocks in other countries are legacy, not models.

**When a focus war fires too early**, fix it in the focus: a strength check in `available` (Bolivia's
`BOL_revenge_of_1879` reads `fighting_army_strength_ratio = { tag = CHL ratio > 1.2 }`) or a
killswitch / factor in `ai_will_do`. If the mod-wide brake is genuinely too weak for every country,
that is a separate PR against `MD_war_declaration_ai.txt`, not a per-TAG block.

**Pre-existing blocks** in `common/ai_strategy/TAG.txt` stay untouched unless they are the
`declare_war`-on-`has_war_with` bug below. `declare_war` is target-keyed and weights only
**opening** a war, so a block gated on `has_war_with = TARGET` is a no-op. Never add a
`TAG_cancel_war_TARGET` block.

**Never** add an `on_daily_<TAG>` pass that caches booleans into country flags for `enable` or
`ai_will_do` to read. Both are already evaluated lazily; a daily cache costs more and lags real
state by a day. Write the condition inline.

## 8. Historical government walker — `events/COLDWAR_DEN_1970_events.txt`

Only when the country's 1970s roster is a **dated timeline** (SKILL.md §2, point 6). On an undated successor
roster, write nothing: the ramp decisions in §6 already deliver the party, and a walker over an
undated roster installs the wrong person.

The path rule steers the party; nothing steers the person. `set_leader` runs on a re-election only
behind a term limit, and most history files set none, so a country whose party keeps winning never
rotates its leader. The walker is the fix: an AI-only hidden event fired at the real historical
dates, which asserts the ruling party and the roster pointer and lets the existing succession list
supply the name.

```
country_event = {
	id = denmark_md.400
	hidden = yes
	is_triggered_only = yes

	trigger = {
		is_ai = yes
		has_civil_war = no
		DEN_ai_historical_path = yes
		DEN_ai_not_historical_path = no
		NOT = { has_country_flag = generic_election_killswitch }
	}

	immediate = {
		log = "[GetDateText]: [Root.GetName]: event denmark_md.400"
		if = {
			limit = { date > 1975.2.11 }
			set_variable = { liberalism_leader = 2 }
			set_temp_variable = { rul_party_temp = 2 }
		}
		else_if = {
			limit = { date > 1973.12.19 }
			set_variable = { socialism_leader = 1 }
			set_temp_variable = { rul_party_temp = 3 }
		}
		else = {
			set_variable = { socialism_leader = 0 }
			set_temp_variable = { rul_party_temp = 3 }
		}

		if = {
			limit = { NOT = { is_in_array = { ruling_party = rul_party_temp } } }
			change_ruling_party_effect = yes
			set_elections_60_months = yes
		}
		else = {
			set_leader = yes
		}
	}
}
```

(The dates and indices above are illustrative; take the real ones from the country's 1970s roster.)

Scheduled once per historical date from the matching `trigger_year_<Y>_events` block. The dispatcher
runs at the January tick and MD's day counts ignore leap years. **This fork** defines those blocks
only for 2001 to 2030, so a 1970s walker first adds `trigger_year_1971_events` (and so on) in a
namespaced effects file such as `COLDWAR_DEN_1970_yearly_effects.txt`, and the PR states that the
dispatcher reaching it is untested in game:

```
DEN = { country_event = { id = denmark_md.400 days = 158 } }
```

**Pointer semantics.** `<subideology>_leader = N` means _the next person created is roster index N_.
Each roster block in `common/scripted_effects/<TAG>_political_leaders.txt` increments before creating,
and the blocks are sequential `if`s rather than `else_if`s, so the cascade keeps running past N until
a block's `date <` end-of-tenure guard sets `b = 1`. The last entry of every branch sets `b`
unconditionally, so the list never falls off its end.

**Assert the index in every branch.** Never blind-advance by calling `set_leader` and trusting the
pointer. Explicit assertion makes each date idempotent and self-repairing: a generic election between
two historical dates moves the pointer, and the next date snaps it back. A walker that
blind-advances installs the wrong person.

**Never pass `change_leader_temp = 1`.** It sets `do_not_retire`, which makes the roster cascade
pin at the current pointer instead of fast-forwarding. Use it only to deliberately keep an
incumbent across a coalition reshuffle.

**Bound the date chain.** One descending `if`/`else_if` where every branch asserts both the party and
the roster index, then one shared tail that decides change-vs-advance. The chain's final `else` must
not change the ruling party on its own: with no upper bound, a re-fire after the last historical date
reinstalls the earliest government.

**`set_elections_XX_months` on a party change only**, matching the
country's `election_frequency`. It resyncs `last_election` so the generic clock does not fire weeks
later and undo the forced government. Calling it on every branch suppresses AI election news
indefinitely.

**Never inline `create_country_leader`.** It duplicates the leader data, leaves the person missing
from the roster, and desyncs the pointer for every other caller of `set_leader`. If the historical
person is absent, append an entry to
`<TAG>_political_leaders.txt` in that file's exact existing shape, with a real end-of-tenure `date <`
marker and a `picture =` that exists under `gfx/leaders/<TAG>/` — nothing validates leader portraits,
and the filename is case-sensitive on Linux.

The event is hidden and `is_ai = yes`, so it gets **no localisation keys at all**. Gate on the §4
scripted triggers, never on raw flags: countries converted before this standard carry older flag names
(ENG reads `ENG_HISTORICAL_AI_FOCUS`, not `_FOCUS_PATH`). Between two historical dates the generic
election machinery still runs and may seat someone else; the next date re-asserts. That is the
accepted fidelity ceiling. The `is_ai = yes` trigger is what keeps a human-run country's government
in the human's hands; never remove it.
