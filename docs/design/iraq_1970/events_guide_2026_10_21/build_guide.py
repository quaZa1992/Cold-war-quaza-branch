# IMPERIA CW — Cold War: read-only event/decision catalogue for multiplayer explanation.
"""Snapshot loaded scripts and English text; never regenerate gameplay content."""
from pathlib import Path
import base64,gzip,hashlib,json,re,sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path[:0]=[str(ROOT/'tools/vietnam_1970'),str(ROOT/'tools/iraq_1970')]
from script_ast import parse,first,values,walk,emit
from audit_design import load_design
DEST=Path('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82/iraq-events-decisions.html')

LOC={}
MD=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')
for base in [MD,ROOT]:
 for p in sorted((base/'localisation/english').glob('*.yml')):
  for m in re.finditer(r'^\s*([^\s:#]+):\d*\s+"(.*)"\s*(?:#.*)?$',p.read_text(encoding='utf-8-sig',errors='replace'),re.M):LOC[m[1]]=m[2].replace('\\"','"').replace('\\n','\n')
def loc(s):
 if not isinstance(s,str):return str(s or '')
 s=LOC.get(s,s)
 for _ in range(5):
  n=re.sub(r'\$([^$]+)\$',lambda m:LOC.get(m[1],m[0]),s)
  if s==n:break
  s=n
 return re.sub(r'§.','',s)

providers={};provider_sources={};hashes={};trees={}
def read(p):
 p=ROOT/p;text=p.read_text(encoding='utf-8-sig');hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest();return text,parse(text)
for p in sorted((ROOT/'common/scripted_effects').glob('COLDWAR_*.txt')):
 if not any(k in p.name for k in ['COLDWAR_IRQ','COLDWAR_USA_gulf']):continue
 _,a=read(p.relative_to(ROOT))
 for k,op,v in a:
  if isinstance(v,list):providers[k]=v;provider_sources[k]=str(p.relative_to(ROOT))

def closure(rows):
 found={};todo=[k for k,op,v in walk(rows) if k in providers and v=='yes']
 while todo:
  k=todo.pop()
  if k in found:continue
  found[k]=providers[k]
  todo += [j for j,op,v in walk(providers[k]) if j in providers and v=='yes' and j not in found]
 return found
def eventrefs(rows):return list(dict.fromkeys(first(v,'id') for k,op,v in walk(rows) if k=='country_event' and isinstance(v,list)))
def line(text,pattern):
 m=re.search(pattern,text,re.M);return text.count('\n',0,m.start())+1 if m else None
def position(file,text,key,event=False):return {'file':file,'line':line(text,r'^\s*'+(r'id\s*=\s*' if event else '')+re.escape(key)+(r'\s*$' if event else r'\s*=\s*\{'))}

COMMENTS={
 'army_priority_review':'Echte nachträgliche Umschaltung: 75 PP für das Menü, weitere 1% BIP bei Umsetzung. Schon eine der beiden umgesetzten Armee-Fokuswahlen genügt. Garde: +3% Organisation, +4% Verteidigung, +10% Personalaufwand; reguläre Armee: +6% Erholung, −8% Ausbildungsdauer, +4% Personalaufwand. Fokusabzeichen und einmalige Investitionen wechseln dadurch nicht. Das relativiert die dauerhafte Exklusivität.',
 'constitutional_settlement_review':'100 PP für die Konferenz, 1% BIP für Ratifikation. Wählt exekutive oder repräsentative Verfassungsgewalt. Unvereinbare aktive Programme werden entsprechend ausgesetzt; keine Partei wird allein dadurch zur Regierung.',
 'political_opening':'75 PP. Annahme kostet 1% BIP, legalisiert die Kommunisten und aktiviert politische Garantien: Bürokratieaufwand +3%, ideologische Abwehr −4%. Ablehnung: Stabilität −1 Punkt. Bestehende Garantien können aufgehoben werden. Ohne separate Oppositionsnation entscheidet hier derselbe Irakspieler über die Antwort.',
 'prison_review':'30 PP; Freilassung kostet zusätzlich 0,5% BIP. Schützt noch lebende/verfügbare Kandidaten über registrierte Schutz- und Rehabilitationsentscheidungen. Kein Regierungswechsel. Befristeter Verwaltungsaufwand: +4% Bürokratie, −3% PP-Gewinn. Die Kandidatenfristen sind echte Codebedingungen.',
 'march_offer':'60 PP. Bestehen KUR/PUK als Staaten, müssen ihre Spieler im verknüpften Autonomieverfahren zustimmen. Andernfalls ist die Zustimmung der Delegierten eine Auswahl im Irak-Event. Annahme kostet 2% BIP, liefert lokale Verfassungsrechte und laufenden Garantieaufwand; sie verschenkt nicht automatisch Gebiete.',
 'north_fiscal_settlement':'75 PP und 2% BIP bei Ratifikation, nur mit aktivem Nordabkommen und irakischer Kontrolle über Kirkuk. Alle existierenden kurdischen Gegenparteien müssen zustimmen. Einnahmenteilung: Steuereinnahmen −5%, Bürokratie +2%, stärkerer Abbau der Nordbelastung. Zentralverwaltung: Armee-Personalkosten +3%, Bürokratie +1%, engere Garantien bleiben bestehen.',
 'front_offer':'75 PP und 1% BIP bei Annahme. Legalisiert die ICP und trägt Baath/ICP in die tatsächliche Regierungskoalition ein. Wechsel der führenden Partei erfolgt dadurch nicht. Garantien kosten Bürokratie +3% und ideologische Abwehr −4%. Ablehnung: −1 Stabilitätspunkt; späterer Austritt ist möglich.',
 'icp_preaccession':'60 PP. Öffnet Gespräche über Frontteilnahme, legale Opposition oder unabhängige Organisation. Unabhängige Organisation kostet 0,5% BIP, erhöht native Parteieingaben um 2 Punkte und verlässt die Front; kein automatischer Umsturz.',
 'front_labour_terms':'50 PP und 1% BIP für 180 Tage: Produktionseffizienzwachstum +5%, Sozialaufwand +2%. Erfordert eine tatsächlich eingehaltene Frontvereinbarung; keine gleichzeitige Parteimonopol-Mobilisierung.',
 'party_state_mobilization':'50 PP und 1% BIP für 180 Tage: PP-Gewinn +5%, Bürokratieaufwand +2%. Erfordert Baath-Parteimonopol ohne aktive Front. Gegenseitig mit dem Front-Arbeitsprogramm gesperrt.',
 'civic_election':'100 PP. Nur bei erlaubten Wahlen. Zählt über das vorhandene MD-Parteiensystem aus und setzt den tatsächlichen Gewinner ein. Kein garantierter Sieg des bisherigen Spielers; kein separat simulierter parlamentarischer Wahlkampf.',
 'officer_transition':'90 PP. Ratifikation kostet 2% BIP, erlaubt Wahlen und aktiviert politische Garantien. Scheitern der Abstimmung kostet 2 Stabilitätspunkte. Die im Event gewählte Antwort ist keine separat durchgewürfelte Abstimmung.',
 'defence_readiness_cycle':'50 PP plus 0,5% BIP: 90 Tage Organisation +4%, Erholung +4%, Armee-Personalaufwand +4%. 180 Tage Sperrfrist; kein dauerhaftes kostenloses Armeeupgrade.',
 'iran_opening':'75 PP und 2% BIP. Einmal im ersten 30-Tage-Fenster des ersten Iran-Krieges, nach dem passenden Fokus. Kurzkriegsplan: gegen Iran Angriff +8%, Planung +15%, Versorgung +8%, Armeekraftstoff +10% für 90 Tage. Alternativ Dauerplan: +5/+10/+5/+6% für 120 Tage. Beide verursachen 180 Tage +8% Personalaufwand, auch nach frühem Frieden.',
 'iran_followup':'100 PP und 3% BIP. Nach mindestens 90 Kriegstagen, ohne überlappende Offensivboni: 60 Tage +5% Angriff gegen Iran, Versorgung und Armeekraftstoff jeweils +12%. Zusätzliche Personalrechnung +12% für 90 Tage; Frieden beendet diese Rechnung nicht sofort.',
 'iran_disarray':'50 PP und 1% BIP, einmalig. Iran muss tatsächlich Bürgerkrieg haben oder unter 40% Stabilität liegen. Gibt 120 Tage Planungsgeschwindigkeit +10%. Erzeugt keine iranische Revolution.',
 'iran_revoke_settlement':'75 PP. Kündigt das tatsächliche bilaterale Grenz-/Schifffahrtsabkommen einseitig, entfernt seine Vorteile und benachrichtigt Iran. Kein automatischer Krieg.',
 'war_authorization':'150 PP. Wählt Iran, Kuwait oder Syrien nur bei vorhandenem irakischem Anspruch auf den jeweiligen Zielstaat und passenden Diplomatiebedingungen. Gibt 180 Tage Kriegsziel; der Spieler muss separat den Krieg erklären.',
 'war_mediation':'60 PP. Gegner Iran/Kuwait/Syrien kann ablehnen. Annahme führt nur dann zu echtem Weißem Frieden, wenn beide Länder die einzigen Beteiligten ihres bilateralen Krieges sind. Sonst bleibt es eine diplomatische Zusage.',
 'iran_war_aims':'80 PP. Dasselbe Vermittlungsmenü: Frieden anbieten, bisherigen Plan fortsetzen oder eine zulässige neue Offensive finanzieren. Kein erzwungener Frieden und keine automatische Schuldenlöschung.',
 'war_sanctions_diplomacy':'80 PP. Tatsächliche Sanktionierer erhalten eigene Anfragen. Nur der jeweils zustimmende Staat hebt seine eigenen gerichteten Imperia-Sanktionen auf.',
 'oil_market_review':'40 PP für eine Informationsanzeige. Keine Preisänderung, kein Geldbonus, kein Vertrag. Für RP eher unnötige Klicksteuer.',
 'industry_pipeline':'25 PP für Projektübersicht und manuelles Nachholen. Die gleichen ausstehenden Fokusbelohnungen haben kostenlose Nachholknöpfe in der Projektkategorie. Kein eigenständiger Bauauftrag.',
 'society_audit':'30 PP für eine Informationsanzeige. Keine Änderung an Alphabetisierung, Gesetzen oder Gebäuden.',
 'iran_frontier_review':'25 PP für Informationen zu Iran-Stabilität/Bürgerkrieg/Krieg und Khuzestan. Kein Aufstand, kein Angriff, kein Anspruch entsteht dadurch.',
 'gulf_credit':'50 PP für das Auswahlmenü. Führt zu den echten Golfkrediten während des Iran-Krieges. Feste Beträge: Kuwait/Saudi-Arabien je 8%, VAE 4% des bei Anfrage eingefrorenen irakischen BIP. Kreditgeber entscheidet selbst.',
 'iran_gulf_credit':'60 PP für dieselbe Golfkredit-Auswahl. Die gesonderten direkten Golfkreditknöpfe kosten je 25 PP. Zustimmung eines echten Kreditgebers und echte Überweisung sind erforderlich.',
 'saddam_repay':'25 PP für Kreditkonten. Gewählter normaler Vertrag wird bis min(2% BIP, Restforderung, tatsächliche Schulden, verfügbare Kasse) zurückgezahlt. Golfkredite haben gesonderte vollständige Rückzahlung.',
 'industry_repay':'25 PP für dieselben Kreditkonten; keine kostenlose Tilgung. Der tatsächliche Gläubiger erhält die Zahlung.',
 'foreign_credit_review':'60 PP für dasselbe Rückzahlungsmenü. Trotz des Namens ist das keine freie Neuverhandlung oder automatische Forderungsabschreibung.',
 'war_debt_conference':'70 PP. Ruft das tatsächliche kuwaitische Erlassverfahren auf; Kuwait kann ablehnen. Ein ähnlicher direkter Golfknopf kostet 50 PP.',
 'puk_kdp_offer':'70 PP. Wenn die PUK existiert, kann das Irak-Event beide Delegationen als zustimmend wählen; zusätzliche Kosten 1% BIP. Kein echter Antwortdialog an einen separat gespielten KDP-/PUK-Staat in diesem lokalen Menü. Das ist für Mehrspieler-RP klärungsbedürftig.',
}
for key in ['constitutional_revision','civic_policy_review','foreign_policy_review','industry_reallocate','society_revision','agriculture_priority_review','oil_revenue_priority_review']:
 COMMENTS[key]='Ändert eine bereits eröffnete aktuelle Politik gegen 1% BIP je gewählter Umstellung. Erzeugt keine zweiten Fabriken oder anderen einmaligen Fokusgewinne. Die politische Menükost steht separat oben. Gegenseitig ausgeschlossene Fokusabzeichen bleiben unverändert; der aktive Politikbonus kann dennoch wechseln.'
for key in ['baath_succession','baath_continuity_cabinet','bakr_power_settlement','bakr_retire','arab_leadership','icp_leadership_vote','aziz_renewal','dawa_leadership','iip_congress','kdp_succession_vote']:
 COMMENTS[key]='Auswahl eines nach Partei, Datum und Überlebensstatus zulässigen Führers. Die Wahl im Menü installiert den Kandidaten über den vorhandenen Führungsprovider; keine gesondert simulierte Parteitagsabstimmung oder fremde Spielerzustimmung. Führergebundene Programme werden neu abgeglichen, vorhandene Fabriken nicht erneut vergeben.'
for key in ['organize_western','organize_emerging','organize_nonaligned','organize_nationalist']:
 COMMENTS[key]='55 PP. Registrierte Partei auswählen, 90 Tage Organisation abwarten. Danach +3-Punkte-Eingaben für diese Partei und ihren Outlook vor der normalen MD-Normalisierung. Endprozente sind deshalb nicht garantiert exakt +3. Kein automatischer Regierungswechsel; 180 Tage Entscheidungs-Sperrfrist.'
for key in ['icp_federal_talks','puk_federal_convention','kdp_kirkuk_talks']:
 COMMENTS[key]='Ohne aktives Nordabkommen führt dies zunächst zur Autonomie-Verhandlung. Mit aktivem Abkommen führt es zum nordirakischen Einnahmen-/Verfassungsmenü. Kein automatischer Besitzwechsel Kirkuks oder neuer Kernstaat. Bestehende KUR/PUK-Spieler müssen den zwischenstaatlichen Teil selbst akzeptieren.'
for key in ['aziz_charter','officer_amnesty_offer']:COMMENTS[key]=COMMENTS['political_opening']
for key in ['aziz_exit_front']:COMMENTS[key]='Verlässt oder erhält die bestehende Baath-ICP-Koalitionsvereinbarung. Austritt ändert die Koalitionsliste und abhängige Programme, löst aber keinen Putsch oder Bürgerkrieg aus.'
COMMENTS['icp_front_terms']=COMMENTS['front_offer'].replace('75 PP','60 PP',1)
COMMENTS['foreign_incident_review']='40 PP. Iran, Syrien, Kuwait, Jordanien, Saudi-Arabien oder Türkei wählen Zustimmung/Ablehnung für einen Vorfallkanal. Mechanisch hauptsächlich Beziehungsänderungen; keine automatische Eskalation oder Schlichtung.'
COMMENTS['iran_policy_review']='60 PP. Kann ein RP-Dossier veröffentlichen (60 Tage Verwaltungsaufwand), ein freigeschaltetes Iran-Abkommen anfragen oder Abschreckung für 1% BIP finanzieren: 90 Tage +3% Organisation, +5% Armee-Personalaufwand. Das publizierte Dossier ist keine vom Spiel überprüfte RP-Begründung.'
COMMENTS['war_emergency_review']='80 PP nach dem Frieden. Beendet ausgewählte aktive Notstandsprogramme, entfernt aber keine dauerhaften Investitionen und löscht keine bereits befristet angefallenen Personalrechnungen.'

SPECS=[
 ('bakr_soviet_offer','cooperation'),('bakr_syria_offer','syria'),('arab_development_offer','development'),('arab_support_offer','development'),('arab_union_offer','cooperation_flag'),
 ('icp_soviet_exchange','exchange'),('civic_credit_offer','loan'),('royal_jordan_offer','cooperation'),('royal_trade_offer','cooperation'),('foreign_partner_offer','cooperation'),
 ('foreign_shatt_offer','border'),('foreign_syria_offer','cooperation'),('foreign_kuwait_offer','cooperation'),('foreign_arab_conference','cooperation'),
 ('dawa_iran_offer','border'),('sciri_border_offer','border'),('sciri_aid_offer','loan'),('iip_arab_offer','cooperation'),('oil_concession_offer','concession'),
 ('oil_contract_review','oil_contract'),('industry_credit','loan'),('agri_water_offer','cooperation'),('defence_soviet_advisers','advisers'),('iran_supplier','arms'),('defence_diversified_offer','advisers_second')]
KINDS={
 'cooperation':'Nach fremder Zustimmung zahlt Irak 1% eingefrorenes BIP als Aufwand. Im Kern bessere gegenseitige Beziehungen und ein Abschlussvermerk. Kein Bündnis, keine Basis, kein Geld beim Gegenüber, keine Fabrik. Der große Vertragstitel verspricht mechanisch häufig mehr, als geliefert wird.',
 'cooperation_flag':'Irak zahlt nach fremder Zustimmung 1% BIP. Bessere Beziehungen und eine Zustimmung, die spätere Integrationsfoki freigibt. Keine tatsächliche Union oder automatische Annexion.',
 'syria':'Syrien muss zustimmen. Irak zahlt 1% BIP als Aufwand; Zustimmung wird für spätere gemeinsame Institutionen vermerkt. Kein Gebiets- oder Führungswechsel allein durch dieses Event.',
 'development':'Nach Zustimmung echte Zahlung von Irak an den Gegenstaat: 1% eingefrorenes irakisches BIP. Bessere Beziehungen; bei arabischer Entwicklung zusätzlich Zustimmung für spätere Foki. Dieses Event baut selbst keine Fabrik.',
 'exchange':'Nach sowjetischer Zustimmung zahlt Irak 1% BIP als Aufwand. 365 Tage Forschung +3%, Bürokratieaufwand +4%. Keine geschenkte Technologie.',
 'loan':'Der gewählte Kreditgeber kann zustimmen oder ablehnen. Bei Annahme überweist er 5% des bei Anfrage eingefrorenen irakischen BIP: Gläubigerkasse sinkt, Irak erhält gleich viel Kasse und tatsächliche MD-Schulden. Separate benannte Forderung; kein kostenloser Zuschuss.',
 'border':'Iran muss zustimmen; Irak zahlt 1% BIP als Aufwand. Aktiviert das bilaterale Navigationsabkommen; Iran erhält PP-Gewinn +3% und Bürokratiekosten +3%, Iraks Folgefoki lesen den gültigen Vertrag. Kein neuer Grenzverlauf, automatischer Frieden oder Staatstransfer.',
 'concession':'Großbritannien muss zustimmen; Irak zahlt den eingefrorenen 1%-BIP-Vertragsbetrag tatsächlich an Großbritannien. Prüft irakische Kontrolle und Infrastrukturkapazität für das anschließende Konzessionsprogramm. Erst ein späterer Fokus liefert dessen Gebäudegewinn.',
 'oil_contract':'Nach Zustimmung zahlt Irak 1% BIP an den Vertragspartner. Ersetzt den einen laufenden Exportvertrag für 365 Tage: Ölexporteinnahmen +3%, Steuereinnahmen −2%, Bürokratiekosten +2%. Keine Weltmarktpreisänderung und kein zusätzliches Öl.',
 'advisers':'Nach fremder Zustimmung zahlt Irak 1% BIP als Aufwand. 180 Tage Armeeorganisation +3%, Armee-Personalkosten +5%. Keine Division oder Waffenlieferung.',
 'advisers_second':'Frankreich oder Großbritannien müssen zustimmen. 1% BIP Aufwand; 180 Tage Organisation +3%, Personalaufwand +5%. Einmalig zusätzlich 25% Artillerieforschungsbonus. Derselbe Beraterspirit stapelt sich nicht einfach zu zwei Missionen.',
 'arms':'Nach Zustimmung liefert der Gegenstaat tatsächlich 1.000 infantry_weapons_1 aus seinem Bestand (gültiger 1965er Ausrüstungstyp). Irak zahlt 1% BIP als Aufwand; der Lieferstaat bekommt dafür keine Zahlung gutgeschrieben. Mindestens 1.000 Waffen müssen bei ihm vorhanden sein.'
}
for key,kind in SPECS:COMMENTS[key]=KINDS[kind]

GULF_COMMENTS={
 'forgiveness':'50 PP, einmalige Anfrage an Kuwait für 30 Tage. Nur die noch bestehende benannte Kuwait-Forderung wird bei dessen Zustimmung abgeschrieben; keine Auszahlung an Kuwait. Ablehnung öffnet die Eskalationsbegründung.',
 'oil_dispute':'50 PP. Kuwait kann ablehnen oder 90 Tage Schlichtung wählen. Beide Antworten setzen im Code die Ablehnungsmarkierung; Schlichtung verzögert nur das Ultimatum. Kein Ölpreis, Produktionswert oder Geldbetrag verändert sich.',
 'claim':'50 PP. Ansprüche auf Staaten 172 und 488 sowie +5 Punkte Kriegsunterstützung. Kein Besitz, kein Kernstaat und keine Kriegserklärung.',
 'ultimatum':'75 PP. Nach Anspruch und tatsächlicher Ablehnung, außerhalb der Schlichtungsfrist: 180 Tage Kriegsziel. Kuwait erhält keine weitere Kapitulations-Abstimmung. Der Irakspieler erklärt separat den Krieg.',
 'integration':'100 PP und 5% aktuelles BIP, obwohl die Grundkosten des Knopfes 0 PP lauten. Beide Kuwait-Staaten müssen Irak gehören und kontrolliert sein; 180 Tage durchgehend Frieden und Stabilität über 50%. Dann beide Kerne. Unterbrechung setzt die Beobachtungsfrist zurück.',
 'recovery':'50 PP und 2% aktuelles BIP bei Frieden und Gesamtschulden von höchstens 20% des aktuellen BIP. Entfernt Price of Victory; tilgt nicht die Schulden selbst.'}
for key,text in GULF_COMMENTS.items():COMMENTS['COLDWAR_IRQ_gulf_'+key]=text
for tag,rate in [('KUW',8),('SAU',8),('UAE',4)]:
 COMMENTS['COLDWAR_IRQ_gulf_request_'+tag]=f'25 PP. Einmalige Anfrage über {rate}% des bei Versand eingefrorenen Irak-BIP, 30 Tage gültig. Der Kreditgeber entscheidet und muss die volle Summe besitzen. Annahme: tatsächliche Überweisung an Irak und gleich hoher Zuwachs seiner MD-Schulden. Nur während echtem Iran-Krieg.'
 COMMENTS['COLDWAR_IRQ_gulf_repay_'+tag]='0 PP. Vollständige noch bestehende benannte Forderung auf einmal zurückzahlen; Irak braucht genügend Kasse und normale Schulden für die ganze Summe. Der echte Kreditgeber bekommt das Geld, Irak tilgt gleich viel Schuld.'
for tag in ['SAU','ENG','FRA','TUR','KUW']:
 COMMENTS['COLDWAR_USA_gulf_invite_'+tag]='Der Empfänger entscheidet: politische Kooperation mit 0,25 Mrd. Dollar echter Zahlung an USA, Kooperation ohne Zahlung oder Ablehnung. Kein automatischer Kriegseintritt, keine Fraktion und kein Stützpunktrecht.'
for tag in ['TUR','SAU','ENG','FRA']:
 for kind,cost in [('staging',2),('north',.5)]:
  COMMENTS['COLDWAR_USA_gulf_request_'+kind+'_'+tag]=f'Der Gastgeber muss Militär- und Luftbasenzugang selbst erlauben. Erste Annahme dieses Vertragstyps kostet die USA {cost} Mrd. Dollar als Aufwand; der Gastgeber erhält das Geld nicht. Erneute Erlaubnis berechnet denselben Aufwand nicht nochmals. Anfrage gilt 14 Tage; Rechte sind widerrufbar.'
US_COMMENTS={
 'revoke_access':'Der Gastgeber entzieht die tatsächlich gewährten US-Militär-/Luftbasenrechte. Bereits verdiente befristete Ausbildungsboni und ihre Personalkosten enden dadurch nicht sofort.',
 'appeal_offer':'25 PP. Politischer Aufruf für 90 Tage. Keine sofortige Armee, Gebietsübertragung oder Rebellion.',
 'rising_response':'Ein bestehender lokaler Akteur koordiniert Kontakte, wenn echte Missstände und eine irakische militärische Öffnung bestehen. Das ist nicht selbst die automatische Untergrund-Abspaltung.',
 'arms_offer':'25 PP für das Angebot; gewähltes KUR/PUK muss zustimmen. Einmalig echte 0,25 Mrd. Dollar plus 1.000 US-Infanteriewaffen. Geteilte Einmalgrenze mit dem Untergrundpaket.',
 'renew_arms':'Erneute Zustimmung eines echten lokalen Akteurs. 90 Tage ein gemeinsamer Zuschuss von 0,05 Mrd. Dollar pro Woche, täglich von USA an Empfänger gezahlt. Berater geben +8% Verteidigung gegen Irak. Kein doppelter paralleler KUR-/PUK-Vertrag.',
 'reconstruction':'Empfänger entscheidet über einmalige echte 0,5 Mrd. Dollar. Das baut noch keine Infrastruktur; lokaler Ausbau kostet danach 0,2 Mrd. Dollar je zulässigem Staat.',
 'uprising_aftermath':'Empfänger wählt, ob er nur die verbliebenen bereits zugesagten Waffen aus dem Lager annimmt. Kein zweites anfängliches Waffenpaket.',
 'underground':'25 PP plus 0,25 Mrd. Dollar und 1.000 echte US-Waffen als zugesagtes Lager. Ohne bestehende KUR/PUK wird in höchstens zwei zulässigen Nordstaaten Widerstand auf mindestens 60 gesetzt. Startet 90 Tage gemeinsamen Finanzierungsrahmen à 0,05 Mrd. Dollar pro Woche. Kann später in echte Abspaltung und Krieg münden.',
 'sustain_underground':'Verlängert die gemeinsame Finanzierung für 90 Tage: 0,05 Mrd. Dollar pro Woche, täglich belastet. Eigener Widerstandsziel-Beitrag +25 Punkte; alle 30 finanzierten Tage ein Impuls +10 bis 80, wenn kein irakisches Sicherheitsprogramm läuft.',
 'warning':'Reine Anzeige. Der tägliche Beobachter zählt die 45 passenden Warn-Tage selbst; dieser Knopf löst den Aufstand nicht aus und hält ihn nicht auf.',
 'end_support':'Beendet künftige Förderung und ihre Ziel-/Beratungsbeiträge. Ausgegebene Mittel kommen nicht zurück. Bereits zugesagte Waffen verschwinden nicht, deshalb kann die Aufstandswarnung unter ihren übrigen Bedingungen weiterlaufen.',
 'writeoff_cache':'Schreibt das noch nicht gelieferte Waffenlager endgültig ab. Kein Rückerstattungs- oder erneutes Anfangspaket.',
 'refugees':'USA: 0,5 Mrd. Dollar einmaliger Startaufwand, dann 90 Tage 0,025 Mrd. Dollar pro Woche; unter Limited War 0,020. Zugängliche zulässige Nordstaaten erhalten +25% Infrastruktur-Reparatur.',
 'protection':'USA: 90 Tage 0,05 Mrd. Dollar pro Woche für Schutzlogistik. +0,10 örtliche Versorgung nur in tatsächlich von USA/KUR/PUK kontrollierten Nordgebieten. Keine Fernsperre für irakische Truppen.',
 'patrols':'Menü zum Verlängern oder Beenden der echten befristeten Luftboni. Neue Gastgeber- und Empfängerzustimmung erforderlich. Es ist keine geografische Engine-Flugverbotszone.',
 'respond':'USA konsultieren, halten ihre Verpflichtung aufrecht oder ziehen sich zurück. Ein US-Krieg erfordert eine gesonderte Entscheidung/Erklärung.',
 'local_rebuild':'Der lokale Empfänger zahlt echte 0,2 Mrd. Dollar. Sofort ein Infrastrukturlevel in einem zulässigen eigenen/kontrollierten Nordstaat; einmal pro Staat.',
 'accord':'25 PP für das erste Angebot. Baghdad und alle beteiligten lokalen Staaten müssen akzeptieren. Anerkannte Autonomie: Irak Personalaufwand −8%, Steuereinnahmen −2%; lokale Subjekte Bau +8%, Bürokratie +3%; USA 90 Tage 0,025 Mrd. Dollar pro Woche.',
 'revise_accord':'100 PP für die Verhandlung. Bei tatsächlichem Verpflichtungswechsel zusätzlich USA 0,25 Mrd. Dollar. Neue Zustimmung für die anerkannte Autonomie nötig; kein automatischer Wechsel bei bloßem Absenden.',
 'external_policy':'25 PP für das erste Angebot. Alle zulässigen extern geschützten lokalen Staaten müssen zustimmen. USA 90 Tage 0,05 Mrd. Dollar pro Woche; lokale Verteidigung gegen Irak +5%, Personalaufwand +5%.',
 'revise_external':'100 PP für die Verhandlung, 0,25 Mrd. Dollar bei tatsächlichem Wechsel. Empfänger und Zugang müssen weiterhin gültig zustimmen.',
 'withdraw_policy':'Beendet die aktuelle US-Verpflichtung. Schon gelieferte Hilfe und vorhandene lokale Institutionen bleiben bestehen.',
 'cancel_policy_offer':'Zieht ein noch offenes Angebot zurück. Politische Verhandlungskosten werden nicht erstattet; unakzeptierte Beiträge werden nicht abgebucht.',
 'decline_protection':'Der lokale Akteur entzieht seine Zustimmung. Entfernt seine Schutzidee und beendet das US-Schutzprogramm.',
 'escalate_protection':'100 PP plus echte 0,5 Mrd. Dollar US-Aufwand. Bei Krieg Iraks gegen einen tatsächlich geschützten Akteur: einmaliges 60-Tage-Befreiungskriegsziel gegen Irak. Keine automatische US-Kriegserklärung.'}
for key,text in US_COMMENTS.items():COMMENTS['COLDWAR_USA_gulf_'+key]=text
for tag in ['KUR','PUK']:
 COMMENTS['COLDWAR_USA_gulf_assembly_offer_'+tag]='Empfänger muss zustimmen: einmaliger tatsächlicher Zuschuss von 0,25 Mrd. Dollar für eine regionale Versammlung. Kein sofortiger Regierungs-, Staats- oder Gebietswechsel.'
 COMMENTS['COLDWAR_USA_gulf_cache_offer_'+tag]=US_COMMENTS['uprising_aftermath']
for state in [164,633,630,1078]:COMMENTS['COLDWAR_USA_gulf_expand_'+str(state)]='USA zahlen 0,1 Mrd. Dollar. Erst nach 30 ununterbrochen finanzierten Tagen wird ein weiterer zulässiger Nordstaat einmalig organisiert. Abbruch kostet die Vorleistung. Halabja braucht eine bereits gebildete PUK.'
for key,cost,personnel,equipment,reduction,target in [('security',2,35,20,15,20),('major_operation',4,60,35,25,35)]:
 COMMENTS['COLDWAR_IRQ_northern_'+key]=f'Irak zahlt {cost}% aktuelles BIP. Für 90 Tage nationale Personal-/Ausrüstungsmehrkosten +{personnel}/+{equipment}%. Mindestens zwei tatsächliche Divisionen müssen 30 Tage im Norden bleiben: dann Widerstand −{reduction}, eigener Zielbeitrag −{target} für 60 Tage. Gemeinsame 90-Tage-Sperrfrist. Abzug beendet die Operation ohne Rückzahlung.'
COMMENTS['COLDWAR_IRQ_northern_withdraw_security']='Beendet außerordentliche Nord-Personal-/Ausrüstungskosten und eigene Widerstandsziel-Senkungen. Kein Geld zurück; Sperrfrist und lokale Missstände bleiben.'
COMMENTS['COLDWAR_IRQ_northern_talks']='50 PP. Bei vorhandenen KUR/PUK erhalten echte Spieler ihre Verhandlungen. Ohne eigene Staaten entscheidet das irakische Delegierten-Event. Zustimmungsart muss für eure RP-Runde klar sein.'

AUTO=[
 {'id':'auto_finance','title':'Iran-Krieg: automatische Kosten und Schuldenkrise','body':'Echter Krieg mit Iran erhöht den Personal-/Ausrüstungs-Kostenanteil zunächst um +100/+50%, ab 180 Tagen +175/+100%, ab 365 Tagen +250/+150%. Jeweils nur eine Stufe. Bei Frieden nach mindestens 180 Tagen und Netto-Neuverschuldung von mindestens 25% des Kriegsbeginn-BIP folgt The Price of Victory: Bau −30%, Steuereinnahmen −20%, Stabilität −10 Punkte, Zinsaufschlag +2 Punkte, Consumer-Goods-Faktor +20%. Es wird kein militärischer Sieg geprüft.'},
 {'id':'auto_kuwait','title':'Kuwait: automatische Folgen einer Eroberung','body':'Nach tatsächlichem irakischem Angriff: Kontrolle beider Kuwait-Staaten erlaubt einmalig min(25% positiver Kuwait-Kasse, 10% Irak-BIP) als echte Beschlagnahmung, solange Kuwait noch existiert. Rechtliches Eigentum und Kontrolle beider Staaten löschen die verbleibende kuwaitische Forderung, entfernen Price of Victory und geben 180 Tage +50% Reparaturgeschwindigkeit. Andere Schulden bleiben bestehen. Kerne brauchen eine separate Entscheidung.'},
 {'id':'auto_rising','title':'Kurdischer Aufstand: tatsächliche Abspaltung und Krieg','body':'Mindestens zwei organisierte Staaten auf mindestens 80 Widerstand, ungelöste Autonomie, verbleibendes zugesagtes Waffenlager sowie echter USA-Irak-Krieg oder jüngste irakische Kapitulation: Nach 30 passenden Tagen erscheint die öffentliche Warnung, nach weiteren 45 passenden Warn-Tagen folgen automatisch Gebietsübertragung an KUR/PUK, kleine lokale Milizaufstellung und gegebenenfalls deren Kriegserklärung an Irak. Unterbrochene Voraussetzungen pausieren die Warnung; nach 15 solchen Tagen wird sie zurückgesetzt. Nur die spätere Ausrüstungsannahme ist ein Empfängerentscheid.'},
 {'id':'auto_ledger','title':'Kreditgeber: was allgemeine MD-Tilgung mit Forderungen macht','body':'Nicht einem Gläubiger zugeordnete Senkungen der normalen irakischen MD-Schulden reduzieren benannte Forderungen in der Reihenfolge Kuwait, Saudi-Arabien, VAE, andere Schulden. Dabei bekommt der jeweilige Gläubiger keine automatische Überweisung. Die benannte Forderung ist deshalb kein vollwertig gesichertes, separat verzinstes Bankguthaben.'},
 {'id':'auto_government','title':'Regierungs- und Führungswechsel','body':'Führer- und parteigebundene Programme werden beim Wechsel neu abgeglichen und können ihre Wirkung verlieren. Einmalige nationale Entwicklung soll erhalten bleiben. Führungsmenüs treffen direkte Spielerauswahlen; interne Parteien ohne eigene Länder haben keinen separaten menschlichen Empfänger. Die normale MD-Partei-/Wahlmechanik bleibt maßgeblich.'},
 {'id':'auto_projects','title':'Fokus fertig, Belohnung noch offen: manuelle Nachholung','body':'Die ausstehenden-Projekte-Kategorie enthält 839 technische Definitionen, nicht 839 verschiedene RP-Geschichten. Sie erscheint nur für aktuell offene Gewinne, Nachträge und Statusanzeigen. Bezahl-/Vertrags-/Kontrollbedingungen müssen bei Nachholung noch gelten. Aktuelle Baugewinne werden dann sofort errichtet; es ist kein normaler Bauauftrag mit eigener Bauzeit. Das Status-Event allein baut nichts.'},
 {'id':'auto_air','title':'Northern Air Shield ist keine geografische Flugverbotszone','body':'Für 90 Tage erhalten die USA Abfangmissionen +15%, Luftüberlegenheits-Effizienz +10%, Luftpersonalaufwand +15%. Zustimmende kurdische Empfänger erhalten CAS-Schadensminderung 25%, gegnerische Luftüberlegenheitswirkung −20%, Armee-Personalaufwand +5%. Die Boni sind national, kein Skript verbietet irakischen Flugzeugen ein Gebiet. Tatsächliche Einsätze brauchen normale Flugzeuge, Basen, Reichweite und Kriegsregeln.'},
]

records=[];design=load_design();dc={d['id']:d for d in design['decisions']}
policy_nodes={n['key']:n for n in design['nodes']}
idea_names={}
for p in (ROOT/'common/ideas').glob('COLDWAR_*.txt'):
 if not any(k in p.name for k in ['COLDWAR_IRQ','COLDWAR_USA_gulf']):continue
 for key,op,body in first(first(parse(p.read_text(encoding='utf-8-sig')),'ideas',[]),'country',[]):
  if isinstance(body,list):idea_names[key]=loc(key)
def highlights(rows):
 """Direct effects only; never flatten conditional reconciliation providers."""
 result=[]
 def scan(rs,scope='Eventempfänger'):
  for key,op,value in rs:
   if key in ['trigger','limit','effect_tooltip','ai_chance','hidden_trigger']:continue
   if key=='set_country_flag':
    flag=first(value,'flag') if isinstance(value,list) else value
    if flag and flag.startswith('COLDWAR_IRQ_policy_'):
     candidate=next((n for k,n in policy_nodes.items() if flag=='COLDWAR_IRQ_policy_'+n['group']+'_'+k),None)
     if candidate:
      result.append(scope+': aktuelle Politik „'+candidate['title']+'“.')
      for mod,amount in candidate.get('modifiers',{}).items():
       name=loc('MODIFIER_'+mod.upper())
       if name.startswith('MODIFIER_'):name=mod.replace('_',' ')
       if mod=='interest_rate_multiplier_modifier':formatted=f'{amount:+g} Prozentpunkte'
       elif mod=='productivity_growth_modifier':formatted=f'{amount:+g} (nativer Zahlenwert)'
       elif mod in ['stability_factor','production_factory_max_efficiency_factor']:formatted=f'{amount*100:+g} Prozentpunkte'
       else:formatted=f'{amount*100:+g}%'
       result.append(f'{name}: {formatted} (Politikbeitrag).')
   elif key in ['add_stability','add_war_support','add_political_power','add_army_experience']:
    label={'add_stability':'Stabilität','add_war_support':'Kriegsunterstützung','add_political_power':'Politische Macht','add_army_experience':'Armee-Erfahrung'}[key]
    try:amount=float(value);formatted=f'{amount*100:+g} Punkte' if key in ['add_stability','add_war_support'] else f'{amount:+g}'
    except (ValueError,TypeError):formatted=str(value)
    result.append(f'{scope}: {label} {formatted}.')
   elif key in ['add_ideas','remove_ideas'] and isinstance(value,str):result.append(scope+': '+('aktiviert ' if key=='add_ideas' else 'entfernt ')+idea_names.get(value,loc(value))+'.')
   elif key=='add_timed_idea':result.append(scope+': '+idea_names.get(first(value,'idea'),loc(first(value,'idea')))+' für '+str(first(value,'days'))+' Tage.')
   elif key=='send_equipment':result.append(scope+': liefert '+str(first(value,'amount'))+' '+str(first(value,'equipment'))+' an '+str(first(value,'target'))+'.')
   elif key=='create_wargoal':result.append(scope+': '+str(first(value,'expire','unbefristet'))+' Tage Kriegsziel gegen '+str(first(value,'target'))+' ('+str(first(value,'type'))+').')
   elif key=='declare_war_on':result.append(scope+': tatsächliche Kriegserklärung an '+str(first(value,'target'))+'.')
   elif key=='white_peace':result.append(scope+': Weißer Frieden mit '+str(value)+' nur bei den geprüften Kriegsbedingungen.')
   elif key=='set_autonomy':result.append(scope+': Autonomiestatus von '+str(first(value,'target'))+' wird '+str(first(value,'autonomy_state'))+'.')
   elif key=='transfer_state':result.append(scope+': Staat '+str(value)+' wird übertragen.')
   elif key=='add_core_of':result.append(scope+': neuer Kernstaat für '+str(value)+'.')
   if isinstance(value,list) and key not in ['create_wargoal','declare_war_on','set_autonomy','send_equipment','add_timed_idea']:
    scan(value,key if re.fullmatch('[A-Z]{3}|[0-9]+',key) else scope)
 scan(rows)
 return list(dict.fromkeys(result))
for filename,group in [('COLDWAR_IRQ_1970_decisions.txt','d_irq'),('COLDWAR_IRQ_gulf_decisions.txt','d_gulf'),('COLDWAR_USA_gulf_decisions.txt','d_us')]:
 file='common/decisions/'+filename;text,a=read(file)
 for cat,op,body in a:
  if not isinstance(body,list):continue
  for key,_,b in body:
   if not isinstance(b,list):continue
   effects=first(b,'complete_effect',[]);called=closure(effects);joined=effects+[r for rows in called.values() for r in rows]
   short=key.removeprefix('COLDWAR_IRQ_decision_');spec=dc.get(key,{})
   records.append({'id':key,'group':group,'type':'decision','title':loc(key),'description':loc(key+'_desc'),
     'explanation':COMMENTS.get(short,''),'pp':first(b,'cost',0),'cooldown':first(b,'days_re_enable'),
     'custom_cost':loc(first(b,'custom_cost_text','')),'focuses':spec.get('audit_providers',[spec.get('unlock')]) if spec else [],
     'conditions':emit(first(b,'available',[])),'script':emit(effects),'events':eventrefs(joined),'providers':list(called),
     'source':position(file,text,key)})
for filename,group in [('COLDWAR_IRQ_1970_decisions.txt','e_irq'),('COLDWAR_IRQ_gulf_events.txt','e_gulf'),('COLDWAR_USA_gulf_events.txt','e_us'),('COLDWAR_IRQ_1970_projects.txt','e_project')]:
 file='events/'+filename;text,a=read(file)
 for b in values(a,'country_event'):
  key=first(b,'id');options=[]
  for opt in values(b,'option'):
   action=[r for r in opt if r[0] not in ['name','ai_chance','trigger']];called=closure(action)
   options.append({'title':loc(first(opt,'name')),'conditions':emit(first(opt,'trigger',[])),'highlights':highlights(action),
                   'script':emit(action),'events':eventrefs(action+[r for rows in called.values() for r in rows]),'providers':list(called)})
  trigger=first(b,'trigger',[]);recipient=first(trigger,'tag')
  if not recipient:
   recipient=next((first(first(o,'trigger',[]),'tag') for o in values(b,'option') if first(first(o,'trigger',[]),'tag')),None)
  if group=='e_gulf' and key=='COLDWAR_IRQ_gulf.21':recipient='KUW'
  if group=='e_us':
   recipient={20:'KUR / PUK',21:'KUR / PUK',22:'KUR / PUK',23:'KUR / PUK',24:'KUR / PUK',25:'KUR / PUK',30:'IRQ',31:'KUR / PUK',40:'TUR',41:'IRQ / USA',42:'USA',43:'USA',44:'USA',45:'USA',46:'USA',47:'USA',50:'SAU / ENG / FRA / TUR / KUW',52:'KUR / PUK',54:'IRQ'}.get(int(key.rsplit('.',1)[1]),recipient)
  if not recipient:recipient='IRQ' if group in ['e_irq','e_gulf','e_project'] else 'siehe Bedingungen'
  records.append({'id':key,'type':'event','group':group,'title':loc(first(b,'title')),'description':loc(first(b,'desc')),
                  'recipient':recipient,'conditions':emit(trigger),'immediate':emit(first(b,'immediate',[])),
                  'options':options,'source':position(file,text,key,True)})
for n in AUTO:records.append({**n,'group':'auto','type':'observer','description':n['body'],'options':[]})
event_ids={r['id'] for r in records if r['type']=='event'}
record_by={r['id']:r for r in records}
for r in records:
 if r['type']=='event':r['origins']=[]
for d in records:
 if d['type']!='decision':continue
 todo=list(d['events']);seen=set()
 while todo:
  eid=todo.pop()
  if eid in seen:continue
  seen.add(eid)
  if eid not in record_by:continue
  e=record_by[eid];e['origins'].append(d['id'])
  todo += [p for o in e.get('options',[]) for p in o['events']]
for r in records:
 if r['type']=='decision':
  assert all(e in event_ids for e in r['events']),('Uncaptured decision event',r['id'],r['events'])
 for o in r.get('options',[]):assert all(e in event_ids for e in o['events']),('Uncaptured followup',r['id'],o['events'])
pending_file='common/decisions/COLDWAR_IRQ_1970_pending.txt';_,pending=read(pending_file)
pending_count=sum(len(b) for k,op,b in pending if isinstance(b,list));assert pending_count==839
groups={'auto':'Automatische Abläufe','d_irq':'Irak: Politik, Wirtschaft, Iran (88)','d_gulf':'Irak: Golfkredite und Kuwait (12)','d_us':'USA, Kurden und irakische Gegenmaßnahmen (50)',
        'e_irq':'Irak-Events (129)','e_gulf':'Golf-Events (9)','e_us':'USA-/Kurden-Events (23)','e_project':'Projektstatus-Event (1)'}
used={k for r in records for k in r.get('providers',[])}|{k for r in records for o in r.get('options',[]) for k in o['providers']}
payload={'records':records,'groups':groups,'providers':{k:{'script':emit(providers[k]),'source':provider_sources[k]} for k in used},
         'hashes':hashes,'pending_count':pending_count,'scope':'Source snapshot, not a live save or engine simulation. Proposed Saddam redesign is not installed.'}
assert sum(r['type']=='decision' for r in records)==150
assert sum(r['type']=='event' for r in records)==162
assert all(r.get('explanation') for r in records if r['type']=='decision')
(HERE/'SOURCE_FRESHNESS.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
(HERE/'CATALOGUE.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
packed=base64.b64encode(gzip.compress(json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode(),9,mtime=0)).decode()
fragment=(HERE/'guide_fragment.html').read_text(encoding='utf-8').replace('<!-- GUIDE_DATA -->',f'<script type="application/octet-stream" id="cw-events-data">{packed}</script>')
assert len(fragment.encode())<1_000_000,len(fragment.encode())
DEST.write_text(fragment,encoding='utf-8',newline='\n')
print(json.dumps({'decisions':150,'events':162,'event_options':sum(len(r.get('options',[])) for r in records),'pending':pending_count,'bytes':len(fragment.encode()),'dest':str(DEST)}))
