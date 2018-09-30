#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018, Laurent Kislaire.
# See /LICENSE for licensing information.


from src.yggscr.shell import YggShell


def test_shell():
    """Test shell."""
    y = YggShell()
    y.do_exclus("")
    y.do_search_torrents("q:cyber c:film n:2 d:True")
    y.do_top_day("")
    y.do_print("")
    y.do_response("")
    y.do_ping("")
    y.do_proxify("")
