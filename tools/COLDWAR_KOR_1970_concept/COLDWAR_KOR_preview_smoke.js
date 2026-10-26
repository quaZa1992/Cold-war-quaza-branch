// IMPERIA CW — Cold War: preview interaction smoke checks without a browser.
// A minimal DOM verifies event/data wiring only, never visual browser layout.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const out=path.resolve(__dirname,'../../docs/design/COLDWAR_KOR_1970');
const preview=process.argv[2];
if(!preview)throw Error('Provide the absolute inline fragment path');
const html=fs.readFileSync(preview,'utf8');
const data=html.match(/<script[^>]*id="coldwar-kor-data"[^>]*>([\s\S]*?)<\/script>/)[1];
const script=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
assert.equal(script.length,1);
fs.writeFileSync(path.join(out,'COLDWAR_KOR_preview_script.js'),'// IMPERIA CW — Cold War: extracted preview script.\n'+script[0][1]);
const D=JSON.parse(data),results=[];
for(const width of [320,736,1024]){
  const saved=[];
  class El{
    constructor(id=''){this.id=id;this.children=[];this.listeners={};this.dataset={};this.style={setProperty(){}};this.attributes={};this.classes=new Set();this.classList={toggle:(k,on)=>on?this.classes.add(k):this.classes.delete(k),add:k=>this.classes.add(k),remove:k=>this.classes.delete(k)};this.clientWidth=width;this.clientHeight=620;this.innerHTML='';this.textContent='';this.options=[];}
    setAttribute(k,v){this.attributes[k]=v;}
    append(e){this.children.push(e);if(e.tag==='option')this.options.push(e);}
    replaceChildren(){this.children=[];}
    querySelector(s){assert(s.startsWith('#'));assert(elements.has(s.slice(1)),'missing DOM query '+s);return elements.get(s.slice(1));}
    addEventListener(k,fn){this.listeners[k]=fn;}
    insertAdjacentHTML(_,s){this.innerHTML+=s;}
    fire(type,value){if(value!==undefined)this.value=value;assert(this.listeners[type],type+' not wired');this.listeners[type]({target:this});}
  }
  const elements=new Map([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>[m[1],new El(m[1])]));
  elements.get('coldwar-kor-data').textContent=data;
  const phaseMarkup=html.match(/<select id="kor-phase"[\s\S]*?<\/select>/)[0];
  elements.get('kor-phase').options=[...phaseMarkup.matchAll(/value="([^"]+)"/g)].map(m=>({value:m[1]}));
  const document={getElementById:id=>{assert(elements.has(id),'missing id '+id);return elements.get(id);},createElement:tag=>{const e=new El();e.tag=tag;return e;},createElementNS:(_,tag)=>new El()};
  const window={openai:{widgetState:null,setWidgetState:s=>{saved.push(s);return Promise.resolve();}},addEventListener(){}};
  const context={document,window,ResizeObserver:class{constructor(fn){this.fn=fn;}observe(){}},console};
  vm.runInNewContext(script[0][1],context,{timeout:5000});
  const buttons=elements.get('kor-world').children.filter(e=>e.dataset.focus);
  assert.equal(buttons.length,298);
  for(const b of buttons){b.fire('click');assert(elements.get('kor-inspector').innerHTML.includes(D.nodes.find(n=>n.id===b.dataset.focus).label));}
  for(const g of D.groups)elements.get('kor-branch').fire('change',g.id);
  elements.get('kor-government').fire('change','roh');
  for(const phase of elements.get('kor-phase').options)elements.get('kor-phase').fire('change',phase.value);
  for(const id of ['kor-overview','kor-native','kor-plus','kor-minus'])elements.get(id).fire('click');
  assert(!elements.get('kor-world').style.transform.includes('NaN'));
  assert(saved.length>298);
  assert(saved.every(s=>JSON.stringify(s).length<16384));
  results.push({width,focus_clicks:buttons.length,programmes:D.groups.length,phase_options:elements.get('kor-phase').options.length,status:'PASS'});
}
fs.writeFileSync(path.join(out,'COLDWAR_KOR_preview_smoke.json'),JSON.stringify({status:'PASS',scope:'Minimal DOM interaction/data wiring; no browser layout or HOI4 engine test',results},null,2)+'\n');
process.stdout.write(JSON.stringify(results)+'\n');
