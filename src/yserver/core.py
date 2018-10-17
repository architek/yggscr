import bottle
import html
import logging
import tempfile
import re
from os import chmod
from urllib.parse import urlencode
from itertools import cycle
from yserver.config import Config
from yggscr.exceptions import YggException, LoginFailed, TooManyFailedLogins
from yggscr.ygg import YggBrowser
from yggscr.link import cats
from yggscr.const import RSS_TPL, DL_TPL, get_dl_link
from yggscr.client import rtorrent_add_torrent, transmission_add_torrent, deluge_add_torrent, exec_cmd


bcyc = cycle([True, False])


class YggServer(bottle.Bottle):
    def __init__(self, cfg="yserver.cfg"):
        super(YggServer, self).__init__()
        self.state = {
            'sorted_torrents': '',
            'rtEn': False,
            'tsEn': False,
            'dgEn': False,
            'exEn': False,
            'ano': True,
            'corder': 'desc',
            'norder': 'desc',
        }

        self.config = Config()
        self.config.load_config(cfg)

        self.ygg = YggBrowser(
            proxy=self.config['proxy'],
            loglevel=logging.DEBUG if self.config.bool('debug') else logging.INFO,
        )
        self.log = self.ygg.log
        self.debug()

        self.log.debug("Yserver configuration used: {}".format(cfg))

        self.auth()
        self.log.info("Anonymous: {}, Proxy: {}, Ygg Auth: {}".format(
            self.state['ano'],
            self.ygg.proxy,
            self.ygg.idstate,
        ))
        self.setup_client_cols()
        self.setup_routes()

    def debug(self):
        if self.config.bool('debug'):
            bottle.debug(True)
            try:
                pass
                from bottle.ext import werkzeug
                werkzeug = werkzeug.Plugin()
                self.install(werkzeug)
                self.log.debug("Werkzeug installed")
            except Exception as e:
                self.log.warning(
                    "Couldn't start werkzeug ({}) debug middleware"
                    ", disabling".format(e))
                pass

    def auth(self):
        try:
            import uwsgi
            self.state['ano'] = uwsgi.opt['ano'].decode('utf8').upper() == "TRUE"
        except KeyError:
            self.state['ano'] = False
        except ImportError:
            # running from CLI, try to auth
            self.log.debug("Could not load uwsgi python module")
            self.state['ano'] = False
            pass

        if not self.state['ano']:
            try:
                username = self.config['ygg.username']
                password = self.config['ygg.password']
            except KeyError:
                self.state['ano'] = True
                pass

        if not self.state['ano']:
            try:
                self.ygg.login(ygg_id=username, ygg_pass=password)
            except Exception as e:
                self.log.error("Could not login with user <{}>, exception {}".format(username, e))
            # FIXME exception here vs 3 attempts later

    def setup_routes(self):
        self.add_hook('before_request', self.reco)
        for l, m in (
            ('/', self.index),
            ('/search', self.search_index),
            ('/rssearch', self.rssearch),
            ('/top/<name:re:(day|week|month|exclus)>', self.top_day),
            ('/dl/<idtorrent:int>', self.dl_torrent),
            ('/<client:re:(ts|rt|dg|ex)>/<idtorrent:int>/<cat:re:', self.send_torrent),
            ('/ex/<cat:path>/<subcat:path>/<idtorrent:int>', self.exec_torrent),
            ('/rss', self.rss),
            ('/rss/<cat>', self.rss_cat),
            ('/stats', self.stats),
            ('/static/<filepath>', self.server_static),
            ('/images/<filepath>', self.server_images),
        ):
            self.route(path=l, callback=m)

    def setup_client_cols(self):
        if not self.state['ano']:
            if self.config['rtorrent.rpc_url']:
                self.state['rtEn'] = True
            if self.config['transmission.host']:
                self.state['tsEn'] = True
            if self.config['deluge.host']:
                self.state['dgEn'] = True
            if self.config['exec.cmd']:
                self.state['exEn'] = True

    def run(self, **kwargs):
        super(YggServer, self).run(
            host=self.config['if.host'],
            port=self.config['if.port'],
            reloader=self.config.bool('debug'),
            **kwargs
        )

    def results_opts(self, results, sort=''):
        """ client side sort """
        return sorted(results,
                      key=lambda k: getattr(k, sort),
                      reverse=next(bcyc)) if sort else results

    def mtemplate(self, tpl, rtn=[], **kwargs):
        return bottle.template(tpl, request=bottle.request,
                               state=self.state, rtn=rtn, **kwargs)

    def rssize(self, torrents, base):
        rss_tpl = """<?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0">
    <channel>
    <title>YggTorrent RSS</title>
    <link>https://yggtorrent.is</link>
    <description>Better than Official YggTorrent RSS Feed</description>
    {items}
    </channel>
    </rss>"""
        item_tpl = """<item><title>{title}</title>"
            "<description>Size: {torrent.nsize}, Seeders: {torrent.seed}, "
            "Leechers: {torrent.leech}</description>
    <link>{torrent.href}</link><pubDate>{torrent.publish_date}</pubDate>
    <enclosure url="{uri}"/></item>"""

        bottle.response.set_header('Content-type', 'application/xml')
        return rss_tpl.format(items=''.join(
                    item_tpl.format(
                        torrent=torrent,
                        uri=base.format(id=torrent.tid),
                        title=html.escape(torrent.title))
                    for torrent in torrents))

    # Hooks
    def reco(self):
        if bottle.request.path.startswith(('/static/', '/images')):
            return
        if self.state['ano']:
            return
        try:
            self.ygg.ping()
        except Exception as e:
            self.log.warning(
                "Ping failed, can't check state, exception is {}".format(e))
        else:
            self.log.debug("Ping reported state {}".format(
                self.ygg.idstate))
        if self.ygg.idstate != "Authenticated":
            try:
                self.ygg.login(ygg_id=self.config['ygg.username'],
                               ygg_pass=self.config['ygg.password'])
            except LoginFailed as e:
                self.log.warning("Failed login, exception is {}".format(e))
                pass
                return
            except TooManyFailedLogins as e:
                self.log.error(
                    "Too many failed logins, login disabled (fix your settings), exception is {}".format(e))
                self.state['ano'] = True
                pass
                return
            except YggException as e:
                self.log.error("Generic exception got raised: {}".format(e))
                pass
                return

            self.log.debug("Logged in as %s" % self.config['ygg.username'])
        else:
            self.log.debug("Already authenticated")

    # Static Images routes
    def server_static(self, filepath):
        return bottle.static_file(filepath, root='resources/static')

    def server_images(self, filepath):
        return bottle.static_file(filepath, root='resources/images')

    # Routes
    def index(self):
        return self.mtemplate(
            'index',
            rtn=["Welcome " + (
                "Anonymous - Connect for more options"
                if self.state['ano'] else self.config['ygg.username'])]
                        )

    def search_index(self):
        q = bottle.request.copy().query.decode()
        if q.pop('act', "") == "Rssize":
            bottle.redirect("rssearch?" + bottle.request.query_string)

        rtn = []
        try:
            torrents = self.ygg.search_torrents(q=q)
        except Exception as e:
            self.state['sorted_torrents'] = []
            rtn.append("Failed: {}".format(e))
        else:
            self.state['sorted_torrents'] = torrents
            rtn.append("Search returned {} torrents".format(len(torrents)))

        q.pop('sort', None)
        q.pop('page', None)
        self.state['corder'] = q.pop('order', 'asc')
        self.state['norder'] = 'desc' if self.state['corder'] == 'asc' else 'asc'

        self.state['qs'] = 'search?' + urlencode(q, True)
        return self.mtemplate('search_results', rtn=rtn)

    def rssearch(self):
        q = bottle.request.copy().query.decode()
        q.pop('act', None)
        q['sort'] = 'publish_date'
        q['order'] = 'desc'
        torrents = self.ygg.search_torrents(q=q)
        if self.state['ano']:
            return self.rssize(torrents, DL_TPL)
        else:
            return self.rssize(torrents, bottle.request.urlparts.scheme + "://" +
                               bottle.request.urlparts.netloc+bottle.request.script_name+"dl/{id}")

    def top_day(self, name):
        torrents = {
            'day': self.ygg.top_day,
            'week': self.ygg.top_week,
            'month': self.ygg.top_month,
            'exclus': self.ygg.exclus,
        }.get(name, lambda: [])()
        self.state['sorted_torrents'] = self.results_opts(torrents, bottle.request.query.sort)
        self.state['qs'] = 'top/{}?'.format(name)
        return self.mtemplate('search_results',
                              rtn=["Search returned {} torrents".format(
                                  len(torrents))])

    def dl_torrent(self, idtorrent):
        head, resp = self.ygg.download_torrent(id=idtorrent)
        for k, v in head:
            bottle.response.set_header(k, v)
        return resp

    def exec_torrent(self, cat, subcat, idtorrent):
        rtn = []

        try:
            _, resp = self.ygg.download_torrent(id=idtorrent)
        except Exception as e:
            rtn.append("Couldn't download torrent [{}]".format(e))

        fp = tempfile.NamedTemporaryFile(prefix="yggscr-", suffix=".torrent")
        fp.write(resp)
        fp.flush()
        chmod(fp.name, 444)

        cmd = self.config['exec.cmd'].format(f=fp.name, cat=cat, subcat=subcat)
        rtn.append("Torrent downloaded, executing command {}".format(cmd))
        output, error = exec_cmd(cmd)
        self.log.debug(error)

        if error:
            rtn.append("FAIL {} | {}".format(error, output))
        else:
            rtn.append("OK | {}".format(output))
        self.state['qs'] = 'search?'
        return self.mtemplate('search_results', rtn=rtn)

    def send_torrent(self, client, idtorrent):
        rtn = []

        try:
            _, resp = self.ygg.download_torrent(id=idtorrent)
            rtn.append("Torrent downloaded, sending to {} client...".format(client))
        except Exception as e:
            rtn.append("Couldn't download torrent [{}]".format(e))

        try:
            if client == "ts":
                user = self.config['transmission.user']
                passw = self.config['transmission.password']
                host = self.config['transmission.host']
                port = self.config['transmission.tport']
                msg = "Adding torrent to transmission {}:{}@{}:{}".format(
                    user, passw, host, port)
                rtn.append(msg)
                transmission_add_torrent(host, port, user, passw, resp)
            elif client == "rt":
                ru = self.config['rtorrent.rpc_url']
                rtn.append("Adding torrent to rtorrent @ rpc_url {}".format(ru))
                rtorrent_add_torrent(ru, resp)
            elif client == "dg":
                user = self.config['deluge.user']
                passw = self.config['deluge.password']
                host = self.config['deluge.host']
                port = self.config['deluge.tport']
                rtn.append("Adding {}:{}@{}:{}".format(user, passw, host, port))
                r = deluge_add_torrent(host, port, user, passw, resp)
                rtn.append("Deluged RPC returned {}".format(r))
        except Exception as e:
            msg = "Adding torrent failed [{}]".format(e)
            rtn.append(msg)
            pass
        else:
            rtn.append("Ok")
        self.state['qs'] = 'search?'
        return self.mtemplate('search_results', rtn=rtn)

    def rss(self):
        return self.mtemplate('rss', results=cats)

    def rss_cat(self, cat):
        def rep_f(match):
            return str(get_dl_link(match.group(1)) + '"')

        if cat in cats.keys():
            cat = cats[cat]
        elif cat not in cats.values():
            return self.rss()
        self.ygg.get(RSS_TPL.format(category=cat))
        uri = bottle.request.urlparts.scheme+"://" + \
            bottle.request.urlparts.netloc
        if self.state['ano']:
            response_body = re.sub(
                r'https:[^"]*torrent_generator[^"0-9]*([0-9]*).*"',
                rep_f,
                self.ygg.response().content.decode('utf-8'))
        else:
            response_body = re.sub(
                r'https:[^"]*torrent_generator[^"0-9]*([0-9]*).*"',
                r'%s/dl/\1"' % uri,
                self.ygg.response().content.decode('utf-8'))
        bottle.response.set_header('Content-type', 'application/xml')
        response_body = re.sub(r'(Official YggTorrent)', r'Better than \1',
                               response_body)
        return response_body

    def stats(self):
        if self.state['ano']:
            return {'error': 'Connect to get your stats in real time'}
        try:
            return self.ygg.get_stats()
        except Exception as e:
            return {'error': 'Error Exception {}'.format(e)}
