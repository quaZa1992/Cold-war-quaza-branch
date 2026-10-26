// IMPERIA CW — Cold War: local browser QA of the approval concept; no game mutation.
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const {chromium}=require('C:/Users/sonyz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
(async()=>{
 const data=JSON.parse(fs.readFileSync(path.join(__dirname,'COLDWAR_NKO_1970_design.json'),'utf8'));
 const launch={headless:true};
 if(process.env.COLDWAR_BROWSER_EXECUTABLE)launch.executablePath=process.env.COLDWAR_BROWSER_EXECUTABLE;
 const browser=await chromium.launch(launch);
 const page=await browser.newPage({viewport:{width:1024,height:1200}}),errors=[],checks=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(__dirname,'COLDWAR_NKO_1970_preview.html')).href);
 await page.locator('.nko-focus').first().waitFor();
 for(const width of [320,736,1024]){
  await page.setViewportSize({width,height:1200});
  for(const group of ['all',...data.groups.map(g=>g.id)]){
   await page.locator('#nko-section').selectOption(group);
   const check=await page.locator('#coldwar-nko-concept').evaluate(el=>({
    overflow:document.documentElement.scrollWidth>document.documentElement.clientWidth+1,
    count:el.querySelectorAll('.nko-focus').length,
    missing:[...el.querySelectorAll('.nko-focus img')].filter(i=>!i.complete||!i.naturalWidth).length,
    edges:el.querySelectorAll('.prerequisite').length
   }));
   const expected=group==='all'?data.nodes.length:data.nodes.filter(n=>n.group===group).length;
   if(check.overflow||check.missing||check.count!==expected)errors.push({width,group,...check});
   checks.push({width,group,...check});
  }
 }
 await page.setViewportSize({width:1024,height:1200});
 for(const group of ['all','wpk','economy','kdp','chondo','atomic']){
  await page.locator('#nko-section').selectOption(group);
  await page.locator('.nko-window').screenshot({path:path.join(__dirname,'browser_'+group+'.png')});
 }
 await page.locator('#nko-section').selectOption('defence');
 await page.locator('[data-id="COLDWAR_NKO_mobile_army"]').click();
 const mobile=await page.locator('#nko-inspector').innerText();
 if(!mobile.includes('Army fuel consumption: +8%')||mobile.includes('Population non-electric'))errors.push('Mobile army fuel label');
 await page.locator('#nko-government').selectOption('5');
 await page.locator('#nko-section').selectOption('kdp');
 if(await page.locator('.nko-focus.inactive').count())errors.push('KDP government state');
 await page.locator('#nko-government').selectOption('4');
 if(await page.locator('.nko-focus.inactive').count()!==14)errors.push('KDP inactive state');
 await page.locator('#nko-section').selectOption('economy');
 await page.locator('[data-id="COLDWAR_NKO_western_credit"]').evaluate(el=>el.click());
 const credit=await page.locator('#nko-inspector').innerText();
 if(!credit.includes('+1.25 percentage points')||!credit.includes('$7.500 billion'))errors.push('Loan units/amount');
 await page.locator('#nko-spirits').click();
 if(await page.locator('#nko-inspector article').count()!==6)errors.push('Spirit count');
 await page.locator('#nko-section').selectOption('wpk');
 await page.locator('#nko-native').click();
 const native=await page.locator('.nko-focus').first().evaluate(el=>({w:el.getBoundingClientRect().width,h:el.getBoundingClientRect().height}));
 if(native.w!==165||native.h!==128)errors.push({native});
 const report={errors,checks,native,source:'local standalone preview',engineTested:false};
 fs.writeFileSync(path.join(__dirname,'browser_validation.json'),JSON.stringify(report,null,2));
 console.log(JSON.stringify({errors,views:checks.length,native}));
 await browser.close();if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
