"""The Politburo and the Republics: three Politburo seats for the Union republics (MP roleplay system).

Design rules (Enes, 15.10.2026): max. 3 seats, Moscow picks them, seat holders get buffs, so the seats are scarce and wanted.
No per-republic loyalty meters (RP happens on Discord); only fixed statuses, fixed dates and visible votes.
No foreign-policy items for now.
"""
from sov_dsl import *

byid = {f['id']: f for f in FOCI}


def hook(fid, *effs):
    byid[PFX + fid]['eff'].extend(effs)


# ------------------------------------------------------------------ ideas (registered for validation and the idea file)
SEAT = idea("politburo_seat", "Seat in the Politburo",
            {"political_power_factor": 0.15, "stability_factor": 0.05, "production_speed_buildings_factor": 0.10})
DEFY = idea("defying_the_politburo", "Defying the Politburo", {"stability_factor": -0.05, "political_power_factor": -0.10}, days=180)
PATRON = idea("patron_in_moscow", "Patron in Moscow", {"political_power_factor": 0.05})
DISGRACE = idea("in_disgrace", "In Disgrace", {"stability_factor": -0.03, "political_power_factor": -0.05})
SLANDER = idea("slanderer", "Slanderer", {"political_power_factor": -0.05})
RELIEF = idea("plan_relief", "Plan Relief", {"stability_factor": 0.03, "political_power_factor": 0.05}, days=730)
SHORTFALL = idea("plan_shortfall", "Plan Shortfall", {"tax_gain_multiplier_modifier": -0.01}, days=730)
SOVEREIGN = idea("declaration_of_sovereignty", "Declaration of Sovereignty", {"stability_factor": 0.03, "political_power_factor": 0.05})

for k, t in [
    ("politburo_seats_category", "Kategorie „Seats of the Republics“ (Moskau): Sitz vergeben, Sitz entziehen, außerordentliches Plenum, Sitzung einberufen, Beförderung nach Moskau"),
    ("republic_politburo_category", "Kategorie „The Republic and the Politburo“ (jede SSR): Bewerbung, Anträge, Kompromat, Planbericht, Petition, Klient, nationale Bewegung"),
]:
    dec(k, t)
for k, t in [
    ("politburo_session", "Sitzung des Politbüros (1. Januar und 1. Juli): Anträge der Mitglieder, Planpriorität im Planjahr"),
    ("politburo_vote", "Abstimmung (je Sitzinhaber): Ja / Nein / Enthaltung; ohne Antwort nach 10 Tagen Enthaltung"),
    ("politburo_tally", "Auszählung nach 10 Tagen, News an alle Länder mit Stimmen pro Republik"),
    ("party_congress", "Parteitag: 30 Tage Umbesetzungsfenster, verdeckte Bewerbungen werden geöffnet"),
    ("kompromat", "Kompromat: Moskau ermittelt oder ignoriert; Ausgang nach Korruptionsstufe"),
    ("promotion_to_moscow", "Beförderung nach Moskau (Angebot an einen Sitzinhaber)"),
    ("republic_referendum", "Unabhängigkeitsreferendum: Moskau verhandelt, erkennt an oder lehnt ab"),
]:
    ev(k, t)

# leadership change as a Politburo vote: see the PLENUM loop in d_leaders.py
LEAN_TXT = {-1: "reformerisch", 0: "neutral", 1: "orthodox"}

# ------------------------------------------------------------------ Politburo resolutions on domestic key foci (no foreign policy for now)
RESOLUTIONS = [("renew_the_cadres", -1), ("respect_for_seniority", 1),
               ("deepen_the_kosygin_reform", -1), ("cybernetic_planning", 0), ("the_ministries_restored", 1),
               ("raise_retail_prices", -1), ("hold_the_prices", 1),
               ("russian_as_lingua_franca", 1), ("native_language_schools", -1),
               ("the_renewed_federation", -1), ("the_iron_union", 1)]
for fid, lean in RESOLUTIONS:
    hook(fid, txt(f"Politbüro-Beschluss ({LEAN_TXT[lean]}): Abstimmung 10 Tage nach Abschluss. Mehrheit → Mandat: PP +25, Stabilität +2 %. "
                  f"Keine Mehrheit → „Defying the Politburo“ (Stabilität −5 %, PP −10 %, 180 Tage) und Zusammenhalt −2"))

# ------------------------------------------------------------------ how the General Secretary trees change the rules (seat count stays 3)
INTERPLAY = [
    ("trust_the_local_barons", "Breschnew / Union", "Sitze nur noch auf Parteitagen änderbar (kein außerordentliches Plenum); Kompromat-Chance −10 %"),
    ("rotate_the_cadres", "Union", "Auf jedem Parteitag muss mindestens ein Sitz die Republik wechseln (Moskau wählt welchen)"),
    ("and_the_discipline_campaign", "Andropow", "Kompromat-Chance +20 %; der KGB darf ohne Ankläger gegen einen Sitzinhaber ermitteln (50 PP)"),
    ("and_the_cotton_affair_exposed", "Andropow", "Jede Republik mit Pripiski-Flag wird sofort untersucht"),
    ("pod_a_federal_union", "Podgorny", "Republikstimmen zählen doppelt bei Unionsfragen (Sprache, Unionsvertrag, Anträge der Republiken)"),
    ("she_purge_the_brezhnevites", "Schelepin", "Einmal: einen Sitzinhaber ohne Plenum-Kosten absetzen"),
    ("gro_iron_discipline", "Romanow", "Pripiski kosten zusätzlich Stabilität −3 % bei der Republik, die sie meldet"),
    ("gor_the_presidency", "Gorbatschow", "Föderationsrat (März 1990): Das Sitz-System endet, alle Republiken beraten den Präsidenten, Sitz-Buffs entfallen"),
]
for fid, who, t in INTERPLAY:
    hook(fid, txt(f"Politbüro der Republiken: {t}"))

# ------------------------------------------------------------------ concept data for the page and the design doc
POLITBURO = dict(
    core=[
        ("Sitze", "3 Sitze im Politbüro für die 14 Unionsrepubliken (die RSFSR ist Moskau selbst). Vollmitglied mit Stimme, keine Kandidatenstufe."),
        ("Wer vergibt", "Moskau (SOV) per gezielter Entscheidung auf eine SSR. Kostenlos im 30-Tage-Fenster eines Parteitags, sonst nur per außerordentlichem Plenum (100 PP, Stabilität −3 %)."),
        ("Start 1970", "Ukraine (Pjotr Schelest, Vollmitglied seit 1964) und Kasachstan (Dinmuchamed Kunajew, historisch ab April 1971 Vollmitglied). "
                       "Der dritte Sitz ist frei bis zum XXIV. Parteitag (30.03.1971): die erste Intrige der Partie."),
        ("Keine Zähler", "Keine Loyalitätswerte pro Republik. Das Spiel kennt nur Status (Sitz, In Disgrace, Slanderer, Patron, Pripiski, Souveränität), feste Termine und sichtbare Abstimmungen. Verhandelt wird im Discord."),
    ],
    seat=dict(name="Seat in the Politburo", mods=[["PP-Gewinn +15 %", True], ["Stabilität +5 %", True], ["Baugeschwindigkeit +10 %", True]],
              rights=["1 Stimme in jeder Abstimmung (Machtwechsel, Beschlüsse, Planpriorität, Anträge)",
                      "1 Antrag pro Sitzung (Unionsprojekt, Planentlastung, Kaderschutz)",
                      "1 Unionsprojekt pro Fünfjahrplan automatisch: ein Gebäude nach Wahl in der eigenen Republik, Moskau zahlt"],
              price="„Moskaus Auge“: Wer einen Sitz hat, kann keine nationalen Entscheidungen nehmen (Volksfront, Souveränität, Referendum). Der Sitz bindet an die Zentrale."),
    rhythm=dict(
        congresses=[("XXIV.", "30.03.1971", 1971.24), ("XXV.", "24.02.1976", 1976.15), ("XXVI.", "23.02.1981", 1981.14),
                    ("XXVII.", "25.02.1986", 1986.15), ("XXVIII.", "02.07.1990", 1990.5)],
        plans=[("IX.", 1971, 1976), ("X.", 1976, 1981), ("XI.", 1981, 1986), ("XII.", 1986, 1991)],
        sessions="Sitzungen am 1. Januar und 1. Juli (erste: 01.07.1970); Moskau kann eine zusätzliche Sitzung einberufen (50 PP).",
        window="Bewerbungen öffnen 90 Tage vor jedem Parteitag; im Parteitag 30 Tage Umbesetzung."),
    vote=dict(
        gensec="Generalsekretär (SOV-Spieler): 1 Stimme, frei.",
        moscow="Moskauer Block: 7 Stimmen, folgen der Politbüro-Balance. Ja-Stimmen = runden(3,5 + 3,5 × Balance × Richtung), Richtung −1 reformerisch, 0 neutral, +1 orthodox. "
               "Bei Anträgen der Republiken immer 3 Ja (die Zentrale ist skeptisch).",
        rep="Republiken: je 1 Stimme (mit Podgornys „A Federal Union“ 2 bei Unionsfragen). Ohne Antwort nach 10 Tagen: Enthaltung.",
        majority="Mehrheit: mehr als die Hälfte aller Stimmen (6 von 11). Enthaltung zählt nicht als Ja.",
        moscow_members=[("Alexei Kossygin", -1), ("Nikolai Podgorny", 0), ("Michail Suslow", 1), ("Andrei Kirilenko", 1),
                        ("Dmitri Poljanski", 1), ("Kirill Masurow", 0), ("Alexander Schelepin", 1)],
        note="Namen nur Kosmetik (Stand Januar 1970, rücken historisch nach). Die Stimmen kommen aus der Formel, nicht aus Personen."),
    agenda=[
        ("Machtwechsel", "Moskau", "nach Kandidat", "Politbüro-Fokus = Kandidatur, dann Entscheidung „Convene the Plenum“ (wiederholbar)",
         "Verbindlich. Ja: neuer Generalsekretär. Nein: kein Wechsel, Stabilität −3 %, Balance 0,05 gegen den Kandidaten, 180 Tage Sperre."),
        ("Nachfolge nach Tod", "Event", "nach Erbe", "Der gewählte Erbe wird zur Abstimmung gestellt",
         "Verbindlich. Nein: Plenum-Event mit den anderen lebenden Kandidaten, erneute Abstimmung."),
        ("Politbüro-Beschluss", "Moskau", "je Fokus", "11 innenpolitische Schlüsselfokusse (Kader, Kossygin-Reform, Preise, Sprache, Unionsvertrag)",
         "Ja: Mandat (PP +25, Stabilität +2 %). Nein: „Defying the Politburo“ und Zusammenhalt −2. Der Fokus gilt trotzdem."),
        ("Planpriorität", "Moskau", "neutral", "Zu Beginn jedes Fünfjahrplans (1971, 1976, 1981, 1986)",
         "Ja: Plan gilt, PP +50. Nein: Plan gilt, „Defying the Politburo“."),
        ("Antrag einer Republik", "Mitglied", "Moskauer Block 3 Ja", "Erst entscheidet Moskau; lehnt Moskau ab, kann das Mitglied vor das Politbüro gehen",
         "Ja: Moskau setzt um oder trägt „Defying the Politburo“. Nein: Antrag fällt."),
    ],
    proposals=[
        ("Unionsprojekt", "Ein Gebäude in der eigenen Republik: Zivilfabrik, Infrastruktur, Kraftwerk, Agrar oder Rüstungsfabrik.",
         "Moskau zahlt 0,5 % BIP (Rüstung 0,8 %) über `skip_payment`; Zusammenhalt +1."),
        ("Planentlastung", "Die Republik bekommt „Plan Relief“ (Stabilität +3 %, PP +5 %, 2 Jahre).", "Moskau bekommt „Plan Shortfall“ (Steuereinnahmen −1 %, 2 Jahre)."),
        ("Kaderschutz", "Immunität gegen Kompromat bis zum nächsten Parteitag.", "Kostet Moskau nichts außer einem Werkzeug."),
    ],
    intrigue=[
        ("Bewerbung", "Jede SSR ohne „Slanderer“", "90 Tage vor dem Parteitag ein verdecktes Gebot: 25, 50 oder 100 PP, sofort bezahlt. Nur Moskau sieht die Gebote.",
         "Moskau erhält die Gebote der Gewählten; die anderen bekommen die Hälfte zurück."),
        ("Kompromat", "Jede SSR (50 PP)", "Gegen einen Sitzinhaber. Moskau ermittelt (25 PP) oder ignoriert. Chance: 15 % + 5 % je Korruptionsstufe (`corruption_level_01`–`10`), +25 % bei Pripiski, +20 % Andropow, −10 % Barone, 0 % mit Kaderschutz, höchstens 90 %.",
         "Erfolg: Sitz weg, „In Disgrace“ bis zum übernächsten Parteitag, Angebot den Ersten Sekretär zu ersetzen, Zusammenhalt −1. Fehlschlag: Ankläger wird „Slanderer“ bis zum nächsten Parteitag."),
        ("Pripiski", "Jede SSR, einmal pro Plan", "Plan übererfüllt melden: PP +50, die News zeigt „Planerfüllung 108 %“.",
         "Korruption +1 Stufe und das Flag Pripiski, bis es aufgedeckt wird. Leichtes Ziel für Kompromat und die Baumwollaffäre."),
        ("Beförderung nach Moskau", "Moskau → Sitzinhaber", "Angebot (wie Alijew 1982, Schewardnadse 1985): Der Erste Sekretär geht nach Moskau.",
         "Annahme: neuer Erster Sekretär, der Sitz wird sofort frei (ohne Plenum-Kosten), die Republik bekommt dauerhaft „Patron in Moscow“ (PP +5 %, 1 Antrag pro Jahr auch ohne Sitz). Ablehnung: keine Strafe."),
    ],
    without=[
        ("Petition", "1 pro Jahr an Moskau, Inhalt wie ein Unionsprojekt. Moskau kann sie kostenlos ignorieren."),
        ("Klient", "Ein Mitglied stellt seinen Antrag für eine Klient-Republik; das Projekt entsteht dort, beide stehen in der News. Netzwerke entstehen."),
        ("Volksfront", "Nur ohne Sitz: nationale Partei der SSR +5 % Popularität; Zusammenhalt −2."),
        ("Souveränitätserklärung", "Nur ohne Sitz, ab Zusammenhalt < 55 oder 1985: „Declaration of Sovereignty“ (Stabilität +3 %, PP +5 %); Zusammenhalt −8, Moskau Steuereinnahmen −1 %."),
        ("Referendum", "Nur ohne Sitz, ab Zusammenhalt < 35: Moskau verhandelt (Unionsvertrag), erkennt an (Republik entlassen) oder lehnt ab. Gewalt nur per normaler Kriegserklärung."),
    ],
    cohesion=[("Sitz vergeben", "+1"), ("Unionsprojekt oder Antrag umgesetzt", "+1"), ("Kompromat erfolgreich", "−1"), ("Sitz entzogen", "−2"),
              ("Mehrheit übergangen", "−2"), ("Volksfront", "−2"), ("Souveränitätserklärung", "−8"), ("Referendum", "−10")],
    interplay=INTERPLAY,
    ai=[("Moskau als KI", "Historische Sitze: Ukraine und Kasachstan, auf dem XXIV. Parteitag Belarus (Mascherow), nach Mascherows Tod (Oktober 1980) auf dem XXVI. Parteitag Aserbaidschan (Alijew). Keine Beförderung, kein Kompromat."),
        ("Republik als KI", "Stimmt mit dem Generalsekretär; bewirbt sich mit 25 PP; alle 2 Jahre ein Unionsprojekt-Antrag; kein Kompromat, keine Pripiski, keine nationale Bewegung vor Zusammenhalt < 15."),
        ("Abwesende Spieler", "Nach 10 Tagen zählt keine Antwort als Enthaltung. Kein Spieler kann eine Abstimmung blockieren.")],
    impl=[("common/decisions/COLDWAR_SOV_politburo_decisions.txt", "Moskau: „Seats of the Republics“ (gezielt auf SSRs, `target_trigger` Subjekt der UdSSR mit `autonomy_soviet_republic_1985`); SSR: „The Republic and the Politburo“"),
          ("common/scripted_effects/COLDWAR_SOV_politburo_effects.txt", "Sitz vergeben/entziehen, Abstimmung starten, Moskauer Block berechnen, auszählen, Kompromat würfeln"),
          ("events/COLDWAR_SOV_politburo_events.txt", "Sitzung, Abstimmung je Mitglied, Auszählung, News an alle, Parteitag, Kompromat, Beförderung, Referendum"),
          ("common/ideas/COLDWAR_SOV_politburo_ideas.txt", "Seat in the Politburo, Defying the Politburo, Patron in Moscow, In Disgrace, Slanderer, Plan Relief, Plan Shortfall, Declaration of Sovereignty"),
          ("Variablen", "`global.COLDWAR_politburo_seats` (Array der Länder), `global.COLDWAR_vote_yes/no`, Flags auf den SSRs (`COLDWAR_SSR_seat`, `_pripiski`, `_disgrace`, `_slanderer`, `_cadre_protection`)"),
          ("später: interface/COLDWAR_politburo_window.gui", "Politbüro-Fenster als Scripted GUI nach den MDCW-UI-Regeln (`player_context`, dirty-Variable, KI wertet nie aus)")],
)
