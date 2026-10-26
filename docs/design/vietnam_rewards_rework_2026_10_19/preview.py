"""Build the installed-reward inspector and a native Chinh branch proof."""
from pathlib import Path
import hashlib,importlib.util,json,re,sys
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
VIZ=Path('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f32-41dc-74b3-baa1-8f6916e026ed')
sys.path.insert(0,str(ROOT/'tools/vietnam_1970'))
from runtime_design import load_design,load_campaign_design

COST={'bureaucracy_cost_multiplier_modifier','education_cost_multiplier_modifier','social_cost_multiplier_modifier','supply_consumption_factor','training_time_army_factor','mdcw_cw_market_exposure','industry_air_damage_factor','land_doctrine_cost_factor','resistance_target','resistance_growth','resistance_damage_to_garrison'}
CATEGORIES={'CAT_industry':'Industry','CAT_construction':'Construction','CAT_electronics':'Electronics','CAT_infantry_weapons':'Infantry equipment','CAT_special_forces_equipment':'Special forces equipment','land_doctrine':'Land doctrine','naval_doctrine':'Naval doctrine','air_doctrine':'Air doctrine'}

def main():
    inv=json.loads((HERE/'inventory.json').read_text(encoding='utf-8'))
    baseline=json.loads((ROOT/'docs/design/vietnam_impact_audit_2026_10_19/inventory.json').read_text(encoding='utf-8'))
    old={n['id']:n for n in baseline['nodes']}
    d,c=load_design(),load_campaign_design();definitions={n['id']:n for n in d['nodes']+c['nodes']}
    loc={k:json.loads(v) for k,v in re.findall(r'^ ([^ :]+):0 (".*")$',(ROOT/'localisation/english/COLDWAR_VIE_1970_l_english.yml').read_text(encoding='utf-8-sig'),re.M)}
    labels={k.removeprefix('COLDWAR_VIE_tt_'):v.split(':')[0] for k,v in loc.items() if k.startswith('COLDWAR_VIE_tt_')}
    def modifier(k,v,target=None):
        title=labels.get(k,k.replace('_',' ').capitalize());flat=k in ('max_dig_in','globalism_equilibrium')
        amount=abs(v) if flat else abs(v)*100
        txt=f'{amount:g}'+(' levels' if k=='max_dig_in' else ' points' if flat else '%')+' '+('higher ' if v>0 else 'lower ')+title
        if target:txt+=' against '+{'CHI':'China','CBD':'Cambodia'}.get(target,target)
        return dict(text=txt,tone='bad' if ((k in COST and v>0) or (k not in COST and v<0)) else 'good')
    def rows(n):
        result=[modifier(k,v) for k,v in n.get('modifiers',{}).items()]
        def add(text,tone=None):result.append(dict(text=text,tone=tone))
        for e in n['effects']:
            kind=e.get('type',e.get('kind'))
            if kind=='idea':
                add(e['title']+(' · '+str(e['duration'])+' days maximum' if e['duration'] else ' · earned institution'))
                result.extend(modifier(k,v) for k,v in e['modifiers'].items())
                result.extend(modifier(k,v,e.get('target')) for k,v in e.get('targeted_modifiers',{}).items())
            elif kind in ('army_experience','xp'):add(str(e.get('value',e.get('amount')))+' Army experience','good')
            elif kind in ('air_xp','navy_xp'):add(str(e['amount'])+(' Air' if kind=='air_xp' else ' Navy')+' experience','good')
            elif kind in ('research','research_bonus'):add(f'{e["uses"]} × {e["bonus"]*100:g}% '+CATEGORIES.get(e['category'],e['category'])+' research bonus','good')
            elif kind in ('doctrine','doctrine_bonus'):add(f'{e["uses"]} × {e.get("value",e.get("cost_reduction"))*100:g}% '+CATEGORIES.get(e.get('category','land_doctrine'),e.get('category','land_doctrine'))+' cost reduction','good')
            elif kind=='spirit_stage':add('Improve '+e['spirit'].replace('_',' ').title()+' to recovery stage '+str(e['stage']),'good')
            elif kind in ('decision_unlock','unlock'):add('Decision programme: '+e.get('label',e.get('category','')).replace('_',' '))
            elif kind=='wargoal':add('War goal against '+e['target'])
            elif kind=='party_popularity':add(f'{e["amount"]*100:g} percentage points of party support','good')
        if n.get('support'):add(f'{n["support"][1]*100:g} percentage points of support for '+{19:'the Front',22:'the military council'}.get(n['support'][0],'the selected party'),'good')
        terrain=n.get('terrain_training',n.get('terrain'))
        if terrain:add(f'{terrain["defence"]*100:g}% Army defence in forest and jungle while the policy is active','good')
        if n.get('building'):
            state,kind=n['building'];title={'industrial_complex':'Civilian complex','arms_factory':'Military factory','dockyard':'Dockyard','fossil_powerplant':'Fossil power plant','infrastructure':'Infrastructure','agriculture_district':'Agricultural district','anti_air_building':'Anti air battery'}.get(kind,kind)
            add(('Complete ' if n.get('instant_build') else 'Start construction of ')+title+' in state '+str(state),'good')
        for text in n.get('preserved_crisis_code',[]):
            m=re.search(r'idea\s*=\s*(\w+).*days\s*=\s*(\d+)',text)
            if m:add(loc.get(m[1],m[1])+' · '+m[2]+' days','bad')
        if n.get('reserve_first_term'):add('First funded term is reserved until its actual conditions hold. Later renewals require payment.')
        return result
    nodes=[]
    for n in inv['nodes']:
        source=definitions[n['id']]
        out={k:n[k] for k in ('id','label','description','group','x','y','days','prerequisites','exclusive','icon')}
        review=source.get('reward_review',{})
        out.update(lines=rows(source),before=rows(old[n['id']]),reason=review.get('why_player_wants_it','') if isinstance(review,dict) else review,
            cost=f'Contribution: ${source.get("cash",0):g} billion once',
            lifetime={'national_persistent':'Nationale Entwicklung','party_bound':'Aktiv bei der regierenden Partei','party_and_leader_bound':'Aktiv bei genau dieser Führung und Partei'}.get(source.get('lifecycle'),'Institution oder finanziertes Programm mit echten Bedingungen'))
        if n['id'] in ('COLDWAR_VIE_chinh_schools','COLDWAR_VIE_chinh_experts'):out['lifetime']='Parteigebundene Institution über die reguläre Nachfolge hinweg'
        nodes.append(out)
    data=dict(nodes=nodes,groups=inv['groups'],art=inv['art'],font=inv['font'])
    html=(VIZ/'coldwar-vietnam-rewards.template.html').read_text(encoding='utf-8').replace('__REWARDS_DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</',r'<\/'))
    dest=VIZ/'coldwar-vietnam-rewards.html';assert len(html.encode('utf-8'))<1_000_000
    dest.write_text(html,encoding='utf-8',newline='\n')
    (HERE/'preview_data.json').write_text(json.dumps(dict(nodes=nodes,groups=inv['groups']),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    spec=importlib.util.spec_from_file_location('reward_native',VIZ/'coldwar-vietnam-render.py');native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
    label=native.NativeLabelFont();bar=Image.open(native.asset('gfx/interface/focusview/titlebar/focus_unavailable_bg.dds')).convert('RGBA')
    subset=[n for n in nodes if n['group']=='chinh' and n['y']<=2];by={n['id']:n for n in nodes}
    im=Image.new('RGBA',(760,520),'#202825');draw=ImageDraw.Draw(im);f=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',17)
    draw.text((18,14),'INSTALLED: a substantive education choice in 140 focus days',font=f,fill='#e9d9a6')
    def pt(n):return round((n['x']-20)*96+380),round(n['y']*130+130)
    for n in subset:
        x,y=pt(n)
        for clause in n['prerequisites']:
            for parent in clause:
                p=by[parent]
                if p not in subset:continue
                px,py=pt(p);mid=(py+69+y-43)//2;draw.line([(px,py+69),(px,mid),(x,mid),(x,y-43)],fill='#8e9c89',width=2)
    for n in subset:
        x,y=pt(n);art=Image.open(ROOT/n['icon']).convert('RGBA');im.alpha_composite(bar,(x-bar.width//2,y+20));im.alpha_composite(art,(x-art.width//2,y-art.height//2));label.draw(im,(x,y+45),n['label'],(230,224,211))
    proof=VIZ/'coldwar-vietnam-rewards-chinh.png';im.convert('RGB').save(proof)
    report=dict(html=str(dest),bytes=dest.stat().st_size,focuses=len(nodes),pairs=inv['counts']['exclusive_pairs'],proof=str(proof),engine_tested=False,browser_tested=False)
    (HERE/'preview_review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':main()
