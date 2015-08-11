#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Eduard Trott" <etrott@redhat.com>

from __future__ import unicode_literals

import cookielib
import logging
import re
import sys
import urllib
import urllib2


# load the root logger if it exists; or use the default if not already created
logging.basicConfig()
logr = logging.getLogger(__name__)


def check_h2(content, search_str):
    if re.search(r'<h2>{}<\/h2>'.format(search_str), content):
        err = re.findall(r'(?<=<strong>).*(?=<\/strong>)', content)[0]
        logr.error(err)
        raise RuntimeError


def download(uri, user, password):
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
        form =  []

    try:
        return urllib2.urlopen(uri, urllib.urlencode(form)).read()
    except:
        raise


def extract(args, config=None):
    base_url = args.get('base_url') or config.get('base_url')
    list_name = args.get('list_name')

    lists = config.get('lists') or {}
    list_config = lists.get(list_name) or {}
    user = args.get('user') or list_config.get('user')
    password = args.get('password') or list_config.get('password')

    logr.debug(
        '[{}] {}: {}'.format(base_url, list_name, user))

    if not base_url and list_name:
        raise RuntimeError(
            "base_url [{}] and list_name [{}] can not be NULL".format(
                base_url, list_name))

    
    list_url = "{}/roster/{}".format(base_url, list_name)
    content = get_content(list_url, user, password)

    check_h2(content, 'Error')

    # source contain list members page content
    users = re.findall(r'(?<=--at--redhat\.com">)(?<=>).*(?=<\/a>)', content)
    users = ['@'.join(user.split(' at ')) for user in users]

    return users