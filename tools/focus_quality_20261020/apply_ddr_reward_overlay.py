# IMPERIA COLD WAR — DDR bounded reward overlay writer.
"""Rebuild reward-only DDR focus changes from the immutable canonical inputs."""
from __future__ import annotations
import json,re,sys,os,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OVERLAY=ROOT/"Claude outputs/COLDWAR_DDR_generator/design/ddr_reward_overlay_20261027.json"
TREE=ROOT/"common/national_focus/COLDWAR_DDR_1970_focus.txt"
LOC=ROOT/"localisation/english/COLDWAR_DDR_1970_l_english.yml"
DYN=ROOT/"common/dynamic_modifiers/COLDWAR_DDR_1970_dynamic_modifiers.txt"
TT=ROOT/"localisation/english/COLDWAR_modifier_tooltips_l_english.yml"
OUT_EFFECT=ROOT/"common/scripted_effects/COLDWAR_DDR_20261027_programmes.txt"
OUT_TRIGGER=ROOT/"common/scripted_triggers/COLDWAR_DDR_20261027_programmes.txt"
sys.path.insert(0,str(ROOT/"Claude outputs/COLDWAR_DDR_generator"));import dg_common
sys.path.insert(0,str(ROOT/"tools/german_reward_revision_20261027"));import programme_assets
sys.path.insert(0,str(ROOT/"tools"))
from building_grants.grants import repair_focus_tree, runtime_outputs as grant_runtime_outputs

def end_block(text,op):
    depth=0;quote=comment=escaped=False
    for i in range(op,len(text)):
        c=text[i]
        if comment:
            if c=="\n":comment=False
            continue
        if quote:
            if c=='"' and not escaped:quote=False
            escaped=c=="\\" and not escaped
            continue
        if c=="#":comment=True
        elif c=='"':quote=True
        elif c=="{":depth+=1
        elif c=="}":
            depth-=1
            if depth==0:return i+1
    raise ValueError("Unclosed Clausewitz block")

def focuses(text):
    out=[]
    for m in re.finditer(r"^\s*(?:focus|shared_focus|joint_focus)\s*=\s*\{",text,re.M):
        op=text.index("{",m.start());e=end_block(text,op);body=text[m.start():e]
        ident=re.search(r"^\s*id\s*=\s*([A-Za-z0-9_.]+)\s*$",body,re.M)
        if ident:out.append((ident.group(1),m.start(),e))
    return out

def field(text,name,required=True):
    m=re.search(r"\b"+re.escape(name)+r"\s*=\s*\{",text)
    if not m:
        if required:raise ValueError("Missing field "+name)
        return None
    op=text.index("{",m.start());e=end_block(text,op)
    return m.start(),e,text[op+1:e-1]

def set_field(text,name,content):
    f=field(text,name,False)
    replacement=f"{name} = {{\n\t\t\t{content.strip()}\n\t\t}}"
    if f:return text[:f[0]]+replacement+text[f[1]:]
    if name=="available":
        m=re.search(r"\bcompletion_reward\s*=\s*\{",text)
        if m:return text[:m.start()]+replacement+"\n\t\t"+text[m.start():]
    return text

def cost_text(value):
    s=f"{float(value):.5f}".rstrip("0").rstrip(".")
    if len(s.partition(".")[2])>5:raise ValueError("GDP cost has more than five decimals")
    return s

def loc_update(text,key,value):
    value=value.replace('"',"'").replace("\n"," ")
    line=f' {key}:0 "{value}"';pat=r'^\s*'+re.escape(key)+r':\d*\s*".*"\s*$'
    if re.search(pat,text,re.M):return re.sub(pat,lambda _:line,text,count=1,flags=re.M)
    return text.rstrip()+"\n"+line+"\n"

def validate_effects(fid,effects,dyn,tt):
    for e in effects:
        if e['type']!="dyn":continue
        group=e['group'];modifier=f"COLDWAR_DDR_{group}_modifier"
        if not re.search(r"^"+re.escape(modifier)+r"\s*=\s*\{",dyn,re.M):raise ValueError("Missing modifier group "+modifier)
        for key in e['mods']:
            pattern=r"^\s*"+re.escape(key)+r"\s*=\s*COLDWAR_DDR_"+re.escape(group)+r"_"+re.escape(key)+r"\s*$"
            if not re.search(pattern,dyn,re.M):raise ValueError("Unregistered modifier "+group+"."+key)
            tooltip=dg_common.mod_tt_key(key)
            if tooltip.startswith("COLDWAR_") and not re.search(r"^\s*"+re.escape(tooltip)+r":\d*\s+\"",tt,re.M):raise ValueError("Missing tooltip "+tooltip)

def effects_lines(fid,effects,dyn,tt,depth=0):
    p="\t"*depth;out=[]
    for index,e in enumerate(effects,1):
        if e['type']=="dyn":
            mod=f"COLDWAR_DDR_{e['group']}_modifier"
            out.append(p+f"custom_effect_tooltip = {{ localization_key = modifies_dynamic_modifier_tt MODIFIER = {mod} }}")
            for key,value in e['mods'].items():
                v=(f"{value:+.5f}".rstrip("0").rstrip(".") if value else "0").removeprefix("+")
                if len(v.partition(".")[2])>5:raise ValueError("Modifier value exceeds native precision")
                out.append(p+f"add_to_variable = {{ COLDWAR_DDR_{e['group']}_{key} = {v} tooltip = {dg_common.mod_tt_key(key)} }}")
            out.append(p+"newline = yes")
        elif e['type']=="tech":
            cats=" ".join("category = "+c for c in e['categories'])
            out.append(p+f"add_tech_bonus = {{ name = {fid}_reward_tech_{index} bonus = {e['bonus']} uses = {e['uses']} {cats} }}")
        elif e['type']=="doctrine":out.append(p+f"add_doctrine_cost_reduction = {{ name = {fid}_reward_doctrine_{index} category = {e['category']} uses = {e['uses']} cost_reduction = {e['bonus']} }}")
        elif e['type']=="equipment":
            fam=" ".join(f"{x} = {{ instant = yes build_cost_ic = {e['bonus']} }}" for x in e['families'])
            out.append(p+f"add_equipment_bonus = {{ name = {fid} bonus = {{ {fam} }} }}")
        else:raise ValueError("Unknown package effect: "+str(e))
    return out

def remove_project_nodes(body,helper_names):
    body=re.sub(r"(?m)^\s*set_temp_variable\s*=\s*\{\s*skip_payment\s*=\s*[01]\s*\}\s*\n?","",body)
    for helper in set(helper_names):body=re.sub(r"(?m)^\s*"+re.escape(helper)+r"\s*=\s*yes\s*\n?","",body)
    spans=[]
    for m in re.finditer(r"set_temp_variable\s*=\s*\{",body):
        op=body.index("{",m.start());stop=end_block(body,op);node=body[m.start():stop]
        if "treasury_change" in node and re.search(r"multiply\s*=\s*-\d",node):
            tail=body[stop:];mod=re.match(r"\s*modify_treasury_effect\s*=\s*yes",tail)
            spans.append((m.start(),stop+(mod.end() if mod else 0)))
    for a,b in reversed(spans):body=body[:a]+body[b:]
    return body

def preview_safe(body):
    body=re.sub(r"(?m)^\s*log\s*=.*\n?","",body)
    # Remove complete hidden blocks with balanced braces, including nested effects.
    while True:
        m=re.search(r"hidden_effect\s*=\s*\{",body)
        if not m:break
        op=body.index("{",m.start());e=end_block(body,op)
        body=body[:m.start()]+body[e:]
    return body.strip()

def replace_modifier(body,group,key,value):
    var=f"COLDWAR_DDR_{group}_{key}"
    return re.sub(r"(?m)^\s*add_to_variable\s*=\s*\{\s*"+re.escape(var)+r"\s*=\s*"+re.escape(str(value))+r"\s+tooltip\s*=\s*[^}]+\}\s*\n?","",body)

def run_overlay():
    data=json.loads(OVERLAY.read_text(encoding="utf-8"))
    if data.get("project")!="IMPERIA COLD WAR":raise ValueError("Canonical overlay project id missing")
    text=TREE.read_text(encoding="utf-8-sig");old_count=len(focuses(text));loc=LOC.read_text(encoding="utf-8-sig")
    dyn=DYN.read_text(encoding="utf-8-sig");tt=TT.read_text(encoding="utf-8-sig")
    for item in data['foci']+data['transactions']:
        fid="COLDWAR_DDR_"+item['id']
        for index,effect in enumerate(item.get('effects',[]),1):
            if effect['type'] in ('tech','doctrine'):
                loc=loc_update(loc,f"{fid}_reward_{effect['type']}_{index}",f"${fid}$")
    effect_defs=[];trigger_defs=[]
    route_guard="original_tag = DDR\ntag = DDR\nIMP_is_1970_scenario = yes"
    hidden_route="hidden_trigger = { original_tag = DDR tag = DDR IMP_is_1970_scenario = yes }"
    # Static policy and military supplements. Base reward and availability are
    # frozen in the canonical record, so rebuilds never consume their own output.
    for item in data['foci']:
        fid="COLDWAR_DDR_"+item['id'];row=[x for x in focuses(text) if x[0]==fid]
        if len(row)!=1:raise ValueError("Expected one focus "+fid)
        _,s,e=row[0];block=text[s:e];reward=item['base_reward'];available=item.get('base_available','')
        for rm in item.get('remove_modifiers',[]):reward=replace_modifier(reward,rm['group'],rm['key'],rm['value'])
        validate_effects(fid,item['effects'],dyn,tt)
        receipt="COLDWAR_DDR_R_20261027_"+item['id'];trigger="COLDWAR_DDR_20261027_static_can_"+item['id'];effect="COLDWAR_DDR_20261027_static_run_"+item['id']
        trigger_defs.append(trigger+" = {\n"+route_guard+"\n"+available+"\n}")
        runtime=[effect+" = {","\tif = {",f"\t\tlimit = {{ {trigger} = yes NOT = {{ has_country_flag = {receipt} }} }}"]
        runtime+=effects_lines(fid,item['effects'],dyn,tt,2);runtime += [f"\t\tset_country_flag = {receipt}","\t}","}"]
        effect_defs.extend(runtime)
        preview="\n".join(effects_lines(fid,item['effects'],dyn,tt,3))
        reward=reward.rstrip()+f"\n\t\teffect_tooltip = {{\n{preview}\n\t\t}}\n\t\thidden_effect = {{ {effect} = yes }}\n\t"
        block=set_field(block,"completion_reward",reward)
        # Restore canonical availability, preserving visibility of all party branches.
        block=set_field(block,"available",available+"\n"+hidden_route+"\n")
        text=text[:s]+block+text[e:]
        loc=loc_update(loc,fid+"_desc",item['desc'])
    # Paid transactions: original and new project effects share a single runtime guard.
    for tx in data['transactions']:
        fid="COLDWAR_DDR_"+tx['id'];row=[x for x in focuses(text) if x[0]==fid]
        if len(row)!=1:raise ValueError("Expected one focus "+fid)
        _,s,e=row[0];block=text[s:e]
        base=tx['base_reward'];available=tx['base_available']
        helpers=[x['effect'] for x in tx.get('legacy_building_helpers',[])]
        residual=remove_project_nodes(base,helpers)
        buildings=tx['buildings'];can=programme_assets.bundle_guards(buildings)
        trigger="COLDWAR_DDR_20261027_can_"+tx['id'];effect="COLDWAR_DDR_20261027_run_"+tx['id'];receipt="COLDWAR_DDR_R_20261027_"+tx['id']
        trigger_body=route_guard+"\n"+available+"\ncheck_variable = { gdp_total > 0 }\n"+can
        trigger_defs.append(trigger+" = {\n"+trigger_body+"\n}")
        validate_effects(fid,tx.get('effects',[]),dyn,tt)
        price=cost_text(tx['cost_fraction'])
        runtime=[effect+" = {","\tif = {",f"\t\tlimit = {{ {trigger} = yes NOT = {{ has_country_flag = {receipt} }} }}",f"\t\tset_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{price} }} }}","\t\tmodify_treasury_effect = yes"]
        cleaned=residual.strip()
        if cleaned:runtime += ["\t\t"+cleaned.replace("\n","\n\t\t")]
        runtime += ["\t\t"+programme_assets.bundle_effects(buildings).replace("\n","\n\t\t")]
        runtime += effects_lines(fid,tx.get('effects',[]),dyn,tt,2)
        runtime += [f"\t\tset_country_flag = {receipt}","\t}","}"]
        effect_defs.extend(runtime)
        preview=[f"\t\t\tset_temp_variable = {{ treasury_change = {{ value = gdp_total multiply = -{price} }} }}","\t\t\tmodify_treasury_effect = yes"]
        safe=preview_safe(residual)
        if safe:preview.append("\t\t\t"+safe.replace("\n","\n\t\t\t"))
        preview.append("\t\t\t"+programme_assets.bundle_effects(buildings).replace("\n","\n\t\t\t"))
        preview += effects_lines(fid,tx.get('effects',[]),dyn,tt,3)
        reward="\n\t\teffect_tooltip = {\n"+"\n".join(preview)+f"\n\t\t}}\n\t\thidden_effect = {{ {effect} = yes }}\n\t"
        block=set_field(block,"completion_reward",reward)
        block=set_field(block,"available",available+"\n"+hidden_route+"\ncheck_variable = { gdp_total > 0 }\n"+can)
        text=text[:s]+block+text[e:]
        loc=loc_update(loc,fid+"_desc",tx['desc'])
    if len(focuses(text))!=old_count:raise ValueError("Focus count changed")
    ids=[x[0] for x in focuses(text)]
    if len(set(ids))!=len(ids):raise ValueError("Duplicate focus ids")
    OUT_EFFECT.parent.mkdir(parents=True,exist_ok=True);OUT_TRIGGER.parent.mkdir(parents=True,exist_ok=True)
    # Parse every complete output and validate top-level keys before touching any file.
    sys.path.insert(0,str(ROOT/"tools/vietnam_1970"));from script_ast import parse,first
    effects_text="# IMPERIA COLD WAR — DDR paid programme transactions 2026-10-27.\n"+"\n".join(effect_defs)+"\n"
    triggers_text="# IMPERIA COLD WAR — DDR paid programme availability 2026-10-27.\n"+"\n".join(trigger_defs)+"\n"
    # Retain both the new paid recipes and the physical-capacity transaction layer.
    text=repair_focus_tree('DDR',text,external_triggers=triggers_text)
    owned={"COLDWAR_DDR_"+item['id'] for item in data['foci']+data['transactions']}
    for fid,start,end in reversed(focuses(text)):
        if fid in owned:
            text=text[:start]+re.sub(r"(?m)[ \t]+$","",text[start:end])+text[end:]
    focus_ast=parse(text);effects_ast=parse(effects_text);triggers_ast=parse(triggers_text)
    def keys(ast):return [k for k,op,value in ast if k!="_bare"]
    if len(keys(effects_ast))!=len(set(keys(effects_ast))):raise ValueError("Duplicate scripted-effect key")
    if len(keys(triggers_ast))!=len(set(keys(triggers_ast))):raise ValueError("Duplicate scripted-trigger key")
    ids=[]
    def scan_focus(ast):
        for k,op,value in ast:
            if k in ("focus","shared_focus","joint_focus") and isinstance(value,list):
                found=first(value,"id")
                if found:ids.append(found)
            if isinstance(value,list):scan_focus(value)
    scan_focus(focus_ast)
    if len(ids)!=old_count or len(set(ids))!=old_count:raise ValueError("Parsed focus graph differs from 836 unique nodes")
    for name,body in zip(keys(triggers_ast),[v for k,o,v in triggers_ast if k!="_bare"]):
        if name in str(body):raise ValueError("Self-recursive trigger "+name)
    plan={TREE:text.encode("utf-8"),LOC:loc.encode("utf-8-sig"),OUT_EFFECT:effects_text.encode("utf-8"),OUT_TRIGGER:triggers_text.encode("utf-8")}
    plan.update({ROOT/relative:payload.encode('utf-8-sig' if relative.endswith('.yml') else 'utf-8')
                 for relative,payload in grant_runtime_outputs().items()})
    staged=[]
    try:
        for path,content in plan.items():
            with tempfile.NamedTemporaryFile(prefix=path.name+".",suffix=".tmp",dir=path.parent,delete=False) as handle:
                handle.write(content);staged.append((path,Path(handle.name)))
        for path,temp in staged:os.replace(temp,path)
    finally:
        for path,temp in staged:
            if temp.exists():temp.unlink()
    return {"project":"IMPERIA COLD WAR","focus_count":old_count,"static_rewards":len(data['foci']),"paid_programmes":len(data['transactions']),"outputs":[str(path.relative_to(ROOT)) for path in plan]}
apply_overlay = run_overlay
if __name__=="__main__":print(json.dumps(run_overlay(),indent=2))
