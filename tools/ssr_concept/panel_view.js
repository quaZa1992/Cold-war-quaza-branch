// IMPERIA COLD WAR — specialisation comparison and sovereign restructuring preview.
function programmePanel(selected=state.programme?.key||'aircraft'){
 state.panel='specialisations';
 const programmes=model.groups.filter(g=>g.specialisation);
 detail.innerHTML='<h2>Union specialisations</h2><p class="ssr-meta">Every republic can choose any of the nine programmes. One primary specialisation; maritime projects require a working coast.</p><div class="ssr-navigation">'+programmes.map(g=>'<button type="button" data-programme="'+g.specialisation+'">'+esc(g.title)+'</button>').join('')+'</div><div class="ssr-controls"><label>Programme direction<select id="ssr-spec-direction"><option value="left">'+esc(by.get(model.nodes.find(n=>n.specialisation===selected&&n.key.endsWith('_left')).id).title)+'</option><option value="right">'+esc(model.nodes.find(n=>n.specialisation===selected&&n.key.endsWith('_right')).title)+'</option></select></label><label>Administration<select id="ssr-spec-admin"><option value="efficiency">Lean Administration</option><option value="priority">Priority Allocations</option></select></label></div><div id="ssr-spec-results"></div>';
 function redraw(){
  const direction=$('#ssr-spec-direction').value,admin=$('#ssr-spec-admin').value;
  state.programme={key:selected,direction,administration:admin};
  const excluded=[direction==='left'?'right':'left',(direction==='left'?'right':'left')+'_follow',admin==='efficiency'?'priority':'efficiency'];
  const ns=model.nodes.filter(n=>n.specialisation===selected&&!excluded.includes(n.key.slice(('special_'+selected+'_').length)));
  const full={},reduced={},equipment={},legacyEquipment={};let setup=0,weekly=0,legacyWeekly=0;
  for(const n of ns){setup+=n.gdp_cost||0;weekly+=n.weekly_gdp_cost||0;legacyWeekly+=n.legacy_weekly_gdp_cost||0;
   for(const [k,v] of Object.entries(n.modifiers))full[k]=(full[k]||0)+v;
   for(const [k,v] of Object.entries(n.legacy_modifiers))reduced[k]=(reduced[k]||0)+v;
   for(const [source,target] of [[n.equipment_bonuses,equipment],[n.legacy_equipment_bonuses,legacyEquipment]])for(const e of source||[]){target[e.target]??={};for(const [k,v] of Object.entries(e.modifiers))target[e.target][k]=(target[e.target][k]||0)+v;}
  }
  const gear=source=>Object.entries(source).map(([target,modifiers])=>({target,modifiers}));
  const rootNode=ns.find(n=>n.key.endsWith('_mandate'));
  $('#ssr-spec-results').innerHTML='<h3>'+esc(model.groups.find(g=>g.specialisation===selected).title)+'</h3><p>'+esc(rootNode.description)+'</p><div class="ssr-detail-grid"><div><h3>Within the Union</h3><ul>'+rows(full)+price(weekly,true)+'</ul>'+gearRows(gear(equipment))+'</div><div><h3>After independence</h3><ul>'+rows(reduced)+price(legacyWeekly,true)+'</ul>'+gearRows(gear(legacyEquipment))+'</div></div><h3>National assets</h3>'+list(ns.filter(n=>n.building).map(n=>DATA.building_labels[n.building.type]+' +'+n.building.level+'; shared building slots +'+n.building.shared_slots).concat(ns.filter(n=>n.research).map(n=>n.research.uses+' x '+n.research.bonus*100+'% research bonus: '+DATA.research_labels[n.research.category])))+'<p class="ssr-meta">'+esc(rootNode.historical_basis)+(rootNode.historical_anchor?': '+esc(rootNode.historical_anchor):'')+'</p><button type="button" id="ssr-inspect-programme">Inspect focus branch</button>';
  $('#ssr-inspect-programme').addEventListener('click',()=>setChapter('spec_'+selected));
 }
 if(state.programme?.key===selected){$('#ssr-spec-direction').value=state.programme.direction||'left';$('#ssr-spec-admin').value=state.programme.administration||'efficiency';}
 detail.querySelectorAll('[data-programme]').forEach(b=>b.addEventListener('click',()=>{programmePanel(b.dataset.programme);persist();}));
 $('#ssr-spec-direction').addEventListener('change',()=>{redraw();persist();});$('#ssr-spec-admin').addEventListener('change',()=>{redraw();persist();});redraw();
}

function marketPanel(){
 state.panel='market';state.restructuring??={};state.restructuring[state.country]??={};const choices=state.restructuring[state.country];
 detail.innerHTML='<h2>A sovereign economic settlement</h2><label>Reform course<select id="ssr-market-course">'+Object.entries(DATA.market.courses).map(([k,v])=>'<option value="'+k+'">'+esc(v.name)+'</option>').join('')+'</select></label><div id="ssr-market-effects"></div><h3>Enterprise restructuring</h3><p class="ssr-meta">Scenario preview. Each sector can be settled once; alternatives remain inspectable. Sales preserve factories. Liquidation closes one civilian factory and requires an eligible controlled state.</p><div id="ssr-lots"></div><div id="ssr-lot-result"></div><div id="ssr-method-detail"></div>';
 $('#ssr-market-course').value=state.marketCourse||'shock';
 function drawEffects(){const key=$('#ssr-market-course').value;state.marketCourse=key;const course=DATA.market.courses[key];
  $('#ssr-market-effects').innerHTML='<p>'+esc(course.description)+'</p><div class="ssr-detail-grid"><div><h3>'+esc(course.window.name)+' ('+course.window.days+' days)</h3><ul>'+rows(course.window.modifiers)+'</ul></div><div><h3>'+esc(course.fiscal.name)+' ('+course.fiscal.days+' days)</h3><ul>'+rows(course.fiscal.modifiers)+'</ul></div></div><h3>'+esc(course.burden.name)+'</h3><ul>'+rows(course.burden.modifiers)+price(course.gdp_cost)+price(course.weekly_gdp_cost,true)+'</ul>';drawLots();
 }
 function methodDetail(method){
  const m=DATA.market.methods[method],key=$('#ssr-market-course').value,delta=-DATA.market.courses[key].burden.modifiers.consumer_goods_factor/6;
  $('#ssr-method-detail').innerHTML='<h3>'+esc(m.title)+'</h3><p>'+esc(m.description)+'</p><div class="ssr-meta">'+m.days+' days | '+(method==='public'?'Active public-investment charter':method==='liquidate'?'Independent government; an owned and controlled core state with at least two civilian factories':'Active market-property charter')+'</div><ul>'+price(m.gdp_cost)+price(m.gdp_income,false,true)+rows(m.modifiers)+'<li>Industrial Restructuring: Consumer goods factor '+percent(delta)+'</li>'+(m.closure?'<li class="ssr-negative">Project state: Civilian factory -1</li>':'')+'</ul>';
 }
 function drawLots(){
  const key=$('#ssr-market-course').value,course=DATA.market.courses[key];
  $('#ssr-lots').innerHTML=DATA.market.sectors.map(([id,title])=>'<div class="ssr-lot"><label>'+esc(title)+'<select data-lot="'+id+'"><option value="">Unsettled</option>'+Object.entries(DATA.market.methods).map(([key,m])=>'<option value="'+key+'">'+esc(m.title)+'</option>').join('')+'</select></label><button type="button" data-method-info="'+id+'">Inspect terms</button></div>').join('');
  let count=0,loss=0,net=0;const mods={};
  for(const [id,method] of Object.entries(choices)){const m=DATA.market.methods[method];if(!m)continue;count++;loss+=m.closure;net+=m.gdp_income-m.gdp_cost;for(const[k,v]of Object.entries(m.modifiers))mods[k]=(mods[k]||0)+v;}
  for(const select of detail.querySelectorAll('[data-lot]')){select.value=choices[select.dataset.lot]||'';select.addEventListener('change',e=>{if(e.target.value)choices[e.target.dataset.lot]=e.target.value;else delete choices[e.target.dataset.lot];drawLots();if(e.target.value)methodDetail(e.target.value);persist();});}
  detail.querySelectorAll('[data-method-info]').forEach(b=>b.addEventListener('click',()=>methodDetail(choices[b.dataset.methodInfo]||'auction')));
  const remaining=Math.max(0,course.burden.modifiers.consumer_goods_factor*(6-count)/6);
  $('#ssr-lot-result').innerHTML='<h3>Projected settlement: '+count+' / 6 sectors</h3><ul><li>Consumer goods factor '+percent(remaining)+'</li><li class="'+(loss?'ssr-negative':'ssr-neutral')+'">Civilian factory levels '+(loss?'-'+loss:'0')+'</li><li class="'+(net>=0?'ssr-positive':'ssr-negative')+'">Treasury, sum of quoted GDP shares '+percent(net)+' of GDP</li>'+rows(mods)+'</ul>';
 }
 $('#ssr-market-course').addEventListener('change',()=>{drawEffects();persist();});drawEffects();methodDetail('auction');
}
