#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018, Laurent Kislaire.
# See /LICENSE for licensing information.


import pytest
import logging
import time
import sys
from mock import patch, Mock
from src.yggscr.exceptions import YggException
from src.yggscr.ygg import YggBrowser
from src.yggscr.stats import Stats
from src.yggscr.sbrowser import SBrowser
from src.yggscr.shout import ShoutMessage, YggShout, main_loop, main as main_shout
from src.yggscr.torrents import htn, Torrent
from src.yggscr.client import rtorrent_add_torrent, transmission_add_torrent, deluge_add_torrent, exec_cmd
from src.yggscr.link import list_cats, list_subcats, get_link, get_cat_id, list_cat_subcat, cat_subcat_from_href
from src.yggscr.const import get_dl_link, detect_redir
from transmissionrpc.error import TransmissionError


def test_link():
    with pytest.raises(YggException):
        get_link('filmvidéo', 'emission_tv')
    get_link('filmvidéo', 'emission-tv')
    get_cat_id('jeu-vidéo', 'tablette')
    get_cat_id('jeu-vidéo', 'tablette')
    get_cat_id('film-vidéo', 'série-tv')
    log = logging.getLogger()
    get_cat_id('jeu-vidéo', 'tablette', log)
    get_cat_id('jeu-vidéo', 'tablette', log)
    get_cat_id('film-vidéo', 'série-tv', log)
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
    with pytest.raises(Exception):
        y.get_stats()
    y.login()
    y.logout()
    ts = y.search_torrents(q={'name': 'cyber'})
    for t in ts:
        print(t)


def test_client1():
    """Test bt client"""
    try:
        rtorrent_add_torrent("http://127.0.0.1/RPC2", b'0')
    except ConnectionRefusedError:
        pass

    with pytest.raises(ValueError):
        rtorrent_add_torrent("http://127.0.0.1/RPC2")

    try:
        transmission_add_torrent("127.0.0.1", 65432, "user", "pass", b'0')
    except TransmissionError:
        pass

    with patch("src.yggscr.client.tclient"):
        transmission_add_torrent("127.0.0.1", 65432, "user", "pass", b'0')

    try:
        deluge_add_torrent("127.0.0.1", 65432, "user", "pass", b'0')
    except ConnectionRefusedError:
        pass

    with patch("src.yggscr.client.DelugeRPCClient"):
        deluge_add_torrent("127.0.0.1", 65432, "user", "pass", b'0')

    exec_cmd("ls .")


@pytest.mark.skipif(sys.version_info[:2] == (3, 5), reason="python3.5 doesn't have tmp_path")
def test_client2(tmp_path):
    try:
        f = tmp_path / "foo.torrent"
        f.write_bytes(b'00')
        rtorrent_add_torrent("http://127.0.0.1/RPC2", None, str(f))
    except ConnectionRefusedError:
        pass


def test_shout1():
    s = ShoutMessage(True)
    s = ShoutMessage(True, None, 1, 1, 1, "message")
    print("{}".format(s))
    s = YggShout()
    print("{}".format(s))
    main_loop()
    time.sleep(2)
    main_loop()


@pytest.mark.skipif(sys.version_info[:2] == (3, 5), reason="python3.5 doesn't have tmp_path")
def test_shout2(tmp_path):
    f = tmp_path / "foo.txt"
    f.write_text("")
    main_shout(["foo", str(f)])
    with patch("src.yggscr.shout.sys.exit") as mock_exit:
        main_shout(["foo", "nonexistent"])
        assert mock_exit.call_args[0][0] == 1


def test_torrents():
    htn("12")
    t = Torrent("title", "12", "1970", "12GO", "12", "12", "12", "http://test/foo/bar/baz")
    t = Torrent("title", "12", "1970", "12GO", "12", "12", "12", href=None, tid="12", cat="12")
    t.get_dl_link()
    t.set_tref('plop')
    t.set_id('12')


def _mock_response(status=200, headers=None):
        mock_resp = Mock()
        mock_resp.status_code = status
        mock_resp.headers = headers
        return mock_resp


@patch('requests.get')
def test_more(mock_get):
    get_dl_link(42)
    detect_redir()
    mock_resp = _mock_response(status=301, headers={'Location': 'https://wtf.yggtorrent.gg'})
    mock_get.return_value = mock_resp
    detect_redir()
