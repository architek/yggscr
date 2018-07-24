# from pprint import (PrettyPrinter, pprint)
# pp = PrettyPrinter(indent=4)


def htn(hsize):
    hsize = hsize.upper()
    units = {'KO': 1024, 'MO': 1024**2, 'GO': 1024**3, 'TO': 1024**4}
    try:
        return int(hsize)
    except ValueError:
        return int(float(hsize[:-2]) * units[hsize[-2:]])


class Torrent():
    def __init__(self, torrent_title, torrent_comm, torrent_age, torrent_size,
                 torrent_compl, torrent_seed, torrent_leech, href, thref=None,
                 tid=None, cat=None):
        self.href = href
        self.title = torrent_title
        self.comm = int(torrent_comm)
        self.age = torrent_age
        self.size = torrent_size
        self.nsize = htn(self.size)
        self.compl = int(torrent_compl)
        self.seeders = int(torrent_seed)
        self.leechers = int(torrent_leech)
        self.thref = thref
        self.cat = cat
        if tid:
            self.tid = int(tid)
        else:
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
