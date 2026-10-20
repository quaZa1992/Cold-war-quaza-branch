"""Build and validate the Egypt 1970 party/character integration from roster.py.

AI edits are supplied separately under generated/<person>.png; Pillow only performs
format conversion and resizing, never colorisation or photographic reconstruction.
"""
import json
import re
from pathlib import Path
from PIL import Image, ImageOps
from roster import IDEOLOGIES, PARTIES, NAMES, MILITARY, PHOTO_PROMPT

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
PORTRAITS = ROOT / 'gfx/leaders/EGY/1970'
LOC_PREFIX = 'COLDWAR_EGY_1970_party_'

def write(path, text, bom=False):
    path = ROOT / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8-sig' if bom else 'utf-8', newline='\n')

def picture(key):
    return f'gfx/leaders/EGY/1970/{key}.dds'

def leader_line(key, ideology):
    return f'create_country_leader = {{ name = "{NAMES[key]}" picture = "{picture(key)}" ideology = {ideology} }}'

def sprites_and_localisation():
    base = (ROOT/'localisation/english/MD_politics_view_parties_l_english.yml').read_text(encoding='utf-8-sig')
    sprites = {}
    for path in (ROOT/'interface').glob('*.gfx'):
        for name, tex in re.findall(r'name\s*=\s*"([^"]+)"\s+texturefile\s*=\s*"([^"]+)"', path.read_text(encoding='utf-8-sig')):
            sprites[name] = tex
    gfx = ['# COLDWAR | Egypt 1970: one registered icon per ideology slot.', 'spriteTypes = {']
    languages = {'english':['l_english:'], 'german':['l_german:']}
    icons = {}
    logo_file=HERE/'party_logo_sources/sources.json'
    logo_sources={p['slot']:p for p in json.loads(logo_file.read_text()) if p.get('path')} if logo_file.exists() else {}
    icon_dir=ROOT/'gfx/texticons/parties_icons/egypt/1970'
    icon_dir.mkdir(parents=True,exist_ok=True)
    for idx, (en, de, key, en_desc, de_desc) in enumerate(PARTIES):
        ideology = IDEOLOGIES[idx]
        match = re.search(rf'^ EGY\.{re.escape(ideology)}: "£(\S+)', base, re.M)
        token = match.group(1) if match else f'generic_{ideology}_small'
        token = {2:'EGY_liberalism_alt',3:'EGY_socialism',5:'EGY_anarchist_communism',
                 6:'EGY_Conservative',7:'EGY_em_Autocracy',16:'EGY_Neutral_Libertarian'}.get(idx,token)
        if idx == 18: token = 'EGY_neutral_Social'
        if idx == 23: token = 'EGY_Monarchist'
        tex = sprites.get('GFX_'+token)
        if not tex:
            raise ValueError(f'No sprite for slot {idx}: {token}')
        if idx in logo_sources and idx != 4:
            im=Image.open(ROOT/logo_sources[idx]['path']).convert('RGBA')
            im.thumbnail((22,22),Image.Resampling.LANCZOS)
            canvas=Image.new('RGBA',(22,22),(0,0,0,0))
            canvas.alpha_composite(im,((22-im.width)//2,(22-im.height)//2))
            tex=f'gfx/texticons/parties_icons/egypt/1970/party_{idx}.dds'
            canvas.save(ROOT/tex)
        icons[key] = tex
        gfx += ['\tspriteType = {',f'\t\tname = "GFX_COLDWAR_EGY_1970_party_{idx}"',
                f'\t\ttexturefile = "{tex}"','\t\tlegacy_lazy_load = no','\t}']
        for lang, name, desc in [('english',en,en_desc),('german',de,de_desc)]:
            prefix = f'{LOC_PREFIX}{idx}'
            text = desc + ('\\n\\nLeader: ' if lang == 'english' else '\\n\\nFührung: ') + NAMES[key]
            languages[lang] += [f' {prefix}:0 "£COLDWAR_EGY_1970_party_{idx} {name}"',
                f' {prefix}_icon:0 "£COLDWAR_EGY_1970_party_{idx}"',
                f' {prefix}_desc:0 "{text}"']
    variants=[('0_future',25,"Nation's Future Party",'Partei Zukunft der Nation',
               'The later party is retained as an alternate foundation in 1970. Anwar Sadat is its alternate candidate, not its historical founder.',
               'Die spätere Partei bleibt als alternative Gründung von 1970 erhalten. Anwar as-Sadat ist ihr alternativer Kandidat, nicht ihr historischer Gründer.'),
              ('18_alliance',24,'Socialist Popular Alliance Party','Partei der Sozialistischen Volksallianz',
               'The later party is retained as an alternate successor to the ASU. Khaled Mohieddin is its alternate 1970 candidate, not its historical founder.',
               'Die spätere Partei bleibt als alternative Nachfolgepartei der ASU erhalten. Khaled Mohieddin ist ihr alternativer Kandidat von 1970, nicht ihr historischer Gründer.')]
    for suffix,source_idx,en,de,en_desc,de_desc in variants:
        im=Image.open(ROOT/logo_sources[source_idx]['path']).convert('RGBA')
        im.thumbnail((22,22),Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(22,22),(0,0,0,0))
        canvas.alpha_composite(im,((22-im.width)//2,(22-im.height)//2))
        tex=f'gfx/texticons/parties_icons/egypt/1970/party_{suffix}.dds'
        canvas.save(ROOT/tex)
        gfx += ['\tspriteType = {',f'\t\tname = "GFX_COLDWAR_EGY_1970_party_{suffix}"',
                f'\t\ttexturefile = "{tex}"','\t\tlegacy_lazy_load = no','\t}']
        for lang,name,desc in [('english',en,en_desc),('german',de,de_desc)]:
            prefix=LOC_PREFIX+suffix
            languages[lang] += [f' {prefix}:0 "£COLDWAR_EGY_1970_party_{suffix} {name}"',
                f' {prefix}_icon:0 "£COLDWAR_EGY_1970_party_{suffix}"',f' {prefix}_desc:0 "{desc}"']
    gfx += ['}']
    write('interface/COLDWAR_EGY_1970_parties.gfx','\n'.join(gfx)+'\n')
    for lang, lines in languages.items():
        for key,name in NAMES.items():
            leader_text=f'§Y{name}§! becomes the leader of [ROOT.GetNameDef].' if lang=='english' else f'§Y{name}§! übernimmt die Führung von [ROOT.GetNameDef].'
            lines.append(f' COLDWAR_EGY_1970_new_leader_{key}_tt:0 "{leader_text}"')
        for key,role,skills,slot,trait,date in MILITARY:
            lines.append(f' COLDWAR_EGY_1970_{key}:0 "{NAMES[key]}"')
        for key,en,de in [('party_formations','Party Foundations','Parteigründungen'),
                          ('found_future_party',"Found the Nation's Future Party",'Die Partei Zukunft der Nation gründen'),
                          ('found_socialist_alliance','Found the Socialist Popular Alliance','Die Sozialistische Volksallianz gründen')]:
            lines.append(f' COLDWAR_EGY_1970_{key}:0 "{en if lang=="english" else de}"')
        lines += [
            ' COLDWAR_EGY_1970_reserve_officers:0 "Reserve Officers"' if lang=='english' else ' COLDWAR_EGY_1970_reserve_officers:0 "Reserveoffiziere"',
            ' COLDWAR_EGY_1970_recall_ahmad_ismail:0 "Recall Ahmad Ismail Ali"' if lang=='english' else ' COLDWAR_EGY_1970_recall_ahmad_ismail:0 "Ahmad Ismail Ali zurückrufen"',
            ' COLDWAR_EGY_1970_recall_zikri:0 "Recall Fouad Abou Zikry"' if lang=='english' else ' COLDWAR_EGY_1970_recall_zikri:0 "Fouad Abou Zikry zurückrufen"',
            ' COLDWAR_EGY_1970_recall_ahmad_ismail_desc:0 "Ahmad Ismail Ali was dismissed in September 1969. Recall him after May 1971."' if lang=='english' else ' COLDWAR_EGY_1970_recall_ahmad_ismail_desc:0 "Ahmad Ismail Ali wurde im September 1969 entlassen. Ab Mai 1971 kann er zurückgerufen werden."',
            ' COLDWAR_EGY_1970_recall_zikri_desc:0 "Abou Zikry left naval command in September 1969. Recall him from October 1972."' if lang=='english' else ' COLDWAR_EGY_1970_recall_zikri_desc:0 "Abou Zikry verlor das Marinekommando im September 1969. Ab Oktober 1972 kann er zurückgerufen werden."',
        ]
        write(f'localisation/{lang}/COLDWAR_EGY_1970_parties_l_{lang}.yml','\n'.join(lines)+'\n',True)
    # Existing dispatch definitions must be patched, not redefined in another file.
    path = ROOT/'common/scripted_localisation/00_MD_politicsview_scripted_localisation.txt'
    original = path.read_text(encoding='utf-8-sig')
    text = original
    for idx, ideology in enumerate(IDEOLOGIES):
        for suffix in ['', '_desc', '_icon']:
            getter = ideology+'_L'+suffix
            line = (f'\ttext = {{ trigger = {{ original_tag = EGY IMP_is_1970_scenario = yes }} '
                    f'localization_key = {LOC_PREFIX}{idx}{suffix} }} # COLDWAR | Egypt 1970\n')
            pattern = rf'(\tname = {re.escape(getter)}\s*\n)'
            if line not in text:
                text, count = re.subn(pattern,lambda m:m.group(1)+line,text,count=1)
                assert count==1, getter
            if idx in (0,18):
                variant='0_future' if idx==0 else '18_alliance'
                flag='COLDWAR_EGY_1970_future_party' if idx==0 else 'COLDWAR_EGY_1970_socialist_alliance'
                alt=(f'\ttext = {{ trigger = {{ original_tag = EGY IMP_is_1970_scenario = yes has_country_flag = {flag} }} '
                     f'localization_key = {LOC_PREFIX}{variant}{suffix} }} # COLDWAR | retained later party\n')
                if alt not in text: text=text.replace(line,alt+line,1)
    if text != original: path.write_text(text,encoding='utf-8',newline='\n')
    return icons

def portraits(icons):
    PORTRAITS.mkdir(parents=True, exist_ok=True)
    (PORTRAITS/'small').mkdir(exist_ok=True)
    keys = {p[2] for p in PARTIES} | {m[0] for m in MILITARY} | {'sadat'}
    for key in sorted(keys):
        png = HERE/'generated'/f'{key}.png'
        if png.exists():
            im = Image.open(png).convert('RGBA')
            ImageOps.fit(im,(156,210),centering=(0.5,0.35)).save(PORTRAITS/f'{key}.dds')
            ImageOps.fit(im,(65,67),centering=(0.5,0.20)).save(PORTRAITS/'small'/f'{key}.dds')
        elif key.endswith('_council'):
            # A collective leader uses its emblem, never an unrelated person's face.
            emblem=Image.open(ROOT/icons[key]).convert('RGBA')
            im=Image.new('RGBA',(156,210),(35,38,45,255))
            emblem.thumbnail((110,110))
            enlarged=emblem.resize((110,110),Image.Resampling.LANCZOS)
            im.paste(enlarged,(23,50),enlarged)
            im.save(PORTRAITS/f'{key}.dds')
            ImageOps.fit(im,(65,67)).save(PORTRAITS/'small'/f'{key}.dds')
    return keys

def effects():
    out=['# COLDWAR | All 24 party leaders, explicitly selected by MD subparty index.',
         '# Later parties and their 1970 casting are intentionally alternate history.',
         'COLDWAR_EGY_set_party_leader_1970 = {']
    for idx, party in enumerate(PARTIES):
        key=party[2]
        out += [f'\t{"if" if idx==0 else "else_if"} = {{',
                f'\t\tlimit = {{ check_variable = {{ ruling_party = {idx} }} }}']
        if idx==18:
            out += ['\t\tif = {','\t\t\tlimit = { has_country_flag = COLDWAR_EGY_1970_socialist_alliance }',
                    '\t\t\t'+leader_line('khaled_mohieddin',IDEOLOGIES[idx]),'\t\t}',
                    '\t\telse_if = {','\t\t\tlimit = { has_country_flag = COLDWAR_EGY_nasser_deceased }',
                    '\t\t\t'+leader_line('sadat',IDEOLOGIES[idx]),'\t\t}',
                    '\t\telse = {','\t\t\t'+leader_line(key,IDEOLOGIES[idx]),'\t\t}']
        else: out += ['\t\t'+leader_line(key,IDEOLOGIES[idx])]
        out += ['\t}']
    out += ['}', '', 'COLDWAR_EGY_recruit_1970_military = {',
            '\tif = {','\t\tlimit = { NOT = { has_country_flag = COLDWAR_EGY_1970_military_recruited } }',
            '\t\tset_country_flag = COLDWAR_EGY_1970_military_recruited']
    for key,role,skills,slot,trait,date in MILITARY:
        if not date: out += [f'\t\trecruit_character = COLDWAR_EGY_1970_{key}']
    out += ['\t}','}']
    write('common/scripted_effects/COLDWAR_EGY_1970_roster_effects.txt','\n'.join(out)+'\n')
    path=ROOT/'common/scripted_effects/EGY_political_leaders.txt'
    text=path.read_text(encoding='utf-8-sig')
    if 'COLDWAR_EGY_set_party_leader_1970' not in text:
        assert text.startswith('set_leader_EGY = {')
        native=text[len('set_leader_EGY = {'):].strip()
        assert native.endswith('}')
        text=('set_leader_EGY = {\n\tif = {\n'
              '\t\tlimit = { IMP_is_1970_scenario = yes }\n'
              '\t\tCOLDWAR_EGY_set_party_leader_1970 = yes\n\t}\n\telse = {\n'
              + native[:-1].rstrip()+'\n\t}\n}\n')
        path.write_text(text,encoding='utf-8',newline='\n')

def characters():
    out=['# COLDWAR | January 1970 military roster. Field marshal = strategic game role.', 'characters = {']
    for key,role,skills,slot,trait,date in MILITARY:
        out += [f'\tCOLDWAR_EGY_1970_{key} = {{',f'\t\tname = "{NAMES[key]}"',
                '\t\tportraits = {','\t\t\tarmy = {',f'\t\t\t\tlarge = "{picture(key)}"',
                f'\t\t\t\tsmall = "gfx/leaders/EGY/1970/small/{key}.dds"','\t\t\t}','\t\t}']
        if role:
            attrs=['skill','attack_skill','defense_skill','maneuvering_skill','coordination_skill'] if role=='navy_leader' else ['skill','attack_skill','defense_skill','planning_skill','logistics_skill']
            out += [f'\t\t{role} = {{']
            out += [f'\t\t\t{attr} = {value}' for attr,value in zip(attrs,skills)]
            out += ['\t\t}']
        ledger='navy' if role=='navy_leader' else 'air' if not role else 'army'
        out += ['\t\tadvisor = {',f'\t\t\tslot = {slot}',f'\t\t\tidea_token = COLDWAR_EGY_1970_{key}',
                f'\t\t\ttraits = {{ {trait} }}','\t\t\tcost = 100',
                '\t\t\tallowed = { original_tag = EGY IMP_is_1970_scenario = yes }']
        if slot=='high_command': out += [f'\t\t\tledger = {ledger}']
        out += ['\t\t\tai_will_do = { factor = 1 }','\t\t}','\t}']
    out += ['}']
    write('common/characters/COLDWAR_EGY_1970_characters.txt','\n'.join(out)+'\n')
    out=['# COLDWAR | Dismissed officers can be recalled on their later historical dates.',
         'COLDWAR_EGY_1970_reserve_officers = {',
         '\tCOLDWAR_EGY_1970_recall_ahmad_ismail = {',
         '\t\ticon = generic_prepare_civil_war_new','\t\tcost = 25',
         '\t\tvisible = { original_tag = EGY IMP_is_1970_scenario = yes NOT = { has_country_flag = COLDWAR_EGY_1970_recalled_ahmad_ismail } }',
         '\t\tavailable = { date > 1971.5.13 }',
         '\t\tcomplete_effect = { recruit_character = COLDWAR_EGY_1970_ahmad_ismail set_country_flag = COLDWAR_EGY_1970_recalled_ahmad_ismail }',
         '\t\tai_will_do = { factor = 1 }','\t}',
         '\tCOLDWAR_EGY_1970_recall_zikri = {',
         '\t\ticon = generic_naval','\t\tcost = 25',
         '\t\tvisible = { original_tag = EGY IMP_is_1970_scenario = yes NOT = { has_country_flag = COLDWAR_EGY_1970_recalled_zikri } }',
         '\t\tavailable = { date > 1972.10.23 }',
         '\t\tcomplete_effect = { recruit_character = COLDWAR_EGY_1970_zikri set_country_flag = COLDWAR_EGY_1970_recalled_zikri }',
         '\t\tai_will_do = { factor = 1 }','\t}','}']
    write('common/decisions/COLDWAR_EGY_1970_reserve_officers.txt','\n'.join(out)+'\n')
    write('common/decisions/categories/COLDWAR_EGY_1970_reserve_officers.txt',
          'COLDWAR_EGY_1970_reserve_officers = {\n\ticon = generic\n'
          '\tallowed = { original_tag = EGY IMP_is_1970_scenario = yes }\n'
          '\tvisible = { original_tag = EGY IMP_is_1970_scenario = yes }\n}\n')
    write('common/decisions/COLDWAR_EGY_1970_party_formations.txt',
          '# COLDWAR | Later parties deliberately retained as optional alternate foundations.\n'
          'COLDWAR_EGY_1970_party_formations = {\n'
          '\tCOLDWAR_EGY_1970_found_future_party = {\n'
          '\t\ticon = generic_political_discourse\n\t\tcost = 50\n'
          '\t\tvisible = { original_tag = EGY IMP_is_1970_scenario = yes NOT = { has_country_flag = COLDWAR_EGY_1970_future_party } }\n'
          '\t\tavailable = { check_variable = { ruling_party = 0 } }\n'
          '\t\tcomplete_effect = { set_country_flag = COLDWAR_EGY_1970_future_party update_dirty_politicsview_expanded = yes }\n'
          '\t\tai_will_do = { factor = 0 }\n\t}\n'
          '\tCOLDWAR_EGY_1970_found_socialist_alliance = {\n'
          '\t\ticon = generic_political_discourse\n\t\tcost = 50\n'
          '\t\tvisible = { original_tag = EGY IMP_is_1970_scenario = yes NOT = { has_country_flag = COLDWAR_EGY_1970_socialist_alliance } }\n'
          '\t\tavailable = { check_variable = { ruling_party = 18 } NOT = { has_country_leader = { name = "Gamal Abdel Nasser" ruling_only = yes } } }\n'
          '\t\tcomplete_effect = { set_country_flag = COLDWAR_EGY_1970_socialist_alliance retire_country_leader = yes COLDWAR_EGY_set_party_leader_1970 = yes set_correct_ideology_trait = yes update_dirty_politicsview_expanded = yes }\n'
          '\t\tai_will_do = { factor = 0 }\n\t}\n}\n')
    write('common/decisions/categories/COLDWAR_EGY_1970_party_formations.txt',
          'COLDWAR_EGY_1970_party_formations = {\n\ticon = generic_political_actions\n'
          '\tallowed = { original_tag = EGY IMP_is_1970_scenario = yes }\n'
          '\tvisible = { original_tag = EGY IMP_is_1970_scenario = yes }\n}\n')

def connect_history_and_focus():
    path=ROOT/'history/countries/EGY - Egypt.txt'
    original=text=path.read_text(encoding='utf-8-sig')
    if 'COLDWAR_EGY_recruit_1970_military = yes' not in text:
        text=text.replace('COLDWAR_EGY_initialize_1970 = yes # COLDWAR | laws, factions, start spirits',
            'COLDWAR_EGY_initialize_1970 = yes # COLDWAR | laws, factions, start spirits\n'
            '\t\tCOLDWAR_EGY_recruit_1970_military = yes # COLDWAR | historically active officers',1)
    text=text.replace('gfx/Leaders/EGY/EGY_Coldwar_Gamal_Abdel_Nasser.dds',picture('nasser'))
    # The scripted September event handles death. An expiry on the same day could
    # remove Nasser first and prevent its has_country_leader trigger from firing.
    text=text.replace(' expire = "1970.9.28"','')
    if text != original: path.write_text(text,encoding='utf-8',newline='\n')
    by_name={name:key for key,name in NAMES.items() if not key.endswith('_council')}
    by_name['Mohammed Ali Fahmi']='air_defence_fahmy'
    targets=[ROOT/'common/national_focus/COLDWAR_EGY_1970_focus.txt',
             ROOT/'common/scripted_effects/COLDWAR_EGY_1970_scripted_effects.txt',
             ROOT/'Claude outputs/COLDWAR_EGY_generator/cw_build.py',
             ROOT/'Claude outputs/COLDWAR_EGY_generator/cw_effects.py']
    for path in targets:
        original=text=path.read_text(encoding='utf-8-sig')
        text=text.replace('gfx/Leaders/EGY/EGY_Coldwar_Gamal_Abdel_Nasser.dds',picture('nasser'))
        # Only named leaders for which this expansion supplies a portrait are patched.
        def replace(m):
            name=m.group(1)
            if name not in by_name: return m.group(0)
            content=re.sub(r'\s+picture = "[^"]+"','',m.group(2))
            return f'create_country_leader = {{ name = "{name}" picture = "{picture(by_name[name])}"{content}'
        text=re.sub(r'create_country_leader = \{ name = "([^"]+)"([^\n]*)',replace,text)
        if path.name=='COLDWAR_EGY_1970_focus.txt':
            pieces=re.split(r'(?m)(^\tfocus = \{)',text)
            for i,part in enumerate(pieces):
                fid=re.search(r'^\s*id = (\w+)',part)
                if not fid or 'power_to' not in fid[1]: continue
                line=re.search(r'create_country_leader = \{ name = "([^"]+)"([^\n]*)',part)
                if not line or 'picture =' in line[0]: continue
                ideology=re.search(r'ideology = (\w+)',line[0])[1]
                idx=IDEOLOGIES.index(ideology)
                key=PARTIES[idx][2]
                new_line=line[0].replace(f'name = "{line[1]}"',f'name = "{NAMES[key]}" picture = "{picture(key)}"',1)
                part=part.replace(line[0],new_line,1)
                part=re.sub(r'COLDWAR_EGY_new_leader_\w+_tt',f'COLDWAR_EGY_1970_new_leader_{key}_tt',part,count=1)
                pieces[i]=part
            text=''.join(pieces)
        if path.name in ('cw_build.py','COLDWAR_EGY_1970_scripted_effects.txt'):
            anchor='COLDWAR_EGY_nasser_dies = {\n'
            if anchor+'\tset_country_flag' not in text:
                text=text.replace(anchor,anchor+'\tset_country_flag = COLDWAR_EGY_nasser_deceased\n',1)
        if path.name=='cw_effects.py' and '# COLDWAR | 1970 portrait overrides' not in text:
            override={name:picture(key) for name,key in by_name.items()}
            code=('\n# COLDWAR | 1970 portrait overrides for all named focus leaders.\n'
                  'LEADER_PORTRAITS_1970 = '+repr(override)+'\n'
                  'LEADER_EN = {k: (name, LEADER_PORTRAITS_1970.get(name, pic))\n'
                  '             for k, (name, pic) in LEADER_EN.items()}\n')
            text=text.replace('\nNEW_TRAITS = ',code+'\nNEW_TRAITS = ',1)
        if path.name=='cw_effects.py' and '# COLDWAR | Party accession casting' not in text:
            cast={i:(NAMES[p[2]],picture(p[2])) for i,p in enumerate(PARTIES)}
            code=('\n# COLDWAR | Party accession casting for formerly unpictured candidates.\n'
                  'COLDWAR_EGY_1970_PARTY_CAST = '+repr(cast)+'\n'
                  'LEADER_EN.update({f"COLDWAR_EGY_1970_candidate_{idx}": value\n'
                  '                  for idx, value in COLDWAR_EGY_1970_PARTY_CAST.items()})\n')
            text=text.replace('\nNEW_TRAITS = ',code+'\nNEW_TRAITS = ',1)
            anchor='        idx = PARTY_BY_NAME[m.group(1)]\n        out = []\n'
            branch=('        idx = PARTY_BY_NAME[m.group(1)]\n'
                    '        if m.group(2) and "power_to" in short and not LEADER_EN.get(m.group(2), (None, None))[1]:\n'
                    '            name_key = f"COLDWAR_EGY_1970_candidate_{idx}"\n'
                    '            leader_name = COLDWAR_EGY_1970_PARTY_CAST[idx][0]\n'
                    '            tooltip_key = f"{PFX}new_leader_{slug(leader_name)}_tt"\n'
                    '            R.tt[tooltip_key] = f"§Y{leader_name}§! becomes the leader of [ROOT.GetNameDef]."\n'
                    '            return [f"custom_effect_tooltip = {tooltip_key}", "hidden_effect = {"] + leader(idx, name_key) + ["}"] + ruling_party(idx)\n'
                    '        out = []\n')
            assert anchor in text
            text=text.replace(anchor,branch,1)
        if text != original: path.write_text(text,encoding='utf-8',newline='\n')
    # Preserve the existing global historical-party override, but route Egypt to
    # the same icon/name as its 1970 party list.
    path=ROOT/'common/scripted_localisation/IMP_1970_party_name_scripted_localisation.txt'
    original=text=path.read_text(encoding='utf-8-sig')
    text=text.replace('original_tag = EGY } localization_key = IMP_1970_EGY_STARTING_PARTY',
                      'original_tag = EGY } localization_key = COLDWAR_EGY_1970_party_18')
    anchor='\ttext = { trigger = { original_tag = EGY } localization_key = COLDWAR_EGY_1970_party_18 }'
    alt='\ttext = { trigger = { original_tag = EGY has_country_flag = COLDWAR_EGY_1970_socialist_alliance } localization_key = COLDWAR_EGY_1970_party_18_alliance }\n'
    if alt not in text: text=text.replace(anchor,alt+anchor,1)
    if text != original: path.write_text(text,encoding='utf-8',newline='\n')

if __name__=='__main__':
    icons=sprites_and_localisation()
    keys=portraits(icons)
    effects()
    characters()
    connect_history_and_focus()
    manifest={'scenario':'1970.1.1','later_parties_retained':True,'photo_prompt':PHOTO_PROMPT,
              'parties':[dict(index=i,ideology=IDEOLOGIES[i],name=p[0],leader=NAMES[p[2]],
                              portrait=picture(p[2]),historical_note=p[3]) for i,p in enumerate(PARTIES)],
              'military':[dict(key=m[0],name=NAMES[m[0]],role=m[1],advisor_slot=m[3],recall_from=m[5]) for m in MILITARY],
              'missing_portraits':[key for key in sorted(keys) if not (PORTRAITS/f'{key}.dds').exists()]}
    (HERE/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False),encoding='utf-8')
    print('Built 24 party names/descriptions/icons, 24 leader choices, 10 military characters.')
    print('Missing portrait assets:',', '.join(manifest['missing_portraits']) or 'none')
