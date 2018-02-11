#!/usr/bin/env python
"""
    Just connects to our Zotero database and dumps our collection to stdout.

    This is more a proof of concept script to exercise pyzotero.

    Source cribbed from https://github.com/urschrei/pyzotero
"""


from pyzotero import zotero

library_id='1969054' # Zotero group id for WolfBytes
library_type='group' # This is Zotero group, not an individual Zotero database

# TODO We need to come up with a sensible API key management system.  I generated a read-only key for myself, but
# hesitated to check it in the git repo for security reasons. (Even though the repo is private.)
api_key='' # You will need to generate your own API key and put it here.


zot = zotero.Zotero(library_id, library_type, api_key)


items = zot.top(limit=5)

# we've retrieved the latest five top-level items in our library
# we can print each item's item type and ID
for i, item in enumerate(items):
    print(i, ':', item['data']['itemType'], item['data']['title'], item['data']['dateAdded'])
