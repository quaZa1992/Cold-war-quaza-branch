// Review-only USA chapter: actual browser interactions, no HOI4 runtime claims.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{pathToFileURL}=require('url');
const out=path.resolve('docs/design/iraq_1970/usa_gulf');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:736,height:1100}}),errors=[],checks=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.join(out,'PREVIEW.html')).href);
 await page.locator('.usg-title canvas').last().waitFor();
 const data=JSON.parse(await page.locator('#usg-data').textContent());
 assert.equal(data.nodes.length,15);assert.equal(data.decisions.length,17);
 assert.equal(data.resistance_campaign.target_contribution,25);
 assert.equal(data.nodes.find(n=>n.id==='COLDWAR_USA_gulf_no_fly').title,'Northern Air Shield');
 assert.ok(!data.nodes.find(n=>n.id==='COLDWAR_USA_gulf_no_fly').reward_summary.some(s=>s.includes('$0.10')));
 assert.equal(data.idea_specs.COLDWAR_KUR_coalition_air_cover.modifier.cas_damage_reduction,.25);
 assert.equal(data.idea_specs.COLDWAR_USA_northern_air_readiness.modifier.air_intercept_efficiency,.15);
 const iraqiResponses=data.decisions.filter(d=>d.actor==='IRAQ');
 assert.equal(iraqiResponses.length,4);
 assert.ok(iraqiResponses.every(d=>d.unlock===null&&d.unlock_label.includes('independent of US focus')));
 assert.equal(await page.locator('#usg-branch').isVisible(),false);
 assert.equal(await page.locator('#usg-government').isVisible(),false);
 const camera=()=>page.locator('#usg-world').evaluate(e=>{const m=new DOMMatrix(e.style.transform);return{x:m.e,y:m.f,z:m.a};});
 const near=(a,b)=>assert.ok(Math.abs(a-b)<1.1,`${a} != ${b}`);
 for(const w of [320,736,1024]){
  await page.setViewportSize({width:w,height:1100});
  await page.locator('#usg-overview').click();
  for(const n of data.nodes){
   // Trigger the DOM button to inspect every locked/optional node, independent of camera.
   await page.locator(`[data-node="${n.id}"]`).evaluate(e=>e.click());
   assert.equal(await page.locator('#usg-detail h3').innerText(),n.title);
  }
  await page.locator('#usg-decisions').click();assert.equal(await page.locator('#usg-detail details').count(),17);
  assert.match(await page.locator('#usg-detail').innerText(),/35% army personnel/);
  assert.match(await page.locator('#usg-detail').innerText(),/independent of US focus completion/);
  await page.locator('#usg-rules').click();
  assert.match(await page.locator('#usg-detail').innerText(),/75% factory/);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  checks.push(`${w}px: all 15 inspectors, 17 decisions including independent Iraqi responses, mechanic limits, no page overflow`);
 }
 await page.locator('#usg-native').click();
 let box=await page.locator('[data-node="COLDWAR_USA_gulf_desert_storm"]').boundingBox();
 let before=await camera();await page.mouse.click(box.x+82,box.y+65);
 assert.equal(await page.locator('#usg-detail h3').innerText(),'Desert Storm');
 let after=await camera();near(before.x,after.x);near(before.y,after.y);
 checks.push('physical focus click opens effects without camera movement');
 await page.mouse.move(box.x+82,box.y+65);await page.mouse.down();
 await page.mouse.move(box.x+42,box.y+100,{steps:8});await page.mouse.up();
 after=await camera();near(after.x-before.x,-40);near(after.y-before.y,35);
 checks.push('drag beginning on focus pans without stealing later clicks');
 const map=await page.locator('#usg-map').boundingBox();
 await page.mouse.move(map.x+20,map.y+20);before=await camera();await page.mouse.wheel(0,200);
 await page.waitForFunction(y=>new DOMMatrix(document.querySelector('#usg-world').style.transform).f!==y,before.y);
 after=await camera();near(after.y-before.y,-200);near(after.z,before.z);checks.push('wheel pans vertically');
 before=after;await page.keyboard.down('Shift');await page.mouse.wheel(0,150);await page.keyboard.up('Shift');
 await page.waitForFunction(x=>new DOMMatrix(document.querySelector('#usg-world').style.transform).e!==x,before.x);
 after=await camera();near(after.x-before.x,-150);near(after.y,before.y);checks.push('shift-wheel pans horizontally');
 before=after;await page.keyboard.down('Control');await page.mouse.wheel(0,-120);await page.keyboard.up('Control');
 await page.waitForFunction(z=>new DOMMatrix(document.querySelector('#usg-world').style.transform).a!==z,before.z);
 after=await camera();assert.ok(after.z>before.z);checks.push('control-wheel zooms');
 await page.locator('#usg-overview').click();
 await page.screenshot({path:path.join(out,'PREVIEW_browser.png'),fullPage:true});
 await page.locator('[data-node="COLDWAR_USA_gulf_arm_front"]').evaluate(e=>e.click());
 await page.locator('#usg-detail').screenshot({path:path.join(out,'PREVIEW_resistance_effects.png')});
 await page.locator('[data-node="COLDWAR_USA_gulf_no_fly"]').evaluate(e=>e.click());
 await page.locator('#usg-detail').screenshot({path:path.join(out,'PREVIEW_air_shield_effects.png')});
 assert.deepEqual(errors,[]);
 fs.writeFileSync(path.join(out,'BROWSER_VALIDATION.json'),JSON.stringify({checks,errors,engine_tested:false},null,2));
 await browser.close();console.log(JSON.stringify({checks:checks.length,inspectors:45,errors}));
})().catch(e=>{console.error(e);process.exit(1)});
