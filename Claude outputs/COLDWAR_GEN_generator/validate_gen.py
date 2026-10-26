# IMPERIA CW — Cold War: Generic 1970 national focus content generator.
"""COLDWAR | validate the generator output in ./out against the mod (MD style, references, layout, loc, encoding).

python3 validate_gen.py [mod_root]   -> prints errors / warnings, exit code 1 on errors
"""
import sys, os, re, json
from gen_common import *
from gen_load import load_focus_file, simple, abs_positions, parse_fields
from gen_focus import MD_ORDER
from gen_misc import loc_keys

MOD = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/uploads/mdcoldwar'
ERR, WARN = [], []


def err(m): ERR.append(m)
def warn(m): WARN.append(m)


def out(rel):
    return read(os.path.join(OUT, rel))


def balanced(text, name):
    d = 0
    for i, line in enumerate(text.split('\n'), 1):
        line = re.sub(r'"[^"]*"', '""', line.split('#')[0])
        d += line.count('{') - line.count('}')
        if d < 0:
            err(f'{name}:{i}: closing brace without opening')
            return
    if d != 0:
        err(f'{name}: {d} unclosed braces')


def main():
    I = idx()
    sprites = set(I['sprites'])
    md_effects = set(I['effects'])
    md_triggers = set(I['triggers'])
    md_ideas = set(I['ideas'])
    moddefs = set(I['moddefs'])
    ref = json.load(open(os.path.join(IDX_DIR, 'modifier_referenz.json')))['schluessel']
    b, design = load_design()
    design_ids = {P + n['id'] for n in design['nodes']}
    report = json.load(open(os.path.join(OUT, 'build_report.json')))
    md_tt_keys = {k for k in mod_loc_keys(MOD) if k.endswith('_tt')}   # only DEFINED keys
    from gen_effects import COLDWAR_TT

    # ------------------------------------------------ encoding and braces
    for root, _, files in os.walk(OUT):
        for fn in files:
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, OUT)
            if fn.endswith('.json'):
                continue
            raw = open(p, 'rb').read()
            if b'\r' in raw:
                err(f'{rel}: CRLF line ends')
            if fn.endswith('.yml'):
                if not raw.startswith(b'\xef\xbb\xbf'):
                    err(f'{rel}: .yml without BOM')
            elif raw.startswith(b'\xef\xbb\xbf'):
                err(f'{rel}: .txt with BOM')
            text = raw.decode('utf-8-sig')
            if fn.endswith('.txt'):
                balanced(text, rel)
                if not all(ord(c) < 128 for c in text):
                    bad = sorted({c for c in text if ord(c) >= 128})
                    err(f'{rel}: non-ASCII characters in script {bad[:10]}')

    # ------------------------------------------------ focus file
    lf = load_focus_file(OUT)
    foci = {}
    for name, fs in lf['sections']:
        for f in fs:
            if f['id'] in foci:
                err(f'duplicate focus id {f["id"]}')
            foci[f['id']] = dict(f, sec=name, d=simple(f['fields']))
    # field order (MD): groups in MD_ORDER, search_filters before available
    rank = {k: i for i, g in enumerate(MD_ORDER) for k in g}
    for fid, f in foci.items():
        keys = [k for k, _ in f['fields']]
        rs = [rank.get(k, 99) for k in keys]
        if rs != sorted(rs):
            err(f'{fid}: field order not MD ({keys})')
        if f['d']['icon'].startswith('GFX_'):
            err(f'{fid}: icon with GFX_ prefix')
    # references
    for fid, f in foci.items():
        d = f['d']
        for pr in d.get('prerequisite', []):
            for x in re.findall(r'focus = (\S+)', pr):
                if x not in foci:
                    err(f'{fid}: prerequisite {x} missing')
        mx = re.findall(r'focus = (\S+)', d.get('mutually_exclusive', ''))
        for x in mx:
            if x not in foci:
                err(f'{fid}: mutually_exclusive {x} missing')
            elif fid not in re.findall(r'focus = (\S+)', foci[x]['d'].get('mutually_exclusive', '')):
                err(f'{fid}: mutually_exclusive with {x} not symmetric')
        r = d.get('relative_position_id')
        if r and r not in foci:
            err(f'{fid}: relative_position_id {r} missing')
        for x in re.findall(r'has_completed_focus = (\w+)', f['raw']):
            if x not in foci:
                err(f'{fid}: has_completed_focus {x} missing')
    # layout: unique cells, also against the GCC and Union attachments
    F = {fid: dict(x=int(f['d']['x']), y=int(f['d']['y']), rel=f['d'].get('relative_position_id')) for fid, f in foci.items()}
    pos = abs_positions(F)
    from gen_load import shared_footprint
    ext = {}
    ext.update({('GCC', k): v for k, v in shared_footprint(MOD, F_GCC).items()})
    ext.update({('UNI', k): v for k, v in shared_footprint(MOD, F_UNI, (-115, -8)).items()})
    cells = {}
    for k, v in list(pos.items()) + list(ext.items()):
        if v in cells:
            err(f'focus position {v} used twice: {cells[v]} and {k}')
        cells[v] = k
        if v[0] < 0 or v[1] < 0:
            err(f'{k}: negative position {v}')
    occupied = set(cells)
    for fid, f in foci.items():
        cx, cy = pos[fid]
        for pr in f['d'].get('prerequisite', []):
            for x in re.findall(r'focus = (\S+)', pr):
                px, py = pos[x]
                if py >= cy:
                    err(f'{fid}: prerequisite {x} not above it')
                # HOI4 drops the line from the parent, runs across above the child and down into it:
                # check the parent's and the child's column between the two rows
                for col in {px, cx}:
                    for yy in range(py + 1, cy):
                        if (col, yy) in occupied and cells[(col, yy)] not in (fid, x):
                            m = f'{fid}: line from {x} runs behind {cells[(col, yy)]}'
                            (err if fid in design_ids else warn)(m + ('' if fid in design_ids else ' (old block, unchanged)'))
    # contour distance between the GCC / Union attachments and our foci (report only)
    for k, (x, y) in ext.items():
        near = [fid for fid, (a, c) in pos.items() if abs(a - x) <= 1 and abs(c - y) <= 1]
        if near:
            warn(f'{k[0]} attachment {k[1]} at {(x, y)} is next to {near}')

    # ------------------------------------------------ party / trunk foci: content rules
    party_text = ''
    for fid in design_ids:
        f = foci.get(fid)
        if not f:
            err(f'{fid}: missing in the focus file')
            continue
        raw = f['raw']
        party_text += raw + '\n'
        if f'log = "[GetDateText]: [Root.GetName]: Focus {fid}"' not in raw:
            err(f'{fid}: completion_reward without log line')
        if re.search(r'force_update_dynamic_modifier = yes(?!\n\t*mdcw_cw_recalculate_country = yes)', raw):
            err(f'{fid}: force_update_dynamic_modifier outside the Cold War recalculation')
        if '>=' in raw or '<=' in raw:
            err(f'{fid}: >= / <= in a condition')
        if re.search(r'^\t\t\t(increase|decrease)_(military_spending|policing_budget|social_spending|healthcare_budget|education_budget|migration_law|exports) = yes', raw, re.M):
            err(f'{fid}: law helper without guard')
        if 'skip_payment = 1' in raw and 'skip_payment = 0' not in raw:
            err(f'{fid}: skip_payment not reset')
        # temp variable directly before the faction helpers
        lines = [l.strip() for l in raw.split('\n')]
        for i, l in enumerate(lines):
            m = re.match(r'change_(\w+)_opinion = yes', l)
            if m and m.group(1) != 'all_internal_faction':
                j = i - 1
                while j >= 0 and re.match(r'change_\w+_opinion = yes', lines[j]):
                    j -= 1
                if not lines[j].startswith('set_temp_variable = { temp_opinion ='):
                    err(f'{fid}: faction helper without temp_opinion directly before')
        # dynamic modifier lines: header before, variable belongs to the party programme
        for m in re.finditer(r'add_to_variable = \{ (GEN_1970_(\w+?)_(\w+)) = (-?[\d.]+) tooltip = (\w+) \}', raw):
            pass
    # forbidden hooks (skill 4)
    forbidden = ['mdcw_cw_start_opec_vote', 'mdcw_cw_start_oil_embargo', 'mdcw_cw_end_oil_embargo', 'global.mdcw_cw_oil_level',
                 'imp_spike_oil_price', 'imp_oil_price_demand', 'imp_oil_prices_ask', 'mdcw_cw_start_program', 'mdcw_cw_start_pps',
                 'globalism_value', 'imp_eco_1_dynamic_modifier', 'imp_eco_2_dynamic_modifier', 'imp_eco_3_dynamic_modifier',
                 'EU_member', 'set_technology', 'given_bonds@', 'active_subsidies@', 'IMP_1970_apply_starting_gdp_profile',
                 'imp_national_ideas_', 'add_resource', 'global.mdcw_cw_tension =', 'set_leader', 'every_country', 'random_country']
    for fb in forbidden:
        if fb in party_text:
            err(f'forbidden hook {fb} in a party/trunk focus')
    # effects and triggers used by our foci exist
    gen_eff = read(f'{MOD}/{F_EFFECTS}')[0]
    gen_trg = read(f'{MOD}/{F_TRIGGERS}')[0]
    our_eff = set(re.findall(r'^(\w+) = \{', gen_eff, re.M))
    our_trg = set(re.findall(r'^(\w+) = \{', gen_trg, re.M))
    VANILLA = {'has_war', 'always', 'is_ai', 'has_government', 'has_completed_focus', 'has_idea', 'has_variable',
               'force_update_dynamic_modifier'}
    for m in set(re.findall(r'^\t*(\w+) = yes$', party_text, re.M)):
        if m in VANILLA:
            continue
        if m not in md_effects and m not in our_eff and m not in md_triggers and m not in our_trg:
            err(f'unknown effect/trigger {m}')
    for m in set(re.findall(r'(\w+) = (?:yes|no) \}', party_text)):
        if m not in md_triggers and m not in our_trg and m not in md_effects:
            err(f'unknown trigger {m}')
    # MD helpers used must exist (explicit list)
    for h in set(re.findall(r'\b(change_\w+_opinion|increase_\w+|decrease_\w+|one_\w+|two_\w+|three_\w+|modify_\w+_effect|'
                            r'update_literacy_rate|change_relative_party_popularity|mdcw_cw_\w+|GEN_1970_change_\w+) = yes', party_text)):
        if h not in md_effects and h not in our_eff:
            err(f'effect {h} not in the mod')

    # ------------------------------------------------ ideas
    ideas_text = out(F_NEW_IDEAS)[0]
    new_ideas = dict(re.findall(r'^\t\t(GEN_1970_\w+) = \{\n\t\t\tpicture = (\S+)', ideas_text, re.M))
    old_ideas_text = read(f'{MOD}/{F_OLD_IDEAS}')[0]
    old_ideas = set(re.findall(r'^\t\t(GEN_1970_\w+) = \{', old_ideas_text, re.M))
    if set(new_ideas) & old_ideas:
        err(f'ideas defined twice (old and new file): {sorted(set(new_ideas) & old_ideas)}')
    if set(new_ideas) & md_ideas:
        err(f'new idea names clash with mod ideas: {sorted(set(new_ideas) & md_ideas)}')
    for iid, pic in new_ideas.items():
        if f'GFX_idea_{pic}' not in sprites and pic not in [l.strip() for l in open(os.path.join(IDX_DIR, 'idea_gfx.txt'))]:
            err(f'{iid}: picture {pic} not found')
    if len(set(new_ideas.values())) != len(new_ideas):
        warn('a picture is used by two new spirits')
    for m in set(re.findall(r'(?:add_ideas = |idea = |has_idea = |remove_idea = |add_idea = )(\w+)', party_text)):
        if m.startswith(P):
            if m not in new_ideas and m not in old_ideas:
                err(f'idea {m} not defined')
        elif m not in md_ideas:
            err(f'MD idea {m} not in the mod')
    for m in set(re.findall(r'add_ideas = (GEN_1970_\w+)|idea = (GEN_1970_\w+)', party_text)):
        pass
    for k in set(re.findall(r'^\t\t\t\t(\w+) = -?[\d.]+$', ideas_text, re.M)):
        if not (k in moddefs or ref.get(k) or k + '_tt' in md_tt_keys):
            warn(f'idea modifier {k} not confirmed in the index')
    balanced(ideas_text, F_NEW_IDEAS)

    # ------------------------------------------------ party programmes
    dm = out(F_DYNMOD)[0]
    progs = {}
    for name, body in re.findall(r'^(GEN_1970_\w+_programme) = \{(.*?)^\}', dm, re.M | re.S):
        progs[name] = dict(re.findall(r'^\t(\w+) = (GEN_1970_\w+)$', body, re.M))
    for m in re.finditer(r'add_to_variable = \{ (GEN_1970_([a-z]+)_(\w+)) = (-?[\d.]+) tooltip = (\w+) \}', party_text):
        var, p, key, v, tt = m.groups()
        pr = f'{P}{p}_programme'
        if pr not in progs:
            err(f'{var}: programme {pr} missing')
        elif progs[pr].get(key) != var:
            err(f'{var}: key {key} not in {pr}')
    for pr, keys in progs.items():
        for k in keys:
            if not (k in moddefs or ref.get(k) or k + '_tt' in md_tt_keys or k in COLDWAR_TT):
                warn(f'{pr}: modifier {k} not confirmed in the index')
    for pr in set(re.findall(r'MODIFIER = (\w+)', party_text)) | set(re.findall(r'add_dynamic_modifier = \{ modifier = (\w+) \}', party_text)):
        if pr not in progs:
            err(f'dynamic modifier {pr} referenced but not defined')

    # ------------------------------------------------ localisation
    new_loc = out(F_NEW_LOC)[0]
    old_loc = out(F_OLD_LOC)[0]
    shared = out(F_SHARED_TT)[0]
    nk, ok, sk = loc_keys(new_loc), loc_keys(old_loc), loc_keys(shared)
    for name, ks in (('new loc', nk), ('old loc', ok), ('shared tooltips', sk)):
        dup = {k for k in ks if ks.count(k) > 1}
        if dup:
            err(f'{name}: duplicate keys {sorted(dup)[:10]}')
    if set(nk) & set(ok):
        err(f'keys in both the new and the old generic loc: {sorted(set(nk) & set(ok))[:10]}')
    if re.search(r'^ \w+:\d+ "', new_loc, re.M) or re.search(r'^ \w+:\d+ "', shared, re.M):
        err('new loc file uses :0')
    allk = set(nk) | set(ok) | set(sk) | mod_loc_keys(MOD)
    # the shared tooltip file belongs to every COLDWAR tree: no key of the current mod file may get lost
    shared_path = f'{MOD}/{F_SHARED_TT}'
    if os.path.exists(shared_path):
        lost = set(loc_keys(read(shared_path)[0])) - set(sk)
        if lost:
            err(f'shared tooltip file drops keys other trees use: {sorted(lost)[:10]}')
    # tooltip keys of the old domain foci (unchanged blocks): report only
    for t in sorted(set(re.findall(r'tooltip = (\w+) \}', out(F_FOCUS)[0])) - set(re.findall(r'tooltip = (\w+) \}', party_text))):
        if t not in allk:
            warn(f'tooltip {t} (old domain focus) has no loc')
    for fid in foci:
        if fid not in allk or fid + '_desc' not in allk:
            err(f'{fid}: name or description missing in the loc')
    for iid in new_ideas:
        if iid not in allk:
            err(f'{iid}: idea name missing in the loc')
    for t in set(re.findall(r'custom_effect_tooltip = (\w+)', party_text)) | set(re.findall(r'tooltip = (\w+) \}', party_text)):
        if t not in allk:
            err(f'tooltip {t} has no loc')
    for pr in progs:
        if pr not in allk:
            err(f'programme {pr} has no name in the loc')
    for line in new_loc.split('\n'):
        m = re.match(r'^ (\w+): "(.*)"$', line)
        if line.startswith(' ') and not line.strip().startswith('#') and not m:
            err(f'bad loc line: {line[:80]}')
        if m:
            if re.search(r'(?<!\\)"', m.group(2)):
                err(f'unescaped quote in {m.group(1)}')
            if '$' in m.group(2) or '[' in m.group(2):
                err(f'$ or [ in {m.group(1)}')
    for k, v in re.findall(r'^ (\w+): "(.*)"$', new_loc, re.M):
        try:
            v.encode('cp1252')
        except UnicodeEncodeError:
            err(f'{k}: character outside Windows-1252 (missing glyph in game)')
    long = [k for k, v in re.findall(r'^ (\w+_desc): "(.*)"$', new_loc, re.M) if len(v) > 260]
    if long:
        warn(f'{len(long)} focus descriptions longer than 260 characters (design texts, kept as approved)')

    # ------------------------------------------------ icons
    used = {}
    for fid, f in foci.items():
        ic = f['d']['icon']
        if ic not in sprites and 'GFX_' + ic not in sprites:
            err(f'{fid}: icon {ic} not found')
        used.setdefault(ic, []).append(fid)
    for ic, ids in used.items():
        if len(ids) > 1 and any(i in design_ids for i in ids) and any(i in design_ids and not next(
                n for n in design['nodes'] if P + n['id'] == i)['old'] for i in ids):
            err(f'icon {ic} used by {ids}')
        if ic in ('STALIN_PLAN', 'ABMT_1'):
            err(f'photo icon {ic}')
    dup_old = {ic: ids for ic, ids in used.items() if len(ids) > 1}
    if dup_old:
        warn(f'{len(dup_old)} icons used twice already in the old tree (kept): ' + ', '.join(list(dup_old)[:6]))

    # ------------------------------------------------ result
    for w in WARN:
        print('warning', w)
    for e in ERR:
        print('ERROR  ', e)
    print(f'{len(foci)} foci checked, {len(new_ideas)} new ideas, {len(progs)} programmes, '
          f'{len(ERR)} errors, {len(WARN)} warnings')
    sys.exit(1 if ERR else 0)


if __name__ == '__main__':
    main()
