IMPERIA COLD WAR

# International Production: Erstes konkretes Konzept

Stand: 30. Oktober 2026. Status: Design und interaktive Konzeptansicht. Keine Implementierung in der Spielwirtschaft. Alle numerischen Balancewerte und Länderprofile sind Vorschläge. Nur Chinas hinterlegter 1970-Produktivitätswert von 144.570 wurde als tatsächlicher Startwert übernommen. Die Beispielprofile bilden keine laufende Partie ab. Die spätere Nutzerkorrektur verlangt einen langjährigen, eigenständig fortbestehenden Ausstiegsdebuff. Die ursprüngliche Vorschau mit einer 24-monatigen Rückverlagerung ist dadurch überholt; die überarbeitete Kategorienansicht verwendet 36 bis 60 Monate.

## Ziel und Umfang

Ein Land entwickelt sich durch bezahlten Kapazitätsaufbau, verlässliche Produktion, ausländische Aufträge und heimische Zulieferer zu einem Exportindustriezentrum. Der Auftraggeber erhält eine begrenzte Konsumgüterentlastung und trägt industrielle Anpassungskosten sowie Lieferabhängigkeit. Der Empfänger erhält einen gedeckelten, gemeinsamen Exportindustriespirit und trägt Absatzabhängigkeit.

Version 1 umfasst zivile Fertigung. Dienstleistungen, Rüstungsproduktion, einzelne Warenketten, Wechselkurse und automatische weltweite Auftragsauktionen bleiben außerhalb dieses ersten Entwurfs. Vertragsentscheidungen vertreten staatliche Rahmenbedingungen und vereinbarte Förderung. Private Importrechnungen werden nicht als Staatsausgaben verbucht.

## Spielerablauf und RP

1. Empfänger erschließt einen Standort durch vorhandene oder separat bezahlte Industrie, Strom und Logistik.
2. Auftraggeber wählt das Empfängerland und ein Volumen. Beide Länder sehen sämtliche voraussichtlichen Effekte vorab, auch bei aktuell gesperrtem Zugang.
3. Ein Angebot speichert Parteien, Kapazität, Kosten und Bedingungen. Es verfällt nach 30 Spieltagen. Ein offenes Angebot bezahlt und reserviert noch nichts.
4. Empfänger stimmt zu oder lehnt ab. Ein Gegenangebot verlangt erneut die Zustimmung des Auftraggebers. Kein RP-Land kann einem anderen Land einen Vertrag aufzwingen.
5. Bei Annahme erfolgen erneute Prüfungen, einmalige Zahlungen und sofortige Reservierung der erforderlichen freien Kapazität in einer gemeinsamen Transaktion.
6. Sechs Monate Vorbereitung, anschließend zwölf Monate linearer Produktionsanlauf. Volle Leistung ab Monat 18. Der Vertrag läuft danach grundsätzlich unbefristet, bis eine Seite kündigt oder Lieferungen ausgesetzt werden.

Es gibt ein ausbaubares Abkommen pro gerichtetem Länderpaar. Die Erweiterung speichert nur das zusätzliche Volumen und belastet nur dieses mit neuen Einrichtungskosten. Ein bestehender Vertrag wird durch einen Erweiterungsversuch nicht zurückgesetzt. KI-Verhalten benutzt dieselben Prüfungen und kann menschliche Zustimmung nicht ersetzen.

## Zugang und Standortkapazität

- Vorgeschlagene Produktivitätsschwelle: mindestens 300. Das ist zugleich die vorgesehene Absenkung des vorhandenen Investment-Target-Einstiegs von über 500. Die vorhandene Spielregel wurde in diesem Konzeptschritt noch nicht verändert.
- Investitionszugang mindestens 50 Prozent, entweder aus tatsächlichem Globalismus oder einer förmlich eingerichteten Exportzone. Eine Exportzone ersetzt keine Handelsgenehmigung und wirkt nur innerhalb ihrer begrenzten Standortkapazität.
- Stabilität mindestens 40 Prozent, gegenseitiger Frieden, tatsächlich erlaubter ziviler Handel und verfügbare Finanzierung.
- Keine nutzbare Produktion bei einem gegenseitigen Warenembargo. Finanzsanktionen verhindern neue Finanzierung; rein diplomatische oder militärische Sanktionen sperren zivile Fertigung nicht pauschal. Bestehende weitergehende Vertragsmoratorien bleiben bindend.
- Kein hartes Bevölkerungsminimum. Bevölkerung begrenzt das erschließbare Potenzial. Betriebsbereite Kapazität benötigt tatsächlich verfügbare Arbeitskräfte, Industrie, Energie und Logistik.

Eine Produktionseinheit entspricht für die Abstimmung dem Output einer normal ausgelasteten Zivilfabrik. Sie erzeugt keine zusätzliche Fabrik. Reservierte Exportkapazität darf nicht erneut für ein anderes Abkommen vergeben werden. Der Kapazitätsansatz muss bei der späteren Umsetzung zum heimischen Bedarf und zu den vorhandenen Fabrikfunktionen abgegrenzt werden: eine Reservierung darf dieselbe Fertigung nicht gleichzeitig als zusätzliche heimische und ausländische Wertschöpfung ausweisen.

Kapazität ist das Minimum aus nutzbaren Industrie-, Arbeitskräfte-, Energie- und Logistikkapazitäten. Das Land kann größere Potenziale durch bezahlten Ausbau erschließen. Gebäudebau benutzt vorhandene Investitionswege. Jede spätere Gebäudevergabe erhält vorher einen zusätzlichen gemeinsamen Staatsbauplatz pro Stufe im selben Staat. Besitz, Kontrolle und native Gebäudekapazität bleiben eigenständige Prüfungen.

Chinas 1970-Ausgangslage erfüllt die Produktivitätsschwelle noch nicht. Das Exportzonenprofil zeigt eine mögliche spätere Entwicklung, keine automatisch gewährte Reform und keinen zusätzlichen bereits existierenden Fokuspfad.

## Kostenvergleich und Konsumgüterentlastung

Für das transparente erste Rechenmodell werden alle GDP/c-Werte in derselben internen Preisbasis benutzt. GDP/c dient als Kostenproxy, nicht als gemessener Lohn. Der Kostenvorteil ist relativ zum jeweiligen Auftraggeber. Entfernung, Zugang und Verlässlichkeit können den günstigen Produktionsstandort verteuern.

Im Simulator beträgt der Kostenindex, bei heimischer Produktion gleich 100:

`100 * clamp(0.35 + 0.65 * cbrt(GDPc_Empfaenger / GDPc_Auftraggeber) + Transport + 0.15 * (1 - Zugang) + 0.15 * (1 - Stabilitaet), 0.4, 1.5)`

Transport ist im Beispiel eine bewusst grobe vorgegebene Länderpaar-Kostenkomponente. Der Simulator differenziert die Transportkosten noch nicht nach allen drei auswählbaren Auftraggebern. Die spätere Spielmechanik soll höchstens vier vorberechnete Verbindungsklassen benutzen: gemeinsamer Landkorridor, regionaler Seehandel, Fernhandel und erschwerte Verbindung. Keine monatliche Pfadfindung für jedes Abkommen.

Kostenersparnis `s = clamp(1 - Kostenindex / 100, 0, 0.6)`. Der Wurzelexponent und alle Gewichte sind Balancevorschläge. Die Formel schätzt keine historisch exakten Löhne oder Güterpreise und ersetzt später keine Plausibilitätskalibrierung.

`Auslagerbarer Bedarf D = native Konsumgueter-Berechnungsbasis N * Konsumgueterquote ohne dieses System B * 0.5`

`Neues Volumen q <= min(freie Standortkapazitaet, noch nicht zugeteilter Bedarf, 30)`

`Entlastung der Quote = Summe(gelieferte Einheiten * Kostenersparnis) / N`

Die Gesamtentlastung ist auf 20 Prozent der Konsumgüterquote ohne dieses System begrenzt. Bei 30 Prozent Ausgangsquote beträgt der maximale Beitrag folglich sechs Prozentpunkte. Die tatsächliche native Rundung entscheidet, wie viele Fabriken frei werden. N ist die native Konsumgüterbasis und darf bei der Implementierung nicht ungeprüft durch die Zahl der Zivilfabriken ersetzt werden.

Die Vorschau zeigt sowohl den tatsächlichen relativen Consumer Goods Factories Factor als auch die resultierende Quote. Der eigene Modifier wird aus der Basisrechnung herausgerechnet, damit eine monatliche Rückkopplung die Entlastung nicht künstlich vervielfacht. Durchgeleitete Exporte und dieselbe Produktionseinheit dürfen kein zweites Mal als neuer Endbedarf gezählt werden.

## Einrichtung und laufende Staatskosten

| Beitrag je vereinbarter Produktionseinheit | Auftraggeber | Empfänger |
| --- | ---: | ---: |
| Einmalige Programmeinrichtung | $0.25 Milliarden | $0.10 Milliarden |
| Wöchentliche Betreuung je gelieferter Einheit | $0.002 Milliarden | $0.001 Milliarden |
| Optionale heimische Industrieanpassung je betroffener Einheit und Woche | $0.005 Milliarden | 0 |
| Befristete finanzierte Rückverlagerung je ursprünglich vereinbarter Einheit und Woche | $0.008 Milliarden | 0 |

Das sind öffentliche Organisations-, Anpassungs- und Verwaltungskosten. Sie enthalten keine kostenlose Fabrik und keinen erneut berechneten allgemeinen Strompreis. Der Bau zusätzlicher Anlagen wird separat bezahlt. Einrichtung wird nur bei erster Annahme oder für echte Zusatzkapazität berechnet. Aussetzung, Wiederaufnahme, Laden eines Spielstands und erneutes Öffnen der Vorschau lösen keine neue Zahlung oder Belohnung aus.

Wiederkehrende Beträge werden ausschließlich in wöchentlichen MD-Einheiten integriert und angezeigt. Script-Literale erhalten höchstens fünf Nachkommastellen. Laufende Betreuung skaliert mit tatsächlich gelieferter Produktion. Während der Vorbereitungsphase fallen keine mengenabhängigen Lieferkosten an.

## Dynamischer Empfängerspirit und Lernen

Ein Land besitzt genau einen zusammengefassten Spirit `Export Manufacturing Network` für alle Abkommen.

`x = gesamte aktive auslaendisch beauftragte Produktion / vorhandene zivile Industriekapazitaet`

`Zivilfabrikbau = min(20 Prozent, 16 Prozent * x + 4 Prozent * L / 100)`

`Zivile Industrieproduktivitaet = min(10 Prozent, 6 Prozent * x + 4 Prozent * L / 100)`

L ist der gespeicherte Zulieferer- und Wissensstand von 0 bis 100. Der erste Simulator erhöht ihn pro abgeschlossenem Liefermonat um `0.6 * gelieferte Einheiten / zivile Industriekapazitaet`. Bestehende Profile haben einen illustrativen bereits aufgebauten Bestand. Lieferstopps löschen diesen Bestand nicht. Neue Aufträge ohne tatsächliche Lieferung erzeugen keinen Lernfortschritt. Für eine spätere Balance können Qualifikation und Technologiegefälle den Lernzuwachs verändern; der Simulator behauptet diese Erweiterung noch nicht.

Die Vorschau zeigt die Veränderung durch das neue Abkommen und den gesamten resultierenden Spirit. Derselbe Gesamtbonus darf niemals pro Partner erneut addiert werden. Neue Fabriken erzeugen Beschäftigung und BIP bereits durch die vorhandenen MD-Leser. Es gibt keinen zusätzlichen pauschalen BIP-Zuschlag für dieselbe Fabrik.

## Anpassung beim Auftraggeber

Der erste konkrete Entwurf bildet den industriellen Strukturwandel über einen heimischen Anpassungsbestand ab. Der neue Spirit `Industrial Adjustment` enthält:

- Zivile Industrieproduktivität: `-min(8 Prozent, 20 Prozent * betroffene Einheiten / heimische Zivilindustrie)`.
- Gewerkschaftsmeinung: `-round(min(15, 30 * betroffene Einheiten / heimische Zivilindustrie))`.

Ein finanziertes Anpassungsprogramm reduziert beide Belastungen auf 60 Prozent. Es ist eine echte wöchentliche Ausgabe und keine dauerhafte kostenlose Entscheidung. Die Vorschau zeigt den vollen vorgesehenen Belastungsumfang. Beim Anlauf wächst der Anpassungsbestand mit der tatsächlich verlagerten Produktion. Ein abrupter Lieferabbruch entfernt ihn nicht.

Version 1 behauptet keine exakt aus diesen Modifiern errechneten verlorenen Arbeitsplätze. Eine quantitativ belastbare Arbeitsplatzverlagerung braucht eine zusätzliche Integration in die Beschäftigungsleser. Produktivitäts- und Gewerkschaftseffekte sind hier die konkret vorgeführten Stellvertreter für die Anpassungsbelastung. Allgemeine verfügbare Arbeitskraft wird nicht reduziert.

## Abhängigkeit, Sanktionen und Ausstieg

Zwei gesonderte Kennzahlen:

- Käuferabhängigkeit: vereinbarte Produktion dieses Standorts geteilt durch den auslagerbaren Bedarf des Auftraggebers.
- Kundenkonzentration: Aufträge dieses Käufers geteilt durch alle ausländischen Aufträge des Empfängers. Dies ist ausdrücklich kein Anteil am gesamten BIP und allein kein nationaler Schadensmultiplikator. Die Größe des Exportsektors kommt zusätzlich über x hinzu.

Bei einem Warenembargo fällt die betroffene Lieferung sofort auf null. Die zugehörige Entlastung und der aktive Exportbonus entfallen. Andere Abkommen und gespeichertes Wissen bleiben bestehen. Die spätere Nutzerkorrektur ersetzt den ursprünglich vorgesehenen 24-monatigen zusätzlichen Lieferengpass durch den nachfolgend definierten langfristigen Anpassungsbestand. Beide Zuschläge werden nicht zusätzlich auf denselben Versorgungsschaden gestapelt.

Die bestehenden allgemeinen Sanktionsrückwirkungen bleiben Teil derselben Gesamtrechnung. Der neue Lieferkanal muss vor Umsetzung gegen deren enthaltene Schäden abgegrenzt oder angerechnet werden. Es darf keinen doppelten pauschalen Versorgungsschaden geben. Militärische und diplomatische Maßnahmen erhalten keine sachlich unpassende vollständige Warenblockade.

Eine Seite kann aus Sicherheitsgründen sofort aussteigen. Keine pauschale Unkündbarkeit und kein Sanktionsschutz durch rein wirtschaftliche Abhängigkeit. Die wirtschaftlichen Folgen verhindern den kostenlosen Ausstieg.

Geordnete Rückverlagerung dauert nach der Nutzerkorrektur mindestens 36 und höchstens 60 Monate. Lieferungen und Entlastung sinken mit tatsächlich ersetzter Kapazität. Der Auftraggeber bezahlt das Rückverlagerungsprogramm und weist nutzbare heimische Arbeitskräfte, Energie und Ersatzkapazität nach. Nur tatsächlich ersetzte Kapazität baut den Anpassungsbestand ab. Die Kategorienansicht zeigt den vollständig finanzierten und kapazitätsgedeckten Fall. Bei Ausfall der Finanzierung oder Ersatzkapazität pausiert der reale Rückbauplan; er erfüllt sich nicht allein durch Zeitablauf.

Während einer Aussetzung dürfen Kapazitäten nur über eine sichtbare Neuvergabe wieder verwendet werden. Wiederaufnahme erhält keine doppelten Anlagen oder Gebühren und braucht verfügbare Kapazität. Wurde sie anderweitig gebunden, ist eine neue beiderseitig akzeptierte Kapazitätszusage erforderlich.

## Nutzerkorrektur: Langjähriger Ausstieg und Kategorienkopf

Der Ausstieg erzeugt einen eigenständigen Anpassungsbestand, sobald tatsächlich eine Produktionsverbindung aufgebaut wurde. Ein noch nicht angenommener Vorschlag erzeugt keinen Ausstiegsdebuff; Abbruch während reiner Vorbereitung verliert bezahlte Einrichtung, aber keine erfundene langjährige Lieferabhängigkeit.

`d = betroffenes Vertragsvolumen / auslagerbarer Bedarf des Auftraggebers`

`t = clamp((abgeschlossene Vertragsmonate - 6) / 60, 0, 1)`

`Dauer = clamp(36 + round(12 * d + 12 * t), 36, 60) Monate`

`Staerke = d * (0.5 + 0.5 * t)`

Die Koeffizienten sind Balancevorschläge. Größe und bisherige Einbindung bestimmen die Belastung; eine Kündigung ist kein politisches Verbot. Die Kategorienansicht setzt voraus, dass die gezeigte Verbindung bereits produktiv ist. Eine spätere echte Transaktion friert Volumen, Einbindungsstand und Dauer am Ausstiegsbeginn ein. Laufende Vertragsänderungen können den Bestand nicht rückwirkend verkleinern.

Der Auftraggeber erhält `Supply Chain Readjustment`: zusätzlicher Consumer Goods Factories Factor bis `+12 Prozent * Staerke`, Zivilfabrikbau `-15 Prozent * Staerke`, Stabilität `-6 Prozent * Staerke`. Die Beiträge sinken im finanzierten Beispiel monatlich mit dem verbleibenden Anpassungsbestand. Geordnete Rückverlagerung halbiert die zusätzliche Schockstärke, unterschreitet aber nicht die Mindestdauer von drei Jahren. Der Verlust der bisherigen Importentlastung wird separat berechnet und nicht nochmals als derselbe Bonusverlust abgezogen.

Zusätzliche Anpassungsförderung kostet je ursprünglich betroffener Einheit $0.005 Milliarden pro Woche und reduziert die zusätzliche Schockstärke um 25 Prozent. Sie entfernt den Bestand nicht sofort und verkürzt die Mindestdauer nicht. Die laufende finanzierte Rückverlagerung kostet weiterhin $0.008 Milliarden je ursprünglich vereinbarter Einheit und Woche, jetzt über die tatsächlich benötigte längere Laufzeit.

Der Empfänger bekommt bei unbesetzter frei werdender Kapazität `Export Market Readjustment`. Dessen maximale Produktivitäts- und Baubeiträge skalieren mit dem verloren gegangenen Volumen relativ zur gesamten Zivilindustrie, nicht nur mit dem Anteil eines Käufers an seinen Exporten. Neue tatsächlich gelieferte Ersatzaufträge reduzieren diese ungenutzte Kapazität. Know-how und vorhandene Anlagen werden nicht gelöscht.

Der Anpassungsbestand wird außerhalb des gekündigten Vertrags gespeichert. Kündigen, Entfernen des Vertragseintrags, Beitritt zu einem anderen Abkommen, gegenseitig akzeptierte Wiederaufnahme und Laden eines Spielstands löschen ihn nicht. Auch ein selbst verhängtes Warenembargo löst den tatsächlichen Lieferabbruch aus und umgeht die Anpassungskosten nicht. Wiederaufnahme kann Lieferungen wiederherstellen; die bereits entstandenen Anpassungskosten des Auftraggebers laufen weiter. Der Empfänger kann seine ungenutzte Kapazität dagegen durch echte Ersatzaufträge reduzieren. Bereits abgebaute Bestände dürfen durch erneutes Laden nicht erneut abgebaut werden. Mehrere Abbrüche werden zu einem gedeckelten Länderbestand mit nachvollziehbaren Beiträgen zusammengefasst, nicht als unbegrenzte Multiplikation identischer Spirits.

Für die Benutzeroberfläche wird eine eigene Entscheidungskategorie `International Production` vorgeschlagen. Oben innerhalb dieser Kategorie steht eine kompakte Übersicht: Auslandslieferanteil, aktuelle Konsumgüterquote, größter relevanter Partner und verbleibende Anpassungszeit. Der gefüllte Zeitbalken zeigt die noch bestehende Belastung. Er wird nicht als Klick-Minispiel verwendet. Darunter folgen normale Entscheidungen für Verhandlungen, Erweiterungen, Diversifizierung und Ausstieg. Eine aufklappbare Abkommens- beziehungsweise Ausstiegsansicht zeigt beide Länder mit ihren vollständigen konkreten Modifiern und Kosten. Für Empfängerländer wechselt die Übersicht auf eingehende Aufträge, gebundene Exportkapazität und Kundenkonzentration.

Ein kategorienspezifischer Kopf ist lokal grundsätzlich belegt: `common/decisions/categories/00_agrarian_economics_category.txt` hängt `agri_statistics` an seine Kategorie; `common/scripted_guis/01_agri_scripted_gui.txt` benutzt `context_type = decision_category`; das vollständige Fenster steht in `interface/agriculture_decisions.gui`. Die neue Ansicht ist ein eigenes HTML-Konzept, kein vollständiger nativer Port und keine vermessene finale Engine-Geometrie. Ein globaler Umbau des gesamten Decisions-Menüs ist dafür nicht vorgesehen.

Die Kategorie liest zwischengespeicherte Länderwerte. Monatliche Abrechnung und gezielte Änderungen invalidieren sie; das reine Anzeigen oder Schweben über einen Balken führt keine Länder-, Vertrags- oder Staatensuche und keine Zahlung aus. Der Monatsabschluss bleibt unabhängig davon aktiv, ob ein menschlicher Spieler die Kategorie geöffnet hat.

## Performance und Multiplayer-Sicherheit

- Vorgeschlagener globaler Rahmen: maximal 256 aktive oder ausgesetzte Vertragsdatensätze. Die Obergrenze ist eine transparente Ressourcenbegrenzung, kein getestetes Engine-Limit. Ein Länderpaar erweitert seinen vorhandenen Datensatz.
- Keine tägliche Suche über alle Länderpaare und keine monatliche Pfadfindung. Das sichtbare Standortmenü prüft eine begrenzte Kandidatenliste erst beim Öffnen beziehungsweise Aktualisieren.
- Einmal monatlich: vorhandene MD-Länderwerte zwischenspeichern, aktive Verträge durchgehen, Beiträge pro Land summieren und einen zusammengefassten Modifier pro Rolle aktualisieren. Aufwand wächst mit Ländern plus vorhandenen Verträgen, nicht mit allen möglichen Länderpaaren.
- Wöchentliche Finanzbuchung liest die vorher aggregierten Länderbeiträge. Sie führt keine weltweite Standortsuche aus.
- Annahme, Ausbau, Embargo, Krieg, Kündigung und Kapazitätsneuvergabe lösen zusätzlich nur für betroffene Vertragsseiten eine Aktualisierung aus. Keine tägliche Kontrolle sämtlicher Angebote; Verfall über befristete Angebote und gezielte Ereignisse.
- Bei gemeinsamer Unterversorgung werden zugesagte Lieferungen proportional gekürzt. Keine Bevorzugung aufgrund der Reihenfolge der Länder- oder Vertragsschleife.
- Ein fester Vertragsbezeichner und ein Zahlungsbeleg sichern jede Annahme und Erweiterung. Annahme prüft Sender, Empfänger, Angebotsstand, Datum, verfügbare Mittel und noch freie Kapazität unmittelbar vor der Mutation.
- Zustand und Lernen beruhen auf Spielzeit und abgeschlossenen Lieferperioden. Zeitanteile werden bei Übergängen beziehungsweise Monatsabschluss abgerechnet. Ein Vertragswechsel am Monatsende liefert keinen vollen zusätzlichen Lernmonat. Kein Zufall und keine reale Uhrzeit für Wirtschaftseffekte.
- Rückwirkungen, Geld und Kapazität werden gemeinsam aktualisiert. Eine Vorschau verändert weder Geld noch Vertragszustand. Effektwerte beider Länder bleiben vor Annahme sichtbar.
- Beim Laden wird vorhandener Vertragszustand abgeglichen. Gebühren, Bauplätze, Anlagen und Lernfortschritt dürfen dadurch nicht erneut ausgezahlt werden.
- Wirtschaftliche Effekte einer Länderübernahme, Auflösung und geänderter Kontrolle müssen über die tatsächlichen Vertragsparteien aufgelöst werden. Ein fremder Nachfolgestaat erbt keine ungeprüfte Zustimmung.
- Benachrichtigungen nur bei Angebot, Antwort, wesentlicher Unterbrechung und abgeschlossenem Ausstieg. Keine monatlichen Bestätigungsfenster und keine Sanktionserlaubnis eines anderen Spielers.

Dies ist eine begrenzte statische Arbeitslastplanung. Multiplayer-Synchronität und tatsächliche Engine-Laufzeit sind damit noch nicht nachgewiesen. Vor späterer Veröffentlichung sind gemeinsame Spielstand-, Parallelangebot-, Kapazitäts-, Sanktions- und Wiederladetests erforderlich.

## Bereits vorhandene Integrationspunkte

- `common/on_actions/zzzzzz_mdcw_imperia_globalism_on_actions.txt`: heutige Investment-Target-Zugangsprüfung und Standortbonus. 300 ist der neue vorgeschlagene Einstieg, keine automatische Übernahme aller bisherigen Bedingungen.
- `common/scripted_effects/mdcw_imperia_globalism_effects.txt`: tatsächlicher Globalismus, langsame Anpassung und bestehende wirtschaftliche Wirkungen.
- `common/ideas/ICW_economic_organisation.txt`: sieben Wirtschaftsorganisationsmodelle. Selektive Exportzonen bleiben mit staatlich gelenkter Entwicklung vereinbar.
- `common/scripted_effects/99_investment_scripted_effects.txt`: Geld, Zustimmung, bestehende Bauprojekte. Vor Wiederverwendung müssen komplette Transaktionen einschließlich Bauplatzvergabe geprüft werden.
- `common/scripted_effects/00_money_system.txt`: Konsumgüterbasis, zivile Sektorproduktivität, Steuern, BIP und Beschäftigung. Native Leser und Grenzwerte brauchen vor Implementierung eine gezielte Prüfung.
- `common/scripted_effects/!_energy_effects.txt`: vorhandene Energieversorgung und Verbrauchswerte für Kapazitätsgrenzen.
- `common/scripted_effects/imp_sanctions_effects.txt`: bestehende Sanktionseffekte und Rückwirkungen.
- `common/scripted_effects/mdcw_cold_war_effects.txt`: vorhandene Weltmarktexposition. Bestehende Globalismus- und Weltmarktboni werden nicht noch einmal als angeblich neue Wirkung ausgezahlt.

## Historische Grundlage und Herkunft

Die Koeffizienten dieses Entwurfs sind eigene Balancevorschläge. Quellen begründen Zusammenhänge, nicht diese Spielzahlen.

- Douglas Zhihua Zeng, World Bank, Global Experiences with Special Economic Zones: Focus on China and Africa, 2015: Reformöffnung, Exportzonen, Infrastruktur, Investitionen aus Hongkong und Taiwan, Technologielernen, heimische Zulieferer und institutionelle Risiken. https://documents.worldbank.org/curated/en/810281468186872492/pdf/WPS7240.pdf
- David H. Autor, David Dorn und Gordon H. Hanson, The China Shock: Learning from Labor Market Adjustment to Large Changes in Trade, 2016: konzentrierte und lang anhaltende Anpassungskosten betroffener Arbeitsmärkte. Importkonkurrenz ist nicht mit jeder einzelnen Direktinvestition gleichzusetzen. https://www.nber.org/papers/w21906
- WTO, Rückblick auf Chinas Beitritt am 11. Dezember 2001: verlässlicherer Marktzugang als spätere Entwicklungsstufe, keine 1970 bereits verfügbare WTO-Mitgliedschaft. https://www.wto.org/english/news_e/news21_e/acc_10dec21_e.htm

Neuer Konzepttext, Rechenmodell und interaktive Darstellung: für Enes mit Codex erstellt. Die Darstellung benutzt keine übernommenen Bilder, Logos, Frame-Pixel oder sonstigen Binärassets. Institutionelle Quellen wurden zusammengefasst, nicht als Artwork übernommen. Die konkrete Projektlizenz für diese neuen Entwurfsdateien ist nicht zusätzlich festgelegt. Rechte und Lizenzen vorhandener MD- und Drittanbieterinhalte bleiben ihren jeweiligen Quellen zugeordnet.
