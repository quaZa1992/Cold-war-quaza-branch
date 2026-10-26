# IMPERIA CW — Cold War: Cold War SOV design — d leader sections.
from sov_dsl import *

G_LEAD = "KPdSU & Generalsekretäre"

S("cpsu", "KPdSU: Partei Lenins", G_LEAD, "#c0392b",
  "Partei 4 (Communist State). Gemeinsamer Parteibaum für jeden Generalsekretär: Nomenklatura, Komsomol, Parteibuchumtausch, Artikel 6.", 4)
S("ple", "Das Politbüro: Machtwechsel", G_LEAD, "#7b1e16",
  "Kein Generalsekretär schließt einen anderen aus. Breschnew regiert zum Start. Jeder Politbüro-Fokus baut eine Kandidatur auf und öffnet die Entscheidung "
  "„Convene the Plenum“: Das Politbüro stimmt ab (Generalsekretär 1 Stimme, Moskauer Block 7 nach der Balance, die 3 Republiksitze). Mehrheit setzt den "
  "Kandidaten ein, auch mitten in einem anderen Baum. Der Baum eines Generalsekretärs ist nur offen, solange er regiert (`COLDWAR_SOV_gensec_<name>`); "
  "Erledigtes bleibt, sein Programm-Modifier fällt beim Wechsel weg. Stirbt ein Generalsekretär, wird der in seinem Baum gewählte Erbe zur Abstimmung gestellt.", 4)

LEADER_SEC = [
    ("bre", "Leonid Breschnew", "#a93226",
     "Start-Generalsekretär (1964–1982). Stabilität der Kader, Entspannung aus der Stärke oder Breschnew-Doktrin, Konsum, Rüstung oder Öl, "
     "Personenkult, Gesundheit und Nachfolge."),
    ("kos", "Alexei Kossygin", "#cb4335",
     "Der Premier (bis 1980). Marktsozialismus, kybernetische Planung oder Reform im Plan; Kampf mit dem Parteiapparat, Handel statt Panzer, Tashkent-Diplomatie."),
    ("pod", "Nikolai Podgorny", "#e74c3c",
     "Vorsitzender des Präsidiums (bis 1977 im Amt, lebt bis 1983). Föderale Union oder starkes Präsidium; der Staat über der Partei."),
    ("sus", "Michail Suslow", "#922b21",
     "Hardliner der Ideologie (bis 1982). Ideologische Reinheit oder militanter Internationalismus, moralische statt materieller Anreize, Kampf gegen Peking und Eurokommunismus."),
    ("she", "Alexander Schelepin", "#7b241c",
     "Hardliner der Ordnung: Ex-KGB-Chef, Gewerkschaftsboss, Kopf der „Komsomolzen“ (Politbüro bis April 1975). Disziplin oder Arbeitersozialismus, Säuberung der Breschnew-Leute."),
    ("and", "Juri Andropow", "#641e16",
     "KGB-Chef (Politbüro ab April 1973, lebt bis 1984). Ordnung und Reform oder tschekistischer Staat; Disziplinkampagne, Baumwollaffäre, Ausweg aus Afghanistan."),
    ("gre", "Marschall Andrei Gretschko", "#4d5a2a",
     "General: Verteidigungsminister, Politbüro ab April 1973, stirbt April 1976. Massenarmee oder nuklearer Schild, Generalstab im Politbüro, Waffen für Verbündete."),
    ("ust", "Marschall Dmitri Ustinow", "#5f6b3a",
     "General des Rüstungskomplexes: ZK-Sekretär für Verteidigungsindustrie, Politbüro ab März 1976, lebt bis Dezember 1984. Qualität oder Masse, Raketenmänner, SS-20."),
    ("gro", "Grigori Romanow", "#7e3a2f",
     "Hardliner-Technokrat aus Leningrad (Erster Sekretär ab 1970, Politbüro ab März 1976). Technokratische Härte oder eiserne Disziplin, Wissenschafts-Produktions-Vereinigungen, Flottenstadt Leningrad."),
    ("che", "Konstantin Tschernenko", "#8c4b40",
     "Der Apparatschik (Politbüro ab November 1978, lebt bis März 1985). Kontinuität oder vorsichtige Öffnung, Briefe des Volkes, Schulreform, kranker Mann im Kreml."),
    ("gor", "Michail Gorbatschow", "#b04a3d",
     "Die neue Generation (Politbüro ab Oktober 1980). Beschleunigung oder Glasnost zuerst, Perestroika, neues Denken, Unionsvertrag – und die Frage, wie weit die Reform geht."),
]
for k, n, c, d in LEADER_SEC:
    S(k, f"Generalsekretär: {n}", G_LEAD, c, d, 4)
