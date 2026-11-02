// IMPERIA COLD WAR — SSR concept browser verification.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),crypto=require('crypto'),{pathToFileURL}=require('url');
const out=path.resolve('docs/design/ssr_1970_concept');
const expectedCountries=14;
const ratios={benefit:.2,cost:.75};
(async()=>{
 const html=path.join(out,'PREVIEW.html');
 if(!fs.existsSync(html))throw Error('Missing current v2 build: '+html);
 const htmlHash=crypto.createHash('sha256').update(fs.readFileSync(html)).digest('hex');
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1024,height:1500}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(html).href);
 await page.waitForFunction(()=>document.getElementById('coldwar-ssr-concept').ssrQA);
 const root=page.locator('#coldwar-ssr-concept');
 const countries=await page.locator('#ssr-country option').evaluateAll(es=>es.map(e=>e.value));
 if(countries.length!==expectedCountries)errors.push('Country coverage '+countries.length);
 let inspected=0,exclusiveInspected=0,offerInspected=0,partyGateChecks=0,ssrStatusChecks=0,landlockedNavyLocked=0;
 const countryReport={};
 for(const country of countries){
  await page.locator('#ssr-country').selectOption(country);
  const inspect=await root.evaluate(el=>{
   const q=el.ssrQA,d=q.data.models[q.state.country],bad=[];let count=0,exclusive=0,offers=0;
   for(const n of [...d.nodes,...q.data.external]){
    const b=el.querySelector('[data-node="'+n.id+'"]');
    if(!b){bad.push('Missing inspector node '+n.id);continue;}
    b.click();count++;
    if(el.querySelector('#ssr-detail h2')?.textContent!==n.title)bad.push('Inspector title '+n.id);
    const detail=el.querySelector('#ssr-detail').textContent;
    if(n.exclusive?.length){exclusive++;for(const id of n.exclusive){const alt=[...d.nodes,...q.data.external].find(x=>x.id===id);if(!alt||!detail.includes(alt.title))bad.push('Exclusive alternative missing '+n.id+' -> '+id);}}
    if(n.action?.startsWith('offer:')){
     offers++;const t=q.data.contracts[n.action.slice(6)];
     if(!detail.includes('If they accept')||!detail.includes(t.origin.spirit)||!detail.includes(t.recipient.spirit)||!detail.includes('of GDP'))bad.push('Incomplete acceptance preview '+n.id);
     for(const side of [t.origin,t.recipient])for(const k of Object.keys(side.modifiers))if(!detail.includes(q.data.labels[k]))bad.push('Offer modifier missing '+n.id+' '+k);
    }
   }
   return {bad,count,exclusive,offers,nodeCount:d.nodes.length,partyCount:d.profile.parties.length,tag:d.profile.tag};
  });
  errors.push(...inspect.bad);inspected+=inspect.count;exclusiveInspected+=inspect.exclusive;offerInspected+=inspect.offers;
  const gate=await page.locator('#coldwar-ssr-concept').evaluate(el=>{
   const q=el.ssrQA,d=q.data.models[q.state.country],bad=[];let checks=0,ssrChecks=0,navy=0;
   const partyNodes=d.nodes.filter(n=>n.phase==='party');
   for(const p of d.profile.parties){
    const slot=String(p.slot);
    const status=el.querySelector('#ssr-status'),gov=el.querySelector('#ssr-government');
    status.value='independent';status.dispatchEvent(new Event('change',{bubbles:true}));
    gov.value=slot;gov.dispatchEvent(new Event('change',{bubbles:true}));
    for(const n of partyNodes){
     const b=el.querySelector('[data-node="'+n.id+'"]');const locked=b.classList.contains('is-locked');
     const expected=Number(n.gate.slice(4))!==Number(slot);
     if(locked!==expected)bad.push('Party gate '+n.id+' for '+slot);
     checks++;
    }
    status.value='ssr';status.dispatchEvent(new Event('change',{bubbles:true}));
    for(const n of d.nodes.filter(n=>n.phase==='ssr')){
     const b=el.querySelector('[data-node="'+n.id+'"]');const locked=b.classList.contains('is-locked');
     const geography=n.geography==='naval_coast'&&d.profile.sea_context==='Landlocked';
     if(geography)navy++;
     if(locked!==geography)bad.push('SSR status/party gate '+n.id+' selected slot '+slot+' locked='+locked+' expectedGeography='+geography);
     ssrChecks++;
    }
   }
   const status=el.querySelector('#ssr-status');status.value='independent';status.dispatchEvent(new Event('change',{bubbles:true}));
   for(const n of d.nodes.filter(n=>n.phase==='ssr')){
    const b=el.querySelector('[data-node="'+n.id+'"]');const locked=b.classList.contains('is-locked');
    if(!locked)bad.push('SSR focus available after independence '+n.id);
   }
   return {bad,checks,ssrChecks,navy,partyNodes:partyNodes.length,partySlots:d.profile.parties.map(p=>p.slot),sea:d.profile.sea_context};
  });
  errors.push(...gate.bad);partyGateChecks+=gate.checks;ssrStatusChecks+=gate.ssrChecks;landlockedNavyLocked+=gate.navy;
  countryReport[country]={inspectors:inspect.count,nodes:inspect.nodeCount,partyNodes:gate.partyNodes,partySlots:gate.partySlots,sea:gate.sea,partyGateChecks:gate.checks,ssrStatusChecks:gate.ssrChecks,landlockedNavy:gate.navy};
  if(gate.sea==='Landlocked'&&gate.navy===0)errors.push('No locked naval-coast focuses for landlocked '+country);
 }
 // All nine specialisation comparisons, all four direction/administration combinations.
 await page.locator('#ssr-country').selectOption('UKR');
 await page.locator('#ssr-status').selectOption('ssr');
 await page.locator('#ssr-specialisations').click();
 const specAudit=await root.evaluate(el=>{
  const q=el.ssrQA,m=q.data.models[q.state.country],groups=m.groups.filter(g=>g.specialisation),bad=[];let ratio20=0,ratio75=0,comparisons=0,universalCountries=0,historicalDescriptions=0;
  for(const [tag,model] of Object.entries(q.data.models)){
   const gs=model.groups.filter(g=>g.specialisation);
   if(gs.length!==9)bad.push('Universal programme coverage '+tag+': '+gs.length);
   else universalCountries++;
   for(const g of gs){
    const root=model.nodes.find(n=>n.specialisation===g.specialisation&&n.key.endsWith('_mandate'));
    if(!root||!root.historical_basis?.includes('Universally selectable'))bad.push('Universal history anchor '+tag+' '+g.specialisation);
    if(!root||!root.description.includes('Historical precedent:')||!root.description.trim().endsWith('.')||root.description.indexOf('Historical precedent:')<root.description.lastIndexOf('Historical precedent:'))bad.push('Historical reference placement '+tag+' '+g.specialisation);
    else historicalDescriptions++;
   }
   for(const n of model.nodes.filter(n=>n.specialisation))for(const [k,v] of Object.entries(n.modifiers||{})){
    const legacy=n.legacy_modifiers?.[k];if(!v||!legacy)continue;
    const r=Math.round((legacy/v)*10000)/10000;
    if(Math.abs(r-.2)<.0001)ratio20++;else if(Math.abs(r-.75)<.0001)ratio75++;else bad.push('Programme legacy ratio '+tag+' '+n.key+' '+k+' '+r);
   }
  }
  if(groups.length!==9)bad.push('Expected nine rendered programmes, found '+groups.length);
  for(const g of groups){
   const button=el.querySelector('[data-programme="'+g.specialisation+'"]');
   if(!button){bad.push('Missing programme comparison '+g.specialisation);continue;}
   button.click();
   for(const direction of ['left','right'])for(const admin of ['efficiency','priority']){
    const d=el.querySelector('#ssr-spec-direction'),a=el.querySelector('#ssr-spec-admin');d.value=direction;d.dispatchEvent(new Event('change',{bubbles:true}));a.value=admin;a.dispatchEvent(new Event('change',{bubbles:true}));
    const text=el.querySelector('#ssr-spec-results').textContent;
    if(!text.includes('Within the Union')||!text.includes('After independence')||!text.includes('Weekly programme budget')||!text.includes('% of GDP'))bad.push('Incomplete comparison '+g.specialisation+' '+direction+' '+admin);
    comparisons++;
   }
  }
  const visibleText=el.querySelector('#ssr-detail').textContent;if(!visibleText.includes('Every republic can choose any of the nine programmes'))bad.push('Missing universal programme statement');
  return {bad,programmes:groups.map(g=>g.specialisation),comparisons,ratio20,ratio75,universalCountries,historicalDescriptions};
 });
 errors.push(...specAudit.bad);
 await page.locator('#ssr-specialisations').click();
 await page.screenshot({path:path.join(out,'PREVIEW_V2_SPECIALISATIONS.png'),fullPage:true});
 await page.locator('[data-programme="industry"]').click();
 await page.screenshot({path:path.join(out,'PREVIEW_V2_COMPARISON.png'),fullPage:true});
 await page.locator('#ssr-chapter').selectOption('spec_industry');
 await page.screenshot({path:path.join(out,'PREVIEW_V2_SPECIAL_BRANCH.png'),fullPage:true});
 // Three market courses: raw growth values, 730-day windows, fiscal spans, GDP-only prices.
 await page.locator('#ssr-market').click();
 const marketCourses=await page.locator('#ssr-market-course option').evaluateAll(es=>es.map(e=>e.value));
 const courseAudit=[];
 for(const course of marketCourses){
  await page.locator('#ssr-market-course').selectOption(course);
  const check=await root.evaluate(el=>{
   const q=el.ssrQA,c=q.data.market.courses[el.querySelector('#ssr-market-course').value],text=el.querySelector('#ssr-market-effects').textContent;
   const growth=c.window.modifiers.productivity_growth_modifier;
   return {name:c.name,windowDays:c.window.days,fiscalDays:c.fiscal.days,growth,gdpCost:c.gdp_cost,weekly:c.weekly_gdp_cost,
    has730:text.includes('(730 days)'),hasGDP:text.includes('% of GDP'),hasRawGrowth:text.includes(q.data.labels.productivity_growth_modifier+' +'+growth.toFixed(3))};
  });
  courseAudit.push(check);
  if(check.windowDays!==730||check.fiscalDays!==730||!check.has730||!check.hasGDP||!check.hasRawGrowth)errors.push('Market course display '+course);
  const expected={shock:1.2,gradual:.4,directed:.3}[course];
  if(Math.abs(check.growth-expected)>1e-8)errors.push('Market raw growth '+course+' '+check.growth+' expected '+expected);
 }
 if(!marketCourses.includes('shock')||!marketCourses.includes('gradual')||!marketCourses.includes('directed'))errors.push('Missing market course options');
 await page.locator('#ssr-market-course').selectOption('shock');
 await page.screenshot({path:path.join(out,'PREVIEW_V2_MARKET.png'),fullPage:true});
 const methodAudit=[];
 for(const method of ['auction','workers','public','liquidate']){
  for(const sel of await page.locator('[data-lot]').all())await sel.selectOption(method);
  const result=await root.evaluate(el=>({text:el.querySelector('#ssr-lot-result').textContent,detail:el.querySelector('#ssr-method-detail').textContent}));
  const loss=method==='liquidate'?6:0;
  if(!result.text.includes('Projected settlement: 6 / 6 sectors')||!result.text.includes('Civilian factory levels '+(loss?'-'+loss:'0')))errors.push('Lot simulation '+method+' '+result.text);
  if(!result.detail.includes('% of GDP')||/[€£$]|\b(?:USD|EUR)\b/.test(result.detail))errors.push('GDP-only lot price '+method);
  if(method==='liquidate'&&!result.detail.includes('Civilian factory -1'))errors.push('Liquidation per-project factory closure');
  if(method!=='liquidate'&&result.detail.includes('Civilian factory -1'))errors.push('Sale unexpectedly closes a factory '+method);
  methodAudit.push({method,sectors:6,civilianFactoryLoss:loss,detailHasGDP:result.detail.includes('% of GDP')});
 }
 const marketText=await page.locator('#ssr-detail').innerText();
 if(/[€£$]|\b(?:USD|EUR)\b/.test(marketText))errors.push('Non-GDP currency in market panel');
 // Responsive panels and transition settlement variants.
 const widths=[320,736,1024],panelIds=['specialisations','market','start','transition','politics','rules'];
 for(const width of widths){
  await page.setViewportSize({width,height:1500});
  for(const id of panelIds){
   await page.locator('#ssr-'+id).click();
   const overflow=await page.evaluate(()=>({doc:document.documentElement.scrollWidth>window.innerWidth+1,root:(()=>{const e=document.getElementById('coldwar-ssr-concept');return e.scrollWidth>e.clientWidth+1;})()}));
   if(overflow.doc||overflow.root)errors.push('Outer overflow '+width+' '+id+' '+JSON.stringify(overflow));
  }
  await page.locator('#ssr-transition').click();
  for(const mode of ['abrupt','prepared','negotiated']){
   await page.locator('#ssr-case').selectOption(mode);
   if(await page.locator('#ssr-transition-spirits .ssr-spirit').count()!==3)errors.push('Transition spirit count '+mode);
  }
  await page.locator('#ssr-start').click();
  if(await page.locator('.ssr-spirit').count()!==5)errors.push('Starting spirits');
 }
 // Native zoom, blank-map pan and pointer click on a focus in the visible chapter.
 await page.setViewportSize({width:1024,height:1500});
 await page.locator('#ssr-country').selectOption('UKR');
 await page.locator('#ssr-status').selectOption('independent');
 await page.locator('#ssr-government').selectOption('20');
 await page.locator('#ssr-chapter').selectOption('party_20');
 await page.locator('#ssr-map').scrollIntoViewIfNeeded();
 await page.locator('#ssr-native').click();
 const beforeZoom=await root.evaluate(el=>el.ssrQA.state.z);
 await page.locator('#ssr-plus').click();
 if(await root.evaluate(el=>el.ssrQA.state.z)===beforeZoom)errors.push('Zoom failed');
 const mapBox=await page.locator('#ssr-map').boundingBox();
 const panPoint=await page.evaluate(({x,y,w,h})=>{
  for(const [dx,dy] of [[10,12],[w-12,12],[12,h-12],[w-12,h-12],[w/2,12],[w-12,h/2]]){
   const e=document.elementFromPoint(x+dx,y+dy);if(e&&!e.closest('#ssr-map button'))return{x:x+dx,y:y+dy};
  }return null;
 },{x:mapBox.x,y:mapBox.y,w:mapBox.width,h:mapBox.height});
 if(!panPoint)errors.push('No blank map point for pan');
 else{
  const beforePan=await root.evaluate(el=>el.ssrQA.state.tx+','+el.ssrQA.state.ty);
  await page.mouse.move(panPoint.x,panPoint.y);await page.mouse.down();await page.mouse.move(panPoint.x+65,panPoint.y+35);await page.mouse.up();
  if(beforePan===await root.evaluate(el=>el.ssrQA.state.tx+','+el.ssrQA.state.ty))errors.push('Pan failed');
  if(await page.evaluate(()=>window.getSelection()?.toString().length>0))errors.push('Pan selected page content');
 }
 const target=await root.evaluate(el=>{
  const q=el.ssrQA,m=q.data.models[q.state.country],n=m.nodes.find(n=>n.phase==='party'&&n.gate==='slot20'&&n.key.endsWith('_root'));
  const b=el.querySelector('[data-node="'+n.id+'"]'),r=b.getBoundingClientRect();return{id:n.id,title:n.title,x:r.x+r.width/2,y:r.y+r.height/2};
 });
 const viewport=await page.evaluate(()=>({width:window.innerWidth,height:window.innerHeight}));
 if(target.x<0||target.y<0||target.x>viewport.width||target.y>viewport.height)errors.push('Pointer target outside viewport '+JSON.stringify(target));
 else{await page.mouse.click(target.x,target.y);if(await page.locator('#ssr-detail h2').innerText()!==target.title)errors.push('Native pointer click '+target.id);}
 // Independent party-route references for OUN-M, ARF and Hunchak.
 async function partyShot(country,slot,name){
  await page.locator('#ssr-country').selectOption(country);await page.locator('#ssr-status').selectOption('independent');await page.locator('#ssr-government').selectOption(String(slot));await page.locator('#ssr-chapter').selectOption('party_'+slot);
  const node=await root.evaluate((el,slot)=>{const m=el.ssrQA.data.models[el.ssrQA.state.country],n=m.nodes.find(n=>n.phase==='party'&&n.gate==='slot'+slot&&n.key.endsWith('_root'));return n&&{id:n.id,title:n.title};},slot);
  if(!node){errors.push('Missing independent party root '+country+' slot '+slot);return;}
  await root.locator('[data-node="'+node.id+'"]').evaluate(e=>e.click());
  if(await page.locator('#ssr-detail h2').innerText()!==node.title)errors.push('Party root inspector '+country+' '+slot);
  await page.screenshot({path:path.join(out,name),fullPage:true});
 }
 await partyShot('UKR',20,'PREVIEW_V2_INDEP_OUN_M.png');
 await partyShot('ARM',0,'PREVIEW_V2_INDEP_ARF.png');
 await partyShot('ARM',18,'PREVIEW_V2_INDEP_HUNCHAK.png');
 const images=await page.locator('img').evaluateAll(es=>es.filter(e=>!e.complete||!e.naturalWidth).length);
 if(images)errors.push('Broken images '+images);
 const report={project:'IMPERIA COLD WAR',revision:'SSR concept v2',preview:'PREVIEW.html',preview_sha256:htmlHash,
  errors,countries:countries.length,inspectors:inspected,exclusive_inspectors:exclusiveInspected,offer_previews:offerInspected,
  party_gate_checks:partyGateChecks,ssr_status_checks:ssrStatusChecks,landlocked_naval_locks:landlockedNavyLocked,
  country_report:countryReport,specialisation_audit:specAudit,market_courses:courseAudit,market_lot_methods:methodAudit,
  widths,panel_ids:panelIds,broken_images:images,screenshots:['PREVIEW_V2_SPECIALISATIONS.png','PREVIEW_V2_COMPARISON.png','PREVIEW_V2_SPECIAL_BRANCH.png','PREVIEW_V2_MARKET.png','PREVIEW_V2_INDEP_OUN_M.png','PREVIEW_V2_INDEP_ARF.png','PREVIEW_V2_INDEP_HUNCHAK.png'],checked_at:new Date().toISOString()};
 fs.writeFileSync(path.join(out,'BROWSER_CHECKS.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report));await browser.close();if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
