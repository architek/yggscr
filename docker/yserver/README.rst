Docker Images
-------------

You need docker, and for nginx instance, docker-compose.

Nginx using uwsgi
=================

TODO

Standalone server
=================

This is minimal docker for dev purpose. Internal webserver, don't use this in production.

Usage:

- Modify configuration src/yserver/yserver.cfg [*]_,
- Execute docker/yserver/start_yserver.

   .. [*] For docker use, one setting NEEDS to be changed in src/yserver/yserver.cfg. 
          The default interface to listen is localhost for security reasons. For docker, you need to change that to 0.0.0.0.

The start_yserver script will:

- Download Debian stretch,
- Install setuptools, python3 and C libraries,
- Build the library and entry points binaries.

