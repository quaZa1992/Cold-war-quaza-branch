# IMPERIA CW — Cold War: eastern mediterranean 1970 — recover outputs.
"""Reattach reviewed imagegen outputs after an export-helper failure.

The explicit mapping was checked visually against the original named references.
Original generated files remain untouched. No image is synthesized here.
"""
import json
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUTS = Path('C:/Users/Enes/.codex/generated_images/01a1431d-4972-7a81-99ad-c3beb5089421')


def main():
    catalog = json.loads((HERE/'request_catalog.json').read_text(encoding='utf-8'))
    mappings = json.loads((HERE/'recovered_outputs.json').read_text(encoding='utf-8'))
    (HERE/'masters').mkdir(exist_ok=True)
    (HERE/'generated').mkdir(exist_ok=True)
    for record in catalog:
        key = record['country']+'_'+record['key']
        if key not in mappings:
            continue
        existing = HERE/'generated'/(key+'.json')
        if existing.is_file() and json.loads(existing.read_text(encoding='utf-8')).get('revision', 0):
            continue  # A subsequently reviewed narrow imagegen edit wins.
        source = OUTPUTS/('exec-'+mappings[key]+'.png')
        assert source.is_file(), source
        master = HERE/'masters'/(key+'.png')
        shutil.copyfile(source, master)
        record.update(master=str(master), generator_output=str(source),
                      verification='Original and restored faces reviewed; explicit source/output mapping.')
        # These source compositions retain more torso; DDS export alone frames
        # head and shoulders. The full generated photograph is preserved.
        crops = {'GRE_constantine_ii': [0.21,0.0,0.79,0.47],
                 'TUR_fahri_koruturk': [0.19,0.0,0.81,0.60],
                 'TUR_bulend_ulusu': [0.29,0.31,0.89,0.86],
                 'GRE_arapakis': [0.25,0.025,0.85,0.59],
                 'GRE_davos': [0.18,0.0,0.99,0.70],
                 'GRE_florakis': [0.15,0.015,0.80,0.55],
                 'GRE_papanikolaou': [0.18,0.24,0.86,0.86],
                 'CYP_georgitsis': [0.10,0.0,0.95,0.77]}
        if key in crops:
            record['crop_box'] = crops[key]
        (HERE/'generated'/(key+'.json')).write_text(
            json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Recovered',len(mappings),'reviewed generated portraits')


if __name__ == '__main__':
    main()
