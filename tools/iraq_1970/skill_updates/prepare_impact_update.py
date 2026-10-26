# IMPERIA CW — Cold War: skill updates — prepare impact update.
"""Stage the user's explicit attractive-choice lesson; never writes skills."""
from pathlib import Path
import json,hashlib

base=Path('C:/Users/Enes/.codex/skills')
changes={
 'mdcw-national-trees/SKILL.md':(
  '- Make choices distinct, with credible benefits, costs, risks and opportunity costs. Do not force a malus onto every focus or offer one universally superior policy behind cosmetic alternatives.',
  '- Make both sides of a historically grounded exclusive choice attractive: the player should want both rewards but have a real reason to choose. Give them different substantial outcomes and, where plausible, a modest disadvantage or credible opportunity cost. Strengthen existing forks before multiplying cosmetic exclusions. Exclude competing constitutional terms, scarce funding priorities or military commitments; keep ordinary complementary development shared. A difficult historical situation and its starting penalties remain real; this preference is not a mandate to make every policy harmless.\n- Audit impact across a whole compatible route, including its follow-ups, starting spirits, temporary decisions and government gates. Do not sum incompatible parties or add several versions of the same army reform on top of one another. Replace overlapping rewards explicitly. Prefer meaningful assets, limited-use research/doctrine bonuses, training and enacted institutions to repetitive tiny PP/stability changes or bureaucracy-only penalties. Check whether a positive reward is already lost at an existing cap.\n- Give important choices enough distinct follow-through to change the programme. Merge accounting/review filler into the reform it serves; avoid stamping every party with the same focus count, doubled fork and ceremonial finale. These are outcome criteria, not a universal minimum bonus, mandatory malus or prescribed number of forks.'),
 'mdcw-national-trees/references/project-contract.md':(
  '| Trade-offs | Costs/disadvantages where plausible, not attached mechanically to every focus. Avoid cosmetic alternatives with one universally superior outcome. |',
  '| Trade-offs | Both historically grounded exclusive options should be attractive enough that the player would like both. Give them distinct substantial benefits and a plausible modest drawback or opportunity cost. Audit the whole reachable programme and its stacking; strengthen existing choices before adding more. Shared ordinary development stays shared. Preserve serious historical starting problems rather than making every policy harmless. |'),
 'mdcw-modifier-audit/SKILL.md':(
  '3. Compare visible tooltips with executed effects.',
  '3. When reviewing reward impact, compare both complete exclusive programmes, including follow-ups, cost, timing and meaningful drawbacks. The user wants two attractive, historically motivated alternatives rather than a strong option beside a punishment. Identify bureaucracy-only filler, duplicated small PP/stability rewards, bonuses discarded at a cap and nominally different choices delivering the same result. Check compatible whole-route stacking before proposing larger values; prefer distinct research/doctrine, assets, training or institutional outcomes over repeated generic combat buffs. Do not infer that all useful projects must be mutually exclusive or that every individual focus needs a malus.\n4. Compare visible tooltips with executed effects.')}
updates=[]
for relative,(before,after) in changes.items():
    path=base/relative;raw=path.read_bytes();text=raw.decode('utf-8')
    assert text.count(before)==1,(relative,'Changed source anchor')
    result=text.replace(before,after,1)
    # Keep the existing mechanic-audit numbered workflow coherent.
    if relative=='mdcw-modifier-audit/SKILL.md':
        result=result.replace('\n4. Follow references transitively:','\n5. Follow references transitively:').replace('\n5. Check that the route is reachable','\n6. Check that the route is reachable').replace('\n6. Report concrete findings','\n7. Report concrete findings')
    updates.append(dict(relative=relative,before_sha256=hashlib.sha256(raw).hexdigest(),after=result))
out=Path(__file__).with_name('impact_updates.json')
out.write_text(json.dumps(updates,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared three bounded skill edits:')
for row in updates:print(row['relative'])
