# -*- coding: utf-8 -*-
import xmlrpc.client
import socket
from base64 import b64encode
from transmissionrpc import Client as tclient

def rtorrent_add_torrent(rpc_url, torrent_binary=None, torrent_file=None):
    if torrent_binary is None:
        if torrent_file is None:
            return 1
        else:
            with open(torrent_file,"rb") as fh:
                torrent_binary = fh.read()
    try:
        server = xmlrpc.client.ServerProxy(rpc_url)
        server.load.raw_start('', xmlrpc.client.Binary(torrent_binary))
    except (socket.error, xmlrpc.client.Error) as cause:
        print("ERROR: %s" % cause)
        return 1
    else:
        return 0

def transmission_add_torrent(ip, port, torrent_binary):
    try:
        tc = tclient(ip, port)
        tc.add_torrent(b64encode(torrent_binary).decode('ascii'))
        return 0
    except:
        return 1

