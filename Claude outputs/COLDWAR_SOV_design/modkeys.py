import sys, glob, json
sys.path.insert(0,'/home/claude/sov')
from parse import *
from collections import Counter
cnt=Counter()
def collect(block):
    for k,o,v in block:
        if isinstance(v,list):
            if k in ('modifier',):
                for kk,oo,vv in v:
                    if not isinstance(vv,list) and oo=='=' : cnt[kk]+=1
            collect(v)
base='/mnt/user-data/uploads/mdcoldwar/common/'
for f in glob.glob(base+'ideas/*.txt'):
    collect(load(f))
SKIP={'icon','enable','remove_trigger','custom_modifier_tooltip','attacker_modifier','valid_relation_trigger'}
for f in glob.glob(base+'dynamic_modifiers/*.txt'):
    for k,o,v in load(f):
        if isinstance(v,list):
            for kk,oo,vv in v:
                if kk not in SKIP and not isinstance(vv,list): cnt[kk]+=1
json.dump(cnt, open('modkeys.json','w'), indent=0)
print(len(cnt))
print(sorted(cnt.items(), key=lambda x:-x[1])[:400])
