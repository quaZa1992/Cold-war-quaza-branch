# IMPERIA CW — Cold War: West Germany integration from quaZa e45483ff.
"""Player-facing tooltips.

* nice(trigger): wraps every condition the game cannot localise on its own (flags,
  variables, arrays) in custom_trigger_tooltip with a generated English sentence.
* hide_vars(effect): hides raw variable arithmetic so tooltips only show the
  explicit custom_effect_tooltip lines.
"""
import hashlib
import re

from cw_lib import P, L, LOC, VARS, DDR_VARS

NATIVE = ("date ", "date<", "date>", "country_exists", "has_completed_focus", "has_idea", "original_tag",
          "IMP_is_1970_scenario", "always", "tag ", "is_ai", "has_war", "is_in_faction", "has_government", "custom_trigger_tooltip", "has_stability")

PARTY = {1: "the CDU/CSU", 3: "the SPD", 4: "the DKP", 5: "the PDS", 2: "the FDP", 17: "the Greens",
         20: "the Republikaner", 21: "the NPD", 22: "the DVU"}
LEADERS = {"cwger_cdu_leader": {1: "Rainer Barzel", 2: "Helmut Kohl", 3: "Franz Josef Strauß", 4: "Ernst Albrecht",
                                5: "Lothar Späth", 6: "Wolfgang Schäuble"},
           "cwger_spd_leader": {1: "Willy Brandt", 2: "Helmut Schmidt", 3: "Hans-Jochen Vogel", 4: "Johannes Rau",
                                5: "Oskar Lafontaine", 6: "Björn Engholm", 7: "Rudolf Scharping", 8: "Gerhard Schröder"}}
FLAGS = {
    "era2": "the 'Wende' has opened a new political era",
    "un_member": "the Federal Republic is a member of the United Nations",
    "reception_ready": "the reception camps have been expanded",
    "cwgg_crisis_cd": "an inner-German crisis has ended within the last year",
    "unity_achieved": "Germany is united",
    "wall_open": "the Berlin Wall is open",
    "asylum_surge": "the asylum debate is raging",
    "greens_founded": "the Greens have been founded",
    "maastricht_signed": "France has ratified Maastricht",
    "maastricht_failed": "France has rejected Maastricht",
    "chernobyl": "the Chernobyl disaster has happened",
    "munich_happened": "the Munich Olympics attack has happened",
    "krisenstab_models": "the crisis staff has refused to yield to terrorists",
    "nato_crisis": "the Federal Republic has refused the missile deployment",
    "barzel_government": "Rainer Barzel became chancellor by a vote of no confidence",
    "csu_fourth_party": "the CSU has split from the CDU",
    "schmidt_iii": "the FDP has left the coalition and Schmidt governs alone",
    "hostage_crisis_active": "a hostage crisis is under way",
    "deutscher_herbst_over": "the German Autumn is over",
    "wsg_hoffmann_active": "a militant far-right group operates unchecked",
    "soviets_want_neutrality": "Moscow has demanded a neutral Germany",
    "soviets_refused": "Moscow has refused German unity",
    "moscow_coup_succeeded": "hardliners have seized power in Moscow",
    "swing_unlocked": "the Swing has been negotiated",
    "freikauf_unlocked": "prisoner buyouts have been agreed",
    "credit_unlocked": "the billion-mark credit is on the table",
    "berlin_agreement": "the Quadripartite Agreement on Berlin is in force",
    "church_contacts": "church contacts with the East exist",
    "mediation_unlocked": "the Mediation Committee is in use",
    "ban_unlocked": "organisation bans are possible",
    "contact_ban_law": "the Contact Ban Act is in force",
    "kinkel_initiative": "the Kinkel initiative has been launched",
    "export_guidelines": "arms export guidelines exist",
    "deployments_allowed": "armed deployments abroad are allowed",
    "oil_shock_seen": "the first oil shock has hit",
    "foundations_unlocked": "the party foundations work abroad",
    "unity_postponed": "unity talks have stalled",
    "confederation_offered": "a confederation has been offered",
    "art146_prepared": "a new constitution has been drafted",
    "neutrality_accepted": "neutrality is acceptable to Bonn",
    "elections_in_progress": "an election campaign is under way",
    "generic_election_killswitch": "elections have been suspended",
    "mdcw_cw_initialized": "it takes part in the Cold War system",
    "cwgg_kanal_koko_unlocked": "the Schalck-Golodkowski channel is available",
    "cwgg_policy_rapprochement": "Bonn follows Change through Rapprochement",
    "cwgg_policy_strength": "Bonn follows the Policy of Strength",
    "energy_saving": "the energy-saving campaign has been launched",
}
NEG_FLAGS = {
    "cwgg_crisis_cd": "no inner-German crisis has ended within the last year",
    "unity_achieved": "Germany is not yet united",
    "elections_in_progress": "no election campaign is under way",
    "generic_election_killswitch": "elections have not been suspended",
    "soviets_refused": "Moscow has not refused German unity",
    "wall_open": "the Berlin Wall still stands",
}
PLURAL = {17, 20}
STAGES = {"> 0": "the GDR crisis has begun", "< 3": "the inner-German border is still closed",
          "= 9": "the GDR regime has crushed the protests", "> 3": "the GDR is in transition",
          "< 9": "the GDR regime has not crushed the protests"}
EXTRA_VARS = {"cwgg_klima": ("Inner-German climate",), "cwgg_druck": ("Escalation pressure",),
              "cwgg_mob_brd": ("Bundeswehr alert level",), "cwger_raf_prisoners": ("Imprisoned RAF leaders",), "cwger_bka_level": ("BKA level",),
              "cwger_gsg9_tier": ("GSG 9 tier",), "cwsec_hunger": ("Hunger strike",)}
OPS = {">": "above", "<": "below", "=": "exactly", ">=": "at least", "<=": "at most"}


def clauses(s):
    out, i, s = [], 0, s.strip()
    while i < len(s):
        while i < len(s) and s[i] in " \t\n":
            i += 1
        if i >= len(s):
            break
        m = re.match(r"[\w.^@:]+ *(?:[<>]=?|=) *", s[i:])
        if not m:
            raise ValueError("cannot parse trigger: " + s[i:i + 80])
        j = i + m.end()
        if s[j] == "{":
            d = 0
            for k in range(j, len(s)):
                if s[k] == "{":
                    d += 1
                elif s[k] == "}":
                    d -= 1
                    if d == 0:
                        break
            out.append(s[i:k + 1])
            i = k + 1
        else:
            m2 = re.match(r"\S+", s[j:])
            out.append(s[i:j + m2.end()])
            i = j + m2.end()
    return out


def inner(clause):
    return clause[clause.index("{") + 1:clause.rindex("}")]


def fdate(d):
    y, m, dd = d.split(".")
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{int(dd)} {months[int(m) - 1]} {y}"


def flag_text(name):
    key = name[len(P) + 1:] if name.startswith(P + "_") else name
    return FLAGS.get(key, key.replace("_", " "))


def describe(c, neg=False):
    c = c.strip()
    head = c.split("=")[0].split("<")[0].split(">")[0].strip()
    if head == "custom_trigger_tooltip":
        match = re.search(r"\btooltip\s*=\s*(\S+)", c)
        text = LOC[match.group(1)].rstrip(".")
        return ("not " if neg else "") + text
    if head == "NOT":
        parts = clauses(inner(c))
        if len(parts) == 1:
            return describe(parts[0], not neg)
        return "not (" + " and ".join(describe(p) for p in parts) + ")"
    if head in ("OR", "AND"):
        parts = [describe(p, neg) for p in clauses(inner(c))]
        joiner = " or " if (head == "OR") != neg else " and "
        return "(" + joiner.join(parts) + ")" if len(parts) > 1 else parts[0]
    if head == "date":
        m = re.match(r"date *([<>])=? *(\S+)", c)
        after = (m.group(1) == ">") != neg
        return ("after " if after else "before ") + fdate(m.group(2))
    if head == "country_exists":
        tag = c.split("=")[1].strip()
        return f"[{tag}.GetName] {'does not exist' if neg else 'exists'}"
    if head == "has_completed_focus":
        fid = c.split("=")[1].strip()
        name = LOC.get(fid)
        if name is None:
            try:
                import tree
                name = tree.BY_KEY[fid[len(P) + 1:]]["name"]
            except (ImportError, KeyError):
                name = fid
        return f"'{name}' {'is not' if neg else 'is'} completed"
    if head in ("has_country_flag", "has_global_flag"):
        name = c.split("=")[1].strip()
        key = name[len(P) + 1:] if name.startswith(P + "_") else name
        if neg:
            return NEG_FLAGS.get(key, "it is not the case that " + flag_text(name))
        return flag_text(name)
    if head == "is_in_array":
        m = re.search(r"gov_coalition_array = (\d+)", c)
        n = int(m.group(1))
        p = PARTY.get(n, "that party")
        verb = ("are" if n in PLURAL else "is") + (" not" if neg else "")
        return f"{p} {verb} in the federal government"
    if head == "check_variable":
        body = inner(c).strip()
        m = re.match(r"([\w^.@]+) *([<>]=?|=) *(\S+)", body)
        var, op, val = m.groups()
        if var == "ruling_party":
            n = int(val)
            p = PARTY.get(n, "another party")
            if n in PLURAL:
                verb = "do not lead" if neg else "lead"
            else:
                verb = "does not lead" if neg else "leads"
            return f"{p} {verb} the federal government"
        if var in LEADERS:
            who = LEADERS[var].get(int(val), "someone else")
            party = "the Union" if "cdu" in var else "the SPD"
            return f"{who} {'does not lead' if neg else 'leads'} {party}"
        if var == "cwddr_wende_stage":
            t = STAGES.get(f"{op} {val}", f"GDR crisis stage {op} {val}")
            return ("it is not the case that " + t) if neg else t
        if var == "party_pop_array^17":
            return f"the Greens {'poll below' if neg else 'poll above'} {round(float(val) * 100, 1)}%"
        if var == "cwger_parliament_shares^17":
            return f"the Greens {'did not win' if neg else 'won'} more than 5% at the last federal election"
        if var == "cwger_margin":
            return "the government has no majority" if neg else "the government has a Bundestag majority"
        if var == "cwger_raf_gen":
            n = int(val) + 1 if op == ">" else int(val)
            ordinal = {2: "second", 3: "third", 4: "fourth"}.get(n, str(n))
            return f"the RAF has {'not yet ' if neg else ''}reached its {ordinal} generation"
        if var == "cwgg_stufe":
            names = ["modus vivendi", "cool coexistence", "tensions", "crisis", "confrontation", "war danger", "war"]
            n = int(val)
            if op == ">":
                t = f"inner-German relations are worse than {names[n]}"
            elif op == "<":
                t = f"inner-German relations are better than {names[n]}"
            else:
                t = f"inner-German relations are at the stage of {names[n]}"
            return ("not: " + t) if neg else t
        t = rivalry_var_text(var, op, val, neg)
        if t:
            return t
        name = (VARS.get(var) or DDR_VARS.get(var) or EXTRA_VARS.get(var) or (var,))[0]
        o = OPS[op]
        if neg:
            o = {"above": "at most", "below": "at least", "exactly": "not"}.get(o, "not " + o)
        return f"{name} is {o} {val}"
    m = re.match(r"(\w{3}) = \{(.*)\}$", c, re.S)
    if m and m.group(1).isupper():
        sub = " and ".join(describe(p, neg) for p in clauses(m.group(2)))
        if m.group(1) in ("DDR", "GER"):
            return sub
        if sub.startswith("it "):
            return f"[{m.group(1)}.GetName] " + sub[3:]
        return f"[{m.group(1)}.GetName]: {sub}"
    raise ValueError("no description for trigger: " + c)


def _count(op, val, neg):
    """'> 2' -> ('at least', 3) etc. for integer-valued meters."""
    v = int(float(val))
    if op == ">":
        return ("at most", v) if neg else ("at least", v + 1)
    if op == "<":
        return ("at least", v) if neg else ("at most", v - 1)
    return ("not", v) if neg else ("exactly", v)


def rivalry_var_text(var, op, val, neg):
    """Readable text for the inner-German mini-game's variables (also when checked from East Berlin)."""
    import rivalry as rv
    m = re.match(r"cwgg_(d?)hebel_(\w+)$", var)
    if m:
        names = dict((a, b) for a, b, _ in (rv.DLEVERS if m.group(1) else rv.LEVERS))
        who = "East Berlin's" if m.group(1) else "Bonn's"
        w, n = _count(op, val, neg)
        lvl = {"at least": f"level {n} or higher", "at most": f"level {n} or lower", "exactly": f"level {n}", "not": f"not at level {n}"}[w]
        return f"{who} lever §Y{names.get(m.group(2), m.group(2))}§! is at {lvl}"
    m = re.match(r"cwgg_vertrag_(\d+)$", var)
    if m:
        name = rv.TREATIES[int(m.group(1)) - 1][2]
        inforce = (op == "=" and val == "1") != neg
        return f"the §Y{name}§! {'is' if inforce else 'is not'} in force"
    m = re.match(r"cwgg_kanal_(\w+)$", var)
    if m and not var.endswith("unlocked"):
        name = dict((a, b) for a, b, _ in rv.CHANNELS).get(m.group(1), m.group(1))
        open_ = (op == "=" and val == "1") != neg
        return f"the channel §Y{name}§! {'is' if open_ else 'is not'} open"
    if var in ("cwgg_krise_typ", "cwgg_countdown"):
        what = "an inner-German crisis is under way" if var == "cwgg_krise_typ" else "a countdown at the brink is running"
        none = "no inner-German crisis is under way" if var == "cwgg_krise_typ" else "no countdown is running"
        active = (op == ">" and val == "0") or (op == "=" and val != "0")
        return what if active != neg else none
    if var in ("cwgg_init_brd", "cwgg_init_ddr"):
        who = "Bonn" if var.endswith("brd") else "East Berlin"
        w, n = _count(op, val, neg)
        return f"{who} has {w} §Y{n}§! initiative"
    if var in ("cwgg_mob_brd", "cwgg_mob_ddr"):
        who = "the Bundeswehr" if var.endswith("brd") else "the National People's Army"
        w, n = _count(op, val, neg)
        lvl = {"at least": f"§Y{n}§! or higher", "at most": f"§Y{n}§! or lower", "exactly": f"§Y{n}§!", "not": f"other than §Y{n}§!"}[w]
        return f"{who} is on alert level {lvl}"
    if var in ("cwgg_aufm_brd", "cwgg_aufm_ddr"):
        who = "the Bundeswehr" if var.endswith("brd") else "the National People's Army"
        w, n = _count(op, val, neg)
        names = ["peacetime garrisons", "a concentration", "a deployment in force", "a massive deployment"]
        if w == "at least" and 0 < n < 4:
            return f"{who} has at least {names[n]} of troops at the border"
        if w == "at most" and 0 <= n < 4:
            return f"{who} has no more than {names[n]} at the border"
        return f"{who}'s troops at the border: {w} level {n}"
    if var == "cwgg_u_phase":
        names = {0: "no unity talks", 1: "a proposal for unity talks", 2: "unity negotiations", 3: "the unity treaty before the Four Powers",
                 4: "the unity treaty before the parliaments", 5: "unity by treaty"}
        w, n = _count(op, val, neg)
        if w == "at least":
            return "unity talks are under way" if n <= 2 else f"the unity talks have reached {names.get(n, n)}"
        if w == "at most":
            return "the unity talks are not yet complete" if n >= 4 else f"the unity talks are at most at {names.get(n, n)}"
        return f"the state of the unity talks is: {names.get(n, n)}" if w == "exactly" else f"the state of the unity talks is not: {names.get(n, n)}"
    if var == "cwgg_detente_m":
        w, n = _count(op, val, neg)
        return f"détente has lasted {w} §Y{n}§! months without a break"
    if var == "cwgg_klima":
        o = OPS[op] if not neg else {"above": "at most", "below": "at least", "exactly": "not"}[OPS[op]]
        return f"the inner-German climate is {o} §Y{val}§!"
    return None


def native(c):
    c = c.strip()
    return c.startswith(NATIVE)


def tooltip_key(text):
    h = hashlib.md5(text.encode()).hexdigest()[:10]
    return L(f"{P}_trg_{h}", text[0].upper() + text[1:] + ".")


def nice(trigger):
    """Return the trigger with every non-native condition wrapped in a localised tooltip."""
    if not trigger.strip():
        return trigger
    out = []
    for c in clauses(trigger):
        if native(c) or c.startswith("custom_trigger_tooltip"):
            out.append(c)
        else:
            text = describe(c)
            if text.startswith("(") and text.endswith(")"):
                text = text[1:-1]
            out.append(f"custom_trigger_tooltip = {{ tooltip = {tooltip_key(text)} {c} }}")
    return " ".join(out)


VAR_OP = re.compile(r"\b(set_variable|add_to_variable|subtract_from_variable|multiply_variable|divide_variable|clamp_variable)( = \{[^{}]*\})")


def hide_vars(effect):
    """Wrap raw variable arithmetic in hidden_effect (it would show up as raw variable names)."""
    return VAR_OP.sub(lambda m: f"hidden_effect = {{ {m.group(1)}{m.group(2)} }}", effect)
