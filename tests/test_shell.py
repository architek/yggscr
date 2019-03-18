#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018-2019, Laurent Kislaire.
# See /LICENSE for licensing information.


import pytest
import mock
import requests
import yggscr.shell
import yggscr.exceptions
import yggscr.ygg


def test_shell_login():
    y = yggscr.shell.YggShell()
    y.do_logout("")
    with pytest.raises(yggscr.ygg.LoginFailed):
        y.do_login('test test')
    y.do_login("")
    y.do_logout("")

    y.do_logout("")
    with pytest.raises(yggscr.ygg.YggException):
        y.do_stats("")
    y.do_login("Pepeh70 Diabolo")
    y.ygg_browser.download_torrent(torrent_id=41909)
    y.do_stats("")
    with mock.patch("yggscr.ygg.YggBrowser.get_stats", side_effect=requests.exceptions.RequestException("Net")):
        y.do_stats("")
    with pytest.raises(Exception):
        y.do_login("Pepeh70 Diabolo")
    y.do_logout("")


def test_shell_core():
    """Test shell."""
    y = yggscr.shell.YggShell(ygg_browser=mock.MagicMock())
    y = yggscr.shell.YggShell()
    y.do_open('http://www.example.org')
    y.do_print("")
    y.do_response("")
    y.do_ping("")
    y.do_proxify("https://192.168.1.1:9000 FOO")
    y.do_proxify("https://192.168.1.1:9000")
    y.do_proxify("")
    y.do_lscat("")
