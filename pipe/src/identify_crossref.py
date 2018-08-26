from datetime import date

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
                                       select='DOI,title,author,type,subject,container-title,'
                                              'subject,publisher,issue,volume,page,ISSN,ISBN,published-online,'
                                              'issued,link')

            # Skip if no results returned
            if crossref_result['message']['total-results'] == 0:
                break

            # Title according to crossref (i.e., best match returned)
            best_match = crossref_result['message']['items'][0]
            cr_title = best_match['title'][0]

            score = fuzz.partial_ratio(message.title, cr_title)
            if score > 90:
                citation_obj = Citation(cr_title=best_match['title'][0],
                                        cr_type=best_match.get('type'),
                                        cr_doi=best_match.get('DOI'),
                                        cr_issue=best_match.get('issue'),
                                        cr_volume=best_match.get('volume'),
                                        cr_page=best_match.get('page'),
                                        cr_pub_publisher=best_match.get('publisher'),
                                        cr_pub_title=best_match['container-title'][0] if 'container-title' in best_match else None,
                                        pub_issn=best_match['ISSN'][0] if 'ISSN' in best_match else None,
                                        pub_isbn=best_match['ISBN'][0] if 'ISBN' in best_match else None,
                                        cr_issued_date=self.partialDate(best_match.get('issued').get('date-parts')),
                                        cr_author=self.concatenate_authors(best_match.get('author')),
                                        cr_subject=",".join(best_match['subject']) if 'subject' in best_match else None
                                        )

                print(citation_obj)
            # print(json.dumps(crossref_result, indent=2))

        return crossref_results

    def partialDate(self, part_date):
        if len(part_date[0]) == 3:
            return date(part_date[0][0], part_date[0][1], part_date[0][2])
        elif len(part_date[0]) == 2:
            return date(part_date[0][0], part_date[0][1], 1)
        elif len(part_date[0]) == 1:
            return date(part_date[0][0], 7, 1)
        else:
            return None


    @staticmethod
    def concatenate_authors(authors):
        return "; ".join([", ".join((n['family'], n['given'])) for n in authors]) if authors is not None else None

    def make_citation(self, message_id, crossref_result):
        candidate = Citation()

    def validate_match(self):
        # TODO implement this method
        pass