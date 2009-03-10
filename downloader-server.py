#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket, simplejson as json
from subprocess import *
import pdb

addr = ('', 33333)
answers = {
    'OK': (0, 'OK'), 
    'BAD_DATA': (1, 'BAD_DATA'), 
    'BAD_REQUEST': (2, 'BAD_REQUEST'), 
    'TOO_MANY': (3, 'TOO_MANY'),
    'WGET_FAILED': (4, 'WGET_FAILED'),
} 

def check_request(data):
    """Проверяет переданные от контроллера данные на корректность

    data = {
        'action' : [start|stop],
        'info' : {'url' : string, 'id': integer, ...},
        'settings' : {'speed-limit': '1k', 'retries': 10, 'timeout': 60, ...}
    }
    """
    required_info = ("id", "url")
    required_settings = ('speed-limit', 'retries', 'timeout')
    checked = False
    #pdb.set_trace()
    
    # проверить на action тоже

    for key in required_info:
        if key not in data['info'].keys():
            checked = False
            break
        else:
            checked = True

    for key in required_settings:
        if key not in data['settings'].keys():
            checked = checked and False
            break
        else:
            checked = checked and True 

    return checked

def check_downloaders():
    return True 

def send_response(response):
    try:
        data = json.dumps(response)
        conn.send(data)
    except:
        pass

def start_downloader(data):
    try:
        p = Popen('downloader.py', stdin=PIPE) 
        p.stdin.write(data)
        p.stdin.close()
    except OSError, e:
        send_response(answers['WGET_FAILED'])
    else:
        send_response(answers['OK'])


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
                if check_request(request) :
                    #if request['action'] == 'start'
                    if check_downloaders():
                        start_downloader(data)
                    else:
                        send_response(answers['TOO_MANY'])
                else:
                    send_response(answers['BAD_REQUEST'])
            except ValueError, e:
                send_response(answers['BAD_DATA'])

    conn.close()
    #break
