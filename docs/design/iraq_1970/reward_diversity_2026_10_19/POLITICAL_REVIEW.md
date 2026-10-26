# Politische Belohnungsvielfalt: unabhängige Bestandsprüfung

19. Oktober 2026. **Nur Audit und Vorschläge: keine Gameplaydatei, kein Generator verändert.** Thema: Baath/Bakr/Saddam, Offiziere, Nasseristen, ICP/Aziz, zivile Parteien, Krone, KDP/PUK, Dawa/SCIRI/IIP.

Alle 252 politischen Fokusdauern und aktuellen Modifikatorpakete wurden gegen den tatsächlich installierten Fokusbaum und die Programmverbraucher abgeglichen: keine Abweichung. Titel kommen aus installierter englischer Lokalisierung; alte `reward_summary`-/`available`-Texte wurden nicht als Belohnungsquelle benutzt. Die 20 konkreten Vorschläge stehen in `POLITICAL_PROPOSALS.json`. Alle neuen Werte sind **nicht genehmigte Balancevorschläge**, keine historischen Wirkungszahlen.

## Wichtigste Ergebnisse

- Alle 14 Kapitel haben exakt 18 aktive Foki und genau zwei exklusive Paare. 220/252 dauern 35 Tage. 201 haben weder Gebäude, einmaligen Effekt, XP noch Entscheidung. Echte Verträge/Wahlen sind dabei sinnvoller Inhalt; ein bloßer laufender Modifier ist nicht automatisch wertlos.
- Häufigste Modifier: Stabilität98, Bürokratie84, PP70, Sozialkosten33, Ideologieabwehr27, Steuern26, allgemeine Forschung18, Auslandseinfluss11. Das ist eine Häufigkeit über alternative Kapitel, keine gleichzeitige Stapelsumme.
- Acht Pakete sind exakt +3 Stabilität/−2% PP; acht andere +2 Stabilität/+3% Bürokratie. Dawa/IIP haben denselben parlamentarischen Pfad (+4 Stabilität/−3% PP), Sozialmarkt (+3% Effizienzaufbau/−2% Steuern), Welfare (+4 Stabilität/+5% Sozialkosten), Bürgerrechte (+3 Stabilität/−4% Ideologieabwehr) und Medizin (+3 Stabilität/+4% Sozialkosten).
- `dawa_medical_network`, `iip_medical_welfare` und `saddam_social_contract` haben genau dasselbe Modifierpaket. Verschiedene Geschichten erzeugen somit dieselbe Handlung im Haushalt.
- Besonders schwache Einzelkarten: Membership Records, Wählerverzeichnis, wiederholte Kompensations-/Gerichtsverwaltung, technische Missionen mit fachfremder Armeepersonalrechnung. Diese drei Verwaltungskarten zusammenführen, nicht alle auf künstlich starke Boni aufblasen.
- Saddams bereits überarbeitete Guard/Regular-Army-Gabel und mehrere Schlussprogramme behalten. Eine weitere pauschale Steigerung würde gute Unterschiede wieder verwischen.

## Ganze kompatible Programme und der Stabilitätscap

Die nachfolgende Enumeration respektiert die zwei exklusiven Paare sowie AND zwischen und OR innerhalb der Voraussetzungsklammern. Verlorene Zweige und ihre Folgekarten werden nicht mitgezählt. Vorausgesetzt sind echte Umsetzung, richtige Regierung/Amtsinhaber und geltende Verträge; dies ist keine automatische Vertragsannahme.

Der installierte Abgleich deckelt **alle positiven Programm-Stabilitätsbeiträge gemeinsam bei +15 Punkten** und skaliert proportional (`common/scripted_effects/COLDWAR_IRQ_1970_programmes.txt:7906–7996`). Negative Stabilitätsbeiträge bleiben ungekürzt. Dawa allein kann auf einem kompatiblen 14-Fokuspfad +22 positive Punkte erreichen, IIP +20, Civic/KDP/Aziz je +19. Ab dem Cap bewirkt ein weiterer ausschließlich positiver Stabilitätsfokus keinen zusätzlichen gesamten positiven Beitrag; Preis und Malus bleiben. Deshalb den Cap behalten und Füller durch konkrete Ergebnisse ersetzen.

Baath plus genau ein aktives Amtsprogramm Bakr/Saddam sind kompatibel; ebenso ICP plus Aziz. **Bakr und Saddam nicht gleichzeitig addieren.** Auf eingehaltenen repräsentativen Baath-/Bakr-Routen sind +30 positive Punkte schon vor gemeinsamen Staats-/Sozialreformen möglich; deren Maximalvarianten sind verfassungsseitig miteinander verträglich. ICP/Aziz kommen auf +36 in ihren vereinbaren pluralistischen/föderalen Regierungsprogrammen. Andere Regierungsparteien werden nicht gleichzeitig addiert.

Startprobleme bleiben daneben real: July State −8 Stabilität/+8% Bürokratie; Unsettled North −12 Stabilität/+10% Armeepersonal/+4% Versorgung; Patronage +10% Bürokratie/−6% Steuern/−5% Organisation; Rural −12% Agrarproduktivität/+3 Punkte Consumer-Goods-Fabriken; IPC −18% Ölexport; Frontier +5% Armeepersonal/−5% eigener Auslandseinfluss (`common/ideas/COLDWAR_IRQ_1970_starting_ideas.txt:5–56`). Literacy verweist auf das tatsächliche MD-Bildungssystem und ist kein zweiter erfundener Forschungsmalus. Behebung dieser Belastungen ist bereits wichtig; dieselbe Entlastung nicht nochmals pro Partei verschenken.

## Fachliche Zuordnung der tatsächlichen Mechaniken

`foreign_influence_modifier` verstärkt eigene Einflussaktionen; `foreign_influence_defense_modifier` verteidigt gegen fremde. Installierte Leser: `common/scripted_effects/00_influence_scripted_effects.txt:255/264`, `:1107/1116`. Negative eigene Außenwirkung ist keine direkte Abwehr iranischer Patronage. Als Preis weniger eigener Auslandsaktivität kann sie weiterhin sinnvoll sein. Das ist besonders bei Dawa/SCIRI-Souveränitätsbenennungen wichtig.

Bürokratie und Sozialkosten sind laufende Ausgabenmultiplikatoren nach Bevölkerung/gewählter Stufe (`00_money_system.txt:3311`, `:3505`). 84 Bürokratieänderungen erzeugen Haushaltskosten, aber nicht automatisch 84 interessante Entscheidungen. Gesundheits-/Bildungskosten greifen ebenfalls auf tatsächliche native Ausgaben (`:3476`, `:3374`): Ersparnis erzeugt kein Bargeld und kann ohne relevante Ausgabe wirkungslos sein. Alphabetisierung aktualisiert Forschung, Bildungsausgaben, Produktivität und Arbeitskräfte über das bestehende System (`00_education_effects.txt:117–131`, `:166`). Für denselben Lernfortschritt nicht gleichzeitig noch einen zweiten Forschungsschub verschenken.

## Haupt-MD-Kalibrierung und 1970er-Verwendbarkeit

Aktuelle Workshop-Dateien am 19. Oktober 2026. Mechanische Formen und Skalen, keine Berechtigung für kostenlose Großmachtpakete.

| Fokus | Dauer | Belohnung und relevante Bedingung |
|---|---:|---|
| `SOV_ratnik_program`, `05_russia.txt:31697` | 21 Tage | 1×15% `CAT_infantry`, nach Reserve Officer Training |
| `GER_KRK_army`, `05_germany.txt:6543`, Bonus:6597 | 42 Tage | 2×50% `land_doctrine`, nach Einsatzführungskommando |
| `ISR_assam_ibrahims_mission`, `05_israel.txt:13005` | 28 Tage | je 1×25% Special-Forces-Equipment und Landdoktrin; EGY existiert, Frieden, Meinung >4 |
| `TUR_industrial_research`, `turkey.txt:1726` | 40,04 Tage | 2×50% `CAT_industry`, nach Research Grants |
| `TUR_electronic_research`, `turkey.txt:1753` | 40,04 Tage | 2×50% `CAT_information_technology`, nach Research Grants |
| `SOV_back_to_the_west`, `05_russia.txt` | 49 Tage | −25% eingehende Investitionsdauer/-kosten plus USA-Meinung und eigene Nachteile; oligarchische Regierung |

Irak-Vorschläge 1×25–35% sind meist kleinere Pakete; beim Staff College wird die gemeinsame zweite Trainingsquelle ausdrücklich mitgerechnet. `CAT_industry`/`CAT_construction` sind in geladenen 1940–1975-Bautechnologien vorhanden (`mdcw_historical_industry.txt:26–148`), `CAT_information_technology` bereits bei 1945/1955-Computern und deren Fortsetzung (`engineering.txt:779–819`), `CAT_infantry` in frühen Infanterietechnologien (`mdcw_historical_land.txt:24–30`). Ein im konkreten Save ausgeschöpftes Forschungsfeld kann trotzdem keinen weiteren Nutzen aus Kategorienboni ziehen.

Weitere echte MD-Verwendungen: `army_intel_factor` in `common/ideas/05_france.txt:231`; `production_speed_industrial_complex_factor` in `05_Australia.txt:50/58`, `05_france.txt:533`; `production_speed_infrastructure_factor` in `03_CHI_SOV_joint.txt:9`; Bildungskosten in `00_MD_dynamic_modifiers.txt:170`; Gesundheitskosten u.a. `05_Australia.txt:42`. Die eingehende Investitionsdauer wird im geladenen `common/scripted_effects/99_investment_scripted_effects.txt:421–449` in Baugeschwindigkeit umgerechnet: −0.15 garantiert nicht linear genau 15% weniger Kalendertage. Niemand wird zum Investieren gezwungen. Widerstandsziel/Entfernung sind in der bestehenden US/Irak-Integration vorhanden; neue Polizeibeiträge brauchen eigene IDs und richtige Eigentums-, Akteur-, Zustimmungs- und Ablaufbedingungen.

## Historische Grundlage und Grenzen

Die zeitgenössische CIA-Studie *Iraq under Baath Rule, 1968–1976* (November 1976) behandelt das Verhältnis von Partei, Sicherheitsapparat, Militär und ziviler Expertise sowie die begrenzte reale Macht kommunistischer Frontpartner. Ost-/Westkontakte und Nordpolitik begründen verschiedene Institutionen und Verhandlungsbedingungen. Das belegt keine deterministischen Modifier und überträgt nicht jeden Zustand von 1976 auf Januar 1970. [US State Department, FRUS Dokument 317](https://history.state.gov/historicaldocuments/frus1969-76v27/d317), geprüft 19. Oktober 2026.

Alternative Regierungen von Hadid/Krone/national regierender KDP/PUK/religiösen Parteien folgen der vorhandenen genehmigten Parteiauswahl. Vorgeschlagene medizinische Effizienz, Produktionszahlen und Ausbildung sind ausdrücklich Counterfactual-/Balancegestaltung, keine historischen Wirkungsstudien. PUK-/SCIRI-Formationsgates, lebende Kandidaten, tatsächliche Regierung und Amtsinhaber bleiben bindend.

Vor einer späteren Umsetzung den ganzen kompatiblen Pfad einschließlich gemeinsamer Militär-/Gesellschaftskapitel, Start-Spirit-Entlastung, temporärer Entscheidungen, echter Kredite und Cap prüfen. Nationale dauerhafte Fortschritte und gerade aktive Partei-/Leaderprogramme trennen. Neue Einmalprämien dürfen bei Rückkehr/Revision nicht erneut erscheinen. Für dieses Audit gab es keinen neuen Spielstart, keine Hover-, Save- oder Multiplayerprüfung und keine Implementierung.



## Aktuelle Beispiele: exakte Werte und installierte Zeilen

F: `common/national_focus/COLDWAR_IRQ_1970_focus.txt`; R: `common/scripted_effects/COLDWAR_IRQ_1970_rewards.txt`; P: `common/scripted_effects/COLDWAR_IRQ_1970_programmes.txt`. Rohwert 0.03 Stabilität = drei Prozentpunkte. BIP-Prozent ist einmaliger aktueller Rechnungssatz, keine Neuquotierung alter Saves.

| Fokus / tatsächlicher englischer Titel | Dauer / Preis | Aktuelle tatsächliche Modifier | Zeilen |
|---|---|---|---|
| `women_unions` — Women in State Service | 35d / 1% GDP | `research_speed_factor=0.02, social_cost_multiplier_modifier=0.03` | F:1309; R:946; P:662 |
| `bakr_technical_mission` — Technical Missions | 35d / 2% GDP | `research_speed_factor=0.03, army_personnel_cost_multiplier_modifier=0.02` | F:2066; R:1490; P:1084 |
| `saddam_security_bureau` — Security Bureau | 35d / 1% GDP | `drift_defence_factor=0.12, bureaucracy_cost_multiplier_modifier=0.06, stability_factor=-0.02` | F:2331; R:1679; P:1268 |
| `saddam_guard` — Presidential Guard | 35d / 2% GDP | `army_org_factor=0.03, army_defence_factor=0.04, army_personnel_cost_multiplier_modifier=0.1` | F:2478; R:1799; P:1309 |
| `officer_staff` — A National Staff College | 35d / 1.5% GDP | `army_morale_factor=0.03, training_time_army_factor=0.03` | F:3322; R:2429; P:1681 |
| `arab_cairo` — Cooperate with Cairo | 35d / 0% GDP | `opinion_gain_monthly_same_ideology_factor=0.05, foreign_influence_modifier=-0.02` | F:3745; R:2726; P:1975 |
| `icp_membership` — Membership Records | 35d / 0.5% GDP | `political_power_factor=0.02` | F:4659; R:3380; P:2419 |
| `icp_union_autonomy` — Independent Unions | 35d / 0% GDP | `stability_factor=0.03, industrial_capacity_factory=-0.02, social_cost_multiplier_modifier=0.02` | F:4789; R:3471; P:2474 |
| `aziz_language_rights` — Language in Schools | 35d / 1% GDP | `stability_factor=0.02, social_cost_multiplier_modifier=0.02` | F:5575; R:4029; P:2929 |
| `aziz_safe_return` — Bring the Exiles Home | 35d / 1% GDP | `research_speed_factor=0.02, bureaucracy_cost_multiplier_modifier=0.02` | F:5838; R:4219; P:3063 |
| `civic_electoral_register` — An Electoral Register | 35d / 1% GDP | `bureaucracy_cost_multiplier_modifier=0.02` | F:6198; R:4482; P:3273 |
| `civic_universities` — University Autonomy | 35d / 2% GDP | `research_speed_factor=0.03, drift_defence_factor=-0.03` | F:6629; R:4783; P:3469 |
| `royal_settlement` — Constitutional Charter | 49d / 0% GDP | `foreign_influence_modifier=0.08, bureaucracy_cost_multiplier_modifier=0.02` | F:7491; R:5422; P:3899 |
| `royal_compensation` — Compensation Tribunal | 35d / 2% GDP | `stability_factor=0.02, bureaucracy_cost_multiplier_modifier=0.02` | F:7126; R:5137; P:3733 |
| `kdp_local_policing` — Local Police Charter | 35d / 1% GDP | `stability_factor=0.02, bureaucracy_cost_multiplier_modifier=0.02` | F:8782; R:6399; P:4443 |
| `puk_student_exchange` — Iraqi Student Exchange | 35d / 1% GDP | `research_speed_factor=0.02, social_cost_multiplier_modifier=0.02` | F:9503; R:6965; P:4766 |
| `dawa_medical_network` — Community Medicine | 35d / 2% GDP | `stability_factor=0.03, social_cost_multiplier_modifier=0.04` | F:10285; R:7534; P:5192 |
| `dawa_independent_iraq` — An Iraqi Programme | 35d / 0% GDP | `drift_defence_factor=0.06, foreign_influence_modifier=-0.03` | F:10138; R:7427; P:5129 |
| `sciri_revolutionary_courts` — Revolutionary Courts | 35d / 1% GDP | `stability_factor=0.02, bureaucracy_cost_multiplier_modifier=0.03` | F:10532; R:7708; P:5365 |
| `iip_business_law` — Small Business Law | 35d / 1.5% GDP | `production_speed_buildings_factor=0.02, bureaucracy_cost_multiplier_modifier=0.02` | F:11436; R:8404; P:5773 |

## Enumerierte kompatible Gesamtprogramme

Jeweils der Pfad mit den meisten positiven Stabilitätspunkten; vor Cap/gemeinsamen Kapiteln, gültige Verträge vorausgesetzt.

| Kapitel | Exklusive Auswahl | aktive Foki | positive Stabilität | Bürokratie gesamt | Forschung gesamt |
|---|---|---:|---:|---:|---:|
| aziz | aziz_federal_guarantees, aziz_negotiated_road | 14 | +19pp | +4% | +2% |
| baath | mass_party, national_front | 14 | +12pp | +11% | +6% |
| bakr | bakr_collective, bakr_contain_deputy | 14 | +18pp | +6% | +3% |
| civic | civic_federal, civic_social_republic | 14 | +19pp | +5% | +5% |
| communists | icp_democratic_front, icp_front_strategy | 14 | +17pp | +14% | +2% |
| dawa | dawa_constitutional, dawa_social_justice | 14 | +22pp | +12% | +6% |
| kurds | kdp_autonomy, kdp_civic_party | 14 | +19pp | +18% | +0% |
| monarchy | royal_ceremonial, royal_land_review | 14 | +18pp | +9% | +0% |
| nasserist | arab_iraqi_sovereignty, arab_mixed_sector | 14 | +12pp | +4% | +5% |
| officers | officer_caretaker, officer_loyalty | 14 | +9pp | +9% | +0% |
| puk | puk_pluralist_left, puk_regional_cooperation | 14 | +14pp | +9% | +5% |
| saddam | saddam_guard, saddam_party_cabinet | 14 | +6pp | -1% | +0% |
| sciri | sciri_independent_relations, sciri_iraqi_charter | 14 | +14pp | +6% | +2% |
| sunni | iip_parliamentary, iip_welfare | 14 | +20pp | +10% | +0% |

## Kuratierte Empfehlungen im Detail

### women_unions — Women in State Service

**HIGH**: 35 Tage/1% BIP: +2% Forschung und +3% Sozialkosten; identisch mit mehreren Bildungsfoki.

**Vorschlag:** +2% allgemeine Forschung ersetzen durch +5% Militärfabrikleistung; +3% Sozialkosten und 1% BIP/35 Tage behalten. Laufendes Baath-Programm.

**Begründung:** Qualifizierte Beschäftigung erhält einen greifbaren Produktionsnutzen. Zahlen sind Balancevorschlag, keine historische Messung.

Mechaniken: `industrial_capacity_factory`, `social_cost_multiplier_modifier`.

### bakr_technical_mission — Technical Missions

**HIGH**: Technical Missions: 35 Tage/2% BIP für +3% allgemeine Forschung und fachfremde +2% Armeepersonalkosten.

**Vorschlag:** Einmalig 1×30% CAT_industry und 1×25% CAT_construction statt beider Dauermodifikatoren. 2% BIP/35 Tage behalten; eigene Lieferbelege verhindern Wiederholung bei Bakrs Rückkehr.

**Begründung:** Konkrete technische Ausbildung passt zum Gegenstand; kein dauerhafter Wissenschaftsbonus mit willkürlicher Militärrechnung.

Mechaniken: `add_tech_bonus`, `CAT_industry`, `CAT_construction`.

### saddam_security_bureau — Security Bureau

**MEDIUM**: 35 Tage/1% BIP: +12% Ideologieabwehr, +6% Bürokratie, −2 Stabilitätspunkte.

**Vorschlag:** +10% Armeeaufklärung und +10% Abwehr fremden Einflusses statt +12% Ideologieabwehr; −2 Stabilitätspunkte und +4% Bürokratie. 1% BIP/35 Tage bleiben.

**Begründung:** Informations-/Abwehrinstitution statt weiterer Ideologiezeile; Überwachung bleibt teuer. Keine Putschsperre, geografische Polizeiwirkung oder Ressourcenbelohnung für Verfolgung behaupten.

Mechaniken: `army_intel_factor`, `foreign_influence_defense_modifier`, `bureaucracy_cost_multiplier_modifier`, `stability_factor`.

### saddam_guard — Presidential Guard

**KEEP**: Guard/Regular-Army ist bereits eine klare, unterschiedlich wirkende exklusive Gabel.

**Vorschlag:** Behalten: Guard +3% Organisation/+4% Verteidigung/+10% Personalkosten; Regular Army +6% Erholung/−8% Ausbildungszeit/+4% Personalkosten. Je 2% BIP/35 Tage. Bestehende Revision 1% BIP/75 PP ohne Assets-/XP-Replay behalten.

**Begründung:** Qualität und Breite haben unterschiedliche greifbare Vorteile. Nationale Modifier ehrlich als nationale Abstraktion beschreiben.

Mechaniken: `army_org_factor`, `army_defence_factor`, `army_morale_factor`, `training_time_army_factor`, `army_personnel_cost_multiplier_modifier`.

### officer_staff — A National Staff College

**HIGH**: A National Staff College: 35 Tage/1,5% BIP für nur +3% Erholung mit +3% Ausbildungszeit.

**Vorschlag:** +3% Erholung durch einmalig 25 Armee-XP und 1×25% Landdoktrinrabatt ersetzen. +3% Ausbildungszeit als gründlichere Ausbildung und 1,5% BIP/35 Tage behalten.

**Begründung:** Zusammen mit gemeinsamem Defence Staff Training: 60 einmalige XP und zwei getrennte 25%-Rabatte, nicht unbeschränkte Wiederholung. Gesamtumfang prüfen.

Mechaniken: `army_experience`, `add_doctrine_cost_reduction`, `land_doctrine`, `training_time_army_factor`.

### arab_cairo — Cooperate with Cairo

**HIGH**: Cooperate with Cairo: +5% Gleichideologie-Meinungswachstum/−2% eigener offensiver Einfluss, statt konkreter Ägyptenbeziehung.

**Vorschlag:** Bestehendes Arab-Development-Angebot hier freischalten; nach ägyptischer Zustimmung supports_us gegenüber EGY und 1×25% CAT_construction. Mission kostet Irak 1% BIP bei Annahme. Keine zusätzliche ägyptische Zahlung/Anlage ohne Zustimmung; Ablehnung blockiert gemeinsamen Wirtschaftsteil nicht.

**Begründung:** Konkrete Partnerschaft statt globaler Beziehungsschablone. Ein alternativer nasseristischer Vertrag, kein behaupteter historischer Automatismus.

Mechaniken: `country_event`, `add_opinion_modifier`, `supports_us`, `add_tech_bonus`, `CAT_construction`, `modify_treasury_effect`.

### icp_membership — Membership Records

**HIGH**: Membership Records: 35 Tage/0,5% BIP für lediglich +2% PP-Zuwachs.

**Vorschlag:** In Congress after Terror/Public Party Offices integrieren; separate aktive Karte entfernen, ID/Lieferbelege für Saves behalten. Kein weiterer Buchhaltungsbonus oder neues Zählsystem.

**Begründung:** Weniger Füllfoki verbessert den Spielverlauf mehr als ein übertriebener Statistikbonus für Mitgliederlisten.

Mechaniken: `has_country_flag`, `set_country_flag`, `unlock_decision_tooltip`.

### icp_union_autonomy — Independent Unions

**HIGH**: Independent Unions: +3 Stabilitätspunkte, −2% Militärfabrikleistung/+2% Sozialkosten; positiver Nutzen am Cap verloren.

**Vorschlag:** +8% Effizienzaufbau/+2 Stabilitätspunkte; −2% Militärfabrikleistung/+2% Sozialkosten behalten. Neu einmalig 1% BIP, 35 Tage. Gegenpol Unions of the Plan: +6% Effizienzmaximum/−2 Stabilitätspunkte statt bisher +3% Maximum. Nur gewähltes laufendes Modell aktiv.

**Begründung:** Mitbestimmung und Planausrichtung erhalten verschiedene produktive Ergebnisse. ICP/Aziz/Front-Gesamtpfad prüfen; nicht alle Gewerkschaftsmodelle stapeln.

Mechaniken: `production_factory_efficiency_gain_factor`, `production_factory_max_efficiency_factor`, `industrial_capacity_factory`, `social_cost_multiplier_modifier`, `stability_factor`.

### aziz_language_rights — Language in Schools

**HIGH**: Language in Schools: erneut +2 Stabilitätspunkte/+2% Sozialkosten, 35 Tage/1% BIP.

**Vorschlag:** Stabilitätsbonus durch einmalig +1,5 Prozentpunkte Alphabetisierung (LR_change=0.015) ersetzen. Laufend +2% Bildungskosten statt Sozialkosten. 1% BIP/35 Tage; geltende Sprach-/Nordvereinbarung beachten, keine automatische Autonomie.

**Begründung:** Unterrichtszugang wirkt im vorhandenen Bildungssystem. Mengen sind Balancevorschläge, keine historische Statistik.

Mechaniken: `set_temp_variable`, `LR_change`, `update_literacy_rate`, `education_cost_multiplier_modifier`.

### aziz_safe_return — Bring the Exiles Home

**MEDIUM**: Bring the Exiles Home: austauschbar +2% Forschung/+2% Bürokratie, 35 Tage/1% BIP.

**Vorschlag:** Einmalig 1×30% CAT_industry und für 365 Tage −8% Bildungskosten statt dauerhafter Forschung/Bürokratie. 1% BIP/35 Tage bleiben. Keine frei erfundenen Bevölkerungs-/Manpowerpunkte.

**Begründung:** Rückkehrende Erfahrung als begrenzte Ausbildung; keine erzwungene Ausreise fremder Spieler oder Gratisbevölkerung.

Mechaniken: `add_tech_bonus`, `CAT_industry`, `add_timed_idea`, `education_cost_multiplier_modifier`.

### civic_electoral_register — An Electoral Register

**HIGH**: An Electoral Register: 35 Tage/1% BIP, dauerhaft ausschließlich +2% Bürokratie und Wahlfreischaltung.

**Vorschlag:** Registerarbeit in Civilian Politics aufnehmen, vorhandene Wahlentscheidung dort freischalten. Separate Karte entfernen, alte ID behalten. Wahl bleibt echte kostenpflichtige politische Entscheidung; keine automatische Ernennung.

**Begründung:** Wahlen sind ein realer institutioneller Ausgang und benötigen keinen zweiten Verwaltungsfokus mit rein negativem Dauerpaket.

Mechaniken: `unlock_decision_tooltip`, `country_event`, `has_country_flag`.

### civic_universities — University Autonomy

**HIGH**: University Autonomy: +3% allgemeine Forschung/−3% Ideologieabwehr, 35 Tage/2% BIP.

**Vorschlag:** Einmalig 2×30% CAT_information_technology statt allgemeiner Forschung; −3% Ideologieabwehr behalten, laufend +2% Bildungskosten. 2% BIP/35 Tage; keine zusätzliche Forschungsstelle.

**Begründung:** Konkrete Wissenschaft statt Dauermultiplikator. Kategorie ist bereits für frühe Computertechnik vorhanden. Eingeschränkte Parteikontrolle bleibt Opportunitätskosten.

Mechaniken: `add_tech_bonus`, `CAT_information_technology`, `education_cost_multiplier_modifier`, `drift_defence_factor`.

### royal_settlement — Constitutional Charter

**HIGH**: Constitutional Charter endet hauptsächlich mit +8% offensivem Auslandseinfluss/+2% Bürokratie.

**Vorschlag:** receiving_investment_duration_modifier=−0.15 und +10% Einflussabwehr statt offensivem Einfluss; +2% Bürokratie behalten. 49 Tage/keine neue BIP-Gebühr. Jordanien-/Handelsangebote weiter zustimmungspflichtig; kein garantierter Investor.

**Begründung:** Alternative konstitutionelle Krone erhält Vertrags-/Finanzprofil. −0.15 ist nativer Modifier, keine Zusage exakt 15% weniger Baukalendertage.

Mechaniken: `receiving_investment_duration_modifier`, `foreign_influence_defense_modifier`, `bureaucracy_cost_multiplier_modifier`.

### royal_compensation — Compensation Tribunal

**MEDIUM**: Compensation Tribunal: 35 Tage/2% BIP für nur +2 Stabilitätspunkte/+2% Bürokratie.

**Vorschlag:** Stabilität ersetzen durch +10% Infrastruktur-Baugeschwindigkeit für 365 Tage; +2% laufende Bürokratie und einmalig 2% BIP behalten. Kein automatischer Landtransfer oder Geld an nicht definierte Empfänger.

**Begründung:** Rechtsklarheit ermöglicht öffentliche Projekte; zeitlicher Bauzyklus statt gecapptem Stimmungsgift. Gegenentwurf für alternative Restauration.

Mechaniken: `production_speed_infrastructure_factor`, `add_timed_idea`, `bureaucracy_cost_multiplier_modifier`.

### kdp_local_policing — Local Police Charter

**HIGH**: Local Police Charter: nur +2 Stabilitätspunkte/+2% Bürokratie, 35 Tage/1% BIP.

**Vorschlag:** Bei respektierter akzeptierter Nordvereinbarung 180 Tage −10 Punkte eigener Widerstandszielbeitrag in irakisch besessenen/kontrollierten Nordstaaten mit bereits aktivem, richtigem Widerstandsakteur. Eigene Target-ID; bei Vertragsbruch entfernen. +2% Bürokratie/1% BIP/35 Tage behalten, Stabilität entfernen.

**Begründung:** Lokale Polizei verändert konkrete Sicherheit ohne nationale Kampfkraftprämie. Keine neuen Widerstände erzeugen, kein pauschales Löschen; US-/Counterinsurgency-Zielbeiträge gemeinsam rechnen.

Mechaniken: `add_resistance_target`, `remove_resistance_target`, `has_resistance`, `occupied_country_tag`, `is_owned_and_controlled_by`, `bureaucracy_cost_multiplier_modifier`.

### puk_student_exchange — Iraqi Student Exchange

**MEDIUM**: Iraqi Student Exchange ist dasselbe +2% Forschung/+2% Sozialkosten-Paket wie andere Schulungsnetze.

**Vorschlag:** Einmalig 1×35% CAT_construction statt Dauerforschung; +2% Bildungskosten statt Sozialkosten, 1% BIP/35 Tage. Regional Universities behält breiteres +3%-Forschungsprogramm.

**Begründung:** Gezielte technische Anschlussfähigkeit für PUK-Verkehrs-/Baukette; nicht dieselbe globale Wissenschaft zweimal stapeln.

Mechaniken: `add_tech_bonus`, `CAT_construction`, `education_cost_multiplier_modifier`.

### dawa_medical_network — Community Medicine

**HIGH**: Community Medicine ist exakt dasselbe +3 Stabilitätspunkte/+4% Sozialkosten-Paket wie IIP Community Welfare und Saddam Oil and Legitimacy.

**Vorschlag:** 730 Tage −10% reale Gesundheitskosten statt Stabilität; laufend +2% Sozialkosten. 2% BIP/35 Tage bleiben. Ersparnis wirkt nur auf tatsächliche Gesundheitsausgaben, erzwingt keine Gesetzesstufe und zahlt kein Geld aus.

**Begründung:** Medizin arbeitet am bestehenden Gesundheitsbudget. Effizienz und Dauer sind Balancevorschläge, keine behauptete universelle Überlegenheit religiöser Wohlfahrt.

Mechaniken: `health_cost_multiplier_modifier`, `social_cost_multiplier_modifier`, `add_timed_idea`.

### dawa_independent_iraq — An Iraqi Programme

**HIGH**: An Iraqi Programme: +6% Ideologieabwehr/−3% eigener Auslandseinfluss schützt nicht unmittelbar vor iranischem Einfluss.

**Vorschlag:** Zusätzlich +15% foreign_influence_defense_modifier; +6% Ideologieabwehr und −3% offensiven Einfluss als Kosten geringerer Aktivität behalten. 35 Tage/keine BIP-Gebühr; keine kostenlose Vertrags-/Darlehensaufhebung.

**Begründung:** Eigene Einflussnahme und Abwehr fremden Einflusses sind getrennte native Größen.

Mechaniken: `foreign_influence_defense_modifier`, `foreign_influence_modifier`, `drift_defence_factor`.

### sciri_revolutionary_courts — Revolutionary Courts

**HIGH**: Revolutionary Courts ist identisch mit religiösen Rechtsprüfungen: +2 Stabilitätspunkte/+3% Bürokratie, 35 Tage/1% BIP.

**Vorschlag:** In tatsächlichen Clerical-Executive-Verfassungsvertrag integrieren; separate aktive Karte entfernen, ID behalten. Garantien/Revision im vorhandenen bezahlten Verfassungssystem abbilden; keine neuen Kampf-/Forschungsboni für politische Gerichte.

**Begründung:** Unterschiedliche Institutionen statt weiterer Gerichtsverwaltungsrechnung. Repression ist kein zusätzlicher Ressourcenlieferant; spätere SCIRI-Formation bleibt bindend.

Mechaniken: `COLDWAR_IRQ_adopt_constitution_executive`, `COLDWAR_IRQ_constitution_executive_active`, `has_country_flag`, `country_event`.

### iip_business_law — Small Business Law

**HIGH**: Small Business Law: nur +2% allgemeiner Bau/+2% Bürokratie, 35 Tage/1,5% BIP.

**Vorschlag:** +10% Baugeschwindigkeit ausschließlich ziviler Fabriken und −3% Steuereinnahmen im laufenden IIP-Programm. 1,5% BIP/35 Tage behalten. Keine sofort erzeugte Fabrik oder Geld; der Spieler muss wirklich bauen.

**Begründung:** Erkennbares privates Produktionsprogramm statt Dawa-/SCIRI-Sozialpaket. Steuervergünstigungen sind die reale Gegenleistung.

Mechaniken: `production_speed_industrial_complex_factor`, `tax_gain_multiplier_modifier`.
