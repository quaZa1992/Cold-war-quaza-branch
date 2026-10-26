// Inserted in the existing native focus-view closure; all interaction is local.
function showTreaties(){
 mode='treaties';
 const selection=treatyStatus.value;
 const variantId={subject:'starting',transition:'scheduled',loyal:'protection',free:'fulfilled',friendship:'friendship'}[selection];
 if(!variantId){detail.innerHTML='<h3>No active UK release agreement in this view</h3><p>The UAE is subject to another overlord. A stale British offer cannot release that relationship, and the sovereign formation focus remains locked.</p>';return;}
 const agreement=data.british_treaties.variants.find(v=>v.id===variantId);
 const cards=[['United Kingdom','uk_spirit','uk_terms'],['UAE / Trucial States','uae_spirit','uae_terms']].map(([country,spirit,terms])=>
  `<article class="uae-treaty-card"><div class="uae-treaty-heading"><img src="${data.assets.icons[agreement.icon]}" alt=""><div><h4>${esc(country)}</h4><p>${esc(agreement.label)}</p></div></div><dl><dt>Status</dt><dd>${esc(agreement.status)}</dd><dt>${esc(agreement.date_label)}</dt><dd class="uae-treaty-date">${esc(agreement.date)}</dd><dt>Independence</dt><dd>${esc(agreement.independence)}</dd></dl><ul>${agreement[terms].map(t=>'<li>'+esc(t)+'</li>').join('')}</ul><details><summary>Proposed national spirit</summary><code>${esc(agreement[spirit])}</code></details></article>`).join('');
 detail.innerHTML=`<h3>UK–UAE Agreement · Paired National Spirits</h3><div class="uae-treaty-grid">${cards}</div><details><summary>Agreement dates and execution</summary><p>${esc(data.british_treaties.timer_contract)}</p><p>${esc(data.british_treaties.delivery_contract)}</p><p>${esc(data.british_treaties.changes_contract)}</p><pre>${esc(data.british_treaties.release_effect)}</pre></details>`;
}
treatyStatus.addEventListener('change',()=>{paintGovernment();if(mode==='treaties')showTreaties();else if(mode==='tree')branch();remember();});
