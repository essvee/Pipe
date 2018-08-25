import json
from datetime import date, datetime

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
            best_match = crossref_result['message']['items'][0]
            cr_title = best_match['title'][0]

            score = fuzz.partial_ratio(message.title, cr_title)
            if score > 90:
                citation_obj = Citation(cr_title=best_match['title'],
                                        cr_type=best_match['type'],
                                        cr_doi=best_match['doi'],
                                        cr_content_version=best_match['license']['content-version'],
                                        cr_issue=best_match['issue'],
                                        cr_volume=best_match['volume'],
                                        cr_page=best_match['page'],
                                        cr_pub_publisher=best_match['publisher'],
                                        cr_pub_title=best_match['container-title'],
                                        pub_issn=best_match['issn'][0],
                                        pub_isbn=best_match['isbn'][0],
                                        cr_url=best_match['link'],
                                        cr_issued=date(*map(int, best_match['issued']['date-parts'][0])),
                                        # todo - authors
                                        # todo - subjects
                                        )

            # print(json.dumps(crossref_result, indent=2))

        return crossref_results

    def date_parts(self, date_parts):
        return date(*map(int, date_parts))

    def make_citation(self, message_id, crossref_result):
        candidate = Citation()

    def validate_match(self):
        # TODO implement this method
        pass