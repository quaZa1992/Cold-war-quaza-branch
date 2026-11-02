# IMPERIA COLD WAR — faithful generic naval preview data
"""Build native-style preview records for the copied MD naval focus block."""
from __future__ import annotations

import base64
import io
import sys
from pathlib import Path

from generic_navy import ID_MAP, ROOT_POSITIONS, SOURCE, resolved
from script_ast import first

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

LABELS = {
    'military_factories_productivity': 'Military factory productivity',
    'dockyard_productivity': 'Dockyard productivity',
    'military_industry_tax_modifier': 'Military industry tax income',
    'dockyard_income_tax_modifier': 'Dockyard tax income',
    'repair_speed_factor': 'Ship repair speed',
    'industrial_capacity_dockyard': 'Dockyard production output',
    'equipment_conversion_speed': 'Equipment conversion speed',
    'industrial_capacity_factory': 'Factory production output',
    'experience_gain_navy_factor': 'Navy experience gain',
    'amphibious_invasion': 'Amphibious invasion speed',
    'extra_marine_supply_grace': 'Marine supply grace hours',
    'marines_special_forces_contribution_factor': 'Marine special forces capacity contribution',
}

BUILDING_ROWS = {
    'COLDWAR_CUB_GEN_light_industry_investments': [
        'CUB: Treasury -$7.50 billion', 'Capital: +2 building slots',
        'Capital: +1 Civilian Factory, instant', 'Capital: +1 Fossil Power Plant, queued'],
    'COLDWAR_CUB_GEN_heavy_industry_investments': [
        'CUB: Treasury -$7.50 billion', 'Capital: +1 building slot',
        'Capital: +1 Arms Factory, instant',
        'If total factories are 21 to 44: +1 random Arms Factory and +1 slot; Treasury -$7.50 billion',
        'If total factories are 45 or more: up to +2 random Arms Factories in eligible states, with +1 slot each; Treasury -$15.00 billion',
        'If Defense Industry is active: Opinion +5'],
    'COLDWAR_CUB_GEN_refitting_the_military_industry': [
        'CUB: Treasury -$7.50 billion', 'Capital: +1 building slot',
        'Capital: +1 Arms Factory, instant',
        'If total factories are 21 to 44: +1 random Arms Factory and +1 slot; Treasury -$7.50 billion',
        'If total factories are 45 or more: up to +2 random Arms Factories in eligible states, with +1 slot each; Treasury -$15.00 billion',
        'If Defense Industry is active: Opinion +5'],
}


def _as_num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _requirements(rows):
    if not rows:
        return []
    out = []
    for key, op, val in rows:
        if key == 'if':
            limit = first(val, 'limit') or []
            is_ai = first(limit, 'is_ai')
            if is_ai == 'no':
                out.append('At peace when selected by a human player; AI requires an interest rate below 15%')
            else:
                out.append('Conditional availability')
            continue
        if key == 'else':
            continue
        if key == 'controls_a_coastal_state':
            out.append('Controls a coastal state')
        elif key == 'num_of_naval_factories':
            n = int(val)
            out.append(f'At least {n + 1} naval factories' if op == '>' else f'At most {n} naval factories')
        elif key == 'num_of_military_factories':
            n = int(val)
            out.append(f'At least {n + 1} military factories' if op == '>' else f'At most {n} military factories')
        elif key == 'num_of_factories':
            n = int(val)
            out.append(f'At least {n + 1} total factories' if op == '>' else f'At most {n} total factories')
        elif key == 'gdp_total_greater_than_95':
            out.append('Total GDP above 95')
        elif key == 'gdp_total_greater_than_150':
            out.append('Total GDP above 150')
        elif key == 'gdp_total_greater_than_200':
            out.append('Total GDP above 200')
        elif key == 'has_war' and val == 'no':
            out.append('At peace')
        elif key == 'has_selected_naval_grand_doctrine':
            out.append('A Naval Grand Doctrine is selected')
        elif key == 'is_special_project_completed':
            labels = {
                'sp:sp_naval_vessel_project': 'Naval Vessel Project is complete',
                'sp:sp_composite_production': 'Composite Production Project is complete',
            }
            out.append(labels.get(val, f'Special project is complete: {val}'))
        elif key == 'has_at_least_major_power_status':
            out.append('At least Major Power status')
        elif key == 'has_at_least_regional_power_status':
            out.append('At least Regional Power status')
    return list(dict.fromkeys(out))


def _effect_rows(fid, source_rows):
    rows = list(BUILDING_ROWS.get(fid, []))
    table = {
        'COLDWAR_CUB_GEN_military_industry_investment_projects': [
            'Military Industry Project for 730 days: +2% Military Factory Productivity; +5% Arms Factory Production Speed',
            'If incomplete: +15% Composite Production Project progress'],
        'COLDWAR_CUB_GEN_naval_reform': [
            'CUB: +75 Navy Experience', 'If a Naval Grand Doctrine is selected: +30 naval doctrine mastery',
            'If incomplete: +15% Naval Vessel Project progress', 'If Maritime Industry is active: Opinion +10'],
        'COLDWAR_CUB_GEN_combined_military_defense_industries': [
            'Combined Defense Industries: +10% Military Factory Productivity; +10% Dockyard Productivity',
            '+10% Military Industry Tax Income; +10% Dockyard Tax Income',
            'If Defense Industry is active: Opinion +5', 'If Maritime Industry is active: Opinion +5',
            'One random Arms Factory and +1 building slot; no treasury charge'],
        'COLDWAR_CUB_GEN_naval_bases': [
            'A controlled state with naval-base capacity: +1 building slot and +1 Naval Base',
            'CUB: Treasury -$0.50 billion', 'If Maritime Industry is active: Opinion +5'],
        'COLDWAR_CUB_GEN_submarines': ['+50% Submarine research bonus, 2 uses'],
        'COLDWAR_CUB_GEN_surface_ships': ['+50% Surface Ship research bonus, 2 uses'],
        'COLDWAR_CUB_GEN_dockyards': [
            'If total factories are below 15: +1 random Dockyard and +1 building slot; Treasury -$7.50 billion',
            'If total factories are 15 or more: up to +2 random Dockyards in eligible states, with +1 slot each; Treasury -$15.00 billion',
            'If Maritime Industry is active: Opinion +5'],
        'COLDWAR_CUB_GEN_nuclear_submarines': [
            '+50% Submarine research bonus, 2 uses',
            'If owned: +50 mastery for Escort Attack Subs, Hunter-Killer Subs and Missile Boats'],
        'COLDWAR_CUB_GEN_naval_doctrine_innovations': [
            'CUB: +50 Navy Experience', '+50 Naval Doctrine mastery'],
        'COLDWAR_CUB_GEN_aircraft_carriers': ['+50% Aircraft Carrier research bonus, 2 uses'],
        'COLDWAR_CUB_GEN_light_helicopter_operators': ['+50% Helicopter Operator research bonus, 2 uses'],
        'COLDWAR_CUB_GEN_large_ship_drydocks': [
            'One random Dockyard and +1 building slot; Treasury -$7.50 billion'],
        'COLDWAR_CUB_GEN_improved_repair_facilities': [
            'Dockyard Repair Focus for 365 days: +25% Ship Repair Speed'],
        'COLDWAR_CUB_GEN_vessel_production': [
            'Naval Production Bonus for 730 days: +20% Dockyard Production Output',
            'If Maritime Industry is active: Opinion +5'],
        'COLDWAR_CUB_GEN_composite_industrial_expansion': [
            'If a controlled state has a free slot: +1 Composite Plant and +1 building slot',
            'CUB: Treasury -$8.50 billion'],
        'COLDWAR_CUB_GEN_weapon_conversion_packages': [
            'Equipment Conversion Efforts for 730 days: +15% Equipment Conversion Speed; +15% Factory Production Output'],
        'COLDWAR_CUB_GEN_naval_doctrine_expertise': [
            'CUB: +25 Navy Experience', '+50 Naval Doctrine mastery'],
        'COLDWAR_CUB_GEN_convoy_and_freighter_production': [
            'Convoy Production Focus: -15% Convoy Equipment Production Cost'],
        'COLDWAR_CUB_GEN_establish_a_marine_corps': [
            'Establish a Marine Corps: +5% Navy Experience Gain; +15% Amphibious Invasion Speed',
            '+48 hours Marine Supply Grace; -5% Marine Special Forces Capacity Contribution'],
        'COLDWAR_CUB_GEN_submarine_expansion_project': [
            '+50% Submarine research bonus, 2 uses',
            'If owned: +50 mastery for Escort Attack Subs, Hunter-Killer Subs and Missile Boats'],
        'COLDWAR_CUB_GEN_stealth_ships': [
            'If incomplete: +10% progress each toward Stealth Corvette, Stealth Frigate and Stealth Destroyer projects'],
        'COLDWAR_CUB_GEN_air_force_reform': [
            'CUB: +50 Air Experience', '+25% Aircraft research bonus, 1 use', '+25 Air Doctrine mastery',
            'If incomplete: +10% Aircraft Project progress'],
        'COLDWAR_CUB_GEN_fighter_planes': ['+50% Aircraft research bonus, 2 uses'],
    }
    rows += table.get(fid, [])
    if not rows:
        raise ValueError(f'No numeric preview mapping for donor focus {fid}')
    return rows


def build_nodes():
    from script_ast import parse
    positions = resolved()
    loc = SOURCE['localisation']
    nodes, art_additions = [], {}
    for record in SOURCE['focuses']:
        fid = record['id']
        rows = parse(record['script'])
        new_id = ID_MAP[fid]
        key = new_id.removeprefix('COLDWAR_CUB_GEN_')
        title = loc[fid]
        description = loc[fid + '_desc']
        icon = first(rows, 'icon')
        prereqs = []
        for _, _, group in [r for r in rows if r[0] == 'prerequisite']:
            ids = [ID_MAP[f] for k, _, f in group if k == 'focus' and f in ID_MAP]
            if ids:
                prereqs.append(ids)
        excludes = []
        for _, _, group in [r for r in rows if r[0] == 'mutually_exclusive']:
            excludes.extend(ID_MAP[f] for k, _, f in group if k == 'focus' and f in ID_MAP)
        cost = _as_num(first(rows, 'cost')) or 10
        xy = list(positions[new_id])
        requirements = _requirements(first(rows, 'available'))
        node = dict(
            id=new_id, key=key, title=title, native_title=title,
            group='naval' if fid in SOURCE['naval_ids'] else 'navy_feeders',
            xy=xy, local_xy=[int(first(rows, 'x')), int(first(rows, 'y'))] if first(rows, 'relative_position_id') else list(xy),
            anchor=ID_MAP.get(first(rows, 'relative_position_id')), cost=cost,
            days=round(cost*7), description=description, modifiers={}, effects=[],
            prerequisites=prereqs, mutually_exclusive=excludes, slot=None,
            extra_gate='', icon=icon, historical_status='Native Millennium Dawn generic naval focus and feeder, copied at user request.',
            lifetime='', reference='Installed Millennium Dawn generic naval tree; donor wording and mechanics preserved.',
            title_width=None, title_art=None,
            effect_rows=[],
            requirements=requirements, guards=[], partner=None, is_existing=False,
            title_wrapped=False, source_focus_id=fid)
        node['title_width'] = None
        node['effect_rows'] = _effect_rows(new_id, first(rows, 'completion_reward'))
        nodes.append(node)
    expected=set(ID_MAP.values())
    assert len(SOURCE['naval_ids']) == 20
    assert len(nodes) == 26 and {n['id'] for n in nodes} == expected
    assert all(n['title'] == SOURCE['localisation'][n['source_focus_id']] for n in nodes)
    assert all(n['description'] == SOURCE['localisation'][n['source_focus_id']+'_desc'] for n in nodes)
    assert all(n['effect_rows'] and n['cost'] > 0 for n in nodes)
    assert all('Conditional availability' not in n['requirements'] for n in nodes)
    assert all(parent in expected for n in nodes for group in n['prerequisites'] for parent in group)
    assert all(parent in expected for n in nodes for parent in n['mutually_exclusive'])
    return nodes


def title_image(title, font):
    from PIL import Image
    words = title.split()
    lines, line = [], ''
    for word in words:
        candidate = word if not line else line + ' ' + word
        if font.width(candidate) <= 143:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    if len(lines) <= 1:
        return font.raster(title), False

    # Balance the complete title over two preview lines. Do not truncate long
    # donor names even when their full native-font width needs scaling.
    choices=[]
    for i in range(1,len(words)):
        left=' '.join(words[:i]);right=' '.join(words[i:])
        choices.append((max(font.width(left),font.width(right)),abs(font.width(left)-font.width(right)),left,right))
    _,_,left,right=min(choices)

    def wide_raster(text):
        image=Image.new('RGBA',(max(1,font.width(text)),20))
        x=0;previous=None
        for char in text:
            cp=ord(char);glyph=font.GLYPHS.get(cp,font.GLYPHS[63])
            x+=font.KERNINGS.get((previous,cp),0)
            crop=font.atlas().crop((glyph['x'],glyph['y'],glyph['x']+glyph['width'],glyph['y']+glyph['height']))
            image.alpha_composite(crop,(x+glyph['xoffset'],2+glyph['yoffset']))
            x+=glyph['xadvance'];previous=cp
        return image

    canvas = Image.new('RGBA', (147, 26))
    for i, item in enumerate((left,right)):
        row = wide_raster(item).resize((147, 13), Image.Resampling.LANCZOS)
        canvas.alpha_composite(row, (0, i*13))
    return canvas, True


def native_art(icons):
    from PIL import Image
    sys.path.insert(0, str(HERE))
    import compile as cuba_compile
    registry = cuba_compile.registry()
    providers = (cuba_compile.GAME, cuba_compile.MD, cuba_compile.ROOT)
    result = {}
    for icon in icons:
        if icon in result:
            continue
        rel = registry.get(icon)
        if not rel:
            raise KeyError(f'Native sprite is not registered: {icon}')
        image_path = next((base / rel.replace('\\', '/') for base in providers if (base / rel.replace('\\', '/')).is_file()), None)
        if image_path is None:
            raise FileNotFoundError(f'Native sprite texture not found: {icon}: {rel}')
        with Image.open(image_path) as source:
            image = source.convert('RGBA')
            buff = io.BytesIO()
            image.save(buff, format='WEBP', quality=88, method=6)
        result[icon] = 'data:image/webp;base64,' + base64.b64encode(buff.getvalue()).decode('ascii')
    return result

