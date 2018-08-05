import unittest
from yggscr import link

class CatTest(unittest.TestCase):

    def test_cat(self):
        for cat in 'jeu-vidéo', 'filmvidéo', 'ebook', 'audio', 'xxx', 'application', 'emulation', 'gps':
            link.get_cat_id(cat)

    def test_subcat(self):
        link.get_cat_id("filmvidéo", "série-tv")
