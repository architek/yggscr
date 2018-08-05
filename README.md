Gitlab (New repository)

[![master branch status](https://gitlab.teebee.n0n3m.com/yggscr/badges/master/pipeline.svg)](https://gitlab.teebee.n0n3m.com/yggscr/commits/master)

Ygg scraper with:
* **Shell** interface - Any [cmd2](https://github.com/python-cmd2/cmd2 "Python cmd2") features can be used: completion, scripts and much more
* **RSS** feed with torrent using passkey
* **Transmission / Rtorrent / Deluge** add torrent directly from webapp
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

### As standalone web server
This server allows searching, downloading torrent file, sending to rtorrent,transmission or deluge client and authenticated RSS.

Fill in your settings in defaults.cfg (at least Hostname, Port to listen to)

```bash
yserver

```

To access webapp, connect to http://localhost:8081 (or any other config you've set)

### Behind nginx using wsgi

```bash
apt install uwsgi uwsgi-plugin-python3
```

Create nginx vhost
```
upstream _bottle {
    server unix:/run/uwsgi/app/yserver/socket;
}

server {
    server_name ygg.com;
    root /var/www;

    listen 80;
    listen [::]:80;
    
    location / {
        # restrict to 192.168.1.0/24
        allow 192.168.1.1/24;
        deny all;
        uwsgi_read_timeout 20s;
        uwsgi_send_timeout 20s;
        include uwsgi_params;
        uwsgi_pass _bottle;
    }
}
```
Create file /etc/uwsgi/apps-available/yserver.ini

```
[uwsgi]
socket = /run/uwsgi/app/yserver/socket
chdir = /var/www/bottle/yserver/
master = true
file = yserver
uid = www-data
gid = www-data
;debug = true
;reloader = true
;catch-all = false
workers = 2
threads = 4
plugins = python3
socket-timeout = 6000000

```

Create directories

```bash
mkdir -p /run/uwsgi/app/yserver
chown www-data:www-data /run/uwsgi/app/yserver
mkdir -p /var/www/bottle/yserver/   # or wherever the tree yserver/ is 
```

Edit yserver.cfg to fit to your need

Enable uwsgi app and reload nginx

```bash
cd /etc/uwsgi/apps-enabled
ln -s ../apps-available/yserver.ini
systemctl restart uwsgi.service
systemctl restart nginx
```




