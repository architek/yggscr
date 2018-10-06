Docker Images
-------------

Two setups are possible:

- Standalone server (yserver)
- Uwsgi app behind nginx

The configuration used is from **src/yserver/yserver.cfg**.

By default, both setups are listening on **tcp/8333**. 

*Note*: 
    For docker use, the if.port setting NEEDS to be changed in yserver.cfg. 
    The script takes care of replacing default by 0.0.0.0.
    Changing port has to be done in the yserver.cfg as well as in the docker file.

Standalone server
=================

The standalone server yserver can be started with docker compose or directly from docker::

    cd ~/git/yggscr
    docker-compose -f docker/docker-compose.yml up yserver

Nginx using uwsgi
=================

Docker-compose is mandatory for container using nginx::

    docker-compose -f docker/docker-compose.yml up nginx

*Note*: If you want to run the uwsgi container behind a reverse proxy on the host, set the socket in the host area with a bind mount.

Stopping
========

If you are using docker-compose::

   docker-compose -f docker/docker-compose.yml down --volumes
