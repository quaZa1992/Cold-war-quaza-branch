const {chromium}=require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
 const page=await browser.newPage({viewport:{width:1024,height:1150}});
 await page.goto(pathToFileURL(path.join(__dirname,'PREVIEW.html')).href);
 await page.locator('.uae-title canvas').last().waitFor();
 await page.locator('#uae-branch').selectOption('oil');
 await page.locator('#uae-fit').click();
 await page.locator('[data-node="COLDWAR_UAE_adia_savings"]').click();
 const text=await page.locator('#uae-detail').innerText();
 if(!text.includes('Annual native investment return: +0.5 percentage points')||!text.includes('cash-only reserve ledger earns no income'))throw Error('Final savings effect missing from inspector');
 await page.screenshot({path:path.join(__dirname,'PREVIEW_savings_effects.png'),fullPage:true});
 fs.writeFileSync(path.join(__dirname,'FINAL_SAVINGS_VALIDATION.json'),JSON.stringify({errors:[],focus:'COLDWAR_UAE_adia_savings',annual_native_return_points:0.5,cash_reserve_income:0},null,2));
 await browser.close();console.log('Final savings inspector: +0.5 annual native ROI points and zero cash-ledger income verified');
})().catch(e=>{console.error(e);process.exitCode=1});
