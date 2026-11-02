// IMPERIA COLD WAR — Browser checks of the proposed tree, not HOI4 engine tests.
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const D=JSON.parse(fs.readFileSync(path.join(__dirname,'proposal.json'),'utf8'));
const out='C:/Users/Enes/.codex/visualizations/2026/10/23/01a16840-34d5-7e60-8c3d-134a5e042a6a/coldwar_france_politics';
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1024,height:1100}}),errors=[],views=[],collisions=[];
 page.on('pageerror',e=>errors.push(e.message));await page.goto(pathToFileURL(path.join(out,'france-programmes-v5.html')).href);
 await page.waitForSelector('#coldwar-france-v5[data-ready="true"]');let clicks=0,offerSides=0,edges=0;
 for(const g of D.groups){
   await page.selectOption('#cw-party',g.id);await page.selectOption('#cw-area','all');await page.click('#cw-fit');
   const ns=D.nodes.filter(n=>n.group===g.id);
   assert.deepEqual(new Set(await page.locator('.cw-node').evaluateAll(xs=>xs.map(x=>x.dataset.key))),new Set(ns.map(n=>n.key)),g.id+' missing nodes');
   assert.equal(await page.locator('[data-edge]').count(),ns.reduce((a,n)=>a+n.parents.flat().length,0),g.id+' connector omissions');
   edges+=await page.locator('[data-edge]').count();
   for(const n of ns){
     await page.selectOption('#cw-focus',n.key);
     assert.equal(await page.locator('#cw-detail h3').textContent(),n.title);
     const text=await page.locator('#cw-detail > .cw-effects').innerText();
     assert(!/\bundefined\b|\bNaN\b|\b0\.0%|governing political current|CAT_industry|programme modifiers apply/i.test(text),n.key+' bad effect text: '+text);
     assert((await page.locator('#cw-detail > .cw-effects .cw-effect').count())>0,n.key+' empty effects');
     if(n.offer_id){assert.equal(await page.locator('#cw-detail .cw-sides > div').count(),2);offerSides+=2;}
     clicks++;
   }
   const boxes=await page.locator('.cw-node').evaluateAll(xs=>xs.map(x=>{const r=x.getBoundingClientRect();return{key:x.dataset.key,x:r.x,y:r.y,w:r.width,h:r.height}}));
   for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){
     const a=boxes[i],b=boxes[j];if(Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>2&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>2)collisions.push({group:g.id,a:a.key,b:b.key});
   }
 }
 for(const [group,area]of [['gaullist','foreign'],['liberal','military'],['centre','military'],['socialist','foreign'],['ecology','foreign'],['national','all']]){
   await page.selectOption('#cw-party',group);await page.selectOption('#cw-area',area);await page.click('#cw-fit');
   const target=path.join(out,`v5-${group}-${area}.png`);await page.screenshot({path:target,fullPage:true});views.push(target);
 }
 for(const width of [736,360]){
   await page.setViewportSize({width,height:1100});await page.selectOption('#cw-party','gaullist');await page.selectOption('#cw-area','foreign');
   assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),width+' document overflow');
   const rects=await page.locator('#cw-detail .cw-effect').evaluateAll(xs=>xs.map(x=>{const r=x.getBoundingClientRect();return{x:r.x,right:r.right,scroll:x.scrollWidth,width:r.width}}));
   assert(rects.every(r=>r.x>=0&&r.right<=width+1&&r.scroll<=r.width+1),width+' effect row overflow');
   await page.click('#cw-native');await page.selectOption('#cw-focus',D.nodes.find(n=>n.group==='gaullist'&&n.offer_id).key);
   const selected=await page.locator('.cw-node[aria-pressed="true"]').boundingBox();assert(selected.x>=0&&selected.x+selected.width<=width,'selected focus not navigable');
   const target=path.join(out,`v5-responsive-${width}.png`);await page.screenshot({path:target,fullPage:true});views.push(target);
 }
 fs.writeFileSync(path.join(__dirname,'COLLISIONS.json'),JSON.stringify(collisions,null,2)+'\n');
 assert.deepEqual(errors,[]);assert.deepEqual(collisions,[],'Overlapping focus cards: '+JSON.stringify(collisions));
 const report={project:'IMPERIA COLD WAR',result:'pass',focusInspections:clicks,offerSpiritSides:offerSides,prerequisiteEdges:edges,scriptErrors:errors,cardOverlaps:collisions,views,limits:'Source-coordinate browser review only; native line routing, focus UI, effect execution and multiplayer ordering need HOI4 testing after approval.'};
 fs.writeFileSync(path.join(__dirname,'PREVIEW_TESTS.json'),JSON.stringify(report,null,2)+'\n');await browser.close();console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exit(1)});
