#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, socket, simplejson as json

config = sys.path[0] + '/downloader.conf'
locations = (('192.168.1.11', 33333),)
urls = (
    'http://www.stephenzunes.org/vitae08.doc', 
    "http://docs.python.org/ftp/python/doc/current/python-2.6.1-docs-pdf-a4.tar.bz2",
    'http://dfn.dl.sourceforge.net/sourceforge/psi/psi-0.12-win-setup-1.exe'
)

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
    s.settimeout(10.0)
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


