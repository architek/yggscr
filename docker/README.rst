Docker Images
-------------

Two setups are possible:

- Uwsgi app behind an http server acting as a reverse proxy (only nginx image provided)
- Uwsgi app with its own http server

Docker hub
==========

Images are available on docker hub::

   docker pull architek/yggscr

   # Optional if you want nginx
   docker pull architek/nginx
   
   # Optional if you want to have yggscr access website with tor
   docker pull architek/docker-tor-socks

For configuration, see chapter below.

Configuration
=============

The default configuration is sufficient for anonymous access, without proxy and without any interface to bittorrent clients.

To override this, you can bind mount a directory on your host to /opt/yggscr/conf in the container and create any (or all) of the following files:

- *yserver.cfg* is the torrent/ygg configuration.
- *ygg.ini* is the uwsgi configuration which creates the mapping between nginx and the application. In this file, you can for example set the yserver.cfg file to be used.
- *ygg.conf* is the nginx configuration used by the nginx container (replaces /etc/nginx/conf.d/default.conf).

Finally you can also override the filename *ygg.ini* by setting an env variable WSGI_INI in yggscr container (for example *ygg-my.ini*)

Keep in mind that all files in your host directory will be copied to the container (but not its subdirectories). 

This allows having a single reverse proxy in front of several uwsgi applications.

Manual install
==============

- Download latest GitHub release at https://github.com/architek/yggscr/releases/latest or better using git::

   git clone https://github.com/architek/yggscr.git && cd yggscr

   # To get updates
   git pull

Start Stop
==========

If you want to stay on the command line:

Nginx using uwsgi::

   docker-compose -f docker/docker-compose.yml up yggscr nginx
   [...]
   docker-compose -f docker/docker-compose.yml down --timeout 1 --volumes

You can change nginx host port to *12345* with::

   docker-compose -f docker/docker-compose.yml run -T --publish 12345:80 --rm nginx

In this mode, yggscr does not open any TCP port.

Standalone server:

The standalone server can be started when you override command with::

   docker-compose -f docker/docker-compose.yml run -p <host port>:8333 stage python -m yserver.__main__

In standalone configuration, the server by defaults listens on 127.0.0.1 for security reasons. When running a container, this adress is changed to 0.0.0.0 automatically.
