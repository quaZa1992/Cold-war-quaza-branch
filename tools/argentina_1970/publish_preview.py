# IMPERIA COLD WAR — Publish the current Argentina layout into its conversation preview.
"""Copy the compiled project fragment, preserving native art and host selection state."""
import argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--destination',type=Path,required=True);args=ap.parse_args()
    source=(ROOT/'docs/design/COLDWAR_ARG_1970/runtime-preview.html').read_text(encoding='utf-8')
    source=source.replace('const save=()=>{};',"const save=()=>window.openai?.setWidgetState?.({modelContent:{selected:state.selected,government:state.government,chapter:state.chapter},privateContent:{mode:state.mode}}).catch(()=>{});")
    assert source.startswith('<!-- IMPERIA COLD WAR') and '<!doctype' not in source.lower() and len(source.encode())<1000000
    args.destination.parent.mkdir(parents=True,exist_ok=True);args.destination.write_text(source,encoding='utf-8',newline='\n')
    print(str(args.destination))
