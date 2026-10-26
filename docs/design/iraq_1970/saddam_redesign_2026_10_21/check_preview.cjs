// IMPERIA CW — Cold War: browser QA for the Saddam concept; never changes game files.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert');
const dir=__dirname,src='C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82/saddam-domestic-paths.html';
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1024,height:1000}}),errors=[],checks=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto('file:///'+src);await page.waitForSelector('#cw-saddam-concept[data-ready="true"]');
 const v=()=>document.getElementById('cw-saddam-concept')._viewer;
 const result=await page.evaluate(()=>{const r=document.getElementById('cw-saddam-concept'),v=r._viewer;let all=0;for(const n of v.data.nodes){v.pick(n.id);if(!r.querySelector('#sc-detail h3').textContent.includes(n.t))throw Error(n.id);all++;}return{all,proposed:v.data.nodes.filter(n=>n.g==='saddam').length,images:r.querySelectorAll('img').length,broken:[...r.querySelectorAll('img')].filter(i=>!i.complete||!i.naturalWidth).length};});
 assert.equal(result.all,417);assert.equal(result.proposed,25);assert.equal(result.broken,0);checks.push({inspectEveryFocus:result});
 await page.selectOption('#sc-policy','government');
 await page.screenshot({path:path.join(dir,'government-1024.png'),fullPage:true});
 const chosen=await page.evaluate(()=>{const v=document.getElementById('cw-saddam-concept')._viewer;for(const p of v.data.pairs){v.choose(p.id,'A');if(v.current().choices[p.id]!=='A')throw Error('A '+p.id);v.choose(p.id,'B');if(v.current().choices[p.id]!=='B')throw Error('B '+p.id);}return v.current().choices;});
 assert.equal(Object.keys(chosen).length,5);checks.push({fiveChoicesSwitchable:chosen});
 await page.selectOption('#sc-policy','industry');
 await page.screenshot({path:path.join(dir,'industry-1024.png'),fullPage:true});
 const map=await page.locator('#sc-map').boundingBox();
 for(const button of ['left','middle','right']){const before=await page.evaluate(()=>document.getElementById('cw-saddam-concept')._viewer.camera());await page.mouse.move(map.x+map.width*.6,map.y+map.height*.6);await page.mouse.down({button});await page.mouse.move(map.x+map.width*.6+71,map.y+map.height*.6+39,{steps:4});await page.mouse.up({button});const after=await page.evaluate(()=>document.getElementById('cw-saddam-concept')._viewer.camera());assert(Math.abs(after.x-before.x-71)<1);assert(Math.abs(after.y-before.y-39)<1);}
 checks.push({threeMouseButtonsPan:true});
 await page.mouse.move(map.x+map.width*.5,map.y+map.height*.5);let before=await page.evaluate(()=>document.getElementById('cw-saddam-concept')._viewer.camera());await page.mouse.wheel(0,170);await page.waitForTimeout(200);let after=await page.evaluate(()=>document.getElementById('cw-saddam-concept')._viewer.camera());assert.equal(Math.round(before.y-after.y),170);
 await page.keyboard.down('Shift');before=after;await page.mouse.wheel(0,130);await page.waitForTimeout(200);await page.keyboard.up('Shift');after=await page.evaluate(()=>document.getElementById('cw-saddam-concept')._viewer.camera());assert.equal(Math.round(before.x-after.x),130);
 await page.keyboard.down('Control');before=after;await page.mouse.wheel(0,-150);await page.waitForTimeout(200);await page.keyboard.up('Control');after=await page.evaluate(()=>document.getElementById('cw-saddam-concept')._viewer.camera());assert(after.z>before.z);checks.push({wheelShiftAndControl:true});
 await page.click('#sc-branch');await page.screenshot({path:path.join(dir,'saddam-overview-1024.png'),fullPage:true});
 await page.click('#sc-all');await page.screenshot({path:path.join(dir,'whole-iraq-1024.png'),fullPage:true});
 await page.selectOption('#sc-policy','army');await page.click('#sc-native');
 const node=page.locator('[data-node="COLDWAR_IRQ_saddam_regular_army"]');before=await page.evaluate(()=>document.getElementById('cw-saddam-concept')._viewer.camera());await node.click();after=await page.evaluate(()=>document.getElementById('cw-saddam-concept')._viewer.camera());assert.deepEqual(after,before);assert.equal(await page.locator('#sc-detail h3').textContent(),'The Regular Army');checks.push({clickWithoutRecentring:true});
 for(const width of [736,320]){await page.setViewportSize({width,height:1000});await page.selectOption('#sc-policy','households');await page.screenshot({path:path.join(dir,`households-${width}.png`),fullPage:true});const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);assert(!overflow,`Page overflow ${width}`);checks.push({width,noHorizontalOverflow:!overflow});}
 assert.deepEqual(errors,[]);fs.writeFileSync(path.join(dir,'BROWSER_QA.json'),JSON.stringify({errors,checks},null,2)+'\n');
 await browser.close();console.log(JSON.stringify({passed:true,checks:checks.length,errors}));
})().catch(e=>{console.error(e);process.exitCode=1;});
