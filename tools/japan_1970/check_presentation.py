# IMPERIA COLD WAR — Cold War: Japan presentation regressions and gameplay preservation.
"""Bounded static QA; native connector routing and hover still need the engine."""
import json
from collections import Counter
from pathlib import Path
from PIL import ImageFont
from check_script_grammar import Entry, parse
from presentation import read_focuses, semantic, field
from layout import CONTINUOUS_POSITION
from reward_revision import effective_inventory, effective_party_map
from generate_staged_effects import state_building_guard, FOCUS_GUARDS
import re

ROOT = Path(__file__).resolve().parent
STAGE = ROOT / 'staging/graph'
BEFORE_POLISH = Path(r'E:\HOI4_Mod_Tools\mdcoldwar\runtime\quaza_eastasia_20261027\donor\tools\japan_1970\staging\graph\before_polish_focus_tree.txt')
BASE_INVENTORY = json.loads((ROOT / 'effect_inventory.json').read_text(encoding='utf-8'))
OLD_REWARDS = {record['id']: record for record in BASE_INVENTORY}
CURRENT_REWARDS = effective_inventory(BASE_INVENTORY)
BASE_PARTY = json.loads((ROOT / 'party_map.json').read_text(encoding='utf-8'))
OLD_PARTY = BASE_PARTY['focus_helpers']
CURRENT_PARTY = effective_party_map(BASE_PARTY)['focus_helpers']

# Verified native MD party triggers in common/scripted_triggers/01_political_triggers.txt.
PARTY_TRIGGER_SLOTS = {
    'western_conservatism_are_in_power': '1',
    'western_liberals_are_in_power': '2',
    'western_social_democrats_are_in_power': '3',
    'emerging_communist_state_are_in_power': '4',
    'neutrality_neutral_conservatism_are_in_power': '14',
}
LEGACY_PARTY_TOOLTIP_SLOTS = {
    'COLDWAR_JAP_1970_governing_LDP': '1',
    'COLDWAR_JAP_1970_governing_DSP': '2',
    'COLDWAR_JAP_1970_governing_JSP': '3',
    'COLDWAR_JAP_1970_governing_JCP': '4',
    'COLDWAR_JAP_1970_governing_Komeito': '14',
}


def intersects(a,b,box):
    """Open interior segment/rectangle overlap, using a Liang–Barsky clip."""
    lo,hi=0.,1.
    x0,y0,x1,y1=box
    for p,q in ((-(b[0]-a[0]),a[0]-x0), (b[0]-a[0],x1-a[0]),
                (-(b[1]-a[1]),a[1]-y0), (b[1]-a[1],y1-a[1])):
        if p==0:
            if q<=0:return False
        elif p<0:lo=max(lo,q/p)
        else:hi=min(hi,q/p)
    return lo<hi and hi>0 and lo<1


def normalize_party_gates(entries):
    """Compare legacy tooltip-wrapped exact slots with their native MD triggers."""
    result = []
    for node in entries:
        if node.key == 'custom_trigger_tooltip' and isinstance(node.value, list):
            tooltip = field(node.value, 'tooltip')
            check = field(node.value, 'check_variable')
            ruling_party = field(check, 'ruling_party') if isinstance(check, list) else None
            slot = LEGACY_PARTY_TOOLTIP_SLOTS.get(tooltip)
            if (slot is not None and ruling_party == slot and
                    len(node.value) == 2 and isinstance(check, list) and len(check) == 1):
                result.append(Entry('__japan_exact_party_gate__', '=', slot, node.line))
                continue
        if (node.key in PARTY_TRIGGER_SLOTS and node.operator == '=' and node.value == 'yes'):
            result.append(Entry('__japan_exact_party_gate__', '=', PARTY_TRIGGER_SLOTS[node.key], node.line))
            continue
        if isinstance(node.value, list):
            result.append(Entry(node.key, node.operator, normalize_party_gates(node.value), node.line))
        else:
            result.append(node)
    return result


def _number(entries, key, default=None):
    value = field(entries, key, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def reward_guarantees_slot(reward, state_id, building, required_slots):
    """Require the preview to show enough guaranteed slots before this building."""
    previews = [node.value for node in reward if node.key == 'effect_tooltip' and isinstance(node.value, list)]
    for preview in previews:
        for state in preview:
            if state.key != state_id or not isinstance(state.value, list):
                continue
            slots = 0
            for node in state.value:
                if node.key == 'add_extra_state_shared_building_slots':
                    try:
                        amount = int(node.value)
                    except (TypeError, ValueError):
                        amount = None
                    if amount is not None:
                        slots += amount
                elif node.key == 'add_building_construction' and isinstance(node.value, list):
                    if field(node.value, 'type') == building:
                        level = _number(node.value, 'level')
                        if level is not None and slots >= max(required_slots, level):
                            return True
    return False


def normalize_superseded_free_slot_checks(old_entries, current_entries, reward):
    """Drop only an old preview/availability slot check covered by its granted slot."""
    removed = 0
    current_state_ids = {
        node.key for node in current_entries
        if node.key.isdigit() and isinstance(node.value, list)
    }

    def visit(nodes, state_id=None):
        nonlocal removed
        result = []
        for node in nodes:
            if node.key == 'free_building_slots' and isinstance(node.value, list) and state_id:
                building = field(node.value, 'building')
                size = field(node.value, 'size')
                required = (int(size) + 1 if field(node.value, 'size') is not None and
                            next((n.operator for n in node.value if n.key == 'size'), None) == '>'
                            else _number(node.value, 'size'))
                if (state_id in current_state_ids and building and required is not None and
                        reward_guarantees_slot(reward, state_id, building, required)):
                    removed += 1
                    continue
            if isinstance(node.value, list):
                nested_state = node.key if node.key.isdigit() else state_id
                result.append(Entry(node.key, node.operator, visit(node.value, nested_state), node.line))
            else:
                result.append(node)
        return result

    return visit(old_entries), removed


def is_positive_gdp_guard(entry):
    if entry.key != 'hidden_trigger' or not isinstance(entry.value, list) or len(entry.value) != 1:
        return False
    check = entry.value[0]
    if check.key != 'check_variable' or not isinstance(check.value, list) or len(check.value) != 1:
        return False
    variable = check.value[0]
    return variable.key == 'gdp_total' and variable.operator == '>' and variable.value == '0'


def normalize_gdp_cost_guard(entries, focus_id, reward_record):
    expected = bool(reward_record and (reward_record.get('cost_gdp_share', 0) or any(
        reward.get('type') == 'treasury_gdp_share' and reward.get('share', 0)
        for reward in reward_record.get('one_time_effects', []))))
    matches = [index for index, entry in enumerate(entries) if is_positive_gdp_guard(entry)]
    if len(matches) != int(expected):
        return entries, f'{focus_id}: expected {int(expected)} positive-GDP availability guard(s), found {len(matches)}'
    if expected:
        entries = [entry for index, entry in enumerate(entries) if index != matches[0]]
    return entries, None


def parsed_state_guard(state_id, building, level, awarded_slots, include_technology=True):
    text = state_building_guard(state_id, building, level, awarded_slots, include_technology)
    return field(parse('available = { ' + text + ' }')[0].value, str(state_id))


def asset_rows(record):
    if not record:
        return []
    if 'buildings' in record:
        return record.get('buildings', [])
    return [(reward['state_id'], reward['building'], int(reward['level']), int(reward['level']))
            for reward in record.get('one_time_effects', []) if reward.get('type') == 'building']


def normalize_overlay_asset_guards(old_available, current_available, focus_id, old_record, current_record):
    """Remove only state guards that exactly match recorded old/new building grants."""
    old_available = list(old_available or [])
    current_available = list(current_available or [])
    errors = []
    old_assets = asset_rows(old_record)
    current_assets = asset_rows(current_record)

    for state_id, building, level, awarded_slots in old_assets:
        expected = parsed_state_guard(state_id, building, level, awarded_slots, False)
        match = next((index for index, entry in enumerate(old_available)
                      if entry.key == str(state_id) and semantic(entry.value) == semantic(expected)), None)
        if match is not None:
            old_available.pop(match)

    for state_id, building, level, _recorded_slots in current_assets:
        expected = parsed_state_guard(state_id, building, level, level)
        match = next((index for index, entry in enumerate(current_available)
                      if entry.key == str(state_id) and semantic(entry.value) == semantic(expected)), None)
        if match is None:
            errors.append(f'{focus_id}: missing capacity/ownership guard matching new {building} x{level} grant in state {state_id}')
        else:
            current_available.pop(match)
    return old_available, current_available, errors


def preview_assets_match(focus_id, reward, reward_record):
    """Require the displayed new building grants and shared slots to match the overlay."""
    previews = [entry.value for entry in reward or []
                if entry.key == 'effect_tooltip' and isinstance(entry.value, list)]
    if len(previews) != 1:
        return f'{focus_id}: expected one native asset preview, found {len(previews)}'
    expected = asset_rows(reward_record)
    actual_buildings = []
    actual_slots = Counter()
    errors = []
    for state in previews[0]:
        if not state.key.isdigit() or not isinstance(state.value, list):
            continue
        pending_slots = 0
        for entry in state.value:
            if entry.key == 'add_extra_state_shared_building_slots':
                try:
                    pending_slots += int(entry.value)
                except (TypeError, ValueError):
                    errors.append(f'{focus_id}: invalid shared-slot quantity in state {state.key}')
            elif entry.key == 'add_building_construction' and isinstance(entry.value, list):
                building = field(entry.value, 'type')
                try:
                    level = int(field(entry.value, 'level'))
                except (TypeError, ValueError):
                    level = 0
                if pending_slots < level:
                    errors.append(f'{focus_id}: {building} x{level} in state {state.key} lacks preceding extra shared slots')
                else:
                    pending_slots -= level
                actual_buildings.append((int(state.key), building, level))
        actual_slots[int(state.key)] += sum(int(entry.value) for entry in state.value
                                            if entry.key == 'add_extra_state_shared_building_slots'
                                            and str(entry.value).lstrip('-').isdigit())
    expected_buildings = sorted((int(state_id), building, int(level))
                                for state_id, building, level, _ in expected)
    if sorted(actual_buildings) != expected_buildings:
        errors.append(f'{focus_id}: preview building grants do not match the effective inventory')
    expected_slots = Counter()
    for state_id, _building, level, _ in expected:
        expected_slots[int(state_id)] += int(level)
    if actual_slots != expected_slots:
        errors.append(f'{focus_id}: preview extra shared slots do not match the effective inventory')
    return '; '.join(errors) if errors else None


def main():
    errors=[]
    if not BEFORE_POLISH.is_file():
        raise FileNotFoundError('Archived pre-polish approval baseline is missing: ' + str(BEFORE_POLISH))
    before=read_focuses(BEFORE_POLISH.read_text(encoding='utf-8'))
    current=read_focuses((STAGE/'focus_tree.txt').read_text(encoding='utf-8'))
    if before.keys()!=current.keys(): errors.append('Focus IDs changed')
    party_gate_equivalences=0
    gdp_guard_equivalences=0
    asset_guard_equivalences=0
    asset_preview_checks=0
    for ident,n in current.items():
        old=before[ident]
        old_entries=normalize_party_gates(old['entries'])
        current_entries=normalize_party_gates(n['entries'])
        old_available=field(old_entries,'available')
        current_available=field(current_entries,'available')
        reward=field(n['entries'],'completion_reward')
        short_id=ident.removeprefix('COLDWAR_JAP_1970_')
        old_record=OLD_REWARDS.get(short_id,OLD_PARTY.get(short_id))
        current_record=CURRENT_REWARDS.get(short_id,CURRENT_PARTY.get(short_id))
        current_available,gdp_error=normalize_gdp_cost_guard(current_available,ident,current_record)
        if gdp_error:
            errors.append(gdp_error)
        elif current_record and (
            current_record.get('cost_gdp_share',0)
            or any(reward.get('type') == 'treasury_gdp_share'
                   for reward in current_record.get('one_time_effects', []))
        ):
            gdp_guard_equivalences+=1
        old_available,current_available,asset_errors=normalize_overlay_asset_guards(
            old_available,current_available,ident,old_record,current_record)
        if short_id == 'microelectronics_capacity':
            # The user requires technology for the full two-level package.
            # Normalize only this explicit replacement of the old tier-1 gate.
            old_chip = parse('has_tech = microchip_production_1')[0]
            new_chip = parse(FOCUS_GUARDS[short_id][0])[0]
            for entries, expected in ((old_available, old_chip), (current_available, new_chip)):
                match = next((i for i, entry in enumerate(entries)
                              if semantic([entry]) == semantic([expected])), None)
                if match is None:
                    asset_errors.append(ident + ': missing expected old/new microchip technology gate')
                else:
                    entries.pop(match)
        errors.extend(asset_errors)
        asset_guard_equivalences+=len(asset_rows(old_record))+len(asset_rows(current_record))
        if (short_id in CURRENT_REWARDS or asset_rows(current_record)):
            asset_preview_checks+=1
            asset_error=preview_assets_match(ident,reward,current_record)
            if asset_error:
                errors.append(asset_error)
        party_gate_equivalences+=sum(
            1 for e in old_available or [] if e.key=='__japan_exact_party_gate__')
        old_entries=[Entry(e.key,e.operator,old_available if e.key=='available' else e.value,e.line)
                     if e.key=='available' else e for e in old_entries]
        current_entries=[Entry(e.key,e.operator,current_available if e.key=='available' else e.value,e.line)
                         if e.key=='available' else e for e in current_entries]
        if semantic(old_entries,('x','y','relative_position_id','completion_reward','icon')) != semantic(current_entries,('x','y','relative_position_id','completion_reward','icon')):
            errors.append(ident+': gameplay/gates changed outside authorized GDP or asset-capacity overlays')
        for data in (old,n):
            reward=field(data['entries'],'completion_reward')
            data['payout']=semantic([e for e in reward if e.key=='hidden_effect'])
        if old['payout']!=n['payout']:errors.append(ident+': guarded payout changed')
    boxes={k:(n['globalX']*96-82.5,n['globalY']*130,n['globalX']*96+82.5,n['globalY']*130+128) for k,n in current.items()}
    keys=list(current)
    for i,k in enumerate(keys):
        a=boxes[k]
        for other in keys[i+1:]:
            b=boxes[other]
            if max(a[0],b[0])<min(a[2],b[2]) and max(a[1],b[1])<min(a[3],b[3]):
                errors.append(f'Card overlap: {k} / {other}')
    exclusive=[]
    for k,n in current.items():
        x,y=n['globalX']*96,n['globalY']*130
        for other in n['exclusive']:
            if other<k:continue
            o=current[other]; ox,oy=o['globalX']*96,o['globalY']*130
            if y!=oy:errors.append('Uneven exclusive row: '+k)
            a,b=(min(x,ox)+83,y+68),(max(x,ox)-83,y+68)
            exclusive.append((k,other,a,b))
            for third,box in boxes.items():
                if third not in (k,other) and intersects(a,b,box):errors.append(f'Exclusion crosses card: {k} / {other} through {third}')
    # Straight center routes are a conservative diagnostic, not the engine path.
    for k,n in current.items():
        b=(n['globalX']*96,n['globalY']*130)
        for group in n['parents']:
            for parent in group:
                p=current[parent];a=(p['globalX']*96,p['globalY']*130+128)
                if p['globalY']>=n['globalY']:errors.append('Backward prerequisite: '+k)
                for third,box in boxes.items():
                    if third not in (k,parent) and intersects(a,b,box):errors.append(f'Prerequisite crosses card: {parent} -> {k} through {third}')
                for left,right,e1,e2 in exclusive:
                    if k in (left,right) or parent in (left,right):continue
                    if a[1]<e1[1]<b[1]:
                        t=(e1[1]-a[1])/(b[1]-a[1]); x=a[0]+t*(b[0]-a[0])
                        if e1[0]<x<e2[0]:errors.append(f'Prerequisite crosses exclusion: {parent} -> {k}')
    px,py=CONTINUOUS_POSITION
    panel=(px,py,px+770,py+380)
    for ident,box in boxes.items():
        if max(box[0],panel[0])<min(box[2],panel[2]) and max(box[1],panel[1])<min(box[3],panel[3]):errors.append('Continuous panel covers '+ident)
    loc=dict(re.findall(r'(?m)^\s*(\w+):\s*"([^"\n]*)"',(STAGE/'focus_l_english.yml').read_text(encoding='utf-8-sig')))
    font=ImageFont.truetype('C:/Windows/Fonts/arial.ttf',14)
    for ident in current:
        if font.getlength(loc[ident])>147:errors.append('Title exceeds approximate 147px name field: '+ident)
    manifest=json.loads((STAGE/'presentation_manifest.json').read_text(encoding='utf-8'))
    import hashlib
    if manifest['focus_sha256']!=hashlib.sha256((STAGE/'focus_tree.txt').read_bytes()).hexdigest():errors.append('Preview is stale')
    print(f'Presentation: {len(current)} focuses; normalized {party_gate_equivalences} exact party-gate presentations, {gdp_guard_equivalences} GDP guards, {asset_guard_equivalences} old/new asset guards; checked {asset_preview_checks} inventory previews against their building and slot records; protected payouts, cards, exclusions, routes, panel and titles; {len(errors)} findings')
    for error in errors:print('ERROR:',error)
    return bool(errors)


if __name__=='__main__':raise SystemExit(main())
