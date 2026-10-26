// IMPERIA CW — Cold War: execute the expanded preview UI without browser or network access.
import {readFile,writeFile} from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {resolve} from 'node:path';

const directory=resolve('docs/design/space_race_1970');
const location='C:/Users/Enes/.codex/visualizations/2026/10/20/01a15b45-9d1a-70e0-bfe5-9e3ecc289124/space-race-map.html';
const source=await readFile(location,'utf8'),scripts=[...source.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
const attributes=raw=>Object.fromEntries([...raw.matchAll(/([\w-]+)(?:="([^"]*)")?/g)].map(m=>[m[1],m[2]??'']));
const elements=[],events=new Map(),globalEvents=new Map(),saved=[];
class Element{
  constructor(tag,attrs={}){this.tagName=tag.toUpperCase();this.attributes=attrs;this.dataset={};this.style={};this.listeners={};this.textContent='';this.innerHTML='';this.hidden='hidden'in attrs;this.disabled='disabled'in attrs;this.value=attrs.value||'';this.classes=new Set((attrs.class||'').split(/\s+/));for(const[key,value]of Object.entries(attrs))if(key.startsWith('data-'))this.dataset[key.slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=value;}
  setAttribute(key,value){this.attributes[key]=value;}
  getAttribute(key){return this.attributes[key]??null;}
  hasAttribute(key){return key in this.attributes;}
  toggleAttribute(key,enabled){if(enabled)this.attributes[key]='';else delete this.attributes[key];}
  addEventListener(type,listener){(this.listeners[type]??=[]).push(listener);}
  dispatchEvent(e){e.target=this;for(const listener of this.listeners[e.type]||[])listener(e);}
  closest(s){return s==='button'&&this.tagName==='BUTTON'?this:null;}
  click(){if(this.disabled)return;for(const listener of events.get('click')||[])listener({target:this});}
}
const parse=html=>[...html.matchAll(/<(div|section|button|input|select|span|strong|h2|p|ul|ol|dd|img|path|label|small|b|main|footer|aside|nav|header|summary|g)\b([^>]*)>/g)].map(m=>new Element(m[1],attributes(m[2])));
elements.push(...parse(source.split('<script>')[0]));
const root=elements.find(e=>e.attributes.id==='cw-space-map');
function matches(e,s){if(s.startsWith('#'))return e.attributes.id===s.slice(1);if(s.startsWith('.'))return e.classes.has(s.slice(1));const m=s.match(/^\[([^=\]]+)(?:=([^\]]+))?\]$/);return m?e.hasAttribute(m[1])&&(m[2]===undefined||e.attributes[m[1]]===m[2]):e.tagName.toLowerCase()===s;}
root.querySelectorAll=s=>[...elements,...elements.flatMap(e=>parse(e.innerHTML))].filter(e=>matches(e,s));
root.querySelector=s=>elements.find(e=>matches(e,s))||root.querySelectorAll(s)[0]||null;root.addEventListener=(type,handler)=>events.set(type,[...(events.get(type)||[]),handler]);
const localMath=Object.create(Math);localMath.random=()=>0;
const context=vm.createContext({document:{getElementById:id=>id==='cw-space-map'?root:null},window:{addEventListener:(n,fn)=>globalEvents.set(n,fn),openai:{widgetState:null,setWidgetState:value=>{saved.push(value);return Promise.resolve();}}},Date,Math:localMath,console});
for(const script of scripts)vm.runInContext(script,context,{timeout:5000});
const api=root.spacePreviewV2,$=s=>{const element=root.querySelector(s);assert(element,'Element exists: '+s);return element;},click=s=>$(s).click();
const row=id=>api.engine().state().programmes.find(p=>p.id===id),checks=[];
const showsImage=key=>$('[data-news-bulletin]').innerHTML.includes(context.SpaceRaceNewsMedia[key].src);
function check(name,condition){assert(condition,name);checks.push(name);}
check('Default profile opens the expanded Mars expedition',api.ui().profile==='SOV'&&api.engine().state().selectedId==='mars-crewed-landing');
check('Command-room layout opens its operations view',root.dataset.view==='map'&&root.dataset.newsStyle==='md');
check('Mars expedition retains the halved development calendar',$('[data-duration]').textContent==='6 years');
check('Mars return and partial outcomes are visible',$('[data-context]').innerHTML.includes('recovered on Earth')&&$('[data-context]').innerHTML.includes('Partial result'));
check('Expanded catalogue loaded',api.engine().state().programmes.length>=84);
check('No historical state saved merely on load',saved.length===0);
check('Menu shows three unclaimed places before campaign prestige is earned',$('[data-prestige-top]').innerHTML.match(/Unclaimed/g).length===3&&$('[data-prestige-status]').textContent==='No campaign leader yet');
api.engine().importWorldState({schema:1,standings:{USA:[140,true,null],FRA:[80,true,null],CHI:[9999,false,null]}});api.render();
check('Menu displays eligible player countries in prestige order',$('[data-prestige-top]').innerHTML.indexOf('United States')<$('[data-prestige-top]').innerHTML.indexOf('France')&&!$('[data-prestige-top]').innerHTML.includes('China'));
api.engine().importWorldState({schema:1,standings:{USA:[140,true,null],FRA:[140,true,null]}});api.render();check('Menu explains suspended leadership bonuses for a tied lead',$('[data-prestige-status]').textContent.includes('Joint leaders')&&$('[data-leader-benefits]').textContent.includes('suspended'));
api.engine().importWorldState({schema:1,standings:{USA:[0,true,null],FRA:[0,true,null]}});api.render();
check('French Moon illustration appears in the initial sample',showsImage('french-lunar-landing')&&$('[data-news-bulletin]').innerHTML.includes('NO CAMPAIGN EFFECT'));
const beforeExample=api.engine().state().prestige;
$('#sp-news-select').value='example-us-mars';$('#sp-news-select').dispatchEvent({type:'change'});check('US Mars sample uses its assigned artwork',showsImage('us-mars-landing'));
$('#sp-news-select').value='example-soviet-moon';$('#sp-news-select').dispatchEvent({type:'change'});check('Soviet lunar sample uses its assigned artwork',showsImage('soviet-lunar-landing'));
$('#sp-news-select').value='example-soviet-mars';$('#sp-news-select').dispatchEvent({type:'change'});check('Orange Soviet artwork is assigned to Mars',showsImage('soviet-mars-landing')&&$('[data-news-bulletin]').innerHTML.includes('Soviet Union Completes a Crewed Mars Expedition'));
$('#sp-news-select').value='example-french-moon';$('#sp-news-select').dispatchEvent({type:'change'});check('French lunar sample uses its assigned artwork',showsImage('french-lunar-landing'));
$('#sp-news-select').value='example-crew-loss';$('#sp-news-select').dispatchEvent({type:'change'});check('News contains the country and effects without image-provenance prose',$('[data-news-bulletin]').innerHTML.includes('Soviet Union: Crew Lost')&&$('[data-news-bulletin]').innerHTML.includes('Crew fatalities')&&!/archive|NASA|photograph|Illustrative station|<figcaption|<a /i.test($('[data-news-bulletin]').innerHTML));
click('[data-news-ack]');check('Acknowledging illustrative news cannot grant rewards or kill crew',api.engine().state().prestige===beforeExample&&api.engine().state().totalCrewFatalities===0);
check('Real successful US Mars events route to the US illustration',api.bulletinMediaKey({country:'USA',programmeId:'mars-crewed-landing',type:'full_success',imageKey:'mars'})==='us-mars-landing');
check('A failed US Mars mission cannot use the victory illustration',api.bulletinMediaKey({country:'USA',programmeId:'mars-crewed-landing',type:'catastrophic_failure',imageKey:'mission-control'})==='mission-control');
check('Soviet crewed Moon events route to the Soviet illustration',api.bulletinMediaKey({country:'SOV',programmeId:'n1-l3-recovery',type:'full_success',imageKey:'lunar'})==='soviet-lunar-landing');
check('Soviet crewed Mars events route to the orange Mars illustration',api.bulletinMediaKey({country:'SOV',programmeId:'mars-crewed-landing',type:'full_success',imageKey:'mars'})==='soviet-mars-landing');
const frenchMoon=context.SpaceRaceCatalogue.programmes.find(p=>(p.grants||[]).includes('lunar-landing'));
check('French crewed Moon events route to the French illustration',api.bulletinMediaKey({country:'FRA',programmeId:frenchMoon.id,type:'full_success',imageKey:'lunar'})==='french-lunar-landing');
click('[data-system=cislunar]');check('Cislunar map changes its title',$('[data-map-title]').textContent==='Cislunar Space');
check('Selected scope reveals matching orbit paths',!$('[data-orbits-cislunar]').hasAttribute('hidden'));
click('[data-system=deep]');check('Solar-system scope changes correctly',$('[data-map-title]').textContent==='Solar System');
click('[data-view=catalogue]');check('Catalogue tab visible',$('#sp2-catalogue').hidden===false);
click('[data-select=salyut]');check('Opening a programme from the full-width catalogue reveals its mission dossier',api.ui().view==='map'&&api.engine().state().selectedId==='salyut'&&root.dataset.view==='map');
for(const p of api.engine().state().programmes){api.selectProgramme(p.id);api.render();check('Programme renders: '+p.id,$('[data-programme-title]').textContent===p.name&&!$('[data-duration]').textContent.includes('NaN'));}
api.selectProgramme('lunar-outpost');api.render();check('Long-term outpost uses the ten-year campaign calendar',$('[data-duration]').textContent==='10 years');check('Future programme guard blocks authorisation',$('[data-primary]').disabled);
api.selectProgramme('salyut');api.render();check('Inherited station retains six months of qualification',$('[data-remaining]').textContent==='6 months');const initial=row('salyut').progress;click('[data-primary]');check('Development authorisation is functional',row('salyut').status==='active');click('[data-advance=3]');check('Quarter does not instantly finish engineering',row('salyut').progress>initial&&row('salyut').progress<100);
check('Authorising development triggers a country-named programme bulletin',api.ui().view==='news'&&api.engine().state().events.some(e=>e.type==='programme_authorised'&&e.countryName==='Soviet Union')&&$('[data-news-bulletin]').innerHTML.includes('Soviet Union: Authorises'));
click('[data-primary]');const paused=row('salyut').progress;click('[data-advance=12]');check('Paused engineering retains its exact progress',row('salyut').progress===paused);
click('[data-primary]');click('[data-advance=12]');check('Long-term completion produces flight hardware',row('salyut').completed&&!row('salyut').deployed);
check('Hardware qualification creates a separate programme report',api.engine().state().events.some(e=>e.type==='hardware_ready')&&$('[data-news-bulletin]').innerHTML.includes('PROGRAMME BULLETIN'));
api.render();click('[data-primary]');check('Flight launch is pending arrival',row('salyut').status==='inflight');check('In-flight UI blocks a second launch',$('[data-primary]').disabled&&$('[data-primary]').textContent==='Mission in Flight');click('[data-advance=3]');check('Successful arrival creates real operations',row('salyut').deployed&&row('salyut').status==='operational');
check('An accepted mission opens an actual news event',api.ui().view==='news'&&$('[data-news-bulletin]').innerHTML.includes('WORLD FIRST CONFIRMED')&&!$('[data-news-bulletin]').innerHTML.includes('NO CAMPAIGN EFFECT'));
check('Actual mission rewards reach the national totals',api.engine().state().researchPoints>0&&api.engine().state().politicalCapital>0);
check('Validated research appears in the assurance breakdown',$('[data-risk-factors]').innerHTML.includes('Validated research and analysis'));
check('Upkeep visible after commissioning',Number(api.engine().state().annualOperatingCostB)>0&&$('[data-total-upkeep]').textContent!=='$0.0b/yr');
const after=api.engine().state().programmes.find(p=>p.id==='salyut');check('Completed engineering policy cannot be rewritten',$('#sp2-policy').disabled);
click('[data-view=record]');check('Decisions appear in national record',$('[data-history-log]').innerHTML.includes('Salyut'));
for(const item of saved)check('Saved state remains below16KiB',JSON.stringify(item).length<16000);
$('#sp-profile').value='USA';$('#sp-profile').dispatchEvent({type:'change'});check('USA profile can be selected',api.engine().state().profileId==='USA');check('USA retains historical lunar capability',api.engine().state().capabilities.includes('lunar-landing'));
const unchangedChance=$('[data-full-chance]').textContent;$('#sp2-budget').value='0';$('#sp2-budget').dispatchEvent({type:'input'});check('Budget control changes actual engine budget',api.engine().state().annualBudgetB===0);check('Changing a budget ceiling cannot instantly buy reliability',$('[data-full-chance]').textContent===unchangedChance);
const catalogue=context.SpaceRaceCatalogue;
check('Historical and newcomer profiles are available',catalogue.profiles.length>=17);
for(const p of catalogue.profiles){$('#sp-profile').value=p.id;$('#sp-profile').dispatchEvent({type:'change'});check('Player profile renders: '+p.id,$('[data-profile-title]').textContent.includes('January 1970')&&$('#sp2-briefing').hidden===false);check('Player control retained: '+p.id,api.engine().state().playerControlled===true);}
$('#sp-profile').value='DDR';$('#sp-profile').dispatchEvent({type:'change'});check('DDR opens its inherited instrument campaign',api.engine().state().selectedId==='interkosmos-instruments');check('DDR briefing exposes national partner programmes',$('[data-national-programmes]').innerHTML.includes('MKF-6')&&$('[data-national-programmes]').innerHTML.includes('Research Cosmonaut'));check('DDR flight heritage does not imply an independent launcher',!api.engine().state().capabilities.includes('launch-basic'));
$('#sp-profile').value='JAP';$('#sp-profile').dispatchEvent({type:'change'});check('Japan does not inherit its future1970 orbital success',!api.engine().state().capabilities.includes('orbital-flight'));
$('#sp-profile').value='CHI';$('#sp-profile').dispatchEvent({type:'change'});check('China does not inherit its future1970 orbital success',!api.engine().state().capabilities.includes('orbital-flight'));
$('#sp-profile').value='CUSTOM';$('#sp-profile').dispatchEvent({type:'change'});
check('Newcomer starts without inherited space capabilities',api.engine().state().capabilities.length===0);
check('Newcomer opens its institutional entry programme',api.engine().state().selectedId==='space-commission'&&!$('[data-primary]').disabled);
$('#sp-custom-name').value='Iraq';$('#sp-custom-name').dispatchEvent({type:'change'});$('#sp-custom-tag').value='irq';$('#sp-custom-tag').dispatchEvent({type:'change'});
check('Any player country can be named',$('[data-profile-title]').textContent.includes('Iraq')&&api.ui().customTag==='IRQ');
click('[data-primary]');check('Newcomer can authorise an actual entry programme',row('space-commission').status==='active');check('Newcomer programme news uses the chosen country name',$('[data-news-bulletin]').innerHTML.includes('Iraq: Authorises')&&api.engine().state().events[0].countryName==='Iraq');
api.engine().setPlayerControlled(false);api.render();const suspended=api.engine().serialize();
check('AI takeover hides programme management',$('.sp-body').hidden&&$('[data-player-only-notice]').hidden===false);
check('AI takeover disables calendar controls',$('[data-advance=1]').disabled&&$('[data-advance=12]').disabled);
check('AI takeover also blocks reset and country renaming',$('[data-reset]').disabled&&$('#sp-custom-name').disabled&&$('#sp-custom-tag').disabled);
$('#sp-custom-name').value='Bypass';$('#sp-custom-name').dispatchEvent({type:'change'});check('Renaming cannot recreate an AI-controlled programme as human',!api.engine().state().playerControlled&&JSON.stringify(api.engine().serialize())===JSON.stringify(suspended));
check('AI cannot progress or spend',!api.engine().advance(12).ok&&JSON.stringify(api.engine().serialize())===JSON.stringify(suspended));
api.engine().setPlayerControlled(true);api.render();check('Player management can resume',$('.sp-body').hidden===false);
const report={method:'Isolated JavaScript + minimal DOM event harness; no browser layout verification',checks:checks.length,passed:checks.length,programmes:api.engine().state().programmes.length,savedSnapshots:saved.length,checksPassed:checks};
await writeFile(resolve(directory,'preview-expanded-qa.json'),JSON.stringify(report,null,2));console.log(JSON.stringify({checks:report.checks,passed:report.passed,programmes:report.programmes,savedSnapshots:saved.length}));
