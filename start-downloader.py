#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from subprocess import *

try:
    data = sys.stdin.read()
    #p = Popen('downloader.py', stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True, shell=True) 
    p = Popen('downloader.py', stdin=PIPE, close_fds=True, shell=True) 
    p.stdin.write(data)
    #o = p.communicate(data)
    retcode = p.returncode
    if retcode < 0:
        print "Child was terminated by signal (%s)" % retcode
    else:
        print >>sys.stderr, "Child returned", retcode
except OSError, e:
    print >>sys.stderr, "Execution failed:", e
