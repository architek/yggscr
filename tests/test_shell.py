import unittest
from yggscr import shell


class MyTest(unittest.TestCase):
    def testload(self):
        y = shell.YggShell()
