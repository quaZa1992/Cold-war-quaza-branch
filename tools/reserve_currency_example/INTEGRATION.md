# IMPERIA COLD WAR — Native Einbaupunkte des Reservebeispiels

**Kein Aktivierungsleitfaden durch bloßes Kopieren.** `runtime/` enthält die neuen Beispielhelfer. Die folgenden nativen Verbindungen sind erforderlich, damit daraus eine vollständige Funktion wird. `integration.py` erstellt wesentliche Verbindungen zur Prüfung im Speicher; es patcht keine Spieldateien.

## 1. Bestehende Schuldenvorgänge bleiben maßgeblich

Beispiel aus `take_manual_debt_effect` in `common/scripted_effects/00_economic_system_utilities.txt`, mit unveränderten nativen Kreditbedingungen:

```text
# IMPERIA COLD WAR — Debt denomination around an accepted native borrowing transaction.
if = {
    limit = {
        check_variable = { interest_rate < 20 }
        NOT = { has_active_mission = cheap_loan_from_the_imf_mission }
        OR = {
            check_variable = { take_debt_min_gdp = 0 }
            check_variable = { gdp_total > take_debt_min_gdp }
        }
    }
    add_to_variable = { treasury = take_debt_amount }
    COLDWAR_MON_before_debt_change = yes
    add_to_variable = { debt = take_debt_cost }
    COLDWAR_MON_after_debt_change = yes
    ingame_update_setup = yes
}
```

Die neue Logik zahlt keinen zusätzlichen Kredit aus. Sie beobachtet den tatsächlich akzeptierten Zugang und schreibt dessen festgehaltenen Dollaranteil. Der Abschluss erfolgt **vor** einer nativen Neuberechnung, damit diese keine halbfertige Buchung sieht.

Im Speicher instrumentiert werden: `automated_debt_taker`, `take_manual_debt_effect`, `repay_manual_debt_effect`, `ai_repay_debt`, `modify_debt_effect` und `restructure_debt_after_financial_collapse`. Bei `modify_debt_effect` gehören Addition und anschließender Null-Clamp in **dieselbe** Buchung; ein vorübergehend negativer Zwischenwert darf kein abgeschlossener Schuldenstand werden.

Generische Tilgungen und Haircuts reduzieren beide Bestände proportional. Währungsspezifische Umschuldungen benötigen später eigene Annahme-/Gläubigerregeln und eine passende Buchung. Bei nativen Nullschulden wird der Dollarbestand ausdrücklich gelöscht.

## 2. Den FX-Faktor ersetzen, nicht verdoppeln

In `common/scripted_effects/00_money_system.txt` wird `calculate_debt_fx_factor` für initialisierte Länder geroutet:

```text
# IMPERIA COLD WAR — Contract stock determines FX exposure for migrated countries.
if = {
    limit = { has_country_flag = COLDWAR_MON_initialized }
    COLDWAR_MON_calculate_debt_fx = yes
}
else = {
    # Retain the complete native calculate_debt_fx_factor body here.
}
```

Der native Zinsweg muss auch den Fall Schulden = 0 vor seiner Nullschulden-Abzweigung abgleichen. Entweder sind alle Schuldenmutationen instrumentiert, oder `COLDWAR_MON_reconcile_untracked` wird zusätzlich am Eingang von `calculate_interest_rate` für initialisierte Länder aufgerufen. Ein zusätzlicher Abgleich dort wäre konstant teuer und darf keine vollständige Aktualisierung aufrufen.

Der Helfer berechnet aus `currency_strength` eine begrenzte Dollarbelastung und gewichtet sie mit `usd_principal / debt`. `no_foreign_reserve` und die ausgewählte Landeswährung löschen keine Altverträge. Für den Dollar-Emittenten bleibt der Faktor 1. Es gibt keine Division durch Null bei Nullschulden oder ungültiger Währungsstärke.

## 3. Vorhandene Reserveprojektionen weiterverwenden

`calculate_reserve_roi_bonus` in `common/scripted_effects/00_currency_effects.txt` verwendet für initialisierte Länder `COLDWAR_MON_refresh_derived`; der komplette alte Funktionskörper bleibt im `else` für bestehende Länder. Der neue Zweig setzt die vorhandenen Variablen `reserve_roi_bonus` und `reserve_trade_bonus` auf die gespeicherten USD-Projektionen, gewichtet mit dem eigenen Reserveanteil. Er addiert keinen zweiten Netzwerkbonus.

`increment_global_reserve_currency` verwendet während MDs vorhandenem Recount für initialisierte Länder `COLDWAR_MON_add_reserve_weight`. Frankreich mit Quote 0.8 zählt damit als 0.8 Dollar-Teilnehmer statt nach seiner Landeswährung als null oder eins. **Das ist eine gewichtete MD-Teilnehmerzahl, kein globaler Anteil des tatsächlichen Reservevermögens.** Eine GDP-Gewichtung wäre ebenfalls keine gemessene Reservegröße. Die native Seigniorage bleibt auf dieser vereinfachten MD-Grundlage.

Die unmittelbaren Zähleränderungen in den `on_add`/`on_remove`-Blöcken der bisherigen Währungsgesetze müssen für initialisierte Länder gezielt unterbunden oder passend ersetzt werden. Nur den Recount zu ändern genügt nicht: Ein späterer Gesetzwechsel könnte sonst zwischen zwei Recounts erneut ganze Teilnehmer addieren oder abziehen. Die übrigen Effekte dieser Gesetzblöcke und die Emittentenflags dürfen dabei nicht pauschal entfernt werden. Das ist im inaktiven Beispiel noch nicht als vollständiger Patch umgesetzt.

## 4. Monatstakt einmal global, einmal je Land

In `common/on_actions/MD_on_actions.txt`, innerhalb des **bereits vorhandenen** `on_monthly_done`-Guards:

```text
# IMPERIA COLD WAR — Persistent monthly dispatch serial; never reset in on_startup.
add_to_variable = { global.COLDWAR_MON_month_serial = 1 }
```

Im selben vorhandenen Callback, außerhalb des globalen Guards, unmittelbar nach `calculate_currency_strength = yes`:

```text
# IMPERIA COLD WAR — Country-local reserve settlement after native currency calculation.
COLDWAR_MON_monthly_once = yes
```

`monthly_preview()` findet beide aktuellen AST-Anker und verlangt genau einen Treffer. Es erzeugt keinen zweiten Monatscallback und keinen neuen `every_country`-Durchlauf. Der globale Projektionsteil arbeitet vor der lokalen Umschichtung; die Netzwerkgrößen bilden bewusst den vorherigen Monatsstand ab.

`COLDWAR_MON_last_month` wird vor dem Fortschritt gespeichert. Mehrfache Aufrufe derselben Monatsstufe, Öffnen des Menüs oder Wiederherstellen eines gespeicherten Modellzustands lösen dadurch keine zweite Monatsstufe aus. Der globale Zähler muss in echten Saves erhalten bleiben. Native `global.month`- und Jahreswerte werden dafür nicht zweckentfremdet.

## 5. Eine einzige Wochenbudget-Zeile

In `calculate_additional_expense_rate`, **nach** dem nativen `additional_expenses_rate = 0`, wird einmal eingefügt:

```text
# IMPERIA COLD WAR — Reserve programme appropriation in native billion-per-week units.
if = {
    limit = { has_country_flag = COLDWAR_MON_initialized }
    COLDWAR_MON_calculate_transition_cost = yes
    add_to_variable = { additional_expenses_rate = COLDWAR_MON_weekly_transition_cost }
}
```

Keine zusätzliche tägliche Abbuchung und kein zweites `modify_treasury_effect` für diese Wochenrate. Eine wiederholte Budgetberechnung baut denselben Ausgabenwert neu auf. Die einmalige Anlaufzahlung des Beschlusses läuft separat durch den nativen `modify_treasury_effect`. Dessen Skip-Flag wird schon vor der Beschlussausführung geprüft, damit daraus keine kostenlose Sonderausnahme wird.

## 6. Explizite Migration und tatsächliche Zustimmung

Startwerte werden in einer einmaligen, versionierten Szenario-/Save-Migration gesetzt, nachdem gültige Schulden und native Währungsstärke vorliegen. Die Landeswährung allein erlaubt keinen Rückschluss auf die Währung vorhandener Kredite.

```text
# IMPERIA COLD WAR — Illustrative approved seed, not historical country data.
if = {
    limit = { NOT = { has_country_flag = COLDWAR_MON_initialized } }
    set_variable = { COLDWAR_MON_seed_debt_usd_share = 0.4 }
    set_variable = { COLDWAR_MON_seed_reserve_usd_share = 0.8 }
    set_variable = { COLDWAR_MON_seed_new_usd_share = 0.6 }
    set_country_flag = COLDWAR_MON_seed_approved
    COLDWAR_MON_initialize = yes
}
```

Alle drei Variablen und die ausdrückliche Freigabe müssen vorliegen. Die Freigabe wird verbraucht. Ein erneuter Startup-Aufruf darf Bestände, Monatsbelege oder die Finanzierungsbedingungen nicht neu setzen. Für unbekannte Altbestände ist vor einer Migration eine dokumentierte Annahme erforderlich; eine freie Wahl der Spieler wäre ein Entschuldungsweg. Anschließend müssen Recount und globale Projektionen einmal im bestehenden Initialisierungsablauf einen kohärenten Startstand erhalten.

`COLDWAR_MON_clearing_access` darf nur die bereits angenommene außenpolitische Zahlungsvereinbarung setzen. `COLDWAR_MON_credit_terms_accepted` und `COLDWAR_MON_requested_usd_share` stammen aus der Annahme einer **gesonderten Kreditvereinbarung**, im Schuldner-Scope. Danach wird `COLDWAR_MON_accept_funding_terms` aufgerufen. Es gibt im Beispiel keinen Knopf, der diesen Zustimmungsbeleg selbst erzeugt.

Der konkrete diplomatische Anbieter ist noch nicht implementiert. Er muss Partner und Schuldner vor Versand festhalten, beide Zustimmungen und Gegenleistungen prüfen und beim endgültigen Abschluss erneut Geld, Bestand und Gültigkeit kontrollieren. Aus einer Währungswahl darf kein fremder Spieler automatisch ein Kreditangebot erhalten oder eine Zustimmung erteilen. `ROOT`, `FROM` und gespeicherte Partner dürfen bei verzögerten Ereignissen nicht neu über den gerade ausgewählten Staat hergeleitet werden. Die neuen Bedingungen gelten erst nach dem angenommenen Abschluss; der alte Dollarbestand bleibt erhalten.

## 7. Was vor einer echten RP-Multiplayer-Aktivierung fehlt

1. **Alle Schuldenzugänge/-abgänge erfassen.** Die sechs zentralen Provider sind ein Anfang. IMF-Missionen, einzelne Events, Foki, Sonderkredite, Defaults, Annexionen und Bürgerkriege können direkt in `debt` schreiben. Ein Nettoabgleich erkennt keine nicht instrumentierte Tilgung plus gleich hohe Neuaufnahme. Der konservative Fallback belastet unbekannte Zugänge vollständig als Dollar und setzt ein Auditflag; er ersetzt diese Prüfung nicht.
2. **Vertragsanbieter und Ablösung abschließen.** Gegenpartei, Annahme, Widerruf, Kosten, Verlust des Zugangs und bestehende Verpflichtungen benötigen vollständige native Abläufe. Das Beispiel enthält nur den prüfbaren Buchungsempfänger und einen Reservebeschluss.
3. **Alle Verbraucher der alten Einzelauswahl auditieren.** Neben den beschriebenen Hooks bestehen weitere `has_idea`-, Modifier- und `no_foreign_reserve`-Abhängigkeiten. Die Reserveeffekte müssen genau einem Bereich zugeordnet werden. Die jetzige Franc-/Lira-Auswahl bleibt bis dahin das alte System; ihre bloße Ergänzung aktiviert dieses Modell nicht. Ein späteres Menü zeigt „National Currency“ und „External Reserve Arrangements“ als getrennte institutionelle Angaben.
4. **Emittenten-/Zählerpfade vollständig prüfen.** Gesetzwechsel, neue Emittenten, Euro-Beitritt/-Austritt sowie Startup und laufender Recount dürfen nicht doppelt zählen oder das Schuldenbuch neu anlegen. Die Gewichtung nach Teilnehmern bleibt als bewusste Abstraktion offenzulegen.
5. **Engine und MP prüfen.** Neuer Spielstand und migrierter Save, Laden während eines laufenden Programms, Monatswechsel nach Laden, zwei gleichzeitige menschliche Entscheidungen, gescheiterte Vereinbarungen sowie Host-/Client-Zustand und OOS-Logs. Die vorhandenen 32 Interpretertests sind keine Zusage für Engine- oder Netzwerksynchronität.

Die Integration sollte zuerst in einem separaten Teststand erfolgen. Originale MD-Hinweise bleiben erhalten; nur die angepassten Projektblöcke tragen den Projektmarker. Scriptdateien bleiben UTF-8 ohne BOM, englische `.yml` mit BOM. Sämtliche Geldliterale im Beispiel haben höchstens fünf Nachkommastellen und laufende Kosten sind Wochenwerte.
