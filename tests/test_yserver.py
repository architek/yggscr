#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018-2019, Laurent Kislaire.
# See /LICENSE for licensing information.


from src.yserver.core import YggServer


def test_new():
    y = YggServer("conf/yserver.cfg") #noqa
