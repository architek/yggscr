#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018, Laurent Kislaire.
# See /LICENSE for licensing information.


from src.yggscr.ygg import YggBrowser


def test_search():
    """Test search."""
    y = YggBrowser()
    ts = y.search_torrents(q={'name': 'cyber'})
    for t in ts:
        print(t)
