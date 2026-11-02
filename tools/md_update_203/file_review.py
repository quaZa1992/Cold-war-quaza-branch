# IMPERIA COLD WAR — Concrete individual source choices for MD 2.0.3.
"""Generate a read-only, file-by-file explanation from verified review reports."""
from pathlib import Path
import difflib
import json
import re

from audit import ROOT,OUT,UP,PROJECT

DEST=Path('C:/Users/Enes/.codex/visualizations/2026/10/27/01a17ef9-3adf-7210-95e8-0788b3b5a632/md-203-file-review.html')
EMPTY_PURPOSE={
 'common/decisions/categories/MD_auto_agency_category.txt':'Früher: die Entscheidungskategorie der zusätzlichen Agentur-Warteschlange.',
 'common/decisions/MD_auto_agency_decisions.txt':'Früher: Entscheidungen zum Einreihen und Verwalten von Agentur-Upgrades.',
 'common/ideas/MD_auto_agency_ideas.txt':'Früher: nationale Modifier für die zusätzliche Agentur-Warteschlange.',
 'common/modifier_definitions/MD_auto_agency_modifier_definitions.txt':'Früher: eigene Modifier-Definitionen für das alte Warteschlangensystem.',
 'common/on_actions/MD_auto_agency_on_actions.txt':'Früher: automatische regelmäßige Aufrufe der alten Agentur-Warteschlange.',
 'common/scripted_effects/00_MD_auto_agency_scripted_effects.txt':'Früher: ausführbare Funktionen der zusätzlichen Agentur-Warteschlange.',
 'common/scripted_guis/00_MD_auto_agency_scripted_gui.txt':'Früher: Schaltflächen und Bedingungen des zusätzlichen Warteschlangenfensters.',
 'common/scripted_localisation/00_MD_auto_agency_scripted_localisation.txt':'Früher: dynamische Statusanzeigen der alten Agentur-Warteschlange.',
 'common/scripted_triggers/00_MD_auto_agency_scripted_triggers.txt':'Früher: Voraussetzungen und Prüfungen für die zusätzliche Warteschlange.',
 'events/MD_auto_agency_events.txt':'Früher: Ereignisse des zusätzlichen Warteschlangensystems.',
 'interface/MD_auto_agency_queue.gui':'Früher: das zusätzliche Agentur-Warteschlangenfenster.',
 'localisation/english/MD_auto_agency_l_english.yml':'Früher: englische Beschriftungen und Tooltips der zusätzlichen Warteschlange.'}
CUSTOM={
 'common/intelligence_agency_upgrades/intelligence_agency_upgrades.txt':'Unsere Erfassung fertiggestellter passiver Abwehr für Nuklearaufklärung und unsere zeitgerechten Geheimdienstgrafiken bleiben erhalten.',
 'common/on_actions/MD_on_actions.txt':'Unsere Gastarbeiter-Überweisungen, 1970-Datumsgrenzen und die Reservewährungs-Buchung bleiben erhalten.',
 'common/scripted_diplomatic_actions/00_scripted_diplomatic_actions.txt':'Die Eingänge im Supermacht-Dossier bei Handelsangebot, Annahme und Ablehnung bleiben erhalten.',
 'common/scripted_guis/00_missiles_scripted_guis.txt':'Unsere Space-Race-, Satelliten- und internationalen Systeme bleiben erhalten. Der alte MD-Satellitenfilter ist bereits entfernt.',
 'common/synchronized_dynamic_tokens/MD_tokens.txt':'Unsere Uran-, Minen-, Energie- und Ressourcenanzeigen behalten ihre registrierten Kennungen.',
 'interface/alerts.gui':'Der zusätzliche Platz für unseren COMECON-Button bleibt erhalten.',
 'interface/countrytechtreeview.gui':'Unsere frühen Forschungstechnologien, zusätzlichen Zweige und ihre Positionen bleiben erhalten.',
 'interface/countrytradeview.gui':'Unser Handelsfenster behält neun Ressourcen samt Uran und die dazu passenden Breiten und Abstände.',
 'interface/general_stuff.gfx':'Die Ressourcenleisten behalten neun Bildfelder einschließlich Uran.',
 'interface/MD_countrymissilesview.gui':'Unser Space-Race-Button und die kompakte Liste für internationale Anerkennung bleiben erhalten.',
 'localisation/english/MD_missiles_l_english.yml':'Unsere Satellitenbeschreibungen bleiben passend zu den tatsächlichen Cold-War-Boni.',
 'localisation/english/research_l_english.yml':'Die beiden neuen MD-Tastatur-Tooltips sind bereits wortgleich enthalten. Unsere zusätzlichen Forschungstexte bleiben erhalten.'}


def sections(name,left,right):
    value=(OUT/name).read_text(encoding='utf-8');result={}
    pattern=re.compile(r'^--- '+re.escape(left)+r'/(.*?)\n\+\+\+ '+re.escape(right)+r'/.*?\n',re.M)
    matches=list(pattern.finditer(value))
    for i,m in enumerate(matches):result[m[1]]=value[m.start():matches[i+1].start() if i+1<len(matches) else len(value)]
    return result


def main():
    plan=json.loads((OUT/'adoption_plan.json').read_text(encoding='utf-8'))
    upstream=sections('upstream_delta.diff','verified_old_MD','supplied_MD')
    local=sections('local_preservation.diff','supplied_MD','Cold_War')
    rows=[]
    for entry in plan['files']:
        p=entry['path'];action=entry['action'];current=ROOT/p
        raw=current.read_bytes() if current.is_file() else None
        content=raw.decode('utf-8-sig') if raw and current.suffix not in ('.png',) else ''
        row=dict(path=p,upstream_diff=upstream.get(p,''),local_diff=local.get(p,''),content='',proposal_diff='',
            impact='Bisher keine Änderung an der aktiven Mod durch diesen Vergleich.',purpose='')
        if action=='ASK_REMOVE_EMPTY_LEGACY_FILE':
            row.update(group='Leere Altdateien entfernen',purpose=EMPTY_PURPOSE[p],ours='Bereits leer: nur ein Kommentar'+(' und der Sprachkopf l_english.' if p.endswith('.yml') else '.'),
                md='Die Datei existiert in der neuen MD-Version nicht mehr.',proposal='Diese einzelne leere Datei entfernen.',
                impact='Das Löschen entfernt keinen aktuell ausführbaren Code. Die native Agentur-Warteschlange und unsere separate SSR-Geheimdienstsperre bleiben bestehen.',content=content,
                proposal_diff=''.join(difflib.unified_diff(content.splitlines(True),[],fromfile=p,tofile='/dev/null')))
        elif action in ('ASK_SYNC_EXISTING_VERSION_LABELS','ASK_UPDATE_METADATA_KEEP_IDENTITY','ASK_UPDATE_UPSTREAM_NOTE'):
            row['group']='Versionen und Beschreibung'
            if p=='descriptor.mod':
                row.update(purpose='Metadaten für den Mod-Launcher.',ours='Version 2.0.2, Name MD Cold War und unsere zusätzlichen replace_path-Einträge.',
                    md='Version 2.0.3, Name Millennium Dawn: A Modern Day Mod und die Standard-MD-Pfade.',proposal='Nur die Versionsnummer auf 2.0.3 setzen. Unseren Namen und unsere Pfade behalten.')
                proposed=content.replace('version="2.0.2"','version="2.0.3"',1)
            elif p=='Changelog.txt':
                row.update(purpose='Textdatei mit den bisherigen MD-Änderungsnotizen.',ours='Längere MD-2.0.2-Notizen zu KI, Balance und Fehlerbehebungen.',
                    md='Kurzer Hinweis zu reparierten Bedienelementen, Tastenkürzeln, Forschungstexten und der nativen Agentur-Warteschlange. Die gelieferte Datei trägt selbst noch die Überschrift v2.0.2.',
                    proposal='Die aktuelle MD-Notiz übernehmen und als Herkunftsangabe kennzeichnen. Die älteren Notizen bleiben im Prüf-Diff nachvollziehbar.')
                proposed=(UP/p).read_text(encoding='utf-8-sig')
            else:
                row.update(purpose='Vorhandene Versionsanzeige'+(' in der Modbeschreibung.' if p.startswith('descriptions/') else ' in der Oberfläche.'),
                    ours='Die vorhandenen Texte nennen noch v2.0.2.',md='Dieselben vorhandenen Texte nennen v2.0.3.',proposal='Nur 2.0.2 durch 2.0.3 ersetzen. Keine neuen Übersetzungen, keine Gameplay-Änderung.')
                proposed=content.replace('2.0.2','2.0.3')
            row['proposal_diff']=''.join(difflib.unified_diff(content.splitlines(True),proposed.splitlines(True),fromfile='aktuell/'+p,tofile='Vorschlag/'+p,n=3))
        elif action=='EXCLUDE_SOURCE_DEVELOPMENT_ARTIFACT':
            row.update(group='Entwicklungsbilder im MD-Ordner',purpose='Eine Vorschaugrafik zu einem Cold-War-Ägypten-Fokusbaum.',ours='Diese Datei ist in unserer Mod an diesem Pfad nicht vorhanden.',
                md='Die PNG liegt im Entwicklungsordner Claude outputs des angegebenen MD-Verzeichnisses.',proposal='Nicht in unsere Mod kopieren.',
                impact='Kein geladenes Spielskript. An der MD-Quelle wird nichts gelöscht.')
        else:
            row['group']='Bereits integriert: beibehalten'
            row['purpose']=CUSTOM.get(p,'Betroffene Datei des MD-Hotfixes. Der vollständige Original-Patch ist unten aufklappbar.')
            row['ours']='Die neue MD-Funktionalität ist bereits enthalten.'
            row['md']='Die im Original-Patch gezeigten UI-, Queue- oder Filterkorrekturen.'
            row['proposal']=CUSTOM.get(p,'Unsere aktuelle Datei behalten. Ihr ausführbarer Inhalt beziehungsweise ihre relevanten MD-Textwerte entsprechen bereits der neuen Quelle.')
            row['impact']='Keine erneute Übernahme der ganzen MD-Datei erforderlich.'
            if p=='common/technology_tags/00_technology.txt':row.update(purpose='Forschungskategorien.',md='Nur ein Unterschied in der Formatierung; keine neue Forschungskategorie.')
            if p.endswith('/README.md'):row.update(purpose='Entwicklerdokumentation für Geheimdienst-Upgrades.',ours='Bereits vollständig identisch mit der neuen MD-Datei.',md='Beschreibung des nativen Geheimdienstfensters und seiner Upgrade-Definitionen.')
        rows.append(row)
    order={'Leere Altdateien entfernen':0,'Versionen und Beschreibung':1,'Bereits integriert: beibehalten':2,'Entwicklungsbilder im MD-Ordner':3}
    rows.sort(key=lambda r:(order[r['group']],r['path']))
    data=json.dumps(rows,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
    template=Path(__file__).with_suffix('.html').read_text(encoding='utf-8')
    html=template.replace('<!-- MD203_DATA -->','<script type="application/json" id="md203-data">'+data+'</script>')
    assert len(html.encode('utf-8'))<1_000_000
    DEST.write_text(html,encoding='utf-8')
    print(json.dumps(dict(project=PROJECT,files=len(rows),bytes=len(html.encode('utf-8')),output=str(DEST),runtime_writes=0)))


if __name__=='__main__':main()
