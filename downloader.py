#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, time, os
from subprocess import *
import logging
import simplejson as json
#from __future__ import with_statement # This isn't required in Python 2.6


def start(data):
    cmd = [
        "/usr/bin/wget", 
        data['info']['url'], 
        "-c", 
        "--limit-rate=%s" % data['settings']['speed-limit'], 
        "--timeout=%d" % data['settings']['timeout'], 
        "-P%s/downloads" % sys.path[0]
    ]
    try:
        olog = open('%s/logs/%d-output.log' % (sys.path[0], data['info']['id']), 'w')
        elog = open('%s/logs/%d-error.log'  % (sys.path[0], data['info']['id']), 'w')
    except IOError as e:
        log("Execution failed: %s" % e, 888)
    else:
        try:
            p = Popen(cmd, stdout=olog, stderr=elog)
            o = p.communicate()
        except OSError, e:
            log("Execution failed: %s" % e, 999)
        finally:
            olog.close()
            elog.close()

def stop():
    # надо еще уметь останавливать закачку
    pass

def _load_data():
    settings = {} 

    data = sys.stdin.read()
    try:
        settings = json.loads(data)
    except ValueError, e:
        log("Кривые данные: %s" % e, 555)
        sys.exit(555)

    return settings

def _check_data(data):
    """Проверяет переданные от контроллера данные на корректность

    data = {
        'action' : [start|stop]
        'info' : {'url' : string, 'id': integer, ...},
        'settings' : {'speed-limit': '1k', 'retries': 10, 'timeout': 60, ...}
    }
    """
    required_info = ("id", "url")
    #required_settings = {'speed-limit': '1k', 'retries': 10, 'timeout': 60}
    required_settings = ('speed-limit', 'retries', 'timeout')
    checked = False

    #settings = required_settings
    #settings.update(data['settings'])
    #data['settings'] = settings

    for key in required_info:
        if key not in data['info'].keys():
            break
        checked = True

    for key in required_settings:
        if key not in data['settings'].keys():
            break
        checked = checked and True 

    #return (checked, data)
    return checked

def log(output, code):
    logging.debug("Сообщение: %s" % output)
    logging.debug("Код возврата: %d" % code)

def create_daemon():
    # do the UNIX double-fork magic, see Stevens' "Advanced Programming in the UNIX Environment" for details (ISBN 0201563177)
    # create - fork 1
    try:
        if os.fork() > 0: 
            # exit first parent 
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
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
            print 'Daemon PID %d' % pid
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)


# ====================================================                             ======================================================== #
#time.sleep(7)

logging.basicConfig(filename=sys.path[0]+'/downloader.log', level=logging.DEBUG, format="%(asctime)s - %(message)s")
logging.debug('Downloader is started')

if __name__ == '__main__':
    create_daemon()
    logging.debug('Daemonized!')

data = _load_data()
logging.debug('Data: %s' % data)

# Отправим привет серверу
print json.dumps({'result' : 'starting'})
#sys.stdout.flush()

if data['action'] == 'start':
    if _check_data(data):
        start(data)
    else:
        log("Не хватает параметров", 444)

logging.debug('Downloader is stopped')
