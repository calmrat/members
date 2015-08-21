#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: "Chris Ward" <cward@redhat.com>

'''
members.py Tornado PyRestful REST API
'''

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

import logging

import tornado.ioloop
import pyrestful.rest

from pyrestful import mediatypes
from pyrestful.rest import get

from members import mailman2 as mm2
from members.utils import config

logr = logging.getLogger(__name__)


class Mailman2Service(pyrestful.rest.RestHandler):
    @get(_path="/mailman2/{list_name}", _produces=mediatypes.APPLICATION_JSON)
    def extract(self, list_name):
        args = {'list_name': list_name}
        members = mm2.extract(args, config['mailman2'])
        return members

if __name__ == '__main__':
    try:
        logr.info("Starting members.py REST API")
        app = pyrestful.rest.RestService([Mailman2Service])
        app.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        logr.warn("\nmembers.py REST API killed!")
