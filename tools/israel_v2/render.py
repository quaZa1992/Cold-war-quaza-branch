# IMPERIA COLD WAR — Render the independent Israel Version 2.0 design preview.
from pathlib import Path
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'docs/israel_1970_v2'
VIS=Path('C:/Users/Enes/.codex/visualizations/2026/10/27/01a17ef9-3adf-7210-95e8-0788b3b5a632/israel-1970-v2.html')
WRAPPER=Path('C:/Users/Enes/.codex/plugins/cache/openai-bundled/visualize/1.0.57/skills/visualize/scripts/render.py')

def main():
    data=json.loads((HERE/'design.json').read_text(encoding='utf-8'))
    fragment=(HERE/'fragment.html').read_text(encoding='utf-8')
    assert fragment.count('<!-- DESIGN_DATA -->')==1
    fragment=fragment.replace('<!-- DESIGN_DATA -->','<script type="application/json" id="isr-v2-data">'+json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'</script>')
    assert len(fragment.encode('utf-8'))<1_000_000
    assert all(token not in fragment.lower() for token in ('<!doctype','<html','<body','<head>'))
    VIS.write_text(fragment,encoding='utf-8')
    subprocess.run([sys.executable,str(WRAPPER),str(VIS),str(OUT/'preview.html'),'--force'],check=True)
    preview=OUT/'preview.html'
    text=preview.read_text(encoding='utf-8')
    text=text.replace('<!doctype html>','<!doctype html>\n<!-- IMPERIA COLD WAR — Israel Version 2.0 standalone design review. -->',1)
    preview.write_text(text,encoding='utf-8')
    print(json.dumps(dict(project='IMPERIA COLD WAR',path=str(VIS),bytes=len(fragment.encode('utf-8')),focuses=len(data['nodes']))))

if __name__=='__main__':main()
