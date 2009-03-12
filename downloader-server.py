#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import sys 
import simplejson as json
from subprocess import *
import logging

addr = ('', 33333)

# ==================================================================   Функции   ==================================================================== #

def check_request(data):
    """Проверяет переданные от контроллера данные на корректность

    data = {
        'action' : [start|stop],
        'info' : {'url' : string, 'id': integer, ...},
        'settings' : {'speed-limit': '1k', 'retries': 10, 'timeout': 60, ...}
    }
    """
    required_info = ("id", "url", "description")
    required_settings = ('speed-limit', 'retries', 'timeout')
    checked = True 
    
    for key in required_info:
        if key not in data['info'].keys():
            checked = False
            break

    for key in required_settings:
        if key not in data['settings'].keys():
            checked = False
            break

    if 'action' not in data:
        checked = False

    return checked

def check_downloaders():
    return False 

def send_status(status, data = None):
    try:
        conn.send(json.dumps({'status': status, 'data': data}))
    except socket.error, e:
        l.debug("Не могу вернуть статус - ошибка сокета: %s" % e)
    #except ValueError, e:
        #l.debug("Socket error: %s" % e)

def start_downloader(data):
    """Передает данные даунлоадеру и запускает его"""
    try:
        p = Popen('downloader.py', stdin=PIPE) 
        p.stdin.write(data)
        p.stdin.close()
    except OSError, e:
        send_status('DOWNLOADER_FAILED', e)
    else:
        send_status('DOWNLOADER_STARTED')

# ======================================================================   Тело   =================================================================== #

logging.basicConfig(filename=sys.path[0]+'/downloader.log', level=logging.DEBUG, format="%(asctime)s - %(name)s - %(message)s")
l = logging.getLogger('downloader-server')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(1)

while 1:
    conn, addr = s.accept()

    while 1:
        data = conn.recv(1024)
        if not data: 
            break
        else:
            try:
                request = json.loads(data)
                if check_request(request):
                    if check_downloaders():
                        start_downloader(data)
                    else:
                        send_status('TOO_MANY')
                else:
                    send_status('BAD_REQUEST')
            except ValueError, e:
                send_status('BAD_DATA', e)

    conn.close()
    #break
