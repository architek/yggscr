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


def test_shell_search():
    y = yggscr.shell.YggShell()
    y.print_torrents([], n=1)
    assert y.kv_to_dict("foo:bar") == {"foo": "bar"}
    assert y.kv_to_dict("foo:bar foo:baz alice:bob") == {"foo": ["bar", "baz"], "alice": "bob"}
    y.do_search_torrents("q:pour")
    y.do_next("n:3")
    y.do_next("")
    y.do_search_torrents("q:tunexistepas c:film n:2 d:True")
    y.do_next("")
    y.do_search_torrents("q:cyber d:True")
    y.do_search_torrents("q:cyber d:True foo:1 foo:2 foo:3")
    with pytest.raises(Exception):
        y.do_next("foo:3")
    with pytest.raises(Exception):
        y.do_next("n:foo")
    with pytest.raises(Exception):
        y.do_search_torrents("foo:foo")
    with pytest.raises(Exception):
        y.do_search_torrents("foo")


def test_shell_top():
    y = yggscr.shell.YggShell()
    y.do_top_day("")
    y.do_top_week("")
    y.do_top_month("")
    y.do_exclus("")


def test_shell_failures():
    y = yggscr.shell.YggShell()
    y.do_login("")
    with mock.patch("yggscr.ygg.YggBrowser.login", side_effect=requests.exceptions.RequestException("Net")):
        y.do_login("a b")
    with mock.patch("yggscr.ygg.YggBrowser.__str__", side_effect=requests.exceptions.RequestException("Net")):
        y.do_print("")
    with mock.patch("yggscr.ygg.YggBrowser.search_torrents", side_effect=requests.exceptions.RequestException("Net")):
        y.do_search_torrents("q:cyber")
    with pytest.raises(yggscr.exceptions.YggException):
        y.do_search_torrents("cyber")
