# -*- encoding: utf-8 -*-
# Ygg Scraper v1.1.6
# Yggtorrent scraper library - Webserver - Rss - Shell
# Copyright © 2018, Laurent Kislaire.
# See /LICENSE for licensing information.

"""
Main routine of Ygg Scraper standalone webserver.

:Copyright: © 2018, Laurent Kislaire.
:License: ISC (see /LICENSE).
"""

__all__ = ('main',)
import sys
import getopt
from yserver.core import YggServer


def main():
    """Main routine of Ygg Scraper webserver."""

    cfg = "yserver.cfg"
    argv = sys.argv[1:]
    if argv:
        try:
            opts, args = getopt.getopt(argv, "c:", ["cfg="])
            for opt, arg in opts:
                if opt in ("-c", "--cfg"):
                    cfg = arg
        except getopt.GetoptError:
            print("Usage: yserver [-c /path/to/yserver.cfg]")
            sys.exit(2)
    app = YggServer(cfg)
    app.run(server='wsgiref')


if __name__ == '__main__':
    main()
