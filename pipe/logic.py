#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pipe.src import gapi, util

# Get email titles and metadata from gmail inbox + write to file
obj = gapi.Gapi()
result_list = obj.main()



# header_fields = result_list[0].keys()
# w = util.Util()
# w.dict_to_csv(result_list, header_fields, 'gapi_results.csv')

for n in result_list:
    for i in n.messages:
        print(i.citation_format)
        print(i.title)
        print(i.bib_data)
        print(i.m_author)
        print(i.m_pub_title)
        print(i.m_pub_year)
        print("-------")
        print()



# TODO - Send just titles for each to crossref
# Time how long it takes and the fuzzy match score
# export to csv

#  TODO - Send titles + associated metadata for each to crossref
# Time how long it takes and the fuzzy match score
# write to csv

