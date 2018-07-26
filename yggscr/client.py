# -*- coding: utf-8 -*-
import socket
from base64 import b64encode
import xmlrpc.client
from transmissionrpc import Client as tclient
from deluge_client import DelugeRPCClient


def rtorrent_add_torrent(rpc_url, torrent_binary=None, torrent_file=None):
    if torrent_binary is None:
        if torrent_file is None:
            return 1
        else:
            with open(torrent_file, "rb") as fh:
                torrent_binary = fh.read()
    try:
        server = xmlrpc.client.ServerProxy(rpc_url)
        server.load.raw_start('', xmlrpc.client.Binary(torrent_binary))
    except (socket.error, xmlrpc.client.Error) as e:
        print("Rtorrent Add torrent exception %s" % e)


def transmission_add_torrent(ip, port, user, password, torrent_binary):
    try:
        tc = tclient(ip, port, user, password)
        tc.add_torrent(b64encode(torrent_binary).decode('ascii'))
    except Exception as e:
        print("Transmission Add torrent exception %s" % e)


def deluge_add_torrent(ip, port, user, password, torrent_binary):
    try:
        client = DelugeRPCClient(ip, int(port), user, password)
        client.connect()
        return client.core.add_torrent_file(
            filename="",
            filedump=b64encode(torrent_binary).decode('ascii'),
            options={})
    except Exception as e:
        print("Deluge Add torrent exception %s" % e)
