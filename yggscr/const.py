# -*- coding: utf-8 -*-

# Normally not needed because of http redirect
YGG_HOST = "ww3.yggtorrent.is"

YGG_HOME = "https://" + YGG_HOST

DL_TPL = YGG_HOME           + "/engine/download_torrent?id={id}"
TORRENT_URL = YGG_HOME      + "/torrents/"
SEARCH_URL = YGG_HOME       + "/engine/search"
TOP_DAY_URL = YGG_HOME      + "/engine/ajax_top_query/day"
TOP_WEEK_URL = YGG_HOME     + "/engine/ajax_top_query/week"
TOP_MONTH_URL = YGG_HOME    + "/engine/ajax_top_query/month"
TOP_SEED_URL = YGG_HOME     + "/engine/mostseeded"
RSS_TPL = YGG_HOME          + "/rss?type=1&parent_category={category}"
SHOUT_URL = YGG_HOME        + "/forum/index.php?shoutbox/refresh"
