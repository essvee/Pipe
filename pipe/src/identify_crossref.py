import json

from habanero import Crossref
from fuzzywuzzy import fuzz

from pipe.src.citation import Citation


class IdentifyCrossRef:
    def __init__(self, messages):
        self.messages = messages
        self.mail_to = "s.vincent@nhm.ac.uk"

    def get_crossref_match(self):
        cr = Crossref()
        cr.mailto = self.mail_to
        crossref_results = []
        suspicious_match = []

        for message in self.messages:
            crossref_result = cr.works(query_title=message.title, query_author=message.m_author,
                                       query_container_title=message.m_pub_title, rows=1,
                                       select='DOI,title,author,type,license,subject,container-title,'
                                              'subject,publisher,issue,volume,page,ISSN,ISBN,published-online,'
                                              'issued,abstract,link')

            # Skip if no results returned
            if crossref_result['message']['total-results'] == 0:
                break

            # Title according to crossref (i.e., best match returned)
            cr_title = crossref_result['message']['items'][0]['title'][0]

            score = fuzz.partial_ratio(message.title, cr_title)
            if score > 90:
                print('wooo')

            print(json.dumps(crossref_result, indent=2))

        return crossref_results

    def make_citation(self, message_id, crossref_result):
        candidate = Citation()

    def validate_match(self):
        # TODO implement this method
        pass