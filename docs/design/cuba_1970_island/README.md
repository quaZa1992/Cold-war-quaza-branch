<!-- IMPERIA CW — Cold War: Cayo Blanco del Sur map feasibility. -->
# Cayo Blanco del Sur: Prüfung eines eigenen HOI4-State

Stand: 23. Oktober 2026. **Die Insel wurde nach dieser Prüfung eingebaut:**
State **1252**, Provinz **16537**, RGB **214 / 173 / 62**, kubanischer Besitz.
Die ursprüngliche Untersuchung folgt unten; `installed_map_comparison.png`
zeigt die tatsächlich eingebaute Karte. `map_location.png` und `map_audit.json`
dokumentieren dagegen den ursprünglichen Zustand vor dem Einbau.

Die Originaldateien liegen mit verifizierten Prüfsummen in
`rollback_backups/cayo_blanco_del_sur_20261023_before_install/`.
Die reproduzierbaren Werkzeuge und die geschützte Wiederherstellung stehen in
`tools/cayo_blanco_del_sur/`.

Die statische Validierung besteht. Auch der echte HOI4-Test im isolierten Profil
hat den Szenariostart, kubanischen Besitz/Core, Produktivität, positives
kubanisches BIP, die separate Übertragung zur DDR, die Umbenennung und die
Rückübertragung bestätigt. Siehe `validation.json` und `engine_report.json`.
Die Computersteuerung wurde anschließend vom Benutzer mit Escape gestoppt;
**Sichtprüfung/Auswählbarkeit und Speichern/Neuladen sind nicht bestätigt**.

Die protokollierte Meldung am Ende von `map/buildings.txt` (Leerzeile nach dem
letzten Datensatz) und die Railway-Assertions existieren auch im früheren
Uranium-Engine-Protokoll vor diesem Einbau. Die neuen Runtime-Dateien erzeugen
keine zugeordneten Fehler. Eine numerische Variablenreferenz in der temporären
Diagnose-Logzeile erzeugte eine Lexer-Meldung; die Ausgabe wurde auf State-Scope
umgestellt, nach dem Abbruch aber nicht erneut im Spiel getestet. Alle fünf
fachlichen Prüfpunkte bestanden bereits im tatsächlichen Lauf. Der normale
Spielbetrieb enthält keine Diagnoseevents und keinen automatischen DDR-Transfer.

## Ergebnis

Ein eigener **HOI4-State unter kubanischem Besitz** ist technisch plausibel und
würde eine spätere, separate Übertragung an die DDR ermöglichen. Ein eigener
Country-Tag ist dafür nicht erforderlich. Der Startname für 1970 lautet
**Cayo Blanco del Sur**.

Die Insel war im betreffenden Küstenabschnitt der ursprünglichen Karte nicht als
abgetrennte Landfläche oder eigene Provinz vorhanden. Deshalb ist dies mehr als
eine zusätzliche State-History: Die Insel muss zunächst kartografisch ergänzt
werden. Ein bloßer Name oder ein State ohne eigene Landprovinz genügt nicht.

## Berlin als bestehendes Beispiel

| Teil | State | Provinz | RGB in `provinces.bmp` und `definition.csv` | Pixel |
| --- | ---: | ---: | --- | ---: |
| East Berlin | 45 | 6521 | 86, 99, 46 | 39 |
| West Berlin | 1251 | 16536 | 167, 217, 90 | 46 |

Beide Teile haben eine eigene State-History und eine eigene Provinz. Beide
Provinzen sind der deutschen strategischen Region zugeordnet. Die Karte ist
5632 × 2048 Pixel groß; `provinces.bmp` ist eine 24-Bit-RGB-Bitmap.

Die Provinzfarbe ist ein exakter Datenbankschlüssel, keine politische Kartenfarbe.
Sie muss in Bitmap und CSV bytegenau übereinstimmen. Beim Zeichnen darf keine
Kantenglättung zusätzliche Farben erzeugen. Dateiformat, Bittiefe und die Paletten
der anderen Kartenebenen müssen erhalten bleiben.

Der ältere Commit `70b466c3` ("Made West Berlin") benutzte noch Provinz 16304,
State 1222 und RGB 167, 217, 89. Das ist **nicht** die heutige Zuordnung. Die
aktuelle Implementierung und `tools/berlin_landmarks/border.py` verwenden die
oben angegebenen Werte. Eine alte Berlin-Anleitung darf deshalb nicht ungeprüft
übernommen werden.

Die Berliner State-Kategorie mit 7 Bauslots pro Hälfte erhält die bisherigen
14 Slots. Für die kleine, unbewohnte Insel wäre diese Kategorie unpassend.

## Historischer und geografischer Befund

- GeoNames führt die Insel unter den Namen Ernst Thälmann Island, Cayo Blanco
  del Sur und Cayo Ernest Thaelmann bei ungefähr **22.033333° N, 81.400000° W**
  in Matanzas. Sie liegt am Golfo de Cazones südlich der Zapata-Halbinsel.
- Nicht mit **Cayo Largo del Sur**, der Isla de Pinos oder anderen Inseln namens
  Cayo Blanco verwechseln. Cayo Largo liegt laut derselben Quelle weiter südlich
  bei ungefähr 21.624° N, 81.484° W.
- Die Umbenennung und Castros symbolische Ehrung der DDR gehören in das Jahr
  **1972**, also nach den Szenariostart. Der MDR dokumentiert die Vorstellung
  während Castros DDR-Besuch im Juni und die Enthüllung der Thälmann-Büste am
  **18. August 1972**.
- Der MDR berichtet unter Berufung auf das Auswärtige Amt und die kubanische
  Botschaft, dass keine rechtsverbindliche Gebietsübertragung erfolgte. Eine
  tatsächliche Übertragung an die DDR sollte daher als bewusste alternative
  Vereinbarung angeboten werden.

Quellen:

- [GeoNames: kubanische Inseln, einschließlich beider ähnlich benannter Cayos](https://www.geonames.org/advanced-search.html?continentCode=&country=CU&featureClass=&q=Island)
- [MDR: Eine Insel als Geschenk – Isla Ernesto Thälmann](https://www.mdr.de/geschichte/ddr/alltag/reisen-freizeit/kuba-insel-fidel-castro-100.html)

## Befund in der aktuellen Modkarte

Die Küste um Zapata ist stark vereinfacht. Provinz **9613** (Matanzas,
State **854**, Habana) besteht aus genau einer zusammenhängenden Landfläche.
Auch die östlich angrenzende Provinz **10498** ist eine zusammenhängende
Landfläche. Es gibt dort keine bereits vorhandene, isolierte Inselkomponente,
die lediglich aus der bestehenden Provinz herausgelöst werden könnte.

Das anhand der lokalen Küstenform geschätzte Untersuchungsfenster liegt bei
ungefähr **x = 1532–1540, y = 819–825**, mit Bitmap-Ursprung links oben.
Das ist keine vermessene Umrechnung von WGS84 in Spielkoordinaten und noch kein
festgelegter Inselumriss. Die umgebende See ist Provinz **5735**, strategische
Region **53** (Caribbean). Im südlichen Teil des Fensters sind die Pixel derzeit
Wasser; die Heightmap enthält dort durchgehend den Wert **88**. Der lokale
Wasserspiegel liegt gemäß `gfx/FX/constants.fxh` bei 9.5 Spielhöhen-Einheiten.

Die Insel ist nur wenige Hundert Meter breit. Bei diesem Kartenmaßstab ist eine
maßstabsgetreue Darstellung deshalb ungeeignet für eine gut auswählbare Provinz.
Ein kleiner, bewusst vergrößerter Inselumriss ist sinnvoll. Die kleinsten
vorhandenen Landprovinzen dieser Modkarte haben **9 Pixel**; das ist ein lokaler
Vergleichswert, keine nachgewiesene Mindestvorgabe des Spielmotors.

Siehe `map_location.png` und `map_audit.json` für den sichtbaren Befund und die
ausgelesenen Werte.

## Umsetzungsplan der ursprünglichen Prüfung

1. Einen kompakten, zusammenhängenden Inselumriss am geografisch passenden
   Küstenabschnitt festlegen. Ein Wasserstreifen muss die Insel vom Festland
   trennen; keine diagonalen Einzelpixel oder Vier-Provinzen-Eckpunkte erzeugen.
2. Eine freie Provinz-ID und eine global unbenutzte RGB-Farbe vergeben. Die
   nächste freie angehängte Provinz wäre bei dieser Prüfung **16537**, der nächste
   State **1252**. Diese Werte wurden anschließend für die Insel verwendet.
3. `provinces.bmp` und `definition.csv` gemeinsam ergänzen: `land`, Küste,
   passendes flaches Terrain und derselbe Kontinentwert **3** wie die übrigen
   kubanischen Provinzen. Trotz des geografischen Namens ist hier die vorhandene
   MD-Kontinentzuordnung maßgeblich.
4. Heightmap und Flussmaske an denselben Pixeln auf Land umstellen; Terrain und
   Stadtmaske passend setzen. Terrainfarben und Höhenbeleuchtung an der Küste
   prüfen. Für diese neuen Landpixel genügt eine Änderung der Provinzfarbe allein
   nicht. Die vorhandenen Bitmap-Header und indizierten Paletten erhalten.
5. Den State mit Name `Cayo Blanco del Sur`, Owner/Controller **CUB** und
   kubanischem Core anlegen; keine Industrien, Ressourcen oder militärischen
   Anlagen aus dem Nichts hinzufügen. Die Bevölkerung einer unbewohnten Insel
   muss mit dem MD-Wirtschaftssystem verträglich abgebildet werden: vorhandene
   Kleinstinsel-States verwenden teilweise `manpower = 1`. Eine neue Bevölkerung
   von null darf nicht ungeprüft eingeführt werden.
6. Eine geeignete State-Kategorie ohne große zusätzliche Industriekapazität
   wählen, die Provinz der Land-/Luftregion **212** (Cuba) hinzufügen und gültige
   Unit-/Gebäudepositionen vorsehen. Einen Hafen erst mit einer begründeten
   Ausgangslage oder einem späteren Bauprojekt anlegen. Keine Landbrücke durch
   `adjacencies.csv` zum Festland erfinden.
7. Englische Lokalisierung ergänzen und alle globalen State-Initialisierungen
   sowie laufenden Wirtschafts-/Entwicklungshelfer auf den zusätzlichen State
   prüfen. Scripts ohne BOM, Lokalisierung mit BOM speichern.
8. Pixel-/RGB-Eindeutigkeit, Flächenzusammenhang, State-/Regionszuordnung und
   Positionen prüfen. Danach mit neuem 1970-Spielstand im Spiel kontrollieren:
   sichtbar, auswählbar, begehbar und separat übertragbar. Die Machbarkeitsprüfung
   ersetzt diesen Motor-Test nicht.

## Anschluss für den künftigen Kuba-Tree

Der neue State startet 1970 kubanisch und unter dem alten Namen. Ein späteres
kubanisch-ostdeutsches Abkommen kann die Umbenennung auslösen und zwei
unterschiedliche politische Ergebnisse ermöglichen:

- Historische symbolische Ehrung: Name und Zusammenarbeit ändern sich; der State
  bleibt kubanisch.
- Alternative territoriale Vereinbarung: Nach Zustimmung beider Länder wird
  ausschließlich der Insel-State an die DDR übertragen. Das erzeugt weder einen
  neuen Country-Tag noch überträgt es Matanzas oder den gesamten State Habana.

Vor einem Transfer müssen kubanischer Besitz/Kontrolle, Existenz der DDR und
die Zustimmung zum Abkommen erneut geprüft werden. Die Umbenennung kann über
`set_state_name`, der Eigentumswechsel im DDR-Länderscope über
`transfer_state = <island_state_id>` erfolgen. Eine Übergabe ist kein Grund,
automatisch einen DDR-Core zu vergeben. Diese Hooks sind hier nur beschrieben;
es wurden keine neuen Fokus-, Event- oder Effektdateien erzeugt.
