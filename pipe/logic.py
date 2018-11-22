#!/usr/bin/env python

from datetime import datetime, date
from pipe.src import harvest_gmail
from pipe.src.classifier import Classifier
from pipe.src.db_objects import Citation, Message
from pipe.src.dimensions import Dimensions
from pipe.src.identify_crossref import IdentifyCrossRef
from pipe.src.unpaywall import Unpaywall
from pipe.src.util import Util

u = Util()

# Get Message objects from Gmail
messages = harvest_gmail.HarvestGmail().main()

# Only process if there are unread emails
if messages:
    # Write messages to database
    message_sql = """INSERT INTO message_store (email_id, title, snippet, m_author, m_pub_title, m_pub_year, sent_date,
    harvested_date, source, id_status, label_id, doi, snippet_match, highlight_length) VALUES (%s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s)"""

    u.write_new_objects(message_sql, messages)


# Get all unidentified messages from message_store
unidentified_sql = "SELECT * FROM message_store WHERE id_status = False AND (last_crossref_run IS NULL " \
                   "OR last_crossref_run < ADDDATE(DATE(NOW()), INTERVAL -1 MONTH))"
cursor = u.query_db(unidentified_sql)
mystery_messages = cursor.fetchall()

# Turn each result back into Message obj
checklist = [Message(message_id=i[0],
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
                     snippet_match=i[14],
                     highlight_length=i[15]
                     ) for i in mystery_messages]

# Query Crossref with new message ids
cr_i = IdentifyCrossRef(checklist)
identified_citations, unidentified_citations = cr_i.get_crossref_match()
found_messages = []
crossref_date = date.today().strftime('%Y-%m-%d')

# For every identified citation, extract source message_id(s)
for x, y in identified_citations.items():
    for i in y.message_ids:
        found_messages.append((x, crossref_date, i))

# Update database with found citations
update_msg_found = """UPDATE message_store SET doi = %s, id_status = True, last_crossref_run = %s WHERE message_id = %s"""
u.write_new_normals(update_msg_found, found_messages)

# Update database record for unidentified messages
update_msg_unidentified = """UPDATE message_store SET last_crossref_run = %s WHERE message_id = %s"""
u.write_new_normals(update_msg_unidentified, unidentified_citations)

# Write messages to citation database
citation_sql = """INSERT INTO citation_store (author, doi, title, type, issued_date, subject, pub_title, pub_publisher,
issn, isbn, issue, volume, page, classification_id, nhm_sub) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,
 %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE classification_id = NULL"""
verified_citations = []
u.write_new_objects(citation_sql, identified_citations.values())

# Update nhm_pub by checking against table of subscribed journals
nhm_pub_sql = 'UPDATE citation_store SET nhm_sub = 1 WHERE issn IN (SELECT issn from nhm_pubs)'
u.query_db(unidentified_sql)

# Only harvest metrics monthly
if date.today().day == 1:
    all_doi_sql = "SELECT doi FROM citation_store WHERE classification_id = True"
    cursor = u.query_db(all_doi_sql)
    citation_dois = cursor.fetchall()

    dim = Dimensions(citation_dois)
    dim_sql, b_data = dim.get_citations()
    u.write_new_normals(dim_sql, b_data)

# Get access data for unchecked dois
unchecked_sql = "SELECT c.doi FROM citation_store c WHERE c.doi NOT IN (SELECT oa.doi FROM open_access oa) AND " \
                "c.classification_id = True"
cursor = u.query_db(unchecked_sql)
unpay = Unpaywall(cursor.fetchall())
unpay_sql, unpay_data = unpay.get_access_data()

# Write access data to database
u.write_new_normals(unpay_sql, unpay_data)

# Get a list of all unclassified citations
unclassified_sql = "SELECT * FROM vw_data WHERE classification_id IS NULL"
cursor = u.query_db(unclassified_sql)
unclassified_dois = cursor.fetchall()

# Pass unclassified DOIs to classifier
classifier = Classifier(unclassified_dois)

if len(classifier.grouped_data) > 0:
    # Get results of classification and update database
    classification_sql, results = classifier.classify()
    u.write_new_normals(classification_sql, results)

# Update csvs (temp workaround)
u.update_repo()


