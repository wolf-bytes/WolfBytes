#!/usr/bin/env python
"""
    Just connects to our Zotero database and dumps our collection to stdout.

    This is more a proof of concept script to exercise pyzotero.

    Source cribbed from https://github.com/urschrei/pyzotero

    You will need to set the environment variable WB_API_KEY to our Zotero API key.

    TODO Or, optionally, have a command line argument.
"""

import os
import sys
import json

from pyzotero import zotero

# This is the environment variable in which we look for the Zotero API key
API_KEY_ENV = 'WB_API_KEY'

# Zotero group id for WolfBytes
LIBRARY_ID= '1969054'

# This is Zotero group, not an individual Zotero database
LIBRARY_TYPE= 'group'



def dump_db(api_key):
    """ Just dump out the entire database

    :param api_key: for our Zotero database
    :return: None
    """
    zot = zotero.Zotero(LIBRARY_ID, LIBRARY_TYPE, api_key)

    # gab *all the stuff
    items = zot.everything(zot.top())

    # print each item's item type and ID
    for i, item in enumerate(items):
        print(json.dumps(item))



if __name__ == '__main__':
    if 'WB_API_KEY' in os.environ:
        api_key = os.environ['WB_API_KEY']
        dump_db(api_key)
    else:
        print(sys.argv[0], ': Need WB_API_KEY environment variable set')