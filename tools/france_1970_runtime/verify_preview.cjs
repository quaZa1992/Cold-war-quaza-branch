// IMPERIA COLD WAR — Verify the rendered France 1970 installed-tree preview.
const { chromium } = require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');

const here = __dirname;
const preview = path.join(here, 'PREVIEW.html');
const screenshots = path.join(here, 'screenshots');
const expected = JSON.parse(fs.readFileSync(path.join(here, 'runtime_design.json'), 'utf8'));
fs.mkdirSync(screenshots, { recursive: true });

function rowCount(effects = []) { return effects.reduce((total, e) => total + (e.kind === 'building' ? 2 : 1), 0); }

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe' });
  const page = await browser.newPage({ viewport: { width: 1024, height: 1420 }, deviceScaleFactor: 1 });
  const failures = [], fitViews = [], screenshotsWritten = [];
  page.on('pageerror', error => failures.push(`pageerror: ${error.message}`));
  await page.goto(pathToFileURL(preview).href);
  await page.locator('.fr-focus').last().waitFor({ state: 'attached' });
  const loaded = await page.evaluate(() => ({
    focuses: window.franceRuntime.data.nodes.length,
    offers: window.franceRuntime.data.nodes.filter(n => n.offer).length,
    groups: window.franceRuntime.data.groups.length,
    shortcuts: document.querySelectorAll('#fr-shortcuts button').length,
    brokenImages: [...document.querySelectorAll('#france-runtime-preview img')].filter(i => !i.complete || !i.naturalWidth).length,
    missingFocusArt: window.franceRuntime.data.nodes.filter(n => !window.franceRuntime.data || !n.icon || !document.querySelector(`[data-key="${CSS.escape(n.key)}"] .fr-goal`)?.src).map(n => n.key),
  }));
  if (loaded.focuses !== 176 || loaded.offers !== 35 || loaded.groups !== 14 || loaded.brokenImages || loaded.missingFocusArt.length) failures.push({ initial_load: loaded });
  const addedKeys = expected.expansion_revision?.added_focus_keys || [];
  if (addedKeys.length !== 20 || addedKeys.some(key => !expected.nodes.some(n => n.key === key))) failures.push({ expansion_focus_inventory: addedKeys });

  for (const width of [320, 736, 1024]) {
    await page.setViewportSize({ width, height: 1420 });
    const outer = await page.locator('#france-runtime-preview').evaluate(root => ({ overflow: root.scrollWidth > root.clientWidth + 2, client: root.clientWidth, scroll: root.scrollWidth }));
    if (outer.overflow) failures.push({ width, root_overflow: outer });
    for (const group of expected.groups) {
      await page.locator('#fr-section').selectOption(group.id);
      const clipped = await page.locator('#fr-map').evaluate((map, groupId) => {
        const bounds = map.getBoundingClientRect();
        const nodes = window.franceRuntime.data.nodes.filter(n => n.group === groupId);
        return nodes.filter(n => {
          const box = map.querySelector(`[data-key="${CSS.escape(n.key)}"]`).getBoundingClientRect();
          return box.left < bounds.left - 1 || box.right > bounds.right + 1 || box.top < bounds.top - 1 || box.bottom > bounds.bottom + 1;
        }).map(n => n.key);
      }, group.id);
      fitViews.push({ width, group: group.id, clipped: clipped.length });
      if (clipped.length) failures.push({ width, group: group.id, clipped });
    }
  }

  await page.setViewportSize({ width: 1024, height: 1420 });
  const nodeChecks = await page.evaluate(() => {
    const issues = [];
    const c = document.createElement('canvas').getContext('2d');
    c.font = '15px Arial';
    for (const n of window.franceRuntime.data.nodes) {
      window.franceRuntime.inspect(n.key, false);
      const title = document.querySelector('#fr-details h2')?.textContent;
      const desc = document.querySelector('#fr-details .fr-description')?.textContent;
      if (title !== n.title) issues.push(`title mismatch ${n.key}`);
      if (desc !== n.description) issues.push(`description mismatch ${n.key}`);
      if (c.measureText(n.title).width > 147) issues.push(`title overflow ${n.key}: ${n.title}`);
      const card = document.querySelector(`[data-key="${CSS.escape(n.key)}"]`);
      if (Math.abs(parseFloat(card.style.left) - n.x * 96) > .01 || Math.abs(parseFloat(card.style.top) - n.y * 130) > .01) issues.push(`native coordinate mismatch ${n.key}`);
      if ([...document.querySelectorAll('#fr-details .fr-effects li')].some(row => !row.textContent.trim())) issues.push(`empty effect row ${n.key}`);
      if (n.effects.some(e => e.kind === 'faction_opinion') && ![...document.querySelectorAll('#fr-details .fr-effects li')].some(row => /Opinion: [+-]\d+/.test(row.textContent))) issues.push(`faction opinion effect missing ${n.key}`);
    }
    return issues;
  });
  failures.push(...nodeChecks);

  const geometryIssues = await page.evaluate(newKeys => {
    const D = window.franceRuntime.data, nodes = D.nodes, byKey = Object.fromEntries(nodes.map(n => [n.key, n]));
    const fresh = new Set(newKeys), issues = { card_overlaps: [], connector_card_hits: [], connector_crossings: [], connector_exclusion_hits: [], heading_card_hits: [], heading_overlaps: [] };
    for (let i = 0; i < nodes.length; i++) for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i], b = nodes[j];
      if (!(fresh.has(a.key) || fresh.has(b.key))) continue;
      if (a.x * 96 < b.x * 96 + 165 && a.x * 96 + 165 > b.x * 96 && a.y * 130 < b.y * 130 + 128 && a.y * 130 + 128 > b.y * 130) issues.card_overlaps.push([a.key, b.key]);
    }
    const edges = [];
    for (const child of nodes) for (const group of child.prerequisites || []) for (const key of group) {
      const parent = byKey[key]; if (!parent || parent.y >= child.y) continue;
      const x1=parent.x*96+82.5,y1=parent.y*130+128,x2=child.x*96+82.5,y2=child.y*130,mid=y2-1;
      const edge={parent:parent.key,child:child.key,isNew:fresh.has(child.key),segments:[['v',x1,y1,mid],['h',mid,x1,x2],['v',x2,mid,y2]]};edges.push(edge);
      if(edge.isNew) for(const card of nodes){if(card.key===parent.key||card.key===child.key)continue;const l=card.x*96,t=card.y*130,r=l+165,b=t+128;for(const [type,a,c,e] of edge.segments){const hit=type==='v'?l<a&&a<r&&Math.max(c,t)<Math.min(e,b):t<a&&a<b&&Math.max(Math.min(c,e),l)<Math.min(Math.max(c,e),r);if(hit){issues.connector_card_hits.push({edge:[parent.key,child.key],card:card.key});break;}}}
    }
    for(let i=0;i<edges.length;i++)for(let j=i+1;j<edges.length;j++){const a=edges[i],b=edges[j];if(!(a.isNew||b.isNew)||a.parent===b.parent||a.parent===b.child||a.child===b.parent||a.child===b.child)continue;for(const s of a.segments)for(const t of b.segments){if(s[0]===t[0])continue;const v=s[0]==='v'?s:t,h=s[0]==='h'?s:t,x=v[1],v0=Math.min(v[2],v[3]),v1=Math.max(v[2],v[3]),y=h[1],h0=Math.min(h[2],h[3]),h1=Math.max(h[2],h[3]);if(v0<y&&y<v1&&h0<x&&x<h1)issues.connector_crossings.push({first:[a.parent,a.child],second:[b.parent,b.child],point:[x,y]});}}
    const bars=[];for(const n of nodes)for(const key of n.exclusions||[]){const other=byKey[key];if(!other||n.key>=key||n.y!==other.y)continue;const left=n.x<other.x?n:other,right=n.x<other.x?other:n;bars.push({pair:[left.key,right.key],x0:left.x*96+166,x1:right.x*96-2,y:left.y*130+92,isOld:!fresh.has(left.key)&&!fresh.has(right.key)});}
    for(const edge of edges.filter(e=>e.isNew))for(const s of edge.segments)for(const bar of bars.filter(b=>b.isOld)){const hit=s[0]==='v'?bar.x0<s[1]&&s[1]<bar.x1&&Math.min(s[2],s[3])<bar.y&&bar.y<Math.max(s[2],s[3]):s[1]===bar.y&&Math.max(Math.min(s[2],s[3]),bar.x0)<Math.min(Math.max(s[2],s[3]),bar.x1);if(hit)issues.connector_exclusion_hits.push({edge:[edge.parent,edge.child],bar:bar.pair});}
    const world=document.querySelector('#fr-world');for(const g of D.groups){const h=world.querySelector('.fr-group[data-group="'+CSS.escape(g.id)+'"]');if(!h)continue;const a={l:h.offsetLeft,t:h.offsetTop,r:h.offsetLeft+h.offsetWidth,b:h.offsetTop+h.offsetHeight};for(const n of nodes.filter(n=>fresh.has(n.key))){const el=world.querySelector('[data-key="'+CSS.escape(n.key)+'"]'),c={l:el.offsetLeft,t:el.offsetTop,r:el.offsetLeft+165,b:el.offsetTop+128};if(a.l<c.r&&a.r>c.l&&a.t<c.b&&a.b>c.t)issues.heading_card_hits.push({group:g.id,focus:n.key});}}
    const hs=[...world.querySelectorAll('.fr-group')];for(let i=0;i<hs.length;i++)for(let j=i+1;j<hs.length;j++){const a=hs[i],b=hs[j];if(a.offsetLeft<b.offsetLeft+b.offsetWidth&&a.offsetLeft+a.offsetWidth>b.offsetLeft&&a.offsetTop<b.offsetTop+b.offsetHeight&&a.offsetTop+a.offsetHeight>b.offsetTop)issues.heading_overlaps.push([a.dataset.group,b.dataset.group]);}
    return issues;
  }, addedKeys);
  for (const [kind, issues] of Object.entries(geometryIssues)) if (issues.length) failures.push({ [kind]: issues });

  const standaloneSlotChecks = await page.evaluate(() => {
    const D=window.franceRuntime.data, checks=[];
    for(const n of D.nodes)for(const e of n.effects.filter(x=>x.kind==='state_slots')){
      window.franceRuntime.inspect(n.key,false);
      const row=[...document.querySelectorAll('#fr-details .fr-effects li[data-extra-slots]')].find(x=>x.dataset.extraSlots===String(e.state));
      checks.push({key:n.key,state:e.state,amount:e.amount,visible:!!row&&row.dataset.extraAmount===String(e.amount)&&row.textContent.includes('+'+e.amount+' shared building slot'),no_implied_building:!n.effects.some(x=>x.kind==='building'&&x.state===e.state)});
    }
    return checks;
  });
  failures.push(...standaloneSlotChecks.filter(x=>!x.visible||!x.no_implied_building).map(x=>({ standalone_slots:x })));

  const expansionRequirementChecks = await page.evaluate(keys => {
    const D=window.franceRuntime.data, checks=[];
    for(const key of keys){const n=D.nodes.find(x=>x.key===key);if(!n){checks.push({key,ok:false,issue:'focus missing'});continue;}
      window.franceRuntime.inspect(key,false);const text=document.querySelector('#fr-details .fr-requirements')?.textContent||'';
      const internalLeak=/is_1970|earned|gdp|receipt|transaction|reward_guard|COLDWAR_FRA2/i.test(text);
      const needsSlots=(n.effects||[]).some(e=>e.kind==='state_slots');
      const ownershipVisible=!needsSlots||(/must own and (fully )?control/i.test(text)&&/(state receiving the building slots|relevant state and province)/i.test(text));
      const boardRequirement=key!=='ps_conversion_boards'||/must own and fully control the state receiving the building slots/i.test(text);
      checks.push({key,needsSlots,ownershipVisible,boardRequirement,internalLeak,ok:!internalLeak&&ownershipVisible&&boardRequirement});}
    return checks;
  }, addedKeys);
  failures.push(...expansionRequirementChecks.filter(x=>!x.ok).map(x=>({ expansion_requirement:x })));

  const stagedSpiritChecks = await page.evaluate(() => {
    const D = window.franceRuntime.data;
    const spirits = Object.fromEntries([...(D.starting_spirits || []), ...(D.recovery_stages || [])].map(s => [s.id, s]));
    const pct = value => `${value >= 0 ? '+' : '-'}${Number(Math.abs(value * 100).toFixed(2)).toString()}%`;
    const keys = ['civic_settlement', 'parliament', 'technical_colleges', 'oil_resilience'];
    const results = [];
    for (const key of keys) {
      const n = D.nodes.find(x => x.key === key);
      if (!n) { results.push({ key, ok: false, issue: 'focus missing' }); continue; }
      window.franceRuntime.inspect(key, false);
      const rows = [...document.querySelectorAll('#fr-details .fr-effects li')];
      const heads = rows.filter(x => x.classList.contains('fr-spirit-head'));
      const details = rows.filter(x => x.classList.contains('fr-spirit-detail'));
      const transitions = n.effects.filter(e => e.kind === 'transition_spirit');
      const groups = n.effects.flatMap(e => e.kind === 'transition_spirit' ? [
        { action: 'Remove national spirit: ', spirit: spirits[e.from] },
        ...(e.to ? [{ action: 'Add national spirit: ', spirit: spirits[e.to] }] : []),
      ] : e.kind === 'remove_spirit' ? [{ action: 'Remove national spirit: ', spirit: spirits[e.spirit] }] : []);
      const issues = [];
      if (!transitions.length) issues.push('no spirit transition in source design');
      if (heads.length !== groups.length) issues.push(`spirit headings ${heads.length}, expected ${groups.length}`);
      groups.forEach((group, i) => {
        if (!group.spirit) { issues.push(`spirit metadata missing for ${group.action}`); return; }
        if (heads[i]?.textContent !== group.action + group.spirit.title) issues.push(`spirit heading mismatch at ${i}`);
        const modifiers = group.spirit.modifiers || [];
        const actual = details.slice(groups.slice(0, i).reduce((sum, g) => sum + (g.spirit?.modifiers?.length || 0), 0), groups.slice(0, i + 1).reduce((sum, g) => sum + (g.spirit?.modifiers?.length || 0), 0));
        if (actual.length !== modifiers.length) issues.push(`${group.spirit.title}: modifier count ${actual.length}, expected ${modifiers.length}`);
        modifiers.forEach((m, j) => { if (!actual[j]?.textContent.endsWith(pct(m.value))) issues.push(`${group.spirit.title}: modifier ${m.key} value missing or unsigned`); });
      });
      results.push({ key, ok: !issues.length, headings: heads.map(x => x.textContent), modifiers: details.map(x => x.textContent), issues });
    }
    const investmentFocuses = D.nodes.filter(n => n.group !== 'udr_nato' && n.effects.some(e => e.kind === 'building'));
    const investmentIssues = [];
    for (const n of investmentFocuses) {
      window.franceRuntime.inspect(n.key, false);
      const rows = document.querySelectorAll('#fr-details .fr-effects li');
      const slots = [...document.querySelectorAll('#fr-details .fr-effects li[data-asset-slot]')];
      const buildings = [...document.querySelectorAll('#fr-details .fr-effects li[data-asset-build]')];
      const expectedBuildings = [
        ...n.effects.filter(e => e.kind === 'building'),
        ...n.effects.filter(e => e.kind === 'unlock_decision').flatMap(e => D.decisions.find(d => d.id === e.id)?.effects.filter(x => x.kind === 'building') || []),
      ];
      if (slots.length !== expectedBuildings.length || buildings.length !== expectedBuildings.length) investmentIssues.push(n.key + ': building/slot rows mismatch');
      expectedBuildings.forEach((e, i) => {
        if (slots[i]?.dataset.assetSlot !== String(e.state) || buildings[i]?.dataset.assetBuild !== String(e.state)) investmentIssues.push(n.key + ': asset state missing');
        if (!slots[i]?.textContent.includes('+' + e.slots) || !buildings[i]?.textContent.includes('+' + e.amount)) investmentIssues.push(n.key + ': concrete slot/level amount missing');
      });
    }
    return { transitions: results, investment_focus_count: investmentFocuses.length, investment_issues: investmentIssues };
  });
  failures.push(...stagedSpiritChecks.transitions.filter(x => !x.ok).map(x => ({ spirit_transition: x })));
  failures.push(...stagedSpiritChecks.investment_issues);

  const cidProgrammeChecks = await page.evaluate(() => {
    const D=window.franceRuntime.data, keys=D.expansion_revision.cid_focus_keys||[], results=[];
    for(const key of keys){const n=D.nodes.find(x=>x.key===key);if(!n){results.push({key,ok:false,issue:'CID focus missing'});continue;}
      window.franceRuntime.inspect(key,false);const heading=[...document.querySelectorAll('#fr-details h3')].some(h=>h.textContent==='Modifies CID Programme');
      const expectsHeading=n.effects.some(e=>e.kind==='modifier');results.push({key,spirit_name:n.spirit_name,heading,expectsHeading,ok:n.spirit_name==='CID Programme'&&heading===expectsHeading});}
    return results;
  });
  failures.push(...cidProgrammeChecks.filter(x=>!x.ok).map(x=>({ cid_programme:x })));

  const offers = await page.evaluate(() => window.franceRuntime.data.nodes.filter(n => n.offer).map(n => {
    const rowCount = effects => effects.reduce((total, e) => total + (e.kind === 'building' ? 2 : 1), 0);
    window.franceRuntime.inspect(n.key, false);
    const details = document.querySelector('#fr-details');
    const text = details.textContent;
    const expectedRows = rowCount(n.effects) + rowCount(n.offer.france.effects) + rowCount(n.offer.recipient.effects) + n.effects.filter(e => e.kind === 'unlock_decision').reduce((sum, e) => {
      const d = window.franceRuntime.data.decisions.find(x => x.id === e.id); return sum + (d ? rowCount(d.effects) : 0);
    }, 0);
    const weekly = [...n.effects, ...n.offer.france.effects, ...n.offer.recipient.effects].filter(e => e.kind === 'weekly_gdp_expense');
    const weeklyRows = [...details.querySelectorAll('.fr-effects li')].filter(li => li.textContent.startsWith('Weekly Additional Expenses: '));
    const weeklyExpected = weekly.map(e => 'Weekly Additional Expenses: -' + Number(Math.abs(e.annual_gdp_percent / e.divisor).toFixed(5)).toString() + '% of current GDP');
    return {
      key: n.key,
      bothParties: [...details.querySelectorAll('.fr-term h3')].length === 2 && [...details.querySelectorAll('.fr-term h3')].some(h => h.textContent.startsWith('France: ')) && [...details.querySelectorAll('.fr-term h3')].some(h => h.textContent.startsWith(n.offer.partner_name + ': ')),
      acceptanceHeading: [...details.querySelectorAll('h3')].some(h => h.textContent === 'If they accept'),
      peaceAndSanctions: /peace/i.test(details.querySelector('.fr-requirements')?.textContent || '') && /sanction/i.test(details.querySelector('.fr-requirements')?.textContent || ''),
      assetCapacityRequirements: ![...n.offer.france.effects, ...n.offer.recipient.effects].some(e => e.kind === 'building') || /native level capacity/i.test(details.querySelector('.fr-requirements')?.textContent || ''),
      noWorkflowText: !/proposal and one-time transaction/i.test(details.querySelector('.fr-requirements')?.textContent || ''),
      noRepeatedAssetLocation: !/in ([A-Za-z][A-Za-z -]+) in \1\b/.test(details.querySelector('.fr-requirements')?.textContent || ''),
      effectRows: details.querySelectorAll('.fr-effects li').length,
      expectedRows,
      weekly_cost_rows: weeklyRows.length,
      weekly_costs_match: weeklyRows.length === weeklyExpected.length && weeklyExpected.every(text => weeklyRows.some(row => row.textContent === text)),
      weekly_formula_hidden: !/annual GDP \/|\/ 52/i.test(details.textContent),
    };
  }));
  failures.push(...offers.filter(o => !o.bothParties || !o.acceptanceHeading || !o.peaceAndSanctions || !o.assetCapacityRequirements || !o.noWorkflowText || !o.noRepeatedAssetLocation || o.effectRows !== o.expectedRows || !o.weekly_costs_match || !o.weekly_formula_hidden).map(o => ({ offer: o })));

  const governmentIssues = [];
  for (const gov of expected.groups.filter(g => g.slot !== null && !g.governing_group)) {
    await page.locator('#fr-government').selectOption(gov.id);
    const bad = await page.evaluate(govId => {
      const g = window.franceRuntime.data.groups.find(x => x.id === govId);
      return [...document.querySelectorAll('.fr-focus')].filter(b => {
        const n = window.franceRuntime.data.nodes.find(x => x.key === b.dataset.key);
        const owner = window.franceRuntime.data.groups.find(x => x.id === n.group);
        return b.classList.contains('is-locked') !== (owner.slot !== null && owner.slot !== g.slot);
      }).map(b => b.dataset.key);
    }, gov.id);
    if (bad.length) governmentIssues.push({ government: gov.id, nodes: bad });
  }
  failures.push(...governmentIssues);

  await page.locator('#fr-government').selectOption('udr');
  await page.locator('#fr-section').selectOption('udr');
  await page.evaluate(() => window.franceRuntime.inspect('progress', false));
  await page.locator('#fr-native').click();
  const nativeScale = await page.evaluate(() => window.franceRuntime.getView().z);
  if (nativeScale !== 1) failures.push(`native scale is ${nativeScale}`);
  const beforePan = await page.evaluate(() => window.franceRuntime.getView());
  const box = await page.locator('#fr-map').boundingBox();
  await page.mouse.move(box.x + 20, box.y + 20); await page.mouse.down();
  await page.mouse.move(box.x + 75, box.y + 60, { steps: 4 }); await page.mouse.up();
  const afterPan = await page.evaluate(() => window.franceRuntime.getView());
  if (Math.abs(afterPan.tx - beforePan.tx) < 20) failures.push('pan did not move map');
  await page.locator('#fr-more').click();
  if ((await page.evaluate(() => window.franceRuntime.getView().z)) <= afterPan.z) failures.push('zoom-in did not increase zoom');

  for (const [section, key, file] of [
    ['udr_nato', 'nato_nuclear_consult', 'france-nato.png'],
    ['udr', 'participation', 'france-gaullist.png'],
    ['institutions', 'parliament', 'france-spirit-transition.png'],
    ['radical', 'municipal_france', 'france-domestic-investment.png'],
    ['economy', 'nuclear_scale', 'france-economy.png'],
    ['diplomacy', 'airbus', 'france-airbus.png'],
    ['ri', 'ri_sme_capital', 'france-expansion-ri.png'],
    ['ps', 'ps_conversion_boards', 'france-expansion-socialists.png'],
    ['psu', 'psu_land_banks', 'france-expansion-psu.png'],
    ['pcf', 'pcf_supply_contracts', 'france-expansion-pcf.png'],
    ['right', 'cid_rural_networks', 'france-expansion-cid.png'],
    ['ecology', 'ecology_municipal_heat', 'france-expansion-ecology.png'],
    ['overview', 'progress', 'france-overview.png'],
  ]) {
    await page.locator('#fr-section').selectOption(section);
    await page.evaluate(k => window.franceRuntime.inspect(k, false), key);
    const target = path.join(screenshots, file);
    await page.locator('#france-runtime-preview').screenshot({ path: target });
    screenshotsWritten.push(file);
  }
  const report = {
    project: 'IMPERIA COLD WAR',
    kind: 'Local browser QA of the emitted native-tree preview; no HOI4 engine test',
    emitted_runtime_sha256: require('crypto').createHash('sha256').update(fs.readFileSync(path.join(here, 'runtime_design.json'))).digest('hex'),
    focus_count: loaded.focuses,
    offer_count: loaded.offers,
    section_count: loaded.groups,
    native_shortcuts: loaded.shortcuts,
    widths: [320, 736, 1024],
    fit_views: fitViews,
    offer_checks: offers,
    expansion_focus_keys: addedKeys,
    expansion_focus_count: addedKeys.length,
    geometry_issues: geometryIssues,
    standalone_slot_checks: standaloneSlotChecks,
    expansion_requirement_checks: expansionRequirementChecks,
    internal_requirement_leaks: expansionRequirementChecks.filter(x=>x.internalLeak).map(x=>x.key),
    weekly_expense_rows: offers.reduce((sum,o)=>sum+o.weekly_cost_rows,0),
    cid_programme_checks: cidProgrammeChecks,
    spirit_transition_checks: stagedSpiritChecks.transitions,
    investment_focus_count: stagedSpiritChecks.investment_focus_count,
    investment_issues: stagedSpiritChecks.investment_issues,
    title_width_limit_px: 147,
    native_card_px: [165, 128],
    native_grid_stride_px: [96, 130],
    title_overflows: nodeChecks.filter(x => x.startsWith('title overflow')),
    pan_zoom: true,
    broken_image_count: loaded.brokenImages,
    screenshots: screenshotsWritten,
    failures,
  };
  fs.writeFileSync(path.join(here, 'PREVIEW_QA.json'), JSON.stringify(report, null, 2) + '\n');
  await browser.close();
  console.log(JSON.stringify({ focuses: report.focus_count, offers: report.offer_count, views: fitViews.length, titleOverflows: report.title_overflows.length, failures }));
  if (failures.length) process.exit(1);
})().catch(error => { console.error(error); process.exit(1); });
