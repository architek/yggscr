#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018-2019, Laurent Kislaire.
# See /LICENSE for licensing information.

import pytest
import yggscr
import yggscr.shell
import yserver.core


def test_instance_yshell():
    """Test imports."""

    s = yggscr.shell.YggShell()
    assert isinstance(s, yggscr.shell.YggShell)


def test_import_yserver():
    """Test imports."""

    with pytest.raises(FileNotFoundError):
        c = yserver.core.YggServer()
