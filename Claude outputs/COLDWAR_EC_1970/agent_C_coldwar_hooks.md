# Agent C – Andockpunkte und wiederverwendbare Muster aus Cold-War-/Imperia-Systemen für die Europäischen Gemeinschaften 1970

Stand: 18.10.2026 · Mod `mdcoldwar` (Arbeitskopie auf dem Nutzer-PC, nur gelesen) · Basis MD 1.12.3B + Imperia (`IMP_`/`imp_`) + Cold War (`mdcw_`/`COLDWAR_`)

**Legende**
- **[V] verifiziert**: im gestagten Code gelesen, Pfad und Zeile angegeben.
- **[Ve] vermutet**: aus Code-Mustern geschlossen, nicht vollständig im Code oder im Spiel geprüft.
- Pfade sind relativ zur Mod-Wurzel `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar`.
- Gelesene Projekt-Dokumente: `claude/mdcw_cold_war_system_as_built.md`, `claude/mdcw_cold_war_spec_v3.md`, `claude/mdcw_sov_1970_implementation.md`, `claude/mdcw_union_missions_concept.md`, `claude/mdcw_coding_playbook.md`. Dazu der historische Bericht `eu1970_history_report.md` (Abschnitte 0, 2, 6).

---

## 0. Kurzfassung

1. **Das EG-System sollte keine fünfte Blockausrichtung werden, sondern eine Organisationsschicht über der bestehenden West-Ausrichtung.** Die Cold-War-Blöcke stecken in `mdcw_cw_alignment` 0–3. Die Blockführer sind fest auf USA/SOV/CHI verdrahtet, und alles ist generiert (`tools/generate_mdcw_cold_war.py`). Ein vierter Block ist nur über den Generator machbar.
2. **Die Abstimmungs-Engine existiert dreimal** (Politbüro SOV, OPEC, UN/NATO). Das Politbüro-Muster (`COLDWAR_SOV_start_vote` / `_cast_vote` / `_tally_vote`, eingefrorene `last_*`-Kopien, Warteschlange) ist die beste Vorlage für einen EG-Ministerrat. Die Gewichte müssten auf 4/4/4/2/2/1 umgestellt und eine Veto-Logik ergänzt werden.
3. **Der Unionszusammenhalt** (`COLDWAR_SOV_union_cohesion`, 4 Stufen-Modifikatoren, Krisenschwellen) ist 1:1 als „Gemeinschaftsgeist“ übertragbar, dann aber als globale Variable.
4. **Die Demokratie-Klausel ist fast geschenkt:** `mdcw_cw_party_core_west` (Konservativ/Liberal/Sozialistisch, Index 1–3) trennt bereits Demokratien von GRE-Junta (22) und SPR/POR (21). Ein Einfrierhook passt über `on_ruling_party_change` und `on_coup_succeeded`.
5. **Größtes Risiko:** Der MD-EU-Start läuft auch 1970 ohne Szenario-Wächter. Er schreibt die 15 EU-Mitglieder von 2000 ins Array `global.EU_member` und gibt ihnen die modernen Ideen `foreign_data_kraken`/`asylum_shopping`. Betroffen sind auch GRE, SPR, POR, AUS, FIN und SWE.
6. **Mehrere Länderinhalte 1970 umgehen eine EG-Zustimmung:**
   - SPR tritt per Fokus-Event direkt bei (`add_ideas = EU_member`).
   - GRE-Fokusse versprechen im Text eine „Gegenpartei-Zustimmung“, gewähren aber einseitig. Wo es doch eine Gegenpartei gibt, ist es ENG statt der Sechs.
   - Auch CYP sendet seine Assoziierung an ENG.

---

## 1. Blocksystem

### 1.1 Datenmodell des Cold-War-Systems [V]

| Baustein | Ort | Inhalt |
|---|---|---|
| Ausrichtung | `mdcw_cw_alignment` (Länder-Variable) | 0 Blockfrei, 1 West, 2 Sowjet, 3 Peking. Gesetzt in `mdcw_cw_setup_country` (`common/scripted_effects/mdcw_cold_war_effects.txt:48-248`) |
| Startlisten 1970 | dort Z. 64-129 (West), 130-162 (Sowjet), 163-171 (Peking) | Alle übrigen Länder sind 0 |
| Mitgliederarrays | `global.mdcw_cw_members_na/_west/_soviet/_beijing` | Werden in `mdcw_cw_rebuild_blocs` (Z. 463-672) jeden Monat komplett neu gebaut, sortiert nach Rang 20/12/7/4/2/1 |
| Blockstärke | `global.mdcw_cw_power_0..3`, `_count_`, `_core_`, `_estranged_` | Aus den MD-Power-Rank-Ideen (`mdcw_cw_update_bloc_value`, Z. 251ff.) |
| Blockführer | `mdcw_cw_is_bloc_leader` (`common/scripted_triggers/mdcw_cold_war_triggers.txt:11-17`) | **fest** `original_tag = USA/SOV/CHI` |
| Ideologie-Filter | `mdcw_cw_party_fits_west` (Z. 62-78), `mdcw_cw_party_core_west` (Z. 81-87) und dieselben für Sowjet und Peking | Liest `ruling_party` (0–23). „Core West“ = 1/2/3 = demokratische Parteien |
| Entfremdung | `mdcw_cw_update_estrangement` (effects Z. 3794-3819) | Flag `mdcw_cw_estranged`, nach 365 Tagen gratis nach 0 |
| Blockwechsel | `mdcw_cw_change_alignment` (Z. 3626-3790) | PP-Kosten, Sperre 730 Tage, Untertanen folgen, Tension-Delta, Event `mdcw_cw.3` an den alten und neuen Führer |
| Blockeffekte | dynamische Modifikatoren `mdcw_cw_bloc_modifier_west` (`common/dynamic_modifiers/mdcw_cold_war_dynamic_modifiers.txt:68-87`) usw. | Variablenbasiert (`mdcw_cw_b_*`), monatlich neu |
| Weltlage | `global.mdcw_cw_tension`, Market Confidence, Arms Demand | `mdcw_cw_add_tension` (effects Z. 13-18) mit Klammer und Anzeige |
| Sanktions-Hook | `mdcw_cw_on_sanction_imposed` / `_lifted` (effects Z. 4301-4504 / 4507-4610) | Wird aus allen 8 Imperia-Sanktionsaktionen aufgerufen (`common/scripted_diplomatic_actions/imp_sanctions_diplomatic_actions.txt:47-49` usw.) |
| Kriegs-/Putsch-Hooks | `mdcw_cw_on_war_relation` (Z. 4788-4821), `mdcw_cw_on_coup` (Z. 4841-4851) | Eingebunden in `common/on_actions/mdcw_cold_war_on_actions.txt:45-72` |
| Szenario-Wächter | `IMP_is_1970_scenario` (`common/scripted_triggers/IMP_cold_war_scenario_triggers.txt`) | Start über `USA = { IMP_is_1970_scenario = yes }` (`mdcw_cold_war_on_actions.txt:8-19`) |

**Startausrichtung 1970 in Europa [V]** (effects Z. 66-126):
- **West (1):** BEL, DEN, FRA, ICE, ITA, LUX, HOL, NRY, POR, ENG, GRE, TUR, GER, SPR. Dazu USA/CAN und die Verbündeten in Übersee.
- **Sowjet (2):** SOV mit den SSRs, POL, DDR, CZE, HUN, BUL, ROM.
- **Peking (3):** CHI, ALB.
- **Blockfrei (0), weil auf keiner Liste:** AUS, SWI, SWE, FIN, IRE, MLT, CYP, YUG.

**Regierungen 1970 (History-Profile) [V]:**
- GRE: `national_autocracy` (Partei 22).
- SPR, POR: `national_fascist` (21).
- TUR, IRE, AUS, FIN, MLT, CYP, NRY, ICE, FRA, ITA, Benelux: `democratic_conservative`.
- ENG, GER, SWE, SWI: `democratic_socialist`.
- DEN: `democratic_liberal`.
- Quelle: `history/countries/<TAG> - *.txt`, Block `1970.1.1`, Z. ~15.

Folge: GRE, SPR und POR passen zum Westen (`fits_west` enthält 21/22), sind aber **keine Kernmitglieder** und senken die Kohäsion des Westblocks.

### 1.2 NATO und Warschauer Pakt als MD-Fraktionen [V/Ve]

- **NATO 1970 [V]** (`common/scripted_effects/IMP_1970_world_politics_effects.txt:1176-1224`):
  - `create_faction_from_template = faction_template_1985_nato` mit 14 Mitgliedern, **einschließlich FRA**.
  - Allen 15 wird die Idee `NATO_member` gegeben. Deren `on_add` füllt `global.nato_members` (`common/ideas/Factions.txt:5-23`).
  - Das Kommando-Austrittsjahr 1966 von Frankreich ist **nicht** abgebildet.
- **Artikel 5 [V]** (`common/on_actions/MD_NATO_on_actions.txt:12-50`): Bei einer Kriegserklärung gegen ein NATO-Mitglied werden **alle** NATO-Mitglieder per `add_to_war` hineingezogen, auch menschliche Spieler. Abschaltbar ist das nur über die Spielregel `GAME_RULE_nato_disabled`.
- **Warschauer Pakt:**
  - **[V]** In `IMP_1970_setup_global_alignment_internal` wird er nicht angelegt.
  - **[Ve]** Die Fraktion kommt aus der SOV-History oder aus MD-Events (`common/on_actions/99_SOV_on_actions.txt:48-59` prüft `faction_warsaw_pact_idea`).
  - **[V]** Die Array-Namen sind inkonsistent: `Warsaw_Pact_join` schreibt `global.Warsaw_Pact_member` (`common/scripted_effects/02_Warsaw_Pact_effects.txt:3`), das Aufräumen entfernt dagegen aus `global.WARSAW_PACT_member` (`common/scripted_effects/01_international_systems_effects.txt:2912`).
- **Cold-War-Blöcke und Fraktionen sind entkoppelt [V]** (as_built §0: „Bloc membership is independent from the NATO / Warsaw Pact factions“).

### 1.3 Wo die EG andockt

**Empfehlung: EG als Organisationsschicht, nicht als Ausrichtung 4 [Ve, Designvorschlag].**

| EG-Element | Andockpunkt im Bestand | Begründung |
|---|---|---|
| Mitgliedschaft | MD-Idee `EU_member` + `global.EU_member` (`common/ideas/Organizations.txt:4-37`) | Geldsystem, Collections und EU-Fenster lesen sie bereits |
| „Westeuropäischer Teilblock“ | Flag/Variable `EC_*` an Ländern mit `mdcw_cw_alignment = 1`. Wirkung über einen eigenen dynamischen Modifikator, der **nicht** in `mdcw_cw_bloc_modifier_west` eingreift | Cold-War-Dateien sind generiert („do not edit by hand“). Neue Werte also in einer eigenen Datei, wie es der SOV-Baum vormacht (`mdcw_cw_*`-Schlüssel nur lesen bzw. über `mdcw_cw_recalculate_country` neu rechnen lassen) |
| Demokratie-Klausel | `mdcw_cw_party_core_west = yes` (`mdcw_cold_war_triggers.txt:81-87`) | Trennt die Demokratien (1/2/3) von Junta und Franco (21/22) |
| Neutralen-Sperre | `has_idea = mdcw_ni_armed_neutrality` (`common/ideas/mdcw_cold_war_national_ideas.txt:476-528`). Die KI wählt die Idee für SWE/SWI/FIN/AUS (Z. 520-526) | Diese Idee sperrt jeden Blockbeitritt (`mdcw_cold_war_triggers.txt:230-233`); für die EG passt sie als Obergrenze „Stufe 3 Freihandel“ |
| Integrationstiefe | Custom-Modifikatoren `globalism_equilibrium` und `mdcw_cw_market_exposure` | Imperia-Globalism (`common/scripted_effects/mdcw_imperia_globalism_effects.txt:1-37`) wirkt bereits auf Sanktionsresistenz, ROI und Zinsen |
| Embargo-Koordination | `mdcw_cw_on_sanction_imposed` (Blockaufruf-Flags `mdcw_cw_embargo_b<bloc>_t<typ>` + Popup `mdcw_cw.10`) | Lässt sich als EG-Aufruf kopieren (siehe Vorschlag 8) |
| Spannung | `mdcw_cw_add_tension` mit `mdcw_cw_tension_delta` | Einheitlicher Kanal für EVG, Ostpolitik und sowjetischen Vorbehalt |

**Wenn alt-historisch doch ein eigener Block entstehen soll („Dritte Kraft“) [V/Ve]:**
- **[V]** Die Ausrichtung 0–3 ist an vielen Stellen hart kodiert: `mdcw_cw_rebuild_blocs` mit festen `else_if`-Ketten für 0–3, die Sanktionsflags `_b1.._b3_`, der Führer-Trigger und die vier Modifikatoren.
- **[Ve]** Nötig wäre ein Generator-Lauf mit neuen Daten in `tools/mdcw_cold_war_data.py`, nicht Handarbeit.

### 1.4 Konflikte

| Fall | Stand im Code | Konflikt für die EG | Lösungsidee |
|---|---|---|---|
| **FRA** 1966 aus der integrierten NATO-Struktur | [V] Volles Fraktionsmitglied plus `NATO_member` (IMP_1970 Z. 1190, 1210) | Artikel 5 zieht FRA automatisch in Kriege. Das gaullistische Profil fehlt völlig | FRA-Startflag `FRA_1970_outside_integrated_command` [Vorschlag]; EG-Verteidigungsthemen (WEU/EVG) lesen das Flag |
| **Neutrale** AUS/SWI/SWE/FIN (+ IRE) | [V] Ausrichtung 0, die KI nimmt Armed Neutrality | Vollmitgliedschaft bricht 1970 die Neutralität (Staatsvertrag AUS, YYA FIN) | Stufe 3 (Freihandel) als Obergrenze, solange Armed Neutrality aktiv ist; darüber feuert der sowjetische Vorbehalt (Vorschlag 10) |
| **Diktaturen** GRE/SPR/POR, TUR nach 1971/1980 | [V] West, aber nicht „core“ | Sie dürfen nicht über die West-Zugehörigkeit EG-Rechte bekommen | Demokratie-Klausel über `mdcw_cw_party_core_west`, Einfrieren per Hook (Vorschlag 6) |
| **SOV erkennt die EWG nicht an** | [V] In der SOV-1970-Lokalisierung kein EWG-Bezug, kein Flag | Keine Haltung modelliert | SOV-Flag `COLDWAR_SOV_ec_recognised` (Decision/Fokus, historisch 1988), bis dahin keine EG-RGW-Abkommen |
| **EG-Mitglieder ohne Szenario-Wächter** | [V] siehe Risiko R1 | MD-EU 2000 läuft parallel | Szenario-Zweig vor dem EG-Bau |

---

## 2. Abstimmungs- und Zusammenhalts-Engine

### 2.1 Politbüro-Abstimmung SOV 1970 [V]

Datei: `common/scripted_effects/COLDWAR_SOV_1970_scripted_effects.txt`.

| Schritt | Effekt / Event | Zeilen | Wiederverwendung für den EG-Rat |
|---|---|---|---|
| Start | `COLDWAR_SOV_start_vote`. Eingaben als Temp-Variablen: `_vt` Typ, `_vl` Neigung, `_vs` Gegenstand, `_vu` Unionsfrage. Setzt `global.*` und das Global-Flag `COLDWAR_SOV_vote_running`, markiert die Wähler (`COLDWAR_SOV_in_vote`, `_vote_pending`), summiert die Gesamtgewichte und sendet den Stimmzettel | 1084-1105 | Identisch: Wähler = `has_idea = EU_member`, Gewicht pro Land |
| Gewicht | `COLDWAR_SOV_vote_weight`: 1, bei Unionsfrage mit „Federal Union“ 2 | 1107-1113 | Ersetzen durch die Länder-Variable `EC_council_weight` (4/4/4/2/2/1, später 10/10/10/10/5/5/3/3/2) |
| Stimmzettel | Event `COLDWAR_SOV.11`: Enthaltung (KI-Chance 0), Ja (10), Nein (1). `timeout_days = 9` | `events/COLDWAR_SOV_1970_events.txt:233-266` | Optionen Ja / Nein / Enthaltung / **„Vital National Interest“** (Veto-Joker) |
| Stimme | `COLDWAR_SOV_cast_vote`: Ja addiert das Gewicht; Nein und Enthaltung nur als Flag | 1115-1128 | Nein-Gewicht zusätzlich zählen (nötig für die Einstimmigkeit) |
| Auszählung | Event `COLDWAR_SOV.12` (verdeckt, 10 Tage später) → `COLDWAR_SOV_tally_vote` | 268-288 / 1130-1406 | Gleich |
| Mehrheit | Moskauer Block = round(3,5 + 3,5 × BOP × Neigung), geklammert 0–7, +1 Generalsekretär, + Republiken. Bestanden, wenn 2 × Ja > Gesamt. **Nichtantworten werden zu Enthaltung und zählen faktisch als Nein** | 1131-1165 | Qualifizierte Mehrheit: Ja ≥ 12 (von 17). Einstimmigkeit: kein Nein (eine Enthaltung blockiert nach Art. 148 Abs. 3 EWGV nicht) |
| Eingefrorene Kopien | `global.COLDWAR_SOV_last_*`, Flags `_last_yes/_no/_abstain` für das News-Event `COLDWAR_SOV.13` | 1166-1185 | Unverzichtbar, damit eine neue Abstimmung die Anzeige nicht überschreibt |
| Folgen nach Typ | `if`-Kette nach `vote_type`/`vote_subject` | 1186-1402 | Dispatcher nach Gegenstand (Beitritt, Assoziierung, Agrarpreise usw.) |
| Warteschlange | `COLDWAR_SOV_queue_resolution` / `_next_queued_vote` (`global.COLDWAR_SOV_res_queue`, 3 Tage Abstand über Event 55) | 1409-1469 | Ratsagenda mit einer laufenden Abstimmung |
| Antrag aus der Peripherie | `COLDWAR_SOV_propose_to_politburo` (Typ 4, feste 3 Moskauer Stimmen) | 1641-1652 | „Kommissionsvorschlag“ bzw. Mitgliedsantrag |

**Gezielte Decisions [V]:**
- Vorbild ist `COLDWAR_SOV_appoint_seat` mit `targets = { UKR … }` und `target_trigger` (`common/decisions/COLDWAR_SOV_1970_decisions.txt:922-958`).
- Das passt für „Open Accession Negotiations with [Ziel]“ oder „Freeze Association of [Ziel]“.

**Machtbalance-Schatten [V]:**
- Die Balance ist im Spiel nicht lesbar. Deshalb spiegelt `COLDWAR_SOV_bop` jede Änderung mit (`COLDWAR_SOV_1970_decisions.txt:7-37`, Drift `COLDWAR_SOV_monthly_bop_drift` Z. 321ff.).
- Vorlage für eine EG-Balance „Supranational (Monnet) ↔ Intergouvernemental (de Gaulle)“.

### 2.2 OPEC-Abstimmung (Cold War) [V]

Datei: `mdcw_cold_war_effects.txt`. Sie ist neuer als die AS-BUILT-Doku; das Öl-Waffe-Decision gibt es nicht mehr.

| Schritt | Zeilen | Merkmal |
|---|---|---|
| `mdcw_cw_start_opec_vote` | 1781-1803 | `global.mdcw_cw_opec_vote_active` (21 Tage), Cooldown 60 Tage. Stimmzettel **nur an Menschen** (`is_ai = no`) in `mdcw_cw_is_opec_member`. Auszählung über `mdcw_cw.17` im USA-Scope nach 14 Tagen |
| `mdcw_cw_record_opec_vote` | 1806-1819 | Kopfzählung Ja/Nein und Gewichtssumme Ja (Exportanteil) |
| `mdcw_cw_finalize_opec_vote` | 1822-1931 | Bestanden, wenn Ja > Nein (Köpfe). **Die Gewichte bestimmen nur die Stärke der Wirkung.** Danach Snapshot-Flags pro Mitglied und News 18–21 |
| Decisions | `common/decisions/mdcw_cold_war_decisions.txt:303-392` | Drei Vorschlagstypen, je 50–75 PP. Kategorie nur für Menschen (`categories/mdcw_cold_war_decision_categories.txt`) |
| Ballot-Events | `events/mdcw_cold_war_events.txt:175-278` (14/15/16), 280-285 (17) | Text 14.d: „AI delegations abstain“ |

**Unterschied, den das Team entscheiden muss [V]:**

| System | Wer stimmt | Was Nichtantworten bedeuten |
|---|---|---|
| Politbüro | KI-Republiken stimmen per `ai_chance` | zählen gegen den Antrag |
| OPEC | nur Menschen | — |
| Archivierter EG-Plan | nur Menschen („verbindliche MP-Vorgabe nach Nutzererklärung“, `docs/europe_1970_audit/einbauplan_1970.md` Z. 9) | — |

Für die EG muss das festgelegt werden. Ohne KI-Stimmen bräuchte der Rat einen Ersatz für KI-Mitglieder: entweder einen historischen Standard je Land oder „Enthaltung zählt nicht“.

### 2.3 Weitere Abstimmungs- und Ratifikationsmuster [V]

- **NATO-Beitrittsratifikation:** Flag `NATO_Ratified_@ROOT` pro Mitglied. KI-Mitglieder ratifizieren automatisch für 20 PP, Menschen per Decision (`common/scripted_effects/01_NATO_effects.txt:14-60`). Das ist **die** Vorlage für die nationale Ratifikation von Beitrittsverträgen (Unterhaus 1971, Referenden 1972).
- **UN-Generalversammlung:**
  - Warteschlange aus zwei parallelen Arrays (`global.ga_vote_type_tracker` / `_nation_tracker`), bestimmte Typen werden vorgezogen (`01_international_systems_effects.txt:616-665`).
  - Die Zweidrittel-Schwelle wird gerundet berechnet (Z. 1143-1152), der Sicherheitsrat braucht 60 % (Z. 1154-1176).
  - Als Zeitgeber dient eine Mission (`common/decisions/un_voting_decisions.txt:2-75`, `days_mission_timeout = 5`).
- **Missionen:** Konzept Unionsmissionen (Projekt-Doc, noch nicht gebaut). Missionen mit `days_mission_timeout`, Urteils-Event bei Fehlschlag, Schwellen-Belohnung (9 von 14). Das ist als Muster für „GAP-Reform-Frist“ oder „Übergangszeit“ brauchbar.

### 2.4 Unionszusammenhalt als Vorlage für den „Gemeinschaftsgeist“ [V]

| Element | Ort | Übertragung |
|---|---|---|
| Wert 0–100, Start 62 | `COLDWAR_SOV_initialize_1970` Z. 50 | `global.EC_community_spirit`, Start etwa 60 (nach dem Den-Haag-Gipfel optimistisch) |
| Änderungs-Helfer mit Scope-Umleitung zu SOV | `COLDWAR_SOV_change_union_cohesion` Z. 296-306 (Temp `COLDWAR_SOV_cohesion_delta`) | `EC_change_community_spirit` mit Temp `EC_spirit_delta`, global, plus `force_update_dynamic_modifier` bei allen Mitgliedern |
| Monatliche Drift | `COLDWAR_SOV_monthly_cohesion` Z. 309-318 (Stabilität, Krieg, Korruption) | Drift aus Vetos, Boykotten, Wirtschaftsklima (`global.mdcw_cw_market_confidence`) und Agrarüberschuss |
| Stufen-Modifikatoren | `common/dynamic_modifiers/COLDWAR_SOV_1970_dynamic_modifiers.txt:141-181`: Unbreakable > 74, Strained 35–54, Crisis 15–34, Disintegration < 15. **Zwischen 55 und 74 gibt es keinen Modifikator** | Modifikator mit `enable = { has_idea = EU_member check_variable = { global.EC_community_spirit > N } }` [Ve: globale Variable im Enable-Trigger zulässig] |
| Schwellen mit Folgen | as_built SOV: unter 55 „Declare Sovereignty“, unter 35 Referendum, unter 15 Krisen-Event 44 | Unter 20 POD 14 „Zerfall“, über 80 Föderationspfad |
| Kosten von Strafen | Konzept Unionsmissionen §5 und §8: jede Strafe kostet Zusammenhalt | Veto-Joker und Boykott kosten Gemeinschaftsgeist |

---

## 3. Diplomatie, Sanktionen, Einfluss, UN, Geld, Handel – was trägt welche EG-Mechanik?

| Baustein | Ort | Funktionsweise | EG-Einsatz |
|---|---|---|---|
| **Angebots-Dispatcher SOV** | `COLDWAR_SOV_offer_*` (`COLDWAR_SOV_1970_scripted_effects.txt:1656-2024`), Antwort-Events 100–147, Rückmeldung 900/901 | Fokus sendet nur, der Empfänger entscheidet, Effekte erst bei Annahme. **Nur Annehmen/Ablehnen, kein Gegenangebot** (z. B. `events/COLDWAR_SOV_1970_events.txt:2653-2699`) | Ostpolitik-Verträge sind schon da: Moskauer Vertrag 104 (2820-2857), Berlin 105, Paris-Achse 108 (2978-3010), Helsinki 110 (3047-3080, mit Unterschriftenzähler `global.COLDWAR_SOV_helsinki_signatures`), Pipelines 133, CoCom 142 (4170-4201) |
| **Angebots-Muster GRE (vollständig)** | `events/COLDWAR_GRE_1970_tree_events.txt:871ff.` (Event `COLDWAR_GRE_TREE.105`) | `_pending`, `_live` (90 Tage) und `_timed_out`. Optionen: Annehmen, Ablehnen, **neue Bedingungen verlangen**, Vertagen, veralteten Vorschlag schließen. Neu senden per Retry-Decision (`common/decisions/COLDWAR_GRE_1970_tree_decisions.txt:203-220`) | Beste Vorlage für Beitrittskapitel. Achtung: Auf „Gegenangebot“ und „Vertagen“ folgt nichts, siehe R3 |
| **Angebots-Muster CYP (Decision statt Event)** | `common/decisions/COLDWAR_CYP_1970_decisions.txt:498-527` (erneut senden), 2837-2919 (annehmen), 2921-2996 (ablehnen) | Die Antwort liegt als Decision im Menü des Partners. Die Angebots-Instanz-ID verhindert alte Antworten (`COLDWAR_CYP_1970_offer_instance_*`) | Angenehm bei mehreren gleichzeitigen Partnern (sechs Ratsmitglieder) |
| **Diplomatische Aktion mit Annahme** | `mdcw_cw_assistance` (`common/scripted_diplomatic_actions/mdcw_cold_war_diplomatic_actions.txt:7-127`) | `requires_acceptance`, `on_sent_effect` speichert ein offenes Angebot, `ai_acceptance` nach Meinung und Block, `send_scripted_gui` | „Financial Protocol“ für Assoziierte als **Hilfsprogramm** (8 Typen, z. B. „Construction Assistance“, „Consumer Supply Credits“, Lokalisierung `mdcw_cold_war_l_english.yml:79-86`) statt eines neuen Systems |
| **Imperia-Sanktionen** | Arrays `imp_<dip/fin/eco/mil>_sanc_on_us` / `_by_us`. Aktionen in `imp_sanctions_diplomatic_actions.txt` mit Cold-War-Hook | Stärke über den BIP-Anteil des Sanktionierers (`common/scripted_effects/imp_sanctions_effects.txt` ab Z. 13). Mehrere Sanktionierer addieren sich | Kollektives EG-Embargo = jedes Mitglied verhängt; die Stärke ergibt sich von selbst |
| **Sanktions-Helfer ohne Aktion** | `IMP_sanctions_add_*_from_prev` (`common/scripted_effects/IMP_sanctions_support_effects.txt:5-52`, generiert von `tools/build_sanctions_reports.py`) | Schreiben Arrays und Meinung, **ohne** den Cold-War-Hook | EPZ-Beschluss „Common Sanctions“ setzt die Sanktionen für alle Mitglieder; danach `mdcw_cw_add_tension` von Hand aufrufen |
| **Historische Sanktionen 1970** | `IMP_1970_sanctions_effects.txt:3ff.`, darin **CoCom** Z. 888-1146 (Militärsanktionen westlicher Staaten auf SOV/DDR u. a.) | Gerichtet, mit Quellen | Embargo-Koordination und EPZ knüpfen an CoCom an, Ostpolitik und KSZE lockern sie |
| **Blockembargo-Aufruf** | `mdcw_cw_on_sanction_imposed` Z. 4332-4413 (Flags `mdcw_cw_embargo_b<n>_t<typ>` 365 Tage, Popup `mdcw_cw.10` an menschliche Blockmitglieder, `events/mdcw_cold_war_events.txt:118-135`), Folgen +15 Meinung des Führers (Z. 4414-4502) | Der Führer ruft auf, Mitglieder folgen freiwillig | „EC Common Commercial Measure“: der Ratsvorsitz bzw. Ratsbeschluss ruft auf, Folgen geben Gemeinschaftsgeist statt Führer-Meinung |
| **Öl-Embargo bilateral** | `mdcw_cw_oil_embargo_impose/lift`, Ausnahmen (`mdcw_cold_war_diplomatic_actions.txt:176-277`), Druck `mdcw_cw_recalculate_oil_embargo_pressure` (effects 1552-1578) | Nur Spieler | EG-Solidaritätstest 1973 (NL-Embargo): die EG verteilt Öl → Ausnahme-Arrays (`mdcw_cw_oil_exempt_targets`) als Hebel [Ve] |
| **Einfluss MD** | `change_influence_percentage` (Temp `percent_change`, `tag_index`, `influence_target`; `common/scripted_effects/00_influence_scripted_effects.txt:1055ff.`), `mp_economic_aid_transfer` (374-396) | Einflussanteile pro Land | Sowjetischer Vorbehalt (FIN/AUS) und deutsch-französischer Einfluss bei Assoziierten. **1970 sind die Einfluss-Arrays leer**, siehe R12 |
| **Geld: BIP-Anteil-Helfer** | `COLDWAR_SOV_pay_gdp_share`, `_receive_gdp_share`, `_transfer_gdp_share` (an `var:COLDWAR_SOV_transfer_target`), `_change_debt_gdp_share` (`COLDWAR_SOV_1970_scripted_effects.txt:82-140`) | Einmalige Transfers in Prozent des BIP | GAP-Jahresabrechnung (Nettozahler → Empfänger), EIB-Kredite (Schulden), Rabatt-Erstattung |
| **Geld: laufende Subventionen** | `imp_subsidies` (`active_subsidies@ZIEL`, `calculate_subsidies_in/out` in `common/scripted_effects/imp_money_transfer_scripted_effects.txt:5-17`), gebucht in `00_money_system.txt:812` (Einnahmen) und `:3620` (Ausgaben) | Laufender bilateraler Transfer über das Geldsystem | Finanzprotokolle (GRE 1962, TUR 1964/1973), ohne neues Geldsystem |
| **Geld: Kredit** | `mdcw_cw_take_loan` (2 % BIP, 0,5–25 Mrd., gleich hohe Schulden; effects 4614-4622) | Kasse + Schulden | EIB-Darlehen an Assoziierte |
| **Geld: MD-EU-Beitrag** | `EU_budget_contribution_weekly` bei `has_idea = EU_member` (`00_money_system.txt:4012-4015`) | MD-nativ, wöchentlich | Basis für Beiträge bis 1970; die Eigenmittel ab 1971 als Umstellung der Berechnung |
| **Basis-Helfer** | `modify_treasury_effect` / `modify_debt_effect` (`common/scripted_effects/00_budget_effects.txt:1487-1505`) | `treasury_change`/`debt_change` | Alle Buchungen |
| **Handelsabkommen** | `set_improved_trade_agreement` (Temp `sender_nation`/`receiver_nation`, optional `remove_agreement = 1`; `common/scripted_effects/00_economic_effects.txt:89-150`) | Gegenseitige Meinung, Flag `trade_agreement@PARTNER`, Zähler `signed_trade_agreements` | Stufe 1/2 (Handels- und Präferenzabkommen YUG, SPR, ISR) zwischen dem Antragsteller und **jedem** EG-Mitglied. Innerdeutscher Handel GER–DDR |
| **Organisations-Kooperation** | Commonwealth: Global-Flags `COMMONWEALTH_*_adopted`, Mitglieds- und Teilnehmer-Effekte, gemeinsamer Variablen-Modifikator (`common/scripted_effects/99_Commonwealth_scripted_effects.txt:1-30, 102-141`; `common/dynamic_modifiers/02_commonwealth_dynamic_modifiers.txt`) | Rahmen, die die Organisation beschlossen hat, schalten Mitglieds-Decisions frei | **EFTA-Gegenblock** und EG-Politikrahmen (Zollunion, GAP, EPZ) im selben Muster |
| **Globalism** | `globalism_equilibrium` → `imp_eco_globalism_tick` (wöchentlich, `common/on_actions/zzzzzz_mdcw_imperia_globalism_on_actions.txt`) | Wirkt auf Kriegsunterstützung, Sanktionen, ROI, Zinsen | Zollunion +10 bis +15, EFTA +5, Assoziierung +3 (Vorschlag) |

---

## 4. Länderinhalte 1970 mit EG-Bezug

### GRE (eigener Baum `COLDWAR_GRE_1970_focus`) [V]

- **Regime:**
  - Junta = `ruling_party = 22`, Leader-Auswahl über `COLDWAR_GRE_1970_political_dossier` (`common/decisions/COLDWAR_GRE_1970_regional_decisions.txt`).
  - Übergangsflags: `COLDWAR_GRE_1970_free_election_implemented`, `_civilian_transfer_implemented`, `_civilian_government_active`, `_civilian_constitution_ratified`, `_current_electoral_mandate_verified`, `_negotiated_transfer_agreed`, `_royal_executive_settlement_implemented`.
- **Europa-Fokusse:**

| Fokus | Stelle | Was der Code tut |
|---|---|---|
| `COLDWAR_GRE_1970_nd_13` „Reactivate the Association Framework“ | `common/national_focus/COLDWAR_GRE_1970_focus.txt:2995-3030` | Gewährt einseitig die Idee `COLDWAR_GRE_1970_nd_13_programme` (`common/scripted_effects/COLDWAR_GRE_1970_tree_effects.txt:6956-7011`), obwohl der Text eine Gegenpartei-Zustimmung verlangt (Lokalisierung `COLDWAR_GRE_1970_tree_l_english.yml:129`) |
| `nd_15` „An Accession Dossier“ | — | Sendet an **ENG** (`COLDWAR_GRE_1970_send_nd_15` Z. 17295ff., Event 105, Annahmeflag `nd_15_accepted_ENG` Z. 7086) |
| `pap_13` „Selective European Opening“, `centre_13` „Open the European Channel“, `royal_13` „A Parliamentary European Course“, `pasok_13` | — | Gewähren **einseitig**, trotz Texten wie „European institutions … must accept terms“ |
| `nd_19` „A European Parliamentary Republic“ | — | 0,8 % BIP Kosten, ebenfalls einseitig |

- **Hooks:**
  - `on_ruling_party_change` und wöchentlicher Tick (`common/on_actions/COLDWAR_GRE_1970_tree_on_actions.txt`).
  - Finanzierungs-Gate `_awaiting_funding` / `_granted` mit Retry-Decision.
  - Ägäis-Flag `COLDWAR_GRE_1970_aegean_dispute_active` (GRE-TUR-Konflikt, relevant für die Einstimmigkeit nach einem Beitritt).

### TUR [V]

- Kein eigener 1970-Baum: TUR nutzt `mdcw_1970_generic_focus` (`common/scripted_effects/mdcw_1970_focus_tree_effects.txt`, keine Ausnahme für TUR).
- 1970 gibt es nur Leader-Roster und Dossier (`COLDWAR_TUR_1970_political_dossier`), dazu `on_daily` (`common/on_actions/COLDWAR_TUR_1970_regional_on_actions.txt`).
- **Kein** Ankara- und kein Zusatzprotokoll-Inhalt, keine Flags.
- Die Datumsfenster `date < 1980.4.7` und `> 1980.9.19` im Roster deuten den Putsch von 1980 an (`COLDWAR_TUR_1970_regional_effects.txt:148, 219`), das Memorandum 1971 nicht.
- `turkey.txt` / `turkey_1985.txt` sind 2000/1985-Inhalte.

### CYP [V]

- Fokus „Seek Western Economic Association“: 0,5 % BIP, Angebot an **ENG** (`COLDWAR_CYP_1970_send_western_association`, `common/scripted_effects/COLDWAR_CYP_1970_effects.txt:4047-4056`). Bei Annahme Idee `COLDWAR_CYP_1970_western_association_idea` (4037-4045).
- Text: „Trade talks in a pre-EU era“ (`COLDWAR_CYP_1970_l_english.yml:996-998`). Historisch: Assoziierung mit der EG am 19.12.1972.
- Kanal `ankara_channel` an TUR.

### SPR (eigener Baum `spain_1970`) [V]

- **Fokusse:**
  - `SPR_1970_apply_to_the_european_communities` (`common/national_focus/spain_1970.txt:1240-1264`): Flag `SPR_1970_european_communities_application`. Event `SPR_1970.145` gibt FRA und GER *beidseitig* „declaration_of_friendship“ (`events/SPR_1970_events.txt:880-897`).
  - `SPR_1970_a_mediterranean_common_market` (1883-1913): Event 219 mit Idee und Meinung zu POR/FRA/ITA.
  - `SPR_1970_accession_to_the_european_communities` (2113-2144) → `SPR_1970.227`: **`add_ideas = EU_member` ohne Zustimmung der Mitglieder** (`events/SPR_1970_events.txt:1672-1684`), dazu `europeanism_change`.
- **Flags:** `SPR_1970_franco_dead`, `_carrero_is_prime_minister`, `_managed_opening_adopted`, `_democracy_consolidated`, `_european_communities_member`, `_left_nato_after_referendum` (Event 229).
- **Präferenzabkommen 29.6.1970:** kein Event, kein Flag.

### USA (Nixon) [V]

| Fokus | Stelle | Flag | Bemerkung |
|---|---|---|---|
| `USA_1970_NIX_E7` „Close the Gold Window“ | `common/national_focus/USA_1970.txt:582-612` | `USA_1970_gold_window_closed` | — |
| `USA_1970_NIX_E8` „Defend Bretton Woods“ | 615-645 | `USA_1970_bretton_woods_defended` | — |
| `USA_1970_NIX_F3` „Reassure the Alliances“ | 1263-1291 | `USA_1970_nixon_alliance_offer` | Das Flag wird **nirgends gelesen** (ein toter Anknüpfungspunkt) |

- Nixon-Angebote (`common/scripted_effects/USA_1970_nixon_diplomacy_effects.txt`) gehen an CHI/SOV/JAP/SVN, nicht an Europa.
- Burden-Sharing-Decisions sind rein US-intern.

### SOV [V]

- Keine EWG-Haltung, kein Anerkennungsflag (Lokalisierung durchsucht).
- Europa-relevante Angebote: `offer_moscow_treaty` (GER), `berlin_agreement` (USA/ENG/FRA), `paris_axis` (FRA), `pipelines_to_europe` (GER/ITA/FRA), `gas_for_pipes` (GER, mit `set_improved_trade_agreement`), `helsinki`, `cocom`, `social_democratic_partners` (GER/SWE), `royal_houses` (ENG/SPR) (`COLDWAR_SOV_1970_scripted_effects.txt:1677-1950`).
- RGW-Inhalte: „Comprehensive Programme“, „World Market Prices“, „Soyuz Pipeline“, „Romania's Maverick Course“ (Lokalisierung Z. 1774-1794).
- Cold-War-Decision „Comecon Integration Programme“ mit SOV-Erstattung (`COLDWAR_SOV_monthly_comecon_refund`, Z. 126-136).

### GER und DDR [V]

- Beide nutzen den generischen 1970-Baum. `ddr.txt`/`GER_1985.txt` sind 1985-Inhalte.
- Generischer Fokus `GEN_1970_sd_ostpolitik` (`common/national_focus/mdcw_1970_generic_focus.txt:1625-1655`): Spannung −1 über `GEN_1970_change_tension`, +50 PP, Meinung kommunistischer Nachbarn.
- **Kein** innerdeutscher Handel (Suche in GER-/DDR-Effekten und On-Actions erfolglos).

### ENG und IRE [V]

- 1970 generischer Baum; Inhalte zu Europa nur 1985: `uk_1985.txt:177-195` (`ENG_the_european_argument`, Variable `ENG_europe_argument`, Meinung `ENG_1985_european_goodwill` bei FRA).
- Die Decision-Kategorie `ENG_union_question_category` ist sauber durch `ENG_1985_systems_active` geschützt (`common/decisions/categories/mdcw_historical_ENG_IRQ_categories.txt:1-11`).
- EFTA ist nirgends modelliert.

### Neutrale [V]

- AUS/SWI/SWE/FIN haben Ausrichtung 0, die KI nimmt `mdcw_ni_armed_neutrality`.
- Ihre EU-Mitgliedschaft und Einfluss-Arrays stehen nur in den `2000.1.1`-Blöcken der History (z. B. `history/countries/FIN - Finland.txt:532-541`).

---

## 5. Konkrete Realisierungsvorschläge

**1. EG-Ministerrat mit gewichteten Stimmen und Veto-Joker.**
- **Engine:** Die Politbüro-Engine wird als `COLDWAR_EC_start_vote` / `_cast_vote` / `_tally_vote` kopiert, mit Gegenstand, Rechtsgrundlage (QMV oder einstimmig) und eingefrorenen `last_*`-Kopien. Das Gewicht kommt aus der Länder-Variable `COLDWAR_EC_council_weight` (FRA/GER/ITA 4, BEL/HOL 2, LUX 1). Ja- und Nein-Gewichte werden getrennt summiert.
- **Regeln:** QMV besteht bei Ja ≥ 12 (später 41 von 58). Einstimmigkeit besteht ohne jedes Nein, Enthaltungen blockieren nicht.
- **Veto-Joker:** Er ist eine vierte Option im Stimmzettel „Invoke a Vital National Interest“. Sie setzt `global.COLDWAR_EC_vote_unanimity_required` und kostet PP, Gemeinschaftsgeist sowie Meinung bei BEL/HOL/ITA, beim zweiten Mal im Jahr doppelt.
- **Takt:** Stimmzettel mit Timeout wie `COLDWAR_SOV.11`, Auszählung 10 Tage später, Warteschlange wie `global.COLDWAR_SOV_res_queue`. Die Rolle von KI-Mitgliedern ist vorher festzulegen (siehe 2.2).

**2. „Gemeinschaftsgeist“ (Community Spirit).**
- **Wert und Kanal:** Eine globale Variable `global.COLDWAR_EC_community_spirit` (0–100). Jede Änderung läuft über einen Helfer nach dem Muster von `COLDWAR_SOV_change_union_cohesion`, mit Klammer und `force_update_dynamic_modifier` bei allen `EU_member`.
- **Stufen:** Vier Modifikatoren wie `COLDWAR_SOV_cohesion_*`, aber ohne Lücke zwischen 55 und 74.
- **Was den Wert bewegt:**
  - sinkt durch Vetos, Boykott, gescheiterte Abstimmungen und nicht befolgte Embargo-Aufrufe;
  - steigt durch erfolgreiche Gipfel, einstimmige EPZ-Erklärungen und Solidarität bei Embargos.
- **Schwellen:** Unter 20 öffnet sich das Zerfalls-Event (POD 14). Über 80 sind Föderationsschritte verfügbar.

**3. Beitrittsverhandlungen in Kapiteln zwischen Spielern.**
- **Start:** Eine gezielte Decision `COLDWAR_EC_open_negotiations` (Muster `COLDWAR_SOV_appoint_seat`, `targets = { ENG IRE DEN NRY }`) braucht einen einstimmigen Ratsbeschluss. Für 1970 Achtung: Norwegen heißt im Mod **NRY**.
- **Kapitel:** Jedes Kapitel (Übergangszeit, GAP, Commonwealth-Handel, Fischerei, Haushalt, Sterling, Institutionen) ist ein Angebots-Event nach dem GRE-Muster `COLDWAR_GRE_TREE.105`. Das Event hat die Zustände `_pending`, `_live` (90 Tage) und `_timed_out` und die Optionen Annehmen, Ablehnen, neue Bedingungen verlangen (mit echtem Folge-Event), Vertagen.
- **Veto pro Kapitel:** Jedes Mitglied hat eines, gespeichert als `COLDWAR_EC_chapter<n>_vetoed@KANDIDAT`.
- **Abschluss:** Die Ratifikation läuft wie `NATO_auto_ratify_accession`, mit dem Flag `COLDWAR_EC_ratified_@KANDIDAT` je Mitglied (Menschen per Decision).

**4. Referenden aus Parteistärken.**
- **Formel:** P(Ja) = Basis + Σ (Stimmenanteil `party_pop_array^i` × Parteihaltung). Die Parteihaltung steht als Tabelle in einer Länder-Variable, analog zu `ENG_europe_argument` (`uk_1985.txt:187`).
- **Einflussgrößen:** Kapitel-Ergebnisse verschieben die Basis, z. B. eine harte Fischerei-Lösung −6 Punkte bei NRY. Die Kampagne der Regierung kostet PP. Koppelt sie die Vertrauensfrage daran (+2 Punkte), stürzt sie bei einem Nein (`change_ruling_party_effect`).
- **Auslosung:** Das Ergebnis wird einmal mit `random_list` gezogen und als `last_*`-Kopie für die News gespeichert.
- **Kalibrierung:** an den historischen Werten von 1972 (NOR 46,5 % Ja, DEN 63,3 %, IRE 83,1 %).

**5. GAP-Haushalt mit Nettopositionen.**
- **Laufende Beiträge:** Sie bleiben im MD-nativen Kanal `EU_budget_contribution_weekly` (`00_money_system.txt:4012-4015`). Bis 1970 nach Schlüssel, ab 1971 nach Eigenmitteln (Importvolumen bzw. BIP-Anteil).
- **Jahresabrechnung:** Ein Event am 1. Januar berechnet pro Mitglied die Nettoposition (Beitrag minus GAP-Rückfluss aus der Agrarpreisrunde). Gebucht wird mit `COLDWAR_SOV_transfer_gdp_share`-artigen Helfern (`treasury_change` beim Zahler, Gutschrift beim Empfänger).
- **Rabatt-Decision:** Sie ist eine Einstimmigkeits-Abstimmung und bucht eine Rückerstattung über denselben Helfer.
- **Politische Folgen:** Nettozahler bekommen Euroskepsis+ (MD `europeanism_change` mit Minuswert, wie in `SPR_1970.227`), Nettoempfänger Euroskepsis−.

**6. Assoziierungsleiter mit Demokratie-Klausel.**
- **Stufen:** Länder-Variable `COLDWAR_EC_level` 0–9 (Stufen aus dem Bericht §6.1). Die Wirkung kommt aus einem Teilnehmer-Modifikator im Commonwealth-Muster (`COMMONWEALTH_cooperation_modifier`): Handelsmeinung, `globalism_equilibrium`, Exportbonus, bei Assoziierung ein Finanzprotokoll als `imp_subsidies`.
- **Bedingung:** Stufe 5 und höher verlangt `mdcw_cw_party_core_west = yes`.
- **Einfrieren:**
  - Auslöser: Hooks in `on_ruling_party_change`, `on_coup_succeeded` (dort gibt es schon `mdcw_cw_on_coup`) und monatlich. Ein Wechsel zu Partei 0/21/22 setzt `COLDWAR_EC_frozen`; die Stufe bleibt, die Boni entfallen, die Subvention wird gestoppt.
  - Die Mitglieder bekommen ein Event „Freeze or Continue“. „Continue“ kostet Gemeinschaftsgeist und Meinung bei Benelux und ITA.
- **Auftauen bei GRE:** Auslöser sind `COLDWAR_GRE_1970_civilian_transfer_implemented` oder `_civilian_constitution_ratified`. Danach ein Fast-Track-Event, und `nd_13` wird auf diesen Ratsbeschluss umgehängt.

**7. EPZ-Erklärungen als einstimmige Decisions.**
- **Ablauf:** Jedes Mitglied kann „Propose a Common Declaration“ nehmen (Muster OPEC-Decisions, `mdcw_cold_war_decisions.txt:303-392`, eigene Kategorie, nur Menschen). Das Thema ist ein laufender Krieg oder eine Konferenz, gespeichert als Ziel-ID. Der Stimmzettel geht an alle Mitglieder; die EPZ verlangt Einstimmigkeit und kostet kein Veto-Kapital, weil sie außerhalb der Verträge liegt.
- **Erfolg:** Opinion bzw. `change_influence_percentage` beim Adressaten, Zähler `global.COLDWAR_EC_epc_declarations`, Gemeinschaftsgeist +2. Optional eine kollektive Sanktion über `IMP_sanctions_add_*_from_prev` für jedes Mitglied, danach `mdcw_cw_add_tension` von Hand.
- **Misserfolg:** Gemeinschaftsgeist −1.
- **Wirkung auf POD 8:** Der Zähler dient als Voraussetzung für „Dritte Kraft“.

**8. Embargo-Koordination (EG-Handelsmaßnahmen).**
- **Hook:** Eine Kopie des Blockaufrufs aus `mdcw_cw_on_sanction_imposed` (Z. 4332-4413) als eigener Hook `COLDWAR_EC_on_sanction_imposed`. Er wird in die Imperia-Aktionen eingehängt, hinter den Cold-War-Hook (markiert mit `COLDWAR`).
- **Aufruf:** Sanktioniert der Ratsvorsitz (rotierende Variable `global.COLDWAR_EC_presidency`) ein Nichtmitglied, ruft das die Gemeinschaft auf: Flags `COLDWAR_EC_call_t<typ>` am Ziel für 365 Tage und ein Popup wie `mdcw_cw.10` an menschliche Mitglieder.
- **Folgen:** Wer folgt, bringt Gemeinschaftsgeist +0,5. Wer bis zum Ablauf nicht folgt, kostet −0,5.
- **Stärke:** Die Imperia-Stärke summiert sich aus den BIP-Anteilen (`imp_sanctions_strength_calculate`); ein gemeinsames Embargo der Sechs wirkt also automatisch stärker.
- **CoCom:** Die historischen CoCom-Paare (IMP_1970 Z. 888ff.) bleiben nationale Sanktionen. Die EG kann sie nur gemeinsam lockern („Ostpolitik-Handel“).

**9. EFTA als Gegenblock.**
- **Muster:** Commonwealth-Kooperation: Global-Flags für beschlossene Rahmen (Industriefreihandel 1960, Island-Beitritt 1.3.1970), ein Mitglieds-Modifikator mit Variablen, Mitglieds-Decisions mit `days_re_enable`.
- **Mitglieder:** Idee `COLDWAR_EFTA_member` für ENG, DEN, NRY, SWE, AUS, SWI, POR, ICE; FIN über eine FINEFTA-Teilnehmerrolle.
- **Führung:** zuerst ENG. Beim EG-Beitritt automatischer EFTA-Austritt, danach geht die Führung an das stärkste Mitglied (Power-Rank `mdcw_cw_bloc_value`).
- **Brücke:** Decision „EC–EFTA Free Trade Agreement“ (Stufe 3 für alle Rest-EFTA-Staaten), einstimmiger EG-Ratsbeschluss plus Annahme je EFTA-Land (CYP-Decision-Muster mit Angebots-Instanz-ID).
- **Wirkung:** `globalism_equilibrium` +5 statt +10 bis +15 bei der Zollunion.

**10. Sowjetischer Vorbehalt bei den Neutralen.**
- **Auslöser:** AUS oder FIN heben `COLDWAR_EC_level` über 3, oder ein Land mit `mdcw_ni_armed_neutrality` beantragt die Mitgliedschaft.
- **Event an SOV** (Angebots-Muster, der SOV-Spieler entscheidet):
  - Protestnote: Meinung −, `mdcw_cw_add_tension` +1;
  - Handelsdruck: Imperia-Wirtschaftssanktion `imp_eco_sanc`, der Cold-War-Hook läuft mit;
  - bei FIN „YYA-Konsultation“: ein Angebot an FIN mit Annehmen (Einfluss von SOV +, Stufe gedeckelt), Gegenangebot (Ausgleichsabkommen FIN–RGW wie 1973, Handelsabkommen mit SOV) oder Ablehnen (Spannung +2, `change_influence_percentage` für SOV −);
  - Hinnehmen.
- **Ohne Spieler:** Ohne Antwort gilt die Protestnote. Das ist keine KI-Automatik über die Spieler hinweg, denn es ändert nur die Meinung.

**11. Ostpolitik-Verträge als Spieler-Events mit EG-Rückbindung.**
- **Bestand:** SOV schickt den Moskauer Vertrag (104), das Berlin-Abkommen (105), Helsinki (110) und Pipelines (133) bereits als Angebote. Ergänzt werden ein Gegenangebot und `COLDWAR_*`-Flags am Empfänger (z. B. `GER_moscow_treaty_signed`).
- **EG-Seite:**
  - Nimmt GER an, erhalten FRA, ITA und Benelux ein Konsultations-Event „Westbindung“. FRA kann eine Gegenleistung verlangen, z. B. die Zustimmung zur GAP-Finanzierung, als Angebot an GER, oder „Sonderweg“-Misstrauen setzen (Gemeinschaftsgeist −2).
  - Den Grundlagenvertrag GER–DDR knüpft das Team an das Handelsabkommen `set_improved_trade_agreement` GER–DDR plus ein EG-Protokoll „Innerdeutscher Handel“ (DDR-Waren zollfrei nach GER; keine EG-Sperre ohne GER).
- **Kanal:** `GEN_1970_sd_ostpolitik` bleibt der nationale Einstieg. Die Spannung sollte aber über `mdcw_cw_add_tension` laufen (siehe R10).

**12. Atlantische Beziehungen und Währungsstufen.**
- **Auslöser `USA_1970_gold_window_closed`:** Event an alle EG-Mitglieder „The Dollar Crisis Reaches Europe“ mit der Wahl W1 (Werner-Koordination), sofortige Schlange (W2) oder nationale Floats. Ratsbeschluss mit QMV.
- **Auslöser `USA_1970_bretton_woods_defended`:** Die Schlange verzögert sich, die Stabilität der Mitglieder steigt.
- **Totes Flag `USA_1970_nixon_alliance_offer`:** Es kann ein Angebot „Atlantic Partnership / Year of Europe“ an den Ratsvorsitz auslösen (Annehmen, Gegenangebot zum Burden-Sharing, Ablehnen).
- **US-Seite:** Annahme gibt den US-Departments-Modifikatoren `temp_change`-Werte (Exportrendite), Ablehnung öffnet den Gaullismus-Pfad.

**13. Spanien: Präferenzabkommen 1970 und Franco-Nachfolge.**
- **Start:** Das Präferenzabkommen gilt ab 1970 als Stufe 2: 1.10.1970, `set_improved_trade_agreement` SPR mit den Sechs, Flag `SPR_1970_ec_preferential_agreement`.
- **Fokus umbauen:** `SPR_1970_accession_to_the_european_communities` gibt nicht mehr `EU_member`. Der Fokus setzt den Antrag `COLDWAR_EC_application`, der Rat entscheidet über Beitrittskapitel (Vorschlag 3).
- **Bedingungen:** Voraussetzung bleibt `SPR_1970_democracy_consolidated` plus `mdcw_cw_party_core_west`.
- **Opinion-Effekte:** Die beidseitigen Effekte in `SPR_1970.145/219` werden zu Angeboten an FRA, GER und ITA.

**14. Türkei: Zusatzprotokoll November 1970 und Putschvorbehalt.**
- **Start:** TUR beginnt auf Stufe 5 (Assoziierung mit Beitrittsperspektive, Flag `TUR_ankara_agreement`).
- **Decision „Sign the Additional Protocol“** (TUR, ab 1970, 50 PP): Ratsbeschluss einstimmig. Danach folgt ein Interimshandelsabkommen (`set_improved_trade_agreement` mit jedem Mitglied) sowie ein Finanzprotokoll als `imp_subsidies` von GER/FRA.
- **Putsch:** Das Memorandum vom 12.3.1971 bzw. der Putsch von 1980 wirken über den Einfrier-Hook (Vorschlag 6).
- **Griechenland:** Ist GRE Mitglied, setzt die Ägäis- bzw. Zypern-Lage (`COLDWAR_GRE_1970_aegean_dispute_active`) einen GRE-Veto-Bonus auf TUR-Abstimmungen.

**15. Zypern und Malta.**
- **CYP:** Die „Western Association“ geht nicht mehr an ENG, sondern an den Rat. Solange ENG nicht Mitglied ist, kann ENG als Fürsprecher ein Kapitel-Bonus-Event erhalten. Der Ablauf (0,5 % BIP, Angebots-Instanz) bleibt.
- **MLT (generischer Baum):** Eine Decision „Association Agreement“ (5.12.1970) ist ein einstimmiger Beschluss. Gewinnt Labour/Mintoff (MLT-Wahl 1971, Parteiwechsel), öffnet ein Event „Neutralist Turn“ mit Wechsel zu Ausrichtung 0 und Wirkung auf die NATO-Basen. Der Wechsel erfolgt nur durch eigene Entscheidung von MLT.

**16. Alt-historisch: Europäische Verteidigungsgemeinschaft und WEU-Revival.**
- **Decision „Reactivate the WEU“:** einstimmig, die Sechs plus ENG. Voraussetzungen: Gemeinschaftsgeist ≥ 70, FRA-Zustimmung, ein Auslöser wie eine Mansfield-ähnliche US-Truppenreduktion (ein neues USA-Flag) oder Spannung ≥ 60.
- **Wirkung:**
  - eigenes Fraktionsziel bzw. Tech-Sharing (Muster `NATO_join`, `add_to_tech_sharing_group`),
  - Spannung +3 bis +5 über `mdcw_cw_add_tension`,
  - SOV-Event „The Bonn–Paris Axis Rearms“,
  - Atomwaffensperrvertrag 1970 als harte Sperre für eine deutsche Kontrolle.
- **MP-Regel:** **keine** automatische Kriegsbeteiligung. Die MD-Artikel-5-Logik (R6) darf nicht kopiert werden; Beistand nur als Angebots-Event.

**17. Alt-historisch: „Dritte Kraft“.**
- **Bevorzugt ohne neuen Block:** Ein EG-Flag `COLDWAR_EC_third_force` (Ratsbeschluss einstimmig). Voraussetzungen: ≥ 3 EPZ-Erklärungen, Gemeinschaftsgeist ≥ 75, Spannung ≤ 40.
- **Eigener Modifikator für die Mitglieder:** Einflussabwehr +, `mdcw_cw_market_exposure` −, Handelsmeinung zu blockfreien Staaten +, Meinung von USA und SOV −.
- **Option für das Team:** Ein echter vierter Block (Ausrichtung 4) nur über `tools/generate_mdcw_cold_war.py` (Daten, Führer-Trigger, Arrays, Modifikator, Fenster). Er wäre ein eigenes Projekt.

**18. Alt-historisch: gaullistisches Veto und Politik des leeren Stuhls.**
- **Balance:** Eine EG-BOP „Supranational ↔ Intergovernmental“ mit Schattenvariable (`COLDWAR_SOV_bop`-Muster).
- **Decision „Boycott the Council“** für jedes Mitglied: Global-Flag `COLDWAR_EC_empty_chair`, Ratsabstimmungen pausieren (Warteschlange hält an), Gemeinschaftsgeist −1 pro Monat.
- **Antwort der anderen:** Event mit Nachgeben (BOP Richtung intergouvernemental, Bonus für den Boykotteur), Kompromiss (Veto-Joker gestärkt) oder Ultimatum. Nach 6 Monaten ohne Einigung folgt POD 14.
- **„Drittes Veto“ gegen ENG:** Es ist einfach das Nein von FRA im Beitrittskapitel.

**19. Alt-historisch: Zerfall der EG.**
- **Auslöser:** Gemeinschaftsgeist < 20 löst das Event „The Communities in Crisis“ aus (Muster: SOV-Krisen-Event 44 unter 15 Zusammenhalt).
- **Optionen für jedes Mitglied** (Angebots-Muster):
  - Bleiben;
  - Austritt mit Freihandelsstufe (`remove_ideas = EU_member`, `on_remove` → `leaving_EU`; Achtung: MD-Aufräumlogik prüfen);
  - Kerneuropa (Benelux + GER + FRA).
- **Kosten:** Auf Seiten von FRA und ENG gehen die Kosten über `europeanism_change`, Euroskepsis steigt.
- **Schutz:** Kein erzwungener Austritt eines Spielers.

**20. Innerdeutscher Handel und RGW-Anerkennung.**
- **Start:** `set_improved_trade_agreement` GER–DDR mit Flag `COLDWAR_EC_inner_german_trade`. EG-Handelssperren gegen die DDR brauchen das Ja von GER (Ratsregel).
- **SOV-Decision „Recognise the EEC“** (historisch 1988): Sie gibt RGW-Staaten die Möglichkeit, Stufe 1 bzw. 2 zu beantragen. Vorher kann ROM (`COLDWAR_SOV_romanias_maverick_course` als Auslöser) ein bilaterales Handelsabkommen versuchen; SOV bekommt dann ein Angebots-Event (Hinnehmen oder Druck über die Imperia-Sanktion).

---

## 6. Auffälligkeiten und Risiken

| Nr. | Befund | Ort | Status |
|---|---|---|---|
| R1 | **Der MD-EU-Start hat keinen 1970-Wächter.** `on_startup_euu_action` wird aus `00_on_actions.txt:1953-1957` (im ABK-Scope) aufgerufen. Er schreibt AUS, BEL, DEN, ENG, FIN, FRA, GER, GRE, HOL, IRE, ITA, LUX, POR, SPR und SWE in `global.EU_member` und gibt ihnen `foreign_data_kraken` und `asylum_shopping`. Die Idee `EU_member` haben sie 1970 **nicht**, denn sie steht nur in den `2000.1.1`-Blöcken der History. `EU_resync_member_array` (MD_on_actions 609-612) entfernt später Array-Einträge ohne Idee | `common/scripted_effects/99_eu_scripted_effects.txt:760-783` | [V] Hinzufügen; [Ve] die Ideen bleiben bestehen |
| R2 | **SPR tritt einseitig bei** (`add_ideas = EU_member` in `SPR_1970.227`). `EU_member.on_add` ruft `EU_adopt_passed_laws` auf und damit die modernen Gesetzesfolgen. Das verstößt gegen die MP-Regel, weil die Mitglieder nicht zustimmen | `events/SPR_1970_events.txt:1676`; `common/ideas/Organizations.txt:7-14` | [V] |
| R3 | **GRE-Europafokusse:** Text und Code widersprechen sich (`nd_13`, `pap_13`, `centre_13`, `royal_13` einseitig). Der einzige echte Partner bei `nd_15` ist ENG (historisch die Sechs). Die Flags `nd_15_negotiating_ENG` und `nd_15_deferred_ENG` werden gesetzt, aber nie gelesen | `COLDWAR_GRE_1970_tree_effects.txt:6956-7091, 17295ff.`; `events/COLDWAR_GRE_1970_tree_events.txt:928-962` | [V] |
| R4 | **Die CYP-Assoziierung geht an ENG statt an die EG** | `COLDWAR_CYP_1970_effects.txt:4047-4056` | [V] |
| R5 | **Die SOV-Angebote 100–147 haben kein Gegenangebot** (nur a/b), entgegen der Team-MP-Regel. Die KI-Annahme steigt bei hoher Spannung (Faktor 1,5 bei > 60) | z. B. `events/COLDWAR_SOV_1970_events.txt:2653-2699, 2978-3010` | [V] |
| R6 | **Der NATO-Artikel 5 zieht alle Mitglieder automatisch in Kriege**, auch Spieler und FRA (1966). Das widerspricht der MP-Regel „kein Zwang zu Krieg“ | `common/on_actions/MD_NATO_on_actions.txt:12-50`; `IMP_1970_world_politics_effects.txt:1187-1224` | [V] |
| R7 | **Cold-War-Dateien sind generiert** („do not edit by hand“), die Blockführer sind fest verdrahtet, die Ausrichtung 0–3 hart kodiert. EG-Hooks gehören in eigene Dateien; Änderungen am Westblock laufen nur über den Generator | `mdcw_cold_war_triggers.txt:1-17` u. a. | [V] |
| R8 | **Die AS-BUILT-Doku (v3.3.2) ist veraltet:** Die Decision „Use the Oil Weapon“ gibt es nicht mehr, stattdessen OPEC-Abstimmungen und bilaterale Embargo-Aktionen | `mdcw_cold_war_decisions.txt:303-422`; `mdcw_cold_war_diplomatic_actions.txt:176-277` | [V] |
| R9 | **Uneinheitliche Abstimmungskonventionen:** Politbüro mit KI-Stimmen und Nichtantwort = Nein, OPEC nur Menschen mit Kopfmehrheit, der archivierte EG-Plan nur Menschen. Das Team muss das für den EG-Rat festlegen | siehe 2.1/2.2 | [V] |
| R10 | **`GEN_1970_change_tension` umgeht `mdcw_cw_add_tension`:** keine Neuberechnung von Stufe, Balken und GUI | `common/scripted_effects/mdcw_1970_generic_focus_effects.txt:39-51` | [V] |
| R11 | **Array-Name des Warschauer Pakts uneinheitlich** (`Warsaw_Pact_member` vs. `WARSAW_PACT_member`) | `02_Warsaw_Pact_effects.txt:3`; `01_international_systems_effects.txt:2912` | [V]; [Ve] Folgen je nach Groß-/Kleinschreibung der Variablen |
| R12 | **1970 sind die Einfluss-Arrays leer:** Alle `influence_array`-Einträge stehen in `2000.1.1`-Blöcken, in IMP_1970/mdcw keine Initialisierung. Einflussbasierte Mechaniken (Finnlandisierung) starten bei null | z. B. `history/countries/FIN - Finland.txt:532-541` | [V] Suche; [Ve] keine andere Quelle |
| R13 | **CoCom-Widerspruch:** Die CoCom-Sanktionen 1970 erhöhen über `mdcw_cw_count_bloc_sanctions` die Spannungsbasis. Das SOV-CoCom-Angebot (142) senkt bei Annahme nur die Spannung und hebt keine Sanktion auf | `IMP_1970_sanctions_effects.txt:888ff.`; `mdcw_cold_war_effects.txt:993-1052`; Event 142 | [V] |
| R14 | **Die Haus-Dokumente `documentation/` und `docs/dev-resources/` fehlen** in der Arbeitskopie, obwohl das Playbook sie als verbindlich nennt (Master-Prompt, project_decisions, code-resource) | Ordner auf dem PC nicht vorhanden | [V] |
| R15 | **Tag-Fehler im Historienbericht:** Norwegen ist im Mod `NRY`, nicht `NOR` | `history/countries/NRY - Norway.txt`; Cold-War-Liste Z. 76 | [V] |
| R16 | **Tägliche Ticks** für GRE-, TUR- und CYP-Roster (`on_daily`) | `COLDWAR_TUR_1970_regional_on_actions.txt` | [V]; Performance gering, aber zu beachten, wenn die EG weitere Ticks hinzufügt |
| R17 | **Globale Einzel-Flags pro Abstimmungssystem** (`COLDWAR_SOV_vote_running`, `mdcw_cw_opec_vote_active`). Die EG braucht einen eigenen Namensraum und eine Warteschlange, sonst kollidieren die Variablen nicht, aber Ereignis-IDs und Anzeigen | — | [V]/[Ve] |
| R18 | **`IMP_sanctions_add_*_from_prev` ruft den Cold-War-Hook nicht auf.** Kollektive EG-Sanktionen über diese Helfer erhöhen die Spannung erst bei der monatlichen Neuzählung | `IMP_sanctions_support_effects.txt:5-52` | [V] |
| R19 | **Der Westblock enthält die Diktaturen GRE/SPR/POR** (über `fits_west`). Die EG-Demokratie-Klausel darf deshalb **nicht** `mdcw_cw_alignment = 1` oder `mdcw_cw_party_fits_west` nutzen, sondern `mdcw_cw_party_core_west` | `mdcw_cold_war_triggers.txt:62-87` | [V] |
| R20 | **Einseitige beidseitige Meinungs-Effekte** in SPR-Events (FRA/GER „declaration_of_friendship“ beidseitig ohne Zustimmung). Das ist nur Meinung, aber formal gegen die MP-Regel „Angebot statt Zwang“ | `events/SPR_1970_events.txt:886-895, 1537-1551` | [V] |

---

## 7. Gestagte Dateien (von Agent C)

Ziel: `/mnt/user-data/uploads/mdcoldwar/<Pfad>`. Schon vorher gestagt und mitgenutzt: `common/scripted_effects/{mdcw_cold_war_effects,IMP_1970_world_politics_effects,99_eu_scripted_effects,99_EU_voting_scripted_effects}.txt`, `common/national_focus/*` (u. a. `COLDWAR_GRE_1970_focus`, `COLDWAR_CYP_1970_focus`, `spain_1970`, `USA_1970`, `mdcw_1970_generic_focus`, `uk_1985`), `docs/*`.

- **common/decisions:**
  - mdcw_cold_war_decisions, NATO, Commonwealth, 99_mp_decisions, COLDWAR_SOV_1970_decisions
  - COLDWAR_GRE_1970_regional_decisions, COLDWAR_GRE_1970_tree_decisions, COLDWAR_TUR_1970_regional_decisions, COLDWAR_CYP_1970_decisions, COLDWAR_NCY_1970_decisions
  - SPR_1970_franco_decisions, imp_sanctions_decisions, Influence Decisions, un_voting_decisions, USA_1970_policy_decisions
  - ENG_1985_decisions, IMP_1985_eastern_bloc_decisions, investments_decisions
- **common/decisions/categories:**
  - mdcw_cold_war_decision_categories, COLDWAR_SOV_1970_decision_categories, NATO_decision_categories, un_voting_categories
  - mdcw_historical_ENG_IRQ_categories, imp_sanctions_cat, influence_decision_category, 99_mp_decision_categories
  - SPR_1970_decision_categories, COLDWAR_GRE_1970_tree_categories, Commonwealth_decision_categories, COLDWAR_CYP_1970_categories
- **common/scripted_effects:**
  - Bündnisse: 01_NATO_effects, 02_Warsaw_Pact_effects, 01_international_systems_effects
  - Sowjetunion: COLDWAR_SOV_1970_scripted_effects, COLDWAR_SOV_1970_putin_effects
  - Sanktionen: imp_sanctions_effects, IMP_1970_sanctions_effects, IMP_sanctions_support_effects, 00_sanctions_scripted_effects
  - Einfluss: 00_influence_scripted_effects, 99_AI_influence_scripted_effects
  - Ostmittelmeer: COLDWAR_GRE_1970_regional_effects, COLDWAR_GRE_1970_tree_effects, COLDWAR_TUR_1970_regional_effects, COLDWAR_CYP_1970_regional_effects, COLDWAR_CYP_1970_effects
  - Spanien und USA: SPR_1970_scripted_effects, USA_1970_nixon_diplomacy_effects, USA_1970_scripted_effects, USA_1970_policy_decision_effects
  - 1985-Inhalte: IMP_1985_eastern_bloc_scripted_effects, 99_DDR_1985_state_crisis_effects, IRE_1985_scripted_effects, 99_1985_western_pressure_effects
  - Länder-Effekte MD: 99_GRE, 99_TUR, 99_SPR, 99_GER, 99_ENG_scripted_effects., 99_Commonwealth, 99_FIN, 99_finland_effects
  - Imperia/Cold War: imp_money_transfer_scripted_effects, mdcw_imperia_globalism_effects, mdcw_imperia_debt_effects, mdcw_1970_generic_focus_effects, mdcw_1970_focus_tree_effects, IMP_1970_gdp_scripted_effects
  - MD-Grundlagen: !_global_reaction_effects, 00_scripted_effects, 00_money_system, 00_power_ranking_effects, 00_economic_effects, 00_economic_system_utilities, !_market_effects, 00_budget_effects, 00_currency_effects, 00_startup_effects, 00_country_classification_arrays, 00_country_group_flags
- **common/scripted_triggers:**
  - mdcw_cold_war_triggers, COLDWAR_SOV_1970_scripted_triggers, IMP_cold_war_scenario_triggers, mdcw_1970_generic_focus_triggers, IMP_1970_party_name_triggers
  - 00_NATO_scripted_triggers, 00_influence_scripted_triggers, 00_diplo_action_valid_triggers, 00_diplomacy_triggers
  - 99_EU_scripted_triggers, 99_EU_voting_scripted_triggers, IMP_1985_eastern_bloc_scripted_triggers
- **common/scripted_diplomatic_actions:** imp_sanctions_diplomatic_actions, imp_money_transfer_diplomatic_actions, mdcw_cold_war_diplomatic_actions
- **common/on_actions:**
  - Cold War/Imperia: mdcw_cold_war_on_actions, 00_IMP_cold_war_scenario_on_actions, 99_IMP_1970_world_on_actions, zzzzzz_imp_sanctions_on_actions, zzzzzz_mdcw_imperia_globalism_on_actions, mdcw_1970_USA_on_actions
  - Länder 1970: COLDWAR_SOV_1970_on_actions, COLDWAR_GRE_1970_regional_on_actions, COLDWAR_GRE_1970_tree_on_actions, COLDWAR_TUR_1970_regional_on_actions, COLDWAR_CYP_1970_regional_on_actions, SPR_1970_on_actions
  - MD: MD_NATO_on_actions, 99_SOV, 99_DDR, 99_GER, 99_GRE, 99_TUR, 00_on_actions, MD_on_actions
- **common/dynamic_modifiers:**
  - mdcw_cold_war_dynamic_modifiers, COLDWAR_SOV_1970_dynamic_modifiers, COLDWAR_GRE_1970_modifiers, SPR_1970_dynamic_modifiers, USA_1970_policy_dynamic_modifiers
  - imp_sanctions_dynamic_modifiers, 02_commonwealth_dynamic_modifiers, mdcw_imperia_globalism_dynamic_modifiers
- **common/ideas:**
  - Organizations, NATO, Factions, mdcw_cold_war_ideas, mdcw_cold_war_national_ideas
  - East_Germany, COLDWAR_GRE_1970_ideas, SPR_1970_ideas, COLDWAR_CYP_1970_ideas
- **events:**
  - Cold War und Imperia: mdcw_cold_war_events, mdcw_cw_assistance_notifications, imp_sanction_events
  - Sowjetunion und Bündnisse: COLDWAR_SOV_1970_events, NATO_system, Warsaw_Pact_system, IMP_1985_eastern_bloc
  - Länder 1970: SPR_1970_events, USA_1970_events, USA_1970_nixon_diplomacy_events, COLDWAR_GRE_1970_tree_events, COLDWAR_CYP_1970_events, DDR_1985
  - MD: UN_Voting_Events, MP_Enhancements, Diplomatic_Response, Influence
- **localisation/english:**
  - COLDWAR_GRE_1970_tree, COLDWAR_CYP_1970, COLDWAR_EASTMED_1970, COLDWAR_SOV_1970, SPR_1970
  - USA_1970_focus, USA_1970_nixon_diplomacy, USA_1970_policy_decisions, USA_1970_events
  - mdcw_cold_war, mdcw_1970_generic_focus, mdcw_historical_starting_spirits_0, mdcw_historical_NATO_tooltip
  - alle mit Endung `_l_english.yml`
- **history/countries:**
  - die Sechs: FRA, GER, ITA, BEL, HOL, LUX
  - Kandidaten und EFTA: ENG, IRE, DEN, NRY, ICE, POR
  - Neutrale: AUS, FIN, SWE, SWI
  - Mittelmeer: GRE, TUR, SPR, MLT, CYP
  - Osten: DDR, SOV, POL
  - EUU

Nicht vorhanden bzw. nicht stageable: `documentation/` (ganzer Ordner), `docs/dev-resources/code-resource.md`.
