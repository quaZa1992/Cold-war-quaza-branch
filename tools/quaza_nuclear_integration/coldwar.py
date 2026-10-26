# IMPERIA CW — Cold War: 1970 uranium history, shortage behaviour and compatible art.
from pathlib import Path
import json,re
from PIL import Image
from port import ROOT,SOURCE,AUDIT,MARKER,read,write,backup
from adapt import block,modify,one

# Rounded gameplay calibration in 100 tU/year units. Western production uses
# BGS 1969/1970, p.375; Eastern figures are explicitly balancing estimates,
# not a claim that the secret production series is known exactly.
PRODUCTION={789:18,803:50,805:12,800:8,804:7,785:3,763:22,756:9,
958:8,959:3,962:2,275:12,276:6,277:14,1004:4,90:1,1055:1,
44:40,545:24,117:18,118:9,1070:10,716:20,717:5,726:20,
1090:10,1087:5,562:4,534:3,572:3,451:1,123:5,909:3,153:4}

# Developed and prospective Cold War mining districts. No modern global
# reserve totals or exhausted 2000 Wismut balance are presented as 1970 data.
# Values are deposit bands for gameplay, not a historical reserve inventory.
DEPOSITS={
747:(40,2,4),741:(20,2,4),756:(150,3,9),763:(200,3,9),
789:(140,3,6),803:(200,3,9),805:(50,3,6),806:(50,3,6),800:(50,3,6),804:(30,2,4),785:(20,2,4),
958:(40,3,6),959:(20,2,4),962:(20,2,4),961:(15,2,4),
44:(100,3,9),545:(150,3,9),117:(100,3,9),118:(50,3,6),626:(5,1,3),
1070:(170,3,9),716:(100,3,6),717:(150,3,9),718:(30,2,4),726:(130,3,6),1090:(150,3,6),1087:(20,2,4),723:(20,2,4),
275:(70,3,6),276:(150,3,9),277:(110,3,6),283:(100,3,9),329:(200,3,9),1004:(30,2,4),
562:(60,3,6),534:(30,2,4),572:(30,2,4),552:(10,2,3),
451:(40,2,4),123:(25,2,4),909:(15,2,4),153:(15,2,4),
90:(25,2,4),970:(5,1,3),1055:(10,2,3),1056:(5,1,3),443:(20,2,4),454:(20,2,4),
603:(10,2,3),611:(5,1,3),35:(5,1,3),306:(10,2,3)}

def main():
    state_paths={int(p.name.split('-')[0]):p for p in (ROOT/'history/states').glob('*.txt')}
    for sid,amount in PRODUCTION.items():
        p=state_paths[sid]
        def resource(s):
            if re.search(r'\buranium\s*=\s*'+str(amount)+r'\b',s):return s
            if not re.search(r'\bresources\s*=\s*\{',s):
                n=block(s,'state')
                return s[:n['close']]+'\n\t'+MARKER+f'\n\tresources = {{ uranium = {amount} }}\n'+s[n['close']:]
            n=block(s,'resources')
            assert not re.search(r'\buranium\s*=',s[n['open']:n['close']]),p
            return s[:n['close']]+'\n\t\t'+MARKER+f'\n\t\turanium = {amount}\n\t'+s[n['close']:]
        modify(p.relative_to(ROOT),resource)
    effects='common/scripted_effects/COLDWAR_quaza_imp_uranium_effects.txt'
    s=read(ROOT/effects)
    # Buildable geology and existing production are different quantities.
    body='\n'.join(f'\t{sid} = {{ imp_uranium_add_deposit = yes set_variable = {{ imp_uranium_deposit_kt = {kt} }} set_variable = {{ imp_uranium_mine_slots = {slots} }} set_variable = {{ imp_uranium_per_level = {out} }} }}' for sid,(kt,slots,out) in sorted(DEPOSITS.items()))
    s+='\n'+MARKER+'\nCOLDWAR_uranium_setup_1970_deposits = {\n'+body+'\n}\n'
    # There is no free 45% civilian output from post-Cold-War weapons
    # downblending. The existing resource reserve system supplies actual stocks.
    s=one(s,'\t\t\tmultiply = 0.55\n\t\t\tadd = 0.45','\t\t\tmultiply = 1\n\t\t\tadd = 0')
    s=s.replace('# Therefore an enrichment facility without any uranium still works at 45 %.','# Cold War adaptation: fuel stocks are explicit; no uranium means no new enrichment output.')
    # Mine damage must affect mine output, not merely the construction display.
    s=one(s,'imp_uranium_mine_levels = building_level@uranium_mine','imp_uranium_mine_levels = non_damaged_building_level@uranium_mine')
    write(ROOT/effects,s)
    hooks='common/on_actions/COLDWAR_quaza_zzzzzz_imp_uranium_on_actions.txt'
    modify(hooks,lambda s:one(s,'imp_uranium_setup_deposits = yes','if = { limit = { IMP_is_1970_scenario = yes } COLDWAR_uranium_setup_1970_deposits = yes }\n\t\t\t\t\telse = { imp_uranium_setup_deposits = yes }'))
    # Keep counts fresh before the weekly disruption check, including captures.
    nuclear_hooks='common/on_actions/COLDWAR_quaza_zzzzzz_imp_nuclear_programme_on_actions.txt'
    modify(nuclear_hooks,lambda s:one(s,'\ton_weekly = {\n\t\teffect = {','\ton_weekly = {\n\t\teffect = {\n\t\t\t'+MARKER+'\n\t\t\tCOLDWAR_refresh_enrichment_count = yes'))
    s=read(ROOT/effects)+'''\n# IMPERIA CW — Cold War: current controlled enrichment capacity after damage or capture.
COLDWAR_refresh_enrichment_count = {
 set_variable = { undamaged_enrichment_facilities = 0 }
 every_controlled_state = {
  set_temp_variable = { COLDWAR_working_enrichment = non_damaged_building_level@enrichment_facility }
  PREV = { add_to_variable = { undamaged_enrichment_facilities = COLDWAR_working_enrichment } }
 }
}
'''
    write(ROOT/effects,s)
    # A civilian nuclear economy must not be blocked by the weapons-AI policy.
    ai='common/ai_strategy/COLDWAR_quaza_imp_nuclear_ai.txt'
    modify(ai,lambda s:s.replace('enable = { NOT = { has_country_flag = imp_ai_wants_nukes } }','enable = { NOT = { has_country_flag = imp_ai_wants_nukes } has_nuclear_reactors = no }').replace('enable = { has_country_flag = imp_ai_wants_nukes }','enable = { OR = { has_country_flag = imp_ai_wants_nukes has_nuclear_reactors = yes } }'))

    # Preserve the shelter icon at frame 39. Append the source mine icon at 40.
    for name in ['building_icon_strip.dds','building_icon_without_bg_strip.dds']:
        rel='gfx/interface/buildings/'+name;backup(rel)
        ours=Image.open(ROOT/rel).convert('RGBA');source=Image.open(SOURCE/rel).convert('RGBA')
        assert ours.size==(1794,46) and source.size==(1794,46)
        result=Image.new('RGBA',(1840,46));result.paste(ours,(0,0));result.paste(source.crop((1748,0,1794,46)),(1794,0))
        result.save(ROOT/rel)
    modify('interface/countrystateview.gfx',lambda s:s.replace('noOfFrames = 39','\n\t\t'+MARKER+'\n\t\tnoOfFrames = 40'))
    modify('common/buildings/00_buildings.txt',lambda s:s.replace('icon_frame = 39','icon_frame = 40'))
    # A known source error mapped Patagonia to Indian state 454 in older map
    # versions. Verify the current ID belongs to the actual Argentine state.
    assert 'Patagonia' in state_paths[454].name
    write(AUDIT/'coldwar_balance.json',json.dumps({'starting_resources':PRODUCTION,'deposits':DEPOSITS,'method':'Western 1969/1970 BGS production rounded to 100-tU units; Eastern production and deposit capacity are documented gameplay estimates.'},indent=2))
    print('1970 producing states:',len(PRODUCTION),'total raw units:',sum(PRODUCTION.values()),'deposit states:',len(DEPOSITS))

if __name__=='__main__':main()
