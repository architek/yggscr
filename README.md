Gitlab (New repository)

[![master branch status](https://gitlab.teebee.n0n3m.com/yggscr/badges/master/pipeline.svg)](https://gitlab.teebee.n0n3m.com/yggscr/commits/master)

Ygg scraper with:
* **Shell** interface - Any [cmd2](https://github.com/python-cmd2/cmd2 "Python cmd2") features can be used: completion, scripts and much more
* **RSS** feed with torrent using passkey
* **Transmission / rtorrent** add torrent directly from webapp
* **Irc** [limnoria](https://github.com/ProgVal/Limnoria "Limnoria") interface
* Cloud Flare bypass using [cfscrape](https://github.com/Anorov/cloudflare-scrape "cfscrape")
* Http and Socks proxy support

## INSTALL

Install with any method you prefer, example

```bash
python setup.py install --user
```
_Note_: If you want the CloudFlare bypass to work, you also need to install *nodejs*

## QUICK START

### Directly from the shell

```bash
$ yshell
Welcome to Ygg Shell. Type help or ? to list commands.

> help

Documented commands (type help <topic>):
========================================
edit     list_torrents  lscat  print    pyscript  search_torrents  shortcuts
help     load           next   proxify  quit      set              stats    
history  login          ping   py       response  shell

> search_torrents q:cyber,c:film,s:docu
* Cyber guérilla 2.0 (2015) Science&Vie; [VFF] [HDTV] [1080p] x264  [0.93GB] S:26 L:0 | https://yggtorrent.com/torrent/filmvidéo/documentaire/184378-cyber+guérilla+2+0+2015+sciencevie+vff+hdtv+1080p+x264 | None | None
* Infrarouge On Nous Ecoute Partie 1 Cyber guerre L Arme Fatale 2015  [1.11GB] S:6 L:0 | https://yggtorrent.com/torrent/filmvidéo/documentaire/22526-infrarouge+on+nous+ecoute+partie+1+cyber+guerre+l+arme+fatale+2015 | None | None
> stats
EXCEPTION of type 'YggException' occurred with message: 'Not connected'
To enable full traceback, run the following command:  'set debug true'
> login TheBoss Passw0rdz
> stats
Ratio:4.19
Down (GB):73.24
Up (GB):306.66
```

### As an IRC bot

Symlink the YBot subdirectory in your supybot plugin directory.
Ask the bot for help ;-)

### As standalone wsgi server
Fill in your settings in defaults.cfg

```bash
yserver

```

To access webapp, connect to http://localhost:8081

