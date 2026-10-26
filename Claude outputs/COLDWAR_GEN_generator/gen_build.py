# IMPERIA CW — Cold War: Generic 1970 national focus content generator.
"""COLDWAR | build the party paths of the 1970 generic tree.

python3 gen_build.py [mod_root]     (default: /mnt/user-data/uploads/mdcoldwar)
Writes the finished files to ./out/<mod path> and ./out/build_report.json; then run validate_gen.py.
"""
import sys, os, re, json, shutil
from gen_common import *
import gen_effects as GE
from gen_load import load_focus_file, simple
from gen_focus import political_sections, domain_moves, write_focus_file
from gen_icons import sprite_pool, picture_pool, keywords, assign, ICON_OVERRIDE, PICTURE_OVERRIDE
from gen_misc import (ideas_file, dynmod_file, old_programme_icons, old_loc_transform, new_loc_file, shared_tt_file,
                      effects_patch, loc_keys)

MOD = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/uploads/mdcoldwar'


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    b, design = load_design()
    meta = b.META
    loaded = load_focus_file(MOD)
    secd = dict(loaded['sections'])

    # ---- old political foci: icon and AI base are kept for existing ids
    pol_names = set(POLITICAL_SECTIONS.values())
    old = {}
    for name in pol_names:
        for f in secd[name]:
            d = simple(f['fields'])
            m = re.search(r'base = (\d+)', d.get('ai_will_do', ''))
            old[f['id']] = dict(icon=d['icon'], ai_base=int(m.group(1)) if m else AI_BASE_NEW)
    design_ids = {P + n['id'] for n in design['nodes']}
    dropped = sorted(set(old) - design_ids)
    if dropped:
        raise SystemExit('old party/trunk foci missing in the design: ' + ', '.join(dropped))
    for n in design['nodes']:
        if n['old'] and P + n['id'] not in old:
            raise SystemExit(f'{n["id"]} marked old but not in the current tree')

    # ---- MD tooltips that exist
    # only keys DEFINED in the mod's localisation (MD's trees use some <modifier>_tt that no file defines)
    md_tt = {k for k in mod_loc_keys(MOD) if k.endswith('_tt')}
    assert 'political_power_factor_tt' in md_tt, 'MD tooltip keys not found (MD_dm_modifiers_l_english.yml)'

    # ---- MD building prices (fixed bn in the helper) -> GDP share
    eff_text = ''
    for fn in ('00_scripted_effects.txt',):
        eff_text += read(f'{MOD}/common/scripted_effects/{fn}')[0]
    for h in b.BUILD:
        m = re.search(r'^' + h + r' = \{', eff_text, re.M)
        if not m:
            raise SystemExit('building helper not found: ' + h)
        body = eff_text[m.start():block_end(eff_text, m.start()) + 1]
        c = re.findall(r'treasury_change = (-?[\d.]+)', body)
        if 'skip_payment' not in body or not c:
            raise SystemExit('building helper without skip_payment/price: ' + h)
        GE.BUILD_COST[h] = abs(float(c[-1]))

    trunk_t2 = {n['o']: n['id'] for n in design['nodes'] if n['grp'] == 'trunk' and n['slot'] == 'T2'}
    ctx = GE.Ctx(md_tt, meta, trunk_t2)

    # ---- MD ideas that another branch can also give -> guard with NOT has_idea
    other_text = '\n'.join(f['raw'] for name, foci in loaded['sections'] if name not in pol_names for f in foci)
    md_uses = {}
    for n in design['nodes']:
        for e in n['fx']:
            if e[0] in ('mdidea', 'mdtimed'):
                md_uses.setdefault(e[1], []).append(n['id'])
    guarded = set(md_uses)        # MD ideas: always behind NOT has_idea (another branch or the start may give them)

    # ---- icons for new foci
    reserved = set()
    for name, foci in loaded['sections']:
        for f in foci:
            reserved.add(simple(f['fields'])['icon'])
    pool = sprite_pool(reserved)
    items = [(n['id'], keywords(n['name'], n['fx'], n['o'], n['party']), n['party'], n['o']) for n in design['nodes'] if not n['old']]
    new_icons = assign(items, pool, {k: v for k, v in ICON_OVERRIDE.items()})
    icons = {n['id']: (old[P + n['id']]['icon'] if n['old'] else new_icons[n['id']]) for n in design['nodes']}

    # ---- focus file
    programme_vars = {p['key']: (f'{P}{p["key"]}_programme', f'{P}{p["key"]}_') for p in design['parties']}
    pol_texts = political_sections(design, ctx, icons, old, meta, GE.compile_focus, GE.resolve_md_ideas, guarded, programme_vars)
    moves, _, _ = domain_moves(loaded['sections'])
    focus_text = write_focus_file(loaded, pol_texts, moves)
    from gen_quality import patch_base_office_focus, runtime_files
    focus_text = patch_base_office_focus(focus_text)
    write(F_FOCUS, focus_text)

    # ---- national spirits
    old_ideas_text = read(f'{MOD}/{F_OLD_IDEAS}')[0]
    old_pics = set(re.findall(r'picture = (\S+)', old_ideas_text))
    ppool = picture_pool(old_pics)
    pitems = []
    for iid, d in ctx.ideas.items():
        fx = [('prog', k, v) for k, v in d['mods'].items()]
        node = next(n for n in design['nodes'] if P + n['id'] == d['focus'])
        pitems.append((iid, keywords(d['name'], fx, node['o'], node['party']), node['party'], node['o']))
    pictures = assign(pitems, ppool, {P + k: v for k, v in PICTURE_OVERRIDE.items()})
    write(F_NEW_IDEAS, ideas_file(ctx.ideas, pictures, meta))

    # ---- party programmes
    dm_old = read(f'{MOD}/{F_DYNMOD}')[0]
    dm_text, prog_keys = dynmod_file(design, meta, old_programme_icons(dm_old))
    write(F_DYNMOD, dm_text)

    # ---- localisation
    old_loc, old_bom = read(f'{MOD}/{F_OLD_LOC}')
    new_old_loc, removed = old_loc_transform(old_loc, [P + n['id'] for n in design['nodes']])
    from gen_quality_narratives import apply_narratives
    new_old_loc = apply_narratives(new_old_loc)
    write(F_OLD_LOC, new_old_loc, bom=old_bom)
    loc_text, new_keys = new_loc_file(design, ctx, set(loc_keys(new_old_loc)))
    write(F_NEW_LOC, loc_text, bom=True)
    shared_path = f'{MOD}/{F_SHARED_TT}'
    shared_existing = read(shared_path)[0] if os.path.exists(shared_path) else ''
    shared_text, shared_added = shared_tt_file(shared_existing, ctx.coldwar_tt, mod_loc_keys(MOD))
    write(F_SHARED_TT, shared_text, bom=True)

    # ---- scripted effects: tension helper
    eff, eff_bom = read(f'{MOD}/{F_EFFECTS}')
    write(F_EFFECTS, effects_patch(eff), bom=eff_bom)
    for relative, payload in runtime_files().items():
        write(relative, payload, bom=relative.endswith('.yml'))

    report = dict(
        foci_total=focus_text.count('\n\tfocus = {'), party_foci=sum(1 for n in design['nodes'] if n['grp'] == 'party'),
        trunk_foci=sum(1 for n in design['nodes'] if n['grp'] == 'trunk'),
        new_ids=sum(1 for n in design['nodes'] if not n['old']), old_ids=sum(1 for n in design['nodes'] if n['old']),
        ideas=len(ctx.ideas), bound_ideas=sum(1 for d in ctx.ideas.values() if d['bound']),
        timed_ideas=sum(1 for d in ctx.ideas.values() if d['days']), coldwar_tt=sorted(ctx.coldwar_tt),
        shared_tt_added=shared_added, loc_removed_from_old=len(removed), new_loc_keys=len(new_keys),
        notes_without_code=ctx.notes_dropped, md_ideas_guarded=sorted(guarded), md_ideas_used=ctx.md_ideas_used,
        domain_moves={k: v[:2] for k, v in moves.items()}, new_icons={k: new_icons[k] for k in sorted(new_icons)},
        pictures=pictures, programme_keys=prog_keys,
    )
    json.dump(report, open(os.path.join(OUT, 'build_report.json'), 'w'), indent=1, ensure_ascii=False)
    print(f'built: {report["foci_total"]} foci ({report["party_foci"]} party, {report["trunk_foci"]} trunk), '
          f'{report["ideas"]} ideas, {len(removed)} old loc keys moved, {len(new_keys)} new loc keys, '
          f'{len(ctx.coldwar_tt)} COLDWAR tooltips')


if __name__ == '__main__':
    main()
