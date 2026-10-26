# IMPERIA CW — Cold War: iraq 1970 concept — usa gulf.
"""COLDWAR_USA: review-only Gulf/Kurdish chapter. Never writes loaded mod files."""
from pathlib import Path
import base64
import hashlib
import io
import json
import re

from PIL import Image, ImageDraw, ImageFont
from native_font import raster, width
from kurdish_resistance import extend as extend_resistance

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OUT = ROOT / 'docs/design/iraq_1970/usa_gulf'
VIZ = Path('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82')
OUT.mkdir(parents=True, exist_ok=True)
PREFIX = 'COLDWAR_USA_gulf_'
nodes = []

def focus(key, title, xy, days, parents, gate, description, effects, *, icon='diplomatic_treaty', historic='Historical sequence; proposed gameplay', excludes=()):
    nodes.append(dict(id=PREFIX+key, title=title, narrative_title=title, group='gulf', xy=xy,
        days=days, cost=days//7, prerequisites=[[PREFIX+p for p in row] for row in parents],
        mutually_exclusive=[PREFIX+p for p in excludes], icon=icon, description=description,
        reward_summary=effects, historical_status=historic, available=gate,
        active_condition='Only while the corresponding agreement, funding and current local conditions remain valid.',
        requirement_contracts=[], modifiers={},
        effect_body='Design contract only. Native primitives and new integration requirements are listed under Mechanic limits. No runnable reward or new provider is claimed here.'))

focus('desert_storm', 'Desert Storm', (4,0), 14, [],
    'Actual Iraqi attack on Kuwait has been recorded, and Iraqi aggression/occupation is unresolved. A quick annexation of Kuwait does not erase the crisis. A complete withdrawal and restored Kuwaiti sovereignty close this opportunity.',
    'Authorize a coalition war to reverse the conquest of Kuwait. This is a direct crisis entry; coalition-building and deployment focuses are optional preparations.',
    ['Create a liberation war goal against IRQ, valid for 90 days. The USA player chooses whether to declare war.',
     'No automatic war, victory, occupation, regime change or Kurdish uprising. Recheck the unresolved crisis before delivery.',
     'Actual deployed forces incur normal MD military expenses. There is no free army or combat multiplier.'], icon='army_reform')
focus('desert_shield', 'Desert Shield', (0,0), 14, [],
    'The same unresolved Iraqi attack on Kuwait; an existing regional host must consent.',
    'Request staging rights and prepare regional logistics without delaying the direct Desert Storm option.',
    ['Offer a $2.0 billion staging/logistics package. Deduct money only after a host accepts and funds remain available.',
     'Receive only the access/basing rights accepted by that host; no automatic Saudi or Turkish participation.',
     'No free bases, divisions, equipment or automatic alliance membership.'], icon='focus_generic_supply_line')
focus('coalition', 'Coalition Mandate', (8,0), 21, [],
    'Unresolved Iraqi attack on Kuwait. Each invited government exists and controls its response.',
    'Negotiate separate commitments from Britain, France and regional governments around Kuwaiti restoration.',
    ['Unlock recipient-owned coalition invitations, cost-sharing and access agreements.',
     'Each player can accept, refuse or restrict its commitment. Financial pledges transfer actual treasury funds once.',
     'A Kuwaiti liberation mandate does not automatically authorize an invasion of Baghdad or Kurdish independence.'])
focus('appeal', 'Appeal to Iraq', (4,1), 14, [['desert_storm']],
    'An actual USA/coalition war against IRQ is underway or ended within 180 days; Iraq still has unresolved domestic opposition.',
    'Encourage Iraqi civilians and military officers to remove the ruling leadership. The appeal is a political signal, not an unconditional promise of American military support.',
    ['Unlock a one-time public appeal and opposition response events.',
     'For 90 days, an already organized Kurdish opposition may seek American assurances and coordinate a rising after an actual Iraqi military setback.',
     'No automatic stability subtraction, territorial transfer or revolt. A respected Kurdish autonomy settlement disables the grievance-based uprising offer.'], icon='government_beu')
focus('contacts', 'Kurdish Contacts', (4,2), 21, [['appeal']],
    'Unresolved northern grievances and identifiable local political actors; do not create KDP/PUK unity merely by completing this focus.',
    'Open separate channels to the Kurdish parties. Their priorities and rivalries remain distinct.',
    ['Unlock offers to existing local KDP and, if actually formed, PUK representatives.',
     'Kurdish players choose negotiation, neutrality or preparation for a rising. Refusal produces no payment or unit grant.',
     'An uprising requires local organization plus coercion/broken autonomy or a comparable real grievance, and an actual Iraqi military opening.'], icon='self_management')
focus('limited_war', 'A Limited War', (2,3), 14, [['contacts']],
    'No direct-arms commitment has been adopted for this crisis.',
    'Keep military action focused on Kuwait while retaining political contacts and a humanitarian response.',
    ['Choose the historical initial restraint: no American arms package or automatic combat support for an internal rising.',
     'Retain access to refugee relief and later protection when a real crisis develops.',
     'Avoid the insurgency subsidy and its exposure risk, while Kurdish partners may refuse assurances they consider insufficient.'],
    excludes=['arm_front'], historic='Historical initial policy; humanitarian protection followed later')
focus('arm_front', 'Arm the Front', (6,3), 21, [['contacts']],
    'No limited-war policy for this crisis; local recipients accept; a real, unresolved northern conflict exists.',
    'Make a stronger commitment than the initial 1991 policy by funding and supplying organized Kurdish forces.',
    ['Unlock one initial offer: $0.25 billion and 1,000 existing infantry_weapons_1 equipment items from the US stockpile, total for this programme rather than per party.',
     'Deliver only after acceptance, a valid recipient/supply route, sufficient actual treasury/stockpile, and current eligibility. No new equipment is spawned.',
     'A 90-day support agreement may continue for $0.05 billion per week, with explicit renewal and recipient consent. Funded advisers can grant the recipient +8% defence against IRQ for the same 90 days; this is country-targeted, not geographically restricted.',
     'Exposure creates a Turkish diplomatic response and Iraqi counteraction. Aid does not guarantee a successful rising.'], icon='army_reform',
    excludes=['limited_war'], historic='ALT: direct armed support beyond the initial US policy of 1991')
focus('northern_access', 'Northern Access', (0,4), 14, [],
    'A willing host can provide a feasible northern route. The earlier staging agreement alone does not confer Turkish rights.',
    'Negotiate the access needed for northern relief and patrols. Turkey retains its own interests and conditions.',
    ['Unlock a separate northern access agreement. Initial US logistics commitment: $0.50 billion on acceptance.',
     'Turkey can refuse, restrict military activity or request safeguards against separatist spillover.',
     'An accepted agreement grants actual air-base access as well as any agreed military access. USA receives air_base_access to the consenting host through the native diplomatic_relation effect.',
     'US aircraft still need actual basing capacity and range. No host territory or aircraft is transferred.'], icon='focus_generic_supply_line')
focus('comfort', 'Provide Comfort', (4,4), 14, [],
    'A real northern displacement/repression crisis has occurred. This independent humanitarian entry does not require the USA to have encouraged or armed the uprising.',
    'Organize multinational relief and protected return after repression and mass flight.',
    ['Unlock an initial $0.50 billion relief operation and a 90-day relief programme costing $0.025 billion per week.',
     'Recipients and access partners consent. Relief delivery supports return and recovery only in accessible affected locations.',
     'No national prosperity bonus, automatic ownership change or blanket immunity for Kurdish forces. Unfunded deliveries stop.'], icon='welfare')
focus('safe_haven', 'Northern Safe Haven', (2,5), 21, [['comfort'],['northern_access']],
    'Accessible affected northern locations; actual local/coalition protection and a funded relief operation.',
    'Protect a bounded northern refuge and enable displaced people to return. This is not a claim to all Kurdish-inhabited territory.',
    ['Unlock a 90-day protection commitment costing $0.05 billion per week beyond normal deployed-force expenses.',
     'Protection operates only where forces and access genuinely permit it. Iraqi threats trigger consultation/escalation decisions.',
     'Core candidate region for a later settlement: states 164, 633, 630 and 1078, individually checked for actual control and agreements.',
     'Kirkuk (165) is separately disputed; it is not handed over with the safe haven.'], icon='government_beu')
focus('no_fly', 'Northern Air Shield', (6,5), 21, [['comfort'],['northern_access']],
    'A northern protection crisis remains active; an existing host has accepted actual air-base access; the USA has deployed aircraft. Existing KUR/PUK recipients must accept their own support offer.',
    'Prepare American interception missions and offer Kurdish ground forces coalition air-cover coordination. The programme improves air operations and reduces the damage suffered by the protected forces.',
    ['USA receives Northern Air Readiness for 90 days: +15% interception mission efficiency, +10% air-superiority mission efficiency and +15% air-force personnel cost modifier. These affect the actual US air force country-wide.',
     'Unlock an accepted 90-day Coalition Air Cover offer for each eligible existing KUR/PUK recipient: +25% damage reduction against CAS, -20% effect of enemy air superiority on its divisions, and +5% army personnel cost modifier for liaison/coordination.',
     'Recipient modifiers affect its forces wherever they fight and against all applicable enemies. They are not a geographically enforced flight ban or an Iraq-only penalty.',
     'If no Kurdish country exists yet, the US aircraft package still works. Country-level protection can be granted after a valid local actor emerges; it is not applied to Iraqi-owned states.',
     'Manage the 90-day commitment through a normal renewal/withdrawal decision. The native military budget pays the higher air-force personnel expenses; only one readiness package is active. Renewal replaces the old package with a fresh 90-day idea and seeks renewed host/recipient consent.',
     'If the host revokes air-base access, actual basing follows normal game restrictions. The completed readiness/liaison training and its costs continue to their expiry unless USA withdraws the programme; access loss does not automatically erase these country ideas.',
     'Actual interception or air-superiority sorties use the normal air interface and actual aircraft. Combat requires the normal war/deployment conditions; peacetime aircraft are not automatically intercepted.'], icon='air_superiority')
focus('assembly', 'Regional Assembly', (2,6), 28, [['safe_haven']],
    'A viable Kurdish local administration or an accepted autonomy framework controls the participating locations; the local parties consent.',
    'Support a regional assembly, civil administration and a negotiated division of authority between Kurdish parties.',
    ['Offer $0.25 billion for local administration and elections; pay once after a valid local recipient accepts.',
     'Local decisions choose a shared administration or competing party structures. Washington does not appoint a ruler by focus.',
     'An accepted settlement can define internal self-government within Iraq; de facto administration requires actual Kurdish control.',
     'Local self-government receives actual regional administration and revenue; Baghdad loses direct collection/recruitment where it genuinely loses control. No fictional country-wide penalty is substituted for this.',
     'No automatic independence, US puppet status, Kirkuk transfer, new population or extra oil.'], icon='Election_graphics')
focus('baghdad_accord', 'Baghdad Accord', (0,7), 28, [['assembly']],
    'A local administration exists; Baghdad and the Kurdish representatives can negotiate freely.',
    'Seek recognition of Kurdish self-government within Iraq, including a practical budget and security settlement.',
    ['Unlock recipient-owned negotiations on internal government, security authority, revenue and guarantees.',
     'If accepted by both sides, a new explicitly designed IRQ-Kurdish autonomy arrangement replaces the current disputed status; no 75% factory tribute.',
     'Rejection leaves the protected de facto route available. Previously agreed and respected autonomy blocks attempts to manufacture the same grievance-based rising.',
     'Formal recognition does not replay aid or create a second autonomous country.'])
focus('self_rule', 'Guarantee Self-Rule', (4,7), 28, [['assembly'],['no_fly']],
    'Actual Kurdish self-government/control OR a mutually accepted autonomy settlement; active host access, protection funding and the Northern Air Shield programme.',
    'Commit to preserving northern self-government even if Baghdad refuses formal recognition.',
    ['Offer a renewable 90-day security commitment; maintain the existing protection agreement and one Northern Air Readiness military-cost modifier.',
     'If Baghdad refuses recognition, actual Kurdish-held territory can remain a protected de facto enclave. Iraqi legal claims are not silently erased.',
     'If a formal settlement exists, guarantee that settlement rather than creating a second status.',
     'Withdrawal, lost access or unpaid commitments end US programme benefits and expose the region to a new crisis. Guarantees do not force an automatic US war.'], icon='government_beu')
focus('recovery', 'Northern Recovery', (2,8), 28, [['baghdad_accord','self_rule']],
    'An actual recognized settlement OR viable protected de facto self-rule exists; participating Kurdish actors accept the investment contract.',
    'Help the regional administration rebuild while confronting factional competition and outside dependence.',
    ['Offer a one-time $0.50 billion reconstruction grant to the valid local administration; actual payment requires US funds and recipient acceptance.',
     'Spend the grant through costed local projects with native capacity checks; no free or duplicated factories.',
     'Persistent local infrastructure belongs to the local administration. US influence and ongoing programme benefits depend on current agreements.',
     'KDP-PUK rivalry, disputed borders and relations with Turkey remain live decisions.'], icon='crane_and_tower')

decisions = []
def decision(key, title, unlock, summary, pp=0, days=0):
    decisions.append(dict(id=PREFIX+key, label=title, unlock=PREFIX+unlock, group='gulf', pp=pp, days=days, summary=summary))
decision('appeal_offer','Broadcast the Appeal','appeal','Once per crisis: invite a local response, with no guaranteed revolt or automatic US combat promise.',25)
decision('rising_response','Coordinate a Local Rising','contacts','Recipient-owned choice. Requires real unresolved grievances, local organization and an Iraqi military setback; respected autonomy blocks this route. Local actors may negotiate, wait or rise. USA support can influence preparation, never guarantee success.')
decision('arms_offer','Offer the Initial Arms Package','arm_front','Accepted transaction only: US treasury -$0.25bn, recipient +$0.25bn; send_equipment transfers 1,000 existing infantry_weapons_1 items from the US stockpile. This is one total package, not one per party. Debit and credit once. No delivery without a valid local recipient and route.',25)
decision('renew_arms','Renew Kurdish Support','arm_front','90-day, recipient-consented contract. US -$0.05bn/week, valid recipient +$0.05bn/week; active funded advisers grant +8% defence against IRQ. Proposed idea COLDWAR_KUR_us_advisers uses native targeted_modifier = { tag = IRQ defense_bonus_against = 0.08 }. It is country-targeted, not geographically restricted. No overlapping copies; terminate when access, eligibility, recipient or funding is lost.',0,90)
decision('refugees','Fund Refugee Relief','comfort','Initial -$0.50bn relief invoice; then -$0.025bn/week for 90 days. Relief spending is not an extra cash payment to all parties. Start/renew explicitly, recheck access and treasury every tick.',0,90)
decision('patrols','Manage Coalition Air Cover','no_fly','Choose renewal of one 90-day programme or withdrawal. Renewal requires a continuing northern crisis and renewed host consent. Reset the USA package with remove_ideas then add_timed_idea for exactly 90 days. Refresh each recipient only after renewed acceptance, likewise remove then add. USA: +15% interception mission efficiency, +10% air-superiority mission efficiency, +15% air-force personnel cost modifier. Consenting KUR/PUK: +25% CAS damage reduction, -20% enemy air-superiority effect, +5% army personnel cost modifier. Recipient effects cancel when the US readiness idea ends or the recipient fights USA. Withdrawal removes the USA idea and current KUR/PUK cover ideas immediately. Host access loss restricts actual basing but does not automatically remove existing training/readiness ideas; they continue with their costs to expiry or withdrawal.',0,90)
decision('respond','Respond to a Protection Crisis','self_rule','Choices: negotiate a withdrawal of Iraqi forces, sustain/strengthen the military commitment, or end the guarantee. Escalation offers a concrete player-controlled response; no automatic war or remote territorial gift.')
decision('accord','Offer the Baghdad Settlement','baghdad_accord','Baghdad and the Kurdish representatives each accept or refuse the specified autonomy, budget and security terms. Acceptance establishes one status; de facto protection remains possible after refusal.',25)
decision('reconstruction','Fund Regional Reconstruction','recovery','Once-only accepted grant: US -$0.50bn, regional administration +$0.50bn. New locally funded projects check construction capacity and spend that grant rather than granting duplicate buildings.')

rules = {
    'scope':'Review-only USA reactive Gulf/Kurdish chapter, not an installed whole-USA tree. Integration beside the current USA programmes remains a later approved layout task. All amounts are balance proposals in MD billions of dollars.',
    'history':'Historical: February 1991 appeal; locally initiated Kurdish rising; initial US restraint; repression/refugees; Provide Comfort; protection and de facto self-government; May 1992 regional elections. Direct US arms support here is an explicit alternate intervention.',
    'entry':'Desert Storm remains a direct 14-day response to an actual unresolved Iraqi attack on Kuwait. Provide Comfort is an independent entry for a real humanitarian crisis, not a reward for encouraging rebellion. No arbitrary 1991 calendar lock or forced Bush succession.',
    'autonomy':'Default MD autonomy_autonomous_state is a strong puppet tier with 75% factory transfer. Do not reuse it for this settlement. Recognized IRQ-Kurdish internal autonomy needs a new explicit status; de facto local control can exist without Baghdad consent. Never make Kurdistan a US subject merely to label it autonomous.',
    'territory':'States 164, 633, 630 and 1078 are a proposal envelope, not an automatic transfer. Check each actual owner/controller and agreed status. Kirkuk 165 remains separately disputed. Do not release every transnational Kurdish core or remove foreign cores wholesale.',
    'air':'Northern Air Shield uses native country ideas: USA interception +15%, air-superiority mission efficiency +10%, air-force personnel cost +15%; accepted KUR/PUK CAS damage reduction +25%, enemy air-superiority effect -20%, army personnel cost +5%. Duration 90 days, renewable without stacking. These modifiers have real national scope, not a geographic flight ban. Native air-base access enables actual basing; real air combat uses normal war and mission rules. Recipient cover cancels when the US readiness idea ends or the recipient fights USA.',
    'transactions':'Offers are recipient-owned. Recheck funds, stockpiles, route, control and consent at delivery. Once-only grants use permanent transaction IDs; save/load, leader change, repeat acceptance and rejoining cannot replay them. Recurring commitments have one owner, one bill and explicit expiry/renewal; weekly rates are prorated over actual active days. Initial access and initial relief have separate invoices, never charged again by a later guarantee.',
    'counterplay':'Baghdad can honor an autonomy agreement, negotiate a new one, sustain coercive policies or challenge protection. A respected settlement removes the corresponding uprising grievance. Turkey, KDP and PUK have their own responses; no unavoidable revolt, guaranteed peace or automatic US victory.',
    'persistent':'Paid permanent construction survives US withdrawal. Logistics/underground/protection contracts depend on their live access, funding and expiry. The earned 90-day air-readiness/liaison-training ideas instead persist with their costs after host access loss until expiry or explicit withdrawal; actual basing still obeys normal access restrictions. Iraqi legal status, local control and foreign guarantees are separate facts; one focus flag does not replace them.',
}
sources = [
    dict(label='Bush appeal, 15 February 1991', url='https://www.bush41library.gov/digital-research-room/finding-aid/public-papers/remarks-raytheon-missile-systems-plant-employees'),
    dict(label='US Army CMH: Kurdish rising and Provide Comfort, pp.29-30',url='https://www.govinfo.gov/content/pkg/GOVPUB-D101-PURL-gpo5268/pdf/GOVPUB-D101-PURL-gpo5268.pdf'),
    dict(label='Bush refugee/protection statement, 16 April 1991',url='https://www.bush41library.gov/digital-research-room/finding-aid/public-papers/remarks-assistance-iraqi-refugees-and-news'),
    dict(label='UN Security Council Resolution 688: no explicit autonomy or NFZ authorization',url='https://digitallibrary.un.org/record/110659?ln=en'),
    dict(label='Kurdistan Parliament: regional elections and administration',url='https://www.parliament.krd/english/about-parliament/history-of-parliament/'),
]
resistance_campaign=extend_resistance(nodes,decisions,rules,sources,PREFIX)
air_ideas={
    'COLDWAR_USA_northern_air_readiness':dict(label='Northern Air Readiness',picture='generic_air_interception',days=90,
        modifier=dict(air_intercept_efficiency=.15,air_superiority_efficiency=.10,airforce_personnel_cost_multiplier_modifier=.15)),
    'COLDWAR_KUR_coalition_air_cover':dict(label='Coalition Air Cover',picture='generic_air_interception',days=90,
        modifier=dict(cas_damage_reduction=.25,enemy_army_bonus_air_superiority_factor=-.20,army_personnel_cost_multiplier_modifier=.05),
        cancel='OR = { NOT = { USA = { exists = yes has_idea = COLDWAR_USA_northern_air_readiness } } has_war_with = USA }'),
}
by_key={n['id'].removeprefix(PREFIX):n for n in nodes}
by_key['no_fly']['effect_body']='''# USA completion payload; idea definitions are included in the review-only specimen.
add_timed_idea = { idea = COLDWAR_USA_northern_air_readiness days = 90 }
# Separate KUR/PUK acceptance event, in that recipient's scope:
# add_timed_idea = { idea = COLDWAR_KUR_coalition_air_cover days = 90 }
# Recipient idea cancel = { OR = {
#  NOT = { USA = { exists = yes has_idea = COLDWAR_USA_northern_air_readiness } }
#  has_war_with = USA
# } }
# Native cancellation caps late recipient grants to the common sponsor's active term.
# US withdrawal payload: remove_ideas = COLDWAR_USA_northern_air_readiness
# Also remove COLDWAR_KUR_coalition_air_cover from current KUR/PUK recipients.
# Renewal: remove the previous idea, then add_timed_idea with days = 90.
# Each recipient renewal requires fresh acceptance before its own remove/add payload.
# Native support uses air_intercept_efficiency (not air_interception_efficiency).'''
by_key['northern_access']['effect_body']='''# Native effect only after the host accepts its agreement.
# Example: USA receives actual air-base access to consenting TUR.
USA = {
 diplomatic_relation = { country = TUR relation = air_base_access active = yes }
}
# A different accepted host is used in its own agreement. No automatic Turkish consent.'''
data = dict(country='USA', phase='CONCEPT ONLY - AWAITING APPROVAL', nodes=nodes,
    groups=[dict(id='gulf',label='Gulf Intervention & Kurdish Self-Rule',outlook='shared',ownership='USA crisis programme; local political outcomes require the relevant Iraqi/Kurdish participants',shape='Direct war entry; optional preparations; political fork; independent relief entry; protection and negotiated/de facto outcomes')],
    decisions=decisions, starting_spirits=[], modifier_labels={}, programme_rules=rules, sources=sources,resistance_campaign=resistance_campaign,idea_specs=air_ideas,
    preview_limits='Native inherited assets/font/grid; browser connectors and availability are illustrative. No loaded USA neighbours are represented; no engine validation.')
byid={n['id']:n for n in nodes}
assert len(byid)==len(nodes)
assert all(width(n['title'])<=143 for n in nodes), [(n['title'],width(n['title'])) for n in nodes]
assert len({tuple(n['xy']) for n in nodes})==len(nodes)
for n in nodes:
    assert n['days']%7==0
    for row in n['prerequisites']:
        for parent in row:
            assert parent in byid and byid[parent]['xy'][1]<n['xy'][1]
    for other in n['mutually_exclusive']:
        assert n['id'] in byid[other]['mutually_exclusive']
catalogue=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
(OUT/'COLDWAR_USA_GULF_CONCEPT.json').write_bytes(catalogue.encode('utf-8'))
specimen=['# COLDWAR review-only native air-shield idea definitions; NOT installed.', 'ideas = {', ' country = {']
for key,idea in air_ideas.items():
    specimen += ['  '+key+' = {','   picture = '+idea['picture']]
    if idea.get('cancel'):specimen += ['   cancel = { '+idea['cancel']+' }']
    specimen += ['   modifier = {']
    specimen += ['    '+k+' = '+str(v) for k,v in idea['modifier'].items()]
    specimen += ['   }','  }']
specimen += [' }','}']
(OUT/'COLDWAR_AIR_SHIELD_IDEAS_SPECIMEN.txt').write_text('\n'.join(specimen)+'\n',encoding='utf-8')

# Reuse the reviewed native Iraq renderer and embedded MD source assets, without
# modifying the Iraqi catalogue, renderer, loaded mod, or existing inline preview.
old=(ROOT/'docs/design/iraq_1970/PREVIEW.html').read_text(encoding='utf-8')
old_data=json.loads(re.search(r'<script type="application/json" id="irq-data">(.*?)</script>',old,re.S)[1])
assets=old_data['assets'].copy()
used={n['icon'] for n in nodes}
air_icon=ROOT/'gfx/interface/goals/00_airforce/air_superiority.dds'
assert re.search(r'name\s*=\s*"air_superiority"\s+texturefile\s*=\s*"gfx/interface/goals/00_airforce/air_superiority.dds"',(ROOT/'interface/goals.gfx').read_text(encoding='utf-8-sig'))
encoded=io.BytesIO();Image.open(air_icon).convert('RGBA').save(encoded,format='WEBP',lossless=True)
assets['icons']={**assets['icons'],'air_superiority':'data:image/webp;base64,'+base64.b64encode(encoded.getvalue()).decode('ascii')}
assets['icons']={key:value for key,value in assets['icons'].items() if key in used}
assert set(assets['icons'])==used
data['assets']=assets
fragment=(HERE/'tree_fragment.html').read_text(encoding='utf-8')
fragment=re.sub(r'<label>Programme .*?</label>','<select id="irq-branch" hidden aria-label="Programme"></select>',fragment,count=1)
fragment=re.sub(r'<label>Government view .*?</label>','<select id="irq-government" hidden aria-label="Concept"><option value="all">Concept</option></select>',fragment,count=1)
fragment=fragment.replace('IRAQ · 1 JANUARY 1970','USA · GULF CRISIS CHAPTER').replace('Iraq national focus concept','US Gulf and Kurdish self-rule focus concept')
fragment=fragment.replace('<h2>National Focus</h2>','<h2>Gulf Intervention</h2>')
fragment=fragment.replace('<button type="button" id="irq-spirits">Starting Spirits</button>','')
fragment=fragment.replace('Government &amp; Programme Rules','Mechanic limits').replace('Government and Programme Rules','Mechanic Limits &amp; Historical Scope')
fragment=fragment.replace("let current='iran_war',picked='COLDWAR_IRQ_iran_arabistan_claim'","let current='gulf',picked='COLDWAR_USA_gulf_desert_storm'")
fragment=fragment.replace("country:'Iraq1970'","country:'USA Gulf/Kurdish chapter'")
fragment=re.sub(r'function available\(n\)\{.*?\}',"function available(n){return true;}",fragment,count=1)
fragment=fragment.replace(' · 7 starting spirits',' · concept only')
fragment=fragment.replace("||'saddam'","||'all'").replace("government.value='saddam'","government.value='all'")
fragment=fragment.replace('Entire tree · Two horizontal tiers ·','Chapter overview ·').replace('The Complete Iraqi Programme','Gulf Intervention &amp; Kurdish Self-Rule')
fragment=fragment.replace('Party, leader and delivery conditions','Crisis and delivery conditions').replace('Native effect body and proposed integration','Implementation status')
fragment=fragment.replace("nodes.get(d.unlock)?.title||'Available from start'", "d.unlock_label||nodes.get(d.unlock)?.title||'Available from start'")
fragment=fragment.replace('Entry focus — no redundant party unlock','Independent crisis entry')
fragment=fragment.replace('Runs once, after current eligibility, the frozen GDP invoice and native building-capacity checks pass. Unfunded completion becomes pending. New COLDWAR_IRQ helpers and condition providers are proposed integration, not existing MD APIs.', 'These are reviewable design contracts. Money/equipment transfers and event responses have native primitives; uprising orchestration, internal autonomy and regional protection require newly authored integration. Nothing in this chapter is installed.')
fragment=fragment.replace('Native source-verified: modifier keys, money/literacy effects, construction and political refresh patterns. Proposed: historical roster extensions, leadership bridges, project/contract decisions and all numeric balance.', 'Native source-verified primitives: treasury changes, events, equipment stockpile transfers, ownership/control checks and autonomy assignment scope. Custom autonomy, uprising and patrol contracts are proposed; numeric balance and their engine behavior remain untested.')
fragment=fragment.replace('<!-- DESIGN_DATA -->','<script type="application/json" id="irq-data">'+json.dumps(data,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+'</script>')
fragment=fragment.replace('coldwar-iraq-concept','coldwar-usa-gulf-concept').replace('irq-','usg-')
fragment=fragment.replace('<style>','<style>\n#coldwar-usa-gulf-concept select[hidden]{display:none!important}',1)
fragment=fragment.replace('Starting Situation · January 1970','No new starting spirits in this reactive chapter')
fragment=fragment.replace('const list=data.decisions.filter', 'const list=data.decisions.filter')
assert len(fragment.encode('utf-8'))<1_000_000
assert 'let current=\'gulf\'' in fragment
assert 'id="usg-data"' in fragment
destination=VIZ/'usa-gulf-kurdish-concept.html'
destination.write_text(fragment,encoding='utf-8')
wrapper=old[:old.index('<div id="coldwar-iraq-concept">')]+fragment+'</main></html>'
wrapper=wrapper.replace('Iraq1970 Focus Concept','USA Gulf/Kurdish Focus Concept')
(OUT/'PREVIEW.html').write_text(wrapper,encoding='utf-8')

# Full chapter at native scale, generated from the same coordinates and labels.
def decode(uri):
    return Image.open(io.BytesIO(base64.b64decode(uri.split(',',1)[1]))).convert('RGBA')
im=Image.new('RGBA',(1030,1390),'#22343c')
draw=ImageDraw.Draw(im)
ox,oy=25,130
for n in nodes:
    x,y=n['xy'][0]*96+ox,n['xy'][1]*130+oy
    for row in n['prerequisites']:
        for parent in row:
            p=byid[parent];px,py=p['xy'][0]*96+ox,p['xy'][1]*130+oy
            y1,y2=py+90,y-26;mid=(y1+y2)//2
            draw.line([(px+80,y1),(px+80,mid),(x+80,mid),(x+80,y2)],fill='#a2b2b5',width=2)
    for other in n['mutually_exclusive']:
        if other<n['id']:continue
        q=byid[other];a=min(x,q['xy'][0]*96+ox)+139;b=max(x,q['xy'][0]*96+ox)+27
        for xx in range(a,b,9):draw.line([(xx,y+20),(min(xx+4,b),y+20)],fill='#d9a287',width=2)
for n in nodes:
    x,y=n['xy'][0]*96+ox,n['xy'][1]*130+oy
    icon=decode(assets['icons'][n['icon']]);bar=decode(assets['unavailable'])
    im.alpha_composite(icon,(int(x+87.5-icon.width/2),int(y+20-icon.height/2)))
    im.alpha_composite(bar,(x+5,y+40));im.alpha_composite(raster(n['title']),(x+15,y+58))
font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
draw.text((25,20),'USA · GULF INTERVENTION & KURDISH SELF-RULE · CONCEPT',font=font,fill='#e3cf90')
draw.text((25,48),'15 focuses · native 96 x 130 grid · relief has an independent crisis entry',font=font,fill='#c4cdcb')
im.convert('RGB').save(OUT/'FULL_CHAPTER.png')
report=dict(phase='concept only',focuses=len(nodes),decisions=len(decisions),catalogue_sha256=hashlib.sha256(catalogue.encode()).hexdigest(),max_title_width=max(width(n['title']) for n in nodes),inline_bytes=len(fragment.encode()),engine_tested=False,installed=False)
(OUT/'DESIGN_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
