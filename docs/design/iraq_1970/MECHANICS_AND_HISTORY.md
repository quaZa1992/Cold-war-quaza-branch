# COLDWAR | Iraq 1970–1990: mechanics and historical evidence

Design research only, inspected 18 October 2026. This file does not load gameplay content. All numerical Iraq spirit and programme values are balance proposals, not measured historical coefficients. Engine loading, tooltips, government transitions and multiplayer/save behaviour remain untested in HOI4.

Programme scope follows the historically significant Iraqi parties and principal leaders. The communist programme comprises the ICP and Aziz Muhammad; other communist organizers and factional debates are represented as party history, advice and internal decisions, not a catalogue of invented alternative governing secretaries.

## Sources and exact present start

Target root: `C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar`.
MD reference root: `E:/SteamLibrary/steamapps/workshop/content/394360/2777392649`.
Both trees provide current MD source; the target additionally contains the preserved Imperia and Cold War systems. Target `descriptor.mod:1` declares MD 2.0.2 and `descriptor.mod:12` HOI4 1.19.*. References below are relative to target unless prefixed `MD:`.

`history/countries/IRQ - Iraq.txt:4–24` establishes January 1970:

- Capital 557, the Babylon/Baghdad state, not a separate Baghdad state ID.
- Ahmed Hassan al-Bakr, portrait `gfx/Leaders/IRQ/IRQ_Coldwar_Ahmed_Hassan_al_Bakr.dds`, ideology `Nat_Fascism`; the history creation has expiry 16 July 1979. Preserve the starting leader.
- Cosmetic `IRQ_BAATH_1970`; `mdcw_1970_generic_focus` is loaded, not the native 2000 Iraqi tree.
- `gdp_per_capita = 0.337`, `overall_productivity = 327.645`. These are game inputs, not an independently validated economic model.
- `IMP_1970_profile_national_fascist = yes`; its exact provider is `common/scripted_effects/IMP_1970_world_politics_effects.txt:170–190`.
- `ruling_party = 21`; outlook `nationalist`; elections disabled; coalition array contains party 22.
- Party array: 0=.03, 1=.02, 4=.03, 5=.02, 10=.02, 13=.10, 14=.04, 18=.04, 20=.08, 21=.54, 22=.08; the other slots are zero. Outlook totals: democratic .05, communism .05, fascism .02, neutrality .18, nationalist .70.
- Land, navy and air OOBs deliberately empty by the user's previous scenario decision. This concept must not add a historical starting army or equipment catalogue as a side effect.

Global 1970 alignment also puts Iraq in the Arab Joint Defence arrangement and joins the Egyptian war against Israel if that war is active: `IMP_1970_world_politics_effects.txt:1237–1289`. Do not interpret the January start as necessarily being at peace. A defensive/war branch needs its actual war predicates.

### A material gap in the existing January start

No `literacy_rate`, budget laws, corruption law or country-specific national spirits are assigned inside Iraq's 1970 history block. The later `add_ideas` block at `history/countries/IRQ - Iraq.txt:382` belongs to **2000.1.1**, including corruption level 09, rentier state, multiethnic society, religion, spending laws and military factions. Those future ideas cannot be assumed present in January 1970.

The generic education startup at `common/on_actions/00_on_actions.txt:1871` calls `EDU_learn_your_ABCs_with_dread`, whose provider `00_education_effects.txt:1–14` requires an already existing `literacy_rate` variable. The global literacy roster in `00_startup_effects.txt:558–632` omits Iraq. Thus no exact numeric Iraqi 1970 literacy value is proved by current source. A future implementation should deliberately initialize a researched/balanced native literacy value and its education spirit, rather than adding an unrelated duplicate “low literacy” research penalty. A provisional value such as .35 must be labelled a proposal until the reference year and population definition are settled.

No claim is made that all default engine law choices are absent: an engine start is needed to establish defaults. The evidence establishes that the country has no authored January law/education package. A starting-spirit balance review must inspect the actual initialized law effects before final values are frozen.

## Governing parties, outlooks and real people

The actual country catalogue at `tools/historical_politics_1970/data/world.json:9053–9167` contains only three Iraqi organizations: Baath 21, ICP 4 and KDP 6. The historical labels are in `localisation/english/mdcw_historical_politics_1970_l_english.yml:1055`, `:1175`, `:1502`.

| Organization or family | January 1970 status in target | Exact current governing trigger | Design consequence |
|---|---|---|---|
| Arab Socialist Baath Party | Live party 21; starts in power | `nationalist_fascist_are_in_power = yes` | Shared Baath institutions plus actual Bakr/Saddam leader programmes. Do not require another accession focus to unlock the already ruling Baath. |
| Iraqi Communist Party | Live party 4 | `emerging_communist_state_are_in_power = yes` | Use the 1970 mapping. The native **2000** Iraq communist route uses neutral communism/19; copying it here would gate the wrong party. |
| Kurdistan Democratic Party | Live party 6 | `emerging_reactionaries_are_in_power = yes` | “Conservative” in its historic roster is MD's emerging Conservative slot6, not Western conservatism1. A federal-Iraq KDP government and a regional KDP settlement are different contexts. |
| Constitutional social democrats/NDP successors | No named 1970 Iraqi party integration yet | Candidate 3 or18, not settled | Historical institutions/people can be designed now; exact roster mapping and leader pool are provisional. Do not claim modern party records are already a 1970 institution. |
| Sunni Muslim Brotherhood/Iraqi Islamic Party | No named 1970 Iraqi integration yet | Candidate 12: `neutrality_neutral_muslim_brotherhood_are_in_power` | Historically relevant Sunni Islamism. Do not substitute ISIS, al-Qaeda or a 2000s Salafi organization. |
| Dawa / Islamic constitutionalists | No named 1970 Iraqi integration yet | Candidate8: `emerging_moderate_shiite_are_in_power` | Country-specific policy/leadership identity must be integrated. Slot label is a gameplay family, not proof that all Dawa doctrine equalled Iranian clerical rule. |
| Iranian-aligned clerical revolutionaries | No named 1970 integration | Candidate9: `emerging_hardline_shiite_are_in_power` | A later SCIRI formation requires its real formation context, never a January1970 named SCIRI branch. |
| Military nationalists | Family22 already in coalition | `nationalist_military_junta_are_in_power` | A genuinely governing junta programme, not an extra reward while Baath governs. Coalition participation alone does not qualify. |
| Hashemite constitutional restoration | Marginal alternate history; no current Iraqi historical integration | Candidate23: `nationalist_monarchists_are_in_power` | Explicitly alternate; Raad is an adult candidate, subject to a real constitutional process and installation. Do not resurrect FaisalII or Abd al-Ilah or invent a January1970 reign. |

Trigger definitions and indexes: `common/scripted_triggers/01_political_triggers.txt:176–337`. Outlook engine groups in `common/ideologies/00_ideologies.txt`: democratic0–3, communism4–9, fascism10–11, neutrality12–19, nationalist20–23. An outlook is not a single political party. An outlook-strengthening focus may change support through the native popularity API; it cannot activate all parties' government programmes simultaneously.

The current native 1970 Baath pool at `common/scripted_effects/mdcw_historical_native_pools.txt:6241–6322` cycles Bakr, Saddam and Tariq Aziz; actual routing is at `:16029`. Their pool indices are not office-holder flags. The catalogue makes Tariq available from1975 and Massoud Barzani from1980, but the native-pool succession helper shown here itself contains no date predicates. Treat that as an existing integration issue to account for, not as authority to backdate every person or rewrite the shared successor system during a focus concept.

### Historically grounded leadership and faction treatment

| Person | Evidence-backed role | Programme treatment |
|---|---|---|
| Ahmed Hassan al-Bakr | Starting president and RCC chair | Historical governing programme; collective party/army management, negotiated front versus security consolidation, industrial and agrarian choices. |
| Saddam Hussein | Bakr's powerful deputy; succeeded in1979 | Historical contender and successor. National security, centralized patronage versus technocratic delegation, Iraq-first versus pan-Arab commitment. Leadership installed through existing succession, never merely by completing a candidature. |
| Tariq Aziz | Actual senior Baath politician/diplomat, existing target successor | Cabinet/diplomatic content and a possible alternate outcome through the existing leadership registry. No additional standalone governing tree is emitted; do not label him a historical Iraqi president. |
| Aziz Muhammad | ICP first secretary elected1964 and again1970 | Main historical communist leader throughout this period; branches for a safeguarded national front versus independent organization, worker councils versus ministerial planning, civilian compromise versus armed resistance. He was not a sequence of short-lived communist leaders. |
| Amir Abdullah | Influential ICP leader; favoured cooperation and served as minister of state | A documented accommodation faction for ICP debates and cabinet decisions, not a separate governing-secretary tree. |
| Zaki Khairi | Veteran ICP leader; deputy first secretary and acting first secretary in a1971 account | Senior participant in ICP policy and leadership history. Do not present him as replacing Aziz Muhammad as historical secretary-general in1970 or give him an invented separate government. |
| Mukarram al-Talabani | ICP minister of irrigation | Agrarian/technical cabinet content, not an evidenced historical secretary-general. |
| Aziz al-Hajj | Led Central Command splinter1967–69; captured and politically broken in February1969 | Historical factional reference. Not a free January1970 secretary-general or a separate surviving governing programme. Any rehabilitation decision concerns individual legal/party status rather than an automatic presidency. |
| Muhammad Baqir al-Sadr | Shia scholar, Dawa's ideological/spiritual reference; executed1980 historically | A real constitutional/Islamic programme can be organized around his ideas and protection; do not mislabel him as a verified1970 elected party secretary. Any head-of-government accession is alternate history. |
| Abd al-Sahib Dukhayl and Muhammad Hadi al-Subayti | Documented Dawa organizational/intellectual leadership in the1963–71 period; accounts dispute individual primacy | Concrete organizational figures for the Dawa party programme and its internal choices. Do not invent a single formally elected1970 secretary-general or confuse either man's party role with an already held Iraqi state office. |
| Numan al-Samarrai | Founding president of the IIP in1960, identified by the party's own obituary | Concrete figure for a lawful party reconstitution/leadership election. A1970 government accession is alternate history, and his1960 title does not by itself prove current1970 office. |
| Ayad al-Samarrai | Brotherhood/IIP underground youth organization from1970 in its own movement history; fled1980 | Clandestine constitutional Sunni organization and later exile continuity; avoid an unverified exact January secretary-general title. |
| Mustafa Barzani | KDP historic leader until death1 March1979 | Real1970 Kurdish counterpart; autonomy negotiation, revenue distribution and education/security arrangements. |
| Masoud Barzani | Elected KDP president at its1979 congress | Later KDP programme after real succession; don't backdate him as1970 party chairman. Current target catalogue begins1980, needing a future deliberate integration decision. |
| Jalal Talabani | Kurdish left/intellectual opposition; PUK founded1975 | KDP reform opposition may be present1970; named PUK state-party programme requires formation, rather than labelling1970 politics PUK. |

Evidence and limits for those distinctions:

- [FRUS, Iraq under Baath rule1968–76](https://history.state.gov/historicaldocuments/frus1969-76v27/d317) documents Bakr/Saddam, Aziz Muhammad's1970 re-election, Amir Abdullah's cooperation position, Mukarram's ministry and Baath constraints on the Front. Its retrospective intelligence judgments are evidence of contemporary assessment, not objective endorsement of a faction. This source's treaty month is inconsistent with the treaty record: use9 April1972, below.
- [Jasim al-Halwai's participant account](https://www.ahewar.org/debat/show.art.asp?aid=55721) identifies Khairi as acting first secretary in1971 and deputy during1976 programme preparation. Memoir evidence must not be inflated into a documented long secretary-general term.
- [Kurdish Institute historical archive, Aziz al-Haj: A Communist Radical](https://bnk.institutkurde.org/images/pdf/983WR6NZAS.pdf) records the armed Central Command milieu and termination of al-Hajj's militant career in February1969. [Central Command overview](https://en.wikipedia.org/wiki/Iraqi_Communist_Party_%E2%80%93_Central_Command) is a secondary locator for Ibrahim al-Alawi; that succession should receive another primary check before implementation.
- [Brotherhood's institutional history of the Iraqi Islamic Party](https://ikhwan.wiki/index.php?title=%D8%A7%D9%84%D8%AD%D8%B2%D8%A8_%D8%A7%D9%84%D8%A5%D8%B3%D9%84%D8%A7%D9%85%D9%8A_%D8%A7%D9%84%D8%B9%D8%B1%D8%A7%D9%82%D9%8A) specifically describes al-Samarrai's youth-organizing task in1970 and clandestine provincial cells. It is a partisan primary account; no claim of neutrality.
- [KDP's own party history](https://kdp-fro.krd/en/about-kdp) establishes Mustafa's role and1970 congress. [Masoud's official biography](https://www.masoudbarzani.krd/en/biography-masoud-barzani/) records his1979 election. These are institutional primary accounts; they are not independent assessments of all territorial claims.
- [Amnesty's Iraq report](https://www.amnesty.org/zh-hans/wp-content/uploads/2021/09/mde140012005en.pdf) documents Baqir al-Sadr and Bint al-Huda's1980 killing. Dawa's organizational founders and exact early titles are disputed in the literature; use the ideologue description and verify any minister/president candidate separately.

### Other concrete historical candidates and office limits

| Route | Named historical figure | What the sources support | Concept boundary |
|---|---|---|---|
| Officer republic | Abd al-Rahman Arif | President1966–68; removed and sent abroad in July1968; later exile in Turkey | A living former president can anchor an explicit return-from-exile alternative. He is not an active1970 president or a guaranteed leader of every officer faction. |
| Arab nationalist / Nasserist | Fuad al-Rikabi | Former Baath founder/minister who moved into Arab nationalist/Nasserist opposition; killed in prison in1971 in the historical course | A concrete opposition figure whose freedom/survival must follow actual campaign events. Do not resurrect him after a recorded killing or treat release as an automatic government transfer. The exact detention timeline needs further primary-source reconciliation. |
| Arab nationalist / civilian economic cadre | Khair al-Din Haseeb | Central-bank/economic administration and later Arab nationalist intellectual work | His professional credentials are historical; a future party election, premiership or presidency is an explicitly alternate outcome. Do not invent a historically held1970 party-chair office. |
| Civilian democratic current | Muhammad Hadid | Senior National Democratic Party figure and finance minister under Qasim | A democratic return from political withdrawal is alternate history. He provides a concrete civilian/economic programme reference, not proof that the banned party already governs. |
| Sunni Islamist current | Numan al-Samarrai; later organizational cadres including Ayad al-Samarrai and Muhsin Abd al-Hamid | Founding IIP leadership,1970 youth organization and later Brotherhood/IIP scholarship and leadership are distinct records | Use Numan for the verified founding-leader reference. Do not backdate Muhsin's later party/state office or Ayad's later secretaryship into January1970. |
| Dawa | Dukhayl, Subayti and the distinct religious reference of Baqir al-Sadr | Organizational, intellectual and religious authority were distributed and sometimes disputed | The concept can name the people and real internal questions now. Exact candidate windows, detention/exile transitions, portraits and integration with government-office installation remain implementation research. |
| SCIRI | Muhammad Baqir al-Hakim | Leader of the exile organization founded in Iran in1982 | A concrete later party/leader programme, contingent on actual formation. It must not appear as an already formed January1970 party or a1970 Iraqi presidency. |
| Constitutional Hashemite alternative | Prince Raad bin Zeid | Adult Hashemite prince; born1936. His father Zeid, rather than Raad, headed the former Iraqi royal house until October1970 | Raad is a possible adult alternate restoration candidate, not a January1970 king or a proven majority-party leader. A constitutional choice may fail; a dynasty claim does not itself install a government. |

Source basis for these candidate distinctions:

- [Contemporary NSC memorandum on the17 July1968 coup](https://history.state.gov/historicaldocuments/frus1964-68v21/d199) records Arif's overthrow and deportation; [Independent obituary](https://www.the-independent.com/news/obituaries/abdulrahman-aref-402708.html) confirms the subsequent Turkish exile. Sources differ on his later return year; the concept does not need to invent an automatic return date.
- [Haseeb's colleague Saad Jawad's recollection](https://iraqieconomists.net/en/2021/04/01/remembering-dr-khair-el-din-haseeb-bellwether-of-the-arab-national-movement-by-saad-jawad/) documents economic offices and post-coup imprisonment/exile context. This is a participant recollection, not proof of a1970 political executive title.
- [Contemporary FRUS1959 memorandum](https://history.state.gov/historicaldocuments/frus1958-60v12/d159) identifies Hadid as an NDP minister and finance minister. It does not establish him as the1970 party's elected chairman or president.
- [IIP political bureau's obituary statement for Numan](https://shafaq.com/ar/%D9%85%D8%AC%D8%AA%D9%80%D9%85%D8%B9/%D8%A7%D9%84%D8%AD%D8%B2%D8%A8-%D8%A7%D9%84-%D8%B3%D9%84%D8%A7%D9%85%D9%8A-%D8%A7%D9%84%D8%B9%D8%B1%D8%A7%D9%82%D9%8A-%D9%8A%D9%86%D8%B9%D9%89-%D8%B1-%D9%8A%D8%B3%D9%87-%D8%A7%D9%84-%D9%88%D9%84) explicitly describes its first president and his1960 founding leadership. [Muhsin Abd al-Hamid's interview](https://www.rudawarabia.net/arabic/categories/interview/1208974) distinguishes the later party from the intervening Brotherhood organization. The movement's own Ayad biography cited above specifically records youth organizing in1970; a later office is not a January1970 title.
- [Ali al-Mu'min's account of Dawa's leadership phases](https://www.almothaqaf.com/books/906110.html), drawing on named participants, identifies Dukhayl's organizational and Subayti's intellectual/political roles and explicitly discusses competing accounts of primacy. It is a retrospective, movement-oriented historical analysis, not an undisputed formal officer register. Execution dates and exact succession windows must not be hard-coded from inconsistent memorial accounts without further checking.
- [Historical study of Iraqi1960s intellectual and political currents](https://pure.uva.nl/ws/files/63844527/Chapter_4.pdf) supports Rikabi's1971 prison death. His future availability must track whether that event occurs in the campaign, rather than mechanically assigning a death in every alternate government.
- [US Institute of Peace report on Iraqi Islamist politics](https://www.usip.org/sites/default/files/resources/sr108.pdf) identifies Muhammad Baqir al-Hakim with SCIRI and its1982 Tehran formation. This supports the later programme's identity, not an unconditional Iranian agreement or an automatic office in Iraq.
- [Royal Hashemite Court's notice honouring Prince Raad](https://rhc.jo/en/news/king-attends-ceremony-honour-prince-raad) confirms his identity; [Neue Gotha's dynastic register](https://neuegotha.com/register/kingdom-of-iraq-house-of-al-hashimi/) gives his1936 birth and the October1970 Zeid-to-Raad succession. The latter is a secondary genealogical source. The concept need only identify a possible adult alternate candidate; it must not backdate his dynastic headship.

These names are adequate to make the concept concrete and historically accountable. A complete executable leadership roster still requires person-specific living/free/exile windows, correct party affiliation for each interval, images, and actual installation hooks. That remaining integration should be reported rather than hidden behind generic “a historical leader” text or false current offices.

## January atmosphere, historical trajectory and choices

The start should show an insecure post-coup state, unresolved northern war, uneven state reach, oil concessions and limited skilled labour. It should not begin with1991 sanctions, Iran-Iraq war devastation,2003 occupation, ISIS, or1980s clerical alliances already completed.

| Historical issue | Historical development | Playable choice and actual mechanical consequence |
|---|---|---|
| Kurdish conflict |11 March1970 autonomy agreement; later implementation dispute | Negotiated autonomy reduces the northern burden but commits administrative/welfare costs and constraints on unilateral police centralization; coercive rule can strengthen state security but maintains unrest, supply and diplomatic burdens. Regional partners need actual consent, not a transfer by tooltip. |
| Oil sovereignty | IPC nationalization1 June1972 | Compensation/marketing settlement versus confrontation. State revenue control can improve `oil_export_multiplier_modifier`; an actual short-term market penalty and payment accompany the transition. No instant oil-income windfall merely for renaming a spirit. |
| Soviet relationship | Treaty9 April1972; oil technical aid | Technology/industrial partnership versus diversified suppliers; influence dependence and diplomatic costs reflect the advantage. No automatic Warsaw Pact membership. |
| National Progressive Front |1973 Baath–ICP pact, with unequal power | A meaningful coalition can exchange appointments and toleration for state legitimacy; coalition membership does not unlock the communist governing programme. Later repression deactivates coalition concessions and produces real opposition, rather than an unlimited stability reward. |
| Northern settlement and Iran | Algiers6 March1975, formal treaty13 June | Border compromise and withdrawal of support require Iranian agreement; it changes diplomatic/security burdens, not free ownership of an Iranian state. |
|1979 transition | Saddam replaced Bakr | Existing succession installs the office-holder; party institutions persist while personal programmes change. A sustained Bakr or Aziz settlement is alternate history and must have continuation. |
| Iran-Iraq War | War1980–88 and1988 ceasefire | Offer territorial revisionism, defensive containment or negotiated coexistence as choices. War routes pay real personnel/equipment and reconstruction costs. UN mediation needs both belligerents; no unilateral guaranteed peace. |
| Anfal and displacement | Mass repression and destruction of Kurdish communities | Represent repression, civilian suffering, resistance, displacement and international repercussions; never make atrocities a clean manpower/production reward. Preserve Imperia refugee/civilian-loss accounting rather than inventing population grants. |
| Postwar crisis and Kuwait | Debt and oil-policy pressures; invasion1990 | Negotiated debt/oil diplomacy versus coercive escalation. Invasion may produce a war goal through supported code if approved; no automatic annexation, stolen reserves or free cores. |

Primary evidence for this table:

- [FRUS oil nationalization assessment,7 June1972](https://history.state.gov/historicaldocuments/frus1969-76ve04/d311) explains operational capability versus marketing/legal risk. [FRUS telegram on the dispute](https://history.state.gov/historicaldocuments/frus1969-76ve04/d314) anticipates serious temporary revenue loss, supporting a costly transitional policy rather than an instant universal improvement.
- [Iraqi ratification law47/1972](https://wiki.dorar-aliraq.net/iraqilaws/law/5426.html), a reproduction of the original law, dates the Soviet treaty9 April1972; [contemporary FRUS treaty memorandum](https://history.state.gov/historicaldocuments/frus1969-76ve04/d305) independently confirms the date.
- [FRUS assessment one year after Algiers](https://history.state.gov/historicaldocuments/frus1969-76v27/d306) describes the exchange of Iranian support for the Kurds for the Shatt al-Arab boundary compromise and the June treaty.
- [Human Rights Watch's Anfal investigation](https://www.hrw.org/reports/1993/iraqanfal/ANFALINT.htm) documents Arabization, forced removals and village destruction. Mechanics should describe the violence and its consequences candidly.
- [UN Security Council resolution598](https://digitallibrary.un.org/record/137345?ln=en) requests ceasefire, withdrawal, mediation and prisoner release; [UN account of the Iran-Iraq agenda](https://main.un.org/securitycouncil/en/content/repertoire/middle-east) records the war and observer mission.

## Verified effect/modifier registry

The following are usable source-backed building blocks. Native engine modifier applications are evidenced by actual MD country ideas; their final campaign effect is calculated by HOI4 and is not proven by a text search. For custom MD modifiers, the consumer is listed. Values in this table describe units, not an Iraq balance prescription.

`MD:G` = `MD:common/ideas/generic_ideas.txt`; `MD:A` = `MD:common/ideas/05_armenia.txt`; `MONEY` = `common/scripted_effects/00_money_system.txt`; `DEF` = `common/modifier_definitions/money_modifier_definitions.txt`.

| Exact key | Scope, units and useful interpretation | Provider/example and consumer |
|---|---|---|
| `political_power_factor` | Country idea/dynamic; .10 = +10% PP gain multiplier | MD:G91; native engine |
| `stability_factor` | Country idea/dynamic; .05 = +5 stability percentage points in active modifier | MD:G34; native engine |
| `war_support_factor` | Country idea/dynamic; .05 =5 support points | MD:G1229; native engine |
| `drift_defence_factor` | Country idea/dynamic; fractional ideology-drift defence | MD:G35/84; native engine; not identical to Cold War campaign resistance |
| `foreign_influence_defense_modifier` | Country; fractional MD influence-defence modifier | MD:G52; `00_influence_scripted_effects.txt:1115–1122` subtracts defender's value from the attacker's gain multiplier before applying positive influence growth; do not relabel it party-support campaign defence |
| `research_speed_factor` | Country; .05 = +5% research speed | MD:G704; native engine |
| `production_speed_buildings_factor` | Country; .10 = +10% construction speed | MD:G168; native engine |
| `industrial_capacity_factory` | Country; .10 = +10% military-factory output | MD:G36/368; native engine; not civilian construction output |
| `production_factory_efficiency_gain_factor` | Country; fractional efficiency-growth multiplier | MD:G186; native engine |
| `production_factory_max_efficiency_factor` | Country; fractional production-efficiency-cap modifier | MD:G120; native engine |
| `consumer_goods_factor` | Country; fractional consumer-goods requirement modifier | MD:G167/310; native engine. Show native wording; no guaranteed same absolute factory count in every economy. |
| `fuel_gain_factor` | Country; .05 = +5% fuel gain from oil | MD:G232; native engine; does not create oil resources or raise export income |
| `army_org_factor` | Country; fractional land-unit organization multiplier | MD:G647; native engine |
| `army_core_defence_factor` | Country; fractional defence bonus on core territory | MD:G1100; native engine |
| `training_time_army_factor` | Country; negative shortens army training | MD:A865; native engine |
| `supply_consumption_factor` | Country; positive increases units' supply burden | MD:A1477/1859; native engine |
| `planning_speed` | Country; fractional planning accumulation speed | MD:A2859; native engine |
| `conscription_factor` | Country; recruitable-population factor, not free manpower | MD:G493; native engine |
| `tax_gain_multiplier_modifier` | Country; .10 adds10% to relevant tax multiplier, not tax rate | DEF2; MD:G169; MONEY425,729,778 |
| `bureaucracy_cost_multiplier_modifier` | Country; .10 increases relevant bureaucracy costs10% | DEF51; MONEY3307 multiplies population-based bureaucracy-law cost by1+modifier |
| `social_cost_multiplier_modifier` | Country; .10 increases selected welfare/social cost10% | DEF107; MD:G250; MONEY3501 multiplies social-law cost by1+modifier |
| `personnel_cost_multiplier_modifier` | Country; .10 increases aggregate personnel-cost multiplier | DEF16; MONEY3179 |
| `army_personnel_cost_multiplier_modifier` | Country; .10 increases army personnel multiplier | DEF23; MD:A443; MONEY3180 |
| `equipment_cost_multiplier_modifier` | Country; military equipment maintenance/cost multiplier; not factory IC price | DEF44; MONEY3184; do not invent `military_cost_multiplier_modifier` |
| `oil_export_multiplier_modifier` | Country; additive resource-specific export-revenue multiplier | DEF121; MONEY4506,4529. Income still needs exported oil, market price and normal sale rate. |
| `agricolture_productivity_modifier` | Exact MD misspelling required. Country fractional agriculture productivity input | DEF353; MD:G307; MONEY408/544/5244/5940; agricultural GDP, tax and output formulas. Not generic industrial productivity. |
| `productivity_growth_modifier` | **Number**, not percent. Base monthly productivity growth input | DEF410; MD:G173. `00_productivity_effects.txt:64–83` multiplies by .5 and1+country_growth; `:30–61` applies state/catch-up scaling; `:229–238` adds state growth. Not +10% monthly productivity. |
| `interest_rate_multiplier_modifier` | **Number of interest percentage points** | DEF9; MD:G288. MONEY2556 adds it to pre-clamp interest; rate clamped .8–50; weekly debt charge calculated from debt and rate. -.5 means half an interest point, not a50% reduction. |
| `return_on_investment_modifier` | Fractional annual ROI addition, .01 =1 percentage point | DEF198; MD:G297; MONEY4481 base.04+modifier clamped to global cap. Actual treasury flow uses held investments. |
| `receiving_investment_cost_modifier` | Fractional investment-project monetary-cost input | `common/modifier_definitions/modifier_definitions.txt:63`; MD:G172; `99_investment_scripted_effects.txt:161–171` builds1+modifier for recipient project pricing. It does not guarantee foreign investors agree. |
| `corruption_cost_factor` | Native corruption-law political cost factor | MD:A337/392. `common/ideas/AA_corruption_laws.txt:2–8` defines corruption law category and300 PP base cost. **Not fiscal corruption leakage**, not a corruption-level reduction. |
| `globalism_equilibrium` | Imperia number,0–100 target; +5 =5 target points | `common/modifier_definitions/mdcw_imperia_globalism_modifiers.txt:8`; `mdcw_imperia_globalism_effects.txt:1–37` reads and clamps target, moves globalism gradually, then recalculates its established modifiers. |
| `mdcw_cw_ideological_defence` | Cold War fractional resistance to foreign party-support campaigns | `common/modifier_definitions/mdcw_cold_war_modifiers.txt:14`; `mdcw_cold_war_effects.txt:3570–3573` computes1−modifier clamped0–1; does not prevent a normal election or coup. |
| `mdcw_cw_market_exposure` | Cold War fractional multiplier to existing market exposure | Same definitions:42; `mdcw_cold_war_effects.txt:4149–4151` scales exposure by1+modifier, final exposure clamped0–2.5. Higher exposure increases both favourable and adverse market effects. |
| `mdcw_cw_assistance_effectiveness` | Cold War fractional assistance benefit factor | Same definitions:7; `mdcw_cold_war_effects.txt:2392`; grant only when the existing assistance system is relevant. |

**Do not approve guessed keys.** `resources_factor`, `military_cost_multiplier_modifier`, free-form state output keys and fake monthly party drift must not be generated merely because they sound appropriate. `add_resource` and explicitly registered MD economic modifiers are safer supported alternatives. Add a new modifier only after defining and proving its consumer, not by adding a localization string.

### Native effect snippets and caveats

Treasury/debt are displayed in game billions: `localisation/english/MD_money_l_english.yml:11`, `:16`, `:25`. No historical-dollar claim should be attached to these calibrated game quantities.

```hoi4
# Country scope: actual MD financial helpers, not nonexistent add_money.
set_temp_variable = { treasury_change = -0.05 }
modify_treasury_effect = yes
set_temp_variable = { debt_change = 0.05 }
modify_debt_effect = yes

# Country scope: changes real subparty support. 0.03 is3 percentage points.
set_temp_variable = { party_index = 4 }
set_temp_variable = { party_popularity_increase = 0.03 }
set_temp_variable = { temp_outlook_increase = 0.03 }
change_relative_party_popularity = yes
set_temp_variable = { temp_outlook_increase = 0 }

# Country scope: real native literacy improvement, earned once.
set_temp_variable = { LR_change = 0.02 }
update_literacy_rate = yes

# State scope, guard actual Iraqi ownership/control and level/slot capacity.
171 = {
    add_resource = { type = oil amount = 4 }
    add_building_construction = {
        type = industrial_complex
        level = 1
        instant_build = yes
    }
}
```

Provider proofs:

- `modify_treasury_effect` and `modify_debt_effect`: `common/scripted_effects/00_budget_effects.txt:1487–1505`; the former updates treasury, the latter clamps debt≥0; both mark money dirty. The treasury helper can take the account below zero, so affordability must be enforced by a real decision/project contract.
- `change_relative_party_popularity`: `00_MD_politicsview_scripted_effects.txt:257–332`. Without `temp_outlook_increase`, the benefit mostly redistributes **inside** the existing outlook and is capped by its remainder. Use the optional outlook parameter only if growing the broader outlook is intended; clear its temp value afterward.
- `change_ruling_party_effect`: same file:1971–2053; input `rul_party_temp`, optional coalition slots and election/leader parameters. It sets the governing subparty, coalition, leader and internal-faction configuration. Use this established system; setting only `set_politics` changes the outlook without reliably authoring the exact subparty.
- `update_literacy_rate`: `00_education_effects.txt:178–193`; clamps .01–1 and updates the existing education dynamic modifier. `:118–131` maps literacy to research, education cost and workforce/productivity effects. Do not execute a one-time literacy gain during government refresh.
- `decrease_corruption`: `00_budget_effects.txt:783–851`; moves a real corruption idea down one tier. At level01 it instead grants150 PP, so a corruption reform must explicitly require a worse tier; otherwise a late reform becomes an accidental PP gift. `increase_corruption` at:675 moves up the tier ladder.
- State resources: `MD:common/national_focus/00_generic.txt:1849`; normal construction syntax at:2832–2844 and:3128–3133. Usable buildings defined by `common/buildings/00_buildings.txt`: `industrial_complex`, `arms_factory`, `offices`(:255), `fossil_powerplant`(:346), `agriculture_district`(:369), `infrastructure`, air/naval bases. Construction must respect controlled state, native max level and staff/energy consequences. A reactor/nuclear project requires the dedicated project system, not a generic free power plant.

### Funding a programme without exploitative replay

The final concept quotes Iraqi public programmes as `gdp_total * proposed_share`, shows the exact MD-billion invoice, and freezes that quote at the first completion attempt. Current node proposals range from .5% to 5% of MD GDP. These are explicit new balancing proposals, not main-MD constants, measured historical expenditure or an existing 1970 construction-price discount.

Payment occurs only on valid delivery, after rechecking exact eligibility, treasury, ownership/control and building capacity. All rewards are inside that transaction. A failed attempt pays nothing and becomes pending; the start-accessible retry preserves the original quote. There is no deposit or refund. A monthly programme refresh cannot charge again or replay buildings, literacy, resources or XP. Native `small_expenditure`/`medium_expenditure`/`large_expenditure` are real references (`00_budget_effects.txt:1455–1481`) but their .2/.4/.6% GDP tiers are not a substitute for project calibration.

Native domestic-helper reference charges in `MD:00_scripted_effects.txt` are civilian factory 7.5 (:235), arms factory 7.5 (:16), dockyard 7.5 (:607), infrastructure 3.5 (:454), office project 12 (:724), fossil power plant 3.25 (:1911) and agriculture district 3.75 (:2083), in MD billions. The office helper additionally builds a power plant. These values are comparison data in the final catalogue, not automatic price floors. `IMP_1970_gdp_scripted_effects.txt:1729` sets Iraq's GDP target to 3.281 and :1829–1830 applies its base adjustment; `00_money_system.txt:6150` onward consumes it. Thus a literal 7.5-billion charge would be approximately 229% of starting MD GDP. No universal 1970 capital-price factor was established in this helper/treasury path. Native budget and building-capacity playtests remain required; no historical real-dollar equivalence is asserted.

## Party programme activation, removal and return

Classify every reward before coding:

| Ownership | Examples | Departure and return |
|---|---|---|
| Permanent national development | Completed schools, paid factories, infrastructure, literacy gain, durable sector improvements | Persist; no further grant on refresh. Political closure cannot unbuild the factory. |
| Party-bound programme | Baath mobilization or ICP planning policy | Earned country variables persist; dynamic modifier becomes inactive/off the list when the exact party no longer governs; returns when the party returns. |
| Leader-bound programme | Bakr, Saddam and Aziz Muhammad policies | Require exact governing party **and actual installed leader**. A candidature or upcoming successor is insufficient. |
| Coalition bargain | Legal Front guarantees and cabinet collaboration | Require the current real coalition and bargain flags, with their specific removal conditions. Does not grant the coalition junior's sovereign-government route. |
| Temporary burden | Nationalization disruption, transition audit, construction mobilization | Timed once; expires normally and does not restart because of a refresh. |
| Conditional national problem | Northern conflict or frontier dispute | Follow problem/settlement state, not the name of the ruler. A defeated party cannot erase an unresolved national conflict. |

There are two real MD patterns that support the user's request:

1. Native Russia: `MD:common/scripted_effects/99_SOV_scripted_effects.txt:10968–11058`, `SOV_update_political_modifiers`, removes existing **political** dynamic modifiers and reattaches those whose earned focus/flag and current party qualify. Backing country variables survive. The common `change_ruling_party_effect` pipeline at `MD:common/scripted_effects/00_MD_politicsview_scripted_effects.txt:2050` calls this for Russia even on subparty changes inside the same outlook. This is the strongest native example for removing/restoring visible spirits.
2. Local Cold War: `common/dynamic_modifiers/mdcw_1970_generic_party_programmes.txt:1–14` and `COLDWAR_SOV_1970_dynamic_modifiers.txt:183–224` keep programme variables and use an exact party/leader `enable` block. Soviet office installers clear authoritative office flags, install the leader and call `force_update_dynamic_modifier` (`COLDWAR_SOV_1970_scripted_effects.txt:378–435`). Disabled dynamics should be runtime-checked for visible hiding versus merely zero effects.

Recommended Iraq architecture is a native Russia-style `COLDWAR_IRQ_refresh_programmes`, with defensive `enable` conditions too. It removes/readds only Iraq's political programme modifiers from an explicit list after evaluating `ruling_party`, actual leader and earned focus variables. Permanent-sector dynamics are separate. Execute after an Iraqi party change through the common helper, after actual leader installation, during Iraq initialization and a lightweight weekly resync. `on_government_change` alone is insufficient: same-outlook subparty changes will not necessarily invoke it. Save/load and delayed-event resync remain engine tests.

Example proposed programme definition, **not installed code**:

```hoi4
COLDWAR_IRQ_icp_aziz_programme = {
    icon = GFX_idea_communism
    enable = {
        original_tag = IRQ
        emerging_communist_state_are_in_power = yes
        has_country_leader = { name = "Aziz Muhammad" ruling_only = yes }
    }
    research_speed_factor = COLDWAR_IRQ_aziz_research_speed_factor
    bureaucracy_cost_multiplier_modifier = COLDWAR_IRQ_aziz_admin_cost
}
```

Focus availability also reads exact governing party and actual leader. National outlook roots can prepare an opposition/civic change, but cannot be a mandatory ceremonial “unlock” above an already ruling party. Completed choices persist. Leadership branches are not all permanently mutually exclusive: a completed Bakr programme can be dormant while Saddam rules and resume only if an authorized living Bakr actually returns. Contradictory permanent domestic choices still need explicit exclusions or a costed reversal mechanism.

## Proposed starting problems and overlap audit

These are candidate Iraq-specific effects **in addition to** whatever native laws are deliberately initialized. They have not been added to loaded ideas. Avoid double-counting the same impairment through a new spirit, high corruption law, native education modifier and Imperia development tier.

| Proposed searchable ID / English title | Balance proposal | Removal or change |
|---|---|---|
| `COLDWAR_IRQ_july_state` / The July State | PP factor+.08; drift defence+.15; stability−.08; bureaucracy cost+.08 | Baath regime-bound; negotiated opening reduces coercive penalties, security consolidation retains costs. It cannot stay fully active under an ICP or constitutional government. |
| `COLDWAR_IRQ_unsettled_north` / An Unsettled North | Stability−.12; army personnel cost+.10; supply consumption+.04 | National problem; autonomy or genuine settlement changes stages. A merely signed promise should not remove all costs instantly. |
| `COLDWAR_IRQ_ipc_concessions` / The Concession Economy | Oil-export income modifier−.18 | Ends through a real nationalization/compensation contract or renegotiated concession; transitional marketing burden is separate. No1970 oil boom yet. |
| `COLDWAR_IRQ_unfinished_rural_reform` / Unfinished Rural Reform | Agriculture productivity−.12; consumer-goods factor+.03 | Irrigation, land administration and cooperative/private choices can improve it. Use actual agriculture-sector effects, not a factory-output bonus called agrarian reform. |
| Native education spirit / Literacy and Technical Capacity | **No duplicate invented “research−.08/efficiency−.06” spirit.** Initialize native literacy only after source/balance choice. | Paid education decisions improve native literacy over time; direct temporary technical-school research programme may exist with a distinct rationale. |
| `COLDWAR_IRQ_patronage_networks` / Patronage Networks | Bureaucracy cost+.10; tax gain−.06; army organization−.05 | Civil-service audit, procurement reform and professional command choices reduce stages. Check against deliberately selected corruption law; reduce overlap before release. |
| `COLDWAR_IRQ_shatt_frontier` / A Contested River Frontier | Army personnel cost+.05; outward foreign influence−.05 | Conditional while the border dispute/escalation persists; diplomatic settlement deactivates. This is the selected diplomatic-cost abstraction, not a defender-resistance modifier. Do not lock it permanently to1975 or replay on a government change. |

Aggregate proposed custom baseline before native laws: stability−.20, bureaucracy cost+.18, army personnel cost+.15, tax−.06, oil-export multiplier−.18, agricultural productivity−.12, organization−.05, supply consumption+.04, consumer goods+.03; July State additionally PP+.08 and drift defence+.15. This is already severe for a poor state, and native literacy/development/corruption may add more. A January1970 engine snapshot and several-year budget test must determine final values; no blanket “balanced” claim is justified.

The existing Imperia development system can already penalize poor productivity and raise borrowing costs (`mdcw_imperia_development_effects.txt:1–160` and its dynamic modifiers). Therefore no extra generic “backward country” spirit should add another interest penalty merely to restate poverty. Native corruption-law reductions already improve taxes, investment and other outcomes; don't award the entire anticipated benefit again as a separate permanent modifier.

## State/resource and building geography

The following19 states have an explicit1970 Iraqi-owner override. This is verified geography, not ownership imported from a2000 focus tree. Resource quantities below are the source's current base map units; they are not barrels or guaranteed extracted/exported amounts.

| State ID | Current name/use | Base resources |
|---|---|---|
|164 | Iraqi Kurdistan / Erbil | oil4 |
|165 | Kirkuk | oil4 |
|166 | Nineveh / Mosul | oil2 |
|167 | Salahuddin | none |
|168 | Anbar | none |
|169 | Najaf | none |
|170 | Diyala / Khanaqin region | oil5 |
|171 | Basrah / Umm Qasr | oil39 |
|557 | Babylon / Baghdad capital | none |
|630 | Sulaymaniyah | none |
|633 | Dohuk | none |
|641 | Sinjar | none |
|1078 | Halabjah | none |
|1122 | Muthanna | none |
|1123 | Dhi Qar | none |
|1124 | Maysan | oil9 |
|1141 | Wasit | oil4 |
|1142 | Qadisiyah | none |
|1143 | Karbala | none |

Map oil sums67 units across these files. Do not mechanically “fix” Kirkuk's low source number or transfer fields from another state during this concept; a resource rebalance is a separate decision. Native `is_iraq_state_owned` at `common/scripted_triggers/MD_regional_owned_triggers.txt:1756` omits1078; do not use it as a complete1970 geography whitelist.

Three representative overlays matter:

- `history/states/557-Babylon.txt:34–55`:1970 sets industrial complex0, arms factory0, offices1, fossil power plant0; inherited infrastructure2, airbase5 remain unless another startup helper changes them. State productivity488.621.
- `history/states/171-Basrah.txt:45–64`:1970 sets arms0, offices0, fossil plant0; inherited infrastructure1, airbase2, navalbase2 at province9045 remain. State productivity307.933.
- `history/states/165-Kirkuk.txt:30–40`:1970 civilian factories0; state productivity251.309.

Fossil capacity is later rebuilt by the existing historical-demand helper; do not mistake a history zero for the final initialized power capacity. Proposed ports should target verified coastal province9045 and guarded state ownership. Kurdistan autonomy must distinguish IRQ-controlled state decentralization from creating/releasing KUR/PUK countries; national focus completion cannot silently redraw another player's borders.

## Imperia and Cold War integration boundaries

- Preserve `imp_eco_progress_calc` and its productivity-driven development tiers. Startup/monthly integration is at `common/on_actions/zzzzzz_mdcw_imperia_development_on_actions.txt:2–3`; paid productivity/education reforms should feed this actual system.
- `globalism_equilibrium` should alter the established gradual globalism mechanism. Calling a modifier refresh is not equivalent to immediately adding the target amount to actual globalism.
- Cold War influence/assistance and ideological-defence are separate from ordinary party support, stability and drift defence. Use the registry's consumer-backed exact keys and current scenario initialization.
- The refugee system at `common/scripted_effects/imp_refugees_effects.txt:6–88` already derives displacement from contested-state population. Do not call the whole refugee calculation repeatedly to manufacture casualties or duplicate a weekly tick. New repression events would need a carefully scoped population/accounting contract, not invented magic manpower effects.
- Foreign oil agreements, purchases, debt forgiveness, bases and peace offers require a recipient-response contract: propose→accept/refuse/expire→check present ownership/government→charge payer once→grant once→feedback→clear pending flags. Mere event delivery cannot stand for agreement.
- Do not automatically award Iranian/Kuwayti/Syrian territory, oil, cores or factories. No global reset of other countries' party or diplomatic systems. One-time cooperation benefits remain signature-guarded if government programmes are later restored.

## Required checks before approval can become implementation

This concept's APIs and historical identities are source-audited; it has no emitted Iraqi focus file. Later implementation needs transitive IDs, localization, idea and dynamic ownership validation; exact party roster integration; province/state guard checks; grouped-prerequisite and exclusion reachability; programme deactivation/reactivation without repeated buildings/cash; exact visible native tooltips; and an HOI4 January1970 start, government changes both ways, leader changes, save/reload and representative multiplayer offers.

The user's boundary remains: visualize and obtain approval before writing loaded Iraqi gameplay content. This document and other design/preview files are preparation for that review.
