# IMPERIA COLD WAR — USA and Soviet player-selected political leadership.
"""Native Sheep-style party choices with preserved appointments and 2000 bookmarks."""
from pathlib import Path
import json
import re
import sys
import uuid
from datetime import date,timedelta
from PIL import Image, ImageOps, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / 'tools'))
from catalogue import PEOPLE
from historical_politics_1970.special_successors import _assignment_blocks, _block_end
from multiplayer_quality.native_compat import normalize

P = 'COLDWAR_SP_1970_'
HEADER = '# IMPERIA COLD WAR — USA and Soviet political leadership integration.\n'
IDEO = ['Western_Autocracy', 'conservatism', 'liberalism', 'socialism', 'communist_state',
    'anarchist_communism', 'Conservative', 'Autocracy', 'Mod_Vilayat_e_Faqih', 'Vilayat_e_Faqih',
    'Kingdom', 'Caliphate', 'Neutral_Muslim_Brotherhood', 'Neutral_Autocracy', 'Neutral_conservatism',
    'oligarchism', 'Neutral_Libertarian', 'Neutral_green', 'neutral_Social', 'Neutral_Communism',
    'Nat_Populism', 'Nat_Fascism', 'Nat_Autocracy', 'Monarchist']
TRIG = ['western_autocrats', 'western_conservatism', 'western_liberals', 'western_social_democrats',
    'emerging_communist_state', 'emerging_anarchist_communism', 'emerging_reactionaries', 'emerging_autocracy',
    'emerging_moderate_shiite', 'emerging_hardline_shiite', 'salafist_kingdom', 'salafist_caliphate',
    'neutrality_neutral_muslim_brotherhood', 'neutrality_neutral_autocracy', 'neutrality_neutral_conservatism',
    'neutrality_neutral_oligarch', 'neutrality_neutral_libertarians', 'neutrality_neutral_green',
    'neutrality_neutral_social', 'neutrality_neutral_communism', 'nationalist_right_wing_populists',
    'nationalist_fascist', 'nationalist_military_junta', 'nationalist_monarchists']
PROFILE_TRAITS = dict(kos='economist_premier', pod='head_of_state', sus='chief_ideologue',
    she='iron_shurik', and_='chekist', gre='marshal_of_the_soviet_union', ust='the_armourer',
    gro='leningrad_boss', che='apparatchik', gor='new_generation')
PROFILE_TRAITS['and'] = PROFILE_TRAITS.pop('and_')
PROFILES = ['bre', 'kos', 'pod', 'sus', 'she', 'and', 'gre', 'ust', 'gro', 'che', 'gor']
WRITTEN = []
DEFAULTS = {('SOV',6):'sergei_trapeznikov', ('SOV',13):'nikolai_baibakov', ('SOV',18):'alexander_yakovlev'}
CROPS = {'USA_hubert_humphrey':(.19,.02,.81,.63), 'USA_george_wallace':(.12,.02,.88,.72),
    'SOV_viktor_tyulkin':(.07,.02,.56,.95), 'SOV_gavriil_popov':(.05,.02,.95,.79),
    'USA_ralph_nader':(.12,.01,.9,.73), 'USA_jesse_jackson':(.05,0,.95,.72)}


def b(key, body):
    return key + ' = {\n' + '\n'.join('\t' + s if s else '' for s in body.splitlines()) + '\n}'


def iff(test, body, other=''):
    return b('if', b('limit', test) + '\n' + body) + ('\n' + b('else', other) if other else '')


def context(tag):
    return f'original_tag = {tag}\nexists = yes\nis_dynamic_country = no\nIMP_is_1970_scenario = yes'


def ident(p):
    return p['tag'] + '_' + p['key']


def incumbent(p):
    checks = [f'has_country_leader = {{ name = "{n}" ruling_only = yes }}' for n in [p['name'], *p.get('aliases', [])]]
    return checks[0] if len(checks) == 1 else b('OR', '\n'.join(checks))

def eligibility(p):
    if not p.get('available_from'):return ''
    d=date(*map(int,p['available_from'].split('.')))-timedelta(days=1)
    return f'date > {d.year}.{d.month}.{d.day}'


def write(relative, content, bom=False):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if not relative.endswith('.json'):
        content = normalize(content, relative)
        if relative.endswith('.yml'):
            if not content.startswith('l_english:\n' + HEADER):
                content = content.replace('l_english:\n', 'l_english:\n' + HEADER, 1)
        elif not content.startswith('# IMPERIA COLD WAR — '):
            content = HEADER + content
    raw = content.encode('utf-8-sig' if bom else 'utf-8')
    before = path.read_bytes() if path.exists() else None
    if before != raw:
        temporary=path.with_name(path.name+'.coldwar_sp_'+uuid.uuid4().hex+'.tmp')
        temporary.write_bytes(raw)
        assert (path.read_bytes() if path.exists() else None)==before, 'Concurrent edit: '+relative
        temporary.replace(path)
    WRITTEN.append(relative)


def pictures():
    sources = {r['id']: r for r in json.loads((HERE / 'sources.json').read_text(encoding='utf-8'))['portraits']}
    out, sprites = {}, []
    for p in PEOPLE:
        key = ident(p)
        s = sources[key]
        record = HERE / 'generated' / (key + '.json')
        if s['status'] == 'reused':
            picture, method = s['portrait'], 'Existing identified mod portrait'
            master = ROOT / picture
        else:
            assert s['status'] == 'reference_ready', key
            if record.exists():
                master = HERE / json.loads(record.read_text(encoding='utf-8'))['master']
                method = 'AI restoration of the identified source photograph'
            else:
                # Explicitly documented originals are valid final assets when restoration is rejected.
                errors = HERE / 'generated' / (key + '_error.json')
                assert errors.exists(), 'Portrait restoration not completed: ' + key
                master = HERE / s['reference']
                method = 'Identified original photograph; image service rejected restoration'
            picture = 'gfx/leaders/COLDWAR_superpower_1970/' + key + '.dds'
            path = ROOT / picture
            path.parent.mkdir(parents=True, exist_ok=True)
            im=Image.open(master).convert('RGBA')
            if key in CROPS:
                im=im.crop(tuple(round(v*im.size[i%2]) for i,v in enumerate(CROPS[key])))
            ImageOps.fit(im, (156, 210), method=Image.Resampling.LANCZOS,
                centering=(.5, .15)).save(path, format='DDS')
        icon = 'gfx/interface/decisions/COLDWAR_superpower_1970/' + key + '.dds'
        path = ROOT / icon
        path.parent.mkdir(parents=True, exist_ok=True)
        ImageOps.fit(Image.open(ROOT / picture).convert('RGBA'), (33, 30), method=Image.Resampling.LANCZOS,
            centering=(.5, .12)).save(path, format='DDS')
        sprites.append(b('spriteType', f'name = "GFX_{P}{key}"\ntexturefile = "{icon}"'))
        out[key] = dict(p, id=key, portrait=picture, icon=icon, method=method, source=s)
    write('interface/COLDWAR_superpower_1970_leaders.gfx', b('spriteTypes', '\n\n'.join(sprites)) + '\n')
    return out


def profile_refresh(p, slot):
    desired = p.get('profile') if slot == 4 else None
    wrong = ['has_country_flag = COLDWAR_SOV_gensec_' + key for key in PROFILES if key != desired]
    test = b('OR', '\n'.join(wrong) + ('\nNOT = { has_country_flag = COLDWAR_SOV_gensec_' + desired + ' }' if desired else ''))
    body = '\n'.join('clr_country_flag = COLDWAR_SOV_gensec_' + key for key in PROFILES)
    if desired:
        body += '\nset_country_flag = COLDWAR_SOV_gensec_' + desired
    return iff(test, body + '\nforce_update_dynamic_modifier = yes')


def appointment(p, slot, data):
    traits = []
    if p['tag']=='USA' and p['key'] in ('richard_nixon','gerald_ford','ronald_reagan',
        'george_h_w_bush','bob_dole','george_mcgovern','jimmy_carter','walter_mondale','michael_dukakis','bill_clinton'):
        traits.append('career_politician')
    if p['tag'] == 'SOV' and slot == 4 and p.get('profile') in PROFILE_TRAITS:
        trait = PROFILE_TRAITS[p['profile']]
        if p['key'] == 'heydar_aliyev': trait = 'chekist_from_baku'
        if p['key'] == 'viktor_grishin': trait = 'moscow_boss'
        traits = ['COLDWAR_SOV_' + trait]
    create = b('create_country_leader', f'name = "{p["name"]}"\npicture = "{data[ident(p)]["portrait"]}"\ndesc = {P}{ident(p)}_desc\nideology = {IDEO[slot]}'
        + ('\ntraits = { ' + ' '.join(traits) + ' }' if traits else ''))
    result=iff((eligibility(p)+'\n' if eligibility(p) else '')+'NOT = { ' + incumbent(p) + ' }', 'retire_country_leader = yes\n' + create)
    if p['key']=='alexander_lukashenko':result+='\nCOLDWAR_LUKASHENKO_apply_portrait = yes'
    return result


def render(data):
    effects, triggers, categories, decisions, loc = {}, {}, [], [], {}
    all_supported = []
    for tag in ('USA', 'SOV'):
        rows = [p for p in PEOPLE if p['tag'] == tag]
        slots = sorted({s for p in rows for s in p['slots']})
        supported = context(tag) + '\nis_ai = no\n' + b('OR', '\n'.join(f'check_variable = {{ ruling_party = {s} }}' for s in slots))
        triggers[P + tag + '_supported'] = supported
        all_supported.append(P + tag + '_supported = yes')
        branches, observers = [], []
        for slot in slots:
            candidates = [p for p in rows if slot in p['slots']]
            pref = P + tag + '_preference_' + str(slot)
            party = TRIG[slot] + '_are_in_power = yes'
            gate = context(tag) + '\nis_ai = no\n' + party
            apply, observe = [], []
            for index, p in enumerate(candidates, 1):
                ready='\n'+eligibility(p) if eligibility(p) else ''
                observed = f'set_variable = {{ {pref} = {index} }}'
                if tag == 'SOV': observed += '\n' + profile_refresh(p, slot)
                observe.append(b('if' if index == 1 else 'else_if', b('limit', incumbent(p)+ready) + '\n' + observed))
                apply.append(b('if' if index == 1 else 'else_if', b('limit', f'check_variable = {{ {pref} = {index} }}'+ready)
                    + '\n' + appointment(p, slot, data)))
                key = P + tag + '_choose_' + str(slot) + '_' + p['key']
                active = b('hidden_trigger',context(tag)+'\nis_ai = no')+'\n'+party+ready+'\nNOT = { ' + incumbent(p) + ' }'
                run = f'set_variable = {{ {pref} = {index} }}\n'
                if tag == 'SOV':
                    run += 'COLDWAR_SOV_clear_heirs = yes\nclr_country_flag = COLDWAR_SOV_bre_retiring\nMDCW_HP_SOV_clear_manual_retirement_pending = yes\n'
                run += appointment(p, slot, data) + '\nset_correct_ideology_trait = yes\n' + P + tag + '_observe = yes'
                effects[key + '_effect'] = iff(active, run)
                effects[P + 'note_' + ident(p) + '_' + str(slot)] = iff(context(tag) + '\nis_ai = no'+ready,
                    f'set_variable = {{ {pref} = {index} }}\n' + iff(party, P + tag + '_observe = yes'))
                choices = b(key, f'icon = GFX_{P}{ident(p)}\ncost = 0\nfire_only_once = no\ndays_re_enable = 0\n'
                    + b('allowed', 'original_tag = '+tag) + '\n' + b('visible', gate) + '\n' + b('available', active)
                    + '\n' + b('complete_effect', key + '_effect = yes') + '\nai_will_do = { factor = 0 }')
                decisions.append((tag, slot, choices))
                loc[key] = 'Select ' + p['name']
                loc[key + '_desc'] = p['description']+(' Available from '+p['available_from'].split('.')[0]+'.' if p.get('available_from') else '')
                loc[P + ident(p) + '_desc'] = p['description']
            default_person = next((p for p in candidates if p['key']==DEFAULTS.get((tag,slot))), candidates[0])
            default_index = candidates.index(default_person)+1
            default = f'set_variable = {{ {pref} = {default_index} }}\n' + appointment(default_person, slot, data)
            apply.append(b('else', default))
            cycle = iff('check_variable = { MDCW_HP_native_retirement = 1 }\nNOT = { has_country_flag = do_not_retire }',
                f'add_to_variable = {{ {pref} = 1 }}\n' + iff(f'check_variable = {{ {pref} > {len(candidates)} }}', f'set_variable = {{ {pref} = 1 }}'))
            branches.append(b('if' if not branches else 'else_if', b('limit', party) + '\n' + cycle + '\n' + '\n'.join(apply)))
            observers.append(b('if' if not observers else 'else_if', b('limit', party) + '\n' + '\n'.join(observe)))
            category = P + tag + '_candidates_' + str(slot)
            if tag=='SOV' and slot in (4,6):
                from lukashenko_1970.build import wardrobe_decisions
                decisions.append((tag,slot,wardrobe_decisions(gate,'SOV_'+str(slot),loc)))
            categories.append(b(category, 'icon = GFX_decision_category_generic_political_actions\npriority = 2000\n'
                + b('allowed', 'original_tag = '+tag) + '\n' + b('visible', gate)))
            loc[category] = 'Leadership Candidates: [show_ruling_party]'
            loc[category + '_desc'] = 'Choose the political representative of the governing party.'+(' Alexander Lukashenko becomes available in '+next(p['available_from'].split('.')[0] for p in candidates if p.get('available_from'))+'.' if any(p.get('available_from') for p in candidates) else ' Candidates remain available throughout the campaign.')
        callback = ''
        if tag == 'USA':
            nixon = next(p for p in rows if p['key'] == 'richard_nixon')
            callback = '\n' + iff('western_conservatism_are_in_power = yes\n' + incumbent(nixon),
                'set_country_flag = USA_1970_nixon_presidency', 'clr_country_flag = USA_1970_nixon_presidency')
            callback += '\n' + iff('has_country_flag = USA_1970_systems_initialized', 'COLDWAR_USA_legacy_reconcile_party_programmes = yes')
        else:
            callback = '\n' + iff('NOT = { emerging_communist_state_are_in_power = yes }',
                iff(b('OR', '\n'.join('has_country_flag = COLDWAR_SOV_gensec_' + k for k in PROFILES)),
                    '\n'.join('clr_country_flag = COLDWAR_SOV_gensec_' + k for k in PROFILES) + '\nforce_update_dynamic_modifier = yes'))
        effects[P + tag + '_observe'] = iff(context(tag) + '\nis_ai = no', '\n'.join(observers) + callback
            + f'\nset_variable = {{ {P}{tag}_observed_party = ruling_party }}')
        # Do not adopt the outgoing representative into another party's remembered selection.
        adopt = iff(f'check_variable = {{ {P}{tag}_observed_party = ruling_party }}', P + tag + '_observe = yes')
        effects[P + tag + '_set_leader'] = iff(P + tag + '_supported = yes', adopt + '\nupdate_set_politics = yes\n'
            + '\n'.join(branches) + '\nset_correct_ideology_trait = yes\n' + P + tag + '_observe = yes')
    triggers[P + 'supported'] = b('OR', '\n'.join(all_supported))
    triggers[P + 'human_sov'] = context('SOV') + '\nis_ai = no'
    pulse = []
    for tag in ('USA', 'SOV'):
        pulse.append(b(tag, iff('exists = yes\nIMP_is_1970_scenario = yes', P + tag + '_observe = yes')))
    hooks = b('on_startup', b('effect', '\n'.join(pulse)))
    for tag in ('USA', 'SOV'):
        hooks += '\n' + b('on_monthly_' + tag, b('effect', iff(context(tag), P + tag + '_observe = yes')))
    write('common/scripted_effects/COLDWAR_superpower_1970_leaders.txt', '\n\n'.join(b(k,v) for k,v in effects.items()) + '\n')
    write('common/scripted_triggers/COLDWAR_superpower_1970_leaders.txt', '\n\n'.join(b(k,v) for k,v in triggers.items()) + '\n')
    write('common/decisions/categories/COLDWAR_superpower_1970_leaders.txt', '\n\n'.join(categories) + '\n')
    write('common/decisions/COLDWAR_superpower_1970_leaders.txt', '\n\n'.join(b(P+tag+'_candidates_'+str(slot), '\n\n'.join(t for tg,s,t in decisions if tg==tag and s==slot))
        for tag in ('USA','SOV') for slot in sorted({s for tg,s,t in decisions if tg==tag})) + '\n')
    write('common/on_actions/COLDWAR_superpower_1970_leaders.txt', b('on_actions', hooks) + '\n')
    write('localisation/english/COLDWAR_superpower_1970_leaders_l_english.yml', 'l_english:\n'+HEADER
        +'\n'.join(' '+k+':0 "'+v.replace('"', "'")+'"' for k,v in sorted(loc.items()))+'\n', True)


def main():
    data = pictures()
    render(data)
    from integration import install
    install(data, write)
    write('tools/superpower_1970_leaders/runtime_roster.json', json.dumps(dict(project='IMPERIA COLD WAR',
        calendar_eligibility=True, calendar_exceptions={k:p['available_from'] for k,p in data.items() if p.get('available_from')}, people=list(data.values())), ensure_ascii=False, indent=2)+'\n')
    manifest = dict(project='IMPERIA COLD WAR', files=sorted(set(WRITTEN)))
    (HERE/'runtime_files.json').write_text(json.dumps(manifest, indent=2)+'\n',encoding='utf-8')
    for tag in ('USA','SOV'):
        items = [r for r in data.values() if r['tag']==tag]
        sheet = Image.new('RGB',(1360,((len(items)+7)//8)*235),'#20272b')
        draw=ImageDraw.Draw(sheet); font=ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',12)
        for i,r in enumerate(items):
            x,y=i%8*170,i//8*235
            sheet.paste(Image.open(ROOT/r['portrait']).convert('RGB'),(x,y))
            draw.text((x+78,y+220),r['name'][:25],font=font,fill='white',anchor='mm')
        sheet.save(HERE/(tag+'_PORTRAIT_REVIEW.png'))
    print(json.dumps(dict(project='IMPERIA COLD WAR', people=len(data), choices=sum(len(p['slots']) for p in PEOPLE), files=len(manifest['files']))))


if __name__ == '__main__':
    main()
