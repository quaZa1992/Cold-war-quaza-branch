# IMPERIA COLD WAR — Stage and apply the user's MD presentation skill corrections.
"""Stages a reviewable patch; --apply writes only the four explicitly named skill files."""
import difflib
import hashlib
import json
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
SKILLS=Path('C:/Users/Enes/.codex/skills')
STAGE=HERE/'skill_updates'
TARGETS={
 'mdcw-national-trees/SKILL.md',
 'mdcw-national-trees/references/project-contract.md',
 'mdcw-modifier-audit/SKILL.md',
 'mdcw-tree-layout/SKILL.md',
}
def sha(raw):return hashlib.sha256(raw).hexdigest()
def after(text,anchor,addition):
    if addition in text:return text
    assert text.count(anchor)==1,anchor
    return text.replace(anchor,anchor+'\n'+addition,1)

if '--apply' in sys.argv:
    manifest=json.loads((STAGE/'manifest.json').read_text(encoding='utf-8'))
    assert set(manifest['files'])==TARGETS
    changes=[]
    for rel,meta in manifest['files'].items():
        target=(SKILLS/rel).resolve()
        assert target.is_relative_to(SKILLS.resolve()) and rel in TARGETS
        staged=(STAGE/rel).read_bytes()
        assert sha(staged)==meta['staged_sha256'],'Staged file changed: '+rel
        assert sha(target.read_bytes())==meta['original_sha256'],'Skill changed since staging: '+rel
        changes.append((target,staged))
    for target,raw in changes:target.write_bytes(raw)
    print('Updated four authorized skill files; unrelated resources and metadata preserved.')
    raise SystemExit(0)

records={};patch=[]
for rel in sorted(TARGETS):
    source=SKILLS/rel;raw=source.read_bytes();old=raw.decode('utf-8-sig');new=old
    if rel=='mdcw-national-trees/SKILL.md':
        new=after(new,
            '- Use MD\'s exact party/subparty model. A programme becomes available when that party governs; do not require a redundant \'unlock our already-ruling party\' focus. Accession focuses are justified when they really change government through the agreed system. Show an unapproved new party as a provisional design; do not invent a live ideology or party-array slot to make it fit.',
            '- Keep all party branches visible and inspectable, including parties outside government, unless the user explicitly requests hiding. Gate focus availability, real completion and programme activation on the exact ruling party; do not use party-dependent `allow_branch` to conceal content.\n- For visible party requirements, reuse the existing native MD exact-party `*_are_in_power` trigger and its registered party-name tooltip. For example, `western_liberals_are_in_power` already checks slot 2 and displays `[liberalism_L] is in Power.` Do not replace it with invented labels such as "Governing political current" or a broad outlook/coalition check. Preserve hidden scenario, dated-identity and receipt guards. Programme names should use the actual registered party name, not a present-to-future party label joined by an arrow.')
        new=after(new,
            'Produce a full-tree preview with existing neighbours and normal-scale branch views, using the same resolved coordinates, connectors and labels as the proposed code. A focus inspector should expose conditions and exact proposed rewards. Narrative prose belongs in descriptions; normal completion rewards remain in native tooltips.',
            '\nEffect fields must contain only concrete native costs, signed modifier changes, research/experience, named spirit changes and decision unlocks. Do not append custom explanatory paragraphs about ownership, consent, expiry or bookkeeping. Put necessary context in descriptions or visible requirements. Keep native numeric formatters and standard MD headings; use `unlock_decision_tooltip` for a decision unlock and non-executing native effect previews for recipient-approved rewards. This applies to every focus, decision, event option and preview in the tree.')
    elif rel=='mdcw-modifier-audit/SKILL.md':
        new=after(new,
            'Read [references/modifier-effect-audit.md](references/modifier-effect-audit.md) when verifying modifier keys, formulas, units, tooltips, stacking, dynamic ideas, equipment, research, or doctrine effects. Read [references/focus-graph-and-scenario.md](references/focus-graph-and-scenario.md) when auditing transitive references, party-change cleanup, or 1970-scenario reachability.',
            '\nFor party and tooltip reviews, verify the visible native MD `*_are_in_power` predicate resolves to the intended exact party slot and existing party-name localisation. Reject invented "Governing political current" labels, outlook/coalition substitutes and combined present/future party names in live requirements. Check that inactive party branches remain inspectable and execution is blocked by availability/completion guards rather than party-dependent `allow_branch`. In effect fields require native numeric/named outcomes, not explanatory custom paragraphs; necessary prose belongs in descriptions or requirements. Native numeric formatters and standard MD headings remain valid. Compare every prospective reward with execution even while its real party/treaty gate is false.')
    elif rel=='mdcw-tree-layout/SKILL.md':
        new=after(new,
            'When approval is reserved, keep the proposed layout outside loaded files until accepted. Implement an already approved layout without another confirmation round.',
            '\nParty branches remain visible and inspectable outside government unless the user explicitly requests hiding. Use exact-party availability/completion and modifier-activation checks; do not add party-dependent `allow_branch`. Reserve the complete footprint of inactive branches and include them in the starting-government overview. A preview that shows all parties cannot validate an installed tree that hides them. Reuse the actual registered party names and native MD requirement display, and check live labels for unsupported glyphs; do not combine current and future party names with arrows.')
    else:
        new=after(new,
            '| Politics | Distinct programmes for relevant parties/leaders, with internal choices. Outlooks and exact governing subparties are different things. Historical starting leader, ruling subparty and country identity belong in dated history; inspect later native callbacks for overwrites instead of using startup patches as the source of truth. |',
            '| Party visibility and requirements | Keep all party trees visible and inspectable; only execution and party programmes depend on governing. Do not hide them with party-dependent `allow_branch`. Reuse native MD exact-party `*_are_in_power` checks and their registered party-name tooltips, rather than invented "Governing political current" text or outlook/coalition substitutes. Use the actual party name instead of a present/future name joined by an arrow. |')
        new=after(new,
            '| Spirits | Relevant starting challenges, visible improvement and intentional party-bound cleanup. Avoid unconditional lists removing spirits a country never had. |',
            '| Effect fields | Show only concrete native costs, signed modifiers, research/experience, named spirit changes and decision unlocks. No custom explanatory paragraphs about ownership, consent, expiry or internal handling; place needed context in descriptions or visible requirements. Native numeric formatters and standard MD headings are appropriate. Apply this across all focuses, decisions, event options and previews. |')
    dest=STAGE/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(new,encoding='utf-8',newline='\n')
    records[rel]={'original_sha256':sha(raw),'staged_sha256':sha(dest.read_bytes())}
    patch.extend(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=str(source),tofile=str(source)))
(STAGE/'manifest.json').write_text(json.dumps({'project':'IMPERIA COLD WAR','scope':'User-requested MD skill preference corrections only','files':records},indent=2)+'\n',encoding='utf-8')
(STAGE/'changes.patch').write_text(''.join(patch),encoding='utf-8')
print('Staged four skill-file edits at '+str(STAGE))
print(''.join(patch))
