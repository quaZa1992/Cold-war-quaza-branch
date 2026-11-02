// IMPERIA COLD WAR — GDP and national-focus effect inspector.
function price(share,weekly=false,income=false){
 if(!share)return '';
 return '<li class="'+(income?'ssr-positive':'ssr-negative')+'">'+(weekly?'Weekly programme budget':'Treasury')+' '+percent(income?share:-share)+' of GDP'+(weekly?'':' (one time)')+'</li>';
}
function gearRows(gears){
 return (gears||[]).map(e=>'<h3>'+esc(DATA.equipment_labels[e.target]||e.target)+'</h3><ul>'+Object.entries(e.modifiers).map(([k,v])=>'<li class="'+((v>0)!==/cost/.test(k)?'ssr-positive':'ssr-negative')+'">'+esc(DATA.gear_labels[k]||k)+' '+percent(v)+'</li>').join('')+'</ul>').join('');
}
function baseEffects(n){
 let h='<ul>'+price(n.gdp_cost)+price(n.weekly_gdp_cost,true);
 if(n.replace)h+='<li>Replace '+esc(n.replace)+' with '+esc(n.spirit)+'</li>';
 else if(n.remove)h+='<li>Remove '+esc(n.remove)+'</li>';
 if(Object.keys(n.modifiers).length){
  if(!n.replace)h+='<li>'+(n.effect_mode==='modify'?'Modify ':'Add ')+esc(n.spirit)+'</li>';
  h+=rows(n.display_modifiers||n.modifiers);
 }
 if(n.building){const b=n.building;h+='<li>'+esc(b.target)+': shared building slots +'+b.shared_slots+'</li><li>'+esc(b.target)+': '+esc(DATA.building_labels[b.type]||b.type)+' +'+b.level+'</li>';}
 if(n.research)h+='<li>'+n.research.uses+' x '+n.research.bonus*100+'% research bonus: '+esc(DATA.research_labels[n.research.category]||n.research.category)+'</li>';
 if(n.doctrine)h+='<li>'+n.doctrine.uses+' x '+n.doctrine.bonus*100+'% doctrine cost reduction: '+(n.doctrine.category==='land_doctrine'?'Land doctrine':esc(n.doctrine.category))+'</li>';
 for(const [key,label] of [['army_xp','Army'],['air_xp','Air'],['navy_xp','Naval']])if(n[key])h+='<li>'+label+' experience +'+n[key]+'</li>';
 if(n.stability)h+='<li>Stability '+sign(n.stability*100)+' percentage points</li>';
 if(n.decision)h+='<li>Unlock decisions: '+esc(n.decision)+'</li>';
 if(n.market_charter)h+='<li>Unlock decisions: Competitive Sale, Worker Buyout</li>';
 if(n.public_charter)h+='<li>Unlock decision: Public Retooling</li>';
 if(n.remove_exposure)h+='<li>Remove '+esc(n.remove_exposure)+'</li>';
 if(n.party_transfer){const t=n.party_transfer;h+='<li>'+esc(t.from_name)+': current party support -'+t.fraction*100+'% (relative)</li><li>'+esc(t.to_name)+': gain the transferred support</li>';}
 h+='</ul>'+gearRows(n.equipment_bonuses);
 for(const idea of n.timed_ideas||[])h+='<h3>Add '+esc(idea.name)+' ('+idea.days+' days)</h3><ul>'+rows(idea.modifiers)+'</ul>';
 for(const idea of n.persistent_ideas||[])h+='<h3>Add '+esc(idea.name)+'</h3><ul>'+rows(idea.modifiers)+'</ul>';
 if(n.specialisation){
  h+='<h3>After independence</h3><ul><li>Modify '+esc(n.legacy_spirit)+'</li>'+rows(n.legacy_modifiers)+price(n.legacy_weekly_gdp_cost,true)+'</ul>'+gearRows(n.legacy_equipment_bonuses);
 }
 if(n.preparation_effect)h+='<h3>On independence</h3><ul><li>Modify '+esc(n.preparation_effect.name)+'</li>'+rows(n.preparation_effect.delta)+'</ul>';
 for(const s of n.conditional_removals||[])h+='<h3>If currently has '+esc(s.name)+'</h3><ul><li>Remove '+esc(s.name)+'</li>'+rows(s.delta)+'</ul>';
 if(n.regional_aftercare){const s=n.regional_aftercare;h+='<h3>If currently has '+esc(s.old)+'</h3><ul><li>Replace '+esc(s.old)+' with '+esc(s.new)+'</li>'+rows(s.delta)+'</ul>';}
 if(n.exposure)h+='<h3>On independence</h3><ul><li>Add '+esc(n.exposure.name)+'</li>'+rows(n.exposure.modifiers)+'</ul>';
 if(n.repair_variants)for(const v of n.repair_variants[state.case])h+='<h3>With '+v.before_count+' completed repairs</h3><ul><li>'+(v.before_count===2?'Remove ':'Modify ')+esc(v.name)+'</li>'+rows(v.delta)+'</ul>';
 if(n.action?.startsWith('offer:')){
  const t=DATA.contracts[n.action.slice(6)];h+='<h3>If they accept</h3><div class="ssr-detail-grid">';
  for(const key of ['origin','recipient']){const side=t[key];h+='<div><strong>'+esc(key==='origin'?model.profile.independent_name:t.target)+'</strong><ul><li>Add '+esc(side.spirit)+'</li>'+rows(side.modifiers)+price(side.gdp_cost)+price(side.weekly_gdp_cost,true)+'</ul></div>';}
  h+='</div>';
 }
 return h;
}
