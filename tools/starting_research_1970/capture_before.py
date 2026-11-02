# IMPERIA COLD WAR — Pre-change archive for worldwide January 1970 research.
"""Keep private history snapshots on E: and a compact hash manifest in the repository."""
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
ARCHIVES=Path('E:/MDColdWar_Backups/Codex_Test_Archives').resolve()


def main():
    record=HERE/'before_hashes.json'
    if record.exists():
        data=json.loads(record.read_text(encoding='utf-8'))
        assert Path(data['archive']).is_file()
        print('Existing pre-change snapshot preserved:',data['archive'])
        return
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
    target=(ARCHIVES/('starting_research_1970_'+stamp+'.zip')).resolve()
    assert target.is_relative_to(ARCHIVES)
    assert not target.exists()
    paths=sorted((ROOT/'history/countries').glob('*.txt'))
    paths.extend(ROOT/'common/scripted_effects'/name for name in ('mdcw_1970_air_research_effects.txt','mdcw_1970_infantry_research_effects.txt'))
    ARCHIVES.mkdir(parents=True,exist_ok=True)
    hashes={}
    with zipfile.ZipFile(target,'x',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            assert path.resolve().is_relative_to(ROOT.resolve()) and not path.is_symlink()
            name=path.relative_to(ROOT).as_posix();data=path.read_bytes()
            hashes[name]=hashlib.sha256(data).hexdigest()
            archive.writestr(name,data)
    record.write_text(json.dumps({'project':'IMPERIA COLD WAR','feature':'January 1970 starting research','archive':str(target),'before_sha256':hashes},indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'archive':str(target),'files':len(hashes),'bytes':target.stat().st_size}))


if __name__=='__main__':main()
