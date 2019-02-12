###
# Copyright (c) 2018, Laurent
# All rights reserved.
#
###

import yggscr
import requests
import threading
from time import sleep, time
from hashlib import sha256
import supybot.ircdb as ircdb   #noqa
from supybot.commands import (wrap, optional)
import supybot.callbacks as callbacks
from yggscr.ygg import YggBrowser
from yggscr.link import list_cat_subcat
from yggscr.shout import (YggShout, ShoutMessage)
from yggscr.exceptions import YggException
from collections import defaultdict
# import supybot.utils as utils
# import supybot.plugins as plugins
import supybot.ircutils as ircutils
from bs4 import BeautifulSoup
from logging import INFO, DEBUG  #noqa

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('YBot')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    def _(x):
        return x

shout_err = 0


class YBot(callbacks.Plugin):
    """sup ygg bot"""
    threaded = True

    def __init__(self, irc):
        global shout_err

        self.__parent = super(YBot, self)
        self.__parent.__init__(irc)
        self.yggb = YggBrowser(loglevel=DEBUG)
        self.yggb.proxify("socks5h://192.168.1.9:9100")
        self.shout = YggShout(self.yggb)
        shout_err = 0
        self.col = dict()

    def yggv(self, irc, msg, args):
        """
        Prints the plugin version
        """
        irc.reply(yggscr.__version__)
    yggv = wrap(yggv)

    def yconn(self, irc, msg, args):
        """
        Print connection details
        """
        irc.reply("{}".format(self.yggb))
    yconn = wrap(yconn)

    def yprox(self, irc, msg, args, https_proxy):
        """[https proxy]
        Sets or removes proxy (http, socks, ..)
        """
        if https_proxy:
            self.yggb.proxify(https_proxy)
        else:
            self.yggb.proxify(None)
        irc.replySuccess()
    yprox = wrap(yprox, ['owner', optional('anything')])

    def ysearch(self, irc, msg, args, n, detail, p):
        """[n:nmax] [detail True/False] q:pattern [c:cat [s:subcat]] [opt:val]*
        Searches on ygg and return first page results -
        Will only return the first nmax results and waits 1s between each reply
        """
        q = {}
        try:
            for t in p.split():
                k, v = t.rsplit(':', 1)
                if k in q.keys():
                    if isinstance(q[k], list):
                        q[k].append(v)
                    else:
                        q[k] = [q[k], v]
                else:
                    q[k] = v
        except ValueError:
            irc.error("Wrong syntax")
            pass
            return

        q['name'] = q.pop('q')
        q['category'] = q.pop('c', "")
        q['sub_category'] = q.pop('s', "")

        if n is None:
            n = 3
        if detail is None:
            detail = False

        try:
            torrents = self.yggb.search_torrents(
                detail=detail, q=q, nmax=int(n))
        except (requests.exceptions.ProxyError,
                requests.exceptions.ConnectionError) as e:
            irc.error("Network Error: %s" % e)
            return
        except YggException as e:
            irc.error("Ygg Exception raised: %s" % e)
            return
        if torrents is None:
            irc.reply("No results")
            return
        for idx, torrent in enumerate(torrents[:n]):
            sleep(1)
            irc.reply("%2d - %s [%s Size:%s C:%s S:%s L:%s Comm:%s Uploader:%s] : %s" %
                      (1+idx, torrent.title, torrent.publish_date, torrent.size,
                       torrent.completed, torrent.seed, torrent.leech,
                       torrent.comm, torrent.uploader, torrent.href))
    ysearch = wrap(ysearch,
                   [optional('int'), optional('boolean'), 'text'])

    def ycat(self, irc, msg, args):
        """Will list available cat/subcat combinaisons
        """
        irc.reply("Available (cat, subcat) combinaisons:{}".
                  format(list_cat_subcat()))
    ycat = wrap(ycat)

    def ylogin(self, irc, msg, args, yuser, ypass):
        """[user pass]
        Logins to ygg using given credentials or stored one
        """
        if not yuser and not ypass:
            yuser = self.registryValue('cred.user')
            ypass = self.registryValue('cred.pass')
            if not yuser or not ypass:
                irc.error("You need to set cred.user and cred.pass")
                return
        elif not ypass:
            irc.error("Wrong syntax")
            return
        try:
            self.yggb.login(yuser, ypass)
        except (requests.exceptions.ProxyError,
                requests.exceptions.ConnectionError) as e:
            irc.error("Network Error: %s" % e)
            return
        except YggException as e:
            irc.error("Ygg Exception raised: %s" % e)
            return
        except Exception as e:
            irc.error("Could not login to Ygg with credentials: %s" % e)
            return
        irc.replySuccess()
        self.log.info("Connected as {}".format(yuser))
    ylogin = wrap(ylogin, ['owner', optional('anything'), optional('anything')])

    def ylogout(self, irc, msg, args):
        """
        Logout from ygg
        """
        self.yggb.logout()
        irc.replySuccess()
    ylogout = wrap(ylogout, ['owner'])

    def ystats(self, irc, msg, args):
        """
        Return ratio stats
        """
        if self.yggb.idstate == "Anonymous":
            irc.error("You need to be authenticated at ygg")
        else:
            try:
                r = self.yggb.stats()
            except (requests.exceptions.ProxyError,
                    requests.exceptions.ConnectionError) as e:
                irc.error("Network Error: %s" % e)
                return
            except YggException as e:
                irc.error("Ygg Exception raised: %s" % e)
                return
            except Exception as e:
                irc.error("Could not get stats: %s" % e)
                return
            irc.reply('↑ {:7.2f}GB ↓ {:7.2f}GB % {:6.4f}'.
                      format(r['up'], r['down'], r['ratio']))
            irc.reply(
                '↑ Instant {}KBps Mean {}KBps ↓ Instant {}KBps Mean {}KBps'.
                format(r['i_up'], r['m_up'], r['i_down'], r['m_down']))
    ystats = wrap(ystats)

    def yresp(self, irc, msg, args):
        """
        Print http response on console
        """
        self.log.info("ygg request response:%s" % self.yggb.response())
        irc.replySuccess()
    yresp = wrap(yresp)

    def yping(self, irc, msg, args, n, quiet):
        """[n] [quiet: boolean(default False)]
        GET /
        """
        t = []
        statuses = defaultdict(int)
        mmin, mmax, mmean = float("inf"), float("-inf"), float("inf")

        if n is None:
            n = 1
        if n > 100:
            n = 100
        if n > 10 and quiet is False:
            n = 10

        for _ in range(n):
            try:
                t1 = time()
                sts = self.yggb.ping()
                t2 = time()
                dt = 1000*(t2-t1)
                mmax = max(mmax, dt)
                mmin = min(mmin, dt)
                t.append(dt)
                if not quiet:
                    irc.reply("{:>2} ping {} time={:>7.2f}ms http {}".format(
                        1+_ if n > 1 else "", self.yggb.browser.url, dt, sts), prefixNick=False)
                statuses[sts] += 1
            except Exception as e:
                pass
                mmax = float("inf")
                irc.reply("{:>2} timeout! [{}]".format(1+_, e), prefixNick=False)
        if n == 1:
            return
        if t:
            mmean = sum(t)/len(t)
        str_statuses = ' | '.join('{}:{}'.format(key, value) for key, value in statuses.items())
        irc.reply("{} packet{} transmitted, {} received, {:.2%} packet loss, http codes {}".
                  format(n, "s" if n > 1 else "", len(t), 1-len(t)/n, str_statuses), prefixNick=False)
        irc.reply("rtt min/avg/max = {:.2f}/{:.2f}/{:.2f} ms".
                  format(mmin, mmean, mmax), prefixNick=False)

    yping = wrap(yping, [optional('PositiveInt'), optional('boolean')])

    def colorize_user(self, user, group, w_colour):

        colours = ('blue',
                   'green',
                   'brown',
                   'purple',
                   'orange',
                   'yellow',
                   'light green',
                   'teal',
                   'light blue',
                   'pink',
                   'dark gray',
                   'light gray')

        # 1: unknown, 2: Membre, 3: supermod, 4: mod, 5: tp, 8: nouveau membre, 9: desactivé
        gcolours = {1: 'blue', 3: 'orange', 4: 'green', 5: 'pink', 8: 'purple', 9: 'brown'}

        # Don't colorize members unless w_colour for color tracking
        if group == 2:
            if w_colour:
                hash = sha256()
                hash.update(user.encode())
                hash = hash.digest()[0]
                hash = hash % len(colours)
                user = ircutils.mircColor(user, colours[hash])
            else:
                pass
        elif group not in gcolours.keys():
            user = ircutils.mircColor(user, gcolours[1])
        else:
            user = ircutils.mircColor(user, gcolours[group])

        # High grade in bold
        if group in [1, 3, 4, 5]:
            user = ircutils.bold(user)
        return user

    def shoutify(self, shout, w_colour):
        user = "{0: >12}".format(shout.user)
        user = self.colorize_user(user, shout.group, w_colour)
        fmt = self.registryValue('shout.fmt')
        msg = shout.message.replace('\n', ' ').replace('\n', ' ')
        return fmt.format(time=shout.mtime, id=shout.id, fuser=user, user=shout.user, group=shout.group, message=msg)

    def yshout(self, irc, msg, args, n, w_colour=False, hfile=None):
        """[int n] [boolean user_colorized] [injected html file]
        Print last shout messages and detects gap. Time is UTC.
        User will be colorized if boolean is True.
        """
        global shout_err
        rate_err = self.registryValue('shout.rate_err')
        if hfile:
            try:
                with open(hfile, "r") as fn:
                    html = fn.read()
            except:
                irc.error("Can't read file %s" % hfile)
                return
            shout = ShoutMessage(shout=None, soup=BeautifulSoup(html, 'html.parser'))
            irc.reply(self.shoutify(shout, False), prefixNick=False)
            return
        try:
            self.shout.get_shouts()
            diff = self.shout.do_diff()
            shout_err = 0
        except Exception as e:
            self.log.info("Could not dump shout, aborting. Error %s. Tid %s" % (e, threading.get_ident()))
            shout_err += 1
            if shout_err % rate_err == 0:
                irc.error("Shout ({} messages suppressed) (Exception {})".format(rate_err, e))
                irc.error("Connection details: {}".format(self.yggb))
            return
        if n is None:
            n = len(diff)
        for removed, shout in diff[len(diff)-n:]:
            prefix = "REMOVED!!: " if removed else ""
            irc.reply(
                    prefix + self.shoutify(shout, w_colour), prefixNick=False)
            sleep(1)
    yshout = wrap(yshout, ['owner', optional('int'), optional('boolean'), optional('filename')])


Class = YBot


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
