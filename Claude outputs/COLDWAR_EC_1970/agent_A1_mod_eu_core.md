# Agent A1: Das EU-Kernsystem der Mod "MD Cold War" und das Szenario 1970

**Stand:** 18.10.2026. Es wurde nur gelesen: Code aus gestagten Kopien unter `/mnt/user-data/uploads/mdcoldwar/`. Auf dem PC wurde nichts verändert, und es lief kein Spieltest.
**Pfade** sind relativ zur Mod-Wurzel `mdcoldwar/`. Zeilenangaben beziehen sich auf den heutigen Dateistand.

**Legende**
- **[V] verifiziert:** im Code nachgelesen.
- **[?] vermutet:** Schluss aus Engine-Verhalten oder aus nicht gestagten Dateien. Muss im Spiel geprüft werden.

**Grenzen der Prüfung**
- Eine Volltextsuche ging nur über die gestagten Dateien (Liste in Anhang A). Andere Fokus-, Event- und Decision-Dateien der Mod wurden **nicht** komplett durchsucht. Ausnahmen sind `common/national_focus/*`, was andere Agenten gestagt haben, sowie die 1970-Länderdateien von SPR, GRE, TUR, CYP und SOV.
- Die Basis-Version ist **widersprüchlich**:
  - In der Aufgabe und im Projektgedächtnis steht MD 1.12.3B mit HOI4 1.18.
  - `README.md:3` sagt dagegen: *"migrated to the Millennium Dawn 2.0.2 base for Hearts of Iron IV 1.19"*, und `Changelog.txt:1` beginnt mit `v2.0.2`.
  - Die heutigen Restore-Berichte vergleichen die EU-Dateien mit der **aktuellen** Workshop-Version (`E:/SteamLibrary/.../2777392649`). Die EU-Dateien entsprechen also dem neuen MD, nicht 1.12.3B [V über die Berichte, Hash-Abgleich unten].

---

## 0. Kurzfazit

1. **Das aktive EU-System ist heute reines, unverändertes Millennium Dawn.**
   - Zwei 1970-Umbauten wurden heute Nacht gebaut und auf ausdrücklichen Wunsch des Nutzers wieder entfernt:
     - CWEC um 01:16 UTC,
     - "MD1970_EU / native extension" um 01:54 UTC.
   - Die fünf Dateien vom 18.10. sind genau diese Rückbauten. Sie enthalten keine COLDWAR-, IMP- oder 1970-Marker (Kap. 2).
2. **Für 1970 gibt es keinen Szenario-Guard.**
   - `on_startup_euu_action` läuft ungeprüft (`common/on_actions/00_on_actions.txt:1956`).
   - Es baut die moderne EU-15 als **Geister-Mitgliederarray** auf, gibt aber niemandem die Idea `EU_member` (Kap. 4).
3. Ergebnis 1970 ist ein **Zombie-System**:
   - Es ist sichtbar: Button für jeden menschlichen Spieler, Rat mit 15 Geistern.
   - Hintergrundschleifen laufen: Haushalts- und MFF-Missionen samt Popups bei UK, Franco-Spanien, Junta-Griechenland, Österreich und Schweden; die EP-"Wahl" 1974.
   - **Handeln kann niemand**: Ämter, Vorschläge und Haushalt verlangen die Idea `EU_member`.
4. Die einzige aktive Cold-War-Andockstelle an die Mitgliedschaft ist **Spanien**. Das Event `SPR_1970.227` gibt `EU_member` direkt, ohne Votum (`events/SPR_1970_events.txt:1676`).
5. **Schutz-Regression:** Der frühere Cold-War-Euro-Riegel in `joining_the_euro` (`date > 1998.12.31` plus DM-Tausch) ist mit dem Main-MD-Restore verschwunden (Diff in Kap. 2.3). Die Euro-Idea selbst bleibt datumsgesperrt (`common/ideas/AA_law_expanded_economics.txt:791-810`).
6. **Harter Sperrriegel für den Haushalt:**
   - Budget und MFF lassen sich nur mit einem EZB-Präsidenten abschließen. Dieses Amt verlangt die Idea `euro`, und die gibt es vor 1999 nicht.
   - Damit ist jede Haushaltsreform 1970–1998 strukturell unmöglich (Kap. 3.8).
7. Nahezu alle Inhalte sind auf 2000+ ausgerichtet: 53 Abstimmungsthemen von der Grundrechtecharta bis zur Wolga-Erweiterung, Art. 50, Frontex, OMT und Migrationskrise. Brauchbar ist die **Mechanik**: Arrays, Missionen, Dispatcher, Haushaltsrechnung, Ämter-Ideas, Europeanism-Variable und GUI. Die Inhalte nicht.

---

## 1. Überblick: Architektur des MD-EU-Systems

```
on_startup (00_on_actions.txt:1956)
  └─ on_startup_euu_action (99_eu_scripted_effects.txt:613)
       ├─ global.EU_member  ← 15 Tags (ohne Idea!)
       ├─ global.EU_potential_votes ← 53 Agenden
       ├─ global.EU_potential ← Collections (Mitglieder + Kandidatenpool)
       ├─ europeanism-Startwerte, Budget/MFF-Missionen, EUelection.2/.1
       └─ Ämter-Zeiger global.* = EUU.id (Leersitz)

Gesetzgebung:  EU_potential_votes ──(EP-Vorschlag, GUI)──► EP-Mission 14 T ──► EU_council_votes
               ──(Rats-Vorschlag, GUI)──► QMV-Mission 14 T ──► apply_EU_QMV_result ──► EU_passed_votes
Monatlich:     set_EU_gdp, check_breach_of_EU_value, EU_update_vars, Migrationskrisen-Check (MD_on_actions.txt:724-806)
Wöchentlich:   Beiträge/Subventionen im Geldsystem nur für has_idea = EU_member (00_money_system.txt:1033-1043, 4012-4015)
```

---

## 2. Jüngste Änderungen am 18.10.2026 (Aufgabe 3)

### 2.1 Teamnotizen: Was heute passiert ist [V]

| Zeit (UTC) | Vorgang | Beleg |
|---|---|---|
| ~01:04 | Referenz-Manifest der Original-MD-Dateien erstellt | `docs/europe_1970_audit/original_md_reference_manifest.json` (mtime) |
| 01:16 | **CWEC-System entfernt**, "Native MD EU restored". 9 Dateien auf den Stand vor CWEC zurückgesetzt, `MD_on_actions.txt` selektiv zurückgesetzt, 29 CWEC-Laufzeitdateien gelöscht | `docs/europe_1970_audit/native_restore.md`, `native_restore_report.json` |
| 01:29–01:43 | Neuer Ansatz "1970 European Communities inside the native MD interface" (Präfix `MD1970_EU_*`, `MD1970_EC_*`) gebaut und validiert (57 Tests) | `docs/native_eu_1970/README.md`, `baseline.json`, `validation_report.json` |
| **01:54** | **Auch dieser Ansatz entfernt**: "all custom CWEC and MD1970 EU adaptations were removed at the user's explicit request". 13 Dateien wiederhergestellt, 21 Tool-Dateien archiviert | `docs/main_md_eu_restore/README.md`, `restore_report.json` |

Die fünf in der Aufgabe genannten Dateien tragen alle mtime 01:54:02 UTC (= 03:54 MESZ). Ausnahme ist `EU_voting_categories.txt` mit 01:16:29 UTC. Sie gehören also zu diesen Rückbauten.

**Archivierte Vorarbeiten**
Die Archive sind für einen neuen Anlauf als Referenz nützlich, sind aber nicht aktiv:
- `docs/europe_1970_audit/native_eu_restore_backup_20261018T011628Z.zip`: CWEC-Code (eigene GUI `interface/CWEC.gui`, 29 Dateien) und die Audit-Dokumente `agent_core.md`, `agent_paths.md`, `agent_voting_ui.md`, `einbauplan_1970.md`, `europa_1970_konzept.md`, `implementation.md`.
- `docs/main_md_eu_restore/removed_eu_adaptation_20261018T015402Z.zip`: MD1970_EU-Code. Darin u. a.:
  - `MD1970_EU_core_effects.txt`, `..._seat_effects.txt` (142→198→410… Sitze), `..._voting_effects.txt`, `..._finance_effects.txt`
  - 118 zusätzliche historische und alternative Agenden
  - Flaggen `gfx/flags/MD1970_EC_*.tga`
  - Tools `tools/native_eu_1970/*.py`
- `docs/native_eu_1970/native_before_extension.zip`: Stand der nativen Dateien vor MD1970.

> **Wichtig für die weitere Planung:** Der Nutzer hat heute zwei vollständige 1970-EU-Umbauten verworfen:
> 1. einen mit eigener GUI,
> 2. einen in der nativen MD-GUI mit Spieler-only-Abstimmungen, Geldbuchung und 118 Agenden.
>
> Den Grund nennen die Dokumente nicht. Ein dritter Anlauf sollte den Grund vorher klären. Plausibel wären zu groß, zu invasiv in MD-Dateien oder am Ziel vorbei. Daraus sollte ein schlankerer, schrittweiser Ansatz mit klaren COLDWAR-Hooks folgen.

### 2.2 Marker und Inhalte der fünf Dateien [V]

`grep -iE "COLDWAR|IMP_|mdcw|1970|has_start_date|CWEC|MD1970"` findet **0 Treffer** in:
- `common/scripted_effects/99_eu_scripted_effects.txt`
- `common/scripted_effects/99_EU_voting_scripted_effects.txt`
- `common/decisions/EU_voting_decisions.txt`
- `common/decisions/categories/EU_voting_categories.txt`
- `events/EU_events.txt`

Dasselbe gilt für GUI, Trigger, Ideas, POTEF/USoE/EFS-Decisions und `EU_news`/`EU_USoE_events`.

### 2.3 Hash-Abgleich mit den Backups [V]

| Datei | heute = Stand vor der Erweiterung? |
|---|---|
| `99_EU_voting_scripted_effects.txt`, `EU_voting_decisions.txt`, `EU_voting_categories.txt`, `EU_events.txt`, `Organizations.txt`, `01_european_union_guis.txt`, `99_EU_voting_scripted_triggers.txt`, `MD_on_actions.txt`, `00_money_system.txt` | **ja, bytegleich** |
| `99_eu_scripted_effects.txt` | **nein**, einziger Unterschied ist `joining_the_euro` |

Was dort fehlt, hatte der Stand vor der Erweiterung noch:
```
# Historical currency compatibility: an event/GUI cannot force the euro into 1970.
if = { limit = { date > 1998.12.31 }
    if = { limit = { has_idea = deutsche_mark } swap_ideas = { remove_idea = deutsche_mark add_idea = euro } }
    set_country_flag = EU_joined_the_eurozone ...
```
Heute (`99_eu_scripted_effects.txt:1829-1915`) setzt `joining_the_euro` die Flagge und tauscht ohne Datumsprüfung. `deutsche_mark` wird nicht berücksichtigt.

Laut `docs/europe_1970_audit/native_restore.md` war dieser Riegel eine **ältere Cold-War-Anpassung**: "the preexisting historical euro date restriction were retained". Der Main-MD-Restore hat ihn bewusst entfernt ("historical_euro_guard_retained": false, `docs/main_md_eu_restore/restore_report.json`).

**Andere Cold-War-Währungsanpassungen sind noch aktiv [V]:**
- `00_currency_effects.txt:65-68`: DM für GER vor 1999.
- `00_currency_effects.txt:86-100`: DEM-Emittent Bonn, kein EUR-Emittent vor 1999.
- `AA_law_expanded_economics.txt:783-810`: `deutsche_mark` nur vor 1999, `euro` unsichtbar und vor 1999 gecancelt.

**Folge [?]:** Gelangt 1970 ein Land über `EU_join_the_euro_decision` (`EU_voting_decisions.txt:1806`) in den Euro, passiert Folgendes: `joining_the_euro` entfernt die bisherige Reserve-Idea, z. B. `british_pound` oder `no_foreign_reserve`, und setzt `euro`. `euro` wird sofort per `cancel` entfernt. Übrig bleibt ein Land **ohne Reservewährungs-Idea**, aber mit Flagge `EU_joined_the_eurozone`.
Die Decision ist nur für `has_idea = EU_member` sichtbar. Das betrifft 1970 praktisch nur Spanien über `SPR_1970.227`.

---

## 3. Inventar der EU-Mechaniken (Aufgabe 1)

### 3.1 Datenmodell der Mitgliedschaft [V]

| Element | Ort | Inhalt |
|---|---|---|
| Idea `EU_member` (kanonisch) | `common/ideas/Organizations.txt:4-38` | `on_add` (Z. 7-15): ins Array `global.EU_member`, `EU_init_default_europeanism`, `EU_adopt_passed_laws`. `on_remove` (Z. 16-27): aus dem Array entfernen, `leaving_EU` mit Schutzflagge. Modifier (Z. 29-37): demokr. Drift +0,05, Neutralitätsdrift +0,03, **PP-Faktor −20 %**, Kriegsunterstützung −5 %, Handelsmeinung +15 %, Stabilität +5 %, Konsumgüter −5 %. `allowed_civil_war` immer ja |
| Array `global.EU_member` | gepflegt per `on_add`/`on_remove`; Start in `99_eu_scripted_effects.txt:760-774`; Resync `:412-429`; Annex-Cleanup `common/scripted_effects/01_international_systems_effects.txt:2882-2890` | Grundlage für fast alle Schleifen (Abstimmung, Haushalt, EP, News) |
| Array `global.EU_potential` | Aufbau `99_eu_scripted_effects.txt:785-792` aus `collection:eu_members_collection` + `eu_potential_countries_collection` (`common/collections/collections.txt:3-17`) | Grundmenge `constant:country_groups.all_eu_available_countries` (`common/script_constants/country_groups.txt:134ff`): 93 Tags inkl. SOV, RUS, ABK, DPR, LPR, CRM, CAT, SCO. **Ohne DDR** |
| Trigger `EU_is_potential` | `common/scripted_triggers/99_EU_scripted_triggers.txt:659-757` | Liste von `original_tag`. Steuert, ob die Decision-Kategorien erlaubt sind (`common/decisions/categories/EU_voting_categories.txt:1-82`) |
| Flaggen | `EU_candidate`, `EU_former_member`, `EU_rejoin_cooldown` (1095 T), `adopt_eu_law`, `Article_50`, `withdrawal_treaty`, `EU_joined_the_eurozone`, `USoE`, `USoE_member` | gesetzt in Voting-Effekten, `leaving_EU`, GUI und History (2000-Blöcke) |
| Opinion-Modifier `EU_member_opinion` | `common/opinion_modifiers/Organization Opinions Modifiers.txt` | +20. Nur in History-2000-Blöcken gesetzt und in `leaving_EU` entfernt |
| Tag EUU | `history/countries/EUU - EU.txt` | **Platzhalter-Scope** ohne Gebiet. Ämter-Leersitz (`global.* = EUU.id`, `99_eu_scripted_effects.txt:856-866`), Mission `EU_election_5_years` (`available = { tag = EUU }`, `EU_voting_decisions.txt:2-17`), Technologie-Pool für USoE |
| Hidden Idea `EUU_monitor` | `common/ideas/EU_ideas.txt:440-443` | Ein zufälliges KI-Land aus `EU_potential` ist "Monitor" für monatliche Rechnungen und POTEF-Wahlen |

### 3.2 Initialisierung `on_startup_euu_action` [V]

`99_eu_scripted_effects.txt:613-879`, aufgerufen in `00_on_actions.txt:1956` (ABK-Scope, **ohne Szenario- oder Datumsabfrage**).
- Z. 615-634: Spielregel `rule_disable_eu` setzt `GAME_RULE_eu_disabled`. Die Schleife über das Array ist an dieser Stelle noch leer.
- Z. 636-689: Cooldown-Regel `rule_european_union_voting_limits` (1/60/90/120/180/210 Tage) setzt globale Flaggen.
- Z. 692-854: einmalige Initialisierung (`EU_initialized`):
  - 53 Agenden in `global.EU_potential_votes` (Z. 699-751).
  - Hilfsarray `global.starting_mep_support_parliament`.
  - **15 Mitglieder ins Array** (Z. 760-774): AUS, BEL, DEN, ENG, FIN, FRA, GER, GRE, HOL, IRE, ITA, LUX, POR, SPR, SWE.
  - **Strafideas `foreign_data_kraken` und `asylum_shopping` für alle 15** (Z. 777-783).
  - `EU_potential` aufbauen.
  - Zufälliger KI-Monitor erhält sofort `EUelection.2` und nach **1625 Tagen** `EUelection.1` (Z. 794-802; Kommentar: "historical June 2004").
  - Europeanism: Standard 0,3 für `EU_potential`. Feste Werte für die 15 (BEL 0,9, FRA 0,86, GER 0,85, GRE 0,92, POR 0,95, SPR 0,94, IRE 0,94, ENG 0,76, SWE 0,62 …), dazu SOV 0,05 und VTB 0,5 (Z. 810-831).
  - `EU_update_vars`, `EU_init_focus_vote_weights`, optional Expansion-Bias.
  - Für alle 15: Missionen `EU_budget_draft_preparations` und `EU_mff_draft_preparations`, Abrufsatz 1 % BIP.
  - Haushalt initialisieren (Z. 839-853).
- Z. 856-875: Ämter-Zeiger auf EUU, 24er-Parteigruppen-Arrays.

### 3.3 Beitritt [V]

- **Kandidatenstatus:** Flagge `EU_candidate` entsteht nur durch:
  - erfolgreiche Erweiterungs-Agenden (`99_EU_voting_scripted_effects.txt:887-1088`, Kohorten siehe 3.5),
  - den MD-Schweizfokus (`common/national_focus/05_switzerland.txt:7709`; 1970 nicht aktiv, SWI lädt `mdcw_1970_generic_focus`).
- **Beitritts-Decision `EU_apply_for_membership`** (`EU_voting_decisions.txt:1635-1804`, Kosten **50 PP**):
  - Bedingungen: `breach_of_EU_value < 3`; Kandidat (oder Ex-Mitglied ohne Cooldown); kein Krieg; kein CHI- bzw. SOV-Einfluss über 15 % (Ausnahme SOV als Kandidat); Europeanism > 0,79 (Mensch) bzw. > 0,69 (KI).
  - Wirkung: **sofort `add_ideas = EU_member`**, ohne Votum der Mitglieder.
  - Wenn `EDU` existiert: NATO-Idea entfernen und in die EU-Fraktion wechseln (Z. 1687-1711).
  - News `EU_news.27`.
  - KI: Faktor 100 ab 2004, 2007 und 2013 (Z. 1788-1802).
- **Vorbeitrittshilfe:** GUI-Knopf `approve_IPA_button_click` (`common/scripted_guis/01_european_union_guis.txt:2406`) gibt Kandidaten Mission `pre_accession_assistance_program` (`EU_voting_decisions.txt:1880`) und Idea `EU_pre_accession_assistance` (`EU_ideas.txt:310`, `europeanism_drift +0,02`). Die Drift wirkt monatlich über `EU_update_vars` (`99_eu_scripted_effects.txt:100-109`).
- **Cold-War-Andockstelle:**
  - `common/national_focus/spain_1970.txt:1241` `SPR_1970_apply_to_the_european_communities` setzt die Flagge `SPR_1970_european_communities_application`.
  - `:2114` `SPR_1970_accession_to_the_european_communities` führt zu `events/SPR_1970_events.txt:1676` `SPR_1970.227`: `add_ideas = EU_member`, Infrastruktur, Idea `SPR_1970_european_development_funds_idea` (730 T), Europeanism +0,03.
  - Kein Votum, kein `EU_news.27`, keine Kandidatenflagge.
- **Weitere Konsumenten der Idea** (laut Grep):
  - `common/decisions/Influence Decisions.txt:332ff` (Einflussboni gegenüber EU-Mitgliedern)
  - `common/decisions/NATO.txt:645`
  - `common/decisions/formable_nation_decisions.txt:311, 2709…`
  - `common/scripted_effects/00_money_system.txt:1037, 4013`
  - `common/ideas/AA_law_expanded_economics.txt:793-806`

### 3.4 Austritt [V]

| Element | Ort | Inhalt |
|---|---|---|
| Art.-50-Auslöser | GUI `EU_Article_50_click` (`01_european_union_guis.txt:1789-1795`), Bedingung `:520-540` (Mitglied, hält kein Amt; KI nur bei Europeanism < 0,4 **oder** `EU_external_sov_chi_influence_50`) | Mission `EU_exit` (730 T), Flagge `Article_50`, Ämter räumen, `EU_news.34` |
| Folge-Decisions | `EU_voting_decisions.txt:777-1207` | `EU_Revoke_Article_50`; `EU_exit` (Timeout ergibt No-Deal 1825/730 T); `EU_extend_Article_50` (Einfluss ≥ 25 % auf außenpolitischen Amtsträger); `EU_exit_three_month` (90 T); `EU_withdrawal_treaty`; `EU_prepared_no_deal_exit` (150 PP) |
| Technisches Cleanup `leaving_EU` | `99_eu_scripted_effects.txt:343-409` | Idea weg, Ex-Mitglied, Cooldown 1095 T, `euro` weg, Opinion weg, 20 Gesetzes-Ideas weg, Tech-Sharing raus, Ämter räumen (`EU_vacate_offices` `:294-340`), Frontex- bzw. EuroArmy-Kontrolle abgeben, Missionen entfernen, EDU verlassen |
| Unfallaustritt | `EUevent.9` (`events/EU_events.txt:307-327`) über `troika_reforms`-Timeout | No-Deal + `leaving_EU` |
| Annexion | `common/on_actions/MD_on_actions.txt:294-327` | annektiertes Mitglied: laufende Abstimmung abbrechen, `leaving_EU`, Monitor neu vergeben |
| Bürgerkrieg | `MD_on_actions.txt:609-612` | `EU_resync_member_array` entfernt **alle** Array-Einträge ohne Idea |

**MD-Bug [?]:**
- `withdrawal_treaty`, `no_deal_exit` und `austerity` haben `cancel = { NOT = { has_idea = EU_member } }` (`EU_ideas.txt:389-423`).
- Sie werden aber vor bzw. unmittelbar mit `leaving_EU` vergeben (`EU_voting_decisions.txt:845-861, 878-885`).
- Folge: Die Austrittsstrafen dürften sofort wieder entfallen. Das ist Engine-Semantik von `cancel`, im Spiel nicht geprüft.

### 3.5 Abstimmungssystem (EU_voting_*) [V]

**Ablauf**

1. **Vorschlag im Parlament** (GUI `eu_parliament_available_reforms_button_click`, `01_european_union_guis.txt:4989-5070`; Bedingungen `:4601-4987`).
   - Voraussetzungen: Mitglied (Sichtbarkeit), kein Delay, **Kommissionspräsident vorhanden oder < 2 Array-Mitglieder**, keine laufende Agenda, kein Budget- bzw. MFF-Block, kein CHI- bzw. SOV-Einfluss > 15 %, Vorgänger-Agenden bestanden.
   - Kosten: 200 PP (101, 201, 203, 204, 301, 401-403) bzw. 300 PP (601-660, 111, 112). Alle übrigen kosten 0.
   - Alle Mitglieder erhalten 14 Tage die Mission `EU_parliament_focus_EUXXX_approve` (`EU_voting_decisions.txt:22-125`). Menschen erhalten Popup `EUvote.1` bzw. `.6`.
2. **Parlament:**
   - Der Vorschlagende erhält automatisch die Unterstützung seiner Regierungspartei-Gruppe (`set_ruling_party_PG_support`, `99_eu_scripted_effects.txt:1769`).
   - Weitere Parteigruppen kauft man mit PP: MEP-Zahl × 2 (`01_european_union_guis.txt:640-663`, `2025ff`).
   - Mehrheit = MEP-Gesamt × 0,5 + 1 (`99_eu_scripted_effects.txt:1673`).
   - Menschen drücken "Pass" (`:2291`). Sonst entscheidet der Kommissionspräsident bzw. der Verwalter beim Timeout.
   - Erfolgreiche Agenden gehen nach `global.EU_council_votes` (`99_EU_voting_scripted_effects.txt:1091-1151`).
3. **Rat** (GUI `eu_council_available_reforms_button_click`, `01_european_union_guis.txt:4382-4433`; Bedingungen `:4257-4380`).
   - Der Vorschlagende zahlt 500 PP, außer er hält Kommission, Rat oder Parlament oder hat ≥ 3 % Einfluss auf alle.
   - Alle Mitglieder erhalten 14 Tage die Mission `EU_voting_mission_focus_EUXXX_QMV_result` (`EU_voting_decisions.txt:385-412`).
   - Menschen: Popup `EUvote.2`; Sonderfall `EUvote.5` bei 111.
   - **KI-Stimmen werden sofort berechnet** (`EU_update_AI_focus_voting_modifier`, `99_EU_voting_scripted_effects.txt:255-310`):
     - Parteiwerte w1..w6 je Agenda (`:170-227`)
     - "historische" +100 bei historischem Fokus
     - Europeanism-Stufen
     - Einfluss
     - SOV/CHI-Einfluss −25…−75
     - Untertanen folgen dem Oberherrn
     - Schwierigkeitsgrad
     - Positiver Wert heißt Ja (`:5-108`).
   - Menschen klicken Support oder Reject (`01_european_union_guis.txt:2638-2675`). Andere Länder umstimmen kostet 300 × pop_ratio × 25 PP (`:4435-4475`).
4. **Ergebnis** beim Timeout durch den Kommissionspräsidenten bzw. Verwalter (`apply_EU_QMV_result`, `99_EU_voting_scripted_effects.txt:316-383`):
   - **Bestanden**, wenn `global.EU_pop_ratio_yes > 0.65` **und** Anteil der Ja-Länder > 0,55 (`common/scripted_triggers/99_EU_voting_scripted_triggers.txt:16-23`).
   - **Kein Veto**, keine Einstimmigkeit, keine Unterscheidung nach Rechtsgrundlage.
   - Danach `cleanup_european_union_voting` (`:1154-1178`): Rats-Delay je nach Spielregel.
5. **Sonderfall 111 (USoE):** wird **unabhängig vom Ergebnis** ausgeführt (`:318-321`).
   - Ablehner werden ausgeschlossen (`remove_ideas = EU_member`).
   - Alle anderen werden vom Kommissionspräsidenten annektiert (`:406-504`).
   - Menschen können in `EUvote.5` ablehnen (dann Austritt) oder sich enthalten (dann Annexion) (`events/EU_events.txt:72-110`).
6. **Rivalisierende Endspiele 111 und 112** schließen sich gegenseitig aus (`EU_drop_rival_endgame`, `:385-403`).

**KI-Initiative**
- Parlament: `01_european_union_guis.txt:5076ff`. Gewichte nach Europeanism, Sozialistenblock +25, vor dem 1.6.2000 −10, "historisch" +250 ab 2004/07/13.
- Rat: `:4484-4560`. Faktor 0 für 110-112, wenn `rule_enable_ai_european_union_end_game_paths = no`.
- Prüfintervall 4,5 bzw. 4 bzw. 7 Tage.

**Spielregeln** (`common/game_rules/00_game_rules.txt:299-384`): `rule_disable_eu`, `rule_european_union_voting_limits`, `rule_european_union_expansion_focus`, `rule_enable_ai_european_union_end_game_paths`.

**Alle 53 Abstimmungsthemen** (Start-Array `99_eu_scripted_effects.txt:699-751`; Wirkungen `99_EU_voting_scripted_effects.txt:406-1088`; Vorgänger `01_european_union_guis.txt:4636-4987`)

| ID | Thema | Wirkung bei Annahme (Kurz) | Vorgänger, Kosten |
|---|---|---|---|
| 101 | Grundrechtecharta | Idea `EUU_cfr_eu` (+8 % Stab.), Europeanism +0,02 | 200 PP |
| 102 | Europäischer Konvent | `european_spirit` 600 T, +0,03 | 101 |
| 103 | Verfassung | `european_spirit`, +0,03 | 102 |
| 104 | Vertrag von Lissabon | `european_spirit`, Flagge `treaty_of_lisbon`, EP 750 Sitze | 103 |
| 105 | Europäischer Auswärtiger Dienst | Flagge schaltet Amt "Außenbeauftragter" frei | 104 |
| 110 | Föderalisierung | keine (Tor zu 111/112) | 208, 305, 306, 406 |
| 111 | United States of Europe | Bildung des Formables durch Annexion aller Zustimmenden | 110; 300 PP; schließt 112 aus |
| 112 | Europäische Föderation | Flagge `european_federation`: POTEF-Wahlen, POTEF-Baum, EFS-Flaggen | 110; 300 PP; schließt 111 aus |
| 201 | EZB-Intervention | `ECB_zero_interest_rate_policy` | 200 PP |
| 202 | Bankenunion | +5 % Stab., Schuldenkrise weg | 201 |
| 203 | Eurobonds | `euro_bonds`, Schuldenumverteilung | 200 PP |
| 204 | EFSF | +10 % Stab., Troika-Missionen POR/ITA/IRE/GRE/SPR/CYP | 200 PP |
| 205 | ESM | `euro_rescue_package` | 204, 203 |
| 206 | Fiskalunion | `fiscal_union` | 104, 202 |
| 207 | Europ. Wirtschaftsregierung | Idea | 205 |
| 208 | Europ. Wirtschafts- und Finanzminister | Amt freigeschaltet | 207, 206 |
| 301 | Verteidigungsagentur | Tech-Sharing `EU_Tech_Share` | 200 PP |
| 302 | PESCO | Tech-Sharing +8 % | 301 |
| 303 | Verteidigungsfonds | Idea | 302 |
| 304 | Europ. Sicherheitsrat | Idea (`can_create_factions = no`, +25 % PP-Faktor): EDU, Manöver | 303, 105 |
| 305 | EuroArmy | Amt und OOB `EU_EuroArmy_basic_2000` | 304 |
| 306 | EuroNavy | Amt | 304 |
| 307 | EU-Sitz im UN-Sicherheitsrat | Amt "UN-Botschafter" | 305, 306, 308 |
| 308 | EU-Atommacht | `nuclear_power_def` für alle | 305, 306 |
| 401 | DSGVO | `EUU_idea_gdpr` ersetzt `foreign_data_kraken` | 200 PP |
| 402 | Urheberrechtsrichtlinie | Idea, −3 % für drei Parteien | 200 PP |
| 403 | Dublin II | `asylum_shopping` weg, Nationalisten +3 % | 200 PP |
| 404 | Umverteilung Asylsuchender | Idea, Nationalisten +5 % | 403 |
| 405 | EU-Türkei-Deal | Idea, Zahlung an TUR | 403, Migrationskrise, TUR kein Mitglied |
| 406 | Asylagentur | Idea | 408, 404 |
| 407 | Frontex | Idea | 403, 301 |
| 408 | Grenz- und Küstenwache | Amt Frontex-Direktor | 407 |
| 601 | Erweiterung 2004 | Kandidat: CYP, CZE, EST, HUN, LAT, LIT, MLT, POL, SLO, SLV | 300 PP, **`date > 2002.1.1`** (`:4864`) |
| 602 | Erweiterung 2007 | BUL, ROM | 601 |
| 603 | Erweiterung 2013 | CRO | 602 |
| 605 | Westbalkan | ALB, SER, MNT, FYR, BOS, RSK, HZG, KOS | 603 |
| 606 | Türkei | TUR | 603 |
| 607 | Östliche Partnerschaft | MLV, UKR | 603 |
| 608 | Kaukasus | ARM, AZE, GEO | 603 |
| 609 | EFTA und Kleinstaaten (EWR) | SWI, **NRY**, ICE, HLS, SMA, MNC, ADO, LIC | 603 |
| 610 | Belarus | BLR | 603 |
| 611 | Interne Erweiterung | CAT, CRE, SCL, SCO, WAS, IOM, GAL, SIL, SPA, CNR, NAV, BAY, GRN, FAO, RUS | 603 |
| 650 | Erweiterter Erweiterungsrahmen | keine | 603 |
| 651 | Lissabon-Änderung | EP 1000 Sitze | 650 |
| 652 | EU-Russland-Partnerschaft | keine | 651 |
| 653 | Russland | SOV Kandidat | 652 |
| 654-660 | Barents-, Wolga-, Don-Kuban-, Nordkaukasus-, Ruthenien-, Donez-, Dnjepr-Erweiterung | Kandidatur der jeweiligen Abspaltungs-Tags | 651 |
| 998 / 999 | MFF- bzw. Jahreshaushalts-Entwurf | EP-Abstimmung über die Haushaltsentwürfe | EZB-Präsident nötig (3.8) |

Zwei Kleinfehler in MD [V]:
- Der Tooltip zu 601 nennt auch ROM (`localisation/english/MD_focus_EU_l_english.yml:1268`), der Effekt nicht.
- `EU_init_focus_vote_weights` enthält eine verwaiste Zeile 703 (`99_EU_voting_scripted_effects.txt:205`).

**1970-relevante Erweiterungen fehlen ganz.** UK, IRE und DEN sind in MD Gründungsmitglieder 2000. Es gibt keine Agenda, die sie zu Kandidaten macht. NRY gibt es nur über 609, und dieser Weg erfordert 601 und damit ein Datum nach 2002.

### 3.6 Euroskeptizismus [V]

- **`eurosceptic_change` existiert in den gestagten Dateien nicht.**
- Euroskepsis ist das Gegenteil der Länder-Variable `europeanism` (0–1).
- Effekte:
  - `europeanism_change` (Ziel ROOT oder ein Tag) (`99_eu_scripted_effects.txt:119-137`)
  - `europeanism_change_this_and_root` (`:140`)
  - `EU_europeanism_change` (alle Mitglieder, `:152`)
  - `EU_potential_europeanism_change` (alle möglichen Mitglieder, `:177`)
  - Kandidaten-Mindestwert 0,5 (`:199`)
  - Standardwert 0,3 (`:207`)
- **Global:** `global.var_europeanism`, nach Bevölkerung gewichtet (`EU_update_vars` `:29-112`).
- **Passive Drift** über Modifier `europeanism_drift`: nur für `EU_potential`, monatlich (`:100-109`; Quellen `european_spirit` und `EU_pre_accession_assistance`, `EU_ideas.txt:301-320`).
- **Folgen:**
  - Regierungs-Trigger `gov_is_eurosceptical` und `gov_is_EUexiteer` (`99_EU_scripted_triggers.txt:455-603`): Parteifamilie plus Schwellen 0,3–0,5; Nationalisten immer.
  - KI-Abstimmung (3.5), KI-Austritt, Beitrittsschwelle (0,79/0,69), Rats-Vorschlag gesperrt bei ≤ 0,6 (`01_european_union_guis.txt:4305-4310`).
- **Kampagnen (GUI):**
  - pro-europäisch national: 50 PP + 0,2 % BIP, 70 % Chance auf +0,05 (`:2537`)
  - pro-europäisch EU-weit: nur Mitglieder (`:2574`)
  - euroskeptisch national: Mitglieder (`:2423`)
  - euroskeptisch EU-weit: **auch Nicht-Mitglieder**, 300 PP + 0,4 % BIP, −0,03/−0,05 für alle `EU_potential` (`:2460-2535`)
- **2000er-Annahme:** `stop_pro_european_campaign` und `stop_euroscepticism_campaign` sind bis zum **15.1.2000 immer wahr** (`99_EU_scripted_triggers.txt:619-657`). Das gibt der KI −40 auf Kampagnen; die KI kampagnisiert also 1970–1999 praktisch nie. SOV-Bonus für die EU-weite Euroskepsis-Kampagne erst ab 2004 (`01_european_union_guis.txt:3698-3703`).

### 3.7 Werteverstöße (Art. 7) [V]

- `check_breach_of_EU_value` (`99_eu_scripted_effects.txt:435-520`) ist ein Summenwert aus:
  - Korruption 1-5
  - Angriffskrieg gegen Mitglieder +10
  - Kommunisten bzw. Reaktionäre in Koalition +1 bzw. Regierung +2
  - `no_women_in_military` +1
  - Interventionismus +1
  - Wahlhürde > 9,5 % +1
  - Schuldenausfall +1
  - keine Wahlen +5
  - Diktatur-Ideas +5
  - Untertan +4
- Läuft monatlich für alle `EU_potential` (`MD_on_actions.txt:751-761`).
- Decisions (je 100 PP; Feststellen > 3, Stimmrecht entziehen > 4, Subventionen sperren): `EU_voting_decisions.txt:127-378`. Ideas `EUU_voting_rights_suspended` und `EUU_subsidies_suspended` (`common/ideas/EU_Council_ideas.txt`).
- Befugnis: Top-3-Einfluss-Konsens oder Kommissionspräsident (`99_EU_scripted_triggers.txt:388-426`).

### 3.8 Haushalt und MFF [V]

- **Einnahmen:** Beitrag = BIP × Abrufsatz × 0,01, wöchentlich /52 (`update_EU_budget_call_rate`, `99_eu_scripted_effects.txt:1312-1355`). MFF-Anzeige = Jahreshaushalt × 5. Dazu EUR-Seigniorage-Pool (`MD_on_actions.txt:95-97`).
- **Ausgaben:** `set_EU_expenditure` (`:1373-1384`) teilt auf in Wachstum 44 %, Natürliche Ressourcen/Agrar 44 %, Globales Handeln 6 %, Verwaltung 6 %.
- **Verteilung:**
  - Wachstum: Bevölkerung × Konjunkturstufe (`:1412-1444`)
  - Natürliche Ressourcen: Bevölkerung × BIP/Kopf-Stufe mit Schwellen bis 200 (`:1446-1481`); 1970 hat GER `gdp_per_capita` 3,551 bis 2,8 → alle in den höchsten Stufen
  - Globales Handeln: an den außenpolitischen Amtsträger (`:1399-1406`)
  - Verwaltung: Kommission bzw. Frontex (`:1484-1532`)
- **Buchung:**
  - Ausgaben: `00_money_system.txt:4012-4015` (`additional_expenses_rate`)
  - Einnahmen: `:1032-1043` (Faktor 0,019 ≈ 1/52)
  - **Nur für `has_idea = EU_member`.**
- **Zyklus:**
  - Jahreshaushalt: 344 + 7 + 14 Tage (`EU_voting_decisions.txt:415-519`)
  - MFF: 1237 + 14 + 28 Tage (`:521-625`)
  - Entwürfe sichern bzw. zurückrollen (`99_eu_scripted_effects.txt:1256-1289`)
  - PP-Kosten je Klick 10 bzw. 15 × Mitgliederzahl (`:1357-1371`)
- **Sperrriegel:** Abschluss nur durch `ECB_president` bzw. ein Mitglied mit diesem Amt (`EU_voting_decisions.txt:476, 495, 582, 601`). Die Fiskal-Buttons verlangen ebenfalls den EZB-Präsidenten (`01_european_union_guis.txt:1340-1355`, `EU_min_call_rate_click_enabled`). Das Amt verlangt `has_idea = euro` (`:289-303`), und `euro` ist vor 1999 gecancelt. **Vor 1999 ist der Haushalt nicht reformierbar** [V über die Kette].
- **Altbekannte MD-Schwäche [V]:** Subventionsvariablen werden bei Amtswechsel nicht genullt (`:1395-1410`, `:1484-1532`).

### 3.9 Ämter [V]

| Amt (Idea) | Ort | Bonus | Zeiger | Claim-Bedingung (GUI) | Laufzeit |
|---|---|---|---|---|---|
| Kommissionspräsident `EU_commission_president` | `EU_ideas.txt:4-19` | PP +0,30 | `global.eu_commission` | Mitglied, frei, kein anderes Amt, Einfluss ≥ 5 % auf alle **oder** Bevölkerung > 5 % (`01_european_union_guis.txt:274-288`) | 1825 T (`:1872`) |
| Ratspräsident `EU_council_president` | `:20-35` | PP +0,15 | `global.eucouncil` | ähnlich (`:170`) | 1825 T (`:1823`) |
| Parlamentspräsident | `:36-51` | +0,10 | `global.euparliamentpresident` | | 1825 T |
| Frontex-Direktor | `:52-67` | +0,10 | `global.eufrontex` | Flagge aus 408 | 1825 T |
| Außenbeauftragter `EU_foreign_minister` | `:68-86` | Einfluss/Meinung | `global.euforeignaffairs` | Flagge aus 105 | 1825 T |
| EZB-Präsident `ECB_president` | `:87-104` | Konjunkturkosten −15 %, PP +0,10 | `global.eucentralbank` | **`has_idea = euro`** (`:289-303`) | **2920 T** (`:1883`) |
| Wirtschafts- und Finanzminister | `:105-122` | | `global.eufinance` | Flagge aus 208 | 1825 T |
| UN-Botschafter, EuroArmy, EuroNavy, POTEF `EU_president` | `:123-195` | | `global.euambassador/euarmy/eunavy/eupresfederation` | Flaggen aus 307/305/306/112 | 1825 T |

- Alle Ämter: `cancel = NOT EU_member`. Bei `on_remove` gehen Benachrichtigungen (`EUevent.21`) an alle Array-Mitglieder.
- Rücktritt: `retire_office_click` (`01_european_union_guis.txt:1932`), Europeanism −0,1, 90 Tage Sperre.
- **MD-Bug [V]:** `EU_influence_on_leader_of_foreign_policy_25_percent` (`99_EU_scripted_triggers.txt:344-364`) liest `global.EU_foreign_minister`, `global.EU_commission_president` und `global.EU_parliament_president`. Diese Variablen werden nirgends gesetzt. Die Ideas schreiben `global.euforeignaffairs`, `global.eu_commission` und `global.euparliamentpresident`. Betroffen sind die Austrittsverlängerung und der Austrittsvertrag.

### 3.10 Euro, Eurozone, OMT [V]

- Decision `EU_join_the_euro_decision` (`EU_voting_decisions.txt:1806-1878`, 100 PP): Zins < 3,5 %, Korruption ≤ 5, Wachstum, BIP/Kopf > 10.
- Effekt `joining_the_euro`: ohne Datumsriegel, siehe 2.3.
- Euro-Idea (`AA_law_expanded_economics.txt:791-830`): vor 1999 unsichtbar und gecancelt.
- Eurozonen-Reformen und Troika (`EU_voting_decisions.txt:629-774`, `EUevent.5-9`).
- OMT: `execute_OMT`/`remove_OMT` (`99_eu_scripted_effects.txt:241-288`) plus GUI (`01_european_union_guis.txt:2988ff`). Nur für `euro`-Länder.

### 3.11 Schengen [V]

**Im Kernsystem nicht vorhanden.** Das Wort taucht nur in Fokus- und Lokalisierungstexten auf, etwa `common/national_focus/05_denmark.txt:6905` `DEN_leave_schengen`. Grenz-Ideas wie `Frontex` und `European_Asylum_Agency` nutzen `border_control_multiplier_modifier` und `migration_rate_value_factor` (`EU_ideas.txt:250-268`).

### 3.12 Verteidigung ("EU-Armee") [V]

- Agenden 301-308 (3.5).
- `EU_create_EDU` (`EU_voting_decisions.txt:1303-1349`): Bedingungen `European_Security_Council` und Außenbeauftragter mit ≥ 25 % Einfluss. Wirkung:
  - Flagge `EDU`
  - **entfernt `NATO_member` bei allen Mitgliedern**
  - `create_faction_from_template = faction_template_edu`
- Frontex, EuroArmy und EuroNavy übernehmen (`:1210-1301`; OOBs `EU_frontex_basic_2000/2017`, `EU_EuroArmy_basic_2000`).
- Grenzmanöver und Gegenmanöver (`:1351-1631`; `add_named_threat`).

### 3.13 USoE, POTEF, EFS, Flaggen [V]

- **USoE (EU111):** siehe 3.5.
  - Fokusbaum `common/national_focus/01_EU_USoE_shared.txt` (90 shared focuses, Wurzel `USoE001`).
  - Decisions `common/decisions/EU_USoE_decisions.txt` (Hauptstadt, Eurosphäre, Integration, "Environmental Imperialism").
  - Ideas `EU_USoE_ideas.txt`.
  - Events `events/EU_USoE_events.txt` (Nichtangriffspakt, Bündnis).
  - Flaggen-Reset `common/decisions/MD_USoE_decisions.txt`.
- **POTEF** (President of the European Federation, EU112):
  - Flagge `european_federation`.
  - Monatliche Wahl `POTEF_election` (`99_eu_scripted_effects.txt:1024-1192`, `MD_on_actions.txt:735-747`).
  - Fokusbaum `02_EU_POTEF_shared.txt` (74 shared focuses; `allow_branch` verlangt `european_federation`; enthält `date > 2017.1.20` bei Z. 877).
  - Decisions `EU_POTEF_decisions.txt` (Wahl, Kampagne, Umweltsanktionen, Verbündete).
  - Dynamische Modifier `05_POTEF_dynamic_modifiers.txt`.
- **MD_EFS** = "European Federation of States": `common/decisions/MD_EFS_decisions.txt:1-287`. Jedes Mitglied wechselt nach Gründung der Föderation per Decision auf ein kosmetisches Tag `EFS_<TAG>` bzw. das EFS-Tag seines Formables (BLT, SCA, IBR); `special_formable_id = 102`. Nur Kosmetik.
- **1970:** Der Generic-Baum `mdcw_1970_generic_focus` enthält USoE- und POTEF-Bäume **nicht**. FRA, GER, ITA, Benelux, ENG usw. laden 1970 diesen Baum (Kap. 4.2).

### 3.14 Events und News [V]

- `events/EU_events.txt`:
  - EUvote.1-6: Popups bzw. USoE-Zustimmung
  - EUbudget.10/.11/.20/.21: minor-Popups ohne Trigger
  - EUevent.4 (Annexion), .5-.9 (Schuldenkrise/Troika/Unfallaustritt), .10 (EuroNavy), .18 (Manöver), .20 (IPA), .21 (Amt abgelaufen), .22 (**Migrationskrise**)
  - EUelection.1/.2 (`:482-517`)
  - EU_POTEF_news.1-6
- `events/EU_news.txt`: Namespace `EU_news`, `next free #57`. Alle Events `is_triggered_only`: Ämter, Austritt (20-24, 34), Beitritt (27), OMT (33), Kampagnen (35-44), EDU (47-49), Manöver (50-51), EP-Wahl (52).
- Lokalisierung: `localisation/english/MD_focus_EU_l_english.yml` (1726 Zeilen; heute 01:54 wiederhergestellt), `MD_focus_EU_POTEF_l_english.yml`, `MD_focus_EU_USoE_l_english.yml`. Durchgehend "European Union" bzw. "EU", z. B. `EU_voting_category: "The European Union"` (`:508`), `EU_apply_for_membership: "Joining the EU"` (`:1203`).

### 3.15 On-Actions [V]

| Hook | Ort | Inhalt |
|---|---|---|
| on_startup | `00_on_actions.txt:1714`, Aufruf `:1956` | `on_startup_euu_action` ohne Guard |
| on_weekly | `MD_on_actions.txt:95-97` | Seigniorage-Pool |
| on_annex | `MD_on_actions.txt:294-327` | Abstimmung abbrechen, `leaving_EU`, Monitor neu vergeben |
| on_civil_war_end | `MD_on_actions.txt:594-614` (Cold-War-Kommentar bei Z. 596; EU-Teil `:609-612` **ohne** Guard) | `EU_resync_member_array` |
| on_monthly | `MD_on_actions.txt:724-806` | GDP, POTEF, Verstöße, `EU_update_vars`, Migrationskrise (`middle_eastern_refugee_source_nations_collection` (Nahost-Länder im Krieg oder salafistisch) × 2,5 % Bevölkerung > 65, also > ca. 260 Mio. Einwohner; `common/collections/generic_collections.txt:64-75`) gibt `EUevent.22` an ein Array-Mitglied. 1970 unwahrscheinlich [?]. Dann aber `Migrant_Crisis_Europe` **ohne cancel** auf alle Array-Mitglieder (`EU_events.txt:462-479`, `EU_ideas.txt:425-435`) |

### 3.16 Ideas, Modifier, GUI, Spielregeln [V]

- **Ideas:**
  - `Organizations.txt` (Mitgliedschaft)
  - `EU_ideas.txt` (11 Ämter, 20 Gesetzes- und Krisen-Ideas, Austritt, `EUU_monitor`)
  - `EU_Council_ideas.txt` (Sanktionen)
  - `EU_POTEF_ideas.txt`, `EU_USoE_ideas.txt`
  - `AA_law_expanded_economics.txt` (euro, deutsche_mark)
- **Dynamische Modifier:** nur POTEF (`05_POTEF_dynamic_modifiers.txt`: army/navy/air/adm). `00_MD_dynamic_modifiers.txt` hat keinen EU-Bezug.
- **GUI:**
  - `interface/eu.gui` und `eu.gfx`: Original, mtime 2026-10-07.
  - Scripted GUI `common/scripted_guis/01_european_union_guis.txt` (5303 Zeilen) mit Fenstern:
    - Öffnen-Button für **jeden menschlichen Spieler** (`:4-37`)
    - Hauptfenster: Ämter, Europe-Info, Kampagnen, IPA (`:39-4155`)
    - State of the EU (`:4158`)
    - OMT-Konto (`:4187`)
    - Rat (`:4215`)
    - Parlament (`:4574`)
    - Fraktions-Detail
    - Beiträge und Verteilung
  - Scripted Localisation: `00_EU_scripted_localisation.txt`, `00_EU_parliament_scripted_localisation.txt`, `00_EU_voting_scripted_localisation.txt` (`name_of_reform` `:2`; Titel und Beschreibung je Agenden-ID `:172-868`).
- **Spielregeln:** 3.5.

---

## 4. Status im 1970-Szenario (Aufgabe 2)

### 4.1 Szenario-Erkennung [V]

- `IMP_is_1970_scenario` = `has_start_date` 31.12.1969–2.1.1970 (`common/scripted_triggers/IMP_cold_war_scenario_triggers.txt:1-4`).
- Flagge `IMP_SCENARIO_1970` wird in `00_IMP_cold_war_scenario_on_actions.txt` und in `IMP_1970_setup_global_alignment` (`IMP_1970_world_politics_effects.txt:1348-1357`) gesetzt.
- Einziges Lesezeichen: `common/bookmarks/blitzkrieg.txt` ("COLD_WAR_1970", 1970.1.1.12).
- **In keiner EU-Datei gibt es eine Abfrage dieser Trigger oder Flaggen.**

### 4.2 History: kein Durchsickern der EU-Ideas [V]

Die Dateien von FRA, GER, ITA, BEL, HOL, LUX, ENG, IRE, DEN, NRY, GRE, SPR, POR, AUS, SWI, SWE, FIN, TUR, MLT, CYP und ICE haben alle diese Struktur:
- `1970.1.1 = { if = { limit = { date < 1985.1.1 } … } … }` (Z. 4-26)
- danach `2000.1.1 = { … }`

**Alle** Einträge `EU_member`, `euro`, `EU_joined_the_eurozone` und `EU_member_opinion` liegen innerhalb des 2000er-Blocks (mit Klammer-Parser geprüft). Beispiele:
- FRA: Block 27-2776, `EU_member` Z. 1497
- GER: 28-2968 / 1445
- ITA: 26-2021 / 1172
- BEL: 25-509 / 372
- HOL: 25-1030 / 763
- LUX: 25-370 / 193
- ENG: 26-2660 / 1383

Bei einem Start 1970 wird der 2000er-Block nicht ausgeführt [V: Engine-Regel für History-Datumsblöcke]. Die 1970-Snapshots enthalten keine EU-Inhalte. **Also: 1970 hat kein Land die Idea `EU_member`, auch die Sechs nicht.**

1985 [?]: Der 1970-Block greift wegen `date < 1985.1.1` nicht, der 2000er-Block auch nicht. Damit ebenfalls keine Mitglieder (historisch wären es zehn). Auch `99_1985_starting_spirits.txt` hat keinen EU-Bezug.

### 4.3 Was am 1.1.1970 und danach passiert [V, Laufzeit nicht getestet]

| Zeitpunkt | Vorgang | Beleg |
|---|---|---|
| Start | `global.EU_member` = AUS, BEL, DEN, ENG, FIN, FRA, GER, GRE, HOL, IRE, ITA, LUX, POR, SPR, SWE, **ohne Idea** ("Geister") | `99_eu_scripted_effects.txt:760-774` |
| Start | `foreign_data_kraken` und `asylum_shopping` für alle 15 (Forschung −5 %, Stab. −5 % usw.). Wegen `cancel = NOT EU_member` vermutlich bald wieder entfernt [?] | `:777-783`, `EU_ideas.txt:206-231` |
| Start | Europeanism 2000er-Werte: POR 0,95 (Caetano), SPR 0,94 (Franco), GRE 0,92 (Junta), IRE 0,94, ENG 0,76; alle anderen in `EU_potential` 0,3 | `:810-831` |
| Start | Zufälliges KI-Land aus `EU_potential` (auch SOV, ABK usw. möglich) wird Monitor; `EUelection.2` verteilt 732 MEP auf die 15 Geister | `:794-802`, `:1582-1676` |
| Start | 53 Agenden der Jahre 2000-2020 in der Parlamentsliste | `:699-751` |
| 8.1.1970 | Mission `EU_budget_draft_preparations` läuft bei den 15 aus: Popup **EUbudget.11** an UK, SPR, POR, GRE, AUS, SWE, FIN usw. | `EU_voting_decisions.txt:435-461`, `EU_events.txt:143-156` |
| 15.1.1970 | MFF-Vorbereitung läuft aus: Popup **EUbudget.21** | `:541-567` |
| 22.1. / 29.1.1970 | Entwurf ohne EZB-Präsident wird zurückgerollt. Jahres-Timer (344 T) bzw. MFF-Timer (1237 T) starten. **Dauerschleife** mit Popups 1971, 1973 usw. | `:463-519`, `:569-625` |
| monatlich | GDP, Verstöße (u. a. "keine Wahlen +5" für Franco, Junta, Ostblock), Europeanism-Drift | `MD_on_actions.txt:724-761` |
| 14.6.1974 | `EUelection.1`: "1974 European Parliament Election" plus `EU_news.52` an alle 15 Geister. Danach 5-Jahres-Mission: **13.6.1979**, 1984, 1989 (passt zufällig zu den echten Direktwahlen!) | `99_eu_scripted_effects.txt:801`, `EU_events.txt:482-503`, `EU_voting_decisions.txt:2-17` |
| erster beendeter Bürgerkrieg | `EU_resync_member_array` leert das ganze Geister-Array | `MD_on_actions.txt:609-612`, `99_eu_scripted_effects.txt:412-429` |

### 4.4 Was Spieler 1970 sehen und tun können [V]

- **Sichtbar:**
  - EU-Button für jeden Menschen (`01_european_union_guis.txt:9-12`).
  - Ämter mit EUU-Flagge, Rat mit 15 Geistern (Liste `eu_council_voting_members_list` `:4475-4480`, Array `global.EU_member`), Parlament mit 2000er-Fraktionen.
  - Decision-Kategorien für alle 93 `EU_is_potential`-Tags (inkl. SOV) mit Budget-Missionen bei den 15.
- **Handlungsfähig:**
  - Niemand. Ämter, Parlaments- und Ratsbuttons, Budget und Art. 50 verlangen `has_idea = EU_member`.
  - Ausnahme: die EU-weite Euroskepsis-Kampagne ist für Nicht-Mitglieder offen (`:1255-1267`). SOV kann also schon heute Anti-EG-Propaganda betreiben (realistisch!).
- **Beitritt:** Nur Spanien über `SPR_1970.227` (Demokratisierungspfad). Ist Spanien die einzige "echte" Mitglied-Idea neben 14 Geistern, folgt [V aus dem Code]:
  - Spanien kann ein Amt beanspruchen (Bevölkerungsanteil > 5 % unter den Geistern).
  - Es kann Agenden einbringen.
  - **Die Geister stimmen als KI im Rat mit.** Die KI-Abstimmung prüft nur `is_ai`, nicht die Idea (`99_EU_voting_scripted_effects.txt:88-104`, Schleife `01_european_union_guis.txt:4412-4428`).
  - Gesetzes-Ideas landen bei den Geistern, werden dort aber gecancelt [?].

### 4.5 Kaputt oder anachronistisch (1970) – Liste [V, sofern nicht markiert]

1. Kein Szenario-Guard (`00_on_actions.txt:1956`, `99_eu_scripted_effects.txt:692`).
2. Array und Idea sind inkonsistent: 15 Geister statt der Sechs. `EU_european_union_currently_exists` prüft nur die Arraygröße (`99_EU_scripted_triggers.txt:1278-1283`).
3. Moderne Strafideas am Start (`:777-783`).
4. Budget-Popups und Missionen bei Nichtmitgliedern, Diktaturen und Neutralen.
5. EP 732 Sitze nach Bevölkerung statt 142 ernannter Delegierter. "Wahl" 1974 (`:1584-1642`, `:801`).
6. Agenden 2000-2020; einzige Datumssperre `date > 2002.1.1` bei 601. Keine Agenden für Den Haag 1969, Eigenmittel, Werner, EPZ, Norderweiterung, Fischerei, Regionalfonds, Direktwahl, EWS, EEA oder Maastricht.
7. Rat: 65 % Bevölkerung **und** 55 % Länder. Kein 4/4/4/2/2/1-Gewicht, keine Einstimmigkeit, kein Luxemburger Veto.
8. Beitritt ohne Votum (`EU_apply_for_membership`, `SPR_1970.227`). EDU-Automatik entfernt NATO.
9. Austritt nur nach Art. 50 (Lissabon 2009). Ein Austritt 1970 ist eigentlich nur per Vertrag möglich.
10. Haushalt: 1 % BIP, 44/44/6/6, keine GAP-Logik, **ohne EZB nicht abschließbar**.
11. Ämter: 11 Posten der 2000er. Ratsvorsitz 5 Jahre statt rotierend 6 Monate. EZB gibt es 1970 nicht.
12. Euro-Riegel im Effekt entfernt (2.3). OMT und Troika ohne Funktion.
13. Euroskepsis-Startwerte: Diktaturen am europafreundlichsten. KI-Kampagnen vor 2000 unterdrückt.
14. Wertekatalog nach heutigen Normen ("Frauen im Militär", Wahlhürde).
15. Migrationskrise kann [?] theoretisch auslösen und klebt dann (keine `cancel`).
16. Namen überall "European Union" bzw. "EU" statt "European Communities".
17. Bestehende MD-Bugs: Variablennamen der Ämter (3.9); `EU_external_sov_chi_influence_50` ist wahr, sobald SOV **kein** Mitglied ist (`99_EU_scripted_triggers.txt:16-25`), also fast immer. Das treibt KI-Austritt und blockiert die KI-Rücknahme von Art. 50. Austrittsstrafen werden gecancelt [?] (3.4).

---

## 5. Urteil pro Mechanik und Umbau (Aufgabe 4)

### 5.0 Grundsatz

- Die Mod hat **nur 1970 (und 1985) als Start** (`common/bookmarks/blitzkrieg.txt`). 2000er-Kompatibilität heißt hier nur: Inhalte bleiben spät im Spiel erreichbar.
- Empfehlung: MD-Dateien möglichst **unangetastet** lassen. Grund: zwei Rückbauten heute, und MD bleibt so aktualisierbar.
- Nur **wenige, markierte Hook-Zeilen** (`# COLDWAR`) in MD-Dateien. Die Logik gehört in neue Dateien `COLDWAR_EC_1970_*.txt`.
- Als Schalter dient `IMP_is_1970_scenario = yes` bzw. eine globale Flagge wie `COLDWAR_EC_mode`. Die Flagge erlaubt einen späteren Übergang ("Maastricht"), ab dem MD-Verhalten wieder gilt.

### 5.1 Übersicht

| Mechanik | Urteil 1970 | Konkreter Andockpunkt |
|---|---|---|
| Init `on_startup_euu_action` | **umbauen** | Am Anfang des Init-Blocks (`99_eu_scripted_effects.txt:692`) verzweigen: `if = { limit = { IMP_is_1970_scenario = yes } COLDWAR_EC_1970_initialize = yes } else = { …MD… }` |
| Idea `EU_member` und Array | **behalten** (kanonisch, 15+ Konsumenten) | Die Sechs per `add_ideas = EU_member` im neuen Init; `on_add` füllt das Array. Modifier entschärfen (5.2) |
| `EU_potential`, `EU_is_potential` | behalten, filtern | Init: Abspaltungs- und Russland-Tags nicht zuschalten bzw. `EU_potential` nur mit `exists = yes` füllen |
| Kandidat, Beitritt | **umbauen** | `EU_candidate` behalten. `EU_apply_for_membership` ersetzen durch "Antrag → Rat einstimmig → Kapitel → Unterzeichnung → Ratifikation → Beitritt". `SPR_1970.227` auf denselben Effekt umleiten |
| Austritt Art. 50 | **1970 abschalten**, neu bauen | `EU_Article_50_click_enabled` (`01_european_union_guis.txt:520`) per Hook bis Maastricht sperren. `leaving_EU` als technisches Cleanup behalten |
| Parlament (Mehrheitsvorstufe) | **umbauen** | 142 feste Sitze, beratend: die Timeout-Logik `EU_voting_decisions.txt:56-124` leitet auch ohne Mehrheit weiter, nur mit "negativer Stellungnahme" |
| Rat / QMV | **umbauen** | `EU_voting_decision_result_trigger` (`99_EU_voting_scripted_triggers.txt:16`) bekommt eine 1970-Verzweigung: gewichtete Stimmen, Einstimmigkeitsliste, Veto-Flagge |
| Agenden 101-660 | **1970 abschalten** (bis Maastricht) | Startarray `:699-751` nicht befüllen. Neue Agenden-IDs plus `apply_EU_QMV_result`-Zweige plus `name_of_reform`-Texte |
| Euroskepsis (`europeanism`) | **behalten**, neu kalibrieren | Startwerte, Drift über `europeanism_drift`-Modifier, `stop_*_campaign`-Datumsgrenze |
| Werteverstöße | umbauen (Demokratie-Klausel) | `check_breach_of_EU_value` bekommt einen 1970-Zweig. Decisions zum "Einfrieren" statt Art. 7 |
| Haushalt / MFF | **umbauen** | Rechenkern behalten (`update_EU_budget_call_rate`, `distribute_*`). EZB-Abfrage im 1970-Modus durch Ratsvorsitz ersetzen |
| Ämter | umbauen bzw. teils abschalten | Kommission, Ratsvorsitz (Rotation) und EP-Präsident behalten. EZB, Finanzminister, Frontex, Army, Navy, UN und POTEF bis zu ihren Meilensteinen |
| Euro, OMT, Troika | **1970 abschalten** | Euro-Riegel wieder in `joining_the_euro` (COLDWAR-Marker). Die Decision sperren |
| Schengen | **neu bauen** (spät, optional) | keine MD-Basis |
| EU-Armee, EDU | **1970 abschalten**; alt-historisch umbauen | `EU_create_EDU` ohne NATO-Entfernung als "EDC/WEU" |
| USoE, POTEF, EFS | **behalten als späte Endspiele**, nur hinter EG-Meilensteinen | 110 erst nach "Europäischer Union" bzw. Spinelli. `EU_drop_rival_endgame` für Fouchet gegen Föderation |
| Events und News | umbauen (Texte), Wahl-Event verschieben | `EUelection.1` auf 1979 bzw. hinter die Agenda "Direktwahlakt". Budget-Popups nur für echte Mitglieder |
| Monats-Hooks | behalten | `on_civil_war_end`-Resync ist erst nach dem Fix der Geister unschädlich |
| GUI | **behalten** (native Fenster) | Texte per Scripted Localisation umbenennen ("European Communities") |
| Spielregeln | behalten plus neue Regel | z. B. `rule_coldwar_ec` mit "historisch / alt-historisch frei / aus" |

### 5.2 Mitgliedschaft und Start 1970 (historisch)

- **Neuer Effekt `COLDWAR_EC_1970_initialize`**, aufgerufen aus dem Hook in `on_startup_euu_action`:
  1. `EU_initialized` setzen. Rules-Flaggen wie bei MD.
  2. `FRA/GER/ITA/BEL/HOL/LUX = { add_ideas = EU_member }`. `on_add` füllt das Array und setzt Europeanism 0,3 als Standard; danach überschreiben.
  3. **Europeanism 1970** als Vorschlag, zu kalibrieren: GER 0,80, ITA 0,85, BEL 0,85, HOL 0,85, LUX 0,85, FRA 0,60 (gaullistische Vorbehalte); ENG 0,45, IRE 0,60, DEN 0,55, NRY 0,45; SWE, SWI, AUS und FIN 0,35; SPR, POR und GRE 0,40, gedeckelt durch die Demokratie-Klausel; SOV 0,05.
  4. ENG, IRE, DEN und NRY erhalten `EU_candidate` (Antrag 1967, wieder aufgenommen Den Haag 1969).
  5. EP: `global.EU_Parliament_max_MEP = 142` und feste Länder-Sitze (36/36/36/14/14/6). Dazu in `election_EU_Parliament_in_member_state` (`99_eu_scripted_effects.txt:1682-1691`) ein Hook: Hat das Land die Variable `COLDWAR_EC_fixed_seats`, gilt dieser Wert statt der Rechnung über `EU_pop_ratio`. `EUelection.2` am Start bleibt; die Verteilung nach nationalen Parteistärken entspricht ungefähr den ernannten Delegationen.
  6. **Keine** `foreign_data_kraken`- oder `asylum_shopping`-Ideas, kein EUU-1625-Tage-Wahlevent (stattdessen später, siehe 5.5).
  7. Ämter: `EU_commission_president` an BEL (Rey bis 30.6.1970), danach ITA (Malfatti) per datiertem Event. `EU_council_president` als **6-Monats-Rotation** BEL → GER → FRA → ITA → LUX → HOL (historische Reihenfolge laut Bericht 1.3). Technisch: `add_timed_idea` mit 182 Tagen plus Folge-Event. Die PP-Boni (0,30 bzw. 0,15) für 1970 senken; Werte in den Ideas lassen sich nur global ändern, daher besser zusätzlicher Malus per dynamischem Modifier.
  8. Budget-Missionen nur für die Sechs. Startwerte siehe 5.6.
  9. Agenden-Array: nur 1970-Agenden (5.4).
- **Modifier der Idea `EU_member`** (`Organizations.txt:29-37`): PP-Faktor −20 % und Kriegsunterstützung −5 % sind für EG-Mitglieder 1970 zu hart, demokratische Drift ist für EG6 okay. Optionen:
  - a) Idea global ändern. Nur 1970/1985 sind spielbar, aber es ist ein MD-Eingriff.
  - b) Ausgleichs-Idea `COLDWAR_EC_community_member` für 1970.
  - **Empfehlung b)**, solange `EU_member` MD-identisch bleiben soll.
- **Andere Systeme reagieren dann automatisch** [V]: Geldsystem (Beiträge und Subventionen), Einfluss-Decisions (`Influence Decisions.txt:332ff`), NATO-Decision (`NATO.txt:645`), Formables (`formable_nation_decisions.txt:311…`). Das ist gewollt, sollte aber geprüft werden.
- **Hotfix ohne Umbau (Sofortmaßnahme):** Im 1970-Modus den Init-Block ganz überspringen und `GAME_RULE_eu_disabled` setzen. Das schaltet Button, Kategorien, Monatslogik und Geldsystem aus. Der Nachteil: Spanien-Fokus und Kampagnen sind tot. Für einen MP-Testlauf ist das besser als das Zombie-System.

### 5.3 Ministerrat 1970: Luxemburger Kompromiss statt Mehrheitsvotum

- **Datenmodell:** Länder-Variable `COLDWAR_EC_council_weight` (FRA, GER, ITA je 4; BEL, HOL je 2; LUX 1; ab EG9: 10/10/10/10/5/5/3/3/2). Globale Schwelle `COLDWAR_EC_qmv_threshold` (12/17, ab 1973 41/58).
- **Hook im Ergebnis-Trigger** `EU_voting_decision_result_trigger` (`99_EU_voting_scripted_triggers.txt:16-23`):
  ```
  if = { limit = { has_global_flag = COLDWAR_EC_mode }
      COLDWAR_EC_vote_passes = yes   # Gewichte der Ja-Länder ≥ Schwelle; bei Einstimmigkeits-Agenden: keine Nein-Stimme; keine Veto-Flagge
  } else = { …MD… }
  ```
  Ja- und Nein-Arrays (`global.EU_active_vote_supporters/rejecters`), QMV-Mission, Popups und KI-Gewichtung bleiben unverändert.
- **Rechtsgrundlage je Agenda:** Array `global.COLDWAR_EC_unanimity_votes`. Darin stehen Beitritt, Assoziation, Eigenmittel, Vertragsänderungen und EPZ.
- **Veto-Joker "Vital National Interest":** neue Decision in `EU_voting_category` (Kategorie hat bereits das richtige `allowed`).
  - Sichtbar bei `has_idea = EU_member` und laufendem Votum (`global.current_active_vote_disp > 0`).
  - Kosten: progressiv in PP (Zähler je Jahr) und Europeanism −0,03 für sich selbst.
  - Opinion-Malus bei BEL, HOL und ITA.
  - Setzt `COLDWAR_EC_vote_vetoed`, Abstimmung scheitert. Zurücksetzen in `cleanup_european_union_voting` (`99_EU_voting_scripted_effects.txt:1154`).
- **Politik des leeren Stuhls:** Decision "Boycott the Council" setzt eine globale Flagge. Ein Hook in `eu_council_available_reforms_button_click_enabled` (`01_european_union_guis.txt:4257`) blockiert dann neue Abstimmungen. Monatliche Kohäsion sinkt (neue globale Variable). Ausgang per Event-Menü.
- **Überstimmen ab 1982 bzw. EEA:** Meilenstein-Agenda setzt `COLDWAR_EC_veto_overridable`. Der Joker kostet dann mehr bzw. kann per zweitem Votum übergangen werden.
- **Ghost-Bug beheben:** Im 1970-Modus nur `has_idea = EU_member` werten. Zusätzliche Bedingung in der KI-Stimmschleife bzw. in der Bedingung `is_ai` (`99_EU_voting_scripted_effects.txt:88-104`).

### 5.4 Agenden 1970–1992 (historisch), getragen von der MD-Abstimmungsmaschine

Neue IDs am besten im Bereich 700–799; die verwaiste Zeile 703 dabei beachten. Je Agenda sind nötig:
- Eintrag ins Startarray
- Vorbedingungen im Parlaments-GUI (`:4601ff`)
- PP-Kosten (`:4989ff`)
- Zweig in `apply_EU_QMV_result` (`:316-383`)
- Text in `name_of_reform` (`00_EU_voting_scripted_localisation.txt:2`)
- Tooltip in `EU_show_display_effects_for_law` (`:1180`)
- KI-Gewichte in `EU_init_focus_vote_weights` (`:170`)

| Agenda | Historisch | Wirkung (Vorschlag) | MD-Träger |
|---|---|---|---|
| Eigenmittelbeschluss (21.4.1970) | 1971 | Umstellung Beiträge → Eigenmittel (Abrufsatz je Land vom Schlüssel auf Importe bzw. Zolleinnahmen) | `update_EU_budget_call_rate`, Abrufsatz pro Land |
| Haushaltsvertrag 1970 / 1975 | 1970/75 | EP-Rechte bei nicht-obligatorischen Ausgaben; 1975 Ablehnungsrecht | Budget-Agenden 998/999, EP-Mehrheit |
| Norderweiterung: Eröffnung (30.6.1970) | 1970-72 | ENG/IRE/DEN/NRY auf Status "in Verhandlung" (5.7) | Kandidatenflaggen-Muster aus `focus_EU601_QMV_result` |
| Gemeinsame Fischereipolitik (20.10.1970) | 1970 | Euroskepsis+ in NRY, IRE, DEN; Kapitel "Fischerei" wird härter | `EU_potential_europeanism_change` bzw. gezielter `europeanism_change` |
| Davignon / EPZ (27.10.1970) | 1970 | schaltet "Gemeinsame Erklärung" frei (Einstimmigkeit) | Ratsabstimmung plus Amt Außenbeauftragter (Idea `EU_foreign_minister`, umbenannt) |
| Werner-Plan Stufe 1 (1971) | 1971 | Idea bzw. Modifier für Stabilität und Spielraum | neue Idea; Konflikt Monetaristen gegen Ökonomisten im KI-Gewicht w1..w6 |
| Schlange (24.4.1972) | 1972 | Teilnahme: Reserve `deutsche_mark` übernehmen bzw. DM-Anker | `AA_law_expanded_economics.txt:783` `deutsche_mark` plus `00_currency_effects.txt` DEM-Emittent |
| Regionalfonds (1975) | 1975 | neuer Ausgabentopf | Ausgabenkategorie "Wachstum" (`distribute_EU_growth_exp`) |
| Europäischer Rat (1974) | 1974 | regelmäßige Gipfel-Events, Amt "Ratspräsident" mit echter Bedeutung | Idea `EU_council_president` |
| Direktwahlakt (1976) | 1979 | schaltet 5-Jahres-Wahlen frei; EP 410 Sitze | `election_EU_Parliament`, Mission `EU_election_5_years` |
| EWS/ECU (1979) | 1979 | stabilere Stufe | Währungssystem; Amt "EZB-Präsident" umdeuten zu "EMCF-Gouverneur" |
| Süderweiterung (1981/86) | 1981/86 | GRE, SPR, POR werden Kandidaten | Kandidatenflaggen-Muster |
| EEA (1986) | 1987 | mehr Mehrheitsentscheidungen: `COLDWAR_EC_veto_overridable` | |
| Maastricht (1992) | 1993 | Umbenennung in "European Union"; `COLDWAR_EC_mode` aus; MD-Agenden 101+ freischalten, Euro ab 1999 | Startarray-Logik nachträglich auffüllen; Euro-Riegel per Datum |

### 5.5 Parlament

- 1970 **beratend**. Die Mehrheitsvorstufe (`EU_parliament_focus_EUXXX_approve`) im 1970-Modus nicht als Sperre nutzen: Bei fehlender Mehrheit wird trotzdem an den Rat weitergeleitet, nur mit Flagge "EP opinion negative" und Europeanism −0,01 für die Vorschlagenden. Ort: `EU_voting_decisions.txt:72-112`.
- Die Wahl 1974 entfällt. `EUelection.1` mit `days = 3450` vom Start ergibt 13.6.1979. Besser: hinter die Agenda "Direktwahlakt" legen.
- Sitze: fest 142, dann 198 (EG9) und 410 (Direktwahl). Die Werte stehen schon im archivierten MD1970-Code (`docs/native_eu_1970/README.md`, Tabelle) und lassen sich wiederverwenden.

### 5.6 Haushalt 1970

- Kern behalten:
  - `set_EU_gdp`, `update_EU_budget_call_rate`, `distribute_*`, `EU_budget_total_gain`
  - Geldbuchung `00_money_system.txt:1032-1043`, `4012-4015`
- **Startwerte zu kalibrieren:** Abrufsatz je Land nach Beitragsschlüssel 1970. Haushaltsgröße grob 0,5–0,8 % BIP der Sechs [?, laut Bericht unsicher; zu prüfen].
- Aufteilung: Agrar 80–85 %, Wachstum (Sozialfonds/EIB) 5 %, Global (EEF/Assoziierte) 5 %, Verwaltung 5 %. Ort: `set_EU_expenditure` per Hook.
- **GAP-Verteilung** nach Agrarleistung statt BIP/Kopf-Stufe. Kandidat ist die Variable `weekly_harvest_billion` aus dem MD-Agrarsystem (`00_money_system.txt:1029`, Definition nicht gestagt [?]).
- **EZB-Riegel lösen:** In `EU_budget_draft_ongoing` und `EU_mff_draft_ongoing` (`EU_voting_decisions.txt:476, 495, 582, 601`) und in den Fiskal-Buttons (`01_european_union_guis.txt:1340ff`) im 1970-Modus `EU_council_president` statt `ECB_president` prüfen.
- Ereignisse:
  - jährliche **Agrarpreisrunde** ("Marathon") als Ratsabstimmung, die `global.EU_natural_exp_ratio` erhöht oder einfriert
  - Netto-Positionen (`EU_budget_net` gibt es schon, `99_eu_scripted_effects.txt:1547`) speisen die Euroskepsis
  - später ein Rabatt-Votum

### 5.7 Erweiterung und Beitritt (historisch und MP-tauglich)

**Kette** (alle Schritte als Decisions oder Ratsabstimmungen):
1. `EU_candidate` (vorhanden).
2. Ratsbeschluss "Verhandlungen eröffnen" (Einstimmigkeit, **Gaullistisches Veto möglich**).
3. Kapitel als Decisions des Kandidaten mit Optionen hart, mittel, weich, z. B. Übergangszeit, GAP, Commonwealth-Zucker/NZ-Butter, Fischerei, Beitrag. Jedes Mitglied kann ein Kapitel blockieren (Veto-Decision).
4. Unterzeichnung (Ratsabstimmung, einstimmig).
5. Ratifikation: Referendum-Event im Kandidatenland. Die Wahrscheinlichkeit kommt aus `party_pop_array` und Kapitel-Flaggen; die MD-Parteiarrays werden schon in `election_EU_Parliament_in_member_state` genutzt.
6. Beitritt zum Datum X: `add_ideas = EU_member` (füllt Array, `EU_adopt_passed_laws`), `EU_news.27`.

**Erhalten bzw. entfernen**
- `EU_former_member` und Cooldown bleiben.
- `EU_apply_for_membership` wird im 1970-Modus ausgeblendet. Die EDU/NATO-Automatik (`EU_voting_decisions.txt:1687-1711`) wird **nicht** übernommen.
- `SPR_1970.227` auf den Beitrittseffekt umstellen (Abstimmung statt Direktvergabe).

**KI-Defaults (Geschichte):** FRA hebt das Veto auf; NRY-Referendum knapp Nein (46,5 %); ENG, IRE und DEN treten am 1.1.1973 bei.

### 5.8 Austritt 1970

- "Renegotiate Terms" (Kapitel neu öffnen), dann Referendum (ENG 1975), bei Nein Austrittsvertrag (einstimmig), dann `leaving_EU`.
- Teil-Austritt nach Grönland-Muster als Sonder-Event.
- Art. 50 bis Maastricht/Lissabon per Hook sperren. Die `cancel`-Bedingung der Austritts-Ideas korrigieren, da diese sonst wirkungslos bleiben [?].

### 5.9 Euroskeptizismus 1970

- Behalten: Variable, Effekte, Trigger und Kampagnen.
- **Neu: Quellen als Drift.** Dynamische Modifier mit `europeanism_drift` für Bauernproteste, Fischerei, Gaullisten, Labour-Linke und Neutralität. Sie wirken über `EU_update_vars` (`99_eu_scripted_effects.txt:100-109`). Wichtig: Die Drift wirkt nur auf `EU_potential`, also Mitglieder und Kandidaten; das ist passend.
- `stop_pro_european_campaign` und `stop_euroscepticism_campaign`: das Datum 2000.01.15 per Hook für den 1970-Modus aufheben (`99_EU_scripted_triggers.txt:621, 640`).
- SOV-Kampagne (EU-weite Euroskepsis) ist schon heute für Nicht-Mitglieder offen. Die KI-Bremse `date > 2004.1.1` (`01_european_union_guis.txt:3699`) für SOV im 1970-Modus lösen.

### 5.10 Demokratie-Klausel statt Art. 7

- `check_breach_of_EU_value` im 1970-Modus: keine Wahlen, Diktatur, Putsch, Untertan. Ohne "Frauen im Militär" und ohne Wahlhürde.
- Andockpunkte:
  - **Griechenland** hat schon `COLDWAR_GRE_1970_european_censure` (`common/scripted_effects/COLDWAR_GRE_1970_tree_effects.txt:18409`, wird bei `:15064` entfernt). Das ist der Status "Assoziation eingefroren".
  - **Spanien:** `SPR_1970_apply_to_the_european_communities` verlangt Demokratie (`spain_1970.txt:1241-1260`).
- Decision "Assoziation einfrieren" bzw. "reaktivieren" auf Basis der vorhandenen Werte-Decisions (`EU_voting_decisions.txt:127-378`), umbenannt.

### 5.11 Währung: Werner statt Euro

- Euro und OMT sperren: COLDWAR-Riegel in `joining_the_euro` wieder einsetzen (Text aus `docs/native_eu_1970/native_before_extension.zip`, Datei `common/scripted_effects/99_eu_scripted_effects.txt`, Z. 1830ff). `EU_join_the_euro_decision` im 1970-Modus ausblenden.
- Stufen: W1 Werner (Idea), W2 Schlange (Bindung an die DM über die `deutsche_mark`-Reserve-Idea und den DEM-Emittenten), W3 EWS/ECU, W5 Euro.
- **Alt-historisch "Werner gelingt":** Die `cancel`/`visible`-Bedingung der Euro-Idea erweitern um `OR = { date > 1998.12.31 has_global_flag = COLDWAR_EC_single_currency }`. Die Euro-Idea liegt in `AA_law_expanded_economics.txt`, einer Cold-War-geänderten Datei. Dazu das EZB-Amt freischalten.

### 5.12 Verteidigung

- 301-308 und EDU im 1970-Modus aus.
- **Alt-historisch "WEU-Reaktivierung / EVG-Revival":** `EU_create_EDU` als Vorlage (`faction_template_edu`, Mitgliederschleife). **Aber** NATO-Entfernung nur bei einer bewussten Entscheidung pro Land (MP-Konsens). Starke SOV-Reaktion über das Cold-War-Spannungssystem.
- `EU_military_exercise` ist als "WEU-Manöver" wiederverwendbar (`EU_voting_decisions.txt:1351-1631`).
- Nuklear: EU308 (`nuclear_power_def`) nur über "europäisierte Force de frappe" und Zustimmung von FRA/ENG.
- Neutrale (IRE, AUS, SWE, FIN) ausnehmen.

### 5.13 Föderationspfad und Endspiele

- **Föderalistisch (Spinelli):** 110 → 111 (USoE) behalten, Voraussetzung aber "Europäische Union" plus Kohäsion. Die MP-Zustimmung ist über `EUvote.5` schon da (Ablehnen heißt Austritt).
- **Gaullistisch "Union der Staaten" (Fouchet):** neue Agenda als Rivale. `EU_drop_rival_endgame` (`99_EU_voting_scripted_effects.txt:385-403`) sperrt den Föderationspfad.
- **POTEF und EFS** (112): behalten als föderales Endspiel ohne Annexion. EFS-Flaggen bleiben Kosmetik.

### 5.14 Weitere alt-historische Ideen und ihre MD-Träger

| Idee | MD-Träger |
|---|---|
| Gaullistisches drittes Veto gegen UK | Ratsabstimmung "Verhandlungen eröffnen" (Einstimmigkeit) plus Veto-Decision (5.3) |
| Norwegen sagt Ja | Referendum-Event, Parteiarrays (5.7) |
| UK-Austritt 1975 | Neuverhandlung, Referendum, `leaving_EU` (5.8) |
| EFTA-EG-Großfreihandel | Agenda 609 "EFTA & Microstates" (vorhanden) umdatieren bzw. kopieren |
| Frühe Süderweiterung | Kandidatenflaggen plus Demokratie-Klausel; SPR-1970-Fokuskette |
| Türkei-Mitgliedschaft | Agenda 606 (vorhanden) umdatieren; Assoziation von 1963 als Startstatus |
| EG-Zerfall (leerer Stuhl) | Boykott-Decision plus `leaving_EU` in Serie |
| Neutralen-Block, Ostannäherung (ROM/HUN) | Trigger `EU_external_sov_influence_15/10/5` (vorhanden): SOV-Einfluss sperrt; Antrag löst ein SOV-Event aus |
| Butter für die UdSSR (1973) | Agrar-Topf (`global.EU_natural_exp_total`) plus Event mit SOV-Handel |
| DDR als "heimliches 7. Mitglied" | dynamischer Handelsbonus DDR–GER; DDR fehlt bewusst in `all_eu_available_countries` |
| Frühe Wiedervereinigung in der EG | `on_annex` (`MD_on_actions.txt:294`) annektiert Gebiet ohne Statusbruch; Rats-Event zu Übergangsregeln |
| Dritte Kraft zwischen den Blöcken | EPZ-Erklärungen zählen; Kopplung an das Cold-War-Blocksystem (Andockpunkt außerhalb dieser Prüfung) |

### 5.15 Empfohlene Reihenfolge

1. **Sofort (1 Hook):** 1970-Guard in `on_startup_euu_action` (Init überspringen oder `COLDWAR_EC_1970_initialize`). Euro-Riegel wieder einsetzen. Beides mit `# COLDWAR`.
2. **Minimal spielbare EG:** Sechs Mitglieder, 142 Sitze, Ratsgewichte plus Veto, Rotation des Vorsitzes, EZB-Ersatz im Haushalt, 3–5 Agenden (Eigenmittel, Eröffnung Norderweiterung, EPZ, Werner).
3. Beitrittskette und Referenden. Dann Fischerei und GAP-Runde.
4. Währungsstufen, Regionalfonds, Direktwahl, Süderweiterung.
5. Maastricht-Übergang zurück auf MD, danach alt-historische Endspiele.

**Vor der Umsetzung** mit dem Nutzer klären, warum CWEC und MD1970_EU verworfen wurden (Kap. 2.1).

---

## Anhang A: Zusätzlich gestagte Dateien (dieser Agent)

- `docs/europe_1970_audit/`: `agent_core.md`, `agent_paths.md`, `agent_voting_ui.md`, `einbauplan_1970.md`, `europa_1970_konzept.md`, `implementation.md`, `native_restore.md`, `native_restore_report.json`, `original_md_compatibility.md`, `original_md_reference_manifest.json`, `native_eu_restore_backup_20261018T011628Z.zip`
- `docs/main_md_eu_restore/`: `README.md`, `restore_report.json`, `removed_eu_adaptation_20261018T015402Z.zip`
- `docs/native_eu_1970/`: `README.md`, `baseline.json`, `validation_report.json`, `native_before_extension.zip`
- `common/scripted_triggers/`: `99_EU_scripted_triggers.txt`, `99_EU_voting_scripted_triggers.txt`, `IMP_cold_war_scenario_triggers.txt`, `mdcw_cold_war_triggers.txt`, `00_game_rule_triggers.txt`, `MD_Country_Groups_Triggers.txt`, `01_international_triggers.txt`
- `common/scripted_guis/01_european_union_guis.txt`
- `common/scripted_localisation/`: `00_EU_parliament_scripted_localisation.txt`, `00_EU_scripted_localisation.txt`, `00_EU_voting_scripted_localisation.txt`, `mdcw_historical_currency_scripted_localisation.txt`, `mdcw_cold_war_scripted_localisation.txt`, `01_organizations_scripted_localisation.txt`
- `common/ideas/`: `Organizations.txt`, `EU_ideas.txt`, `EU_Council_ideas.txt`, `EU_POTEF_ideas.txt`, `EU_USoE_ideas.txt`, `AA_law_expanded_economics.txt`, `mdcw_cold_war_ideas.txt`, `99_1985_starting_spirits.txt`
- `common/on_actions/`: `00_on_actions.txt`, `MD_on_actions.txt`, `00_IMP_cold_war_scenario_on_actions.txt`, `99_IMP_1970_world_on_actions.txt`, `mdcw_cold_war_on_actions.txt`, `999_game_rules_on_actions.txt`, `99_IMP_1985_eastern_bloc_on_actions.txt`, `zzzzzz_mdcw_imperia_globalism_on_actions.txt`, `_documentation.md`
- `common/game_rules/00_game_rules.txt`, `common/collections/collections.txt`, `common/collections/generic_collections.txt`, `common/script_constants/country_groups.txt`, `common/bookmarks/blitzkrieg.txt`
- `common/dynamic_modifiers/05_POTEF_dynamic_modifiers.txt`, `common/dynamic_modifiers/00_MD_dynamic_modifiers.txt`
- `common/opinion_modifiers/Organization Opinions Modifiers.txt`, `common/opinion_modifiers/EU_POTEF.txt`
- `common/scripted_effects/`: `00_money_system.txt`, `00_currency_effects.txt`, `01_international_systems_effects.txt`, `01_NATO_effects.txt`, `mdcw_imperia_globalism_effects.txt`, `COLDWAR_GRE_1970_tree_effects.txt`, `COLDWAR_GRE_1970_regional_effects.txt`, `COLDWAR_TUR_1970_regional_effects.txt`, `COLDWAR_CYP_1970_effects.txt`, `SPR_1970_scripted_effects.txt`, `COLDWAR_SOV_1970_scripted_effects.txt`
- `common/decisions/categories/different_country_flags.txt`, `common/decisions/categories/mdcw_cold_war_decision_categories.txt`
- `history/countries/` (35 Dateien): FRA, GER, ITA, BEL, HOL, LUX, ENG, IRE, DEN, NRY, GRE, SPR, POR, AUS, SWI, SWE, FIN, TUR, EUU, MLT, CYP, ICE, DDR, SLO, CZE, EST, SLV, CRO, HUN, POL, LIT, LAT, ROM, BUL, ABK
- `localisation/english/`: `MD_focus_EU_l_english.yml`, `countries_l_english.yml`, `IMP_1970_country_and_party_names_l_english.yml`
- `events/`: `SPR_1970_events.txt`, `NATO_system.txt`, `mdcw_cold_war_events.txt`, `COLDWAR_GRE_1970_tree_events.txt`, `COLDWAR_SOV_1970_events.txt`, `COLDWAR_CYP_1970_events.txt`
- `README.md`, `Changelog.txt`

Zur Analyse entpackt (Scratchpad, nur lesend): `scratchpad/zip_md1970/`, `scratchpad/zip_native/`.

## Anhang B: Nicht geprüft bzw. offen

- Laufzeitverhalten: Popups, `cancel` von Ideas, Ladereihenfolge der `on_startup`-Dateien. Für Guards daher `IMP_is_1970_scenario` statt der Flagge verwenden.
- Herkunft von `weekly_harvest_billion`, `EU_map_mode`, `faction_template_edu`, `EU_Tech_Share`.
- Nicht gestagte Fokus-, Event- und Decision-Dateien auf weitere `EU_member`-Konsumenten.
- Ob ein 1985-Start real angeboten wird (`common/bookmarks/the_gathering_storm.txt` nicht gelesen).
