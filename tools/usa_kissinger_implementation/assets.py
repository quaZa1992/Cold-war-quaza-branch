# IMPERIA COLD WAR — Technical atlas extraction and native texture registration.
from .shared import *
from io import BytesIO
from PIL import Image

def save_bytes(relative,data):
    path=ROOT/relative;path.parent.mkdir(parents=True,exist_ok=True)
    if path.exists() and path.read_bytes()==data:return False
    path.write_bytes(data);return True

def emit_assets():
    changed=[]
    source=HERE/'source/kissinger-atlas.webp'
    if not source.exists():
        approved=Path('C:/Users/Enes/.codex/visualizations/2026/10/24/01a16eeb-40d0-7851-80fa-70784386712c/kissinger-icons-concept-v2.webp')
        assert approved.exists(),'Approved art source missing'
        source.parent.mkdir(parents=True,exist_ok=True);source.write_bytes(approved.read_bytes())
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='df158e35ad6f3f852d35347e2e0742181d83b543c2fba2b5291327592ba21623'
    atlas=Image.open(source).convert('RGBA');assert atlas.size==(1448,1086)
    for i in range(12):
        x=(i%4)*362;y=(i//4)*362
        cell=atlas.crop((x,y,x+362,y+362)).resize((90,90),Image.Resampling.LANCZOS)
        buffer=BytesIO();cell.save(buffer,format='DDS')
        relative=f'gfx/interface/goals/COLDWAR_USA_KS/focus_{i}.dds'
        if save_bytes(relative,buffer.getvalue()):changed.append(relative)
    # Reuse the native Kurdish flag for related local authorities, preserving
    # the provider art at all three native sizes. No flag is put into history
    # ownership or on the map until an actual regional country exists.
    for tag in ('KPI','KPT','KPS'):
        for size in ('','medium/','small/'):
            donor=ROOT/('gfx/flags/'+size+'KUR_neutrality.tga');assert donor.exists(),donor
            relative='gfx/flags/'+size+tag+'.tga'
            if save_bytes(relative,donor.read_bytes()):changed.append(relative)
    notice=dict(project='IMPERIA COLD WAR',feature='Kissinger focus artwork and regional flags',
      concept=dict(source='OpenAI built-in image generation and edit, commissioned by this user',credit='AI-generated concept art; prompts by Codex',licence_or_permission='Generated for the user. Separate distribution licence unknown.',sha256=hashlib.sha256(source.read_bytes()).hexdigest(),modifications='Exact square cell extraction, resizing to native 90-pixel focus medallions and uncompressed RGBA DDS conversion. No creative repainting.'),
      native=dict(source='Installed Millennium Dawn / HOI4 assets',credit='Original Paradox and Millennium Dawn artists; individual names unknown',licence_or_permission='Unknown; retained upstream redistribution conditions apply.',references=['gfx/flags/KUR_neutrality.tga and its native medium/small versions','gfx/interface/autonomy/subject_progress_bar_long.dds and background','gfx/interface/ideas/diplomacy/flexible_foreign_policy2.dds','gfx/interface/ideas/politics/political_reform.dds','gfx/event_pictures/generic/elections/political_deal.dds'],modifications='Flag bytes copied to new related country tags; other native files referenced unchanged.'))
    relative='tools/usa_kissinger_implementation/ART_PROVENANCE.json'
    if write(relative,json.dumps(notice,indent=2)+'\n'):changed.append(relative)
    from .event_art import emit
    return changed+emit()
