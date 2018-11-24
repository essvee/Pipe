#!/usr/bin/env python
from datetime import date, timedelta
from sqlalchemy import or_
from pipe.src.base import Session
from pipe.src.db_objects import Message, Citation
from pipe.src.harvest_gmail import HarvestGmail
from pipe.src.identify_crossref import IdentifyCrossRef

# Connect to Gmail account
messages = HarvestGmail().main()

# Open new db session
session = Session()

# Write new messages to message_store
session.add_all(messages)

# Set cutoff to one month before current date
cutoff = date.today() - timedelta(days=31)

# Query message_store for records which haven't been checked against crossref in the last month (or ever)
mystery_messages = list(session.query(Message)
                        .filter(or_(Message.last_crossref_run == None, Message.last_crossref_run < cutoff))
                        .filter(Message.id_status == False))

identified_citations, id_messages = IdentifyCrossRef(mystery_messages).get_crossref_match()

# Update message table for both matched and unmatched messages
session.add_all(id_messages)

# Get all known citations
known_citations = {x.doi for x in session.query(Citation)}

# Strip out citations already in the database
identified_citations = [d for d in identified_citations if d.doi not in known_citations]

# Add new citations
session.add_all(identified_citations)
session.flush()

# TODO - change view to populate issn as TRUE if in nhm_pubs table in view instead of here
# TODO - update nhm_sub table
# TODO - convert metric to ORM
# TODO - convert access to ORM

