# IMPERIA CW — Cold War: coldwar 1970 economy — data.
import json,re,glob,sys,math
sys.path.insert(0,'/tmp/claude-0/-home-claude/e0b16908-9a1c-5c10-a9dd-42d281a526d7/scratchpad/work')
from collections import defaultdict
W='/tmp/claude-0/-home-claude/e0b16908-9a1c-5c10-a9dd-42d281a526d7/scratchpad/work/'
M='/mnt/user-data/uploads/mod/mdcoldwar/'
st=json.load(open(W+'states_full.json'))
bs=json.load(open(W+'blds_split.json'))
imp=open(M+'common/scripted_effects/IMP_1970_gdp_scripted_effects.txt',encoding='utf-8-sig').read()
tgt={t:float(g) for t,g in re.findall(r'original_tag = (\w+) \} set_variable = \{ imp_1970_target_gdp = ([\d.]+)',imp)}
sprod={int(a):float(b) for a,b in re.findall(r'\n\t\t(\d+) = \{ set_variable = \{ productivity_state_var = ([\d.]+) \} \}',imp)}
catslots={}
for f in glob.glob(M+'common/state_category/*.txt'):
    s=open(f,encoding='utf-8-sig').read()
    for n,v in re.findall(r'(\w+) = \{\s*local_building_slots = (\d+)',s): catslots[n]=int(v)
cat={};extra={}
for f in glob.glob(M+'history/states/*.txt'):
    s=open(f,encoding='utf-8-sig',errors='replace').read()
    m=re.search(r'\bid\s*=\s*(\d+)',s); 
    if not m: continue
    sid=m.group(1)
    c=re.search(r'state_category\s*=\s*(\w+)',s); cat[sid]=c.group(1) if c else 'state_00'
    extra[sid]=sum(int(x) for x in re.findall(r'add_extra_state_shared_building_slots\s*=\s*(\d+)',s))
wb={l.split()[0]:float(l.split()[1]) for l in open(W+'wb2000.txt')}
# country aggregates
C=defaultdict(lambda: dict(pop=0,res=0,states=[],pw=0))
for sid,s in st.items():
    c=C[s['ctrl']]; p=s['mp']/1e6; c['pop']+=p; c['res']+=sum(s['res'].values()); c['states'].append(sid); c['pw']+=p*sprod[int(sid)]
for t,c in C.items(): c['prod_pw']=c['pw']/c['pop'] if c['pop']>0 else 100
calib=json.load(open(W+'calib_log.json'))
b=[l.split('budget check ')[1] for l in open('/mnt/user-data/uploads/logs/game.log',encoding='utf-8',errors='replace') if 'budget check' in l]
logprod={}
for r,x in zip(calib,b):
    logprod[r[0]]=float(re.search(r'prod ([\d.]+)',x).group(1))
