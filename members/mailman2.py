#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Eduard Trott" <etrott@redhat.com>

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

import cookielib
import logging
import re
import urllib
import urllib2

logr = logging.getLogger(__name__)


def check_h2(content, search_str):
    if re.search(r'<h2>{}<\/h2>'.format(search_str), content):
        err = re.findall(r'(?<=<strong>).*(?=<\/strong>)', content)
        if not err:
            logr.error(err[0])
        raise RuntimeError


def mm2_download(uri, user, password):
    '''
    # FIXME DOCS
    '''
    if user and password:
        logr.debug('AUTH {}:{}'.format(user, uri))
        cookieJar = cookielib.CookieJar()

        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
        opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible)")]
        urllib2.install_opener(opener)

        form = dict()
        form['roster-email'] = user
        form['roster-pw'] = password
    else:
        form = []

    return urllib2.urlopen(uri, urllib.urlencode(form)).read()


def extract(args, config=None):
    '''
    # FIXME DOCS
    '''
    base_url = args.get('base_url') or config.get('base_url')
    list_name = args.get('list_name')

    lists = config.get('lists') or {}
    list_config = lists.get(list_name) or {}
    user = args.get('user') or list_config.get('user')
    password = args.get('password') or list_config.get('password')

    logr.debug(
        '[{}] {}: {}'.format(base_url, list_name, user))

    if not (base_url or list_name):
        raise RuntimeError(
            "base_url [{}] and list_name [{}] can not be NULL".format(
                base_url, list_name))

    list_url = "{}/roster/{}".format(base_url, list_name)
    content = mm2_download(list_url, user, password)

    # Check for and report any errors return in the HTML
    check_h2(content, 'Error')

    # source contain list members page content
    users = re.findall(r'(?<=--at--redhat\.com">)(?<=>).*(?=<\/a>)', content)
    users = ['@'.join(u.split(' at ')) for u in users]

    return users
