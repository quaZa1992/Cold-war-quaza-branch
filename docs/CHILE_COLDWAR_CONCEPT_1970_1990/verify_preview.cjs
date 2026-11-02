// IMPERIA COLD WAR — Cold War Chile independent browser/model preview checks.
const {chromium}=require('C:/Users/sonyz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url');const path=require('path');const fs=require('fs');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.setViewportSize({width:1180,height:1000});await page.goto(pathToFileURL(path.join(__dirname,'preview-review.html')).href);
 await page.locator('.ch-focus').first().waitFor();
 const data=await page.evaluate(()=>window.COLDWAR_CHL_PREVIEW.data);
 const missingArt=await page.locator('.ch-art').evaluateAll(imgs=>imgs.filter(im=>!im.complete||im.naturalWidth===0).length);
 const sections=await page.locator('#ch-section option').evaluateAll(opts=>opts.map(o=>o.value));const overlaps=[];
 for(const section of sections.filter(x=>x!=='all')){
   await page.locator('#ch-section').selectOption(section);
   const boxes=await page.locator('.ch-focus').evaluateAll(bs=>bs.map(b=>{const r=b.getBoundingClientRect();return{id:b.dataset.id,x:r.x,y:r.y,w:r.width,h:r.height}}));
   for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const a=boxes[i],b=boxes[j];if(Math.min(a.x+a.w,b.x+b.w)>Math.max(a.x,b.x)+1&&Math.min(a.y+a.h,b.y+b.h)>Math.max(a.y,b.y)+1)overlaps.push([a.id,b.id]);}
 }
 for(const n of data.nodes){
   await page.evaluate(id=>window.COLDWAR_CHL_PREVIEW.select(id),n.id);
   const title=await page.locator('#ch-inspector h3').textContent();if(title!==n.title)throw Error('Inspector title '+n.id);
   const body=await page.locator('#ch-inspector').innerText();
   if(!body.includes('Effects'))throw Error('Missing effects '+n.id);
   if(n.agreement&&!body.includes('If they accept'))throw Error('Missing prospective acceptance '+n.id);
 }
 const partyVariants=[];
 for(const gov of ['1','2','3','18','4','19','14','20','0','5','22','22P']){
   await page.locator('#ch-government').selectOption(gov);await page.locator('#ch-section').selectOption('all');
   partyVariants.push({government:gov,nodes:await page.locator('.ch-focus').count()});
 }
 await page.locator('#ch-government').selectOption('1');
 const geometry=await page.evaluate(()=>{
   const cards=[...document.querySelectorAll('.ch-focus')].map(b=>({id:b.dataset.id,x:parseFloat(b.style.left),y:parseFloat(b.style.top),w:165,h:128}));
   const collisions=[];
   for(const edge of document.querySelectorAll('#ch-edges path[data-parent]')){
     const [x1,y1,ym,x2,y2]=edge.getAttribute('d').match(/-?\d+(?:\.\d+)?/g).map(Number);
     const segments=[[x1,y1,x1,ym],[x1,ym,x2,ym],[x2,ym,x2,y2]];
     for(const c of cards){if(c.id===edge.dataset.parent||c.id===edge.dataset.child)continue;
       const hit=segments.some(([ax,ay,bx,by])=>ax===bx?(ax>c.x&&ax<c.x+c.w&&Math.max(ay,by)>c.y&&Math.min(ay,by)<c.y+c.h):(ay>c.y&&ay<c.y+c.h&&Math.max(ax,bx)>c.x&&Math.min(ax,bx)<c.x+c.w));
       if(hit)collisions.push({parent:edge.dataset.parent,child:edge.dataset.child,card:c.id});
     }
   }
   return {links:document.querySelectorAll('#ch-edges path[data-parent]').length,collisions,titleOverflow:[...document.querySelectorAll('.ch-title>span')].filter(s=>s.scrollWidth>s.clientWidth).map(s=>s.textContent)};
 });
 const terms=[];
 for(const a of data.agreements){
   const n=data.nodes.find(n=>n.agreement===a.id);await page.evaluate(id=>window.COLDWAR_CHL_PREVIEW.select(id),n.id);
   const text=await page.locator('#ch-inspector').innerText();const sides=await page.locator('.ch-terms section').all();
   if(sides.length!==(a.partners?.length||1)+1)throw Error('Missing agreement side '+a.id);
   for(let i=0;i<sides.length;i++){
      const t=i===0?a.chile:a.recipient;const sideText=await sides[i].innerText();
      const dollars=[...sideText.matchAll(/\$(\d+(?:\.\d+)?) billion/g)].map(m=>Number(m[1]));
      if(dollars.length!==2||dollars[0]!==t.setup||dollars[1]!==t.weekly)throw Error('Missing exact money terms '+a.id);
      for(const [key,value]of Object.entries(t.modifiers)){
        const amount=key==='interest_rate_multiplier_modifier'?value:value*100;
        const expected=(amount>0?'+':'')+Number(amount.toFixed(3))+(key==='interest_rate_multiplier_modifier'?' pp':'%');
        if(!sideText.includes(expected))throw Error('Missing signed agreement modifier '+a.id+' '+key);
      }
   }
   terms.push({id:a.id,ifAccept:text.includes('If they accept'),sides:sides.length,exactMoneyAndModifiers:true});
 }
 await page.locator('#ch-events').click();for(const ev of data.events){await page.locator('#ch-event').selectOption(ev.key);if(await page.locator('.ch-choice').count()!==ev.options.length)throw Error('Event option coverage '+ev.key);}
 const responsive=[];
 for(const width of [1180,736,360]){
   await page.setViewportSize({width,height:1000});await page.evaluate(()=>window.COLDWAR_CHL_PREVIEW.select('pdc_social'));
   const overflow=await page.evaluate(()=>({window:document.documentElement.clientWidth,scroll:document.documentElement.scrollWidth}));
   responsive.push({width,...overflow});if(width===1180)await page.screenshot({path:path.join(__dirname,'preview-pdc.png'),fullPage:true});if(width===360)await page.screenshot({path:path.join(__dirname,'preview-mobile.png'),fullPage:true});
 }
 await page.setViewportSize({width:1180,height:1000});await page.locator('#ch-government').selectOption('22P');await page.evaluate(()=>window.COLDWAR_CHL_PREVIEW.select('pinochet_chicago'));await page.screenshot({path:path.join(__dirname,'preview-pinochet.png'),fullPage:true});
 await page.evaluate(()=>window.COLDWAR_CHL_PREVIEW.select('soviet_machinery'));await page.screenshot({path:path.join(__dirname,'preview-agreement.png'),fullPage:true});
 await page.evaluate(()=>window.COLDWAR_CHL_PREVIEW.overview());await page.locator('.ch-viewport').screenshot({path:path.join(__dirname,'preview-overview.png')});
 await page.locator('#ch-spirits').click();await page.locator('#ch-inspector').screenshot({path:path.join(__dirname,'preview-starting-spirits.png')});
 const report={project:'IMPERIA COLD WAR',inspectedFocuses:data.nodes.length,inspectedEvents:data.events.length,missingArt,overlaps,geometry,partyVariants,agreementTerms:terms,responsive,errors,engineTested:false};
 fs.writeFileSync(path.join(__dirname,'BROWSER_QA.json'),JSON.stringify(report,null,2)+'\n');
 await browser.close();console.log(JSON.stringify(report));
 if(errors.length||missingArt||overlaps.length||geometry.collisions.length||geometry.titleOverflow.length||responsive.some(r=>r.scroll>r.window+1)||partyVariants.some(v=>v.nodes!==data.nodes.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
