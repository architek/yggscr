# Docker file for wsgi ygg app

[![](https://images.microbadger.com/badges/image/architek/yggscr.svg)](https://microbadger.com/images/architek/yggscr "Get your own image badge on microbadger.com") [![](https://images.microbadger.com/badges/version/architek/yggscr.svg)](https://microbadger.com/images/architek/yggscr "Get your own version badge on microbadger.com")

Configure settings by mounting your local file yserver.cfg to /opt/yggscr/conf/yserver.cfg in the container.

Otherwise, default options for user, network and client are used.


* The app uwsgi will communicate through unix socket to nginx container (see nginx image for an example)

* If you want to run this standalone without nginx, simply use this as parameter to run command: `python -m yserver.__main__`

