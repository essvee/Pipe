#!/usr/bin/env python
from datetime import date, timedelta
from sqlalchemy import or_
from pipe.src.base import Session
from pipe.src.classifier import Classifier
from pipe.src.db_objects import Message, Citation, Name
from pipe.src.dimensions import Dimensions
from pipe.src.harvest_gmail import HarvestGmail
from pipe.src.identify_crossref import IdentifyCrossRef
import logging
from pipe.src.unpaywall import Unpaywall
from pipe.src.find_names import FindNames


# Set up logger
logging.basicConfig(filename='citations.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("------")
# Connect to Gmail account
messages = HarvestGmail().main()

# Open new db session
session = Session()

# Write new messages to message_store
session.add_all(messages)

# Log no. new messages written out
logging.info(f"{len(messages)} new messages writen to message_store.")

# Set cutoff to one month before current date
cutoff = date.today() - timedelta(days=31)

# Query message_store for records which haven't been checked against crossref in the last month (or ever)
mystery_messages = list(session.query(Message)
                        .filter(or_(Message.last_crossref_run == None, Message.last_crossref_run < cutoff))
                        .filter(Message.id_status == False))

identified_citations, id_messages = IdentifyCrossRef(mystery_messages).get_crossref_match()
print("crossref identification complete")


# Update message table for both matched and unmatched messages
session.add_all(id_messages)

# Get all known citations
known_citations = {x.doi for x in session.query(Citation)}

# Strip out citations already in the database
identified_citations = [d for d in identified_citations if d.doi not in known_citations]

# Add new citations
session.add_all(identified_citations)
logging.info(f"{len(identified_citations)} citations written to citation_store.")
session.flush()
print("crossref identifications written to db")

# Harvest metrics monthly
if date.today().day == 1:
    logging.info("Running metrics...")
    citation_dois = list(session.query(Citation).filter(Citation.classification_id == True))
    session.flush()

    new_metrics = Dimensions(citation_dois).get_citations()

    # Write to bibliometrics table and log results
    session.add_all(new_metrics)
    logging.info(f"{len(new_metrics)} access metrics written to bibliometrics.")
    session.flush()

print("starting access queries")
# Get access data for citations newly-identified in this pass
new_access = Unpaywall(identified_citations).get_access_data()
session.add_all(new_access)
session.flush()

# Every six months, re-check all Citation records for updated access info
if date.today().day == 1 and (date.today().month == 12 or date.today().month == 6):

    all_records = list(session.query(Citation)
                       .filter(Citation.classification_id == True, Citation.identified_date != date.today()))

    updated_access_records = Unpaywall(all_records).get_access_data()
    session.add_all(updated_access_records)
    session.flush()

unclassified_citations = list(session.query(Citation).filter(Citation.classification_id == None))
print("finished access queries - starting classification")

# Classify
if len(unclassified_citations) > 0:
    classified_citations = Classifier(unclassified_citations).classify()
    session.add_all(classified_citations)
    session.flush()

print("classification finished starting name parsing...")
result = []

# Extract taxonomic names (Limited to new, NHM-ref papers for now)
nhm_citations = list(session.query(Citation)
                     .filter(Citation.identified_date == date.today())
                     .filter(Citation.classification_id == True)
                     .filter(or_(Citation.type == 'peer-review', Citation.type == 'journal-article')))

# test_list = nhm_citations[0:5]
names = []

# Get names for each title
for x in nhm_citations:
    print(x.title)
    result.extend(FindNames(x.doi, x.title).get_names())

# Convert each sp. name into a Name object
for r in result:
    print(f"{r[0]}: {r[1]}")
    names.append(Name(doi=r[0], label=r[1]))

session.add_all(names)
session.flush()
