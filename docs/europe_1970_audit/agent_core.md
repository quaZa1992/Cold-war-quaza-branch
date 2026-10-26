> **Archived CWEC material.** The custom system was removed on 18 October 2026. [Native MD restoration status](native_restore.md) supersedes the implementation claims below.

# Agentenbefund MD EU Kernsystem und 1970

Stand: 18.10.2026. Reine statische Recherche im aktuellen Workspace; keine Gameplay-Dateien geändert, kein HOI4-Laufzeittest. Historische Einordnung und Datumsbelege werden im Hauptbericht ergänzt. Die vorgeschlagenen `COLDWAR_EEC_*`-Namen sind neue Entwurfsnamen, keine vorhandenen Effects.

## Entscheidender Istzustand 1970 besitzt keinen konsistenten EG Start

Der globale Startup in [00_on_actions.txt](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/on_actions/00_on_actions.txt:1714>) ruft in ABK-Scope einmal `on_startup_euu_action = yes` auf ([Zeile 1953](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/on_actions/00_on_actions.txt:1953>)). Es gibt um diesen Aufruf kein Szenario- oder Datumsgate.

`on_startup_euu_action` startet in [99_eu_scripted_effects.txt:613](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:613>). Sein Initialisierungsblock prüft nur `NOT GAME_RULE_eu_disabled` und `NOT EU_initialized`, dann setzt er `EU_initialized` ([Zeile 691](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:691>)). Er unterscheidet 1970, 1985 und 2000 nicht.

**Wichtig: Der Code fügt 15 Tags in `global.EU_member` ein, aber gibt ihnen dabei nicht die Idea `EU_member`.** Die Liste AUS, BEL, DEN, ENG, FIN, FRA, GER, GRE, HOL, IRE, ITA, LUX, POR, SPR, SWE steht in [Zeile 760](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:760>). Im 1970-Historyblock von GER/FRA/ITA/BEL gibt es keine Mitgliedsidee; die jeweiligen `EU_member`-Einträge liegen erst innerhalb `2000.1.1`:

| Land | Beginn moderner History | moderne Mitgliedsidee |
|---|---|---|
| GER | [Zeile 28](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/history/countries/GER - Germany.txt:28>) | [Zeile 1445](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/history/countries/GER - Germany.txt:1445>) |
| FRA | [Zeile 27](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/history/countries/FRA - France.txt:27>) | [Zeile 1497](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/history/countries/FRA - France.txt:1497>) |
| ITA | [Zeile 26](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/history/countries/ITA - Italy.txt:26>) | [Zeile 1172](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/history/countries/ITA - Italy.txt:1172>) |
| BEL | [Zeile 25](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/history/countries/BEL - Belgium.txt:25>) | [Zeile 372](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/history/countries/BEL - Belgium.txt:372>) |

Statische Konsequenz: Der 1970-Start erzeugt eine widersprüchliche Kombination aus modernem Mitgliederarray und fehlender tatsächlicher Mitgliedsidee. Arraybasierte Bevölkerung/BIP/QMV rechnen mit der 15er-Liste; viele Buttons, Ämter sowie echte Ein- und Auszahlungen prüfen `has_idea = EU_member`. Es handelt sich somit nicht einfach um eine spielbare EU mit neun falschen Mitgliedern.

`EU_european_union_currently_exists` prüft ausschließlich `global.EU_member^num > 0` ([99_EU_scripted_triggers.txt:1278](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_triggers/99_EU_scripted_triggers.txt:1278>)); die Inkonsistenz wird dort nicht erkannt.

### Wann werden die Geistereinträge entfernt

`EU_resync_member_array` in [99_eu_scripted_effects.txt:412](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:412>) entfernt zunächst alle Arraymitglieder ohne Idea, fügt danach gegebenenfalls den Bürgerkriegssieger hinzu, der seine Mitgliedsidee geerbt hat.

Der einzige gefundene Aufruf steht in `on_civil_war_end` ([MD_on_actions.txt:594](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/on_actions/MD_on_actions.txt:594>), Aufruf [Zeile 611](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/on_actions/MD_on_actions.txt:611>)), ohne 1970-Ausnahme. Es gibt keinen täglichen, wöchentlichen oder monatlichen Resync. Der erste beendete Bürgerkrieg irgendwo kann deshalb die gesamte 15er-Liste leeren, falls weiterhin keine Mitgliedsideen vorhanden sind. Bis dahin können die Geistereinträge bestehen bleiben. Annex-Cleanup `remove_from_bloc_membership_arrays` entfernt nur das jeweilige Land aus dem Array ([01_international_systems_effects.txt:2882](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/01_international_systems_effects.txt:2882>)).

Die EU-Hintergrundchecks stehen tatsächlich in `on_monthly` ([MD_on_actions.txt:681](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/on_actions/MD_on_actions.txt:681>), EU-Block [Zeile 724](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/on_actions/MD_on_actions.txt:724>)). Sie berechnen BIP, Verstöße und Europeanism, synchronisieren aber keine Mitgliedschaft.

## Weitere unpassende Startup Inhalte

| Vorhandener Inhalt | Beleg | 1970-Konsequenz / Wiederverwendung |
|---|---|---|
| Moderne Agenden von Grundrechtecharta/Lissabon bis EZB/PESCO/DSGVO/Frontex und Erweiterungen 2004/2007/2013 | [99_eu_scripted_effects.txt:699](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:699>) | Eigene 1970-Agendenliste initialisieren, bestehende Voting-Infrastruktur als Transport verwenden. Nicht nur Texte ersetzen. |
| `foreign_data_kraken`, `asylum_shopping` für alle 15 Arraymitglieder | [Zeile 776](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:776>) | Nachweisbare moderne Belastungen auch ohne Mitgliedsidee; im 1970-Initializer weglassen. |
| Zufälliger KI-Monitor in `global.EU_potential`; sofort `EUelection.2`, nach 1625 Tagen `EUelection.1` | [Zeile 794](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:794>) | 1625 ist ein relativer 2000→2004-Abstand, kein absolutes 2004-Gate. In einem 1970-Start landet der nächste Wahlaufruf entsprechend 1974. Eigener Delegiertenmodus bis zur freigeschalteten Direktwahl. |
| Europeanism-Werte für die moderne 15er-Liste, SOV 0,05, VTB 0,5 | [Zeile 807](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:807>) | Eigenständige 1970-Werte statt unveränderter hoher Werte für IRE/POR/SPR/GRE. |
| Budget-/MFF-Vorbereitung für alle Arraymitglieder; Callrate je 1; Mindestcallrate 1 | [Zeile 839](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:839>) | Haushaltsmechanik sehr brauchbar, aber Six-only und passender Institutionseigner erforderlich. |
| Sämtliche Amtsvariablen zunächst EUU.id | [Zeile 856](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:856>) | EUU ist ein Leersitz-/Speicherscope; nicht automatisch ein 1970 existierender europäischer Staat. |

EUU selbst erhält 1970 lediglich generischen Fokusbaum, Wirtschafts-/Technikwerte und leere OOBs ([EUU - EU.txt:4](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/history/countries/EUU - EU.txt:4>)); dort gibt es keine EG-Institutionsinitialisierung.

## Mitgliedschaft Eintritt und Austritt was bereits funktioniert

### Datenmodell

`EU_member` ist die kanonische Mitgliedsidee ([Organizations.txt:4](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/ideas/Organizations.txt:4>)). `on_add` trägt das Land dedupliziert in `global.EU_member` ein, initialisiert Europeanism und ruft `EU_adopt_passed_laws` auf. `on_remove` entfernt das Land aus dem Array und startet geschützten Cleanup über `leaving_EU`.

Die Idea hat erhebliche allgemeine Boni/Kosten: demokratischer/neutraler Drift, −20 % politischer Machtfaktor, −5 % Kriegsunterstützungsfaktor, +15 % Handelsmeinung, +5 % Stabilitätsfaktor und −5 % Konsumgüterfaktor ([Zeile 29](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/ideas/Organizations.txt:29>)). Das ist kein neutrales institutionelles Mitgliedschaftsflag. Bei Wiederverwendung als EWG-Mitgliedschaft ist eine bewusste 1970-Balancefassung erforderlich.

`global.EU_potential` wird aus Mitglieder- und Nichtmitgliederkollektionen aufgebaut ([99_eu_scripted_effects.txt:785](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:785>)). Beide Kollektionen beruhen auf `constant:country_groups.all_eu_available_countries` und unterscheiden nur nach Mitgliedsidee ([collections.txt:3](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/collections/collections.txt:3>)). `EU_is_potential` ist eine sehr breite Tagliste einschließlich zahlreicher postsowjetischer/Abspaltungs-Tags ([99_EU_scripted_triggers.txt:659](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_triggers/99_EU_scripted_triggers.txt:659>)). Für 1970 sollte politische Teilnahme zusätzlich Existenz, Souveränität und passende Kampagnenbedingungen verlangen.

### Eintritt

`EU_apply_for_membership`, Kosten 50 PP, erteilt beim Abschluss direkt `add_ideas = EU_member` ([EU_voting_decisions.txt:1634](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:1634>), Abschluss [Zeile 1683](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:1683>)). Vorbedingungen:

- `breach_of_EU_value < 3`.
- `EU_candidate` und kein `EU_former_member`, oder ehemaliges Mitglied ohne `EU_rejoin_cooldown`.
- Kein Krieg; chinesischer Einfluss unter nativem 15er-Gate; sowjetischer Einfluss unter entsprechendem Gate oder SOV selbst besitzt Kandidatenflag.
- Spieler: Europeanism >0,79; KI: >0,69.

Das ist eine autonome Aufnahmeentscheidung des Kandidaten, sobald Kandidatur und Kennzahlen vorhanden sind. Für MP-RP fehlt an dieser Stelle die abschließende Zustimmung/Ratifizierung jedes bestehenden Mitglieds. Nach positivem Vertragsvotum besser einen begrenzten Ratifikationszustand setzen und erst nach allen Ja-Ratifikationen gemeinsam die Idea hinzufügen.

Bei bestehendem globalem `EDU` entfernt Eintritt unter Umständen die NATO-Idea und zieht das Land in die Fraktion eines EU-Fraktionsführers ([Zeile 1687](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:1687>)). EWG-Erweiterung darf 1970 nicht unbemerkt eine militärische Blockverschiebung auslösen; diesen Zweig ausdrücklich an eine gesonderte Verteidigungsvertragsreform binden.

### Austritt

`leaving_EU` ([99_eu_scripted_effects.txt:343](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:343>)) entfernt Mitgliedschaft, Euro und zahlreiche Gesetzesideen, räumt Ämter sowie Force-Controller auf, entfernt Budget-/MFF-/Abstimmungstimer und setzt `EU_former_member` plus dreijährige `EU_rejoin_cooldown` (1095 Tage). Dieses Cleanup ist gut wiederverwendbar.

Die politische Austrittskette bildet dagegen Art. 50 mit `Article_50`, 730-Tage-Frist und No-deal-Strafideen ab ([EU_voting_decisions.txt:777](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:777>), Frist [Zeile 838](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:838>)). Für 1970 neue politische Kette als Vertragskrise, einseitige Nichtanwendung oder verhandelter Austrittsvertrag; danach denselben technischen Cleanup verwenden. Der vorhandene `EU_former_member`-Cooldown ist eine Gameplayregel, keine historische Rechtsregel.

## Europeanism und Vertragsverstöße

`EU_update_vars` ([99_eu_scripted_effects.txt:29](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:29>)) berechnet Bevölkerung, `EU_pop_ratio`, bevölkerungsgewichteten `global.var_europeanism`, QMV-Staatenschwelle und passiven Europeanism-Drift aus `modifier@europeanism_drift`. `europeanism_change`, `EU_europeanism_change` und `EU_potential_europeanism_change` erlauben gezielte, mitgliedsweite oder gesamteuropäische Änderungen. Für RP brauchbar als öffentliches politisches Integrationsmandat; nicht als alleinige automatische Vertragszustimmung.

`check_breach_of_EU_value` in [Zeile 435](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:435>) summiert Korruption, Angriffskrieg gegen Mitglieder, kommunistische/reaktionäre Regierungsbeteiligung, Frauen in der Armee, Interventionismus, Wahlhürde, Zahlungsausfall, fehlende Wahlen, Diktatur und Untertanenstatus. **Das ist ein moderner, normativer Summenscore.** Für Cold-War-RP sachliche Einzelgründe speichern: Vertragsbruch, Zollkonflikt, Kapitalverkehr, offene Grenz-/Gebietsfrage, freie Wahlen, Souveränität. Kommunistische Beteiligung oder damalige Rekrutierungsregeln sollten kein unsichtbarer pauschaler Vertragsbruch sein.

`EU_council_has_breach_authority` gibt bestehende Durchsetzungsbefugnisse einem Top-3-Einfluss-Konsens oder dem Kommissionspräsidenten ([99_EU_scripted_triggers.txt:388](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_triggers/99_EU_scripted_triggers.txt:388>)). Als Machtpolitikspiel nutzbar; für förmliche 1970-Vertragsverfahren ausdrücklich durch Ratsbeschluss oder Schiedsverfahren ersetzen.

## Haushalt technisch nützlich politisch umzubauen

### Reale Geldanbindung

- `set_EU_gdp` ermittelt Gesamt-BIP und BIP-Anteile ([99_eu_scripted_effects.txt:1229](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1229>)).
- `update_EU_budget_call_rate` setzt jährlichen Beitrag = BIP × nationale Callrate ×0,01, wöchentlichen Beitrag = /52, Beitragsanteile sowie `global.EU_mff_total = Gesamtbudget ×5` ([Zeile 1312](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1312>)).
- Diese wöchentlichen Beiträge gehen bei tatsächlichen Mitgliedern in `additional_expenses_rate` ein ([00_money_system.txt:4012](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/00_money_system.txt:4012>)).
- Subventionen werden bei Mitgliedern ohne `EUU_subsidies_suspended` als Summe der vier Körbe ×0,019 in `additional_income_rate` gebucht ([00_money_system.txt:1032](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/00_money_system.txt:1032>)). Hinweis für spätere Balanceprüfung: 0,019 ist nur ungefähr 1/52; Ausgaben und Einnahmen nutzen nicht exakt denselben Faktor.

### Verteilung

`set_EU_expenditure`: 44 % Wachstum, 44 % natürliche Ressourcen, 6 % globales Handeln, 6 % Verwaltung ([Zeile 1373](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1373>)). Wachstum verteilt nach Bevölkerung × umgekehrtem Konjunkturlevel ([Zeile 1412](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1412>)); natürliche Ressourcen nach Bevölkerung × Einkommensstufe ([Zeile 1446](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1446>)). Das ist keine echte Agrarproduktion-/Kohle-/Stahlverteilung. Die absoluten BIP/Kopf-Bänder reichen bis 200, während GER 1970 mit 3,551 initialisiert wird; für eine historische Agrarpolitik muss die Berechnungsgrundlage angepasst werden.

Globale Ausgaben fließen vollständig an den `EU_is_leader_of_foreign_policy`-Träger; Verwaltung an Kommissionspräsident/Frontex-Direktor ([Zeile 1395](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1395>), [Zeile 1484](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1484>)). Für RP ist es problematisch, Gemeinschaftsverwaltung als zusätzlichen nationalen frei verfügbaren Gewinn des Amtsinhabers auszuzahlen. Besser Projektfonds/Kommissionsverwaltung als eigenen gespeicherten Topf und konkret bewilligte Auszahlungen modellieren.

**Statisches Risiko vor Wiederverwendung:** `EU_global_exp_subsidies` und `EU_admin_subsidies` werden in diesen Effekten nur für derzeit berechtigte Ämter gesetzt; die übrigen Mitglieder werden nicht auf null zurückgesetzt. Bei Ämterwechsel können alte Zuschüsse weiterleben. `EU_budget_total_gain` summiert diese Variablen unverändert ([Zeile 1534](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1534>)). Ebenso wird `EU_growth_subsidies` nur bei erkanntem Konjunkturlevel neu gesetzt, vor der anschließenden Normalisierung ohne solchen Level aber nicht gelöscht. Laufzeittest für Amtswechsel/fehlende Konjunkturidea erforderlich.

### Politischer Haushaltszyklus

Jährlicher Haushalt: 344 Tage Timer, 7 Tage Vorbereitung, 14 Tage Verhandlung ([EU_voting_decisions.txt:415](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:415>)). MFF: 1237 Tage Timer, 14 Tage Vorbereitung, 28 Tage Verhandlung ([Zeile 521](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:521>)). Die 5-fache Budgetanzeige und der ungefähr 3,5-jährige MFF-Timer passen bereits untereinander nicht unmittelbar zusammen; für 1970 ausdrücklich bestimmen, ob man jährliche Finanzierung oder bewusst ein alternatives Mehrjahresregime modelliert.

`EU_save_budget_values`, `EU_save_mff_values`, `EU_rollback_budget_values`, `EU_rollback_mff_values` speichern/rekonstruieren Entwürfe ([99_eu_scripted_effects.txt:1256](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1256>)). Diese Transaktionsidee ist gut wiederverwendbar.

**Harte Abhängigkeit:** Budgetabschluss und MFF-Abschluss werden nur von `ECB_president` finalisiert; ohne dieses Amt wird der Entwurf zurückgerollt ([EU_voting_decisions.txt:476](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:476>), [Zeile 582](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/decisions/EU_voting_decisions.txt:582>)). Die EZB 1970 bloß auszublenden macht Haushaltsreformen unabschließbar. Zuständigkeit auf Kommission/Ratspräsidentschaft übertragen und das damalige parlamentarische Haushaltsrecht separat modellieren.

## Ämter Währung und weitere technische Stolpersteine

Amtsideen schreiben direkt Scope-Zeiger, beispielsweise `EU_commission_president` → `global.eu_commission` und `EU_council_president` → `global.eucouncil` ([EU_ideas.txt:4](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/ideas/EU_ideas.txt:4>), [Zeile 20](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/ideas/EU_ideas.txt:20>)). Beim Entfernen werden Leersitz EUU, Benachrichtigungen und KI-Cooldowns gesetzt. Damit kann man reale Spielerämter gut darstellen. Die derzeitige Verleihung gibt dem Rat 1825 Tage und der Kommission 1825 Tage ([01_european_union_guis.txt:1823](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:1823>), [Zeile 1873](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_guis/01_european_union_guis.txt:1873>)). Für 1970 Ratspräsidentschaft als kurze Rotation und Kommission als institutioneller Vorschlaggeber neu regeln; externe Akteure können Beobachter/Assoziationspartner sein, ohne ein EG-Amt zu besetzen.

`EU_influence_on_leader_of_foreign_policy_25_percent` liest `global.EU_foreign_minister`, `global.EU_commission_president`, `global.EU_parliament_president` ([99_EU_scripted_triggers.txt:344](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_triggers/99_EU_scripted_triggers.txt:344>)). Die Amtsideen speichern jedoch `global.euforeignaffairs`, `global.eu_commission`, `global.euparliamentpresident`. Dieser Namenskonflikt ist vor Verwendung für verhandelte Austritte zu korrigieren; allein die vorhandene Leersitz-Ausweichregel behebt einen gefüllten, falsch referenzierten Sitz nicht.

**Euro ist bereits geschützt:** `joining_the_euro` läuft nur nach 31.12.1998 ([99_eu_scripted_effects.txt:1829](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:1829>)); die Idea `euro` ist vor 1999 unsichtbar und wird vor 1999 gecancelt ([AA_law_expanded_economics.txt:791](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/ideas/AA_law_expanded_economics.txt:791>)). Für eine frühe alternative Währungsunion braucht man folglich eine neue Vor-Euro-Währungskooperation/Verrechnungseinheit oder eine bewusst freigegebene Alternativregel in beiden Gates. Nur GUI-Umbenennung oder früher Focus genügt nicht.

`execute_OMT`/`remove_OMT` stellen eurogebundene Schuldenoperationen dar ([99_eu_scripted_effects.txt:241](<C:/Users/Enes/Documents/Paradox Interactive/Hearts of Iron IV/mod/mdcoldwar/common/scripted_effects/99_eu_scripted_effects.txt:241>)). Nicht als 1970-Standardmechanik übernehmen. Passender wäre ein begrenzter Kredit-/Beistandsfonds mit national ratifizierter Haftung.

## Konkreter Umsetzungsentwurf für eine erste spielbare Fassung

1. **Szenarioweiche vor dem nativen Initializer:** `IMP_is_1970_scenario` entscheidet zwischen neuem `COLDWAR_EEC_initialize` und dem bestehenden modernen Startup. Nicht erst nach dessen Ablauf korrigieren, weil bereits moderne Eventtimer und Missionen bewaffnet wurden.
2. **Ein kanonischer Mitgliederzustand:** Gründungssechs FRA/GER/ITA/BEL/HOL/LUX konsistent als 1970-Mitgliedsidee und Array setzen; `add_ideas` nutzt den vorhandenen on_add. Entweder bestehende Idea bewusst an die Epoche anpassen oder alle Consumer über einen einheitlichen Trigger auf eine eigene EG-Idea umstellen. Mischzustände vermeiden. Beim Laden einmal deduplizieren und tatsächliche Mitgliedschaft abgleichen.
3. **EWG, EGKS, Euratom als Vertragsebenen:** Vorhandenes Vollmitgliedsarray bleibt die institutionelle Basis; zusätzliche Länderflags/Arrays für Assoziation, Zollverein, Euratom-Projektteilnahme und Kapitalverkehr. So kann Österreich/Schweden/Schweiz kooperieren, ohne sofort volle Mitgliedschaft oder NATO-Folgen zu erben.
4. **Ratspräsidentschaft und Kommission:** Ratsposten rotierend; Kommission kontrolliert Agenda-/Haushaltsentwürfe. Vorhandene Amtszeiger und Cleanup behalten, Amtsdauer/Befugnisse ändern. Nationale Delegationen kontrollieren Ratifikation; persönliche Kommissare müssen nicht bedeuten, dass ihr Herkunftsland das EG-Budget bekommt.
5. **Erweiterungswelle als Vertrag:** Eigene Kandidatengruppe ENG/IRE/DEN/NRY, Verhandlungskapitel Landwirtschaft, Fischerei, Haushalt und Übergangsfristen. Kandidaten erhalten nicht sofort modernen hohen Europeanism und nicht allein durch 50 PP die Mitgliedschaft. Rat einstimmig → nationale Zustimmung/Referendum → gemeinsames Inkrafttreten. Nein eines Kandidaten blockiert dessen Beitritt, nicht zwingend die anderen.
6. **Haushalt mit sichtbarem Konflikt:** Vorhandene BIP-/Wochenbuchhaltung und Entwurfsrollback behalten. Ausgangsfinanzierung bewusst begrenzen, national unterschiedliche Beiträge und finanzierte Agrar-/Industrie-/Forschungsprojekte zeigen. Streit um Eigenmittel, Agrarausgaben und Rückflüsse wird über konkrete RP-Abstimmungen spielbar. Rat/Kommission statt EZB finalisieren.
7. **Delegiertenparlament zunächst beratend:** Sofortige EUelection.2 und relativen 1625-Tage-Timer ersetzen. Eine Reform kann spätere Direktwahlen, stärkere Budgetrechte und geänderte Amtsbesetzung freischalten; frühe Alternative benötigt expliziten Vertrag.
8. **Vertragssouveränität:** Krisen, Boykott und einzelne nicht umgesetzte Beschlüsse als abgestufte Zustände statt sofortiger moderner Art.-50-Kette. Technischen `leaving_EU`-Cleanup erst beim finalen Ausscheiden auslösen.
9. **Historischer Fortschritt und alternative Wege:** Währungskooperation, politische Kooperation, Sozialfonds-/Regionalförderung, frühere Föderalisierung oder lockere intergouvernementale Gemeinschaft als konkurrierende Verträge freischalten. Für MP immer explizite Spielerzustimmung zu Schuldenhaftung, Währungsaufgabe, Militärkontrolle oder Staatsfusion verlangen.

## Sinnvolle Prüfungen vor Freigabe

- 1970 Tag 1: genau sechs konsistente Vollmitglieder, keine modernen Strafideen, keine moderne Wahl nach 1625 Tagen, Euro in keinem Mitgliedsland.
- Erster beendeter Bürgerkrieg: Mitgliederarray bleibt korrekt und ein Sieger erbt nur die sachlich gewünschte Mitgliedschaft.
- Monatswechsel: Bevölkerung/BIP, Verstöße und Europeanism laufen ohne moderne Migrantenkrise oder nicht existierende Kandidaten-UI.
- Haushaltsänderung ohne EZB: Entwurf kann unter passender 1970-Zuständigkeit passieren oder sauber verworfen werden; Subventionssummen konservieren die verfügbaren Mittel.
- Amtswechsel: alter Amtsinhaber verliert sämtliche Verwaltung-/Außenpolitikzuschüsse; neuer erhält nur genehmigte Mittel.
- Erweiterung/Austritt: keine automatische NATO-/Fraktionsänderung ohne zusätzlichen Verteidigungsvertrag, keine Wiedereintrittsumgehung, keine verwaisten Missionen.

Diese Prüfungen wurden nicht ausgeführt; sie sind die nach dem statischen Audit nötige Integrationsprüfung.
