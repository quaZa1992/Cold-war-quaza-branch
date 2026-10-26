# IMPERIA CW — Cold War: historical currencies — validate.
"""Check historical English currency labels, date gates, art and preservation."""
from pathlib import Path
import copy,hashlib,json,re,struct,sys
from PIL import Image
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'tools/israel_1970'))
from script_format import read
sys.path.insert(0,str(ROOT/'tools/currency_balance'))
from balance_manifest import reverse_if_recorded


def sha(data):return hashlib.sha256(data).hexdigest()
def one(block,key):
    values=[v for k,o,v in block if k==key and o=='=']
    assert len(values)==1,(key,len(values))
    return values[0]
def parsed(path):return read(reverse_if_recorded(path,(ROOT/path).read_bytes()).decode('utf-8-sig'))


def reverse_edits(data,record):
    assert sha(data)==record['after_sha256'],'Current file differs from recorded scoped edits'
    for edit in reversed(record['edits']):
        offset=edit['offset_after'];after=edit['after'].encode();before=edit['before'].encode()
        assert data[offset:offset+len(after)]==after
        data=data[:offset]+before+data[offset+len(after):]
    assert sha(data)==record['before_sha256'],'Unrelated file bytes changed'
    return data


def date(text):return tuple(map(int,text.split('.')))
def enabled(block,when,flags=(),focuses=()):
    result=[]
    for key,op,value in block:
        if key.startswith('#'):continue
        if key=='NOT':result.append(not enabled(value,when,flags,focuses))
        elif key=='OR':result.append(any(enabled([entry],when,flags,focuses) for entry in value))
        elif key=='AND' or key=='HOL':result.append(enabled(value,when,flags,focuses))
        elif key=='date':result.append(when<date(value) if op=='<' else when>date(value))
        elif key=='has_country_flag':result.append(value in flags)
        elif key=='has_completed_focus':result.append(value in focuses)
        else:raise AssertionError(('Unsupported gate',key))
    return all(result)


def main():
    checks=[]
    def check(condition,message):
        assert condition,message
        checks.append(message)
    baseline=json.loads((HERE/'baseline.json').read_text())
    changes=json.loads((HERE/'changes.json').read_text())['files']
    before={}
    for name,record in changes.items():
        before[name]=reverse_edits(reverse_if_recorded(name,(ROOT/name).read_bytes()),record)
        check(sha(before[name])==baseline['before'][name],f'Exact reverse-byte proof: {name}')
    for name,digest in baseline['protected'].items():
        current=(ROOT/name).read_bytes()
        check(sha(current)==digest,f'Protected asset unchanged: {name}')
    path='common/ideas/AA_law_expanded_economics.txt'
    old=one(one(read(before[path].decode('utf-8-sig')),'ideas'),'reserve_currency')
    laws=one(one(parsed(path),'ideas'),'reserve_currency')
    check([k for k,o,v in laws]==[k for k,o,v in old],'Every currency ID and its order preserved')
    for key,op,value in old:
        current=copy.deepcopy(one(laws,key)) if isinstance(value,list) else value
        if key in ('russia_rouble','gulden'):
            picture=one(current,'picture')
            check(picture==('mdcw_soviet_rouble' if key=='russia_rouble' else 'mdcw_dutch_guilder'),f'{key}: native picture reference')
            current=[entry for entry in current if entry[0]!='picture']
        if key=='gulden':
            alternatives=one(one(current,'available'),'OR')
            check(alternatives.count(('date','<','1999.1.1'))==1,'Historical guilder date gate is unique')
            alternatives.remove(('date','<','1999.1.1'))
        check(current==value,f'Original law effects and conditions preserved: {key}')
    available=one(one(laws,'gulden'),'available')
    for when,focuses,flags,want in [
        ('1970.1.1',(),(),True),('1985.1.1',(),(),True),('1998.12.31',(),(),True),
        ('1999.1.1',(),(),False),('2000.1.1',('HOL_bring_back_the_gulden',),(),True),
        ('2000.1.1',('HOL_restore_royal_authority',),(),True),
        ('2000.1.1',('HOL_bring_back_the_gulden',),('EU_joined_the_eurozone',),False)]:
        check(enabled(available,date(when),flags,focuses)==want,f'Guilder availability: {when}, {focuses}, {flags}')
    loc={}
    for name in ['localisation/english/MD_currency_l_english.yml','localisation/english/mdcw_dem_currency_l_english.yml',
                 'localisation/english/mdcw_coldwar_currency_labels_l_english.yml']:
        raw=(ROOT/name).read_bytes()
        check(raw.startswith(b'\xef\xbb\xbf'),f'English localization BOM: {name}')
        entries=dict(re.findall(r'^ (\w+): "(.*)"$',raw.decode('utf-8-sig'),re.M))
        check(not loc.keys()&entries.keys(),f'No duplicate English keys: {name}')
        loc.update(entries)
    helpers={one(value,'name'):value for key,op,value in parsed('common/scripted_localisation/mdcw_historical_currency_scripted_localisation.txt')}
    def select(helper,when):
        for key,op,entry in helpers[helper]:
            if key!='text':continue
            trigger=[v for k,o,v in entry if k=='trigger']
            if not trigger or enabled(trigger[0],date(when)):
                return loc[one(entry,'localization_key')]
        raise AssertionError('No localization fallback')
    check(select('GetMdcwRoubleName','1970.1.1')=='Soviet Rouble','1970 name resolves to Soviet Rouble')
    check(select('GetMdcwRoubleName','1992.1.1')=='Russian Rouble','Later Russian name resolves')
    check('Soviet Union' in select('GetMdcwRoubleDescription','1970.1.1'),'Soviet description resolves')
    check('Russian Federation' in select('GetMdcwRoubleDescription','2000.1.1'),'Modern rouble description retained')
    check('euro' not in select('GetMdcwGuilderDescription','1970.1.1').lower(),'1970 guilder description omits euro restoration')
    check('reintroduced' in select('GetMdcwGuilderDescription','2000.1.1'),'Later restored-guilder description retained')
    check('not freely convertible' in select('GetMdcwYuanDescription','1970.1.1'),'Cold War yuan exchange controls described')
    check('emerging reserve' in select('GetMdcwYuanDescription','2000.1.1'),'Later yuan description retained')
    check([loc[key] for key in ['gulden','swiss_frank','chinese_yuan']]==['Dutch Guilder','Swiss Franc','Chinese Yuan'],'Fixed English currency names resolve')
    sprites=one(parsed('interface/mdcw_coldwar_currency_icons.gfx'),'spriteTypes')
    assets=json.loads((HERE/'asset_manifest.json').read_text())['assets']
    for name,record in assets.items():
        raw=(ROOT/record['texture']).read_bytes()
        check(sha(raw)==record['texture_sha256'],f'{name}: shipped icon hash')
        check(sha((ROOT/record['source']).read_bytes())==record['source_sha256'],f'{name}: generated master preserved')
        check(len(raw)==18560 and raw[:4]==b'DDS ' and struct.unpack_from('<II',raw,12)==(64,72),f'{name}: native 72x64 DDS')
        check(struct.unpack_from('<I',raw,88)[0]==32 and struct.unpack_from('<4I',raw,92)==(0xff0000,0xff00,0xff,0xff000000),f'{name}: BGRA alpha format')
        image=Image.open(ROOT/record['texture']).convert('RGBA');alpha=image.getchannel('A')
        check(alpha.getextrema()==(0,255) and all(alpha.getpixel((x,y))==0 for x in range(72) for y in [0,63])
              and all(alpha.getpixel((x,y))==0 for y in range(64) for x in [0,71]),f'{name}: transparent outer border')
        symbol='mdcw_soviet_rouble' if name=='soviet_rouble' else 'mdcw_dutch_guilder'
        matches=[v for k,o,v in sprites if one(v,'name')=='"GFX_idea_'+symbol+'"']
        check(len(matches)==1 and one(matches[0],'texturefile').strip('"')==record['texture'],f'{name}: exact sprite linkage')
    report={'status':'PASS','checks':checks,'scope':'Static source, English labels, date gates and native art; no in-game test.'}
    (HERE/'validation_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS: {len(checks)} checks; historical English currency labels, icons and preserved law effects verified.')


if __name__=='__main__':main()
