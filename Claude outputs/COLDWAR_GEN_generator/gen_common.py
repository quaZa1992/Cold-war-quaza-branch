# IMPERIA CW — Cold War: Generic 1970 national focus content generator.
"""COLDWAR | generic 1970 tree - party paths generator: shared constants and helpers.

Usage: python3 gen_build.py <mod_root>   (reads the current mod files, writes ./out/<mod path>)
Values Enes may want to tune after testing are constants in this file.
"""
import os, sys, json, re, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'out')
IDX_DIR = os.path.join(HERE, 'index')
DESIGN_DIR = os.path.join(HERE, 'design')

P = 'GEN_1970_'                     # id prefix of the generic tree (kept: the tree and its ids already exist)
TREE_ID = 'mdcw_1970_generic_focus'

# ---------------------------------------------------------------- mod paths (relative to the mod root)
F_FOCUS = 'common/national_focus/mdcw_1970_generic_focus.txt'
F_DYNMOD = 'common/dynamic_modifiers/mdcw_1970_generic_party_programmes.txt'
F_OLD_LOC = 'localisation/english/mdcw_1970_generic_focus_l_english.yml'
F_OLD_IDEAS = 'common/ideas/mdcw_1970_generic_focus_ideas.txt'
F_EFFECTS = 'common/scripted_effects/mdcw_1970_generic_focus_effects.txt'
F_TRIGGERS = 'common/scripted_triggers/mdcw_1970_generic_focus_triggers.txt'
F_GCC = 'common/national_focus/COLDWAR_GCC_1970_shared.txt'
F_UNI = 'common/national_focus/COLDWAR_UNI_1970_union_joint.txt'
F_MD_TT = 'localisation/english/MD_dm_modifiers_l_english.yml'
# new files (ours)
F_NEW_IDEAS = 'common/ideas/COLDWAR_GEN_1970_party_ideas.txt'
F_NEW_LOC = 'localisation/english/COLDWAR_GEN_1970_party_paths_l_english.yml'
F_SHARED_TT = 'localisation/english/COLDWAR_modifier_tooltips_l_english.yml'

# ---------------------------------------------------------------- layout (house rules W1-W3 of 19.10.2026)
FIRST_ENTRY_X = 19      # first party entry; leaves columns 32-33 free for the GCC attachment root at (32, 11)
PARTY_ROW = 4           # party entries; trunk rows 0-3, party trees rows 4-11 (floor 1)
FLOOR2_ROW = 13         # domain blocks (foreign policy ... navy) on floor 2, rows 13-20
FLOOR2_X = 40           # first domain block; x 26-36 rows 11-15 stay free for the GCC attachment
BLOCK_GAP = 4           # contour gap between domain blocks (W3)
CONTINUOUS_FOCUS_POSITION = (50, 1700)   # pixels: below the government block, left of the GCC attachment
DOMAIN_ORDER = ['Foreign Policy', 'Economic System', 'Development', 'Industry and Energy',
                'Society and Science', 'Army', 'Air Force', 'Navy']
POLITICAL_SECTIONS = {'W': 'Western Outlook', 'E': 'Emerging Outlook', 'S': 'Salafist Outlook',
                      'N': 'Non-Aligned Outlook', 'R': 'Nationalist Outlook'}

# ---------------------------------------------------------------- economy
# building price as GDP share: MD fixed price (bn) x BUILD_PRICE_PER_BN; a civilian factory (7.5 bn) = 1 % of GDP
BUILD_PRICE_PER_BN = 0.01 / 7.5

# ---------------------------------------------------------------- AI
AI_BASE_NEW = 25        # same weight the old generic tree gave its party and outlook foci
AI_OVERRIDE = {'vf_export_the_revolution': 5}   # capstone: rare for the AI (old tree: 0)
# old ids keep their old AI base (e.g. 0 on ac_cultural_revolution / cal_the_holy_war: the AI takes the other side),
# except party entries, which always get AI_BASE_NEW so that the AI can open its party tree

# ---------------------------------------------------------------- outlooks: MD party index range (end exclusive), government
OUTLOOK_RANGE = {'W': (0, 4), 'E': (4, 10), 'S': (10, 12), 'N': (12, 20), 'R': (20, 24)}
OUTLOOK_LABEL = {'W': 'Western', 'E': 'Emerging', 'S': 'Salafist', 'N': 'Non-Aligned', 'R': 'Nationalist'}
OUTLOOK_GOV = {'W': 'democratic', 'E': 'communism', 'S': 'fascism', 'N': 'neutrality', 'R': 'nationalist'}
CHAMPIONS = {'W': 'champion_western', 'E': 'champion_emerging', 'S': 'champion_salafist',
             'N': 'champion_non_aligned', 'R': 'champion_nationalist'}

# religion gates (as the old generator): allow_branch on these design ids
ALLOW_BRANCH = {
    'champion_salafist': 'salafist_path_allowed', 'an_islamic_government': 'salafist_path_allowed',
    'sk': 'salafist_path_allowed', 'cal': 'salafist_path_allowed',
    'mvf': 'shia_path_allowed', 'vf': 'shia_path_allowed', 'mb': 'muslim_brotherhood_allowed',
}

T = '\t'

_LOC_KEYS = {}


def mod_loc_keys(mod_root):
    """every loc key DEFINED in the mod's English localisation (MD's files included), without our own generated files.
    A <modifier>_tt that MD's trees merely use is not enough: 12 of them are defined nowhere (e.g. research_speed_factor_tt)."""
    if mod_root not in _LOC_KEYS:
        import glob
        own = {os.path.basename(F_NEW_LOC), os.path.basename(F_SHARED_TT)}
        keys = set()
        for f in sorted(glob.glob(os.path.join(mod_root, 'localisation/english/**/*.yml'), recursive=True)):
            if os.path.basename(f) in own:
                continue
            for line in open(f, encoding='utf-8-sig', errors='replace'):
                m = re.match(r'^\s+([^\s:#]+):\d*\s', line)
                if m:
                    keys.add(m.group(1))
        _LOC_KEYS[mod_root] = keys
    return _LOC_KEYS[mod_root]


def game_label(modifier, english, loc):
    """the game's own modifier name (like MD: $MODIFIER_X$), our English label only where the game has none"""
    for key in ('MODIFIER_' + modifier.upper(), 'MODIFIER_' + modifier, modifier):
        if key in loc:
            return f'${key}$'
    return english


def read(path, bom_ok=True):
    with open(path, 'rb') as f:
        b = f.read()
    had_bom = b.startswith(b'\xef\xbb\xbf')
    return b.decode('utf-8-sig'), had_bom


def write(rel, text, bom=False):
    """write ./out/<rel> with LF line ends; .yml with BOM"""
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = text.replace('\r\n', '\n')
    data = text.encode('utf-8')
    if bom:
        data = b'\xef\xbb\xbf' + data
    with open(path, 'wb') as f:
        f.write(data)
    return path


def load_design():
    """import design/build.py and run it on design/parts/*.py (validates the approved design)"""
    sys.path.insert(0, DESIGN_DIR)
    spec = importlib.util.spec_from_file_location('design_build', os.path.join(DESIGN_DIR, 'build.py'))
    b = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b)
    b.FIRST_ENTRY_X = FIRST_ENTRY_X
    import glob
    paths = sorted(glob.glob(os.path.join(DESIGN_DIR, 'parts', '*.py')))
    parties, trunks, err, warn = b.run(paths)
    if err or warn:
        raise SystemExit('design does not validate:\n' + '\n'.join(err + warn))
    d = b.emit(parties, trunks, err, warn)
    return b, d


def idx():
    return json.load(open(os.path.join(IDX_DIR, 'idx_mdcw.json')))


def block_end(s, i):
    """index of the closing brace matching the '{' at or after i"""
    k = s.index('{', i)
    d = 0
    j = k
    n = len(s)
    while j < n:
        c = s[j]
        if c == '"':
            j = s.index('"', j + 1)
        elif c == '#':
            e = s.find('\n', j)
            j = n - 1 if e < 0 else e
            continue
        elif c == '{':
            d += 1
        elif c == '}':
            d -= 1
            if d == 0:
                return j
        j += 1
    raise ValueError('unbalanced braces')


def num(v):
    """format a number like MD (0.05, 0.1 -> 0.10 for 2-digit shares, ints plain)"""
    if isinstance(v, int) or float(v).is_integer() and abs(v) >= 1:
        return str(int(v))
    s = f'{v:.4f}'.rstrip('0')
    if s.endswith('.'):
        s += '0'
    # two decimals at least for shares like 0.1 -> 0.10 (MD style)
    if '.' in s and len(s.split('.')[1]) == 1:
        s += '0'
    return s
