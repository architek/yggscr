# -*- coding: utf-8 -*-
from base64 import b64encode
import xmlrpc.client
from transmissionrpc import Client as tclient
from deluge_client import DelugeRPCClient


def rtorrent_add_torrent(rpc_url, torrent_binary=None, torrent_file=None):
    if torrent_binary is None:
        if torrent_file is None:
            raise ValueError("Missing parameter")
    with open(torrent_file, "rb") as fh:
        torrent_binary = fh.read()
    server = xmlrpc.client.ServerProxy(rpc_url)
    server.load.raw_start('', xmlrpc.client.Binary(torrent_binary))


def transmission_add_torrent(ip, port, user, password, torrent_binary):
    tc = tclient(ip, port, user, password)
    tc.add_torrent(b64encode(torrent_binary).decode('ascii'))


def deluge_add_torrent(ip, port, user, password, torrent_binary):
    client = DelugeRPCClient(ip, int(port), user, password)
    client.connect()
    return client.core.add_torrent_file(
        filename="",
        filedump=b64encode(torrent_binary).decode('ascii'),
        options={})
