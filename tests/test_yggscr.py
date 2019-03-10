#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018-2019, Laurent Kislaire.
# See /LICENSE for licensing information.


import pytest
import logging
import time
import sys
import robobrowser
import requests
from mock import patch, Mock
from src.yggscr.exceptions import YggException, LoginFailed
import src.yggscr.ygg
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


def test_core():
    """Test search."""
    s = Stats()
    s.add([('10.5', 'T'), ('8.2', 'G')])
    s.add([('1', 'G'), ('8.2', 'T')])
    s = SBrowser(parser='html.parser')
    print("{}".format(s))
    s.proxify("socks5h://user:pass@127.0.0.1:port")
    print(s.parsed())
    y = src.yggscr.ygg.YggBrowser()
    y.download_torrent(id=41909)
    y.next_torrents()
    y.cat_subcat()
    with pytest.raises(Exception):
        y.get_stats()
    y.login()
    ts = y.search_torrents(q={'name': 'cyber'})
    for t in ts:
        print(t)
    y.logout()
    for _ in range(1, 4):
        with pytest.raises(src.yggscr.ygg.LoginFailed):
            y.login("a b")
        time.sleep(1)
    with pytest.raises(src.yggscr.ygg.TooManyFailedLogins):
        y.login("a b")


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


def test_shout_diff():
    y = YggShout()
    y.get_shouts()
    y.do_diff()     # set last_shouts

    time.sleep(2)
    y.get_shouts()  # set new_shouts
    del y.new_shouts[1]
    success = False
    for removed, shout in y.do_diff():
        if removed:
            shout.message += "<-- REMOVED"
            success = True
        print(shout)
    assert success


# 20s test
@pytest.mark.timeout(20)
def test_shout_main():
    try:
        main_shout([])
    except: #noqa
        pass


@pytest.mark.skipif(sys.version_info[:2] == (3, 5), reason="python3.5 doesn't have tmp_path")
def test_shout2(tmp_path):
    f = tmp_path / "foo.txt"
    f.write_text("""
    <li use="2" data-id="3087">
     <a href="/forum/index.php?members/allain6610.522/" class="avatar avatar--xxs" data-user-id="522" data-xf-init="member-tooltip" id="js-XFUniqueId20">
     <img src="/forum/data/avatars/s/0/522.jpg?1530742137" alt="Allain6610" class="avatar-u522-s" itemprop="image">
     </a>
     <a href="/forum/index.php?members/allain6610.522/" class="username" dir="auto" data-user-id="522" data-xf-init="member-tooltip" user-group-id="2" id="js-XFUniqueId21">Allain6610</a>:
     <span><div class="bbWrapper"><a href="https://ww1.yggtorrent.is/forum/index.php?members/18575/" class="username" data-xf-init="member-tooltip" data-user-id="18575" data-username="Mycke3131" id="js-XFUniqueId22">Mycke3131</a> <b>Fonctions en attente de mise a jour :</b><ul>
      <li>Les MP sur le forum</li>
      <li>Les Trophees sur le forum auront une utilité</li>
      <li>Le bouton "Signaler" dans les torrents (ecrire a <a href="mailto:contact@ygg.is">contact@ygg.is</a> ou voir un TP sur la shout)</li>
      <li>Editer/Supprimer dans l'historique de telechargement</li>
      </ul></div></span>
      <time class="u-dt" dir="auto" datetime="2018-07-16T14:58:54+0100" data-time="1531749534" data-date-string="16/7/18" data-time-string="14:58" title="16/7/18, à 14:58">il y a 33 minutes</time>
    </li>
    """)
    main_shout(["foo", str(f)])
    with patch("src.yggscr.shout.sys.exit") as mock_exit:
        main_shout(["foo", "nonexistent"])
        assert mock_exit.call_args[0][0] == 1
        main_shout(None)
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


def test_sbrowser_failures():
    # Initialise
    s = SBrowser()
    s.open("http://example.com")

    # Verify example doesn't use CF
    assert s.is_cloudflare() is False
    print(s.is_cloudflare())

    # Generate exception on cfscrape, verify internal handling of RoboError
    with patch("cfscrape.CloudflareScraper.is_cloudflare_challenge",
               side_effect=robobrowser.exceptions.RoboError()):
        print(s.is_cloudflare())
    # Generate unhandled exception on cfscrape, verify exception raised
    with patch("cfscrape.CloudflareScraper.is_cloudflare_challenge",
               side_effect=Exception("!")):
        with pytest.raises(Exception):
            print(s.is_cloudflare())

    s = SBrowser()
    s.connection_details()
    with patch("robobrowser.RoboBrowser.open", side_effect=requests.exceptions.ProxyError()):
        assert s.connection_details() == {'ip': 'Unknown'}
    with patch("robobrowser.RoboBrowser.open", side_effect=requests.exceptions.ConnectionError):
        assert s.connection_details() == {'ip': 'Unknown'}
    with patch("robobrowser.RoboBrowser.open", side_effect=ValueError()):
        assert s.connection_details() == {'ip': 'Unknown'}
    with patch("robobrowser.RoboBrowser.open", side_effect=Exception()):
        assert s.connection_details() == {'ip': 'Unknown'}


def test_shout_failures():
    # Long test of 1 retry: 16+31 (47s)
    # Long test of 2 retries: 16+31+46 (93s)
    N_MAXTRIES = 1
    with patch("src.yggscr.shout.YggShout.get_shouts", side_effect=requests.exceptions.Timeout):
        with pytest.raises(YggException):
            main_loop(N_MAXTRIES)
            assert 0
    main_loop(2)
