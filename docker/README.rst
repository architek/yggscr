Docker Images
-------------

Two setups are possible:

- Uwsgi app behind nginx
- Standalone server (yserver)

Quick Start
-----------

- Download latest GitHub release at https://github.com/architek/yggscr/releases/latest::

   git clone https://github.com/architek/yggscr.git && cd yggscr

- Use either of the two setups (see below)


Nginx using uwsgi
=================

Docker-compose is mandatory for container using nginx::

   docker-compose -f docker/docker-compose.yml up nginx

*Note*: If you want to run the uwsgi container behind a reverse proxy on the host, set the socket in the host area with a bind mount (either through command line or in uwsgi Dockerfile)

Standalone server
=================

The standalone server yserver can be started with docker-compose (or directly with docker)::

   docker-compose -f docker/docker-compose.yml run -p 8333:8333 stage python -m yserver.__main__

Tweaking
========

Configuration files are in conf/

- yserver.cfg is the torrent/ygg conf. You need to change some settings there.

For nginx setup:
- ygg.conf is the nginx conf
- ygg.ini is the wsgi conf


To stop everything started by up::

   docker-compose -f docker/docker-compose.yml down --timeout 1 --volumes

You can change nginx host port to *12345* with::

   docker-compose -f docker/docker-compose.yml run -T --publish 12345:80 --rm nginx

*Note*:
    For yserver, the if.port setting NEEDS to be changed in yserver.cfg.  The yserver docker takes care of replacing default by 0.0.0.0.
    Up command will use compose file to set host port, changing port has to be done in the yserver.cfg (only used by yserver) as well as in the yserver or nginx docker file.

