# Party Localisation Reference

Read before adding or reworking any `TAG.<subideology>` key. Three files are involved:

- `localisation/english/MD_politics_view_parties_l_english.yml`: name, icon, and
  description strings.
- `common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt`: the
  per-tag hooks that select them.
- `interface/MD_parties_icons.gfx`: the `GFX_<TAG>_<party>` sprites.

A loc key with no hook is dead. The politics view calls `[conservatism_L]`, which
resolves through the scripted-localisation switch. It never reads `TAG.conservatism`
directly.

## This fork: 1970 party names

The inherited `TAG.<subideology>` keys describe each country's parties around 2000. For
the 1970 start, do not rewrite them. Add 1970 keys and route to them first:

- Keys: `COLDWAR_<TAG>_party_<subideology>`, `..._desc` and, when a tag sprite exists,
  `..._icon`, in `localisation/english/COLDWAR_<TAG>_party_l_english.yml` (UTF-8 BOM).
- Hooks: in `00_MD_politicsview_scripted_localisation.txt`, insert one clause
  **immediately before** the existing clause for the same tag and block:

  ```
  text = { trigger = { original_tag = TAG IMP_is_1970_scenario = yes } localization_key = COLDWAR_TAG_party_conservatism }
  ```

  Keep the inherited clause after it as the modern fallback.
- The starting ruling party label (`IMP_1970_historical_ruling_party_L` and the
  `IMP_1970_<TAG>_STARTING_PARTY` keys) is a separate, existing system. Keep the two
  consistent: the slot that rules on 1 January 1970 must carry the same party in both.
- `docs/iceland_1970/PARTY_INTEGRATION.md` is the worked example, including the
  per-slot table and the leader-window approach.

## The 24 subideologies

Defined in `common/ideologies/00_ideologies.txt`. `^N` is the country's `party_pop_array`
slot, set in `history/countries/<TAG>*.txt`.

| `^N` | Subideology                  | Ideology      | Generic label                 |
| ---- | ---------------------------- | ------------- | ----------------------------- |
| 0    | `Western_Autocracy`          | `democratic`  | Pro-Western Autocrats         |
| 1    | `conservatism`               | `democratic`  | Conservatives                 |
| 2    | `liberalism`                 | `democratic`  | Liberals                      |
| 3    | `socialism`                  | `democratic`  | Social Democrats              |
| 4    | `communist_state`            | `communism`   | Communists                    |
| 5    | `anarchist_communism`        | `communism`   | Left-Wing Radicals            |
| 6    | `Conservative`               | `communism`   | Reactionaries                 |
| 7    | `Autocracy`                  | `communism`   | Autocrats                     |
| 8    | `Mod_Vilayat_e_Faqih`        | `communism`   | Moderate Shiite Revolutionary |
| 9    | `Vilayat_e_Faqih`            | `communism`   | Hardline Shiite Revolutionary |
| 10   | `Kingdom`                    | `fascism`     | Pro-Establishment Salafism    |
| 11   | `Caliphate`                  | `fascism`     | Salafi Jihadism               |
| 12   | `Neutral_Muslim_Brotherhood` | `neutrality`  | Moderate Islamists            |
| 13   | `Neutral_Autocracy`          | `neutrality`  | Non-Aligned Autocrats         |
| 14   | `Neutral_conservatism`       | `neutrality`  | Conservatives                 |
| 15   | `oligarchism`                | `neutrality`  | Oligarchs                     |
| 16   | `Neutral_Libertarian`        | `neutrality`  | Libertarians                  |
| 17   | `Neutral_green`              | `neutrality`  | Greens                        |
| 18   | `neutral_Social`             | `neutrality`  | Socialist Democrats           |
| 19   | `Neutral_Communism`          | `neutrality`  | Communists                    |
| 20   | `Nat_Populism`               | `nationalist` | Right Wing Populists          |
| 21   | `Nat_Fascism`                | `nationalist` | Fascists                      |
| 22   | `Nat_Autocracy`              | `nationalist` | Military Junta                |
| 23   | `Monarchist`                 | `nationalist` | Monarchists                   |

Case matters. `neutral_Social` and `oligarchism` are the only two with a lowercase first
letter.

## Key format

```
 MOR.conservatism: "£MOR_NRI (RNI) - National Rally of Independents"
 MOR.conservatism_icon: "£MOR_NRI"
 MOR.conservatism_desc: "(Classic Liberalism) - National Rally of Independents (Arabic: Altajamue Alwataniu Lil'ahrar, French: Rassemblement National des Indépendants, RNI)\n\nDescription."
```

- Every line has a leading space before the key.
- A tag's keys sit in one contiguous block, placed alphabetically by tag and ordered
  inside the block by `^N`.
- `(Ideology Group)` is the party's real-world label (`Liberal Conservatism`,
  `Salafi Jihadism`), not the MD subideology token.
- Native names follow the English name, one language per label, abbreviation last.
- `\n\n` is a literal backslash-n pair in the `.yml`.
- Descriptions are factual and present tense, and describe the party as it is under its
  own gate. No forward references to a later rename, merger, or split.
- Tags to copy from: `MOR`, `ITA`, `GEO`.

## Icons

A party gets an `_icon` key only when a tag sprite exists: a `spriteType` in
`interface/MD_parties_icons.gfx` backed by a `.dds` under
`gfx/texticons/parties_icons/<country>/`. Never invent a `GFX_` name.

With no tag sprite, use the generic one inline in the name key and omit the `_icon`
key. The icon hook falls back to `generic.<slot>_icon`. Generic sprites are
`GFX_generic_<slot>_small`, with two irregulars:

- `communist_state` uses `£generic_Communist_State_small`.
- `Neutral_Muslim_Brotherhood` uses `£muslim_brotherhood_small`.

## Hooks

Each subideology has three `defined_text` blocks: `<slot>_L` (name), `<slot>_L_desc`,
and `<slot>_L_icon`. Each is a switch sorted alphabetically by tag that ends in a
generic fallback:

```
 text = { trigger = { original_tag = GRE } localization_key = GRE.conservatism }
 text = { localization_key = generic.conservatism }
```

Add one line per block per party. Use `original_tag`, never `tag`, so a civil-war
split-off keeps its parties.

## Flag-gated variants

A mid-period identity change (rename, merger, dissolution, split) is a flag set by a
flavor event, not a bare `date >` in the hook. First match wins, so the flag line goes
first:

```
 text = { trigger = { original_tag = BOT has_country_flag = BOT_business_botswana_formed } localization_key = BOT.oligarchism_2015 }
 text = { trigger = { original_tag = BOT NOT = { has_country_flag = BOT_business_botswana_formed } } localization_key = BOT.oligarchism }
```

The event (`Botswana_events.8` is the upstream reference) is `is_triggered_only` and
`fire_only_once`, checks `original_tag`, has no picture, and its one option sets the
flag and runs `update_party_name = yes`. Schedule it on the real date through the yearly
dispatcher. **This fork:** only `trigger_year_2001_events` to `trigger_year_2030_events`
exist, so a 1970s change first needs its `trigger_year_<YYYY>_events` block (see
`coldwar-1970-context.md`). In a multiplayer RP game an identity change should follow
from what happened in that game where possible (a focus, decision or election result),
with the dated event only as the AI-country fallback.

- Split the icon hook too, or the old logo shows beside the new name.
- Check the tag in copied gate lines. A `GER` for `GRE` typo is silent, since both tags
  are valid.
- Older bare date gates exist. Do not add new ones.

## Choosing parties

Use only organisations that existed on 1 January 1970, plus later ones behind the event
or flag that creates them (founding, split, legalisation, return from exile). Parties
that are banned or in exile in 1970 (for example under a junta or one-party state) may
fill a slot but say so in the description. If a slot has no real counterpart, leave it
generic.

Non-party entities are acceptable where MD precedent exists: employers' confederations
for `oligarchism`, `<Country> Armed Forces` for `Nat_Autocracy`, and the royal house for
`Monarchist`. Say what the entity is in its description.

## Verification

Upstream's `validate_party_loc.py` is not in this repository. Run the static checker
on the touched `.yml` and scripted-localisation files (`validation-pipeline.md`), then
check by hand: name and description format, every key has a hook and every hook a key,
icon agreement, subideology casing, no duplicate gates, and

1. Every `£sprite` resolves in `interface/`.
2. Keys are alphabetical within the block, with the leading space and BOM intact.
3. `party_pop_array^N` indices in `history/countries/<TAG>*.txt` match their slots.
4. Each 1970 clause sits before the inherited clause for the same key and carries
   `IMP_is_1970_scenario = yes`.
5. In game: the politics view on 1 January 1970, then after `event <id>` for each new
   identity-change event.
