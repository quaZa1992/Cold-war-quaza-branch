# IMPERIA COLD WAR — Native masked-flag assets and offline review fixtures.
from pathlib import Path
from PIL import Image,ImageOps

GAME=Path('E:/SteamLibrary/steamapps/common/Hearts of Iron IV')
MD=Path('E:/SteamLibrary/steamapps/workshop/content/394360/2777392649')


def asset_path(root,relative):
    return next((base/relative for base in [root,MD,GAME] if (base/relative).exists()),root/relative)


def preview_flag(root,m,expression,sprite,first):
    """Offline fixture only. Runtime uses the engine's current GetFlag value.

    These fixture identities follow the supplied 1970 history files. The native
    renderer, not this dictionary, handles later ideology/cosmetic-tag changes.
    """
    target=expression.strip('"')[2:].removesuffix('.GetFlag]')
    country=m.c if target in ['THIS','ROOT'] else m.country('var:'+target)
    assert country is not None,'Visible flag has no country: '+expression
    cosmetic={'SOV':'SOV_Coldwar_Communism','DDR':'DDR_DDR','POL':'POL_communist','FRA':'FRA_1970'}.get(country.tag,country.tag)
    ideology='communism' if country.tag in ['SOV','DDR','POL'] else 'democratic'
    names=[cosmetic+'_'+ideology,cosmetic,country.tag+'_'+ideology,country.tag]
    path=next((asset_path(root,'gfx/flags/'+name+'.tga') for name in names if asset_path(root,'gfx/flags/'+name+'.tga').exists()),None)
    assert path,'No flag source for review country '+country.tag
    overlay=Image.open(asset_path(root,first(sprite,'textureFile1').strip('"'))).convert('RGBA')
    mask=Image.open(asset_path(root,first(sprite,'textureFile2').strip('"'))).convert('RGBA')
    result=ImageOps.fit(Image.open(path).convert('RGBA'),overlay.size,method=Image.Resampling.LANCZOS)
    result.putalpha(mask.getchannel('A'));result.alpha_composite(overlay)
    return result
