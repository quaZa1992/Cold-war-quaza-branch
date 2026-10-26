# Cold War UAE / Trucial States: native MD layout reference

Read-only source audit, 19 October 2026. This records the current installed main Millennium Dawn reference and the existing Cold War UAE starting setup. It is a design reference, not an implemented or engine-tested UAE tree. No loaded game file was changed by this audit.

## Scope and source identity

- Main MD root: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`.
- `descriptor.mod`: version `2.0.2`, supported HOI4 `1.19.*`.
- Main Generic: `common/national_focus/00_generic.txt`, 139,665 bytes, last-write 3 October 2026. SHA-256 `c3f2e55df976b712e423fa906afd18b9e638c838d1cb34a13fb80bfa2ea82ac5`.
- Main Russia: `common/national_focus/05_russia.txt`, 956,238 bytes, last-write 8 October 2026. SHA-256 `db03d72e1fdbc239076eba9f7e9259e1791e909eab425186304cd6b14858b602`.
- Current local `interface/nationalfocusview.gui`, `nationalfocusview.gfx`, `goals.gfx`, and `common/national_focus/00_titlebar_styles.txt` have identical SHA-256 hashes to main MD. Therefore the measurements and native art registrations below apply directly to the Cold War checkout at audit time.
- Direct national-focus declarations were parsed and all relative anchors were recursively resolved. Shared-focus subtrees were excluded from the focus counts/extents below; they require separate host-aware placement if attached to the UAE design.

## Measured reference profile

| Measurement | Generic | Russia |
|---|---:|---:|
| Direct focuses | 158 | 806 |
| Focuses using `relative_position_id` | 150 | 800 |
| Absolute x extent, excluding shared focuses | -13 to 51 | 0 to 235 |
| Absolute y extent | 0 to 10 | 0 to 26 |
| Most frequent same-row nearest-neighbour spacing | 2 units, 101 occurrences | 2 units, 423 occurrences |
| Next common same-row spacing | 3 units, 23 occurrences | 3 units, 108; 4 units, 68 |
| Most common prerequisite displacement | dx 1 / dy 1, 73 edges | dx 1 / dy 1, 434 edges |
| Straight vertical prerequisite displacement | dx 0 / dy 1, 42 edges | dx 0 / dy 1, 268 edges |
| Direct conditional `offset` declarations | 0 | 0 |

These are measurements, not engine spacing limits or a requirement to copy Russia's superpower-sized canvas. Native MD composes small coherent clusters, stable roots, straight spines, one-row policy forks, and midpoint joins. It does not use a uniformly spaced catalogue grid. Two x units provide 192 pixels between centres; a one-unit diagonal changes x by 96 and y by 130.

### Concrete geometry to emulate

All line anchors refer to the current main MD files.

| Pattern | Source | Emitted placement | Resolved placement / interpretation |
|---|---|---|---|
| Section root | Generic `:55–61`, `GENERIC_political_reform` | x -7, y 0, no anchor | (-7, 0); ordinary section anchor |
| Two neighbouring institutional inputs | Generic `:81–90`, `:110–119` | (-4,1), (-2,1), both relative to root | (-11,1), (-9,1); 2-unit spacing |
| AND join midway below inputs | Generic `:139–149`, `GENERIC_political_games` | (-3,2) relative to root | (-10,2); two separate prerequisite blocks mean both inputs |
| Follow-on diamond | Generic `:165–174`, `:198–207`, `:223–235` | inputs (-4,3), (-2,3), join (-3,4) | tight fork and centred merge |
| Binary reciprocal exclusive choice | Generic `:604–651` | centralization (7,2), decentralization (9,2), root-relative | (0,2) versus (2,2); reciprocal exclusivity, both cards visible |
| Government programme entry | Russia `:109–122`, `SOV_putin` | (13,1) relative to Yeltsin root (62,0) | (75,1); actual party gate is `available` |
| Programme spine | Russia `:156–169`, `SOV_the_grand_bargain` | (0,1) relative to Putin | (75,2) |
| Three-column policy row | Russia `:187–235`, `:279–295` | x -2,0,+2 / y2, Putin-relative | (73,3), (75,3), (77,3) |
| Two-input centred join | Russia `:320–330`, `SOV_young_guard` | (-1,3), Putin-relative | (74,4), between the (73,3) and (75,3) inputs |
| Three mutually exclusive settlements | Russia `:553–664` | oligarchic x -1, mixed x1, corporatist x3 / y7 | (74,8), (76,8), (78,8); 2-unit rhythm |
| OR continuation from alternatives | Russia `:697–710` | x3,y8 relative Putin | (78,9); one prerequisite block contains corporatist OR mixed |
| Wide branch roots around one political anchor | Russia `:4223`, `:4837`, `:12139` | western x -35, nationalist x31, communist x -52 / y1, Yeltsin-relative | x27,93,10 at y1; entire subtree footprints determine spacing |
| Economic section anchor | Russia `:31846–31853` | x90,y0 relative to Yeltsin | (152,0); a positioning anchor need not be a prerequisite |

### Costs and nominal durations

Base-game `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/common/defines/00_defines.lua:3598–3599` defines `FOCUS_POINT_DAYS = 7`; neither checked MD defines file overrides it. Nominal durations below exclude saved progress and gameplay modifiers.

- Russia: cost3 = 21 days, 314 focuses; cost5 = 35 days, 216; cost7 = 49 days, 168. Cost1/2 entries provide 7/14-day setup and transition moments. The audited file has only one cost10 focus.
- Generic: cost10 = 70 days, 103 focuses; cost7.86 = 55.02 nominal days, 29; cost8.6 = 60.2 days, 10; cost5 = 35 days, 9. The decimal native costs should not be reinterpreted as a new day conversion.
- For a deep UAE concept, Russia's 21/35/49-day rhythm is the closer depth reference. Use short political entries only when a real action and reward justify them; substantial infrastructure and institutional reform can use 49/70 days. Do not add empty positioning focuses.

## Native GUI and art closure

`interface/nationalfocusview.gui`:

- `:446–449`: `national_focus_item` is 165×128 pixels with clipping off.
- `:467–473`: actual icon is the `symbol` button, x5/y-44, centred. Icons are not restricted to a fabricated uniform 72-pixel square.
- `:487–495`: title at x15/y58, font `hoi_16mbs`, max width147 and max height20, centred. Long English titles need a short displayed label and full inspector title, not resized global UI.
- `:574–575`: native grid spacing x96/y130.
- `:590–595`: engine connector endpoints are `link_begin` (80,64) and `link_end` (80,0). External connector paths remain approximations until checked in HOI4.
- `:537–570`, `:598–607`: exclusivity uses native line sprites plus centre mark, with exclusive offsets and a two-unit positioning interval. It is not a prerequisite arrow.

`common/national_focus/00_titlebar_styles.txt:1–9` selects default unavailable/completed/available/current states. The corresponding registrations in `interface/nationalfocusview.gfx` are:

| State | Sprite / source line | Texture |
|---|---|---|
| Unavailable | `GFX_focus_unavailable`, `:132–133` | `gfx/interface/focusview/titlebar/focus_unavailable_bg.dds` |
| Available | `GFX_focus_can_start`, `:136–137` | `gfx/interface/focusview/titlebar/focus_can_start_bg.dds` |
| Current | `GFX_focus_current`, `:153–184` | available texture plus native ongoing masks/animated texture |
| Completed | `GFX_focus_completed`, `:188–206` | `gfx/interface/focusview/titlebar/focus_completed_bg.dds` plus native completion animation |

The exact bitmap font atlas and glyph metrics are available at `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/gfx/fonts/hoi_16mbs.fnt` and `.dds`. The FNT header identifies Ubuntu Bold, size16, lineHeight16. A browser using the decoded atlas can reproduce these labels; generic browser typography is an approximation. Native animated current/completion effects remain an external-preview limitation.

### Visually reviewed reusable icon set

These exact `icon` sprite names and texture files exist in both main MD and the local Cold War checkout. Twenty were opened together at native texture size; their motifs contain no foreign national flags. The additional water/education/airport/Arab League choices have source closure; they still need selection-specific texture review in the final render. Prefix all newly registered UAE aliases `GFX_COLDWAR_UAE_…`; existing sprites can also be referenced directly.

| Exact sprite | Texture relative to `gfx/interface/goals/` | Main `interface/goals.gfx` line | Suitable theme |
|---|---|---:|---|
| `government_beu` | `00_politics/government_beu.dds` | 9133 | Federal administration |
| `Election_graphics` | `00_politics/Election_graphics.dds` | 8697 | Representation / constitutional choices |
| `monarchism_constitution` | `00_ideology/monarchy/monarchism_constitution.dds` | 7881 | Rulers' constitutional compact |
| `centralization` | `00_economy/centralization.dds` | 4821 | Federal authority |
| `decentralized_economy` | `00_economy/decentralized_economy.dds` | 5441 | Emirate autonomy |
| `oil_companies` | `00_energy_resources/oil_companies.dds` | 6421 | Oil concessions / ADNOC |
| `oil_production2` | `00_energy_resources/oil_production2.dds` | 6433 | Oil and gas processing |
| `resource_extraction` | `00_energy_resources/resource_extraction.dds` | 6465 | Resource development |
| `construction_engineering` | `00_economy/construction_engineering.dds` | 5413 | Ports / urban construction |
| `generic_healthcare` | `00_economy/generic_healthcare.dds` | 5853 | Clinics / public health |
| `scientific_exchange` | `00_science/scientific_exchange.dds` | 10753 | Foreign educational assistance |
| `national_grid` | `00_energy_resources/national_grid.dds` | 6385 | Electricity and utilities |
| `global_community` | `00_regions/global_community.dds` | 9829 | International admission |
| `treaty2` | `00_diplomacy/treaty2.dds` | 4449 | Treaties / agreements |
| `neutrality` | `00_ideology/neutrality.dds` | 7917 | Independent foreign policy |
| `navy2` | `00_navy/navy2.dds` | 8393 | Coastal force |
| `sunni_government` | `00_religion/sunni_government.dds` | 10489 | Historically relevant Sunni institutions |
| `union_negotiations` | `00_economy/union_negotiations.dds` | 6221 | Labour protection / bargaining |
| `liberalization` | `00_trade/liberalization.dds` | 11149 | Trading hub |
| `economic_water_supply` | `00_economy/economic_water_supply.dds` | 5561 | Water infrastructure |
| `desalination_plants` | `yemen/desalination_plants.dds` | 40806 | Desalination |
| `focus_generic_education` | `00_science/focus_generic_education.dds` | 10605 | Schools / university |
| `build_airport` | `00_economy/build_airport.dds` | 4797 | Civil aviation |
| `align_to_arab_league` | `00_align/align_to_arab_league.dds` | 433 | Arab diplomacy |

The exact sprite `generic_airport_icon` exists but visually depicts a modern bridge/transport emblem. Prefer `build_airport` for the UAE aviation programme. Filenames alone do not establish visual suitability. Native Generic source `:56` uses `Election_graphics` directly rather than assuming every main-MD sprite has a `GFX_goal_` prefix. New aliases and matching shine need their actual registered contracts; ideas use their separate `GFX_idea_<picture>` convention.

## Party gating and stable geometry

Russia has 724 direct `available` declarations and only two `allow_branch` declarations. Putin entry `:122`, subsequent `:169` and many descendants check `emerging_reactionaries_are_in_power = yes`. These make a focus eligible under the ruling subparty; they do not demonstrate dynamic branch hiding or automatic programme suspension. Political branches reserve their full space even when unavailable.

The checked `allow_branch` precedents instead concern DLC (`Generic :417`, Russia `:24527`), Sunni/global-rule eligibility (`Generic :863–868`), or a persistent Duma flag (`Russia :30781`). They are not proof that it is safe to hide and show the same earned tree on every government change. For the UAE design, retain fixed geometry and show inactive party branches locked; govern programme spirit suspension/restoration separately through verified party-change support. A change of government must not regrant buildings, money, manpower, resources or one-time reform rewards.

Grouped prerequisites must survive design, preview and emission unchanged. Multiple prerequisite blocks are AND; multiple `focus` entries inside one block are OR. The three-way Russian settlement has OR continuation at `:706–709`, not an impossible AND of mutually exclusive parents. `available` may carry a cross-section gate without drawing a long line; using it must be an explicit readability decision rather than silently dropping dependencies.

## Reward and presentation grammar to carry into the concept

The companion mechanics audit should calibrate each UAE value to its 1970 economy and validate providers; these source examples show native bundle and tooltip presentation:

- Russia `SOV_stabilisation_fund`, `:297–304`: native `unlock_decision_tooltip`, named idea, treasury -155 via `modify_treasury_effect`, further programme support. This is a 35-day focus; -155 is a Russian 2000-era amount, not a UAE recommendation.
- Russia `SOV_oligarchic_republic`, `:628–639`: conditional native `swap_ideas`, corruption increase, oligarch opinion +10. Exclusive policies can combine institutional gains and realistic political costs.
- Russia `SOV_outer_space_initiative`, `:31900–31906`: named dynamic-modifier heading and exact native formatter rows; research speed +3%, education cost +5%, plus decision unlock. This directly demonstrates a positive programme modifier with a plausible ongoing cost.
- Russia `SOV_economic_russian`, `:31857–31870`: state-scoped four-factory bundle and treasury -34, native building and financial effects.
- Generic `GENERIC_light_industry_investments`, `:2826–2840`: treasury -7.5, capital building slot +1, instant civilian factory +1, queued fossil plant +1; staffing/bankruptcy influence AI behaviour. A meaningful economic focus can alter actual structures as well as its spirit.
- Generic `GENERIC_decentralization`, `:618–627`: named idea plus a conditional GDP-based cost. `centralization` is the reciprocal excluded alternative at `:641–657`.

Use native named/numeric rewards in the inspector and eventual tooltips. Descriptions should explain the UAE institution, conflict and policy stakes in English. They should not narrate variable bookkeeping, invoices or authoring commands. Agreement-event options should show exact native numeric costs/rewards while the event description stays short.

## Existing Cold War UAE and preview tools

`history/countries/UAE - United Arab Emirates.txt:4–23` currently supplies a 1970 conditional snapshot, loads `mdcw_1970_generic_focus`, sets GDP per capita2.394 and productivity582.800, applies `IMP_1970_profile_monarchist`, uses `UAE_TRUCIAL_1970`, recruits `UAE_MDCW_1970_incumbent`, and follows the existing temporary empty land/naval/air OOB decision. A new concept should not silently replace these systems or fabricate a loaded UAE tree. Starting leaders/party mappings must be checked against their actual character/profile providers by the history/mechanics audit.

Relevant existing tools were read for reuse only:

- `tools/israel_1970/render_preview.py`: renders from canonical design data but has a hardcoded output path and executes writes at import/top level; do not run against UAE.
- `tools/israel_1970/focus_art.py`: art registration and contact-sheet examples; its `register` function writes GFX/shine assets and may convert PNG art. Do not invoke during the concept phase.
- `docs/design/vietnam_impact_audit_2026_10_19/build_preview.py`: native atlas label and card proof-sheet technique; hardcoded Vietnam source hashes and output path make it a reference, not a generic UAE validator.
- `tools/iraq_1970_concept/verify_preview.cjs`: available browser-verification precedent. Read side effects and parameterization before reuse; no generic correctness claim follows from its existence.

## Recommended UAE geometry and approval boundary

For roughly 180 proposed focuses, fifteen compact programme clusters in three tiers are reasonable if the complete footprint is reserved. Use local root anchors and 2-unit same-row spacing; wider alternatives use 4-unit separation where the intervening subtrees need it. Keep most prerequisite edges one row deep with straight or one-unit diagonal joins. Vary topology by programme: institutional diamond, two-column policy competition, three-column delivery, and separate diplomatic/defence spines. Do not repeat an identical fork template for every cluster.

The approval preview should use the exact coordinates from one canonical manifest and show all locked alternatives. Each focus must be clickable, with English title, nominal duration, grouped prerequisites, exclusions, government gate, exact benefits, costs and ownership semantics. Preserve the actual native grid, titlebar, glyph atlas and icon dimensions. The full overview supplies navigation; normal-scale adjacent branch views prove card/title fit. Use shortcuts for independence/federation, governing programmes, oil/development, society, defence and Gulf diplomacy. Initial camera should show the January1970 problem and formation programme, not the centre of the entire canvas. Place continuous focuses in genuinely empty space after checking the whole visible tree.

The user's approval is reserved. Keep all concept JSON, diagrams, HTML, static proof sheets, proposed code and reports under design/visualization paths. Do not write national focuses, ideas, decisions, localisation, on-actions, character/history changes or generated GFX into loaded paths until the concept is accepted.

## Verification limits

Source structure, direct focus coordinates, native GUI dimensions, resource existence, font metrics, titlebar mappings and the twenty-icon contact sheet were inspected. This audit does not certify engine connector routing, focus hover rendering, title truncation, dynamic focus visibility, shader animation, complete shared-focus footprints, or the future UAE node geometry. Those require the actual concept render followed by an independent review, and eventually an HOI4 check after implementation is authorized.
