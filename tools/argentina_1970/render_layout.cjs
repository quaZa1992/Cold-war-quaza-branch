// IMPERIA COLD WAR — Compact Argentina native-card browser review.
const {chromium}=require('C:/Users/sonyz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const {pathToFileURL}=require('url'),fs=require('fs'),path=require('path');
(async()=>{
 const root=path.resolve(__dirname,'../..'),out=path.join(root,'docs/design/COLDWAR_ARG_1970');
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe'});
 const page=await browser.newPage({viewport:{width:1600,height:1100}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 const source=process.argv[2]||path.join(out,'runtime-preview.html');
 await page.goto(pathToFileURL(source).href);await page.locator('.ar-focus').first().waitFor();
 const expected=JSON.parse(fs.readFileSync(path.join(__dirname,'runtime_design.json'),'utf8'));
 const actual=await page.evaluate(()=>window.COLDWAR_ARG_PREVIEW.data);
 if(JSON.stringify(actual.nodes)!==JSON.stringify(expected.nodes))throw Error('Rendered layout data differs from compiled runtime design');
 await page.evaluate(()=>window.COLDWAR_ARG_PREVIEW.overview());
 const global=await page.evaluate(()=>{
  const bs=[...document.querySelectorAll('.ar-focus')].map(e=>({id:e.dataset.id,x:parseFloat(e.style.left),y:parseFloat(e.style.top),w:165,h:128})),overlaps=[];
  for(let i=0;i<bs.length;i++)for(let j=i+1;j<bs.length;j++){const a=bs[i],b=bs[j];if(Math.min(a.x+a.w,b.x+b.w)>Math.max(a.x,b.x)&&Math.min(a.y+a.h,b.y+b.h)>Math.max(a.y,b.y))overlaps.push([a.id,b.id]);}
  return {focuses:bs.length,overlaps,missingArt:[...document.querySelectorAll('.ar-art')].filter(i=>!i.complete||!i.naturalWidth).length,titleOverflow:[...document.querySelectorAll('.ar-title>span')].filter(s=>s.scrollWidth>147).map(s=>s.textContent)};
 });
 await page.locator('#ar-viewport').screenshot({path:path.join(out,'compact-overview.png')});
 for(const [key,name]of [['army_directives','military'],['social_pact','pj'],['economic_survey','economy'],['sovereignty_dossier','falklands']]){
  await page.evaluate(k=>{window.COLDWAR_ARG_PREVIEW.select(k);const api=window.COLDWAR_ARG_PREVIEW,n=api.data.nodes.find(n=>n.key===k),ns=api.data.nodes.filter(v=>v.group===n.group),vp=document.getElementById('ar-viewport');vp.style.height=((Math.max(...ns.map(n=>n.y))-Math.min(...ns.map(n=>n.y)))*130+180)+'px';vp.scrollTop=0;vp.scrollLeft=0;},key);
  await page.locator('#ar-viewport').screenshot({path:path.join(out,'compact-'+name+'.png')});
 }
 await page.evaluate(()=>{
  window.COLDWAR_ARG_PREVIEW.overview();const c=document.getElementById('ar-canvas'),s=document.getElementById('ar-stage'),v=document.getElementById('ar-viewport');c.style.transform='scale(1)';c.style.top='0';s.style.width=c.style.width;s.style.height=c.style.height;document.getElementById('ar-chapters').style.display='none';v.style.height='1080px';v.scrollLeft=0;v.scrollTop=0;
 });
 await page.locator('#ar-viewport').screenshot({path:path.join(out,'compact-political-neighbours.png')});
 const governments=[];for(const id of Object.keys(actual.parties)){await page.locator('#ar-government').selectOption(id);await page.evaluate(()=>window.COLDWAR_ARG_PREVIEW.overview());governments.push({id,focuses:await page.locator('.ar-focus').count()});}
 const result={project:'IMPERIA COLD WAR',...global,errors,governments,geometryMatchesRuntime:true,render:'Native-sized card composition using existing MD art. Font and routing approximate; not an HOI4 screenshot.',credit:'Millennium Dawn or underlying game art. Individual artists and separate redistribution permissions unknown. See PREVIEW_PROVENANCE.json and runtime-preview-NOTICE.md.'};
 fs.writeFileSync(path.join(out,'compact-browser-qa.json'),JSON.stringify(result,null,2)+'\n');await browser.close();console.log(JSON.stringify(result));
 if(errors.length||global.overlaps.length||global.missingArt||global.titleOverflow.length||governments.some(g=>g.focuses!==299))process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
