// IMPERIA COLD WAR — Browser verification of individual MD update choices.
const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(pathToFileURL(path.resolve('docs/md_update_203_20261028/file_review_preview.html')).href);
 const frame=page.frameLocator('iframe');await frame.locator('#md203-file').waitFor();
 const options=await frame.locator('#md203-file option').evaluateAll(nodes=>nodes.map(n=>n.value));
 if(options.length!==73)errors.push('Not all 73 file choices are available');
 let checked=0;
 for(const width of [320,736,1024]){
  await page.setViewportSize({width,height:1100});
  for(const file of options){
   await frame.locator('#md203-file').selectOption(file);
   if(await frame.locator('#md203-path').textContent()!==file)errors.push('Selection mismatch '+file);
   const overflow=await frame.locator('#md203-files').evaluate(root=>document.documentElement.scrollWidth>document.documentElement.clientWidth+2||root.scrollWidth>root.clientWidth+2);
   if(overflow)errors.push('Overflow '+width+' '+file);
   if(!(await frame.locator('#md203-proposal').textContent()).trim())errors.push('Missing proposed action '+file);
   checked++;
  }
 }
 await frame.locator('#md203-file').selectOption('descriptor.mod');
 const proposed=await frame.locator('#md203-proposal-diff').innerText();
 if(!proposed.includes('+version="2.0.3"')||!proposed.includes('name="MD Cold War"'))errors.push('Descriptor preview must preserve Cold War identity');
 await frame.locator('#md203-file').selectOption(options[0]);await frame.locator('#md203-next').click();
 if(await frame.locator('#md203-file').inputValue()!==options[1])errors.push('Next-file navigation');
 await frame.locator('#md203-prev').click();
 if(await frame.locator('#md203-file').inputValue()!==options[0])errors.push('Previous-file navigation');
 await page.setViewportSize({width:780,height:1100});
 await page.screenshot({path:path.resolve('docs/md_update_203_20261028/file_review_preview.png'),fullPage:true});
 const report={project:'IMPERIA COLD WAR',status:errors.length?'FAIL':'PASS',errors,file_choices:options.length,views_checked:checked,native_test:false};
 fs.writeFileSync('docs/md_update_203_20261028/file_review_browser.json',JSON.stringify(report,null,2)+'\n');
 console.log(JSON.stringify(report));await browser.close();if(errors.length)process.exitCode=1;
})();
