// IMPERIA COLD WAR — Verify the proposed France party-programme comparison preview.
const { chromium } = require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const crypto = require('crypto');

const here = __dirname;
const preview = path.join(here, 'PREVIEW.html');
const screenshots = path.join(here, 'screenshots');
const proposal = JSON.parse(fs.readFileSync(path.join(here, 'proposal.json'), 'utf8'));
const baseline = JSON.parse(fs.readFileSync(path.join(here, 'BASELINE.json'), 'utf8'));
const changes = JSON.parse(fs.readFileSync(path.join(here, 'CHANGES.json'), 'utf8'));
fs.mkdirSync(screenshots, { recursive: true });
const rows = effects => (effects || []).reduce((total, e) => total + (e.kind === 'building' ? 2 : 1), 0);

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage({ viewport: { width: 1024, height: 1400 }, deviceScaleFactor: 1 });
  const failures = [], fitViews = [], offerChecks = [], screenshotsWritten = [];
  page.on('pageerror', error => failures.push(`pageerror: ${error.message}`));
  await page.goto(pathToFileURL(preview).href);
  await page.locator('[data-key="soviet_friendship"]').waitFor();

  async function state() {
    return page.evaluate(() => ({
      mode: window.francePartyPreview.getView().mode,
      focuses: window.francePartyPreview.data().nodes.length,
      offers: window.francePartyPreview.data().nodes.filter(n => n.offer).length,
      groups: window.francePartyPreview.data().groups.length,
      shortcuts: document.querySelectorAll('#fr-shortcuts button').length,
      banner: !document.querySelector('#fr-proposal-banner').hidden,
      brokenImages: [...document.querySelectorAll('#france-party-deals-preview img')].filter(i => !i.complete || !i.naturalWidth).length,
    }));
  }
  let loaded = await state();
  if (loaded.mode !== 'proposed' || loaded.focuses !== 156 || loaded.offers !== 35 || loaded.groups !== 14 || !loaded.banner || loaded.brokenImages) failures.push({ initial_load: loaded });
  if (await page.locator('#fr-section').inputValue() !== 'pcf') failures.push('initial section is not PCF');

  const proposedTitleIssues = await page.evaluate(() => {
    const c = document.createElement('canvas').getContext('2d'); c.font = '15px Arial';
    return window.francePartyPreview.data().nodes.filter(n => c.measureText(n.title).width > 147).map(n => ({ key:n.key,title:n.title,width:c.measureText(n.title).width }));
  });
  if (proposedTitleIssues.length) failures.push({ proposed_title_overflows: proposedTitleIssues });
  const connectorIssues = await page.evaluate(() => {
    const collisions=[];
    for(const mode of ['current','proposed']){
      const nodes=window.francePartyPreview.pack[mode].nodes,byKey=Object.fromEntries(nodes.map(n=>[n.key,n]));
      for(const child of nodes)for(const group of child.prerequisites||[])for(const key of group){
        const parent=byKey[key];if(!parent||parent.y>=child.y)continue;
        const x1=parent.x*96+82.5,y1=parent.y*130+128,x2=child.x*96+82.5,y2=child.y*130;
        for(const card of nodes){if(card.key===parent.key||card.key===child.key)continue;const l=card.x*96,t=card.y*130,r=l+165,b=t+128;const vertical=l<=x1&&x1<=r&&Math.max(y1,t)<Math.min(y2-1,b);const horizontal=t<=y2-1&&y2-1<=b&&Math.max(Math.min(x1,x2),l)<Math.min(Math.max(x1,x2),r);if(vertical||horizontal)collisions.push({mode,parent:parent.key,child:child.key,blocked_by:card.key});}
      }
    }
    return collisions;
  });
  if(connectorIssues.length)failures.push({connector_collisions:connectorIssues});

  for (const width of [320, 736, 1024]) {
    await page.setViewportSize({ width, height: 1400 });
    const outer = await page.locator('#france-party-deals-preview').evaluate(root => ({ overflow: root.scrollWidth > root.clientWidth + 2, client: root.clientWidth, scroll: root.scrollWidth }));
    if (outer.overflow) failures.push({ width, root_overflow: outer });
    for (const group of proposal.groups) {
      await page.locator('#fr-section').selectOption(group.id);
      const clipped = await page.locator('#fr-map').evaluate((map, groupId) => {
        const bounds = map.getBoundingClientRect();
        const nodes = window.francePartyPreview.data().nodes.filter(n => n.group === groupId);
        return nodes.filter(n => { const box=map.querySelector(`[data-key="${CSS.escape(n.key)}"]`).getBoundingClientRect(); return box.left<bounds.left-1||box.right>bounds.right+1||box.top<bounds.top-1||box.bottom>bounds.bottom+1; }).map(n=>n.key);
      }, group.id);
      fitViews.push({ width, group: group.id, clipped: clipped.length });
      if (clipped.length) failures.push({ width, group: group.id, clipped });
    }
  }

  await page.setViewportSize({ width: 1024, height: 1400 });
  const proposedNodeIssues = await page.evaluate(() => {
    const issues=[],c=document.createElement('canvas').getContext('2d');c.font='15px Arial';
    const d=window.francePartyPreview.data();
    for(const n of d.nodes){window.francePartyPreview.inspect(n.key,false);const h=document.querySelector('#fr-details h2')?.textContent;if(h!==n.title)issues.push(`proposed title mismatch ${n.key}`);if(c.measureText(n.title).width>147)issues.push(`title overflow ${n.key}`);if([...document.querySelectorAll('#fr-details .fr-effects li')].some(row=>!row.textContent.trim()))issues.push(`empty effect row ${n.key}`);}
    for(const row of d.nodes.filter(n=>window.francePartyPreview.pack.changed_keys[n.key])){window.francePartyPreview.inspect(row.key,false);const hs=[...document.querySelectorAll('#fr-details h4')].map(h=>h.textContent);if(!hs.includes('Current effects')||!hs.includes('Proposed effects'))issues.push(`missing before/after effects ${row.key}`);}
    return issues;
  });
  failures.push(...proposedNodeIssues);

  for (const n of proposal.nodes.filter(n => n.offer)) {
    const result = await page.evaluate(key => {
      const n=window.francePartyPreview.data().nodes.find(x=>x.key===key);window.francePartyPreview.inspect(key,false);const box=document.querySelector('#fr-details'),text=box.textContent;
      const rowCount=effects=>(effects||[]).reduce((total,e)=>total+(e.kind==='building'?2:1),0);
      const requirements=[...box.querySelectorAll('.fr-requirements')].map(x=>x.textContent).join(' ');
      const partnerLabel={SOV:'the Soviet Union',USA:'the United States',GER:'West Germany',ENG:'Britain',ITA:'Italy',ALG:'Algeria',SER:'Yugoslavia'}[n.offer.partner]||n.offer.partner_name;
      const buildingSides=[['France',n.offer.france], [partnerLabel,n.offer.recipient]].filter(([,side])=>(side.effects||[]).some(e=>e.kind==='building')).map(([label])=>label);
      const assetLines=[...box.querySelectorAll('.fr-requirements li')].filter(li=>li.textContent.includes('must own and fully control'));
      return {key,bothParties:text.includes(n.offer.france.title)&&text.includes(n.offer.recipient.title),acceptance:[...box.querySelectorAll('h3')].some(h=>h.textContent==='If they accept'),peaceAndSanctions:requirements.includes('Both countries must exist')&&requirements.includes('No native embargo')&&requirements.includes('No mirrored diplomatic, financial, economic, or military sanctions'),assetSidesPresent:buildingSides.every(label=>assetLines.some(li=>li.textContent.startsWith(label+' must own and fully control'))),assetRequirements:assetLines.map(li=>li.textContent),rows:box.querySelectorAll('.fr-effects li').length,minimum:rowCount(n.effects)+rowCount(n.offer.france.effects)+rowCount(n.offer.recipient.effects)};
    }, n.key);
    offerChecks.push(result);if(!result.bothParties||!result.acceptance||!result.peaceAndSanctions||!result.assetSidesPresent||result.rows<result.minimum)failures.push({offer:result});
  }

  for (const gov of proposal.groups.filter(g=>g.slot!==null&&!g.governing_group)) {
    await page.locator('#fr-government').selectOption(gov.id);
    const bad=await page.evaluate(govId=>{const d=window.francePartyPreview.data(),g=d.groups.find(x=>x.id===govId);return [...document.querySelectorAll('.fr-focus')].filter(b=>{const n=d.nodes.find(x=>x.key===b.dataset.key),owner=d.groups.find(x=>x.id===n.group);return b.classList.contains('is-locked')!==(owner.slot!==null&&owner.slot!==g.slot);}).map(b=>b.dataset.key);},gov.id);
    if(bad.length)failures.push({government:gov.id,nodes:bad});
  }

  await page.locator('#fr-government').selectOption('pcf');
  await page.locator('#fr-section').selectOption('pcf');
  await page.evaluate(()=>window.francePartyPreview.inspect('soviet_friendship',false));
  const proposedScreenshot=path.join(screenshots,'france-party-proposed-pcf.png');
  await page.locator('#france-party-deals-preview').screenshot({path:proposedScreenshot});screenshotsWritten.push(path.basename(proposedScreenshot));
  await page.locator('#fr-current').click();loaded=await state();
  if(loaded.mode!=='current'||loaded.focuses!==152||loaded.offers!==19||loaded.banner||loaded.brokenImages)failures.push({current_toggle:loaded});
  const currentTitles=await page.evaluate(()=>{const c=document.createElement('canvas').getContext('2d');c.font='15px Arial';return window.francePartyPreview.data().nodes.filter(n=>c.measureText(n.title).width>147).map(n=>({key:n.key,title:n.title,width:c.measureText(n.title).width}));});
  if(currentTitles.length)failures.push({current_title_overflows:currentTitles});
  await page.evaluate(()=>window.francePartyPreview.inspect('soviet_friendship',false));
  const currentScreenshot=path.join(screenshots,'france-party-current-pcf.png');await page.locator('#france-party-deals-preview').screenshot({path:currentScreenshot});screenshotsWritten.push(path.basename(currentScreenshot));
  await page.locator('#fr-proposed').click();
  await page.locator('#fr-section').selectOption('psu');
  await page.evaluate(()=>window.francePartyPreview.inspect('psu_cooperative_exchange',false));
  const psuScreenshot=path.join(screenshots,'france-party-proposed-psu.png');await page.locator('#france-party-deals-preview').screenshot({path:psuScreenshot});screenshotsWritten.push(path.basename(psuScreenshot));

  const report={
    project:'IMPERIA COLD WAR',kind:'Browser verification of current vs proposed focus-tree preview; proposal is not installed; no HOI4 engine test',
    baseline_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(here,'BASELINE.json'))).digest('hex'),
    proposal_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(here,'proposal.json'))).digest('hex'),
    changes_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(here,'CHANGES.json'))).digest('hex'),
    proposed_focus_count:156,current_focus_count:152,proposed_offer_count:35,current_offer_count:19,changed_focus_count:changes.changes.length,section_count:14,
    view_count:fitViews.length,widths:[320,736,1024],fit_views:fitViews,offer_checks:offerChecks,
    strict_fragment_limit_bytes:1000000,fragment_bytes:fs.statSync(path.join('C:/Users/Enes/.codex/visualizations/2026/10/28/01a183df-ceae-74b3-b1f4-d519f043ee74','france-party-deals.html')).size,
    native_title_width_limit_px:147,title_overflows:proposedTitleIssues.concat(currentTitles),
    government_views:proposal.groups.filter(g=>g.slot!==null&&!g.governing_group).length,connector_collisions:connectorIssues,screenshots:screenshotsWritten,failures,
  };
  fs.writeFileSync(path.join(here,'PREVIEW_QA.json'),JSON.stringify(report,null,2)+'\n');
  await browser.close();
  console.log(JSON.stringify({current_focus_count:report.current_focus_count,proposed_focus_count:report.proposed_focus_count,offers:offerChecks.length,fit_views:fitViews.length,title_overflows:report.title_overflows.length,failures}));
  if(failures.length)process.exit(1);
})().catch(error=>{console.error(error);process.exit(1);});
