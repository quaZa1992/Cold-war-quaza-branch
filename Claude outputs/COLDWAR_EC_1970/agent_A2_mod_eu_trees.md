# Agent A2: EU-Fokusbäume und Länder-Hooks im Mod (Stand 18.10.2026)

Reine Lese-Analyse des Workspaces `mdcoldwar` (gestagte Kopien unter `/mnt/user-data/uploads/mdcoldwar/`). Nichts auf dem Nutzer-PC geändert. Kein Spieltest.

**Kennzeichnung**
- **[V]** verifiziert: im gestagten Code gelesen, Datei:Zeile angegeben.
- **[V-stat]** statisch verifiziert über alle gestagten Dateien (Grep), aber nicht über den ganzen Mod.
- **[A]** vermutet / abgeleitet / Engine-Verhalten, nicht im Mod belegt.
- **[P]** Projekt-Doku des Teams (`claude/mdcw_union_missions_implementation_plan.md`), nicht von mir neu geprüft.

Alle Pfade relativ zu `mod/mdcoldwar/`. Fokusnamen in eckigen Klammern sind die englische Lokalisierung.

---

## 0. Kurzfassung

1. Im 1970-Start erreicht **kein** Land einen der EU-Shared-Bäume. FRA, GER, ITA, BEL, HOL, LUX, ENG, IRE, DEN, NRY (und TUR, AUS, SWI, SWE, FIN, POR, ICE, MLT) laden per History den generischen Baum `mdcw_1970_generic_focus`. Der hat **keine** `shared_focus`-Zeile und **keinen** EG-Inhalt. [V]
2. `USoE001` (United States of Europe) und `POTEF001` (President of the European Federation) hängen nur in den 2000er-MD-Bäumen und in `00_generic.txt`. Beide sind zusätzlich an ein bestandenes EU-Votum gebunden (111 bzw. 112). [V]
3. Der Benelux-Baum (`03_benelux_shared.txt`) ist ein echter `joint_focus`-Baum (33 Fokusse) mit sauberer Mitglieds-Mechanik. Er hängt aber nur in `05_netherlands.txt` und `00_generic.txt`, also 1970 unerreichbar. [V]
4. EG-Inhalt in **aktiven** 1970-Bäumen gibt es nur bei SPR (Antrag 1977 / Beitritt), GRE (Assoziierung reaktivieren, „European Dossier“) und CYP (Assoziierungsangebot). [V]
5. Wiederverwendbar sind vor allem: die Joint-Mechanik von Benelux, das Angebots-Event-Muster der GRE/CYP-1970-Bäume, die Europeanism-Helfer, `EU_member` mit `on_add`, die POTEF-Wahl, die französischen „Invest in …“-Decisions, die Referendums-`random_list` aus DEN/HOL/SWE und die Dänemark-/Norwegen-Nordic-Fokusse. Anachronistisch sind die meisten Effekte von USoE (Kreuzzüge, Weltherrschaft, KI-Regierung, Monarchie) und große Teile von POTEF (Trump, Drohnen, Seidenstraße, Annexionen von Separatistenstaaten).

---

## 1. Die geteilten EU-Bäume

### 1.1 Einbindung (wer hat `shared_focus = USoE001 / POTEF001 / BNL_benelux_union_treaty`)

| Host-Baum (Datei:Zeile) | Tree-ID | USoE001 | POTEF001 | BNL | Aktiv 1970? |
|---|---|---|---|---|---|
| `common/national_focus/00_generic.txt:15-16, 31` | `generic_focus` | ja | ja | ja | nein (`country = { base = 0 }`, Z. 5) |
| `05_france.txt:20217-20218` | `france_focus` | ja | ja | – | nein |
| `05_germany.txt:25722-25723` | `germany_focus` | ja | ja | – | nein |
| `05_italy.txt:23430-23431` | `italy_focus` | ja | ja | – | nein |
| `05_netherlands.txt:16-17, 20` | `netherlands_focus` | ja | ja | ja | nein |
| `05_united_kingdom.txt:22808-22809` (+ Commonwealth Z. 11) | `united_kingdom_focus` | ja | ja | – | nein |
| `05_denmark.txt:18013-18014` | `denmark_focus` | ja | ja | – | nein |
| `05_norway.txt:3851-3852` | `norway_focus` | ja | ja | – | nein |
| `05_sweden.txt:20336-20337` | (sweden) | ja | ja | – | nein |
| `05_switzerland.txt:7-8` | `switzerland_focus` | ja | ja | – | nein |
| `05_finland.txt:3278-3279` | `finland_focus` | ja | ja | – | nein |
| `05_greece.txt:9-10` | `greece_focus` | ja | ja | – | nein |
| `05_spain.txt:12-13` | `spanish_focus` | ja | ja | – | nein |
| `turkey.txt:5-6` | `turkey_focus` | ja | ja | – | nein |
| `mdcw_1970_generic_focus.txt` | `mdcw_1970_generic_focus` | **nein** | **nein** | **nein** | **ja** |
| `spain_1970.txt`, `COLDWAR_GRE_1970_focus.txt`, `COLDWAR_CYP_1970_focus.txt`, `USA_1970.txt` | 1970-Eigenbäume | nein | nein | nein | ja |
| `uk_1985.txt:11`, `GER_1985.txt`, `ireland_1985.txt`, `turkey_1985.txt` | 1985-Bäume | nein (UK nur Commonwealth) | nein | nein | nur 1985 |

Alle Zeilen [V] (Grep über die gestagten Fokusdateien).

### 1.2 USoE: „United States of Europe“ (`01_EU_USoE_shared.txt`, 90 Fokusse, 3919 Zeilen)

**Eintritt und Sichtbarkeit [V]**
- `USoE001` [Constitute the new European Nation], Z. 2. Position x 21 / y 18 mit **33 tag-basierten Offsets** (Z. 9-172, z. B. FRA +14/−10, GER +63/+7, SWI −75/−17, EST −93/−1). NRY steht doppelt (Trigger Z. 81 und Z. 121).
- `allow_branch` (Z. 176-283): `is_in_array = { global.EU_passed_votes value = 111 }` **und** eine Tagliste mit rund 94 `original_tag`-Einträgen (u. a. ABK, DPR, LPR, CAT, SCO, KOS: viele 1970 nicht existent; SOV nur als Mitglied) **und** nicht `GAME_RULE_eu_disabled`.
- `available` (Z. 287-294): Flag `USoE` + Votum 111.
- `completion_reward` (Z. 298-308): `remove_ideas = EU_member`, +100 PP.
- Das Votum 111 läuft in `common/scripted_effects/99_EU_voting_scripted_effects.txt:406` (`focus_EU111_QMV_result`): Ablehner verlieren `EU_member`, alle übrigen Mitglieder werden über `global.USoE_formation_members` annektiert, Technologien, Generäle, Schatz und Schulden gehen auf den Gründer über. 111 und 112 stehen schon beim Start in `global.EU_potential_votes` (`99_eu_scripted_effects.txt:750-751`).

**Zweige und Inhalt [V] (Zeilen = Fokusbeginn)**

| Zweig | Fokusse (Zeile) | Inhalt / typische Effekte | 1970-Bewertung |
|---|---|---|---|
| Gründung | 001 (2), 002 [A European Officer Corps] (320), 003 [European Political Parties] (345), 004 [European Patriotism] (370), 005 [The New Great Game] (396), 006 [Europe's Heart and Soul] (423) | `update_EU_military_leaders`, `update_EU_country_leaders`, Idea `european_spirit` (+15 % PP, +5 % Stabilität, `europeanism_drift`; `common/ideas/EU_ideas.txt:301`), Decision `EU_USoE_capital_of_europe` (`EU_USoE_decisions.txt:4`) | **umbaubar**: 002 → integrierte EVG-Kommandostruktur; 003 → europäische Parteienbünde (EVP, Sozialdemokraten, Liberale, 1974-76); 004 → `european_spirit` als Föderalisten-Idee; Hauptstadt-Decision → Sitzfrage Brüssel/Straßburg/Luxemburg |
| Sphären | 100 [A Game of Spheres] (450), 101-103 (477-539: Kriegsziele `puppet_wargoal_focus` gegen USA/SOV/CHI), 104 [A Heart of Iron] (570) | Kriegsziele gegen Supermächte | **anachronistisch / MP-untauglich** |
| Koexistenz | 200 [Peaceful Coexistence] (603), 201 [America First] (630), 202 [Russosphere] (665), 203 [Shinosphere] (707), 204 [Eurosphere] (742) | Nichtangriffspakt-**Angebote** per `USoEevent.1` an USA/SOV/CHI (Ja/Nein, `events/EU_USoE_events.txt:2-25`), Decision `EU_USoE_create_eurosphere_decision` (`EU_USoE_decisions.txt:79`) | **direkt umbaubar** für „Dritte Kraft“/Entspannung: MP-konform, weil der Empfänger entscheidet |
| Zivilisationskonflikt | 300 (770), 301 [The Rest of the West] (800: `NATO_leave`, Z. 820), 302-310 (836-1212: Kriegsziele gegen TUR, SYR, LEB, HEZ, ISR; „Westernize“ für Nordafrika), 311-313 (1257-1354), 320-325 (1383-1559, u. a. 325 [Operation Unthinkable 2.0]: `annex_everything` gegen SOV), 305 [Eurasian Alliance] (974: Bündnisangebot `USoEevent.2`) | Kreuzzug-, Annexions- und Verwestlichungsziele | **anachronistisch**; nur 305 (Bündnisangebot, Event mit Ja/Nein) als Technik verwendbar |
| Innenpolitik liberal | 400 [The Torch of Freedom] (1596), 401 [Digital Democracy] (1639), 404 [AI Government] (1749: Idea `USoE_AI_government`) | Parteipopularität, Ideas | 400 umbaubar; 401/404 **anachronistisch** |
| Innenpolitik kommunistisch | 402 [Hammer and Sickle] (1680), 403 [EUSSR] (1717: `set_cosmetic_tag = USoE_com`, Wahlen aus) | Parteiwechsel | 402 → **Eurokommunismus** (PCI/PCF/PCE 1975-77) als Alt-Pfad; 403 nur als extremer Alt-Endpunkt |
| Grün | 500 [The Green Future] (1779), 501 (1817), 502-510 [Environmental Imperialism] + Weltregionen (1852-2063) | Parteipopularität, globale Flags, Sanktions-Decisions | 500 → „Grenzen des Wachstums“ (1972) möglich; 502-510 **anachronistisch** |
| Monarchie/Imperium | 600-605 (2089-2275), 620-649 (2326-3842: Häuser, Paläste mit `set_capital`, Krönung, [The Holy European Empire]) | Gebäude, Hauptstadtwechsel, Ideas | reiner Alt-Spaß, für 1970 nicht empfohlen |
| Abschluss | 700 [Pax Occidentalis] (3867), 701 [Guardians of World Peace] (3894: `add_ideas` direkt bei USA, SOV, CHI) | Ideas | 701 **MP-Verstoß** (Idea bei fremden Spielern) |

### 1.3 POTEF: „President of the European Federation“ (`02_EU_POTEF_shared.txt`, 74 Fokusse, 7668 Zeilen)

**Eintritt und Sichtbarkeit [V]**
- `POTEF001`, Z. 2, Position relativ zu `USoE001` (x +27). `allow_branch` (Z. 13-117): globales Flag `european_federation` + Tagliste. `available` (Z. 120-125): Votum 112. Das Flag setzt `focus_EU112_QMV_result` (`99_EU_voting_scripted_effects.txt:875-876`). **Keine Annexion** (anders als 111).
- Fast alle Folgefokusse: `available = { has_idea = EU_president … }` und `bypass = { any_of_scopes = { array = global.EU_member has_completed_focus = X } }`. Das heißt: Der amtierende Präsident macht den Fokus, für alle anderen Mitglieder wird er übersprungen („einer für alle“).
- Regionsbedingungen über `EU_member_is_<region>` / `POTEF_is_<region>` in `common/scripted_triggers/99_EU_scripted_triggers.txt:945-1060` (alpine, benelux, iberian, british, nordic, mediterranean, balkan, black_sea, caucasus, visegrad, baltic, eastern).
- Präsidentenwahl: `POTEF_election` / `election_POTEF_in_member_state` (`99_eu_scripted_effects.txt:1024-1063`), bevölkerungsgewichtete Parteistimmen aller Mitglieder; Decisions in `common/decisions/EU_POTEF_decisions.txt:306-567`.

**Typischer Effekt [V]** (Beispiel `POTEF150` [German Doctrine], Z. 513-567):
```
if = { limit = { has_idea = EU_member NOT = { has_dynamic_modifier = { modifier = POTEF_dynmod_army } } }
	add_dynamic_modifier = { modifier = POTEF_dynmod_army } }        # nur ROOT
for_each_scope_loop = { array = global.EU_member
	add_to_variable = { POTEF_army_armor_attack_factor = 0.10 } … }   # alle Mitglieder
```

**Befund (Bug) [V-stat]:** Die dynamischen Modifikatoren `POTEF_dynmod_army/_navy/_air/_adm` (`common/dynamic_modifiers/05_POTEF_dynamic_modifiers.txt:1-70`) werden **nur** im Scope des abschließenden Präsidenten hinzugefügt. Die Variablen der anderen Mitglieder steigen, aber ohne den Modifikator wirken sie nicht. In keiner gestagten Datei (common/, events/) gibt es eine andere `add_dynamic_modifier = { modifier = POTEF_dynmod_* }`-Stelle. Laufzeitwirkung nicht getestet.

**Zweige [V]**

| Zweig | Fokusse (Zeile) | Inhalt | 1970-Bewertung |
|---|---|---|---|
| Alpen | 100 (135), 101 (187) | Infanterieverteidigung, Gelände; Erneuerbare | 100 umbaubar (Gebirgsjäger-Standard), 101 anachron. |
| Umwelt-Imperialismus | 102-110 (250-484) | globale Flags | anachronistisch |
| Deutsch | 150 [German Doctrine] (513), 151 [Empire of Trade] (570) | Panzerboni; `trade_opinion_factor`, `opinion_gain_monthly_factor` | 150 → Leopard/Standardisierung (Werte halbieren); **151 → Gemeinsame Handelspolitik** |
| Französisch | 200 [French Doctrine] (626), 201 [Imperial Power] (683), 202 [Empire of Freedom] (740) | mech./mot. Boni; 201 senkt Einfluss von USA/SOV/CHI in allen Mitgliedern um 3 %; 202 Geheimdienst, Freiwillige | 200 umbaubar; **201 → EPZ „mit einer Stimme sprechen“** (MP-heikel: wirkt auf Einfluss fremder Supermacht-Spieler) |
| Amerika | 203 (783, braucht `EDU`), 204 [NATO Legacy] (819: `USA = { add_ideas = EDU_major_non_EU_ally }`), 205 [Trump's Legacy] (859, `date > 2017.1.20` Z. 877), 206 (913) / 207 (970) Kriegsziele | | 204 Idee „atlantischer Pfad“ ok, aber Idea bei USA = MP-Verstoß; 205-207 **anachronistisch** |
| Benelux | 250 [Benelux Doctrine] (1106), 251 [Liberal Legacy] (1169: Konsumgüter −5 %), 252 [Safeguard the old Trade Routes] (1210), 253 [Indonesia] (1503) | Aufklärung/Fallschirm; Gebäude in Fremdstaaten | 251 → Zollunions-Dividende; 252/253 → **Eurafrika-/Entwicklungsprojekte** (nur mit Zustimmung des Empfängers) |
| Iberisch | 300 (1744), 301 [Latin Cousins] (1800), 302-306 (1924-2602: Bauten in MEX, COL, PAN, URG, BRA) | | Lateinamerika-Kooperation, später (SPR/POR nach Beitritt) |
| Britisch | 350 (2752), 351 (2806), 352 [Commonwealth Legacy] (3077), 353-355 (CAN/AST/NZL, 3139-3231), 356 [Safeguard the North Sea] (3278), 357-359 (Malaya/Singapur, 3587-3727), 360 [Guarantee Hong Kong] (3785) | | 352-355 → **UK-Beitrittskapitel „Commonwealth-Handel“** (NZ-Butter, Zucker) |
| Nordisch | 400 (3845), 401 [Safeguard the Arctic] (3898) | Winter-/Marineboni, Küstenbauten | umbaubar (NATO-Nordflanke) |
| Mittelmeer | 450 (4363), 451 [Northern Africa] (4418: **annektiert GNA/GNC/HOR in LBA**, Z. 4555-4569), 452 [Unite Cyprus] (4716: **CYP annektiert NCY, `transfer_state = 812`**, Z. 4795-4806) | | 451 nur ohne Annexion → Eurafrika; 452 **unbrauchbar** (würde den CYP-1970-Komplex überspringen) |
| Balkan | 500 (4865), 501 (4920), 502 [Contest the Silk Road] (5319) | | 502 anachron. |
| Asien | 503-507 (5390-5535: Kriegsziel CHI, Allianzidee für KOR/JAP) | | anachron. / MP-Verstoß (Ideas bei KOR/JAP) |
| Schwarzes Meer | 550 (5573), 551 (5626), 552 [Reintegrate the Breakaway Republics] (6012: Annexion PMR, NOV, ABK, SOO, NKR …), 553 [Rival Russia] (6125), 554 [Operation Charlemagne] (6169: Kriegsziel SOV) | | 552-554 **unbrauchbar** |
| Kaukasus, Visegrád, Baltikum, Osten | 600-601 (6208-6272), 650-652 (6507-6869), 700-701 (7047-7104), 750-753 (7444-7587: 751 [Drone Warfare]) | Infrastruktur/Luftverteidigung in Ost-Mitgliedern | 1970 keine Mitglieder; 751 anachron. |
| Abschluss | 800 [Pax Europaea] (7640: Idea `POTEF_pax_europaea` für alle Mitglieder, +10 % PP) | | Abschlussidee umbaubar |

### 1.4 Benelux (`03_benelux_shared.txt`, 33 `joint_focus`, 1600 Zeilen)

**Mechanik [V]**
- Wurzel `BNL_benelux_union_treaty` (Z. 3): `allow_branch = { is_benelux_country = yes }` (Z. 14), `joint_trigger = { is_benelux_nation = yes }` (Z. 18), `available = { benelux_cooperation_trigger = yes }` (Z. 20). Trigger: `common/scripted_triggers/99_HOL_scripted_triggers.txt:31-43` (alle drei existieren, kein Krieg untereinander) und `MD_Country_Groups_Triggers.txt:1701`.
- `completion_reward` (läuft bei jedem Mitglied) füllt Variablen des Modifikators `BNL_dynmod_union` und den Zähler `BNL_integration`; `completion_reward_joint_originator` (+150 PP, +2 % Stabilität, Z. 31-34); `completion_reward_joint_member` (+50 PP, Z. 36).
- Endpunkt `BNL_treaty_of_union` (Z. 751): braucht `BNL_integration ≥ 100`. Er sendet BEL/HOL/LUX die Angebotsevents `benelux.1/.4/.5` (`events/03_benelux.txt`); erst bei **Annahme** wird der Empfänger Puppet des Organisators. Ablehnung setzt nur ein Flag. **MP-konform.**

**Zweige und 1970-Bewertung [V Inhalte, Bewertung A]**

| Zweig | Fokusse (Zeile) | 1970 |
|---|---|---|
| Wirtschaft | single_market (41), port_cooperation (81), capital_integration (127), north_sea_wind (169), freight_corridors (211), gas_hub (251) | Binnenmarkt, Häfen Rotterdam/Antwerpen, Kapitalmarkt, Güterkorridore **passen** (Benelux-Wirtschaftsunion seit 1960). Gas-Hub mit Groningen-Bezug umbaubar. Windkraft anachron. |
| Forschung | research_cooperation (292, `add_to_tech_sharing_group`), university_network (338), hightech_triangle (367), space_cooperation (414), nuclear_research (464), innovation_area (522) | Raumfahrt → ESRO/ELDO, Kern → Euratom/Mol (BEL) **passen** |
| Politik | benelux_parliament (584), benelux_court (620), shared_foreign_policy (668), political_union (705), treaty_of_union (751) | Interparlamentarischer Rat (1955) und Benelux-Gerichtshof (Vertrag 1965) **passen**; Union als Alt-Endpunkt |
| Militär | benelux_defence (810), air_policing (855), air_defence_command (911), binational_air_command (965), mrtt_fleet (1019), eatc (1061), belux_a400m (1095), f35_cooperation (1134), benesam (1174), admiral_benelux (1229), vlissingen_class (1271), hollandklasse_frigate (1352), aswf_frigate (1426), para_school (1511), csomtg (1555) | fast alles **anachronistisch** (F-35, A400M, MRTT, EATC, Schiffsklassen der 2010er/20er). Ersatz: F-104-Nachfolge (F-16 „Deal of the Century“ 1975), Van-Speijk-/Kortenaer-Fregatten, Tromp-Klasse |

### 1.5 Commonwealth (`Commonwealth_shared.txt`, Team-Datei, 24 Fokusse)

Kein EU-Baum, aber die modernste **Team-Vorlage** für einen Bündnisbaum [V]:
- Offsets nach Host-Baum statt nach Tag: `offset = { … trigger = { has_focus_tree = ENG_1985_focus } }` (Z. 9-48).
- „Einer schaltet frei, alle profitieren“: `COMMONWEALTH_unlock_<focus>_for_members` (`common/scripted_effects/99_Commonwealth_scripted_effects.txt:887ff`) plus globale positive Effekte `COMMONWEALTH_apply_global_secretariat` (Z. 91).
- **Achtung:** `unlock_national_focus` auf Mitglieder verstößt gegen die Team-Regel aus dem Union-Plan („No `complete_national_focus`, `unlock_national_focus` … on members“) [P]. Für den EG-Baum daher `joint_focus` oder GCC-`bypass` nehmen.

---

## 2. Erreichbarkeit 1970

### 2.1 Tree-Auswahl [V]

- Jede Europa-History setzt im 1970-Block `load_focus_tree = mdcw_1970_generic_focus`, geschützt durch `if = { limit = { date < 1985.1.1 } }`:
  - FRA `history/countries/FRA - France.txt:8`, GER `GER - Germany.txt:9` (Hauptstadt Bonn, Z. 5), ITA `:8`, BEL `:8`, HOL `:8`, LUX `:8`, ENG `:8`, IRE `:8`, DEN `:8`, NRY `:8`, SWE `:9`, SWI `:8`, AUS `:8`, FIN `:8`, ICE `:8`, MLT `:8`, POR `:8`, TUR `:8`, sogar EUU `:8`.
  - Eigene Bäume: SPR `SPR - Spain.txt:8` → `SPR_1970_focus`; GRE `GRE - Greece.txt:9` → `COLDWAR_GRE_1970_focus`; CYP `CYP - Cyprus.txt:8` → `COLDWAR_CYP_1970_focus`.
- Gewichte: `mdcw_1970_generic_focus` hat `country = { factor = 0 modifier = { add = 20 IMP_is_1970_scenario = yes } }` (Z. 6-12). `SPR_1970_focus` und `USA_1970_focus` haben `add = 100 tag = X IMP_is_1970_scenario = yes`. Alle MD-2000er-Bäume haben `country = { base = 0 }`.
- `mdcw_load_1970_fallback_tree` (`common/scripted_effects/mdcw_1970_focus_tree_effects.txt:4-30`) schützt nur USA, SPR, LBA, EGY sowie (nur 1970) SOV, CYP, ISR, GRE. Alle anderen bekommen den generischen Baum. Ein neuer Eigenbaum für FRA/ENG usw. muss **dort und in der History** eingetragen werden. Aufrufer dieses Effekts liegen außerhalb der gestagten Dateien [A].
- `EU_member` (Idea) steht in allen Europa-History-Dateien **nur im `2000.1.1`-Block** (FRA Z. 1497, GER 1445, ITA 1172, BEL 372, HOL 763, LUX 193, ENG 1383, IRE 176, DEN 548, GRE 245). 1970 hat also niemand die Idea. Gleichzeitig füllt `on_startup_euu_action` ohne Szenario-Gate `global.EU_member` mit den 15 Ländern von 2000 (`99_eu_scripted_effects.txt:760-774`). Details dazu im Kernsystem-Bericht (`docs/europe_1970_audit/agent_core.md`).

### 2.2 Ergebnis je Land [V]

| Land | 1970-Baum | EU-Shared-Fokus erreichbar? | EG-Inhalt im aktiven Baum |
|---|---|---|---|
| FRA, GER, ITA, BEL, HOL, LUX | generisch | nein | keiner |
| ENG, IRE, DEN, NRY | generisch | nein | keiner |
| SPR | `SPR_1970_focus` | nein | ja: `SPR_1970_apply_to_the_european_communities` (`spain_1970.txt:1240`, Bedingung Demokratie + Konservative an der Macht), `SPR_1970_accession_to_the_european_communities` (Z. 2113). Event `SPR_1970.227` (`events/SPR_1970_events.txt:1672`) macht **einseitig** `add_ideas = EU_member` + Entwicklungsfonds-Idee (2 Jahre) + Europeanism +0,03. |
| GRE | `COLDWAR_GRE_1970_focus` | nein | ja: Idea `COLDWAR_GRE_1970_european_censure` beim Start (`COLDWAR_GRE_1970_tree_effects.txt:18409`, in `COLDWAR_GRE_1970_tree_initialize` ab Z. 18395); `COLDWAR_GRE_1970_nd_13` [Reactivate the Association Framework] (`COLDWAR_GRE_1970_focus.txt:2996`); `COLDWAR_GRE_1970_foreign_6` [A Credible European Dossier] (Z. 8562) mit Angebot an **ENG** (`COLDWAR_GRE_1970_send_foreign_6`, Effekte Z. 18365; Event `COLDWAR_GRE_TREE.142`, `events/COLDWAR_GRE_1970_tree_events.txt:4662`) |
| CYP | `COLDWAR_CYP_1970_focus` | nein | ja: `COLDWAR_CYP_1970_western_association` [Seek Western Economic Association] (Z. 3504), Angebot an **ENG** (`COLDWAR_CYP_1970_effects.txt:4047`, Event `COLDWAR_CYP_1970.1192`) |
| TUR | generisch | nein | keiner (Zusatzprotokoll 23.11.1970 fehlt) |

### 2.3 Europa-/Bündnisinhalt des generischen 1970-Baums [V]

`mdcw_1970_generic_focus.txt` hat 349 Fokusse auf x 0-226 × y 0-7 (gemessen). Header Z. 1-2: „Generated by `tools/generate_1970_generic_focus_tree.py` – edit the generator“. Laut Projekt-Doku liegt der Generator unter `/home/claude/gentools/generic_1970_focus_tree/…` (Header Z. 346-356) [P]; im Mod-Ordner wurde er nicht gefunden (`agent_paths.md`).

Kein `shared_focus`, kein `EU_member`, kein EG-Bezug. Europa-nahe Fokusse sind nur generisch:
- `GEN_1970_foreign_policy_review` (6475) → `GEN_1970_lean_to_the_west` (6750: Timed Idea `generic_western_boost_idea2`), `GEN_1970_non_alignment` (6879), `GEN_1970_peaceful_coexistence` (6694), `GEN_1970_champion_of_detente` (7259).
- `GEN_1970_trade_with_the_neighbours` (6591): Meinung + Einfluss bei Nachbarn, Agrarpreise.
- `GEN_1970_lib_free_trade` (1095), `GEN_1970_sd_ostpolitik` (1625: Spannung −1 über `GEN_1970_change_tension`, `mdcw_1970_generic_focus_effects.txt:40`).

**Konsequenz:** Ein EG-Baum für die Sechs und die Kandidaten muss als `shared_focus`/`joint_focus` an den generischen Baum gehängt werden (eine Zeile im Generator), dazu an `SPR_1970_focus`, `COLDWAR_GRE_1970_focus` (Generator `tools/greece_1970/compile.py`) und `COLDWAR_CYP_1970_focus`. Genau dieses Muster plant das Team bereits für den Unionsbaum (`COLDWAR_UNI_the_union_plan` bei x 232 / y 0 im generischen Baum) [P].

---

## 3. EU-Hooks in den 2000er-Länderbäumen und -Decisions

Grep-Muster: `EU_member`, `EU_*`, `europeanism*`, `eurosceptic*`, `euro`, `eurozone`, `schengen`, `USoE*`, `POTEF*`, `european_*`, `leaving_EU`, `NATO_member`. Ergebnisse [V]; Bewertung [A].

### 3.1 Wichtige gemeinsame Helfer [V]

| Helfer | Ort | Nutzen 1970 |
|---|---|---|
| Idea `EU_member` mit `on_add`/`on_remove` (Array pflegen, `EU_adopt_passed_laws`, `leaving_EU`) | `common/ideas/Organizations.txt:4-38` | Kern für Beitritt; Modifikatoren (−20 % PP usw.) für 1970 neu balancieren |
| `europeanism_change` (Ziel per `modify_europeanism_target`), `EU_europeanism_change` (alle Mitglieder), `EU_potential_europeanism_change` (alle potenziellen), `set_eu_candidate_europeanism_floor` (auf 0,5) | `99_eu_scripted_effects.txt:119, 152, 177, 199` | direkt nutzbar |
| `invest_in_EU_single_market_infra` (Infrastruktur beim Empfänger, Europeanism beider) | Z. 217 | Regionalfonds-Projekte |
| `leaving_EU` (Austritt, Ämter räumen, Cooldown 1095 Tage) | Z. 343 | Austrittspfad |
| `POTEF_election`, `election_EU_Parliament` | Z. 1024, 1582 | Direktwahl 1979 / Ratspräsident |
| `joining_the_euro` (Währungs-Idea → `euro`) | Z. 1829 | nur als Technik; 1970 anachronistisch |
| Flag `EU_candidate`, Idea `EU_pre_accession_assistance` (+25 % PP, +15 % Steuern, endet mit Mitgliedschaft) | `SWI_eu_candidacy`, `EU_ideas.txt:310` | Kandidatenstatus |
| Decision `EU_apply_for_membership` (50 PP, braucht `EU_candidate` + Europeanism ≥ 0,8) gibt **einseitig** `add_ideas = EU_member` | `common/decisions/EU_voting_decisions.txt:1635-1683` | **MP-Problem**: Mitglieder stimmen nicht zu |
| Austritt per GUI-Flag `Article_50` → Mission `EU_exit` (730 Tage), `EU_Revoke_Article_50`, `EU_extend_Article_50`, Ideas `withdrawal_treaty`, `no_deal_exit` | `EU_voting_decisions.txt:777-1030`; Flag gesetzt in `common/scripted_guis/01_european_union_guis.txt:1791` | Austrittsmechanik als Vorlage (Artikel 50 selbst ist Lissabon 2009) |

### 3.2 Pro Land

**Frankreich** (`05_france.txt`, 79 Treffer; Decisions `France.txt`)
- Pro-EU (alle mit `available … has_idea = euro` und `bypass = { NOT = { has_idea = euro } }`, also 1970 automatisch übersprungen): `FRA_eu_federalism` (579: Europeanism +0,1 für alle anderen Mitglieder, schaltet Kategorie `FRA_EU_assistance_decision_category` frei), `FRA_strenght_throught_EU` (1429: Idea `FRA_EU_strong`, Europeanism +0,3), `FRA_independant_Euro` (1894), `FRA_nuclear_eu` (2162: Event an alle Mitglieder, **senkt GER/AUT-Europeanism um 0,15/0,10**; `AUT` ist kein MD-Tag, Österreich heißt `AUS`, der Zweig greift also nie), `FRA_eu_mil` (2432), `FRA_share_eu` (2613, „Eu_nuclear_power“).
- Euroskeptisch/Austritt: `FRA_question_ref` (3110), `FRA_neccesity_leaving` (3956), `FRA_campaign_frexit` (4486), `FRA_frexit_ref` (4594 → Event `france_md.180`, `events/France.txt:2154`: **nur eine Option**, kein echtes Referendum), `FRA_no_more_eu` (10305: `leaving_EU` + `NATO_leave`), `FRA_renogociate_treaty` (8886), `FRA_fate_eurocommunism` (12449).
- Decisions: Frexit-Kategorie (`France.txt:484-591`), **`FRA_veto_eu_federalization`** (6019: 50 PP, alle 365 Tage, Meinungsmalus `FRA_eu_obstruction` bei allen Mitgliedern), **`FRA_inst_civ_/inf_/eco_<TAG>`** (6549-7349: Frankreich investiert in GER, GRE, ITA, BEL, SPR, POL; Event an den Empfänger, Kosten bei FRA).
- 1970: Euro-Fokusse fallen weg. **Vorlagen:** Veto-Decision → Luxemburger-Kompromiss-Joker / „leerer Stuhl“; Invest-Decisions → EAGGF-/Regionalfonds-Projekte (positiv für Empfänger); `FRA_share_eu`/`FRA_nuclear_eu` → europäische Force de frappe (Alt-Pfad).

**Deutschland** (`05_germany.txt`; `GER_1985.txt`; `Germany.txt` ohne EU-Decisions)
- `GER_european_ties` (16570: Europeanism +0,03, Einfluss in allen Mitgliedern), `GER_european_values` (16674: Timed Idea), `GER_European_Anker_Army` (11632: Event `GER_Cold_War.30`, bypass ohne NATO), `GER_question_european_union` (18599), `GER_european_mentor`-Zweig (22030ff: Monarchien restaurieren).
- 1985: `GER_1985_european_defence_identity` (518: Idea `GER_1985_european_defence_policy`, Doktrin-Rabatt), `GER_1985_deepen_european_integration` (674: FRA-Meinung `franco_german_friendship`), `GER_1985_germany_in_europe` (1182).
- **Vorlagen:** 1985-Fokusse sind periodennah (deutsch-französische Freundschaft, Elysée-Linie, WEU-Revival); `GER_European_Anker_Army` → EVG-Brigaden.

**Italien** (`05_italy.txt`; `Italy.txt` ohne EU-Decisions)
- Kette `ITA_european_relations` (11654, Kosten 0,1, braucht `EU_member`) → `ITA_european_speech` (11675), `ITA_with_europe` (11731), `ITA_without_europe` (11793), `ITA_italeave` (11845). Dazu `ITA_return_to_lira` (4585), `ITA_safeguard_european_development_funds` (19269), `ITA_seek_european_help` (20709).
- **Vorlagen:** Entscheidungsstern „mit/ohne Europa“ als nationale Position; Entwicklungsfonds → Mezzogiorno/Regionalfonds 1975.

**Niederlande** (`05_netherlands.txt`, hängt auch Benelux ein)
- `HOL_eu_single_market_champion` (14247), `HOL_frugal_four_leadership` (14301: Meinung mit AUS/DEN/SWE), `HOL_european_strategic_autonomy` (14349: Meinung + Einfluss in allen Mitgliedern), `HOL_strong_european_union` (17835), `HOL_push_for_nexit` (21460: `random_list` 60/40 mit Modifikator `nationalist > 0.25`), `HOL_bring_back_the_gulden` (21522), `HOL_european_navy` (10835), `HOL_d66_european_initiative` (22396).
- **Vorlagen:** föderalistischer Benelux-Kurs; Referendum-`random_list`.

**Belgien, Luxemburg:** kein eigener MD-Baum; nur `00_generic.txt` (USoE/POTEF/BNL). EG-Inhalt nur über Benelux.

**Vereinigtes Königreich** (`05_united_kingdom.txt`; `uk_1985.txt`; `05_ENG_decisions.txt` ohne EU-Hooks)
- 2000: `ENG_to_europa_and_beyond` (12150, braucht `EU_member`), `ENG_fighting_the_power_of_brussels` (14049: Europeanism −0,05, Meinungsmalus aller Mitglieder), `ENG_a_more_flexible_europe` (14091: Angebotsevent `britain_md.12` an europäische Nicht-NATO-Staaten), `ENG_european_outreach` (16984), `ENG_european_defence_cooperation` (7280).
- **Es gibt keine Brexit-Kette** im UK-Baum (Grep `brexit|referendum|leave_eu` nur Schottland/Irland/Wales-Referenden in `05_ENG_decisions.txt:3332-3501`). Austritt läuft nur über die generische Artikel-50-Mechanik.
- 1985: `ENG_the_european_argument` (176: Variable `ENG_europe_argument` +1, FRA-Meinung), `ENG_social_europe` (5252), `ENG_anchor_britain_in_europe` (6272), `ENG_channel_tunnel_question` (339). `ENG_europe_argument` wird in den gestagten Dateien nur erhöht, nie gelesen [V-stat].
- **Vorlagen:** `ENG_europe_argument` als Kampagnenzähler für Heath 1971 / Wilson-Neuverhandlung 1974-75; Referendum über `random_list` (DEN/HOL-Muster) statt der Ein-Options-Events von Frankreich.

**Irland** (kein 2000er-Baum gefunden; `ireland_1985.txt`)
- `IRE_european_pioneer` (886) → `IRE_single_european_act` (907) → `IRE_structural_funds_strategy` (935) → … `IRE_european_monetary_anchor` (1149): Idea-Kette per `swap_ideas`. `IRE_deepen_the_eec` (1901), `IRE_guard_our_neutrality` (1917), `IRE_open_the_nato_question` (1934).
- **Vorlage:** Stufen-Idea per `swap_ideas` (Mitgliedschaft → Strukturfonds → Währung) für Irlands Beitritt 1973 und Neutralität.

**Dänemark** (`05_denmark.txt`; `Denmark.txt` ohne EU-Decisions)
- Gabel `DEN_commit_to_the_eu` (6550) / `DEN_distance_from_the_eu` (6716) / `DEN_tollerate_the_eu` (6801), gegenseitig ausschließend.
- `DEN_distance_from_the_eu`: **`random_list` 60/40**, gewichtet mit `nationalist > 0.25`. Das ist die beste vorhandene Referendums-Vorlage.
- Austritt: `DEN_leave_schengen` (6904), `DEN_leave_the_eu` (6958: `leaving_EU`).
- Nordisch: `DEN_defense_treatys` (6169), `DEN_strengthen_nordefco` (6224: `give_guarantee` an SWE, NRY, ICE, FIN), `DEN_formalize_nordefco` (6303).
- Partnerwahl: `DEN_German_partner` (7178), `DEN_ties_to_France` (7232), `DEN_ties_to_GB` (7303), `DEN_Benelux_fokus` (7374). `DEN_the_euro_question` (13676).
- **Vorlagen:** Referendum 1972 (63,3 % Ja); Nordek statt EG (Alt-Pfad) über NORDEFCO-Kette.

**Norwegen** (`05_norway.txt`; `Norway.txt` ohne EU-Decisions)
- **Kein Beitrittsfokus, kein Referendum.** `NRY_european_investments` (241: Angebotsevents `norway.5` an GER/FRA/ENG), `NRY_our_european_allies` (3121), `NRY_eea_free_zones` (3187: gegenseitiger Einfluss mit ICE/LIC, EFTA-artig), `NRY_maintain_eu_distance` (3272: Europeanism −0,05).
- **Vorlagen:** Angebotsevents (MP-konform); EFTA-Freihandel; das Referendum 1972 muss neu gebaut werden (Muster DEN).

**Schweden, Schweiz, Finnland (EFTA/Neutrale)**
- SWE: Zweig `SWE_EU_*` (11894-12641: Partnerwahl Paris/Berlin/London, Forschungsrat), `SWE_suspend_eu_defense_integration` (16458: `random_list`), `SWE_non_aligned_responsibility` (14268: Idea `neutrality_idea`).
- SWI: `SWI_move_closer_to_the_eu` (3307), `SWI_distance_from_eu` (4334), `SWI_denounce_eu` (5671), **`SWI_eu_candidacy`** (7688: Flag `EU_candidate`, Europeanism-Boden), `SWI_trust_in_the_eu` (7764), `SWI_european_defence` (7936), `SWI_expanded_trade` (7368), `SWI_eu_investments` (7587).
- FIN: `FIN_secure_european_trade_deals` (444) und `FIN_european_involvement` (1713): gegenseitige Meinungsmodifikatoren mit allen Mitgliedern (positiv).
- **Vorlagen:** Freihandelsabkommen 1972/73 (Stufe 3), Kandidatenflag.

**Griechenland** (`05_greece.txt`; 1970: `COLDWAR_GRE_1970_focus`)
- 2000: `GRE_convert_to_euro` (3064), `GRE_eu_cohesion_funds` (4473: Bautempo +5 %), `GRE_eu_political_anchor` (10442: gegenseitig `declaration_of_friendship`), `GRE_discredit_eu` (8636), `GRE_support_eu` (8690), `GRE_balkans_eu_advocacy` (11006).
- 1970 (aktiv): siehe 2.2. **Inhaltlicher Befund:** Das „European Dossier“ und die CYP-Assoziierung adressieren **ENG** als Gegenpartei. Historisch verhandelte die EWG-Kommission bzw. der Rat der Sechs (GRE-Assoziierung 1961, CYP-Abkommen 1972); der Europarat (Ausschluss Dezember 1969) ist eine andere Organisation. Sobald ein EG-System existiert, sollten diese Angebote an den Ratsvorsitz bzw. an alle Sechs gehen [A].

**Spanien** (`05_spain.txt`; 1970: `spain_1970.txt`)
- 2000: `SPR_europe_now_and_forever` (5675), `SPR_eu_spanish_alignment` (5739), `SPR_a_dominant_role` (5911: **senkt Europeanism anderer großer Mitglieder um 0,10**), `SPR_the_drift_from_europe` (5978), `SPR_spexit` (6173), `SPR_the_european_upheaval` (8731).
- 1970: siehe 2.2. Der Präferenzvertrag vom 29.6.1970 fehlt. Der Beitritt ist einseitig (`SPR_1970.227`).

**Türkei** (`turkey.txt`, `turkey_1985.txt`)
- `TUR_look_west` (1030: Angebot an BUL/GRE), `TUR_approach_the_eu` (5920: gegenseitige Meinung mit allen Mitgliedern).
- 1985: `TUR85_eec_application` (1524) und `TUR85_customs_union` (1601) sind Platzhalter (nur PP, Stabilität, +30 Schatz).

**Allgemein `00_generic.txt`:** `GENERIC_the_west` (688) prüft `EU_member`, sonst nichts.

### 3.3 Was 1970 wegfällt, was Vorlage ist [A]

| Kategorie | Fällt 1970 weg | Taugt als Vorlage für |
|---|---|---|
| Euro-gebundene Fokusse (FRA, HOL, DEN, GRE, ITA) | alles mit `has_idea = euro` / `bypass NOT euro` | Werner-Stufen, Schlange 1972, EWS 1979 (neue Ideas statt `euro`) |
| Austrittsketten (Frexit, Italeave, Nexit, Spexit, DEN, Artikel 50) | moderner Kontext | **UK-Neuverhandlung + Referendum 1975**, Grönland 1982-85, Alt-Pfad „Zerfall der EG“ |
| Kandidatur (SWI_eu_candidacy, EU_candidate, EU_pre_accession_assistance) | – | Kandidatenstatus ENG/IRE/DEN/NRY 1970 |
| Referendum-`random_list` (DEN 6716, HOL 21460, SWE 16458) | – | **NOR 1972 (Nein)**, DEN 1972, IRE 1972, UK 1975 |
| Angebotsevents (NRY 241, ENG 14091, GRE_1970 foreign_6, CYP_1970) | – | Assoziierung, Kapitelverhandlungen |
| SPR_1970-Beitrittskette | – | Süderweiterung; Präferenzabkommen 1970 nachrüsten |
| TUR/TUR85 | – | Zusatzprotokoll 1970, Zollunionsfahrplan |
| Schengen (DEN_leave_schengen) | ja | Passunion erst 1985; Vorläufer (Nordische/Benelux-Passunion) als Start-Idea |
| Migrations-, Green-Deal-, Rail-, Fossil-Fokusse (FRA, GER) | ja | – |

---

## 4. Vorschlag: 1970-EG-Bäume

### 4.1 Architektur

**Zwei Wurzeln in einer neuen Datei `common/national_focus/COLDWAR_EC_1970_shared.txt`** (Präfix `COLDWAR_EC_`; die archivierten Namen `CW_EC_*` / `COLDWAR_EEC_*` aus dem entfernten CWEC-System nicht wiederverwenden):

1. **Gemeinschaftsbaum** `COLDWAR_EC_the_hague_agenda` als **`joint_focus`** für Mitglieder.
   - `allow_branch` mit **statischer** Tagliste: FRA GER ITA BEL HOL LUX ENG IRE DEN NRY GRE SPR POR TUR CYP MLT AUS SWI SWE FIN ICE. Bei Beitritt `mark_focus_tree_layout_dirty = yes`.
   - `joint_trigger` mit **Live**-Mitgliedschaft (`has_idea = EU_member` oder ein neues EG-Flag).
   - Muster: Benelux und `COLDWAR_UNI` [P].
2. **Annäherungsbaum** `COLDWAR_EC_the_road_to_brussels` als **`shared_focus`** für Nichtmitglieder.
   - Statusleiter wie im Geschichtsbericht 6.1: Handelsabkommen → Präferenz → Freihandel → Assoziierung → Antrag → Verhandlung → Vertrag → Ratifikation/Referendum → Übergangszeit.
   - Zweige per `allow_branch` je Gruppe: Kandidaten ENG/IRE/DEN/NRY; Süden GRE/SPR/POR/TUR; Mittelmeer CYP/MLT; EFTA-Neutrale AUS/SWI/SWE/FIN/ICE.

**Einhängen**
- je eine `shared_focus`-Zeile in:
  - den Generator des generischen Baums
  - `spain_1970.txt`
  - den GRE-Generator (`tools/greece_1970/compile.py`)
  - `COLDWAR_CYP_1970_focus.txt`
- **Offsets nach `has_focus_tree`** (Commonwealth-Muster), **nicht nach Tag** wie bei `USoE001`.
- Position im generischen Baum: rechts vom geplanten Unionskasten (x 232 bis ca. 252), also ab **x ≈ 258, y 0**. Dass ausgeblendete Zweige mit gleichen Koordinaten nicht gezeichnet werden, ist laut Projekt-Doku noch zu prüfen [P].

**Pfadwahl ohne `mutually_exclusive` in Joint-Zweigen** (Team-Regel [P]):
- Ob der historische Pfad, der gaullistische oder der föderale gilt, entscheidet ein Ratsbeschluss. Dafür das MD-Votum (`apply_EU_QMV_result`, `99_EU_voting_scripted_effects.txt:316`) oder einstimmige Angebotsevents nutzen. Ergebnis: globales Flag `COLDWAR_EC_path_*`.
- Joint-Fokusse eines Pfades prüfen dieses Flag in `available`.
- Nationale Positionen (Gaullismus, Labour-Linke, Eurokommunismus) sind normale `shared_focus` in eigenen Unterzweigen. Effekte nur auf das eigene Land.

**MP-Regeln (aus Vorgabe und Team-Doku)**
- `completion_reward` / `_joint_member` nur positiv. Keine Tag-Scopes wie `USA = { … }`, keine globalen Schreibzugriffe; Kosten und Globales nur in `_originator`.
- `select_effect` setzt ein zeitlich begrenztes Global-Flag (Team-Regel).
- **Kein einseitiges `add_ideas = EU_member`.** Bisher tun das `EU_apply_for_membership` und `SPR_1970.227`. Beitritt und Assoziierung laufen über ein Angebotsevent an jedes Mitglied: annehmen, nachverhandeln, vertagen, ablehnen; Schweigen nach 90 Tagen ist keine Zustimmung (Vorlage GRE `foreign_6` / `COLDWAR_GRE_TREE.142`). Erst bei Einstimmigkeit `add_ideas = EU_member`.
- Fremde Europeanism/Meinung nur über Events senken, nicht per Fokus (betrifft Vorlagen wie `FRA_nuclear_eu`, `SPR_a_dominant_role`, `ENG_fighting_the_power_of_brussels`).

### 4.2 Gemeinschaftsbaum: historischer Pfad

| Zweig | Neue Fokusse (Vorschlag) | Wiederverwendbare Fokusse/Effekte (ID, Datei) |
|---|---|---|
| **Den Haager Agenda / Vollendung** | `the_hague_agenda` (Wurzel), `own_resources_1970` (Eigenmittel), `financing_the_cap`, `common_commercial_policy` | `POTEF151` [Empire of Trade] (`02_EU_POTEF_shared.txt:570`, Werte trade_opinion +5 %/opinion gain +10 %); `POTEF251` [Liberal Legacy] (Z. 1169, Konsumgüter −5 %); `BNL_single_market` (`03_benelux_shared.txt:41`), `BNL_freight_corridors` (211) für Zahlen; MD-Budget (`distribute_EU_budget`, `99_eu_scripted_effects.txt:1395`) |
| **GAP und Mansholt-Plan** | `the_green_europe`, `mansholt_plan` (Höfe zusammenlegen: Produktivität +, Bauernmeinung −), `the_butter_mountain` | `AGRI_price_change_all_crops` + `change_farmers_opinion` (beide in `GEN_1970_trade_with_the_neighbours`, `mdcw_1970_generic_focus.txt:6591`, und `USoE502`); `FRA_inst_eco_*`-Decisions (`France.txt:7114ff`) als Strukturhilfe |
| **Werner-Plan / Währung** | `the_werner_report` (1970), `the_snake` (1972), `the_european_monetary_system` (1979), optional `werner_succeeds` (Alt-Pfad) | `IRE_european_monetary_anchor` (`ireland_1985.txt:1149`, Idea-Stufen per `swap_ideas`); `DEN_the_euro_question` (`05_denmark.txt:13676`); Technik `joining_the_euro` (`99_eu_scripted_effects.txt:1829`) nur für eine Alt-Währungs-Idea, nicht für den Euro |
| **EPZ (Davignon)** | `the_davignon_report`, `one_voice_at_the_csce`, `european_council_1974` | `FIN_european_involvement` (`05_finland.txt:1713`, gegenseitige Meinung, positiv); `HOL_european_strategic_autonomy` (`05_netherlands.txt:14349`); `GER_1985_deepen_european_integration` (`GER_1985.txt:674`, `franco_german_friendship`); Meinungsmodifikator `CSCE_peace_talks` (aus `POTEF552`) |
| **Erweiterung** (Mitgliederseite) | `open_the_doors` (30.6.1970), `the_luxembourg_negotiations`, `the_treaty_of_brussels_1972`, später `the_southern_enlargement` | Angebotsmuster `COLDWAR_GRE_1970_send_foreign_6` (`COLDWAR_GRE_1970_tree_effects.txt:18365`) und `COLDWAR_GRE_TREE.142`; `EU_pre_accession_assistance` (`EU_ideas.txt:310`); `set_eu_candidate_europeanism_floor` |
| **Regionalfonds 1975** | `the_regional_fund` → Decision „Fund a Regional Project in [TAG]“ | `FRA_inst_civ_/inf_*` (`France.txt:6549-7066`: Geber zahlt, Empfänger bekommt Event); `invest_in_EU_single_market_infra` (`99_eu_scripted_effects.txt:217`); `GRE_eu_cohesion_funds` (`05_greece.txt:4473`); `SPR_1970_european_development_funds_idea` |
| **Direktwahl 1979** | `the_act_of_1976`, `direct_elections_1979`, `parliament_gains_the_budget` | `election_EU_Parliament` (`99_eu_scripted_effects.txt:1582`), `POTEF_election` (1024); `USoE003` [European Political Parties] (`01_EU_USoE_shared.txt:345`) inhaltlich → Parteienbünde |
| **Abschluss** | `the_european_union_1980s` (Tindemans / Maastricht-Vorstufe) | `POTEF800` [Pax Europaea] (`02_EU_POTEF_shared.txt:7640`) als positive Abschlussidee für alle Mitglieder; `european_spirit` (`EU_ideas.txt:301`) |

### 4.3 Gemeinschaftsbaum: alt-historische Pfade (je per Ratsbeschluss freigeschaltet)

| Pfad | Neue Fokusse | Wiederverwendung (ID, Datei) | MP-Hinweis |
|---|---|---|---|
| **Europa der Vaterländer (Fouchet)** | `the_fouchet_revival`, `union_of_states`, `the_luxembourg_veto` | `FRA_veto_eu_federalization` (`France.txt:6019`) als **Veto-Joker-Decision** für jedes Mitglied; `FRA_question_ref` (`05_france.txt:3110`) als nationale Position | Veto kostet den Nutzer PP + Meinung; kein Zwang für andere |
| **Föderalistische Vereinigte Staaten von Europa (Spinelli)** | `the_constituent_assembly`, `the_federal_treaty`, `capital_of_europe`, optional `the_united_states_of_europe` | `USoE002`/`003`/`004` (`01_EU_USoE_shared.txt:320-370`), Decision `EU_USoE_capital_of_europe` (`EU_USoE_decisions.txt:4`), Votum 112 / Flag `european_federation` (keine Annexion); Votum 111 (`99_EU_voting_scripted_effects.txt:406`, Snapshot-Muster `global.USoE_formation_members`) **nur** mit Zustimmungsevent jedes Mitglieds | Staatsvereinigung = einzelne Zustimmung jedes Spielers |
| **EVG mit Atomwaffe** | `the_weu_reawakens`, `the_european_defence_community`, `integrated_command`, `the_european_deterrent` | Standardisierungsfokusse aus `POTEF150/200/250/350/400/450` (Werte halbieren, Bug mit `POTEF_dynmod_*` beheben, d. h. Modifikator für jeden Teilnehmer setzen); `USoE002` (Offizierskorps); `GER_1985_european_defence_identity` (`GER_1985.txt:518`); `FRA_share_eu` / `FRA_nuclear_eu` (`05_france.txt:2613/2162`) nur als FRA-Originator; Decision `EU_military_exercise` (`EU_voting_decisions.txt:1351`) für Manöver | NPT-Sperre für GER-Kontrolle; NATO-Austritt nur national |
| **„Dritte Kraft“ zwischen den Blöcken** | `between_the_blocs`, `a_pact_with_moscow`, `a_pact_with_washington`, `the_eurosphere` | `USoE200-204` (`01_EU_USoE_shared.txt:603-742`) mit `USoEevent.1` (Ja/Nein); `POTEF201` (Einfluss der Supermächte −3 %) nur als Event-Angebot; `GEN_1970_change_tension` (`mdcw_1970_generic_focus_effects.txt:40`); `EU_create_EDU` (`EU_voting_decisions.txt:1303`) **nur** mit Einzelzustimmung (entfernt sonst `NATO_member`) | Bündniswechsel nie per Joint-Belohnung |
| **Eurafrika** | `the_yaounde_convention`, `the_lome_convention`, `eurafrican_development_fund` | `POTEF451` (`02_EU_POTEF_shared.txt:4418`) **ohne** Annexionsblock Z. 4555-4569; `POTEF252/253` (Bauten in Ex-Kolonien) als Angebotsevent an den Empfänger | Bauten in Fremdstaaten nur nach Annahme |
| **EFTA-Fusion / Großfreihandelszone** | `the_great_free_trade_area`, `efta_bridge` | `NRY_eea_free_zones` (`05_norway.txt:3187`), `NRY_european_investments` (241, Angebotsevents `norway.5`), `SWI_expanded_trade` (`05_switzerland.txt:7368`), Commonwealth-Handelszweig (`COMMONWEALTH_preferential_trade_talks`) | – |
| **Zerfall der EG / neuer leerer Stuhl** | `the_empty_chair`, `the_community_in_crisis`, `dissolution_talks` | `leaving_EU` (`99_eu_scripted_effects.txt:343`), `withdrawal_treaty`/`no_deal_exit` (`EU_ideas.txt:389/401`), Mission `EU_exit` (`EU_voting_decisions.txt:827`) neu begründet (es gab keine Austrittsklausel); Frexit-Decisions (`France.txt:484-591`) als nationale Druckmittel | Auflösung = Ratsbeschluss, kein Joint-Effekt |
| **Eurokommunismus** (nationale Position) | `the_historic_compromise` (ITA), `eurocommunist_programme` | `USoE402` (`01_EU_USoE_shared.txt:1680`), `FRA_eu_communism_PCF` (`05_france.txt:9202`) | Parteieffekte nur im eigenen Land |

### 4.4 Annäherungsbaum (Kandidaten, Assoziierte, EFTA)

| Zweig | Neue Fokusse | Wiederverwendung (ID, Datei) |
|---|---|---|
| **Antrag und Kapitel** (ENG, IRE, DEN, NRY) | `the_application`, Kapitel `customs_union_transition`, `cap_alignment`, `commonwealth_trade` (ENG), `fisheries` (NRY, IRE), `budget_contribution`, `sterling` (ENG), `greenland_and_faroes` (DEN) | `SWI_eu_candidacy` (`05_switzerland.txt:7688`: `EU_candidate`, Europeanism-Boden); `POTEF352-355` (`02_EU_POTEF_shared.txt:3077-3231`) inhaltlich für Commonwealth-Kapitel; Angebotsevent je Kapitel an jedes Mitglied (GRE-`foreign_6`-Muster) |
| **Ratifikation und Referendum** | `the_referendum` (NRY, DEN, IRE; ENG optional), `the_accession` | `random_list` aus `DEN_distance_from_the_eu` (`05_denmark.txt:6716`) mit Partei-Gewichten; historische Anker im Geschichtsbericht 6.5; Beitritt erst nach Einstimmigkeit, dann `add_ideas = EU_member` wie in `SPR_1970.227` |
| **UK: Neuverhandlung 1974/75** | `renegotiate_the_terms`, `the_1975_referendum` | Zähler `ENG_europe_argument` (`uk_1985.txt:176/6272`); Labour-Spaltung über Parteihaltungen; bei „Nein“ `leaving_EU` + Freihandelsstatus |
| **NOR: Nein-Pfad** | `nei_til_ef`, `the_free_trade_agreement_1973` | `NRY_maintain_eu_distance` (`05_norway.txt:3272`), `NRY_eea_free_zones` (3187) |
| **Nordek (Alt)** | `nordek` | `DEN_strengthen_nordefco` / `DEN_formalize_nordefco` (`05_denmark.txt:6224/6303`), aber `give_guarantee` als Angebot statt einseitig |
| **Süden: GRE** | Assoziierung reaktivieren (vorhanden), `the_1975_application`, `accession_1981` | `COLDWAR_GRE_1970_nd_13` (`COLDWAR_GRE_1970_focus.txt:2996`), `COLDWAR_GRE_1970_foreign_6` (8562); Adressat von ENG auf EG-Rat umlenken |
| **Süden: SPR, POR** | `the_preferential_agreement_1970` (SPR, neu), Antrag/Beitritt (vorhanden) | `SPR_1970_apply_…` (`spain_1970.txt:1240`), `SPR_1970_accession_…` (2113), `SPR_1970.227` auf Zustimmung umbauen |
| **TUR** | `the_additional_protocol_1970`, `the_customs_union_roadmap`, `the_1987_application` | `TUR_approach_the_eu` (`turkey.txt:5920`), `TUR85_eec_application` / `TUR85_customs_union` (`turkey_1985.txt:1524/1601`) |
| **Mittelmeer** (MLT, CYP, MOR, TUN, ISR, YUG) | `association_agreement` | `COLDWAR_CYP_1970_western_association` (`COLDWAR_CYP_1970_focus.txt:3504`; Adressat ENG → EG) |
| **EFTA-Neutrale** (AUS, SWI, SWE, FIN, ICE, POR) | `the_free_trade_agreement_1972`, `neutral_bloc` (Alt) | `FIN_secure_european_trade_deals` (`05_finland.txt:444`), `SWE_non_aligned_responsibility` (`05_sweden.txt:14268`), `SWI_move_closer_to_the_eu` (3307) |

### 4.5 Technische Stolpersteine

1. **Generatoren:** Generischer Baum und GRE-Baum sind generiert. Die `shared_focus`-Zeile muss im Generator stehen, sonst überschreibt der nächste Lauf sie. Fehlt die Wurzel-ID, stürzt das Spiel im Hauptmenü ab; Datei und Header-Zeile daher immer zusammen ausliefern [P].
2. **`USoE001`/`POTEF001` nicht direkt in 1970-Bäume hängen:** tag-basierte Offsets (Z. 9-172, NRY doppelt in Z. 81/121) passen nur zu den MD-Bäumen; dazu Vote-Gates, die Tagliste mit rund 94 Einträgen und Annexionsfolgen.
3. **POTEF-Modifikator-Bug** (Abschnitt 1.3) beim Kopieren der Doktrinen beheben.
4. **Mitgliedschaft 1970 zuerst reparieren:** Startarray mit 15 Ländern, aber ohne Idea (Kernsystem-Bericht). Ohne konsistentes `EU_member` greift kein `joint_trigger`.
5. **Titelleiste:** Es gibt keinen EG-Stil in `00_titlebar_styles.txt` (342 Zeilen: nur `JOINT_*`-Stile für BEL/HOL/LUX, SOV, CHI usw.). Ohne `text_icon` erscheint die Standardleiste; ein `JOINT_EC_focus_style` braucht eigene GFX.
6. **Rückfall, falls Joint-Fokusse im MP Probleme machen:** `shared_focus` mit GCC-`bypass` („einer erledigt für alle“): `gulf_shared.txt:55-61` setzt `GCC_the_gcc_completed`; POTEF nutzt dasselbe Muster mit `any_of_scopes … has_completed_focus`.
7. Für eigene Länderbäume (z. B. FRA_1970) zusätzlich die Whitelist in `mdcw_load_1970_fallback_tree` erweitern.

---

## 5. Gestagte Dateien (diese Sitzung zusätzlich)

- **national_focus:** `03_benelux_shared`, `06_czehcoslavakia_shared`, `06_MERCOSUR_shared`, `06_AfricanUnion_shared`, `Commonwealth_shared`, `mdcw_1970_generic_focus`, `mdcw_1970_empty`, `00_generic`, `00_titlebar_styles`, `gulf_shared`, `05_france`, `05_germany`, `05_italy`, `05_netherlands`, `05_united_kingdom`, `05_denmark`, `05_norway`, `05_sweden`, `05_switzerland`, `05_finland`, `05_greece`, `05_spain`, `turkey`, `turkey_1985`, `spain_1970`, `USA_1970`, `uk_1985`, `GER_1985`, `ddr`, `ireland_1985`, `COLDWAR_GRE_1970_focus`, `COLDWAR_CYP_1970_focus`
- **decisions:** `France`, `Germany`, `Italy`, `netherlands`, `Denmark`, `Norway`, `05_ENG_decisions`, `05_GRE_decisions`, `Spain`, `Turkey`, `05_SWI_decisions`, `05_sweden_decision`, `05_POR_decisions`, `Greece`, `Commonwealth`, `NATO`, `ENG_1985_decisions`, `COLDWAR_TUR_1970_regional_decisions`, `COLDWAR_GRE_1970_regional_decisions`, `SPR_1970_franco_decisions`, `mdcw_cold_war_decisions`, `formable_nation_decisions`; neu gestagt (Gerät war neuer, Inhalt gleich groß): `EU_voting_decisions`
- **scripted_effects:** `mdcw_1970_focus_tree_effects`, `mdcw_1970_generic_focus_effects`, `99_FRA_scripted_effects`, `99_GER_scripted_effects`, `99_ENG_scripted_effects.`, `01_NATO_effects`, `COLDWAR_TUR_1970_regional_effects`, `COLDWAR_GRE_1970_regional_effects`, `SPR_1970_scripted_effects`, `COLDWAR_GRE_1970_tree_effects`; neu gestagt: `99_eu_scripted_effects`, `99_EU_voting_scripted_effects`
- **scripted_triggers:** `99_HOL`, `00_scripted_triggers`, `99_FRA`, `99_GER`, `99_ENG`, `99_ITA`, `99_DEN`, `99_NRY`, `99_GRE`, `99_TUR`, `99_SPR`, `99_SWE`, `99_SWI`, `99_CZE`, `mdcw_1970_generic_focus_triggers`, `01_political_triggers`, `MD_regional_triggers`, `00_game_rule_triggers`
- **events:** `03_benelux`, `France`, `Norway`, `Denmark`, `Italy`, `Turkey`, `05_switzerland_events`, `Greece`, `Finland`, `05_united_kingdom`, `ENG_1985_politics`, `Spain`; neu gestagt: `EU_events`
- **history/countries:** FRA, GER, ITA, BEL, HOL, LUX, ENG, IRE, DEN, NRY, SWE, SWI, AUS, POR, SPR, GRE, TUR, FIN, ICE, CYP, MLT, EUU
- **localisation/english:** `MD_focus_EU_USoE`, `MD_focus_EU_POTEF`, `MD_focus_Benelux_shared`, `MD_focus_EU`, `mdcw_1970_generic_focus`, `MD_focus_FRA/GER/ITA/HOL/ENG/DEN/NRY/GRE/TUR/SPR/SWE/SWI/FIN`, `MD_focus_IRE_1985`, `mdcw_historical_MD_focus_ENG_1985`, `SPR_1970`, `MD_focus_DDR`, `mdcw_selected14_GER_1985_focus`, `MD_focus_TUR_1985`, `MD_focus_CMW`, `Commonwealth`

Hilfsskripte (nur lesend) liegen unter `/tmp/claude-0/-home-claude/aa6f7bfa-ace8-51af-9368-3a16aa20beb7/scratchpad/a2tools/`.
