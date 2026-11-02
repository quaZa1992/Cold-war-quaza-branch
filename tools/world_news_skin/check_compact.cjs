// IMPERIA COLD WAR — Full compact title/report reachability in the authoring fixture.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path');
let browser;
(async()=>{
 const here=__dirname;
 browser=await chromium.launch({executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',headless:true});
 const page=await browser.newPage({viewport:{width:736,height:900},colorScheme:'light'});
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.setContent('<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0}body{padding:16px}[hidden]{display:none!important}</style></head><body>'+fs.readFileSync(path.join(here,'source/world_ledger_approved.html'),'utf8')+'</body></html>');
 await page.locator('body').evaluate((body,css)=>{const style=document.createElement('style');style.textContent=css;body.appendChild(style);},fs.readFileSync(path.join(here,'source/world_ledger_compact.css'),'utf8'));
 const result=await page.locator('[data-design="World Ledger"]').evaluate(paper=>{
  const title=paper.querySelector('[data-title]'),body=paper.querySelector('[data-report]');
  title.textContent=('A lengthy international headline concerning economic and diplomatic developments. ').repeat(7)+'FINAL HEADLINE WORDS';
  body.textContent=('A detailed international report remains available in full through its scrollable text field. ').repeat(120)+'FINAL REPORT WORDS';
  const titleOverflow=title.scrollHeight>title.clientHeight,bodyOverflow=body.scrollHeight>body.clientHeight;
  title.scrollTop=title.scrollHeight;body.scrollTop=body.scrollHeight;
  const endVisible=el=>{const range=document.createRange(),node=el.firstChild;range.setStart(node,Math.max(0,node.length-10));range.setEnd(node,node.length);const last=range.getBoundingClientRect(),box=el.getBoundingClientRect();return last.top>=box.top-1&&last.bottom<=box.bottom+2;};
  const t=title.getBoundingClientRect(),image=paper.querySelector('[data-photo]').getBoundingClientRect(),b=body.getBoundingClientRect(),footer=paper.querySelector('.event-responses').getBoundingClientRect();
  return {window:[paper.offsetWidth,paper.offsetHeight],titleOverflow,bodyOverflow,titleFinalWordsReachable:endVisible(title),reportFinalWordsReachable:endVisible(body),titleDoesNotOverlapPhoto:t.bottom<image.top,reportDoesNotOverlapFooter:b.bottom<footer.top,titleRetained:title.textContent.endsWith('FINAL HEADLINE WORDS'),reportRetained:body.textContent.endsWith('FINAL REPORT WORDS')};
 });
 if(errors.length||result.window[0]!==528||result.window[1]!==595||Object.entries(result).some(([key,value])=>key!=='window'&&!value))throw new Error(JSON.stringify({result,errors}));
 const report={project:'IMPERIA COLD WAR',status:'PASS',scope:'Compact browser authoring fixture. Native text control bindings checked separately; no engine/UI/MP test.',...result,errors};
 fs.writeFileSync(path.join(here,'COMPACT_TEXT_CHECK.json'),JSON.stringify(report,null,2)+'\n');
 await browser.close();console.log(JSON.stringify(report));
})().catch(async error=>{if(browser)await browser.close();console.error(error);process.exitCode=1;});
