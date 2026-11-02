# IMPERIA COLD WAR — sovereign market opening and finite enterprise restructuring.
"""GDP-priced design records, not installed decisions or money-system code."""
import content as c

COURSES={
 'shock':dict(name='Shock Therapy',description="Prices, trade and enterprise privileges will be released in a single programme. New firms and investment can respond quickly to genuine demand, but wages, savings and public revenue will bear the disruption before a new commercial order is secure.",
   gdp_cost=.004,window=dict(name='Market Opening',days=730,modifiers=c.M(growth=1.2,civbuild=15,eff=8)),
   fiscal=dict(name='Fiscal and Social Dislocation',days=730,modifiers=c.M(tax=-25,st=-8,social=10)),
   burden=dict(name='Industrial Restructuring',modifiers=c.M(cg=18)),weekly_gdp_cost=0),
 'gradual':dict(name='Gradual Transition',description="Essential prices and public commitments will change in stages while enterprises acquire new customers and commercial accounts. The government will preserve a measure of household security, accepting slower investment and a continuing obligation to support weak producers.",
   gdp_cost=.003,window=dict(name='Orderly Market Entry',days=730,modifiers=c.M(growth=.4,civbuild=5,eff=5)),
   fiscal=dict(name='Transition Support',days=730,modifiers=c.M(tax=-8,st=4,social=6)),
   burden=dict(name='Industrial Restructuring',modifiers=c.M(cg=9)),weekly_gdp_cost=.00005),
 'directed':dict(name='Directed Reconstruction',description="The state will retain command of strategic enterprises and finance their reconstruction through a national investment plan. Public control can protect jobs and essential supply, but the treasury must carry risks that a private investor would refuse.",
   gdp_cost=.005,window=dict(name='Public Reconstruction Drive',days=730,modifiers=c.M(growth=.3,eff=8,milbuild=8)),
   fiscal=dict(name='Public Enterprise Support',days=730,modifiers=c.M(st=5,social=10,build=-4)),
   burden=dict(name='Industrial Restructuring',modifiers=c.M(cg=6)),weekly_gdp_cost=.00015),
}

SECTORS=[
 ('light_industry','Light Industry','Consumer workshops and light manufacturing employ workers whose skills may not find an immediate place in larger industrial combines.'),
 ('food_processing','Food Processing','Processing plants connect rural producers to urban consumers. Their reconstruction must preserve viable agricultural supply as well as factory machinery.'),
 ('repair_engineering','Repair and Engineering','Repair workshops keep machinery working across the economy. Their customers and staff may be worth more than the equipment listed in a hurried valuation.'),
 ('building_materials','Building Materials','Construction depends on a reliable supply of materials. New owners can improve production, but a poorly handled sale can interrupt the wider building economy.'),
 ('consumer_durables','Consumer Durables','Factories producing household goods need new designs, distribution and customers. Their workers face a demanding transition from guaranteed orders to competitive sales.'),
 ('industrial_suppliers','Industrial Suppliers','Specialised suppliers were organised around larger Union customers. Some can find new orders; others survive only through arrears and public support.'),
]

METHODS={
 'auction':dict(title='Competitive Sale',description="A public auction will invite investors to acquire the enterprise with clear obligations and published accounts. The state gains modest proceeds and new management, while accepting a smaller immediate share of the firm's income and the risk of restructuring its workforce.",
     gdp_cost=.0005,gdp_income=.0015,modifiers=c.M(eff=1,corp=-1),closure=0,days=60),
 'workers':dict(title='Worker Buyout',description="Employees and local investors will acquire the enterprise through a supervised buyout. The settlement protects workplace knowledge and social confidence, but limited capital and concessional financing leave more of the initial burden with the public budget.",
     gdp_cost=.0012,gdp_income=.0003,modifiers=c.M(eff=.5,st=1),closure=0,days=90),
 'liquidate':dict(title='Close the Combine',description="An unviable enterprise will be closed and its recoverable assets sold. The decision ends a claim on scarce public resources and clears the way for new activity, while destroying productive capacity and leaving the workforce to find a new livelihood.",
     gdp_cost=.0003,gdp_income=.0008,modifiers=c.M(admin=-1,st=-1),closure=1,days=45),
 'public':dict(title='Public Retooling',description="The enterprise will remain in public ownership while its equipment, management and accounts are reorganised. The state preserves productive capacity and employment, taking responsibility for an investment whose return depends on finding viable customers.",
     gdp_cost=.002,gdp_income=0,modifiers=c.M(eff=1.5,tax=1,admin=1),closure=0,days=120),
}

RULES={
 'prices':'Every fee, receipt and recurring allocation is a specified share of the relevant country\'s GDP. Setup shares use GDP at execution. Weekly shares use current GDP at each weekly pass. No fixed dollar price is used.',
 'window':'The first sovereign reform course starts its 730-day window once. The same country cannot restart or extend it by changing government, rejoining the Union, repeating a decision or saving and loading. The absolute deadline survives suspension. Timed benefits and fiscal burdens require actual independence.',
 'growth':'productivity_growth_modifier is a number input. At neutral scalars +1.2 produces +0.6 state productivity points per monthly pass, approximately +14.4 over 24 passes. State catch-up and other native modifiers change the actual result. It is not +120 percent annual growth.',
 'consumer_goods':'consumer_goods_factor is relative to the native corporate-tax-derived consumer-goods base. +18 percent is not eighteen percentage points of all factories. The burden is a game abstraction for industrial capacity tied up in restructuring, distinct from the fiscal loss.',
 'finite':'There are six sector lots. Each lot can be settled once by one method, and only one lot can be in progress nationally. The chosen method consumes the same lot receipt; government changes cannot reopen it. A shared 30-day interval follows completion.',
 'relief':'Each settled lot removes one sixth of this reform course\'s original restructuring burden: 3 percentage points of the modifier for shock, 1.5 for gradual, 1 for directed reconstruction. Six lots remove that spirit. Changes never lower unrelated consumer-goods requirements. Settlement modifiers belong to the national restructuring programme and persist through party changes while independent.',
 'capacity':'A competitive sale or worker buyout preserves CIVs. Liquidation removes one actual industrial_complex level in the selected owned and controlled core state and requires at least two levels there at execution. Removed capacity, GDP and tax consequences use the native economy. No factory destruction is disguised as an ownership transfer.',
 'authority':'Competitive sales and worker buyouts require the market-property charter from the chosen independent political programme. Public retooling requires its public-investment charter. Liquidation remains available under any sovereign government. The country must have an eligible surviving enterprise; no sector is a licence to remove a foreign state\'s factory.',
 'transaction':'The fee, proceeds, factory removal if any, named programme changes and lot receipt execute atomically after current sovereignty, authority, ownership and control are rechecked. Failed or cancelled execution produces no payment, proceeds or receipt. Progress restoration grants no repeated proceeds or modifiers.',
}

def revise(c):
    by={n['key']:n for n in c.NODES}
    for key,course in [('rapid_conversion','shock'),('gradual_conversion','gradual')]:
        n=by[key];r=COURSES[course]
        n.update(title=r['name'],description=r['description'],modifiers={},spirit=None,
                 gdp_cost=r['gdp_cost'],timed_ideas=[r['window'],r['fiscal']],persistent_ideas=[r['burden']],
                 market_course=course,decision='Enterprise restructuring',weekly_gdp_cost=r['weekly_gdp_cost'],
                 ownership='National reform course')
    g=next(g for g in c.GROUPS if g['id']=='transition_economy');r=COURSES['directed']
    c.F(g,'directed_reform',r['name'],r['description'],0,1,['payment_register'],gdp_cost=r['gdp_cost'],
        timed_ideas=[r['window'],r['fiscal']],persistent_ideas=[r['burden']],market_course='directed',
        decision='Enterprise restructuring',weekly_gdp_cost=r['weekly_gdp_cost'],ownership='National reform course',kind='industry')
    for key in ['rapid_conversion','gradual_conversion']:c.X('directed_reform',key)
    by['supplier_contracts']['prerequisites']=[[c.PREFIX+k for k in ['rapid_conversion','gradual_conversion','directed_reform']]]

def decisions():
    out=[]
    for sector,title,context in SECTORS:
        for method,m in METHODS.items():
            out.append(dict(id='COLDWAR_SSR_'+sector+'_'+method,sector=sector,sector_title=title,method=method,
                title=title+': '+m['title'],description=context+' '+m['description'],**{k:v for k,v in m.items() if k not in {'title','description'}}))
    return out
