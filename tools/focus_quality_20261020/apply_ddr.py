# IMPERIA CW — Cold War: focus quality 20261020 — apply ddr.
"""Apply only approved DDR focus changes; leave unrelated live output intact."""
import json
import re
from source_edit import ROOT, write, replace_reward, loc_update
from ddr_runtime import build

P = 'COLDWAR_DDR_'
GEN = ROOT / 'Claude outputs/COLDWAR_DDR_generator'
actions = {'plan_repay_at_any_price': 'open_repayment',
           'nva_buy_from_the_brothers': 'start_import',
           'nva_the_t72_licence': 'start_licence'}
descs = {
    'power_gl': "Industrial pollution has turned an administrative failure into a crisis of confidence. A cabinet committed to environmental reform would challenge ministries accustomed to meeting production targets regardless of their consequences. Its task is to protect public health while keeping factories, employment and the energy system functioning.",
    'power_spk': "The State Planning Commission coordinates resources, investment and the targets imposed on every major enterprise. A government led by its planners would move economic authority away from competing party patrons and towards technical administration. Clearer priorities could ease shortages, but the planners would also have to answer publicly for choices once hidden behind the plan.",
    'cc_sto': "The chairman of the Council of Ministers commands an administration responsible for putting party decisions into practice. By seeking the party leadership as well, the premier would bring those offices under one political direction. Supporters promise coherent government; opponents fear that cabinet appointments and economic resources will become instruments of a personal succession campaign.",
    'nt_our_own_road': "Dependence on Soviet supplies and Western credit leaves the republic vulnerable to decisions made elsewhere. An independent course would put domestic production, alternative trading partners and a narrower range of essential imports at the centre of economic policy. Greater freedom of action must be earned through difficult choices about what the country can produce and afford.",
    'plan_repay_at_any_price': "Every debt payment competes with investment, imports and the goods households expect to find in the shops. The government will reserve liquid funds for a measurable reduction in outstanding principal rather than another expansion financed from abroad. A stronger balance sheet promises greater freedom of action, but the resources committed to repayment cannot build the next factory.",
    'nva_buy_from_the_brothers': "Soviet reserves offer a quicker route to strengthening the armoured force than building a new production industry at home. A paid procurement agreement would bring existing vehicles, training opportunities and closer military cooperation. The order must be accepted in Moscow, and the vehicles supplied will reflect the equipment actually available for delivery.",
    'nva_the_t72_licence': "Domestic tank assembly would give the republic industrial skills that an import order cannot provide. Soviet design rights and technical cooperation must accompany investment in workshops and production capacity. The project will proceed only when an available design can be licensed and the assembly works can be delivered; it does not grant access to a future tank generation.",
}


def apply():
    treepath = GEN / 'design/ddr_tree.json'
    pagepath = GEN / 'design/page_data.json'
    tree = json.loads(treepath.read_text(encoding='utf-8'))
    page = json.loads(pagepath.read_text(encoding='utf-8'))
    for f in tree['foci']:
        sid = f['id'].removeprefix(P)
        for e in f['eff']:
            if e['k'] == 'fac' and e['f'] == 'defense_industry':
                e['f'] = 'industrial_conglomerates'
        if sid in actions:
            f['eff'] = [{'k': 'quality', 'action': actions[sid]}]
        if sid == 'nva_the_t72_licence':
            f['name'] = 'Soviet Tank Assembly Licence'
    for f in page['foci']:
        sid = f['i']
        if sid in descs:
            f['d'] = descs[sid]
        for row in f['e']:
            row[2] = row[2].replace('Arms Industry opinion', 'Industrial Conglomerates opinion')
        if sid in actions:
            f['e'] = [['mix', 'quality', {
                'open_repayment': 'Fund a treasury-backed repayment up to3%GDP; matching debt reduction, -0.25pp interest730days, +8%sanction resistance and +5Moscow Trust on settlement.',
                'start_import': '25ArmyXP; request90real Soviet tanks at1%GDP, paid on accepted delivery; no equipment grant on refusal.',
                'start_licence': 'Request an available Soviet tank licence and2military factories at1.6%GDP; +3%military-factory productivity only on successful implementation.'
            }[actions[sid]]]]
            f['o'] = 'Paid implementation and one-time settlement are maintained in dg_quality.py runtime sources.'
        if sid == 'nva_the_t72_licence':
            f['n'] = 'Soviet Tank Assembly Licence'
    write(treepath, json.dumps(tree, ensure_ascii=False, separators=(',', ':')) + '\n')
    write(pagepath, json.dumps(page, ensure_ascii=False, separators=(',', ':')) + '\n')
    path = ROOT / 'common/national_focus/COLDWAR_DDR_1970_focus.txt'
    text = path.read_text(encoding='utf-8-sig')
    text = text.replace('change_defense_industry_opinion = yes', 'change_industrial_conglomerates_opinion = yes')
    for sid, action in actions.items():
        fid = P + sid
        text = replace_reward(text, fid, f'log = "[GetDateText]: [Root.GetName]: Focus {fid}"\n{P}Q_{action} = yes')
    write(path, text)
    locpath = ROOT / 'localisation/english/COLDWAR_DDR_1970_l_english.yml'
    entries = {P + sid + '_desc': desc for sid, desc in descs.items()}
    entries[P + 'nva_the_t72_licence'] = 'Soviet Tank Assembly Licence'
    write(locpath, loc_update(locpath.read_text(encoding='utf-8-sig'), entries))
    build()


if __name__ == '__main__':
    apply()
