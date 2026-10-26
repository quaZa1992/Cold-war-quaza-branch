# Party paths – design rules (generic 1970 tree, COLDWAR)

Work directory: this folder. Data only (no game code yet): `dsl.py` (vocabulary + effect helpers), `build.py` (template, layout, validator, scoring), reference party `parts/R_jun.py` (read it first – it is the quality bar).

## Template (fixed, positions/prerequisites/costs come from build.py)

```
E (entry, cost 5)                      programme on, faction, law
POL (5)                 ECO (5)        hubs: political / economic question
A1 ⟷ A2 (7.2)           B1 ⟷ B2 (7.2)  choice A = how the party rules; choice B = economic model / who pays
A1f   A2f (8.6)         B1f   B2f       exclusive payoff of the chosen side (only reachable through it)
PM (5)                  EM (5)          merge (OR of the two follow-ups)
C1 ⟷ C2 (7.2)           D1 ⟷ D2 (7.2)  choice C = society / security / culture; choice D = foreign stance / military / allies
CM (8.6)                DM (8.6)        payoff after the choice (OR)
              CAP (10)                  capstone (needs CM and DM)
```
Trunk per outlook: `T0` champion (existing id, 5-way exclusive with the other champions) → `T1a ⟷ T1b` (new choice, existing ids) → `T2` majority (OR) → `T3` government (no prerequisite, available while the outlook rules; party entries hang from it).

## Rules (the technical brief)

1. **Impact.** Every focus ≥ 2 real effects and a net score inside its band (`build.py` BANDS). Prefer programme/idea lines of 0.05–0.10 over 0.02 crumbs. Each party needs lasting assets (buildings, tech, XP, national spirits) – aim for 6+, minimum 4. Capstone = a national spirit (`idea`/`swap`, 3–5 lines) or 2+ buildings, plus something else.
2. **Choices.** Four per party (A, B, C, D). Each side: a real gain (≥ 3 points, ideally 5–7) **and** a small visible price (1–2.5 points). Comparable value (net difference ≤ 2.5). Different *kind* of reward on each side (legitimacy vs power, buildings now vs a lasting modifier, guns vs butter, state vs market, ally A vs ally B, who pays) – the player should want both. Not mirrored numbers. The follow-up (A1f …) is the exclusive payoff of its side: make each one distinct and attractive.
3. **Downsides** outside choices only where they make sense (money for buildings, a faction that loses). Never hidden.
4. **Historically justified.** Every focus has `why`: one or two English sentences with a concrete 1960s–80s precedent (country, year, institution or person), ≤ 320 characters. Each party has `identity` (one sentence) and `history` (the real 1970s variants the choices are built on). Names in English, evocative, ≤ 42 characters, unique across the tree; no real person names in focus names (generic tree).
5. **Generic.** Works for any country governed by that party: no country tags, states or wars, no annexations, no forced bloc change, nothing executed in another country. Cold War effects only through `tension()` and the `mdcw_cw_*` / `imp_*` modifier keys.
6. **Vocabulary only from `dsl.py`:** `KEYS`, `FACTIONS`, `BUILD`, `LAWS`, `CATS`, `MD_IDEAS`. Buildings are paid by the MD helpers (no extra money line needed).
7. **Existing ids.** `E` must keep the party's existing entry id. Re-use the existing exclusive pair, its two follow-ups and the capstone (`old=True`) in the slots where they fit best (keep their names). New ids: `<partykey>_<snake_case_name>`. Idea ids start with `<partykey>_` (trunk ideas with `trunk_<o>_`).
8. **Political power** in at most 3 foci per party (entry/hubs/merges, or a choice side that buys PP with a price), ≤ 150. No PP-only focus.
9. **Programme vs spirit.** `prog` = the party programme (active only while this party governs – right for party policy). `idea(..., bound=True)` = regime institution that falls with the party; `bound=False` = lasting national reform. Buildings/tech/XP are permanent.
10. **Religious paths** (mvf, vf, sk, cal, mb) stay behind the existing religion gates; keep content sober, institutional and non-glorifying.
11. **Check:** `python3 build.py parts/<yourfile>.py` must report 0 errors and 0 warnings. Then run `python3 build.py` (all files) to catch duplicate names.

## Programme caps (richest path): see `PROG_CAPS` in build.py.

## House rules of 19.10.2026 (now enforced by build.py – they override the bands above)

- **Bands by cost (net points = gain − price):** cost 2 → 1.5–3.5 · cost 5 → 3.5–6.5 · cost 7.2 → 4.0–7.5 · cost 8.6 → 5.0–9.0 · cost 10 → 6–11. Entry and government foci may exceed the upper end by 3.
- **Choices:** both sides a real gain and a small visible price (1–2.5 points); net gap between the sides ≤ 1.5; the two sides share at most ONE modifier key; never PP on both sides.
- **Political power:** at most 2 foci per party tree; amounts only 50 / 75 / 100 / 150; never on a capstone.
- **Values per focus:** one-off stability ≤ +6 % (capstone exempt); XP 15–50 per line; factions +5 / +10 (never above +10), costs −5 / −10 / −15 … −25; `fac('all', …)` within ±5; party popularity ≤ 0.10; ≤ 6 programme lines.
- **Cold War / Imperia key sizes** (programme line / idea line): ideological defence 0.10 / 0.30 · support effectiveness 0.10 / 0.25 · assistance limit 0.25 / 0.50 · assistance capacity 1 / 2 · market exposure 0.10 / 0.25 · military programme cost 0.15 / 0.25 · sanction resistance 0.10 / 0.15 · globalism 5 / 15 · oil price resistance 0.10 / 0.20. Ideological defence on the richest path ≤ 0.50.
- **Money gains** (`money(+x)`) need a political price in the same focus (faction loss, corruption, tension, stability, a cost line).
- **Impact first:** when a focus is below its band, raise the GAIN (stronger programme/idea lines within caps, a paid building, a tech bonus, XP ≤ 50, a timed or permanent spirit) rather than deleting the price. Keep prices small (1–2.5 points).
