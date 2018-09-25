![Travis build](https://travis-ci.org/architek/yggscr.svg?branch=master "Travis")
[![pipeline status](https://framagit.org/torrent/yggscr/badges/master/pipeline.svg)](https://framagit.org/torrent/yggscr/commits/master)

Ygg scraper with:
* **Shell** interface - Any [cmd2](https://github.com/python-cmd2/cmd2 "Python cmd2") features can be used: completion, scripts and much more
* **RSS** feed with torrent using passkey
* **Transmission / Rtorrent / Deluge** add torrent directly from webapp
* **Irc** [limnoria](https://github.com/ProgVal/Limnoria "Limnoria") interface
* Cloud Flare bypass using [cfscrape](https://github.com/Anorov/cloudflare-scrape "cfscrape")
* Http and Socks proxy support

![alt text](https://user-images.githubusercontent.com/490053/43690510-8dc22da8-990b-11e8-902a-ba135ed9e449.png "YggScraper")

## INSTALL

Install with any method you prefer, example

```
sudo apt install python3-setuptools git
git clone https://github.com/architek/yggscr.git
cd yggscr
python3 setup.py install --user
```

_Note_: You need at least setuptools 33.1.1. On jessie you can use official backports

```
echo "deb http://ftp.debian.org/debian/ jessie-backports main contrib non-free" >> /etc/apt/sources.list
sudo apt update
sudo apt install python3-setuptools -t jessie-backports
```

_Note_: If you want the CloudFlare bypass to work, you also need to install *nodejs*


## QUICK START

### Directly from the shell

```
$ yshell
Welcome to Ygg Shell. Type help or ? to list commands.

> help

Documented commands (type help <topic>):
========================================
alias   help           login  print     quit             shell      unalias
edit    history        lscat  proxify   response         shortcuts
exclus  list_torrents  next   py        search_torrents  stats    
get     load           ping   pyscript  set              top_day  

> search_torrents q:cyber c:film s:docu
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

Fill in your settings in defaults.cfg (at least Hostname, Port to listen to, username and password) and launch the server

```bash
./yserver

```

To access webapp, connect to http://localhost:8081 (or any other config you've set)

### Behind apache or nginx using wsgi
The same can be run behind any webserver, here is nginx described:

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
route-run = fixpathinfo:
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
;set-placeholder = ano=true


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
Note that it's possible to run the webapp without any credentials (see uwsgi 'ano' option). The realtime stats will not be shown and its up to the consumer application to provide the authentication cookie (e.g. the browser itself).

You can have as many instances of the webapp running as you have .ini files. An example can be different configurations (anonymous, user1, user2). Each application has its own configuration and nginx can connect to the correct application through the relevant unix socket.

Example for 2 configurations (internal LAN/external WAN):
```
http {
    [...]
	geo $client { 
		default extra;
    		192.168.1.1/24 intra;
  	}
}

upstream _bottle {
    server unix:/run/uwsgi/app/yserver/socket;
}

upstream _bottle_ano {
    server unix:/run/uwsgi/app/yserver-ano/socket;
}

server {
    [...]
	location / {
		uwsgi_read_timeout 20s;
		uwsgi_send_timeout 20s;
        	include uwsgi_params;
		if ( $client = "extra" ) {
        		uwsgi_pass _bottle_ano;
		}
		if ( $client = "intra" ) {
        		uwsgi_pass _bottle;
		}
	}
}
```

_Note_: While the html is very limited for search/rss, the webapp is a "passthrough" relay for unknown parameters. The following is an rss feed about electro musique:

```
https://server.example.com/ano/rssearch?category=audio&sub_category=musique&option_genre%3Amultiple[]=1&option_genre%3Amultiple[]=15&option_genre%3Amultiple[]=33&option_genre%3Amultiple[]=34&option_genre%3Amultiple[]=35&option_genre%3Amultiple[]=119&option_genre%3Amultiple[]=124
```
