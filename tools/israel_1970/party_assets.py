# IMPERIA CW — Cold War: israel 1970 — party assets.
"""Register period party identities, constituent lists and later MD party variants."""
from pathlib import Path
import re
from PIL import Image

# Fixed MD slots are political families. Constituents use named variants of the
# same family instead of expanding the global 24-slot politics engine.
START_NAMES={0:'Mafdal - National Religious Party',1:'Gahal - Herut and Liberal Bloc',2:'Independent Liberals',3:'Alignment - Labor and Mapam',4:'Rakah - New Communist List',13:'Agudat Israel and Poalei Agudat Israel',14:'State List',15:'Progress and Development / Cooperation and Brotherhood',16:'HaOlam HaZeh - New Force',18:'Mapam - United Workers Party',19:'Maki - Israeli Communist Party',20:'Free Center'}
# key, slot, first year, English name, MD icon, optional period leader.
VARIANTS=[
 ('herut',1,1970,'Herut','generic_conservatism_small','Menachem Begin'),
 ('liberal_party',1,1970,'Liberal Party','generic_liberalism_small','Elimelech Rimalt'),
 ('labor_party',3,1970,'Labor Party - HaAvoda','ISR_socialism','Golda Meir'),
 ('agudat',13,1970,'Agudat Israel','generic_Neutral_Autocracy_small','Orthodox Parliamentary Council'),
 ('poalei_agudat',13,1970,'Poalei Agudat Israel','generic_Neutral_Autocracy_small','Workers\' Religious Council'),
 ('progress_development',15,1970,'Progress and Development','generic_oligarchism_small','Municipal Development Council'),
 ('cooperation_brotherhood',15,1970,'Cooperation and Brotherhood','generic_oligarchism_small','Arab Municipal Council'),
 ('peace_list',18,1970,'Peace List','generic_neutral_Social_small','Peace List Council'),
 ('young_israel',0,1970,'Young Israel','generic_Western_Autocracy_small','Religious Youth Council'),
 ('likud',1,1973,'Likud - National Liberal Movement','ISR_conservatism','Menachem Begin'),
 ('shinui',2,1974,'Shinui - Change','ISR_liberalism_alt2','Amnon Rubinstein'),
 ('hadash',4,1977,'Hadash - Democratic Front for Peace and Equality','ISR_Communist_State','Meir Vilner'),
 ('shas',6,1984,'Shas - Sephardic Guardians','ISR_Nat_Populism','Ovadia Yosef'),
 ('kach',21,1971,'Kach','generic_Nat_Fascism_small','Meir Kahane'),
 ('utj',13,1992,'United Torah Judaism','ISR_Neutral_Autocracy','Orthodox Parliamentary Council'),
 ('meretz',18,1992,'Meretz','ISR_neutral_Social','Yossi Sarid'),
 ('balad',5,1995,'Balad - National Democratic Alliance','ISR_anarchist_communism','Azmi Bishara'),
 ('daam',19,1995,'Da\'am - Workers Party','ISR_Neutral_Communism','Workers\' Party Council'),
 ('taal',7,1996,'Ta\'al - Arab Movement for Renewal','ISR_Autocracy','Ahmad Tibi'),
 ('raam',12,1996,'Ra\'am - United Arab List','ISR_Neutral_Muslim_Brotherhood','Municipal Reform Council'),
 ('yisrael_baaliyah',14,1996,'Yisrael BaAliyah - Israel on the Rise','ISR_non_aligned_conservative','Natan Sharansky'),
 ('greens',17,1997,'HaYerukim - The Greens','ISR_Neutral_Green','Environmental Council'),
 ('tkuma',20,1998,'Tkuma - National Union','ISR_liberalism','National Religious Council'),
 ('center_party',2,1999,'Merkaz - Center Party','ISR_liberalism_alt','Yitzhak Mordechai'),
 ('yisrael_beiteinu',15,1999,'Yisrael Beiteinu - Israel Our Home','ISR_oligarchism','Avigdor Lieberman'),
 ('kadima',1,2005,'Kadima - Forward','ISR_liberalism_alt1','Ariel Sharon'),
 ('yesh_atid',2,2012,'Yesh Atid - There Is a Future','ISR_liberalism_alt3','Yair Lapid'),
 ('otzma',21,2012,'Otzma Yehudit - Jewish Power','ISR_Nat_Fascism','National Front Executive'),
 ('zehut',16,2015,'Zehut - Identity','ISR_Neutral_Libertarian','Moshe Feiglin'),
 ('jewish_home',0,2008,'HaBayit HaYehudi - Jewish Home','ISR_Western_Autocracy','Religious Zionist Council'),
 ('hosen',2,2018,'Hosen LeYisrael - Israel Resilience','ISR_liberalism_alt4','Benny Gantz'),
 ('blue_white',2,2019,'Kahol Lavan - Blue and White','ISR_liberalism_alt5','Benny Gantz'),
 ('noam',0,2019,'Noam','ISR_nationalist_monarchist','Religious Social Council'),
 ('new_hope',2,2020,'Tikva Hadasha - New Hope','ISR_liberalism_alt7','Gideon Sa\'ar'),
 ('national_unity',2,2022,'HaMahane HaMamlakhti - National Unity','ISR_liberalism_alt6','Benny Gantz'),
 ('democrats_labor',3,2024,'The Democrats - Labor Wing','ISR_democrats','Democratic Alliance Council'),
 ('democrats_meretz',18,2024,'The Democrats - Meretz Wing','ISR_democrats','Democratic Alliance Council'),
]

def register(root,ideologies,parties,write,loc,active_slots):
    src='\n'.join(p.read_text(encoding='utf-8-sig') for p in (root/'interface').glob('*.gfx') if p.name!='ISR70_parties.gfx')
    sprites=dict(re.findall(r'name\s*=\s*"([^"]+)"\s*\n\s*texturefile\s*=\s*"([^"]+)"',src))
    lines=['# MD Cold War | Israel party icons; native MD art, no invented historical logos.','spriteTypes = {']
    iconmap={}
    def asset(key,source):
        if source=='generic_communist_state_small':source='generic_Communist_State_small'
        name='GFX_'+source
        assert name in sprites,(key,name)
        path=root/sprites[name];assert path.is_file(),path
        im=Image.open(path).convert('RGBA');im.thumbnail((22,22),Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(22,22));canvas.alpha_composite(im,((22-im.width)//2,(22-im.height)//2))
        texture='gfx/texticons/parties_icons/israel/1970/'+key+'.dds'
        dest=root/texture;dest.parent.mkdir(parents=True,exist_ok=True);canvas.save(dest)
        lines.extend(['\tspriteType = {',f'\t\tname = "GFX_ISR70_{key}"',f'\t\ttexturefile = "{texture}"','\t\tlegacy_lazy_load = no','\t}'])
        iconmap[key]=texture
    for idx,ideology in enumerate(ideologies):
        if idx not in active_slots:continue
        source='ISR_socialism' if idx==3 else 'generic_'+ideology+'_small'
        asset('party_'+str(idx),source)
        loc(f'ISR70_party_{idx}_icon','£ISR70_party_'+str(idx))
    for key,idx,year,name,source,leader in VARIANTS:
        asset('variant_'+key,source)
        loc('ISR70_variant_'+key,'£ISR70_variant_'+key+' '+name)
        loc('ISR70_variant_'+key+'_icon','£ISR70_variant_'+key)
        desc=('A named constituent of the period political family. Choosing this list changes the family\'s presentation and candidate without creating extra votes.' if year==1970 else f'A later political formation, available from {year}. It retains the existing party-family programme and does not duplicate focus rewards.')
        if key=='noam':desc+=' This socially religious party is represented in the religious-Zionist family; it does not establish a monarchy.'
        loc('ISR70_variant_'+key+'_desc',desc)
    lines.append('}');write('interface/ISR70_parties.gfx','\n'.join(lines)+'\n')
    return iconmap
