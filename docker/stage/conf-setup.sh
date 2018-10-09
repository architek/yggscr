#!/bin/sh
cp /opt/yggscr/conf/yserver.cfg .
sed 's/^;*\s*host\s*=\s*127.0.0.1/host = 0.0.0.0/' -i yserver.cfg
cat yserver.cfg
exec "$@"
