# IMPERIA COLD WAR — mutually exclusive republican Union specialisations.
"""Concept programmes: network advantages shrink after independence; assets remain."""
import content as c
from historical_references_v2 import HISTORY_TEXT

SEA={'UKR':'Black Sea','EST':'Baltic Sea','LAT':'Baltic Sea','LIT':'Baltic Sea','GEO':'Black Sea',
     'AZE':'Caspian Sea','KAZ':'Caspian Sea','TRK':'Caspian Sea'}
HISTORICAL={
 'aircraft':{'UKR':'Antonov aircraft, Kharkiv production and Zaporizhzhia engines','GEO':'Tbilisi aircraft assembly','UZB':'Tashkent transport aircraft'},
 'armour':{'UKR':'Kharkiv tank production'},
 'artillery':{},
 'army':{'BLR':'heavy vehicle chassis and western military logistics','KAZ':'large training areas and overland military support','KYR':'mountain training and technical services','TAJ':'mountain logistics and border service'},
 'navy':{'UKR':'Mykolaiv shipyards','EST':'Baltic ports and maritime repair','LAT':'Baltic ports and maritime support','LIT':'Klaipeda merchant shipping and repair','GEO':'Black Sea ports and coastal services','AZE':'Caspian repair and flotilla support','KAZ':'Caspian transport and coastal support','TRK':'Caspian ports and coastal services'},
 'agriculture':{'UKR':'grain and food processing','BLR':'livestock, tractors and agricultural machinery','MLV':'wine, fruit and food processing','EST':'livestock and food processing','LAT':'livestock and food processing','LIT':'agriculture and food processing','GEO':'tea, fruit and subtropical agriculture','ARM':'fruit and agricultural processing','AZE':'cotton and agricultural processing','KAZ':'grain and livestock','UZB':'cotton and irrigation','TRK':'cotton and irrigation','KYR':'livestock and irrigated agriculture','TAJ':'cotton and upstream water management'},
 'industry':{'UKR':'metallurgy and engineering','BLR':'tractors and heavy vehicles','MLV':'tractors and agricultural processing','LAT':'rail vehicles and electrical goods','LIT':'manufacturing and food processing','GEO':'ferroalloys and light industry','ARM':'engineering and precision workshops','AZE':'oil equipment','KAZ':'metallurgy and heavy industry','UZB':'textiles and machinery'},
 'resources':{'UKR':'coal and metallurgical resources','BLR':'potash and fertiliser','EST':'oil shale','GEO':'manganese and ferroalloys','ARM':'non-ferrous mining','AZE':'oil and refining','KAZ':'coal, oil and metals','UZB':'gold and gas','TRK':'gas','KYR':'mining and industrial water use','TAJ':'mining and hydropower investment'},
 'electronics':{'UKR':'defence electronics and technical institutes','EST':'technical and computing research','LAT':'VEF communications equipment','LIT':'Ruta computers and the Sigma association','ARM':'Nairi computers and radioelectronics'},
}

def gear(target,**stats):return dict(target=target,modifiers=stats)

# The native MD continuous_air_production idea lists base and duplicate
# archetypes separately. Use its exact target grammar without assuming that
# a bonus on one archetype automatically covers another equipment family.
AIR_TYPES=('small_plane_airframe','small_plane_strike_airframe','small_plane_cas_airframe',
           'medium_plane_fighter_airframe','medium_plane_airframe','medium_plane_cas_airframe',
           'large_plane_air_transport_airframe')
ARTILLERY_TYPES=('artillery_equipment','medium_tank_artillery_chassis','medium_tank_rocket_chassis')
NAVAL_TYPES=('patrol_boat','corvette','frigate')

def gearset(targets,**stats):return [gear(target,**stats) for target in targets]

BASE_COSTS={
 'aircraft':gearset(AIR_TYPES,build_cost_ic=-.05),
 'armour':[gear('medium_tank_chassis',build_cost_ic=-.06)],
 'artillery':gearset(ARTILLERY_TYPES,build_cost_ic=-.08),
 'army':gearset(('infantry_weapons_type','util_vehicle_type'),build_cost_ic=-.05),
 'navy':gearset(NAVAL_TYPES,build_cost_ic=-.05),
 'electronics':[gear('cnc_equipment_type',build_cost_ic=-.04)],
}

def add(profile):
    M=c.M;B=c.B;R=c.R
    records=[
    dict(key='aircraft',name='Aviation and Aircraft',programme='Union Aviation Programme',legacy='Independent Aviation Complex',kind='air',
      intro='Aircraft production links design bureaux, precision workshops and flying schools across the Union. Common tooling and component orders will lower the cost of light fighters, strike aircraft, air-superiority fighters, multirole aircraft, close-support aircraft and heavy transports. These advantages depend on customers and suppliers beyond the republic.',
      foundation=('Aviation Workshops','Airframe tooling and repair facilities will gather skilled workers around a permanent aviation centre. The workshops must meet specifications issued across a much larger industrial network, with a continuing appetite for specialised materials and power.',B('arms_factory')),
      school=('Aviation Institutes','Designers, production engineers and flying instructors must learn to work with the same technical standards. Strengthening aviation education will give the republic a larger voice in projects whose complexity reaches far beyond a single factory.',R('CAT_aircraft',50,2)),
      base=M(out=5,airtrain=10,energy=4),
      left=('Aircraft Production','Priority will go to manufacturing fighters, strike aircraft, close-support aircraft and heavy transports. Dedicated tooling will lower their production costs further, while better workshop organisation also strengthens military manufacturing. These advantages require the steady flow of materials and technical instructions supplied through the Union.',M(out=5,energy=4),gearset(AIR_TYPES,build_cost_ic=-.10)),
      right=('Air Service Schools','Flying schools and technical service units will take priority over another expansion of aircraft assembly. Better instruction and maintenance can keep aircraft useful for longer, although the training establishment requires instructors, fuel and dependable public funding.',M(airtrain=20,airfuel=-10),None),
      left_follow=('Precision Airframes','Precision workshops will concentrate on consistent components and production quality. Their machinery can support civilian engineering as well, but the investment increases dependence on imported tools and materials.',M(eff=5,energy=2),{}),
      right_follow=('Flight Instructors','A permanent instructor corps will carry experience between schools and operational units. It strengthens the republic\'s technical contribution without allowing training standards to depend on a handful of individual officers.',M(airtrain=8),dict(air_xp=35)),
      join=('Aviation Supply Office','An aviation supply office will coordinate spare parts, workshop schedules and technical documentation. Better administration can reduce waste, but the specialised industry will remain bound to the wider network that sustains its orders.',M(airfuel=-4,admin=3)),
      final=M(research=3),weekly=.00008),
    dict(key='armour',name='Armour Production',programme='Union Armoured Industry',legacy='Independent Armoured Complex',kind='army',
      intro='Armoured vehicle production demands metallurgy, engines, precision machinery and a dependable military customer. Union component orders will lower the cost of main battle tanks and sustain a privileged place in military procurement, provided we accept the cost of building an industrial chain that few republics possess in full.',
      foundation=('Armoured Workshops','Dedicated machining and assembly halls will prepare the republic for armoured vehicle contracts. The new capacity must be supported by testing facilities, trained personnel and a steady supply of engines, armour and other specialised components.',B('arms_factory')),
      school=('Vehicle Design Bureau','A vehicle design bureau will connect local engineers with the Union\'s research and testing institutions. It will allow the republic to improve production methods and adapt established designs to the requirements of long military orders.',R('CAT_tanks',50,2)),
      base=M(out=5,cap=5,energy=4),
      left=('Advanced Armour','Our engineers will pursue demanding standards of protection and mechanical reliability. Better vehicles can justify higher production costs, while placing greater demands on metallurgy, testing and maintenance.',M(cap=8,energy=4),gear('medium_tank_chassis',armor_value=.10,reliability=.08,build_cost_ic=.05)),
      right=('Serial Tank Production','Standardised production will favour long runs of an established vehicle over continual redesign. Methods developed for the tank works will strengthen military manufacturing more broadly. Lower tank costs come at the expense of protection and more ambitious engineering.',M(out=8,energy=3),gear('medium_tank_chassis',build_cost_ic=-.12,armor_value=-.04)),
      left_follow=('Armour Test Grounds','Permanent trials will expose mechanical weaknesses before an entire production series reaches the troops. The testing service will improve the quality of military engineering while committing skilled staff to work that produces no immediate consumer return.',M(research=4,admin=3),dict(army_xp=15)),
      right_follow=('Common Spare Parts','Long production runs become more useful when workshops can exchange tools, parts and repair instructions. Common components will lower the logistical burden of the republic\'s military contribution.',M(supply=-8,cap=4),{}),
      join=('Military Order Book','A dependable military order book will allow workshops to plan beyond the next allocation. That security binds their future to decisions taken by Union procurement offices and to the suppliers needed to honour those commitments.',M(out=4,energy=2)),
      final=M(cap=4),weekly=.00008),
    dict(key='artillery',name='Artillery and Ordnance',programme='Union Ordnance Programme',legacy='Independent Ordnance Complex',kind='army',
      intro='Artillery requires more than an assembly hall: barrels, ammunition, sights and specialised steel must arrive to consistent standards. Union designs and supply contracts will lower the production costs of towed artillery, self-propelled guns and multiple rocket launchers, while committing substantial resources to a demanding industrial role.',
      foundation=('Ordnance Works','Dedicated workshops will manufacture and repair artillery components under Union specifications. The project will have to earn its place beside established producers by supplying dependable equipment and maintaining a trained industrial workforce.',B('arms_factory')),
      school=('Ballistics Institute','A small institute for ballistics and manufacturing science will connect workshop experience with formal research. It will train specialists able to improve ordnance production rather than relying indefinitely on instructions received from elsewhere.',R('CAT_artillery',50,2)),
      base=M(out=5,supply=-4,energy=3),
      left=('Precision Ordnance','The programme will favour accuracy, quality control and demanding specifications in guns and rocket artillery. Better weapons can make each battery more effective, but careful machining and inspection consume part of the savings secured through Union supply.',M(research=3,energy=3),gearset(ARTILLERY_TYPES,soft_attack=.10,build_cost_ic=.06)),
      right=('Volume Production','Standardised guns, launchers and ammunition will take priority over expensive refinements. Large contracts and production methods will benefit the wider armaments industry. Lower artillery costs leave less time for the testing and finishing that protect reliability.',M(out=6,energy=4),gearset(ARTILLERY_TYPES,build_cost_ic=-.14,reliability=-.04)),
      left_follow=('Fire Control Schools','Technical schools will bring artillery officers and industrial specialists into contact with the same methods of observation and fire control. Their experience will improve the republic\'s contribution to military training.',M(org=3,train=3),dict(army_xp=25)),
      right_follow=('Ordnance Stores','A standardised stock of spare parts and handling equipment will support sustained military supply. Storage and inspection remain essential when a single defective batch can undermine the value of a large production run.',M(supply=-7,energy=2),{}),
      join=('Artillery Directorate','A permanent directorate will coordinate technical standards, production and service reports. It can reduce waste between the works and the troops, while adding another specialised establishment to the republican budget.',M(cap=6,admin=3)),
      final=M(out=4),weekly=.00008),
    dict(key='army',name='Ground Forces and Logistics',programme='Union Ground Service Programme',legacy='Independent Ground Service',kind='army',
      intro='Training grounds, repair depots and transport services are as necessary to a large army as its weapons factories. Common small-arms and utility-vehicle orders will lower production costs while the republic develops experienced personnel and the logistical institutions that sustain formations in the field.',
      foundation=('Training Corridors','A reliable transport corridor will connect training areas, depots and technical schools. It strengthens civilian communications as well, though military schedules will make substantial demands on the same facilities.',B('infrastructure')),
      school=('Land Service Schools','Military schools will train officers, mechanics and communications personnel for service in a common command system. The republic\'s reputation will rest on professional standards rather than the size of a parade.',R('CAT_infantry',50,2)),
      base=M(org=5,train=-6,milcost=4),
      left=('Professional Cadres','Longer courses and a permanent instructor corps will favour competence and cohesion. The service will produce better prepared personnel at the price of a slower training cycle and a more expensive establishment.',M(org=10,morale=8,train=6,milcost=5),None),
      right=('Mass Reserve Schools','A larger network of reserve schools will prepare personnel throughout the republic. Rapid instruction broadens mobilisation capacity, while placing greater responsibility on later service to complete the training.',M(train=-18,defence=8,org=-4),None),
      left_follow=('Staff Exercises','Staff exercises will test command, communications and supply together. Officers will learn to recognise the administrative weaknesses that can defeat an otherwise capable formation before it reaches the battlefield.',M(supply=-6),dict(army_xp=35)),
      right_follow=('Reserve Transport','Local transport and mobilisation records will be organised around the reserve system. The additional reach comes with a continuing demand for equipment, staff and practical exercises.',M(supply=-8,milcost=3),dict(army_xp=25)),
      join=('Permanent Service Depots','Permanent repair depots will carry technical knowledge between training cycles and keep equipment from deteriorating in storage. Their work strengthens sustained readiness rather than another brief mobilisation campaign.',M(morale=5,fuel=-5)),
      final=M(defence=4),weekly=.00006),
    dict(key='navy',name='Maritime Industry and Fleet',programme='Union Maritime Programme',legacy='Independent Maritime Complex',kind='navy',
      intro='Shipyards, repair docks and maritime schools can give the republic a distinctive role in the Union\'s naval affairs. Common machinery and orders will lower the cost of patrol boats, corvettes and frigates. Such an industry requires a real working coast and customers able to sustain projects measured in years.',
      foundation=('Maritime Workshops','A dedicated yard will strengthen construction and repair on our coast. Its workforce must master an exacting combination of machinery, welding and marine engineering, supported by suppliers that extend far beyond the port itself.',B('dockyard')),
      school=('Marine Engineering','Maritime schools will train engineers, technicians and officers for coastal service and ship repair. Their expertise will determine whether new capacity becomes a durable industry or another yard dependent on outside specialists.',R('CAT_corvettes',50,2)),
      base=M(dock=8,navalfuel=4,energy=3),
      left=('Shipbuilding Orders','The yards will pursue longer patrol-boat, corvette and frigate runs under common specifications. Stable orders and specialised tooling can lower their production costs further, but the republic must carry a substantial demand for materials and power.',M(dock=12,energy=5),gearset(NAVAL_TYPES,build_cost_ic=-.10,reliability=.05)),
      right=('Coastal Fleet Service','Repair, coastal readiness and technical instruction will take priority over an ambitious construction programme. A dependable local service offers fewer industrial contracts but makes more economical use of the vessels already available.',M(navalorg=12,navalfuel=-10,dock=4),None),
      left_follow=('Marine Suppliers','A network of marine suppliers will make the yards less vulnerable to a missing engine, pump or electrical fitting. The workshops also offer a market for civilian engineering and skilled labour.',M(eff=5,energy=2),{}),
      right_follow=('Coastal Training','Regular coastal exercises will bring technical services and officers into contact with the conditions in which their vessels actually operate. The programme requires persistent attention to fuel, maintenance and instruction.',M(navalorg=5),dict(navy_xp=35)),
      join=('Maritime Directorate','A common directorate will coordinate repairs, training and the yard\'s order book. Better planning can strengthen the maritime economy while reducing the competition between commercial customers and military schedules.',M(dock=5,admin=3)),
      final=M(navalbase=10),weekly=.00008),
    dict(key='agriculture',name='Agriculture and Food',programme='Union Agricultural Programme',legacy='Independent Agricultural Complex',kind='agriculture',
      intro='The Union depends on republican farms for grain, livestock, industrial crops and the food consumed in its cities. Agricultural specialisation can secure machinery, processing contracts and a wider market, while increasing dependence on fuel, fertiliser and coordinated water use.',
      foundation=('Processing District','Processing, storage and repair facilities will keep more of the harvest useful throughout the year. The investment strengthens agriculture only if farms can also obtain the machinery, power and transport required to supply those facilities.',B('agriculture_district')),
      school=('Agricultural Institutes','Agronomists and agricultural engineers will work with producers on machinery, storage and the demands of reliable processing. Their task is to turn technical knowledge into improvements suited to local soils and water.',R('CAT_industry',50,2)),
      base=M(agri=10,energy=3,social=2),
      left=('Intensive Production','Larger mechanised units and concentrated water and fertiliser use will pursue the highest possible agricultural output. The harvest can grow quickly, but the strain on energy, land and neighbouring water users will grow with it.',M(agri=20,energy=8),None),
      right=('Diverse Rural Supply','A broader mix of crops, livestock and local processing will give rural communities more than a single demanding target. The immediate agricultural gain is smaller, while a wider range of goods reaches republican consumers.',M(agri=12,eff=5,tax=-3),None),
      left_follow=('Harvest Machinery','Repair crews and machinery schedules will be organised around the most demanding stages of the harvest. Keeping equipment in the field protects output, provided the republic can maintain its fuel and spare-parts supply.',M(agri=6,energy=3),{}),
      right_follow=('Rural Cooperatives','Producer cooperatives will connect smaller farms, local markets and processing workshops. Their independence improves the use of local knowledge while making the agricultural economy less easy to direct from a single office.',M(agri=5,st=3,admin=3),{}),
      join=('Food Supply Contracts','Long supply contracts will connect republican producers with reliable customers across the Union. They promise a steadier market, at the price of keeping production tied to common payment and delivery arrangements.',M(agri=5,tax=3)),
      final=M(agri=4),weekly=.00004),
    dict(key='industry',name='Civilian Industry',programme='Union Civilian Industry Programme',legacy='Independent Industrial Complex',kind='industry',
      intro='Tractors, machinery, electrical goods and consumer products give a republic a place in everyday economic life across the Union. A civilian industrial programme can broaden skilled employment and commercial capacity, while requiring dependable energy and a large market for its output.',
      foundation=('Civilian Combine','A modern civilian combine will gather workshops, maintenance and technical services around a common industrial site. Its value will depend on products that customers can use rather than the prestige of the new buildings.',B('industrial_complex')),
      school=('Industrial Engineering','Industrial engineers will study production methods, machine tools and the organisation of large workshops. Better technical practice can raise productivity without requiring every enterprise to begin again with entirely new machinery.',R('CAT_industry',50,2)),
      base=M(eff=6,energy=3),
      left=('Capital Goods','Investment will favour machinery and the means of constructing further industry. This approach promises a larger future capacity, although households must wait longer for the goods that make development visible in daily life.',M(civbuild=20,build=6,energy=5,st=-3),None),
      right=('Consumer Manufacturing','Household goods and civilian orders will take priority over another expansion of capital equipment. Better supply can release resources for wider economic use, while margins and public revenues remain under pressure.',M(eff=15,cg=-8,tax=-3),None),
      left_follow=('Machine Suppliers','Specialised suppliers will support larger industrial projects with tools, components and maintenance. Their growth gives the republic a wider engineering base, accompanied by a greater demand for skilled workers and power.',M(eff=6,energy=3),{}),
      right_follow=('Commercial Distribution','A dependable commercial network will bring manufactured goods to customers beyond the factory gates. It improves the value of civilian production while adding a public responsibility for standards, transport and honest accounts.',M(eff=5,corp=3,admin=3),{}),
      join=('Republican Order Book','A coherent civilian order book will connect workshops with the wider Union market. The republic will gain from dependable demand, while its prosperity becomes more sensitive to the continuity of those commercial relationships.',M(eff=5,energy=2)),
      final=M(civbuild=8),weekly=.00006),
    dict(key='resources',name='Resources and Processing',programme='Union Resource Programme',legacy='Independent Resource Complex',kind='industry',
      intro='The republic\'s mineral and energy resources can support much more than the shipment of raw material. Surveying, processing and transport investment will strengthen its place in Union supply, while confronting the energy and environmental costs of a resource-led economy.',
      foundation=('Industrial Corridors','Resource production needs roads, freight facilities and dependable power before another deposit becomes useful to industry. A stronger transport corridor will serve existing works and open room for the processing economy around them.',B('infrastructure')),
      school=('Geological Service','A professional geological and industrial service will improve knowledge of existing resources and the requirements of their development. Better information must be followed by investment before a surveyed deposit can contribute to production.',R('CAT_industry',50,2)),
      base=M(oil=8,light=8,techmetals=8,steel=8,precious=8,energy=4),
      left=('Extraction Priority','Investment will favour greater output from resources that the republic can already exploit. Higher extraction will strengthen the Union\'s supply, while exposing land, water and the power system to a heavier industrial burden.',M(oil=20,light=20,techmetals=20,steel=20,precious=20,energy=8,agri=-4),None),
      right=('Processing Priority','Processing and industrial services will capture more value from domestic and imported materials. This wider industrial role is less dependent on the size of local deposits, but requires substantial power and technical capacity.',M(eff=18,power=10,energy=10),None),
      left_follow=('Mining Machinery','Dependable machinery and maintenance will make existing extraction less vulnerable to breakdowns. The additional output remains useful only if freight, processing and customers can keep pace.',M(oil=7,light=7,techmetals=7,steel=7,precious=7,energy=2),{}),
      right_follow=('Materials Laboratories','Testing laboratories will help processors meet the standards demanded by engineering customers. Their expertise can strengthen a wider manufacturing economy, while adding another permanent technical institution to public expenditure.',M(research=4,eff=4,admin=3),{}),
      join=('Resource Supply Office','A dedicated supply office will coordinate transport, processing and industrial customers. Its task is to keep the value of resource development from disappearing in bottlenecks between the mine and the final purchaser.',M(eff=4,admin=3)),
      final=M(power=5),weekly=.00006),
    dict(key='electronics',name='Electronics and Research',programme='Union Electronics Programme',legacy='Independent Electronics Complex',kind='research',
      intro='Communications, computing and precision electronics connect scientific institutions with civilian industry and defence. Common radio and component orders will lower the production cost of command-and-control equipment, while the programme relies on a wide network of suppliers, testing facilities and research contracts.',
      foundation=('Electronic Workshops','Precision assembly and engineering workshops will give scientific institutes a dependable industrial partner. The new facilities must develop practical production skills rather than relying on a succession of promising prototypes.',B('industrial_complex')),
      school=('Computing Institutes','Computing and communications institutes will train engineers able to connect theory with the needs of factories and public institutions. Their work will depend on access to components, common standards and sustained research funding.',R('CAT_electronics',50,2)),
      base=M(research=5,eff=5,energy=3),
      left=('Defence Electronics','Research will concentrate on military communications and command systems. Dedicated radio production and testing will lower the cost and improve the reliability of command-and-control equipment. Scientific prestige and a secure customer come with dependence on official procurement.',M(research=10,cap=8,energy=5),gear('cnc_equipment_type',build_cost_ic=-.10,reliability=.05)),
      right=('Civilian Electronics','Communications equipment and practical computing will take priority over specialised military work. A broader civilian market can strengthen commercial productivity, although competitive prices and rapid product changes will challenge established workshops.',M(eff=15,corp=4,cap=-3),None),
      left_follow=('Testing Laboratories','Permanent testing facilities will connect military customers, researchers and manufacturers. Their common standards can reduce failures and improve technical reliability, at the price of a more expensive scientific establishment.',M(research=4,admin=3),{}),
      right_follow=('Technical Applications','Engineers will bring communications and computing into enterprise administration and production. The gains will depend on practical instruction and maintenance rather than the announcement of another experimental machine.',M(eff=5,research=3,social=3),{}),
      join=('Research Contracts','Long research contracts will give institutes and manufacturers time to turn specialised knowledge into dependable products. The same contracts will make them vulnerable if Union priorities, common standards or guaranteed customers disappear.',M(research=3,admin=2)),
      final=M(eff=4),weekly=.00010),
    ]
    roots=[]
    for index,s in enumerate(records):
        key=s['key'];base='special_'+key+'_';roots.append(base+'mandate')
        g=c.G('spec_'+key,s['name'],6+index*10,14,'ssr')
        g.update(specialisation=key,programme=s['programme'])
        anchor=HISTORICAL[key].get(profile['tag'])
        premise='Universally selectable Union investment programme'
        intro=s['intro']
        def f(suffix,title,desc,x,y,parents=(),**kw):
            return c.F(g,base+suffix,title,desc+' Historical precedent: '+HISTORY_TEXT[key],x,y,[tuple(base+v for v in p) if not isinstance(p,str) else base+p for p in parents],
                       kind=s['kind'],ownership='Union specialisation',specialisation=key,
                       historical_basis=premise,historical_anchor=anchor,legacy_spirit=s['legacy'],**kw)
        f('mandate',s['name'],intro,0,0,mod=s['base'],gdp_cost=.003,weekly_gdp_cost=s['weekly'],choice_set='union_specialisation',equipment_bonuses=BASE_COSTS.get(key,[]))
        title,desc,building=s['foundation'];f('works',title,desc,0,1,['mandate'],gdp_cost=.015 if building['type'] in {'arms_factory','industrial_complex','dockyard'} else .009,building=building,cost=10)
        title,desc,research=s['school'];f('schools',title,desc,0,2,['works'],gdp_cost=.002,research=research)
        for side,x in [('left',-3),('right',3)]:
            title,desc,mods,equipment=s[side]
            f(side,title,desc,x,3,['schools'],mod=mods,gdp_cost=.002,equipment_bonuses=(equipment if isinstance(equipment,list) else [equipment]) if equipment else [])
            title,desc,mods,extra=s[side+'_follow']
            f(side+'_follow',title,desc,x,4,[side],mod=mods,gdp_cost=.0015,**extra)
        c.X(base+'left',base+'right')
        title,desc,mods=s['join'];f('office',title,desc,0,5,[['left_follow','right_follow']],mod=mods,gdp_cost=.001)
        f('priority','Priority Allocations','Priority allocations will protect the specialised programme when materials and technical staff are scarce. Other enterprises and public institutions will have to accept a smaller share of the republic\'s attention and investment.',-3,6,['office'],mod=M(research=3,pp=5,social=4),gdp_cost=.001)
        f('efficiency','Lean Administration','A smaller coordinating service will give workshops and professional institutions more room to solve their own problems. Lower administrative costs come at the price of less direct political control over the specialised programme.',3,6,['office'],mod=M(admin=-8,pp=-5,eff=3),gdp_cost=.0015)
        c.X(base+'priority',base+'efficiency')
        f('settlement','Union Production Role','The republic has secured a distinctive role in the Union economy. Its specialised institutions now possess skills and capacity that would be difficult to assemble in isolation, together with a lasting dependence on the customers, suppliers and common standards that made their growth possible.',0,7,[['priority','efficiency']],mod=s['final'],gdp_cost=.001)
        for n in c.NODES:
            if n.get('specialisation')!=key:continue
            if key=='navy':n['geography']='naval_coast';n['sea_context']=SEA.get(profile['tag'],'Landlocked')
            if key=='resources' and n['key'] in {base+'left',base+'left_follow'}:n['needs_existing_resources']=True
    for i,a in enumerate(roots):
        for b in roots[i+1:]:c.X(a,b)

def is_benefit(key,value):
    bad=any(word in key for word in ('cost','consumption','training_time','energy_use','consumer_goods'))
    return value<0 if bad else value>0

def legacy(mods):return {k:round(v*(.20 if is_benefit(k,v) else .75),5) for k,v in mods.items()}
