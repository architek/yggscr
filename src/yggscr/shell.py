import shlex
import requests
from cmd2 import Cmd
import logging
from . import ygg
from . import ylogging
from . import link
from functools import wraps
from .exceptions import YggException
# from pprint import (PrettyPrinter, pprint)
# pp = PrettyPrinter(indent=4)


LOG = logging.INFO


def wrapper(method):
    @wraps(method)
    def _impl(self, *method_args, **method_kwargs):
        try:
            torrents = method(self, *method_args, **method_kwargs)
        except (requests.exceptions.RequestException) as e:
            print("Wrapped Network error:%s" % e)
            return
        if torrents:
            self.print_torrents(torrents)
        else:
            print("No results")
    return _impl


class YggShell(Cmd):
    'Ygg command line interface'
    def __init__(self, ygg_browser=None, **kwargs):
        Cmd.__init__(self, **kwargs)
        self.intro = "Welcome to Ygg Shell. Type help or ? to list commands.\n"
        self.prompt = "> "
        self.log = ylogging.consolelog(__name__, LOG)
        self.allow_redirection = False
        if ygg_browser is not None:
            self.ygg_browser = ygg_browser
        else:
            self.ygg_browser = ygg.YggBrowser(loglevel=LOG)
#        self.ygg_browser.proxify("socks5h://192.168.1.17:9100")

    def print_torrents(self, torrents, n=None):
        if n is not None:
            n = int(n)
        for i, t in enumerate(torrents[:n]):
            print("* %2d - %s" % (1+i, t))

    def do_proxify(self, line):
        '''Sets or resets proxy settings
        proxify [xxx://user:pass@host:port]
        proxify without arguments will set no proxy
        proxify http://1.1.1.1:8080 to select an http proxy
        proxify socks5h://1.1.1.1 to select a socks proxy with remote dns
        proxify socks5://1.1.1.1 to select a socks proxy with local dns
        '''
        args = shlex.split(line.strip())
        if args and len(args) != 1:
            print("ERROR: Syntax is proxify [https_proxy]")
            return
        if not args:
            self.ygg_browser.proxify(None)
        else:
            self.ygg_browser.proxify(args[0])

    def do_login(self, line):
        'login <user> <pass> used to authenticate on ygg'
        args = shlex.split(line.strip())
        try:
            self.ygg_browser.login(args[0], args[1])
            print("Connected as %s" % args[0])
        except (requests.exceptions.RequestException) as e:
            print("Login Network error:%s" % e)
            return
        except IndexError:
            print("ERROR: Syntax is login id pass")
            return

    def do_logout(self, line):
        self.ygg_browser.logout()

    def do_stats(self, line):
        'stats to return ratio statistics once authenticated'
        try:
            mystat = self.ygg_browser.get_stats()
        except (requests.exceptions.RequestException) as e:
            print("Network error:%s" % e)
            return
        print("Ratio:%s" % mystat['ratio'])
        print("Down (GB):%s" % mystat['down'])
        print("Up (GB):%s" % mystat['up'])
        print("Instant speed (KBps):Up {} - Down {}".format(
              mystat['i_up'], mystat['i_down']))
        print("Mean speed (KBps):Up {} - Down {}".format(
              mystat['m_up'], mystat['m_down']))

    def do_print(self, line):
        'prints connection status'
        try:
            print(self.ygg_browser)
        except (requests.exceptions.RequestException) as e:
            print("Network error:%s" % e)
            return

    def do_search_torrents(self, line):
        '''search torrents
        search_torrents q:<pattern> [c:<category>] [s:<subcategory>]
        [s:<subcategory>] [opt1:val] [opt2:val1] [opt2:val2] [d:False] [n:3]
        any other option will be passed unchanged to the webserver
        d is for detail which will fetch each torrent url for more details
        n is the number of torrents to display (all by default)
        '''
        q = {}
        try:
            for t in shlex.split(line.strip()):
                k, v = t.rsplit(':', 1)
                if k not in q:
                    q[k] = v
                else:
                    if isinstance(q[k], list):
                        q[k].append(v)
                    else:
                        q[k] = [q[k], v]
        except ValueError as e:
            raise YggException("Error: Invalid syntax in search_torrents {}".format(e))
        try:
            q['name'] = q.pop('q')
            q['category'] = q.pop('c', "")
            q['sub_category'] = q.pop('s', "")
        except KeyError as e:
            raise YggException("Error: Invalid syntax in search_torrents {}".format(e))

        detail = q.pop('d', False)
        n = int(q.pop('n', 3))

        self.log.debug("do_search_torrents parameter:{}".format(q))
        try:
            torrents = self.ygg_browser.search_torrents(
                q=q,
                detail=detail, nmax=n)
        except (requests.exceptions.RequestException) as e:
            print("Network error:%s" % e)
            return
        # except KeyError:
        #    raise YggException(
        #        "Error: Syntax is search_torrents " +
        #        "q:<pattern> [c:<category>] [s:<subcategory>] [d:True]")
        if torrents:
            self.print_torrents(torrents)
        else:
            print("No results")

    def do_next(self, line):
        'returns next torrents from previous search or list'
        line = line.strip()
        if line:
            if line.startswith('n:'):
                try:
                    n = int(line[2:])
                except ValueError:
                    raise YggException("Error: Syntax is next [n:nmax]")
            else:
                raise YggException("Error: Syntax is next [n:nmax]")
        else:
            n = 3
        torrents = self.ygg_browser.next_torrents(nmax=n)
        if torrents:
            self.print_torrents(torrents)
        else:
            print("No results")

    @wrapper
    def do_top_day(self, line):
        """ Get Top day """
        return self.ygg_browser.top_day()

    @wrapper
    def do_top_week(self, line):
        """ Get Top week """
        return self.ygg_browser.top_week()

    @wrapper
    def do_top_month(self, line):
        """ Get Top month """
        return self.ygg_browser.top_month()

    @wrapper
    def do_exclus(self, line):
        """ Get exclu """
        return self.ygg_browser.exclus()

    def do_lscat(self, line):
        'list categories and subcategories'
        print("List of cat, subcat combinaisons:\n%s" %
              link.list_cat_subcat())

    def do_ping(self, line):
        'perform a connection to /'
        r = self.ygg_browser.ping()
        print("Return code {}".format(r))

    def do_response(self, line):
        'get last response'
        print(self.ygg_browser.response().text)

    def do_open(self, url):
        'do a simple get on an url'
        print("Getting %s ..." % url)
        self.ygg_browser.open(url)
