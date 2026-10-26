// COLDWAR_UAE concept-only visual and interaction checks; no game writes.
const { chromium }=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');const path=require('path');const {pathToFileURL}=require('url');
const out=__dirname;
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1400,height:1200}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(out,'PREVIEW.html')).href);
 await page.locator('.uae-title canvas').last().waitFor();
 const design=JSON.parse(fs.readFileSync(path.join(out,'COLDWAR_UAE_1970_CONCEPT.json'),'utf8'));
 const edges=design.nodes.reduce((s,n)=>s+n.prerequisites.flat().length,0);
 const broken=await page.locator('img').evaluateAll(es=>es.filter(e=>!e.complete||!e.naturalWidth).length);
 if(broken)errors.push('Broken images '+broken);
 const views=[];
 for(const width of [320,736,1024,1400]){
  await page.setViewportSize({width,height:1200});
  for(const g of design.groups){
   await page.locator('#uae-branch').selectOption(g.id);
   await page.locator('#uae-fit').click();
   const info=await page.locator('#coldwar-uae-concept').evaluate(r=>({overflow:r.scrollWidth>r.clientWidth+2,nodes:r.querySelectorAll('.uae-node').length,edges:r.querySelectorAll('.prerequisite').length}));
   if(info.overflow||info.nodes!==design.nodes.length||info.edges!==edges)errors.push(width+' '+g.id+' '+JSON.stringify(info));
   views.push({width,branch:g.id,...info});
  }
 }
 const inspected=await page.evaluate(()=>{const bad=[];for(const b of document.querySelectorAll('.uae-node')){b.click();if(document.querySelector('#uae-detail h3')?.textContent!==b.getAttribute('aria-label'))bad.push(b.dataset.node);}return bad;});
 errors.push(...inspected.map(x=>'Inspector failed '+x));
 const pairs=[['monarchy','COLDWAR_UAE_majlis',false],['monarchy','COLDWAR_UAE_social_compact',true],['left_communist','COLDWAR_UAE_social_ownership',false],['left_communist','COLDWAR_UAE_social_market',true],['left_social','COLDWAR_UAE_social_market',false],['left_social','COLDWAR_UAE_social_ownership',true],['arab_civil','COLDWAR_UAE_civilian_arabism',false],['arab_civil','COLDWAR_UAE_officers_republic',true]];
 for(const [gov,id,locked] of pairs){await page.locator('#uae-government').selectOption(gov);if(await page.locator(`[data-node="${id}"]`).evaluate(e=>e.classList.contains('is-locked'))!==locked)errors.push('Government gate '+gov+' '+id);}
 await page.locator('#uae-government').selectOption('monarchy');
 await page.setViewportSize({width:1400,height:1200});
 for(const group of design.groups){await page.locator('#uae-branch').selectOption(group.id);await page.locator('#uae-fit').click();await page.screenshot({path:path.join(out,'PREVIEW_'+group.id+'.png'),fullPage:true});}
 await page.locator('#uae-overview').click();await page.screenshot({path:path.join(out,'PREVIEW_overview.png'),fullPage:true});
 await page.locator('#uae-spirits').click();
 if(await page.locator('.uae-spirit').count()!==design.starting_spirits.length)errors.push('Missing spirits');
 await page.screenshot({path:path.join(out,'PREVIEW_spirits.png'),fullPage:true});
 // Actual mouse click on a locked programme must open details without panning.
 await page.locator('#uae-branch').selectOption('left');await page.locator('#uae-fit').click();
 const target=page.locator('[data-node="COLDWAR_UAE_social_ownership"]');
 const before=await page.locator('#uae-world').evaluate(e=>e.style.transform);
 await target.click();
 const after=await page.locator('#uae-world').evaluate(e=>e.style.transform);
 if(before!==after)errors.push('A click moved camera');
 if(await page.locator('#uae-detail h3').innerText()!=='Public Ownership')errors.push('Locked mouse click failed');
 await page.locator('#uae-plus').click();
 if(await page.locator('#uae-world').evaluate(e=>e.style.transform)===after)errors.push('Zoom failed');
 const box=await page.locator('#uae-map').boundingBox();const panBefore=await page.locator('#uae-world').evaluate(e=>e.style.transform);
 await page.mouse.move(box.x+40,box.y+40);await page.mouse.down();await page.mouse.move(box.x+100,box.y+90,{steps:6});await page.mouse.up();
 if(await page.locator('#uae-world').evaluate(e=>e.style.transform)===panBefore)errors.push('Pan failed');
 await page.locator('#uae-branch').selectOption('union');await page.locator('#uae-fit').click();
 const report={errors,focusInspectors:design.nodes.length,branchViews:views.length,imagesBroken:broken,governmentCases:pairs.length,mouseClickLockedNode:true,pan:true,zoom:true,views};
 fs.writeFileSync(path.join(out,'BROWSER_VALIDATION.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({errors,focusInspectors:design.nodes.length,branchViews:views.length,governmentCases:pairs.length}));
 await browser.close();if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
