# IMPERIA COLD WAR — Native USA/Soviet dossiers and read-only diplomatic correspondence
"""Build only this feature. Existing diplomatic actions keep ownership of gameplay."""
from pathlib import Path
import hashlib
import json
import re
import os
import time
from PIL import Image, ImageDraw, ImageFont
from runtime import KINDS

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
MARK = '# IMPERIA COLD WAR — USA and Soviet intelligence dossiers\n'
PREFIX = 'icsd'
OUTPUTS = []
LOCS = {}


def native_loops(text):
    # Native for_each_scope_loop has no limit property. Conditions belong inside an if.
    for match in reversed(list(re.finditer(r'for_each_scope_loop\s*=\s*\{',text))):
        a=match.end();i=a;depth=1
        while depth:depth+=(text[i]=='{')-(text[i]=='}');i+=1
        chunk=text[a:i-1]
        for m in re.finditer(r'\blimit\s*=\s*\{',chunk):
            if chunk[:m.start()].count('{')!=chunk[:m.start()].count('}'):continue
            q=m.end();j=q;d=1
            while d:d+=(chunk[j]=='{')-(chunk[j]=='}');j+=1
            chunk=chunk[:m.start()]+'if = { limit = {'+chunk[q:j-1]+'}'+chunk[j:]+' }'
            text=text[:a]+chunk+text[i-1:]
            break
    return text


def write(rel, text):
    if rel.startswith(('common/scripted_effects/ICW_superpower','events/ICW_superpower')):
        text = native_loops(text)
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    payload=text.encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8')
    if not p.exists() or p.read_bytes()!=payload:
        # A file watcher must not leave a half-written native script behind.
        assert p.resolve().is_relative_to(ROOT.resolve())
        temporary=p.with_name(p.name+'.icwt-writing')
        for attempt in range(5):
            try:
                temporary.write_bytes(payload)
                os.replace(temporary,p)
                break
            except OSError as error:
                if attempt==4 or error.errno not in (13,22):raise
                time.sleep(.05)
    OUTPUTS.append(rel)


def loc(key, text):
    assert not any(c in text for c in '\u2013\u2014')
    LOCS[key] = text.replace('\n', '\\n').replace('"', "'")
    return key


def block(name, body):
    return name + ' = {\n' + body + '\n}\n'


def defined(name, rows, fallback='icsd_empty'):
    return block('defined_text', 'name = ' + name + '\n' + '\n'.join(
        f'text = {{ trigger = {{ {test} }} localization_key = {key} }}' for test, key in rows
    ) + f'\ntext = {{ localization_key = {fallback} }}')


def build_runtime():
    from runtime import build
    build(write, block, MARK)


def patch_native_observers():
    """Insert only metadata callbacks; preserve exact provider execution and fees."""
    specs = [('common/scripted_diplomatic_actions/00_scripted_diplomatic_actions.txt', 'propose_improved_trade_agreement', 'trade'),
             ('common/scripted_diplomatic_actions/imp_money_transfer_diplomatic_actions.txt', 'imp_money_transfer', 'money')]
    integrations = []
    for rel, action, topic in specs:
        p = ROOT / rel
        before = p.read_text(encoding='utf-8-sig')
        source = before
        marker = '# IMPERIA COLD WAR — Superpower dossier correspondence observer integration\n'
        if not source.startswith(marker):
            source = marker + source
        # A balanced scan limits callbacks to the intended action, not subsidies or other agreements.
        start = re.search(r'\b' + action + r'\s*=\s*\{', source).end()
        depth, quoted, end = 1, False, start
        while depth:
            c = source[end]
            if c == '"': quoted = not quoted
            if not quoted:
                depth += (c == '{') - (c == '}')
            end += 1
        fragment = source[start:end-1]
        for field, verb in [('on_sent_effect','sent'), ('complete_effect','accepted'), ('reject_effect','declined')]:
            callback = f'icsd_note_{topic}_{verb} = yes'
            if callback not in fragment:
                fragment, count = re.subn(r'(\b' + field + r'\s*=\s*\{)', r'\1\n\t\t\t# IMPERIA COLD WAR — Read-only correspondence receipt\n\t\t\t' + callback, fragment, count=1)
                assert count == 1, (rel, action, field)
        source = source[:start] + fragment + source[end-1:]
        if source != before:
            assert p.read_text(encoding='utf-8-sig') == before, 'Concurrent provider edit: retry from current source'
            p.write_text(source, encoding='utf-8', newline='\n')
        integrations.append(rel)
    from integrations import patch
    return integrations + patch(ROOT)


def build_art():
    from presentation import make_art
    make_art(ROOT, HERE, MARK, write)


def build_ui():
    data={'icsd_empty':'','icsd_category':'Superpower Diplomacy','icsd_category_desc':'Foreign intelligence dossiers and diplomatic correspondence for Washington and Moscow.',
          'icsd_open_decision':'Open Intelligence Dossier','icsd_open_decision_desc':'Review current American and Soviet commitments, diplomatic correspondence and available diplomatic responses.',
          'icsd_open_tt':'Open the intelligence dossier.','icsd_title_usa':'CENTRAL INTELLIGENCE AGENCY','icsd_title_sov':'COMMITTEE FOR STATE SECURITY',
          'icsd_sub_usa':'Superpower Affairs: Directorate of Intelligence','icsd_sub_sov':'Special Intelligence File: First Chief Directorate',
          'icsd_register':'CONTROLLED DISTRIBUTION','icsd_footer':'USA AND USSR ONLY   |   FOREIGN INTELLIGENCE FILE',
          'icsd_tab_1':'Field Reports','icsd_tab_2':'Diplomatic Offers','icsd_tab_3':'Current Commitments','icsd_prev':'Previous','icsd_next':'Next',
          'icsd_page':'Page [?icsd_page|0]   |   [?icsd_view_count|0] records','icsd_no_records':'No records are available.','icsd_pick':'Choose response country',
          'icsd_pick_tt':'Close the file, select a country on the map and use the dossier target button in its country view.',
          'icsd_picker_label':'Use this country for dossier response','icsd_picker_cancel':'Cancel dossier selection','icsd_locate':'Locate response country',
          'icsd_response_none':'Response country: not selected','icsd_response_set':'Response country: [?icsd_response_target.GetName]',
          'icsd_select_prompt':'Select a record from the file index.','icsd_desc_1':'An active lend-lease connection is recorded. Exact delivered quantities are not available from this connection record.',
          'icsd_desc_2':'Volunteer forces from the provider are present in the recipient country.','icsd_desc_3':'A military attache from the provider is assigned to the recipient country.',
          'icsd_desc_4':'Existing Imperia sanctions imposed by the provider are recorded against the recipient.',
          'icsd_desc_5':'The existing MD improved trade agreement is recorded between these countries.',
          'icsd_desc_6':'The existing MD trade action generated this diplomatic correspondence. Replies are handled through the normal diplomatic offer.',
          'icsd_desc_7':'The existing Imperia money-transfer action generated this correspondence. Replies and treasury transfers use the normal diplomatic offer.',
          'icsd_detail_title':'[?icsd_selected_target.GetName]','icsd_detail_facts':'Provider: [?icsd_selected_actor.GetName]\nRecipient: [?icsd_selected_target.GetName]\nRecord: [icsd_selected_kind_L]\nStatus: [icsd_selected_state_L]\nObserved: [?icsd_selected_date.GetDateStringNoHourLong]\n[icsd_transfer_line]',
          'icsd_amount':'Transfer amount: $[?icsd_selected_amount|2] billion',
          'icsd_guide':'Right-click the chosen country on the map to open diplomacy. Select the action below. Normal costs, permissions and recipient responses apply.',
          'icsd_correspondence_note':'Correspondence records an observed send or reply. It does not replace the native offer window.',
          'icsd_actions':'AVAILABLE DIPLOMATIC ACTIONS','icsd_lend':'Lend-lease','icsd_volunteers':'Volunteer forces','icsd_attache':'Military attache',
          'icsd_money':'Transfer money','icsd_sanctions':'Imperia sanctions','icsd_trade':'Improved trade agreement','icsd_back':'Back to actions',
          'icsd_route_1':'Diplomacy > Lend-lease\nChoose equipment, amount and schedule from your stockpile or production. End your own existing connection through the current lend-lease controls.',
          'icsd_route_2':'Diplomacy > Send volunteers\nChoose your own eligible divisions. Use the normal recall action to withdraw an existing deployment.',
          'icsd_route_3':'Diplomacy > Send military attache\nNative political-power, command-power and recipient requirements apply. Recall your own existing mission through diplomacy.',
          'icsd_route_4':'Diplomacy > Transfer money\nChoose the amount from your treasury. The recipient accepts or refuses the existing Imperia offer.',
          'icsd_route_5':'Diplomacy > Sanctions\nExisting diplomatic, financial, economic and military sanctions are available. Each impose or lift action costs 35 political power.',
          'icsd_route_6':'Diplomacy > Improved trade agreement\nProposal cost: 75 political power. Native peace, opinion, embassy and recipient-acceptance conditions apply.',
          'icsd_kind_1':'Lend-lease','icsd_kind_2':'Volunteer deployment','icsd_kind_3':'Military attache','icsd_kind_4':'Imperia sanctions','icsd_kind_5':'Improved trade agreement','icsd_kind_6':'Trade correspondence','icsd_kind_7':'Money transfer',
          'icsd_state_0':'Recorded active','icsd_state_1':'Proposal sent','icsd_state_2':'Accepted','icsd_state_3':'Declined'}
    from ui import extend
    extra_scripts = extend(data, loc, defined)
    scripts = [MARK]
    scripts.append(defined('icsd_title',[('tag = USA','icsd_title_usa')], 'icsd_title_sov'))
    scripts.append(defined('icsd_subtitle',[('tag = USA','icsd_sub_usa')], 'icsd_sub_sov'))
    for field in ('kind','state'):
        rows=[(f'check_variable = {{ icsd_selected_{field} = {i} }}',f'icsd_{field}_{i}') for i in (KINDS if field=='kind' else range(6))]
        scripts.append(defined(f'icsd_selected_{field}_L',rows))
    scripts.append(defined('icsd_description',[(f'check_variable = {{ icsd_selected_kind = {i} }}',f'icsd_desc_{i}') for i in KINDS],'icsd_select_prompt'))
    scripts.append(defined('icsd_route_text',[(f'check_variable = {{ icsd_route = {i} }}',f'icsd_route_{i}') for i in range(1,13)],'icsd_guide'))
    scripts.append(defined('icsd_response_label',[('check_variable = { icsd_response_target > 0 }','icsd_response_set')],'icsd_response_none'))
    scripts.append(defined('icsd_transfer_line',[('check_variable = { icsd_selected_kind = 7 }','icsd_amount')]))
    for i in range(5):
        loc(f'icsd_row_{i}',f'[?icsd_r{i}_target.GetName]\n[icsd_row_{i}_kind]')
        scripts.append(defined(f'icsd_row_{i}_kind',[(f'check_variable = {{ icsd_r{i}_kind = {k} }}',f'icsd_kind_{k}') for k in KINDS]))
    scripts.extend(extra_scripts)
    from presentation import localisation
    scripts.extend(localisation(loc, defined))
    write('common/scripted_localisation/ICW_superpower_dossier.txt',''.join(scripts))
    from presentation import build_ui as native_ui
    native_ui(write, loc, defined, MARK)
    write('localisation/english/ICW_superpower_dossier_l_english.yml','l_english:\n'+MARK+'\n'.join(f' {k}:0 "{v}"' for k,v in LOCS.items())+'\n')


def main():
    build_runtime()
    from treaties import build as treaty_runtime
    from treaty_text import build as treaty_text
    treaty_runtime(write, loc, defined, MARK, ROOT, HERE)
    treaty_text(write, loc, defined, MARK)
    build_art();build_ui();integrations=patch_native_observers()
    from treaty_integrations import patch as treaty_integrations
    integrations += treaty_integrations(ROOT)
    manifest={'project':'IMPERIA COLD WAR','generated':OUTPUTS,'integrations':integrations,'sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in OUTPUTS+integrations}}
    (HERE/'generated.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'project':'IMPERIA COLD WAR','generated':len(OUTPUTS),'integrations':integrations},indent=2))


if __name__=='__main__':main()
