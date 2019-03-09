#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018, Laurent Kislaire.
# See /LICENSE for licensing information.


import pytest
import mock
from src.yggscr.shell import YggShell
import src.yggscr.exceptions
import src.yggscr.ygg


def test_shell_login():
    y = YggShell()
    y.do_logout("")
    with pytest.raises(src.yggscr.ygg.LoginFailed):
        y.do_login('test test')
    y.do_login("")
    y.do_logout("")

    y.do_logout("")
    with pytest.raises(src.yggscr.ygg.YggException):
        y.do_stats("")
    y.do_login("Pepeh70 Diabolo")
    y.do_stats("")
    with pytest.raises(Exception):
        y.do_login("Pepeh70 Diabolo")
    y.do_logout("")


def test_shell_core():
    """Test shell."""
    y = YggShell(ygg_browser=mock.MagicMock())
    y = YggShell()
    y.do_open('http://www.example.org')
    y.do_print("")
    y.do_response("")
    y.do_ping("")
    y.do_proxify("https://192.168.1.1:9000 FOO")
    y.do_proxify("https://192.168.1.1:9000")
    y.do_proxify("")
    y.do_lscat("")


def test_shell_search():
    y = YggShell()
    y.print_torrents([], n=1)
    y.do_search_torrents("q:pour")
    y.do_next("n:3")
    y.do_next("")
    y.do_search_torrents("q:tunexistepas c:film n:2 d:True")
    y.do_next("")
    with pytest.raises(Exception):
        y.do_next("foo:3")
    with pytest.raises(Exception):
        y.do_next("n:foo")
    with pytest.raises(Exception):
        y.do_search_torrents("foo:foo")
    with pytest.raises(Exception):
        y.do_search_torrents("foo")
    y.do_search_torrents("q:cyber d:True")


def test_shell_top():
    y = YggShell()
    y.do_top_day("")
    y.do_top_week("")
    y.do_top_month("")
    y.do_exclus("")
