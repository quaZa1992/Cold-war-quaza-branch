// COLDWAR_IRQ concept browser QA. Reads local preview; no game or network changes.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');const path=require('path');const {pathToFileURL}=require('url');
const out=path.resolve('docs/design/iraq_1970');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1024,height:1150}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(out,'PREVIEW.html')).href);
 await page.locator('.irq-node').last().waitFor();
 await page.locator('.irq-title canvas').last().waitFor();
 const design=JSON.parse(fs.readFileSync(path.join(out,'COLDWAR_IRQ_1970_CONCEPT.json'),'utf8'));
 const expectedEdges=design.nodes.reduce((s,n)=>s+n.prerequisites.flat().length,0);
 const imageFailures=await page.locator('img').evaluateAll(imgs=>imgs.filter(i=>!i.complete||!i.naturalWidth).length);
 if(imageFailures)errors.push('broken images:'+imageFailures);
 const saddamArt=await page.locator('[data-node="COLDWAR_IRQ_saddam_presidency"] .irq-icon').evaluate(i=>({width:i.naturalWidth,height:i.naturalHeight}));
 if(saddamArt.width!==100||saddamArt.height!==91)errors.push('incorrect supplied Saddam icon dimensions '+JSON.stringify(saddamArt));
 const branches=await page.locator('#irq-branch option').evaluateAll(es=>es.map(e=>e.value));
 const views=[];
 for(const width of [320,736,1024]){
  await page.setViewportSize({width,height:1150});
  for(const branch of branches){
   await page.locator('#irq-branch').selectOption(branch);
   const info=await page.locator('#coldwar-iraq-concept').evaluate(r=>({overflow:r.scrollWidth>r.clientWidth+2,nodes:r.querySelectorAll('.irq-node').length,edges:r.querySelectorAll('.prerequisite').length}));
   if(info.overflow||info.nodes!==design.nodes.length||info.edges!==expectedEdges)errors.push(width+' '+branch+' '+JSON.stringify(info));
   views.push({width,branch,...info});
  }
  await page.locator('#irq-overview').click();
  if(await page.locator('#coldwar-iraq-concept').evaluate(r=>r.scrollWidth>r.clientWidth+2))errors.push('overview overflow '+width);
  await page.locator('#irq-spirits').click();
  if(await page.locator('.irq-spirit').count()!==7)errors.push('missing starting spirit');
 }
 const inspected=await page.evaluate(()=>{const errors=[];for(const b of document.querySelectorAll('.irq-node')){b.click();if(document.querySelector('#irq-detail h3')?.textContent!==b.getAttribute('aria-label'))errors.push(b.dataset.node);}return errors;});
 errors.push(...inspected.map(e=>'failed focus inspector '+e));
 const governments=await page.locator('#irq-government option').evaluateAll(es=>es.map(e=>e.value));
 for(const value of governments)await page.locator('#irq-government').selectOption(value);
 await page.locator('#irq-government').selectOption('bakr');
 if(await page.locator('[data-node="COLDWAR_IRQ_regional_command"]').evaluate(e=>e.classList.contains('is-locked')))errors.push('Baath locked under Bakr');
 if(!(await page.locator('[data-node="COLDWAR_IRQ_icp_congress"]').evaluate(e=>e.classList.contains('is-locked'))))errors.push('ICP active under Bakr');
 await page.locator('#irq-government').selectOption('aziz');
 if(!(await page.locator('[data-node="COLDWAR_IRQ_regional_command"]').evaluate(e=>e.classList.contains('is-locked'))))errors.push('Baath active under Aziz');
 if(await page.locator('[data-node="COLDWAR_IRQ_icp_congress"]').evaluate(e=>e.classList.contains('is-locked')))errors.push('ICP locked under Aziz');
 await page.locator('#irq-government').selectOption('bakr');
 await page.setViewportSize({width:1024,height:1150});
 for(const branch of ['state','baath','bakr','saddam','communists','aziz','dawa','oil','defence','war','iran_war']){
  await page.locator('#irq-branch').selectOption(branch);
  await page.screenshot({path:path.join(out,'PREVIEW_'+branch+'.png'),fullPage:true});
 }
 await page.locator('#irq-branch').selectOption('state');await page.locator('#irq-decisions').click();
 if(!(await page.locator('#irq-detail').innerText()).includes('Deliver a Pending Programme'))errors.push('pending retry not visible');
 await page.locator('#irq-overview').click();await page.screenshot({path:path.join(out,'PREVIEW_overview.png'),fullPage:true});
 const overviewZoom=await page.locator('#irq-zoom').innerText();
 await page.locator('#irq-spirits').click();
 await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
 if(await page.locator('#irq-zoom').innerText()!==overviewZoom)errors.push('opening spirit details changed map zoom');
 await page.screenshot({path:path.join(out,'PREVIEW_spirits.png'),fullPage:true});
 await page.locator('#irq-branch').selectOption('baath');
 const before=await page.locator('#irq-world').evaluate(e=>({transform:e.style.transform,x:e.querySelector('.irq-node').style.left}));
 await page.locator('#irq-plus').click();
 const after=await page.locator('#irq-world').evaluate(e=>({transform:e.style.transform,x:e.querySelector('.irq-node').style.left}));
 if(before.transform===after.transform||before.x!==after.x)errors.push('zoom changed layout or failed');
 fs.writeFileSync(path.join(out,'BROWSER_VALIDATION.json'),JSON.stringify({errors,images:imageFailures,branchViews:views.length,focusInspectors:design.nodes.length,governmentViews:governments,views},null,2));
 console.log(JSON.stringify({errors,branchViews:views.length,focusInspectors:design.nodes.length,governmentViews:governments.length}));
 await browser.close();if(errors.length)process.exitCode=1;
})();
