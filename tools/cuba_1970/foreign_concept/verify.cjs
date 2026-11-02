// IMPERIA COLD WAR — browser checks for the proposed foreign focus tree.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const out=path.resolve('docs/design/cuba_foreign_1970');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1024,height:1500}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(out,'PREVIEW.html')).href);
 await page.locator('.fp-node').last().waitFor({state:'attached'});
 const design=JSON.parse(fs.readFileSync(path.join(out,'FOREIGN_POLICY_CONCEPT.json'),'utf8'));
 const views=[];
 for(const width of [320,736,1024]){
  await page.setViewportSize({width,height:1500});
  for(const v of [...design.foreign_views,{id:'context'}]){
   await page.locator('#fp-view').selectOption(v.id);
   const stats=await page.locator('#cuba-foreign-proposal').evaluate(r=>({overflow:r.scrollWidth>r.clientWidth+1,nodes:r.querySelectorAll('.fp-node').length,visible:[...r.querySelectorAll('.fp-node')].filter(n=>!n.hidden).length}));
   if(stats.overflow||stats.nodes!==120)errors.push({width,view:v.id,...stats});
   const clipped=await page.locator('#fp-map').evaluate(m=>{const b=m.getBoundingClientRect();return [...m.querySelectorAll('.fp-node')].filter(n=>!n.hidden).filter(n=>{const a=n.getBoundingClientRect();return a.left<b.left-1||a.right>b.right+1||a.top<b.top-1||a.bottom>b.bottom+1}).map(n=>n.dataset.node)});
   if(clipped.length)errors.push({width,view:v.id,clipped});
   views.push({width,view:v.id,...stats});
  }
  for(const panel of ['contract','budget']){
   await page.locator('#fp-'+panel).click();
   if(await page.locator('#cuba-foreign-proposal').evaluate(r=>r.scrollWidth>r.clientWidth+1))errors.push('panel overflow '+panel+' '+width);
  }
 }
 const bad=await page.evaluate(()=>{const bad=[];for(const b of document.querySelectorAll('.fp-node')){b.click();if(document.querySelector('#fp-detail h2')?.textContent!==b.getAttribute('aria-label'))bad.push(b.dataset.node)}return bad});
 errors.push(...bad.map(x=>'inspector '+x));
 await page.setViewportSize({width:1024,height:1500});
 for(const view of ['foreign','trade','atlantic','missions','context']){
  await page.locator('#fp-view').selectOption(view);
  await page.locator('[data-node="COLDWAR_CUB_foreign_'+(view==='missions'?'expeditionary':view==='atlantic'?'cession':'sov_industry')+'"]').evaluate(n=>n.click());
  await page.screenshot({path:path.join(out,'PREVIEW_'+view+'.png'),fullPage:true});
 }
 await page.locator('#fp-view').selectOption('missions');
 const before=await page.locator('#fp-world').evaluate(w=>w.style.transform);
 await page.locator('#fp-plus').click();
 const after=await page.locator('#fp-world').evaluate(w=>w.style.transform);
 if(before===after)errors.push('zoom does not change camera');
 const box=await page.locator('#fp-map').boundingBox();
 await page.mouse.move(box.x+25,box.y+25);await page.mouse.down();await page.mouse.move(box.x+95,box.y+65,{steps:4});await page.mouse.up();
 const dragged=await page.locator('#fp-world').evaluate(w=>w.style.transform);
 if(dragged===after)errors.push('pan does not change camera');
 const named=await page.locator('#fp-detail h2').textContent();
 await page.locator('#fp-fit').click();
 const target=page.locator('[data-node="COLDWAR_CUB_foreign_advisers"]');
 await target.click();
 if(await page.locator('#fp-detail h2').textContent()!=='Advisory Missions')errors.push('real click after drag failed');
 if(await page.locator('img').evaluateAll(imgs=>imgs.some(i=>i.complete&&i.naturalWidth===0)))errors.push('broken native image');
 const report={project:'IMPERIA COLD WAR',status:errors.length?'fail':'pass',errors,inspected:design.nodes.length,views,zoom:true,pan:true,real_click:true,native_assets:true,game_engine_tested:false};
 fs.writeFileSync(path.join(out,'BROWSER_VALIDATION.json'),JSON.stringify(report,null,2)+'\n');
 await browser.close();console.log(JSON.stringify({status:report.status,errors,inspected:120,views:views.length}));
 if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
