# IMPERIA CW — Cold War: current delivery geometry and native-art preview.
"""Render the effective revision without mutating icon assignments or old concepts."""
from PIL import Image
import COLDWAR_KOR_render as r
from COLDWAR_KOR_alliance_revision import load_design

def main():
    r.D=load_design()
    for family,source in r.SOURCES.items():
        im=Image.open(r.ROOT/source).convert('RGBA')
        im.thumbnail((94,90),Image.Resampling.LANCZOS)
        r.IMG[family]=im
    for groups,path,title,scale in (
        (['usfk'],'COLDWAR_KOR_USFK_detail.png','US FORCES KOREA',1),
        (['defence','foreign','usfk'],'COLDWAR_KOR_Alliance_neighbours.png','DEFENCE AND FOREIGN POLICY',1),
        ([g['id'] for g in r.D['groups']],'COLDWAR_KOR_delivery_entire_tree.png','SOUTH KOREA — JANUARY 1970',.35)):
        r.image_view(groups,path,title=title,scale=scale,
            subtitle='DELIVERY PREVIEW · Native grid and art · Fonts and connectors approximate')
        print(path)

if __name__=='__main__':main()
