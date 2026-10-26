# IMPERIA CW — Cold War: Egypt 1970 content generator.
# DSL for the Egypt 1970 focus tree design (Imperia MD Cold War)
# Each effect line is German design text; `backticks` mark real game/mod tokens
# (scripted effects, modifiers, triggers) and are validated against the mod index.

PARTY = {
    0: "National Democratic Party (Western Autocracy)",
    1: "New Wafd (Conservatism)",
    2: "Liberal Socialists (Liberalism)",
    3: "Socialist Labour (Socialism)",
    4: "Egyptian Communist Party (Communist State)",
    7: "Arab Socialist Vanguard (Emerging Autocracy)",
    10: "Al-Azhar Ulema Front (Islamic Kingdom)",
    11: "Islamic Jihad (Caliphate)",
    12: "Muslim Brotherhood",
    13: "Technocratic Presidency (Neutral Autocracy)",
    15: "Infitah Business Circle (Oligarchism)",
    18: "Arab Socialist Union (neutral_Social)",
    19: "Tagammu - Independent Left (Neutral Communism)",
    20: "Young Egypt (Nat. Populism)",
    21: "Revolutionary Command Council (Nat. Fascism)",
    22: "Egyptian Armed Forces (Nat. Autocracy)",
    23: "Royalists - House of Muhammad Ali (Monarchist)",
}
SHORT = {0: "NDP", 1: "New Wafd", 2: "Liberale", 3: "Socialist Labour", 4: "ECP", 7: "Vanguard",
         10: "Azhar-Front", 11: "Islamic Jihad", 12: "Muslimbrüder", 13: "Technokraten", 15: "Infitah-Kreis",
         18: "ASU", 19: "Tagammu", 20: "Young Egypt", 21: "RCC", 22: "Armee", 23: "Royalisten"}
OUTLOOK = {"west": "Western", "emerg": "Emerging", "sala": "Salafist", "na": "Non-Aligned", "nat": "Nationalist"}

FOCI = []
SECTIONS = []


def S(key, title, group, color, desc):
    SECTIONS.append(dict(key=key, title=title, group=group, color=color, desc=desc))


def F(fid, name, sec, pre="", mx="", av="", c=5, e=(), n="", h=0, by=""):
    FOCI.append(dict(id="EGY_1970_" + fid, name=name, sec=sec,
                     pre=[["EGY_1970_" + x.strip() for x in grp.split("|")] for grp in pre.split(",") if grp.strip()],
                     mx=["EGY_1970_" + x.strip() for x in mx.split(",") if x.strip()],
                     av=av, cost=c, eff=list(e), note=n, hist=h, bypass=by))


# ---------- effect helpers ----------
def pp(n):
    return f"PP {n:+d} `add_political_power`"


def stab(p):
    return f"Stabilität {p:+d} % `add_stability`"


def ws(p):
    return f"Kriegsunterstützung {p:+d} % `add_war_support`"


FAC = {"the_military": "Militär", "intelligence_community": "Mukhabarat", "labour_unions": "Gewerkschaften",
       "farmers": "Fellachen (Bauern)", "the_ulema": "Ulema (al-Azhar)", "communist_cadres": "Kader",
       "small_medium_business_owners": "Mittelstand", "landowners": "Großgrundbesitzer",
       "oligarchs": "Oligarchen", "industrial_conglomerates": "Staatskonzerne", "fossil_fuel_industry": "Ölindustrie",
       "defense_industry": "Rüstungsindustrie", "international_bankers": "Banken"}


def fac(f, n):
    return f"{FAC[f]} {n:+d} `EGY_1970_change_{f}_exact` → `change_{f}_opinion`"


def party(i, p, o=None):
    o = p if o is None else o
    return f"{SHORT[i]} {p:+.0f} % Popularität (Outlook {o:+.0f} %) `change_relative_party_popularity`"


def outl(name, p):
    return f"Outlook {name} {p:+.0f} % `change_relative_party_popularity`"


def cost(pct):
    return f"Kosten {pct} % BIP `EGY_1970_pay_gdp_share`"


def credit(pct):
    return f"Kredit +{pct} % BIP Treasury, Schulden +{pct} % BIP `modify_treasury_effect` `modify_debt_effect`"


def st(t):
    return f"Staat: {t} `EGY_1970_state_modifier`"


def ec(t):
    return f"Wirtschaftsmodell: {t} `EGY_1970_economy_modifier`"


def mil(t):
    return f"Streitkräfte: {t} `EGY_1970_armed_forces_modifier`"


def idea(name, t, days=None):
    d = f" ({days} Tage `add_timed_idea`)" if days else " `add_ideas`"
    return f"Idee „{name}“: {t}{d}"


def rp(i, leader=""):
    l = f", Staatschef {leader} `create_country_leader`" if leader else ""
    return f"Regierungspartei → {PARTY[i]} `change_ruling_party_effect`{l}"


def ev(t):
    return f"Event: {t}"


def offer(tag, t):
    return f"Angebot an {tag} (Event, Spieler/KI entscheidet; keine Vorab-Belohnung): {t}"


def infl(tags, p):
    return f"Einfluss {p:+d} % in {tags} `change_influence_percentage`"


def op(tag, n):
    return f"Meinung {tag} {n:+d} `add_opinion_modifier`"


def tech(cat, n=1, b="+50 %"):
    return f"Forschungsbonus {cat} {b} ×{n} `add_tech_bonus`"


def build(state, what, n, helper):
    return f"Gebäude: +{n} {what} in {state} `{helper}` (MD-Helper mit `skip_payment`, BIP-skalierte Kosten)"


def flag(f):
    return f"Flag `{f}`"

PARTY.update({5: "Revolutionary Workers' Councils (Anarchist Communism)", 6: "Misr Party of Order (Emerging Conservative)",
              8: "Islamic Revolutionary Front (Moderate Vilayat)", 9: "Guardians of the Revolution (Vilayat-e Faqih)",
              14: "Independent Notables – al-A'yan (Neutral Conservatism)", 16: "Free Economy Movement (Neutral Libertarian)",
              17: "Friends of the Nile (Neutral Green)"})
SHORT.update({5: "Arbeiterräte", 6: "Misr-Partei", 8: "Islam. Rev.-Front", 9: "Revolutionswächter", 14: "Notabeln",
              16: "Freie Wirtschaft", 17: "Friends of the Nile"})
FAC.update({"wahabi_ulema": "Wahhabitische Ulema", "saudi_royal_family": "Saudische Königsfamilie"})


def pm(key, t):
    return f"Partei-Programm: {t} `EGY_1970_{key}_programme`"


def ptax(n):
    return f"Einkommensteuersatz {n:+d} Pkt. (`pop_change`) `modify_population_tax_rate_effect`"


def ctax(n):
    return f"Unternehmenssteuersatz {n:+d} Pkt. (`corp_change`) `modify_corporate_tax_rate_effect`"


def trade(up=True):
    return "Handelsgesetz eine Stufe offener `increase_exports`" if up else "Handelsgesetz eine Stufe geschlossener `decrease_exports`"


def growth():
    return "Konjunktur eine Stufe besser `increase_economic_growth`"


def prodf(n):
    return f"Produktivität {n:+d} `flat_productivity_change_effect`"


def law(kind, up=True):
    m = {"edu": "education_budget", "health": "healthcare_budget", "social": "social_spending", "police": "policing_budget"}
    if kind == "mil":
        return "Militärbudget +1 Stufe `increase_military_spending`" if up else "Militärbudget −1 Stufe `decrease_military_spending`"
    lab = {"edu": "Bildungsbudget", "health": "Gesundheitsbudget", "social": "Sozialbudget", "police": "Polizeibudget"}[kind]
    return f"{lab} {'+1' if up else '−1'} Stufe `{'increase' if up else 'decrease'}_{m[kind]}`"


def intinv(n):
    return f"Auslandsvermögen {n:+.1f} % BIP (`int_investment_change`) `modify_international_investment_effect`"


def newfac(f, op_):
    return f"Neue Fraktion: {FAC[f]} (Meinung {op_}) `add_ideas` `{f}`"


def treas(p):
    return f"Treasury {p:+.1f} % BIP `modify_treasury_effect`"
