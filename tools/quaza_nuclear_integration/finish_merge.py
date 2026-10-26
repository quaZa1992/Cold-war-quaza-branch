# IMPERIA CW — Cold War: explicitly resolve and install reviewed nuclear changes.
import difflib,re
from port import ROOT,SOURCE,AUDIT,MARKER,read,write
from adapt import block,blocks,inject,one

def mark(original,merged):
    before=original.splitlines();after=merged.splitlines();inserts=[]
    for tag,i,j,a,b in difflib.SequenceMatcher(None,before,after,autojunk=False).get_opcodes():
        if tag!='equal' and a<b:inserts.append(a)
    for a in reversed(inserts):after.insert(a,after[a][:len(after[a])-len(after[a].lstrip())]+MARKER)
    return '\n'.join(after)+'\n'

def replace_block(s,name,replacement):
    n=block(s,name);return s[:n['start']]+replacement+s[n['end']:]

def before(rel):return read(AUDIT/'before'/rel)

def main():
    for p in (AUDIT/'staged').rglob('*'):
        if p.is_file():write(ROOT/p.relative_to(AUDIT/'staged'),read(p))
    for p in (AUDIT/'conflicts').rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(AUDIT/'conflicts').as_posix()
        if rel.endswith('industry.txt'):continue # removed future technologies remain removed
        if rel.endswith('countrystateview.gfx'):continue # existing 39-frame strip already correct
        s=read(p)
        s=re.sub(r'<<<<<<<[^\n]*\n(.*?)=======\n(.*?)>>>>>>>[^\n]*\n',lambda m:m[2],s,flags=re.S)
        if rel.endswith('99_investment_scripted_effects.txt'):
            q=read(SOURCE/rel);n=block(q,'add_finished_buildings');replacement=q[n['start']:n['end']]
            original=before(rel);n=block(original,'add_finished_buildings');part=original[n['start']:n['end']]
            a=part.index('\t# IMPERIA CW');b=part.index('\n\t# Buildings to Add',a)
            reward=part[a:b]
            replacement=one(replacement,'\t\t# Buildings to Add','\n'+'\n'.join('\t'+l for l in reward.splitlines())+'\n\n\t\t# Buildings to Add')
            s=replace_block(s,'add_finished_buildings',replacement)
        write(ROOT/rel,mark(before(rel),s))

    rel='common/buildings/00_buildings.txt';s=before(rel);q=read(SOURCE/rel)
    n=block(s,'buildings');extra=''
    for name in ['uranium_mine','imp_uranium_reserved_slots']:
        z=block(q,name);extra+='\n\t'+MARKER+'\n\t'+q[z['start']:z['end']]+'\n'
    s=s[:n['close']]+extra+s[n['close']:]
    z=block(s,'enrichment_facility');part=s[z['start']:z['end']]
    part=one(part,'nuclear_reactor_fuel_production = 350','nuclear_reactor_fuel_production = 350\n\t\t\t\t'+MARKER+'\n\t\t\t\tcountry_resource_cost_uranium = 25')
    write(ROOT/rel,replace_block(s,'enrichment_facility',part))

    rel='common/special_projects/projects/nuclear_projects.txt';s=before(rel)
    # Native project IDs and Cold War technology removals stay intact.
    for name,cost in [('sp_nuclear_energy',2),('sp_thorium_nuclear_fuel',1),('sp_nuclear_bomb',4),('sp_nuclear_warhead_program',4)]:
        n=block(s,name);part=s[n['start']:n['end']]
        if 'resource_cost' in part:part=inject(part,'resources',f'\t\t\turanium = {cost}')
        else:part=part[:-1]+f'\n\tresource_cost = {{ resources = {{ uranium = {cost} }} }}\n}}'
        if name in ['sp_nuclear_bomb','sp_nuclear_warhead_program']:
            available=f'''\tavailable = {{
\t\tFROM = {{
\t\t\tcustom_trigger_tooltip = {{
\t\t\t\ttooltip = imp_sp_needs_3_enrichment_facilities_tt
\t\t\t\tOR = {{
\t\t\t\t\tcheck_variable = {{ undamaged_enrichment_facilities > 2 }}
\t\t\t\t\tis_special_project_being_researched = sp:{name}
\t\t\t\t}}
\t\t\t}}
\t\t}}
\t}}'''
            if name=='sp_nuclear_bomb':part=part[:-1]+'\n'+available+'\n}'
            else:
                av=block(part,'available');body=part[av['start']:av['end']]
                body=inject(body,'FROM','\t\t\tcustom_trigger_tooltip = { tooltip = imp_sp_needs_3_enrichment_facilities_tt OR = { check_variable = { undamaged_enrichment_facilities > 2 } is_special_project_being_researched = sp:sp_nuclear_warhead_program } }')
                part=part[:av['start']]+body+part[av['end']:]
            part=inject(part,'ai_will_do','\t\tmodifier = { factor = 0 ROOT = { NOT = { has_country_flag = imp_ai_wants_nukes } } }\n\t\tmodifier = { factor = 20 ROOT = { has_country_flag = imp_ai_wants_nukes } }')
        s=s[:n['start']]+part+s[n['end']:]
    write(ROOT/rel,mark(before(rel),s))

    rel='common/special_projects/projects/naval_projects.txt';s=before(rel)
    for name,cost in [('sp_medium_naval_nuclear_engines',2),('sp_nuclear_torpedoes',1)]:
        n=block(s,name);part=s[n['start']:n['end']]
        if 'resource_cost' in part:part=inject(part,'resources',f'\t\t\turanium = {cost}')
        else:part=part[:-1]+f'\n\tresource_cost = {{ resources = {{ uranium = {cost} }} }}\n}}'
        s=s[:n['start']]+part+s[n['end']:]
    write(ROOT/rel,mark(before(rel),s))
    for rel,name in [('common/units/equipment/MD_ballistic_missiles.txt','nuclear_ballistic_missile_equipment'),('common/units/equipment/MD_nuclear_missiles.txt','nuclear_missile_equipment')]:
        s=before(rel);n=block(s,name);part=s[n['start']:n['end']]
        part=inject(part,'resources','\t\t\turanium = 1')
        s=s[:n['start']]+part+s[n['end']:]
        write(ROOT/rel,mark(before(rel),s))
    print('Reviewed shared-file merges installed.')

if __name__=='__main__':main()
