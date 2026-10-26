// Concept-only checks for the user's low-oil / expensive-expansion revision.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
(async()=>{
 const design=JSON.parse(fs.readFileSync(path.join(__dirname,'COLDWAR_UAE_1970_CONCEPT.json'),'utf8'));
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1400,height:1200}}),errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(__dirname,'PREVIEW.html')).href);
 await page.locator('.uae-title canvas').last().waitFor();
 await page.locator('#uae-branch').selectOption('oil');await page.locator('#uae-fit').click();
 if(!(await page.locator('#uae-meta').innerText()).includes('Start:4 base oil'))errors.push('Oil branch omits low start');
 for(const phase of design.oil_development){
  await page.locator(`[data-node="${phase.focus}"]`).click();
  const text=await page.locator('#uae-detail').innerText();
  if(!text.includes(`Treasury: −$${phase.treasury_billion} billion`))errors.push('Invoice missing '+phase.focus);
  if(!text.includes(`${phase.days} days`))errors.push('Duration missing '+phase.focus);
 }
 await page.screenshot({path:path.join(__dirname,'PREVIEW_oil_investment.png'),fullPage:true});
 await page.locator('#uae-spirits').click();
 const start=await page.locator('#uae-detail').innerText();
 if(!start.includes('4 total: Abu Dhabi3 + Dubai1'))errors.push('Starting resources missing');
 await page.screenshot({path:path.join(__dirname,'PREVIEW_low_oil_start.png'),fullPage:true});
 fs.writeFileSync(path.join(__dirname,'OIL_BROWSER_VALIDATION.json'),JSON.stringify({errors,starting_base:design.starting_resources.proposed_base,stages_checked:design.oil_development.length,total_capex_billion:design.oil_development.reduce((s,p)=>s+p.treasury_billion,0)},null,2));
 await browser.close();console.log(JSON.stringify({errors,stages_checked:4,starting_base:4,total_capex_billion:16.25}));if(errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
