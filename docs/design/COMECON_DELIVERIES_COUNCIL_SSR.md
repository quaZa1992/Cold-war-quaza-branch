IMPERIA COLD WAR: Deliveries, Host Selection, Council and Soviet Republics
========================================================================

Statuskorrektur nach dem jüngsten Nutzerwunsch: [Shared Production Revision](COMECON_SHARED_PRODUCTION_REVISION.md) ersetzt den normalen Rücklieferungsablauf durch automatische Produktionsboni für die anderen zahlenden Teilnehmer. Die früheren einzeln abrufbaren Bauunterstützungs-/Lieferpakete unten bleiben eine verworfene Standardvariante beziehungsweise mögliche spätere Spezialvorlage. Hostwahl, ausdrückliche Zustimmung, ein sowjetischer Sitz und die Performance-Anforderungen bleiben erhalten.

Stand: 24. Oktober 2026. Weiterentwicklung des angeforderten RGW-Konzepts. Keine Laufzeitimplementierung und kein Nachweis nativer Multiplayer-Stabilität. Diese Ergänzung konkretisiert die Rücklieferungsalternative zu Geldtilgung und die ausdrücklich gewünschte sowjetische Vertretung.

## 1. Historischer Ausgangspunkt

Die Sowjetunion war als Gesamtstaat Mitglied des RGW. Die Charta nennt sie als Vertragspartei neben den anderen Mitgliedstaaten; einzelne Sowjetrepubliken erscheinen dort nicht als zusätzliche RGW-Mitglieder. [Charta von 1959, UN Treaty Series 368, Nr. 5245](https://treaties.un.org/doc/Publication/UNTS/Volume%20368/volume-368-I-5245-English.pdf)

Die Ukrainische SSR und die Belarussische SSR behalten jeweils ihren eigenen Sitz und ihr eigenes Stimmrecht in der UN-Generalversammlung zusätzlich zum Sitz der UdSSR. Beide waren UN-Gründungsmitglieder von 1945. Der 1970-Laufzeitcode enthält `UKR` und `BLR` bereits als eigene UN-Mitglieder, auch bei fortbestehendem sowjetischem Untertanenstatus. Diese historische UN-Ausnahme erzeugt keine zusätzlichen RGW-Delegationen und keine ständigen Sicherheitsratssitze oder Vetorechte. Die Aussagen über genau eine sowjetische Stimme in diesem Konzept beziehen sich auf den RGW-Rat. [UN-Liste der Gründungsmitglieder](https://research.un.org/en/unmembers/founders)

Das ist der historische Grund für genau eine sowjetische Delegation. Standorte, Betriebe und regionale Durchführung innerhalb der Union bleiben möglich. Als späteres Beispiel nennt die UNIDO gemeinsame Vorhaben auf sowjetischem Territorium, darunter das Kernkraftwerk Chmelnyzkyj. Die Einordnung als Projekt der UdSSR bleibt von seiner Lage innerhalb einer bestimmten Republik zu unterscheiden. [UNIDO 1984, gedruckte S. 12](https://downloads.unido.org/ot/47/94/4794479/10001-15000_13995.pdf)

Die historische Quelle beschreibt Beiträge und Gegenlieferungen als vertraglich vereinbarte Leistungen. Ein Baubonus ist unsere Spielabstraktion für bestimmte Maschinen-, Material- und Betreuungsleistungen. Er ist keine historische RGW-Währung und keine universelle Gegenleistung für beliebige Investitionen.

## 2. Drei Rollen, die nicht verwechselt werden dürfen

| Rolle | Entscheidung und Ergebnis |
|---|---|
| Council Representative | Unterzeichnet und stimmt als tatsächliches RGW-Mitglied ab |
| Host / Asset Recipient | Besitzt und kontrolliert den vereinbarten Standort, erhält die konkreten Anlagen |
| Delivery Recipient | Erhält vereinbarte Rücklieferungen oder ein befristetes geeignetes Leistungsprogramm |

Für ein Vorhaben in der ukrainischen SSR lautet die Anzeige deshalb beispielsweise **Council Representative: Soviet Union**, **Host: Ukrainian SSR**. Die SSR erhält keine zusätzliche Stimme. Dieselbe Unionsforderung wird nicht bei der Union und allen Republiken dupliziert.

Eine gesondert spielbare SSR kann Projekte empfangen, bei passenden Voraussetzungen Anlagen beherbergen und einen vom Unionsanteil zugewiesenen Lieferanspruch nutzen. Die Union legt diese Zuweisung ausdrücklich fest. Die Unterverteilung zieht den Betrag vom verfügbaren Unionsanspruch ab. Weder der SSR-Tag noch sein bloßer Status erzeugen einen weiteren Zuschuss, Grundanspruch oder Einflussanteil.

Kosten und Pflichten eines menschlich gespielten Empfängers brauchen dessen eigene Zustimmung. Dafür dient eine **Local Implementation Agreement**. Dies ist eine bewusst gewählte Multiplayer-RP-Regel, keine Behauptung über ein historisches außenpolitisches Vetorecht der SSR. Die lokale Zustimmung wird nicht im Ratsquorum gezählt. Eine Republik, die nur einen vom Geber finanzierten Vorteil erhält, wird nicht durch ihre bloße Auswahl heimlich belastet.

Der aktuelle Mod kennt den tatsächlichen Status `autonomy_soviet_republic_1985`. Dieser Status und der aktuelle Unionszusammenhang sind die Ausgangspunkte für die technische SSR-Erkennung, nicht ausschließlich eine starre Liste von Ländernamen oder Farben. Ein Austritt oder eine Unabhängigkeit verleiht nicht automatisch RGW-Mitgliedschaft oder eine Ratsstimme. Bestehende Anlagen, Lieferungen und Verbindlichkeiten sind dann getrennt zu prüfen.

Bestehende interne Wirtschaftsregeln werden nicht still überschrieben: Der untersuchte SSR-Status enthält unter anderem `cic_to_overlord_factor = 0.25`. Vier im SSR-Territorium errichtete Fabrikstufen sind daher von der tatsächlich frei verfügbaren SSR-Baukapazität zu unterscheiden. Die vorhandene Aufteilung mit der Union, Arbeitskräfte und weitere native Bedingungen bleiben wirksam. Das tatsächliche Eigentum und die Kontrolle des Standortstaates sind bei einem Bau in einer separat repräsentierten SSR zu prüfen.

## 3. Welche Rücklieferung welchen Effekt rechtfertigt

| Projekt / gelieferte Leistung | Passende Spielwirkung |
|---|---|
| Maschinen und technische Betreuung für den Industriebau | Zeitweiliger Bonus ausschließlich auf den Bau von Zivilfabriken |
| Baugeräte und Materialien für Verkehrsvorhaben | Zeitweiliger Infrastruktur-Baugeschwindigkeitsbonus |
| Landwirtschaftliche Bau- und Ausrüstungspakete | Zeitweiliger Bonus auf den Bau von Agrarbezirken |
| Energieanlage | Tatsächlich verfügbare Stromlieferung aus dem Energiesystem |
| Rohstoffprojekt | Tatsächliche Rohstofflieferung oder ein vertraglicher Erlös-/Abnahmeanspruch |
| Abgegrenztes Entwicklungsprogramm | Begrenzter Forschungsbonus in einer tatsächlich verwendeten Kategorie |

Es gibt keinen allgemeinen Knopf, der Gaslieferungen in beliebige Armeeboni umwandelt. Jede Vorlage enthält eine begrenzte Liste zulässiger Leistungen.

Für den Industriefall stehen die drei vorher bepreisten Intensitäten **+5%, +10% oder +15% Civilian Industry Construction Speed** zur Wahl. Derselbe Anspruch reicht bei höherer Intensität kürzer. Die nativen Modifikatoren verändern die Geschwindigkeit des jeweiligen Gebäudetyps landesweit. Eine Beschränkung auf nur einen fremdfinanzierten Bauauftrag ist damit nicht automatisch gegeben. Dieser breite Geltungsbereich muss in der Beschreibung und Bewertung stehen.

Die nativen Leser sind nachgewiesen: `get_building_construction_values` in `common/scripted_effects/99_investment_scripted_effects.txt` liest unter anderem `production_speed_industrial_complex_factor`, `production_speed_infrastructure_factor` und `production_speed_agriculture_district_factor`. Bestehende MD-Ideen verwenden den Zivilindustrie-Baueffekt ebenfalls.

## 4. Ein begrenzter Anspruch statt eines ewigen Bonus

Bezahlt ein Land einen rücklieferungsfähigen Beitrag, wird dessen tatsächlicher Betrag im Vertrag vermerkt. Die spätere Gegenleistung mindert genau diesen Anspruch. Zuschüsse erzeugen keine Forderung. Noch nicht bezahlte Zusagen erzeugen ebenfalls keine abrufbare Leistung.

Für ein Bedienbeispiel kann ein fest bewertetes **13-week supply package** verwendet werden. Es steht für Maschinen, Ersatzteile und technische Betreuung während eines Bauabschnitts. Ein +10%-Paket benötigt doppelt so viel vereinbarte Lieferleistung wie ein +5%-Paket; ein +15%-Paket dreimal so viel. Das ist eine vorgeschlagene lineare Preisregel, keine native Produktionsformel.

Rechenbeispiel auf Basis des bisherigen großen Industrieprojekts: Die DDR finanziert 20% von 74.880 Milliarden, also 14.976 Milliarden. Ein für diesen Vertrag bewerteter Grundbaustein kostet im Beispiel 0.936 Milliarden und unterstützt +5% Zivilindustrie-Baugeschwindigkeit für 13 aktive Wochen. Damit reichen die 16 Grundbausteine wahlweise für **+5% über 208 aktive Wochen** oder **+10% über 104 aktive Wochen**. Eine +15%-Variante verwendet volle Blöcke und lässt einen Restanspruch, der sichtbar erhalten bleibt. Dieser Anspruch wird nicht zusätzlich noch einmal vollständig in Geld getilgt.

Der Paketpreis von 0.936 Milliarden dient nur diesem Bedienbeispiel. Vor einer Umsetzung muss der Angebotspreis die Reichweite im Empfängerland berücksichtigen, beispielsweise den bei Angebotsabschluss festgestellten Umfang seines relevanten Bausektors. Derselbe prozentuale landesweite Bonus hat in einer sehr großen und einer kleinen Volkswirtschaft unterschiedliche Wirkungen. Vergleichspreise werden beim Angebot festgelegt; eine spätere Vergrößerung der Empfängerwirtschaft darf nicht unbemerkt unbegrenzte Leistungen aus einem alten kleinen Paket erzeugen. Größere Reichweiten benötigen neu bepreiste Folgepakete.

Lieferansprüche beginnen grundsätzlich erst mit der tatsächlichen Inbetriebnahme der produzierenden Anlage. Technische Hilfe vor Fertigstellung ist nur als eigenes vorhandenes und finanziertes Vorleistungsprogramm möglich. Ein Projekt finanziert nicht durch seinen erst zukünftigen Produktionsbonus kostenlos seinen eigenen Bau.

## 5. Der Lieferant muss wirklich etwas leisten

Die neue Anlage darf nicht gleichzeitig uneingeschränkt die nationale Bauwirtschaft bedienen und unbegrenzte kostenlose Exportprogramme erzeugen. Für eine erste Umsetzung kann ein vereinbarter Teil ziviler Kapazität während der Lieferphase gebunden werden. Der vorhandene native Modifikator `civilian_factory_use` wird in MD-Entscheidungen und bestehenden Projektideen verwendet. Seine genaue Wechselwirkung mit der aktuellen MD-Ökonomie braucht einen Spieltest.

Als vorgeschlagene Startkalibrierung für einen großen Maschinenkomplex werden **2 zivile Fabrikkapazitäten** für die laufenden Lieferprogramme gebunden und **0.020 Milliarden pro Woche** als Betriebs-/Betreuungsbudget ausgewiesen. Diese Zahlen sind Entwurf. Die Bindung setzt verfügbare Kapazität voraus und kann nicht zweimal für zwei gleichzeitig angebotene Exportprogramme verwendet werden.

Die Projektvorlage begrenzt zudem die gleichzeitig bedienbaren Lieferpakete. Aufträge erhalten eine vorab vereinbarte Reihenfolge oder Kapazitätsquote. Umfang und Reichweite der Empfängerpakete müssen zu dieser Kapazität passen. Alle Zahlungen, die Kapitalbindung und der begrenzte Lieferplan stehen vor der Unterschrift fest. Eine reine hohe Restforderung beweist keine sofortige Lieferfähigkeit.

Fehlen Standortkontrolle, erforderliche Energie, Kapazität oder der zulässige Handelsweg, wird die betroffene Dienstleistung ausgesetzt. Für nicht erbrachte Wochen werden kein Lieferanspruch getilgt und kein laufender Unterstützungsbonus gewährt. Verbleibende aktive Wochen und Forderungen bleiben erhalten. Bereits abgeschlossene Gebäude und tatsächlich entstandene Produktivitätszuwächse werden nicht rückwirkend entfernt. Wiederaufnahme vergibt weder eine zweite Anlage noch einen neuen Anfangsanspruch.

Für das erste Spielmodell ist eine gemeinsame Wochenabrechnung maßgeblich. Bedeutende Zustandswechsel können Leistungen früher deaktivieren, falls das native Ereignis verfügbar ist. Andernfalls beträgt die Reaktionsgrenze höchstens ein Abrechnungsintervall; eine behauptete sofortige Reaktion ohne entsprechenden Hook wäre falsch.

## 6. Host-Auswahl und Abstimmung

1. Ein Mitglied erstellt eine Projektvorlage und schlägt Host, konkrete geeignete Staaten, Bauumfang, Finanzierung und Gegenleistungen vor.
2. Das vorgeschlagene Standortland nimmt die lokale Durchführung an. Bei einem SSR-Standort unterzeichnet die Sowjetunion außenpolitisch; eine notwendige lokale Kosten-/Durchführungszustimmung bleibt getrennt.
3. Die betroffenen Mitgliedsdelegationen stimmen der identischen Vertragsfassung zu. Bei normalen Projekten zählt der Konsens der verpflichteten beziehungsweise unmittelbar betroffenen Mitgliedstaaten. Ein nicht beteiligtes Mitglied erzeugt keine fremde Zahlungsverpflichtung und blockiert kein unabhängiges Vorhaben durch bloßes Desinteresse.
4. Noch offene oder abgelehnte Verpflichtungen verhindern den Start. Eine Mehrheit darf einem ablehnenden Finanzier nicht trotzdem Geld abziehen. Änderungen verlangen eine neue, genau bezeichnete Vertragsfassung und neue Zustimmung der betroffenen Parteien.
5. Erst bei gültigem Standort, gedeckter Finanzierung und allen erforderlichen Zustimmungen wird das Projekt zur Ausführung freigegeben.

Die offizielle Wahlberechtigung wird im Klick-Effekt nochmals geprüft. Ausgeblendete SSR-Knöpfe allein sind keine Absicherung. Ein gestandener SSR-Status ist weder zusätzliche Mitgliedschaft noch ein Ersatz für die tatsächliche Staatsvertretung.

## 7. Oberfläche im Factions-Stil

Der bestehende Hauptfenster-Donor besitzt 550 Einheiten Breite; seine Zielkarten und Tabs dienen als Referenz. Der Forschungsdonor besitzt ein seitliches Fenster mit 450 Einheiten Breite. Eine spätere Umsetzung muss die vollständigen Fenster mit ihren Nachbarn und Listen prüfen. Eine ähnliche HTML-Darstellung ist kein nativer Funktionstest.

Die vier Detailansichten heißen **Project**, **Funding**, **Council** und **Returns**:

- Project: Host auswählen, sowjetische Vertretung von SSR-Standorten anzeigen, Bauort, Umfang und lokale Durchführung prüfen.
- Funding: Angebote der Länder, Wochenzahlungen, Eigenanteil, gesamte Deckung und tatsächliche Einzahlungen.
- Council: nur echte Mitgliedsdelegationen, angenommene Vertragsfassung und erforderliche lokale Zustimmung getrennt anzeigen.
- Returns: Empfänger, Gebäudetyp, Intensität, aktive Dauer, offener Anspruch, vereinbarter Paketpreis, Lieferstatus und Kosten des Produzenten.

Eine SSR sieht ihre Anlagen und zugewiesenen Leistungen. Im Ratsbereich steht ihre sowjetische Vertretung. Sie bekommt keine eigene offizielle Wahlzeile. In einer konzeptionellen Vorschau darf man Länderansichten wechseln; im echten Multiplayer bestimmt das tatsächlich kontrollierte Land die verfügbaren Aktionen.

## 8. Performance und Multiplayer

Ein zentraler autoritativer Wochenlauf verarbeitet nur die aktiven Projekte, ihre Teilnehmer und gegebenenfalls aktuell laufenden Lieferpakete. Er läuft nicht erneut für jeden Spieler, der das Fenster öffnet. Ein gespeicherter Abrechnungszeitraum und Einmalbelege schützen vor Wiederholung bei Save/Reload oder Rehost. Native Hooks und tatsächlicher Länderkontext sind bei Implementierung zu prüfen.

Der Dispatcher benötigt genau einen gültigen Spielkontext und eine festgelegte Ersatzregel, falls sein Koordinator ausfällt. Ein pro Land ausgelöster Hook darf nicht denselben globalen Vertrag mehrfach abrechnen. Spielzeit und gespeicherte Vertragsfassung sind maßgeblich; lokale Rechnerzeit und Client-Ansicht sind keine Abrechnungsgrundlage. Gleichzeitige Aktionen werden gegen die aktuelle autoritative Fassung geprüft. Diese Voraussetzungen sind Entwurfsanforderungen, keine Behauptung über bereits vorhandenen Code.

Mitglieds-, Teilnehmer-, Kandidaten- und Wahlberechtigungslisten werden bei Änderungen aufgebaut und ansonsten wiederverwendet. Die UI berechnet keine Weltstatistik in ihren Properties und bindet ihre Dirty-Variable nicht an jeden Tageswechsel. Finanzierungsangebote, Stimmabgaben, Standortwechsel und Abrechnungsergebnisse erhöhen gezielt den zuständigen Änderungszähler, auch wenn die Änderung von einer KI oder einem anderen Land stammt.

Zustand: Projekt-ID, Vertragsfassung, Vertretung, Host/Empfänger, Teilnehmer, Angebote, bezahlte Beträge, offene Ansprüche, lokale Zustimmungen, Stimmen und nächste Abrechnung. Anzeigezustand und Tooltipvorschau bleiben wirkungslos. Wiederholte Klicks auf dieselbe Fassung sind idempotent. Nach einer wesentlichen Vertragsänderung zählen alte Zustimmungen nicht als Annahme der neuen Bedingungen.

Die Laufzeit der Kernabrechnung wächst mit der Summe tatsächlich aktiver Teilnehmer und Lieferpakete. Die erste Fassung kann beispielsweise 12 aktive Projekte mit höchstens 8 offiziellen Mitgliedsdelegationen je Projekt vorsehen und Listen seitenweise anzeigen. Diese Kapazitätszahlen sind vorläufige Grenzen der Umsetzung, keine historische Regel. SSR-Empfänger sind Untereinträge und erzeugen keine weiteren Ratsstimmen. Abgeschlossene Verträge werden kompakt archiviert, nicht auf Dauer im Wochenlauf mitgerechnet.

Es wurden keine Millisekunden, FPS oder Desync-Raten gemessen. Sinnvolle Nachweise sind ein nativer GUI-Prototyp sowie ein Mehrspieler-Test mit gleichzeitigen Stimmen, SSR-Empfängern, geänderten Angeboten, Pause/Restore und Save/Rehost. Source- und Modellentests können diese Nachweise vorbereiten, nicht ersetzen.

## 9. Quellen und Provenienz

Eigenständiger Entwurf für IMPERIA COLD WAR. Historische Quellen sind die oben verlinkte RGW-Charta und die UNIDO-Studie von 1984. Die SSR-Stimmregel folgt der Mitgliedschaft der UdSSR; die lokale Zustimmungsregel für separat gespielte SSRs ist eine ausdrücklich ausgewiesene RP-Anpassung. Die Paketpreise, Kapazitätsbindung und Modifikatoren sind Spielvorschläge.

Lokale technische Referenzen: `interface/factions/countryfactionview.gui`, `interface/factions/faction_research.gui`, `common/scripted_guis/01_european_union_guis.txt`, `common/autonomous_states/99_1985_soviet_republic_autonomies.txt`, `common/scripted_triggers/COLDWAR_SSR_intelligence.txt`, `common/scripted_effects/99_investment_scripted_effects.txt`, `common/decisions/05_bulgaria.txt` und `common/ideas/COLDWAR_UNI_1970_ideas.txt`. Native Systeme: Paradox Interactive; Modsysteme: MD-Team und jeweilige Projektbeitragende. Einzelautorenschaft und genaue Lizenz jeder lokalen Anpassung sind nicht vollständig verifiziert und bleiben unbekannt. Es wurde kein fremdes Bildmaterial kopiert.
