#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import time
import json
import datetime
from bs4 import BeautifulSoup
from .torrents import Torrent
from .sbrowser import SBrowser
from .exceptions import YggException
from .link import get_link, get_cat_id, list_cat_subcat

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# from pprint import (PrettyPrinter, pprint)
# pp = PrettyPrinter(indent=4)

SITE = "ww1.yggtorrent.is"
HOME_URL = "https://" + SITE
TORRENT_URL = HOME_URL + "/torrents/"
SEARCH_URL = HOME_URL + "/engine/search"
TOP_DAY_URL = HOME_URL + "/engine/ajax_top_query/day"
TOP_WEEK_URL = HOME_URL + "/engine/ajax_top_query/week"
TOP_MONTH_URL = HOME_URL + "/engine/ajax_top_query/month"
TOP_SEED_URL = HOME_URL + "/engine/mostseeded"
DL_TMPL = HOME_URL + "/engine/download_torrent?id=%s"


class YggBrowser(SBrowser):
    """Ygg Scrapper with CloudFlare bypass
    """
    def __init__(self, scraper=None,
                 browser=None):
        SBrowser.__init__(self, scraper, browser)
        self.idstate = None
        self.detail = False         # No detailed torrent info by default
        self.browser.session.hooks['response'].append(self.gen_state())
        self.first = {"time": None, "up": None, "down": None}
        self.last = {"time": None, "up": None, "down": None}

    def __str__(self):
        return "{} | [YGG] Auth {}".format(
            SBrowser.__str__(self),
            self.idstate)

    def gen_state(self):
        def upd_state(r, *args, **kwargs):
            if "yggtorrent.is" in r.url and "forum" not in r.url \
                    and r.encoding is not None:
                if "Mon compte" in r.text:
                    self.idstate = "authenticated"
                else:
                    self.idstate = "anonymous"
        return upd_state

    def login(self, ygg_id=None, ygg_pass=None):
        self.browser.open(HOME_URL)
        if self.idstate == "authenticated":
            raise YggException("Disconnect first")
        self._id = ygg_id if ygg_id else os.environ['ygg_id']
        self._pass = ygg_pass if ygg_id else os.environ['ygg_pass']
        for form in self.browser.get_forms():
            if form.parsed.find(id="login_msg_pass"):
                login_form = form
                break
        else:
            raise YggException("Can't find any form containing")

        login_form['id'].value = self._id
        login_form['pass'].value = self._pass
        self.browser.submit_form(login_form)
        self.browser.open(HOME_URL)
        if self.idstate != "authenticated":
            raise YggException("Login failed")

    def logout(self):
        self.browser.session.cookies.clear()
        self.idstate = "anonymous"

    def upd_speed(self, up, down):
        GiB = 1024*1024
        ctime = time.time()
        if self.last["time"] is None:
            i_up = i_down = "?"
        else:
            i_up = round(GiB*(up-self.last["up"])/(
                ctime-self.last["time"]))
            i_down = round(GiB*(down-self.last["down"])/(
                ctime-self.last["time"]))
        self.last = {"time": ctime, "up": up, "down": down}
        if self.first["time"] is None:
            self.first = {"time": time.time(), "up": up, "down": down}
            m_up = m_down = "?"
        else:
            m_up = round(GiB*(up-self.first["up"])/(
                ctime-self.first["time"]))
            m_down = round(GiB*(down-self.first["down"])/(
                ctime-self.first["time"]))
        return i_up, m_up, i_down, m_down

    def stats(self):
        if self.idstate != "authenticated":
            raise YggException("Not logged in")

        self.browser.open(HOME_URL)

        html = str(self.response().content)
        pos_r = html.find('Ratio')
        html = html[pos_r-500:pos_r+500]
        vals = re.findall(r'\b([0-9\.]+)([GT])[oB]\b', html)
        if len(vals) != 2:
            raise YggException("Can't find ratio information")

        # Will only work for ratio above 1 but makes the search more robust
        # Note that website is inconsistent (TiB vs TB, GiB vs GB)
        down, up = sorted(float(e[0]) if e[1] == 'G' else float(e[0]) * 1024
                          for e in vals)
        i_up, m_up, i_down, m_down = self.upd_speed(up, down)
        ratio = round(up/down, 4)
        return {'down': down, 'up': up, 'ratio': ratio,
                'i_up': i_up, 'm_up': m_up, 'i_down': i_down, 'm_down': m_down}

    def _get_torrents_xhr(self, url, method="get"):
        torrent_list = []
        self.browser.open(url, method=method)
        jres = json.loads(self.response().content.decode('utf-8'))
        for jcat in jres:
            for jtor in jres[jcat]:
                torrent_list.append(Torrent(
                    torrent_title=BeautifulSoup(jtor[1], "lxml").text.rstrip(),
                    torrent_comm=jtor[3],
                    torrent_age=datetime.datetime.fromtimestamp(
                        int(BeautifulSoup(jtor[4], "lxml").div.text)).strftime(
                            "%Y-%m-%d %H:%M:%S"),
                    torrent_size=jtor[5].split(">")[-1],
                    torrent_compl=jtor[6],
                    torrent_seed=jtor[7],
                    torrent_leech=jtor[8],
                    href=BeautifulSoup(jtor[1], "lxml").find(
                        'a', href=True)['href'],
                    cat=jcat
                ))
        return torrent_list

    def top_day(self):
        return self._get_torrents_xhr(TOP_DAY_URL)

    def top_week(self):
        return self._get_torrents_xhr(TOP_WEEK_URL)

    def top_month(self):
        return self._get_torrents_xhr(TOP_MONTH_URL)

    def top_seeded(self):
        return self._get_torrents_xhr(TOP_SEED_URL, method="post")

    def _parse_torrents(self, sup=None, detail=None):
        torrent_list = []
        if sup is None:
            sup = self.parsed()
        if detail is None:
            detail = self.detail
        try:
            if "Aucun résultat" in sup.text:
                return None
            table = sup.find_all('table')[1]
            if table is None:
                raise YggException("Couldn't decode web page")
            table = table.find('tbody')
            for row in table.find_all('tr'):
                rlinks = row.find_all('a')
                rlink = rlinks[1]
                name = rlink.text.rstrip()
                href = rlink['href']
                tds = row.find_all('td')
                comm, age, size, compl, seeders, leechers = (c.text.rstrip()
                                                             for c in tds[3:])
                age = age.split(" ")[0]
                age = datetime.datetime.fromtimestamp(
                    int(age)).strftime('%Y-%m-%d %H:%M:%S')
                if detail:
                    self.browser.open(href)
                    thref = self.browser.find(
                        'a',
                        attrs={'href': re.compile("download_torrent")})['href']
                    date = re.findall(r'\d+/\d+/\d+ \d+:\d+',
                                      str(self.response().content))[0]
                    tid = parse.parse_qs(parse.urlparse(thref).query)['id'][0]
                    torrent_list.append(Torrent(
                        name, comm, age, size, compl, seeders, leechers, href,
                        thref, tid))
                else:
                    torrent_list.append(Torrent(
                        name, comm, age, size, compl, seeders, leechers, href))
        except (IndexError, KeyError):
            raise YggException("Couldn't decode web page")

        return torrent_list

    def list_torrents(self, cat, subcat, detail=False):
        self.browser.open(TORRENT_URL + get_link(cat, subcat))
        self.detail = detail
        return self._parse_torrents()

    def search_torrents(self, pattern, cat=None, subcat=None, detail=False):
        param = dict()
        if cat is not None:
            param = get_cat_id(cat, subcat)
        param['order'] = "desc"
        param['sort'] = "seed"
        param['name'] = pattern
        param['do'] = "search"
        self.browser.open(SEARCH_URL, params=param)
        self.detail = detail
        return self._parse_torrents()

    def next_torrents(self):
        s_href = self.browser.find('a', string=re.compile('suivant'))
        if s_href:
            self.browser.follow_link(s_href)
        else:
            return None
        return self._parse_torrents()

    def cat_subcat(self):
        return list_cat_subcat()

    def ping(self):
        self.browser.open(HOME_URL)

    def id2href(self, id):
        return DL_TMPL % id

    def download_torrent(self, torrent=None, id=None):
        href = torrent.get_dl_link() if torrent is not None \
                                       else self.id2href(id)
        self.get(href)
        iheaders = self.response().headers
        headers = [('Content-type', iheaders['Content-type']),
                   ('Content-Disposition',  iheaders['Content-Disposition'])]
        response_body = self.response().content
        return headers, response_body
