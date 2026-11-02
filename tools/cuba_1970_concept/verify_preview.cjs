// IMPERIA COLD WAR — local approval preview QA; no game changes.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const out=path.resolve('docs/design/cuba_1970_concept');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1024,height:1400}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(out,'PREVIEW.html')).href);
 await page.locator('.cub-node').last().waitFor({state:'attached'});
 const design=JSON.parse(fs.readFileSync(path.join(out,'COLDWAR_CUB_1970_CONCEPT.json'),'utf8'));
 const views=[];
 for(const width of [320,736,1024]){
  await page.setViewportSize({width,height:1400});
  for(const g of design.groups){
   await page.locator('#cub-branch').selectOption(g.id);
   const info=await page.locator('#coldwar-cuba-concept').evaluate(r=>({overflow:r.scrollWidth>r.clientWidth+2,nodes:r.querySelectorAll('.cub-node').length,edges:r.querySelectorAll('.cub-prerequisite').length}));
   if(info.overflow||info.nodes!==design.nodes.length||info.edges!==design.nodes.reduce((s,n)=>s+n.prerequisites.flat().length,0))errors.push(width+' '+g.id+' '+JSON.stringify(info));
   const clipped=await page.locator('#cub-map').evaluate(map=>{const b=map.getBoundingClientRect();return [...map.querySelectorAll('.cub-node')].filter(n=>!n.hidden).filter(n=>{const r=n.getBoundingClientRect();return r.left<b.left-1||r.right>b.right+1||r.top<b.top-1||r.bottom>b.bottom+1}).map(n=>n.dataset.node)});
   if(clipped.length)errors.push('Fit clips '+width+' '+g.id+': '+clipped.join(','));
   views.push({width,group:g.id,...info});
  }
  await page.locator('#cub-starting').click();
  if(await page.locator('.cub-spirit').count()!==7)errors.push('missing spirits '+width);
  for(const panel of ['starting','agreements','timeline','rules']){
   await page.locator('#cub-'+panel).click();
   if(await page.locator('#coldwar-cuba-concept').evaluate(r=>r.scrollWidth>r.clientWidth+2))errors.push('overflow panel '+panel+' '+width);
  }
 }
 const inspected=await page.evaluate(()=>{const bad=[];for(const b of document.querySelectorAll('.cub-node')){b.click();if(document.querySelector('#cub-detail h2')?.textContent!==b.getAttribute('aria-label'))bad.push(b.dataset.node);}return bad;});
 errors.push(...inspected.map(x=>'failed focus inspector '+x));
 for(const g of design.groups.filter(g=>g.slot!==null)){
  await page.locator('#cub-government').selectOption(g.id);
  const invalid=await page.evaluate(({slot,nodes})=>nodes.filter(n=>document.querySelector('[data-node="'+n.id+'"]').classList.contains('is-locked')!==(n.slot!==null&&n.slot!==slot)).map(n=>n.id),{slot:g.slot,nodes:design.nodes.map(n=>({id:n.id,slot:n.slot}))});
  if(invalid.length)errors.push('government mismatch '+g.id+': '+invalid.join(','));
 }
 await page.locator('#cub-government').selectOption('pcc');
 await page.setViewportSize({width:1024,height:1400});
 for(const group of ['pcc','economy','society','defence','foreign','liberal','minint','ospaaal','juceplan']){
  await page.locator('#cub-branch').selectOption(group);
  await page.locator('[data-node="'+design.groups.find(g=>g.id===group).nodes[0]+'"]').evaluate(e=>e.click());
  await page.screenshot({path:path.join(out,'PREVIEW_'+group+'.png'),fullPage:true});
 }
 // Native-scale neighbour context for the expanded PCC footprint, independent of
 // the branch-only navigation view. Camera/art only; canonical coordinates stay fixed.
 await page.setViewportSize({width:1760,height:1500});
 await page.locator('#cub-branch').selectOption('pcc');
 await page.locator('#cub-native').click();
 await page.locator('[data-node="COLDWAR_CUB_popular_power"]').evaluate(e=>e.click());
 await page.locator('#cub-map').evaluate(e=>e.style.height='1100px');
 await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
 await page.locator('#cub-world').evaluate(w=>{
  w.style.transform='translate(-90px,-1260px) scale(1)';
  w.querySelectorAll('.cub-node').forEach(n=>{n.hidden=false;n.style.display='flex'});
  w.querySelectorAll('.cub-prerequisite,.cub-mex').forEach(p=>p.style.display='');
  w.querySelectorAll('.cub-exclusive-marker').forEach(p=>p.hidden=false);
 });
 await page.screenshot({path:path.join(out,'PREVIEW_pcc_neighbours.png'),fullPage:true});
 await page.locator('#cub-map').evaluate(e=>e.style.height='');
 await page.setViewportSize({width:1024,height:1400});
 await page.locator('#cub-branch').selectOption('pcc');
 await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
 await page.locator('[data-node="COLDWAR_CUB_biological_front"]').evaluate(e=>e.click());
 await page.screenshot({path:path.join(out,'PREVIEW_biological_front.png'),fullPage:true});
 // Zoom and drag must change only the camera, never native node coordinates.
 const before=await page.locator('#cub-world').evaluate(e=>({transform:e.style.transform,left:e.querySelector('.cub-node').style.left}));
 await page.locator('#cub-plus').click();
 const after=await page.locator('#cub-world').evaluate(e=>({transform:e.style.transform,left:e.querySelector('.cub-node').style.left}));
 if(before.transform===after.transform||before.left!==after.left)errors.push('zoom camera invalid');
 const box=await page.locator('#cub-map').boundingBox();
 await page.mouse.move(box.x+30,box.y+30);await page.mouse.down();await page.mouse.move(box.x+110,box.y+85);await page.mouse.up();
 if(after.transform===await page.locator('#cub-world').evaluate(e=>e.style.transform))errors.push('drag did not pan');
 await page.locator('#cub-branch').selectOption('foreign');
 await page.locator('[data-node="COLDWAR_CUB_caribbean_treaty"]').evaluate(e=>e.click());
 await page.locator('[data-contract="island_cession"]').click();
 const cession=await page.locator('#cub-detail').innerText();
 if(!cession.includes('State 1252')||!cession.includes('-0.40')||!cession.includes('Retain CUB core'))errors.push('cession terms incomplete');
 await page.screenshot({path:path.join(out,'PREVIEW_cession.png'),fullPage:true});
 await page.locator('#cub-overview').click();await page.screenshot({path:path.join(out,'PREVIEW_overview.png'),fullPage:true});
 await page.locator('#cub-starting').click();await page.screenshot({path:path.join(out,'PREVIEW_starting.png'),fullPage:true});
 const imageFailures=await page.locator('img').evaluateAll(imgs=>imgs.filter(i=>!i.complete||!i.naturalWidth).length);
 if(imageFailures)errors.push('broken images '+imageFailures);
 const report={errors,views:views.length,inspectors:design.nodes.length,governments:design.groups.filter(g=>g.slot!==null).length,imageFailures,details:views};
 fs.writeFileSync(path.join(out,'BROWSER_VALIDATION.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({errors,views:views.length,inspectors:design.nodes.length,governments:report.governments,imageFailures}));
 await browser.close();if(errors.length)process.exitCode=1;
})();
