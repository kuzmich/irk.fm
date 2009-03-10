#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from subprocess import *

try:
    data = sys.stdin.read()
    p = Popen('downloader.py', stdin=PIPE) 
    p.stdin.write(data)
    p.stdin.close()
except OSError, e:
    print >>sys.stderr, "Execution failed:", e
