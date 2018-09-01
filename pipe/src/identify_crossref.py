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
        identified_citations = {}
        unidentified_citations = []
        harvest_date = date.today().strftime('%Y-%m-%d')

        for message in self.messages:
            print(f"Starting crossref check for {message.title}. id: {message.message_id}")

            crossref_result = cr.works(query_title=message.title,
                                       query_author=message.m_author,
                                       query_container_title=message.m_pub_title, rows=1,
                                       select='DOI,title,author,type,subject,container-title,'
                                              'subject,publisher,issue,volume,page,ISSN,ISBN,published-online,'
                                              'issued,link')

            # Skip if no results returned
            if crossref_result['message']['total-results'] == 0:
                unidentified_citations.append((harvest_date, message.message_id))
                continue

            # Compare original title to title of best match returned by CrossRef
            best_match = crossref_result['message']['items'][0]
            cr_title = best_match['title'][0]
            score = fuzz.partial_ratio(message.title, cr_title)

            # If similar, use to create Citation
            if score > 90:
                cr_doi = best_match.get('DOI')

                if cr_doi is None:
                    unidentified_citations.append((harvest_date, message.message_id))
                    continue

                # If already seen, store the message id to update message in message_store with doi FK
                elif cr_doi in identified_citations:
                    unidentified_citations.append((harvest_date, message.message_id))

                else:
                    print(best_match['issued'])
                    result = Citation(cr_title=best_match['title'][0],
                                      cr_type=best_match.get('type'),
                                      cr_doi=best_match.get('DOI'),
                                      cr_issue=best_match.get('issue'),
                                      cr_volume=best_match.get('volume'),
                                      cr_page=best_match.get('page'),
                                      cr_pub_publisher=best_match.get('publisher'),
                                      cr_pub_title=best_match['container-title'][0] if 'container-title' in best_match
                                      else None,
                                      pub_issn=best_match['ISSN'][0] if 'ISSN' in best_match else None,
                                      pub_isbn=best_match['ISBN'][0] if 'ISBN' in best_match else None,
                                      cr_issued_date=self.partial_date(best_match.get('issued').get('date-parts')),
                                      message_ids=[message.message_id],
                                      cr_author=self.concatenate_authors(best_match.get('author')),
                                      cr_subject=",".join(best_match['subject']) if 'subject' in best_match else None
                                      )

                    identified_citations[cr_doi] = result
            else:
                unidentified_citations.append((harvest_date, message.message_id))

        return identified_citations, unidentified_citations

    @staticmethod
    def partial_date(part_date):
        if part_date[0][0] is None:
            return None
        elif len(part_date[0]) == 3:
            return date(part_date[0][0], part_date[0][1], part_date[0][2])
        elif len(part_date[0]) == 2:
            return date(part_date[0][0], part_date[0][1], 1)
        elif len(part_date[0]) == 1:
            return date(part_date[0][0], 7, 1)
        else:
            return None

    @staticmethod
    def concatenate_authors(authors):
        return "; ".join([", ".join((n.get('family', ''), n.get('given', ''))) for n in authors]) \
            if authors is not None else None
