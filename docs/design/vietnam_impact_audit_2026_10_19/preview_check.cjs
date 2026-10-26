// Logic checks for the review UI. DOM mock, not browser or engine verification.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const path='C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f32-41dc-74b3-baa1-8f6916e026ed/coldwar-vietnam-impact.html';
const html=fs.readFileSync(path,'utf8');
const data=JSON.parse(html.match(/<script type="application\/json" id="vi-audit-data">([\s\S]*?)<\/script>/)[1]);
const script=html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
assert(Buffer.byteLength(html)<1e6);assert(!html.includes('__AUDIT_DATA__'));
assert.equal(data.nodes.length,307);assert.equal(new Set(data.nodes.map(n=>n.id)).size,307);
assert.equal(data.issues.length,12);assert.equal(data.choices.length,13);
const noop=()=>{};
const ctx=new Proxy({}, {get:(o,k)=>o[k]||noop,set:(o,k,v)=>(o[k]=v,true)});
class El{
 constructor(tag='div'){this.tagName=tag;this.children=[];this.listeners={};this.attrs={};this.value='';this.textContent='';}
 append(...e){this.children.push(...e)}
 replaceChildren(...e){this.children=e}
 setAttribute(k,v){this.attrs[k]=v}
 addEventListener(k,v){this.listeners[k]=v}
 getBoundingClientRect(){return {left:0,top:0,width:804,height:540}}
 getContext(){return ctx}
 setPointerCapture(){this.capture=true}
 hasPointerCapture(){return !!this.capture}
 releasePointerCapture(){this.capture=false}
 fire(type,e={}){assert(this.listeners[type],'Missing listener: '+type);return this.listeners[type](e)}
}
const els={};for(const id of html.matchAll(/\bid="([^"]+)"/g))els['#'+id[1]]=new El();
els['#vi-audit-data'].textContent=JSON.stringify(data);els['.vi-issues']=new El();
const root=els['#vie-impact-review'];root.querySelector=s=>{assert(els[s],'Unknown selector '+s);return els[s]};
let saves=0,lastState,followup;
const handlers={};
const win={devicePixelRatio:1,addEventListener:(k,v)=>handlers[k]=v,openai:{
 setWidgetState:s=>{saves++;lastState=s;return Promise.resolve()},
 sendFollowUpMessage:q=>{followup=q;return Promise.resolve()}
}};
class MockImage{constructor(){this.width=95;this.height=88}set src(s){assert(s.startsWith('data:image/'));this.onload?.()}}
const context={document:{getElementById:id=>els['#'+id],createElement:tag=>new El(tag)},window:win,
 Image:MockImage,ResizeObserver:class{constructor(cb){this.cb=cb}observe(){this.cb()}},requestAnimationFrame:f=>f()};
vm.runInNewContext(script,context,{filename:'vietnam-review.js'});
assert.equal(saves,0,'Initial display must not write saved state');
assert.equal(els['.vi-issues'].children.length,12);
const flatten=n=>n.children.flatMap(c=>[c,...flatten(c)]);
assert.equal(flatten(els['#vi-focus']).filter(e=>e.tagName==='option').length,307);
for(const n of data.nodes){
 els['#vi-focus'].value=n.id;els['#vi-focus'].fire('change');
 assert.equal(els['#vi-focus-title'].textContent,n.label);
 assert(els['#vi-effects'].children.length>0,'Empty effect inspector: '+n.id);
 assert.equal(els['#vi-focus-art'].src,data.art[n.icon]);
 // A real click at the newly centered focus must select it, even when locked in game.
 els['#vi-focus'].value='';
 els['#vi-canvas'].fire('pointerdown',{button:0,pointerId:1,clientX:402,clientY:270});
 els['#vi-canvas'].fire('pointerup',{pointerId:1,clientX:402,clientY:270});
 assert.equal(els['#vi-focus'].value,n.id,'Focus hit failed: '+n.id);
}
for(let i=0;i<12;i++){
 els['.vi-issues'].children[i].fire('click');
 assert.equal(els['#vi-finding-title'].textContent,data.issues[i].title);
 assert.equal(els['#vi-focus'].value,data.issues[i].ids[0]);
}
for(let i=0;i<data.choices.length;i++){
 els['#vi-choice'].value=String(i);els['#vi-choice'].fire('change');
 assert.equal(els['#vi-options'].children.length,2);
 assert.equal(els['#vi-choice-title'].textContent,data.choices[i].title);
}
const prior=els['#vi-focus'].value;
els['#vi-canvas'].fire('pointerdown',{button:0,pointerId:2,clientX:402,clientY:270});
els['#vi-canvas'].fire('pointermove',{pointerId:2,clientX:492,clientY:280});
els['#vi-canvas'].fire('pointerup',{pointerId:2,clientX:492,clientY:280});
assert.equal(els['#vi-focus'].value,prior,'Panning must not click another card');
for(const b of ['plus','minus','fit'])els['#vi-'+b].fire('click');
els['#vi-canvas'].fire('wheel',{preventDefault:noop,deltaY:90,clientX:300,clientY:200});
els['#vi-tab-proposed'].fire('click');assert(els['#vi-current'].hidden);assert(!els['#vi-proposed'].hidden);
els['#vi-proposal-followup'].fire('click');assert(followup.prompt.includes(data.choices.at(-1).title));
const previousSaves=saves;
handlers['openai:set_globals']({detail:{globals:{widgetState:lastState}}});
assert.equal(saves,previousSaves,'Restoring host state must not save recursively');
for(const n of data.nodes)assert(data.art[n.icon],'Missing native icon '+n.id);
const report={status:'passed',focus_selects:307,focus_pointer_clicks:307,issue_selections:12,choice_pairs:data.choices.length,
 panning_and_zoom:true,host_state_and_followup:true,html_bytes:Buffer.byteLength(html),
 browser_tested:false,engine_tested:false,method:'Node VM with DOM/canvas mocks; native card proofs inspected separately'};
fs.writeFileSync(__dirname+'/preview_logic_check.json',JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report));
