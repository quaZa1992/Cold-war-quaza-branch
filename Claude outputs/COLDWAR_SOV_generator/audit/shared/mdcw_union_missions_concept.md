# Konzept: Unionsmissionen – Missionen der Republiken, Moskaus Urteil, Belohnungen (18.10.2026, Entscheidungen eingearbeitet)

Status: **Konzept entschieden** (Enes, 18.10.2026), noch nichts gebaut. Umsetzungsplan: `Claude outputs/COLDWAR_SOV_generator/audit/shared/union_missions_implementation_plan.md` (Projekt: `claude/mdcw_union_missions_implementation_plan.md`). Grundlage sind Enes' Vorgabe vom 18.10.2026 und drei Agenten-Berichte unter `Claude outputs/COLDWAR_SOV_generator/audit/shared/`:
- `hoi4_shared_focus_mechanics.md`: shared/joint focus in HOI4
- `md_coldwar_feasibility.md`: was in MD 2.0.2 / unserer Mod geht
- `shared_union_tree_ideas.md`: Ideensammlung für den gemeinsamen Unionsbaum

Enes' Vorgabe: Die SSRs müssen **Missionen** erfüllen. Bei einem Fehlschlag entscheidet der **Sowjet-Spieler**, ob und wie er bestraft: Zivilfabriken oder Büros für z. B. zwei Monate wegnehmen, Einnahmen abschöpfen, den Republikführer absetzen – oder gar nicht strafen. Bei Erfolg gibt es Buffs für eine Weile. Offen ist noch, ob die Buffs nur für die erfüllende SSR und die Sowjetunion gelten oder für alle.

---

## 0. Kurzfassung

- **Mechanik:** HOI4-**Missionen**. Das sind zeitlich begrenzte Entscheidungen mit Countdown-Balken (`days_mission_timeout`). Erfüllt die Republik das Ziel vor Ablauf, gibt es den Erfolg. Läuft die Zeit ab, bekommt Moskau ein Urteils-Event.
- **Moskaus Urteil:** vier Stufen, von „Begnadigen“ bis „Ersten Sekretär ablösen“. Jede Strafe kostet Moskau etwas (Zusammenhalt, PP, Balance). Harte Hand treibt so die Republiken in Richtung Souveränität. Das ist die eingebaute Bremse über bestehende Systeme.
- **Empfehlung:**
  - **Hybrid-Vergabe:** ein automatisches Jahresziel pro Republik, dazu wenige Sonderdirektiven Moskaus.
  - **Schwellen-Belohnung:** persönlicher Buff für den Erfüller und für Moskau, dazu ein Unionsbuff für alle Erfüller, wenn genug Republiken liefern.
  - **Pripiski als Versuchung:** Erfüllung melden, ohne zu erfüllen.

---

## Entscheidungen von Enes (18.10.2026) – gelten vor allen Abschnitten unten

1. **Unionsbaum = Joint Focus** (Saadabad-Stil).
   - Start mit etwa 12 Foki (Umsetzungsplan §1.7). Jeder Fokus ist nur für Moskau, nur für Republiken oder für alle.
   - Mitglieder bekommen nur positive Belohnungen.
   - Megaprojekte und Endspiel folgen später.
2. **Vergabe: Hybrid mit eigener Wahl der Spieler.**
   - Bei der Januar-Sitzung bekommt jede Republik das Event **„Gosplan's Draft for [Jahr]“** mit **3 Missionen zur Wahl**:
     - eine passend zu Moskaus Planpriorität (Belohnung ×1,5)
     - eine regionale
     - eine allgemeine
   - Ohne Wahl nach 15 Tagen gilt die Prioritätsmission. Die KI nimmt die Prioritätsmission.
   - Dazu darf Moskau höchstens **2 Sonderdirektiven pro Republik und Fünfjahrplan** vergeben (25 PP). Moskau wählt Republik und Mission.
3. **Frist des Jahresziels: ~300 Tage**, Ende vor der nächsten Januar-Sitzung. Die Abrechnung läuft am 1. Januar.
4. **Belohnung: Schwelle 9 von 14.**
   - Die Erfüller und Moskau bekommen ihren Buff.
   - Ab 9 Erfüllern gibt es „The Plan Is Fulfilled!“ für alle Erfüller und Moskau.
   - Unter 5 Erfüllern bekommt Moskau Plan Shortfall.
5. **Stufe 2: alle vier wirtschaftlichen Strafen** wählbar:
   - Zivilfabriken requirieren (60 Tage; Moskau bekommt dieselbe Zahl frei)
   - Einnahmen abschöpfen (0,3 % BIP)
   - Büros drosseln (60 Tage)
   - **Bauen verlangsamen** (60 Tage Baugeschwindigkeit −20 %, Moskau +5 %)
   
   Jede kostet Zusammenhalt −1.
6. **Absetzen des Ersten Sekretärs: Moskau wählt den Weg.**
   - **Mit Politbüro-Abstimmung** (neuer Abstimmungstyp „Kaderfrage“): 100 PP, Zusammenhalt −3.
   - **Per Dekret** ohne Abstimmung: 150 PP, Zusammenhalt −5, Moskau bekommt „Defying the Politburo“.
   - **Scheitert die Abstimmung:** Es passiert nichts, die Kosten sind weg. Das Dekret bleibt möglich.
   - **Die betroffene Republik stimmt mit.** Das ist historisch realistisch: Absetzungen wurden formal einstimmig beschlossen, der Betroffene war dabei und „bat selbst um Entlassung“, z. B. Schelest im April 1973.
7. **Kein Urteil nach 15 Tagen = keine Strafe.**
8. **Moskau bestimmt alles selbst.** Nach jedem Fehlschlag sind alle Stufen 0–3 frei wählbar, es gibt keine Eskalationsvoraussetzung. Statuswerte sperren nichts mehr, sie **verteuern** nur:
   - Strafe gegen eine Republik mit Kaderschutz oder „Patron in Moscow“: zusätzlich Zusammenhalt −2 und „Defying the Politburo“.
   - Strafe gegen einen Sitzinhaber: Zusammenhalt −1 extra.
   - **Generalsekretärs-Kurs**:
     - Breschnews „Barone“: Stufe 2–3 kosten doppelten Zusammenhalt.
     - Romanows eiserne Disziplin: Stufe 2 kostet keinen Zusammenhalt.
     - Andropows Disziplin: Absetzen kostet die Hälfte, wenn Pripiski aufgeflogen sind.
     - Gorbatschows Chosrastschot: zusätzliche Option „Plan Shortfall only“ ohne Strafe.
9. **Souveränitätserklärung = raus aus dem Unionssystem:** keine Missionen, keine Strafen, keine Joint-Belohnungen mehr.

**Von mir gesetzte Standards** (änderbar):
- **Nachfolger:** die historischen Nachfolger aus dem Umsetzungsplan §4.3, z. B. Schtscherbyzkyj, Pugo, Schewardnadse, Kolbin.
- **Requirierung:** 25 % der Zivilfabriken, abgerundet, mindestens 1.
- **Pripiski:** Die bestehende Pripiski-Entscheidung und „Report Fulfilment“ werden zu einer zusammengelegt.
- **Anbindung:** im generischen 1970-Baum der Republiken mit einer Zeile, kein eigener Republikbaum. Sonst verlören die Republiken ihre 349 generischen Foki.
- **Präfix:** `COLDWAR_UNI_`.

---

## 1. Der Kreislauf

```
1. Januar (Politbüro-Sitzung, Event 10)
   └─ jede SSR bekommt ihr Jahresziel (Mission, 365 Tage)        ← automatisch
   └─ Moskau darf zusätzlich Sonderdirektiven vergeben             ← gezielte Entscheidung, kostet PP
        │
        ├─ Ziel erreicht  → Erfolg: Buff für die SSR + Beitrag für Moskau (+ Zähler für den Unionsbuff)
        ├─ „Erfüllung gemeldet“ (Pripiski) → zählt als Erfolg, Risiko späterer Aufdeckung
        └─ Zeit abgelaufen → Fehlschlag: Event „Plan Failure in [Republik]“ an Moskau
                               └─ Moskau wählt das Urteil (Stufe 0–3); ohne Antwort nach 15 Tagen: Stufe 0
                               └─ die SSR bekommt die Folge als Event mit eigener Reaktion
31. Dezember / nächste Januar-Sitzung
   └─ Abrechnung: Anteil der erfüllten Jahresziele → Unionsbuff (Modell C), News „Das Planjahr 1973“
```

---

## 2. Technik (was HOI4/MD hergibt)

| Baustein | Einsatz | Sicherheit |
|---|---|---|
| Missionen: `days_mission_timeout`, `activation`, `available` (= Ziel erreicht), `complete_effect`, `timeout_effect`, `cancel_trigger` | Jahresziele und Direktiven, Countdown sichtbar im Entscheidungsmenü der SSR | **sicher**: MD nutzt es (`Russia.txt`, `investments_decisions.txt`) |
| `activate_mission = <id>` im Scope der Republik | Moskau vergibt eine Direktive: `UKR = { activate_mission = … }` | sicher (Vanilla) |
| Gezielte Entscheidungen (`targets`, `target_trigger`) | „Issue a Directive to [Republik]“, „Pass Judgement on [Republik]“ | sicher (Vanilla, bei uns schon für Sitze genutzt) |
| `civilian_factory_use` in Idee oder dynamischem Modifikator | Zivilfabriken binden (Strafe) bzw. freigeben (Moskaus Gewinn, negativer Wert) | **sicher**: MD nutzt +3/+2/+1 und −1 (Iran, Polen, China) |
| Dynamische Modifikatoren mit Variablenwerten | Strafe skaliert mit der Größe der Republik (z. B. 25 % ihrer Zivilfabriken) | sicher (MD und wir nutzen es) |
| `offices_productivity`, `office_park_income_tax_modifier`, `tax_gain_multiplier_modifier` | Büros und Einnahmen drosseln | sicher: MD-Modifikatoren |
| Unsere Geldhelfer `COLDWAR_SOV_transfer_gdp_share` / `pay_gdp_share` | Einnahmen abschöpfen (BIP-Anteil von der SSR an Moskau) | sicher (unser System) |
| `retire_country_leader` + `create_country_leader` im Scope der SSR | Ersten Sekretär ablösen | sicher |
| Zählen von Gebäuden (`num_of_civilian_factories`, Gebäudestufen per `any_owned_state`) | Ziel „+1 Fabrik/Kraftwerk“ gegenüber dem Stand bei Missionsbeginn | **prüfen**: Wert beim Start in eine Variable schreiben |
| Politbüro-Abstimmung `COLDWAR_SOV_start_vote` | Kaderwechsel (Stufe 3) nur mit Beschluss | sicher (unser System, neuer Abstimmungstyp nötig) |

**Achtung:** Laut Agenten-Scan haben die SSRs 1970 fast keine Industrie (insgesamt ~10 Zivilfabriken in 85 Staaten).
- **Strafen** in festen Fabrikzahlen wären entweder wirkungslos oder vernichtend. Deshalb skalieren sie: ein Anteil, mindestens 1.
- **Missionsziele** müssen klein sein, z. B. „+1 Gebäude“.

---

## 3. Wer vergibt die Missionen? Drei Konzepte

### A – Planziele (automatisch)
Jede SSR bekommt am 1. Januar ein **Jahresziel** aus ihrem Profil (Region + aktuelle Planpriorität Moskaus).
- **Vorteile:**
  - Läuft auch mit KI-Moskau oder abwesendem Spieler.
  - Gleich für alle, keine Schikane möglich.
  - Wenig Klickarbeit für den SOV-Spieler.
- **Nachteile:**
  - Moskau steuert nichts.
  - Wenig Interaktion, ein reines „PvE“-Gefühl.

### B – Moskauer Direktiven (Sowjet-Spieler vergibt)
Moskau vergibt per gezielter Entscheidung Missionen aus dem Katalog (§4) an einzelne Republiken. Das kostet PP; Moskau wählt Ziel und Frist.
- **Vorteile:**
  - Maximale Interaktion und Rollenspiel.
  - Moskau lenkt die Unionswirtschaft wirklich.
- **Nachteile:**
  - Viel Last auf dem SOV-Spieler (14 Republiken).
  - Missbrauchsgefahr: Dauerschikane einer Republik.
  - Ohne aktiven SOV-Spieler passiert nichts.

### C – Hybrid (entschieden, mit eigener Wahl der Republik – siehe Entscheidung 2)
- **Basis:** das automatische Jahresziel aus A.
- **Dazu:** höchstens **2 Sonderdirektiven pro Republik und Fünfjahrplan** aus B. Sie kosten Moskau 25 PP, sind schwerer und belohnen stärker.
- Eine Republik hat nie mehr als **2 aktive Missionen** gleichzeitig.
- **Vorteile:** Grundrauschen ohne Aufwand, gezielter Druck möglich, Missbrauch begrenzt.
- **Nachteil:** etwas mehr Code als A oder B allein.

---

## 4. Missionskatalog (Vorschlag zum Festlegen)

Ziele sind klein und messbar, die Frist ist 365 Tage (Direktiven 180–365 Tage). „+1“ heißt gegenüber dem Stand bei Missionsbeginn. Bauen bezahlt die SSR normal über das MD-Geldsystem.

### 4.1 Allgemein (jede Republik)
| # | Mission (EN-Name im Spiel) | Ziel | Belohnung SSR (180 Tage) | Beitrag Moskau |
|---|---|---|---|---|
| 1 | **Fulfil the Industrial Plan** | +1 Zivilfabrik | Baugeschwindigkeit +5 %, PP +5 % | Gosplan-Linie +0,01 Produktion (180 T.) |
| 2 | **Power for the Plan** | +1 Kraftwerk | Energieverbrauch −5 %, Stabilität +2 % | PP +15 |
| 3 | **The Harvest Quota** | +1 Agrardistrikt | Agrarproduktivität +5 %, Stabilität +2 % | Konsumgüter −1 % (180 T.) |
| 4 | **Roads of the Union** | +1 Infrastruktur in 2 Staaten | Bau Infrastruktur +10 % | PP +10 |
| 5 | **Plan Deliveries** | Entscheidung „Deliver to the Union Fund“: 0,2 % BIP an Moskau | PP +5 %, Zusammenhalt +1 | erhält den Betrag |
| 6 | **Party Discipline** | Stabilität ≥ 50 % am Fristende | PP +5 %, Stabilität +2 % | Balance 0,01 Richtung orthodox |
| 7 | **The Komsomol Brigades** | Entscheidung: 5.000 Arbeitskräfte für ein Unionsprojekt | Kriegsunterstützung +2 %, Rekrutierbare Bev. +1 % | Arbeitskräfte +5.000 / Projektfortschritt |
| 8 | **Clean Up the Apparatus** | Korruption um 1 Stufe senken *(nur Direktive, schwer)* | PP-Kosten Gesetze −10 %, Stabilität +3 % | Zusammenhalt +1 |

### 4.2 Regional (Profil der Republik; ersetzt im Jahresziel eine allgemeine Mission)
| Region | Mission | Ziel | Besonderheit |
|---|---|---|---|
| Ukraine, Belarus | **Steel and Tractors** | +1 Zivil- oder Rüstungsfabrik | Mit Moskaus Priorität „Rüstung“ zählt nur die Rüstungsfabrik, Belohnung ×1,5 |
| Ukraine, Litauen, Armenien | **Atoms for the Republic** | +1 Kernkraftwerk *(Direktive)* | Erhöht das bestehende RBMK-Risiko (Event 45): Erfolg mit Preis |
| Baltikum | **Ports of the Union** | +1 Werft oder Marinebasisstufe | „Schaufenster des Sozialismus“: zusätzlich Stabilität ≥ 60 % für doppelte Belohnung |
| Georgien, Armenien, Aserbaidschan | **Black Sea and Caspian** | GEO Infrastruktur/Stabilität; AZE Ölförderung (+1 Ressourcen-/Raffineriegebäude); ARM Industrie | Ölpreis bleibt unberührt (nur Förderung) |
| Usbekistan, Turkmenien, Tadschikistan, Kirgisien | **White Gold** | +1 Agrardistrikt (Baumwolle) | Pripiski-Versuchung am größten. Jede Erfüllung erhöht das Aral-Risiko (bestehendes Event 46) |
| Tadschikistan, Kirgisien | **Nurek and Toktogul** | +1 Kraftwerk *(Direktive)* | Wasser gegen Energie, verknüpfbar mit dem Ideenpapier §4-E |
| Kasachstan | **Virgin Lands Harvest / Baikonur** | Agrardistrikt bzw. Infrastruktur im Staat Baikonur | Baikonur-Erfolg gibt Moskau Raumfahrtfortschritt (prüfen) |
| Moldau | **Orchards and Vineyards** | +1 Agrardistrikt | – |

### 4.3 Steuerung durch Moskaus Planpriorität
Die Planpriorität (Gruppe A, Gruppe B, Rüstung, Ernährungsprogramm) wählt im **Jahresziel** die passende Mission:
- **Gruppe A:** Industrie
- **Rüstung:** Fabriken
- **Ernährungsprogramm:** Ernte
- **Gruppe B:** Infrastruktur oder Disziplin

So hängt das Missionssystem an der bestehenden Planabstimmung, ohne Parallelsystem.

---

## 5. Moskaus Urteil bei Fehlschlag

Bei Ablauf bekommt Moskau das Event **„Plan Failure in [Republik]“** (Timeout 15 Tage). Jede Stufe ist eine Option. Die gewählte Folge geht als Event an die SSR, oft mit eigener Reaktion.

| Stufe | Option (EN) | Folge für die SSR | Kosten / Folge für Moskau |
|---|---|---|---|
| **0** | **Accept Their Explanations** (keine Strafe) | nichts | Zusammenhalt +1 (höchstens +1 pro Planjahr), Balance 0,01 Richtung Reform |
| **1** | **A Severe Party Reprimand** | PP −50; Idee „Reprimanded“ 90 Tage: Stabilität −2 % | keine; Balance 0,01 Richtung orthodox |
| **2a** | **Requisition Their Capacity** („Zivilfabriken wegnehmen“) | 60 Tage `civilian_factory_use` = 25 % ihrer Zivilfabriken, mind. 1 | 60 Tage dieselbe Zahl **frei** (negativer `civilian_factory_use`); Zusammenhalt −1 |
| **2b** | **Gosplan Takes the Offices** („Büros wegnehmen“) | 60 Tage Büroproduktivität −25 %, Bürosteuer −20 % | 60 Tage Steuereinnahmen +1 %; Zusammenhalt −1 |
| **2c** | **Levy the Shortfall** („Einnahmen abschöpfen“) | sofort 0,3 % BIP an Moskau (Transfer-Helfer) | erhält den Betrag; Zusammenhalt −1 |
| **3** | **Replace the First Secretary** („Leader absetzen“) | Führer abgesetzt, Moskaus Mann eingesetzt (Eigenschaft „Moscow's Man“: PP −10 %, Kompromat-Immunität); Stabilität −10 % für 180 Tage | 100 PP, Zusammenhalt −3, Balance 0,05 Richtung orthodox |

**Reaktion der SSR auf Stufe 3** (eigenes Event, historisch: Jeltoqsan 1986, Tiflis 1978):
- **Accept Moscow's Choice:** Die Stabilitätsstrafe halbiert sich nach 90 Tagen.
- **The Streets Answer:** Zusammenhalt −5. Die Volksfront-Entscheidung öffnet sofort. Die Stabilitätsstrafe bleibt.

### Eskalation und Schutz (ursprünglicher Vorschlag – ersetzt durch Entscheidung 8: Moskau wählt frei, Status verteuert nur)
- **Nur nach einem Fehlschlag.** Es gibt keine Strafe ohne gescheiterte Mission und pro Fehlschlag genau ein Urteil.
- **Stufe 2** höchstens einmal pro Republik und 365 Tage.
- **Stufe 3** nur, wenn **zwei Fehlschläge im selben Fünfjahrplan** vorliegen oder **Pripiski aufgeflogen** sind. Zusätzlich braucht sie einen **Politbüro-Beschluss** (neuer Abstimmungstyp „Kaderfrage“, Moskauer Block orthodox). Die Republiken mit Sitz stimmen mit. Höchstens einmal pro Plan und Republik.
- **Bestehende Statuswerte wirken mit:**
  - **Kaderschutz** (Antrag Typ 7) sperrt Stufe 3.
  - **Patron in Moscow** begrenzt auf Stufe 1.
  - **Sitzinhaber:** Jede Strafe kostet Moskau zusätzlich Zusammenhalt −1.
- **Generalsekretäre ändern die Regeln** (passt zum bestehenden Muster):
  - Breschnews `trust_the_local_barons`: höchstens Stufe 1.
  - Andropows Disziplin: Stufe 3 schon nach einem Fehlschlag mit Pripiski.
  - Romanows eiserne Disziplin: Stufe 2 kostet keinen Zusammenhalt.
  - Gorbatschow (Chosrastschot): Fehlschlag ohne Urteil, nur „Plan Shortfall“.
- **Transparenz:** Die Missions-Tooltip zeigt vorher, welche Stufen Moskau bei einem Fehlschlag offenstehen.
- **Abwesender SOV-Spieler:** Ohne Antwort gilt Stufe 0. Es gibt keine Strafe ohne aktive Entscheidung.
- **Die Bremse über bestehende Systeme:** Harte Strafen senken den Unionszusammenhalt. Unter 55 öffnet „Declare Sovereignty“, unter 35 das Referendum, unter 15 das Krisen-Event 44. Ein Moskau, das ständig straft, verliert die Union.

---

## 6. Belohnungen: für wen?

### Modell 1 – Nur wer liefert (die SSR + Moskau)
- **Vorteile:**
  - Klare Verantwortung, kein Trittbrettfahren, einfach zu bauen und zu verstehen.
  - Moskau profitiert von jeder Erfüllung, hat also Interesse an fairen Zielen.
- **Nachteile:**
  - Kein Gemeinschaftsgefühl.
  - Starke Republiken (Ukraine, Belarus) ziehen davon.
  - Schwache geraten in eine Abwärtsspirale aus Strafe und fehlendem Buff.

### Modell 2 – Alle profitieren (alle SSRs + Moskau bei jeder Erfüllung)
- **Vorteile:**
  - Gruppengefühl und Gruppendruck im Discord („Wegen euch kriegen wir nichts“).
  - Keine Abwärtsspirale für Schwache.
- **Nachteile:**
  - Trittbrettfahrer.
  - Die eigene Leistung ist kaum spürbar.
  - Bei 14 Republiken stapeln sich die Buffs. Das ginge nur als „auffrischen statt stapeln“, ist dann aber fast ein Dauerbuff.
  - Moskau gewinnt immer.

### Modell 3 – Schwelle / Hybrid (Empfehlung)
- **Persönlich:** Die erfüllende SSR bekommt ihren Missionsbuff (180 Tage), Moskau seinen kleinen Beitrag.
- **Union:** Bei der Januar-Abrechnung bekommen **alle Republiken, die ihr Jahresziel erfüllt haben, und Moskau** den Unionsbuff **„The Plan Is Fulfilled!“**, wenn **mindestens 9 von 14** (≈ 60 %) ihr Ziel erreicht haben. Der Buff gilt 365 Tage: Stabilität +3 %, Baugeschwindigkeit +5 %, Zusammenhalt +2 für Moskau.
- **Wer verfehlt hat**, bekommt den Unionsbuff nicht.
- **Unter 5 von 14:** Moskau bekommt „Plan Shortfall“ (bestehende Idee).
- **Vorteile:** Kooperation **und** Verantwortung. Die Starken haben Grund, den Schwachen zu helfen (Unionsprojekte, Lieferverträge). Für Moskau ist der Unionsbuff wertvoller als jede Strafe.
- **Nachteile:**
  - Etwas mehr Code: ein Jahreszähler als Status, keine Loyalitätswerte, also verträglich mit der Regel vom 15.10.
  - KI-Republiken brauchen eine faire Erfolgsquote.

**Optional dazu:** das **„Transferable Red Banner“** für die Republik mit den meisten erfüllten Missionen im Plan, aus dem Ideenpapier §4-B.

---

## 7. Pripiski: melden statt erfüllen

Während eine Mission läuft, kann die SSR die Entscheidung **„Report Fulfilment“** nehmen.
- **Sofort:** Die Mission zählt als erfüllt, mit voller Belohnung und Zähler für den Unionsbuff. Gesetzt wird das bestehende Flag `COLDWAR_SOV_pripiski`.
- **Risiko:** die bestehende Untersuchung (`COLDWAR_SOV_investigate_republic`): 15 % + 5 % je Korruptionsstufe + 25 % mit Pripiski, Andropow +20 %.
- **Aufgedeckt:**
  - Die Belohnung wird entfernt.
  - Der Fehlschlag wird nachträglich gezählt (wichtig für die Eskalation).
  - „In Disgrace“ (bestehende Idee).
  - Moskau bekommt sofort ein Urteil mit freigeschalteter Stufe 3.

Das ist die historische Baumwollaffäre als Spielmechanik.

---

## 8. KI

- **KI-Moskau** urteilt nach der Balance des Generalsekretärs:
  - **Reformer** (Kossygin, Gorbatschow): Stufe 0–1.
  - **Neutral** (Breschnew): Stufe 1.
  - **Orthodox** (Suslow, Andropow, Romanow, Ustinow): Stufe 2. Bei aufgeflogenen Pripiski auch Stufe 3, wenn die Abstimmung durchgeht.
- **KI-Republiken** erfüllen ihr Jahresziel mit etwa 75 % Wahrscheinlichkeit: verdeckter „AI-Boden“, damit KI-lastige Runden den Unionsbuff nicht blockieren. Pripiski nutzt die KI nicht (wie heute).
- **KI-Moskau vergibt keine Sonderdirektiven**, nur die Jahresziele laufen.

---

## 9. Einbettung in den gemeinsamen Unionsbaum (Shared Tree)

Der gemeinsame Baum (Ideenpapier) liefert die **Werkzeuge**, das Missionssystem die **Pflicht**:
- **SSR-Fokusse im Plan-Zweig:**
  - „Storming the Plan“ (Schturmowschtschina): Eine laufende Mission ist sofort erfüllt, Stabilität −3 %.
  - „The Tolkachi“: Frist +90 Tage.
  - „The Counter-Plan“: freiwillig eine schwerere Mission mit Belohnung ×1,5.
  - „Keep Reserves in Hand“: Pripiski-Risiko −10 %.
- **SOV-Fokusse:** „The People's Control Committee“ (Untersuchungen billiger), „Gosplan Directives“ (Sonderdirektiven 15 PP statt 25) und die Generalsekretärs-Regeln aus §5.
- **Technik des Baums:**
  - `shared_focus` für die Plan-Zweige, jede Republik erledigt ihre eigene Kopie.
  - `joint_focus` nur für Plan-Abschlüsse mit kleinen positiven Effekten: Ein gemeinsamer Fokus wirkt in den Bäumen der Mitspieler, siehe MP-Hinweis im Ideenpapier §2.
  - Vorlage ist MDs Tschechoslowakei-Baum (gemischt joint/shared).
  - Die SSRs nutzen heute den generischen 1970-Baum. Entweder kommt der Zweig dort hinein, oder es gibt einen kleinen eigenen Republikbaum, dann aber auf die Fallback-Whitelist setzen.

---

## 10. MP-Regel – Ausnahme (entschieden)

Neue Ergänzung der MP-Regel:

> „Ausnahme: Im Unionsmissions-System bestimmt Moskau nach einer **gescheiterten** Mission frei die Strafe (Stufe 0–3, Absetzen mit oder ohne Politbüro). Die Bremse sind die Kosten: PP, Unionszusammenhalt, ‚Defying the Politburo‘ und der Weg zur Souveränität.“

## 11. Stand

Alle Entscheidungen aus der Konzeptphase sind getroffen, siehe oben.

**Vor dem Bau:** Der Umsetzungsplan empfiehlt zuerst einen Smoke-Test des Sowjet-1970-Systems im Spiel. Missionen hängen an der Politbüro-Sitzung, den Abstimmungen und den Geldhelfern.

**Im Spiel zu testen:**
- Joint Focus bei Republiken, die Subjekte sind
- laufende Foki der Mitglieder bei einem Joint-Abschluss
- Absetzen und Nachfolger-Porträts
- Requirierung über den dynamischen Modifikator
- Missionstitel mit Scripted Loc

**Aufwand laut Plan:** 60–80 Stunden Entwicklung inklusive drei Testrunden.
