#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from pipe.src import harvest_gmail, util, message, citation
from pipe.src.identify_crossref import IdentifyCrossRef
from pipe.src.util import Util

a = datetime.now()
u = Util()

# Get Message objects from Gmail
messages = harvest_gmail.HarvestGmail().main()

# Only process if there are unread emails
if messages:
    # Write messages to database
    message_sql = """INSERT INTO message_store (email_id, title, snippet, m_author, m_pub_title, m_pub_year, sent_date,
    harvested_date, source, id_status, label_id, doi, match_context, snippet_match, highlight_length) VALUES (%s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    u.write_new_objects(message_sql, messages)


# Get all unidentified messages from message_store
unidentified_sql = "SELECT * FROM message_store WHERE id_status = False AND (last_crossref_run IS NULL " \
                   "OR last_crossref_run < ADDDATE(DATE(NOW()), INTERVAL -1 MONTH))"
cursor = u.query_db(unidentified_sql)
mystery_messages = cursor.fetchall()

# Turn each result back into Message obj
checklist = [message.Message(message_id=i[0],
                             email_id=i[1],
                             title=i[2],
                             snippet=i[3],
                             m_author=i[4],
                             m_pub_title=i[5],
                             m_pub_year=i[6],
                             sent_date=i[7],
                             harvested_date=i[8],
                             source=i[9],
                             identification_status=i[10],
                             label=i[11],
                             match_context=i[13],
                             snippet_match=i[14],
                             highlight_length=i[15]
                             ) for i in mystery_messages]

cr_i = IdentifyCrossRef(checklist)
identified_citations, unidentified_citations = cr_i.get_crossref_match()
found_messages = []
for x, y in identified_citations.items():
    for i in y.message_ids:
        found_messages.append((x, i))

update_msg_found = """UPDATE message_store SET doi = %s, id_status = True WHERE message_id = %s"""
u.write_new_normals(update_msg_found, found_messages)

update_msg_unidentified = """UPDATE message_store SET last_crossref_run = %s WHERE message_id = %s"""
u.write_new_normals(update_msg_unidentified, unidentified_citations)

# Write messages to citation database
citation_sql = """INSERT INTO citation_store (author, doi, title, type, issued_date, subject, pub_title, pub_publisher,
issn, isbn, issue, volume, page, classification_id, nhm_sub) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
 %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE nhm_sub = 1"""

verified_citations = []
u.write_new_objects(citation_sql, identified_citations.values())

# Update nhm_pub by checking against table of subscribed journals
nhm_pub_sql = 'UPDATE citation_store SET nhm_sub = 1 WHERE issn IN (SELECT issn from nhm_pubs)'
u.query_db(unidentified_sql)

b = datetime.now()
c = b - a
print(f"Runtime: {c}")


