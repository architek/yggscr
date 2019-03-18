#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018-2019, Laurent Kislaire.
# See /LICENSE for licensing information.


import pytest
import yggscr.shout


# 20s test
@pytest.mark.timeout(20)
def test_shout_main():
    ' Testing shout script for 20s '
    print("Testing for 20s")
    try:
        yggscr.shout.main([])
    except Exception:
        assert 0
    except:
        pass
