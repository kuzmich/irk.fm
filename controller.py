#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import socket
import simplejson as json
import time
import logging

config = sys.path[0] + '/downloader-config.json'
downloader_servers = (('192.168.1.11', 33333),)

def create_download(info):
    """Сохраняет информацию о новой закачке в базу и стартует ее

    info = {
        'url':string,
        'description':string
    }
    """
    info['id'] = _store_download(info) 
    settings = _load_settings(config)
    _start_download(info, settings, downloader_servers[0])

def _start_download(info, settings, location):
    """Соединяется по сокету с download-server.py и передает ему полученные от клиента данные вместе с настройками даунлоадера"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(location)
        s.send(json.dumps({'action': 'start', 'info':info, 'settings':settings}))
        response = s.recv(1024)
    except socket.error, e:
        _update_status("SOCKET_ERROR", e)
    else:
        s.close()
        update_status(response)

def _load_settings(config):
    """Загружает настройки даунлоадера из файла config"""
    settings = {}
    try:
        f = open(config)
        try:
            settings = json.load(f)
        except ValueError, e:
            _update_status("BAD_CONFIG", e)
            sys.exit(333)
        finally:
            f.close()
    except IOError, e:
        _update_status("CANT_OPEN_CONFIG", e)
        sys.exit(444)
    else:
        return settings

def on_finish(id, result):
    pass

def _store_download(info):
    return 3333

def _update_download(id, status):
    pass

def _update_status(status, data = None):
    l.debug("Статус: %s; Данные: %s" % (status, data))
    

def update_status(data):
    try:
        data = json.loads(data)
        if 'status' in data and 'data' in data:
            _update_status(data['status'], data['data'])
        else:
            l.error("Пришел странный статус")
    except ValueError, e:
        l.error("Пришел кривой статус: %s", e)


logging.basicConfig(filename=sys.path[0]+'/downloader.log', level=logging.DEBUG, format="%(asctime)s - %(name)s - %(message)s")
l = logging.getLogger('controller')
