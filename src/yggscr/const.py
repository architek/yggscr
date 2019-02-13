# -*- coding: utf-8 -*-
import requests
from urllib.parse import urlsplit

YGG_HOST = "www2.yggtorrent.gg"   # YGG_HOST = "www.yggtorrent.gg" Waiting for ygg to correct their webserver...
YGG_HOME = "https://" + YGG_HOST


def detect_redir():
    global YGG_HOME, DL_TPL, TORRENT_URL, SEARCH_URL, TOP_DAY_URL, TOP_WEEK_URL, TOP_MONTH_URL, \
           EXCLUS_URL, TOP_SEED_URL, RSS_TPL, SHOUT_URL
    ir = requests.get(YGG_HOME, allow_redirects=False)
    if ir.status_code in [307, 301]:
        url = ir.headers['Location']
        split_url = urlsplit(url)
        YGG_HOME = "{}://{}".format(split_url.scheme, split_url.netloc)
    DL_TPL = YGG_HOME           + "/engine/download_torrent?id={id}"
    TORRENT_URL = YGG_HOME      + "/torrents/"
    SEARCH_URL = YGG_HOME       + "/engine/search"
    TOP_DAY_URL = YGG_HOME      + "/engine/ajax_top_query/day"
    TOP_WEEK_URL = YGG_HOME     + "/engine/ajax_top_query/week"
    TOP_MONTH_URL = YGG_HOME    + "/engine/ajax_top_query/month"
    EXCLUS_URL = YGG_HOME       + "/torrents/exclus"
    TOP_SEED_URL = YGG_HOME     + "/engine/mostseeded"
    RSS_TPL = YGG_HOME          + "/rss?type=1&parent_category={category}"
    SHOUT_URL = YGG_HOME        + "/forum/index.php?shoutbox/refresh"


def get_dl_link(id):
    return DL_TPL.format(id=id)


detect_redir()
