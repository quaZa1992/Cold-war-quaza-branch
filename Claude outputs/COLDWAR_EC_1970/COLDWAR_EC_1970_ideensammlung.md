# EG 1970 im MD-EU-System – Systemdesign v2

Stand 18.10.2026 · MD Cold War (`mdcoldwar`, Basis MD 2.0.2 / HOI4 1.19), Start 1.1.1970, MP-Rollenspiel · Marker für neuen Code: `COLDWAR`

**Grundsatz:** Es gibt **ein** System, und das ist das native MD-EU-System. 1970 bedeutet nur drei Dinge:
- **MD-EU mit 1970-Daten**
- **neue Agenden im MD-Nummernschema**
- **wenige `# COLDWAR`-Hooks** in MD-Dateien

Was es nicht gibt:
- keine eigene GUI
- keine eigene Abstimmungs-Engine
- keine Parallel-Arrays
- keinen Ersatz für MD-Logik

Der Codex-Stand in `docs/europe_1970_audit`, `docs/native_eu_1970` und `docs/main_md_eu_restore` ist **keine Grundlage** und wird nicht verwendet. Status: **Stufe 1 ist eingebaut** (18.10.2026, siehe §8). Stufe 2 folgt nach Freigabe.

---

## 1. Die MD-Mechanik, auf der alles läuft

```
Agenda-ID in global.EU_potential_votes
  → Parlament: Vorschlag im EU-Fenster (0/200/300 PP) → Mission 14 Tage → Fraktionsmehrheit (50 % + 1)
  → global.EU_council_votes
  → Rat: Vorschlag (500 PP, gratis für Amtsinhaber) → Mission 14 Tage
       KI stimmt nach Tabelle w1..w6 (Regierungsfamilie) + Europeanism + Einfluss + historischem Gewicht,
       Spieler stimmen per Klick
  → EU_voting_decision_result_trigger: über 65 % Bevölkerung UND über 55 % der Staaten
  → apply_EU_QMV_result → focus_EU<ID>_QMV_result → global.EU_passed_votes
```

**KI-Gruppen** (`99_EU_voting_scripted_effects.txt:112-158`):

| Gewicht | Parteifamilie (Index) |
|---|---|
| w1 | Konservative (1, 6, 14) |
| w2 | Liberale (2, 16) |
| w3 | Sozialisten (3, 18) |
| w4 | Grüne (17) |
| w5 | Kommunisten (4, 5, 19) |
| w6 | Nationalisten, Autokraten, Monarchisten (20–23) |

Dazu kommt `EU_vote_hist`: ein Bonus, wenn „historischer Fokus“ an ist.

**Eine neue Agenda braucht genau die sieben Stellen, die auch jede MD-Agenda hat:**
1. Eintrag ins Startarray, oder später per Ergebnis-Effekt
2. Vorbedingung in `eu_parliament_available_reforms_button_click_enabled` (`01_european_union_guis.txt:4601ff`)
3. PP-Kosten im Klick-Effekt (`:4989ff`)
4. Zeile in `EU_init_focus_vote_weights` (`99_EU_voting_scripted_effects.txt:170`)
5. Zweig in `apply_EU_QMV_result` (`:316`) plus Effekt `focus_EU<ID>_QMV_result`
6. `name_of_reform` und Tooltip (`00_EU_voting_scripted_localisation.txt`, `EU_show_display_effects_for_law`)
7. Englische Lokalisierung

**Warum die MD-Ratsregel bleibt:** Für die Sechs (Bevölkerung 1970 grob GER 61, ITA 54, FRA 51, HOL 13, BEL 10, LUX 0,3 Mio.) verhält sich die MD-Regel fast wie die historische Sperrminorität (6 von 17 Stimmen):
- Blockieren können: ein Großer plus ein Mittlerer, oder zwei Große.
- Nicht blockieren kann: ein Großer plus Luxemburg.
- Einzige Abweichung: Benelux allein blockiert über die 55-%-Staatenhürde, historisch konnte es das nicht.

**Die Regel bleibt deshalb unverändert.**

---

## 2. Startzustand 1970 (Stufe 1)

| Element | MD-Mechanik (unverändert) | 1970-Wert | Hook |
|---|---|---|---|
| **Mitglieder** | Idea `EU_member` per History (MD macht das im Block `2000.1.1`), dazu Array-Einträge im Startup | FRA, GER, ITA, BEL, HOL, LUX | `add_ideas = EU_member` im 1970-Snapshot der sechs History-Dateien; Startup trägt nur diese sechs ins Array ein |
| **Startup** | `on_startup_euu_action` (`99_eu_scripted_effects.txt:613`) | 1970-Datenzweig | `if = { limit = { IMP_is_1970_scenario = yes } COLDWAR_EC_1970_startup_data = yes } else = { …MD-Daten 2000… }` |
| **Strafideen** | `foreign_data_kraken`, `asylum_shopping` (`:777-783`) | entfallen 1970 | Teil des Datenzweigs |
| **Agenden** | Startarray (`:699-751`) | nur 1970-Agenden (§3). Die MD-Agenden 101–112, 201–208, 301–308, 401–408 und 601+ kommen erst mit „Treaty on European Union“ (125) ins Array | Datenzweig plus Ergebnis-Effekt 125 |
| **Europeanism** | Startwerte (`:810-831`), Drift, Kampagnen | Mitglieder: GER 0,80, ITA 0,85, BEL/HOL/LUX 0,85, FRA 0,60. Kandidaten: ENG 0,55, IRE 0,70, DEN 0,65, NRY 0,45. Neutrale 0,35, SPR/POR/GRE 0,40, TUR 0,50, SOV 0,05 (Werte zum Kalibrieren) | Datenzweig |
| **Kampagnen** | `stop_pro_european_campaign` / `stop_euroscepticism_campaign` sperren die KI bis zum 15.1.2000 (`99_EU_scripted_triggers.txt:621, 640`) | ab 1970 aktiv | Datumsbedingung um den 1970-Start ergänzen |
| **Parlament** | `election_EU_Parliament`: Sitzzahl und Klammern je nach Vertragsflag (732/750/1000; `:1582-1640`) | **142 Sitze, Klammer 6–36** (ergibt etwa 36/36/36/10/7/6). Nach dem Beitritt der Neun 198, nach der Direktwahl (123) 410 mit Klammer 6–81 | zusätzliche Stufen in derselben `if`-Kette, gesteuert über Flags der 1970-Agenden |
| **Erste Wahl** | `EUelection.2` beim Start (Delegationen nach `party_pop_array`), `EUelection.1` nach 1625 Tagen | `.2` beim Start bleibt (Delegationen der nationalen Parlamente). **`.1` erst nach Agenda 123** | Datenzweig |
| **Fraktionsnamen** | `defined_text` mit Datumsweichen (`00_EU_parliament_scripted_localisation.txt:160ff`) | bis 1979: Christian-Democratic Group, Socialist Group, Liberal and Allies Group, European Democratic Union (Gaullisten), ab 1973 Communist and Allies sowie European Conservative Group | zusätzliche `text = { trigger = { date < … } }`-Zeilen, MD-Muster |
| **Ämter** | 11 Ämter als Ideas, freigeschaltet über globale Flags (`treaty_of_lisbon`, `EU_foreign_minister` …) | Kommission frei, BEL (Rey) bis 30.6.1970 als Timed Idea. Parlamentspräsident frei ab Start. Ratspräsident ab Agenda 122. „High Representative“ ab 121 (als *EPC Chair* lokalisiert). EZB ab 222 (als *EMS Board* lokalisiert). Frontex, Army, Navy, UN und POTEF bleiben gesperrt | jeweils `OR` mit dem 1970-Flag in den `…_click_enabled`-Bedingungen (`01_european_union_guis.txt:170ff`) |
| **Haushalt** | Beitrag = BIP × Abrufsatz; 44/44/6/6; Abschluss nur durch den EZB-Präsidenten (`EU_voting_decisions.txt:476, 495, 582, 601`) | Abrufsatz 0,6 %, Aufteilung 80/8/6/6 (Agrar dominiert). **Bis Agenda 222 schließt der Kommissionspräsident den Haushalt ab** | Datenzweig plus `OR` im EZB-Riegel |
| **Euro** | `EU_join_the_euro_decision`, `joining_the_euro`, Euro-Idea im Reservewährungsgesetz | erst nach Agenda 223. Die Euro-Idea wird statt über das Datum (vor 1999) über das 223-Flag freigeschaltet. `joining_the_euro` tauscht auch `deutsche_mark` | Bedingung in Decision und Idea; eine Zeile in `joining_the_euro` |
| **Name** | MD-Loc „European Union“ | „European Communities“ bis Agenda 125, danach „European Union“ | Scripted Loc mit Flagweiche wie bei den Fraktionsnamen |
| **Werteverstoß** | `check_breach_of_EU_value`: keine Wahlen +5, Diktatur +5 …; Beitritt nur unter 3 | **unverändert.** Diese Regel *ist* die Demokratie-Klausel von 1970: Franco, Caetano und die Junta können nicht beitreten | keiner |
| **Austritt** | Art.-50-Mission, `leaving_EU` | unverändert (nur als „Withdrawal“ lokalisiert) | Loc |
| **Endspiele** | 110–112 (USoE/POTEF) mit Vorgänger-Kette | kommen erst über 125 (oder alt-historisch 128) ins Array | keiner |

**MD-Bugs, die wir dabei beheben** (alle verifiziert):
- IPA-Timeout 5 statt 180 Tage (`EU_voting_decisions.txt:1892`)
- falsche Variablennamen in `EU_influence_on_leader_of_foreign_policy_25_percent`
- `EU_external_sov_chi_influence_50` ist wahr, sobald SOV kein Mitglied ist
- Kandidaten können im Rat mitklicken
- POTEF-Modifier wirken nur beim Präsidenten
- `FRA_nuclear_eu` nutzt den Tag `AUT` statt `AUS`

**Spanien:** Das Event `SPR_1970.227` vergibt `EU_member` heute direkt. Künftig setzt der Spanien-Fokus nur das Antragsflag, und der Beitritt läuft über den MD-Weg: Agenda 626 macht Spanien zum Kandidaten, danach folgt die MD-Decision `EU_apply_for_membership`.

---

## 3. Agenden-Katalog 1970 im MD-Nummernschema

**Freie Nummernblöcke** (MD belegt 101–112, 201–208, 301–308, 401–408, 601–611, 650–660, 998/999; 703 ist verwaist):

| Block | Thema |
|---|---|
| 120–129 | Verträge |
| 220–229 | Wirtschaft und Währung |
| 320–329 | Verteidigung (vorerst zurückgestellt) |
| 620–629 | Erweiterung und Assoziierung |

**KI-Gewichte** in der Reihenfolge w1 Konservative / w2 Liberale / w3 Sozialisten / w4 Grüne / w5 Kommunisten / w6 Nationalisten, dazu `hist`. Mit `hist = 100` folgt die KI bei „historischem Fokus“ der Geschichte.

### 3.1 Verträge und Institutionen

| ID | Agenda (EN) | Datum hist. | Vorgänger | PP | Wirkung (MD-Helfer) | KI w1–w6 / hist |
|---|---|---|---|---|---|---|
| 120 | **Own Resources Decision** | 21.4.1970 | – | 200 | Abrufsatz +0,2; `EU_europeanism_change` +0,02 | 50/50/50/25/−25/−25 / 100 |
| 121 | **Davignon Report: European Political Cooperation** | 27.10.1970 | – | 200 | Flag `EU_foreign_minister`: Amt „EPC Chair“ (Einfluss und Meinung wie bei MD) | 25/25/25/25/−25/−25 / 100 |
| 122 | **The European Council** | Dez. 1974 | 121 | 200 | schaltet das Amt Ratspräsident frei; Gipfel-News | 25/25/25/25/−25/−25 / 100 |
| 123 | **Direct Elections Act** | 1976, Wahl 6/1979 | 122 | 200 | Flag Direktwahl, 410 Sitze; `EUelection.1` nach ca. 1080 Tagen, danach MD-Fünfjahresrhythmus | 25/50/50/50/0/−25 / 100 |
| 124 | **Single European Act** | 1986 | 123, 225 | 300 | MD-Idee „Binnenmarkt“ (Handel/Konsumgüter), Europeanism +0,03 | 50/50/25/25/−25/−25 / 100 |
| 125 | **Treaty on European Union** | 1992 | 124, 223 | 300 | Name „European Union“; MD-Agenden 101–112, 201–208, 301–308, 401–408 und 601+ ins Array | 25/25/25/25/−25/−25 / 100 |
| 126 | **Schengen Agreement** | 14.6.1985 | 123 | 200 | Grenz-Idee mit den MD-Modifiern von Frontex (`border_control`/`migration`) | 25/50/25/25/−10/−25 / 100 |
| 127 | *(alt)* **A Union of States (Fouchet)** | – | 121 | 300 | sperrt die föderalen Endspiele über `EU_drop_rival_endgame`; Europeanism der Mitglieder −0,02 | 25/0/0/0/−25/50 / 0 |
| 128 | *(alt)* **The Spinelli Constitution** | – | 123 | 300 | setzt 110 (Föderalisierung) direkt ins Array; Europeanism +0,05 | 0/50/50/50/0/−50 / 0 |

### 3.2 Wirtschaft und Währung

| ID | Agenda (EN) | Datum hist. | Vorgänger | PP | Wirkung | KI w1–w6 / hist |
|---|---|---|---|---|---|---|
| 220 | **The Werner Plan** | 22.3.1971 | 120 | 200 | Idea für alle Mitglieder (Stabilität +, Zinsspielraum −) | 25/25/25/25/−25/−25 / 100 |
| 221 | **The Currency Snake** | 24.4.1972 | 220 | 0 | Idea für alle Mitglieder (Inflation −, Exportbonus). Decision „Leave the Snake“ pro Land, wie UK 1972 und FRA 1974 | 25/25/10/10/−25/−25 / 100 |
| 222 | **European Monetary System** | 13.3.1979 | 221 | 200 | Flag schaltet das EZB-Amt als „EMS Board“ frei; Haushaltsabschluss geht dorthin | 25/25/25/25/−25/−25 / 100 |
| 223 | **Economic and Monetary Union** | 1989–92 | 222 | 300 | schaltet den MD-Euro frei (Decision und Idea). **Früh beschlossen = alt-historisch „Werner gelingt“** | 10/25/25/25/−25/−25 / 100 |
| 224 | **The Mansholt Plan** | 1968–72 | – | 0 | Agrar-Anteil am Haushalt −10, Bauernmeinung −, Stabilität −2 % für 180 Tage, später Produktivität + | −10/25/25/10/−25/−25 / 0 |
| 225 | **European Regional Development Fund** | 3/1975 | 120 | 200 | Wachstums-Anteil +8 (über `set_EU_expenditure`): ITA, IRE und ENG werden Nettoempfänger | 10/10/25/25/0/−25 / 100 |
| 226 | **Common Fisheries Policy** | 20.10.1970 | – | 0 | gleicher Zugang; Europeanism −0,05 in NRY, IRE, DEN und ICE (Nichtmitglieder) | 25/25/10/10/−10/−10 / 100 |

### 3.3 Verteidigung (zurückgestellt)

Laut Entscheidung vom 18.10.2026 vorerst kein Thema: keine EU-Verteidigungs- und keine Atom-Agenden für 1970. Die MD-Verteidigungsagenden 301–308 und die EDU bleiben wie alle modernen MD-Agenden bis „Treaty on European Union“ (125) gesperrt.

### 3.4 Erweiterung und Assoziierung (MD-Weg: Agenda → `EU_candidate` → `EU_apply_for_membership`)

| ID | Agenda (EN) | Datum hist. | Bedingung | PP | Wirkung | KI w1–w6 / hist |
|---|---|---|---|---|---|---|
| 620 | **The First Enlargement** | Eröffnung 30.6.1970, Beitritt 1.1.1973 | – | 300 | ENG, IRE, DEN, NRY: `EU_candidate` plus `set_eu_candidate_europeanism_floor` (genau wie `focus_EU601_QMV_result`) | 25/25/25/25/25/−25 / 100 |
| 621 | **Preferential Agreements** | 29.6.1970 | – | 0 | SPR, ISR: `set_improved_trade_agreement` mit jedem Mitglied | 25/10/−10/−10/−25/25 / 100 |
| 622 | **Mediterranean Association** | MLT 1970, CYP 1972 | – | 200 | MLT, CYP (MOR, TUN): Flag `EU_associate`, Handelsabkommen, IPA-berechtigt | 25/25/25/25/0/−25 / 100 |
| 623 | **EFTA Free Trade Agreements** | 22.7.1972 | 620 | 200 | AUS, SWI, SWE, POR, ICE, FIN, NRY (falls draußen): Handelsabkommen | 25/50/25/25/0/−25 / 100 |
| 624 | **Additional Protocol with Turkey** | 23.11.1970 | – | 200 | TUR: Handelsabkommen, IPA-berechtigt | 25/10/10/0/−25/0 / 100 |
| 625 | **The Greek Enlargement** | 1975–81 | GRE Werteverstoß < 3 | 300 | GRE: `EU_candidate` | 25/25/25/25/25/−25 / 100 |
| 626 | **The Iberian Enlargement** | 1977–86 | SPR und POR Werteverstoß < 3 | 300 | SPR, POR: `EU_candidate` | 25/25/25/25/25/−25 / 100 |
| 627 | **The Neutral Enlargement** | 1989–95 | 125 *oder* Spannung niedrig | 300 | AUS, SWE, FIN (SWI, NRY): `EU_candidate`; Cold-War-Event an SOV (Vorbehalt) | 25/25/25/25/25/−25 / 100 |
| 628 | **The Turkish Application** | 1987 | 624, TUR Werteverstoß < 3 | 300 | TUR: `EU_candidate` | −25/25/25/25/25/−25 / 0 |

**Beitritt nach dem Beschluss:** Er läuft exakt über die MD-Decision `EU_apply_for_membership`:
- Bedingungen: Werteverstoß unter 3, kein Krieg, Europeanism über 0,79 (Spieler) bzw. 0,69 (KI)
- **Die Europeanism-Schwelle ist das Referendum.** Ein menschlicher Norweger muss Europeanism mit der MD-Kampagne „pro-europäisch national“ (50 PP + 0,2 % BIP) hochziehen.
- Die KI-Norweger erreichen 0,69 nicht und bleiben draußen, wie 1972.
- KI-Beitrittstermin für ENG/IRE/DEN: `ai_will_do`-Datumsfaktor 1.1.1973, nach dem MD-Muster für 2004/2007/2013.

**Optional im MD-Stil:** ein Referendums-Event beim Antrag für NRY, DEN und IRE. Es ist ein `random_list`, gewichtet nach Europeanism, wie `DEN_distance_from_the_eu` im MD-Dänemarkbaum.

**Assoziierte:** Das Flag `EU_associate` (einzige neue Statusmarke) macht ein Land IPA-berechtigt (Heranführungshilfe, MD). Ein **Einfrieren** ist die vorhandene MD-Idea `EUU_subsidies_suspended`:
- Griechenland startet assoziiert *und* eingefroren (Junta).
- Aufgetaut wird über die MD-Decision zum Aufheben, sobald Griechenland demokratisch ist. Die Decision zielt heute nur auf Mitglieder, ihr Ziel-Trigger muss also um `EU_associate` erweitert werden.
- Die Türkei startet assoziiert (Ankara 1963).

---

## 4. Andockpunkte in unseren 1970-Inhalten (alles über MD-Helfer)

| Land | Heute | Neu |
|---|---|---|
| **SPR** | Fokus „Accession“ gibt `EU_member` direkt (`SPR_1970.227`) | Der Fokus setzt das Antragsflag, das Agenda 626 voraussetzt. Der Beitritt läuft über `EU_apply_for_membership`. Das Präferenzabkommen kommt über Agenda 621 |
| **GRE** | `COLDWAR_GRE_1970_european_censure`; Fokusse `nd_13`/`foreign_6` gehen an ENG | Start: assoziiert und eingefroren. `nd_13` beantragt das Auftauen (MD-Decision), `foreign_6` setzt das Antragsflag für Agenda 625 |
| **CYP** | Assoziierungsangebot geht an ENG | Der Fokus setzt die Vorbedingung für Agenda 622 |
| **TUR** | kein Inhalt | Start assoziiert. Ein Putsch erhöht über die MD-Logik den Werteverstoß, eingefroren wird per MD-Decision |
| **SOV** | – | Die MD-Kampagne „EU-weite Euroskepsis“ ist für Nichtmitglieder offen (Anti-EG-Propaganda). Event bei Agenda 627 (Neutrale) mit Spannung über `mdcw_cw_add_tension` |
| **Neutrale** | Idea `mdcw_ni_armed_neutrality` | Bis Agenda 627 nur Handelsabkommen (623) |
| **Alle Länder** | – | Nationale Fokusse nutzen nur MD-Helfer: `europeanism_change`, `EU_candidate`, Antragsflags |

---

## 5. Alt-historische Pfade (alle durch dieselbe MD-Pipeline)

| Pfad | Wie er entsteht |
|---|---|
| **Drittes französisches Veto** | FRA (plus ein Mittlerer) stimmt im Rat gegen 620. Die Agenda scheitert und kann nach Ablauf des Cooldowns erneut eingebracht werden |
| **Norwegen tritt bei** | Ein menschliches NRY zieht seine Europeanism über 0,79 (Kampagnen) |
| **UK-Austritt 1975** | Ein menschliches ENG startet Art. 50 (MD), Ergebnis Austrittsvertrag oder No-Deal |
| **Werner gelingt** | Agenda 223 wird früh beschlossen, der Euro kommt vor 1999 |
| **Europa der Vaterländer** | Agenda 127; die föderalen Endspiele sind dann gesperrt |
| **Föderation** | Agenda 128 → 110 → 112 (POTEF, ohne Annexion) bzw. 111 (USoE, MD-Annexion mit `EUvote.5`-Zustimmung) |
| **Frühe Süderweiterung** | Demokratisierung senkt den Werteverstoß, dann 625/626 sofort einbringen |
| **Türkei als Mitglied** | 628 |
| **Zerfall** | Mehrere Austritte über Art. 50, wenn Europeanism einbricht (MD-KI-Austritt bei < 0,4) |

---

## 6. Umsetzung in drei Stufen

1. **Stufe 1, Startzustand (2–3 Tage):**
   - History der Sechs
   - Startup-Datenzweig
   - Sitzstufen und Fraktionsnamen
   - Ämter-Freischaltung
   - Haushalts- und Euro-Riegel
   - Name „European Communities“
   - Kampagnen-Datum
   - Spanien-Fix
   - MD-Bugfixes

   Ergebnis: eine saubere EG der Sechs, moderne Agenden ausgeblendet.
2. **Stufe 2, historische Agenden (ca. 1 Woche):** 120–126, 220–226, 620–626, mit KI-Gewichten, Loc und News-Events im `EU_news`-Stil.
3. **Stufe 3, Länder-Hooks und alt-historische Agenden:** GRE/CYP/TUR/SPR, 127/128, 627/628, optionale Referendums-Events.

**Dateien:**
- Neue Logik in `common/scripted_effects/COLDWAR_EC_1970_effects.txt`, `…_triggers.txt` und `localisation/english/COLDWAR_EC_1970_l_english.yml`.
- In MD-Dateien nur kurze, mit `# COLDWAR` markierte Hook-Zeilen: Startup-Weiche, Dispatcher-Zeilen, GUI-Bedingungen, Sitz-`if`-Kette, Ämter-`OR`, Haushalts-`OR`, Euro-Bedingung.

---

## 7. Zu entscheiden

**Luxemburger Kompromiss – was gemeint ist:**
- **Historisch:** Seit 1966 konnte jedes EG-Mitglied eine Mehrheitsabstimmung im Rat stoppen, indem es „sehr wichtige nationale Interessen“ geltend machte. Dann wurde nicht abgestimmt, bis alle einverstanden waren. Faktisch hatte damit jedes Land ein Veto. Frankreich hatte das 1965/66 mit der „Politik des leeren Stuhls“ erzwungen. Erst 1982 wurde das UK erstmals trotzdem überstimmt.
- **Im MD-System heute:** Der Rat entscheidet nur per Mehrheit (65 % Bevölkerung, 55 % der Staaten). Ein Land, das überstimmt wird, kann nichts tun.
- **Vorschlag:** eine einzige Decision „Invoke the Luxembourg Compromise“. Sie ist nur sichtbar, während im Rat abgestimmt wird, und kostet z. B. 50 PP sowie Europeanism −0,03 im eigenen Land. Wer sie nimmt, lässt die laufende Agenda scheitern, egal wie die Mehrheit aussieht. Die KI nutzt sie nicht; das Vorbild in MD ist die französische Decision `FRA_veto_eu_federalization`.
- **Rollenspiel-Effekt:** Ein Gaullist-Frankreich kann z. B. die Erweiterung um Großbritannien blockieren, bezahlt das aber politisch.
- **Ohne die Decision** braucht ein Blocker Verbündete: ein Großer plus ein Mittlerer (siehe §1).

**Offene Punkte:**
1. Luxemburger Kompromiss als Decision: **ja oder nein?** Das gehört zu Stufe 2.
2. **Stufe 2 freigeben?**
