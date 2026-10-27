# IMPERIA CW — Cold War: recipient replies and reliable Japan offer dispatch.
"""Generate sender reports; agreement payments remain in recipient transactions."""
import json
from pathlib import Path
import re
from check_script_grammar import parse
from presentation import field
from foreign_presentation import offer_tooltip

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=HERE/'staging/foreign'
PROJECTS={'seoul_industrial_cooperation','asean_infrastructure','mekong_development','indochina_reconstruction'}


def quote(value):
    return '"'+value.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n')+'"'


def emit(path,text):
    # Effects and events deliberately share their active basename, so their
    # canonical staged sources must occupy different directories.
    staged=(OUT/path.parent.name/path.name if path.name=='COLDWAR_JAP70_diplomatic_reports.txt' else OUT/path.name)
    staged.parent.mkdir(parents=True,exist_ok=True)
    data=text.encode('utf-8-sig' if path.suffix=='.yml' else 'utf-8')
    for target in (staged,path):
        temporary=target.with_suffix(target.suffix+'.tmp')
        temporary.write_bytes(data)
        temporary.replace(target)


def main():
    transactions=[json.loads(l) for l in (OUT/'bilateral_manifest.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    registry={r['focus']:r for r in json.loads((OUT/'foreign_helper_registry.json').read_text(encoding='utf-8'))}
    prefix='COLDWAR_JAP70_'
    header='# IMPERIA CW — Cold War: Japanese diplomatic response reports.\n'
    helpers=[header]
    events=[header,'add_namespace = COLDWAR_JAP70_REPORT\n']
    loc=['l_english:',' COLDWAR_JAP70_report_acknowledge: "Acknowledge the report"']
    manifest=[]
    event_index=1
    for t in transactions:
        focus=t['focus']
        for outcome in ('accepted','refused',*(['completed'] if focus in PROJECTS else [])):
            key=prefix+'notice_'+focus+'_'+outcome
            receipt=prefix+focus+('_project_reported' if outcome=='completed' else '_response_reported')
            event='COLDWAR_JAP70_REPORT.'+str(event_index)
            event_index+=1
            helpers += [f'{key} = {{', '\tif = {',
                        f'\t\tlimit = {{ NOT = {{ tag = JAP }} country_exists = JAP NOT = {{ has_country_flag = {receipt} }} }}',
                        f'\t\tset_country_flag = {receipt}',
                        f'\t\tset_country_flag = {prefix}{focus}_{outcome}',
                        f'\t\tJAP = {{ country_event = {{ id = {event} hours = 1 }} }}', '\t}', '}\n']
            title={'accepted':'Financing Approved' if focus in PROJECTS else 'Agreement Accepted',
                   'refused':'Proposal Declined','completed':'Project Completed'}[outcome]
            title='$COLDWAR_JAP_1970_'+focus+'$: '+title
            if outcome=='refused':
                description='[FROM.GetNameDefCap] has declined our proposal. The proposed agreement will not take effect.'
                tooltip='This proposal incurs no expenditure and grants no agreement bonuses.'
            elif outcome=='accepted' and focus in PROJECTS:
                description='[FROM.GetNameDefCap] has approved our financing offer. Its government can now select a project location.'
                tooltip='The recipient may select a location under §YRecipient-Selected Development Projects§!. Japan pays when the project is completed.'
            else:
                description=('[FROM.GetNameDefCap] has completed the agreed development project. The expenditure and benefits have been applied.'
                             if outcome=='completed' else '[FROM.GetNameDefCap] has accepted our proposal. The agreement is now in effect.')
                preview=offer_tooltip(registry[focus],t).splitlines()
                # The first three lines identify the offer and the conditional
                # trigger. The remaining lines are the already-applied terms.
                start=next(i for i,line in enumerate(preview) if line.startswith('  ') and 'Treasury:' in line)
                tooltip='§YAlready applied:§!\n'+'\n'.join(preview[start:])
            loc += [f' {key}_title: {quote(title)}',f' {key}_desc: {quote(description)}',f' {key}_tt: {quote(tooltip)}']
            events += ['country_event = {',f'\tid = {event}','\tis_triggered_only = yes','\tpicture = GFX_treaty',
                       f'\ttitle = {key}_title',f'\tdesc = {key}_desc',
                       '\toption = {','\t\tname = COLDWAR_JAP70_report_acknowledge',f'\t\tcustom_effect_tooltip = {key}_tt','\t}','}\n']
            manifest.append({'focus':focus,'outcome':outcome,'helper':key,'event':event,'scope':'recipient -> JAP; FROM is the responding recipient'})
    # Recover only genuinely unanswered direct offers from already completed
    # focuses in existing saves. A resolved or still-pending recipient is never
    # contacted again; no payment or benefit is executed by this migration.
    recovery=['COLDWAR_JAP70_restore_unanswered_offers = {', '\tif = {',
              '\t\tlimit = { original_tag = JAP IMP_is_1970_scenario = yes NOT = { has_country_flag = COLDWAR_JAP70_response_recovery_v1 } }']
    for t in transactions:
        targets=([t['recipient']] if t.get('recipient') else t.get('recipients',[]))
        for index,tag in enumerate(targets):
            focus=t['focus']
            resolved=(t.get('resolved_flag') or f'COLDWAR_JAP70_BIL_{focus}'+(f'_{tag}' if t.get('recipients') else '')+'_resolved')
            pending=resolved.removesuffix('_resolved')+'_pending'
            event=t['events'][index] if t.get('events') else t.get('event',t.get('offer_event'))
            if not event:raise ValueError('Missing recovery event '+focus)
            receipt=t['helper']+'_receipt'
            recovery += ['\t\tif = {',f'\t\t\tlimit = {{ has_completed_focus = COLDWAR_JAP_1970_{focus} {tag} = {{ exists = yes NOT = {{ has_country_flag = {pending} }} NOT = {{ has_country_flag = {resolved} }} }} }}',
                         f'\t\t\tset_country_flag = {receipt}',
                         f'\t\t\t{tag} = {{ set_country_flag = {pending} country_event = {{ id = {event} }} }}', '\t\t}']
    recovery += ['\t\tset_country_flag = COLDWAR_JAP70_response_recovery_v1','\t}','}\n']
    helpers.extend(recovery)
    for text in ('\n'.join(helpers),'\n'.join(events)):parse(text)
    emit(ROOT/'common/scripted_effects/COLDWAR_JAP70_diplomatic_reports.txt','\n'.join(helpers)+'\n')
    emit(ROOT/'events/COLDWAR_JAP70_diplomatic_reports.txt','\n'.join(events)+'\n')
    emit(ROOT/'localisation/english/COLDWAR_JAP70_diplomatic_reports_l_english.yml','\n'.join(loc)+'\n')
    emit(ROOT/'common/on_actions/COLDWAR_JAP70_diplomatic_recovery.txt',header+'on_actions = {\n\ton_daily_JAP = {\n\t\teffect = { COLDWAR_JAP70_restore_unanswered_offers = yes }\n\t}\n}\n')
    (OUT/'diplomatic_reports_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')

    # A receipt represents an actual dispatch, rather than an attempted call
    # whose recipient had disappeared or already answered.
    path=ROOT/'common/scripted_effects/COLDWAR_JAP70_bilateral_effects.txt'
    text=(OUT/path.name).read_text(encoding='utf-8')
    single=[t for t in transactions if t.get('recipient')]
    for t in single:
        focus=t['focus'];tag=t['recipient']
        receipt=f'COLDWAR_JAP70_FOREIGN_{focus}_offer_receipt'
        # Move the receipt into the target-validated dispatch body. The
        # replacement is idempotent and leaves every existing runtime guard.
        text=re.sub(r'(?m)^  set_country_flag = '+re.escape(receipt)+r'\n','',text)
        pending=f'COLDWAR_JAP70_BIL_{focus}_pending'
        old=f'{tag} = {{ set_country_flag = {pending} country_event = '
        new=f'set_country_flag = {receipt}\n  '+old
        if new not in text:
            if old not in text:raise ValueError('Missing dispatch body '+focus)
            text=text.replace(old,new,1)
    parse(text)
    emit(path,text)
    print(f'Installed {len(manifest)} sender reports covering {len(transactions)} offers and four project completions; {len(single)} dispatch receipts now follow recipient validation.')


if __name__=='__main__':main()
