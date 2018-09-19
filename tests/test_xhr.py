import unittest
from yggscr.ygg import YggBrowser


class XhrTest(unittest.TestCase):

    def test_top_day(self):
        ygg = YggBrowser()
        for torrent in sorted(ygg.top_day(), key=lambda k: k.cat):
            print("* %s %s" % (torrent.cat, torrent))
