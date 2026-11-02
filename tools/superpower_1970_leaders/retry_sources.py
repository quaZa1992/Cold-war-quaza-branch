# IMPERIA COLD WAR — Complete pending identified portrait downloads.
from pathlib import Path
import json
import time
import requests
from prepare import download, HERE, USER_AGENT

path = HERE / 'sources.json'
data = json.loads(path.read_text(encoding='utf-8'))
for row in data['portraits']:
    if row['id'] == 'SOV_pyotr_siuda':
        row.update(source_url='https://meduza.io/image/attachments/images/002/639/677/original/7HoNnohUlHc-dB5ZCMgupg.jpg',
            source_page='https://meduza.io/en/feature/2017/11/23/the-novocherkassk-massacre',
            source_author='Photo from the Novocherkassk Tragedy Foundation; original photographer unknown', licence='unknown')
    if row['id'] == 'SOV_leonid_smirnov':
        row.update(actual_download_url='https://www.valka.cz/attachments/35946/Smirnov_LV.jpg',
            source_author='unknown', licence='unknown')
    if row['status'] not in ('reused', 'reference_ready'):
        download(row)
        print(row['id'], row['status'], flush=True)
        time.sleep(2)
path.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
