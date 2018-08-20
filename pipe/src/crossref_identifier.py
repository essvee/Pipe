from habanero import Crossref
from fuzzywuzzy import fuzz


class CrossRefIdentifier:
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
                                       query_container_title=message.m_pub_title, rows=1)

            # Title according to crossref (i.e., best match returned)
            cr_title = crossref_result['message']['items'][0]['title'][0]

            # Snip both strings down to the length of the shortest title to allow fair comparison
            substring_length = min(len(cr_title), len(message.title))

            if message.title[: substring_length] == cr_title[:substring_length]:
                crossref_results.append(crossref_result['message']['items'][0])
                # TODO use to make Citation objects and stash for return
            else:
                suspicious_match.append(crossref_result['message']['items'][0])

        return crossref_results

    def validate_match(self):
        # TODO implement this method
        pass