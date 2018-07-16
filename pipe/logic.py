#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pipe.harvest import gapi
from pipe.utils import write_out

# Get email titles and metadata from gmail inbox + write to file
result_list = gapi.main()
fields = result_list[0].keys()
write_out.dict_to_csv(result_list, fields, 'gapi_results.csv')


# TODO - Send just titles for each to crossref
# Time how long it takes and the fuzzy match score
# export to csv

#  TODO - Send titles + associated metadata for each to crossref
# Time how long it takes and the fuzzy match score
# write to csv

