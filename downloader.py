#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import time
import os
import socket
from subprocess import *
import logging
import simplejson as json
#from __future__ import with_statement # This isn't required in Python 2.6

controller_server = ('192.168.1.11', 33334)

# ==================================================================   Функции   ==================================================================== #

def start(data):
    """Запускает wget"""
    cmd = [
        "/usr/bin/wget", 
        data['info']['url'], 
        "-c", 
        "--limit-rate=%s" % data['settings']['speed-limit'], 
        "--timeout=%d" % data['settings']['timeout'], 
        "--tries=%d" % data['settings']['retries'], 
        "-P%s/downloads" % sys.path[0]
    ]
    try:
        olog = open('%s/logs/%d-output.log' % (sys.path[0], data['info']['id']), 'w')
        elog = open('%s/logs/%d-error.log'  % (sys.path[0], data['info']['id']), 'w')
    except IOError as e:
        send_status('CANT_OPEN_LOG_FILES', e)
    else:
        try:
            p = Popen(cmd, stdout=olog, stderr=elog)
            o = p.communicate()
        except OSError, e:
            send_status('WGET_FAILED', e)
        else:
            send_status("FINISHED")
        finally:
            olog.close()
            elog.close()

def stop():
    # надо еще уметь останавливать закачку
    pass

def load_data():
    """Считывает данные для даунлоадера из stdin и преобразует их из json-формата"""
    settings = {} 
    data = sys.stdin.read()
    try:
        settings = json.loads(data)
    except ValueError, e:
        send_status('BAD_DATA', e)
        sys.exit(555)

    return settings

def send_status(status, data = None):
    """Посылает данные о статусе закачки серверу контроллера"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3.0)
    try:
        s.connect(controller_server)
        s.send(json.dumps({'status': status, 'data': data}))
    except socket.error, e:
        l.debug("Не могу послать статус - ошибка сокета: %s" % e)
    #except ValueError, e:
        #l.debug("Socket error: %s" % e)
    else:
        s.close()

def create_daemon():
    """Делает двойной форк"""
    # do the UNIX double-fork magic, see Stevens' "Advanced Programming in the UNIX Environment" for details (ISBN 0201563177)
    # create - fork 1
    try:
        if os.fork() > 0: 
            # exit first parent 
            sys.exit(0)
    except OSError, e:
        #l.debug("fork #1 failed: %d (%s)" % (e.errno, e.strerror))
        send_status('FORK_1_FAILED', e)
        sys.exit(1)

    # it separates the son from the father
    # decouple from parent environment
    os.chdir('/')
    os.setsid()
    os.umask(0)

    # create - fork 2
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            #l.debug('Downloader PID %d' % pid)
            send_status('PID', pid)
            sys.exit(0)
    except OSError, e:
        #l.debug("fork #2 failed: %d (%s)" % (e.errno, e.strerror))
        send_status('FORK_2_FAILED', e)
        sys.exit(1)

# ======================================================================   Тело   =================================================================== #

#time.sleep(7)

logging.basicConfig(filename=sys.path[0]+'/downloader.log', level=logging.DEBUG, format="%(asctime)s - %(name)s - %(message)s")
l = logging.getLogger('downloader')
l.debug('Downloader is started')

if __name__ == '__main__':
    create_daemon()
    l.debug('Daemonized!')

data = load_data()
l.debug('Data: %s' % data)

if data['action'] == 'start':
    start(data)

l.debug('Downloader is stopped')
