# IMPERIA COLD WAR — sovereign political and economic programmes.
"""Exact-party programmes with different institutions, ownership and fiscal choices."""
import content as c
from party_profiles_v2 import PROFILES
from party_routes_core_v2 import ROUTES as CORE_ROUTES
from party_routes_central_asia_v2 import ROUTES as CENTRAL_ASIA_ROUTES
ROUTES={**CORE_ROUTES,**CENTRAL_ASIA_ROUTES}

def add(profile):
    M=c.M;R=c.R;B=c.B
    for index,p in enumerate(profile['parties']):
        data=PROFILES[profile['tag'],p['slot']];fam=p['family'];k=f'p{p["slot"]}_'
        g=c.G('party_'+str(p['slot']),p['name'],6+index*12,39,'party',p['status'])
        g['economic_identity']=data['economic_identity'];g['anti_communist']=data['anti_communist']
        p.update(economic_identity=data['economic_identity'],anti_communist=data['anti_communist'])
        def f(suffix,title,desc,x,y,parents=(),**kw):
            return c.F(g,k+suffix,title,desc,x,y,[tuple(k+v for v in parent) if not isinstance(parent,str) else k+parent for parent in parents],
                 gate='slot'+str(p['slot']),ownership='Party programme',**kw)
        def sig(i,y,parent):
            s=data['signatures'][i]
            return f('institution' if i==0 else 'development',s['title'],s['description'],0,y,[parent],
                mod=s['modifiers'],gdp_cost=s['gdp_cost'],kind=s['kind'],research=s.get('research'))

        roots={
          'communist':M(eff=4,st=3,admin=3),
          'social':M(st=3,corp=3,social=3),'national_social':M(st=3,corp=3,social=3),
          'liberal':M(research=3,civbuild=4,pp=-3),'restoration':M(pp=6,tax=3,admin=3),
          'conservative':M(agri=4,st=3,build=-2),'faith_civic':M(st=4,agri=3,admin=3),
          'authoritarian':M(pp=10,st=-4),'nationalist':M(pp=7,corp=3,st=-3),
        }
        f('root',data['root_title'],data['root_description'],0,0,mod=roots.get(fam,M(tax=3,pp=5,admin=3)),gdp_cost=.001)

        if fam=='communist':
            constitutional=[
              ('civic','Accountable Soviets','Public ownership need not mean that every official is protected from public criticism. Elected workplace and local representatives will scrutinise appointments and enterprise obligations, giving socialist institutions a broader mandate while limiting the party executive.',M(st=5,research=4,pp=-5,admin=3)),
              ('executive','Party Primacy','The party will preserve its leading position in government and coordinate the republic\'s reconstruction through a disciplined executive. Clear authority can settle industrial priorities quickly, at the expense of the criticism and outside expertise that independent institutions might provide.',M(pp=12,eff=3,research=-4)),
            ]
            econ=[
              ('public','State Investment','The state will concentrate capital in strategic enterprises, including military production, and direct their orders towards national reconstruction. Public control protects a coherent industrial policy, while leaving the treasury responsible for expensive capacity and employment commitments.',M(out=8,corp=5,cg=6),dict(public_charter=True,gdp_cost=.003)),
              ('market','Enterprise Leases','Enterprises and cooperatives will receive wider rights to lease facilities, retain earnings and seek customers. Public assets remain a national concern, but managers gain room to respond to demand without waiting for a ministry to revise its instructions.',M(eff=10,corp=-4,cg=-3),dict(market_charter=True,gdp_cost=.002)),
            ]
            follow=[
              ('production','Strategic Workshops','A strategic workshop programme will give public armaments enterprises the facilities needed to honour national orders. Its maintenance and power needs will remain a public obligation even when demand becomes less favourable.',M(energy=4),dict(building=B('arms_factory'),gdp_cost=.012,kind='army')),
              ('consumer','Cooperative Supply','Cooperatives and leased workshops will supply goods neglected by the larger public enterprises. A wider commercial economy can improve everyday supply, though collecting its revenues is more difficult than drawing payments from a few large combines.',M(eff=6,agri=6,tax=-3),dict(gdp_cost=.002,kind='industry')),
            ]
            fiscal=[
              ('universal','Universal Subsidies','Broad subsidies will protect households and sustain demand during reconstruction. Their political value is considerable, but a universal promise obliges the government to support consumers who could afford to pay more.',M(st=6,social=12,cg=3)),
              ('targeted','Targeted Provision','Support will be concentrated on households and services most exposed to hardship. A narrower commitment can improve public finances, while requiring a larger administrative effort and accepting less universal protection.',M(tax=5,social=-5,admin=6,st=2)),
            ]
            end_title='Republican Socialism'
            end_desc='A sovereign socialist republic must be judged by the work, services and institutions it can sustain. Public responsibility will remain central to national development, with economic decisions now answerable to the republic rather than a distant Union plan.'
            end_mod=M(eff=3,tax=3)
        elif fam in {'social','national_social'}:
            constitutional=[
              ('civic','A Labour Assembly','Trade unions, professional associations and elected representatives will review the cabinet\'s programme. A broader labour mandate can protect reconstruction from a narrow party machine, while making national decisions slower and more difficult to settle.',M(st=5,research=3,pp=-4,admin=3)),
              ('executive','The Social Cabinet','A disciplined social cabinet will coordinate enterprise reconstruction and essential services. Concentrated responsibility promises quicker action, while workers and rival parties must accept that many decisions will be taken by officials and technical managers.',M(pp=9,eff=4,st=-3)),
            ]
            econ=[
              ('public','Producer Cooperatives','Workers and agricultural producers will organise capital, machinery and marketing through cooperatives. Participation can preserve practical knowledge and local confidence, while dispersed ownership makes large investment programmes harder to coordinate.',M(eff=10,agri=6,build=-4),dict(market_charter=True,public_charter=True,gdp_cost=.003)),
              ('market','Development Trusts','Public development trusts will finance enterprises and infrastructure that private investors are unwilling to carry alone. The approach offers a coherent investment programme, with the treasury accepting the losses if those projects fail.',M(build=10,eff=6,social=5),dict(public_charter=True,gdp_cost=.004)),
            ]
            follow=[
              ('production','Cooperative Credit','Credit unions will supply small producers with working capital and access to equipment. Better finance can strengthen rural and industrial livelihoods, provided the public authorities accept modest revenues rather than demanding immediate returns from every borrower.',M(agri=6,eff=3,tax=-3),dict(gdp_cost=.002,kind='agriculture')),
              ('consumer','Public Works','A national works programme will give reconstruction a visible purpose in transport and local industry. Employment and commercial links improve together, while the state must maintain the facilities after the construction crews depart.',M(st=2,admin=2),dict(building=B('infrastructure'),gdp_cost=.009,kind='industry')),
            ]
            fiscal=[
              ('universal','Progressive Revenue','Profitable firms will carry a larger share of the public settlement. Higher receipts can protect services and relieve households, but additional claims on business resources slow the investment needed to renew production.',M(corp=9,cg=5,civbuild=-4)),
              ('targeted','A Broader Tax Base','The government will bring smaller enterprises and new commercial activity into dependable public accounts. A broader base avoids relying entirely on a few large firms, at the price of stronger enforcement and a more expensive revenue service.',M(tax=6,admin=6,st=-2)),
            ]
            end_title='A Social Republic'
            end_desc='National independence must include institutions through which workers and communities can defend their livelihoods. A lasting social settlement will connect productive enterprise, organised labour and public services without treating every disagreement as a threat to the state.'
            end_mod=M(eff=3,st=2)
        elif fam=='conservative':
            constitutional=[
              ('civic','Local Representation','Local councils and established community institutions will share responsibility for the national settlement. Their participation can give government deeper roots, while leaving the cabinet to negotiate with interests it cannot simply instruct.',M(st=5,agri=3,pp=-4,admin=3)),
              ('executive','National Stewardship','A stronger national executive will defend public order and coordinate reconstruction through experienced officials. Its supporters expect decisive government, even where that authority restricts the influence of local institutions and public critics.',M(pp=10,admin=-4,research=-3)),
            ]
            econ=[
              ('public','Family Property','Secure family property and inheritance will give farmers and smaller businesses a firmer basis for investment. The republic will favour independent producers over another concentration of economic power in large industrial organisations.',M(agri=12,corp=4,civbuild=-3),dict(market_charter=True,gdp_cost=.002)),
              ('market','Mutual Credit','Community banks and mutual credit societies will connect local savings with productive work. Broader access to finance can support both farms and workshops, while concessions to smaller borrowers reduce immediate public revenue.',M(agri=8,eff=6,tax=-4,admin=3),dict(public_charter=True,market_charter=True,gdp_cost=.003)),
            ]
            follow=[
              ('production','Farm Mechanisation','Independent producers need machinery and technical instruction if legal ownership is to yield better harvests. A national mechanisation programme will bring engineering services closer to farms without placing their daily work under a single industrial manager.',M(agri=5,energy=3),dict(research=R('CAT_industry'),gdp_cost=.002,kind='agriculture')),
              ('consumer','Rural Roads','Local transport can matter more to a small producer than another formal promise of credit. Better roads will connect farms and workshops to customers, provided the state accepts a long-term maintenance responsibility.',M(admin=2),dict(building=B('infrastructure'),gdp_cost=.009,kind='industry')),
            ]
            fiscal=[
              ('universal','Land and Business Tax','Property and commercial income will support the institutions that protect national life. More dependable revenue strengthens government, while farmers and local businesses resist a burden they believe distant industrial interests can more easily evade.',M(tax=6,corp=4,st=-3)),
              ('targeted','Smallholder Relief','Smaller farms and family firms will receive relief while the new economy settles. More resources remain in local production, but the treasury must meet public obligations from a narrower immediate base.',M(agri=8,cg=-3,tax=-5)),
            ]
            end_title='A Settled Republic'
            end_desc='The republic will rest on institutions that families, producers and local communities can recognise as their own. National authority must preserve that confidence while finding the revenue and commercial capacity needed to sustain an independent state.'
            end_mod=M(agri=3,corp=3)
        elif fam=='faith_civic':
            constitutional=[
              ('civic','Community Schools','Community schools will connect religious education with literacy and practical instruction. Their local support can extend education beyond the reach of state institutions, although the government must negotiate standards with authorities it does not directly appoint.',M(st=5,research=2,admin=4)),
              ('executive','National Curriculum','A common national curriculum will protect technical education and a shared public qualification. Its scientific advantages come with political tension where local educators regard uniform supervision as another attempt to displace their authority.',M(research=6,social=4,st=-3)),
            ]
            econ=[
              ('public','Community Endowments','Endowments and cooperative funds will support farms, workshops and local services. A community-based economy can broaden participation, while making public revenue and national investment priorities more difficult to coordinate.',M(agri=10,eff=5,tax=-3,admin=3),dict(public_charter=True,market_charter=True,gdp_cost=.003)),
              ('market','Enterprise Charters','Independent firms will receive clear commercial rights and a national framework for contracts. New investment can answer demands that local funds cannot meet, while exposing established communities to unfamiliar employers and changing social relations.',M(civbuild=12,tax=4,st=-4),dict(market_charter=True,gdp_cost=.002)),
            ]
            follow=[
              ('production','Village Workshops','Local repair and processing workshops will connect agricultural livelihoods with technical services. Their modest scale can preserve community control, although it cannot supply every machine or investment required by a modern economy.',M(agri=6,eff=3,build=-2),dict(gdp_cost=.002,kind='agriculture')),
              ('consumer','Technical Colleges','Technical colleges will prepare graduates for industry and national administration. The investment broadens professional opportunity, while requiring the state to carry institutions whose return will arrive more slowly than a commercial sale.',M(research=3,social=4),dict(research=R('CAT_industry'),gdp_cost=.002,kind='research')),
            ]
            fiscal=[
              ('universal','A Social Guarantee','A public guarantee of essential care will join community obligations to the authority of the state. It offers protection during economic upheaval, at a substantial and continuing cost to the social budget.',M(st=6,social=10)),
              ('targeted','Local Responsibility','Local funds and voluntary institutions will take a larger part in social provision. Lower central expenditure leaves greater resources for investment, while the quality of care depends more heavily on the wealth and organisation of each community.',M(social=-6,civbuild=6,st=-3,admin=3)),
            ]
            end_title='The Civic Compact'
            end_desc='A sovereign public life can make room for religious communities without abandoning national law and technical education. Its durability will depend on whether government can balance local authority, commercial change and the rights of citizens who expect the state to speak for them all.'
            end_mod=M(agri=3,tax=3)
        else:
            hard=fam in {'authoritarian','nationalist'}
            if data['anti_communist']:
                constitutional=[
                  ('civic','Lustration','Party appointments and political police networks gave the old order an influence that survived the change of flag. Opening public offices to scrutiny will break those protections, while removing experienced personnel and deepening the bitterness of the transition.',M(pp=12,tax=5,admin=8,research=-4,st=-3)),
                  ('executive','Retain Technical Staff','The republic cannot rebuild every ministry and workshop from nothing. Experienced officials and engineers will remain in service under new authority, preserving expertise at the price of continued suspicion towards people whose careers were made under Soviet rule.',M(research=5,eff=4,pp=-5,corp=-3)),
                ]
            else:
                constitutional=[
                  ('civic','Independent Courts','Public authority must answer to law rather than another circle of personal appointments. Independent courts will protect commercial and civil rights, requiring the executive to accept scrutiny and finance institutions beyond its direct political control.',M(tax=5,research=3,admin=5,pp=-3)),
                  ('executive','Professional Service','Experienced civil servants will carry administrative responsibility while elected leaders settle the national programme. A professional service can bring order to government, but it gives less influence to outsiders impatient for a complete political break.',M(pp=8,admin=-6,research=-3)),
                ]
            if hard:
                econ=[
                  ('public','National Corporations','Strategic firms will be coordinated through national corporations answerable to the executive. Concentrated capital can pursue large orders, while carrying the energy requirements and political protections associated with major industrial interests.',M(out=8,eff=5,energy=7,admin=3),dict(public_charter=True,gdp_cost=.004)),
                  ('market','National Enterprise','Domestic entrepreneurs will be encouraged to rebuild production under the protection of the new state. A wider commercial base can respond more quickly to demand, although independent employers complicate the government\'s claim to direct national development.',M(eff=10,corp=4,cg=-3,st=-3),dict(market_charter=True,gdp_cost=.003)),
                ]
                follow=[
                  ('production','Strategic Industry','A strategic industrial programme will give the republic more capacity to supply its own economy. The new combine will carry demanding obligations to national customers alongside its continuing need for power and maintenance.',M(energy=3),dict(building=B('industrial_complex'),gdp_cost=.015,kind='industry')),
                  ('consumer','Industrial Credit','Credit will support domestic firms able to replace old contracts with viable production. Public support can accelerate that change, while leaving the treasury exposed when politically favoured borrowers fail to repay.',M(civbuild=10,corp=-3),dict(research=R('CAT_industry'),gdp_cost=.002,kind='industry')),
                ]
            else:
                econ=[
                  ('public','Domestic Capital','National savings and domestic investors will receive priority in enterprise reconstruction. A stronger local tax base and commercial class come at the price of slower access to the larger pools of capital and machinery available abroad.',M(eff=6,corp=6,civbuild=-4),dict(market_charter=True,public_charter=True,gdp_cost=.003)),
                  ('market','Open Investment','The republic will offer secure commercial rights and favourable conditions to new investors. Machinery, capital and expertise can arrive more quickly, while tax concessions and outside commercial interests narrow the government\'s immediate return.',M(civbuild=15,eff=8,corp=-6),dict(market_charter=True,gdp_cost=.002)),
                ]
                follow=[
                  ('production','Local Industrial Funds','National credit institutions will direct savings towards workshops and viable manufacturing. A broader domestic economy can emerge from those investments, though the public authorities must finance patient lending and absorb the risk of failure.',M(admin=3),dict(building=B('industrial_complex'),gdp_cost=.015,kind='industry')),
                  ('consumer','Technical Exchange','Commercial partnerships will bring new production methods and machinery standards into national industry. Technical education is essential if the republic is to retain more than the simplest work in the new division of labour.',M(research=3,social=3),dict(research=R('CAT_industry',50,2),gdp_cost=.002,kind='research')),
                ]
            fiscal=[
              ('universal','Low Business Levies','A lighter burden on commercial activity will leave more resources with new firms and encourage further investment. The state must accept lower immediate receipts and resist using every growing enterprise to repair the public budget.',M(corp=-6,civbuild=10,cg=-4)),
              ('targeted','Revenue Before Growth','Profitable enterprises will contribute more firmly to national reconstruction. The additional revenue gives the government greater room to act, while the claim on business resources reduces the pace at which firms can expand.',M(corp=9,cg=5,civbuild=-4)),
            ]
            end_title='National Consolidation' if hard else 'A Free Republic'
            end_desc='Independence will endure only if national institutions can sustain authority, productive work and a public life beyond the struggle that brought them to power. The government must turn its political claim into an economic and constitutional settlement that ordinary citizens can recognise.'
            end_mod=M(eff=3,pp=3)

        override=ROUTES.get((profile['tag'],p['slot']),{})
        constitutional=override.get('constitutional',constitutional)
        econ=override.get('econ',econ);follow=override.get('follow',follow);fiscal=override.get('fiscal',fiscal)
        for suffix,title,desc,mods in constitutional:f(suffix,title,desc,-3 if suffix=='civic' else 3,1,['root'],mod=mods,gdp_cost=.001)
        c.X(k+'civic',k+'executive')
        sig(0,2,['civic','executive'])
        if data['anti_communist']:
            f('archives','Open Party Archives','The party-state kept records of appointments, surveillance and the privileges through which public authority was exercised. Opening those files will expose the networks that survived independence and strengthen demands for a new political settlement, while placing a difficult responsibility on national institutions.',-4,2,[['civic','executive']],mod=M(pp=6,research=3,admin=5),gdp_cost=.001,
              party_transfer=dict(from_slot=4,to_slot=p['slot'],fraction=.15))
        for i,(suffix,title,desc,mods,extra) in enumerate(econ):f(suffix,title,desc,-3 if i==0 else 3,3,['institution'],mod=mods,kind='industry',**extra)
        c.X(k+'public',k+'market')
        for i,(suffix,title,desc,mods,extra) in enumerate(follow):f(suffix,title,desc,-3 if i==0 else 3,4,['public' if i==0 else 'market'],mod=mods,**extra)
        sig(1,5,['production','consumer'])
        for i,(suffix,title,desc,mods) in enumerate(fiscal):f(suffix,title,desc,-3 if i==0 else 3,6,['development'],mod=mods,gdp_cost=.001)
        c.X(k+'universal',k+'targeted')
        if fam not in {'conservative','faith_civic'}:
            f('enterprise_service','Enterprise Services','Reliable accounts, advice and technical services will help enterprises carry the government\'s economic settlement into daily practice. Their benefits extend beyond a few favoured firms, while imposing a continuing demand for qualified staff and public supervision.',-3,7,['universal'],mod=M(eff=3,admin=3),gdp_cost=.0015)
            f('revenue_courts','Revenue Appeals','Tax disputes need a dependable procedure rather than competing political instructions. A specialised appeals service will protect enforceable public claims while requiring officials to justify their decisions before the law.',3,7,['targeted'],mod=M(tax=3,pp=-3),gdp_cost=.0015)
            parents=[['enterprise_service','revenue_courts']];end_y=8
        else:parents=[['universal','targeted']];end_y=7
        f('settlement',end_title,end_desc,0,end_y,parents,mod=end_mod,gdp_cost=.001)
        if fam=='unionist':
            f('romanian','Romanian Convention','Language, family ties and a shared cultural inheritance have survived the frontier. A cultural convention with Bucharest can reconnect schools and public institutions, while leaving the two governments to confront the larger questions raised by that renewed relationship.',0,end_y+1,['settlement'],action='offer:romanian',kind='diplomacy')
        if fam in {'authoritarian','nationalist'}:
            f('civilian','Civilian Settlement','Veteran organisations and political cadres must find a place within national law. Giving civilian institutions the final authority will broaden consent and attract independent expertise, while requiring the movement to share a power it once claimed exclusively.',-3,end_y+1,['settlement'],mod=M(st=5,research=3,pp=-5),gdp_cost=.0015)
            f('cadres','National Directorate','A permanent national directorate will bind military and administrative leadership to the governing movement. It promises discipline and coordinated authority, while deepening the dependence of the state on a narrow and costly political establishment.',3,end_y+1,['settlement'],mod=M(pp=12,org=5,admin=6,st=-4),gdp_cost=.002)
            c.X(k+'civilian',k+'cadres')
