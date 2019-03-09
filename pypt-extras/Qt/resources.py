# -*- encoding: utf-8 -*-
# Ygg Scraper v0.1.0
# Yggtorrent scraper library - Webserver - Rss - Shell
# Copyright © 2018-2019, Laurent Kislaire.
# See /LICENSE for licensing information.
# This file was adapted from Chris Warrick’s Python Project Template.

"""
Adapt Qt resources to Python version.

:Copyright: © 2018-2019, Laurent Kislaire.
:License: ISC (see /LICENSE).
"""

__all__ = ()

import sys

if sys.version_info[0] == 2:
    import yggscr.ui.resources2  # NOQA
elif sys.version_info[0] == 3:
    import yggscr.ui.resources3  # NOQA
else:
    print('FATAL: python version does not match `2` nor `3`')
    sys.exit(0)
