# IMPERIA CW — Cold War: focus quality 20261020 — test canonical sources.
"""Check owned generator contracts against the installed October quality pass."""
import json
from pathlib import Path
import re
import sys
import unittest
from source_edit import ROOT, focus_span
from script_model import parse, first, walk


class CanonicalSources(unittest.TestCase):
    def test_ddr_design_page_live_and_dynamic_readers(self):
        base=ROOT/'Claude outputs/COLDWAR_DDR_generator'
        design=json.loads((base/'design/ddr_tree.json').read_text(encoding='utf-8'))
        page=json.loads((base/'design/page_data.json').read_text(encoding='utf-8'))
        by={f['id']:f for f in design['foci']};pg={f['i']:f for f in page['foci']}
        text=(ROOT/'common/national_focus/COLDWAR_DDR_1970_focus.txt').read_text(encoding='utf-8')
        self.assertNotIn('change_defense_industry_opinion',text)
        self.assertFalse(any(e['k']=='fac' and e['f']=='defense_industry' for f in by.values() for e in f['eff']))
        expected={'plan_repay_at_any_price':'open_repayment','nva_buy_from_the_brothers':'start_import','nva_the_t72_licence':'start_licence'}
        for sid,action in expected.items():
            fid='COLDWAR_DDR_'+sid;self.assertEqual(by[fid]['eff'],[{'k':'quality','action':action}])
            self.assertEqual(len(pg[sid]['e']),1)
            a,b=focus_span(text,fid);self.assertIn('COLDWAR_DDR_Q_'+action+' = yes',text[a:b])
            self.assertNotIn('add_to_variable',text[a:b])
        sys.path.insert(0,str(base))
        import dg_effects as e
        for sid in expected:
            self.assertEqual(e.compile_effect(by['COLDWAR_DDR_'+sid]['eff'][0],by['COLDWAR_DDR_'+sid]),['COLDWAR_DDR_Q_'+expected[sid]+' = yes'])
        self.assertIn('imp_sanction_resistance',e.R.dyn['COLDWAR_DDR_planned_economy_modifier'])
        self.assertIn('military_factories_productivity',e.R.dyn['COLDWAR_DDR_planned_economy_modifier'])
        dyn=(ROOT/'common/dynamic_modifiers/COLDWAR_DDR_1970_dynamic_modifiers.txt').read_text(encoding='utf-8')
        for key in ['imp_sanction_resistance','military_factories_productivity']:
            self.assertIn(key+' = COLDWAR_DDR_planned_economy_'+key,dyn)
        for p in (base/'quality_runtime').rglob('*'):
            if p.is_file():self.assertEqual(p.read_bytes(),(ROOT/p.relative_to(base/'quality_runtime')).read_bytes(),str(p))

    def test_generic_real_compiler_and_installed_project_calls(self):
        sys.path.insert(0,str(ROOT/'Claude outputs/COLDWAR_GEN_generator'))
        import gen_common as g, gen_effects as e
        from gen_quality import OFFICE_PROJECTS,prefix,runtime_files,patch_base_office_focus
        from gen_quality_narratives import apply_narratives
        from gen_misc import old_loc_transform
        builder,design=g.load_design()
        raw=(ROOT/'common/scripted_effects/00_scripted_effects.txt').read_text(encoding='utf-8')
        for helper in ['two_office_construction','one_random_infrastructure']:
            match=re.search(r'^'+helper+r' = \{',raw,re.M)
            body=raw[match.start():g.block_end(raw,match.start())+1]
            e.BUILD_COST[helper]=abs(float(re.findall(r'treasury_change = (-?[\d.]+)',body)[-1]))
        ctx=e.Ctx(g.mod_loc_keys(str(ROOT)),builder.META,{})
        text=(ROOT/g.F_FOCUS).read_text(encoding='utf-8')
        checked=0
        for node in design['nodes']:
            fid='GEN_1970_'+node['id']
            if fid not in OFFICE_PROJECTS:continue
            lines=e.compile_focus(ctx,node,'GEN_1970_'+node['party']+'_programme','GEN_1970_'+node['party']+'_')
            self.assertEqual(lines.count(prefix(fid)+'_open = yes'),1)
            self.assertNotIn('two_office_construction = yes',lines)
            a,b=focus_span(text,fid);self.assertIn(prefix(fid)+'_open = yes',text[a:b])
            if fid=='GEN_1970_nlib_free_enterprise_zones':
                self.assertIn('one_random_infrastructure = yes',lines)
                self.assertIn('multiply = -0.005','\n'.join(lines))
            else:self.assertNotIn('modify_treasury_effect = yes',lines)
            checked+=1
        self.assertEqual(checked,10)
        self.assertEqual(text,patch_base_office_focus(text))
        a,b=focus_span(text,'GEN_1970_export_processing_zones')
        self.assertIn('add_ideas = GEN_1970_export_zones',text[a:b])
        for relative,payload in runtime_files().items():
            self.assertEqual((ROOT/relative).read_text(encoding='utf-8-sig'),payload.strip()+'\n')
        old=(ROOT/g.F_OLD_LOC).read_text(encoding='utf-8-sig')
        transformed,_=old_loc_transform(old,['GEN_1970_'+n['id'] for n in design['nodes']])
        self.assertIn('Attack helicopters require more than new aircraft',apply_narratives(transformed))

    def test_new_native_references_and_confirmation_lock(self):
        base=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
        registered=set()
        for directory in [ROOT/'interface',base/'interface']:
            for path in directory.rglob('*.gfx'):
                registered.update(re.findall(r'\bname\s*=\s*"?([\w.-]+)',path.read_text(encoding='utf-8-sig',errors='replace')))
        texts=[]
        for rel in ['events/COLDWAR_DDR_1970_quality.txt','common/decisions/COLDWAR_DDR_1970_quality.txt','common/decisions/categories/COLDWAR_DDR_1970_quality.txt','common/decisions/COLDWAR_GEN_1970_quality.txt','common/decisions/categories/COLDWAR_GEN_1970_quality.txt']:
            source=(ROOT/rel).read_text(encoding='utf-8');texts.append(source)
            for key,_,v in walk(parse(source)):
                if key in ['picture','icon'] and isinstance(v,str) and v.startswith('GFX_'):
                    self.assertIn(v.strip('"'),registered,rel)
        source=texts[0]
        event=next(v for k,_,v in parse(source) if k=='country_event' and first(v,'id')=='COLDWAR_DDR_Q.6')
        accept=first(event,'option')
        self.assertIn(('has_country_flag','=','COLDWAR_DDR_Q_repayment_dialog'),first(accept,'trigger'))
        self.assertIn('days = 8 value = 1',texts[1])
        self.assertEqual(first(event,'timeout_days'),'7')


if __name__=='__main__':unittest.main(verbosity=2)
