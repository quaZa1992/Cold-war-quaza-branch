# IMPERIA COLD WAR — researched SSR specialisation and sovereign aftermath revision.
"""Compose revision two without touching loaded game directories."""
import content as c
import lore,market,politics,specialisations

CONTRACT_PRICES={
 'clearing':(.002,.001,.00003,.00002),'technical':(.004,.0015,.00005,.00003),
 'border':(.001,.001,.00002,.00002),'training':(.003,.0015,.00005,.00003),
 'energy':(.003,.0025,.00004,.00003),'water':(.002,.002,.00003,.00003),
 'romanian':(.001,.001,.00002,.00002),
}

def apply(profile):
    c.NODES[:]=[n for n in c.NODES if n['phase']!='party']
    c.GROUPS[:]=[g for g in c.GROUPS if g['phase']!='party']
    lore.apply_common(c,profile)
    orders=next(n for n in c.NODES if n['key']=='deepen_specialisation')
    orders.update(title='Union Supply Contracts',modifiers=c.M(eff=6,tax=3,energy=3))
    market.revise(c)
    for n in c.NODES:
        if n['phase']=='independent':n['y']+=12
    for g in c.GROUPS:
        if g['phase']=='independent':g['y']+=12
    politics.add(profile)
    specialisations.add(profile)
    for n in c.NODES:
        if n.get('specialisation'):
            n['legacy_modifiers']=specialisations.legacy(n['modifiers'])
            n['legacy_weekly_gdp_cost']=round(n.get('weekly_gdp_cost',0)*.5,5)
            n['legacy_equipment_bonuses']=[dict(target=e['target'],modifiers=specialisations.legacy(e['modifiers'])) for e in n.get('equipment_bonuses',[])]
            n['legacy_retention']=.20
        if n.get('public_charter') or n.get('market_charter'):
            n['decision']='Enterprise restructuring'
    for key,(a,b,wa,wb) in CONTRACT_PRICES.items():
        for role,cost,weekly in [('origin',a,wa),('recipient',b,wb)]:
            side=c.CONTRACTS[key][role]
            side.pop('cash',None);side.pop('weekly',None)
            side['gdp_cost']=cost;side['weekly_gdp_cost']=weekly
    profile['regional']['description']='The republic\'s established economy rests on '+profile['context'].lower()+'. These strengths bring inherited costs in transport, public administration and the inputs needed to keep production operating reliably.'
    profile['sea_context']=specialisations.SEA.get(profile['tag'],'Landlocked')
    profile['specialisation_anchors']={key:anchors.get(profile['tag']) for key,anchors in specialisations.HISTORICAL.items()}
