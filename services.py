"""
services.py

This file connects models.py and database.py together. It holds
our "real world actions" - things like "register a new member" or
"check out a piece of equipment" - and coordinates both files to
make that happen correctly.
"""

import database
import models


def register_member(name, email):
    """
    Save a brand new member into the database, then return a real
    Member object built from what was actually saved.
    """
    new_id = database.insert_member(name, email)
    return models.Member(name, email, new_id)
