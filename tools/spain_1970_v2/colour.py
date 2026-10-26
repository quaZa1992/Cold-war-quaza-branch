# IMPERIA CW — Cold War: native Nationalist Spain map colour and regime routing.
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[2]
MARK='# IMPERIA CW — Cold War: Spain Nationalist map colour.\n'

def write(rel,text,loc=False):
    p=ROOT/rel;p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists() and p.read_text(encoding='utf-8-sig')==text:return
    stage=p.with_name(p.name+'.coldwar-stage')
    stage.write_text(text,encoding='utf-8-sig' if loc else 'utf-8',newline='\n')
    stage.replace(p)

# IMPERIA CW — Cold War: change the actual registered SPR colour, including
# the country-definition fallback; history effects are not the base source.
rel='common/countries/colors.txt'
text=(ROOT/rel).read_text(encoding='utf-8-sig')
match=re.search(r'(?m)^SPR\s*=\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',text)
if not match:raise ValueError('Registered SPR colour block missing')
block=match[0]
block,n=re.subn(r'\bcolor\s*=\s*rgb\s*\{[^{}]*\}','color = rgb { 200 100 31 }',block)
if n!=1:raise ValueError('Expected exactly one SPR map colour')
block,n=re.subn(r'\bcolor_ui\s*=\s*rgb\s*\{[^{}]*\}','color_ui = rgb { 245 123 38 }',block)
if n!=1:raise ValueError('Expected exactly one SPR UI colour')
if not text[:match.start()].endswith(MARK):block=MARK+block
write(rel,text[:match.start()]+block+text[match.end():])

rel='common/countries/Spain.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
text,n=re.subn(r'(?m)^color\s*=\s*\{[^{}]*\}', 'color = { 200 100 31 }',text)
if n!=1:raise ValueError('Expected exactly one Spanish country-definition colour')
if MARK not in text:text=text.replace('color = { 200 100 31 }',MARK+'color = { 200 100 31 }',1)
write(rel,text)

# Cosmetic colours belong in the loaded cosmetic registry, not an unregistered
# country-definition file. Keep the runtime alias for ongoing campaigns.
cosmetic='''COLDWAR_SPR_nationalist = {
 color = rgb { 200 100 31 }
 color_ui = rgb { 245 123 38 }
}
'''
rel='common/countries/cosmetic.txt';text=(ROOT/rel).read_text(encoding='utf-8-sig')
match=re.search(r'(?m)^COLDWAR_SPR_nationalist\s*=\s*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',text)
if match:text=text[:match.start()]+cosmetic.rstrip()+text[match.end():]
else:text=text.rstrip()+'\n\n'+MARK+cosmetic
write(rel,text)
obsolete=ROOT/'common/countries/COLDWAR_SPR_colours.txt'
if obsolete.exists():
    if obsolete.read_text(encoding='utf-8-sig')!=MARK+cosmetic:raise ValueError('Unexpected contents in obsolete owned colour file')
    obsolete.unlink()
write('common/scripted_effects/COLDWAR_SPR_colour.txt',MARK+'''COLDWAR_SPR_refresh_colour = {
 if = {
  limit = { original_tag = SPR }
  if = {
   limit = {
    OR = {
     check_variable = { ruling_party = 21 }
     AND = {
      IMP_is_1970_scenario = yes
      OR = {
       COLDWAR_SPR_government_continuity = yes
       COLDWAR_SPR_government_crown = yes
      }
     }
    }
   }
   if = {
    limit = { NOT = { has_cosmetic_tag = COLDWAR_SPR_nationalist } }
    set_cosmetic_tag = COLDWAR_SPR_nationalist
   }
  }
  else_if = {
   limit = { has_cosmetic_tag = COLDWAR_SPR_nationalist }
   drop_cosmetic_tag = yes
  }
 }
}
''')
write('common/on_actions/COLDWAR_SPR_colour.txt',MARK+'''on_actions = {
 on_daily_SPR = { effect = { COLDWAR_SPR_refresh_colour = yes } }
 on_ruling_party_change = {
  effect = { if = { limit = { original_tag = SPR } COLDWAR_SPR_refresh_colour = yes } }
 }
}
''')
write('localisation/english/COLDWAR_SPR_colour_l_english.yml','l_english:\n'+MARK+''' COLDWAR_SPR_nationalist:0 "Spain"
 COLDWAR_SPR_nationalist_DEF:0 "Spain"
 COLDWAR_SPR_nationalist_ADJ:0 "Spanish"
''',True)
(Path(__file__).resolve().parent/'colour_reference.json').write_text(json.dumps({'source':'E:/SteamLibrary/steamapps/common/Hearts of Iron IV/common/countries/cosmetic.txt','native_cosmetic':'SPR_nationalist_spain','map_rgb':[200,100,31],'ui_rgb':[245,123,38],'base_files':['common/countries/colors.txt','common/countries/Spain.txt'],'cosmetic_registry':'common/countries/cosmetic.txt','route':'Cold War mod base SPR colour is Nationalist brown-orange. The registered cosmetic alias also preserves that colour under fascist and Cold War authoritarian governments.'},indent=2)+'\n',encoding='utf-8')
print('Nationalist Spain colour generated: RGB200/100/31')
