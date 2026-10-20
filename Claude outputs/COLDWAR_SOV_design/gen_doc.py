"""Generate the German design doc (markdown) and the machine-readable data JSON from the DSL."""
import sys, json, collections
sys.path.insert(0, '/home/claude/sov')
import build_all
from sov_dsl import *
import d_concept as C
import d_republics as R

VERSION = "Entwurf v3, 15.10.2026"
ART = "https://claude.ai/artifact/43ToufYGLjP7mezpQayZqU"
short = lambda x: x.replace(PFX, "")

cnt = collections.Counter(f['sec'] for f in FOCI)
import subprocess, re
_v = subprocess.run([sys.executable, '/home/claude/sov/validate.py'], capture_output=True, text=True, cwd='/home/claude/sov').stdout
_m = re.search(r"downside: (\d+) \((\d+) %\), with exclusive choice: (\d+), historical: (\d+)", _v)
assert "ERRORS 0" in _v and "ERRORS2 0" in _v, _v[-2000:]
pct_cost, n_mx = int(_m.group(2)), int(_m.group(3))
n_hist = sum(1 for f in FOCI if f['hist'])
party_secs = [s for s in SECTIONS if s['group'] == 'Parteien']
leader_secs = [s for s in SECTIONS if s['title'].startswith('Generalsekretär')]

L = []
w = L.append
w(f"# Sowjetunion 1970 – Focus-Tree-Design ({VERSION})\n")
w(f"Status: **Design, noch kein Code** (Approval-Gate). Visualisierung: Artifact „Soviet Union 1970 Focus Tree“ ({ART}). "
  f"Tree-ID `COLDWAR_SOV_1970_focus`, Präfix `COLDWAR_SOV_`, Events `COLDWAR_SOV.N`. Maschinenlesbare Daten: `claude/mdcw_sov_1970_focus_tree_data.json` "
  f"(Generator-Eingabe, Effekte mit Typ und Parametern). Quellen (DSL, Validator, Export) im Mod-Ordner unter `Claude outputs/COLDWAR_SOV_design/`.\n")
w(f"Umfang: **{len(FOCI)} Fokusse** in {len(SECTIONS)} Bereichen · {len(IDEAS)} Ideen (davon 7 Startgeister) · {len(PROGS)} Partei-/Führerprogramme · "
  f"{len(OFFERS)} Angebote an andere Länder · {len(TRAITS)} Traits. Statische Prüfung gegen die Mod (MD 2.0.2 + Imperia + MDCW): 0 Fehler. "
  f"{pct_cost} % der Fokusse haben einen Preis, {n_mx} sind Teil einer exklusiven Wahl, {n_hist} historisch.\n")
w("## Änderungen in v2 und v3\n")
w("- **Generalsekretäre schließen sich nicht mehr aus.** Neuer Bereich „Das Politbüro: Machtwechsel“: Breschnew regiert zum Start "
  "(Flag `COLDWAR_SOV_gensec_bre` aus dem Init). Jeder andere Kandidat hat einen eigenen Politbüro-Fokus, der nur prüft, ob er lebt, im Politbüro sitzt "
  "und seine Fraktionen hinter sich hat. Kein Fokus sperrt einen anderen; man kann mitten in Breschnews Baum zu Kossygin wechseln und später zu Andropow.")
w("- **Ein Baum pro Generalsekretär, offen solange er regiert** (`COLDWAR_SOV_gensec_<name>`). Erledigte Fokusse bleiben, das Programm des Vorgängers fällt weg.")
w("- **Elf Generalsekretäre statt sechs**, jeder detailliert (Team, erste Weiche, Politikzweige, zweite Weiche, Nachfolge, Abschluss): "
  "Breschnew, Kossygin, Podgorny, Andropow, Tschernenko, Gorbatschow; **Hardliner** Suslow, Schelepin, Romanow; **Marschälle** Gretschko und Ustinow.")
w("- **Nachfolge über Erben-Flags** (`COLDWAR_SOV_heir_<name>`) und ein Todes-Event am historischen Todesdatum des Amtsinhabers.")
w("- **Salafistische, schiitische und islamische Wege entfernt** (Outlook-Block, Richtung im Stamm, Power-Fokusse, Parteibäume 8–12).")
w("- **Das Politbüro und die Republiken:** 3 Sitze für die SSR-Spieler, Abstimmungen bei Machtwechsel, Beschlüssen, Planpriorität und Anträgen; Intrige über Bewerbung, Kompromat, Pripiski und Beförderung. Der Machtwechsel läuft jetzt über Kandidatur-Fokus plus Plenum-Abstimmung.\n")
w("## Leitideen\n")
w("- MD-2000er-Stil (Russland/Generic): `relative_position_id`, Log in jedem `completion_reward`, `search_filters` überall, `ai_will_do` mit `is_historical_focus_on`, Kosten 1/3/5/7/10.")
w("- Drei Kernsysteme machen das Zusammenhalten schwer, aber machbar: **7 Startgeister**, **Politbüro-Balance** (BOP wie `SOV_west_east_bop`), **Zusammenhalt der Union** (0–100, Start 62).")
w("- Fünf Länder-Modifier mit Variablen (Muster `SOV_economy_modifier` / US-Departments): Parteistaat, Gosplan, Streitkräfte, Union, Sozialistische Gemeinschaft.")
w("- Politik in drei Ebenen wie Ägypten Rev. 7: Stamm mit Richtungswahl (vier Richtungen) → Outlook stärken + „Power to …“ → Outlook-Einstieg (`has_government`) → "
  f"Parteibäume (`*_are_in_power`). Neben der KPdSU haben {len(party_secs)} Parteien einen Baum.")
w(f"- KPdSU: gemeinsamer Parteibaum + Politbüro-Bereich + {len(leader_secs)} Generalsekretär-Bäume ohne gegenseitigen Ausschluss. "
  "Sechs Wege führen aus dem Parteistaat hinaus: Suslow → 6, Schelepin → 7, Kossygin → 13, Podgorny → 19, Gretschko → 22, Gorbatschow → 3.")
w("- Nachteile nur, wo sie aus der Sache folgen. Multiplayer: kein Fokus erzwingt etwas bei einem anderen Land, alles über Angebote (Dispatcher-Event, keine Vorab-Belohnung).")
w("- Cold-War-Integration: `mdcw_cw_add_tension`, `mdcw_cw_change_alignment`, CW-Custom-Modifier (Kampagnen, Hilfskapazität, Militärprogrammkosten, ideologische Abwehr).\n")

w("## Startgeister\n")
for k, n, m, why, how in C.START_SPIRITS:
    w(f"- **{n}** `{PFX}{k}`: {mods_text(m)}. {why} *Weg hinaus:* {how}")
w("")
w("Startgesetze: " + ", ".join(f"`{a}`" for a, _ in C.START_LAWS) + ".\n")
w("Startfraktionen: " + ", ".join(f"{n} {v}" for _, n, v in C.START_FACTIONS) + ".\n")

b = C.BOP
w(f"## Politbüro-Balance `{b['id']}` (Start {str(b['initial']).replace('.', ',')})\n")
for r in b['ranges']:
    w(f"- {r[0]} **{r[1]}**: {r[2]}" + (f" – {r[3]}" if len(r) > 3 and r[3] else ""))
w("")
w(f"{b['drift']} {b['decisions']}\n")
c = C.COHESION
w(f"## Zusammenhalt der Union `{c['var']}` (Start {c['start']})\n")
for t in c['tiers']:
    w(f"- {t[0]} **{t[1]}**: {t[2]}")
w("")
w(f"{c['monthly']} Werkzeuge: {c['tools']}\n")
w("## Länder-Modifier\n")
for key, name, grp, desc, start in C.DYNMODS:
    w(f"- **{name}** `{PFX}{key}_modifier`: {desc}. Start: {start}.")
w("")
w("## Entscheidungen\n")
for n, d in C.DECISIONS_C:
    w(f"- **{n}**: {d}")
w("")
w("## Events\n")
for n, d in C.EVENTS_C:
    w(f"- **{n}**: {d}")
w("")

w("## KPdSU: Politbüro und Generalsekretäre\n")
w("Ablauf: `ple_the_politburo` (Kosten 1) öffnet die Politbüro-Fokusse und Breschnews Baum. Jeder Politbüro-Fokus (`ple_<name>`, Kosten 5) "
  "baut eine Kandidatur auf und öffnet die Entscheidung „Convene the Plenum: <Name>“ (wiederholbar, 180 Tage Sperre nach einem Fehlschlag). "
  "Das Politbüro stimmt ab (Generalsekretär 1, Moskauer Block 7 nach Balance und Richtung des Kandidaten, 3 Republiksitze). Bei Mehrheit setzt "
  "`COLDWAR_SOV_install_gensec` den neuen Generalsekretär ein (Flag tauschen, `create_country_leader` / `promote_character`, Traits), mit Stabilität −5 %, "
  "„Plenum Shake-up“ (Stabilität −5 %, PP −10 %, 120 Tage) und Fraktionsänderungen nach Kandidat; ohne Mehrheit kein Wechsel, Stabilität −3 %, Balance 0,05 gegen ihn. "
  "Kein Politbüro-Fokus ist exklusiv. Ein Generalsekretär-Baum hat als `available` "
  "`communist_states_are_in_power` + `has_country_flag = COLDWAR_SOV_gensec_<name>`.\n")
w("Erben: Die Nachfolgeweiche in jedem Baum setzt `COLDWAR_SOV_heir_<name>`. Das Todes-Event am historischen Datum des Amtsinhabers stellt den Erben dem Politbüro "
  "zur Abstimmung (ohne Fokus-Kosten; der Politbüro-Fokus wird per `unlock_national_focus` als erledigt markiert), sofern der Erbe dann noch lebt; "
  "ohne Erben oder ohne Mehrheit folgt ein Plenum-Event mit den lebenden Kandidaten. Die KI folgt den historischen Todesfällen und nimmt keine alt-hist Politbüro-Fokusse.\n")
w("| Generalsekretär | Typ | Politbüro-Fokus | Tod | Erben und Endpunkte | Fokusse |\n|---|---|---|---|---|---|")
for nm, k, win, death, typ, heirs in C.LEADERS_C:
    w(f"| {nm} | {typ} | {win} | {death} | {heirs} | {cnt.get(k, 0)} |")
w("")

P_ = R.POLITBURO
w("## Das Politbüro und die Republiken (3 Sitze)\n")
w("Multiplayer-RP-System: Die 14 Unionsrepubliken (SSR-Spieler) kämpfen um 3 Sitze im Politbüro. Verhandelt wird im Discord; das Spiel hält Sitze, Abstimmungen und Folgen fest "
  "und meldet jedes Ergebnis allen Spielern als News. Keine Loyalitätswerte pro Republik. Außenpolitische Mitsprache ist bewusst noch nicht enthalten.\n")
for a, b_ in P_['core']:
    w(f"- **{a}**: {b_}")
w("")
w(f"**{P_['seat']['name']}**: " + ", ".join(m[0] for m in P_['seat']['mods']) + ". Rechte: " + "; ".join(P_['seat']['rights']) + f". {P_['seat']['price']}\n")
w("**Rhythmus:** Parteitage " + ", ".join(f"{c[0]} {c[1]}" for c in P_['rhythm']['congresses']) + "; Fünfjahrpläne " +
  ", ".join(f"{p_[0]} {p_[1]}–{p_[2] - 1}" for p_ in P_['rhythm']['plans']) + f". {P_['rhythm']['window']} {P_['rhythm']['sessions']}\n")
w(f"**Abstimmung:** {P_['vote']['gensec']} {P_['vote']['moscow']} {P_['vote']['rep']} {P_['vote']['majority']}\n")
w("| Gegenstand | Von | Richtung | Wann | Folgen |\n|---|---|---|---|---|")
for a in P_['agenda']:
    w("| " + " | ".join(a) + " |")
w("")
w("Politbüro-Beschlüsse im Baum: " + ", ".join(f"`{f}` ({R.LEAN_TXT[l]})" for f, l in R.RESOLUTIONS) + ".\n")
w("**Anträge der Mitglieder** (1 pro Sitzung; erst entscheidet Moskau, bei Ablehnung Abstimmung):\n")
for a, b_, c_ in P_['proposals']:
    w(f"- **{a}**: {b_} {c_}")
w("")
w("**Intrige:**\n")
for a, who, how, res in P_['intrigue']:
    w(f"- **{a}** ({who}): {how} {res}")
w("")
w("**Ohne Sitz:**\n")
for a, b_ in P_['without']:
    w(f"- **{a}**: {b_}")
w("")
w("**Zusammenhalt** (nur feste Schritte): " + ", ".join(f"{a} {b_}" for a, b_ in P_['cohesion']) + ".\n")
w("**Die Generalsekretäre ändern die Regeln** (Zahl der Sitze bleibt 3):\n")
for fid, who, t in P_['interplay']:
    w(f"- `{fid}` ({who}): {t}")
w("")
w("**KI:**\n")
for a, b_ in P_['ai']:
    w(f"- **{a}**: {b_}")
w("")
w("**Dateien:**\n")
for a, b_ in P_['impl']:
    w(f"- `{a}`: {b_}")
w("")

w("## Parteien\n")
w("| # | Partei | Ideologie | Führung 1970 | Baum |\n|---|---|---|---|---|")
psec = {s['party']: s for s in SECTIONS if s['group'] == 'Parteien'}
for i in range(24):
    n, ideo, lead = PARTY[i]
    tree = "KPdSU + Politbüro + Generalsekretäre" if i == 4 else (f"{cnt[psec[i]['key']]} Fokusse" if i in psec else "kein Baum")
    w(f"| {i} | {n} | {ideo} | {lead} | {tree} |")
w("")
w(C.NO_TREE + "\n")

w("## Angebote (Multiplayer)\n")
for k, v in OFFERS.items():
    w(f"- `{k}` → {', '.join(v['tags'])}: {v['text']}")
w("")

w("## Fokusse\n")
for s in SECTIONS:
    fs = [f for f in FOCI if f['sec'] == s['key']]
    w(f"### {s['title']} ({len(fs)})\n")
    w(s['desc'] + "\n")
    for f in fs:
        head = f"- **{f['name']}** `{f['id']}` · Kosten {f['cost']}"
        if f['hist']: head += " · hist."
        head += " · benötigt: " + (", ".join(" oder ".join(short(x) for x in g) for g in f['pre']) or "–")
        if f['mx']: head += " · schließt aus: " + ", ".join(short(x) for x in f['mx'])
        if f['av']: head += f" · verfügbar: {f['av']}"
        if f['bypass']: head += f" · Bypass: {f['bypass']}"
        if f['ai'] == '0': head += " · nur Spieler (KI nie)"
        w(head)
        for e in f['eff']:
            w(f"  - {e['t']}")
        if f['note']:
            w(f"  - _Anmerkung:_ {f['note']}")
    w("")

w("## Dateien (Umsetzung)\n")
for p, d in C.FILES:
    w(f"- `{p}`: {d}")
w("")
w("## Porträts\n")
w(", ".join(f"{n} ({d})" for n, d in C.PORTRAITS) + "\n")
w("## Offen für die Umsetzung\n")
w("- Fokus-Icons aus den Cold-War-GFX-Ordnern zuordnen (wie Ägypten: Icon + 2 Alternativen pro Fokus).")
w("- Staats-IDs für Samotlor/Tjumen, Magnitka, Amur-Bunker prüfen (derzeit `random_owned_controlled_state` mit Limit).")
w("- Getreideimporte und Fünfjahrpläne als Decisions ausformulieren; Kosten der MD-Bau-Helfer über `skip_payment` + BIP-Anteil (BIP SOV ≈ 186).")
w("- `COLDWAR_SOV_install_gensec`: Charaktere für alle elf Kandidaten plus Grischin und Alijew anlegen (Porträts siehe oben); Todesdaten als Game-Rule-abhängige Events.")
w("- Ingame-Test HOI4 1.19 mit frischem `error.log`; KI-Beobachtung (Breschnew-Weg, Nachfolge 1982–1985).")
open('/home/claude/sov/mdcw_sov_1970_focus_tree_design.md', 'w').write("\n".join(L) + "\n")

data = dict(
    meta=dict(tree="COLDWAR_SOV_1970_focus", version="design v3 (15.10.2026)",
              note="Generator input. Effects carry k (kind) + params + t (German design text). Leaders: non-exclusive plenum foci + gensec/heir flags."),
    sections=SECTIONS, foci=FOCI, ideas=IDEAS, programmes=PROGS, offers=OFFERS, events=EVENTS, decisions=DECISIONS,
    traits=TRAITS, opinions=OPINIONS, politburo_republics=R.POLITBURO, flags=sorted(FLAGS), gensec=GENSEC, party={i: list(v) for i, v in PARTY.items()}, trig=TRIG,
    concept=dict(spirits=C.START_SPIRITS, laws=C.START_LAWS, factions=C.START_FACTIONS, dynmods=C.DYNMODS, bop=C.BOP, cohesion=C.COHESION,
                 decisions=C.DECISIONS_C, events=C.EVENTS_C, leaders=C.LEADERS_C, no_tree=C.NO_TREE, portraits=C.PORTRAITS, files=C.FILES))
open('/home/claude/sov/sov_tree_full.json', 'w').write(json.dumps(data, ensure_ascii=False, indent=1, default=list))
print(len(FOCI), "foci;", len(L), "lines")
