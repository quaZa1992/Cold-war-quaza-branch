// IMPERIA COLD WAR — France concept browser interaction verification.
const { chromium }=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url'),crypto=require('crypto');
const out=path.resolve('tools/france_1970_design');
const viz='C:/Users/Enes/.codex/visualizations/2026/10/28/01a183df-ceae-74b3-b1f4-d519f043ee74';
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1024,height:1500}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(out,'PREVIEW.html')).href);
 await page.locator('.fr-focus').last().waitFor();
 const d=JSON.parse(fs.readFileSync(path.join(out,'concept.json'),'utf8'));
 const views=[];
 for(const width of [320,736,1024]){
  await page.setViewportSize({width,height:1500});
  for(const panel of ['tree','start','agreements','course']){
   await page.locator('[data-panel="'+panel+'"]').click();
   const state=await page.locator('#france-concept').evaluate(r=>({overflow:r.scrollWidth>r.clientWidth+2,brokenImages:[...r.querySelectorAll('img')].filter(i=>!i.complete||!i.naturalWidth).length}));
   if(state.overflow||state.brokenImages)errors.push({width,panel,...state});
  }
  await page.locator('[data-panel="tree"]').click();
  for(const g of d.groups){
   await page.locator('#fr-section').selectOption(g.id);
   const fit=await page.locator('#fr-map').evaluate((map,group)=>{const b=map.getBoundingClientRect();return [...map.querySelectorAll('.fr-focus')].filter(n=>window.franceConcept.data.nodes.find(f=>f.key===n.dataset.key).group===group).filter(n=>{const t=n.getBoundingClientRect();return t.left<b.left-1||t.right>b.right+1||t.top<b.top-1||t.bottom>b.bottom+1;}).map(n=>n.dataset.key);},g.id);
   if(fit.length)errors.push({width,group:g.id,clipped:fit});
   views.push({width,group:g.id,fit:fit.length===0});
  }
 }
 await page.setViewportSize({width:1024,height:1500});
 const clicks=await page.evaluate(()=>{const errors=[];for(const b of document.querySelectorAll('.fr-focus')){const before=JSON.stringify(window.franceConcept.getView());b.click();const h=document.querySelector('#fr-details h2');if(h.textContent!==b.getAttribute('aria-label'))errors.push(b.dataset.key);const a=JSON.parse(before),v=window.franceConcept.getView();if(a.tx!==v.tx||a.ty!==v.ty||a.z!==v.z)errors.push('click moved map: '+b.dataset.key);}return errors;});errors.push(...clicks);
 for(const g of d.groups.filter(g=>g.slot!==null&&!g.governing_group)){
  await page.locator('#fr-government').selectOption(g.id);
  const bad=await page.evaluate(g=>[...document.querySelectorAll('.fr-focus')].filter(b=>{const n=window.franceConcept.data.nodes.find(n=>n.key===b.dataset.key),gr=window.franceConcept.data.groups.find(g=>g.id===n.group),gov=window.franceConcept.data.groups.find(a=>a.id===g);return b.classList.contains('is-locked')!==(gr.slot!==null&&gr.slot!==gov.slot);}).map(b=>b.dataset.key),g.id);
  errors.push(...bad.map(k=>'government '+g.id+' '+k));
 }
 const offerChecks=await page.evaluate(()=>window.franceConcept.data.nodes.filter(n=>n.offer).map(n=>{window.franceConcept.inspect(n.key);const text=document.querySelector('#fr-details').textContent,ef=[...n.effects,...n.offer.france.effects,...n.offer.recipient.effects];const weeklyPrecise=ef.filter(e=>e.kind==='weekly_gdp_expense').every(e=>text.includes('('+Number(e.annual_gdp_percent.toFixed(5))+'% of current GDP) ÷ 52'));const gdpPrecise=ef.filter(e=>e.kind==='treasury_gdp').every(e=>text.includes(Number(Math.abs(e.percent).toFixed(5))+'% of current GDP'));return {key:n.key,both:text.includes('If they accept')&&text.includes(n.offer.france.name)&&text.includes(n.offer.recipient.name),weeklyPrecise,gdpPrecise,effectRows:document.querySelectorAll('#fr-details .fr-effects li').length,expected:ef.reduce((s,e)=>s+(e.kind==='building'?2:1),0)};}));
 errors.push(...offerChecks.filter(x=>!x.both||!x.weeklyPrecise||!x.gdpPrecise||x.effectRows!==x.expected));
 const allEffectChecks=await page.evaluate(()=>{const issues=[];for(const n of window.franceConcept.data.nodes){window.franceConcept.inspect(n.key);const rows=[...document.querySelectorAll('#fr-details .fr-effects li')];if(rows.some(r=>!r.textContent.trim()))issues.push('empty effect '+n.key);for(const b of document.querySelectorAll('[data-asset-build]'))if(b.previousElementSibling?.dataset.assetSlot!==b.dataset.assetBuild)issues.push('slot order '+n.key);for(const e of n.effects)if(['treasury','weekly_expense'].includes(e.kind))issues.push('flat money '+n.key);}return issues;});errors.push(...allEffectChecks);
 const titleFlags=await page.evaluate(()=>{const ctx=document.createElement('canvas').getContext('2d');ctx.font='15px Arial';return window.franceConcept.data.nodes.map(n=>({key:n.key,title:n.title,width:ctx.measureText(n.title).width})).filter(n=>n.width>147);});
 errors.push(...titleFlags.map(n=>({title_overflow:n})));
 await page.locator('#fr-government').selectOption('udr');await page.locator('#fr-section').selectOption('udr');
 await page.evaluate(()=>window.franceConcept.inspect('progress'));
 await page.locator('#fr-native').click();
 const target=page.locator('[data-key="progress"]');await target.click();
 const before=await page.evaluate(()=>window.franceConcept.getView());
 const box=await page.locator('#fr-map').boundingBox();await page.mouse.move(box.x+20,box.y+20);await page.mouse.down();await page.mouse.move(box.x+85,box.y+65,{steps:4});await page.mouse.up();
 const after=await page.evaluate(()=>window.franceConcept.getView());if(Math.abs(after.tx-before.tx)<20)errors.push('Pan did not move map');
 await page.locator('#fr-more').click();if((await page.evaluate(()=>window.franceConcept.getView())).z<=after.z)errors.push('Zoom in did not increase zoom');
 const screenshots=[];
 for(const [section,key] of [['udr_nato','nato_nuclear_consult'],['udr','participation'],['economy','nuclear_scale'],['diplomacy','airbus'],['overview','progress']]){
  await page.locator('#fr-section').selectOption(section);await page.evaluate(k=>window.franceConcept.inspect(k),key);
  const filename='france-'+section+'.png';await page.locator('#france-concept').screenshot({path:path.join(viz,filename)});screenshots.push(filename);
 }
 await page.locator('[data-panel="start"]').click();await page.locator('#france-concept').screenshot({path:path.join(viz,'france-start.png')});
 const report={project:'IMPERIA COLD WAR',kind:'Local browser verification; no HOI4 engine test',concept_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(out,'concept.json'))).digest('hex'),focus_clicks:d.nodes.length,government_states:d.groups.filter(g=>g.slot!==null&&!g.governing_group).length,widths:[320,736,1024],fit_views:views,offers:offerChecks,pan_zoom:true,title_flags:titleFlags,errors,screenshots};
 fs.writeFileSync(path.join(out,'BROWSER_QA.json'),JSON.stringify(report,null,2));await browser.close();console.log(JSON.stringify({focuses:d.nodes.length,offers:offerChecks.length,views:views.length,errors}));if(errors.length)process.exit(1);
})();
