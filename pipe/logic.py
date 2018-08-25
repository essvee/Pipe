#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from pipe.src import harvest_gmail, util
from pipe.src.identify_crossref import IdentifyCrossRef
from pipe.src.util import Util

a = datetime.now()
u = Util()

# Get Message objects from Gmail
messages = harvest_gmail.HarvestGmail().main()

# Write messages to database
message_sql = """INSERT INTO message_store (email_id, title, snippet, m_author, m_pub_title, m_pub_year, sent_date,
harvested_date, source, id_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

u.write_new(message_sql, messages)


for n in messages:
    print(n)

# for n in email_list:
#     messages = n.messages
#     cr_i = CrossRefIdentifier(messages)
#     cr_i_result_list = cr_i.get_crossref_match()
#     for i in cr_i_result_list:
#         print(i.keys())

b = datetime.now()
c = b - a
print(f"Runtime: {c}")



# w = util.Util()
#
# for n in result_list:
#     for i in n.messages:
#         message_list.append(i)
#
# w.write_object_to_csv(list_dict_data=message_list, filename='gapi_results_messages.csv')

# cr_i = CrossRefIdentifier(result_list)
#
# cr_i_result_list = cr_i.get_crossref_match()
#
# for i in cr_i_result_list:
#     print(i)

# TODO - Send just titles for each to crossref
# Time how long it takes and the fuzzy match score
# export to csv

#  TODO - Send titles + associated metadata for each to crossref
# Time how long it takes and the fuzzy match score
# write to csv

