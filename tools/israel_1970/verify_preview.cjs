// IMPERIA COLD WAR — Israel 1970 full focus-inspector browser verification.
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
  const labour=design.nodes.find(n=>n.id==='ISR70_p3_ea');
  if(!(await frame.locator('#isr70-selected').innerText()).includes(labour.label))errors.push('selection failed');
  const rewardText=await frame.locator('#isr70-selected').innerText();
  if(!labour.reward_summary.every(line=>rewardText.includes(line)))errors.push('readable focus rewards missing');
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
  await settle();
  if(!(await frame.locator('#isr70-selected h3').innerText()).includes('Entire Focus Tree'))errors.push('overview not active');
  await page.screenshot({path:path.resolve('docs/israel_1970_design/preview_overview.png'),fullPage:true});
  const clicks=[];
  for(const group of design.groups){
    const node=design.nodes.find(n=>n.group===group.id);
    await frame.locator('#isr70-branch').selectOption(group.id);await settle();
    const card=frame.locator(`[data-value="${node.id}"]`);
    await card.focus();
    const beforeClick=await frame.locator('#isr70-world').evaluate(e=>e.style.transform);
    await card.click();await settle();
    if(await frame.locator('#isr70-selected h3').innerText()!==node.label)errors.push('pointer inspection '+node.id);
    if(await frame.locator('#isr70-world').evaluate(e=>e.style.transform)!==beforeClick)errors.push('click moved camera '+node.id);
    clicks.push(node.id);
  }
  const allInspected=await frame.locator('#isr70-tree').evaluate(root=>{
    let count=0;
    for(const node of root.querySelectorAll('[data-action="focus"]')){node.click();if(root.querySelector('#isr70-selected h3').textContent===node.getAttribute('aria-label'))count++;}
    return count;
  });
  if(allInspected!==design.nodes.length)errors.push('some locked/alternative focuses cannot be inspected');
  await page.setViewportSize({width:1680,height:1400});
  await frame.locator('#isr70-branch').selectOption('policy_settlements');await settle();
  await frame.locator('[data-value="ISR70_settlement_unilateral"]').focus();
  await frame.locator('[data-value="ISR70_settlement_unilateral"]').click();await settle();
  await page.screenshot({path:path.resolve('docs/israel_1970_design/preview_settlements.png'),fullPage:true});
  await frame.locator('#isr70-branch').selectOption('policy_presence');await settle();
  for(const slug of ['west_bank','gaza','sinai','golan']){
    const card=frame.locator(`[data-value="ISR70_presence_${slug}"]`);
    await card.focus();await card.click();await settle();
    const text=await frame.locator('#isr70-selected').innerText();
    for(const term of ['Office Productivity +4%','Agricultural Productivity +3%','Agricultural Productivity -3%','Bureaucracy Cost +2.5%','Police Cost +2%','Stability -1%','Local Infrastructure Construction Speed -10%','Local Factory Access -5%','Local Supplies -5%','Israel Treasury: -1%']){
      if(!text.includes(term))errors.push('unilateral settlement terms missing '+slug+'/'+term);
    }
    if(/If accepted|transferred to the host|Civilian Holdings Compact|Negotiate a/.test(text))errors.push('obsolete host agreement shown '+slug);
    const palTerms=['Stability -2%','Political Power Gain -2.5%','Office Productivity -4%','Bureaucracy Cost +4%','Social Costs +3%'];
    if(['west_bank','gaza'].includes(slug)){
      for(const term of palTerms)if(!text.includes(term))errors.push('Palestinian foreign terms missing '+slug+'/'+term);
    }else if(text.includes('Territorial and Settlement Pressures'))errors.push('Palestinian burden on unrelated state '+slug);
  }
  for(const slug of ['west_bank','gaza']){
    const card=frame.locator(`[data-value="ISR70_develop_${slug}"]`);
    await card.focus();await card.click();await settle();
    const text=await frame.locator('#isr70-selected').innerText();
    for(const term of ['Stability -2%','Political Power Gain -2.5%','Office Productivity -4%','Bureaucracy Cost +4%','Social Costs +3%','Stability -4%','Political Power Gain -5%','Office Productivity -8%','Bureaucracy Cost +8%','Social Costs +6%']){
      if(!text.includes(term))errors.push('Palestinian controlled-project terms missing '+slug+'/'+term);
    }
  }
  await frame.locator('#isr70-branch').selectOption('policy_settlements');await settle();
  await frame.locator('[data-value="ISR70_settlement_compensation"]').focus();
  await frame.locator('[data-value="ISR70_settlement_compensation"]').click();await settle();
  const compensationText=await frame.locator('#isr70-selected').innerText();
  for(const term of ['West Bank: Territorial and Settlement Pressures','Gaza: Territorial and Settlement Pressures','Stability -2%','Office Productivity -4%']){
    if(!compensationText.includes(term))errors.push('compensation Palestinian terms missing '+term);
  }
  await frame.locator('#isr70-branch').selectOption('policy_presence');await settle();
  await frame.locator('[data-value="ISR70_presence_west_bank"]').focus();
  await frame.locator('[data-value="ISR70_presence_west_bank"]').click();await settle();
  await page.screenshot({path:path.resolve('docs/israel_1970_design/preview_presence.png'),fullPage:true});
  await frame.locator('#isr70-spirits').click();await settle();
  if(await frame.locator('.occupation-profile').count()!==4)errors.push('occupation profiles missing');
  const occupationText=await frame.locator('#isr70-selected').innerText();
  if(!occupationText.includes('Local Garrison Requirement: +60%')||!occupationText.includes('Israel: Personnel Cost: +8%'))errors.push('occupation costs missing');
  await frame.locator('.occupation-profile').first().scrollIntoViewIfNeeded();await settle();
  await page.screenshot({path:path.resolve('docs/israel_1970_design/preview_occupation.png'),fullPage:true});
  await frame.locator('#isr70-overview').click();await settle();
  await page.screenshot({path:path.resolve('docs/israel_1970_design/preview_overview.png'),fullPage:true});
  console.log(JSON.stringify({errors,views:results.length,pointerClicks:clicks.length,allInspected}));
  const reportPath=path.resolve('docs/israel_1970_design/preview_validation.json');
  const tempPath=reportPath+'.tmp';
  fs.writeFileSync(tempPath,JSON.stringify({project:'IMPERIA COLD WAR',errors,views:results.length,pointerClicks:clicks.length,allInspected,results},null,2));
  fs.renameSync(tempPath,reportPath);
  await browser.close();
  if(errors.length)process.exitCode=1;
})();
