const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1400,height:1250}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(__dirname,'PREVIEW.html')).href);
 await page.locator('.uae-title canvas').last().waitFor();
 if(await page.locator('#uae-branch').inputValue()!=='british')errors.push('First visit did not open British branch');
 const design=JSON.parse(fs.readFileSync(path.join(__dirname,'COLDWAR_UAE_1970_CONCEPT.json'),'utf8'));
 const start=design.british_treaties.starting_state;
 if(!start.starts_with_both_spirits||start.requires_focus||start.requires_new_uk_acceptance)errors.push('Starting withdrawal requires a new petition/approval');
 const cases=[];
 for(const [state,mainLocked,protectionLocked] of [['subject',true,true],['transition',true,true],['loyal',true,false],['free',false,true],['friendship',false,true],['other',true,true]]){
  await page.locator('#uae-treaty-status').selectOption(state);
  for(const [id,want] of [['COLDWAR_UAE_sovereign_union',mainLocked],['COLDWAR_UAE_protected_administration',protectionLocked],['COLDWAR_UAE_petition_independence',state==='other']]){
   const locked=await page.locator(`[data-node="${id}"]`).evaluate(e=>e.classList.contains('is-locked'));
   if(locked!==want)errors.push('Incorrect treaty gate '+state+' '+id);
  }
  await page.locator('#uae-treaties').click();
  const cards=await page.locator('.uae-treaty-card').count();
  if(cards!==(state==='other'?0:2))errors.push('Missing bilateral spirits '+state);
  if(state==='subject'){
   const body=await page.locator('#uae-detail').innerText();
   if(!body.includes('British Withdrawal Announced')||!body.includes('By the end of 1971')||!body.includes('Historical scenario execution: 1 December 1971'))errors.push('Initial paired spirits omit the already-announced timetable');
   await page.screenshot({path:path.join(__dirname,'PREVIEW_british_treaty_starting.png'),fullPage:true});
  }
  if(state==='transition'){
   const dates=await page.locator('.uae-treaty-date').allTextContents();
   if(dates.length!==2||dates[0]!==dates[1]||dates[0]!=='1 December 1971')errors.push('Scheduled release dates differ');
   await page.screenshot({path:path.join(__dirname,'PREVIEW_british_treaty_signed.png'),fullPage:true});
  }
  if(state==='loyal'){
   const body=await page.locator('#uae-detail').innerText();
   if(!body.includes('No fixed independence date'))errors.push('Loyal review mistaken for independence');
   await page.screenshot({path:path.join(__dirname,'PREVIEW_british_treaty_loyal.png'),fullPage:true});
  }
  cases.push({state,mainLocked,protectionLocked,cards});
 }
 // All party design view still respects actual independence/status gates.
 await page.locator('#uae-government').selectOption('all');await page.locator('#uae-treaty-status').selectOption('transition');
 if(!(await page.locator('[data-node="COLDWAR_UAE_sovereign_union"]').evaluate(e=>e.classList.contains('is-locked'))))errors.push('Party design view bypassed independence');
 await page.locator('#uae-government').selectOption('monarchy');
 for(const width of [320,736,1024,1400]){
  await page.setViewportSize({width,height:1250});
  await page.locator('#uae-branch').selectOption('british');await page.locator('#uae-fit').click();
  if(await page.locator('#coldwar-uae-concept').evaluate(r=>r.scrollWidth>r.clientWidth+2))errors.push('British branch overflow '+width);
  for(const state of ['subject','transition']){
   await page.locator('#uae-treaty-status').selectOption(state);
   await page.locator('#uae-treaties').click();
   if(await page.locator('#coldwar-uae-concept').evaluate(r=>r.scrollWidth>r.clientWidth+2))errors.push('Treaty spirits overflow '+width+' '+state);
   if(width===320||width===1024)await page.screenshot({path:path.join(__dirname,`PREVIEW_british_treaty_${state==='subject'?'starting':'signed'}_${width}.png`),fullPage:true});
  }
 }
 await page.setViewportSize({width:1400,height:1250});await page.locator('#uae-treaty-status').selectOption('subject');
 await page.locator('#uae-branch').selectOption('british');await page.locator('#uae-fit').click();
 await page.locator('[data-node="COLDWAR_UAE_petition_independence"]').click();
 if(await page.locator('#uae-detail h3').innerText()!=='Prepare the Handover')errors.push('Old freedom petition title retained');
 if(!(await page.locator('#uae-detail').innerText()).includes('needs neither this focus nor a new UK approval'))errors.push('Handover inspector still gates the historical withdrawal');
 await page.screenshot({path:path.join(__dirname,'PREVIEW_british_petition.png'),fullPage:true});
 const report={errors,statusCases:cases,viewportWidths:[320,736,1024,1400],actualIndependenceRequired:true,bothCountriesSeeSameDate:true};
 fs.writeFileSync(path.join(__dirname,'BRITISH_BROWSER_VALIDATION.json'),JSON.stringify(report,null,2));
 await browser.close();console.log(JSON.stringify({errors,statusCases:cases.length,viewportWidths:4}));if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
