# IMPERIA COLD WAR — Argentina live GDP cost inspector.
"""Build the standalone runtime finance inspector from approved tree data."""
from __future__ import annotations

import json
import re
import copy
from pathlib import Path
from typing import Any


def build_preview(root: str | Path, design: dict[str, Any]) -> dict[str, Path]:
    """Write only the runtime HTML template and emitted HTML; return both paths."""
    root = Path(root)
    out_dir = root / "docs/design/COLDWAR_ARG_1970"
    template_path = out_dir / "runtime-preview.template.html"
    output_path = out_dir / "runtime-preview.html"
    source = out_dir / "preview.template.html"
    concept_preview = out_dir / "COLDWAR_ARG_preview.html"

    template = source.read_text(encoding="utf-8")
    # Existing local preview holds the already approved native art as embedded data.
    emitted = concept_preview.read_text(encoding="utf-8")
    art_match = re.search(r",art=(\{.*?\});\s*const\s*\$=", emitted, re.S)
    if not art_match:
        # Standalone review wrapper uses the same source fragment but may not have the
        # exact whitespace above. Stop instead of silently substituting new art.
        art_match = re.search(r"art=(\{.*?\});\s*const\s*\$=", emitted, re.S)
    if not art_match:
        raise ValueError("Could not extract the existing embedded Argentina preview art")
    art_json = art_match.group(1)
    display_design = copy.deepcopy(design)
    source_gdp = (root / "common/scripted_effects/IMP_1970_gdp_scripted_effects.txt").read_text(encoding="utf-8-sig")
    targets = {
        tag: round(float(target) * 3.4, 5)
        for tag, target in re.findall(
            r"original_tag\s*=\s*([A-Z0-9]{3}).*?imp_1970_target_gdp\s*=\s*([0-9]+(?:\.[0-9]+)?)",
            source_gdp,
            re.S,
        )
    }
    # The approved Argentine runtime input preserves its more precise native baseline.
    targets["ARG"] = float(display_design["budget_revision"]["arg_1970_internal_gdp"])
    first_partner = display_design["agreements"][0]["partner"]
    display_design["preview_gdp_estimates"] = {
        "source": "IMPERIA COLD WAR 1970 scripted GDP targets multiplied by 3.4; scenario GDP can exceed the estimate",
        "values": targets,
    }
    initial_recipient_gdp = targets.get(first_partner, targets["ARG"])
    data_json = json.dumps(display_design, ensure_ascii=False, separators=(",", ":"))

    template = template.replace(
        "<!-- IMPERIA COLD WAR — Argentina approval concept using native MD focus art and resolved geometry. -->",
        "<!-- IMPERIA COLD WAR — Argentina implemented runtime GDP cost inspector. -->",
    )
    template = template.replace("NATIONAL FOCUS CONCEPT", "IMPLEMENTED RUNTIME PREVIEW")
    # Link the visible title/icon ports in the single-row compact layout. The
    # horizontal rail remains inside the native two-pixel inter-row gap.
    template = template.replace('ay=py(p)+128,bx=px(n)+82.5,by=py(n),mid=', 'ay=py(p)+115,bx=px(n)+82.5,by=py(n)+12,mid=')
    template = template.replace(
        '<label>Government<select id="ar-government" aria-label="Governing party"></select></label>',
        '<label>Government<select id="ar-government" aria-label="Governing party"></select></label>'
        '<label>Argentina GDP, $bn<input id="ar-gdp" type="number" min="0.00001" step="0.00001" value="107.38543"></label>'
        '<label><span id="ar-recipient-gdp-label">Recipient GDP, $bn (' + first_partner + ' estimate)</span><input id="ar-recipient-gdp" type="number" min="0.00001" step="0.00001" value="' + f'{initial_recipient_gdp:.5f}' + '"></label>',
    )
    template = template.replace(
        "#coldwar-argentina select{width:235px}",
        "#coldwar-argentina select{width:235px}\n#coldwar-argentina input{font:13px Arial,sans-serif;padding:7px 9px;color:#e8e6d6;background:#3a483a;border:1px solid #79836b;border-radius:0;width:165px}",
    )
    template = template.replace(
        '<span>Concept composition. Font and connector routing approximated.</span>',
        '<span>Runtime budget preview. Native font and connector routing approximated. Estimated Argentine native GDP is $107.38543 bn, calibrated from 1970 scripted GDP targets x 3.4 against the $31.58395 bn historical display baseline. Recipient estimates use their scripted targets x 3.4. Live GDP can exceed these targets; treasury amounts use current GDP.</span>',
    )
    template = template.replace(
        "const root=document.getElementById('coldwar-argentina'),data=__DATA__,art=__ART__;",
        "const root=document.getElementById('coldwar-argentina'),data=__DATA__,art=__ART__;",
    )
    template = template.replace(
        "const chapter=$('#ar-chapter'),government=$('#ar-government'),viewport=",
        "const chapter=$('#ar-chapter'),government=$('#ar-government'),gdpInput=$('#ar-gdp'),recipientGDPInput=$('#ar-recipient-gdp'),viewport=",
    )
    template = template.replace(
        "const money=v=>'$'+Math.abs(v).toFixed(5).replace(/0{1,2}$/,'')+' billion';",
        "const money=v=>'$'+Math.abs(v).toFixed(5)+' bn';\n"
        "const annualShare=s=>(Number(s||0)*100).toFixed(3).replace(/0+$/,'').replace(/\\.$/,'')+'% annual GDP';\n"
        "const oneoffShare=s=>(Number(s||0)*100).toFixed(3).replace(/0+$/,'').replace(/\\.$/,'')+'% GDP';\n"
        "const argGDP=()=>Math.max(0,Number(gdpInput.value)||0),recipientGDP=()=>Math.max(0,Number(recipientGDPInput.value)||0);\n"
        "const budgetAmount=(share,gdp)=>Number(share||0)*gdp,weeklyAmount=(share,gdp)=>Number(share||0)*gdp/52;\n"
        "let recipientTag=" + json.dumps(first_partner) + ";const recipientOverrides={};\n"
        "function setRecipientTag(tag){if(!tag)return;recipientTag=tag;const estimate=Number(data.preview_gdp_estimates?.values?.[tag]??data.budget_revision.arg_1970_internal_gdp),overridden=Object.prototype.hasOwnProperty.call(recipientOverrides,tag);recipientGDPInput.value=Number(overridden?recipientOverrides[tag]:estimate).toFixed(5);$('#ar-recipient-gdp-label').textContent='Recipient GDP, $bn ('+tag+(overridden?' override':' estimate')+')'}",
    )
    old_fx = "const moneyFx=(amount,weekly=0,credit=0)=> (amount?'<li>Treasury: <span class=\"'+(amount>0?'ar-negative':'ar-positive')+'\">'+(amount>0?'-':'+')+money(amount)+'</span></li>':'')+(weekly?'<li>Additional expenses: <span class=\"ar-negative\">+'+money(weekly)+' weekly</span></li>':'')+(credit?'<li>Additional income: <span class=\"ar-positive\">+'+money(credit)+' weekly</span></li>':'');"
    new_fx = "const moneyFx=(legacy,legacyWeekly=0,credit=0,setupShare=0,annual=0,basis=argGDP())=>{const setup=setupShare?budgetAmount(setupShare,basis):0,week=weeklyAmount(annual,basis);return (setup?'<li>Treasury: <span class=\"ar-negative\">-'+money(setup)+'</span> ('+oneoffShare(setupShare)+')</li>':legacy<0?'<li>Treasury: <span class=\"ar-positive\">+'+money(Math.abs(legacy))+'</span></li>':'')+(week?'<li>Weekly appropriation: <span class=\"ar-negative\">-'+money(week)+'</span> ('+annualShare(annual)+')</li>':'')+(credit?'<li>Weekly credit: <span class=\"ar-positive\">+'+money(weeklyAmount(credit,basis))+'</span> ('+annualShare(credit)+')</li>':'')};"
    if old_fx not in template:
        raise ValueError("Could not locate money effect renderer in native preview template")
    template = template.replace(old_fx, new_fx)
    template = template.replace(
        "function agreementSide(a,side,tag){const t=a[side];let out='<section><h4>'+esc(data.countries[tag])+'</h4><ul>'+moneyFx(t.setup,t.weekly,t.credit)+(t.grant?moneyFx(-t.grant):'')+'<li>Add national spirit: '+esc(t.spirit)+'<ul>'+modList(t.modifiers)+'</ul></li>'+buildingList(a.buildings.filter(b=>b.country===tag))+researchList(a.research.filter(r=>r.country===tag));",
        "function agreementSide(a,side,tag){const t=a[side],basis=tag==='ARG'?argGDP():recipientGDP();let out='<section><h4>'+esc(data.countries[tag])+'</h4><ul>'+moneyFx(t.setup,t.weekly,0,t.setup_gdp_share,t.weekly_own_annual_gdp_share,basis)+(a.transfer&&a.transfer.payer===tag?'<li>Transfer payment: <span class=\"ar-negative\">-'+money(weeklyAmount(a.transfer.annual_arg_gdp_share,argGDP()))+'</span> weekly ('+annualShare(a.transfer.annual_arg_gdp_share)+' of Argentine GDP)</li>':'')+(a.transfer&&a.transfer.recipient===tag?'<li>Transfer income: <span class=\"ar-positive\">+'+money(weeklyAmount(a.transfer.annual_arg_gdp_share,argGDP()))+'</span> weekly ('+annualShare(a.transfer.annual_arg_gdp_share)+' of Argentine GDP)</li>':'')+(t.grant_arg_gdp_share?'<li>Argentine-funded grant: <span class=\"ar-positive\">+'+money(budgetAmount(t.grant_arg_gdp_share,argGDP()))+'</span> ('+oneoffShare(t.grant_arg_gdp_share)+' of Argentine GDP)</li>':'')+'<li>Add national spirit: '+esc(t.spirit)+'<ul>'+modList(t.modifiers)+'</ul></li>'+buildingList(a.buildings.filter(b=>b.country===tag))+researchList(a.research.filter(r=>r.country===tag));",
    )
    template = template.replace(
        "let out='<section><h4>'+esc(data.countries[tag])+'</h4><ul>'+moneyFx(t.setup,t.weekly,t.credit,t.setup_gdp_share,t.weekly_own_annual_gdp_share,basis)+(t.grant?moneyFx(-t.grant,0,0,0,0,basis):'')",
        "let out='<section><h4>'+esc(data.countries[tag])+'</h4><ul>'+moneyFx(t.setup,t.weekly,0,t.setup_gdp_share,t.weekly_own_annual_gdp_share,basis)",
    )
    template = template.replace(
        "html+='<h4>Effects</h4><ul>'+moneyFx(n.money,n.weekly);",
        "html+='<h4>Effects</h4><ul>'+moneyFx(n.money,n.weekly,0,n.money_gdp_share,n.weekly_annual_gdp_share,argGDP());",
    )
    template = template.replace("let out=moneyFx(d.money,d.weekly);", "let out=moneyFx(d.money,d.weekly,0,d.money_gdp_share,d.weekly_annual_gdp_share,argGDP());")
    template = template.replace("'<ul>'+moneyFx(o.money,o.weekly)+", "'<ul>'+moneyFx(o.money,o.weekly,0,o.money_gdp_share,o.weekly_annual_gdp_share,argGDP())+")
    template = template.replace("if(ids[state.selected])inspect(ids[state.selected]);", "if(ids[state.selected]){const selected=ids[state.selected];if(selected.agreement){const a=data.agreements.find(x=>x.id===selected.agreement);if(a)setRecipientTag(a.partner)}inspect(selected)}")
    template = template.replace(
        "function showNode(n,persist=true){state.selected=n.id;state.mode='tree';inspect(n);",
        "function showNode(n,persist=true){state.selected=n.id;state.mode='tree';if(n.agreement){const a=data.agreements.find(x=>x.id===n.agreement);if(a)setRecipientTag(a.partner)}inspect(n);",
    )
    # Remove implementation references from focus Effects while retaining runtime guards elsewhere.
    start = " html+='<details><summary>Design record and native API references</summary>"
    end = " inspector.innerHTML=html;"
    i, j = template.find(start), template.find(end)
    if i < 0 or j < 0:
        raise ValueError("Could not locate the focus implementation-details block")
    template = template[:i] + "\n" + template[j:]
    template = template.replace("const save=()=>window.openai?.setWidgetState?.({modelContent:{selected:state.selected,government:state.government,chapter:state.chapter},privateContent:{mode:state.mode}}).catch(()=>{});", "const save=()=>{};")
    # Re-render selected inspector amounts whenever either live GDP estimate changes.
    marker = "chapter.addEventListener('change',()=>{"
    template = template.replace(marker, "function refreshBudgetInspector(){if(state.mode==='tree'&&ids[state.selected])inspect(ids[state.selected]);else if(state.mode==='events')showEvents($('#ar-event')?.value||null,false)}gdpInput.addEventListener('input',refreshBudgetInspector);recipientGDPInput.addEventListener('input',()=>{recipientOverrides[recipientTag]=recipientGDP();$('#ar-recipient-gdp-label').textContent='Recipient GDP, $bn ('+recipientTag+' override)';refreshBudgetInspector()});\n" + marker)
    template_path.write_text(template, encoding="utf-8")
    emitted_html = template.replace("__DATA__", data_json).replace("__ART__", art_json)
    output_path.write_text(emitted_html, encoding="utf-8")
    return {"template": template_path, "html": output_path}


def main() -> None:
    root = Path(__file__).resolve().parents[2]
    design = json.loads((root / "tools/argentina_1970/runtime_design.json").read_text(encoding="utf-8"))
    result = build_preview(root, design)
    print(json.dumps({k: str(v) for k, v in result.items()}))


if __name__ == "__main__":
    main()
