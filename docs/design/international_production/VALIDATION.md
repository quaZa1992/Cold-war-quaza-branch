IMPERIA COLD WAR

# Konzeptprüfung vom 30. Oktober 2026

Geprüft wurden das neue Rechenmodell und die interaktive Konzeptansicht. Die Spielmechanik wurde nicht implementiert. Keine nativen Engine-, Leistungs- oder Multiplayer-Tests wurden durchgeführt. Die folgenden ursprünglichen Prüfungen dokumentieren Version 1. Deren 24-monatiger Rückverlagerungsvorschlag wurde inzwischen durch den längeren Ausstieg ersetzt.

- 576 Kombinationen aus drei Auftraggebern, vier Standortprofilen, vier Vertragszuständen, sechs Zeitpunkten und zwei Anpassungsprogrammen: alle geprüften numerischen Werte endlich; keine überbuchte Standortkapazität; keine Lieferung oberhalb des Vertragsvolumens; Konsumgüterentlastung sowie beide Empfängerboni innerhalb ihrer Obergrenzen.
- Offene Angebote: keine laufenden Kosten, keine Lieferung und kein vergangener Liefermonat.
- Produktivität 299.99 verweigert den Zugang, 300 und 300.01 gewähren ihn bei erfüllten übrigen Bedingungen.
- Drei zusätzliche Kapazitätsgrenzfälle einschließlich vollständig vergebener und überhöhter anderer Aufträge: keine doppelte Kapazitätsvergabe im Rechenmodell.
- Bedienprüfung in lokal gestartetem Chromium mit dem HTML-Fragment als Dokumentinhalt: Annahme beginnt mit Vorbereitung; Monat 12 liefert die Hälfte; finanziertes Anpassungsprogramm hat die vorgesehene Wochenbelastung; Embargo stoppt Lieferung und behält Wissen; finanzierter Ausstieg endet nach Monat 24; gesperrtes China-Profil zeigt weiterhin beide vollständigen Effektvorschauen.
- Layoutbreiten 1000, 736 und 320 Pixel: kein horizontaler Dokumentüberlauf. Visuell geprüft bei 736 und 320 Pixeln. Keine JavaScript-Seitenfehler.
- Die optionale Zustandsübergabe an die Gesprächsoberfläche ist im Fragment berücksichtigt, wurde aber nicht mit einer produktiven Host-Sitzung end-to-end geprüft.

Die Produktionskosten, Industrieeffekte, Kapazitäten und Finanzbeiträge bleiben illustrative Balancevorschläge. Die Tests beweisen die beschriebenen Modellgrenzen und Interaktionen, nicht historische Genauigkeit oder das Verhalten nativer MD-Modifikatoren. Die spätere Implementierung benötigt eigene Prüfungen gegen die echten Wirtschaftsleser, Sanktionen, parallele Angebote und Spielstandwechsel.

## Version 2: Kategorienkopf und langfristiger Ausstieg

Die neue Konzeptansicht `production-decisions.html` zeigt den Kopf einer eigenen Entscheidungskategorie mit einer Restlaufzeit für den unabhängig gespeicherten Ausstiegsdebuff.

- 640 Kombinationen aus vier Volumina, vier bisherigen Vertragsaltern, fünf Ausstiegszeitpunkten, vier Szenarien und zwei Förderzuständen: endliche Zahlen, keine negativen Restlaufzeiten, keine Lieferung über dem vereinbarten Umfang und Laufzeiten zwischen 36 und 60 Monaten bei positivem Vertragsvolumen.
- Bei gegenseitig akzeptierter Wiederaufnahme werden Lieferungen wiederhergestellt, der noch laufende Anpassungsdebuff des Auftraggebers bleibt jedoch bestehen.
- Das Beispiel mit 16 Produktionseinheiten und einem 24 Monate alten Abkommen ergibt 46 Monate Anpassungsdauer. Die Schwächung durch bezahlte Förderung reduziert die Dauer nicht unter die Mindestdauer.
- Die lokalen Kategorien- und GUI-Dateien belegen die grundsätzliche Kategorieanbindung einer `decision_category`-GUI. Das neue Fenster wurde nicht in die Engine portiert; eine native Endgeometrie ist noch nicht nachgewiesen.
- Die neue Oberfläche wurde bei 736 und 320 Pixeln ohne horizontalen Überlauf geprüft. Interaktionen für Restlaufzeit, Wiederaufnahme, zusätzliche bezahlte Förderung, finanzierte Rückverlagerung und vollständiges Auslaufen funktionierten ohne JavaScript-Seitenfehler. Bei Wiederaufnahme bleibt die bereits verstrichene Anpassungszeit erhalten.
