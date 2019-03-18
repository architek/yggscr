# from pprint import (PrettyPrinter, pprint)
# pp = PrettyPrinter(indent=4)

from yggscr.const import get_dl_link
from yggscr.link import cat_subcat_from_href
from yggscr.ylogging import init_default_logger


def htn(hsize):
    hsize = hsize.upper()
    units = {'KO': 1024, 'MO': 1024**2, 'GO': 1024**3, 'TO': 1024**4}
    try:
        return int(hsize)
    except ValueError:
        return int(float(hsize[:-2]) * units[hsize[-2:]])


class Torrent():
    def __init__(self, torrent_title, torrent_comm, torrent_age, torrent_size,
                 torrent_completed, torrent_seed, torrent_leech,
                 href, log=None, thref=None,
                 tid=None, cat=None, subcat=None, uploader=None):
        self.href = href
        self.title = torrent_title
        self.comm = int(torrent_comm)
        self.publish_date = torrent_age
        self.nsize = torrent_size
        self.size = htn(self.nsize)
        self.completed = int(torrent_completed)
        self.seed = int(torrent_seed)
        self.leech = int(torrent_leech)
        self.thref = thref
        self.uploader = uploader
        self.log = log or init_default_logger()
        if tid:
            self.tid = int(tid)
        else:
            fn = self.href.split("/")[-1]
            tid = fn.split('-')[0]
            try:
                self.tid = int(tid)
            except ValueError:
                self.tid = 0
        if cat:
            self.cat = cat
        if href:
            self.cat, self.subcat = cat_subcat_from_href(href)
        self.log.debug("Torrent is %s", self)

    def set_id(self, tid):
        self.tid = tid

    def set_tref(self, thref):
        self.thref = thref

    def get_dl_link(self, id=None):
        return get_dl_link(id=id or self.tid)

    def __str__(self):
        return "{self.title} [{self.publish_date} Size:{self.nsize} "\
            "C:{self.completed} S:{self.seed} L:{self.leech} "\
            "Comm:{self.comm} Uploader:{self.uploader}] "\
            ": {self.href} [id {self.tid}]".format(
                self=self)
