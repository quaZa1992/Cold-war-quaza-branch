// IMPERIA CW — Cold War: QA of the read-only event/decision guide.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');
(async()=>{
const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
const page=await browser.newPage({viewport:{width:736,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('file:///'+path.join(__dirname,'preview.html').replaceAll('\\','/'));
const frame=page.frames().find(f=>f.parentFrame());assert(frame);await frame.waitForSelector('#cw-iraq-event-guide[data-ready="true"]');
const checks=await frame.evaluate(()=>{const root=document.getElementById('cw-iraq-event-guide'),v=root._guide,d=v.data;let options=0;for(const r of d.records){v.show(r.id,false);if(root.querySelector('#ieg-detail h4').textContent!==r.title)throw Error(r.id);if(r.type==='event'){const n=root.querySelectorAll('.ieg-option').length;if(n!==r.options.length)throw Error('options '+r.id);options+=n;}}return{entries:d.records.length,decisions:d.records.filter(r=>r.type==='decision').length,events:d.records.filter(r=>r.type==='event').length,options,missingDecisionExplanations:d.records.filter(r=>r.type==='decision'&&!r.explanation).map(r=>r.id)};});
assert.equal(checks.decisions,150);assert.equal(checks.events,162);assert.equal(checks.options,449);assert.deepEqual(checks.missingDecisionExplanations,[]);
await frame.selectOption('#ieg-group','d_irq');await frame.selectOption('#ieg-item','COLDWAR_IRQ_decision_iran_supplier');
await frame.locator('[data-open]').first().click();assert((await frame.locator('#ieg-detail h4').first().textContent()).includes('Wartime Supply'));
await frame.click('#ieg-back');assert.equal(await frame.locator('#ieg-item').inputValue(),'COLDWAR_IRQ_decision_iran_supplier');
await frame.selectOption('#ieg-group','auto');await frame.selectOption('#ieg-item','auto_rising');await page.screenshot({path:path.join(__dirname,'guide-736.png'),fullPage:true});
for(const width of [320,1024]){await page.setViewportSize({width,height:1000});await frame.selectOption('#ieg-group','e_us');await frame.selectOption('#ieg-item','COLDWAR_USA_gulf_events.31');await page.waitForTimeout(200);assert(!(await frame.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1)));const height=await frame.evaluate(()=>document.documentElement.scrollHeight);await page.locator('iframe').evaluate((el,h)=>el.style.height=h+'px',height+20);await page.screenshot({path:path.join(__dirname,`event-${width}.png`),fullPage:true});}
assert.deepEqual(errors,[]);fs.writeFileSync(path.join(__dirname,'BROWSER_QA.json'),JSON.stringify({checks,errors,followingAndBack:true,widths:[320,736,1024]},null,2)+'\n');
await browser.close();console.log(JSON.stringify({passed:true,...checks}));
})().catch(e=>{console.error(e);process.exitCode=1;});
