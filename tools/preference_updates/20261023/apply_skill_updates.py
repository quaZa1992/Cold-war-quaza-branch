# IMPERIA COLD WAR — Install the explicitly requested, validated MD-CW skill updates.
from pathlib import Path
import hashlib
import json
import shutil

HERE=Path(__file__).resolve().parent
TARGET=Path('C:/Users/Enes/.codex/skills').resolve()
ALLOWED={'mdcw-national-trees','mdcw-modifier-audit','mdcw-tree-layout'}


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    manifest=json.loads((HERE/'SKILL_UPDATE_MANIFEST.json').read_text())
    assert Path(manifest['root']).resolve()==TARGET
    validation=json.loads((HERE/'SKILL_VALIDATION.json').read_text())
    assert set(validation['skills'])==ALLOWED
    pending=[]
    for entry in manifest['files']:
        rel=Path(entry['path']);assert rel.parts[0] in ALLOWED and rel.suffix=='.md'
        source=(HERE/'draft'/rel).resolve();dest=(TARGET/rel).resolve()
        assert source.is_relative_to((HERE/'draft').resolve()) and dest.is_relative_to(TARGET)
        assert not (TARGET/rel).is_symlink()
        assert digest(source)==entry['after_sha256']
        assert (digest(dest) if dest.exists() else None)==entry['before_sha256'],str(dest)
        pending.append((source,dest,entry))
    for source,dest,entry in pending:
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
        assert digest(dest)==entry['after_sha256']
    report={'project':'IMPERIA COLD WAR','installed_files':len(pending),'skills':sorted(ALLOWED),'files':manifest['files']}
    (HERE/'SKILL_INSTALL_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'installed_files':len(pending),'skills':sorted(ALLOWED)}))


if __name__=='__main__':main()
