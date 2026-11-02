// IMPERIA COLD WAR — Interactive review of Turkish intervention and Greek escalation.
const baseInterventionState={phase:'choice',day:0,pressure:70,used:[],greekBranch:null,greekWar:false,cyprusWar:false,natoGreece:true,natoTurkey:true,notice:''};
const allowedInterventionPhases=['choice','terms','army','control','coup','war','volunteers','peace'];
const readableInterventionText=text=>String(text).replace(/(?<=[A-Za-z])(?=\d)/g,' ').replace(/(?<=\d)(?=[A-Za-z])/g,' ').replace(/(?<=%)(?=[A-Za-z])/g,' ');
function readInterventionState(value){
 if(!value||!allowedInterventionPhases.includes(value.phase))return {...baseInterventionState,used:[]};
 return {...baseInterventionState,...value,used:Array.isArray(value.used)?value.used.filter(k=>['rotate','mandate','control','intervene'].includes(k)):[],day:Math.max(0,Math.min(180,Number(value.day)||0)),pressure:Math.max(0,Math.min(100,Number(value.pressure)||0))};
}
let interventionState=readInterventionState(saved.privateContent?.intervention);
function interventionAction(label,callback,disabled=false){let b=document.createElement('button');b.type='button';b.textContent=readableInterventionText(label);b.disabled=disabled;b.addEventListener('click',()=>{callback();drawIntervention();store()});$('#cw-intervention-actions').append(b)}
function interventionList(spirit){
 return '<h3>'+esc(spirit.name)+(spirit.days?' · '+spirit.days+' days':'')+'</h3><ul class="cw-effects">'+Object.entries(spirit.values).map(([k,v])=>'<li>'+esc(D.modifier_labels[k])+' '+(k==='send_volunteer_size'?(v>=0?'+':'')+v:pct(v))+'</li>').join('')+'</ul>';
}
function startTurkishIntervention(){
 interventionState.phase='war';interventionState.cyprusWar=true;interventionState.greekBranch=null;
 interventionState.notice='Turkey authorizes intervention. The temporary military bonus begins with the real war. Greece now chooses its exclusive support path.';
}
function drawIntervention(){
 const s=interventionState,i=D.intervention;
 $('#cw-intervention-actions').innerHTML='';
 $('#cw-intervention-state').textContent=({choice:'The Turkish Choice',terms:'Negotiated Safeguards',army:'Angry General Staff',control:'Civilian Authority Restored',coup:'Military Takeover',war:'The Cyprus War',volunteers:'The Volunteer Mission',peace:'Peace and NATO Return'})[s.phase];
 $('#cw-intervention-notice').textContent=readableInterventionText(s.notice||'An unresolved constitutional rupture and failed guarantor consultation open the Turkish intervention window.');
 $('#cw-intervention-membership').textContent='Greece: '+(s.natoGreece?'NATO member':'temporarily outside NATO')+' · Turkey: '+(s.natoTurkey?'NATO member':'temporarily outside NATO');
 $('#cw-intervention-pressure').hidden=s.phase!=='army';
 $('#cw-intervention-pressure-label').textContent='Day '+s.day+' · Military pressure '+s.pressure+'/100 · Coup resolution: day '+i.coup_day;
 $('#cw-intervention-pressure-fill').style.width=s.pressure+'%';
 $('#cw-intervention-pressure-meter').setAttribute('aria-valuenow',s.pressure);
 let details='';
 if(s.phase==='choice'){
  details='<p>Exclusive Turkish focus paths: intervention, an accepted settlement, or refusal. Refusal starts the army crisis immediately; an unresolved diplomatic deadline starts it after '+i.initial_deadline_days+' days.</p>';
  interventionAction('Intervene in Cyprus',startTurkishIntervention);
  interventionAction('Negotiate safeguards',()=>{s.phase='terms';s.notice='Cyprus and the relevant delegations must accept the terms. A failed settlement does not remove the intervention deadline.'});
  interventionAction('Refuse intervention',()=>{s.phase='army';s.day=0;s.pressure=i.military_pressure_initial;s.used=[];s.notice='The refusal activates a180-day penalty. Two once-only control measures reduce pressure by25each; a military memorandum adds15on day30. An uncontained plot can succeed on day60.'});
 }else if(s.phase==='terms'){
  details='<p>Successful constitutional restoration resolves the external security crisis. Unaccepted terms leave the crisis open.</p>';
  interventionAction('Preview accepted terms',()=>{s.phase='peace';s.notice='All required terms are accepted and the Cyprus security crisis is resolved. The intervention countdown and military confrontation end.'});
  interventionAction('Preview failed deadline',()=>{s.phase='army';s.pressure=i.military_pressure_initial;s.day=0;s.used=[];s.notice='No settlement was accepted before the30-day deadline. Angry General Staff and the finite crisis chain now begin.'});
 }else if(s.phase==='army'){
  details=interventionList(i.angry_army)+'<p>At pressure 60 or above on day 60: military takeover. At pressure 35 or below, with both control measures: the plot is defeated. Intervention removes the refusal penalty.</p>';
  for(const key of ['rotate','mandate']){let d=D.crisis_decisions.find(c=>c.key===key);interventionAction(d.title+' ('+d.pp_cost+' PP'+(d.gdp_percent?', '+d.gdp_percent+'% GDP':'')+')',()=>{s.used.push(key);s.pressure=Math.max(0,s.pressure+d.pressure_delta);s.notice=d.title+': pressure reduced by25. This action cannot be repeated.'},s.used.includes(key))}
  interventionAction('Reassert civilian authority (75 PP, 0.25% GDP)',()=>{s.used.push('control');s.phase='control';s.notice='The coup chain is closed. Angry General Staff is replaced by90days of Command Reorganization.'},!['rotate','mandate'].every(k=>s.used.includes(k))||s.pressure>i.civilian_control_pressure_max);
  interventionAction('Authorize the Cyprus operation',startTurkishIntervention);
  interventionAction('Advance 30 days',()=>{
   const before=s.day;s.day=Math.min(180,s.day+30);
   if(before<i.memorandum_day&&s.day>=i.memorandum_day){s.pressure=Math.min(100,s.pressure+i.memorandum_pressure_delta);s.notice='The General Staff memorandum adds15pressure. The coup deadline is day60.'}
   if(before<i.coup_day&&s.day>=i.coup_day){
    if(s.pressure>=i.successful_coup_pressure_min){s.phase='coup';s.notice='Pressure reached the disclosed coup threshold. A dated native military-junta government replaces civilian rule. No extra war is declared automatically.'}
    else if(s.pressure<=i.civilian_control_pressure_max&&['rotate','mandate'].every(k=>s.used.includes(k))){s.notice='The plot is defeated by the completed control measures. Reasserting civilian authority removes the remaining refusal penalty.'}
    else{s.notice='The attempted coup fails, with stability-5%. Remaining army discontent must still be managed.'}
   }
   if(s.day>=180){s.phase='peace';s.notice='The180-day army penalty expires. The recorded coup outcome and other permanent political changes are preserved.'}
  },s.day>=180);
 }else if(s.phase==='control'){
  details=interventionList(i.civilian_control_spirit)+'<p>The Cyprus war was avoided. Existing NATO membership remains intact.</p>';
 }else if(s.phase==='coup'){
  details='<p>A takeover is a Turkish political consequence of the unresolved army confrontation. It does not choose another war for the player.</p>';
  interventionAction('Authorize intervention under the new government',startTurkishIntervention);
 }else if(s.phase==='war'||s.phase==='volunteers'){
  details=interventionList(i.intervention_buff)+'<p>Turkey: setup 0.5% of own GDP; expedition expense 0.005% of GDP per week. The bonus ends after 180 days or at related peace.</p>';
  if(!s.greekBranch){
   interventionAction('Greece: volunteers for Cyprus',()=>{s.phase='volunteers';s.greekBranch='volunteers';s.notice='The volunteer focus offers help to Cyprus. Actual units still require an accepted, engine-eligible volunteer deployment. NATO status is unchanged.'});
   interventionAction('Greece: fight beside Cyprus',()=>{s.greekBranch='direct';s.greekWar=true;s.natoGreece=false;s.natoTurkey=false;s.notice='Both prior members leave NATO before Greece joins the Cyprus side against Turkey. Both restore membership after the two relevant war relations end.'});
  }
  if(s.greekBranch==='volunteers')details+=interventionList(i.volunteer_spirit)+'<p>Volunteer diplomatic eligibility while Turkey remains a NATO ally requires live-game validation.</p>';
  if(s.cyprusWar)interventionAction('Cyprus-Turkey peace',()=>{s.cyprusWar=false;s.notice=s.greekWar?'Cyprus-Turkey hostilities ended. Greece-Turkey war continues, so both NATO returns are still pending.':'The Cyprus war ended. No active Greek-Turkish war remains.';finishInterventionPeace()});
  if(s.greekWar)interventionAction('Greece-Turkey peace',()=>{s.greekWar=false;s.notice=s.cyprusWar?'Greece-Turkey hostilities ended. Cyprus-Turkey war continues, so both NATO returns are still pending.':'Both relevant wars ended.';finishInterventionPeace()});
 }else if(s.phase==='peace'){
  details='<p>No related war remains in this preview. Prior Greek and Turkish NATO membership is restored automatically when the native return conditions are valid.</p>';
 }
 $('#cw-intervention-effects').innerHTML=details;
 interventionAction('Restart preview',()=>{interventionState={...baseInterventionState,used:[]}});
}
function finishInterventionPeace(){
 const s=interventionState;if(s.cyprusWar||s.greekWar)return;
 s.phase='peace';s.natoGreece=true;s.natoTurkey=true;s.notice='Greece-Turkey and Cyprus-Turkey peace are both confirmed. Both prior members return to NATO automatically; no unrelated war must end.';
}
window.addEventListener('openai:set_globals',e=>{let incoming=e.detail?.globals?.widgetState?.privateContent?.intervention;if(incoming){interventionState=readInterventionState(incoming);drawIntervention()}});
drawIntervention();
