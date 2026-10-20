/* Browser QA for the preview resolved from emitted Syria focus scripts. */
const {chromium} = require('C:/Users/sonyz/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs'), path = require('path'), {pathToFileURL} = require('url');
let browser;
(async () => {
  const output = process.argv[2];
  if (!output) throw new Error('Usage: node verify_preview.cjs <preview-directory>');
  const design = JSON.parse(fs.readFileSync(path.join(__dirname, 'manifest.json'), 'utf8'));
  browser = await chromium.launch({headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const page = await browser.newPage({viewport: {width: 1024, height: 1400}}), errors = [], checks = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(pathToFileURL(path.join(output, 'preview.html')).href);
  const frame = page.frameLocator('iframe');
  await frame.locator('.focus-node').first().waitFor({state: 'attached'});
  await frame.locator('.focus-node img').first().evaluate(img => img.decode());
  const edges = design.nodes.reduce((sum, n) => sum+n.prerequisites.flat().length, 0);
  for (const width of [320, 736, 1024]) {
    await page.setViewportSize({width, height: 1400});
    for (const group of design.groups) {
      await frame.locator('#syr70-section').selectOption(group.id);
      const result = await frame.locator('#syr70-tree').evaluate((el, ids) => {
        const bounds = el.querySelector('.game-viewport').getBoundingClientRect();
        return {
          overflow: el.scrollWidth > el.clientWidth+2,
          nodes: el.querySelectorAll('.focus-node').length,
          edges: el.querySelectorAll('.prerequisite').length,
          missing: [...el.querySelectorAll('.focus-node img')].filter(img => !img.complete || !img.naturalWidth).length,
          clipped: [...el.querySelectorAll('.focus-node')].filter(b => ids.includes(b.dataset.id)).filter(b => {
            const r = b.getBoundingClientRect();
            return r.left < bounds.left-1 || r.right > bounds.right+1 || r.top < bounds.top-1 || r.bottom > bounds.bottom+1;
          }).map(b => b.dataset.id)
        };
      }, design.nodes.filter(n => n.group === group.id).map(n => n.id));
      if (result.overflow || result.nodes !== 420 || result.edges !== edges || result.missing || result.clipped.length) errors.push({width, group: group.id, ...result});
      checks.push({width, group: group.id, ...result});
    }
  }
  await page.setViewportSize({width: 1024, height: 1400});
  for (const group of ['opening', 'hafez', 'agriculture', 'citizenship', 'limited_war', 'outlooks', 'brotherhood', 'army']) {
    await frame.locator('#syr70-section').selectOption(group);
    await page.evaluate(() => window.scrollTo(0, 0));
    await frame.locator('#syr70-tree').evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({path: path.join(output, 'preview-'+group+'.png'), fullPage: true});
  }
  await frame.locator('#syr70-section').selectOption('army');
  await frame.locator('[data-id="COLDWAR_SYR_army_entry"]').evaluate(el => el.click());
  const army = await frame.locator('#syr70-detail').innerText();
  if (!army.includes('Army organization: +2%') || !army.includes('Supply consumption: +1%') || army.includes('Opens the following policy choices')) errors.push('Lessons of1967 actual bonus/burden absent');
  await frame.locator('#syr70-section').selectOption('brotherhood');
  await frame.locator('[data-id="COLDWAR_SYR_brotherhood_05"]').evaluate(el => el.click());
  let civilian = await frame.locator('#syr70-detail').innerText();
  const narrative = design.nodes.find(n => n.id === 'COLDWAR_SYR_brotherhood_05').description;
  if (!civilian.includes(narrative) || !civilian.includes('$3.500 billion')) errors.push('Civilian Institutes narrative or cost absent');
  await page.screenshot({path: path.join(output, 'preview-civilian-institutes.png'), fullPage: true});
  await frame.locator('#syr70-section').selectOption('agriculture');
  await frame.locator('[data-id="COLDWAR_SYR_agriculture_09"]').evaluate(el => el.click());
  let text = await frame.locator('#syr70-detail').innerText();
  if (!text.includes('$7.000 billion')) errors.push('Current focus cost absent from Tabqa inspector');
  await frame.locator('#syr70-detail details').nth(1).locator('summary').click();
  text = await frame.locator('#syr70-detail').innerText();
  if (!text.includes('renewable_energy_infra') || !text.includes('treasury_change = -7') || !text.includes('994')) errors.push('Installed Tabqa effect code absent');
  await frame.locator('#syr70-section').selectOption('levant');
  await frame.locator('[data-id="COLDWAR_SYR_levant_02"]').evaluate(el => el.click());
  await frame.locator('#syr70-detail details').nth(1).locator('summary').click();
  if (!(await frame.locator('#syr70-detail').innerText()).includes('create_wargoal')) errors.push('Installed war-goal adapter absent');
  await frame.locator('#syr70-spirits').click();
  if (await frame.locator('#syr70-detail article').count() !== 7) errors.push('Starting spirit coverage');
  await frame.locator('#syr70-all').click();
  await frame.locator('.game-window').screenshot({path: path.join(output, 'preview-overview.png')});
  fs.writeFileSync(path.join(__dirname, 'preview_validation.json'), JSON.stringify({errors, views: checks.length, edges, checks}, null, 2));
  console.log(JSON.stringify({errors, views: checks.length, edges}));
  await browser.close();
  if (errors.length) process.exitCode = 1;
})().catch(async error => { console.error(error); if (browser) await browser.close(); process.exitCode = 1; });
