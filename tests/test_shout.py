import unittest
from yggscr import shout
from bs4 import BeautifulSoup

case_files = "test.txt", "test2.txt", "test3.txt", \
             "test4.txt", "test5.txt", "test6.txt"


class ShoutTest(unittest.TestCase):

    def test_shoutparse(self):
        for tfile in case_files:
            try:
                with open("tests/" + tfile, "r") as fn:
                    html = fn.read()
            except FileNotFoundError:
                continue
            soup = BeautifulSoup(html, 'lxml')
            theshout = shout.ShoutMessage(shout=None, soup=soup)
            print("Parsing %s ==> Shout: <%s> (user <%s>, message <%s>)" %
                  (tfile, theshout, theshout.user, theshout.message))
            print("Html:\n%s\n*****************" % soup.prettify())
