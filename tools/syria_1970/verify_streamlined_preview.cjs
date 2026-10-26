// IMPERIA CW — Cold War: browser review of the installed Syrian reform preview.
const fs=require('fs'),path=require('path'),os=require('os');
const {pathToFileURL}=require('url');
const {chromium}=require(path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));
(async()=>{
  const file=path.resolve(process.argv[2]);
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const page=await browser.newPage({viewport:{width:1280,height:960}}),errors=[],views=[];
  page.on('pageerror',e=>errors.push(e.message));
  try {
    await page.goto(pathToFileURL(file).href);
    await page.locator('.focus-node').first().waitFor({state:'attached'});
    for(const width of [736,1280]){
      await page.setViewportSize({width,height:960});
      for(const group of ['opening','baath','industry','agriculture','infrastructure','army','navy','great_powers','limited_war','outlooks']){
        await page.locator('#syr70-section').selectOption(group);
        const status=await page.locator('#syr70-tree').evaluate(el=>({nodes:el.querySelectorAll('.focus-node').length,missing:[...el.querySelectorAll('.focus-node img')].filter(i=>!i.complete||!i.naturalWidth).length}));
        if(status.nodes!==420||status.missing)errors.push({width,group,...status});
        views.push({width,group,...status});
      }
    }
    const checks=[['industry','COLDWAR_SYR_industry_06',['Civilian Factory Productivity: +6%']],['army','COLDWAR_SYR_army_03',['25%','Planning Speed: +8%']],['limited_war','COLDWAR_SYR_limited_war_reserves',['Army Personnel Expenditure: +3.5%','Army Org']]];
    for(const [group,id,expected] of checks){
      await page.locator('#syr70-section').selectOption(group);
      await page.locator('[data-id="'+id+'"]').evaluate(el=>el.click());
      const text=await page.locator('#syr70-detail').innerText();
      for(const term of expected)if(!text.toLowerCase().includes(term.toLowerCase()))errors.push({id,missingInspector:term});
    }
    await page.locator('#syr70-section').selectOption('limited_war');
    await page.screenshot({path:path.join(path.dirname(file),'syria-streamlined-review.png'),fullPage:true});
    const report={scope:'Browser/source preview only; no HOI4 engine claim',views:views.length,errors,checks:views};
    fs.writeFileSync(path.join(__dirname,'../../docs/syria_1970_streamlining_20261021/PREVIEW_REVIEW.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify({views:views.length,errors}));
    if(errors.length)process.exitCode=1;
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
