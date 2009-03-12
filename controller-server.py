#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys 
import socket 
import simplejson as json
import logging
import controller as c 

addr = ('', 33334)

logging.basicConfig(filename=sys.path[0]+'/downloader.log', level=logging.DEBUG, format="%(asctime)s - %(name)s - %(message)s")
l = logging.getLogger('controller-server')

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
            c.update_status(data)

    conn.close()
