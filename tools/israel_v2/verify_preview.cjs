// IMPERIA COLD WAR — Israel Version 2.2 focus-only proposed tree browser QA.
const { chromium } = require('C:/Users/Enes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const crypto = require('crypto');
let activeBrowser;

(async () => {
  const output=path.resolve('docs/israel_1970_v2');
  fs.mkdirSync(output,{recursive:true});
  const refreshOnly=process.argv.includes('--refresh');
  const input=path.resolve(process.argv.slice(2).find(argument=>!argument.startsWith('--')) || 'docs/israel_1970_v2/preview.html');
  const dataPath=path.resolve('tools/israel_v2/design.json');
  const fragmentPath=path.resolve('tools/israel_v2/fragment.html');
  const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
  const sourceHashes={data:hash(dataPath),fragment:hash(fragmentPath),preview:hash(input)};
  const data=JSON.parse(fs.readFileSync(dataPath,'utf8'));
  const positions=new Map(data.nodes.map(node=>[node.id,{x:node.xy[0]*data.layout.x_unit,y:node.xy[1]*data.layout.y_unit}]));
  const nodeCollisions=[];const connectorIntersections=[];const offRowExclusions=[];
  for(let i=0;i<data.nodes.length;i++)for(let j=i+1;j<data.nodes.length;j++){
    const a=positions.get(data.nodes[i].id),b=positions.get(data.nodes[j].id);
    if(Math.abs(a.x-b.x)<147 && Math.abs(a.y-b.y)<142)nodeCollisions.push([data.nodes[i].id,data.nodes[j].id]);
  }
  for(const node of data.nodes){
    const end=positions.get(node.id);
    for(const id of node.exclusive || [])if(node.id<id && positions.has(id) && positions.get(id).y!==end.y)offRowExclusions.push([node.id,id]);
  }
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  activeBrowser=browser;
  const page=await browser.newPage({viewport:{width:1024,height:1150}});
  const failures=[];const views=[];const clicked=[];const depthNavigation=[];const overviewGeometry=[];const navigationControls={};
  if(nodeCollisions.length)failures.push('Focus card collisions: '+JSON.stringify(nodeCollisions));
  if(offRowExclusions.length)failures.push('Exclusive choices on different rows: '+JSON.stringify(offRowExclusions));
  page.on('pageerror',error=>failures.push(error.message));
  await page.goto(pathToFileURL(input).href);
  const frame=page.frameLocator('iframe');
  await frame.locator('#isr-v2[data-ready="true"]').waitFor();
  const initialState=await frame.locator('#isr-v2').evaluate(root=>root.israelV2.getState());
  if(data.default_focus && initialState.picked!==data.default_focus)failures.push('Default focus does not match the proposed policy context');
  await frame.locator('#isr-v2').screenshot({path:path.join(output,'preview-default.png')});
  if(initialState.current==='mafdal')await frame.locator('#isr-v2').screenshot({path:path.join(output,'preview-mafdal-choice.png')});
  const geometry=await frame.locator('#isr-v2').evaluate(root=>({
    cards:[...root.querySelectorAll('.v2-focus')].map(node=>({id:node.dataset.node,x:parseFloat(node.style.left),y:parseFloat(node.style.top)})),
    edges:[...root.querySelectorAll('.v2-edge')].map(edge=>({from:edge.dataset.from,to:edge.dataset.to,points:JSON.parse(edge.dataset.points)})),
    clippedTitles:[...root.querySelectorAll('.v2-focus-name')].filter(label=>label.scrollHeight>label.clientHeight+1).map(label=>label.parentElement.dataset.node)}));
  for(const edge of geometry.edges)for(const other of geometry.cards){
    if(other.id===edge.from || other.id===edge.to)continue;
    const left=other.x+2,right=other.x+145,top=other.y+2,bottom=other.y+132;
    const segments=edge.points.slice(1).map((point,index)=>[...edge.points[index],...point]);
    if(segments.some(([ax,ay,bx,by])=>ax===bx?ax>left && ax<right && Math.max(ay,by)>top && Math.min(ay,by)<bottom:ay>top && ay<bottom && Math.max(ax,bx)>left && Math.min(ax,bx)<right))connectorIntersections.push({from:edge.from,to:edge.to,intersects:other.id});
  }
  if(connectorIntersections.length)failures.push('Connector/card intersections: '+JSON.stringify(connectorIntersections));
  if(geometry.clippedTitles.length)failures.push('Focus titles overflow: '+geometry.clippedTitles.join(', '));
  console.log(JSON.stringify({phase:'geometry',nodes:data.nodes.length,card_collisions:nodeCollisions.length,connector_card_intersections:connectorIntersections.length,title_overflow_ids:geometry.clippedTitles}));
  const expectedEdges=data.nodes.reduce((sum,node)=>sum+(node.pre || []).reduce((count,row)=>count+row.length,0),0);
  const settle=()=>page.waitForTimeout(45);
  if(!refreshOnly){
    const before=await frame.locator('#isr-v2').evaluate(root=>root.israelV2.getState());
    const box=await frame.locator('#isr-v2-view').boundingBox();
    await page.mouse.move(box.x+8,box.y+8);await page.mouse.down();
    await page.mouse.move(box.x+52,box.y+46,{steps:5});await page.mouse.up();
    const after=await frame.locator('#isr-v2').evaluate(root=>root.israelV2.getState());
    navigationControls.actual_pointer_pan=after.camera.x>before.camera.x+40 && after.camera.y>before.camera.y+34 && after.picked===before.picked;
    if(!navigationControls.actual_pointer_pan)failures.push('Native-style pointer pan did not move the map independently of focus selection');
    await page.waitForTimeout(220);await frame.locator('#isr-v2-fit').click();
    const baseZoom=await frame.locator('#isr-v2').evaluate(root=>root.israelV2.getState().camera.z);
    await frame.locator('#isr-v2-plus').click();
    const larger=await frame.locator('#isr-v2').evaluate(root=>root.israelV2.getState().camera.z);
    await frame.locator('#isr-v2-minus').click();
    const returned=await frame.locator('#isr-v2').evaluate(root=>root.israelV2.getState().camera.z);
    navigationControls.actual_zoom_buttons=larger>baseZoom && Math.abs(returned-baseZoom)<.001;
    if(!navigationControls.actual_zoom_buttons)failures.push('Zoom controls did not change and restore readable map scale');
  }

  if(!refreshOnly)for(const width of [320,736,1024]) {
    await page.setViewportSize({width,height:1150});
    for(const group of data.groups) {
      await frame.locator('#isr-v2-branch').selectOption(group.id);await settle();
      const state=await frame.locator('#isr-v2').evaluate(root=>{
        const box=root.getBoundingClientRect();
        return {overflow:root.scrollWidth>root.clientWidth+2,nodes:root.querySelectorAll('.v2-focus').length,
          edges:root.querySelectorAll('.v2-edge').length,
          controlsOutside:[...root.querySelectorAll('.v2-toolbar button,.v2-toolbar select')].some(element=>{const r=element.getBoundingClientRect();return r.left<box.left-2 || r.right>box.right+2;}),
          selected:root.querySelector('#isr-v2-inspector').dataset.selectedFocus,
          imageFailures:[...root.querySelectorAll('.v2-focus img')].filter(image=>!image.complete || !image.naturalWidth).length,
          hiddenNodes:[...root.querySelectorAll('.v2-focus')].filter(node=>getComputedStyle(node).display==='none').length};
      });
      views.push({width,group:group.id,...state});
      if(state.overflow || state.controlsOutside)failures.push(`Overflow at ${width}px / ${group.id}`);
      if(state.nodes!==data.nodes.length || state.edges!==expectedEdges || state.hiddenNodes)failures.push(`Incomplete tree at ${width}px / ${group.id}`);
      if(state.imageFailures)failures.push(`Missing native icons at ${width}px / ${group.id}`);
      if(!data.nodes.some(node=>node.id===state.selected && node.group===group.id))failures.push(`Wrong inspector programme ${group.id}`);
      const depth={width,group:group.id,downward_jumps:0};
      const beginning=await frame.locator('#isr-v2').evaluate(root=>root.israelV2.getState());
      while(await frame.locator('#isr-v2-next-row').isVisible()){
        const before=await frame.locator('#isr-v2').evaluate(root=>root.israelV2.getState());
        await frame.locator('#isr-v2-next-row').click();await settle();
        const after=await frame.locator('#isr-v2').evaluate(root=>root.israelV2.getState());
        depth.downward_jumps++;
        if(after.camera.y>=before.camera.y-1){failures.push(`Downward navigation did not advance ${width}/${group.id}`);break;}
        if(after.picked!==before.picked)failures.push(`Downward navigation changed the inspected focus ${width}/${group.id}`);
        if(depth.downward_jumps>data.nodes.length){failures.push(`Downward navigation failed to reach the end ${width}/${group.id}`);break;}
      }
      const lastNode=data.nodes.filter(node=>node.group===group.id).sort((a,b)=>b.xy[1]-a.xy[1])[0];
      depth.last_row_visible=await frame.locator('#isr-v2').evaluate((root,id)=>{
        const view=root.querySelector('#isr-v2-view').getBoundingClientRect(),footer=root.querySelector('.v2-map-footer').getBoundingClientRect();
        const last=root.querySelector(`.v2-focus[data-node="${id}"]`).getBoundingClientRect();
        return last.top>=view.top-1 && last.bottom<=footer.top+1;
      },lastNode.id);
      if(!depth.last_row_visible)failures.push(`Final branch row remains clipped after navigation ${width}/${group.id}`);
      if(depth.downward_jumps){
        if(!await frame.locator('#isr-v2-back-top').isVisible())failures.push(`Missing return to top ${width}/${group.id}`);
        else {await frame.locator('#isr-v2-back-top').click();await settle();}
        const returned=await frame.locator('#isr-v2').evaluate(root=>root.israelV2.getState());
        depth.returned_to_top=Math.abs(returned.camera.y-beginning.camera.y)<1;
        if(!depth.returned_to_top)failures.push(`Return to top did not restore the branch ${width}/${group.id}`);
      }
      depthNavigation.push(depth);
    }
    await frame.locator('#isr-v2-overview').click();await settle();
    if(await frame.locator('#isr-v2 .v2-overview-list [data-group]').count()!==data.groups.length)failures.push(`Incomplete overview index at ${width}`);
    if(await frame.locator('#isr-v2').evaluate(root=>root.scrollWidth>root.clientWidth+2))failures.push(`Overview overflow at ${width}`);
    const overview=await frame.locator('#isr-v2').evaluate(root=>{
      const labels=[...root.querySelectorAll('#isr-v2-overview-labels button')].map(element=>({id:element.dataset.group,box:element.getBoundingClientRect()})).filter(entry=>entry.box.width>0 && entry.box.height>0);
      const overlaps=[];
      for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++){
        const a=labels[i].box,b=labels[j].box;
        if(Math.min(a.right,b.right)-Math.max(a.left,b.left)>1 && Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>1)overlaps.push([labels[i].id,labels[j].id]);
      }
      const view=root.querySelector('#isr-v2-view').getBoundingClientRect();
      const clipped=labels.filter(entry=>entry.box.top<view.top-1 || entry.box.bottom>view.bottom+1).map(entry=>entry.id);
      return {overlaps,clipped};
    });
    overviewGeometry.push({width,...overview});
    if(overview.overlaps.length || overview.clipped.length)failures.push(`Overview labels overlap or clip at ${width}: ${JSON.stringify(overview)}`);
    await frame.locator('#isr-v2-starting').click();await settle();
    if(await frame.locator('.v2-starting-entry').count()!==(data.starting || []).length)failures.push(`Incomplete starting conditions at ${width}`);
  }

  await page.setViewportSize({width:1024,height:1150});
  if(!refreshOnly)for(const node of data.nodes) {
    await frame.locator('#isr-v2-branch').selectOption(node.group);
    await frame.locator('#isr-v2').evaluate((root,id)=>root.israelV2.centerFocus(id),node.id);
    await settle();
    const button=frame.locator(`.v2-focus[data-node="${node.id}"]`);
    await button.click();
    const inspect=frame.locator('#isr-v2-inspector');
    if(await inspect.getAttribute('data-selected-focus')!==node.id)failures.push(`Pointer selection failed ${node.id}`);
    if(await inspect.locator('.v2-effects>li').count()!==(node.effects || []).length)failures.push(`Missing effects ${node.id}`);
    if(await inspect.locator('h3').innerText()!==node.label)failures.push(`Incorrect focus title ${node.id}`);
    if(/unlock[^\n]*decisions?|decisions?[^\n]*unlock/i.test(await inspect.locator('.v2-effects').innerText()))failures.push(`Decision unlock remains in focus effects ${node.id}`);
    if(await inspect.locator('summary').filter({hasText:'Programme details'}).count())failures.push(`Implementation programme notes remain visible ${node.id}`);
    clicked.push(node.id);
  }

  const alignment=data.groups.find(group=>/alignment/i.test(group.id+' '+group.label)) || data.groups.find(group=>group.kind==='party') || data.groups[0];
  await frame.locator('#isr-v2-branch').selectOption(alignment.id);await settle();
  await frame.locator('#isr-v2').screenshot({path:path.join(output,'preview-alignment.png')});
  for(const id of ['alignment','gahal','mafdal']){
    if(!data.groups.some(group=>group.id===id))continue;
    await frame.locator('#isr-v2-branch').selectOption(id);await settle();
    let jumps=0;
    while(await frame.locator('#isr-v2-next-row').isVisible() && jumps++<data.nodes.length){await frame.locator('#isr-v2-next-row').click();await settle();}
    const finalNode=data.nodes.filter(node=>node.group===id).sort((a,b)=>b.xy[1]-a.xy[1])[0];
    await frame.locator(`.v2-focus[data-node="${finalNode.id}"]`).click();await settle();
    await frame.locator('#isr-v2').screenshot({path:path.join(output,`preview-${id}-deep.png`)});
  }
  const settlements=data.groups.find(group=>/settle|territor|frontier/i.test(group.id+' '+group.label));
  if(settlements){await frame.locator('#isr-v2-branch').selectOption(settlements.id);await settle();await frame.locator('#isr-v2').screenshot({path:path.join(output,'preview-settlements.png')});}
  await frame.locator('#isr-v2-overview').click();await settle();
  await frame.locator('#isr-v2').screenshot({path:path.join(output,'preview-overview.png')});
  const endingHashes={data:hash(dataPath),fragment:hash(fragmentPath),preview:hash(input)};
  const changedSources=Object.keys(sourceHashes).filter(key=>sourceHashes[key]!==endingHashes[key]);
  if(changedSources.length)failures.push('Sources changed during browser verification: '+changedSources.join(', '));
  const report={project:'IMPERIA COLD WAR',status:failures.length?'FAIL':'PASS',source:path.relative(process.cwd(),input).replaceAll('\\','/'),
    revision:data.revision,nodes:data.nodes.length,groups:data.groups.length,expected_edges:expectedEdges,
    source_hashes:sourceHashes,source_changes_during_verification:changedSources,initial_state:initialState,navigation_controls:navigationControls,depth_navigation:depthNavigation,overview_geometry:overviewGeometry,
    focus_only_effect_inspections:clicked.length,decision_unlocks_visible:failures.filter(failure=>failure.startsWith('Decision unlock remains')).length,
    implementation_notes_visible:failures.filter(failure=>failure.startsWith('Implementation programme notes')).length,
    responsive_views:views,actual_pointer_focus_inspections:clicked.length,inspected_focus_ids:clicked,
    geometry:{node_card_collisions:nodeCollisions,connector_card_intersections:connectorIntersections,off_row_exclusions:offRowExclusions,title_overflow_ids:geometry.clippedTitles,detoured_edges:geometry.edges.filter(edge=>edge.points.length>4).length,
      card_width:147,card_height:142,preview_grid:{x_unit:data.layout.x_unit,y_unit:data.layout.y_unit},native_reference:{file:'interface/nationalfocusview.gui',card_width:165,card_height:128,grid_x:96,grid_y:130,title_width:147,title_height:20},
      approximation:'Native artwork and MD-style titlebars. External Georgia typography, larger multiline labels and concept spacing; not exact HOI4 engine geometry.'},failures,
    evidence:'Headless Chrome browser, native-art design preview. No HOI4 engine rendering or gameplay execution.'};
  report.scope=refreshOnly?'Bounded display and geometry refresh. Full branch navigation and focus interaction coverage remains separately recorded in browser_validation.json.':'Full geometry, responsive, downward navigation and pointer inspection';
  fs.writeFileSync(path.join(output,refreshOnly?'display_refresh.json':'browser_validation.json'),JSON.stringify(report,null,2)+'\n');
  await browser.close();
  activeBrowser=null;
  console.log(JSON.stringify({status:report.status,nodes:report.nodes,groups:report.groups,responsive_views:views.length,actual_pointer_focus_inspections:clicked.length,failures},null,2));
  process.exitCode=failures.length?1:0;
})().catch(async error=>{console.error(error);if(activeBrowser)await activeBrowser.close();process.exitCode=1;});
