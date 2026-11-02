// IMPERIA COLD WAR — Native-size World Ledger paper, preserving the original approval.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
const here=__dirname,source=path.join(here,'source');
const compact=!process.argv.includes('--approved');
const prefix=compact?'world_ledger_compact':'world_ledger';
let browser;
(async()=>{
 browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:736,height:1300},deviceScaleFactor:1,colorScheme:'light'});
 // A local authoring fixture. Host-only carousel controls are unnecessary for the fixed selected design.
 const fragment=fs.readFileSync(path.join(source,'world_ledger_approved.html'),'utf8');
 await page.setContent('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;background:transparent}body{padding:16px} [hidden]{display:none!important}</style></head><body>'+fragment+'</body></html>');
 await page.locator('[data-design="World Ledger"] [data-photo]').evaluate(image=>image.decode());
 if(compact)await page.locator('body').evaluate((body,css)=>{const style=document.createElement('style');style.textContent=css;body.appendChild(style);},fs.readFileSync(path.join(source,'world_ledger_compact.css'),'utf8'));
 await page.waitForTimeout(100);
 const geometry=await page.locator('[data-design="World Ledger"]').evaluate((paper,compact)=>{
  const rect=paper.getBoundingClientRect(),pad=compact?0:18;
  const box=selector=>{const r=paper.querySelector(selector).getBoundingClientRect();return [Math.round(r.x-rect.x+pad),Math.round(r.y-rect.y+pad),Math.round(r.width),Math.round(r.height)];};
  return {project:'IMPERIA COLD WAR',design:'World Ledger',window:[Math.round(rect.width+pad*2),Math.round(rect.height+pad*2)],
   clip:{x:rect.x-pad,y:rect.y-pad,width:Math.round(rect.width+pad*2),height:Math.round(rect.height+pad*2)},
   title:box('[data-title]'),picture:box('[data-photo]'),description:box('[data-report]'),options:box('[data-options]'),
   paper:[pad,pad,Math.round(rect.width),Math.round(rect.height)],
   title_font:{file:'georgiab.ttf',size:compact?24:35,line_height:compact?26:37},body_font:{file:'georgia.ttf',size:16,line_height:23}};
 },compact);
 await page.screenshot({path:path.join(source,compact?'world_ledger_compact_preview.png':'world_ledger_approved_preview.png'),clip:geometry.clip,omitBackground:true});
 await page.locator('[data-design="World Ledger"]').evaluate(paper=>{
  for(const selector of ['[data-title]','[data-photo]','[data-report]','[data-options]'])paper.querySelector(selector).style.visibility='hidden';
  const image=paper.querySelector('[data-photo]');image.removeAttribute('src');
 });
 await page.screenshot({path:path.join(source,prefix+'_background.png'),clip:geometry.clip,omitBackground:true});
 delete geometry.clip;
 fs.writeFileSync(path.join(source,prefix+'_geometry.json'),JSON.stringify(geometry,null,2)+'\n');
 console.log(JSON.stringify(geometry));
 await browser.close();
})().catch(async error=>{if(browser)await browser.close();console.error(error);process.exitCode=1;});
