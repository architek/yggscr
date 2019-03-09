# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
from bs4 import NavigableString

from .ygg import YggBrowser
from .const import SHOUT_URL
import requests
import socket
import sys


class ShoutMessage(object):

    def __init__(self, shout, soup=None, mtime=None,
                 user=None, group=None, message=None):
        """ shout : parent object """
        self.shout = shout
        self.soup = soup
        if mtime and user and group and message:
            self.mtime = mtime
            self.user = user
            self.group = int(group)
            self.message = message
        elif soup:
            self.mtime, self.id, self.user, \
                self.group, self.message = self.parse_shout(soup)

    def __str__(self):
        return '{self.mtime} : {self.user:>12}: {self.message}'.format(self=self)

    def __eq__(self, other):
        return self.mtime == other.mtime and self.user == other.user \
            and self.group == other.group and self.message == other.message

    def parse_shout(self, soup):
        message = ""
        id = soup.get('data-id')
        username = soup.find("a", class_="username").text.strip()
        group_id = soup.find("a", class_="username")['user-group-id']
        mtime = soup.time['datetime'][:-5]
        for e in soup.div.contents:
            if isinstance(e, NavigableString):
                message = message + e.string.rstrip('\n\t')
            elif e.name == "img":
                disp = " {} ".format(e["alt"]) if e["alt"] else " "
                message = message + disp
            elif e.has_attr("class") and e.get("class")[0] .strip() == "username":
                    message = message + e.string
            elif e.name == "a":
                message = message + e["href"]
        return mtime, id, username, int(group_id), str(message)


class YggShout:
    def __init__(self, robs=None, debug=False, irc=False, colour=False):
        self.robs = robs or YggBrowser()
        self.irc = irc
        self.colour = colour
        self.last_shouts = []
        self.debug = debug
        self.diffshouts = []

    def get_shouts(self):
        """ Set current shouts from website """
        self.robs.open(SHOUT_URL, timeout=3)
        self.new_shouts = [ShoutMessage(soup=li, shout=self)
                           for li in list(reversed(
                            [li for li in self.robs.parsed().find_all("li")
                                if li.has_attr('data-id')]
                           ))]

    def do_diff(self):
        """ Compute and return list of new shouts """
        last_index = None
        self.diffshouts = []
        for shout in self.new_shouts:
            try:
                index = self.last_shouts.index(shout)
            except ValueError:
                self.diffshouts.append([False, shout])
            else:
                if last_index is not None:
                    if last_index != (index-1):
                        for i in range(last_index+1, index-1):
                            self.diffshouts.append([True, self.last_shouts[i]])
                last_index = index
        self.last_shouts = self.new_shouts
        return self.diffshouts

    def __str__(self):
        """ Print new and removed shouts in a multiline block """
        res = ""
        for removed, shout in self.diffshouts:
            pre = "REMOVED " if removed else ""
            res += "{shout.user}:{pre}{shout.message}\n".format(
                    shout=shout, pre=pre)
        return res


def parse_file(hfile):
    with open(hfile, "r") as fn:
        html = fn.read()
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.get_text())


yggshout = None


def main_loop():
    global yggshout
    nt = 0
    while nt < 10:
        try:
            if yggshout is None:
                yggshout = YggShout()
                print("Started")
            if nt == 5:
                print("Max retries reached... Reconnecting")
                yggshout = YggShout()
                time.sleep(1)
            yggshout.get_shouts()
            break
        except (requests.exceptions.Timeout, socket.timeout) as e:
            dt = 1 + 15*(nt % 5)
            if nt > 0:
                print("ERROR: Can't get shout messages... [{}] - Trying again in {}s...".format(e, dt))
            time.sleep(dt)
            nt += 1
        except requests.exceptions.ConnectionError as e:
            print("Connection error...[{}]".format(e))
            nt += 1
    if nt >= 10:
        print("FATAL: No connection")
        sys.exit(2)
    elif nt > 1:
        print("Reconnected")
    for removed, shout in yggshout.do_diff():
        if removed:
            shout.message += "<-- REMOVED"
        print(shout)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    if len(argv) > 1:
        hfile = argv[1]
        try:
            parse_file(hfile)
        except (FileNotFoundError, IsADirectoryError) as e:
            print("Can't read file, {}".format(e))
            sys.exit(1)
    else:
        while True:
            try:
                main_loop()
                time.sleep(15)
            except KeyboardInterrupt:
                return
