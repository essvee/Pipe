from bs4 import BeautifulSoup


class GapiEmail(object):
    def __init__(self, harvested_date, sent_date, email_body, email_id, label=None):
        self.harvested_date = harvested_date
        self.sent_date = sent_date
        self.email_body = email_body
        self.email_id = email_id
        self.label = label
        self.messages = self.extract_messages()

    def extract_messages(self):
        # Turn body of email into html object
        soup = BeautifulSoup(self.email_body, 'html.parser')
        h3 = soup("h3")

        all_messages = []

        for i in h3:
            result = {'label': self.label}

            # Gets PDF/HTML indicator, if present
            if i.span:
                result['format'] = i.span.text
            else:
                result['format'] = "UNKNOWN"

            # Gets author/journal/pub date
            bib_details = i.next_sibling
            result['bib_details'] = bib_details.text

            # Gets snippet matching search query
            snippet = bib_details.next_sibling
            result['snippet'] = " ".join(snippet.stripped_strings).replace("…", "")

            # Gets title
            result['title'] = i.find('a', class_="gse_alrt_title").text

            all_messages.append(result)

        return all_messages
