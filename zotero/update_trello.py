#!/usr/bin/env python
"""
    Adds trello cards for Zotero entries that have zero tags to Zotero Database Management board.
    You will need to set the environment variable WB_API_KEY to our Zotero API key.

    Currently hardcoded to only send cards for one collection, CFG.

    TODO Expand to other collections, color tagged to identify encompassing collection
"""

import os
import sys
import subprocess

import argparse

from pprint import pprint

from pyzotero import zotero

# This is the environment variable in which we look for the Zotero API key
API_KEY_ENV = 'WB_API_KEY'

# Zotero group id for WolfBytes
LIBRARY_ID = '1969054'

# This is Zotero group, not an individual Zotero database
LIBRARY_TYPE = 'group'

# This is the email address for adding a card to the Trello baord
TRELLO_EMAIL = 'markcoletti1+ylusi3zf18unsafnls2o@boards.trello.com'


def _get_collection_keys(api_key):
    """
    :param api_key: for accessing our Zotero database
    :return: a dictionary of Zotero collection data using the Zotero key
    """
    zot = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, api_key)

    # gab *all the stuff
    items = zot.collections_top()

    collection = {}

    for i, item in enumerate(items):
        collection[item['data']['name']] = {'zoteroKey' : item['key'], 'numItems' : item['meta']['numItems']}

    return collection


def _get_untagged_items(collections, api_key):
    """
    :param collections: dictionary of collections
    :param api_key: for accessing our Zotero database
    :return: list of items that need tagging
    """
    untagged_items = []

    zot = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, api_key)

    # gab *all* the stuff
    items = zot.everything(zot.top())

    # grind through everything, only keeping the items that belong to the CFR collection that have *NO* tags
    for i, item in enumerate(items):

        # TODO pass in collections name instead of hard-coding 'CFR'
        if collections['CFR']['zoteroKey'] in item['data']['collections'] and item['data']['tags'] == []:
            untagged_items.append({'title' : item['data'].setdefault('title','no title')}) #, 'abstract' : item['data']['abstractNote']})

    return untagged_items


def emit_email_lines(untagged_items):
    """ Emit email lines to stdout that can be executed by the shell

    :param untagged_items: each element corresponds to an untagged Zotero record
    :return: None
    """
    for item in untagged_items:
        print('Processing', ''.join(item['title']))

        subject = "#yellow #red " + ''.join(item['title'])
        output = subprocess.check_output(['/bin/echo', '-s', subject, TRELLO_EMAIL])
        
        print(output)



if __name__ == '__main__':

    if not 'WB_API_KEY' in os.environ:
        print(sys.argv[0], ': Need WB_API_KEY environment variable set')
        sys.exit(-1)

    api_key = os.environ['WB_API_KEY']

    collections = _get_collection_keys(api_key)

    # pprint(collections)

    untagged_items = _get_untagged_items(collections, api_key)

    # pprint(untagged_items)

    emit_email_lines(untagged_items)

