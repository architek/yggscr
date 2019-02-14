#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018, Laurent Kislaire.
# See /LICENSE for licensing information.


import pytest
from src.yggscr.exceptions import YggException
from src.yggscr.ygg import YggBrowser, Stats
from src.yggscr.sbrowser import SBrowser
from src.yggscr.shout import ShoutMessage, YggShout
from src.yggscr.torrents import htn, Torrent
from src.yggscr.client import rtorrent_add_torrent, transmission_add_torrent, deluge_add_torrent, exec_cmd
from src.yggscr.link import list_cats, list_subcats, get_link, get_cat_id, list_cat_subcat, cat_subcat_from_href


def test_link():
    with pytest.raises(YggException):
        get_link('filmvidéo', 'emission_tv')
    get_link('filmvidéo', 'emission-tv')
    get_cat_id('jeu-vidéo', 'tablette')
    get_cat_id('film-vidéo', 'série-tv')
    list_cat_subcat()
    with pytest.raises(YggException):
        get_cat_id('jeu_vidéo', 'foo')
    cat_subcat_from_href('')
    for c in list_cats():
        a = ','.join('"' + e + '"' for e in list_subcats(c))
        print('cat["'+c+'"]=['+a+'];')


def test_ygg():
    """Test search."""
    s = Stats()
    s.add([('10.5', 'T'), ('8.2', 'G')])
    s.add([('1', 'G'), ('8.2', 'T')])
    s = SBrowser(parser='html.parser')
    print("{}".format(s))
    s.proxify("socks5h://user:pass@127.0.0.1:port")
    print(s.parsed())
    y = YggBrowser()
    y.download_torrent()
    y.next_torrents()
    y.login()
# FIXME    with pytest.raises(YggException, match=r"Not logged in"):
#        y.get_stats()
    y.logout()
    ts = y.search_torrents(q={'name': 'cyber'})
    for t in ts:
        print(t)


def test_client():
    """Test bt client"""
    try:
        rtorrent_add_torrent("http://127.0.0.1/RPC2", b'0')
    except: #noqa
        pass

    try:
        rtorrent_add_torrent("http://127.0.0.1/RPC2", None, 'foo.torrent')
    except: #noqa
        pass

    with pytest.raises(ValueError):
        rtorrent_add_torrent("http://127.0.0.1/RPC2")

    try:
        transmission_add_torrent("127.0.0.1", 65432, "user", "pass", b'0')
    except: #noqa
        pass

    try:
        deluge_add_torrent("127.0.0.1", 65432, "user", "pass", b'0')
    except: #noqa
        pass

    exec_cmd("ls .")


def test_shout():
    s = ShoutMessage(True)
    s = ShoutMessage(True, None, 1, 1, 1, "message")
    print("{}".format(s))
    s = YggShout()
    print("{}".format(s))


def test_torrents():
    htn("12")
    t = Torrent("title", "12", "1970", "12GO", "12", "12", "12", "http://test/foo/bar/baz")
    t = Torrent("title", "12", "1970", "12GO", "12", "12", "12", href=None, tid="12", cat="12")
    t.get_dl_link()
    t.set_tref('plop')
    t.set_id('12')
