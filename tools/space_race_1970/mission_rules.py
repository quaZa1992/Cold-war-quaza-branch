# IMPERIA CW — Cold War: successful precursor flights required before major departures.
# Each tuple is one required qualification; entries within it are alternatives.
# Development may proceed in parallel. Failure and partial results never qualify.
STATION = ('salyut','skylab','almaz','apollo-applications')
MOON = ('lunar-expedition','n1-l3-recovery')
REQUIREMENTS = {
    'crewed-capsule': [('recoverable-satellite',)],
    'heavy-lift': [('upper-stage',),('propulsion-qualification',)],
    'docking-tests': [('crewed-capsule',)],
    'life-support': [('crewed-capsule',)],
    'automated-docking': [('docking-tests',)],
    'cargo-ferry': [('automated-docking',)],
    'salyut': [('crewed-capsule',),('docking-tests',),('life-support',)],
    'skylab': [('crewed-capsule',),('docking-tests',),('life-support',),('heavy-lift',)],
    'almaz': [('crewed-capsule',),('docking-tests',),('life-support',)],
    'apollo-applications': [('crewed-capsule',),('docking-tests',),('life-support',),('heavy-lift',)],
    'modular-station': [STATION,('automated-docking',),('cargo-ferry',),('life-support',)],
    'reusable-shuttle': [('crewed-capsule',),('docking-tests',),('propulsion-qualification',)],
    'energia-buran': [('crewed-capsule',),('automated-docking',),('propulsion-qualification',)],
    'orbital-tug': [('upper-stage',),('docking-tests',)],
    'orbital-depot': [('cryogenic-storage',),('automated-docking',),('cargo-ferry',)],
    'space-telescope': [('solar-observatory','ariel-science','isis-science','ans-astronomy')],
    'lunar-rover': [('lunar-orbiter',)],
    'lunar-sample-return': [('lunar-orbiter',)],
    'circumlunar-flight': [('crewed-capsule',),('upper-stage',),('life-support',)],
    'lunar-expedition': [('lunar-orbiter',),('circumlunar-flight',),('docking-tests',),('heavy-lift',)],
    'n1-l3-recovery': [('lunar-orbiter',),('circumlunar-flight',),('docking-tests',),('propulsion-qualification',)],
    'lunar-orbit-station': [('circumlunar-flight',),STATION,('cargo-ferry',),('life-support',)],
    'lunar-outpost': [MOON,('cargo-ferry',),('life-support',)],
    'se-l2-observatory': [('space-telescope',),('cryogenic-storage',)],
    'venus-entry': [('interplanetary-probe-bus',)],
    'venus-orbiter': [('interplanetary-probe-bus',)],
    'mars-orbiter': [('interplanetary-probe-bus',)],
    'mars-lander': [('mars-orbiter',),('interplanetary-probe-bus',)],
    'jupiter-flyby': [('interplanetary-probe-bus',)],
    'grand-tour': [('jupiter-flyby',)],
    'mercury-flyby': [('interplanetary-probe-bus',)],
    'vega': [('venus-entry',),('interplanetary-probe-bus',)],
    'apollo-soyuz': [('crewed-capsule',),('docking-tests',)],
    'interkosmos-cosmonaut': [('interkosmos-instruments',)],
    'mars-rover': [('mars-orbiter',),('mars-lander',)],
    'mars-sample-return': [('mars-orbiter',),('mars-lander',),('lunar-sample-return',)],
    'deep-space-habitat': [('modular-station',),('life-support',),('circumlunar-flight',)],
    'mars-heavy-edl': [('mars-lander',),('heavy-lift',),('propulsion-qualification',)],
    'mars-crewed-landing': [('mars-heavy-edl',),('deep-space-habitat',),('mars-sample-return',),MOON],
}

# Established flight families count as qualifications, without granting programme
# completions, deployed hardware, campaign prestige or research awards.
# Sources: https://www.nasa.gov/missions/apollo/apollo-8-mission-details/
# https://www.nasa.gov/mission/lunar-orbiter-1/
# https://ntrs.nasa.gov/api/citations/19950016829/downloads/19950016829.pdf
HERITAGE = {
    'USA': ('crewed-capsule','docking-tests','upper-stage','heavy-lift','lunar-orbiter','circumlunar-flight','lunar-expedition','interplanetary-probe-bus'),
    'SOV': ('crewed-capsule','docking-tests','upper-stage','lunar-orbiter','interplanetary-probe-bus'),
}


def qualified(group,ids):
    return 'OR = { '+' '.join(f'has_country_flag = cw_sr_p{ids[item]}_awarded has_country_flag = cw_sr_heritage_{ids[item]}' for item in group)+' }'


def launch_gates(programme_id,ids):
    return ' '.join(qualified(group,ids) for group in REQUIREMENTS.get(programme_id,[]))
