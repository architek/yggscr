# -*- encoding: utf-8 -*-
# Ygg Scraper v0.1.0
# Yggtorrent scraper library - Webserver - Rss - Shell
# Copyright © 2018, Laurent Kislaire.
# All rights reserved.
#
"""
Yggtorrent scraper library - Webserver - Rss - Shell

:Copyright: © 2018, Laurent Kislaire.
:License: ISC (see /LICENSE).
"""

from . import client
from . import const
from . import exceptions
from . import link
from . import sbrowser
from . import shell
from . import shout
from . import torrents
from . import ygg
from . import ylogging


__title__ = 'Ygg Scraper'
__version__ = '0.1.0'
__author__ = 'Laurent Kislaire'
__license__ = 'ISC'
__docformat__ = 'restructuredtext en'

__all__ = ["client", "const", "exceptions", "link", "sbrowser",
           "shell", "shout", "torrents", "ygg", "ylogging"]


# import gettext
# G = gettext.translation('yggscr', '/usr/share/locale', fallback='C')
# _ = G.gettext