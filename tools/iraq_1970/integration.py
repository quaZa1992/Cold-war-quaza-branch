# IMPERIA CW — Cold War: iraq 1970 — integration.
"""Narrow, idempotent adapters into the existing native MD providers."""
from common import *
import re,hashlib,json

def closing(text,opening):
    depth=0;quote=False;comment=False;escape=False
    for i in range(opening,len(text)):
        c=text[i]
        if comment:
            if c=='\n':comment=False
            continue
        if quote:
            if escape:escape=False
            elif c=='\\':escape=True
            elif c=='"':quote=False
            continue
        if c=='#':comment=True
        elif c=='"':quote=True
        elif c=='{':depth+=1
        elif c=='}':
            depth-=1
            if depth==0:return i
    raise ValueError('Unbalanced source block')

def install(root=ROOT):
    changes=[];backups=root/'tools/iraq_1970/integration_baseline';backups.mkdir(parents=True,exist_ok=True)
    def edit(rel,fn):
        p=root/rel;old=p.read_text(encoding='utf-8-sig');new=fn(old)
        parse(new)
        backup=backups/rel;backup.parent.mkdir(parents=True,exist_ok=True)
        if not backup.exists():backup.write_bytes(p.read_bytes())
        if old!=new:p.write_text(new,encoding='utf-8',newline='\n')
        changes.append({'path':rel,'baseline_sha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    def once(s,marker,needle,replacement):
        if marker in s:return s
        assert s.count(needle)==1,(marker,s.count(needle))
        return s.replace(needle,replacement,1)
    def history(s):
        s=once(s,'# COLDWAR IRQ authored tree','load_focus_tree = mdcw_1970_generic_focus','load_focus_tree = COLDWAR_IRQ_1970_focus # COLDWAR IRQ authored tree').replace('expire = "1979.7.16"','expire = "1982.10.4"')
        needle='create_country_leader = { name = "Ahmed Hassan al-Bakr" picture = "gfx/Leaders/IRQ/IRQ_Coldwar_Ahmed_Hassan_al_Bakr.dds" expire = "1982.10.4" ideology = Nat_Fascism }'
        return once(s,'# COLDWAR IRQ history spirits',needle,needle+'\n\t\tCOLDWAR_IRQ_seed_starting_spirits = yes # COLDWAR IRQ history spirits')
    edit('history/countries/IRQ - Iraq.txt',history)
    edit('common/scripted_effects/mdcw_1970_focus_tree_effects.txt',lambda s:once(s,'# COLDWAR IRQ authored exemption','original_tag = VIE IMP_is_1970_scenario = yes } # COLDWAR_VIE_1970_focus','original_tag = VIE IMP_is_1970_scenario = yes } # COLDWAR_VIE_1970_focus\n\t\t\t\t\tAND = { original_tag = IRQ IMP_is_1970_scenario = yes } # COLDWAR IRQ authored exemption'))
    dispatch='\t# IMPERIA CW — Cold War: iraq 1970 generated content.\n\t# COLDWAR IRQ LEADER ROUTE BEGIN\n\telse_if = {\n\t\tlimit = { COLDWAR_IRQ_campaign_active = yes }\n\t\tCOLDWAR_IRQ_set_leader = yes\n\t}\n\t# COLDWAR IRQ LEADER ROUTE END\n'
    edit('common/scripted_effects/00_leader_setup_scripted_effects.txt',lambda s:once(s,'COLDWAR IRQ LEADER ROUTE BEGIN','\t# COLDWAR EASTMED DISPATCH END\n','\t# COLDWAR EASTMED DISPATCH END\n'+dispatch))
    def irqprovider(s):
        if '# COLDWAR IRQ PROVIDER BEGIN' in s:return s
        # The old native-pool generator left the provider's final closing brace
        # inside its end-marker comment. Restore that brace before wrapping.
        if '# MDCW HISTORICAL NATIVE POOL END IRQ}' in s:
            s=s.replace('# MDCW HISTORICAL NATIVE POOL END IRQ}','# MDCW HISTORICAL NATIVE POOL END IRQ\n}')
        m=re.search(r'\bset_leader_IRQ\s*=\s*\{',s);end=closing(s,m.end()-1)
        return s[:m.end()]+'\n# IMPERIA CW — Cold War: iraq 1970 generated content.\n# COLDWAR IRQ PROVIDER BEGIN\nif = { limit = { COLDWAR_IRQ_campaign_active = yes } COLDWAR_IRQ_set_leader = yes }\nelse = {\n'+s[m.end():end]+'''\n}
# COLDWAR IRQ PROVIDER END
'''+s[end:]
    edit('common/scripted_effects/IRQ_political_leaders.txt',irqprovider)
    edit('common/scripted_effects/00_MD_politicsview_scripted_effects.txt',lambda s:once(s,'# COLDWAR IRQ exact subparty refresh','\t\tif = { limit = { COLDWAR_VIE_is_1970 = yes } COLDWAR_VIE_sync_programmes = yes }','\t\tif = { limit = { COLDWAR_VIE_is_1970 = yes } COLDWAR_VIE_sync_programmes = yes }\n\t\tif = { limit = { COLDWAR_IRQ_campaign_active = yes } COLDWAR_IRQ_reconcile_programmes = yes COLDWAR_IRQ_reconcile_situations = yes } # COLDWAR IRQ exact subparty refresh'))
    def parties(s):
        for slot,(_,family,_) in PARTIES.items():
            for suffix in ['', '_desc','_icon']:
                marker=f'# COLDWAR IRQ registry {slot}{suffix}'
                if marker in s:continue
                name='MDCW_HP_'+family+suffix
                pat=re.compile(r'(\bname\s*=\s*'+re.escape(name)+r'\s*\n)')
                ms=list(pat.finditer(s));assert len(ms)==1,(name,len(ms));m=ms[0]
                gate='COLDWAR_IRQ_campaign_active = yes'
                if slot==19:gate+=' has_country_flag = COLDWAR_IRQ_puk_formed'
                if slot==9:gate+=' has_country_flag = COLDWAR_IRQ_sciri_formed'
                row='\ttext = { trigger = { '+gate+' } localization_key = COLDWAR_IRQ_party_'+str(slot)+suffix+' } '+marker+'\n'
                s=s[:m.end()]+row+s[m.end():]
        return s
    edit('common/scripted_localisation/mdcw_historical_parties.txt',parties)
    # Preserve native Bakr identity during the startup world-profile pass. The
    # country provider handles optional retention and actual dated mortality.
    def world(s):
        marker='# COLDWAR IRQ leadership lifetime'
        if marker in s:return s
        needle='create_country_leader = { name = "Ahmed Hassan al-Bakr" picture = "gfx/Leaders/IRQ/IRQ_Coldwar_Ahmed_Hassan_al_Bakr.dds" expire = "1979.7.16" ideology = Nat_Fascism }'
        assert s.count(needle)==1
        return s.replace(needle,needle.replace('1979.7.16','1982.10.4')+' '+marker)
    edit('common/scripted_effects/IMP_1970_world_politics_effects.txt',world)
    def usa(s):
        marker='# COLDWAR USA GULF FOCUSES BEGIN';endmarker='# COLDWAR USA GULF FOCUSES END'
        if marker in s:
            start=s.index(marker);end=s.index(endmarker,start)+len(endmarker)
            s=s[:start]+s[end:].lstrip('\r\n')
        m=re.search(r'\bfocus_tree\s*=\s*\{',s);end=closing(s,m.end()-1)
        fragment=(root/'tools/iraq_1970/staged/USA_GULF_FOCUS_FRAGMENT.txt').read_text(encoding='utf-8-sig')
        fs=parse(fragment)
        for k,o,v in fs:
            if k=='focus' and first(v,'relative_position_id') is None:
                for i,(key,op,value) in enumerate(v):
                    if key=='x':v[i]=(key,op,str(int(value)+30))
        fragment=emit(fs)
        addition=marker+'\n'+fragment+'\nshortcut = { name = COLDWAR_USA_gulf_shortcut target = COLDWAR_USA_gulf_desert_storm scroll_wheel_factor = 0.8 }\n'+endmarker+'\n'
        return s[:end]+addition+s[end:]
    edit('common/national_focus/USA_1970.txt',usa)
    def resistance(s):
        marker='# COLDWAR IRQ bounded northern uprising guard'
        if marker in s:return s
        m=re.search(r'\bresistance_90\s*=\s*\{',s);start=m.end();end=closing(s,start-1)
        old=s[start:end];en=re.search(r'\benabled\s*=\s*\{',old)
        if en:
            pos=start+en.end();return s[:pos]+'\nNOT = { COLDWAR_USA_gulf_native_revolt_guard = yes } '+marker+'\n'+s[pos:]
        return s[:start]+'\n\tenabled = { NOT = { COLDWAR_USA_gulf_native_revolt_guard = yes } } '+marker+s[start:]
    edit('common/resistance_compliance_modifiers/resistance_modifiers.txt',resistance)
    return changes
