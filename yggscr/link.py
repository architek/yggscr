# -*- coding: utf-8 -*-
import re
from . import exceptions as ygge

links = (
    "2145-filmvidéo",
    "filmvideo/2178-animation",
    "filmvideo/2179-animation-serie",
    "filmvideo/2180-concert",
    "filmvideo/2181-documentaire",
    "filmvideo/2182-emission-tv",
    "filmvideo/2183-film",
    "filmvideo/2184-serie-tv",
    "filmvideo/2185-spectacle",
    "filmvideo/2186-sport",
    "filmvideo/2187-video-clips",
    "2139-audio",
    "audio/2147-karaoke",
    "audio/2148-musique",
    "audio/2150-podcast-radio",
    "audio/2149-samples",
    "2144-application",
    "application/2177-autre",
    "application/2176-formation",
    "application/2171-linux",
    "application/2172-macos",
    "application/2174-smartphone",
    "application/2175-tablette",
    "application/2173-windows",
    "2142-jeu+vidéo",
    "jeu-video/2167-autre",
    "jeu-video/2159-linux",
    "jeu-video/2160-macos",
    "jeu-video/2162-microsoft",
    "jeu-video/2163-nintendo",
    "jeu-video/2165-smartphone",
    "jeu-video/2164-sony",
    "jeu-video/2166-tablette",
    "jeu-video/2161-windows",
    "2140-ebook",
    "ebook/2151-audio",
    "ebook/2152-bds",
    "ebook/2153-comics",
    "ebook/2154-livres",
    "ebook/2155-mangas",
    "ebook/2156-presse",
    "2141-emulation",
    "emulation/2157-emulateurs",
    "emulation/2158-roms",
    "2143-gps",
    "gps/2168-applications",
    "gps/2169-cartes",
    "gps/2170-divers",
    "2188-xxx",
    "xxx/2189-films",
    "xxx/2190-hentai",
    "xxx/2191-images")


def get_link(cat, subcat):
    for link in links:
        if cat in link and (subcat or subcat in link):
            return link
    raise ygge.YggException("Cat or subcat not found")


def get_cat_id(cat, subcat=None):
    print("get_cat_id({},{})".format(cat, subcat))
    if cat == "filmvideo":
        cat = "filmvidéo"
    if cat == "jeu-video":
        cat = "jeu+vidéo"
    cat_id = None
    subcat_id = None
    for link in links:
        if cat_id is None and re.findall('\d+-%s' % cat, link):
            cat_id = re.findall(r'\d+', link)[0]
            continue
        if cat_id is not None and subcat and "-{}".format(subcat) in link:
            subcat_id = re.findall(r'\d+', link)[0]
            break
    if cat_id is None or (subcat and subcat_id is None):
        raise ygge.YggException("Cat or subcat not found")
    return {"category": cat_id, "sub_category": subcat_id}


def list_cat_subcat():
    r = ""
    for link in links:
        words = re.findall(r"[a-zA-Zé-]+", link)
        if len(words) > 1:
            if not words[1].startswith('-'):
                continue
            words[1] = words[1][1:]
            r = r + "({}, {}) ".format(words[0], words[1])
    return r
