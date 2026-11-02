# IMPERIA COLD WAR — Approved France 1970 replacement compiler.
"""Deterministic country-scoped generator. Never invoke the retired France compiler."""
from __future__ import annotations
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
APPROVED_HASH = '4f57a4c6e3d13eba6b7ec4129cb81fd8b9a2a645e9fac10c5ebf8d36588c18b5'
PARTY_REVISION_HASH = '5159aaad0f0b13bbf3ef38e2d374be05fcb907a5df6386c8b2e933520b278419'
EXPANSION_HASH = 'c8e6ab3933bf72a14b043c3a92d846826f3d1937f902efc7cc3d0dd64364c055'
MARK = '# IMPERIA COLD WAR — France 1970 approved replacement.\n'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def loc_text(values: dict[str, str]) -> str:
    rows = ['l_english:', MARK.rstrip()]
    for key, value in sorted(values.items()):
        assert '\u2013' not in value and '\u2014' not in value, (key, value)
        value = value.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')
        # Existing authored literal localisation line breaks remain intentional.
        value = value.replace('\\\\n', '\\n')
        rows.append(f' {key}:0 "{value}"')
    return '\n'.join(rows) + '\n'


def build() -> tuple[dict[str, bytes], dict]:
    from core import build_core
    from diplomacy import build_diplomacy
    from polish import build_art
    from integration import build_integrations
    from identity import build_identity
    from balance_revision import apply_balance_revision
    from starting_spirit_revision import apply_starting_spirit_revision
    from asset_reward_revision import apply_asset_reward_revision
    from expansion_revision import apply_expansion_revision
    from foreign_policy_revision import apply_foreign_policy_revision, APPROVED_SHA256 as FOREIGN_POLICY_HASH
    from deal_balance_revision import apply_deal_balance_revision
    from pressure import build_pressure
    from ec_membership_revision import apply_ec_membership_revision
    raw = (HERE / 'approved_design.json').read_bytes()
    assert sha(raw) == APPROVED_HASH, 'Immutable approved input has changed.'
    revision_raw = (HERE / 'approved_party_revision.json').read_bytes()
    assert sha(revision_raw) == PARTY_REVISION_HASH, 'Immutable party revision input has changed.'
    # The revision already contains the approved condensed native coordinates,
    # descriptions and artwork. Running the original polish again would replace
    # the newly approved programmes and distort their positions.
    design = apply_balance_revision(json.loads(revision_raw))
    design = apply_starting_spirit_revision(design)
    design = apply_asset_reward_revision(design)
    design['status'] = 'IMPLEMENTED. Compiled from the approved France 1970 party revision.'
    design['approved_source_sha256'] = APPROVED_HASH
    design['approved_party_revision_sha256'] = PARTY_REVISION_HASH
    design['revision'] = 'FRA2 runtime 1.2: persistent recovery and funded investment'
    design = apply_expansion_revision(design)
    design['status'] = 'IMPLEMENTED. Compiled from the approved France 1970 party and expansion revisions.'
    design['approved_expansion_sha256'] = EXPANSION_HASH
    design['revision'] = 'FRA2 runtime 1.3: approved 20-focus party expansion'
    design = apply_foreign_policy_revision(design)
    design['status'] = 'IMPLEMENTED. Compiled from approved French national and foreign-policy programmes.'
    design['approved_foreign_policy_sha256'] = FOREIGN_POLICY_HASH
    design['revision'] = 'FRA2 runtime 1.4: negotiated foreign policy'
    design = apply_deal_balance_revision(design)
    design['revision'] = 'FRA2 runtime 1.5: asymmetric agreements and restrained doctrine rewards'
    design['pressure_revision'] = json.loads((HERE / 'pressure_contracts.json').read_text(encoding='utf-8'))
    design = apply_ec_membership_revision(design)
    design['revision'] = 'FRA2 runtime 1.6: European Communities membership checks'
    packs = [build_core(design), build_diplomacy(design), build_art(design), build_identity(), build_pressure(design)]
    outputs: dict[str, bytes] = {}
    localisation = {}
    ownership = {}
    polished_localisation = []
    for pack_index, pack in enumerate(packs):
        for rel, text in pack.get('files', {}).items():
            assert rel not in outputs, ('Conflicting output owners', rel)
            if rel.endswith('.json'):
                assert json.loads(text).get('project') == 'IMPERIA COLD WAR', rel
            elif rel.endswith('.md'):
                assert text.startswith('IMPERIA COLD WAR'), rel
            elif rel == 'localisation/english/MD_money_l_english.yml':
                assert text.startswith('l_english:\n# IMPERIA COLD WAR — France 1970 bilateral budget breakdown integration.\n'), rel
                outputs[rel] = text.encode('utf-8-sig')
                ownership[rel] = 'narrow_shared_integration_bom_localisation'
                continue
            else:
                assert text.startswith('# IMPERIA COLD WAR — '), rel
            assert not text.startswith('\ufeff'), rel
            outputs[rel] = text.replace('\r\n', '\n').encode('utf-8')
            ownership[rel] = 'narrow_shared_integration' if pack_index == 3 else 'generated_runtime'
        for key, value in pack.get('loc', {}).items():
            if key in localisation and localisation[key] != value:
                assert pack_index == 2, ('Conflicting localisation providers', key)
                polished_localisation.append(key)
            localisation[key] = value
        for asset in pack.get('art_copies', []):
            source = Path(asset['source_absolute_path'])
            target = asset['target_repo_path']
            assert not source.is_symlink() and source.is_file()
            assert target not in outputs
            outputs[target] = source.read_bytes()
            ownership[target] = 'unchanged_donor_asset'
    loc_rel = 'localisation/english/COLDWAR_FRA2_1970_l_english.yml'
    outputs[loc_rel] = loc_text(localisation).encode('utf-8-sig')
    ownership[loc_rel] = 'generated_english_localisation'
    for rel, text in build_integrations().items():
        assert rel not in outputs
        outputs[rel] = text.encode('utf-8-sig' if rel.endswith('.yml') else 'utf-8')
        ownership[rel] = 'narrow_shared_integration'
    installed = json.dumps(design, ensure_ascii=False, indent=2) + '\n'
    outputs['tools/france_1970_runtime/runtime_design.json'] = installed.encode('utf-8')
    ownership['tools/france_1970_runtime/runtime_design.json'] = 'compiled_design'
    manifest = {
        'project': 'IMPERIA COLD WAR', 'feature': 'France 1970 replacement',
        'approved_sha256': APPROVED_HASH, 'focus_tree': 'COLDWAR_FRA2_1970_focus',
        'approved_party_revision_sha256': PARTY_REVISION_HASH,
        'approved_expansion_sha256': EXPANSION_HASH,
        'approved_foreign_policy_sha256': FOREIGN_POLICY_HASH,
        'foreign_policy_revision_source_sha256': sha((HERE / 'foreign_policy_revision.py').read_bytes()),
        'deal_balance_revision_source_sha256': sha((HERE / 'deal_balance_revision.py').read_bytes()),
        'pressure_source_sha256': sha((HERE / 'pressure.py').read_bytes()),
        'pressure_contracts_sha256': sha((HERE / 'pressure_contracts.json').read_bytes()),
        'pressure_partner_count': len(design['pressure_revision']['partners']),
        'foreign_policy_approval_sha256': sha((HERE / 'FOREIGN_POLICY_APPROVAL.json').read_bytes()),
        'expansion_revision_source_sha256': sha((HERE / 'expansion_revision.py').read_bytes()),
        'expansion_approval_sha256': sha((HERE / 'EXPANSION_APPROVAL.json').read_bytes()),
        'balance_revision_source_sha256': sha((HERE / 'balance_revision.py').read_bytes()),
        'starting_spirit_revision_source_sha256': sha((HERE / 'starting_spirit_revision.py').read_bytes()),
        'asset_reward_revision_source_sha256': sha((HERE / 'asset_reward_revision.py').read_bytes()),
        'ec_membership_revision_source_sha256': sha((HERE / 'ec_membership_revision.py').read_bytes()),
        'focus_count': len(design['nodes']), 'expansion_focus_count': len(design['expansion_revision']['added_focus_keys']),
        'offer_count': sum('offer' in n for n in design['nodes']),
        'english_localisation_keys': len(localisation),
        'editorial_localisation_overrides': polished_localisation,
        'files': {rel: {'sha256': sha(data), 'bytes': len(data), 'ownership': ownership[rel]}
                  for rel, data in sorted(outputs.items())},
    }
    return outputs, manifest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--check', action='store_true', help='Compare generated output without writing.')
    args = ap.parse_args()
    outputs, manifest = build()
    changed = []
    for rel, data in sorted(outputs.items()):
        path = ROOT / rel
        assert path.resolve().is_relative_to(ROOT.resolve()), rel
        if not path.is_file() or path.read_bytes() != data:
            changed.append(rel)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
    manifest_path = HERE / 'manifest.json'
    data = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if not args.check:
        manifest_path.write_bytes(data)
    elif not manifest_path.is_file() or manifest_path.read_bytes() != data:
        changed.append('tools/france_1970_runtime/manifest.json')
    print(json.dumps({'project': 'IMPERIA COLD WAR', 'check_only': args.check,
                      'focuses': manifest['focus_count'], 'offers': manifest['offer_count'],
                      'changed': changed}, indent=2))
    return 1 if args.check and changed else 0


if __name__ == '__main__':
    sys.exit(main())
