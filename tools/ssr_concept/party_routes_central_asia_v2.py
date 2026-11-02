# IMPERIA COLD WAR — Central Asian party route concepts
"""Concept-only party economy and sector forks for five Central Asian SSRs."""

import content as c


def _econ(public, market):
    """Make public and market charter tuples in the route data contract."""
    return (
        ('public', public[0], public[1], c.M(**public[2]),
         dict(public_charter=True, gdp_cost=public[3])),
        ('market', market[0], market[1], c.M(**market[2]),
         dict(market_charter=True, gdp_cost=market[3])),
    )


def _follow(suffix, title, lore, modifiers, extra):
    return (suffix, title, lore, c.M(**modifiers), extra)


ROUTES = {
    ('KAZ', 2): dict(
        econ=_econ(
            ('Alash Land Trusts', 'A constitutional land trust will secure grazing routes and regulate leases through elected district councils. Local property rights gain protection, while the trust reconciles family claims with collective farms and industrial concessions.', dict(agri=7, st=3, admin=3), .002),
            ('Steppe Credit Unions', 'Independent credit unions will lend to family farms, veterinary services, and small workshops under public contract law. Local savings can fund practical improvements, but dispersed lending limits capital for large national projects.', dict(agri=6, eff=5, tax=-3), .002)),
        follow=(
            _follow('production', 'Rural Machinery', 'District workshops will repair tractors, pumps, and freight equipment close to farms and mining settlements. Reliable machinery improves harvests and transport, while many small depots cost more to staff than a central combine.', dict(agri=5, supply=-3, eff=3), dict(gdp_cost=.002, kind='agriculture', research=c.R('CAT_industry', 25))),
            _follow('consumer', 'Public Schools', 'Teacher colleges and rural schools will train local officials, engineers, and health workers for a republic spread across immense distances. Civic capacity grows beyond major cities, but salaries and transport delay other investment.', dict(research=5, st=3, social=3), dict(gdp_cost=.0015, kind='society', research=c.R('CAT_industry', 25))))),
    ('KAZ', 3): dict(
        econ=_econ(
            ('Clean Industry Board', 'A public board will inspect mines, military sites, water, and soil before approving new industrial works. Better evidence supports safer investment and local health, but remediation and compliance raise extraction costs.', dict(research=4, agri=4, energy=-3, admin=3), .002),
            ('Repair Cooperatives', 'Worker and community cooperatives will repair equipment, reclaim damaged land, and serve mining settlements. Local knowledge improves practical recovery, while shared ownership complicates large-scale financing and public accountability.', dict(eff=6, agri=4, tax=-2, energy=-2), .002)),
        follow=(
            _follow('production', 'Mine Safety Teams', 'Permanent teams will survey shafts, tailings, and power lines and train crews in prevention. Fewer interruptions protect skilled employment, although inspection and repairs absorb funds that could raise raw output.', dict(supply=-3, st=3, eff=-2), dict(gdp_cost=.0015, kind='industry')),
            _follow('consumer', 'Rural Health Posts', 'Clinics and mobile medical teams will serve mining settlements and distant agricultural districts. Better access protects households and workers, but operating costs recur across a very large territory.', dict(st=4, social=4, admin=2), dict(gdp_cost=.0015, kind='society')))),
    ('KAZ', 20): dict(
        econ=_econ(
            ('Pasture Commons', 'Legally protected grazing and water commons will give local communities a voice before land is committed to mines or large farms. Stewardship strengthens rural confidence, while industrial leases require more negotiation.', dict(agri=7, st=4, build=-3), .0015),
            ('Land Lease Code', 'A transparent lease code will let farms and workshops invest in land and equipment without surrendering civic oversight. Clear contracts support smaller producers, but commercial access may favour well-capitalised districts.', dict(agri=5, eff=5, tax=2), .0015)),
        follow=(
            _follow('production', 'Steppe Repair Shops', 'Regional workshops will maintain farm machinery, rail equipment, and vehicles near the communities that use them. Local employment and supply resilience increase, though dispersed production costs more than a central factory.', dict(eff=5, supply=-3, agri=3), dict(gdp_cost=.002, kind='industry')),
            _follow('consumer', 'Village Stores', 'Cooperative storage, milling, and livestock services will bring everyday goods to rural districts. Household supply improves and producers retain more value, while concentrated heavy investment proceeds more slowly.', dict(agri=6, st=3, civbuild=-3), dict(gdp_cost=.0015, kind='agriculture')))),
    ('UZB', 1): dict(
        econ=_econ(
            ('Language Schools Act', 'Public teacher colleges and libraries will expand Uzbek-language education while retaining technical instruction in Russian. Wider literacy strengthens civic administration, but staffing and translation across remote districts costs time and money.', dict(research=4, st=3, admin=3), .0015),
            ('Local Milling Rights', 'Municipal firms and farm cooperatives will gain rights to mill, store, and sell food near growing towns. Local supply becomes less dependent on distant deliveries, while small operators need credit and reliable transport.', dict(agri=5, eff=5, civbuild=-3, tax=-2), .0015)),
        follow=(
            _follow('production', 'Village Mills', 'Small mills, storage depots, and repair workshops will connect growers with nearby markets. Rural earnings rise and spoilage falls, but dispersed facilities cannot match cotton combines in scale or export receipts.', dict(agri=5, eff=4, tax=-2), dict(gdp_cost=.002, kind='industry')),
            _follow('consumer', 'Public Reading Rooms', 'Libraries and evening courses will bring technical manuals, literature, and civic education to provincial towns. Skilled learning supports future workshops, though teachers and facilities compete with immediate food and irrigation needs.', dict(research=4, st=3, social=2), dict(gdp_cost=.001, kind='society', research=c.R('CAT_industry', 25))))),
    ('UZB', 2): dict(
        econ=_econ(
            ('Irrigation Science', 'Republican institutes will measure canal losses, soil salinity, and crop needs before new water allocations. Research can improve yields without expanding acreage, but findings require investment and coordination with upstream neighbours.', dict(research=5, agri=4, admin=3), .002),
            ('Water User Contracts', 'Farm associations will receive enforceable water schedules and pay for measured delivery and canal maintenance. Clear rights reward careful use, but weaker districts may struggle against large farms and state combines.', dict(agri=5, energy=-3, tax=2, admin=2), .0015)),
        follow=(
            _follow('production', 'Textile Engineering', 'Technical schools and mills will adapt machinery for repairable local production and better cloth. New skills broaden industry, but imported components and dependable power remain essential to factory output.', dict(eff=5, research=4, energy=2), dict(gdp_cost=.003, kind='research', research=c.R('CAT_industry', 25))),
            _follow('consumer', 'Canal Repair Crews', 'Engineers and farmers will repair drainage and canals before losses damage another harvest. Reliable local supply protects food crops and downstream communities, while maintenance funds cannot build textile capacity.', dict(agri=6, energy=-3, st=2), dict(gdp_cost=.0015, kind='agriculture')))),
    ('UZB', 3): dict(
        econ=_econ(
            ("Women's Skills College", 'Public colleges will train women for nursing, teaching, textile engineering, and food processing, with placements near local services. Skilled work and household income grow, while safe transport, childcare, and rural staffing require public funds.', dict(research=4, eff=4, tax=2, social=3), .002),
            ('Women’s Work Charters', 'Factory and farm contracts will guarantee equal pay, apprenticeships, and safe access to skilled work for women. Employers gain a wider trained workforce, but enforcement and childcare bring costs smaller firms may resist.', dict(eff=5, tax=3, admin=3), .0015)),
        follow=(
            _follow('production', 'Women’s Trade Halls', 'Training halls will prepare women for electrical repair, textile maintenance, and food plant supervision. More technicians can reduce factory downtime, though recruitment depends on housing, childcare, and reliable transport.', dict(eff=5, research=3, civbuild=2), dict(gdp_cost=.002, kind='industry', research=c.R('CAT_industry', 25))),
            _follow('consumer', 'Rural Health Posts', 'Clinics and maternity services will bring nurses, midwives, and preventive care closer to village households. Public health improves and women’s employment expands, while staffing dispersed districts creates recurring costs.', dict(st=4, social=4, admin=2), dict(gdp_cost=.0015, kind='society')))),
    ('UZB', 14): dict(
        econ=_econ(
            ('Mahalla Service Trusts', 'Municipal trusts will fund water repair, food assistance, and vocational classes under secular law and public audit. Neighbourhood networks can reach households quickly, while officials protect equal access for newcomers and dissenters.', dict(st=4, agri=3, admin=3, social=2), .0015),
            ('Neighbourhood Credit', 'Community credit circles will lend to household workshops, small farms, and market traders under republican contract law. Local savings support flexible work, but borrowers need transparent appeals and protection from personal patronage.', dict(eff=4, agri=4, tax=-3, admin=2), .0015)),
        follow=(
            _follow('production', 'Canal Service Guilds', 'Local service guilds will schedule canal repairs, pump maintenance, and farm deliveries with public engineers. Water and equipment reach users more reliably, but districts must negotiate when seasonal allocations cannot meet every demand.', dict(agri=5, energy=-2, supply=-2), dict(gdp_cost=.0015, kind='agriculture')),
            _follow('consumer', 'Village Skills Rooms', 'Neighbourhood classrooms will combine literacy, bookkeeping, practical trades, and lawful civic education. Families gain useful skills near home, while instruction must remain open and consistent across districts.', dict(research=3, st=3, eff=2), dict(gdp_cost=.001, kind='society', research=c.R('CAT_industry', 25))))),
    ('TRK', 1): dict(
        econ=_econ(
            ('Turkmen Schools Act', 'Public colleges will train Turkmen-language teachers, engineers, and administrators for towns beyond Ashgabat. Local education strengthens civic institutions, while distance and specialist shortages slow coverage across the republic.', dict(research=4, st=3, admin=3), .0015),
            ('Local Press Licences', 'Independent publishers and cultural workshops will receive clear licences to print, repair equipment, and employ apprentices. Cultural work broadens skilled employment, but remote distribution and imported parts limit commercial reach.', dict(eff=4, research=3, tax=2), .0015)),
        follow=(
            _follow('production', 'Teacher Training Halls', 'Technical colleges will train instructors for gas maintenance, irrigation, transport, and vocational schools. Graduates can reduce reliance on distant specialists, but housing and placement costs make results gradual.', dict(research=4, eff=3, admin=2), dict(gdp_cost=.0015, kind='research', research=c.R('CAT_industry', 25))),
            _follow('consumer', 'Desert Repair Depots', 'Small depots will maintain pumps, trucks, and farm equipment closer to settlements spread across the desert. Downtime falls and local jobs grow, while fuel and spare-parts delivery remains expensive.', dict(eff=4, supply=-3, agri=3), dict(gdp_cost=.002, kind='industry')))),
    ('TRK', 2): dict(
        econ=_econ(
            ('Turkmenfilm Institute', 'A public film institute will preserve Turkmen-language production, train technicians, and provide educational screenings outside the capital. Cultural services reach more towns, but public funding leaves studios dependent on official priorities.', dict(research=3, st=4, social=2), .0015),
            ('Studio Service Leases', 'Film and broadcast crews will lease workshops and equipment under clear contracts, keeping room for independent production. Commercial services widen technical employment, but specialist parts and reliable electricity remain scarce.', dict(eff=4, tax=2, supply=-2), .0015)),
        follow=(
            _follow('production', 'Broadcast Repair Shops', 'Technicians will repair cameras, sound equipment, and electrical systems for regional studios and public broadcasters. Practical skills support wider communication, though specialist components must still come from outside the republic.', dict(eff=4, research=3, supply=-2), dict(gdp_cost=.0015, kind='industry')),
            _follow('consumer', 'Mobile Cinema Service', 'Mobile screenings will carry education, news, and Turkmen-language films to distant settlements. Public communication broadens, while vehicles, operators, and electricity add costs across long routes.', dict(st=3, research=2, social=2), dict(gdp_cost=.001, kind='society')))),
    ('TRK', 3): dict(
        econ=_econ(
            ('Gas Workers Charter', 'A public workers’ charter will establish safety inspections, maintenance duties, housing standards, and representation at extraction sites. Skilled crews gain protection and reliable facilities, while repairs and employment guarantees raise costs.', dict(st=4, supply=-2, energy=2, eff=-2), .002),
            ('Field Service Leases', 'Specialist teams will contract for repairs, housing, and safety work at gas fields under published labour rules. Flexible crews can restore equipment quickly, but contracts need enforcement and may weaken permanent employment.', dict(eff=5, build=2, tax=-2), .0015)),
        follow=(
            _follow('production', 'Pipeline Safety Crews', 'Permanent crews will inspect compressors, pipelines, and emergency equipment before breakdowns interrupt deliveries. Reliability protects production and workers, but inspection capacity consumes money and engineers otherwise used for expansion.', dict(supply=-3, eff=2, energy=-2), dict(gdp_cost=.0015, kind='industry')),
            _follow('consumer', 'Workers’ Housing Trust', 'A public trust will maintain water, housing, and clinics for gas and transport workers’ families. Stable communities retain skilled staff, while repairs leave less money for new fields and export facilities.', dict(st=4, social=3, build=-3), dict(gdp_cost=.0015, kind='society')))),
    ('TRK', 14): dict(
        econ=_econ(
            ('Elders’ Land Council', 'Local councils will record pasture access, well maintenance, and village consent before large works begin. Negotiated land use protects established livelihoods, while consultation can delay gas and transport projects with national value.', dict(agri=4, st=4, build=-3), .0015),
            ('Pasture Lease Code', 'A public lease code will clarify seasonal grazing, well access, and compensation for farms and transport works. Predictable rights support investment, but commercial claims can strain customary access unless appeals remain enforceable.', dict(agri=4, eff=3, tax=2), .0015)),
        follow=(
            _follow('production', 'Shared Well Service', 'Village councils and public engineers will maintain wells, pumps, and local canals through published schedules. Reliable water supports livestock and crops, although repair priorities remain contentious in dry seasons.', dict(agri=5, energy=-2, st=2), dict(gdp_cost=.0015, kind='agriculture')),
            _follow('consumer', 'Village Market Roads', 'Local roads and market depots will connect herders, growers, and towns across long distances. Household supply and rural trade improve, while the state accepts a lasting maintenance burden for lightly used routes.', dict(agri=3, tax=2, supply=-2), dict(gdp_cost=.002, kind='industry', building=c.B('infrastructure'))))),
    ('KYR', 1): dict(
        econ=_econ(
            ('Manas Language Fund', 'A public cultural fund will support oral-history archives, multilingual schools, and local research under equal-citizenship rules. Shared heritage gains an institution, while grants must avoid privileging one region or community.', dict(research=4, st=3, admin=2), .0015),
            ('Cultural Workshop Act', 'Local publishers, repair shops, and cultural cooperatives will gain rights to sell work and train apprentices. Small enterprise creates jobs near communities, but poor roads and seasonal access limit the market.', dict(eff=4, tax=2, supply=-2), .0015)),
        follow=(
            _follow('production', 'Rural Power Workshops', 'Technicians will maintain small turbines, pumps, and farm machinery in remote districts. Local repair capacity makes electricity and harvests more reliable, while specialist staff remain scarce outside major towns.', dict(power=3, agri=4, supply=-2), dict(gdp_cost=.0015, kind='industry')),
            _follow('consumer', 'Oral History Archive', 'Universities and local historians will record oral traditions, regional languages, and family histories across the republic. Public learning broadens, but a plural archive must represent communities on fair terms.', dict(research=4, st=3, social=2), dict(gdp_cost=.001, kind='society', research=c.R('CAT_industry', 25))))),
    ('KYR', 2): dict(
        econ=_econ(
            ('River Protection Board', 'Scientists and local councils will monitor water quality, fisheries, pasture, and settlement needs before major works proceed. Better evidence protects livelihoods, but review can slow projects promising rapid industrial returns.', dict(research=4, agri=3, energy=-3), .0015),
            ('Village Service Rules', 'Small firms and cooperatives will receive contracts for repair, food storage, and visitor services in mountain districts. Local employment grows beyond state industry, but roads and power determine whether firms survive.', dict(eff=4, agri=3, tax=2), .0015)),
        follow=(
            _follow('production', 'Lake Survey Service', 'Research teams will map water quality, erosion, and seasonal access around lakes and rivers. Public decisions gain a scientific basis, although surveys do not replace investment in treatment and maintenance.', dict(research=4, agri=2, admin=2), dict(gdp_cost=.001, kind='research', research=c.R('CAT_industry', 25))),
            _follow('consumer', 'Village Workshop Fund', 'Small grants will support repair shops, food storage, and cultural services near mountain communities. Work stays closer to rural households, while firms still need dependable roads, power, and credit.', dict(eff=4, agri=3, st=2), dict(gdp_cost=.0015, kind='industry')))),
    ('KYR', 3): dict(
        econ=_econ(
            ('Factory Account Boards', 'Worker and regional boards will review factory costs, energy use, and deliveries before managers receive new targets. Better information makes reform practical, while shared oversight slows decisions and exposes hidden losses.', dict(eff=4, tax=2, admin=3), .0015),
            ('Cooperative Credit Law', 'Regional banks and producer cooperatives will lend to workshops, power repairs, and food processors under public accounting rules. Local credit spreads investment, but a small deposit base cannot finance rapid modernization.', dict(eff=4, agri=4, tax=-2), .0015)),
        follow=(
            _follow('production', 'Regional Credit Banks', 'Republican banks will direct savings toward hydro repairs, machinery, and suppliers outside the capital. Investment responds to local needs, though lending remains limited by household savings and public guarantees.', dict(build=3, eff=3, agri=3), dict(gdp_cost=.002, kind='industry')),
            _follow('consumer', 'Farm Market Depots', 'Storage and market depots will help livestock and farm producers sell into nearby towns. Rural income and food supply improve, but local trade needs roads and public inspection to protect quality.', dict(agri=5, st=2, tax=-2), dict(gdp_cost=.0015, kind='agriculture')))),
    ('KYR', 14): dict(
        econ=_econ(
            ('Balanced Regions Act', 'Regional assemblies will publish budgets for roads, schools, and clinics under common national standards. North and south receive a voice without becoming ethnic blocs, while national planners lose some investment discretion.', dict(st=4, admin=-3, pp=-2), .0015),
            ('Valley Farm Rights', 'Farmers and local firms will gain rights to market crops, maintain canals, and lease equipment across provincial boundaries. Trade responds to local needs, but differences in water access can create new disputes.', dict(agri=5, eff=3, tax=-2), .0015)),
        follow=(
            _follow('production', 'Regional Road Works', 'Road crews will link mountain settlements, valleys, and markets with a published maintenance schedule. Access to services and workshops improves, but difficult terrain makes construction and upkeep expensive.', dict(build=3, supply=-2, st=2), dict(gdp_cost=.003, kind='industry', building=c.B('infrastructure'))),
            _follow('consumer', 'Valley Irrigation', 'Farmers and engineers will repair canals and agree seasonal allocations for crops, towns, and hydroelectric use. Harvests become more reliable, but upstream and downstream districts must accept shared limits.', dict(agri=6, energy=-2, st=2), dict(gdp_cost=.0015, kind='agriculture')))),
    ('TAJ', 1): dict(
        econ=_econ(
            ('Samanid Culture Trust', 'A secular public trust will support Tajik-language archives, historical research, schools, and provincial cultural centres. Education gains a durable institution, while funding requires equal access and distance from political patronage.', dict(research=5, st=3, admin=2), .0015),
            ('Tajik Publishing Rights', 'Publishers, printers, and bookshops will gain rights to produce Tajik-language material and train apprentices. A wider cultural economy develops, but rural distribution and scarce paper limit reach beyond cities.', dict(eff=4, research=3, tax=2), .0015)),
        follow=(
            _follow('production', 'Provincial Printing', 'Regional presses will print schoolbooks, technical manuals, and public notices closer to readers. Local education and administration improve, though equipment and paper remain dependent on inter-republic deliveries.', dict(research=3, eff=3, admin=2), dict(gdp_cost=.0015, kind='industry')),
            _follow('consumer', 'District Service Posts', 'Teacher and medical colleges will train staff for districts far from Dushanbe. Public services reach more families, but salaries, housing, and transport make rural placements costly to sustain.', dict(st=4, social=3, admin=2), dict(gdp_cost=.0015, kind='society')))),
    ('TAJ', 2): dict(
        econ=_econ(
            ('Provincial Institutes', 'Independent universities and libraries will expand research, literature, and technical education beyond the capital. Open scholarship broadens civic life and trained capacity, but can expose disagreements officials prefer to keep private.', dict(research=5, st=3, pp=-2), .0015),
            ('Village Food Firms', 'Local mills and family workshops will gain commercial rights to process fruit, grain, and dairy near mountain farms. Rural income and food supply improve, though small firms need credit and reliable roads.', dict(agri=5, eff=4, tax=-2), .0015)),
        follow=(
            _follow('production', 'Provincial Libraries', 'Libraries and schools will receive books, teachers, and meeting rooms in provincial towns. Civic exchange and technical learning reach beyond the capital, while the network needs recurring funds and reliable transport.', dict(research=4, st=3, social=2), dict(gdp_cost=.001, kind='society', research=c.R('CAT_industry', 25))),
            _follow('consumer', 'Local Food Processing', 'Small mills and storage facilities will help mountain growers preserve fruit, grain, and dairy near their communities. Rural earnings and supply improve, while dispersed plants cannot match one large combine.', dict(agri=5, eff=3, tax=-2), dict(gdp_cost=.0015, kind='industry')))),
    ('TAJ', 3): dict(
        econ=_econ(
            ('Worker Safety Charter', 'Public enterprises will recognise elected safety representatives, bargaining procedures, and enforceable maintenance standards. Workers gain a voice in restructuring, while inspections and employment commitments pressure fragile enterprise budgets.', dict(st=4, supply=-2, eff=-2, social=2), .0015),
            ('Workshop Lease Law', 'Workers and managers will lease selected workshops and processing lines with clear duties for wages, repairs, and accounts. Local initiative can preserve useful production, but leaseholders carry risk when inputs or customers disappear.', dict(eff=5, tax=-2, admin=2), .0015)),
        follow=(
            _follow('production', 'Dam Safety Crews', 'Engineers and workers will inspect dams, transmission lines, and emergency systems before expanding generation. Reliable electricity protects homes and workshops, while maintenance uses funds that could finance new capacity.', dict(power=3, supply=-3, build=-2), dict(gdp_cost=.0015, kind='industry')),
            _follow('consumer', 'Independent Union Law', 'Trade unions will elect officers who can inspect safety, bargain over wages, and challenge dismissals under public law. Workers gain real protection, while enterprises face new obligations during a fragile transition.', dict(st=4, eff=-2, social=2), dict(gdp_cost=.001, kind='society')))),
    ('TAJ', 12): dict(
        econ=_econ(
            ('Civic Education Trusts', 'Civic religious associations will fund literacy, practical schooling, and clinics through audited public trusts. Local teaching and charity reach underserved districts, while the state guarantees lawful instruction and equal access for girls and minorities.', dict(st=4, research=3, social=2, admin=2), .0015),
            ('Charity Endowments', 'Independent community endowments will support food assistance, village teachers, and small workshops under transparent law. Local giving responds quickly to hardship, but services may become uneven without open and audited grants.', dict(st=4, agri=3, tax=-2, admin=2), .0015)),
        follow=(
            _follow('production', 'Rural Skills Schools', 'Schools will combine literacy, practical trades, and lawful religious instruction under public standards. Villages gain teachers and skilled workers, while equal access and professional oversight must be protected.', dict(research=3, eff=3, st=3), dict(gdp_cost=.001, kind='society', research=c.R('CAT_industry', 25))),
            _follow('consumer', 'Local Charity Clinics', 'Community trusts will publish accounts for clinics, food aid, and education in underserved districts. Local charities reach families overlooked by distant ministries, while independent auditors protect recipients from political pressure.', dict(st=4, social=3, admin=2), dict(gdp_cost=.001, kind='society')))),
}
