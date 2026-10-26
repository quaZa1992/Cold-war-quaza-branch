# Wirtschafts-, Gesellschafts- und gemeinsame Entwicklungsprogramme: Belohnungsvielfalt

Lesender Audit vom19.10.2026. Keine Spieländerung und kein Generatorlauf. Gegenstand sind140aktive Foki aus oil,industry,agriculture,society,defence,foreign,war undiran_war. Quelle für aktuelle Werte: `current_design.json` **modifiers/building/instant/army_xp**, gegengeprüft an den geladenen Rewards und Programme-Verbrauchern. Veraltete `reward_summary`, `effect_code` und `available`-Katalogtexte sind keine Ist-Belege. Die20maschinenlesbaren Änderungsvorschläge stehen in `ECONOMIC_PROPOSALS.json`; die Abschnitte hier fassen sie zu14bewertbaren Entscheidungen zusammen.

## Befund und Größenordnung

57der140Foki enthalten Bürokratie,56davon als Mehrkosten. Das ist nicht allein eine Frage zu hoher Zahlen: verschiedene Tätigkeiten erhalten dieselbe Bezahlung und dieselbe Strafzeile.

| Identisches aktuelles Paket | Foki |
|---|---|
| Nur+2%Bürokratie,keinGDP-Preis | foreign_dossier,agri_land_survey,war_contingency |
| +2%Steuer,+2%Bürokratie,keinGDP-Preis | oil_accounts,oil_sovereignty |
| +3%Fabrikeffizienzwachstum,+2%Bürokratie,1%GDP | industry_public_accounts,defence_procurement_board |
| +2%Agri,+2%Bürokratie,1%GDP | agri_water_accounts,agri_water_inspection |
| +2%Steuer,+2%Bürokratie,0.5%GDP | society_budget_review,war_accounts |

Gleiche Statzeilen beweisen keinen gleichen Gesamtnutzen. **Land Survey schaltet mittlerweile tatsächlich den Rural-Priority-Review frei.** **Field Maintenance entfernt auf dem nationalisierten Weg zusätzlich die verbleibenden−6%IPC-Exportlast.** Solche Leistungen müssen beim Kürzen erhalten bleiben. Insbesondere ist der Footer `reconcile_situations` nicht automatisch eine zusätzliche Belohnung: nur ein nachgewiesener Consumer des betreffenden Flags zählt.

Die laufende Bürokratieformel lautet Population ×(1+Summe der Bürokratiemodifier)×nativer Kostensatz×gewählte Haushaltsstufe (`common/scripted_effects/00_money_system.txt:3309`). +52%heißt52%mehr **auf dieser einen Ausgabenzeile**, nicht52%desGDP und nicht52%mehr Gesamtausgaben. Der Compiler summiert alle kompatiblen Beiträge; ein Bürokratiecap existiert hier nicht. Positive **Programme**-Stabilität ist hingegen auf insgesamt15Punkte begrenzt (`tools/iraq_1970/compile.py:206`).

## Vierzehn konkrete Empfehlungen

Alle Zahlen rechts sind **Balancevorschläge**, keine historische Messung. Jeder Vorschlag ersetzt den alten Payload, sofern ausdrücklich nichts anderes steht. Einmalige Anlagen, Ressourcen und Forschung bleiben dauerhaft erhalten; Programmeffekte folgen der vorhandenen Auswahl-/Governmentlogik. Keine kostenlose Wiederholung nach Regierungswechsel oder bezahlter Prioritätsrevision.

1. **Foreign Dossier entfernen; keine Ersatzprämie erfinden.** Aktuell21Tage und ausschließlich+2%Bürokratie. Die geladenen Rewards setzen nur earned/implemented und rufen allgemeine Rekonzilierer auf (`rewards.txt:5444`). Das Flag dient nachfolgenden Foki, nicht einer eigenständigen Verhandlungsmechanik. Treaty Partner/Non-Alignment werden gleichberechtigte Einstiege mit ihren bisherigen35Tagen.

2. **Treaty Register in die zwei Angebotswege zusammenlegen.** Aktuell35Tage,0.5%GDP,+1%Bürokratie, keine zusätzliche Vertragswirkung (`rewards.txt:5567`). Vorschlag: Partner Treaty49Tage/0.5%GDP; Open Cooperation49Tage/1.5%GDP, jeweils einschließlich bisherigem Registerpreis. Register-Bürokratie entfällt. Open Cooperation hat aktuell selbst keinen Decision-Unlock und sein+4%Same-Outlook-Opinion hilft gerade nicht speziell bei unterschiedlichen Blöcken. Derselbe vorhandene empfängerbestätigte zivile Vertragskanal sollte daher auf beiden Wegen erreichbar sein; keine automatisch erzwungenen Partner. Weitere Vertragsgebühren bleiben unverändert.

3. **War Contingency mit der tatsächlichen militärischen Wahl zusammenlegen.** Aktuell21Tage/+2%Bürokratie, keine eigenständige Kriegswirkung (`rewards.txt:11913`). Armed Restraint/Offensive Option behalten35Tage und ihre unterschiedlichen Verteidigungs-/Angriffs- und Personalkosten. Kein neues Gratis-XP als Entschädigung für entfernte Büroarbeit.

4. **Civil Crisis Authority in die Notstandshaushalte aufnehmen.** Aktuell35Tage/1%GDP/+2%Bürokratie ohne tatsächliche Zivilschutzleistung (`rewards.txt:12037`). War Economy und Civilian Budget Floor tragen stattdessen jeweils einmalig1%GDP bei35Tagen. Der zusätzliche Vorgänger und seine+2%Bürokratie entfallen. Die existierenden Gegensätze+5%Militärausstoß/+4%relativeCG/+6%Personal gegenüber zivilem Budget/−3%Militärausstoß/+3%Sozialausgaben bleiben erhalten. Reale Notstandsbedingungen nicht in bloße Textbehauptungen verwandeln.

5. **Campaign Ledger und Long War als reine Zugangsarbeit kürzen.** Ledger21Tage/0.5%GDP führt nach Bezahlung nur Metadaten aus (`rewards.txt:12969`); Gulf-Kredite entstehen durch andere echte Kriegs-/Kreditconsumer. Nachfolger erhalten weiterhin `iran_first_war_seen` und Launch-Campaign/Home-Front-Prerequisites. Long War21Tage ist ebenfalls leer, hat aber eine wichtige echte Bedingung: laufender Krieg mitPER seit mindestens90Tagen (`rewards.txt:13049`). Diese Bedingung gehört in die nachfolgenden Reserve-/Offensivpakete. Keine weichere Uhr und keine Belohnung dafür, einen aussichtslosen Krieg absichtlich zu verlängern.

6. **Provincial Settlement mit der Integrationswahl zusammenlegen.** Aktuell49Tage/2%GDP/+2%Bürokratie/−2%PP (`rewards.txt:13286`). Eigentum+Kontrolle399 und Frieden mitIran bleiben auf beiden verbleibenden49-Tage-Wegen. Der2%-Preis wird in die Angebote verlagert: Equal Citizenship6%GDP mit bisher12Compliance/+6%Bürokratie/+4%Sozial; Central State Rule4.5%GDP mit bisher6Compliance/+3%Bürokratie/+8%Driftverteidigung/−3Stabilität. Der reine zusätzliche+2%Büro-/−2%PP-Aufschlag entfällt. Core-Endfokus70Tage/6%GDP und dessen eigenen Bedingungen unverändert. **Das ist ausdrücklich alternatives Eroberungs-/Integrationsspiel, keine Behauptung historischer irakischer VerwaltungKhuzestans.**

7. **Oil Sovereignty nicht zum zweiten Oil Accounts machen.** Finale49Tage/+2%Steuer/+2%Bürokratie ist eine Wiederholung (`programmes.txt:6242`). Seine Schlussfunktion kann ohne zusätzliche Zahlen in Field Maintenance/Contract Review aufgehen. Sowohl+2%Steuer als auch+2%Bürokratie entfallen. Das kürzt Inflation auf beiden Seiten; keine pauschale Landesverbesserung.

8. **Field Maintenance seinen wirklichen technischen Fortschritt lassen.** Aktuell35Tage/2%GDP,+3%Export/+2%Bürokratie **plus** Entfernung der letzten−6%IPC-Last nach State Company (`situations.txt:46–51`, `rewards.txt:9225`). Diesen materiellen Institutionsfortschritt erhalten; den zusätzlichen Export-/Bürokratie-Payload entfernen. Keine zusätzlichen statischenÖlressourcen erfinden: bessere Nutzbarkeit bereits vorhandener Förderung ist schon durch die echteIPC-Entlastung vertreten. Das Projekt erhält ausdrücklich State Company als Voraussetzung; der Konzessionsweg darf ohne dieses nationalisierte Nebenprojekt abgeschlossen werden und verliert nicht seinen vereinbarten fremden Anteil. Der separate Kirkuk-Survey4Öl bleibt unverändert.

9. **Grid Management an den Energiehaushalt anschließen.** Aktuell35Tage/1%GDP,+2%Bauen/+2%Bürokratie (`programmes.txt:6428`). Vorschlag+2%Bauen behalten, Bürokratie durch−5%relativen Brennstoffverbrauch fossiler Kraftwerke ersetzen. Das verbessert vorhandene Anlagen, erzeugt selbst keinen Strom und erhöht weder Forschung noch allgemeinesGDP. Main-MD-Irak verwendet genau−5%in `IRQ_strategic_partnerships` (`common/ideas/Iraqi.txt:1707`).

10. **Die zwei Wasserabrechnungen zu einer echten Wasserbehörde machen.** Accounts und Inspectorate kosten aktuell zusammen70Tage/2%GDP für+4%Agri/+4%Bürokratie (`programmes.txt:6553`,`:6678`). Inspectorate als überlebendes Paket:35Tage/1.5%GDP,+4%Agri/+2%Bürokratie; Accounts als eigener Fokus entfällt. Frühe Bewässerungswahl direkt an die Kreditwege anbinden, den späteren Wasser-Talks-Zweig nicht in einen erzwungenen ausländischen Vertrag umwandeln. Die eigenen Wasserregeln und tatsächliche Partnerzustimmung bleiben gesondert.

11. **Großbewässerung gegen lokale Erschließung als vollständige Investitionswahl.** Large aktuell35Tage/4%GDP,+5%Agri/+2%relativeCG; Local35Tage/2.5%GDP,+4%Agri/+3%Bürokratie und optional echtes Dhi-Qar-Folgeprojekt49Tage/2.5%GDP/1Agrardistrikt (`programmes.txt:6565`,`:6583`). Vorschlag Large49Tage/4%GDP,+8%Agri/+2%relativeCG und1Infrastruktur1141; Local35Tage/2.5%GDP,+4%Agri/+1%Sozialausgaben, danach **bestehendes** Dhi-Qar-Projekt unverändert. Large kauft stärkere landesweite Produktivität und Infrastruktur, Local früheren Zugang zu neuem Agrarland. Beide brauchen keinen zusätzlichen generischen Beamtenmalus. Keine zweite kostenlose Landwirtschaftsanlage im Large-Paket.

12. **Universal/Targeted über vollständige Folgewirkungen unterscheiden.** Aktuell Universal+4Stabilität/+6%Sozial, Targeted+2Stabilität/+3%Sozial/+2%Bürokratie (`programmes.txt:6822`,`:6840`). Beide35Tage ohneGDP-Gebühr. Vorschlag Universal ersetzt Stabilität durch `productivity_growth_modifier=0.03`, erhält+6%Sozialkosten; Primary Care35Tage/2.5%GDP ersetzt seine weiteren+2Stabilität/+3%Sozial durch−5%echte Gesundheitsbetriebskosten. Targeted ersetzt Stabilität durch−2%relativeCG, erhält+3%Sozial/+2%Bürokratie für tatsächliche Bedürftigkeitsprüfung. Priority Districts35Tage erhöht den Preis1.5→2.5%GDP und ersetzt+2Stabilität/+2%Bürokratie durch1Infrastruktur166. Langfristige nationale Leistungsfähigkeit gegen schnell nutzbare Provinzkapazität; beide Wege haben echte, unterschiedliche Preise. Es wird kein Gesundheitsgesetz übergangen und keine Bevölkerung aus dem Nichts erzeugt.

13. **Science Maintenance begrenzen und fachlich zuordnen.** Aktuell35Tage/2%GDP,+2%Globalforschung/+2%Bürokratie nach Teacher First+5%Globalforschung (`programmes.txt:6972`). Vorschlag2×25%CAT_electronics und+1%Bildungsausgaben. Damit bleiben Colleges' Bau-/Industrieboni eigenständig, und die Wissenschaft erzeugt nicht unbegrenzt stapelbare Globalforschung. Electronics hat reale frühe Technologietreffer; ein Genetikbonus wäre hier1970schwach, denn native genetics_1 beginnt erst1985.

14. **Maintenance Manuals soll Wartung und Bedienung belohnen.** Aktuell35Tage/2%GDP,+3%Fabrikeffizienzwachstum/+2%Bürokratie auf dem Mixed-Supplier-Weg (`programmes.txt:7141`). Vorschlag1×35%CAT_infantry,−3%Attrition,+2%Armeeausbildungszeit; generische Effizienz-/Bürokratiezeilen entfallen. Mixed Supply behält seinen tatsächlichen+3%Versorgungsverbrauch; Soviet Standard−10%Versorgungsverbrauch und anders geartete Einflussabhängigkeit bleibt ein klarer Gegenweg. Keine neuenOrg-/Recovery-Boni, keine spontanen kostenlosen Waffen. Vorbild für Fähigkeit mit eigener Ausbildungsfolge: Main-MD-Deutschland `GER_Specialized_Indantry` verwendet−5%Attrition,+5%Hitze-/Kälteakklimatisation,+10%Ausbildungszeit (`05_germany.txt:6994`).

Zusätzlich kleiner, ausdrücklich **nicht** leerer Einstieg: Land Survey besitzt den Rural-Priority-Review-Unlock. Falls sein Tempo stört,21→14Tage und+2%Bürokratie entfernen, den bestehenden1%GDP/75PP/180-Tage-Review selbst erhalten. Diese optionale Tempoänderung ist nicht in den20JSON-Records und den primären Summen unten eingerechnet.

## Ganze kompatible Routen statt Summen aller Alternativen

Die folgenden Routen enthalten **alle** kompatiblen Seitenprojekte der vier genannten Kapitel, jedoch keine Parteiprogramme, Regierungssprünge, fremden Verträge oder Kriegsboni. Januar1970-Irak bleibt im selben Staat und kann in Frieden alle heimischen Zielstaaten besitzen/kontrollieren; erforderliche Baukapazität und Finanzierung sind ausdrücklich angenommen. Prerequisite-Gruppen und Exclusions wurden für beide Knotenlisten direkt gegen die aktuellen Daten geprüft. Jahre des Fokusfortschritts und laufende Kosten lassen sich nicht als eine einzige sofort zahlbare Jahresrechnung ausgeben.

**Route A: nationale Ölrente, zivile Industriebasis, Kooperativen mit lokaler Erschließung, Teacher First mit gezielten Diensten.** Auswahl: oil_nationalize+oil_revenue_state; industry_light+industry_public_finance; agri_cooperatives+agri_local_irrigation; society_teacher_first+society_targeted_services. Enthalten sind auch Dhi Qar, alle drei ländlichen Reform-Meilensteine, Stromwerk, Offices, Housing und Colleges.47Foki/1729Fokustage.

**Route B: nationale Diversifizierung, Grundindustrie, Kooperativen mit Großbewässerung, Massenalphabetisierung mit universellen Diensten.** Auswahl: oil_nationalize+oil_diversification; industry_heavy+industry_public_finance; agri_cooperatives+agri_large_irrigation; society_mass_literacy+society_universal_services. Dhi Qar und Priority Districts liegen hier auf den ungewählten Ästen und zählen nicht.46Foki/1680Fokustage.

| Aktive Kapitelbeiträge, vor anderen Ideen/Gesetzen | A aktuell | A Vorschlag | B aktuell | B Vorschlag |
|---|---:|---:|---:|---:|
| Bürokratieausgabenmodifier | +52% | **+37%** | +43% | **+33%** |
| davon Öl/Industrie/Agrar/Gesellschaft |14/10/18/10%|10/8/13/6%|14/8/15/6%|10/6/13/4%|
| Sozialausgabenmodifier |+16%|+17%|+22%|+19%|
| Allgemeine Steuergewinnmodifier |+10%|+8%|+13%|+11%|
| Ölexportmodifier |+28%|+25%|+7%|+4%|
| Landwirtschaftsproduktivitätsmodifier |+23%|+23%|+24%|+27%|
| Globalforschung |+7%|+5%|+2%|0%|
| Positive Programme-Stabilität, ungecappt |+6Punkte|+2Punkte|+8Punkte|+2Punkte|
| Relative Consumer-Goods-Faktoren |+1%|−1%|+5%|+5%|
| Native Produktivitätswachstumsparameter |0|0|0|+.03|
| Fossile Kraftwerks-Brennstoffkosten |0|−5%|0|−5%|
| Gesundheitskosten |0|0|0|−5%|
| Bildungskosten aus neuem Laborbetrieb |0|+1%|0|+1%|
| Fokustage der jeweiligen vollständigen Route |1729|1645|1680|1610|
| Summe deklarierter GDP-Invoice-Anteile* |87.5%|88%|89%|88.5%|

\*Die letzte Zeile ist nur die Summe der Kataloganteile über mehrere Jahre. Sie entspricht tatsächlichen addierten Rechnungen **ausschließlich**, falls jeder Fokus bei demselbenGDP zitiert würde. Kein Cashflow-Forecast, kein Anteil eines einzelnen realen Haushaltsjahrs. Tatsächliche Preise frieren pro Auftrag zu dessen Quotezeit ein.

Die Vorschläge senken also nicht einfach jede negative Zahl: Route A verliert2%Allgemeinsteuer,3%Export,2%Globalforschung und4Stabilitätspunkte; sie bezahlt zusätzlich1%GDP für einen realenDistriktausbau und trägt je1%zusätzliche Sozial- bzw.Bildungskosten. Dafür bekommt sie weniger dauernde Behördenlast, eine weitere echteInfrastrukturstufe und begrenzte Elektronikforschung. Route B verliert dieselben generischen Einkommen-/Forschungszeilen und6Stabilitätspunkte, erhält aber echte Großbewässerungsinfrastruktur, einen nativen langfristigen Wachstumsparameter und Gesundheitsbetriebseffizienz.

Auf beiden ausdrücklich unverändert regierten Routen bleiben ohne politische Reform July-State+8%Bürokratie und Patronage+10%Bürokratie bestehen. Damit sind die konkreten Beiträge inklusive **dieser zwei** Startideen A+70→+55% und B+61→+51%, vor weiteren nativen Gesetzen/Ideen. Die optionale Land-Survey-Kürzung würde die Vorschlagswerte um weitere2Punkte senken. Andere Starting-Spirits, deren andere Modifiers, native wirtschaftliche Gesetze und Vertragskosten werden dadurch nicht gelöscht.

Vollständige Routenlisten zur Nachprüfung: In beiden Fällen alle aktiven Foki der vier Kapitel nehmen und folgende Schlüssel ausschließen:

- **A ausgeschlossen:** oil_renegotiate,oil_concession_delivery,oil_diversification; industry_heavy,industry_credit_finance,industry_debt_accounts; agri_smallholders,agri_large_irrigation; society_mass_literacy,society_evening_classes,society_universal_services,society_primary_care.
- **B ausgeschlossen:** oil_renegotiate,oil_concession_delivery,oil_revenue_state; industry_light,industry_credit_finance,industry_debt_accounts; agri_smallholders,agri_local_irrigation,agri_dhiqar; society_teacher_first,society_teacher_deployment,society_targeted_services,society_priority_districts.

## Nachgewiesene native Mechaniken und ihre Grenzen

Alle folgenden Pfade sind relativ zum Modroot `C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar`, außer ausdrücklich als MainMD angegeben. Durch Quellenlesung belegt bedeutet nicht imEngine-Start getestet.

| Mechanik | Definition/Provider | Tatsächlicher Consumer bzw. bewährter nativer Effekt |
|---|---|---|
| Bürokratie,Sozial-,Gesundheits-,Bildungskosten | `common/modifier_definitions/money_modifier_definitions.txt:51`,`:107`,`:72`,`:65` | `00_money_system.txt:3311`,`:3505`,`:3476`,`:3374`; jeweils eigene Budgetzeile |
| Agri-Produktivität | `money_modifier_definitions.txt:353` | `00_money_system.txt:411`,`:547`,`:5947`; beeinflusst tatsächliches Agrar-GDP/Steuerberechnung, nicht magisch vorhandenes Land |
| Öl-Export | registrierter nativer modifier | `00_money_system.txt:4513`; an tatsächliche Ausfuhr/Preis gekoppelt, kein Ersatz für Förderressourcen |
| RelativeCG | vorhandener nativer Engine-Modifier | `00_money_system.txt:4674–4678`; erwarteterCG-Anteil×(1+Modifier), keine festen Fabrik-Prozentpunkte |
| Stromwerks-Brennstoffverbrauch | `energy_modifier_definitions.txt:101`; MainMD `common/ideas/Iraqi.txt:1707` | `common/scripted_effects/!_energy_effects.txt:382`; `energy_calc_generation`, getrennt von erzeugter Strommenge |
| Produktivitätswachstum | `money_modifier_definitions.txt:410`,ausdrücklich value_type=number; natives `health_02/.03` in `AA_law_budget.txt:1360`,`:1450` verwendet+.05/+.10 | `00_productivity_effects.txt:73–82` nimmt den Parameter×.5×(1+country_growth),danach State-Catchup-Faktor0..2/StateGrowth und Addition auf productivity_state_var(:235); monatlicherAufruf `MD_on_actions.txt:1200`. Keine Behauptung+3%sofortigesGDP |
| Vorhandene einmaligeRessourcen | vorhandener IRQ-Survey-Reward `rewards.txt`/`oil_kirkuk_survey` | natives `165={add_resource={type=oil amount=4}}`; bleibt unverändert. Kein neuer Ressourcenbonus fürWartung |
| EinmaligeInfrastruktur/Agrardistrikte | `common/buildings/00_buildings.txt`, bestehende IRQ-Zielstaaten1141/166 | natives `add_building_construction` mit Eigentum/Kontrolle/Kapazitätsprüfung **vor** Geldfluss; Receipt gegenWiederholung |
| BegrenzteTechnikforschung | `add_tech_bonus`; vorhandene IRQ-Industry/Colleges-Rewards | MainMD Türkei `TUR_industrial_research`2×50%Industry,40.04Tage (`turkey.txt:1726`); Israel `ISR_deliver_computers`1×25%IT,35Tage/$3bn (`05_israel.txt:2357`). Tatsächliche1970erTreffer: computing_1(1965),engineering.txt:822/835; microprocessors(1975),:883/904. Infantry:infantry_weapons_1(1965),:41/88; camouflage_1(1970),:1137ff; nicht nur ein Kategoriename ohneTechnologien |
| Wartungsfähigkeit/Ausbildungsnachteil | natives `attrition`, bestehendes IRQ `training_time_army_factor` | MainMDDeutschland `GER_Specialized_Indantry`, `05_germany.txt:6994`,Verbraucher `common/dynamic_modifiers/99_GER_dynamic_modifiers.txt:250`; Engine-Dokumentation `E:/SteamLibrary/steamapps/common/Hearts of Iron IV/documentation/modifiers_documentation.md:2002`und`:5044`registriertAttrition/ArmyTraining. Kein neuer scripted budget proxy |

Weitere Kalibrierung: MainMDRussland `SOV_aero_improvements`21Tage/$3bn/1×25%Aircraft/−10%AirAccidents (`05_russia.txt:13269`) trennt technisches Ziel und echte Kosten. Deutschland `GER_modernise_mining_equipment`45.5Tage/$10bn/1×40%Construction (`05_germany.txt:1976`) liefert eine endliche Projekthilfe. Diese modernen Länderwerte sind Referenzen für Form und Größenordnung, keine1970-Irak-Preisliste.

Insbesondere ist der vorgeschlagene+.03-Wachstumsparameter bewusst kein sofortiger Großbonus: bei ausgeglichenem Welt-/Staatsproduktivitätsniveau und ohne weitereWachstumsfaktoren beträgt sein eigener zusätzlicher Beitrag+.015absoluteProduktivitätspunkte jeMonat. Catchup und vorhandeneCountry-/State-Growth-Werte verändern diesen Beitrag. Seine praktische Haushaltsrendite sollte vor einer Umsetzung an einem echten1970Save gegenüber den höherenSozialkosten bewertet werden; aus dem Namen allein folgt keine+3%-GDP-Prämie.

Historischer Anker, knapp: Die zeitgenössischen Einschätzungen beschreiben bei irakischer Entwicklung konkrete Wasser-,Vermarktungs-,Transport-/Lager- und Fachkräfte-/Ersatzteilengpässe sowie pragmatisch gemischte Wirtschaftsformen. Daraus folgen unterschiedliche technische und institutionelle Programme, keine historisch gemessenen Prozentwerte. Quellen: [FRUS-Lagebild1976](https://history.state.gov/historicaldocuments/frus1969-76v27/d317), [FRUS-Einschätzung1973](https://history.state.gov/historicaldocuments/frus1969-76v27/d208). Die Irak-Iran-Eroberungsintegration und alle hier genannten Koeffizienten bleiben ausdrücklich alternative Spielgestaltung bzw.Balancevorschläge.

## Starke vorhandene Inhalte erhalten

Heavy/Light,Nationalisierung/Konzession,Revenue/Diversification,Professional/Reserve undSoviet/Mixed sind bereits brauchbare spezialisierte Investitionsentscheidungen; nicht mit neuen pauschalenBoni überladen. Das Gold ist ihre tatsächliche Fabrik,Forschung,Ausbildung,Lieferantenentscheidung und dauernde Verpflichtung.

Die großen Iran-/Kuwait-Prämien und Krisen sind ebenfalls bereits materiell: KhuzestanClaim/Wargoal/Core,stark erhöhte echte Iran-Wage-/Equipmentkosten,Golfkredite und konkrete Kuwait-Schulden-/Krisenauflösung. Die geladenen Iran-Kostenstufen erreichen+100/+175/+250%Armee-Personalkosten und+50/+100/+150%Equipmentkosten; Price of Victory trägt−30%Bauen,−20%Steuern,−10Stabilität,+2nativeZinsaufschlag und+20%relativeCG (`common/ideas/COLDWAR_IRQ_gulf_ideas.txt:5–29`). Diese Krise ist die eigentliche schwere historische Spielkette. Zusätzliche generische Bürokratie pro Bilanzfokus macht sie nicht glaubwürdiger. Ihre bestehenden Zeit-,Schulden-,Kriegsergebnis- und Empfängerzustimmungsgates bleiben daher unberührt.

Die aktuellen tatsächlichen Focus-/Decision-Tooltips und die Engine-Auswirkung der neuen Vorschläge wurden nicht getestet, weil diese Vorschläge ausdrücklich **nicht implementiert** sind. Save-Migration,paid revisions und einmalige Asset-Receipts müssen bei späterer Umsetzung eigenständig erhalten/geprüft werden; das bloße Austauschen einesModifiers imJSON genügt dafür nicht.
