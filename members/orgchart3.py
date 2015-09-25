#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: "Chris Ward" <cward@redhat.com>

'''
OrgChart3 CSV exporter Script.

Supported AUthentication:
    Kereberos AUTH (kinit)
'''

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

import logging
import os
from urllib import urlencode
import tempfile
import warnings
warnings.simplefilter('ignore')

from functioncache import functioncache
import pandas as pd
import requests as rq
from requests_kerberos import HTTPKerberosAuth, OPTIONAL

logr = logging.getLogger(__name__)

# UPDATES HERE REQUIRE UPDATES IN TESTS/test_orgchart3.py
GET_ARGS = {
    'direct': 'true',
    'indirect': 'true',
    'kerberos': 'true',
    'location': 'true',
    'realname': 'false',
    'product_role': 'true',  # Product / Role
    'manager': 'false',
    'functional': 'false',
    'group': 'true',  # Group
    'email': 'true',  # Email
    'start': 'true',  # Hire Date
    'type': 'true',   # Empoyee Type
    'costcenter': 'true',  # Cost Center
    'organization': 'true',  # Organization
    'title': 'false',
    'tag': 'false',
}


# note this leaves garbage in ~/.functioncache that might need to be cleaned
@functioncache(1 * 60 * 60)  # cache for 1 hour
def download(uri, user=None, password=None, saveas=None, ssl_verify=False):
    '''
    FIXME: DOCS...
    '''
    if saveas is None:
        temp = tempfile.NamedTemporaryFile(prefix='requests_',
                                           dir='/tmp')
        saveas = temp.name
        temp.close()

    if not (user or password):
        # Fall back to kerberos auth
        auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)
    else:
        auth = None

    with open(saveas, 'wb') as handle:
        r = rq.get(uri, verify=ssl_verify, auth=auth)
        if not r.ok:
            raise RuntimeError
        for block in r.iter_content(1024):
            if not block:
                break
            handle.write(block)
    return saveas


def extract(uid=None, base_url=None, use_default_email_domain=False,
            default_email_domain=None):
    '''
    FIXME: DOCS...
    '''
    assert base_url and isinstance(base_url, (unicode, str))
    export_url = os.path.join(base_url, 'export_csv')

    # ded is shortform for "default email domain"
    # this will convert uid's to  uid@default_email_domain.com
    use_ded = use_default_email_domain
    ded = default_email_domain

    get_args = GET_ARGS.copy()
    get_args['uid'] = uid
    uri = '{}?{}'.format(export_url, urlencode(get_args))
    csv_path = download(uri)

    members_df = pd.read_csv(csv_path)

    users = list(members_df['Kerberos'].unique())

    # the team lead should be included as a member of their own team
    users.append(uid)

    if use_ded:
        if not ded:
            raise RuntimeError("No default email domain set!")
        users = ['@'.join((u, ded)) for u in users]

    logr.info('{} members FOUND'.format(len(users)))

    return sorted(users)
