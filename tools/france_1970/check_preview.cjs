// IMPERIA COLD WAR — Full installed-tree inspector interaction and presentation checks.
const fs=require('fs'),path=require('path'),assert=require('assert'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const D=JSON.parse(fs.readFileSync(path.join(__dirname,'approved_design.json'),'utf8'));
const preview=JSON.parse(fs.readFileSync(path.join(__dirname,'PREVIEW_SYNC.json'),'utf8')).preview;
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1024,height:1150}}),errors=[],views=[];let clicked=0,edges=0;
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(preview).href);await page.waitForSelector('#coldwar-france-politics[data-ready="true"]');
 for(const g of D.groups){
  await page.selectOption('#ef-area',g.id);
  if(g.id!=='institutions')await page.selectOption('#ef-domain','all');
  const ns=D.nodes.filter(n=>n.group===g.id);
  const actual=await page.locator('.ef-node').evaluateAll(xs=>xs.map(x=>x.dataset.id));
  assert.deepEqual(new Set(actual),new Set(ns.map(n=>n.id)),`Missing installed preview nodes: ${g.id}`);
  const nEdges=await page.locator('#ef-lines [data-edge]').count();
  assert.equal(nEdges,ns.reduce((a,n)=>a+n.parents.flat().length,0));edges+=nEdges;
  assert.equal(await page.locator('.ef-effects .ef-contract').count(),0,'Explanatory contract text remains inside effects');
  for(const n of ns){
   await page.locator(`[data-key="${n.key}"]`).evaluate(b=>b.click());
   assert.equal(await page.locator('#ef-detail h3').textContent(),n.title);clicked++;
   const text=await page.locator(`[data-key="${n.key}"] .ef-effects`).textContent();
   assert(!/awaiting approval|programme modifiers apply|once per bilateral|selected partner must accept|existing .* retained/i.test(text),'Custom explanatory prose remains');
   if(n.offer_id)assert(text.includes('Unlock decision:'),'Foreign focus does not show its actual decision unlock');
  }
 }
 for(const [group,domain]of [['gaullist','politics'],['radical','military'],['gaullist','foreign'],['socialist','foreign']]){
  await page.selectOption('#ef-area',group);await page.selectOption('#ef-domain',domain);
  await page.click('#ef-fit');
  const file=path.join(path.dirname(preview),`installed-${group}-${domain}.png`);
  await page.screenshot({path:file,fullPage:true});views.push(file);
 }
 for(const width of [736,360]){
  await page.setViewportSize({width,height:1100});await page.selectOption('#ef-area','institutions');
  assert(!await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),'Document overflow');
 }
 assert((await page.locator('footer').textContent()).includes('Installed tree'));
 assert.deepEqual(errors,[]);
 const report={project:'IMPERIA COLD WAR',kind:'Rendered source inspector; not HOI4 GUI',focusClicks:clicked,groups:D.groups.length,prerequisiteEdges:edges,customProseInsideEffects:0,scriptErrors:errors,views,result:'pass'};
 fs.writeFileSync(path.join(__dirname,'PREVIEW_TESTS.json'),JSON.stringify(report,null,2)+'\n');
 await browser.close();console.log(JSON.stringify(report,null,2));
})().catch(e=>{console.error(e);process.exit(1)});
