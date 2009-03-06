#!/usr/bin/python
# -*- coding: utf-8 -*-
import controller as c

urls = (
    'http://www.stephenzunes.org/vitae08.doc', 
    "http://docs.python.org/ftp/python/doc/current/python-2.6.1-docs-pdf-a4.tar.bz2",
    'http://dfn.dl.sourceforge.net/sourceforge/psi/psi-0.12-win-setup-1.exe'
)

c.create_download({
    'url': urls[1], 
    'description': 'Документация по пайтону'
})
