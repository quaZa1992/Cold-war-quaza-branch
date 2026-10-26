# Agent B: EU-System der neuesten Millennium-Dawn-Version als Referenz für die EG 1970

**Stand:** 18.10.2026. Nur gelesen, auf dem PC wurde nichts verändert (kein `device_commit_files`).
**Referenz (MD-Wurzel):** `E:\SteamLibrary\steamapps\workshop\content\394360\2777392649`. Alle Pfade unten sind relativ zu dieser Wurzel, sofern nichts anderes steht.
**Vergleichsstände:**
- **MD-neu** = Workshop-Version 2.0.2 (oben).
- **Mod-aktuell** = `C:\Users\Enes\Documents\Paradox Interactive\Hearts of Iron IV\mod\mdcoldwar`.
- **Alt-Basis** = Sicherung `E:\MDColdWar_Backups\mdcoldwar_2026-10-08_before_md_2_0_2_migration\mod` (Stand vor der Migration, HOI4 1.18). Der Ordner wurde nur lesend freigegeben.

**Legende**
- **[V] verifiziert:** im Code bzw. per Byte-Vergleich nachgeprüft.
- **[A] vermutet:** abgeleitet, aber nicht im Spiel getestet oder nicht vollständig nachverfolgt.
- **Aufwand:** klein = nur Daten, Startwerte, Arrays oder Loc (≤ 1 Tag); mittel = neue Effekte, Decisions oder Events im bestehenden Gerüst (2–5 Tage); groß = neues Subsystem oder GUI-Ausbau (> 1 Woche).

---

## 0. Kurzfazit

1. **Die Prämisse des Auftrags ist überholt [V].** Die Mod basiert nicht mehr auf MD 1.12.3B für HOI4 1.18. Sie wurde auf **MD 2.0.2 für HOI4 1.19.\*** migriert:
   - Mod-`descriptor.mod`: `version="2.0.2"`, `supported_version="1.19.*"`.
   - Mod-`README.md`: "Cold War / Imperia content migrated to the Millennium Dawn 2.0.2 base for Hearts of Iron IV 1.19.*".
   - Mod-`Changelog.txt` ist byte-identisch mit dem MD-2.0.2-Changelog.
   - Die Alt-Basis (`descriptor.mod`: `version="1.18*"`, `supported_version="1.18.*"`) liegt nur noch als Sicherung vor.
2. **Das EU-System der Mod ist heute byte-identisch mit MD 2.0.2 [V].** Gilt für 31 EU-Dateien (Liste in 4.1), darunter GUI, Scripted GUI, Effekte, Trigger, Decisions, Events, Ideas, Fokusbäume und Lokalisierung. Grund: Am 18.10.2026 wurden zwei eigene Umbauten (CWEC und MD1970_EU) auf Wunsch des Nutzers entfernt und das native System wiederhergestellt (Mod-`docs/main_md_eu_restore/README.md`, `restore_report.json`).
   - **Ein "Delta Mod gegen MD-neu" gibt es für die EU-Kerndateien also nicht.**
   - Abweichungen gibt es nur in angrenzenden Dateien, z. B. die D-Mark als Reservewährung in `00_currency_effects.txt` und Cold-War-Schutzweichen in `MD_on_actions.txt`.
   - Abschnitt 4 vergleicht deshalb **Alt-Basis (1.18) gegen MD 2.0.2**, also den Stand, den das Team bis 8.10.2026 kannte.
3. **Das native System startet 1970 im modernen Zustand [V Code, A Laufzeit].** `on_startup_euu_action` läuft in der Mod ohne Datumsprüfung (Mod-`common/on_actions/00_on_actions.txt:1956`).
   - Die 15 Mitglieder von 2000 (AUS, FIN, SWE, ENG, DEN, IRE, GRE, POR, SPR usw.) werden ins Array `global.EU_member` geschrieben (`common/scripted_effects/99_eu_scripted_effects.txt:760-774`).
   - Die Idee `EU_member` steht in der Mod-History aber nur in den `2000.1.1`-Blöcken (z. B. Mod-`history/countries/FRA - France.txt:1497` in `2000.1.1`).
   - Ergebnis: 1970 sind Array und Idee inkonsistent, die Sechs sind keine Mitglieder, und 15 Staaten bekommen moderne Strafideen (`foreign_data_kraken`, `asylum_shopping`).
4. Das MD-EU-System ist ein **datengetriebenes Gerüst**:
   - Agenden haben numerische IDs: `global.EU_potential_votes` → `global.EU_council_votes` → `global.EU_passed_votes`.
   - Die KI-Gewichte stehen in einer Tabelle (`EU_init_focus_vote_weights`).
   - Ergebnisse laufen über einen Dispatcher (`apply_EU_QMV_result`).
   - Für 1970 lässt sich vieles durch **neue IDs, neue Startwerte und Lokalisierung** erreichen, ohne die GUI neu zu bauen.
5. **Blocker für 1970 im nativen Code [V]:**
   - Haushalts- und MFF-Entwürfe erreichen das Parlament nur, wenn ein Mitglied **ECB-Präsident** ist. Dieses Amt erfordert die Idee `euro`.
   - Ratspräsident und Parlamentspräsident erfordern `treaty_of_lisbon`.
   - Für ENG/IRE/DEN gibt es **keinen** Kandidatenpfad.
   - Das Parlament hat 732 Sitze nach Bevölkerung statt 142 ernannter Sitze.
   - Die erste EP-Wahl fiele auf Juni 1974.

---

## 1. Version, Changelogs, Docs, "Claude outputs"

| Quelle | Befund | Status |
|---|---|---|
| `descriptor.mod` | `version="2.0.2"`, `supported_version="1.19.*"`, `remote_file_id="2777392649"`. `replace_path` u. a. für `common/scripted_effects`, `common/decisions`, `common/ideas`, `common/national_focus`, `common/factions/*`, `common/doctrines/*` | [V] |
| `Changelog.txt` | v2.0.2: Inflation, Policy-Rate, Bugfixes. **Kein EU-Eintrag.** Verweist auf `docs/src/content/changelogSections/v2-0-changes.md` im Git-Repo; dieser Ordner wird im Workshop nicht ausgeliefert | [V] |
| `docs/` | existiert in der MD-Wurzel nicht | [V] |
| `Claude outputs/` | enthält nur `COLDWAR_EGY_1970_layout_preview.png` und `COLDWAR_EGY_1970_nationalist_preview.png`. **Keine EU-Analysen** | [V] |
| Dokumentation im Code | `common/on_actions/_documentation.md`, `common/collections/_documentation.md`, `common/factions/_documentation.md`, `common/script_constants/documentation.md`, `common/map_modes/documentation.txt`, `common/scripted_guis/README.md` (nicht EU-spezifisch, nicht gelesen) | [V] |
| Mod-Doku zur EU | Mod-`docs/europe_1970_audit/*`, `docs/native_eu_1970/README.md` und `docs/main_md_eu_restore/README.md` beschreiben die entfernten Umbauten CWEC und MD1970_EU und die Wiederherstellung | [V] |

---

## 2. Datei-Inventar EU (MD 2.0.2)

| Datei | Zeilen | Rolle |
|---|---:|---|
| `common/scripted_effects/99_eu_scripted_effects.txt` | 2092 | Kern: Europeanism, Mitgliedschaft und Austritt, Ämter, Startup, Parlament, Haushalt, Euro, OMT, Werteverstöße, USoE-Helfer |
| `common/scripted_effects/99_EU_voting_scripted_effects.txt` | 1464 | KI-Abstimmungsgewichte, QMV-Dispatcher, Ergebnis-Handler je Agenda, Aufräumen nach Abstimmungen |
| `common/scripted_triggers/99_EU_scripted_triggers.txt` | 1290 | Einfluss von außen (SOV/CHI), Amtsbedingungen, Seiten-Trigger der GUI, Kandidatenliste, POTEF-Regionen |
| `common/scripted_triggers/99_EU_voting_scripted_triggers.txt` | 525 | QMV-Ergebnis, `focus_EUxxx_accepted` |
| `common/decisions/EU_voting_decisions.txt` | 1908 | Missionen für Parlament, Rat, Haushalt und MFF; Werteverstöße; Eurozone und Troika; Austritt; Verteidigung; Beitritt; Euro-Beitritt; IPA |
| `common/decisions/EU_USoE_decisions.txt` | 742 | Decisions der USoE (Hauptstadt, "Westernize", Eurosphere, Umwelt-Imperialismus) |
| `common/decisions/EU_POTEF_decisions.txt` | 628 | Wahl des Präsidenten der Föderation (POTEF), Umwelt-Imperialismus, Verbündete rufen |
| `common/decisions/MD_EFS_decisions.txt`, `MD_USoE_decisions.txt` | 287 / 67 | Kosmetische Flaggen (EFS_*, USoE-Reset) |
| `common/decisions/categories/EU_voting_categories.txt` | 82 | 7 Kategorien |
| `common/ideas/Organizations.txt` | 255 | `EU_member` (Z. 4-38) |
| `common/ideas/EU_ideas.txt` | 445 | 11 Ämter, Rechtsakte, Krisen- und Hilfsideen |
| `common/ideas/EU_Council_ideas.txt` | 26 | Sanktionsideen: `EUU_voting_rights_suspended`, `EUU_subsidies_suspended` |
| `common/ideas/EU_POTEF_ideas.txt`, `EU_USoE_ideas.txt` | 445 / 122 | Endgame-Ideen |
| `common/ideas/AA_law_expanded_economics.txt:674ff, 769` | – | Reservewährungs-Gesetz inkl. `euro` |
| `common/dynamic_modifiers/05_POTEF_dynamic_modifiers.txt` | 72 | variablengetriebene POTEF-Boni |
| `common/modifier_definitions/modifier_definitions.txt:95` | – | eigener Modifier `europeanism_drift` |
| `common/scripted_guis/01_european_union_guis.txt` | 5303 | Komplette EU-GUI-Logik inkl. KI-Gewichte |
| `interface/eu.gui` / `interface/eu.gfx` | 2325 / 39 | Fenster |
| `common/scripted_localisation/00_EU_parliament_scripted_localisation.txt` | 493 | Namen und Icons der 24 Fraktionen, mit Datumsweichen |
| `common/scripted_localisation/00_EU_scripted_localisation.txt` | 446 | Titel der Nebenanzeigen, POTEF-Umfragen |
| `common/scripted_localisation/00_EU_voting_scripted_localisation.txt` | 1036 | Namen und Status der Agenden |
| `events/EU_events.txt`, `EU_news.txt`, `EU_USoE_events.txt` | 569 / 459 / 218 | 27 + 40 + 7 Events |
| `common/national_focus/01_EU_USoE_shared.txt` | 3919 | 90 `shared_focus` (USoE) |
| `common/national_focus/02_EU_POTEF_shared.txt` | 7668 | 74 `shared_focus` (POTEF) |
| `localisation/english/MD_focus_EU_l_english.yml` (+ `_POTEF`, `_USoE`) | 1726 / 399 / 515 | EN-Lokalisierung |
| `common/map_modes/EU_map_mode.txt` | – | Kartenmodus der Ämter |
| `common/collections/collections.txt:3-17` | – | `eu_potential_countries_collection`, `eu_members_collection` |
| `common/script_constants/country_groups.txt` | – | `all_eu_available_countries` (94 Tags) |
| `common/factions/templates/00_EU.txt` | – | Templates `faction_template_fep`, `_edu`, `_eurasian_alliance`, `_western_alliance` |
| `common/game_rules/00_game_rules.txt:299-383` | – | 4 EU-Regeln |
| Einhängepunkte | – | `common/on_actions/00_on_actions.txt:1929`; `common/on_actions/MD_on_actions.txt:295-326, 607, 720-757`; `common/scripted_effects/00_money_system.txt:996-1007, 3967-3970`; `common/scripted_effects/00_currency_effects.txt:448ff` |

---

## 3. Feature-Inventar (MD 2.0.2, identisch mit Mod-aktuell)

### 3.1 Mitgliedschaft, Beitritt, Austritt
- **Kanonisch [V]:**
  - Idee `EU_member` (`common/ideas/Organizations.txt:4-38`). `on_add` schreibt in `global.EU_member`, setzt einen Europeanism-Standardwert und übernimmt beschlossene Rechtsakte (`EU_adopt_passed_laws`, `99_eu_scripted_effects.txt:1917`). `on_remove` ruft `leaving_EU` auf.
  - Modifier der Mitgliedschaft: `democratic_drift 0.05`, `neutrality_drift 0.03`, `political_power_factor -0.2`, `trade_opinion_factor 0.15`, `stability_factor 0.05`, `consumer_goods_factor -0.05`.
  - Die alte `allowed`-Liste mit 35 Tags ist entfallen. Ersatz ist die Konstante `all_eu_available_countries` (`common/script_constants/country_groups.txt`). Sie enthält **kein DDR** [V].
- **Beitritt [V]:** `EU_apply_for_membership` (`common/decisions/EU_voting_decisions.txt:1635`), Kosten 50 PP. Bedingungen:
  - Werteverstoß-Wert unter 3,
  - Flag `EU_candidate` oder abgelaufener Wiederbeitritts-Cooldown,
  - kein Krieg,
  - SOV- oder CHI-Einfluss unter 15 %,
  - Europeanism über 0,79 (Mensch) bzw. über 0,69 (KI).
  - Bei aktiver EDU entfernt der Beitritt `NATO_member` (Z. 1688-1693).
- **Kandidatenstatus [V]:** Nur über erfolgreiche Erweiterungsagenden (`focus_EU601…660_QMV_result`, `99_EU_voting_scripted_effects.txt:887-1088`). Diese setzen `EU_candidate` und heben Europeanism auf mindestens 0,5 an (`set_eu_candidate_europeanism_floor`, `99_eu_scripted_effects.txt:199`).
- **Austritt [V]:**
  - Auslöser ist der GUI-Klick `EU_Article_50_click` (`common/scripted_guis/01_european_union_guis.txt:1789`). Er startet die Mission `EU_exit` (730 Tage) und räumt alle Ämter.
  - Decisions: `EU_Revoke_Article_50`, `EU_extend_Article_50` (+90 Tage), `EU_withdrawal_treaty`, `EU_prepared_no_deal_exit` (`EU_voting_decisions.txt:777-1207`).
  - No-Deal-Strafe `no_deal_exit`: 1825 bzw. 730 Tage.
  - `leaving_EU` (`99_eu_scripted_effects.txt:343`) entfernt Euro und alle Rechtsakte, räumt Ämter (`EU_vacate_offices`, Z. 294) und Missionen, verlässt die EDU und setzt `EU_former_member` mit **1095 Tagen Wiederbeitritts-Cooldown** (Z. 349-352).
- **Bürgerkrieg [V]:** `EU_resync_member_array` (Z. 412) bereinigt das Array nach `on_civil_war_end` (`MD_on_actions.txt:607`).

### 3.2 Kandidatenprozess, Heranführungshilfe, Werteprüfung
- **IPA [V]:** Der GUI-Knopf `approve_IPA_button_click` (`01_european_union_guis.txt:2406`) steht nur Inhabern der Ämter Kommission, Rat, Hoher Vertreter, Parlament oder Finanzminister zur Verfügung.
  - Wirkung für alle Kandidaten: `EU_pre_accession_assistance` für 180 Tage (`EU_ideas.txt:310`: PP +25 %, Steuerertrag +15 %, Korruptionskosten −75 %, `europeanism_drift` +0,02) und Mission `pre_accession_assistance_program` (+400 PP bei niedriger Korruption).
  - **Fehler [V]:** `days_mission_timeout = 5 #180` (`EU_voting_decisions.txt:1892`).
- **Verhandlungskapitel:** **nicht vorhanden** [V]. Es gibt nur "Kandidat-Flag → Antrag → sofortiger Beitritt".
- **Werteverstoß-Wert [V]:** `check_breach_of_EU_value` (`99_eu_scripted_effects.txt:435`), wöchentlich für alle potenziellen Mitglieder (`MD_on_actions.txt:745-753`). Punkte:
  - Korruption 1-5,
  - Angriffskrieg gegen ein Mitglied +10,
  - Kommunisten bzw. Reaktionäre in der Koalition +1, an der Regierung +2,
  - keine Wahlen +5,
  - Diktatur-Idee +5,
  - Subjekt +4,
  - Sperrklausel über 9,5 % +1,
  - Staatsbankrott +1.
- **Ratsmaßnahmen [V]:** `EU_council_determine_serious_breach…`, `…suspend_voting_rights`, `…suspend_subsidies` und Rücknahmen, je 100 PP (`EU_voting_decisions.txt:127-378`). Die Befugnis liegt bei der Top-3-Einfluss-Mehrheit oder beim Kommissionspräsidenten (`EU_council_has_breach_authority`, `99_EU_scripted_triggers.txt:388`).

### 3.3 Abstimmungen (Parlament → Rat)
- **Pipeline [V]:** Agenden sind Zahlen.
  - Start-Katalog: 53 IDs (`99_eu_scripted_effects.txt:699-751`) für Verträge 101-105, Euro und Fiskal 201-208, Verteidigung 301-308, Migration und Digitales 401-408, Erweiterung 601-660 sowie Endgame 110-112.
- **Parlament [V]:**
  - Vorschlag aus `eu_parliament_available_reforms_list` (`01_european_union_guis.txt:4989`), Kosten 200 bzw. 300 PP.
  - Voraussetzungen: ein Kommissionspräsident existiert (oder es gibt weniger als 2 Mitglieder), keine laufende Agenda, kein Haushaltsentwurf, Einfluss von außen unter 15 %. Hinzu kommen Agenda-Ketten (z. B. 102 erst nach 101, Z. 4601ff).
  - Die Fraktion der eigenen Regierungspartei unterstützt automatisch. Weitere Fraktionen kauft man per `PG_party_X_influence_click`: **2 PP je MEP** (Z. 2025ff).
  - Mehrheit: `global.MEP_Majority` = 50 % + 1.
  - Mission `EU_parliament_focus_EUXXX_approve` (14 Tage, `EU_voting_decisions.txt:22`). Abschluss nur durch den Kommissionspräsidenten oder einen menschlichen Platzhalter (`EU_is_commission_caretaker`, `99_EU_scripted_triggers.txt:377`).
- **Rat [V]:**
  - Vorschlag aus `global.EU_council_votes` (`01_european_union_guis.txt:4382`). Kosten 500 PP, außer für Amtsinhaber oder wer mindestens 3 % Einfluss auf alle anderen hat.
  - Menschen erhalten das Event `EUvote.2` bzw. `EUvote.5`; KI-Stimmen werden sofort berechnet.
  - Menschen stimmen per GUI ab (Z. 2638/2657). Stimmen anderer lassen sich gegen PP kippen: 300 × Bevölkerungsanteil × 25 (Z. 4435).
  - **QMV:** Ja-Bevölkerungsanteil über 65 % **und** Unterstützer/Mitglieder über 55 % (`99_EU_voting_scripted_triggers.txt:16-23`). **Enthaltung zählt damit als Nein.**
  - Ergebnis nach 14 Tagen (`EU_voting_decisions.txt:385`), angewendet durch den Kommissionspräsidenten. Das globale Ergebnis wird **einmal** angewendet, nicht pro Mitglied.
- **Veto, Einstimmigkeit, Ratspräsidentschaft:** gibt es **nicht** [V]. Auch das USoE-Endgame (111) läuft per QMV. Ablehner verlieren dabei vorher die Mitgliedschaft (`99_EU_voting_scripted_effects.txt:406-410`).
- **Cooldowns [V]:** Game-Rule `rule_european_union_voting_limits` mit 1/60/90/120 (Standard)/180/210 Tagen (`00_game_rules.txt:315`). Umgesetzt in `set_the_eu_parliament_delay` und `set_the_eu_council_delay` (`99_eu_scripted_effects.txt:881/958`).

### 3.4 Institutionen und Ämter
- **11 Ämter als Ideen [V]** (`EU_ideas.txt:4-197`; `on_add` setzt `global.eu_commission`, `global.eucouncil` usw., Platzhalter ist `EUU.id`):
  - Kommission +0,30 PP/Tag, Rat +0,15, Parlament +0,10, Frontex +0,10, Finanzminister +0,10,
  - Hoher Vertreter (Einfluss, Meinung, Handel), ECB, EuroArmy, EuroNavy, UN-Botschafter, POTEF.
- **Besetzung [V]:** Wer zuerst kommt, besetzt das Amt per GUI (`01_european_union_guis.txt:1822-1931`) als `add_timed_idea` für 1825 Tage (ECB 2920 Tage). Bedingungen (Z. 170-379):
  - Mitglied, nicht schon Inhaber eines anderen Amts, kein Rücktritt in den letzten 90 Tagen,
  - mindestens 5 % Einfluss auf alle Mitglieder **oder** mindestens 5 % der EU-Bevölkerung **oder** "alle Großen haben schon ein Amt",
  - Freischaltungen: Rat und Parlament erst mit `treaty_of_lisbon` (EU104); Hoher Vertreter mit EU105; ECB erst mit `has_idea = euro`; EuroArmy/EuroNavy mit EU305/306; POTEF nie per GUI (`always = no`, Z. 369).
- **Rücktritt [V]:** `retire_office_click`, Europeanism −0,1 (Z. 1932). Beim Verlust eines Amts erhalten alle Mitglieder das Event `EUevent.21`, und die KI bekommt eine 14-tägige Nachfrist.
- **Kartenmodus [V]:** `EU_map_mode` färbt Amtsinhaber ein (`common/map_modes/EU_map_mode.txt`).

### 3.5 Europäisches Parlament (Wahl, Fraktionen)
- **Wahl [V]:** `election_EU_Parliament` (`99_eu_scripted_effects.txt:1582`).
  - Sitze: 732 (vor Lisbon), 750 (Lisbon) bzw. 1000 (Lisbon + EU651).
  - Verteilung nach `EU_pop_ratio`, begrenzt auf 5-99 Sitze je Land.
  - Pro Land werden Sitze über `party_pop_array` auf die **24 Unterideologie-Parteien** verteilt (Z. 1677-1742).
  - Rhythmus: `EUelection.2` beim Start, `EUelection.1` nach **1625 Tagen**, danach alle 5 Jahre über die Mission `EU_election_5_years` (`99_eu_scripted_effects.txt:799-801`, `EU_voting_decisions.txt:2`).
- **Fraktionsnamen [V]:** Pro Index gibt es einen festen Namen, teils mit Datumsweiche (z. B. EPP-ED → EPP ab 2009.6.22; `00_EU_parliament_scripted_localisation.txt:160ff`; Loc `MD_focus_EU_l_english.yml:1418-1447`).
- **Neu [V]:** Detailansicht der Fraktionen (`eu_view_party_X_members_click` → `EU_select_party_members`, `99_eu_scripted_effects.txt:1747`, GUI `eu_party_member_detail_gui`, `01_european_union_guis.txt:5216`).

### 3.6 Haushalt, Beiträge, Fonds, MFF
- **Beiträge [V]:** `EU_budget_contribution = gdp_total × call_rate %` (Start 1 %), wöchentlich /52 (`99_eu_scripted_effects.txt:1312-1355`). Die Buchung läuft als Ausgabe im Money-System (`00_money_system.txt:3967-3970`).
- **Ausgaben [V]:** Start 44 % Wachstum, 44 % "natural" (Kohäsion bzw. Landwirtschaft), 6 % global, 6 % Verwaltung (`set_EU_expenditure`, Z. 1373). Verteilung:
  - Wachstum nach Konjunkturidee × Bevölkerungsanteil (Z. 1412),
  - "natural" nach BIP pro Kopf in 12 Stufen (Z. 1446),
  - global an den Hohen Vertreter,
  - Verwaltung an Kommission bzw. Frontex.
  - Die Auszahlung (Summe × 0,019 ≈ 1/52) ist eine Einnahme im Money-System (`00_money_system.txt:996-1007`) und entfällt bei `EUU_subsidies_suspended`.
  - Die Nettoposition steht in `EU_budget_net` (Z. 1547).
- **Zyklus [V]:**
  - Jahreshaushalt: 344 Tage Timer + 7 Tage Vorbereitung + 14 Tage Entwurf.
  - MFF: 1237 + 14 + 28 Tage (`EU_voting_decisions.txt:415-625`).
  - Änderungen kosten 10 bzw. 15 PP pro Mitglied (`EU_global_click_cost`).
  - **Der Entwurf geht nur ins Parlament, wenn ein Mitglied `ECB_president` hält** (Z. 475-511, 581-617). Sonst wird er zurückgerollt.
- **Seigniorage [V]:** Ohne EUU fließt die Seigniorage des Euro in `global.EU_seigniorage_pool` und von dort in den EU-Haushalt (`99_eu_scripted_effects.txt:1327-1331`, `00_currency_effects.txt:448-475`).

### 3.7 Euro, Eurozone, Zinsen, EZB
- **Euro [V]:** Der Euro ist jetzt ein Gesetz im Slot `reserve_currency` (`AA_law_expanded_economics.txt:674, 769`). `cancel` greift ohne `EU_member` oder USoE.
- **Beitritt zum Euro [V]:** `EU_join_the_euro_decision` (`EU_voting_decisions.txt:1806`), 100 PP. Bedingungen:
  - Zins unter 3,5 % (Sonderfälle GRE und DEN),
  - Korruption höchstens Stufe 5,
  - stabiles Wachstum,
  - BIP pro Kopf über 10.
  - Danach `joining_the_euro` (`99_eu_scripted_effects.txt:1829`): Tausch gegen USD, CNY, JPY, RUB, GBP, CHF, Gulden, BRL, Bitcoin oder "kein Reserve". **Ein Tausch gegen `deutsche_mark` fehlt** [V]. Die D-Mark ist eine Ergänzung der Mod (Mod-`common/ideas/AA_law_expanded_economics.txt:769`).
- **OMT [V]:** Nur der ECB-Präsident mit `ECB_zero_interest_rate_policy` kann es starten bzw. anpassen (`01_european_union_guis.txt:2988-3094`). Effekt `execute_OMT` (`99_eu_scripted_effects.txt:241`): kauft für Euro-Mitglieder mit Zins über 4 % Schulden zurück, bis zu `global.OMT_size_limit` (400, +200 je Anpassung).
- **Schuldenkrise [V]:** Agenden 201-208 (EZB-Intervention, Bankenunion, Eurobonds mit Schuldenumverteilung, EFSF mit Troika-Missionen für POR/ITA/IRE/GRE/SPR/CYP, ESM, Fiskalunion, Wirtschaftsregierung, Finanzminister). Dazu Missionen `eurozone_reforms` und `troika_reforms` (`EU_voting_decisions.txt:630-773`).

### 3.8 Schengen
- **Nicht vorhanden** [V]. "Schengen" erscheint nur im Text zu Frontex (`MD_focus_EU_l_english.yml:113, 472, 1000, 1008`).

### 3.9 Verteidigung
- **Agenden [V]:** EDA (301, Tech-Sharing-Gruppe `EU_Tech_Share`), PESCO (302, +8 % Tech-Sharing), EDF (303), Sicherheitsrat (304), EuroArmy (305), EuroNavy (306), UN-Sitz (307), Nuklearmacht (308, `nuclear_power_def`).
- **Decisions [V]** (`EU_voting_decisions.txt:1209-1550`):
  - Frontex, EuroNavy, EuroArmy übernehmen; dabei werden OOBs geladen (`EU_frontex_basic_2000/2017`, `EU_EuroArmy_basic_2000`).
  - `EU_create_EDU` mit Faction-Template `faction_template_edu`: **entfernt `NATO_member` bei allen Mitgliedern** (Z. 1303-1349).
  - Grenzmanöver `EU_military_exercise`, Host, Mission und Gegenmanöver mit Bedrohung, Erfahrung, Kommandopunkten und Meinung (Z. 1351-1631).

### 3.10 Sanktionen
- **Kein EU-Sanktionsinstrument gegen Drittstaaten** [V]. Es gibt nur interne Sanktionen (3.2) und im USoE- bzw. POTEF-Endgame "environmental sanctions" (`EU_POTEF_decisions.txt:4-305`, `EU_USoE_decisions.txt:438-700`).

### 3.11 Euroskepsis → "Europeanism"
- **Umbau [V]:** Die Variable heißt jetzt `europeanism` (0-1; früher `eurosceptic`, invertiert). API:
  - `europeanism_change`, `EU_europeanism_change`, `EU_potential_europeanism_change` (`99_eu_scripted_effects.txt:119-195`),
  - bevölkerungsgewichteter EU-Mittelwert `global.var_europeanism` (`EU_update_vars`, Z. 29-112),
  - passive Drift über `modifier@europeanism_drift` für Kandidaten (Z. 99-109).
- **Kampagnen [V]:** Vier GUI-Kampagnen pro/contra im eigenen Land bzw. EU-weit, 50-300 PP plus BIP-Anteil aus der Staatskasse, Zufallsergebnis, 120 Tage Cooldown (`01_european_union_guis.txt:2423-2636`).
- **Wirkung [V]:**
  - KI-Stimmverhalten (`99_EU_voting_scripted_effects.txt:24-41`),
  - Austritts-KI (`01_european_union_guis.txt:3097`),
  - Rats-Vorschlagsrecht nur bei Europeanism über 0,6 (Z. 4307),
  - Beitrittsschwelle.
- **Startwerte [V]:** fest 2000-bezogen (`99_eu_scripted_effects.txt:815-831`).

### 3.12 GUI und Scripted GUI
- **Struktur [V]:**
  - Startknopf `open_the_eu_scripted_gui` (Z. 4) → Hauptfenster `european_union_gui` (Z. 39) mit 5 Tabs: Ämter, Europeanism/Euro-Info, Parlament, Rat, Fiskal.
  - Unterlisten als eigene `scripted_gui` mit `parent_scripted_gui`: `european_info_dynamic_lists` (4157), `european_omt_budget_dynamic_lists` (4186), `european_council_voting_dynamic_lists` (4216), `european_parliament_dynamic_lists` (4573), `epsd_dynamic_lists` (5187), `eu_party_member_detail_gui` (5216), `eu_contributions_2nd_display_gui` (5251), `eu_distribution_2nd_display_gui` (5278).
  - Aktualisierung über `global.EU_dirty_update_var`.
- **Neu gegenüber der Alt-Basis [V]:** Seitenpanel Fiskal (Beiträge/Ausschüttungen umschaltbar, `eu_fiscal_view_toggle_click`, Z. 1806) und Fraktions-Detailpanel.

### 3.13 KI-Logik
- **GUI-KI [V]:** `ai_enabled`/`ai_check` mit Prüfintervall 108 h (`01_european_union_guis.txt:68-89`). Gewichte für Austritt, Ämter, Fraktionskauf, Kampagnen und Haushalt ab Z. 3095.
- **Abstimmungs-KI [V]:**
  - Tabelle `global.EU_vote_w1..w6^ID` (nach Regierungspartei-Gruppe) plus `EU_vote_hist^ID` (`99_EU_voting_scripted_effects.txt:170-227`),
  - Zuschläge nach Einfluss, Europeanism, SOV/CHI-Einfluss (−25 bis −75), Subjekt folgt Oberherr, Schwierigkeitsgrad (Z. 5-108),
  - Game-Rule-Bias für Erweiterung (Z. 229).
- **Rats-Vorschläge der KI [V]:** Gewichte in `list_of_available_council_votes` (`01_european_union_guis.txt:4484-4550`), mit Historie-Boni für 2004/2007/2013 und Rule-Sperre für Endgames.
- **Wöchentlicher "Monitor" [V]:** Ein zufälliger KI-Kandidat mit `EUU_monitor` (`99_eu_scripted_effects.txt:794-797`, `MD_on_actions.txt:720-757`).

### 3.14 Gemeinsame Fokusbäume und Endgame
- **USoE (EU111) [V]:** Annektiert alle Mitglieder in den Kommissionspräsidenten. Das gilt **auch für menschliche Spieler**: Ablehner verlieren vorher nur die Mitgliedschaft. Formable 101, Fokusbaum `01_EU_USoE_shared.txt` mit 90 shared focuses, moderne Themen wie "AI Government", "EUSSR", "Operation Unthinkable 2.0" (`99_EU_voting_scripted_effects.txt:406-504`).
- **Europäische Föderation (EU112) [V]:** Flag `european_federation`, POTEF-Wahl über Kampagnen (`EU_POTEF_decisions.txt:306-566`, `99_eu_scripted_effects.txt:1024-1192`), Fokusbaum `02_EU_POTEF_shared.txt` mit 74 "Doktrinen" nach Regionen.
- **Gegenseitiger Ausschluss [V]:** 111 und 112 schließen sich aus (`EU_drop_rival_endgame`, Z. 385).
- **EFS-Flaggen [V]:** `MD_EFS_decisions.txt`.
- **Einbindung [A]:** Die shared focuses werden in Länderbäume über `shared_focus = …` eingebunden. Ob die 1970-Bäume der Mod (`mdcw_1970_generic_focus` usw.) das tun, ist ungeprüft.

### 3.15 Startup und Game Rules
- **Startup [V]:** `on_startup_euu_action` (`99_eu_scripted_effects.txt:613-879`) setzt: Game-Rule-Flags, Katalog, 15 Gründungsmitglieder, Strafideen, `EU_potential` aus Collections, Monitor, erste Wahl nach 1625 Tagen, Europeanism-Startwerte, KI-Gewichte, Haushaltsmissionen, Amts-Platzhalter `EUU.id`.
- **Game Rules [V]:**
  - `rule_disable_eu` (yes/no),
  - `rule_european_union_voting_limits`,
  - `rule_european_union_expansion_focus`,
  - `rule_enable_ai_european_union_end_game_paths` (`00_game_rules.txt:299-383`).
  - Die Mod-Kopie ist byte-identisch [V].

---

## 4. Delta

### 4.1 Mod-aktuell gegen MD 2.0.2 [V]
**Byte-identisch (31 Dateien):**
- `common/decisions/EU_POTEF_decisions.txt`, `EU_USoE_decisions.txt`, `EU_voting_decisions.txt`, `MD_EFS_decisions.txt`, `MD_USoE_decisions.txt`
- `common/decisions/categories/EU_voting_categories.txt`, `00_decision_categories.txt`
- `common/national_focus/01_EU_USoE_shared.txt`, `02_EU_POTEF_shared.txt`
- `common/scripted_effects/99_eu_scripted_effects.txt`, `99_EU_voting_scripted_effects.txt`, `EUU_political_leaders.txt`
- `common/scripted_triggers/99_EU_scripted_triggers.txt`, `99_EU_voting_scripted_triggers.txt`
- `common/ideas/EU_ideas.txt`, `EU_Council_ideas.txt`, `EU_POTEF_ideas.txt`, `EU_USoE_ideas.txt`, `Organizations.txt`
- `common/scripted_guis/01_european_union_guis.txt`
- `common/scripted_localisation/00_EU_parliament…`, `00_EU_scripted…`, `00_EU_voting…`
- `interface/eu.gui`, `eu.gfx`
- `localisation/english/MD_focus_EU_l_english.yml`
- `events/EU_events.txt`, `EU_news.txt`, `EU_USoE_events.txt`
- `common/dynamic_modifiers/05_POTEF_dynamic_modifiers.txt`
- `common/game_rules/00_game_rules.txt`

**Abweichend, EU-relevant:**
- `common/scripted_effects/00_currency_effects.txt`:
  - D-Mark-Emittent (Staat 966, Bonn/Köln) vor 1999,
  - "Euro has no issuer in the historical Cold War period",
  - `deutsche_mark` für GER bei Start vor 1999 (Mod-Datei, Z. 65-68 und 84-117).
- `common/on_actions/MD_on_actions.txt`: Bürgerkriegs-Epiloge und jahresgebundene Events nur nach 1999. **EU-Hooks unverändert.**
- `common/on_actions/00_on_actions.txt`: Warschauer Pakt, Libyen/Utility-Weichen. **EU-Startup unverändert** (Z. 1956).
- `00_money_system.txt`, `00_startup_effects.txt`: abweichend. EU-Stellen nicht verändert [A]; nur die EU-Zeilen wurden geprüft.

### 4.2 Alt-Basis (1.18, vor 8.10.2026) gegen MD 2.0.2: neu, umgebaut, entfernt [V]

| Bereich | Neu in 2.0.2 | Umgebaut | Entfernt |
|---|---|---|---|
| Stimmung | `europeanism` (0-1), `europeanism_drift`-Modifier, `EU_init_default_europeanism`, Kandidaten-Untergrenze 0,5 | GUI-Header "Europeanism" statt "Euroscepticism" (`eu.gui`: `soteu_europeanism_header`, `country_europeanism_status`) | `eurosceptic_change`, `EU_eurosceptic_change`, `EU_potential_eurosceptic_change`; Beitrittsprüfung `eurosceptic < 0.15` (alt `EU_voting_decisions.txt:2481-2484`) |
| Mitgliedschaft | `EU_former_member` + 1095 Tage Cooldown, `EU_resync_member_array`, `EU_vacate_offices`, `EU_adopt_passed_laws` beim Beitritt | `EU_member` ohne `allowed`-Liste (alt: 35 Tags); `EU_potential` aus Collections und Script-Konstante | – |
| Abstimmung | `apply_EU_QMV_result`-Dispatcher, Platzhalter-Logik (`EU_is_commission_caretaker`), `EU_drop_rival_endgame`, `EU_finalize_passed_agenda` | KI-Gewichte als Tabelle statt 47 Einzel-Effekte (Kommentar `99_EU_voting_scripted_effects.txt:167-168`); **QMV: Enthaltung zählt jetzt als Nein** (alt: Ja/(Ja+Nein) > 0,55, alt `99_EU_voting_scripted_triggers.txt:57-64`) | 47× `EU_update_AI_focus_EU###_voting_modifier`, ~60 `focus_EU###_EP_approval`-Trigger, `is_*_block`-Trigger, `cleanup_european_union_voting_yes/no`, `EU_clear_voting` und zugehörige Missionen (`EU_clear_voting_mission`, `EU_update_vars_mission`, `…_timer`) |
| Erweiterung | Agenden 654-660 (russische Regionen); Game-Rule `rule_european_union_expansion_focus` | – | – |
| Wahlen | Wahlrhythmus über die 5-Jahres-Mission (erste Wahl nach 1625 Tagen) | Fraktionsnamen generisch nach 24 Unterideologien | festdatierte `EU_election_2004`/`EU_election_2019`; Zuordnung Länderpartei → Fraktion (alt `00_EU_parliament_scripted_localisation.txt`: 15 125 Zeilen, jetzt 493) |
| Haushalt | Fiskal-Seitenpanel, Failsafes `EU_budget_EP_block`, Seigniorage-Pool | Entwurf läuft über den ECB-Präsidenten | `00_EU_budget_scripted_localisation.txt` (1870 Zeilen); Decisions `EU_budget_draft_ongoing_president`, `EU_mff_draft_ongoing_president` |
| Euro | `EU_join_the_euro_decision` (GRE/DEN-Sonderwege), `joining_the_euro` als Tausch im Reservewährungs-Gesetz | Idee `the_euro` (alt `Organizations.txt:70`) → Gesetz `euro` (`AA_law_expanded_economics.txt:769`) | alte Decision `EU_join_the_Euro` |
| Einfluss | – | – | `EU_money_for_influence`, `invest_in_EU_single_market_cic`, Decisions `invest_in_FRA/GER/POL_cic/SWI`, `create_eurosphere` (jetzt USoE-Decision), `catholic_leadership`, `christian_leadership` |
| POTEF | Dynamic Modifier `POTEF_dynmod_*` mit Variablen (`05_POTEF_dynamic_modifiers.txt`) | – | 60× `update_POTEF_*_factor`; 8 POTEF-Ideen (z. B. `POTEF_infantry_doctrine`, `EU_naval_doctrine`) |
| GUI | Fraktions-Detailansicht (24 Knöpfe), Fiskal-Umschalter | `eu.gfx` von 160 auf 39 Zeilen (Sprites verlagert [A]) | Fraktions-Icons `epp`, `pes`, `eldr`, `uen`, `eu_greens`, `eu_gue` usw. als eigene GUI-Elemente |
| Events | `EUvote.5`/`.6` (USoE-Abstimmung) | – | `EU_party_news.*`, `EUcheat.1`, `EUupdate.1/2`, `EUelection.3`, `EUevent.2/3/17`, 10 `EU_news` (u. a. `.1`, `.28-.31`, `.53-.56`), `EU_info.1` |
| Fokus | – | USoE 93 → 90 IDs (`USoEevent.1-3` als IDs entfernt), POTEF 74 IDs unverändert, Inhalte geändert | – |

---

## 5. Was 1970 im nativen Code konkret passiert (Code-Pfad-Analyse)

| # | Befund | Beleg | Status |
|---|---|---|---|
| 1 | Der Startup schreibt 15 Staaten von 2000 nach `global.EU_member`. Die Sechs haben 1970 keine `EU_member`-Idee | `99_eu_scripted_effects.txt:760-774`; Mod-`00_on_actions.txt:1956`; Mod-History nur `2000.1.1` | V (Laufzeit A) |
| 2 | Die 15 erhalten `foreign_data_kraken` und `asylum_shopping` | `99_eu_scripted_effects.txt:777-783` | V |
| 3 | Kein ECB-Präsident ohne Euro → Haushalts- und MFF-Änderungen werden immer zurückgerollt | `EU_voting_decisions.txt:475-511, 581-617`; GUI Z. 289-291 | V |
| 4 | Rats- und Parlamentspräsident sind erst nach EU104 (Lisbon) besetzbar | `01_european_union_guis.txt:170-175, 254-258` | V |
| 5 | Kein Kandidatenpfad für ENG/IRE/DEN (EU609 deckt nur NRY/ICE/SWI/Mikrostaaten ab) | `99_EU_voting_scripted_effects.txt:963-975` | V |
| 6 | Parlament: 732 Sitze nach Bevölkerung, begrenzt 5-99 → EG6 ergäbe etwa 3×99 + HOL ~50 + BEL ~38 + LUX 5 ≈ 390 statt 142 | `99_eu_scripted_effects.txt:1598-1642, 1682-1690` | Formel V, Zahl A |
| 7 | Erste EP-Wahl nach 1625 Tagen ≈ Juni 1974, danach 1979/84/89. Die späteren Termine treffen zufällig die echten Direktwahlen | `99_eu_scripted_effects.txt:799-801` | V |
| 8 | Alle Agenden ab 2000 sind sofort wählbar (101 braucht nur 200 PP) | `01_european_union_guis.txt:4645` | V |
| 9 | QMV nach Bevölkerung 65 %/55 % statt Gewichtung 4/4/4/2/2/1 (12 von 17); Enthaltung zählt als Nein | `99_EU_voting_scripted_triggers.txt:16-23` | V |
| 10 | `joining_the_euro` tauscht die D-Mark nicht → GER mit `deutsche_mark` bekäme keinen Euro, nur das Flag `EU_joined_the_eurozone` | `99_eu_scripted_effects.txt:1829-1915`; Mod-`00_currency_effects.txt:65-68` | V |
| 11 | EDU entfernt NATO bei allen Mitgliedern; USoE annektiert auch menschliche Mitglieder | `EU_voting_decisions.txt:1327-1335`; `99_EU_voting_scripted_effects.txt:429-466` | V |
| 12 | Kandidaten können den Rat-Tab öffnen. `support_council_vote_button_click_enabled` prüft keine Mitgliedschaft → Kandidaten könnten mitstimmen (Bevölkerungsgewicht 0, zählen aber bei den Staaten mit) | `01_european_union_guis.txt:113-118, 1323-1326` | V Code, A Effekt |
| 13 | `all_eu_available_countries` enthält kein DDR (relevant für innerdeutschen Handel und Wiedervereinigung) | `common/script_constants/country_groups.txt` | V |
| 14 | `pre_accession_assistance_program` endet nach 5 statt 180 Tagen | `EU_voting_decisions.txt:1892` | V |

---

## 6. Portierbarkeit

### 6.1 Syntax- und Engine-Risiken
- **1.18 gegen 1.19 ist für die Mod heute irrelevant [V]:** Die Mod läuft auf 1.19.\*, und das EU-System ist bereits das native 2.0.2-System.
- Nur falls jemand auf 1.18 zurückportieren wollte [A]:
  - `constant:country_groups…` (Script-Konstanten),
  - `every_collection_element`/`named_collection`,
  - der eigene Modifier über `modifier@europeanism_drift`,
  - `mark_focus_tree_layout_dirty`.
  - Die alte 1.18-EU nutzte bereits `create_faction_from_template`, `force_update_map_mode`, `meta_effect`, `for_each_scope_loop`, `while_loop_effect` und `population_total` [V, grep Alt-Basis]. Diese gelten damit als 1.18-sicher.

### 6.2 Abhängigkeiten zu anderen MD-Systemen [V, im Code referenziert]
| Abhängigkeit | Genutzt durch |
|---|---|
| Money-System | `additional_income_rate`/`additional_expenses_rate`, `modify_treasury_effect`, `interest_rate`, `debt`, `debt_ratio` |
| Reservewährung und Seigniorage | `reserve_currency`-Gesetz, `global.eur_issuer` |
| Einfluss-System | `influence_array`, `influence_higher_X`, `is_top3_influencer` |
| Partei-System | `party_pop_array` mit 24 Indizes, `ruling_party`, `change_relative_party_popularity`, `recalculate_party` |
| Konjunktur- und Korruptionsideen | `economic_boom`…`depression`, `corruption_level_01-10` |
| Weitere | Wahlen (`has_elections`), NATO (`NATO_member`, `global.nato_members`), Faction-Templates, Collections und Script-Konstanten, Kartenmodus, Dummy-Tag `EUU` (Mod-History vorhanden [V]), Formable-ID 101, Raketeninventar, ENG/GER-Flags, Tech-Sharing `EU_Tech_Share`, OOB-Dateien |

Alle Abhängigkeiten sind in der Mod vorhanden, weil sie auf MD 2.0.2 basiert [A, `script_constants` V].

### 6.3 Aufwand je Hebel
| Hebel | Aufwand |
|---|---|
| Startup 1970 (EG6, Katalog, Europeanism, Strafideen weg) per eigenem `on_startup`-Zweig vor bzw. statt `on_startup_euu_action` | klein |
| Neue Agenda-IDs für 1970: Arrays + `EU_vote_w*`-Zeilen + Dispatcher-Zweig + Loc + Prüfung in `eu_parliament_available_reforms_button_click_enabled` | mittel (Gerüst vorhanden) |
| Gewichteter Rat 4/4/4/2/2/1, QMV 12/17, Einstimmigkeit und Veto-Joker: `EU_voting_decision_result_trigger` ersetzen + Gewichtsvariablen | mittel |
| Rotierende Präsidentschaft per Halbjahres-Timer statt "wer zuerst kommt" | mittel |
| Parlament: feste Sitze 142/198, Fraktionen 1970, Direktwahl 1979 | mittel |
| Haushalts-Gate vom ECB-Präsidenten lösen (z. B. Kommission oder Ratsvorsitz) | klein |
| Beitrittskapitel, Referenden, Assoziierungsleiter | groß |
| Währungsstufen Werner/Schlange/EWS | mittel bis groß |
| EPZ-Erklärungen mit Imperia-Sanktionen, Schengen-Vorläufer | mittel |

---

## 7. Eignung für 1970 und Ideen je Feature

| MD-Feature (Beleg) | Historisch 1970 | Alt-historische Option | Bewertung | Aufwand |
|---|---|---|---|---|
| Mitgliedschaft `EU_member` + Array (`Organizations.txt:4`) | EG6 FRA/GER/ITA/BEL/HOL/LUX. Name "European Communities" (Loc), "European Union" als späterer Meilenstein | Kleineuropa ohne UK (POD 1); Nordek statt Beitritt | **übernehmen** (Startup ersetzen) | klein |
| Beitritt (`EU_apply_for_membership`, 1635) | Ab 30.6.1970 verhandeln ENG/IRE/DEN/NOR. Neue Agenda "Hague Enlargement Mandate" setzt `EU_candidate` für die vier. Europeanism-Schwelle 0,8 für Menschen ist zu hoch für ENG 1970 → Schwelle pro Agenda oder Referendum | NOR tritt bei (POD 2); DEN Nein (POD 19); frühe Süderweiterung nach Demokratisierung (POD 11) | **umbauen** | mittel |
| Kapitel und Referenden | fehlen in MD. Kapitelmissionen pro Kandidat (Zollunion, GAP, Commonwealth, Fischerei, Haushalt, Institutionen), Referendum mit `party_pop_array`-Formel | Kapitel-Veto als Hebel (FRA GAP gegen ENG Regionalfonds) | **neu** (MD bietet nur die Pipeline) | groß |
| Austritt (Art. 50, `EU_voting_decisions.txt:777`) | Kein Austrittsartikel vor Lisbon → "Renegotiation of Terms" (UK 1974/75) + Referendum + Austrittsvertrag einstimmig; Grönland 1985 als Teilgebiet. Missionsgerüst (730 Tage, Strafe `no_deal_exit`) wiederverwenden | UK-Austritt 1975 (POD 3) | **umbauen** (Loc, Bedingungen) | mittel |
| IPA/Heranführung (2406, 1880) | Assoziierungs-Finanzprotokolle und EIB-Darlehen: Türkei-Zusatzprotokoll 23.11.1970, Malta 5.12.1970, Griechenland eingefroren. Timeout-Fehler beheben | Jugoslawien-Abkommen, Rumänien-Annäherung (POD 13/17) | **umbauen** | klein |
| Werteverstoß und Sanktionen (435; 127-378) | Punkteliste passt gut zur Birkelbach-Doktrin. Diktatur und keine Wahlen sperren Assoziierung bzw. Beitritt (SPR/POR/GRE). Suspendierung gab es nicht (Art. 7 erst 1999) → "Freeze Association" für Assoziierte | Fortsetzung trotz Junta (Kohäsionskosten) | **umbauen** (für Mitglieder entschärfen, für Assoziierte nutzen) | klein bis mittel |
| Parlament → Rat (Pipeline, Missionen) | EP nur beratend: Stellungnahme statt Hürde (Vorschlag: EP-Stufe nur als Meinung, später mit Haushaltsrecht 1975). Rat: Gewichte 4/4/4/2/2/1, QMV 12/17, faktisch Konsens + Joker "Luxemburger Kompromiss" | Überstimmung ab Mai 1982 bzw. EEA; Krise des leeren Stuhls (POD 14) | **umbauen** | mittel |
| Cooldown-Rule (315) | passt für MP | – | **übernehmen** | – |
| Ämter (Ideen 4-197; GUI 1822-1931) | Ratsvorsitz halbjährlich alphabetisch: BEL H1 1970, GER H2, FRA/ITA 1971, LUX/HOL 1972 → `EU_council_president` per Timer. Kommission (Malfatti ab 1.7.1970) per Einstimmigkeits-Agenda. EP-Präsident ohne Bonus. Hoher Vertreter, Finanzminister, Frontex, EuroArmy, EuroNavy, UN, POTEF für 1970 ausblenden | Gaullistischer Rats-Generalsekretär (Fouchet, POD 5); föderaler Kommissionspräsident (POD 6) | **umbauen** | mittel |
| Wahl und Fraktionen (1582, `00_EU_parliament…`) | 142 ernannte Sitze (36/36/36/14/14/6), 1973 198. Direktwahl Juni 1979 (erste Wahl auf 3450 Tage verschieben = 7.6.1979). Fraktionsnamen 1970 per Datumsweichen: Christdemokraten, Sozialisten, Liberale, EDP (Gaullisten); 1973 Kommunisten und Konservative. Nebenbei: Die Index-Zuordnung (1 = EPP, 3 = PES, 2 = ELDR, 19 = GUE …) passt fast | Frühe Direktwahl (Spinelli) | **umbauen** | mittel |
| Europeanism + Kampagnen (119-195; 2423-2636) | Startwerte 1970 aus Abschnitt 6.11 des Historienberichts (Gaullisten, Labour-Linke, Fischer usw.); Kampagnen beibehalten | Föderalisten-Kampagne als Voraussetzung für Vertiefung | **übernehmen** (Werte neu) | klein |
| Haushalt (1312-1550; Money 996-1007, 3967) | Bis 1970 Beiträge nach Schlüssel. Eigenmittel 21.4.1970 (ab 1971 Zölle und Abschöpfungen, MwSt bis 1 % ab 1979). Ausgaben: GAP ca. 80-90 % ("natural"), Sozialfonds, Regionalfonds ab 1975, Verwaltung. `EU_budget_net` als Hook für die britische Haushaltsfrage und den Rabatt (Fontainebleau 1984). MFF erst ab Delors-I 1988 → bis dahin nur Jahreshaushalt. Gate über den ECB lösen | Höhere Eigenmittel, Föderalhaushalt | **umbauen** | mittel |
| Euro, Eurozone, EZB, OMT (1806, 1829, 241) | Werner-Plan (8.10.1970) als Agenda; Schlange 24.4.1972 als Gruppen-Idee mit Austrittsrecht und DM als Anker (Mod-DEM-Emittent nutzbar); EWS/ECU 1979; Euro erst Maastricht/1999. OMT, Eurobonds, ESM, Troika für 1970 sperren. D-Mark-Tausch in `joining_the_euro` ergänzen | Werner-Plan gelingt, Währungsunion ~1980 (POD 4) | Euro/OMT/Krise: **weglassen** für 1970 (für 2000-Start behalten); Werner/Schlange/EWS: **neu** auf dem Reservewährungs-Gerüst | mittel bis groß |
| Schengen | nicht vorhanden. Start-Ideen nordische Passunion, Benelux-Passunion, Common Travel Area UK-IRE; Schengen 1985 als Agenda | Frühe Passunion als EPZ-Folge | **neu** | klein bis mittel |
| Verteidigung (301-308; 1209-1550) | Keine EU-Armee. WEU ruht (FRA-Boykott 1969). "WEU Reactivation" (1984), EVG-Revival und nukleare Option als alt-historische Agenden. EDU nur alt-historisch, weil sie NATO entfernt. Manöver-Decisions als WEU-Übungen nutzbar | EVG-Revival, europäisierte Force de frappe (POD 7), Dritte Kraft (POD 8) | **umbauen bzw. großteils weglassen** | mittel |
| Sanktionen | MD hat keine EG-Außensanktionen → EPZ (Davignon 27.10.1970): Decision "Common Declaration" einstimmig, optional kollektive Sanktionen über die Imperia-Sanktionen (Mod `imp_sanctions_*`) | Sanktionen gegen Junta-Griechenland bzw. Franco-Spanien | **neu** | mittel |
| Migration, Digitales (401-408), Strafideen | 1970 anachronistisch | – | **weglassen** | klein |
| Erweiterungswellen (601-660) | Ersetzen durch 1973 (ENG/IRE/DEN/NOR), Süderweiterung (GRE 1981, SPR/POR 1986), EFTA 1995, Osterweiterung nach 1989. 654-660 weglassen | Türkei (POD 12), Neutralen-Block (POD 16) | **umbauen** | klein (Daten) |
| Endgame USoE/POTEF + shared Trees | Spinelli-Pfad (Verfassung 1984) → USoE nur alt-historisch und nur mit einstimmiger Zustimmung der Menschen (MP-Schutz). Die Bäume sind modern (Trump, Drohnen, KI-Regierung) → für 1970 sperren | Föderale USoE (POD 6), Union der Staaten (POD 5) | **weglassen** (vorerst) bzw. später umbauen | groß |
| GUI (5 Tabs, Seitenpanels) | Bleibt unverändert, nur Loc und Sichtbarkeiten anpassen. Die Erfahrung mit CWEC zeigt: parallele GUIs vermeiden | – | **übernehmen** | klein |
| KI (Gewichtstabelle, Monitor) | Tabelle um 1970-IDs ergänzen; historische Defaults (FRA-Veto, GER Ökonomist) über `EU_vote_hist` | – | **übernehmen** | klein |
| Kartenmodus, Game Rules | Rule "Historical EC 1970 start" ergänzen | – | **übernehmen** | klein |

---

## 8. Empfehlung zur Vorgehensweise (kurz)

1. **Erster Schritt (klein):** Startup-Zweig für Starts vor 1999 anlegen.
   - Setzen: EG6 als Mitglieder (Idee + Array), keine Strafideen, 1970er-Katalog, Europeanism-Startwerte, erste Wahl erst 1979.
   - Gates anpassen: ECB → Kommission bzw. Ratsvorsitz; Lisbon-Sperren für Rat und Parlament nur für moderne Ämter.
   - Bugfixes: IPA-Timeout, D-Mark-Tausch, Ratsabstimmung nur für Mitglieder.
   - Den Code der Basis nicht kopieren, sondern in den bestehenden Dateien gezielt patchen. Die Mod-Doku zur Wiederherstellung warnt vor parallelen Systemen.
2. **Zweiter Schritt (mittel):** Neue Agenda-IDs (z. B. 7xx) für Eigenmittel, Werner, EPZ, Regionalfonds, Europäischer Rat, Direktwahl, EEA, Maastricht und Schengen. Dazu Gewichtsregel 4/4/4/2/2/1 mit Veto-Joker.
3. **Dritter Schritt (groß):** Beitrittskapitel und Referenden, Währungsstufen, Assoziierungsleiter.

---

## 9. Offen bzw. im Spiel zu prüfen [A]
- Laufzeitverhalten des Startups von 2000 in der 1970-Kampagne: Log-Einträge `on_startup_euu_action` und Inhalt von `EU_member` am 1.1.1970.
- Ob 1970-Länderbäume die USoE/POTEF-shared-focuses einbinden.
- Wirkung von Kandidaten-Stimmen im Rat (Befund 12).
- Ob noch irgendein Länderfokus der Mod `eurosceptic`-Variablen der Alt-Basis nutzt. Die nationalen Fokusdateien der Mod wurden nicht gestagt.

---

## 10. Gestagte Dateien (nur gelesen)

**MD 2.0.2 → `/mnt/user-data/uploads/2777392649/`**
- `descriptor.mod`, `Changelog.txt`
- `common/decisions/`: `EU_POTEF_decisions.txt`, `EU_USoE_decisions.txt`, `EU_voting_decisions.txt`, `MD_EFS_decisions.txt`, `MD_USoE_decisions.txt`, `00_monetary_policy_decisions.txt`, `categories/EU_voting_categories.txt`, `categories/00_decision_categories.txt`
- `events/`: `EU_events.txt`, `EU_news.txt`, `EU_USoE_events.txt`
- `common/national_focus/`: `01_EU_USoE_shared.txt`, `02_EU_POTEF_shared.txt`
- `common/scripted_effects/`: `99_eu_scripted_effects.txt`, `99_EU_voting_scripted_effects.txt`, `EUU_political_leaders.txt`, `00_startup_effects.txt`, `00_money_system.txt`, `01_international_systems_effects.txt`, `00_currency_effects.txt`, `00_yearly_effects.txt`, `00_scripted_effects.txt`, `00_country_group_flags.txt`, `00_AI_scripted_effects.txt`, `00_influence_scripted_effects.txt`, `00_economic_effects.txt`
- `common/scripted_triggers/`: `99_EU_scripted_triggers.txt`, `99_EU_voting_scripted_triggers.txt`, `00_game_rule_triggers.txt`, `01_international_triggers.txt`, `00_scripted_triggers.txt`, `MD_Country_Groups_Triggers.txt`, `00_economic_triggers.txt`, `00_influence_scripted_triggers.txt`, `01_political_triggers.txt`
- `common/ideas/`: `EU_Council_ideas.txt`, `EU_ideas.txt`, `EU_POTEF_ideas.txt`, `EU_USoE_ideas.txt`, `Organizations.txt`, `AA_law_expanded_economics.txt`
- `common/dynamic_modifiers/`: `05_POTEF_dynamic_modifiers.txt`, `00_MD_dynamic_modifiers.txt`
- `common/scripted_guis/01_european_union_guis.txt`
- `common/scripted_localisation/`: `00_EU_parliament_scripted_localisation.txt`, `00_EU_scripted_localisation.txt`, `00_EU_voting_scripted_localisation.txt`, `01_international_scripted_localisation.txt`, `01_money_scripted_localisation.txt`
- `interface/`: `eu.gfx`, `eu.gui`
- `localisation/english/`: `MD_focus_EU_l_english.yml`, `MD_focus_EU_POTEF_l_english.yml`, `MD_focus_EU_USoE_l_english.yml`, `MD_international_l_english.yml`, `MD_currency_l_english.yml`
- `common/on_actions/`: `00_on_actions.txt`, `MD_on_actions.txt`, `999_game_rules_on_actions.txt`, `MD_event_on_actions.txt`
- `common/game_rules/00_game_rules.txt`
- `common/modifier_definitions/`: `modifier_definitions.txt`, `influence_modifier_definitions.txt`, `political_modifier_definitions.txt`, `money_modifier_definitions.txt`
- `common/map_modes/EU_map_mode.txt`
- `common/collections/`: `collections.txt`, `generic_collections.txt`
- `common/factions/templates/00_EU.txt`
- `common/script_constants/country_groups.txt`
- `common/opinion_modifiers/`: `Organization Opinions Modifiers.txt`, `EU_POTEF.txt`, `new_opinion_modifiers.txt`

**Mod-aktuell → `/mnt/user-data/uploads/mdcoldwar/` (zusätzlich zu den schon vorhandenen Dateien)**
- `descriptor.mod`, `Changelog.txt`, `README.md`, `mdcoldwar.mod`
- `common/scripted_guis/01_european_union_guis.txt`
- `common/scripted_triggers/`: `99_EU_scripted_triggers.txt`, `99_EU_voting_scripted_triggers.txt`
- `common/ideas/`: `EU_ideas.txt`, `Organizations.txt`, `EU_POTEF_ideas.txt`, `EU_USoE_ideas.txt`, `EU_Council_ideas.txt`, `AA_law_expanded_economics.txt`
- `common/scripted_localisation/00_EU_*` (3 Dateien)
- `interface/`: `eu.gui`, `eu.gfx`
- `localisation/english/MD_focus_EU_l_english.yml`
- `common/on_actions/`: `MD_on_actions.txt`, `00_on_actions.txt`
- `common/scripted_effects/`: `00_money_system.txt`, `00_startup_effects.txt`, `00_currency_effects.txt`
- `common/dynamic_modifiers/05_POTEF_dynamic_modifiers.txt`
- `common/game_rules/00_game_rules.txt`
- `history/countries/`: FRA, ENG, SWE, AUS, GER, EUU, BEL, SPR

**Alt-Basis → `/mnt/user-data/uploads/mdcoldwar_2026-10-08_before_md_2_0_2_migration/mod/`**
- `descriptor.mod`
- `common/decisions/`: `EU_POTEF_decisions.txt`, `EU_USoE_decisions.txt`, `EU_voting_decisions.txt`
- `events/`: `EU_events.txt`, `EU_news.txt`, `EU_USoE_events.txt`
- `common/national_focus/`: `01_EU_USoE_shared.txt`, `02_EU_POTEF_shared.txt`
- `common/scripted_effects/`: `99_eu_scripted_effects.txt`, `99_EU_voting_scripted_effects.txt`
- `common/scripted_triggers/`: `99_EU_scripted_triggers.txt`, `99_EU_voting_scripted_triggers.txt`
- `common/ideas/`: `EU_ideas.txt`, `EU_Council_ideas.txt`, `EU_POTEF_ideas.txt`, `EU_USoE_ideas.txt`, `Organizations.txt`
- `common/scripted_guis/01_european_union_guis.txt`
- `common/scripted_localisation/`: `00_EU_budget…`, `00_EU_parliament…`, `00_EU_scripted…`, `00_EU_voting…`
- `localisation/english/`: `MD_focus_EU_l_english.yml`, `MD_focus_EU_POTEF_l_english.yml`, `MD_focus_EU_USoE_l_english.yml`
- `interface/`: `eu.gui`, `eu.gfx`
