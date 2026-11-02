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
const additions = JSON.parse(fs.readFileSync(path.join(here, 'ADDITIONS.json'), 'utf8'));
const currentCount = baseline.nodes.length, proposedCount = proposal.nodes.length;
const addedKeys = new Set(additions.added_focuses.map(n => n.key));
const focusChanges = additions.focus_changes || [];
const currentOffers = baseline.nodes.filter(n => n.offer).length, proposedOffers = proposal.nodes.filter(n => n.offer).length;
fs.mkdirSync(screenshots, { recursive: true });
const rows = effects => (effects || []).reduce((total, e) => total + (e.kind === 'building' ? 2 : 1), 0);

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage({ viewport: { width: 1024, height: 1400 }, deviceScaleFactor: 1 });
  const failures = [], fitViews = [], offerChecks = [], screenshotsWritten = [];
  page.on('pageerror', error => failures.push(`pageerror: ${error.message}`));
  await page.goto(pathToFileURL(preview).href);
  await page.locator('[data-key="ri_sme_capital"]').waitFor();

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
  if (loaded.mode !== 'proposed' || loaded.focuses !== proposedCount || loaded.offers !== proposedOffers || loaded.groups !== 14 || !loaded.banner || loaded.brokenImages) failures.push({ initial_load: loaded });
  if (await page.locator('#fr-section').inputValue() !== 'ri') failures.push('initial section is not RI');

  const proposedTitleIssues = await page.evaluate(() => {
    const c = document.createElement('canvas').getContext('2d'); c.font = '15px Arial';
    return window.francePartyPreview.data().nodes.filter(n => c.measureText(n.title).width > 147).map(n => ({ key:n.key,title:n.title,width:c.measureText(n.title).width }));
  });
  if (proposedTitleIssues.length) failures.push({ proposed_title_overflows: proposedTitleIssues });
  await page.locator('#fr-section').selectOption('overview');
  const geometryIssues = await page.evaluate(() => {
    const d=window.francePartyPreview.data(),added=new Set(window.francePartyPreview.pack.proposed.nodes.map(n=>n.key)),nodes=d.nodes,byKey=Object.fromEntries(nodes.map(n=>[n.key,n])),issues={card_overlaps:[],connector_card_hits:[],connector_crossings:[],connector_exclusion_hits:[],exclusion_card_hits:[],heading_card_hits:[],heading_overlaps:[]};
    for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){const a=nodes[i],b=nodes[j];if(a.y===b.y&&Math.abs(a.x-b.x)*96<165&&(added.has(a.key)||added.has(b.key)))issues.card_overlaps.push([a.key,b.key]);}
    const edges=[];
    for(const child of nodes)for(const group of child.prerequisites||[])for(const key of group){const parent=byKey[key];if(!parent||parent.y>=child.y)continue;const x1=parent.x*96+82.5,y1=parent.y*130+128,x2=child.x*96+82.5,y2=child.y*130,mid=y2-1,edge={parent:parent.key,child:child.key,isNew:added.has(child.key),segments:[['v',x1,y1,mid],['h',mid,x1,x2],['v',x2,mid,y2]]};edges.push(edge);
      if(edge.isNew)for(const card of nodes){if(card.key===parent.key||card.key===child.key)continue;const l=card.x*96,t=card.y*130,r=l+165,b=t+128;for(const [type,a,c,e] of edge.segments){const hit=type==='v'?l<a&&a<r&&Math.max(c,t)<Math.min(e,b):t< a&&a<b&&Math.max(Math.min(c,e),l)<Math.min(Math.max(c,e),r);if(hit){issues.connector_card_hits.push({parent:parent.key,child:child.key,blocked_by:card.key});break;}}}
    }
    for(let i=0;i<edges.length;i++)for(let j=i+1;j<edges.length;j++){const a=edges[i],b=edges[j];if(!(a.isNew||b.isNew)||a.parent===b.parent||a.parent===b.child||a.child===b.parent||a.child===b.child)continue;for(const s of a.segments)for(const t of b.segments){if(s[0]===t[0])continue;const v=s[0]==='v'?s:t,h=s[0]==='h'?s:t;const x=v[1],v0=Math.min(v[2],v[3]),v1=Math.max(v[2],v[3]),y=h[1],h0=Math.min(h[2],h[3]),h1=Math.max(h[2],h[3]);if(v0<y&&y<v1&&h0<x&&x<h1)issues.connector_crossings.push({first:[a.parent,a.child],second:[b.parent,b.child],point:[x,y]});}}
    const bars=[];for(const n of nodes)for(const key of n.exclusions||[]){const other=byKey[key];if(!other||n.key>=key||n.y!==other.y)continue;const left=n.x<other.x?n:other,right=n.x<other.x?other:n;const middle=nodes.some(m=>m.y===n.y&&m.x>left.x&&m.x<right.x&&(n.exclusions||[]).includes(m.key)&&(other.exclusions||[]).includes(m.key));if(!middle)bars.push({pair:[left.key,right.key],x0:left.x*96+166,x1:right.x*96-2,y:left.y*130+92,isOld:!added.has(left.key)&&!added.has(right.key)});}
    for(const edge of edges.filter(e=>e.isNew))for(const s of edge.segments)for(const bar of bars.filter(b=>b.isOld)){const hit=s[0]==='v'?bar.x0<s[1]&&s[1]<bar.x1&&Math.min(s[2],s[3])<bar.y&&bar.y<Math.max(s[2],s[3]):s[1]===bar.y&&Math.max(Math.min(s[2],s[3]),bar.x0)<Math.min(Math.max(s[2],s[3]),bar.x1);if(hit)issues.connector_exclusion_hits.push({edge:[edge.parent,edge.child],bar:bar.pair,point:s[0]==='v'?[s[1],bar.y]:[Math.max(Math.min(s[2],s[3]),bar.x0),s[1]]});}
    for(const child of nodes.filter(n=>added.has(n.key)))for(const key of child.exclusions||[]){const other=byKey[key];if(!other||other.y!==child.y)continue;const left=child.x<other.x?child:other,right=child.x<other.x?other:child;const x0=left.x*96+166,x1=right.x*96-2,y=left.y*130+92;for(const card of nodes){if(card.key===left.key||card.key===right.key||card.y!==left.y)continue;const l=card.x*96,r=l+165;if(Math.max(x0,l)<Math.min(x1,r))issues.exclusion_card_hits.push({pair:[left.key,right.key],blocked_by:card.key});}}
    const world=document.querySelector('#fr-world');for(const g of d.groups){const h=world.querySelector(`.fr-group[data-group="${CSS.escape(g.id)}"]`);if(!h)continue;const a={l:h.offsetLeft,t:h.offsetTop,r:h.offsetLeft+h.offsetWidth,b:h.offsetTop+h.offsetHeight};for(const n of nodes){const el=world.querySelector(`[data-key="${CSS.escape(n.key)}"]`);if(!el)continue;const c={l:el.offsetLeft,t:el.offsetTop,r:el.offsetLeft+165,b:el.offsetTop+128};if(a.l<c.r&&a.r>c.l&&a.t<c.b&&a.b>c.t)issues.heading_card_hits.push({group:g.id,focus:n.key});}}
    const hs=[...world.querySelectorAll('.fr-group')];for(let i=0;i<hs.length;i++)for(let j=i+1;j<hs.length;j++){const a=hs[i],b=hs[j];if(a.offsetLeft<b.offsetLeft+b.offsetWidth&&a.offsetLeft+a.offsetWidth>b.offsetLeft&&a.offsetTop<b.offsetTop+b.offsetHeight&&a.offsetTop+a.offsetHeight>b.offsetTop)issues.heading_overlaps.push([a.dataset.group,b.dataset.group]);}
    return issues;
  });
  for(const [kind,issues] of Object.entries(geometryIssues))if(issues.length)failures.push({[kind]:issues});

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
    const issues=[],c=document.createElement('canvas').getContext('2d'),countRows=effects=>(effects||[]).reduce((total,e)=>total+(e.kind==='building'?2:1),0);c.font='15px Arial';
    const d=window.francePartyPreview.data();
    for(const n of d.nodes){window.francePartyPreview.inspect(n.key,false);const h=document.querySelector('#fr-details h2')?.textContent;if(h!==n.title)issues.push(`proposed title mismatch ${n.key}`);if(c.measureText(n.title).width>147)issues.push(`title overflow ${n.key}`);if([...document.querySelectorAll('#fr-details .fr-effects li')].some(row=>!row.textContent.trim()))issues.push(`empty effect row ${n.key}`);for(const req of n.asset_requirements||[])if(!document.querySelector('#fr-details .fr-requirements')?.textContent.includes(req))issues.push(`asset requirement missing ${n.key}: ${req}`);if(window.francePartyPreview.pack.changed_keys[n.key]?.type==='new'){const decisionEffects=(n.effects||[]).filter(e=>e.kind==='unlock_decision').flatMap(e=>d.decisions.find(x=>x.id===e.id)?.effects||[]);const expectedRows=countRows(n.effects)+countRows(decisionEffects),actualRows=document.querySelectorAll('#fr-details .fr-effects li').length;if(actualRows!==expectedRows)issues.push(`effect rows ${actualRows}, expected ${expectedRows} ${n.key}`);for(const e of (n.effects||[]).filter(e=>e.kind==='state_slots'))if(![...document.querySelectorAll('#fr-details .fr-effects li')].some(x=>x.textContent.includes('+'+e.amount+' shared building slot')&&!x.dataset.assetBuild))issues.push(`standalone state slots missing ${n.key}`);}}
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
  await page.locator('#fr-section').selectOption('overview');
  const overviewScreenshot=path.join(screenshots,'france-party-proposed-overview.png');await page.locator('#france-party-deals-preview').screenshot({path:overviewScreenshot});screenshotsWritten.push(path.basename(overviewScreenshot));
  await page.locator('#fr-section').selectOption('psu');
  await page.evaluate(()=>window.francePartyPreview.inspect('psu_land_banks',false));
  const psuLandBankScreenshot=path.join(screenshots,'france-party-proposed-psu-land-bank.png');await page.locator('#france-party-deals-preview').screenshot({path:psuLandBankScreenshot});screenshotsWritten.push(path.basename(psuLandBankScreenshot));
  await page.locator('#fr-section').selectOption('right');
  await page.evaluate(()=>window.francePartyPreview.inspect('cid_rural_networks',false));
  const rightScreenshot=path.join(screenshots,'france-party-proposed-right.png');await page.locator('#france-party-deals-preview').screenshot({path:rightScreenshot});screenshotsWritten.push(path.basename(rightScreenshot));
  await page.locator('#fr-current').click();loaded=await state();
  if(loaded.mode!=='current'||loaded.focuses!==currentCount||loaded.offers!==currentOffers||loaded.banner||loaded.brokenImages)failures.push({current_toggle:loaded});
  const currentTitles=await page.evaluate(()=>{const c=document.createElement('canvas').getContext('2d');c.font='15px Arial';return window.francePartyPreview.data().nodes.filter(n=>c.measureText(n.title).width>147).map(n=>({key:n.key,title:n.title,width:c.measureText(n.title).width}));});
  if(currentTitles.length)failures.push({current_title_overflows:currentTitles});
  await page.evaluate(()=>window.francePartyPreview.inspect('soviet_friendship',false));
  const currentScreenshot=path.join(screenshots,'france-party-current-pcf.png');await page.locator('#france-party-deals-preview').screenshot({path:currentScreenshot});screenshotsWritten.push(path.basename(currentScreenshot));
  await page.locator('#fr-section').selectOption('right');
  await page.evaluate(()=>window.francePartyPreview.inspect('cid_cooperatives',false));
  const currentCidScreenshot=path.join(screenshots,'france-party-current-cid.png');await page.locator('#france-party-deals-preview').screenshot({path:currentCidScreenshot});screenshotsWritten.push(path.basename(currentCidScreenshot));
  await page.locator('#fr-section').selectOption('ps');
  const decisionComparison=await page.evaluate(()=>{
    window.francePartyPreview.inspect('public_banks',false);
    const req=()=>[...document.querySelectorAll('#fr-details .fr-requirements li')].map(x=>x.textContent);
    const effectRows=()=>[...document.querySelectorAll('#fr-details .fr-effects li')].map(x=>x.textContent);
    const current=req();
    const currentEffects=effectRows();
    document.querySelector('#fr-proposed').click();window.francePartyPreview.inspect('public_banks',false);const proposed=req();
    const proposedEffects=effectRows();
    return {current:current.filter(x=>x.includes('Regional Conversion Fund')),proposed:proposed.filter(x=>x.includes('Regional Conversion Fund')),sameEffects:JSON.stringify(currentEffects)===JSON.stringify(proposedEffects),effects:proposedEffects};
  });
  if(!decisionComparison.current.some(x=>x.includes('Public Bank Credit completed'))||!decisionComparison.proposed.some(x=>x.includes('Public Bank Credit or Conversion Boards completed'))||!decisionComparison.sameEffects)failures.push({decision_requirement_comparison:decisionComparison});
  await page.evaluate(()=>window.francePartyPreview.inspect('ps_conversion_boards',false));
  const psScreenshot=path.join(screenshots,'france-party-proposed-conversion-boards.png');await page.locator('#france-party-deals-preview').screenshot({path:psScreenshot});screenshotsWritten.push(path.basename(psScreenshot));
  await page.locator('#fr-section').selectOption('psu');
  await page.evaluate(()=>window.francePartyPreview.inspect('psu_cooperative_markets',false));
  const psuScreenshot=path.join(screenshots,'france-party-proposed-psu.png');await page.locator('#france-party-deals-preview').screenshot({path:psuScreenshot});screenshotsWritten.push(path.basename(psuScreenshot));

  const report={
    project:'IMPERIA COLD WAR',kind:'Browser verification of current vs proposed focus-tree preview; proposal is not installed; no HOI4 engine test',
    baseline_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(here,'BASELINE.json'))).digest('hex'),
    proposal_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(here,'proposal.json'))).digest('hex'),
    additions_sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(here,'ADDITIONS.json'))).digest('hex'),
    proposed_focus_count:proposedCount,current_focus_count:currentCount,proposed_offer_count:proposedOffers,current_offer_count:currentOffers,new_focus_count:addedKeys.size,revised_focus_count:focusChanges.length,changed_focus_count:addedKeys.size+focusChanges.length,section_count:14,
    view_count:fitViews.length,widths:[320,736,1024],fit_views:fitViews,offer_checks:offerChecks,
    strict_fragment_limit_bytes:1000000,fragment_bytes:fs.statSync(path.join('C:/Users/Enes/.codex/visualizations/2026/10/28/01a183df-ceae-74b3-b1f4-d519f043ee74','france-party-expansion.html')).size,
    native_title_width_limit_px:147,title_overflows:proposedTitleIssues.concat(currentTitles),
    government_views:proposal.groups.filter(g=>g.slot!==null&&!g.governing_group).length,geometry_issues:geometryIssues,decision_requirement_comparison:decisionComparison,screenshots:screenshotsWritten,failures,
  };
  fs.writeFileSync(path.join(here,'PREVIEW_QA.json'),JSON.stringify(report,null,2)+'\n');
  await browser.close();
  console.log(JSON.stringify({current_focus_count:report.current_focus_count,proposed_focus_count:report.proposed_focus_count,offers:offerChecks.length,fit_views:fitViews.length,title_overflows:report.title_overflows.length,failures}));
  if(failures.length)process.exit(1);
})().catch(error=>{console.error(error);process.exit(1);});
