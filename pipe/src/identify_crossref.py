from datetime import date
from habanero import Crossref
from fuzzywuzzy import fuzz
from pipe.src.db_objects import Citation


class IdentifyCrossRef:
    def __init__(self, messages):
        self.messages = messages
        self.mail_to = "s.vincent@nhm.ac.uk"

    def get_crossref_match(self):
        """
         Uses list of DOIs used to instantiate the class to query CrossRef
         and return article metadata.
         :return: List of identified Citation objects and list of unidentified message ids
         """
        cr = Crossref()
        cr.mailto = self.mail_to
        identified_citations = set()
        citation_results = []
        harvest_date = date.today().strftime('%Y-%m-%d')

        print("")
        print('Starting identification:')

        for message in self.messages:
            print(f"CrossRef check for {message.title}...")
            query = message.title if message.m_pub_title is None else f"{message.title} {message.m_pub_title}"
            pub_date = '1990-01-01' if message.m_pub_year is None else f"{message.m_pub_year}-01-01"
            crossref_result = cr.works(
                                    query=query,
                                    filter={'from_pub_date': pub_date},
                                    limit=1,
                                    select='DOI,title,author,type,subject,container-title,'
                                    'subject,publisher,issue,volume,page,ISSN,ISBN,published-online,'
                                    'issued,link')

            # Update crossref date and skip if no results returned
            if crossref_result['message']['total-results'] == 0:
                message.last_crossref_run = harvest_date
                continue

            # Compare original title to title of best match returned by CrossRef
            best_match = crossref_result['message']['items'][0]
            cr_title = 'Unknown' if 'title' not in best_match else best_match['title'][0]
            score = fuzz.partial_ratio(message.title, cr_title)

            # If similar, use to create Citation
            if score >= 90:
                cr_doi = best_match.get('DOI')

                if cr_doi is None:
                    # Update crossref date and skip if no doi in record
                    message.last_crossref_run = harvest_date
                    continue

                # If already seen, store the message id to update message in message_store with doi FK
                elif cr_doi in identified_citations:
                    # Update the message with citation, identification and run date
                    message.doi = cr_doi
                    message.id_status = True
                    message.last_crossref_run = harvest_date
                    continue
                else:
                    identified_citations.add(cr_doi)
                    message.doi = cr_doi
                    message.id_status = True
                    message.last_crossref_run = harvest_date

                    citation_results.append(Citation(author=self.concatenate_authors(best_match.get('author')),
                                            doi=best_match.get('DOI'),
                                            title=best_match['title'][0],
                                            type=best_match.get('type'),
                                            issued_date=self.partial_date(best_match.get('issued').get('date-parts')),
                                            subject=",".join(best_match['subject']) if 'subject' in best_match
                                            else None,
                                            pub_title=best_match['container-title'][0] if 'container-title' in
                                                                                          best_match else None,
                                            pub_publisher=best_match.get('publisher'),
                                            issn=best_match['ISSN'][0] if 'ISSN' in best_match else None,
                                            isbn=best_match['ISBN'][0] if 'ISBN' in best_match else None,
                                            issue=best_match.get('issue'),
                                            volume=best_match.get('volume'),
                                            page=best_match.get('page'),
                                            classification_id=3,
                                            nhm_sub=0
                                            ))

            else:
                # Update crossref date and skip if no good match found
                message.last_crossref_run = harvest_date

        print(f"{len(citation_results)} matches found, {len(self.messages) - len(citation_results)} not found.")
        print("")
        return citation_results, self.messages


    @staticmethod
    def partial_date(part_date):
        """
        Parses partial dates and fills in missing values
        :param part_date:
        :return: Date
        """
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
        """
        Concatenates author list
        :param authors:
        :return: String of authors, semicolon delimited
        """
        return "; ".join([", ".join((n.get('family', ''), n.get('given', ''))) for n in authors]) \
            if authors is not None else None
