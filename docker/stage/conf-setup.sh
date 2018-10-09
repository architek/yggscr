#!/bin/sh
BASE=/opt/yggscr/conf/yserver.cfg
DEST=/opt/yggscr/src/yserver
cp "$BASE" "$DEST"
cat /opt/yggscr/src/yserver/yserver.cfg
exec "$@"
