#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Ygg Scraper test suite
# Copyright © 2018-2019, Laurent Kislaire.
# See /LICENSE for licensing information.


import time
import sys
import requests
import pytest
from mock import patch, MagicMock
import yggscr.exceptions
from yggscr.shout import ShoutMessage, YggShout, main_loop, main as main_shout


def test_shout1():
    s = ShoutMessage(True)
    s = ShoutMessage(True, None, 1, 1, 1, "message")
    print("{}".format(s))
    s = YggShout(log=MagicMock())
    print("{}".format(s))
    main_loop(log=MagicMock())
    time.sleep(2)
    main_loop(log=MagicMock())


def test_shout_diff():
    y = YggShout(log=MagicMock())
    y.get_shouts()
    y.do_diff()     # set last_shouts

    time.sleep(2)
    y.get_shouts()  # set new_shouts
    del y.new_shouts[1]
    success = False
    for removed, shout in y.do_diff():
        if removed:
            shout.message += "<-- REMOVED"
            success = True
        print(shout)
    assert success


@pytest.mark.skipif(sys.version_info[:2] == (3, 5), reason="python3.5 doesn't have tmp_path")
def test_shout2(tmp_path):
    f = tmp_path / "foo.txt"
    f.write_text("""
    <li use="2" data-id="3087">
     <a href="/forum/index.php?members/allain6610.522/" class="avatar avatar--xxs" data-user-id="522" data-xf-init="member-tooltip" id="js-XFUniqueId20">
     <img src="/forum/data/avatars/s/0/522.jpg?1530742137" alt="Allain6610" class="avatar-u522-s" itemprop="image">
     </a>
     <a href="/forum/index.php?members/allain6610.522/" class="username" dir="auto" data-user-id="522" data-xf-init="member-tooltip" user-group-id="2" id="js-XFUniqueId21">Allain6610</a>:
     <span><div class="bbWrapper"><a href="https://ww1.yggtorrent.is/forum/index.php?members/18575/" class="username" data-xf-init="member-tooltip" data-user-id="18575" data-username="Mycke3131" id="js-XFUniqueId22">Mycke3131</a> <b>Fonctions en attente de mise a jour :</b><ul>
      <li>Les MP sur le forum</li>
      <li>Les Trophees sur le forum auront une utilité</li>
      <li>Le bouton "Signaler" dans les torrents (ecrire a <a href="mailto:contact@ygg.is">contact@ygg.is</a> ou voir un TP sur la shout)</li>
      <li>Editer/Supprimer dans l'historique de telechargement</li>
      </ul></div></span>
      <time class="u-dt" dir="auto" datetime="2018-07-16T14:58:54+0100" data-time="1531749534" data-date-string="16/7/18" data-time-string="14:58" title="16/7/18, à 14:58">il y a 33 minutes</time>
    </li>
    """)
    main_shout(["foo", str(f)])
    with patch("yggscr.shout.sys.exit") as mock_exit:
        main_shout(["foo", "nonexistent"])
        assert mock_exit.call_args[0][0] == 1
        main_shout(None)
        assert mock_exit.call_args[0][0] == 1


N_MAXTRIES = 1


def test_shout_failures():
    # Long test of 1 retry: 16+31 (47s)
    # Long test of 2 retries: 16+31+46 (93s)
    print("Testing connection failure for 47s")
    with patch("yggscr.shout.YggShout.get_shouts", side_effect=requests.exceptions.Timeout):
        with pytest.raises(yggscr.exceptions.YggException):
            main_loop(log=MagicMock(), NTRY=N_MAXTRIES)
            assert 0
    main_loop(log=MagicMock, NTRY=2)
