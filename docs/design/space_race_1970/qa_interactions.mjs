// IMPERIA CW — Cold War: interaction-model checks without browser or network access.
import {readFile,writeFile} from 'node:fs/promises';
import vm from 'node:vm';
import {resolve} from 'node:path';

const directory=resolve('docs/design/space_race_1970');
const source=await readFile(resolve(directory,'space-race-map.template.html'),'utf8');
const script=source.match(/<script>([\s\S]*?)<\/script>/)[1];
const elements=[],events=new Map();
class Element{
  constructor(tag,attributes={}){this.tagName=tag.toUpperCase();this.attributes=attributes;this.dataset={};this.style={};this.listeners={};this.textContent='';this.innerHTML='';this.hidden=false;this.disabled='disabled' in attributes;this.value=attributes.value||'';this.classes=new Set((attributes.class||'').split(/\s+/));for(const[key,value]of Object.entries(attributes))if(key.startsWith('data-'))this.dataset[key.slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=value;this.classList={toggle:(key,enabled)=>enabled?this.classes.add(key):this.classes.delete(key)};}
  setAttribute(key,value){this.attributes[key]=value;}
  hasAttribute(key){return key in this.attributes;}
  addEventListener(type,handler){(this.listeners[type]??=[]).push(handler);}
  dispatchEvent(event){event.target=this;for(const listener of this.listeners[event.type]||[])listener(event);return true;}
  closest(selector){return selector==='button'&&this.tagName==='BUTTON'?this:null;}
  click(){if(this.disabled)return;for(const listener of events.get('click')||[])listener({target:this});}
}
const attrs=raw=>Object.fromEntries([...raw.matchAll(/([\w-]+)(?:="([^"]*)")?/g)].map(m=>[m[1],m[2]??'']));
for(const match of source.split('<script>')[0].matchAll(/<(div|section|button|input|select|span|strong|h2|p|ul|dd|img|path|label|small|b|main|footer|aside|nav|header)\b([^>]*)>/g))elements.push(new Element(match[1],attrs(match[2])));
function matches(element,selector){if(selector[0]==='#')return element.attributes.id===selector.slice(1);if(selector[0]==='.')return element.classes.has(selector.slice(1));const m=selector.match(/^\[([^=\]]+)(?:=([^\]]+))?\]$/);return m?element.hasAttribute(m[1])&&(m[2]===undefined||element.attributes[m[1]]===m[2]):element.tagName.toLowerCase()===selector;}
const root=elements.find(e=>e.attributes.id==='cw-space-map');
root.querySelectorAll=selector=>{const dynamic=elements.flatMap(e=>[...e.innerHTML.matchAll(/<(button|div|span|p|b|li)\b([^>]*)>/g)].map(m=>new Element(m[1],attrs(m[2]))));return [...elements,...dynamic].filter(e=>matches(e,selector));};
root.querySelector=selector=>root.querySelectorAll(selector)[0]||null;
root.addEventListener=(type,handler)=>events.set(type,[...(events.get(type)||[]),handler]);
const localMath=Object.create(Math);
const sandbox={document:{getElementById:id=>id==='cw-space-map'?root:null},window:{addEventListener(){}},Math:localMath,Date,console,globalThis:{}};
vm.runInNewContext(script,sandbox,{timeout:2000});
const api=root.spacePreview,$=s=>{const e=root.querySelector(s);if(!e)throw new Error('Missing element '+s);return e;},click=s=>$(s).click(),results=[];
function check(label,condition){results.push({label,pass:!!condition});if(!condition)throw new Error(label);}
api.reset();let a=api.stats('crewed');
check('Full success combines launch and conditional objective probabilities',Math.abs(a.full-.8742)<1e-9);
check('Initial crewed mission is ready',a.ready);
check('Heavy launcher remains gated by engineering',!api.stats('heavy').ready&&api.stats('heavy').development);
check('Outcome probabilities sum to one',Math.abs(a.full+a.partial+a.abort+a.loss-1)<1e-9);
click('[data-mission=lunar]');check('Mission selection updates detail heading',$('[data-mission-title]').textContent==='Robotic Lunar Sample Return');
const policy=$('#sp-policy');
for(let i=0;i<8;i++){policy.value='rush';policy.dispatchEvent({type:'change'});policy.value='standard';policy.dispatchEvent({type:'change'});}
check('Policy toggling cannot shorten preparation for free',api.stats('lunar').remaining===18);
policy.value='tests';policy.dispatchEvent({type:'change'});
check('Extended testing adds cost and preparation',Math.abs(api.stats('lunar').cost-3)<1e-9&&api.stats('lunar').remaining===108);
check('Extended testing improves launch reliability',Math.abs(api.stats('lunar').launch-.94)<1e-9);
api.reset();click('[data-upgrade=test]');
check('Infrastructure purchase charges reserve',Math.abs(api.getState().reserve-55.5)<1e-9);
click('[data-upgrade=test]');check('Duplicate infrastructure purchase blocked',Math.abs(api.getState().reserve-55.5)<1e-9);
check('Infrastructure improves forecast',Math.abs(api.stats('crewed').launch-.96)<1e-9);
click('[data-joint]');check('Cooperation contribution charged',Math.abs(api.getState().reserve-53.5)<1e-9);
click('[data-joint]');check('Duplicate cooperation blocked',Math.abs(api.getState().reserve-53.5)<1e-9);
click('[data-advance]');check('Quarter advances time and engineering progress',api.getState().days===90&&api.getState().progress.station>62);
check('Quarter charges development plus upkeep',Math.abs(api.getState().reserve-49.9)<1e-8);
api.reset();localMath.random=()=>0;click('[data-launch]');
check('Successful mission recorded',api.getState().completed.crewed.type==='full');
check('Mission cost and prestige applied',Math.abs(api.getState().reserve-57.6)<1e-9&&api.getState().prestige===25);
click('[data-launch]');check('Repeat mission prestige farming blocked',api.getState().log.length===1);
api.reset();let values=[0,.95];localMath.random=()=>values.shift()??0;click('[data-launch]');
check('Partial success branch reachable',api.getState().completed.crewed.type==='partial');
api.reset();values=[.999,.1];localMath.random=()=>values.shift()??0;click('[data-launch]');
check('Launch failure can include safe crew recovery',api.getState().completed.crewed.type==='loss'&&api.getState().completed.crewed.text.includes('safely'));
api.reset();$('#sp-budget').value='24';$('#sp-budget').dispatchEvent({type:'input'});
for(let i=0;i<7;i++)click('[data-advance]');
check('Sustained funding unlocks heavy test after development and preparation',api.stats('heavy').ready);
api.reset();
const report={method:'Isolated JavaScript execution with minimal DOM event harness; no browser layout verification',checks:results.length,passed:results.filter(x=>x.pass).length,results};
await writeFile(resolve(directory,'preview-qa.json'),JSON.stringify(report,null,2));
console.log(JSON.stringify({checks:report.checks,passed:report.passed}));
