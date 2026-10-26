# COLDWAR UAE / Trucial States, 1970

The approved tree is installed as `COLDWAR_UAE_1970_focus`. Start a **new 1970 campaign as UAE / Trucial States** with the mod's Millennium Dawn dependencies enabled. The country history selects this tree and the generic fallback excludes this campaign. Later starts retain their native history/providers. Existing-save migration is not a verified target.

The immutable original snapshot has SHA-256 `23e89bc7f0a02f4df337248bcfa67d139ec8fc910c414978a3f5ef5913158272`. Subsequent authorized overlays now produce **114 focuses and three decisions**. The latest [focus-led policy revision](FOCUS_ONLY_IMPLEMENTATION.md) supersedes older inventories: only OPEC and reserve management remain decisions; domestic programmes and foreign offers use focuses. Four optional/reactive focuses cover political competition and Kuwait responses. `flavour.py` and explicit reviewed overrides supply English narrative.

## Starting situation and British withdrawal

Latest user duration revision: all114 national UAE focuses now take70 nominal
days (`cost = 10`), including proclamation, oil and industrial projects. Earlier
duration figures in historical audit snapshots are superseded. Shared GCC
focuses retain their separate multi-country durations.

- The dated country history directly defines the **Trucial States Council**, its portrait, **Western Autocracy** subparty 0 and **Trucial States** identity. Selection-preview identity requires no startup call or scenario predicate. The historical ruling houses follow MD's Western outlook; an alternate sovereigntist dynastic alignment retains Monarchist subparty 23. Both use the existing dynastic programme. [Native MD comparison and integration revision](NATIVE_OUTLOOK_REVISION.md).
- Native Gulf government-change cosmetics preserve the Trucial name until actual federal formation. British treaty protection preserves the domestic government instead of imposing the overlord's party; this exemption does not restore a party or cover other subjects, other overlords or later non-treaty puppeting.
- Both countries start with **British Withdrawal Announced**. The announced deadline was the end of 1971; the scenario uses **1 December 1971** as the historical execution date. No focus or new British approval is required.
- UAE remains a British subject until actual release. **A Coast in Transition** requires full independence. **The Protected Coast** requires British subject status and has no treasury fee or silent funding gate; its ongoing contribution ends with protection.
- **British Withdrawal** remains the constitutional join after actual independence and the founders' settlement. The following **Proclaim the Union** focus alone forms/names the United Arab Emirates and creates the federal offices. Independence, the calendar and the earlier focus do not rename the country or replace the collective Council.
- Only a mutually accepted alternative replaces the current plan. Pending/refused proposals never pause it. Acceptances check their non-reused event round and current treaty version. Late renewal cannot postpone a release already due.
- Paired UK/UAE spirits show their terms and matching dates. Exactly one UAE carrier supplies −10% political power while subject to Britain. A retained-protection review date does not itself cause independence.
- Taking no British opening focus does not block later handover/friendship preparation. Only the non-exclusive liaison root is bypassed without fees or rewards; no exclusive choice is automatically completed.

Treaty descriptions use country-specific English lore from `flavour.py`, followed by the scheduled, actual or review date. They do not expose the mechanical concept catalogue. `art.py` resolves national spirits through native `MD_ideas.gfx` and requires textures under `gfx/interface/ideas/`; focus artwork and completion shine retain their approved sources. The artwork change covers all 31 spirit/programme/office aliases.

## Economy and earned progress

The starting **An Expatriate Workforce** spirit gives **+10% workforce size**
and **−20% Division Recovery Rate** (`army_morale_factor`). The later user
revision replaces its former recruitable-population penalty; it no longer
reduces the recruitable-population factor.

The starting **Pearls, Fishing and Dhows** spirit represents the inherited coastal economy: **+10% primary-sector productivity**, **+3% office-sector productivity** for maritime merchants, **-5% social spending multiplier**, and **-5% country productivity growth** from its difficult transition. It enters the actual native primary/office GDP, tax and social-cost readers; it is not a recurring treasury gift. Social relief affects the native population/law-based welfare bill, not the separate flat guest-worker supplement. Pearling is described as a declining legacy by1970, alongside active fishing and dhow commerce.

Two existing focuses develop that economy without enlarging the tree: **Pearls and Fishing** costs$0.10bn and adds+10% primary-sector productivity,+6% office productivity and-2% social spending multiplier before oil expansion. **Fishing Harbours** costs$0.15bn, adds another+10% primary-sector productivity,-3% social spending multiplier and+2% energy use, retains its port-construction/bureaucracy effects, and removes the inherited-5% growth penalty. The maritime starting icon is native `GFX_idea_maritime_industry` using an actual national-spirit72x64DDS, not focus art.

Each of the four successfully delivered oil-capacity focuses reduces the original maritime productivity and social-cost relief by20%, retaining shares of100/80/60/40/20%. Only the starting maritime spirit and the two named coastal investments scale. Other commerce, industry, harbour construction,+3% harbour bureaucracy and+2% harbour energy remain unchanged; the inherited growth penalty and its remedy also remain unchanged. With both coastal focuses earned, the compatible maritime totals are primary productivity+30/+24/+18/+12/+6%, office productivity+9/+7.2/+5.4/+3.6/+1.8%, and social multiplier-10/-8/-6/-4/-2%. `maritime.py` owns the shared arithmetic; reconciliation derives it from persistent delivery receipts, independent of focus order and later governments. Investing after the oil boom grants only the retained share. Every oil hover shows its actual marginal losses on the named existing carriers using native signed numbers.

Historical references: [Abu Dhabi Culture maritime life](https://abudhabiculture.ae/en/cultural-heritage/intangible/heritage-register/social-practices/maritime-life), [Qatar Digital Library pearling archives](https://www.qdl.qa/finding-aid-sources-gulf%E2%80%99s-pearl-industry-and-trade), and the [1970 Trucial States Development Office fisheries report](https://humanities-collections.exeter.ac.uk/dame/files/original/f0f7b43183694bfdadba9407357026ed9ad32213.pdf). Growth bonuses, zero starting metals/composites and the200% tree-growth cap are preserved.

Start: **4 base oil — Abu Dhabi 3, Dubai 1**. The once-only resource bootstrap and starting economic debuffs precede native GDP calibration. The existing accounting offset preserves the authored $0.686bn initial GDP target. Later development, native world prices and depletion remain active; refresh never refills oil or resets the GDP ledger.

**1970 starts with zero light metals, zero steel and zero composite plants in both states.** `economy_start.py` removes the inherited19+22 light metals and5 steel once, before the GDP calibration, under the original static1970 UAE identity and full ownership/control guards. It explicitly zeros the1970 composite history and clears any remaining initial plants with a bounded native removal. Native later-bookmark composite levels1/0 are restored by dated2000 history snapshots. These dates are not runtime events. Reload/refresh never strips funded later resources or buildings.

The four extraction projects cost **$0.75bn / $2.50bn / $5.00bn / $8.00bn**, adding **8 / 10 / 15 / 10** base oil: **$16.25bn for +43**, reaching nominal47 before extraction/depletion. Every UAE focus now has **no Treasury prerequisite**, including its actual application/retry guard; displayed costs still debit once through native `modify_treasury_effect`. Insufficient cash therefore does not prevent the focus or suppress its reward. Negative balances are handled by MD's existing automated debt system. Ownership/control, prerequisites, exclusive choices, recipient consent and once-only receipts remain enforced. Decision and agreement affordability remains separate and unchanged.

The industrial port commissions **one real civilian factory after70 focus days for$7.5bn**, using the native focus-price precedent. It supplies the completed industrial base needed by the two complementary70-day projects after Earnings beyond Oil: **Jebel Ali Smelter costs$4.5bn for+12 base aluminium inDubai and+12% energy use; Steel Rolling Mills cost$3bn for+5 base steel inAbuDhabi and+6% energy use**. Both recheck finishedDubaiCIC and recipient ownership/control before once-only payment, without requiring a positive balance. Resource grants remain physical; their ongoing energy burden suspends while the actual facility state is lost and resumes on return. Industrial port plus both metal projects cost$15bn. These are processing industries, not invented domestic ore deposits.

The exclusive aviation alternative now commissions **one Dubai airport/airbase level for$2.5bn after70days**, without giving shared slots, planes or troops. Both capital focuses deliver completed facilities, avoiding a first-factory queue in a country with no startingCIC. Other previously queued projects keep ordinary construction.

Five public-service focuses now provide large native `monthly_population` contributions: **Schools and Clinics+40%; Water for the Towns+30%; Homes for Citizens+50% OR Housing the Workforce+90%; Services That Endure+40%**. Costs are$0.15bn/$0.50bn/$0.75bn or$0.60bn/$0.25bn; water and housing programmes take70days. Recurring health/social/power burdens accompany the benefits. The full six-focus population routes, including the existing training and technical institutes, cost **$1.69bn or$1.54bn** and add **+160% or+200% to normal population growth**. This does not instantly increase population by those percentages. At MD's0.6% yearly base alone, the resulting rates would be1.56% or1.80% yearly before GDP, migration and other modifiers. A hard+200% focus-tree cap is enforced on every programme refresh, including abnormal combinations of both exclusive housing flags. Native focus tooltips show the actual marginal benefit at the cap. No other UAE focus programme supplies an uncapped growth contribution; generation rejects a new provider outside this pool. Native GDP, migration and other game systems keep their own normal modifiers.

Historical basis: [EGA](https://www.ega.ae/en/about-us/operations/jebel-ali/) dates smelter construction to1976 and production to1979. [EMSTEEL](https://www.emsteel.com/our-journey/) dates its own rolling mill to2001; the earlier playable steel programme is an explicitly accelerated alternative. The native focus helpers charge7.5bn for a civilian factory and2.5bn for an airbase in `00_scripted_effects.txt`; the separate international-investment system charges12bn for aCIC. The new focuses use the focus precedents, not the investment array or historical nominal invoices.

National remedies survive government changes. Political contributions follow the actual native subparty, suspend on departure and return with earned progress. Refresh never repeats cash, oil, buildings, productivity or experience. Positive stability contributions in each active political programme are capped at +15 percentage points; negative contributions remain. Starting penalties are recomputed from their original components and clamp at zero.

`presentation.py` uses the main MD Russia pattern: named dynamic modifiers, native signed formatter rows, native treasury/building/resource/experience effects, decision unlocks and event names. Starting-spirit relief previews show the actual current-to-post-focus numeric change, including family maxima and clamps. Positive political stability previews show the marginal capped change. All50 status/government-dependent programme previews now show their prospective native numbers even before eligibility; actual grant and refresh guards remain in force. Recipient-dependent benefits use native `TT_IF_THEY_ACCEPT`. This fixes the reported Shared Administration cost-plus-empty-heading hover. Repeated reward explanations are removed; the only custom modifier formatters are the two Imperia keys lacking native MD formatters. Short duration notices remain where needed.

Buildings use native workers and power. The two capital focuses charge their full cost and commission their buildings on completion; other queued projects still require ordinary construction. Starting armies, fleets, aircraft and equipment remain deferred as requested.

## Agreements and implementation choices

Foreign partners control acceptance. Numeric costs/rewards use native MD option effects. GDP offers freeze their price; current authority, funds, recipient and event round are checked again. Paid courses deliver on successful completion; repeated benefits replace their old carrier.

The procurement concept left the seller's quotation open. The installed initial quotation follows the existing Cold War Gulf contract: **1,000 infantry weapons (1965) for $0.25bn**. Seller quotation, buyer confirmation and actual stock are required. No equipment is created from nothing.

Each agreement/recurring-meeting family has **128 non-reused event rounds**. Exhaustion disables another proposal instead of reusing an old popup's authority. This finite implementation limit is separate from the approved focus layout; normal programme cooldowns still apply.

The Dirham uses the native domestic currency-law system. It grants no international reserve-currency issuer status or artificial exchange strength. GCC/OPEC content uses the existing frameworks; it creates no automatic military faction or war.

## Rebuild and verification

`compile.py` writes only its36 manifest outputs and skips unchanged files. `politics.py` supplies nine bounded shared integrations, recorded with purpose and original/current hashes in `politics_shared_integrations.json`. `economy_start.py` owns two reversible state-history additions and its separate startup helper; the compiler preserves their byte encoding and line endings outside owned markers.

```powershell
python tools/uae_1970/compile.py
python tools/uae_1970/validate.py
python tools/uae_1970/test_focus_runtime.py
python tools/uae_1970/test_politics.py
python tools/uae_1970/test_diplomacy.py
python tools/uae_1970/test_revision.py
python tools/uae_1970/test_presentation.py
python tools/uae_1970/test_start_economy.py --installed
python tools/uae_1970/test_development.py
python tools/uae_1970/test_maritime.py
python tools/uae_1970/audit_layout.py
```

Checks parse emitted scripts, resolve references/artwork, compare installed geometry and native numeric previews with approval, and exercise selected emitted transaction/lifecycle cases. Independent reviews and native-scale proof sheets are in `docs/design/uae_1970/installed/`.

The 18 political regression groups include direct history identity without startup predicates, the guarded native puppet matcher, exact native outlook traits, same-name subtype changes, native inline icons and the actual native Gulf cosmetic callback before/after formation. To inspect the revised history and GFX in HOI4, restart the game and create a new 1970 campaign.

**No live HOI4 load, hover, engine save/reload or multiplayer test has been performed.** Script models/proof sheets are not engine evidence. Native APIs are source-verified; balance remains the approved proposal.
