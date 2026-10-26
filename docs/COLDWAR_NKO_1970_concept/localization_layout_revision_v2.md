# DPRK 1970 concept: localization and layout revision v2

This is a prose and geometry proposal for the current 167-focus concept. It adds ten shared foreign-relations focuses and an eight-focus alternate-history war route against South Korea, for a projected total of 185 focuses. No canonical JSON, build script, game localization, or loaded game file was changed.

## Native MD localization profile

The best match for the requested clean player-facing style is a short, specific title followed by one or two sentences that explain the historical stakes. Keep costs, requirements, and modifier values in the ordinary focus tooltip. The description should not restate those effects or mention scripts, flags, variables, country-routing, acceptance triggers, or other implementation details. For a diplomatic offer, describe the proposal and its trade-off; present acceptance and refusal as neutral recipient choices.

The installed MD NKO localization provides a useful warning and a useful subject range. `MD_focus_NKO_l_english.yml:153–171` repeats almost the same two-sentence “trade agreements” description for Vietnam, China, Egypt, Syria, Iraq, Iran, Venezuela, Brazil, and Indonesia. New focuses should identify the actual relationship and its stakes instead of repeating that template. The same file’s `NKO_arms_export` material at lines 1834–1875 mixes a good institutional title with long explanatory text, UI instructions, thresholds, and tooltip prose; those details belong in tooltips or interface hints, not focus descriptions. For comparable Korea policy, see `MD_focus_SOV_l_english.yml:427–450`: it supplies specific subjects (status quo, North-South talks, reunification, military support) but several descriptions turn into broad political commentary. Keep the subject specificity and trim the commentary.

For diplomacy and reunification precedents, the donor’s `events/Korea.txt:1131–1622` presents a recipient-controlled proposal with acceptance and refusal, followed by separate response events at lines 1624 and 1659. The matching `events_l_english.yml:983–989` explains the offer and its result. Its refusal text is accusatory and longer than needed; a cleaner version should simply state that the proposal was declined and that talks remain open or have ended. This fits the concept’s existing rule that each international agreement receives a decision from its recipient, while keeping ordinary focus text narrative-only. The existing trade-decision block is `common/decisions/05_north_korea.txt:2612–2773`; its country-specific decision names are localized alongside the focus keys at `MD_focus_NKO_l_english.yml:153–171`.

Use the event description to state what was offered, then let the recipient’s options carry the decision. For example: “Pyongyang has proposed a new supply and technical agreement. The offer would strengthen cooperation, but its terms may draw us closer to a difficult partner.” Acceptance can read “The agreement is accepted. Our governments will open talks on its terms.” Refusal can read “The offer is declined. Existing channels remain open, but no agreement has been reached.” Keep numeric effects in the option tooltips. This is a style sample, not final event localization.

### Proposed shared foreign-relations section — 10 focuses

Proposed root: `(68,1)`, relative to the new section anchor. It hangs from the current `independent_diplomacy` focus at `(44,0)`; its first-row connector occupies the clear gap immediately below the start row. Existing focus bounds are x=2..56 and y=0..25. The new section reaches x=64..72 and y=1..9, with no card or title-box intersections at the native 96×130 px pitch. The geometry check used 165×128 px focus cards and 147×20 px title boxes. Proposed relative offsets are measured from the new root at `(68,1)`.

| Focus key | Display title | Proposed narrative description | Absolute grid / relative offset |
|---|---|---|---|
| `foreign_service` | A Wider Foreign Service | The republic needs missions that can pursue trade, technical exchange and recognition while preserving its freedom of action. | (68,1) / (0,0) |
| `moscow_ties` | Soviet Technical Ties | The 1961 treaty keeps a channel open with Moscow. Engineers and diplomats can build practical cooperation while Pyongyang preserves room to maneuver. | (64,3) / (−4,2) |
| `beijing_protocol` | Repair Ties with Beijing | Border commerce and agricultural deliveries can repair ties strained by recent disputes. Both sides will remain wary of dependence. | (68,3) / (0,2) |
| `hanoi_mission` | Hanoi Mission | Solidarity with Vietnam can deepen Asian cooperation through training, political exchange and support for its war effort. | (72,3) / (+4,2) |
| `eastern_bloc` | Eastern Bloc Machinery | Socialist partners can supply machine tools and technical advice. Repayment will depend on exports the country can sustain. | (64,5) / (−4,4) |
| `chongryon` | Chongryon Channel | Overseas Koreans in Japan provide a bridge for family contact and commerce, despite the absence of formal relations with Tokyo. | (68,5) / (0,4) |
| `arab_partners` | Arab Partnerships | Relations with Cairo and Algiers can widen cooperation beyond the socialist bloc and add new voices to Korea’s diplomatic case. | (72,5) / (+4,4) |
| `nonaligned` | Non-Aligned Outreach | The movement offers Pyongyang a forum beyond the rivalry of Moscow and Beijing. Wider ties can affirm independence without isolation. | (66,7) / (−2,6) |
| `un_korea` | Korea at the UN | Newly independent states are reshaping General Assembly debates. Pyongyang can seek support for Korean representation while accepting that partners will weigh each issue on its merits. | (70,7) / (+2,6) |
| `wider_ties` | Wider Diplomatic Ties | More embassies and agreements will widen access to trade and technical cooperation. New partners can strengthen the republic’s standing without ending dependence on larger states. | (68,9) / (0,8) |

Suggested connector structure: the new root follows `independent_diplomacy`; its three contacts with Moscow, Beijing, and Hanoi are alternatives available in parallel; the machinery, Chongryon, and Arab contacts extend those links; the Non-Aligned and UN focuses then combine before the capstone. The Non-Aligned focus should reflect the DPRK’s 1975 membership rather than imply that this status existed at the January 1970 start.

### Proposed Korean war route — 8 focuses

Add this as a hard-line branch inside “Patrons and the Korean Question,” below the existing diplomacy tree. All eight focuses are explicitly alternate history: the armistice held in 1970, and the concept’s research memo describes peaceful talks and later military confrontation as competing directions. The route begins from `external_resilience` at `(44,9)` and uses the current diplomacy group root `(44,0)` for relative positioning. It reaches x=48..52 and y=10..16, staying clear of the conditional-programme row at y=17.

| Focus key | Display title | Proposed narrative description | Absolute grid / relative offset |
|---|---|---|---|
| `second_campaign` | The Second Campaign | The armistice has frozen the front but left reunification unresolved. A renewed offensive would demand political backing and a costly concentration of forces. | (50,10) / (+6,10) |
| `southern_defences` | Map Southern Defenses | Reconnaissance of roads, depots and defensive positions would shape any advance south of the armistice line. | (48,12) / (+4,12) |
| `beijing_assurances` | Beijing Assurances | A renewed war could draw China across the Yalu. Pyongyang must learn Beijing’s position before risking a second intervention. | (52,12) / (+8,12) |
| `reserve_callup` | Call Up the Reserves | Reserves will reinforce the front, drawing skilled workers away from factories and fields. | (48,13) / (+4,13) |
| `artillery_concentration` | Artillery Concentration | Forward batteries can strike defensive positions, but their movement will be difficult to conceal. | (52,13) / (+8,13) |
| `general_mobilization` | General Mobilization | The whole state will be placed on a war footing. This decision will close the remaining space for negotiation. | (50,14) / (+6,14) |
| `cross_38th_parallel` | Cross the 38th Parallel | The Korean People’s Army begins a renewed offensive south. The armistice is over, and foreign intervention is likely. | (50,15) / (+6,15) |
| `claim_korean_authority` | Claim Korean Authority | Victory would not settle who governs the peninsula. Pyongyang must present a political settlement to a divided people. | (50,16) / (+6,16) |

Suggested sequence: the campaign opens onto two planning lines, reconnaissance and a recipient-controlled request for Beijing’s position. The next row mobilizes reserves and concentrates artillery; both feed General Mobilization, then the crossing and a political claim. The Beijing response should be a genuine negotiation with a clear acceptance or refusal. Refusal should not silently create support, funds, or a guarantee; it should leave a visible diplomatic consequence and a reachable choice for the NKO player. The final focus should not grant annexation or forced faction membership by description alone.

### Title-width check

All 18 proposed titles were measured with the installed game’s `hoi_16mbs.fnt` glyph advances. Every title is supported and fits the 147 px focus-name field; the maximum is 140 px (`A Wider Foreign Service`, `Repair Ties with Beijing`, and `Claim Korean Authority`). This is a glyph-width check, not a claim about browser rendering or every display scale.

## Icons and world-news presentation

Existing NKO goal sprites provide a coherent native war set; all names are already defined in the donor’s `interface/goals.gfx` and can be reused directly:

- `NKO_defence` → `gfx/interface/goals/north_korea/NKO_defence.dds` for the war-route entry and command planning.
- `NKO_38_parallel` → `gfx/interface/goals/north_korea/NKO_38_parallel.dds` for the armistice line and diplomatic end-state.
- `NKO_rebels_in_south` → `gfx/interface/goals/north_korea/NKO_rebels_in_south.dds` for southern-front reconnaissance or agitation.
- `NKO_reserve` → `gfx/interface/goals/north_korea/NKO_reserve.dds` for call-up and mobilization.
- `NKO_koksan` → `gfx/interface/goals/north_korea/NKO_koksan.dds` for artillery concentration.
- `NKO_army` → `gfx/interface/goals/north_korea/NKO_army.dds` for the KPA offensive.
- `NKO_united_finally` → `gfx/interface/goals/north_korea/NKO_united_finally.dds` for the final political claim, if the art is framed as a desired outcome rather than a guaranteed one.

For a world report, follow the native event presentation: a `news_event` with a concise title, a short neutral description, `major = yes` when the event merits world attention, and a single event image. The donor’s existing Korean offensive uses this pattern at `events/War.txt:570–577` (`world_war.5`). The game’s standard event report frame is defined in base `interface/eventwindow.gui:25–109` and `interface/eventwindow.gfx:14–53`; the picture sits inside the report frame and clip. Reuse that frame and let the image carry the scene.

For this route, a restrained title such as “War Resumes in Korea” and a two-sentence report would fit the base-MD news voice: “Fighting has resumed across the Korean armistice line. Governments in the region are assessing the risk of a wider conflict.” Avoid outcome claims in the headline unless the event actually reports that outcome.

I inspected the donor’s likely Korea news images. `GFX_CHI_chinese_soldiers_news` maps at `interface/MD_eventpictures.gfx:2503–2505` to `gfx/event_pictures/asia/china - CHI/CHI_chinese_soldiers_news.dds`; it is a modern Chinese soldier formation and is the picture used by the existing 2020-era regional war. `GFX_NKO_korea_unification` at lines 2939–2941 maps to `NKO_korea_unification.dds`, a modern North-South summit handshake. The latter fits a peace announcement, not a 1970 war. For a 1970 second-war announcement, the cleanest match is a period-appropriate Korean battlefield image in the same native report frame. If no new art is approved, use a neutral peninsula/flag image rather than presenting a modern photo as a 1970 event.

## Source anchors

- Historical basis: `history_research.md:21–23` (Juche as autonomy with continued Soviet and Chinese patronage), lines 35–39 (1972 communiqué and détente), and source note 9 at line 99 (FRUS and NKIDP records). A second war is an explicit alternate-history branch, not a historical forecast.
- Existing diplomacy concept: `COLDWAR_NKO_1970_CONCEPT.md:1028–1200` (patron proposals and diplomacy), and `history_research.md:21–23`.
- Donor focus prose: `localisation/english/MD_focus_NKO_l_english.yml:153–171` (trade-description repetition), `1834–1875` (Foreign Affairs Office mixed with UI/tooltip detail), and `localisation/english/MD_focus_SOV_l_english.yml:427–450` (Korean-policy titles and prose).
- Donor source focuses: `common/national_focus/05_north_korea.txt:1717` and `1761` (Soviet and Chinese trade paths); `common/national_focus/05_russia.txt:20234`, `20446`, and `20887` (North Korea relationship, peaceful reunification, and second-war escalation).
- Recipient and news patterns: `events/Korea.txt:1131–1622`, `1624`, and `1659`; `events_l_english.yml:893–896`, `950–952`, and `983–989`; `events/War.txt:570–577` and `events_l_english.yml:2133–2135`.
- Event presentation: base-game `interface/eventwindow.gui:25–109`, `interface/eventwindow.gfx:14–53`, `interface/eventpictures.gfx:324–326`; donor image registry `interface/MD_eventpictures.gfx:2503–2508` and `2939–2941`.

