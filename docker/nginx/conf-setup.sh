#!/bin/sh
cat /opt/yggscr/conf/ygg.conf
cp /opt/yggscr/conf/ygg.conf /etc/nginx/conf.d/default.conf
exec "$@"
