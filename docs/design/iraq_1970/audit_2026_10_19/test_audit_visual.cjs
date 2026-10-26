// Browser-only audit presentation QA. No game execution or gameplay claim.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{pathToFileURL}=require('url');
const out=__dirname;
(async()=>{
 const checks=[],errors=[];
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:736,height:1050}});
 page.on('pageerror',e=>errors.push(e.message));
 try{
  await page.goto(pathToFileURL(path.join(out,'PREVIEW.html')).href);
  const frame=page.frames().find(f=>f!==page.mainFrame());
  assert.ok(frame,'Sandbox frame missing');
  await frame.locator('#cw-iraq-impact-audit').waitFor();
  for(const width of [320,400,560,736,1024]){
   await page.setViewportSize({width,height:1100});
   await frame.locator('#cwa-reward-tab').click();
   for(const [pair,title] of Object.entries({industry:'Basic Industries First',army:'A Professional Core',guard:'Presidential Guard',literacy:'Mass Literacy',oil:'An Oil Revenue State',front:'National Front'})){
    await frame.locator('#cwa-pair').selectOption(pair);
    assert.equal(await frame.locator('.cwa-program h3').first().innerText(),title);
    assert.equal(await frame.locator('#cwa-pair').inputValue(),pair);
    assert.equal(await frame.locator('.cwa-program').count(),2);
    assert.equal(await frame.locator('.cwa-program tr').count(),6);
    assert.ok(await frame.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Reward overflow ${width}/${pair}`);
   }
   checks.push(`Six reward pairs update at ${width}px`);
   await frame.locator('#cwa-structure-tab').click();
   for(const issue of ['oil','iran','industry','opposition','kdp','finale']){
    await frame.locator('#cwa-issue').selectOption(issue);
    await frame.locator('#cwa-current svg').waitFor({state:'visible'});
    assert.equal(await frame.locator('.cwa-diagrams svg').count(),2);
    assert.ok(await frame.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Structure overflow ${width}/${issue}`);
    const clipping=await frame.locator('.cwa-node-label').evaluateAll(xs=>xs.filter(x=>x.scrollHeight>x.clientHeight+1||x.scrollWidth>x.clientWidth+1).map(x=>({text:x.textContent,client:[x.clientWidth,x.clientHeight],scroll:[x.scrollWidth,x.scrollHeight]})));
    assert.deepEqual(clipping,[],`Node labels clipped ${width}/${issue}`);
   }
   checks.push(`Six before/after graphs fit without clipped labels at ${width}px`);
  }
  await frame.evaluate(()=>{
   window.__saves=[];
   window.openai={widgetState:null,setWidgetState:async v=>{window.__saves.push(v);window.openai.widgetState=v;window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{widgetState:v}}}));}};
  });
  await frame.locator('#cwa-issue').selectOption('iran');
  assert.equal(await frame.evaluate(()=>window.__saves.length),1);
  assert.equal(await frame.locator('#cwa-issue').inputValue(),'iran');
  await frame.evaluate(()=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{widgetState:{privateContent:{pair:'front',issue:'oil',updatedAt:Date.now()+1000}}}}})));
  assert.equal(await frame.locator('#cwa-pair').inputValue(),'front');
  assert.equal(await frame.locator('#cwa-issue').inputValue(),'oil');
  assert.equal(await frame.evaluate(()=>window.__saves.length),1);
  await frame.evaluate(()=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{widgetState:{privateContent:{pair:'industry',issue:'iran',updatedAt:1}}}}})));
  assert.equal(await frame.locator('#cwa-pair').inputValue(),'front');
  assert.equal(await frame.locator('#cwa-issue').inputValue(),'oil');
  checks.push('Interaction state persists; incoming state restores without save loops');
  await page.setViewportSize({width:736,height:1100});
  await frame.locator('#cwa-issue').selectOption('oil');
  await frame.waitForFunction(()=>innerHeight>=document.body.scrollHeight-1,null,{timeout:5000});
  await page.screenshot({path:path.join(out,'AUDIT_STRUCTURE_PREVIEW.png'),fullPage:true});
  await frame.locator('#cwa-reward-tab').click();
  await frame.locator('#cwa-pair').selectOption('industry');
  await frame.waitForFunction(()=>innerHeight>=document.body.scrollHeight-1,null,{timeout:5000});
  assert.equal(await frame.locator('.cwa-program h3').first().innerText(),'Basic Industries First');
  await page.screenshot({path:path.join(out,'AUDIT_REWARDS_PREVIEW.png'),fullPage:true});
  await page.emulateMedia({colorScheme:'dark'});
  await page.screenshot({path:path.join(out,'AUDIT_REWARDS_DARK_PREVIEW.png'),fullPage:true});
  checks.push('Native tabs, six pairs, six graph selections, light/dark screenshots');
 }catch(e){errors.push(e.stack||String(e));
  await page.screenshot({path:path.join(out,'AUDIT_QA_FAILURE.png'),fullPage:true});
  const f=page.frames().find(x=>x!==page.mainFrame());
  if(f)console.log(JSON.stringify(await f.evaluate(()=>[...document.querySelectorAll('#cw-iraq-impact-audit *')].filter(e=>e.getBoundingClientRect().right>innerWidth+1).map(e=>({tag:e.tagName,cls:e.className,text:e.textContent.slice(0,90),right:e.getBoundingClientRect().right,width:innerWidth})).slice(0,16)),null,2));
 }
 await browser.close();
 const report={scope:'HTML fragment in actual sandboxed browser wrapper; not an HOI4 runtime test',checks,errors};
 fs.writeFileSync(path.join(out,'BROWSER_QA.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify(report,null,2));if(errors.length)process.exitCode=1;
})();
