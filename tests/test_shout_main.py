#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018-2019, Laurent Kislaire.
# See /LICENSE for licensing information.


import pytest
from src.yggscr.shout import main as main_shout

# 20s test
@pytest.mark.timeout(20)
def test_shout_main():
    print("Testing for 20s")
    try:
        main_shout([])
    except:
        pass
