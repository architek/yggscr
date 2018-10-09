# Docker file for wsgi ygg app


Configure settings by mounting your local file yserver.cfg to /opt/yggscr/conf/yserver.cfg in the container.

Otherwise, default options for user, network and client are used.


* If you want to run this standalone, use this run command:

``` python -m yserver.__main__

* Otherwise, by default it will communicate through unix socket to nginx container (see nginx image)
