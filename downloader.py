#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, time
from subprocess import *
import logging
import simplejson as json


def start(settings):
    cmd = [
        "/usr/bin/wget", 
        settings['url'], 
        "-c", 
        "--limit-rate=%s" % settings['speed-limit'], 
        "--timeout=%d" % settings['timeout'], 
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


def _check_settings(settings):
    required_keys = ("id", "url")
    default_settings = {'speed-limit': '1k', 'retries': 10, 'timeout': 60}
    retrieval_settings = default_settings
    retrieval_settings.update(settings)
    checked = False

    for key in required_keys:
        if key not in retrieval_settings.keys():
            break
        checked = True

    return (checked, retrieval_settings)


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

# считаем переданные контроллером настройки и данные
data = sys.stdin.read()
logging.debug('Data: %s' % data)


# Теперь надо разобрать и проверить переданные параметры и получить как минимум url закачки
try:
    settings = json.loads(data)
except ValueError, e:
    _call_controller("Кривой конфиг: %s" % e, 555)
    sys.exit(555)

(checked, settings) = _check_settings(settings)
if checked:
    start(settings)
else:
    _call_controller("Не хватает параметров", 444)


logging.debug('Downloader is stopped')
