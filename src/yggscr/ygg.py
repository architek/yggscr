# -*- coding: utf-8 -*-

import re
import os
import json
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG #noqa
import datetime
from bs4 import BeautifulSoup
from yggscr import ylogging
from yggscr.stats import Stats
from yggscr.torrents import Torrent
from yggscr.sbrowser import SBrowser
from yggscr.exceptions import YggException, LoginFailed, TooManyFailedLogins
from yggscr.const import YGG_HOME, TOP_DAY_URL, TOP_WEEK_URL, TOP_MONTH_URL, \
                   EXCLUS_URL, TOP_SEED_URL, SEARCH_URL, get_dl_link
from yggscr.link import get_cat_id, list_cat_subcat

from urllib.parse import urlparse, parse_qs, urlsplit

# from pprint import (PrettyPrinter, pprint)
# pp = PrettyPrinter(indent=4)


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
        self.log.debug("Created YggBrowser")
        self.last_ygg_id = None
        self.login_attempts = 0

    def __str__(self):
        return "{} | [YGG] Auth {}".format(
            SBrowser.__str__(self),
            self.idstate)

    def gen_state(self):
        def upd_state(r, *args, **kwargs):
            if urlsplit(YGG_HOME).netloc == urlsplit(r.url).netloc and "forum" not in r.url \
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

        if ygg_id != self.last_ygg_id:
            self.login_attempts = 1
            self.last_ygg_id = ygg_id

        if self.login_attempts > 3:
            self.log.debug("Not trying to login with 3 consecutive failed attempts. Fix your configuration and retry.")
            raise TooManyFailedLogins("3 consecutives logins")
        try:
            self._id = ygg_id if ygg_id else os.environ['ygg_id']
            self._pass = ygg_pass if ygg_id else os.environ['ygg_pass']
        except KeyError:
            self.log.error("Asked to login but provided "
                           "neither config nor environment variable")
            pass
            return

        self.open(YGG_HOME)
        self.login_attempts += 1

        if self.idstate == "Authenticated":
            raise YggException("Logout first")

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
            raise LoginFailed("State did not change to authenticate")
        self.login_attempts = 0

    def logout(self):
        self.browser.session.cookies.clear()
        self.idstate = "Anonymous"

    def get_stats(self):
        self.open(YGG_HOME)
        if self.idstate != "Authenticated":
            raise YggException("Not logged in, idstate is {}".format(self.idstate))

        html = str(self.response().content)
        pos_r = html.find('Ratio')
        html = html[pos_r-500:pos_r+500]
        vals = re.findall(r'\b([0-9\.]+)([GTP])[oB]\b', html)
        if len(vals) != 2:
            raise YggException("Can't find ratio information")
        else:
            self.stats.add(vals)

        # Return dict of first level keys
        return {k: v for (k, v) in self.stats.__dict__.items() if not isinstance(v, dict)}

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
        return self._parse_torrents(table_num=0, n=100)

    def top_seeded(self):
        return self._get_torrents_xhr(TOP_SEED_URL, method="post")

    def _parse_torrents(self, sup=None, detail=False, table_num=1, n=100):
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
            for row in table.find_all('tr')[:n]:
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
                    date = re.findall(r'\d+/\d+/\d+ \d+:\d+', #noqa
                                      str(self.response().content))[0]
                    uploader = self.parsed().find('td', string='Uploadé par')\
                        .parent.find_all('td')[1].get_text()
                    tid = parse_qs(urlparse(thref).query)['id'][0]
                    torrent_list.append(Torrent(
                        name, comm, age, size, compl, seeders, leechers, href,
                        thref, tid, uploader=uploader))
                else:
                    torrent_list.append(Torrent(
                        name, comm, age, size, compl, seeders, leechers, href))
        except (IndexError, KeyError):
            raise YggException("Couldn't decode web page")

        return torrent_list

    def search_torrents(self, detail=False, q=None, nmax=100, **kwargs):
        qx = {}

        category = q.get('category', '')
        sub_category = q.get('sub_category', '')

        if category and not category.isdigit():
            q.pop('category')   # Formsdict
            q.pop('sub_category', '')
            q.update(get_cat_id(category, sub_category, self.log))

        self.log.debug("Searching...")

        # Convert formsdict or dict to requests parameters list
        for k in q.keys():
            try:
                vals = q.getall(k)
                qx[k] = vals if len(vals) > 1 else vals[0]
            except AttributeError:
                qx[k] = q[k]

        qx['do'] = 'search'
        self.open(SEARCH_URL, params=qx)
        self.log.debug("Searched on this url {} with detail:{}"
                       .format(self.response().url, detail))

        return self._parse_torrents(detail=detail, n=nmax)

    def next_torrents(self, nmax=100):
        s_href = self.browser.find('a', string=re.compile('suivant'))
        if s_href:
            self.browser.follow_link(s_href)
        else:
            return []
        return self._parse_torrents(n=nmax)

    def cat_subcat(self):
        return list_cat_subcat()

    def ping(self):
        self.open(YGG_HOME)
        return self.response().status_code

    def download_torrent(self, torrent=None, id=None):
        href = torrent.get_dl_link() if torrent is not None \
                                       else get_dl_link(id)
        self.open(href)
        iheaders = self.response().headers
        try:
            headers = [('Content-type', iheaders['Content-type']),
                       ('Content-Disposition',  iheaders['Content-Disposition'])]
        except KeyError:
            self.log.error("Couldn't download torrent")
            return
        response_body = self.response().content
        return headers, response_body
