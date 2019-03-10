#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018-2019, Laurent Kislaire.
# See /LICENSE for licensing information.


import src.yggscr
import src.yggscr.shell
import src.yserver.core
import src.yggscr.__main__


def test_import_yggscr():
    """Test imports."""
    src.yggscr
    src.yggscr.__main__.main()


def test_import_yserver():
    """Test imports."""

    src.yserver


def test_import_yshell():
    """Test imports."""

    s = src.yggscr.shell
    # assert isinstance(s, src.yggscr.shell.YggShell)
