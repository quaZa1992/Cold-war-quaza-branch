// IMPERIA COLD WAR — Argentina independent spatial fixture and full browser inspector verification.
const {chromium}=require('C:/Users/sonyz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url'),fs=require('fs'),path=require('path');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'});
 const page=await browser.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.setViewportSize({width:1180,height:1000});await page.goto(pathToFileURL(path.join(__dirname,'preview-review.html')).href);
 await page.locator('.ar-focus').first().waitFor();
 const data=await page.evaluate(()=>window.COLDWAR_ARG_PREVIEW.data),nodes=Object.fromEntries(data.nodes.map(n=>[n.id,n]));
 const missingArt=await page.locator('.ar-art').evaluateAll(imgs=>imgs.filter(im=>!im.complete||!im.naturalWidth).length);
 // Independently read emitted Clausewitz braces and resolve native relative_position_id.
 const txt=fs.readFileSync(path.join(__dirname,'proposal_graph_fixture.txt'),'utf8'),fixture={};
 const re=/\bfocus\s*=\s*\{/g;let m;
 while((m=re.exec(txt))){let depth=1,end=re.lastIndex;while(end<txt.length&&depth){if(txt[end]==='{')depth++;if(txt[end]==='}')depth--;end++}
  const block=txt.slice(re.lastIndex,end-1);re.lastIndex=end;const id=block.match(/\bid\s*=\s*(\w+)/)[1];
  const groups=[...block.matchAll(/prerequisite\s*=\s*\{([^}]+)\}/g)].map(m=>[...m[1].matchAll(/focus\s*=\s*(\w+)/g)].map(m=>m[1]));
  fixture[id]={x:+block.match(/\bx\s*=\s*(-?\d+)/)[1],y:+block.match(/\by\s*=\s*(-?\d+)/)[1],anchor:block.match(/relative_position_id\s*=\s*(\w+)/)?.[1],groups};
 }
 function resolve(id,seen=new Set()){if(seen.has(id))throw Error('Anchor cycle');seen.add(id);const n=fixture[id];if(!n)throw Error('Missing anchor '+id);const a=n.anchor?resolve(n.anchor,seen):{x:0,y:0};return{x:a.x+n.x,y:a.y+n.y}}
 const fixtureErrors=[];for(const n of data.nodes){const p=resolve(n.id);if(p.x!==n.x||p.y!==n.y||JSON.stringify(fixture[n.id].groups)!==JSON.stringify(n.prerequisites))fixtureErrors.push(n.id)}
 const chapters=await page.locator('#ar-chapter option').evaluateAll(opts=>opts.map(o=>o.value)),overlaps=[];
 for(const ch of chapters.filter(x=>x!=='all')){
  await page.locator('#ar-chapter').selectOption(ch);
  const bs=await page.locator('.ar-focus').evaluateAll(bs=>bs.map(b=>({id:b.dataset.id,x:parseFloat(b.style.left),y:parseFloat(b.style.top),w:165,h:128})));
  for(let i=0;i<bs.length;i++)for(let j=i+1;j<bs.length;j++){const a=bs[i],b=bs[j];if(Math.min(a.x+a.w,b.x+b.w)>Math.max(a.x,b.x)+1&&Math.min(a.y+a.h,b.y+b.h)>Math.max(a.y,b.y)+1)overlaps.push([a.id,b.id]);}
 }
 for(const n of data.nodes){
  await page.evaluate(id=>window.COLDWAR_ARG_PREVIEW.select(id),n.id);
  if(await page.locator('#ar-inspector h3').textContent()!==n.title)throw Error('Wrong inspector '+n.id);
  const text=await page.locator('#ar-inspector').innerText();
  if(!text.includes('Effects'))throw Error('Missing effects '+n.id);
  for(const [k,v]of Object.entries(n.modifiers)){const a=k==='interest_rate_multiplier_modifier'?v:v*100;const exact=(a>0?'+':'')+Number(a.toFixed(4))+(k==='interest_rate_multiplier_modifier'?' pp':'%');if(!text.includes(exact))throw Error('Missing signed focus modifier '+n.id+' '+k)}
  if(n.decision&&!text.includes(data.decisions.find(d=>d.key===n.decision).title))throw Error('Missing decision contract');
 }
 const agreementTerms=[];
 await page.evaluate(()=>window.COLDWAR_ARG_PREVIEW.select('rosario_plan'));
 const rosario=data.nodes.find(n=>n.key==='rosario_plan');
 if(rosario.wargoal?.type!=='take_state_focus'||rosario.wargoal.target!=='ENG'||JSON.stringify(rosario.wargoal.states)!=='[26]'||rosario.wargoal.expire!==730||rosario.decision)throw Error('Rosario must grant the Falklands war goal directly');
 const rosarioEffects=await page.locator('#ar-inspector>ul').last().innerText();
 if(!rosarioEffects.includes('Gain Take State war goal against the United Kingdom: Falkland Islands (730 days)'))throw Error('Missing native prospective war goal effect');
 if(rosario.proposed_code.includes('declare_war_on')||data.decisions.some(d=>d.key==='rosario'))throw Error('Unexpected automatic Rosario war declaration');
 for(const a of data.agreements){
  await page.evaluate(id=>window.COLDWAR_ARG_PREVIEW.select(id),a.focus);
  if(!(await page.locator('#ar-inspector').innerText()).includes('If they accept'))throw Error('Missing conditional agreement preview');
  const sides=await page.locator('.ar-terms section').all();if(sides.length!==2)throw Error('Missing agreement side');
  for(let i=0;i<2;i++){
   const t=a[i===0?'argentina':'recipient'],text=await sides[i].innerText();
   for(const f of ['setup','weekly','credit','grant'])if(t[f]&&!text.includes('$'+Math.abs(t[f]).toFixed(5).replace(/0{1,2}$/,'')+' billion'))throw Error('Missing agreement money '+a.id+' '+f);
   for(const [k,v]of Object.entries(t.modifiers)){const av=k==='interest_rate_multiplier_modifier'?v:v*100;const exact=(av>0?'+':'')+Number(av.toFixed(4))+(k==='interest_rate_multiplier_modifier'?' pp':'%');if(!text.includes(exact))throw Error('Missing agreement modifier '+a.id+' '+k)}
   const tag=i===0?'ARG':a.partner;for(const b of a.buildings.filter(b=>b.country===tag))if(!text.includes(data.states[b.state])||!text.includes('+'+b.slots+' shared building slot'))throw Error('Missing exact state/slot '+a.id);
   for(const r of a.research.filter(r=>r.country===tag))if(!text.includes(r.uses+' x '+Math.round(r.bonus*100)+'% research bonus'))throw Error('Missing acceptance research '+a.id);
   if(a.territory&&(!text.includes(data.states[a.territory.state])||!text.includes('state ownership')))throw Error('Missing acceptance territorial effect '+a.id);
  }
  agreementTerms.push({id:a.id,allMoneyModifiersBuildingsResearchVisible:true,sides:2});
 }
 await page.locator('#ar-events').click();for(const ev of data.events){await page.locator('#ar-event').selectOption(ev.key);if(await page.locator('.ar-choice').count()!==ev.options.length)throw Error('Event option coverage '+ev.key)}
 const governmentVariants=[];
 for(const gov of Object.keys(data.parties)){await page.locator('#ar-government').selectOption(gov);await page.locator('#ar-chapter').selectOption('all');governmentVariants.push({government:gov,count:await page.locator('.ar-focus').count()});}
 await page.locator('#ar-government').selectOption('22');
 const geometry=await page.evaluate(()=>{
  const cards=[...document.querySelectorAll('.ar-focus')].map(b=>({id:b.dataset.id,x:parseFloat(b.style.left),y:parseFloat(b.style.top),w:165,h:128})),collisions=[];
  for(const edge of document.querySelectorAll('#ar-edges path[data-parent]')){
   const [x1,y1,ym,x2,y2]=edge.getAttribute('d').match(/-?\d+(?:\.\d+)?/g).map(Number),segments=[[x1,y1,x1,ym],[x1,ym,x2,ym],[x2,ym,x2,y2]];
   for(const c of cards){if(c.id===edge.dataset.parent||c.id===edge.dataset.child)continue;
    const hit=segments.some(([ax,ay,bx,by])=>ax===bx?(ax>c.x&&ax<c.x+c.w&&Math.max(ay,by)>c.y&&Math.min(ay,by)<c.y+c.h):(ay>c.y&&ay<c.y+c.h&&Math.max(ax,bx)>c.x&&Math.min(ax,bx)<c.x+c.w));
    if(hit)collisions.push({parent:edge.dataset.parent,child:edge.dataset.child,card:c.id});
   }
  }
  const exclusiveArtCollisions=[];
  for(const edge of document.querySelectorAll('#ar-edges path[data-exclusive]')){
   const [x,y,x2]=edge.getAttribute('d').match(/-?\d+(?:\.\d+)?/g).map(Number);
   for(const c of cards)if(y>c.y&&y<c.y+128&&Math.max(x,x2)>c.x+.5&&Math.min(x,x2)<c.x+164.5)exclusiveArtCollisions.push({pair:edge.dataset.exclusive,card:c.id});
  }
  return {links:document.querySelectorAll('#ar-edges path[data-parent]').length,collisions,exclusiveArtCollisions,titleOverflow:[...document.querySelectorAll('.ar-title>span')].filter(s=>s.scrollWidth>s.clientWidth||s.scrollWidth>147).map(s=>s.textContent)};
 });
 const responsive=[];
 for(const width of [1180,736,360]){await page.setViewportSize({width,height:1000});await page.evaluate(()=>window.COLDWAR_ARG_PREVIEW.select('army_directives'));const r=await page.evaluate(()=>({client:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}));responsive.push({width,...r});if(width===360)await page.screenshot({path:path.join(__dirname,'preview-mobile.png'),fullPage:true});}
 await page.setViewportSize({width:1180,height:1000});
 for(const [key,name]of [['army_directives','military'],['social_pact','pj'],['sovereignty_dossier','falklands'],['rosario_plan','rosario-wargoal'],['soviet_grain','agreement'],['sovereignty_treaty','sovereignty'],['uranium_development','uranium']]){await page.evaluate(id=>window.COLDWAR_ARG_PREVIEW.select(id),key);await page.screenshot({path:path.join(__dirname,'preview-'+name+'.png'),fullPage:true});}
 await page.locator('#ar-spirits').click();await page.locator('#ar-inspector').screenshot({path:path.join(__dirname,'preview-starting-spirits.png')});
 await page.evaluate(()=>window.COLDWAR_ARG_PREVIEW.overview());await page.locator('.ar-viewport').screenshot({path:path.join(__dirname,'preview-overview.png')});
 const report={project:'IMPERIA COLD WAR',focusInspectors:data.nodes.length,eventInspectors:data.events.length,rosarioWarGoal:{target:'ENG',states:[26],type:'take_state_focus',expire:730,visibleInEffects:true,automaticDeclaration:false},agreementTerms,fixtureErrors,missingArt,overlaps,geometry,governmentVariants,responsive,errors,engineTested:false};
 fs.writeFileSync(path.join(__dirname,'BROWSER_QA.json'),JSON.stringify(report,null,2)+'\n');await browser.close();console.log(JSON.stringify(report));
 if(errors.length||fixtureErrors.length||missingArt||overlaps.length||geometry.collisions.length||geometry.exclusiveArtCollisions.length||geometry.titleOverflow.length||responsive.some(r=>r.scroll>r.client+1)||governmentVariants.some(v=>v.count!==data.nodes.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
