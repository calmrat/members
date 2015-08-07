#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
# Author: "Eduard Trott" <etrott@redhat.com>

from __future__ import unicode_literals

import logging
import re
import sys

from bs4 import BeautifulSoup
import ClientForm
import mechanize
import requests as rq


# load the root logger if it exists; or use the default if not already created
logging.basicConfig()
logr = logging.getLogger(__name__)


def check_h2(content, search_str):
    # IN: string or bs4 object
    if isinstance(content, str):
        # convert to beautifulsoup
        content = BeautifulSoup(content, 'html.parser')
    h2s = [l.string for l in content.find_all('h2')]
    if 'Error' in h2s:
        # FIXME: get content from the following "<strong>" tag, which contains
        # the details of the error
        err = '#FIXME: replace with the actual error ^^^'
        logr.error(err)
        raise RuntimeError


def auth(list_link, user, password):
    logr.debug('AUTH {}:{}'.format(user, list_link))
    cookieJar = mechanize.CookieJar()

    opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookieJar))
    opener.addheaders = [("User-agent", "Mozilla/5.0 (compatible)")]
    mechanize.install_opener(opener)
    forms = ClientForm.ParseResponse(
        mechanize.urlopen(list_link), backwards_compat=False)

    form = forms[2]
    form['roster-email'] = user
    form['roster-pw'] = password
    try:
        fp = mechanize.urlopen(form.click())
        content = fp.read()
        check_h2(content, 'Error')
    finally:
        fp.close()


def extract(args, config=None):
    # BeautifulSoup find_all fails b/c of max recursion depth exceeded; bump it
    sys.setrecursionlimit(10000)

    base_url = args.get('base_url') or config.get('base_url')
    list_name = args.get('list_name')

    lists = config.get('lists') or {}
    list_config = lists.get(list_name) or {}
    list_user = args.get('user') or list_config.get('user')
    list_password = args.get('password') or list_config.get('password')

    logr.debug(
        '[{}] {}: {}'.format(base_url, list_name, list_user))

    if not base_url and list_name:
        raise RuntimeError(
            "base_url [{}] and list_name [{}] can not be NULL".format(
                base_url, list_name))

    list_link = "{}/listinfo/{}".format(base_url, list_name)
    list_members_link = "{}/roster/{}".format(base_url, list_name)

    if list_user and list_password:
        # auth is specified, use it
        auth(list_link, list_user, list_password)
        content = mechanize.urlopen(list_members_link).read()
    else:
        # if anyone can access to the list of members
        content = rq.get(list_members_link).content

    content = BeautifulSoup(content, 'html.parser')
    check_h2(content, 'Error')

    # source contain list members page content
    members_link = re.compile(r"\.\./options/%s/\S*redhat\.com" % (list_name))

    users = ['@'.join(link.string.split(' at '))
             for link in content.find_all(href=members_link)]

    return users
