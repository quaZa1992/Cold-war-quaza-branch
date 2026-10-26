# BRD 1970: Plan für die deutsch-deutsche Rivalität, die Innere Sicherheit und den neuen Fokusbaum

Stand: 17.10.2026. Dieser Plan ist noch nicht umgesetzt; es wurde nichts an der Mod geändert. Er baut auf dem bestehenden Generator auf (`tools/west_germany_1970/`) und ersetzt dessen Teile Schritt für Schritt.

Es gibt drei Arbeitspakete:

- **A. „Deutsch-deutsches Verhältnis“:** ein eigenes Minispiel mit eigenem Fenster (im Stil von *Cold War Equilibrium*). Das Verhältnis kann sich entspannen, in Krisen geraten und im schlimmsten Fall in einen Krieg kippen.
- **B. „Lagezentrum Innere Sicherheit“:** RAF, Rechtsterror und internationaler Terror werden sichtbar und spielbar, ebenfalls mit eigenem Fenster.
- **C. Neuer Fokusbaum:** aufgebaut nach dem Vorbild von MDs Russland- und Israel-Baum, vor allem in der Art der Effekte.

---

## 0. Befund: was am jetzigen Stand schlecht ist

Der aktuelle Baum im Vergleich mit den MD-Vorbildern (gezählt in den Dateien):

| Kennzahl | BRD 1970 heute | MD Russland | MD Israel |
|---|---|---|---|
| Fokusse | 213 | 806 | 667 |
| Kosten | 183 × 7, sonst 5–10 | überwiegend 3, dann 5 und 7, selten 2 | überwiegend 5, 2 und 3, dazu 4 und 6 |
| `relative_position_id` | 0 | 800 | durchgängig |
| Dynamische Modifikatoren über Fokusse ausgebaut (`modifies_dynamic_modifier_tt`) | 0 | 287 | 0 (arbeitet mit `swap_ideas`) |
| `unlock_decision_tooltip` | 0 | 117 | 3 |
| MD-Einfluss (`change_influence_percentage`) | 0 | 73 | 161 |
| Bau von Gebäuden in Staaten | 25 | 78 | 63 |
| `swap_ideas` (Geist entwickelt sich weiter) | 0 | 53 | 81 |
| Kriegspfade (`will_lead_to_war_with` / `create_wargoal`) | 0 / 0 | 50 / 44 | 26 / 22 |
| `add_opinion_modifier` | 58 | 148 | 216 |

Was daraus folgt:

1. **Die Fokusse sind zu teuer und gleichförmig.** Fast alle kosten 70 Tage und geben „+PP, +Stabilität, ein Geist“. Bei MD ist ein Fokus kurz, und er greift fast immer in ein System ein: Er baut einen bestehenden Geist um, schaltet eine Entscheidung frei, verschiebt Einfluss, setzt Meinungen oder baut in einem konkreten Staat.
2. **Kein wachsender Kern-Geist.** Russland hat einen dynamischen Modifikator pro Säule, und jeder Fokus verändert ihn sichtbar per `modifies_dynamic_modifier_tt`. Bei uns stapeln sich 55 Einzelgeister.
3. **Die Systeme sind unsichtbar.** RAF, Rivalität und Spionage laufen als Variablen und Missionen im Hintergrund. Der Spieler sieht nur Ereignisse. Es fehlt eine Oberfläche, auf der er den Zustand liest und gezielt handelt.
4. **Die Rivalität mit der DDR hat keine Eskalation.** Es gibt Krisenstufen der DDR (Ausreisewelle → Wende), aber keine zwischenstaatliche Krise, keine Entspannungsleiter und keinen Weg in den Krieg.

---

## A. Minispiel „Deutsch-deutsches Verhältnis“

### A.1 Grundidee

Bonn und Ost-Berlin spielen ein laufendes Zwei-Parteien-Spiel. Es gibt:

- eine **Klima-Achse** von −100 (Konfrontation) bis +100 (Verflechtung);
- eine **Eskalationsleiter** mit sieben Stufen;
- eine **Entspannungsleiter** aus Verträgen;
- **Krisen**, die in Runden ausgetragen werden;
- **Hebel** auf beiden Seiten;
- **Gesprächskanäle**, die offen oder geschlossen sind;
- **Initiative**: Aktionspunkte, mit denen jede Seite pro Monat handelt.

Die DDR ist ein KI-Gegner mit eigener Persönlichkeit, je nach SED-Chef. Spielt jemand die DDR, sieht er dasselbe Fenster gespiegelt (Phase 4, optional).

Das Minispiel ersetzt die bisherigen Wende-Meter nicht, sondern sitzt darüber. Die bestehenden DDR-Meter werden zu den Hebeln Bonns:

| Bestehender DDR-Meter | Wird im Minispiel zu |
|---|---|
| Devisenmangel, Abhängigkeit von Bonn | Hebel „Devisen“ |
| Westmedien-Reichweite | Hebel „Medien“ |
| Ausreisedruck | Hebel „Menschen“ (auch als DDR-Druckmittel) |
| SED-Kontrolle | Widerstandskraft der DDR gegen Druck |
| Moskauer Garantie | Rückendeckung der DDR in Krisen |
| Anerkennung | Hebel „Anerkennung“ der DDR |

### A.2 Kernvariablen (Präfix `cwgg_`, beim Land GER, die DDR-Seite gespiegelt bei DDR)

| Variable | Bereich | Bedeutung |
|---|---|---|
| `cwgg_klima` | −100…+100 | Grundstimmung zwischen beiden Staaten |
| `cwgg_druck` | 0…100 | kurzfristiger Eskalationsdruck aus Zwischenfällen; zerfällt um 10 % pro Monat |
| `cwgg_stufe` | 0…6 | Eskalationsstufe (siehe A.3) |
| `cwgg_vertrag` | 0…9 | erreichte Stufe der Entspannungsleiter (siehe A.5) |
| `cwgg_init_brd` / `cwgg_init_ddr` | 0…6 | Initiative (Aktionspunkte) |
| `cwgg_gesicht_brd` / `cwgg_gesicht_ddr` | −50…+50 | Ansehen und Verhandlungsposition aus gewonnenen oder verlorenen Krisen |
| `cwgg_buendnis` | 0…100 | Rückhalt der Westmächte für Bonns Kurs |
| `cwgg_mob_brd` / `cwgg_mob_ddr` | 0…3 | Alarmstufe der Streitkräfte |
| `cwgg_krise_typ`, `_int`, `_phase`, `_tage`, `_runde` | | aktive Krise (eine zur Zeit; eine zweite nur als „Nebenkrise“ ohne Runden) |
| `cwgg_kanal_<n>` | 0/1/2 | Kanal geschlossen / offen / belastet (Stasi-Verdacht) |
| `cwgg_hebel_<n>` | 0…3 | Stufe eines Hebels |
| `cwgg_log_1..3` | Code | die letzten drei Meldungen für den Lagebericht im Fenster |

### A.3 Eskalationsleiter

```
 0 MODUS VIVENDI   ●───────────────────────────────  Klima ≥ 40
 1 KÜHLE KOEXISTENZ ●──────────────────────────────  10 ≤ Klima < 40
 2 SPANNUNGEN      ●──────────────────────────────  −20 ≤ Klima < 10
 3 KRISE           ●────────────  Krisenintensität ≥ 50   oder Klima < −20
 4 KONFRONTATION   ●────────────  Intensität ≥ 75         oder Klima < −45
 5 KRIEGSGEFAHR    ●────────────  Intensität ≥ 90 und Klima < −60, oder beide Seiten auf Alarmstufe 3
 6 KRIEG           ●────────────  nur über einen der Kriegspfade in A.8
```

- **Hysterese:** Nach unten fällt die Stufe erst 5 Punkte unter, nach oben erst 5 Punkte über der Schwelle. So flackert sie nicht.
- **Modifikatoren:** Jede Stufe setzt einen dynamischen Modifikator *Innerdeutsches Verhältnis* bei GER und DDR (mit variablengetriebenen Werten).

| Stufe | Wirkung (GER, DDR entsprechend) | Imperia |
|---|---|---|
| 0 | +Konsumgüter-Entlastung über den innerdeutschen Handel, +3 % Stabilität, −5 % Kriegsunterstützung, Übersiedler-Abkommen günstiger | −0,3 Spannung/Monat |
| 1 | +1 % Stabilität | ±0 |
| 2 | −2 % Stabilität, +3 % Kriegsunterstützung | +0,2 Spannung/Monat |
| 3 | −4 % Stabilität, +6 % Kriegsunterstützung, +10 % Kosten für Entspannungsaktionen | +0,5/Monat |
| 4 | −6 % Stabilität, +10 % Kriegsunterstützung, Wehrpflicht-Akzeptanz steigt, innerdeutscher Handel halbiert | +1/Monat |
| 5 | −8 % Stabilität, +15 % Kriegsunterstützung, −5 % Fabrikleistung (Vorbereitung), Friedensbewegung +3/Monat | +2/Monat; Weltspannung mindestens 70 |
| 6 | Krieg (siehe A.8) | Spannung 100 |

### A.4 Klima: monatliche Bewegung

Pro Monat:

```
klima += (basis − klima) × 0,05 + Aktionen + Ereignisse − druck × 0,1
```

Die **Basis** (dahin strebt das Klima, wenn niemand handelt) setzt sich zusammen aus:

- erreichter Entspannungsstufe: +4 je Vertrag;
- Weltspannung (Imperia): `−(Spannung − 50) / 4`;
- SED-Chef:
  - Ulbricht −10;
  - Honecker −5, ab 1981 0 (Devisenhunger);
  - Krenz −5;
  - Modrow +15;
  - ein Reformer +20;
- Moskauer Linie:
  - Breschnew-Doktrin −10;
  - Neues Denken +10;
  - Sinatra-Doktrin +15;
  - Putsch der Hardliner −25;
- BoP *Deutschlandpolitik*: Seite „Rechtsposition“ bis −10, Seite „Wandel durch Annäherung“ bis +10;
- Bonner Regierung:
  - CDU/CSU allein −5;
  - Koalition mit CSU-Vorsitz im Kabinett −3;
  - Grüne in der Regierung +3;
- NATO-Nachrüstung beschlossen −5, Null-Lösung +5;
- offene Kanäle: +2 je offenem Kanal.

### A.5 Entspannungsleiter (Verträge)

Jede Sprosse ist ein **Verhandlungsprojekt**. Der Ablauf:

1. Der Spieler klickt „Verhandlungen aufnehmen“. Das kostet Initiative und PP.
2. Es läuft ein Fortschrittsbalken (60–180 Tage). Der Fortschritt pro Monat hängt von Klima, offenen Kanälen und der Laune der DDR-KI ab.
3. Krisen pausieren den Fortschritt. Eine Krise ab Stufe 4 bricht ihn ab.
4. Am Ende steht ein Ereignis: Abschluss, Nachverhandlung oder Scheitern.
5. Im Bundestag muss die Mehrheit stehen (bestehende Bundestagsarithmetik). Scheitern kann eine Ratifikationskrise auslösen (bestehendes Ereignis zu den Ostverträgen).

| # | Sprosse | Historisches Vorbild | Voraussetzung | Ertrag |
|---|---|---|---|---|
| 1 | Treffen der Regierungschefs | Erfurt (19.3.1970) und Kassel (21.5.1970) | Klima ≥ −10, Fokus *Wandel durch Annäherung* | Kanal *Bahr–Kohl* öffnet; Klima +10 |
| 2 | Berlin-Regelung | Viermächteabkommen (3.9.1971), Transitabkommen (17.12.1971) | Sowjetunion ist nicht feindlich; Klima ≥ 0 | Transitkrisen −60 % Häufigkeit; Transitpauschale als Hebel; gemeinsames Berlin-Flag mit dem SOV-Baum |
| 3 | Grundlagenvertrag | 21.12.1972 | Sprossen 1 und 2, Mehrheit im Bundestag | Basis +8; DDR-Anerkennung +15; Hallstein-Krisen enden; Option *Brief zur deutschen Einheit* (Einheitsweg bleibt offen) |
| 4 | UNO-Beitritt beider Staaten | 18.9.1973 | Sprosse 3 | DDR-Anerkennung +10; BRD-Weltrolle +; Imperia-Spannung −2 |
| 5 | Ständige Vertretungen | Mai 1974 (Gaus in Ost-Berlin) | Sprosse 3 | Kanal *Ständige Vertretung* öffnet dauerhaft; +1 Initiative pro Monat |
| 6 | Verkehrs- und Postabkommen, Reiseerleichterungen | 1972–1980er | Klima ≥ 20 | Westmedien und Ausreisedruck +; Konsumgüter-Entlastung |
| 7 | Kulturabkommen, Städtepartnerschaften | Kulturabkommen Mai 1986, Saarlouis–Eisenhüttenstadt 1986 | Klima ≥ 30, ab 1980 | Basis +4; Zivilopposition in der DDR + |
| 8 | Staatsbesuch des SED-Chefs in Bonn | Honecker, September 1987 | Klima ≥ 40, Sprosse 5 | Basis +6; SED-Kontrolle −5 (Erwartungen wecken); CDU-Rechte verärgert |
| 9 | Vertragsgemeinschaft oder Konföderation | Zehn-Punkte-Plan (1989), Modrow (1990) | Wende-Stufe ≥ 3 oder Klima ≥ 70 mit Reformer an der Spitze | öffnet den bestehenden Konföderationsweg zur Einheit |

Die Gegenrichtung gibt es auch: Mit der Aktion **Vertrag aussetzen** fällt eine Sprosse weg (Klima −20, Westmächte uneins). Über die BoP-Seite *Rechtsposition* lassen sich Verträge auch nur eingeschränkt umsetzen.

### A.6 Hebel und Kanäle

**Hebel Bonns.** Jeder Hebel hat die Stufen 0–3; der Ausbau kommt über Fokusse und Aktionen. Ein Hebel wird pro Krise oder Verhandlung eingesetzt und gibt dort Boni:

| Hebel | Quelle | Einsatz |
|---|---|---|
| **Devisen** | Swing, Milliardenkredit (1983/84), Transitpauschale | Verhandlungsfortschritt +; in Krisen „Geld gegen Nachgeben“. Kostet Treasury (MD) und stärkt kurzfristig die DDR-Wirtschaft |
| **Menschen** | Häftlingsfreikauf (historisch rund 33.700 Häftlinge für rund 3,4 Mrd. DM) | senkt den Ausreisedruck kontrolliert; gibt Gesicht im Inland. Kostet Treasury |
| **Medien** | ARD/ZDF-Reichweite, RIAS, Deutsche Welle | Druck auf die SED-Kontrolle; in Krisen „Öffentlichkeit herstellen“ |
| **Recht** | Alleinvertretung, Salzgitter-Erfassungsstelle, Staatsangehörigkeit | moralischer Druck; blockiert die DDR-Anerkennung, senkt aber das Klima |
| **Bündnis** | Drei Mächte für Berlin, NATO | ruft die Alliierten in Krisen; abhängig von `cwgg_buendnis` und der US-Meinung |
| **Handel** | innerdeutscher Handel, EG-Sonderstatus | Kreditstopp oder Lieferstopp als Sanktion; verbindet sich mit den Imperia-Sanktionen |

**Hebel Ost-Berlins** (von der KI benutzt; im Fenster sichtbar):

| Hebel | Wirkung |
|---|---|
| **Transitwege** | Schikane auf der Autobahn, Sperrung der Zugangswege nach West-Berlin |
| **Menschen** | Zwangsumtausch erhöhen (Oktober 1980 auf 25 DM), Ausreisen stoppen oder als Ventil öffnen, Ausbürgerung (Biermann, November 1976) |
| **Stasi/HVA** | Spionage (bestehender Spionagekrieg); belastet Bonner Kanäle; kann der RAF Unterschlupf bieten (siehe B) |
| **Moskau** | Rückendeckung in Krisen; Truppenbewegungen der GSSD |
| **Anerkennung** | diplomatische Offensive in der Dritten Welt (Hallstein-Bruch) |
| **Grenzregime** | Schießbefehl, Selbstschussanlagen SM-70, Minen; Grenzzwischenfälle |

**Kanäle** (offen 1 / belastet 2 / geschlossen 0). Ein offener Kanal senkt die Chance, dass eine Krise eskaliert. Er ist Voraussetzung für die Krisenantwort *Geheimkanal* und gibt Klima-Basis. Jeder offene Kanal kann von der Stasi angezapft werden; das Risiko hängt von der bestehenden Stasi-Penetration ab:

| Kanal | Öffnen über | Besonderheit |
|---|---|---|
| Bahr–Kohl | Sprosse 1 oder Fokus | stark in Vertragsverhandlungen |
| Ständige Vertretung | Sprosse 5 | dauerhaft, +1 Initiative |
| Anwaltskanal Vogel–Stange | Fokus *Freikauf* | schaltet den Hebel *Menschen* frei; in Ausreisekrisen +50 % |
| Schalck-Golodkowski (KoKo) | Fokus *Strauß-Kredit* oder CDU-Regierung | Devisengeschäfte; Korruptionsrisiko (MD-Korruption) |
| Kirchenkanal (EKD/BEK) | Fokus *Kirche im Sozialismus* | stärkt die Zivilopposition; in Dissidentenkrisen stark |
| Heißer Draht Bonn–Moskau | Moskauer Vertrag | in Kriegsgefahr: einmal pro Krise −30 Intensität |

### A.7 Krisen: Erzeugung, Runden, Ausgang

**Erzeugung.** Pro Monat:

```
p = 1 % + 0,15 % × max(0, −klima) + 0,1 % × druck
```

- Nach einer Krise gibt es eine Sperrfrist von 6 Monaten.
- Der Typ wird nach Epoche und Lage gewichtet (siehe Tabelle unten).
- Einige Krisen haben feste Auslöser aus bestehenden Systemen:
  - Spionageaffäre, wenn ein Maulwurf enttarnt wird;
  - Botschaftsflüchtlinge bei Wende-Stufe 1;
  - Raketenkrise beim NATO-Doppelbeschluss (12.12.1979) bzw. bei SS-20-Flags im SOV-Baum;
  - Manöverkrise bei Weltspannung ≥ 80 (Vorbild Able Archer, November 1983).

**Ablauf einer Krise.** Sie hat eine Intensität von 0–100, Startwert je nach Typ 30–55.

- Sie läuft in **Runden zu je 15 Tagen**.
- In jeder Runde wählt der Spieler im Fenster **eine Haltung**. Ohne Wahl gilt *Abwarten*.
- Die DDR-KI wählt verdeckt ihre Antwort. Beide Wahlen werden zu Beginn der nächsten Runde aufgedeckt.
- Ein Lagebericht beschreibt den Zug der Gegenseite.

Haltungen Bonns:

| Haltung | Kosten | Wirkung (Grundwert) |
|---|---|---|
| **Abwarten** | – | Intensität ±0, Gesicht −2 |
| **Deeskalieren** | 1 Initiative | Intensität −10; Gesicht −5; bei CDU/CSU-Opposition ein Glaubwürdigkeitsmalus im Bundestag |
| **Standhaft bleiben** | 1 Initiative, 10 PP | Intensität +5; Gesicht +5 |
| **Gegendruck** (Hebel einsetzen) | 2 Initiative + Hebelkosten | Intensität +10; DDR-Gesicht −10; Zusatzwirkung je Hebel |
| **Alliierte einschalten** | 1 Initiative; `cwgg_buendnis` ≥ 40 | Intensität −5 oder +10 (wenn Moskau ebenfalls gerufen wird); Krise wird zur **Großmachtkrise**: Bonn verliert Kontrolle (Souveränitätsmalus, Gesicht −5), USA und UdSSR entscheiden mit; Imperia-Spannung +3 |
| **Geheimkanal** | 2 Initiative, offener Kanal | Intensität −15 × Kanalqualität; Stasi-Leck-Risiko (dann Gesicht −10, Kanal belastet) |
| **Mobilmachung vorbereiten** | ab Stufe 4; 3 Initiative | `cwgg_mob_brd` +1, Intensität +15; Abschreckung: DDR-*Verschärfen* verliert 50 % Wirkung; Friedensbewegung + |

Antworten der DDR: **Nachgeben**, **Hinhalten**, **Verschärfen**, **Moskau anrufen**, **Gegenangebot** (fordert Devisen oder Anerkennung).

**Auszahlungsmatrix** (Intensität; Gesicht BRD/DDR):

| BRD ↓ / DDR → | Nachgeben | Hinhalten | Verschärfen | Moskau anrufen | Gegenangebot |
|---|---|---|---|---|---|
| Abwarten | −5; +2/−5 | 0; −2/+2 | +10; −5/+5 | +10; −5/+3 | 0; −2/0 |
| Deeskalieren | −20; 0/0 | −10; −3/+3 | +5; −10/+10 | 0; −8/+5 | −15, Angebot annehmbar |
| Standhaft | −10; +8/−8 | +5; +2/−2 | +15; +3/+3 | +15; 0/+3 | +5; +3/−3 |
| Gegendruck | −10; +12/−12 | +5; +5/−5 | +25; ±0 (Spirale) | +25; −3/+5 | +10; +5/−5 |
| Alliierte | −15; +6/−6 | −5; +3/−3 | +5; +2/−2 | +10, Großmachtkrise | −5 |
| Geheimkanal | −25; +4/+4 | −15; +2/+2 | −5; 0/0 | −10 | −20, Deal möglich |
| Mobilmachung | −15; +10/−10 | +10; +5/−5 | +30; ±0 | +30, Moskau mobilisiert | +15 |

Die Grundwerte werden mit folgenden Faktoren skaliert:

- Krisentyp (jeder Typ hat eine „stärkste“ Haltung, siehe Tabelle unten);
- eingesetzte Hebel;
- Moskauer Garantie (wirkt auf *Verschärfen* und *Moskau anrufen*);
- SED-Kontrolle;
- `cwgg_mob_*` (Abschreckung);
- `cwgg_buendnis`.

**Ausgang.**

- **Intensität ≤ 0:** Die Krise ist **beigelegt**. Wer mehr Gesicht gesammelt hat, „gewinnt“.
  - Sieg Bonns: Klima −5 bis +10 je nach Weg; im Inland Stabilität und Regierungspartei +; Westmächte +.
  - Sieg der DDR: Anerkennung +, SED-Kontrolle +, Bonner Regierungspartei − (Bundestagswahl), Opposition gewinnt Ostpolitik-Themen.
- **Zeitablauf** (6–10 Runden): **Erstarrung**. Klima −10, Druck +20, die Krise flammt nach 3 Monaten mit 50 % Wahrscheinlichkeit wieder auf.
- **Intensität ≥ 100: Höhepunkt.** Ein Entscheidungsereignis mit drei Optionen:
  1. **Einlenken:** Gesicht −20, Klima +10, die Opposition greift an (Misstrauensvotum-Risiko über die bestehende Mehrheitslogik).
  2. **Härte zeigen:** Stufe 5; ein Countdown von 30 Tagen beginnt.
  3. **Moskau/Washington vermitteln lassen:** nur mit Heißem Draht oder `cwgg_buendnis` ≥ 60; Ausgang nach Großmachtlage.

  Im Countdown kann jede Seite noch einlenken. Halten beide durch, folgt die Kriegsprüfung (A.8).

**Krisentypen** (jeder mit eigener Ereigniskette: Ausbruch, je Runde ein Lagebericht, Höhepunkt, Ausgang; dazu ein eigener Sonderknopf):

| Typ | Epoche | Start | Stärkste Antwort | Sonderknopf | Folgen |
|---|---|---|---|---|---|
| **Transitkrise** (Berlin-Zugang) | 1970–71 stark, nach Sprosse 2 selten | 40 | Alliierte (Drei Mächte) | *Luftbrücke vorbereiten* (Treasury, Transportflugzeuge; Intensität −20, DDR-Gesicht −15) | West-Berlin-Staat: Stabilität und Industrie −, Berlinförderung |
| **Grenzzwischenfall** (Todesopfer an der Grenze) | ganzer Zeitraum, öfter bei Grenzregime 3 | 35 | Standhaft + Hebel Medien | *Vor die UN-Menschenrechtskommission* | Recht + / Klima − |
| **Spionageaffäre** | ausgelöst durch enttarnten Maulwurf | 45 | Geheimkanal | *Agentenaustausch auf der Glienicker Brücke* | bei Kanzleramts-Spion: Rücktrittsereignis (Vorbild Guillaume, 1974) |
| **Botschaftsflüchtlinge** | Wende-Stufe ≥ 1 | 50 | Geheimkanal Vogel / Diplomatie | *Sonderzüge aushandeln* (Vorbild Prag, 30.9.1989) | Ausreisedruck +, Übersiedler-Schub |
| **Anerkennungskrise** (ein Drittstaat erkennt die DDR an) | nur vor Sprosse 3, BoP *Rechtsposition* | 30 | Recht / Handel | *Beziehungen abbrechen* (Hallstein) oder *hinnehmen* | MD-Einfluss im Drittstaat −/+ |
| **Raketenkrise** (SS-20 / Pershing II) | 1977–1987 | 45 | Alliierte; Geheimkanal Moskau | *Null-Lösung vorschlagen* | Friedensbewegung, Hofgarten, Imperia-Spannung |
| **Manöverkrise** | Weltspannung ≥ 80 | 55 | Heißer Draht | *Manöver absagen* (Gesicht −5, Intensität −30) | Fehlalarm-Risiko (Kriegspfad D) |
| **Dissidentenkrise** (Ausbürgerung, Haft prominenter Oppositioneller) | 1976–1989 | 30 | Medien / Kirchenkanal | *Aufnahme anbieten* | Zivilopposition + |
| **Elbe-Grenzstreit** (Talweg oder Ostufer) | 1970–1989 | 25 | Recht | *Grenzkommission* | gering; gut zum Gesichtsammeln |
| **Volksaufstand in der DDR** | Wende-Stufe 9 und zweite Welle | 70 | — | *Grenze öffnen / helfen / stillhalten* | Kriegspfad C |

**DDR-KI.** Pro Runde wird die Antwort gewichtet nach:

- Persönlichkeit:
  - Ulbricht: Verschärfen ×1,5, Gegenangebot ×0,5;
  - Honecker: Hinhalten ×1,5; ab 1981 Gegenangebot ×2;
  - Krenz: Hinhalten;
  - Modrow und Reformer: Nachgeben und Gegenangebot;
- Devisenmangel (hoch → Gegenangebot);
- Moskauer Garantie (hoch → Verschärfen und Moskau anrufen);
- SED-Kontrolle (niedrig → Nachgeben);
- Gesicht (unter −20 → riskiert mehr);
- `cwgg_mob_brd` (hoch → weniger Verschärfen);
- eine Zufallskomponente.

Zwischen den Krisen gibt die KI ihre DDR-Initiative für Hebel aus (Zwangsumtausch, Spionage, Anerkennungsoffensive, Bitte um Devisen). Jede Aktion erzeugt eine Meldung im Lagebericht.

### A.8 Kriegspfade (Stufe 6)

Ein Krieg ist der seltenste Ausgang und nie zufällig ohne Vorwarnung. Jeder Pfad führt über Stufe 5 und einen Countdown, in dem beide Seiten aussteigen können. Die Bonner KI wählt nie einen Angriffspfad.

| Pfad | Auslöser | Wer erklärt | Wer kämpft mit | Ziel |
|---|---|---|---|---|
| **A: Politik der Stärke** (Spieler) | Fokus *Befreiungsdoktrin* (Konfrontationszweig, `will_lead_to_war_with = DDR`), Stufe 5, Klima ≤ −80, `cwgg_mob_brd` = 3, Bestätigungsereignis mit zwei Rückfragen | GER | NATO nur, wenn `cwgg_buendnis` ≥ 70 und die USA-Meinung hoch ist; sonst Bonn allein. Die UdSSR tritt bei, wenn die Moskauer Garantie ≥ 40 ist | `create_wargoal` gegen die DDR (Annexion); Imperia-Spannung 100 |
| **B: Ostberliner Erpressung** | Stufe 5, Höhepunkt, Bonn hält durch, Moskauer Garantie ≥ 70 und Hardliner in Moskau (Breschnew-Doktrin oder Putsch) | DDR (Wurf: 15 % + 5 % je Runde Countdown) | Warschauer Pakt über MD-Fraktionen; NATO über Artikel 5 (MD-NATO) | Weltkrieg (WK III) |
| **C: Bruderhilfe** | Volksaufstand (Krisentyp 10), Bonn wählt *helfen* | GER (Spieler) | die DDR zerfällt in einen Bürgerkrieg (Aufständische als eigener Tag mit Kernen, Vorbild Mod-Bürgerkriegs-Mechanik); die UdSSR greift ein, wenn die Garantie ≥ 50 ist | Einheit unter Kriegsbedingungen |
| **D: Fehlalarm** | Manöverkrise auf Stufe 5, keine offenen Kanäle, beide Seiten auf Alarmstufe 3 | Wurf: 5 % pro Woche; Heißer Draht senkt ihn auf 1 % | wie B | Weltkrieg |

**Rund um den Krieg:**

- **Vor dem Krieg:** Das Ereignis *Verteidigungsfall* (Art. 115a GG) setzt Kriegsrecht-Modifikatoren. Es berührt die Bundestagsarithmetik (Gemeinsamer Ausschuss) und Kriegsunterstützung. Bei hoher Friedensbewegung gibt es Massenproteste (MD-Proteste).
- **Atomschwelle:** Ein Ereignis nach 30 Kriegstagen fragt, ob die NATO nukleare Erstverwendung freigibt. Es nutzt die vorhandene MD-Nuklearlogik; das prüfe ich bei der Umsetzung. Andernfalls bleibt es bei einem Flavor-Ereignis mit Spannung und Kriegsmüdigkeit.
- **Frieden durch Sieg Bonns:** Die Einheit wird erzwungen. Ein eigener Einheitsweg *Anschluss unter Besatzung* folgt: lange Aufbau-Ost-Last, Widerstand im Osten, Imperia-Ausrichtung bleibt westlich, die UdSSR bleibt feindlich.
- **Frieden durch Niederlage Bonns:** Neutralisierung (bestehender Neutralitätsweg, aber erzwungen) oder Gebietsverlust West-Berlins.
- **Ausstieg aus dem Countdown:** Jeder Countdown-Ausstieg kostet die aussteigende Seite Gesicht −25 und setzt Klima auf −40 (Kalter Frieden).

### A.9 Initiative (Aktionspunkte)

Bonn bekommt pro Monat 1 Initiative, +1 mit der Ständigen Vertretung, +1 durch Fokusse (*Kanzleramt als Lagezentrum*), +1 auf Stufe ≥ 3 (Krisenstab). Höchstens 6 Punkte.

Aktionen außerhalb von Krisen (Knöpfe im Tab *Hebel & Kanäle*; Abklingzeit 3–12 Monate):

| Aktion | Kosten | Wirkung |
|---|---|---|
| Swing-Kredit erhöhen | 1 I, Treasury | Devisenhebel +1; Klima +5; Abhängigkeit +5 |
| Milliardenkredit | 2 I, Treasury (nur CDU/CSU-Kanzler oder Kanal KoKo) | Klima +10; DDR baut Selbstschussanlagen ab (Grenzregime −1); CSU-Basis gespalten |
| Häftlinge freikaufen | 1 I, Treasury | Ausreisedruck −5, Inland +; Übersiedler-Schub |
| Transitpauschale neu verhandeln | 1 I | Transitkrisen seltener; Treasury −/Jahr |
| Medienoffensive | 1 I | Westmedien +5, SED-Kontrolle −3, Klima −5 |
| Alleinvertretung bekräftigen | 1 I, BoP → Rechtsposition | DDR-Anerkennung −5, Klima −8 |
| Kreditstopp / Lieferstopp | 2 I | Devisenmangel +10, Klima −15, Imperia-Wirtschaftssanktion optional |
| Fluchthilfe dulden | 1 I | Ausreisedruck +, Grenzzwischenfälle wahrscheinlicher |
| Grenznahe Manöver | 2 I | Abschreckung `cwgg_mob_brd` +1 (zeitweise), Klima −10, Druck +15 |
| Stasi-Netze ausheben | 2 I | Stasi-Penetration −10, belastete Kanäle wieder offen, Klima −5 |
| Gipfel vorschlagen | 2 I | startet eine Vertrags-Sprosse (A.5) |
| Kanal öffnen oder schließen | 1 I | siehe A.6 |

### A.10 Verzahnung mit dem Bestehenden

| System | Verbindung |
|---|---|
| **Imperia-Spannung** | Jede Eskalationsstufe gibt oder nimmt Spannung über `mdcw_cw_add_tension`. Weltspannung zieht die Klima-Basis. Weltspannung ≥ 80 erlaubt Manöverkrisen |
| **Imperia-Ausrichtung** | Bündnis unter 30 bei Stufe 0 heißt *Äquidistanz*-Risiko (bestehende Logik); Pfad A ohne NATO zieht westliche Opinion stark ab |
| **Imperia-Programme und Sanktionen** | Swing und Kredite laufen als Programm *Consumer Supply Credits*; Kreditstopp kann Imperia-Wirtschaftssanktionen setzen; Sieg nach Pfad C führt zu Sanktionen der UdSSR |
| **Imperia-Flüchtlinge** | Krisen „Botschaftsflüchtlinge“ und „Volksaufstand“ speisen `imp_refugees_taken_k` |
| **BoP Deutschlandpolitik** | Aktionen verschieben den BoP; der BoP verändert Kosten (Rechtsposition: Druckaktionen −1 I; Annäherung: Verträge −20 % Dauer) |
| **Bundestag und Wahlen** | Verlorene Krisen schwächen die Regierungspartei; Einlenken auf dem Höhepunkt startet das Misstrauensvotum-Risiko; Verträge brauchen die Mehrheit; Klima ist Wahlkampfthema (`MD4_election_campaign`) |
| **MD-Fraktionen** | DGB für Entspannung, BDI für Ost-Handel, Vertriebenenverbände (neu als Meinungswert, kein volles Fraktionssystem) gegen die Anerkennung |
| **MD-NATO** | Pfade B und D lösen Artikel 5 über die MD-NATO-Logik aus; Pfad A nur bei Zustimmung |
| **Spionagekrieg** | Stasi-Penetration belastet Kanäle; enttarnte Maulwürfe lösen die Spionageaffäre aus |
| **Wende-Stufen** | Klima beeinflusst Ausreisedruck und Zivilopposition; Wende-Stufe 3 setzt Stufe 0 und öffnet Sprosse 9 |
| **Sowjetischer 1970-Baum** | Doktrin-Fokusse ändern die Basis und die Moskau-Antwort der DDR-KI; Moskauer Vertrag öffnet den Heißen Draht |
| **RAF** (B) | Bei Klima < −30 gewährt die Stasi der RAF Unterschlupf und Logistik (historisch: zehn RAF-Aussteiger in der DDR 1980–82); die RAF-Logistik steigt. Im Gegenzug kann *Stasi-Netze ausheben* RAF-Kontakte aufdecken |

### A.11 Fenster „Deutsch-deutsches Verhältnis“

**Aufbau des Fensters:**

- **Größe und Grafik:** 780 × 700, gleiche Grafikbausteine wie `mdcw_cold_war` (Fensterhintergrund, Tabs, Knöpfe 160/96, Abschnittsköpfe, Balkenspuren). So passt es optisch zur Mod.
- **Topbar:** ein eigener Knopf neben *Cold War Equilibrium* (x = 1580), sichtbar nur für GER und DDR im 1970er-Szenario. Er zeigt ein Symbol und die aktuelle Stufe als Zahl; die Farbe der Zahl geht von Grün über Gelb und Orange bis Rot.
- **Zweiter Zugang:** über eine Entscheidungskategorie *Deutschlandpolitik* (Knopf „Lagekarte öffnen“).

**Kopfzeile** (in allen Tabs):

```
[Wappen BRD]  DEUTSCH-DEUTSCHES VERHÄLTNIS         Stufe 2: SPANNUNGEN   [X]
              Bundesrepublik · Kanzler Brandt        Initiative ●●●○○○
[Tab: Lage] [Tab: Krise] [Tab: Hebel & Kanäle] [Tab: Verträge]
```

**Tab 1 „Lage“:**

```
┌ Porträt Kanzler ┐   KLIMA  −100 ███████████▌░░░░░░░░ +100   [−12]   ┌ Porträt SED-Chef ┐
│ (Frame aus der  │   Basis: +4 (Tooltip: alle Summanden)                  │ (Frame aus der   │
│ Porträt-Sheet)  │                                                         │ Porträt-Sheet)   │
└─────────────────┘   ESKALATIONSLEITER  ○0 ○1 ●2 ○3 ○4 ○5 ○6              └──────────────────┘
                      Druck ███░░░░░░  27
 Gesicht BRD  +6  ████        Gesicht DDR  −3  ██
 Rückhalt der Westmächte  ██████████░░  71       Moskauer Garantie  ████████░░░  64
 ─ LAGEBERICHT ───────────────────────────────────────────────────────────
  • 03.1974  Ost-Berlin erhöht den Zwangsumtausch.
  • 02.1974  Ständige Vertretung: Gespräche über Reiseerleichterungen.
  • 01.1974  Grenzzwischenfall bei Helmstedt, ein Toter.
 ─ AKTIVE KRISE ──────────────  [Karte mit Typ, Intensität, Runde, „Zur Krise ▶“]
```

**Tab 2 „Krise“:**

- Krisenkarte (Typ-Bild, Titel, Phase, Intensitätsbalken, Runden-Timer).
- Darunter sieben Haltungsknöpfe mit Tooltips. Die Tooltips zeigen die erwartete Wirkung gegen die wahrscheinlichste DDR-Antwort (aus der KI-Gewichtung, als „Lagebeurteilung des BND“). Mit hoher BND-Stufe ist die Prognose genauer.
- Rechts: die letzte DDR-Antwort, die Haltung der Drei Mächte (USA/UK/F mit Text „unterstützt / zurückhaltend / drängt zum Ausgleich“), die Haltung Moskaus und der Sonderknopf des Krisentyps.
- Unten: „Ausgewählte Haltung: …“ mit Knopf „Zurücknehmen“ bis zum Rundenende.

**Tab 3 „Hebel & Kanäle“:**

- Links: sechs Bonner Hebel als Zeilen (Name, 3 Stufen-Pips, Aktion „Einsetzen“, Abklingzeit).
- Rechts: sechs DDR-Hebel (nur Anzeige, dazu Warnsymbol, wenn die KI ihn vorbereitet).
- Unten: sechs Kanal-Karten (offen / belastet / geschlossen, Qualität, Knopf „Öffnen“ bzw. „Schließen“) und der Abschnitt *Schattenkrieg* (Stasi-Penetration, Abwehr, Knopf „Netze ausheben“, Knopf „Doppelagent führen“ aus dem bestehenden Spionagekrieg).

**Tab 4 „Verträge“:**

- Die neun Sprossen als senkrechte Leiter, jeweils mit Zustand: gesperrt (Grund im Tooltip), verfügbar, in Verhandlung (Fortschrittsbalken), abgeschlossen, ausgesetzt.
- Knöpfe „Verhandlungen aufnehmen“ und „Vertrag aussetzen“.
- Rechts die Ratifikationslage (Mehrheit, Abweichler) aus der Bundestagsarithmetik.

**Technische Umsetzung** (wie im Mod-Muster):

- `scripted_gui` mit `context_type = player_context`; `dirty = global.cwgg_dirty`, das bei jeder Änderung hochgezählt wird.
- Tabs über `cwgg_tab`; Balken über Kind-GUIs mit `properties = { <fill> = { x = var } }`.
- Porträts als ein Frame-Sprite (Sheet aus den vorhandenen 20 kolorierten Porträts).
- Texte über `scripted_localisation`: Stufennamen, Kanalzustand, Lagebericht aus den `cwgg_log_*`-Codes.
- Klick-Effekte rufen dieselben Effekte auf wie die bisherigen Entscheidungen. Die betroffenen Entscheidungen (Deutschlandpolitik-Kategorie DR) werden versteckt bzw. entfallen, damit nichts doppelt existiert.
- Rechenlast: nur monatlicher Tick plus Klicks. In Krisen kommt ein Tick alle 15 Tage über eine versteckte Mission/Timer-Variable dazu.

---

## B. Lagezentrum Innere Sicherheit (RAF sichtbar machen)

### B.1 Warum die RAF heute nicht zu sehen ist

Das Terrormodell (Generationen, Kader, Milieu, Häftlinge, Geiselkette, GSG 9) läuft nur im Monatstick und zeigt sich ausschließlich über Ereignisse und zwei Missionen. Es gibt keine Anzeige, keine Ziele, keine Fahndung als Handlung. Das neue Fenster macht daraus ein Katz-und-Maus-Spiel.

### B.2 Neue Mechaniken

**1. Fahndungsliste („Köpfe“).** Statt einer anonymen Kaderzahl gibt es pro Generation 6–8 benannte Führungsfiguren als Karten. Jede Karte zeigt einen Zustand (flüchtig / Spur / verhaftet / tot / ausgestiegen) und einen Ortungswert von 0–100.

- **Ortung steigt durch:** BKA-Stufe, Rasterfahndung, Tipps aus der Bevölkerung (Belohnung), Kronzeugen.
- **Ortung sinkt durch:** Sympathisantenmilieu, Stasi-Unterschlupf (A.10), Auslandsaufenthalt (Jemen-Camps 1970, Naher Osten).
- **Ab 60 Ortung:** Knopf **Zugriff** (Erfolg nach Ortung und GSG-9- bzw. SEK-Stufe; ein Fehlschlag kann ein Feuergefecht mit Toten auslösen – Vorbild Bad Kleinen 1993 – und gibt dann Rechtsstaatsmalus und Milieu +).
- Eine Verhaftung senkt den aktiven Kader und erhöht die Häftlinge. Das ist wichtig, weil Geiselnahmen Häftlinge zum Freipressen brauchen.

Generationen, Figuren als historische Personen (Fahndungsplakat-Stil ohne Fotos, nur Silhouetten):

- 1. Generation: Baader, Ensslin, Meinhof, Raspe, Meins, Mohnhaupt (Bindeglied).
- 2. Generation: Mohnhaupt, Klar, Folkerts, Boock, Wisniewski, Schulz.
- 3. Generation: als anonymisierte „Kommandoebene“ mit Decknamen. Die Täter sind bis heute teils unbekannt, deshalb gibt es dort keine erfundenen Zuschreibungen.

**2. Anschlagsplanung der RAF und Personenschutz.** Die RAF-KI plant jeden Monat gegen eine von sechs Zielkategorien:

1. Justiz (Bundesanwaltschaft);
2. Wirtschaft (Vorstände, Arbeitgeberverband);
3. US-Streitkräfte;
4. Politik;
5. Infrastruktur und Gefängnisse;
6. Botschaften im Ausland.

Ablauf:

- Jede Kategorie hat einen **Planungsfortschritt** von 0–100, im Fenster als Balken. Je nach BKA-Aufklärung ist er unsichtbar, geschätzt (±25) oder genau.
- Der Spieler hat **Personenschutz-Kontingente**: 2 Schutzslots, +1 mit dem Fokus *BKA-Sicherungsgruppe*, +1 mit *Objektschutz der Bundespolizei*. Diese verteilt er auf Kategorien.
- Erreicht eine Planung 100, folgt der Anschlag. In einer geschützten Kategorie wird er mit 50–80 % vereitelt (Ereignis „Anschlag vereitelt“, Ortung des Kommandos +30). In einer ungeschützten Kategorie trifft er (Ereignis mit Opfer).
- Kategorien und Häufigkeiten folgen den Generationen:
  - 1972 Mai-Offensive: US-Hauptquartier Heidelberg, Springer, Polizei;
  - 1975 Stockholm (Botschaften);
  - 1977 Buback (7.4.), Ponto (30.7.), Schleyer (5.9.): Justiz und Wirtschaft;
  - 1979 Haig, 1981 Ramstein: US-Streitkräfte;
  - 1985 Zimmermann, 1986 Beckurts, 1989 Herrhausen (30.11.), 1991 Rohwedder (1.4.): Wirtschaft;
  - 1993 Weiterstadt: Gefängnisbau.
- Die Ereignisse nennen die historischen Opfer **nur**, wenn Datum und Lage ungefähr passen. Sonst kommt ein generisches Opfer derselben Kategorie, damit keine falschen historischen Zuschreibungen entstehen.

**3. Stammheim und Haftregime.** Für die Häftlinge gibt es drei Schalter:

- **Isolationshaft:** Milieu +, Hungerstreik-Risiko +, Ausbruch −.
- **Normalvollzug:** neutral.
- **Zusammenlegung:** Milieu −; Kommunikation erleichtert Anschläge der nächsten Generation.

Dazu kommt ein **Hungerstreik-Meter**. Ein Hungerstreik ab 80 kann zu einem Todesfall führen (Vorbild Holger Meins 1974): Milieu +20, 2. Generation +.

Die Ereignisse der „Todesnacht von Stammheim“ (18.10.1977) gibt es nur, wenn die Geiselkette mit Mogadischu endet. Sie bleiben ohne Schuldfestlegung, mit der historischen Kontroverse als Text.

**4. Krisenstab (Geiselnahme) im Fenster.** Die bestehende Mission *Das Ultimatum* erscheint als Karte mit:

- Countdown;
- Knöpfen „Stürmen“, „Razzia“, „Kontaktsperre“, „Nachgeben“ und neu „Hinhalten“ (Zeit kaufen: +5 Tage, Ortung +10, Milieu-Zorn);
- der Erfolgschance als Prozentzahl (aus GSG 9 und BKA).

Die bisherigen Entscheidungen entfallen dafür.

**5. Sicherheitsstaat gegen Rechtsstaat (Waage).** Zwei sichtbare Gegengewichte:

- **Sicherheitsapparat:** BKA, Rasterfahndung, INPOL, Kontaktsperregesetz 1977, Radikalenerlass 1972.
- **Rechtsstaatliche Glaubwürdigkeit.**

Jede harte Maßnahme gibt Sicherheit +, Rechtsstaat − und Milieu +. Die bestehenden Missbrauchsfälle (Traube, Celler Loch, Kießling) hängen an der Waage. Weiche Maßnahmen wirken umgekehrt:

- Aussteigerprogramm;
- Kronzeugenregelung (1989);
- Kinkel-Initiative (1992): Haftlockerung gegen Gewaltverzicht, führt zur Gewaltverzichtserklärung 1992 und zur Auflösung 1998, wenn das Milieu niedrig ist.

**6. Zweite und dritte Front.** In Kurzform sichtbar:

- **Rechtsterror:** Wehrsportgruppe Hoffmann (Verbot 1980), Oktoberfest-Attentat (26.9.1980) als Risiko, wenn die Rechtsterror-Bedrohung hoch und ohne Verbot ist; Knopf „Verbot“.
- **Internationaler Terror:** München 1972 als Auslöser der GSG 9 (Gründung September 1972), wenn der Fokus noch fehlt; Knopf „Grenzschutz-Sondereinheit aufstellen“.

### B.3 Fenster „Lagezentrum Innere Sicherheit“

Das Fenster ist 780 × 700 groß und hat einen zweiten Topbar-Knopf mit Stern-Symbol. Die Zahl zeigt die RAF-Bedrohung; bei einer aktiven Geiselnahme blinkt das Symbol rot.

| Tab | Inhalt |
|---|---|
| **Lage** | drei Bedrohungsbalken (RAF / rechts / international); Generationsabzeichen (1–4 mit Namen); Milieu, Kader, Häftlinge; die Waage Sicherheit gegen Rechtsstaat; Lagebericht (3 Zeilen) |
| **Fahndung** | Raster der Fahndungskarten (8 Slots) mit Ortungsbalken und Zugriff-Knopf; Knöpfe „Rasterfahndung“ (Kosten PP, Rechtsstaat −), „Belohnung aussetzen“ (Treasury), „Kronzeugen anwerben“ |
| **Schutz** | sechs Zielkategorien mit Planungsbalken (Genauigkeit nach BKA-Stufe), Schutzslot-Knöpfe, freie Kontingente |
| **Krisenstab** | aktive Geiselnahme bzw. Haftregime-Schalter, Hungerstreik-Meter, Aussteiger- und Dialogmaßnahmen |

### B.4 Verzahnung

- **MD-Terrorabwehr:** Die Modifikatoren `terror_threat_detection_modifier` und `terror_threat_base_defense_modifier` erhöhen die Ortung und die Vereitelungsquote.
- **MD-Proteste:** Isolationshaft und Hungertod speisen `protest_strength`; Radikalenerlass und Berufsverbote speisen die Studentenproteste.
- **MD-Korruption:** Das Celler Loch und Vertuschungen hängen an der Waage.
- **Rivalität:** Der Stasi-Unterschlupf senkt die Ortung von Aussteigern. *Stasi-Netze ausheben* oder die Wende-Stufe 4 (Akten offen) enthüllt Unterschlupf: Ereignis 1990 „RAF-Aussteiger in der DDR verhaftet“ mit Klima- bzw. Einheitswirkung.
- **NATO/USA:** Anschläge auf US-Streitkräfte senken die US-Meinung; Schutz dort hebt `cwgg_buendnis`.
- **Bundestag:** Ein „Deutscher Herbst“ (mehrere Anschläge in einem Jahr) gibt der Opposition Stimmen (Thema innere Sicherheit) und setzt die FDP-Bürgerrechtsflügel unter Druck (bestehender FDP-Kurs).

---

## C. Neuer Fokusbaum nach dem Vorbild von MDs Russland- und Israel-Baum

### C.1 Leitlinien (aus den Vorbildern übernommen)

1. **Kurze Fokusse:** 2 (Politik-Schnellschuss), 3 (Standard), 5 (Reform), 7 (Großprojekt). Ziel ist ein Durchschnitt um 4, statt 183 Fokusse zu je 7.
2. **Drei bis fünf Effektarten pro Fokus**, möglichst nie nur PP und Stabilität. Pro Fokus mindestens einer dieser Effekte:
   - **Kern-Geist umbauen** (Russland-Stil): `custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = … }` mit `add_to_variable = { VAR = … tooltip = …_tt }` und `newline = yes`;
   - **Geist austauschen** (Israel-Stil, `swap_ideas`), wenn ein Problem-Geist schrittweise gelöst wird;
   - **Entscheidung oder Knopf freischalten:** `unlock_decision_tooltip` bzw. „Schaltet im Fenster *Deutsch-deutsches Verhältnis* frei: …“ als `custom_effect_tooltip`;
   - **konkreter Staat:** `add_building_construction` in benannten Staaten, `build_railway`, Staats-Modifikatoren (dynamische Modifikatoren auf Staaten, wie MD);
   - **MD-Einfluss:** `percent_change`, `tag_index`, `influence_target`, `change_influence_percentage`;
   - **Meinungen und Fraktionen:** `add_opinion_modifier`, MD-Fraktionsmeinungen (DGB, BDI/BDA, Mittelstand), MD-EU (`europeanism_change`), Treasury und Debt über die MD-Effekte;
   - **BoP-Verschiebung** oder **Minispiel-Effekt** (Klima, Hebelstufe, Kanal, Initiative, Schutzslot, BKA-Stufe).
3. **`relative_position_id`** in jedem Fokus. Die Säulen werden relativ zu ihrem Hub positioniert; das Layout-Skript prüft weiterhin auf Überlappung.
4. **Hub-Fokusse** wie Russlands „Speak to …“: ein kurzer Einstieg pro Säule (Kosten 1–2), der den Kern-Geist der Säule einführt.
5. **Pfadabhängige KI:** `ai_will_do` liest Pfad-Flags (historisch / CDU-Wende / Konfrontation / Entspannung), die beim Start und nach Wahlen gesetzt werden. Die KI wählt nie den Kriegszweig.
6. **Suchfilter:** eigene `FOCUS_FILTER_GER_*` pro Säule plus die MD-Standardfilter.
7. **Gegenseitige Ausschlüsse** an echten Weggabelungen: Sozialliberal oder Wende, Entspannung oder Politik der Stärke, Einheitsweg.

### C.2 Kern-Geister (dynamische Modifikatoren, nach dem Muster der SOV-Modifikatoren)

| Kern-Geist | Säule | Variablen (Beispiele) | Startwert |
|---|---|---|---|
| **Bonner Republik** | Kanzleramt | Stabilität, PP, Parteipopularität der Regierung, Entscheidungskosten | leicht positiv |
| **Modell Deutschland** | Wirtschaft | Fabrikleistung, Konsumgüter, Steuereinnahmen (MD), Forschungstempo, Bau-Tempo | neutral |
| **Energiemix** | Energie | Ölabhängigkeit (MD-Ölverbrauch), Ressourcenfaktor, Stabilität bei Ölschocks | negativ (Ölabhängigkeit) |
| **Wehrhafte Demokratie** | Innere Sicherheit | Terrorabwehr-Modifikatoren, Rechtsstaat, Polizei-Kosten; speist B | neutral |
| **Armee im Bündnis** | Bundeswehr | Divisionsorganisation, Wehrpflicht, Ausrüstungs-Tempo, Ausbildungszeit, NATO-Interoperabilität | neutral |
| **Westbindung** | Westintegration | Handel und Meinung zu EG und NATO, Europeanism-Drift, Rückhalt `cwgg_buendnis` pro Monat | positiv |
| **Neue Ostpolitik** bzw. **Politik der Stärke** | Deutschlandpolitik | Klima-Basis, Initiative, Hebelkosten; wechselt per Fokus seine Identität (zwei Modifikatoren, einer aktiv) | – |
| **Wirtschaftsmacht, politischer Zwerg** → **Zivilmacht** | Weltrolle | Einfluss pro Monat, Entwicklungshilfe-Kapazität (Imperia), Exporte | negativ → positiv |

Die bisherigen 55 Einzelgeister werden größtenteils in diese Variablen überführt. Übrig bleiben nur echte Problem-Geister mit Lösungsweg per `swap_ideas`:

- Stagflation → Haushaltskonsolidierung;
- Bildungsnotstand → Bildungsexpansion;
- Bundesrat in Oppositionshand → Paketlösung;
- Last des Ostens → Solidarpakt.

### C.3 Neuer Aufbau (Säulen, Hubs, Pfade)

Gesamtumfang: rund 230–260 Fokusse; gleichzeitig spielbar sind etwa 140–160 wegen der Ausschlüsse.

```
                         ┌── Regierungserklärung 1969 („Mehr Demokratie wagen“) [2] ──┐
     ┌──────────┬────────┼─────────┬──────────┬──────────┬───────────┬──────────┐
 Kanzleramt  Modell D.  Energie  Wehrhafte  Armee im  Westbindung Deutschland- Weltrolle
  (Hub)       (Hub)     (Hub)    Demokratie  Bündnis    (Hub)     politik     (Hub)
                                  (Hub)      (Hub)                 (Hub)
                                                                     │
                                                       ┌─────────────┼───────────────┐
                                                 Wandel durch   Rechtsposition   Konfrontation
                                                 Annäherung     (CDU/CSU)        (exklusiv, Kriegspfad A)
                                                       └───────┬──────┘
                                                        Einheit (spät; erscheint mit Wende-Stufe ≥ 3)
                                                 Art. 23 | Art. 146 | Konföderation | Neutral (exklusiv)
```

**1. Kanzleramt** (Politik, ca. 32 Fokusse):

- Hub *Regierungserklärung*: setzt *Bonner Republik*.
- Teilpfade:
  - **Sozialliberal** (Mehr Demokratie wagen, Wahlalter 18, Bildungsreform, Mitbestimmung 1976, Radikalenerlass-Revision);
  - **Wende 1982** (konstruktives Misstrauensvotum als Fokus, nur bei FDP-Kurs > 40: löst das bestehende Ereignis `.26` und den Koalitionswechsel aus; geistig-moralische Wende, Privatisierungen);
  - **Grüne und Neue Mitte** (spät; Atomausstieg, Staatsbürgerschaftsreform).
- Effekte:
  - MD-Parteipopularität;
  - FDP-Kurs-Variable;
  - Bundesrat-Paket (`swap_ideas`);
  - im Minispiel +1 Initiative (*Kanzleramt als Lagezentrum*);
  - *Kanzlerprinzip* senkt die Entscheidungskosten;
  - Wahlalter 18 verschiebt die Parteipopularität (SPD/FDP +).

**2. Modell Deutschland** (Wirtschaft, ca. 38):

- Hub *Konzertierte Aktion*.
- Pfade: **Globalsteuerung** (Schiller/Schmidt) oder **Angebotspolitik** (Lambsdorff-Papier, Stoltenberg).
- Staatenbezogene Effekte nach Muster Israel. Die Staats-IDs werden bei der Umsetzung aus den MD-Staatsdateien ermittelt; bestätigt ist bisher West-Berlin 1251.
  - **Ruhrgebiet:** Strukturwandel. Kohle-Subventionen erhalten oder abbauen; Zivilfabriken +2, Ruhrkohle AG (1968) als Geist mit Ablaufdatum; Universitäten Bochum und Dortmund geben Forschungstempo.
  - **Saarland:** Stahlkrise (Saarstahl), Infrastruktur.
  - **Hamburg und Bremen:** Häfen +1, Werftenkrise.
  - **Baden-Württemberg und Bayern:** Hochtechnologie (Mikroelektronik, Luft- und Raumfahrt bei MBB) als Forschungsbonus mit Gebäuden.
  - **Niedersachsen:** VW, Transrapid-Teststrecke (Emsland) als Eisenbahn bzw. Infrastruktur.
  - **West-Berlin:** Berlinförderung; Industrie +1, Infrastruktur +1, Staats-Modifikator *Schaufenster des Westens* (Stabilität).
- Weitere Effekte:
  - MD-Treasury und Debt;
  - BDI- und DGB-Meinungen;
  - Imperia-Programme (Gastarbeiter-Anwerbestopp 1973 senkt Arbeitskraft und erhöht Stabilität);
  - `build_railway` für die Neubaustrecken Hannover–Würzburg und Mannheim–Stuttgart (ICE ab 1991).

**3. Energie** (ca. 18):

- Hub *Energieprogramm 1973*.
- Pfade: **Kernkraft** (Biblis, Brokdorf mit Protest, Wackersdorf), **Kohle-Vorrang** (Jahrhundertvertrag), **Erdgas-Röhren-Geschäft** (verbindet sich mit dem SOV-Gas-Deal und dem US-Embargo).
- Effekte: MD-Ölverbrauch und Ressourcen, Proteste, Imperia-Ölschock-Abfederung, Gebäude (Kraftwerke als Infrastruktur oder Zivilfabriken je nach MD-Gebäudesatz).

**4. Wehrhafte Demokratie** (ca. 28):

- Hub *Innere Sicherheit als Staatsaufgabe*.
- Jeder Fokus schaltet ein Werkzeug im Fenster *Lagezentrum* frei:

| Fokus | Freischaltung bzw. Wirkung |
|---|---|
| BKA-Ausbau unter Herold | Aufklärungsgenauigkeit |
| INPOL | Ortung +5/Monat |
| Rasterfahndung | Knopf *Rasterfahndung* |
| GSG 9 aufstellen | GSG-9-Stufe 1 |
| Mogadischu-Doktrin | GSG 9 im Ausland |
| Sicherungsgruppe | Schutzslot +1 |
| Kontaktsperregesetz | Knopf *Kontaktsperre* |
| Kronzeugenregelung | Knopf *Kronzeugen anwerben* |
| Aussteigerprogramm | Kinkel-Initiative |
| Verbot der Wehrsportgruppe | Rechtsterror-Knopf *Verbot* |

- Gabel: **Starker Staat** (Sicherheit +, Rechtsstaat −) oder **Liberaler Rechtsstaat** (Bürgerrechtsflügel der FDP, Milieu −).
- Effekte: MD-Terror-Modifikatoren über den Kern-Geist, FDP-Kurs, Proteste.

**5. Armee im Bündnis** (ca. 30):

- Hub *Weißbuch 1970*.
- Zweige:
  - **Heer:** Heeresstruktur III und IV, Leopard 2, Marder; Ausrüstungsboni im MD-Stil. Ich prüfe, ob MD MIOs nutzt; Russland und Israel nutzen sie nicht, also bleibt es bei Forschungs- und Produktionsboni bzw. Lizenzen.
  - **Luftwaffe:** Tornado (MRCA) mit UK und Italien; ergibt Meinung und MD-Einfluss.
  - **Marine:** Ostsee.
  - **Innere Führung:** Wehrbeauftragter, Zivildienst-Reform; Friedensbewegung −.
  - **Nachrüstung:** Pershing II und Doppelbeschluss. Gibt `cwgg_buendnis` +15 und Klima −10, löst die Raketenkrise im Minispiel aus, sowie Friedensbewegung und Hofgarten-Protest.
- Konfrontationszweig: *Vorneverteidigung stärken*, *Grenznahe Großmanöver* (Minispiel-Aktion freischalten), *Verteidigungsfall vorbereiten* (Alarmstufe 3 möglich).

**6. Westbindung** (ca. 30):

- Hub *Élysée-Geist erneuern*.
- Teilpfade:
  - **Europa** (Werner-Plan, EWS 1979, Einheitliche Akte, Maastricht, Euro): MD-EU-Effekte;
  - **Atlantik** (Offset-Abkommen, Doppelbeschluss);
  - **Frankreich** (Deutsch-französische Brigade 1989).
- Effekte: MD-Einfluss nach Israel-Muster in FRA, BEL, NED, ITA (z. B. `percent_change = 3`); Meinungen; `cwgg_buendnis` +; Imperia-Ausrichtung.

**7. Deutschlandpolitik** (ca. 40, das Herz des Minispiels):

- Hub *Deutschlandpolitik neu denken*: öffnet das Fenster bzw. führt es ein, gibt 2 Initiative.
- **Wandel durch Annäherung:** Tutzing-Rede als Leitmotiv; Bahr-Papier (Kanal Bahr–Kohl); Erfurt/Kassel (Sprosse 1 verfügbar); Moskauer Vertrag (Heißer Draht; Verbindung zum SOV-Baum); Warschauer Vertrag (Meinung und Einfluss POL); Prager Vertrag; Grundlagenvertrag vorbereiten; Freikauf institutionalisieren (Kanal Vogel, Hebel Menschen +1); Swing ausbauen (Hebel Devisen +1); Kirche im Sozialismus (Kirchenkanal); Verantwortungsgemeinschaft; Koalition der Vernunft (Schmidt–Honecker).
- **Rechtsposition** (CDU/CSU; nach Wahl oder Wende 1982 verfügbar; mit Annäherung kombinierbar):
  - Brief zur deutschen Einheit;
  - Karlsruher Urteil 1973 (Verfassungsklage Bayerns; die Rechtsposition bleibt gewahrt, die Verträge bleiben);
  - Milliardenkredit (Kanal KoKo, Hebel Devisen +2, nach Vorbild Strauß 1983);
  - Salzgitter stärken (Hebel Recht +1);
  - Medienoffensive (Hebel Medien +1);
  - Menschenrechte in der KSZE.
- **Konfrontation** (exklusiv zu Annäherung; nur Spieler, KI-Faktor 0; zeigt im Tooltip deutliche Warnungen): Alleinvertretung erneuern (Hallstein zurück); Wirtschaftskrieg (Kreditstopp, Lieferstopp, Imperia-Sanktionen); Fluchthilfe als Staatsräson; Befreiungsdoktrin (`will_lead_to_war_with = DDR`, öffnet Kriegspfad A, `create_wargoal` erst im Countdown-Ereignis).
- **Einheit** (spät; `available` an die Wende-Stufe gebunden; die vorhandenen Einheitswege werden zu Fokussen mit gegenseitigem Ausschluss): Zehn-Punkte-Plan; Währungsunion (MD-Treasury, Last des Ostens); Zwei-plus-Vier (verbindet sich mit dem bestehenden SOV-Ereignis); Treuhand; Hauptstadtbeschluss (Bonn/Berlin, Staats-Modifikatoren in Berlin 45 und 1251, Gebäude); Aufbau Ost (Gebäude in den neuen Ländern).

**8. Weltrolle** (ca. 22):

- Hub *Zivilmacht*.
- Inhalte: BMZ und Entwicklungspartnerschaften (Imperia-Programme, MD-Einfluss in Partnerländern); Weltwirtschaftsgipfel (Rambouillet 1975); Nahost (Wiedergutmachung, Meinung ISR, arabische Staaten); Rüstungsexport-Richtlinien (MIC, Korruption); KSZE-Schlussakte (verbindet sich mit dem Helsinki-Flag des SOV-Baums); Parteistiftungen (Imperia-PPS in Portugal, Spanien, Griechenland, Chile, Nicaragua).
- Effekte: `change_influence_percentage` mit festen Zielen, Meinungen, Imperia-Programme.

### C.4 Beispiel-Fokus im neuen Stil

So sieht ein Fokus im neuen Stil aus (gekürzt; erzeugt vom Generator):

```
focus = {
	id = COLDWAR_GER_1970_freikauf
	icon = GFX_goal_COLDWAR_GER_1970_freikauf
	relative_position_id = COLDWAR_GER_1970_annaeherung_hub
	x = 2 y = 2
	cost = 3
	prerequisite = { focus = COLDWAR_GER_1970_bahr_papier }
	search_filters = { FOCUS_FILTER_GER_DEUTSCHLAND FOCUS_FILTER_POLITICAL }
	completion_reward = {
		custom_effect_tooltip = { localization_key = modifies_dynamic_modifier_tt MODIFIER = COLDWAR_GER_1970_dm_ostpolitik }
		add_to_variable = { VAR = cwger_dm_ostpolitik_basis TOOLTIP = cwger_dm_ostpolitik_basis_tt VALUE = 3 }
		add_to_variable = { VAR = cwger_dm_ostpolitik_init TOOLTIP = cwger_dm_ostpolitik_init_tt VALUE = 0.25 }
		newline = yes
		custom_effect_tooltip = COLDWAR_GER_1970_unlock_kanal_vogel_tt     # „Schaltet frei: Anwaltskanal Vogel–Stange“
		set_variable = { cwgg_kanal_vogel = 1 }
		add_to_variable = { cwgg_hebel_menschen = 1 }
		newline = yes
		set_temp_variable = { treasury_change = -0.4 }   # skaliert wie bisher an gdp_total
		modify_treasury_effect = yes
		DDR = { add_opinion_modifier = { target = GER modifier = COLDWAR_GER_1970_freikauf_om } }
		change_DGB_opinion = …   # MD-Fraktion, Name wird gegen die Mod geprüft
	}
	ai_will_do = { base = 5 modifier = { factor = 0 has_country_flag = cwger_ai_path_konfrontation } }
}
```

### C.5 Was aus dem alten Baum übernommen wird

- **Inhalte, die gut waren:** Ereignisse, Bundestag, FDP-Kurs, Einheitswege, Imperia-Hooks und die SOV-Verbindungen bleiben erhalten. Sie werden aus den neuen Fokussen aufgerufen.
- **Rund 60 % der Fokus-Ideen** bleiben thematisch, werden aber gekürzt, neu verteilt und mit Effekten im neuen Stil versehen.
- **Die Säule „Ostpolitik“** geht in *Deutschlandpolitik* auf; die bisherigen Entscheidungen der Kategorie DR entfallen zugunsten des Fensters.
- **Fokus-Icons:** Die vorhandenen werden wiederverwendet. Neue entstehen über `icons.py` im gleichen Stil, oder es werden vorhandene MD-Goal-Sprites per Name referenziert, wie es Russland und Israel tun (z. B. `attack_america2`).

---

## D. Umsetzung

### D.1 Module (Generator)

| Neu oder geändert | Inhalt |
|---|---|
| `rivalry.py` (neu) | Variablen, Monats- und Runden-Tick, Krisenerzeugung, Matrix, DDR-KI, Verträge, Kanäle, Hebel, Kriegspfade, Lagebericht-Codes |
| `events_rivalry.py` (neu) | ca. 70 Ereignisse: 10 Krisentypen × (Ausbruch, Höhepunkt, 2–3 Ausgänge), 9 Vertragsabschlüsse, Countdown, Verteidigungsfall, Atomschwelle, Kriegsfrieden, DDR-Spiegelereignisse |
| `security.py` (neu, ersetzt den Terrorteil in `systems.py`) | Fahndungskarten, Zielplanung, Schutzslots, Haftregime, Hungerstreik, Waage, Rechts- und Auslandsterror |
| `events_security.py` (neu) | ca. 35 Ereignisse; die bestehenden Terror-Ereignisse werden umgehängt, nicht dupliziert |
| `gui.py` (neu) | erzeugt `interface/COLDWAR_GER_1970_rivalry.gui`, `…_security.gui`, `.gfx`, `common/scripted_guis/COLDWAR_GER_1970_*.txt`, `scripted_localisation`, Topbar-Knöpfe |
| `gui_sprites.py` (neu) | erzeugt die zusätzlichen Grafiken (Leiter-Pips, Krisenkarten, Fahndungskarten, Kanal-Karten, Porträt-Sheet) als DDS; vorhandene `mdcw_cw_*`-Sprites werden mitbenutzt |
| `focus_tree3.py` (neu, ersetzt `focus_tree.py` und `focus_tree2.py`) | neuer Baum nach C; ein Hilfs-DSL für Effektbausteine (`dm()`, `unlock_gui()`, `influence()`, `state_build()`, `rail()`, `faction()`) |
| `dynamic_modifiers.py` (neu) | die acht Kern-Geister plus *Innerdeutsches Verhältnis*, inklusive GFX-Registrierung wie bei MD |
| `decisions.py` | DR-Kategorie und Terror-Entscheidungen werden auf GUI-Pendants umgestellt; die Kategorie DR behält nur noch den Knopf „Lagekarte öffnen“ und Entscheidungen ohne GUI-Entsprechung |
| `validate.py` | zusätzlich: GUI-Elementnamen gegen `scripted_gui`, Sprites gegen `.gfx`, `scripted_localisation`-Schlüssel, `relative_position_id`-Ziele, Kostenverteilung, „Fokus ohne Systemeffekt“-Warnung |
| `preview.py` | rendert zusätzlich Mock-ups der beiden Fenster als PNG, damit Layoutfehler vor dem Spieltest auffallen |

### D.2 Reihenfolge

1. **Kern der Rivalität**: `rivalry.py` und Ereignisse, ohne GUI, über Debug-Entscheidungen testbar. So ist die Spielmechanik zuerst im Spiel prüfbar.
2. **Fenster „Deutsch-deutsches Verhältnis“**: GUI, Sprites, Lokalisierung, Topbar; die DR-Entscheidungen werden umgestellt.
3. **Lagezentrum Innere Sicherheit**: `security.py`, Fenster, Umbau der RAF-Ereignisse.
4. **Neuer Fokusbaum** mit Kern-Geistern; der alte Baum wird ersetzt.
5. **Integration, Validierung, Balancing** mit einer 30-Jahres-Simulation: Ein Python-Modell des Monats-Ticks spielt 1.000 KI-Partien durch und zählt Krisen pro Jahrzehnt, Kriegsquote, Einheitsjahr und Verteilung der Wege.

   Zielwerte:
   - historischer KI-Lauf: 4–8 Krisen bis 1989, Krieg unter 1 %;
   - Einheit 1989–1992 in rund 50 % der Läufe, keine Einheit vor 1985 ohne Spieler.
6. Optional: **DDR spielbar** mit gespiegeltem Fenster.

### D.3 Prüfliste für den Spieltest

- Fenster öffnen und schließen, Tabs wechseln, Knöpfe nur sichtbar bzw. aktiv, wenn erlaubt (Tooltip mit Grund).
- Eine Krise per Debug-Entscheidung starten: Runden laufen, Lagebericht aktualisiert sich, der Höhepunkt erscheint.
- Eine Vertragsverhandlung abschließen; Ratifikation über den Bundestag; Vertrag aussetzen.
- Kriegspfad A per Debug: Countdown, Ausstieg, Kriegserklärung, NATO-Beitritt je nach Rückhalt.
- RAF: Fahndungskarte orten, Zugriff, Schutzslot verteilen, Anschlag vereitelt bzw. erfolgreich, Geiselnahme mit Krisenstab.
- Fokusbaum: keine Überlappungen (Layoutprüfung), alle Tooltips lesbar, keine rohen Variablennamen.
- Fehlerlog sauber; keine Abstürze in einem einjährigen Beobachterlauf bei 5er-Geschwindigkeit.

### D.4 Entscheidungen, die ich ohne weitere Rückmeldung so treffe

- **Zwei getrennte Fenster** (Rivalität und Sicherheit) mit zwei kleinen Topbar-Knöpfen, statt eines Fensters mit acht Tabs.
- **Nur eine aktive Krise mit Runden**; weitere laufen als Nebenkrise ohne Runden.
- **Ein Krieg nur über die vier Pfade in A.8**, nie direkt aus einem Zufallsereignis. Die Bonner KI greift nie an.
- **RAF-Figuren der 3. Generation** nur mit Decknamen; historische Opfer nur bei passendem Datum.
- **Der alte Baum wird ersetzt**, nicht erweitert; Inhalte werden übernommen, wo sie passen.
- Wie bisher: **nichts aus dem Downloads-Ordner**; Quellen sind nur die hochgeladenen bzw. freigegebenen Mod-Ordner.

---

## E. Umsetzungsstand (18.10.2026)

Alle drei Pakete sind gebaut und liegen im Mod-Ordner. Die Validierung meldet 0 Fehler und 0 Warnungen; im Spiel getestet ist es noch nicht.

### Paket A: Fenster *Inner-German Relations*

- **Topbar-Knopf** bei x = 1700 und Entscheidung „Fenster öffnen“.
- **Vier Tabs** wie geplant, Kriegspfade A–D.
- **Abweichungen vom Plan nach dem Balancing:**
  - Start-Klima −5.
  - Ulbricht −5; Honecker −5 in 1980–82 und +5 ab 1983.
  - Druck wirkt mit 3 % statt 10 % auf das Klima.
  - Erschöpfte Krisen unter Intensität 50 werden nach Ansehen entschieden statt eingefroren.
  - Die Vertragsschwellen liegen etwas niedriger.
- **Simulation:**
  - Historische KI: etwa 3 Krisen bis 1990, kein Krieg; Verträge 1–6 zwischen 1971 und 1976.
  - Spieler auf hartem Konfrontationskurs: etwa 5 Höhepunkte und rund 20 % Kriegsrisiko in 20 Jahren.

### Paket B: Fenster *Internal Security*

- Topbar-Knopf bei x = 1760.
- Fahndungsliste, Anschlagsplanung mit Personenschutz, Haftregime und Hungerstreik, Krisenstab mit eigener Uhr, Politik.
- RAF-Anschläge kommen jetzt aus dem Planungsmodell.
- Die entsprechenden Entscheidungen und die Ultimatum-Mission sind entfernt.

### Paket C: Fokusbaum

- **Umfang:** 235 Fokusse.
- **Aufbau:**
  - Wurzel und acht Hubs; alle Fokusse mit `relative_position_id`; Kosten 1–7.
  - Acht Kern-Geister; der Deutschlandpolitik-Geist hat drei Gesichter.
- **Effekte:**
  - Gebäude in benannten Staaten und zehn Staats-Modifikatoren.
  - Vier Bahnstrecken.
  - MD-Einfluss und Fraktionen.
  - Freischaltungen für beide Fenster.
- **Pfade:**
  - Konfrontationszweig mit *Liberation Doctrine* (`will_lead_to_war_with = DDR`).
  - *Strong State* und *Liberal Rule of Law* schließen sich gegenseitig aus.

### Offen bzw. im Spiel zu prüfen

- Ob die Topbar-Positionen mit anderen Elementen kollidieren.
- Ob `build_railway` mit `start_province`/`target_province` funktioniert.
- Wie die Krisen-Bilder (`image`-Property) dargestellt werden.
- Ob die Fenster scrollen bzw. passen, wenn die Auflösung kleiner als 1920 ist.

---

## F. Multiplayer-Umbau und Akten-Stil (18.10.2026)

Anlass: Die Mod wird als Multiplayer-Rollenspiel gespielt. Versteckte Punktestände, die Ausgänge vorentscheiden, passen dazu nicht. Krisen sollen seltener und langsamer laufen, die Oberfläche soll nach BRD/DDR aussehen.

### Entfernt

- **Ansehen** (`cwgg_face_*`, `cwgg_krise_fb/fd`) und **Rückhalt der Westmächte** (`cwgg_buendnis`) samt Fensterabschnitt, Tooltips und allen Fokus-Effekten.
- *Alliierte einschalten*, *Null-Lösung* und die Vermittlung am Höhepunkt hängen jetzt an `has_idea = NATO_member` (bzw. am Heißen Draht).
- Kein automatischer NATO-Beitritt zu einem Krieg. Die UdSSR tritt nur automatisch bei, wenn sie KI ist; eine KI-DDR ohne Moskauer Garantie verlässt die Fraktion, eine menschliche DDR entscheidet selbst.

### Krisen im Halbjahrestakt

- Eine Runde alle **sechs Monate**, gezählt im Monats-Tick (`cwgg_krise_monat`). Die wiederkehrenden versteckten Ereignisse `GGR.2`, `.13` und `.16` sind weg.
- Krisen dauern 2–4 Runden; die Intensitätswerte der Matrix sind um den Faktor 1,5 erhöht.
- **Ausgang ohne Ansehen:** Wer in der letzten Runde nachgegeben hat, verliert; sonst endet die Krise im **Kompromiss** (neuer Ausgang 7, Klima +5). Über Intensität 50 erstarrt sie.
- **Countdown** am Höhepunkt: drei Monatsschritte, beide Seiten können jederzeit einlenken.
- **Fehlalarm** (Kriegspfad D) nur, wenn mindestens eine Seite KI ist.
- Sperrfrist nach einer Krise: 12 Monate.

### Menschliche DDR

| Ereignis bzw. Entscheidung | Wirkung |
|---|---|
| `GGR.200` *Our Course in the Crisis* | die verdeckte Antwort der DDR für die nächste Runde (`cwgg_ddr_wahl`) |
| `GGR.201` | Ausgang der Krise aus Ost-Berliner Sicht |
| `GGR.210` | Countdown: durchhalten oder einlenken |
| `GGR.211` | Countdown abgelaufen: Moskaus Zurückhaltung annehmen oder Angriff auf West-Berlin (Garantie ≥ 60, NVA-Alarm ≥ 2) |
| `GGR.230` | Kriegsbeginn aus Sicht der DDR |
| Kategorie *Policy Towards Bonn* | Kurs ändern, NVA-Alarmstufe, Zwangsumtausch, Transitschikane, Grenzanlagen, HVA-Offensive, Anerkennung, Geste des guten Willens, Kreditbitte, Zugangswege sperren |

Die DDR-KI handelt nur noch, wenn die DDR KI ist.

### Alarmstufen

Bundeswehr und NVA geben stufenweise Mobilisierungsgeschwindigkeit und Kriegsunterstützung (über `mobilization_speed` im dynamischen Modifikator):

| Stufe | Mobilisierung | Kriegsunterstützung |
|---|---|---|
| 1 | +10 % | +2 % |
| 2 | +25 % | +5 % |
| 3 | +50 % | +10 % |

Der frühere Fabrikmalus der Alarmstufen entfällt.

### Weitere Änderungen

- **Geiselnahme:** ein einziges terminiertes Ereignis zur Frist statt Abfrage alle drei Tage. Kontaktsperre und Hinhalten verschieben die Frist; die Anzeige rechnet über `global.num_days`.
- **Texte:** „world tension … a month“ heißt jetzt „Cold War world tension … a month“ (Imperia-Spannung), ebenso im Tension-Tooltip.
- **Lagebericht** mit fünf statt drei Zeilen.

### Akten-Stil

Neue Grafiken aus `akte_sprites.py`:

- **Kanzleramts-Akte** (khakifarbener Aktendeckel) mit Bundesadler links und DDR-Emblem rechts, Aktenschild, Abheftlöchern, Registerreitern, Stempel-Knöpfen, Dienstsiegel und Kennzeichnung „VS – NUR FÜR DEN DIENSTGEBRAUCH“.
- **BKA-Akte** (graugrün) mit Polizeistern, „GEHEIM“-Kennzeichnung und Stempel.
- Die blauen `mdcw_cw_*`-Teile und der US-Stern werden nicht mehr benutzt.

### Simulation (neu)

- Historische KI: etwa 2,3 Krisen bis 1990, meist mit Kompromiss; Krieg 0,05 %.
- Harter Konfrontationskurs: etwa 2,5 Höhepunkte und rund 10 % Kriegsrisiko.

### Nachtrag: Krieg nur auf menschlichen Befehl (18.10.2026)

Am Ende eines Countdowns kann nur noch ein Mensch den Angriff Ost-Berlins befehlen: eine menschliche DDR (`GGR.211`) oder, bei KI-DDR, eine menschliche Sowjetunion (neues Ereignis `GGR.212`; die UdSSR tritt dann selbst in den Krieg ein). Sind DDR und Sowjetunion KI, bremst Moskau immer (Ausgang 6). Anlass war ein Spiel, in dem eine KI-DDR 1972 den Dritten Weltkrieg ausgelöst hat.

### Nachtrag: Wahlergebnis, Grenzaufmarsch, US-Truppen (18.10.2026)

- **Bundestag:** Sitze, Mehrheiten, Koalitionsrechnung und alle Mehrheitsabstimmungen (Ratifikation, Nachrüstung, Misstrauensvotum) nutzen das Ergebnis der letzten Bundestagswahl (`party_pop_elect_array` aus MDs `hold_elections`) statt der aktuellen Umfragen. Der Fokus *Greens in the Bundestag* braucht die Grünen über 5 % bei der letzten Wahl.
- **Truppen an der Grenze:** monatliche Zählung mit dem Vanilla-Trigger `divisions_in_state` in den Grenzstaaten beider Seiten. Drei Stufen (Konzentration, Aufmarsch, massiver Aufmarsch) erhöhen Druck und Cold-War-Spannung, senken das Klima und halten die Leiter auf *Krise* bzw. *Konfrontation*. Die Gegenseite bekommt ein Ereignis (`GGR.240`/`.241`). Grenzmanöver, Erstschlag, Bruderhilfe und der Angriff Ost-Berlins brauchen Truppen an der Grenze.
- **US-Streitkräfte** als RAF-Ziel nur, solange US-Divisionen in einem westdeutschen Staat stehen.

---

## G. Außenpolitik, schwerere RAF, autoritärer Pfad (18.10.2026)

Leitlinie: Multiplayer-Rollenspiel. Wo andere Länder betroffen sind, entscheiden deren Regierungen selbst; die KI beginnt keinen Krieg.

### Außenpolitik (+41 Fokusse, `foreign.py`)

- **Angebotsmechanik (`COLDWAR_GDIP`):** Viele Fokusse schicken dem Partnerland ein Angebot. Ein menschlicher Spieler entscheidet selbst (annehmen oder ablehnen, beides mit Folgen); eine KI entscheidet nach ihrer Meinung über Bonn. Bonn bekommt den Ertrag nur bei Zustimmung, bei Ablehnung 15 PP Trost. Der Fokus-Tooltip zeigt, was Bonn bei Zustimmung bekommt.
- **Westbindung:** Atlantische Erklärung 1974 (USA), Neutronenbomben-Streit oder Loyalität zu Washington, Host Nation Support (USA), SDI-Forschung oder „Gorbatschow beim Wort nehmen“, Pershing-Ia-Frage; Regionalfonds, Direktwahl des Europaparlaments, Genscher-Colombo-Plan (ITA), Süderweiterung, Fontainebleau, Weimarer Dreieck (POL, FRA), Osterweiterung, Jugendwerk.
- **Ostpolitik jenseits der DDR:** Beziehungen zu Ungarn und Bulgarien, Freikauf der Rumäniendeutschen (ROM), Kredite gegen Ausreise (POL), Partnerschaft mit Belgrad (SER), Solidarność-Pakete oder stille Diplomatie, Sowjetdeutsche (SOV), Bonner Erklärung 1989 (SOV), Ungarns Grenzöffnung (HUN).
- **Weltrolle:** Beziehungen zu Peking (CHI), Japan, Cap Anamur, Indien (RAJ); Euro-Arabischer Dialog, Venedig-Erklärung oder Israel zuerst, Leopard-Geschäft mit Riad (SAU); Lomé, Namibia-Kontaktgruppe, Apartheid-Sanktionen oder Handel mit Pretoria; Exil für Chilenen, Demokratie in Lateinamerika; NV-Vertrag ratifizieren (schließt die nationale Atomoption), UNO, KSZE-Folgekonferenzen, Rambouillet (FRA).
- **Behoben:** `NED` (gibt es in MD nicht) → `HOL`; `IND` (Indonesien) → `RAJ` (Indien).

### RAF schwerer

- Spurgewinn: Grundwert 0,5 statt 1, BKA ×1 statt ×1,5, Milieu wirkt stärker (/15 statt /25), 2. Generation −1, 3. Generation −2,5, Terrorabwehr-Bonus gedeckelt.
- Neu: Eine geortete Zelle wechselt mit 20 % (ab 2. Generation 30 %) pro Monat die Wohnung (Spur −15).
- Zugriff: 35 PP, alle 45 Tage, Grundchance 30 statt 40; Fehlschlag 45 (Spur −35); neu **Schusswechsel** (15, mit GSG 9 Stufe 2 halbiert): Verdächtiger tot oder entkommen, ein toter Beamter, Milieu +, Rechtsstaat −.
- Automatische Festnahmen seltener (6 % statt 10 % Grundwert, kleinere Zuschläge, Doppelfestnahme erst ab BKA 3 und nur zu 50 %).
- Anschlagsplanung schneller (÷3,3 statt ÷4), Personenschutz bremst weniger (×0,6), vereitelt 55 % statt 65 %; nach einer Vereitelung weicht das Kommando auf ungeschützte Ziele aus (+15 Planung).
- Rekrutierung +50 %; Ende der RAF erst bei Milieu < 10 und Kader < 6.
- Simulation (`simulate_manhunt.py`, Median bis 4 Festnahmen der 1. Generation): BKA 1: 11 → 21 Monate; BKA 2: 9 → 16; BKA 3: 7 → 11.

### Autoritärer Pfad (`dark_path.py`, `COLDWAR_GDARK`)

- Nur menschliches GER (`is_ai = no`, KI-Gewicht 0). Fiktives Regime („National Directorate“), keine historische Person an der Spitze.
- Vorstufe: *Courting the National Right* (Rechte zusammen > 6 % in Umfragen oder Rechtsterror > 30) → *Order Above Everything* (Nachricht an alle menschlichen Spieler) → *The Street and the Ballot Box* (Gegendemonstration).
- Tor *The Crisis of the Republic*: Erosion der Republik ≥ 60, Rechte zusammen ≥ 15 % bei der **letzten Bundestagswahl**, Stabilität < 30 %, Rechtsstaat < 35, Sicherheitsstaat > 65.
- Drei Hürden, an denen der Pfad endgültig scheitern kann: Karlsruhe (gehorchen = Ende), konstruktives Misstrauensvotum (40 %, mehr ohne Mehrheit), Generäle (50 %, mehr mit Innerer Führung und NATO).
- *The National Directorate*: NPD-Regierung ohne Wahlen, eigener Geist, Spannung +15.
- **Reaktionen:** NATO-Mitglieder: Bonn suspendieren (`NATO_leave`), Sanktionen, Vorbehaltsrechte der drei Westmächte (Kriegsziel, nur menschliche Regierungen), abwarten. UdSSR: Feindstaatenklauseln (Kriegsziel, nur menschlich), Alarm der GSSD (neuer Geist) und Garantien für DDR und Polen, Sanktionen. DDR und Polen eigene Ereignisse. KI reagiert hart, aber ohne Krieg.
- Danach: Säuberung, nationale Aufrüstung, Ostverträge kündigen, *The Old Borders* (Kriegsziel DDR); Widerstand als eigener Wert mit Ereignissen; Ausweg *Restore the Basic Law* (bei Stabilität < 20 %, Widerstand ≥ 60 oder Krieg), NATO-Staaten entscheiden über Aufhebung ihrer Maßnahmen.

Stand: 288 Fokusse, 224 Ereignisse, Validierung 0 Fehler. Im Spiel nicht getestet.

---

## H. Innenpolitik (18.10.2026, `domestic.py`, `COLDWAR_GDOM`)

+22 Fokusse, +13 Ereignisse, 2 Entscheidungen; jetzt 310 Fokusse, 237 Ereignisse. Validierung 0 Fehler, im Spiel nicht getestet.

- **Verfassungsänderungen** brauchen zwei Drittel der Sitze aus der letzten Bundestagswahl (`cwger_two_thirds`, monatlich aus `cwger_seats_total`). Ohne sie entscheidet der Spieler: der Opposition ihren Preis zahlen (75 PP, größte Oppositionspartei +1 %) oder scheitern lassen. Kein verdeckter Würfelwurf.
- **Reform der Republik** (Enquete-Kommission): Volksentscheide ins Grundgesetz (schaltet die Entscheidung *Put the Question to the People* frei) → Direktwahl des Bundespräsidenten; Neugliederung der Länder (Nordstaat, Saarland zu Rheinland-Pfalz oder nichts; neue Staats-Modifikatoren); Notstandsgesetze an Karlsruhe binden; Mehrheitswahlrecht (Hürde 15 %) oder Drei-Prozent-Hürde (3 %), gegenseitig ausschließend.
- **Verzahnung mit dem autoritären Pfad:** gebundene Notstandsgesetze (+20) und ein direkt gewählter Präsident (+15) erhöhen die Chance, dass der Bundestag eine Notstandsregierung stoppt.
- **Gesellschaft im Wandel:** §218 (Fristenlösung → Karlsruhe 1975, Urteil annehmen oder Grundgesetz ändern; Indikationslösung; altes Recht), Gleichbehandlung, Gesamtschule oder dreigliedrige Schule, Hochschulrahmengesetz, Volkszählung 1983 (Datenschutz oder durchsetzen), Privatfernsehen oder öffentlich-rechtliches Monopol, Staatsbürgerschaft (Geburtsort mit oder ohne Doppelpass oder zurückziehen).
- **Flick-Affäre** (ab Oktober 1981, Skandaldruck > 15): Amnestiegesetz oder Ermittlungen; danach Parteienfinanzierungsgesetz.
- **Arbeit:** ABM, Vorruhestand oder Rentenreform 1992.
- Entscheidung *Federal Reform Commission* (ab 1985).
- Fokus-Tooltips zeigen die Szenario-Prüfung (GER, 1970er Szenario) nicht mehr (`hidden_trigger`).

---

## I. Friedliche Einheit durch Entspannung (18.10.2026, `unity.py`, `COLDWAR_GGU`)

Neuer fünfter Tab **Unity** im Fenster *Inner-German Relations*. Nicht der Zusammenbruch der DDR (dieser Weg bleibt), sondern zwei Staaten, die sich gut genug verstehen, um einen Staat auszuhandeln. Jetzt 316 Fokusse, 259 Ereignisse; Validierung 0 Fehler, im Spiel nicht getestet.

- **Vorbedingungen (schwer):** Fokus *A European Peace Order* (Klima ≥ 60, höchstens *Cool Coexistence*, Verkehrsabkommen in Kraft); Grundlagenvertrag, Ständige Vertretungen, Verkehrsabkommen und Kultur oder Staatsbesuch in Kraft; Klima ≥ 70; *Modus Vivendi* ohne Krise; **36 Monate ununterbrochene Entspannung** (`cwgg_detente_m`, fällt bei Spannungen auf 0); 3 Initiative und 100 PP. Nach gescheiterten Gesprächen drei Jahre Pause.
- **Vorschlag:** Bonn (Knopf im Tab) oder Ost-Berlin (Entscheidung *Propose Unity Talks*). Die andere Regierung entscheidet: ein Mensch selbst, eine KI nach Führung, Abhängigkeit von Bonn, Devisenmangel und Moskaus Rückhalt (eine Hardliner-Führung lehnt fast immer ab).
- **Fünf Kapitel**, eins pro Runde (3 Monate): Verfassung (Grundgesetz Art. 23 / neue Verfassung Art. 146 / sozialistische Verfassung), Wirtschaft (soziale Marktwirtschaft / gemischte Wirtschaft / Planwirtschaft), Bündnis (NATO / bewaffnete Neutralität / Warschauer Pakt), Hauptstadt (Bonn föderal / Berlin föderal / Berlin zentralistisch), Grenzen (Friedensvertragsvorbehalt / Oder-Neiße endgültig / Grenze und Friedensvertrag). Beide Seiten wählen eine Position; gleiche Position = vereinbart. Ein Mensch auf DDR-Seite wählt per Ereignis, verdeckt. Eine KI-DDR rückt nach jeder gescheiterten Runde ein Stück auf Bonns Position zu. 8 gescheiterte Runden, eine Konfrontation oder ein Abbruch durch eine Seite beenden die Gespräche; eine Krise pausiert sie.
- **Vier Mächte:** USA, UdSSR, Großbritannien und Frankreich stimmen zu oder legen ein Veto mit Forderung ein (öffnet das betroffene Kapitel wieder). Drei Vetos oder ein grundsätzliches Veto beenden die Gespräche. KI-Gewichte: Die UdSSR akzeptiert NATO-Mitgliedschaft vor 1987 kaum, die USA kaum Neutralität; ab 1987 und mit dem Abzugsfonds wird ein Deutschland in der NATO möglich.
- **Ratifikation:** Bundestag (neue Verfassung braucht zwei Drittel, sonst Preis der Opposition oder Volksabstimmung über den Fokus *Let Both Peoples Decide*) und Volkskammer.
- **Ergebnis:** Beitritt nach Art. 23 oder neue Verfassung nach Art. 146 (bestehende Effekte), dazu Neutralität oder Warschauer Pakt, gemischte oder Planwirtschaft, Hauptstadt Berlin, Grenzfolgen. Eine sozialistische Verfassung lässt die DDR die Bundesrepublik übernehmen – nur möglich, wenn auch die Westmächte zustimmen.
- **Bindung der vorhandenen Einheits-Fokusse an das Minispiel:** Zehn-Punkte-Plan, Runder Tisch, Vertragsgemeinschaft, neue Verfassung, Neutralitätsangebot, Grenzvertrag, Währungsunion und Zwei-plus-Vier brauchen jetzt höchstens *Cool Coexistence* und Klima über 40; sie öffnen sich mit dem Mauerfall **oder** während der Einheitsgespräche und verschieben dann Ost-Berlins Haltung bzw. die Zustimmung der Mächte.
- **Neue Fokusse:** *A European Peace Order*, *A Social Union*, *Berlin, Capital of Germany*, *A Fund for the Soviet Withdrawal*, *A Conference of the Four Powers*, *Let Both Peoples Decide*.
- **DDR-Entscheidungen:** Gespräche vorschlagen, Position neu festlegen, Moskaus Segen suchen, Gespräche abbrechen. Bonn: Entscheidung *The Unity Talks* öffnet den Tab.
- Fenster hat jetzt fünf schmalere Reiter; „Levers & Channels“ heißt „Levers“.

---

## J. Ausbau der kurzen Zweige (18.10.2026, `branches.py`, `COLDWAR_GBR`)

+47 Fokusse, +27 Ereignisse; jetzt 363 Fokusse, 286 Ereignisse. Validierung 0 Fehler, im Spiel nicht getestet. Koalitionen richten sich nach dem letzten Wahlergebnis (`cwger_rg_share`, `cwger_cf_share`, `cwger_sl_share` im monatlichen Tick).

- **Lafontaine:** Mannheimer Parteitag (eigener Einstieg, macht ihn zum SPD-Chef) → ökologischer Umbau, Arbeit teilen → Rot-grüner Pakt (rot-grüne Regierung nur mit Mehrheit) → Reichensteuer oder Frieden mit der Bundesbank → Europäischer Beschäftigungspakt (Angebot an Frankreich).
- **Große Koalition:** Macht der zwei Drittel → Finanzreform, Konzertierte Aktion → Opposition außerhalb des Parlaments (Ereignis) → Fortsetzung oder Ende (kleine Koalition nur mit Mehrheit, sonst Neuwahl).
- **CSU als vierte Partei:** CSU in jedem Land oder CDU in Bayern → Krieg der Schwestern (Kreuth: Nichtangriffspakt, getrennte Wege, Rückkehr nach Bayern) → rechts von der CSU keine Partei.
- **Kanzler Barzel:** Verträge mit Vorbehalt, Vermögensbildung → Kampf um die Mehrheit (Neuwahl, christlich-liberale Koalition, weiterregieren) → Barzels Europa.
- **Grüne:** Turnschuh-Minister (Hanau), Rotationsprinzip → Schwerter zu Pflugscharen; Bündnis 90/Die Grünen (nach der Einheit) → Bielefeld 1999.
- **Späth:** Silicon Valley am Neckar, Partner im Osten → Jenoptik → Bremer Putsch (Späth stürzt Kohl oder scheitert).
- **Spendenaffären:** Untersuchungsausschuss → schwarze Kassen (Ehrenwort-Ereignis); Transparenzgesetz.
- **Nukleare Teilhabe:** Sitz in der Nuklearen Planungsgruppe → zwei Schlüssel; chemiewaffenfreie Zone (Angebot an die DDR, schließt die nationale Option aus); nach der nationalen Option: Gronau → deutsche Bombe (nur Mensch, nicht nach NV-Vertrag; USA, UdSSR, Großbritannien und Frankreich reagieren, Kriegsziel nur für menschliche Regierungen).
- **Vorneverteidigung:** Sperrpläne Fulda Gap, REFORGER (Angebot an die USA); WINTEX → Zivilschutz oder defensive Verteidigung.
- **Strauß:** Wackersdorf (bauen oder nach Frankreich), Flug nach Moskau (Angebot an die UdSSR).
- **Schmidts Minderheitsregierung:** Regieren ohne Mehrheit (Vertrauensfrage, Tolerierung durch die Grünen, weiterregieren) → Abschied des Staatsmanns.
- **Aufgeräumt:** Kreuzende Voraussetzungen im Bundeswehr-Zweig (Exportrichtlinien, AWACS, Zivildienst, Out-of-Area-Urteil) vereinfacht.
