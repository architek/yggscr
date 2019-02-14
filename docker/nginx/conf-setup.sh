#!/bin/sh
cp /opt/yggscr/conf/ygg.conf /etc/nginx/conf.d/default.conf
exec "$@"
