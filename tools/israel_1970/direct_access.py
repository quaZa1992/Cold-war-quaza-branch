"""Remove political unlock chains: governing a party directly opens its policies."""
import re

OUTLOOKS=('western','emerging','nonaligned','nationalist')
REMOVED={f'ISR70_{outlook}_{stage}' for outlook in OUTLOOKS for stage in ('debate','campaign','mandate')}
REMOVED|={f'ISR70_p{slot}_mandate' for slot in range(24) if slot not in (8,9,10,11)}

DESCRIPTIONS={
 'knesset':'The Seventh Knesset brings together the parties elected in October 1969. Parliamentary committees and a working legislative agenda must give the new government a durable basis for reform.',
 'oversight':'The State Comptroller must be able to follow public money from the cabinet to local administrations. Independent audits will make officials answer for misuse of their offices.',
 'p0_cb':'Religious Zionist organizations seek a lasting place in the settlement movement. Local organization and defense preparations will shape their contribution to national policy.',
 'p18_cb':'A binational constitutional convention would require equal civic institutions and representatives prepared to negotiate a common political settlement.',
 'golda_panthers':'The development towns demand a hearing on housing, schools and access to work. The cabinet must decide how to respond to a growing protest movement.',
 'golda_succession':'Golda Meir holds the Alignment together, but Rabin and Peres offer different visions for its future. The party must settle who will lead its next cabinet.',
 'economic_plan':'Industry, agriculture and public infrastructure must keep pace with a growing population. A national economic programme will coordinate investment for the coming decade.',
 'negev_agriculture':'Water and agricultural engineering can give southern communities a more secure livelihood. New irrigated districts will bring cultivation and employment to the Negev.',
 'import_substitution':'Foreign embargoes expose the vulnerabilities of an economy dependent on imported machinery. Domestic production must be able to sustain essential industries under pressure.',
 'diaspora_bonds':'Diaspora savings can support public investment through a credible bond programme. Transparent administration and durable projects will be essential to retaining investors\' confidence.',
 'investment_scrutiny':'Publish investment contracts and subject concessions to independent audits. Public confidence requires clear terms and officials who can be held accountable.',
 'civil_electronics':'Technical workshops and civilian electronics can become a new foundation for industrial development. Skilled engineers will connect university research with practical manufacturing.',
 'armour_programme':'Israel Tal advocates a tank designed around the needs of Israeli crews and the lessons of recent wars. Domestic engineering and sustained trials will be necessary to carry that ambition forward.',
 'artillery':'Recent fighting has demonstrated the importance of responsive fire support and counter-battery work. The artillery arm needs better training and a coherent development programme.',
 'foreign_aircraft':'A reliable American supply channel allows the air force to plan its next generation of aircraft. Conversion training and maintenance arrangements must accompany procurement.',
 'local_aircraft':'Israel Aircraft Industries can reduce dependence on foreign suppliers. Domestic design teams, workshops and flight trials will require sustained government backing.',
 'us_security':'An agreement with Washington gives military planners a dependable basis for cooperation. Training and procurement offices must turn diplomatic commitments into lasting working arrangements.',
 'soviet_dialogue':'An agreed emigration framework opens a new chapter in relations with Moscow. Israel must prepare housing, employment and local services for the families who arrive.',
 'africa_contacts':'Technical missions abroad offer cooperation in agriculture, training and public works. Lasting partnerships will depend on useful expertise and reliable commitments.',
 'iran_contacts':'The relationship with the Shah\'s Iran offers opportunities in supply and commerce. A lasting arrangement will require agreement in Tehran as well as Jerusalem.',
 'keep_ambiguity':'Discretion preserves freedom of action in a hostile region. The cabinet will reaffirm a policy of strategic ambiguity and tightly controlled diplomatic communication.',
 'nuclear_transparency':'Civilian nuclear cooperation offers a different diplomatic course. Greater openness would place international research and peaceful technical exchanges at the center of policy.',
 'deep_raids':'Deep raids promise to disrupt the enemy\'s preparations beyond the front line. The cabinet must commit aircraft and trained personnel while accepting the diplomatic consequences of escalation.',
 'territorial_maximalism':'Supporters of permanent territorial control want the cabinet to commit to a lasting administrative presence. Their programme will shape relations with neighboring states and the communities under Israeli control.',
 'annexation_review':'Parliament must debate the future of the territories under Israeli control. Administrative continuity, municipal negotiations and sovereignty claims present different political commitments.',
 'intelligence':'Mossad and military intelligence need experienced analysts, secure communications and a clear division of responsibilities. Reliable assessments must inform both diplomacy and defense.',
 'gaza_services':'Civilian administration in Gaza depends on functioning local services. Work with municipal institutions to improve provision and the practical conditions of daily life.',
}

DECISIONS={
 'mapam_split':'Organize Mapam as a separate parliamentary list with its own public campaign and political leadership.',
 'reserve_exercise':'Bring reserve formations together for a scheduled training cycle and review their mobilization procedures.',
 'reserve_mobilize':'Call up additional reserves during the current war. The temporary deployment draws personnel and production away from civilian employment.',
 'negev_productivity':'Send instructors and technical advisers to southern development towns to connect vocational training with local employment.',
 'galilee_productivity':'Provide northern farming communities with agricultural advice and practical support for their next planting cycle.',
 'shelters':'Fund an additional shelter project for civilian communities in the Negev.',
 'civil_industry':'Commission a civilian industrial project in Tel Aviv. The treasury reserves its budget while construction proceeds.',
 'office_project':'Commission a municipal service center in the Negev. The treasury reserves its budget while construction proceeds.',
 'armi_project':'Commission an additional defense manufacturing facility in the Negev and reserve its construction budget.',
 'equipment_trials':'Run a series of field trials with the defense industry and army procurement offices.',
 'debt_repayment':'Use available treasury funds to retire part of the public debt. The payment is capped at the debt still outstanding.',
 'export_mission':'Send a commercial delegation abroad to establish contacts for Israeli manufacturers and exporters.',
 'talks_us':'Ask Washington to agree to military deliveries or a civilian cooperation arrangement. The American government will decide its response.',
 'talks_sov':'Ask Moscow to discuss diplomatic contacts and an agreed emigration framework.',
 'talks_egypt':'Present Egypt with a negotiated peace proposal and a framework for returning the Sinai administration.',
 'talks_pal':'Invite Palestinian representatives to discuss a municipal compact or a negotiated state settlement.',
 'roster_likud':'Propose an early unification of Herut and the Liberals in a common Likud list.',
 'later_shas':'Organize a distinct Sephardic religious list around the movement\'s community leadership.',
 'later_hadash':'Bring the communist movement and its partners together in the Hadash front.',
 'constitutional_convention':'Convene representatives to debate the Basic Law order and possible constitutional alternatives.',
}

def apply(data):
    assert REMOVED <= {n['id'] for n in data['nodes']},'Unexpected source for political access revision'
    data['nodes']=[n for n in data['nodes'] if n['id'] not in REMOVED]
    data['groups']=[g for g in data['groups'] if not g['id'].startswith('outlook_')]
    for n in data['nodes']:
        n['prerequisites']=[[p for p in row if p not in REMOVED] for row in n['prerequisites']]
        n['prerequisites']=[row for row in n['prerequisites'] if row]
        if n['group'].startswith('party_'):
            n['available']=re.sub(r'\bhas_country_flag\s*=\s*ISR70_(?:party_\d+_founded|mapam_independent)\b','',n['available']).strip()
        short=n['id'].removeprefix('ISR70_')
        if short in DESCRIPTIONS:n['description']=n['note']=n['effect_explanation']=DESCRIPTIONS[short]
        if not n['group'].startswith('party_') and n['modifiers']:
            data['idea_definitions'][short+'_idea']['treatment']=n['description']
        if short in ('unity_cabinet','narrow_cabinet'):
            n['reward']='remove_ideas = ISR70_unity\n'+n['reward']
    for d in data['decisions']:
        short=d['id'].removeprefix('ISR70_decision_')
        if d['unlock'] in REMOVED or short.startswith(('campaign_','found_','later_')) or short=='mapam_split':d['unlock']=None
        if short.startswith('campaign_'):d['note']='Organize meetings, local committees and a public campaign for this political movement.'
        elif short.startswith('found_'):d['note']='Establish an independent political organization with local branches and a public platform.'
        else:d['note']=DECISIONS[short]
    for short,label in [('unity_cabinet','National Unity Cabinet'),('narrow_cabinet','A Working Parliamentary Majority')]:
        data['idea_definitions'][short+'_idea']['label']=label
    data['removed_unlock_focuses']=sorted(REMOVED)
    data['access_revision']=3
    return data
