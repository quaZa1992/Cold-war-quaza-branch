# IMPERIA CW — Cold War: archival photographs for nuclear readiness events.
"""Package individually colourised archival photographs in the native MD frame."""
from pathlib import Path
import argparse
import hashlib
import json
import struct
import textwrap

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps, ImageStat

ROOT = Path(__file__).resolve().parents[2]
ART = Path(__file__).resolve().parent / 'art'
OUT = ROOT / 'gfx/event_pictures/COLDWAR_nuclear_readiness'
REVIEW = ROOT / 'docs/nuclear_readiness/event_art'
PREFIX = 'GFX_COLDWAR_nuclear_readiness_'
FRAME = ROOT / 'gfx/event_pictures/generic/elections/political_deal.dds'

# Each source is an existing archival photograph, never a generated historical scene.
ASSETS = {
    'strategic_command': {
        'file': 'command_post.jpg', 'title': 'Strategic Air Command underground command post',
        'url': 'https://nsarchive2.gwu.edu/nukevault/gallery/image04.htm',
        'creator': 'U.S. Air Force / National Archives, RG 342B, Box 295',
        'date': 'February 1961', 'license': 'Public domain, U.S. federal government photograph',
        'scene': 'Strategic Air Command operations room, February 1961. Muted grey-green consoles, pale projection screens, blue-grey uniforms, restrained tungsten lighting.',
        'center': [0.56, 0.54],
    },
    'civil_defence': {
        'file': 'commons_1812212.png', 'title': 'Basement family fallout shelter with emergency supplies',
        'url': 'https://commons.wikimedia.org/wiki/File:Fallout_shelter_photo.png',
        'creator': 'Office of Civil and Defense Mobilization / National Archives, 542105',
        'date': 'circa 1957; Commons dates the reproduction circa 1960',
        'license': 'Public domain, U.S. federal government photograph',
        'scene': 'Late-1950s civil defence shelter. Natural timber, subdued cream walls, olive-grey bedding, aged paper labels and varied muted food tins. Preserve the checkered cloth and every shelf.',
    },
    'missile_warning': {
        'file': 'commons_15768847.jpg', 'title': 'Atlas missiles on alert at Vandenberg Air Force Base',
        'url': 'https://commons.wikimedia.org/wiki/File:Atlas_missiles_on_alert_at_Vandenberg_Air_Force_Base_-_1960.jpg',
        'creator': 'U.S. Air Force', 'date': '1960', 'license': 'Public domain, U.S. federal government photograph',
        'scene': 'Atlas missile alert positions at Vandenberg in 1960. Silver metal missiles and bomber, dark gantries, sun-bleached concrete and scrub, subdued blue sky. The missiles stand upright; none is launching.',
    },
    'counter_alert': {
        'file': 'commons_51999114.jpg', 'title': 'B-52 ground-alert crew running to their aircraft',
        'url': 'https://commons.wikimedia.org/wiki/File:B-52_Ground_alert.jpg',
        'creator': 'U.S. Air Force', 'date': 'circa 1970', 'license': 'Public domain, U.S. federal government photograph',
        'scene': 'B-52H 60-0031 on ground alert circa 1970. Subdued period bomber camouflage, pale lower surfaces, olive flight suits, neutral concrete. Keep every crew member, the exact nose and all engines in their original positions.',
        'center': [0.45, 0.54],
    },
    'crisis_communications': {
        'file': 'commons_22384179.jpg', 'title': 'Washington-Moscow hotline teletype terminal room',
        'url': 'https://commons.wikimedia.org/wiki/File:Hotlineroom.jpg',
        'creator': 'White House / National Security Agency',
        'date': 'Undated historic photograph; reproduction metadata is dated 10 May 2005',
        'license': 'Public domain, U.S. federal government photograph',
        'scene': 'Historic hotline teletype operators in a communications room. Warm off-white paper, grey-green and beige electromechanical terminals, muted period civilian clothing and natural skin tones. These are teleprinters, not telephones. Preserve the existing cropped framing of the standing operator.',
    },
    'mutual_standdown': {
        'file': 'commons_192799779.jpg', 'title': 'Signing of the ABM Treaty and interim SALT agreement',
        'url': 'https://commons.wikimedia.org/wiki/File:President_Richard_Nixon_and_General_Secretary_Leonid_Brezhnev_signing_the_ABM_Treaty.jpg',
        'creator': 'White House Photo Office / National Archives', 'date': '26 May 1972',
        'license': 'Public domain, U.S. federal government photograph', 'already_colour': True,
        'center': [0.48, 0.60],
    },
    'diplomatic_venue': {
        'file': 'commons_67124360.jpg', 'title': 'Vienna venue associated with the 1970 SALT negotiations',
        'url': 'https://commons.wikimedia.org/wiki/File:SALT-conferentie_16_april_aanstaande_in_Wenen_tussen_USSR_USA_over_beperking_str,_Bestanddeelnr_923-3982.jpg',
        'creator': 'Anefo / Nationaal Archief, photograph 923-3982', 'date': '1 April 1970',
        'license': 'CC0 1.0', 'license_url': 'https://creativecommons.org/publicdomain/zero/1.0/',
        'scene': 'Vienna diplomatic building photographed in April 1970, associated with the SALT talks. Muted pale stone, dark winter branches, natural paving, softly overcast light. Preserve every window and the exact building facade.',
    },
    'strategic_situation': {
        'file': 'command_display.jpg', 'title': 'Strategic Air Command situation displays and television facilities',
        'url': 'https://nsarchive2.gwu.edu/nukevault/gallery/image03.htm',
        'creator': 'U.S. Air Force / National Archives, RG 342B, Box 295',
        'date': 'February 1961', 'license': 'Public domain, U.S. federal government photograph',
        'scene': 'Strategic Air Command situation displays in February 1961. Muted cream map boards, pale blue and beige cartography, grey cameras and consoles, blue-grey uniforms. Preserve the television cameras, map markings and every person.',
        'center': [0.48, 0.38],
    },
    'security_consultation': {
        'file': 'commons_16455340.tif', 'title': 'National Security Council meeting',
        'input_file': 'security_consultation_input.png',
        'url': "https://commons.wikimedia.org/wiki/File:First_meeting_of_the_President%27s_National_Security_Council_-_NARA_-_194279.tif",
        'creator': 'White House photographic collection / National Archives, 194279',
        'date': '21 January 1969', 'license': 'Public domain, U.S. federal government photograph',
        'scene': 'National Security Council meeting on 21 January 1969. Dark period business suits, natural skin, polished brown conference table, cream walls, muted upholstery. Preserve all identities, seated positions, documents and the room layout. Remove no person.',
        'trim': [0.015, 0.015, 0.985, 0.965],
    },
    'nuclear_detonation': {
        'file': 'atomic_cloud.gif', 'title': 'Operation Cue nuclear cloud',
        'input_file': 'atomic_cloud_input.png',
        'url': 'https://www.archives.gov/education/lessons/fallout-docs',
        'creator': 'Office of Civil and Defense Mobilization / National Archives, 541787',
        'date': '5 May 1955', 'license': 'Public domain, U.S. federal government photograph',
        'scene': 'Operation Cue test cloud, Nevada, 5 May 1955. Dusty grey-brown mushroom cloud, subdued blue sky, dry brown desert, muted observer clothing. The distant cloud is already formed: do not add a fireball, flames, cities, casualties or extra explosions.',
        'trim': [0.012, 0.012, 0.988, 0.988],
    },
    'nuclear_aftermath': {
        'file': 'blast_aftermath.gif', 'title': 'Operation Cue test house after the blast',
        'input_file': 'blast_aftermath_input.png',
        'url': 'https://www.archives.gov/education/lessons/fallout-docs',
        'creator': 'Office of Civil and Defense Mobilization / National Archives, 541788',
        'date': '5 May 1955', 'license': 'Public domain, U.S. federal government photograph',
        'scene': 'Damaged test house after Operation Cue, Nevada, May 1955. Weathered pale timber, exposed dark brown wood, dusty tan desert, muted blue-grey sky. Preserve exactly the existing damage, the two-storey structure and distant landscape. No flames, smoke, people, gore or additional destruction.',
        'trim': [0.012, 0.012, 0.988, 0.988],
    },
    'intelligence_assessment': {
        'file': 'aerial_recon.jpg', 'title': 'U-2 reconnaissance photograph of missile deployment in Cuba',
        'url': 'https://commons.wikimedia.org/wiki/File:U-2_photo_during_Cuban_Missile_Crisis.jpg',
        'creator': 'U.S. Air Force; photograph taken by Major Steve Heyser',
        'date': '14 October 1962', 'license': 'Public domain, U.S. federal government photograph',
        'scene': 'U-2 reconnaissance photograph of the missile deployment near San Cristobal, Cuba, 14 October 1962. Very restrained olive vegetation, tan tracks and grey structures. Preserve all aerial details, shadows, printed annotation marks and their exact registration. Keep a technical photographic character, not a painted map.',
    },
}

EVENT_ART = {
    1: 'strategic_command', 2: 'civil_defence', 3: 'missile_warning',
    4: 'counter_alert', 5: 'crisis_communications', 6: 'mutual_standdown',
    7: 'diplomatic_venue', 8: 'strategic_command', 9: 'diplomatic_venue',
    10: 'strategic_situation', 11: 'security_consultation',
    12: 'nuclear_detonation', 13: 'nuclear_aftermath', 14: 'intelligence_assessment',
    15: 'missile_warning', 16: 'strategic_command', 17: 'counter_alert',
    18: 'strategic_situation', 19: 'diplomatic_venue', 20: 'diplomatic_venue',
    21: 'strategic_situation',
}


def prompts():
    base = (
        'Use case: identity-preserve. Asset type: archival photograph for a Cold War strategy-game event. '
        'Input image 1 is the edit target. Colourise this exact archival photograph conservatively; '
        'preserve its photographic grain, lighting, composition, perspective, all human identities and '
        'poses, object counts, equipment silhouettes and existing details. Change only colour and '
        'gently restore scan clarity. Use credible, restrained period colours with natural materials; '
        'retain realistic contrast and fine photographic texture. Keep the exact original framing and '
        'aspect ratio, including any subjects cropped by the original. No new people, objects, scenery, '
        'lettering, captions, logos, watermarks, decorative borders or cinematic effects. Do not '
        'reinterpret the scene or turn it into an illustration. '
    )
    return {slug: base + a['scene'] for slug, a in ASSETS.items() if not a.get('already_colour')}


def registry_source():
    return 'spriteTypes = {\n' + ''.join(
        f'spriteType = {{ name = "{PREFIX}{slug}" '
        f'texturefile = "gfx/event_pictures/COLDWAR_nuclear_readiness/{slug}.dds" }}\n'
        for slug in ASSETS) + '}\n'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export():
    OUT.mkdir(parents=True, exist_ok=True)
    REVIEW.mkdir(parents=True, exist_ok=True)
    frame = Image.open(FRAME).convert('RGBA')
    assert frame.size == (217, 163), frame.size
    records = []
    previews = {}
    downloads = json.loads((ART/'source/download_urls.json').read_text(encoding='utf-8'))
    for slug, asset in ASSETS.items():
        source = ART / 'source' / asset['file']
        master = source if asset.get('already_colour') else ART / 'colourised' / (slug + '.png')
        assert master.is_file(), f'Missing colourised master: {master}'
        photo = ImageOps.exif_transpose(Image.open(master)).convert('RGB')
        if 'trim' in asset:
            photo = photo.crop(tuple(round(n * photo.size[i % 2]) for i, n in enumerate(asset['trim'])))
        photo = ImageOps.fit(photo, (180, 150), Image.Resampling.LANCZOS,
                             centering=tuple(asset.get('center', [0.5, 0.5])))
        spread = sum(ImageStat.Stat(ImageChops.difference(photo.getchannel('R'), photo.getchannel('B'))).mean)
        assert spread > 1, f'Expected colour photograph: {slug}'
        image = frame.copy()
        image.paste(photo.convert('RGBA'), (19, 6))
        assert all(image.getpixel((x,y)) == frame.getpixel((x,y))
                   for y in range(163) for x in range(217)
                   if not (19 <= x < 199 and 6 <= y < 156)), slug
        pixels = image.tobytes()
        header = [124,4111,163,217,217*4,0,0]+[0]*11+[32,65,0,32,255,65280,16711680,4278190080,4096,0,0,0,0]
        output = OUT / (slug + '.dds')
        output.write_bytes(b'DDS ' + struct.pack('<31I', *header) + pixels)
        assert Image.open(output).convert('RGBA').tobytes() == pixels, slug
        preview = REVIEW / (slug + '.png')
        image.save(preview)
        previews[slug] = image
        records.append(dict(asset, slug=slug, source=str(source.relative_to(ROOT)),
                            source_sha256=sha(source), master=str(master.relative_to(ROOT)),
                            download_url=downloads[asset['file']],
                            master_sha256=sha(master), output=str(output.relative_to(ROOT)),
                            output_sha256=sha(output), size=[217,163], inset=[19,6,180,150],
                            colourised=not asset.get('already_colour',False),
                            method='Original colour photograph' if asset.get('already_colour') else 'Built-in ImageGen colourisation',
                            frame_pixels_unchanged=True, decoded_dds_matches_preview=True))
    manifest = {'assets': records, 'event_pictures': {f'cw_nuclear.{i}':PREFIX+s for i,s in EVENT_ART.items()},
                'frame_source':str(FRAME.relative_to(ROOT)), 'frame_sha256':sha(FRAME),
                'note':'Archival illustrations; colours are interpretive restorations, not historical colour evidence.'}
    (REVIEW/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    credits = ['# Nuclear readiness event photographs', '',
               'Archival photographs selected from online collections. Eleven monochrome originals were individually colourised with built-in ImageGen; the SALT signing photograph retains its original colour. Colours are interpretive restorations. Native MD framing and proportional crops were applied after colourisation.', '',
               'Historical subjects illustrate the event themes for all countries; the photographs do not identify the governments participating in a particular campaign.', '',
               '| Photograph | Date | Creator and collection | Rights |', '|---|---|---|---|']
    for a in records:
        credits.append(f"| [{a['title']}]({a['url']}) | {a['date']} | {a['creator']} | {a['license']} |")
    credits += ['', 'The U.S. Air Force photographs hosted by the National Security Archive are from National Archives RG 342B; see the [gallery provenance](https://nsarchive2.gwu.edu/nukevault/gallery/index.htm). The Vienna photograph is available under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).', '',
                'Original downloads and repository metadata: `tools/nuclear_readiness/art/source/`. Colourisation prompts: `tools/nuclear_readiness/art/prompts.json`. Colourised masters: `tools/nuclear_readiness/art/colourised/`.', '']
    credits += ['Installed game textures: `gfx/event_pictures/COLDWAR_nuclear_readiness/`. Event-to-sprite bindings and file hashes are recorded in [manifest.json](manifest.json). The complete framed set is shown in [contact_sheet.png](contact_sheet.png).', '']
    (REVIEW/'CREDITS.md').write_text('\n'.join(credits),encoding='utf-8')
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf',14)
    title_font = ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf',15)
    sheet = Image.new('RGB',(1000,((len(EVENT_ART)+3)//4)*244+56),'#17202a')
    draw = ImageDraw.Draw(sheet)
    draw.text((20,15),'NUCLEAR READINESS — EVENT PHOTOGRAPHS',font=title_font,fill='#e5d7b5')
    for index,(ident,slug) in enumerate(EVENT_ART.items()):
        x=(index%4)*250+16;y=(index//4)*244+55
        image=previews[slug];sheet.paste(image,(x,y),image)
        title=f'{ident:02d}  {ASSETS[slug]["title"]}'
        draw.multiline_text((x,y+169),'\n'.join(textwrap.wrap(title,29))[:130],font=font,fill='#dbe1e6',spacing=2)
    sheet.save(REVIEW/'contact_sheet.png')
    print(f'Exported {len(records)} colour event photographs for {len(EVENT_ART)} events; native frames and DDS pixels verified.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prompts',action='store_true')
    args = parser.parse_args()
    if args.prompts:
        ART.mkdir(parents=True,exist_ok=True)
        (ART/'prompts.json').write_text(json.dumps(prompts(),indent=2)+'\n',encoding='utf-8')
        print('Wrote 11 individual colourisation prompts.')
    else:
        export()
