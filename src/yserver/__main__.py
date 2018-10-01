# -*- encoding: utf-8 -*-
# Ygg Scraper v1.0.9
# Yggtorrent scraper library - Webserver - Rss - Shell
# Copyright © 2018, Laurent Kislaire.
# See /LICENSE for licensing information.

"""
Main routine of Ygg Scraper standalone webserver.

:Copyright: © 2018, Laurent Kislaire.
:License: ISC (see /LICENSE).
"""

__all__ = ('main',)
from yserver.core import YggServer


def main():
    """Main routine of Ygg Scraper webserver."""
    app = YggServer('YggServer')
    app.run(server='wsgiref')


if __name__ == '__main__':
    main()
