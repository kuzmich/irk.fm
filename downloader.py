#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, time
from subprocess import *
import logging
import simplejson as json


def start(data):
    cmd = [
        "/usr/bin/wget", 
        data['info']['url'], 
        "-c", 
        "--limit-rate=%s" % data['settings']['speed-limit'], 
        "--timeout=%d" % data['settings']['timeout'], 
        "-P%s" % sys.path[0]
    ]
    try:
        p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        o = p.communicate()
        _call_controller(o[0] + o[1] , p.returncode)
    except OSError, e:
        _call_controller("Execution failed: %s" % e, 999)

def stop():
    # надо еще уметь останавливать закачку
    print ""

def _load_data():
    settings = {} 

    data = sys.stdin.read()
    try:
        settings = json.loads(data)
    except ValueError, e:
        _call_controller("Кривые данные: %s" % e, 555)
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


def _call_controller(output, code):
    logging.debug("Сообщение: %s" % output)
    logging.debug("Код возврата: %d" % code)

# ====================================================                             ======================================================== #
# Сохранять закачку в случайную директорию (например hash от текущего времени)
#time.sleep(7)

# Отправим привет серверу
print json.dumps({'result' : 'started'})
sys.stdout.flush()

logging.basicConfig(filename=sys.path[0]+'/downloader.log', level=logging.DEBUG, format="%(asctime)s - %(message)s")
logging.debug('Downloader is started')

data = _load_data()
logging.debug('Data: %s' % data)


if data['action'] == 'start':
    if _check_data(data):
        start(data)
    else:
        _call_controller("Не хватает параметров", 444)


logging.debug('Downloader is stopped')
