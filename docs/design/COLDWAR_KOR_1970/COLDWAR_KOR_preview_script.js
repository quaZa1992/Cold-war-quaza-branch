// IMPERIA CW — Cold War: extracted preview script.

(() => {
  const root=document.getElementById('coldwar-kor-concept');
  const D=JSON.parse(document.getElementById('coldwar-kor-data').textContent);
  root.style.setProperty('--kor-native-titlebar','url("'+D.titlebar_data+'")');
  const q=id=>root.querySelector('#'+id), escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const view=q('kor-view'),world=q('kor-world'),lines=q('kor-lines'),inspector=q('kor-inspector');
  const byId=new Map(D.nodes.map(n=>[n.id,n]));
  const worldWidth=Math.max(...D.nodes.map(n=>n.xy[0]*96+300),D.layout.continuous_focus_position[0]+550),worldHeight=Math.max(...D.nodes.map(n=>n.xy[1]*130+160),D.layout.continuous_focus_position[1]+550);
  world.style.width=worldWidth+'px';world.style.height=worldHeight+'px';lines.setAttribute('width',worldWidth);lines.setAttribute('height',worldHeight);
  const NS='http://www.w3.org/2000/svg';
  const X=n=>n.xy[0]*96,Y=n=>n.xy[1]*130;
  let scale=.85,tx=0,ty=0,branch='transition',government='drp',phase='authoritarian',selection=D.layout.initial_focus,overview=false,drag=null,ready=false,restoring=false;
  const groups=new Map(D.groups.map(g=>[g.id,g]));
  const govGroups={drp:'drp',ndp:'ndp',ys:'reform',dj:'reform',chun:'army',roh:'army',usp:'usp',students:'minjung',left:'minjung',rpr:'rpr',security:'security',kjp:'kjp',choi:'caretaker'};
  function ownerEligible(n){
    if(n.ownership==='national')return true;
    if(n.group!==govGroups[government])return false;
    if(n.ownership.startsWith('leader:')){
      const owner=n.ownership.slice(7);const names={drp:'Park Chung Hee',ys:'Kim Young-sam',dj:'Kim Dae-jung',chun:'Chun Doo-hwan',roh:'Roh Tae-woo',kjp:'Kim Jong-pil'};
      return owner===names[government];
    }
    if(n.ownership==='party:5')return government==='students';
    if(n.ownership==='party:19')return government==='left';
    return true;
  }
  const phaseKeys=['electoral_opening','caretaker_installed','military_opening_authorized','negotiating_commitment','talks_authorized','constitutional_ratification_passed','constitutional_order','lawful_election_completed'];
  function eligible(n){
    if(!ownerEligible(n))return false;
    const flags=new Set();
    if(phase==='electoral')flags.add('electoral_opening');
    if(phase==='caretaker')flags.add('caretaker_installed');
    if(phase==='withdrawal')flags.add('military_opening_authorized');
    if(['talks','ratified','civilian','handover'].includes(phase)){flags.add(government==='choi'?'caretaker_installed':['chun','roh','security'].includes(government)?'military_opening_authorized':'electoral_opening');flags.add('negotiating_commitment');flags.add('talks_authorized');}
    if(['ratified','civilian','handover'].includes(phase))flags.add('constitutional_ratification_passed');
    if(['civilian','handover'].includes(phase))flags.add('constitutional_order');
    if(phase==='handover')flags.add('lawful_election_completed');
    const gate=n.native_gate_body||'';
    return phaseKeys.every(k=>!gate.includes('has_country_flag = COLDWAR_KOR_'+k)||flags.has(k));
  }
  function svg(tag,attrs){let e=document.createElementNS(NS,tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));lines.append(e);return e;}
  for(const n of D.nodes){
    for(const row of n.prerequisites)for(const id of row){
      const p=byId.get(id),px=X(p)+82.5,py=Y(p),x=X(n)+82.5,y=Y(n),mid=(py+96+y-25)/2;
      svg('path',{d:`M${px},${py+96} V${mid} H${x} V${y-25}`,class:'kor-prerequisite','data-from':id,'data-to':n.id});
    }
    for(const id of n.mutually_exclusive)if(n.id<id){
      const other=byId.get(id),a=X(n)+82.5,b=X(other)+82.5,y=Y(n)+23;
      if(D.nodes.some(q=>q.xy[1]===n.xy[1]&&q.xy[0]>Math.min(n.xy[0],other.xy[0])&&q.xy[0]<Math.max(n.xy[0],other.xy[0])&&n.mutually_exclusive.includes(q.id)&&q.mutually_exclusive.includes(id)))continue;
      const left=Math.min(a,b),right=Math.max(a,b);
      svg('path',{d:`M${left+68},${y} H${right-68}`,class:'kor-exclusive'});
      svg('text',{x:(left+right)/2,y:y+7,class:'kor-cross'}).textContent='×';
    }
  }
  const buttons=new Map();
  for(const n of D.nodes){
    let b=document.createElement('button');b.type='button';b.className='kor-focus';b.dataset.focus=n.id;
    b.style.left=X(n)+'px';b.style.top=Y(n)+'px';b.setAttribute('aria-label',n.label+', '+n.days+' days');b.setAttribute('aria-pressed','false');
    b.innerHTML='<img alt="" src="'+D.art[n.icon_family].data+'"><span class="kor-titlebar"><span>'+escape(n.label)+'</span></span>';
    b.addEventListener('click',()=>select(n.id));world.append(b);buttons.set(n.id,b);
  }
  const continuous=document.createElement('div');continuous.className='kor-continuous';continuous.style.left=D.layout.continuous_focus_position[0]+'px';continuous.style.top=D.layout.continuous_focus_position[1]+'px';continuous.textContent='Native continuous-focus panel · reserved footprint';world.append(continuous);
  const labels={transition:'Democratic transition',drp:'Park / DRP',ndp:'NDP',reform:'The Two Kims',army:'Chun / Roh',usp:'Social democracy',minjung:'Southern left',rpr:'Revolution',security:'KCIA',economy:'Development',defence:'Defence',foreign:'Foreign policy',korea:'North Korea',kjp:'Kim Jong-pil'};
  for(const g of D.groups){let o=document.createElement('option');o.value=g.id;o.textContent=g.label;q('kor-branch').append(o);}
  function drawLabels(){
    const layer=q('kor-overview-labels');layer.replaceChildren();if(!overview||view.clientWidth<500)return;
    for(const g of D.groups){let b=document.createElement('button');b.type='button';b.textContent=labels[g.id];b.style.left=(g.anchor[0]*96*scale+tx+82.5*scale)+'px';b.style.top=(g.anchor[1]*130*scale+ty-5)+'px';b.addEventListener('click',()=>navigate(g.id));layer.append(b);}
  }
  function camera(){world.style.transform=`translate(${tx}px,${ty}px) scale(${scale})`;world.classList.toggle('overview',scale<.36);drawLabels();}
  function bounds(ns){return {x:Math.min(...ns.map(X))-20,y:Math.min(...ns.map(Y))-85,right:Math.max(Math.max(...ns.map(X))+185,D.layout.continuous_focus_position[0]+550),bottom:Math.max(Math.max(...ns.map(Y))+130,D.layout.continuous_focus_position[1]+550)};}
  function navigate(id){branch=id;overview=false;q('kor-branch').value=id;const g=groups.get(id);scale=.85;tx=view.clientWidth/2-(g.anchor[0]*96+82.5)*scale;ty=85;camera();q('kor-caption').textContent=g.label;select(g.root);save();}
  function entire(commit=true){const b=bounds(D.nodes);overview=true;scale=Math.min((view.clientWidth-32)/(b.right-b.x),(view.clientHeight-60)/(b.bottom-b.y));tx=(view.clientWidth-(b.right-b.x)*scale)/2-b.x*scale;ty=40-b.y*scale;camera();q('kor-caption').textContent='Entire tree · choose a programme above to inspect';if(commit)save();}
  function zoom(mult){const old=scale;scale=Math.max(.06,Math.min(1.7,scale*mult));const cx=view.clientWidth/2,cy=view.clientHeight/2;tx=cx-(cx-tx)*scale/old;ty=cy-(cy-ty)*scale/old;overview=scale<.36;camera();save();}
  function val(key,v){return key==='interest_rate_multiplier_modifier'?(v>=0?'+':'')+v+' percentage points':(v>=0?'+':'')+(v*100).toFixed(2).replace(/\.00$/,'')+'%';}
  function bad(key,v){const expenses=/cost|consumer_goods|training_time|supply_consumption|worker_requirement|interest_rate/.test(key);return expenses?v>0:v<0;}
  function policyHTML(p){return '<li><span class="kor-policy">Policy slot: '+escape(p.qualified_slot||p.slot)+'</span><ul>'+Object.entries(p.modifiers).map(([k,v])=>'<li class="'+(bad(k,v)?'kor-bad':'kor-good')+'">'+escape(D.modifier_labels[k]||k)+': '+val(k,v)+'</li>').join('')+'</ul>'+(p.active_condition?'<em>Requires '+escape(p.active_condition)+'</em>':'')+'</li>';}
  function selectedContractHTML(key){const c=D.contracts.find(x=>x.key===key);if(!c)return '';return '<h4>Offer: '+escape(key.replaceAll('_',' '))+'</h4><p>'+escape(c.description)+'</p><p class="kor-meta">Recipient: '+escape(c.recipient)+' · '+(c.duration_days?c.duration_days+' days':'Political framework')+'</p><ul class="kor-effects"><li class="kor-bad">KOR pays on acceptance: $'+c.KOR_cost_bn+'bn once; $'+c.KOR_weekly_bn.toFixed(5)+'bn/week</li>'+c.KOR_policy.map(policyHTML).join('')+'</ul><p>'+escape(c.refusal)+'</p><details><summary>Recipient option effects</summary><pre>'+escape(JSON.stringify(c.recipient_effects,null,2))+'</pre></details>';}
  function select(id){
    const n=byId.get(id);if(!n)return;selection=id;for(const [k,b] of buttons)b.setAttribute('aria-pressed',String(k===id));
    let effects='';const e=n.effects;
    if(e.cost)effects+='<li class="kor-bad">Treasury: −$'+e.cost+'bn once</li>';
    if(e.weekly)effects+='<li class="kor-bad">Active programme: $'+e.weekly.toFixed(5)+'bn/week; replaces prior slot commitment</li>';
    effects+=e.policies.map(policyHTML).join('');
    for(const b of e.buildings)effects+='<li class="kor-good">State '+b.state+': +'+b.level+' '+escape(b.type.replaceAll('_',' '))+'; once, requires ownership and capacity</li>';
    for(const [k,v] of Object.entries(e.one_time))effects+='<li>'+escape(k.replaceAll('_',' '))+': '+(v>=0?'+':'')+v+'; once</li>';
    for(const a of e.actions)if(!['condition','leader','note','offer'].includes(a.type))effects+='<li>'+escape(a.type.replaceAll('_',' '))+': '+escape(a.value.replaceAll('_',' '))+'</li>';
    if(n.start_replacements)effects+='<li>Replace starting problem: '+escape(n.start_replacements.join(', '))+'</li>';
    const pres=n.prerequisites.map(row=>'('+row.map(id=>byId.get(id).label).join(' OR ')+')').join(' AND ')||'Independent programme entry';
    inspector.innerHTML='<h3>'+escape(n.label)+'</h3><div class="kor-meta">'+n.days+' days · Grid ('+n.xy.join(', ')+') · '+escape(n.ownership)+'</div><p>'+escape(n.description)+'</p><p><strong>Requires:</strong> '+escape(n.gate)+'<br>'+escape(pres)+'</p>'+(n.requirements?.length?'<p>'+n.requirements.map(escape).join('<br>')+'</p>':'')+'<ul class="kor-effects">'+effects+'</ul>'+(n.mutually_exclusive.length?'<p><strong>Mutually exclusive:</strong> '+escape(n.mutually_exclusive.map(id=>byId.get(id).label).join(', '))+'</p>':'')+e.actions.filter(a=>a.type==='offer').map(a=>selectedContractHTML(a.value)).join('')+(n.bypass?'<p><strong>On a refused prerequisite:</strong> '+escape(typeof n.bypass==='string'?n.bypass:n.bypass.effects)+'</p>':'')+(n.conditional_completion?'<p><strong>Settlement:</strong> '+escape(JSON.stringify(n.conditional_completion))+'</p>':'')+'<details><summary>Exact proposal record</summary><pre>'+escape(JSON.stringify(n,null,2))+'</pre></details>';
    if(n.state_effects?.length)inspector.insertAdjacentHTML('beforeend','<h4>Institutional outcomes</h4><ul>'+n.state_effects.map(x=>'<li>'+escape(D.state_outcome_labels?.[x]||x.replace('set_country_flag = COLDWAR_KOR_','Establish: ').replace('clr_country_flag = COLDWAR_KOR_','End: ').replaceAll('_',' '))+'</li>').join('')+'</ul>');
    if(n.temporary_effect)inspector.insertAdjacentHTML('beforeend','<h4>Temporary adjustment · '+n.temporary_effect.days+' days</h4><ul class="kor-effects">'+policyHTML({slot:'Command adjustment',modifiers:n.temporary_effect.modifiers})+'</ul>');
    save();
  }
  function availability(){for(const n of D.nodes)buttons.get(n.id).classList.toggle('unavailable',!eligible(n));}
  function save(){if(!ready||restoring)return;if(window.openai?.setWidgetState)window.openai.setWidgetState({modelContent:{design_revision:D.revision,programme:branch,government,institutional_stage:phase,selected_focus:selection},privateContent:{scale,tx,ty,overview}}).catch(()=>{});}
  function restore(s){if(!s||s.modelContent?.design_revision!==D.revision)return;restoring=true;try{const m=s.modelContent||{};if(groups.has(m.programme)){branch=m.programme;q('kor-branch').value=branch;}if(m.government in govGroups){government=m.government;q('kor-government').value=government;}if([...q('kor-phase').options].some(o=>o.value===m.institutional_stage)){phase=m.institutional_stage;q('kor-phase').value=phase;}availability();if(byId.has(m.selected_focus))select(m.selected_focus);const p=s.privateContent;if(p&&Number.isFinite(p.scale)){scale=p.scale;tx=p.tx;ty=p.ty;overview=!!p.overview;camera();}}finally{restoring=false;}}
  q('kor-spirits').innerHTML=D.starting_spirits.map(s=>'<article class="kor-spirit"><h4>'+escape(s.label)+'</h4><p>'+escape(s.history)+'</p><ul>'+Object.entries(s.modifiers).map(([k,v])=>'<li class="'+(bad(k,v)?'kor-bad':'kor-good')+'">'+escape(D.modifier_labels[k]||k)+': '+val(k,v)+'</li>').join('')+'</ul><p>'+escape(s.resolution)+'</p></article>').join('');
  q('kor-events').innerHTML=D.transition_events.map(e=>'<article class="kor-spirit"><h4>'+escape(e.label)+'</h4><p>'+escape(e.historical_context)+'</p><p class="kor-meta">'+escape(e.trigger)+'</p><ul>'+e.choices.map(c=>'<li><strong>'+escape(c.label)+':</strong> '+escape(c.effects)+'</li>').join('')+'</ul></article>').join('');
  const decisionLabels={reopen_constitutional_talks:'Reopen Constitutional Talks',reopen_charter_ballot:'Resubmit the Charter',register_charter_endorsement:'Register a Party Endorsement',implement_constitutional_court:'Commission the Constitutional Court'};
  q('kor-decisions').innerHTML=D.transition_decisions.map(d=>'<article class="kor-spirit"><h4>'+escape(decisionLabels[d.id.replace('COLDWAR_KOR_','')]||d.id)+'</h4><p>'+escape(d.cost)+'</p><p>'+escape(d.reader)+'</p><details><summary>Exact decision requirements</summary><pre>'+escape(d.available)+'</pre></details></article>').join('')+'<article class="kor-spirit"><h4>Resolve the Command Challenge</h4><p>'+escape(D.proposed_transition_events['COLDWAR_KOR_transition.12'].resolution_mode)+'</p><p>'+escape(D.proposed_transition_events['COLDWAR_KOR_transition.12'].success_cost)+'</p></article>';
  q('kor-notes').innerHTML='<p>'+escape(D.layout.approximation)+'</p><p>'+escape(D.party_migration.confirmed_problem)+'</p><p>'+escape(D.party_migration.proposal)+'</p><p>'+escape(D.rules.lifecycle)+'</p><p>'+escape(D.rules.weekly)+'</p><p>Government and institutional-state shading are preview assumptions. Recipient responses, live capacity, prerequisites and actual engine state remain requirements in the inspector.</p>';
  q('kor-count').textContent=D.nodes.length+' focuses · '+D.expansion_summary.added+' added · 36 transition focuses';q('kor-spirits-heading').textContent='Starting national spirits · '+D.starting_spirits.length;
  q('kor-branch').addEventListener('change',e=>navigate(e.target.value));
  q('kor-government').addEventListener('change',e=>{government=e.target.value;availability();save();});
  q('kor-phase').addEventListener('change',e=>{phase=e.target.value;availability();save();});
  q('kor-overview').addEventListener('click',entire);q('kor-plus').addEventListener('click',()=>zoom(1.25));q('kor-minus').addEventListener('click',()=>zoom(.8));
  q('kor-native').addEventListener('click',()=>{const g=groups.get(branch);overview=false;scale=1;tx=view.clientWidth/2-(g.anchor[0]*96+82.5);ty=85;camera();save();});
  view.addEventListener('pointerdown',e=>{if(e.target.closest('button'))return;drag={x:e.clientX,y:e.clientY,tx,ty};view.setPointerCapture(e.pointerId);view.classList.add('dragging');});
  view.addEventListener('pointermove',e=>{if(!drag)return;tx=drag.tx+e.clientX-drag.x;ty=drag.ty+e.clientY-drag.y;camera();});
  view.addEventListener('pointerup',()=>{drag=null;view.classList.remove('dragging');save();});
  view.addEventListener('wheel',e=>{e.preventDefault();zoom(e.deltaY>0?.9:1.1);},{passive:false});
  new ResizeObserver(()=>{if(overview)entire(false);else camera();}).observe(view);
  availability();navigate('transition');entire(false);restore(window.openai?.widgetState);
  ready=true;
  window.addEventListener('openai:set_globals',e=>restore(e.detail?.globals?.widgetState));
})();
