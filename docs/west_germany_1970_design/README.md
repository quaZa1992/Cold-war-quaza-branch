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
| `interface/COLDWAR_GER_1970_windows.gui`, `.gfx` | window layout and sprites; frame, tabs, buttons and bar tracks reuse `gfx/interface/mdcw_cold_war` |
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

## Inner-German Relations (mini-game)

This is a two-player game between Bonn and East Berlin. East Berlin is an AI with the SED leader's personality. All state is in `cwgg_*` variables on GER.

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

Each stage sets stability, war support, consumer goods and factory output in both German states, and changes Imperia world tension every month. *War Danger* lifts world tension to at least 70.

### Crises

| Item | Detail |
|---|---|
| Types | Transit, border incident, spy affair, embassy refugees, recognition, missiles, manoeuvre, dissidents, Elbe border, uprising |
| How they start | A monthly roll that grows with bad climate and high pressure. Some have fixed causes: the double-track decision, world tension above 80, a GDR exit wave, a second rising after a crackdown |
| Rounds | Every 15 days. Bonn chooses one of seven stances. East Berlin answers secretly with one of five, weighted by its leader, its hard-currency need, Moscow's guarantee, Bonn's alert level and the standing in the crisis. A payoff matrix sets intensity and standing. Each type has a best answer and a special action |
| End | Intensity 0 means resolved. When the rounds run out, the side with more standing wins below intensity 50; otherwise the crisis freezes. Intensity 100 means the brink |
| The brink | Give way, show resolve (a 30-day countdown in which East Berlin may blink), or ask the superpowers to mediate. If nobody gives way, Moscow restrains East Berlin or East Berlin attacks |

### Levers, channels and treaties

- **Initiative.** Up to 6 points; every action costs initiative.
- **Bonn's levers.** Six levers: hard currency, people, media, legal position, alliance, trade. They carry 13 actions, including the Swing, the billion-mark credit, prisoner buy-outs, transit payments, the media offensive, a credit freeze, escape helpers, border exercises, rolling up Stasi networks and alert levels.
- **East Berlin's levers.** Four levers, used by its AI between crises: transit, compulsory exchange, Stasi, border regime.
- **Channels.** Six channels. The Stasi can tap them; a raid secures them again.
- **Treaties.** A ladder of nine, from the Erfurt/Kassel meeting to a treaty community. Each is negotiated over months and the Bundestag must ratify the ones that change the legal position. They fire the existing events (Erfurt, the Basic Treaty, the Karlsruhe ruling, Honecker in Bonn).

### War paths

There are four. NATO joins a war Bonn starts only with Western backing of at least 70. The Soviet Union only fights for a GDR it still guarantees.

| Path | Trigger |
|---|---|
| A | Bonn strikes first. Needs *The Liberation Doctrine*, the countdown, alert level 3 and climate -80 |
| B | East Berlin attacks at the end of a countdown. Needs a strong Moscow guarantee, more likely with hard-liners in Moscow |
| C | Brotherly help for a rising in the GDR |
| D | A false alarm during a manoeuvre crisis with both armies on alert 3. The hotline helps |

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
| Historical AI | About 3 crises up to 1990, no war. Treaties 1–6 in 1971–1976, the state visit around 1985 |
| A player who always holds firm on the confrontation path | About 5 brinks in 20 years and a war in roughly one game in five |

## Internal Security

The window has four tabs. All state is in `cwsec_*` variables plus the existing terror variables.

| Tab | Content |
|---|---|
| Situation | Threat bars (RAF, right-wing, foreign), the RAF's generation, cadre, milieu and prisoners, BKA/GSG 9 capability, the balance of security state and rule of law, a situation report |
| Manhunt | Six wanted cards per generation, each with a trace value: generations 1 and 2 by name, generation 3 anonymous. Access raids, dragnet, reward, wanted posters, crown witness, informant, exit programme |
| Protection | The RAF plans against six target categories, weighted by generation. Protection details halve the planning and foil 65–75% of attacks. BKA levels reveal where (level 1) and how far (level 2) |
| Prisons & Crisis Staff | Prison regime (isolation, normal, association), hunger strike, force-feeding. The hostage crisis on its own clock: storm, raid, contact ban, play for time, give in. Policy actions: Kinkel initiative, bans, counter-espionage |

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
| `gui.py`, `gui_sprites.py` | window DSL and sprites |
| `systems.py`, `mechanics.py` | monthly simulation, missions, leaders |
| `events_ger.py`, `events_ddr.py`, `decisions.py`, `ideas.py`, `icons.py`, `hooks.py`, `tooltips.py` | events, decisions, spirits, focus icons, links to mod systems, generated tooltips |

`old_focus_text.json` keeps the texts of the first tree, which `tree.py` reuses by key.
