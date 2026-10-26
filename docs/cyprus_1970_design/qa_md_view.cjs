const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const design=JSON.parse(fs.readFileSync(path.join(__dirname,'coldwar_cyprus_1970_design.json'),'utf8'));
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const views=[];
  for(const width of [1024,736,360]){
    await page.setViewportSize({width,height:1200});
    await page.goto(pathToFileURL(path.join(__dirname,'md-view-qa.html')).href);
    const frame=page.frameLocator('iframe'),root=frame.locator('#coldwar-cyprus-md');
    await frame.locator('[data-ready="true"]').waitFor();
    const count=await frame.locator('#md-jump option[value^="n:"]').count();
    const starters=await frame.locator('#md-spirit-grid [data-spirit]').count();
    await frame.locator('[data-spirit="COLDWAR_CYP_1970_tc_parallel_administration"]').click();
    if(!(await frame.locator('#md-selection').textContent()).toLowerCase().includes('police'))throw Error('Starting spirit details missing');
    await frame.locator('#md-tc').click();
    if(!(await frame.locator('#md-selection h3').textContent()).includes('Community'))throw Error('Turkish Cypriot shortcut failed');
    await frame.locator('#md-war').click();
    if(!(await frame.locator('#md-selection h3').textContent()).includes('Armed Patrons'))throw Error('Road to war shortcut failed');
    if(width===1024){await page.waitForTimeout(80);await root.screenshot({path:path.join(__dirname,'md-road-to-war.png')});}
    await frame.locator('#md-jump').selectOption('n:COLDWAR_CYP_1970_war_civilian_guard');
    if(!(await frame.locator('#md-selection').textContent()).includes('Coup pressure: -10'))throw Error('Coup-pressure effect missing');
    await frame.locator('#md-jump').selectOption('n:COLDWAR_CYP_1970_war_guarantors');
    if(!(await frame.locator('#md-selection').textContent()).includes('Fast crisis response'))throw Error('Crisis timing explanation missing');
    const rootKey='COLDWAR_CYP_1970_republic_at_ten';
    await frame.locator('#md-jump').selectOption('n:'+rootKey);
    await page.waitForTimeout(50);
    if(await root.getAttribute('data-selected')!==rootKey)throw Error('Focus jump failed');
    const before=Number(await root.getAttribute('data-scale'));
    await frame.locator('#md-in').click();await page.waitForTimeout(40);
    const after=Number(await root.getAttribute('data-scale'));
    if(after<=before)throw Error('Zoom failed');
    await frame.locator('#md-native').click();await page.waitForTimeout(40);
    const native=Number(await root.getAttribute('data-scale'));
    if(Math.abs(native-1)>.01)throw Error('Native zoom failed');
    const canvas=frame.locator('#md-world');await canvas.scrollIntoViewIfNeeded();
    const box=await canvas.boundingBox();
    const oldPan=Number(await root.getAttribute('data-pan-x'));
    await page.mouse.move(box.x+box.width/2,box.y+box.height/2);
    await page.mouse.down();await page.mouse.move(box.x+box.width/2+70,box.y+box.height/2+25,{steps:4});await page.mouse.up();await page.waitForTimeout(40);
    const newPan=Number(await root.getAttribute('data-pan-x'));
    if(Math.abs(newPan-oldPan)<60)throw Error('Drag pan failed at width '+width+': '+oldPan+' → '+newPan);
    await frame.locator('#md-jump').selectOption('n:'+rootKey);await page.waitForTimeout(40);
    await canvas.click({position:{x:box.width/2,y:box.height/2}});
    if(await root.getAttribute('data-selected')!==rootKey)throw Error('Canvas hit test failed');
    await frame.locator('#md-grid').check();
    const sectionValues=await frame.locator('#md-jump option[value^="s:"]').evaluateAll(ns=>ns.map(n=>n.value));
    for(const value of sectionValues)await frame.locator('#md-jump').selectOption(value);
    await frame.locator('#md-all').click();await page.waitForTimeout(80);
    if(width===1024){await canvas.scrollIntoViewIfNeeded();await canvas.screenshot({path:path.join(__dirname,'md-full-overview.png')});}
    const allScale=Number(await root.getAttribute('data-scale'));
    const allBox=await canvas.boundingBox();
    const maxX=Math.max(...design.focuses.map(n=>n.x));
    if((380+90*maxX)*allScale>allBox.width+1)throw Error('Whole-tree view clipped at width '+width);
    await frame.locator('#md-opening').click();await page.waitForTimeout(80);
    if(width===1024){await canvas.scrollIntoViewIfNeeded();await canvas.screenshot({path:path.join(__dirname,'md-opening.png')});}
    if(width===360){await canvas.scrollIntoViewIfNeeded();await canvas.screenshot({path:path.join(__dirname,'md-mobile.png')});}
    if(width===1024){await frame.locator('#md-tc').click();await page.waitForTimeout(80);await canvas.scrollIntoViewIfNeeded();await canvas.screenshot({path:path.join(__dirname,'md-turkish-cypriots.png')});}
    const painted=await canvas.evaluate(c=>{const a=c.getContext('2d').getImageData(0,0,c.width,c.height).data;let count=0;for(let i=3;i<a.length;i+=4)if(a[i])count++;return count;});
    if(painted<100)throw Error('Empty focus canvas at width '+width);
    const overflow=await root.evaluate(el=>({width:el.clientWidth,scroll:el.scrollWidth}));
    views.push({width,focusOptions:count,startingSpirits:starters,sections:sectionValues.length,allScale,paintedPixels:painted,zoom:true,dragPan:true,canvasSelection:true,turkishCypriotShortcut:true,roadToWarShortcut:true,overflow});
  }
  await browser.close();
  const report={errors,views};fs.writeFileSync(path.join(__dirname,'MD_VIEW_QA.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
  if(errors.length||views.some(v=>v.focusOptions!==design.focuses.length||v.sections!==design.sections.length||v.startingSpirits!==design.starting_spirits.filter(s=>s.activation==='start').length||v.overflow.scroll>v.overflow.width+1))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
