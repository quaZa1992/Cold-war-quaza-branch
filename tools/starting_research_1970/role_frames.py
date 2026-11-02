# IMPERIA COLD WAR — Retired extra historical aircraft role frames.
"""Keep old generated paths inert; historical variants now use native MD types."""
import argparse
import os
import re
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
MARK='# IMPERIA COLD WAR — Native role derivatives for historical early airframes.'
ENUM_BEGIN=MARK+' BEGIN'
ENUM_END=MARK+' END'

def outputs():
    source_path=ROOT/'common/script_enums.txt'
    source=source_path.read_text(encoding='utf-8-sig')
    source=re.sub(r'(?m)^[ \t]*'+re.escape(ENUM_BEGIN)+r'\n.*?^[ \t]*'+re.escape(ENUM_END)+r'\n','',source,flags=re.S)
    return {
        source_path:source,
        ROOT/'common/units/equipment/MD_w_COLDWAR_1970_historical_role_frames.txt':MARK+'\n# Retired. Historical variants use native MD production frames.\nequipments = {}\n',
        ROOT/'localisation/english/COLDWAR_1970_historical_role_frames_l_english.yml':'l_english:\n '+MARK+'\n # Retired. No additional equipment types.\n',
    }

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    for path,source in outputs().items():
        raw=source.encode('utf-8-sig' if path.suffix=='.yml' else 'utf-8')
        if args.apply:
            temporary=path.with_name(path.name+'.retirement.tmp')
            temporary.write_bytes(raw)
            os.replace(temporary,path)
        if args.check:assert path.read_bytes()==raw,path
    print('Historical extra role frames retired: zero custom production frames')

if __name__=='__main__':main()
