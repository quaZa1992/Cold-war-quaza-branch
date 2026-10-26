# Irak: Belohnungsvielfalt und laufende Verwaltungskosten

19. Oktober 2026. **Der Einwand ist berechtigt.** Die Hauptwahlen wurden zuletzt stärker, viele Nebenfoki verwenden aber weiterhin dieselben kleinen Stabilitäts-, Forschungs- und Verwaltungsbausteine. Besonders problematisch sind dauerhaft steigende Kosten neben bereits gedeckeltem Nutzen und Pflichtkarten ohne eigene Leistung.

Dies ist ein **lesender Audit mit Änderungsvorschlägen**. Keine geladenen Fokus-, Effekt-, Ideen- oder Lokalisierungsdateien wurden dafür bearbeitet; kein Ländercompiler wurde ausgeführt. Die vorgeschlagenen Werte sind neue Balanceentwürfe, keine installierten Effekte oder historischen Wirkungszahlen.

## Vollständiger Bestand

[Alle 410 Foki mit englischem Namen, Dauer, BIP-Preis, tatsächlichen Modifikatoren, Einmalbelohnungen, Spirit-Änderungen und Entscheidungen](FOCUS_INVENTORY.md). Derselbe Bestand liegt als [CSV](FOCUS_INVENTORY.csv) und [JSON](FOCUS_INVENTORY.json) vor. Die 16 verborgenen Kompatibilitätseinträge sind keine spielbaren Foki und zählen hier nicht mit.

| Befund | Aktueller Bestand |
|---|---:|
| Aktive Foki | 410 |
| Foki mit höheren Bürokratiekosten | **140 / 34,1%** |
| Foki mit niedrigeren Bürokratiekosten | 10 |
| Foki mit höheren Sozialkosten | 48 |
| Foki mit positiver Programm-Stabilität | **99** |
| Foki mit politischem Machtfaktor, beide Vorzeichen | 77 |
| Foki mit einer tatsächlichen Gebäudebelohnung | 23 |
| Foki mit begrenztem Forschungsbonus | 9 |
| Foki mit Entscheidungsfreischaltungen | 78 |
| Individuelle Fokusbewertungen | **44: 40 Änderungsvorschläge, vier bewusst behalten** |

Häufigkeit allein entscheidet nicht über Qualität. Ein Bürokratiemalus bei einer neuen Provinzverwaltung passt; derselbe Malus bei jeder Wartung, Forschungsmission und Buchhaltungsrunde erzeugt wenig unterschiedliche Spielentscheidungen. Eine Wahlfreischaltung oder die Verbesserung eines Start-Spirits kann ein großer echter Nutzen sein, auch ohne Fabrik oder grünen Programmwert.

Die Zahlen kommen aus aktuellen Modifikatorfeldern und den geladenen Vorschau-/Ausführungspfaden. Alte `reward_summary`-Texte im Katalog sind teilweise überholt und wurden ausdrücklich nicht als Istwerte benutzt. Alle 410 numerischen Fokusvorschauen, Rechnungssätze und Entscheidungslisten wurden dagegen abgeglichen.

## Was den Eindruck verursacht

**Identische Pakete unter sehr verschiedenen Namen.** Zehn Foki wiederholen `+2% Steuerertrag / +2% Bürokratie`, darunter Oil Accounts und Sovereign Accounts. Acht wiederholen `+3 Stabilitätspunkte / −2% PP-Gewinn`; acht weitere `+2 Stabilitätspunkte / +3% Bürokratie`. Dawa und IIP haben mehrere nahezu gleiche Sozialmarkt-, Wohlfahrts-, Medizin- und Bürgerrechtsbausteine. Ihre Rolle und Geschichte unterscheiden sich stärker als ihr derzeitiger Spielnutzen.

**Zusätzliche Stabilität kann ihren Nutzen verlieren.** Der installierte Programmverbraucher begrenzt die Summe positiver Programm-Stabilität auf 15 Punkte. Negative Stabilitätsbeiträge und laufende Kosten bleiben bestehen. Ein komplett kompatibler Dawa-Parteipfad liefert bereits 22 positive Punkte, IIP 20 und Civic/KDP je 19, bevor gemeinsame Staats- und Gesellschaftsprogramme hinzukommen. Ein weiterer reiner `+2 Stabilität / +2% Bürokratie`-Fokus kann dann die Kosten erhöhen, ohne die gesamte positive Stabilität zu erhöhen. Der Vorschlag lautet, solche Belohnungen zu spezialisieren; der gemeinsame Deckel muss dafür nicht abgeschafft werden.

**Leere oder rein negative Zwischenschritte.** Foreign Policy Dossier, External Obligations, Contingency Planning und Civil Crisis Authority liefern ihren eigenen generischen Verwaltungsaufschlag und Nachfolgerzugang, aber keine entsprechende zusätzliche diplomatische, militärische oder zivile Leistung. The Campaign Ledger und Fight Through Attrition reichen vor allem echte Kampagnenbedingungen weiter. Solche Karten sollten in ihre konkrete Folgepolitik eingehen; bloß erfundene Ersatzboni würden den Baum nur aufblasen.

**Einige Begriffe greifen auf die falsche Wirkung zurück.** `foreign_influence_modifier` stärkt die eigene offensive Einflussnahme; Einflussabwehr besitzt einen anderen tatsächlichen Reader. Ein negativer offensiver Wert ist kein unmittelbarer Schutz gegen fremden Einfluss. Ebenso verbessert eine Stabilitätszeile weder Gesundheitsversorgung noch Alphabetisierung. Thematisch passende native Systeme existieren bereits.

## Konkrete Vorher-/Nachher-Vorschläge

Alle neuen Werte ersetzen die benannten alten Werte. Kosten, die im jeweiligen Vorschlag beibehalten werden, bleiben zusätzlich relevant. Die ausführlichen 44 Bewertungen mit Begründung stehen in [RECOMMENDATIONS.md](RECOMMENDATIONS.md).

| Tatsächlicher Fokusname | Aktuell | Empfohlene Richtung |
|---|---|---|
| **Foreign Policy Dossier** | 21 Tage; nur +2% Bürokratie | Als separate Pflichtkarte entfernen; Vorbereitung in die beiden realen diplomatischen Einstiege übernehmen. |
| **External Obligations** | 35 Tage, 0,5% BIP; nur +1% Bürokratie | Mit der gewählten Vertrags-/Kooperationspolitik zusammenlegen; tatsächliche Empfängerzustimmung und Vertragsgebühren behalten. |
| **The Campaign Ledger** | 21 Tage, 0,5% BIP; keine eigene numerische/physische Belohnung | Mit den Kampagnenfolgen verbinden; wirkliche Iran-Kriegsteilnahme weiterhin ausdrücklich prüfen. |
| **A Provincial Settlement** | 49 Tage, 2% BIP; +2% Bürokratie, −2% PP | Budget und Bedingungen in Equal Citizenship / Central State Rule integrieren. Deren echte Compliance-Unterschiede und spätere Core-Bedingungen behalten. |
| **Power Dispatch** | +2% Baugeschwindigkeit, +2% Bürokratie; 1% BIP | Bauwert und Preis behalten; statt Bürokratie **−5% Brennstoffverbrauch tatsächlicher fossiler Kraftwerke**. |
| **Neglected Districts** | +2 Stabilitätspunkte, +2% Bürokratie; 1,5% BIP | **Eine echte Infrastruktur in Nineveh 166**; Preis auf 2,5% BIP. Vor Zahlung Eigentum, Kontrolle und freie Infrastrukturkapazität prüfen. |
| **Maintain Laboratories** | +2% allgemeine Forschung, +2% Bürokratie; 2% BIP | **2×25% Elektronikforschung**, +1% tatsächliche Bildungskosten; bisherige Dauermodifikatoren ersetzen. |
| **Technical Missions** | +3% allgemeine Forschung, +2% Armeepersonalkosten; 2% BIP | **1×30% Industrie- und 1×25% Bauforschung** einmalig; keine fachfremde dauerhafte Militärrechnung. |
| **A National Staff College** | +3% Erholung, +3% Ausbildungszeit; 1,5% BIP | **25 Armee-XP und 1×25% Landdoktrinrabatt**; längere Ausbildung und Preis behalten. Mit gemeinsamem Staff Training wären es zusammen 60 einmalige XP und zwei getrennte Rabattverwendungen. |
| **Community Medicine** | +3 Stabilitätspunkte, +4% Sozialkosten; 2% BIP | **730 Tage −10% reale Gesundheitskosten**, laufend +2% Sozialkosten; keine automatische Gesundheitsgesetz-Stufe oder Gratisbevölkerung. |
| **Small Business Law** | +2% allgemeines Bauen, +2% Bürokratie; 1,5% BIP | **+10% Baugeschwindigkeit nur ziviler Fabriken**, −3% Steuerertrag im laufenden IIP-Programm; tatsächliches Bauen bleibt nötig. |
| **Constitutional Charter** | +8% offensiver Auslandseinfluss, +2% Bürokratie | Schnellere tatsächlich angenommene Auslandsinvestitionen und +10% Einflussabwehr; laufende Verwaltung und echte Investorentscheidung bleiben. |

Diese Alternativen geben verschiedene Dinge: technische Anwendungen, Ausbildung, reale Anlagen, Betriebseffizienz, konkretes Investitionsverhalten und zeitlich begrenzte Programme. Einmalige Projektkosten, Fokuszeit, Lieferbedingungen und ein entgangener Alternativweg sind bereits echte Kosten. Ein zusätzlicher permanenter Nachteil braucht jeweils einen eigenen inhaltlichen Grund.

## Ganze erreichbare Wege statt unvereinbarer Gesamtsummen

Die Wirtschaftsprüfung definiert zwei konkrete friedliche Wege durch Öl, Industrie, Landwirtschaft und Gesellschaft. Sie enthält keine fremden Regierungsprogramme, keine Bakr-/Saddam-Mischung und keine Kriegsprämien. Heimatstaaten, Finanzierung und freie Baukapazität sind angenommen; alle Prerequisite-Gruppen und Ausschlüsse der Listen sind nachgerechnet.

| Vollständiger Vier-Kapitel-Weg | Aktuell | Nach dem Entwurf |
|---|---|---|
| Ölrente + zivile Industrie + Kooperativen/lokale Bewässerung + Lehrer/gezielte Dienste | 47 Foki; 1.729 Fokustage; **+52% Bürokratiebeitrag** | +37% Bürokratiebeitrag; begrenzte Fachforschung, reale Infrastruktur und Kraftwerks-Brennstoffeffizienz |
| Diversifizierung + Grundindustrie + Kooperativen/Großbewässerung + Alphabetisierung/universelle Dienste | 46 Foki; 1.680 Fokustage; **+43% Bürokratiebeitrag** | +33% Bürokratiebeitrag; stärkere Bewässerungsinfrastruktur, nativer Produktivitätsfortschritt und Gesundheitsbetriebseffizienz |

Das ist keine pauschale Verstärkung: Beide Entwürfe verlieren unter anderem wiederholte Steuer-, Export-, allgemeine Forschungs- und gedeckelte Stabilitätsbeiträge. Einzelne reale Projekte werden teurer. Der Vorteil liegt in unterschiedlichen Ergebnissen statt immer derselben Verwaltungsrechnung. Die genauen Restwerte und vollständigen Knotenlisten stehen im [Wirtschaftsbericht](ECONOMIC_REVIEW.md).

**Einheiten beachten:** Die +52 addieren sich zum Multiplikator der Bürokratie-Ausgabenzeile. Es sind keine 52 Prozentpunkte des gesamten Staatshaushalts. Bleiben die anfänglichen July-State- und Patronage-Beiträge von zusammen +18 bestehen, ergibt das vor weiteren Quellen +70. Bei eingefrorener Wirtschaftsgrundlage wäre der Vergleich `1,18 × Basis → 1,70 × Basis`, also rund 44,1% mehr als die anfänglichen Bürokratieausgaben. Wachstum, Inflation, Gesetze und politische Reformen verändern die tatsächliche Rechnung.

## Vorhandene gute Inhalte erhalten

Basic Industries First / Consumer Expansion, Berufskern / Reserve, Presidential Guard / The Regular Army sowie Sowjetstandardisierung / Lieferantenmix haben bereits echte unterschiedliche Ergebnisse. Zusätzliche generische Boni würden sie eher verwässern. Ministerial Payrolls und Funded Guarantees ändern tatsächlich vorhandene Start-Spirits; sie sind keine leeren Karten. Die neue Provinzverwaltung ist ein sinnvoller Ort für reale dauerhafte Verwaltungskosten. A Workable Iraqi State liefert eine passende Verwaltungseffizienz als Abschluss.

Der schwierige Start, die massiven wirklichen Iran-Kriegskosten, Golfkredite, Nachkriegskrise und die materiellen Kuwait-/Khuzestan-Ziele bleiben eigenständige historische Kampagnenmechaniken. Belohnungsvielfalt ist kein Grund, diese Belastungen zu entfernen oder jedes Dorfprojekt mit nationaler Angriffskraft zu versehen.

## Referenzen und spätere Umsetzung

Der [MD-Referenzbericht](MD_REFERENCE_PALETTE.md) prüft 20 konkrete normale 2000er-Beispiele aus Russland, Deutschland, Israel und Türkei einschließlich tatsächlicher Provider/Reader. Beispiele sind bessere Spezialisierung gegen längere Ausbildung, Bewegungstempo gegen Nachschubverbrauch, empfängerabhängige Ausbildung sowie zeitlich begrenzte Bildung mit eigenen Bildungskosten. Die 1970 verwendbaren Forschungskategorien wurden geprüft; heutige Excavation-/Fuel-Refining-Einstiege ab 1985/1990 sind keine unmittelbaren Januar-1970-Prämien.

Historischer Themenanker: Zeitgenössische Einschätzungen nennen Bewässerung, Vermarktung, Transport/Lagerung und Fachkräfte beziehungsweise Ersatzteile als konkrete Entwicklungsengpässe; eine weitere beschreibt pragmatisch gemischte Wirtschaftsformen. Daraus lassen sich unterschiedliche technische und institutionelle Spielprogramme ableiten. Die vorgeschlagenen Prozentwerte sind eigene Balanceentwürfe. [FRUS-Lagebild 1976](https://history.state.gov/historicaldocuments/frus1969-76v27/d317), [FRUS-Einschätzung 1973](https://history.state.gov/historicaldocuments/frus1969-76v27/d208).

Vor einer Umsetzung zuerst reine Pflicht-/Aktenkarten zusammenlegen, dann gedeckelte oder geklonte Programme spezialisieren und zuletzt ganze exklusive Wege erneut bilanzieren. Alte IDs, eingefrorene offene Angebote, bezahlte Lieferbelege und Programmwechsel müssen sauber migriert werden. Neue einmalige Gebäude, XP und Forschungsboni dürfen bei Regierungsrückkehr nicht wiederholt werden. Zusammenarbeit bleibt eine tatsächliche Entscheidung des Empfängers.

**Prüfgrenzen:** Das ist ein Quell-/Designaudit, kein neues HOI4-, Hover-, Save-Load- oder Mehrspielerergebnis. Die 103 Irak-/US-eigenen Ausgaben entsprechen dem letzten Manifest. Sechs gemeinsam genutzte Integrationsdateien wurden seitdem durch andere Arbeit verändert; sie wurden nicht zurückgesetzt und sind kein Teil einer neuen Startzertifizierung. Der [Quell-Snapshot](AUDIT_SOURCE_SNAPSHOT.json) und die [Browserprüfung](AUDIT_BROWSER_REPORT.json) grenzen das tatsächliche Prüfungsergebnis ein.
