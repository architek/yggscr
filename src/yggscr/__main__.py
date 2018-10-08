# -*- encoding: utf-8 -*-
# Ygg Scraper v1.1.9
# Yggtorrent scraper library - Webserver - Rss - Shell
# Copyright © 2018, Laurent Kislaire.
# See /LICENSE for licensing information.

"""
Main routine of Ygg Scraper shell.

:Copyright: © 2018, Laurent Kislaire.
:License: ISC (see /LICENSE).
"""

__all__ = ('main',)
from yggscr.shell import YggShell


def main():
    """Main routine of Ygg Scraper shell."""
    YggShell().cmdloop()


if __name__ == '__main__':
    main()
