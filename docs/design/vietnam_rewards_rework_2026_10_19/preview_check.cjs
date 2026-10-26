// Selected-state and click/pan checks, using DOM mocks rather than a browser.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const html=fs.readFileSync('C:/Users/Enes/.codex/visualizations/2026/10/18/01a14f32-41dc-74b3-baa1-8f6916e026ed/coldwar-vietnam-rewards.html','utf8');
const data=JSON.parse(html.match(/<script type="application\/json" id="vr-data">([\s\S]*?)<\/script>/)[1]);
const script=html.match(/<script>\s*([\s\S]*?)<\/script>/)[1];
const noop=()=>{},ctx=new Proxy({},{get:(o,k)=>o[k]||noop,set:(o,k,v)=>(o[k]=v,true)});
class El{
 constructor(tag='div'){this.tagName=tag;this.children=[];this.listeners={};this.attrs={};this.textContent='';this.value=''}
 append(...e){this.children.push(...e)}replaceChildren(...e){this.children=e}setAttribute(k,v){this.attrs[k]=v}
 addEventListener(k,v){this.listeners[k]=v}getBoundingClientRect(){return {left:0,top:0,width:960,height:400}}
 getContext(){return ctx}setPointerCapture(){this.capture=true}hasPointerCapture(){return this.capture}releasePointerCapture(){this.capture=false}
 fire(k,e={}){return this.listeners[k](e)}
}
const els={};for(const m of html.matchAll(/\bid="([^"]+)"/g))els['#'+m[1]]=new El();
els['#vr-data'].textContent=JSON.stringify(data);els['#vie-rewards-installed'].querySelector=s=>{assert(els[s],s);return els[s]};
let saves=0,snapshot;const handlers={};
const window={devicePixelRatio:1,addEventListener:(k,v)=>handlers[k]=v,openai:{setWidgetState:s=>{saves++;snapshot=s;return Promise.resolve()}}};
class Img{constructor(){this.width=95;this.height=88}set src(v){assert(v.startsWith('data:image/'));this.onload?.()}}
vm.runInNewContext(script,{document:{getElementById:id=>els['#'+id],createElement:t=>new El(t)},window,Image:Img,ResizeObserver:class{constructor(f){this.f=f}observe(){this.f()}},requestAnimationFrame:f=>f()});
assert.equal(saves,0);assert.equal(data.nodes.length,307);let peers=0;
for(const n of data.nodes){
 els['#vr-focus'].value=n.id;els['#vr-focus'].fire('change');assert.equal(els['#vr-title'].textContent,n.label);
 assert(els['#vr-effects'].children.length>0,'Empty actual rewards '+n.id);
 els['#vr-focus'].value='';els['#vr-canvas'].fire('pointerdown',{button:0,pointerId:1,clientX:480,clientY:200});els['#vr-canvas'].fire('pointerup',{pointerId:1,clientX:480,clientY:200});
 assert.equal(els['#vr-focus'].value,n.id,'Pointer target '+n.id);
 if(n.exclusive.length){els['#vr-peer'].fire('click');assert.equal(els['#vr-focus'].value,n.exclusive[0]);peers++}
}
const before=els['#vr-focus'].value;
els['#vr-canvas'].fire('pointerdown',{button:0,pointerId:2,clientX:480,clientY:200});els['#vr-canvas'].fire('pointermove',{clientX:500,clientY:210});els['#vr-canvas'].fire('pointerup',{pointerId:2,clientX:500,clientY:210});assert.equal(els['#vr-focus'].value,before);
for(const id of ['vr-in','vr-out','vr-fit'])els['#'+id].fire('click');
els['#vr-canvas'].fire('wheel',{deltaY:50,clientX:300,clientY:200,preventDefault:noop});
const prev=saves;handlers['openai:set_globals']({detail:{globals:{widgetState:snapshot}}});assert.equal(saves,prev);
assert(Buffer.byteLength(html)<1e6);
const report={status:'passed',focus_selections:307,pointer_clicks:307,alternative_selections:peers,pan_and_zoom:true,state_restore:true,html_bytes:Buffer.byteLength(html),browser_tested:false,engine_tested:false};
fs.writeFileSync(__dirname+'/preview_logic_check.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
