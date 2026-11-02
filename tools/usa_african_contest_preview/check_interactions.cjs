// IMPERIA COLD WAR — Execute the real preview script in a bounded DOM fixture
// This is source-level interaction evidence, not browser, CSS layout or HOI4 execution.
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const root=path.resolve(__dirname,'../..');
const source=fs.readFileSync(path.join(root,'docs/design/usa_african_contest_20261030/preview.html'),'utf8');
const data=JSON.parse(source.match(/<script type="application\/json" id="af-data">([\s\S]*?)<\/script>/)[1]);
const script=[...source.matchAll(/<script>([\s\S]*?)<\/script>/g)][0][1];
const byId=Object.fromEntries(data.nodes.map(n=>[n.id,n]));
class Element {
  constructor(tag='div'){this.tagName=tag;this.children=[];this.attributes={};this.dataset={};this.style={};this.hidden=false;this.events={};this._text='';this.clientWidth=694;this.className='';this.classList={toggle:(name,on)=>{const set=new Set(this.className.split(' ').filter(Boolean));if(on)set.add(name);else set.delete(name);this.className=[...set].join(' ');}};}
  set textContent(value){this._text=String(value);this.children=[];}
  get textContent(){return this._text+this.children.map(c=>c.textContent).join('\n');}
  append(...items){this.children.push(...items);}
  replaceChildren(...items){this._text='';this.children=[...items];}
  setAttribute(k,v){this.attributes[k]=String(v);}
  addEventListener(k,v){this.events[k]=v;}
  click(){if(this.events.click)this.events.click({target:this});else if(this.onclick)this.onclick();}
}
const elements={};for(const [,id] of source.matchAll(/\bid="([^"]+)"/g))elements[id]=new Element();
elements['af-data'].textContent=JSON.stringify(data);
const tabs=[...source.matchAll(/data-area="([^"]+)"/g)].map(m=>{const e=new Element('button');e.dataset.area=m[1];return e;});
elements['icw-african-contest'].querySelector=sel=>{assert(/^#[\w-]+$/.test(sel),sel);assert(elements[sel.slice(1)],'Missing DOM element '+sel);return elements[sel.slice(1)];};
elements['icw-african-contest'].querySelectorAll=sel=>sel==='.af-tabs button'?tabs:sel==='.af-focus'?elements['af-nodes'].children:assert.fail('Unknown selector '+sel);
const stateWrites=[],events={};
const context={document:{getElementById:id=>elements[id],createElement:tag=>new Element(tag),createElementNS:(ns,tag)=>new Element(tag)},window:{openai:{widgetState:null,setWidgetState:s=>{stateWrites.push(JSON.parse(JSON.stringify(s)));return Promise.resolve();}},addEventListener:(k,fn)=>{events[k]=fn;}},ResizeObserver:class{constructor(callback){this.callback=callback;}observe(){}},console};
vm.runInNewContext(script,context,{timeout:1000});
assert.equal(stateWrites.length,0,'Initial rendering must not save state');
let selected=0,priorities=0;
for(const tab of tabs){
  tab.click();
  const expected=data.nodes.filter(n=>n.area===tab.dataset.area);
  for(const n of expected){
    const button=elements['af-nodes'].children.find(b=>b.dataset.id===n.id);assert(button,n.id+' visible');button.click();
    assert.equal(elements['af-title'].textContent,n.title,n.id+' opens its inspector');
    const fx=elements['af-effects'].textContent;
    for(const text of n.effects)assert(fx.includes(text),n.id+' missing concrete effect '+text);
    if(n.deals.length)assert(fx.includes('If they accept:'),n.id+' must show prospective terms before consent');
    for(const t of n.deals){assert(fx.includes(t.country),n.id+' missing country');if(t.spirit)assert(fx.includes(t.spirit),n.id+' missing spirit');for(const [k,v] of Object.entries(t.modifiers))assert(fx.includes(k+': '+v),n.id+' missing modifier');if(t.setup)assert(fx.includes(t.setup),n.id+' missing setup');if(t.weekly)assert(fx.includes(t.weekly+' of '+t.weekly_basis),n.id+' missing weekly cost/basis');for(const a of t.assets)assert(fx.includes(a),n.id+' missing asset');}
    if(n.priority){
      const peers=data.nodes.filter(v=>v.priority===n.priority&&v.id!==n.id);assert.equal(peers.length,1,n.priority+' must have two funded alternatives');assert(elements['af-choice'].textContent.includes(peers[0].title));
      elements['af-choice'].children.find(c=>c.tagName==='button').click();
      assert.equal(stateWrites.at(-1).modelContent.priorities[n.priority],n.id);
      assert.equal(elements['af-title'].textContent,n.title);priorities++;
    }
    assert.equal(stateWrites.at(-1).modelContent.selected,n.id);selected++;
  }
}
assert.equal(selected,data.nodes.length);
assert.equal(priorities,8);
events['openai:set_globals']({detail:{globals:{widgetState:{revision:2,area:'horn',selected:'berbera',priorities:{horn:'kagnew'}}}}});
assert.equal(elements['af-title'].textContent,'Negotiate Berbera Access');
const excluded=elements['af-nodes'].children.find(b=>b.dataset.id==='berbera');assert(excluded.className.includes('is-other-priority'));excluded.click();assert.equal(elements['af-title'].textContent,'Negotiate Berbera Access','Other priority stays inspectable');
const copper=data.nodes.find(n=>n.id==='copperbelt').deals.find(d=>d.country==='Zaire');assert.equal(copper.setup_basis,'own GDP');assert.equal(copper.weekly_basis,'US GDP');
assert.equal(data.nodes.find(n=>n.id==='roundtable').deals.length,2,'Integrated opposition cannot receive a fictional state treasury');
tabs.find(b=>b.dataset.area==='operations').click();
elements['af-nodes'].children.find(b=>b.dataset.id==='finance_protests').click();
assert(elements['af-node-kind'].textContent.includes('PROPOSED TARGETED DECISION'));
assert(elements['af-effects'].textContent.includes('protest strength: +10'));
assert(!elements['af-effects'].textContent.includes('If they accept:'),'Hostile opposition funding does not need the target government to accept');
elements['af-nodes'].children.find(b=>b.dataset.id==='western_coup').click();
assert.equal(elements['af-node-kind'].textContent,'EXISTING MD ACTION');
assert(elements['af-rp'].textContent.includes('failure'));
const result={project:'IMPERIA COLD WAR',status:'PASS',clicked_entries:selected,priority_options:priorities,checks:['All real preview-script focus and action clicks open correct inspectors','Every country, spirit, signed modifier, GDP base, setup, weekly amount and asset remains visible before consent','All four priority pairs have both options and preserve inspection','Saved state restores the selected Horn strategy and inspection separately','Recipient GDP bases and integrated-state reconstruction are coherent'],scope:'Real emitted JavaScript in a bounded DOM fixture. Not browser rendering, CSS, native-engine or multiplayer proof.'};
fs.writeFileSync(path.join(root,'docs/design/usa_african_contest_20261030/INTERACTIONS.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
