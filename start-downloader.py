#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from subprocess import *

try:
    data = sys.stdin.read()
    p = Popen('downloader.py', stdin=PIPE) 
    p.stdin.write(data)
except OSError, e:
    print >>sys.stderr, "Execution failed:", e
