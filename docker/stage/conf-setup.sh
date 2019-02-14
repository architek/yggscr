#!/bin/sh
cp /opt/yggscr/conf/* .
sed 's/^;*\s*host\s*=\s*127.0.0.1/host = 0.0.0.0/' -i yserver.cfg
addgroup -g $DEF_GUID host_group
adduser uwsgi host_group

exec "$@"
