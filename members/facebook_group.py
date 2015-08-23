#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: "Chris Ward" <cward@redhat.com>

'''
Facebook Group API membership
'''

# PY3 COMPAT
from __future__ import unicode_literals, absolute_import

import logging
logr = logging.getLogger(__name__)

import requests as rq

APP_SLUG = 'facebook_group'

# facebook v2.4
VALID_FIELDS = set([
    'description', 'cover', 'email', 'icon', 'id', 'name', 'link',
    'updated_time', 'privacy', 'parent', 'venue', ' picture',
    'members', 'files', 'owner', 'albums', 'docs', 'feed'])


def extract(group_id, access_token, fields=None):
    '''
    FIXME: DOCS...
    Links:
       * https://developers.facebook.com/tools/explorer/

    '''
    fields = fields or ['id', 'owner', 'email', 'name', 'members']
    # TEST that fields are a subset of valid fields
    assert set(fields).issubset(VALID_FIELDS)

    get_args = {'fields': ','.join(fields),
                'access_token': access_token}
    get_args_str = '&'.join(
        ['{}={}'.format(x, y) for x, y in get_args.items()])

    base_url = 'https://graph.facebook.com/{}/?{}'.format(
        group_id, get_args_str)
    logr.debug(' LOADING URL: {}'.format(base_url))

    response = rq.get(base_url)

    # FIXME: check for errors
    # probably want to validate here somehow...?
    r_json = response.json()
    subscribers = r_json.get('members')

    return subscribers


if __name__ == '__main__':
    from members.utils import config

    _config = config.get(APP_SLUG) or {}
    access_token = _config.get('access_token')

    group_id = 769782779718163
    extract(group_id=group_id, access_token=access_token)
