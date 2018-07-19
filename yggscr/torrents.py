# from pprint import (PrettyPrinter, pprint)
# pp = PrettyPrinter(indent=4)


class Torrent():
    def __init__(self, torrent_title, torrent_comm, torrent_age, torrent_size,
                 torrent_compl, torrent_seed, torrent_leech, href, thref, tid):
        self.href = href
        self.title = torrent_title
        self.comm = torrent_comm
        self.age = torrent_age
        self.size = torrent_size
        self.compl = torrent_compl
        self.seeders = torrent_seed
        self.leechers = torrent_leech
        self.thref = thref
        self.tid = tid
        if self.tid is None:
            fn = self.href.split("/")[-1]
            id = fn.split('-')[0]
            try:
                self.tid = int(id)
            except ValueError:
                pass

    def set_id(self, tid):
        self.tid = tid

    def set_tref(self, thref):
        self.thref = thref

    def get_dl_link(self, id=None):
        tmpl = "https://ww1.yggtorrent.is/engine/download_torrent?id=%s"
        return tmpl % id if id is not None else tmpl % self.tid

    def download(self):
        pass

    def __str__(self):
        return "{self.title} [{self.age} Size:{self.size} C:{self.compl} "\
            "S:{self.seeders} L:{self.leechers} Comm:{self.comm}] : "\
            "{self.href} [id {self.tid}]".format(self=self)
