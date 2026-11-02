# IMPERIA CW — Cold War: render installed DDR GUI coordinates and DDS assets.
"""Approximate native preview using actual installed-script presentation values."""
from pathlib import Path
import json
import re
from PIL import ImageFont
import preview_gui as p
from test_ddr_relations import Relations,load,first,E
from script_ast import emit

ROOT=Path(__file__).resolve().parents[2]


def main():
    p.font=lambda size,bold=True:ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',size)
    Relations.setUpClass();fixture=Relations();fixture.setUp()
    fixture.d.flags.add('cwgg_east_open')
    fixture.w.vars.update(cwgg_krise_typ=1,cwgg_krise_int=45,cwgg_krise_runde=1,cwgg_krise_max=4,
                          cwgg_krise_monat=3,cwgg_last_h=2,cwgg_last_a=5,cwgg_ddr_wahl=2,
                          cwgg_vertrag_1=1,cwgg_vertrag_2=1,cwgg_verh=3,cwgg_verh_prog=58,
                          cwgg_mob_brd=1,cwgg_mob_ddr=1,cwgg_aufm_brd_div=7,cwgg_aufm_ddr_div=9)
    fixture.m.run(E+'_gui_refresh',fixture.d)
    # Only preview fixtures become floats; the execution model uses Decimal.
    state={k:float(v) for k,v in fixture.w.vars.items()}
    state.update({k:float(v) for k,v in fixture.d.vars.items()})
    state.update({'GER.'+k:float(v) for k,v in fixture.w.vars.items()})
    state['_flags']=list(fixture.d.flags)
    r=p.Renderer(str(ROOT),str(ROOT/'gfx/interface'),state)
    loc=(ROOT/'localisation/english/COLDWAR_DDR_1970_relations_l_english.yml').read_text(encoding='utf-8-sig')
    r.loc.update({k:v.replace('\\n','\n') for k,v in re.findall(r'^ ([^:\s]+):0 "(.*)"$',loc,re.M)})
    r.loc={k:v.replace('[Root.GetLeader]','Walter Ulbricht') for k,v in r.loc.items()}
    r.sprites['GFX_cwgg_akte_bg_ddr']=(str(ROOT/'gfx/interface/cwger_1970/cwgg_akte_bg_ddr.dds'),1)
    for k,o,v in load('common/scripted_localisation/COLDWAR_DDR_1970_relations.txt'):
        r.dt[first(v,'name')]=[(emit(first(row,'trigger',[])),first(row,'localization_key')) for key,op,row in v if key=='text']
    wins=p.parse_gui((ROOT/'interface/COLDWAR_DDR_1970_relations.gui').read_text())
    sg=(ROOT/'common/scripted_guis/COLDWAR_DDR_1970_relations.txt').read_text()
    bars=[k for k in wins if k!='cwgg_east_main_window' and k.endswith('_window')]
    out=Path(__file__).with_name('ddr_relations_preview');out.mkdir(exist_ok=True)
    report={}
    for tab in range(1,6):
        r.state['cwgg_east_tab']=tab
        report[str(tab)]=r.render(wins,'cwgg_east_main_window',bars,sg,tab,str(out/f'tab_{tab}.png'))
    (out/'review.json').write_text(json.dumps(dict(native_engine=False,approximate_fonts=True,tabs=report),indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report))


if __name__=='__main__':main()
