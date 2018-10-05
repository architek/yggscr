# -*- coding: utf-8 -*-
import re
from . import exceptions as ygge

links = (
    "2145-filmvidéo",
    "filmvidéo/2178-animation",
    "filmvidéo/2179-animation-serie",
    "filmvidéo/2180-concert",
    "filmvidéo/2181-documentaire",
    "filmvidéo/2182-emission-tv",
    "filmvidéo/2183-film",
    "filmvidéo/2184-serie-tv",
    "filmvidéo/2185-spectacle",
    "filmvidéo/2186-sport",
    "filmvidéo/2187-video-clips",
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
    "jeu+vidéo/2167-autre",
    "jeu+vidéo/2159-linux",
    "jeu+vidéo/2160-macos",
    "jeu+vidéo/2162-microsoft",
    "jeu+vidéo/2163-nintendo",
    "jeu+vidéo/2165-smartphone",
    "jeu+vidéo/2164-sony",
    "jeu+vidéo/2166-tablette",
    "jeu+vidéo/2161-windows",
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

cats = {'Films & Vidéos': 2145, 'Audio': 2139, 'Application': 2144,
        'Jeu vidéo': 2142, 'Ebook': 2140, 'Emulation': 2141,
        'GPS': 2143, 'XXX': 2188}


def get_link(cat, subcat):
    for link in links:
        if cat in link and (not subcat or subcat in link):
            return link
    raise ygge.YggException("Cat or subcat not found in get_link")


def get_cat_id(log, cat, subcat=None):
    log.debug("get_cat_id({},{})".format(cat, subcat))
    if cat == "filmvideo" or cat == "film-vidéo":
        cat = "filmvidéo"
    if cat == "jeu-video" or cat == "jeu-vidéo":
        cat = "jeu+vidéo"
    if subcat == "série-tv":
        subcat = "serie-tv"

    cat_id = ""
    subcat_id = ""
    for link in links:
        if not cat_id and re.findall(r'\d+-%s' % re.escape(cat), link):
            cat_id = re.findall(r'\d+', link)[0]
            log.debug('cat_id {}'.format(cat_id))
            continue
        if cat_id and subcat and "-{}".format(subcat) in link:
            subcat_id = re.findall(r'\d+', link)[0]
            log.debug('subcat_id {}'.format(subcat_id))
            break
    if not cat_id or (subcat and not subcat_id):
        raise ygge.YggException("Cat or subcat not found in get_cat_id")
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


def list_subcats(cat):
    subcats = []
    for link in links:
        if link.startswith(cat):
            subcats.append(link.split('/')[1].split('-', 1)[1])
    return subcats


def list_cats():
    cats = []
    for link in links:
        if '/' not in link:
            cats.append(link.split('-')[1])
    return cats
