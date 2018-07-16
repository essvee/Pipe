#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
from pipe.harvest import gapi

# Get email titles and metadata from gmail inbox
result_list = gapi.main()

with open('gapi_results.csv', 'w', newline='\n') as csvfile:

    fieldnames = ['title', 'label', 'format', 'bib_details', 'snippet']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect='excel')
    writer.writeheader()
    writer.writerows(result_list)

# Send just titles for each to crossref
# Time how long it takes and the fuzzy match score
# export to csv

# Send titles + associated metadata for each to crossref
# Time how long it takes and the fuzzy match score
# write to csv

