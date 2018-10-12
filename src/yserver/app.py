from yserver.core import YggServer
from sys import argv

if len(argv) >= 2:
    fname = argv[1]
else:
    fname = "yserver.cfg"

application = app = YggServer(fname)
