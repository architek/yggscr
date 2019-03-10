#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018-2019, Laurent Kislaire.
# See /LICENSE for licensing information.


import src.yggscr
import src.yggscr.shell
import src.yserver.core


def test_import_yshell():
    """Test imports."""

    s = src.yggscr.shell.YggShell()
    assert isinstance(s, src.yggscr.shell.YggShell)
