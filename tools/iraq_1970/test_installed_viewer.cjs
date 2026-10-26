// Browser QA only: actual pointer/wheel interactions and every installed card.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{pathToFileURL}=require('url');
const destination='C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f4e-9042-7b61-be51-9d85f9facd82/iraq-1970-installed.html';
const out=path.resolve('docs/design/iraq_1970/implementation');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'}),page=await browser.newPage({viewport:{width:1024,height:1150}}),checks=[],errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 const camera=()=>page.locator('#cw-world').evaluate(e=>{const m=new DOMMatrix(e.style.transform);return{x:m.e,y:m.f,z:m.a};});
 const near=(a,b)=>assert.ok(Math.abs(a-b)<1.1,`${a} != ${b}`);
 const drag=async(x,y,dx,dy,button='left')=>{await page.mouse.move(x,y);await page.mouse.down({button});await page.mouse.move(x+dx,y+dy,{steps:8});await page.mouse.up({button});};
 try{
  await page.goto(pathToFileURL(destination).href);await page.locator('#cw-installed-viewer[data-ready="true"]').waitFor({timeout:60000});
  assert.equal(await page.locator('.cw-node').count(),410);
  // Every card remains selectable, irrespective of in-game party/focus gates.
  for(const [tag,count]of [['IRQ',410],['USA',228]]){
   await page.locator('#cw-country').selectOption(tag);
   const result=await page.evaluate(()=>{const v=document.querySelector('#cw-installed-viewer')._viewer;for(const n of v.data.trees[v.current().tag].nodes){v.pick(n.id);if(document.querySelector('#cw-detail h3').textContent!==n.t)throw Error('Inspector mismatch '+n.id);}return v.data.trees[v.current().tag].nodes.length;});
   assert.equal(result,count);checks.push(`All ${count} ${tag} installed focus inspectors`);
  }
  await page.locator('#cw-country').selectOption('IRQ');await page.locator('#cw-branch').selectOption('iran_war');
  let box=await page.locator('[data-node="COLDWAR_IRQ_iran_arabistan_claim"]').boundingBox(),before=await camera();
  const initial=await page.locator('#cw-detail h3').innerText();await drag(box.x+82,box.y+65,-60,40);let after=await camera();near(after.x-before.x,-60);near(after.y-before.y,40);assert.equal(await page.locator('#cw-detail h3').innerText(),initial);checks.push('Drag begins on a focus without accidentally selecting it');
  await page.waitForTimeout(200);box=await page.locator('[data-node="COLDWAR_IRQ_iran_arabistan_claim"]').boundingBox();before=await camera();await page.mouse.click(box.x+82,box.y+65);after=await camera();assert.equal(await page.locator('#cw-detail h3').innerText(),'The Arabistan Claim');near(after.x,before.x);near(after.y,before.y);checks.push('Physical focus click opens inspector without recentering');
  let map=await page.locator('#cw-map').boundingBox();
  for(const button of ['left','middle','right']){before=await camera();await drag(map.x+25,map.y+25,30,20,button);after=await camera();near(after.x-before.x,30);near(after.y-before.y,20);checks.push(`${button} background drag`);}
  await page.mouse.move(map.x+30,map.y+30);before=await camera();await page.mouse.wheel(0,150);await page.waitForTimeout(80);after=await camera();near(after.y-before.y,-150);near(after.z,before.z);checks.push('Ordinary wheel pans vertically');
  before=await camera();await page.keyboard.down('Shift');await page.mouse.wheel(0,110);await page.keyboard.up('Shift');await page.waitForTimeout(80);after=await camera();near(after.x-before.x,-110);near(after.y,before.y);checks.push('Shift wheel pans horizontally');
  const point={x:170,y:140};await page.mouse.move(map.x+point.x,map.y+point.y);before=await camera();await page.keyboard.down('Control');await page.mouse.wheel(0,-120);await page.keyboard.up('Control');await page.waitForTimeout(80);after=await camera();assert.ok(after.z>before.z);near((point.x-before.x)/before.z,(point.x-after.x)/after.z);near((point.y-before.y)/before.z,(point.y-after.y)/after.z);checks.push('Control zoom preserves the pointer anchor');
  before=await camera();let mini=await page.locator('#cw-mini').boundingBox();await page.mouse.click(mini.x+20,mini.y+20);after=await camera();assert.ok(Math.abs(after.x-before.x)>20||Math.abs(after.y-before.y)>20);checks.push('Minimap moves across the whole installed tree');
  await page.locator('#cw-branch').selectOption('iran_war');box=await page.locator('[data-node="COLDWAR_IRQ_rcc_rules"]').boundingBox();map=await page.locator('#cw-map').boundingBox();await page.mouse.move(map.x+25,map.y+25);await page.mouse.wheel(box.x+box.width/2-map.x-map.width/2,box.y+65-map.y-map.height/2);await page.waitForTimeout(80);box=await page.locator('[data-node="COLDWAR_IRQ_rcc_rules"]').boundingBox();await page.waitForTimeout(200);await page.mouse.click(box.x+82,box.y+65);assert.equal(await page.locator('#cw-detail h3').innerText(),'State of January 1970');checks.push('Physical whole-tree traversal from Iran to Iraqi State');
  await page.locator('#cw-country').selectOption('USA');await page.evaluate(()=>document.querySelector('#cw-installed-viewer')._viewer.pick('COLDWAR_USA_gulf_no_fly'));
  const detail=await page.locator('#cw-detail').textContent();assert.ok(detail.includes('cas_damage_reduction = 0.25'));assert.ok(detail.includes('air_intercept_efficiency = 0.15'));assert.ok(!detail.includes('proposed integration'));checks.push('USA inspector contains actual native air-idea definitions');
  for(const width of [320,736,1024]){
   await page.setViewportSize({width,height:1150});await page.waitForTimeout(80);
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   const controls=await page.locator('#cw-country').boundingBox();assert.ok(controls.x>=0&&controls.x+controls.width<=width);
   checks.push(`No page/control overflow at ${width}px`);
  }
  // Host state echoes must preserve a manually moved camera.
  await page.evaluate(()=>{window.openai={widgetState:null,setWidgetState:async value=>{window.openai.widgetState=value;window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{widgetState:value}}}));}};});
  map=await page.locator('#cw-map').boundingBox();before=await camera();await drag(map.x+25,map.y+25,50,35);after=await camera();near(after.x-before.x,50);near(after.y-before.y,35);checks.push('Host state echo preserves manual navigation');
  await page.locator('#cw-fit').click();await page.screenshot({path:path.join(out,'INSTALLED_VIEWER_BROWSER.png'),fullPage:true});
 }catch(e){errors.push(e.stack||String(e));}
 const report={scope:'Real Chromium pointer/wheel/keyboard, all638 active inspectors, three responsive widths. No HOI4 engine test.',checks,errors};fs.writeFileSync(path.join(out,'INSTALLED_VIEWER_BROWSER_REPORT.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));await browser.close();if(errors.length)process.exitCode=1;
})();
