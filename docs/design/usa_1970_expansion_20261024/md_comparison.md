IMPERIA COLD WAR: USA 1970 and original Millennium Dawn comparison

Date: 24 October 2026. Scope: read-only source comparison for a proposed US expansion. No runtime changes or HOI4 playtests were performed for this report.

## Sources and provenance

The actual original Millennium Dawn reference is the installed workshop donor, not the modified `05_usa.txt` inside this Cold War checkout.

- Donor root: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`.
- Donor descriptor: `descriptor.mod:1`, version `2.0.2`, supported HOI4 version `1.19.*`, workshop item `2777392649`.
- Original focus file: `common/national_focus/05_usa.txt`, modified 3 October 2026 in this local installation.
- Original focus SHA256: `D6B28C5954D342B61BDE498A98A32F3D57CDD0F45D30F89D70FB272EB19C0301`.
- Original English text: `localisation/english/MD_focus_USA_l_english.yml`.
- Original first-line credits: Writers and Coders `Luigi IV#8053`; Junior Coders `Maki#0677`.
- Separate redistribution licence or permission for the source content: unknown in this inspection. Existing author credits remain applicable; the project marker does not establish ownership.
- Current Cold War focus file: `C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/national_focus/USA_1970.txt`.
- Current SHA256 at inspection: `479D4979B1B7574AC8F58E2943505DDC432DE1E563429C837E276D0E585C8DA8`.
- Local retained modern `common/national_focus/05_usa.txt` SHA256: `D9F710DC20CC06F76AEE8FB35ED30205545CEB5EEEB3AE94D364D181C2DD7212`. Its country-selection block differs from original MD, so it is not the comparison baseline.
- `original_inventory.json` is a structural extraction of all 776 original focuses, original names and descriptions, prerequisite groups, exclusions, icons, rewards, raw source blocks and recursively resolved base coordinates. No source file was edited. Its provenance record includes the English localisation hash.

All source-line references below are one-based and refer to the inspected files. Donor references are relative to the donor root; Cold War references are explicitly identified.

## Scale and section coverage

The original tree contains 776 focuses; the current 1970 tree contains 229. Both contain 28 unique mutually exclusive focus pairs. A three-way exclusive fork contributes three pairs, so pair counts are not equivalent to counts of player choices.

| Current US 1970 section | Focuses |
|---|---:|
| Nixon first administration | 50 |
| Election programmes 1972 to 1996 | 113 |
| General economy | 12 |
| Energy | 9 |
| General foreign policy, including Bahrain | 12 |
| Society | 9 |
| Defence | 9 |
| Gulf module | 15 |
| Total | 229 |

| Original MD section | Focuses |
|---|---:|
| Main administrations and economy | 87 |
| Armed services | 79 |
| Foreign policy | 66 |
| Regional economy | 57 |
| Space | 12 |
| Media | 10 |
| Drugs | 11 |
| Crisis | 8 |
| Constitutional reform | 4 |
| Alternative-party programmes | 442 |
| Total | 776 |

The original's headline count is unsuitable as a numerical expansion target. Its 442 alternative-party focuses account for most of the difference. Its most useful transferable strengths are differentiated military procurement, regional assets and continuation after a substantive choice. The original military section starts at `05_usa.txt:4779`, foreign policy at `:8683`, regional economy at `:11230`, space at `:15209`, media at `:15802`, drugs at `:16307`, crisis at `:16765`, constitutional reform at `:17205`, and alternative parties at `:17408`.

Sixteen of the current tree's 28 exclusive pairs occur in the first Nixon programme. None are explicit exclusions inside the 113 later election nodes. This is a structural observation; governing-party and election gates still constrain reachability.

## Reward variety already present

The current tree already contains meaningful asset grants. More factories alone would not solve its depth problem.

| Direct reward syntax in a focus | Current 1970 | Original MD |
|---|---:|---:|
| Building construction | 51 | 62 |
| Treasury transactions | 145 | 106 |
| Political-power changes | 52 | 41 |
| Stability changes | 82 | 43 |
| Permanent idea add/swap | 0 | 94 |
| Timed idea grant | 1 | 2 |

These are counts of focuses containing a named native command directly in their completion-reward syntax. They are not counts of buildings or distinct gameplay systems, and they exclude transitive scripted effects and dynamic-modifier helpers. There are 135 direct building-construction commands in the current tree and 242 in the original. A focus may contain multiple grants or mutually conditional branches. Zero direct permanent-idea commands does not mean that current scripted helpers never grant a spirit.

The useful direction is stronger route identity: durable institutions, limited specialist rewards, meaningful budget choices, and complete bilateral terms. Balance must consider reachable routes, active starting spirits, government-bound programmes and mutually incompatible choices together.

## Concrete original MD benchmarks

### Military scale versus professional quality

Original `USA_focus_five_star_folly`, `05_usa.txt:4921`, and `USA_focus_gold_star_program`, `:5421`, form an exclusive pair. Both cost 8.6 focus units.

| Effect | Five Star Folly | Gold Star Program |
|---|---:|---:|
| Personnel cost modifier | -10% | +4% |
| Education cost modifier | 0 | +7% |
| Daily army experience | +0.01 | +0.03 |
| Leader experience gain | -4% | +8% |
| Army training time | -8% | +8% |
| Army unit experience gain | +3% | 0 |
| Reconnaissance | 0 | +3% |
| Army organisation regain | 0 | -4% |
| Army attack | -3% | +3% |
| Army defence | -3% | +2% |
| Military-factory construction speed | +5% | +10% |

These are actual changes to the USA variable-based dynamic modifiers. Consumers are in donor `common/dynamic_modifiers/99_USA_dynamic_modifiers.txt:22` for military-factory construction, `:71` for daily army XP, `:82` for attack, `:85` for training time and `:113` for personnel cost. The explicit contrast between scale, training, professional capability and expenditure is reusable. The complete numerical bundle is a benchmark, not a proposed 1970 reward.

Other original specialisation examples include frigates versus corvettes at `05_usa.txt:6319` and `:6363`, and carriers versus gunships at `:6742` and `:6789`. Names, technology context, reachable stacking and historical procurement precedents must be adapted for 1970.

### Regional industrial renewal

Original `USA_focus_from_rust_to_refined`, `05_usa.txt:13311`, costs 4.3 focus units and requires congressional support.

- One civilian factory and one extra shared slot in each of states 775, 776 and 778.
- Treasury change -30 in native MD money units.
- Economic regulation change +3, Wall Street opinion -1, small congressional opposition and party-popularity effects.
- An AI staffing guard appears at `:13379`.

This is a clear pattern for named regional development. Proposed Great Lakes renewal, Appalachian development, Gulf ports or aerospace corridors should have identifiable local assets and different policy consequences. Reuse of the pattern does not establish current ownership, control, capacity or the affordability of a proposed 1970 grant. Those require separate verification.

### Three diplomatic doctrines

The original doctrine focuses cost 6.5 units and are mutually exclusive:

| Original focus | Concrete direct rewards |
|---|---|
| `USA_focus_the_salesman_approach`, `05_usa.txt:8800` | War support -4 percentage points; stability +4 points; PP +50; offensive foreign influence +1% |
| `USA_focus_the_humanitarian_approach`, `:8954` | War support +2 points; stability +2 points; PP +100; offensive foreign influence +1% |
| `USA_focus_the_interventionist_will`, `:9086` | War support +4 points; stability -4 points; PP +50; drift defence -5%; offensive foreign influence +1% |

The current tree already adapts this architecture. Another similar top-level fork would add little. Meaningful expansion should vary the commitment, budget and diplomatic offer, while retaining cooperation with multiple regions.

Original state visits can change domestic and economic variables as well as opinions. The UK state visit, `05_usa.txt:9154`, grants PP gain +5%, offensive foreign influence +1%, influence defence +1%, resource export return +5%, market resources -3% and mutual improved-trade opinion. This is an existing mechanical reward bundle, not a sufficient representation of a consensual bilateral agreement.

### Original recipient response example and its limits

Donor `events/United States.txt:18455`, `USA_foreign_event.1`, is a triggered acceptance/refusal offer to Sierra Leone following `USA_focus_supplying_our_sierra_leone`.

- Acceptance creates 1,000 infantry weapons, 100 command-and-control equipment and 50 utility vehicles for Sierra Leone, costs its treasury 2 units and changes party popularity.
- A later USA acknowledgement at `:18521` grants treasury +5 and PP +50, plus political effects.
- Refusal sends an acknowledgement event. The listed recipient refusal rewards at `:18510` are inside `effect_tooltip`, so that block is a display preview rather than executable rewards.
- This example does not establish a paired standing-spirit lifecycle, symmetric suspension, renewal behaviour or conservation of transferred equipment.

It shows that recipient interaction is native MD practice. New Cold War offers should use current project consent and guarded transaction patterns rather than copying this old event wholesale. Their locked focus inspectors must show both countries' full prospective numeric terms.

### Space-funding choices are not automatically well differentiated

Original `USA_finance_nasa`, `05_usa.txt:15230`, and `USA_finance_private_space_ventures`, `:15268`, each cost 10 focus units and treasury 200.

- Both immediately swap `continued_space_efforts` for the same `continued_space_efforts2` idea.
- NASA additionally gives PP +150.
- The actual research-speed values are +2% for the first idea and +3% for the second, in donor `common/ideas/united_states.txt:65` and `:72`.
- Different custom tooltips and later conditional continuations do not make the immediate spirit rewards different.

This is a useful caution against treating every original MD choice as a proven balance model. Space Force, private commercial-space expansion, asteroid mining, Mars and lunar-outpost content should not be imported directly into 1970. New US space rewards must integrate with the existing Cold War space programme and avoid duplicate progression.

## Current diplomatic structure to reconsider

In Cold War `common/national_focus/USA_1970.txt:6011`, `USA_1970_F4`, The Atlantic Bargain, requires F1 or F2. Choosing F3, The Interventionist Will, therefore excludes this Atlantic continuation. A proposed expansion should allow NATO engagement under all three doctrines, with different priorities or terms.

The current F7, F8 and F9 choices at `:6073`, `:6102` and `:6131` make Israeli security assistance, mediation and Arab trade/energy entirely exclusive. A more nuanced RP structure would attach exclusion to a specific scarce funding commitment or mediation mandate. General trade, communication and diplomatic relationships need not all be mutually exclusive.

This is a design recommendation rather than a syntax defect. The existing choices should not be silently removed during a layout-only change.

## Transferable expansion priorities

1. Develop Army, Navy, Air Force and joint-command programmes with different procurement and operational choices.
2. Expand named regional industrial and transport programmes with local assets, sector productivity, employment or energy consequences.
3. Give selected post-1972 party programmes consequential internal priorities and distinct follow-through instead of applying the same branch template everywhere.
4. Keep geographic diplomacy broadly reachable. Use doctrine and budgets to shape offers rather than block an entire partner region.
5. Retain the existing US machinery: Congress, Wall Street, federal budgets, regulation and native USA dynamic modifiers. The project API bridge exposes general-staff and army helpers, including Cold War `common/scripted_effects/mdcw_1970_USA_native_api_bridge.txt:250`, `:340` and `:358`.
6. Prioritise complete consent-based agreements with named recipient countries, paired spirits, exact weekly monetary costs and explicit duration. A historical institutional precedent and a balance proposal are separate evidence categories.

## Evidence boundaries

Counts were computed from complete parsed `focus_tree` blocks using the repository's read-only Clausewitz parser functions. The original inventory resolves all 776 relative-coordinate chains: there are no missing or forward relative anchors and no conditional `offset` blocks in the inspected donor. The inventory retains availability and branch-hiding conditions; it does not evaluate every government or election state.

Source inspection establishes structure and declared effects. It does not prove HOI4 tooltip rendering, AI behaviour, actual focus timing, modifier efficacy, native building limits or multiplayer stability. No new historical policy is justified solely by resemblance to a modern MD focus.
