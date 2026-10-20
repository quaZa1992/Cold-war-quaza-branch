const { chromium } = require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
(async () => {
  const browser = await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const page = await browser.newPage({viewport:{width:780,height:1050}});
  const errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(pathToFileURL(path.resolve('docs/israel_1970_design/preview.html')).href);
  const frame=page.frameLocator('iframe');
  const settle=async()=>{await page.waitForTimeout(100);};
  await frame.locator('#isr70-branch').waitFor();
  const options=await frame.locator('#isr70-branch option').evaluateAll(elements=>elements.map(e=>e.value));
  const results=[];
  const design=JSON.parse(fs.readFileSync(path.resolve('tools/israel_1970/english_design.json'),'utf8'));
  const expectedEdges=design.nodes.reduce((sum,n)=>sum+n.visual_prerequisites.reduce((total,row)=>total+row.length,0),0);
  for(const width of [320,736,1024]) {
    await page.setViewportSize({width,height:1100});
    for(const branch of options) {
      await frame.locator('#isr70-branch').selectOption(branch);
      await settle();
      const info=await frame.locator('#isr70-tree').evaluate(root=>({
        overflow:root.scrollWidth>root.clientWidth+2,
        nodes:root.querySelectorAll('[data-action="focus"]').length,
        edges:root.querySelectorAll('.focus-connections .prerequisite').length,
        controlsOutside:[...root.querySelectorAll('.focus-toolbar button,.focus-toolbar select')].some(b=>b.getBoundingClientRect().right>root.getBoundingClientRect().right+2)
      }));
      if(info.overflow||info.controlsOutside)errors.push(`overflow ${width} ${branch}: ${JSON.stringify(info)}`);
      if(info.nodes!==design.nodes.length||info.edges!==expectedEdges)errors.push(`incomplete focus map ${branch}`);
      results.push({width,branch,...info});
    }
    await frame.locator('#isr70-overview').click();
    await settle();
    if(await frame.locator('#isr70-tree').evaluate(root=>root.scrollWidth>root.clientWidth+2))errors.push(`overview overflow ${width}`);
    await frame.locator('#isr70-spirits').click();
    await settle();
    if(await frame.locator('.spirit-list article').count()!==7)errors.push('starting spirit count');
  }
  await page.setViewportSize({width:1024,height:1200});
  await frame.locator('#isr70-branch').selectOption('party_3');
  await settle();
  await frame.locator('[data-value="ISR70_p3_ea"]').click();
  await settle();
  if(!(await frame.locator('#isr70-selected').innerText()).includes('Modernize the Histadrut'))errors.push('selection failed');
  const rewardText=await frame.locator('#isr70-selected').innerText();
  if(!rewardText.includes('Production Efficiency Cap: +5%')||!rewardText.includes('Labor Unions Opinion: +15'))errors.push('readable focus rewards missing');
  await page.screenshot({path:path.resolve('docs/israel_1970_design/preview_alignment.png'),fullPage:true});
  const before=await frame.locator('#isr70-world').evaluate(e=>({transform:e.style.transform,nodeX:e.querySelector('[data-value="ISR70_p3_ea"]').style.left}));
  await frame.locator('#isr70-plus').click();
  await settle();
  const after=await frame.locator('#isr70-world').evaluate(e=>({transform:e.style.transform,nodeX:e.querySelector('[data-value="ISR70_p3_ea"]').style.left}));
  if(before.transform===after.transform||before.nodeX!==after.nodeX)errors.push('zoom must move camera without rearranging nodes');
  await frame.locator('#isr70-branch').selectOption('territories');
  await settle();
  await page.screenshot({path:path.resolve('docs/israel_1970_design/preview_territories.png'),fullPage:true});
  await frame.locator('#isr70-branch').selectOption('defense');
  await settle();
  await page.screenshot({path:path.resolve('docs/israel_1970_design/preview_defense.png'),fullPage:true});
  await frame.locator('#isr70-overview').click();
  await page.screenshot({path:path.resolve('docs/israel_1970_design/preview_overview.png'),fullPage:true});
  fs.writeFileSync(path.resolve('docs/israel_1970_design/preview_validation.json'),JSON.stringify({errors,views:results.length,results},null,2));
  console.log(JSON.stringify({errors,views:results.length}));
  await browser.close();
  if(errors.length)process.exitCode=1;
})();
