# -*- coding: utf-8 -*-

import re
import os
import time
import json
from yggscr import ylogging
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG #noqa
import datetime
from bs4 import BeautifulSoup
from .torrents import Torrent
from .sbrowser import SBrowser
from .exceptions import YggException
from .const import YGG_HOME, TOP_DAY_URL, TOP_WEEK_URL, TOP_MONTH_URL, \
                   EXCLUS_URL, TOP_SEED_URL, TORRENT_URL, SEARCH_URL, DL_TPL
from .link import get_link, get_cat_id, list_cat_subcat

from urllib.parse import urlparse, parse_qs

# from pprint import (PrettyPrinter, pprint)
# pp = PrettyPrinter(indent=4)


class Stats():
    def __init__(self):
        self.first = {"time": None,
                      "up": None, "down": None}
        self.last = {"time": None,
                     "up": None, "down": None}

    def upd_speed(self):
        GiB = 1024*1024
        ctime = time.time()
        if self.last["time"] is None:
            i_up = i_down = "?"
        else:
            i_up = round(GiB*(self.up-self.last["up"])/(
                ctime-self.last["time"]))
            i_down = round(GiB*(self.down-self.last["down"])/(
                ctime-self.last["time"]))
        self.last = {"time": ctime, "up": self.up, "down": self.down}
        if self.first["time"] is None:
            self.first = {
                "time": time.time(),
                "up": self.up,
                "down": self.down
            }
            m_up = m_down = "?"
        else:
            m_up = round(GiB*(self.up-self.first["up"])/(
                ctime-self.first["time"]))
            m_down = round(GiB*(self.down-self.first["down"])/(
                ctime-self.first["time"]))
        return i_up, m_up, i_down, m_down

    # Will only work for ratio above 1 but makes the search more robust
    # Note that website is inconsistent (TiB vs TB, GiB vs GB)
    def add(self, vals):
        self.down, self.up = sorted(
            float(e[0]) if e[1] == 'G' else float(e[0]) * 1024
            for e in vals)
        self.iup, self.mup, self.idown, self.mdown = self.upd_speed()
        self.ratio = round(self.up/self.down, 4)


class YggBrowser(SBrowser):
    """Ygg Scrapper with CloudFlare bypass
    """
    def __init__(self, scraper=None,
                 browser=None, proxy=None, loglevel=INFO):
        self.log = ylogging.consolelog(__name__, loglevel)
        SBrowser.__init__(self, scraper=scraper, browser=browser,
                          proxy=proxy, history=False, timeout=10,
                          parser='html.parser', loglevel=loglevel)
        self.idstate = None
        self.stats = Stats()
        self.browser.session.hooks['response'].append(self.gen_state())
        self.log.info("Created YggBrowser")

    def __str__(self):
        return "{} | [YGG] Auth {}".format(
            SBrowser.__str__(self),
            self.idstate)

    def gen_state(self):
        def upd_state(r, *args, **kwargs):
            if YGG_HOME in r.url and "forum" not in r.url \
                    and r.encoding is not None:
                old_state = self.idstate
                if "Mon compte" in r.text:
                    self.idstate = "Authenticated"
                else:
                    self.idstate = "Anonymous"
                if old_state != self.idstate:
                    self.log.debug("Auth state changed {}->{}".format(
                        old_state, self.idstate))
        return upd_state

    def login(self, ygg_id=None, ygg_pass=None):
        self.open(YGG_HOME)
        if self.idstate == "Authenticated":
            raise YggException("Logout first")
        try:
            self._id = ygg_id if ygg_id else os.environ['ygg_id']
            self._pass = ygg_pass if ygg_id else os.environ['ygg_pass']
        except KeyError:
            self.log.error("Asked to login but provided "
                           "neither config nor environment variable")
            pass
            return

        for form in self.browser.get_forms():
            if form.parsed.find(id="login_msg_pass"):
                login_form = form
                break
        else:
            raise YggException("Can't find any form containing")

        login_form['id'].value = self._id
        login_form['pass'].value = self._pass
        self.browser.submit_form(login_form)
        self.open(YGG_HOME)
        if self.idstate != "Authenticated":
            raise YggException("Login failed")

    def logout(self):
        self.browser.session.cookies.clear()
        self.idstate = "Anonymous"

    def get_stats(self):
        self.open(YGG_HOME)
        if self.idstate != "Authenticated":
            raise YggException(
                "Not logged in, idstate is {}".format(self.idstate))

        html = str(self.response().content)
        pos_r = html.find('Ratio')
        html = html[pos_r-500:pos_r+500]
        vals = re.findall(r'\b([0-9\.]+)([GT])[oB]\b', html)
        if len(vals) != 2:
            raise YggException("Can't find ratio information")
        else:
            self.stats.add(vals)

        return {'down': self.stats.down, 'up': self.stats.up,
                'ratio': self.stats.ratio,
                'i_up': self.stats.iup, 'i_down': self.stats.idown,
                'm_up': self.stats.mup, 'm_down': self.stats.mdown
                }

    def _get_torrents_xhr(self, url, method="get", timeout=None):
        torrent_list = []
        self.open(url, method=method, timeout=timeout)
        jres = json.loads(self.response().content.decode('utf-8'))
        for jcat in jres:
            for jtor in jres[jcat]:
                try:
                    torrent_list.append(Torrent(
                        torrent_title=BeautifulSoup(
                            jtor[1], 'html.parser').text.rstrip(),
                        torrent_comm=jtor[3],
                        torrent_age=datetime.datetime.fromtimestamp(
                            int(BeautifulSoup(
                                jtor[4], 'html.parser').div.text)).strftime(
                            "%Y-%m-%d %H:%M:%S"),
                        torrent_size=jtor[5].split(">")[-1],
                        torrent_completed=jtor[6],
                        torrent_seed=jtor[7],
                        torrent_leech=jtor[8],
                        href=BeautifulSoup(jtor[1], 'html.parser').find(
                            'a', href=True)['href'],
                        cat=jcat
                    ))
                except Exception as e:
                    # unknown elements
                    pass
                    self.log.debug(
                        "While getting xhr: {}, jtor={}".format(e, jtor))
        return torrent_list

    def top_day(self):
        return self._get_torrents_xhr(TOP_DAY_URL, timeout=30)

    def top_week(self):
        return self._get_torrents_xhr(TOP_WEEK_URL, timeout=30)

    def top_month(self):
        return self._get_torrents_xhr(TOP_MONTH_URL, timeout=30)

    def exclus(self):
        self.open(EXCLUS_URL)
        return self._parse_torrents(table_num=0)

    def top_seeded(self):
        return self._get_torrents_xhr(TOP_SEED_URL, method="post")

    def _parse_torrents(self, sup=None, detail=False, table_num=1):
        torrent_list = []
        if sup is None:
            sup = self.parsed()
        try:
            if "Aucun résultat" in sup.text:
                return []
            table = sup.find_all('table')[table_num]
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
                    self.log.debug("Fetching details for torrent")
                    self.open(href)
                    thref = self.browser.find(
                        'a',
                        attrs={'href': re.compile("download_torrent")})['href']
                    date = re.findall(r'\d+/\d+/\d+ \d+:\d+',
                                      str(self.response().content))[0]
                    tid = parse_qs(urlparse(thref).query)['id'][0]
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
        "This doesn't exist anymore on website"
        self.open(TORRENT_URL + get_link(cat, subcat))
        return self._parse_torrents(detail=detail)

    def search_torrents(self, detail=False, q=None, **kwargs):
        category = q.get('category', '')
        sub_category = q.get('sub_category', '')
        if category and not category.isdigit():
                q.update(get_cat_id(self.log, category, sub_category))

        q['do'] = 'search'
        self.log.debug("Searching...")

        # Convert formsdict q to request params
        qx = dict()
        for k in q.keys():
            vals = []
            try:
                for v in q.getall(k):
                    vals.append(v)
            except AttributeError:
                vals.append(q[k])
            if len(vals) > 1:
                qx[k] = vals
            else:
                qx[k] = vals[0]
        self.log.debug("qx is {}".format(qx))
        self.open(SEARCH_URL, params=qx)
        self.log.debug("Searched on this url {} with detail:{}"
                       .format(self.response().url, detail))

        return self._parse_torrents(detail=detail)

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
        self.open(YGG_HOME)
        return self.response().status_code

    def id2href(self, id):
        return DL_TPL.format(id=id)

    def download_torrent(self, torrent=None, id=None):
        href = torrent.get_dl_link() if torrent is not None \
                                       else self.id2href(id)
        self.get(href)
        iheaders = self.response().headers
        headers = [('Content-type', iheaders['Content-type']),
                   ('Content-Disposition',  iheaders['Content-Disposition'])]
        response_body = self.response().content
        return headers, response_body
