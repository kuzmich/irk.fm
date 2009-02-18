#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, logging, simplejson as json
from subprocess import *

def start(url):
  cmd = ["/usr/bin/wget", url, "-c", "--limit-rate=1k", "--timeout=3", "-P", sys.path[0]]
  try:
    p = Popen(cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    o = p.communicate()
    call_controller(o[0] + o[1] , p.returncode)
  except OSError, e:
    call_controller("Execution failed: %s" % e, 999)

def stop():
  # надо еще уметь останавливать закачку
  print ""

def call_controller(output, code):
  logging.debug("Сообщение: %s" % output)
  logging.debug("Код возврата: %d" % code)

# ====================================================                             ======================================================== #

# Сначала надо разобрать переданные параметры и получить как минимум url закачки
# Сохранять закачку в случайную директорию (например hash от текущего времени)

# Отправим привет серверу
#  print json.dumps({'result' : 'OK', 'url':data['url']})
print json.dumps({'result' : 'OK'})
sys.stdout.flush()

data = sys.stdin.read()
settings = json.loads(data)

logging.basicConfig(filename=sys.path[0]+'/downloader.log', level=logging.DEBUG, format="%(asctime)s - %(message)s")
logging.debug('Downloader is started')
logging.debug('Data: %s' % data)


if 'url' in settings:
  start(settings['url'])

logging.debug('Downloader is stopped')
