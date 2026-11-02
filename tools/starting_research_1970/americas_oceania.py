# IMPERIA COLD WAR — January 1970 Americas and Oceania research evidence.
"""Curated, conservative regional inputs. These are capability estimates, not inventories."""
import copy
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCES = {
    'us_air': 'https://www.nationalmuseum.af.mil/Visit/Museum-Exhibits/Fact-Sheets/Display/Article/2929390/mcdonnell-douglas-f-4c-phantom-ii/',
    'us_navy': 'https://www.history.navy.mil/content/history/nhhc/browse-by-topic/ships/submarines/george-washington-ssbn-598.html',
    'us_helo': 'https://history.army.mil/portals/143/Images/Publications/catalog/90-4.pdf',
    'us_nuclear': 'https://inl.gov/20-questions/',
    'us_navigation': 'https://www.darpa.mil/about/innovation-timeline/transit-satellite-space-based-navigation',
    'robots': 'https://www.computerhistory.org/timeline/ai-robotics/',
    'can_nuclear': 'https://www.aecl.ca/radioactive-waste/project-sites/douglas-point/',
    'can_reactors': 'https://publications.gc.ca/Collection-R/LoPBdP/BP/bp365-e.htm',
    'ast_air': 'https://www.airforce.gov.au/about-us/history/our-journey/first-flight-mirage',
    'ast_cutoff': 'https://www.airforce.gov.au/community/visit-and-learn/heritage-centres/raaf-base-wagga-heritage-centre/display-aircraft',
    'ast_sub': 'https://seapower.navy.gov.au/history/units/hmas-ovens',
    'ast_nuclear': 'https://www.arpansa.gov.au/regulation-and-licensing/regulation/about-regulatory-services/who-we-regulate/major-facilities/hifar',
    'nzl_air': 'https://nzhistory.govt.nz/war/rnzaf/timeline',
    'nzl_cutoff': 'https://airforcemuseum.co.nz/blog/50-years-on-rnzaf-skyhawk-purchase-and-arrival/',
    'arg_nuclear': 'https://www.argentina.gob.ar/cnea/Tecnologia-nuclear/reactores-de-investigacion/ra-1',
    'arg_air': 'https://www.argentina.gob.ar/node/229873',
    'bra_air': 'https://www.fab.mil.br/notimp/mostra/14072018',
    'bra_nuclear': 'https://www.gov.br/ien/pt-br/instalacoes/reator-nuclear-de-pesquisa-argonauta/historico-do-reator-argonauta',
    'mex_nuclear': 'https://www.inin.gob.mx/mini_sitios/segundo_plano.cfm?codigo_opc=400008000&cve_area=RN',
    'crops': 'https://www.nobelprize.org/prizes/peace/1970/borlaug/lecture/',
    'pru_air': 'https://elperuano.pe/noticia/68125-el-vuelo-del-mirage-5',
    'chl_air': 'https://fach.mil.cl/fach/documentos/biblioteca-del-aviador/tercer.pdf',
    'chl_industry': 'https://www.cia.gov/readingroom/docs/CIA-RDP85T00875R001600020055-9.pdf',
    'bol_air': 'https://fab.bo/wp-content/uploads/2024/08/2023-OCT-LIBRO-DEL-CENTENARIO-FAB_compressed.pdf',
    'col_computing': 'https://www.banrepcultural.org/del-fichero-al-ciberespacio/cronologia.htm',
    'cuba': 'https://www.cia.gov/readingroom/docs/CIA-RDP65B00383R000200260009-5.pdf',
    'caribbean': 'https://www.loc.gov/item/88600483/',
    'caribbean_industry': 'https://www.elibrary.imf.org/view/journals/022/0010/002/article-A004-en.xml',
    'pacific': 'https://www.un.org/en/global-issues/decolonization/',
    'fiji_industry': 'https://www.unido.org/publications/ot/9648451/pdf',
    'can_air': 'https://www.canada.ca/en/air-force/services/aircraft/canadair-starfighter.html',
    'ast_navy': 'https://www.navy.gov.au/about-navy/history/history-milestones/charles-f-adams-perth-class-destroyers-ikara-missile-system',
    'col_nuclear': 'https://www2.sgc.gov.co/Noticias/Paginas/Por-que-el-reactor-nuclear-colombiano-no-genera-energia.aspx',
    'ven_nuclear': 'https://www-pub.iaea.org/MTCD/publications/PDF/TE-1748_web.pdf',
}
DOMAINS = ('construction machinery grid computing infantry support communications vehicles camouflage special_forces night_vision body_armor anti_tank anti_air artillery armor jet_light jet_medium aircraft_modules helicopter naval_surface naval_submarine').split()


def template(values):
    return dict(zip(DOMAINS, values))


TEMPLATES = {
    'frontier': template([1960,1961,1965,1965,1965,1965,1960,1965,1950,1965,1965,1960,1965,1965,1965,1965,1960,1960,1965,1965,1965,1965]),
    'industrial': template([1960,1955,1965,1955,1965,1965,1960,1965,1950,1965,1950,1945,1965,1950,1965,1965,1960,1955,1955,1965,1965,1959]),
    'regional': template([1960,1950,1955,1945,1955,1955,1960,1960,1950,1950,0,1945,1950,1950,1955,1943,1950,0,1955,1955,1955,1945]),
    'limited': template([1950,1950,1955,0,1950,1955,1950,1950,1940,1940,0,0,1950,1940,1940,1940,1940,0,0,0,1945,0]),
    'island': template([1940,1940,0,0,1940,1940,1940,1940,0,0,0,0,1940,0,0,0,0,0,0,0,0,0]),
    'police': template([1950,1940,1955,0,1940,0,1940,1940,0,0,0,0,0,0,0,0,0,0,0,0,0,0]),
    'disabled': dict.fromkeys(DOMAINS, 0),
}
COUNTRIES = {}
FILES = {p.stem[:3]: p for p in (ROOT/'history/countries').glob('*.txt')}


def add(tag, base, rationale, source_ids=(), changes=None, extras=(), exclusions=(), status='independent', confidence='medium'):
    domains = copy.deepcopy(TEMPLATES[base])
    domains.update(changes or {})
    COUNTRIES[tag] = {
        'name': FILES[tag].stem[6:], 'status_1970': status, 'confidence': confidence,
        'domains': domains, 'add_techs': list(extras), 'remove_techs': [],
        'rationale': rationale,
        'sources': [SOURCES[key] for key in source_ids],
        'exclusions': list(exclusions),
    }


def build():
    add('USA','frontier','Mature mass-production, semiconductor, mainframe, aerospace and nuclear industries. Operational F-4, F-111, B-52, AH-1G, strategic missiles and nuclear submarines predate the cutoff. Operational equipment does not imply every 1970 prototype or every future module.',
        ('us_air','us_navy','us_helo','us_nuclear','us_navigation','robots'), extras=(
        'mdcw_rpv_1964','mdcw_marksman_rifles_1963','mdcw_underbarrel_grenade_launcher_1969','mdcw_unconventional_warfare_1952','mdcw_secure_voice_1968','mdcw_combat_engineer_vehicles_1968','combat_eng_equipment','mdcw_nylon_armour_vests_1952','mdcw_helicopter_medevac_1962',
        'mdcw_early_aam_1957','mdcw_delta_wing_1956','mdcw_fire_control_1963','mdcw_engines_1964','mdcw_cooled_ir_1965','air_weapons_1','countermeasures_1','ag_weapons_1','naval_weapons_1','gen_3_large','variable_wing_design','strategic_bomber1','transport_plane1','naval_plane1','nsb_attack_helicopter_tech_1','nsb_engine_tech_1','nsb_rocket_pods_tech_1','nsb_gun_pods_tech_1','nsb_light_nose_gun_tech_1',
        'mdcw_carrier_hull_1955','carrier_hull_1','destroyer_hull_1','cruiser_hull_1','battleship_hull_1','missile_submarine_hull_1','tech_nuclear_power_systems_1','tech_power_systems_1','tech_combat_support_systems','tech_fire_control_1','tech_naval_weapon_systems','mdcw_naval_sam_1955','tech_landing_craft_1',
        'ballistic_missile','ICBM','ICBM1','IRBM','IRBM1','air_defense','SAM','SAM0','cruise_missile','GLCM','GLCM1','TEL_launched_missiles','TEL_3','OLV1','COMSAT1','SPYSAT1','GNSS1',
        'nuclear_technology','mdcw_experimental_power_reactors_1954','mdcw_reactor_fuel_fabrication_1953','mdcw_reactor_licensing_1957','reactor2',
        'mdcw_intermodal_containers_1968','mdcw_high_yield_crops_1968','mdcw_electric_arc_minimills_1969','mdcw_pan_carbon_fibers_1961','mdcw_computer_aided_drafting_1963','mdcw_genetic_code_1966','mdcw_supercritical_steam_1957','mdcw_large_hydro_turbines_1965','mdcw_combined_cycle_generation_1967','mdcw_mechanized_track_renewal_1967','encryption_1','decryption_1','radar'),
        exclusions=('No all-1970 package, flying-wing combat airframe, later pulse-Doppler step, laser-guided weapons1972 or postwar IFV type merely because a prototype existed.','No special project completion, warheads, satellites, equipment or deployed formations are created.'))
    add('CAN','industrial','Domestic aerospace, electronics and civil nuclear engineering coexist with licensed Canadian-built CF-104/J79, imported CF-101 and British diesel submarines. NPD1962 and DouglasPoint1966/68 demonstrate actual heavy-water engineering; MD has no accurately dated pre1970 CANDU power node, so do not substitute Magnox or PWR.',('can_nuclear','can_reactors','can_air'), changes={'computing':1965,'jet_light':1955}, extras=('nuclear_technology','mdcw_experimental_power_reactors_1954','mdcw_reactor_fuel_fabrication_1953','mdcw_reactor_licensing_1957','destroyer_hull_1','mdcw_large_hydro_turbines_1965','mdcw_intermodal_containers_1968','mdcw_early_aam_1957','mdcw_fire_control_1963','radar','transport_plane1','naval_plane1'), exclusions=('No sovereign nuclear weapons, ICBMs, nuclear submarine design, orbital launcher or later CF-18.','CANDU power representation is limited by the existing tree; no forced 1971 mutually exclusive policy choice.'))
    add('AST','industrial','Licensed MirageIIIO assembly and established shipyards; HIFAR1958 is research-only. Perth guided-missile destroyers and Oberon-class diesel submarines precede1970. F-111 and leasedF-4 deliveries are later than the cutoff.',('ast_air','ast_cutoff','ast_sub','ast_nuclear'),changes={'computing':1945,'jet_medium':1950},extras=('nuclear_technology','destroyer_hull_1','mdcw_naval_sam_1955','mdcw_carrier_hull_1955','mdcw_early_aam_1957','mdcw_delta_wing_1956','radar','transport_plane1','naval_plane1','mdcw_helicopter_medevac_1962'),exclusions=('No F-111, F-4, nuclear power station, indigenous strategic missile or nuclear submarine.','Mirage operation does not grant indigenous semiconductor or jet-engine research.'))
    add('NZL','regional','Established engineering, hydroelectricity and maintenance of imported Vampire/Canberra aircraft, Hercules, Orion and Iroquois. Skyhawks were handed over and shipped only during1970.',('nzl_air','nzl_cutoff'),changes={'machinery':1950,'grid':1965,'computing':1945,'infantry':1965,'support':1965,'special_forces':1965,'vehicles':1960,'helicopter':1965,'naval_surface':1965,'naval_submarine':0},extras=('mdcw_large_hydro_turbines_1965','transport_plane1','naval_plane1','radar'),exclusions=('No January1970 Skyhawk, supersonic fighter, nuclear programme or submarine industry.',))
    add('ARG','regional','Industrial and university base with domestic small arms, vehicles and limited aircraft development; RA-1 locally constructed1958. PulquiII never entered series service, Pucara was a1969 prototype. Operational combat aviation remains imported/subsonic.',('arg_nuclear','arg_air'),changes={'machinery':1955,'grid':1965,'computing':1945,'jet_medium':1950},extras=('nuclear_technology','mdcw_reactor_fuel_fabrication_1953','mdcw_battle_rifles_1954','combat_eng_equipment','mdcw_carrier_hull_1955','mdcw_destroyer_hull_1955'),exclusions=('No MirageIII1972, Pucara series-production1975, TAM tank or Atucha commercial power1974.','No automatic PWR/Magnox from a research reactor.'))
    add('BRA','regional','Substantial industrial and engineering base, licensed small arms and motor vehicles, Meteor-era jets and embryonic Embraer1969. Research reactors operated by1957/1965; nuclear power and modern supersonic combat aviation came later.',('bra_air','bra_nuclear'),changes={'machinery':1955,'grid':1965,'computing':1945},extras=('nuclear_technology','mdcw_battle_rifles_1954','mdcw_carrier_hull_1955','mdcw_destroyer_hull_1955','mdcw_large_hydro_turbines_1965'),exclusions=('No MirageIII1972, F-5delivery1975, EMB110service1973, Angra power or nuclear submarine.','No universal agricultural high-yield research from founding EMBRAPA1973.'))
    add('MEX','regional','Import-substitution industry and military workshops; imported T-33-era aviation. TRIGA reactor acceptedNov/Dec1968. The Mexican wheat programme demonstrates established high-yield agricultural knowledge before1968.',('mex_nuclear','crops'),changes={'special_forces':1940,'naval_submarine':0,'armor':1940},extras=('nuclear_technology','mdcw_high_yield_crops_1968'),exclusions=('No F-5, power reactor, nuclear fuel fabrication, domestic jet design or modern MBT production.',))
    add('CUB','regional','Soviet-supported operating and maintenance capacity includes MiG21, Soviet medium tanks and SAMs. Plantation and processing industries do not imply Soviet industrial, semiconductor or strategic research capabilities.',('cuba',),changes={'construction':1954,'machinery':1950,'computing':0,'infantry':1965,'support':1965,'anti_tank':1965,'anti_air':1950,'armor':1955,'jet_light':1960,'jet_medium':1950,'aircraft_modules':1955,'naval_surface':1945,'naval_submarine':0},extras=('mdcw_assault_rifles_1943','mdcw_early_aam_1957','air_defense','SAM','SAM0','radar'),exclusions=('No Cuban ownership of Soviet strategic missiles or nuclear weapons after their1962 withdrawal.','No indigenous supersonic design/engine, submarine industry or nuclear power.'))
    add('PRU','limited','Mirage5P arrivedJune1968 and flew locallyJuly1968, justifying imported supersonic operating knowledge. Civil industry and field forces remain uneven and predominantly supplied from abroad.',('pru_air',),changes={'construction':1954,'computing':1945,'infantry':1955,'support':1955,'armor':1943,'jet_light':1960,'aircraft_modules':1955,'helicopter':1955,'naval_surface':1955,'naval_submarine':1945},extras=('mdcw_delta_wing_1956','mdcw_destroyer_hull_1955'),exclusions=('No later Soviet tank/fighter imports, domestic Mirage development or reactor1988.',))
    add('CHL','regional','Copper-linked processing, public engineering and imported military equipment. Operational Hunter fleet1967/68 is early-jet knowledge; a supersonic dive is not a sustained supersonic fighter design. The first research reactor followed1974.',('chl_air','chl_industry'),changes={'computing':1945,'armor':1943,'naval_submarine':1945},extras=('mdcw_destroyer_hull_1955',),exclusions=('No Mirage/F-5, indigenous supersound design, reactor1974 or PWR power plant.',))
    add('COL','limited','Industry and financial mainframe use existed, including imported IBM650 in1957 and banking data processing1969. Imported computing supports only basic use, not an indigenous integrated-circuit industry.',('col_computing',),changes={'construction':1954,'computing':1945,'infantry':1955,'artillery':1955,'jet_light':1950,'aircraft_modules':1950,'helicopter':1955,'naval_surface':1955},exclusions=('No modern supersonic fighter, semiconductor industry, MBT production or civil power reactor.',))
    add('BOL','limited','Conservative land and piston-aircraft maintenance baseline. The Bolivian air force records first T-33 arrivals on7Aug1973, so an early-jet starting grant would be premature.',('bol_air',),changes={'naval_surface':0,'armor':0},exclusions=('No T-33/F-86, nuclear reactor, modern tank production or modern naval shipbuilding.',))
    for tag,notes,changes in [
        ('VEN','Oil industry and service workshops support modern construction, but US-supplied F-86-era jets do not establish a domestic aerospace sector. Mirage deliveries and advanced naval programmes belong later.',{'construction':1960,'grid':1965,'computing':1945,'infantry':1955,'jet_light':1950,'aircraft_modules':1950,'helicopter':1955,'naval_surface':1955,'naval_submarine':1945}),
        ('ECU','Uneven civil economy and imported piston/early-jet forces. Later Jaguar/Mirage and more advanced armour are excluded.',{'jet_light':1950,'aircraft_modules':1950,'helicopter':1955,'naval_surface':1955,'armor':1940}),
        ('URG','Established civic and engineering institutions, with imported F-80/T-33-era aviation and older US/British equipment; not an indigenous supersonic sector.',{'construction':1954,'computing':1945,'infantry':1955,'jet_light':1950,'aircraft_modules':1950,'naval_surface':1955,'armor':1943}),
        ('PAR','Agrarian and riverine economy; older small arms, piston aircraft and imported light armour are the safe baseline. No evidence here for a January1970 jet fleet.',{'naval_surface':1945,'armor':1940}),
        ('GUA','Imported small arms and basic aviation with limited industrial depth. Advanced domestic programmes are unsupported.',{'jet_light':1950,'aircraft_modules':1950}),
        ('HON','1969 war experience still relied heavily on piston aircraft and old ground equipment. No automatic postwar jet modernization.',{'jet_light':1940,'armor':1940}),
        ('ELS','1969 war forces rely on piston aviation and old imported infantry equipment; civil processing does not establish advanced industry.',{'jet_light':1940,'armor':0}),
        ('NIC','Small US-supported guard and imported older aircraft. Modern arms and aerospace manufacturing are unsupported.',{'jet_light':1940,'armor':1940}),
        ('PAN','Canal service infrastructure and policing do not establish independent US research or a strategic armed force.',{'construction':1954,'naval_surface':1945,'artillery':0,'armor':0,'jet_light':0,'special_forces':0}),
        ('DOM','Imported older military hardware and an import-dependent industrial base; cap advanced branches conservatively.',{'jet_light':1950,'aircraft_modules':1950,'naval_surface':1955,'armor':1940}),
        ('HAI','Severely constrained industrial base and imported older security equipment; no unsupported heavy, nuclear or aerospace branch.',{'construction':1940,'machinery':1940,'grid':0,'infantry':1940,'support':1940,'artillery':0,'armor':0,'jet_light':1940,'naval_surface':1945}),
        ('GUY','Bauxite and agricultural processing support limited engineering; the small defence force does not inherit British heavy industries.',{'construction':1950,'machinery':1940,'grid':0,'artillery':0,'armor':0,'jet_light':0,'naval_surface':1945}),
    ]:
        add(tag,'limited',notes,('caribbean','caribbean_industry'),changes=changes,confidence='low',exclusions=('Conservative capability inference; the cited regional surveys do not prove every individual technology.','No strategic nuclear, missile, semiconductor or modern aircraft-design package.'))
    add('COS','police','Army abolished1948; civilian institutions and police require no tank, artillery, combat-jet or special-forces package.',('caribbean',),exclusions=('No standing-army heavy research inferred from US regional presence.',))
    for tag,note in [
        ('JAM','Independent since1962; bauxite/alumina processing is a specific industrial enclave, not a full heavy-arms economy.'),
        ('TRI','Independent since1962; petroleum and refining support service engineering, not automatic domestic weapons development.'),
        ('BAR','Independent since1966; early assembly industries do not imply a semiconductor fabrication industry.'),
        ('BAH','British colony; tourism, shipping and local policing do not inherit metropolitan research.'),
        ('ANT','British associated state; local construction and constabulary capabilities only.'),
        ('DMI','British associated state; limited local technical institutions.'),
        ('GRA','British associated state; no independent heavy-arms or jet sector.'),
        ('STK','British associated state; local and imported policing equipment only.'),
        ('STL','British associated state; no established January1970 combat aviation industry.'),
        ('STV','British associated state from1969; use the local economy rather than British strategic research.'),
        ('BLZ','British Honduras; limited local engineering and policing.'),
        ('SUR','Autonomous country within the Kingdom of the Netherlands; bauxite industry is not independent Dutch high technology.'),
        ('NLA','Netherlands Antilles; refineries and dock services do not inherit Dutch national military research.'),
        ('PTR','US territory with substantial manufacturing but no separate sovereign strategic research establishment.'),
        ('FGU','French department with a foreign-operated space range; no independent launcher or satellite-design capability.'),
    ]:
        changes={}
        if tag in {'JAM','TRI','BAR','SUR','NLA','PTR'}:changes.update(construction=1950,machinery=1950,grid=1955)
        if tag=='PTR':changes.update(construction=1954,computing=1945)
        add(tag,'island',note,('caribbean','caribbean_industry'),changes=changes,status='independent' if tag in {'JAM','TRI','BAR'} else 'dependent territory or associated state',confidence='low',exclusions=('No inherited metropolitan strategic, nuclear, missile, modern jet or submarine research.',))
    for tag,note in [
        ('FIJ','British colony untilOctober1970; established locally recruited infantry, no advanced independent industries.'),
        ('PAP','Australian-administered territory; local construction and infantry capabilities do not inherit Australian modern research.'),
        ('SAM','Independent WesternSamoa; small civilian economy without a regular heavy military.'),
        ('TON','British protected state untilJune1970; modest royal/infantry force, no heavy industry.'),
        ('NAU','Independent since1968; phosphate extraction is a foreign-dependent enclave, not broad industrial engineering.'),
        ('KIR','British Gilbert and Ellice Islands; local/colonial baseline.'),
        ('TUL','Part of British Gilbert and Ellice Islands, no independent national R&D.'),
        ('SOL','British protectorate; police and civilian works only.'),
        ('VAN','Anglo-French NewHebrides condominium; local technical base only.'),
        ('MIC','US Trust Territory of the Pacific Islands; not a sovereign US research inheritor.'),
        ('MAR','US-administered trust territory; test-range presence does not confer independent nuclear technology.'),
        ('PAU','US-administered trust territory; no autonomous heavy or strategic research establishment.'),
    ]:
        add(tag,'island',note,('pacific','fiji_industry') if tag=='FIJ' else ('pacific',),changes={'special_forces':1940} if tag in {'FIJ','PAP','TON'} else {},status='independent' if tag in {'SAM','NAU'} else 'dependent territory or protected state',confidence='low',exclusions=('Conservative local-capability inference where detailed period research was unavailable.','No automatic Australian/British/American technology inheritance.'))
    # Release countries represent local institutions only. They do not receive a
    # sovereign parent's strategic laboratories, weapons, satellites or complete navy.
    for tag in 'ASK CAL CAS CSA FLA HWI IDH KAN LKT NEN NYK TEX UDT USB VMT WVA'.split():
        changes={'construction':1960,'machinery':1950,'grid':1955,'computing':1945,'armor':1943,'jet_light':1950,'aircraft_modules':1950,'naval_submarine':0}
        if tag in {'CAL','NYK','TEX','NEN'}:changes.update(machinery=1955,grid=1965,computing=1955)
        if tag in {'LKT','IDH','KAN','VMT','WVA'}:changes.update(machinery=1940,computing=0,jet_light=1940,aircraft_modules=0)
        add(tag,'limited','No independent state on1Jan1970. Conservative release profile based on local US infrastructure and maintenance capacity; no automatic national strategic research inheritance.',('us_air',),changes=changes,status='hypothetical release',confidence='low',exclusions=('No independent nuclear, orbital, missile, carrier or supersonic development programme inferred from federal facilities.',))
    for tag in ['QUE']:
        add(tag,'regional','No independent state on1Jan1970. Local industrial and hydroelectric expertise only; Canadian federal nuclear and strategic research is not inherited automatically.',('can_reactors',),changes={'naval_submarine':0,'naval_surface':1945,'computing':1945},status='hypothetical release',confidence='low',extras=('mdcw_large_hydro_turbines_1965',))
    for tag in 'PAT RGD SPL SUL YUC'.split():
        add(tag,'limited','No independent state on1Jan1970. Limited regional civil/maintenance profile; no automatic inheritance of the parent country\'s national R&D.',(),changes={'construction':1950,'machinery':1950,'grid':1955,'jet_light':1940,'naval_submarine':0},status='hypothetical release',confidence='low')
    for tag in 'SLA TAM TRC ZAP'.split():
        add(tag,'island','This modern non-state tag did not exist as a separate January1970 country. Only a conservative old-small-arms/vehicle fallback; no cartel-era or national strategic technologies.',(),status='nonexistent modern non-state tag',confidence='low')
    for tag in 'ALN ADS C01 ZOM'.split():
        add(tag,'disabled','Utility or fictional tag, not a historical nation. No human national research package is invented; existing fantasy-specific undated technology is preserved.',(),status='fictional or utility',confidence='not applicable')
    # Native gen2 already represents F-104/MiG21/MirageIII. Gen3 is not a
    # generic entitlement for every aircraft produced after1960.
    for tag in ('AST','CUB','PRU'):
        COUNTRIES[tag]['domains']['jet_light']=1955
    COUNTRIES['AST']['sources'].append(SOURCES['ast_navy'])
    COUNTRIES['CUB']['add_techs'].remove('SAM0')
    for tag,key,note in [
        ('COL','col_nuclear','IAN-R1 research-reactor operation from1965 supports nuclear science only.'),
        ('VEN','ven_nuclear','RV-1 research reactor first critical12July1960 supports nuclear science only.'),
    ]:
        COUNTRIES[tag]['add_techs'].append('nuclear_technology')
        COUNTRIES[tag]['sources'].append(SOURCES[key])
        COUNTRIES[tag]['rationale']+=' '+note
        COUNTRIES[tag]['exclusions'].append('Research reactor knowledge grants no actual enrichment plant, power reactor or nuclear weapon.')
    for tag in 'IDH KAN LKT UDT VMT WVA'.split():
        COUNTRIES[tag]['domains']['naval_surface']=0
    result={'project':'IMPERIA COLD WAR','region':'Americas and Oceania','cutoff':'1970-01-01','sources':SOURCES,'countries':COUNTRIES}
    (HERE/'americas_oceania_profiles.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    lines=['IMPERIA COLD WAR','', '# Americas and Oceania research sources','', 'Dated claims are sourced below. Low-confidence records are explicitly conservative design inferences, not claims that each technology is proven by the regional survey. Imported equipment is treated as usable/maintainable equipment-family knowledge, not an indigenous modern industrial base.','']
    lines.extend(f'- {key}: {url}' for key,url in SOURCES.items())
    (HERE/'americas_oceania_sources.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Americas/Oceania profiles:',len(COUNTRIES))


if __name__=='__main__':build()
