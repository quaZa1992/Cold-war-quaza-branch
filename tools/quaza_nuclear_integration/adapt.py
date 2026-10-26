# IMPERIA CW — Cold War: Cold War compatibility and manual merge resolutions.
from pathlib import Path
import hashlib
import json
import re
import shutil
from port import ROOT, BASE, SOURCE, AUDIT, MARKER, backup, read, write

TOKEN = re.compile(r'#[^\n]*|"(?:[^"\\]|\\.)*"|[{}]|[^\s{}#"]+')

def blocks(text):
    """Brace blocks with offsets and their immediate children; comments/strings safe."""
    tokens=[m for m in TOKEN.finditer(text) if not m.group().startswith('#')]
    stack=[]; result=[]
    for i,t in enumerate(tokens):
        if t.group()=='{':
            name=tokens[i-2].group() if i>=2 and tokens[i-1].group()=='=' else None
            node={'name':name,'start':tokens[i-2].start() if name else t.start(),'open':t.end(),'children':[]}
            (stack[-1]['children'] if stack else result).append(node); stack.append(node)
        elif t.group()=='}':
            assert stack, 'Unmatched closing brace'
            node=stack.pop(); node['close']=t.start();node['end']=t.end()
    assert not stack,'Unclosed brace'
    return result

def block(text,name):
    def walk(nodes):
        for n in nodes:
            if n['name']==name:yield n
            yield from walk(n['children'])
    found=list(walk(blocks(text)))
    assert len(found)==1,(name,len(found))
    return found[0]

def modify(rel, fn):
    original=read(ROOT/rel); updated=fn(original)
    if original!=updated:
        backup(rel);write(ROOT/rel,updated)

def one(text,old,new):
    assert text.count(old)==1,(old[:100],text.count(old))
    return text.replace(old,new,1)

def inject(text,name,body):
    n=block(text,name)
    return text[:n['open']]+'\n'+body+text[n['open']:]

def main():
    # Two less obvious prerequisites: labour fulfillment and reserve withdrawals.
    for rel,old,new in [
        ('common/dynamic_modifiers/00_money_dynamic_modifiers.txt','\tlocal_resources_chromium_factor = resource_sector_worker_fulfillment_var','\tlocal_resources_chromium_factor = resource_sector_worker_fulfillment_var\n\t'+MARKER+'\n\tlocal_resources_uranium_factor = resource_sector_worker_fulfillment_var'),
        ('common/dynamic_modifiers/00_MD_dynamic_modifiers.txt','\tcountry_resource_chromium = precious_from_storage','\tcountry_resource_chromium = precious_from_storage\n\t'+MARKER+'\n\tcountry_resource_uranium = uranium_from_storage')]:
        modify(rel,lambda s,old=old,new=new:one(s,old,new))

    # Remaining excavation levels have identical neighbouring values. Modify by
    # technology block rather than guessing a matching text occurrence.
    def excavation(s):
        lines=s.splitlines();out=[]
        for i,l in enumerate(lines):
            out.append(l)
            if 'local_resources_chromium_factor' in l and not any('local_resources_uranium_factor' in x for x in lines[i+1:i+5]):
                out.extend(['\t\t'+MARKER,l.replace('chromium','uranium')])
        return '\n'.join(out)+'\n'
    modify('common/technologies/industry.txt',excavation)
    # Earlier 1960s/1970s extraction technologies must treat uranium equally.
    for p in (ROOT/'common/technologies').glob('mdcw_*.txt'):
        if 'local_resources_chromium_factor' in read(p):modify(p.relative_to(ROOT),excavation)

    def nuclear(s):
        for name in ['sp_nuclear_bomb','sp_nuclear_warhead_program']:
            n=block(s,name); part=s[n['start']:n['end']]
            if 'imp_ai_wants_nukes' not in part:
                part=inject(part,'ai_will_do','\t\t'+MARKER+'\n\t\tmodifier = { factor = 0 ROOT = { NOT = { has_country_flag = imp_ai_wants_nukes } } }\n\t\tmodifier = { factor = 20 ROOT = { has_country_flag = imp_ai_wants_nukes } }')
            if name=='sp_nuclear_warhead_program':
                part=one(part,'resources = { tungsten = 80 chromium = 80 }','resources = { tungsten = 80 chromium = 80 uranium = 4 }')
            s=s[:n['start']]+part+s[n['end']:]
        return s
    modify('common/special_projects/projects/nuclear_projects.txt',nuclear)
    def torpedo(s):
        n=block(s,'sp_nuclear_torpedo');part=s[n['start']:n['end']]
        if 'uranium' not in part:
            part=inject(part,'resources','\t\t\t'+MARKER+'\n\t\t\turanium = 1')
        return s[:n['start']]+part+s[n['end']:]
    # Some MD builds use sp_naval_nuclear_torpedo instead.
    naval='common/special_projects/projects/naval_projects.txt'
    if re.search(r'\bsp_nuclear_torpedo\s*=',read(ROOT/naval)):modify(naval,torpedo)
    else:
        def naval_resource(s):
            for n in reversed(blocks(s)):
                if n['name'] and 'nuclear_torpedo' in n['name']:
                    part=s[n['start']:n['end']]
                    if 'uranium' not in part:part=inject(part,'resources','\t\t\t'+MARKER+'\n\t\t\turanium = 1')
                    s=s[:n['start']]+part+s[n['end']:]
            return s
        modify(naval,naval_resource)
    modify('common/units/equipment/MD_nuclear_missiles.txt',lambda s:one(s,'\t\t\tmicrochips = 3','\t\t\tmicrochips = 3\n\t\t\t'+MARKER+'\n\t\t\turanium = 1'))

    # Resolve remaining aircraft/cruise availability edits, retaining existing
    # Cold War human-only conditions. All raid classes receive the same policy.
    for rel in ['common/raids/air_raids.txt','common/raids/cruise_missile_strike.txt']:
        modify(rel,lambda s:s.replace('raid_available_grey_zone = yes','imp_raid_missile_grey_zone = yes').replace('raid_target_eligible = yes','imp_raid_missile_target_eligible = yes'))
    raid_counts={}
    for p in (ROOT/'common/raids').glob('*.txt'):
        if p.name.startswith('_'):continue
        def human_only(s):
            roots=blocks(s)
            if not roots or roots[0]['name']!='raid_types':return s
            edits=[];count=0
            for raid in roots[0]['children']:
                if raid['name'] is None:continue
                count+=1
                for field in ['available','can_launch']:
                    nodes=[n for n in raid['children'] if n['name']==field]
                    if nodes:
                        n=nodes[0]
                        # The guard is first, so AI evaluation short-circuits.
                        edits.append((n['open'],'\n\t\t\t'+MARKER+'\n\t\t\tis_ai = no'))
                    else:edits.append((raid['open'],'\n\t\t'+MARKER+'\n\t\t'+field+' = { is_ai = no }'))
                ai=[n for n in raid['children'] if n['name']=='ai_will_do']
                if ai:edits.append((ai[0]['open'],'\n\t\t\t'+MARKER+'\n\t\t\tfactor = 0'))
            raid_counts[p.name]=count
            for pos,body in sorted(edits,reverse=True):s=s[:pos]+body+s[pos:]
            return s
        modify(p.relative_to(ROOT),human_only)
    write(AUDIT/'raid_policy.json',json.dumps(raid_counts,indent=2))

    # The source's nuclear-state helper lives in its unrelated shelter AI file.
    # Import the small shared predicate without replacing our shelter mechanics.
    trigger='common/scripted_triggers/COLDWAR_quaza_imp_nuclear_ai_triggers.txt'
    modify(trigger,lambda s:s+'\n'+MARKER+'\nimp_is_nuclear_power = {\n\tOR = { has_idea = nuclear_power_off has_idea = nuclear_power_def }\n}\n')

    # Import only the new assets. Existing construction strips already have the
    # 39th frame in this checkout; preserve them after checking dimensions.
    assets=['gfx/interface/resources_strip.dds','gfx/interface/missing_resources_strip.dds']
    for rel in ['interface/imp_uranium.gfx','interface/MD_dynamic_topbar.gfx','interface/military_raids/MD_military_raids.gfx']:
        source=read(SOURCE/rel)
        for tex in re.findall(r'texturefile\s*=\s*"([^"]+)"',source,re.I):
            if 'uranium' in tex or 'enrichment_facility_strike' in tex:assets.append(tex)
    for rel in set(assets):
        backup(rel);(ROOT/rel).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(SOURCE/rel,ROOT/rel)
    # Add uranium to the existing monetary tooltips without discarding local
    # commodity naming, spending or policy descriptions.
    money='localisation/english/MD_money_l_english.yml'
    def money_loc(s):
        out=[]
        for l in s.splitlines():
            if l.lstrip().startswith('TRADE_INCOME_REVENUES_TOOLTIP:'):
                l=l[:-1]+'\\n$[?uranium_exports|+3] from §YUranium§!"'
                out.append(' '+MARKER)
            elif l.lstrip().startswith('INFRA_EXPENSE_TOOLTIP_DELAYED:'):
                l=l[:-1]+'\\nUranium Mines: §R$[?uranium_mine_infra_expense|3]§!"';out.append(' '+MARKER)
            out.append(l)
        return '\n'.join(out)+'\n'
    modify(money,money_loc)
    print('Raid definitions blocked for AI:',sum(raid_counts.values()),raid_counts)
    print('Assets imported:',len(set(assets)))

if __name__=='__main__':main()
