#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, socket
import simplejson as json

urls = (
  'http://www.stephenzunes.org/vitae08.doc', 
  "http://docs.python.org/ftp/python/doc/current/python-2.6.1-docs-pdf-a4.tar.bz2",
  'http://dfn.dl.sourceforge.net/sourceforge/psi/psi-0.12-win-setup-1.exe'
)
ips = (('192.168.1.11', 33333),)

# загрузим общие настройки, добавим персональные для данной закачки 
# отправим их downloader.py и получим ответ от сервера

with open(sys.path[0] + '/downloader.conf') as f:
  settings = json.load(f)
#f.closed

settings['url'] = urls[1]
settings['id'] = 1233

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ips[0][0], ips[0][1]))
s.send(json.dumps(settings))
response = s.recv(1024)
s.close()

print response 
