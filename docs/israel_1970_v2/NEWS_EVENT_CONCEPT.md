IMPERIA COLD WAR: Israel occupation events and world news

30 October 2026. Design extension to [the occupation concept](OCCUPATION_SYSTEM_CONCEPT.md). The event rules remain a proposal. The user subsequently selected **World Ledger** as the common native world-news presentation. Its interface and the registered colour settler illustration are separate from the proposed event system. See [the artwork notice](../../tools/world_news_skin/NOTICE.md). Event thresholds, costs and durations below remain proposed balance. The installed focus tree is unchanged.

## Presentation and authorship

Use normal country events for Israeli operational reports and responses, and native world-news events for developments of international significance. Keep the ordinary occupation Decision menu. No additional occupation dashboard is proposed.

The user rejected MD's BNN artwork and, after several detailed concepts, approved **World Ledger** exactly as shown. Its neutral paper, serif masthead, double rules, framed colour picture and layered shadows replace the earlier World Dispatch appearance. Only ordinary `EventWindow_News` is adapted. Actual headlines, pictures, reports and options remain native, with separate news-local serif fonts. Country-event frames, shared option entries and gameplay scripts remain unchanged. Fabricated date/location fields and visible image captions are excluded. The earlier two-column and Agency Print previews are superseded concepts. Browser compositions and private native tests are identified separately in the artwork records.

The inherited window was inspected in full at `interface/eventwindow.gui`, including its adjacent options. It is 528 x 595; its photo and overlay begin at x59/y91, with a 399 x 155 overlay. Its title starts at x35/y253 with width444/height32; the description starts at absolute x52/y296 with width405/height210. The options grid and its 352 x 48 entry were also inspected. Sprite definitions are inherited from the installed engine's `interface/eventwindow.gfx`. These are donor facts, not dimensions of an already integrated redesign. The country-event 217 x 163 frame is a different asset and must be checked separately when local event artwork is implemented.

All selected photographs are colourized archival derivatives, labelled as such. Colour is a reconstruction, not evidence of original uniform, clothing or object colour. An ordinary market photograph must never be captioned as the victims, perpetrators or aftermath of a fictional incident. Original English event prose below is written for alternate-history gameplay; none of the drafts is a quotation or a claim that its fictional occurrence happened historically.

## Publication rules

Local reports follow actual completed actions or committed incidents. They do not generate incidents by being opened. Serious world news reports the resulting facts. A raid may produce a local report without a world report, and successful civilian investment can also produce news.

| Proposed family | Trigger for a world report | Frequency and recipient |
|---|---|---|
| W1: New military-agricultural outpost | First completed Nahal project in an occupied region, actual residents and assets present | Once per region. All extant countries |
| W2: Settlement expansion | At least three completed cohorts and at least 1,500 actual surviving residents in a region | First threshold crossing only. All extant countries |
| W3: Major attack on Israeli personnel | Recorded exceptional personnel-loss episode, or a fatal attack meeting the major-incident threshold | Proposed regional 26-week family cooldown. All extant countries |
| W4: Civilian deaths in an Israeli operation | Actual raid-caused civilian fatalities plus a major incident, or repeated linked civilian-harm incidents | Proposed regional 26-week family cooldown. All extant countries |
| W5: Settler violence | Actual settler-perpetrated serious incident against local residents | Requires resident presence and the actual incident. Proposed regional 26-week family cooldown. All extant countries |
| W6: Sustained freeze | Two consecutive paid 13-week freezes, no intervening arrival or approval in the covered region | Once per maintained freeze episode, not every renewal. All extant countries |
| W7: Completed evacuation | At least one actual surviving cohort has been returned; the named site is actually closed | First qualifying regional evacuation, later only a substantial new closure. All extant countries |
| W8: Civilian administration investment | At least 26 continuous funded weeks, a completed civilian project and an actual service improvement | Once per regional programme milestone. All extant countries |
| W9: Domestic incorporation | Final core transaction actually completes after every long-term requirement | Once per actual state's first incorporation. All extant countries |

For tuning, a major incident can initially mean at least 50 game military manpower lost in one committed episode, at least three actual civilian fatalities, or two linked fatal civilian incidents within 26 weeks. These are independent eligibility tests, not a conversion of manpower into deaths. They are proposed publication thresholds, not historical frequency estimates. Local reports still cover smaller incidents. Do not reward the player for reaching a casualty threshold.

Routine milestone publications have a country-wide eight-week interval; a pending older milestone can be included in the next report rather than becoming stale breaking news. A major fatal incident can bypass that routine interval, but not its own duplicate receipt. Merge reports arising from the same incident into one truthful account; do not independently broadcast an attack, response raid and its civilian harm as three headlines about the same episode. A raid result after a previously reported attack is a new episode only when it actually occurs later. Keep at most one queued routine milestone and one bounded quarterly local summary per region. Do not build an unbounded news queue.

World-news acknowledgement options have no gameplay effects. Foreign players decide their response. No automatic war, sanctions, UN resolution, recognition, diplomatic statement, territorial handover, election result or Palestinian acceptance is attached. Palestinian existence is unnecessary for local residents to suffer an incident. Where Palestine or another host country exists and has actual local assets or population, its own report can show the consequences already applied by the mechanic; it has no veto over Israel's unilateral settlement action.

The future execution must store incident state, actor, date, outcome, casualty categories and response separately from later controller changes. Commit losses and invoices once before sending the local response. All spectators receive the same committed event snapshot. Israel must not be charged again when a foreign observer acknowledges the news. A military reserve deduction is not a verified fatality count. If only personnel loss is known, use `losses` or `casualties`, never an invented killed/wounded breakdown. The final text branch must match the actual result, any completed investigation and any genuine admission or denial. No invented quotation or automatic statement by a human-controlled foreign government.

Use synchronized native simulation outcomes and persistent publication receipts across reload/rehost. Send reports from the actual transaction and the existing monthly occupation update. No world-wide daily polling, additional incident rolls or checks driven by an open newspaper window are necessary. These are design choices, not measured multiplayer performance results.

## World-news drafts

`{STATE}`, `{TERRITORY}` and `{ACTOR}` below are editorial placeholders, not verified HOI4 getter syntax. The implementation must resolve the stored event scope and use tested native localisation tokens. The concrete preview cases use Sinai and West Bank to avoid unresolved display tokens.

### W1. New Israeli Outpost Established

The Israeli military administration has completed a new military-agricultural outpost in {STATE}. Its first residents have arrived under the Nahal programme, combining army service with the establishment of an agricultural community.

The outpost extends Israel's presence in occupied territory and adds another settlement to the military administration's protection duties. Cultivation, supply and access now require continuing expenditure. Its establishment changes the situation on the ground while leaving the territory's wider political future unresolved.

Acknowledgement: `A new commitment.`

Use only for an actual Nahal project. A residential or workshop cohort uses W2, never a fictional military founding ceremony. The 1969 Nahal Yam photograph is suitable for the concrete Sinai example, with an archival caption.

### W2. Israeli Settlement Expansion

Successive groups of Israeli residents have moved into settlements in {STATE}, following approvals and construction by the authorities. The latest arrivals mark a substantial expansion of the civilian presence under Israeli protection.

The growing communities require housing, public services and security expenditure. Their establishment also raises the stakes of any future territorial agreement. Settlement construction has created a lasting administrative commitment, even as the question of sovereignty remains unsettled.

Acknowledgement: `The dispute continues.`

Do not report opposition by a named player government unless that government has actually acted. A relevant regional settlement photograph is still needed before every geographic variant is production-ready.

### W3. Attack on an Israeli Patrol

An Israeli patrol in {STATE} has come under attack, resulting in military casualties. The incident adds to the demands on forces responsible for protecting military routes, administrative facilities and settlements in the territory.

The attack demonstrates the continuing reach of armed underground networks despite the military presence. The authorities now face another choice over the scale and cost of their security response. Further operations could disrupt those networks, but would also place new demands on the administration and the people living under it.

Acknowledgement: `A dangerous escalation.`

This version needs actual military casualties and a recorded underground attack. Name Fatah, the PFLP or another organisation only when the committed incident establishes its involvement and the organisation exists in that period. An attack with known fatalities may use an explicitly fatal text branch; a reserve loss alone does not support one. The rejected Gaza colourization is not an approved picture for this event.

### W4. Civilians Killed in Israeli Raid

Civilians have been killed during an Israeli security operation in {STATE}. The raid, directed against an armed underground network, has brought renewed attention to the conduct of military operations in populated areas.

The deaths leave the administration facing demands for accountability alongside its continuing security commitments. An investigation, relief payments and restrictions on further operations would carry costs of their own. Whatever response the authorities choose, the incident has added to the tensions surrounding their presence in the territory.

Acknowledgement: `The human cost is mounting.`

Requires actual civilian fatalities caused by this resolved raid. The base version does not pretend an investigation has already opened. If a funded investigation has actually begun before publication, replace the second paragraph with its concrete status. Do not show an unrelated child's photograph or a later war's casualties as the victims. The current preview does not claim a production-ready Gaza image.

### W5. Settler Violence in the West Bank

Israeli settlers have attacked Palestinian residents in the West Bank, causing civilian casualties. The incident has deepened tensions around the settlements and placed the conduct of armed civilian groups under scrutiny.

The military administration faces pressure to protect residents and enforce public order while maintaining security for the settlements themselves. An investigation and restrictions on further arrivals would require a political decision. Leaving the attack unresolved could allow another cycle of violence to develop.

Acknowledgement: `The violence deepens the dispute.`

This draft requires recorded settler perpetrators, Palestinian civilian casualties and the West Bank location. A property-damage-only event needs a non-casualty variant. Other states need their actual local population wording. The text does not blame all settlers or assert that armed settler violence was already a uniform mass pattern in January 1970. Eligibility follows actual armed groups and incidents; there is no automatic historical date for it. Following the user's picture correction, the selected settler picture is now a new colour illustration of civilian settlers, some with slung period rifles, near a West Bank stone wall. Its intended period is the mid-1970s. It illustrates the setting, not an actual attack or the identity of perpetrators. The older external preview's Hebron market selection is superseded for this event. The actual registered news image and retained source are documented in the artwork notice.

### W6. Israel Extends Settlement Freeze

Israeli authorities have maintained a halt to new settlement approvals and arrivals in {STATE}. The extension follows an initial suspension and leaves existing settlements in place under continued protection.

The policy limits further expansion for the present, but does not remove the costs of administering the territory or determine its final status. Renewal, construction and security remain matters for the authorities. The freeze marks a sustained pause in settlement activity rather than a territorial withdrawal.

Acknowledgement: `A pause in expansion.`

Do not call a regional 13-week Decision a permanent national moratorium. Publication requires the actual 26-week uninterrupted episode specified above.

### W7. Israeli Settlement Evacuated

Israeli authorities have completed the evacuation of a settlement in {STATE}. Its surviving residents have been relocated, and the military administration has ended the site's operation.

The closure reduces one of the administration's local protection commitments, while leaving the wider occupation and existing territorial claims unchanged. The evacuation may affect future settlement policy, but it does not by itself constitute a border agreement or the withdrawal of Israeli forces from the territory.

Acknowledgement: `A settlement closes.`

Use the closure version only if the site actually closes. A partially reduced cohort uses `Settlement Residents Relocated` and states explicitly that the settlement remains. Do not resurrect lost residents, imply their consent, invent unrest at the evacuation or suggest a completed treaty.

### W8. New Services in Occupied Territory

A sustained programme of civilian expenditure has expanded services under the Israeli military administration in {STATE}. The completed work adds to the facilities available to local residents and the obligations carried by the administration.

The investment offers a practical improvement without settling the territory's political status. Continued operation requires regular funding, and public services remain exposed to disruption when security deteriorates. Maintaining the programme will therefore depend on decisions still to be made, rather than the completion of construction alone.

Acknowledgement: `Administration carries obligations.`

This draft requires real completed civilian work, actual local service availability and continuous programme funding. Mere office construction serving only settlers is insufficient. The Hebron market illustration fits a West Bank civilian-economy variant after 26 August 1970, not a claim that the photograph documents a new government facility.

### W9. Israel Changes Territory's Status

Israel has extended its domestic civil administration to {STATE}, following a prolonged period of control and a decision to incorporate the territory. The measure establishes new obligations toward its permanent residents under Israeli administration.

The change determines Israel's own treatment of the territory. It does not establish an agreed international boundary, remove competing claims or compel recognition by another government. Those questions remain separate from the domestic decision now taken.

Acknowledgement: `The question of recognition remains.`

Send only after the actual final incorporation transaction, never after settlement approval. No claim that these alternate-history core requirements were a historical legal path to sovereignty. No auto-recognition, foreign core removal or replacement of Palestinian political agency in other matters.

## Local event drafts and response effects

These are local country events, not additional permanent Decisions. Outcomes and losses already committed by the operation appear as the concrete resolved report; responses have their own actual prospective effects. The game must not replay those losses in every option. English Effects use native signed values and numeric formatters, with no explanatory implementation paragraphs. The descriptions below remain political and institutional.

| Draft title | Short description | Proposed responses |
|---|---|---|
| `An Attack on an IDF Patrol` | An Israeli patrol has suffered losses in {STATE}. The military administration must review its protection arrangements as the cost of holding the territory rises. | `Review the security deployment.` Acknowledgement only. Further paid protection uses the existing recurring security Decision. The report shows the actual loss tier, not an automatic second deduction. |
| `Underground Network Disrupted` | The operation in {STATE} has disrupted an armed network. The military administration reports a temporary improvement in the security situation, while patrol and protection duties continue. | `Maintain the deployment.` Acknowledgement. The actual successful raid has already applied Resistance Activity -20 for 8 weeks, or its funded-defence adjusted outcome. No extra core progress, equipment or manpower. |
| `An Inconclusive Operation` | The search in {STATE} has ended without a decisive disruption of the underground. Forces have returned to their regular duties after a costly operation. | `Review the operation.` Acknowledgement. Show the committed limited-result losses and Resistance Activity -5 for 4 weeks. An escalation uses its own description and committed -50 military manpower / +10 activity for 13 weeks. |
| `Civilian Deaths during an Operation` | Civilians have died during the operation in {STATE}. The military administration must decide whether to fund an investigation and emergency assistance. | `Open an investigation and fund relief.` Setup cost 0.05% of annual GDP; Political Power -25; Resistance Activity -10 for 13 weeks; new arrivals suspended for 13 weeks. `Take no additional measures.` No additional expenditure or relief. The actual civilian fatalities, +15 activity for 26 weeks, Consolidation -3 and calm-clock interruption have already occurred. |
| `An Attack on a Settlement` | An attack has disrupted an Israeli settlement in {STATE}. Residents and the local administration now face repairs and a renewed review of protection arrangements. | `Record the damage and losses.` Acknowledgement. The actual 0.10%-GDP repair invoice, 13-week arrival suspension and Consolidation -1 are committed once. Mention civilian deaths or injuries only when they actually occurred. |
| `Violence against Local Residents` | Israeli settlers have attacked local residents in {STATE}. The authorities must decide whether to investigate and restrict further arrivals while the incident remains unresolved. | `Fund an investigation.` Setup cost 0.10% of annual GDP; Resistance Activity -10 for 13 weeks; arrivals suspended for 13 weeks; the additional unresolved-incident recurrence weight is suppressed only while oversight is funded. `Take no additional measures.` No extra invoice or relief. The incident's actual damage, +15 activity and Consolidation -3 cannot be undone by either option. |
| `A Settlement Project Completed` | The approved project in {STATE} has received its residents and completed the facilities specified in its authorisation. Protection, maintenance and civilian services now become continuing commitments. | `The administration assumes its duties.` Acknowledgement of the actual completed project. Do not grant buildings or move population again on acknowledgement. The settlement type, approved price and investor terms come from the original project. |
| `Military Administration: Quarterly Report` | The administration has submitted its account of expenditure, security incidents and civilian programmes in the occupied territories. | `Receive the report.` Show actual aggregate expenditure and separate military losses, Israeli civilian fatalities, local civilian fatalities and wounded. No random new incident, reward, invoice or opinion bonus for reading it. |

The settler-violence investigation's temporary relief and 13-week oversight are new proposed response terms. They do not rewrite the original incident losses or make existing resident-related pressure disappear. On expiry the full underlying pressure and unresolved recurrence weight return unless a fresh paid intervention applies. Never stack a new permanent resistance reduction through repeated event options. Disable unaffordable paid responses, retain a free response and expire unanswered choice windows under a defined default so the recurring system cannot be frozen by an unclosed event.

## Image sources, transformation and limitations

The two selected preview pictures are licensed CC BY 4.0. Credits and the [licence](https://creativecommons.org/licenses/by/4.0/) accompany the preview. Both were transformed with the built-in image-generation editor solely for colourization. Colours are inferred and small generative detail changes cannot be excluded. Preserve the original source and describe modifications in the final mod notice before runtime release. Colourization does not establish new ownership over the source photograph.

| Picture | Source and author | Preview use and limits |
|---|---|---|
| Nahal Yam, 1969 | [Individual Commons source](https://commons.wikimedia.org/wiki/File:Dan_Hadani_collection_(990048238410205171).jpg). Israel Press and Photo Agency (I.P.P.A.) / Dan Hadani collection, National Library of Israel. CC BY 4.0, permission ticket 2020052410005395 | A military-agricultural outpost in Sinai. Colourized, resized and presentation-cropped. Not an image of fictional attackers or later settlers. Original file SHA256 and the final derivative are recorded in the visual-source manifest. |
| Hebron market, 26 August 1970 | [Individual Commons source](https://commons.wikimedia.org/wiki/File:Following_the_Cholera_desease,_Hebron_fruit_and_vegetable_merchants_can_hardly_sell_their_products_(FL45788605).jpg). IPPA Staff / Dan Hadani collection / National Library of Israel / The Pritzker Family National Photography Collection. CC BY 4.0, permission ticket 2021092910005788 | Ordinary civilian economy in the West Bank. The source concerns disruption during a cholera episode. Colourized, resized and presentation-cropped; use only as an explicit archival regional illustration after its date. It depicts neither a raid nor settler violence. |

The source selected for a Gaza search in 1969 was downloaded and inspected, but its colourization was rejected by the image tool. It is **not** included in the final newspaper preview or approved for runtime release. The 1971 Gaza patrol candidate was not used. Source research also encountered an older photograph with incomplete cross-jurisdiction licence information; it was not selected. Regional Gaza/Golan pictures, a closed-settlement image, and the different native country-event compositions still need their own period and rights checks before production integration. The requested rule is that every picture actually used in this preview is colourized, not that a production event pack is already complete.

The earlier selected coloured archive pictures and the editable external newspaper concept are in the thread's authorized visualization directory. Its manifest records source URLs, licence, hashes, exact colourization prompts and the built-in tool's output paths. The subsequent actual native newspaper and selected settler illustration are now retained under `tools/world_news_skin/`, including their source records and exact generation prompt. The installed skin uses original code-native artwork and contains no inherited BNN pixels or third-party newspaper masthead. The supplied settler reference's author and licence are unknown; the original photograph is not redistributed. The illustration is newly generated, not an archival colourization.

## Historical basis

These records justify the kinds of event, not the fictional drafts or their numerical balance:

- [JTA, 8 May 1969: Nahal Argaman](https://www.jta.org/archive/third-israeli-outpost-on-west-bank-is-inaugurated-named-for-2-dead-officers): contemporary military-agricultural settlement and the Nahal institutional setting.
- [JTA, 17 November 1969: incidents and security responses](https://www.jta.org/archive/fighting-grenade-incidents-cause-21-israeli-casualties-over-weekend): distinct military and civilian casualties. Its individual responsibility claims require attribution, not automatic adoption as verified fact.
- [JTA, 6 January 1970: Gaza confrontation](https://www.jta.org/archive/israeli-soldiers-and-arab-guerrillas-killed-and-wounded-in-encounter): an active armed underground at the scenario opening, not a reason to create modern organisations in 1970.
- [JTA, 27 April 1970: Hebron housing dispute](https://www.jta.org/archive/new-split-emerges-in-cabinet-over-issue-of-permanent-jewish-settlement-in-hebron): settlement policy as a real cabinet and institutional controversy.
- [FRUS, 1 February 1969, document 4](https://history.state.gov/historicaldocuments/frus1969-76v23/d4): a contemporary US assessment of armed movements, retaliation, territorial proposals and Israeli political disagreement.
- [UN seminar report, 1983](https://www.un.org/unispal/document/auto-insert-194986/): later discussion of increasing settler violence from 1979/1980. It cannot establish an identical widespread pattern in January 1970. W5 follows actual alternate-history escalation rather than a forced date.

Original concept and English drafts prepared with Codex for IMPERIA COLD WAR. MD/Paradox retain their inherited interface rights; original artists and specific upstream asset licences are unknown here. The inherited window was inspected as a donor, not claimed as original work or redistributed with the new preview. No live game rendering, save/reload execution, news delivery, performance timing or multiplayer verification has been performed for this proposed system.

External-preview check: all three example reports loaded with both selected colourized pictures at widths 736, 360 and 320, in light and dark appearance. Eighteen browser cases passed image-loading, containment and content-position checks with no page errors. Scenario switching and acknowledgement were checked separately; desktop and narrow screenshots were visually inspected. This establishes the external preview's behaviour only, not native event delivery or in-game readability. The editable source is `israel-world-news-template.html`; the built fragment is `israel-world-news.html`, both in the thread's authorized visualization directory alongside `israel-news-colourization.json` and `israel-world-news-browser-check.json`.
