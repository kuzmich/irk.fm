#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, socket, simplejson as json
import time

config = sys.path[0] + '/downloader.conf'
locations = (('192.168.1.11', 33333),)

def create_download(info):
    """Сохраняет информацию о новой закачке в базу и стартует ее

    info = {
        'url':string,
        'description':string
    }
    """
    info['id'] = _store_download(info) 
    settings = _load_settings()
    _start_download(info, settings, locations[0])

def _start_download(info, settings, location):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(location)
        s.send(json.dumps({'action': 'start', 'info':info, 'settings':settings}))
        response = s.recv(1024)
    except socket.error, e:
        print "Socket error: ", e
    else:
        s.close()
        print response 

def _load_settings():
    settings = {}
    try:
        f = open(config)
        try:
            settings = json.load(f)
        except ValueError, e:
            print "Кривой конфиг"
            sys.exit(333)
        finally:
            f.close()
    except IOError, e:
        print "Ну и где конфиг?"
        sys.exit(444)
    else:
        return settings

def on_finish(id, result):
    pass

def _store_download(info):
    return 3333

def _update_download(info):
    pass


