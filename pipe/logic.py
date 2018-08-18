#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pipe.src import gapi, util

# Get email titles and metadata from gmail inbox + write to file
obj = gapi.Gapi()
result_list = obj.main()
header_fields = result_list[0].keys()
w = util.Util()
w.dict_to_csv(result_list, header_fields, 'gapi_results.csv')


# TODO - Send just titles for each to crossref
# Time how long it takes and the fuzzy match score
# export to csv

#  TODO - Send titles + associated metadata for each to crossref
# Time how long it takes and the fuzzy match score
# write to csv

