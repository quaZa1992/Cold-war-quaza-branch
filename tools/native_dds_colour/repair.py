# IMPERIA COLD WAR — Repair audited RGBA DDS storage without changing decoded artwork.
"""Normalize the nine audited 32-bit textures; --check verifies without writing."""
from pathlib import Path
import argparse
import hashlib
import io
import json
import struct
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
TEXTURES = (
    'gfx/event_pictures/coldwar_1970/COLDWAR_DDR_intro.dds',
    'gfx/event_pictures/coldwar_1970/COLDWAR_SOV_politburo_session.dds',
    'gfx/event_pictures/COLDWAR_UAE/COLDWAR_UAE_rulers_colour.dds',
    'gfx/interface/bop/PER_bop_ayatolas.dds',
    'gfx/interface/ideas/nat_ideas/COLDWAR_IMPERIA_joint_training_command.dds',
    'gfx/interface/ideas/nat_ideas/mdcw_gw_overseas_employment.dds',
    'gfx/interface/ideas/nat_ideas/mdcw_gw_recruitment.dds',
    'gfx/interface/ideas/companies/Denmark/Maersk.dds',
    'gfx/texticons/parties_icons/turkey/TUR_Western_Autocracy.dds',
)
RGBA = (0xff, 0xff00, 0xff0000, 0xff000000)
BGRA = (0xff0000, 0xff00, 0xff, 0xff000000)
ARCHIVES = {
    TEXTURES[0]: 'Claude outputs/COLDWAR_DDR_generator/art/dds/COLDWAR_DDR_intro.dds',
    TEXTURES[1]: 'Claude outputs/COLDWAR_SOV_generator/art/dds/COLDWAR_SOV_politburo_session.dds',
}
RECEIPTS = {
    TEXTURES[0]: 'tools/event_art/source/COLDWAR_DDR_intro_export.json',
    TEXTURES[1]: 'docs/event_art_review/politburo_export.json',
    TEXTURES[2]: 'tools/uae_1970/art/EVENT_PICTURE_VALIDATION.json',
    TEXTURES[4]: 'tools/joint_training_icon/validation.json',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    records = []
    for rel in TEXTURES:
        path = ROOT / rel
        before = path.read_bytes()
        assert before[:4] == b'DDS '
        header = struct.unpack('<31I', before[4:128])
        assert header[20] == 0 and header[21] == 32 and header[22:26] in (RGBA, BGRA), rel
        decoded = Image.open(io.BytesIO(before)).convert('RGBA')
        if header[22:26] == RGBA:
            assert not args.check, 'Non-native channel layout: ' + rel
            # Swap every pixel in all mip levels; retain the complete DDS layout.
            payload = bytearray(before[128:])
            assert len(payload) % 4 == 0
            payload[0::4], payload[2::4] = payload[2::4], payload[0::4]
            fixed = bytearray(before[:128])
            struct.pack_into('<4I', fixed, 92, *BGRA)
            after = bytes(fixed) + bytes(payload)
            assert len(after) == len(before)
            assert Image.open(io.BytesIO(after)).convert('RGBA').tobytes() == decoded.tobytes(), rel
            backup = HERE / 'before' / rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                backup.write_bytes(before)
            path.write_bytes(after)
        else:
            after = before
        if rel in ARCHIVES:
            archive = ROOT / ARCHIVES[rel]
            if args.check:
                assert archive.read_bytes() == after, str(archive)
            else:
                archive.write_bytes(after)
        if rel in RECEIPTS and not args.check:
            receipt = ROOT / RECEIPTS[rel]
            data = json.loads(receipt.read_text(encoding='utf-8'))
            data.update(project='IMPERIA COLD WAR', format='DDS uncompressed BGRA8 (A8R8G8B8)',
                        dds_sha256=hashlib.sha256(after).hexdigest())
            receipt.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
        records.append({'texture': rel, 'size': list(decoded.size), 'mip_levels': header[6],
                        'before_sha256': hashlib.sha256(before).hexdigest(),
                        'after_sha256': hashlib.sha256(after).hexdigest(),
                        'decoded_art_and_alpha_preserved': True})
    if not args.check:
        (HERE / 'repair_report.json').write_text(json.dumps({
            'project': 'IMPERIA COLD WAR', 'engine_tested': False, 'textures': records,
        }, indent=2) + '\n', encoding='utf-8')
    print(f'PASS: {len(records)} audited textures use native BGRA storage; decoded artwork is preserved.')


if __name__ == '__main__':
    main()
