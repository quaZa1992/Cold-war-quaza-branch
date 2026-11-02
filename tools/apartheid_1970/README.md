# IMPERIA COLD WAR 1970 apartheid implementation

`compile.py` owns the dynamic spirit, its exact user-supplied base, five policy domains, reform and restoration decisions, shared focus branch, native numeric previews, recipient-approved diplomatic normalisation and historical exceptions. It patches only two commercial agriculture calculations in the native money system and attaches one shared branch to the existing generic tree.

Run from the mod root:

```powershell
python tools/apartheid_1970/compile.py
python tools/apartheid_1970/validate.py
python tools/apartheid_1970/preview.py
```

The generator advertised in the generic focus header is absent from this checkout. The active `Claude outputs/COLDWAR_GEN_generator/gen_focus.py` preserves the loaded tree header, including this attachment. Do not regenerate the entire generic tree to install this feature. The scoped compiler is idempotent and preserves unrelated current content.

Policy tiers range from 4 to 0, each representing one quarter of that domain's specified base. Contributions are assigned afresh from their base and tier on each refresh. They never multiply an already scaled contribution. The dynamic modifier is refreshed before the native economy. When every domain reaches zero it is removed; restoration decisions remain reachable through the retained policy mandates. Ending political controls changes the title to `Legacy of Racial Segregation` while other domains remain.

The five 35-day focuses each perform one first reform and unlock the domain's two repeatable decisions. Further reform or restoration costs 75 political power and shares a 90-day domain cooldown, or 180 days for population policy. These costs and intervals are implementation balance choices. Government changes do not automatically repeal policy. AI weights are zero for policy changes to preserve player direction.

Worldwide opposition is a literal incoming trade-opinion modifier of -20 points at the base. Regional opposition separately adds -50 trade and -50 diplomatic opinion in both directions. Each originates in a distinct modifier namespace, so two host countries cannot erase one another's opinion entries. All four old tiers are removed before the active tier is reapplied. Monthly refresh observes independence, revival, war, concessions and changes in authored colonial or minority-government status.

Normalisation offers cost 50 political power and last 180 days. The recipient owns acceptance, refusal and withdrawal. There is no event or acceptance picture. Two concessions in political or public-service reform are required while some political controls remain. Acceptance removes the regional penalties while peace and concessions persist; the worldwide trade penalty remains. Backtracking or war suspends the exception. A recipient can withdraw it. Repeated acceptance has no additional effect.

At a 1970 start the independent hosts are SAF and ZIM. Namibia's starting states are owned by SAF. An actually released NAM under SAF can initialize the system; an independent liberation government does not receive it merely because its tag is NAM. Already initialized NAM retains its reform branch after independence.

Malawi has a revocable historical regional exception with South Africa. Botswana, Lesotho and Swaziland have trade-only exceptions reflecting customs arrangements, while diplomatic opposition remains. Existing and future colonial exemptions require actual subject status for known dependencies; the extension flag `COLDWAR_AP_colonial_government` also requires subject status. An authored sovereign settler regime can use `COLDWAR_AP_minority_government`; its owning political system must clear that flag when minority rule ends. No country is classified by a leader's ethnicity or a general ideology slot.

`validation.json` records source/parser and source-driven effect-model checks, including every one of the 3,125 possible policy vectors, repeat execution, diplomacy direction, recipient scope and cleanup. These are not native engine or multiplayer results. Fractional opinion display, actual focus hovers, expected-spending caps and weekly native budget application need a game rehearsal. A 1970 save created before this feature has no recorded policy history; its first weekly pass initializes historical defaults. Do not use that migration as a reconstruction of a previously reformed late-game country.

The complete base table and historical rationale are in [the design record](../../docs/design/SAF_1970_APARTHEID_CONCEPT.md). The [focus preview](../../docs/design/apartheid_1970/FOCUS_PREVIEW.html) includes the existing generic tree and a normal-size view of the five additions, using emitted coordinates and prerequisite links.
