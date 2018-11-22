#!/usr/bin/env python
from datetime import date, timedelta

from sqlalchemy import or_

from pipe.src.base import Session
from pipe.src.db_objects import Message
from pipe.src.harvest_gmail import HarvestGmail

# Connect to Gmail account
messages = HarvestGmail().main()

# Open new db session
session = Session()

# Write new messages to message_store
session.add_all(messages)

# Set cutoff to one month before current date
cutoff = date.today() - timedelta(days=31)

# Query message_store for records which haven't been checked against crossref in the last month (or ever)
mystery_messages = session.query(Message)\
    .filter(Message.id_status == False)\
    .filter(or_(Message.last_crossref_run is None, Message.last_crossref_run < cutoff))

