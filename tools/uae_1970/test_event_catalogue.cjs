// Local data/interaction checks; not a browser or HOI4 rendering test.
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const file = 'C:/Users/Enes/.codex/visualizations/2026/10/19/01a153f9-9c59-71b2-8460-d28a5d918d07/uae-gcc-events.html';
const fragment = fs.readFileSync(file,'utf8');
const script = fragment.match(/<script>([\s\S]*?)<\/script>/)[1];
class Element {
  constructor(tag) { this.tag=tag; this.children=[]; this.attributes={}; this.value=''; this.textContent=''; }
  append(...children) { this.children.push(...children); }
  replaceChildren(...children) { this.children=[...children]; }
  setAttribute(key,value) { this.attributes[key]=value; }
}
const elements={};
for(const match of fragment.matchAll(/\bid="([^"]+)"/g)) elements[match[1]]=new Element(match[1]);
elements['cw-events-review'].querySelector=selector=>elements[selector.slice(1)];
const document={getElementById:id=>elements[id],createElement:tag=>new Element(tag)};
const window={addEventListener:()=>{}};
const context=vm.createContext({document,window,Response,Blob,DecompressionStream,Uint8Array,atob,console});
(async()=>{
  await new vm.Script(script).runInContext(context);
  const types=elements['cw-event-type'], ids=elements['cw-event-id'];
  if(types.children.length!==16)throw new Error('Missing event groups');
  let events=0,options=0;
  for(const opt of types.children){
    types.value=opt.value; types.onchange();
    for(const id of ids.children){
      ids.value=id.value; ids.onchange();
      if(!elements['cw-event-title'].textContent)throw new Error('Blank event title');
      if(!elements['cw-event-picture'].src?.startsWith('data:image/jpeg;base64,'))throw new Error('Missing picture');
      const source=elements['cw-event-code'].textContent;
      if(!source.includes('id = '+id.textContent))throw new Error('Wrong exact event source');
      for(const button of elements['cw-event-options'].children){button.onclick();options++;}
      events++;
    }
  }
  if(events!==2112)throw new Error('Missing exact event IDs');
  const report={passed:true,groups:types.children.length,events,options,bytes:Buffer.byteLength(fragment),
    allExactSourcesPresent:true,allPrimarySelectionsExercised:true,browserTested:false,engineTested:false};
  fs.writeFileSync(path.join(__dirname,'EVENT_PREVIEW_VALIDATION.json'),JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report));
})().catch(error=>{console.error(error);process.exitCode=1});
