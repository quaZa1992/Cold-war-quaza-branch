/* Design preview QA only: no game files are loaded or changed. */
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path=require('path');
const {pathToFileURL}=require('url');
const fs=require('fs');
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const page=await browser.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const results=[];
  for(const width of [736,1024,360]){
    await page.setViewportSize({width,height:950});
    await page.goto(pathToFileURL(path.join(__dirname,'preview-qa.html')).href);
    const frame=page.frameLocator('iframe');
    await frame.locator('#cw-section').waitFor();
    const values=await frame.locator('#cw-section option').evaluateAll(ns=>ns.map(n=>n.value));
    const overlaps=[];
    for(const value of values){
      await frame.locator('#cw-section').selectOption(value);
      const visibleButtons=await frame.locator('.cw-graph .cw-node').evaluateAll(bs=>bs.map(b=>{
        const r=b.getBoundingClientRect();return{id:b.querySelector('button').dataset.focus,x:r.x,y:r.y,w:r.width,h:r.height,visible:!!b.getClientRects().length};
      }));
      for(let i=0;i<visibleButtons.length;i++)for(let j=i+1;j<visibleButtons.length;j++){
        const a=visibleButtons[i],b=visibleButtons[j];
        if(a.visible&&b.visible&&Math.min(a.x+a.w,b.x+b.w)-Math.max(a.x,b.x)>1&&Math.min(a.y+a.h,b.y+b.h)-Math.max(a.y,b.y)>1)overlaps.push([value,a.id,b.id]);
      }
      const active=width<560?frame.locator('.cw-mobile button').last():frame.locator('.cw-graph button').last();
      await active.click();
      if(!(await frame.locator('#cw-details h3').textContent()))throw Error('No selected focus detail');
    }
    await frame.locator('#cw-spirits').click();
    const starterRows=await frame.locator('#cw-content tbody tr').count();
    await frame.locator('#cw-atlas').click();
    const atlasDots=await frame.locator('.cw-atlas circle').count();
    await frame.locator('#cw-section').selectOption('constitution');
    const overflow=await frame.locator('#coldwar-cyprus-design').evaluate(el=>({scroll:el.scrollWidth,width:el.clientWidth}));
    if(width===736)await frame.locator('#coldwar-cyprus-design').screenshot({path:path.join(__dirname,'preview-desktop.png')});
    if(width===360)await frame.locator('#coldwar-cyprus-design').screenshot({path:path.join(__dirname,'preview-mobile.png')});
    results.push({width,sections:values.length,starterRows,atlasDots,overlaps,overflow});
  }
  await browser.close();
  const report={errors,viewports:results};
  fs.writeFileSync(path.join(__dirname,'PREVIEW_QA.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report));
  if(errors.length||results.some(r=>r.overlaps.length||r.starterRows!==7||r.atlasDots!==330||r.overflow.scroll>r.overflow.width+2))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
