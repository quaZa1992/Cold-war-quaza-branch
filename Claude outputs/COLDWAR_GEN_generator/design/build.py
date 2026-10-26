# IMPERIA CW — Cold War: design — build.
"""Merge, lay out, validate and score the party-path design.

python3 build.py            -> validates every parts/*.py, writes design.json + report.txt
python3 build.py parts/x.py -> validates only that file (prints errors/warnings)
"""
import importlib.util, json, sys, glob, os, re
from dsl import KEYS, FACTIONS, BUILD, LAWS, CATS, MD_IDEAS, OUTLOOKS

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- parties (MD index order)
PARTY_META = [
    # key, idx, outlook, party name, trigger, existing ids (entry first)
    ('wa', 0, 'W', 'Western Autocracy', 'western_autocrats_are_in_power'),
    ('con', 1, 'W', 'Conservatism', 'western_conservatism_are_in_power'),
    ('lib', 2, 'W', 'Liberalism', 'western_liberals_are_in_power'),
    ('sd', 3, 'W', 'Social Democracy', 'western_social_democrats_are_in_power'),
    ('cs', 4, 'E', 'Communist State', 'emerging_communist_state_are_in_power'),
    ('ac', 5, 'E', 'Anarchist Communism', 'emerging_anarchist_communism_are_in_power'),
    ('ce', 6, 'E', 'Conservative Emerging', 'emerging_reactionaries_are_in_power'),
    ('ea', 7, 'E', 'Emerging Autocracy', 'emerging_autocracy_are_in_power'),
    ('mvf', 8, 'E', 'Moderate Vilayat-e Faqih', 'emerging_moderate_shiite_are_in_power'),
    ('vf', 9, 'E', 'Vilayat-e Faqih', 'emerging_hardline_shiite_are_in_power'),
    ('sk', 10, 'S', 'Salafist Kingdom', 'salafist_kingdom_are_in_power'),
    ('cal', 11, 'S', 'Caliphate', 'salafist_caliphate_are_in_power'),
    ('mb', 12, 'N', 'Muslim Brotherhood', 'neutrality_neutral_muslim_brotherhood_are_in_power'),
    ('na', 13, 'N', 'Neutral Autocracy', 'neutrality_neutral_autocracy_are_in_power'),
    ('ncon', 14, 'N', 'Neutral Conservatism', 'neutrality_neutral_conservatism_are_in_power'),
    ('oli', 15, 'N', 'Oligarchism', 'neutrality_neutral_oligarch_are_in_power'),
    ('nlib', 16, 'N', 'Neutral Libertarianism', 'neutrality_neutral_libertarians_are_in_power'),
    ('gr', 17, 'N', 'Neutral Green', 'neutrality_neutral_green_are_in_power'),
    ('ns', 18, 'N', 'Neutral Social', 'neutrality_neutral_social_are_in_power'),
    ('nc', 19, 'N', 'Neutral Communism', 'neutrality_neutral_communism_are_in_power'),
    ('rwp', 20, 'R', 'Right-Wing Populism', 'nationalist_right_wing_populists_are_in_power'),
    ('fas', 21, 'R', 'Fascism', 'nationalist_fascist_are_in_power'),
    ('jun', 22, 'R', 'Military Junta', 'nationalist_military_junta_are_in_power'),
    ('mon', 23, 'R', 'Monarchism', 'nationalist_monarchists_are_in_power'),
]
META = {m[0]: dict(key=m[0], idx=m[1], outlook=m[2], party=m[3], trigger=m[4]) for m in PARTY_META}
OUTLOOK_GOV = {'W': ('a_western_government', 'democratic'), 'E': ('a_revolutionary_government', 'communism'),
               'S': ('an_islamic_government', 'fascism'), 'N': ('a_non_aligned_government', 'neutrality'),
               'R': ('a_national_government', 'nationalist')}

# ---------------------------------------------------------------- template
#        slot: (dx, dy, cost, prerequisite groups (AND of OR), mx partner, role)
SLOTS = {
    'E':   (0, 0, 5,    [],                 None, 'entry'),
    'POL': (-2, 1, 5,   [['E']],            None, 'hub'),
    'ECO': (2, 1, 5,    [['E']],            None, 'hub'),
    'A1':  (-3, 2, 7.2, [['POL']],          'A2', 'choice'),
    'A2':  (-1, 2, 7.2, [['POL']],          'A1', 'choice'),
    'B1':  (1, 2, 7.2,  [['ECO']],          'B2', 'choice'),
    'B2':  (3, 2, 7.2,  [['ECO']],          'B1', 'choice'),
    'A1f': (-3, 3, 8.6, [['A1']],           None, 'follow'),
    'A2f': (-1, 3, 8.6, [['A2']],           None, 'follow'),
    'B1f': (1, 3, 8.6,  [['B1']],           None, 'follow'),
    'B2f': (3, 3, 8.6,  [['B2']],           None, 'follow'),
    'PM':  (-2, 4, 5,   [['A1f', 'A2f']],   None, 'merge'),
    'EM':  (2, 4, 5,    [['B1f', 'B2f']],   None, 'merge'),
    'C1':  (-3, 5, 7.2, [['PM']],           'C2', 'choice'),
    'C2':  (-1, 5, 7.2, [['PM']],           'C1', 'choice'),
    'D1':  (1, 5, 7.2,  [['EM']],           'D2', 'choice'),
    'D2':  (3, 5, 7.2,  [['EM']],           'D1', 'choice'),
    'CM':  (-2, 6, 8.6, [['C1', 'C2']],     None, 'payoff'),
    'DM':  (2, 6, 8.6,  [['D1', 'D2']],     None, 'payoff'),
    'CAP': (0, 7, 10,   [['CM'], ['DM']],   None, 'capstone'),
}
TSLOTS = {
    'T0':  (0, 0, 7.2, [],              None, 'champion'),
    'T1a': (-1, 1, 5,  [['T0']],        'T1b', 'choice'),
    'T1b': (1, 1, 5,   [['T0']],        'T1a', 'choice'),
    'T2':  (0, 2, 8.6, [['T1a', 'T1b']], None, 'majority'),
    'T3':  (0, 3, 2,   [],              None, 'government'),
}
# net points (gain - price) by cost, house bands of 19.10.2026 (DBR): 2 -> 1.5-3.5, 5 -> 3.5-6.5, 7 -> 4-7.5, 10 -> 6-11
COST_BANDS = {2: (1.5, 3.5), 5: (3.5, 6.5), 7.2: (4.0, 7.5), 8.6: (5.0, 9.0), 10: (6.0, 11.0)}
POWER_ROLES = ('entry', 'government')          # taking power may exceed the band by 3 points
def band(cost, role):
    lo, hi = COST_BANDS[cost]
    return (lo, hi + 3) if role in POWER_ROLES else (lo, hi)
BANDS = {}  # kept for compatibility
PP_VALUES = (50, 75, 100, 150)
# per-focus size limits for Cold War / Imperia keys: key -> (programme line max, idea line max)
CW_CAPS = {'mdcw_cw_ideological_defence': (0.10, 0.30), 'mdcw_cw_support_effectiveness': (0.10, 0.25),
           'mdcw_cw_assistance_limit': (0.25, 0.50), 'mdcw_cw_assistance_capacity': (1, 2),
           'mdcw_cw_market_exposure': (0.10, 0.25), 'mdcw_cw_military_programme_cost': (0.15, 0.25),
           'imp_sanction_resistance': (0.10, 0.15), 'globalism_equilibrium': (5, 15), 'imp_oil_price_resistance': (0.10, 0.20)}
# programme totals on the richest path (warning above)
PROG_CAPS = {'stability_factor': 0.20, 'political_power_factor': 0.35, 'research_speed_factor': 0.12,
             'war_support_factor': 0.25, 'drift_defence_factor': 0.60, 'production_speed_buildings_factor': 0.30,
             'conscription_factor': 0.15, 'industrial_capacity_factory': 0.15, 'tax_gain_multiplier_modifier': 0.20,
             'mdcw_cw_ideological_defence': 0.50}

BAND_ROW = 0            # politics stays on floor 1 (rows 0-11); domain blocks move to floor 2
PARTY_GAP = 9           # entry to entry inside an outlook: 7 wide + contour gap 3 (house rule W3)
OUTLOOK_GAP = 10        # last entry of one outlook to first entry of the next: contour gap 4 (W3)
FIRST_ENTRY_X = 17      # government block x 0-9, block gap 4 (W3), half party width 3 -> first entry at x 17


# ---------------------------------------------------------------- scoring
def line_pts(key, v):
    lab, kind, typ, sign = KEYS[key]
    if sign == 0:
        return abs(v) / typ * 0.5          # globalism: double-edged, small credit
    return v / typ * sign


def fx_pts(e, own_outlook):
    t = e[0]
    if t == 'prog':
        return line_pts(e[1], e[2])
    if t in ('idea',):
        return sum(line_pts(k, v) for k, v in e[2].items())
    if t == 'timed':
        f = max(0.33, min(1.0, e[2] / 1095))
        return sum(line_pts(k, v) for k, v in e[3].items()) * f
    if t == 'swap':
        return None                          # resolved by caller (needs old idea)
    if t == 'mdidea':
        return MD_IDEAS[e[1]][1]
    if t == 'mdtimed':
        return MD_IDEAS[e[1]][1] * max(0.33, min(1.0, e[2] / 1095))
    if t == 'pp':
        return e[1] / 50
    if t == 'stab':
        return e[1] / 0.02
    if t == 'ws':
        return e[1] / 0.03
    if t == 'fac':
        return e[2] / 10 * (2 if e[1] == 'all' else 1)
    if t == 'pop':
        return e[1] / 0.04
    if t == 'outlook':
        return (e[2] / 0.04) if e[1] == own_outlook else (-e[2] / 0.04 * 0.5)
    if t == 'build':
        return 1.5 * BUILD[e[1]][1]
    if t == 'money':
        return e[1] / 0.005
    if t == 'debt':
        return -e[1] / 0.01
    if t == 'tech':
        return e[2] * e[3] / 0.33 * 0.75 * (len(e[1]) ** 0.5)
    if t == 'xp':
        return e[2] / 25
    if t == 'law':
        return 0.0
    if t == 'corruption':
        return -2.0 * e[1]
    if t == 'corruption_chance':
        return -1.0
    if t == 'tension':
        return -0.4 * e[1]
    if t == 'literacy':
        return e[1] / 0.025
    if t == 'growth':
        return 2.0 * e[1]
    return 0.0


def is_price(e, pts):
    return (pts is not None and pts < -0.05) or e[0] in ('law', 'corruption_chance') or \
        (e[0] in ('idea', 'timed', 'swap') and any(line_pts(k, v) < 0 for k, v in (e[3] if e[0] == 'timed' else e[2] if e[0] == 'idea' else e[3]).items()))


# ---------------------------------------------------------------- loading
def load(path):
    spec = importlib.util.spec_from_file_location(os.path.basename(path)[:-3], path)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, HERE)
    spec.loader.exec_module(m)
    return getattr(m, 'PARTIES', []), getattr(m, 'TRUNKS', [])


def current_ids():
    try:
        return set(json.load(open(os.path.join(HERE, 'current_tree.json'))).keys())
    except Exception:
        return set()


# ---------------------------------------------------------------- validation
def check_fx(e, where, err):
    t = e[0]
    def keys_ok(mods):
        for k, v in mods.items():
            if k not in KEYS:
                err.append(f'{where}: unknown modifier key {k}')
            if not isinstance(v, (int, float)):
                err.append(f'{where}: value of {k} not a number')
    if t == 'prog':
        if e[1] not in KEYS: err.append(f'{where}: unknown programme key {e[1]}')
    elif t == 'idea':
        keys_ok(e[2])
        if not 2 <= len(e[2]) <= 6: err.append(f'{where}: idea {e[1]} should have 2-6 lines')
    elif t == 'timed':
        keys_ok(e[3])
        if not 90 <= e[2] <= 1825: err.append(f'{where}: timed idea days {e[2]} outside 90-1825')
    elif t == 'swap':
        keys_ok(e[3])
    elif t in ('mdidea', 'mdtimed'):
        if e[1] not in MD_IDEAS: err.append(f'{where}: unknown MD idea {e[1]}')
    elif t == 'fac':
        if e[1] not in FACTIONS: err.append(f'{where}: unknown faction {e[1]}')
        if abs(e[2]) > 25: err.append(f'{where}: faction change {e[2]} too big')
    elif t == 'build':
        if e[1] not in BUILD: err.append(f'{where}: unknown building helper {e[1]}')
    elif t == 'law':
        if e[1] not in LAWS: err.append(f'{where}: unknown law helper {e[1]}')
    elif t == 'tech':
        for c in e[1]:
            if c not in CATS: err.append(f'{where}: unknown tech category {c}')
        if e[2] > 1.0 or e[3] > 3: err.append(f'{where}: tech bonus too big')
    elif t == 'outlook':
        if e[1] not in OUTLOOKS: err.append(f'{where}: unknown outlook {e[1]}')
    elif t == 'xp':
        if e[1] not in ('army', 'air', 'navy'): err.append(f'{where}: xp kind {e[1]}')
    elif t == 'pp':
        if e[1] > 150: err.append(f'{where}: PP {e[1]} above 150')
    elif t in ('stab', 'ws'):
        if abs(e[1]) > 0.10: err.append(f'{where}: {t} {e[1]} above 10 %')
    elif t in ('pop',):
        if abs(e[1]) > 0.10: err.append(f'{where}: popularity {e[1]} above 0.10')
    elif t in ('money', 'debt'):
        if abs(e[1]) > 0.04: err.append(f'{where}: money/debt {e[1]} above 4 % GDP')
    elif t in ('corruption', 'corruption_chance', 'tension', 'literacy', 'growth', 'flag', 'note'):
        pass
    else:
        err.append(f'{where}: unknown effect type {t}')


def score_focus(f, ideas, own_outlook):
    gain = price = 0.0
    has_price = False
    for e in f['fx']:
        if e[0] == 'swap':
            old = ideas.get(e[1], {})
            p = sum(line_pts(k, v) for k, v in e[3].items()) - sum(line_pts(k, v) for k, v in old.items())
            neg = any(line_pts(k, v) < 0 for k, v in e[3].items())
        else:
            p = fx_pts(e, own_outlook)
            neg = False
        if p is None:
            p = 0
        if p >= 0:
            gain += p
        else:
            price += -p
        if neg or is_price(e, p):
            has_price = True
        if e[0] == 'idea':
            ideas[e[1]] = e[2]
        if e[0] == 'swap':
            ideas[e[2]] = e[3]
    return round(gain, 2), round(price, 2), has_price


def validate_unit(kind, unit, slots, prefix, own_outlook, err, warn, ids, names):
    foci = unit['foci']
    missing = [s for s in slots if s not in foci]
    extra = [s for s in foci if s not in slots]
    if missing: err.append(f'{prefix}: missing slots {missing}')
    if extra: err.append(f'{prefix}: unknown slots {extra}')
    ideas = {}
    stats = {}
    pp_foci = 0
    for s in slots:
        if s not in foci:
            continue
        f = foci[s]
        where = f'{prefix}.{s} ({f["id"]})'
        if f['id'] in ids: err.append(f'{where}: duplicate id')
        ids.add(f['id'])
        if f['name'] in names: warn.append(f'{where}: duplicate name {f["name"]}')
        names.add(f['name'])
        if len(f['name']) > 42: warn.append(f'{where}: name longer than 42 characters')
        if len(f.get('why', '')) < 50: err.append(f'{where}: "why" (historical justification) missing or too short')
        if kind == 'party' and not f['id'].startswith(unit['key'] + '_'): err.append(f'{where}: id must start with {unit["key"]}_')
        if f.get('old') and CUR and ('GEN_1970_' + f['id']) not in CUR:
            err.append(f'{where}: marked old but not in the current tree')
        real = [e for e in f['fx'] if e[0] not in ('note', 'flag')]
        if len(real) < 2: err.append(f'{where}: needs at least 2 real effects (has {len(real)})')
        for e in f['fx']:
            check_fx(e, where, err)
            if e[0] in ('idea', 'timed') and not e[1].startswith(unit.get('key', unit.get('outlook', '')).lower() + '_') and kind == 'party':
                err.append(f'{where}: idea id {e[1]} must start with {unit["key"]}_')
        role = slots[s][5]
        if any(e[0] == 'pp' for e in f['fx']):
            pp_foci += 1
            if all(e[0] in ('pp', 'note', 'flag') for e in f['fx']): err.append(f'{where}: PP-only focus')
            if role == 'capstone': err.append(f'{where}: no PP on a capstone')
            for e in f['fx']:
                if e[0] == 'pp' and e[1] not in PP_VALUES: err.append(f'{where}: PP {e[1]} not in 50/75/100/150')
        st_sum = sum(e[1] for e in f['fx'] if e[0] == 'stab')
        if st_sum > 0.06 + 1e-9 and role != 'capstone': err.append(f'{where}: one-off stability {st_sum:+.2f} above +6 %')
        for e in f['fx']:
            if e[0] == 'xp' and not 15 <= e[2] <= 50: err.append(f'{where}: XP {e[2]} outside 15-50')
            if e[0] == 'fac':
                if e[1] == 'all' and abs(e[2]) > 5: err.append(f'{where}: all factions {e[2]} beyond +-5')
                elif e[1] != 'all' and e[2] > 10: err.append(f'{where}: faction {e[1]} {e[2]:+d} above +10')
                elif e[2] < -25: err.append(f'{where}: faction {e[1]} {e[2]} below -25')
                elif e[1] != 'all' and e[2] not in (5, 10, -5, -10, -15, -20, -25): warn.append(f'{where}: faction {e[1]} {e[2]:+d} not a house value (5/10, -5..-25)')
            if e[0] in ('prog', 'idea', 'timed', 'swap'):
                mods = {e[1]: e[2]} if e[0] == 'prog' else (e[3] if e[0] in ('timed', 'swap') else e[2])
                for k, v in mods.items():
                    if k in CW_CAPS:
                        cap = CW_CAPS[k][0 if e[0] == 'prog' else 1]
                        if abs(v) > cap + 1e-9: err.append(f'{where}: {k} {v} above the per-focus size {cap}')
        if sum(1 for e in f['fx'] if e[0] == 'prog') > 6: warn.append(f'{where}: more than 6 programme lines')
        g, p, hp = score_focus(f, ideas, own_outlook)
        if any(e[0] == 'money' and e[1] > 0 for e in f['fx']):
            others = [e for e in f['fx'] if not (e[0] == 'money' and e[1] > 0)]
            if not any(is_price(e, fx_pts(e, own_outlook) if e[0] != 'swap' else 0) for e in others):
                err.append(f'{where}: money gain without a political price in the same focus')
        lo, hi = band(slots[s][2], role)
        net = g - p
        stats[s] = dict(gain=g, price=p, net=round(net, 2), has_price=hp)
        if net < lo - 0.01: warn.append(f'{where}: net {net:.1f} below band {lo}-{hi} ({role})')
        if net > hi + 0.01: warn.append(f'{where}: net {net:.1f} above band {lo}-{hi} ({role})')
        if role == 'capstone' and not any(e[0] in ('idea', 'swap') for e in f['fx']) and \
                sum(BUILD[e[1]][1] for e in f['fx'] if e[0] == 'build') < 2:
            err.append(f'{where}: capstone needs a national spirit (idea/swap) or 2+ buildings')
    # choices
    for s, (dx, dy, c, pre, mx, role) in slots.items():
        if mx and s < mx and s in stats and mx in stats:
            a, b = stats[s], stats[mx]
            for side, st in ((s, a), (mx, b)):
                if not st['has_price']: err.append(f'{prefix}.{side}: choice side without a visible price')
                if st['gain'] < 3: err.append(f'{prefix}.{side}: choice side gain {st["gain"]} below 3 points')
            if abs(a['net'] - b['net']) > 1.5 + 1e-9:
                warn.append(f'{prefix}.{s}/{mx}: sides unbalanced (net {a["net"]} vs {b["net"]}, max gap 1.5)')
            def keys_of(f):
                ks = set()
                for e in f['fx']:
                    if e[0] == 'prog': ks.add(e[1])
                    elif e[0] == 'idea': ks |= set(e[2])
                    elif e[0] in ('timed', 'swap'): ks |= set(e[3])
                return ks
            shared = keys_of(foci[s]) & keys_of(foci[mx])
            if len(shared) > 1: warn.append(f'{prefix}.{s}/{mx}: sides share {len(shared)} modifier keys {sorted(shared)} (max 1)')
            if any(e[0] == 'pp' for e in foci[s]['fx']) and any(e[0] == 'pp' for e in foci[mx]['fx']):
                err.append(f'{prefix}.{s}/{mx}: PP on both sides of a choice')
    if kind == 'party':
        if pp_foci > 2: err.append(f'{prefix}: {pp_foci} foci give PP (house max 2 per party tree)')
        assets = sum(1 for f in foci.values() for e in f['fx'] if e[0] in ('build', 'tech', 'xp', 'idea', 'swap', 'mdidea'))
        if assets < 4: warn.append(f'{prefix}: only {assets} lasting assets (buildings/tech/xp/ideas), aim for 4+')
        # programme totals on the richest path
        tot = {}
        def add(slot, sign=1):
            for e in foci.get(slot, {}).get('fx', []):
                if e[0] == 'prog':
                    tot.setdefault(e[1], []).append((slot, e[2]))
        for s in slots: add(s)
        for k, cap in PROG_CAPS.items():
            vals = dict(tot.get(k, []))
            best = 0
            for pair in (('A1', 'A1f', 'A2', 'A2f'), ('B1', 'B1f', 'B2', 'B2f'), ('C1', None, 'C2', None), ('D1', None, 'D2', None)):
                x = vals.get(pair[0], 0) + (vals.get(pair[1], 0) if pair[1] else 0)
                y = vals.get(pair[2], 0) + (vals.get(pair[3], 0) if pair[3] else 0)
                best += max(x, y)
            best += sum(v for sl, v in vals.items() if sl in ('E', 'POL', 'ECO', 'PM', 'EM', 'CM', 'DM', 'CAP'))
            if best > cap + 1e-9: warn.append(f'{prefix}: programme {k} reaches {best:.2f} on the richest path (cap {cap})')
    return stats


CUR = current_ids()


def run(paths):
    err, warn, ids, names = [], [], set(), set()
    parties, trunks = [], []
    for p in paths:
        P, T = load(p)
        for x in P: x['_file'] = os.path.basename(p)
        for x in T: x['_file'] = os.path.basename(p)
        parties += P
        trunks += T
    out_parties = []
    for u in parties:
        if u.get('key') not in META:
            err.append(f'{u.get("_file")}: unknown party key {u.get("key")}'); continue
        m = META[u['key']]
        for fld in ('identity', 'history'):
            if len(u.get(fld, '')) < 40: err.append(f'{u["key"]}: party "{fld}" missing/short')
        st = validate_unit('party', u, SLOTS, u['key'], m['outlook'], err, warn, ids, names)
        if u['foci'].get('E', {}).get('id') and CUR:
            cur_entries = {'GEN_1970_' + u['foci']['E']['id']}
            if not (cur_entries & CUR): err.append(f'{u["key"]}.E: entry must keep its existing id')
        out_parties.append((u, st))
    out_trunks = []
    for t in trunks:
        st = validate_unit('trunk', t, TSLOTS, 'trunk_' + t['outlook'], t['outlook'], err, warn, ids, names)
        out_trunks.append((t, st))
    return out_parties, out_trunks, err, warn


def layout(parties, trunks):
    """absolute positions in the political band"""
    pos = {}
    by_o = {o: sorted([p for p, _ in parties if META[p['key']]['outlook'] == o], key=lambda p: META[p['key']]['idx'])
            for o in OUTLOOKS}
    # also place outlooks that have no party file yet (keep spacing stable)
    x = FIRST_ENTRY_X
    centres = {}
    for o in OUTLOOKS:
        keys = [k for k, mm in META.items() if mm['outlook'] == o]
        keys.sort(key=lambda k: META[k]['idx'])
        first = x
        for i, k in enumerate(keys):
            ex = x + i * PARTY_GAP
            pos[('party', k)] = ex
        last = x + (len(keys) - 1) * PARTY_GAP
        centres[o] = (first + last) / 2
        x = last + OUTLOOK_GAP
    return pos, centres


def emit(parties, trunks, err, warn):
    pos, centres = layout(parties, trunks)
    nodes = []
    def fx_out(f, own_outlook, ideas):
        return [list(e) if not isinstance(e[-1], dict) else list(e) for e in f['fx']]
    for t, st in trunks:
        cx = int(round(centres[t['outlook']]))
        for s, (dx, dy, cost, pre, mx, role) in TSLOTS.items():
            f = t['foci'].get(s)
            if not f: continue
            nodes.append(dict(grp='trunk', o=t['outlook'], party=None, slot=s, role=role, id=f['id'], name=f['name'],
                              x=cx + dx, y=BAND_ROW + dy, cost=cost, old=f.get('old', False), why=f['why'],
                              pre=[[t['foci'][q]['id'] for q in g if q in t['foci']] for g in pre],
                              mx=[t['foci'][mx]['id']] if mx and mx in t['foci'] else [],
                              fx=f['fx'], st=st.get(s)))
    for u, st in parties:
        m = META[u['key']]
        ex = pos[('party', u['key'])]
        gov = OUTLOOK_GOV[m['outlook']][0]
        for s, (dx, dy, cost, pre, mx, role) in SLOTS.items():
            f = u['foci'].get(s)
            if not f: continue
            pr = [[u['foci'][q]['id'] for q in g if q in u['foci']] for g in pre]
            if s == 'E':
                pr = []          # W1 (19.10.2026): no line into a party tree, opens via available only
            nodes.append(dict(grp='party', o=m['outlook'], party=u['key'], slot=s, role=role, id=f['id'], name=f['name'],
                              x=ex + dx, y=BAND_ROW + 4 + dy, cost=cost, old=f.get('old', False), why=f['why'],
                              pre=pr, mx=[u['foci'][mx]['id']] if mx and mx in u['foci'] else [],
                              fx=f['fx'], st=st.get(s)))
    party_info = [dict(key=u['key'], idx=META[u['key']]['idx'], o=META[u['key']]['outlook'], party=META[u['key']]['party'],
                       trigger=META[u['key']]['trigger'], identity=u['identity'], history=u['history'],
                       title=u.get('title', META[u['key']]['party']), x=pos[('party', u['key'])])
                  for u, _ in parties]
    trunk_info = [dict(o=t['outlook'], title=t.get('title', ''), note=t.get('note', ''), x=int(round(centres[t['outlook']])))
                  for t, _ in trunks]
    return dict(nodes=nodes, parties=party_info, trunks=trunk_info, errors=err, warnings=warn)


if __name__ == '__main__':
    paths = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, 'parts', '*.py')))
    parties, trunks, err, warn = run(paths)
    for e in err: print('ERROR  ', e)
    for w in warn: print('warning', w)
    print(f'{len(parties)} parties, {len(trunks)} trunks, {sum(len(u["foci"]) for u, _ in parties)} party foci, '
          f'{len(err)} errors, {len(warn)} warnings')
    if len(sys.argv) == 1:
        d = emit(parties, trunks, err, warn)
        json.dump(d, open(os.path.join(HERE, 'design.json'), 'w'), indent=1, ensure_ascii=False)
        print('design.json written')
