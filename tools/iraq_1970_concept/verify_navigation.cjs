// Real pointer/wheel regression checks for the Iraq concept; no game changes.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),{pathToFileURL}=require('url');
const out=path.resolve('docs/design/iraq_1970');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1024,height:1150}}),checks=[],errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 try{
  await page.goto(pathToFileURL(path.join(out,'PREVIEW.html')).href);
  await page.locator('.irq-title canvas').last().waitFor();
  const camera=()=>page.locator('#irq-world').evaluate(e=>{const m=new DOMMatrix(e.style.transform);return{x:m.e,y:m.f,z:m.a};});
  const near=(a,b)=>assert.ok(Math.abs(a-b)<1.1,`${a} != ${b}`);
  const node=id=>page.locator(`[data-node="COLDWAR_IRQ_${id}"]`);
  const drag=async(x,y,dx,dy,button='left')=>{await page.mouse.move(x,y);await page.mouse.down({button});await page.mouse.move(x+dx,y+dy,{steps:8});await page.mouse.up({button});};
  await page.locator('#irq-branch').selectOption('iran_war');
  let b=await node('iran_arabistan_claim').boundingBox(),before=await camera();
  const selected=await page.locator('#irq-detail h3').innerText();
  await drag(b.x+82,b.y+65,-75,50);
  let after=await camera();near(after.x-before.x,-75);near(after.y-before.y,50);near(after.z,before.z);
  assert.equal(await page.locator('#irq-detail h3').innerText(),selected);
  checks.push('left drag starting on a focus pans without selecting it');
  b=await node('iran_arabistan_claim').boundingBox();
  before=await camera();await page.mouse.click(b.x+82,b.y+65);after=await camera();
  assert.equal(await page.locator('#irq-detail h3').innerText(),'The Arabistan Claim');
  near(after.x,before.x);near(after.y,before.y);
  checks.push('next normal focus click opens its inspector without moving the camera');
  let map=await page.locator('#irq-map').boundingBox();
  for(const button of ['left','middle','right']){
   before=await camera();await drag(map.x+35,map.y+35,40,25,button);after=await camera();
   near(after.x-before.x,40);near(after.y-before.y,25);checks.push(button+' background drag');
  }
  await page.mouse.move(map.x+30,map.y+30);before=await camera();await page.mouse.wheel(0,180);
  await page.waitForFunction(y=>new DOMMatrix(document.querySelector('#irq-world').style.transform).f!==y,before.y);
  after=await camera();near(after.y-before.y,-180);near(after.z,before.z);checks.push('wheel scrolls vertically without zoom');
  before=await camera();await page.keyboard.down('Shift');await page.mouse.wheel(0,120);await page.keyboard.up('Shift');
  await page.waitForFunction(x=>new DOMMatrix(document.querySelector('#irq-world').style.transform).e!==x,before.x);
  after=await camera();near(after.x-before.x,-120);near(after.y,before.y);checks.push('shift wheel scrolls sideways');
  before=await camera();await page.keyboard.down('Control');await page.mouse.wheel(0,-120);await page.keyboard.up('Control');
  await page.waitForFunction(z=>new DOMMatrix(document.querySelector('#irq-world').style.transform).a!==z,before.z);
  after=await camera();assert.ok(after.z>before.z);checks.push('control wheel zooms');
  // Move from the far-right Iran sector to the far-left Iraqi State, using real wheel input.
  await page.locator('#irq-branch').selectOption('iran_war');
  b=await node('rcc_rules').boundingBox();map=await page.locator('#irq-map').boundingBox();
  await page.mouse.move(map.x+30,map.y+30);before=await camera();
  await page.mouse.wheel(b.x+b.width/2-map.x-map.width/2,b.y+b.height/2-map.y-map.height/2);
  await page.waitForFunction(x=>new DOMMatrix(document.querySelector('#irq-world').style.transform).e!==x,before.x);
  b=await node('rcc_rules').boundingBox();near(b.x+b.width/2,map.x+map.width/2);near(b.y+b.height/2,map.y+map.height/2);
  await page.mouse.click(b.x+b.width/2,b.y+65);
  assert.equal(await page.locator('#irq-detail h3').innerText(),'State of January 1970');
  checks.push('whole-tree traversal: Iran to Iraqi State, then physical focus click');
  // Host state echoes and resize must not snap a manually moved camera back to a branch.
  await page.evaluate(()=>{window.openai={widgetState:null,setWidgetState:async value=>{window.openai.widgetState=value;window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{widgetState:value}}}));}};});
  map=await page.locator('#irq-map').boundingBox();before=await camera();await drag(map.x+30,map.y+30,70,45);after=await camera();
  near(after.x-before.x,70);near(after.y-before.y,45);checks.push('host state echo preserves manual pan');
  before=await camera();await page.setViewportSize({width:736,height:1150});
  await page.waitForFunction(()=>document.querySelector('#irq-map').clientWidth<900);
  await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  after=await camera();near(after.y,before.y);near(after.z,before.z);checks.push('resize preserves manual vertical position and zoom');
  await page.locator('#irq-branch').selectOption('iran_war');await page.locator('#irq-fit').click();
  b=await node('iran_core_khuzestan').boundingBox();await page.mouse.click(b.x+b.width/2,b.y+b.height/2);
  assert.equal(await page.locator('#irq-detail h3').innerText(),'An Iraqi Province');
  assert.ok((await page.locator('#irq-detail').innerText()).includes('730 continuous days'));
  checks.push('new core focus can be physically clicked and inspected');
  await page.screenshot({path:path.join(out,'PREVIEW_navigation_core.png'),fullPage:true});
 }catch(e){errors.push(e.stack||String(e));}
 fs.writeFileSync(path.join(out,'NAVIGATION_VALIDATION.json'),JSON.stringify({errors,checks,scope:'Real Chromium mouse buttons, drag gestures, wheel, modifier keys, host-state echo and resize; browser QA, not HOI4.'},null,2));
 console.log(JSON.stringify({errors,checks}));await browser.close();if(errors.length)process.exitCode=1;
})();
