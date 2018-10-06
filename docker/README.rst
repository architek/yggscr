Docker Images
-------------

Two setups are possible:

- Standalone server (yserver)
- Uwsgi app behind nginx

The configuration used is from **src/yserver/yserver.cfg**. By default, both setups are listening on **tcp/8333**.

Standalone server
=================

The standalone server yserver can be started with docker compose or directly from docker::

    cd ~/git/yggscr
    docker-compose -f docker/docker-compose.yml up yserver

Nginx using uwsgi
=================

Docker-compose is mandatory for container using nginx::

    docker-compose -f docker/docker-compose.yml up nginx

*Note*: If you want to run the uwsgi container behind a reverse proxy on the host, set the socket in the host area with a bind mount (either through command line or in uwsgi Dockerfile)

Tweaking
========

To stop everything started by up::

   docker-compose -f docker/docker-compose.yml down --timeout 1 --volumes

You can change nginx host port to *12345* with::

   docker-compose -f docker/docker-compose.yml run -T --publish 12345:80 --rm nginx

*Note*:
    For yserver, the if.port setting NEEDS to be changed in yserver.cfg.  The yserver docker takes care of replacing default by 0.0.0.0.
    Up command will use compose file to set host port, changing port has to be done in the yserver.cfg (only used by yserver) as well as in the yserver or nginx docker file.

Watch logs::

   docker logs -f docker_uwsgi_1
