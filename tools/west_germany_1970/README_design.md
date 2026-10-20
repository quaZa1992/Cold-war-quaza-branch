# West Germany 1970 (COLDWAR_GER_1970)

Content for the Federal Republic in the 1970 scenario:

- a focus tree of 235 focuses in eight pillars, built after MD's Russia and Israel trees;
- two windows on the top bar, *Inner-German Relations* and *Internal Security*;
- a monthly simulation of Bonn politics, terrorism and the GDR;
- 141 events, decisions, national spirits, portraits and Imperia hooks.

It only runs when `original_tag = GER` and `IMP_is_1970_scenario = yes`. The 1985 and 2000 content for Germany is untouched.

Nothing in the German question is fixed to a date. Crises, détente, the GDR's collapse, unity and even war come from the numbers and the player's choices.

## Files

| File | Content |
|---|---|
| `common/national_focus/COLDWAR_GER_1970_focus.txt` | the focus tree |
| `common/scripted_effects/COLDWAR_GER_1970_effects.txt` | setup, monthly tick, Bundestag, terror model, GDR model, unity, Imperia wrappers, leaders, core spirits |
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
- **Costs.** 1 for hubs, 2 for quick political steps, 3 as standard, 5 for reforms, 7 for great projects (*Aufbau Ost*). The average cost is about 3.
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

`python3 preview.py <dir>` renders the tree as PNGs.

## Bundestag arithmetic

Seats, majorities, coalition talks and every vote that needs a majority (ratification, the deployment vote, the constructive vote of no confidence) use the **last federal election result** (MD's `party_pop_elect_array`, written by `hold_elections`), not today's polls. Between elections the Bundestag only changes through coalition changes and defectors. The *Greens in the Bundestag* focus needs the Greens above 5% at the last election.

## Inner-German Relations (mini-game)

This is a two-player game between Bonn and East Berlin, built for multiplayer roleplay: both sides can be human. A human East Berlin answers crises through events (`COLDWAR_GGR.200`-`.230`) and plays its levers and the NVA alert level through the decision category *Policy Towards Bonn*; an AI East Berlin uses the SED leader's personality. There are no hidden standing or backing scores: outcomes follow from what the players actually chose. All state is in `cwgg_*` variables on GER.

### Climate and the escalation ladder

**Climate** runs from -100 to +100. It moves 5% a month towards a base, minus 3% of the escalation pressure. The base adds up:

- the treaties in force (+4 each);
- open channels (+2 each);
- world tension (Imperia);
- the SED leader;
- Moscow's line (Soviet 1970 tree);
- the government in Bonn;
- the NATO double-track decision and the zero option;
- the Deutschlandpolitik course and the focus tree.

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
| Rounds | Every six months, resolved by the monthly tick (no recurring hidden events). Bonn chooses one of seven stances. East Berlin answers secretly with one of five: a human picks it by event, the AI weighs its leader, its hard-currency need, Moscow's guarantee and Bonn's alert level. A payoff matrix sets the change of intensity. Each type has a best answer and a special action. Crises last 2-4 rounds |
| End | Intensity 0, or running out of rounds below 50, settles the crisis: whoever gave way in the last round loses it, otherwise it ends in a compromise. Above 50 it freezes and may flare up again. Intensity 100 means the brink |
| The brink | Give way, show resolve (a three-month countdown, one step a month, in which either side may give way), or ask the superpowers to mediate (hotline or NATO membership). If nobody gives way, a human East Berlin decides between Moscow's restraint and war; for an AI East Berlin a human Soviet Union decides, and with both AI Moscow always reins East Berlin in |

### Troops at the border

The divisions each side has in its border states are counted with the vanilla trigger `divisions_in_state` (Bonn: Schleswig-Holstein, Lower Saxony, Hesse, Franconia, Bavaria, West Berlin; East Berlin: Mecklenburg, Saxony-Anhalt, Thuringia, Saxony, Brandenburg, East Berlin): exact up to six per state, approximate above, capped at 30. The count is refreshed with the window and every month. 4 / 10 / 20 divisions in all border states together make the build-up levels *concentration*, *deployment in force* and *massive deployment*. Each level raises escalation pressure (+3 / +6 / +10 a month), costs climate (-1 / -2 / -4) and, from level 2, raises Cold War world tension (+0.25 / +0.5). A deployment in force by either side holds the ladder at *Crisis* or worse, both sides at *Confrontation*, both massively deployed at *War Danger*. The other side gets an event when the build-up grows. Border exercises, a first strike, brotherly help and East Berlin's attack need troops at the border.

### Levers, channels and treaties

- **Initiative.** Up to 6 points; every action costs initiative.
- **Bonn's levers.** Six levers: hard currency, people, media, legal position, alliance, trade. They carry 13 actions, including the Swing, the billion-mark credit, prisoner buy-outs, transit payments, the media offensive, a credit freeze, escape helpers, border exercises, rolling up Stasi networks and alert levels.
- **East Berlin's levers.** Four levers: transit, compulsory exchange, Stasi, border regime. An AI GDR uses them between crises; a human GDR uses the decisions *Raise the Compulsory Exchange*, *Harass the Transit Routes*, *Strengthen the Border Installations*, *HVA Offensive*, *Win Another Recognition*, *A Gesture of Goodwill*, *Ask Bonn for a Credit* and *Close the Access Routes*.
- **Channels.** Six channels. The Stasi can tap them; a raid secures them again.
- **Treaties.** A ladder of nine, from the Erfurt/Kassel meeting to a treaty community. Each is negotiated over months and the Bundestag must ratify the ones that change the legal position. They fire the existing events (Erfurt, the Basic Treaty, the Karlsruhe ruling, Honecker in Bonn).

### War paths

There are four. Nobody is pulled into the war automatically except an AI Soviet Union that still guarantees the GDR; NATO governments and a human Soviet Union decide for themselves. An AI GDR without Moscow's guarantee leaves the Warsaw Pact faction.

| Path | Trigger |
|---|---|
| A | Bonn strikes first. Needs *The Liberation Doctrine*, the countdown, alert level 3 and climate -80 |
| B | East Berlin attacks at the end of a countdown, only on a human order: a human GDR (Moscow's guarantee 60, NVA alert 2) or, for an AI GDR, a human Soviet Union (NVA alert 2). An AI GDR never starts this war |
| C | Brotherly help for a rising in the GDR |
| D | A false alarm during a manoeuvre crisis with both armies on alert 3. The hotline helps. Never between two human players |

The war brings:

- the state of defence (Art. 115a);
- a threshold event with a ceasefire offer;
- unity by force, defeat (West Berlin lost, neutrality) or an armistice.

### Links and balancing

Links to the old meters:

- `cwger_ostpolitik` follows the climate.
- Old effects on it are folded into the climate.
- The GDR meters serve as levers and shape East Berlin's behaviour.

`python3 simulate_rivalry.py [ai|hawk]` is a Monte Carlo model of the tick:

| Run | Result |
|---|---|
| Historical AI | About 2-3 crises up to 1990, mostly ending in compromise; practically no war (0.05%). Treaties 1–6 in 1970–1975, the state visit around 1985 |
| A player who always holds firm on the confrontation path | About 2-3 brinks in 20 years. Against an AI GDR and AI Soviet Union no war follows unless Bonn strikes first (path A) |

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
| Soviet 1970 tree | Doctrine focuses move Moscow's guarantee and the climate base; Moscow and Helsinki hooks; the Berlin flag; the gas deal |

## Integration edits to existing files

Unchanged from the first version. `history/countries/GER - Germany.txt` loads the tree and calls `COLDWAR_GER_1970_setup_politics`. The leader setup dispatches to `COLDWAR_GER_1970_set_leader`. GER is exempt from the generic 1970 tree, and two modern-day decision categories are hidden in 1970. `tools/west_germany_1970/integration/apply.py` makes these edits.

## Rebuilding

```
cd tools/west_germany_1970
python3 compile.py ../..                    # generated files, sprites included
python3 integration/apply.py ../.. ../..    # integration edits (safe to repeat)
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
