#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from pipe.src import harvest_gmail, util, message, citation
from pipe.src.identify_crossref import IdentifyCrossRef
from pipe.src.util import Util

a = datetime.now()
u = Util()

# todo - uncomment this when crossref module working
# Get Message objects from Gmail
messages = harvest_gmail.HarvestGmail().main()

if messages:
    # Write messages to database
    message_sql = """INSERT INTO message_store (email_id, title, snippet, m_author, m_pub_title, m_pub_year, sent_date,
    harvested_date, source, id_status, label_id, doi) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

    u.write_new_objects(message_sql, messages)

    # Get all unidentified messages from message_store
    unidentified_sql = "SELECT * FROM message_store WHERE id_status = False"
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
                                 label=i[11]
                                 ) for i in mystery_messages]


    cr_i = IdentifyCrossRef(checklist)
    identified_citations = cr_i.get_crossref_match()
    found_messages = []
    for x, y in identified_citations.items():
        for i in y.message_ids:
            found_messages.append((x, i))

    update_msg = """UPDATE message_store SET doi = %s, id_status = True WHERE message_id = %s"""
    u.write_new_normals(update_msg, found_messages)

    # Write messages to citation database
    citation_sql = """INSERT INTO citation_store (author, doi, title, type, issued_date, subject, pub_title, pub_publisher,
    issn, isbn, issue, volume, page, classification_id, nhm_sub) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
     %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE nhm_sub = 1"""

    verified_citations = []
    u.write_new_objects(citation_sql, identified_citations.values())

b = datetime.now()
c = b - a
print(f"Runtime: {c}")


