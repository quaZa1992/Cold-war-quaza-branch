IMPERIA COLD WAR — West Germany 1970 (COLDWAR_GER_1970)

Current multiplayer balance and two-month crisis rounds are documented in [BALANCE_IMPLEMENTATION.md](BALANCE_IMPLEMENTATION.md).

Content for the Federal Republic in the 1970 scenario:

- a focus tree of 417 focuses in eight pillars, built after MD's Russia and Israel trees;
- two launchers beside faction membership in the politics panel, *Inner-German Relations* and *Internal Security* (DDR: *Domestic Affairs*);
- an East Berlin perspective on the shared Inner-German Relations file, with DDR policy controls;
- monthly Bonn institutions, security and bilateral-pressure systems;
- 360 events, decisions, national spirits, portraits and Imperia hooks.

It only runs when `original_tag = GER` and `IMP_is_1970_scenario = yes`. The 1985 and 2000 content for Germany is untouched.

The West German focus tree and selectable policies remain player-paced. For a human BRD–DDR game, the old GER-authored Honecker appointment, Wall/Wende and collapse chains, scheduled BRD leadership stories, and unilateral DDR unity annexation are retired. Political alternatives still available through explicit focus or event choices are guarded by current party and leadership conditions. The native DDR tree owns DDR leadership and government choices; its historical mortality events apply only to AI-controlled DDR. Historical dated world flavor, regular elections, and genuine condition-driven crisis consequences remain. The German two-player bridge reads the current native DDR border ladder for border-opening checks; it does not infer a border or government outcome from a historical date or an obsolete proxy.

## Files

| File | Content |
|---|---|
| `common/national_focus/COLDWAR_GER_1970_focus.txt` | the focus tree |
| `common/scripted_effects/COLDWAR_GER_1970_effects.txt` | setup, monthly tick, Bundestag, security and bilateral-pressure models, negotiated unity, Imperia wrappers, core spirits |
| `common/scripted_effects/COLDWAR_GER_1970_windows_effects.txt` | the rivalry mini-game, internal security, window refresh |
| `common/scripted_triggers/COLDWAR_GER_1970_windows_triggers.txt` | availability of every window action |
| `common/scripted_guis/COLDWAR_GER_1970_windows.txt` | scripted GUIs of both windows and their top-bar buttons |
| `common/scripted_localisation/COLDWAR_GER_1970_windows.txt` | dynamic texts (stages, crisis names, situation reports, wanted list) |
| `interface/COLDWAR_GER_1970_windows.gui`, `.gfx` | window layout and sprites in a file-folder ("Akte") skin drawn by `akte_sprites.py`: khaki chancellery file with Bundesadler and GDR emblem, grey-green BKA file with GEHEIM marking |
| `gfx/interface/cwger_1970/*.dds` | sprites drawn by `gui_sprites.py` |
| `events/COLDWAR_GER_1970_events.txt` | namespaces `COLDWAR_GER`, `COLDWAR_DDR`, `COLDWAR_GGR` (rivalry), `COLDWAR_GSEC` (security) |
| `common/decisions/...COLDWAR_GER_1970_*` | decision categories; window actions are no longer duplicated as decisions |
| `common/dynamic_modifiers/...` | state of the republic, inner-German relations (GER and GDR), eight core spirits, state modifiers |
| `common/ideas`, `common/bop`, `common/on_actions` | spirits, Deutschlandpolitik balance of power, startup and monthly hooks |

## The focus tree

The tree follows the conventions of MD's Russia and Israel trees:

- **Hubs.** A root focus (*The Government Statement*) opens eight hub focuses, one per pillar. Every other focus is placed with `relative_position_id`.
- **Focus duration.** The catalogue retains its relative design weights. Weights 1–2 take 35 days; ordinary steps and reforms (weights 3–5) take 70 days; existing weight-7 projects (*Aufbau Ost*) retain 98 days. HOI4's `NFocus.FOCUS_POINT_DAYS = 7` means emitted costs of 5, 10 and 14. The 417 focuses comprise 129 at 35 days, 285 at 70 days and 3 at 98 days.
- **Player-paced availability.** Focuses have no calendar requirements, calendar alternatives, era locks or date-expiry bypasses. Government, parliamentary, treaty, security, unity and other real gameplay conditions remain. Post-opening branches require actual border opening or unity. Unity talks retain 36 months of achieved détente and their treaty requirements. The euro programme uses the native MD currency effect without waiting for 1999. Nuclear safety, the environment ministry, GSG 9 and a renunciation offer do not wait for historically dated incidents or a scheduled RAF generation. Dated world flavor remains; crisis and foreign-consent outcomes follow live conditions and player choices.

- **Core spirits.** Eight dynamic modifiers grow focus by focus. Each reward shows a *Modifies …* block, as MD's `modifies_dynamic_modifier_tt` does. The variables are `cwfo_<core>_<modifier>`.

  | Core spirit | Pillar | Modifiers |
  |---|---|---|
  | The Chancellor's Office | The Chancellery | stability, political power, drift defence, bureaucracy costs |
  | Modell Deutschland | Economy | productivity growth, consumer goods, factory output, tax revenue, social costs, construction speed |
  | The Energy Mix | Energy | energy production, fossil fuel use, nuclear and renewable energy, energy use (MD energy system) |
  | Militant Democracy | Internal security | terror detection and defence (MD counter-terror), police costs, foreign influence defence |
  | An Army in the Alliance | Bundeswehr | organisation, core defence, army experience, recruitable population, equipment costs, planning |
  | Anchored in the West | Western integration | trade opinion, research, europeanism drift (MD EU), ideological defence (Cold War), opinion gain |
  | Deutschlandpolitik | Deutschlandpolitik | stability, war support, consumer goods, sanction resistance (Imperia). Its face changes with the policy: *Change through Rapprochement* or *Policy of Strength* |
  | A Civilian Power | World role | Imperia assistance capacity and effectiveness, political support effectiveness, international market income |

- **Concrete effects.**
  - **Buildings in named states.** Ruhr (NRW), Bavaria, Baden-Württemberg, Hesse, Hamburg, Schleswig-Holstein, Saarland, Lower Saxony, West Berlin, and East German states after unity.
  - **State modifiers.** Showcase of the West, Bavarian Model, Structural Change in the Ruhr, Capital Berlin and others.
  - **Railways.** Hannover–Würzburg, Mannheim–Stuttgart, Cologne–Frankfurt and Hannover–Berlin.
  - **MD influence** in France, the Benelux countries, Italy, Poland, Czechoslovakia, Brazil, Africa and the Middle East.
  - **Other systems.** MD internal factions (DGB, BDI, Mittelstand), treasury and debt, taxes, technology, opinions, and the Deutschlandpolitik balance of power.
- **Unlocks.** Focuses unlock window functions, for example:
  - channels: Bahr–Kohl, Vogel, Koko, church, hotline;
  - levers, and treaty negotiations;
  - border exercises and the third alert level;
  - BKA levels, GSG 9 tiers and protection details;
  - the dragnet, crown witness and exit programme.
- **Paths.** The pillars are:
  - **Chancellery:** social-liberal reforms, the FDP's course, the Union's road to the 1982 change of government, the Greens, institutions, and governments only some histories produce (Barzel, Strauß, Späth, Lafontaine, Schmidt alone, grand coalition).
  - **Deutschlandpolitik:** *Change through Rapprochement* and *Policy of Strength* exclude each other. *The Legal Position* combines with either. The confrontation branch ends in *The Liberation Doctrine* (`will_lead_to_war_with = DDR`). Unity comes at the bottom.
  - **Militant Democracy:** *The Strong State* or *The Liberal Rule of Law*.
  - **Bundeswehr:** *Forward Defence* and *Prepare the State of Defence* feed the rivalry window.
- **AI.** `ai_will_do` follows the historical path. The AI never takes the confrontation branch or the war focuses.

The preventive environmental wording draws on the Federal Republic's [1971 environmental programme](https://dserver.bundestag.de/btd/06/027/0602710.pdf) and its [precaution, polluter-pays and cooperation principles](https://www.bundesumweltministerium.de/meldung/50-jahre-umweltprogramm). Historically the separate environment ministry [followed Chernobyl in 1986](https://www.bundesumweltministerium.de/ministerium/geschichte/umweltpolitische-meilensteine-von-1986-bis-heute), while GSG 9 [was founded after Munich on 26 September 1972](https://www.komm-zur-bundespolizei.de/sechs-meilensteine-in-der-geschichte-der-bundespolizei/). Choosing either institution earlier is an alternate-history policy choice; the existing benefits and trade-offs are retained.

Focus-linked political sources retain their substantive conditions: a Barzel government requires the successful confidence vote and his leadership; a CSU split requires its existing opposition/autonomy conditions and the player's split decision. Refugee-policy branches accept either an existing asylum surge or current `imp_refugee_pressure > 0.15`, matching the existing scheduler's pressure threshold without its year requirement. The Greens' parliamentary entry retains the established-party and last-election threshold checks without waiting for a dated founding event.

Direct decisions and window actions likewise retain their gameplay requirements without year locks: the Federal Reform Commission follows the constitutional focus; East Berlin's socialist opening requires an SED government; the cultural agreement retains treaty progress and climate requirements; the PKK ban retains its current-threat and prior-ban checks. The trust and alignment point mechanics have been removed; see [DDR_RELATIONS.md](DDR_RELATIONS.md). Other calendar weights in AI behaviour, random incident scheduling and passive historical simulation remain.

`python3 preview.py <dir>` renders the tree as PNGs.

## Bundestag arithmetic

Seats, majorities, coalition talks and every vote that needs a majority (ratification, the deployment vote, the constructive vote of no confidence) use the **last federal election result** (MD's `party_pop_elect_array`, written by `hold_elections`), not today's polls. Between elections the Bundestag only changes through coalition changes and defectors. The *Greens in the Bundestag* focus needs the Greens above 5% at the last election.

## Inner-German Relations (mini-game)

This is a two-player game between Bonn and East Berlin, built for multiplayer roleplay: both sides can be human. A human East Berlin answers crises through events (`COLDWAR_GGR.200`-`.230`) and plays its levers and the NVA alert level through the decision category *Policy Towards Bonn*; an AI East Berlin uses the SED leader's personality. There are no hidden standing or backing scores: outcomes follow from what the players actually chose. All state is in `cwgg_*` variables on GER.

### Climate and the escalation ladder

**Climate** runs from -100 to +100. It moves 5% a month towards a base, minus 3% of the escalation pressure. The base reflects:

- the treaties in force (+4 each);
- open channels (+2 each);
- world tension (Imperia);
- enacted Bonn policies and alliance choices;
- the NATO double-track decision and the zero option;
- the focus-tree policy choices.

DDR's native political course, government and leader remain under DDR control and do not directly drive the bilateral climate. The retired Moscow Guarantee and Wende/leader proxy scores are not climate inputs.

**Escalation ladder.** Seven stages, with hysteresis:

0. Modus Vivendi
1. Cool Coexistence
2. Tensions
3. Crisis
4. Confrontation
5. War Danger
6. War

Each stage sets stability, war support, consumer goods and factory output in both German states, and changes Cold War world tension (Imperia, `global.mdcw_cw_tension`) every month. *War Danger* lifts it to at least 70.

**Alert levels** of the Bundeswehr and the NVA (0-3) give mobilisation speed and war support step by step: +10%/+2%, +25%/+5%, +50%/+10%. Bonn raises its level in the window, a human GDR by decision.

### Crises

| Item | Detail |
|---|---|
| Types | Transit, border incident, spy affair, embassy refugees, recognition, missiles, manoeuvre, dissidents, Elbe border, uprising |
| How they start | A monthly roll that grows with bad climate and high pressure. Some have fixed causes: the double-track decision, world tension above 80, a GDR exit wave, a second rising after a crackdown |
| Rounds | Every two months, resolved by the monthly tick. Bonn chooses one of seven stances. When DDR is human, it submits its own order; the round remains pending until each human country has submitted. AI behavior is used only for AI-controlled countries and follows current economic, security and force conditions. A payoff matrix sets the change of intensity. Each type has a best answer and a special action. Crises last 2-4 rounds |
| End | Intensity 0, or running out of rounds below 50, settles the crisis: whoever gave way in the last round loses it, otherwise it ends in a compromise. Above 50 it freezes and may flare up again. Intensity 100 means the brink |
| The brink | Give way, show resolve (a three-month countdown, one step a month, in which either side may give way), or ask the superpowers to mediate (hotline or NATO membership). With two human German players, each country must submit its own readiness/order before a round resolves. A DDR attack requires an explicit DDR order and current Soviet-faction membership; a human Soviet Union is never called into war automatically |

### Troops at the border

The divisions each side has in its border states are counted with the vanilla trigger `divisions_in_state` (Bonn: Schleswig-Holstein, Lower Saxony, Hesse, Franconia, Bavaria, West Berlin; East Berlin: Mecklenburg, Saxony-Anhalt, Thuringia, Saxony, Brandenburg, East Berlin): exact up to six per state, approximate above, capped at 30. The count is refreshed with the window and every month. 4 / 10 / 20 divisions in all border states together make the build-up levels *concentration*, *deployment in force* and *massive deployment*. Each level raises escalation pressure (+3 / +6 / +10 a month), costs climate (-1 / -2 / -4) and, from level 2, raises Cold War world tension (+0.25 / +0.5). A deployment in force by either side holds the ladder at *Crisis* or worse, both sides at *Confrontation*, both massively deployed at *War Danger*. The other side gets an event when the build-up grows. Border exercises, a first strike, brotherly help and East Berlin's attack need troops at the border.

### Levers, channels and treaties

- **Initiative.** Up to 6 points; every action costs initiative.
- **Bonn's levers.** Six levers: hard currency, people, media, legal position, alliance, trade. They carry 13 actions, including the Swing, the billion-mark credit, prisoner buy-outs, transit payments, the media offensive, a credit freeze, escape helpers, border exercises, rolling up Stasi networks and alert levels.
- **East Berlin's levers.** Four levers: transit, compulsory exchange, Stasi, border regime. An AI GDR uses them between crises; a human GDR uses the decisions *Raise the Compulsory Exchange*, *Harass the Transit Routes*, *Strengthen the Border Installations*, *HVA Offensive*, *Win Another Recognition*, *A Gesture of Goodwill*, *Ask Bonn for a Credit* and *Close the Access Routes*.
- **Channels.** Six channels. The Stasi can tap them; a raid secures them again.
- **Treaties.** A ladder of nine, from the Erfurt/Kassel meeting to a treaty community. Either side can initiate each treaty for 25 political power and 2 of the initiator's own initiative, subject to the existing treaty requirements. Both countries must give explicit consent; a ready or deferred offer remains locked until accepted, refused or explicitly lapsed. No timeout signs a treaty for a player. The cooperative confederation flag and idea require valid bilateral Treaty 9 standing and do not make DDR a subject or alter its faction membership.

### War paths

War is reached only through a valid war path and current country/faction conditions. There is no guarantee-score route and no automatic Soviet call for a human-controlled USSR. Actual Soviet faction membership is checked where the DDR attack path requires it; NATO membership alone does not call NATO governments into the war.

| Path | Trigger |
|---|---|
| A | Bonn strikes first. Needs *The Liberation Doctrine*, the countdown, alert level 3 and climate -80 |
| B | A human East Berlin may order an attack at the end of a countdown when the current crisis, NVA alert and actual Soviet-faction membership requirements are met. The engine does not enlist a human USSR automatically |
| C | Brotherly help for a rising in the GDR |

A false alarm during a manoeuvre crisis can open a decision event, but it never declares war by itself. Bonn's armistice proposal is routed to DDR through the recipient event `COLDWAR_GGR.260`; DDR decides whether to accept or reject it.

The war brings:

- the state of defence (Art. 115a);
- a threshold event with a ceasefire offer;
- negotiated outcomes or an armistice response from DDR. There is no GER-owned automatic collapse or unity annexation chain.

### Links and balancing

Links to the old meters:

- `cwger_ostpolitik` follows the climate.
- Old effects on it are folded into the climate.
- The GDR meters serve as levers and shape East Berlin's behaviour.

`python3 simulate_rivalry.py [ai|hawk]` is an exploratory model of selected tick behaviors. Its results are not historical schedules or outcome guarantees and do not validate human consent, HOI4 behavior, multiplayer synchronization or frame time.

## Internal Security

The window has four tabs. All state is in `cwsec_*` variables plus the existing terror variables.

| Tab | Content |
|---|---|
| Situation | Threat bars (RAF, right-wing, foreign), the RAF's generation, cadre, milieu and prisoners, BKA/GSG 9 capability, the balance of security state and rule of law, a situation report |
| Manhunt | Six wanted cards per generation, each with a trace value: generations 1 and 2 by name, generation 3 anonymous. Access raids, dragnet, reward, wanted posters, crown witness, informant, exit programme |
| Protection | The RAF plans against six target categories, weighted by generation. *US Forces* is only a target while US divisions are stationed in a West German state. Protection details halve the planning and foil 65–75% of attacks. BKA levels reveal where (level 1) and how far (level 2) |
| Prisons & Crisis Staff | Prison regime (isolation, normal, association), hunger strike, force-feeding. The hostage crisis runs to a deadline (one scheduled event, no polling; contact ban and playing for time push it back): storm, raid, contact ban, play for time, give in. Policy actions: Kinkel initiative, bans, counter-espionage |

These connect to the rest of the content:

- **RAF attacks.** They now come from the planning model and no longer from a random roll.
- **Arrests.** Arrests from the old model mark the best-traced wanted card.
- **The Stasi.** A member who leaves the group after 1979 may go to the GDR. A Stasi raid in the rivalry window or the Stasi files after unity can uncover this.

## Links to existing mod systems

| System | Link |
|---|---|
| Imperia | Tension (ladder and events), assistance programmes, PPS, sanctions, refugees, oil shocks, arms demand, alignment, assistance and support modifiers in the core spirits |
| MD | Elections and coalitions, internal factions, treasury, debt and taxes, counter-terror modifiers, protests, corruption, EU europeanism, NATO, influence, energy modifiers |
| Soviet 1970 tree | Moscow and Helsinki hooks, the Berlin flag and the gas deal; no retired Moscow Guarantee score feeds the German sandbox |

## Integration edits to existing files

Unchanged from the first version. `history/countries/GER - Germany.txt` loads the tree and calls `COLDWAR_GER_1970_setup_politics`. The leader setup dispatches to `COLDWAR_GER_1970_set_leader`. GER is exempt from the generic 1970 tree, and two modern-day decision categories are hidden in 1970. `tools/west_germany_1970/integration/apply.py` makes these edits.

## Rebuilding

The runtime performance review and its focused regression commands are recorded in [PERFORMANCE.md](PERFORMANCE.md).

<!-- IMPERIA COLD WAR — Independent DDR politics and shared dossier access -->
The DDR-facing dossier, shared state ownership, historical policy references and bounded installer are documented in [DDR_RELATIONS.md](DDR_RELATIONS.md). The DDR retains its own national tree and political course. That course no longer feeds the bilateral climate, and the trust/alignment point mechanics are removed.

<!-- IMPERIA CW — Cold War: shared RAF case and bounded security build. -->
The RAF tree/cabinet/shared-file integration and focused build commands are recorded in [SECURITY_CONTRACT.md](SECURITY_CONTRACT.md). Use `compile_security.py` for a security-only installation into a live checkout with unrelated changes.

```
cd tools/west_germany_1970
python3 compile_sandbox.py --dry-run       # review bounded two-player sandbox changes
python3 compile_sandbox.py                 # apply only bounded sandbox nodes and files
python3 validate.py ../.. ../..             # references, localisation, sprites, GUI hooks, layout
python3 preview_gui.py ../.. <png dir> <out dir> [state.json]   # window mock-ups
python3 preview.py <out dir>                # focus tree PNGs
python3 simulate_rivalry.py                 # balancing model
```

| Module | Content |
|---|---|
| `tree.py`, `tree_pillars.py` | focus DSL, core spirits, state modifiers, and the focuses |
| `rivalry.py`, `events_rivalry.py` | inner-German mini-game and its events |
| `security.py` | internal security window, mechanics and events |
| `gui.py`, `gui_sprites.py`, `akte_sprites.py` | window DSL, sprites and the file-folder skin |
| `systems.py`, `mechanics.py` | monthly simulation, missions, leaders |
| `events_ger.py`, `events_ddr.py`, `decisions.py`, `ideas.py`, `icons.py`, `hooks.py`, `tooltips.py` | events, decisions, spirits, focus icons, links to mod systems, generated tooltips |

`old_focus_text.json` keeps the texts of the first tree, which `tree.py` reuses by key.
