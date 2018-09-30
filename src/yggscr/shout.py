#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
from bs4 import NavigableString

from .ygg import YggBrowser
from .const import SHOUT_URL


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
        if self.shout is not None and self.shout.debug:
            print("Parsing\n%s" % soup.prettify())
        message = ""
        id = soup.get('data-id')
        username = soup.find("a", class_="username ").text.strip()
        group_id = soup.find("a", class_="username ")['user-group-id']
        mtime = soup.time['datetime'][:-5]
        for e in soup.div.contents:
            if isinstance(e, NavigableString):
                message = message + e.string.rstrip('\n\t')
            elif e.name == "img":
                # TODO image with no alt needs at least a space
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

    def get_shouts(self):
        """ Return current shouts from website """
        self.robs.open(SHOUT_URL, timeout=3)
        return [ShoutMessage(soup=li, shout=self)
                for li in list(reversed(
                     [li for li in self.robs.parsed().find_all("li")
                      if li.has_attr('data-id')]
                ))]

    def do_diff(self):
        """ Http Get new shouts, compute and return list of new shouts """
        newshouts = self.get_shouts()
        last_index = None
        self.diffshouts = []
        for shout in newshouts:
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
        self.last_shouts = list(newshouts)
        return self.diffshouts

    def __str__(self):
        """ Print new and removed shouts in a multiline block """
        res = ""
        for removed, shout in self.diffshouts:
            pre = "REMOVED " if removed else ""
            res += "{shout.user}:{pre}{shout.message}\n".format(
                    shout=shout, pre=pre)
        return res


def main():
    import sys
    if len(sys.argv) > 1:
        hfile = sys.argv[1]
        try:
            with open(hfile, "r") as fn:
                html = fn.read()
        except FileNotFoundError:
            print("Can't read file {}".format(hfile))
            exit(1)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        print(soup.get_text())
        exit(0)
    yggshout = YggShout()
    while(True):
        yggshout.get_shouts()
        for removed, shout in yggshout.do_diff():
            pre = "REMOVED" if removed else ""
            shout.message += pre
            print(shout)
        time.sleep(2)


if __name__ == '__main__':
    main()
