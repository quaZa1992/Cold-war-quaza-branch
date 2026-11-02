# IMPERIA COLD WAR — country-specific sovereign party route cores.
"""Distinct constitutional and economic routes for selected non-communist parties."""

import content as c


def _route(constitutional, econ, follow, fiscal=None):
    data = dict(constitutional=constitutional, econ=econ, follow=follow)
    if fiscal is not None:
        data['fiscal'] = fiscal
    return data


def _e(public_title, public_desc, public_mod, public_cost,
       market_title, market_desc, market_mod, market_cost):
    return [
        ('public', public_title, public_desc, public_mod,
         dict(gdp_cost=public_cost, public_charter=True, market_charter=False)),
        ('market', market_title, market_desc, market_mod,
         dict(gdp_cost=market_cost, public_charter=False, market_charter=True)),
    ]


def _f(production_title, production_desc, production_mod, production_cost, production_kind,
       consumer_title, consumer_desc, consumer_mod, consumer_cost, consumer_kind,
       production_extra=None, consumer_extra=None):
    a = dict(gdp_cost=production_cost, kind=production_kind)
    b = dict(gdp_cost=consumer_cost, kind=consumer_kind)
    if production_extra:
        a.update(production_extra)
    if consumer_extra:
        b.update(consumer_extra)
    return [
        ('production', production_title, production_desc, production_mod, a),
        ('consumer', consumer_title, consumer_desc, consumer_mod, b),
    ]


ROUTES = {
    # Ukraine
    ('UKR', 0): _route(
        [
            ('civic', 'Civilian Council', "The Liberation Council opens cabinet deliberations to elected municipal delegates, teachers, and former political prisoners. Public participation broadens its authority beyond wartime networks, while veteran commanders give up the exclusive voice they held in exile.", c.M(st=5, research=3, pp=-4)),
            ('executive', 'Council Secretariat', "A disciplined secretariat coordinates the council's diaspora offices and the new republic's ministries. It can move quickly through a divided administration, but underground habits and concentrated appointments make civilian oversight harder to establish.", c.M(pp=9, admin=-3, st=-3)),
        ],
        _e('Village Cooperatives', "Farm cooperatives share machinery, credit, and storage while protecting smallholders from sudden land sales. The model builds rural loyalty and food capacity, but capital-intensive industry grows more slowly than under a concentrated state investment plan.", c.M(agri=10, st=3, build=-3), .0012,
           'Diaspora Industry Fund', "Ukrainian exile donors finance machine shops, power repairs, and technical schools through a public fund. Investment arrives with skills and overseas contacts, but contributors gain influence over priorities that local voters may rank differently.", c.M(eff=6, civbuild=4, corp=-3), .0015),
        _f('Farm Machinery Service', "Repair depots and cooperative credit extend tractors, seed, and storage to small farms. Harvest losses fall, although public support must continue where landholdings are too small to repay equipment loans quickly.", c.M(agri=6, eff=3, energy=2), .0009, 'agriculture',
           'Prolog Press House', "Diaspora publishers and local editors restore Ukrainian books, technical journals, and school texts. Cultural work strengthens public life and technical learning, but printing and distribution compete with urgent factory investment.", c.M(research=5, st=3, social=2), .0007, 'society', None, {'research': c.R('CAT_electronics', 25)})),
    ('UKR', 1): _route(
        [
            ('civic', 'National Council', "The State Centre's National Council seats exile parties, regional representatives, and citizens who remained in Ukraine. A broad parliament can make legal continuity credible at home, but coalition bargaining slows decisions over land, language, and the former state economy.", c.M(st=5, pp=-4, research=3)),
            ('executive', 'Presidential Mandate', "A responsible executive draws on the UPR's constitutional inheritance to settle urgent questions of citizenship and public order. Concentrated authority speeds reconstruction, while the National Council must work harder to keep political rivals inside the legal settlement.", c.M(pp=9, admin=-3, st=-2)),
        ],
        _e('Land Claims Tribunal', "A tribunal hears former owners, tenants, and families who cultivate land today before deciding restitution or compensation. Clear titles can unlock farm credit and investment, but hearings delay transactions and can divide villages over competing claims.", c.M(tax=4, pp=3, build=-3), .0010,
           'Smallholder Credit', "A parliamentary bank directs savings to small farms, food processors, and local workshops rather than returning every asset to its former owner. New producers gain capital, while slow public lending limits the first wave of expansion.", c.M(agri=6, eff=5, tax=-2), .0012),
        _f('Farm Title Registry', "A public registry records land claims and tenancy rights before credit and investment expand. Farmers gain legal certainty, but unresolved restitution cases continue to tie up property and staff.", c.M(agri=5, tax=3, admin=2), .0006, 'agriculture',
           'Parliamentary Works', "The National Council finances rail, housing, and power repairs through a public works bank with published accounts. Reconstruction reaches several regions, but repayment obligations limit later spending on schools and services.", c.M(build=5, eff=3, tax=-2), .0010, 'industry', None, {'building': c.B('infrastructure')})),
    ('UKR', 2): _route(
        [
            ('civic', 'Rights Charter', "The Sixtiers' rights advocates turn constitutional guarantees into enforceable protections for speech, language, and fair trials. Independent courts gain authority, while the young civic coalition must accept that legal review can delay policies popular with its own supporters.", c.M(research=5, st=4, pp=-4)),
            ('executive', 'Civic Cabinet', "A cabinet of educators, lawyers, and local administrators coordinates the first republic-wide reforms. Skilled officials can restore public services quickly, but a narrow circle of intellectuals risks speaking over workers and rural communities.", c.M(admin=-5, pp=7, st=-3)),
        ],
        _e('University Co-ops', "University and student cooperatives retain public campuses while selling research, translation, and technical services to Ukrainian firms. Knowledge reaches new customers, but commercial work can draw staff away from public teaching and basic science.", c.M(research=6, eff=4, corp=-2), .0009,
           'Local Workshop Charter', "Cities license independent repair shops and small manufacturers with open access to credit and contracts. Employment spreads beyond large combines, while fragmented supply and uneven standards limit productivity in major industrial plants.", c.M(eff=7, tax=4, admin=3), .0008),
        _f('Engineering Press', "Independent technical journals and university laboratories share new methods with factories. Research reaches the productive economy, though results take time and do not immediately restore household supply.", c.M(research=5, eff=3, pp=-2), .0007, 'research',
           'Municipal Repair Shops', "Municipal contracts support repair, furniture, and household-equipment shops in industrial cities. Everyday goods return sooner, but local firms compete for skilled workers and investment with larger state plants.", c.M(eff=6, st=3, build=-2), .0007, 'industry', {'research': c.R('CAT_electronics', 25)})),
    ('UKR', 3): _route(
        [
            ('civic', 'Labour Assembly', "The URDP convenes unions, farm associations, and parliamentary parties to write the social settlement. Workers and smallholders gain a durable voice, while coalition negotiations make national production and wage agreements harder to conclude quickly.", c.M(st=5, pp=-4, eff=3)),
            ('executive', 'Social Cabinet', "A social cabinet coordinates reconstruction with elected labour and farmer representatives. It can protect employment and public services during conversion, but concentrating decisions among party officials weakens local bargaining.", c.M(pp=8, social=4, st=-3)),
        ],
        _e('Worker-Farmer Coops', "Worker and farmer cooperatives own shares in processing, tools, and local distribution. Participation protects livelihoods and spreads income, but shared control makes large investment decisions slower and more difficult to finance.", c.M(eff=8, agri=7, build=-4), .0010,
           'Social Market Firms', "Independent firms gain access to credit and contracts under labour law and public competition rules. New capital can modernize production faster, while weaker firms and workers face the pressure of market selection.", c.M(eff=7, corp=4, st=-3), .0011),
        _f('Union Credit League', "Labour and farm credit leagues finance machinery and working capital for member-owned enterprises. Local employment rises, though public revenues grow more slowly than under large private employers.", c.M(agri=6, eff=4, tax=-3), .0008, 'industry',
           'Clinics and Housing', "Parliament directs funds to clinics, housing repairs, and municipal services during industrial conversion. Families receive practical protection, while the treasury delays more ambitious factory modernization.", c.M(st=4, social=5, build=-3), .0010, 'society', None, {'building': c.B('infrastructure')})),
    ('UKR', 20): _route(
        [
            ('civic', 'Coalition Council', "OUN-M shares government with the UPR Council, civic associations, and local cooperatives. The arrangement trades direct movement control for a broader national mandate and a visible break with the exclusive authority claimed by OUN-B.", c.M(st=5, pp=-4, research=3)),
            ('executive', 'Christian Directorate', "A Christian-national directorate gives experienced exile cadres responsibility for appointments and public service. It can coordinate reconstruction around a common social ethic, but excludes rivals from decisions and risks turning solidarity into party patronage.", c.M(pp=8, st=-3, admin=3)),
        ],
        _e('Parish Credit Unions', "Parish and village credit unions lend to family farms, dairies, and workshops under published rules. Small producers preserve their independence and gain machinery, while a dispersed cooperative network cannot match the scale of centralized industrial credit.", c.M(agri=8, eff=4, tax=-3), .0009,
           'Guild Contracts', "Independent industrial guilds bid for public orders in machinery, food processing, and transport repair. Skilled Ukrainian firms gain work and investment, while established guilds can restrict new competitors and raise contract prices.", c.M(eff=6, civbuild=3, build=-3), .0010),
        _f('Cooperative Storage', "Shared granaries, dairies, and repair depots help village producers reach markets without selling their land. Rural incomes improve, though cooperative managers need training and public audits to prevent local favoritism.", c.M(agri=6, eff=4, st=2), .0008, 'agriculture',
           'Guild Apprenticeships', "Industrial guilds train apprentices in machine repair, metalwork, and quality control. Skilled employment rises in Ukrainian firms, but training costs arrive before every workshop can secure long-term orders.", c.M(eff=5, research=3, build=2), .0007, 'industry', None, {'research': c.R('CAT_industry', 25)})),
    ('UKR', 21): _route(
        [
            ('civic', 'National Assembly', "A constituent assembly gives parties, churches, unions, and regional delegates a lawful way to contest the Bandera movement's claim to rule. Consent and outside expertise broaden legitimacy, while the revolutionary cadre yields part of its command.", c.M(st=5, research=4, pp=-6)),
            ('executive', 'Revolutionary Command', "A single national command binds the movement's cadres to ministries, security, and production offices. It can issue decisions quickly, but surveillance, political exclusion, and costly loyal appointments make the state feared as well as obeyed.", c.M(pp=12, admin=5, st=-6)),
        ],
        _e('National Syndicates', "The state organizes employers and workers into syndicates that prioritize rifles, vehicles, ammunition, and communications equipment for the armed forces. Coordinated capital restores military supply, but independent unions and small competitors lose influence over wages, contracts, and investment.", c.M(out=9, energy=5, st=-5), .0011,
           'Protected Workshops', "Private workshops receive secure state contracts for tools, clothing, and repair parts. Consumer supply responds quickly, while political protection and favored suppliers weaken competition and raise public procurement costs.", c.M(eff=6, corp=4, st=-4), .0010),
        _f('Cadre Machine Combine', "A state combine concentrates weapons, military vehicles, and metalworking around army procurement. Arms output and efficiency rise, but appointments and energy allocations remain tied to political loyalty and a large administrative apparatus.", c.M(out=6, cap=4, energy=4), .0015, 'industry',
           'National Service Shops', "State-backed shops provide household goods and repairs in cities neglected by strategic plants. Everyday supply improves, though public contracts reinforce the same cadre networks that control heavy industry.", c.M(eff=6, st=2, admin=3), .0009, 'industry', {'building': c.B('industrial_complex')})),

    # Belarus
    ('BLR', 1): _route(
        [
            ('civic', 'Rada of the Republic', "The BNR Rada invites elected local representatives to join an exile government whose legal claim survived abroad. Broad participation can reconnect constitutional continuity to people at home, but compromises dilute the authority once exercised by the Rada's leaders.", c.M(st=5, pp=-4, research=3)),
            ('executive', 'Continuity Cabinet', "A continuity cabinet draws on the Rada's diplomatic and legal institutions to restore state administration. Experienced exile officials can act quickly, but their distance from Soviet-era residents makes public trust difficult to win.", c.M(pp=8, admin=-4, st=-3)),
        ],
        _e('Village Land Trusts', "Land trusts lease and finance farms while protecting smallholders from immediate sale to distant owners. Rural credit returns and food processing expands, but slow claims review postpones the large capital projects sought by returning investors.", c.M(agri=8, tax=-3, st=3), .0009,
           'Diaspora Machine Fund', "Belarusian communities abroad finance machine shops, rail repairs, and technical schools through a parliamentary fund. Capital and expertise arrive quickly, while overseas donors seek influence over contracts set in Minsk.", c.M(civbuild=5, eff=6, pp=-2), .0012),
        _f('Rural Credit Offices', "Local offices lend for seed, storage, and farm machinery under public oversight. Producers gain a route to modernize without surrendering land, though repayment depends on reliable harvests and transport.", c.M(agri=6, tax=-2, admin=2), .0007, 'agriculture',
           'Belarusian Press', "Publishers and schools restore Belarusian-language books, technical journals, and civic education. Public culture gains reach, while print capacity and skilled editors remain scarce outside the largest cities.", c.M(research=5, st=3, social=2), .0007, 'society', None, {'research': c.R('CAT_electronics', 25)})),
    ('BLR', 2): _route(
        [
            ('civic', 'Municipal Charter', "The Hrodna Circle builds a civic coalition through elected councils, bilingual public services, and local cultural associations. Municipal knowledge can rebuild trust, but regional councils slow decisions that require common standards for the whole republic.", c.M(st=5, admin=-3, pp=-2)),
            ('executive', 'Civic Secretariat', "Teachers, editors, and local administrators coordinate a professional secretariat for the new state. It can make services reliable without a party machine, but a narrow civic leadership risks ignoring workers outside Hrodna's cultural networks.", c.M(admin=-5, research=3, pp=5)),
        ],
        _e('Municipal Workshops', "City councils charter repair firms, furniture makers, and food processors under open procurement rules. Local employment and consumer supply improve, while municipal credit cannot fund the large machine plants that anchor the national economy.", c.M(eff=7, tax=3, build=-2), .0008,
           'Cross-Border Traders', "Private traders and cooperatives reconnect Hrodna's markets with Poland and Lithuania under published customs rules. Goods and income return quickly, though import competition can displace local workshops without careful credit policy.", c.M(civbuild=4, eff=4, corp=-3), .0008),
        _f('Repair Guilds', "Small repair guilds train apprentices and maintain farm equipment, transport, and household machinery. Their work reaches towns quickly, but a fragmented network requires strong inspection to keep standards consistent.", c.M(eff=5, civbuild=3, research=2), .0007, 'industry',
           'Bilingual Schools', "Municipal schools train teachers and provide books in Belarusian and Russian. Families gain equal civic access, while staffing and translation raise recurring costs for local governments.", c.M(st=4, research=3, admin=2), .0006, 'society', None, {'research': c.R('CAT_electronics', 25)})),
    ('BLR', 3): _route(
        [
            ('civic', 'Editorial Assembly', "Writers, teachers, and professional associations create a public assembly to review the cabinet and its cultural policy. Open debate gives reform socialism a broader base, but decisions take longer when workers and rural representatives contest priorities.", c.M(research=4, st=4, pp=-4)),
            ('executive', 'Reform Secretariat', "A reform secretariat joins engineers, editors, and managers to keep enterprises operating during political change. It can preserve expertise, but central coordination gives fewer opportunities for local communities to shape investment.", c.M(eff=5, admin=-4, pp=5)),
        ],
        _e('Enterprise Board', "Workers and technical managers share authority over investment, safety, and production targets in public factories. Practical knowledge improves decisions, while divided control can delay major restructuring and new capital projects.", c.M(eff=6, st=4, civbuild=-2), .0008,
           'Open Workshop Licences', "Small firms receive licences and credit to make household goods, farm parts, and repair services. Consumer supply improves sooner, while unregulated growth can pull skilled staff from the larger plants.", c.M(eff=7, tax=4, admin=3), .0008),
        _f('Factory Account Books', "Enterprises publish debts, deliveries, and public-service obligations before new contracts are signed. Honest accounts expose waste and protect viable plants, but weak firms can no longer hide behind plan targets.", c.M(eff=5, tax=4, pp=-2), .0007, 'industry',
           'Regional Food Stores', "Local storage and food processors reduce spoilage and keep supplies in regional towns. Households benefit from dependable goods, though investment shifts away from export-oriented machine production.", c.M(agri=6, st=3, civbuild=-2), .0007, 'industry')),

    # Moldova
    ('MLV', 1): _route(
        [
            ('civic', 'Village Land Assembly', "The Peasant Party lets farm communities and municipal representatives negotiate land claims before titles are issued. A public hearing can avoid dispossessing current cultivators, but contested estates make restitution slow and politically costly.", c.M(st=4, agri=4, pp=-3)),
            ('executive', 'Agrarian Cabinet', "An agrarian cabinet settles land, rural credit, and food prices through experienced administrators. It can protect harvests quickly, but rural leadership may neglect industrial workers and towns dependent on state factories.", c.M(agri=5, tax=-3, pp=6)),
        ],
        _e('Family Farm Titles', "Secure titles and compensation rules encourage family farms to invest in orchards, vineyards, and livestock. Production can adapt to local markets, but concentrated land and unpaid claims threaten rural stability.", c.M(agri=10, tax=4, st=-3), .0009,
           'Cooperative Canneries', "Farmers retain land while joining cooperative canneries, dairies, and wine presses. Shared processing keeps more value near villages, though cooperative borrowing makes large export expansion slower.", c.M(agri=7, eff=5, build=-2), .0008),
        _f('Rural Credit Bank', "A rural bank lends for machinery and seed after resolving the most urgent tenancy claims. Small farms gain productive equipment, while the public fund bears losses when weather or prices spoil repayment.", c.M(agri=6, tax=-3, eff=2), .0008, 'agriculture',
           'Village Food Markets', "Open markets connect growers to towns and encourage local mills, dairies, and food shops. Consumer choice grows, while price swings replace the security of guaranteed state deliveries.", c.M(agri=5, eff=5, st=-2), .0007, 'industry')),
    ('MLV', 2): _route(
        [
            ('civic', 'Writers Assembly', "The Writers' Union convenes Romanian-speaking, Russian-speaking, Ukrainian, and Gagauz representatives to shape education and public language. Cultural autonomy can reduce fear of exclusion, but every school and office needs costly translation and trained staff.", c.M(st=5, research=3, admin=3)),
            ('executive', 'Cultural Ministry', "A professional cultural ministry protects publishing, museums, and education through common standards. It can act faster than dispersed local boards, while communities may distrust centralized choices about language and history.", c.M(research=5, pp=5, admin=-3)),
        ],
        _e('Cooperative Food Trust', "Growers and processors share cold storage, bottling, and export contracts through a cooperative trust. Regional farms gain bargaining power and local jobs, while shared ownership slows decisions on new equipment.", c.M(agri=8, eff=5, civbuild=-2), .0009,
           'Literary Service Firms', "Independent presses, translation houses, and cultural services win contracts from schools and new private publishers. Skilled jobs diversify the economy, but public access depends on customers able to pay.", c.M(research=5, eff=4, corp=2), .0007),
        _f('Farm Processing Lines', "Cooperative bottling and canning lines give village producers a route from harvest to market. More value stays in the countryside, though seasonal crops leave the equipment underused for part of the year.", c.M(agri=6, eff=4, energy=2), .0008, 'industry',
           'Multilingual Books', "Teachers and editors produce schoolbooks that reflect the republic's languages and local histories. Students gain access and shared civic knowledge, while print runs raise public costs in a small market.", c.M(research=4, st=4, social=2), .0006, 'society', None, {'research': c.R('CAT_electronics', 25)})),
    ('MLV', 3): _route(
        [
            ('civic', 'Workers Congress', "Workers, cultural associations, and elected delegates debate the new socialist constitution. Public ownership remains legitimate only if citizens can challenge the party and influence services, which makes policy slower and more contested.", c.M(st=5, pp=-4, research=3)),
            ('executive', 'Reform Cabinet', "A reform cabinet of engineers and managers grants enterprises more autonomy while retaining public ownership. It can improve output without immediate privatization, but workers have less influence when managers close or reorganize plants.", c.M(eff=6, pp=6, st=-3)),
        ],
        _e('Public Food Combine', "Public combines coordinate vineyards, canneries, and rural transport under accountable enterprise books. They can guarantee food supply and stable employment, but their costs remain a charge on the state when export orders falter.", c.M(agri=8, eff=5, tax=-2), .0010,
           'Worker Market Co-ops', "Worker cooperatives sell food, clothing, and repair services under clear market contracts. Flexible production responds to shortages, while unequal access to credit can leave rural members behind.", c.M(eff=7, agri=4, tax=3), .0008),
        _f('Enterprise Councils', "Workers elect councils to review safety, investment, and public-service duties inside state firms. Participation can protect skilled teams, though negotiations slow conversion of plants with obsolete equipment.", c.M(st=4, eff=4, civbuild=-2), .0007, 'industry',
           'Local Market Halls', "Municipal market halls connect growers, artisans, and town consumers under published rules. Everyday goods circulate more freely, while price changes expose households with fixed wages to new uncertainty.", c.M(agri=5, eff=4, tax=2), .0007, 'industry')),
    ('MLV', 20): _route(
        [
            ('civic', 'Patriotic Assembly', "The National Patriotic Front submits its programme to an elected constituent assembly and recognizes that independence requires broad Romanian-speaking and minority support. Open debate may delay national measures, but it prevents clandestine authority from becoming a new monopoly.", c.M(st=5, pp=-4, research=3)),
            ('executive', 'National Directorate', "A national directorate coordinates the front's cadres, public offices, and language transition. Central authority can replace Soviet institutions quickly, but coercive appointments risk reviving the distrust built by clandestine rule.", c.M(pp=10, admin=4, st=-5)),
        ],
        _e('Restitution Orchards', "Former owners and current cultivators settle claims through compensation, long leases, or return of selected orchards and vineyards. Clear rights can lift investment, while unresolved claims threaten harvests and village peace.", c.M(agri=8, tax=4, st=-3), .0009,
           'Romanian Credit Links', "Moldavian firms seek credit and machinery through Romanian commercial ties while retaining their own legal titles. New supply channels accelerate modernization, but dependency on Bucharest narrows the republic's economic room.", c.M(eff=6, civbuild=4, corp=-3), .0010),
        _f('Latin Script Schools', "Schools and courts adopt Latin-script Romanian with teacher training and translated public forms. Administration becomes more accessible to Romanian speakers, while other language communities need guarantees and costly parallel services.", c.M(research=5, admin=3, st=-2), .0006, 'society',
           'Orchard Packing Houses', "Small packing houses and cold stores help growers sell fruit and wine to nearby markets. Rural earnings improve, though market access depends on stable crossings and foreign buyers.", c.M(agri=6, eff=4, civbuild=3), .0008, 'industry', None, {'research': c.R('CAT_industry', 25)})),

    # Estonia
    ('EST', 0): _route(
        [
            ('civic', 'Restoration Parliament', "The government in exile convenes residents and returning representatives to settle citizenship, property, and constitutional continuity. A broad parliament makes restoration credible at home, but compromises with Soviet-era institutions limit the speed of legal reversal.", c.M(st=5, pp=-4, research=3)),
            ('executive', 'Continuity Cabinet', "The former state administration returns through a continuity cabinet with experienced diplomatic and legal officials. It can restore public offices quickly, though distance from local communities leaves the executive short of trust and technical staff.", c.M(pp=7, admin=-4, st=-3)),
        ],
        _e('Co-op Shale Power', "Public utilities retain the oil-shale system while cooperatives and municipalities improve efficiency and environmental safeguards. Stable electricity supports industry, but the state inherits pollution costs and expensive equipment renewal.", c.M(power=5, energy=-3, eff=3), .0011,
           'Baltic Engineering', "Private engineering workshops gain credit and port access to serve Nordic and Baltic customers. Skilled export jobs grow quickly, while small firms face strong foreign competition and volatile demand.", c.M(eff=7, civbuild=4, corp=-3), .0010),
        _f('Port Workshop Fund', "A public fund repairs cranes, rail equipment, and precision tools needed for trade. Export capacity returns, though port investment leaves less money for housing and rural services.", c.M(civbuild=4, eff=3, build=2), .0009, 'industry',
           'Returnee Housing Bonds', "Parliament issues bonds for rental housing used by returning families and local residents. Skilled workers can settle near ports and factories, while debt service limits future public borrowing.", c.M(st=4, build=4, tax=-2), .0010, 'society', None, {'building': c.B('infrastructure')})),
    ('EST', 1): _route(
        [
            ('civic', 'Exile Council', "The National Council shares authority among exile organizations, socialists, and younger advocates of restoration. Coalition government brings more voices into the state, but requires the older government-in-exile to surrender its claim to exclusive continuity.", c.M(st=5, research=3, pp=-4)),
            ('executive', 'Returnee Cabinet', "A cabinet of returning lawyers, engineers, and administrators rebuilds national ministries. Experience shortens the institutional gap, but residents who carried the republic through Soviet rule may see returnees as distant decision-makers.", c.M(admin=-5, pp=7, st=-3)),
        ],
        _e('Public Port Authority', "A public port authority reinvests dues in harbours, rail links, and coastal engineering. Export revenues remain accountable to parliament, though public ownership slows private upgrades and places maintenance costs on the state.", c.M(eff=5, civbuild=4, tax=2), .0010,
           'Diaspora Workshop Fund', "Exile communities buy shares in engineering firms, repair shops, and food exporters. Capital and expertise return quickly, but foreign shareholders can redirect production toward external buyers.", c.M(eff=6, civbuild=4, corp=-3), .0009),
        _f('Baltic Trade Standards', "Common technical standards help Estonian factories meet Nordic and Baltic contracts. Export quality improves and skilled jobs return, while certification expenses burden older plants and smaller suppliers.", c.M(eff=5, tax=3, research=2), .0007, 'industry',
           'Returnee Housing Fund', "Public housing repairs and rental construction help skilled families return without displacing current residents. Labour supply improves, while building costs compete with industrial modernization and ports.", c.M(st=4, build=4, tax=-2), .0010, 'society', None, {'building': c.B('infrastructure')})),
    ('EST', 2): _route(
        [
            ('civic', 'University Charter', "The Cassette Generation's writers and students establish academic freedom and local language rights as public guarantees. Independent universities nurture skill and debate, while government gives up the ability to direct research toward immediate state needs.", c.M(research=6, pp=-4, admin=3)),
            ('executive', 'Technical Cabinet', "Engineers, editors, and planners form a cabinet able to restore technical services and open Baltic trade. It can build capacity quickly, though cultural activists fear that economic priorities will once again silence public debate.", c.M(eff=5, pp=6, research=-3)),
        ],
        _e('University Co-ops', "Universities and research institutes retain public assets while selling engineering and environmental services to Baltic firms. Scientific work gains customers, but commercial contracts can displace basic research and open teaching.", c.M(research=6, eff=4, corp=-2), .0008,
           'Clean Coast Firms', "Independent firms win contracts for waste treatment, marine repair, and clean industrial equipment. Coastal employment and technology grow, while compliance costs make early profits uncertain.", c.M(eff=5, energy=-4, corp=2), .0008),
        _f('Marine Research Fund', "Universities and local firms test safer methods for coastal energy and shipping. Research supports future industry, but expensive equipment gives little immediate relief to households.", c.M(research=5, energy=-3, eff=2), .0007, 'research',
           'Coastal Repair Shops', "Small firms repair boats, appliances, and port equipment for coastal communities. Local service jobs grow, while fragmented ownership makes quality and safety harder to enforce.", c.M(eff=5, tax=3, admin=2), .0007, 'industry', {'research': c.R('CAT_electronics', 25)})),
    ('EST', 3): _route(
        [
            ('civic', 'Labour Parliament', "The exile Social Democrats restore parliamentary bargaining among unions, employers, and municipalities. Workers gain a lawful voice in economic change, while agreement takes time and can frustrate a government facing urgent supply shortages.", c.M(st=5, pp=-4, research=3)),
            ('executive', 'Labour Cabinet', "Social-democratic ministers coordinate public services and collective bargaining through a professional civil service. It can protect wages while reopening trade, but centralized negotiation limits local unions' ability to shape each factory's future.", c.M(social=4, pp=7, st=-3)),
        ],
        _e('Public Utility Trust', "A parliamentary trust retains energy and transport assets while workers and municipalities oversee investment. Reliable services support industrial recovery, but public debt grows as shale plants and networks require modernization.", c.M(power=4, build=4, social=3), .0010,
           'Nordic Labour Firms', "Worker-managed firms and private exporters receive credit under common labour and safety rules. New orders can revive engineering, while higher standards and wage costs make older plants less competitive.", c.M(eff=6, civbuild=4, corp=-2), .0009),
        _f('Bargaining Law', "Unions negotiate plant-level wages, retraining, and closure plans before enterprise conversion. Skilled workers remain involved, but production adjustments take longer when employers and unions disagree.", c.M(st=4, eff=3, build=-2), .0006, 'society',
           'Public Health Service', "Clinics and preventive care remain available as workers change jobs and ownership shifts. Families gain security, while service costs reduce funds available for port and factory investment.", c.M(st=4, social=4, tax=-2), .0008, 'society')),

    # Latvia
    ('LAT', 0): _route(
        [
            ('civic', 'Citizenship Court', "The diplomatic service's continuity claim must be joined to fair citizenship rules for residents who remained in Latvia. A court protects due process and broadens trust, while complex claims slow the return of land and property.", c.M(st=5, admin=4, pp=-3)),
            ('executive', 'Restoration Cabinet', "A cabinet of diplomats and returning officials restores ministries and the prewar legal order. It can act quickly, but residents with Soviet-era careers and Russian-language institutions may feel excluded from the new state.", c.M(pp=8, admin=-4, st=-4)),
        ],
        _e('Public Port Works', "The state retains Riga's port and rail links, directing dues toward repair and industrial access. Public control protects national revenue, but scarce capital and state maintenance obligations delay new consumer businesses.", c.M(civbuild=4, tax=3, build=3), .0010,
           'Riga Merchant Houses', "Private exporters and repair firms regain access to Baltic markets under commercial law. Jobs and goods return quickly, while outside buyers gain leverage over investment and port priorities.", c.M(eff=6, civbuild=4, corp=-3), .0009),
        _f('Rail and Harbour Fund', "A public fund repairs the rail lines, cranes, and warehouses that connect Riga to regional producers. Trade recovers, though port investment leaves less immediate capital for housing.", c.M(civbuild=4, tax=3, build=3), .0009, 'industry',
           'Citizenship Offices', "Local offices help residents resolve citizenship, language, and pension claims. Families gain clear access to public services, while administration remains costly during the transition years.", c.M(st=4, admin=3, pp=-2), .0006, 'institution', None, {'building': c.B('infrastructure')})),
    ('LAT', 1): _route(
        [
            ('civic', 'Diaspora Assembly', "The World Federation of Free Latvians shares authority with residents, social democrats, and municipal representatives. A broad coalition can mobilize overseas capital without ruling from exile, but it slows decisions over property and citizenship.", c.M(st=5, research=3, pp=-4)),
            ('executive', 'Foreign Policy Council', "Experienced exile diplomats and federation leaders coordinate recognition, trade, and the return of skilled families. Their networks bring contacts quickly, but a cabinet led abroad risks neglecting local voices.", c.M(influence=5, pp=7, st=-3)),
        ],
        _e('Diaspora Capital Fund', "Latvian communities abroad subscribe capital for port repair, housing, and small manufacturers under parliamentary review. Investment returns home quickly, while donors expect influence over projects and dividend payments.", c.M(eff=6, build=4, tax=3), .0010,
           'Private Port Leases', "Parliament leases selected port services and warehouses to Latvian and Nordic firms. Efficiency and trade can improve, but foreign operators gain leverage over employment and national transport.", c.M(eff=5, civbuild=4, tax=-3), .0009),
        _f('Diaspora Machine Shops', "Overseas engineers help reopen workshops that make transport and factory parts. Skilled employment returns, while equipment and quality standards depend on continued foreign contacts and credit.", c.M(eff=5, research=3, civbuild=3), .0008, 'industry',
           'Riga Housing Bonds', "Public bonds finance rental homes for local families and returnees near port and engineering jobs. Labour supply improves, but repayment limits later borrowing for industry.", c.M(st=4, build=4, tax=-2), .0010, 'society', {'research': c.R('CAT_industry', 25)}, {'building': c.B('infrastructure')})),
    ('LAT', 2): _route(
        [
            ('civic', 'Language Rights Pact', "The Latvian Sixtiers turn language access and cultural autonomy into enforceable public rights. A bilingual civic settlement can include residents wary of restoration politics, while requiring sustained translation and teacher training.", c.M(st=5, research=4, admin=2)),
            ('executive', 'Cultural Cabinet', "A cabinet of educators and municipal officials restores Latvian-language schools and local institutions. It can act coherently, but central standards risk crowding out regional voices and independent cultural debate.", c.M(research=5, admin=-4, pp=5)),
        ],
        _e('Clean Public Utilities', "Municipal utilities remain public while investing in cleaner heating, water, and industrial standards. Residents gain reliable services and cleaner cities, but public investment is slower than selling concessions to private operators.", c.M(energy=-4, st=3, build=3), .0009,
           'Green Workshop Permits', "Independent firms receive licences for repair, waste handling, and efficient equipment. Local innovation can reduce pollution and create jobs, while weak early standards risk uneven environmental results.", c.M(eff=5, energy=-3, tax=3), .0008),
        _f('Coastal Monitoring', "Public laboratories monitor industrial discharge and port pollution, guiding permits with measured evidence. Environmental policy becomes credible, although clean-up follows only as fast as public budgets allow.", c.M(research=4, energy=-3, agri=2), .0007, 'research',
           'Local Language Presses', "Small presses publish Latvian and Russian-language civic information and technical manuals. Residents can navigate public services and new businesses, while printing costs limit circulation outside the cities.", c.M(research=4, st=3, admin=2), .0006, 'society', {'research': c.R('CAT_electronics', 25)})),
    ('LAT', 3): _route(
        [
            ('civic', 'Workers Parliament', "The exile Social Democrats join unions, parliamentarians, and local representatives in a new legislature. Public bargaining guards against authoritarian restoration, while broader consultation slows urgent industrial conversion.", c.M(st=5, pp=-4, research=3)),
            ('executive', 'Social Democratic Govt', "A parliamentary cabinet coordinates labour law, social insurance, and export industries through professional ministries. It can protect workers during change, but its public obligations burden a budget short of revenue.", c.M(social=4, pp=7, st=-3)),
        ],
        _e('Public Port Authority', "A public corporation retains port and rail revenue for worker protections and equipment renewal. National control preserves income, but debt and maintenance costs reduce funds for private industry.", c.M(eff=4, social=3, tax=3), .0010,
           'Worker Export Firms', "Private exporters and worker cooperatives compete for engineering and timber orders under union contracts. Flexible production raises output, while wage and safety standards make new contracts more expensive.", c.M(eff=6, civbuild=4, corp=-2), .0009),
        _f('Workers Insurance Fund', "Employers and unions fund retraining, injury support, and temporary unemployment benefits during factory changes. Families gain protection, while payroll costs reduce investment in older plants.", c.M(st=4, social=4, corp=-2), .0008, 'society',
           'Export Standards', "Engineers and workers certify machinery, timber, and port services for foreign customers. Contracts become more dependable, though compliance costs hit small firms hardest and delay expansion.", c.M(eff=5, tax=3, research=2), .0007, 'industry')),

    # Lithuania
    ('LIT', 0): _route(
        [
            ('civic', 'Continuity Assembly', "The Lithuanian diplomatic service brings legal continuity before a parliament of residents, exiles, and local institutions. The settlement can restore the state without erasing those who stayed, but land and citizenship claims require slow hearings.", c.M(st=5, pp=-4, admin=3)),
            ('executive', 'Restoration Cabinet', "Returning officials and legal experts rebuild ministries under the prewar constitution. Administrative experience helps restart courts and services, while residents raised under Soviet rule may distrust decisions made by returnees.", c.M(pp=8, admin=-4, st=-3)),
        ],
        _e('Land Claims Court', "A court settles claims between former owners, tenants, and families cultivating farms today. Fair rulings let credit return to the countryside, but compensation and title disputes weigh heavily on public accounts.", c.M(agri=6, tax=3, build=-2), .0009,
           'Baltic Export Bank', "Private and cooperative firms receive credit to sell machinery, wood products, and food across the Baltic. New markets attract investment, while exposure to foreign prices makes employment less secure.", c.M(civbuild=4, eff=5, corp=-3), .0009),
        _f('Farm Restitution Board', "Local offices record land claims and protect current tenants while courts review ownership. Farmers can plan planting seasons, though unresolved cases continue to delay large investments.", c.M(agri=5, admin=3, st=2), .0007, 'agriculture',
           'Rail Export Warehouses', "Warehouses and rail depots help Lithuanian producers store goods for export and domestic sale. Spoilage falls and routes improve, while construction diverts funds from housing.", c.M(eff=4, tax=3, build=3), .0009, 'industry', None, {'building': c.B('infrastructure')})),
    ('LIT', 1): _route(
        [
            ('civic', 'Catholic Social Pact', "Christian Democrats write parish education and social welfare into a pluralist constitution under elected civilian law. Community institutions gain standing, while the state must guarantee equal access to citizens outside church networks.", c.M(st=5, social=3, pp=-3)),
            ('executive', 'Stewardship Cabinet', "An experienced cabinet coordinates family farms, schools, and public services through national ministries. It can protect a social settlement quickly, but centralized appointments risk making Catholic institutions instruments of government.", c.M(pp=8, admin=-4, research=-3)),
        ],
        _e('Parish Co-op Banks', "Parish and village banks lend to family farms, dairies, and small workshops with public audits. Local savings support productive work, while small deposits cannot fund major industrial expansion.", c.M(agri=8, eff=4, tax=-3), .0008,
           'Christian Trade Houses', "Independent firms link Lithuanian manufacturers to diaspora buyers and Baltic markets. Trade and small business expand, while commercial influence can outpace the social safeguards that Christian Democrats promise.", c.M(civbuild=4, eff=5, corp=-3), .0009),
        _f('Farm Machinery Guilds', "Cooperative guilds repair tractors and train mechanics for family farms. Harvest reliability improves, though a dispersed service network costs more than centralized industrial depots and reduces scale.", c.M(agri=6, energy=2, eff=3), .0008, 'agriculture',
           'Parish School Renewal', "Parishes and municipalities repair schools and train teachers in local districts. Education and community life recover, while construction costs limit factory investment and transport renewal.", c.M(st=4, research=3, social=2), .0007, 'society', None, {'building': c.B('infrastructure')})),
    ('LIT', 2): _route(
        [
            ('civic', 'Open Society Charter', "Santara-Sviesa's liberal diaspora tradition protects individual rights, secular education, and civic associations. Independent courts can restrain a new executive, while open debate may slow decisions on urgent enterprise reform.", c.M(research=5, pp=-4, st=3)),
            ('executive', 'Liberal Cabinet', "Educators, lawyers, and returning professionals coordinate reforms through a cabinet accountable to parliament. Technical expertise helps rebuild public institutions, but centralized administration can frustrate the federation's preference for open civic life.", c.M(admin=-5, research=3, pp=6)),
        ],
        _e('University Endowments', "Public universities retain their campuses while diaspora endowments support laboratories and independent research. Scientific work gains resources, but donors can influence subjects and universities must protect open access.", c.M(research=7, social=2, corp=-2), .0008,
           'Small Firm Charter', "Family firms and repair shops receive predictable licences, bank credit, and access to imported tools. Employment and household supply grow quickly, while small businesses strain a new tax administration.", c.M(eff=7, civbuild=4, admin=3), .0008),
        _f('Open University Press', "Independent presses publish Lithuanian science, law, and history for universities and public libraries. Knowledge and civic debate expand, though print and translation costs limit circulation.", c.M(research=5, st=2, pp=-2), .0006, 'research',
           'Family Workshop Loans', "Local banks finance repair shops, furniture makers, and food processors in smaller towns. Jobs spread beyond Vilnius, while uneven credit risks favour communities with better connections.", c.M(eff=5, tax=3, st=2), .0007, 'industry', {'research': c.R('CAT_electronics', 25)})),
    ('LIT', 3): _route(
        [
            ('civic', 'Labour Parliament', "The Social Democrats bring unions, municipal representatives, and parliamentary parties into a negotiated settlement. Workers gain a voice in public ownership and conversion, while coalition bargaining makes policy slower.", c.M(st=5, pp=-4, research=3)),
            ('executive', 'Labour Cabinet', "A social-democratic cabinet coordinates wages, public services, and industrial contracts through professional officials. It can keep essential plants operating, but the treasury carries heavy costs while exports recover.", c.M(social=4, pp=7, st=-3)),
        ],
        _e('Public Utility Board', "Parliament retains energy and transport utilities under worker and municipal oversight. Reliable services support farms and factories, though maintenance and pensions compete for scarce public funds.", c.M(power=4, social=3, build=3), .0010,
           'Co-op Export Firms', "Worker cooperatives and private exporters bid for Baltic machinery, food, and timber contracts under labour law. Market access improves, while smaller firms face unpredictable prices and wage obligations.", c.M(eff=6, civbuild=4, corp=-2), .0009),
        _f('Bargaining Act', "Unions negotiate wages, safety, and retraining before plants change ownership or close. Workers gain protection, though agreements can keep obsolete production running longer and raise consumer prices.", c.M(st=4, eff=3, build=-2), .0006, 'society',
           'Public Housing Repairs', "Municipalities repair apartments, heating, and clinics before expanding new construction. Industrial families retain essential services, but fewer funds remain for modernization, new housing, and transport.", c.M(st=4, social=3, build=-2), .0008, 'society', None, {'building': c.B('infrastructure')})),
    ('LIT', 20): _route(
        [
            ('civic', 'Constitutional Union', "Nationalists share authority with parliamentarians, Catholic associations, and municipal leaders under a written constitution. The coalition broadens consent beyond the interwar party tradition, while limiting the executive's ability to impose one national line.", c.M(st=4, pp=-4, research=2)),
            ('executive', 'National Directorate', "A strong directorate coordinates language, industry, and public appointments through loyal officials. It can establish the new state quickly, but centralized authority revives memories of authoritarian interwar government.", c.M(pp=10, admin=4, st=-5)),
        ],
        _e('Family Industry Trusts', "Private and cooperative trusts invest in Lithuanian machine shops, food processing, and domestic suppliers. National firms gain capital, while contract favoritism and family concentration can limit competition.", c.M(eff=6, civbuild=4, corp=3), .0009,
           'Priority Contracts', "A national board directs contracts for army vehicles, radios, ammunition, and other strategic goods to favoured domestic firms. Military supply can expand quickly, while political patronage and weak competition raise costs.", c.M(out=7, build=4, pp=5), .0010),
        _f('National Tool Works', "A state-backed tool works supplies farms and small manufacturers that cannot import machinery. Domestic capacity grows, but subsidies can preserve plants that never become efficient.", c.M(eff=5, civbuild=4, energy=3), .0010, 'industry',
           'Rural Land Registry', "Registries and credit offices record farm titles and support local food producers. Rural investment improves, while disputes over former estates remain politically sensitive and costly.", c.M(agri=6, tax=3, st=-2), .0007, 'agriculture', {'building': c.B('industrial_complex')})),

    # Georgia
    ('GEO', 1): _route(
        [
            ('civic', 'Regional Language Pact', "The Writers' Union protects Georgian public culture while guaranteeing education and civic access for Abkhaz, Ossetian, Armenian, and other communities. Local consent strengthens the republic, but language services require trained teachers and durable funding.", c.M(st=5, research=4, admin=3)),
            ('executive', 'Cultural Ministry', "A national ministry coordinates schools, publishing, and public history across the republic. Common standards strengthen Georgian-language education, while communities outside Tbilisi fear that cultural policy will be set without them.", c.M(research=5, pp=6, admin=-3)),
        ],
        _e('Winegrower Co-ops', "Village cooperatives share presses, storage, and export contracts for wine, tea, and fruit. Growers retain local control and earn more from processing, while fragmented ownership slows large investment.", c.M(agri=8, eff=5, civbuild=-2), .0009,
           'Black Sea Arts Firms', "Private studios, publishers, and tourism firms connect Georgian culture to Black Sea markets. Skilled jobs and visitors diversify income, while seasonal demand and outside ownership make earnings uncertain.", c.M(eff=6, tax=3, corp=-2), .0008),
        _f('Regional Press Network', "Local presses publish Georgian literature, technical works, and histories of the republic's regions. Education and civic participation improve, though printing costs compete with roads and agricultural investment.", c.M(research=5, st=3, social=2), .0007, 'society',
           'Black Sea Repair Yards', "Small yards repair fishing vessels, port equipment, and agricultural machinery. Coastal employment grows, but specialized parts remain expensive to import and maintain at local yards.", c.M(eff=5, civbuild=3), .0008, 'industry', {'research': c.R('CAT_electronics', 25)})),
    ('GEO', 2): _route(
        [
            ('civic', 'Artists Assembly', "The Georgian film community invites universities, municipalities, and regional artists into a cultural assembly. Independent art can support public debate, but urban institutions must answer to citizens outside Tbilisi.", c.M(research=5, st=3, pp=-3)),
            ('executive', 'Studio Secretariat', "A professional secretariat coordinates film, technical education, and cultural exports through common standards. It can keep studios operating, while central direction risks reducing artists to instruments of state promotion.", c.M(research=4, eff=4, pp=5)),
        ],
        _e('Public Film Studios', "State studios retain equipment and train technicians for Georgian film and television. Domestic production and skilled work survive, though public budgets subsidize projects without secure audiences.", c.M(research=5, eff=3, social=2), .0008,
           'Independent Studios', "Small producers and cinemas receive commercial rights to reach Georgian and foreign audiences. Private investment brings equipment faster, while popular projects can crowd out regional and experimental work.", c.M(civbuild=6, eff=5, corp=-2), .0008),
        _f('Technical Film School', "A film school trains sound engineers, editors, and camera crews for domestic studios and broadcasters. Technical skill grows, but graduates need jobs beyond publicly financed productions.", c.M(research=5, eff=2, social=2), .0007, 'research',
           'Regional Cinema Houses', "Municipal cinemas and mobile screenings bring Georgian films to towns and mountain communities. Public culture reaches further, while upkeep costs exceed ticket revenue in smaller districts.", c.M(st=3, social=3, admin=2), .0007, 'society', {'research': c.R('CAT_electronics', 25)})),
    ('GEO', 3): _route(
        [
            ('civic', 'Local Soviets', "The Menshevik tradition restores elected local councils and a constituent assembly rather than a party monopoly. Regions gain a voice over land and services, while coalition debate slows national decisions.", c.M(st=5, pp=-4, agri=3)),
            ('executive', 'Parliamentary Cabinet', "A cabinet accountable to parliament coordinates agrarian reform, transport, and trade. Professional officials can secure continuity, but central ministries may overrule local priorities in the name of national recovery.", c.M(admin=-4, pp=7, research=2)),
        ],
        _e('Village Land Co-ops', "Farmers combine land, machinery, and produce marketing through voluntary cooperatives rather than state collectivization. Rural output and participation improve, but the model struggles to finance large industrial projects.", c.M(agri=9, tax=-3, st=3), .0009,
           'Private Export Houses', "Independent firms trade wine, tea, and agricultural goods through Black Sea routes under parliamentary law. Export earnings rise quickly, while private merchants can dominate small producers and regional markets.", c.M(tax=3, agri=5, corp=-3), .0009),
        _f('Elected Rural Banks', "Local banks lend to farms and cooperatives under elected council oversight. Producers gain credit close to home, though fragmented lending increases administrative cost and default risk.", c.M(agri=6, tax=-2, admin=3), .0007, 'agriculture',
           'Rail Repair Workshops', "Public workshops repair rail, bridges, and freight equipment serving farms and coastal ports. Trade links recover, but maintenance draws funds from new roads and schools.", c.M(civbuild=3, eff=4, build=2), .0008, 'industry', None, {'building': c.B('infrastructure')})),

    # Armenia
    ('ARM', 0): _route(
        [
            ('civic', 'National Assembly', "The ARF invites rival parties, civic associations, and residents who stayed in Armenia to share constitutional authority. This broadens the party's anti-Soviet mandate, while limiting its claim to speak for the whole nation and diaspora.", c.M(st=5, pp=-5, research=3)),
            ('executive', 'Federation Executive', "A disciplined ARF executive coordinates security, diaspora capital, and national reconstruction through trusted cadres. It can act quickly in a threatened state, but concentrated authority deepens distrust among rival parties and local institutions.", c.M(pp=10, admin=4, st=-5)),
        ],
        _e('Public Power Authority', "The state retains power generation and engineering works as national assets, financing repair and new capacity through public accounts. Strategic control supports independence, but long payback periods burden the treasury.", c.M(power=5, build=4, tax=-3), .0012,
           'Diaspora Industry Fund', "Armenian communities abroad buy shares in machine works, workshops, and exporters under national law. Expertise and capital return quickly, while investors may favour profitable export firms over services in poorer districts.", c.M(eff=6, civbuild=4, corp=-3), .0010),
        _f('Engineering Institutes', "Public institutes train engineers for power, machinery, and industrial maintenance. Technical capacity strengthens self-reliance, though laboratories need imported equipment and years of investment before results appear.", c.M(research=5, eff=3, build=-2), .0008, 'research',
           'Diaspora Trade Houses', "Trade houses connect local firms to Armenian exporters, schools, and suppliers abroad. Commercial links broaden the economy, while outside partners can shape domestic priorities and influence credit terms.", c.M(tax=3, eff=4, influence=3), .0008, 'industry', {'research': c.R('CAT_industry', 25)})),
    ('ARM', 1): _route(
        [
            ('civic', 'Liberal Assembly', "Ramkavar liberals invite diaspora educators, merchants, and local civic groups into a pluralist assembly. Their accommodation with Soviet Armenia helps preserve social ties, while nationalist rivals challenge their right to define the republic's memory.", c.M(research=4, st=4, pp=-3)),
            ('executive', 'Commercial Cabinet', "A cabinet of lawyers, educators, and commercial leaders restores civil administration and diaspora exchange. Expertise accelerates recovery, but reliance on wealthy sponsors can narrow representation in public decisions.", c.M(admin=-4, research=4, pp=6)),
        ],
        _e('University Endowments', "Diaspora endowments equip universities while keeping teaching and research under public charters. Scholars gain equipment and exchange, but donors can steer resources toward institutions with stronger overseas links.", c.M(research=7, social=2, corp=-2), .0009,
           'Diaspora Chambers', "Commercial chambers connect Armenian firms abroad with local workshops and exporters under open contracts. Capital and markets arrive quickly, while outside buyers can capture value and influence investment.", c.M(civbuild=4, eff=5, corp=-3), .0009),
        _f('Technical Scholarships', "Scholarships train engineers, teachers, and accountants for public institutions and private firms. Skills return to the republic, though students may leave again for better-funded laboratories abroad.", c.M(research=5, admin=2, eff=2), .0007, 'research',
           'Export Credit Office', "A public office insures small exporters against delayed payments and failed buyers. Trade grows beyond a few large firms, while the treasury carries losses when markets turn.", c.M(civbuild=4, tax=3, admin=2), .0007, 'industry', {'research': c.R('CAT_electronics', 25)})),
    ('ARM', 18): _route(
        [
            ('civic', 'Workers Assembly', "Hunchakian socialists give unions, teachers, and local representatives a voice in public ownership and welfare policy. Democratic review separates social government from communist monopoly, though bargaining slows urgent decisions.", c.M(st=5, pp=-4, social=3)),
            ('executive', 'Social Cabinet', "A Hunchakian cabinet keeps public firms and services under coordinated management while accepting electoral competition. It can preserve jobs and essential care, but officials gain influence over workers they claim to represent.", c.M(pp=8, eff=4, st=-3)),
        ],
        _e('Worker-Owned Workshops', "Workers and technical managers share ownership of repair shops, machine firms, and food processors. Employees gain a claim on profits and decisions, while dispersed ownership makes large investment difficult.", c.M(eff=8, st=4, build=-3), .0010,
           'Public Enterprise Act', "Public firms retain essential utilities and heavy industry but must publish costs, wages, and service obligations. Social ownership survives, while poor accounts and unprofitable services remain public responsibilities.", c.M(civbuild=5, social=4, tax=-3), .0011),
        _f('Worker Enterprise Plan', "Elected boards review safety, training, and production targets in state firms. Worker voice can protect skilled teams, but plant conversion takes longer when unions resist closures.", c.M(eff=5, st=4, civbuild=-2), .0008, 'industry',
           'Clinics and Schools', "Public clinics and schools retain universal access during economic reform. Families keep essential services, while construction and staffing costs reduce funds for industrial modernization and roads.", c.M(st=4, social=5, build=-3), .0010, 'society', None, {'building': c.B('infrastructure')})),
    ('ARM', 20): _route(
        [
            ('civic', 'Civilian Security Law', "The National United Party places underground security networks under courts, elected ministers, and public rules. Citizens gain legal protection, while former clandestine leaders surrender discretion over surveillance and appointments.", c.M(st=5, pp=-5, admin=4)),
            ('executive', 'Security Council', "A council of trusted independence veterans coordinates border protection and sensitive appointments. The new state can respond to threats quickly, but secrecy limits public oversight and civilian expertise.", c.M(pp=10, defence=4, st=-5)),
        ],
        _e('Strategic Machines', "Public contracts expand civilian machine shops that repair power, transport, and industrial equipment locally. New workshops improve industrial services, but security priorities divert capital from consumer production and raise energy demand.", c.M(eff=6, civbuild=4, energy=4), .0010,
           'Independent Repairs', "Licensed firms compete to repair vehicles, pumps, and factory parts for domestic customers. Supply improves through competition, while small operators may lack capital for strategic equipment.", c.M(eff=6, tax=3, civbuild=3), .0008),
        _f('Civilian Machine Works', "A public plant manufactures essential electrical and mechanical components for the new state. Domestic production reduces dependence on old Union contracts, though equipment remains costly and limited in scale.", c.M(eff=5, build=3, energy=3), .0010, 'industry',
           'Security Court Service', "Independent courts hear security cases and review detention and property claims. Civilian trust improves, while legal safeguards can slow emergency action favored by veterans and security officials.", c.M(st=4, pp=-3, admin=3), .0006, 'institution', {'building': c.B('industrial_complex')})),

    # Azerbaijan
    ('AZE', 1): _route(
        [
            ('civic', 'Secular Republic', "Musavat builds a secular parliamentary republic whose citizenship does not depend on religion or language. Civic law can unite a diverse oil city and countryside, while the party must restrain both clerical influence and nationalist exclusion.", c.M(st=5, pp=-4, research=3)),
            ('executive', 'Republican Cabinet', "A parliamentary cabinet coordinates oil revenue, trade, and public administration through experienced officials. It can protect state continuity quickly, but concentrated executive control risks weakening the pluralism Musavat claims to defend.", c.M(pp=8, admin=-4, tax=3)),
        ],
        _e('Public Oil Dividend', "The republic retains oil and refining assets, publishing revenue and directing a share to education, ports, and non-oil industry. National control funds diversification, but public firms remain exposed to price and equipment shocks.", c.M(oil=5, tax=4, build=3), .0012,
           'Refinery Leases', "Independent firms receive transparent concessions to modernize refineries and sell oil products abroad. Investment and expertise arrive faster, while tax concessions and foreign buyers reduce the public share of the resource.", c.M(eff=6, civbuild=4, corp=-4), .0010),
        _f('Caspian Machine Shops', "Local engineering shops supply pumps, port equipment, and refinery repairs. Skilled employment grows beyond extraction, though domestic firms need imported tools and standards to compete.", c.M(eff=6, civbuild=3, tax=2), .0009, 'industry',
           'Non-Oil Export Credit', "Credit supports food processing, textiles, and shipping services outside the petroleum sector. Employment diversifies, while public funds earn less than they would from another oil expansion.", c.M(eff=5, agri=4, tax=3), .0008, 'industry', {'research': c.R('CAT_industry', 25)})),
    ('AZE', 2): _route(
        [
            ('civic', 'Writers Assembly', "The Writers' Union becomes a secular civic assembly for language, education, and public debate. Its broad cultural reach can support a plural republic, but authors and teachers must share authority with workers and commercial institutions.", c.M(research=5, st=3, pp=-3)),
            ('executive', 'Cultural Secretariat', "Editors, teachers, and scholars coordinate national education and publishing through a professional secretariat. It can restore Azerbaijani-language institutions, while central standards risk suppressing regional and minority voices.", c.M(research=5, admin=-4, pp=5)),
        ],
        _e('Public Publishing Fund', "A public trust funds presses, bookstores, and technical publishing without requiring each title to turn a profit. Cultural access widens, but public subsidy competes with power and transport investment.", c.M(research=6, social=2, tax=-2), .0007,
           'Urban Service Firms', "Private firms repair housing, port equipment, and electrical systems under clear city licences. Jobs grow beyond oil, while weak inspection can let connected contractors capture municipal markets.", c.M(eff=6, tax=4, admin=3), .0007),
        _f('Technical Press', "Editors translate engineering, medicine, and law into Azerbaijani for schools and workshops. Technical access improves, while production costs make wide distribution difficult outside major cities.", c.M(research=5, eff=2, social=2), .0007, 'research',
           'Baku Repair Market', "Small workshops compete to repair household equipment, pumps, and port tools. Consumers find more services, though firms still depend on imported parts and oil-sector wages.", c.M(eff=5, tax=3, civbuild=3), .0007, 'industry', {'research': c.R('CAT_electronics', 25)})),
    ('AZE', 3): _route(
        [
            ('civic', 'Elected Union Councils', "Trade unions gain the right to elect officers, bargain over safety, and challenge management decisions before independent tribunals. Workers acquire real representation, while collective bargaining slows restructuring in oil and refinery plants.", c.M(st=5, pp=-4, eff=3)),
            ('executive', 'Workers Cabinet', "A cabinet of union leaders and technical managers coordinates public energy firms and social services. It protects employment and supply, but risks replacing party officials with another narrow industrial leadership.", c.M(eff=5, pp=7, social=3)),
        ],
        _e('Public Oil and Welfare', "Public oil firms finance worker pensions, clinics, and refinery maintenance from published accounts. Resource wealth supports social security, but generous obligations leave less revenue for non-oil development.", c.M(oil=4, social=5, tax=3), .0011,
           'Worker Co-op Shops', "Workers form cooperatives to repair machinery and produce consumer goods outside the main oil combines. Employment and household supply improve, while member firms struggle to access large credit lines.", c.M(eff=6, st=4, corp=-2), .0008),
        _f('Oil Pension Fund', "A public fund protects refinery, platform, and transport workers during dangerous work and enterprise change. Families gain security, while employer contributions raise costs in aging facilities.", c.M(st=4, social=4, oil=-2), .0008, 'society',
           'Shopfloor Training', "Union training halls teach repair, safety, and electrical skills for industrial workers. Productivity and safety improve, though training draws workers away from already stretched shifts.", c.M(eff=4, train=-3, research=2), .0007, 'industry', None, {'research': c.R('CAT_industry', 25)})),
}
